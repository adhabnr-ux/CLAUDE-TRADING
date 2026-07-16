#!/usr/bin/env python3
"""Verify vendored upstream snapshots without importing or executing them."""

from __future__ import annotations

import hashlib
import json
import stat
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "third_party/snapshots.json"
ENTRY_KEYS = {
    "name",
    "source_url",
    "upstream_ref",
    "commit",
    "tree",
    "archive_sha256",
    "license",
    "file_count",
    "total_bytes",
    "local_root",
    "path_rewrites",
}
ACTIVE_INSTRUCTION_FILES = {
    "agents.md",
    "claude.md",
    "claude.local.md",
}
ACTIVE_INSTRUCTION_DIRECTORIES = {
    ".agents",
    ".claude",
}


class SnapshotError(RuntimeError):
    """A vendored snapshot no longer matches its reviewed upstream tree."""


def _git_hash(kind: str, payload: bytes) -> bytes:
    header = f"{kind} {len(payload)}\0".encode("ascii")
    return hashlib.sha1(header + payload).digest()


def _tree_hash(files: dict[PurePosixPath, tuple[str, bytes]]) -> str:
    root: dict[str, object] = {}
    for relative, value in files.items():
        node = root
        for component in relative.parts[:-1]:
            child = node.setdefault(component, {})
            if not isinstance(child, dict):
                raise SnapshotError(f"path collision at {relative}")
            node = child
        name = relative.name
        if name in node:
            raise SnapshotError(f"duplicate virtual path: {relative}")
        node[name] = value

    def digest_tree(node: dict[str, object]) -> bytes:
        rows: list[tuple[bytes, bytes]] = []
        for name, value in node.items():
            name_bytes = name.encode("utf-8")
            if isinstance(value, dict):
                object_id = digest_tree(value)
                sort_key = name_bytes + b"/"
                row = b"40000 " + name_bytes + b"\0" + object_id
            else:
                mode, content = value
                object_id = _git_hash("blob", content)
                sort_key = name_bytes
                row = mode.encode("ascii") + b" " + name_bytes + b"\0" + object_id
            rows.append((sort_key, row))
        payload = b"".join(row for _, row in sorted(rows, key=lambda item: item[0]))
        return _git_hash("tree", payload)

    return digest_tree(root).hex()


def _virtual_path(local: PurePosixPath, rewrites: dict[str, str]) -> PurePosixPath:
    first, *rest = local.parts
    upstream_first = rewrites.get(first, first)
    candidate = PurePosixPath(upstream_first, *rest)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise SnapshotError(f"unsafe rewritten path: {candidate}")
    return candidate


def _snapshot_files(
    root: Path, rewrites: dict[str, str]
) -> tuple[dict[PurePosixPath, tuple[str, bytes]], int]:
    files: dict[PurePosixPath, tuple[str, bytes]] = {}
    total_bytes = 0
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise SnapshotError(f"symlinks are forbidden in snapshots: {path}")
        if path.is_dir():
            continue
        mode_value = path.stat(follow_symlinks=False).st_mode
        if not stat.S_ISREG(mode_value):
            raise SnapshotError(f"special files are forbidden in snapshots: {path}")
        relative = PurePosixPath(path.relative_to(root).as_posix())
        if relative.name.casefold() in ACTIVE_INSTRUCTION_FILES or any(
            component.casefold() in ACTIVE_INSTRUCTION_DIRECTORIES
            for component in relative.parts
        ):
            raise SnapshotError(
                f"active agent-instruction surface must be quarantined: {relative}"
            )
        virtual = _virtual_path(relative, rewrites)
        if virtual in files:
            raise SnapshotError(f"rewrites collide at upstream path: {virtual}")
        content = path.read_bytes()
        mode = "100755" if mode_value & 0o111 else "100644"
        files[virtual] = (mode, content)
        total_bytes += len(content)
    return files, total_bytes


def verify(manifest_path: Path = MANIFEST) -> list[str]:
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SnapshotError(f"cannot read snapshot manifest: {exc}") from exc
    if set(manifest) != {"schema_version", "snapshots"}:
        raise SnapshotError("snapshot manifest has unexpected top-level fields")
    if manifest["schema_version"] != 1:
        raise SnapshotError("unsupported snapshot manifest version")
    entries = manifest["snapshots"]
    if not isinstance(entries, list) or not entries:
        raise SnapshotError("snapshot manifest must contain entries")

    verified: list[str] = []
    names: set[str] = set()
    roots: set[Path] = set()
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != ENTRY_KEYS:
            raise SnapshotError("snapshot entry fields do not match the contract")
        name = entry["name"]
        if not isinstance(name, str) or not name or name in names:
            raise SnapshotError(f"invalid or duplicate snapshot name: {name!r}")
        names.add(name)
        for field, length in (("commit", 40), ("tree", 40), ("archive_sha256", 64)):
            value = entry[field]
            if not isinstance(value, str) or len(value) != length:
                raise SnapshotError(f"{name}: invalid {field}")
            try:
                int(value, 16)
            except ValueError as exc:
                raise SnapshotError(f"{name}: invalid {field}") from exc
        if entry["license"] not in {
            "MIT",
            "MIT (scope per upstream LICENSE note)",
        }:
            raise SnapshotError(f"{name}: only reviewed MIT snapshots are expected")
        if not str(entry["source_url"]).startswith("https://github.com/"):
            raise SnapshotError(f"{name}: source URL must be an HTTPS GitHub repository")

        relative_root = Path(entry["local_root"])
        if relative_root.is_absolute() or ".." in relative_root.parts:
            raise SnapshotError(f"{name}: unsafe local root")
        root = (ROOT / relative_root).resolve()
        third_party_root = (ROOT / "third_party").resolve()
        if not root.is_relative_to(third_party_root) or root in roots:
            raise SnapshotError(f"{name}: local root is invalid or duplicated")
        roots.add(root)
        if not root.is_dir():
            raise SnapshotError(f"{name}: snapshot root is missing")

        rewrites = entry["path_rewrites"]
        if not isinstance(rewrites, dict) or any(
            not isinstance(local, str)
            or not isinstance(upstream, str)
            or "/" in local
            or "/" in upstream
            or local in {"", ".", ".."}
            or upstream in {"", ".", ".."}
            for local, upstream in rewrites.items()
        ):
            raise SnapshotError(f"{name}: path rewrites must map top-level names")

        files, total_bytes = _snapshot_files(root, rewrites)
        if len(files) != entry["file_count"]:
            raise SnapshotError(
                f"{name}: expected {entry['file_count']} files, found {len(files)}"
            )
        if total_bytes != entry["total_bytes"]:
            raise SnapshotError(
                f"{name}: expected {entry['total_bytes']} bytes, found {total_bytes}"
            )
        actual_tree = _tree_hash(files)
        if actual_tree != entry["tree"]:
            raise SnapshotError(
                f"{name}: tree mismatch: expected {entry['tree']}, found {actual_tree}"
            )
        license_path = root / "LICENSE"
        if not license_path.is_file():
            raise SnapshotError(f"{name}: upstream LICENSE is missing")
        verified.append(
            f"{name}: {entry['commit']} ({len(files)} files, tree {actual_tree})"
        )
    return verified


def main() -> int:
    try:
        rows = verify()
    except SnapshotError as exc:
        print(f"snapshot verification failed: {exc}")
        return 1
    for row in rows:
        print(f"verified upstream snapshot: {row}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

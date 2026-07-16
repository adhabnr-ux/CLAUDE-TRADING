from __future__ import annotations

import fcntl
import hashlib
import os
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, TextIO

from .risk import RiskRejected


@contextmanager
def account_lock(account_id: str) -> Iterator[None]:
    """Fail closed when another process on this host owns the paper account."""
    normalized = account_id.strip().lower()
    if not normalized:
        raise RiskRejected("ALPACA_EXPECTED_ACCOUNT_ID is required for account locking")
    digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:24]
    path = Path(tempfile.gettempdir()) / f"bulltrader-account-{digest}.lock"
    descriptor = os.open(path, os.O_CREAT | os.O_RDWR, 0o600)
    os.fchmod(descriptor, 0o600)
    handle: TextIO = os.fdopen(descriptor, "r+")
    try:
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise RiskRejected("another trading gateway process owns this account on this host") from exc
        handle.seek(0)
        handle.truncate()
        handle.write(str(os.getpid()))
        handle.flush()
        os.fsync(handle.fileno())
        yield
    finally:
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        finally:
            handle.close()

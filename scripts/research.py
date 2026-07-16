#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from bulltrader.research import (  # noqa: E402
    ResearchError,
    append_pending_packet,
    ledger_path,
    packet_identity,
    pending_path,
    validate_ledger,
)
from bulltrader.policy import PolicyError, load_policy  # noqa: E402


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="Validate or atomically append profile-scoped research evidence packets"
    )
    sub = result.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate")
    validate.add_argument("--agent", choices=["bull", "aggro"], required=True)
    append = sub.add_parser("append")
    append.add_argument("--agent", choices=["bull", "aggro"], required=True)
    return result


def _require_agent_binding(agent: str) -> None:
    bound_agent = os.environ.get("TRADING_AGENT", "")
    if bound_agent not in {"bull", "aggro"}:
        raise ResearchError("TRADING_AGENT must be exactly bull or aggro")
    if bound_agent != agent:
        raise ResearchError(
            f"TRADING_AGENT is bound to {bound_agent}; refusing {agent} profile command"
        )


def main() -> int:
    args = parser().parse_args()
    path = ledger_path(ROOT, args.agent)
    try:
        policy = load_policy(args.agent, ROOT)
        market_source_max_age_minutes = int(
            policy.system["research_market_source_max_age_minutes"]
        )
        if args.command == "append":
            _require_agent_binding(args.agent)
            packet = append_pending_packet(
                ROOT,
                args.agent,
                market_source_max_age_minutes=market_source_max_age_minutes,
                allow_candidates=(
                    os.environ.get("BULL_RESEARCH_DISCOVERY_ONLY") != "1"
                ),
            )
            packets = validate_ledger(path, args.agent)
        else:
            packet = None
            packets = validate_ledger(path, args.agent)
        appended_identity = packet_identity(packet) if packet else None
        latest_identity = packet_identity(packets[-1]) if packets else None
    except (PolicyError, ResearchError) as exc:
        print(
            json.dumps(
                {"ok": False, "agent": args.agent, "ledger": str(path), "error": str(exc)},
                indent=2,
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        return 2
    print(
        json.dumps(
            {
                "ok": True,
                "agent": args.agent,
                "ledger": str(path),
                "packets": len(packets),
                "latest_packet_id": packets[-1]["packet_id"] if packets else None,
                "latest_packet_sha256": (
                    latest_identity["packet_sha256"] if latest_identity else None
                ),
                "appended_packet_id": packet["packet_id"] if packet else None,
                "appended_packet_sha256": (
                    appended_identity["packet_sha256"] if appended_identity else None
                ),
                "pending": str(pending_path(ROOT, args.agent)),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

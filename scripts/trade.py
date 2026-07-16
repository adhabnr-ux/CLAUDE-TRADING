#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from bulltrader.alpaca import AlpacaClient, BrokerError  # noqa: E402
from bulltrader.execution import execute_buy, execute_sell, reconcile  # noqa: E402
from bulltrader.lock import account_lock  # noqa: E402
from bulltrader.plan import PlanError, find_intent  # noqa: E402
from bulltrader.policy import PolicyError, load_policy  # noqa: E402
from bulltrader.research import ResearchError, require_current_candidate  # noqa: E402
from bulltrader.risk import RiskRejected  # noqa: E402


def _plan_path(agent: str) -> Path:
    return ROOT / "memory" / ("aggressive/research-log.md" if agent == "aggro" else "research-log.md")


def _decimal(value: str) -> Decimal:
    try:
        result = Decimal(value)
    except InvalidOperation as exc:
        raise argparse.ArgumentTypeError("must be numeric") from exc
    if not result.is_finite() or result <= 0 or result != result.to_integral_value():
        raise argparse.ArgumentTypeError("must be a positive whole-share quantity")
    return result


def _require_agent_binding(agent: str) -> None:
    bound_agent = os.environ.get("TRADING_AGENT", "").strip().lower()
    if bound_agent not in {"bull", "aggro"}:
        raise RiskRejected("TRADING_AGENT must be exactly bull or aggro")
    if bound_agent != agent:
        raise RiskRejected(
            f"TRADING_AGENT is bound to {bound_agent}; refusing {agent} profile command"
        )


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="Machine-enforced paper-trading risk and execution gateway"
    )
    sub = result.add_subparsers(dest="command", required=True)

    buy = sub.add_parser("buy", help="validate today's plan and execute one bounded limit entry")
    buy.add_argument("--agent", choices=["bull", "aggro"], required=True)
    buy.add_argument("--symbol", required=True)
    buy.add_argument("--dry-run", action="store_true")

    sell = sub.add_parser("sell", help="execute a planned trim/exit or verified midday loss cut")
    sell.add_argument("--agent", choices=["bull", "aggro"], required=True)
    sell.add_argument("--symbol", required=True)
    sell.add_argument("--qty", required=True, type=_decimal)
    sell.add_argument("--trigger", choices=["planned", "midday_loss"], required=True)
    sell.add_argument("--reason", required=True)

    audit = sub.add_parser("reconcile", help="compare broker positions with protective orders")
    audit.add_argument("--agent", choices=["bull", "aggro"], required=True)
    audit.add_argument("--repair", action="store_true")
    return result


def _execute(args: argparse.Namespace, policy, client: AlpacaClient, now: datetime) -> int:
    control_path = ROOT / "memory" / "control.md"
    if args.command == "reconcile":
        result = reconcile(
            client=client,
            policy=policy,
            agent=args.agent,
            repair=args.repair,
            control_path=control_path,
            root=ROOT,
        )
        print(json.dumps(result.__dict__, indent=2, sort_keys=True))
        return 0 if result.ok else 2

    symbol = args.symbol.upper()
    today = now.astimezone(__import__("zoneinfo").ZoneInfo(policy.system["timezone"])).date()
    if args.command == "buy":
        intent = find_intent(_plan_path(args.agent), policy, symbol, "buy", today)
        result = execute_buy(
            client=client,
            policy=policy,
            agent=args.agent,
            intent=intent,
            now=now,
            control_path=control_path,
            fresh_buy_guard=lambda: require_current_candidate(
                ROOT,
                args.agent,
                symbol,
                now,
                str(policy.system["timezone"]),
                thesis=intent.thesis,
                invalidation=intent.invalidation,
                review_by=intent.review_by,
                candidate_max_age_minutes=int(
                    policy.system["research_candidate_max_age_minutes"]
                ),
                market_source_max_age_minutes=int(
                    policy.system["research_market_source_max_age_minutes"]
                ),
            ),
            root=ROOT,
            dry_run=args.dry_run,
        )
    else:
        intent = None
        if args.trigger == "planned":
            plan_path = _plan_path(args.agent)
            try:
                intent = find_intent(plan_path, policy, symbol, "trim", today)
            except PlanError:
                intent = find_intent(plan_path, policy, symbol, "exit", today)
        result = execute_sell(
            client=client,
            policy=policy,
            agent=args.agent,
            symbol=symbol,
            qty=args.qty,
            trigger=args.trigger,
            reason=args.reason,
            intent=intent,
            now=now,
            control_path=control_path,
            root=ROOT,
        )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def main() -> int:
    args = parser().parse_args()
    now = datetime.now(timezone.utc)
    try:
        _require_agent_binding(args.agent)
        policy = load_policy(args.agent, ROOT)
        expected_account_id = os.environ.get("ALPACA_EXPECTED_ACCOUNT_ID", "")
        with account_lock(expected_account_id):
            client = AlpacaClient.from_env(policy)
            return _execute(args, policy, client, now)
    except (BrokerError, PlanError, PolicyError, ResearchError, RiskRejected) as exc:
        print(json.dumps({"status": "blocked", "error": str(exc)}, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

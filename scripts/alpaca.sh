#!/usr/bin/env bash
# Alpaca REST API helper for the Bull trading agent.
# Credentials are read from environment variables only — never from repo files.
set -euo pipefail

BASE_URL="${ALPACA_BASE_URL:-https://paper-api.alpaca.markets}"
DATA_URL="https://data.alpaca.markets"
CANONICAL_PAPER_URL="https://paper-api.alpaca.markets"

if [[ "${BASE_URL%/}" != "$CANONICAL_PAPER_URL" ]]; then
  echo "ERROR: refusing non-canonical Alpaca endpoint: ${BASE_URL}" >&2
  exit 64
fi

if [[ -z "${ALPACA_API_KEY_ID:-}" || -z "${ALPACA_API_SECRET_KEY:-}" || -z "${ALPACA_EXPECTED_ACCOUNT_ID:-}" ]]; then
  echo "ERROR: ALPACA_API_KEY_ID, ALPACA_API_SECRET_KEY, and ALPACA_EXPECTED_ACCOUNT_ID must be set." >&2
  exit 1
fi

AUTH=(-H "APCA-API-KEY-ID: ${ALPACA_API_KEY_ID}" -H "APCA-API-SECRET-KEY: ${ALPACA_API_SECRET_KEY}")
JSON=(-H "Content-Type: application/json")

usage() {
  cat <<'EOF'
Usage: ./scripts/alpaca.sh <command> [args]

Account & portfolio:
  account                          Account summary (equity, cash, buying power)
  positions                        All open positions
  position <SYM>                   One position
  history [period] [timeframe]     Portfolio equity history (default 1M / 1D)
  orders [status] [limit]          Orders (status: open|closed|all; default all/50)
  calendar <start> <end>           Exchange sessions (YYYY-MM-DD dates)

Market data:
  clock                            Market open/closed + next open/close
  snapshot <SYM>                   Latest trade/quote/day bar for a symbol
  quote <SYM>                      Latest quote
  bars <SYM> [timeframe] [limit]   Historical bars (default 1Day / 30)

Trading:
  MUTATIONS ARE DISABLED HERE. Use scripts/trade.py so every order passes the
  machine-enforced paper endpoint, plan, idempotency, risk, and protection gates.
EOF
}

cmd="${1:-help}"; shift || true

ACCOUNT_JSON="$(curl --fail-with-body -sS "${AUTH[@]}" "${BASE_URL}/v2/account")"
ACTUAL_ACCOUNT_ID="$(python3 -c 'import json,sys; value=json.load(sys.stdin).get("id"); print(value if isinstance(value,str) else "")' <<<"$ACCOUNT_JSON")"
if [[ -z "$ACTUAL_ACCOUNT_ID" || "$ACTUAL_ACCOUNT_ID" != "$ALPACA_EXPECTED_ACCOUNT_ID" ]]; then
  echo "ERROR: Alpaca account fingerprint mismatch; refusing all broker/data access." >&2
  exit 65
fi

require_symbol() {
  [[ "${1:-}" =~ ^[A-Z][A-Z0-9.-]{0,9}$ ]] || {
    echo "ERROR: invalid symbol" >&2
    exit 64
  }
}

require_date() {
  [[ "${1:-}" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] || {
    echo "ERROR: date must be YYYY-MM-DD" >&2
    exit 64
  }
}

case "$cmd" in
  account)
    [[ $# -eq 0 ]] || { echo "ERROR: account takes no arguments" >&2; exit 64; }
    printf '%s' "$ACCOUNT_JSON"
    ;;
  positions)
    [[ $# -eq 0 ]] || { echo "ERROR: positions takes no arguments" >&2; exit 64; }
    curl --fail-with-body -sS "${AUTH[@]}" "${BASE_URL}/v2/positions"
    ;;
  position)
    [[ $# -eq 1 ]] || { echo "ERROR: position requires one symbol" >&2; exit 64; }
    require_symbol "$1"
    curl --fail-with-body -sS "${AUTH[@]}" "${BASE_URL}/v2/positions/$1"
    ;;
  history)
    [[ $# -le 2 && "${1:-1M}" =~ ^[0-9]+[A-Za-z]+$ && "${2:-1D}" =~ ^[0-9]+[A-Za-z]+$ ]] || { echo "ERROR: invalid history arguments" >&2; exit 64; }
    curl --fail-with-body -sS "${AUTH[@]}" "${BASE_URL}/v2/account/portfolio/history?period=${1:-1M}&timeframe=${2:-1D}"
    ;;
  orders)
    [[ $# -le 2 && "${1:-all}" =~ ^(open|closed|all)$ && "${2:-50}" =~ ^[0-9]+$ && ${2:-50} -ge 1 && ${2:-50} -le 500 ]] || { echo "ERROR: invalid orders arguments" >&2; exit 64; }
    curl --fail-with-body -sS "${AUTH[@]}" "${BASE_URL}/v2/orders?status=${1:-all}&limit=${2:-50}&direction=desc"
    ;;
  calendar)
    [[ $# -eq 2 ]] || { echo "ERROR: calendar requires start and end dates" >&2; exit 64; }
    require_date "$1"; require_date "$2"
    curl --fail-with-body -sS "${AUTH[@]}" "${BASE_URL}/v2/calendar?start=$1&end=$2"
    ;;
  clock)
    [[ $# -eq 0 ]] || { echo "ERROR: clock takes no arguments" >&2; exit 64; }
    curl --fail-with-body -sS "${AUTH[@]}" "${BASE_URL}/v2/clock"
    ;;
  snapshot|quote)
    [[ $# -eq 1 ]] || { echo "ERROR: $cmd requires one symbol" >&2; exit 64; }
    require_symbol "$1"
    suffix="snapshot"; [[ "$cmd" == "quote" ]] && suffix="quotes/latest"
    curl --fail-with-body -sS "${AUTH[@]}" "${DATA_URL}/v2/stocks/$1/${suffix}?feed=iex"
    ;;
  bars)
    [[ $# -ge 1 && $# -le 3 ]] || { echo "ERROR: bars requires symbol and optional timeframe/limit" >&2; exit 64; }
    require_symbol "$1"
    [[ "${2:-1Day}" =~ ^[0-9]+[A-Za-z]+$ && "${3:-30}" =~ ^[0-9]+$ && ${3:-30} -ge 1 && ${3:-30} -le 10000 ]] || { echo "ERROR: invalid bars arguments" >&2; exit 64; }
    curl --fail-with-body -sS "${AUTH[@]}" "${DATA_URL}/v2/stocks/$1/bars?timeframe=${2:-1Day}&limit=${3:-30}&feed=iex"
    ;;
  buy|sell|buy-limit|trailing-stop|close|cancel)
    echo "ERROR: direct broker mutations are disabled. Use python3 scripts/trade.py --help." >&2
    exit 64
    ;;
  help|*) usage ;;
esac
echo

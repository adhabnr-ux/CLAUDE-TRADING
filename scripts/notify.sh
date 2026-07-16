#!/usr/bin/env bash
# Send a Telegram notification via the BullTheBullishBot.
# Credentials are read from environment variables only.
set -euo pipefail

msg="${1:?usage: ./scripts/notify.sh \"message\"}"

if [[ -z "${TELEGRAM_BOT_TOKEN:-}" || -z "${TELEGRAM_CHAT_ID:-}" ]]; then
  echo "ERROR: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set as environment variables." >&2
  exit 1
fi

curl --fail-with-body -sS -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  --data-urlencode "chat_id=${TELEGRAM_CHAT_ID}" \
  --data-urlencode "text=${msg}"
echo

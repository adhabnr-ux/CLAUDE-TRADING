#!/usr/bin/env bash
# Send a Telegram notification via the trusted Python delivery helper.
set -euo pipefail

msg="${1:?usage: ./scripts/notify.sh \"message\"}"
shift
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "${script_dir}/notify.py" "${msg}" "$@"

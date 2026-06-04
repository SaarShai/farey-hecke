#!/usr/bin/env bash
# scripts/dispatch_mimo.sh
#
# Thin wrapper around the Xiaomi MiMo Open Platform chat-completions API
# (OpenAI-compatible). Reads a prompt from a file or stdin, returns the
# model's text output on stdout, and is safe to use as a building block
# for piping in larger dispatch pipelines.
#
# Usage:
#   scripts/dispatch_mimo.sh [options] <prompt-file-or-->
#   echo "hello" | scripts/dispatch_mimo.sh -
#
# Options:
#   --model NAME          Model id (default: mimo-v2-flash, the cheapest tested)
#                         Available chat models (probed 2026-05-09):
#                           mimo-v2-flash    (cheapest, fastest)
#                           mimo-v2-omni
#                           mimo-v2-pro
#                           mimo-v2.5
#                           mimo-v2.5-pro    (flagship)
#   --max-tokens N        Max output tokens (default: 8000)
#   --system-file PATH    Optional system prompt loaded from PATH
#   --temperature F       Sampling temperature (default: 0.7)
#   --raw                 Emit the raw JSON response instead of just text
#   -h | --help           Show this help and exit
#
# Behaviour:
#   - Prompt is read from the FILE argument, or stdin when the argument is "-".
#   - Always sends "thinking":{"type":"disabled"} per the delta-machine
#     roadmap (without it, reasoning models can return empty content).
#   - On HTTP != 200 the full response body is dumped to stderr and the
#     script exits with code 2.
#   - The API key is loaded from ~/.farey_api_keys (env var MIMO_API_KEY).
#     The key is never echoed; any error path prints only a masked form
#     (first 6 + last 4 chars).
#
# Exit codes:
#   0  success (response text on stdout)
#   1  usage / config error (missing key, bad arguments)
#   2  API call failed (non-200 or empty content)

set -euo pipefail

# ---------- helpers ----------------------------------------------------------

err() { printf '%s\n' "$*" >&2; }

mask_key() {
  # Print first 6 + last 4 chars; never the middle.
  local k="${1:-}"
  if [ -z "$k" ]; then printf '<empty>'; return; fi
  if [ "${#k}" -le 10 ]; then printf '<masked>'; return; fi
  printf '%s...%s' "${k:0:6}" "${k: -4}"
}

usage() {
  sed -n '2,30p' "$0"
}

# ---------- arg parsing ------------------------------------------------------

MODEL="mimo-v2-flash"
MAX_TOKENS=8000
SYSTEM_FILE=""
TEMPERATURE="0.7"
RAW=0
PROMPT_SRC=""

while [ $# -gt 0 ]; do
  case "$1" in
    --model)        MODEL="$2"; shift 2 ;;
    --max-tokens)   MAX_TOKENS="$2"; shift 2 ;;
    --system-file)  SYSTEM_FILE="$2"; shift 2 ;;
    --temperature)  TEMPERATURE="$2"; shift 2 ;;
    --raw)          RAW=1; shift ;;
    -h|--help)      usage; exit 0 ;;
    --)             shift; PROMPT_SRC="${1:-}"; shift || true; break ;;
    -)              PROMPT_SRC="-"; shift ;;
    -*)             err "Unknown option: $1"; usage >&2; exit 1 ;;
    *)              PROMPT_SRC="$1"; shift ;;
  esac
done

if [ -z "$PROMPT_SRC" ]; then
  err "ERROR: missing <prompt-file-or-->. See --help."
  exit 1
fi

# ---------- key loading ------------------------------------------------------

if [ ! -f ~/.farey_api_keys ]; then
  err "ERROR: ~/.farey_api_keys not found."
  exit 1
fi
# shellcheck disable=SC1090
set -a; . ~/.farey_api_keys; set +a

if [ -z "${MIMO_API_KEY:-}" ]; then
  err "ERROR: MIMO_API_KEY not set after sourcing ~/.farey_api_keys."
  exit 1
fi

# ---------- read prompt ------------------------------------------------------

if [ "$PROMPT_SRC" = "-" ]; then
  PROMPT_TEXT="$(cat)"
else
  if [ ! -r "$PROMPT_SRC" ]; then
    err "ERROR: cannot read prompt file: $PROMPT_SRC"
    exit 1
  fi
  PROMPT_TEXT="$(cat -- "$PROMPT_SRC")"
fi

SYSTEM_TEXT=""
if [ -n "$SYSTEM_FILE" ]; then
  if [ ! -r "$SYSTEM_FILE" ]; then
    err "ERROR: cannot read system file: $SYSTEM_FILE"
    exit 1
  fi
  SYSTEM_TEXT="$(cat -- "$SYSTEM_FILE")"
fi

if [ -z "$PROMPT_TEXT" ]; then
  err "ERROR: empty prompt."
  exit 1
fi

# ---------- build payload (python3 for safe JSON escaping) -------------------

PAYLOAD_FILE="$(mktemp -t mimo_payload.XXXXXX)"
RESPONSE_FILE="$(mktemp -t mimo_response.XXXXXX)"
trap 'rm -f "$PAYLOAD_FILE" "$RESPONSE_FILE"' EXIT

PROMPT_TEXT="$PROMPT_TEXT" \
SYSTEM_TEXT="$SYSTEM_TEXT" \
MODEL="$MODEL" \
MAX_TOKENS="$MAX_TOKENS" \
TEMPERATURE="$TEMPERATURE" \
python3 - "$PAYLOAD_FILE" <<'PY'
import json, os, sys
out_path = sys.argv[1]
messages = []
sys_text = os.environ.get("SYSTEM_TEXT", "")
if sys_text.strip():
    messages.append({"role": "system", "content": sys_text})
messages.append({"role": "user", "content": os.environ["PROMPT_TEXT"]})
payload = {
    "model": os.environ["MODEL"],
    "messages": messages,
    "max_tokens": int(os.environ["MAX_TOKENS"]),
    "temperature": float(os.environ["TEMPERATURE"]),
    # Mandatory: without this, reasoning models return empty content.
    "thinking": {"type": "disabled"},
}
with open(out_path, "w") as f:
    json.dump(payload, f)
PY

# ---------- call API ---------------------------------------------------------

API_URL="https://api.xiaomimimo.com/v1/chat/completions"

HTTP_CODE="$(
  curl -sS -m 120 \
    -o "$RESPONSE_FILE" \
    -w '%{http_code}' \
    -H "Authorization: Bearer ${MIMO_API_KEY}" \
    -H "Content-Type: application/json" \
    -X POST \
    --data-binary "@${PAYLOAD_FILE}" \
    "$API_URL" || echo "000"
)"

if [ "$HTTP_CODE" != "200" ]; then
  err "ERROR: MiMo API HTTP $HTTP_CODE (key $(mask_key "$MIMO_API_KEY"), model $MODEL)"
  err "--- response body ---"
  # Scrub the key out of the body just in case the API echoed it back.
  if [ -n "${MIMO_API_KEY:-}" ]; then
    sed "s|${MIMO_API_KEY}|<MIMO_API_KEY:masked>|g" "$RESPONSE_FILE" >&2 || cat "$RESPONSE_FILE" >&2
  else
    cat "$RESPONSE_FILE" >&2
  fi
  err ""
  exit 2
fi

# ---------- parse + emit -----------------------------------------------------

if [ "$RAW" = "1" ]; then
  cat "$RESPONSE_FILE"
  exit 0
fi

CONTENT="$(
python3 - "$RESPONSE_FILE" <<'PY'
import json, sys
with open(sys.argv[1]) as f:
    data = json.load(f)
choices = data.get("choices") or []
if not choices:
    print("__MIMO_EMPTY__")
    sys.exit(0)
msg = choices[0].get("message") or {}
content = msg.get("content") or ""
sys.stdout.write(content)
PY
)"

if [ -z "$CONTENT" ] || [ "$CONTENT" = "__MIMO_EMPTY__" ]; then
  err "ERROR: empty content from MiMo (model $MODEL, key $(mask_key "$MIMO_API_KEY"))."
  err "--- raw body ---"
  if [ -n "${MIMO_API_KEY:-}" ]; then
    sed "s|${MIMO_API_KEY}|<MIMO_API_KEY:masked>|g" "$RESPONSE_FILE" >&2 || cat "$RESPONSE_FILE" >&2
  else
    cat "$RESPONSE_FILE" >&2
  fi
  exit 2
fi

printf '%s\n' "$CONTENT"

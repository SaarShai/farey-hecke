#!/usr/bin/env bash
# Poll Aristotle for one or more dispatched projects.
#
# Project IDs and labels are read from `scripts/aristotle_project_ids.txt`,
# one per line in the form
#     <project-id>  <label>
# Lines starting with `#` and blank lines are ignored.
#
# Currently tracked:
#   424973ae-8e9a-4ef1-8a6d-970ffa3b88ad   SmoothedDwfFormula  (P3b dispatch, 2026-05-09)
#   8e608890-f0ba-4a89-bbb0-a63b5bcab697   R1_B_plus           (R1 dispatch,  2026-05-09)
#
# Usage:
#   ./scripts/poll_aristotle.sh                       # one-shot status of all tracked projects
#   ./scripts/poll_aristotle.sh --watch               # poll every 15 min until ALL are COMPLETE
#   ./scripts/poll_aristotle.sh --download <label>    # download result for the named project
#   ./scripts/poll_aristotle.sh --download SmoothedDwfFormula
#   ./scripts/poll_aristotle.sh --download R1_B_plus
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ID_FILE="$REPO_ROOT/scripts/aristotle_project_ids.txt"
VENV="/tmp/aristotle_venv"
RESULT_DIR="$REPO_ROOT/formal-conjectures"

# Sanity: load API key
if [ ! -f ~/.farey_api_keys ]; then
  echo "ERROR: ~/.farey_api_keys not found. Cannot authenticate to Aristotle."
  exit 1
fi
set -a; . ~/.farey_api_keys; set +a
if [ -z "${ARISTOTLE_API_KEY:-}" ]; then
  echo "ERROR: ARISTOTLE_API_KEY not set after sourcing ~/.farey_api_keys."
  exit 1
fi

# Sanity: aristotlelib venv
if [ ! -d "$VENV" ]; then
  echo "Setting up aristotlelib venv at $VENV (one-time, ~30s)..."
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install --quiet --upgrade pip
  "$VENV/bin/pip" install --quiet aristotlelib==1.0.1
fi

ARISTOTLE="$VENV/bin/aristotle"
if [ ! -x "$ARISTOTLE" ]; then
  echo "ERROR: $ARISTOTLE not executable; reinstall the venv."
  exit 1
fi

if [ ! -f "$ID_FILE" ]; then
  echo "ERROR: project-id config $ID_FILE not found."
  exit 1
fi

# Load (id, label) pairs from $ID_FILE into parallel arrays.
IDS=()
LABELS=()
while IFS= read -r line; do
  # strip comments and blank lines
  line="${line%%#*}"
  line="$(echo "$line" | awk '{$1=$1};1')"  # trim
  [ -z "$line" ] && continue
  id=$(echo "$line"   | awk '{print $1}')
  lbl=$(echo "$line"  | awk '{print $2}')
  if [ -z "$id" ] || [ -z "$lbl" ]; then
    echo "WARN: skipping malformed line: $line"; continue
  fi
  IDS+=("$id"); LABELS+=("$lbl")
done < "$ID_FILE"

if [ ${#IDS[@]} -eq 0 ]; then
  echo "ERROR: no project IDs found in $ID_FILE."; exit 1
fi

# Status of all tracked projects (one-shot). Returns 0 if all COMPLETE,
# 1 otherwise.
status_all() {
  local listing
  listing="$("$ARISTOTLE" list --limit 50 2>/dev/null)"
  local all_done=0
  local i
  for i in "${!IDS[@]}"; do
    local id="${IDS[$i]}"
    local lbl="${LABELS[$i]}"
    local row
    row=$(echo "$listing" | grep -F "$id" || true)
    if [ -z "$row" ]; then
      printf "  %-22s  %s  NOT_FOUND_IN_LIST\n" "$lbl" "$id"
      all_done=1
    else
      local status
      status=$(echo "$row" | awk '{print $2}')
      printf "  %-22s  %s  %s\n" "$lbl" "$id" "$status"
      case "$status" in
        COMPLETE|COMPLETE_WITH_ERRORS|FAILED|OUT_OF_BUDGET|CANCELLED) ;;
        *) all_done=1 ;;
      esac
    fi
  done
  return $all_done
}

# Download the result for one labeled project.
download_one() {
  local target_label="$1"
  local i
  for i in "${!LABELS[@]}"; do
    if [ "${LABELS[$i]}" = "$target_label" ]; then
      local id="${IDS[$i]}"
      local lbl="${LABELS[$i]}"
      local tgz="$RESULT_DIR/${lbl}_aristotle_result.tar.gz"
      local extract_dir="$RESULT_DIR/${lbl}_aristotle_result_extract"
      echo "Fetching result for $lbl ($id) → $tgz ..."
      "$ARISTOTLE" result "$id" --destination "$tgz"
      if [ -f "$tgz" ]; then
        echo "Saved tarball: $tgz"
        mkdir -p "$extract_dir"
        tar xzf "$tgz" -C "$extract_dir"
        local lean_file
        lean_file=$(find "$extract_dir" -name "${lbl}*.lean" -type f | head -1)
        if [ -z "$lean_file" ]; then
          # Fallback: any .lean file with the label substring (case-insensitive)
          lean_file=$(find "$extract_dir" -name "*.lean" -type f | grep -i "$lbl" | head -1 || true)
        fi
        if [ -n "$lean_file" ]; then
          cp "$lean_file" "$RESULT_DIR/${lbl}_full.lean"
          echo "Saved Lean file: $RESULT_DIR/${lbl}_full.lean"
        else
          echo "WARN: no ${lbl}*.lean found in extracted tarball; check $extract_dir manually."
        fi
        return 0
      else
        echo "ERROR: result download failed."; return 1
      fi
    fi
  done
  echo "ERROR: label '$target_label' not found in $ID_FILE."
  echo "Known labels: ${LABELS[*]}"
  return 1
}

case "${1:-status}" in
  --watch)
    echo "Watching ${#IDS[@]} project(s); Ctrl-C to stop."
    while true; do
      echo "---- $(date +'%Y-%m-%d %H:%M:%S') ----"
      if status_all; then
        echo "All tracked projects reached terminal status."
        exit 0
      fi
      sleep 900  # 15 minutes
    done
    ;;
  --download)
    target="${2:-}"
    if [ -z "$target" ]; then
      echo "Usage: $0 --download <label>"
      echo "Known labels: ${LABELS[*]}"
      exit 1
    fi
    download_one "$target"
    ;;
  status|*)
    echo "Polling ${#IDS[@]} project(s) from $ID_FILE..."
    status_all || true
    echo ""
    echo "Status legend: QUEUED → IN_PROGRESS → COMPLETE (or COMPLETE_WITH_ERRORS / FAILED)"
    echo "Run with --watch to poll every 15 min, or --download <label> to fetch a result."
    ;;
esac

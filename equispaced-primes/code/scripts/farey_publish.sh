#!/bin/bash
# Fresh Farey checkpoint publisher.
#
# Stages only relevant repo sections, commits a small checkpoint, and pushes
# only when explicitly requested and the remote is the canonical GitHub repo.

set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"

PUSH=0
MESSAGE="farey: checkpoint sync"

while [ $# -gt 0 ]; do
  case "$1" in
    --push) PUSH=1 ;;
    --message) MESSAGE="${2:-}"; shift ;;
    --message=*) MESSAGE="${1#*=}" ;;
    *) echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
  shift
done

REMOTE_EXPECTED="https://github.com/SaarShai/Primes-Equispaced.git"

STAGE_PATHS=()
while IFS= read -r path; do
  STAGE_PATHS+=("$path")
done < <(python3 - <<'PY'
from pathlib import Path
import subprocess

allow_patterns = [
    ".claude/agents/farey-publisher.md",
    ".claude/settings.json",
    "configs/settings.claude.json",
    "README.md",
    "HANDOFF.md",
    "L1_index.md",
    "L2_facts/*.md",
    "L4_archive/*.md",
    "log.md",
    "projects/farey-research/**",
    "projects/agents-triage/**/*.md",
    "projects/skill-crystallizer/**/*.py",
    "projects/skill-crystallizer/**/*.md",
    "scripts/farey_publish.sh",
    "raw/farey-archive/**",
]

status = subprocess.check_output(
    ["git", "ls-files", "--modified", "--others", "--exclude-standard"], text=True
)
items = []
for path in status.splitlines():
    rel = Path(path)
    if rel.exists() and any(rel.match(pattern) for pattern in allow_patterns):
        items.append(path)

for item in items:
    print(item)
PY
)

if [ "${#STAGE_PATHS[@]}" -eq 0 ]; then
  echo "No relevant Farey / Token Economy changes to publish."
  exit 0
fi

git add -- "${STAGE_PATHS[@]}"

if git diff --cached --quiet; then
  echo "Nothing staged after filtering."
  exit 0
fi

if ! git rev-parse --verify HEAD >/dev/null 2>&1; then
  git commit -m "$MESSAGE"
else
  git commit -m "$MESSAGE"
fi

if [ "$PUSH" -eq 1 ]; then
  CURRENT_REMOTE="$(git remote get-url origin 2>/dev/null || true)"
  if [ "$CURRENT_REMOTE" != "$REMOTE_EXPECTED" ]; then
    echo "Remote origin is not the canonical publish target: ${CURRENT_REMOTE:-<unset>}" >&2
    exit 3
  fi
  git push origin HEAD
fi

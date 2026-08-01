#!/usr/bin/env bash
# Disabled 2026-07-19: the matched-observable pointwise claim is false.
set -euo pipefail

cat >&2 <<'EOF'
ERROR: submission disabled.

Exact endpoint-inclusive arithmetic gives M(13) = -3 and
DeltaW(13) = -95083/180180 < 0, so the proposed pointwise sign relation is
false. The frozen scan also found zero agreements among 4,617 qualifying
primes through 100000. See:

  papers/nw-mertens-note/INTEGRAL_FAREY_KILL_TEST_REPORT_2026-07-19.md
  function-field/formal_conjectures_submission/PR3716_FOLLOWUP_DRAFT_2026-07-18.md

Do not push, post, open an issue, or open a PR for this withdrawn proposal.
EOF

exit 2

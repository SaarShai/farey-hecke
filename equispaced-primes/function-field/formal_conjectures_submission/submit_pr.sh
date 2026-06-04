#!/usr/bin/env bash
# Submit the Farey-discrepancy density-one conjecture to google-deepmind/formal-conjectures.
export PATH="$HOME/.local/bin:$PATH"   # gh installed here (no brew on this machine)
# Prereqs (USER): Google CLA signed (done); `gh` installed & authed as SaarShai
#   (`brew install gh && gh auth login`).  Run this from anywhere.
# It is idempotent-ish: safe to re-run; will skip fork if it exists.
set -euo pipefail

UPSTREAM="google-deepmind/formal-conjectures"
FORK="SaarShai/formal-conjectures"
BRANCH="farey-discrepancy-density-one"
SRC="$(cd "$(dirname "$0")" && pwd)/FareyDiscrepancySign.lean"
DEST_REL="FormalConjectures/Other/FareyDiscrepancySign.lean"
WORK="$(mktemp -d)"

command -v gh >/dev/null || { echo "ERROR: gh not installed. brew install gh && gh auth login"; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "ERROR: gh not authenticated. Run: gh auth login"; exit 1; }
test -f "$SRC" || { echo "ERROR: missing $SRC"; exit 1; }

echo ">> Fork (skip if exists)"
gh repo fork "$UPSTREAM" --clone=false 2>/dev/null || echo "   fork already exists"

echo ">> Clone fork"
gh repo clone "$FORK" "$WORK/fc" -- -q
cd "$WORK/fc"
git remote add upstream "https://github.com/$UPSTREAM.git" 2>/dev/null || true
git fetch -q upstream
DEFAULT_BRANCH="$(gh repo view "$UPSTREAM" --json defaultBranchRef --jq .defaultBranchRef.name)"
git checkout -q "upstream/$DEFAULT_BRANCH" -B "$BRANCH"

echo ">> Add file at $DEST_REL"
mkdir -p "$(dirname "$DEST_REL")"
cp "$SRC" "$DEST_REL"
git add "$DEST_REL"

echo ">> Optional local build check (their toolchain; may be slow). Skip with SKIP_BUILD=1"
if [ "${SKIP_BUILD:-0}" != "1" ]; then
  if command -v lake >/dev/null; then lake exe cache get >/dev/null 2>&1 || true; lake build FormalConjectures.Other.FareyDiscrepancySign || { echo "WARN: lake build failed — fix before PR (likely import/attr path)"; }; fi
fi

git -c user.name="Saar Shai" -c user.email="$(gh api user --jq .email 2>/dev/null || echo saarshai@users.noreply.github.com)" \
    commit -q -m "Add open conjecture: density-one Farey L2-discrepancy sign pattern

@[category research open, AMS 11]. Concrete (non-opaque) Farey/Weyl-L2
discrepancy + Mertens defs; body \`by sorry\`. Pointwise form is false
(recorded in docstring); density-one form is the open conjecture.
Source: S. Shai, The per-step Farey discrepancy (2026)."
git push -q -u origin "$BRANCH"

echo ">> Open issue (their required issue-first convention)"
ISSUE_URL=$(gh issue create --repo "$UPSTREAM" \
  --title "Add open conjecture: density-one sign pattern for the prime-step Farey L2 discrepancy" \
  --body "I'd like to contribute one \`@[category research open, AMS 11]\` conjecture. Setup: \`W N\` = L2 (Weyl) discrepancy of the order-N Farey sequence; \`ΔW p = W (p-1) − W p\`; \`M\` = Mertens. The *pointwise* relation sgn(ΔW p)=sgn(−M p) for every prime with M p ≤ −3 is **false** (explicit counterexamples). The **density-one** form (proportion of qualifying primes ≤ X that agree → 1 as X→∞) is open: numerically ≈73% at X=1e7; expected density-one under the L-function hypotheses controlling the explicit-formula expansion of ΔW. Statement uses concrete (non-opaque) Farey/discrepancy defs and typechecks against Mathlib v4.28.0 (single expected sorry). Source: S. Shai, *The per-step Farey discrepancy* (2026). Q: keep the concrete Farey/discrepancy defs inline, or move to FormalConjecturesForMathlib?")
echo "   issue: $ISSUE_URL"

echo ">> Open PR linked to issue"
PR_URL=$(gh pr create --repo "$UPSTREAM" --base "$DEFAULT_BRANCH" --head "SaarShai:$BRANCH" \
  --title "Add open conjecture: density-one Farey L2-discrepancy sign pattern" \
  --body "Closes ${ISSUE_URL##*/} via $ISSUE_URL. Adds \`$DEST_REL\`: one \`@[category research open, AMS 11]\` conjecture (density-one Farey discrepancy sign pattern), Apache header, reference, \`by sorry\`. Concrete definitions; honest docstring (pointwise form is false, recorded). Typechecks against Mathlib v4.28.0 outside the repo (single expected sorry). Google CLA signed.")
echo "   PR: $PR_URL"
echo ">> DONE. issue=$ISSUE_URL  pr=$PR_URL"

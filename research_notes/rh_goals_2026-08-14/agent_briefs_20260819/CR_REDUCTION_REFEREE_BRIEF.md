GOAL: Cold-adversarially referee committed candidate d8b7a44 for the RATE-A reduced constant and write only CR_REDUCTION_REFEREE.md.
IN-SCOPE: research_notes/rh_goals_2026-08-14/lane_g/CR_REDUCTION_SOL.md and its cited immutable sources; write only research_notes/rh_goals_2026-08-14/lane_g/CR_REDUCTION_REFEREE.md.
OUT-OF-SCOPE: Do not edit source theorem notes, MAP, tasks, any existing file, or git state; do not use files outside this worktree as evidence.

PHASE 0 — before any edit: reply with your plan and EVERY disagreement with this
brief, citing real files as evidence — or state what you checked before concluding
it is sound. Verify named APIs/paths/versions against the live repo before
planning. Silent compliance is a lane defect; silent scope additions are a lane
defect.

GATE (re-run, do not self-certify): your final output is judged by a SEPARATE
verifier on a machine check — not your done-claim. Return raw findings/data, not
"done". State attempts tried + abandoned and every assumption. If you produce a
file/artifact, say exactly what you changed; do NOT touch anything outside the
named scope. END with "READY FOR JUDGING", never "complete".

ACTIVE RULES:
- team-lead: Team-lead: leader plans+reviews only; builders do keystrokes; every claim cold-verified; one worker one lane; briefs self-contained (hooks don't fire in subagents).

DONE MEANS:
- Independently verify the source-invariant substitution C4=2^100 to C4'=2^62+1, including whether the proved atom bridge actually supports the sharper +1 rather than only 2^63.
- Independently reconstruct every formula and outward-rounding step leading to the primary and fallback constants, using /Users/za/.venvs/farey-rh/bin/python with flint.arb; include exact commands and output.
- Independently recompute the selected A0 logarithmic threshold and minimal strict integer cutoff for the primary constant; verify strictness at q and failure or equality at q-1.
- Attack scope, ledger strength, conditional inputs, wrap and pair coefficients, and the distinction between analytic-tail onset and full all-q closure; classify each candidate claim CONFIRMED, GAPS, or REFUTED.
- Write a self-contained append-only-style research_notes/rh_goals_2026-08-14/lane_g/CR_REDUCTION_REFEREE.md with source hashes, attack ledger, exact receipts, caveats, and a final verdict; state machine/full-operator/finite-block limits every time a promotion is summarized.

VERIFY: shasum source inputs; run the exact candidate receipt plus an independently written Arb script; run git diff --check and prove git status shows no changed path except CR_REDUCTION_REFEREE.md and this untracked brief; quote all relevant output and do not self-certify.

Specific attack list:
- Check BOUNDARY_ALPHA_THEOREM_SOL.md formulas line by line rather than trusting CR_REDUCTION_SOL.md prose.
- Resolve any mismatch between A_X^2 < 2^62, integer/rational coefficient ceilings, and a legal C4'=2^62+1.
- Verify positivity/monotonicity of every majorant before substituting a smaller C4.
- Confirm 38160259896392973127946053 is an upward integer ceiling and that one less is invalid; do likewise for fallback 76320519792785946239303038.
- Confirm q_transport=97418971860452658435229799565334786148 is the minimal strict integer threshold under the selected A0 formula, not a full-program q0.
- Search for hidden refutations or dependencies that make the candidate conditional or unusable.

LANE REPORT (hard shape — the orchestrator reads only this): summary <=200 words;
changed_paths (every file, exhaustive); evidence (exact commands + output lines
for each done-means criterion); attempts; assumptions; leftovers/concerns. End
with exactly one status line: STATUS: COMPLETE | COMPLETE_WITH_CONCERNS (list) |
BLOCKED (exact blocker + what you tried) — then the line READY FOR JUDGING. Raw
results only — no verdicts about your own work, no 'done'.

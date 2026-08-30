GOAL: Independently prove or reject the 2026-08-19 refutation of the q=8 CLOSED_CONTOUR_CERTIFIED interpretation and audit the stated q=9..12 blast radius
IN-SCOPE: Read repository code/receipts; write only research_notes/rh_goals_2026-08-14/lane_f/F8_R3B_REFUTATION_REFEREE.md
OUT-OF-SCOPE: No edits to correction blocks, receipts, engines, MAP, plans, git state, Kaggle, Aristotle, or external services
DONE MEANS: A cold standalone referee reconstructs the algorithm, tests the logical implications with explicit countermodels where applicable, and returns CONFIRMED, GAPS, or REFUTED for the correction
VERIFY: Exact source/hash/status searches, local no-write countermodel/replay commands, q=9..12 driver comparison, git diff --check, and final status limited to the referee file plus this leader-owned brief

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
- You are not alone. Do not alter any file except the one referee deliverable;
  do not stage, commit, stash, checkout, reset, or revert anything.
- Work cold. Inspect the original q=8 script and its imported engine before
  reading the appended correction verdict. Never strengthen a source.
- Receipts before claims: quote exact commands and decisive output. A numerical
  reproduction proves only what the algorithm computes, not a missing analytic
  implication.
- Every unproved conclusion is CONJECTURAL. This audit asks whether the
  certificate proves a zero, not whether the underlying determinant actually
  has or lacks a zero.

LANE REPORT (hard shape — the orchestrator reads only this): summary <=200 words;
changed_paths (every file, exhaustive); evidence (exact commands + output lines
for each done-means criterion); attempts; assumptions; leftovers/concerns. End
with exactly one status line: STATUS: COMPLETE | COMPLETE_WITH_CONCERNS (list) |
BLOCKED (exact blocker + what you tried) — then the line READY FOR JUDGING. Raw
results only — no verdicts about your own work, no 'done'.

## Mandatory attacks

1. Trace `f8_certify_r3b_flagship.py` from contour point generation through
   `certify_segment`, `Evaluator.det_ball`, the imported even engine, and the
   returned receipt fields. State exactly what set of points/sets is enclosed.
2. Decide whether endpoint nonzero balls plus
   `Re(B*conj(A))>0` logically imply nonvanishing on the segment interior.
   Supply an explicit entire scalar countermodel accepted at its endpoints but
   zero inside if the implication is false. Distinguish failure of a proof rule
   from evidence that the actual determinant vanishes.
3. Trace the trivial-sector tail actually used by q=8. Determine whether the
   observed finite determinant-increment ratios plus `q<0.85` have a proved
   theorem forcing all later increments to decay geometrically. If no such
   theorem is bound, give a finite-sequence/continuation countermodel showing
   why extrapolation from the observed window is insufficient.
4. Compare the geometry used by the determinant builder to
   `f8_certify_tb_blocks.py::EXACT_FACTORS`; determine whether any theorem binds
   the winding tail to the TB geometry.
5. Inspect both N=30 and N=32 q=8 receipts and the Kaggle reproduction. Confirm
   or reject the narrower corrected statement “same-byte sampled
   finite-section polygon winding evidence.” Do not call it a zero certificate.
6. Compare the q=9..12 driver(s) line-by-line at the relevant evaluator,
   segment, and tail calls. Classify each q as the same refutation,
   `SUSPENDED / AT RISK`, or unaffected. Do not infer merely from filenames.
7. Audit the appended correction blocks in `F8_CERT_PLAN.md`,
   `F9_F12_BASE_EXTENSION.md`, and `MAP.md` only after steps 1–6. Check that the
   blast radius neither understates nor overstates what was negated.

## Verdict vocabulary

Use exactly one principal verdict:

- `REFUTATION CONFIRMED` if the former continuous-Fredholm-certificate claim is
  false and the appended corrected scope is sound;
- `GAPS / NOT REFUTED` if the correction is directionally plausible but a
  stated defect or blast-radius edge is unproved; or
- `CORRECTION REFUTED` if the old certificate does contain the required
  continuous and uniform analytic enclosures, quoting their exact theorem and
  binding.

A confirmed refutation does **not** prove the q=8 determinant has no zero. It
proves only that these artifacts do not establish one. Preserve q=5, q=7,
RATE-A, and the qualitative Selberg–Hejhal tail unless an exact dependency from
this faulty engine is demonstrated.

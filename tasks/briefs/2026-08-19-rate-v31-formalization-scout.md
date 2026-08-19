GOAL: Select the next load-bearing Aristotle formalization target that advances an unconditional full proof of the (RATE) law.
IN-SCOPE: `/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v26/` through `/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v30/`, their exact result/referee artifacts, and open prerequisites recorded in `/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/`.
OUT-OF-SCOPE: No file writes; no git state changes; no Aristotle submission; no Kaggle launch; no claim that finite Lean algebra proves an analytic or paper-source theorem.

PHASE 0 — before any work, state the read-only search plan and every disagreement
with this brief, citing live files as evidence, or state what was checked before
concluding it is sound.  Silent scope additions are a lane defect.

GATE (re-run, do not self-certify): a separate context judges the report from exact paths, commands, theorem
signatures, and source mappings.  Every unproved statement is `CONJECTURAL`.
Respect `V30_REFEREE.md`: finite serialization/algebra is confirmed; full paper
source-table coverage, canonical/Ford inputs, analytic `(FW)`/`(AM)`, and RATE-A
machine certification remain gaps.  The branch is
`codex/prime-step-review-economic-validation`.  Never print or echo the Aristotle
key.

CONSTRAINTS:
- Use v29/v30 `DISPATCH.md` patterns and the v26 cache only as inspected evidence.
- Prefer a theorem whose Lean proof removes a real dependency edge; reject targets
  that merely repackage already-proved arithmetic.
- For each candidate, give the paper/source lemma, exact Lean type, dependency
  imports, and what remains analytic after it succeeds.
- Syntax feasibility may be checked read-only against existing sources; do not
  create a project, dispatch, or result file.
- No state-changing git command.  Do not modify any file, including task ledgers.

DONE MEANS:
1. Rank at least three candidates by load-bearing value, formalizability, and duplication risk.
2. Select one v31 target or return `NO LOAD-BEARING TARGET` with the exact missing mathematical statement.
3. Give exact proposed theorem signatures and a source-to-type coverage table for the selected target.
4. State an Aristotle dispatch/rebuild gate, including zero-`sorry`, zero declared-`axiom`, exact signature, and independent v26-cache rebuild checks.
5. Quote exact commands/output proving that the target is not already present in v26-v30.

VERIFY: `git status --short --branch`; targeted theorem-signature searches and
direct reads of `DISPATCH.md`, result source, and referee artifacts.  End with the
required lane-report shape below.

LANE REPORT (hard shape — the orchestrator reads only this): summary <=200 words; changed_paths (must be `none`); evidence (exact
commands plus output lines for each criterion); attempts; assumptions;
leftovers/concerns.  Then exactly one status line, `STATUS: COMPLETE`,
`STATUS: COMPLETE_WITH_CONCERNS (...)`, or `STATUS: BLOCKED (...)`, followed by
`READY FOR JUDGING`.

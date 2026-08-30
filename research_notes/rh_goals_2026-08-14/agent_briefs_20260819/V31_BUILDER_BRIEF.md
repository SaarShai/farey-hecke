GOAL: Build a syntax-checked Aristotle v31 dispatch for the paper one/two-mark source encoder and inverse decoder
IN-SCOPE: projects/aristotle_dispatch_v31/ in the isolated worktree only
OUT-OF-SCOPE: No edits outside projects/aristotle_dispatch_v31; no git operations, Aristotle submission, Kaggle launch, status promotion, or analytic/Ford/RATE claims
DONE MEANS: DISPATCH.md and RateCoreVI.lean encode the actual bounded paper record, pass the v26-cache syntax gate, and carry explicit CONJECTURAL scope and escape hatches
VERIFY: v26-cache Lean syntax precheck, exact target and forbidden-declaration searches, strict brief lint, and git diff --check

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
- You are not alone in the repository. Do not revert, rewrite, stage, commit, or
  otherwise disturb work by other agents. Work only in the isolated worktree and
  only in the stated directory.
- Receipts before claims. Every numeric/status statement in the dispatch must
  quote the command and output that supports it.
- Every unproved mathematical statement is labelled CONJECTURAL. False targets
  get an explicit negation/corrected statement, never a forced proof.
- No API key may be printed, echoed, copied into a file, or included in output.

LANE REPORT (hard shape — the orchestrator reads only this): summary <=200 words;
changed_paths (every file, exhaustive); evidence (exact commands + output lines
for each done-means criterion); attempts; assumptions; leftovers/concerns. End
with exactly one status line: STATUS: COMPLETE | COMPLETE_WITH_CONCERNS (list) |
BLOCKED (exact blocker + what you tried) — then the line READY FOR JUDGING. Raw
results only — no verdicts about your own work, no 'done'.

## Source authority and dependency edge

Read completely before designing types:

- `projects/aristotle_dispatch_v29/DISPATCH.md` (dispatch/escape-hatch pattern),
- `projects/aristotle_dispatch_v30/DISPATCH.md`,
- `projects/aristotle_dispatch_v30/V30_REFEREE.md` (especially the exact v30
  source-table gap),
- `research_notes/rh_goals_2026-08-14/lane_g/TWOMARK_RENEWAL_SOL.md`, sections
  containing the endpoint normalization, atomization, one/two-mark table, and
  decoder (`§4.1`, lines approximately 333–590),
- `research_notes/rh_goals_2026-08-14/lane_g/TWOMARK_REFEREE.md`, and
- `research_notes/rh_goals_2026-08-14/lane_g/AM_REFEREE.md`.

The exact v30 gap is that `MarkedCode` is only a local serialization with three
boundary statuses. It is not the paper source-object type, does not express the
paper's four cut actions, and does not prove coverage of the full one/two-mark
source table. Do not rename or wrap `MarkedCode` and call the gap closed.

## Principal deliverable

Create `projects/aristotle_dispatch_v31/DISPATCH.md` and its standalone Lean
source `projects/aristotle_dispatch_v31/RateCoreVI.lean`. The dispatch must be
ready for a later Aristotle submission, but you must not submit it.

The source must contain executable, non-opaque definitions (not theorem
hypotheses) for:

1. normalized source atoms representing `H+`, `H-`, `U^t`, and `L^t`;
2. the balanced-range/maximal-run validity data needed by the paper source
   decomposition;
3. a one-mark or ordered-distinct-two-mark choice;
4. four distinct cut actions, three empty-core flags, and the four coupled-case
   alternatives;
5. a `PaperCode` whose payload matches the paper's bounded record: at most three
   cores, four auxiliary integers, two heavy magnitudes, plus the finite tag;
6. executable `sourceEncode`, `sourceDecode`, and `codeGain`.

Do not make injectivity tautological by storing the complete source object or an
unbounded atom list inside `PaperCode`. If the printed source table is
insufficient to implement a branch, stop and report that exact branch as a GAP.

The CONJECTURAL Aristotle targets are:

```lean
theorem source_encode_valid {q : ℕ} (s : MarkedSource q) :
  PaperCode.Valid q (sourceEncode s)

theorem source_decode_encode {q : ℕ} (s : MarkedSource q) :
  sourceDecode (sourceEncode s) = some s

theorem source_encode_injective {q : ℕ} :
  Function.Injective (@sourceEncode q)

theorem source_codeGain_pos {q : ℕ} (s : MarkedSource q) :
  1 ≤ codeGain (sourceEncode s)

theorem paperTag_card :
  Fintype.card PaperTag = 82944

theorem paperTag_card_lt :
  Fintype.card PaperTag < 2^20
```

If the correct executable type design forces a signature change, document the
reason and preserve the same dependency content. The numeric tag size is an
overcount ceiling; only `sourceEncode` should select admissible tags.

## Done means

- `DISPATCH.md` contains a source-to-type table covering every paper datum, the
  exact target signatures, a FALSE-AS-STATED escape hatch, explicit exclusions
  of matrix inequality `(4.1)`, Ford counting, `(AM)`, RATE-A, and the LAW, plus
  an adversarial test list for every one-mark/two-mark/coupled branch and reverse
  adjacent `L,U`.
- `RateCoreVI.lean` is standalone under `import Mathlib`; all definitions and
  target declarations parse against the v26 cache. Proof bodies may use the
  dispatch placeholder style expected by the existing Aristotle workflow, but
  may not smuggle the target as an axiom or assumption.
- A literal search shows no accidental reuse of v30 `MarkedCode` as the paper
  type and no declared `axiom`.
- The lane report quotes the exact syntax-precheck command, exit code/output,
  target-signature search, forbidden-declaration search, and `git diff --check`.

## Verification commands

Use the Lean executable through the v26 cache at
`projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle/` and
`/Users/za/.elan/bin/lake`. Follow the proven v29/v30 invocation pattern rather
than inventing a new cache layout. Also run:

```bash
rg -n '^\s*axiom\b|MarkedCode' projects/aristotle_dispatch_v31
rg -n 'source_encode_valid|source_decode_encode|source_encode_injective|source_codeGain_pos|paperTag_card' projects/aristotle_dispatch_v31/RateCoreVI.lean
git diff --check -- projects/aristotle_dispatch_v31
```

Do not claim a proof: until Aristotle returns, independent rebuild succeeds,
and a separate cold referee audits coverage, the v31 result is CONJECTURAL.

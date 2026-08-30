# Cold referee brief — v31 bounded-source refutation

You are the independent adversarial referee for the v31 Lean packet. Work only
in this isolated worktree. Other agents are active elsewhere; do not revert or
modify their files.

Read, but do not edit:

- `projects/aristotle_dispatch_v31/RateCoreVI.lean`
- `projects/aristotle_dispatch_v31/DISPATCH.md`
- `research_notes/rh_goals_2026-08-14/lane_g/TWOMARK_RENEWAL_SOL.md`
- `research_notes/rh_goals_2026-08-14/lane_g/TWOMARK_REFEREE.md`

Your sole owned deliverable is:

- `projects/aristotle_dispatch_v31/V31_REFEREE.md`

The packet claims only a local refutation/corrected formalization status. Judge
it cold. In particular:

1. Rebuild `RateCoreVI.lean` using the absolute v26 cache command printed in
   `DISPATCH.md`; quote the command, output, and exit code.
2. Verify zero `sorry` and zero declared `axiom`; audit theorem dependencies if
   Lean exposes anything beyond standard Mathlib foundations.
3. Check each named counterexample semantically, not merely by compilation:
   `balanced_word_valid_rejects_nonmaximal`, `collision_sources_valid`,
   `source_encode_collision`, `source_decode_mark_counterexample`,
   `source_encode_injective_false`, and `source_encode_valid_false`.
4. Try to defeat the collision: verify that the two sources are distinct and
   locally valid, that their codes are definitionally equal, and that no hidden
   invalidity or differing payload invalidates the witness.
5. Check the cardinal arithmetic and tag range:
   `4^2 * 3^4 * 2^3 * 4 * 2 = 82944`, the base-3 cut encoding, and whether the
   implementation or prose overstates injectivity/coverage. Inspect the decoder
   bit/digit layout adversarially and record any additional mismatch.
6. Verify that the false positive theorem declarations
   `source_encode_valid`, `source_decode_encode`, and
   `source_encode_injective` are absent, while all surviving positive claims are
   exactly as weak as their proofs.
7. Enforce the ledger scope: the exact paper encoder/decoder and source-table
   coverage must remain OPEN / CONJECTURAL. This packet cannot upgrade (FW),
   (AM), RATE-A, q7, any finite LAW case, or the LAW.

Return one of `REFUTATION CONFIRMED`, `GAPS / NOT REFUTED`, or
`REFUTATION REFUTED`. Every numerical/status claim must include a quoted fresh
command receipt. If you find a false or overstated claim, state its negation and
the weakest corrected statement. Finish the report with `READY FOR JUDGING`.
Run `git diff --check` and quote the final scoped `git status --short --branch`.
Do not commit, submit to Aristotle, launch Kaggle, or touch credentials.

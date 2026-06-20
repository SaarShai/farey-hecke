# Demo D-D — Aristotle submission log (budget governance)

Fresh lemma: `let x : Real := 2 * Real.cos (Real.pi / 9); then x^3 - 3*x - 1 = 0`.

## Intended budget: ONE submission.

- **Canonical submission:** project_id `52301831-be26-4d70-93b0-549fbcf6d31e`
  (name `aristotle_lambda9`), made by `run_demo.py --submit` via
  `engine.formal_verify.verify(..., submit=True)`. This is the ONE intended job.

- **Incident:** the first `run_demo.py --submit` driver crashed AFTER a
  successful submit when an `aristotle show` CLI call hung past its 60 s timeout
  (the CLI blocks while a project is RUNNING, streaming live events). The
  submission itself was fine; only the *driver's* polling raised. A second
  `aristotle_lambda9` project (`b203940e-0592-41ca-9f8c-6bf2092e6de2`) appeared
  during the recovery window.

- **Governance action:** to respect the one-submission budget, the duplicate
  `b203940e` was **cancelled** (`aristotle cancel`, confirmed IDLE). Only the
  canonical `52301831` was allowed to run to completion. No re-submission was
  made; the final RunRecord is assembled by post-processing `52301831` via
  `run_demo.py --project-id 52301831-...` (download + extract only, NO new
  compute).

- **Driver hardening (demo-local only, engine modules untouched):**
  `run_demo.py` now polls with `_robust_poll_and_certify`, which tolerates
  transient `aristotle show` CLI timeouts/errors with backoff so a slow status
  call can never discard an already-paid-for proof. Project status is also
  trackable via the fast `aristotle list` command (does not hang while RUNNING).

## Outcome: PROVED.

- Project `52301831` finished. Its project-level status was
  `COMPLETE_WITH_ERRORS` (errors in intermediate proof-search attempts), but the
  FINAL `RequestProject/Main.lean` is a clean sorry-free proof of
  `lambda_9_min_poly`. Aristotle found a SIMPLER route than the Chebyshev hint:
  the cosine triple-angle identity `Real.cos_three_mul` at θ=π/9 (3·(π/9)=π/3,
  cos(π/3)=1/2 ⟹ 4cos³−3cos=1/2; x=2cos rearranges via `nlinarith`).

- Because the project status was ambiguous, the proof was **independently
  re-verified LOCALLY** (NOT merely Aristotle-reported): the Main.lean was built
  against a local prebuilt Mathlib (toolchain `leanprover/lean4:v4.28.0`, sibling
  project `projects/aristotle_dispatch_v14`). Result: `lake env lean` exit 0,
  zero `sorry`/`admit`, and `#print axioms lambda_9_min_poly` =
  `[propext, Classical.choice, Quot.sound]`. RunRecord therefore records
  `proved=True`. Temp build files were removed from the sibling project
  (left clean).

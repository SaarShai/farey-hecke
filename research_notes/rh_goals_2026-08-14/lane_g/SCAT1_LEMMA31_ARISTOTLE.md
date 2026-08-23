# SCAT-1 Lemma 3.1 — Aristotle dispatch (UNREFEREED)

**Status:** UNREFEREED. Submitted to Aristotle 2026-08-23; proof search in
progress at handoff. Nothing here is verified until Aristotle returns a
sorry-free file and it is checked locally.

## Project

- **Name:** `scat1-lemma31-reflection`
- **Aristotle project id:** `ca1833f9-c955-4f7b-b6a6-18e2e718ed15`
- **Local slot:** `projects/aristotle_dispatch_v33/Scat1Lemma31Reflection.lean`
- **Source lemma:** `SCAT1_PHIQ_ZERO_CERTIFIER_SOL.md` §Lemma 3.1, step (ii)
  only (the abstract reflection core). Reflection is `s ↦ 1 − s`, NOT
  `1 − conj(s)` — no conjugation anywhere.

## Submitted Lean statement (verbatim)

```lean
theorem scat1_lemma31_reflection
    (U : Set ℂ) (hU : IsOpen U) (hUrefl : ∀ s ∈ U, (1 - s) ∈ U)
    (φ : ℂ → ℂ) (hφ : MeromorphicOn φ U)
    (hfe : ∀ s ∈ U, ∀ᶠ z in 𝓝[≠] s, φ z * φ (1 - z) = 1)
    (sstar : ℂ) (hs : sstar ∈ U)
    (m : ℕ) (hm : 1 ≤ m)
    (hpole : meromorphicOrderAt φ sstar = (-(m : ℤ) : WithTop ℤ)) :
    meromorphicOrderAt φ (1 - sstar) = ((m : ℤ) : WithTop ℤ) := by
  sorry
```

Formalization choices: "meromorphic identity away from poles" is carried as
the identity holding frequently in `𝓝[≠] s` for every `s ∈ U`; pole/zero of
order `m` use `meromorphicOrderAt` (`WithTop ℤ`), values `-m` / `m`.
Aristotle was permitted to adapt the mathlib order-API spelling but NOT the
mathematical content.

## Resume / poll

```bash
source ~/.farey_api_keys
~/.local/bin/aristotle show ca1833f9-c955-4f7b-b6a6-18e2e718ed15
# when done:
~/.local/bin/aristotle download ca1833f9-c955-4f7b-b6a6-18e2e718ed15 \
  # (see `aristotle download --help` for destination flag)
```

Note: submission warned "no .lake folder" (statement-only dispatch, no local
lake build shipped) — consistent with prior dispatches.

## Status log

- 2026-08-23: submitted; project created; task
  `87925d91-8e83-452a-a4b5-785493464ca2` QUEUED → RUNNING (1% at ~30s).
  Note: `aristotle show` streams live progress and does not exit while the
  task runs — Ctrl-C after reading the status line.

## COMPLETE (2026-08-23, append-only)

Aristotle finished: full Lean proof, no sorry/admit (grep 0), axioms only
propext / Classical.choice / Quot.sound per Aristotle's report. Proof route:
affine change of variable z -> 1-z preserves meromorphic order (derivative
-1 != 0); functional equation makes phi * g eventually 1 near s*, so order 0;
order additivity gives -m + ord(phi at 1-s*) = 0. Result downloaded to
projects/aristotle_dispatch_v33/aristotle_dispatch_v33_aristotle/ (75-line
Scat1Lemma31Reflection.lean inside). Local lake build NOT run (toolchain
fetch heavy); Aristotle-side elaboration report is the current evidence —
MACHINE-VERIFIED (Aristotle-side), local re-elaboration optional.

## LOCAL RE-ELABORATION PASS (2026-08-23, append-only)

`lake build` in projects/aristotle_dispatch_v33/aristotle_dispatch_v33_aristotle
completed successfully (8034 jobs; log projects/aristotle_dispatch_v33/
LEAN_REELAB.log; only unused-variable linter warnings). Lemma 3.1 reflection
core is now machine-verified BOTH Aristotle-side and locally.

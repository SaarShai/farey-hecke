# Local rebuild receipt — `scat1_lemma31_reflection` — 2026-08-27

First local re-verification of Aristotle run
`87925d91-8e83-452a-a4b5-785493464ca2`. Until now the "no `sorry`, no `axiom`"
statement for this lemma was the run's own report; it is now checked here.

Directory:
`projects/aristotle_dispatch_v33/aristotle_dispatch_v33_aristotle/aristotle_dispatch_v33_aristotle/`
Toolchain: `leanprover/lean4:v4.28.0`, Mathlib pinned at `v4.28.0` by
`lake-manifest.json`.

## Build

```text
⚠ [8026/8027] Built Scat1Lemma31Reflection (26s)
warning: Scat1Lemma31Reflection.lean:39:17: unused variable `hU`
warning: Scat1Lemma31Reflection.lean:43:13: unused variable `hm`
Build completed successfully (8027 jobs).
```

Both warnings are the two the run reported, on hypotheses the dispatch
required be kept in the statement. Full log: `SCAT1_REBUILD_2026-08-27.log`.

## Axiom check

```text
$ lake env lean AxCheck.lean          # import + #print axioms
'scat1_lemma31_reflection' depends on axioms: [propext, Classical.choice, Quot.sound]
```

Only the three standard Lean axioms. **`sorryAx` is absent**, which is the
check that matters: a `sorry` anywhere in the proof would appear here.
`grep -c "sorry\|admit"` over the source returns 0.

## What was proved

```lean
theorem scat1_lemma31_reflection
    (U : Set ℂ) (hU : IsOpen U) (hUrefl : ∀ s ∈ U, (1 - s) ∈ U)
    (φ : ℂ → ℂ) (hφ : MeromorphicOn φ U)
    (hfe : ∀ s ∈ U, ∀ᶠ z in 𝓝[≠] s, φ z * φ (1 - z) = 1)
    (sstar : ℂ) (hs : sstar ∈ U)
    (m : ℕ) (hm : 1 ≤ m)
    (hpole : meromorphicOrderAt φ sstar = (-(m : ℤ) : WithTop ℤ)) :
    meromorphicOrderAt φ (1 - sstar) = ((m : ℤ) : WithTop ℤ)
```

A pole of order `m` at `s*` forces a zero of order `m` at `1 - s*`, for any
meromorphic `φ` satisfying the functional equation `φ(s)φ(1-s) = 1` on a
reflection-closed open set. Scope: this is the elementary reflection step
only. It formalizes no analytic or spectral content, and proves nothing about
`φ_q` for any particular group — that membership is a separate, unformalized
claim.

## Disk

The rebuild recreated a 6.9 GB `.lake` under that directory (git-ignored). It
is cheap to recreate: the Mathlib olean cache lives in `~/.cache/mathlib`
(403 MB), so `lake exe cache get` needed no downloads and decompression took
~6 s. Delete the 6.9 GB freely; re-running the two commands above reproduces
this receipt.

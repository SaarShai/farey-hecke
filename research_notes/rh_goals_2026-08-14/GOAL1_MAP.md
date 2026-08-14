# GOAL 1 — Sample complexity of zero detection from prime data

Preliminary map, 2026-08-14. Status updates same day: S2 scout — CR headline
UNOCCUPIED (no collision 2018–2026); Prony/Frobenius classical (frame as
infrastructure). Anchor lemma MACHINE-VERIFIED: prony_power_sum_uniqueness
(Aristotle project 964f8c92, sorry-free, axiom-clean) at
projects/aristotle_dispatch_v16/result/project_aristotle/PronyPowerSums.lean.

## Aim

State and prove the first quantitative answer to: **how many prime
measurements determine the first d nontrivial zeros of an L-function to
precision ε?** Treat the explicit formula as a line-spectrum model
(ψ(x) − x = −Σ_ρ x^ρ/ρ + …) and derive matching information-theoretic lower
bounds and algorithmic upper bounds.

## Why this is RH-relevant (article-style)

The article's result was a measurable partial: a bound moved. Here the
measurable object is N(d, ε, X) — the sample complexity of the inverse
explicit-formula problem. It quantifies the information content of primes
about zeros, the exact channel every RH-adjacent argument uses. A tight
unconditional detection statement ("any prime subset with Σ 1/p = ∞ sees
every zero"; "an off-line zero produces a divergent signal") is a new lens on
how RH failure would be *visible* — and is a theorem family others can
sharpen.

## What we already hold (verified)

- Working recovery pipeline: MUSIC/Prony AND fair windowed periodogram both
  recover 5/5 Dirichlet zeros <0.3% and 10/10 ζ zeros to 0.04–0.5%
  (projects/mimo-mini-project, SPECTROSCOPY_GATE_RESULTS.md Gate 1 PASS,
  non-circular, null-tested).
- The kill-gate record proving the TOOL framing is dead — which is exactly
  what forces the theory framing here (Gate 2/3: FFT ties, no super-res).
- Gate-0 novelty scan (101 agents): O(d)/Cramér–Rao for zeros-from-counts
  unaddressed in the literature; nearest prior art is spectral DISPLAY only
  (Lan–Yong 2006, Csoka 2015/17).
- Spectroscope theorem skeletons: detection (unconditional), universality
  (Σ 1/p = ∞, currently conditional), stability (Montgomery–Vaughan).
  Partial Lean: MertensSpectroscopeUniversality.lean (2 unconditional
  lemmas), FareyBridgeIdentity.lean (unconditional), LocalPerronResidue.lean
  (zero-sorry).
- Function-field control: finite exact case (zeros = Frobenius eigenvalues,
  N = 2d Prony bound is meaningful and testable exactly; δ_ff enumeration
  infrastructure).
- IMPORTED 2026-08-14 (research_notes/imported_farey_now/):
  - DPAC_context.md + ARISTOTLE_SUMMARY.md — cleanest DPAC evidence packet
    (R_K avoidance ratios 4–16×, 300/300 interval-certified nonvanishing,
    density-zero backbone proved, dpac_of_LI open).
  - SPECTROSCOPE_DETECTION_THRESHOLD.md — draft detection statistic
    F_K(γ) with S/N > 3 thresholds (K ≥ 10, P ≥ 1000); starting point for
    the S2 estimator analysis.
  - LFUNC_BATCH_CROSSOVER_VERIFIED.md — the audited batch-crossover
    benchmark (2.25×–20×); use these numbers, not the unaudited
    spectroscope README figures.

## Headline NEW facts targeted (niche-doctrine compliant)

1. **Theorem (lower bound):** Fisher-information/Cramér–Rao bound for
   estimating γ_1..γ_d from {ψ(x): x ≤ X} (or from p ≤ X prime counts) under
   the explicit-formula signal model with arithmetic-fluctuation noise.
   First-of-kind statement; even a clean conditional (RH-assumed noise model)
   version is new.
2. **Theorem (upper bound):** windowed-periodogram estimator achieving
   γ-recovery to ε with explicitly bounded X(d, ε) — formalizing what the
   Gate-1/Gate-2 numerics already do.
3. **Theorem (unconditional detection, honest version):** at least one
   nontrivial zero is detectable unconditionally; if RH fails, the most
   off-line zero dominates the spectroscope signal with divergent
   amplification. Proof audit + Lean of the finite-side lemmas.
4. **Universality upgrade attempt:** replace the Soundararajan-style
   hypothesis in the Σ 1/p = ∞ universality theorem with something weaker, or
   prove sharpness (a thin prime set that misses a zero) — either outcome is
   a publishable new fact.

## Stage ladder with falsification gates

- **S0 (1–2 d).** Freeze the model: signal, noise, estimator class,
  parameter regime. Preregister the theorem statements. Resolve README
  inflation: mark spectroscope README claims unaudited; carry only
  kill-gate-surviving numbers forward.
- **S1 (1 wk).** Function-field exact case first (finite spectrum, Weil RH
  true): prove the exact N = 2d Prony statement + CR bound there. GATE: if
  even FF sample complexity has hidden prior art (signal-processing lit,
  algebraic decoding/Prony-for-Frobenius), stop and re-scope to a survey
  note.
- **S2 (2 wk).** Number-field lower bound with RH-model noise; upper bound
  for the windowed periodogram on ζ (d ≤ 20, using existing Odlyzko-verified
  pipeline as the numerical audit). GATE: constants must beat trivial
  counting bounds, else the theorem is vacuous — kill or weaken.
- **S3 (2 wk).** Unconditional detection theorem, written + adversarially
  refereed + Lean the finite lemmas (extend MertensSpectroscopeUniversality
  unconditional pair). Aristotle dispatch for the residue algebra.
- **S4 (open).** Universality sharpening; DPAC connection (DPAC-style
  avoidance at zeros is the obstruction to some estimator guarantees —
  reuse DPAC_full.lean scaffolds).

## Kill criteria / risks

- Prior-art collision on CR-for-zeros (S1 gate). The 101-agent scan was
  2026-06; re-run a focused scout before S2.
- The noise model is the science: arithmetic fluctuation is not iid Gaussian.
  If no defensible noise model exists, the LOWER bound degrades to a
  heuristic — then re-scope headline to detection + universality only.
- Do NOT claim computational superiority (killed). The claim is
  information-theoretic structure, not speed.

## First 3 actions

1. Write the frozen model spec (S0) into this directory.
2. Focused prior-art re-scout: "Cramér–Rao zeros explicit formula",
   "Prony Frobenius eigenvalue recovery", "line spectral estimation prime
   counting" (research-lite lane).
3. FF exact-case theorem draft + numeric audit harness reusing
   projects/mimo-mini-project/code/gate3_finite_d.py.

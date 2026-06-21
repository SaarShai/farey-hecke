# pgen_orbit_realization — PROVED axiom-clean (2026-06-20)

/ goal P-realization: prove the wiring lemma that `Pgen` along the corridor `Mmap`-orbit equals a
positive-scale multiple of a sinusoid on the conserved ellipse `E`. **DONE — axiom-clean, no sorry.**

## Result

`pgen_orbit_realization` (file `projects/hsa_realization_lean/RequestProject/Main.lean`):
for `q = m+2 ≥ 3`, `l = lamq q`, `p ∈ Dcorr l`, and the corridor E-floor `EfloorQ m l ≤ Eform l p`,

  ∃ C0 R φ, 0 < R ∧
    (∀ k, Pgen l ((Mmap l)^[k] p) = C0 + R·cos(φ + 2k·(π/q))) ∧
    (1/l³ − C0)/R ≤ cos(π/q).

`lake env lean` EXIT 0, no warnings, `#print axioms pgen_orbit_realization →
[propext, Classical.choice, Quot.sound]` (NO sorryAx). Verified against prebuilt Mathlib v4.28.0 at
`projects/aristotle_dispatch_v15/.lake`. Reusable helpers `recur_closed_form`, `recur_to_Rcos`
(sinusoid-from-2-step-recurrence) also axiom-clean.

## Constants (sealed-Pgen normalization, NOT the L1b Fobs constants)

Sealed `Pgen l (a,b)=a(a+lb)/l`, `Mmap l (a,b)=(b,−a+lb)`, `Eform l (a,b)=a²−lab+b²`. With c=cos(π/q),
s=sin(π/q), l=2c:

  C0 = alphaC l · E,  R = rhoC l · E,  E = Eform l p,
  alphaC l = (l²+2)/(l(4−l²)) = 1/(4c)+3c/(4s²)
  rhoC  l = 2√(2l²+1)/(l(4−l²)) = √(8c²+1)/(4s²c)
  EfloorQ m l = 1/(l³(alphaC l + rhoC l·cos(π/q)))

Asymptotics: alphaC·(4−l²)→3, rhoC·(4−l²)→3 as q→∞ (confirmed q=1000: 2.99999.., 3.00000..).
Reference (q,alpha,rho,Efloor,1/l³): (5, 2.0652476, 2.2335744, 0.0609641, 0.2360680),
(7, 3.8668992, 4.0349591, 0.0227818, 0.1709152), (22, 36.906265, 37.073116, 0.0017513, 0.128896).

These DIFFER from L1b Fobs constants (mean 3l/(4A2), amp 1/(2√A2), A2=1+2l²): symbolic
`alphaC ≠ mean_L1b`, `rhoC ≠ amp_L1b`. The wiring lemma uses the raw alpha,rho matching literal
sealed `Pgen`. Kaggle kernel pins BOTH sets.

## Honesty: the FALSE current statement was corrected

The pre-existing `mu_close_hSuperArc/Main.lean:326-337` asserts the gate `(1/l³−C0)/R ≤ cos θ` for
ALL `p ∈ Dcorr l` — this is FALSE (q=5 has corridor points with `E < Efloor ⟹ gate fails`). The
faithful statement carries `hE : EfloorQ m l ≤ Eform l p` (scout Form A). The orbit identity (1a) is
unconditional; the E-floor enters ONLY the gate. Off-floor (k≥2 deep-mid) points are covered
separately by `genuine_hEject_deepmid` on the Tgen orbit (not this lemma's job). Added `hm : 1 ≤ m`
(q≥3), faithful to Hecke groups.

## Proof method — NO external hard step

The whole proof is `field_simp; ring` + `nlinarith` + Mathlib trig. No matrix machinery, no
Aristotle needed:
1. Two-step recurrence `hseq(k+2) = 2cos(2θ)·hseq(k+1) − hseq k`, `hseq k := Pgen(Mᵏp) − C0`,
   per-step by `field_simp; ring` (uses `Mmap_preserves_E` so E is constant on the orbit, and
   cos(2θ)=l²/2−1 from l=2cosθ).
2. `recur_to_Rcos` ⟹ closed form `R·cos(φ+k·2θ)`; phase φ via `Complex.arg`.
3. Amplitude invariant `h0²−2cos2θ h0h1+h1² = (rhoC·E)²sin²2θ` (`field_simp; ring`) forces
   `R = rhoC l · E > 0` (rhoC>0, E>0 on corridor).
4. Gate `⟺ E ≥ EfloorQ`, discharged by `hE`.

## Numeric confirmation (Kaggle `saarshai/hsa-constants`, COMPLETE)

60-dps orbit-identity stress test over 200 random corridor points × k=0..2q, all q∈{3..100}:
max |Pgen(Mᵏp) − (C0+R cos(φ+2kθ))| ~ 1e-60..1e-55 (machine-exact). Gate at E=Efloor equals cos(π/q)
to ~1e-61 (the floor is exactly where the gate becomes tight). Output:
`code/hsa_realization/kaggle_out/hsa_constants.json`. Local 50-dps check:
`code/hsa_realization/verify_orbit.py`; symbolic derivation `derive_constants.py`, `recurrence.py`.

## Files

- Lean (PROVED): `projects/hsa_realization_lean/RequestProject/Main.lean` (+ PROMPT.md, standalone
  lakefile mirroring hmeas_lean).
- Numeric: `code/hsa_realization/{derive_constants,verify_orbit,recurrence}.py`, `kaggle_out/`.
- Kernel: `kaggle_kernels/hsa_constants/`, pushed id `saarshai/hsa-constants` (status COMPLETE).

## Downstream wiring

This discharges the single named residual `pgen_orbit_realization` at
`mu_close_hSuperArc/Main.lean:337`. Consumers `orbit_hit_of_realization`, `cos_grid_hit`,
`SuperArcCover_corridor` are already PROVED there. The k≥2 deep-mid branch (E<Efloor) is the
`genuine_hEject_deepmid` one-step branch (separate). NOTE: to splice into that file one must thread
`hm : 1 ≤ m` and the `hE` E-floor split through the corridor inclusion — the E-floor lower bound on
`Dcorr` (E bounded below away from cusp) is the remaining small companion lemma for the k=1 region,
or absorbed by the genFloor k=1/k≥2 split.

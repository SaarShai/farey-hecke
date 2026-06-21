# pgen_orbit_realization — realization wiring lemma for hSuperArc

This RequestProject contains a COMPLETE, axiom-clean proof (no `sorry`, no `sorryAx`) of
`pgen_orbit_realization`, the wiring lemma that identifies the genuine observable `Pgen` along the
`Mmap`-corridor orbit as an affine sinusoid `C0 + R·cos(φ + 2kθ)` on the conserved energy ellipse,
together with the threshold gate `(1/l³ − C0)/R ≤ cos θ` under the corridor E-floor.

## Faithfulness

- Sealed defs reproduced VERBATIM: `lamq`, `Mmap`, `Pgen`, `Eform`, `Dcorr`.
- The statement is **Form A** (scout-recommended): the orbit identity is UNCONDITIONAL; the gate is
  gated by the explicit E-floor hypothesis `hE : EfloorQ m l ≤ Eform l p`.  The current
  `mu_close_hSuperArc/Main.lean:326-337` form (gate for ALL `p ∈ Dcorr`) is FALSE for small `q`
  (numerically `q=5` has corridor points with `E < Efloor`); this file carries the `hE` hypothesis.
- Added hypothesis `hm : 1 ≤ m` (i.e. `q = m+2 ≥ 3`), faithful to Hecke groups (which require
  `q ≥ 3`; for `q=2`, `l = 2cos(π/2) = 0` is degenerate).

## Constants (Kaggle `saarshai/hsa-constants`, 60 dps + sympy symbolic)

- `alphaC l = (l²+2)/(l(4−l²)) = 1/(4c)+3c/(4s²)`,  c=cos(π/q), s=sin(π/q)
- `rhoC  l = 2√(2l²+1)/(l(4−l²)) = √(8c²+1)/(4s²c)`
- `EfloorQ m l = 1/(l³(alphaC l + rhoC l · cos(π/q)))`
- `C0 = alphaC l · E`, `R = rhoC l · E`, `E = Eform l p`.

## Proof structure (all `ring`/`field_simp`/`nlinarith`, no external hard step)

1. `recur_closed_form` / `recur_to_Rcos` (general, reusable): a real sequence satisfying the
   two-step recurrence `h(k+2) = 2cos ω·h(k+1) − h k` (sin ω ≠ 0) equals `R cos(φ + kω)`.
2. The orbit offset `hseq k = Pgen(Mᵏp) − C0` satisfies that recurrence with `ω = 2θ`
   (per-step identity by `field_simp; ring`, using `Mmap_preserves_E` so `Eform(Mᵏp)=Eform p`).
3. Amplitude invariant `h0² − 2cos2θ·h0h1 + h1² = (rhoC l · E)²sin²2θ` (`field_simp; ring`) forces
   `R = rhoC l · E > 0`.
4. Gate `(1/l³ − αE)/(ρE) ≤ cos θ ⟺ E ≥ EfloorQ`, supplied by `hE`.

`#print axioms pgen_orbit_realization` → `[propext, Classical.choice, Quot.sound]` (no sorryAx).

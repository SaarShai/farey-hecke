# Aristotle dispatch — q=12 scalar window-4 Positivstellensatz case (the one gap in q=7..16)

**USER submits this; do not self-submit.** Self-contained. The q=7..11,13,14,15,16 window lemmas are
machine-checked locally (axiom-clean); q=12 is the only value whose single `(1,1,1)` Positivstellensatz
case our local nullspace-LP could not certify at product-degree ≤ 3. The system IS infeasible
(numerically confirmed). Aristotle's job: prove the `False` below (find the certificate / let a stronger
search or `polyrith`/`nlinarith` close it).

## Field
`lam = 2 cos(pi/12) = sqrt(2+sqrt 3) ≈ 1.93185`, minimal relation **`lam^4 = 4*lam^2 - 1`** (degree 4,
unique root in (1,2)). Threshold `1/lam^3 ≈ 0.13854`.

## The lemma to prove (paste into Lean with full Mathlib)
```lean
import Mathlib
set_option maxHeartbeats 4000000
noncomputable section

-- q=12 single Chebyshev (K=1) window-4 case: 5 coords on the rotation line, both Taha edges,
-- cap, floor-upper (K=1), all 4 products < 1/lam^3  ==>  False.
theorem case_q12 (a b c d e lam : ℝ) (hps : lam^4 = 4*lam^2 - 1)
    (h2 : (1:ℝ) < lam) (h3 : lam < 2)
    (hpa : 0 < a) (hpb : 0 < b) (hpc : 0 < c) (hpd : 0 < d) (hpe : 0 < e)
    (hca : a ≤ 1) (hcb : b ≤ 1) (hcc : c ≤ 1) (hcd : d ≤ 1) (hce : e ≤ 1)
    (hr0 : a+lam*b > 1) (hr1 : b+lam*c > 1) (hr2 : c+lam*d > 1) (hr3 : d+lam*e > 1)
    (hg0 : lam*a+b > 1) (hg1 : lam*b+c > 1) (hg2 : lam*c+d > 1) (hg3 : lam*d+e > 1)
    (hk0 : a+c = 1*lam*b) (hk1 : b+d = 1*lam*c) (hk2 : c+e = 1*lam*d)
    (hf0 : 1+a < (1+1)*(lam*b)) (hf1 : 1+b < (1+1)*(lam*c)) (hf2 : 1+c < (1+1)*(lam*d))
    (hP0 : a*b < 1/lam^3) (hP1 : b*c < 1/lam^3) (hP2 : c*d < 1/lam^3) (hP3 : d*e < 1/lam^3) :
    False := by
  sorry
```

## Notes / what works locally for the OTHER q
- For q=7..11,13,15 we substitute the K=1 recurrence (`c=lam*b-a`, `d=lam*c-b`, `e=lam*d-c`) to reduce
  to 2 variables `(a,b)`, then a nonneg combination of pairwise products of the generators
  {a,b,coords>0; 1-coord; both edges-1; floor-upper `2 lam coord_{i+1}-1-coord_i`; slacks
  `1-coord_i coord_{i+1} lam^3`} reduces (mod `hps`) to a NEGATIVE RATIONAL, closed by `linarith`.
  Each product `g_i*g_j = (a,b-reduced)` is bridged by `linear_combination (field+recurrence cofactors)`.
- For q=12 the degree-2 and degree-3 Handelman cones did not yield a cert in our float LP (possibly a
  conditioning issue, or a genuinely degree-4 certificate). The infeasibility is real (no `(a,b)` in the
  domain has all four products `< 1/lam^3`).
- Suggested routes: (i) exact-rational Positivstellensatz LP at product-degree 4 over the power basis
  `{1,lam,lam^2,lam^3}`; (ii) `polyrith`; (iii) an SOS certificate; (iv) note `lam^2 = 2+sqrt 3` may make
  a `sqrt 3`-adic split cleaner.

## Anchor checks (must hold for any cert tooling)
q=3→2/9, q=4→√2/8, q=5→1/φ³, q=6→√3/9; `W_q` trace = lam. Threshold is ALWAYS `1/lam^3` (NOT V(q)).

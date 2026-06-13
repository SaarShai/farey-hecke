import Mathlib
/-!
# Cusp-branch envelope, ALL q (parametric in `l = λ = 2cos(π/q) ≥ φ`)

Generalises the q=5 `branch3_envelope` (`BCZHeckeG5_genuine_envelope_VERIFIED.lean`) to EVERY q.
The genuine `G_q`-BCZ cusp branch is `i = q−2`, with `x_{q-2}=1, x_{q-3}=l, x_{q-4}=l²−1`, observable
`P = a(a + l b)/l`.  This file machine-checks, **for every `l ≥ φ`** (i.e. every `q ≥ 5`):

  `cusp_envelope` :  on the cusp branch,  `P = a(a+l b)/l ≥ 1/l³`  (tight at the cusp vertex `(1/l,0)`).

Certificate (general `l`, verified symbolically in `projects/mimo-mini-project/code/Fgoal_cusp_cert_verify.py`), with
`W := l²·a(a+l b) − 1`, `G := l a + (l²−1) b − 1 > 0` [branch guard `L_{q-3}>1`],
`d := l a + b − 1 > 0` [domain]:
* case `a ≥ 1/l` :  `(l²−2)·W = (l³−l−1)·a·G + (l²−2)(l a−1)(1−a) + (l²−l−1)·a·d`,
* case `a ≤ 1/l` :  first `l²a ≥ 1` (from `a ≥ 1/(l+1)`, itself from the upper guard `a+l b ≤ 1`
  and the domain, plus `l² ≥ l+1`); then
  `(l²−2)·W = (l³−l−1)·a·d + (l²−2)(l²a−1)(1−l a) + (l²−l−1)·a·G`.
All coefficients are `≥ 0` for `l ≥ φ` (`l²−2>0`, `l³−l−1>0`, `l²−l−1≥0`), and `l²−2>0` gives `W ≥ 0`.

NOTE (honesty): this is ONLY the cusp branch `i=q−2`.  The full per-branch envelope on *all*
non-scalar branches `i=2..q−2` — the premise of the scalar reduction — is **FALSE for q ≥ 16**
(middle branches carry genuine points with `P < 1/l³`; witness q=16: `(a,b)≈(0.7857,−0.5412)`,
`P≈0.13036 < 1/l³≈0.13249`).  See `FINDINGS_goalF_*`.  So `cusp_envelope` does NOT give the
reduction for large q; it is the uniformly-true cusp piece (the optimiser lives on this branch).

`#print axioms` shows only `[propext, Classical.choice, Quot.sound]`.
-/
open Int
noncomputable section

/-- **Cusp-branch envelope, all q.** For `l ≥ φ` (`l² ≥ l+1`, `l>1`): on the genuine cusp branch
`i=q−2` (guards `l a + (l²−1) b > 1`, domain `l a + b > 1`, upper `a + l b ≤ 1`, `0<a≤1`),
the observable `P = a(a+l b)/l ≥ 1/l³`. -/
theorem cusp_envelope (l a b : ℝ)
    (hl1 : 1 < l) (hlphi : l ^ 2 ≥ l + 1)
    (ha : 0 < a) (ha1 : a ≤ 1)
    (hG : l * a + (l ^ 2 - 1) * b > 1)
    (hd : l * a + b > 1)
    (hU : a + l * b ≤ 1) :
    1 / l ^ 3 ≤ a * (a + l * b) / l := by
  have hl : 0 < l := by linarith
  have hl2 : l ^ 2 - 2 > 0 := by nlinarith [hlphi, hl1]
  have hc1 : l ^ 3 - l - 1 ≥ 0 := by nlinarith [hlphi, hl1]
  have hc2 : l ^ 2 - l - 1 ≥ 0 := by linarith [hlphi]
  -- main: W = l^2 a (a + l b) - 1 ≥ 0
  have hkey : 1 ≤ l ^ 2 * (a * (a + l * b)) := by
    rcases le_or_gt a (1 / l) with hca | hca
    · -- a ≤ 1/l
      have hfa : l * a ≤ 1 := by rw [mul_comm]; exact (le_div_iff₀ hl).mp hca
      -- a ≥ 1/(l+1):  from upper guard hU and domain hd
      have hage : a * (l + 1) ≥ 1 := by nlinarith [hU, hd, hl]
      have hlo : 1 ≤ l ^ 2 * a := by nlinarith [hage, hlphi, ha, hl]
      -- (l^2-2) W = (l^3-l-1) a d + (l^2-2)(l^2 a -1)(1-l a) + (l^2-l-1) a G
      nlinarith [hl2, hl,
        mul_nonneg hc1 (mul_nonneg ha.le (show (0:ℝ) ≤ l * a + b - 1 by linarith)),
        mul_nonneg hl2.le (mul_nonneg (show (0:ℝ) ≤ l ^ 2 * a - 1 by linarith)
                                      (show (0:ℝ) ≤ 1 - l * a by linarith)),
        mul_nonneg hc2 (mul_nonneg ha.le (show (0:ℝ) ≤ l * a + (l ^ 2 - 1) * b - 1 by linarith))]
    · -- a > 1/l
      have hfa : 1 ≤ l * a := by
        have h := (div_lt_iff₀ hl).mp hca; rw [mul_comm] at h; linarith
      -- (l^2-2) W = (l^3-l-1) a G + (l^2-2)(l a -1)(1-a) + (l^2-l-1) a d
      nlinarith [hl2, hl,
        mul_nonneg hc1 (mul_nonneg ha.le (show (0:ℝ) ≤ l * a + (l ^ 2 - 1) * b - 1 by linarith)),
        mul_nonneg hl2.le (mul_nonneg (show (0:ℝ) ≤ l * a - 1 by linarith)
                                      (show (0:ℝ) ≤ 1 - a by linarith)),
        mul_nonneg hc2 (mul_nonneg ha.le (show (0:ℝ) ≤ l * a + b - 1 by linarith))]
  -- convert W ≥ 0 to the envelope
  have e : a * (a + l * b) / l - 1 / l ^ 3
      = (l ^ 2 * (a * (a + l * b)) - 1) / l ^ 3 := by
    rw [div_sub_div _ _ (by positivity : (l:ℝ) ≠ 0) (by positivity : (l:ℝ) ^ 3 ≠ 0)]
    rw [div_eq_div_iff (by positivity) (by positivity)]; ring
  have hnn : 0 ≤ a * (a + l * b) / l - 1 / l ^ 3 := by
    rw [e]; exact div_nonneg (by linarith [hkey]) (by positivity)
  linarith

#print axioms cusp_envelope

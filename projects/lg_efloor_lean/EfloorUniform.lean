import Mathlib

open scoped Real
open Real

set_option maxHeartbeats 4000000

/-!
# `EfloorUniform` — the uniform corridor E-floor `hEfloor` (q ≥ 5), proved axiom-clean.

Target (the second residual of the keystone `Xomega_ge_unconditional`):

  `hEfloor : ∀ p ∈ Sclosed, isK1 p → EfloorQ m l ≤ Eform l p`.

Sealed defs (VERBATIM from `hsa_realization_lean` / `hsa_unconditional_lean`):
  `lamq q = 2 cos(π/q)`,  `Eform l (a,b) = a² − l a b + b²`,
  `Dcorr l = {0<a≤1, 0<b≤1, a+lb>1, la+b>1}`,
  `alphaC l = (l²+2)/(l(4−l²))`,  `rhoC l = 2√(2l²+1)/(l(4−l²))`,
  `EfloorQ m l = 1/(l³ (alphaC l + rhoC l · cos(π/(m+2))))`,
and the k=1 (`isK1`) floor bracket  `λb ≤ 1+a  ∧  1+a < 2λb`  (kfloor = 1).

## Mathematical content (scout R-efloor route, numerically certified high-dps)

On the closed `k=1` corridor the conserved `Eform` is minimized at the single vertex
  `V(l) = ((2l−1)/(2l²+1), (1+l)/(2l²+1))  =  {λa+b=1} ∩ {1+a=2λb}`,
with the EXACT value
  `Eform l (V l) = (2−l)/(2l²+1)`.
The minimum is certified by a KKT identity (PROVED by `ring`):
  `Eform(a,b) − (2−l)/(2l²+1)
     = ((2−l)/(2l²+1))·(λa+b−1) + ((2−l)/(2l²+1))·(2λb−1−a) + Eform(a−aV, b−bV)`,
where the two multipliers `(2−l)/(2l²+1) ≥ 0` (since `l<2`), the two bracketed terms are
`≥ 0` on the corridor (Dcorr edge `λa+b>1` and bracket upper edge `1+a<2λb`), and
`Eform(shift) ≥ 0` (positive-definite since `4−l²>0`).  Hence `Eform(a,b) ≥ (2−l)/(2l²+1)`.

The closed-form gate `(2−l)/(2l²+1) ≥ EfloorQ` (with `cos(π/q)=l/2`) reduces, after clearing
positive denominators and squaring (the `s=√(2l²+1)` term), to the polynomial inequality
  `g(l) := l⁷ + 2l⁶ − 3l⁵ − 4l³ − 4l² − l − 2 ≥ 0`,
whose largest real root is `≈ 1.61236 < φ = 2cos(π/5) ≈ 1.61803`.  So `g ≥ 0` for all
`l ≥ φ`, i.e. for all `q ≥ 5`.  (For `q = 3,4` the floor `hEfloor` is FALSE — see notes —
so the faithful uniform statement is `q ≥ 5`, i.e. `m ≥ 3`.)
-/

noncomputable section

def lamq (q : ℕ) : ℝ := 2 * Real.cos (Real.pi / q)
def Eform (l : ℝ) (p : ℝ × ℝ) : ℝ := p.1 ^ 2 - l * (p.1 * p.2) + p.2 ^ 2
def Dcorr (l : ℝ) : Set (ℝ × ℝ) :=
  {p | 0 < p.1 ∧ p.1 ≤ 1 ∧ 0 < p.2 ∧ p.2 ≤ 1 ∧ p.1 + l * p.2 > 1 ∧ l * p.1 + p.2 > 1}
def alphaC (l : ℝ) : ℝ := (l ^ 2 + 2) / (l * (4 - l ^ 2))
def rhoC (l : ℝ) : ℝ := 2 * Real.sqrt (2 * l ^ 2 + 1) / (l * (4 - l ^ 2))
def EfloorQ (m : ℕ) (l : ℝ) : ℝ :=
  1 / (l ^ 3 * (alphaC l + rhoC l * Real.cos (Real.pi / ((m + 2 : ℕ) : ℝ))))

/-! ## §1.  The geometric minimum:  `Eform ≥ (2−l)/(2l²+1)` on the k=1 corridor. -/

/-- **Geometric E-floor (KKT identity, PROVED).**  For any `(a,b)` with `0<l<2`, the Dcorr
edge `λa+b ≥ 1`, and the k=1 upper bracket `1+a ≤ 2λb`, the conserved `Eform` is bounded below
by the vertex value `(2−l)/(2l²+1)`.  No reference to `q`; pure quadratic geometry. -/
theorem Eform_ge_vertex (l a b : ℝ) (hl0 : 0 < l) (hl2 : l < 2)
    (hedge : 1 ≤ l * a + b) (hbr : 1 + a ≤ 2 * l * b) :
    (2 - l) / (2 * l ^ 2 + 1) ≤ Eform l (a, b) := by
  have hD : 0 < 2 * l ^ 2 + 1 := by positivity
  set aV : ℝ := (2 * l - 1) / (2 * l ^ 2 + 1) with haV
  set bV : ℝ := (1 + l) / (2 * l ^ 2 + 1) with hbV
  set lam : ℝ := (2 - l) / (2 * l ^ 2 + 1) with hlam
  -- multipliers ≥ 0
  have hlam_nn : 0 ≤ lam := by rw [hlam]; apply div_nonneg (by linarith) (le_of_lt hD)
  -- the two corridor slacks ≥ 0
  have hg1 : 0 ≤ l * a + b - 1 := by linarith
  have hg2 : 0 ≤ 2 * l * b - 1 - a := by linarith
  -- the PSD shift term  Eform(a-aV, b-bV) ≥ 0  (4 - l² > 0)
  have h4 : 0 < 4 - l ^ 2 := by nlinarith
  have hshift : 0 ≤ Eform l (a - aV, b - bV) := by
    simp only [Eform]
    nlinarith [sq_nonneg ((a - aV) - (l / 2) * (b - bV)), mul_nonneg (le_of_lt h4) (sq_nonneg (b - bV)),
      sq_nonneg (b - bV)]
  -- the exact KKT identity (ring)
  have hid : Eform l (a, b) - lam
      = lam * (l * a + b - 1) + lam * (2 * l * b - 1 - a) + Eform l (a - aV, b - bV) := by
    simp only [Eform, haV, hbV, hlam]
    field_simp
    ring
  have hsum : 0 ≤ lam * (l * a + b - 1) + lam * (2 * l * b - 1 - a) + Eform l (a - aV, b - bV) := by
    have t1 : 0 ≤ lam * (l * a + b - 1) := mul_nonneg hlam_nn hg1
    have t2 : 0 ≤ lam * (2 * l * b - 1 - a) := mul_nonneg hlam_nn hg2
    linarith
  have : 0 ≤ Eform l (a, b) - lam := by rw [hid]; exact hsum
  rw [hlam] at this ⊢; linarith

/-! ## §2.  The closed-form gate:  `(2−l)/(2l²+1) ≥ EfloorQ`  for `q ≥ 5`. -/

/-- The polynomial gate `g(l) ≥ 0` for `l ≥ φ = 2cos(π/5)`.  Largest real root `≈1.6124 < φ`. -/
theorem gpoly_nonneg (l : ℝ) (hlo : (1617 : ℝ) / 1000 ≤ l) (hhi : l < 2) :
    0 ≤ l ^ 7 + 2 * l ^ 6 - 3 * l ^ 5 - 4 * l ^ 3 - 4 * l ^ 2 - l - 2 := by
  nlinarith [hlo, hhi, sq_nonneg (l - 1617/1000), sq_nonneg l, mul_pos (show (0:ℝ) < l by linarith) (show (0:ℝ) < l by linarith),
    pow_pos (show (0:ℝ) < l by linarith) 3, pow_pos (show (0:ℝ) < l by linarith) 5,
    mul_nonneg (sub_nonneg.mpr hlo) (sub_nonneg.mpr hlo)]

/-- **Closed-form E-floor gate.**  For `l ∈ [φ, 2)` (i.e. `q ≥ 5`) and `cos(π/q) = l/2`,
`EfloorQ ≤ (2−l)/(2l²+1)`.  `EfloorQ` is rewritten with `cos(π/q)=l/2`. -/
theorem EfloorQ_le_vertex (m : ℕ) (l : ℝ) (hcos : Real.cos (Real.pi / ((m + 2 : ℕ) : ℝ)) = l / 2)
    (hlo : (1617 : ℝ) / 1000 ≤ l) (hhi : l < 2) :
    EfloorQ m l ≤ (2 - l) / (2 * l ^ 2 + 1) := by
  have hl0 : 0 < l := by linarith
  have h4 : 0 < 4 - l ^ 2 := by nlinarith
  have hD : 0 < 2 * l ^ 2 + 1 := by positivity
  set s : ℝ := Real.sqrt (2 * l ^ 2 + 1) with hs
  have hspos : 0 < s := by rw [hs]; exact Real.sqrt_pos.mpr (by positivity)
  have hssq : s ^ 2 = 2 * l ^ 2 + 1 := by rw [hs]; exact Real.sq_sqrt (by positivity)
  -- EfloorQ closed form: 1/(l³(αC + ρC·(l/2))) = (4-l²)/(l²((l²+2)+l·s))
  have hgate_den : 0 < (l ^ 2 + 2) + l * s := by positivity
  have hden2 : 0 < l ^ 2 * ((l ^ 2 + 2) + l * s) := by positivity
  have hEf : EfloorQ m l = (4 - l ^ 2) / (l ^ 2 * ((l ^ 2 + 2) + l * s)) := by
    rw [EfloorQ, hcos, alphaC, rhoC, ← hs]
    rw [div_eq_div_iff (by positivity) (ne_of_gt hden2)]
    field_simp
  rw [hEf]
  rw [div_le_div_iff₀ hden2 hD]
  -- goal: (4-l²)·(2l²+1) ≤ (2-l)·(l²((l²+2)+l s))
  -- i.e.  (2-l)·l²·(l²+2) + (2-l)·l³·s − (4-l²)(2l²+1) ≥ 0
  -- = P(l) + Q(l)·s   with Q=l³(2-l)>0, P=-l⁵+4l⁴-2l³-3l²-4 < 0,
  -- so use Q·s ≥ -P via squaring: (Q s)² = Q²(2l²+1) ≥ P²  ⟺  g(l)·(l-2)²(l+2) ≥ 0.
  have hQpos : 0 < l ^ 3 * (2 - l) := mul_pos (by positivity) (by linarith)
  set P : ℝ := -l ^ 5 + 4 * l ^ 4 - 2 * l ^ 3 - 3 * l ^ 2 - 4 with hP
  set Q : ℝ := l ^ 3 * (2 - l) with hQ
  have hPneg : P < 0 := by rw [hP]; nlinarith [hlo, hhi, sq_nonneg l, pow_pos hl0 4, pow_pos hl0 5]
  -- Q·s ≥ -P : both sides positive, square.  Q²s² − P² = g(l)·(l-2)²(l+2).
  have hg := gpoly_nonneg l hlo hhi
  have hsq : (Q * s) ^ 2 - P ^ 2 =
      (l ^ 7 + 2 * l ^ 6 - 3 * l ^ 5 - 4 * l ^ 3 - 4 * l ^ 2 - l - 2)
        * ((l - 2) ^ 2 * (l + 2)) := by
    rw [mul_pow, hssq, hP, hQ]; ring
  have hfactor_nn : 0 ≤ (l - 2) ^ 2 * (l + 2) := by positivity
  have hQs_sq_ge : P ^ 2 ≤ (Q * s) ^ 2 := by nlinarith [hsq, mul_nonneg hg hfactor_nn]
  have hQs_pos : 0 < Q * s := mul_pos hQpos hspos
  have hQs_ge_negP : -P ≤ Q * s := by nlinarith [hQs_sq_ge, hQs_pos, hPneg, sq_nonneg (Q*s + P)]
  -- assemble: (4-l²)(2l²+1) ≤ (2-l) l² ((l²+2)+l s)
  -- RHS − LHS = P + Q s ≥ 0
  nlinarith [hQs_ge_negP, hssq, hP, hQ]

/-! ## §3.  ★ The uniform corridor E-floor `hEfloor` (q ≥ 5). -/

/-- `q ≥ 5 ⟹ 2cos(π/q) ≥ 1617/1000` (a rational lower bound below `φ=2cos(π/5)≈1.618`). -/
theorem lamq_ge_of_q5 (q : ℕ) (hq : 5 ≤ q) : (1617 : ℝ) / 1000 ≤ 2 * Real.cos (Real.pi / q) := by
  have hqr : (0:ℝ) < (q:ℝ) := by exact_mod_cast (by omega : 0 < q)
  have hq5r : (5:ℝ) ≤ (q:ℝ) := by exact_mod_cast hq
  -- cos(π/q) ≥ cos(π/5)  (cos decreasing on [0,π], 0 ≤ π/q ≤ π/5 ≤ π)
  have hx0 : 0 ≤ Real.pi / q := by positivity
  have hx5 : Real.pi / q ≤ Real.pi / 5 := by
    apply div_le_div_of_nonneg_left (le_of_lt Real.pi_pos) (by norm_num) hq5r
  have hxpi : Real.pi / 5 ≤ Real.pi := by
    rw [div_le_iff₀ (by norm_num)]; nlinarith [Real.pi_pos]
  have hmono : Real.cos (Real.pi / 5) ≤ Real.cos (Real.pi / q) :=
    Real.cos_le_cos_of_nonneg_of_le_pi hx0 hxpi hx5
  -- cos(π/5) = (1+√5)/4 ; (1+√5)/2 ≥ 1617/1000  since √5 ≥ 2.236
  have hc5 : Real.cos (Real.pi / 5) = (1 + Real.sqrt 5) / 4 := Real.cos_pi_div_five
  have hsqrt5 : (2236 : ℝ) / 1000 ≤ Real.sqrt 5 := by
    rw [show (2236:ℝ)/1000 = Real.sqrt ((2236/1000)^2) by rw [Real.sqrt_sq (by norm_num)]]
    apply Real.sqrt_le_sqrt; norm_num
  have : (1617 : ℝ) / 1000 ≤ 2 * Real.cos (Real.pi / 5) := by
    rw [hc5]; rw [show 2 * ((1 + Real.sqrt 5) / 4) = (1 + Real.sqrt 5)/2 by ring]
    linarith [hsqrt5]
  linarith [hmono]

/-- **★ THE UNIFORM CORRIDOR E-FLOOR (faithful, q ≥ 5).**  For `q = m+2 ≥ 5` (`m ≥ 3`),
`l = lamq q`, and a corridor point `p ∈ Dcorr l` on the `k=1` part (floor bracket
`λb ≤ 1+a` ∧ `1+a < 2λb`), the conserved ellipse clears the E-floor:
  `EfloorQ m l ≤ Eform l p`.
This discharges the keystone hypothesis `hEfloor` uniformly in `q ≥ 5`.

Hypotheses `hbr_lo`, `hbr_hi` are EXACTLY the `isK1`/`kfloor=1` floor bracket, and `hp` is
the corridor membership (`Sclosed ⊆ Dcorr`).  No `sorry`; only the def-unfolds and the two
PROVED analytic lemmas above. -/
theorem hEfloor_uniform (m : ℕ) (hm : 3 ≤ m) (l : ℝ) (hl : l = lamq (m + 2))
    (p : ℝ × ℝ) (hp : p ∈ Dcorr l)
    (hbr_lo : l * p.2 ≤ 1 + p.1) (hbr_hi : 1 + p.1 < 2 * l * p.2) :
    EfloorQ m l ≤ Eform l p := by
  obtain ⟨ha0, ha1, hb0, hb1, hab1, hba1⟩ := hp
  set q : ℕ := m + 2 with hq_def
  have hq5 : 5 ≤ q := by omega
  -- l = 2cos(π/q), the value facts
  have hcos : Real.cos (Real.pi / ((m + 2 : ℕ) : ℝ)) = l / 2 := by
    rw [hl, lamq, hq_def]; ring
  have hlo : (1617 : ℝ) / 1000 ≤ l := by
    rw [hl, lamq, hq_def]; exact lamq_ge_of_q5 q hq5
  have hl0 : 0 < l := by linarith
  have hhi : l < 2 := by
    rw [hl, lamq, hq_def]
    have hqr : (0:ℝ) < ((m+2:ℕ):ℝ) := by positivity
    have h3 : (3:ℝ) ≤ ((m+2:ℕ):ℝ) := by exact_mod_cast (by omega : 3 ≤ m+2)
    have hpos : 0 < Real.pi / ((m+2:ℕ):ℝ) := by positivity
    have hlt : Real.pi / ((m+2:ℕ):ℝ) < Real.pi := by
      rw [div_lt_iff₀ hqr]
      nlinarith [Real.pi_pos, h3]
    have hcle : Real.cos (Real.pi / ((m+2:ℕ):ℝ)) < 1 := by
      rcases lt_or_eq_of_le (Real.cos_le_one (Real.pi / ((m+2:ℕ):ℝ))) with h | h
      · exact h
      · exfalso
        have := (Real.cos_eq_one_iff_of_lt_of_lt (x := Real.pi/((m+2:ℕ):ℝ))
          (by linarith [Real.pi_pos]) (by linarith [Real.pi_pos])).mp h
        linarith
    linarith
  -- geometric floor:  (2-l)/(2l²+1) ≤ Eform
  have hgeo : (2 - l) / (2 * l ^ 2 + 1) ≤ Eform l p := by
    have := Eform_ge_vertex l p.1 p.2 hl0 hhi (le_of_lt hba1) (le_of_lt hbr_hi)
    simpa using this
  -- closed-form gate:  EfloorQ ≤ (2-l)/(2l²+1)
  have hgate := EfloorQ_le_vertex m l hcos hlo hhi
  linarith

/-- **★ KEYSTONE WIRING.**  The exact `hEfloor` obligation of `Xomega_ge_unconditional`,
delivered for `q = m+2 ≥ 5`.  `isK1` is supplied abstractly together with the DEFINITIONAL
bridge `hK1 : isK1 p ↔ (λb ≤ 1+a ∧ 1+a < 2λb)` (= `kfloor_eq_one_iff_bracket`, the genuine
`kfloor = 1` characterization), and `hpcorr : Sclosed ⊆ Dcorr`.  Conclusion: the keystone
hypothesis `hEfloor` holds.  This is the literal shape consumed by `conull_cover_assembled`
/ `Xomega_ge_unconditional`. -/
theorem hEfloor_keystone (m : ℕ) (hm : 3 ≤ m) (l : ℝ) (hl : l = lamq (m + 2))
    (Sclosed : Set (ℝ × ℝ)) (isK1 : (ℝ × ℝ) → Prop)
    (hpcorr : ∀ p ∈ Sclosed, isK1 p → p ∈ Dcorr l)
    (hK1 : ∀ p, isK1 p → (l * p.2 ≤ 1 + p.1 ∧ 1 + p.1 < 2 * l * p.2)) :
    ∀ p ∈ Sclosed, isK1 p → EfloorQ m l ≤ Eform l p := by
  intro p hp hk1
  obtain ⟨hbr_lo, hbr_hi⟩ := hK1 p hk1
  exact hEfloor_uniform m hm l hl p (hpcorr p hp hk1) hbr_lo hbr_hi

end

#print axioms hEfloor_keystone
#print axioms hEfloor_uniform
#print axioms Eform_ge_vertex
#print axioms EfloorQ_le_vertex
#print axioms gpoly_nonneg
#print axioms lamq_ge_of_q5

import Mathlib
set_option maxHeartbeats 4000000
/-!
# WF5 obs_align — relate the F-window scalar product `a*b` to the genuine observable `Pgen`.

On the scalar branch `q-1` the gap-product is `a*b` (the observable consumed by the F-window
contradiction `case_q{q}`). The genuine observable is `Pgen l (a,b) = a (a + l b)/l`. We want a
clean transfer lemma so that a `Pgen`-sub-threshold F-run implies a `(a*b)`-sub-threshold run, ready
to invoke `g{q}_no_window` / `case_q{q}`.

CORE IDENTITY (pure algebra, `l ≠ 0`):
    Pgen l (a,b) = a*(a + l*b)/l = a^2/l + a*b,
so
    Pgen l (a,b) - a*b = a^2 / l   ( ≥ 0 when l > 0 ),
hence
    a*b ≤ Pgen l (a,b)   and strictly   a*b < Pgen l (a,b)   when a ≠ 0.

Consequences (the transfer):
* `prod_lt_of_Pgen_lt`   : `Pgen l (a,b) < t  →  a*b < t`              (scalar branch, `l>0`).
* `prod_run_of_Pgen_run` : a 6-step `Pgen`-sub-threshold F-run gives a 6-step `(a*b)`-sub-threshold
                           run — exactly the `hP0..hP5` hypotheses `case_q18` consumes.
* the reverse gap `Pgen - a*b = a^2/l` is recorded exactly (`Pgen_sub_prod`) and is the *only*
  slack, so the transfer is tight: on the cusp line `a*b = Pgen - a^2/l` shows the products vanish
  while `Pgen = a^2/l` stays positive — the products are STRICTLY below `Pgen`, never above.

`#print axioms` on every theorem must be `[propext, Classical.choice, Quot.sound]`.
-/
namespace HeckeObsAlign

noncomputable section

/-- Genuine observable `P = a (a + l b)/l` (matches the assembly's `Pgen` and the q=5 `P3`). -/
def Pgen (l : ℝ) (p : ℝ × ℝ) : ℝ := p.1 * (p.1 + l * p.2) / l
@[simp] lemma Pgen_apply (l : ℝ) (p : ℝ × ℝ) : Pgen l p = p.1 * (p.1 + l * p.2) / l := rfl

/-- Scalar-branch gap-product observable `Pprod (a,b) = a*b` (the F-window observable). -/
def Pprod (p : ℝ × ℝ) : ℝ := p.1 * p.2
@[simp] lemma Pprod_apply (p : ℝ × ℝ) : Pprod p = p.1 * p.2 := rfl

/-! ## §1. THE CORE IDENTITY linking `Pgen` and the product `a*b`. -/

/-- **Pgen splits as product + `a²/l`.**  `Pgen l (a,b) = a*b + a^2/l`. Pure field algebra. -/
theorem Pgen_eq_prod_add (l a b : ℝ) (hl : l ≠ 0) :
    Pgen l (a, b) = a * b + a ^ 2 / l := by
  simp only [Pgen_apply]
  field_simp
  ring

/-- **The reverse-gap identity** `Pgen − a*b = a²/l`. This is the exact (and only) slack between the
genuine observable and the F-window product. -/
theorem Pgen_sub_prod (l a b : ℝ) (hl : l ≠ 0) :
    Pgen l (a, b) - a * b = a ^ 2 / l := by
  rw [Pgen_eq_prod_add l a b hl]; ring

/-- **`a²/l ≥ 0` for `l > 0`** (the sign of the gap). -/
theorem gap_nonneg (l a : ℝ) (hl : 0 < l) : 0 ≤ a ^ 2 / l :=
  div_nonneg (sq_nonneg a) hl.le

/-! ## §2. THE TRANSFER (product ≤ Pgen, strictly when a ≠ 0). -/

/-- **Product is `≤` the genuine observable** (`l > 0`): `a*b ≤ Pgen l (a,b)`. The gap is `a²/l ≥ 0`. -/
theorem prod_le_Pgen (l a b : ℝ) (hl : 0 < l) :
    a * b ≤ Pgen l (a, b) := by
  have h := Pgen_sub_prod l a b (ne_of_gt hl)
  have hnn := gap_nonneg l a hl
  linarith [h, hnn]

/-- **STRICT product `<` genuine observable** when `a ≠ 0` (`l > 0`): `a*b < Pgen l (a,b)`. On the
genuine domain `a > 0` this is always strict — the products are *strictly* below `Pgen`. -/
theorem prod_lt_Pgen (l a b : ℝ) (hl : 0 < l) (ha : a ≠ 0) :
    a * b < Pgen l (a, b) := by
  have h := Pgen_sub_prod l a b (ne_of_gt hl)
  have hpos : 0 < a ^ 2 / l := div_pos (by positivity) hl
  linarith [h, hpos]

/-- **THE KEY TRANSFER LEMMA.**  A `Pgen`-sub-threshold point is product-sub-threshold:
`Pgen l (a,b) < t  ⟹  a*b < t`.  (Because `a*b ≤ Pgen`.)  This is exactly what lets the F-window's
"no sub-threshold `a*b`" obstruction fire on a `Pgen`-sub-threshold run. -/
theorem prod_lt_of_Pgen_lt (l a b t : ℝ) (hl : 0 < l)
    (hP : Pgen l (a, b) < t) : a * b < t :=
  lt_of_le_of_lt (prod_le_Pgen l a b hl) hP

/-! ## §3. THE 6-STEP F-RUN TRANSFER (the shape `case_q{q}` consumes).

On a scalar-branch F-stretch the coordinates are `(a,b),(b,c),(c,d),(d,e),(e,f),(f,g)` (consecutive
pairs of the scalar orbit, with the shift `(orbit n).2 = (orbit (n+1)).1`). The F-window contradiction
`case_q18` consumes the six PRODUCT sub-threshold facts `a*b, b*c, c*d, d*e, e*f, f*g < 1/lam^3`.
Here we package: from the six GENUINE-observable sub-threshold facts (`Pgen` on each pair), the six
product facts follow.  So a `Pgen`-sub-threshold F-run ⟹ a product-sub-threshold run. -/

/-- **6-step F-run transfer.**  Six consecutive `Pgen`-sub-threshold pairs give the six product
sub-threshold facts that `case_q18`/`g{q}_no_window` consume.  `t = 1/lam^3` in the application. -/
theorem prod_run_of_Pgen_run (l a b c d e f g t : ℝ) (hl : 0 < l)
    (hQ0 : Pgen l (a, b) < t) (hQ1 : Pgen l (b, c) < t) (hQ2 : Pgen l (c, d) < t)
    (hQ3 : Pgen l (d, e) < t) (hQ4 : Pgen l (e, f) < t) (hQ5 : Pgen l (f, g) < t) :
    a * b < t ∧ b * c < t ∧ c * d < t ∧ d * e < t ∧ e * f < t ∧ f * g < t :=
  ⟨prod_lt_of_Pgen_lt l a b t hl hQ0, prod_lt_of_Pgen_lt l b c t hl hQ1,
   prod_lt_of_Pgen_lt l c d t hl hQ2, prod_lt_of_Pgen_lt l d e t hl hQ3,
   prod_lt_of_Pgen_lt l e f t hl hQ4, prod_lt_of_Pgen_lt l f g t hl hQ5⟩

/-! ## §3b. ORBIT-LEVEL form (matches the assembly's `genuine_no_sustained_orbit`).

The genuine assembly works with `orbit : ℕ → ℝ × ℝ` on the scalar branch, where `Tmap_fst` gives the
shift `(orbit n).2 = (orbit (n+1)).1`. The genuine observable on step `n` is `Pgen l (orbit n)`, and
the F-window product on step `n` is `(orbit n).1 * (orbit (n+1)).1`. Under the shift these are exactly
`Pgen l ((orbit n).1, (orbit (n+1)).1)` and its product — so the transfer applies verbatim along the
orbit, with no extra hypotheses beyond `l > 0` and the shift. -/

/-- **Orbit-step transfer.**  Given the scalar-branch shift `(orbit n).2 = (orbit (n+1)).1`, a
`Pgen`-sub-threshold step forces the consecutive-coordinate product sub-threshold:
`Pgen l (orbit n) < t ⟹ (orbit n).1 * (orbit (n+1)).1 < t`. -/
theorem orbit_prod_lt_of_Pgen_lt (l : ℝ) (orbit : ℕ → ℝ × ℝ) (n : ℕ) (t : ℝ) (hl : 0 < l)
    (hlink : (orbit n).2 = (orbit (n + 1)).1)
    (hP : Pgen l (orbit n) < t) :
    (orbit n).1 * (orbit (n + 1)).1 < t := by
  have hPpair : Pgen l ((orbit n).1, (orbit n).2) < t := by
    rw [Prod.mk.eta]; exact hP
  have := prod_lt_of_Pgen_lt l (orbit n).1 (orbit n).2 t hl hPpair
  rw [hlink] at this; exact this

/-! ## §4. NON-VACUITY of the transfer (the cusp line witnesses the strict gap).

On the cusp line `(s,0)` with `0 < s`: the product is `Pprod (s,0) = 0`, but `Pgen l (s,0) = s²/l > 0`.
So `Pprod < Pgen` is STRICT there and the product is sub-threshold (`0 < 1/l³`) while `Pgen` need NOT
be — i.e. the transfer's slack `a²/l` is genuinely nonzero exactly where the cusp lives. This is the
non-vacuity witness: the F-window obstruction is on the *product*, the genuine bound on *Pgen*, and
they differ by precisely `a²/l ≥ 0`, vanishing only at `a = 0`. -/

/-- On the cusp line `(s,0)`: the product vanishes (`Pprod = 0`) and `Pgen = s²/l`. -/
theorem cusp_line_values (l s : ℝ) :
    Pprod (s, (0:ℝ)) = 0 ∧ Pgen l (s, (0:ℝ)) = s ^ 2 / l := by
  refine ⟨?_, ?_⟩
  · simp only [Pprod_apply, mul_zero]
  · simp only [Pgen_apply, mul_zero, add_zero]; ring

/-- **Non-vacuity witness for the strict gap.**  For `0 < s`, `l > 0`: `Pprod (s,0) = 0 < s²/l =
Pgen l (s,0)`, so the gap `a²/l` is strictly positive on the cusp line — the product is strictly
sub-`Pgen`. -/
theorem cusp_gap_strict (l s : ℝ) (hl : 0 < l) (hs : 0 < s) :
    Pprod (s, (0:ℝ)) < Pgen l (s, (0:ℝ)) := by
  obtain ⟨hp, hg⟩ := cusp_line_values l s
  rw [hp, hg]; positivity

end

end HeckeObsAlign

-- ════════════ AXIOM AUDIT ════════════
#print axioms HeckeObsAlign.Pgen_eq_prod_add
#print axioms HeckeObsAlign.Pgen_sub_prod
#print axioms HeckeObsAlign.gap_nonneg
#print axioms HeckeObsAlign.prod_le_Pgen
#print axioms HeckeObsAlign.prod_lt_Pgen
#print axioms HeckeObsAlign.prod_lt_of_Pgen_lt
#print axioms HeckeObsAlign.prod_run_of_Pgen_run
#print axioms HeckeObsAlign.orbit_prod_lt_of_Pgen_lt
#print axioms HeckeObsAlign.cusp_line_values
#print axioms HeckeObsAlign.cusp_gap_strict

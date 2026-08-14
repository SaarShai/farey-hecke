import Mathlib

open scoped BigOperators

namespace CharacterOrthogonality

variable {G R I : Type*} [CommGroup G] [CommRing R] [Fintype I]

/- A finite family of multiplicative characters. -/
variable (chi : I → G →* R)

/-- The algebraic kernel in the manuscript targets `a⁻¹`, because
`chi a * chi x = chi (a * x)`. -/
theorem weighted_character_sum (a x : G) :
    (Finset.univ.sum fun i => (1 - chi i a) * chi i x) =
      (Finset.univ.sum fun i => chi i x) -
        (Finset.univ.sum fun i => chi i (a * x)) := by
  simp only [sub_mul, one_mul, map_mul, Finset.sum_sub_distrib]

open Classical in
/- Under the usual character-orthogonality hypothesis, the weighted kernel is
the difference of the indicators of `1` and `a⁻¹`, not `1` and `a`. -/
theorem weighted_character_sum_eq_inverse_indicator
    (horth : forall y : G,
      (Finset.univ.sum fun i => chi i y) =
        if y = 1 then (Fintype.card I : R) else 0)
    (a x : G) :
    (Finset.univ.sum fun i => (1 - chi i a) * chi i x) =
      (if x = 1 then (Fintype.card I : R) else 0) -
        (if x = a⁻¹ then (Fintype.card I : R) else 0) := by
  classical
  rw [weighted_character_sum chi a x, horth x, horth (a * x)]
  congr 2
  simp only [mul_eq_one_iff_eq_inv]
  apply propext
  constructor
  · intro h
    simpa using (congrArg (fun y : G => y⁻¹) h).symm
  · intro h
    simpa using (congrArg (fun y : G => y⁻¹) h).symm

/-- The concrete modulus-7 mismatch used in the audit: `3⁻¹ = 5 (mod 7)`. -/
theorem three_inverse_mod_seven : (3 : ZMod 7)⁻¹ = 5 := by
  native_decide

/-- Hence the kernel printed with `a = 3` cannot select the class `3`. -/
theorem three_not_its_inverse_mod_seven : (3 : ZMod 7) ≠ (3 : ZMod 7)⁻¹ := by
  native_decide

end CharacterOrthogonality

#print axioms CharacterOrthogonality.weighted_character_sum
#print axioms CharacterOrthogonality.weighted_character_sum_eq_inverse_indicator
#print axioms CharacterOrthogonality.three_inverse_mod_seven
#print axioms CharacterOrthogonality.three_not_its_inverse_mod_seven

import Mathlib

/-!
GATE 2 (Hecke-BCZ genuine confinement) — formal BEDROCK lemmas.
λ=2cos(π/q); Chebyshev iterates X(-1)=0, X 0=1, X(i+1)=λ X i - X(i-1) (so X i = U_i(cos π/q)).
The genuine BCZ_q per-branch Jacobian on branch i, floor k is
  DT = [[X i, X(i-1)], [X(i+1)+k λ X i, X i + k λ X(i-1)]].
These three lemmas formalize: (1) the Casorati/Wronskian invariant is constant; (2) it equals
det DT, hence det DT = 1 (AREA-PRESERVING — the KAM-wall source); (3) on branch q-1 (X(q-1)=0,
X(q-2)=1) the per-step trace is k λ, so for λ∈(1,2) only floors k≤1 are elliptic (|tr|<2) =
exactly the two G_q=(2,q,∞) elliptic generators (k=0 order-2 tr 0; k=1 order-q tr λ).
All three are TRUE (numerically verified 2026-06-03). Prove each (replace `sorry`); axioms must be
exactly [propext, Classical.choice, Quot.sound], no sorryAx.
-/
namespace GATE2Base

/-
**Casorati invariant is constant** along the Hecke recurrence (any l, any X).
-/
theorem casorati_const (l : ℝ) (X : ℤ → ℝ)
    (hrec : ∀ i : ℤ, X (i + 1) = l * X i - X (i - 1)) (i : ℤ) :
    X i ^ 2 - X (i - 1) * X (i + 1) = X 0 ^ 2 - X (-1) * X 1 := by
  induction' i using Int.induction_on with n ihn n ihn;
  · rfl;
  · grind +ring;
  · grind

/-
**The Casorati invariant equals det DT.** With the recurrence `Xip1 = l*Xi - Xim1`,
the Jacobian determinant `Xi*(Xi+klXim1) - Xim1*(Xip1+klXi)` collapses to `Xi^2 - Xim1*Xip1`
(independent of k). Combined with `casorati_const` and `X(-1)=0, X 0=1` this gives det DT = 1.
-/
theorem det_jacobian_eq_casorati (l Xi Xim1 Xip1 k : ℝ)
    (hX : Xip1 = l * Xi - Xim1) :
    Xi * (Xi + k * l * Xim1) - Xim1 * (Xip1 + k * l * Xi) = Xi ^ 2 - Xim1 * Xip1 := by
  rw [hX]; ring

/-
**Two-elliptic-generator classification on branch q-1.** There the per-step trace is `k*l`
(since `Xi=0`); for `l∈(1,2)` it is elliptic (`|k*l|<2`) iff `k ≤ 1`.
-/
theorem trace_branch_qm1_elliptic_iff (l : ℝ) (hl1 : 1 < l) (hl2 : l < 2) (k : ℕ) :
    |(k : ℝ) * l| < 2 ↔ k ≤ 1 := by
  rw [ abs_of_nonneg ] <;> try positivity;
  exact ⟨ fun h => Nat.le_of_lt_succ ( by rw [ ← @Nat.cast_lt ℝ ] ; push_cast; nlinarith ), fun h => by interval_cases k <;> norm_num ; linarith ⟩

end GATE2Base
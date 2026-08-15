import Mathlib

/-!
# M1D q=4 intertwiner U₄: the 5 ARISTOTLE-ABLE finite-algebra obligations

Source: `research_notes/rh_goals_2026-08-14/lane_g/M1D_U4_CONSTRUCTION.md` (2026-08-15),
gaps ledger §9, obligations tagged **ARISTOTLE-ABLE**: G1, G2, and the weight-neutrality
computation of §1. Each statement below is finite/algebraic — no operator-space analysis,
no meromorphic continuation, no infinite alphabet — matching the note's own scoping
("at the linear-algebra level" for the determinant splitting; a finite alphabet-generator
identity for the coset cocycle; a single chain-rule computation for weight-neutrality).

Deliberately OUT OF SCOPE (not dispatched, FRONTIER-tagged in the note's ledger): G5–G9
(the Eisenstein-derivation of `phi_4`, the resonance/divisor transport, the `N_{s,+}`
↔ `Z_{Γ₀(2)}` identification) — none of these are finitely statable without importing
the Selberg zeta function and MMS's operator category wholesale.
-/

open Matrix

/-! ## 1. Coset-cocycle constancy

M1D §2.3 / §4 (C7): `ρ⁺(A_n) = σ` for **every** `n ∈ A` (uniform across the infinite
alphabet), hence for a length-`r` word `M_w = A_{a₁}⋯A_{a_r}`, `ρ⁺(M_w) = σ^r` — the
cocycle depends only on word length. Since `A_n = W₂ T^n` with `T ∈ Γ₀(2)` (so
`ρ⁺(T) = 1`) and `ρ⁺` is a group homomorphism, this reduces to a one-line induction on
the word list, stated here for an abstract group `G` and a homomorphism to the sign
group `Multiplicative (ZMod 2)`.

Quoted (M1D §2.3): "`ρ⁺(A_n) = σ` for **every** `n ∈ A`, with no exceptions. This
uniformity is the structural reason the repair works cleanly: the coset cocycle is
constant across the whole infinite alphabet." -/
theorem coset_cocycle_constant {G : Type*} [Group G]
    (φ : G →* Multiplicative (ZMod 2)) (W T : G)
    (hW : φ W = Multiplicative.ofAdd (1 : ZMod 2)) (hT : φ T = 1)
    (L : List ℤ) :
    φ ((L.map (fun n => W * T ^ n)).prod)
      = Multiplicative.ofAdd ((L.length : ZMod 2)) := by
  sorry

/-! ## 2. The W₂ normalizer computation on Γ₀(2)

M1D §2.3: "For `γ = [[a,b],[2c,d]] ∈ Γ₀(2)` (so `ad − 2bc = 1`), direct multiplication
gives `w γ w⁻¹ = [[d, −c], [−2b, a]] ∈ Γ₀(2)`." Stated here as the inverse-free matrix
identity `w γ = [[d,−c],[−2b,a]] w` (equivalent given `w` invertible over `ℚ`), plus the
determinant preservation that keeps the image in `Γ₀(2)`. -/
theorem w2_conjugation_identity (a b c d : ℤ) :
    (!![0, -1; 2, 0] : Matrix (Fin 2) (Fin 2) ℤ) * !![a, b; 2 * c, d]
      = !![d, -c; -2 * b, a] * !![0, -1; 2, 0] := by
  sorry

theorem w2_conjugate_in_gamma0_2 (a b c d : ℤ) (h : a * d - 2 * b * c = 1) :
    d * a - 2 * (-c) * (-b) = 1 := by
  sorry

/-! ## 3. Weight-neutrality of the D₂ composition operator (chain rule)

M1D §1: "Conjugation is weight-neutral. Let `δ(x) = √2 x` and `ϑ̂_n = δ⁻¹ ∘ ϑ_n ∘ δ`.
Then by the chain rule `ϑ̂_n'(x) = (1/√2)·ϑ_n'(√2 x)·√2 = ϑ_n'(√2 x)`, so the `s`-power
of the branch Jacobian transports with **no extra scalar factor**." Stated here with the
explicit closed forms `ϑ_n(z) = −1/(z + n√2)`, `ϑ̂_n(x) = δ⁻¹(ϑ_n(δ x)) = −1/(2(x+n))`. -/
noncomputable def theta (n : ℝ) (z : ℝ) : ℝ := -1 / (z + n * Real.sqrt 2)

noncomputable def thetaHat (n : ℝ) (x : ℝ) : ℝ := -1 / (2 * (x + n))

theorem thetaHat_eq_delta_conj (n x : ℝ) :
    thetaHat n x = theta n (Real.sqrt 2 * x) / Real.sqrt 2 := by
  sorry

theorem weight_neutral_chain_rule (n x : ℝ) (hx : x + n ≠ 0) :
    deriv (thetaHat n) x = deriv (theta n) (Real.sqrt 2 * x) := by
  sorry

/-! ## 4. The block-diagonalization identity

M1D §3.3: with `V = (1/√2)[[1,1],[1,−1]]` (the character-basis change) and
`σ = [[0,1],[1,0]]`, `V σ V⁻¹ = diag(1,−1)`. Stated inverse-free as `V σ = diag(1,−1) V`
(equivalent given `V` invertible). -/
theorem block_diagonalization_identity :
    ((Real.sqrt 2)⁻¹ • (!![1, 1; 1, -1] : Matrix (Fin 2) (Fin 2) ℝ)) * !![0, 1; 1, 0]
      = (!![1, 0; 0, -1] : Matrix (Fin 2) (Fin 2) ℝ)
          * ((Real.sqrt 2)⁻¹ • (!![1, 1; 1, -1] : Matrix (Fin 2) (Fin 2) ℝ)) := by
  sorry

/-! ## 5. The exact 2×2 determinant splitting, at the linear-algebra level

M1D §3.3 / gaps ledger G1: `det(1 − L̂ ⊗ σ) = det(1 − L̂) · det(1 + L̂)`. The note's own
proof route (trace expansion + meromorphic continuation) is for a nuclear operator on a
Banach space and is out of scope here; the ledger explicitly flags the underlying content
as "a standard nuclear-determinant lemma" whose finite shadow — the `n × n` matrix
identity below, with `A ⊗ σ` realized as the block matrix `[[0,A],[A,0]]` — is the
ARISTOTLE-ABLE part. -/
theorem det_block_swap_splitting {n : ℕ} (A : Matrix (Fin n) (Fin n) ℂ) :
    (Matrix.fromBlocks (1 : Matrix (Fin n) (Fin n) ℂ) (-A) (-A) 1).det
      = (1 - A).det * (1 + A).det := by
  sorry

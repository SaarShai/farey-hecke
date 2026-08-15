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
  induction L with
  | nil => simp
  | cons a L ih =>
      simp only [List.map_cons, List.prod_cons, map_mul, ih, List.length_cons, hW,
        map_zpow, hT, _root_.one_zpow, mul_one, ← ofAdd_add]
      congr 1
      push_cast
      ring

/-! ## 2. The W₂ normalizer computation on Γ₀(2)

M1D §2.3: "For `γ = [[a,b],[2c,d]] ∈ Γ₀(2)` (so `ad − 2bc = 1`), direct multiplication
gives `w γ w⁻¹ = [[d, −c], [−2b, a]] ∈ Γ₀(2)`." Stated here as the inverse-free matrix
identity `w γ = [[d,−c],[−2b,a]] w` (equivalent given `w` invertible over `ℚ`), plus the
determinant preservation that keeps the image in `Γ₀(2)`. -/
theorem w2_conjugation_identity (a b c d : ℤ) :
    (!![0, -1; 2, 0] : Matrix (Fin 2) (Fin 2) ℤ) * !![a, b; 2 * c, d]
      = !![d, -c; -2 * b, a] * !![0, -1; 2, 0] := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

theorem w2_conjugate_in_gamma0_2 (a b c d : ℤ) (h : a * d - 2 * b * c = 1) :
    d * a - 2 * (-c) * (-b) = 1 := by
  linarith [h, mul_comm a d, mul_comm b c]

/-! ## 3. Weight-neutrality of the D₂ composition operator (chain rule)

M1D §1: "Conjugation is weight-neutral. Let `δ(x) = √2 x` and `ϑ̂_n = δ⁻¹ ∘ ϑ_n ∘ δ`.
Then by the chain rule `ϑ̂_n'(x) = (1/√2)·ϑ_n'(√2 x)·√2 = ϑ_n'(√2 x)`, so the `s`-power
of the branch Jacobian transports with **no extra scalar factor**." Stated here with the
explicit closed forms `ϑ_n(z) = −1/(z + n√2)`, `ϑ̂_n(x) = δ⁻¹(ϑ_n(δ x)) = −1/(2(x+n))`. -/
noncomputable def theta (n : ℝ) (z : ℝ) : ℝ := -1 / (z + n * Real.sqrt 2)

noncomputable def thetaHat (n : ℝ) (x : ℝ) : ℝ := -1 / (2 * (x + n))

theorem thetaHat_eq_delta_conj (n x : ℝ) :
    thetaHat n x = theta n (Real.sqrt 2 * x) / Real.sqrt 2 := by
  have hs : Real.sqrt 2 ≠ 0 := by positivity
  have hs2 : Real.sqrt 2 * Real.sqrt 2 = 2 := Real.mul_self_sqrt (by norm_num)
  have key : Real.sqrt 2 * x + n * Real.sqrt 2 = Real.sqrt 2 * (x + n) := by ring
  unfold theta thetaHat
  rw [key]
  rcases eq_or_ne (x + n) 0 with h | h
  · rw [h]; simp
  · field_simp
    nlinarith [hs2]

theorem weight_neutral_chain_rule (n x : ℝ) (hx : x + n ≠ 0) :
    deriv (thetaHat n) x = deriv (theta n) (Real.sqrt 2 * x) := by
  have hs : Real.sqrt 2 ≠ 0 := by positivity
  have hden1 : (2 : ℝ) * (x + n) ≠ 0 := mul_ne_zero two_ne_zero hx
  have hrw : Real.sqrt 2 * x + n * Real.sqrt 2 = Real.sqrt 2 * (x + n) := by ring
  have hden2 : Real.sqrt 2 * x + n * Real.sqrt 2 ≠ 0 := by
    rw [hrw]; exact mul_ne_zero hs hx
  have h1 : HasDerivAt (thetaHat n) (1 / (2 * (x + n) ^ 2)) x := by
    have hv : HasDerivAt (fun y : ℝ => 2 * (y + n)) 2 x := by
      simpa using ((hasDerivAt_id x).add_const n).const_mul (2 : ℝ)
    have h := (hasDerivAt_const x (-1 : ℝ)).div hv hden1
    simpa only [thetaHat] using h.congr_deriv (by field_simp; ring)
  have h2 : HasDerivAt (theta n) (1 / (2 * (x + n) ^ 2)) (Real.sqrt 2 * x) := by
    have hv : HasDerivAt (fun z : ℝ => z + n * Real.sqrt 2) 1 (Real.sqrt 2 * x) :=
      (hasDerivAt_id _).add_const _
    have h := (hasDerivAt_const (Real.sqrt 2 * x) (-1 : ℝ)).div hv hden2
    have heq : (0 * (Real.sqrt 2 * x + n * Real.sqrt 2) - (-1 : ℝ) * 1)
        / (Real.sqrt 2 * x + n * Real.sqrt 2) ^ 2 = 1 / (2 * (x + n) ^ 2) := by
      rw [hrw, mul_pow, Real.sq_sqrt (by norm_num : (0:ℝ) ≤ 2)]
      norm_num
    simpa only [theta] using h.congr_deriv heq
  rw [h1.deriv, h2.deriv]

/-! ## 4. The block-diagonalization identity

M1D §3.3: with `V = (1/√2)[[1,1],[1,−1]]` (the character-basis change) and
`σ = [[0,1],[1,0]]`, `V σ V⁻¹ = diag(1,−1)`. Stated inverse-free as `V σ = diag(1,−1) V`
(equivalent given `V` invertible). -/
theorem block_diagonalization_identity :
    ((Real.sqrt 2)⁻¹ • (!![1, 1; 1, -1] : Matrix (Fin 2) (Fin 2) ℝ)) * !![0, 1; 1, 0]
      = (!![1, 0; 0, -1] : Matrix (Fin 2) (Fin 2) ℝ)
          * ((Real.sqrt 2)⁻¹ • (!![1, 1; 1, -1] : Matrix (Fin 2) (Fin 2) ℝ)) := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [Matrix.mul_apply, Fin.sum_univ_succ]

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
  rw [Matrix.det_fromBlocks_one₁₁, ← Matrix.det_mul]
  congr 1
  noncomm_ring

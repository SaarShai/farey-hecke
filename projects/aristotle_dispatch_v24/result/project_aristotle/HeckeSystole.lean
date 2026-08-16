import Mathlib

/-!
# U2b Hecke-systole anchor: finite-algebra obligations (v24 dispatch)

Source: `research_notes/rh_goals_2026-08-14/lane_g/LAW_U2B_CLOSURE.md` §6,
Aristotle-able items **A1, A2, A3, A6**. Each statement below is finite/algebraic
— a Chebyshev-recursion matrix identity, a nonnegative-matrix trace-path
inequality, a systole case-analysis given A1+A2 (stated over a fixed finite
alphabet), and an explicit real-polynomial non-monotonicity witness — matching
the note's own scoping.

Skipped: **A5** (the `t cot t` strict antitonicity lemma, Theorem U2b-B's
engine) and **A4** (`W_q` antitone in `q`, which depends on A5). Both are
genuine analysis (derivative/limit arguments over `(0, π)` and an infinite
family indexed by `q`), not finite algebra — recorded in `SKIPPED.md`.

## Note on the ordered product of matrices

The A2/A3 statements as originally drafted wrote the product of a family of
matrices `A : Fin n → Matrix (Fin 2) (Fin 2) ℝ` as `∏ i, A i`. That notation is
`Finset.prod`, which requires a `CommMonoid` structure on the target; matrix
multiplication is *not* commutative and Mathlib provides no such instance, so
those statements did not elaborate. They are restated verbatim below with the
(order-sensitive) product written as `matProd A := (List.ofFn A).prod`, i.e.
`A 0 * A 1 * ⋯ * A (n-1)`, which is the intended meaning. Nothing else in the
statements changed.
-/

open Matrix

/-! ## A1 (§6, "the Chebyshev normal form"). The load-bearing algebra:
`S R^a = -M_a`, `det M_a = 1`, via the Chebyshev-type recursion
`u_0 = 0, u_1 = 1, u_{n+2} = lam * u_{n+1} - u_n`. -/

variable {R : Type*} [CommRing R]

/-- Chebyshev-type sequence `u_j(lam)` attached to the recursion
`R^2 = lam R - 1`. -/
def u (lam : R) : ℕ → R
  | 0 => 0
  | 1 => 1
  | (n + 2) => lam * u lam (n + 1) - u lam n

/-- `S = [[0,-1],[1,0]]`. -/
def Smat : Matrix (Fin 2) (Fin 2) R := !![0, -1; 1, 0]

/-- `R = [[0,-1],[1,lam]]`. -/
def Rmat (lam : R) : Matrix (Fin 2) (Fin 2) R := !![0, -1; 1, lam]

/-- `M_a := [[u_a, u_{a+1}],[u_{a-1}, u_a]]` (indices `a ≥ 1`; `u_{a-1}` uses
`ℕ`-truncated subtraction, valid since `a ≥ 1`). -/
def Mmat (lam : R) (a : ℕ) : Matrix (Fin 2) (Fin 2) R :=
  !![u lam a, u lam (a + 1); u lam (a - 1), u lam a]

/-- `R^2 = lam • R - 1`, the defining relation of the recursion. -/
theorem Rmat_sq (lam : R) : Rmat lam ^ 2 = lam • Rmat lam - 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Rmat, pow_two, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

/-- `R^a = u_a • R - u_{a-1} • 1` for `a ≥ 1`, by induction on the recursion. -/
theorem Rmat_pow (lam : R) (a : ℕ) (ha : 1 ≤ a) :
    Rmat lam ^ a = u lam a • Rmat lam - u lam (a - 1) • (1 : Matrix (Fin 2) (Fin 2) R) := by
  induction a with
  | zero => omega
  | succ n ih =>
    rcases Nat.eq_or_lt_of_le ha with h | h
    · simp [← h, u]
    · have hn : 1 ≤ n := by omega
      have hrec := ih hn
      obtain ⟨k, rfl⟩ : ∃ k, n = k + 1 := ⟨n - 1, by omega⟩
      rw [pow_succ, hrec, sub_mul, smul_mul_assoc, smul_mul_assoc, one_mul, ← pow_two, Rmat_sq]
      have hu : u lam (k + 1 + 1) = lam * u lam (k + 1) - u lam k := rfl
      simp only [Nat.add_sub_cancel, hu]
      module

/-- `S * R^a = -M_a` for `a ≥ 1`. -/
theorem SR_pow (lam : R) (a : ℕ) (ha : 1 ≤ a) :
    Smat * Rmat lam ^ a = - Mmat lam a := by
  obtain ⟨k, rfl⟩ : ∃ k, a = k + 1 := ⟨a - 1, by omega⟩
  rw [Rmat_pow lam _ ha]
  have hu : u lam (k + 1 + 1) = lam * u lam (k + 1) - u lam k := rfl
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Smat, Rmat, Mmat, Matrix.mul_apply, Fin.sum_univ_succ, hu, Matrix.one_fin_two] <;> ring

/-- `det M_a = 1` for `a ≥ 1`, the Chebyshev identity `u_a^2 - u_{a+1} u_{a-1} = 1`. -/
theorem det_Mmat (lam : R) (a : ℕ) (ha : 1 ≤ a) :
    (Mmat lam a).det = 1 := by
  have h1 : (Smat * Rmat lam ^ a : Matrix (Fin 2) (Fin 2) R).det = 1 := by
    rw [Matrix.det_mul, Matrix.det_pow]
    simp [Smat, Rmat, Matrix.det_fin_two_of]
  rw [SR_pow lam a ha] at h1
  rw [Matrix.det_fin_two] at h1 ⊢
  simp only [Matrix.neg_apply] at h1
  linear_combination h1

/-! ## A2 (§6, "the trace-path expansion is a sum of nonnegative terms"). A
finite product of entrywise-nonnegative `2×2` matrices has trace bounded below
by the sum of the two diagonal-path products, and more generally by any single
cyclic state-path product. -/

/-- The ordered product `A 0 * A 1 * ⋯ * A (n-1)` of a finite family of
matrices. -/
def matProd {n : ℕ} (A : Fin n → Matrix (Fin 2) (Fin 2) ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  (List.ofFn A).prod

theorem matProd_succ {n : ℕ} (A : Fin (n + 1) → Matrix (Fin 2) (Fin 2) ℝ) :
    matProd A = A 0 * matProd (fun i : Fin n => A i.succ) := by
  simp [matProd, List.ofFn_succ]

/-- Entrywise-nonnegative matrices have an entrywise-nonnegative product. -/
theorem matProd_nonneg : ∀ {n : ℕ} (A : Fin n → Matrix (Fin 2) (Fin 2) ℝ),
    (∀ i p q, 0 ≤ A i p q) → ∀ p q, 0 ≤ matProd A p q := by
  intro n
  induction n with
  | zero => intro A _ p q; simp [matProd, Matrix.one_apply]; positivity
  | succ n ih =>
    intro A hA p q
    rw [matProd_succ, Matrix.mul_apply]
    exact Finset.sum_nonneg fun z _ => mul_nonneg (hA 0 _ _) (ih _ (fun i p q => hA _ p q) _ _)

/-- Every state path `s` contributes a single nonnegative term to the entry
`(s 0, s n)` of the product, hence is dominated by it. -/
theorem matProd_ge_path : ∀ {n : ℕ} (A : Fin n → Matrix (Fin 2) (Fin 2) ℝ),
    (∀ i p q, 0 ≤ A i p q) → ∀ s : ℕ → Fin 2,
    (∏ k : Fin n, A k (s (k : ℕ)) (s ((k : ℕ) + 1))) ≤ matProd A (s 0) (s n) := by
  intro n
  induction n with
  | zero => intro A _ s; simp [matProd]
  | succ n ih =>
    intro A hA s
    rw [matProd_succ, Matrix.mul_apply, Fin.prod_univ_succ]
    have key := ih (fun i : Fin n => A i.succ) (fun i p q => hA _ p q) (fun j => s (j + 1))
    simp only [Fin.val_succ] at key ⊢
    calc A 0 (s 0) (s 1) * ∏ i : Fin n, A i.succ (s ((i : ℕ) + 1)) (s ((i : ℕ) + 1 + 1))
        ≤ A 0 (s 0) (s 1) * matProd (fun i : Fin n => A i.succ) (s 1) (s (n + 1)) := by
          refine mul_le_mul_of_nonneg_left ?_ (hA 0 _ _)
          simpa using key
      _ ≤ ∑ z, A 0 (s 0) z * matProd (fun i : Fin n => A i.succ) z (s (n + 1)) := by
          refine Finset.single_le_sum
            (f := fun z => A 0 (s 0) z * matProd (fun i : Fin n => A i.succ) z (s (n + 1)))
            ?_ (Finset.mem_univ (s 1))
          intro z _
          exact mul_nonneg (hA 0 _ _) (matProd_nonneg _ (fun i p q => hA _ p q) _ _)

/-- The trace of a finite product of entrywise-nonnegative `2×2` real matrices
is nonnegative. -/
theorem trace_prod_nonneg {n : ℕ} (A : Fin n → Matrix (Fin 2) (Fin 2) ℝ)
    (hA : ∀ i p q, 0 ≤ A i p q) : 0 ≤ Matrix.trace (matProd A) := by
  rw [Matrix.trace_fin_two]
  exact add_nonneg (matProd_nonneg A hA 0 0) (matProd_nonneg A hA 1 1)

/-- The two constant diagonal paths (`i ≡ 0` and `i ≡ 1`) lower-bound the trace
of a product of entrywise-nonnegative `2×2` matrices. -/
theorem trace_ge_diag {n : ℕ} (A : Fin n → Matrix (Fin 2) (Fin 2) ℝ)
    (hA : ∀ i p q, 0 ≤ A i p q) :
    (∏ i, A i 0 0) + (∏ i, A i 1 1) ≤ Matrix.trace (matProd A) := by
  rw [Matrix.trace_fin_two]
  exact add_le_add (matProd_ge_path A hA (fun _ => 0)) (matProd_ge_path A hA (fun _ => 1))

/-- More generally, every cyclic state-path product lower-bounds the trace of a
product of entrywise-nonnegative `2×2` matrices (`n > 0`; the path is a
function `ZMod n → Fin 2` closing up cyclically). -/
theorem trace_ge_path {n : ℕ} (hn : 0 < n) (A : Fin n → Matrix (Fin 2) (Fin 2) ℝ)
    (hA : ∀ i p q, 0 ≤ A i p q) (i : ZMod n → Fin 2) :
    (∏ k : Fin n, A k (i k) (i (k + 1))) ≤ Matrix.trace (matProd A) := by
  set s : ℕ → Fin 2 := fun j => i (j : ZMod n) with hs
  have key := matProd_ge_path A hA s
  have hsn : s n = s 0 := by simp [hs]
  have heq : (∏ k : Fin n, A k (i k) (i (k + 1)))
      = ∏ k : Fin n, A k (s (k : ℕ)) (s ((k : ℕ) + 1)) := by
    refine Finset.prod_congr rfl fun k _ => ?_
    simp [hs]
  rw [heq, Matrix.trace_fin_two]
  rw [hsn] at key
  have h00 := matProd_nonneg A hA 0 0
  have h11 := matProd_nonneg A hA 1 1
  have h2 : s 0 = 0 ∨ s 0 = 1 := by
    rcases h : s 0 with ⟨v, hv⟩
    interval_cases v
    · exact Or.inl rfl
    · exact Or.inr rfl
  rcases h2 with h2 | h2 <;> rw [h2] at key <;> linarith

/-! ### Two further product facts used by A3 -/

/-- The determinant is multiplicative along the ordered product. -/
theorem matProd_det : ∀ {n : ℕ} (A : Fin n → Matrix (Fin 2) (Fin 2) ℝ),
    (matProd A).det = ∏ i, (A i).det := by
  intro n
  induction n with
  | zero => intro A; simp [matProd]
  | succ n ih =>
    intro A
    rw [matProd_succ, Matrix.det_mul, ih, Fin.prod_univ_succ]

/-- An ordered product of upper unitriangular `2×2` matrices is upper
unitriangular. -/
theorem matProd_upper : ∀ {n : ℕ} (A : Fin n → Matrix (Fin 2) (Fin 2) ℝ),
    (∀ i, A i 1 0 = 0 ∧ A i 0 0 = 1 ∧ A i 1 1 = 1) →
    matProd A 0 0 = 1 ∧ matProd A 1 1 = 1 ∧ matProd A 1 0 = 0 := by
  intro n
  induction n with
  | zero => intro A _; refine ⟨?_, ?_, ?_⟩ <;> simp [matProd]
  | succ n ih =>
    intro A hA
    obtain ⟨e00, e11, e10⟩ := ih (fun i : Fin n => A i.succ) (fun i => hA _)
    obtain ⟨f10, f00, f11⟩ := hA 0
    refine ⟨?_, ?_, ?_⟩ <;>
      rw [matProd_succ, Matrix.mul_apply, Fin.sum_univ_two] <;>
      simp [e00, e11, e10, f10, f00, f11]

/-- An ordered product of lower unitriangular `2×2` matrices is lower
unitriangular. -/
theorem matProd_lower : ∀ {n : ℕ} (A : Fin n → Matrix (Fin 2) (Fin 2) ℝ),
    (∀ i, A i 0 1 = 0 ∧ A i 0 0 = 1 ∧ A i 1 1 = 1) →
    matProd A 0 0 = 1 ∧ matProd A 1 1 = 1 ∧ matProd A 0 1 = 0 := by
  intro n
  induction n with
  | zero => intro A _; refine ⟨?_, ?_, ?_⟩ <;> simp [matProd]
  | succ n ih =>
    intro A hA
    obtain ⟨e00, e11, e01⟩ := ih (fun i : Fin n => A i.succ) (fun i => hA _)
    obtain ⟨f01, f00, f11⟩ := hA 0
    refine ⟨?_, ?_, ?_⟩ <;>
      rw [matProd_succ, Matrix.mul_apply, Fin.sum_univ_two] <;>
      simp [e00, e11, e01, f01, f00, f11]

/-! ## A3 (§6, "the systole theorem, given A1 + A2"). Stated over a FIXED
finite level `q` and a fixed finite word length `m`, so the statement is a
concrete finite claim about real numbers (`lam_q := 2 * Real.cos (π / q)`), not
a scheme quantified over all `q`. -/

/-- `lam_q := 2 cos(pi/q)`. -/
noncomputable def lamQ (q : ℕ) : ℝ := 2 * Real.cos (Real.pi / q)

/-- `sin a ≤ sin x` whenever `0 ≤ a ≤ x ≤ π - a`. -/
theorem sin_le_sin_between {a x : ℝ} (ha : 0 ≤ a) (hax : a ≤ x) (hx : x ≤ Real.pi - a) :
    Real.sin a ≤ Real.sin x := by
  have main : ∀ b y : ℝ, 0 ≤ b → b ≤ y → y ≤ Real.pi / 2 → Real.sin b ≤ Real.sin y := by
    intro b y hb hby hy
    rcases eq_or_lt_of_le hby with h | h
    · rw [h]
    · exact le_of_lt (Real.sin_lt_sin_of_lt_of_le_pi_div_two (by linarith [Real.pi_pos]) hy h)
  rcases le_total x (Real.pi / 2) with h | h
  · exact main a x ha hax h
  · rw [← Real.sin_pi_sub x]
    exact main a (Real.pi - x) ha (by linarith) (by linarith)

/-- `u_j(2 cos θ) sin θ = sin (j θ)`: the closed form of the Chebyshev
recursion. -/
theorem u_two_cos (θ : ℝ) (j : ℕ) :
    u (2 * Real.cos θ) j * Real.sin θ = Real.sin (j * θ) := by
  induction j using Nat.twoStepInduction with
  | zero => simp [u]
  | one => simp [u]
  | more n ih1 ih2 =>
    have hu : u (2 * Real.cos θ) (n + 2)
        = 2 * Real.cos θ * u (2 * Real.cos θ) (n + 1) - u (2 * Real.cos θ) n := rfl
    have key : Real.sin (((n : ℝ) + 2) * θ)
        = 2 * Real.cos θ * Real.sin (((n : ℝ) + 1) * θ) - Real.sin ((n : ℝ) * θ) := by
      rw [show ((n : ℝ) + 2) * θ = ((n : ℝ) + 1) * θ + θ by ring,
        show (n : ℝ) * θ = ((n : ℝ) + 1) * θ - θ by ring, Real.sin_add, Real.sin_sub]
      ring
    rw [hu]
    push_cast at key ih1 ih2 ⊢
    rw [key]
    linear_combination (2 * Real.cos θ) * ih2 - ih1

theorem sin_pi_div_q_pos {q : ℕ} (hq : 4 ≤ q) : 0 < Real.sin (Real.pi / q) := by
  have hq0 : (4 : ℝ) ≤ (q : ℝ) := by exact_mod_cast hq
  have h1 : 0 < Real.pi / q := div_pos Real.pi_pos (by linarith)
  have h2 : Real.pi / q < Real.pi := by
    rw [div_lt_iff₀ (by linarith)]
    nlinarith [Real.pi_pos]
  exact Real.sin_pos_of_pos_of_lt_pi h1 h2

theorem lamQ_pos {q : ℕ} (hq : 4 ≤ q) : 0 < lamQ q := by
  have hq0 : (4 : ℝ) ≤ (q : ℝ) := by exact_mod_cast hq
  have hc : 0 < Real.cos (Real.pi / q) := by
    apply Real.cos_pos_of_mem_Ioo
    constructor
    · have : 0 < Real.pi / q := div_pos Real.pi_pos (by linarith)
      linarith [Real.pi_pos]
    · rw [div_lt_div_iff₀ (by linarith) (by norm_num)]
      nlinarith [Real.pi_pos]
  rw [lamQ]; linarith

/-- Monotonicity of `j ↦ u_j(lam_q)` in the range where `sin` is increasing:
`u_c ≤ u_j` whenever `c ≤ j` and `j + c ≤ q`. -/
theorem uQ_mono {q : ℕ} (hq : 4 ≤ q) (c j : ℕ) (hcj : c ≤ j) (hjc : j + c ≤ q) :
    u (lamQ q) c ≤ u (lamQ q) j := by
  have hq0 : (4 : ℝ) ≤ (q : ℝ) := by exact_mod_cast hq
  have hs := sin_pi_div_q_pos hq
  have h1 := u_two_cos (Real.pi / q) c
  have h2 := u_two_cos (Real.pi / q) j
  have hθ : 0 < Real.pi / q := div_pos Real.pi_pos (by linarith)
  have hb : Real.sin (c * (Real.pi / q)) ≤ Real.sin (j * (Real.pi / q)) := by
    apply sin_le_sin_between
    · positivity
    · have : (c : ℝ) ≤ j := by exact_mod_cast hcj
      nlinarith
    · have hjc' : (j : ℝ) + c ≤ q := by exact_mod_cast hjc
      have : (j : ℝ) * (Real.pi / q) + c * (Real.pi / q) ≤ Real.pi := by
        rw [← add_mul]
        calc ((j : ℝ) + c) * (Real.pi / q) ≤ (q : ℝ) * (Real.pi / q) :=
              mul_le_mul_of_nonneg_right hjc' (le_of_lt hθ)
          _ = Real.pi := by field_simp
      linarith
  rw [lamQ]
  nlinarith [h1, h2, hb, hs]

theorem uQ_one {q : ℕ} : u (lamQ q) 1 = 1 := rfl

theorem uQ_two {q : ℕ} : u (lamQ q) 2 = lamQ q := by simp [u]

theorem uQ_qsub1 {q : ℕ} (hq : 4 ≤ q) : u (lamQ q) (q - 1) = 1 := by
  have hs := sin_pi_div_q_pos hq
  have h := u_two_cos (Real.pi / q) (q - 1)
  have hq0 : (4 : ℝ) ≤ (q : ℝ) := by exact_mod_cast hq
  have hcast : ((q - 1 : ℕ) : ℝ) = (q : ℝ) - 1 := by
    have h1 : (1 : ℕ) ≤ q := by omega
    push_cast [h1]; ring
  rw [hcast] at h
  have he : ((q : ℝ) - 1) * (Real.pi / q) = Real.pi - Real.pi / q := by field_simp
  rw [he, Real.sin_pi_sub] at h
  rw [lamQ]
  nlinarith [h, hs]

theorem uQ_q {q : ℕ} (hq : 4 ≤ q) : u (lamQ q) q = 0 := by
  have hs := sin_pi_div_q_pos hq
  have h := u_two_cos (Real.pi / q) q
  have hq0 : (4 : ℝ) ≤ (q : ℝ) := by exact_mod_cast hq
  have he : (q : ℝ) * (Real.pi / q) = Real.pi := by field_simp
  rw [he, Real.sin_pi] at h
  rw [lamQ]
  nlinarith [h, hs]

theorem uQ_qsub2 {q : ℕ} (hq : 4 ≤ q) : u (lamQ q) (q - 2) = lamQ q := by
  have hs := sin_pi_div_q_pos hq
  have h := u_two_cos (Real.pi / q) (q - 2)
  have h2 := u_two_cos (Real.pi / q) 2
  have hq0 : (4 : ℝ) ≤ (q : ℝ) := by exact_mod_cast hq
  have hcast : ((q - 2 : ℕ) : ℝ) = (q : ℝ) - 2 := by
    have h1 : (2 : ℕ) ≤ q := by omega
    push_cast [h1]; ring
  rw [hcast] at h
  have he : ((q : ℝ) - 2) * (Real.pi / q) = Real.pi - 2 * (Real.pi / q) := by field_simp
  rw [he, Real.sin_pi_sub] at h
  have hu2 : u (2 * Real.cos (Real.pi / q)) 2 = 2 * Real.cos (Real.pi / q) := by simp [u]
  rw [hu2] at h2
  push_cast at h2
  rw [lamQ]
  nlinarith [h, h2, hs]

/-- For a fixed level `q ≥ 4` and a fixed word length `m ≥ 1`, every hyperbolic
cyclically reduced word `S R^{a_1} ... S R^{a_m}` with letters `a_i ∈ [1, q-1]`
has `|tr w| ≥ 2 * lam_q`. The word is represented by its letters `a : Fin m →
ℕ` and its trace by the real number `t`, related by the (already-established,
A1-level) fact that `t = tr(∏ Mmat (lamQ q) (a i))` up to sign — taken here as
a hypothesis `htr` so the statement isolates the systole inequality itself. -/
theorem systole_trace_bound (q m : ℕ) (hq : 4 ≤ q) (hm : 1 ≤ m)
    (a : Fin m → ℕ) (ha : ∀ i, 1 ≤ a i ∧ a i ≤ q - 1)
    (t : ℝ) (htr : t = Matrix.trace (matProd (fun i : Fin m => Mmat (lamQ q) (a i))))
    (hhyp : 2 < |t|) :
    2 * lamQ q ≤ |t| := by
  set lam := lamQ q with hlamdef
  set M : Fin m → Matrix (Fin 2) (Fin 2) ℝ := fun i => Mmat lam (a i) with hM
  have hlampos : 0 < lam := lamQ_pos hq
  -- entries of each letter matrix
  have hM00 : ∀ i, M i 0 0 = u lam (a i) := by intro i; simp [hM, Mmat]
  have hM11 : ∀ i, M i 1 1 = u lam (a i) := by intro i; simp [hM, Mmat]
  have hM01 : ∀ i, M i 0 1 = u lam (a i + 1) := by intro i; simp [hM, Mmat]
  have hM10 : ∀ i, M i 1 0 = u lam (a i - 1) := by intro i; simp [hM, Mmat]
  -- all entries are nonnegative
  have hu0 : u lam 0 = 0 := rfl
  have hnn : ∀ j : ℕ, j ≤ q → 0 ≤ u lam j := by
    intro j hj
    have := uQ_mono hq 0 j (Nat.zero_le _) (by omega)
    rwa [hu0] at this
  have hfin2 : ∀ p : Fin 2, p = 0 ∨ p = 1 := by decide
  have hA : ∀ i (p r : Fin 2), 0 ≤ M i p r := by
    intro i p r
    obtain ⟨ha1, ha2⟩ := ha i
    rcases hfin2 p with hp | hp <;> rcases hfin2 r with hr | hr <;> subst hp <;> subst hr
    · rw [hM00]; exact hnn _ (by omega)
    · rw [hM01]; exact hnn _ (by omega)
    · rw [hM10]; exact hnn _ (by omega)
    · rw [hM11]; exact hnn _ (by omega)
  -- each `u_{a i}` is at least 1
  have hu1 : ∀ i, 1 ≤ u lam (a i) := by
    intro i
    obtain ⟨ha1, ha2⟩ := ha i
    have := uQ_mono hq 1 (a i) ha1 (by omega)
    rwa [uQ_one] at this
  -- the two diagonal paths
  have hdiag0 : (∏ i, u lam (a i)) ≤ matProd M 0 0 := by
    have := matProd_ge_path M hA (fun _ => 0)
    simpa [hM00] using this
  have hdiag1 : (∏ i, u lam (a i)) ≤ matProd M 1 1 := by
    have := matProd_ge_path M hA (fun _ => 1)
    simpa [hM11] using this
  have hprod1 : (1 : ℝ) ≤ ∏ i, u lam (a i) := Finset.one_le_prod _ hu1
  have h00 : (1 : ℝ) ≤ matProd M 0 0 := le_trans hprod1 hdiag0
  have h11 : (1 : ℝ) ≤ matProd M 1 1 := le_trans hprod1 hdiag1
  have htsum : t = matProd M 0 0 + matProd M 1 1 := by rw [htr, Matrix.trace_fin_two]
  have htpos : 0 ≤ t := by rw [htsum]; linarith
  rw [abs_of_nonneg htpos] at hhyp ⊢
  by_cases hcase : ∃ i, 2 ≤ a i ∧ a i + 2 ≤ q
  · -- Case A: some letter lies in the "interior" `[2, q-2]`, so `u_{a i} ≥ lam`.
    obtain ⟨i0, hi1, hi2⟩ := hcase
    have hlam_le : lam ≤ u lam (a i0) := by
      have := uQ_mono hq 2 (a i0) hi1 (by omega)
      rwa [uQ_two] at this
    have hrest : (1 : ℝ) ≤ ∏ i ∈ Finset.univ.erase i0, u lam (a i) :=
      Finset.one_le_prod _ hu1
    have hbig : lam ≤ ∏ i, u lam (a i) := by
      rw [← Finset.mul_prod_erase _ _ (Finset.mem_univ i0)]
      nlinarith
    linarith [le_trans hbig hdiag0, le_trans hbig hdiag1]
  · -- Case B: every letter is `1` or `q-1`.
    push_neg at hcase
    have hB : ∀ i, a i = 1 ∨ a i = q - 1 := by
      intro i
      obtain ⟨ha1, ha2⟩ := ha i
      rcases Nat.lt_or_ge (a i) 2 with h | h
      · left; omega
      · right; have := hcase i h; omega
    have huB : ∀ i, u lam (a i) = 1 := by
      intro i
      rcases hB i with h | h
      · rw [h, uQ_one]
      · rw [h, uQ_qsub1 hq]
    by_cases hall1 : ∀ i, a i = 1
    · -- all letters `1`: the product is upper unitriangular, so the trace is 2.
      exfalso
      have hup : ∀ i, M i 1 0 = 0 ∧ M i 0 0 = 1 ∧ M i 1 1 = 1 := by
        intro i
        refine ⟨?_, ?_, ?_⟩
        · rw [hM10, hall1 i]; exact hu0
        · rw [hM00, huB i]
        · rw [hM11, huB i]
      obtain ⟨e00, e11, _⟩ := matProd_upper M hup
      rw [htsum, e00, e11] at hhyp
      linarith
    · by_cases hallq : ∀ i, a i = q - 1
      · -- all letters `q-1`: the product is lower unitriangular, so the trace is 2.
        exfalso
        have hlow : ∀ i, M i 0 1 = 0 ∧ M i 0 0 = 1 ∧ M i 1 1 = 1 := by
          intro i
          refine ⟨?_, ?_, ?_⟩
          · rw [hM01, hallq i]
            have : q - 1 + 1 = q := by omega
            rw [this, uQ_q hq]
          · rw [hM00, huB i]
          · rw [hM11, huB i]
        obtain ⟨e00, e11, _⟩ := matProd_lower M hlow
        rw [htsum, e00, e11] at hhyp
        linarith
      · -- mixed letters: both off-diagonal entries of the product are ≥ lam.
        push_neg at hall1 hallq
        obtain ⟨i1, hi1⟩ := hall1
        obtain ⟨i2, hi2⟩ := hallq
        have ha1 : a i1 = q - 1 := (hB i1).resolve_left hi1
        have ha2 : a i2 = 1 := (hB i2).resolve_right hi2
        -- path realising `M 0 1 ≥ lam`
        have hoff01 : lam ≤ matProd M 0 1 := by
          set s : ℕ → Fin 2 := fun k => if k ≤ (i2 : ℕ) then (0 : Fin 2) else 1 with hs
          have hs0 : s 0 = 0 := by simp [hs]
          have hsm : s m = 1 := by
            have : ¬ (m ≤ (i2 : ℕ)) := by have := i2.isLt; omega
            simp [hs, this]
          have hpath := matProd_ge_path M hA s
          rw [hs0, hsm] at hpath
          refine le_trans (le_of_eq ?_) hpath
          rw [Finset.prod_eq_single i2]
          · have hkey : s (i2 : ℕ) = 0 := by simp [hs]
            have hkey2 : s ((i2 : ℕ) + 1) = 1 := by
              have : ¬ ((i2 : ℕ) + 1 ≤ (i2 : ℕ)) := by omega
              simp [hs, this]
            rw [hkey, hkey2, hM01, ha2]
            exact uQ_two.symm
          · intro b _ hb
            rcases Nat.lt_or_ge (b : ℕ) (i2 : ℕ) with h | h
            · have h1 : s (b : ℕ) = 0 := by simp [hs]; omega
              have h2 : s ((b : ℕ) + 1) = 0 := by simp [hs]; omega
              rw [h1, h2, hM00, huB b]
            · have hne : (i2 : ℕ) < (b : ℕ) := by
                rcases Nat.lt_or_ge (i2 : ℕ) (b : ℕ) with h' | h'
                · exact h'
                · exact absurd (Fin.ext (le_antisymm h' h)) hb
              have h1 : s (b : ℕ) = 1 := by simp [hs]; omega
              have h2 : s ((b : ℕ) + 1) = 1 := by simp [hs]; omega
              rw [h1, h2, hM11, huB b]
          · intro h; exact absurd (Finset.mem_univ i2) h
        -- path realising `M 1 0 ≥ lam`
        have hoff10 : lam ≤ matProd M 1 0 := by
          set s : ℕ → Fin 2 := fun k => if k ≤ (i1 : ℕ) then (1 : Fin 2) else 0 with hs
          have hs0 : s 0 = 1 := by simp [hs]
          have hsm : s m = 0 := by
            have : ¬ (m ≤ (i1 : ℕ)) := by have := i1.isLt; omega
            simp [hs, this]
          have hpath := matProd_ge_path M hA s
          rw [hs0, hsm] at hpath
          refine le_trans (le_of_eq ?_) hpath
          rw [Finset.prod_eq_single i1]
          · have hkey : s (i1 : ℕ) = 1 := by simp [hs]
            have hkey2 : s ((i1 : ℕ) + 1) = 0 := by
              have : ¬ ((i1 : ℕ) + 1 ≤ (i1 : ℕ)) := by omega
              simp [hs, this]
            rw [hkey, hkey2, hM10, ha1]
            have hqq : q - 1 - 1 = q - 2 := by omega
            rw [hqq, uQ_qsub2 hq]
          · intro b _ hb
            rcases Nat.lt_or_ge (b : ℕ) (i1 : ℕ) with h | h
            · have h1 : s (b : ℕ) = 1 := by simp [hs]; omega
              have h2 : s ((b : ℕ) + 1) = 1 := by simp [hs]; omega
              rw [h1, h2, hM11, huB b]
            · have hne : (i1 : ℕ) < (b : ℕ) := by
                rcases Nat.lt_or_ge (i1 : ℕ) (b : ℕ) with h' | h'
                · exact h'
                · exact absurd (Fin.ext (le_antisymm h' h)) hb
              have h1 : s (b : ℕ) = 0 := by simp [hs]; omega
              have h2 : s ((b : ℕ) + 1) = 0 := by simp [hs]; omega
              rw [h1, h2, hM00, huB b]
          · intro h; exact absurd (Finset.mem_univ i1) h
        -- determinant 1 turns the off-diagonal bound into a trace bound
        have hdet : matProd M 0 0 * matProd M 1 1 - matProd M 0 1 * matProd M 1 0 = 1 := by
          have h1 : (matProd M).det = ∏ i, (M i).det := matProd_det M
          have h2 : ∀ i, (M i).det = 1 := by
            intro i
            exact det_Mmat lam (a i) (ha i).1
          rw [Matrix.det_fin_two] at h1
          simp only [h2, Finset.prod_const_one] at h1
          exact h1
        rw [htsum]
        have hps : 1 + lam * lam ≤ matProd M 0 0 * matProd M 1 1 := by
          nlinarith [hoff01, hoff10, hdet, hlampos]
        nlinarith [sq_nonneg (matProd M 0 0 - matProd M 1 1), hps, hlampos, h00, h11]

/-! ## A6 (§6, "the counterexample, worth banking as a decide-style fact"). The
literal statement of `Conjecture U1-2` — `|tr S R^5| = 2|u_5(lam)|` nondecreasing
on `(1,2]` — is false: `u_5(lam) = lam^4 - 3 lam^2 + 1` is non-monotone, witnessed
by the explicit triple `lam = 1, 1.2434, sqrt 2` from `LAW_U2B_CLOSURE.md` §3.2. -/

/-- `u_5(lam) = lam^4 - 3 lam^2 + 1` fails to be monotone on `(1, 2]`: it rises
from `lam = 1` to `lam = 1.2434` and falls back by `lam = sqrt 2`. -/
theorem u5_not_monotone :
    ¬ MonotoneOn (fun lam : ℝ => 2 * (lam ^ 4 - 3 * lam ^ 2 + 1)) (Set.Ioc (1 : ℝ) 2) := by
  intro h
  have h1 : (1.1 : ℝ) ∈ Set.Ioc (1 : ℝ) 2 := by norm_num
  have h2 : (1.2434 : ℝ) ∈ Set.Ioc (1 : ℝ) 2 := by norm_num
  have := h h1 h2 (by norm_num)
  norm_num at this

/-- The explicit witness inequality triple: at `lam = 1`, `|2 u_5| = 2`; at
`lam = 1.2434`, `|2 u_5| > 2.49`; at `lam = sqrt 2`, `|2 u_5| = 2`. This pins
down the rise-then-fall shape used by `u5_not_monotone`. -/
theorem u5_witness_triple :
    |2 * ((1 : ℝ) ^ 4 - 3 * 1 ^ 2 + 1)| = 2 ∧
    2.49 < |2 * ((1.2434 : ℝ) ^ 4 - 3 * 1.2434 ^ 2 + 1)| ∧
    |2 * ((Real.sqrt 2) ^ 4 - 3 * (Real.sqrt 2) ^ 2 + 1)| = 2 := by
  have hs : (Real.sqrt 2) ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  refine ⟨by norm_num, by rw [abs_of_nonpos (by norm_num)]; norm_num, ?_⟩
  have h4 : (Real.sqrt 2) ^ 4 = 4 := by
    rw [show (Real.sqrt 2) ^ 4 = ((Real.sqrt 2) ^ 2) ^ 2 by ring, hs]; norm_num
  rw [h4, hs]
  norm_num

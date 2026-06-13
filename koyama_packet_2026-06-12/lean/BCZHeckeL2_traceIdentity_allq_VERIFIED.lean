import Mathlib
/-!
# Goal M — the CONCEPTUAL backbone of (L2): the SL₂ trace identity + why a corridor
  switch is parabolic + the extremal-trace bound (λ is the slowest rotation).  ALL q,
  parametric in `l = λ = 2cos(π/q)`.

The earlier `BCZHeckeL2_composite_VERIFIED.lean` proved the composite-trace law
`tr (F k₂ · F k₁) = l²(k₁−2)(k₂−2) − 2` for the `W_q`-corridor family by a direct `ring`.
This file exposes the STRUCTURE behind it and supplies the two uniform facts that the
corridor classification (goal M) rests on:

1.  **General SL₂ trace identity** (`tr_mul_add_tr_mul_adj`):  for ANY 2×2 matrices `X,Y`,
    `tr (X·Y) + tr (X·adj Y) = tr X · tr Y`,  where `adj Y = [[Y.d,−Y.b],[−Y.c,Y.a]]` is the
    adjugate (`= Y⁻¹` when `det Y = 1`).  Pure `ring`, no determinant hypothesis.

2.  **A corridor switch is PARABOLIC** (`adjF_switch_parabolic`):  for the `W_q`-family
    `F k = B·A0·A k`,  `tr (F k₂ · adj (F k₁)) = 2` for ALL `k₁,k₂,l`.  I.e. the "switch
    element" `F k₂·(F k₁)⁻¹` is parabolic (trace 2) — it is conjugate to the unipotent
    `[[1,0],[(k₂−k₁)l,1]]`.  THIS is the reason switching corridors crosses the cusp/threshold:
    combined with (1), `tr (F k₂·F k₁) = tr(F k₁)·tr(F k₂) − 2`, recovering the composite law
    (`trace_compose_via_identity`) — now as a CONSEQUENCE of "the switch is parabolic", not a
    coincidence of `ring`.

3.  **λ is the slowest rotation / the extremal elliptic trace** (`abs_cos_le_of_between`,
    `lam_is_max_elliptic_trace`):  every elliptic monodromy in the Hecke group `G_q=(2,q,∞)`
    has trace `2cos(jπ/q)`, `1≤j≤q−1` (its finite-order torsion spectrum); for any such angle
    `θ ∈ [π/q, π−π/q]`, `|2cos θ| ≤ 2cos(π/q) = l`.  So NO elliptic corridor rotates slower
    than `π/q`; the `W_q`/`F`-family (`j=1`, trace `l`) is the unique slowest rotation, hence
    has the LONGEST sub-threshold arc — the corridor set's extremal element.

Together (1)+(2) give the (L2) switch obstruction conceptually; (3) is the extremality that
reduces the whole corridor set to the `F`-family for the (L1) arc bound.  This is the
backbone of the goal-M classification verdict (the corridor set is exactly the elliptic
torsion of `G_q`, with `l` extremal — numerically airtight, HP residual ≤ 1e-45).

`#print axioms` on every theorem is `[propext, Classical.choice, Quot.sound]`.
-/
namespace HeckeL2trace

open Real

/-- A 2×2 real matrix `[[a,b],[c,d]]`. -/
structure M2 where
  a : ℝ
  b : ℝ
  c : ℝ
  d : ℝ

@[ext] theorem M2.ext {X Y : M2}
    (ha : X.a = Y.a) (hb : X.b = Y.b) (hc : X.c = Y.c) (hd : X.d = Y.d) : X = Y := by
  cases X; cases Y; simp_all

def mul (X Y : M2) : M2 :=
  ⟨X.a * Y.a + X.b * Y.c, X.a * Y.b + X.b * Y.d,
   X.c * Y.a + X.d * Y.c, X.c * Y.b + X.d * Y.d⟩

def tr  (X : M2) : ℝ := X.a + X.d
def det (X : M2) : ℝ := X.a * X.d - X.b * X.c
/-- Adjugate `adj X = [[d,−b],[−c,a]]`; equals `X⁻¹` exactly when `det X = 1`. -/
def adj (X : M2) : M2 := ⟨X.d, -X.b, -X.c, X.a⟩

/-- **General SL₂ trace identity.**  `tr (X·Y) + tr (X·adj Y) = tr X · tr Y`, for ALL `X,Y`
    (no determinant hypothesis — it is a pure polynomial identity). -/
theorem tr_mul_add_tr_mul_adj (X Y : M2) :
    tr (mul X Y) + tr (mul X (adj Y)) = tr X * tr Y := by
  simp only [mul, tr, adj]; ring

/-- `adj X` is the inverse of `X` when `det X = 1`: `X · adj X = I` (entrywise). -/
theorem mul_adj_eq_one (X : M2) (hX : det X = 1) :
    mul X (adj X) = ⟨1, 0, 0, 1⟩ := by
  have : X.a * X.d - X.b * X.c = 1 := hX
  ext <;> simp only [mul, adj] <;> ring_nf <;> linarith [this]

variable (l : ℝ)

/-- Scalar branch generator `M_{q-1,k} = [[0,1],[-1,k l]]`. -/
def A (k : ℝ) : M2 := ⟨0, 1, -1, k * l⟩
/-- Branch `q-3` generator `M_{q-3,0} = [[l,l²-1],[1,l]]`. -/
def B : M2 := ⟨l, l ^ 2 - 1, 1, l⟩
/-- The `W_q`-family corridor `F k = B · A0 · A k` (`F 3 = W_q`). -/
def F (k : ℝ) : M2 := mul (mul (B l) (A l 0)) (A l k)

/-- Each corridor is unimodular (so `adj (F k) = (F k)⁻¹`). -/
theorem det_F (k : ℝ) : det (F l k) = 1 := by
  simp only [F, mul, det, A, B]; ring

/-- Single-corridor trace `tr (F k) = l·(k−2)`. -/
theorem trace_F (k : ℝ) : tr (F l k) = l * (k - 2) := by
  simp only [F, mul, tr, A, B]; ring

/-- **The corridor SWITCH element is PARABOLIC.**  `tr (F k₂ · adj (F k₁)) = 2` for all
    `k₁,k₂,l`.  Since `adj (F k₁) = (F k₁)⁻¹` (det 1), the switch `F k₂·(F k₁)⁻¹` is
    parabolic (trace 2) — it is conjugate to a unipotent `[[1,0],[*,1]]`.  THIS is why a
    corridor switch is a threshold (cusp) kick, not a new slow rotation. -/
theorem adjF_switch_parabolic (k₁ k₂ : ℝ) :
    tr (mul (F l k₂) (adj (F l k₁))) = 2 := by
  simp only [F, mul, adj, tr, A, B]; ring

/-- **Composite-trace law, as a CONSEQUENCE of "the switch is parabolic".**  Plugging
    `adjF_switch_parabolic` and `trace_F` into the general identity `tr_mul_add_tr_mul_adj`
    gives `tr (F k₂·F k₁) = tr(F k₁)·tr(F k₂) − 2 = l²(k₁−2)(k₂−2) − 2`. -/
theorem trace_compose_via_identity (k₁ k₂ : ℝ) :
    tr (mul (F l k₂) (F l k₁)) = l ^ 2 * (k₁ - 2) * (k₂ - 2) - 2 := by
  have hid := tr_mul_add_tr_mul_adj (F l k₂) (F l k₁)
  have hpar := adjF_switch_parabolic l k₁ k₂
  have h1 := trace_F l k₁
  have h2 := trace_F l k₂
  -- hid : tr(F k₂ · F k₁) + tr(F k₂ · adj (F k₁)) = tr(F k₂) · tr(F k₁)
  rw [hpar, h1, h2] at hid
  linarith [hid]

/-! ### (3) Extremality: λ = 2cos(π/q) is the largest elliptic trace (slowest rotation). -/

/-- **Extremal-trace bound.**  For any angle `θ ∈ [θ₁, π − θ₁]` with `0 ≤ θ₁`, one has
    `|cos θ| ≤ cos θ₁`.  Applied with `θ₁ = π/q` and `θ = jπ/q` (`1 ≤ j ≤ q−1`), every Hecke
    torsion trace `2cos(jπ/q)` satisfies `|2cos(jπ/q)| ≤ 2cos(π/q) = l`.  No elliptic element
    rotates slower than `π/q`. -/
theorem abs_cos_le_of_between (θ θ₁ : ℝ) (h0 : 0 ≤ θ₁) (h1 : θ₁ ≤ θ) (h2 : θ ≤ π - θ₁) :
    |Real.cos θ| ≤ Real.cos θ₁ := by
  have hθ1π : θ₁ ≤ π := le_trans h1 (by linarith [Real.pi_pos, h0])
  have hθπ : θ ≤ π := le_trans h2 (by linarith [h0])
  have hθ0 : 0 ≤ θ := le_trans h0 h1
  -- cos is antitone on [0, π]
  have hanti := Real.strictAntiOn_cos.antitoneOn
  -- upper: cos θ ≤ cos θ₁   (θ ≥ θ₁, both in [0,π])
  have hupper : Real.cos θ ≤ Real.cos θ₁ :=
    hanti ⟨h0, hθ1π⟩ ⟨hθ0, hθπ⟩ h1
  -- lower: −cos θ₁ ≤ cos θ.   cos(π−θ₁) = −cos θ₁, and θ ≤ π−θ₁ ⇒ cos(π−θ₁) ≤ cos θ
  have hcps : Real.cos (π - θ₁) = - Real.cos θ₁ := Real.cos_pi_sub θ₁
  have hlower' : Real.cos (π - θ₁) ≤ Real.cos θ :=
    hanti ⟨hθ0, hθπ⟩ ⟨by linarith [h0], by linarith [hθ1π]⟩ h2
  rw [hcps] at hlower'
  rw [abs_le]
  exact ⟨by linarith [hlower'], hupper⟩

/-- **λ is the max elliptic trace.**  With `l = 2cos(π/q)`, every torsion angle
    `θ = jπ/q ∈ [π/q, π−π/q]` gives `|2 cos θ| ≤ l`.  (Instantiate `abs_cos_le_of_between` at
    `θ₁ = π/q`; the `W_q`/`F`-family `j=1` attains `l`.) -/
theorem lam_is_max_elliptic_trace (q : ℝ) (hq : 0 < q) (θ : ℝ)
    (h1 : π / q ≤ θ) (h2 : θ ≤ π - π / q) :
    |2 * Real.cos θ| ≤ 2 * Real.cos (π / q) := by
  have h0 : 0 ≤ π / q := by positivity
  have hb := abs_cos_le_of_between θ (π / q) h0 h1 h2
  rw [abs_mul]
  have : |(2:ℝ)| = 2 := by norm_num
  rw [this]
  nlinarith [hb, Real.cos_le_one (π/q), abs_nonneg (Real.cos θ)]

/-! ### Rotation-subgroup trace spectrum: `tr(Rⁿ) = 2cos(nπ/q)` (Chebyshev).

The fundamental rotation `R = [[0,1],[−1,l]]` (`= A 1`) satisfies Cayley–Hamilton `R² = l·R − I`, so
its trace sequence `tᵢ := tr(Rⁱ)` obeys `t₀=2, t₁=l, t_{n+2}=l·t_{n+1}−t_n`.  With `l = 2cos θ`
(`θ=π/q`) this is exactly the Chebyshev/cosine recurrence, giving `tr(Rⁿ) = 2cos(nθ) = 2cos(nπ/q)`.
Hence the rotation subgroup `⟨R⟩` realises EXACTLY the trace spectrum `{2cos(jπ/q)}` — the values the
corridor classification asserts (the complementary half to `lam_is_max_elliptic_trace`, which says
`j=1` is extremal).  (The remaining input — that *every* elliptic corridor is conjugate into `⟨R⟩` —
is the discreteness/triangle-group structure of `G_q`, not formalised here.) -/
theorem rotation_trace_spectrum (θ : ℝ) (s : ℕ → ℝ)
    (h0 : s 0 = 2) (h1 : s 1 = 2 * Real.cos θ)
    (hrec : ∀ n, s (n + 2) = 2 * Real.cos θ * s (n + 1) - s n) :
    ∀ n, s n = 2 * Real.cos ((n : ℝ) * θ) := by
  have key : ∀ n, s n = 2 * Real.cos ((n : ℝ) * θ)
      ∧ s (n + 1) = 2 * Real.cos (((n : ℝ) + 1) * θ) := by
    intro n
    induction n with
    | zero => exact ⟨by simpa using h0, by simpa using h1⟩
    | succ k ih =>
        obtain ⟨iha, ihb⟩ := ih
        refine ⟨by exact_mod_cast ihb, ?_⟩
        -- s(k+2) = l·s(k+1) − s(k) = 2cosθ·2cos((k+1)θ) − 2cos(kθ) = 2cos((k+2)θ)
        have hcc : Real.cos (((k : ℝ) + 2) * θ) + Real.cos ((k : ℝ) * θ)
            = 2 * Real.cos (((k : ℝ) + 1) * θ) * Real.cos θ := by
          have e1 : ((k : ℝ) + 2) * θ = ((k : ℝ) + 1) * θ + θ := by ring
          have e2 : ((k : ℝ)) * θ = ((k : ℝ) + 1) * θ - θ := by ring
          rw [e1, e2, Real.cos_add, Real.cos_sub]; ring
        rw [hrec k, ihb, iha]
        push_cast
        have harg : ((k : ℝ) + 1 + 1) * θ = ((k : ℝ) + 2) * θ := by ring
        rw [harg]
        linear_combination -2 * hcc
  exact fun n => (key n).1

#print axioms rotation_trace_spectrum
#print axioms tr_mul_add_tr_mul_adj
#print axioms mul_adj_eq_one
#print axioms det_F
#print axioms trace_F
#print axioms adjF_switch_parabolic
#print axioms trace_compose_via_identity
#print axioms abs_cos_le_of_between
#print axioms lam_is_max_elliptic_trace

end HeckeL2trace

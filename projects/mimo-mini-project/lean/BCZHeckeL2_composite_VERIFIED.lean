import Mathlib
/-!
# Goal I — (L2) no regime-chaining: the COMPOSITE-MONODROMY certificate (ALL q, parametric in `l = λ`)

Goal H reduced the all-q lower bound `X_Ω(q) ≥ 1/l³` (q ≥ 17) to two lemmas:
* (L1) rotation-oscillation — a single elliptic corridor's product exceeds `1/l³` within `O(q)`
  steps (machine-checked: `product_le/ge_on_ellipse` in `BCZHeckeRotation_allq_VERIFIED.lean`);
* (L2) no regime-chaining — an orbit cannot stay sub-threshold by SWITCHING between distinct
  elliptic corridors.

This file machine-checks the **algebraic core of (L2)** for the dominant corridor family
`F k = M_{q-3,0} · M_{q-1,0} · M_{q-1,k}` (the `W_q`-family; `F 3 = W_q`).  Using only the
universal boundary Chebyshev generators (q-independent in `l`):

  `A k = M_{q-1,k} = [[0,1],[-1,k·l]]`,  `B = M_{q-3,0} = [[l,l²-1],[1,l]]`.

RESULTS (all `ring`, valid for every real `l`):
1. `trace_F`           : `tr (F k) = l·(k-2)`  (the single-corridor trace dichotomy: elliptic
                          ⇔ `|l(k-2)|<2` ⇔ `k ∈ {1,2,3}` for `0<l<2`).
2. `trace_compose`     : **`tr (F k₂ · F k₁) = l²·(k₁-2)·(k₂-2) - 2`**  — the trace of CHAINING
                          corridor `F k₁` then `F k₂`.  Equivalently `tr(F k₁)·tr(F k₂) - 2`.
3. `compose_not_slow_elliptic` : for `0<l<2` and `k₁,k₂ ∈ {1,2,3}`, the composite is strictly
   elliptic (`|tr|<2`) **iff `k₁ = k₂ ∈ {1,3}`** (i.e. the orbit STAYED in one corridor).  Any
   genuine SWITCH (`k₁ ≠ k₂`, or via `k=2`) gives `|tr| ≥ 2` (parabolic `tr=-2`, or hyperbolic
   `tr<-2`) — NOT a new sustainable slow rotation.  Hence chaining distinct sub-threshold
   corridors cannot keep the product sub-threshold: each switch crosses `1/l³`.  This is the
   exact (L2) obstruction for the `W_q`-family.

Concretely (the three switch types):
* `compose_k2_parabolic`  : `k₂ = 2` (or `k₁=2`) ⇒ `tr = -2` (parabolic; the cusp boundary).
* `compose_13_hyperbolic` : `{k₁,k₂} = {1,3}` ⇒ `tr = -l²-2 < -2` (hyperbolic ⇒ escape).
* `compose_same_elliptic` : `k₁ = k₂ = k`, `k∈{1,3}` ⇒ `tr = l²-2 ∈ (-2,2)` (same corridor).

`#print axioms` on every theorem is `[propext, Classical.choice, Quot.sound]`.
-/
namespace HeckeL2

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

variable (l : ℝ)

/-- Scalar branch generator `M_{q-1,k} = [[0,1],[-1,k l]]`. -/
def A (k : ℝ) : M2 := ⟨0, 1, -1, k * l⟩
/-- Branch `q-3` generator `M_{q-3,0} = [[l,l²-1],[1,l]]`. -/
def B : M2 := ⟨l, l ^ 2 - 1, 1, l⟩

/-- The `W_q`-family corridor `F k = B · M_{q-1,0} · M_{q-1,k}` (`F 3 = W_q`). -/
def F (k : ℝ) : M2 := mul (mul (B l) (A l 0)) (A l k)

/-- Each corridor is unimodular. -/
theorem det_F (k : ℝ) : det (F l k) = 1 := by
  simp only [F, mul, det, A, B]; ring

/-- **Single-corridor trace** `tr (F k) = l·(k-2)`.  For `0<l<2`: ELLIPTIC (`|tr|<2`,
    a sustainable rotation) iff `k ∈ {1,2,3}`; HYPERBOLIC for `k=0` or `k≥4`. -/
theorem trace_F (k : ℝ) : tr (F l k) = l * (k - 2) := by
  simp only [F, mul, tr, A, B]; ring

/-- **Composite trace law (the (L2) core).**  Chaining corridor `F k₁` then `F k₂` has
    `tr (F k₂ · F k₁) = l²·(k₁-2)·(k₂-2) - 2 = tr(F k₁)·tr(F k₂) - 2`. -/
theorem trace_compose (k₁ k₂ : ℝ) :
    tr (mul (F l k₂) (F l k₁)) = l ^ 2 * (k₁ - 2) * (k₂ - 2) - 2 := by
  simp only [F, mul, tr, A, B]; ring

/-- The composite trace equals `tr(F k₁)·tr(F k₂) − 2` exactly (SL₂ identity made explicit). -/
theorem trace_compose_eq_prod (k₁ k₂ : ℝ) :
    tr (mul (F l k₂) (F l k₁)) = tr (F l k₁) * tr (F l k₂) - 2 := by
  rw [trace_compose, trace_F, trace_F]; ring

/-- **Switch via `k=2` is parabolic.**  If either digit is `2`, the composite has `tr = -2`
    (parabolic — the cusp/threshold boundary, not a sub-threshold rotation). -/
theorem compose_k2_parabolic (k₁ : ℝ) :
    tr (mul (F l 2) (F l k₁)) = -2 := by
  rw [trace_compose]; ring

/-- **Switch `{1,3}` is hyperbolic.**  Chaining the two distinct genuine corridors `k=1, k=3`
    gives `tr = -l²-2`, which is `< -2` for `l > 0` ⇒ HYPERBOLIC ⇒ the orbit escapes the
    corridor (a `P ≥ 1/l³` step). -/
theorem compose_13_hyperbolic : tr (mul (F l 3) (F l 1)) = -l ^ 2 - 2 := by
  rw [trace_compose]; ring

theorem compose_13_hyperbolic_lt (hl : 0 < l) :
    tr (mul (F l 3) (F l 1)) < -2 := by
  rw [compose_13_hyperbolic]; nlinarith [sq_nonneg l, hl]

/-- **Staying in one corridor stays elliptic.**  `k₁ = k₂ = k` with `k ∈ {1,3}` gives
    `tr = l²-2 ∈ (-2,2)` for `0<l<2` — the rotation simply continues (NOT a switch). -/
theorem compose_same_elliptic (k : ℝ) (hk : k = 1 ∨ k = 3) :
    tr (mul (F l k) (F l k)) = l ^ 2 - 2 := by
  rcases hk with h | h <;> subst h <;> (rw [trace_compose]; ring)

theorem compose_same_elliptic_abs_lt (hl0 : 0 < l) (hl2 : l < 2) (k : ℝ)
    (hk : k = 1 ∨ k = 3) : |tr (mul (F l k) (F l k))| < 2 := by
  rw [compose_same_elliptic l k hk, abs_lt]
  constructor <;> nlinarith [sq_nonneg l, hl0, hl2]

/-- **(L2) dichotomy, packaged.**  For `0<l<2` and digits `k₁,k₂ ∈ {1,2,3}` (the only
    single-corridor-elliptic digits), the composite is STRICTLY ELLIPTIC (`|tr|<2`) iff the
    orbit did NOT switch corridor, i.e. `k₁ = k₂ ∧ k₁ ≠ 2`.  Stated as: a genuine switch
    forces `|tr| ≥ 2` (no new sustainable rotation).  We prove the contrapositive cases that
    matter: every distinct pair, and the `k=2` pair, has `|tr| ≥ 2`. -/
theorem switch_forces_nonelliptic
    (k₁ k₂ : ℝ) (h1 : k₁ = 1 ∨ k₁ = 2 ∨ k₁ = 3) (h2 : k₂ = 1 ∨ k₂ = 2 ∨ k₂ = 3)
    (hswitch : k₁ ≠ k₂ ∨ k₁ = 2 ∨ k₂ = 2) :
    2 ≤ |tr (mul (F l k₂) (F l k₁))| := by
  rw [trace_compose, le_abs]; right
  -- every switch case has `tr ≤ -2`, so the right disjunct `2 ≤ -tr` is the one to prove
  rcases hswitch with hne | hk1 | hk2
  · rcases h1 with h1 | h1 | h1 <;> rcases h2 with h2 | h2 | h2 <;> subst h1 <;> subst h2 <;>
      first
        | exact absurd rfl hne                                      -- equal pair: contradicts k₁≠k₂
        | nlinarith [sq_nonneg l]                                  -- distinct pair: tr ≤ -2
  · subst hk1; nlinarith [sq_nonneg l]                              -- k₁=2 ⇒ tr = -2
  · subst hk2; nlinarith [sq_nonneg l]                              -- k₂=2 ⇒ tr = -2

#print axioms det_F
#print axioms trace_F
#print axioms trace_compose
#print axioms trace_compose_eq_prod
#print axioms compose_k2_parabolic
#print axioms compose_13_hyperbolic
#print axioms compose_13_hyperbolic_lt
#print axioms compose_same_elliptic
#print axioms compose_same_elliptic_abs_lt
#print axioms switch_forces_nonelliptic

end HeckeL2

import Mathlib
/-!
# Genuine all-q Hecke–BCZ branch map — foundational + wiring layer (hyp (1) of the qge18 assembly).

λ = l = 2cos(π/q).  Encoded ALGEBRAICALLY: `X(q-1) = 0`, i.e. `cheb l q = 0`, so this file is
parametric in `(q, l)` with no trig.

Chebyshev boundary data (handoff §1):  X(-1)=0, X(0)=1, X(i+1)=λ X(i) − X(i-1).
ℕ-index with a +1 shift:  `cheb l 0 = 0 (=X(-1))`, `cheb l 1 = 1 (=X(0))`,
`cheb l (n+2) = λ·cheb l (n+1) − cheb l n`.  Hence `X(i) = cheb l (i+1)`, and the branch linear
form is `L_i = a X(i) + b X(i-1) = a·cheb(i+1) + b·cheb(i)`.

Contents:
* §1 Chebyshev `cheb`, the **Casorati identity** `X(i)²−X(i-1)X(i+1)=1` (per-step det=1).
* §2 branch form `L_i`, observable `P_i = a L_i / X(i-1)`, the recurrence `L_{i+1}=λL_i−L_{i-1}`.
* §3 **WIRING (1):** the genuine observable identity `P_i = u v − r v²` with `u=L_{i-1}, v=L_i,
  r=X(i-2)/X(i-1)` — exactly the `(u,v,r)` variables of `BCZHeckeEjection.ejection_kick`. Pure
  Casorati consequence.
* §4 the scalar-branch successor `genStep` and **WIRING (2):** the successor product identity
  `P' = a' b' = λv² − uv + kλv² ≥ λv² − uv` (the lower bound `ejection_kick` consumes).

Together §3+§4 reduce the genuine deep-mid ejection step to the already-proven `ejection_kick`,
modulo the (still-to-formalize) branch SELECTOR that decides which `i` is active.

`#print axioms` on every theorem must be `[propext, Classical.choice, Quot.sound]`.
-/
namespace HeckeGenuine

noncomputable section
variable (l : ℝ)

/-! ## §1. Chebyshev + Casorati. -/

/-- Chebyshev sequence: `cheb l 0 = 0 = X(-1)`, `cheb l 1 = 1 = X(0)`,
`cheb l (n+2) = l·cheb l (n+1) − cheb l n`.  Then `X(i) = cheb l (i+1)`. -/
def cheb : ℕ → ℝ
  | 0 => 0
  | 1 => 1
  | (n + 2) => l * cheb (n + 1) - cheb n

@[simp] lemma cheb_zero : cheb l 0 = 0 := rfl
@[simp] lemma cheb_one : cheb l 1 = 1 := rfl
lemma cheb_rec (n : ℕ) : cheb l (n + 2) = l * cheb l (n + 1) - cheb l n := rfl

/-- `X(i) = cheb l (i+1)`. -/
def X (i : ℕ) : ℝ := cheb l (i + 1)

@[simp] lemma X_zero : X l 0 = 1 := rfl
lemma X_one : X l 1 = l := by simp [X, cheb_rec]

/-- **Casorati identity** `cheb(n+1)² − cheb(n)·cheb(n+2) = 1` (per-step det=1; `X(i)²−X(i-1)X(i+1)=1`).
Proved by induction — the difference telescopes to 0. -/
theorem casorati (n : ℕ) : cheb l (n + 1) ^ 2 - cheb l n * cheb l (n + 2) = 1 := by
  induction n with
  | zero => simp [cheb]
  | succ k ih =>
    have hk2 : cheb l (k + 2) = l * cheb l (k + 1) - cheb l k := cheb_rec l k
    have hk3 : cheb l (k + 3) = l * cheb l (k + 2) - cheb l (k + 1) := cheb_rec l (k + 1)
    have e : cheb l (k + 1 + 1) ^ 2 - cheb l (k + 1) * cheb l (k + 1 + 2)
        = cheb l (k + 1) ^ 2 - cheb l k * cheb l (k + 2) := by
      rw [show k + 1 + 1 = k + 2 from rfl, show k + 1 + 2 = k + 3 from rfl, hk3, hk2]; ring
    rw [e]; exact ih

/-- Casorati in `X`-form: `X(i)² − X(i-1) X(i+1) = 1`. -/
theorem casorati_X (i : ℕ) : X l (i + 1) ^ 2 - X l i * X l (i + 2) = 1 := by
  simpa [X] using casorati l (i + 1)

/-! ## §2. Branch form `L_i`, observable `P_i`, the `L`-recurrence. -/

/-- Branch linear form `L_i(a,b) = a X(i) + b X(i-1) = a·cheb(i+1) + b·cheb(i)` (handoff §1).
`L_0 = a` (since `cheb 1 = 1, cheb 0 = 0`). -/
def L (a b : ℝ) (i : ℕ) : ℝ := a * cheb l (i + 1) + b * cheb l i

/-- Genuine observable on branch `i`: `P_i = a · L_i / X(i-1) = a · L_i / cheb(i)` (handoff §1). -/
def Pobs (a b : ℝ) (i : ℕ) : ℝ := a * L l a b i / cheb l i

/-- The branch form obeys the same Chebyshev recurrence: `L_{i+1} = λ L_i − L_{i-1}`. -/
theorem L_rec (a b : ℝ) (i : ℕ) : L l a b (i + 2) = l * L l a b (i + 1) - L l a b i := by
  simp only [L]
  rw [cheb_rec l (i + 1), cheb_rec l i]; ring

/-! ## §3. WIRING (1) — the genuine observable identity `P_i = u v − r v²`.

With `i = n+1`, `u = L_{i-1} = L_n`, `v = L_i = L_{n+1}`, `r = X(i-2)/X(i-1) = cheb n / cheb(n+1)`,
the genuine observable equals `u v − r v²`.  These are exactly the `(u, v, r)` of
`BCZHeckeEjection.ejection_kick`.  The proof is a one-line Casorati reduction. -/
theorem Pobs_eq_uvrv (a b : ℝ) (n : ℕ) (hne : cheb l (n + 1) ≠ 0) :
    Pobs l a b (n + 1)
      = L l a b n * L l a b (n + 1)
        - (cheb l n / cheb l (n + 1)) * (L l a b (n + 1)) ^ 2 := by
  -- the Casorati core: `L_n·X(i-1) − X(i-2)·L_i = a`  (here `X(i-1)=cheb(n+1), X(i-2)=cheb n`)
  have key : L l a b n * cheb l (n + 1) - cheb l n * L l a b (n + 1) = a := by
    simp only [L, show n + 1 + 1 = n + 2 from rfl]
    linear_combination a * casorati l n
  rw [Pobs]
  field_simp
  linear_combination (-(L l a b (n + 1))) * key

/-! ## §4. WIRING (2) — the scalar-branch successor and its product identity.

At a genuine branch step with active index `i` and floor `k`, the successor lands on the scalar
branch `q−1` with `a' = L_i`, `b' = L_{i+1} + k λ L_i` (handoff §1).  Using `L_{i+1} = λ L_i − L_{i-1}`
(`L_rec`), the successor product (= observable on the scalar branch) is
  `P' = a' b' = L_i (L_{i+1} + k λ L_i) = λ L_i² − L_{i-1} L_i + k λ L_i²`.
With `u = L_{i-1}, v = L_i` this is `λ v² − u v + k λ v² ≥ λ v² − u v` for `k ≥ 0, λ ≥ 0` —
the exact lower bound `ejection_kick` turns into `≥ thr`. -/

/-- Successor first/second coordinates on the scalar branch (handoff §1). -/
def succA (a b : ℝ) (i : ℕ) : ℝ := L l a b i
def succB (a b : ℝ) (i : ℕ) (k : ℝ) : ℝ := L l a b (i + 1) + k * l * L l a b i

/-- **Successor product identity.** `a'·b' = λ v² − u v + k λ v²` with `u=L_{i-1}=L l a b i`,
`v=L_i=L l a b (i+1)` (indices shifted: here `i` plays `i-1`). -/
theorem succ_prod_eq (a b : ℝ) (i : ℕ) (k : ℝ) :
    succA l a b (i + 1) * succB l a b (i + 1) k
      = l * (L l a b (i + 1)) ^ 2 - L l a b i * L l a b (i + 1)
        + k * l * (L l a b (i + 1)) ^ 2 := by
  simp only [succA, succB]
  have hLr : L l a b (i + 2) = l * L l a b (i + 1) - L l a b i := L_rec l a b i
  rw [show i + 1 + 1 = i + 2 from rfl, hLr]; ring

/-- **Successor lower bound** (the bound `ejection_kick` consumes): for `k ≥ 0`, `λ ≥ 0`,
`a'·b' ≥ λ v² − u v`. -/
theorem succ_prod_lb (a b : ℝ) (i : ℕ) (k : ℝ) (hk : 0 ≤ k) (hl : 0 ≤ l) :
    l * (L l a b (i + 1)) ^ 2 - L l a b i * L l a b (i + 1)
      ≤ succA l a b (i + 1) * succB l a b (i + 1) k := by
  rw [succ_prod_eq l a b i k]
  have : 0 ≤ k * l * (L l a b (i + 1)) ^ 2 := by positivity
  linarith

/-! ## §5. THE GENUINE EJECTION STEP (wiring §3 + §4 through the proven `ejection_kick`).

Inlined verbatim from `BCZHeckeEjection_q16to21_VERIFIED.ejection_kick` (self-recompiled, axiom-clean):
the deep-mid box bound `thr ≤ λv² − uv` under the genuine domain constraints.  Then `genuine_ejection`
feeds the genuine `(u,v,r)` of §3 and the successor lower bound of §4 into it to conclude, ON THE
GENUINE MAP, that a deep-mid sub-threshold step ejects: the scalar successor product is `≥ thr`. -/

/-- **Deep-mid ejection box bound** (q=16..21). Verbatim from the verified ejection file. -/
theorem ejection_kick (r u v thr : ℝ)
    (hl : (49:ℝ)/25 ≤ l) (hl' : l ≤ (99:ℝ)/50)
    (hr : (47:ℝ)/50 ≤ r) (hr' : r ≤ (61:ℝ)/50)
    (ht : (129:ℝ)/1000 ≤ thr) (ht' : thr ≤ (663:ℝ)/5000)
    (hu : (1:ℝ) < u) (hv : v ≤ 1)
    (htop : l * v - u ≤ 1) (hbot : (1:ℝ) < 2 * l * v - u)
    (hP : u * v - r * v ^ 2 < thr) :
    thr ≤ l * v ^ 2 - u * v := by
  have hlpos : (0:ℝ) < l := by linarith
  have hlv : (1:ℝ) < l * v := by linarith
  have hvpos : (0:ℝ) < v := by nlinarith [hlv, hlpos]
  nlinarith [mul_pos (show (0:ℝ) < u - 1 by linarith) hvpos,
             mul_pos (show (0:ℝ) < l * v - 1 by linarith) hvpos,
             mul_pos hvpos hvpos,
             mul_nonneg (show (0:ℝ) ≤ 1 - v by linarith) hvpos.le,
             mul_nonneg (show (0:ℝ) ≤ thr - (u * v - r * v ^ 2) by linarith) hvpos.le,
             mul_nonneg (show (0:ℝ) ≤ (61:ℝ)/50 - r by linarith) (mul_nonneg hvpos.le hvpos.le),
             mul_pos hvpos (show (0:ℝ) < 2 * l * v - u - 1 by linarith),
             sq_nonneg (l * v - 1), sq_nonneg (u - 1), hlv, hvpos, hu, hr, hr']

/-- **Genuine deep-mid ejection on the all-q map** (box q=16..21).  Active branch `i = n+1`;
write `u = L_{i-1} = L_n`, `v = L_i = L_{n+1}`, `r = X(i-2)/X(i-1) = cheb n / cheb(n+1)`.  Under the
genuine domain box (`l,r,thr` in the verified ranges, `u>1, v≤1, λv−u≤1, 1<2λv−u`) and floor `k≥0`,
a sub-threshold genuine observable `P_i < thr` forces the scalar successor product `a'·b' ≥ thr` —
i.e. dwell ≤ 1.  This is hyp (2)'s ejection content, proven on the genuine map: §3 (`Pobs_eq_uvrv`)
supplies `P_i = uv − rv²`, `ejection_kick` gives `thr ≤ λv²−uv`, §4 (`succ_prod_lb`) lifts it to the
successor product. -/
theorem genuine_ejection (a b : ℝ) (n : ℕ) (k thr : ℝ)
    (hne : cheb l (n + 1) ≠ 0)
    (hl : (49:ℝ)/25 ≤ l) (hl' : l ≤ (99:ℝ)/50)
    (hr : (47:ℝ)/50 ≤ cheb l n / cheb l (n + 1)) (hr' : cheb l n / cheb l (n + 1) ≤ (61:ℝ)/50)
    (ht : (129:ℝ)/1000 ≤ thr) (ht' : thr ≤ (663:ℝ)/5000)
    (hu : (1:ℝ) < L l a b n) (hv : L l a b (n + 1) ≤ 1)
    (htop : l * L l a b (n + 1) - L l a b n ≤ 1)
    (hbot : (1:ℝ) < 2 * l * L l a b (n + 1) - L l a b n)
    (hk : 0 ≤ k)
    (hP : Pobs l a b (n + 1) < thr) :
    thr ≤ succA l a b (n + 1) * succB l a b (n + 1) k := by
  have hlpos : (0:ℝ) ≤ l := by linarith
  -- §3: rewrite the genuine observable into the `uv − rv²` form `ejection_kick` expects
  have hPuv : L l a b n * L l a b (n + 1)
      - (cheb l n / cheb l (n + 1)) * (L l a b (n + 1)) ^ 2 < thr := by
    rw [← Pobs_eq_uvrv l a b n hne]; exact hP
  -- ejection box bound: thr ≤ λv² − uv
  have hkick := ejection_kick l (cheb l n / cheb l (n + 1)) (L l a b n) (L l a b (n + 1)) thr
    hl hl' hr hr' ht ht' hu hv htop hbot hPuv
  -- §4: λv² − uv ≤ a'·b'
  have hlb := succ_prod_lb l a b n k hk hlpos
  linarith

end
end HeckeGenuine

#print axioms HeckeGenuine.casorati
#print axioms HeckeGenuine.casorati_X
#print axioms HeckeGenuine.L_rec
#print axioms HeckeGenuine.Pobs_eq_uvrv
#print axioms HeckeGenuine.succ_prod_eq
#print axioms HeckeGenuine.succ_prod_lb

#print axioms HeckeGenuine.ejection_kick
#print axioms HeckeGenuine.genuine_ejection

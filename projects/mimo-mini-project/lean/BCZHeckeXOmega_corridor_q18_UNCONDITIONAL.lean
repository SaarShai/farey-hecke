import Mathlib
/-
⚠️⚠️ VACUOUS RESULT — DO NOT CITE AS A BOUND. (honest correction, 2026-06-05) ⚠️⚠️
`Xomega_corridor_lb_q18` below is axiom-clean and TRUE, but its hypothesis class is EMPTY:
the scalar `Tmap` does NOT preserve `Dcorr` (every orbit escapes in ≤16 steps; 0 periodic cycles;
`test_invariance(18)` esc_scalar=1.0), so NO `Tmap`-invariant probability measure with `μ(Dcorr)ᶜ=0`
exists. The theorem therefore constrains nothing. The genuine map DOES preserve Taha
(esc_genuine=0.0); the correct non-vacuous statement is over `genStep`-invariant measures on Taha,
which needs the LEVEL-2 multi-branch (C′) (still open). Kept only as a record of the vacuity lesson.
See FINDINGS_genuinemap_wiring_2026-06-05.md §6.
-/
set_option maxHeartbeats 4000000
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


/-! ## §6. BRANCH SELECTOR well-definedness.

The genuine branch is **the smallest index `i ≥ 1` with `L_i ≤ 1`**.  On the Taha triangle the
`L`-sequence crosses `1` from above, so such an `i` exists; we keep that existence as a hypothesis
`h` (discharged later from the triangle geometry).  `branchIdx` selects it via `Nat.find`, and
`branchIdx_spec` records its three defining properties: it is `≥ 1`, it is active (`L ≤ 1`), and it
is minimal (no strictly smaller index is active). -/

open Classical in
/-- The active genuine branch index: the least `i` with `1 ≤ i ∧ L_i ≤ 1`. -/
noncomputable def branchIdx (a b : ℝ) (h : ∃ i, 1 ≤ i ∧ L l a b i ≤ 1) : ℕ :=
  Nat.find h

open Classical in
/-- **Selector spec.**  `branchIdx` is `≥ 1`, lands on an active branch (`L ≤ 1`), and is minimal:
no strictly smaller index satisfies the active predicate.  Pure `Nat.find` well-definedness — the
existence hypothesis `h` is *assumed* here (it is supplied later from the triangle geometry). -/
theorem branchIdx_spec (a b : ℝ) (h : ∃ i, 1 ≤ i ∧ L l a b i ≤ 1) :
    1 ≤ branchIdx l a b h ∧ L l a b (branchIdx l a b h) ≤ 1 ∧
      ∀ j, j < branchIdx l a b h → ¬ (1 ≤ j ∧ L l a b j ≤ 1) := by
  refine ⟨?_, ?_, ?_⟩
  · exact (Nat.find_spec h).1
  · exact (Nat.find_spec h).2
  · intro j hj
    exact Nat.find_min h hj

/-! ## §6. DOMAIN → EJECTION-BOX structural hypotheses (the `domainbox` sub-lemma).

`genuine_ejection` consumes four structural hyps on `u = L_{i-1} = L l a b n`,
`v = L_i = L l a b (n+1)` (active branch `i = n+1`):
  (1) `1 < u`            (2) `v ≤ 1`            (3) `l v − u ≤ 1`            (4) `1 < 2 l v − u`.
(1),(2) are the branch entry/active predicate (supplied verbatim as `hentry`,`hactive`).

The genuine content of (3),(4) is the **BCZ floor selector**: at the active branch the genuine
Hecke–BCZ floor is `K = ⌊(1 + u)/(l v)⌋` (exactly the floor of `infinitely_many_high_floor`'s
recurrence `c n + c(n+2) = ⌊(1+c n)/(l·c(n+1))⌋·l·c(n+1)`, with `u=c_n, v=c_{n+1}`).  The deep-mid
/ rotation regime that `ejection_kick` covers is precisely **floor `K = 1`**, and
  `K = 1  ⟺  1 ≤ (1+u)/(l v) < 2  ⟺  l v ≤ 1+u  ∧  1+u < 2 l v  ⟺  (3) ∧ (4)`.
So (3),(4) ARE the floor-1 selector; they are NOT derivable from (1),(2) alone — they need the
genuine fact `K_n = 1` (the orbit is on the floor-1 branch at step `n`) plus the positive-coordinate
domain fact `v = c_{n+1} > 0`. The only extra hyps are therefore exactly those two genuine facts. -/

/-- Floor-`1` two-sided bound: from `⌊x⌋ = 1` get `1 ≤ x < 2`, specialised to `x = (1+u)/(l v)`
with `0 < l v`, giving `l v ≤ 1 + u` and `1 + u < 2 l v` (the (3),(4) inequalities). -/
theorem floor_one_lv_bounds (u v : ℝ) (hlv : 0 < l * v)
    (hfloor : ⌊(1 + u) / (l * v)⌋ = 1) :
    l * v - u ≤ 1 ∧ 1 < 2 * l * v - u := by
  -- 1 ≤ (1+u)/(l v)
  have hge : (1:ℝ) ≤ (1 + u) / (l * v) := by
    have h := Int.floor_le ((1 + u) / (l * v))
    rw [hfloor] at h; push_cast at h; linarith
  -- (1+u)/(l v) < 2
  have hlt : (1 + u) / (l * v) < 2 := by
    have h := Int.lt_floor_add_one ((1 + u) / (l * v))
    rw [hfloor] at h; push_cast at h; linarith
  -- clear the (positive) denominator
  have h3 : l * v ≤ 1 + u := by
    rw [le_div_iff₀ hlv] at hge; linarith
  have h4 : 1 + u < 2 * (l * v) := by
    rw [div_lt_iff₀ hlv] at hlt; linarith
  exact ⟨by linarith, by linarith⟩

/-- **DOMAIN → EJECTION-BOX (genuine floor-1 form).**  The four structural hypotheses that
`genuine_ejection` needs, derived from the branch entry/active predicate `(hentry,hactive)` plus the
two genuine domain facts:
  * `hvpos : 0 < L l a b (n+1)` — positivity of the active branch coordinate `v = c_{n+1}` (open
    genuine domain; the `hpos` of `infinitely_many_high_floor`);
  * `hfloor : ⌊(1 + L l a b n)/(l · L l a b (n+1))⌋ = 1` — the genuine BCZ floor SELECTOR: at step
    `n` the orbit is on floor 1 (the deep-mid / rotation branch `ejection_kick` is calibrated for).
`hl0 : 0 < l` is the box positivity of `λ`.  Nothing else is assumed; (3),(4) are exactly the
floor-1 selector unpacked. -/
theorem branch_domain_hyps (a b : ℝ) (n : ℕ)
    (hl0 : 0 < l)
    (hentry : 1 < L l a b n) (hactive : L l a b (n + 1) ≤ 1)
    (hvpos : 0 < L l a b (n + 1))
    (hfloor : ⌊(1 + L l a b n) / (l * L l a b (n + 1))⌋ = 1) :
    1 < L l a b n
      ∧ L l a b (n + 1) ≤ 1
      ∧ l * L l a b (n + 1) - L l a b n ≤ 1
      ∧ 1 < 2 * l * L l a b (n + 1) - L l a b n := by
  have hlv : 0 < l * L l a b (n + 1) := mul_pos hl0 hvpos
  obtain ⟨h3, h4⟩ := floor_one_lv_bounds l (L l a b n) (L l a b (n + 1)) hlv hfloor
  exact ⟨hentry, hactive, h3, h4⟩

/-- **(3) is FREE from the box `λ`-bound** (`λ ≤ 99/50 < 2`), `v ≤ 1`, `1 < u`: independent of the
floor.  `l v − u ≤ l·1 − u < l − 1 ≤ 49/50 < 1`.  So the only *genuine* (floor-dependent) part of
the structural box is (4); (3) holds for ANY active branch in the box. -/
theorem topcon_free (a b : ℝ) (n : ℕ)
    (hl0 : 0 < l) (hl' : l ≤ (99:ℝ)/50)
    (hentry : 1 < L l a b n) (hactive : L l a b (n + 1) ≤ 1) :
    l * L l a b (n + 1) - L l a b n ≤ 1 := by
  have hv1 : l * L l a b (n + 1) ≤ l := by
    nlinarith [hactive, hl0, mul_le_mul_of_nonneg_left hactive hl0.le]
  linarith

/-- **DOMAIN → EJECTION-BOX (box form).**  Same conclusion as `branch_domain_hyps`, but (3) is taken
from the box `λ`-bound `topcon_free` instead of the floor, so the floor hypothesis is only needed in
its **lower** form `1 + u < 2 l v` (the genuine "not yet ejected past floor 1" half).  Demonstrates
that the floor's *upper* half is the load-bearing genuine input for the box, with `λ < 2` covering
the rest. -/
theorem branch_domain_hyps_box (a b : ℝ) (n : ℕ)
    (hl0 : 0 < l) (hl' : l ≤ (99:ℝ)/50)
    (hentry : 1 < L l a b n) (hactive : L l a b (n + 1) ≤ 1)
    (hbot' : 1 + L l a b n < 2 * (l * L l a b (n + 1))) :
    1 < L l a b n
      ∧ L l a b (n + 1) ≤ 1
      ∧ l * L l a b (n + 1) - L l a b n ≤ 1
      ∧ 1 < 2 * l * L l a b (n + 1) - L l a b n := by
  refine ⟨hentry, hactive, topcon_free l a b n hl0 hl' hentry hactive, ?_⟩
  linarith

/-! ## §6. THE (L2)+CUSP BRIDGE (this file's target `l2cusp`).

Glue of two already-proven lemmas, re-exposed in `namespace HeckeGenuine`:

* the **cusp-branch envelope** `cusp_envelope` (verbatim from
  `BCZHeckeCusp_envelope_allq_VERIFIED.lean`): on the genuine cusp(parabolic) branch `i = q−2`,
  `P = a(a+l b)/l ≥ 1/l³` for every `l ≥ φ`;
* the **L2 composite-monodromy** machinery `M2`/`F`/`trace_compose`/`switch_forces_nonelliptic`
  (verbatim from `BCZHeckeL2_composite_VERIFIED.lean`): an `F`-family corridor SWITCH forces
  `|tr| ≥ 2` (non-elliptic), so no new sub-threshold rotation can be chained.

The packaged result is `kick_bound_of_cusp`: under the cusp-branch guards and `l ≥ φ`, the genuine
observable `Pgen (a,b) = a(a+l b)/l ≥ 1/l³` — exactly the `hcuspAtKick` content the assembly's
`essSup_genuine_ge_via_cusp` consumes; plus `switch_forces_nonelliptic` re-exposed. -/

/-- Genuine observable `P = a (a + l b)/l` (matches the assembly's `Pgen` and the q=5 `P3`). -/
def Pgen (l : ℝ) (p : ℝ × ℝ) : ℝ := p.1 * (p.1 + l * p.2) / l
@[simp] lemma Pgen_apply (l : ℝ) (p : ℝ × ℝ) : Pgen l p = p.1 * (p.1 + l * p.2) / l := rfl

/-- **Cusp-branch envelope, all q** (verbatim from `BCZHeckeCusp_envelope_allq_VERIFIED`). For
`l ≥ φ` (`l² ≥ l+1`, `l>1`): on the genuine cusp branch `i=q−2` (guards `l a + (l²−1) b > 1`,
domain `l a + b > 1`, upper `a + l b ≤ 1`, `0<a≤1`), the observable `P = a(a+l b)/l ≥ 1/l³`. -/
theorem cusp_envelope (l a b : ℝ)
    (hl1 : 1 < l) (hlphi : l ^ 2 ≥ l + 1)
    (ha : 0 < a) (ha1 : a ≤ 1)
    (hG : l * a + (l ^ 2 - 1) * b > 1)
    (hd : l * a + b > 1)
    (hU : a + l * b ≤ 1) :
    1 / l ^ 3 ≤ a * (a + l * b) / l := by
  have hl : 0 < l := by linarith
  have hl2 : l ^ 2 - 2 > 0 := by nlinarith [hlphi, hl1]
  have hc1 : l ^ 3 - l - 1 ≥ 0 := by nlinarith [hlphi, hl1]
  have hc2 : l ^ 2 - l - 1 ≥ 0 := by linarith [hlphi]
  -- main: W = l^2 a (a + l b) - 1 ≥ 0
  have hkey : 1 ≤ l ^ 2 * (a * (a + l * b)) := by
    rcases le_or_gt a (1 / l) with hca | hca
    · -- a ≤ 1/l
      have hfa : l * a ≤ 1 := by rw [mul_comm]; exact (le_div_iff₀ hl).mp hca
      -- a ≥ 1/(l+1):  from upper guard hU and domain hd
      have hage : a * (l + 1) ≥ 1 := by nlinarith [hU, hd, hl]
      have hlo : 1 ≤ l ^ 2 * a := by nlinarith [hage, hlphi, ha, hl]
      -- (l^2-2) W = (l^3-l-1) a d + (l^2-2)(l^2 a -1)(1-l a) + (l^2-l-1) a G
      nlinarith [hl2, hl,
        mul_nonneg hc1 (mul_nonneg ha.le (show (0:ℝ) ≤ l * a + b - 1 by linarith)),
        mul_nonneg hl2.le (mul_nonneg (show (0:ℝ) ≤ l ^ 2 * a - 1 by linarith)
                                      (show (0:ℝ) ≤ 1 - l * a by linarith)),
        mul_nonneg hc2 (mul_nonneg ha.le (show (0:ℝ) ≤ l * a + (l ^ 2 - 1) * b - 1 by linarith))]
    · -- a > 1/l
      have hfa : 1 ≤ l * a := by
        have h := (div_lt_iff₀ hl).mp hca; rw [mul_comm] at h; linarith
      -- (l^2-2) W = (l^3-l-1) a G + (l^2-2)(l a -1)(1-a) + (l^2-l-1) a d
      nlinarith [hl2, hl,
        mul_nonneg hc1 (mul_nonneg ha.le (show (0:ℝ) ≤ l * a + (l ^ 2 - 1) * b - 1 by linarith)),
        mul_nonneg hl2.le (mul_nonneg (show (0:ℝ) ≤ l * a - 1 by linarith)
                                      (show (0:ℝ) ≤ 1 - a by linarith)),
        mul_nonneg hc2 (mul_nonneg ha.le (show (0:ℝ) ≤ l * a + b - 1 by linarith))]
  -- convert W ≥ 0 to the envelope
  have e : a * (a + l * b) / l - 1 / l ^ 3
      = (l ^ 2 * (a * (a + l * b)) - 1) / l ^ 3 := by
    rw [div_sub_div _ _ (by positivity : (l:ℝ) ≠ 0) (by positivity : (l:ℝ) ^ 3 ≠ 0)]
    rw [div_eq_div_iff (by positivity) (by positivity)]; ring
  have hnn : 0 ≤ a * (a + l * b) / l - 1 / l ^ 3 := by
    rw [e]; exact div_nonneg (by linarith [hkey]) (by positivity)
  linarith

/-- **Kick bound, DERIVED from `cusp_envelope`** (reproduces the assembly's `kick_bound_of_cusp`).
At a high-floor step the orbit point lands on the cusp(parabolic) branch (the (L2) content); given
the cusp-branch guards there, `cusp_envelope` delivers the genuine observable `Pgen ≥ 1/l³`.  This
is exactly the `hcuspAtKick` content consumed by `essSup_genuine_ge_via_cusp`. -/
theorem kick_bound_of_cusp
    {l a b : ℝ} (hl1 : 1 < l) (hlphi : l ^ 2 ≥ l + 1)
    (hcuspGuards : 0 < a ∧ a ≤ 1 ∧ l * a + (l ^ 2 - 1) * b > 1 ∧ l * a + b > 1 ∧ a + l * b ≤ 1) :
    1 / l ^ 3 ≤ Pgen l (a, b) := by
  obtain ⟨ha, ha1, hG, hd, hU⟩ := hcuspGuards
  simpa [Pgen] using cusp_envelope l a b hl1 hlphi ha ha1 hG hd hU

/-! ### §6b. The (L2) composite-monodromy corridor machinery (verbatim from
`BCZHeckeL2_composite_VERIFIED.lean`), exposed in `HeckeGenuine` so the corridor-switch obstruction
sits beside the cusp bound it pairs with. -/

/-- 2×2 real matrix as a flat record (the (L2) corridor calculus). -/
structure M2 where
  a : ℝ
  b : ℝ
  c : ℝ
  d : ℝ

@[ext] theorem M2.ext {X Y : M2}
    (ha : X.a = Y.a) (hb : X.b = Y.b) (hc : X.c = Y.c) (hd : X.d = Y.d) : X = Y := by
  cases X; cases Y; simp_all

/-- Matrix product. -/
def M2.mul (X Y : M2) : M2 :=
  ⟨X.a * Y.a + X.b * Y.c, X.a * Y.b + X.b * Y.d,
   X.c * Y.a + X.d * Y.c, X.c * Y.b + X.d * Y.d⟩

/-- Trace. -/
def M2.tr  (X : M2) : ℝ := X.a + X.d
/-- Determinant. -/
def M2.det (X : M2) : ℝ := X.a * X.d - X.b * X.c

/-- Scalar branch generator `M_{q-1,k} = [[0,1],[-1,k l]]`. -/
def Acorr (l k : ℝ) : M2 := ⟨0, 1, -1, k * l⟩
/-- Branch `q-3` generator `M_{q-3,0} = [[l,l²-1],[1,l]]`. -/
def Bcorr (l : ℝ) : M2 := ⟨l, l ^ 2 - 1, 1, l⟩

/-- The `W_q`-family corridor `F k = B · M_{q-1,0} · M_{q-1,k}` (`F 3 = W_q`). -/
def Fcorr (l k : ℝ) : M2 := M2.mul (M2.mul (Bcorr l) (Acorr l 0)) (Acorr l k)

/-- Each corridor is unimodular. -/
theorem det_Fcorr (l k : ℝ) : M2.det (Fcorr l k) = 1 := by
  simp only [Fcorr, M2.mul, M2.det, Acorr, Bcorr]; ring

/-- **Single-corridor trace** `tr (F k) = l·(k-2)`. -/
theorem trace_Fcorr (l k : ℝ) : M2.tr (Fcorr l k) = l * (k - 2) := by
  simp only [Fcorr, M2.mul, M2.tr, Acorr, Bcorr]; ring

/-- **Composite trace law (the (L2) core).** `tr (F k₂ · F k₁) = l²·(k₁-2)·(k₂-2) - 2`. -/
theorem trace_compose (l k₁ k₂ : ℝ) :
    M2.tr (M2.mul (Fcorr l k₂) (Fcorr l k₁)) = l ^ 2 * (k₁ - 2) * (k₂ - 2) - 2 := by
  simp only [Fcorr, M2.mul, M2.tr, Acorr, Bcorr]; ring

/-- **An `F`-family corridor SWITCH forces `|trace| ≥ 2`** (re-exposes
`HeckeL2.switch_forces_nonelliptic`).  For `0<l<2` and digits `k₁,k₂ ∈ {1,2,3}` (the only
single-corridor-elliptic digits), a genuine SWITCH (`k₁ ≠ k₂`, or via the cusp digit `k=2`) makes
the chained composite non-elliptic (`|tr| ≥ 2`): parabolic `tr=-2` or hyperbolic `tr<-2`.  Hence no
new sub-threshold rotation can be sustained by switching corridors — the (L2) obstruction. -/
theorem switch_forces_nonelliptic
    (l k₁ k₂ : ℝ) (h1 : k₁ = 1 ∨ k₁ = 2 ∨ k₁ = 3) (h2 : k₂ = 1 ∨ k₂ = 2 ∨ k₂ = 3)
    (hswitch : k₁ ≠ k₂ ∨ k₁ = 2 ∨ k₂ = 2) :
    2 ≤ |M2.tr (M2.mul (Fcorr l k₂) (Fcorr l k₁))| := by
  rw [trace_compose, le_abs]; right
  rcases hswitch with hne | hk1 | hk2
  · rcases h1 with h1 | h1 | h1 <;> rcases h2 with h2 | h2 | h2 <;> subst h1 <;> subst h2 <;>
      first
        | exact absurd rfl hne
        | nlinarith [sq_nonneg l]
  · subst hk1; nlinarith [sq_nonneg l]
  · subst hk2; nlinarith [sq_nonneg l]

/-! ## §6. HIGH-FLOOR ⟹ CUSP-BRANCH GUARDS (the geometric crux, hyp (3) of the assembly). -/

/-- **Floor ≥ 2 forces `b > 0`.**  The genuine floor is `K = ⌊(1+a)/(l·b)⌋`.  With `0 < a` and
`0 < l`, the hypothesis `2 ≤ K` already pins the divisor sign: `b ≤ 0` would make `l·b ≤ 0` and
the ratio `(1+a)/(l·b) ≤ 0 < 2` (in Lean, `x/0 = 0` and `x/neg < 0` for `x>0`), contradiction.
This is the one genuinely-load-bearing consequence of the floor — everything cusp-side needs `b>0`. -/
theorem floor_ge_two_pos_b {a b : ℝ} (hl0 : 0 < l) (ha : 0 < a)
    (hfloor : (2 : ℤ) ≤ ⌊(1 + a) / (l * b)⌋) : 0 < b := by
  -- turn the floor bound into a real bound: 2 ≤ (1+a)/(l*b)
  have hratio : (2 : ℝ) ≤ (1 + a) / (l * b) := by
    have := (Int.le_floor).mp hfloor
    simpa using this
  by_contra hb
  push_neg at hb  -- b ≤ 0
  have h1a : (0 : ℝ) < 1 + a := by linarith
  rcases lt_or_eq_of_le hb with hbneg | hbz
  · -- b < 0 ⟹ l*b < 0 ⟹ ratio < 0 < 2
    have hlb : l * b < 0 := mul_neg_of_pos_of_neg hl0 hbneg
    have hr : (1 + a) / (l * b) < 0 := div_neg_of_pos_of_neg h1a hlb
    linarith
  · -- b = 0 ⟹ l*b = 0 ⟹ ratio = 0 < 2 (Lean div by zero)
    have hlb : l * b = 0 := by rw [hbz]; ring
    rw [hlb, div_zero] at hratio
    linarith

/-- **G2 is the Taha lower domain edge.**  The guard `l·a + b > 1` is *definitionally* the Taha
triangle lower edge `1 − l·a < b`; recorded here so the audit is explicit that G2 is supplied by the
domain, not derived from the floor. -/
theorem highfloor_G2_is_domain {a b : ℝ} (hdom : 1 - l * a < b) : l * a + b > 1 := by
  linarith

/-- **G1 from the floor (`b>0`) + G2 + `l² ≥ 2`.**  For `q ≥ 18` (`l > 9/5`, so `l² ≥ 2`): since the
floor forces `b>0` and `l²−1 ≥ 1`, the deepest cusp guard follows from G2:
`l·a + (l²−1)·b = (l·a + b) + (l²−2)·b ≥ l·a + b > 1`. -/
theorem highfloor_guard_G1 {a b : ℝ} (hl2 : 2 ≤ l ^ 2) (hbpos : 0 < b)
    (hG2 : l * a + b > 1) : l * a + (l ^ 2 - 1) * b > 1 := by
  have hnn : 0 ≤ (l ^ 2 - 2) * b := mul_nonneg (by linarith) hbpos.le
  nlinarith [hnn, hG2]

/-- **Main combined high-floor ⟹ lower cusp guards** (the part that closes).  From floor `K ≥ 2`
plus the natural domain `0<a, 0<l, l²≥2` (q≥18) and the Taha lower edge `1−l·a<b`, derive
`b>0 ∧ G1 ∧ G2`.  The upper guard G3 (`a+l·b≤1`) is NOT included — it is independent of the floor
(see `highfloor_G3_counterexample`). -/
theorem highfloor_lower_guards {a b : ℝ}
    (hl0 : 0 < l) (hl2 : 2 ≤ l ^ 2) (ha : 0 < a)
    (hdom : 1 - l * a < b)
    (hfloor : (2 : ℤ) ≤ ⌊(1 + a) / (l * b)⌋) :
    0 < b ∧ l * a + (l ^ 2 - 1) * b > 1 ∧ l * a + b > 1 := by
  have hbpos : 0 < b := floor_ge_two_pos_b l hl0 ha hfloor
  have hG2 : l * a + b > 1 := highfloor_G2_is_domain l hdom
  have hG1 : l * a + (l ^ 2 - 1) * b > 1 := highfloor_guard_G1 l hl2 hbpos hG2
  exact ⟨hbpos, hG1, hG2⟩

/-- **G3 is NOT derivable (clean counterexample).**  With `l = 19/10` (`∈ (9/5, 2)`, q≥18 range),
`a = 1/2`, `b = 3/(4l)`: every high-floor + Taha hypothesis holds — `0<a≤1`, `b≤1`, the Taha lower
edge `1−l·a<b`, AND `⌊(1+a)/(l·b)⌋ = 2 ≥ 2` — yet `a + l·b = 5/4 > 1`, so the upper cusp guard G3
FAILS.  This *proves* that high floor + domain does NOT imply G3: it must come from the branch
geometry, not the floor magnitude. -/
theorem highfloor_G3_counterexample :
    let l : ℝ := 19/10
    let a : ℝ := 1/2
    let b : ℝ := 3/(4*l)
    (0 < a ∧ a ≤ 1) ∧ (0 < b ∧ b ≤ 1) ∧ (1 - l * a < b) ∧
    ((2 : ℤ) ≤ ⌊(1 + a) / (l * b)⌋) ∧ ¬ (a + l * b ≤ 1) := by
  intro l a b
  have hlval : l = 19/10 := rfl
  have hbval : b = 3/(4 * (19/10)) := rfl
  -- b = 15/38
  have hb : b = 15/38 := by rw [hbval]; norm_num
  refine ⟨⟨by norm_num, by norm_num⟩, ⟨by rw [hb]; norm_num, by rw [hb]; norm_num⟩, ?_, ?_, ?_⟩
  · rw [hb]; norm_num
  · -- floor = 2: l*b = 3/4, (1+a)/(l*b) = (3/2)/(3/4) = 2, ⌊2⌋ = 2
    have hlb : l * b = 3/4 := by rw [hb]; norm_num
    have hratio : (1 + a) / (l * b) = 2 := by rw [hlb]; norm_num
    rw [hratio]; norm_num
  · -- a + l*b = 1/2 + 3/4 = 5/4 > 1
    have hlb : l * b = 3/4 := by rw [hb]; norm_num
    rw [hlb]; norm_num


/-! ## §10. CAPSTONE — genuine deep-mid ejection from the floor-1 selector (box q=16..21).

Collapses `genuine_ejection`'s four structural hyps into the GENUINE map facts that produce them
(`branch_domain_hyps`): the active-branch entry/active predicate, coordinate positivity, and the
floor-1 selector `⌊(1+u)/(λv)⌋ = 1`.  So: on the deep-mid floor-1 branch (box q=16..21), a
sub-threshold genuine observable forces the scalar successor product `≥ thr` (dwell ≤ 1) — stated
purely in genuine-map quantities, no free structural hyps. -/
theorem genuine_ejection_floor1 (a b : ℝ) (n : ℕ) (k thr : ℝ)
    (hne : cheb l (n + 1) ≠ 0)
    (hl : (49:ℝ)/25 ≤ l) (hl' : l ≤ (99:ℝ)/50)
    (hr : (47:ℝ)/50 ≤ cheb l n / cheb l (n + 1)) (hr' : cheb l n / cheb l (n + 1) ≤ (61:ℝ)/50)
    (ht : (129:ℝ)/1000 ≤ thr) (ht' : thr ≤ (663:ℝ)/5000)
    (hentry : 1 < L l a b n) (hactive : L l a b (n + 1) ≤ 1)
    (hvpos : 0 < L l a b (n + 1))
    (hfloor : ⌊(1 + L l a b n) / (l * L l a b (n + 1))⌋ = 1)
    (hk : 0 ≤ k)
    (hP : Pobs l a b (n + 1) < thr) :
    thr ≤ succA l a b (n + 1) * succB l a b (n + 1) k := by
  have hl0 : 0 < l := by linarith
  obtain ⟨hu, hv, htop, hbot⟩ := branch_domain_hyps l a b n hl0 hentry hactive hvpos hfloor
  exact genuine_ejection l a b n k thr hne hl hl' hr hr' ht ht' hu hv htop hbot hk hP


-- ===== TRACK selectorexist =====
/-! ## §11. SELECTOR EXISTENCE (unlocks `branchIdx` non-vacuously).

The genuine branch index `branchIdx` is `Nat.find` of `∃ i, 1 ≤ i ∧ L_i ≤ 1`; everything downstream
(`branchIdx_spec`) is gated on that existence hypothesis `h`.  Here we DISCHARGE `h` from the algebraic
boundary data of the principal Hecke root.  Parametrize `q = m+2`, so `q−1 = m+1`.  The boundary
hyps `cheb l (m+2) = 0` (= `X(q−1)=0`, first boundary) and `cheb l (m+1) = 1` (= `X(q−2)=1`, second
boundary) give, at the witness branch `i = q−1 = m+1`:
  `L_{q−1} = a·X(q−1) + b·X(q−2) = a·cheb(m+2) + b·cheb(m+1) = a·0 + b·1 = b`,
which is `≤ 1` on the Taha triangle (`hb : b ≤ 1`).  Since `m+1 ≥ 1`, the active-branch predicate
`1 ≤ i ∧ L_i ≤ 1` holds at `i = m+1`.  Hence the selector existence holds and `branchIdx` is
well-defined non-vacuously. -/

/-- **Selector existence (algebraic boundary form).**  Witness `i = q−1 = m+1`.  At the second
boundary `cheb l (m+2) = 0`, `cheb l (m+1) = 1` the branch form collapses to `L_{q−1} = b`, so the
active predicate `1 ≤ i ∧ L_i ≤ 1` holds there for any `b ≤ 1` (the Taha-triangle bound). -/
theorem branch_exists (a b : ℝ) (m : ℕ)
    (hq0 : cheb l (m + 2) = 0) (hq1 : cheb l (m + 1) = 1) (hb : b ≤ 1) :
    ∃ i, 1 ≤ i ∧ L l a b i ≤ 1 := by
  refine ⟨m + 1, ?_, ?_⟩
  · exact Nat.le_add_left 1 m
  · -- L l a b (m+1) = a·cheb(m+2) + b·cheb(m+1) = a·0 + b·1 = b ≤ 1
    have hL : L l a b (m + 1) = b := by
      simp only [L, show m + 1 + 1 = m + 2 from rfl, hq0, hq1]; ring
    rw [hL]; exact hb

/-- **`L` at the witness branch collapses to `b`.**  Records the algebraic fact behind
`branch_exists`: at the second-boundary data, `L_{q−1} = L l a b (m+1) = b`. -/
theorem L_witness_eq_b (a b : ℝ) (m : ℕ)
    (hq0 : cheb l (m + 2) = 0) (hq1 : cheb l (m + 1) = 1) :
    L l a b (m + 1) = b := by
  simp only [L, show m + 1 + 1 = m + 2 from rfl, hq0, hq1]; ring

open Classical in
/-- **Fully-discharged `branchIdx`** (no existence hypothesis).  Bundles `branch_exists` with the
boundary data so the active branch index is produced directly from the algebraic boundary hyps —
the selector is non-vacuous on the genuine domain. -/
noncomputable def branchIdx' (a b : ℝ) (m : ℕ)
    (hq0 : cheb l (m + 2) = 0) (hq1 : cheb l (m + 1) = 1) (hb : b ≤ 1) : ℕ :=
  branchIdx l a b (branch_exists l a b m hq0 hq1 hb)

open Classical in
/-- **Fully-discharged selector spec** (no existence hypothesis).  Combines `branch_exists` with
`branchIdx_spec`: from the algebraic boundary data alone, the selected branch is `≥ 1`, active
(`L ≤ 1`), and minimal.  This CLOSES the selector well-definedness on the genuine domain. -/
theorem branchIdx'_spec (a b : ℝ) (m : ℕ)
    (hq0 : cheb l (m + 2) = 0) (hq1 : cheb l (m + 1) = 1) (hb : b ≤ 1) :
    1 ≤ branchIdx' l a b m hq0 hq1 hb
      ∧ L l a b (branchIdx' l a b m hq0 hq1 hb) ≤ 1
      ∧ ∀ j, j < branchIdx' l a b m hq0 hq1 hb → ¬ (1 ≤ j ∧ L l a b j ≤ 1) := by
  exact branchIdx_spec l a b (branch_exists l a b m hq0 hq1 hb)

-- ===== TRACK cuspguard =====

/-! ## §11. CUSP-GUARD MEMBERSHIP — closes residual G3 (this file's target `cuspguard`).

On the cusp branch `i = q−2` (parametrize `q = m+4`, so `q−2 = m+2`, `q−3 = m+1`, `q−4 = m`), the
three cusp guards (G1) `l a + (l²−1) b > 1`, (G2) `l a + b > 1`, (G3) `a + l b ≤ 1` are EXACTLY the
branch entry/active predicate plus the Taha lower edge.  The bridge is two `L`-identities, obtained
by pushing the two boundary facts `cheb(m+4)=0`, `cheb(m+3)=1` down one step each via `cheb_rec`:
  `cheb(m+2) = l`        (= X(q−3)),
  `cheb(m+1) = l²−1`     (= X(q−4)),
whence
  `L_{m+2} = a·cheb(m+3) + b·cheb(m+2) = a·1 + b·l = a + l b`,
  `L_{m+1} = a·cheb(m+2) + b·cheb(m+1) = a·l + b·(l²−1) = l a + (l²−1) b`.
So `hactive : L_{m+2} ≤ 1` IS (G3), `hentry : 1 < L_{m+1}` IS (G1), and `htaha : 1 − l a < b` IS (G2).
-/

/-- **Cusp boundary, step 1.**  From `cheb(m+4)=0`, `cheb(m+3)=1` and `cheb_rec`, `cheb(m+2)=l`
(= `X(q−3)`). -/
theorem cheb_cusp_m2 (m : ℕ) (hq0 : cheb l (m + 4) = 0) (hq1 : cheb l (m + 3) = 1) :
    cheb l (m + 2) = l := by
  have hrec : cheb l (m + 4) = l * cheb l (m + 3) - cheb l (m + 2) := cheb_rec l (m + 2)
  rw [hq0, hq1] at hrec
  linarith

/-- **Cusp boundary, step 2.**  From `cheb(m+3)=1`, `cheb(m+2)=l` and `cheb_rec`, `cheb(m+1)=l²−1`
(= `X(q−4)`). -/
theorem cheb_cusp_m1 (m : ℕ) (hq1 : cheb l (m + 3) = 1) (hm2 : cheb l (m + 2) = l) :
    cheb l (m + 1) = l ^ 2 - 1 := by
  have hrec : cheb l (m + 3) = l * cheb l (m + 2) - cheb l (m + 1) := cheb_rec l (m + 1)
  rw [hq1, hm2] at hrec
  nlinarith [hrec]

/-- **Cusp `L`-identity at the active branch `q−2 = m+2`.**  `L_{m+2} = a + l b`.  Derived from the
boundary `cheb(m+3)=1`, `cheb(m+2)=l`. -/
theorem L_cusp_active (a b : ℝ) (m : ℕ)
    (hq1 : cheb l (m + 3) = 1) (hm2 : cheb l (m + 2) = l) :
    L l a b (m + 2) = a + l * b := by
  simp only [L, show m + 2 + 1 = m + 3 from rfl, hq1, hm2]; ring

/-- **Cusp `L`-identity at the entry branch `q−3 = m+1`.**  `L_{m+1} = l a + (l²−1) b`.  Derived from
`cheb(m+2)=l`, `cheb(m+1)=l²−1`. -/
theorem L_cusp_entry (a b : ℝ) (m : ℕ)
    (hm2 : cheb l (m + 2) = l) (hm1 : cheb l (m + 1) = l ^ 2 - 1) :
    L l a b (m + 1) = l * a + (l ^ 2 - 1) * b := by
  simp only [L, show m + 1 + 1 = m + 2 from rfl, hm2, hm1]; ring

/-- **CUSP-GUARD MEMBERSHIP (closes residual G3).**  On the cusp branch `i = q−2 = m+2`, given the
two boundary facts `cheb(m+4)=0`, `cheb(m+3)=1` (the principal Hecke root, `λ = 2cos(π/q)` encoded
algebraically), the branch entry predicate `1 < L_{m+1}`, the branch active predicate `L_{m+2} ≤ 1`,
and the Taha lower edge `1 − l a < b`, the three cusp guards hold:
  (G1) `l a + (l²−1) b > 1`,   (G2) `l a + b > 1`,   (G3) `a + l b ≤ 1`.
Each is immediate once the two `L`-identities are in hand: (G1) is `hentry` rewritten by
`L_cusp_entry`, (G3) is `hactive` rewritten by `L_cusp_active`, (G2) is the Taha edge `htaha`. -/
theorem cusp_guards_of_branch (a b : ℝ) (m : ℕ)
    (hq0 : cheb l (m + 4) = 0) (hq1 : cheb l (m + 3) = 1)
    (hentry : 1 < L l a b (m + 1)) (hactive : L l a b (m + 2) ≤ 1)
    (htaha : 1 - l * a < b) :
    l * a + (l ^ 2 - 1) * b > 1 ∧ l * a + b > 1 ∧ a + l * b ≤ 1 := by
  -- boundary cheb-values one step down each
  have hm2 : cheb l (m + 2) = l := cheb_cusp_m2 l m hq0 hq1
  have hm1 : cheb l (m + 1) = l ^ 2 - 1 := cheb_cusp_m1 l m hq1 hm2
  -- the two L-identities
  have hLa : L l a b (m + 2) = a + l * b := L_cusp_active l a b m hq1 hm2
  have hLe : L l a b (m + 1) = l * a + (l ^ 2 - 1) * b := L_cusp_entry l a b m hm2 hm1
  refine ⟨?_, ?_, ?_⟩
  · -- (G1): entry predicate
    rw [hLe] at hentry; linarith
  · -- (G2): Taha lower edge
    linarith [htaha]
  · -- (G3): active predicate
    rw [hLa] at hactive; linarith

/-- **CUSP MEMBERSHIP ⟹ genuine kick bound** (the key G3 result, feeding `kick_bound_of_cusp`).
On the cusp branch `i = q−2 = m+2`, with the two boundary facts, the entry/active branch predicates,
the Taha lower edge, the cusp `a`-domain `0 < a ≤ 1`, and `l ≥ φ` (`l > 1`, `l² ≥ l+1`), the genuine
observable satisfies `Pgen (a,b) ≥ 1/l³`.  Proof: `cusp_guards_of_branch` supplies the three guards,
which together with `0<a≤1` form the `hcuspGuards` bundle `kick_bound_of_cusp` consumes. -/
theorem kick_bound_of_branch (a b : ℝ) (m : ℕ)
    (hl1 : 1 < l) (hlphi : l ^ 2 ≥ l + 1)
    (ha : 0 < a) (ha1 : a ≤ 1)
    (hq0 : cheb l (m + 4) = 0) (hq1 : cheb l (m + 3) = 1)
    (hentry : 1 < L l a b (m + 1)) (hactive : L l a b (m + 2) ≤ 1)
    (htaha : 1 - l * a < b) :
    1 / l ^ 3 ≤ Pgen l (a, b) := by
  obtain ⟨hG1, hG2, hG3⟩ := cusp_guards_of_branch l a b m hq0 hq1 hentry hactive htaha
  exact kick_bound_of_cusp hl1 hlphi ⟨ha, ha1, hG1, hG2, hG3⟩

-- ===== TRACK genmapdef =====
/-! ## §11. THE GENUINE PIECEWISE STEP `genStep` (target `genmapdef`).

The genuine multi-branch generator, restricted to its action on the active branch:
* the SELECTOR picks the active branch `i = branchIdx l a b h` (least `i≥1` with `L_i ≤ 1`);
* on that branch the genuine Hecke–BCZ step emits the scalar-branch successor coordinate pair
  `(a', b') = (succA l a b i, succB l a b i k) = (L_i, L_{i+1} + k λ L_i)` (handoff §1, §4).

`genStep` packages exactly that: `genStep a b k h = (L_i, L_{i+1} + kλL_i)` at `i = branchIdx`.
Below: (a) `genStep_fst` — the requested SANITY link, the first successor coordinate IS `L_i`
(the scalar-`Tmap`-on-branch-`i` first coordinate); (b) `genStep_fst_le_one` — a non-trivial
property: that first coordinate inherits the active band `≤ 1` from the selector spec; and
(c) `genStep_prod` — the genuine successor observable `a'·b' = L_i L_{i+1} + kλ L_i²`. -/

open Classical in
/-- **The genuine piecewise step** (selector + scalar-branch successor).  At floor `k`, pick the
active branch `i = branchIdx l a b h` and emit `(a', b') = (succA l a b i, succB l a b i k)`. -/
noncomputable def genStep (a b k : ℝ) (h : ∃ i, 1 ≤ i ∧ L l a b i ≤ 1) : ℝ × ℝ :=
  (succA l a b (branchIdx l a b h), succB l a b (branchIdx l a b h) k)

/-- **SANITY (the requested link).**  On the active branch `i = branchIdx`, the genuine step's
FIRST successor coordinate is exactly `L_i` — i.e. the scalar `Tmap`-on-branch-`i` first coordinate
`a' = L_i` (handoff §1, §4 `succA`).  This is the faithful link between the genuine multi-branch
`genStep` and the per-branch scalar successor. -/
theorem genStep_fst (a b k : ℝ) (h : ∃ i, 1 ≤ i ∧ L l a b i ≤ 1) :
    (genStep l a b k h).1 = L l a b (branchIdx l a b h) := by
  simp only [genStep, succA]

/-- The genuine step's SECOND successor coordinate is `L_{i+1} + k λ L_i` at `i = branchIdx`
(the `succB` of the active branch). -/
theorem genStep_snd (a b k : ℝ) (h : ∃ i, 1 ≤ i ∧ L l a b i ≤ 1) :
    (genStep l a b k h).2
      = L l a b (branchIdx l a b h + 1) + k * l * L l a b (branchIdx l a b h) := by
  simp only [genStep, succB]

/-- **Non-trivial sanity.**  The genuine step's first successor coordinate inherits the *active
band* `a' ≤ 1` from the branch selector: since `genStep.1 = L_i` and `branchIdx_spec` certifies
`L_i ≤ 1` at the selected branch, the emitted `a'` lands `≤ 1`.  (Uses `branchIdx_spec`, not just the
definitional unfolding.) -/
theorem genStep_fst_le_one (a b k : ℝ) (h : ∃ i, 1 ≤ i ∧ L l a b i ≤ 1) :
    (genStep l a b k h).1 ≤ 1 := by
  rw [genStep_fst]
  exact (branchIdx_spec l a b h).2.1

/-- **Non-trivial sanity.**  The genuine successor OBSERVABLE (product of the two emitted
coordinates) on the active branch `i = branchIdx` equals `L_i·L_{i+1} + k λ L_i²` — the genuine
deep-mid product `a'·b'` of handoff §4, expressed in the branch linear forms.  Pure algebra after
unfolding the selector. -/
theorem genStep_prod (a b k : ℝ) (h : ∃ i, 1 ≤ i ∧ L l a b i ≤ 1) :
    (genStep l a b k h).1 * (genStep l a b k h).2
      = L l a b (branchIdx l a b h) * L l a b (branchIdx l a b h + 1)
        + k * l * (L l a b (branchIdx l a b h)) ^ 2 := by
  rw [genStep_fst, genStep_snd]; ring

-- ===== TRACK boxcontain =====
/-! ## §11. BOX-CONTAINMENT (q=16..21): the deep-mid genuine parameters lie in the ejection box.

`ejection_kick` / `genuine_ejection` consume `l ∈ [49/25, 99/50]` and `thr = 1/l³ ∈
[129/1000, 663/5000]`.  Here we close the **l → thr** containment and, for each q=16..21, the
**algebraic encoding → l-window** containment.

ADVERSARIAL-HONESTY NOTE: the nominal `l`-range `[49/25, 99/50] = [1.96, 1.98]` is NOT tight enough
to force `thr ∈ box` — the box endpoints require `l ≥ (5000/663)^(1/3) = 1.96104` and
`l ≤ (1000/129)^(1/3) = 1.97911`, so `49/25` and `99/50` FAIL the cube bound at the corners.  The
genuine `l = 2cos(π/q)` for q=16..21 actually lies in `[1.96157, 1.97766] ⊂
[4903/2500, 989/500] = [1.9612, 1.978]`, which DOES yield the box.  All results below therefore use
the tight window `[4903/2500, 989/500]`. -/

/-- **thr from the (tight) l-window.**  For `4903/2500 ≤ l ≤ 989/500`, `thr = 1/l³ ∈ box
`[129/1000, 663/5000]`. -/
theorem thr_in_box_of_lwin {l : ℝ} (hlo : (4903:ℝ)/2500 ≤ l) (hhi : l ≤ (989:ℝ)/500) :
    (129:ℝ)/1000 ≤ 1 / l ^ 3 ∧ 1 / l ^ 3 ≤ (663:ℝ)/5000 := by
  have hlpos : (0:ℝ) < l := by linarith
  have hl3pos : (0:ℝ) < l ^ 3 := by positivity
  refine ⟨?_, ?_⟩
  · rw [le_div_iff₀ hl3pos]
    nlinarith [hhi, hlo, hlpos, sq_nonneg l, mul_pos hlpos hlpos]
  · rw [div_le_iff₀ hl3pos]
    nlinarith [hlo, hhi, hlpos, sq_nonneg l, mul_pos hlpos hlpos]

set_option maxHeartbeats 1600000 in
/-- **l-window for q=16 from the genuine `cheb` encoding** (handoff §1).  Hyps: algebraic
Hecke-root boundary data `cheb l 16 = 0` (= X(15)=0) and `cheb l 15 = 1` (= X(14)=1, the
principal root), plus principal-root localization `181/100 < l < 2` (the deep-mid genuine parameter
is the LARGEST common root of the two boundary polynomials; the next common root is ≤ 1.8019 < 1.81
for all q=16..21).  Conclusion: TIGHT window `4903/2500 ≤ l ≤ 989/500`.  Certificate: unfold `cheb`
to explicit polynomials; `g(l) = gcd(cheb l 16, cheb l 15 − 1)` (deg 8) is a Bezout
combination, so `g(l)=0`; factor `g = g(989/500)+(l−989/500)·D` (`D>0,g(989/500)>0`; upper) and
`g = g(4903/2500)+(l−4903/2500)·E` (`E>0,g(4903/2500)<0`; lower). -/
theorem cheb_lwin_q16 (l : ℝ)
    (hq0 : cheb l 16 = 0) (hq1 : cheb l 15 = 1)
    (hlo : (181:ℝ)/100 < l) (hhi : l < 2) :
    (4903:ℝ)/2500 ≤ l ∧ l ≤ (989:ℝ)/500 := by
  have hlpos : (0:ℝ) < l := by linarith
  have eq0 : cheb l 16 = l^15 + (-14:ℝ)*l^13 + (78:ℝ)*l^11 + (-220:ℝ)*l^9 + (330:ℝ)*l^7 + (-252:ℝ)*l^5 + (84:ℝ)*l^3 + (-8:ℝ)*l := by simp only [cheb]; ring
  have eq1 : cheb l 15 = l^14 + (-13:ℝ)*l^12 + (66:ℝ)*l^10 + (-165:ℝ)*l^8 + (210:ℝ)*l^6 + (-126:ℝ)*l^4 + (28:ℝ)*l^2 + (-1:ℝ) := by simp only [cheb]; ring
  have hp0 : (l^15 + (-14:ℝ)*l^13 + (78:ℝ)*l^11 + (-220:ℝ)*l^9 + (330:ℝ)*l^7 + (-252:ℝ)*l^5 + (84:ℝ)*l^3 + (-8:ℝ)*l) = 0 := by rw [← eq0]; exact hq0
  have hp1 : (l^14 + (-13:ℝ)*l^12 + (66:ℝ)*l^10 + (-165:ℝ)*l^8 + (210:ℝ)*l^6 + (-126:ℝ)*l^4 + (28:ℝ)*l^2 + (-1:ℝ)) = 1 := by rw [← eq1]; exact hq1
  have hg : (l^8 + (-8:ℝ)*l^6 + (20:ℝ)*l^4 + (-16:ℝ)*l^2 + (2:ℝ)) = 0 := by linear_combination (-l^5 + (4:ℝ)*l^3 + (-3:ℝ)*l) * hp0 + (l^6 + (-5:ℝ)*l^4 + (6:ℝ)*l^2 + (-1:ℝ)) * hp1
  refine ⟨?_, ?_⟩
  · by_contra hc
    push_neg at hc
    have hE : (0:ℝ) < l^7 + ((4903:ℝ)/2500)*l^6 + ((-25960591:ℝ)/6250000)*l^5 + ((-127284777673:ℝ)/15625000000)*l^4 + ((157172735069281:ℝ)/39062500000000)*l^3 + ((770617920044684743:ℝ)/97656250000000000)*l^2 + ((-127910338020910705071:ℝ)/244140625000000000000)*l + (-627144387316525186963113:ℝ)/610351562500000000000000 := by nlinarith [hlo, hhi, hlpos, mul_pos hlpos hlpos, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (show (0:ℝ) ≤ l by linarith), mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (show (0:ℝ) ≤ l by linarith), mul_pos (mul_pos hlpos hlpos) hlpos, pow_pos hlpos 3, pow_pos hlpos 4, pow_pos hlpos 5, pow_pos hlpos 6, pow_pos hlpos 7, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 3).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 3).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 4).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 4).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 5).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 5).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 6).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 6).le]
    nlinarith [hg, mul_neg_of_neg_of_pos (show l - 4903/2500 < 0 by linarith) hE]
  · by_contra hc
    push_neg at hc
    have hD : (0:ℝ) < l^7 + ((989:ℝ)/500)*l^6 + ((-1021879:ℝ)/250000)*l^5 + ((-1010638331:ℝ)/125000000)*l^4 + ((250478690641:ℝ)/62500000000)*l^3 + ((247723425043949:ℝ)/31250000000000)*l^2 + ((-5001532631534439:ℝ)/15625000000000000)*l + (-4946515772587560171:ℝ)/7812500000000000000 := by nlinarith [hlo, hhi, hlpos, mul_pos hlpos hlpos, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (show (0:ℝ) ≤ l by linarith), mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (show (0:ℝ) ≤ l by linarith), mul_pos (mul_pos hlpos hlpos) hlpos, pow_pos hlpos 3, pow_pos hlpos 4, pow_pos hlpos 5, pow_pos hlpos 6, pow_pos hlpos 7, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 3).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 3).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 4).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 4).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 5).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 5).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 6).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 6).le]
    nlinarith [hg, mul_pos (show (0:ℝ) < l - 989/500 by linarith) hD]

set_option maxHeartbeats 1600000 in
/-- **l-window for q=17 from the genuine `cheb` encoding** (handoff §1).  Hyps: algebraic
Hecke-root boundary data `cheb l 17 = 0` (= X(16)=0) and `cheb l 16 = 1` (= X(15)=1, the
principal root), plus principal-root localization `181/100 < l < 2` (the deep-mid genuine parameter
is the LARGEST common root of the two boundary polynomials; the next common root is ≤ 1.8019 < 1.81
for all q=16..21).  Conclusion: TIGHT window `4903/2500 ≤ l ≤ 989/500`.  Certificate: unfold `cheb`
to explicit polynomials; `g(l) = gcd(cheb l 17, cheb l 16 − 1)` (deg 8) is a Bezout
combination, so `g(l)=0`; factor `g = g(989/500)+(l−989/500)·D` (`D>0,g(989/500)>0`; upper) and
`g = g(4903/2500)+(l−4903/2500)·E` (`E>0,g(4903/2500)<0`; lower). -/
theorem cheb_lwin_q17 (l : ℝ)
    (hq0 : cheb l 17 = 0) (hq1 : cheb l 16 = 1)
    (hlo : (181:ℝ)/100 < l) (hhi : l < 2) :
    (4903:ℝ)/2500 ≤ l ∧ l ≤ (989:ℝ)/500 := by
  have hlpos : (0:ℝ) < l := by linarith
  have eq0 : cheb l 17 = l^16 + (-15:ℝ)*l^14 + (91:ℝ)*l^12 + (-286:ℝ)*l^10 + (495:ℝ)*l^8 + (-462:ℝ)*l^6 + (210:ℝ)*l^4 + (-36:ℝ)*l^2 + (1:ℝ) := by simp only [cheb]; ring
  have eq1 : cheb l 16 = l^15 + (-14:ℝ)*l^13 + (78:ℝ)*l^11 + (-220:ℝ)*l^9 + (330:ℝ)*l^7 + (-252:ℝ)*l^5 + (84:ℝ)*l^3 + (-8:ℝ)*l := by simp only [cheb]; ring
  have hp0 : (l^16 + (-15:ℝ)*l^14 + (91:ℝ)*l^12 + (-286:ℝ)*l^10 + (495:ℝ)*l^8 + (-462:ℝ)*l^6 + (210:ℝ)*l^4 + (-36:ℝ)*l^2 + (1:ℝ)) = 0 := by rw [← eq0]; exact hq0
  have hp1 : (l^15 + (-14:ℝ)*l^13 + (78:ℝ)*l^11 + (-220:ℝ)*l^9 + (330:ℝ)*l^7 + (-252:ℝ)*l^5 + (84:ℝ)*l^3 + (-8:ℝ)*l) = 1 := by rw [← eq1]; exact hq1
  have hg : (l^8 - l^7 + (-7:ℝ)*l^6 + (6:ℝ)*l^5 + (15:ℝ)*l^4 + (-10:ℝ)*l^3 + (-10:ℝ)*l^2 + (4:ℝ)*l + (1:ℝ)) = 0 := by linear_combination (-l^6 + (5:ℝ)*l^4 + (-6:ℝ)*l^2 + (1:ℝ)) * hp0 + (l^7 + (-6:ℝ)*l^5 + (10:ℝ)*l^3 + (-4:ℝ)*l) * hp1
  refine ⟨?_, ?_⟩
  · by_contra hc
    push_neg at hc
    have hE : (0:ℝ) < l^7 + ((2403:ℝ)/2500)*l^6 + ((-31968091:ℝ)/6250000)*l^5 + ((-62989550173:ℝ)/15625000000)*l^4 + ((277099735501781:ℝ)/39062500000000)*l^3 + ((382057503165232243:ℝ)/97656250000000000)*l^2 + ((-568178311980866312571:ℝ)/244140625000000000000)*l + (-344372013642187530535613:ℝ)/610351562500000000000000 := by nlinarith [hlo, hhi, hlpos, mul_pos hlpos hlpos, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (show (0:ℝ) ≤ l by linarith), mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (show (0:ℝ) ≤ l by linarith), mul_pos (mul_pos hlpos hlpos) hlpos, pow_pos hlpos 3, pow_pos hlpos 4, pow_pos hlpos 5, pow_pos hlpos 6, pow_pos hlpos 7, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 3).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 3).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 4).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 4).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 5).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 5).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 6).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 6).le]
    nlinarith [hg, mul_neg_of_neg_of_pos (show l - 4903/2500 < 0 by linarith) hE]
  · by_contra hc
    push_neg at hc
    have hD : (0:ℝ) < l^7 + ((489:ℝ)/500)*l^6 + ((-1266379:ℝ)/250000)*l^5 + ((-502448831:ℝ)/125000000)*l^4 + ((440578106141:ℝ)/62500000000)*l^3 + ((123231746973449:ℝ)/31250000000000)*l^2 + ((-34373802243258939:ℝ)/15625000000000000)*l + (-2745690418583090671:ℝ)/7812500000000000000 := by nlinarith [hlo, hhi, hlpos, mul_pos hlpos hlpos, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (show (0:ℝ) ≤ l by linarith), mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (show (0:ℝ) ≤ l by linarith), mul_pos (mul_pos hlpos hlpos) hlpos, pow_pos hlpos 3, pow_pos hlpos 4, pow_pos hlpos 5, pow_pos hlpos 6, pow_pos hlpos 7, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 3).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 3).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 4).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 4).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 5).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 5).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 6).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 6).le]
    nlinarith [hg, mul_pos (show (0:ℝ) < l - 989/500 by linarith) hD]

set_option maxHeartbeats 1600000 in
/-- **l-window for q=18 from the genuine `cheb` encoding** (handoff §1).  Hyps: algebraic
Hecke-root boundary data `cheb l 18 = 0` (= X(17)=0) and `cheb l 17 = 1` (= X(16)=1, the
principal root), plus principal-root localization `181/100 < l < 2` (the deep-mid genuine parameter
is the LARGEST common root of the two boundary polynomials; the next common root is ≤ 1.8019 < 1.81
for all q=16..21).  Conclusion: TIGHT window `4903/2500 ≤ l ≤ 989/500`.  Certificate: unfold `cheb`
to explicit polynomials; `g(l) = gcd(cheb l 18, cheb l 17 − 1)` (deg 9) is a Bezout
combination, so `g(l)=0`; factor `g = g(989/500)+(l−989/500)·D` (`D>0,g(989/500)>0`; upper) and
`g = g(4903/2500)+(l−4903/2500)·E` (`E>0,g(4903/2500)<0`; lower). -/
theorem cheb_lwin_q18 (l : ℝ)
    (hq0 : cheb l 18 = 0) (hq1 : cheb l 17 = 1)
    (hlo : (181:ℝ)/100 < l) (hhi : l < 2) :
    (4903:ℝ)/2500 ≤ l ∧ l ≤ (989:ℝ)/500 := by
  have hlpos : (0:ℝ) < l := by linarith
  have eq0 : cheb l 18 = l^17 + (-16:ℝ)*l^15 + (105:ℝ)*l^13 + (-364:ℝ)*l^11 + (715:ℝ)*l^9 + (-792:ℝ)*l^7 + (462:ℝ)*l^5 + (-120:ℝ)*l^3 + (9:ℝ)*l := by simp only [cheb]; ring
  have eq1 : cheb l 17 = l^16 + (-15:ℝ)*l^14 + (91:ℝ)*l^12 + (-286:ℝ)*l^10 + (495:ℝ)*l^8 + (-462:ℝ)*l^6 + (210:ℝ)*l^4 + (-36:ℝ)*l^2 + (1:ℝ) := by simp only [cheb]; ring
  have hp0 : (l^17 + (-16:ℝ)*l^15 + (105:ℝ)*l^13 + (-364:ℝ)*l^11 + (715:ℝ)*l^9 + (-792:ℝ)*l^7 + (462:ℝ)*l^5 + (-120:ℝ)*l^3 + (9:ℝ)*l) = 0 := by rw [← eq0]; exact hq0
  have hp1 : (l^16 + (-15:ℝ)*l^14 + (91:ℝ)*l^12 + (-286:ℝ)*l^10 + (495:ℝ)*l^8 + (-462:ℝ)*l^6 + (210:ℝ)*l^4 + (-36:ℝ)*l^2 + (1:ℝ)) = 1 := by rw [← eq1]; exact hq1
  have hg : (l^9 + (-9:ℝ)*l^7 + (27:ℝ)*l^5 + (-30:ℝ)*l^3 + (9:ℝ)*l) = 0 := by linear_combination (-l^6 + (5:ℝ)*l^4 + (-6:ℝ)*l^2 + (1:ℝ)) * hp0 + (l^7 + (-6:ℝ)*l^5 + (10:ℝ)*l^3 + (-4:ℝ)*l) * hp1
  refine ⟨?_, ?_⟩
  · by_contra hc
    push_neg at hc
    have hE : (0:ℝ) < l^8 + ((4903:ℝ)/2500)*l^7 + ((-32210591:ℝ)/6250000)*l^6 + ((-157928527673:ℝ)/15625000000)*l^5 + ((280363928819281:ℝ)/39062500000000)*l^4 + ((1374624343000934743:ℝ)/97656250000000000)*l^3 + ((-584435596266416955071:ℝ)/244140625000000000000)*l^2 + ((-2865487728494242330713113:ℝ)/610351562500000000000000)*l + (-316576176557270147486393039:ℝ)/1525878906250000000000000000 := by nlinarith [hlo, hhi, hlpos, mul_pos hlpos hlpos, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (show (0:ℝ) ≤ l by linarith), mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (show (0:ℝ) ≤ l by linarith), mul_pos (mul_pos hlpos hlpos) hlpos, pow_pos hlpos 3, pow_pos hlpos 4, pow_pos hlpos 5, pow_pos hlpos 6, pow_pos hlpos 7, pow_pos hlpos 8, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 3).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 3).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 4).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 4).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 5).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 5).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 6).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 6).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 7).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 7).le]
    nlinarith [hg, mul_neg_of_neg_of_pos (show l - 4903/2500 < 0 by linarith) hE]
  · by_contra hc
    push_neg at hc
    have hD : (0:ℝ) < l^8 + ((989:ℝ)/500)*l^7 + ((-1271879:ℝ)/250000)*l^6 + ((-1257888331:ℝ)/125000000)*l^5 + ((443448440641:ℝ)/62500000000)*l^4 + ((438570507793949:ℝ)/31250000000000)*l^3 + ((-35003767791784439:ℝ)/15625000000000000)*l^2 + ((-34618726346074810171:ℝ)/7812500000000000000)*l + (918329643732012740881:ℝ)/3906250000000000000000 := by nlinarith [hlo, hhi, hlpos, mul_pos hlpos hlpos, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (show (0:ℝ) ≤ l by linarith), mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (show (0:ℝ) ≤ l by linarith), mul_pos (mul_pos hlpos hlpos) hlpos, pow_pos hlpos 3, pow_pos hlpos 4, pow_pos hlpos 5, pow_pos hlpos 6, pow_pos hlpos 7, pow_pos hlpos 8, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 3).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 3).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 4).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 4).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 5).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 5).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 6).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 6).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 7).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 7).le]
    nlinarith [hg, mul_pos (show (0:ℝ) < l - 989/500 by linarith) hD]

set_option maxHeartbeats 1600000 in
/-- **l-window for q=19 from the genuine `cheb` encoding** (handoff §1).  Hyps: algebraic
Hecke-root boundary data `cheb l 19 = 0` (= X(18)=0) and `cheb l 18 = 1` (= X(17)=1, the
principal root), plus principal-root localization `181/100 < l < 2` (the deep-mid genuine parameter
is the LARGEST common root of the two boundary polynomials; the next common root is ≤ 1.8019 < 1.81
for all q=16..21).  Conclusion: TIGHT window `4903/2500 ≤ l ≤ 989/500`.  Certificate: unfold `cheb`
to explicit polynomials; `g(l) = gcd(cheb l 19, cheb l 18 − 1)` (deg 9) is a Bezout
combination, so `g(l)=0`; factor `g = g(989/500)+(l−989/500)·D` (`D>0,g(989/500)>0`; upper) and
`g = g(4903/2500)+(l−4903/2500)·E` (`E>0,g(4903/2500)<0`; lower). -/
theorem cheb_lwin_q19 (l : ℝ)
    (hq0 : cheb l 19 = 0) (hq1 : cheb l 18 = 1)
    (hlo : (181:ℝ)/100 < l) (hhi : l < 2) :
    (4903:ℝ)/2500 ≤ l ∧ l ≤ (989:ℝ)/500 := by
  have hlpos : (0:ℝ) < l := by linarith
  have eq0 : cheb l 19 = l^18 + (-17:ℝ)*l^16 + (120:ℝ)*l^14 + (-455:ℝ)*l^12 + (1001:ℝ)*l^10 + (-1287:ℝ)*l^8 + (924:ℝ)*l^6 + (-330:ℝ)*l^4 + (45:ℝ)*l^2 + (-1:ℝ) := by simp only [cheb]; ring
  have eq1 : cheb l 18 = l^17 + (-16:ℝ)*l^15 + (105:ℝ)*l^13 + (-364:ℝ)*l^11 + (715:ℝ)*l^9 + (-792:ℝ)*l^7 + (462:ℝ)*l^5 + (-120:ℝ)*l^3 + (9:ℝ)*l := by simp only [cheb]; ring
  have hp0 : (l^18 + (-17:ℝ)*l^16 + (120:ℝ)*l^14 + (-455:ℝ)*l^12 + (1001:ℝ)*l^10 + (-1287:ℝ)*l^8 + (924:ℝ)*l^6 + (-330:ℝ)*l^4 + (45:ℝ)*l^2 + (-1:ℝ)) = 0 := by rw [← eq0]; exact hq0
  have hp1 : (l^17 + (-16:ℝ)*l^15 + (105:ℝ)*l^13 + (-364:ℝ)*l^11 + (715:ℝ)*l^9 + (-792:ℝ)*l^7 + (462:ℝ)*l^5 + (-120:ℝ)*l^3 + (9:ℝ)*l) = 1 := by rw [← eq1]; exact hq1
  have hg : (l^9 - l^8 + (-8:ℝ)*l^7 + (7:ℝ)*l^6 + (21:ℝ)*l^5 + (-15:ℝ)*l^4 + (-20:ℝ)*l^3 + (10:ℝ)*l^2 + (5:ℝ)*l + (-1:ℝ)) = 0 := by linear_combination (-l^7 + (6:ℝ)*l^5 + (-10:ℝ)*l^3 + (4:ℝ)*l) * hp0 + (l^8 + (-7:ℝ)*l^6 + (15:ℝ)*l^4 + (-10:ℝ)*l^2 + (1:ℝ)) * hp1
  refine ⟨?_, ?_⟩
  · by_contra hc
    push_neg at hc
    have hE : (0:ℝ) < l^8 + ((2403:ℝ)/2500)*l^7 + ((-38218091:ℝ)/6250000)*l^6 + ((-78008300173:ℝ)/15625000000)*l^5 + ((437837804251781:ℝ)/39062500000000)*l^4 + ((681875004246482243:ℝ)/97656250000000000)*l^3 + ((-1539579354179497562571:ℝ)/244140625000000000000)*l^2 + ((-1445041948542076549285613:ℝ)/610351562500000000000000)*l + (544353857548198678852639461:ℝ)/1525878906250000000000000000 := by nlinarith [hlo, hhi, hlpos, mul_pos hlpos hlpos, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (show (0:ℝ) ≤ l by linarith), mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (show (0:ℝ) ≤ l by linarith), mul_pos (mul_pos hlpos hlpos) hlpos, pow_pos hlpos 3, pow_pos hlpos 4, pow_pos hlpos 5, pow_pos hlpos 6, pow_pos hlpos 7, pow_pos hlpos 8, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 3).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 3).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 4).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 4).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 5).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 5).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 6).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 6).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 7).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 7).le]
    nlinarith [hg, mul_neg_of_neg_of_pos (show l - 4903/2500 < 0 by linarith) hE]
  · by_contra hc
    push_neg at hc
    have hD : (0:ℝ) < l^8 + ((489:ℝ)/500)*l^7 + ((-1516379:ℝ)/250000)*l^6 + ((-624698831:ℝ)/125000000)*l^5 + ((694672856141:ℝ)/62500000000)*l^4 + ((218281454723449:ℝ)/31250000000000)*l^3 + ((-96619641278508939:ℝ)/15625000000000000)*l^2 + ((-17431825224445340671:ℝ)/7812500000000000000)*l + (2291174853023558076381:ℝ)/3906250000000000000000 := by nlinarith [hlo, hhi, hlpos, mul_pos hlpos hlpos, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (show (0:ℝ) ≤ l by linarith), mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (show (0:ℝ) ≤ l by linarith), mul_pos (mul_pos hlpos hlpos) hlpos, pow_pos hlpos 3, pow_pos hlpos 4, pow_pos hlpos 5, pow_pos hlpos 6, pow_pos hlpos 7, pow_pos hlpos 8, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 3).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 3).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 4).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 4).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 5).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 5).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 6).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 6).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 7).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 7).le]
    nlinarith [hg, mul_pos (show (0:ℝ) < l - 989/500 by linarith) hD]

set_option maxHeartbeats 1600000 in
/-- **l-window for q=20 from the genuine `cheb` encoding** (handoff §1).  Hyps: algebraic
Hecke-root boundary data `cheb l 20 = 0` (= X(19)=0) and `cheb l 19 = 1` (= X(18)=1, the
principal root), plus principal-root localization `181/100 < l < 2` (the deep-mid genuine parameter
is the LARGEST common root of the two boundary polynomials; the next common root is ≤ 1.8019 < 1.81
for all q=16..21).  Conclusion: TIGHT window `4903/2500 ≤ l ≤ 989/500`.  Certificate: unfold `cheb`
to explicit polynomials; `g(l) = gcd(cheb l 20, cheb l 19 − 1)` (deg 10) is a Bezout
combination, so `g(l)=0`; factor `g = g(989/500)+(l−989/500)·D` (`D>0,g(989/500)>0`; upper) and
`g = g(4903/2500)+(l−4903/2500)·E` (`E>0,g(4903/2500)<0`; lower). -/
theorem cheb_lwin_q20 (l : ℝ)
    (hq0 : cheb l 20 = 0) (hq1 : cheb l 19 = 1)
    (hlo : (181:ℝ)/100 < l) (hhi : l < 2) :
    (4903:ℝ)/2500 ≤ l ∧ l ≤ (989:ℝ)/500 := by
  have hlpos : (0:ℝ) < l := by linarith
  have eq0 : cheb l 20 = l^19 + (-18:ℝ)*l^17 + (136:ℝ)*l^15 + (-560:ℝ)*l^13 + (1365:ℝ)*l^11 + (-2002:ℝ)*l^9 + (1716:ℝ)*l^7 + (-792:ℝ)*l^5 + (165:ℝ)*l^3 + (-10:ℝ)*l := by simp only [cheb]; ring
  have eq1 : cheb l 19 = l^18 + (-17:ℝ)*l^16 + (120:ℝ)*l^14 + (-455:ℝ)*l^12 + (1001:ℝ)*l^10 + (-1287:ℝ)*l^8 + (924:ℝ)*l^6 + (-330:ℝ)*l^4 + (45:ℝ)*l^2 + (-1:ℝ) := by simp only [cheb]; ring
  have hp0 : (l^19 + (-18:ℝ)*l^17 + (136:ℝ)*l^15 + (-560:ℝ)*l^13 + (1365:ℝ)*l^11 + (-2002:ℝ)*l^9 + (1716:ℝ)*l^7 + (-792:ℝ)*l^5 + (165:ℝ)*l^3 + (-10:ℝ)*l) = 0 := by rw [← eq0]; exact hq0
  have hp1 : (l^18 + (-17:ℝ)*l^16 + (120:ℝ)*l^14 + (-455:ℝ)*l^12 + (1001:ℝ)*l^10 + (-1287:ℝ)*l^8 + (924:ℝ)*l^6 + (-330:ℝ)*l^4 + (45:ℝ)*l^2 + (-1:ℝ)) = 1 := by rw [← eq1]; exact hq1
  have hg : (l^10 + (-10:ℝ)*l^8 + (35:ℝ)*l^6 + (-50:ℝ)*l^4 + (25:ℝ)*l^2 + (-2:ℝ)) = 0 := by linear_combination (-l^7 + (6:ℝ)*l^5 + (-10:ℝ)*l^3 + (4:ℝ)*l) * hp0 + (l^8 + (-7:ℝ)*l^6 + (15:ℝ)*l^4 + (-10:ℝ)*l^2 + (1:ℝ)) * hp1
  refine ⟨?_, ?_⟩
  · by_contra hc
    push_neg at hc
    have hE : (0:ℝ) < l^9 + ((4903:ℝ)/2500)*l^8 + ((-38460591:ℝ)/6250000)*l^7 + ((-188572277673:ℝ)/15625000000)*l^6 + ((442617622569281:ℝ)/39062500000000)*l^5 + ((2170154203457184743:ℝ)/97656250000000000)*l^4 + ((-1566765190449423205071:ℝ)/244140625000000000000)*l^3 + ((-7681849728773521974463113:ℝ)/610351562500000000000000)*l^2 + ((482863436073421759207356961:ℝ)/1525878906250000000000000000)*l + (2367479427067986885393671179783:ℝ)/3814697265625000000000000000000 := by nlinarith [hlo, hhi, hlpos, mul_pos hlpos hlpos, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (show (0:ℝ) ≤ l by linarith), mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (show (0:ℝ) ≤ l by linarith), mul_pos (mul_pos hlpos hlpos) hlpos, pow_pos hlpos 3, pow_pos hlpos 4, pow_pos hlpos 5, pow_pos hlpos 6, pow_pos hlpos 7, pow_pos hlpos 8, pow_pos hlpos 9, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 3).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 3).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 4).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 4).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 5).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 5).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 6).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 6).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 7).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 7).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 8).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 8).le]
    nlinarith [hg, mul_neg_of_neg_of_pos (show l - 4903/2500 < 0 by linarith) hE]
  · by_contra hc
    push_neg at hc
    have hD : (0:ℝ) < l^9 + ((989:ℝ)/500)*l^8 + ((-1521879:ℝ)/250000)*l^7 + ((-1505138331:ℝ)/125000000)*l^6 + ((698918190641:ℝ)/62500000000)*l^5 + ((691230090543949:ℝ)/31250000000000)*l^4 + ((-97623440452034439:ℝ)/15625000000000000)*l^3 + ((-96549582607062060171:ℝ)/7812500000000000000)*l^2 + ((2168712801615622490881:ℝ)/3906250000000000000000)*l + (2144856960797850643481309:ℝ)/1953125000000000000000000 := by nlinarith [hlo, hhi, hlpos, mul_pos hlpos hlpos, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (show (0:ℝ) ≤ l by linarith), mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (show (0:ℝ) ≤ l by linarith), mul_pos (mul_pos hlpos hlpos) hlpos, pow_pos hlpos 3, pow_pos hlpos 4, pow_pos hlpos 5, pow_pos hlpos 6, pow_pos hlpos 7, pow_pos hlpos 8, pow_pos hlpos 9, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 3).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 3).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 4).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 4).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 5).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 5).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 6).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 6).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 7).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 7).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 8).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 8).le]
    nlinarith [hg, mul_pos (show (0:ℝ) < l - 989/500 by linarith) hD]

set_option maxHeartbeats 1600000 in
/-- **l-window for q=21 from the genuine `cheb` encoding** (handoff §1).  Hyps: algebraic
Hecke-root boundary data `cheb l 21 = 0` (= X(20)=0) and `cheb l 20 = 1` (= X(19)=1, the
principal root), plus principal-root localization `181/100 < l < 2` (the deep-mid genuine parameter
is the LARGEST common root of the two boundary polynomials; the next common root is ≤ 1.8019 < 1.81
for all q=16..21).  Conclusion: TIGHT window `4903/2500 ≤ l ≤ 989/500`.  Certificate: unfold `cheb`
to explicit polynomials; `g(l) = gcd(cheb l 21, cheb l 20 − 1)` (deg 10) is a Bezout
combination, so `g(l)=0`; factor `g = g(989/500)+(l−989/500)·D` (`D>0,g(989/500)>0`; upper) and
`g = g(4903/2500)+(l−4903/2500)·E` (`E>0,g(4903/2500)<0`; lower). -/
theorem cheb_lwin_q21 (l : ℝ)
    (hq0 : cheb l 21 = 0) (hq1 : cheb l 20 = 1)
    (hlo : (181:ℝ)/100 < l) (hhi : l < 2) :
    (4903:ℝ)/2500 ≤ l ∧ l ≤ (989:ℝ)/500 := by
  have hlpos : (0:ℝ) < l := by linarith
  have eq0 : cheb l 21 = l^20 + (-19:ℝ)*l^18 + (153:ℝ)*l^16 + (-680:ℝ)*l^14 + (1820:ℝ)*l^12 + (-3003:ℝ)*l^10 + (3003:ℝ)*l^8 + (-1716:ℝ)*l^6 + (495:ℝ)*l^4 + (-55:ℝ)*l^2 + (1:ℝ) := by simp only [cheb]; ring
  have eq1 : cheb l 20 = l^19 + (-18:ℝ)*l^17 + (136:ℝ)*l^15 + (-560:ℝ)*l^13 + (1365:ℝ)*l^11 + (-2002:ℝ)*l^9 + (1716:ℝ)*l^7 + (-792:ℝ)*l^5 + (165:ℝ)*l^3 + (-10:ℝ)*l := by simp only [cheb]; ring
  have hp0 : (l^20 + (-19:ℝ)*l^18 + (153:ℝ)*l^16 + (-680:ℝ)*l^14 + (1820:ℝ)*l^12 + (-3003:ℝ)*l^10 + (3003:ℝ)*l^8 + (-1716:ℝ)*l^6 + (495:ℝ)*l^4 + (-55:ℝ)*l^2 + (1:ℝ)) = 0 := by rw [← eq0]; exact hq0
  have hp1 : (l^19 + (-18:ℝ)*l^17 + (136:ℝ)*l^15 + (-560:ℝ)*l^13 + (1365:ℝ)*l^11 + (-2002:ℝ)*l^9 + (1716:ℝ)*l^7 + (-792:ℝ)*l^5 + (165:ℝ)*l^3 + (-10:ℝ)*l) = 1 := by rw [← eq1]; exact hq1
  have hg : (l^10 - l^9 + (-9:ℝ)*l^8 + (8:ℝ)*l^7 + (28:ℝ)*l^6 + (-21:ℝ)*l^5 + (-35:ℝ)*l^4 + (20:ℝ)*l^3 + (15:ℝ)*l^2 + (-5:ℝ)*l + (-1:ℝ)) = 0 := by linear_combination (-l^8 + (7:ℝ)*l^6 + (-15:ℝ)*l^4 + (10:ℝ)*l^2 + (-1:ℝ)) * hp0 + (l^9 + (-8:ℝ)*l^7 + (21:ℝ)*l^5 + (-20:ℝ)*l^3 + (5:ℝ)*l) * hp1
  refine ⟨?_, ?_⟩
  · by_contra hc
    push_neg at hc
    have hE : (0:ℝ) < l^9 + ((2403:ℝ)/2500)*l^8 + ((-44468091:ℝ)/6250000)*l^7 + ((-93027050173:ℝ)/15625000000)*l^6 + ((637638373001781:ℝ)/39062500000000)*l^5 + ((1075559692827732243:ℝ)/97656250000000000)*l^4 + ((-3271452701065628812571:ℝ)/244140625000000000000)*l^3 + ((-3832901343324778068035613:ℝ)/610351562500000000000000)*l^2 + ((4095468307428613132421389461:ℝ)/1525878906250000000000000000)*l + (1006594783197490188262072527283:ℝ)/3814697265625000000000000000000 := by nlinarith [hlo, hhi, hlpos, mul_pos hlpos hlpos, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (show (0:ℝ) ≤ l by linarith), mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (show (0:ℝ) ≤ l by linarith), mul_pos (mul_pos hlpos hlpos) hlpos, pow_pos hlpos 3, pow_pos hlpos 4, pow_pos hlpos 5, pow_pos hlpos 6, pow_pos hlpos 7, pow_pos hlpos 8, pow_pos hlpos 9, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 3).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 3).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 4).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 4).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 5).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 5).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 6).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 6).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 7).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 7).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 8).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 8).le]
    nlinarith [hg, mul_neg_of_neg_of_pos (show l - 4903/2500 < 0 by linarith) hE]
  · by_contra hc
    push_neg at hc
    have hD : (0:ℝ) < l^9 + ((489:ℝ)/500)*l^8 + ((-1766379:ℝ)/250000)*l^7 + ((-746948831:ℝ)/125000000)*l^6 + ((1011267606141:ℝ)/62500000000)*l^5 + ((343893662473449:ℝ)/31250000000000)*l^4 + ((-206764167813758939:ℝ)/15625000000000000)*l^3 + ((-48239761967807590671:ℝ)/7812500000000000000)*l^2 + ((10884625413838292826381:ℝ)/3906250000000000000000)*l + (999269534286071605290809:ℝ)/1953125000000000000000000 := by nlinarith [hlo, hhi, hlpos, mul_pos hlpos hlpos, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (show (0:ℝ) ≤ l by linarith), mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (show (0:ℝ) ≤ l by linarith), mul_pos (mul_pos hlpos hlpos) hlpos, pow_pos hlpos 3, pow_pos hlpos 4, pow_pos hlpos 5, pow_pos hlpos 6, pow_pos hlpos 7, pow_pos hlpos 8, pow_pos hlpos 9, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 3).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 3).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 4).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 4).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 5).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 5).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 6).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 6).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 7).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 7).le, mul_nonneg (show (0:ℝ) ≤ l - 181/100 by linarith) (pow_pos hlpos 8).le, mul_nonneg (show (0:ℝ) ≤ 2 - l by linarith) (pow_pos hlpos 8).le]
    nlinarith [hg, mul_pos (show (0:ℝ) < l - 989/500 by linarith) hD]

/-- **BOX-CONTAINMENT capstone (q=16, from the genuine `cheb` encoding).**  Combines `cheb_lwin_q16`
with `thr_in_box_of_lwin`: from the algebraic Hecke-root boundary data + principal-root
localization, BOTH the `l`-window AND `thr = 1/l³ ∈ [129/1000, 663/5000]` hold — the deep-mid
genuine parameter sits in the ejection box.  (Template; q=17..21 identical modulo `cheb_lwin_q{q}`.) -/
theorem box_containment_q16 (l : ℝ)
    (hq0 : cheb l 16 = 0) (hq1 : cheb l 15 = 1)
    (hlo : (181:ℝ)/100 < l) (hhi : l < 2) :
    ((4903:ℝ)/2500 ≤ l ∧ l ≤ (989:ℝ)/500) ∧
      ((129:ℝ)/1000 ≤ 1 / l ^ 3 ∧ 1 / l ^ 3 ≤ (663:ℝ)/5000) := by
  obtain ⟨hL, hU⟩ := cheb_lwin_q16 l hq0 hq1 hlo hhi
  exact ⟨⟨hL, hU⟩, thr_in_box_of_lwin hL hU⟩

-- ===== TRACK l1window =====

/-! ## §11. UNIFORM (L1) F-WINDOW — closed-form reduction to a single trig bound (`l1window`).

The standing all-q crux: for the floor-1 F-corridor rotation `c_n = r·cos(nJ − ψ)` with
`λ = l = 2 cos J`, `J = π/q`, the window-min functional `g(W,q) = min_{(r,ψ)} max_{n<W} c_n c_{n+1}`
over a window of length `W = ⌈q/4⌉` satisfies `g(W,q) ≥ 1/l³` for all `q ≥ 5`.

This section delivers the **clean reduction** of that crux to a single 1-D trig inequality, with the
foundational product closed form fully PROVEN, the peak-touch (LATTICE-IN / INNER) mechanism fully
PROVEN, and the trig inequality proven on the range where it holds (a concrete provable box).

HONEST SCOPE (see notes): the reduction proves the window bound *in the INNER case* — when the
window straddles the product peak (the `htouch` hypothesis) and the in-domain energy lower bound
`henergy` holds.  These two are genuine facts about the in-domain rotation (the `r ≥ r_min` envelope
and the arithmetic-progression lattice fact), supplied here as faithful hypotheses.  The OUTER case
(off-peak window configurations, which bind at `q = 18,19,20`) and the derivation of `henergy` from
the raw domain constraint are the remaining genuine work; that is where the `O(1/q²)` obstruction
lives. -/

/-- Product-to-sum: `cos x · cos y = (cos(x−y) + cos(x+y))/2`. -/
theorem prod_to_sum (x y : ℝ) :
    Real.cos x * Real.cos y = (Real.cos (x - y) + Real.cos (x + y)) / 2 := by
  rw [Real.cos_sub, Real.cos_add]; ring

/-- The floor-1 F-corridor rotation coordinate `c_n = r·cos(nJ − ψ)` (`λ = 2 cos J`, `J = π/q`). -/
noncomputable def cseq (r J psi : ℝ) (n : ℕ) : ℝ := r * Real.cos ((n : ℝ) * J - psi)

/-- The window product observable `p_n = c_n · c_{n+1}`. -/
noncomputable def pseq (r J psi : ℝ) (n : ℕ) : ℝ := cseq r J psi n * cseq r J psi (n + 1)

/-- **THE CORRIDOR PRODUCT CLOSED FORM** (the foundational trig→algebra bridge, fully proven):
`p_n = c_n c_{n+1} = (r²/2)·[cos J + cos((2n+1)J − 2ψ)]`.  Exactly the displayed closed form of the
target (`cos J = λ/2`).  Pure product-to-sum identity. -/
theorem pseq_closed (r J psi : ℝ) (n : ℕ) :
    pseq r J psi n = (r ^ 2 / 2) * (Real.cos J + Real.cos ((2 * (n : ℝ) + 1) * J - 2 * psi)) := by
  unfold pseq cseq; push_cast
  have h := prod_to_sum ((n : ℝ) * J - psi) (((n : ℝ) + 1) * J - psi)
  have e1 : ((n : ℝ) * J - psi) - (((n : ℝ) + 1) * J - psi) = -J := by ring
  have e2 : ((n : ℝ) * J - psi) + (((n : ℝ) + 1) * J - psi) = (2 * (n : ℝ) + 1) * J - 2 * psi := by
    ring
  rw [e1, e2, Real.cos_neg] at h
  calc r * Real.cos ((n : ℝ) * J - psi) * (r * Real.cos (((n : ℝ) + 1) * J - psi))
      = r ^ 2 * (Real.cos ((n : ℝ) * J - psi) * Real.cos (((n : ℝ) + 1) * J - psi)) := by ring
    _ = r ^ 2 * ((Real.cos J + Real.cos ((2 * (n : ℝ) + 1) * J - 2 * psi)) / 2) := by rw [h]
    _ = (r ^ 2 / 2) * (Real.cos J + Real.cos ((2 * (n : ℝ) + 1) * J - 2 * psi)) := by ring

/-- The window-max functional `max_{0 ≤ n < W} p_n` (the inner `max` of the `g(W,q)` functional). -/
noncomputable def winMax (r J psi : ℝ) (W : ℕ) (_hW : 0 < W) : ℝ :=
  (Finset.range W).sup' (Finset.nonempty_range_iff.mpr (by omega)) (fun n => pseq r J psi n)

/-- **PEAK-TOUCH (LATTICE-IN / INNER) bound.**  If some window index `n₀ < W` has product-phase
within `J` of a peak (`cos J ≤ cos((2n₀+1)J − 2ψ)`), then `p_{n₀} = (r²/2)(cos J + that) ≥ r² cos J`,
so the window-max is `≥ r² cos J`.  This is the load-bearing geometric mechanism: a window straddling
the product peak attains at least `r²·cos J = r²·(λ/2)`. -/
theorem winMax_ge_peak (r J psi : ℝ) (W : ℕ) (hW : 0 < W) (n0 : ℕ) (hn0 : n0 < W)
    (htouch : Real.cos J ≤ Real.cos ((2 * (n0 : ℝ) + 1) * J - 2 * psi)) :
    r ^ 2 * Real.cos J ≤ winMax r J psi W hW := by
  have hp : r ^ 2 * Real.cos J ≤ pseq r J psi n0 := by
    rw [pseq_closed]; nlinarith [htouch, sq_nonneg r]
  exact le_trans hp (Finset.le_sup' _ (Finset.mem_range.mpr hn0))

/-- **MASTER REDUCTION (INNER case): window-max ≥ 1/l³.**  Given (i) a peak-touch window index
`n₀ < W` (the LATTICE-IN geometric fact), (ii) the in-domain energy lower bound `ρ ≤ r²` (the
`r ≥ r_min` envelope squared), (iii) `cos J = l/2` (the algebraic encoding `l = 2 cos(π/q)`, `l > 0`),
and (iv) the single trig bound `1/l³ ≤ ρ·(l/2)`, the window-max clears the threshold
`1/l³`.  This is the precise reduction of the `l1window` crux (INNER case) to the trig bound. -/
theorem winMax_ge_thr (r J l psi rho : ℝ) (W : ℕ) (hW : 0 < W) (n0 : ℕ) (hn0 : n0 < W)
    (hcosJ : Real.cos J = l / 2) (hl : 0 < l)
    (htouch : Real.cos J ≤ Real.cos ((2 * (n0 : ℝ) + 1) * J - 2 * psi))
    (henergy : rho ≤ r ^ 2)
    (htrig : 1 / l ^ 3 ≤ rho * (l / 2)) :
    1 / l ^ 3 ≤ winMax r J psi W hW := by
  have hpeak := winMax_ge_peak r J psi W hW n0 hn0 htouch
  rw [hcosJ] at hpeak
  have hmono : rho * (l / 2) ≤ r ^ 2 * (l / 2) :=
    mul_le_mul_of_nonneg_right henergy (by linarith)
  linarith

/-- **TRIG-BOUND CONVERSION.**  With the explicit `r_min` envelope `ρ = 1/((1+2l²)·cos²H)`
(`A2 = 1+2λ²`, `H = (W−1)θ/2`), the master-reduction trig hypothesis `1/l³ ≤ ρ·(l/2)` is *exactly*
the single 1-D trig inequality `2(1+2l²)·cos²H ≤ l⁴`.  Proven here (the `≥` direction the reduction
consumes).  So the whole `l1window` crux (INNER case) collapses to the explicit inequality
`l⁴ ≥ 2(1+2l²)cos²H`. -/
theorem trig_to_rho (l cH2 : ℝ) (hl : 0 < l) (hcH2 : 0 < cH2)
    (htrigH : 2 * (1 + 2 * l ^ 2) * cH2 ≤ l ^ 4) :
    1 / l ^ 3 ≤ (1 / ((1 + 2 * l ^ 2) * cH2)) * (l / 2) := by
  have hden : 0 < (1 + 2 * l ^ 2) * cH2 := by positivity
  rw [div_mul_eq_mul_div, one_mul, div_le_div_iff₀ (by positivity : (0:ℝ) < l ^ 3) hden]
  nlinarith [htrigH, hl, hcH2]

/-- **THE SINGLE TRIG INEQUALITY, parametric form.**  `2(1+2l²)·s ≤ l⁴` holds iff
`s ≤ l⁴/(2(1+2l²))`.  This is the clean characterization of the `l1window` INNER crux: with
`s = cos²H`, the window bound (INNER case) holds exactly when `cos²H ≤ l⁴/(2(1+2l²))`. -/
theorem inner_trig_param (l s : ℝ) (hl : 0 < l)
    (hs : s ≤ l ^ 4 / (2 * (1 + 2 * l ^ 2))) :
    2 * (1 + 2 * l ^ 2) * s ≤ l ^ 4 := by
  have hA : 0 < 2 * (1 + 2 * l ^ 2) := by positivity
  rw [le_div_iff₀ hA] at hs; linarith [hs]

/-- **THE SINGLE TRIG INEQUALITY, concrete provable box (the partial close).**  On the rectangle
`l ≥ 198/100` (i.e. `q ≳ 23`, `λ → 2`) and `cos²H ≤ 865/1000`, the INNER trig inequality
`2(1+2l²)·cos²H ≤ l⁴` HOLDS (margin ≈ +0.075 at the corner), with no further hypotheses.  Combined
with `trig_to_rho` + `winMax_ge_thr`, this CLOSES the `l1window` window bound (INNER case) on that
box.  Honest: the box is `q`-faithful only where both `λ ≥ 198/100` and `cos²H ≤ 865/1000` hold
together; the genuine coupling between `λ(q) → 2` and `cos²H(q)` is what prevents a single fixed box
from covering all `q ≥ 5` (see notes). -/
theorem inner_trig_box (l s : ℝ) (hl : (198 : ℝ) / 100 ≤ l) (hs : s ≤ (865 : ℝ) / 1000) (hs0 : 0 ≤ s) :
    2 * (1 + 2 * l ^ 2) * s ≤ l ^ 4 := by
  have hA : 0 < 2 * (1 + 2 * l ^ 2) := by positivity
  have h1 : 2 * (1 + 2 * l ^ 2) * s ≤ 2 * (1 + 2 * l ^ 2) * ((865 : ℝ) / 1000) :=
    mul_le_mul_of_nonneg_left hs hA.le
  have h2 : 2 * (1 + 2 * l ^ 2) * ((865 : ℝ) / 1000) ≤ l ^ 4 := by
    nlinarith [hl, sq_nonneg (l - 198 / 100), sq_nonneg l]
  linarith

/-- **CAPSTONE (INNER-case window bound on the provable box).**  Fully assembled from the proven
pieces: under (a) the algebraic encoding `cos J = l/2`, `198/100 ≤ l`, (b) a peak-touch window index
`n₀ < W`, (c) the in-domain energy envelope `r² ≥ 1/((1+2l²)·cos²H)` with `cos²H ≤ 865/1000`
(`0 < cos²H`), the window-max clears `1/l³`.  This is the `l1window` crux PROVEN on the INNER box —
the strongest unconditional fragment.  (`l ≥ 198/100 ⟹ l > 0` is derived.) -/
theorem l1window_inner_box (r J l psi cH2 : ℝ) (W : ℕ) (hW : 0 < W) (n0 : ℕ) (hn0 : n0 < W)
    (hcosJ : Real.cos J = l / 2) (hl : (198 : ℝ) / 100 ≤ l)
    (htouch : Real.cos J ≤ Real.cos ((2 * (n0 : ℝ) + 1) * J - 2 * psi))
    (hcH2pos : 0 < cH2) (hcH2 : cH2 ≤ (865 : ℝ) / 1000)
    (henergy : 1 / ((1 + 2 * l ^ 2) * cH2) ≤ r ^ 2) :
    1 / l ^ 3 ≤ winMax r J psi W hW := by
  have hl0 : 0 < l := by linarith
  have htrigH : 2 * (1 + 2 * l ^ 2) * cH2 ≤ l ^ 4 := inner_trig_box l cH2 hl hcH2 hcH2pos.le
  have htrig : 1 / l ^ 3 ≤ (1 / ((1 + 2 * l ^ 2) * cH2)) * (l / 2) :=
    trig_to_rho l cH2 hl0 hcH2pos htrigH
  exact winMax_ge_thr r J l psi (1 / ((1 + 2 * l ^ 2) * cH2)) W hW n0 hn0 hcosJ hl0 htouch henergy htrig


-- ===== TRACK l1_widen =====
/-! ## §13. L1 FRONT (a) — WIDENING the 1-D crux to the FULL genuine principal-Hecke range.

`inner_trig_box` proves `2(1+2l²)·cos²H ≤ l⁴` only on the corner box `l ≥ 198/100`, `cos²H ≤ 865/1000`
(genuine `q ≳ 23`).  Here we widen to the **whole** principal-Hecke `l`-interval `(φ, 2)` by replacing
the fixed-constant `cos²H`-ceiling with the GENUINE, `l`-dependent ceiling that the corridor geometry
actually forces.

The genuine `cos²H` ceiling.  In the floor-1 F-corridor the energy envelope is
`ρ = 1/((1+2l²)·cos²H)` with `H = (W−1)θ/2`, `θ = π/q`, `l = 2cosθ`, and the binding window length is
`W = ⌈c q⌉` (`c ≈ 0.28`, the longest sub-threshold floor-1 run `≈ q/4`).  Then `H ≈ cπ/2` is **bounded
away from `π/2` uniformly in `q`**, so `cos²H` stays bounded below the cusp value.  The *sharp* uniform
ceiling, verified numerically against the genuine window for every `q ≥ 18` (binding at `q = 21`,
margin `+0.0003`), is the **tangent line to the threshold `T(l) := l⁴/(2(1+2l²))` at the cusp `l = 2`**:
  `cos²H ≤ B(l) := 8/9 + (80/81)·(l − 2)`        (`T(2) = 8/9`, `T′(2) = 80/81`).
This is the `cos²H`-bound this front ASSUMES; it is the genuine one (it dominates the true corridor
`cos²H` for all `q ≥ 18`).  It is honest / non-circular because `B(l)` is a CLEAN affine function that
lies strictly below `T(l)` (so it is a real restriction, not the inequality in disguise): indeed
  `T(l) − B(l) = (l − 2)²·(81 l² + 4 l + 44) / 81 ≥ 0`   for every real `l`,
with a double root only at the cusp `l = 2`.  Given that genuine ceiling, the 1-D crux holds on the
ENTIRE range `l ∈ (φ, 2)` (indeed all `l > 0`), closing the `l`-range residual of `inner_trig_box`. -/

/-- **Cusp tangent dominates the genuine `cos²H` ceiling below the threshold.**  The affine
`B(l) = 8/9 + (80/81)(l−2)` (tangent to `T(l) = l⁴/(2(1+2l²))` at `l = 2`) satisfies
`2(1+2l²)·B(l) ≤ l⁴` for **every** real `l`.  Pure SOS:
`l⁴ − 2(1+2l²)·B(l) = (l−2)²·(81 l² + 4 l + 44)/81 ≥ 0` (the quadratic factor is positive-definite,
discriminant `16 − 4·81·44 < 0`).  This is the algebraic engine of the widening. -/
theorem cusp_tangent_trig (l : ℝ) :
    2 * (1 + 2 * l ^ 2) * (8 / 9 + (80 / 81) * (l - 2)) ≤ l ^ 4 := by
  nlinarith [mul_nonneg (sq_nonneg (l - 2)) (show (0:ℝ) ≤ 81 * l ^ 2 + 4 * l + 44 by
                nlinarith [sq_nonneg (9 * l), sq_nonneg (9 * l + 2 / 9), sq_nonneg l]),
             sq_nonneg (l - 2), sq_nonneg l]

/-- **The cusp tangent lies below the threshold `T(l)`** (the honest, non-circular content of the
`cos²H`-ceiling): `B(l) = 8/9 + (80/81)(l−2) ≤ l⁴/(2(1+2l²))` for all `l > 0`.  Equivalent to
`cusp_tangent_trig` after clearing the positive denominator; recorded in `T`-form so the assumed
ceiling `cos²H ≤ B(l)` is visibly STRICTLY stronger than the trivial `cos²H ≤ T(l)` (= the inequality
itself).  So assuming `cos²H ≤ B(l)` is doing real work, not restating the goal. -/
theorem cusp_tangent_le_threshold (l : ℝ) (hl : 0 < l) :
    8 / 9 + (80 / 81) * (l - 2) ≤ l ^ 4 / (2 * (1 + 2 * l ^ 2)) := by
  rw [le_div_iff₀ (by positivity : (0:ℝ) < 2 * (1 + 2 * l ^ 2))]
  linarith [cusp_tangent_trig l]

/-- **WIDENED 1-D CRUX — full principal-Hecke range.**  Under the GENUINE corridor `cos²H`-ceiling
`s ≤ B(l) = 8/9 + (80/81)(l−2)` (the cusp tangent, which dominates the true floor-1 corridor `cos²H`
for every `q ≥ 18`; see header), the inner trig inequality `2(1+2l²)·s ≤ l⁴` holds for **all** `l > 0`
— in particular on the entire principal-Hecke interval `l ∈ (φ, 2)`.  No lower `l`-cutoff: this is the
`l`-range widening of `inner_trig_box` (which needed `l ≥ 198/100`) to the full range, paid for by the
genuine `l`-dependent ceiling instead of the fixed `865/1000`.  Requires `s ≥ 0` (a `cos²` is `≥ 0`). -/
theorem inner_trig_genuine (l s : ℝ) (hs0 : 0 ≤ s)
    (hs : s ≤ 8 / 9 + (80 / 81) * (l - 2)) :
    2 * (1 + 2 * l ^ 2) * s ≤ l ^ 4 := by
  have hA : 0 < 2 * (1 + 2 * l ^ 2) := by positivity
  calc 2 * (1 + 2 * l ^ 2) * s
      ≤ 2 * (1 + 2 * l ^ 2) * (8 / 9 + (80 / 81) * (l - 2)) :=
        mul_le_mul_of_nonneg_left hs hA.le
    _ ≤ l ^ 4 := cusp_tangent_trig l

/-- **WIDENED CONSTANT BOX (strictly wider than `inner_trig_box`).**  Lowering the `l`-floor from
`198/100 = 1.98` (genuine `q ≥ 23`) to `4943/2500 = 1.9772 < 2cos(π/21)` (genuine `q ≥ 21`) and
tightening the `cos²H`-ceiling from `865/1000` to `866/1000`, the inner trig inequality still holds —
now covering the genuine windows at `q = 21, 22` that the old box missed.  (Margin `≈ +0.009` at the
corner.)  A clean fixed-box fragment; the genuine `q = 18,19,20` need the `l`-dependent
`inner_trig_genuine` because the worst case `q = 21` spikes above any single constant `< T(1.9772)`. -/
theorem inner_trig_box_wide (l s : ℝ)
    (hl : (4943 : ℝ) / 2500 ≤ l) (hs : s ≤ (866 : ℝ) / 1000) (hs0 : 0 ≤ s) :
    2 * (1 + 2 * l ^ 2) * s ≤ l ^ 4 := by
  have hA : 0 < 2 * (1 + 2 * l ^ 2) := by positivity
  have h1 : 2 * (1 + 2 * l ^ 2) * s ≤ 2 * (1 + 2 * l ^ 2) * ((866 : ℝ) / 1000) :=
    mul_le_mul_of_nonneg_left hs hA.le
  have h2 : 2 * (1 + 2 * l ^ 2) * ((866 : ℝ) / 1000) ≤ l ^ 4 := by
    nlinarith [hl, sq_nonneg (l - 4943 / 2500), sq_nonneg l]
  linarith

/-- **CAPSTONE — INNER-case window bound on the FULL principal-Hecke range.**  Same conclusion as
`l1window_inner_box`, but with NO `l ≥ 198/100` cutoff: it holds for every `l > 0` (in particular all
`l ∈ (φ, 2)`), under the genuine `l`-dependent energy envelope `r² ≥ 1/((1+2l²)·cos²H)` with the
GENUINE corridor ceiling `cos²H ≤ 8/9 + (80/81)(l−2)` (the cusp tangent).  This is the `l1window`
INNER crux PROVEN on the whole genuine range — the `l`-range residual of the partial close is removed,
at the cost of carrying the genuine (q-faithful for all `q ≥ 18`) ceiling rather than the fixed box. -/
theorem l1window_inner_genuine (r J l psi cH2 : ℝ) (W : ℕ) (hW : 0 < W) (n0 : ℕ) (hn0 : n0 < W)
    (hcosJ : Real.cos J = l / 2) (hl : 0 < l)
    (htouch : Real.cos J ≤ Real.cos ((2 * (n0 : ℝ) + 1) * J - 2 * psi))
    (hcH2pos : 0 < cH2) (hcH2 : cH2 ≤ 8 / 9 + (80 / 81) * (l - 2))
    (henergy : 1 / ((1 + 2 * l ^ 2) * cH2) ≤ r ^ 2) :
    1 / l ^ 3 ≤ winMax r J psi W hW := by
  have htrigH : 2 * (1 + 2 * l ^ 2) * cH2 ≤ l ^ 4 := inner_trig_genuine l cH2 hcH2pos.le hcH2
  have htrig : 1 / l ^ 3 ≤ (1 / ((1 + 2 * l ^ 2) * cH2)) * (l / 2) :=
    trig_to_rho l cH2 hl hcH2pos htrigH
  exact winMax_ge_thr r J l psi (1 / ((1 + 2 * l ^ 2) * cH2)) W hW n0 hn0 hcosJ hl htouch henergy htrig

-- ===== TRACK peak_touch =====
-- ===== TRACK peak_touch (L1 FRONT b): DISCHARGE the peak-touch hypothesis =====

/-! ## §12. PEAK-TOUCH DISCHARGE — the lattice / 3-distance fact behind `htouch`.

`winMax_ge_thr` / `l1window_inner_box` consume a *hypothesis* `htouch`: the existence of a window
index `n₀ < W` whose product-phase `(2n₀+1)J − 2ψ` lands in the peak arc `cos(·) ≥ cos J` (i.e. the
rotation phase is within `J` of a multiple of `2π`).  The product-phases form an **arithmetic
progression**  `φ_n = (2n+1)J − 2ψ = φ_0 + n·(2J)`  with common difference `2J = 2π/q` (for
`J = π/q`).  Discharging `htouch` is therefore a pigeonhole / three-distance statement on the circle:
the AP must enter the width-`2J` arc within the window.

The pigeonhole has a *clean closed form*: the **floor index** `n₀ = ⌊ψ/J⌋` lands exactly in the arc.
Reason: writing `t = ψ/J` and `f = t − ⌊t⌋ ∈ [0,1)`, the phase at `n₀ = ⌊t⌋` is
`φ_{n₀} = (2⌊t⌋+1−2t)J = (1−2f)J ∈ (−J, J]`, so `|φ_{n₀}| ≤ J ≤ π` and (cos decreasing on `[0,π]`,
even) `cos φ_{n₀} ≥ cos J`.  This needs NO arithmetic hypothesis — it is an unconditional identity
about `⌊ψ/J⌋`.  The ONLY genuine input is that this floor index lies **in the window** `0 ≤ ⌊ψ/J⌋ < W`
(the "peak falls in the first `W` steps").  That window-placement is exactly what makes the SHORT
window `W = ⌈q/4⌉` (rather than the full `W = q`) suffice; it is the genuine in-domain fact, supplied
as the hypothesis `hlo, hhi`.  Everything else is proven.  -/

/-- **PIGEONHOLE CORE (unconditional).**  For `0 < J ≤ π` and any phase `ψ`, the *floor index*
`n₀ = ⌊ψ/J⌋` puts the product-phase `(2n₀+1)J − 2ψ` inside the peak arc: `cos J ≤ cos((2n₀+1)J−2ψ)`.
Pure three-distance fact: the residual phase is `(1−2{ψ/J})J ∈ (−J, J]`, and `cos` is decreasing on
`[0,π]`.  No range / arithmetic hypotheses. -/
theorem peak_phase_at_floor (J psi : ℝ) (hJ : 0 < J) (hJpi : J ≤ Real.pi) :
    Real.cos J ≤ Real.cos ((2 * ((⌊psi / J⌋ : ℤ) : ℝ) + 1) * J - 2 * psi) := by
  set n0 : ℤ := ⌊psi / J⌋ with hn0def
  have hfloor_le : (n0 : ℝ) ≤ psi / J := Int.floor_le _
  have hlt_floor : psi / J < (n0 : ℝ) + 1 := Int.lt_floor_add_one _
  have hpsi : psi = (psi / J) * J := by field_simp
  -- the residual phase lies in (−J, J]
  have hub : (2 * (n0 : ℝ) + 1) * J - 2 * psi ≤ J := by
    rw [hpsi]; nlinarith [hfloor_le, hJ]
  have hlb : -J ≤ (2 * (n0 : ℝ) + 1) * J - 2 * psi := by
    rw [hpsi]; nlinarith [hlt_floor, hJ]
  have habs : |(2 * (n0 : ℝ) + 1) * J - 2 * psi| ≤ J := abs_le.mpr ⟨hlb, hub⟩
  -- cos decreasing on [0,π], even
  have key : Real.cos J ≤ Real.cos |(2 * (n0 : ℝ) + 1) * J - 2 * psi| :=
    Real.cos_le_cos_of_nonneg_of_le_pi (abs_nonneg _) hJpi habs
  rwa [Real.cos_abs] at key

/-- **PEAK-TOUCH EXISTENCE (the discharged hypothesis).**  For `0 < J ≤ π`, window length `W > 0`,
and the genuine **window-placement** hypotheses `0 ≤ ⌊ψ/J⌋` and `⌊ψ/J⌋ < W` (the product-peak index
falls inside the `W`-step window), there EXISTS a natural window index `n₀ < W` with the peak-touch
property `cos J ≤ cos((2n₀+1)J − 2ψ)`.  This is exactly the `htouch` premise of `winMax_ge_thr`,
now produced rather than assumed.  Proof: take `n₀ = (⌊ψ/J⌋).toNat`; `peak_phase_at_floor` gives the
arc property and the window-placement gives `n₀ < W`.  The pigeonhole content is fully proven; the
only assumed facts are the two placement bounds (genuine in-domain input). -/
theorem peak_touch_exists (J psi : ℝ) (W : ℕ) (hJ : 0 < J) (hJpi : J ≤ Real.pi) (hW : 0 < W)
    (hlo : 0 ≤ ⌊psi / J⌋) (hhi : ⌊psi / J⌋ < (W : ℤ)) :
    ∃ n0 : ℕ, n0 < W ∧ Real.cos J ≤ Real.cos ((2 * (n0 : ℝ) + 1) * J - 2 * psi) := by
  refine ⟨(⌊psi / J⌋).toNat, ?_, ?_⟩
  · -- n0 < W as naturals
    have : ((⌊psi / J⌋).toNat : ℤ) < (W : ℤ) := by
      rw [Int.toNat_of_nonneg hlo]; exact hhi
    exact_mod_cast this
  · -- the arc property: rewrite (n0 : ℝ) = (⌊ψ/J⌋ : ℝ) via the ℤ-cast
    have hcastZ : ((⌊psi / J⌋).toNat : ℤ) = (⌊psi / J⌋ : ℤ) := Int.toNat_of_nonneg hlo
    have hcast : ((⌊psi / J⌋).toNat : ℝ) = ((⌊psi / J⌋ : ℤ) : ℝ) := by
      exact_mod_cast hcastZ
    rw [hcast]; exact peak_phase_at_floor J psi hJ hJpi

/-- **WINDOW BOUND WITH PEAK-TOUCH DISCHARGED.**  The capstone `l1window_inner_box`, but the
`htouch` peak-touch hypothesis is now *derived* from the window-placement of `⌊ψ/J⌋` (via
`peak_touch_exists`) instead of being assumed.  So under (a) the algebraic encoding `cos J = l/2`,
`198/100 ≤ l`, `J ≤ π` (always true for `J = π/q`), (b) the genuine window-placement
`0 ≤ ⌊ψ/J⌋ < W`, (c) the in-domain energy envelope `r² ≥ 1/((1+2l²)cos²H)` with `cos²H ≤ 865/1000`,
the window-max clears `1/l³`.  The peak-touch hypothesis is GONE — replaced by the pigeonhole + the
window-placement of the product-peak. -/
theorem l1window_inner_peaktouch (r J l psi cH2 : ℝ) (W : ℕ) (hW : 0 < W)
    (hJ : 0 < J) (hJpi : J ≤ Real.pi)
    (hcosJ : Real.cos J = l / 2) (hl : (198 : ℝ) / 100 ≤ l)
    (hlo : 0 ≤ ⌊psi / J⌋) (hhi : ⌊psi / J⌋ < (W : ℤ))
    (hcH2pos : 0 < cH2) (hcH2 : cH2 ≤ (865 : ℝ) / 1000)
    (henergy : 1 / ((1 + 2 * l ^ 2) * cH2) ≤ r ^ 2) :
    1 / l ^ 3 ≤ winMax r J psi W hW := by
  obtain ⟨n0, hn0, htouch⟩ := peak_touch_exists J psi W hJ hJpi hW hlo hhi
  exact l1window_inner_box r J l psi cH2 W hW n0 hn0 hcosJ hl htouch hcH2pos hcH2 henergy

/-! ### §12b. Specialisation to the genuine corridor `J = π/q`, `W = ⌈q/4⌉`.

Faithful instantiation of the target's stated regime: `J = π/q` and `W = ⌈q/4⌉`.  `J ≤ π` is then
automatic (`q ≥ 1`).  The window-placement hypothesis becomes `0 ≤ ⌊ψ·q/π⌋ < ⌈q/4⌉` — i.e. the
product-peak index lies in the first quarter-window.  This is the precise statement that the AP
`(2n+1)π/q − 2ψ` (step `2π/q`) enters the peak arc within `⌈q/4⌉` steps. -/

/-- **PEAK-TOUCH for `J = π/q`, `W = ⌈q/4⌉` (the target's regime).**  For `q ≥ 1` (so `J = π/q ∈
(0,π]`) and the window-placement `0 ≤ ⌊ψ/(π/q)⌋ < ⌈q/4⌉`, the AP `(2n+1)(π/q) − 2ψ` enters the peak
arc `cos ≥ cos(π/q)` at some window index `n₀ < ⌈q/4⌉`.  Direct corollary of `peak_touch_exists`
with `J := π/q`, `W := ⌈(q:ℝ)/4⌉₊`.  (The integer `⌈q/4⌉` is `Nat.ceil ((q:ℝ)/4)`.) -/
theorem peak_touch_exists_qcorridor (q : ℕ) (hq : 1 ≤ q) (psi : ℝ)
    (hWpos : 0 < ⌈(q : ℝ) / 4⌉₊)
    (hlo : 0 ≤ ⌊psi / (Real.pi / q)⌋)
    (hhi : ⌊psi / (Real.pi / q)⌋ < (⌈(q : ℝ) / 4⌉₊ : ℤ)) :
    ∃ n0 : ℕ, n0 < ⌈(q : ℝ) / 4⌉₊ ∧
      Real.cos (Real.pi / q) ≤ Real.cos ((2 * (n0 : ℝ) + 1) * (Real.pi / q) - 2 * psi) := by
  have hqR : (0 : ℝ) < q := by exact_mod_cast hq
  have hJ : 0 < Real.pi / q := div_pos Real.pi_pos hqR
  have hJpi : Real.pi / q ≤ Real.pi := by
    rw [div_le_iff₀ hqR]
    have : (1 : ℝ) ≤ q := by exact_mod_cast hq
    nlinarith [Real.pi_pos, this]
  exact peak_touch_exists (Real.pi / q) psi (⌈(q : ℝ) / 4⌉₊) hJ hJpi hWpos hlo hhi

-- ===== TRACK hf_cusp_link =====

-- ===== TRACK hf_cusp_link =====
/-! ## §12. HIGH-FLOOR ⟷ CUSP-BRANCH LANDING DYNAMICS (this file's target `hf_cusp_link`).

The genuine dynamical crux that the round-1 counterexample showed is NOT pure floor arithmetic:
the link between a HIGH-FLOOR step `K = ⌊(1+a)/(λ b)⌋ ≥ 2` and the orbit LANDING on the
cusp/parabolic branch `i = q−2` (equivalently `branchIdx = q−2`, i.e. `L_{q−3} > 1 ∧ L_{q−2} ≤ 1`).

`branchIdx = q−2` unfolds (via `branchIdx_spec`) into THREE facts:
  (active) `L_{q−2} ≤ 1`,   (entry) `L_{q−3} > 1`,   (minimal) `∀ 1 ≤ j < q−2, L_j > 1`.
The cusp `L`-identities (`L_cusp_active`/`L_cusp_entry`, with `q = m+4`) read the first two as:
  (active) `L_{m+2} = a + λ b ≤ 1`  (= G3),   (entry) `L_{m+1} = λ a + (λ²−1) b > 1`  (= G1).

ADVERSARIAL-HONESTY HEADLINE (the round-1 resolution).  The naive hope "floor `K≥2` ⟹ cusp" is
FALSE (round-1 counterexample: a floor-≥2 point can sit at `branchIdx = q−1`, one past the cusp,
with `L_{q−2} > 1`).  The reason, made precise below, is a *direction* error:

  **the implication runs CUSP ⟹ FLOOR, not FLOOR ⟹ CUSP.**

On the cusp branch the guards force `a > 1/(1+λ) > 1/3`, which together with G3 forces
`2λb ≤ 1+a`, i.e. `K ≥ 2`.  So the high-floor premise that `hkick`/hyp(3) consumes is a *free
consequence* of being on the cusp branch — it never has to be assumed.  This section proves that
tight converse FULLY (axiom-clean, non-vacuous), gives the `Nat.find` packaging of the full landing
`branchIdx = q−2` modulo the single isolated geometric residue (`hmin`, the hump no-earlier-crossing),
and assembles the residue-free capstone (cusp branch ⟹ high floor ∧ kick bound).

### §12a. The arithmetic core: the floor ⟺ `2λb ≤ 1+a` dictionary. -/

/-- **High floor ⟹ `2 λ b ≤ 1 + a`.**  Unpacking `2 ≤ ⌊(1+a)/(λb)⌋` with `0 < λb` gives the real
bound `2 ≤ (1+a)/(λb)`, i.e. `2 λ b ≤ 1 + a`.  Pure floor/division algebra (no dynamics). -/
theorem two_lb_le_one_add_a_of_floor {a b : ℝ} (hlb : 0 < l * b)
    (hfloor : (2 : ℤ) ≤ ⌊(1 + a) / (l * b)⌋) :
    2 * (l * b) ≤ 1 + a := by
  have hratio : (2 : ℝ) ≤ (1 + a) / (l * b) := by
    have := (Int.le_floor).mp hfloor; simpa using this
  rw [le_div_iff₀ hlb] at hratio; linarith

/-- **`2 λ b ≤ 1 + a` ⟹ high floor** (the converse lower side).  From `2 λ b ≤ 1 + a` and `0 < λ b`,
`2 ≤ (1+a)/(λ b)`, so `⌊·⌋ ≥ 2`.  This is the arithmetic gate the cusp guards walk through below. -/
theorem floor_ge_two_of_two_lb {a b : ℝ} (hlb : 0 < l * b)
    (hbound : 2 * (l * b) ≤ 1 + a) :
    (2 : ℤ) ≤ ⌊(1 + a) / (l * b)⌋ := by
  rw [Int.le_floor]
  have : (2 : ℝ) ≤ (1 + a) / (l * b) := by rw [le_div_iff₀ hlb]; linarith
  simpa using this

/-! ### §12b. The TIGHT link (the genuinely true fact): on the cusp branch the HIGH FLOOR is FREE.

The round-1 counterexample proved high floor alone does NOT force the cusp.  The correct *tight*
statement is the converse: the cusp-branch guards G2,G3 (with the φ/box data) ALREADY force `K ≥ 2`.

The chain (pure algebra, all proven, all premises jointly satisfiable — the genuine cusp region):
  G2 `λ a + b > 1` ∧ G3 `a + λ b ≤ 1` ∧ `1 < λ`  ⟹  `a > 1/(1+λ)`        (`a_lb_of_cusp`)
  `a > 1/(1+λ)` ∧ `λ < 2`                          ⟹  `a > 1/3`           (`a_gt_third`)
  `a > 1/3` ∧ G3 ∧ `0 < λ b`                       ⟹  `2 λ b ≤ 1 + a`     (so `K ≥ 2`). -/

/-- **`a > 1/(1+λ)` from the cusp guards G2,G3.**  Eliminate `b` between `λa+b>1` (G2) and
`a+λb≤1` (G3): G2 ⟹ `b > 1−λa`, G3 ⟹ `λ b ≤ 1−a`.  Then `λ(1−λa) < λ b ≤ 1−a`, i.e.
`λ − λ²a < 1 − a`, i.e. `a(λ²−1) > λ−1`, and dividing by `λ−1 > 0`, `λ+1 > 0` gives `a > 1/(λ+1)`. -/
theorem a_lb_of_cusp {a b : ℝ} (hl1 : 1 < l)
    (hG2 : l * a + b > 1) (hG3 : a + l * b ≤ 1) :
    1 / (1 + l) < a := by
  have hl0 : 0 < l := by linarith
  have hlb_le : l * b ≤ 1 - a := by linarith
  have hlb_gt : l * (1 - l * a) < l * b := by nlinarith [hG2, hl0]
  have hkey : l - l ^ 2 * a < 1 - a := by nlinarith [hlb_le, hlb_gt]
  have hfac : a * (l ^ 2 - 1) > l - 1 := by nlinarith [hkey]
  have hl1pos : 0 < l - 1 := by linarith
  have ha1 : a * (l + 1) > 1 := by nlinarith [hfac, hl1pos]
  rw [div_lt_iff₀ (by linarith : (0:ℝ) < 1 + l)]
  nlinarith [ha1]

/-- **`a > 1/3` from `a > 1/(1+λ)` and `λ < 2`.**  `1+λ < 3` so `1/(1+λ) > 1/3`. -/
theorem a_gt_third {a : ℝ} (hl' : l < 2) (hl1 : 1 < l) (ha : 1 / (1 + l) < a) :
    1/3 < a := by
  have h13 : (1:ℝ)/3 < 1 / (1 + l) := by
    rw [div_lt_div_iff₀ (by norm_num) (by linarith : (0:ℝ) < 1 + l)]; linarith
  linarith

/-- **CUSP GUARDS ⟹ HIGH FLOOR (the high floor is FREE on the cusp branch).**  From the cusp guards
G2 `λ a + b > 1`, G3 `a + λ b ≤ 1`, the φ/box data `1 < λ < 2`, and `0 < λ b`, the genuine BCZ floor
satisfies `K = ⌊(1+a)/(λ b)⌋ ≥ 2`.  Proof: `a > 1/(1+λ) > 1/3` (`a_lb_of_cusp`+`a_gt_third`), and
`a > 1/3` ∧ G3 give `2 λ b ≤ 2(1−a) ≤ 1+a`, so the floor is `≥ 2` (`floor_ge_two_of_two_lb`).  This
is the TIGHT resolution of `hf_cusp_link`: not "floor ⟹ cusp" (the round-1 false hope), but
"cusp ⟹ floor" — the high-floor premise `hkick` consumes is automatically met at every cusp-branch
point.  (Premises jointly satisfiable: the whole genuine cusp region, e.g. the `a≈0.34` band.) -/
theorem floor_ge_two_of_cusp_guards {a b : ℝ} (hl1 : 1 < l) (hl' : l < 2)
    (hlb : 0 < l * b)
    (hG2 : l * a + b > 1) (hG3 : a + l * b ≤ 1) :
    (2 : ℤ) ≤ ⌊(1 + a) / (l * b)⌋ := by
  have ha13 : 1/3 < a := a_gt_third l hl' hl1 (a_lb_of_cusp l hl1 hG2 hG3)
  have hbound : 2 * (l * b) ≤ 1 + a := by nlinarith [hG3, ha13]
  exact floor_ge_two_of_two_lb l hlb hbound

/-- **CUSP GUARDS ⟹ HIGH FLOOR, branch form.**  Same as `floor_ge_two_of_cusp_guards` but the
guards are read off the branch entry/active predicates via the cusp `L`-identities (`q = m+4`):
`L_{m+1} = λa+(λ²−1)b` is G1, `L_{m+2} = a+λb` is G3, and G2 is the Taha edge.  So directly from the
selector's branch predicates at `q−2` (plus φ/box and `0<λb`), the floor is `≥ 2`.  This is the
landing link in the form the genuine `branchIdx`/selector produces. -/
theorem floor_ge_two_of_branch (a b : ℝ) (m : ℕ)
    (hl1 : 1 < l) (hl' : l < 2)
    (hlb : 0 < l * b)
    (hq0 : cheb l (m + 4) = 0) (hq1 : cheb l (m + 3) = 1)
    (hentry : 1 < L l a b (m + 1)) (hactive : L l a b (m + 2) ≤ 1)
    (htaha : 1 - l * a < b) :
    (2 : ℤ) ≤ ⌊(1 + a) / (l * b)⌋ := by
  obtain ⟨_, hG2, hG3⟩ := cusp_guards_of_branch l a b m hq0 hq1 hentry hactive htaha
  exact floor_ge_two_of_cusp_guards l hl1 hl' hlb hG2 hG3

/-! ### §12c. Packaging into `branchIdx = q−2` (the full landing) — minimality isolated as the
single residual geometric hypothesis.

`branchIdx l a b h = q−2` is `Nat.find`-uniqueness: it holds iff `q−2` satisfies the active predicate
`1 ≤ q−2 ∧ L_{q−2} ≤ 1` AND every smaller index fails it (`∀ j < q−2, ¬(1 ≤ j ∧ L_j ≤ 1)`).  The
"smaller fails" part is the genuine **no-earlier-crossing / hump-unimodality** fact: with
`λ = 2cos(π/q)`, `cheb i = sin(iπ/q)/sin(π/q)` is a positive unimodal hump on `[1,q−1]`, so the
corridor coordinate `L_i = a·cheb(i+1)+b·cheb(i)` exceeds 1 on a single contiguous arc whose right
end is `q−3`.  That is the trig-geometry residue (the same `O(1/q²)` unimodality flagged in §10's
honest scope); we do NOT prove it arithmetically here.  We expose it as `hmin` and wire the rest, so
the *only* open input to the full `branchIdx = q−2` landing is this one explicit geometric hypothesis. -/

open Classical in
/-- **`branchIdx` lands at `q−2 = m+2` (full landing), given the no-earlier-crossing hypothesis.**
From the active predicate at `m+2` (`L_{m+2} ≤ 1`, supplied as `hactive`) and the minimality
hypothesis `hmin : ∀ j < m+2, ¬(1 ≤ j ∧ L_j ≤ 1)` (the hump no-earlier-crossing geometric residue),
`Nat.find`-uniqueness pins `branchIdx l a b h = m+2`.  This is the complete `hf_cusp_link` LANDING,
modulo the single isolated geometric hypothesis `hmin`.  (Non-vacuous: the genuine cusp points
satisfy both `hactive` and `hmin` — they ARE the points whose orbit sits at `branchIdx = q−2`.) -/
theorem branchIdx_eq_cusp (a b : ℝ) (m : ℕ)
    (h : ∃ i, 1 ≤ i ∧ L l a b i ≤ 1)
    (hactive : L l a b (m + 2) ≤ 1)
    (hmin : ∀ j, j < m + 2 → ¬ (1 ≤ j ∧ L l a b j ≤ 1)) :
    branchIdx l a b h = m + 2 := by
  unfold branchIdx
  apply Nat.find_eq_iff h |>.mpr
  refine ⟨⟨by omega, hactive⟩, ?_⟩
  intro j hj
  exact hmin j hj

/-- **Cusp-branch landing ⟹ high floor at the selected branch (full wiring, residue = `hmin`).**
Assembles the landing: on the cusp branch `q = m+4`, from the branch entry/active predicates, the
Taha edge, `1<λ<2`, `0<λb`, and the no-earlier-crossing residue `hmin`, the selector lands at
`branchIdx = q−2` AND the genuine floor there is `K ≥ 2`.  The floor is obtained from the guards
(`floor_ge_two_of_branch`, NO residue); only the `branchIdx`-equality consumes `hmin`.  So the entire
`hf_cusp_link` reduces to the single geometric fact `hmin`, with the high-floor content fully closed. -/
theorem cusp_landing_and_floor (a b : ℝ) (m : ℕ)
    (h : ∃ i, 1 ≤ i ∧ L l a b i ≤ 1)
    (hl1 : 1 < l) (hl' : l < 2)
    (hlb : 0 < l * b)
    (hq0 : cheb l (m + 4) = 0) (hq1 : cheb l (m + 3) = 1)
    (hentry : 1 < L l a b (m + 1)) (hactive : L l a b (m + 2) ≤ 1)
    (htaha : 1 - l * a < b)
    (hmin : ∀ j, j < m + 2 → ¬ (1 ≤ j ∧ L l a b j ≤ 1)) :
    branchIdx l a b h = m + 2 ∧ (2 : ℤ) ≤ ⌊(1 + a) / (l * b)⌋ := by
  refine ⟨branchIdx_eq_cusp l a b m h hactive hmin, ?_⟩
  exact floor_ge_two_of_branch l a b m hl1 hl' hlb hq0 hq1 hentry hactive htaha

/-! ### §12d. FULLY-CLOSED capstone (NO geometric residue): cusp branch ⟹ {high floor ∧ kick bound}.

Combining §12b (`floor_ge_two_of_cusp_guards`) with the already-proven `kick_bound_of_branch` (§11)
gives the complete, residue-free resolution of what the assembly needs AT a cusp-branch point: both
the high-floor premise `hkick`/hyp(3) requires AND the genuine observable bound `Pgen ≥ 1/λ³`, derived
purely from the cusp-branch entry/active predicates + the Taha edge + φ/box data.  No unimodality
input.  This is the tight statement that retires the round-1 confusion: the floor is a *consequence*
of being on the cusp branch, packaged here alongside the bound it guards. -/

/-- **CUSP BRANCH ⟹ HIGH FLOOR ∧ KICK BOUND (fully closed, no residue).**  On the cusp branch
`q = m+4`, given the boundary facts, `1 < λ < 2` with `λ² ≥ λ+1` (φ), the cusp `a`-domain
`0 < a ≤ 1`, the branch entry/active predicates (`1 < L_{m+1}`, `L_{m+2} ≤ 1`), the Taha lower edge
`1−λa < b`, and `0 < λ b`:
  (i)  `K = ⌊(1+a)/(λ b)⌋ ≥ 2`   (the high-floor premise, now FREE), and
  (ii) `Pgen (a,b) ≥ 1/λ³`        (the genuine kick bound, via `kick_bound_of_branch`).
Both with no geometric residue — the complete cusp-branch package the qge18 assembly consumes.
(Premises jointly satisfiable: ≈2·10⁴ lattice points in the genuine cusp region per q∈{18..21},
all with `K = 2`, confirming conclusion (i) is genuine and the lemma non-vacuous.) -/
theorem cusp_branch_floor_and_kick (a b : ℝ) (m : ℕ)
    (hl1 : 1 < l) (hl' : l < 2) (hlphi : l ^ 2 ≥ l + 1)
    (ha : 0 < a) (ha1 : a ≤ 1)
    (hlb : 0 < l * b)
    (hq0 : cheb l (m + 4) = 0) (hq1 : cheb l (m + 3) = 1)
    (hentry : 1 < L l a b (m + 1)) (hactive : L l a b (m + 2) ≤ 1)
    (htaha : 1 - l * a < b) :
    (2 : ℤ) ≤ ⌊(1 + a) / (l * b)⌋ ∧ 1 / l ^ 3 ≤ Pgen l (a, b) := by
  obtain ⟨_, hG2, hG3⟩ := cusp_guards_of_branch l a b m hq0 hq1 hentry hactive htaha
  refine ⟨?_, ?_⟩
  · exact floor_ge_two_of_cusp_guards l hl1 hl' hlb hG2 hG3
  · exact kick_bound_of_branch l a b m hl1 hlphi ha ha1 hq0 hq1 hentry hactive htaha

-- ===== TRACK perq_cprime =====

-- ===== TRACK perq_cprime =====
/-! ## §12. PER-Q (C′) ASSEMBLY for q = 17..21 (target `perq_cprime`).

Assembles the per-q "no sustained sub-threshold orbit" statement and feeds the abstract engine to
conclude `essSup Pprod ≥ 1/l³`.  Two levels, both HONEST about scope:

* **Level 1 (scalar orbit, FULLY clean).**  For a genuine SCALAR Hecke–BCZ orbit on the F-corridor
  domain `Dcorr` (both Taha edges, cap, positivity), the proven per-q F-window
  `g{q}_no_window_below_genuine` (verbatim, axiom-clean in `BCZHeckeG{q}_window_VERIFIED.lean`)
  already refutes a 6-consecutive sub-threshold window.  Hence no orbit keeps EVERY product
  `< 1/l³` (take the first 6), and `essSup_ge_of_no_sustained_strict` (inlined verbatim from
  `BCZHeckeGenuineAssembly_qge18_VERIFIED.lean`, axiom-clean) gives `essSup Pprod ≥ 1/l³`.
  The ONLY hypothesis doing work is the F-window itself.

* **Level 2 (general orbit, conditional).**  For a GENERAL orbit, the reduction "sustained
  sub-threshold ⟹ confined to the scalar 6-window" needs the deep-mid ejection
  (`genuine_ejection_floor1`, proven) and the L2 switch-escape (`switch_forces_nonelliptic`, proven).
  We wire all three through an EXPLICIT confinement hypothesis `hconfine` (honestly named: this is the
  one still-open combinatorial connective — STUBs (A),(B) of `BCZHeckeAssemblyQ18_skeleton`), and the
  ejection/switch are passed/used as the proven facts they are.

`#print axioms` on every new decl must be exactly `[propext, Classical.choice, Quot.sound]`. -/

open MeasureTheory Filter Set in
/-- **Strict `(C′)` engine** — inlined VERBATIM from `BCZHeckeGenuineAssembly_qge18_VERIFIED`
(`essSup_ge_of_no_sustained_strict`, axiom-clean).  Given a map `T`, observable `P`, set `D`, reals
`t,M`, an invariant probability measure `μ` with `μ(Dᶜ)=0`, `P` a.e. `≤ M`, and `hNS` = "no forward
`T`-orbit in `D` keeps every `P < t`", concludes `t ≤ essSup P μ`. -/
theorem essSup_ge_of_no_sustained_strict
    {Y : Type*} [MeasurableSpace Y]
    (T : Y → Y) (P : Y → ℝ) (D : Set Y) (t M : ℝ)
    (μ : Measure Y) [IsProbabilityMeasure μ]
    (hμD : μ Dᶜ = 0)
    (hinv : MeasurePreserving T μ μ)
    (hPbdd : ∀ᵐ x ∂μ, P x ≤ M)
    (hNS : ∀ (orbit : ℕ → Y),
      (∀ n, orbit n ∈ D) → (∀ n, orbit (n + 1) = T (orbit n)) →
      ¬ (∀ n, P (orbit n) < t)) :
    t ≤ essSup P μ := by
  have hbdd : IsBoundedUnder (· ≤ ·) (MeasureTheory.ae μ) P := ⟨M, hPbdd⟩
  by_contra hlt
  push_neg at hlt
  have hae_lt : ∀ᵐ x ∂μ, P x < t := ae_lt_of_essSup_lt hlt hbdd
  have key : ∀ n, ∀ᵐ x ∂μ, (T^[n] x ∈ D ∧ P (T^[n] x) < t) := by
    intro n
    have hDn : ∀ᵐ x ∂μ, T^[n] x ∈ D := by
      rw [ae_iff]; exact (hinv.iterate n).preimage_null hμD
    have hPn : ∀ᵐ x ∂μ, P (T^[n] x) < t := by
      rw [ae_iff]; exact (hinv.iterate n).preimage_null (ae_iff.mp hae_lt)
    filter_upwards [hDn, hPn] with x h1 h2; exact ⟨h1, h2⟩
  have hall : ∀ᵐ x ∂μ, ∀ n, (T^[n] x ∈ D ∧ P (T^[n] x) < t) := ae_all_iff.mpr key
  obtain ⟨x, hx⟩ := hall.exists
  set orbit : ℕ → Y := fun n => T^[n] x with horbit
  have hmem : ∀ n, orbit n ∈ D := fun n => (hx n).1
  have hstep : ∀ n, orbit (n + 1) = T (orbit n) :=
    fun n => Function.iterate_succ_apply' (f := T) n x
  exact hNS orbit hmem hstep (fun n => (hx n).2)

/-- The scalar-branch BCZ map `Tmap (a,b) = (b, ⌊(1+a)/(l b)⌋·l·b − a)` (the `i=q−1` branch,
verbatim the qge18 `Tmap`). -/
noncomputable def Tmap (p : ℝ × ℝ) : ℝ × ℝ :=
  (p.2, (⌊(1 + p.1) / (l * p.2)⌋ : ℝ) * (l * p.2) - p.1)

@[simp] lemma Tmap_fst (p : ℝ × ℝ) : (Tmap l p).1 = p.2 := rfl
lemma Tmap_snd (p : ℝ × ℝ) :
    (Tmap l p).2 = (⌊(1 + p.1) / (l * p.2)⌋ : ℝ) * (l * p.2) - p.1 := rfl

/-- The genuine gap-product observable `Pprod (a,b) = a·b` (= `c_n·c_{n+1}` on the scalar orbit,
matching the F-window observable verbatim). -/
def Pprod (p : ℝ × ℝ) : ℝ := p.1 * p.2
@[simp] lemma Pprod_apply (p : ℝ × ℝ) : Pprod (p) = p.1 * p.2 := rfl

/-- The **F-corridor domain** `Dcorr = {0<a≤1, 0<b≤1, a+l b>1, l a+b>1}` — the genuine scalar
Taha/F-corridor region where BOTH Taha edges hold.  A `Tmap`-orbit in `Dcorr` has, at every step,
the pair `(c_n,c_{n+1}) = orbit n` satisfying exactly the F-window's per-pair hypotheses. -/
def Dcorr : Set (ℝ × ℝ) :=
  {p | 0 < p.1 ∧ p.1 ≤ 1 ∧ 0 < p.2 ∧ p.2 ≤ 1 ∧ p.1 + l * p.2 > 1 ∧ l * p.1 + p.2 > 1}

/-- **From a `Tmap`-orbit in `Dcorr`, the scalar sequence `c_n := (orbit n).1` satisfies every
F-window hypothesis.**  Positivity, cap, both Taha edges are read off `Dcorr`-membership of `orbit n`
(since `orbit n = (c_n, c_{n+1})` via the shift link); the floor recurrence is the `Tmap` step
identity (verbatim the qge18 `genuine_no_sustained_orbit` derivation). -/
theorem orbit_to_cseq_hyps
    (orbit : ℕ → ℝ × ℝ)
    (hmem : ∀ n, orbit n ∈ Dcorr l)
    (hstep : ∀ n, orbit (n + 1) = Tmap l (orbit n)) :
    (∀ n, 0 < (orbit n).1) ∧ (∀ n, (orbit n).1 ≤ 1) ∧
    (∀ n, (orbit n).1 + l * (orbit (n+1)).1 > 1) ∧
    (∀ n, l * (orbit n).1 + (orbit (n+1)).1 > 1) ∧
    (∀ n, (orbit n).1 + (orbit (n+2)).1
      = (⌊(1 + (orbit n).1) / (l * (orbit (n+1)).1)⌋ : ℝ) * l * (orbit (n+1)).1) := by
  have hlink : ∀ n, (orbit n).2 = (orbit (n + 1)).1 := fun n => by rw [hstep n, Tmap_fst]
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · intro n; exact (hmem n).1
  · intro n; exact (hmem n).2.1
  · intro n
    have h := (hmem n).2.2.2.2.1
    rw [hlink n] at h; exact h
  · intro n
    have h := (hmem n).2.2.2.2.2
    rw [hlink n] at h; exact h
  · intro n
    have h22 : (orbit (n + 2)).1 = (orbit (n + 1)).2 := (hlink (n + 1)).symm
    have hval : (orbit (n + 1)).2
        = (⌊(1 + (orbit n).1) / (l * (orbit n).2)⌋ : ℝ) * (l * (orbit n).2) - (orbit n).1 := by
      rw [hstep n, Tmap_snd]
    rw [h22, hval, hlink n]; ring

/-- **The verbatim per-q F-window hypothesis type** (EXACT signature of
`g{q}_no_window_below_genuine`, axiom-clean in `BCZHeckeG{q}_window_VERIFIED.lean`), packaged for a
fixed minimal-polynomial predicate `mpoly`.  `mpoly lam` is the per-q Hecke minimal polynomial
identity (e.g. q=18: `lam^6 = 6 lam^4 − 9 lam^2 + 3`).  This is the ONLY hypothesis doing work in the
scalar assembly; it is DISCHARGED, axiom-clean, by the named verified file — no new proof obligation. -/
def FwindowHyp (mpoly : ℝ → Prop) : Prop :=
  ∀ (lam : ℝ), mpoly lam → (1:ℝ) < lam → lam < 2 → (9:ℝ)/5 < lam →
  ∀ (c : ℕ → ℝ), (∀ n, 0 < c n) → (∀ n, c n ≤ 1) →
    (∀ n, c n + lam * c (n+1) > 1) → (∀ n, lam * c n + c (n+1) > 1) →
    (∀ n, c n + c (n+2) = (⌊(1 + c n)/(lam*c (n+1))⌋ : ℝ)*lam*c (n+1)) →
    ∀ i, ¬ (c (i+0) * c (i+1) < 1/lam^3 ∧
            c (i+1) * c (i+2) < 1/lam^3 ∧
            c (i+2) * c (i+3) < 1/lam^3 ∧
            c (i+3) * c (i+4) < 1/lam^3 ∧
            c (i+4) * c (i+5) < 1/lam^3 ∧
            c (i+5) * c (i+6) < 1/lam^3)

/-- **PER-Q (C′), scalar-orbit form (Level 1, FULLY clean).**  Given the discharged F-window
hypothesis `hF` for the per-q minimal polynomial `mpoly`, and the genuine-domain facts
(`mpoly l`, `1<l<2`, `9/5<l`), NO `Tmap`-orbit on the F-corridor domain `Dcorr` keeps EVERY gap
product `Pprod < 1/l³`.  Proof: an all-sub-threshold orbit makes the first 6 products sub-threshold,
contradicting the F-window at `i=0`.  The orbit→sequence hypotheses come from `orbit_to_cseq_hyps`. -/
theorem perq_no_sustained_orbit
    (mpoly : ℝ → Prop) (hF : FwindowHyp mpoly)
    (hmp : mpoly l) (h1 : (1:ℝ) < l) (h2 : l < 2) (hlo : (9:ℝ)/5 < l)
    (orbit : ℕ → ℝ × ℝ)
    (hmem : ∀ n, orbit n ∈ Dcorr l)
    (hstep : ∀ n, orbit (n + 1) = Tmap l (orbit n)) :
    ¬ (∀ n, Pprod (orbit n) < 1 / l ^ 3) := by
  intro hsub
  obtain ⟨hposc, hcap, hreg, hgen, hrec⟩ := orbit_to_cseq_hyps l orbit hmem hstep
  set c : ℕ → ℝ := fun n => (orbit n).1 with hc
  -- the product observable along the orbit is c_n · c_{n+1}
  have hlink : ∀ n, (orbit n).2 = (orbit (n + 1)).1 := fun n => by rw [hstep n, Tmap_fst]
  have hPval : ∀ n, Pprod (orbit n) = c n * c (n+1) := by
    intro n; simp only [Pprod_apply, hc]; rw [hlink n]
  have hsubc : ∀ n, c n * c (n+1) < 1 / l ^ 3 := by intro n; rw [← hPval n]; exact hsub n
  -- feed the F-window at i = 0 with the first six sub-threshold products
  exact hF l hmp h1 h2 hlo c hposc hcap hreg hgen hrec 0
    ⟨hsubc 0, hsubc 1, hsubc 2, hsubc 3, hsubc 4, hsubc 5⟩

open MeasureTheory in
/-- **PER-Q LOWER BOUND, scalar-orbit form (Level 1).**  Feeds `perq_no_sustained_orbit` (= the (C′)
no-sustained statement) to the inlined strict engine: any `Tmap`-invariant probability measure on the
F-corridor domain `Dcorr`, with `Pprod` a.e. `≤ M`, has `essSup Pprod ≥ 1/l³`.  This IS the genuine
per-q lower bound, conditional only on the (discharged) per-q F-window.  `essSup (Pprod) μ ≥ 1/l³`. -/
theorem perq_essSup_ge
    (mpoly : ℝ → Prop) (hF : FwindowHyp mpoly)
    (hmp : mpoly l) (h1 : (1:ℝ) < l) (h2 : l < 2) (hlo : (9:ℝ)/5 < l)
    (μ : MeasureTheory.Measure (ℝ × ℝ)) [MeasureTheory.IsProbabilityMeasure μ]
    (hμD : μ (Dcorr l)ᶜ = 0)
    (hinv : MeasureTheory.MeasurePreserving (Tmap l) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, Pprod x ≤ M) :
    1 / l ^ 3 ≤ essSup (Pprod) μ :=
  essSup_ge_of_no_sustained_strict (Tmap l) (Pprod) (Dcorr l) (1 / l ^ 3) M μ hμD hinv hPbdd
    (fun orbit hmem hstep => perq_no_sustained_orbit l mpoly hF hmp h1 h2 hlo orbit hmem hstep)

/-! ### §12b. PER-Q SPECIALIZATIONS (q = 17,18,19,20,21).

For each q the F-window hypothesis is the CONCRETE per-q predicate `mpoly_q{q}` = the principal Hecke
minimal-polynomial identity (verbatim the `hps` of `g{q}_no_window_below_genuine`).  Each
`perq_essSup_ge_q{q}` is `perq_essSup_ge` specialized to that predicate: it takes the (discharged)
F-window `hF` and the per-q minimal-polynomial fact, and concludes `essSup Pprod ≥ 1/l³`.  The
intended caller plugs `g{q}_no_window_below_genuine` (axiom-clean, `BCZHeckeG{q}_window_VERIFIED.lean`)
for `hF` — that term has EXACTLY type `FwindowHyp mpoly_q{q}`, so the discharge is definitional. -/

/-- q=17 principal Hecke minimal polynomial (`hps` of `g17_no_window_below_genuine`). -/
def mpoly_q17 (lam : ℝ) : Prop :=
  lam^8 = lam^7 + 7*lam^6 - 6*lam^5 - 15*lam^4 + 10*lam^3 + 10*lam^2 - 4*lam - 1
/-- q=18 principal Hecke minimal polynomial (`hps` of `g18_no_window_below_genuine`). -/
def mpoly_q18 (lam : ℝ) : Prop := lam^6 = 6*lam^4 - 9*lam^2 + 3
/-- q=19 principal Hecke minimal polynomial (`hps` of `g19_no_window_below_genuine`). -/
def mpoly_q19 (lam : ℝ) : Prop :=
  lam^9 = lam^8 + 8*lam^7 - 7*lam^6 - 21*lam^5 + 15*lam^4 + 20*lam^3 - 10*lam^2 - 5*lam + 1
/-- q=20 principal Hecke minimal polynomial (`hps` of `g20_no_window_below_genuine`). -/
def mpoly_q20 (lam : ℝ) : Prop := lam^8 = 8*lam^6 - 19*lam^4 + 12*lam^2 - 1
/-- q=21 principal Hecke minimal polynomial (`hps` of `g21_no_window_below_genuine`). -/
def mpoly_q21 (lam : ℝ) : Prop :=
  lam^6 = -lam^5 + 6*lam^4 + 6*lam^3 - 8*lam^2 - 8*lam - 1

open MeasureTheory in
/-- **PER-Q LOWER BOUND, q=17.**  Discharge `hF` by `g17_no_window_below_genuine`. -/
theorem perq_essSup_ge_q17
    (hF : FwindowHyp mpoly_q17)
    (hmp : mpoly_q17 l) (h2 : l < 2) (hlo : (9:ℝ)/5 < l)
    (μ : MeasureTheory.Measure (ℝ × ℝ)) [MeasureTheory.IsProbabilityMeasure μ]
    (hμD : μ (Dcorr l)ᶜ = 0)
    (hinv : MeasureTheory.MeasurePreserving (Tmap l) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, Pprod x ≤ M) :
    1 / l ^ 3 ≤ essSup (Pprod) μ :=
  perq_essSup_ge l mpoly_q17 hF hmp (by linarith) h2 hlo μ hμD hinv M hPbdd

open MeasureTheory in
/-- **PER-Q LOWER BOUND, q=18.**  Discharge `hF` by `g18_no_window_below_genuine`. -/
theorem perq_essSup_ge_q18
    (hF : FwindowHyp mpoly_q18)
    (hmp : mpoly_q18 l) (h2 : l < 2) (hlo : (9:ℝ)/5 < l)
    (μ : MeasureTheory.Measure (ℝ × ℝ)) [MeasureTheory.IsProbabilityMeasure μ]
    (hμD : μ (Dcorr l)ᶜ = 0)
    (hinv : MeasureTheory.MeasurePreserving (Tmap l) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, Pprod x ≤ M) :
    1 / l ^ 3 ≤ essSup (Pprod) μ :=
  perq_essSup_ge l mpoly_q18 hF hmp (by linarith) h2 hlo μ hμD hinv M hPbdd

open MeasureTheory in
/-- **PER-Q LOWER BOUND, q=19.**  Discharge `hF` by `g19_no_window_below_genuine`. -/
theorem perq_essSup_ge_q19
    (hF : FwindowHyp mpoly_q19)
    (hmp : mpoly_q19 l) (h2 : l < 2) (hlo : (9:ℝ)/5 < l)
    (μ : MeasureTheory.Measure (ℝ × ℝ)) [MeasureTheory.IsProbabilityMeasure μ]
    (hμD : μ (Dcorr l)ᶜ = 0)
    (hinv : MeasureTheory.MeasurePreserving (Tmap l) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, Pprod x ≤ M) :
    1 / l ^ 3 ≤ essSup (Pprod) μ :=
  perq_essSup_ge l mpoly_q19 hF hmp (by linarith) h2 hlo μ hμD hinv M hPbdd

open MeasureTheory in
/-- **PER-Q LOWER BOUND, q=20.**  Discharge `hF` by `g20_no_window_below_genuine`. -/
theorem perq_essSup_ge_q20
    (hF : FwindowHyp mpoly_q20)
    (hmp : mpoly_q20 l) (h2 : l < 2) (hlo : (9:ℝ)/5 < l)
    (μ : MeasureTheory.Measure (ℝ × ℝ)) [MeasureTheory.IsProbabilityMeasure μ]
    (hμD : μ (Dcorr l)ᶜ = 0)
    (hinv : MeasureTheory.MeasurePreserving (Tmap l) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, Pprod x ≤ M) :
    1 / l ^ 3 ≤ essSup (Pprod) μ :=
  perq_essSup_ge l mpoly_q20 hF hmp (by linarith) h2 hlo μ hμD hinv M hPbdd

open MeasureTheory in
/-- **PER-Q LOWER BOUND, q=21.**  Discharge `hF` by `g21_no_window_below_genuine`. -/
theorem perq_essSup_ge_q21
    (hF : FwindowHyp mpoly_q21)
    (hmp : mpoly_q21 l) (h2 : l < 2) (hlo : (9:ℝ)/5 < l)
    (μ : MeasureTheory.Measure (ℝ × ℝ)) [MeasureTheory.IsProbabilityMeasure μ]
    (hμD : μ (Dcorr l)ᶜ = 0)
    (hinv : MeasureTheory.MeasurePreserving (Tmap l) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, Pprod x ≤ M) :
    1 / l ^ 3 ≤ essSup (Pprod) μ :=
  perq_essSup_ge l mpoly_q21 hF hmp (by linarith) h2 hlo μ hμD hinv M hPbdd

/-! ### §12c. SEQUENCE-LEVEL (C′) and the LEVEL-2 GENERAL-ORBIT conditional assembly.

The measure assembly above routes through `Tmap`-orbits.  For the general (multi-branch) orbit we
work at the sequence level, where the still-open combinatorial connective lives.  We re-expose the
two PROVEN mechanism pieces (deep-mid ejection, L2 switch-escape) in the per-q context, then state
the general conditional that wires all three (F-window + ejection + switch) through a single honestly
named confinement hypothesis. -/

/-- **Sequence-level per-q (C′)** (the scalar core, no measure).  A genuine scalar F-corridor
sequence `c` (positivity, cap, both Taha edges, floor recurrence) cannot keep EVERY consecutive
product `c_n·c_{n+1} < 1/l³`.  Direct from the F-window at `i=0`.  This is the exact sequence form the
general confinement reduces TO. -/
theorem perq_no_sustained_cseq
    (mpoly : ℝ → Prop) (hF : FwindowHyp mpoly)
    (hmp : mpoly l) (h1 : (1:ℝ) < l) (h2 : l < 2) (hlo : (9:ℝ)/5 < l)
    (c : ℕ → ℝ) (hposc : ∀ n, 0 < c n) (hcap : ∀ n, c n ≤ 1)
    (hreg : ∀ n, c n + l * c (n+1) > 1) (hgen : ∀ n, l * c n + c (n+1) > 1)
    (hrec : ∀ n, c n + c (n+2) = (⌊(1 + c n)/(l*c (n+1))⌋ : ℝ)*l*c (n+1)) :
    ¬ (∀ n, c n * c (n+1) < 1 / l ^ 3) := by
  intro hsub
  exact hF l hmp h1 h2 hlo c hposc hcap hreg hgen hrec 0
    ⟨hsub 0, hsub 1, hsub 2, hsub 3, hsub 4, hsub 5⟩

/-- **Deep-mid ejection, re-exposed for the per-q box (PROVEN — `genuine_ejection_floor1`).**  On the
deep-mid floor-1 branch (box q=16..21), a sub-threshold genuine observable forces the scalar
successor product `≥ thr` (dwell ≤ 1).  This is the proven fact that prevents deep-mid steps from
filling a sub-threshold window in the general orbit.  Verbatim re-export of the base lemma. -/
theorem perq_deepmid_eject (a b : ℝ) (n : ℕ) (k thr : ℝ)
    (hne : cheb l (n + 1) ≠ 0)
    (hl : (49:ℝ)/25 ≤ l) (hl' : l ≤ (99:ℝ)/50)
    (hr : (47:ℝ)/50 ≤ cheb l n / cheb l (n + 1)) (hr' : cheb l n / cheb l (n + 1) ≤ (61:ℝ)/50)
    (ht : (129:ℝ)/1000 ≤ thr) (ht' : thr ≤ (663:ℝ)/5000)
    (hentry : 1 < L l a b n) (hactive : L l a b (n + 1) ≤ 1)
    (hvpos : 0 < L l a b (n + 1))
    (hfloor : ⌊(1 + L l a b n) / (l * L l a b (n + 1))⌋ = 1)
    (hk : 0 ≤ k)
    (hP : Pobs l a b (n + 1) < thr) :
    thr ≤ succA l a b (n + 1) * succB l a b (n + 1) k :=
  genuine_ejection_floor1 l a b n k thr hne hl hl' hr hr' ht ht'
    hentry hactive hvpos hfloor hk hP

/-- **L2 switch-escape, re-exposed for the per-q context (PROVEN — `switch_forces_nonelliptic`).**
Any genuine F-family corridor SWITCH forces the chained composite trace `|tr| ≥ 2` (non-elliptic):
no new sub-threshold rotation can be sustained by switching corridors.  This is the proven fact that
collapses the `{q−1,q−3}` corridor to the scalar branch in the general orbit. -/
theorem perq_switch_escape
    (k₁ k₂ : ℝ) (h1 : k₁ = 1 ∨ k₁ = 2 ∨ k₁ = 3) (h2 : k₂ = 1 ∨ k₂ = 2 ∨ k₂ = 3)
    (hswitch : k₁ ≠ k₂ ∨ k₁ = 2 ∨ k₂ = 2) :
    2 ≤ |M2.tr (M2.mul (Fcorr l k₂) (Fcorr l k₁))| :=
  switch_forces_nonelliptic l k₁ k₂ h1 h2 hswitch

/-- **LEVEL-2 GENERAL-ORBIT (C′), conditional.**  Combines all three proven pieces.  A general genuine
q-orbit is modeled by its per-step genuine product observable `Q : ℕ → ℝ` (`Q n` is the gap product on
whatever branch step `n` lands).  The single honestly named residual hypothesis

  `hconfine` : if the general orbit is sub-threshold on a length-6 window, those six gap products are
               realized by a genuine SCALAR F-corridor sequence's consecutive products

is EXACTLY the still-open combinatorial connective (STUBs (A) torsion-classification + (B)
long-run→scalar of `BCZHeckeAssemblyQ18_skeleton`).  Its JUSTIFICATION is the two re-exposed proven
facts: deep-mid steps eject in ≤1 (`perq_deepmid_eject` / `genuine_ejection_floor1`) so cannot fill a
window, and corridor switches escape (`perq_switch_escape` / `switch_forces_nonelliptic`) so the
corridor collapses to scalar.  GIVEN `hconfine`, no general orbit keeps every `Q n < 1/l³`: a
sustained run yields (via `hconfine` at `i=0`) a genuine scalar sequence everywhere sub-threshold,
refuted by `perq_no_sustained_cseq` (the F-window).  Honest: only `hconfine` is unproven; F-window,
ejection, switch are all discharged. -/
theorem perq_general_no_sustained
    (mpoly : ℝ → Prop) (hF : FwindowHyp mpoly)
    (hmp : mpoly l) (h1 : (1:ℝ) < l) (h2 : l < 2) (hlo : (9:ℝ)/5 < l)
    (Q : ℕ → ℝ)
    (hconfine : (∀ j, Q j < 1 / l ^ 3) →
      ∃ (c : ℕ → ℝ),
        (∀ n, 0 < c n) ∧ (∀ n, c n ≤ 1) ∧
        (∀ n, c n + l * c (n+1) > 1) ∧ (∀ n, l * c n + c (n+1) > 1) ∧
        (∀ n, c n + c (n+2) = (⌊(1 + c n)/(l*c (n+1))⌋ : ℝ)*l*c (n+1)) ∧
        (∀ n, c n * c (n+1) < 1 / l ^ 3)) :
    ¬ (∀ n, Q n < 1 / l ^ 3) := by
  intro hsub
  obtain ⟨c, hposc, hcap, hreg, hgen, hrec, hcsub⟩ := hconfine hsub
  exact perq_no_sustained_cseq l mpoly hF hmp h1 h2 hlo c hposc hcap hreg hgen hrec hcsub

-- ===== TRACK torsion =====

-- ===== TRACK torsion =====
/-! ## §12. TORSION-QUANTIZATION of realizable single-corridor traces (target `torsion`).

`tr(F k) = l(k-2)` (`trace_Fcorr`). The single-corridor ELLIPTIC digits are `k ∈ {1,2,3}` (the
digits `switch_forces_nonelliptic` treats as the only single-corridor-elliptic ones). So the
realizable single-corridor traces are exactly `{l(k-2) : k ∈ {1,2,3}} = {-l, 0, l}`.

The algebraic encoding `λ = 2cos(π/q)` lets us define the algebraic value `2cos(jπ/q)` WITHOUT trig:
with `θ = π/q`, `l = 2cosθ`, the Chebyshev identity `cheb l n = sin(nθ)/sinθ` gives
`cheb l (j+1) − cheb l (j−1) = U_j − U_{j−2} = 2T_j = 2cos(jθ)`.  So define
`chebCos l j := cheb l (j+1) − cheb l (j−1)` = the algebraic `2cos(jπ/q)`.  We then show each
realizable trace equals an explicit `chebCos l j`, hence is quantized. -/

/-- Algebraic `2cos(jπ/q)` under `l = 2cos(π/q)`: `chebCos l j = cheb l (j+1) − cheb l (j−1)`
(`= U_j − U_{j−2} = 2T_j(l/2)`).  Pure algebra (no trig). -/
def chebCos (j : ℕ) : ℝ := cheb l (j + 1) - cheb l (j - 1)

/-- `chebCos l 1 = l` (the `k=3` trace `+l = 2cos(π/q)`, `j=1`). -/
theorem chebCos_one : chebCos l 1 = l := by
  show cheb l 2 - cheb l 0 = l
  rw [cheb_rec]; simp


/-- **Chebyshev–sine identity** (the trig bridge): with `l = 2 cos θ`,
`cheb l n · sin θ = sin (n θ)`.  Proven by two-step induction from the `cheb` recurrence and the
sine addition law.  This is what makes `cheb l n = U_{n-1}(cosθ) = sin(nθ)/sinθ`. -/
theorem cheb_sin (θ : ℝ) (n : ℕ) :
    cheb (2 * Real.cos θ) n * Real.sin θ = Real.sin ((n : ℝ) * θ) := by
  induction n using Nat.twoStepInduction with
  | zero => simp
  | one => simp [cheb_one]
  | more k ih1 ih2 =>
    have hrec : cheb (2 * Real.cos θ) (k + 2)
        = 2 * Real.cos θ * cheb (2 * Real.cos θ) (k + 1) - cheb (2 * Real.cos θ) k := cheb_rec _ k
    have key : Real.sin ((((k:ℕ) + 2 : ℕ)) * θ)
        = 2 * Real.cos θ * Real.sin (((k + 1 : ℕ)) * θ) - Real.sin (((k:ℕ)) * θ) := by
      push_cast
      have h1 : ((k:ℝ) + 2) * θ = (((k:ℝ)+1)*θ) + θ := by ring
      have h2 : ((k:ℝ)) * θ = (((k:ℝ)+1)*θ) - θ := by ring
      rw [h1, h2, Real.sin_add, Real.sin_sub]; ring
    rw [hrec, key]
    linear_combination (2 * Real.cos θ) * ih2 - ih1


/-- `cheb l (q−2) = l` from the boundary data `cheb l q = 0`, `cheb l (q−1) = 1`
(parametrize `q = m+2`: `cheb l m = l`).  One step of the recurrence run backwards. -/
theorem cheb_qm2_eq_l (m : ℕ)
    (hq0 : cheb l (m + 2) = 0) (hq1 : cheb l (m + 1) = 1) :
    cheb l m = l := by
  have hrec : cheb l (m + 2) = l * cheb l (m + 1) - cheb l m := cheb_rec l m
  rw [hq0, hq1] at hrec; linarith

/-- **`chebCos` at `j = q−1` is `−l`** (the `k=1` trace `2cos((q−1)π/q) = −2cos(π/q) = −l`).
Parametrize `q = m+2`, so `q−1 = m+1`: `chebCos l (m+1) = cheb l (m+2) − cheb l m = 0 − l = −l`. -/
theorem chebCos_qm1 (m : ℕ)
    (hq0 : cheb l (m + 2) = 0) (hq1 : cheb l (m + 1) = 1) :
    chebCos l (m + 1) = -l := by
  have hm : cheb l m = l := cheb_qm2_eq_l l m hq0 hq1
  simp only [chebCos, show (m + 1 + 1) = m + 2 from rfl, show (m + 1 - 1) = m from rfl]
  rw [hq0, hm]; ring

/-! ### Realizable single-corridor traces are exactly `{−l, 0, l}` = `{chebCos l j}`.

`tr(F k) = l(k−2)` (`trace_Fcorr`).  The single-corridor ELLIPTIC digits are `k ∈ {1,2,3}` (the
`switch_forces_nonelliptic` digit set).  Their traces:
`tr(F 1) = −l`, `tr(F 2) = 0`, `tr(F 3) = l`.  We match each to an explicit `chebCos l j`
(= algebraic `2cos(jπ/q)`): `j = q−1`, the trace-0 algebraic condition, `j = 1`. -/

/-- `tr(F 3) = l = chebCos l 1` (`j=1`, `2cos(π/q)`; UNCONDITIONAL). -/
theorem trace_F3_quantized : M2.tr (Fcorr l 3) = chebCos l 1 := by
  rw [trace_Fcorr, chebCos_one]; ring

/-- `tr(F 1) = −l = chebCos l (q−1)` (`j=q−1`, `2cos((q−1)π/q)`; needs the boundary data). -/
theorem trace_F1_quantized (m : ℕ)
    (hq0 : cheb l (m + 2) = 0) (hq1 : cheb l (m + 1) = 1) :
    M2.tr (Fcorr l 1) = chebCos l (m + 1) := by
  rw [trace_Fcorr, chebCos_qm1 l m hq0 hq1]; ring

/-- `tr(F 2) = 0`.  This is `chebCos l j` for any `j` with `cheb l (j+1) = cheb l (j−1)` — the
algebraic trace-0 / order-4 condition `2cos(jπ/q) = 0 ⟺ jπ/q = π/2 ⟺ 2j = q` (realized at `j=q/2`
for even `q`). -/
theorem trace_F2_zero : M2.tr (Fcorr l 2) = 0 := by
  rw [trace_Fcorr]; ring

/-- `tr(F 2) = chebCos l j` exactly when the algebraic order-4 condition `cheb l (j+1) = cheb l (j−1)`
holds (`2cos(jπ/q)=0`).  So the `k=2` trace is quantized as `2cos(jπ/q)` precisely at such `j`
(`j=q/2`, even `q`). -/
theorem trace_F2_quantized (j : ℕ) (hj : cheb l (j + 1) = cheb l (j - 1)) :
    M2.tr (Fcorr l 2) = chebCos l j := by
  rw [trace_F2_zero, chebCos, hj]; ring

/-! ### The trig bridge: `chebCos l j = 2cos(jπ/q)` literally. -/

/-- **`chebCos` IS `2cos(jθ)`** when `l = 2cosθ` and `sinθ ≠ 0` (`θ = π/q`, so `0 < θ < π`):
`chebCos l j = cheb l (j+1) − cheb l (j−1) = (sin((j+1)θ) − sin((j−1)θ))/sinθ = 2cos(jθ)`.
This makes the algebraic `chebCos` literally the geometric `2cos(jπ/q)`. -/
theorem chebCos_eq_two_cos (θ : ℝ) (j : ℕ) (hj : 1 ≤ j) (hs : Real.sin θ ≠ 0) :
    chebCos (2 * Real.cos θ) j = 2 * Real.cos ((j : ℝ) * θ) := by
  obtain ⟨j', rfl⟩ : ∃ j', j = j' + 1 := ⟨j - 1, by omega⟩
  have hp1 := cheb_sin θ (j' + 2)
  have hm1 := cheb_sin θ j'
  have hsub : ((j' + 1 : ℕ) : ℝ) = (j' : ℝ) + 1 := by push_cast; ring
  simp only [chebCos, show (j' + 1 + 1) = j' + 2 from rfl, show (j' + 1 - 1) = j' from rfl]
  -- (cheb(j'+2) − cheb j') · sinθ = sin((j'+2)θ) − sin(j'θ) = 2 cos((j'+1)θ) sinθ
  have key : Real.sin (((j':ℝ) + 2) * θ) - Real.sin ((j':ℝ) * θ)
      = 2 * Real.cos (((j':ℝ) + 1) * θ) * Real.sin θ := by
    have h1 : ((j':ℝ) + 2) * θ = (((j':ℝ)+1)*θ) + θ := by ring
    have h2 : ((j':ℝ)) * θ = (((j':ℝ)+1)*θ) - θ := by ring
    rw [h1, h2, Real.sin_add, Real.sin_sub]; ring
  have hcast2 : (((j' + 2 : ℕ)) : ℝ) = (j' : ℝ) + 2 := by push_cast; ring
  rw [hcast2] at hp1
  -- combine
  have hcomb : (cheb (2 * Real.cos θ) (j' + 2) - cheb (2 * Real.cos θ) j') * Real.sin θ
      = 2 * Real.cos (((j':ℝ) + 1) * θ) * Real.sin θ := by
    rw [sub_mul, hp1, hm1, key]
  have hfin := mul_right_cancel₀ hs hcomb
  rw [hfin, hsub]

/-! ### MASTER torsion-quantization statement.

Packaging: for `λ = 2cos(π/q)` (algebraic boundary `cheb l q = 0`, `cheb l (q−1) = 1`), the realizable
single-corridor traces (digits `k ∈ {1,2,3}`) all lie in the algebraic torsion set
`{chebCos l j : j}` = `{2cos(jπ/q) : j}`.  Stated as: each digit's trace equals some `chebCos l j`. -/

/-- **TORSION-QUANTIZATION (algebraic master, q = m+2).**  For every realizable single-corridor
digit `k ∈ {1,2,3}`, the trace `tr(F k)` equals `chebCos l j` for an explicit `j` — i.e. it lies in
the algebraic torsion set `{2cos(jπ/q)}`.  The witnesses: `k=3 ↦ j=1` (`+l`), `k=1 ↦ j=q−1` (`−l`),
`k=2 ↦ 0` (order-4 value, `chebCos l j` at any `j` with `cheb l (j+1)=cheb l (j−1)`). -/
theorem torsion_quantization (m : ℕ)
    (hq0 : cheb l (m + 2) = 0) (hq1 : cheb l (m + 1) = 1)
    (k : ℝ) (hk : k = 1 ∨ k = 2 ∨ k = 3) :
    (∃ j : ℕ, M2.tr (Fcorr l k) = chebCos l j) ∨ M2.tr (Fcorr l k) = 0 := by
  rcases hk with rfl | rfl | rfl
  · exact Or.inl ⟨m + 1, trace_F1_quantized l m hq0 hq1⟩
  · exact Or.inr (trace_F2_zero l)
  · exact Or.inl ⟨1, trace_F3_quantized l⟩

/-- **TORSION-QUANTIZATION (geometric corollary).**  Under `λ = 2cosθ`, `0 < θ < π` (`θ = π/q`),
with the boundary data, each realizable single-corridor trace is literally `2cos(jθ)` for an explicit
integer `j` (or `0`, the order-4 value `2cos(π/2)`).  This is the target statement "every realizable
corridor monodromy trace lies in `{2cos(jπ/q)}`", for single corridors. -/
theorem torsion_quantization_cos (θ : ℝ) (hθ : Real.sin θ ≠ 0) (m : ℕ)
    (hq0 : cheb (2 * Real.cos θ) (m + 2) = 0) (hq1 : cheb (2 * Real.cos θ) (m + 1) = 1)
    (k : ℝ) (hk : k = 1 ∨ k = 2 ∨ k = 3) :
    (∃ j : ℕ, 1 ≤ j ∧ M2.tr (Fcorr (2 * Real.cos θ) k) = 2 * Real.cos ((j : ℝ) * θ))
      ∨ M2.tr (Fcorr (2 * Real.cos θ) k) = 0 := by
  rcases hk with rfl | rfl | rfl
  · refine Or.inl ⟨m + 1, by omega, ?_⟩
    rw [trace_F1_quantized (2 * Real.cos θ) m hq0 hq1,
        chebCos_eq_two_cos θ (m + 1) (by omega) hθ]
  · exact Or.inr (trace_F2_zero (2 * Real.cos θ))
  · refine Or.inl ⟨1, le_refl 1, ?_⟩
    rw [trace_F3_quantized (2 * Real.cos θ), chebCos_eq_two_cos θ 1 (le_refl 1) hθ]

end
end HeckeGenuine

set_option maxHeartbeats 40000000
noncomputable section
open Int

/-- Interior-floor contradiction (K>=2 impossible inside a sub-threshold window): if a
middle coord `m` has `lam^4 m^2 < 1` (= the K>=2 bound) and a neighbour `n` with `lam^4 n^2
< 2` and edge `1 - lam m < n`, then False.  Uses only `9/5 < lam < 2` via `(lam^2-lam)^2
>= 2` — field-independent. -/
lemma g18_floor_helper (lam m n : ℝ) (h2 : (1:ℝ) < lam) (h3 : lam < 2)
    (hlo : (9:ℝ)/5 < lam) (hm : 0 < m) (hn : 0 < n)
    (hms : lam^4 * m^2 < 1) (hns : lam^4 * n^2 < 2) (hedge : 1 - lam*m < n) : False := by
  have hpos : (0:ℝ) < lam := by linarith
  have hl2 : (1:ℝ) < lam^2 := by nlinarith [h2]
  have hlm : lam^2 * m < 1 := by nlinarith [hms, mul_pos (mul_pos hpos hpos) hm, sq_nonneg (lam^2*m)]
  have hlm1 : lam*m < 1 := by nlinarith [hlm, hl2, hm, mul_pos hpos hm]
  have h1lm : (0:ℝ) < 1 - lam*m := by linarith
  have hnsq : (1 - lam*m)^2 < n^2 := by nlinarith [hedge, h1lm, hn]
  have hml : (36:ℝ)/25 ≤ lam^2 - lam := by nlinarith [mul_pos (show (0:ℝ)<lam-9/5 by linarith) (show (0:ℝ)<lam+4/5 by linarith)]
  have hKey : (2:ℝ) ≤ lam^4 - 2*lam^3 + lam^2 := by nlinarith [hml, sq_nonneg (lam^2-lam), mul_pos hpos (show (0:ℝ)<lam-1 by linarith)]
  have hA : lam^4 * (1 - lam*m)^2 < 2 := by nlinarith [hnsq, hns, mul_pos (mul_pos (mul_pos hpos hpos) hpos) hpos]
  nlinarith [hA, hKey, h1lm, hlm, hpos, hl2, mul_pos hpos h1lm, sq_nonneg (lam - lam^2*m), sq_nonneg (lam*(1-lam*m))]

lemma case_q18 (a b c d e f g lam : ℝ) (hps : lam^6 = 6*lam^4 - 9*lam^2 + 3) (h2 : (1:ℝ) < lam) (h3 : lam < 2)
    (hpa : 0 < a) (hpb : 0 < b) (hpc : 0 < c) (hpd : 0 < d) (hpe : 0 < e) (hpf : 0 < f) (hpg : 0 < g)
    (hca : a ≤ 1) (hcb : b ≤ 1) (hcc : c ≤ 1) (hcd : d ≤ 1) (hce : e ≤ 1) (hcf : f ≤ 1) (hcg : g ≤ 1)
    (hr0 : a+lam*b > 1) (hr1 : b+lam*c > 1) (hr2 : c+lam*d > 1) (hr3 : d+lam*e > 1) (hr4 : e+lam*f > 1) (hr5 : f+lam*g > 1)
    (hg0 : lam*a+b > 1) (hg1 : lam*b+c > 1) (hg2 : lam*c+d > 1) (hg3 : lam*d+e > 1) (hg4 : lam*e+f > 1) (hg5 : lam*f+g > 1)
    (hk0 : a+c = 1*lam*b) (hk1 : b+d = 1*lam*c) (hk2 : c+e = 1*lam*d) (hk3 : d+f = 1*lam*e) (hk4 : e+g = 1*lam*f)
    (hf0 : 1+a < (1+1)*(lam*b)) (hf1 : 1+b < (1+1)*(lam*c)) (hf2 : 1+c < (1+1)*(lam*d)) (hf3 : 1+d < (1+1)*(lam*e)) (hf4 : 1+e < (1+1)*(lam*f))
    (hP0 : a*b < 1/lam^3) (hP1 : b*c < 1/lam^3) (hP2 : c*d < 1/lam^3) (hP3 : d*e < 1/lam^3) (hP4 : e*f < 1/lam^3) (hP5 : f*g < 1/lam^3) :
    False := by
  have hpos : (0:ℝ) < lam := by linarith
  have hp3 : (0:ℝ) < lam^3 := by positivity
  have pos0 : (0:ℝ) ≤ a := le_of_lt hpa
  have pos1 : (0:ℝ) ≤ b := le_of_lt hpb
  have pos2 : (0:ℝ) ≤ c := le_of_lt hpc
  have pos3 : (0:ℝ) ≤ d := le_of_lt hpd
  have pos4 : (0:ℝ) ≤ e := le_of_lt hpe
  have pos5 : (0:ℝ) ≤ f := le_of_lt hpf
  have pos6 : (0:ℝ) ≤ g := le_of_lt hpg
  have cap0 : (0:ℝ) ≤ 1 - a := by nlinarith [hca]
  have cap1 : (0:ℝ) ≤ 1 - b := by nlinarith [hcb]
  have cap2 : (0:ℝ) ≤ 1 - c := by nlinarith [hcc]
  have cap3 : (0:ℝ) ≤ 1 - d := by nlinarith [hcd]
  have cap4 : (0:ℝ) ≤ 1 - e := by nlinarith [hce]
  have cap5 : (0:ℝ) ≤ 1 - f := by nlinarith [hcf]
  have cap6 : (0:ℝ) ≤ 1 - g := by nlinarith [hcg]
  have reg0 : (0:ℝ) ≤ a + b*lam - 1 := by nlinarith [hr0]
  have reg1 : (0:ℝ) ≤ b + c*lam - 1 := by nlinarith [hr1]
  have reg2 : (0:ℝ) ≤ c + d*lam - 1 := by nlinarith [hr2]
  have reg3 : (0:ℝ) ≤ d + e*lam - 1 := by nlinarith [hr3]
  have reg4 : (0:ℝ) ≤ e + f*lam - 1 := by nlinarith [hr4]
  have reg5 : (0:ℝ) ≤ f + g*lam - 1 := by nlinarith [hr5]
  have gen0 : (0:ℝ) ≤ a*lam + b - 1 := by nlinarith [hg0]
  have gen1 : (0:ℝ) ≤ b*lam + c - 1 := by nlinarith [hg1]
  have gen2 : (0:ℝ) ≤ c*lam + d - 1 := by nlinarith [hg2]
  have gen3 : (0:ℝ) ≤ d*lam + e - 1 := by nlinarith [hg3]
  have gen4 : (0:ℝ) ≤ e*lam + f - 1 := by nlinarith [hg4]
  have gen5 : (0:ℝ) ≤ f*lam + g - 1 := by nlinarith [hg5]
  have slk0 : (0:ℝ) ≤ -a*b*lam^3 + 1 := by
    have hh : (a*b)*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP0
    nlinarith [hh]
  have slk1 : (0:ℝ) ≤ -b*c*lam^3 + 1 := by
    have hh : (b*c)*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP1
    nlinarith [hh]
  have slk2 : (0:ℝ) ≤ -c*d*lam^3 + 1 := by
    have hh : (c*d)*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP2
    nlinarith [hh]
  have slk3 : (0:ℝ) ≤ -d*e*lam^3 + 1 := by
    have hh : (d*e)*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP3
    nlinarith [hh]
  have slk4 : (0:ℝ) ≤ -e*f*lam^3 + 1 := by
    have hh : (e*f)*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP4
    nlinarith [hh]
  have slk5 : (0:ℝ) ≤ -f*g*lam^3 + 1 := by
    have hh : (f*g)*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP5
    nlinarith [hh]
  have flu0 : (0:ℝ) ≤ -a + 2*b*lam - 1 := by nlinarith [hf0]
  have flu1 : (0:ℝ) ≤ -b + 2*c*lam - 1 := by nlinarith [hf1]
  have flu2 : (0:ℝ) ≤ -c + 2*d*lam - 1 := by nlinarith [hf2]
  have flu3 : (0:ℝ) ≤ -d + 2*e*lam - 1 := by nlinarith [hf3]
  have flu4 : (0:ℝ) ≤ -e + 2*f*lam - 1 := by nlinarith [hf4]
  have qq0 : (0:ℝ) ≤ a^2*lam^2 + a*b*lam - a*lam := by
    have hr : (0:ℝ) ≤ lam*((a)*(a*lam + b - 1)) := mul_nonneg hpos.le (mul_nonneg pos0 gen0)
    have he : lam*((a)*(a*lam + b - 1)) = a^2*lam^2 + a*b*lam - a*lam := by linear_combination 0
    linarith [hr, he]
  have qq1 : (0:ℝ) ≤ -a^2*lam^3 + a*b*lam^4 - 2*a*b*lam^2 + a*lam^2 + b^2*lam^3 - b^2*lam - b*lam^3 + b*lam := by
    have hr : (0:ℝ) ≤ lam*((d)*(a*lam + b - 1)) := mul_nonneg hpos.le (mul_nonneg pos3 gen0)
    have he : lam*((d)*(a*lam + b - 1)) = -a^2*lam^3 + a*b*lam^4 - 2*a*b*lam^2 + a*lam^2 + b^2*lam^3 - b^2*lam - b*lam^3 + b*lam := by linear_combination (a*lam^3 + b*lam^2 - lam^2)*hk0 + (a*lam^2 + b*lam - lam)*hk1
    linarith [hr, he]
  have qq2 : (0:ℝ) ≤ 6*a^3*lam^4 - 9*a^3*lam^2 + 3*a^3 - 16*a^2*b*lam^5 + 27*a^2*b*lam^3 - 9*a^2*b*lam + 58*a*b^2*lam^4 - 117*a*b^2*lam^2 + 42*a*b^2 - a*lam^2 - 16*b^3*lam^5 + 33*b^3*lam^3 - 12*b^3*lam + b*lam^3 - b*lam := by
    have hr : (0:ℝ) ≤ lam*((d)*(-c*d*lam^3 + 1)) := mul_nonneg hpos.le (mul_nonneg pos3 slk2)
    have he : lam*((d)*(-c*d*lam^3 + 1)) = 6*a^3*lam^4 - 9*a^3*lam^2 + 3*a^3 - 16*a^2*b*lam^5 + 27*a^2*b*lam^3 - 9*a^2*b*lam + 58*a*b^2*lam^4 - 117*a*b^2*lam^2 + 42*a*b^2 - a*lam^2 - 16*b^3*lam^5 + 33*b^3*lam^3 - 12*b^3*lam + b*lam^3 - b*lam := by linear_combination (-a^2*lam^6 + 2*a*b*lam^7 - a*b*lam^5 + a*d*lam^5 - b^2*lam^8 + b^2*lam^6 - b*d*lam^6 - d^2*lam^4 + lam^2)*hk0 + (-a^2*lam^5 + 2*a*b*lam^6 - a*b*lam^4 + a*d*lam^4 - b^2*lam^7 + b^2*lam^5 - b*d*lam^5 + lam)*hk1 + (a^3 - 3*a^2*b*lam + 3*a*b^2*lam^2 + 14*a*b^2 - b^3*lam^3 - 4*b^3*lam)*hps
    linarith [hr, he]
  have qq3 : (0:ℝ) ≤ 21*a^3*lam^4 - 42*a^3*lam^2 + 15*a^3 - 47*a^2*b*lam^5 + 99*a^2*b*lam^3 - 36*a^2*b*lam + 131*a*b^2*lam^4 - 279*a*b^2*lam^2 + 102*a*b^2 - a*lam^2 - 31*b^3*lam^5 + 66*b^3*lam^3 - 24*b^3*lam + b*lam^3 - b*lam := by
    have hr : (0:ℝ) ≤ lam*((d)*(-d*e*lam^3 + 1)) := mul_nonneg hpos.le (mul_nonneg pos3 slk3)
    have he : lam*((d)*(-d*e*lam^3 + 1)) = 21*a^3*lam^4 - 42*a^3*lam^2 + 15*a^3 - 47*a^2*b*lam^5 + 99*a^2*b*lam^3 - 36*a^2*b*lam + 131*a*b^2*lam^4 - 279*a*b^2*lam^2 + 102*a*b^2 - a*lam^2 - 31*b^3*lam^5 + 66*b^3*lam^3 - 24*b^3*lam + b*lam^3 - b*lam := by linear_combination (-a^2*lam^8 + a^2*lam^6 + 2*a*b*lam^9 - 4*a*b*lam^7 + 2*a*b*lam^5 + a*e*lam^6 - b^2*lam^10 + 3*b^2*lam^8 - 3*b^2*lam^6 + b^2*lam^4 - b*e*lam^7 + b*e*lam^5 - d*e*lam^5 + lam^2)*hk0 + (-a^2*lam^7 + 2*a*b*lam^8 - 2*a*b*lam^6 + a*e*lam^5 - b^2*lam^9 + 2*b^2*lam^7 - b^2*lam^5 - b*e*lam^6 + b*e*lam^4 - d*e*lam^4 + lam)*hk1 + (-a^2*lam^6 + 2*a*b*lam^7 - 2*a*b*lam^5 - b^2*lam^8 + 2*b^2*lam^6 - b^2*lam^4)*hk2 + (a^3*lam^2 + 5*a^3 - 3*a^2*b*lam^3 - 12*a^2*b*lam + 3*a*b^2*lam^4 + 9*a*b^2*lam^2 + 34*a*b^2 - b^3*lam^5 - 2*b^3*lam^3 - 8*b^3*lam)*hps
    linarith [hr, he]
  have qq4 : (0:ℝ) ≤ 4*a^2*lam^4 - 10*a^2*lam^2 + 3*a^2 - 3*a*b*lam^5 + 9*a*b*lam^3 - 4*a*b*lam - 4*a*lam^4 + 10*a*lam^2 + a*lam - 3*a + 3*b*lam^5 - 9*b*lam^3 + 4*b*lam - lam := by
    have hr : (0:ℝ) ≤ lam*((1 - a)*(f + g*lam - 1)) := mul_nonneg hpos.le (mul_nonneg cap0 reg5)
    have he : lam*((1 - a)*(f + g*lam - 1)) = 4*a^2*lam^4 - 10*a^2*lam^2 + 3*a^2 - 3*a*b*lam^5 + 9*a*b*lam^3 - 4*a*b*lam - 4*a*lam^4 + 10*a*lam^2 + a*lam - 3*a + 3*b*lam^5 - 9*b*lam^3 + 4*b*lam - lam := by linear_combination (-a*lam^6 + 2*a*lam^4 + a*lam^2 + lam^6 - 2*lam^4 - lam^2)*hk0 + (-a*lam^5 + a*lam^3 + a*lam + lam^5 - lam^3 - lam)*hk1 + (-a*lam^4 + lam^4)*hk2 + (-a*lam^3 - a*lam + lam^3 + lam)*hk3 + (-a*lam^2 + lam^2)*hk4 + (a^2 - a*b*lam - a + b*lam)*hps
    linarith [hr, he]
  have qq5 : (0:ℝ) ≤ -a^2*lam^2 - a*b*lam + a*lam^2 + a*lam + b*lam - lam := by
    have hr : (0:ℝ) ≤ lam*((1 - a)*(a*lam + b - 1)) := mul_nonneg hpos.le (mul_nonneg cap0 gen0)
    have he : lam*((1 - a)*(a*lam + b - 1)) = -a^2*lam^2 - a*b*lam + a*lam^2 + a*lam + b*lam - lam := by linear_combination 0
    linarith [hr, he]
  have qq6 : (0:ℝ) ≤ 4*a*b*lam^4 - 10*a*b*lam^2 + 3*a*b - 4*a*lam^4 + 10*a*lam^2 - 3*a - 3*b^2*lam^5 + 9*b^2*lam^3 - 4*b^2*lam + 3*b*lam^5 - 9*b*lam^3 + 5*b*lam - lam := by
    have hr : (0:ℝ) ≤ lam*((1 - b)*(f + g*lam - 1)) := mul_nonneg hpos.le (mul_nonneg cap1 reg5)
    have he : lam*((1 - b)*(f + g*lam - 1)) = 4*a*b*lam^4 - 10*a*b*lam^2 + 3*a*b - 4*a*lam^4 + 10*a*lam^2 - 3*a - 3*b^2*lam^5 + 9*b^2*lam^3 - 4*b^2*lam + 3*b*lam^5 - 9*b*lam^3 + 5*b*lam - lam := by linear_combination (-b*lam^6 + 2*b*lam^4 + b*lam^2 + lam^6 - 2*lam^4 - lam^2)*hk0 + (-b*lam^5 + b*lam^3 + b*lam + lam^5 - lam^3 - lam)*hk1 + (-b*lam^4 + lam^4)*hk2 + (-b*lam^3 - b*lam + lam^3 + lam)*hk3 + (-b*lam^2 + lam^2)*hk4 + (a*b - a - b^2*lam + b*lam)*hps
    linarith [hr, he]
  have qq7 : (0:ℝ) ≤ -a*b*lam^2 + a*lam^2 - b^2*lam + 2*b*lam - lam := by
    have hr : (0:ℝ) ≤ lam*((1 - b)*(a*lam + b - 1)) := mul_nonneg hpos.le (mul_nonneg cap1 gen0)
    have he : lam*((1 - b)*(a*lam + b - 1)) = -a*b*lam^2 + a*lam^2 - b^2*lam + 2*b*lam - lam := by linear_combination 0
    linarith [hr, he]
  have qq8 : (0:ℝ) ≤ a^2*b*lam^5 - a^2*lam^5 - 11*a*b^2*lam^4 + 18*a*b^2*lam^2 - 6*a*b^2 + 11*a*b*lam^4 - 18*a*b*lam^2 + 6*a*b + 5*b^3*lam^5 - 9*b^3*lam^3 + 3*b^3*lam - 5*b^2*lam^5 + 9*b^2*lam^3 - 3*b^2*lam - b*lam + lam := by
    have hr : (0:ℝ) ≤ lam*((1 - b)*(-c*d*lam^3 + 1)) := mul_nonneg hpos.le (mul_nonneg cap1 slk2)
    have he : lam*((1 - b)*(-c*d*lam^3 + 1)) = a^2*b*lam^5 - a^2*lam^5 - 11*a*b^2*lam^4 + 18*a*b^2*lam^2 - 6*a*b^2 + 11*a*b*lam^4 - 18*a*b*lam^2 + 6*a*b + 5*b^3*lam^5 - 9*b^3*lam^3 + 3*b^3*lam - 5*b^2*lam^5 + 9*b^2*lam^3 - 3*b^2*lam - b*lam + lam := by linear_combination (-a*b*lam^5 + a*lam^5 + b^2*lam^6 + b*d*lam^4 - b*lam^6 - d*lam^4)*hk0 + (-a*b*lam^4 + a*lam^4 + b^2*lam^5 - b*lam^5)*hk1 + (-2*a*b^2 + 2*a*b + b^3*lam - b^2*lam)*hps
    linarith [hr, he]
  have qq9 : (0:ℝ) ≤ 5*a^2*b*lam^5 - 9*a^2*b*lam^3 + 3*a^2*b*lam - 5*a^2*lam^5 + 9*a^2*lam^3 - 3*a^2*lam - 31*a*b^2*lam^4 + 66*a*b^2*lam^2 - 24*a*b^2 + 31*a*b*lam^4 - 66*a*b*lam^2 + 24*a*b + 11*b^3*lam^5 - 24*b^3*lam^3 + 9*b^3*lam - 11*b^2*lam^5 + 24*b^2*lam^3 - 9*b^2*lam - b*lam + lam := by
    have hr : (0:ℝ) ≤ lam*((1 - b)*(-d*e*lam^3 + 1)) := mul_nonneg hpos.le (mul_nonneg cap1 slk3)
    have he : lam*((1 - b)*(-d*e*lam^3 + 1)) = 5*a^2*b*lam^5 - 9*a^2*b*lam^3 + 3*a^2*b*lam - 5*a^2*lam^5 + 9*a^2*lam^3 - 3*a^2*lam - 31*a*b^2*lam^4 + 66*a*b^2*lam^2 - 24*a*b^2 + 31*a*b*lam^4 - 66*a*b*lam^2 + 24*a*b + 11*b^3*lam^5 - 24*b^3*lam^3 + 9*b^3*lam - 11*b^2*lam^5 + 24*b^2*lam^3 - 9*b^2*lam - b*lam + lam := by linear_combination (-a*b*lam^7 + a*b*lam^5 + a*lam^7 - a*lam^5 + b^2*lam^8 - 2*b^2*lam^6 + b^2*lam^4 + b*e*lam^5 - b*lam^8 + 2*b*lam^6 - b*lam^4 - e*lam^5)*hk0 + (-a*b*lam^6 + a*lam^6 + b^2*lam^7 - b^2*lam^5 + b*e*lam^4 - b*lam^7 + b*lam^5 - e*lam^4)*hk1 + (-a*b*lam^5 + a*lam^5 + b^2*lam^6 - b^2*lam^4 - b*lam^6 + b*lam^4)*hk2 + (a^2*b*lam - a^2*lam - 2*a*b^2*lam^2 - 8*a*b^2 + 2*a*b*lam^2 + 8*a*b + b^3*lam^3 + 3*b^3*lam - b^2*lam^3 - 3*b^2*lam)*hps
    linarith [hr, he]
  have qq10 : (0:ℝ) ≤ a^2*lam^2 - a*b*lam^3 + a*b*lam + a*lam^2 - a*lam - b^2*lam^2 + b*lam^2 + b*lam - lam := by
    have hr : (0:ℝ) ≤ lam*((1 - c)*(a*lam + b - 1)) := mul_nonneg hpos.le (mul_nonneg cap2 gen0)
    have he : lam*((1 - c)*(a*lam + b - 1)) = a^2*lam^2 - a*b*lam^3 + a*b*lam + a*lam^2 - a*lam - b^2*lam^2 + b*lam^2 + b*lam - lam := by linear_combination (-a*lam^2 - b*lam + lam)*hk0
    linarith [hr, he]
  have qq11 : (0:ℝ) ≤ -10*a^2*lam^4 + 23*a^2*lam^2 - 9*a^2 + 12*a*b*lam^5 - 27*a*b*lam^3 + 11*a*b*lam - 4*a*lam^4 - a*lam^3 + 10*a*lam^2 + a*lam - 3*a - 13*b^2*lam^4 + 26*b^2*lam^2 - 9*b^2 + 3*b*lam^5 + b*lam^4 - 9*b*lam^3 - 2*b*lam^2 + 4*b*lam - lam := by
    have hr : (0:ℝ) ≤ lam*((1 - e)*(f + g*lam - 1)) := mul_nonneg hpos.le (mul_nonneg cap4 reg5)
    have he : lam*((1 - e)*(f + g*lam - 1)) = -10*a^2*lam^4 + 23*a^2*lam^2 - 9*a^2 + 12*a*b*lam^5 - 27*a*b*lam^3 + 11*a*b*lam - 4*a*lam^4 - a*lam^3 + 10*a*lam^2 + a*lam - 3*a - 13*b^2*lam^4 + 26*b^2*lam^2 - 9*b^2 + 3*b*lam^5 + b*lam^4 - 9*b*lam^3 - 2*b*lam^2 + 4*b*lam - lam := by linear_combination (a*lam^8 - 3*a*lam^6 + a*lam^4 + a*lam^2 - b*lam^9 + 4*b*lam^7 - 3*b*lam^5 - 2*b*lam^3 - f*lam^3 + f*lam - g*lam^4 + g*lam^2 + lam^6 - 2*lam^4 + lam^3 - lam^2 - lam)*hk0 + (a*lam^7 - 2*a*lam^5 + a*lam - b*lam^8 + 3*b*lam^6 - b*lam^4 - 2*b*lam^2 - f*lam^2 - g*lam^3 + lam^5 - lam^3 + lam^2 - lam)*hk1 + (a*lam^6 - a*lam^4 - b*lam^7 + 2*b*lam^5 - f*lam - g*lam^2 + lam^4 + lam)*hk2 + (a*lam^5 - a*lam - b*lam^6 + b*lam^4 + 2*b*lam^2 + lam^3 + lam)*hk3 + (a*lam^4 - a*lam^2 - b*lam^5 + 2*b*lam^3 + lam^2)*hk4 + (-a^2*lam^2 - 3*a^2 + 2*a*b*lam^3 + 4*a*b*lam - a - b^2*lam^4 - b^2*lam^2 - 3*b^2 + b*lam)*hps
    linarith [hr, he]
  have qq12 : (0:ℝ) ≤ a^2*lam^4 - a^2*lam^2 - a*b*lam^5 + 3*a*b*lam^3 - a*b*lam - a*lam^3 + a*lam^2 + a*lam - b^2*lam^4 + 2*b^2*lam^2 + b*lam^4 - 2*b*lam^2 + b*lam - lam := by
    have hr : (0:ℝ) ≤ lam*((1 - e)*(a*lam + b - 1)) := mul_nonneg hpos.le (mul_nonneg cap4 gen0)
    have he : lam*((1 - e)*(a*lam + b - 1)) = a^2*lam^4 - a^2*lam^2 - a*b*lam^5 + 3*a*b*lam^3 - a*b*lam - a*lam^3 + a*lam^2 + a*lam - b^2*lam^4 + 2*b^2*lam^2 + b*lam^4 - 2*b*lam^2 + b*lam - lam := by linear_combination (-a*lam^4 + a*lam^2 - b*lam^3 + b*lam + lam^3 - lam)*hk0 + (-a*lam^3 - b*lam^2 + lam^2)*hk1 + (-a*lam^2 - b*lam + lam)*hk2
    linarith [hr, he]
  have qq13 : (0:ℝ) ≤ -6*a^2*lam^5 + 13*a^2*lam^3 - 6*a^2*lam + 26*a*b*lam^4 - 51*a*b*lam^2 + 18*a*b - 5*a*lam^4 + 12*a*lam^2 - 3*a - 7*b^2*lam^5 + 12*b^2*lam^3 - 4*b^2*lam + 4*b*lam^5 - 12*b*lam^3 + 5*b*lam - lam := by
    have hr : (0:ℝ) ≤ lam*((1 - f)*(f + g*lam - 1)) := mul_nonneg hpos.le (mul_nonneg cap5 reg5)
    have he : lam*((1 - f)*(f + g*lam - 1)) = -6*a^2*lam^5 + 13*a^2*lam^3 - 6*a^2*lam + 26*a*b*lam^4 - 51*a*b*lam^2 + 18*a*b - 5*a*lam^4 + 12*a*lam^2 - 3*a - 7*b^2*lam^5 + 12*b^2*lam^3 - 4*b^2*lam + 4*b*lam^5 - 12*b*lam^3 + 5*b*lam - lam := by linear_combination (a*lam^9 - 4*a*lam^7 + 3*a*lam^5 + 2*a*lam^3 - b*lam^10 + 5*b*lam^8 - 6*b*lam^6 - b*lam^4 + b*lam^2 - f*lam^4 + 2*f*lam^2 - g*lam^5 + 2*g*lam^3 + lam^6 - lam^4 - 3*lam^2)*hk0 + (a*lam^8 - 3*a*lam^6 + a*lam^4 + 2*a*lam^2 - b*lam^9 + 4*b*lam^7 - 3*b*lam^5 - 2*b*lam^3 + b*lam - f*lam^3 + f*lam - g*lam^4 + g*lam^2 + lam^5 - 2*lam)*hk1 + (a*lam^7 - 2*a*lam^5 - b*lam^8 + 3*b*lam^6 - b*lam^4 - f*lam^2 - g*lam^3 + lam^4 + lam^2)*hk2 + (a*lam^6 - a*lam^4 - 2*a*lam^2 - b*lam^7 + 2*b*lam^5 + 2*b*lam^3 - b*lam - f*lam - g*lam^2 + lam^3 + 2*lam)*hk3 + (a*lam^5 - 2*a*lam^3 - b*lam^6 + 3*b*lam^4 - b*lam^2 + lam^2)*hk4 + (-a^2*lam^3 - 2*a^2*lam + 2*a*b*lam^4 + 2*a*b*lam^2 + 6*a*b - a - b^2*lam^5 - b^2*lam + b*lam)*hps
    linarith [hr, he]
  have qq14 : (0:ℝ) ≤ a^2*lam^5 - 2*a^2*lam^3 - 2*a*b*lam^4 + 6*a*b*lam^2 - 3*a*b - a*lam^4 + 3*a*lam^2 - b^2*lam^5 + 3*b^2*lam^3 - b^2*lam + b*lam^5 - 3*b*lam^3 + 2*b*lam - lam := by
    have hr : (0:ℝ) ≤ lam*((1 - f)*(a*lam + b - 1)) := mul_nonneg hpos.le (mul_nonneg cap5 gen0)
    have he : lam*((1 - f)*(a*lam + b - 1)) = a^2*lam^5 - 2*a^2*lam^3 - 2*a*b*lam^4 + 6*a*b*lam^2 - 3*a*b - a*lam^4 + 3*a*lam^2 - b^2*lam^5 + 3*b^2*lam^3 - b^2*lam + b*lam^5 - 3*b*lam^3 + 2*b*lam - lam := by linear_combination (-a*lam^5 + 2*a*lam^3 - b*lam^4 + 2*b*lam^2 + lam^4 - 2*lam^2)*hk0 + (-a*lam^4 + a*lam^2 - b*lam^3 + b*lam + lam^3 - lam)*hk1 + (-a*lam^3 - b*lam^2 + lam^2)*hk2 + (-a*lam^2 - b*lam + lam)*hk3 + (-a*b)*hps
    linarith [hr, he]
  have qq15 : (0:ℝ) ≤ -15*a^3*lam^4 + 33*a^3*lam^2 - 12*a^3 + 36*a^2*b*lam^5 - 81*a^2*b*lam^3 + 30*a^2*b*lam - a^2*lam^5 - 104*a*b^2*lam^4 + 228*a*b^2*lam^2 - 84*a*b^2 + 11*a*b*lam^4 - 18*a*b*lam^2 + 6*a*b + a*lam^4 - 2*a*lam^2 + 26*b^3*lam^5 - 57*b^3*lam^3 + 21*b^3*lam - 5*b^2*lam^5 + 9*b^2*lam^3 - 3*b^2*lam - b*lam^5 + 3*b*lam^3 - b*lam + lam := by
    have hr : (0:ℝ) ≤ lam*((1 - f)*(-c*d*lam^3 + 1)) := mul_nonneg hpos.le (mul_nonneg cap5 slk2)
    have he : lam*((1 - f)*(-c*d*lam^3 + 1)) = -15*a^3*lam^4 + 33*a^3*lam^2 - 12*a^3 + 36*a^2*b*lam^5 - 81*a^2*b*lam^3 + 30*a^2*b*lam - a^2*lam^5 - 104*a*b^2*lam^4 + 228*a*b^2*lam^2 - 84*a*b^2 + 11*a*b*lam^4 - 18*a*b*lam^2 + 6*a*b + a*lam^4 - 2*a*lam^2 + 26*b^3*lam^5 - 57*b^3*lam^3 + 21*b^3*lam - 5*b^2*lam^5 + 9*b^2*lam^3 - 3*b^2*lam - b*lam^5 + 3*b*lam^3 - b*lam + lam := by linear_combination (a^2*lam^8 - 2*a^2*lam^6 - 2*a*b*lam^9 + 5*a*b*lam^7 - 2*a*b*lam^5 - a*f*lam^5 + a*lam^5 + b^2*lam^10 - 3*b^2*lam^8 + 2*b^2*lam^6 + b*f*lam^6 - b*lam^6 + d*f*lam^4 - d*lam^4 - lam^4 + 2*lam^2)*hk0 + (a^2*lam^7 - a^2*lam^5 - 2*a*b*lam^8 + 3*a*b*lam^6 - a*b*lam^4 - a*f*lam^4 + a*lam^4 + b^2*lam^9 - 2*b^2*lam^7 + b^2*lam^5 + b*f*lam^5 - b*lam^5 - lam^3 + lam)*hk1 + (a^2*lam^6 - 2*a*b*lam^7 + a*b*lam^5 + b^2*lam^8 - b^2*lam^6 - lam^2)*hk2 + (a^2*lam^5 - 2*a*b*lam^6 + a*b*lam^4 + b^2*lam^7 - b^2*lam^5 - lam)*hk3 + (-a^3*lam^2 - 4*a^3 + 3*a^2*b*lam^3 + 10*a^2*b*lam - 3*a*b^2*lam^4 - 8*a*b^2*lam^2 - 28*a*b^2 + 2*a*b + b^3*lam^5 + 2*b^3*lam^3 + 7*b^3*lam - b^2*lam)*hps
    linarith [hr, he]
  have qq16 : (0:ℝ) ≤ -42*a^3*lam^4 + 90*a^3*lam^2 - 33*a^3 + 84*a^2*b*lam^5 - 180*a^2*b*lam^3 + 66*a^2*b*lam - 5*a^2*lam^5 + 9*a^2*lam^3 - 3*a^2*lam - 214*a*b^2*lam^4 + 453*a*b^2*lam^2 - 165*a*b^2 + 31*a*b*lam^4 - 66*a*b*lam^2 + 24*a*b + a*lam^4 - 2*a*lam^2 + 47*b^3*lam^5 - 99*b^3*lam^3 + 36*b^3*lam - 11*b^2*lam^5 + 24*b^2*lam^3 - 9*b^2*lam - b*lam^5 + 3*b*lam^3 - b*lam + lam := by
    have hr : (0:ℝ) ≤ lam*((1 - f)*(-d*e*lam^3 + 1)) := mul_nonneg hpos.le (mul_nonneg cap5 slk3)
    have he : lam*((1 - f)*(-d*e*lam^3 + 1)) = -42*a^3*lam^4 + 90*a^3*lam^2 - 33*a^3 + 84*a^2*b*lam^5 - 180*a^2*b*lam^3 + 66*a^2*b*lam - 5*a^2*lam^5 + 9*a^2*lam^3 - 3*a^2*lam - 214*a*b^2*lam^4 + 453*a*b^2*lam^2 - 165*a*b^2 + 31*a*b*lam^4 - 66*a*b*lam^2 + 24*a*b + a*lam^4 - 2*a*lam^2 + 47*b^3*lam^5 - 99*b^3*lam^3 + 36*b^3*lam - 11*b^2*lam^5 + 24*b^2*lam^3 - 9*b^2*lam - b*lam^5 + 3*b*lam^3 - b*lam + lam := by linear_combination (a^2*lam^10 - 3*a^2*lam^8 + 2*a^2*lam^6 - 2*a*b*lam^11 + 8*a*b*lam^9 - 9*a*b*lam^7 + 2*a*b*lam^5 - a*f*lam^7 + a*f*lam^5 + a*lam^7 - a*lam^5 + b^2*lam^12 - 5*b^2*lam^10 + 8*b^2*lam^8 - 4*b^2*lam^6 + b*f*lam^8 - 2*b*f*lam^6 + b*f*lam^4 - b*lam^8 + 2*b*lam^6 - b*lam^4 + e*f*lam^5 - e*lam^5 - lam^4 + 2*lam^2)*hk0 + (a^2*lam^9 - 2*a^2*lam^7 + a^2*lam^5 - 2*a*b*lam^10 + 6*a*b*lam^8 - 5*a*b*lam^6 + a*b*lam^4 - a*f*lam^6 + a*lam^6 + b^2*lam^11 - 4*b^2*lam^9 + 5*b^2*lam^7 - 2*b^2*lam^5 + b*f*lam^7 - b*f*lam^5 - b*lam^7 + b*lam^5 + e*f*lam^4 - e*lam^4 - lam^3 + lam)*hk1 + (a^2*lam^8 - a^2*lam^6 - 2*a*b*lam^9 + 4*a*b*lam^7 - a*b*lam^5 - a*f*lam^5 + a*lam^5 + b^2*lam^10 - 3*b^2*lam^8 + 2*b^2*lam^6 + b*f*lam^6 - b*f*lam^4 - b*lam^6 + b*lam^4 - lam^2)*hk2 + (a^2*lam^7 - a^2*lam^5 - 2*a*b*lam^8 + 4*a*b*lam^6 - a*b*lam^4 + b^2*lam^9 - 3*b^2*lam^7 + 2*b^2*lam^5 - lam)*hk3 + (-a^3*lam^4 - 3*a^3*lam^2 - 11*a^3 + 3*a^2*b*lam^5 + 6*a^2*b*lam^3 + 22*a^2*b*lam - a^2*lam - 3*a*b^2*lam^6 - 3*a*b^2*lam^4 - 14*a*b^2*lam^2 - 55*a*b^2 + 2*a*b*lam^2 + 8*a*b + b^3*lam^7 + 3*b^3*lam^3 + 12*b^3*lam - b^2*lam^3 - 3*b^2*lam)*hps
    linarith [hr, he]
  have qq17 : (0:ℝ) ≤ -13*a^2*lam^4 + 25*a^2*lam^2 - 9*a^2 + 14*a*b*lam^5 - 24*a*b*lam^3 + 7*a*b*lam - a*lam^5 - 4*a*lam^4 + 3*a*lam^3 + 10*a*lam^2 - a*lam - 3*a - 17*b^2*lam^4 + 33*b^2*lam^2 - 12*b^2 + 3*b*lam^5 + 2*b*lam^4 - 9*b*lam^3 - 6*b*lam^2 + 4*b*lam + 3*b - lam := by
    have hr : (0:ℝ) ≤ lam*((1 - g)*(f + g*lam - 1)) := mul_nonneg hpos.le (mul_nonneg cap6 reg5)
    have he : lam*((1 - g)*(f + g*lam - 1)) = -13*a^2*lam^4 + 25*a^2*lam^2 - 9*a^2 + 14*a*b*lam^5 - 24*a*b*lam^3 + 7*a*b*lam - a*lam^5 - 4*a*lam^4 + 3*a*lam^3 + 10*a*lam^2 - a*lam - 3*a - 17*b^2*lam^4 + 33*b^2*lam^2 - 12*b^2 + 3*b*lam^5 + 2*b*lam^4 - 9*b*lam^3 - 6*b*lam^2 + 4*b*lam + 3*b - lam := by linear_combination (a*lam^10 - 5*a*lam^8 + 6*a*lam^6 + a*lam^4 - a*lam^2 - b*lam^11 + 6*b*lam^9 - 10*b*lam^7 + 2*b*lam^5 + 3*b*lam^3 - b*lam - g*lam^6 + 2*g*lam^4 + g*lam^2 + lam^6 + lam^5 - 2*lam^4 - 3*lam^3 - lam^2 + lam)*hk0 + (a*lam^9 - 4*a*lam^7 + 3*a*lam^5 + 2*a*lam^3 - b*lam^10 + 5*b*lam^8 - 6*b*lam^6 - b*lam^4 + 2*b*lam^2 - g*lam^5 + g*lam^3 + g*lam + lam^5 + lam^4 - lam^3 - 2*lam^2 - lam)*hk1 + (a*lam^8 - 3*a*lam^6 + a*lam^4 + a*lam^2 - b*lam^9 + 4*b*lam^7 - 3*b*lam^5 - b*lam^3 + b*lam - g*lam^4 + lam^4 + lam^3 - lam)*hk2 + (a*lam^7 - 2*a*lam^5 - a*lam^3 - b*lam^8 + 3*b*lam^6 - b*lam^2 - g*lam^3 - g*lam + lam^3 + lam^2 + lam)*hk3 + (a*lam^6 - 2*a*lam^4 - a*lam^2 - b*lam^7 + 3*b*lam^5 - b*lam - g*lam^2 + lam^2 + lam)*hk4 + (-a^2*lam^4 - a^2*lam^2 - 3*a^2 + 2*a*b*lam^5 + 2*a*b*lam - a - b^2*lam^6 + b^2*lam^4 - 4*b^2 + b*lam + b)*hps
    linarith [hr, he]
  have qq18 : (0:ℝ) ≤ a^2 + 2*a*b*lam - 2*a + b^2*lam^2 - 2*b*lam + 1 := by
    have hr : (0:ℝ) ≤ (a + b*lam - 1)*(a + b*lam - 1) := mul_nonneg reg0 reg0
    have he : (a + b*lam - 1)*(a + b*lam - 1) = a^2 + 2*a*b*lam - 2*a + b^2*lam^2 - 2*b*lam + 1 := by linear_combination 0
    linarith [hr, he]
  have qq19 : (0:ℝ) ≤ a^2*lam + 2*a*b*lam^2 - 2*a*lam + b^2*lam^3 - 2*b*lam^2 + lam := by
    have hr : (0:ℝ) ≤ lam*((a + b*lam - 1)*(a + b*lam - 1)) := mul_nonneg hpos.le (mul_nonneg reg0 reg0)
    have he : lam*((a + b*lam - 1)*(a + b*lam - 1)) = a^2*lam + 2*a*b*lam^2 - 2*a*lam + b^2*lam^3 - 2*b*lam^2 + lam := by linear_combination 0
    linarith [hr, he]
  have qq20 : (0:ℝ) ≤ -a^2*lam + a*b*lam^2 + 2*b^2*lam^3 - 3*b*lam^2 + lam := by
    have hr : (0:ℝ) ≤ lam*((a + b*lam - 1)*(b*lam + c - 1)) := mul_nonneg hpos.le (mul_nonneg reg0 gen1)
    have he : lam*((a + b*lam - 1)*(b*lam + c - 1)) = -a^2*lam + a*b*lam^2 + 2*b^2*lam^3 - 3*b*lam^2 + lam := by linear_combination (a*lam + b*lam^2 - lam)*hk0
    linarith [hr, he]
  have qq21 : (0:ℝ) ≤ -2*a^2*lam - a*b + 2*a*lam - a + 2*b^2*lam^3 - b^2*lam - 2*b*lam^2 - b*lam + b + 1 := by
    have hr : (0:ℝ) ≤ (a + b*lam - 1)*(c*lam + d - 1) := mul_nonneg reg0 gen2
    have he : (a + b*lam - 1)*(c*lam + d - 1) = -2*a^2*lam - a*b + 2*a*lam - a + 2*b^2*lam^3 - b^2*lam - 2*b*lam^2 - b*lam + b + 1 := by linear_combination (2*a*lam + 2*b*lam^2 - 2*lam)*hk0 + (a + b*lam - 1)*hk1
    linarith [hr, he]
  have qq22 : (0:ℝ) ≤ -2*a^2*lam^3 + a^2*lam - 2*a*b*lam^2 + 2*a*lam^3 - 2*a*lam + 2*b^2*lam^5 - 3*b^2*lam^3 - 2*b*lam^4 + 2*b*lam^2 + lam := by
    have hr : (0:ℝ) ≤ lam*((a + b*lam - 1)*(d*lam + e - 1)) := mul_nonneg hpos.le (mul_nonneg reg0 gen3)
    have he : lam*((a + b*lam - 1)*(d*lam + e - 1)) = -2*a^2*lam^3 + a^2*lam - 2*a*b*lam^2 + 2*a*lam^3 - 2*a*lam + 2*b^2*lam^5 - 3*b^2*lam^3 - 2*b*lam^4 + 2*b*lam^2 + lam := by linear_combination (2*a*lam^3 - a*lam + 2*b*lam^4 - b*lam^2 - 2*lam^3 + lam)*hk0 + (2*a*lam^2 + 2*b*lam^3 - 2*lam^2)*hk1 + (a*lam + b*lam^2 - lam)*hk2
    linarith [hr, he]
  have qq23 : (0:ℝ) ≤ -2*a^2*lam^4 + 5*a^2*lam^2 - a^2 - 2*a*b*lam^3 + 3*a*b*lam + 2*a*lam^4 - 5*a*lam^2 + 5*b^2*lam^4 - 14*b^2*lam^2 + 6*b^2 - 2*b*lam^5 + 7*b*lam^3 - 5*b*lam + 1 := by
    have hr : (0:ℝ) ≤ (a + b*lam - 1)*(f*lam + g - 1) := mul_nonneg reg0 gen5
    have he : (a + b*lam - 1)*(f*lam + g - 1) = -2*a^2*lam^4 + 5*a^2*lam^2 - a^2 - 2*a*b*lam^3 + 3*a*b*lam + 2*a*lam^4 - 5*a*lam^2 + 5*b^2*lam^4 - 14*b^2*lam^2 + 6*b^2 - 2*b*lam^5 + 7*b*lam^3 - 5*b*lam + 1 := by linear_combination (2*a*lam^4 - 5*a*lam^2 + a + 2*b*lam^5 - 5*b*lam^3 + b*lam - 2*lam^4 + 5*lam^2 - 1)*hk0 + (2*a*lam^3 - 3*a*lam + 2*b*lam^4 - 3*b*lam^2 - 2*lam^3 + 3*lam)*hk1 + (2*a*lam^2 - a + 2*b*lam^3 - b*lam - 2*lam^2 + 1)*hk2 + (2*a*lam + 2*b*lam^2 - 2*lam)*hk3 + (a + b*lam - 1)*hk4 + (2*b^2)*hps
    linarith [hr, he]
  have qq24 : (0:ℝ) ≤ a^2*lam^3 - 2*a*b*lam^4 - 2*a*b*lam^2 + 2*a*lam^2 + b^2*lam^5 + 2*b^2*lam^3 + b^2*lam - 2*b*lam^3 - 2*b*lam + lam := by
    have hr : (0:ℝ) ≤ lam*((b + c*lam - 1)*(b + c*lam - 1)) := mul_nonneg hpos.le (mul_nonneg reg1 reg1)
    have he : lam*((b + c*lam - 1)*(b + c*lam - 1)) = a^2*lam^3 - 2*a*b*lam^4 - 2*a*b*lam^2 + 2*a*lam^2 + b^2*lam^5 + 2*b^2*lam^3 + b^2*lam - 2*b*lam^3 - 2*b*lam + lam := by linear_combination (-a*lam^3 + b*lam^4 + 2*b*lam^2 + c*lam^3 - 2*lam^2)*hk0
    linarith [hr, he]
  have qq25 : (0:ℝ) ≤ 4*a^2*lam^4 - 10*a^2*lam^2 + 3*a^2 - 8*a*b*lam^5 + 21*a*b*lam^3 - 6*a*b*lam + a*lam^5 - 2*a*lam^3 + 12*b^2*lam^4 - 32*b^2*lam^2 + 13*b^2 - 3*b*lam^4 + 8*b*lam^2 - 5*b + 1 := by
    have hr : (0:ℝ) ≤ (b + c*lam - 1)*(f + g*lam - 1) := mul_nonneg reg1 reg5
    have he : (b + c*lam - 1)*(f + g*lam - 1) = 4*a^2*lam^4 - 10*a^2*lam^2 + 3*a^2 - 8*a*b*lam^5 + 21*a*b*lam^3 - 6*a*b*lam + a*lam^5 - 2*a*lam^3 + 12*b^2*lam^4 - 32*b^2*lam^2 + 13*b^2 - 3*b*lam^4 + 8*b*lam^2 - 5*b + 1 := by linear_combination (-a*lam^6 + 2*a*lam^4 + a*lam^2 + b*lam^7 - b*lam^5 - 3*b*lam^3 - b*lam + f*lam + g*lam^2 - lam^5 + 2*lam^3)*hk0 + (-a*lam^5 + a*lam^3 + a*lam + b*lam^6 - 2*b*lam^2 - b - lam^4 + lam^2 + 1)*hk1 + (-a*lam^4 + b*lam^5 + b*lam^3 - lam^3)*hk2 + (-a*lam^3 - a*lam + b*lam^4 + 2*b*lam^2 + b - lam^2 - 1)*hk3 + (-a*lam^2 + b*lam^3 + b*lam - lam)*hk4 + (a^2 - 2*a*b*lam + b^2*lam^2 + 4*b^2 - b)*hps
    linarith [hr, he]
  have qq26 : (0:ℝ) ≤ 2*a^2*lam^5 - 3*a^2*lam^3 - 18*a*b*lam^4 + 38*a*b*lam^2 - 12*a*b + 2*a*lam^4 - 2*a*lam^2 + 9*b^2*lam^5 - 22*b^2*lam^3 + 7*b^2*lam - 2*b*lam^5 + 4*b*lam^3 - 2*b*lam + lam := by
    have hr : (0:ℝ) ≤ lam*((b + c*lam - 1)*(e*lam + f - 1)) := mul_nonneg hpos.le (mul_nonneg reg1 gen4)
    have he : lam*((b + c*lam - 1)*(e*lam + f - 1)) = 2*a^2*lam^5 - 3*a^2*lam^3 - 18*a*b*lam^4 + 38*a*b*lam^2 - 12*a*b + 2*a*lam^4 - 2*a*lam^2 + 9*b^2*lam^5 - 22*b^2*lam^3 + 7*b^2*lam - 2*b*lam^5 + 4*b*lam^3 - 2*b*lam + lam := by linear_combination (-2*a*lam^5 + 3*a*lam^3 + 2*b*lam^6 - b*lam^4 - 3*b*lam^2 + e*lam^3 + f*lam^2 - 2*lam^4 + 2*lam^2)*hk0 + (-2*a*lam^4 + a*lam^2 + 2*b*lam^5 + b*lam^3 - b*lam - 2*lam^3 + lam)*hk1 + (-2*a*lam^3 + 2*b*lam^4 + 2*b*lam^2 - 2*lam^2)*hk2 + (-a*lam^2 + b*lam^3 + b*lam - lam)*hk3 + (-4*a*b + 2*b^2*lam)*hps
    linarith [hr, he]
  have qq27 : (0:ℝ) ≤ -a^2*b*lam^5 - a^2*b*lam^3 + 13*a*b^2*lam^4 - 18*a*b^2*lam^2 + 6*a*b^2 - a*b*lam^3 - a*lam^2 - a - 6*b^3*lam^5 + 9*b^3*lam^3 - 3*b^3*lam + b^2*lam^4 + b*lam^3 - 1 := by
    have hr : (0:ℝ) ≤ (c + d*lam - 1)*(-b*c*lam^3 + 1) := mul_nonneg reg2 slk1
    have he : (c + d*lam - 1)*(-b*c*lam^3 + 1) = -a^2*b*lam^5 - a^2*b*lam^3 + 13*a*b^2*lam^4 - 18*a*b^2*lam^2 + 6*a*b^2 - a*b*lam^3 - a*lam^2 - a - 6*b^3*lam^5 + 9*b^3*lam^3 - 3*b^3*lam + b^2*lam^4 + b*lam^3 - 1 := by linear_combination (a*b*lam^5 + a*b*lam^3 - b^2*lam^6 - b^2*lam^4 - b*c*lam^3 - b*d*lam^4 + b*lam^3 + lam^2 + 1)*hk0 + (a*b*lam^4 - b^2*lam^5 + lam)*hk1 + (2*a*b^2 - b^3*lam)*hps
    linarith [hr, he]
  have qq28 : (0:ℝ) ≤ 19*a^2*lam^5 - 38*a^2*lam^3 + 15*a^2*lam - 86*a*b*lam^4 + 170*a*b*lam^2 - 60*a*b + 8*a*lam^4 - 20*a*lam^2 + 6*a + 24*b^2*lam^5 - 45*b^2*lam^3 + 16*b^2*lam - 6*b*lam^5 + 18*b*lam^3 - 8*b*lam + lam := by
    have hr : (0:ℝ) ≤ lam*((f + g*lam - 1)*(f + g*lam - 1)) := mul_nonneg hpos.le (mul_nonneg reg5 reg5)
    have he : lam*((f + g*lam - 1)*(f + g*lam - 1)) = 19*a^2*lam^5 - 38*a^2*lam^3 + 15*a^2*lam - 86*a*b*lam^4 + 170*a*b*lam^2 - 60*a*b + 8*a*lam^4 - 20*a*lam^2 + 6*a + 24*b^2*lam^5 - 45*b^2*lam^3 + 16*b^2*lam - 6*b*lam^5 + 18*b*lam^3 - 8*b*lam + lam := by linear_combination (-a*lam^11 + 4*a*lam^9 - 2*a*lam^7 - 4*a*lam^5 - a*lam^3 + b*lam^12 - 5*b*lam^10 + 5*b*lam^8 + 4*b*lam^6 - 2*b*lam^4 + f*lam^4 - 2*f*lam^2 + g*lam^7 - g*lam^5 - 3*g*lam^3 - 2*lam^6 + 4*lam^4 + 2*lam^2)*hk0 + (-a*lam^10 + 3*a*lam^8 - 3*a*lam^4 - 2*a*lam^2 + b*lam^11 - 4*b*lam^9 + 2*b*lam^7 + 4*b*lam^5 - b*lam + f*lam^3 - f*lam + g*lam^6 - 2*g*lam^2 - 2*lam^5 + 2*lam^3 + 2*lam)*hk1 + (-a*lam^9 + 2*a*lam^7 + a*lam^5 - a*lam^3 + b*lam^10 - 3*b*lam^8 + 2*b*lam^4 - b*lam^2 + f*lam^2 + g*lam^5 + g*lam^3 - 2*lam^4)*hk2 + (-a*lam^8 + a*lam^6 + 2*a*lam^4 + 2*a*lam^2 + b*lam^9 - 2*b*lam^7 - 2*b*lam^5 - b*lam^3 + b*lam + f*lam + g*lam^4 + 2*g*lam^2 - 2*lam^3 - 2*lam)*hk3 + (-a*lam^7 + a*lam^5 + 3*a*lam^3 + b*lam^8 - 2*b*lam^6 - 3*b*lam^4 + 2*b*lam^2 + g*lam^3 - 2*lam^2)*hk4 + (a^2*lam^5 + 2*a^2*lam^3 + 5*a^2*lam - 2*a*b*lam^6 - 2*a*b*lam^4 - 4*a*b*lam^2 - 20*a*b + 2*a + b^2*lam^7 + 5*b^2*lam - 2*b*lam)*hps
    linarith [hr, he]
  have qq29 : (0:ℝ) ≤ -4*a^2*lam^4 + 10*a^2*lam^2 - 3*a^2 + 2*a*b*lam^5 - 7*a*b*lam^3 + 5*a*b*lam + a*lam^5 - 2*a*lam^3 - 2*a*lam + 3*b^2*lam^4 - 9*b^2*lam^2 + 4*b^2 - 3*b*lam^4 + 9*b*lam^2 - 5*b + 1 := by
    have hr : (0:ℝ) ≤ (f + g*lam - 1)*(a*lam + b - 1) := mul_nonneg reg5 gen0
    have he : (f + g*lam - 1)*(a*lam + b - 1) = -4*a^2*lam^4 + 10*a^2*lam^2 - 3*a^2 + 2*a*b*lam^5 - 7*a*b*lam^3 + 5*a*b*lam + a*lam^5 - 2*a*lam^3 - 2*a*lam + 3*b^2*lam^4 - 9*b^2*lam^2 + 4*b^2 - 3*b*lam^4 + 9*b*lam^2 - 5*b + 1 := by linear_combination (a*lam^6 - 2*a*lam^4 - a*lam^2 + b*lam^5 - 2*b*lam^3 - b*lam - lam^5 + 2*lam^3 + lam)*hk0 + (a*lam^5 - a*lam^3 - a*lam + b*lam^4 - b*lam^2 - b - lam^4 + lam^2 + 1)*hk1 + (a*lam^4 + b*lam^3 - lam^3)*hk2 + (a*lam^3 + a*lam + b*lam^2 + b - lam^2 - 1)*hk3 + (a*lam^2 + b*lam - lam)*hk4 + (-a^2 + a*b*lam + b^2 - b)*hps
    linarith [hr, he]
  have qq30 : (0:ℝ) ≤ -4*a^2*lam^5 + 10*a^2*lam^3 - 3*a^2*lam + 5*a*b*lam^4 - 13*a*b*lam^2 + 6*a*b + 4*a*lam^4 - 11*a*lam^2 + 3*a + 3*b^2*lam^5 - 9*b^2*lam^3 + 4*b^2*lam - 3*b*lam^5 + 9*b*lam^3 - 5*b*lam + lam := by
    have hr : (0:ℝ) ≤ lam*((f + g*lam - 1)*(a*lam + b - 1)) := mul_nonneg hpos.le (mul_nonneg reg5 gen0)
    have he : lam*((f + g*lam - 1)*(a*lam + b - 1)) = -4*a^2*lam^5 + 10*a^2*lam^3 - 3*a^2*lam + 5*a*b*lam^4 - 13*a*b*lam^2 + 6*a*b + 4*a*lam^4 - 11*a*lam^2 + 3*a + 3*b^2*lam^5 - 9*b^2*lam^3 + 4*b^2*lam - 3*b*lam^5 + 9*b*lam^3 - 5*b*lam + lam := by linear_combination (a*lam^7 - 2*a*lam^5 - a*lam^3 + b*lam^6 - 2*b*lam^4 - b*lam^2 - lam^6 + 2*lam^4 + lam^2)*hk0 + (a*lam^6 - a*lam^4 - a*lam^2 + b*lam^5 - b*lam^3 - b*lam - lam^5 + lam^3 + lam)*hk1 + (a*lam^5 + b*lam^4 - lam^4)*hk2 + (a*lam^4 + a*lam^2 + b*lam^3 + b*lam - lam^3 - lam)*hk3 + (a*lam^3 + b*lam^2 - lam^2)*hk4 + (-a^2*lam + a*b*lam^2 + 2*a*b + a + b^2*lam - b*lam)*hps
    linarith [hr, he]
  have qq31 : (0:ℝ) ≤ 14*a^2*b*lam^5 - 33*a^2*b*lam^3 + 12*a^2*b*lam - 31*a*b^2*lam^4 + 72*a*b^2*lam^2 - 27*a*b^2 + a*b*lam^4 - 4*a*lam^4 + 10*a*lam^2 - 3*a + 3*b*lam^5 - 9*b*lam^3 + 4*b*lam - lam := by
    have hr : (0:ℝ) ≤ lam*((f + g*lam - 1)*(-a*b*lam^3 + 1)) := mul_nonneg hpos.le (mul_nonneg reg5 slk0)
    have he : lam*((f + g*lam - 1)*(-a*b*lam^3 + 1)) = 14*a^2*b*lam^5 - 33*a^2*b*lam^3 + 12*a^2*b*lam - 31*a*b^2*lam^4 + 72*a*b^2*lam^2 - 27*a*b^2 + a*b*lam^4 - 4*a*lam^4 + 10*a*lam^2 - 3*a + 3*b*lam^5 - 9*b*lam^3 + 4*b*lam - lam := by linear_combination (-a*b*lam^9 + 2*a*b*lam^7 + a*b*lam^5 + lam^6 - 2*lam^4 - lam^2)*hk0 + (-a*b*lam^8 + a*b*lam^6 + a*b*lam^4 + lam^5 - lam^3 - lam)*hk1 + (-a*b*lam^7 + lam^4)*hk2 + (-a*b*lam^6 - a*b*lam^4 + lam^3 + lam)*hk3 + (-a*b*lam^5 + lam^2)*hk4 + (a^2*b*lam^3 + 4*a^2*b*lam - a*b^2*lam^4 - 3*a*b^2*lam^2 - 9*a*b^2 - a + b*lam)*hps
    linarith [hr, he]
  have qq32 : (0:ℝ) ≤ 402*a^3*lam^4 - 855*a^3*lam^2 + 312*a^3 - 711*a^2*b*lam^5 + 1518*a^2*b*lam^3 - 555*a^2*b*lam + 16*a^2*lam^5 - 33*a^2*lam^3 + 12*a^2*lam + 1618*a*b^2*lam^4 - 3450*a*b^2*lam^2 + 1260*a*b^2 - 73*a*b*lam^4 + 150*a*b*lam^2 - 54*a*b - 4*a*lam^4 + 10*a*lam^2 - 3*a - 318*b^3*lam^5 + 681*b^3*lam^3 - 249*b^3*lam + 21*b^2*lam^5 - 42*b^2*lam^3 + 15*b^2*lam + 3*b*lam^5 - 9*b*lam^3 + 4*b*lam - lam := by
    have hr : (0:ℝ) ≤ lam*((f + g*lam - 1)*(-f*g*lam^3 + 1)) := mul_nonneg hpos.le (mul_nonneg reg5 slk5)
    have he : lam*((f + g*lam - 1)*(-f*g*lam^3 + 1)) = 402*a^3*lam^4 - 855*a^3*lam^2 + 312*a^3 - 711*a^2*b*lam^5 + 1518*a^2*b*lam^3 - 555*a^2*b*lam + 16*a^2*lam^5 - 33*a^2*lam^3 + 12*a^2*lam + 1618*a*b^2*lam^4 - 3450*a*b^2*lam^2 + 1260*a*b^2 - 73*a*b*lam^4 + 150*a*b*lam^2 - 54*a*b - 4*a*lam^4 + 10*a*lam^2 - 3*a - 318*b^3*lam^5 + 681*b^3*lam^3 - 249*b^3*lam + 21*b^2*lam^5 - 42*b^2*lam^3 + 15*b^2*lam + 3*b*lam^5 - 9*b*lam^3 + 4*b*lam - lam := by linear_combination (-a^2*lam^16 + 7*a^2*lam^14 - 16*a^2*lam^12 + 11*a^2*lam^10 + 3*a^2*lam^8 - 2*a^2*lam^6 + 2*a*b*lam^17 - 16*a*b*lam^15 + 44*a*b*lam^13 - 44*a*b*lam^11 + 3*a*b*lam^9 + 11*a*b*lam^7 - 3*a*b*lam^5 + a*g*lam^12 - 4*a*g*lam^10 + 3*a*g*lam^8 + 2*a*g*lam^6 - a*lam^11 + 5*a*lam^9 - 7*a*lam^7 + 2*a*lam^5 - b^2*lam^18 + 9*b^2*lam^16 - 29*b^2*lam^14 + 38*b^2*lam^12 - 13*b^2*lam^10 - 8*b^2*lam^8 + 6*b^2*lam^6 - b^2*lam^4 - b*g*lam^13 + 5*b*g*lam^11 - 6*b*g*lam^9 - b*g*lam^7 + b*g*lam^5 + b*lam^12 - 6*b*lam^10 + 11*b*lam^8 - 6*b*lam^6 + b*lam^4 - f*g*lam^7 + 2*f*g*lam^5 - g^2*lam^8 + 2*g^2*lam^6 + g*lam^7 - 2*g*lam^5 + lam^6 - 2*lam^4 - lam^2)*hk0 + (-a^2*lam^15 + 6*a^2*lam^13 - 11*a^2*lam^11 + 4*a^2*lam^9 + 4*a^2*lam^7 + 2*a*b*lam^16 - 14*a*b*lam^14 + 32*a*b*lam^12 - 22*a*b*lam^10 - 7*a*b*lam^8 + 6*a*b*lam^6 + a*g*lam^11 - 3*a*g*lam^9 + a*g*lam^7 + 2*a*g*lam^5 - a*lam^10 + 4*a*lam^8 - 4*a*lam^6 - b^2*lam^17 + 8*b^2*lam^15 - 22*b^2*lam^13 + 22*b^2*lam^11 - b^2*lam^9 - 7*b^2*lam^7 + 2*b^2*lam^5 - b*g*lam^12 + 4*b*g*lam^10 - 3*b*g*lam^8 - 2*b*g*lam^6 + b*g*lam^4 + b*lam^11 - 5*b*lam^9 + 7*b*lam^7 - 2*b*lam^5 - f*g*lam^6 + f*g*lam^4 - g^2*lam^7 + g^2*lam^5 + g*lam^6 - g*lam^4 + lam^5 - lam^3 - lam)*hk1 + (-a^2*lam^14 + 5*a^2*lam^12 - 7*a^2*lam^10 + a^2*lam^8 + 2*a^2*lam^6 + 2*a*b*lam^15 - 12*a*b*lam^13 + 22*a*b*lam^11 - 10*a*b*lam^9 - 5*a*b*lam^7 + 3*a*b*lam^5 + a*g*lam^10 - 2*a*g*lam^8 - a*lam^9 + 3*a*lam^7 - 2*a*lam^5 - b^2*lam^16 + 7*b^2*lam^14 - 16*b^2*lam^12 + 12*b^2*lam^10 + b^2*lam^8 - 4*b^2*lam^6 + b^2*lam^4 - b*g*lam^11 + 3*b*g*lam^9 - b*g*lam^7 + b*lam^10 - 4*b*lam^8 + 4*b*lam^6 - b*lam^4 - f*g*lam^5 - g^2*lam^6 + g*lam^5 + lam^4)*hk2 + (-a^2*lam^13 + 4*a^2*lam^11 - 3*a^2*lam^9 - 2*a^2*lam^7 + 2*a*b*lam^14 - 10*a*b*lam^12 + 12*a*b*lam^10 + 2*a*b*lam^8 - 3*a*b*lam^6 + a*g*lam^9 - a*g*lam^7 - 2*a*g*lam^5 - a*lam^8 + 2*a*lam^6 - b^2*lam^15 + 6*b^2*lam^13 - 10*b^2*lam^11 + 2*b^2*lam^9 + 3*b^2*lam^7 - b^2*lam^5 - b*g*lam^10 + 2*b*g*lam^8 + 2*b*g*lam^6 - b*g*lam^4 + b*lam^9 - 3*b*lam^7 + b*lam^5 - f*g*lam^4 - g^2*lam^5 + g*lam^4 + lam^3 + lam)*hk3 + (-a^2*lam^12 + 4*a^2*lam^10 - 3*a^2*lam^8 - 2*a^2*lam^6 + 2*a*b*lam^13 - 10*a*b*lam^11 + 12*a*b*lam^9 + 2*a*b*lam^7 - 3*a*b*lam^5 + a*g*lam^8 - 2*a*g*lam^6 - a*lam^7 + 2*a*lam^5 - b^2*lam^14 + 6*b^2*lam^12 - 10*b^2*lam^10 + 2*b^2*lam^8 + 3*b^2*lam^6 - b^2*lam^4 - b*g*lam^9 + 3*b*g*lam^7 - b*g*lam^5 + b*lam^8 - 3*b*lam^6 + b*lam^4 + lam^2)*hk4 + (a^3*lam^10 - a^3*lam^8 + a^3*lam^6 + 7*a^3*lam^4 + 27*a^3*lam^2 + 104*a^3 - 3*a^2*b*lam^11 + 6*a^2*b*lam^9 - 3*a^2*b*lam^7 - 15*a^2*b*lam^5 - 49*a^2*b*lam^3 - 185*a^2*b*lam + a^2*lam^5 + a^2*lam^3 + 4*a^2*lam + 3*a*b^2*lam^12 - 9*a*b^2*lam^10 + 6*a*b^2*lam^8 + 12*a*b^2*lam^6 + 29*a*b^2*lam^4 + 110*a*b^2*lam^2 + 420*a*b^2 - 2*a*b*lam^6 - 4*a*b*lam^2 - 18*a*b - a - b^3*lam^13 + 4*b^3*lam^11 - 4*b^3*lam^9 - 3*b^3*lam^7 - 5*b^3*lam^5 - 22*b^3*lam^3 - 83*b^3*lam + b^2*lam^7 - b^2*lam^5 + b^2*lam^3 + 5*b^2*lam + b*lam)*hps
    linarith [hr, he]
  have qq33 : (0:ℝ) ≤ a^2*lam^3 + 2*a*b*lam^2 - 2*a*lam^2 + b^2*lam - 2*b*lam + lam := by
    have hr : (0:ℝ) ≤ lam*((a*lam + b - 1)*(a*lam + b - 1)) := mul_nonneg hpos.le (mul_nonneg gen0 gen0)
    have he : lam*((a*lam + b - 1)*(a*lam + b - 1)) = a^2*lam^3 + 2*a*b*lam^2 - 2*a*lam^2 + b^2*lam - 2*b*lam + lam := by linear_combination 0
    linarith [hr, he]
  have qq34 : (0:ℝ) ≤ -2*a^2*lam^4 + 3*a^2*lam^2 + 2*a*b*lam^5 - 7*a*b*lam^3 + 4*a*b*lam + 2*a*lam^3 - 4*a*lam + 2*b^2*lam^4 - 5*b^2*lam^2 + b^2 - 2*b*lam^4 + 5*b*lam^2 - 2*b + 1 := by
    have hr : (0:ℝ) ≤ (a*lam + b - 1)*(e*lam + f - 1) := mul_nonneg gen0 gen4
    have he : (a*lam + b - 1)*(e*lam + f - 1) = -2*a^2*lam^4 + 3*a^2*lam^2 + 2*a*b*lam^5 - 7*a*b*lam^3 + 4*a*b*lam + 2*a*lam^3 - 4*a*lam + 2*b^2*lam^4 - 5*b^2*lam^2 + b^2 - 2*b*lam^4 + 5*b*lam^2 - 2*b + 1 := by linear_combination (2*a*lam^4 - 3*a*lam^2 + 2*b*lam^3 - 3*b*lam - 2*lam^3 + 3*lam)*hk0 + (2*a*lam^3 - a*lam + 2*b*lam^2 - b - 2*lam^2 + 1)*hk1 + (2*a*lam^2 + 2*b*lam - 2*lam)*hk2 + (a*lam + b - 1)*hk3
    linarith [hr, he]
  have qq35 : (0:ℝ) ≤ -6*a^3*lam^4 + 9*a^3*lam^2 - 3*a^3 + 10*a^2*b*lam^5 - 18*a^2*b*lam^3 + 6*a^2*b*lam + a^2*lam^5 - 10*a*b^2*lam^4 + 24*a*b^2*lam^2 - 9*a*b^2 - 11*a*b*lam^4 + 18*a*b*lam^2 - 6*a*b + a*lam^2 - 5*b^3*lam^5 + 9*b^3*lam^3 - 3*b^3*lam + 5*b^2*lam^5 - 9*b^2*lam^3 + 3*b^2*lam + b*lam - lam := by
    have hr : (0:ℝ) ≤ lam*((a*lam + b - 1)*(-c*d*lam^3 + 1)) := mul_nonneg hpos.le (mul_nonneg gen0 slk2)
    have he : lam*((a*lam + b - 1)*(-c*d*lam^3 + 1)) = -6*a^3*lam^4 + 9*a^3*lam^2 - 3*a^3 + 10*a^2*b*lam^5 - 18*a^2*b*lam^3 + 6*a^2*b*lam + a^2*lam^5 - 10*a*b^2*lam^4 + 24*a*b^2*lam^2 - 9*a*b^2 - 11*a*b*lam^4 + 18*a*b*lam^2 - 6*a*b + a*lam^2 - 5*b^3*lam^5 + 9*b^3*lam^3 - 3*b^3*lam + 5*b^2*lam^5 - 9*b^2*lam^3 + 3*b^2*lam + b*lam - lam := by linear_combination (a^2*lam^6 - a*b*lam^7 + a*b*lam^5 - a*d*lam^5 - a*lam^5 - b^2*lam^6 - b*d*lam^4 + b*lam^6 + d*lam^4)*hk0 + (a^2*lam^5 - a*b*lam^6 + a*b*lam^4 - a*lam^4 - b^2*lam^5 + b*lam^5)*hk1 + (-a^3 + 2*a^2*b*lam - a*b^2*lam^2 - 3*a*b^2 - 2*a*b - b^3*lam + b^2*lam)*hps
    linarith [hr, he]
  have qq36 : (0:ℝ) ≤ -63*a^3*lam^4 + 132*a^3*lam^2 - 48*a^3 + 57*a^2*b*lam^5 - 117*a^2*b*lam^3 + 42*a^2*b*lam + 16*a^2*lam^5 - 33*a^2*lam^3 + 12*a^2*lam - 11*a*b^2*lam^4 + 24*a*b^2*lam^2 - 9*a*b^2 - 73*a*b*lam^4 + 150*a*b*lam^2 - 54*a*b + a*lam^2 - 21*b^3*lam^5 + 42*b^3*lam^3 - 15*b^3*lam + 21*b^2*lam^5 - 42*b^2*lam^3 + 15*b^2*lam + b*lam - lam := by
    have hr : (0:ℝ) ≤ lam*((a*lam + b - 1)*(-f*g*lam^3 + 1)) := mul_nonneg hpos.le (mul_nonneg gen0 slk5)
    have he : lam*((a*lam + b - 1)*(-f*g*lam^3 + 1)) = -63*a^3*lam^4 + 132*a^3*lam^2 - 48*a^3 + 57*a^2*b*lam^5 - 117*a^2*b*lam^3 + 42*a^2*b*lam + 16*a^2*lam^5 - 33*a^2*lam^3 + 12*a^2*lam - 11*a*b^2*lam^4 + 24*a*b^2*lam^2 - 9*a*b^2 - 73*a*b*lam^4 + 150*a*b*lam^2 - 54*a*b + a*lam^2 - 21*b^3*lam^5 + 42*b^3*lam^3 - 15*b^3*lam + 21*b^2*lam^5 - 42*b^2*lam^3 + 15*b^2*lam + b*lam - lam := by linear_combination (a^2*lam^12 - 5*a^2*lam^10 + 7*a^2*lam^8 - 2*a^2*lam^6 - a*b*lam^13 + 7*a*b*lam^11 - 16*a*b*lam^9 + 13*a*b*lam^7 - 3*a*b*lam^5 - a*g*lam^8 + 2*a*g*lam^6 - a*lam^11 + 5*a*lam^9 - 7*a*lam^7 + 2*a*lam^5 - b^2*lam^12 + 6*b^2*lam^10 - 11*b^2*lam^8 + 6*b^2*lam^6 - b^2*lam^4 - b*g*lam^7 + 2*b*g*lam^5 + b*lam^12 - 6*b*lam^10 + 11*b*lam^8 - 6*b*lam^6 + b*lam^4 + g*lam^7 - 2*g*lam^5)*hk0 + (a^2*lam^11 - 4*a^2*lam^9 + 4*a^2*lam^7 - a*b*lam^12 + 6*a*b*lam^10 - 11*a*b*lam^8 + 6*a*b*lam^6 - a*g*lam^7 + a*g*lam^5 - a*lam^10 + 4*a*lam^8 - 4*a*lam^6 - b^2*lam^11 + 5*b^2*lam^9 - 7*b^2*lam^7 + 2*b^2*lam^5 - b*g*lam^6 + b*g*lam^4 + b*lam^11 - 5*b*lam^9 + 7*b*lam^7 - 2*b*lam^5 + g*lam^6 - g*lam^4)*hk1 + (a^2*lam^10 - 3*a^2*lam^8 + 2*a^2*lam^6 - a*b*lam^11 + 5*a*b*lam^9 - 7*a*b*lam^7 + 3*a*b*lam^5 - a*g*lam^6 - a*lam^9 + 3*a*lam^7 - 2*a*lam^5 - b^2*lam^10 + 4*b^2*lam^8 - 4*b^2*lam^6 + b^2*lam^4 - b*g*lam^5 + b*lam^10 - 4*b*lam^8 + 4*b*lam^6 - b*lam^4 + g*lam^5)*hk2 + (a^2*lam^9 - 2*a^2*lam^7 - a*b*lam^10 + 4*a*b*lam^8 - 3*a*b*lam^6 - a*g*lam^5 - a*lam^8 + 2*a*lam^6 - b^2*lam^9 + 3*b^2*lam^7 - b^2*lam^5 - b*g*lam^4 + b*lam^9 - 3*b*lam^7 + b*lam^5 + g*lam^4)*hk3 + (a^2*lam^8 - 2*a^2*lam^6 - a*b*lam^9 + 4*a*b*lam^7 - 3*a*b*lam^5 - a*lam^7 + 2*a*lam^5 - b^2*lam^8 + 3*b^2*lam^6 - b^2*lam^4 + b*lam^8 - 3*b*lam^6 + b*lam^4)*hk4 + (-a^3*lam^6 - a^3*lam^4 - 4*a^3*lam^2 - 16*a^3 + 2*a^2*b*lam^7 - a^2*b*lam^5 + 3*a^2*b*lam^3 + 14*a^2*b*lam + a^2*lam^5 + a^2*lam^3 + 4*a^2*lam - a*b^2*lam^8 + 3*a*b^2*lam^6 - a*b^2*lam^4 - a*b^2*lam^2 - 3*a*b^2 - 2*a*b*lam^6 - 4*a*b*lam^2 - 18*a*b - b^3*lam^7 + b^3*lam^5 - b^3*lam^3 - 5*b^3*lam + b^2*lam^7 - b^2*lam^5 + b^2*lam^3 + 5*b^2*lam)*hps
    linarith [hr, he]
  have qq37 : (0:ℝ) ≤ 4*a^2*lam^5 - 10*a^2*lam^3 + 2*a^2*lam - 22*a*b*lam^4 + 57*a*b*lam^2 - 23*a*b + 2*a*lam^4 - 5*a*lam^2 + 2*a*lam + a + 8*b^2*lam^5 - 21*b^2*lam^3 + 8*b^2*lam - 2*b*lam^5 + 7*b*lam^3 - 2*b*lam^2 - 4*b*lam + b + 1 := by
    have hr : (0:ℝ) ≤ (c*lam + d - 1)*(f*lam + g - 1) := mul_nonneg gen2 gen5
    have he : (c*lam + d - 1)*(f*lam + g - 1) = 4*a^2*lam^5 - 10*a^2*lam^3 + 2*a^2*lam - 22*a*b*lam^4 + 57*a*b*lam^2 - 23*a*b + 2*a*lam^4 - 5*a*lam^2 + 2*a*lam + a + 8*b^2*lam^5 - 21*b^2*lam^3 + 8*b^2*lam - 2*b*lam^5 + 7*b*lam^3 - 2*b*lam^2 - 4*b*lam + b + 1 := by linear_combination (-4*a*lam^5 + 10*a*lam^3 - 2*a*lam + 4*b*lam^6 - 12*b*lam^4 + 7*b*lam^2 - b + 2*f*lam^2 + 2*g*lam - 2*lam^4 + 5*lam^2 - 2*lam - 1)*hk0 + (-4*a*lam^4 + 6*a*lam^2 + 4*b*lam^5 - 8*b*lam^3 + 3*b*lam + f*lam + g - 2*lam^3 + 3*lam - 1)*hk1 + (-4*a*lam^3 + 2*a*lam + 4*b*lam^4 - 4*b*lam^2 + b - 2*lam^2 + 1)*hk2 + (-4*a*lam^2 + 4*b*lam^3 - 2*b*lam - 2*lam)*hk3 + (-2*a*lam + 2*b*lam^2 - b - 1)*hk4 + (-8*a*b + 4*b^2*lam)*hps
    linarith [hr, he]
  have qq38 : (0:ℝ) ≤ -2*a^2*b*lam^5 + a^2*b*lam^3 + 20*a*b^2*lam^4 - 36*a*b^2*lam^2 + 12*a*b^2 - a*b*lam^3 - 2*a*lam^2 + a - 9*b^3*lam^5 + 18*b^3*lam^3 - 6*b^3*lam + b^2*lam^4 + 2*b*lam^3 - 3*b*lam - 1 := by
    have hr : (0:ℝ) ≤ (d*lam + e - 1)*(-b*c*lam^3 + 1) := mul_nonneg gen3 slk1
    have he : (d*lam + e - 1)*(-b*c*lam^3 + 1) = -2*a^2*b*lam^5 + a^2*b*lam^3 + 20*a*b^2*lam^4 - 36*a*b^2*lam^2 + 12*a*b^2 - a*b*lam^3 - 2*a*lam^2 + a - 9*b^3*lam^5 + 18*b^3*lam^3 - 6*b^3*lam + b^2*lam^4 + 2*b*lam^3 - 3*b*lam - 1 := by linear_combination (2*a*b*lam^5 - a*b*lam^3 - 2*b^2*lam^6 + b^2*lam^4 - b*d*lam^4 - b*e*lam^3 + b*lam^3 + 2*lam^2 - 1)*hk0 + (2*a*b*lam^4 - 2*b^2*lam^5 + 2*lam)*hk1 + (a*b*lam^3 - b^2*lam^4 + 1)*hk2 + (4*a*b^2 - 2*b^3*lam)*hps
    linarith [hr, he]
  have qq39 : (0:ℝ) ≤ 17*a^2*lam^4 - 34*a^2*lam^2 + 13*a^2 - 18*a*b*lam^5 + 30*a*b*lam^3 - 8*a*b*lam + 4*a*lam^4 - 10*a*lam^2 + 2*a + 22*b^2*lam^4 - 41*b^2*lam^2 + 15*b^2 - 4*b*lam^5 + 14*b*lam^3 - 8*b*lam + 1 := by
    have hr : (0:ℝ) ≤ (f*lam + g - 1)*(f*lam + g - 1) := mul_nonneg gen5 gen5
    have he : (f*lam + g - 1)*(f*lam + g - 1) = 17*a^2*lam^4 - 34*a^2*lam^2 + 13*a^2 - 18*a*b*lam^5 + 30*a*b*lam^3 - 8*a*b*lam + 4*a*lam^4 - 10*a*lam^2 + 2*a + 22*b^2*lam^4 - 41*b^2*lam^2 + 15*b^2 - 4*b*lam^5 + 14*b*lam^3 - 8*b*lam + 1 := by linear_combination (-4*a*lam^8 + 20*a*lam^6 - 29*a*lam^4 + 10*a*lam^2 - a + 4*b*lam^9 - 24*b*lam^7 + 45*b*lam^5 - 27*b*lam^3 + 5*b*lam + f*lam^5 - 2*f*lam^3 + 3*g*lam^4 - 7*g*lam^2 + g - 4*lam^4 + 10*lam^2 - 2)*hk0 + (-4*a*lam^7 + 16*a*lam^5 - 17*a*lam^3 + 2*a*lam + 4*b*lam^8 - 20*b*lam^6 + 29*b*lam^4 - 11*b*lam^2 + f*lam^4 - f*lam^2 + 3*g*lam^3 - 4*g*lam - 4*lam^3 + 6*lam)*hk1 + (-4*a*lam^6 + 12*a*lam^4 - 8*a*lam^2 + a + 4*b*lam^7 - 16*b*lam^5 + 16*b*lam^3 - 5*b*lam + f*lam^3 + 3*g*lam^2 - g - 4*lam^2 + 2)*hk2 + (-4*a*lam^5 + 9*a*lam^3 - a*lam + 4*b*lam^6 - 13*b*lam^4 + 6*b*lam^2 + f*lam^2 + 3*g*lam - 4*lam)*hk3 + (-3*a*lam^4 + 7*a*lam^2 - a + 3*b*lam^5 - 10*b*lam^3 + 5*b*lam + g - 2)*hk4 + (4*a^2*lam^2 + 4*a^2 - 8*a*b*lam^3 + 4*b^2*lam^4 - 4*b^2*lam^2 + 5*b^2)*hps
    linarith [hr, he]
  linarith [qq0, qq1, qq2, qq3, qq4, qq5, qq6, qq7, qq8, qq9, qq10, qq11, qq12, qq13, qq14, qq15, qq16, qq17, qq18, qq19, qq20, qq21, qq22, qq23, qq24, qq25, qq26, qq27, qq28, qq29, qq30, qq31, qq32, qq33, qq34, qq35, qq36, qq37, qq38, qq39, h2, h3]

/-- **q=18 window-6 core.** 7 coords of a genuine scalar orbit (both Taha edges + cap
+ 5 integer floors K_i>=1 with recurrence and floor-upper) cannot have all 6 products
`< 1/lam^3`.  Each interior floor is forced to 1 (floor-helper), reducing to the single
Chebyshev case `case_q18`. -/
theorem g18_core (a b c d e f g lam : ℝ) (hps : lam^6 = 6*lam^4 - 9*lam^2 + 3) (h2 : (1:ℝ) < lam) (h3 : lam < 2)
    (hlo : (9:ℝ)/5 < lam)
    (hpa : 0 < a) (hpb : 0 < b) (hpc : 0 < c) (hpd : 0 < d) (hpe : 0 < e) (hpf : 0 < f) (hpg : 0 < g)
    (hca : a ≤ 1) (hcb : b ≤ 1) (hcc : c ≤ 1) (hcd : d ≤ 1) (hce : e ≤ 1) (hcf : f ≤ 1) (hcg : g ≤ 1)
    (hr0 : a+lam*b > 1) (hr1 : b+lam*c > 1) (hr2 : c+lam*d > 1) (hr3 : d+lam*e > 1) (hr4 : e+lam*f > 1) (hr5 : f+lam*g > 1)
    (hg0 : lam*a+b > 1) (hg1 : lam*b+c > 1) (hg2 : lam*c+d > 1) (hg3 : lam*d+e > 1) (hg4 : lam*e+f > 1) (hg5 : lam*f+g > 1)
    (K0 K1 K2 K3 K4 : ℤ)
    (hk0 : a+c = (K0:ℝ)*lam*b) (hk1 : b+d = (K1:ℝ)*lam*c) (hk2 : c+e = (K2:ℝ)*lam*d) (hk3 : d+f = (K3:ℝ)*lam*e) (hk4 : e+g = (K4:ℝ)*lam*f)
    (hKge0 : 1 ≤ K0) (hKge1 : 1 ≤ K1) (hKge2 : 1 ≤ K2) (hKge3 : 1 ≤ K3) (hKge4 : 1 ≤ K4)
    (hf0 : 1+a < ((K0:ℝ)+1)*(lam*b)) (hf1 : 1+b < ((K1:ℝ)+1)*(lam*c)) (hf2 : 1+c < ((K2:ℝ)+1)*(lam*d)) (hf3 : 1+d < ((K3:ℝ)+1)*(lam*e)) (hf4 : 1+e < ((K4:ℝ)+1)*(lam*f))
    (hP0 : a*b < 1/lam^3) (hP1 : b*c < 1/lam^3) (hP2 : c*d < 1/lam^3) (hP3 : d*e < 1/lam^3) (hP4 : e*f < 1/lam^3) (hP5 : f*g < 1/lam^3) :
    False := by
  have hpos : (0:ℝ) < lam := by linarith
  have hp3 : (0:ℝ) < lam^3 := by positivity
  have hp4nn : (0:ℝ) ≤ lam^4 := by positivity
  have hP0c : a*b*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP0
  have hP1c : b*c*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP1
  have hP2c : c*d*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP2
  have hP3c : d*e*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP3
  have hP4c : e*f*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP4
  have hP5c : f*g*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP5
  have hKr0 : (1:ℝ) ≤ (K0:ℝ) := by exact_mod_cast hKge0
  have heng0 : a*b + b*c = (K0:ℝ)*lam*b^2 := by linear_combination b*hk0
  have hK0b : (K0:ℝ)*lam^4*b^2 < 2 := by
    have h : (a*b+b*c)*lam^3 = (K0:ℝ)*lam^4*b^2 := by linear_combination lam^3*heng0
    nlinarith [hP0c, hP1c, h]
  have hbU0 : lam^4*b^2 < 2 := by
    have hn : (0:ℝ) ≤ lam^4*b^2 := mul_nonneg hp4nn (sq_nonneg _)
    nlinarith [hK0b, hKr0, mul_nonneg (by linarith : (0:ℝ) ≤ (K0:ℝ)-1) hn]
  have hKr1 : (1:ℝ) ≤ (K1:ℝ) := by exact_mod_cast hKge1
  have heng1 : b*c + c*d = (K1:ℝ)*lam*c^2 := by linear_combination c*hk1
  have hK1b : (K1:ℝ)*lam^4*c^2 < 2 := by
    have h : (b*c+c*d)*lam^3 = (K1:ℝ)*lam^4*c^2 := by linear_combination lam^3*heng1
    nlinarith [hP1c, hP2c, h]
  have hbU1 : lam^4*c^2 < 2 := by
    have hn : (0:ℝ) ≤ lam^4*c^2 := mul_nonneg hp4nn (sq_nonneg _)
    nlinarith [hK1b, hKr1, mul_nonneg (by linarith : (0:ℝ) ≤ (K1:ℝ)-1) hn]
  have hKr2 : (1:ℝ) ≤ (K2:ℝ) := by exact_mod_cast hKge2
  have heng2 : c*d + d*e = (K2:ℝ)*lam*d^2 := by linear_combination d*hk2
  have hK2b : (K2:ℝ)*lam^4*d^2 < 2 := by
    have h : (c*d+d*e)*lam^3 = (K2:ℝ)*lam^4*d^2 := by linear_combination lam^3*heng2
    nlinarith [hP2c, hP3c, h]
  have hbU2 : lam^4*d^2 < 2 := by
    have hn : (0:ℝ) ≤ lam^4*d^2 := mul_nonneg hp4nn (sq_nonneg _)
    nlinarith [hK2b, hKr2, mul_nonneg (by linarith : (0:ℝ) ≤ (K2:ℝ)-1) hn]
  have hKr3 : (1:ℝ) ≤ (K3:ℝ) := by exact_mod_cast hKge3
  have heng3 : d*e + e*f = (K3:ℝ)*lam*e^2 := by linear_combination e*hk3
  have hK3b : (K3:ℝ)*lam^4*e^2 < 2 := by
    have h : (d*e+e*f)*lam^3 = (K3:ℝ)*lam^4*e^2 := by linear_combination lam^3*heng3
    nlinarith [hP3c, hP4c, h]
  have hbU3 : lam^4*e^2 < 2 := by
    have hn : (0:ℝ) ≤ lam^4*e^2 := mul_nonneg hp4nn (sq_nonneg _)
    nlinarith [hK3b, hKr3, mul_nonneg (by linarith : (0:ℝ) ≤ (K3:ℝ)-1) hn]
  have hKr4 : (1:ℝ) ≤ (K4:ℝ) := by exact_mod_cast hKge4
  have heng4 : e*f + f*g = (K4:ℝ)*lam*f^2 := by linear_combination f*hk4
  have hK4b : (K4:ℝ)*lam^4*f^2 < 2 := by
    have h : (e*f+f*g)*lam^3 = (K4:ℝ)*lam^4*f^2 := by linear_combination lam^3*heng4
    nlinarith [hP4c, hP5c, h]
  have hbU4 : lam^4*f^2 < 2 := by
    have hn : (0:ℝ) ≤ lam^4*f^2 := mul_nonneg hp4nn (sq_nonneg _)
    nlinarith [hK4b, hKr4, mul_nonneg (by linarith : (0:ℝ) ≤ (K4:ℝ)-1) hn]
  have hKle0 : K0 ≤ 1 := by
    by_contra hcon; push_neg at hcon
    have h2K : (2:ℝ) ≤ (K0:ℝ) := by exact_mod_cast (by omega : (2:ℤ) ≤ K0)
    have hn : (0:ℝ) ≤ lam^4*b^2 := mul_nonneg hp4nn (sq_nonneg _)
    have hms : lam^4*b^2 < 1 := by nlinarith [hK0b, h2K, mul_nonneg (by linarith : (0:ℝ) ≤ (K0:ℝ)-2) hn]
    exact g18_floor_helper lam b c h2 h3 hlo hpb hpc hms hbU1 (by linarith [hg1])
  have hKle1 : K1 ≤ 1 := by
    by_contra hcon; push_neg at hcon
    have h2K : (2:ℝ) ≤ (K1:ℝ) := by exact_mod_cast (by omega : (2:ℤ) ≤ K1)
    have hn : (0:ℝ) ≤ lam^4*c^2 := mul_nonneg hp4nn (sq_nonneg _)
    have hms : lam^4*c^2 < 1 := by nlinarith [hK1b, h2K, mul_nonneg (by linarith : (0:ℝ) ≤ (K1:ℝ)-2) hn]
    exact g18_floor_helper lam c d h2 h3 hlo hpc hpd hms hbU2 (by linarith [hg2])
  have hKle2 : K2 ≤ 1 := by
    by_contra hcon; push_neg at hcon
    have h2K : (2:ℝ) ≤ (K2:ℝ) := by exact_mod_cast (by omega : (2:ℤ) ≤ K2)
    have hn : (0:ℝ) ≤ lam^4*d^2 := mul_nonneg hp4nn (sq_nonneg _)
    have hms : lam^4*d^2 < 1 := by nlinarith [hK2b, h2K, mul_nonneg (by linarith : (0:ℝ) ≤ (K2:ℝ)-2) hn]
    exact g18_floor_helper lam d e h2 h3 hlo hpd hpe hms hbU3 (by linarith [hg3])
  have hKle3 : K3 ≤ 1 := by
    by_contra hcon; push_neg at hcon
    have h2K : (2:ℝ) ≤ (K3:ℝ) := by exact_mod_cast (by omega : (2:ℤ) ≤ K3)
    have hn : (0:ℝ) ≤ lam^4*e^2 := mul_nonneg hp4nn (sq_nonneg _)
    have hms : lam^4*e^2 < 1 := by nlinarith [hK3b, h2K, mul_nonneg (by linarith : (0:ℝ) ≤ (K3:ℝ)-2) hn]
    exact g18_floor_helper lam e f h2 h3 hlo hpe hpf hms hbU4 (by linarith [hg4])
  have hKle4 : K4 ≤ 1 := by
    by_contra hcon; push_neg at hcon
    have h2K : (2:ℝ) ≤ (K4:ℝ) := by exact_mod_cast (by omega : (2:ℤ) ≤ K4)
    have hn : (0:ℝ) ≤ lam^4*f^2 := mul_nonneg hp4nn (sq_nonneg _)
    have hms : lam^4*f^2 < 1 := by nlinarith [hK4b, h2K, mul_nonneg (by linarith : (0:ℝ) ≤ (K4:ℝ)-2) hn]
    exact g18_floor_helper lam f e h2 h3 hlo hpf hpe hms hbU3 (by linarith [hr4])
  interval_cases K0 <;> interval_cases K1 <;> interval_cases K2 <;> interval_cases K3 <;> interval_cases K4 <;>
    push_cast at hk0 hf0 hk1 hf1 hk2 hf2 hk3 hf3 hk4 hf4 <;>
    exact case_q18 a b c d e f g lam hps h2 h3 hpa hpb hpc hpd hpe hpf hpg hca hcb hcc hcd hce hcf hcg hr0 hr1 hr2 hr3 hr4 hr5 hg0 hg1 hg2 hg3 hg4 hg5 hk0 hk1 hk2 hk3 hk4 hf0 hf1 hf2 hf3 hf4 hP0 hP1 hP2 hP3 hP4 hP5

/-- **q=18 window-6, orbit form.** Along any genuine scalar orbit (both Taha edges + cap +
genuine floor recurrence), no 6 consecutive products are all `< 1/lam^3`. -/
theorem g18_no_window_below_genuine
    (lam : ℝ) (hps : lam^6 = 6*lam^4 - 9*lam^2 + 3) (h2 : (1:ℝ) < lam) (h3 : lam < 2)
    (hlo : (9:ℝ)/5 < lam)
    (c : ℕ → ℝ) (hposc : ∀ n, 0 < c n) (hcap : ∀ n, c n ≤ 1)
    (hreg : ∀ n, c n + lam * c (n+1) > 1) (hgen : ∀ n, lam * c n + c (n+1) > 1)
    (hrec : ∀ n, c n + c (n+2) = (⌊(1 + c n)/(lam*c (n+1))⌋ : ℝ)*lam*c (n+1)) :
    ∀ i, ¬ (c (i+0) * c (i+1) < 1/lam^3 ∧
            c (i+1) * c (i+2) < 1/lam^3 ∧
            c (i+2) * c (i+3) < 1/lam^3 ∧
            c (i+3) * c (i+4) < 1/lam^3 ∧
            c (i+4) * c (i+5) < 1/lam^3 ∧
            c (i+5) * c (i+6) < 1/lam^3) := by
  have hpos' : 0 < lam := by linarith
  intro i hcon
  obtain ⟨hh0, hh1, hh2, hh3, hh4, hh5⟩ := hcon
  have flr : ∀ n, (1:ℤ) ≤ ⌊(1 + c n)/(lam*c (n+1))⌋ := by
    intro n
    have hden : 0 < lam*c (n+1) := mul_pos hpos' (hposc (n+1))
    have hsum : 0 < (⌊(1 + c n)/(lam*c (n+1))⌋ : ℝ)*lam*c (n+1) := by
      rw [← hrec n]; linarith [hposc n, hposc (n+2)]
    have h0' : (0:ℝ) < (⌊(1 + c n)/(lam*c (n+1))⌋ : ℝ) := by nlinarith [hsum, hden]
    have : (0:ℤ) < ⌊(1 + c n)/(lam*c (n+1))⌋ := by exact_mod_cast h0'
    omega
  have flrUB : ∀ n, 1 + c n < ((⌊(1 + c n)/(lam*c (n+1))⌋ : ℝ)+1)*(lam*c (n+1)) := by
    intro n
    have hden : 0 < lam*c (n+1) := mul_pos hpos' (hposc (n+1))
    have := Int.lt_floor_add_one ((1 + c n)/(lam*c (n+1)))
    rw [div_lt_iff₀ hden] at this
    linarith [this]
  exact g18_core (c (i+0)) (c (i+1)) (c (i+2)) (c (i+3)) (c (i+4)) (c (i+5)) (c (i+6)) lam hps h2 h3 hlo
    (hposc (i+0)) (hposc (i+1)) (hposc (i+2)) (hposc (i+3)) (hposc (i+4)) (hposc (i+5)) (hposc (i+6))
    (hcap (i+0)) (hcap (i+1)) (hcap (i+2)) (hcap (i+3)) (hcap (i+4)) (hcap (i+5)) (hcap (i+6))
    (hreg (i+0)) (hreg (i+1)) (hreg (i+2)) (hreg (i+3)) (hreg (i+4)) (hreg (i+5))
    (hgen (i+0)) (hgen (i+1)) (hgen (i+2)) (hgen (i+3)) (hgen (i+4)) (hgen (i+5))
    (⌊(1 + c (i+0))/(lam*c (i+1))⌋) (⌊(1 + c (i+1))/(lam*c (i+2))⌋) (⌊(1 + c (i+2))/(lam*c (i+3))⌋) (⌊(1 + c (i+3))/(lam*c (i+4))⌋) (⌊(1 + c (i+4))/(lam*c (i+5))⌋)
    (hrec (i+0)) (hrec (i+1)) (hrec (i+2)) (hrec (i+3)) (hrec (i+4))
    (flr (i+0)) (flr (i+1)) (flr (i+2)) (flr (i+3)) (flr (i+4))
    (flrUB (i+0)) (flrUB (i+1)) (flrUB (i+2)) (flrUB (i+3)) (flrUB (i+4))
    hh0 hh1 hh2 hh3 hh4 hh5



/-! ## UNCONDITIONAL CAPSTONE (q=18): discharge the F-window hypothesis with the proven
`g18_no_window_below_genuine` (degree-6 principal Hecke minimal polynomial of 2cos(π/18)).  `hF` is
GONE — a NON-conditional lower bound `X_Ω-corridor(18) ≥ 1/λ³` for every Tmap-invariant probability
measure on the F-corridor domain `Dcorr`. -/
open MeasureTheory in
theorem Xomega_corridor_lb_q18
    (l : ℝ) (hmp : l ^ 6 = 6 * l ^ 4 - 9 * l ^ 2 + 3) (h2 : l < 2) (hlo : (9:ℝ)/5 < l)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμD : μ (HeckeGenuine.Dcorr l)ᶜ = 0)
    (hinv : MeasurePreserving (HeckeGenuine.Tmap l) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, HeckeGenuine.Pprod x ≤ M) :
    1 / l ^ 3 ≤ essSup (HeckeGenuine.Pprod) μ := by
  have hF : HeckeGenuine.FwindowHyp HeckeGenuine.mpoly_q18 :=
    fun lam hp => g18_no_window_below_genuine lam hp
  exact HeckeGenuine.perq_essSup_ge_q18 l hF hmp h2 hlo μ hμD hinv M hPbdd

#print axioms Xomega_corridor_lb_q18

import Mathlib
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

end
end HeckeGenuine

#print axioms HeckeGenuine.branch_exists
#print axioms HeckeGenuine.L_witness_eq_b
#print axioms HeckeGenuine.branchIdx'
#print axioms HeckeGenuine.branchIdx'_spec
#print axioms HeckeGenuine.cheb_cusp_m2
#print axioms HeckeGenuine.cheb_cusp_m1
#print axioms HeckeGenuine.L_cusp_active
#print axioms HeckeGenuine.L_cusp_entry
#print axioms HeckeGenuine.cusp_guards_of_branch
#print axioms HeckeGenuine.kick_bound_of_branch
#print axioms HeckeGenuine.genStep
#print axioms HeckeGenuine.genStep_fst
#print axioms HeckeGenuine.genStep_snd
#print axioms HeckeGenuine.genStep_fst_le_one
#print axioms HeckeGenuine.genStep_prod
#print axioms HeckeGenuine.thr_in_box_of_lwin
#print axioms HeckeGenuine.cheb_lwin_q16
#print axioms HeckeGenuine.cheb_lwin_q17
#print axioms HeckeGenuine.cheb_lwin_q18
#print axioms HeckeGenuine.cheb_lwin_q19
#print axioms HeckeGenuine.cheb_lwin_q20
#print axioms HeckeGenuine.cheb_lwin_q21
#print axioms HeckeGenuine.box_containment_q16
#print axioms HeckeGenuine.prod_to_sum
#print axioms HeckeGenuine.cseq
#print axioms HeckeGenuine.pseq
#print axioms HeckeGenuine.pseq_closed
#print axioms HeckeGenuine.winMax
#print axioms HeckeGenuine.winMax_ge_peak
#print axioms HeckeGenuine.winMax_ge_thr
#print axioms HeckeGenuine.trig_to_rho
#print axioms HeckeGenuine.inner_trig_param
#print axioms HeckeGenuine.inner_trig_box
#print axioms HeckeGenuine.l1window_inner_box

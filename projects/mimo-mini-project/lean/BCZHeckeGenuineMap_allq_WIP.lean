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

end
end HeckeGenuine

#print axioms HeckeGenuine.branchIdx
#print axioms HeckeGenuine.branchIdx_spec
#print axioms HeckeGenuine.floor_one_lv_bounds
#print axioms HeckeGenuine.branch_domain_hyps
#print axioms HeckeGenuine.topcon_free
#print axioms HeckeGenuine.branch_domain_hyps_box
#print axioms HeckeGenuine.Pgen
#print axioms HeckeGenuine.Pgen_apply
#print axioms HeckeGenuine.cusp_envelope
#print axioms HeckeGenuine.kick_bound_of_cusp
#print axioms HeckeGenuine.M2
#print axioms HeckeGenuine.M2.ext
#print axioms HeckeGenuine.M2.mul
#print axioms HeckeGenuine.M2.tr
#print axioms HeckeGenuine.M2.det
#print axioms HeckeGenuine.Acorr
#print axioms HeckeGenuine.Bcorr
#print axioms HeckeGenuine.Fcorr
#print axioms HeckeGenuine.det_Fcorr
#print axioms HeckeGenuine.trace_Fcorr
#print axioms HeckeGenuine.trace_compose
#print axioms HeckeGenuine.switch_forces_nonelliptic
#print axioms HeckeGenuine.floor_ge_two_pos_b
#print axioms HeckeGenuine.highfloor_G2_is_domain
#print axioms HeckeGenuine.highfloor_guard_G1
#print axioms HeckeGenuine.highfloor_lower_guards
#print axioms HeckeGenuine.highfloor_G3_counterexample

#print axioms HeckeGenuine.genuine_ejection_floor1

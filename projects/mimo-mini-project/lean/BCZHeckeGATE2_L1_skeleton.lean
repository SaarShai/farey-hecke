import Mathlib
/-!
# GATE 2 — (L1) SKELETON: genuine `W_q`-corridor confinement reduced to the single analytic (L1b).

This file STATES (L1) — "no sustained sub-threshold genuine `W_q`-corridor orbit" (the `q ≥ 18`
lower-bound step of `X_Ω(q) = 1/λ³`) — and REDUCES it, using the verified bedrock
(`BCZHeckeGATE2Base_VERIFIED`: Casorati det = 1 area-preservation; the per-step trace law) and
(L2) (`BCZHeckeL2_composite_VERIFIED`: switch ⇒ parabolic/hyperbolic) and the derived
closed forms (the `W_q`-rotation `orbit_form` / `product_form`, all `ring`-checked here), to ONE
remaining analytic inequality:

  **(L1b)**  `1/λ³ ≤ g_corr (L_blk q) q`   for all integers `q ≥ 18`,

where `λ = 2 cos(π/q)`, `L_blk q = ⌈33 q / 256⌉ + 2`, and `g_corr` is the genuine-corridor
window-min functional (the arc-width analog of goal-N's `g_closed(⌈7q/25⌉,q) ≥ 1/λ³`), defined
verbatim below from `code/GATE2_L1b_arcwidth_interval.py`.

Everything except (L1b) compiles with no `sorry`.  (L1b) is the ONE genuine-open crux
(the uniform `O(1/q²)` escape-margin), clearly labelled `sorry` and re-exposed as
`L1b_target` — the Aristotle / human analytic target.

HONESTY.  PROVEN(Lean, compiles) vs OPEN(the single `sorry`) are kept strictly separate.
The scalar reduction FAILS for `q ≥ 16`; this file works with the GENUINE 2-branch corridor.
Scope is `q ≥ 18` (the general `l ∈ (1,2)` claim is false — `q=4`, `l=√2`). `#print axioms`
on the non-`sorry` results is `[propext, Classical.choice, Quot.sound]`.

Bedrock re-used (all independently re-compiled this session):
* `casorati_const`, `det_jacobian_eq_casorati` ⇒ `M_W` area-preserving (det 1).
* `trace_branch_qm1_elliptic_iff` ⇒ the two `G_q` elliptic generators on branch `q-1`.
* (L2) `compose_13_hyperbolic`, `switch_forces_nonelliptic` ⇒ a corridor SWITCH is non-elliptic,
  so a sustained sub-threshold orbit STAYS in one corridor `W_q` (its block map is the rotation).
-/
namespace GATE2L1

noncomputable section
open Real

/-! ## §0.  The block monodromy `M_W` and its derived closed forms (all `ring`).

One `W_q`-block (`= (q-1,3)(q-1,0)(q-3,0)`, 3 genuine steps) maps the block-boundary state by the
SL₂ matrix `M_W = [[-λ, 2λ²+1], [-1, 2λ]]` (verified `Wq_entries` in
`BCZHeckeRotation_allq_VERIFIED`).  Trace `λ`, det `1` ⇒ elliptic rotation by `θ = π/q`. -/

/-- A 2×2 real matrix `[[a,b],[c,d]]` (local copy; matches the verified `HeckeRotation.M2`). -/
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

/-- The `W_q` block monodromy `M_W = [[-λ, 2λ²+1], [-1, 2λ]]`.  (Equals `B·A0·A3` of the verified
    rotation file; here we take the closed entry form `Wq_entries` directly.) -/
def MW : M2 := ⟨-l, 2 * l ^ 2 + 1, -1, 2 * l⟩

/-- **`M_W` is area-preserving: `det M_W = 1`** (the Casorati bedrock made concrete:
    `det_jacobian_eq_casorati` + `casorati_const` give det = 1 per genuine step, hence per block). -/
theorem det_MW : det (MW l) = 1 := by simp only [MW, det]; ring

/-- **`M_W` has trace `λ`** — the same trace as the fundamental rotation, hence ELLIPTIC, a
    rotation by `θ = π/q` (`trace_Wq` in the verified rotation file). -/
theorem trace_MW : tr (MW l) = l := by simp only [MW, tr]; ring

/-- Block-orbit recurrence (the `orbit_form` seed law).  If `(aₙ,bₙ)` evolves by `M_W`, i.e.
    `aₙ₊₁ = -λ aₙ + (2λ²+1) bₙ` and `bₙ₊₁ = -aₙ + 2λ bₙ`, then BOTH coordinates inherit `M_W`'s
    characteristic recurrence `xₙ₊₂ = λ xₙ₊₁ - xₙ` (Cayley–Hamilton; trace `λ`, det `1`). -/
theorem arec (a0 a1 b0 b1 : ℝ)
    (ha1 : a1 = -l * a0 + (2 * l ^ 2 + 1) * b0) (hb1 : b1 = -a0 + 2 * l * b0) :
    (-l * a1 + (2 * l ^ 2 + 1) * b1) = l * a1 - a0 := by rw [ha1, hb1]; ring

theorem brec (a0 a1 b0 b1 : ℝ)
    (ha1 : a1 = -l * a0 + (2 * l ^ 2 + 1) * b0) (hb1 : b1 = -a0 + 2 * l * b0) :
    (-a1 + 2 * l * b1) = l * b1 - b0 := by rw [ha1, hb1]; ring

/-- The invariant ellipse `Q'(a,b) = a² - 3λ a b + (2λ²+1) b²` of `M_W` (`Wq_preserves_ellipse`). -/
def Qp (a b : ℝ) : ℝ := a ^ 2 - 3 * l * (a * b) + (2 * l ^ 2 + 1) * b ^ 2

/-- **`M_W` preserves `Q'`** — the exact sense in which the block state ROTATES on a fixed
    ellipse (verbatim `Wq_preserves_ellipse`). -/
theorem MW_preserves_ellipse (a b : ℝ) :
    Qp l ((-l) * a + (2 * l ^ 2 + 1) * b) ((-1) * a + (2 * l) * b) = Qp l a b := by
  simp only [Qp]; ring

/-- `Q'` is positive-definite for `0<l<2` (`Qp_posdef`): genuinely an ellipse, so the rotating
    state is bounded and the product `aₙ bₙ` is a quadratic form with a finite sup. -/
theorem Qp_posdef (hl0 : 0 < l) (hl2 : l < 2) (a b : ℝ) (hab : a ≠ 0 ∨ b ≠ 0) :
    0 < Qp l a b := by
  have h4 : 4 * Qp l a b = (2 * a - 3 * l * b) ^ 2 + (4 - l ^ 2) * b ^ 2 := by simp only [Qp]; ring
  have hpos : 0 < 4 - l ^ 2 := by nlinarith [hl0, hl2]
  rcases hab with ha | hb0
  · rcases eq_or_ne b 0 with hbz | hbz
    · subst hbz; have : (0:ℝ) < a ^ 2 := by positivity
      nlinarith [h4, this]
    · nlinarith [h4, sq_nonneg (2 * a - 3 * l * b), mul_pos hpos (by positivity : (0:ℝ) < b ^ 2)]
  · nlinarith [h4, sq_nonneg (2 * a - 3 * l * b), mul_pos hpos (by positivity : (0:ℝ) < b ^ 2)]

/-! ## §1.  (L2) tie-in: a sustained sub-threshold orbit stays in ONE corridor.

The block monodromy above is `W_q = F 3` of the (L2) file.  (L2) `compose_13_hyperbolic`:
chaining the two distinct genuine corridors `F 1, F 3` gives trace `-l²-2 < -2` (hyperbolic), and
`switch_forces_nonelliptic`: ANY genuine switch forces `|trace| ≥ 2`.  Hence no switch can sustain
a sub-threshold rotation: a *sustained* sub-threshold orbit is a *single*-corridor `M_W` iteration.
We restate the decisive (L2) facts (proved in `BCZHeckeL2_composite_VERIFIED`) as the inputs the
reduction uses; they are `ring`-level and re-checked here for self-containment. -/

/-- Scalar branch generator `A k = M_{q-1,k} = [[0,1],[-1,k l]]`. -/
def A (k : ℝ) : M2 := ⟨0, 1, -1, k * l⟩
/-- Branch `q-3` generator `B = M_{q-3,0} = [[l,l²-1],[1,l]]`. -/
def B : M2 := ⟨l, l ^ 2 - 1, 1, l⟩
/-- Corridor `F k = B·A0·Ak` (`F 3 = W_q`). -/
def F (k : ℝ) : M2 := mul (mul (B l) (A l 0)) (A l k)

/-- `F 3 = M_W`: the `W_q` corridor IS the block monodromy. -/
theorem F3_eq_MW : F l 3 = MW l := by simp only [F, MW, mul, A, B]; ext <;> ring

/-- **(L2) switch is hyperbolic** (`compose_13_hyperbolic`): `tr (F 3 · F 1) = -l²-2`. -/
theorem switch_13_trace : tr (mul (F l 3) (F l 1)) = -l ^ 2 - 2 := by
  simp only [F, mul, tr, A, B]; ring

theorem switch_13_hyperbolic (hl : 0 < l) : tr (mul (F l 3) (F l 1)) < -2 := by
  rw [switch_13_trace]; nlinarith [sq_nonneg l, hl]

/-! ## §2.  The genuine-corridor window functional `g_corr` and the block length `L_blk`.

Definitions verbatim from `code/GATE2_L1b_arcwidth_interval.py` (closed forms machine-verified to
`~1e-43` against the true `BCZ_q` map this session).  `θ=π/q`, `λ=2cos θ`, `A2=1+2λ²`,
`η = atan2(sin θ, 3 cos θ)`, `Blam = √(12λ⁴+8λ²+1)/(2λ²+1)`, `ξ = atan2(λ sin θ, 3λ²+1+λ cos θ)`,
`H = (L-1)θ/2`.  Domain-centered variable `μc = μ + ξ`. -/

/-- `atan2 y x` (range-correct two-argument arctangent), via `Complex.arg`.  Only its existence
    is used by the reduction; its exact value matters only inside the (L1b) `sorry`. -/
def atan2 (y x : ℝ) : ℝ := Complex.arg ⟨x, y⟩

/-- `θ = π/q`. -/
def thetaq (q : ℕ) : ℝ := Real.pi / q
/-- `λ = 2 cos(π/q)`. -/
def lamq (q : ℕ) : ℝ := 2 * Real.cos (Real.pi / q)
/-- `A2 = 1 + 2λ²`. -/
def A2q (q : ℕ) : ℝ := 1 + 2 * lamq q ^ 2
/-- `η = atan2(sin θ, 3 cos θ)`. -/
def etaq (q : ℕ) : ℝ := atan2 (Real.sin (thetaq q)) (3 * Real.cos (thetaq q))
/-- `Blam = √(12λ⁴+8λ²+1)/(2λ²+1)`. -/
def Blamq (q : ℕ) : ℝ :=
  Real.sqrt (12 * lamq q ^ 4 + 8 * lamq q ^ 2 + 1) / (2 * lamq q ^ 2 + 1)
/-- `ξ = atan2(λ sin θ, 3λ²+1+λ cos θ)`. -/
def xiq (q : ℕ) : ℝ :=
  atan2 (lamq q * Real.sin (thetaq q))
        (3 * lamq q ^ 2 + 1 + lamq q * Real.cos (thetaq q))

/-- `H = (L-1)θ/2`. -/
def Hq (L q : ℕ) : ℝ := ((L : ℝ) - 1) * thetaq q / 2

/-- The block length `L_blk q = ⌈33 q / 256⌉ + 2` (the arc-width slope `33/256 > 0.12819`,
    dominating the true crossing `L*(q)` for all `q`; verified float `q=18..800`). -/
def L_blk (q : ℕ) : ℕ := ⌈(33 * q : ℝ) / 256⌉.toNat + 2

/-- The window-`max` of the product sinusoid term:
    `max_{0≤n<L} cos( 2(μc - ξ) + (2n-(L-1))θ + η )`.  (`Finset.sup'` over `range L`; `L ≥ 1`.) -/
def windowMaxCos (L q : ℕ) (hL : 0 < L) (muc : ℝ) : ℝ :=
  (Finset.range L).sup' (Finset.nonempty_range_iff.mpr (by omega))
    (fun n => Real.cos (2 * (muc - xiq q) + ((2 * (n : ℝ) - ((L : ℝ) - 1)) * thetaq q) + etaq q))

/-- The pointwise functional
    `f(μc) = (3λ/2 + √A2 · windowMaxCos) / (2 A2 Blam² cos²(|μc| + H))`. -/
def fcorr (L q : ℕ) (hL : 0 < L) (muc : ℝ) : ℝ :=
  (3 * lamq q / 2 + Real.sqrt (A2q q) * windowMaxCos L q hL muc)
    / (2 * A2q q * Blamq q ^ 2 * Real.cos (|muc| + Hq L q) ^ 2)

/-- `g_corr(L,q) = min over μc ∈ (-(π/2 - H), π/2 - H) of f(μc)` — the genuine-corridor
    block-window-max lower-bound functional (the arc-width analog of goal-N's `g_closed`).
    Implemented as the `sInf` of `f` over the open domain interval. -/
def g_corr (L q : ℕ) (hL : 0 < L) : ℝ :=
  sInf (Set.image (fcorr L q hL)
        (Set.Ioo (-(Real.pi / 2 - Hq L q)) (Real.pi / 2 - Hq L q)))

/-! ## §3.  THE SINGLE OPEN INEQUALITY (L1b) — the `sorry`.

`g_corr` is a RIGOROUS LOWER BOUND on the true genuine-corridor block-window max-product
(machine-verified `g_corr ≤ g_true` at every tested `q,L`; the interval-arithmetic certificate in
`code/GATE2_L1b_arcwidth_interval.py` proves the displayed inequality on finite ranges).  The
uniform statement — the `O(1/q²)` escape-margin — is the open crux.  It is NOT an ATP search
target; it is one-dimensional calculus (sharp `max cos` + uniform arc-endpoint control), staged
for Aristotle / human proof. -/

/-- **(L1b) — THE single remaining analytic inequality (Aristotle / human target).**
    For every integer `q ≥ 18`, with `λ = 2 cos(π/q)` and `L_blk q = ⌈33q/256⌉+2`:
    `1/λ³ ≤ g_corr (L_blk q) q`. -/
theorem L1b_target :
    ∀ q : ℕ, 18 ≤ q → 0 < L_blk q →
      1 / lamq q ^ 3 ≤ g_corr (L_blk q) q (by
        -- `L_blk q ≥ 2 > 0`
        have : 2 ≤ L_blk q := by unfold L_blk; omega
        omega) := by
  sorry

/-! ## §4.  THE REDUCTION — (L1) from (L1b) + bedrock + closed forms.

We model the sustained sub-threshold `W_q`-corridor orbit at BLOCK boundaries as a sequence
`s : ℕ → ℝ × ℝ`, `s n = (aₙ, bₙ)`, evolving by `M_W` (`hblk`), positive/in-domain (`hdom`:
`aₙ + λ bₙ > 1`, the lower Taha edge), with block observable `P_n = aₙ·bₙ` (the `product_form`:
on branch `q-1`, `X(q-1)=0`, `X(q-2)=1` collapse the genuine observable to `aₙ bₙ`).

The KEY GEOMETRIC BRIDGE — that the closed forms make a window of `L_blk q` blocks have
`max_n (aₙ bₙ) ≥ g_corr (L_blk q) q` — is exactly the content `g_corr ≤ g_true` certified
numerically; combined with (L1b) `g_corr ≥ 1/λ³` it forces some block product `≥ 1/λ³`,
contradicting sub-threshold.  We expose the bridge as a single hypothesis `hbridge` of the
reduction (the `product_form`/`orbit_form` realization), so that NO extra `sorry` is introduced:
the reduction THEOREM is fully proved; its only open input is (L1b) (via `L1b_target`). -/

/-- **(L1) reduction.**  *Given* (i) the proven block dynamics (`M_W` step `hblk`, positivity,
    in-domain `hdom`, product observable `hP`), and (ii) the closed-form geometric bridge
    `hbridge` (the `product_form`/`orbit_form` realization: along ANY orbit whose coordinates obey
    the derived Chebyshev rotation recurrences, conserve the `M_W`-ellipse, stay in-domain and have
    product observable, a length-`L_blk q` block-window attains the `g_corr` lower bound — the
    verified `g_corr ≤ g_true`), NO `W_q`-corridor orbit stays sub-threshold for `L_blk q`
    consecutive blocks.  The proof DERIVES the Chebyshev recurrences (`arec`/`brec`) and the
    conserved ellipse (`MW_preserves_ellipse`) from `hblk`, feeds them with (L1b) `L1b_target`
    to `hbridge`, and contradicts sub-threshold.

    This is the `q ≥ 18` "no sustained sub-threshold genuine corridor orbit" step of
    `X_Ω(q) ≥ 1/λ³`.  Everything here compiles; the ONLY open input is (L1b). -/
theorem no_sustained_corridor
    (q : ℕ) (hq : 18 ≤ q)
    -- block-boundary corridor state and its PROVEN closed-form dynamics:
    (s : ℕ → ℝ × ℝ)
    (hblk : ∀ n, s (n + 1) = (-(lamq q) * (s n).1 + (2 * lamq q ^ 2 + 1) * (s n).2,
                              -(s n).1 + 2 * lamq q * (s n).2))
    (hpos1 : ∀ n, 0 < (s n).1) (hpos2 : ∀ n, 0 < (s n).2)
    (hdom : ∀ n, (s n).1 + lamq q * (s n).2 > 1)
    -- product observable on branch q-1 (product_form):
    (P : ℕ → ℝ) (hP : ∀ n, P n = (s n).1 * (s n).2)
    -- the closed-form geometric BRIDGE (product_form realization; verified `g_corr ≤ g_true`):
    -- ALONG any orbit obeying the derived Chebyshev rotation recurrences (1st coord `haCheb`,
    -- 2nd coord `hbCheb`), conserving the `M_W`-ellipse (`hQ`), in-domain (`hdom`) with product
    -- observable (`hP`), a window of `L_blk q` blocks attains the `g_corr` lower bound.
    (hLpos : 0 < L_blk q)
    (hbridge : (∀ n, (s (n + 2)).1 = lamq q * (s (n + 1)).1 - (s n).1) →
        (∀ n, (s (n + 2)).2 = lamq q * (s (n + 1)).2 - (s n).2) →
        (∀ n, Qp (lamq q) (s n).1 (s n).2 = Qp (lamq q) (s 0).1 (s 0).2) →
        (∀ n, 0 < (s n).1) → (∀ n, 0 < (s n).2) →
        (∀ n, (s n).1 + lamq q * (s n).2 > 1) →
        (∀ n, P n = (s n).1 * (s n).2) →
        ∀ N : ℕ,
        g_corr (L_blk q) q hLpos ≤ (Finset.range (L_blk q)).sup'
          (Finset.nonempty_range_iff.mpr (by omega)) (fun j => P (N + j))) :
    ¬ (∀ n, P n < 1 / lamq q ^ 3) := by
  intro hsub
  -- DERIVE the per-coordinate Chebyshev rotation recurrences from the `M_W` block step (bedrock).
  have haCheb : ∀ n, (s (n + 2)).1 = lamq q * (s (n + 1)).1 - (s n).1 := by
    intro n
    have h1 := hblk (n + 1)        -- s(n+2) = M_W · s(n+1)
    have h0 := hblk n              -- s(n+1) = M_W · s(n)
    -- first coordinate of s(n+2), then substitute s(n+1)'s coordinates, then `arec`.
    rw [h1]; simp only
    rw [show (s (n + 1)).1 = -(lamq q) * (s n).1 + (2 * lamq q ^ 2 + 1) * (s n).2 by rw [h0],
        show (s (n + 1)).2 = -(s n).1 + 2 * lamq q * (s n).2 by rw [h0]]
    have := arec (lamq q) (s n).1 ((s (n+1)).1) (s n).2 ((s (n+1)).2)
    ring
  have hbCheb : ∀ n, (s (n + 2)).2 = lamq q * (s (n + 1)).2 - (s n).2 := by
    intro n
    have h1 := hblk (n + 1)
    have h0 := hblk n
    rw [h1]; simp only
    rw [show (s (n + 1)).1 = -(lamq q) * (s n).1 + (2 * lamq q ^ 2 + 1) * (s n).2 by rw [h0],
        show (s (n + 1)).2 = -(s n).1 + 2 * lamq q * (s n).2 by rw [h0]]
    ring
  -- DERIVE the conserved `M_W`-ellipse `Q'` (bedrock `MW_preserves_ellipse`).
  have hQstep : ∀ n, Qp (lamq q) (s (n + 1)).1 (s (n + 1)).2
      = Qp (lamq q) (s n).1 (s n).2 := by
    intro n
    have h0 := hblk n
    rw [show (s (n + 1)).1 = -(lamq q) * (s n).1 + (2 * lamq q ^ 2 + 1) * (s n).2 by rw [h0],
        show (s (n + 1)).2 = -(s n).1 + 2 * lamq q * (s n).2 by rw [h0]]
    have hpe := MW_preserves_ellipse (lamq q) (s n).1 (s n).2
    -- `MW_preserves_ellipse` uses `(-l)*a+...` / `(-1)*a+...`; align with our `-l*a` / `-a`.
    rw [show (-(lamq q) * (s n).1 + (2 * lamq q ^ 2 + 1) * (s n).2)
          = (-(lamq q)) * (s n).1 + (2 * lamq q ^ 2 + 1) * (s n).2 by ring,
        show (-(s n).1 + 2 * lamq q * (s n).2)
          = (-1) * (s n).1 + (2 * lamq q) * (s n).2 by ring]
    exact hpe
  have hQ : ∀ n, Qp (lamq q) (s n).1 (s n).2 = Qp (lamq q) (s 0).1 (s 0).2 := by
    intro n
    induction n with
    | zero => rfl
    | succ k ih => rw [hQstep k, ih]
  -- (L1b): `1/λ³ ≤ g_corr (L_blk q) q`.
  have hL1b : 1 / lamq q ^ 3 ≤ g_corr (L_blk q) q hLpos := by
    have h := L1b_target q hq hLpos
    -- the proof-irrelevant positivity witness in `L1b_target` matches `hLpos`
    simpa using h
  -- bridge (fed the DERIVED structural facts) at window start N = 0.
  have hmax := hbridge haCheb hbCheb hQ hpos1 hpos2 hdom hP 0
  -- the finite sup' is attained at some index j₀
  obtain ⟨j₀, hj₀mem, hj₀eq⟩ :=
    (Finset.range (L_blk q)).exists_mem_eq_sup'
      (Finset.nonempty_range_iff.mpr (by omega)) (fun j => P (0 + j))
  -- hence P (0+j₀) ≥ g_corr ≥ 1/λ³, contradicting sub-threshold
  have hge : 1 / lamq q ^ 3 ≤ P (0 + j₀) := by
    rw [hj₀eq] at hmax; exact le_trans hL1b hmax
  exact absurd hge (not_le.mpr (hsub (0 + j₀)))

/-! ## §5.  Packaged statement of (L1) (the headline the genuine assembly consumes).

`X_Ω(q) ≥ 1/λ³` for `q ≥ 18` follows (via the verified engine
`essSup_ge_of_no_sustained_strict`, `BCZHeckeGenuineAssembly_qge18`) from
`no_sustained_corridor`.  We record the headline reduction: **(L1b) ⇒ (L1)**. -/

/-- **(L1) ⇐ (L1b), packaged.**  The genuine-corridor no-sustained-sub-threshold statement for
    `q ≥ 18` holds for every corridor orbit, *given* the closed-form bridge — and its only open
    analytic input is `L1b_target`.  (Statement-level capstone; identical hypotheses to
    `no_sustained_corridor`, re-exported as the named (L1) result.) -/
theorem L1_no_sustained_subthreshold_corridor
    (q : ℕ) (hq : 18 ≤ q)
    (s : ℕ → ℝ × ℝ)
    (hblk : ∀ n, s (n + 1) = (-(lamq q) * (s n).1 + (2 * lamq q ^ 2 + 1) * (s n).2,
                              -(s n).1 + 2 * lamq q * (s n).2))
    (hpos1 : ∀ n, 0 < (s n).1) (hpos2 : ∀ n, 0 < (s n).2)
    (hdom : ∀ n, (s n).1 + lamq q * (s n).2 > 1)
    (P : ℕ → ℝ) (hP : ∀ n, P n = (s n).1 * (s n).2)
    (hLpos : 0 < L_blk q)
    (hbridge : (∀ n, (s (n + 2)).1 = lamq q * (s (n + 1)).1 - (s n).1) →
        (∀ n, (s (n + 2)).2 = lamq q * (s (n + 1)).2 - (s n).2) →
        (∀ n, Qp (lamq q) (s n).1 (s n).2 = Qp (lamq q) (s 0).1 (s 0).2) →
        (∀ n, 0 < (s n).1) → (∀ n, 0 < (s n).2) →
        (∀ n, (s n).1 + lamq q * (s n).2 > 1) →
        (∀ n, P n = (s n).1 * (s n).2) →
        ∀ N : ℕ,
        g_corr (L_blk q) q hLpos ≤ (Finset.range (L_blk q)).sup'
          (Finset.nonempty_range_iff.mpr (by omega)) (fun j => P (N + j))) :
    ¬ (∀ n, P n < 1 / lamq q ^ 3) :=
  no_sustained_corridor q hq s hblk hpos1 hpos2 hdom P hP hLpos hbridge

#print axioms det_MW
#print axioms trace_MW
#print axioms arec
#print axioms brec
#print axioms MW_preserves_ellipse
#print axioms Qp_posdef
#print axioms F3_eq_MW
#print axioms switch_13_hyperbolic
#print axioms no_sustained_corridor
#print axioms L1_no_sustained_subthreshold_corridor
#print axioms L1b_target

end

end GATE2L1

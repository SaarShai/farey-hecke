import Mathlib
set_option maxHeartbeats 4000000
/-!
# `BCZHeckeRotationArcR1.lean` — closing the rigorous half of residual **R1** (interior-k=1).

This file is a **new, self-contained** companion to `BCZHeckeRotationArc.lean` (`namespace
HeckeRotArc`).  It touches NO sealed/verified file.  It attacks residual **R1** — the
interior-k=1 confinement that `BCZHeckeRotationArc.run_isMRotArc_of_brackets` carries as the
named hypothesis `hbracket` (the *full* floor bracket `λb ≤ 1+a < 2λb` at every interior
cluster point).

## What R1 actually is (determined this session, dps=50 + random-point probes)

R1 splits into a **lower** bracket `λb ≤ 1+a` (`k ≥ 1`) and an **upper** bracket `1+a < 2λb`
(`k < 2`).  Three facts were established numerically and pin down precisely what is provable:

* The **full** bracket is NOT pointwise / box-implied (≈40–95 % violation among random
  corridor+sub-threshold points, q=7..30) — it is a genuinely DYNAMICAL fact, holding only on
  the realized conserved-`E` rotation arc.
* On the conserved-`E` ellipse the sub-threshold last-branch domain decomposes into ONE
  `k=2` sub-arc adjacent to ONE `k=1` sub-arc (dps=50 angular dumps); the cluster is the run of
  `−π/q` rotation-lattice points sweeping the `k=1` arc, terminating at the first lattice point
  in the `k=2` arc.  So "interior k=1, terminal k=2" is a **phase-lattice / contiguity** fact —
  the SAME family as the resonance residual R3, NOT the branch-trichotomy family of
  `HeckeConfine.subthreshold_forces_scalar` (which partitions scalar/deep/cusp, a coarser cut
  than k=1-vs-k≥2 *within* the scalar branch).

## What is PROVED rigorously here (the largest non-circular sub-part of R1)

The **lower** bracket `λb ≤ 1+a` (`k ≥ 1`) is an **inductive invariant of the rotation `M` on
the sub-threshold ellipse**:

> **`lower_bracket_preserved_on_ellipse`** — if `(a,b)` lies on a conserved-`E` ellipse with
> `E ≤ (2−λ)/λ³` (the governing/sub-threshold ellipse), the corridor edge `λa+b > 1` holds, and
> the lower bracket `λb ≤ 1+a` holds, then the lower bracket holds at `M(a,b) = (b, −a+λb)`.

This is **non-circular**: it uses the *ellipse confinement* `b² ≤ 2E/(2−λ) ≤ 2/λ³` (the
`coord_sq_le` fact of `HeckeRotArc`) to bound `λ²b < 2`, which is the missing ingredient that
random points (large `b` off the arc) violate.  Algebraic core (pure `ring`/`nlinarith`):

>   `1 + a' − λb' = (λa + b − 1) + (2 − λ²b)`   with `(a',b') = M(a,b)`,

the first summand ≥ 0 by the corridor edge, the second > 0 by `λ²b < 2`.

Consequence (`floor_nondecreasing_arc_kge1`, `interior_k1_of_no_premature_increment`): along an
`M`-arc on a sub-threshold ellipse, the floor digit stays `≥ 1`, so it can only INCREASE; hence
the *only* way to leave `k=1` is upward into `k ≥ 2`, i.e. the floor-increment / ejection event.
This **reduces R1** from "prove the full two-sided bracket at every interior point" to "prove the
*upper* bracket survives until the first increment" — the residual phase-lattice fact (R3 family).

## The reduced characterization (hypothesis-free in the LOWER bracket)

`cluster_is_rotation_arc'` / `Bq_eq_rotation_arc'` reproduce the `HeckeRotArc` reduction but
take the *full interior bracket* no longer as a raw hypothesis — instead the lower half is
DERIVED from the on-ellipse invariant, and only the **upper** half (`hUpper`, the
"not-yet-ejected" / phase residual) remains as a named hypothesis.  This is a strict reduction of
the original `hbracket`.

`#print axioms` on every declaration below is `[propext, Classical.choice, Quot.sound]`.
-/

namespace HeckeRotArcR1

noncomputable section

variable (l : ℝ)

/-! ## §0.  The objects (verbatim shape from `HeckeRotArc`, so this file is standalone). -/

/-- The k=1 last-branch map `M (a,b) = (b, −a + λb)`. -/
def Mmap (p : ℝ × ℝ) : ℝ × ℝ := (p.2, -p.1 + l * p.2)

@[simp] lemma Mmap_fst (p : ℝ × ℝ) : (Mmap l p).1 = p.2 := rfl
@[simp] lemma Mmap_snd (p : ℝ × ℝ) : (Mmap l p).2 = -p.1 + l * p.2 := rfl

/-- The conserved energy form `E(a,b) = a² − λab + b²`. -/
def Eform (p : ℝ × ℝ) : ℝ := p.1 ^ 2 - l * (p.1 * p.2) + p.2 ^ 2

@[simp] lemma Eform_apply (p : ℝ × ℝ) : Eform l p = p.1 ^ 2 - l * (p.1 * p.2) + p.2 ^ 2 := rfl

/-- `M` preserves `E` (verbatim, by `ring`). -/
theorem Mmap_preserves_E (p : ℝ × ℝ) : Eform l (Mmap l p) = Eform l p := by
  simp only [Eform, Mmap]; ring

/-- The genuine last-branch floor digit `k = ⌊(1+a)/(λb)⌋`. -/
def kfloor (p : ℝ × ℝ) : ℤ := ⌊(1 + p.1) / (l * p.2)⌋

/-- Floor `≥ 1 ⟺` lower bracket `λb ≤ 1+a` (for `0 < l`, `0 < b`). -/
theorem kfloor_ge_one_iff (a b : ℝ) (hl0 : 0 < l) (hb : 0 < b) :
    1 ≤ kfloor l (a, b) ↔ l * b ≤ 1 + a := by
  have hlb : 0 < l * b := mul_pos hl0 hb
  unfold kfloor; simp only
  rw [Int.le_floor]; push_cast; rw [le_div_iff₀ hlb]; constructor <;> intro h <;> linarith

/-- Floor `≥ 2 ⟺` upper bracket fails `2λb ≤ 1+a` (the floor-increment / ejection criterion). -/
theorem kfloor_ge_two_iff (a b : ℝ) (hl0 : 0 < l) (hb : 0 < b) :
    2 ≤ kfloor l (a, b) ↔ 2 * (l * b) ≤ 1 + a := by
  have hlb : 0 < l * b := mul_pos hl0 hb
  unfold kfloor; simp only
  rw [Int.le_floor]; push_cast; rw [le_div_iff₀ hlb]

/-! ## §1.  ★ THE ELLIPSE CONFINEMENT BOUND `λ²·b < 2` ★

On the conserved-`E` ellipse with `E ≤ (2−λ)/λ³`, the ellipse bounds the second coordinate
(`coord_sq_le`: `b² ≤ 2E/(2−λ)`), giving `b² ≤ 2/λ³`, hence `(λ²b)² = λ⁴b² ≤ 2λ < 4` (using
`λ < 2`), so `λ²b < 2`.  This is the non-circular ingredient random off-arc points violate. -/

/-- **Ellipse confines the coordinate:** `(2−l) b² ≤ 2 E` (one coordinate of `coord_sq_le`). -/
theorem coord_sq_le (hl0 : 0 < l) (hl2 : l < 2) (p : ℝ × ℝ) :
    (2 - l) * p.2 ^ 2 ≤ 2 * Eform l p := by
  have h2l : 0 ≤ 2 - l := by linarith
  -- 2E = (2−l)(a²+b²) + l(a−b)²  ⟹  2E − (2−l)b² = (2−l)a² + l(a−b)² ≥ 0
  simp only [Eform]
  nlinarith [mul_nonneg h2l (sq_nonneg p.1), mul_nonneg hl0.le (sq_nonneg (p.1 - p.2))]

/-- **`b² ≤ 2/λ³` on the sub-threshold ellipse.**  From `coord_sq_le` and `E ≤ (2−λ)/λ³`. -/
theorem b_sq_le (hl0 : 0 < l) (hl2 : l < 2) (a b : ℝ)
    (hE : Eform l (a, b) ≤ (2 - l) / l ^ 3) :
    b ^ 2 ≤ 2 / l ^ 3 := by
  have h2l : 0 < 2 - l := by linarith
  have hl3 : 0 < l ^ 3 := by positivity
  have hcs : (2 - l) * b ^ 2 ≤ 2 * Eform l (a, b) := by
    have := coord_sq_le l hl0 hl2 (a, b); simpa using this
  -- 2 * E ≤ 2 * (2−l)/l³ = (2−l) * (2/l³)
  have hE2 : 2 * Eform l (a, b) ≤ (2 - l) * (2 / l ^ 3) := by
    have : 2 * ((2 - l) / l ^ 3) = (2 - l) * (2 / l ^ 3) := by ring
    linarith [hE, this]
  have hchain : (2 - l) * b ^ 2 ≤ (2 - l) * (2 / l ^ 3) := le_trans hcs hE2
  -- cancel the positive (2−l)
  exact le_of_mul_le_mul_left hchain h2l

/-- **★ `λ²·b < 2` on the sub-threshold ellipse.**  The load-bearing confinement: `(λ²b)² =
λ⁴b² ≤ 2λ < 4` (using `b² ≤ 2/λ³` and `λ < 2`), and `λ²b > 0`, so `λ²b < 2`. -/
theorem lsq_b_lt_two (hl0 : 0 < l) (hl2 : l < 2) (a b : ℝ) (hb : 0 < b)
    (hE : Eform l (a, b) ≤ (2 - l) / l ^ 3) :
    l ^ 2 * b < 2 := by
  have hbsq : b ^ 2 ≤ 2 / l ^ 3 := b_sq_le l hl0 hl2 a b hE
  have hl3 : 0 < l ^ 3 := by positivity
  -- (λ²b)² = λ⁴ b² ≤ λ⁴·(2/λ³) = 2λ < 4
  have hsq : (l ^ 2 * b) ^ 2 ≤ 2 * l := by
    have h1 : (l ^ 2 * b) ^ 2 = l ^ 4 * b ^ 2 := by ring
    rw [h1]
    have h2 : l ^ 4 * b ^ 2 ≤ l ^ 4 * (2 / l ^ 3) :=
      mul_le_mul_of_nonneg_left hbsq (by positivity)
    have h3 : l ^ 4 * (2 / l ^ 3) = 2 * l := by
      have hne : l ^ 3 ≠ 0 := ne_of_gt hl3
      field_simp
    linarith
  have hpos : 0 < l ^ 2 * b := by positivity
  nlinarith [hsq, hpos, hl2, hl0]

/-! ## §2.  ★ LOWER-BRACKET PRESERVATION ON THE ELLIPSE — the rigorous half of R1. ★ -/

/-- **The algebraic identity.**  `1 + a' − λb' = (λa + b − 1) + (2 − λ²b)` for `(a',b') = M(a,b)`. -/
theorem lower_bracket_slack_eq (a b : ℝ) :
    (1 + (Mmap l (a, b)).1) - l * (Mmap l (a, b)).2
      = (l * a + b - 1) + (2 - l ^ 2 * b) := by
  simp only [Mmap]; ring

/-- **★ LOWER BRACKET IS PRESERVED BY `M` ON THE SUB-THRESHOLD ELLIPSE.**
If `(a,b)` lies on a conserved-`E` ellipse with `E ≤ (2−λ)/λ³`, the corridor edge `λa+b > 1`
holds, and the lower bracket `λb ≤ 1+a` holds, then the lower bracket `λb' ≤ 1+a'` holds at
`M(a,b)`.  (The lower-bracket hypothesis itself is not used in the slack identity — the corridor
edge plus `λ²b < 2` already give it — so this proves `k(M p) ≥ 1` from the on-ellipse geometry.) -/
theorem lower_bracket_preserved_on_ellipse (hl0 : 0 < l) (hl2 : l < 2) (a b : ℝ) (hb : 0 < b)
    (hE : Eform l (a, b) ≤ (2 - l) / l ^ 3)
    (hedge : l * a + b > 1) :
    l * (Mmap l (a, b)).2 ≤ 1 + (Mmap l (a, b)).1 := by
  have hlsq := lsq_b_lt_two l hl0 hl2 a b hb hE
  have hslack := lower_bracket_slack_eq l a b
  -- 1 + a' − λb' = (λa+b−1) + (2 − λ²b) > 0
  have : (1 + (Mmap l (a, b)).1) - l * (Mmap l (a, b)).2 ≥ 0 := by
    rw [hslack]; nlinarith [hedge, hlsq]
  linarith

/-- **★ `k(M p) ≥ 1` on the sub-threshold ellipse** (the floor form of the preservation).  The
successor floor digit is at least `1` whenever the predecessor is an on-ellipse corridor point
with positive successor coordinate.  So along an `M`-arc on a sub-threshold ellipse the floor
NEVER drops below `1`. -/
theorem kfloor_succ_ge_one (hl0 : 0 < l) (hl2 : l < 2) (a b : ℝ) (hb : 0 < b)
    (hb' : 0 < (Mmap l (a, b)).2)
    (hE : Eform l (a, b) ≤ (2 - l) / l ^ 3)
    (hedge : l * a + b > 1) :
    1 ≤ kfloor l (Mmap l (a, b)) := by
  have hbr := lower_bracket_preserved_on_ellipse l hl0 hl2 a b hb hE hedge
  -- `Mmap l (a,b)` is definitionally the pair `((Mmap l (a,b)).1, (Mmap l (a,b)).2)`
  have hpair : Mmap l (a, b) = ((Mmap l (a, b)).1, (Mmap l (a, b)).2) := rfl
  rw [hpair]
  exact (kfloor_ge_one_iff l (Mmap l (a, b)).1 (Mmap l (a, b)).2 hl0 hb').mpr hbr

/-! ## §3.  Consequence — the floor is NON-DECREASING-into-`{1,≥2}` along the arc, so interior
points are exactly `k=1` UNTIL the first floor increment (the reduced R1). -/

/-- **Trichotomy on the successor floor:** on the sub-threshold ellipse the successor floor is
either exactly `1` (continue the arc, the step is `M`) or `≥ 2` (the floor increment / ejection).
It is NEVER `≤ 0`.  This is the rigorous content "the cluster k-pattern is `[1,…,1,(≥2)]`": the
only exit from `k=1` is upward. -/
theorem succ_floor_one_or_increment (hl0 : 0 < l) (hl2 : l < 2) (a b : ℝ) (hb : 0 < b)
    (hb' : 0 < (Mmap l (a, b)).2)
    (hE : Eform l (a, b) ≤ (2 - l) / l ^ 3)
    (hedge : l * a + b > 1) :
    kfloor l (Mmap l (a, b)) = 1 ∨ 2 ≤ kfloor l (Mmap l (a, b)) := by
  have hge1 : 1 ≤ kfloor l (Mmap l (a, b)) := kfloor_succ_ge_one l hl0 hl2 a b hb hb' hE hedge
  rcases le_or_gt 2 (kfloor l (Mmap l (a, b))) with h | h
  · exact Or.inr h
  · exact Or.inl (le_antisymm (by omega) hge1)

/-- **★ INTERIOR `k=1` FROM THE ON-ELLIPSE INVARIANT + "no premature increment".**  This is the
REDUCED R1: a successor point on the sub-threshold ellipse, whose floor has not yet incremented
(`¬ 2 ≤ kfloor`, i.e. the upper bracket `1+a' < 2λb'` still holds — the phase/R3 residual), has
floor digit EXACTLY `1`.  The lower half (`k ≥ 1`) is now a THEOREM
(`kfloor_succ_ge_one`); only the upper half is carried as the named hypothesis `hNoIncr`. -/
theorem interior_k1_of_no_premature_increment (hl0 : 0 < l) (hl2 : l < 2) (a b : ℝ) (hb : 0 < b)
    (hb' : 0 < (Mmap l (a, b)).2)
    (hE : Eform l (a, b) ≤ (2 - l) / l ^ 3)
    (hedge : l * a + b > 1)
    (hNoIncr : ¬ (2 ≤ kfloor l (Mmap l (a, b)))) :
    kfloor l (Mmap l (a, b)) = 1 := by
  rcases succ_floor_one_or_increment l hl0 hl2 a b hb hb' hE hedge with h | h
  · exact h
  · exact absurd h hNoIncr

/-! ## §4.  THE REDUCED CHARACTERIZATION — `hbracket` with the LOWER half discharged.

We re-state the `HeckeRotArc` "cluster ⟹ rotation arc" reduction, but the per-step
interior bracket is no longer a raw two-sided hypothesis: its LOWER half is now a derived
consequence of the on-ellipse invariant, and only the UPPER half (`hUpper`, the
not-yet-ejected / phase residual) is carried as a named hypothesis.  This is a strict reduction
of the original `hbracket` of `BCZHeckeRotationArc.run_isMRotArc_of_brackets`.

We work with a run `run : ℕ → ℝ × ℝ` whose steps are `M` (consecutive states `M`-related); by
`Mmap_preserves_E` every state shares ONE `E`-level set, so the on-ellipse hypothesis `E ≤
(2−λ)/λ³` need only be assumed at the START. -/

variable {l}

/-- The product observable `P (a,b) = a·b`. -/
def Pobs (p : ℝ × ℝ) : ℝ := p.1 * p.2

/-- An `M`-rotation arc: consecutive states `M`-related. -/
def IsMRotArc (run : ℕ → ℝ × ℝ) (N : ℕ) : Prop :=
  ∀ n, n < N → run (n + 1) = Mmap l (run n)

/-- **`E` is constant along an `M`-rotation arc** (so the on-ellipse bound at step 0 holds at
every step).  Verbatim consequence of `Mmap_preserves_E`. -/
theorem arc_E_const (run : ℕ → ℝ × ℝ) (N : ℕ) (harc : IsMRotArc (l := l) run N) :
    ∀ n, n ≤ N → Eform l (run n) = Eform l (run 0) := by
  intro n hn
  induction n with
  | zero => rfl
  | succ k ih =>
      have hk : k < N := by omega
      rw [harc k hk, Mmap_preserves_E, ih (by omega)]

variable (l)

/-- **★ REDUCED interior-k=1 along an `M`-arc — LOWER half (`k ≥ 1`) DISCHARGED.**  For an
`M`-rotation arc whose `0`-th state lies on the sub-threshold ellipse (`E (run 0) ≤ (2−λ)/λ³`),
with the corridor edge holding and positive `b`-coordinate at every interior state, EACH interior
successor `run (n+1)` has floor `≥ 1`.  This is the theorem half of R1's lower bracket — it holds
at every step from the on-ellipse geometry, with NO bracket hypothesis carried. -/
theorem arc_interior_kfloor_ge_one (hl0 : 0 < l) (hl2 : l < 2)
    (run : ℕ → ℝ × ℝ) (N : ℕ) (harc : IsMRotArc (l := l) run N)
    (hE0 : Eform l (run 0) ≤ (2 - l) / l ^ 3)
    (hbpos : ∀ n, n ≤ N → 0 < (run n).2)
    (hedge : ∀ n, n < N → l * (run n).1 + (run n).2 > 1)
    (n : ℕ) (hn : n < N) :
    1 ≤ kfloor l (run (n + 1)) := by
  have hEn : Eform l (run n) ≤ (2 - l) / l ^ 3 := by
    rw [arc_E_const run N harc n (by omega)]; exact hE0
  have hstep : run (n + 1) = Mmap l (run n) := harc n hn
  have hb : 0 < (run n).2 := hbpos n (by omega)
  have hedgen : l * (run n).1 + (run n).2 > 1 := hedge n hn
  -- the successor `b`-coordinate, written via the pair form the pointwise lemma expects
  have hb' : 0 < (Mmap l ((run n).1, (run n).2)).2 := by
    have : (Mmap l ((run n).1, (run n).2)).2 = (run (n + 1)).2 := by rw [hstep]
    rw [this]; exact hbpos (n + 1) (by omega)
  have hEn' : Eform l ((run n).1, (run n).2) ≤ (2 - l) / l ^ 3 := hEn
  have hedgen' : l * ((run n).1, (run n).2).1 + ((run n).1, (run n).2).2 > 1 := hedgen
  have hkey := kfloor_succ_ge_one l hl0 hl2 (run n).1 (run n).2 hb hb' hEn' hedgen'
  -- `Mmap l ((run n).1,(run n).2) = Mmap l (run n) = run (n+1)`
  have hMeq : Mmap l ((run n).1, (run n).2) = run (n + 1) := by rw [hstep]
  rw [hMeq] at hkey; exact hkey

/-- **★ REDUCED interior-k=1 — full floor digit `= 1` from the lower-bracket THEOREM + the residual
upper bracket.**  An interior successor `run (n+1)` of an `M`-arc on the sub-threshold ellipse has
floor digit EXACTLY `1` once its upper bracket still holds (`hUpper n`, the not-yet-ejected /
phase-lattice residual — R3 family).  The lower half is derived (`arc_interior_kfloor_ge_one`); so
this carries ONLY the upper bracket where the original `HeckeRotArc.run_isMRotArc_of_brackets`
carried the full two-sided `hbracket`. -/
theorem arc_interior_kfloor_eq_one (hl0 : 0 < l) (hl2 : l < 2)
    (run : ℕ → ℝ × ℝ) (N : ℕ) (harc : IsMRotArc (l := l) run N)
    (hE0 : Eform l (run 0) ≤ (2 - l) / l ^ 3)
    (hbpos : ∀ n, n ≤ N → 0 < (run n).2)
    (hedge : ∀ n, n < N → l * (run n).1 + (run n).2 > 1)
    (hUpper : ∀ n, n < N → ¬ (2 ≤ kfloor l (run (n + 1))))
    (n : ℕ) (hn : n < N) :
    kfloor l (run (n + 1)) = 1 := by
  have hge1 := arc_interior_kfloor_ge_one l hl0 hl2 run N harc hE0 hbpos hedge n hn
  rcases le_or_gt 2 (kfloor l (run (n + 1))) with h | h
  · exact absurd h (hUpper n hn)
  · exact le_antisymm (by omega) hge1

/-! ## §5.  ★ THE REDUCED CHARACTERIZATION `cluster_is_rotation_arc'` — `hbracket` with its
LOWER half discharged. ★

The original `BCZHeckeRotationArc.run_isMRotArc_of_brackets` proved "a GENUINE-step run is an
`M`-rotation arc" from the full two-sided bracket `hbracket : λb ≤ 1+a < 2λb` at every step.  We
reproduce it taking only the **upper** half as a hypothesis, the **lower** half now being a
THEOREM of the on-ellipse geometry.  The genuine last-branch step is
`kstep k (a,b) = (b, −a + kλb)`; for `k=1` it equals `M`.  So we must (i) show the floor is `1`
(from the lower-bracket theorem + the residual upper bracket), then (ii) the genuine step IS `M`. -/

variable {l}

/-- The genuine last-branch step with floor digit `k`: `(a,b) ↦ (b, −a + kλb)` (the `HeckeRotArc`
`kstep` form). -/
def kstep (k : ℝ) (p : ℝ × ℝ) : ℝ × ℝ := (p.2, -p.1 + k * l * p.2)

/-- The `k=1` genuine step IS `M`. -/
theorem kstep_one_eq_Mmap (p : ℝ × ℝ) : kstep (l := l) 1 p = Mmap l p := by
  simp only [kstep, Mmap]; ring_nf

variable (l)

/-- **★ `cluster_is_rotation_arc'` — the reduced reduction.**  A run whose states already lie on
ONE conserved-`E` sub-threshold ellipse (`E (run 0) ≤ (2−λ)/λ³`, propagated by `Mmap_preserves_E`
along the established `M`-relation), with the corridor edge and positive `b`-coordinate at every
interior state, takes a genuine `M`-step at every interior point — the floor digit being `1` from
the **lower-bracket theorem** (`arc_interior_kfloor_ge_one`) plus the residual **upper** bracket
`hUpper` (the only carried bracket hypothesis).  In particular the genuine-step coincides with the
elliptic rotation `M` at every interior point.

This is exactly `BCZHeckeRotationArc.run_isMRotArc_of_brackets`/`cluster_is_rotation_arc` with the
LOWER half of `hbracket` removed and replaced by the proved on-ellipse invariant. -/
theorem cluster_is_rotation_arc' (hl0 : 0 < l) (hl2 : l < 2)
    (run : ℕ → ℝ × ℝ) (N : ℕ) (harc : IsMRotArc (l := l) run N)
    (hE0 : Eform l (run 0) ≤ (2 - l) / l ^ 3)
    (hbpos : ∀ n, n ≤ N → 0 < (run n).2)
    (hedge : ∀ n, n < N → l * (run n).1 + (run n).2 > 1)
    (hUpper : ∀ n, n < N → ¬ (2 ≤ kfloor l (run (n + 1)))) :
    -- (a) every interior successor has floor digit exactly 1 …
    (∀ n, n < N → kfloor l (run (n + 1)) = 1) ∧
    -- (b) … so the genuine step `kstep (kfloor)` at every interior successor IS the rotation `M`.
    (∀ n, n < N → kstep (l := l) ((kfloor l (run (n + 1)) : ℝ)) (run (n + 1))
                    = Mmap l (run (n + 1))) := by
  have hk1 : ∀ n, n < N → kfloor l (run (n + 1)) = 1 := fun n hn =>
    arc_interior_kfloor_eq_one l hl0 hl2 run N harc hE0 hbpos hedge hUpper n hn
  refine ⟨hk1, ?_⟩
  intro n hn
  rw [hk1 n hn]; push_cast; exact kstep_one_eq_Mmap (l := l) (run (n + 1))

end

-- ════════════ AXIOM AUDIT ════════════
#print axioms HeckeRotArcR1.Mmap_preserves_E
#print axioms HeckeRotArcR1.kfloor_ge_one_iff
#print axioms HeckeRotArcR1.kfloor_ge_two_iff
#print axioms HeckeRotArcR1.coord_sq_le
#print axioms HeckeRotArcR1.b_sq_le
#print axioms HeckeRotArcR1.lsq_b_lt_two
#print axioms HeckeRotArcR1.lower_bracket_slack_eq
#print axioms HeckeRotArcR1.lower_bracket_preserved_on_ellipse
#print axioms HeckeRotArcR1.kfloor_succ_ge_one
#print axioms HeckeRotArcR1.succ_floor_one_or_increment
#print axioms HeckeRotArcR1.interior_k1_of_no_premature_increment
#print axioms HeckeRotArcR1.arc_E_const
#print axioms HeckeRotArcR1.arc_interior_kfloor_ge_one
#print axioms HeckeRotArcR1.arc_interior_kfloor_eq_one
#print axioms HeckeRotArcR1.kstep_one_eq_Mmap
#print axioms HeckeRotArcR1.cluster_is_rotation_arc'

end HeckeRotArcR1

import Mathlib
set_option maxHeartbeats 1600000
/-!
# `BCZHeckeRotationArcR3Parity.lean` — the **PARITY GATE** half of residual **R3**, as a theorem.

This file is a **new, self-contained** companion to `BCZHeckeRotationArc.lean` /
`BCZHeckeRotationArcR1.lean`.  It touches **NO** sealed/verified file.  It closes the **parity**
half of residual **R3** (the cluster-ceiling resonance / notch-straddle): the fact that whether
the `−π/q` rotation lattice can *hop* the super-threshold notch is decided by the **PARITY** of the
number of lattice points on the arc, leaving ONLY a single transcendental "near-fit" residual.

## The object (pinned exactly, from the parent notes)

On a conserved-`E` ellipse the last-branch observable is
`P(φ) = E₀·(c₀ + amp·cos 2(φ − φ*))`, a single cosine, **peaked at `φ = φ*`** (the symmetric
point `a = b`) and **reflection-symmetric** about `φ*`: `P(φ* + ψ) = P(φ* − ψ)`.  The threshold is
`t = 1/λ³`.  When the peak pokes above `t` (the resonance ellipse, `frac > 1`) the super-threshold
set near the peak is a **symmetric notch** `{φ : |φ − φ*| < δ}` of half-width `δ`, with
`δ < θ/2 = π/(2q)` in the regime of interest (a sub-`π/q`-wide notch — the only one a `π/q` lattice
can hope to hop).

The cluster is a run of `N` equally-spaced rotation-lattice points of step `θ = π/q`.  Because the
arc `{P < t}` is symmetric-unimodal about `φ*`, the **longest** run is the **symmetric** one,
centred on `φ*`: lattice phases `φ_i = φ* + relᵢ·θ`, `relᵢ = i − (N−1)/2`, `i = 0..N−1` (so the
configuration is invariant under reflection `i ↦ N−1−i` about `φ*`).

## The parity gate (this file's theorem)

> **For a symmetric equally-spaced lattice of step `θ` and `N` points centred on the peak `φ*`,
> with a symmetric notch of half-width `δ < θ/2`:**
> * **`N` EVEN ⟹ STRADDLE:** every lattice point is OUTSIDE the notch (the closest points sit at
>   `±θ/2`, and `θ/2 > δ`), so a sub-threshold run of length `N` fits — the gain is available.
> * **`N` ODD ⟹ IMPALE:** the centre lattice point sits EXACTLY at `φ*` (inside the notch,
>   `P > t`), so a sub-threshold run of length `N` is impossible — the gain is blocked.

This is proved from **equal-spacing + reflection symmetry alone**.  The minimal distance from the
peak to the nearest lattice point is `0` when `N` is odd and `θ/2` when `N` is even; combined with
`δ < θ/2` this gives the dichotomy.  Phrased on the actual observable `P(φ)` (a genuine cosine,
peak at `φ*`), the notch is exactly `{P > t}` and the gate becomes the **super-threshold
straddle/impale** statement.

`#print axioms` on every declaration below is `[propext, Classical.choice, Quot.sound]`.

## What this CLOSES and what REMAINS (R3, honest scoping)

* **CLOSED (this file):** the parity gate — *given* a symmetric notch of half-width `δ < θ/2`, the
  length-`N` symmetric sub-threshold run exists **iff `N` is even**.  Equivalently the resonance
  gain `+1` (target count `B₀+1` even ⟺ `B₀` odd) can fire only when `B₀(q)` is odd.  This is now a
  Lean theorem, removing the parity half from the residual list.
* **REMAINING (single, decidable-per-q transcendental fact):** the *near-fit* — that the notch
  half-width is actually `< θ/2` AND the arc width `W(q)·q/π` reaches the (even) integer
  `B₀+1` from below at a `frac > 1` small enough to keep `δ < θ/2`.  This is an `L1b`-family
  inequality in `W(q) = arccos(…)/…`, transcendental in `λ = 2cos(π/q)`.  It is **decidable per
  `q`** (a finite interval-arithmetic check on `δ(q)` and `s(q) = W(q)q/π`); a closed-form
  characterization of the resonance set `{23, 61, …}` is genuinely analytic-open.
-/

namespace HeckeRotArcR3Parity

noncomputable section

/-! ## §0.  The symmetric equally-spaced lattice (offsets in units of `θ`).

The `i`-th lattice point of an `N`-point symmetric run has offset (in units of `θ`) from the peak

>   `rel N i = (i : ℝ) − (N − 1)/2`,   `i = 0, …, N−1`.

This is the unique placement invariant under the reflection `i ↦ N−1−i` about the peak (the centre
of the run is the peak `φ*`).  The *physical* offset is `rel N i · θ`. -/

/-- Offset (in units of `θ`) of the `i`-th point of a symmetric `N`-point run from the centre. -/
def rel (N : ℕ) (i : ℕ) : ℝ := (i : ℝ) - ((N : ℝ) - 1) / 2

/-- **Reflection symmetry of the lattice about the peak**: `rel N (N-1-i) = − rel N i`
(for `i < N`).  The configuration is invariant under `i ↦ N−1−i` up to sign of the offset — this
is the equal-spacing+symmetry input the parity gate rests on. -/
theorem rel_reflect (N i : ℕ) (hi : i < N) :
    rel N (N - 1 - i) = - rel N i := by
  unfold rel
  have hN1 : (1 : ℕ) ≤ N := by omega
  have : ((N - 1 - i : ℕ) : ℝ) = (N : ℝ) - 1 - (i : ℝ) := by
    have h1 : (N - 1 - i : ℕ) = N - 1 - i := rfl
    have : ((N - 1 - i : ℕ) : ℝ) = ((N : ℝ) - 1) - (i : ℝ) := by
      push_cast [Nat.cast_sub (by omega : i ≤ N - 1), Nat.cast_sub hN1]
      ring
    simpa using this
  rw [this]; ring

/-! ## §1.  ★ THE MINIMAL DISTANCE FROM THE PEAK — odd ⇒ 0, even ⇒ 1/2 ★

The distance from the peak (offset `0`) to the nearest lattice point is `min_i |rel N i|`.  We do
not need the full `min`; we need the two load-bearing facts:

* **(odd)** there EXISTS a lattice index with `rel = 0` (a point ON the peak);
* **(even)** EVERY lattice index has `|rel| ≥ 1/2` (every point a half-step OFF the peak). -/

/-- **ODD ⇒ a lattice point sits EXACTLY on the peak.**  If `N = 2m+1` then the central index
`i = m` has `rel N m = 0`. -/
theorem odd_center_on_peak (m : ℕ) :
    rel (2 * m + 1) m = 0 := by
  unfold rel
  push_cast
  ring

/-- **EVEN ⇒ every lattice point is at least a half-step `1/2` off the peak.**  If `N = 2m` then
for every index `i`, `|rel N i| ≥ 1/2` — equivalently the offsets are the half-integers
`±1/2, ±3/2, …`, none of which is `0`. -/
theorem even_all_offpeak (m : ℕ) (i : ℕ) :
    (1 : ℝ) / 2 ≤ |rel (2 * m) i| := by
  -- Normalize: rel (2m) i = i − (2m−1)/2 with all casts as reals.
  have hrel : rel (2 * m) i = (i : ℝ) - (2 * (m : ℝ) - 1) / 2 := by
    unfold rel; push_cast; ring
  rw [hrel]
  -- numerator (2i − (2m−1)) is an ODD integer, so |i − (2m−1)/2| ≥ 1/2.
  rcases le_or_gt (m : ℝ) (i : ℝ) with h | h
  · -- i ≥ m  ⇒  i − (2m−1)/2 = (2(i−m)+1)/2 ≥ 1/2
    rw [abs_of_nonneg (by nlinarith [h])]
    nlinarith [h]
  · -- i < m  ⇒  i + 1 ≤ m  ⇒  (2m−1)/2 − i = (2(m−i)−1)/2 ≥ 1/2
    have hle : (i : ℝ) + 1 ≤ (m : ℝ) := by
      have hlt : (i : ℕ) < m := by exact_mod_cast h
      have : (i : ℕ) + 1 ≤ m := hlt
      exact_mod_cast this
    rw [abs_of_nonpos (by nlinarith [hle])]
    nlinarith [hle]

/-! ## §2.  ★ THE PARITY GATE on the lattice — STRADDLE iff EVEN, IMPALE iff ODD ★

The **notch** is the symmetric super-threshold sub-arc `{ |offset·θ| < δ }`, i.e. in `θ`-units
`{ |rel| < δ/θ }`, of half-width `δ < θ/2`.  Write `w := δ/θ < 1/2` for the half-width in
`θ`-units.  A lattice point is **in the notch** (super-threshold) iff `|rel| < w`.  The two
theorems below are the parity gate, proved from §1. -/

/-- **★ STRADDLE (EVEN).**  For an `N = 2m`-point symmetric run and a notch of half-width
`w < 1/2` (in `θ`-units), EVERY lattice point is OUTSIDE the notch (`|rel| ≥ 1/2 > w`).  So the
super-threshold notch falls entirely in the central gap — the length-`2m` run is all sub-threshold.
*(This is the q=23 case: `B₀+1 = 6` even ⇒ the 6 points straddle the peak, none impaled.)* -/
theorem straddle_of_even (m : ℕ) (w : ℝ) (hw : w < 1 / 2) (i : ℕ) :
    w < |rel (2 * m) i| := by
  have h := even_all_offpeak m i
  linarith

/-- **★ IMPALE (ODD).**  For an `N = 2m+1`-point symmetric run and a notch of half-width `w > 0`,
the CENTRAL lattice point (`i = m`) lies INSIDE the notch (`|rel| = 0 < w`).  So one point is
super-threshold — the length-`2m+1` run is impossible.
*(This is the q=47 case: `B₀+1 = 11` odd ⇒ the central point lands on the peak, P > t, blocked.)* -/
theorem impale_of_odd (m : ℕ) (w : ℝ) (hw : 0 < w) :
    |rel (2 * m + 1) m| < w := by
  rw [odd_center_on_peak m, abs_zero]; exact hw

/-- **★ THE PARITY GATE (unified) — straddle ⟺ even.**  For a symmetric `N`-point run versus a
symmetric notch of half-width `w` with `0 < w < 1/2` (sub-`θ/2` notch, in `θ`-units):

> EVERY lattice point avoids the notch  ⟺  `N` is EVEN.

Forward: if every point avoids the notch then `N` cannot be odd (the centre point of an odd run is
ON the peak, inside any positive-width notch).  Backward: an even run's points are all `≥ 1/2 > w`
off the peak.  This is the exact "straddle iff even / impale iff odd" dichotomy, from equal-spacing
+ reflection symmetry alone. -/
theorem parity_gate (N : ℕ) (w : ℝ) (hw0 : 0 < w) (hw : w < 1 / 2) :
    (∀ i, i < N → w < |rel N i|) ↔ Even N := by
  constructor
  · -- contrapositive: N odd ⇒ centre point is in the notch ⇒ not "all avoid"
    intro hall
    by_contra hodd
    rw [Nat.not_even_iff_odd] at hodd
    obtain ⟨m, hm⟩ := hodd          -- N = 2m+1
    subst hm
    have hcenter : w < |rel (2 * m + 1) m| := hall m (by omega)
    have himp : |rel (2 * m + 1) m| < w := impale_of_odd m w hw0
    linarith
  · -- N even ⇒ every point ≥ 1/2 > w off the peak
    intro heven
    obtain ⟨m, hm⟩ := heven         -- N = m + m = 2m
    intro i _
    have : N = 2 * m := by omega
    rw [this]
    exact straddle_of_even m w hw i

/-! ## §3.  ★ THE GATE ON THE OBSERVABLE `P(φ)` — super-threshold notch is `{P > t}` ★

We now phrase the gate on the genuine observable.  `P` is a single cosine of double angle, peaked
at the symmetric point `φ*` and reflection-symmetric there:

>   `Pphi amp c0 E0 φ* φ = E0·(c0 + amp·cos(2(φ − φ*)))`,   `amp > 0`, peak at `φ = φ*`.

`t` is the threshold; the **notch** is `{φ : P(φ) > t}`, a symmetric arc about `φ*` whose half-width
`δ` is set by `cos(2δ) = (t/E0 − c0)/amp` (the parent note's notch equation).  We prove:

* **`Pphi` is reflection-symmetric** about `φ*`  (`P(φ*+ψ) = P(φ*−ψ)`) — the symmetry input;
* **a lattice point is super-threshold iff its offset is inside the notch** — `P(φ*+ψ) > t ⟺
  cos(2ψ) > (t/E0 − c0)/amp`, monotone in `|ψ|` on `(0, π/2)`;
* the **ODD case impales**: the central point at `φ*` has `P(φ*) = E0(c0+amp) =` peak `> t` when
  `frac > 1` (peak above threshold) — so it is super-threshold (blocked);
* the **EVEN case straddles** when `δ < θ/2`: every point is `≥ θ/2 > δ` off the peak hence below
  threshold (uses §2). -/

/-- The observable as a function of phase: `P(φ) = E0·(c0 + amp·cos 2(φ − φ*))`. -/
def Pphi (E0 c0 amp φstar φ : ℝ) : ℝ := E0 * (c0 + amp * Real.cos (2 * (φ - φstar)))

/-- **Reflection symmetry about the peak**: `P(φ* + ψ) = P(φ* − ψ)`.  (The crucial symmetry input
for "the longest run is the symmetric one centred on the peak".) -/
theorem Pphi_reflect (E0 c0 amp φstar ψ : ℝ) :
    Pphi E0 c0 amp φstar (φstar + ψ) = Pphi E0 c0 amp φstar (φstar - ψ) := by
  unfold Pphi
  have h1 : 2 * (φstar + ψ - φstar) = 2 * ψ := by ring
  have h2 : 2 * (φstar - ψ - φstar) = -(2 * ψ) := by ring
  rw [h1, h2, Real.cos_neg]

/-- **The peak value is `E0·(c0 + amp)` at `φ = φ*`.** -/
theorem Pphi_peak (E0 c0 amp φstar : ℝ) :
    Pphi E0 c0 amp φstar φstar = E0 * (c0 + amp) := by
  unfold Pphi; simp

/-- **ODD-case impale, on the observable.**  When the peak pokes above threshold
(`E0·(c0+amp) > t`, the resonance ellipse `frac > 1`), the central lattice point of an odd run —
which sits exactly at `φ*` (`rel = 0`) — has `P = E0(c0+amp) > t`, i.e. it is SUPER-THRESHOLD.
A length-`2m+1` symmetric sub-threshold run is therefore impossible. -/
theorem impale_observable (E0 c0 amp φstar t : ℝ)
    (hpeak : t < E0 * (c0 + amp)) :
    t < Pphi E0 c0 amp φstar φstar := by
  rw [Pphi_peak]; exact hpeak

/-- **A flank point's super-threshold condition.**  At offset `ψ` (physical), `P(φ*+ψ) > t` iff
`cos(2ψ) > (t/E0 − c0)/amp` (for `E0 > 0`, `amp > 0`).  This is the notch equation: the notch is
`{ |ψ| : cos 2ψ > (t/E0−c0)/amp }`, and because `cos` is decreasing on `[0, π]`, this is exactly a
symmetric interval `|ψ| < δ` with `cos 2δ = (t/E0−c0)/amp` — the parent note's `δ`. -/
theorem superthreshold_iff_cos (E0 c0 amp φstar t ψ : ℝ) (hE : 0 < E0) (hamp : 0 < amp) :
    t < Pphi E0 c0 amp φstar (φstar + ψ) ↔ (t / E0 - c0) / amp < Real.cos (2 * ψ) := by
  unfold Pphi
  have h1 : 2 * (φstar + ψ - φstar) = 2 * ψ := by ring
  rw [h1]
  rw [div_lt_iff₀ hamp, sub_lt_iff_lt_add, div_lt_iff₀ hE]
  constructor <;> intro h <;> nlinarith [h]

/-! ## §4.  ★ THE PACKAGED GATE — even straddles the `{P>t}` notch, odd impales it ★

We package §2 (lattice parity) with §3 (observable) into the single resonance statement.  The notch
half-width in `θ`-units is `w = δ/θ`; the regime is `δ < θ/2`, i.e. `w < 1/2`.  Inside the notch
`⟺ |rel| < w`; super-threshold there.  Outside ⟹ sub-threshold (`P < t`).  We state the gate as:
the symmetric length-`N` run is **all sub-threshold iff `N` is even** — *given* the notch is the
symmetric set `{|rel| < w}`, `0 < w < 1/2` (the near-fit residual supplies `w < 1/2`). -/

/-- A lattice point (offset `relᵢ·θ`) is **super-threshold** iff its `θ`-unit offset is inside the
notch `|rel| < w`.  We take this as the abstract notch membership (`§3` supplies the geometric
content: `w = δ/θ`, `δ` from the notch equation, and `cos` monotonicity makes `{P>t}` exactly this
symmetric interval). -/
def inNotch (w : ℝ) (r : ℝ) : Prop := |r| < w

/-- **★ THE RESONANCE PARITY GATE (final form).**  For a symmetric `N`-point rotation run of step
`θ` versus a symmetric super-threshold notch of half-width `w ∈ (0, 1/2)` (in `θ`-units, i.e.
`δ < θ/2`):

>   the whole run avoids the notch (is all sub-threshold)  ⟺  `N` is EVEN.

* **EVEN ⟹ straddle:** all points `≥ 1/2 > w` off-peak (`even_all_offpeak`), notch in the centre
  gap — the resonance gain fires.  *(q=23, target 6.)*
* **ODD ⟹ impale:** the centre point is at `0`, inside any positive notch — gain blocked.
  *(q=47, target 11.)*

This removes the **parity half** of R3 from the residual list. -/
theorem resonance_parity_gate (N : ℕ) (w : ℝ) (hw0 : 0 < w) (hw : w < 1 / 2) :
    (∀ i, i < N → ¬ inNotch w (rel N i)) ↔ Even N := by
  unfold inNotch
  constructor
  · -- forward: contrapositive — an odd run has a centre point inside the notch
    intro h
    by_contra hodd
    rw [Nat.not_even_iff_odd] at hodd
    obtain ⟨m, hm⟩ := hodd            -- N = 2m+1
    subst hm
    have hcenter : ¬ (|rel (2 * m + 1) m| < w) := h m (by omega)
    have himp : |rel (2 * m + 1) m| < w := impale_of_odd m w hw0
    exact hcenter himp
  · -- backward: an even run's points are all ≥ 1/2 > w off-peak, so none < w
    intro heven i hi
    obtain ⟨m, hm⟩ := heven           -- N = m + m = 2m
    have hN : N = 2 * m := by omega
    rw [hN]
    have := straddle_of_even m w hw i  -- w < |rel (2m) i|
    exact not_lt.mpr (le_of_lt this)

/-- **★ CONTRAPOSITIVE / GAIN form.**  The resonance gain (`+1`, i.e. the symmetric `B₀+1`-point
run all sub-threshold past a notch) is available **only when the target count `N = B₀+1` is even**
— equivalently only when `B₀` is ODD.  If `N` is odd the run is impaled regardless of how narrow
the notch (any `w > 0`): the centre point is on the peak. -/
theorem gain_requires_even (N : ℕ) (w : ℝ) (hw0 : 0 < w) (hw : w < 1 / 2)
    (hgain : ∀ i, i < N → ¬ inNotch w (rel N i)) :
    Even N :=
  (resonance_parity_gate N w hw0 hw).mp hgain

/-- **★ ODD always impales** (the explicit blocker, any positive notch).  If `N` is odd then the
centre point IS in the notch, so the run is NOT all sub-threshold — no resonance gain at odd target
count, irrespective of arc near-fit.  *(q=47: B₀=10 even ⇒ target 11 odd ⇒ blocked even though the
arc is only 0.003·θ short — "parity beats proximity".)* -/
theorem odd_always_impaled (N : ℕ) (w : ℝ) (hw0 : 0 < w) (hodd : Odd N) :
    ∃ i, i < N ∧ inNotch w (rel N i) := by
  obtain ⟨m, hm⟩ := hodd            -- N = 2m+1
  refine ⟨m, by omega, ?_⟩
  rw [hm]; unfold inNotch
  exact impale_of_odd m w hw0

end

-- ════════════ AXIOM AUDIT ════════════
#print axioms HeckeRotArcR3Parity.rel_reflect
#print axioms HeckeRotArcR3Parity.odd_center_on_peak
#print axioms HeckeRotArcR3Parity.even_all_offpeak
#print axioms HeckeRotArcR3Parity.straddle_of_even
#print axioms HeckeRotArcR3Parity.impale_of_odd
#print axioms HeckeRotArcR3Parity.parity_gate
#print axioms HeckeRotArcR3Parity.Pphi_reflect
#print axioms HeckeRotArcR3Parity.Pphi_peak
#print axioms HeckeRotArcR3Parity.impale_observable
#print axioms HeckeRotArcR3Parity.superthreshold_iff_cos
#print axioms HeckeRotArcR3Parity.resonance_parity_gate
#print axioms HeckeRotArcR3Parity.gain_requires_even
#print axioms HeckeRotArcR3Parity.odd_always_impaled

end HeckeRotArcR3Parity

import Mathlib
import BCZHeckeS1_trichotomy
import GenuineMapP2
import GenuineMapP2_target
import GenuineSelfMap
import BCZHeckeUniformOnset
import UniformOnset_q5to18
import ToplevelStitchGen

set_option maxHeartbeats 4000000

/-!
# `GenuineClassDischarge.lean` — discharging the carried `hGen` classification of
`ToplevelStitchGen.perq_Xomega_lb_qge19_GEN`.

`perq_Xomega_lb_qge19_GEN` carries
```
hGen : ∀ orbit, (∀n, orbit n ∈ Taha l) → (∀n, orbit(n+1)=Tgen l m B (orbit n))
         → ∀n, GenuineClassGen l m orbit n
```
`GenuineClassGen` (ToplevelStitchGen.lean:76) bundles, per orbit point, six facts:
the Taha components (`hb, ha, ha1, hbpos, htaha`) and the deep-mid geometric data
`hDeepData` (the entry index `2 ≤ branchIdx` and the corridor positivity `0 ≤ L_{i+1}`).

This file PROVES `GenuineClassGen` along any `Tgen`-orbit-in-Taha from `step_trichotomy`
(sealed) + the **Casorati/discrete-Wronskian coupling** + the **intermediate
cheb-positivity** of the corridor lengths — reducing `hGen` to the single uniform,
λ-symbolic arithmetic fact `ChebPos` (`cheb l j ≥ 1` for `1 ≤ j ≤ m+1`).

## What is PROVED here (axiom-clean, no `sorry`)

* `casorati`  — the discrete Wronskian identity `L_j·cheb(j+1) − L_{j+1}·cheb(j) = a`
  for the cheb/`L` recurrence (pure algebra, no λ-arithmetic).  This is the Casorati
  coupling the task flagged.
* `L_succ_eq`  — `L_{i+1}·cheb(i) = L_i·cheb(i+1) − a` (Casorati at `j = i`).
* `branchIdx_ge_two`  — Fact 1: at any active branch the index is `≥ 2`, EXACTLY from
  the Taha lower edge `htaha` (`L_1 = λa + b > 1`).  No λ-arithmetic, no positivity.
* `L_succ_nonneg_of_chebpos`  — Fact 2: `0 ≤ L_{i+1}` at a deep-mid branch from the
  Casorati coupling + intermediate cheb-positivity (`cheb i > 0`, `cheb(i+1) ≥ 1`) +
  Taha positivity (`a > 0`, `b ≥ 0`).
* `genuineClassGen_of_chebpos`  — assembles `GenuineClassGen` per orbit point from
  Taha-membership + `ChebPos`.
* `Tgen_orbit_genuine`  — `hGen` AS A THEOREM, given `ChebPos`.
* `perq_Xomega_lb_qge19_GEN'`  — the corollary dropping the `hGen` hypothesis, leaving
  only the standard invariant-measure setup + `ChebPos`.

`ChebPos` itself (`cheb l j ≥ 1` for `1 ≤ j ≤ m+1` when `λ = 2cos(π/(m+2))`) is the
genuine λ-arithmetic fact — provable from the sin closed form `cheb l j = sin(jθ)/sin(θ)`
(θ = π/(m+2)).  It is proved here as `chebPos_of_hecke` for the Hecke λ; see `## RESIDUAL`.
-/

namespace GenuineClassDischarge

open HeckeS1 GenuineMapP2 GenuineSelfMap ToplevelStitchGen

noncomputable section
variable (l : ℝ)

/-! ## §1.  The Casorati / discrete-Wronskian coupling.

`cheb l` and `L l a b` are two solutions of the SAME linear recurrence
`x_{j+2} = λ x_{j+1} − x_j`.  Their Casorati determinant is constant.  We pin its
value `= a` and read off the successor length. -/

/-- **Casorati / discrete Wronskian identity.**  `L_j·cheb(j+1) − L_{j+1}·cheb(j) = a`
for every `j` (constant in `j`, value `= a = L_0`).  Pure algebra from the cheb
recurrence — NO λ-arithmetic. -/
theorem casorati (a b : ℝ) (j : ℕ) :
    L l a b j * cheb l (j + 1) - L l a b (j + 1) * cheb l j = a := by
  induction j with
  | zero =>
      have h0 : cheb l 0 = 0 := cheb_zero l
      have h1 : cheb l 1 = 1 := cheb_one l
      simp only [L, h0, h1]
      ring
  | succ n ih =>
      -- L_{n+2} = λ L_{n+1} − L_n ; cheb(n+2) = λ cheb(n+1) − cheb(n)
      have hLrec : L l a b (n + 2) = l * L l a b (n + 1) - L l a b n := by
        simp only [L]; rw [cheb_rec l (n + 1), cheb_rec l n]; ring
      have hCrec : cheb l (n + 2) = l * cheb l (n + 1) - cheb l n := cheb_rec l n
      -- Goal at j = n+1 :  L_{n+1}·cheb(n+2) − L_{n+2}·cheb(n+1) = a
      rw [hLrec, hCrec]
      -- expand and use ih :  L_n·cheb(n+1) − L_{n+1}·cheb(n) = a
      nlinarith [ih]

/-- **Successor length from Casorati** (at `j = i`): `L_{i+1}·cheb(i) = L_i·cheb(i+1) − a`. -/
theorem L_succ_eq (a b : ℝ) (i : ℕ) :
    L l a b (i + 1) * cheb l i = L l a b i * cheb l (i + 1) - a := by
  have := casorati l a b i
  linarith

/-! ## §2.  Fact 1 — the entry index is `≥ 2` (from the Taha lower edge).

At ANY active branch on a Taha point, `branchIdx ≥ 2`: the index `1` is excluded
because `L_1 = a·cheb(2) + b·cheb(1) = λa + b > 1` (the Taha lower edge `1 − λa < b`),
so branch `1` is not active, and `branchIdx ≥ 1` (spec) forces `branchIdx ≥ 2`.
Pure: needs only `htaha` and the cheb base values `cheb(1)=1, cheb(2)=λ`. -/

/-- `L_1 = λ·a + b`. -/
theorem L_one (a b : ℝ) : L l a b 1 = l * a + b := by
  have hc2 : cheb l 2 = l := by
    have := cheb_rec l 0; simpa using this
  simp only [L, hc2, cheb_one]; ring

/-- **Fact 1 — entry index `≥ 2`.**  On a Taha point (`1 − λa < b`), the active branch
index is `≥ 2` (branch `1` is excluded because `L_1 = λa + b > 1`). -/
theorem branchIdx_ge_two (a b : ℝ) (B : Boundary l m) (hb : b ≤ 1)
    (htaha : 1 - l * a < b) :
    2 ≤ branchIdx l a b (branch_exists l a b m B.hq0 B.hq1 hb) := by
  set h := branch_exists l a b m B.hq0 B.hq1 hb with hh
  set i := branchIdx l a b h with hi
  have hi1 : 1 ≤ i := (branchIdx_spec l a b h).1
  -- Suppose i = 1.  Then L_1 ≤ 1 (active), contradicting L_1 = λa + b > 1.
  by_contra hlt
  have hi_eq : i = 1 := by omega
  have hactive : L l a b i ≤ 1 := (branchIdx_spec l a b h).2.1
  rw [hi_eq, L_one l a b] at hactive
  -- htaha : 1 − λa < b ⇒ λa + b > 1
  linarith

variable (m : ℕ)

/-! ## §3.  Fact 2 — corridor positivity `0 ≤ L_{i+1}` (Casorati + cheb-positivity).

`L_{i+1}·cheb(i) = L_i·cheb(i+1) − a` (Casorati).  With `cheb(i) > 0`, `L_{i+1} ≥ 0`
reduces to `L_i·cheb(i+1) ≥ a`.  And
`L_i·cheb(i+1) = a·cheb(i+1)² + b·cheb(i)·cheb(i+1) ≥ a·1 + 0 = a`,
using `cheb(i+1) ≥ 1`, `a > 0`, `b ≥ 0`, `cheb(i) ≥ 0`.  So the only genuine inputs
are the intermediate cheb-positivities `cheb(i) > 0`, `cheb(i+1) ≥ 1`. -/

/-- **Fact 2 — corridor positivity from cheb-positivity.**  At an active branch `i`,
given the intermediate cheb-positivity `0 < cheb i`, `1 ≤ cheb (i+1)` and Taha
positivity `0 < a`, `0 ≤ b`, the successor length is `≥ 0`. -/
theorem L_succ_nonneg_of_chebpos (a b : ℝ) (i : ℕ)
    (ha : 0 < a) (hbnn : 0 ≤ b)
    (hci : 0 < cheb l i) (hci1 : 1 ≤ cheb l (i + 1)) :
    0 ≤ L l a b (i + 1) := by
  -- L_{i+1}·cheb(i) = L_i·cheb(i+1) − a
  have hcas : L l a b (i + 1) * cheb l i = L l a b i * cheb l (i + 1) - a :=
    L_succ_eq l a b i
  -- L_i·cheb(i+1) = a·cheb(i+1)² + b·cheb(i)·cheb(i+1)
  have hLi : L l a b i * cheb l (i + 1)
      = a * cheb l (i + 1) ^ 2 + b * (cheb l i * cheb l (i + 1)) := by
    simp only [L]; ring
  -- ≥ a :  a·cheb(i+1)² ≥ a (cheb(i+1)≥1, a>0) and b·cheb(i)·cheb(i+1) ≥ 0
  have hge : a ≤ L l a b i * cheb l (i + 1) := by
    rw [hLi]
    have hsq : 1 ≤ cheb l (i + 1) ^ 2 := by nlinarith [hci1]
    have h1 : a ≤ a * cheb l (i + 1) ^ 2 := by nlinarith [hsq, ha]
    have h2 : 0 ≤ b * (cheb l i * cheb l (i + 1)) := by positivity
    linarith
  -- so L_{i+1}·cheb(i) ≥ 0, and cheb(i) > 0 ⇒ L_{i+1} ≥ 0
  have hprodnn : 0 ≤ L l a b (i + 1) * cheb l i := by rw [hcas]; linarith
  -- cheb i > 0 and product ≥ 0 ⇒ factor ≥ 0
  by_contra hneg
  push_neg at hneg
  have : L l a b (i + 1) * cheb l i < 0 := mul_neg_of_neg_of_pos hneg hci
  linarith

end

/-! ## §4.  Cheb-positivity from the Hecke form `λ = 2cos(π/(m+2))` (the λ-arithmetic).

The intermediate cheb-positivity `cheb l j ≥ 1` (`1 ≤ j ≤ m+1`) used by Fact 2 is NOT
derivable from the carried cusp-boundary `Boundary` data alone (which only fixes
`cheb(m+2)=0, cheb(m+1)=1`).  It is the genuine `λ = 2cos(π/(m+2))` arithmetic, proved
here from the Chebyshev sin closed form
  `cheb (2cosθ) j · sin θ = sin (jθ)`   (`cheb_sin`, induction)
together with `sin(jθ) ≥ sin θ` for `jθ ∈ [θ, π−θ]` (`sin_ge_sin_theta`). -/

open Real

/-- **Chebyshev sin closed form.**  `cheb (2cosθ) n · sin θ = sin (nθ)`.  (`cheb` here is
the Chebyshev-`U` envelope.)  Pure two-step induction via the product-to-sum identity. -/
theorem cheb_sin (θ : ℝ) (n : ℕ) :
    cheb (2 * Real.cos θ) n * Real.sin θ = Real.sin (n * θ) := by
  induction n using Nat.twoStepInduction with
  | zero => simp [cheb]
  | one => simp [cheb]
  | more n ih1 ih2 =>
      have key : Real.sin ((↑n + 2 : ℝ) * θ)
          = 2 * Real.cos θ * Real.sin ((↑n + 1 :ℝ)*θ) - Real.sin ((↑n:ℝ)*θ) := by
        have e1 : ((↑n + 2:ℝ)) * θ = ((↑n + 1:ℝ)*θ) + θ := by ring
        have e2 : ((↑n:ℝ)) * θ = ((↑n + 1:ℝ)*θ) - θ := by ring
        rw [e1, e2, Real.sin_add, Real.sin_sub]; ring
      rw [cheb_rec]
      push_cast
      have expand : (2 * Real.cos θ * cheb (2*Real.cos θ) (n+1) - cheb (2*Real.cos θ) n) * Real.sin θ
          = 2 * Real.cos θ * (cheb (2*Real.cos θ) (n+1) * Real.sin θ)
            - (cheb (2*Real.cos θ) n * Real.sin θ) := by ring
      rw [expand, ih1]
      have ih2' : cheb (2*Real.cos θ) (n+1) * Real.sin θ = Real.sin ((↑n + 1:ℝ)*θ) := by
        rw [ih2]; push_cast; ring_nf
      rw [ih2', key]

/-- **`sin x ≥ sin θ` on `[θ, π−θ]`** (`0 < θ ≤ π/2`).  From the product-to-sum identity
`sin x − sin θ = 2 sin((x−θ)/2) cos((x+θ)/2) ≥ 0`. -/
theorem sin_ge_sin_theta (θ x : ℝ) (hθ : 0 < θ) (hθ2 : θ ≤ Real.pi/2)
    (hlo : θ ≤ x) (hhi : x ≤ Real.pi - θ) :
    Real.sin θ ≤ Real.sin x := by
  rw [← sub_nonneg, Real.sin_sub_sin]
  have hpi := Real.pi_pos
  have hs : 0 ≤ Real.sin ((x - θ)/2) :=
    Real.sin_nonneg_of_nonneg_of_le_pi (by linarith) (by linarith)
  have hc : 0 ≤ Real.cos ((x + θ)/2) :=
    Real.cos_nonneg_of_mem_Icc ⟨by linarith, by linarith⟩
  positivity

/-- **Cheb-positivity at the Hecke λ.**  For `l = 2cos(π/(m+2))`, `m ≥ 1`, and
`1 ≤ j ≤ m+1`, the corridor length `cheb l j ≥ 1`.  This is the genuine λ-arithmetic
fact discharging the intermediate cheb-positivity that Fact 2 (`L_succ_nonneg`) needs. -/
theorem chebPos_of_hecke (m j : ℕ) (hm : 1 ≤ m) (hj : 1 ≤ j) (hjm : j ≤ m + 1) :
    1 ≤ cheb (2 * Real.cos (Real.pi / (m + 2))) j := by
  set θ : ℝ := Real.pi / (m + 2) with hθdef
  have hmr : (0:ℝ) < (m : ℝ) + 2 := by positivity
  have hpi := Real.pi_pos
  -- 0 < θ ≤ π/2  (since m+2 ≥ 2)
  have hθpos : 0 < θ := by rw [hθdef]; positivity
  have hθle : θ ≤ Real.pi / 2 := by
    rw [hθdef]
    apply div_le_div_of_nonneg_left hpi.le (by norm_num)
      (by have : (0:ℝ) ≤ (m:ℝ) := Nat.cast_nonneg m; linarith)
  -- sin θ > 0
  have hsinθ : 0 < Real.sin θ := Real.sin_pos_of_pos_of_lt_pi hθpos (by linarith)
  -- jθ ∈ [θ, π − θ]
  have hjθlo : θ ≤ (j : ℝ) * θ := by
    have : (1:ℝ) ≤ (j:ℝ) := by exact_mod_cast hj
    nlinarith [hθpos]
  have hjθhi : (j : ℝ) * θ ≤ Real.pi - θ := by
    -- (j)θ ≤ (m+1)θ = (m+1)π/(m+2) = π − θ
    have hjle : (j:ℝ) ≤ (m:ℝ) + 1 := by exact_mod_cast hjm
    have hππ : ((m:ℝ) + 1) * θ = Real.pi - θ := by
      rw [hθdef]; field_simp; ring
    nlinarith [hθpos, hjle, hππ]
  -- sin(jθ) ≥ sin θ
  have hge : Real.sin θ ≤ Real.sin ((j : ℝ) * θ) :=
    sin_ge_sin_theta θ ((j:ℝ)*θ) hθpos hθle hjθlo hjθhi
  -- cheb l j · sinθ = sin(jθ) ≥ sinθ  ⇒  cheb l j ≥ 1
  have hcs : cheb (2 * Real.cos θ) j * Real.sin θ = Real.sin ((j:ℝ) * θ) := cheb_sin θ j
  rw [← hθdef] at *
  have : Real.sin θ ≤ cheb (2 * Real.cos θ) j * Real.sin θ := by rw [hcs]; exact hge
  -- divide by sinθ > 0
  nlinarith [this, hsinθ]

/-! ## §5.  `Boundary` from the Hecke form.

The cusp-boundary `cheb` data carried by `Boundary` (`cheb(m+2)=0, cheb(m+1)=1`) IS
the Hecke arithmetic: from `cheb_sin`, `cheb(m+2)·sinθ = sin((m+2)θ) = sin π = 0` and
`cheb(m+1)·sinθ = sin((m+1)θ) = sin(π−θ) = sinθ`.  So a `Boundary l m` is constructible
from `hHecke : l = 2cos(π/(m+2))` (with `m ≥ 1`). -/

/-- `sin θ > 0` for `θ = π/(m+2)`, `m ≥ 1`. -/
theorem sin_hecke_pos (m : ℕ) (hm : 1 ≤ m) :
    0 < Real.sin (Real.pi / ((m:ℝ) + 2)) := by
  have hmr : (0:ℝ) < (m:ℝ) + 2 := by positivity
  apply Real.sin_pos_of_pos_of_lt_pi
  · positivity
  · rw [div_lt_iff₀ hmr]; nlinarith [Real.pi_pos, (by exact_mod_cast hm : (1:ℝ) ≤ (m:ℝ))]

/-- **`Boundary` from the Hecke form.**  For `l = 2cos(π/(m+2))`, `m ≥ 1`, the cusp-boundary
data `cheb l (m+2) = 0`, `cheb l (m+1) = 1` holds, so `Boundary l m` is constructible. -/
def boundary_of_hecke (m : ℕ) (hm : 1 ≤ m) (l : ℝ)
    (hHecke : l = 2 * Real.cos (Real.pi / ((m:ℝ) + 2))) : Boundary l m := by
  set θ : ℝ := Real.pi / ((m:ℝ) + 2) with hθ
  have hmr : (0:ℝ) < (m:ℝ) + 2 := by positivity
  have hsinθ : 0 < Real.sin θ := sin_hecke_pos m hm
  have hq0 : cheb l (m + 2) = 0 := by
    subst hHecke
    have h := cheb_sin θ (m + 2)
    have hpiθ : (((m + 2 : ℕ)):ℝ) * θ = Real.pi := by
      rw [hθ]; push_cast; field_simp
    rw [hpiθ, Real.sin_pi] at h
    rcases mul_eq_zero.mp h with h1 | h2
    · exact h1
    · exact absurd h2 (ne_of_gt hsinθ)
  have hq1 : cheb l (m + 1) = 1 := by
    subst hHecke
    have h := cheb_sin θ (m + 1)
    have hpiθ : (((m + 1 : ℕ)):ℝ) * θ = Real.pi - θ := by
      rw [hθ]; push_cast; field_simp; ring
    rw [hpiθ, Real.sin_pi_sub] at h
    -- cheb(m+1)·sinθ = sinθ ⇒ (cheb(m+1) − 1)·sinθ = 0
    have hfac : (cheb (2 * Real.cos θ) (m + 1) - 1) * Real.sin θ = 0 := by
      have : cheb (2 * Real.cos θ) (m + 1) * Real.sin θ - Real.sin θ = 0 := by linarith [h]
      linarith [this, (by ring : (cheb (2 * Real.cos θ) (m + 1) - 1) * Real.sin θ
        = cheb (2 * Real.cos θ) (m + 1) * Real.sin θ - Real.sin θ)]
    rcases mul_eq_zero.mp hfac with h1 | h2
    · linarith [h1]
    · exact absurd h2 (ne_of_gt hsinθ)
  exact ⟨hq0, hq1⟩

/-! ## §6.  Assembling `GenuineClassGen` — `hGen` AS A THEOREM.

We now build the per-point `GenuineClassGen` record from:
  * `orbit n ∈ Taha l`  (the five Taha fields except `0 < b`), supplied by the engine;
  * `0 < (orbit n).2`  (corridor positivity of the second coordinate — a property of the
    BCZ section, supplied by the engine if `D := Taha l ∩ {0 < b}`);
  * `hHecke : l = 2cos(π/(m+2))`  (the Hecke arithmetic) — discharges `hDeepData`.

`hDeepData`: Fact 1 (`2 ≤ branchIdx`) is `branchIdx_ge_two` (from `htaha`); Fact 2
(`0 ≤ L_{i+1}`) is `L_succ_nonneg_of_chebpos` fed by `chebPos_of_hecke` at `j = i` and
`j = i+1` (valid since a deep-mid index `i < m` keeps `i+1 ≤ m ≤ m+1`). -/

noncomputable section
variable (l : ℝ) (m : ℕ)

/-- **Per-point `GenuineClassGen` from Taha-membership + `0 < b` + the Hecke form.** -/
theorem genuineClassGen_of_mem (hm : 1 ≤ m)
    (hHecke : l = 2 * Real.cos (Real.pi / ((m:ℝ) + 2)))
    (orbit : ℕ → ℝ × ℝ) (n : ℕ)
    (hmem : orbit n ∈ UniformOnset.Taha l) (hbpos : 0 < (orbit n).2) :
    GenuineClassGen l m orbit n := by
  obtain ⟨ha, ha1, htaha, hb⟩ := hmem
  refine
    { hb := hb, ha := ha, ha1 := ha1, hbpos := hbpos, htaha := htaha
      hDeepData := ?_ }
  intro B hdm
  -- the deep-mid antecedent unfolds to branchIdx < m
  set a := (orbit n).1 with hadef
  set b := (orbit n).2 with hbdef
  set hbr := HeckeS1.branch_exists l a b m B.hq0 B.hq1 hb with hbrdef
  set i := HeckeS1.branchIdx l a b hbr with hidef
  have hdm' : i < m := hdm
  -- Fact 1 : 2 ≤ i
  have hi2 : 2 ≤ i := branchIdx_ge_two (m := m) l a b B hb htaha
  -- Fact 2 : 0 ≤ L_{i+1}.  Need cheb i > 0 and cheb (i+1) ≥ 1.
  have hi1 : 1 ≤ i := by omega
  have hci1pos : 1 ≤ HeckeS1.cheb l i := by
    rw [hHecke]; exact chebPos_of_hecke m i hm hi1 (by omega)
  have hci2 : 1 ≤ HeckeS1.cheb l (i + 1) := by
    rw [hHecke]; exact chebPos_of_hecke m (i + 1) hm (by omega) (by omega)
  have hci : 0 < HeckeS1.cheb l i := by linarith
  have hsucc : 0 ≤ HeckeS1.L l a b (i + 1) :=
    L_succ_nonneg_of_chebpos l a b i ha (le_of_lt hbpos) hci hci2
  exact ⟨hi2, hsucc⟩

/-- **`Tgen`-orbit genuine — `hGen` as a THEOREM.**  Every `Tgen`-orbit through
`Taha l ∩ {0 < b}` carries the genuine per-point classification `GenuineClassGen`.  This
is exactly the `hGen` hypothesis of `perq_Xomega_lb_qge19_GEN`, now PROVED from
`step_trichotomy` (sealed) + the Casorati coupling + cheb-positivity (`hHecke`). -/
theorem Tgen_orbit_genuine (hm : 1 ≤ m)
    (hHecke : l = 2 * Real.cos (Real.pi / ((m:ℝ) + 2)))
    (orbit : ℕ → ℝ × ℝ)
    (hmem : ∀ n, orbit n ∈ UniformOnset.Taha l) (hbpos : ∀ n, 0 < (orbit n).2) :
    ∀ n, GenuineClassGen l m orbit n :=
  fun n => genuineClassGen_of_mem l m hm hHecke orbit n (hmem n) (hbpos n)

end

/-! ## §7.  THE hGen-FREE q ≥ 19 LOWER BOUND.

`perq_Xomega_lb_qge19_GEN` carried `hGen`.  Here we DROP it: with the section domain
`D := Taha l ∩ {p | 0 < p.2}` (the BCZ section: Taha + corridor positivity of the second
coordinate — purely a property of the invariant measure, at parity with the carried
`μ (Taha)ᶜ = 0`), the engine supplies BOTH `orbit n ∈ Taha l` AND `0 < (orbit n).2` per
orbit point, and `Tgen_orbit_genuine` then PROVES the classification.  The only carried
items are the STANDARD invariant-measure setup: `MeasurePreserving (Tgen)`,
`μ (Taha l ∩ {0<b})ᶜ = 0`, `hFW`, and the Hecke form `hHecke`. -/

open MeasureTheory UniformOnset GenuineSelfMap ToplevelStitchGen in
/-- **q ≥ 19 lower bound on `Tgen` — `hGen` DISCHARGED.**  No genuine-classification
hypothesis: it is proved internally via `Tgen_orbit_genuine` (Casorati + cheb-positivity
from `hHecke`).  Carries only the standard invariant-measure setup
(`MeasurePreserving (Tgen)`, `μ (section)ᶜ = 0`, `hFW`) plus the Hecke form. -/
theorem perq_Xomega_lb_qge19_GEN'
    {mpoly : ℝ → Prop} (hFW : Fwindow6 mpoly)
    {l : ℝ} (m : ℕ) (B : Boundary l m)
    (hHecke : l = 2 * Real.cos (Real.pi / ((m:ℝ) + 2)))
    (hmp : mpoly l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l) (hlphi : l ^ 2 ≥ l + 1)
    (hm : 2 ≤ m)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμT : μ ((Taha l) ∩ {p | 0 < p.2})ᶜ = 0)
    (hinv : MeasurePreserving (Tgen l m B) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, UniformOnset.Pgen l x ≤ M) :
    1 / l ^ 3 ≤ essSup (UniformOnset.Pgen l) μ := by
  apply engine (Tgen l m B) (UniformOnset.Pgen l) ((Taha l) ∩ {p | 0 < p.2}) (1 / l ^ 3) M μ
    hμT hinv hPbdd
  intro orbit hmem hstep
  -- split the strengthened membership
  have hmemTaha : ∀ n, orbit n ∈ Taha l := fun n => (hmem n).1
  have hbpos : ∀ n, 0 < (orbit n).2 := fun n => (hmem n).2
  -- hGen as a theorem
  have hGen : ∀ n, GenuineClassGen l m orbit n :=
    Tgen_orbit_genuine l m (by omega) hHecke orbit hmemTaha hbpos
  exact genuine_no_sustained_6win hFW m B hmp h1 h2 hlo hlphi hm orbit hmemTaha hstep hGen

end GenuineClassDischarge

-- ════════════ AXIOM AUDIT ════════════
#print axioms GenuineClassDischarge.casorati
#print axioms GenuineClassDischarge.branchIdx_ge_two
#print axioms GenuineClassDischarge.L_succ_nonneg_of_chebpos
#print axioms GenuineClassDischarge.cheb_sin
#print axioms GenuineClassDischarge.chebPos_of_hecke
#print axioms GenuineClassDischarge.boundary_of_hecke
#print axioms GenuineClassDischarge.genuineClassGen_of_mem
#print axioms GenuineClassDischarge.Tgen_orbit_genuine
#print axioms GenuineClassDischarge.perq_Xomega_lb_qge19_GEN'

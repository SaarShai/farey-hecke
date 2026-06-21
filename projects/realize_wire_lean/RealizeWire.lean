import Mathlib
import L1bArcCoverage
import LblkWindow
import OnsetEquality
import GenuineClassDischarge

set_option maxHeartbeats 4000000

/-!
# `RealizeWire.lean` — B-WIRE: discharge `FwindowL (L_blk q)` from the corridor
realization identity (taken as a NAMED hypothesis) and assemble the `q ≥ 22` genuine
onset lower bound.

## Scope (HONEST)

The genuinely hard analytic crux — the uniform escape-margin
`1/λ³ ≤ g_corr (L_blk q) q` for all `q ≥ 18` — is ALREADY PROVED axiom-clean as
`L1bArcCoverage.B1_target`.  The remaining open input is the corridor REALIZATION
identity (`g_corr ≤ g_true`): along any corridor `c`-sequence obeying the genuine
floor-1 recurrence, a length-`L_blk q` block window of the scalar products
`c(i+j)·c(i+j+1)` attains the `g_corr` lower bound.

This file:
1. names that realization identity as a single Prop `CorridorRealization q`
   (the `c`-native form of `no_sustained_corridor`'s `hbridge`, in the SAME
   `FwindowL` sequence convention);
2. PROVES the inf-step + L1b chaining: `CorridorRealization q → FwindowL (L_blk q) mpoly`
   for any `mpoly` pinning `lam = lamq q` (no weakening of `B1_target`);
3. wires the discharged `FwindowL (L_blk q)` into the sealed
   `LblkWindow.Xomega_ge_L`, yielding the genuine `1/λ³ ≤ Xomega` for `q = m+2 ≥ 22`,
   conditional ONLY on `CorridorRealization (m+2)` + definitional Hecke / measure-class data.

NOTHING here introduces a `sorry`.  The SOLE remaining open mathematical input is the
named `CorridorRealization` hypothesis (target A, the realization identity); everything
else (the inf-step, the L1b bound, the sealed-Xomega wiring) is proved.
-/

namespace RealizeWire

open L1bArcCoverage
open GenuineSelfMap
open scoped Classical

noncomputable section

/-! ## §1.  The named corridor-realization identity (target A), in `c`-native form. -/

/-- **Corridor realization identity** (target A; the `c`-native form of
`BCZHeckeGATE2_L1_skeleton.no_sustained_corridor`'s `hbridge`).

For any corridor sequence `c : ℕ → ℝ` obeying the genuine floor-1 corridor data
(positive, capped by `1`, both lower-Taha-edge inequalities, and the floor recurrence
that the `M_W` block step induces on the scalar coordinate), at parameter `λ = lamq q`,
every length-`L_blk q` block window of the scalar products `c(i+j)·c(i+j+1)` attains the
`g_corr (L_blk q) q` lower bound.

This is EXACTLY the realization input the genuine chain needs: combined with the PROVED
`B1_target` (`1/λ³ ≤ g_corr`) it forces some window product `≥ 1/λ³`.  It is the direct
corridor analog of the energy-route `pgen_orbit_realization` (PROVED axiom-clean in
`hsa_realization_lean`); deriving it (recurrence → `R·cos` closed form → window-max
pigeonhole via `cos_grid_hit` / `arc_coverage_ineq`) is target A. -/
def CorridorRealization (q : ℕ) : Prop :=
  ∀ (hL : 0 < L_blk q) (c : ℕ → ℝ),
    (∀ n, 0 < c n) → (∀ n, c n ≤ 1) →
    (∀ n, c n + lamq q * c (n+1) > 1) → (∀ n, lamq q * c n + c (n+1) > 1) →
    (∀ n, c n + c (n+2) = (⌊(1 + c n)/(lamq q * c (n+1))⌋ : ℝ) * lamq q * c (n+1)) →
    ∀ i, g_corr (L_blk q) q hL ≤
      (Finset.range (L_blk q)).sup' (Finset.nonempty_range_iff.mpr hL.ne')
        (fun j => c (i+j) * c (i+j+1))

/-! ## §2.  The inf-step + L1b chaining: `CorridorRealization q → FwindowL (L_blk q) mpoly`.

The `mpoly` is required to pin `lam = lamq q` (so `B1_target`'s `1/lamq q ^ 3` lines up with
`FwindowL`'s `1/lam^3`).  No weakening of `B1_target`: we use it verbatim. -/

/-- **B-WIRE core.**  The realization identity (A) discharges the discrete length-`L_blk q`
F-window for any `mpoly` pinning `lam = lamq q`, using the PROVED continuous half
`B1_target` (`1/λ³ ≤ g_corr (L_blk q) q`).  Proof: chain
`1/lam^3 = 1/lamq q ^3 ≤ g_corr ≤ sup'_{j<L} c(i+j)·c(i+j+1)`; the sup' is attained at
some `j₀ < L_blk q`, so `c(i+j₀)·c(i+j₀+1) ≥ 1/lam^3`, contradicting all-sub-threshold. -/
theorem FwindowL_Lblk_of_realization
    (q : ℕ) (hq : 18 ≤ q)
    {mpoly : ℝ → Prop} (hpin : ∀ lam, mpoly lam → lam = lamq q)
    (hreal : CorridorRealization q) :
    LblkWindow.FwindowL (L_blk q) mpoly := by
  -- L_blk q ≥ 2 > 0 always (it is `…+2`).
  have hLpos : 0 < L_blk q := by unfold L_blk; omega
  intro lam hmp h1 h2 hlo c hpos hcap hreg1 hreg2 hrec i hall
  -- Pin lam = lamq q.
  have hlam : lam = lamq q := hpin lam hmp
  subst hlam
  -- Continuous half (PROVED): 1/λ³ ≤ g_corr (L_blk q) q.
  have hL1b : 1 / lamq q ^ 3 ≤ g_corr (L_blk q) q hLpos := B1_target q hq hLpos
  -- Realization (A): g_corr ≤ window-sup of products, at window start i.
  have hbridge := hreal hLpos c hpos hcap hreg1 hreg2 hrec i
  -- The finite sup' is attained at some index j₀ < L_blk q.
  obtain ⟨j₀, hj₀mem, hj₀eq⟩ :=
    (Finset.range (L_blk q)).exists_mem_eq_sup'
      (Finset.nonempty_range_iff.mpr hLpos.ne')
      (fun j => c (i+j) * c (i+j+1))
  have hj₀lt : j₀ < L_blk q := Finset.mem_range.mp hj₀mem
  -- Chain: 1/λ³ ≤ g_corr ≤ sup' = c(i+j₀)·c(i+j₀+1).
  have hge : 1 / lamq q ^ 3 ≤ c (i+j₀) * c (i+j₀+1) := by
    rw [hj₀eq] at hbridge; exact le_trans hL1b hbridge
  -- But all-sub-threshold forces the same product < 1/λ³ — contradiction.
  have hlt : c (i+j₀) * c (i+j₀+1) < 1 / lamq q ^ 3 := by
    have := hall j₀ hj₀lt
    -- `hall j` states `c (i+j) * c (i+j+1) < 1/lam^3`; here lam = lamq q.
    simpa using this
  exact absurd hge (not_le.mpr hlt)

/-! ## §3.  Assembly: the `q = m+2 ≥ 22` genuine `Xomega` lower bound.

We tie `q := m + 2` and pin `lam = lamq (m+2)` from `hHecke`.  The conclusion is the SEALED
`OnsetEquality.Xomega` value (via `LblkWindow.Xomega_ge_L`), with NO object weakened.
The ONLY open input is `CorridorRealization (m+2)` (target A) plus definitional Hecke /
band / measure-class data. -/

/-- `lamq (m+2) = l` from the Hecke value. -/
theorem lamq_eq_of_hecke {l : ℝ} (m : ℕ)
    (hHecke : l = 2 * Real.cos (Real.pi / ((m:ℝ) + 2))) :
    lamq (m + 2) = l := by
  unfold lamq
  rw [hHecke]
  congr 2
  push_cast
  ring

/-- **The pinning `mpoly`** at `q = m+2`: `lam = lamq (m+2)`.  Trivially pins. -/
def mpolyLam (q : ℕ) : ℝ → Prop := fun lam => lam = lamq q

theorem mpolyLam_pins (q : ℕ) : ∀ lam, mpolyLam q lam → lam = lamq q := fun _ h => h

/-- **q = m+2 ≥ 22 genuine onset lower bound — sealed `Xomega`, conditional ONLY on the
realization identity (A) + definitional/measure data.**

`1/λ³ ≤ Xomega l m B`, where `Xomega` is `OnsetEquality.Xomega` (`= sInf XomegaSet`, the
genuine onset value).  Carries:
* `hreal : CorridorRealization (m+2)`        — the SOLE open input (target A);
* `hHecke : l = 2cos(π/(m+2))`               — DEFINITIONAL Hecke value;
* band facts `h1,h2,hlo,hlphi`, `hm : 2 ≤ m`, `hq22 : 22 ≤ m+2` — DEFINITIONAL;
* `hne : (XomegaSet …).Nonempty`             — measure-class data.

Nothing weakened: the window discharge is SOUND (real `B1_target`, no weakened cover). -/
theorem Xomega_ge_qge22_uncond
    {l : ℝ} (m : ℕ) (B : GenuineSelfMap.Boundary l m)
    (hreal : CorridorRealization (m + 2))
    (hHecke : l = 2 * Real.cos (Real.pi / ((m:ℝ) + 2)))
    (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l) (hlphi : l ^ 2 ≥ l + 1)
    (hm : 2 ≤ m) (hq22 : 22 ≤ m + 2)
    (hne : (OnsetEquality.XomegaSet l m B).Nonempty) :
    1 / l ^ 3 ≤ OnsetEquality.Xomega l m B := by
  -- q := m + 2 ≥ 22 ≥ 18.
  have hq18 : 18 ≤ m + 2 := by omega
  -- Pin: lamq (m+2) = l.
  have hlamq : lamq (m + 2) = l := lamq_eq_of_hecke m hHecke
  -- The pinning mpoly and its discharge of the window.
  have hpin : ∀ lam, mpolyLam (m + 2) lam → lam = lamq (m + 2) := mpolyLam_pins (m + 2)
  have hFW : LblkWindow.FwindowL (L_blk (m + 2)) (mpolyLam (m + 2)) :=
    FwindowL_Lblk_of_realization (m + 2) hq18 hpin hreal
  -- `hmp : mpolyLam (m+2) l` is `l = lamq (m+2)`, i.e. `hlamq.symm`.
  have hmp : mpolyLam (m + 2) l := hlamq.symm
  -- Wire into the sealed `Xomega_ge_L` (the genuine sInf-XomegaSet value).
  exact LblkWindow.Xomega_ge_L (L_blk (m + 2)) hFW m B hHecke hmp h1 h2 hlo hlphi hm hne

end

/-! ## §4.  AXIOM AUDIT. -/

#print axioms RealizeWire.FwindowL_Lblk_of_realization
#print axioms RealizeWire.lamq_eq_of_hecke
#print axioms RealizeWire.Xomega_ge_qge22_uncond

end RealizeWire

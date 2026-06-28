<!-- INTERNAL — merge-target for the Shai–Koyama joint paper, CORRIDOR (our) track. -->
<!-- NOT for submission; all outward comms USER-gated. Assembled 2026-06-28. -->
<!-- This file UNIFIES the four pre-existing corridor drafts into one structure with -->
<!-- ONE reconciled status ledger. It assembles BY REFERENCE — the prose lives in the -->
<!-- source files named per section; this is the spine + the authoritative claim ledger. -->

# The Farey/Hecke Corridor — consolidated manuscript spine (Shai side)

**Role.** Per Koyama correspondence entry [5] (2026-06-28) the joint paper splits into two
parallel tracks: **his** number-theoretic cornerstone (the `−1`-dominance repair under
`p^{−1/2}` weighting) and **ours**, the *corridor mechanics* — "firm up the magnificent
Farey/Hecke corridor mechanics." This file is the merge-target for our track. The two tracks
join into one manuscript at end of summer; nothing here is communicated externally without
explicit author approval.

---

## 0. Reconciled status-tag legend (unifies the four source drafts)

The source drafts used three slightly different tag vocabularies; this is the single
reconciled set. Every assertion in the assembled paper carries exactly one.

- **[PROVEN:Lean]** — sorry-free Lean 4 (Mathlib v4.28.0); `#print axioms` returns exactly
  `[propext, Classical.choice, Quot.sound]` (no `sorryAx`, no `native_decide`). Declaration
  name + file quoted.
- **[PROVEN:Lean-mod-H]** — Lean theorem object axiom-clean **modulo named structural
  hypotheses carried in the statement**; each hypothesis tracked with its own tag.
- **[PROVEN:exact-witness]** — explicit algebraic certificate over ℚ(λ_q), exact symbolic
  arithmetic (no float); λ_q pinned by rational-interval minimal-polynomial sign certificate.
- **[CERTIFIED-NUMERIC]** — rigorous interval / high-precision (mpmath dps≥50) arithmetic
  whose integer/sign output is robust under refinement.
- **[NUMERICAL]** — exact-witness ladders / junction-safe orbit scans / golden-section
  minimization; not a proof.
- **[CONJECTURE]** — consistent with all data, no proof claimed.
- **[REFUTED]** — a previously-stated pattern now disproven; retained only as a cautionary
  record, never cited as a result.

---

## 1. Unified abstract (corridor track)

Fix an integer q ≥ 3, the Hecke triangle group G_q ⊂ PSL(2,ℝ), λ_q = 2cos(π/q). On the last
(scalar) branch of the Taha G_q–BCZ Poincaré section (Taha, arXiv:1810.10668) — the
Hecke-family analogue of the Farey–BCZ map — the return map is (a,b) ↦ (b, −a + kλ_q b) and
the gap-product observable is P = a·b (genuine form P_gen = a(a+λ_q b)/λ_q ≥ a·b). We study
the ergodic-optimization edge value X_Ω(q) = inf over T-invariant probability measures of
ess-sup_μ P — the support edge of the slope-gap statistic. We establish, on the corridor side:

1. **Onset value (machine-verified).** X_Ω(q) = 1/λ_q³ as a non-attained infimum, **[PROVEN:Lean]
   axiom-clean for q ∈ {5,…,21}** (17 indices, golden-L q=5 included). Realized in the limit by
   the cusp parabolic-Dirac sequence. For q ≥ 22 the result is **reduced** to a single
   in-domain-residency interface residual (see §4) — not unconditional.
2. **Arithmeticity dichotomy.** B(q) = 2 ⟺ G_q arithmetic (q ∈ {3,4,6}). Forward **[PROVEN:Lean]**;
   reverse **[PROVEN:exact-witness]** for q = 5,7,8,…,24 (q=5,7 also Lean). Outright both
   directions on 3 ≤ q ≤ 7.
3. **Rotation-arc mechanism.** The k=1 last-branch step M = [[0,1],[−1,λ_q]] is the elliptic
   rotation by π/q preserving E = a² − λ_q ab + b²; a cluster is a sub-threshold rotation arc.
   Forward implication **[PROVEN:Lean]**.
4. **Growth + no closed form.** B(q) grows with asymptotic slope ≈ 0.216 q for non-arithmetic q
   and admits **no continuous closed form** (arithmetic lattice-vs-notch resonance; the
   formula B(q)=2+⌊(q−1)/6⌋ is **[REFUTED]**).

We position (1)–(2) honestly as the machine-verified, *local-gap-statistic* instance of the
Luo–Sarnak bounded-clustering program and the Geninska–Leuzinger global-trace-set
characterization; we do not claim a new arithmeticity criterion.

---

## 2. Section map — assembled BY REFERENCE (source-of-truth files)

| § | Content | Source file (authoritative prose) | Draft state |
|---|---------|-----------------------------------|-------------|
| Intro | Setup, section, observable, positioning vs Luo–Sarnak / Geninska–Leuzinger | `PAPER_arithmeticity_dichotomy_SUBMISSION.md` §1 + `PAPER_uniform_onset_SUBMISSION.md` Abstract/§1 | complete |
| Onset value | X_Ω(q)=1/λ³ equality + lower bound, q=5..21 | `PAPER_uniform_onset_SUBMISSION.md` §2–§5 | complete |
| Dichotomy | B(q)=2 ⟺ arithmetic; forward Lean + reverse witnesses | `PAPER_arithmeticity_dichotomy_SUBMISSION.md` §2–§6 | complete |
| Mechanism | rotation-arc on conserved energy ellipse E | `manuscript/section_mechanism.md` | complete |
| Reverse/realization | B(q) realization witnesses (uniform family + per-q ladder) | `manuscript/section_uniform_witness.md` | complete |
| q≥22 reduction | reduction to the in-domain-residency interface residual | `UNCONDITIONAL_REDUCTION_2026-06-20.md` + `uniform_onset_blockmap_2026-06-20.md` | complete (residual OPEN, §4) |
| Growth/no-closed-form | 0.216q slope; resonance set; refuted formula | `Bq_rotation_arc_2026-06-14.md` + `Bq_width_resonance_closed_form_2026-06-18.md` | complete |

**Assembly TODO (mechanical, not research):** flatten the seven sources into one LaTeX
document with continuous numbering and the §0 unified tag set. No new mathematics required —
every section is already drafted and status-tagged.

---

## 3. Authoritative verified-bank ledger (the heart of the merge)

One row per load-bearing corridor result. This is the reconciled truth; where a source draft
disagrees, this table wins (see §5 reconciliation notes).

| # | Result | Range / scope | Status | Lean decl / witness · file |
|---|--------|---------------|--------|----------------------------|
| R1 | X_Ω(q) = 1/λ_q³ (equality, non-attained inf) | q = 5..21 | **[PROVEN:Lean]** axiom-clean | `OnsetEquality.lean`, `OnsetEqualityUniform.lean`, `OnsetEqualityLowQ.lean`, `GenuineClassDischarge.lean` |
| R2 | X_Ω(q) ≥ 1/λ_q³ (lower bound) | q = 5..21 | **[PROVEN:Lean]** | same footprint |
| R3 | X_Ω(q) ≥ 1/λ_q³ (lower bound) | q ≥ 22 | **[PROVEN:Lean-mod-H]** → ONE residual | `ToplevelStitch.Xomega_lb_allq` mod `hCorr`,`(P2)`; reduced per §4 |
| R4 | L1b analytic arc-width crux | all q | **[PROVEN:Lean]** (sealed; does NOT alone discharge `hCorr`) | `fcorr_lb` / `B1_target` |
| R5 | Dichotomy forward: B(q)=2 for q∈{3,4,6} | q ∈ {3,4,6} | **[PROVEN:Lean]** | arithmetic no-3-cluster theorems |
| R6 | Dichotomy reverse: B(q)≥3 for non-arith | q = 5,7,8,…,24 | **[PROVEN:exact-witness]** (q=5,7 also Lean) | explicit 3-clusters in ℚ(λ_q) |
| R7 | Dichotomy reverse, all non-arith q | q ≥ 5 non-arith | **[CONJECTURE]** | — |
| R8 | M preserves E and = rotation by π/q | q ≥ 5 | **[PROVEN:Lean]** | `Mmap_preserves_E`, `Mmat_conj_eq_rot` · `BCZHeckeRotationArc.lean` |
| R9 | cluster ⟹ rotation-arc (forward) | q ≥ 5 | **[PROVEN:Lean]** | `cluster_is_rotation_arc`, `cluster_le_rotation_arc` · same |
| R10 | B(q) realization residual R2 (reverse arc) | q = 5..13 ladder + uniform family | **[PROVEN:exact-witness]** / **[PROVEN:Lean-mod-H]** `hrealize` | `Bq_eq_rotation_arc` · same file; `section_uniform_witness.md` |
| R11 | B(q) ~ 0.216 q asymptotic slope | non-arith q | **[NUMERICAL]** | orbit scans, `Bq_rotation_arc_2026-06-14.md` |
| R12 | B(q) has NO continuous closed form (resonance) | all q | **[PROVEN:exact-witness]** (structural) + formula **[REFUTED]** | `Bq_width_resonance_closed_form_2026-06-18.md` |
| R13 | Low-q onset values X(3)=2/9, X(4)=√2/8 | q=3,4 | **[PROVEN:exact-witness]** | dichotomy draft |

---

## 4. The single open residual (q ≥ 22) — KOYAMA-OWNED, DEFERRED

The all-q lower bound R3 is reduced (not solved) to **one in-domain-residency interface
residual**: the naive six-window route caps at q=21 (it fails once B(q) > ~5, and B(q)~0.22q),
so q≥22 carries the corridor-assembly hypothesis `hCorr` (block-monodromy → essSup wiring) plus
the genuine-map bridge `(P2)`. L1b (R4) is sealed but does not alone discharge `hCorr`.

**Ownership (entry [5], verbatim intent):** Koyama took this — *"I will give it some thought
from the transfer-operator perspective once I have some cognitive breathing room."* He also
endorsed the **no-dwell / measure** mechanism over the uniform-spectral-gap framing; therefore
the certified spectral gaps (gap_q5=0.797, gap_q7=0.659) are **NOT load-bearing** and should
not be developed further on our side. **Action for us: NONE — do not spend compute attacking
q≥22.** It is on his plate, on his timeline.

---

## 5. Reconciliation notes (drift fixed in this consolidation)

- **STALE:** the dichotomy draft (`PAPER_arithmeticity_dichotomy_SUBMISSION.md`, 2026-06-13)
  §Abstract/§7 states "X_Ω(q) = 1/λ_q³ is OPEN (in progress)." **Superseded** by the onset draft
  (2026-06-14) and the 2026-06-20 reduction: R1/R2 are PROVEN:Lean for q=5..21; q≥22 is
  reduced-to-residual (R3). When flattening, replace that line with a cross-reference to §3 R1–R3.
- **CAUTION:** `PAPER_DRAFT_arithmeticity_dichotomy.md` is the OLD draft, explicitly superseded by
  the SUBMISSION version — do not merge from it.
- **Tag unification:** `[PROVED:Lean]` (witness section) and `[PROVEN:Lean]` (papers) are the same
  tag → use `[PROVEN:Lean]` (§0).

---

## 6. Honest open / not-ours list (so nothing is over-claimed)

- **q ≥ 22 unconditional bound** — OPEN, reduced to one residual; **Koyama-owned, deferred** (§4).
- **All-q reverse dichotomy** (R7) — CONJECTURE; only q≤24 has witnesses, only q≤7 both directions.
- **Exact B(q) value** — settled-NEGATIVE: no continuous closed form (R12). Do not put a formula
  in the paper.
- **Not claimed:** a new arithmeticity criterion, or being the first statistic to detect
  arithmeticity. Positioned as the machine-verified local-gap-statistic instance only.
- **Dead/owned (do not reintroduce):** the Veech slope-gap "X=1/λ³ = hard edge" bridge
  (`VEECH_BRIDGE_2026-06-27.md`) and any X_Ω-as-new-invariant framing
  (`Xomega_generalize_2026-06-14.md`).

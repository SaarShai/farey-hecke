## HARVEST — 2026-08-17

Task `cc1d7494-eb9d-418e-beff-28fe4e107db6` returned **COMPLETE**. Downloaded
to `projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle/`
(`RateCore.lean` + `ARISTOTLE_SUMMARY.md` + manifest/lakefile/toolchain).

**Sorry count: 0 live.** Two `sorry` occurrences in the raw file (lines 199,
387) are both inside `/- FALSE AS STATED ... -/` comment blocks that keep
the draft's original (disproved) statements visible for reference — neither
is a live declaration. Confirmed by inspection of surrounding context.

**Corrections present, as documented:**
- `cpow_neg_two_s_bound_false` (proves the unconditional P4 statement is
  false, witness `x=1,y=2,s=-1`) + `cpow_neg_two_s_bound'` (same bound with
  added hypothesis `-1/2 ≤ Re s`) — both present and proved.
- `wordLimitMap_matched_depth_one_false` (proves the draft's stated
  depth-1 identity `c_{[]}(λ) = -1/λ` is false, witness `λ=1`) +
  `wordLimitMap_matched_depth_one'` (proves the correct identity
  `c_{[]}(λ) = λ`) — both present and proved.

**Axiom usage: `wordLimitMap_injective_on_matched` confirmed unused.**
Declared once (line 371) as a standing hypothesis; grep for the identifier
elsewhere in the file returns no other occurrence — nothing in the proved
theorems depends on it.

**Local build: SUCCEEDED (not skipped).** v25's `.lake` cache
(`projects/aristotle_dispatch_v25/result/project_aristotle/.lake`, ~12 GB)
was reused — `lake-manifest.json` for v26 is byte-identical to v25's (same
Mathlib rev `8f9d9cff6bd728b17a24e163c9402775d9e6a365` pinned via `v4.28.0`,
same toolchain `leanprover/lean4:v4.28.0`), so the cache was copied wholesale
into the v26 result dir and `lake build RateCore` ran against it rather than
rebuilding Mathlib from scratch. `lake build RateCore` completed in the
result directory: `Build completed successfully (8027 jobs)`, only two
`unused variable` linter warnings (`hq` at line 263, `hlam` at line 415, both
noted in-file as intentionally-unneeded hypotheses kept for draft-fidelity),
zero errors, zero sorry-warnings. This is a genuine local re-verification,
not just Aristotle's cloud report.

**Verdict: P1, P2, P3, P5, P6 (+ P6 corollary) and the M1 depth-1/depth-2
finite instances are now machine-verified** (both locally rebuilt and
Aristotle-cloud-reported). P4 is machine-verified in its corrected form
(`Re s ≥ -1/2` hypothesis added — see downstream-impact note below, and the
updated draft file for the domain check). The general N1/N2–N4/M2/M3/§3
gaps remain untouched, exactly as scoped in this dispatch's original note
below.

---

# V26 dispatch note — RATE lemma formalizable core

**Date:** 2026-08-17. **Lane G.**
**Project ID:** `4730142e-cc15-417a-bccf-ca30b25f2bcf`.
**Task ID:** `cc1d7494-eb9d-418e-beff-28fe4e107db6` (QUEUED at submit, RUNNING
as of this note — Aristotle has read `RateCore.lean` and started work).
Toolchain `leanprover/lean4:v4.28.0`, Mathlib pinned `v4.28.0` (same pin as
v25).

**Source.**
`research_notes/rh_goals_2026-08-14/lane_g/LAW_R2_RATE_LEMMA_DRAFT.md`
(DRAFT LEMMA, not a proved theorem). This dispatch formalizes only the
**P1–P6 chain** the draft's §5 gap list tags "Aristotle: YES" or "MAYBE"
under "Proved in this draft (i)", plus two finite depth-bounded instances of
gap **M1** (the word-level `λ → 2` structural map). Nothing from §3 (the
assembled candidate lemma with `Δ_X`, `E_q`, `E_θ`, `T_X`) or the other gaps
(N1–N4, M2, M3) is formalized — those remain numeric/open per the draft.

## Setup (matches draft §1 exactly)

`Qmat lam = (0, -1/lam; lam, 0)`, `Spow n = (1, n; 0, 1)` for `n : ℤ`
(closed form of `S^n`), `Emat = diag(-1, 1)`. A reduced word `w = Q S^{n_1}
Q ... S^{n_{k-1}} Q` is encoded as `List ℤ` of the exponents
`[n_1, ..., n_{k-1}]`; `depth w = w.length + 1 = k`; `c lam w` is the
lower-left entry (`(1,0)`) of the recursively-defined word matrix.

## Obligations sent (8 statements, all `sorry`, no `sorry` in any signature)

| # | Lean name | Draft correspondence |
|---|---|---|
| 1 | `c_eq_scaled_int_poly` | **P1** — `c_w(λ)·λ^{k_w}` is (the real cast of) an integer polynomial evaluated at `λ`; integer-Laurent structure. |
| 2 | `hasDerivAt_Qmat` | **P2** — `dQ/dλ = (1/λ) E Q`, entrywise `HasDerivAt`. |
| 3 | `mvt_bound` | **P3** — generic mean-value inequality `|f(b)−f(a)| ≤ M(b−a)` for `|f'| ≤ M` on `[a,b]`; the instance the draft applies to `c_w`. |
| 4 | `cpow_neg_two_s_bound` | **P4** — `‖x^{-2s} − y^{-2s}‖ ≤ 2‖s‖·min(x,y)^{-2σ-1}·|x−y|` for `x,y>0`, `s=σ+it`. |
| 5 | `two_sub_lam_le` | **P5** — `2(1−cos(π/q)) ≤ π²/q²`. |
| 6 | `c_chebyshevWord` | **P6** — Chebyshev subfamily `c_w(λ) = λ·U_{m-1}(λ/2)` (Mathlib `Polynomial.Chebyshev.U`), `w = (QS)^{m-1}Q` encoded as `chebyshevWord m = List.replicate (m-1) 1`. |
| 7 | `c_chebyshevWord_two` | **P6** corollary — `c_w(2) = 2m` for the Chebyshev word, per draft's "At λ=2: c=2m". |
| 8 | `wordLimitMap_matched_depth_one`, `c_depth_two` | **M1**, finite depth-`≤2` instances (draft: "finite-depth restricted version … is YES per (q,K)"): depth-1 word is trivial (`c=-1/λ`); depth-2 words `[n]` give the closed form `c_{[n]}(λ) = n·λ²`, injective in `n` for fixed `λ≠0`. |

**Left as an axiom, not sent for proof:** `wordLimitMap_injective_on_matched`
— the *general* (all-`K`, all-`q`) form of M1's matching-injectivity claim.
The draft explicitly tags the unrestricted M1 "Aristotle: NOT as stated"
(needs a normal-form/geodesic argument in `ℤ₂ * ℤ_q` vs `ℤ₂ * ℤ`, "the
structural lemma"); it is recorded here as a standing hypothesis so the
finite instances above type-check against the same vocabulary, not
formalized. The submission prompt explicitly told Aristotle to leave this
one alone.

## What was NOT formalized (deliberately, per the draft's own gap tags)

- **N1 (`C1`)**: the universal `sup|c_w'| ≤ (11/20)k²|c_w(λ_q)|` bound —
  numeric-only (measured max 0.518 over 1138 cosets); the draft itself calls
  the general induction "genuinely open".
- **N2–N4, M2, M3**: matching-onto-window scaling, the beyond-window tail
  majorant, the `φ(2n)` multiplicity claim, `s`-uniformity — all analytic/
  infinite-sum or numeric-only per the draft's own tags.
- **§3's candidate lemma** (the assembled `ε(q;s)` bound) and its NUMERIC-
  CONJECTURED constants (`11/20`, `C(1.1,1.5) ≤ 2.0`) — explicitly excluded
  by the task ("where the draft's constant … is NUMERIC-CONJECTURED, do NOT
  bake it into a theorem").

## Local sanity check

**Not run to completion.** `lake env lean --version` in this directory
began cloning Mathlib `v4.28.0` from scratch (no shared `.lake`/build cache
was found under this project tree or the sibling `/Users/za/code/mathlib4`
checkout); a from-scratch Mathlib build was judged too slow for this
dispatch's time budget and was aborted (partial `.lake`/`lake-manifest.json`
removed before submission, matching a clean tree). Aristotle's own
`submit` step confirmed it can read and parse `RateCore.lean` (it reported
the standard "no `.lake` folder" advisory, then proceeded to read the file
and begin work, per `aristotle show` output) — no syntax rejection at
ingestion. **This is a real gap versus the v25 workflow**, which dispatched
against an already-built `.lake` tree; a follow-up local build (or reuse of
a shared Mathlib cache) is recommended before trusting the statement types
fully, though the file was written closely against Mathlib API confirmed
present in the local `/Users/za/code/mathlib4` checkout (`Matrix` `!!`
notation, `Polynomial.Chebyshev.U : ℤ → R[X]`, `HasDerivAt`, `Complex`
`‖·‖` norm in place of the deprecated `Complex.abs`).

## Status effect

If the task returns clean, P1–P6 (the algebraic/derivative/trig/Chebyshev
core of the RATE draft) become machine-verified, and M1 gets two finite
depth-instance down payments — but the draft's headline gaps (N1's
universal `(C1)` bound, M1's general bijection, M2's tail majorant) are
**unchanged**: this dispatch does not close the RATE lemma, only its
already-"YES/MAYBE"-tagged foundational pieces. No novelty claim; the RATE
lemma itself stays DRAFT status per the source note.

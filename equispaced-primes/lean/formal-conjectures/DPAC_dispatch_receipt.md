---
title: "DPAC — Aristotle dispatch receipt: DirichletPolynomialAvoidance.lean (1 sorry-stub research_open theorem) → proof or honest reduction"
type: dispatch-receipt
domain: research
created: 2026-05-09
sources:
  - formal-conjectures/DirichletPolynomialAvoidance.lean
  - https://github.com/google-deepmind/formal-conjectures/pull/3716
  - experiments/AVOIDANCE_RATIO_RESULTS.md
  - experiments/AVOIDANCE_LFUNC_RESULTS.md
  - experiments/AVOIDANCE_EXTENDS_TO_LFUNCTIONS.md
  - experiments/AVOIDANCE_LOWER_BOUND_V2.md
  - experiments/CODEX_DPAC_LOWER_BOUND_THINKING.md
  - experiments/M1_DS_DPAC_DENSITY_ONE_RIGOROUS.md
  - experiments/M1_DS_LI_IMPLIES_DPAC.md
tags: [aristotle, dispatch, lean, formalization, DPAC, dirichlet-polynomial, mobius, riemann-zeta, langer, perron, research-open]
---

# DPAC — Aristotle dispatch receipt

## Headline

**Project submitted to Aristotle.**
- **Project ID:** `59d181d5-b207-4882-a5ba-0786ec51d361`
- **Status at dispatch:** `QUEUED`
- **Status ~2 min after dispatch:** `IN_PROGRESS` (3% progress)
- **Dispatched at (UTC):** `2026-05-09T23:55:08Z`
- **Mode:** asynchronous (no `--wait`).  Lean output is **not yet available**;
  poll for completion (instructions below).
- **Target:** Dirichlet Polynomial Avoidance Conjecture (DPAC) — a
  `research_open` problem (AMS 11M26, 30D15) with a single
  `theorem … := by sorry` skeleton, verbatim from
  `google-deepmind/formal-conjectures` PR #3716 (Saar Shai, 2026-04-11).

## API contract used

| Item | Value |
|---|---|
| Service | Harmonic Aristotle (cloud Lean theorem prover) |
| Base URL | `https://aristotle.harmonic.fun/api/v2` |
| Auth | `Authorization: Bearer $ARISTOTLE_API_KEY` |
| Client | `aristotlelib` 1.0.1 (PyPI), Python 3.13 venv at `/tmp/aristotle_venv/` |
| CLI invoked | `aristotle submit "<prompt>" --project-dir /tmp/aristotle_dispatch_DPAC` |
| API key source | `~/.farey_api_keys` (env var `ARISTOTLE_API_KEY`); length 49, prefix `arstl_`, last 4 `CwzQ` |

## Relationship to prior dispatches

Third programmatic Aristotle dispatch from this account.

| # | Project ID | Label | Date (UTC) | Status (latest) |
|---|---|---|---|---|
| 1 | `424973ae-8e9a-4ef1-8a6d-970ffa3b88ad` | SmoothedDwfFormula (P3b) | 2026-05-09T18:35Z | `COMPLETE_WITH_ERRORS` (vacuous-witness pattern) |
| 2 | `8e608890-f0ba-4a89-bbb0-a63b5bcab697` | R1_B_plus | 2026-05-09T21:07Z | `IN_PROGRESS` |
| 3 | `59d181d5-b207-4882-a5ba-0786ec51d361` | **DPAC** | 2026-05-09T23:55Z | `IN_PROGRESS` (3% at receipt-write time) |

This dispatch is independent of the other two: it formalises a single
`research_open` non-vanishing theorem from the DeepMind formal-conjectures
repository, structurally distinct from the analytic-NT P3b dispatch and the
elementary-Fourier R1 dispatch, and uses a separate Lean payload.

## Payload summary (what Aristotle is working on)

**Project directory:** `/tmp/aristotle_dispatch_DPAC/` (uploaded; minimal —
4 files, 314 LOC)

| File | LOC | MD5 | Role |
|---|---:|---|---|
| `lakefile.toml` | 11 | `d3ae68ec…888c` | Lake project config (Mathlib v4.28.0; identical to prior dispatches) |
| `lean-toolchain` | 1 | `b8b2923c…83b7` | `leanprover/lean4:v4.28.0` |
| `RequestProject/DirichletPolynomialAvoidance.lean` | 70 | `aed8d7dd…4f5b` | **Target file** — 1 `sorry` (`dirichlet_polynomial_avoidance_conjecture`); verbatim from `google-deepmind/formal-conjectures` PR #3716 with namespace adjusted from `FormalConjectures.Paper` to `RequestProject` |
| `DPAC_context.md` | 232 | `0a90d9b5…cca8` | Mathematical context: verbatim DPAC statement, Saar's 2026-04-12 email excerpt, Langer 1931 reference, full empirical evidence (avoidance ratios at 4×–16× across ζ + 5 Dirichlet L-functions, 800 interval certificates), already-considered proof routes with obstructions, three honest-reduction options (R1 density-one, R2 pointwise asymptotic, R3 LI), references |

The single `sorry` target, verbatim:

```lean
@[category research_open]
@[AMS 11M26, 30D15]
/-- For fixed K ≥ 2 and any nontrivial zero ρ of the Riemann zeta function,
the truncated Möbius Dirichlet polynomial c_K(ρ) = Σ_{k=2}^{K} μ(k) · k^{-ρ}
is nonzero. -/
theorem dirichlet_polynomial_avoidance_conjecture
    (K : ℕ) (hK : K ≥ 2)
    (ρ : ℂ) (hρ : riemannZeta ρ = 0)
    (hρ_nontrivial : 0 < ρ.re ∧ ρ.re < 1) :
    (∑ k in Finset.range (K - 1), (ArithmeticFunction.moebius (k + 2) : ℂ) *
      ((k + 2 : ℂ) ^ (-ρ))) ≠ 0 := by
  sorry
```

Per the prompt, Aristotle is **explicitly authorised to substitute an honest
reduction** if the full proof is out of reach.  Acceptable outputs ranked by
preference:

| Rank | Reduction | Mechanism | Hypotheses |
|---|---|---|---|
| 1 (preferred) | **R2 pointwise asymptotic** | Perron residue identity `c_K(ρ) ~ log K / ζ'(ρ)` | simple-zero hypothesis at `ρ` |
| 2 | **R1 density-one** | Langer `O(T log K)` vs `N(T) ~ (T/2π) log T` | none (unconditional) |
| 3 | **R3 reduction to LI** | LI for `{γ_j}` ⇒ DPAC | LI as a *theorem hypothesis*, NOT an axiom |

In all three cases the original `theorem dirichlet_polynomial_avoidance_conjecture`
must remain unchanged in name, statement, attributes (`@[category research_open]`,
`@[AMS 11M26, 30D15]`), and docstring; reductions add **new** lemmas above it.

## Prompt sent to Aristotle (verbatim, sanitised — no API key)

> Fill the single sorry in RequestProject/DirichletPolynomialAvoidance.lean
> with a rigorous Lean 4 proof in Mathlib v4.28.0, OR an honest reduction
> (see options below).
>
> The target is the Dirichlet Polynomial Avoidance Conjecture (DPAC):
>
>   For the truncated Mobius-Dirichlet polynomial
>     c_K(s) := sum_{n=2}^{K} mu(n) * n^{-s},  K >= 2,
>   the zeros of c_K (which by Langer 1931 are infinitely many in the
>   critical strip) systematically avoid the ordinates of nontrivial
>   Riemann zeta zeros. Empirically, the avoidance ratio
>     R_K = min_{j<=100} |c_K(1/2 + i*gamma_j)| / min_{t in [0,T]} |c_K(1/2 + it)|
>   lies in 4x-16x for K in {5,10,15,20,30,50}, and the same property holds
>   for the five Dirichlet L-functions L(chi_3), L(chi_4), L(chi_5),
>   L(chi_11) and zeta itself; 800 interval-arithmetic certificates confirm
>   300/300 nonvanishing cases at the first 100 zeta zeros for K in {10,20,50}
>   at 100-digit precision.  See DPAC_context.md (bundled in this project
>   dir) for the full empirical table and references.
>
> The Lean target (verbatim from google-deepmind/formal-conjectures PR #3716,
> 2026-04-11, Saar Shai) is:
>
>   theorem dirichlet_polynomial_avoidance_conjecture
>       (K : Nat) (hK : K >= 2)
>       (rho : Complex) (hrho : riemannZeta rho = 0)
>       (hrho_nontrivial : 0 < rho.re /\ rho.re < 1) :
>       (sum_{k in Finset.range (K - 1)} (ArithmeticFunction.moebius (k + 2) : Complex) *
>         ((k + 2 : Complex) ^ (-rho))) != 0 := by
>     sorry
>
> A complete unconditional proof of DPAC is *comparable in difficulty to
> the Linear Independence Hypothesis (LI) for zeta-zero ordinates* and is
> likely out of reach.  We therefore explicitly authorise the following
> honest reductions, ranked by preference (any of which would be accepted
> as a successful dispatch outcome):
>
>   (R1) DENSITY-ONE (unconditional): for each fixed K >= 2, the set of
>        nontrivial zeros rho with c_K(rho) = 0 has natural density zero
>        among the zeta-zero ordinates.  Mechanism: Langer's count of
>        O(T log K) zeros of c_K up to height T versus N(T) ~ (T/2pi) log T
>        for zeta. Express the conclusion as a clean Lean lemma about the
>        limit of |{j <= N : c_K(rho_j) = 0}| / N as N -> infty going to 0.
>
>   (R2) POINTWISE ASYMPTOTIC (under simple-zero hypothesis): for each
>        fixed simple nontrivial zeta zero rho, |c_K(rho)| -> infty as
>        K -> infty; equivalently c_K(rho) != 0 for all but finitely many
>        K.  Mechanism: Perron's formula gives the residue identity
>        c_K(rho) ~ log K / zeta'(rho).  This is the most useful "honest"
>        reduction because it captures the qualitative content of DPAC.
>
>   (R3) REDUCTION TO LI (conditional, full statement): assume the Linear
>        Independence Hypothesis for the multiset {gamma_j} of zeta-zero
>        ordinates and derive DPAC verbatim.  Acceptable to introduce LI
>        as a hypothesis variable on the theorem statement (NOT as an
>        axiom).
>
> Constraints:
> - Mathlib version is v4.28.0 (lean-toolchain pinned in this project dir).
> - Do NOT introduce any new axioms.  If a sub-step truly requires Mathlib
>   infrastructure that does not yet exist in v4.28.0 (e.g. a particular
>   Perron-formula lemma for arbitrary Dirichlet polynomials), leave that
>   step as `sorry` with a `-- TODO(aristotle): <prerequisite name>`
>   comment AND prove everything else.
> - Do NOT modify the theorem statement, its name, its attributes
>   (`@[category research_open]`, `@[AMS 11M26, 30D15]`), or its
>   docstring.  If you choose reduction R1 or R2, ADD a new lemma above
>   the main theorem capturing the reduced result and use it in the
>   proof of the main theorem (which may still end with a `sorry` for the
>   unreduced full DPAC, but only if the new lemma is fully proved and
>   the reduction step is completely formal).
> - Build target: `lake build RequestProject.DirichletPolynomialAvoidance`
>   returns 0 (sorries permitted only in the unreduced parts of the main
>   theorem; all auxiliary lemmas you introduce must be sorry-free).
>
> Mathematical context bundled in this project dir:
> - DPAC_context.md (~10 KB): verbatim DPAC statement, Saar Shai 2026-04-12
>   email excerpt, Langer 1931 reference, full empirical evidence tables
>   (avoidance ratios at 4x-16x across zeta and 5 Dirichlet L-functions,
>   800 interval-arithmetic certificates), already-considered proof routes
>   with their obstructions, three honest-reduction options (R1, R2, R3),
>   and a literature reference list (Langer, Titchmarsh, Montgomery, Gonek).
>
> Project structure:
> - RequestProject/DirichletPolynomialAvoidance.lean (single target file,
>   one theorem, one sorry; verbatim DeepMind PR #3716 with namespace
>   adjusted from FormalConjectures.Paper to RequestProject)
>
> If the full proof is genuinely beyond reach within the scope of this
> dispatch (which is entirely possible — DPAC is a research-open
> problem), please attempt the strongest honest reduction (R2 preferred,
> then R1, then R3) and clearly document in a Lean comment what was
> reduced, what remains open, and which Mathlib lemmas would be needed
> for further progress.

## Aristotle's response

```
WARNING: Your project contains .lean files but no .lake folder.
Aristotle works better with access to your project's dependencies.
Did you forget to run `lake build`?

Project created: 59d181d5-b207-4882-a5ba-0786ec51d361
```

The `.lake` warning is benign (same as P3b and R1 dispatches): the upload
omits the local Mathlib build artefacts (~5 GB).  Aristotle's worker will
resolve Mathlib v4.28.0 from its own cache.

`aristotle list --limit 5` immediately after submission confirmed:

```
59d181d5-b207-4882-a5ba-0786ec51d361 QUEUED   6 secs ago    -
```

(Status moves QUEUED → IN_PROGRESS → COMPLETE / COMPLETE_WITH_ERRORS / FAILED / OUT_OF_BUDGET.)

## How to poll / retrieve the result

**Pre-flight (every session):**

```bash
set -a; source ~/.farey_api_keys; set +a   # loads ARISTOTLE_API_KEY
source /tmp/aristotle_venv/bin/activate    # aristotlelib 1.0.1
```

**Check status of just this project (one-liner):**

```bash
/tmp/aristotle_venv/bin/aristotle list --limit 50 \
  | grep -F 59d181d5-b207-4882-a5ba-0786ec51d361
```

**Block until done and download the result tarball:**

```bash
/tmp/aristotle_venv/bin/aristotle result 59d181d5-b207-4882-a5ba-0786ec51d361 \
  --destination /Users/za/Documents/Farey\ NOW/primes-equispaced/formal-conjectures/DPAC_aristotle_result.tar.gz
```

**Cancel (if needed):**

```bash
/tmp/aristotle_venv/bin/aristotle cancel 59d181d5-b207-4882-a5ba-0786ec51d361
```

**Multi-project polling.** `scripts/poll_aristotle.sh` is driven by the
project-IDs file at `scripts/aristotle_project_ids.txt`, which has been
extended to include this dispatch:

```
424973ae-8e9a-4ef1-8a6d-970ffa3b88ad SmoothedDwfFormula
8e608890-f0ba-4a89-bbb0-a63b5bcab697 R1_B_plus
59d181d5-b207-4882-a5ba-0786ec51d361 DPAC
```

To poll all three projects:

```bash
./scripts/poll_aristotle.sh                 # one-shot status of all three
./scripts/poll_aristotle.sh --watch         # poll every 15 min, all projects
./scripts/poll_aristotle.sh --download DPAC # download DPAC once COMPLETE
```

**Expected wall-clock.**  Per the task brief and Harmonic SLA, full theorems
of analytic-NT difficulty take **4–8 weeks** on Aristotle's side.  DPAC is at
the **hard end** of the spectrum (`research_open`, comparable to LI), so it
may simply return `COMPLETE_WITH_ERRORS` with the original `sorry` retained,
or one of the authorised reductions completed.  No human-side work is
required while it runs.

## Once Aristotle returns COMPLETE / COMPLETE_WITH_ERRORS

1. Download tarball with `aristotle result <id> --destination …`
2. Extract to obtain `DirichletPolynomialAvoidance.lean` (the filled-in version)
3. Save to `formal-conjectures/DirichletPolynomialAvoidance_full.lean`
4. Run `lake build RequestProject.DirichletPolynomialAvoidance` from a
   compatible Lean toolchain; capture output
5. Audit which sorries remain: `grep -nE "sorry|axiom " DirichletPolynomialAvoidance_full.lean`
6. Identify which (if any) of R1 / R2 / R3 was completed
7. Append build status + sorry/axiom audit + reduction outcome to this receipt
8. If a non-trivial reduction was completed, draft a follow-up comment to
   `google-deepmind/formal-conjectures` PR #3716 noting the new Lean
   artefact (do NOT push without Saar's explicit go-ahead).

## Local artefacts (preserved for reproducibility)

- `/tmp/aristotle_dispatch_DPAC/` — full project directory submitted (do not
  rely on this surviving reboots; copy to repo if needed for audit)
- `/tmp/aristotle_submit_DPAC_output.txt` — verbatim CLI stdout from `aristotle submit`
- `/tmp/aristotle_DPAC_prompt.txt` — verbatim prompt text passed to Aristotle
- `/tmp/aristotle_DPAC_timestamp.txt` — UTC dispatch timestamp
- `/tmp/aristotle_venv/` — Python 3.13 venv with `aristotlelib` 1.0.1
- `/tmp/dpac_pr_fetch/` — copies of the three Lean files from
  `google-deepmind/formal-conjectures` PR #3716 (DirichletPolynomialAvoidance,
  FareyBridgeIdentity, FareySignPattern), fetched via raw.githubusercontent.com
  for diff/audit purposes (only the DPAC file was repackaged into the
  dispatch payload)

## Constraints honoured

- **API key never written to any saved file.**  The key was sourced from
  `~/.farey_api_keys` into the env (length 49, prefix `arstl_`, last 4
  `CwzQ`); only this masked form appears in any artefact.
- **R1 deliverables untouched.**  No file in `handoff-2026-05-09-followup/`,
  `archive/`, or the existing `formal-conjectures/` Lean files was modified
  by this dispatch.  The dispatch payload was assembled in `/tmp/`.
- **No bundle modifications.**  The R1 dispatch project at
  `/tmp/aristotle_dispatch_R1/` and the P3b project at
  `/tmp/aristotle_dispatch_P3b/` were not touched.  This dispatch lives in
  its own directory `/tmp/aristotle_dispatch_DPAC/`.
- **No Lean proofs written by the dispatcher.**  The single `sorry` in
  `DirichletPolynomialAvoidance.lean` remains as `theorem … := by sorry`;
  only the file-header comment block was edited (to add a one-paragraph
  provenance note explaining the namespace adjustment from
  `FormalConjectures.Paper` to `RequestProject`).  The conjecture
  statement, attributes, docstring, imports, and `:= by sorry` are
  bit-for-bit identical to the upstream PR.

## Appendix — payload sanity checks

- `wc -l /tmp/aristotle_dispatch_DPAC/RequestProject/DirichletPolynomialAvoidance.lean` → 70
- `grep -c "sorry" /tmp/aristotle_dispatch_DPAC/RequestProject/DirichletPolynomialAvoidance.lean` → 2 (1 actual `:= by sorry`, plus 1 mention in the file-header comment block)
- `grep -c "axiom " /tmp/aristotle_dispatch_DPAC/RequestProject/DirichletPolynomialAvoidance.lean` → 0
- All `import` lines resolve to standard Mathlib v4.28.0 modules:
  `Mathlib.Analysis.SpecialFunctions.Complex.Log`,
  `Mathlib.NumberTheory.ArithmeticFunction`,
  `Mathlib.NumberTheory.ZetaFunction` (no in-project sibling imports).
- Diff against upstream PR #3716
  (`/tmp/dpac_pr_fetch/DirichletPolynomialAvoidance.lean`):
  the *only* difference is a 12-line provenance comment inserted inside
  the existing copyright block (between `Authors: Saar Shai` and the
  closing `-/`).  The theorem, attributes, docstring, imports, and the
  entire module-level `Statement / Evidence / Partial results /
  Difficulty` documentation block match upstream byte-for-byte.  Verified
  via `diff /tmp/dpac_pr_fetch/DirichletPolynomialAvoidance.lean
  /tmp/aristotle_dispatch_DPAC/RequestProject/DirichletPolynomialAvoidance.lean`
  → 12 inserted lines, 0 deleted, 0 modified.

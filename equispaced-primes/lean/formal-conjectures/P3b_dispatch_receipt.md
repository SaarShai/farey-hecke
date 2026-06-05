---
title: "P3b / G3 — Aristotle dispatch receipt: SmoothedDwfFormula stub → full theorem"
type: dispatch-receipt
domain: research
created: 2026-05-09
sources:
  - tasks/P3b-G3-lean-smoothed-dwf.md
  - handoff-2026-05-04-theorem-B-and-C1/SmoothedDwfFormula.lean
  - handoff-2026-05-04-theorem-B-and-C1/T2_Lean_SmoothedDwf_REPORT.md
tags: [aristotle, dispatch, lean, formalization, smoothed-dwf, P3b, G3]
---

# P3b / G3 — Aristotle dispatch receipt

## Headline

**Project submitted to Aristotle.**
- **Project ID:** `424973ae-8e9a-4ef1-8a6d-970ffa3b88ad`
- **Status at dispatch:** `QUEUED`
- **Dispatched at (UTC):** `2026-05-09T18:35:17Z`
- **Mode:** asynchronous (no `--wait`).  Lean output is **not yet available**;
  poll for completion (instructions below).

## API contract used

| Item | Value |
|---|---|
| Service | Harmonic Aristotle (cloud Lean theorem prover) |
| Base URL | `https://aristotle.harmonic.fun/api/v2` |
| Auth | `Authorization: Bearer $ARISTOTLE_API_KEY` |
| Client | `aristotlelib` 1.0.1 (PyPI), Python 3.13 venv at `/tmp/aristotle_venv/` |
| CLI invoked | `aristotle submit "..." --project-dir /tmp/aristotle_dispatch_p3b` |
| API key source | `~/.farey_api_keys` (env var `ARISTOTLE_API_KEY`) |

The base URL was extracted directly from the SDK source
(`/private/tmp/aristotle_venv/lib/python3.13/site-packages/aristotlelib/api_request.py`
line `BASE_URL = f"https://aristotle.harmonic.fun/api/v{API_VERSION}"` with
`API_VERSION = "2"`).  Endpoints used internally include `POST /projects`,
`GET /projects`, `GET /projects/{id}`, and a result-download endpoint.

## What changed since the T2 report (2026-05-04)

The prior `T2_Lean_SmoothedDwf_REPORT.md` (confidence 0.92) explicitly noted:

> Aristotle is, as of this session, only available via the interactive web
> UI. There is no public REST endpoint I could use to dispatch each lemma
> programmatically.

This is **no longer true.**  As of `aristotlelib` 1.0.1 (Apr 7 2026), Harmonic
publishes a Python SDK and CLI that wraps the `https://aristotle.harmonic.fun/api/v2`
REST surface.  Auth is via the same `ARISTOTLE_API_KEY` token used in the
interactive UI; keys are generated at Dashboard → API Keys.  The CLI commands
are `submit`, `formalize`, `result`, `list`, `cancel`.

Therefore: this dispatch is the **first programmatic Aristotle call** in
this project's history.  Outcome is unknown until the project completes.

## Payload summary (what Aristotle is working on)

**Project directory:** `/tmp/aristotle_dispatch_p3b/` (uploaded, 1623 lines total)

| File | LOC | MD5 | Role |
|---|---:|---|---|
| `lakefile.toml` | 11 | `d3ae68ec…83bc` | Lake project config (Mathlib v4.28.0) |
| `lean-toolchain` | 1 | `b8b2923c…83b7` | `leanprover/lean4:v4.28.0` |
| `RequestProject/SmoothedDwfFormula.lean` | 398 | `0214f595…47e0` | **Target file** — 7 `sorry`s to fill |
| `Smoothed_Dwf_publishable.md` | 604 | `3393a2d0…3265` | Math reference (proof in §X.4 steps 1-5) |
| `Smoothed_Dwf_explicit_formula_VERIFIED.md` | 380 | `201d75e8…ca19` | Math reference (residue calc verified) |
| `T2_Lean_SmoothedDwf_REPORT.md` | 229 | `ea2f8781…2bed` | Prior T2 report (axiom inventory + gaps) |

The 7 `sorry` targets, in source order:

| # | Lemma name | Status before | Target |
|---|---|---|---|
| 1 | `log_lin_deriv_form` | axiom | theorem (calculus) |
| 2 | `mellin_decay` | axiom | theorem (Stirling on strips) |
| 3 | `inv_zeta_polynomial_growth` | axiom | theorem (Titchmarsh §3.11) |
| 4 | `contour_shift_one_to_minus_A` | axiom | theorem (Cauchy contour, double poles) |
| 5 | `tail_bound` | axiom | theorem (Schwartz tail) |
| 6 | `smoothed_dwf_exists` | axiom | theorem (existence with R₀ = -2) |
| 7 | `main_explicit_formula` | axiom | theorem (full decomposition) |

The R₀ = -2 anchor (`R0_eq_neg_two`) is **already proved** end-to-end via
Mathlib's `riemannZeta_zero` and is preserved verbatim from the prior 373-LOC
extension.

## Prompt sent to Aristotle (verbatim)

> Fill in all sorries in RequestProject/SmoothedDwfFormula.lean. Target: a
> fully-proved Lean 4 file in Mathlib v4.28.0 (no sorry, no axiom) of the
> Smoothed Δw_f explicit formula with R₀ = -2. The R₀ = -2 anchor is already
> proven by Mathlib's riemannZeta_zero — do not regress it. The 7 sorries
> are: log_lin_deriv_form (calculus), mellin_decay (Stirling on strips for
> Schwartz Mellin transform), inv_zeta_polynomial_growth (Titchmarsh §3.11),
> contour_shift_one_to_minus_A (Cauchy contour shift with double-pole
> residues at trivial zeros of ζ), tail_bound (Schwartz N^{-A} tail bound),
> smoothed_dwf_exists (existence of a SmoothedDwfRecord with R₀ = -2), and
> main_explicit_formula (full decomposition theorem from §1.3 Theorem 1 of
> Smoothed_Dwf_publishable.md). Reference manuscripts
> Smoothed_Dwf_publishable.md (proof in §X.4 steps 1-5) and
> Smoothed_Dwf_explicit_formula_VERIFIED.md ship in the project dir alongside
> the prior T2_Lean_SmoothedDwf_REPORT.md. If a sorry truly requires Mathlib
> infrastructure absent from v4.28.0 (e.g. uniform Stirling bound on strips,
> double-pole residue calculus), leave it as sorry and add a -- TODO(aristotle):
> prerequisite <name> comment — do NOT introduce new axioms. Target ~600 LOC.
> Build target: lake build SmoothedDwfFormula returns 0.

## Aristotle's response

```
WARNING: Your project contains .lean files but no .lake folder.
Aristotle works better with access to your project's dependencies.
Did you forget to run `lake build`?

Project created: 424973ae-8e9a-4ef1-8a6d-970ffa3b88ad
```

The `.lake` warning is benign: the upload skipped the local Mathlib build
artefacts (~5 GB).  Aristotle's worker will resolve Mathlib v4.28.0 from its
own cache.

`aristotle list --limit 3` immediately after submission confirmed:

```
ID                                   STATUS    CREATED       PROGRESS
424973ae-8e9a-4ef1-8a6d-970ffa3b88ad  QUEUED   5 secs ago    -
```

## How to poll / retrieve the result

**Pre-flight (every session):**

```bash
set -a; source ~/.farey_api_keys; set +a   # loads ARISTOTLE_API_KEY
source /tmp/aristotle_venv/bin/activate    # aristotlelib 1.0.1
```

**Check status (cheap, run anytime):**

```bash
aristotle list --limit 5
# look for ID 424973ae-8e9a-4ef1-8a6d-970ffa3b88ad; status will move
# QUEUED → IN_PROGRESS → COMPLETE / COMPLETE_WITH_ERRORS / FAILED / OUT_OF_BUDGET
```

**Block until done and download the result tarball:**

```bash
aristotle result 424973ae-8e9a-4ef1-8a6d-970ffa3b88ad \
  --destination /Users/za/Documents/Farey\ NOW/primes-equispaced/formal-conjectures/SmoothedDwfFormula_aristotle_result.tar.gz
```

**Cancel (if needed):**

```bash
aristotle cancel 424973ae-8e9a-4ef1-8a6d-970ffa3b88ad
```

**Expected wall-clock.**  Per the task brief, Aristotle takes **4-8 weeks**
on ~600 LOC theorems of this analytic-NT difficulty.  Recent COMPLETE
projects in the account log range from minutes (small sorry-fills) to
multi-day (manuscript formalization).  This one is at the upper end of
sorry-fill difficulty (the `contour_shift_one_to_minus_A` sorry alone is
~300 LOC of meromorphic-residue calculus per the T2 report) but well below
"formalize a full paper" scope.

## Once Aristotle returns COMPLETE

1. Download tarball with `aristotle result <id> --destination …`
2. Extract to obtain `SmoothedDwfFormula.lean` (the filled-in version)
3. Save to `formal-conjectures/SmoothedDwfFormula_full.lean`
4. Run `lake build SmoothedDwfFormula` from this repo root; capture output
5. Verify `grep -c "sorry\|axiom" SmoothedDwfFormula_full.lean` is 0
6. Append build status + axiom audit to this receipt

## Local artefacts (preserved for reproducibility)

- `/tmp/aristotle_dispatch_p3b/` — full project directory submitted (do not
  rely on this surviving reboots; copy to repo if needed for audit)
- `/tmp/aristotle_submit_output.txt` — verbatim CLI stdout from `aristotle submit`
- `/tmp/aristotle_venv/` — Python 3.13 venv with `aristotlelib` 1.0.1

## Constraints honoured

- **API key never written to any saved file.**  The key was sourced from
  `~/.farey_api_keys` into the env (length 49, prefix `arstl__`, last 4
  `CwzQ`); only this masked form appears in any artefact.
- **No file outside `formal-conjectures/` or `handoff-2026-05-09-followup/`
  was modified.**  The original `handoff-2026-05-04-theorem-B-and-C1/`
  bundle and the task file are untouched.
- **No Lean proofs were written by the dispatcher.**  The Lean stub was
  rewritten only to convert prior `axiom` declarations into
  `theorem … := by sorry` so that Aristotle has explicit fill targets.

## Appendix — discovery trace (~15 min)

| Step | URL / cmd | Outcome |
|---|---|---|
| 1 | `WebFetch https://harmonic.fun` | Marketing site; only "Try Aristotle" → `https://aristotle.harmonic.fun/` |
| 2 | `WebFetch https://aristotle.harmonic.fun/` | Login wall; no public docs links |
| 3 | `WebSearch harmonic.fun Aristotle API documentation` | Surfaced `aristotlelib` on PyPI + `lean-aristotle-mcp` GitHub |
| 4 | `WebFetch https://pypi.org/project/aristotlelib/` | Full CLI/SDK docs, env var, install via `uv pip install` |
| 5 | `uv venv --python 3.13 /tmp/aristotle_venv` | Created Python 3.13 venv (system Python 3.9.6 too old) |
| 6 | `uv pip install aristotlelib` | Installed 1.0.1 + 12 deps |
| 7 | `aristotle list --limit 5` | API key works; account has 5 prior COMPLETE projects |
| 8 | Source-grep BASE_URL in `api_request.py` | Confirmed `https://aristotle.harmonic.fun/api/v2` |
| 9 | `aristotle submit … --project-dir /tmp/aristotle_dispatch_p3b` | Project ID `424973ae-…-3ad` returned |

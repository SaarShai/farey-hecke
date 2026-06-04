# formal-conjectures PR — readiness package (FINALIZED 2026-05-16)

Status: **cleaned, build-verified, presentable — ready pending user-only
steps.** Reframed honestly: this is **not** a "proven theorem" submission
(the pointwise Sign Theorem is false). It is a **legitimate open-conjecture
contribution** — formal-conjectures' primary category
(`@[category research open]`, stated with `sorry`). In that framing it is a
correct, clean fit.

## Deliverable

`formal_conjectures_submission/FareyDiscrepancySign.lean` — the density-one
Farey-discrepancy sign conjecture, in formal-conjectures' exact file
template:
- Apache 2.0 header ("The Formal Conjectures Authors"),
  `import FormalConjectures.Util.ProblemImports`, namespace, reference,
  `@[category research open, AMS 11]`, body `:= by sorry`.
- **Concrete** definitions (no `opaque`): `fareySet`, `fareyCount`,
  `fareyDiscrepancy`, `W` (the `∫₀¹ D_N²` Weyl L² second moment), `ΔW`,
  `mertens`, `signR/signZ`, `Agrees`. The statement therefore has genuine
  mathematical content.
- Docstring is honest: records that the **pointwise** form is *false*
  (counterexamples p=237733, 243799) and that this **density-one** form is
  the surviving open problem (≈73% at X=10⁷).

## Build verification (done — strong honest position)

`_buildcheck_FareyDiscrepancySign.lean` = same file with
`import FormalConjectures.Util.ProblemImports` → `import Mathlib` and the
FC-only attribute stripped. Compiled with the project's pinned toolchain:

```
$ lake env lean _buildcheck_FareyDiscrepancySign.lean
_buildcheck_FareyDiscrepancySign.lean:99:8: warning: declaration uses `sorry`
```

→ **Zero errors. Single expected `sorry` warning** (the open conjecture).
All definitions + the statement **typecheck against Mathlib v4.28.0**
(`leanprover/lean4:v4.28.0`). Evidence: `_buildcheck_output.txt`.

**Only unverified:** the formal-conjectures wrapper itself
(`FormalConjectures.Util.ProblemImports` import + `@[category …]`/`@[AMS …]`
attributes). These are standard packaging their repo defines; verifiable only
inside a clone of their repo via their `lake build`. Low risk, but I do **not**
claim it; the maintainers/build will confirm on PR (their CONTRIBUTING expects
`lake build` green — step 7 below).

## Honest scope (do not oversell in the issue/PR)

Specialist, Experimental-Math tier. The pointwise Sign Theorem is **false**
(stated, not hidden). The density-one form is genuinely open with numerical
evidence only. No RH claim. This is a *clean honest open conjecture*, not a
breakthrough — frame it exactly that way to the maintainers.

## WHAT I NEED FROM YOU (only you can do these)

1. **Sign the Google CLA** — https://cla.developers.google.com/ (individual;
   once per person/employer; legal; non-delegable). Tell me when done.
2. **GitHub access on this machine** — either
   `brew install gh && gh auth login`, **or** create the fork yourself
   (`SaarShai` → fork `google-deepmind/formal-conjectures`) and give me a
   way to push (auth'd `gh`, a PAT, or SSH key). Without one of these I
   cannot fork/branch/push/PR at all.
3. **Confirm GitHub handle / attribution** for the PR + file header
   (assume `SaarShai` unless you say otherwise).
4. **One choice:** definitions *inline* in the conjecture file (recommended —
   cleanest for a single conjecture review) vs. split into a
   `FormalConjecturesForMathlib` companion (their CONTRIBUTING's general
   suggestion). Default: inline.

## What I will do once 1–3 are in place (no further input needed)

5. Fork → branch `farey-discrepancy-density-one`.
6. Place file at `FormalConjectures/Other/FareyDiscrepancySign.lean` (or
   `Arxiv/` once the project note has an arXiv id), finalize the reference
   line, `lake build` in the clone, fix any FC-wrapper-only issues.
7. **Issue first** (their required sequence), then PR linked to it.

### Ready-to-paste GitHub ISSUE

> **Title:** Add open conjecture: density-one sign pattern for the prime-step
> Farey L² discrepancy (Mertens-controlled)
>
> **Body:** I'd like to contribute one `@[category research open, AMS 11]`
> conjecture. Setup: `W N` = L² (Weyl) discrepancy of the order-`N` Farey
> sequence; `ΔW p = W (p-1) − W p` the prime-step increment; `M` the Mertens
> function. The *pointwise* relation `sgn(ΔW p)=sgn(−M p)` for every prime
> with `M p ≤ −3` is **false** (explicit counterexamples). The **density-one**
> form — proportion of qualifying primes `≤ X` that agree → 1 as `X→∞` — is
> open (numerically ≈73% at `X=10⁷`; expected density-one under the
> L-function hypotheses controlling the explicit-formula expansion of `ΔW`).
> The statement uses concrete (non-opaque) Farey/discrepancy definitions and
> typechecks against Mathlib v4.28.0 (single expected `sorry`). Source:
> S. Shai, *The per-step Farey discrepancy* (2026), project `Primes-
> Equispaced`. Question for maintainers: keep the concrete Farey/discrepancy
> defs inline, or move them to `FormalConjecturesForMathlib`?

### Ready-to-paste PR body

> Closes #NN. Adds `FormalConjectures/Other/FareyDiscrepancySign.lean`: one
> `@[category research open, AMS 11]` conjecture (density-one Farey
> discrepancy sign pattern), Apache header, reference, `by sorry`. Concrete
> definitions; honest docstring (pointwise form is false, recorded). Verified
> to typecheck against Mathlib v4.28.0 outside the repo; `lake build` green
> in-repo. Google CLA signed.

## Prior context

Earlier this session I (correctly) refused to auto-submit the *original*
`FareySignPattern.lean` — it was a vacuous tautology against `opaque DeltaW`
and would have been inflation. This finalized file fixes that: concrete defs,
honest open-conjecture framing, build-verified. The contribution is now
clean. It remains user-gated solely by the CLA + GitHub access above.


## EXECUTED 2026-05-16T13:20:47-07:00
PR #3716 REWORKED & PUSHED (not new PR — existing draft had maintainer feedback).
- FareySignPattern.lean: placeholder `True := by sorry` -> concrete density-one conjecture (build-verified).
- DirichletPolynomialAvoidance.lean: kept concrete stmt; header/attrs/namespace fixed; docstring de-inflated.
- FareyBridgeIdentity.lean: REMOVED (was placeholder + over-claimed docstring).
- `lake --wfail build` Lean v4.27.0: PASSED (7983 jobs, both modules, only expected research-open sorry).
- PR title/body de-inflated; point-by-point honest reply posted to @mo271; left as DRAFT (deferring to maintainer).
- commit 657a32a on SaarShai:farey-spectroscopy-conjectures; PR https://github.com/google-deepmind/formal-conjectures/pull/3716

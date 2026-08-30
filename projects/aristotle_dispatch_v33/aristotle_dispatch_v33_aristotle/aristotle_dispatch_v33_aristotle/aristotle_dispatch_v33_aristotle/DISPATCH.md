# V33 dispatch — the LAW: statement skeleton + the divergence core

**Date:** 2026-08-22
**Slot:** `projects/aristotle_dispatch_v33/`
**Lane:** NEXT-2 (MAP entry `2026-08-23 05:00Z`), rung 1 of the LAW
formalization ladder.
**Status at authoring:** `DRAFT` → see §8 for the dispatch receipt. Every
target carries a `sorry` body and is therefore **CONJECTURAL at the Lean
level**. **This dispatch machine-verifies nothing.**

This slot touches no file outside `projects/aristotle_dispatch_v33/`. Nothing
is committed.

## 1. The LAW, and what rung 1 covers

The promoted paper-level theorem
(`research_notes/rh_goals_2026-08-14/lane_g/LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_SOL.md`,
2026-08-19 promotion block; double-audited **CONFIRMED** by
`LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_REFEREE.md` and, cold and
independently, by `LAW_SECOND_AUDIT_REFEREE.md`):

> For every finite integer `q ≥ 3`, the scalar trivial-character scattering
> determinant `φ_q` of the one-cusp Hecke triangle orbifold has infinitely
> many nonreal zeros `ρ` with `Re ρ > 1/2`, and therefore infinitely many
> multiplicity-matched scattering poles `1 - ρ` with `Re (1 - ρ) < 1/2`.

Its dependency skeleton, as the two audits reconstruct it:

| # | Ingredient | Nature | Formalizable now? |
|---|---|---|---|
| S1 | `G_q` is a one-cusp Fuchsian orbifold; `Φ` is `1×1`, so `det Φ = φ_q` | geometry / MMS + Hejhal §7 | no |
| S2 | Meromorphic continuation, `φ(s)φ(1-s) = 1`, `\|φ(1/2+it)\| ≡ 1`, finitely many real zeros in `Re s > 1/2` | FJS §2.4 / Venkov | no |
| S3 | Hejhal (7.5) generalized Dirichlet series; discreteness of the `\|c\|`-values | Hejhal §7 | no |
| S4 | Vertical polynomial bound (Hejhal Lemma 7.7) | analysis | no |
| S5 | Jensen/Littlewood rectangle `(J)` = Kelmer (4.20) = `[Sel90, Lem 1,2]` | complex analysis | no |
| S6 | Critical-line integral `(I)`, leading coefficient `1/(4π)` | calculus + `Γ`-quotient | **the calculus half: yes** |
| S7 | `F_q(1/2,T) = (1/4π) T² log T + O_q(T²)` | S5 ∘ S6 | no |
| S8 | **finiteness ⇒ `O(T)`, hence contradiction, hence infinitely many** | finite sums + real growth | **yes** |
| S9 | strictness (weight `β-1/2` vanishes on the line) | order arithmetic | **yes** |
| S10 | real zeros are finitely many ⇒ infinitely many *nonreal* | set theory | **yes** |
| S11 | reflection `ρ ↦ 1-ρ`: `Re < 1/2`, `Im ≠ 0` | complex arithmetic | **yes** |
| S12 | Kelmer's printed-constant corrections (`A = a + 2B`; `B` correction) | explicit algebra | **yes** |

**Chosen obligation for rung 1: S8–S12, plus the calculus half of S6.**

Rationale, matching the lane brief's own selection rule (arithmetic /
inequality / algebraic lemmas formalize well; analytic continuation and
spectral theory do not): S1–S5 and S7 are precisely the spectral-theoretic
and complex-analytic imports that no current Lean library supports, and any
attempt to state them would need a Lean type for `φ_q`, which does not exist
and would be a multi-dispatch project on its own. S8–S12 are the *finish* of
the proof — pure finite-sum, order and set arithmetic — and they are the part
that carries the LAW's actual logical shape ("divergent weighted count over a
would-be finite family"). They are exactly the v32-style constant/inequality
chain the template proves out.

Section 4 of the Lean file additionally machine-states the second audit's own
arithmetic findings (`LAW_SECOND_AUDIT_REFEREE.md` finding C), which were
verified only numerically there. Retiring hand numerics into Lean algebra is
free value at this rung.

## 2. Named hypotheses — the analytic content that is NOT verified

In v32's `hconv`/`hford` style, every non-formalizable input is an explicit
Lean hypothesis, never an assertion. `φ_q` has **no Lean definition** in this
dispatch; the zero family is an abstract predicate `Zero : ℂ → Prop`, and the
weighted Jensen count is an abstract `F : ℝ → ℝ`.

| Tag | Lean name | Paper content | Source | Status carried |
|---|---|---|---|---|
| H1 | `Zfin`, `hZfin` | finite truncation of the right-zero set at height `T` | bookkeeping (`§4.1`) | definitional |
| H2 | `hFdef` | the *definition* of `F_q(1/2,T)` as the weighted Jensen sum | `LAW_..._SOL.md` §4.1 | definitional |
| **H3** | `hgrowth` | `F_q(1/2,T) = (1/4π) T² log T + O_q(T²)`, lower half only | promotion block; `(J)` ∘ `(I)` | **paper-level import, NOT proved here** |
| **H4** | `hreal_finite` | only finitely many *real* zeros of `φ_q` in `Re s > 1/2` | FJS divisor item 2 / Hejhal | **literature import, NOT proved here** |
| **H5** | `hpole` | `φ(s)φ(1-s)=1` sends an order-`m` zero at `ρ` to an order-`m` pole at `1-ρ` | `(F)`, §5 | **paper-level import, NOT proved here** |

**What a completed v33 would establish, stated exactly:**

> the LAW's statement skeleton + the divergence core (targets A1–A3), the
> strictness/nonreality/reflection finish (B1–B5), the `(I)` leading-coefficient
> calculus identity (C1), and the constant corrections (D1–D4) — **conditional
> on the named hypotheses H3, H4, H5**, and saying nothing whatever about
> `φ_q`, `G_q`, scattering theory, or the truth of H3–H5.

It would **not** establish the LAW. The LAW's analytic weight lives entirely
in H3.

## 3. The ladder — 14 targets in `LawSkeletonI.lean`

Locally proved scaffolding, no `sorry`, no LAW content: `weight_pos`,
`weight_nonneg`, `mem_RightZeros_iff`.

| # | Target | Source | Difficulty |
|---|---|---|---|
| A1 | `growth_beats_quadratic_target` | promotion block ("would be only `O_q(T)`") | small |
| A2 | `finite_family_linear_bound_target` | §5 boundedness step | small |
| A3 | `law_right_zeros_infinite_target` | **§5 + promotion block — the skeleton** | assembly |
| B1 | `weight_eq_zero_iff_target` | audit attack 4a (i) | small |
| B2 | `nonreal_right_zeros_infinite_target` | §5 / attack 4b | small |
| B3 | `reflection_strict_left_target` | §5 | small |
| B4 | `reflection_nonreal_target` | §5 | small |
| B5 | `law_offline_poles_infinite_target` | **§5 — the conclusion skeleton** | assembly |
| C1 | `jensen_leading_integral_target` | §4.2 displayed identity; attack 2c | medium |
| C2 | `gamma_quotient_modulus_target` (**optional**) | §4.2 `(GT)` | large |
| D1 | `finite_difference_leading_target` | audit finding C | medium |
| D2 | `constant_A_eq_a_add_two_B_target` | audit finding C | medium |
| D3 | `corrected_A_value_target` | audit finding C | small |
| D4 | `kelmer_printed_B_ne_true_B_target` | audit finding C | small |

A1–B5 are the rung that matters. C2 is flagged optional and expected to be
the most expensive; it must not crowd out the rest.

### Statement-selection decisions

1. **Multiplicity is dropped.** The conclusions are `Set.Infinite` statements
   about sets of distinct points. The audit's confirmed conclusion is
   "infinitely many"; a multiplicity-weighted count would be *stronger* than
   confirmed for a set-level statement, so the weaker reading is taken.
2. **`(C)` is not used; the weak `O_q(T²)` form is.** The 2026-08-19
   promotion block and the second audit (attack E) both record that the
   triangular `F_q(1/2,T) = (1/4π)T²logT + O_q(T²)` route is *strictly more
   robust* than `(C)` — it needs neither the finite-difference step, nor the
   `<T` vs `≤T` convention, nor boundedness of `β`. H3 is therefore stated in
   that form, and only its lower-bound half is assumed.
3. **`A_q` is never given a formula.** The promotion block asserts only its
   existence. Section 4's `A = a + 2B` is a *general* expansion lemma about an
   abstract `F`, not a claim about `A_q`.
4. **`hgrowth` is an existential over `C`.** This is exactly `O_q(T²)` with a
   group-dependent implied constant, matching the source's deliberately
   `q`-dependent `O_q`. No `q`-uniformity is expressible here, and none is
   claimed.
5. **No arithmeticity.** Second-audit attack 5b: the "in particular,
   nonarithmetic `G_q`" clause carries **zero** arithmeticity information
   (`q = 3` has the same property, with a positive proportion of poles at
   `Re s = 1/4`). The Lean file mentions arithmeticity nowhere, and the
   LEDGER RULE block forbids reusing it as an arithmeticity signature.
6. **D4 is stated as a disequality on purpose.** Making "do not consume
   Kelmer's printed `B_Γ`" a machine-checked fact is cheaper than a prose
   warning that a later session can miss.

## 4. FALSE-statement escape hatch

Same convention as v30/v32. If a target is false, do not force an
inconsistent proof: keep the original inside a `FALSE AS STATED` comment,
prove `<target>_false` with an exact witness, then state and prove the
weakest corrected theorem and report the downstream status change.

## 5. Deliberate exclusions

This dispatch does not encode or claim:

* any Lean definition of `φ_q`, `Φ`, `L_q^*`, `G_q`, `M_q`, or a scattering
  determinant of any kind;
* the meromorphic continuation, the functional equation, unitarity on the
  critical line, or the 7-item divisor (S2);
* Hejhal's (7.5) series, the discreteness of its `|c|`-values, or Lemma 7.7
  (S3, S4);
* the Jensen/Littlewood rectangle `(J)` / Kelmer (4.20) / `[Sel90, Lem 1,2]`
  (S5) — the residual dependency the second audit could not discharge, since
  no one in the lineage has read Selberg 1990;
* the full critical-line integral `(I)` — only its elementary displayed
  identity (C1) and, optionally, the `Γ`-quotient modulus (C2) are requested;
* the sharp `(C)` asymptotic;
* any `q`-uniform error, any effective first height, any `A_q`/`B_q`/`C_q`
  value for the actual orbifold;
* every open item of the *other* LAW lane (`LAW_MINIMAL_HYPOTHESES.md`): U1-min,
  the corridor hypothesis, the Vitali–Porter continuation. Those belong to the
  deformation route and are untouched here.

All of these remain paper-level or **OPEN**, exactly as the audits leave them.

## 6. Exact local syntax receipt

Pre-check run against the v26 cache; no `.lake` directory is created inside
`v33`.

Command:

```bash
( cd /Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle && \
  ~/.elan/bin/lake env lean \
  /Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v33/LawSkeletonI.lean ); echo "exit=$?"
```

Verbatim output:

```text
/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v33/LawSkeletonI.lean:116:8: warning: declaration uses `sorry`
/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v33/LawSkeletonI.lean:128:8: warning: declaration uses `sorry`
/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v33/LawSkeletonI.lean:154:8: warning: declaration uses `sorry`
/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v33/LawSkeletonI.lean:176:8: warning: declaration uses `sorry`
/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v33/LawSkeletonI.lean:186:8: warning: declaration uses `sorry`
/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v33/LawSkeletonI.lean:199:8: warning: declaration uses `sorry`
/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v33/LawSkeletonI.lean:204:8: warning: declaration uses `sorry`
/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v33/LawSkeletonI.lean:217:8: warning: declaration uses `sorry`
/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v33/LawSkeletonI.lean:237:8: warning: declaration uses `sorry`
/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v33/LawSkeletonI.lean:250:8: warning: declaration uses `sorry`
/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v33/LawSkeletonI.lean:270:8: warning: declaration uses `sorry`
/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v33/LawSkeletonI.lean:284:8: warning: declaration uses `sorry`
/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v33/LawSkeletonI.lean:298:8: warning: declaration uses `sorry`
/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v33/LawSkeletonI.lean:309:8: warning: declaration uses `sorry`
exit=0
```

No errors, no lint warnings. The fourteen `sorry` warnings are exactly the
fourteen dispatch targets of §3.

## 7. Independent statement audit before submission

Hand-check of each target against its source, plus float corroboration where
an identity has a numeric value. Repeat these:

* **A1** is true because `a T² log T - C T² - M T = T (a T log T - C T - M)`
  and `a log T → ∞`.
* **A2** is true termwise: `|Im ρ| ≤ T` gives `T - |Im ρ| ≥ 0`, so each term
  is `≤ T · w ρ`, and dropping `S \ S'` only removes nonnegative terms.
* **A3** is the composition: `RightZeros` finite ⇒ `Zfin T ⊆ S` for all `T`
  ⇒ `F T ≤ M T` by A2 ⇒ contradiction with `hgrowth` by A1 at
  `a = 1/(4π) > 0`. The weights are nonnegative on `S` because membership
  forces `Re ρ > 1/2`.
* **C1** float check of `2∫₀^T (T-t) log t dt` vs `T² log T - (3/2)T²`
  (2·10⁶-point Riemann sum): `T=0.5: -0.548285` vs `-0.548287`;
  `T=1: -1.499992` vs `-1.5`; `T=3: -3.612421` vs `-3.612489`;
  `T=10: 80.259211` vs `80.258509`. Closed form re-derived by hand:
  `∫₀^T (T-t)log t = ½T²log T - ¾T²`.
* **D1** the bracketed quantity equals `log T + 3/2 + O(1/T)`; the ratio to
  `1 + log T` measured `1.773, 1.383, 1.161, 1.090, 1.049` at
  `T = 1, 2, 10, 100, 10⁴`, so `c = 2` is a valid witness. The statement is
  existential in `c`, so it is robust.
* **D2** follows from D1 plus `B((T+1)² - T²) = 2BT + B` and
  `D(T+1) - D T = D`: the linear coefficient `D` cancels, leaving
  `(a + 2B) T`, which is the audit's `A = a + 2B`.
* **D3** exact algebra: `1/(4π) + (-2logπ-3)/(4π) = -(2 + 2logπ)/(4π)`.
  Float: both sides `-0.34134436292984843`, and the audit records this equals
  the Riemann–von Mangoldt value at `q = 3` to 12 digits.
* **D4** the two numerators agree iff `-4logπ - 1 = -2logπ - 3` iff
  `logπ = 1` iff `π = e`; false.
* **B1–B5** are elementary; B2 is "infinite minus finite is infinite".

## 8. Dispatch receipt

Credentials were sourced from `~/.farey_api_keys` without printing; every CLI
stream was sanitized through `grep -iv key`.

```bash
export $(grep -o 'ARISTOTLE_API_KEY=[^ ]*' ~/.farey_api_keys | head -1)
~/.local/bin/aristotle submit \
  --project-dir /Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v33 \
  '<prompt below>' 2>&1 | grep -iv key
```

Prompt sent (verbatim):

> Prove the targets in LawSkeletonI.lean. Partial credit is wanted: prove as
> many rungs as possible rather than only attempting the assemblies. Suggested
> order: A1 growth_beats_quadratic_target, A2
> finite_family_linear_bound_target, then B1-B4 (elementary), then A3
> law_right_zeros_infinite_target and B5 law_offline_poles_infinite_target
> which are the two assembly targets, then D3, D4, D1, D2, then C1
> jensen_leading_integral_target. C2 gamma_quotient_modulus_target is OPTIONAL
> and expected to be the most expensive - attempt it only after the others.
> Do not weaken or strengthen any statement, and do not remove or relax any
> hypothesis. Do NOT attempt to prove the named hypotheses hgrowth, hreal_finite
> or hpole - they are deliberate paper-level imports from the scattering
> literature and must remain hypotheses. If a target is false, use the FALSE AS
> STATED escape hatch documented in the file header: give a counterexample and
> the weakest corrected theorem. Return Lean source suitable for an independent
> rebuild against a Mathlib cache; introduce no axioms and leave no sorrys in
> any result you claim proved.

**Receipt:**

| field | value |
|---|---|
| submitted | 2026-08-22 |
| project id | `a4a17b62-84c6-4b7f-8e50-a2d1feee9dfc` |
| project name | `aristotle_dispatch_v33` |
| status at submit | `RUNNING` |
| CLI | `~/.local/bin/aristotle` (aristotlelib 2.0.0), verb `submit`, not `--wait` |

Poll and download:

```bash
export $(grep -o 'ARISTOTLE_API_KEY=[^ ]*' ~/.farey_api_keys | head -1)
~/.local/bin/aristotle show a4a17b62-84c6-4b7f-8e50-a2d1feee9dfc 2>&1 | grep -iv key
~/.local/bin/aristotle download a4a17b62-84c6-4b7f-8e50-a2d1feee9dfc \
  --destination /Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v33/result 2>&1 | grep -iv key
```

## 9. Harvest and independent rebuild (for whoever collects)

Harvest only Lean source and non-cache metadata under `result/`; exclude
`.lake`, caches, worktrees and archives. The collector must independently run
the returned source against the v26 cache, quote the exact exit output, grep
the returned source for real `sorry` and `axiom` declarations, stream
`#print axioms` for every target, and record each as `PROVED`, `REFUTED` or
still `OPEN`. Diff statements target-by-target against this file: a returned
theorem with a weakened hypothesis or a strengthened conclusion is a defect,
not a win — in particular any returned file in which `hgrowth`, `hreal_finite`
or `hpole` has been discharged or dropped is a defect. No promotion until the
rebuild succeeds **and** a cold adversarial `V33_REFEREE.md` has reviewed the
proof-status upgrade.

**Ledger wording for any future harvest, and no stronger:** *"statement
skeleton of the LAW plus the divergence-core, strictness, nonreality and
reflection lemmas, machine-verified conditional on the named hypotheses H3
(Jensen growth `O_q(T²)`), H4 (finitely many real right zeros) and H5
(functional-equation pole reflection); no scattering-theoretic content is
machine-verified."*

## 10. Verification checklist

```text
( cd /Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle && \
  ~/.elan/bin/lake env lean \
  /Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v33/LawSkeletonI.lean )
rg -n "sorry|axiom|CONJECTURAL|paper-level|escape" projects/aristotle_dispatch_v33
find projects/aristotle_dispatch_v33 -name '.lake' -o -name '*.olean'
git diff --check -- projects/aristotle_dispatch_v33
rg -n -i "api[_-]?key|authorization|bearer|token" projects/aristotle_dispatch_v33
```

The secret scan must print only names and locations, never values. Any
key-like value in output or in a written file is a hard failure.

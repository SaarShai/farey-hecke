# V29 dispatch note — sharp no-wrap law + Route-B algebra

**Status:** DRAFT FOR ARISTOTLE. Every theorem in `RateCoreIV.lean` has a live
`sorry`; none is claimed machine-proved by this dispatch. At the Lean level the
targets remain **OPEN / CONJECTURAL UNTIL HARVEST**. The sharp no-wrap theorem
and Route-B algebra carry paper/referee confirmation as source status, not as a
substitute for a sorry-free rebuild. The global localization and RATE claims
remain CONJECTURAL or FALSE exactly as their source notes state.

## Sources and carried status

- `research_notes/rh_goals_2026-08-14/lane_g/M2_LOCALIZATION_THEOREM_SOL.md`
  §0 states the sharp finite law at lines 13–37; §3 gives the continuant proof
  and equality cases at lines 484–587. Its global localization laws `(LOC_0)`,
  `(LOC)`, and `(LOC_mu)` are CONJECTURAL, while unrestricted raw-depth growth
  and the stated global positive-majorant targets are FALSE.
- `research_notes/rh_goals_2026-08-14/lane_g/M1_LOCALIZATION_TRIPLE_REFEREE.md`
  §2.1, lines 223–280, finds no counterexample and adjudicates the sharp sine
  envelope TRUE after one mandatory repair: before the subtract-branch bound,
  prove
  `lambda*|n| >= lambda > 1/p >= 1/|r|`. It also corrects the all-`-1`
  equality to `K_j = (-1)^j u_j`, so equality is for `|c|`.
- `research_notes/rh_goals_2026-08-14/lane_g/M1_ROUTE_B_REPAIR_SOL.md`
  lines 285–320 and 508–556 prove at paper level the `SL` signs
  `Q^2 = R^q = -I` and the four boundary-cancellation cases. The triple
  referee independently confirms those pieces at lines 33–92 and 136–175.
  This does not close the source's CONJECTURAL RATE-strength
  `O(q^{1-2*sigma})` target.
- The harvested v26 theorem
  `projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle/RateCore.lean:332-340`
  already proves `c = lambda * U_{m-1}(lambda/2)` sorry-free. Its exact public
  signature is copied into v29 because the dispatch remains standalone with
  only `import Mathlib`; v29 does not depend on another submitted file.

## Exact conventions

`Qmat`, `Spow`, `wordMatrix`, `depth`, and `c` are copied verbatim from
`projects/aristotle_dispatch_v27/RateCoreII.lean:45-63`:

- `[n_1, ..., n_{k-1}]` encodes
  `Q S^{n_1} Q ... S^{n_{k-1}} Q`;
- `wordMatrix [] = Qmat`;
- `depth w = w.length + 1` counts `Q` letters;
- `c` is matrix entry `(1, 0)`, the lower-left entry, so `c lambda [] = lambda`.

`SyntacticallyReduced w` is the missing explicit raw-syntax predicate:
`forall n in w, n != 0`. It does not mean free-product depth, a globally
minimal representative, or minimal double-coset depth.

## Obligations

| Lean name | Scope | Status carried into v29 |
|---|---|---|
| `c_eq_lam_mul_continuant` | `c_w(lambda) = lambda K(w)` for the negative continuant | algebra identity REFEREE-CONFIRMED; local Lean target OPEN |
| `subtract_branch_magnitude_ordering` | the omitted chain `lambda|n| >= lambda > 1/p >= 1/|r|` | mandatory referee repair; local Lean target OPEN |
| `subtract_branch_lower_bound` | reverse-triangle consequence after the ordering lemma | referee repair; must use the preceding lemma; local Lean target OPEN |
| `sharp_no_wrap` | `|c_w(lambda_N)| >= lambda_N sin(k pi/N)/sin(pi/N)` for syntactically reduced `w`, `depth w = k`, `1 <= k <= N-1` | PAPER/REFEREE CONFIRMED; local Lean target OPEN |
| `c_chebyshevWord` | `c = lambda U_{m-1}(lambda/2)` for the all-`+1` word | MACHINE-VERIFIED in harvested v26; standalone v29 copy has live `sorry` |
| `c_negativeChebyshevWord_sign` | all-`-1` signed value is `(-1)^(m-1)` times the all-`+1` value | referee sign repair; local Lean target OPEN |
| `sharp_no_wrap_eq_chebyshev_words` | both `eps = +1` and `eps = -1` attain the sharp absolute-value envelope | PAPER/REFEREE CONFIRMED; local Lean target OPEN |
| `Qmat_sq_neg_one` | exact `SL` lift identity `Q^2 = -I` for `lambda != 0` | ROUTE-B PAPER/REFEREE CONFIRMED; local Lean target OPEN |
| `Rmat_pow_lamN_neg_one` | exact `SL` lift identity `(QS)^N = -I` at `lambda_N` | ROUTE-B PAPER/REFEREE CONFIRMED; local Lean target OPEN |
| `four_sign_boundary_cancellation` | reduced tagged-syllable lists remain reduced in all four boundary sign cases; the middle sublist is literal and unchanged | ROUTE-B PAPER/REFEREE CONFIRMED; bounded list-algebra Lean target OPEN |

## Deliberate exclusions

- No unrestricted raw-depth lower bound. The sine envelope turns over and
  vanishes at the elliptic relation.
- No `(LOC_0)`, `(LOC)`, `(LOC_mu)`, global matched-section, weighted-count,
  or RATE theorem. Those remain CONJECTURAL; the stronger positive-majorant
  assertions identified in M2 are FALSE.
- No identification of raw `Q,S` depth with free-product syllable depth or
  minimal double-coset depth.
- No PSL quotient or group-presentation theorem is invented. The two matrix
  theorems retain the `SL` sign `-I`; projective relations are mentioned only
  in docstrings as source context.
- The four-sign target is exactly the finite tagged-`List` algebra. It assumes
  a reduced core and endpoint exclusions, proves all four boundary splices
  reduced, and does not claim canonical-section existence or RATE support.
- No v26 c-only word-injectivity axiom is revived; v27 machine-refuted that
  proxy at depth three.

## FALSE-statement escape hatch

Follow the harvested v26 pattern and the explicit v27/v28 rule. If a target is
FALSE as stated:

1. retain the original only in a `FALSE AS STATED` comment;
2. prove `<target>_false` as its negation with an exact witness;
3. state and prove the weakest corrected `<target>'` theorem;
4. report the downstream status change rather than forcing the original.

## Local syntax receipt

Run against the reachable v26 harvested cache. Do not copy, create, edit, or
commit any `.lake` directory.

Final command, run 2026-08-18 from the repository root:

```text
$ ( cd projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle && ~/.elan/bin/lake env lean ../../../aristotle_dispatch_v29/RateCoreIV.lean )
../../../aristotle_dispatch_v29/RateCoreIV.lean:91:8: warning: declaration uses `sorry`
../../../aristotle_dispatch_v29/RateCoreIV.lean:105:8: warning: declaration uses `sorry`
../../../aristotle_dispatch_v29/RateCoreIV.lean:119:8: warning: declaration uses `sorry`
../../../aristotle_dispatch_v29/RateCoreIV.lean:136:8: warning: declaration uses `sorry`
../../../aristotle_dispatch_v29/RateCoreIV.lean:162:8: warning: declaration uses `sorry`
../../../aristotle_dispatch_v29/RateCoreIV.lean:174:8: warning: declaration uses `sorry`
../../../aristotle_dispatch_v29/RateCoreIV.lean:186:8: warning: declaration uses `sorry`
../../../aristotle_dispatch_v29/RateCoreIV.lean:206:8: warning: declaration uses `sorry`
../../../aristotle_dispatch_v29/RateCoreIV.lean:217:8: warning: declaration uses `sorry`
../../../aristotle_dispatch_v29/RateCoreIV.lean:264:8: warning: declaration uses `sorry`
[exit 0]
```

Verdict: syntax/type-check PASSED. The ten warnings are exactly the ten live
dispatch obligations. No theorem in v29 is promoted to machine-verified until
Aristotle returns a sorry-free file and an independent rebuild succeeds.

`.lake` non-creation receipt:

```text
$ find projects/aristotle_dispatch_v29 -type d -name .lake -print
(no output; exit 0)
```

## DISPATCHED 2026-08-18

Project `59877996-ccc8-4a0d-ae21-94baf065ea94`. Orchestrator re-ran the
syntax pre-check pre-submission (exit 0, 10 sorry-only warnings). Prompt
includes the FALSE-statement escape hatch, the magnitude-ordering lemma
emphasis, and the (−1)^j equality-case sign. Harvest on completion.

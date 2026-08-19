# V30 dispatch — finite `(FW)` renewal arithmetic and typed `(AM)` coding

**Date:** 2026-08-19  
**Status at authoring:** `DRAFT FOR ARISTOTLE`; local syntax passed against the
v26 cache. The paper-level `(FW)` and `(AM)` theorems remain **CONJECTURAL at
the Lean level**. No full analytic counting, canonical-section, or operator
claim is called machine-verified by this dispatch.

## Scope and source ledger

This dispatch formalizes only finite data/algebra that can be stated honestly
in Lean:

| Target | Lean scope | Carried paper/source status |
|---|---|---|
| `fw_product_gain` | ordered-ring implication from `2(n-2)AB <= Y`, `n >= 4`, `A,B >= 0` to `nAB <= Y` | `(FW)` overflow factorization and Ford count are paper-level **PROVED** in `FW_RENEWAL_COUNT_SOL.md:195-465`; this finite implication is not the full theorem |
| `fw_product_mono` | positive-integer relaxation `nrs <= Y -> rs <= Y` | finite algebra only; no multiplicity or Ford bound |
| `atomOfTag_atomTag`, `modeOfTag_modeTag`, `statusOfTag_statusTag`, `signedNat_decode` | constructor/tag and signed-payload parser scaffolding | local Lean proofs |
| `marked_code_source_injective_target` | injectivity of the explicit typed serialization on `WellFormed` codes | source marked-code injectivity **CONFIRMED at paper level** by `AM_REFEREE.md` and `TWOMARK_REFEREE.md`; this Lean theorem is a live dispatch target |
| `decode_encode_target` | executable round-trip of the finite-list serialization | local serialization target; no claim that it inverts the full source-table encoder |
| `marked_code_product_gain_target` | list-size consequences of the typed code bounds | local Lean proof; no analytic product-gain estimate |

The `(FW)` source is `research_notes/rh_goals_2026-08-14/lane_g/FW_RENEWAL_COUNT_SOL.md`:
equations (1.11)--(1.15) give the affine overflow entry and product gain, while
(1.16)--(1.20) add the prefix/suffix multiplicity and harmonic summation. The
current file formalizes the ordered-ring/product portion only.

The `(AM)` source is `ATOM_MOMENT_BRIDGE_SOL.md:80-265`, with the marked
branch tables in `TWOMARK_RENEWAL_SOL.md:440-590`. The typed `MarkedCode`
records:

* `MarkMode.one`/`.two`;
* four explicit atom constructors (`heavyPos`, `heavyNeg`, `unitPos`,
  `unitNeg`);
* `BoundaryStatus.bridge`, `.absorbLeft`, `.absorbRight`, `.split`, and
  `.coupled`;
* endpoint-normalized `Core` bodies and removed unit-run lengths;
* up to three stored cores, four auxiliary gains, and two heavy magnitudes as
  explicit lists, with those source bounds stated by `WellFormed`.

## Deliberate exclusions

This dispatch does not encode or claim:

* the canonical `R^{a_0} Q ... Q R^{a_k}` normal-form theorem;
* the theta image characterization or Ford counting;
* the full `(FW)` estimate
  `A_wrap,q(Y) <= 128(1+log 2) Y^2/q (1+log_+(Y/q))`;
* the endpoint-core population bound, the source Lemma 4.1 branch coverage, or
  the `(AM)` atom-moment estimate with constant `2^63`/`2^100`;
* a full source-table decoder theorem, machine verification of `(RATE-A)`, or
  the analytic operator tails.

All such statements remain paper-level or **CONJECTURAL at the Lean level**
until a returned source is independently rebuilt and audited for `sorry`s and
nonstandard axioms.

## FALSE-statement escape hatch

If Aristotle finds a requested target false, it must not force an inconsistent
proof. Retain the original only inside a `FALSE AS STATED` comment, prove a
named `<target>_false` negation with an exact witness, then state and prove the
weakest corrected theorem and report the downstream status change.

## Exact local syntax receipt

The precheck was run against the v26 cache, not a fresh dependency environment:

```text
$ ( cd /Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle && ~/.elan/bin/lake env lean /Users/za/Documents/farey-hecke/.worktrees/rate-v30-20260819/projects/aristotle_dispatch_v30/RateCoreV.lean )
/Users/za/Documents/farey-hecke/.worktrees/rate-v30-20260819/projects/aristotle_dispatch_v30/RateCoreV.lean:259:26: warning: This simp argument is unused: Int.not_le
/Users/za/Documents/farey-hecke/.worktrees/rate-v30-20260819/projects/aristotle_dispatch_v30/RateCoreV.lean:259:38: warning: This simp argument is unused: not_false_eq_true
/Users/za/Documents/farey-hecke/.worktrees/rate-v30-20260819/projects/aristotle_dispatch_v30/RateCoreV.lean:259:57: warning: This simp argument is unused: reduceIte
/Users/za/Documents/farey-hecke/.worktrees/rate-v30-20260819/projects/aristotle_dispatch_v30/RateCoreV.lean:266:8: warning: declaration uses `sorry`
/Users/za/Documents/farey-hecke/.worktrees/rate-v30-20260819/projects/aristotle_dispatch_v30/RateCoreV.lean:272:8: warning: declaration uses `sorry`
exit=0
```

The three unused-simp diagnostics are harmless lint warnings. The two
`sorry` warnings are the explicitly marked Aristotle targets; they are not
machine-verified claims. No `.lake` directory is created in v30 by this
precheck.

## Dispatch command and receipt

Credential loading uses `~/.farey_api_keys` as a sourceable file without
printing its contents. Every CLI stream is sanitized through `grep -iv key`.

```bash
set -a
source ~/.farey_api_keys
set +a
aristotle submit \
  --project-dir /Users/za/Documents/farey-hecke/.worktrees/rate-v30-20260819/projects/aristotle_dispatch_v30 \
  'Prove the honest finite targets in RateCoreV.lean. Prioritize fw_product_gain, fw_product_mono, the typed AtomKind/MarkMode/BoundaryStatus/ Core/MarkedCode serialization scaffolding, marked_code_source_injective_target, and decode_encode_target. Do not claim the full analytic FW or AM theorem. If a target is false, use the FALSE AS STATED escape hatch: give a counterexample and weakest corrected theorem. Return Lean source suitable for an independent v26-cache rebuild; do not introduce axioms or leave sorrys in proved results.' \
  2>&1 | grep -iv key
```

**Project id/status:** `PENDING DISPATCH RECEIPT` at authoring. The
orchestrator must append the sanitized command output, project id, and status
here after submission. If credentials or the service are unavailable, append
the exact sanitized blocker instead and leave status `BLOCKED / OPEN`.

## Harvest and independent rebuild

No Aristotle result is present at authoring. If a result lands, harvest only
Lean source and non-cache metadata under `result/`; exclude `.lake`, caches,
worktrees, and archives. The orchestrator must independently run the returned
source against the v26 cache, quote the exact exit output, search the returned
source for actual `sorry` and `axiom` declarations, and record whether the
result is `PROVED`, `REFUTED`, or still `OPEN`. A returned file is not promoted
until this independent rebuild succeeds and the corresponding adversarial
referee has reviewed any proof-status upgrade.

## Verification checklist

From the isolated worktree:

```text
git status --short --branch
( cd /Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle && ~/.elan/bin/lake env lean /Users/za/Documents/farey-hecke/.worktrees/rate-v30-20260819/projects/aristotle_dispatch_v30/RateCoreV.lean )
rg -n "sorry|axiom|CONJECTURAL|paper-level|escape" projects/aristotle_dispatch_v30
git diff --check -- projects/aristotle_dispatch_v30
```

The secret scan must print only names/locations (never values), for example:

```text
rg -n -i "api[_-]?key|authorization|bearer|token" projects/aristotle_dispatch_v30
```

Any key-like value in output or written files is a hard failure.

## HARVEST 2026-08-19

Returned source: `RateCoreV.lean` (single file, unchanged interface). Status of
the requested targets:

| Target | Status in returned source |
|---|---|
| `fw_product_gain` | PROVED (was already proved in the dispatch draft) |
| `fw_product_mono` | PROVED (already proved in the draft) |
| `atomOfTag_atomTag`, `modeOfTag_modeTag`, `statusOfTag_statusTag`, `signedNat_decode` | PROVED (`signedNat_decode` cleaned of three unused `simp` arguments, removing the lint warnings quoted in the syntax receipt) |
| `decode_encode_target` | PROVED, `sorry` removed |
| `marked_code_source_injective_target` | PROVED, `sorry` removed |
| `marked_code_product_gain_target` | PROVED (already proved in the draft) |

No target was found false, so the `FALSE AS STATED` escape hatch was not used
and no statement was weakened. All original statements are retained verbatim.

New supporting material added (all locally proved, no axioms, no `sorry`):
`takeNatList_append`, `takeNatList_self`, `signedNat_length`,
`flatMap_signedNat_length`, `decodeDigits_flatMap`, `decodeCore_append`,
`decodeCores_append`, plus the unconditional strengthening `encode_injective`
(`Function.Injective encode` on all of `MarkedCode`, from which the
`WellFormed`-hypothesised target follows; the `WellFormed` hypotheses are kept
in the requested statement but are not needed). Three `#guard` checks pin the
concrete wire format and the rejection of a bad header tag.

Nothing analytic is claimed: the paper-level `(FW)` estimate, Ford counting,
canonical normal form, source-table coverage, and the `(AM)` atom-moment bound
remain **CONJECTURAL at the Lean level**.

Axiom audit of the returned source (`#print axioms`):

```text
'RateCoreV.fw_product_gain' depends on axioms: [propext, Classical.choice, Quot.sound]
'RateCoreV.fw_product_mono' depends on axioms: [propext]
'RateCoreV.decode_encode_target' depends on axioms: [propext, Quot.sound]
'RateCoreV.marked_code_source_injective_target' depends on axioms: [propext, Quot.sound]
'RateCoreV.encode_injective' depends on axioms: [propext, Quot.sound]
'RateCoreV.marked_code_product_gain_target' does not depend on any axioms
```

Only the standard Lean axioms occur; the file declares no `axiom` and contains
no `sorry`. The build is warning-free.

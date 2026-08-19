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

**Post-submit local recheck (2026-08-19):** the only source change after the
upload removed those three unused-simp arguments; the theorem interfaces and
the two deliberate dispatch targets are unchanged. Against the same v26 cache:

```text
/Users/za/Documents/farey-hecke/.worktrees/rate-v30-20260819/projects/aristotle_dispatch_v30/RateCoreV.lean:265:8: warning: declaration uses `sorry`
/Users/za/Documents/farey-hecke/.worktrees/rate-v30-20260819/projects/aristotle_dispatch_v30/RateCoreV.lean:271:8: warning: declaration uses `sorry`
syntax_exit=0
```

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

**Dispatch receipt (2026-08-19, sanitized):**

```text
WARNING: Your project contains .lean files but no lean-toolchain is present.
Aristotle works best with Lean Toolchain leanprover/lean4:v4.28.0

WARNING: Your project contains .lean files but no .lake folder.
Aristotle works better with access to your project's dependencies.
Did you forget to run `lake build`?

Project created: 97b16c1b-653d-42b9-a5da-4ed765a8eb88
exit=0
```

Project `97b16c1b-653d-42b9-a5da-4ed765a8eb88`, task
`768f5d6f-6b5c-4516-981b-6d8f967b6a6b`: **RUNNING / OPEN**. The warnings are
about Aristotle's upload environment; the required local syntax gate was
already run against the v26 cache above. The bounded watcher was interrupted
after a progress receipt rather than claiming completion:

```text
Task: 768f5d6f-6b5c-4516-981b-6d8f967b6a6b
Project: 97b16c1b-653d-42b9-a5da-4ed765a8eb88
THINKING: I'll start by exploring the project.
RUNNING_COMMAND: `find /workspace/request-project -name "*.lean" | head -50; echo ---; ls /workspace/request-project`
READING_FILES: Read /workspace/request-project/RateCoreV.lean
exit=124
```

The `exit=124` is the local bounded `timeout` on the watcher, not a project
failure. The project remains running/open for later harvest.

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

Project `97b16c1b-653d-42b9-a5da-4ed765a8eb88` remains **RUNNING / OPEN** at the
bounded dispatch window. No returned source is present, so no harvest or
independent rebuild is claimed. The orchestrator should poll later and append
the result, if any, under this dated block.

Latest bounded watcher receipt (2026-08-19, sanitized; local watcher timeout
after 12 seconds, project still running):

```text
2% (started 3m 33s ago)
Task: 768f5d6f-6b5c-4516-981b-6d8f967b6a6b
Project: 97b16c1b-653d-42b9-a5da-4ed765a8eb88
THINKING: I need to verify whether decode_encode_target is actually true by running through some test cases with #eval.
RUNNING_COMMAND: `... #eval encode c1; #eval decode (encode c1) == some c1; #eval decode (encode c2) == some c2 ...`
watch_exit=124
```

Follow-up bounded watcher receipt (same date; still no result):

```text
3% (started 4m 27s ago)
Task: 768f5d6f-6b5c-4516-981b-6d8f967b6a6b
Project: 97b16c1b-653d-42b9-a5da-4ed765a8eb88
THINKING: I'm debugging a parse error in what looks like a struct initialization — the issue is at column 91 on line 3 where `.unitPos` appears after `some`.
RUNNING_COMMAND: `cd /workspace/request-project; lake env lean /tmp/t.lean 2>&1 | grep -v manifest`
watch_exit=124
```

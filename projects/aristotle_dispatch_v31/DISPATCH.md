# v31 dispatch — bounded paper source encoder/decoder

**Status:** LOCAL REFUTATION RECORDED — DO NOT SUBMIT.  Three initially
requested source-table targets are FALSE AS STATED for the current executable
data model.  The source remains a local diagnostic artifact; it is not an
Aristotle request, a Kaggle launch, or a paper-proof claim.

## Scope and source ledger

The authoritative paper record is the endpoint-normalized one-/two-mark coding
lemma in `research_notes/rh_goals_2026-08-14/lane_g/TWOMARK_RENEWAL_SOL.md`:

- §2.4 (lines 329–344) defines the `U^t`/`L^t` atoms, heavy magnitudes, and
  maximal constant-sign unit runs.
- §3 (lines 362–414) deletes the maximal leading `L` and trailing `U` runs
  and leaves an empty or balanced canonical core.
- §4.1 (lines 440–590) gives the one-mark bridge table, the six two-mark
  bridge/absorption rows, the three coupled rows `U,H`, `H,L`, `U,L`, and the
  reverse adjacent `L,U` escape through the two outer cores.
- Equation (4.6) gives the finite overcount
  `4^2 * 3^4 * 2^3 * 4 * 2 = 82944 < 2^20`.

`TWOMARK_REFEREE.md` and `AM_REFEREE.md` confirm this coding at paper level
only and identify the missing formal artifact as an explicit source data type
and decoder.  The v30 dispatch's local wire record is not reused here: the
v31 source object and bounded code are separate types.  The exact paper branch
map has not been extracted into a verified encoder/decoder, so the maps below
are OPEN and CONJECTURAL pending that extraction.

## Source-to-type table

| paper datum | v31 executable representation | coverage note |
|---|---|---|
| `H_{+n}`, `H_{-n}` | `SourceAtom.heavyPos n`, `SourceAtom.heavyNeg n` | magnitude is explicit; `rangeOK` checks `2 ≤ n` and the bounded range |
| `U^t`, `L^t` | `SourceAtom.unitPos t`, `SourceAtom.unitNeg t` | run length is explicit; `t ≥ 1` is checked by `rangeOK` |
| balanced alphabet/range | `SourceAtom.rangeOK q` and `BalancedRangeData.rangeOK` | executable Boolean check, retained in `BalancedWord.checks` |
| maximal constant-sign unit runs | `sameUnitSign` and `maximalRunOK` | adjacent equal-sign light atoms are rejected by the check |
| normalized source word | `BalancedWord q` | carries the atom list plus both executable checks |
| one mark | `MarkChoice.one index` | index validity is stated by `MarkChoice.Valid` |
| ordered distinct two marks | `MarkChoice.two leftIndex rightIndex` | `MarkChoice.Valid` requires `leftIndex < rightIndex < length` |
| four cut-boundary fields | `CutData.leftAction`, `.middleAction`, `.rightAction`, `.outerAction` | each field has one of the three `CutAction` statuses `.bridge`, `.absorb`, `.split`; this is the paper `3^4` factor |
| three empty-core flags | `EmptyCoreFlags.left`, `.middle`, `.right` | Boolean fields are carried in `CutData.empty` |
| four coupled alternatives | `CoupledCase.unitHeavy`, `.heavyUnit`, `.unitUnit`, `.reverseUnitUnit` | the fourth constructor is the reverse `L,U` escape branch |
| four gain-bearing integers | `CutData.auxiliaries : Fin 4 → ℕ` | represents `p,r,s,v` or the light bridge lengths |
| endpoint-normalized core | `Core` with body and removed left/right run lengths | code has three fixed `Option Core` slots |
| at most three cores | `PaperCode.cores : Fin 3 → Option Core` | the bound is structural, not a list-length hypothesis |
| at most two marked heavy magnitudes | `PaperCode.heavyMagnitudes : Fin 2 → Option ℕ` | `sourceEncode` extracts marked heavy entries only |
| finite tag | `PaperTag := Fin 82944` | exact overcount ceiling; `paperTag_card_lt` proves it is below `2^20` |
| paper source object | `MarkedSource q` | word, mark choice, cut data, and normalized cores are all explicit |
| source encoder | `sourceEncode` | executable bounded packing; exact paper branch map remains OPEN |
| source decoder | `sourceDecode` | executable diagnostic reconstruction; coverage/round-trip remains OPEN |
| integer product gain | `codeGain` | executable positive baseline plus four auxiliary/heavy contributions |

`Core.body` is a paper core word, not a second copy of the full source word.
The bounded code has exactly three core slots and no source-object field or
unbounded source-list field.  The target is therefore not made tautological by
storing the complete `MarkedSource` in the code.

## Retained finite target signatures

Only these finite statements remain declarations after the local refutation:

```lean
theorem source_codeGain_pos {q : ℕ} (s : MarkedSource q) :
  1 ≤ codeGain (sourceEncode s)

theorem paperTag_card :
  Fintype.card PaperTag = 82944

theorem paperTag_card_lt :
  Fintype.card PaperTag < 2^20
```

`source_codeGain_pos`, `paperTag_card`, and `paperTag_card_lt` are proved by
the local executable definitions.  The removed validity, round-trip, and
injectivity statements are recorded below as FALSE AS STATED and are not
submission targets.

## Branch obligations and adversarial tests

The later referee must test every paper branch below against any future
extracted encoder and decoder, including malformed and out-of-range data.  The
current executable maps do not claim this branch coverage.  A bounded test is
diagnostic evidence only; it cannot replace the source-coverage proof.

One mark:

1. heavy positive `H_{+n}` bridge, with both endpoint runs zero/nonzero;
2. heavy negative `H_{-n}` bridge, with the same four endpoint combinations;
3. light `U^t` with right `L^v` bridge (`p = 0`, `v > 0`);
4. light `U^t` absorbed into the right core (`p = 0`, `v = 0`);
5. light `L^t` with left `U^p` bridge (`v = 0`, `p > 0`);
6. light `L^t` absorbed into the left core (`v = 0`, `p = 0`);
7. empty and nonempty endpoint-normalized cores, including maximality at each
   absorbed boundary.

Two ordered distinct marks:

1. each of `H_{+n}`, `H_{-n}`, `U^t`, `L^t` as the left mark;
2. each of the same four kinds as the right mark;
3. all left bridge/absorption rows (`H`, `U` with `r>0`, `L` with `p>0`);
4. all right bridge/absorption rows (`H`, `U` with `v>0`, `L` with `s>0`);
5. every empty/nonempty middle-core flag and every simultaneous outer-core
   absorption combination;
6. index order and unequal-index rejection for adjacent, separated, and
   endpoint marks.

Coupled alternatives and the dangerous reverse junction:

1. adjacent `U^t,H_{±n}` with the heavy bridge gain
   `n(1+t)(1+v)`;
2. adjacent `H_{±n},L^u` with the heavy bridge gain
   `n(1+p)(1+u)`;
3. adjacent `U^t,L^u` with the light gain `tu`;
4. reverse adjacent `L^u,U^t`, verifying that no false direct `ut` gain is
   claimed and that the two outer cores/absorption tags recover both marks;
5. equal-sign adjacent light runs, which must be one maximal atom rather than
   two marks;
6. truncated/invalid source words, invalid heavy magnitudes, invalid `q`,
   duplicate marks, and malformed code slots.

## FALSE-AS-STATED escape hatch

If Aristotle finds any requested target false, retain the original statement
only in a `FALSE AS STATED` comment, provide an exact counterexample and a
named `<target>_false` negation, then state the weakest corrected theorem and
record the downstream status change.  Never force a contradiction by adding a
source-table assumption or an opaque proof object.

## Explicit exclusions

This dispatch does not encode or claim:

- matrix inequality `(4.1)` or the heavy-entry bounds used to derive it;
- Ford packing/counting or the endpoint-core population bound;
- the analytic atom-moment estimate `(AM)` or its constants;
- RATE-A, operator tails, or any global renewal estimate;
- the LAW, canonical-section existence, theta-image characterization, or a
  finite-height theorem beyond the explicit data structures;
- a proof that the printed paper branch prose is complete, collision-free, or
  injective at all `q`.

These remain paper-level inputs or **CONJECTURAL** until separately verified.

## Local syntax gate

The required check uses the proven absolute v26 cache and does not create a
cache in this dispatch directory:

```bash
( cd /Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle && \
  /Users/za/.elan/bin/lake env lean \
  /Users/za/Documents/farey-hecke/.worktrees/law-v31-source-decoder-20260819/projects/aristotle_dispatch_v31/RateCoreVI.lean )
```

The corrected source is expected to typecheck with zero exit and no placeholder
warnings.  The lane report records the fresh exit and output, plus the exact
target search, forbidden-declaration search, brief lint, and `git diff --check`
receipt.

No Aristotle credentials are loaded or printed by this dispatch.  No Aristotle
submission and no Kaggle launch are authorized in this lane.

## 2026-08-19 — local refutation and corrected-target status

The initial target set was audited before any submission.  The following are
FALSE AS STATED and have been removed from the Lean submission surface:

```lean
-- FALSE AS STATED (removed):
-- source_encode_valid {q} (s : MarkedSource q) :
--   PaperCode.Valid q (sourceEncode s)
-- source_decode_encode {q} (s : MarkedSource q) :
--   sourceDecode (sourceEncode s) = some s
-- source_encode_injective {q} :
--   Function.Injective (@sourceEncode q)
```

Machine-checked witnesses in `RateCoreVI.lean` are:

- `balanced_word_valid_rejects_nonmaximal`: stored `true` checks do not make a
  word valid when adjacent equal-sign unit atoms violate maximality;
- `source_encode_valid_false`: a raw source with core `H_{+1}` produces a code
  failing `PaperCode.Valid`;
- `source_encode_collision`: marks at indices `0` and `2` with the same atom
  kind produce equal codes, while `source_collision_sources_ne` proves the
  sources differ; `collision_sources_valid` verifies both source witnesses pass
  the strengthened local validity predicate;
- `source_decode_mark_counterexample`: decoding the index-`2` source returns
  the hard-coded index-`0` mark rather than that source;
- `source_encode_injective_false`: the requested injectivity statement is
  refuted by that collision;
- `source_decode_total`: the executable decoder is total on this format, which
  is the weakest local replacement currently proved.  It is not a source
  round-trip theorem.

The tag arithmetic was corrected from four four-way fields to four three-way
status fields.  `sourceTagIndex` now uses
`2 * 16 * 3^4 * 2^3 * 4 = 82944`; the modulo in `paperTagOfSource` is retained
only as a defensive total constructor.  This fixes the prior 262144-selector
overcount but cannot restore injectivity because mark indices and the full
source branch map are not in the bounded payload.

The exact paper encoder/decoder, including recovery of arbitrary mark indices,
is **OPEN / CONJECTURAL pending source-table extraction**.  No forced theorem,
opaque assumption, or analytic `(4.1)`, Ford, `(AM)`, RATE-A, or LAW claim is
introduced by this correction.

## 2026-08-19 — cold-referee confirmation and decoder-slice correction

`V31_REFEREE.md` independently rebuilt this exact source against the v26
cache (`EXIT_CODE=0`), re-proved the collision and decode negation without
using the file's proof terms, and returned **REFUTATION CONFIRMED**.  The two
locally valid, distinct sources `collisionLeft` and `collisionRight` encode to
the identical payload

```text
tag=41492, cores=[none,none,none], auxiliaries=[0,0,0,0],
heavyMagnitudes=[none,none].
```

The referee also found a second, independent decoder defect.  The packing is

```text
mode + 2 * (kindCode + 16 * (cutCode + 81 * (emptyCode + 8 * coupledCode))),
```

but `sourceDecode` takes base-3 cut digits immediately from `tag / 2` instead
of first removing the 16-way `kindCode` slice.  For the witness, the current
decoder reads action digits `[1,0,1,0]` where the packed cut code has digits
`[0,0,0,0]`.  Correct slicing would begin with
`kindCode = payload % 16` and `cutCode = (payload / 16) % 81`; even that would
not recover arbitrary mark indices or reconstruct the source word.

The strongest banked result is therefore the **referee-confirmed negation** of
the three naive targets for this executable model.  The exact paper
encoder/decoder, branch coverage, and any repaired conditional validity or
round-trip theorem remain **OPEN / CONJECTURAL**.  No Aristotle submission was
made because no load-bearing positive paper-source target survived the local
falsification gate.  This confirmation changes no status for `(FW)`, `(AM)`,
RATE-A, q7, any finite LAW case, or the LAW.

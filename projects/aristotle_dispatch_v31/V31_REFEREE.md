# v31 cold referee report — bounded-source refutation

**Verdict: REFUTATION CONFIRMED**

This confirms only a local refutation of the false-as-stated targets in the
current executable data model.  It does not verify the paper encoder/decoder
or the paper source-table coverage.  Those remain **OPEN / CONJECTURAL**.

## Fresh receipts

The brief's exact absolute-cache command was run verbatim:

```text
$ ( cd /Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle && \
    /Users/za/.elan/bin/lake env lean \
    /Users/za/Documents/farey-hecke/.worktrees/law-v31-source-decoder-20260819/projects/aristotle_dispatch_v31/RateCoreVI.lean )
EXIT_CODE=0
```

The target path in that required command and the local referee copy are the
same file by hash:

```text
$ sha256sum projects/aristotle_dispatch_v31/RateCoreVI.lean /Users/za/Documents/farey-hecke/.worktrees/law-v31-source-decoder-20260819/projects/aristotle_dispatch_v31/RateCoreVI.lean
b8b3ed67870b4f9d35c4a049cd27e266984dedaf159caac3d700b2106144ee5e  projects/aristotle_dispatch_v31/RateCoreVI.lean
b8b3ed67870b4f9d35c4a049cd27e266984dedaf159caac3d700b2106144ee5e  /Users/za/Documents/farey-hecke/.worktrees/law-v31-source-decoder-20260819/projects/aristotle_dispatch_v31/RateCoreVI.lean
```

The clean stdin recheck imported the exact source text, checked every named
witness, and evaluated the relevant finite data:

```text
$ { sed -n '1,417p' projects/aristotle_dispatch_v31/RateCoreVI.lean; ...; } \
    | ( cd /Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle && \
        /Users/za/.elan/bin/lake env lean --stdin )
RateCoreVI.balanced_word_valid_rejects_nonmaximal :
  ¬{ atoms := [SourceAtom.unitPos 1, SourceAtom.unitPos 1], checks := { rangeOK := true, maximalRunsOK := true } }.Valid
RateCoreVI.collision_sources_valid : collisionLeft.Valid ∧ collisionRight.Valid
RateCoreVI.source_encode_collision : sourceEncode collisionLeft = sourceEncode collisionRight
RateCoreVI.source_decode_mark_counterexample : sourceDecode (sourceEncode collisionRight) ≠ some collisionRight
RateCoreVI.source_encode_injective_false : ¬Function.Injective sourceEncode
RateCoreVI.source_encode_valid_false : ∃ s, ¬PaperCode.Valid 3 (sourceEncode s)
("left_checks", true, true, true)
("right_checks", true, true, true)
("nonmax", true, false)
("invalid_core", false, true)
("encode_equal", true)
("source_ne", false)
("decode_roundtrip", false)
("tag_left_right", 41492, 41492, 41492, 41492)
("card", 82944, true)
("product", 82944)
EXIT_CODE=0
```

For the exact decoded object and both encoded payloads:

```text
$ { sed -n '1,417p' projects/aristotle_dispatch_v31/RateCoreVI.lean; ...; } \
    | ( cd /Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle && \
        /Users/za/.elan/bin/lake env lean --stdin )
("encoded_left",
 { tag := 41492, cores := ![none, none, none], auxiliaries := ![0, 0, 0, 0], heavyMagnitudes := ![none, none] })
("encoded_right",
 { tag := 41492, cores := ![none, none, none], auxiliaries := ![0, 0, 0, 0], heavyMagnitudes := ![none, none] })
("decoded_right",
 some { word := { atoms := [], checks := { rangeOK := true, maximalRunsOK := true } },
   mark := RateCoreVI.MarkChoice.one 0,
   cuts := { leftAction := RateCoreVI.CutAction.absorb,
             middleAction := RateCoreVI.CutAction.bridge,
             rightAction := RateCoreVI.CutAction.absorb,
             outerAction := RateCoreVI.CutAction.bridge,
             empty := { left := false, middle := false, right := false },
             coupled := RateCoreVI.CoupledCase.unitHeavy,
             auxiliaries := ![0, 0, 0, 0] },
   cores := [] })
EXIT_CODE=0
```

The arithmetic and decoder-slice replay was independently evaluated:

```text
$ python3 -c 'product=4**2*3**4*2**3*4*2; max_tag=1+2*(15+16*(80+81*(7+8*3))); tag=41492; payload=tag//2; cut=(payload//16)%81; ec=(payload//(16*81)); print("product",product); print("max_tag",max_tag); print("tag_range",0 <= max_tag < product); print("collision_payload",payload); print("current_action_digits",[payload % 3,(payload//3)%3,(payload//9)%3,(payload//27)%3]); print("current_empty_digit",payload//81); print("current_coupled_digit",(payload//81//8)%4); print("correct_kind_code",payload%16); print("correct_cut_code",cut); print("correct_action_digits",[cut%3,(cut//3)%3,(cut//9)%3,(cut//27)%3]); print("correct_empty_code",ec%8); print("correct_coupled_code",(ec//8)%4)'
product 82944
max_tag 82943
tag_range True
collision_payload 20746
current_action_digits [1, 0, 1, 0]
current_empty_digit 256
current_coupled_digit 0
correct_kind_code 10
correct_cut_code 0
correct_action_digits [0, 0, 0, 0]
correct_empty_code 0
correct_coupled_code 2
```

## Witness audit

### `balanced_word_valid_rejects_nonmaximal`

Confirmed.  The stored checks for `[U^1,U^1]` are both `true`, but the
recomputed range/maximality result is `(true,false)`.  The adjacent equal-sign
unit atoms therefore fail `maximalRunOK`; merely storing `true` checks does not
make the word valid.  This is the `("nonmax", true, false)` receipt above.

### `collision_sources_valid` and `source_encode_collision`

Confirmed semantically.  The two sources use the same atom list
`[unitPos 1, unitNeg 1, unitPos 1]`, the same zero cut data, empty core list,
and valid recomputed checks.  Their marks are `.one 0` and `.one 2` in a
three-atom word; the checked source-validity theorem was also re-used in two
fresh `example` declarations, both of which typechecked in the receipt above.

The marks are distinct (`source_ne = false` for the equality decision), but
the source encodings are equal (`encode_equal = true`).  The full payload
receipt shows equality in every field: tag `41492`, all three core slots
`none`, four zero auxiliaries, and two absent heavy magnitudes.  This is a
genuine valid-source collision, not an invalidity loophole or a differing
payload.

### `source_decode_mark_counterexample`

Confirmed.  Decoding the common code produces an empty word and mark `.one 0`,
not `collisionRight` (which has the three atoms and mark `.one 2`).  The exact
decoded object is printed above, and the equality decision is `false`.
The named theorem therefore captures a real round-trip failure.

### `source_encode_injective_false`

Confirmed.  The preceding valid, distinct pair with equal encodings is exactly
the witness needed to refute `Function.Injective (@sourceEncode 3)`.  As a
cold proof check independent of the file's proof term, the following fresh
reproofs compiled with exit zero:

```text
$ { sed -n '1,417p' projects/aristotle_dispatch_v31/RateCoreVI.lean; ...; } \
    | ( cd /Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle && \
        /Users/za/.elan/bin/lake env lean --stdin )
EXIT_CODE=0
```

The stdin suffix was:

```lean
open RateCoreVI
theorem cold_recheck_decode : sourceDecode (sourceEncode collisionRight) ≠ some collisionRight := by decide
theorem cold_recheck_equal : sourceEncode collisionLeft = sourceEncode collisionRight := by rfl
theorem cold_recheck_ne : collisionLeft ≠ collisionRight := by decide
```

The corresponding cold reproof dependency receipt was:

```text
'cold_recheck_decode' depends on axioms: [propext, Classical.choice, Quot.sound]
'cold_recheck_equal' depends on axioms: [propext, Classical.choice, Quot.sound]
'cold_recheck_ne' depends on axioms: [propext, Classical.choice, Quot.sound]
EXIT_CODE=0
```

### `source_encode_valid_false`

Confirmed as stated.  `invalidSource` contains `invalidCore` with
`heavyPos 1` at `q = 3`.  Its body range check is `false` while its maximality
check is `true` (`("invalid_core", false, true)` above), so `Core.Valid 3
invalidCore` is false.  `sourceEncode` places that core in the first core
slot, while the requested theorem quantifies over an arbitrary raw
`MarkedSource` and does not assume `MarkedSource.Valid`.  Thus the code-validity
claim is false for its stated domain.

The weakest safe repair is conditional: any validity-preservation theorem must
add `MarkedSource.Valid s` (and still requires a proof).  The current packet
does not claim that repaired theorem.

## Tag/cardinality and decoder audit

The finite product is correct:

```text
4^2 * 3^4 * 2^3 * 4 * 2 = 82944,
maximal encoded tag = 82943,
Fintype.card (Fin 82944) = 82944 < 2^20.
```

The product, range, and `< 2^20` facts are the fresh receipts above.  The
encoder's four cut actions use the intended base-3 digits `0,1,2`, and the
four-digit cut block has size `3^4 = 81`.  This arithmetic is a valid finite
overcount, not an injectivity proof.

The packing layout is

```text
tag = mode + 2 * (kindCode + 16 * (cutCode + 81 * (emptyCode + 8 * coupledCode))).
```

For the collision, `kindCode = 10`, `cutCode = 0`, `emptyCode = 0`,
`coupledCode = 2`, giving payload `tag/2 = 20746`.  The implementation's
decoder sets `cutDigit := tag/2` and immediately takes base-3 residues.  It
therefore sees action digits `[1,0,1,0]`, `emptyDigit = 256`, and coupled
digit `0`, instead of the source's `[0,0,0,0]`, empty code `0`, and coupled
code `2`.  The independent arithmetic receipt and the printed decoded object
agree on this mismatch.

The decoder should first remove the kind block (`payload % 16`), then decode
the cut block from `(payload / 16) % 81`, and only then split the empty/coupled
block.  Even that slice correction would not recover arbitrary mark indices:
`sourceDecode` currently ignores the encoded kind digits and
`heavyMagnitudes`, reconstructs atoms only from `Core.body`, and hard-codes the
mark as `.one 0` or `.two 0 1`.  Consequently its totality theorem is only
totality of this diagnostic reconstruction, not validity, coverage, or
round-trip.

## Declaration and dependency audit

The exact placeholder and forbidden-target scans returned no matches:

```text
$ rg -n "\b(sorry|admit|axiom)\b" projects/aristotle_dispatch_v31/RateCoreVI.lean
PLACEHOLDER_SCAN_EXIT=1
$ rg -n "^[[:space:]]*(theorem|lemma|def)[[:space:]]+(source_encode_valid|source_decode_encode|source_encode_injective)\b" projects/aristotle_dispatch_v31/RateCoreVI.lean
FORBIDDEN_TARGET_SCAN_EXIT=1
```

The exit code `1` is `rg`'s no-match result; there are zero `sorry`, `admit`,
or declared `axiom` tokens, and no declarations named exactly
`source_encode_valid`, `source_decode_encode`, or `source_encode_injective`.
Only the named `_false` witnesses remain.

The surviving positive declarations are exactly:

```text
400:theorem source_decode_total {q : ℕ} (s : MarkedSource q) :
404:theorem source_codeGain_pos {q : ℕ} (s : MarkedSource q) :
409:theorem paperTag_card :
413:theorem paperTag_card_lt :
```

Their meanings remain weak: `source_decode_total` says only
`∃ t, sourceDecode (sourceEncode s) = some t`; `source_codeGain_pos` is only
the baseline `1 ≤ codeGain`; the two `paperTag` declarations are cardinality
and finite-range facts.  None says source validity, decoder round-trip,
injectivity, or exact paper branch coverage.

`#print axioms` on all named declarations exposed only the usual
`propext`, `Classical.choice`, and `Quot.sound`, except that the file's
`source_decode_mark_counterexample` proof uses `native_decide` and therefore
also reports `Lean.ofReduceBool` and `Lean.trustCompiler`:

```text
'RateCoreVI.balanced_word_valid_rejects_nonmaximal' depends on axioms: [propext]
'RateCoreVI.source_encode_collision' depends on axioms: [propext, Classical.choice, Quot.sound]
'RateCoreVI.collision_sources_valid' depends on axioms: [propext, Classical.choice, Quot.sound]
'RateCoreVI.source_decode_mark_counterexample' depends on axioms: [propext, Classical.choice, Lean.ofReduceBool, Lean.trustCompiler, Quot.sound]
'RateCoreVI.source_encode_injective_false' depends on axioms: [propext, Classical.choice, Quot.sound]
'RateCoreVI.source_encode_valid_false' depends on axioms: [propext, Classical.choice, Quot.sound]
'RateCoreVI.source_decode_total' depends on axioms: [propext, Classical.choice, Quot.sound]
'RateCoreVI.source_codeGain_pos' depends on axioms: [propext, Classical.choice, Quot.sound]
'RateCoreVI.paperTag_card' depends on axioms: [propext, Classical.choice, Quot.sound]
'RateCoreVI.paperTag_card_lt' depends on axioms: [propext, Classical.choice, Quot.sound]
EXIT_CODE=0
```

The native-decision dependency does not carry the verdict: the independent
`by decide` reproof of the decode negation above uses only the standard
foundation set (`propext`, `Classical.choice`, `Quot.sound`).

## Ledger boundary

The dispatch itself records that the exact paper branch map and source-table
coverage are **OPEN / CONJECTURAL**.  Its fresh scope scan states that the
executable does not assert `(4.1)`, Ford counting, `(AM)`, RATE-A, or the LAW:

```text
7:  executable definitions do not assert the matrix inequality (4.1), Ford
15: executable definitions do not assert the matrix inequality (4.1), Ford
16: counting, `(AM)`, RATE-A, or the LAW.  Those are paper inputs/exclusions, not
28: are OPEN and CONJECTURAL pending that extraction.
50: | source encoder | `sourceEncode` | executable bounded packing; exact paper branch map remains OPEN |
51: | source decoder | `sourceDecode` | executable diagnostic reconstruction; coverage/round-trip remains OPEN |
136: - the analytic atom-moment estimate `(AM)` or its constants;
137: - RATE-A, operator tails, or any global renewal estimate;
138: - the LAW, canonical-section existence, theta-image characterization, or a
143: These remain paper-level inputs or **CONJECTURAL** until separately verified.
205: is **OPEN / CONJECTURAL pending source-table extraction**.  No forced theorem,
206: opaque assumption, or analytic `(4.1)`, Ford, `(AM)`, RATE-A, or LAW claim is
```

Accordingly this local result cannot upgrade **(FW)**, **(AM)**, RATE-A, q7,
any finite LAW case, or the LAW.  No such analytic or global theorem is
introduced by the executable or by this report.  The valid corrected statement
is strictly local: the current raw source maps have explicit counterexamples,
while the exact paper encoder/decoder and its coverage/injectivity remain
unproved.

## Final checks

```text
$ git diff --check
DIFF_CHECK_EXIT=0
$ git status --short --branch
## codex/law-v31-referee-20260819
?? projects/aristotle_dispatch_v31/REFEREE_BRIEF.md
?? projects/aristotle_dispatch_v31/V31_REFEREE.md
```

READY FOR JUDGING

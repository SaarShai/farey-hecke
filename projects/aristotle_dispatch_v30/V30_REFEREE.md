# V30 cold referee — candidate `41e1af6`

Date: 2026-08-19.  This is a cold audit of the committed returned source, not
an acceptance of the paper-level RATE argument.

## Inputs and hashes

The referee worktree was at
`41e1af634895c790c9f8ddd40650d0c5811a7e74` (the requested candidate; no
tracked source was changed).  The live toolchain is Lean 4.28.0 and Lake
5.0.0-src+7e01a1b.

| artifact | SHA-256 |
|---|---|
| `projects/aristotle_dispatch_v30/RateCoreV.lean` (draft) | `4335bcae46b120be09a7c80cd9c250ba2acedf09b2f6e2ed2ffc1e03a777febd` |
| `projects/aristotle_dispatch_v30/result/aristotle_dispatch_v30_aristotle/RateCoreV.lean` (returned) | `a7bbee7e18a51ce9271222cc5f0e7b4553a77d9ecc3c2b09fdfbd9db3ad629dc` |
| `projects/aristotle_dispatch_v30/DISPATCH.md` | `2b34d8f00c5954d8fad831f5ce4ec0bd2e228f817029212b0400885cedd6c0ad` |
| returned `ARISTOTLE_SUMMARY.md` | `a530d136a3748c63ae830bff95144faa7602d11d12d5ce0c1f3e52dcbccf319f` |
| returned `DISPATCH.md` | `88487fc41f248107f4fdda2ca36806d356bce19b7567abad2ea9b9687488f31f` |
| v26 cache `.../result/aristotle_dispatch_v26_aristotle/RateCore.lean` | `a2fa4111ab5ed4c92e34697b1e5ddb84b0b477984233b1e29ab2fcc94e47536d` |

The brief names the v26 cache directory, which exists.  Its tracked source is
`RateCore.lean`, not `RateCoreV.lean`; the directory is used only as the Lake
environment.  The returned source itself is the exact file hashed above.

## Independent rebuild

Exact command, run against the v26 cache directory:

```text
$ ( cd /Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle && /Users/za/.elan/bin/lake env lean /Users/za/Documents/farey-hecke/.worktrees/rate-v30-referee-20260819/projects/aristotle_dispatch_v30/result/aristotle_dispatch_v30_aristotle/RateCoreV.lean )
lean_rebuild_exit=0
```

There was no compiler diagnostic on the successful run.  A first invocation
hit the 30-second tool wait while the v26 Mathlib cache was being populated;
it was not treated as a result.  A separate trial against the incomplete v26
cache copy in this referee worktree failed with
`object file .../.lake/packages/mathlib/.lake/build/lib/lean/Mathlib.olean ... does not exist`;
that trial was abandoned.  The required absolute v26-cache command above was
then rerun and passed.

## Forbidden declarations and axioms

The actual returned source was searched, not its summary:

```text
$ rg -n '^\s*(sorry|axiom)\b' projects/aristotle_dispatch_v30/result/aristotle_dispatch_v30_aristotle/RateCoreV.lean
forbidden_decl_rg_exit=1
$ rg -n -i '\bsorry\b|\baxiom\b' projects/aristotle_dispatch_v30/result/aristotle_dispatch_v30_aristotle/RateCoreV.lean
forbidden_token_rg_exit=1
```

Both searches produced no matching line.  Thus the returned source contains
zero `sorry` terms and zero declared `axiom`s.  This does not mean zero axiom
dependencies.

The following was streamed by appending `#print axioms` commands to the exact
returned source on stdin and running `lake env lean` in the v26 cache:

```text
$ { sed -n '1,$p' projects/aristotle_dispatch_v30/result/aristotle_dispatch_v30_aristotle/RateCoreV.lean
    printf '%s\n' '#print axioms RateCoreV.fw_product_gain' '#print axioms RateCoreV.fw_product_mono' '#print axioms RateCoreV.atomOfTag_atomTag' '#print axioms RateCoreV.modeOfTag_modeTag' '#print axioms RateCoreV.statusOfTag_statusTag' '#print axioms RateCoreV.signedNat_decode' '#print axioms RateCoreV.takeNatList_append' '#print axioms RateCoreV.takeNatList_self' '#print axioms RateCoreV.signedNat_length' '#print axioms RateCoreV.flatMap_signedNat_length' '#print axioms RateCoreV.decodeDigits_flatMap' '#print axioms RateCoreV.decodeCore_append' '#print axioms RateCoreV.decodeCores_append' '#print axioms RateCoreV.decode_encode_target' '#print axioms RateCoreV.encode_injective' '#print axioms RateCoreV.marked_code_source_injective_target' '#print axioms RateCoreV.marked_code_product_gain_target'
  } | ( cd /Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle && /Users/za/.elan/bin/lake env lean --stdin )
'RateCoreV.fw_product_gain' depends on axioms: [propext, Classical.choice, Quot.sound]
'RateCoreV.fw_product_mono' depends on axioms: [propext]
'RateCoreV.atomOfTag_atomTag' does not depend on any axioms
'RateCoreV.modeOfTag_modeTag' does not depend on any axioms
'RateCoreV.statusOfTag_statusTag' does not depend on any axioms
'RateCoreV.signedNat_decode' depends on axioms: [propext, Classical.choice, Quot.sound]
'RateCoreV.takeNatList_append' depends on axioms: [propext]
'RateCoreV.takeNatList_self' depends on axioms: [propext]
'RateCoreV.signedNat_length' does not depend on any axioms
'RateCoreV.flatMap_signedNat_length' depends on axioms: [propext, Quot.sound]
'RateCoreV.decodeDigits_flatMap' depends on axioms: [propext, Quot.sound]
'RateCoreV.decodeCore_append' depends on axioms: [propext, Quot.sound]
'RateCoreV.decodeCores_append' depends on axioms: [propext, Quot.sound]
'RateCoreV.decode_encode_target' depends on axioms: [propext, Quot.sound]
'RateCoreV.encode_injective' depends on axioms: [propext, Quot.sound]
'RateCoreV.marked_code_source_injective_target' depends on axioms: [propext, Quot.sound]
'RateCoreV.marked_code_product_gain_target' does not depend on any axioms
axiom_audit_exit=0
```

The only dependencies are the standard Lean axioms `propext`,
`Classical.choice`, and `Quot.sound`.  They are real dependencies and are not
reported as “zero dependencies”; no nonstandard declaration occurs.

## Statement preservation and finite verdicts

The focused diff compared the nine requested theorem signatures by name and
returned exit zero:

```text
extract_requested() {
  /usr/bin/perl -0777 -ne '
    my @names = qw(fw_product_gain fw_product_mono atomOfTag_atomTag modeOfTag_modeTag statusOfTag_statusTag signedNat_decode marked_code_source_injective_target decode_encode_target marked_code_product_gain_target);
    for my $name (@names) {
      if (/^theorem\s+\Q$name\E\b(.*?)(?::=)/ms) {
        my $s = "theorem $name$1";
        $s =~ s/\s+\z//;
        print "$s\n";
      }
    }
  ' "$1"
}
diff -u <(extract_requested projects/aristotle_dispatch_v30/RateCoreV.lean) <(extract_requested projects/aristotle_dispatch_v30/result/aristotle_dispatch_v30_aristotle/RateCoreV.lean)
requested_signature_diff_exit=0
```

The normalized signatures were exactly:

```text
theorem fw_product_gain
    {n A B Y : ℝ}
    (hn : 4 ≤ n)
    (hA : 0 ≤ A)
    (hB : 0 ≤ B)
    (hheight : 2 * (n - 2) * A * B ≤ Y) :
    n * A * B ≤ Y
theorem fw_product_mono
    {n r s Y : ℕ}
    (hn : 1 ≤ n)
    (h : n * r * s ≤ Y) :
    r * s ≤ Y
theorem atomOfTag_atomTag (k : AtomKind) : atomOfTag (atomTag k) = some k
theorem modeOfTag_modeTag (m : MarkMode) : modeOfTag (modeTag m) = some m
theorem statusOfTag_statusTag (s : BoundaryStatus) :
    statusOfTag (statusTag s) = some s
theorem signedNat_decode (z : ℤ) :
    decodeSigned (signedNat z) = some (z, [])
theorem marked_code_source_injective_target :
    ∀ (x y : MarkedCode), WellFormed x → WellFormed y →
      encode x = encode y → x = y
theorem decode_encode_target (c : MarkedCode) : decode (encode c) = some c
theorem marked_code_product_gain_target
    (c : MarkedCode) (h : WellFormed c) :
    c.gains.length ≤ 4 ∧ c.heavyMagnitudes.length ≤ 2
```

The returned source changes only proof material and adds local parser lemmas,
`decode_encode_target`, `encode_injective`, and three executable guards.  The
`signedNat_decode` proof removes unused simp arguments.  No requested
assumption, conclusion, or dependency order was weakened or strengthened in
the signatures; `encode_injective` is an additional unconditional theorem on
the same local data type.

| target | exact formal result | verdict |
|---|---|---|
| `fw_product_gain` | From real `n >= 4`, `A,B >= 0`, and `2*(n-2)*A*B <= Y`, derives `n*A*B <= Y`. | **CONFIRMED** as this ordered-ring implication only. |
| `fw_product_mono` | From natural `n >= 1` and `n*r*s <= Y`, derives `r*s <= Y`. | **CONFIRMED** as this monotonic relaxation only. |
| three tag round trips | `atomOfTag`, `modeOfTag`, and `statusOfTag` invert their corresponding finite constructors. | **CONFIRMED**. |
| `signedNat_decode` | The sign/magnitude encoding of every `Int` decodes to that `Int` with empty remainder. | **CONFIRMED** for `decodeSigned (signedNat z)`. |
| `decode_encode_target` | Every `MarkedCode` value, with no `WellFormed` assumption, decodes from its explicit `encode` list. | **CONFIRMED** for the local wire format. |
| `encode_injective` | `Function.Injective encode` on all `MarkedCode`, obtained from the round trip. | **CONFIRMED** for the local wire format. |
| `marked_code_source_injective_target` | The requested `WellFormed`-hypothesised statement follows from local `encode` injectivity; its hypotheses are ignored by the proof. | **CONFIRMED** at exactly this type scope; **GAPS** for any paper source map. |
| `marked_code_product_gain_target` | Merely projects `WellFormed`'s `gains.length <= 4` and `heavyMagnitudes.length <= 2`. | **CONFIRMED** as a list-bound consequence, not an analytic gain theorem. |

The supporting lemmas `takeNatList_append`, `takeNatList_self`,
`signedNat_length`, `flatMap_signedNat_length`, `decodeDigits_flatMap`,
`decodeCore_append`, and `decodeCores_append` are also present in the returned
source and are covered by the independent build and axiom stream above.

## Adversarial decoder audit

The implementation is a terminating `Option` parser, not a proof that every
raw list is valid.  The following facts are directly visible in returned
`RateCoreV.lean` lines 132--240:

* The format tag is exactly `30`.  `modeOfTag`, `atomOfTag`, and
  `statusOfTag` reject out-of-range tags; second-kind tag `4` is the reserved
  `none` encoding.
* `takeNatList` recurses on the announced natural length and returns `none` on
  truncation.  Core bodies announce a length and consume exactly twice that
  many natural digits.  Core, gain, and heavy lists each consume their own
  length-prefixed segment, and the final `trailing = []` test rejects extra
  digits.
* `decodeSigned` rejects signs other than `0` and `1`.  `signedNat` uses sign
  `0` for nonnegative integers and sign `1` for negative integers, so the
  encoded path is round-trip correct.
* The raw decoder accepts `(sign,magnitude) = (1,0)` as integer zero.  This is
  a noncanonical raw spelling: re-encoding the resulting zero uses `(0,0)`.
  Therefore the proved theorem is `decode (encode c) = some c`, not a
  canonical inverse or `encode (decode xs) = xs` for every accepted `xs`.
* `decode` does not enforce `WellFormed`: arbitrary list counts, arbitrary
  core bodies/unit-run lengths, and mode/second-kind combinations are decoded
  as data when their wire syntax is valid.  This is harmless for injectivity
  of the explicit `MarkedCode` record, but it is not a source-branch validity
  theorem.

The returned guards cover one concrete sample, its round trip, and rejection
of a bad leading tag (lines 350--366).  Independent stdin probes exercised
empty/truncated input, invalid mode/atom/second-kind/status tags, a trailing
digit, and an invalid sign; all eight malformed cases returned `none`.  The
noncanonical sign-one/zero case returned a concrete code:

```text
$ { sed -n '1,$p' projects/aristotle_dispatch_v30/result/aristotle_dispatch_v30_aristotle/RateCoreV.lean
    printf '%s\n' '#eval RateCoreV.decode []' '#eval RateCoreV.decode [30]' '#eval RateCoreV.decode [30, 2, 0, 4, 0, 0, 0, 0, 0, 0]' '#eval RateCoreV.decode [30, 0, 4, 4, 0, 0, 0, 0, 0, 0]' '#eval RateCoreV.decode [30, 0, 0, 5, 0, 0, 0, 0, 0, 0]' '#eval RateCoreV.decode [30, 0, 0, 4, 5, 0, 0, 0, 0, 0]' '#eval RateCoreV.decode [30, 0, 0, 4, 0, 0, 0, 0, 0, 0, 99]' '#eval RateCoreV.decode [30, 0, 0, 4, 0, 0, 0, 1, 0, 0, 1, 2, 0, 0, 0]' '#eval RateCoreV.decode [30, 0, 0, 4, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0]'
  } | ( cd /Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle && /Users/za/.elan/bin/lake env lean --stdin )
none
none
none
none
none
none
none
none
some { mode := RateCoreV.MarkMode.one,
  firstKind := RateCoreV.AtomKind.heavyPos,
  secondKind := none,
  leftStatus := RateCoreV.BoundaryStatus.bridge,
  middleStatus := RateCoreV.BoundaryStatus.bridge,
  rightStatus := RateCoreV.BoundaryStatus.bridge,
  cores := [{ body := [0], leftUnitRun := 0, rightUnitRun := 0 }],
  gains := [],
  heavyMagnitudes := [] }
decoder_probe_exit=0
```

## Formal scope versus paper scope

`MarkedCode` is a locally declared structure with fields `mode`, atom tags,
three boundary-status fields, lists of `Core`, gains, and heavy magnitudes
(returned lines 104--124).  There is no paper source-object type, source-table
encoder, branch-coverage predicate, canonical-word map, or theorem connecting
paper marked objects to `MarkedCode`.

Consequently, `marked_code_source_injective_target` does **not** prove a
decoder or injectivity theorem for the full paper marked-source map.  Its type
only says that equal natural-number lists from this local `encode` imply equal
local `MarkedCode` records (under two unused `WellFormed` hypotheses).  The
returned header explicitly limits both new theorems to the concrete
serialization and says source-table coverage is not claimed (lines 15--18);
the proof comment makes the same limitation (lines 338--346).  The paper-level
source-table coverage verdict is **GAPS**.

Likewise:

* the finite `fw_product_gain` implication is not the affine overflow
  factorization plus prefix/suffix multiplicities, harmonic sum, Ford count,
  or the displayed analytic `(FW)` estimate;
* `fw_product_mono` has no multiplicity hypotheses or conclusion;
* `marked_code_product_gain_target` only projects list lengths from
  `WellFormed`; it is not the `(AM)` atom-moment bound;
* no canonical `R^{a_0}Q...QR^{a_k}` normal form, theta image/Ford counting,
  endpoint-core population bound, source Lemma 4.1 branch coverage, analytic
  `(AM)`, `(RATE-A)` machine certificate, or operator-tail theorem is present.

Verdicts for these broader claims are **GAPS / CONJECTURAL at the Lean level**,
not `CONFIRMED` and not silently upgraded by the successful finite build.

## Final verification receipts

```text
COMMAND: git diff --check -- projects/aristotle_dispatch_v30
git_diff_check_exit=0

COMMAND: forbidden generated-artifact scan under projects/aristotle_dispatch_v30
artifact_scan_exit=0

COMMAND: concrete secret-value scan (names/locations only)
concrete_secret_value_scan_exit=1
```

The broader keyword scan matched only the literal documentation examples
`~/.farey_api_keys` and the scan command in `DISPATCH.md`; it exposed no key,
token, bearer value, or credential.  No `.lake`, OLean, archive, worktree, or
other generated artifact is present under `projects/aristotle_dispatch_v30`.

Before this file was created, `git status --short --branch` showed only the
brief supplied by the orchestrator:

```text
## codex/rate-v30-referee-20260819
?? REFEREE_BRIEF.md
```

The only intended new artifact from this pass is this file.  No existing
source, result, dispatch, MAP, task, theorem ledger, or git state was edited.

## Overall referee disposition

**FINITE SERIALIZATION/ALGEBRA: CONFIRMED**, conditioned on the exact returned
source hash and the independent v26-cache rebuild above.  **PAPER-SCOPE
DECODING, SOURCE-TABLE COVERAGE, ANALYTIC FW/AM, and RATE-A: GAPS**.  The
returned candidate is a machine-verified finite wire-format result, not a
machine-verified completion of the paper argument.

## Lane report

summary: Candidate `41e1af6` returned source hash
`a7bbee7e18a51ce9271222cc5f0e7b4553a77d9ecc3c2b09fdfbd9db3ad629dc`; the
exact v26-cache rebuild exited 0.  The actual-source forbidden-declaration
searches were empty, and the streamed target audit found only standard Lean
axioms.  Requested theorem signatures matched the draft exactly.  Parser
probes rejected the tested malformed inputs; raw sign-one/zero is accepted as
noncanonical zero.  The formal result is restricted to the explicit local
`MarkedCode` wire format.

changed_paths: `projects/aristotle_dispatch_v30/V30_REFEREE.md` (created);
`REFEREE_BRIEF.md` was pre-existing and unmodified.  No other path changed.

evidence: exact `/Users/za/.elan/bin/lake env lean` v26-cache rebuild
`lean_rebuild_exit=0`; forbidden declaration searches exit 1 with no output;
all streamed `#print axioms` lines are recorded above and end
`axiom_audit_exit=0`; keyed signature diff `requested_signature_diff_exit=0`;
`git_diff_check_exit=0`; generated-artifact scan exit 0; concrete secret-value
scan exit 1; final status was:

```text
$ git status --short --branch
## codex/rate-v30-referee-20260819
?? REFEREE_BRIEF.md
?? projects/aristotle_dispatch_v30/V30_REFEREE.md
```

attempts: Initial rebuild wait timed out at 30 seconds during dependency-cache
population; the required absolute-cache command was rerun successfully.  An
incomplete referee-worktree cache trial failed on missing `Mathlib.olean` and
was abandoned.  A malformed shell-quoting search was corrected and rerun.

assumptions: The v26 cache directory is the comparison environment even though
its tracked source is named `RateCore.lean`; the returned file is the exact
hashed artifact.  `propext`, `Classical.choice`, and `Quot.sound` are standard
Lean dependencies, not declarations introduced by the returned source.

leftovers/concerns: Full paper source-table coverage, canonical serialization,
analytic FW/AM, Ford counting, canonical normal form, and RATE-A remain
unformalized; the raw decoder's accepted noncanonical zero is outside the
proved encode-to-decode round trip.

STATUS: COMPLETE_WITH_CONCERNS (paper/source-table scope remains GAPS; noncanonical raw zero spelling)
READY FOR JUDGING

## Exact signature-command supplement — 2026-08-19

The earlier signature section quoted normalized signatures and the exit token
but abbreviated the command as a label.  The orchestrator reran the following
computed comparison against the exact hashed draft and returned files:

```bash
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 - <<'PY'
from pathlib import Path
import re
names = [
    'fw_product_gain', 'fw_product_mono', 'atomOfTag_atomTag',
    'modeOfTag_modeTag', 'statusOfTag_statusTag', 'signedNat_decode',
    'marked_code_source_injective_target', 'decode_encode_target',
    'marked_code_product_gain_target',
]
paths = {
    'draft': Path('projects/aristotle_dispatch_v30/RateCoreV.lean'),
    'returned': Path('projects/aristotle_dispatch_v30/result/aristotle_dispatch_v30_aristotle/RateCoreV.lean'),
}
def signatures(path):
    text = path.read_text()
    found = {}
    for name in names:
        match = re.search(rf'(?ms)^theorem {re.escape(name)}\b(.*?)(?=:=)', text)
        assert match, (path, name)
        found[name] = re.sub(r'\s+', ' ', f'theorem {name}{match.group(1)}').strip()
    return found
sigs = {label: signatures(path) for label, path in paths.items()}
for name in names:
    same = sigs['draft'][name] == sigs['returned'][name]
    print(f'{name}_signature_same={same}')
    if not same:
        print('draft=', sigs['draft'][name])
        print('returned=', sigs['returned'][name])
assert all(sigs['draft'][name] == sigs['returned'][name] for name in names)
print('requested_signature_diff_exit=0')
PY
```

Exact output:

```text
fw_product_gain_signature_same=True
fw_product_mono_signature_same=True
atomOfTag_atomTag_signature_same=True
modeOfTag_modeTag_signature_same=True
statusOfTag_statusTag_signature_same=True
signedNat_decode_signature_same=True
marked_code_source_injective_target_signature_same=True
decode_encode_target_signature_same=True
marked_code_product_gain_target_signature_same=True
requested_signature_diff_exit=0
```

This supplement changes no target, scope finding, or verdict.

STATUS: COMPLETE_WITH_CONCERNS (paper/source-table scope remains GAPS; noncanonical raw zero spelling)
READY FOR JUDGING

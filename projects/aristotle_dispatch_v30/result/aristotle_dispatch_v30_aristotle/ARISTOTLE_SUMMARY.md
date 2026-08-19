# Summary of changes for run 768f5d6f-6b5c-4516-981b-6d8f967b6a6b
All requested targets in `RateCoreV.lean` are now proved; the file builds warning-free with no `sorry` and no `axiom` declarations, and the interface of every requested statement is unchanged.

**Targets, final status**
- `fw_product_gain`, `fw_product_mono`, `marked_code_product_gain_target` — already proved in the supplied draft; re-verified sorry-free.
- Typed scaffolding `atomOfTag_atomTag`, `modeOfTag_modeTag`, `statusOfTag_statusTag`, `signedNat_decode` — proved. I removed three unused `simp` arguments in `signedNat_decode`, which eliminates the three lint warnings quoted in the dispatch's syntax receipt (fixing the cause, not suppressing the linter).
- `decode_encode_target` (`decode (encode c) = some c`) — proved, `sorry` removed.
- `marked_code_source_injective_target` (injectivity of `encode` on `WellFormed` codes) — proved, `sorry` removed.

**No target was false**, so the FALSE AS STATED escape hatch was not used and no statement was weakened or commented out.

**Supporting material added** (all locally proved, no axioms): `takeNatList_append`, `takeNatList_self`, `signedNat_length`, `flatMap_signedNat_length`, `decodeDigits_flatMap`, `decodeCore_append`, `decodeCores_append`. Plus the unconditional strengthening `encode_injective : Function.Injective encode` — the round trip holds for every `MarkedCode`, so injectivity does not need `WellFormed`; the requested `WellFormed`-hypothesised statement is derived from it and its hypotheses are retained (with a docstring noting they are unnecessary), since the dispatch asked for them. Three `#guard` checks pin the concrete wire format of a sample two-mark code, its round trip, and rejection of a bad header tag.

**Scope discipline**: nothing analytic is claimed. The paper-level `(FW)` estimate, Ford counting, canonical normal form, source-table coverage, and the `(AM)` atom-moment bound are untouched and remain conjectural at the Lean level; the file's header comment was updated to state exactly which serialization theorems are now machine-checked.

**Axiom audit** (`#print axioms`): only `propext`, `Classical.choice`, `Quot.sound` occur — `fw_product_gain` and `signedNat_decode` use all three, `decode_encode_target`, `marked_code_source_injective_target`, `encode_injective` use `propext`/`Quot.sound`, `fw_product_mono` only `propext`, and `marked_code_product_gain_target` none.

`DISPATCH.md` now carries a HARVEST section recording the per-target status table, the added lemmas, and the axiom audit. The returned source is a single self-contained file (`RateCoreV.lean`, `import Mathlib`) suitable for an independent v26-cache rebuild.
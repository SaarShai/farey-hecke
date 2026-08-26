# S2 ASSEMBLY — cold adversarial referee report (Fable seat)

Date: 2026-08-26. Referee: cold read-only seat (Fable). Object:
`THEOREM_G5_SECONDPIN_ASSEMBLY.md` (UNREFEREED assembly, second certified
off-line Selberg-zeta zero for G_5 + two-pin φ_5 consequence). Mandate:
refute if possible; verify every load-bearing claim against primary
artifacts with fresh computation. Interval arithmetic:
`/Users/za/.venvs/farey-rh/bin/python` with python-flint arb. All commands
run from `research_notes/rh_goals_2026-08-14/lane_g/kaggle_s2_contour/`.

---

## 1. Chunk-receipt census and directed rounding — VERIFIED (recomputed)

I re-parsed all 16 `local_receipts/S2_CHUNK_a*.json` (non-ckpt) receipts
and recomputed every aggregate from the PER-RECORD leaves, not the chunk
summary fields, asserting per-leaf `finite_Taylor_det_excludes_zero`,
`inflated_det_excludes_zero`, `rH_strictly_below_one`,
`Neumann_q_strictly_below_one`, `chunk_gate_pass`,
`complete_closed_cover`, and `status == CHUNK_ARCS_CLEAR` on every one.
Fresh output:

```
16 chunk files
total accepted: 452 subdivisions: 260 max depth: 8
min margin (per-record): [3.064554329376952e-8 +/- 3.21e-24]
max rH: [0.4947074695853866 +/- 6.07e-17]
unique F_R: 1 unique T_tail: 1 unique colsum: 1
F_R: [2.089448415544807945468931703035184024842793261502142661034...
T_tail: [1.425115035894808277428321845321694685678882628611784588173...
colsum: [37.68397782322482394233713138564839047510340211346171423952...
min margin >= 3.064554329376951375e-8 ? True
max rH <= 0.49470747 ? True
F_R <= 2.0894485e-8 ? True
T_tail <= 1.4251151e-41 ? True
 trace-norm bound: [37.68397782326745 +/- 6.62e-15]  <=37.6839779: True
all 16 chunk shas match merged receipt: True
merged census fields: 452 260
merged min margin matches per-record min: [+/- 5.67e-24]
```

Verdicts: 452 accepted subarcs, 260 adaptive subdivisions, max depth 8,
base arcs 16×12=192 — all match the doc. Directed rounding is correct in
every quoted constant: min margin 3.064554329376951375e-8 is a certified
LOWER bound (arb comparison True), max rH 0.49470747 an UPPER bound,
F_R 2.0894485e-8 UP from receipt ball 2.0894484155448079…e-8, T_tail
1.4251151e-41 UP from 1.4251150358948082…e-41, ‖L‖₁ 37.6839779 UP from
the same-endpoint trace-norm bound 37.68397782326745…, and the quoted
finite column-norm sum 37.68397782322482394… matches the receipt digit
for digit. All 16 receipts carry ONE common F_R, T_tail, and column-norm
sum. All 16 chunk sha256 values in the merged receipt match fresh hashes
of the local files.

F_R formula independently reproduced at 450-bit precision from the
receipt's own T_tail and B_same:

```
F_R recomputed: [2.089448415544807945468932e-8 +/- 2.97e-33]
receipt F_R    : 2.089448415544807945468931703035184024842793e-8
```

## 2. Winding — VERIFIED (recomputed two ways)

(a) Ball containment: the merged receipt's winding ball has midpoint
1 − 3.53e-114 with radius 1.22e-113; fresh check at 500 bits:

```
contains 1: True
width < 0.5 (unique integer): True
1-mid: [3.5277e-114 +/- 3.91e-119]
rad: [1.2200e-113 +/- 3e-122]
```

The ball contains exactly one integer, 1. The doc's width quote
(1.22e-113) matches. (b) Independent recomputation: I summed all 452
`argument_increment_records` deltas as arb balls and divided by 2π:

```
sum delta / 2pi = [1.0000000000000000000 +/- 3e-25] contains 1: True
```

## 3. Box arithmetic, reflections, gap — VERIFIED (exact decimal)

Fresh Decimal computation (exact, no rounding):

```
Re interval: 0.41054273549473627 0.41054473549473627   (= doc)
Im interval: 7.81976724701551188 7.81976924701551188   (= doc)
delta2 = 0.08945526450526373 >= 0.08945526450526372 ? True
rho2 Re: 0.58945526450526373 0.58945726450526373        (= doc)
rho2 Im: -7.81976924701551188 -7.81976724701551188      (= doc)
centre diff == 0.04335144458020843 ? True
gap == 0.04334944458020843 ? True
disjoint: True
both in (1/2,1): True
R5: lower corner Re>0: True  Im>1: True
```

δ₂ exact value is 0.08945526450526373; the doc quotes ≥ …372, correctly
rounded DOWN. The ρ₁ intervals match the first pin: centre
0.4538951800749447 ± 1e-6 (THEOREM_G5_OFFLINE_ASSEMBLY.md, constants
table line 188) reflects to Re ρ₁ ∈ [0.5461038199250553,
0.5461058199250553] and Im ρ₁ ∈ [−5.7635382417301305,
−5.7635362417301305] — exactly the doc's intervals. The banned figure
0.5894543 appears in the doc only inside the sentence banning it.

## 4. K_s exclusion and R5 domain — VERIFIED

KS_GATE_REPORT.md: exact zero lattice Re(s) = −n rows, vertical spacing
π/a_5 = 1.44915850729921 with a_5 = 2.167873726556495 — matches the
doc's s = −n + iπk/a_q with Re ≤ 0. Box₂ closed Re ≥
0.41054273549473627 > 0, so the whole-box exclusion is exact, as
claimed; no point-distance approximation is used in the doc's link 5.
TB_R5_DETERMINANT_IDENTIFICATION.md is v3.1 and defines
Ω* = {Re s > 1/2} ∪ {Re s > 0 and Im s > 1} (line 59), with h_q = 1,
κ_q = 3 (line 17). Box₂'s lower corner (0.41054273549473627,
7.81976724701551188) satisfies Re > 0, Im > 1: fresh check True/True.

## 5. Citations and attribution — VERIFIED with one correction

- MMS PDF banked: sha256 of
  `lane_g/MMS_arxiv_0912.2236.pdf` freshly computed =
  `a10020bd084534dc60fc3e887958f1583f2fc115d567961b461df1a59b32e072`,
  matching the doc's a10020bd…e072. The banked extraction
  (`.worktrees/aletheia-restore/research_notes/MMS_0912.2236_EXTRACTION.txt`
  line 108) confirms the odd-q reduced operator display is headed
  "q=2h_q+3" with h_q ≥ 1 (odd q ≥ 5); the doc's eq-(34)-vs-Thm-6.4
  correction and the heading-inconsistency disclosure implement SOL
  correction 5 verbatim.
- SCAT1_LEMMA31_ARISTOTLE.md: Lean theorem `scat1_lemma31_reflection`,
  reflection s ↦ 1−s, pole of order m at s* ⇒ zero of order m at 1−s*
  under φ(s)φ(1−s)=1, no sorry/admit — the doc attributes ONLY this
  step to the Lean core (link 7b), exactly as both seats required.
- FJS: the doc calls it "banked PDF sha 36c9d020…7228". CORRECTION
  NEEDED: that sha exists in the repo only as a recorded hash line in
  LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_SOL.md:380 pointing at
  `/tmp/fjs_2011.12795.pdf`, which no longer exists
  (`ls: /tmp/fjs_2011.12795.pdf: No such file or directory`), and no
  copy is banked anywhere in the repo (find over research_notes: no
  hit). The PDF is not "banked" in the sense the MMS PDF is.
- Interval-only phrasing: the doc contains no point-value zero claim;
  the Statement, two-pin consequence, and separation section are all
  interval statements, and the "never at its centre" caveat is present.

## 6. Merge provenance — VERIFIED with two corrections

- Merge script: fresh `shasum -a 256 merge_s2_chunks.py` =
  `1fb975c2a201b58186dc74b17e9cf7cf92a49efaf1ced798e7ec3436fdefa0b9` ✓.
- Producer runtime sha: `source_bindings.R3b_orchestrator.sha256` =
  `4ac59a18767bbf36ff39b0fb90a910685ea92b07391c352cff87ee75c8203840` in
  ALL 16 receipts (asserted in the §1 script), and fresh
  `git show 9763dba:code/second_pin/certify_r3b_flagship.py | shasum`
  in `.worktrees/aletheia-restore` = the same sha ✓.
- Reproduction: I ran the stated command with `--out` to scratch:
  `/Users/za/.venvs/farey-rh/bin/python merge_s2_chunks.py --chunk-dir
  local_receipts --out $SCRATCH/merged_repro.json`. Full recursive diff
  against the stored receipt:

```
{"merged_winding": 1, "gate_pass": true, "reason": null, ...}
diff count: 2
('/wall_seconds', '0.16953516006469727', '0.13826799392700195')
('/merge_provenance', 'missing')
```

  Every aggregate, chunk row, winding record, and gate field reproduces
  bit-identically. CORRECTION NEEDED (documentation only): the
  `merge_provenance` block is NOT produced by the sha-bound merge script
  — the reproduction lacks it — so it was appended to the stored receipt
  after the merge. Its contents all verify independently (this report,
  §§1, 6), and the doc's phrase "recreate every stored aggregate field"
  is literally true, but the doc/receipt should state the provenance
  block was added post-merge, outside the hashed script.
- Platform split digit count: local F_R = 2.0894484155448079…e-8,
  Kaggle copy = 2.0894484155449752…e-8 (fresh read of
  `chunk_receipts/S2_CHUNK_*.json`). Common prefix 2.089448415544 = 13
  significant digits; first difference at the 14th, not "the 12th" as
  the receipt provenance and doc line 76 state. Cosmetic; the
  substantive claim (both are valid upper bounds, merge gate needs one
  common F_R, local-only source) stands.

## 7. Seven-correction compliance (SOL corrections 1–7; Fable conditions 1–6)

1. Fredholm-vs-Z_{G_5} phrasing — IMPLEMENTED (links 1 and 4 claim only
   the finite/Fredholm winding; promotion runs through R5+MMS+K_s).
2. Interval-only real parts, both pins — IMPLEMENTED (§3 above).
3. FJS/Lean attribution split — IMPLEMENTED (links 7a/7b).
4. Provenance reissue with local paths, both shas, explicit command —
   IMPLEMENTED in the receipt's merge_provenance and verified (§6),
   modulo the post-merge-append disclosure above.
5. MMS eq (34) vs Thm 6.4 + heading inconsistency — IMPLEMENTED (link 6).
6. N=128 control — PARTIALLY IMPLEMENTED. The doc says receipt
   `local_receipts/S2_CONTROL_N128.json`, "result to be recorded on
   completion", NEGATIVE and NON-LOAD-BEARING. The file exists (2.0 MB,
   mtime Aug 26 03:29) but is IN-FLIGHT: `status: running`,
   `closed_contour: {}` (empty), `active_phase: closed_contour_N288`
   (a producer-script phase label that says N288 inside the N128
   control receipt — needs explanation), endpoint blocks for both 288
   and 128 CERTIFIED, N=128 F_R ≈ 1.1796e17 (so the arm mathematically
   cannot pass the ~1e-7 margins — genuinely a negative control). Both
   seats agreed non-load-bearing; SOL correction 6 permits an
   explicitly-labelled unrun control, and the doc so labels it. Not a
   refutation, but the receipt is not yet a filed result.
7. S2-specific assembly document — this document IS it; contains the R5
   domain check, MMS sector identification, whole-box K_s exclusion,
   scalar divisor source, reflected intervals, and separation.
   Fable conditions (1) provenance, (3) assembly, (4) 0.58945626450526373
   only — implemented; (2) control — in flight as above; (5) commit —
   a036-048 and the merged receipt are committed (commits 9338198,
   1288e50; fresh `git log` verified); (6) second seat — S2 assembly
   seats are this report and its counterpart.

## 8. Overclaiming audit — CLEAN

Doc status line: "UNREFEREED / CONJECTURAL as an assembly"; NOGO-OPEN-1
and NO_VERTICAL_LINE_COROLLARY stated as remaining OPEN pending a cold
referee pass of this document (lines 5–14). No sentence claims either
ledger item closed. N* floor claim (274/273, margin −2.11e-7) is backed
by S2_NSCALING_RECEIPT.md:101 verbatim. R2 receipt sha freshly verified:
`6410dff31e503176dbf03a1b181568c99f5bc386287b109ced371f08d7eee83d` ✓.

## 9. What this seat did NOT independently re-derive

Inherited from the prior refereed rounds (flagship + merged-certificate
seats): the F_R perturbation inequality as a uniform bound on
|det_Fred − det_fin| (R2/TB chain), the Sylvester/finite-section Lean
joints, the overlap-polygon homotopy lemma, per-leaf matrix rebuilds,
and the R5 v3.1 proofs themselves. No claim in the doc misstates the
scope of any of these.

---

## VERDICT

PASS-WITH-CORRECTIONS — no load-bearing claim refuted; every recomputed
constant, hash, winding, and interval matches. Required corrections,
numbered, exact:

1. FJS source is not banked. Retrieve arXiv 2011.12795, verify its
   sha256 equals 36c9d020fcc7d0118264c486330db9936f866670c45c0e77b185cdc2b9127228,
   bank it beside MMS_arxiv_0912.2236.pdf, and change link 7a's "banked
   PDF" to cite the in-repo path. Until then the doc's word "banked" is
   false (the sha survives only as a hash line over a deleted /tmp file).
2. Disclose in the doc (and/or a receipt note) that the
   merge_provenance block was appended to S2_MERGED_CONTOUR_RECEIPT.json
   after the merge and is not emitted by merge script sha 1fb975c2…f0b9;
   the reproduction command recreates every field EXCEPT merge_provenance
   and wall_seconds.
3. Correct "12th significant digit" (doc line ~76 and the receipt's
   chunk_source text) to "14th significant digit" for the local/Kaggle
   F_R platform split (common prefix 2.089448415544; local …8079 vs
   Kaggle …9752).
4. The N=128 control receipt is in-flight, not filed: on completion,
   record the honest-fail result in the doc's Controls section, and
   explain the producer's `active_phase: closed_contour_N288` label
   appearing inside the N128 control receipt (script phase-name
   artifact vs actual N of the contour phase).

Corrections 2–4 are documentation-level; correction 1 is an artifact
gap. None affects the certified mathematics: the second winding box,
the box/reflection/gap arithmetic, the whole-box K_s exclusion, the R5
domain membership, and the two-pin distinct-real-parts interval
statement all verify under fresh computation.

VERDICT: PASS-WITH-CORRECTIONS

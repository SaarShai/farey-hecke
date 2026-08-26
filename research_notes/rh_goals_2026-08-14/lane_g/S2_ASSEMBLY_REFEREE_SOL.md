# S2 assembly — cold adversarial referee report (SOL seat)

Date: 2026-08-26. Object: `THEOREM_G5_SECONDPIN_ASSEMBLY.md`.
Mandate: attempt refutation; read-only except this report. Arithmetic used
`/Users/za/.venvs/farey-rh/bin/python` with python-flint Arb/Acb. All bounds
were tested upward and all claimed positive margins downward.

## Executive ruling

I did not refute the N=288 contour certificate, its Fredholm-to-Selberg
promotion, the existence of an S2 zero in the stated box, or the numerical
separation of the two reflected real intervals. The 16 selected local chunk
receipts hash correctly, tile the full contour, pass every leaf gate, reproduce
the stored aggregate, and pin winding 1. The whole closed S2 box lies in R5's
domain and is disjoint from the exact `K_s` zero lattice. MMS Theorem 6.4 and
the banked FJS source support the stated factorization/divisor chain, subject to
the disclosed MMS q=5 heading inconsistency.

The document is not passable verbatim. It contains a literal conjugation error
in the load-bearing reflection sentence, does not explicitly instantiate the
new FJS/Lean `phi_5` bridge for the first pin, and violates its own
interval-only rule twice. These are repairable assembly defects rather than a
numerical refutation. Exact required corrections are in section 10.

## 1. Sixteen-receipt census and directed rounding

I parsed the 16 paths in
`kaggle_s2_contour/chunk_receipts/S2_MERGED_CONTOUR_RECEIPT.json:/merge_provenance/chunk_paths`,
resolved each against `kaggle_s2_contour/`, checked its SHA-256 against the
corresponding merged `chunks[]` row, and recomputed the extrema from all 452
leaf records. Fresh output:

```text
files = 16 hashes_match_merged = True ranges_tile_[0,192) = True
base_arcs = 192 accepted = 452 subdivisions = 260 achieved_max_depth = 2
all_chunk_and_leaf_gates = True
min_margin_raw = [3.064554329376951755251952620056559943464231764407801654136005686437949e-8 +/- 7.54e-80]
min_margin_location = S2_CHUNK_a156-168.json 160 160R
directed_DOWN min_margin >= 3.064554329376951375e-8 = True
max_rH_raw = [0.4947074695853866606598702474252877049237070105385758646375757391893828 +/- 6.25e-72]
max_rH_location = S2_CHUNK_a168-180.json 169 169R
directed_UP max_rH <= 0.49470747 = True
unique_endpoint_F_R = 1
F_R_raw = [2.089448415544807945468931703035184024842793261502142661034292555539032e-8 +/- 3.13e-78]
directed_UP F_R <= 2.0894485e-8 = True
merged_min_margin_same_ball = True
```

Thus the assembly's 452 accepted leaves, 260 subdivisions, positive rounded-
down margin, rounded-up `rH`, and rounded-up `F_R` are valid. The actual
achieved leaf depth is 2; the document's `max depth <= 8` is true but reports
the configured ceiling rather than the observed maximum.

The other determinant-comparison constants also check. The finite-column sum
is a displayed value, not itself the rounded public upper bound:

```text
T_tail_raw = [1.425115035894808277428321845321694685678882628611784588173559981095157e-41 +/- 1.54e-111]
T_tail_directed_UP_le_1.4251151e-41 = True
finite_column_sum_raw = [37.68397782322482394233713138564839047510340211346171423952849789870793 +/- 9.20e-70]
trace_norm_raw = [37.68397782326745282140803434563768428634677894256952217876356611256717 +/- 2.73e-69]
trace_norm_directed_UP_le_37.6839779 = True
```

Replaying `F_R=T_tail*exp(1+2*B_same)` from serialized upper inputs gives the
same displayed bound and remains strictly below the public upward rounding:

```text
T_tail.upper = [1.4251150358948082774283218453216946856788826286117845881735599810951568460723634e-41 +/- 3.93e-121]
B_same.upper = [37.683977823267452821408034345637684286346778942569522178763566112567172722150887 +/- 1.44e-79]
F_R replay from serialized UP inputs = [2.0894484155448079454689317030351840248427932615021426610342925555390316877716084e-8 +/- 1.90e-88]
F_R stored receipt = [2.0894484155448079454689317030351840248427932615021426610342925555390316877716084e-8 +/- 1.90e-88]
replayed valid upper < 2.0894485e-8 = True
stored valid upper < 2.0894485e-8 = True
```

## 2. Independent merge replay and winding pin

Command, run with the required interpreter from `lane_g/kaggle_s2_contour/`:

```text
/Users/za/.venvs/farey-rh/bin/python merge_s2_chunks.py \
  --chunk-dir local_receipts \
  --out /tmp/S2_MERGED_CONTOUR_REFEREE_REPLAY.json
```

Fresh output and recursive field comparison:

```text
{
  "merged_winding": 1,
  "gate_pass": true,
  "reason": null,
  "out": "/tmp/S2_MERGED_CONTOUR_REFEREE_REPLAY.json"
}
AGGREGATE_REPLAY_EQUAL_EXCEPT ['merge_provenance', 'wall_seconds'] True
F_R_upper_bound MATCH
N MATCH
chunks MATCH
closed_contour_gate_pass MATCH
expected_base_closed_arc_count MATCH
merged_winding MATCH
minimum_finite_lower_minus_F_margin MATCH
note MATCH
schema MATCH
status MATCH
winding_info MATCH
```

The exclusion of `merge_provenance` is intentional: that block was appended
after the merge and the assembly now discloses this. `wall_seconds` is
nondeterministic.

I also reparsed the stored winding ball and independently re-summed all 452
serialized argument increments:

```text
argument_increment_records = 452
stored_winding_ball = [0.99999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999647226100000 +/- 1.23e-113]
stored_contains_1 = True
stored_unique_integer_1 = True
candidate_integer = 1 integer_pinned = True merged_winding = 1
serialized_delta_resum_over_2pi = [1.0000000000000000000000000000000000 +/- 3e-40]
serialized_resum_unique_integer_1 = True
```

This establishes one zero counted with multiplicity for the analytic Fredholm
determinant inside Box2. Because the winding is exactly 1, the zero is simple.

## 3. Box, reflection, and separation arithmetic

Exact decimal endpoint arithmetic was cross-checked with Arb interval
inequalities. Fresh output:

```text
S2_Re_closed = 0.41054273549473627 0.41054473549473627
S2_Im_closed = 7.81976724701551188 7.81976924701551188
delta2_exact = 0.08945526450526373 quoted_DOWN_0.08945526450526372_valid = True
rho1_Re_closed = 0.5461038199250553 0.5461058199250553
rho1_Im_closed = -5.7635382417301305 -5.7635362417301305
rho2_Re_closed = 0.58945526450526373 0.58945726450526373
rho2_Im_closed = -7.81976924701551188 -7.81976724701551188
reflected_centre_difference_exact = 0.04335144458020843
closed_interval_separation_exact = 0.04334944458020843
separation >= 0.04334944458020843 = True
real_intervals_disjoint = True
both_reflected_intervals_inside_(1/2,1) = True
Arb_rho_gap_strictly_positive = True
```

The claimed lower separation `0.04334944458020843` is exact, not merely a
rounded estimate. The displayed negative imaginary intervals are those of
`rho_i=1-s_i`.

## 4. Whole-box `K_s` exclusion and R5 domain

`KS_GATE_REPORT.md:39-59` derives
`det(1-K_s)=product_{n>=0}(1-ell_5^(2s+2n))`, hence the exact zero lattice
`s=-n+i*pi*k/a_5`, whose real parts are `-n <= 0`.
`TB_R5_DETERMINANT_IDENTIFICATION.md:57-66` states determinant equality on

```text
Omega* = {Re s > 1/2} union {Re s > 0 and Im s > 1}.
```

The same fresh Arb box computation gives:

```text
Arb_box_Re = [0.41054373549473627000000000000000000 +/- 1.01e-6]
Arb_box_Im = [7.8197682470155118800000000000000000 +/- 1.01e-6]
Arb_whole_box_Ks_exclusion_by_Re>0 = True
Arb_R5_second_component_Re>0_Im>1 = True True
```

Therefore `det(1-K_s)` is nonzero on the entire closed box by horizontal
separation alone; the older point-distance precision issue is irrelevant.
The entire box, not merely its centre, lies in R5's second component.

## 5. Provenance, platform split, and control arm

The explicit local paths, merge hash, producer hash, local-only command, and
post-merge disclosure are present. Fresh checks:

```text
local_F_R = 2.08944841554480794546893170303518402484279326150214266103429255553903168777160838104954000553255960867179384564034473972e-8
kaggle_F_R = 2.08944841554497520863892307386648173354244770597320612790733059618003593619919947219887582026217633244896118392991260411e-8
common_significant_prefix = 2089448415544 length = 13
first_differing_significant_digit = 14 local_digit = 8 kaggle_digit = 9
all_16_source_binding_maps_identical = True
all_16_runtime_producer_sha = ['4ac59a18767bbf36ff39b0fb90a910685ea92b07391c352cff87ee75c8203840']
provenance_chunk_paths = 16 all_local_prefix = True
merge_script_sha_matches = True
post_merge_append_disclosed = True
1fb975c2a201b58186dc74b17e9cf7cf92a49efaf1ced798e7ec3436fdefa0b9  merge_s2_chunks.py
4ac59a18767bbf36ff39b0fb90a910685ea92b07391c352cff87ee75c8203840  -
```

The first local/Kaggle difference is indeed the 14th significant digit. Both
values are upper bounds, not enclosures of one unique real; selecting the
homogeneous local family is valid. The current producer differs from the
archived runtime producer only by added platform/version receipt fields.

The N=128 control is a completed, honest failure, while its N=288 comparison
certifies the same base arc:

```text
receipt_status = complete all_theorem_gates_pass = False
N128_status = NOT_CERTIFIED failure_arc = 0 lineage = 0 depth = 0
N128_rH_failure = [1.216520408071738556634537104247536255194316310344245802845259828417602 +/- 1.74e-70]
N128_rH_strictly_greater_than_1 = True
N128_accepted = 0 complete_cover = False
N288_same_base_arc_status = CHUNK_ARCS_CLEAR chunk_range = [0, 1] accepted = 2 chunk_gate_pass = True
N288_same_arc_min_margin = [3.723915177842620411796068033909077298753944334062499245e-6 +/- 4.54e-61]
```

The control receipt has two inherited metadata defects that do not change the
nested result:

```text
date_field = 2026-08-14
updated_unix = 1787742797.112471 utc = 2026-08-26T11:13:17.112471+00:00
top_level_verdict = THEOREM-GRADE closed-contour NO at N=288
top_level_status = complete
N128_status = NOT_CERTIFIED
N288_control_scope = [0, 1]
```

The assembly reads the authoritative nested `closed_contour[128]` fields
correctly, but the inherited date and generic top-level verdict should be
normalized or explicitly disclosed in the control receipt.

## 6. MMS citation and q=5 scope

Fresh SHA-256:

```text
a10020bd084534dc60fc3e887958f1583f2fc115d567961b461df1a59b32e072  research_notes/rh_goals_2026-08-14/lane_g/MMS_arxiv_0912.2236.pdf
```

Fresh source transcription from `pdftotext -layout` (typographic operators
normalized only):

```text
Theorem 6.4. The Selberg zeta function ZS (s) for the Hecke triangle group Gq
can be written as
                         det (1 - Ls )   det [(1 - Ls,+ )(1 - Ls,- )]
                ZS (s) =               =                              ,
                         det (1 - Ks )           det (1 - Ks )
where Ls , Ls,+/- and Ks ... are the transfer operators given by Theorem 4.10,
(32)-(34) and (42)-(43), respectively.
```

The source separately prints:

```text
For q = 2hq + 3 > 5 we get
```

above equation (34), while its general incidence formulas and Lemma 6.3 say
odd `q >= 5`. The assembly correctly cites Theorem 6.4, not equation (34), for
the determinant quotient and explicitly discloses the inconsistent printed
heading. R5 supplies the local `h_q=1`, three-component q=5 identification.
This is an honest source caveat, not a hidden citation substitution, but a
publication should label the q=5 equation-(34) use as an independently derived
specialization rather than silently treating the printed heading as applicable.

The same PDF states Theorem 4.10's poles are only the real points
`s_k=(1-k)/2`, and states that all Hecke triangle groups have one cusp. Thus
the minus determinant is analytic near both nonreal boxes and the trivial-
representation scattering matrix is scalar.

## 7. FJS attribution and Lean scope

The PDF is now genuinely banked at
`research_notes/rh_goals_2026-08-14/lane_p/literature/FJS_completed_zeta_divisor.pdf`.
Fresh hash:

```text
36c9d020fcc7d0118264c486330db9936f866670c45c0e77b185cdc2b9127228  research_notes/rh_goals_2026-08-14/lane_p/literature/FJS_completed_zeta_divisor.pdf
```

Fresh primary-source transcription from `pdftotext -layout` (typographic
operators normalized; the extractor drops the overbar on the second `rho`):

```text
Definition 3.8. We define completed zeta functions Z+ and Z- as

                                                  Z(s)
                               Z+ (s) =                       ,      Z- (s) = Z+ (s)phi(s),
                                          G1 (s)(Gamma(s - 1/2))^k

where G1 (s) is defined in (3.9) and phi(s) is the scattering determinant.
...
4. At each point s = 1 - rho, 1 - rho where rho is a zero of phi(s)
   with Re(rho) > 1/2 and Im(rho) > 0.
```

The PDF's scattering divisor also lists poles at the reflected left-half-strip
points and zeros at the right-half-strip points. Since the gamma/`G_1` trivial
divisors are real and both pin boxes are nonreal, a pin zero is a pole of
`phi_5` of matching order. The functional equation then gives a zero at
`1-s`.

The finished nested Lean artifact is sorry-free and its local build log ends
`Build completed successfully (8034 jobs)`. The root dispatch stub still
contains `sorry`, but `SCAT1_LEMMA31_ARISTOTLE.md:56-72` correctly identifies
the finished nested file and successful re-elaboration. Lean proves only:

```text
pole of phi at sstar  =>  zero of phi at 1 - sstar,
under phi(s) phi(1-s) = 1.
```

It does not prove the FJS Selberg-to-scattering divisor step. The target
document correctly separates these at lines 141-159.

## 8. Seven SOL corrections

Against `S2_MERGED_REFEREE_SOL.md:213-221`:

1. **Receipt scope:** implemented. Lines 59-115 keep the receipt at the
   Hilbert/Fredholm level and use R5 + MMS + zero-free `K_s` separately.
2. **Both reflected intervals:** implemented at lines 35-50; the banned
   `0.5894543` occurs only in a warning not to reuse it.
3. **FJS versus Lean attribution:** substantially implemented at lines
   141-159. Residual: only S2 is explicitly composed; the first-pin `rho_1`
   assertion is not explicitly run through the same bridge.
4. **Merged provenance:** implemented through the 16-entry
   `merge_provenance.chunk_paths` list, both hashes, and explicit command.
   `chunks[].file` remains a basename, but the path list maps one-to-one by
   basename and order. Post-merge append is disclosed.
5. **MMS citation:** implemented at lines 126-137, including the heading
   inconsistency and q=5 local specialization.
6. **N=128 control:** implemented at lines 177-190; the result is complete,
   negative, and expressly non-load-bearing.
7. **S2 assembly:** substantially implemented: R5 domain, sector, whole-box
   `K_s`, scalar source, intervals, and gap are present. The first-pin bridge
   omission above prevents an unqualified two-`phi_5`-zero assembly pass.

## 9. Interval and overclaim audit

The theorem statement and both reflected coordinates are intervals, and lines
47-50 explicitly prohibit treating a box centre as the zero. No equality
`Re(rho_i)=centre` appears. However, lines 31 and 138 say `Im(s2) approximately
7.82`, which is point-like shorthand contrary to the document's own sentence
that only interval statements are licensed. The nonreality and pole-set
arguments should instead cite the positive imaginary interval.

The attempted NOGO overclaim refutation failed. Fresh text scan:

```text
11:remain **OPEN** until a cold adversarial referee passes THIS document.
```

The document claims the two-pin *premise*, not closure of NOGO-OPEN-1. This is
correct: the downstream metatheorem still must instantiate
`M=(phi_5,D) in M(A)` and pass its own referee gate.

One non-load-bearing control sentence is too broad. Line 179 calls N=274 the
`N* floor`, while `S2_NSCALING_RECEIPT.md:99-107` defines it against one
bottom-edge midpoint point probe and expressly warns that full interval arcs
may require subdivision. It is not a proven minimum N for the full contour.

## 10. Required corrections, exact

1. **Correct the reflection and divisor direction.** Replace lines 153-161's
   `pole/zero` and `rho₂ = 1 − s̄-type reflection` wording by:
   `FJS identifies s₂ as a pole of φ_5 of the same order. By the Lean
   reflection core, φ_5 has a zero ρ₂ := 1 − s₂ of the same order.`
   There is no conjugation in this step. The currently displayed negative-
   imaginary `rho2` interval is already the correct image under `1-s2`.

2. **Instantiate the first pin explicitly.** Add the parallel sentence:
   `Applying the same FJS divisor step and Lean reflection core to the first-pin
   zero s₁ gives the φ_5 zero ρ₁ := 1 − s₁ in the stated ρ₁ box.`
   Do not say link 7 is inherited unchanged from
   `THEOREM_G5_OFFLINE_ASSEMBLY.md`: that document's link 7 is only the
   standard resonance interpretation and does not contain this FJS/Lean
   scalar-`phi_5` bridge.

3. **Make interval-only phrasing literal.** Replace line 31's
   `Im(s₂) ≈ 7.82 ≠ 0` with
   `Im(s₂) ∈ [7.81976724701551188, 7.81976924701551188] ⊂ (0,∞)`.
   Replace line 138's `Im ≈ 7.82` parenthetical by the same box-
   interval fact. Keep centres only when explicitly labelled as box centres.

4. **Qualify the N-scaling control.** Replace line 179's `N=274 measured
   floor` by `N=274 bottom-edge-midpoint point-probe floor; N=273 fails that
   probe`. Add that this is not a minimum-N theorem for the full contour and is
   non-load-bearing for the N=288 certificate.

Receipt hygiene, recommended but not verdict-bearing: normalize the N=128
control receipt's inherited `date` and generic top-level N=288 `verdict`, and
have the merge script emit the verified provenance block itself so future
replays do not require a disclosed post-merge append.

No required correction changes the certified box, margin, winding, R5 domain,
`K_s` exclusion, FJS/MMS source content, or rigorous real-part separation.

VERDICT: PASS-WITH-CORRECTIONS

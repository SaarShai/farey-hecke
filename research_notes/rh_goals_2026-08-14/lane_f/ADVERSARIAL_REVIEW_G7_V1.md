# ADVERSARIAL REVIEW G7 V1 — hostile cold pass on the assembled q=7 theorem

Reviewer: independent frontier verifier, 2026-08-17. Target:
`THEOREM_G7_OFFLINE_ASSEMBLY.md` (STATUS: ASSEMBLED) and its full evidence
chain. This is link-table row 8, the gating item.

Independence: the reviewer wrote none of the target, ran no `git` command, and
recomputed every load-bearing constant from `λ_7 = 2cos(π/7)` upward with its
own scripts before comparing with any receipt. Interpreters:
`/Users/za/.venvs/farey-rh/bin/python` (python-flint Arb/Acb, 384 bits) and
mpmath at dps 50–60 as a second, structurally different arithmetic.

**RULING: SOUND-WITH-REPAIRS.** No theorem-level defect. The stated theorem —
`Z_S` has a zero `s*` in the box, hence `Re(s*) ≤ 0.4751658 < 1/2` and
`δ ≥ 0.0248342` — is fully supported by evidence reproduced independently here.
One printed bound in the Link-5 lemma is FALSE and must be corrected
(D1); two editorial defects and two disclosure defects follow.

---

## Attack 1 — independent recomputation of the K_s / lattice constants

Probe: `crg7_recompute.py`, `crg7_detK.py` (mpmath, dps 50–60), plus a
byte-level replay of the flint generators. Nothing was read from the manifest
before computing.

| Quantity | Doc / receipt claim | Reviewer's independent value | Verdict |
|---|---|---|---|
| λ_7 | 1.801937735804838252472204639014890102331… | 1.801937735804838252472204639014890102332 | **CONFIRMED-SOUND** |
| min poly | x³−x²−2x+1 contains 0 | m(λ_7) = 0.0 (deg 3; x³+x²−2x−1 gives 4.494, so the polynomial is not interchangeable) | **CONFIRMED-SOUND** |
| word M₂M₁M₂M₁M₁ | det = 1, trace = 4λ²+3λ | det = 1.0; trace = 18.3937316222843830016166529891 = 4λ²+3λ exactly; all three cyclic rotations agree (LAW's word [1,1,2,1,2] is a rotation) | **CONFIRMED-SOUND** |
| τ_7 | ≥ 18.393731622284383001616652 (rounded DOWN) | 18.3937316222843830016166529891 — truncation direction correct | **CONFIRMED-SOUND** |
| ell_7 | 0.05452799479805249083392519594349… | 0.05452799479805249083392519594349369522759 | **CONFIRMED-SOUND** |
| a_7 | 2.909041043174856595598222179862… | 2.909041043174856595598222179862414856901 | **CONFIRMED-SOUND** |
| π/a_7 | 1.079940986381249360096096828198… | 1.079940986381249360096096828198450774439 | **CONFIRMED-SOUND** |
| b_7 = ell² | 0.00297330221669643950… | 0.002973302216696439500642434287943555993; the INDEPENDENT LAW orbit-product route (`lane_g/law_probes/q3diag_detK.json`, κ=5, word [1,1,2,1,2]) gives 0.0029733022166964396 — two derivations agree | **CONFIRMED-SOUND** |
| box→lattice distance | ball [0.5895479897495818278130858801517574259447 ± 3.93e-41]; ≥ 0.5895479 | 0.5895479897495818278130858801517574259447 — **40-digit exact match**; nearest point (n,k) = (0,4) at Im = 4.3197639455249974404 confirmed as nearest by exhaustive scan n∈[0,5], k∈[−2,11] | **CONFIRMED-SOUND** |
| 2nd-nearest (0,5) | box distance ≥ 0.8718275 | 0.8718275833588685562763613416244441652382 | **CONFIRMED-SOUND** |
| centre→lattice | 0.5895493876724655… | 0.58954938767246553569 (= manifest point margin 0.589549387672466) | **CONFIRMED-SOUND** |
| manifest erratum | manifest §4.3/§7 "≈ 0.5895480" is a round-UP | **CONFIRMED**: manifest lines 210 and 270 print 0.5895480; true value 0.58954798975 < 0.5895480, so the manifest overstates the margin by 1.0e-8. (The manifest's own derivation `point − √2·1e−6` yields 0.58954797345, also below its printed 0.5895480.) The doc's honest rounded-DOWN 0.5895479 verifies: `best > arb("0.5895479")` is True | **CONFIRMED-SOUND (erratum valid)** |
| σ_lo on box | ≥ 0.4751637 | 0.4751637621098225 | **CONFIRMED-SOUND** |
| δ | 1/2 − Re₀ − 1e−6 = 0.02483423789017750, ≥ 0.0248342 | 0.0248342378901775 — rounded DOWN correctly | **CONFIRMED-SOUND** |
| corrected Re(s*) | ≤ 0.4751658 | Re₀ + 1e−6 = 0.4751657621098225 ≤ 0.4751658, rounded UP correctly | **CONFIRMED-SOUND** |
| plan erratum | plan's 0.4751648 omits the half-width | **CONFIRMED**: `F7_CERT_PLAN.md:8` prints "Re(s*) ≤ 0.4751648 < 1/2", which is Re₀ rounded up, not a bound on the closed box | **CONFIRMED-SOUND (erratum valid)** |
| det(1−K_s) LOWER | 0.936818983390 | Π_{n<24}(1−t_n)·(1−tail) = 0.9368189833904026963 — exact match to the receipt ball [0.9368189833904026963033671209126567399736 ± 2.62e-41]; t₀ = 0.063004963346649393574 ≤ 0.063004963347 ✓; per-factor min 0.93699503665335060643 ≥ 0.936995036653 ✓ | **CONFIRMED-SOUND** |
| det(1−K_s) UPPER | ≤ 1.000000000001, "certified" | **REFUTED — see DEFECT D1** | **DEFECT** |

Every generator replays byte-identically: `f7links_ks_gate.py` and
`f7links_e1_recheck.py` were re-run and the two receipts diffed against
pre-run copies — **BYTE-IDENTICAL**, exit 0 both.

## Attack 2 — assembly integrity

`assemble_f7.py` re-run by the reviewer (no `--write`):

```
verdict: THEOREM-GRADE closed-contour YES at N=256
gate_pass: coverage/hash_pinning/seam_closure/margins/arc_exclusions/winding/comparison_control_arm = all true
winding: 1   winding_ball: [0.99999…998426476 +/- 5.17e-114]
min_margin_down: 0.00000241285276269068356797445   max_rH_up: 0.211064737207127407537372
accepted_subarcs: 192   seam_failures: []
```

Reproduces the banked receipt exactly. But the assembler is the author's own
code, so every gate was **re-derived from the 16 raw chunk receipts by the
reviewer's own script**, all 16 checked, none sampled:

| Check | Reviewer's evidence | Verdict |
|---|---|---|
| Coverage tiles [0,192) once | 16 `chunk_arc_range`s = [0,12),[12,24),…,[180,192); union == set(range(192)); 12 records each, 192 total; `base_arc_index` multiset == 0..191 | **CONFIRMED-SOUND** |
| Per-chunk minima match raw | recomputed min over each chunk's 12 raw `finite_lower_minus_F_margin` balls; global min 2.41285276269068356797445899437e-6 in **chunk-06** — matches the doc's "attained in chunk-06" and rounds DOWN to 2.41285e-6 | **CONFIRMED-SOUND** |
| Per-arc gates, all 192 | `finite_Taylor_det_excludes_zero`, `inflated_det_excludes_zero`, `rH_strictly_below_one`, `Neumann_q_strictly_below_one` all True on 192/192; every margin ball > 0. Failure list: `[]` | **CONFIRMED-SOUND** |
| Accepted whole / splits 0 | `subdivision_depth` set == {0} across all 192; accepted subarcs 12/12 per chunk. The doc says "adaptive splits 0" — correct, and (unlike q=5 defect 1-C1) it does NOT misreport the depth-8 budget as an achievement | **CONFIRMED-SOUND** |
| Edge census | 48 arcs each on bottom/left/right/top = 4 × 48 | **CONFIRMED-SOUND** |
| Seam closure, all 192 | reviewer's own Arb comparison of `s_end[k]` vs `s_start[(k+1) mod 192]`, tolerance 1e−60, for all 192 junctions **including the 191→0 wrap**: 0 failures | **CONFIRMED-SOUND** |
| Winding ball, INDEPENDENT | reviewer summed atan2 argument increments of the 192 `midpoint_det` values without using the orchestrator's polygon method: **1.0000000000000004** | **CONFIRMED-SOUND** |
| rH, rG global | max rH = 0.21106473720712740754 → 0.211065 (UP) ✓ < 1; max rG = 8.8850044057198788757e-7 → 8.88501e-7 (UP) ✓ | **CONFIRMED-SOUND** |
| Control arm N=224 | `NOT_CERTIFIED`, `accepted_closed_subarc_count: 0` in **all 16** chunks — the designed failure fires | **CONFIRMED-SOUND** |
| Hash pinning, all 16 | the tuple of every `*_sha256` field is identical across all 16 receipts; `source_bindings` pins R2 `4e5f0105…9202efc`, TB_V2 `93baddf5…251f4f6`, engine `b6ee87fd…e28a0f`, and the E1 receipt's `immutable_inputs` carry the SAME R2/TB_V2 shas | **CONFIRMED-SOUND** |
| Engine-drift explanation | `shasum -a 256 …/out/kaggle_top4/hecke-gap-sweep/zeta_cert_rosen.py` = **b6ee87fd8f35f0b704323a1f4c0f7d1c510b5ac6c79a0d6dbf58c95d70e28a0f** — the certified bytes ARE recoverable at the documented path; live primary path is `965c2e5f…` (drifted, as disclosed) | **CONFIRMED-SOUND, honestly disclosed** |
| Link-3 endpoint constants | chunk receipt: column-norm sum 20.16963692338443550953513186…, output-tail corrections 7.706042496573776902616531e-13, T_tail(256) 2.411487076500882178674099513617e-27 → `same_endpoint_trace_norm_bound` 20.169636923385206113784789246469… → 20.1696370 (UP) ✓; F_R 2.16622446489421717768358726940…e-9 → 2.16623e-9 (UP) ✓; T_tail → 2.41149e-27 (UP) ✓ | **CONFIRMED-SOUND** |
| margin / F_R | 2.41285276269068e-6 / 2.166224464894e-9 = **1113.85** ≈ 1.11e3 ✓. The q=5 comparison also checks: q=5's 3.43786e-8 / 1.77974e-6 = 1.93% ≈ "2% of F_R" | **CONFIRMED-SOUND** |
| B_total not theorem-valid | R2 receipt `B_total` = 119.06285559909506923733… — the doc correctly labels it a comparison envelope and uses 20.1697 instead | **CONFIRMED-SOUND** |

## Attack 3 — logic audit

| Probe | Finding | Verdict |
|---|---|---|
| **Is the E1 V2 receipt q=7 or a stale q=5 port?** | Genuinely q=7. 19 blocks with labels spanning discs 1..5 (κ_7 = 5, not κ_5 = 3): `1→4,+2,head` … `5→5,−2,tail`; `radius_multipliers_exact_strings` = ["3.522","2.622","2.372","1.79","1.6"] matching the R2 receipt's `exact_factor_strings`; `max_N` 256; `immutable_inputs` carry the q=7 R2/TB_V2 shas. **Not stale.** | **CONFIRMED-SOUND** |
| E1 extremal claims, per block | reviewer re-extracted all 19 raw balls: worst ratio ρ̂ = 0.9152411837446921486199057 at block **5→3, +1, head** → 0.9152412 (UP) ✓; min remaining clearance 0.9915072451437825333425458 at block **3→1, +1, head** → ≥ 0.9915 ✓; max enlargement 0.04282750414706513326732806 → ≤ 0.0429 ✓; headroom 0.9915/0.0429 = **23.1**, matching the doc's "factor ≳ 23" and its refusal to claim three orders; η = 1/1.15 = 0.869565217391304… → 0.8695653 (UP) ✓ for all 19 | **CONFIRMED-SOUND** |
| **R5 lemma: is the n ≥ 0 product truncated silently?** | **No — a rigorous tail bound is present and correct.** The lemma uses Π_{n≥24}(1−t_n) ≥ 1 − Σ_{n≥24} t_n (Weierstrass, valid for t_n ∈ [0,1)), with Σ_{n≥24} t_n = t₀·ell⁴⁸/(1−ell²). Reviewer's value 1.440141902e-62 ≤ the claimed 1e−60 ✓. The generator implements exactly this (`f7links_ks_gate.py:205`). The task's suspicion is unfounded for the load-bearing lower bound. | **CONFIRMED-SOUND** |
| E1 recheck vs V2 receipt | `f7links_e1_recheck.py` consumes `F7_E1_ENLARGED_CONTRACTION_V2_RECEIPT.json`, re-derives ρ̂, η, R_enl = R+e, remaining = clearance − e, and the cap rule e = min(clearance/4, 0.15R) from raw balls — 19/19 blocks, 10 checks each, no summary literal trusted. It does NOT re-certify the ratio balls themselves; the doc discloses precisely this at caveat (iii) ("a re-run of the same method, not an independent implementation"). No overclaim. | **CONFIRMED-SOUND** |
| **Sector scope: is the statement scoped to match mms+/sign=+1?** | Yes, and correctly. The sector restriction is internal to the METHOD (the certified winding is of the + sector's Fredholm determinant); the CONCLUSION is about `Z_S`, which is sector-independent, and passes through MMS 6.4 legitimately. The doc claims **no parity label** and says so twice. `κ_7 = q−2 = 5`, `h_7 = 2`, `q = 2h+3 = 7` are internally consistent. | **CONFIRMED-SOUND** |
| Zero survives the factorization | `Z_S = det(1−L₊)·det(1−L₋)/det(1−K)`. `det(1−L₊)(s*) = 0`; `det(1−L₋)` analytic near Box (MMS 4.10 poles only at real s = (1−k)/2, Box has Im ≈ 4.67) so it contributes no cancelling pole; `det(1−K)` non-vanishing (verified). Zero × analytic / non-zero = zero. Multiplicity claim ("at least that of the + factor") is correct. | **CONFIRMED-SOUND** |
| Argument principle needs analyticity | Simon Adv. Math. 24 (1977) Thm 3.3 is cited for exactly this and appears in the CITED ledger. | **CONFIRMED-SOUND** |
| ρ̂ vs ρ* vs rH conflation | The doc devotes a labelled paragraph to keeping rG/rH (Link 1, s-contour mean-value device) apart from ρ̂ (Link 4b, z-geometry) and lists ρ* ≤ 0.763213 and ρ̂ ≤ 0.9152412 side by side with a do-not-conflate warning. ρ* verified against TB_V2's `[0.763212029206899202166157 ± 1.41e-25]` → 0.763213 (UP) ✓. This is q=5 defect 1-C6 **fixed**. | **CONFIRMED-SOUND** |
| GK comparison endpoint provenance | Two independent runs exist: the chunk receipts' `endpoint_trace_bounds/256` (20.169636923385206113784789246469…) and `F7_R3B_ENDPOINT_V2_RECEIPT.json` `/bounds/256` (20.169636923385172661643267982167…). They differ at the 21st digit; both are ≤ 20.1696370, so the printed bound covers both. Not a defect — but the doc cites both files for "the" constant without noting they are two runs. | **CONFIRMED-SOUND (see O2-adjacent note)** |
| MMS eq-34 heading condition | Arithmetically sound at q=7 (2h_q+3 = 7 > 5, and q=7 ≥ 5 for Lemma 4.2). **But not repo-verifiable — see DEFECT D5.** | **DEFECT (disclosure)** |

## Attack 4 — statement audit

Rounding directions were checked one by one against the reviewer's own values.
Every error bound in the constants table rounds UP and every quantity rounds
DOWN, as the table's own header promises — with the single exception of D1.
No "declared" language survives: the doc says **ASSEMBLED — NOT YET DECLARED**
in the status block, repeats it in "What remains open" item 1, and files its own
missing review as link-table row 8 **GAP**. The epistemic self-labelling is
honest and, if anything, harder on itself than necessary.

Defects found: **D1** (false printed bound), **D2** (link renumbering
collision), **D3** (mis-attributed erratum).

## Attack 5 — recurrence of the q=5 hostile-round defect classes

Checked against `lane_g/ADVERSARIAL_AUDIT_KIMI_K3.md` (1-E1…1-E9, 1-C1…1-C8)
and the V4–V8 rounds.

| q=5 class | Recurs at q=7? | Evidence |
|---|---|---|
| **1-E1** Lean v18 lemmas were `sorry`-only, no result tarball | **NO — fixed.** The q=7 doc reuses `det_one_sub_proj_mul_proj` and `trace_unitary_le_sum_column_norms` and the artifact now exists: `projects/aristotle_dispatch_v18/project_aristotle/project_aristotle/R1Lemmas.lean` has **0 `sorry`**, both theorems proved, `#print axioms` commands present, summary reports `[propext, Classical.choice, Quot.sound]`. The v19 joints (`l2_le_card_mul_sup_sq`, `coeff_bound_of_uniform`, `geom_tail_le`) are in `aristotle_dispatch_v19/project_aristotle/R1Completion.lean`, **0 `sorry`**. *Reviewer caveat: no Lean build was executed here; the axiom-cleanliness rests on the in-repo `#print axioms` and the Aristotle summaries.* The doc's citation path omits one `project_aristotle/` level. | CLEARED |
| **1-E2** pre-review directives left in a declared doc | NO. No "what V4 must clear" checklist; the trailing "READY FOR JUDGING" is a handoff line, not a stale directive. | CLEARED |
| **1-E3** dependency ledger omitted Link-4b citations | NO. The CITED ledger now carries Simon Thm 3.3 **and** Thm 4.2, Grothendieck Résumé Thm 8, MMS Thm 4.10 — exactly the omissions Kimi named — and the MACHINE-CERTIFIED list includes the E1 receipt. | CLEARED |
| **1-E4** winding ball not reconstructible from the receipt | NO — **better at q=7.** The reviewer re-derived the full ball [0.99999…998426476 ± 5.17e-114] by re-running the assembler over the 192 raw records, and independently got winding 1.0000000000000004 by an unrelated atan2 sum. Replayable. | CLEARED |
| **1-E5** R1 Steps 3–4 cited wholesale while stale | NO. Link 2 states "R1 Steps 1–2 ONLY; R1 Steps 3–4 are SUPERSEDED at q=5 and are not used at q=7 either". | CLEARED |
| **1-E6** KS gate was a point margin, not a box margin | NO — **fixed at the outset**, and the doc says so by name ("Kimi erratum 1-E6 applied at the outset"). Reviewer confirmed the receipt computes `dx = re_lo − x`, `dy` clamped to 0 inside the Im-range, i.e. a genuine closed-box distance; the centre distance is reported separately for comparison only. | CLEARED |
| **1-E7** MMS eq-(34) heading caveat dropped | **Legitimately dissolved at q=7** (the heading's condition q = 2h+3 > 5 holds at 7, unlike at 5) **but not re-verified** — see D5. | PARTIAL |
| 1-E8 post-review edits inside the declared commit | N/A (nothing declared yet). | N/A |
| **1-E9** uncertified `W_B^ε` in a displayed bound | NO. Link 4b states W_B^ε "is used only for FINITENESS (Kimi 1-E9 presentational fix), so no numerical weight bound is owed". | CLEARED |
| **1-C1** depth-8 budget reported as achievement | NO. Doc says "adaptive splits 0"; reviewer confirmed all 192 `subdivision_depth` == 0 and that 8 is `max_subdivision_depth` (budget). | CLEARED |
| **1-C2** E1 labels double-encoded mojibake | NO. Labels parse cleanly as `1→4, +2, head` etc. | CLEARED |
| **1-C3/1-C4/1-C5** latent code paths | Carried forward and disclosed by name in Link 1 and in "What remains open" item 6; 1-C5 is actively mitigated (the assembly re-derives the global margin from the 192 raw records rather than trusting the two hard-coded `True` literals — reviewer independently confirmed the re-derivation reproduces the same minimum). Correct handling of an inherited latent defect. | DISCLOSED |
| **1-C6** two contraction constants floating around | NO — both now in the constants table with a do-not-conflate warning. | CLEARED |
| **1-C8** novelty claim rests on a prior-art sweep not redone | **YES, recurs — see D4.** | RECURS |

**Nine of twelve applicable q=5 classes are cleared, one legitimately
dissolved-but-unverified, one recurs, three are honestly disclosed as
inherited.** The port carried the q=5 lessons forward rather than repeating
them — which is itself the strongest signal in this review.

---

## DEFECT LIST

### D1 — DEFECT (severity: REPAIR). The det(1−K_s) UPPER bound is FALSE.

**Claim.** `THEOREM_G7_OFFLINE_ASSEMBLY.md` asserts, in five places, that
`0.936818983390 ≤ |det(1 − K_s)| ≤ 1.000000000001` on the closed Box, with
"both bounds certified in 384-bit ball arithmetic":

- line 131–132 — "in fact 0.936818983390 ≤ |det(1−K_s)| ≤ 1.000000000001 for every s in the closed Box (certified two-sided)";
- lines 320–324 — the **LEMMA statement** itself, plus "both bounds certified in 384-bit ball arithmetic";
- line 337 — "the same tail bound gives |det| ≤ 1 + 1e-60, printed as 1.000000000001 (rounded UP)";
- lines 344–345 — "here the divisor is bounded away from 0 *and* from ∞ on the closed box, two-sidedly";
- line 349–350 — "the divisor correction on this box multiplies |Z_S| by a factor in [0.9368, 1.0000000001]";
- line 424 — constants table, "|det(1−K_s)| on Box ∈ [0.936818983390, 1.000000000001]".

**Refutation.** Direct evaluation of `Π_{n<60}(1 − b_7^{s+n})` on a 26×26 grid
over the closed box (mpmath, dps = 50) gives

```
min |det(1-K_s)| on box grid = 1.02958306826979
max |det(1-K_s)| on box grid = 1.0295840703552
detK(centre)                 = 1.02802418597478 + 0.0566444988086304i,  |·| = 1.02958356931062
```

The true modulus is **≈ 1.0295836, which exceeds the claimed upper bound
1.000000000001 by about 3%.** The claim is refuted, not merely loose.

**Root cause.** The generator computes the "upper bound" as
`f7links_ks_gate.py:209`:

```python
# a matching upper bound, for context only (not load-bearing)
upper = arb(1) + tail_sum
```

`1 + Σ_{n≥24} t_n` is not an upper bound on `|Π_{n≥0}(1 − z_n)|`. The elementary
correct bound is `Π_{n≥0}(1 + t_n)`, which the reviewer computes as
**1.06320469300741**. The error is that `|1 − z| ≤ 1 + |z|` was replaced by
`|1 − z| ≤ 1 + (tail)`, dropping the n = 0 term's contribution entirely;
`b_7^{s*}` is not near the positive reals (arg = −2.0304 rad, modulus
0.06300460), so each factor can and does have modulus above 1.

**Why it does not reach theorem level.** The identification step consumes only
non-vanishing, i.e. the LOWER bound — which reproduces exactly
(0.9368189833904026963, 40-digit agreement with the receipt ball). Finiteness
of the product is immediate from `Σ t_n < ∞`, needing no numeric bound. The
theorem's conclusion, gap, and box are untouched.

**Why the author likely missed it.** The generator's own comment labels the
field "for context only (not load-bearing)", so it received no scrutiny inside
the script; the assembly document then lifted the receipt field
`abs_detK_upper_bound_rounded_up: "1.000000000001"` into a LEMMA statement and
attached the word "certified" to it. This is precisely the failure mode the
document elsewhere guards against (1-C5, "re-derive from raw fields") — applied
to Link 1 but not to its own new Link 5.

**Required repair.**
1. Replace the upper bound with `Π_{n≥0}(1 + t_n) ≤ 1.0632047` (certifiable by
   the same tail machinery), or state the true certified range ≈ [1.029583,
   1.029585]; remove "certified two-sided" and "bounded away from … ∞ …
   two-sidedly" as currently phrased.
2. Fix the proof sentence at line 337: the tail bound does **not** give
   `|det| ≤ 1 + 1e-60`.
3. Line 349–350: the bracket `[0.9368, 1.0000000001]` is refuted. The
   quantitative consequence "moves MAGNITUDES by at most ~6.4%" survives if
   derived from the correct lower bound (1 − 0.9368 = 6.32%); the true
   magnitude effect is **≈ 2.9%** (division by 1.02958). The load-bearing
   clause — "moves NO zero, because it neither vanishes nor blows up there" —
   is unaffected and correct.
4. Fix `f7links_ks_gate.py:209` and re-emit the receipt, or delete the field.

### D2 — DEFECT (severity: REPAIR, editorial). Link renumbering collision.

The numbered chain assigns **Link 4 = "TRUE-DETERMINANT ZERO IN BOX [ARGUMENT
PRINCIPLE]"** (line 113) and **Link 5 = the K_s divisor gate** (line 130), and
the link table agrees (row 4 = argument principle, row 5 = det(1−K_7) ≠ 0). But:

- the detail section at **line 174 is headed "## Link 4 in detail — the K_s divisor gate at q=7"** — filing Link 5's content under Link 4;
- **line 135**, inside Link 5, says "See §'Link 5 in detail'" for the K_s constants — which actually live in §"Link 4 in detail";
- **line 423** (constants table) says "see Link 4" for the K_s box margin;
- **line 204** says "Kimi erratum 1-E6 applied" inside the mis-numbered section;
- the generator docstring (`f7links_ks_gate.py:1-2`) uses the older numbering, "assembly link 4" for the K_s gate and "link 5/R5 closure" for the identification.

Two different numbering schemes are live in one document; every cross-reference
to the K_s constants points at the wrong section. A referee hits this on the
first read of Link 5. Likely cause: the chain was renumbered when Link 4b was
inserted, and the detail headings plus the generator docstring were not
re-swept.

### D3 — DEFECT (severity: COSMETIC). Mis-attributed erratum.

Lines 49–52 state: "`F7_CERT_PLAN.md` §1 **and `F7_CONSTANTS_MANIFEST.md` §5**
print 'Re(s*) ≤ 0.4751648'." The manifest does not. A grep of
`F7_CONSTANTS_MANIFEST.md` for `47516` returns lines 191, 202, 207, 269 —
none of which prints 0.4751648; **§5 line 207 is correct**, writing
`δ = 1/2 − 0.4751647621098225 − 1e−6 = 0.0248342` with the half-width included.
The erratum exists only at `F7_CERT_PLAN.md:8`. The document accuses a clean
file of an error. (Its companion erratum against the manifest — the 0.5895480
round-up at manifest lines 210 and 270 — is genuine and verified.)

### D4 — DEFECT (severity: COSMETIC, disclosure). Priority claim not repo-verifiable, and not listed as open.

Lines 44–47 claim this is "the second member of the non-arithmetic Hecke family
to carry a rigorously localized off-line resonance, and **the first at
h_q = 2**", with "(Bruggeman–Pohl leave the non-arithmetic Hecke resonances
conjectural; prior-art sweep lane_c)". This is a literature claim resting on a
lane_c sweep that was not redone in this session and not redone by this
reviewer. It is the exact class of Kimi 1-C8 at q=5, **carried over without
being logged**: the eight-item "What remains open" list does not mention it.
Add it as item 9, or downgrade the sentence to a citation of the lane_c sweep.

### D5 — DEFECT (severity: COSMETIC, disclosure). The MMS eq-(34) heading text is not verifiable in-repo.

Lines 145–147 and 454–455 rest a positive claim on primary-source wording: "the
heading above MMS eq. (34) prints 'q = 2h_q + 3 > 5', which applies to q = 7
verbatim… the q=5 erratum footnote is not needed." The reviewer searched the
tree for any MMS text (`*mayer*`, `*momeni*`, `*MMS*pdf`) and found **no
e-print or PDF anywhere** — only derived notes and probes. The arithmetic is
sound (2·2 + 3 = 7 > 5, and 7 ≥ 5 for Lemma 4.2), and Kimi K3's q=5 audit
attests the heading text against the primary PDF, so residual risk is low. But
the doc's own item 8 flags only the journal **numbering** of Theorem 6.4, not
the heading **text** that Link 6's "verbatim" boast depends on. Add the heading
text to the `TODO-VERIFY` alongside the numbering, or paste the heading into
the constants manifest as a quoted source line.

---

## OBSERVATIONS — anomalies examined and explained (not defects)

- **O1. The 16 per-chunk minima cluster into 4 near-identical groups by chunk
  index mod 4** (≈2.81662e-6 / 2.43478e-6 / 2.41285e-6 / 2.72361e-6, agreeing
  across groups to ~8 significant digits) even though the groups sit on
  different edges of the box. This looks like a copy-paste artifact and is not.
  WHY: each 48-arc edge is split into exactly 4 chunks of 12, so chunk index
  mod 4 IS position-within-edge; over a box of diameter 2e-6 the determinant is
  near-constant and the four edges are near-symmetric. The reviewer verified
  each chunk's own `chunk_arc_range` and the 48-per-edge `edge_name` census
  independently, and the 192 `s_start`/`s_end` balls form one closed cycle — so
  the four groups are genuinely distinct arcs, not duplicated records.
- **O2. E1's disc radii are not the R2 receipt's radius balls.** E1 block 1's
  `original_radius_upper_bound` = 0.174393823623839918698224185000000418… while
  the R2 receipt's certified radius = [0.174393823623839918698223815347389… ±
  2.19e-115]. They diverge at ~3.7e-21 and the balls do not overlap. The field
  name says "upper bound" and the direction is conservative for the source
  enlargement; the induced perturbation of the ρ̂ ratio is ~1e-20 against
  0.0848 of headroom to 1, so the gate cannot flip. Not a defect — but a
  referee could read it as a geometry mismatch between Link 1's operator and
  Link 4b's certificate. One clarifying line in the paper is cheap insurance.
- **O3. Link 3's endpoint constant has two provenances** (the chunk receipts'
  `endpoint_trace_bounds/256`, 20.169636923385206113784789246469…, and
  `F7_R3B_ENDPOINT_V2_RECEIPT.json` `/bounds/256`,
  20.169636923385172661643267982167…), differing at the 21st digit. Both are
  below the printed 20.1696370, so the bound covers both. The doc cites both
  files for "the" constant without noting they are two runs; harmless, worth a
  clause.
- **O4. Every chunk receipt carries `all_theorem_gates_pass: false`.** Correct
  and expected — a 12-arc chunk is not a closed cycle
  (`finite_argument_winding_info: "chunked run: not a closed cycle, winding
  deferred to merge"`); the winding gate is supplied only at assembly. No
  overclaim anywhere.
- **O5. The mms− sector claim** ("12 pins all within 5e-10 of Re(s) = 1/2",
  line 363) traces only to `F7_CONSTANTS_MANIFEST.md:219-224`, not to a JSON
  receipt. It is a scoping remark in the honesty section and nothing depends on
  it; noting it so a future round does not mistake it for certified.

---

## OVERALL RULING

**SOUND-WITH-REPAIRS.**

**No theorem-level defect.** The theorem as stated —
`Z_S` has a zero `s*` with `|Re(s*) − 0.4751647621098225| ≤ 10⁻⁶` and
`|Im(s*) − 4.668743786424289| ≤ 10⁻⁶`, hence `Re(s*) ≤ 0.4751658 < 1/2` and
`δ ≥ 0.0248342` — is supported by an evidence chain that the reviewer
reproduced independently end to end: every lattice constant to 40 digits from
`2cos(π/7)` upward, the box-to-lattice distance to a 40-digit exact match, the
det(1−K) lower bound exactly, both link generators byte-identically, the
assembly's winding and margins, all 16 chunk receipts individually, all 192
per-arc gates, all 192 seams including the wrap, an independent winding
computation by an unrelated method, the engine hash by `shasum`, all four Lean
joints `sorry`-free, and all 19 E1 blocks with their three extremal claims. The
document's two self-declared errata (the plan's `Re(s*)` and the manifest's K_s
margin) are both genuine, and both corrections round in the honest direction.

**Repairs required before any DECLARED label or circulation:**

1. **D1 (mandatory, mathematical).** The printed upper bound
   `|det(1−K_s)| ≤ 1.000000000001` is FALSE — the true value on the box is
   ≈1.0295836. Fix the lemma statement, the proof sentence, the
   `[0.9368, 1.0000000001]` bracket, the constants table, and
   `f7links_ks_gate.py:209`. Non-load-bearing, but it is a false statement
   inside a lemma.
2. **D2 (mandatory, editorial).** Resolve the Link 4 / Link 5 numbering
   collision across the two detail headings, lines 135 and 423, and the
   generator docstring.
3. **D3 (editorial).** Withdraw the `F7_CONSTANTS_MANIFEST.md` §5 half of the
   `Re(s*) ≤ 0.4751648` erratum; only `F7_CERT_PLAN.md:8` carries it.
4. **D4 (disclosure).** Log the h_q = 2 priority claim as an open literature
   item (q=5 class 1-C8, recurring).
5. **D5 (disclosure).** Add the MMS eq-(34) heading TEXT to the `TODO-VERIFY`
   beside the journal numbering.

**On link-table row 8.** This pass discharges "no adversarial round has been run
against this q=7 assembly" — one hostile round is now on the record. It does not
by itself substitute for q=5's five rounds plus an independent hostile audit:
this reviewer read code and receipts and re-derived numbers, but did not open
Simon, Grothendieck, or MMS, did not run a Lean build, and did not re-execute
the 107.8-hour contour certification or the E1 enlarged-contour run from
scratch. Those are the residual soft spots, and they are the same ones the q=5
chain carries.

Reviewer probe scripts: `crg7_recompute.py`, `crg7_detK.py` (session scratchpad).
No repo file other than this review was written; no `git` command was run.

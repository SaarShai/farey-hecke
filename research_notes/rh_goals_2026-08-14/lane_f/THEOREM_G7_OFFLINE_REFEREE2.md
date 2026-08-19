# THEOREM G7 OFFLINE REFEREE 2 — COLD LANE REPORT

Date: 2026-08-19  
Worktree: `/Users/za/Documents/farey-hecke/.worktrees/law-g7-referee2-20260819`

## Summary (<=200 words)

The q=7 finite contour certificate replays: 384-bit Arb/Acb, 16 chunks,
192 seams/arcs, winding `1`, positive `finite lower − F` margin, and the
`N=224` comparison arm fails as designed. The q=7 enlarged-disc and `K_s`
box rechecks also pass their stated numerical gates. The first load-bearing
theorem gap is Link 4b: `TB_R5_DETERMINANT_IDENTIFICATION.md` v3.1 Clause 1
binds a q=5, `h=1`, `κ=3`, 11-block wrapper with q=5 radii. The q=7 files
provide a 19-block numerical port (`h=2`, `κ=5`) but only call the remaining
paper proof “q-independent”; they do not prove that this q=7 engine is the
same MMS operator with the same branches, weights, and source geometry.
Therefore the implication from the certified q=7 Hilbert Fredholm zero to
the MMS Banach determinant, and hence to `Z_S`, is unclosed. MMS source text
and a q=7 Lean `K_s` specialization are secondary open items.

Principal verdict: **GAPS / NOT REFUTED**.

## changed_paths (exhaustive)

- `research_notes/rh_goals_2026-08-14/lane_f/THEOREM_G7_OFFLINE_REFEREE2.md` — this report only.
- No other file was written, staged, committed, reverted, or otherwise modified. The pre-existing untracked `G7_REFEREE2_BRIEF.md` was left untouched.

## Phase 0: binding, plan, and disagreements

I read `G7_REFEREE2_BRIEF.md` completely before editing. Its nine mandatory
attacks and hard report shape were binding. I verified the named q=7 paths,
the 384-bit `python-flint` backend, the q=7 receipt schemas, R5 v3.1, the
MMS-derived local note, and the Aristotle files before forming the verdict.

The brief describes `f7links_e1_recheck.py` and `f7links_ks_gate.py` as
receipt-writing scripts, while the active scope rule permits writing only
this report. I therefore copied each script and its input receipt to a
temporary directory and ran the copy; the assembler was run without
`--write` and with `PYTHONDONTWRITEBYTECODE=1`. This is the only execution
deviation from the brief, and it avoided any out-of-scope write.

## Evidence

### 1. Receipt identity, contour, seams, and winding

Command (no-write replay):

```text
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python \
  research_notes/rh_goals_2026-08-14/lane_f/kaggle_f7/assemble_f7.py
```

Decisive output:

```text
"verdict": "THEOREM-GRADE closed-contour YES at N=256"
"coverage": true, "hash_pinning": true, "seam_closure": true,
"margins": true, "arc_exclusions": true, "winding": true,
"comparison_control_arm": true
"winding": 1
"winding_ball": "[0.999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999998426476 +/- 5.17e-114]"
"min_margin_down": "0.00000241285276269068356797445"
"max_rH_up": "0.211064737207127407537372"
"accepted_subarcs": 192
"seam_failures": []
```

The banked receipt records `q=7`, `sign=1`, `N_primary=256`,
`N_comparison=224`, `precision_bits=384`, `k_per_edge=48`,
`base_closed_arc_count=192`, and `chunk_count=16`. The 16 chunk ranges are
`[0,12),[12,24),...,[180,192)`; each has 12 records, and their union is
exactly `[0,192)`. The raw receipt gate is local-chunk `all_theorem_gates_pass
= false` only because a chunk is not a closed cycle; the merged receipt is
the closed-cycle gate quoted above. Hash pinning reports all immutable
bindings verified, R2/TB orchestrator agreement true, and all 16 chunks
agreeing on their receipt hashes. The certified engine bytes are recoverable
at the documented `out/kaggle_top4/.../zeta_cert_rosen.py` path, but the live
primary engine path has a different hash; this provenance drift is disclosed,
not silently treated as a fresh rerun.

The N=224 arm is explicitly `NOT_CERTIFIED`/closed-contour false, while N=256
passes. Thus the two truncation settings are not being conflated, and the
reported 384-bit precision is pinned rather than inferred from a dashboard.

### 2. Finite section to Fredholm tail

`F7_R3B_ASSEMBLY_CERT.md` §6–§7 and
`f7_certify_r3b_flagship.py:535-583` use the same finite matrix convention
throughout: the winding object is `det(I - L P_N)`, and the F-inflated
homotopy is the bridge to `det(I - L_s)`. The q=7 N=256 endpoint fields are:

```text
matrix dimension 1280
same endpoint trace-norm bound <= 20.169636923385206113784789246469...
T_tail(256) <= 2.411487076500882178674099513617...e-27
F_R = T_tail*exp(1+2*B_same) <= 2.166224464894217177683587269404...e-9
min(finite lower - F) >= 2.41285276269068356797445e-6
ratio min-margin/F_R ~= 1113.8517
```

The code records the same bound for `||L||_1` and `||LP_N||_1`, and the
certificate states that all 192 F-inflated tubes exclude zero. The finite
Taylor/derivative enclosure, truncation tail, and straight-line homotopy are
therefore a supported q=7 *Hilbert Fredholm* zero route. This link does not
repair the later Hilbert-to-MMS identification gap.

### 3. q=7 enlarged-disc E1 recheck

The deterministic recheck was run from a temporary copy of the script and
input receipt. Decisive output:

```text
"precision_bits": 384, "blocks_seen": 19, "expected_blocks": 19
"all_blocks_pass_all_checks": true, "all_gates_pass": true
"rho_hat_rederived_upper_rounded_up": "0.9152411837446922"
"rho_hat_worst_block": "5→3, +1, head"
"eta_max_rederived_upper_rounded_up": "0.8695652173913044"
"rho_hat_below_q5_chain_value": true
"verdict": "PASS_E1_REDERIVED_FROM_RAW_FIELDS"
```

The raw q=7 receipt gives the minimum remaining pole/branch-cut clearance
`[0.9915072451437825333425457873... +/- 3.19e-101]` at `3→1,+1,head`,
strictly positive. It records the rule `e_B=min(clearance_B/4,0.15*R_i)`.
This is a genuine q=7 geometry/contraction recheck, but it rechecks raw
fields from the same certification method; it does not prove the q=7
operator's MMS identity.

### 4. First load-bearing gap: Hilbert-to-Banach/MMS identification

The q=7 numerical geometry is real. Command:

```text
jq '{q,kappa,h_q,radius_multipliers_exact_strings,
     blocks_source:(.blocks_source|{count,expected_count,exact_count_check}),
     certification_verdict}' \
  research_notes/rh_goals_2026-08-14/lane_f/f7_receipts/F7_TB_BLOCK_CERTIFICATES_RECEIPT.json
```

Decisive output:

```text
q: 7, kappa: 5, h_q: 2
radius_multipliers_exact_strings: ["3.522","2.622","2.372","1.79","1.6"]
blocks_source: {count:19, expected_count:19, exact_count_check:true}
certification_verdict: "PASS_RHO_LT_0.80"
```

`f7_source_builder.py:75-99` explicitly assembles the q=7 19 calls, with
positive/negative branches, q=7 centers/radii, and `sign=+1`. However,
`TB_R5_DETERMINANT_IDENTIFICATION.md` v3.1, lines 14-29, binds Clause 1
explicitly to “the reduced q=5 ... system”, `h_q=1`, `κ_q=3`, exact factors
`3.14, 2.27, 1.70`, and eleven q=5 blocks. Its lines 51-65 then define the
two realizations and the determinant equality for that Clause-1 object.
Its lines 178-185 identify that already-reduced three-component q=5 system
with MMS eq. (34). The later smoothing, Jordan-chain, spectral-product, and
identity-theorem clauses quantify over that bound object; they do not supply
a q-generic operator-binding lemma.

Thus the first missing implication is exactly

```text
det_H(1 - L_{s,+}^{q=7,engine}) =
det_B(1 - L_{s,+}^{q=7,MMS})  on Ω*
```

The current q=7 bytes establish the left-hand finite/Hilbert object and its
q=7 contraction data, but merely label the proof “q-independent”. They do
not discharge, for q=7, the branch formulas, five-disc source geometry,
19-block correspondence, weights, and exact MMS sector/sign identification
needed to make the two operators the same. E1 cannot supply this abstract
identity. Consequently the q=7 Fredholm zero is not yet a theorem-level zero
of the MMS determinant or of `Z_S`.

### 5. `K_s` divisor and lattice

The deterministic KS replay (temporary copy) returned:

```text
"all_gates_pass": true
"box_to_lattice_distance_ball":
  "[0.5895479897495818278130858801517574259447 +/- 3.93e-41]"
"box_to_lattice_distance_lower_bound_rounded_down": "0.5895479"
"nearest_lattice_point": {"n":0,"k":4,"Re":"0",
  "Im":"[4.31976394552499744038438731279 +/- 3.81e-30]"}
"abs_detK_lower_bound_ball":
  "[0.9368189833904026963033671209126567399736 +/- 2.62e-41]"
"abs_detK_upper_bound_rounded_up": "1.063204693008"
"strictly_positive_on_closed_box": true
"verdict": "PASS_KS_BOX_CLEAR_AND_DETK_NONVANISHING"
```

The exact lattice has `Re=-n<=0`, so the certified box lies in the positive
half-plane and misses it by the outward lower bound above. The generic
Aristotle theorem `KsZeroLattice.lean:15-42` proves that a zero of one factor
with `0<ell<1` has `Re(s)=-n`; it is not q=7-specific and no q=7 Lean
specialization/rebuild receipt was found. The ball certificate is sufficient
for the numerical nonvanishing step, but this is a formal-coverage leftover,
not a repair of Link 4b.

### 6. MMS/Selberg convention and factorization

The local derived source note `LAW_Q3_BRANCH_DIAGNOSIS.md:83-94` transcribes
the intended convention

```text
Z_S(s) = det(1-L_s)/det(1-K_s)
       = det[(1-L_{s,+})(1-L_{s,-})]/det(1-K_s).
```

The q=7 source builder uses `sign=+1` and the 19-block q=7 reduced system,
and the assembly keeps the minus factor and divisor separate. This is
consistent at the code/notation level. But the MMS e-print/PDF is absent from
the repository. The assembly itself marks the eq. (34) heading text and
journal theorem numbering `TODO-VERIFY`; the local note records a retrieved
e-print but does not bank its source bytes. Therefore the published
factorization, exact heading condition, and cited numbering remain a
secondary GAP, not a fact that can be promoted from citation labels.

### 7. Off-critical gap and resonance scope

From the certified closed box in `THEOREM_G7_OFFLINE_ASSEMBLY.md:31-35`,

```text
Re(s*) <= 0.4751647621098225 + 1e-6 = 0.4751657621098225
delta >= 0.5 - 0.4751657621098225 = 0.0248342378901775
```

Hence the safe printed bounds `Re(s*)<=0.4751658` and `δ>=0.0248342` are
strictly below the critical line; the box has nonzero imaginary part near
`4.6687437864`, excluding the cited real/trivial alternatives. The standard
resonance interpretation is conditional on the MMS factorization and the
unclosed Link 4b bridge. No stronger claim about parity, completeness, or the
full resonance list follows.

### 8. Independence from RATE/`phi_q`/full LAW

The route is a finite q=7 determinant computation: fixed `q=7`, 19 blocks,
`N=256`, and banked tail bounds. The assembly explicitly scopes the certified
object to the `+` sector and says no claim is made about RATE, a true-scalar
`phi_q` block, q=8, or the unconditional full LAW. I found no hidden use of
those conjectural layers in the q=7 receipt chain. This attack passes as a
scope check only; it does not cure the Link 4b implication.

### 9. V1 objections and current-byte audit

I reconstructed the chain before reading `ADVERSARIAL_REVIEW_G7_V1.md`, as
required. The current assembly bytes contain the V1 repairs/disclosures:

- D1: the false `K_s` upper bound is corrected to the elementary
  `1.063204693008` context bound; only the lower bound is load-bearing.
- D2: the divisor section is now headed Link 5, resolving the Link 4/5
  collision.
- D3: the plan/manifest erratum distinction is stated.
- D4 and D5: the h=2 priority claim and MMS heading/source items remain
  explicitly open.
- The assembly discloses engine-path drift, the non-independent q=7 E1
  recheck, latent runner assertions, one hostile round, and the q=7 Lean
  lattice gap.

These repairs are current-byte facts. V1's “SOUND-WITH-REPAIRS” is not copied
as a theorem verdict: its acceptance of the phrase “q-independent” does not
answer the present Clause-1 q=5/q=7 binding check. A further provenance
concern is that `F7_CONSTANTS_MANIFEST.md` retains older geometry-factor text
while the q=7 receipts bind the adopted five exact strings; the receipts/code
are internally consistent, but the manifest should be reconciled before
circulation.

## Attempts, assumptions, and leftovers

### Attempts performed

- Replayed the q=7 assembler without writing; verified the merged winding,
  all gates, 192 accepted arcs, 192 seams, N=256 margin, and N=224 failure.
- Re-ran E1 and KS deterministic rechecks from temporary copies at 384-bit
  Arb/Acb; neither touched the worktree.
- Read all q=7 R3B assembly/certification Markdown and JSON named by the
  theorem, q=7 source builder/engine/endpoint files, the complete R5 v3.1
  note and its cited V-series correction material, the MMS-derived local
  note, the V1 review, and the v17/v18 Aristotle artifacts.

### Attempts not performed (and why)

- No fresh multi-hour q=7 contour or stage-4b certification: the banked
  receipts and no-write assembler replay were sufficient for this cold gate;
  the brief's hard write boundary forbids regenerating receipts in place.
- No Lean build: it would create build artifacts outside the owned report;
  the repository summaries were treated as claims, not as a fresh build
  receipt.
- No external MMS/Selberg source fetch: the task requires repository-grounded
  evidence and the missing source is recorded as a GAP rather than silently
  strengthened.

### Assumptions

- Banked q=7 receipt JSON and their pinned hashes are the supplied immutable
  evidence; the live-engine hash drift is treated exactly as disclosed.
- The q=7 finite/Hilbert route is accepted only to the scope stated by its
  certificate. No q-independent theorem is inferred from q=5 prose alone.
- Outward endpoint directions are used: upper bounds are rounded up and
  margins/lower bounds down.

### Leftovers / concerns

1. Supply a q-generic or explicit q=7 Clause-1 operator-binding/common-
   continuation proof, including the 19 exact blocks, five discs, branches,
   weights, source geometry, and MMS `+` sector correspondence. This is the
   first required repair before a paper-level q=7 `Z_S` claim.
2. Bank and verify the MMS primary source text and theorem numbering.
3. Add/rebuild a q=7 Lean lattice specialization if formal coverage is
   required; the existing generic theorem and ball certificate do not equal
   that artifact.
4. Reconcile stale manifest geometry prose with the receipt-bound exact
   q=7 factors, restore pinned engine bytes before any rerun, and obtain more
   independent q=7 review depth if circulation requires it.

STATUS: COMPLETE_WITH_CONCERNS (Link 4b q7 operator-binding gap; MMS source text unbanked; q7 Lean K_s specialization absent; engine-path drift; one hostile round)
READY FOR JUDGING

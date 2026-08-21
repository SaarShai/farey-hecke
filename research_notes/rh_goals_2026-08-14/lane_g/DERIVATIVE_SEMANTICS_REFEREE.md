# Referee report — DERIVATIVE_SEMANTICS_SOL.md (commit 6b839d4)

Date: 2026-08-20. Cold referee, independent context. Interpreter `/Users/za/.venvs/farey-rh/bin/python` (python-flint/Arb, prec 384). Nothing edited, nothing committed. Probes in session scratchpad (`ref_common.py`, `p1.py`–`p4.py`).

## Verdict table

| # | Claim | My independent evidence | Verdict |
|---|---|---|---|
| a1 | Anchored factorization `A(s)^-1 = (I-A0^-1 dC)^-1 A0^-1`; lines 973-979 assemble the true arc log-derivative | Re-derived from `q8_schur_contour.py:885-1005`. `A=I-C=A0-dC=A0(I-A0^-1 dC)` ⇒ identity exact. `delta[i,j]=disc(r·sup|C'_arc[i,j]|)` ⊇ `dC(s)_ij` (segment integral, disc is 0-centred); `A0_inverse*delta` ⊇ `A0^-1 dC`; `corr.inv()` is Arb verified-LU (fails loudly — I reproduced `ZeroDivisionError: matrix is singular` on the arc box). Composition order `corr^-1 (A0^-1 (-e C'))` = (6) | **PASS** |
| a2 | s-direction conventions correct on every edge (the 90° suspicion) | All four edges checked, not sampled: `closed_boundary_segments` gives edge0 bottom L→R, edge1 right up, edge2 top R→L, edge3 left down; `segment_direction=(1, i, -1, -i)` matches `(end-start)/|end-start|` on each. Verified leaf a2/[1,0,0,0,0,0,0] has `edge=2`, `end-start` negative real. `H=|tr|` is a modulus ⇒ `|e|=1` cannot change it | **PASS** |
| a3 | Gronwall remainder `rH·|det_mid|/(1-rH)` at :984 | Line 984 is literally `radius*H*|midpoint_det|/(1-rH)`. Derivation valid on the real interval `u∈[-r,r]` (note's "disc `|u|≤r`" phrasing is loose — `cprime_arc` is enclosed on `segment_box`, which for an axis-aligned edge is the segment only, not a disc; the interval version is the one used and it is sound) | **PASS (with flagged looseness)** |
| a4 | "true threshold `rH < 1/2`" (eqn 4, and §5A "the *real* pass threshold") | **REFUTED.** `inflate()` builds a **square** box (`acb(re±t, im±t)`), not a disc. Zero-exclusion ⟺ `t < max(\|Re det\|,\|Im det\|)` ⟹ guaranteed only for `rH < 1/(1+√2)=0.41421`. Receipt `SHARD_a2_l64-128`: max PASS `rH=0.4262`; **six OPEN leaves with `rH` = 0.4375, 0.4491, 0.4609, 0.4731, 0.4855, 0.4982 — all `< 1/2`, all `excludes_zero=False`**. My square-box predictor matched the receipt on all 10 straddling leaves (10/10). This regresses against `ZERO_EXCLUSION_DIAGNOSIS_SOL.md:56` (`rH < mu/(1+mu)`, `[0.4142,0.5]`), which was right | **FAIL** |
| b | No 128×/90° conflict; trace = FD of `det(I-C(s))` | Reproduced at a **different N and a different leaf** (N=64, arc 3, path 0101010, vertical edge): `-tr(A0^-1 C'_mid) = -898592.095272 - 301870.504940 i`; FD of `det(I-C(s))`, `h=1e-11` → rel diff **1.947e-22**, `h=1e-12` → **1.947e-24`. Magnitude 9.5e5, not 1.28e8 | **PASS** |
| b2 | The old probe's `1.28000000605e8` = `1/radius` | `1/7.8125e-9 = 128000000.0` exactly; probe value agrees to 8 s.f. (rel 4.7e-8), whereas certified `H=1.27546e8` differs by 0.35% — so the match is with `1/r`, not with `H`. But `trace_test.py` **does not exist in the repo** (`find` returns nothing), the residual `+6.05` and `+10.14i` are unexplained, and the note calls the match "exactly" | **PLAUSIBLE-UNPROVEN** (immaterial: b is confirmed directly) |
| c | 127.55× all in `correction_inverse`; arc-box C' = 1.0000381×; N=48 reproduces N=262 `H` to 6 s.f. | Reproduced step-by-step (p3.py, N=48, leaf a2/1000000): A `\|tr(A0^-1 C'_mid)\|=9.9996977e5`; B arc-box `=1.0000078e6`, ratio **1.0000381**; C production `H=1.2754593e8`, ratio **127.5498**; `qOp=0.6544379`. Receipt N=262: `H=1.27546049e8`, `qOp=0.6544379`, `rH=0.996454` vs my N=48 `rH=0.996453` | **PASS (exact)** |
| d1 | "worst failing leaf depth 7 `rH = 0.9965`" | **REFUTED.** Record 0 is the *lowest*-`rH` failing leaf. Shard max is `rH = 1.0290323` at path `[1,0,0,0,1,1,1]` (record 7); records 1–11 all exceed 1.0. The note audited record 0 = the first record, not the worst — a sample-of-one error | **FAIL** |
| d2 | depth 8 → `rH ≈ 0.189`, `EXCLUDES_ZERO=True` | Reproduced (N=48): rec0 children `rH = 0.189213 / 0.189761`, `excl0=True`. **Extended to the true worst leaf myself**: rec7 d7 `rH=1.029031` (receipt 1.029032 ✓), children `rH = 0.194449 / 0.194463`, `excl0=True`. (`status=FAIL_GATE` at N=48 only via `full_output_projection_tail_available`, an N=48 tail-receipt artifact, unrelated to the Taylor gate) | **PASS, and strengthened** |
| d3 | super-quadratic scaling | 7 measurements, 4 distinct leaves, both edge orientations: 5.266, 5.251 (rec0); 5.292, 5.292 (rec7); 4.910, 4.917 (a3/0101010, vertical edge, `rH` 0.695079→0.141550/0.142237); 4.595 (a0/0000000, 0.355662→0.077405; receipt min-`rH` is 0.35566 ✓). All > 4 | **PASS** |
| d4 | "2.6× margin below threshold" | Against the *correct* threshold 0.41421 the margin is **2.13×** (0.4142/0.19446 for the true worst leaf), not 2.6× | **FAIL (arithmetic follows a4)** |
| d5 | "~50 h"; "`certify_adaptive` only splits failing leaves, so this is a `max_depth` bump, not a re-shard" | **Mechanism REFUTED, number defensible.** Production is `q8_leaf_shard.py`, which is **uniform-depth by construction** ("Uniform depth, not adaptive", :30-37) and passes `args.depth` into `checkpoint_parameters` (:279) ⇒ a depth-8 run has different `params` ⇒ **no depth-7 checkpoint can be resumed and no depth-7 PASS leaf is reusable**. Correct count: 2^8 × 4 arcs = **1024 leaves**, not "2 extra evaluations per open leaf". Cost: measured `leaf_seconds_mean` 1882 s (a2) / 1989 s (a0) ⇒ **535 CPU-hours**; 44.6–49.4 **wall**-hours at the observed 12 workers. So ~50 h happens to be right *as the full uniform depth-8 wall time* (512→24.7 h, 1024→49.4 h, 2048→98.8 h is exactly the note's own ladder), but the stated cheap mechanism does not exist in the driver | **FAIL (reasoning) / number OK** |
| e | Direct arc-box `(I-C)^-1` fails, ~5e-6 inflation | Reproduced: `A_arc[0,0] = [0.16182 ± 4.38e-6] + [0.06020 ± 4.96e-6]i` vs midpoint `[0.16181636 ± 3.2e-9] + [0.060195774 ± 7.9e-11]i`; `.inv()` → `ZeroDivisionError: matrix is singular` | **PASS** |
| 6a | No leaf PASS claimed beyond receipts | Receipts total 36 PASS (a0 4/4, a2 8/64, a3 12/12-partial). Note claims 12 — under-counts (a3 shard mtime 20:30 predates the 21:11 commit), never over-counts | **PASS (stale count, non-fatal)** |
| 6b | depth-8 sufficiency graded as measured-on-samples | §6 hedges correctly ("measured at N=48 on one leaf, CONJECTURAL"), but the **headline (line 19) and §3.3 heading assert it flatly** ("makes depth 8 the sufficient re-shard"), and §3.3's "worst open leaf of the shard" is false (d1). Only 2 of 512 depth-7 leaves had their children measured by the author; no uniform bound on `H_true` is proved. My own probe found a further failing leaf outside the audited shard (a3 path 0101010, `rH=0.695`, `excl0=False`) — the open region is broader than the note's framing | **FAIL (headline overclaim)** |

## Item 5 — blast radius: yes, `ZERO_EXCLUSION_DIAGNOSIS_SOL.md` needs a further append-only block

Its current correction block is now wrong on two counts: (i) it still calls the 128×/90° split "the real open question ... mutually inconsistent" and leaves a which-inverse question open; (ii) it withdraws H-tightening on the ground that "H is a faithful evaluation of `|tr(A0^-1 C'_mid)|`, box overhead 0.35%" — I measured the overhead at **127.55×**, so that stated reason is false even though the withdrawal itself survives. Specified repair text:

```markdown
## Dated correction block (2026-08-20 #2, supersedes correction block #1 — append-only)

**The "128x / 90-degree" inconsistency DOES NOT EXIST.**  Independently
re-measured (referee lane, N = 64, arc 3 leaf path 0101010, and N = 48,
arc 2 leaf 64): `-tr(A0^-1 C'_mid)` equals an end-to-end central finite
difference of `det(I - C(s))` to 1.9e-22 (h = 1e-11) and 1.9e-24
(h = 1e-12) relative, with magnitude ~1.0e6 — matching the finite
differences of the certified `midpoint_det` values.  The
`1.28000000605e8` of correction block #1 came from a probe
(`trace_test.py`, not present in the repo) whose value agrees with
`1/radius = 1/7.8125e-9 = 1.28e8` to 8 significant figures.  It was not a
trace.  **The which-inverse question is CLOSED:** lines 973-979 of
`q8_schur_contour.py` carry the true arc inverse via the exact anchored
factorization `A(s)^-1 = (I - A0^-1 dC)^-1 A0^-1`; `tr(A0^-1 C')` is
never used as the gate quantity.  The directional convention is also
correct on all four edges.

**Correction to correction block #1's stated reason for withdrawing
H-tightening.**  The claim "box overhead 0.35%, not 73-133x" is FALSE.
Measured at the leaf-64 midpoint, N = 48: `|tr(A0^-1 C'_mid)| = 9.99970e5`,
arc-box `|tr(A0^-1 C'_arcbox)| = 1.000008e6` (1.0000381x), production
`H = 1.2754593e8` (**127.55x**).  100% of the slack is the
`correction_inverse` factor.  The withdrawal of §2.4/§5.4 STANDS, but for
the correct reason: the slack is a structural limit of norm-type bounds on
a near-cancelling trace, and closing it needs a rigorous nuclear-norm
bound on `A0^-1 C'` that the codebase does not have.

**§5.2's threshold `rH < mu/(1+mu)`, `mu in [1/sqrt(2), 1]`, is CONFIRMED
and takes priority** over any later "rH < 1/2" statement: `inflate()`
builds a square box, and six leaves of `SHARD_a2_l64-128` with
`rH` in (0.4375, 0.4982) — all below 1/2 — have
`finite_taylor_excludes_zero = false`.  The safe per-leaf predictor is
`rH < 1/(1+sqrt(2)) = 0.41421`.
```

## Defects (what · where · why missed)

1. **Threshold regression** · `DERIVATIVE_SEMANTICS_SOL.md` eqn (4), lines 63-65, §4/§5A "the *real* pass threshold rH<0.5" · author derived the disc criterion analytically and never cross-checked it against `inflate()` (square box) or against the six sub-0.5 OPEN leaves in the very receipt being audited.
2. **Wrong "worst leaf"** · §3 lines 116-119, §3.3 line 197 · author took record 0 of the checkpoint (leaf 64, the first record) as the worst; it is the *best* of the failing leaves. Classic sample-of-one. (Harmless in outcome — I verified the true worst also clears depth 8.)
3. **Wrong margin** · §3.3 line 198 "2.6x" · downstream of defect 1; correct value 2.13×.
4. **Cost mechanism does not match the production driver** · §4 lines 222-232 · author reasoned from `certify_adaptive` in `lane_f`, but the campaign runs `q8_leaf_shard.py`, which is uniform-depth and `params`-bound to `--depth`. Correct restart scope: 1024 fresh leaves, ~535 CPU-h, ~45-50 wall-h at 12 workers, with **all 36 banked depth-7 PASS receipts unusable for resume**.
5. **Headline overclaim** · line 19 and the §3.3 heading assert depth-8 sufficiency flatly, contradicting the correct hedge in §6.
6. Minor: "disc `|u| ≤ r`" in §1 (only the real interval is enclosed); "1/radius exactly" in §3.1 (8 s.f., with an unexplained residue and a missing probe source); stale "12 banked PASS" (36 exist).

## Final

**House verdict: GAPS NOT REFUTED.** The load-bearing mathematics — claims (a1-a3), (b), (c), (e) and the depth-8 measurements of (d2)/(d3) — reproduced exactly under my own independent probes, and (d2) strengthened to the true worst leaf. But three material claims are refuted (`rH<1/2` threshold, "worst failing leaf", the restart-cost mechanism) and the headline overclaims sufficiency. The note is not committable as written.

**GO / NO-GO: CONDITIONAL GO** for the depth-8 restart. The restart is justified — measured `rH ≈ 0.189-0.195` on the true worst leaf, `EXCLUDES_ZERO=True`, 2.13× below the *correct* 0.41421 threshold, on both edge orientations, with N=48 reproducing N=262 `rH` to 6 s.f. Conditions before spending the compute:

1. Use **`rH < 0.41421`**, not 0.5, as the per-leaf pass predictor everywhere.
2. Budget the restart as **1024 uniform depth-8 leaves ≈ 535 CPU-h / 45-50 wall-h at 12 workers**, with no resume from the depth-7 checkpoints; do not plan on "2 extra evaluations per open leaf" unless `q8_leaf_shard.py` is first given mixed-depth support (out of scope here).
3. Run the recommended pre-flight (§5A) at **N = 262** on the true worst leaves — path `[1,0,0,0,1,1,1]` of arc 2 first, plus at least one leaf from arcs 0/1 and a3 path `[0,1,0,1,0,1,0]` (which I found failing at depth 7, `rH = 0.695`) — ~4 leaf-evaluations, ~2 CPU-h, before the 50 h.
4. Screen the depth-7 receipts: any leaf with `rH > 4 × 0.41421 ≈ 1.66` is not predicted to clear depth 8. None observed (max 1.029), but arcs 0/1 and 460 of 512 leaves are unmeasured, so this remains **measured-on-samples, not proven**.

READY FOR JUDGING

---

*Installation note (orchestrator, 2026-08-21): produced by a read-only frontier-verifier and installed verbatim from its transcript.*

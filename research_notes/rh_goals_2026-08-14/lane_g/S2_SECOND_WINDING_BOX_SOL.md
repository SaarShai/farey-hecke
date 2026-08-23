# S2 — second winding box: B7 closed, B1 closed, half-width reconciled, frozen execution plan

- Date: 2026-08-23. Lane S2 (owner-approved). **Status: UNREFEREED.**
- Session interpreter: `/Users/za/.venvs/farey-rh/bin/python` (python-flint/Arb + mpmath).
  All work ran at 1–2 cores; the live d8 shard queue was not touched.
- LEDGER RULE honored: every number below is labelled by its evidence grade.
  Grades used: [ARB-MID] = midpoint of an Arb ball computation (rigorous ball
  arithmetic, midpoint quoted — NOT a certified enclosure by itself),
  [FLOAT] = plain double/mpmath float (NON-RIGOROUS), [CERT] = quoted from an
  existing certified receipt. Margins/clearances are **truncated toward the
  conservative direction** (extra digits printed, then cut — no
  round-to-nearest; the §8/C1 lesson of `SCAT1_PHIQ_ZERO_CERTIFIER_SOL.md`).
- Nothing else in the repo was edited. No commit was made. This file is new.

## 0. Verdicts, up front

1. **B7 (convention gate 0.4332 vs 0.4539): CLOSED — the discrepancy was a
   discretization BUG in the independent reimplementation, not a convention
   difference.** Root-caused, reproduced, and proven by a one-line fix that
   makes the very same reimplementation reproduce the flagship pin to 10
   decimals (§1). The certified engine's `sign=+1` operator is verified
   line-by-line against MMS arXiv:0912.2236 eq.(34) + the p.21 negative-branch
   definitions, and independently reimplemented from the paper in mpmath with
   a different discretization; worst builder-vs-builder relative error over a
   12-point grid spanning both sectors and both pins' ordinates: `8.2e-11`
   (§1.3). Caveat: this closure is UNREFEREED (this session's own work); the
   sector label should still be written "P-symmetric (mms+)", not "even".
2. **Half-width ±1e-6 vs ±1.01e-6: RECONCILED — the declared ±1e-6 box is
   contained in the operative certified ball; declared statements hold a
   fortiori** (§2).
3. **B1 (box freezability): CLOSED for BOTH second-pin candidates.** The
   4.5e-6 spread in `SECOND_PIN_PREP.md` was driven entirely by the N=16 row.
   Flagship-pattern re-pins at N = 22/28/36/44: fallback pin Re-spread
   `1.03e-12`, s_2 Re-spread `9.92e-11` — both freezable at ±1e-6 with orders
   of margin (§3).
4. **Candidate selection: the fallback pin `0.41054373549473627 +
   7.81976824701551188 i` is the recommended second box** (§4). ΔRe from the
   flagship = `0.0433514445` [FLOAT, truncated down] = 21675 box-widths;
   mildest B2 degradation of all candidates; K_s clearance `0.7056870`
   [FLOAT, truncated down] — larger than the flagship's certified `0.455100`.
5. **NOGO-OPEN-1: CLOSABLE, not yet closed.** The remaining blocker is purely
   compute + engineering: F_R closure at the new box at N = 160 is still not
   inferable (B2), and B3–B6 of `SECOND_PIN_PREP.md` (merge seams, bundle
   generator, sha plumbing, Kimi guards) remain code tasks. No conceptual or
   convention blocker survives this session. Frozen execution plan: §6.

---

## 1. B7 closed — root cause of the 0.4332 pin

### 1.1 What the "independent reimplementation" was

`projects/g5-crosscheck/{collocation_even_sonnet.py, results_sonnet.json}`
(worktree `aletheia-restore`; addendum commit `94bc6eb`). It located an
M-stable zero at `0.43318010033549964 + 5.6757468217484615 i`
(`|det| = 2.1e-10`, M = 14 and 22) from the flagship target — the 0.090
discrepancy that has gated every endpoint quote since V1 §1.3/§4.2.

### 1.2 Sign-swap hypothesis refuted first

Certified engine (`zeta_cert_rosen_q5.py`, UNMODIFIED, N = 22, n_head = 4),
`|det|` midpoints [ARB-MID]:

```
flagship (0.45389518,5.76353724)  sign=+1  6.821e-09   sign=-1  7.611e-01
sonnet   (0.43318010,5.67574682)  sign=+1  3.554e-01   sign=-1  8.333e-01
fallback (0.41054374,7.81976825)  sign=+1  2.295e-08   sign=-1  3.101e+00
sonnet_s2(0.35084450,7.86396390)  sign=+1  3.753e-01   sign=-1  3.468e+00
```

The sonnet pins are zeros of NEITHER sector of the certified operator — so
the sonnet code discretized a genuinely different operator, and the question
became which side is MMS-faithful.

### 1.3 Line-by-line + independent-implementation verification of the certified operator

(a) **Line-by-line against the paper.** MMS arXiv:0912.2236 (the PDF is
`lane_g/MMS_arxiv_0912.2236.pdf`, pp. 20–21) eq.(34), q = 2h_q+3 = 5
(h_q = 1, κ_q = 3):

```
(L_{s,±} g)_1 = L_{2,s} g_2 + Linf_{3,s} g_3 ± L_{-1,s} g_2 ± Linf_{-2,s} g_3
(L_{s,±} g)_2 =              Linf_{2,s} g_3 ± L_{-1,s} g_2 ± Linf_{-2,s} g_3
(L_{s,±} g)_3 = L_{1,s} g_1 + Linf_{2,s} g_3 ± L_{-1,s} g_2 ± Linf_{-2,s} g_3
```

with (p.21, below eq.(34)): for i > 0 the L coincide with eq.(26)/(27)
(`map −1/(z+nλ)`, weight `((z+nλ)²)^{-s}`), and
`L∞_{−i,s}g(z) = Σ_{n≥i} (z−nλ)^{-2s} g(1/(z−nλ))`,
`L_{−i,s}g(z) = (z−iλ)^{-2s} g(1/(z−iλ))`, squared-weight principal-sheet
convention per Lemma 5.1's proof. `build_reduced_matrix_ball`
(`zeta_cert_rosen_q5.py:328-…`) implements exactly these four terms per row
with `sgn = sign` on the two negative-branch terms; `sign=+1` therefore IS
the MMS `L_{s,+}` (P-symmetric / mms+) operator. The Hurwitz tail closure
(`_tail_block_allcols`) was re-derived independently in this session from
scratch (binomial expansion of the normalized monomial; pos:
`a0 = n0 + z/λ`, neg: `a0 = n0 − z/λ`, common per-m factor `(−1/λ)^m`,
common prefactor `(λ²)^{-s}`) and agrees with the engine's formula including
the neg-branch principal-sheet split.

(b) **Fresh independent mpmath implementation.** Written this session from
the paper text only (scratchpad `mms_q5_indep.py`; different discretization —
Cauchy-trapezoid Taylor coefficients, `dps = 30`, `n_head = 6` deliberately
different from the engine's 4). Values [FLOAT@30dps], N = 16, eps = +1:

```
flagship (0.45389518,5.76353724): |det| = 4.26e-9    (vanishes)
sonnet   (0.43318010,5.67574682): |det| = 0.3554     (does NOT vanish)
fallback (0.41054374,7.81976825): |det| = 8.56e-8    (vanishes)
generic  (0.30,6.00):             |det| = 1.6397
```

(c) **Builder-vs-builder grid** (same truncated object, N = 12, both signs,
σ ∈ {0.2, 0.35, 0.45}, t ∈ {5.76353724, 10.56029678} — the two pins'
ordinates; scratchpad `crossval_grid.py`). Relative error of the mpmath
implementation against the certified Arb builder's midpoints:

```
eps=+1 s=0.2+5.76353724i  |ref|=1.738938e+00 relerr=3.192e-16
eps=-1 s=0.2+5.76353724i  |ref|=6.016114e-01 relerr=5.536e-16
eps=+1 s=0.2+10.56029678i |ref|=5.694409e-01 relerr=8.134e-11
eps=-1 s=0.2+10.56029678i |ref|=6.361571e+00 relerr=3.517e-12
eps=+1 s=0.35+5.76353724i |ref|=5.071017e-01 relerr=5.714e-16
eps=-1 s=0.35+5.76353724i |ref|=7.291202e-01 relerr=2.745e-16
eps=+1 s=0.35+10.56029678i |ref|=8.212948e-01 relerr=1.573e-11
eps=-1 s=0.35+10.56029678i |ref|=2.755905e+00 relerr=2.297e-12
eps=+1 s=0.45+5.76353724i |ref|=1.546207e-02 relerr=1.261e-14
eps=-1 s=0.45+5.76353724i |ref|=7.603425e-01 relerr=1.460e-16
eps=+1 s=0.45+10.56029678i |ref|=1.162704e+00 relerr=4.253e-12
eps=-1 s=0.45+10.56029678i |ref|=1.771047e+00 relerr=1.625e-12
WORST 8.134158228041616e-11
```

Worst observed: `8.2e-11` (limited by 30-dps cancellation at t = 10.56, not
by any structural difference). This is the odd-q analogue of the accepted
`EVENQ_CROSSVAL_KIMI.md` q = 12 check, now at q = 5, both sectors.

### 1.4 The sonnet bug, found and PROVEN by fix

Reading + block-level probing showed sonnet's individual branch/tail blocks
agree with the true functional to `1e-13` (probe: sonnet
`single_branch_block` / `linf_block` applied to input-monomial node values vs
direct evaluation — all rel errs `1.5e-15 … 3.6e-13`). The defect is in the
ASSEMBLY's basis bookkeeping:

> Sonnet's state vector is function values at collocation nodes
> `z_a = c_j + 0.5·ρ_j·u_a` (`radius_scale = 0.5`, `u_a` = unit-circle
> roots), i.e. the Lagrange cardinal basis lives in the coordinate
> `x = (w − c_j)/(0.5·ρ_j)`. But every block evaluates the cardinal
> polynomials at `x_arg = (θ(z) − c_j)/ρ_j` — normalized by the FULL ρ_j.
> The factor-2 coordinate error means the assembled matrix discretizes the
> DIFFERENT operator `g ↦ weight(z)·g(c_j + (θ(z) − c_j)/2)`, which has its
> own (M-stable!) Fredholm zeros — at 0.4332.

Proof by fix (this session; sonnet's code used unmodified except the input
normalization radius `ρ_j → 0.5·ρ_j` in the block calls — the one-line
correction of the coordinate mismatch), Newton from the flagship target:

```
fix=False M=14: 0.4331804712+5.6757472946i |det|=1.58e-15   } exact reproduction
fix=False M=22: 0.4331801004+5.6757468217i |det|=1.34e-15   } of results_sonnet.json
fix=True  M=14: 0.4538989810+5.7635394327i |det|=6.61e-16
fix=True  M=22: 0.4538951801+5.7635372416i |det|=1.01e-15   <- flagship pin, 10 decimals
```

[FLOAT] With the fix, the SAME reimplementation — the one whose 0.4332 result
created B7 — reproduces the flagship `0.4538951800749447` to 10 decimals and
becomes a genuine independent-discretization confirmation.

### 1.5 B7 disposition

- The 0.4332 number is a bug artifact; no convention ambiguity survives.
- The certified engine's `sign=+1` operator is the MMS `L_{s,+}` per
  eq.(34)/p.21, verified (a) line-by-line, (b) by an independent mpmath
  implementation (§1.3), (c) by the repaired collocation discretization
  (§1.4). Three distinct discretizations now agree on the flagship pin.
- Standing label correction still applies: write "P-symmetric (mms+)
  sector", not "even sector" (V1 §4.2; `zeta_mayer_rosen.py:68-72`).
- Remaining caveat: this closure is UNREFEREED. Before paper quotation, a
  cold referee should replay §1.2–§1.4 (all commands are in this session's
  transcript; the two scratchpad scripts total < 200 lines).

## 2. Half-width reconciliation (±1e-6 declared vs ±1.01e-6 printed)

The flagship box is constructed (`r3b_endpoint.py:53-57`,
`certify_r2_flagship.py:59,399-400`) as
`arb("0.4538951800749447") + arb(0, arb("1e-6"))` per coordinate. Direct
inspection of the stored ball [ARB]:

```
>>> x = arb("0.4538951800749447") + arb(0, arb("1e-6"))
>>> float(x.rad())
1.00000000458067e-06        # operative radius
>>> float(x.rad() - arb(10)**-6)
4.580670065479353e-15       # excess over exact 1e-6
```

- The operative certified radius is `1.00000000458067e-6`: the decimal string
  "1e-6" is not binary-representable, so Arb stores an upward-rounded binary
  radius (excess `4.6e-15`), and the JSON's "±1.01e-6" is Arb's PRINT-TIME
  radius display, which always rounds the radius UP to few digits.
- Therefore: **operative certified ball ⊃ declared closed box
  [center ± 1e-6]²**. Every enclosure certified over the ball holds on the
  declared box a fortiori; every margin/clearance in the receipts was
  computed AT the (slightly larger) operative ball and is therefore
  conservative for the declared box. The declaration "±1e-6" in
  `THEOREM_G5_OFFLINE_ASSEMBLY.md` is safe as written.
- Referee item 12 of `SCAT1_PHIQ_ZERO_CERTIFIER_REFEREE.md` is discharged:
  the two figures are the same object at two print precisions, with the
  containment in the safe direction. Recommended paper footnote: "box
  half-width 1e-6; the Arb receipt prints the (upward-rounded) operative
  radius 1.01e-6, whose ball contains the stated box."

## 3. B1 closed — flagship-pattern re-pins at N = 22/28/36/44

Method: complex Newton on the certified builder's det midpoints
(`build_reduced_matrix_ball` + `_det_block`, sign = +1, n_head = 4), seeded
from the scan pins; numerical derivative h = 1e-9; convergence |dz| < 1e-13.
[ARB-MID; the pins are midpoint-Newton values, NOT certified enclosures —
the certification is the winding box, exactly as for the flagship.]

**Fallback pin (seed 0.41054373549576567, 7.819768247017059):**

```
PIN N=22: 0.41054373549576567 7.81976824701705908   (2s)
PIN N=28: 0.41054373549473622 7.81976824701551188   (7s)
PIN N=36: 0.41054373549473627 7.81976824701551188   (11s)
PIN N=44: 0.41054373549473627 7.81976824701551188   (18s)
re_spread 1.0294542995836764e-12  im_spread 1.5472068071176182e-12
```

Stable to 12 decimals from N = 28 on — the ±1e-6 box has ~6 orders of
freeze margin. **FROZEN second-pin constants (recommended):**
`PIN_RE = 0.41054373549473627`, `PIN_IM = 7.81976824701551188`.

**s_2 (seed 0.24302842340131198, 10.560296779143401):**

```
PIN N=22: 0.24302842340131198 10.56029677914340148
PIN N=28: 0.24302842350047418 10.56029678032932750
PIN N=36: 0.24302842350057649 10.56029678032925112
PIN N=44: 0.24302842350057649 10.56029678032925112
re_spread 9.926451327579855e-11  im_spread 1.185926024049877e-09
```

Also freezable (`SECOND_PIN_PREP.md` B1's 4.5e-6 spread was entirely the
N = 16 row, which is below this candidate's convergence floor). If s_2 is
ever run: `PIN_RE = 0.24302842350057649`, `PIN_IM = 10.56029678032925112`.

**Independent-discretization confirmation of both candidates** (the §1.4
repaired collocation code, M = 22) [FLOAT]:

```
fallback: 0.410543734234+7.819768243221i  (agrees with frozen pin to ~4e-9)
s2:       0.243027349925+10.560296628835i (agrees to ~1.1e-6; slower
          M-convergence at |t|=10.56 — consistent with the B2 degradation)
```

## 4. Candidate selection: the fallback pin is the second box

Per the referee-corrected fallback table (`SCAT1…SOL.md` §8/C2), only
`0.4105437` (|t| = 7.82) is a genuine milder fallback. This session adds:

| criterion | fallback 0.4105437 + 7.8198i | s_2 0.2430284 + 10.5603i |
|---|---|---|
| ΔRe vs flagship [FLOAT, trunc down] | 0.0433514445 (= 21675 declared box-widths) | 0.2108667565 |
| B1 (re-pin spread, N 22–44) | 1.03e-12 — closed | 9.92e-11 — closed |
| B2 deep-tail p = 2(σ−1e-6) [trunc down] | 0.8210854709 (flagship: 0.9077883601) | 0.4860548468 |
| B2 angle factor driver \|t\| | 7.8198 (flagship 5.7635) | 10.5603 |
| K_s point clearance [FLOAT, trunc down] | 0.7056870 (nearest lattice zero (0, k=5) at (0, 7.245792536496066)) | 0.4819487 (matches prep's 0.481952 within float; nearest (0, k=7)) |
| scan-level winding | 1, `zero_certified: true`, ball [0.99999949, 1.00000051], K=28, hx=hy=0.012 | 1, ball [0.99996722, 1.00003277] |

Both K_s clearances exceed the flagship's certified 0.455100; both must be
re-evaluated through the certified Arb path in production (these are the
scan's float metric — NOT EVIDENCE, flagged per prep §3).

ΔRe = 0.0433514445 with two ±1e-6 boxes gives certified distinct real parts
with ≥ 0.0433494445 to spare — the NOGO-OPEN-1 requirement ("two φ_5 zeros
at distinct real parts", via Lemma 3.1 reflection to
`Re ρ = 1 − 0.4105437… ≈ 0.5894543` vs the flagship's `0.5461048`) is met by
this pair if the second box certifies.

**Why not s_2 first:** every B2 driver is strictly worse (p 0.82 → 0.49,
|t| 7.82 → 10.56), the flagship margin was only 3.4e-8, and the prep note
already flags that s_2 may need N > 160 at steeply rising cost. The fallback
maximizes the probability that N = 160 closes. s_2 remains the
prestige target (ΔRe > 0.21) for a later run; nothing here retires it.

## 5. What remains open (honest)

- **B2 — F_R closure at the new box is still not inferable.** No W/R2/R3b
  re-run was executed this session. The head-weight inflation between
  p = 0.908 and p = 0.800 in the existing W V2 table (18.64 → 232.2) brackets
  the fallback's p = 0.821; whether the final margin closes at N = 160 must
  come out of Phase 1 below, and the plan gates all Kaggle spend on it.
- **B3–B6** (merge seam handling, bundle generator rewrite, sha-pin plumbing,
  the two Kimi-K3 guards + re-derived gate literals) are unchanged code
  tasks; see `SECOND_PIN_PREP.md` §5.
- **This note is UNREFEREED**, including the B7 closure. The corollary
  upgrade in `NO_VERTICAL_LINE_COROLLARY.md` must NOT be edited until the
  second box certifies AND a cold referee passes this note.

## 6. Frozen execution plan (ready to dispatch)

Phase numbering follows `SECOND_PIN_PREP.md` §4; deltas frozen here.

- **Phase 0 — DONE (this session).** Pins frozen (§3):
  `PIN_RE = 0.41054373549473627`, `PIN_IM = 7.81976824701551188`,
  `HALF_WIDTH = "1e-6"`.
- **Phase 1 — box-local receipts (local, background, ≤ 2 cores).** Copies
  (never in-place) of `certify_r2_flagship.py`, `certify_r3_flagship.py`,
  `r3b_endpoint.py`, `certify_r3b_flagship.py` from
  `.worktrees/aletheia-restore/code/tb_certify/` into a new
  `code/second_pin/` dir; replace the three PIN constant sites; W-envelope
  re-run for the new box first, then R2; update `R2_EXPECTED_SHA256` in the
  orchestrator copy; add the two Kimi guards (assert `rho >= center_ratio`
  in the endpoint copy — MUST be re-verified at this box; assert unique FTC
  direction overlap) and re-derive the two gate literals from raw records.
  TB V2 + E1 + K_s receipts reused verbatim (no `s` dependence — prep §2).
  Expected wall: W+R2 were minutes-scale at the flagship; budget ≤ 1 h.
  **GATE: inspect F_R(new box) against the flagship's 1.78e-6 and the
  endpoint B; if the projected per-arc margin at N = 160 is below ~1e-8,
  STOP and re-plan N before any arc is run.**
- **Phase 2 — local smoke.** `--self-test`, then `--arcs 0:2 --workers 2`
  (NOT 4 — the d8 queue owns the box's cores; cap total at 2–3). Flagship
  calibration ≈ 212 s CPU/arc at N = 160; expect ≈ 7–10 min wall.
- **Phase 3 — full contour.** 192 base arcs, N = 160 first attempt.
  Local option: ~17 CPU-h ≈ 8.5 h at 2 workers — feasible overnight AFTER
  the d8 queue drains, else Kaggle 16-chunk pattern (chunk NN →
  `--arcs 12·NN : 12·NN+12`, 4 workers/kernel, 5-slot feeder; per-chunk ≈
  21–45 min; B4 bundle rewrite required first).
- **Phase 4 — merge + closure.** Extend `merge_chunks_and_verify_closure`
  for subdivided seams (B3) or verify chunks accept whole base arcs; then
  the adjacent-box overlap-polygon winding check; write the merge driver
  (does not exist yet).
- **Phase 5 — assembly.** N = 128 control arm (expected NOT_CERTIFIED),
  report render, second-pin cert doc mirroring
  `THEOREM_G5_OFFLINE_ASSEMBLY.md`, THEN (referee-gated) the
  `NO_VERTICAL_LINE_COROLLARY.md` upgrade with the Lemma 3.1 corollary:
  two φ_5 zeros at `Re ρ ≈ 0.5461` and `≈ 0.5895` — closing NOGO-OPEN-1.

## 7. Receipts index (session)

- Certified-builder evaluations, re-pins, K_s distances: commands and full
  outputs inline above; all runs used `zeta_cert_rosen_q5.py` UNMODIFIED
  from `.worktrees/aletheia-restore/code/`.
- Scratchpad artifacts (session-local, quoted in full where load-bearing):
  `mms_q5_indep.py` (independent mpmath builder), `crossval_grid.py`,
  `repin_fallback.log`.
- Flagship sources referenced: `r3b_endpoint.py:53-57`,
  `certify_r2_flagship.py:59,368-373,399-400`,
  `collocation_even_sonnet.py:119-167,189-217,235-270`,
  `results_sonnet.json`, commit `94bc6eb`.

## §8 — Referee corrections applied (2026-08-23, append-only)

The following entries record the cold referee's C1–C7 and m1–m7 corrections. Each corrected superseding statement governs any conflicting wording above.

### C1 — §2 half-width reconciliation and object identity

- **Referee point:** §2 used `1.00000000458067e-6` from the solid `flagship_s_box`, although the localization contour is constructed by `closed_boundary_segments(..., arb(HALF_WIDTH), ...)`; the cited receipt itself records the contour half-width, and the original a-fortiori implication reverses the load-bearing zero-localization logic.
- **Corrected superseding statement:** The half-width reconciliation must cite the CONTOUR construction `arb("1e-6")` (radius ~4.5e-23) and the receipt's own `"half_width": "[1.00000000000000000000000e-6 +/- 1e-34]"` field, not the solid `flagship_s_box`. The a-fortiori direction in the original §2 is retracted; any a-fortiori statement is restricted to enclosure-type quantities and does not infer a zero in the smaller declared box from a zero in a larger region.

### C2 — Reflected endpoint

- **Referee point:** §4's `Re ρ ≈ 0.5894543` is an arithmetic/transposition error in the paper-facing reflected endpoint.
- **Corrected superseding statement:** The reflected endpoint is `Re rho = 0.5894562645052637 (= 1 − 0.41054373549473627)`. The value `0.5894543` is WRONG and is superseded everywhere.

### C3 — Missing B7 traceability artifacts

- **Referee point:** The §7 receipts index lists three scratchpad artifacts that do not exist in the repository or worktrees; §1.3(b)(c) and the fallback winding row therefore cannot be reached by a later referee.
- **Corrected superseding statement:** The three §7 receipts-index items `mms_q5_indep.py`, `crossval_grid.py`, and `repin_fallback.log` are declared MISSING. §1.3(b)(c) and the fallback winding ball `[0.99999949, 1.00000051]` are downgraded to UNVERIFIABLE-pending-artifact. The decisive proof-by-fix evidence remains separately reproduced, but it does not restore the missing receipt chain.

### C4 — MMS citation and 1-E7 caveat

- **Referee point:** The three-row operator display is `reduced3`, not MMS eq. (34); eq. (34) is the `LoverK` factorization, and the q=5 heading caveat was omitted.
- **Corrected superseding statement:** The citation is corrected to `MMS reduced3 display (content verified)`, with eq.(34) identified as the `LoverK` factorization. The 1-E7 caveat is reinstated: the heading prints `q > 5` while Lemma 4.2 states `q ≥ 5`, so the q=5 identification rests on the general incidence formula and must carry that footnote.

### C5 — Cross-validation coverage

- **Referee point:** The advertised grid uses ordinates `5.76353724` and `10.56029678`, corresponding to the flagship and s_2 pins, while the selected second pin has `|t| = 7.8198` and is absent.
- **Corrected superseding statement:** The crossval-grid coverage claim is narrowed to `t = 5.76` and `t = 10.56`; it does NOT cover the selected pin's `t = 7.82`.

### C6 — Frozen execution plan and dead N=160 claims

- **Referee point:** §6 names the wrong source directory for two scripts, incorrectly says there is no s-dependent K_s work, and retains the failed N=160 campaign constants and route.
- **Corrected superseding statement:** The N=160 constants and associated cost/route claims are marked dead (gate FAIL); the campaign runs N=288. Source-directory names are corrected per the referee: `certify_r2_flagship.py` and `r3b_endpoint.py` are in `code/tb_certify/`, while `certify_r3_flagship.py` and `certify_r3b_flagship.py` are in `code/tc_rerun/`. The claim of “no s-dependent K_s work” is retracted: the divisor lattice is s-independent, but the per-pin K_s distance/clearance evaluation is required.

### C7 — K_s grading

- **Referee point:** §4 calls the flagship's `0.455100` “certified” while grading the identically derived candidate values as point margins, contrary to the assembly document's LEDGER RULE.
- **Corrected superseding statement:** Grading is harmonized: flagship `0.455100` is restated as a point margin per the assembly doc. The candidate clearances are point margins as well, with no box-certification upgrade implied.

### m1 — Pin digits

- **Referee point:** The 17–18 significant digits quoted for the §3 pin come from double-precision midpoint Newton and include exact-binary-expansion digits beyond converged information.
- **Corrected superseding statement:** `PIN_IM = 7.81976824701551188` is retained only as a frozen constant parsed by the code; it is not claimed as converged information beyond the supported stability (the rerun gives `7.819768247015512`).

### m2 — B1 freezability

- **Referee point:** The B1 evidence varies N only; `n_head = 4`, `sign = +1`, and double-precision midpoint arithmetic remain fixed.
- **Corrected superseding statement:** The B1 result supports N-spread stability only. A stronger freezability statement remains pending one fixed-N perturbation of `n_head` (for example `n_head = 6`), with the fixed sign and arithmetic recorded.

### m3 — s_2 B2 inconsistency

- **Referee point:** §4's `s_2` value `B2 p = 0.4860548468` is derived from the N=22 value `0.24302842340131198`, not from the frozen §3 value `0.24302842350057649`.
- **Corrected superseding statement:** The `0.4860548468` figure is explicitly N=22-derived; if it is derived from the frozen §3 value instead, the superseding figure is `0.4860548470`. The internal inconsistency is not treated as a single frozen value without its source N.

### m4 — NOGO-OPEN-1 closing condition

- **Referee point:** The conditional closure sentence omits the requirements that the zero be nonreal, off-line, and strictly interior.
- **Corrected superseding statement:** The NOGO-OPEN-1 requirement is met by this pair only if the second box certifies and the selected zero is nonreal, off-line, and strictly interior with `0 < Re s* < 1/2`; both pins satisfy these conditions numerically.

### m5 — Box-width convention

- **Referee point:** `21675` and `21676` differ because the former is truncation-down and the latter round-up for the same full-width quantity; the half-width reading would give `43351`.
- **Corrected superseding statement:** `21675` is the conservative truncation-down count of `21675.72` full box-widths at width `2e-6`; `21676` is a round-up convention, not a contradiction. On a half-width reading the corresponding count is `43351`.

### m6 — Midpoint versus ball validation

- **Referee point:** §1.3(c) compares the independent mpmath builder with Arb midpoints, validating the formula but not ball radii or enclosure semantics.
- **Corrected superseding statement:** The mpmath cross-check is described as midpoint/formula validation only; it is not independent validation of Arb ball radii or enclosure semantics.

### m7 — Dimension-tail qualification

- **Referee point:** The §1.2 N=22 table has no dimension-tail bound, so `6.821e-09` and `2.295e-08` are small midpoint values, not certified zeros.
- **Corrected superseding statement:** The §1.2 entries `6.821e-09` and `2.295e-08` are reported as small [ARB-MID] evidence, not as zeros; the phrase “zeros of NEITHER sector” is not promoted beyond what the midpoint evidence supports.

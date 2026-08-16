# F7 STAGE-4b RE-OPTIMIZATION — the enlarged-contour blocker, resolved

Date: 2026-08-15. Lane F, follow-up to
`f7_receipts/smoke/F7_R3B_SMOKE_CERT.md` (stage 4b BLOCKED: six full-Markov
blocks' enlarged-contour ratios above 1, `F_R ≈ 1.98e+61452309` at N=256).
Scope: exactly the three levers the smoke report names — radii,
`ENLARGEMENT_MARGIN_DIVISOR`, per-block enlargement headroom. No Kaggle, no
commit, no other lanes' files.

**Verdict: GO.** All three gates pass. The adopted radii did **not** change.

---

## 1. Diagnosis — the blocker was never the radii

The enlargement rule in `f7_r3b_endpoint.derive_enlarged_discs` was

```
e_B = clearance_B / ENLARGEMENT_MARGIN_DIVISOR        (divisor = 4)
```

i.e. it was scaled **only** by the pole/branch-cut clearance and carried no
reference to the disc's own radius. At q=7 the discs are small
(R₁…R₅ = 0.1744, 0.1441, 0.1626, 0.1773, 0.2855) while the clearances are
large (1.02 … 4.38), so a quarter of the clearance is **2.4× to 6.3× the
radius itself**. Measured from the smoke receipt:

| block | R | clearance | e = clr/4 | R_enl | R_enl/R | ratio |
|:---|---:|---:|---:|---:|---:|---:|
| 3→1, +1, head | 0.16256 | 1.01589 | 0.25397 | 0.41653 | **2.56** | 2.6456 |
| 4→2, +1, head | 0.17727 | 1.16875 | 0.29219 | 0.46945 | **2.65** | 2.7353 |
| 5→3, +1, head | 0.28552 | 1.33797 | 0.33449 | 0.62001 | **2.17** | 2.2968 |
| 5→4, −1, head | 0.28552 | 1.69487 | 0.42372 | 0.70923 | **2.48** | 1.8667 |
| 4→4, −1, head | 0.17727 | 2.08060 | 0.52015 | 0.69742 | 3.93 | 1.0442 |
| 2→5, +2, tail | 0.14410 | 2.71280 | 0.67820 | 0.82230 | 5.71 | 1.0965 |
| 3→5, +2, tail | 0.16256 | 2.81783 | 0.70446 | 0.86701 | 5.33 | 1.0323 |

The six blocks the `F7_CONSTANTS_MANIFEST.md` §3 flagged as full-Markov are
exactly the ones that break (plus `3→5, +2` and `4→4, −1`, marginally). The
un-enlarged TB-certified ρ\* is 0.763212; the geometry is healthy. What was
unhealthy was asking a contraction certified on a disc of radius 0.163 to
survive on a disc of radius 0.417.

The q=5 analogue (`lane_g/certify_e1_enlarged.py`) used a flat additive
`ε = 0.1` on q=5 radii of ~0.19–0.32 — i.e. an *implicit* relative
enlargement of ~30–50%, never a 2–6× blow-up. The q=7 port replaced that flat
ε by "clearance/4" and, at q=7's much larger clearances, silently left the
regime the q=5 constant had kept it in. **This is a porting defect, not a
statement about κ=5 geometry.**

## 2. Lever chosen

Add a **relative cap** on the enlargement (surgical, 5 lines in
`f7_r3b_endpoint.py`):

```
e_B = min( clearance_B / 4 ,  CAP · R_i ),     CAP = 0.15
```

`CAP = "0"` restores the legacy rule. The rule and the cap are recorded in
every per-block record, so no receipt is silently reinterpreted.

Both other levers were left untouched and are **not needed**:

- **Radii**: unchanged at the adopted `(3.522, 2.622, 2.372, 1.79, 1.6)`.
  Re-optimizing them would have regressed d₅ = 1.6, the value the mitigation
  report showed governs endpoint tail-column growth (gate 3).
- **`ENLARGEMENT_MARGIN_DIVISOR`**: unchanged at 4. Raising it uniformly is a
  strictly worse instrument — it would have to reach ≈ 25 to bring 5→3 under
  control, and would then over-shrink the *tail* blocks' enlargement (their
  clearances are 3–4×) and push η toward 1 for no reason.

### Cap scan (Arb at 384 bits, M=512 arcs, all 19 blocks; a SEARCH, not a certificate)

`scan_alpha.py`, scratchpad. ρ̂ = max over all 19 blocks of the enlarged-contour
ratio (head: `center_included_base_ratio`; tail: `center_included_rho`).

| CAP | η = R/R_enl | ρ̂ (worst block) | verdict |
|---:|---:|---:|:---|
| legacy `clr/4` | 0.121–0.461 | 2.7353 (4→2, +1, head) | FAIL |
| 0.10 | 0.909091 | 0.863451 (5→3, +1, head) | pass |
| **0.15** | **0.869565** | **0.915241 (5→3, +1, head)** | **ADOPTED** |
| 0.20 | 0.833333 | 0.968190 (5→3, +1, head) | pass, thin |
| 0.25 | 0.800000 | 1.022339 (5→3, +1, head) | FAIL |

CAP = 0.15 is the largest 0.05-grid value that lands ρ̂ **below the q=5
chain's own ρ̂ ≤ 0.948343590351** while keeping η = 0.869565 — so
η²²⁴ ≈ 2.5e−14 and the output-tail corrections are numerically irrelevant.
The binding block at every cap is `5→3, +1, head`, the same block that binds
the un-enlarged ρ\*: the geometry is consistent, not pathological.

## 3. Certified results (Arb/Acb, 384 bits, directed rounding)

Driver: `f7_stage4b_reopt.py`. Immutable inputs re-hashed and matched before
any arithmetic (`R2 4e5f0105…`, `TB V2 93baddf5…`).

### Gate 1 — un-enlarged certified ρ\* < 0.80

`f7_certify_tb_blocks.py` re-run at the adopted radii; every field of the
banked receipt reproduced **byte-identically** (`rho_star_upper_bound`,
`source_radii`, all 19 `blocks`, `pole_clearance`, `branch_cut_clearance`,
`certification_verdict`).

**ρ\* ≤ 0.763212029206899202166157**, worst block `5→3, +1, head`,
verdict `PASS_RHO_LT_0.80`. **PASS.**

Also re-verified byte-identically: the W envelope
(W^(≥1) = 7.08501261150862810346347, W^(0) = 6.54960613713658448989529,
F = 1.97300869555021851791109e+41) and the R2 envelope
(B_total = 119.06285559909506923733105505540038073444…, and all eight
`tail_bounds` at N = 192/224/232/234/236/238/240/256 identical).

### Gate 2 — all 19 ENLARGED-contour ratios < 1

Receipt: `f7_receipts/F7_E1_ENLARGED_CONTRACTION_V2_RECEIPT.json`
(schema `f7-e1-enlarged-contraction/v2`, the q=7 analogue of
`lane_g/E1_ENLARGED_CONTRACTION_RECEIPT.json`). Verdict
**`PASS_RHO_HAT_LT_1`**.

**ρ̂ ≤ 0.9152411837446922** (rounded UP), worst block `5→3, +1, head`.
η ≤ 0.8695652173913044 for all 19 blocks, all strictly below 1.
Every block's remaining pole/branch-cut clearance stays positive
(min 0.99150, block `3→1, +1, head`).

| block | R_enl | ratio ≤ | <1 |
|:---|---:|---:|:--|
| 1→4, +2, head | 0.20055 | 0.661639708053 | yes |
| 1→5, +3, tail | 0.20055 | 0.751081661530 | yes |
| 1→4, −1, head | 0.20055 | 0.595352602020 | yes |
| 1→5, −2, tail | 0.20055 | 0.751532746242 | yes |
| 2→5, +2, tail | 0.16571 | 0.759108301108 | yes |
| 2→4, −1, head | 0.16571 | 0.493913290609 | yes |
| 2→5, −2, tail | 0.16571 | 0.751851874675 | yes |
| 3→1, +1, head | 0.18694 | 0.901726982030 | yes |
| 3→5, +2, tail | 0.18694 | 0.758585218939 | yes |
| 3→4, −1, head | 0.18694 | 0.412571466699 | yes |
| 3→5, −2, tail | 0.18694 | 0.752520252163 | yes |
| 4→2, +1, head | 0.20385 | 0.893088966843 | yes |
| 4→5, +2, tail | 0.20385 | 0.757822045627 | yes |
| 4→4, −1, head | 0.20385 | 0.280485435165 | yes |
| 4→5, −2, tail | 0.20385 | 0.753382556481 | yes |
| **5→3, +1, head** | 0.32834 | **0.915241183745** | yes |
| 5→5, +2, tail | 0.32834 | 0.757055878103 | yes |
| 5→4, −1, head | 0.32834 | 0.842819415625 | yes |
| 5→5, −2, tail | 0.32834 | 0.755302468394 | yes |

**PASS** — and below the q=5 chain's ρ̂ ≤ 0.9484.

### Gate 3 — endpoint B < 30 and flat in N

Receipt: `f7_receipts/F7_R3B_ENDPOINT_V2_RECEIPT.json`. B_same is the
certified bound on both `‖L‖₁` and `‖LP_N‖₁`: computed-row column-2-norm sum
+ enlarged-disc output-tail corrections + immutable R2 input tail.

| N | computed-row column-2-norm sum | Σ output-tail corrections | T_tail (R2, immutable) | **B_same ≤** |
|---:|---:|---:|---:|---:|
| 224 | 20.16963679020219665298 | 6.7478e−11 | 1.4792e−23 | **20.169636790269674667** |
| 238 | 20.16963686107914943784 | 9.5366e−12 | 3.2636e−25 | **20.169636861088686015** |
| 256 | 20.16963692338440205739 | 7.7060e−13 | 2.4115e−27 | **20.169636923385172662** |

**PASS** — B ≤ 20.1697 < 30, flat in N (ΔB < 1.4e−7 across N = 224→256;
d₅ = 1.6 untouched, so the mitigation lesson is not regressed).

This is the load-bearing repair. Under the legacy rule the correction sum at
N=256 was **7.07e+7**; under the cap it is **7.71e−13** — 20 orders of
magnitude, purchased entirely by η dropping from ~0.25 to 0.8696 being
*irrelevant* once ρ̂ < 1 bounds `U_{B,k}` uniformly in k (the legacy run had
ρ̂ > 1, so `U_{B,k}` grew like ρ̂^k and no η could rescue it).

### F_R table and the m₀ rule

`F_R = T_tail(N) · exp(1 + 2·B_same(N))`, Arb upper endpoint.
m₀ = 3.313176035446919e−06 (N=32 sampled boundary minimum — **NON-RIGOROUS**
float preparation, a sample not a cover), threshold 0.1·m₀ = 3.313176e−07.
Receipt: `f7_receipts/F7_STAGE2_FR_V2_RECEIPT.json`.

| N | T_tail ≤ | B_same ≤ | **F_R ≤** | vs 0.1·m₀ |
|---:|---:|---:|---:|:--|
| 224 | 1.4792e−23 | 20.169636790 | 1.328761e−05 | fail (×40 over) |
| 238 | 3.2636e−25 | 20.169636861 | 2.931669e−07 | **PASS** (×1.13) |
| 256 | 2.4115e−27 | 20.169636923 | 2.166224e−09 | **PASS** (×153) |

`N* = 238` is the smallest passing N; the frozen `N_PRIMARY = 256` clears by
×153 and `N_COMPARISON = 224` remains a justified NOT_CERTIFIED control arm.
These reproduce the v1 planning numbers to every printed digit, which is the
point: the corrections are now small enough not to move F_R at all.

The F_R side is certified; the threshold side inherits m₀'s non-rigor, so this
remains a **planning gate for freezing N\***, not a certificate.

## 4. GO / NO-GO for the Kaggle launch

**GO.** Stage 4b is unblocked with the adopted radii unchanged, so nothing
upstream (TB, W, R2, endpoint B, the 16-way chunk table in
`F7_PILOT_REPORT.md` §4, the `N_PRIMARY = 256 / N_COMPARISON = 224` freeze)
needs revision. The only artifact the closed-contour phase consumes from
stage 4b is `F_R(N)`, and it is now 2.166e−09 at N=256 — finite, small, and
×153 inside the m₀ rule.

Launch preconditions still owed by the launcher, unchanged by this work:
the closed-contour cover itself is untouched here (the smoke run reached
`evaluations = 0`), so the Kaggle run is the *first* execution of the winding
phase and its cost estimate (~420 CPU-h) is still an estimate, not a measured
pilot.

## 5. Honest scope and caveats

- The cap `0.15` is a **chosen constant**, like the q=5 ε = 0.1 and like the
  ρ\* gate 0.80. It is not a theorem constant. What is certified is ρ̂ ≤
  0.9152 *at that cap*, and the certificate records the cap.
- Gate 3's "flat in N" is measured at three N values (224/238/256), not
  proved. It agrees with the mitigation report's N = 32…224 series.
- m₀ is a 96-point sample at N=32. The N\* = 238 margin (×1.13) is thin
  against a value that can only be an over-estimate of the true boundary
  minimum; N\* = 256 is the safe freeze and is what is frozen.
- No claim is made about the closed-contour winding, the MMS sector
  factorization, or `det(1−K_s) ≠ 0` — all outside stage 4b.
- `f7_r3b_endpoint.py` changed, so its sha256 moved from
  `3ad7918899c70bda…` to `3d397de009122966…`. The smoke receipts under
  `f7_receipts/smoke/` still record the old hash and are left untouched as the
  historical record of the blocked run.

## 6. Artifacts

New (this session):

- `f7_stage4b_reopt.py` — the stage-4b driver.
- `f7_receipts/F7_E1_ENLARGED_CONTRACTION_V2_RECEIPT.json` — E1 analogue, ρ̂ gate.
- `f7_receipts/F7_R3B_ENDPOINT_V2_RECEIPT.json` — B_same / F_R at N = 224/238/256.
- `f7_receipts/F7_STAGE2_FR_V2_RECEIPT.json` — the m₀ decision rule, v2.

Modified: `f7_r3b_endpoint.py` (`ENLARGEMENT_RELATIVE_CAP`, the `min(...)`,
and two extra provenance fields per block record).

Untouched: all pre-existing receipts, `f7_certify_tb_blocks.py`,
`f7_certify_tb_weights.py`, `f7_certify_r2_flagship.py`,
`f7_certify_r3b_flagship.py`, every q=5 file, every other lane.

Reproduce:

```bash
/Users/za/.venvs/farey-rh/bin/python \
  research_notes/rh_goals_2026-08-14/lane_f/f7_stage4b_reopt.py
```

Wall time 174.7 s (enlarged sups 512 arcs × 19 blocks, then three matrix
builds at 384 bits: 50.6 s / 56.8 s / 66.4 s).

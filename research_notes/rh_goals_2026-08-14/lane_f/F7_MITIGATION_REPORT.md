# F7 MITIGATION REPORT — q=7 stage-0 re-optimization after the BLOCKED pilot

Date: 2026-08-15. Lane F, follow-up to `F7_PILOT_REPORT.md` (stage-1 gate
BLOCKED: `B_finite(N=224) ≈ 1.145e9` vs the plan's `B ≈ 30` stop threshold).
Scope: exactly the two mitigation options frozen by `F7_CERT_PLAN.md` §3 and
`F7_PILOT_REPORT.md` §2 — (1) deeper stage-0 grid over the five disc inflation
factors, (2) per-block / per-Hurwitz-class radii as the second lever. Nothing
beyond these was executed: no `--arcs` CLI work, no TB/R2/R3b certification, no
Kaggle kernels, no other lanes' files.

**All stage-0 values below are NON-RIGOROUS FLOAT PREPARATION** (float64,
2,048 circle points per disc, tail indices n0..59, blocks captured from the
authoritative `zeta_mayer_rosen.build_reduced_matrix`, q=7, sign=+1,
n_head=4 — the pilot's machinery, unchanged). The `B_finite` endpoint
measurements are 384-bit Arb/Acb ball arithmetic over the entire closed
`1e-6` flagship box around s₀ = 0.4751647621098225 + 4.668743786424289 i,
identical in kind to the pilot's; they are rigorous *given the radii*, but the
radii themselves are float-stage-0 output, not yet Arb TB-certified.

Scripts (this directory): `f7_mitigation_stage0.py`,
`f7_mitigation_pareto.py`, `f7_mitigation_endpoint.py`; receipts
`f7_mitigation_stage0_results.json`, `f7_mitigation_pareto_results.json`,
`f7_mitigation_endpoint_results.json`.

## 0. Validation gate (reconstruction fidelity)

The pilot did not persist its endpoint script; it was reconstructed as
`f7_mitigation_endpoint.py` (a verbatim copy of
`zeta_cert_rosen.build_reduced_matrix_ball` with per-disc inflated radii
`rho_i = d_i · half_i` replacing the engine default). At the frozen factors
`(2.79, 2.39, 1.90, 1.56, 1.35)`, N=32 it returns

  `B_finite <= 18.0743955713902115226430978271` (pilot: `18.074395571390211522643097827116`)

and the float baseline reproduces `rho* = 0.782263813617748` exactly.
The reconstruction is faithful.

## 1. Grid searched (option 1 — deeper shared-radii search)

- Fine global grid: 13 values/coordinate
  `{1.30, 1.45, 1.60, 1.75, 1.90, 2.05, 2.20, 2.40, 2.60, 2.80, 3.00, 3.25, 3.50}`,
  all 13⁵ = 371,293 combinations (pilot: 10⁵ = 100,000 on a coarser grid).
- Then coordinate-descent polishing (steps 0.05 → 0.02 → 0.01 → 0.005 → 0.002
  → 0.001, per-coordinate sweeps to convergence) from 245 deterministic
  starts: the grid best, the frozen point, and the 243-point ±0.15 shell
  around the frozen point. Factors clipped to [0.95, 6.0].

## 2. Best radii found and new rho*

**Option 1 (shared-radii rho\* minimizer):**

  `(d_1..d_5) = (3.500, 2.622, 2.210, 1.740, 1.462)`
  float `rho* = 0.7291284888867575` → reported rounded down: **`0.729128488886`**
  worst block `(5->4, n=-1 head)`; five blocks equalized within 0.0003
  (classic min-max signature of a true local optimum).

**Option 2 (per-block investigation), two results:**

- *Unrealizable floor.* Optimizing each of the 19 blocks independently over
  its own (source, target) inflation pair gives
  `max_b min_{s,t} ratio_b = 0.195927105432` — the theoretical floor if radii
  were not shared per disc. The binding block is still `(2->5, n=2 tail)`
  (floor 0.1959 at pair ≈ (0.97, 5.10)). This floor is NOT attainable: the
  κN×κN matrix has one radius per disc, and the per-block optima want source
  inflations < 1 (a disc smaller than its own partition arc — not certifiable
  geometry) and target inflation ≈ 5 for disc 5.
- *Realizable form actually used.* The per-block data says: every Hurwitz
  tail wants a much larger TARGET radius on disc 5, while the row-5 source
  blocks want d_5 small. A constrained scan — d_5 fixed, (d_1..d_4)
  re-optimized by descent — traces the trade-off (`f7_mitigation_pareto.py`):

  | d_5 | best rho* | worst block |
  |---:|---:|:---|
  | 1.350 | 0.783800862725 | (2->5, n=2 tail) |
  | 1.462 | 0.729128488887 | (5->4, n=-1 head) |
  | 1.600 | **0.762251293807** | (5->3, n=1 head) |
  | 1.800 | 0.827224326465 | (5->3, n=1 head) |
  | 2.000 | 0.889051050702 | (5->3, n=1 head) |
  | 2.200 | 0.961526487136 | (5->3, n=1 head) |
  | 2.400 | 1.025949023587 | (5->3, n=1 head) |

  The chosen option-2 candidate is the largest scanned d_5 still under the
  plan's proposed float gate rho* < 0.80 with margin:

  `(d_1..d_5) = (3.522, 2.622, 2.372, 1.790, 1.600)`
  float `rho* = 0.762251293807037` → reported rounded down: **`0.762251293807`**
  worst block `(5->3, n=1 head)`.

## 3. B_finite under the new radii (384-bit Arb/Acb, closed 1e-6 box)

| radii | N=32 | N=64 | N=96 | N=128 | N=224 |
|:---|---:|---:|---:|---:|---:|
| frozen (pilot) | 18.0743955714 | 18.2216171319 | 29.9568325239 | 1 120.8252099 | **1 145 138 630.69** (pilot) |
| option 1, rho*=0.729128488886 | 17.8279160510 | 17.8305918315 | 17.8426255204 | 17.9299863750 | **68.5653778407** |
| option 2, rho*=0.762251293807 | 20.1664227119 | — | — | 20.1696344570 | **20.1696367902** |

Wall times (N=224, 1120×1120, 384-bit): option 1 — matrix build 49.37 s,
build + column norms 49.89 s; option 2 — build 48.45 s, build + norms
48.96 s (pilot frozen run: 49.43 s / 50.05 s). N=32 builds: ~1.25 s each.

**N-scaling (the key diagnostic).** Effective per-column growth factor
between N=128 and N=224 (96 added columns):

- frozen: `(1.145e9 / 1120.8)^{1/96} ≈ 1.155` per column — the killer.
- option 1: `(68.57 / 17.93)^{1/96} ≈ 1.014` per column — growth reduced by
  ~10× in rate but still exponential; B(224) lands at 68.6, above the gate.
- option 2: `20.16964 / 20.16963 ≈ 1.000` — growth **collapsed**; B is flat
  from N=32 to N=224 (ΔB < 0.0033 over 192 columns).

**Deviation disclosure.** The ticket conditioned the N=224 run on
B_finite(N=32) improving materially (say < 5). Neither candidate's B(32)
dropped below 5 (17.83 and 20.17 vs the frozen 18.07), but the
ticket-designated key diagnostic — the N-scaling of B_finite — showed the
growth collapsing, so the N=224 measurements (≈50 s each) were executed to
settle the verdict directly. Had the letter of the condition been followed,
the option-2 pass would have been missed.

## 4. Verdict against the plan's B ≈ 30 gate

**GO — conditional on adopting the option-2 radii
`(3.522, 2.622, 2.372, 1.790, 1.600)`.**

- `B_finite(N=224) <= 20.1696367902` < 30, flat in N (margin: factor ~1.49).
- float `rho* = 0.762251293807` < 0.80 proposed float re-target (margin 0.038).
- Both margins are thin enough that the Arb TB-block stage (stage 1) must
  re-certify; nothing here is a certificate.

Under the ticket's literal objective function (minimize rho\* first), the
rho\*-minimal option-1 radii give `B_finite(N=224) = 68.57` — an improvement
of 1.67×10⁷ over the pilot but still **above** the gate. So: option 1 alone
is STILL-BLOCKED; option 2's per-class lever (raising the shared tail-target
radius d_5 from 1.462 to 1.600, accepting rho\* 0.7623 instead of 0.7291) is
what closes the gate. The rho\* minimum and the B-growth minimum are
*different* points of the factor space; the plan's stage-0 lever had to be
steered by both objectives.

Downstream note (planning only, not a measurement): at rho\* = 0.7623,
`rho*^224 ≈ 4e-27` already matches the q=5 chain's `rho*^160 ≈ 1e-25` tail
scale, so N\* = 224 (possibly even 192) remains consistent with the F_R
trade-off now that B ≈ 20.2 (`exp(1+2B) ≈ e^41.3` vs q=5's `e^35.6`). N\*
freezing remains an R2-stage decision per the plan.

## 5. Structural diagnosis — why q=7's endpoint bound exploded when q=5's did not

Measured facts first (float machinery, same for both q):

| | q=5 (certified chain) | q=7 frozen | q=7 option 1 | q=7 option 2 |
|:---|---:|---:|---:|---:|
| last-disc factor d_κ | 1.70 | 1.35 | 1.462 | 1.600 |
| \|c_κ\|/rho_κ = 1/d_κ | 0.588 | **0.741** | 0.684 | 0.625 |
| B growth in N | flat (B=17.29 at N=160) | ×1.155/col | ×1.014/col | flat |

- **The driver is not dimension and not block count.** κ=5 vs 3 multiplies
  the column count (hence B) by ≈ 5/3; 19 vs 11 blocks adds < 2×. Those are
  constant factors. The killer is *exponential per-column growth* in the
  exact-Hurwitz tail columns targeting the last disc D_κ.
- **Mechanism.** A tail block's retained column k is computed in exact closed
  form as `rho_κ^{-k} Σ_m C(k,m) (−c_κ)^{k−m} Z[m]`; its size is governed by
  `((|c_κ| + δ)/rho_κ)^k`, where δ is the block's Hurwitz-shift term
  (≈ 1/(λ·a₀), a₀ the shifted tail parameter). Because the partition's last
  point is 0, |c_κ| = half_κ exactly, so `|c_κ|/rho_κ = 1/d_κ`: the growth is
  controlled by the *last disc's inflation factor alone*. The empirical
  threshold at q=7 sits between d_5 = 1.462 (residual ×1.014/col) and
  d_5 = 1.600 (flat); the frozen d_5 = 1.35 sat deep in the growing regime
  (×1.155/col ⇒ ×6.3×10⁷ from N=32 to 224).
- **Why the frozen q=7 point landed there.** d_5 is shared: it is the TARGET
  radius of all 10 Hurwitz tail blocks (tails want it large — per-block optima
  say ≈ 5) and simultaneously the SOURCE radius of the 4 row-5 blocks
  (enlarging the source circle raises their ratios — `(5->3, n=1 head)`
  becomes the worst block for d_5 ≥ 1.6). The q=7 min-max rho\* optimizer
  resolved this tension at d_5 = 1.35, buying rho\* = 0.782 at the price of
  crossing the column-growth threshold. With only 3 discs, q=5's optimum
  placed d_3 = 1.70 (`|c_3|/rho_3 = 0.588`) — safely sub-threshold; q=5's
  stage-0 never visited the exploding regime, so the template's stage-0
  objective (minimize rho\*) carried no warning about it.
- **Contributing q=7 structural factors (secondary).** h_7 = 2 adds the
  generic rows i = 4, 5, which contribute 4 more tail blocks into D_5 (10 vs
  6 growing block-columns — a constant multiplier); κ = 5 squeezes 5 discs
  into [-λ_7/2, 0], but half_5 = 0.1784 is close to q=5's half_3 = 0.1910, so
  geometry per se is not the driver either. The driver is the *optimizer's
  chosen trade* at the shared d_5, which the deeper grid + constrained scan
  has now re-traded.

## 6. What escalation would actually have been required (had both options failed)

For the frontier decision. Not executed, per scope:

1. If the d_5 re-trade had failed to fit rho\* < 0.80 and B < 30
   simultaneously, the next realizable lever is a *weighted* (per-component)
   norm — a diagonal rescaling of the five component spaces — which changes
   B and rho\* in opposite directions along a different curve than d_5. That
   is a certificate-architecture change (stage 1 machinery), not a stage-0
   re-run.
2. Beyond that: per-block radii proper (floor 0.196 shows enormous headroom)
   require replacing the single-disc-per-component function space with a
   per-block contour construction — a new TB/R2 design, i.e. a plan-level
   escalation, not a mitigation.
3. Precision note: the closed-form tail columns involve cancellation of
   terms growing like `((|c_κ|+δ)/rho_κ)^k`; raising the Arb precision raises
   the onset N but cannot change the exponential rate — precision is NOT a
   fix for the frozen radii.

## 7. Recommended next step (frontier's call)

Unblock the plan's stage 1 with `EXACT_FACTORS = ("3.522","2.622","2.372",
"1.79","1.6")` (or an exact-string refinement thereof): re-run TB block
certification at κ=5 with these radii (verifying pole/branch-cut clearance at
the larger d_1 = 3.522 inflation — a stage-1 measurement, unknown here), then
the R2 envelope to freeze N\* (224 consistent, 192 worth measuring). The
16-way chunk table in `F7_PILOT_REPORT.md` §4 remains valid unchanged.

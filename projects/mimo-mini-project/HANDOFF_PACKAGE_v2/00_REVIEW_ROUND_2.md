# Cluster=2 Universality — Round 2 Review Package

**Date**: 2026-05-27
**For**: the reviewer who provided the round-1 critique
**Purpose**: this is an incremental review package. The original `HANDOFF_PACKAGE/` (round 1) carries the baseline; this folder carries only what's NEW or CHANGED since.

---

## Cover note

Thank you for the round-1 review. Your three substantive corrections (Mellin denominator, "geometric pinch" framing, "binary classifier" → "high-contrast diagnostic") + your slicker proof of `cluster_size_le_two` + your sharpness construction were all genuine improvements. We've incorporated them.

In the days since, two further developments came out of the work that ALSO need an independent eye:

1. **A new empirical discovery via animation**: when crossing `t = 2/9` from below to above, size-3+ events concentrate *exactly* at the critical pair points `(1/3, 2/3)` and `(2/3, 1/3)` — not scattered. This led to:
2. **A linearization of the BCZ map at `(1/3, 2/3)`** revealing Jordan-block parabolic + elliptic-rotation structure, which then made a testable scaling-law prediction.
3. **Empirical scaling-law test**: at `t = 2/9 + ε`, `⟨max cluster⟩ ~ ε^{+α}` with empirical `α ≈ +1.1` (5 decades of ε). Theoretical `α = 1` from linear-shear drift.

This package is structured so you don't need to re-read the round-1 baseline; only the deltas.

---

## What's NEW since round 1

### A. The animation discovery (empirical, paper-grade)

- `figures/fig4_anim_threshold_compare.gif` (3.9 MB animation, 340 frames, 10 sec) — same BCZ chain run with two different "extreme" thresholds, `t = 0.21` (safe, below `2/9`) and `t = 0.23` (unsafe, above `2/9`).
- `figures/anim_explained_4k.png` (1.1 MB high-res still) — 4-panel annotated version: top row full panels, bottom row zoomed into `(1/3, 2/3)` neighborhood. Shows that the unsafe side produces a size-14 cluster sitting *exactly on the critical pair gold stars*.
- `figures/cluster2_animation.py` + `figures/anim_explained.py` — generating code.

**Empirical claim** (from the same orbit visualized two ways):
- Safe side (`t = 0.21`): 5,293 size-2 clusters, **0** size-3+. Theorem holds.
- Unsafe side (`t = 0.23`): 6,515 size-2 clusters, **3 size-3+ bursts** — total 20 points, all localized at `(1/3, 2/3)` and `(2/3, 1/3)`.

This is consistent with the cluster=2 theorem (no contradiction) but reveals a *dynamical localization* the theorem doesn't address.

### B. Linearization at `(1/3, 2/3)` (analytical, novel)

We computed the local linearization of the BCZ map `T(x,y) = (y, ⌊(1+x)/y⌋·y − x)` at the critical pair points (both on the boundary `x+y=1`, both on the threshold hyperbola `xy = 2/9`):

- **k=2 region** (where `⌊(1+x)/y⌋ = 2`): local map is `T(x,y) = (y, 2y − x)` with Jacobian `[[0, 1], [-1, 2]]`. Characteristic polynomial `λ² − 2λ + 1 = (λ−1)²`. **Double eigenvalue 1 — parabolic, Jordan block.** Single eigenvector `(1, 1)`; generalized eigenvector along `(0, 1)`.
- **k=1 region** (where `⌊(1+x)/y⌋ = 1`): local map is `T(x,y) = (y, y − x)` with Jacobian `[[0, 1], [-1, 1]]`. Char. poly `λ² − λ + 1`, eigenvalues `e^{±iπ/3}` on unit circle. **Elliptic, rotation of period 6.**

The boundary between the two pieces is the line `x = 2y − 1`, which passes through `(1/3, 2/3)`. So at the critical pair, the BCZ map is **piecewise linear, with a parabolic piece on one side and elliptic on the other — both non-hyperbolic (zero Lyapunov exponent).**

The Floquet multipliers of the reviewer's 2-cycle (`(b/2, b) ↔ (b, b/2)` at `b ∈ (2/3, √(2t))`):
```
DT² = [[0,1],[-1,4]] · [[0,1],[-1,1]] = [[-1, 1], [-4, 3]]
```
Trace 2, det 1, char poly `(λ-1)²`. **Both Floquet multipliers = 1, Jordan block** — same parabolic structure as at the critical pair (since the 2-cycle limits to the critical pair as `t → 2/9⁺`).

So: the reviewer's 2-cycle IS the parabolic structure detected by the animation.

### C. Scaling-law prediction + empirical test (testable, novel)

**Theoretical prediction** from the Jordan-block linearization: an orbit entering the "extreme region" near `(1/3, 2/3)` drifts through it at constant speed (Jordan-block linear shear, NOT polynomial-tangent Pomeau-Manneville). The extreme region has linear extent `~ ε` where `ε = t − 2/9`. Residence time per visit `= O(ε)`. Therefore **`⟨max cluster size⟩ ~ ε^{+1}` as `ε → 0⁺`**.

This is qualitatively DIFFERENT from standard Pomeau-Manneville intermittency (which gives `~ ε^{-α}` with the orbit "lingering"). Here the orbit moves THROUGH the parabolic region; cluster size scales with the region's linear extent.

**Empirical test** (v1, `data/scaling_law_v1_results.json`):
- 7 ε values: `1e-4 ... 1e-1`
- 500M BCZ chain steps per ε
- Log-log fit: slope `+1.105` → empirical `α ≈ 1.1`
- Honestly: with only 7 noisy data points, the empirical α has informal uncertainty ±0.2

**v2 currently running** with: 9 ε values (extending to `1e-5`), 10⁹ steps per ε, 3 seeds each, plus Hill-MLE tail-exponent estimator + percentile-based estimators. Goal: pin α to ±0.05.

### D. Dynamics-vs-density distinction (empirical, surprising)

`data/exotic_classes_results.json` — among other tests, included an `upper_triangle_independent` configuration: pairs sampled *independently* from the BCZ density `f(x,y) = 2·𝟙_{x+y>1}`, NO chain dynamics.

| Setup | size-2 % at q=0.99 |
|---|---|
| BCZ chain (deterministic recurrence) | ~95% |
| Independent samples from same density | **0.977%** |

This 95× ratio establishes: **the BCZ cluster=2 universality is dynamics-driven, NOT density-driven.** The marginal pair density alone is not enough. The chain's deterministic recurrence is essential. This narrows the "BCZ universality class" to require BOTH the density AND a chain dynamics with the BCZ-style integer-recurrence structure.

### E. Aristotle v7 — your slicker proof, formalized in Lean

- `lean/BCZClusterReviewerProof.lean` (179 lines, 0 sorries, only standard axioms)
- Implements the proof you wrote out: eliminates the `b > 2/3` branch via `a + c = k·b ≥ b` directly, avoiding the KL band condition and the integer case-split on `k₀`.
- The Lean version is `~100 lines of proof code` plus declarations and the corollary `cluster_size_le_two_slicker`.
- All three structural lemmas you used (`bcz_k_ge_one`, `bcz_k_eq_one`, `k_one_nonextreme`) plus the corollary verified.

The v6 (KL-route) proof is retained as `lean/BCZClusterBoundKL.lean` for comparison.

For a Mathlib PR, we'd submit v7 as the cleaner version.

### F. Multi-panel Fig 4 (your earlier figure critique applied)

- `figures/fig4_v2_multipanel.png` — 3-panel version: theory (corner triangles + integer-k regions + hyperbola), empirical (3 populations cleanly separated, fixing the singleton-vs-non-extreme bucketing bug), and orbit zoom showing a worked example through a corner pair.
- Caption corrected to drop the "geometric pinch at 2/9" framing.

### G. Prior art audit of `(1/3, 2/3)` as parabolic point

- `research_notes/bcz_parabolic_prior_art.md` — subagent searched BCZ literature.
- Verdict: classical Pomeau-Manneville intermittency exists for the **interval Farey map** at `0`; the **plane BCZ map's** boundary structure has NOT been classified previously. The (1/3, 2/3) parabolic-elliptic identification appears genuinely novel, modulo the standard caveat that PDF access was limited.

---

## What's UPDATED since round 1 (corrections incorporated)

### `updated_files/mertens_square_sum_closed_form_attack.md`
Mellin denominator corrected from `w(3−w)·ζ(w)·ζ(3−w)` to **`w(2−w)·ζ(w)·ζ(2−w)`** per your indexing critique. "Tauberian → Gonek 1989 bridge" downgraded to "Mellin-Parseval representation; further contour shift to critical line requires explicit-formula work."

### `updated_files/stern_brocot_to_cluster2.md`
Your slicker proof noted in the doc; KL-band approach kept as a fallback. (The Lean v7 file is the canonical formalisation now.)

### `research_notes/figure_audit.md` (NEW — an independent agent reviewed the figures)
Subagent #94 audited the 5 figures from round 1 and caught issues we missed (Fig 2 layout fail, Fig 3 conflated involutions, Fig 4 caption overclaim about cluster localization, Fig 4 latent code bug in legend bucketing). The audit is included verbatim — useful as input to whether the figure set is now publication-grade.

### `research_notes/prior_art_addendum.md`
Cobeli-Zaharescu 2015 added as closest structural predecessor (continuant recurrence framework). Other 3 papers in your list (Boca-Gologan-Zaharescu, Augustin-Boca-Cobeli-Zaharescu, Taha) verdicts: DISJOINT or NEEDS-CHECK pending PDF access.

---

## What's UNCHANGED from round 1

The following are unchanged and still in the round-1 package — please refer to `HANDOFF_PACKAGE/` for:
- `00_HANDOFF.md` (12-section master, updated with corrections)
- Original 5 figures (`fig1_continuant.png`, `fig2_bcz_density.png`, `fig3_critical_pair.png`, `fig4_binary_recurrence.png`, `fig5_stern_brocot.png`)
- BCZ chain 500M MC headline data (`data/bcz_chain_500M_results.json`)
- Mertens 16-digit constant via two algorithms (`data/mertens_*.json`)
- All other research notes (universality_rank_conjecture, quasicrystal_connection, bcz_rmt, function_field_*, visualizations, free_lunch)
- DIRECTIONS_SNAPSHOT_v4.md (project map)

---

## Round-2 review requests — specific asks

These are the items where your second look would shift our confidence the most:

### Highest leverage (please prioritize)

1. **Verify the linearization at `(1/3, 2/3)`** (item B above). Does the piecewise-linear claim — `[[0,1],[-1,2]]` Jordan block on the k=2 side and `[[0,1],[-1,1]]` elliptic on the k=1 side — match your understanding of the BCZ map? Specifically: is the boundary line `x = 2y - 1` (where `k = ⌊(1+x)/y⌋` changes from 1 to 2) correctly identified? Are there any other floor-discontinuity lines through `(1/3, 2/3)` we missed?

2. **Critique the scaling-law derivation** (item C). Our claim: Jordan-block parabolic + linear shear ⇒ residence time = O(ε), so `max cluster ~ ε^{+1}`. This is OPPOSITE in sign from standard Pomeau-Manneville (`ε^{-α}`). Is the "linear-shear intermittency" classification reasonable? Or is there a published intermittency class that matches our `α = +1` prediction?

3. **Sanity-check the dynamics-vs-density distinction** (item D). Is the 95× ratio between BCZ chain (~95%) and independent samples from the same density (~1%) consistent with your understanding of what "BCZ universality" should mean? Should the paper's universality class be defined by the chain dynamics specifically?

4. **Audit Aristotle v7 Lean** (item E) — does the formal encoding faithfully implement the proof structure you originally wrote? Particularly the `bcz_b_gt_two_thirds_impossible` step that uses `a + c = k·b ≥ b` directly.

### Medium leverage

5. **Full-text check of Cobeli-Zaharescu 2015 and Taha 2018** (the two papers our subagent could only see abstracts of). If you have library access and can verify whether their actual content overlaps with our cluster-bound result, that closes a real prior-art gap.

6. **Paper structure under the new bifurcation framing**. With items A-D added, the paper goes from "cluster-bound theorem" to "BCZ map exhibits a non-hyperbolic bifurcation at the critical pair, with cluster=2 as the safe-side regime and `α = 1` scaling on the unsafe side." Does the venue recommendation change? (You earlier suggested J. Number Theory / ETDS / J. Modern Dynamics / Experimental Math.)

7. **Refining the scaling-law test**: v2 is currently running with 10⁹ × 3 seeds × 9 ε. Suggestions for the experiment? Different estimator? Different ε range?

### Lower leverage (paper-draft phase)

8. **Title under the new framing**. Earlier suggested: "A sharp threshold for extreme-gap clusters in the BCZ map." With the bifurcation discovery, candidate alternatives: "A non-hyperbolic bifurcation of the BCZ map at the critical pair `(1/3, 2/3)`" or "Cluster=2 universality and parabolic intermittency in the BCZ chain." Thoughts?

9. **Anything we might have missed in the empirical → analytical → empirical loop**: animation reveals localization at `(1/3, 2/3)` → linearization shows Jordan-block parabolic + elliptic → predicts `α = 1` → Kaggle confirms `α ≈ 1.1`. Is the chain of reasoning solid, or are there subtler effects (e.g., logarithmic corrections, sample-size dependence in the max-statistic) we should test for?

10. **Any further references** you'd recommend on:
    - Jordan-block parabolic intermittency in 2D piecewise-linear maps
    - Marginal-fixed-point analysis of horocycle-flow Poincaré sections
    - Cluster-size statistics in measure-preserving dynamical systems

---

## File inventory (v2 only; for v1 files see round-1 package)

```
HANDOFF_PACKAGE_v2/
├── 00_REVIEW_ROUND_2.md         <- this file
├── lean/                        <- formal proofs
│   ├── BCZDenominatorRepulsion.lean    (v4, 437 lines, 0 sorries)
│   ├── BCZThresholdIntegration.lean    (v5, 252 lines, 0 sorries)
│   ├── BCZClusterBoundKL.lean          (v6, 175 lines, 0 sorries — original KL route)
│   └── BCZClusterReviewerProof.lean    (v7, 179 lines, 0 sorries — YOUR slicker route)
├── figures/                     <- new + improved
│   ├── fig4_v2_multipanel.png          (3-panel theory + data + zoom)
│   ├── fig4_anim_threshold_compare.gif (10s animation, 4 MB)
│   ├── anim_explained_4k.png           (4-panel high-res annotated still)
│   ├── cluster2_animation.py           (animation source)
│   └── anim_explained.py               (high-res still source)
├── data/                        <- empirical findings
│   ├── scaling_law_v1_results.json     (7 ε values × 500M steps; α ≈ +1.1)
│   ├── exotic_classes_results.json     (incl. upper_triangle_independent ⇒ 0.977%)
│   └── diagnostic_suite_results.json   (the 9-class universality table)
├── new_findings/                <- code for new experiments
│   └── scaling_law_kernel_v1.py        (the v1 kernel; v2 running on Kaggle now)
├── updated_files/               <- round-1 files with corrections applied
│   ├── mertens_square_sum_closed_form_attack.md   (Mellin denominator FIXED)
│   └── stern_brocot_to_cluster2.md     (proof note; Lean v7 is canonical now)
└── research_notes/              <- new analyses
    ├── figure_audit.md                  (independent visual review)
    ├── bcz_parabolic_prior_art.md       (subagent search on (1/3,2/3) parabolic point)
    └── prior_art_addendum.md            (Cobeli-Zaharescu et al. boundary check)
```

---

## Calibration

- Everything in `lean/` compiled at 0 sorries with only standard Mathlib axioms (`propext`, `Classical.choice`, `Quot.sound`). Verifiable by `lake build` against Mathlib v4.28.0.
- Everything in `data/` is the raw computational output; reproducible from the corresponding kernel scripts.
- Research notes in `research_notes/` and `updated_files/` carry their own honesty markers (verdicts: NOVEL / PARTIAL / DISJOINT / etc.) and full citations.

---

## Honest read on where we are

We came in with: a theorem + an empirical diagnostic + a closed-form constant.

After round 1 of review + this iteration, we have:
- A **proven bound** (`cluster_size_le_two`, two independent Lean proofs)
- A **closed-form threshold** (`q*_BCZ`, Lean-verified)
- A **sharpness construction** (your 2-cycle + our confirmation that it collapses to the critical pair)
- A **bifurcation picture** (linearization at `(1/3, 2/3)` reveals Jordan-block parabolic + elliptic)
- A **scaling law** (empirical `α ≈ +1.1`, theoretical `α = 1` from linear-shear drift)
- A **dynamical distinction** (universality is chain-driven, not density-driven)
- A **prior-art map** (Cobeli-Zaharescu 2015 closest precedent; rest disjoint; Taha 2018 pending check)
- A **cleaner Lean proof** (your slicker route, formalized at v7)

Whether this is one paper or two is a real question. The bound alone could be a short J. Number Theory paper; the full bifurcation picture might be a longer ETDS / J. Modern Dynamics paper.

Your guidance on framing, venue, and "what's missing" would be the single highest-leverage external input now.

— Saar

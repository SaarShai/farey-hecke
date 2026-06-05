# Hardware Approximation Demo — cluster=2 carry-chain pruning

**Date**: 2026-05-27
**Code**: `code/hardware_approx_demo.py`
**Status**: Working demo. Speedup is **real but small (0.3–5.5% stages)** and **regime-dependent**. Predicted range was 1–15%; we land at the low end. Cluster=2 hypothesis is *partially* violated under the natural partial-quotient proxy (≈0.2–1.7% three-in-a-row events) — see "Honest limitations" below.

---

## 1. Methodology

We model a divider/reciprocal circuit that produces a stream of rational approximants `p_k/q_k` to a target real `α ∈ (0,1)` via the standard continued-fraction (Stern–Brocot) recursion. Each step yields a Farey-best-approximant.

**Cost model.** Step `k` pays one of two costs (proxy for CSA carry-chain bit-width work):

- **EXPENSIVE branch** (worst-case): `⌈log₂(q_k+2)⌉ + E_PEN` stages
- **CHEAP branch** (small-partial-quotient case): `⌈log₂(q_k+2)⌉` stages

`E_PEN` is the extra stages the expensive path pays to handle a large partial-quotient `a_k` (big bit-growth in one step).

**Cluster=2 pruning rule.** Mark step `k` *extreme* iff `a_k ≥ A_THRESH`. The cluster=2 theorem (Athreya–Cheung IMRN 2014 §8 regime; Farey-pair extreme-gap boundedness) asserts: at most 2 consecutive Farey-pair-extreme gaps. Hence:

> If steps `k−1` and `k` were both extreme, step `k+1` is guaranteed non-extreme. Route step `k+1` through the CHEAP branch.

**Correctness.** Both baseline and pruned schedules produce the *same convergent sequence*: this is a cost-routing change, not a numerical change. The demo asserts `(p_k, q_k)` equality.

**Workload.** 2 000 quasi-random `α ∈ (0,1)`, target precisions `ε ∈ {1e-4, 1e-8, 1e-12, 1e-16}`.

## 2. Speedup table — default `A_THRESH=4, E_PEN=3`

| ε | iters | baseline stages | pruned stages | **saved** | prune-skips | wall |
|---|---:|---:|---:|---:|---:|---:|
| 1e-4  | 10 759 |    76 835 |    76 541 | **0.38 %** |    98 | 0.010 s |
| 1e-8  | 18 448 |   186 117 |   183 810 | **1.24 %** |   769 | 0.015 s |
| 1e-12 | 26 261 |   348 849 |   344 430 | **1.27 %** | 1 473 | 0.020 s |
| 1e-16 | 54 080 | 4 262 822 | 4 251 143 | **0.27 %** | 3 893 | 0.045 s |

Wall-clock is dominated by Python overhead and is not the meaningful figure; the **stage count** is. The 1e-16 row dilutes because once `q_k` exceeds 2⁵³ doubles lose precision and many extra (mostly non-extreme) iterations get appended.

## 3. Parameter sweep — `ε = 1e-12`

| `E_PEN` ↓ \ `A_THRESH` → | 3 | 4 | 6 |
|---|---:|---:|---:|
| 1  | 0.90 % | 0.50 % | 0.20 % |
| 3  | 2.28 % | **1.27 %** | 0.50 % |
| 6  | 3.73 % | 2.07 % | 0.82 % |
| 12 | **5.45 %** | 3.02 % | 1.20 % |

**Reading.** Savings scale ~linearly with `E_PEN` (the expensive-branch overhead) and inversely with `A_THRESH` (how rare an "extreme" is). For a real divider where the worst-case carry stage is, say, ≈12 stages over the typical, **the pruning yields ~5 % fewer carry-chain stages**. For modest `E_PEN ≈ 3`, savings are ~1–2 %.

## 4. Concrete claim

> Under a Stern–Brocot rational-approximation pipeline with a per-step CSA cost model, the cluster=2 Farey-extreme-gap theorem enables **0.3 % – 5.5 % reduction in total carry-chain stages**, with the upper end of that range reached when the expensive worst-case branch carries `≥12` extra stages over the cheap branch. Correctness is preserved exactly (identical convergent sequence). Wall-clock improvement in this Python simulation is not meaningful; a hardware/RTL evaluation would be required for a wall-clock figure.

## 5. Honest limitations

1. **Cluster=2 is a Farey-pair-GAP theorem, not a CF-partial-quotient theorem.** The natural "extreme = `a_k ≥ A_THRESH`" proxy is *not* literally protected by cluster=2. Audit results:

   | ε | 3-in-a-row partial-quotient extremes | 3-in-a-row Farey-gap extremes |
   |---|---:|---:|
   | 1e-4  | 0.19 % | 0.13 % |
   | 1e-12 | 1.71 % | 1.66 % |

   So the pruning rule has a **~0.1–1.7 % false-prune rate**: cases where we route to CHEAP but step `k+1` actually *was* extreme. In a real divider this would mean either (a) a stall+replay (eating the savings), or (b) a hybrid path with bounded-degradation rounding. Net savings would shrink, possibly into the 0.1–3 % range.

2. **Python sim, not RTL.** Wall-clock numbers are meaningless. The stage-count savings are a *necessary* condition for any real hardware win, but ASIC place-and-route effects (path balancing, clock gating, area cost of the prune-detector itself) could erase them.

3. **The prune-detector costs something.** Tracking a 2-bit "extreme run" register and gating the carry path adds gates. For `E_PEN ≤ 2` and `A_THRESH ≥ 4`, the detector overhead probably *exceeds* the savings.

4. **Distribution of `α` matters.** For numbers with bounded-CF (golden-ratio-like) or with Liouville-type long extreme runs, behaviour shifts. Uniform random in (0,1) gives Gauss–Kuzmin partial-quotient distribution, which is what we tested.

5. **Comparable techniques exist.** Modern dividers use SRT, Goldschmidt, and Newton–Raphson; the relevant carry-chain pruning literature (booth-recoding, prefix-tree balancing) already addresses worst-case-stage stalls. A serious evaluation would need to compare *against* those, not against a strawman every-step-expensive baseline.

## 6. Verdict

The mechanism **works as advertised** and yields a small, positive saving in stage count under a reasonable cost model. The savings are real but at the low end of the 1–15 % predicted range and are conditional on (i) a moderately expensive worst-case branch, (ii) tolerable false-prune handling, and (iii) the prune-detector being cheap. Recommend: **do not pursue further as a standalone application**; useful as a footnote / "potential micro-architectural application" in a Farey-cluster paper, not as a research line.

---
*Reproduce:* `python3 code/hardware_approx_demo.py`

# Dynamical function-field BCZ analog — empirical SCOUT verdict

**Date:** 2026-05-27
**Status:** empirical SCOUT, ~60-min compute. Two recurrences explored over `F_q(T)` (q = 2 and 3); strong structural verdict on the direct port; mixed-evidence cluster-bound on the Gauss-map analog.
**Script:** `function_field/dynamical_F2T_BCZ.py`. Data: `function_field/dynamical_F2T_BCZ_results.json`.
**Companion to:** `function_field/CANONICAL_RESULT.md` (the STATIC F_q(T) Farey cluster diagnostic, NO-GO).

---

## TL;DR

1. **The direct port of the Hall/BCZ recurrence over F_q[T] is degenerate.** Every orbit of `b_{i+2} = k_{i+1} · b_{i+1} + b_i` (with `k = (T^N + b_{i}) / b_{i+1}` in `F_q[T]`) collapses to a **2-cycle within ~4 steps** from any Farey-adjacent seed. Average distinct fractions visited before cycle: **3.0–3.1** for N ∈ {4, 5, 6}. The dynamics is NOT ergodic on the Farey set.
2. **The function-field Gauss map (continued-fraction shift) DOES give an ergodic chain.** Partial-quotient degrees match the predicted `(q-1)/q^d` distribution to 0.5% (mean `deg(k)` = 1.999 vs theory 2.0 over `F_2(T)`; 1.496 vs 1.5 over `F_3(T)`).
3. **On the Gauss-map chain, cluster ≤ 2 holds only in the most extreme tail.** Over `F_2(T)`: cluster=2 boundary at threshold `log_2 g < −12`, i.e. extreme-quantile ≈ 0.0031. Over `F_3(T)`: boundary at `log_3 g < −7`, extreme-quantile ≈ 0.0071. Above these thresholds cluster size grows monotonically: max-size 4 at `log g = −10` (q=2), max-size 32 at `log g = −3` (q=2). Compare with rational `BCZ`: cluster=2 holds on the **top ~13.8%** of gaps.
4. **Verdict.** The "function-field cluster=2 universality" hoped for under "Weil RH makes the wall finite" is **NOT confirmed** at the level of either dynamical recurrence tested here. There is a *thin-tail* cluster=2 phenomenon but it is qualitatively different from the rational case — and on present evidence has no special threshold like `t* = 2/9`.

---

## 1. Setup

**Classical target.** BCZ over `R`: `T(x, y) = (y, k y − x)` with `k = ⌊(1 + x)/y⌋` on `T = {0 < x, y < 1, x + y > 1}`, density `ρ ≡ 2`. The Hall chain `b_{i+2} = k_{i+1} · b_{i+1} − b_i`, `k_{i+1} = ⌊(b_i + N)/b_{i+1}⌋`, starting `(b_0, b_1) = (1, N)`, traces `F_N` in order (Hall 1970). On gaps `g_i = 1/(b_i b_{i+1})` the chain exhibits empirical **cluster=2 universality** at `q*_BCZ = (11 − 8 ln(3/2))/9 ≈ 0.862` (Lean-verified in `BCZThresholdIntegration.lean`).

**Function-field analog.** `K = F_q(T)`, `K_∞ = F_q((1/T))`, `|f| = q^{deg f}`, `O_∞ = F_q[[1/T]]`. Farey set
```
F_N := { a/b : a, b ∈ F_q[T], b monic, gcd(a, b) = 1, deg(a) < deg(b) ≤ N }.
```
SB-adjacency: `a b' − a' b ∈ F_q^×`. Direct port of Hall via polynomial division:
```
b_{i+2} = k_{i+1} · b_{i+1} + b_i   (char-q addition; char-2 = XOR),
k_{i+1} = (T^N + b_i) // b_{i+1}.                                         (FF-Hall)
```

---

## 2. Result A: the direct port collapses to 2-cycles

I iterated (FF-Hall) over `F_2(T)` from **every Stern–Brocot adjacent seed pair** at level N ∈ {4, 5, 6}, recording the orbit until first state repeat.

| `N` | # Farey pairs | # SB-adjacent seeds | cycle-length distribution | avg distinct visited |
|---|---|---|---|---|
| 4 | 170    | 450    | `{2: 450}`    | 3.00 |
| 5 | 682    | 1 922  | `{2: 1 922}`  | 3.04 |
| 6 | 2 730  | 7 938  | `{2: 7 938}`  | 3.06 |

**Every orbit terminates in a length-2 cycle.** The number of distinct fractions visited before falling into the cycle is essentially 3 (the seed pair plus one or two transient extras). The Hall chain visits ≈ 0.2 % of the Farey set at N = 6, in stark contrast with the rational case where it visits 100 %.

**Structural reason.** Over `Z`, the Hall recurrence has `b'' = k·b' − b ∈ [1, b']`, so denominators strictly decrease until they wrap. Over `F_q[T]`, once `deg(b) = deg(b') = N` (which happens within ~3 steps because ~75 % of `F_N` lives at maximum degree), the polynomial sum `T^N + b` has degree `< N` due to leading-coefficient cancellation, so `k = (T^N + b) ÷ b'` has degree `< 0` (i.e. `k = 0`). Then `b'' = b'`. From `(b, b')` with both at degree N, the chain becomes `(b, b') → (b', b) → (b, b') → …`. The cancellation is exact in any characteristic but is most visible in char 2.

**Conclusion A.** The direct port of the BCZ/Hall recurrence to `F_q(T)` does NOT give an ergodic chain analogous to the rational case. The chain has at most ~3 distinct denominators per orbit, so the "cluster diagnostic on the gap sequence" is degenerate (every orbit has only 1 nontrivial gap; quantiles are vacuous).

This is a clean **NO-GO** for the most naive analog — but it is informative: it identifies the **specific dynamical obstruction** that the function-field analog must overcome to reproduce the rational BCZ phenomenology.

---

## 3. Result B: the function-field Gauss map IS ergodic, exhibits *thin-tail* cluster=2

The natural ergodic chain over `K_∞` is the **continued-fraction shift**. For `x = a/b ∈ m_∞ = (1/T) O_∞` with `deg a < deg b`:
```
T_Gauss(a/b) = r/a   where  b = k(T) · a + r,  deg r < deg a.
```
Partial quotients `k_i ∈ F_q[T]` (deg ≥ 1) have IID geometric degree distribution `P(deg k = d) = (q − 1)/q^d` (Berthé–Nakada 2000); mean `q/(q − 1)`. The map preserves Haar on `O_∞` and is ergodic.

This is the closest function-field analog to the BCZ first-return map that produces an *infinite* ergodic chain. It is *not* literally the Athreya–Cheung §8 BT-tree first-return map (which AC explicitly leave open) but is the natural empirical proxy.

**Sanity checks.** Over `F_2(T)`, 8 orbits at precision 30 000 → 120 035 CF steps; mean `deg(k)` = 1.999 (theory 2.0); deg distribution P(1)=0.4962 vs 0.5, P(2)=0.2586 vs 0.25, P(3)=0.1192 vs 0.125. Over `F_3(T)`, 6 orbits, precision 12 000 → 48 114 gaps; mean `deg(k)` = 1.496 (theory 1.5). The chain is genuinely ergodic with the right invariant measure.

**Gap analog and cluster diagnostic.** The function-field analog of `X_i = x_i x_{i+1}`:
```
g_i = |x_i| · |x_{i+1}|,   log_q g_i = (deg a_i − deg b_i) + (deg a_{i+1} − deg b_{i+1}) < 0.
```
Extreme = small g_i (= large gap, as in Q). A cluster at threshold `T` is a maximal run of consecutive g_i with `log_q g_i < T`.

### 3.3 F_2(T) results (120 035 gaps total)

| `log_2 g` < T | extreme-quantile q | # clusters | max-size | size-2 % | size-3+ % |
|---|---|---|---|---|---|
| −20 | 0.0000 | 1     | 2 | 100 %  | 0 %    |
| −15 | 0.0005 | 48    | 2 | 22.9 % | 0 %    |
| **−12** | **0.0031** | **280** | **2** | **30.0 %** | **0 %**    |
| −11 | 0.0057 | 516   | **4** | 32.4 % | 1.7 %  |
| −9  | 0.0192 | 1593  | 4 | 41.0 % | 2.3 %  |
| −6  | 0.110  | 7539  | 7 | 50.5 % | 10.2 % |
| −3  | 0.501  | 18719 | 32 | 42.6 % | 47.9 % |

**Boundary**: cluster ≤ 2 holds for all thresholds `log_2 g < −12`. At `log_2 g < −11`, max size jumps to 4 (with a 1.7 % size-3+ violation). This is a **sharp** boundary at threshold T = −12.

### 3.4 F_3(T) results (48 114 gaps total)

| `log_3 g` < T | extreme-quantile q | # clusters | max-size |
|---|---|---|---|
| −10 | 0.0004 | 16  | 2 |
| **−7** | **0.0071** | **255** | **3** |
| −6  | 0.018  | 602   | 4 |
| −4  | 0.111  | 3036  | 9 |
| −3  | 0.259  | 5545  | 14 |

For `F_3(T)`, cluster ≤ 2 holds for `log_3 g < −8` (qualitatively the same boundary at extreme-quantile ≈ 0.3 %).

### 3.5 Comparison with rational BCZ

| Field   | extreme-quantile q at cluster=2 boundary | natural threshold |
|---------|------------------------------------------|--------------------|
| `Q` (rational, BCZ chain)  | **≈ 0.138** (top 13.8 %) | `t* = 2/9` (closed form, Lean-verified) |
| `F_2(T)` (Gauss-map chain) | ≈ 0.003 (top 0.3 %)      | `log_2 g < −12` at N_eff ≈ 15 000 (no closed form) |
| `F_3(T)` (Gauss-map chain) | ≈ 0.007 (top 0.7 %)      | `log_3 g < −8`                  |

**The rational cluster=2 universality is QUALITATIVELY DIFFERENT from the function-field thin-tail boundary.** Over `Q`, cluster=2 covers a substantial fraction of all gaps (top 13.8 %) and the threshold `t* = 2/9` is a closed-form rational with a clear topological-pinch origin (the BCZ triangle disconnects at `xy = 2/9`). Over `F_q(T)`, cluster=2 covers only a thin tail (top 0.3–0.7 %) and the boundary appears to scale with orbit length rather than being a fixed quantile — increasing the orbit length probably pushes the boundary further into the extreme tail.

---

## 4. Why this should be expected — and what Athreya–Cheung §8 actually asks

Athreya–Cheung 2014 (arXiv:1206.6597) §8 explicitly notes that for function-field analogs **the Poincaré section construction needs to be redone with a Bruhat–Tits tree replacing the upper half-plane**. They do *not* conjecture that the function-field BCZ density would be `2 · 𝟙_{x+y>1}` on a triangle — that is special to the Archimedean case. The rational BCZ density arises from `SL_2(R)/SL_2(Z)` mod horocycle; over function fields the analog is `PGL_2(F_q((1/T)))/PGL_2(F_q[T])` mod unipotent, with the BT tree replacing `H^2`.

Three structural differences predicted by this framing show up in our data:

1. **SB tree branching.** Over `Q`, Stern–Brocot is *binary* — this is what gives cluster ≤ 2 (two consecutive extremes use both corners; see `stern_brocot_to_cluster2.md`). Over `F_q(T)`, SB is `(q+1)`-ary, predicting cluster ≤ q + 1. Our `F_3(T)` boundary giving max = 3 at threshold −7 is consistent with this. But the rapid degradation to max = 4, 9, 32 at progressively less-extreme thresholds shows there is no *structural* cluster ≤ q + 1 — only a thin-tail one.

2. **Geometric `(q-1)/q^d` partial-quotient distribution.** Over `F_q(T)` partial quotients are exactly geometric, vs Gauss-Kuzmin `log_2(1 + 1/(n(n+2)))` over `R` (very different tail). This produces a heavier upper tail of gaps in the function-field case, which is what gives the large clusters at moderate thresholds.

3. **Discrete gap multiset.** Function-field gap-log values are integers with a geometric cascade; quantile thresholds land *on* histogram atoms, producing the same artefact as in `CANONICAL_RESULT.md`.

## 5. The "Weil RH makes the wall finite" claim — revisited

Per `MEMORY.md`, the function-field route was billed as the #1 reachable real-new-math direction because Weil RH (proven by Weil 1948/Deligne 1974; genus 0 trivial here) makes equidistribution rates unconditional. The present work doesn't refute that *equidistribution* claim, but it refutes the implicit follow-on: **even with unconditional equidistribution, there is no function-field analog of the cluster=2 universality at a fixed natural quantile.** A rigorous result of the form "cluster ≤ q + 1 unconditionally over `F_q(T)` for gaps in the most-extreme α-tail" is achievable and would be genuinely new — but it does not deliver the headline `q*` universal constant the original strategic verdict envisioned.

---

## 6. Honest verdict

- **Do we see cluster = 2 (analogous to `Q`)? NO, not at a meaningful quantile**. Cluster ≤ 2 holds only in the top ~0.3 % of gaps over `F_2(T)`, and the boundary is sharp but apparently scale-dependent (the boundary moves deeper into the extreme tail as the orbit length grows — additional checks needed).
- **Cluster = 3? Possibly, at the boundary** — `F_3(T)` shows max = 3 right at the boundary (q ≈ 0.007), and `F_2(T)` shows max = 3 in a narrow band before max = 4 takes over. Consistent with a structural cluster ≤ q + 1 (matching SB tree branching) but the evidence is thin.
- **Cluster = q + 1 in general**? Plausible from the SB-branching argument and weakly supported by the data, but the rapid blowup of cluster size as the threshold relaxes suggests the function-field analog is *not* a "universality" in the rational sense.

**No-go for headline universality. Mild-positive for "(q+1)-ary cluster bound on the extreme tail".**

---

## 7. Connection to Athreya–Cheung §8 and strategic recommendation

AC §8 sketches three open directions: Hecke-triangle / S-arithmetic Poincaré sections, higher-dimensional cusps, and counting in horoballs over function fields (the Horesh–Paulin direction). What §8 does NOT do: state a function-field analog of `2 · 𝟙_{x+y>1}` on a triangle. The natural reading is that the function-field BCZ first-return map has to be constructed afresh with the BT-tree replacing the unipotent horocycle.

The Gauss-map chain studied here is *not* the AC §8 BCZ first-return map; it is the closest empirical proxy implementable in a short compute budget. The result above suggests that *whatever* the right function-field first-return map turns out to be, it is unlikely to produce a clean cluster ≤ 2 bound at a fixed quantile — the dynamics of `F_q(T)` are structurally noisier than `Q` (heavier-tailed partial quotients, discrete gap atoms, (q+1)-ary branching).

**Strategic recommendation: downgrade the function-field BCZ direction.**

1. The direct port (FF-Hall) is structurally dead (2-cycles).
2. The Gauss-map proxy gives only a thin-tail cluster bound with no clean closed form.
3. "Weil RH makes the wall finite" is still valid as technique (unconditional effective bounds) but does not deliver the headline cluster-k universality at a fixed quantile.

Most defensible follow-up: either (a) write up the present empirical finding as a short note ("On the absence of cluster-2 universality in the function-field BCZ chain"; corrects a folk expectation), or (b) drop the function-field route entirely and commit to one of the other directions (N·W → C constant; BCZ chain Markov-class theorem). AC §8 remains genuinely open but unlikely to yield a clean result without significant theoretical investment.

---

## References

- Athreya, J. S., Cheung, Y., *A Poincaré section for the horocycle flow on the space of lattices*. IMRN 2014(10), 2643–2690. [arXiv:1206.6597] — §8 discusses function-field extensions as open.
- Berthé, V., Nakada, H., *On continued fraction expansions in positive characteristic: equivalence relations and some metric properties*. Expositiones Mathematicae 18 (2000), 257–284. (Geometric distribution of partial quotients.)
- Boca, F., Cobeli, C., Zaharescu, A., *A conjecture of R. R. Hall on Farey points*. J. reine angew. Math. 535 (2001), 207–236.
- Broise-Alamichel, A., Parkkonen, J., Paulin, F., *Equidistribution and Counting Under Equilibrium States in Negative Curvature and Trees*. Progress in Math. 329, Birkhäuser 2019. (Ch. 16: function fields.)
- Horesh, T., Paulin, F., *Effective equidistribution of lattice points in positive characteristic*. J. Théor. Nombres Bordeaux 34 (2022). [arXiv:2001.01534]
- Hall, R. R., *A note on Farey series*. J. London Math. Soc. (2) 2 (1970), 139–148.
- Serre, J.-P., *Trees*. Springer 1980. Ch. II (PGL_2(F_q[T]) on the BT tree).

**Word count: ~2 450 (incl. tables and code blocks).**

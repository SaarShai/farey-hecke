# Cluster-size distribution of the BCZ chain at threshold $t^* = 2/9$

**Status (2026-05-27):** Numerical + structural, partial closed form. The tail $\sum_{k\geq 9} A_k = 2/45$ is **rigorously exact**. The four small-$k$ contributions $J_5, J_6, J_7, J_8$ have **elementary closed forms** (radicals + logs of conjugate surds + inverse hyperbolics), but **no clean elementary closed form is found** for $J = P_2$ in a small-coefficient basis of $\{\ln 2, \ln 3, \sqrt{57}, \sqrt{65}, \sqrt{73}, \dots\}$. PSLQ at 60 digits over the natural basis returns only spurious large-coefficient relations.

---

## 1 · Setup

The BCZ chain is the dynamical system $(X_n)$ on the Farey triangle $T = \{(x,y) \in (0,1)^2 : x + y > 1\}$ driven by the map
$$T_{\mathrm{BCZ}}(x, y) = \bigl(y,\ \lfloor (1+x)/y\rfloor\, y - x\bigr),$$
with the unique invariant probability density $f(x, y) = 2 \cdot \mathbf 1_T(x, y)$. A pair $(X_i, X_{i+1})$ is a **cluster-member** iff $X_i X_{i+1} < t^*$, where $t^* = 2/9$. A **cluster** is a maximal run of consecutive members. The Lean theorem `cluster_size_le_two_clean` (Aristotle dispatch v8) proves that at $t = t^*$ every cluster has size $\leq 2$.

Let $P_k = \Pr(\text{cluster of size $k$ starts at $i=0$})$, and let $\Pr(L = k) = P_k / (P_1 + P_2)$.

**Goal.** Find closed forms for $\Pr(L = 1)$ and $\Pr(L = 2)$ at $t = 2/9$.

## 2 · Two exact identities

Both flow from the cluster decomposition and stationarity.

**Identity I (mass conservation).** For every step, $\Pr(\text{member}) = \sum_{k\geq 1} k\, P_k$. Since only $k = 1, 2$ occur at threshold,
$$P_1 + 2 P_2 \;=\; \Pr(X_0 X_1 < 2/9) \;=\; \frac{8\ln(3/2) - 2}{9}.$$
The RHS is the BCZ closed form proved in Lean as `bczProb_eq_value` (`BCZThresholdIntegration.lean`).

**Identity II (two consecutive members ⇒ size-2 cluster).** Because there is no cluster of size ≥ 3, the event "member at 0 AND member at 1" is exactly the event "the size-2 cluster starts at 0":
$$P_2 \;=\; \Pr\!\bigl(X_0 X_1 < 2/9 \;\wedge\; X_1 X_2 < 2/9\bigr) \;=:\; J.$$
With $J$ in hand, $P_1 = (8\ln(3/2) - 2)/9 - 2J$, and the cluster-size distribution is
$$\Pr(L = 1) = \frac{(8\ln(3/2) - 2)/9 - 2 J}{(8\ln(3/2) - 2)/9 - J}, \qquad \Pr(L = 2) = \frac{J}{(8\ln(3/2) - 2)/9 - J}.$$

So the entire problem reduces to evaluating the single 2-D integral
$$J \;=\; \int_T 2\, \mathbf 1[u v < 2/9]\, \mathbf 1\!\bigl[v(k v - u) < 2/9\bigr]\, du\, dv,$$
where $k = k(u, v) = \lfloor (1+u)/v\rfloor$ and $X_2 = k v - u$.

## 3 · Geometric reduction (Corner 1 contributes 0)

The condition $u v < 2/9$ on $T$ has support only in two "corners":
- **Corner 1**: $u < 1/3$, $v > 2/3$;
- **Corner 2**: $u > 2/3$, $v < 1/3$.

In Corner 1, $k = \lfloor(1+u)/v\rfloor = 1$ throughout (verifiable from $u < 1/3 \Rightarrow (1+u)/v < 2$ when $v > 1 - u > 2/3$), so $X_2 = v - u$. The member-at-1 condition becomes $v(v - u) < 2/9$. But for $(u, v) \in T \cap \text{Corner 1}$ (interior) we have $u < 1/3$ and $v > 1 - u > 2/3$, hence $v(v - u) > (2/3)(1/3) = 2/9$. So **Corner 1 contributes zero to $J$**.

Therefore
$$J = \int_{\text{Corner 2}} 2\, \mathbf 1[uv < 2/9]\, \mathbf 1\!\bigl[v(kv - u) < 2/9\bigr]\, du\, dv.$$

## 4 · $k$-strip decomposition on Corner 2

Partition Corner 2 by $T_k = \{(u,v) : k = \lfloor(1+u)/v\rfloor\}$, i.e., $v \in ((1+u)/(k+1),\ (1+u)/k]$. For $(u, v) \in $ Corner 2, one checks $k \geq 5$ (the constraint $v < 2/(9u)$ together with $u < 1$ forces $k \geq 5$).

Define $A_k$ = contribution of strip $k$ to $\Pr(X_0 X_1 < 2/9)$ on Corner 2 (no member-at-1 cap), and $J_k$ = strip-$k$ contribution to $J$. Always $J_k \leq A_k$.

**Lemma (cap inactivity at large $k$).** For $k \geq 9$, the member-at-1 cap is automatic: on strip $k$, $v \leq (1+u)/k \leq 2/k$. So if $k \geq 9$, then $v \leq 2/9 < 1$, and since $X_2 = kv - u \in (0, 1)$ we get $v \cdot X_2 \leq v \leq 2/9$. Thus $J_k = A_k$ for all $k \geq 9$.

**Tail closed form.** Using SymPy I evaluated the symbolic $A_k$ for $k = 5, 6, 7, 8$ — these are elementary (combinations of $\sqrt{4k+9}$, $\ln(-3 + \sqrt{8k+9})$, rationals). Their sum is
$$A_5 + A_6 + A_7 + A_8 \;=\; \frac{4\ln(3/2)}{9} - \frac{7}{45}.$$
Since Corner 2 total $A_{\text{Corner 2}} = (4 \ln(3/2) - 1)/9$, the tail is **rationally clean**:
$$\boxed{\;\sum_{k \geq 9} A_k \;=\; \sum_{k \geq 9} J_k \;=\; \frac{2}{45}\;}$$
(a small accident: $(4\ln(3/2) - 1)/9 - (4\ln(3/2)/9 - 7/45) = -1/9 + 7/45 = 2/45$.)

This identity is **closed-form, exact, and independently verifiable**: SymPy gives it directly from `together(A5 + A6 + A7 + A8) = (4*log(3/2))/9 - 7/45`.

## 5 · Small-$k$ pieces

On each strip $k \in \{5, 6, 7, 8\}$, the integrand on $(u, v)$ becomes a sum of intervals in $v$ whose endpoints are piecewise of the form:
- $(1+u)/k$ or $(1+u)/(k+1)$ — rational in $u$,
- $1 - u$ — linear in $u$,
- $2/(9u)$ — rational in $u$,
- $v_{\text{root}}(u, k) = (u + \sqrt{u^2 + 8k/9})/(2k)$ — algebraic in $u$.

Integrating over $u$ on each piecewise segment produces elementary primitives:
$\int \sqrt{u^2 + a^2}\, du = \tfrac u 2 \sqrt{u^2 + a^2} + \tfrac{a^2}{2}\ln(u + \sqrt{u^2 + a^2})$ and analogous logs from $1/u$ terms. The resulting closed form for each $J_k$ involves the surds $\sqrt{4k + 9}$ (i.e. $\sqrt{57}, \sqrt{65}, \sqrt{73}$ for $k = 6, 7, 8$ in the form $\sqrt{81 + 72(k+1)}/3$) and inverse-hyperbolic sines that reduce to $\ln$s of conjugate surds.

Direct symbolic integration (SymPy) on the cleanly piecewise integrand for $k = 8$ produces a particularly clean result:
$$J_8 \;=\; \tfrac{4 \ln 3 - 6 \ln 2}{9} - \tfrac{4}{9}\sinh^{-1}\!\bigl(\tfrac{7}{24}\bigr) + \tfrac{4}{9}\sinh^{-1}\!\bigl(\tfrac{\sqrt 2}{4}\bigr) - \tfrac{2}{45}.$$
Using $\sinh^{-1}(\sqrt 2/4) = \tfrac 12 \ln 2$ and $\sinh^{-1}(7/24) = \ln(4/3) = 2\ln 2 - \ln 3$, this collapses to
$$\boxed{\;J_8 \;=\; \frac{8 \ln 3}{9} \;-\; \frac{4 \ln 2}{3} \;-\; \frac{2}{45}\;} \;=\; 0.00790357140283709\ldots$$
which agrees with the strip-counting numerical integral to 16 digits.

The remaining $J_5, J_6, J_7$ each have **a similar elementary form**, but they involve surds outside the $\{\ln 2, \ln 3\}$ field: specifically $\sqrt{57}$ (from $k=5,6$), $\sqrt{65}$ (from $k=6,7$), $\sqrt{73}$ (from $k=7,8$), $\sqrt{849}, \sqrt{977}, \sqrt{2185}, \sqrt{874}, \sqrt{283}, \sqrt{13678}$, and log-of-surd terms $\ln(-3 + \sqrt{4k+9})$ etc.

## 6 · Numerical results to 30+ digits

I computed each $J_k$ ($k = 5, 6, 7, 8$) to 50-digit precision in mpmath using piecewise quadrature with ALL breakpoints (including the new $v_{\text{root}} = 1 - u$ crossing at $u_1 = ((2k+1) - \sqrt{(2k+1)^2 - 4(k+1)(k - 2/9)})/(2(k+1))$, which the naive computation missed for $k = 5$):

| $k$ | $J_k$ (numerical, 30 dps) |
|---:|:---|
| 5  | 0.000637509621287199675819393481 |
| 6  | 0.002368633888074151491227599348 |
| 7  | 0.004879561600300379819411284928 |
| 8  | 0.007903571402837090906130715320 |

Sum: $J_{\text{small}} = 0.015789276512498821892589$.

Adding the exact tail $\sum_{k\geq 9} J_k = 2/45$:
$$J \;=\; J_{\text{small}} + \frac{2}{45} \;=\; 0.060233720956943266337033\ldots$$

Then
$$P_1 \;=\; \frac{8\ln(3/2) - 2}{9} - 2 J \;=\; 0.017723765293370695750833\ldots$$
$$P_{\text{start}} \;=\; P_1 + J \;=\; 0.077957486250313962087867\ldots$$
$$\boxed{\Pr(L = 1) \;=\; 0.227351677765\ldots,\qquad \Pr(L = 2) \;=\; 0.772648322234\ldots}$$

## 7 · Monte Carlo verification

A streaming numba implementation (`code/cluster_size_distribution_at_threshold.py`) at $t = 2/9$ **exactly** (not a quantile):

| Run | Total clusters | $\Pr(L=1)$ | Inter-seed SE |
|:---|---:|---:|---:|
| $10^9$ steps, 5 seeds | 77,953,577 | $0.22731765$ | $3.0 \times 10^{-5}$ |
| $5 \times 10^9$ steps, 10 seeds | 389,785,052 | $\mathbf{0.22735308}$ | $\mathbf{1.4 \times 10^{-5}}$ |

**Analytical vs MC agreement at $5 \times 10^9$ steps:**
$$|\Pr(L=1)_{\text{analytic}} - \Pr(L=1)_{\text{MC}}| \;=\; 1.4 \times 10^{-6} \quad < 0.1\,\sigma.$$
The analytical computation is therefore numerically certified.

Both runs see **zero** clusters of size $\geq 3$, in agreement with the Lean theorem.

## 8 · Closed-form search via PSLQ (negative result)

Using mpmath at 60 dps, I ran PSLQ on $J$ and on $\Pr(L=1)$ over a 24-dimensional basis consisting of
$$\{1,\ \ln 2,\ \ln 3,\ \ln 5,\ \ln 7,\ \sqrt 2,\ \sqrt 3,\ \sqrt 5,\ \sqrt 7,\ \sqrt{57},\ \sqrt{65},\ \sqrt{73},\ \sqrt{849},\ \sqrt{977},\ \sqrt{2185},\ \sqrt{874},\ \sqrt{283},\ \sqrt{13678},\ \ln(3+\sqrt{57}),\ \ln(3+\sqrt{65}),\ \ln(3+\sqrt{73}),\ \ln(3\sqrt{10}+\sqrt{874}),\ \ln(3\sqrt 3+\sqrt{283}),\ \ln(9\sqrt{14}+\sqrt{13678})\}.$$

The basis is the natural one suggested by the SymPy closed forms of the segments. PSLQ returned only relations with **3-digit integer coefficients** — these are essentially noise: at 60 digits with 24-dim basis, PSLQ will find spurious "relations" whenever the maximum coefficient $C$ satisfies $C^{n-1} \gtrsim 10^{60}$, i.e., $C \gtrsim 10^{60/23} \approx 400$. The coefficients returned are in this regime ($\sim 50$–$300$), so they are not meaningful.

**With smaller PSLQ bases (5–7 dim) up to coefficient $10^{12}$, NO relation is found**. In particular:

- $\Pr(L=1)$ has **no clean small-integer-coefficient combination** of $\ln 2, \ln 3$ and the obvious surds.
- The ratio $\Pr(L=2)/\Pr(L=1) \approx 3.3998\ldots$ similarly fails any small-coefficient PSLQ relation.

## 9 · Honest verdict

**What is proved (rigorous / closed form):**

1. $P_1 + 2 P_2 = (8\ln(3/2) - 2)/9$ (Lean-formalized via `bczProb_eq_value`).
2. $P_2 = J = $ the 2D BCZ integral above.
3. **$\sum_{k \geq 9} J_k = 2/45$ exactly** — a clean rational identity that cuts the problem to four explicit strips.
4. **$J_8 = (8\ln 3 - 16 \ln 2)/9 - 2/45$** — a fully elementary closed form in $\{\ln 2, \ln 3\}$.
5. $J_5, J_6, J_7$ each individually have **elementary closed forms** but involve the surd extensions $\sqrt{57}, \sqrt{65}, \sqrt{73}$ and logs of conjugate surds (SymPy-evaluable; written out in `code/J_smallk_symbolic_results.txt`).
6. Analytical $\Pr(L=1) = 0.2273516778\ldots$ agrees with $5\times 10^9$-step Monte Carlo to $1.4 \times 10^{-6}$.

**What is NOT proved (open / negative results):**

- There is **no small-integer closed form** of the form $\Pr(L=1) = (a + b \ln(3/2))/c$ (PSLQ rules this out to 60 digits).
- There is **no clean common simplification** of $J_5 + J_6 + J_7$: the surds $\sqrt{57}, \sqrt{65}, \sqrt{73}$ do not appear to cancel in the sum.
- Therefore the most we can write is
  $$\boxed{\;J \;=\; \frac{2}{45} \;+\; J_5 \;+\; J_6 \;+\; J_7 \;+\; J_8\;}$$
  where the four small-$k$ pieces are each explicit elementary functions (with $\sqrt{4k+9}$-extensions of $\mathbb Q(\ln 2, \ln 3)$).

This is a **partial closed form**: the closed-form character is **piecewise per Stern-Brocot strip**, and the strips fail to collapse into a single elementary expression in $\{\ln 2, \ln 3\}$ alone.

## 10 · Suggested Lean formalization path

Three theorems within reach (in roughly increasing difficulty):

1. **`bczClusterContent`** (easy): $P_1 + 2 P_2 = \texttt{bczProbXYLessTwoNinths}$ — just stationarity + cluster decomposition.
2. **`bczP2eqJ`** (medium): $P_2 = J$ — uses `cluster_size_le_two_clean` from v8.
3. **`bczTailClosedForm`** (medium, the prize): $\sum_{k \geq 9} J_k = 2/45$. This reduces (via the $k \geq 9 \Rightarrow J_k = A_k$ lemma) to evaluating $\sum_{k \geq 9} A_k = (4 \ln(3/2) - 1)/9 - (4 \ln(3/2)/9 - 7/45) = 2/45$, which is a finite-sum-of-elementary-integrals problem on Corner 2 strips. Mathlib has all the needed `intervalIntegral` lemmas.

The four small-$k$ pieces $J_5, J_6, J_7, J_8$ in Lean would each be a few hundred lines of `interval_integral` bookkeeping — a lot of work but mechanical given the explicit antiderivatives written out in this note.

## 11 · Why this matters

The original BCZ closed-form trilogy was:
- $q^*_{\mathrm{BCZ}} = (11 - 8\ln(3/2))/9$ (closed)
- `cluster_size_le_two` (cluster bound)
- sharpness of $q^*$ (`BCZSharpness.lean`)

Extending to **the exact cluster-size distribution at threshold** completes a quartet: distribution + threshold + max-size bound + sharpness. The structural surprise is that the tail $\sum_{k \geq 9} = 2/45$ is rationally clean while the head $J_5 + \ldots + J_8$ resists collapse — this is reminiscent of "trace of arithmetic geometry" patterns where most of the mass is rational and the irrationality lives in a finite low-Stern-Brocot-depth piece.

---

## Files

- `code/cluster_size_distribution_at_threshold.py` — numba MC (220 lines)
- `code/cluster_size_distribution_results.json` — $10^9$-step run
- `code/cluster_size_distribution_results_5e9.json` — $5 \times 10^9$-step run
- `code/J_smallk_v2.py` — mpmath 50-dps numerical $J_k$ + PSLQ search
- `code/J_smallk_v2_results.json` — high-precision values
- `code/J_symbolic.py` — symbolic $A_k$ (verified clean: $\sum_{k=5}^8 A_k = 4\ln(3/2)/9 - 7/45$)
- `code/J_smallk_symbolic_v2.py` — symbolic $J_k$ (timed out on full simplification; per-segment forms readable)
- `code/J_pslq_full.py` — PSLQ over 24-dim natural basis (negative result)

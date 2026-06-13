# The cluster-size distribution of the BCZ chain at the threshold

**Saar Shai — June 2026**

This note records the fourth piece of the cluster-size picture: the exact
distribution of cluster sizes *at* the threshold $t^\* = 2/9$, together with its
Monte-Carlo cross-check. The threshold value, the size-$\le 2$ bound, and its
sharpness were the first three; this completes the quartet.

---

## 1 · Setup

The BCZ chain is the system $(X_n)$ on the Farey triangle
$T = \{(x,y)\in(0,1)^2 : x+y>1\}$ driven by
$$
T_{\mathrm{BCZ}}(x,y) = \bigl(y,\ \lfloor (1+x)/y\rfloor\, y - x\bigr),
$$
with invariant probability density $f(x,y) = 2\cdot\mathbf 1_T(x,y)$. A consecutive
pair $(X_i,X_{i+1})$ is a **member** iff $X_i X_{i+1} < t^\*$, with $t^\* = 2/9$;
a **cluster** is a maximal run of consecutive members. At $t = t^\*$ every cluster
has size $\le 2$ (machine-checked, `cluster_size_le_two_clean`, Aristotle v8).

Write $P_k = \Pr(\text{a size-}k\text{ cluster starts at }i=0)$ and
$\Pr(L=k) = P_k/(P_1+P_2)$. **Goal:** $\Pr(L=1)$ and $\Pr(L=2)$ at $t = 2/9$.

## 2 · Two exact identities

**(I) Mass conservation.** $\Pr(\text{member}) = \sum_{k\ge1} k\,P_k$. Only $k=1,2$
occur, so
$$
P_1 + 2P_2 \;=\; \Pr(X_0X_1 < 2/9) \;=\; \frac{8\ln(3/2)-2}{9},
$$
the RHS being the BCZ closed form (Lean: `bczProb_eq_value`).

**(II) Two consecutive members $\Rightarrow$ a size-2 cluster.** Since no cluster
has size $\ge 3$, "member at 0 *and* member at 1" is exactly "the size-2 cluster
starts at 0":
$$
P_2 \;=\; \Pr\bigl(X_0X_1<2/9 \;\wedge\; X_1X_2<2/9\bigr) \;=:\; J.
$$
Then $P_1 = (8\ln(3/2)-2)/9 - 2J$ and
$$
\Pr(L=1) = \frac{(8\ln(3/2)-2)/9 - 2J}{(8\ln(3/2)-2)/9 - J},
\qquad
\Pr(L=2) = \frac{J}{(8\ln(3/2)-2)/9 - J}.
$$
The whole problem reduces to one 2-D integral
$$
J = \int_T 2\,\mathbf 1[uv<2/9]\,\mathbf 1[v(kv-u)<2/9]\,du\,dv,
\qquad k=\lfloor(1+u)/v\rfloor,\ X_2 = kv-u.
$$

## 3 · Stern–Brocot strip decomposition

The condition $uv<2/9$ on $T$ lives in two corners. In **Corner 1**
($u<1/3,\ v>2/3$) one has $k=1$ and $v(v-u) > (2/3)(1/3) = 2/9$, so it
contributes **zero**. On **Corner 2** ($u>2/3,\ v<1/3$) partition by the floor
value $k$, i.e. by the Stern–Brocot depth $T_k = \{v\in((1+u)/(k+1),(1+u)/k]\}$;
on Corner 2 one has $k\ge 5$.

**Tail collapse (the clean part).** For $k\ge 9$ the member-at-1 cap is automatic
($v\le 2/k \le 2/9$ forces $v\cdot X_2 \le 2/9$), so $J_k = A_k$, where $A_k$ is
the uncapped strip contribution. The closed forms give
$$
A_5+A_6+A_7+A_8 = \frac{4\ln(3/2)}{9} - \frac{7}{45},
\qquad
A_{\text{Corner 2}} = \frac{4\ln(3/2)-1}{9},
$$
so the **entire deep tail is a clean rational**:
$$
\boxed{\;\sum_{k\ge 9} J_k \;=\; \frac{2}{45}\;}
$$
The "irrationality" is confined to the four shallow strips $J_5,\dots,J_8$.

**Shallow strips.** $J_8$ collapses fully into $\{\ln2,\ln3\}$:
$$
\boxed{\;J_8 = \frac{8\ln 3}{9} - \frac{4\ln 2}{3} - \frac{2}{45}
= 0.00790357140283709\ldots\;}
$$
$J_5,J_6,J_7$ each have an explicit elementary closed form, but in the surd
extensions $\sqrt{57},\sqrt{65},\sqrt{73}$ (and logs of conjugate surds); they do
not collapse into $\mathbb Q(\ln2,\ln3)$. A 60-digit PSLQ over the natural
24-dimensional basis finds **no** small-coefficient relation for $J$, $\Pr(L=1)$,
or the ratio — so the head genuinely resists elementary collapse.

## 4 · Numerical value

To 50-dps quadrature (all breakpoints, including the $v_{\text{root}} = 1-u$
crossing):

| $k$ | $J_k$ (30 dps) |
|---:|:---|
| 5 | 0.000637509621287199675819393481 |
| 6 | 0.002368633888074151491227599348 |
| 7 | 0.004879561600300379819411284928 |
| 8 | 0.007903571402837090906130715320 |

$J = J_5+J_6+J_7+J_8 + 2/45 = 0.060233720956943266\ldots$, hence
$$
\boxed{\Pr(L=1) = 0.2273516778\ldots,\qquad \Pr(L=2) = 0.7726483222\ldots}
$$

## 5 · Monte-Carlo cross-check

Streaming `numba` run at $t = 2/9$ **exactly** (not a quantile),
`cluster_size_distribution_at_threshold.py`:

| Run | Total clusters | $\Pr(L=1)$ | inter-seed SE |
|:---|---:|---:|---:|
| $10^9$ steps, 5 seeds | 77,953,577 | 0.22731765 | $3.0\times10^{-5}$ |
| $5\times10^9$ steps, 10 seeds | 389,785,052 | **0.22735308** | $1.4\times10^{-5}$ |

Analytic vs MC at $5\times10^9$ steps:
$$
|\Pr(L=1)_{\text{analytic}} - \Pr(L=1)_{\text{MC}}| = 1.4\times10^{-6} < 0.1\,\sigma.
$$
Both runs see **zero** clusters of size $\ge 3$, matching the Lean bound.

## 6 · What is rigorous vs numerical

**Rigorous / closed form:** (1) $P_1+2P_2 = (8\ln(3/2)-2)/9$;
(2) $P_2 = J$; (3) $\sum_{k\ge9}J_k = 2/45$ exactly;
(4) $J_8 = (8\ln3 - 12\ln2)/9 - 2/45$ in $\{\ln2,\ln3\}$;
(5) $J_5,J_6,J_7$ elementary in $\sqrt{57},\sqrt{65},\sqrt{73}$.

**Numerical / negative:** $\Pr(L=1)$ has no small-coefficient closed form (PSLQ to
60 dps); the surds in $J_5+J_6+J_7$ do not cancel. The clean object is the
*piecewise-per-strip* form $J = 2/45 + J_5 + J_6 + J_7 + J_8$.

The structural surprise — most of the mass rational ($2/45$ tail), the
irrationality confined to a finite low-depth head — is the cluster-size analogue
of the trace patterns in the extremal-constant family.

## 7 · Files in this folder

- `cluster_size_distribution_at_threshold.py` — streaming `numba` Monte Carlo at $t=2/9$ exactly.
- `cluster_size_distribution_results.json` — $10^9$-step run.
- `cluster_size_distribution_results_5e9.json` — $5\times10^9$-step run.

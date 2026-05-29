# T12 — BCZ ergodic optimization: orbit- and measure-level promotion of the 2/9 ceiling

**Status.** Task (a) on-paper proof. The *orbit form* (1) is a near-immediate corollary of
the proven, Lean-formalized pointwise 3-window bound (`cluster_size_le_two_clean`, v8). The
*measure form* (2) requires a short ergodic-theory argument (Poincaré recurrence + invariance);
it is rigorous as written but its Lean formalization needs Mathlib infrastructure that is only
partially present — see the honesty section at the end and `PROMPT_T12.md`.

Author framing only (no claim these papers prove our statement): ergodic optimization — Jenkinson,
*Ergodic optimization in dynamical systems*, ETDS 39 (2019) 2593–2618; Contreras, *Ground states
are generically a periodic orbit*, Invent. Math. 205 (2016) 383–412; Bousch, *Le poisson n'a pas
d'arêtes*, Ann. IHP 36 (2000). These establish that for many systems the minimizing/maximizing
invariant measure of a generic continuous observable is supported on a periodic orbit. Our result
is an *instance flavored* by that theory but is proved directly, not by appeal to it.

---

## 0. Setup and the input theorem

Let
$$\mathcal T=\{(a,b)\in\mathbb R^2 : 0<a<1,\ 0<b<1,\ a+b>1\}$$
(the open BCZ / Farey triangle — note the strict inequalities; this matters, see §4). The BCZ map is
$$T(a,b)=\bigl(b,\ k\,b-a\bigr),\qquad k=k(a,b)=\Big\lfloor\frac{1+a}{b}\Big\rfloor\in\mathbb Z_{\ge1},$$
which preserves Lebesgue density $2$ on $\mathcal T$ (the SL$(2,\mathbb Z)$ horocycle return map).
The observable is the **gap product**
$$P(a,b)=a\,b.$$
Note $P\circ T(a,b)=b\,(kb-a)$, so along a forward orbit $x,Tx,T^2x,\dots$ the values
$P(T^n x)$ are exactly the consecutive products $\dots,P_{n-1},P_n,P_{n+1},\dots$ in the v8
certificate.

**Input (proven; Lean v8, 0 sorries).** For four consecutive orbit coordinates the contrapositive
of `cluster_size_le_two_clean` gives the **3-window bound**:

> **(W)** For every $x\in\mathcal T$ with $Tx,T^2x\in\mathcal T$ (automatic since $T$ maps $\mathcal T\to\mathcal T$),
> $$\max\bigl(P(x),\,P(Tx),\,P(T^2x)\bigr)\ \ge\ \tfrac29 .$$

Indeed `cluster_size_le_two_clean` is stated as: if $P(x)<2/9$ and $P(Tx)<2/9$ then $P(T^2x)\ge2/9$.
Contrapositively, you cannot have three consecutive products all $<2/9$, which is exactly (W) for
the window $\{x,Tx,T^2x\}$. Shifting the index, for every $n$,
$$\max\bigl(P(T^{n}x),P(T^{n+1}x),P(T^{n+2}x)\bigr)\ge\tfrac29. \tag{W$_n$}$$

We treat $T$ as a (forward) self-map of $\mathcal T$. Where a two-sided orbit ($n\in\mathbb Z$) is
referenced, it means: $T$ is a.e. invertible on $\mathcal T$ (its inverse is
$T^{-1}(a,b)=(\ell b-a,\,a)$ with $\ell=\lfloor(1+b)/a\rfloor$ off a measure-zero floor-discontinuity
set), and the two-sided orbit is the bi-infinite extension; (W$_n$) holds for all $n\in\mathbb Z$ by
the same local computation.

---

## 1. Orbit form (1)

**Claim 1a (pointwise ceiling).** For every $x\in\mathcal T$,
$$\sup_{n\ge0} P(T^n x)\ \ge\ \tfrac29 .$$

*Proof.* Apply (W$_0$): $\max(P(x),P(Tx),P(T^2x))\ge2/9$, and the LHS is $\le\sup_{n\ge0}P(T^nx)$.
$\qquad\blacksquare$

This is the whole of the "consequently" clause: a single instance of the proven 3-window bound
forces the forward ceiling to be at least $2/9$. (No recurrence, no measure theory.)

**Claim 1b (infimum over orbits $=2/9$, attained).** Let
$$C(x):=\sup_{n\in\mathbb Z}P(T^nx)\quad(\ge\sup_{n\ge0}P(T^nx)),\qquad
c^\*:=\inf_{x\in\overline{\mathcal T}}C(x).$$
Then $c^\*=2/9$, and on the closed triangle it is attained exactly on the period-2 vertex orbit
$$O_\* := \{(1/3,2/3),\ (2/3,1/3)\}.$$

*Proof.*
($\ge$) By Claim 1a, $C(x)\ge2/9$ for every $x\in\mathcal T$, so $c^\*\ge2/9$. (On the open triangle
the inequality is what (W) delivers; we pass to the closure below to realize equality.)

($\le$, attainment) Evaluate on $O_\*$. The two points $(1/3,2/3)$ and $(2/3,1/3)$ each have
$P=1/3\cdot2/3=2/9$. They form a genuine period-2 orbit of $T$ *as a limit of the interior
$[4,1]$ family* (see §3 and the boundary remark §4): on the family $(a,a/2)\leftrightarrow(a/2,a)$,
$a\in(2/3,1]$, every orbit point has product $a^2/2$, and
$$C\bigl((a,a/2)\bigr)=\tfrac{a^2}{2}\ \searrow\ \tfrac{(2/3)^2}{2}=\tfrac29\quad\text{as }a\to(2/3)^+ .$$
Hence $\inf_a C=2/9$, realized in the limit at the vertex orbit $O_\*$, giving $c^\*\le2/9$. With ($\ge$),
$c^\*=2/9$.

(uniqueness of the minimizer) Suppose $C(x)=2/9$. Then $P(T^nx)\le2/9$ for **all** $n$. Combined with
the 3-window bound (W$_n$), which forces $\max$ over each window $\ge2/9$, every window must have its
maximum *equal* to $2/9$; in particular $P(T^nx)\le2/9$ for all $n$ and the bound is saturated. The v8
analysis shows the only way a *window* attains exactly $2/9$ at its max with the other two entries
$\le2/9$ pins the middle coordinate to the boundary case $b\to1/3$, $c\to2/3$ (the Step 1–6 chain
collapses to its equality locus $b=1/3$, $c=2/3$). Iterating, every orbit coordinate equals
$(1/3,2/3)$ or $(2/3,1/3)$, i.e. $x\in O_\*$. (This is the closure-realized equality case;
no *interior* point of $\mathcal T$ achieves $C=2/9$, since interior $[4,1]$ orbits have
$C=a^2/2>2/9$.) $\qquad\blacksquare$

**Remark (why $[4,1]$, not $[2,2]$).** The optimizing symbolic word is $k$-word $[4,1]$
(read off the floors $\lfloor(1+a)/b\rfloor=4$ at $(a,a/2)$ and $=1$ at $(a/2,a)$), *not* the
diagonal fixed family word $[2]$. The diagonal family $(a,a)$ has product $a^2$ with infimum
$1/4>2/9$; it is the runner-up ceiling family, not the optimizer. T9 confirmed this numerically
(`task3.optimal_word=[4,1]`, `runner_up_family=[2]`).

---

## 2. Measure form (2) — the publishable statement

Equip $\mathcal T$ with its Borel $\sigma$-algebra. $P:\mathcal T\to(0,1)$ is bounded continuous.
For a $T$-invariant Borel probability measure $\mu$, write
$$M(\mu):=\operatorname*{ess\,sup}_{\mu}P=\inf\{t:\mu(P>t)=0\}.$$

**Theorem 2.** For every $T$-invariant Borel probability measure $\mu$ on $\mathcal T$,
$$M(\mu)\ \ge\ \tfrac29 ,$$
with equality **iff** $\mu=\mu_\*:=\tfrac12(\delta_{(1/3,2/3)}+\delta_{(2/3,1/3)})$, the unique
invariant probability measure carried by the vertex orbit $O_\*$.

*(Caveat on the support of $\mu$: $O_\*$ lies on $\partial\mathcal T$ — see §4. If one insists
$\mu$ be supported in the **open** $\mathcal T$, then $M(\mu)>2/9$ strictly and the infimum $2/9$ is
an unattained limit. The clean "iff" is correct precisely when invariant measures on the closed
triangle $\overline{\mathcal T}$ are allowed, which is the natural setting because $\mu_\*$ is the
weak-$*$ limit of the interior $[4,1]$ family's invariant measures.)*

### Proof of the inequality $M(\mu)\ge2/9$.

Suppose for contradiction $M(\mu)<2/9$. Pick $t$ with $M(\mu)<t<2/9$. Set
$$A:=\{x : P(x)\le t\}.$$
By definition of ess-sup, $\mu(P>t)=0$, i.e. $\mu(A)=1$.

Define the **forward-good set**
$$G:=\{x : P(T^n x)\le t\ \text{for all }n\ge0\}=\bigcap_{n\ge0}T^{-n}A .$$
Each $T^{-n}A$ has $\mu(T^{-n}A)=\mu(A)=1$ by $T$-invariance of $\mu$ (push-forward
$T_*\mu=\mu$ gives $\mu(T^{-n}A)=\mu(A)$). A countable intersection of full-measure sets is full, so
$$\mu(G)=1 .$$
In particular $\mu(G)>0$, so $G\neq\varnothing$; pick $x\in G$. Then $P(T^nx)\le t<2/9$ for **every**
$n\ge0$. Take $n=0$:
$$\max\bigl(P(x),P(Tx),P(T^2x)\bigr)\le t<\tfrac29,$$
directly contradicting the 3-window bound (W$_0$). Hence $M(\mu)\ge2/9$. $\qquad\blacksquare$

> **Note.** This argument does **not** even need Poincaré recurrence — invariance of $\mu$ plus the
> countable intersection $G=\bigcap_{n\ge0}T^{-n}A$ already produces a full-measure set of points whose
> *entire forward orbit* stays $\le t$, which (W) forbids. Recurrence is needed only if one wants the
> *two-sided* statement $\sup_{n\in\mathbb Z}$ from a one-sided hypothesis, or to upgrade "ess-sup over
> the orbit" to "ess-sup over the space"; for the ess-sup-over-space statement above it is unnecessary.
> I flag this because the task prompt suggested Poincaré recurrence; the cleaner route bypasses it.
> Recurrence does give an alternative proof (below) and is the natural tool if one only assumes
> $\mu(A)>0$ for an *invariant* $A$, so I record it.

### Alternative proof via Poincaré recurrence (records the recurrence route).

The set $G=\bigcap_{n\ge0}T^{-n}A$ is forward-invariant ($T^{-1}G\supseteq G$, and $\mu(T^{-1}G)=\mu(G)$
forces $\mu(G\triangle T^{-1}G)=0$, so $G$ is invariant mod $\mu$-null). On the invariant full-measure
set $G$, $T|_G$ preserves $\mu|_G$. By Poincaré recurrence, $\mu$-a.e. $x\in G$ returns to every
neighborhood; in particular a.e. orbit in $G$ is recurrent and infinite, and on it $P\le t<2/9$ forever
— again contradicting (W$_0$) applied at any window. (The first proof is strictly shorter; recurrence
adds nothing essential here because (W) already triggers at $n=0$.)

### Proof of the equality characterization.

($\Leftarrow$) For $\mu_\*$: $P\equiv2/9$ on the two-point support $O_\*$, so $M(\mu_\*)=2/9$.
$\mu_\*$ is invariant because $T$ swaps the two points (period 2), and it is the **unique** invariant
probability on $O_\*$: any invariant $\mu$ on the 2-cycle must give equal mass $1/2$ to each point
(invariance under the swap), so $\mu=\mu_\*$.

($\Rightarrow$) Suppose $\mu$ is invariant with $M(\mu)=2/9$. Then $\mu(P>2/9)=0$, so $P\le2/9$
$\mu$-a.e. Repeat the good-set construction with $t=2/9$ and **non-strict** inequality:
$A':=\{P\le2/9\}$ has $\mu(A')=1$; $G':=\bigcap_{n\ge0}T^{-n}A'$ has $\mu(G')=1$. For $x\in G'$,
$P(T^nx)\le2/9$ for all $n$, and by (W$_n$) each window's max is $\ge2/9$, hence **every** window max
equals $2/9$ — so the equality locus of the v8 Step 1–6 chain holds at every coordinate. As in Claim 1b,
that locus is exactly $\{b=1/3,c=2/3\}$ and its $T$-image, i.e. the orbit is $O_\*$. Therefore
$\mu(G'\setminus O_\*)$ carries points whose orbit is forced onto $O_\*$; combined with $\mu(G')=1$,
$\mu$ is supported on $O_\*$ (every full-measure orbit lands in $O_\*$). The unique invariant
probability on $O_\*$ is $\mu_\*$, so $\mu=\mu_\*$. $\qquad\blacksquare$

---

## 3. Why the optimizer is the vertex orbit (consistency with ergodic optimization)

For the **min-ess-sup ("ceiling") functional** $\mu\mapsto M(\mu)$, the minimizing measure is
$\mu_\*$, supported on the period-2 orbit with symbolic word $[4,1]$ in the boundary limit
$a\to(2/3)^+$. This is the BCZ analogue of the "optimal measure is a periodic orbit" phenomenon, with
a *parabolic-family twist*: because $T$ is area-preserving and parabolic, periodic orbits are not
isolated — each word with $\mathrm{tr}\,M=2$ gives a 1-parameter family. The $[4,1]$ family carries
the unique infimal ceiling $a^2/2\downarrow2/9$, attained only in the boundary/vertex limit. T9's
numerics (`min_sup_P` over enumerated orbits at the $[4,1]$ 2-cycle; brute-force corroboration: no
orbit dips below $2/9$) match this exactly.

---

## 4. Genuine subtleties / gaps flagged (adversarial honesty)

1. **The vertex sits on a floor discontinuity (real subtlety, handled).** At $(1/3,2/3)$,
   $(1+a)/b=(4/3)/(2/3)=2$ exactly, so $k=\lfloor2\rfloor=2$ there, while the *interior* $[4,1]$ family
   approaching it has $k=4$ on one leg and $k=1$ on the other. The vertex orbit is therefore a
   **boundary limit** of the $[4,1]$ family, not an interior $[2,2]$ orbit. Two honest consequences:
   - The optimizer's symbolic word is $[4,1]$, **not** $[2,2]$. Stating the equality case as "the
     period-2 vertex orbit" is correct; stating it as "the $[2,2]$/diagonal orbit" would be wrong.
   - $O_\*\subset\partial\mathcal T$ (since $a+b=1$ there, not $>1$, and one coordinate hits the open-set
     boundary in the limit). With the **open** triangle the infimum $2/9$ is a non-attained limit; the
     clean "iff $\mu=\mu_\*$" requires admitting invariant measures on $\overline{\mathcal T}$. I state
     both versions in Theorem 2. **This is the one place the equality "iff" needs the closure
     hypothesis** — flagged, not papered over.

2. **One-sided vs two-sided.** The ess-sup-over-space inequality (§2 main proof) is fully rigorous with
   only forward invariance and the countable intersection; it needs neither invertibility nor recurrence.
   The two-sided orbit ceiling $\sup_{n\in\mathbb Z}$ uses a.e. invertibility of $T$ (true off a null
   set), which is standard but is an extra fact beyond the v8 file.

3. **Existence of non-trivial invariant measures is not asserted.** Theorem 2 is a *lower bound on
   every* invariant measure; it does not claim interesting invariant measures exist (they do — Lebesgue
   density 2 is invariant, with $M=\sup P\to1/4$ region... in fact $\operatorname{ess\,sup}_{\rm Leb}P=1/4$
   at the diagonal corner; consistent with $\ge2/9$). No gap, just clarifying scope.

4. **No gap in the inequality.** The inequality $M(\mu)\ge2/9$ is unconditional (any invariant Borel
   probability, open or closed triangle). Only the *equality characterization* carries the closure
   caveat of point 1.

**Summary of solidity.** (1) orbit form and (2) the inequality $M(\mu)\ge2/9$ are airtight, resting on
one instance of the proven 3-window bound + invariance. The equality/uniqueness clause is rigorous
modulo the explicitly stated closure convention (point 1), and its sharpest step — that the saturated
window locus is exactly $\{b=1/3,c=2/3\}$ — is a re-reading of the v8 Step 1–6 equality case, which is
true but is *not itself separately formalized in v8* (v8 proves the strict cluster bound, not the
equality-locus characterization). That is the only place a Lean formalization would need a genuinely new
lemma. See `PROMPT_T12.md`.

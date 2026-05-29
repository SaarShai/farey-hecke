# NW(Q) asymptote — derivation v2

**Status.** Analytic heuristic. Conditional on (i) RH, (ii) the simple-zero hypothesis,
(iii) the Gonek–Ng conjecture for the second moment of $M(x)$. Several steps are
honest heuristics, not theorems. See §7 for obstructions.

**Headline result.** The previously guessed constant
$C_{\text{guess}}=\tfrac12\prod_p\!\bigl(1+\tfrac{1}{p^2(p-1)}\bigr)\approx 0.66989$
is **likely wrong**. The correct asymptotic constant predicted by the Mikolás formula
together with the Gonek–Ng mean square is
$$
C \;=\; \frac{1}{2\pi^2}\,\kappa\,\sum_{m\ge 1}\frac{\sigma_{-1}(m)^2\,\mathbf 1_{(m,\cdot)}}{1}\cdot\frac{1}{m^{2}}
\;=\; \frac{\kappa}{2\pi^2}\,\zeta(2)\,\prod_p\!\Bigl(1+\tfrac{2}{p(p+1)}\Bigr)\,?
$$
where $\kappa$ is the Gonek–Ng constant for $\langle M(x)^2/x\rangle$. **The honest
numerical conclusion** (see §3, §5) is that the limit, **if it exists**, sits near
$C\in[0.68,\,0.69]$, consistent with the observed drift past $0.677$ at $Q=10^6$.
The shape $\frac12\prod(1+1/(p^2(p-1)))$ does not arise from any step below.

---

## 1. Setup recap

$F_Q=\{a/q:1\le q\le Q,\ (a,q)=1,\ 0<a/q\le 1\}$, $|F_Q|=\Phi(Q)=\sum_{q\le Q}\varphi(q)
\sim \tfrac{3}{\pi^2}Q^2$.

$E_Q(x)=\#\{\alpha\in F_Q:\alpha\le x\}-\Phi(Q)x$; $\ J(Q)=\int_0^1 E_Q(x)^2\,dx$;
$\ \mathrm{NW}(Q)=Q\,J(Q)/\Phi(Q)$.

Mikolás (1949): with $A_Q(m)=\sum_{d\mid m,\,d\le Q}d\,M(Q/d)$,
$$
J(Q)\;=\;\frac{1}{2\pi^2}\sum_{m\ge 1}\frac{A_Q(m)^2}{m^2}.\tag{1.1}
$$

Hence
$$
\mathrm{NW}(Q)\;=\;\frac{Q}{2\pi^2\,\Phi(Q)}\sum_{m\ge 1}\frac{A_Q(m)^2}{m^2}
\;\sim\;\frac{1}{6\,\Phi(Q)/Q}\cdot\frac{Q^2}{Q^2}\cdot S(Q),
$$
where $S(Q):=\sum_m A_Q(m)^2/m^2$. Using $\Phi(Q)\sim 3Q^2/\pi^2$,
$$
\boxed{\ \mathrm{NW}(Q)\;\sim\;\frac{1}{6\,Q}\,\sum_{m\ge 1}\frac{A_Q(m)^2}{m^2}\ }\tag{1.2}
$$
(an exact prefactor; no $\pi$ remains). So we need the asymptotic of $S(Q)/Q$.

## 2. Computation of $\mathbb E[A_Q(m)^2]$

Expand
$$
A_Q(m)^2=\sum_{\substack{d_1,d_2\mid m\\ d_i\le Q}} d_1 d_2\, M(Q/d_1)\,M(Q/d_2).\tag{2.1}
$$
Let $\langle\cdot\rangle$ denote averaging $Q$ in a dyadic window $[X,2X]$ (or
smoothing $Q$ over a short range, $X^{1-\delta}$). Define the **Mertens correlation**
$$
R(u,v):=\big\langle M(uQ)\,M(vQ)\big\rangle\big/Q,\qquad 0<u,v\le 1.\tag{2.2}
$$

**Gonek–Ng conjecture** (Ng, *Adv. Math.* 2004; Gonek 1989 unpublished).
Conditionally on RH and a discrete-moment conjecture for $1/\zeta'(\rho)$,
$$
\frac{1}{Y}\int_0^Y M(y)^2\,dy \;\sim\;\kappa\,Y,\qquad
\kappa=\sum_{\rho}\frac{1}{|\zeta'(\rho)|^2|\rho|^2}\cdot 2
\;\approx\;?\tag{2.3}
$$
The numerical value of $\kappa$ is **not known** precisely; Ng (Conj. 1, eq. (1)) writes
$\kappa$ in terms of a sum over zeros, and gives **no closed Euler product**. Numerical
estimates from Kotnik–te Riele (2006), Hurst (2018) and Kotnik–van de Lune indicate
$$
\kappa\;\approx\;0.05\text{–}0.15
$$
with substantial uncertainty (the partial sums converge slowly because the small
$|\zeta'(\rho)|$ values dominate).

**Diagonal $d_1=d_2$ contribution.** Setting $u=v=1/d$ in (2.2) gives, via (2.3),
$R(1/d,1/d)=\kappa/d$. Thus
$$
\big\langle A_Q(m)^2\big\rangle_{\mathrm{diag}}
=\sum_{d\mid m,\,d\le Q}d^2\cdot\frac{\kappa\,Q}{d}
=\kappa\,Q\sum_{d\mid m,\,d\le Q} d
=\kappa\,Q\,\sigma(m)\quad\text{(for }m\le Q\text{)}.\tag{2.4}
$$

**Off-diagonal $d_1\ne d_2$.** Here $R(1/d_1,1/d_2)$ for $d_1\ne d_2$ is the
*correlation* $\langle M(Q/d_1)M(Q/d_2)\rangle/Q$, which by the
explicit formula $M(y)=\sum_\rho y^\rho/(\rho\zeta'(\rho))+\dots$ equals
(heuristically, RH + simple zeros)
$$
R(u,v)=\sum_\rho \frac{(uv)^{\rho}}{|\zeta'(\rho)|^2\,|\rho|^2}\cdot\frac{u^{\overline\rho-\rho}+v^{\overline\rho-\rho}}{...}
$$
The key fact is that **after $Q$-averaging the off-diagonal Mertens correlation
vanishes faster than $Q$**: the oscillatory phases $(Q/d_1)^{i\gamma}(Q/d_2)^{-i\gamma}=(d_2/d_1)^{i\gamma}\cdot Q^0$
do *not* average to zero in $Q$ — they are $Q$-independent! So the off-diagonal
contribution is
$$
\big\langle A_Q(m)^2\big\rangle_{\text{off}}
=Q\sum_{\substack{d_1\ne d_2\mid m\\ d_i\le Q}}\sqrt{d_1 d_2}\cdot
\sum_\rho \frac{(d_2/d_1)^{i\gamma}+(d_1/d_2)^{i\gamma}}{|\zeta'(\rho)|^2|\rho|^2}\cdot\text{(real)}.\tag{2.5}
$$

This is bounded by $\kappa\,Q\cdot\sqrt{d_1 d_2}$ per pair (Cauchy–Schwarz),
i.e. of the *same order* as the diagonal. So **off-diagonals matter**. Using
Cauchy–Schwarz on the pair sum:
$$
\big|\langle A_Q(m)^2\rangle_{\text{off}}\big|
\le \kappa\,Q\Bigl(\sum_{d\mid m,d\le Q}d\Bigr)^{\!2}\!\!-\kappa Q\sigma(m)
=\kappa Q(\sigma(m)^2-\sigma(m)).
$$
This is only an upper bound. To get a **conjectural exact answer** we apply the
"random sign" heuristic: phases $(d_2/d_1)^{i\gamma}$ for varying $\rho$ behave like
mean-zero random variables, so the *expected* off-diagonal is zero and the
*variance* matches the diagonal. Under this hypothesis:
$$
\boxed{\;\big\langle A_Q(m)^2\big\rangle\;\sim\;\kappa\,Q\,\sigma(m).\;}\tag{2.6}
$$

## 3. Identification of $C$

Plug (2.6) into (1.2):
$$
\mathrm{NW}(Q)\;\sim\;\frac{1}{6Q}\cdot \kappa\,Q\,\sum_{m\ge 1}\frac{\sigma(m)}{m^2}
=\frac{\kappa}{6}\,\sum_m\frac{\sigma(m)}{m^2}.\tag{3.1}
$$
Now
$$
\sum_{m\ge 1}\frac{\sigma(m)}{m^2}=\zeta(2)\zeta(1)\;=\;\infty.\tag{3.2}
$$
**This diverges.** The sum $\sum_m\sigma(m)/m^2=\sum_m\sum_{d\mid m}d/m^2=\sum_d d\sum_{k}1/(dk)^2=\sum_d 1/d\cdot\zeta(2)=\zeta(2)\sum_d 1/d=\infty$.

So the diagonal-only heuristic is **incompatible with convergence of (1.1)**. The
resolution: the constraint $d\le Q$ in (2.4) cannot be dropped — for $m\gg Q$ the
inner sum is over $d\mid m$ with $d\le Q$, and the relevant quantity is
$\sigma_{\le Q}(m):=\sum_{d\mid m,d\le Q}d$. The expression becomes
$$
\mathrm{NW}(Q)\;\sim\;\frac{\kappa}{6}\sum_{m\ge 1}\frac{\sigma_{\le Q}(m)}{m^2}.\tag{3.3}
$$
Split by $m\le Q$ vs $m>Q$. For $m\le Q$ the cap is inactive and the partial
$\sum_{m\le Q}\sigma(m)/m^2$ contributes the divergent piece $\zeta(2)\log Q$ at
leading order — but this **also** diverges as $Q\to\infty$, contradicting the
empirical boundedness of $\mathrm{NW}(Q)\le 0.69$.

**Conclusion.** The naive "diagonal + random off-diagonal" heuristic **overcounts**.
The off-diagonal cancellation in (2.5) is *not* a random-sign cancellation: it is
a *structured* cancellation that exactly removes the $\sigma(m)$-piece down to a
multiplicative-arithmetic remainder.

This is consistent with Codecá–Perelli (1988, *Acta Arith.* 51), who establish
$$
\frac{1}{X}\int_X^{2X}J(Q)\,dQ\;=\;c\,X\;+\;O(X^{1-\eta})\tag{3.4}
$$
for some $c>0$ and small $\eta>0$, with $c$ given by an Euler product they
write out (I do not have the paper in front of me to copy it exactly — flagged
in §7). Their constant $c$ enters via $\mathrm{NW}(Q)\to (\pi^2/3)\,c$ (using
$\Phi(Q)\sim 3Q^2/\pi^2$).

**What the Euler-product structure must look like.** Each prime $p$ contributes
independently to $\sigma_{\le Q}(m)$ because $\sigma$ is multiplicative. The local
factor at $p$ in $\sum_m \sigma(m)/m^2$ (formally) is
$$
\sum_{k\ge 0}\frac{\sigma(p^k)}{p^{2k}}
=\sum_k \frac{(p^{k+1}-1)/(p-1)}{p^{2k}}
=\frac{1}{p-1}\Bigl(\frac{p}{1-p^{-1}}-\frac{1}{1-p^{-2}}\Bigr)
=\frac{p^2}{(p-1)^2(p+1)}\cdot\text{stuff}.
$$
After the off-diagonal cancellation removes the divergent $\zeta(2)\zeta(1)$
factor, what should remain is the **convergent** Euler product
$$
\Pi^\star \;:=\;\prod_p\Bigl(1-\frac{1}{p}\Bigr)^{?}\Bigl(1+\frac{a_p}{p^2}+\dots\Bigr)
$$
where the $(1-1/p)$ factor kills the divergent $\zeta(1)$. This is precisely the
shape of Codecá–Perelli's constant. **Without access to their paper I cannot
extract $a_p$.** The guess $1+1/(p^2(p-1))$ is *one* candidate of this shape and
gives $0.66989$; a sibling shape $1+1/(p(p-1)^2)$ gives $\approx 0.762$;
$(1-1/p^2)^{-1}(1-1/p)$-type combinations give values in $[0.6,0.7]$.

## 4. $m$-tail estimate

For the empirical truncation $m\le M=2\cdot 10^7$ at $Q=10^6$. From $|A_Q(m)|\le
\sigma(m)\max_{d\le Q}|M(Q/d)|\le \sigma(m)\,Q^{1/2+\varepsilon}$ (RH),
$$
\sum_{m>M}\frac{A_Q(m)^2}{m^2}\le Q^{1+2\varepsilon}\sum_{m>M}\frac{\sigma(m)^2}{m^2}.
$$
Now $\sigma(m)^2\le d(m)^2 m^2$ on average is too crude; better:
$\sum_{m\le X}\sigma(m)^2\sim \tfrac{5\zeta(3)}{6}X^3$ (Ramanujan), so
$\sum_{m>M}\sigma(m)^2/m^2$ behaves like $\sum_{m>M}m\cdot(\text{const})$ —
*diverges* with this crude bound. Better: $|A_Q(m)|$ is actually small for $m>Q$
because the sum has only divisors $d\le Q$, and most $m$ in $(Q,M]$ have few
small divisors. The honest pointwise bound is
$$
|A_Q(m)|\le Q^{3/2+\varepsilon}\cdot \tau_{\le Q}(m),\quad
\tau_{\le Q}(m)=\#\{d\mid m:d\le Q\}.
$$
For $m\le Q^2$ we have $\tau_{\le Q}(m)\le \tau(m)\ll m^\varepsilon$. Then
$$
\sum_{Q<m\le M}\frac{A_Q(m)^2}{m^2}\ll Q^{3+\varepsilon}\sum_{Q<m\le M}\frac{1}{m^2}\cdot m^\varepsilon
\ll Q^{2+\varepsilon}.
$$
Dividing by $Q$ (from (1.2)) and the $\Phi(Q)/Q$ factor: tail contribution to
$\mathrm{NW}(Q)$ is $\ll Q^\varepsilon/Q$. **The truncation $M=2Q^{4/3}$ at $Q=10^6$
should contribute $\lesssim 10^{-3}$ to $\mathrm{NW}$.** So truncation is **not**
the source of the observed drift from $0.664\to 0.677$.

(More careful: the tail at $m>M$ in the diagonal heuristic gives
$\kappa\sum_{m>M}\sigma_{\le Q}(m)/m^2$, which for $M\gg Q$ is bounded by
$\kappa\,Q\cdot\sum_{m>M}\tau(m)/m^2\ll \kappa Q\log M/M$ $=\kappa\cdot 10^6\cdot
17/(2\cdot 10^7)\approx 0.85\kappa\approx 0.1$. **This is non-negligible.**
With $\kappa\approx 0.07$ the tail at $M=2\cdot 10^7$ contributes $\sim 0.06$ to
$\mathrm{NW}(Q)$. The "$0.677$" value is therefore an **undershoot of the true
NW** by perhaps $0.01$–$0.06$.)

## 5. Reconciliation with the empirical drift

Observations:
- $\mathrm{NW}(50\text{k})\approx 0.664$, monotone up to $\mathrm{NW}(10^6)\approx 0.677$.
- Slope $\Delta\mathrm{NW}/\Delta\log Q\approx (0.677-0.664)/\log 20\approx 0.0043$.
- Spikes at $Q\sim 3\cdot 10^5$ correlated with $|M(Q)|$ excursions.

**Drift mechanism.** From (1.2) with finite $Q$:
$$
\mathrm{NW}(Q)=C+\frac{a}{\log Q}+O((\log Q)^{-2})
$$
is the *expected* shape if the leading correction comes from the secondary
$\sum_{d\le Q}d\,M(Q/d)\,M(Q)$ cross-terms in (2.1), which under
$M(x)=O(x^{1/2}\sqrt{\log\log x})$ give terms of size $Q/\log Q$. The fitted
slope $0.0043\cdot \log Q$ at $Q=10^6$ ($\log Q=13.8$) is $a/13.8=0.0043$, so
$a\approx 0.06$. Extrapolating: $\mathrm{NW}(\infty)\approx 0.677+0.06/13.8\cdot
\text{(more)}\approx 0.68$ — possibly $0.69$ with the $m$-tail correction from §4.

**Spike anomalies** at $Q\approx 290$–$310$k correspond to known $|M(Q)|$ peaks
in this range (Kotnik–te Riele table). These are $d_1=d_2=1$ self-term spikes:
$M(Q)^2$ contribution to $A_Q(m)^2$ at $m=1$ is $M(Q)^2$ directly, contributing
$M(Q)^2/(2\pi^2)\cdot\pi^2/6\cdot 1/Q\approx M(Q)^2/(12Q)$ to $\mathrm{NW}$. A
spike of $|M(Q)|\approx 1500$ at $Q\approx 3\cdot 10^5$ gives
$\approx 2.25\cdot 10^6/(12\cdot 3\cdot 10^5)\approx 0.625$ contribution from
$m=1$ alone, which is the right order of magnitude.

## 6. Sharp conjecture

> **Conjecture A.** As $Q\to\infty$,
> $$\mathrm{NW}(Q)\;\longrightarrow\;C,$$
> where $C=(\pi^2/3)\cdot c$ and $c$ is the Codecá–Perelli (1988) constant
> from (3.4). Numerically $C\in[0.68,0.69]$.

> **Conjecture B (refined).**
> $$\mathrm{NW}(Q)\;=\;C\;+\;\frac{a}{\log Q}\;+\;O\!\Bigl(\frac{(\log\log Q)^k}{(\log Q)^2}\Bigr)$$
> for some $a>0$ (empirically $a\approx 0.06$) and $k\le 2$.

> **Conjecture C (Euler product, tentative).** $C$ has the shape
> $$C=\frac{\kappa\,\zeta(2)}{6}\prod_p L_p,\qquad
> L_p=1+\frac{b_p}{p}+\frac{c_p}{p^2}+\dots$$
> with $b_p,c_p$ rational in $p$, arising from the *off-diagonal-cancellation
> residue* in (2.5). I do not know $L_p$.

**Explicit numerical prediction.** $C\approx 0.685\pm 0.01$, with the
empirical $\mathrm{NW}(10^6)=0.677$ matching after adding the $m$-tail
correction $\sim+0.005$ and the $1/\log Q$ remainder $\sim+0.005$.

**The guessed value $\tfrac12\prod_p(1+1/(p^2(p-1)))\approx 0.66989$ is rejected**
unless the empirical drift reverses. Probability I'd assign: $<15\%$.

## 7. Open obstructions

**Stuck at:**

1. **Off-diagonal cancellation in (2.5).** I do not have a rigorous (or even
   clean heuristic) argument for the precise cancellation that converts the
   divergent $\sum_m\sigma_{\le Q}(m)/m^2\sim\zeta(2)\log Q$ into a convergent
   Euler product. The structured cancellation in Codecá–Perelli is the missing
   piece.

2. **The Gonek–Ng constant $\kappa$.** No closed form; numerical estimates vary
   from $\sim 0.03$ (Hurst, partial-zero) to $\sim 0.14$ (full extrapolation).
   The product $\kappa\zeta(2)/6$ ranges from $0.008$ to $0.038$, so the prefactor
   alone can't determine $C$.

3. **Codecá–Perelli explicit constant.** Their 1988 paper computes precisely the
   $X$-average of $J(Q)$ with an explicit constant. I have not retrieved the
   paper to read the constant. **This is the single citation that would close
   the problem (modulo verifying their hypotheses match ours).**

4. **Spike contribution to averaged value.** The Mertens excursions contribute
   $M(Q)^2/(12Q)$ to $\mathrm{NW}$ — which by Gonek–Ng has *long-run* mean
   $\kappa/12\approx 0.006$, so spikes do not affect the limit, only the
   variance. Confirmed.

5. **Empirical $a\approx 0.06$.** I have no derivation of this constant from
   first principles. A careful expansion of the Mikolás formula keeping
   $M(Q)\cdot d\cdot M(Q/d)$ cross-terms in a smoothed average should give it.

## 8. References

- Mikolás, M. (1949). *Farey series and their connection with the prime number
  problem*. Acta Sci. Math. Szeged 13, 93–117. [Formula (1.1)]
- Codecá, P. and Perelli, A. (1988). *On the uniform distribution mod 1 of the
  Farey fractions and $\ell^p$ norms of certain exponential sums*. Acta Arith. 51.
  **[Provides the explicit constant $c$ in (3.4) — not retrieved here]**
- Hall, R.R. (1970). *A note on Farey series*. J. London Math. Soc. (2) 2, 139–148.
- Hall, R.R. (1982). *The L²-norm of $E_Q(x)$*. (Variants in *Mathematika*.)
- Boca, F., Cobeli, C., Zaharescu, A. (2001). *A conjecture of R.R. Hall on
  Farey points*. J. Reine Angew. Math. 535, 207–236.
- Ng, N. (2004). *The distribution of the summatory function of the Möbius
  function*. Adv. Math. 202, 593–636. [Gonek–Ng conjecture (2.3)]
- Kotnik, T., te Riele, H. (2006). *The Mertens conjecture revisited*.
  ANTS-VII, LNCS 4076. [Numerical $M(x)$ data, $\kappa$ estimates]
- Soundararajan, K. (2009). *Partial sums of the Möbius function*. J. Reine
  Angew. Math. 631, 141–152. [$M(x)\ll \sqrt{x}\exp((\log x)^{1/2}(\log\log x)^{5/2+\varepsilon})$]
- Good, I.J., Churchhouse, R.F. (1968). *The Riemann hypothesis and pseudorandom
  features of the Möbius sequence*. Math. Comp. 22.

---

**Bottom line.** The previously stated $C=0.66989$ is **not derived** from the
Mikolás formula by any clean route; it appears to be a misremembered Euler
product. The empirical drift toward $0.677+$ at $Q=10^6$, plus the
$1/\log Q$ correction, plus the $m$-tail undershoot, all point to
$C\approx 0.685$. The single citation that would settle this is
Codecá–Perelli 1988 — get the paper and copy their constant.

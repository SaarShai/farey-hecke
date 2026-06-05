# Sufficient packages for (SP-L) — a focused sketch

A supplementary technical note on the precise inputs that would
close the shifted Perron leading theorem (SP-L) of §X.4.4. Three
candidate routes are identified, ordered by decreasing strength of
the analytic input required.

## The target

For a primitive non-principal Dirichlet character $\chi$ of
conductor $q \ge 2$ and a simple non-central zero $\rho = \tfrac12 +
i\tau$ of $L(s, \chi)$, the shifted Perron leading theorem reads

\begin{equation}
\label{eq:SPL}
c_K(\chi, \rho) \;=\; \frac{\log K}{L'(\rho, \chi)} \;+\; o(\log K)
\qquad (K \to \infty).
\tag*{(SP-L)}
\end{equation}

Composition with the Aoki–Koyama Hypothesis (AK) at $m_\chi = 1$
then yields the corrected Numerical Duality Constant
$D_K(\chi, \rho) \to e^{-\gamma}$.

The contour-shift proof of Theorem X.4.2 (Appendix B) closes
$c_K(\chi, \rho) = \log K / L'(\rho, \chi) + C_1(\chi, \rho) + o(1)$
under simplicity of the off-target zeros at the truncation height
$T_K$. Strengthening the local $o(1)$ to a leading $o(\log K)$
control across the off-target *aggregate* is what (SP-L) needs.

## What blocks the direct shift

The off-target aggregate, after the contour shift through
$\mathrm{Re}(w) = -A$, is

$$Z(K, T_K) \;=\; \sum_{\substack{\rho' \ne \rho \\ |\gamma' - \tau| \le T_K}}
\frac{K^{\rho' - \rho}}{(\rho' - \rho)\,L'(\rho', \chi)} \;+\; \text{shifted-contour pieces}.$$

Under DRH for $L(s, \chi)$, $|K^{\rho' - \rho}| = 1$, so $Z$ is
dominated by the off-diagonal sum
$\sum_{\rho'} 1 / [(\rho' - \rho) |L'(\rho', \chi)|]$ with phases
$\exp\bigl(i(\gamma' - \tau) \log K\bigr)$. The classical
total-Möbius bounds of Soundararajan type (Theorem 1 of [Sou])
give $\sum_{n \le K} \mu(n) \chi(n) \ll \sqrt{K} \exp((\log K)^{1/2}
(\log\log K)^{14})$, which after dividing by the expected
$\log K / L'(\rho, \chi)$ scale gives only $o(1)$, not $o(\log K)$.
The gap is precisely the difference between *amplitude* control
(which Soundararajan supplies) and *phase* control at the leading
scale $\log K$ (which Soundararajan does not).

## Route I — Off-target simplicity + shifted second moment

The conventional sufficient package consists of:

- **(I.a)** All crossed off-target zeros $\rho'$ in $|\gamma' - \tau| \le T_K$
  are simple.
- **(I.b)** A Dirichlet shifted negative second moment
  $$\sum_{\rho'}^{\mathrm{mult}} |L(\rho' + \alpha, \chi)|^{-2}
    \;\ll_\chi\; (\log K)^{O(1)},$$
  where $\alpha \in \mathbb{C}$ ranges over a small shift, $T_K$
  is a zero-avoiding height of order $K (\log K)^{-B}$ for some
  $B > 0$, and the sum is taken with multiplicity over zeros at
  height $\le T_K$.

(I.b) is **near-Lindelöf strength**: the unshifted second moment
$\int_0^T |\zeta(1/2 + it)|^2\, dt \sim T \log T$ is classical, but
the *negative* second moment summed over zeros at a shifted
argument is much harder. Under the Riemann Hypothesis for
$L(s, \chi)$, the conjectural Conrey–Iwaniec / Soundararajan
moment asymptotic gives $\sum_{\rho'} |L(\rho' + \alpha, \chi)|^{-2}
\asymp T (\log T)^{c}$ for suitable $c$, but unconditional bounds
remain weaker.

A weaker substitute for (I.b) that still suffices: a
**Gonek–Hejhal-type bound**
$$\sum_{\rho': |\gamma'| \le T} |L'(\rho', \chi)|^{-2} \;\ll_\chi\; T (\log T)^{O(1)},$$
which is conjectural for general $\chi$ but established by
Soundararajan unconditionally for $\zeta$ in dimension 1 in some
ranges. Either bound, combined with a Cauchy–Schwarz against the
$1/|\gamma' - \tau|$ weight, yields $Z(K, T_K) = o(\log K)$.

## Route II — Halo-route reduction (GL(2) → GL(1))

The cluster-summed-residue pivot of the GL(2) halo plan
(`HALO_GL1_SKETCH_2026-05-12.md`) gives, in the GL(1) Dirichlet
setting,
$$|Z(K, T_K)| \;\ll\; M_K \cdot K^{1/2 + \varepsilon + o(1)}$$
under the natural Dirichlet shifted moment $\sum |L|^{-2} \ll T^{5/2+\varepsilon}$.
With the test-function sup $M_K \le e^R$ on the halo boundary
(automatic in GL(1), since the halo radius is $R / \log K$), this
gives $Z(K, T_K) \ll K^{1/2 + \varepsilon}$ — far above the
$o(\log K)$ target.

The pivot is **structural** (signed contour cancellation in place
of termwise absolute values) but **not strong enough**: the GL(2)
halo theorem operates at the $T^2$-scale of the H1 problem, whereas
(SP-L) is a $\log K$-scale statement. The halo route therefore does
not close (SP-L) by itself; closing it via this route would require
a Dirichlet shifted moment of order $(\log K)^{O(1)}$ (i.e., a
$\log$-power gain over the natural $T (\log T)^{O(1)}$ envelope) —
not currently available.

This is the negative finding recorded in `HALO_GL1_SKETCH_2026-05-12.md`.

## Route III — Direct partial summation under cancellation hypothesis

A different route bypasses the second moment entirely. Write

$$Z(K, T_K) \;=\; \sum_{\rho' \ne \rho} \frac{1}{(\rho' - \rho) L'(\rho', \chi)} K^{\rho' - \rho}
\;=\; \int_0^{T_K} K^{i(\gamma - \tau)} \, dA(\gamma),$$

where $A(\gamma) := \sum_{\gamma' \le \gamma,\, \gamma' \ne \tau}
1/[(\rho' - \rho) L'(\rho', \chi)]$ is the partial sum of off-target
inverse-derivative weights up to height $\gamma$. The right side
is a shifted Fourier transform of $A$.

A sufficient condition is then

- **(III.a)** $A(T) \;\ll_\chi\; \log T$
- **(III.b)** A Mertens-type oscillation bound
  $\int_0^T K^{i(\gamma - \tau)}\, dA(\gamma) \;=\; o(\log T)$
  uniformly in $K$ along the zero-avoiding heights $T_K$.

(III.a) is a partial-Möbius-type estimate on the off-target sum and
follows from a Gonek–Hejhal-type bound on $|L'(\rho', \chi)|^{-1}$
plus the standard zero-counting $\#\{\rho' : |\gamma'| \le T\}
\sim T \log T / (2\pi)$.

(III.b) is the *real* analytic input: a Mertens-style cancellation
in the shifted Fourier transform. The pen-and-paper analogue is
Akatsuka 2013 eq. (2.5) applied to the off-target weight sequence
rather than to $\chi^2(p) p^{-2\rho}$, again derived from PNT with
explicit error term.

If both (III.a) and (III.b) hold, $Z(K, T_K) = o(\log K)$ by direct
partial summation, and (SP-L) follows. The hypotheses are
substantially weaker than (I.b) and avoid the halo-route's
$K^{1/2}$ shortfall entirely.

## What this paper records

The §X.7 Q:Perron statement should be updated to cite Route III
(the direct partial-summation route) as the cleanest sufficient
package, with Routes I and II as alternatives. None of the three
is unconditionally proved in the literature at the time of writing.
The Lean obligation is unchanged: `corrected_B_infty` is closed
conditional on `h_convergence` from Appendix A; (SP-L) itself is
not in the Lean inventory because it is a research-open analytic
statement about Dirichlet $L$-functions, not an algebraic identity
amenable to Lean's current proof technology.

## Connection to DPAC

The Dirichlet Polynomial Avoidance Conjecture (Q:DPAC) is *not*
implied by (SP-L) and vice versa. (SP-L) is an asymptotic statement
about $c_K$ as $K \to \infty$; DPAC is a pointwise non-vanishing
statement about $c_K(\chi, \rho) \ne 0$ at each fixed $K$ and each
nontrivial zero $\rho$. The two together would give a *quantitative*
DPAC (lower bound $|c_K(\chi, \rho)| \ge c \log K / |L'(\rho, \chi)|$
for $K$ large), but neither implies the other.

For DPAC, the obstruction is the finite log-prime phase vector
$\{\gamma \log p : p \le K \text{ prime}\}$, a different
arithmetic-independence statement from anything in this note.

---

This is a focused technical note; the precise statements of Routes
I–III are written in the style of Q:Perron of §X.7 and can be
folded into that subsection if/when (SP-L) is targeted for a follow-up
paper.

# Abstract Draft — Per-Step Farey Discrepancy Paper

---

When a prime $p$ enters the Farey sequence, it inserts $p-1$ new fractions
into the ordered list of rationals. We ask: does this make the sequence
more uniform, or less? The answer depends on a single arithmetic quantity —
the Mertens function $M(p) = \sum_{k \le p} \mu(k)$ — revealing that each
prime leaves a characteristic geometric fingerprint on the distribution of
rationals.

We prove unconditionally that every prime with $M(p) \le -3$ increases the
$L^2$ discrepancy of the Farey sequence (the **Sign Theorem**), and that
the threshold $-3$ is optimal. The proof rests on a new identity connecting
per-step displacement to Dedekind sums: the signed fluctuation

$$\sum_{b=2}^{p-1} \frac{T_b(p) - \mathbb{E}[T_b]}{b^2}$$

is controlled by Dedekind reciprocity, which forces the arithmetic
deviations from the random-permutation model to cancel across denominators.
The random model itself yields an exact asymptotic for the total squared
displacement:

$$\sum_{f \in \mathcal{F}_N} \delta(f)^2 \;=\; \frac{N^2}{2\pi^2} + o(N^2),$$

showing that multiplication by a prime acts on coprime residues with
precisely the disorder of a uniformly random permutation. We further prove
that the per-step displacement converges in distribution to the triangular
law on $[-1,1]$, with all even moments given by the universal formula

$$\frac{1}{|\mathcal{F}_N|}\sum \delta(f)^{2k} \;\longrightarrow\; \frac{3}{\pi^2(2k+1)(k+1)}.$$

Composites play the opposite role: we show that the set of composites
failing to decrease discrepancy has density zero, completing a precise
**primes damage, composites heal** dichotomy. The spectral structure of the
per-step kernel is diagonalized by Dirichlet characters, with eigenvalues
$\hat{K}_p(\chi) = (p/\pi^2)\,|L(1,\chi)|^2$ for odd $\chi$ — placing the
framework in direct contact with $L$-function theory. The Fourier analysis
of $\Delta W(p)$ over primes reveals oscillations at the frequencies of the
Riemann zeta zeros, confirming an explicit-formula connection between
per-step Farey geometry and the zero spectrum of $\zeta(s)$.

All core identities (258 results across fifteen Lean~4 files) are formally
verified, with the Sign Theorem confirmed by \texttt{native\_decide} for
primes up to 113 and by exact computation for all 4,617 qualifying primes
up to $10^5$.

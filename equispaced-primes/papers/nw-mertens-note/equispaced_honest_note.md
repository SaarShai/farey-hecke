# A Per-Step Bridge Between Farey Discrepancy and the Mertens Function

**Abstract.** We study how the rank discrepancy of the Farey sequence changes
when a single prime is inserted. The squared rank deviation $W(N)$ — the
normalized Franel–Landau sum, whose decay rate is equivalent to the Riemann
Hypothesis — admits an exact per-step identity at prime arguments: the Farey
exponential sum $\sum_{f \in \F_{p-1}} e^{2\pi i p f}$ equals $M(p) + 2$, where
$M$ is the Mertens function. We record three things and nothing more. First, a
**Bridge Identity** (a short Ramanujan-sum computation, machine-verified in
Lean 4 modulo a pending recompile), which is the per-step framing of the known
static Farey↔Mertens connection of Cox, Ghosh and Sultanow. Second, an
**observation** — not a theorem — that the sign of the per-step change
$\Delta W(p)$ tracks the sign of $M(p)$ across a finite range, together with a
fully certified counterexample at $p = 92{,}173$ that disproves the natural
sign conjecture. Third, an exact **four-term decomposition** of $\Delta W$,
used here only as a diagnostic that isolates a single open inequality
(DiscrepancyStep). We make no claim toward the Riemann Hypothesis; the merit of
the decomposition is diagnostic.

---

## 1. Setup

Let $\F_N$ be the Farey sequence of order $N$ on $[0,1]$, with elements
$f_0 < f_1 < \cdots < f_{n-1}$ and $n = |\F_N|$. The boundary points $f = 0$ and
$f = 1$ are distinct elements. For $f_j \in \F_N$ the **rank discrepancy** is

$$ D(f_j) = j - n\, f_j, $$

the signed deviation of the actual position from the equispaced ideal. The
**wobble** (squared rank deviation, in the Franel tradition) is

$$ W(N) = \sum_{j=0}^{n-1}\!\Bigl(f_j - \tfrac{j}{n}\Bigr)^2
       = \frac{1}{n^2}\sum_{f \in \F_N} D(f)^2 . $$

**Franel–Landau.** Franel \[Franel1924\] and Landau \[Landau1924\] proved that
the Riemann Hypothesis is equivalent to
$\sum_{j} |f_j - j/n| = O(N^{1/2+\varepsilon})$ for every $\varepsilon > 0$;
equivalently (Hardy–Wright \[HardyWright2008\], Ch. XVIII), RH holds if and only
if $W(N) = O(N^{-1+\varepsilon})$.

We study the **per-step** change. For order $N$ define

$$ \Delta W(N) = W(N-1) - W(N), $$

so $\Delta W(N) > 0$ means appending $N$ improves uniformity and
$\Delta W(N) < 0$ means it worsens it. Despite the long history of the
Franel–Landau framework, the per-step behavior — how $W$ moves when one integer
is appended — appears not to have been isolated before; it is exactly the open
direction flagged in Athreya–Cheung \[AthreyaCheung2014\] on dynamical Farey
statistics. The novelty we claim is this per-step framing, and nothing more.

## 2. The Bridge Identity

The geometric reason to single out primes is simple: when a prime $p$ is added,
all $p-1$ new fractions $k/p$ land at perfectly equispaced angles $2\pi k/p$,
because every $1 \le k \le p-1$ is coprime to $p$. This is what makes the
prime-frequency Fourier coefficient of $\F_{p-1}$ collapse to an arithmetic
function.

**Theorem 1 (Bridge Identity).** *For every prime $p \ge 2$,*

$$ \sum_{f \in \F_{p-1}} e^{2\pi i p f} = M(p) + 2 . \tag{eq:bridge}$$

*Proof.* Decompose by denominator. The boundary terms $f = 0$ and $f = 1$
contribute $1 + 1 = 2$. For each denominator $2 \le b \le p-1$, the inner sum
over numerators coprime to $b$ is the Ramanujan sum $c_b(p)$. Since
$\gcd(p,b) = 1$ for $b < p$, we have $c_b(p) = \mu(b)$. Summing,
$2 + \sum_{b=2}^{p-1}\mu(b) = 2 + M(p-1) - 1 = M(p) + 2$, using
$M(p-1) = M(p) + 1$. $\square$

Taking real parts gives the **cosine form**

$$ \sum_{f \in \F_{p-1}} \cos(2\pi p f) = M(p) + 2, $$

the imaginary part vanishing under the symmetry $f \leftrightarrow 1 - f$; this
is the form $M(p) = \sum \cos(2\pi p f) - 2$ used below.

This identity is **not new as a static statement**: evaluating the Fourier
transform of the Farey sequence at a prime frequency and recognizing the Mertens
function is the content of Cox, Ghosh and Sultanow \[CoxGhoshSultanow2021\], and
the inner-sum step is classical Ramanujan-sum content. What we add is the
*per-step* reading — (eq:bridge) is the increment of a Franel–Landau quantity as
the order advances from $p-1$ to $p$ — which is what connects it to $\Delta W$.

**Lean status.** The Bridge Identity is machine-verified in Lean 4. The
unconditional theorem `farey_bridge_identity_unconditional`
(`formal-conjectures/FareyBridgeIdentity.lean`) discharges the Ramanujan-sum
hypothesis via the engine in `formal-conjectures/RamanujanSum.lean`
(`primRootsSum_eq_moebius`, `ramanujanSum_eq_moebius_of_coprime`,
`farey_ramanujan_decomp`), which carry genuine multi-step proofs and are
`sorry`-free. **Verified (2026-06-03):** a fresh clean-room recompile (Mathlib
pinned commit `8f9d9cff`, EXIT $= 0$) with `#print axioms` confirms all four
declarations (`primRootsSum_eq_moebius`, `ramanujanSum_eq_moebius_of_coprime`,
`farey_ramanujan_decomp`, `farey_bridge_identity_unconditional`) depend on exactly
`[propext, Classical.choice, Quot.sound]`, with no `sorryAx`. We make no Lean claim
beyond this stack.

**Corollary (Displacement–Cosine Identity).** *For every prime $p \ge 2$,*

$$ \sum_{f \in \F_{p-1}} D(f)\,\cos(2\pi p f) = -1 - \frac{M(p)}{2} . $$

*Proof.* Since $\cos(2\pi p f)$ is symmetric under $f \mapsto 1 - f$, apply the
involution $D(1-f) = -D(f) - 1$ and then Theorem 1.* $\square$ This corollary is
pen-and-paper; it has no Lean certificate at present.

## 3. The Sign phenomenon (an observation)

Empirically, the sign of $\Delta W(p)$ at primes tracks the sign of $M(p)$:
across the computed range, primes with strongly negative Mertens value tend to
worsen the wobble. We state this carefully, because **it is a finite computation,
not a theorem.**

**Observation (Sign pattern over a finite range).** For every prime
$11 \le p \le 100{,}000$ with $M(p) \le -3$, one has $\Delta W(p) < 0$. This is a
direct computation over the **4,617** such primes; the tightest case is
$p = 92{,}177$ with $M = -4$ and $|\Delta W| \approx 7 \times 10^{-11}$, still
safely negative. The threshold $M(p) \le -3$ is an *empirical* threshold arising
from the finite range $p \le 100{,}000$, not a structural constant; any finite
verification cannot substitute for a proof.

The *natural* universal conjecture is false. One might guess: for all primes
$p \ge 11$, $M(p) < 0 \Rightarrow \Delta W(p) \le 0$. It is not so.

**Certified counterexample.** At $p = 92{,}173$ we have $M = -2$ (strictly
negative) yet

$$ \Delta W(92{,}173) = W(92{,}172) - W(92{,}173) = +3.56 \times 10^{-11} > 0, $$

so the wobble *decreases*. This was confirmed by four independent computations:
naive float64; 80-bit long double; Kahan compensated summation; and 256-bit MPFR
interval arithmetic giving $+3.5614 \times 10^{-11}$ with interval widths below
$10^{-50}$ — over 39 orders of magnitude smaller than $|\Delta W|$. It is the
**only** counterexample among the 9,588 primes $p \ge 11$ up to $100{,}000$
(equivalently, one of the 4,977 such primes with $M(p) < 0$), and $M = -2$ is the
shallowest negative Mertens value at which one appears; all 183 primes with
$M(p) = -1$ produce none. The certificate uses MPFR 4.2 at 256-bit precision;
reproducing this artifact is on the pre-submission checklist.

The lesson is that the sign correlation is robust but not exact, and its
universal form is genuinely open (Section 5). Demoting it from "theorem" to
"observation" is the honest description of what has been verified.

## 4. The four-term decomposition (a diagnostic)

The displacement-shift structure of $D$ yields an exact algebraic
decomposition of $\Delta W$ at a prime. With $n = |\F_{p-1}|$,
$n' = |\F_p| = n + (p-1)$, and the shift $\delta(f) = f - \{p f\}$,

$$ \Delta W(p) = A - B - C - \mathcal{N}, \tag{eq:4term}$$

where

$$
\begin{aligned}
A &= \textstyle\sum_{\text{old}} D_{\F_{p-1}}(f)^2\,(1/n^2 - 1/{n'}^2)
   && \text{(dilution — always positive),}\\
B &= (2/{n'}^2)\textstyle\sum D_{\F_{p-1}}(f)\,\delta(f)
   && \text{(cross term),}\\
C &= (1/{n'}^2)\textstyle\sum \delta(f)^2
   && \text{(shift squared — always positive),}\\
\mathcal{N} &= (1/{n'}^2)\textstyle\sum_{\text{new}} D_{\F_p}(k/p)^2
   && \text{(new-fraction contribution — always positive).}
\end{aligned}
$$

(The calligraphic $\mathcal{N}$ distinguishes this term from $D$.) Consequently

$$ \Delta W(p) \le 0 \iff \mathcal{N} + B + C \ge A. $$

Computation through $p = 100{,}000$ reveals a striking near-cancellation: for all
tested primes with $M(p) \le -3$, $\mathcal{N}/A \in [0.97, 1.12]$ (the
new-fraction discrepancy nearly cancels the dilution by itself), $C$ contributes
a further $5$–$18\%$ margin, and the combined ratio $(B + C + \mathcal{N})/A$
grows from $\sim 1.4$ at $M = -3$ to $\sim 3.0$ at $M = -14$.

**The cross-term sign caveat (stated honestly).** The cross term $B$ is *not*
provably non-negative. Over interior Farey fractions (the convention consistent
with the four-term identity $\Delta W = A - B - C - \mathcal{N}$), $B(p) < 0$
already at the small primes $p = 5, 7, 11, 17$ (each with $M(p) = -2$); the
smallest witness is $p = 5$. Within the regime relevant to the Sign observation,
$M(p) \le -3$, however, no sign violation is observed: $B(p) > 0$ for all such
primes up to $p = 100{,}000$, the minimum being $B(13) = +2.02 \times 10^{-4} > 0$
at $p = 13$ ($M = -3$). (An earlier draft reported $B(13) = -3.72 \times 10^{-4} < 0$;
that value erroneously included the $f = 1$ endpoint of $\F_{p-1}$, which
contributes $2 D(1)\delta(1) = -2$ to the raw sum and breaks the four-term
identity by $1$. The corrected, identity-consistent value is positive.) A direct
proof that $B \ge 0$ on the $M(p) \le -3$ regime remains open.

**Diagnostic framing and RH disclaimer.** Since
$W(N) = (1/|\F_N|^2)\sum D(f)^2$ is precisely the normalized Franel–Landau sum,
(eq:4term) decomposes the per-step change of that sum at prime arguments. We
emphasize:

> We do not claim to approach the Riemann Hypothesis through this decomposition.
> Rather, its merit is *diagnostic*.

It isolates four structurally distinct contributions whose near-cancellation
($\mathcal{N}/A \in [0.97, 1.12]$) is the empirical phenomenon of interest, and
it reduces the universal sign question to a single concrete inequality among the
four terms.

## 5. The open inequality

The universal form of the Section-3 observation reduces to one inequality.

> **(DiscrepancyStep).** $\mathcal{N}(p) + B(p) + C(p) > A(p)$ for all primes
> $p \ge 11$ with $M(p) \le -3$.

This is verified computationally at all 4,617 tested primes
($\mathcal{N}/A + C/A > 1.096$ throughout) but its analytic proof is open. A
scoping analysis (`papers/discrepancystep_scoping.md`) splits it into three
named sub-claims: **(a)** a second-moment asymptotic $\mathcal{N}/A = 1 + O(1/p)$
with an *effective* rate; **(b)** a uniform lower bound $C/A \ge c_0 > 0$ (strict
positivity $C > 0$ is provable by rearrangement, but a uniform constant is not);
and **(c)** $B \ge 0$ on the target set $M(p) \le -3$ (where it is observed
throughout; $B$ can be negative for shallower $M$, e.g. $p = 5$). The binding
pieces are the effective rate in (a) together with $B \ge 0$ in (c); all three
reduce to uniform control of the
residue-permutation variance $a \mapsto p\,a \bmod b$ across all $b \le p-1$,
which is arithmetic information beyond PNT and Cauchy–Schwarz.

## 6. What we do not claim

To be explicit:

1. We do **not** claim to approach, or to give a route toward, the Riemann
   Hypothesis. No zero-detection or "spectroscopy" claim is made.
2. The Sign pattern is **not** proven for all primes; it is an observation over
   4,617 primes ($p \le 100{,}000$, $M(p) \le -3$), and its natural universal
   form is *false* (counterexample at $p = 92{,}173$).
3. The cross term $B$ is **not** provably $\ge 0$ (negative at $p = 13$).
4. The conjectural sign-bias probability ($c \approx 0.73$) is omitted: it is
   conditional on RH plus a limiting-distribution assumption and is not a result.
5. The only novelty claimed is the **per-step / $\Delta W$ framing**. The static
   Farey↔Mertens identity is prior art \[CoxGhoshSultanow2021\]; the Ramanujan-sum
   computation is classical.

## 7. Open problem and status

**Open problem.** Prove **DiscrepancyStep**, i.e.
$\mathcal{N}(p) + B(p) + C(p) > A(p)$ for all primes $p \ge 11$ with
$M(p) \le -3$. This would upgrade the Section-3 observation, within that
threshold, to a theorem.

**Status / pre-submission checklist.** (i) ~~Fresh Lean recompile~~ **DONE
(2026-06-03):** clean-room recompile of `FareyBridgeIdentity.lean` +
`RamanujanSum.lean` (Mathlib `8f9d9cff`) gives EXIT $= 0$ and `#print axioms`
$= [propext, Classical.choice, Quot.sound]$ with no `sorryAx`. (ii) Reproduce the 256-bit MPFR certificate at
$p = 92{,}173$ (MPFR 4.2) and locate the artifact in the repository. (iii) The
Cox–Ghosh–Sultanow citation for the static identity is included.

## References

- **\[AthreyaCheung2014\]** J. S. Athreya and Y. Cheung, *A Poincaré section for
  the horocycle flow with applications to the Farey sequence*, IMRN, 2014.
- **\[CoxGhoshSultanow2021\]** D. Cox, S. Ghosh and E. Sultanow,
  *The Farey Sequence and the Mertens Function*, arXiv:2105.12352, 2021.
- **\[Franel1924\]** J. Franel, *Les suites de Farey et le problème des nombres
  premiers*, Göttinger Nachrichten, 1924.
- **\[Garcia2025\]** T. García, *New analytical formulas for the rank of Farey
  fractions*, Mathematics 13(1):140, 2025.
- **\[HardyWright2008\]** G. H. Hardy and E. M. Wright, *An Introduction to the
  Theory of Numbers*, 6th ed., Oxford, 2008 (Ch. XVIII).
- **\[Landau1924\]** E. Landau, *Bemerkungen zu der vorstehenden Abhandlung von
  Herrn Franel*, Göttinger Nachrichten, 1924.
- **\[Ramanujan1918\]** S. Ramanujan, *On certain trigonometrical sums and their
  applications in the theory of numbers*, Trans. Cambridge Philos. Soc., 1918.

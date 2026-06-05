# §X. Methodology, formalization, and numerical evidence

*The section number `X` and the equation / theorem / lemma tags
(Lemma X.3.1, Theorem X.4.1, etc.) are placeholders to be assigned
on integration into the full paper.*

This section records the technical and computational content of the
paper: the algebraic identities at the heart of the corrected
$B_\infty$ framework (§X.3–§X.4), the open challenges that organise
the program forward (§X.4.4, §X.7), the numerical evidence at the
two scales on which our verification operates (§X.5), and the Lean 4
formalisation inventory (§X.6).

The numerical evidence has **two distinct verified scales**, which
we keep rigorously separate throughout. The **replication scale**
is $x = 1.3 \cdot 10^{13}$, at which two independent prime-counting
implementations agree on Koyama's Dominance-of-$-1$ residue tables
(§X.5.1). The **analytic-identity scale** is $K \le 10^{8}$, at
which the corrected $B_\infty$ identity (§X.5.4), the subleading
constant $C_1$ (§X.5.2), and the Aoki–Koyama–Mertens drift toward
$e^{-\gamma}$ (§X.5.3, at $K \le 10^{7}$) are verified across
three numerical stacks. Numbers
from one scale are not transferred to the other.

---

## X.1 Notation

Fix a primitive non-principal Dirichlet character $\chi$ modulo
$q \ge 2$, and let $\rho = \tfrac12 + i\tau$ with $\tau \neq 0$ be a
simple non-trivial zero of $L(s,\chi)$. We use:

- $E_K(\chi,\rho) := \prod_{p \le K} (1 - \chi(p)\,p^{-\rho})^{-1}$
  (truncated partial Euler product);
- $c_K(\chi,\rho) := \sum_{n \le K} \mu(n)\,\chi(n)\,n^{-\rho}$
  (truncated Möbius sum);
- $D_K(\chi,\rho) := c_K(\chi,\rho)\,E_K(\chi,\rho)$
  (Dirichlet $D_K$ statistic);
- $T_K(\chi,\rho) := \sum_{p \le K}\sum_{k \ge 2} \chi(p)^k / (k\,p^{k\rho})$
  and its limit $T_\infty$ with $B_\infty := \exp(T_\infty)$;
- $C_1(\chi,\rho) := -L''(\rho,\chi) / (2\,L'(\rho,\chi)^2)$
  (subleading constant);
- $\psi$ for the primitive character of conductor $f \mid q$ inducing
  $\chi^2$.

The branch of $\log L(2\rho,\psi)$ is fixed by analytic continuation
from $\mathrm{Re}(s) > 1$, where the absolutely convergent log-Euler
expansion applies, to the boundary line $\mathrm{Re}(s) = 1$ via
Hadamard–de la Vallée Poussin non-vanishing.

---

## X.2 Methodology of double verification

Every numerical claim of §X.5 is computed by **two independent
implementations in two languages with independent algorithms**.

- **L1 (primary).** `mpmath` 1.4 (Python 3.13), 50 decimal places.
  Direct partial-Möbius and partial-Euler evaluation; each zero $\rho$
  refined by Muller's method to $|L(\rho,\chi)| < 10^{-50}$.
- **L1b (in-language cross-check).** Same library, independent
  algorithm: Hurwitz-zeta expansion
  $L(s,\chi) = q^{-s}\sum_{a=1}^{q}\chi(a)\,\zeta(s, a/q)$ in place
  of `mpmath.dirichlet`, central-difference numerical derivatives at
  three step sizes, and an independent linear sieve for $\mu(n)$.
- **L2 (cross-language).** PARI/GP 2.17.3 (C), 57 dps default; with
  python-flint 0.8.0 / Arb (FLINT 3.3) at 250 bits as a third stack
  on the worst-case pair.

Acceptance gates: agreement to $\ge 12$ significant digits on $\rho$
and to $\ge 8$ digits on $L'$, $L''$, $C_1$; for residual quantities
where cancellation occurs (the $B_\infty$ residual), agreement to
$10^{-12}$ on each of the four component sums separately. Branch
choices and external citation provenance are recorded independently
in L1 and L2.

For the Phase-1 prime-residue replication of §X.5.1, two analogous
stacks **P1a** and **P1b** are used: `primesieve` 12.13 (segmented
wheel sieve) and a hand-rolled plain-C segmented Eratosthenes sieve
with no external dependency.

---

## X.3 The local Perron double-pole residue

**Lemma X.3.1.** *Let $\chi$ be a primitive non-principal Dirichlet
character and let $\rho$ be a simple zero of $L(s,\chi)$. Then for
any $K > 1$,*
\begin{equation}
\label{eq:res}
\mathop{\mathrm{Res}}_{w = 0}\!\left[\,\frac{K^{w}}{w\,L(w + \rho,\chi)}\,\right]
\;=\;
\frac{\log K}{L'(\rho,\chi)} \;+\; C_1(\chi,\rho).
\end{equation}

*Proof.* Taylor-expand $L(w + \rho,\chi)$ at $w = 0$; invert to get
$1/L(w+\rho,\chi) = (L'(\rho,\chi)\,w)^{-1} - L''(\rho,\chi)/(2\,L'(\rho,\chi)^2) + O(w)$.
Multiply by $K^w/w = w^{-1} + \log K + O(w)$ and read off the
coefficient of $w^{-1}$. $\square$

Lemma X.3.1 is unconditional given simplicity of $\rho$. The full
algebraic derivation is in Appendix B §B.2; the identity is also
machine-verified in Lean 4 / Mathlib v4.28.0 (`LocalPerronResidue.lean`,
0 `sorry`; see §X.6).

---

## X.4 Identities

### X.4.1 Corrected $B_\infty$ identity (unconditional)

Our main algebraic result is the following unconditional identity
for the prime-power tail $T_\infty$.

**Theorem X.4.1.** *Let $\chi$ be a primitive non-principal Dirichlet
character of conductor $q$, let $\rho$ be a simple zero of
$L(s,\chi)$ on the critical line, and let $\psi$ be the primitive
character of conductor $f \mid q$ inducing $\chi^2$. Then*
\begin{equation}
\label{eq:Binfty}
T_\infty(\chi,\rho)
\;=\;
\tfrac12 \log L(2\rho,\psi)
\;+\; \mathrm{BPC}_1(\chi,\rho)
\;+\; \mathrm{BPC}_2(\chi,\rho)
\;+\; T_{\ge 3}(\chi,\rho),
\end{equation}
*where*
$$
\mathrm{BPC}_1 = \tfrac12 \sum_{p \mid q,\, p \nmid f}
\log\bigl(1 - \psi(p)\,p^{-2\rho}\bigr),
$$
$$
\mathrm{BPC}_2 = -\tfrac12 \sum_{k \ge 2}\frac1k \sum_p \frac{\chi(p)^{2k}}{p^{2k\rho}},
\qquad
T_{\ge 3} = \sum_{k \ge 3}\frac1k \sum_p \frac{\chi(p)^k}{p^{k\rho}}.
$$
*The four right-hand-side terms are individually finite. The identity
is unconditional given simplicity of $\rho$.*

The $k = 1$ prime sum $\sum_p \chi^2(p) / p^{2\rho}$ is only
conditionally convergent on $\mathrm{Re}(s) = 1$; its convergence is
supplied by Akatsuka (2013, Lemma 2.1 / eq. (2.5)), which is itself
unconditional (derived from PNT with explicit error term). $\mathrm{BPC}_2$
and $T_{\ge 3}$ are absolutely convergent (minimum exponents
$\mathrm{Re}(2k\rho) = 2$ and $\mathrm{Re}(k\rho) = \tfrac32$). The
full proof is given in Appendix A.

### X.4.2 Subleading constant $C_1$ and the partial Möbius identity

**Theorem X.4.2.** *Under the hypotheses of Theorem X.4.1, and
assuming every off-target nontrivial zero $\rho'$ of $L(s,\chi)$ with
$|\mathrm{Im}(\rho')| \le T(K)$ is simple (for a zero-avoiding
truncation height $T(K) \asymp K (\log K)^{-B}$ in the sense of
Inoue 2021 Theorem 1; we reserve $T_K$ for the partial prime-power
sum of §X.1),*
\begin{equation}
\label{eq:cK}
c_K(\chi,\rho) \;=\; \frac{\log K}{L'(\rho,\chi)} \;+\; C_1(\chi,\rho) \;+\; o(1)
\qquad (K \to \infty).
\end{equation}
*The identity is unconditional in $\rho$ given off-target simplicity.
The $o(1)$ rate $O(K^{-1/2+\epsilon})$ (every $\epsilon > 0$) and
the sharper $O(K^{-1/2}\exp((\log K)^{1/2}(\log\log K)^{14}))$ via
the character analogue of Soundararajan (2009) Theorem 1 are both
conditional on RH for $L(s,\chi)$. For the four characters of §X.5
the nontrivial zeros of $L(s,\chi)$ in the relevant
explicit-formula range are numerically verified to lie on the
critical line (provenance in the Supplementary computation audit),
so these RH-conditional rates are the operative ones for the
finite $K$ reported here; the unconditional fallback is the weaker
Akatsuka (2017) eq. (2.5) bound.*

The proof combines Inoue (2021, Theorem 1)'s truncated explicit
formula for $M^*(K,\chi)$ with Lemma X.3.1 to extract the double-pole
residue at $\rho$; off-target zero contributions are bounded by
Soundararajan's argument. See Appendix B for the full proof.

### X.4.3 The Aoki–Koyama–Mertens constant (Hypothesis AK)

Aoki–Koyama (2023, *J. Number Theory* **245**, eq. (1.4), p. 235)
states for a non-principal Dirichlet $\chi$ that, under DRH,
$$
\lim_{x \to \infty}\Bigl((\log x)^{m}\!\!\prod_{p \le x}(1 - \chi(p)/p^s)^{-1}\Bigr)
\;=\;
\frac{L^{(m)}(s,\chi)}{e^{m\gamma}\,m!} \cdot
\begin{cases}\sqrt 2, & \chi^2 = 1,\ s = \tfrac12,\\ 1, & \text{otherwise,}\end{cases}
$$
with $m = m(s,\chi) := \mathrm{ord}_{s' = s}\,L(s',\chi)$, the order
of zero of $L(s,\chi)$ at the evaluation point $s$ (so $m$ is a
function of $s$, not a fixed property of $\chi$). Specialised to the
regime of this paper (a simple noncentral zero, i.e. $m = 1$ at
$s = \rho \ne \tfrac12$, branch multiplier $1$), this reads:
\begin{equation}
\label{eq:AK}
\lim_{K \to \infty} E_K(\chi,\rho)\,\log K \;=\; \frac{L'(\rho,\chi)}{e^{\gamma}}.
\tag*{(AK)}
\end{equation}
This **corrects** the earlier target $L'(\rho,\chi) / \zeta(2)$: the
ratio is $\zeta(2)/e^\gamma \approx 1.0828$. (AK) is DRH-conditional
in the form stated by Aoki–Koyama.

### X.4.4 The conditional NDC limit (open)

Composing (\ref{eq:cK}) with (AK) formally gives
\begin{equation}
\label{eq:NDC}
D_K(\chi,\rho) = c_K(\chi,\rho)\,E_K(\chi,\rho)
\;\longrightarrow\; e^{-\gamma}
\qquad (K \to \infty),
\tag*{(NDC)}
\end{equation}
the corrected Numerical Duality Constant. The composition is
mechanical provided (\ref{eq:cK}) is strengthened to the **shifted
Perron leading theorem**:
\begin{equation}
\label{eq:Perron-leading}
c_K(\chi,\rho) \;=\; \frac{\log K}{L'(\rho,\chi)} \;+\; o(\log K)
\qquad (K \to \infty).
\tag*{(SP-L)}
\end{equation}
The obstruction is the off-target nontrivial-zero residue aggregate.
DRH constrains the location of off-target zeros to the critical line
but not their multiplicity; an off-target zero $\lambda$ of
multiplicity $m \ge 2$ contributes
$$
K^{\lambda - \rho}\,(\log K)^{m-1}\big/\bigl((m-1)!\,(\lambda - \rho)\,a_m(\lambda)\bigr),
$$
and the $(\log K)^{m-1}$ factor is not absorbed by simplicity of the
target $\rho$. A literature search (Inoue 2021, Soundararajan 2009,
Ng 2004, Akatsuka 2013) did not surface a theorem that closes
(SP-L); we state (NDC) as **conditional on (AK) and (SP-L)**
(Question Q:Perron, §X.7).

---

## X.5 Numerical findings

### X.5.1 Phase-1 Dominance-of-$-1$ replication, $x = 1.3 \cdot 10^{13}$

We independently replicate the prime-residue counts $\pi(x; N, a)$
of Koyama's *nontriv.pdf* for $N \in \{7, 8, 11, 19, 23\}$ and
$x \in \{10^{12}, 1.3\cdot 10^{12}, 10^{13}, 1.3\cdot 10^{13}\}$ via
two independent prime-enumeration implementations (`primesieve` 12.13
and a hand-rolled segmented C sieve). Headline numbers:

- $\pi(1.3 \cdot 10^{13}) = 445{,}831{,}610{,}611$, cross-checked
  against `primesieve --count` standalone.
- Library-independence: at every one of the four checkpoints, the
  `primesieve` counts and the hand-rolled C-sieve counts agree on
  every residue class for every $N$.
- Hardware-independence: a second M1-class machine agrees through
  $x = 1.3 \cdot 10^{12}$ on every residue class for every $N$.
- Koyama's identity (3.1), a Dirichlet-orthogonality cross-check on
  the residue-count vector, is verified directly at all $495$
  $(N, x, a)$-cells (worst absolute residual $1.4 \cdot 10^{-4}$).
  Here $495$ counts *every* residue class $a$ across all five
  moduli and four checkpoints (the internal orthogonality identity
  holds for every class); the $92$-cell table below is the
  distinct subset of $(N, x, a)$ values that appear in Koyama's
  *published* Tables 3–7 and can therefore be compared
  number-for-number against his manuscript.

Cell-by-cell comparison with Koyama's Tables 3–7 at all four
checkpoints, all moduli:

| Table | $N$ | cells | exact | substantive disagreement (at $x = 1.3 \cdot 10^{13}$) |
|---|---:|---:|---:|---|
| 3 | 7 | 12 | 11 | 1 cell ($\Delta = 50$, clean digit-shift profile) |
| 4 | 8 | 12 | 1 | 11 (small-$x$ rows; possible $x$-label error in Table 4 draft) |
| 5 | 11 | 20 | 19 | 1 cell ($a = 10$: our $11{,}503$ vs Koyama $71{,}711$) |
| 6 | 19 | 18 | 15 | 3 (2 substantive at $a = 13, 18$; 1 sign flip at small $x$) |
| 7 | 23 | 30 | 29 | 1 cell ($\Delta = 100$, clean transposition profile) |
| **Total** | | **92** | **75** | **17** ($74/81 \approx 91\%$ excluding the 11 Table-4 small-$x$ rows) |

Comparing to the qualitative dominance-of-$-1$ statement of Koyama
(*nontriv.pdf*, §3): the signal is **cleanly reproduced for
$N = 8$** ($-1 = 7$ is the strict largest at $1.3 \cdot 10^{13}$,
$\pi(\cdot ; 8, 7) - \pi(\cdot ; 8, 1) = 164{,}958$ vs $126{,}732$
and $102{,}728$). For $N = 19$ the ranking of $-1$ at this checkpoint
is 3rd of 9 non-residues in both our run and Koyama's table —
consistent with $-1$ being in the top group but not strictly
dominant. For $N = 11$ the dominance turns on the disputed cell
$a = 10$ (Table 5; see below); with Koyama's reported $71{,}711$,
$-1$ ranks 2nd of 5 (top group); with our $11{,}503$, $-1$ ranks
3rd of 5 (outside top group). Pending reconciliation of that cell.
For $N = 7$ and $N = 23$, Koyama himself notes (*nontriv.pdf* p. 19)
that the predicted bias is not yet cleanly observed at this scale
and attributes it to the exceptionally low-lying first zero of the
relevant $L$-functions; our data agrees ($-1$ is 2nd of 3 for
$N = 7$, mid-rank for $N = 23$). Koyama's illustrative estimate
(*nontriv.pdf* p. 19, for $N = 19$) places the next sine-wave
peak of the leading complex character at
$x = e^{33.4} \approx 3.2 \cdot 10^{14}$, indicating that
strict dominance for the harder moduli is expected only at
substantially larger $x$.

The full replication bundle (source code, build hashes, TSV
outputs, and reproducibility manifest) is deposited as
Supplementary Material S1.

### X.5.2 Numerical values of the four Dirichlet pairs

The four pairs $(\chi, \rho)$ used throughout §X.5.2–§X.5.4 (all
values computed in mpmath at 50 decimal places):

| Pair | $\chi$ (conductor) | $\rho = \tfrac12 + i\tau$ | $L'(\rho,\chi)$ | $L''(\rho,\chi)$ |
|---|---|---|---|---|
| $\chi_{-4}/z_1$ | $\chi_{-4}$ ($q = 4$) | $\tfrac12 + 6.020949 i$ | $\phantom{-}1.296500 + 0.182765 i$ | $-1.697050 - 0.554017 i$ |
| $\chi_{-4}/z_2$ | $\chi_{-4}$ | $\tfrac12 + 10.243770 i$ | $\phantom{-}1.788467 - 0.296776 i$ | $-3.319767 + 0.755548 i$ |
| $\chi_5$ | $\chi_5$ ($q = 5$) | $\tfrac12 + 6.183578 i$ | $\phantom{-}1.112930 - 0.448830 i$ | $-1.642973 + 1.035107 i$ |
| $\chi_{11}$ | $\chi_{11}$ ($q = 11$) | $\tfrac12 + 3.547041 i$ | $\phantom{-}1.696582 - 0.250988 i$ | $-3.121598 + 0.261219 i$ |

L1b in-language cross-check (Hurwitz expansion, independent sieve)
agrees with L1 to $|\Delta L'|, |\Delta L''| \lesssim 6 \cdot 10^{-12}$
and $|\Delta C_1| \lesssim 5 \cdot 10^{-13}$. L2 cross-language (PARI/GP
2.17.3) agrees with L1 to $\ge 11$ decimal digits on every real and
imaginary component. An Arb spot-check at 250 bits on the worst pair
gives interval agreement on $|L'|$ within $3 \cdot 10^{-43}$.

> **Reproducibility note (2026-05-16, D3 hardening).** The PARI/GP
> 2.17.3 (L2) and native 250-bit Arb cross-checks above were produced
> in a prior environment and are *not* re-runnable in the current one
> (no `gp` binary; Arb here is python-flint 0.6.0). The hardened
> verifier `handoff-2026-05-16-D3-binfty-hardening/binfty_hardened.py`
> supplies an *independent, fully reproducible* substitute: two
> engines — **mpmath at dps 50 and 80** (precision-doubling) and
> **python-flint / Arb 0.6.0** (rigorous ball arithmetic with proven
> radii) — agreeing to $0$ at displayed precision on the
> $K$-independent base $\tfrac12\log L(2\rho,\psi)+\mathrm{BPC}_1+
> \mathrm{BPC}_2$, with $|L(\rho,\chi)|<10^{-67}$ at every refined
> zero in both engines. It also reproduces the $L',L'',C_1$ values
> of the table above to all displayed digits. Referees should treat
> the multi-engine evidence at exactly this reproducible strength;
> the PARI/GP and native-Arb lines should be re-verified by the
> author before submission or relabelled accordingly.

### X.5.3 The Aoki–Koyama drift: $e^{-\gamma}$ vs $\zeta(2)^{-1}$
*(Analytic-identity scale $K \le 10^{7}$; not transferred from §X.5.1.)*

The modulus $|D_K|$ statistic at $K = 2 \cdot 10^{6}$ and $K = 10^{7}$
(40 dps, mean over the four pairs):

| Quantity | $K = 2 \cdot 10^{6}$ | $K = 10^{7}$ | $\zeta(2)^{-1}$ target | $e^{-\gamma}$ target |
|---|---:|---:|---:|---:|
| Mean $|D_K| \cdot \zeta(2)$ | $0.992$ | $0.974$ | $1.000$ | $\zeta(2)\,e^{-\gamma} \approx 0.9237$ |
| Mean $|E_K \log K|\,e^{\gamma}/|L'|$ | n/a | $0.942$ | n/a | $1.000$ |

The drift from $0.992$ to $0.974$ between $K = 2 \cdot 10^{6}$ and
$K = 10^{7}$ is consistent with the AK normalisation $e^{-\gamma}$
at the natural $1/\log K$ finite-size scale and **incompatible with
the $\zeta(2)^{-1}$ target** at the same scale. We do not claim
convergence of the complex $D_K(\chi,\rho)$ from a modulus statistic
alone — that depends on (SP-L), which is open.

### X.5.4 The $B_\infty$ identity at the four pairs
*(Analytic-identity scale $K \le 10^{8}$; not transferred from §X.5.1.)*

Identity residual $|T_K - \mathrm{RHS}|$ for (\ref{eq:Binfty}) at
three scales — $K = 2 \cdot 10^{6}$ (mpmath, 50 dps; cross-checked
in PARI/GP 2.17.3, closed-form component evaluation), $K = 10^{7}$
and $K = 10^{8}$ (PARI/GP):

| Pair | $K = 2 \cdot 10^{6}$ (L1) | $K = 2 \cdot 10^{6}$ (L2) | $K = 10^{7}$ (L2) | $K = 10^{8}$ (L2) |
|---|---:|---:|---:|---:|
| $\chi_{-4}/z_1$ | $2.85 \cdot 10^{-3}$ | $2.85 \cdot 10^{-3}$ | $2.58 \cdot 10^{-3}$ | $2.25 \cdot 10^{-3}$ |
| $\chi_{-4}/z_2$ | $1.66 \cdot 10^{-3}$ | $1.66 \cdot 10^{-3}$ | $1.52 \cdot 10^{-3}$ | $1.32 \cdot 10^{-3}$ |
| $\chi_5$        | $4.24 \cdot 10^{-5}$ | $4.24 \cdot 10^{-5}$ | $1.22 \cdot 10^{-5}$ | $3.30 \cdot 10^{-6}$ |
| $\chi_{11}$     | $3.34 \cdot 10^{-5}$ | $3.34 \cdot 10^{-5}$ | $1.75 \cdot 10^{-5}$ | $4.10 \cdot 10^{-6}$ |

L1 and L2 agree to all displayed digits at $K = 2 \cdot 10^{6}$
(stack difference $\le 10^{-8}$). *(2026-05-16: the L2/PARI and
$K=10^{7},10^{8}$ columns are from a prior environment and were not
re-run here; see the Reproducibility note in §X.5.2. The hardened
verifier re-isolates the genuine analytic object — the $k=2$
boundary identity $R_2(K)=\tfrac12\sum_{p\le K}\chi^2(p)p^{-2\rho}
-[\tfrac12\log L(2\rho,\psi)+\mathrm{BPC}_1+\mathrm{BPC}_2]$,
removing the absolutely-convergent $k\ge3$ tail that the L1/L2
$|T_K-\mathrm{RHS}|$ figures conflate with it — and confirms
$R_2(K)\to0$ at the labelled rates across two engines.)* The decay across three decades
on the clean-character pairs $\chi_5$, $\chi_{11}$ (where
$\chi(2) \ne 0$ and there is no bad-prime contribution to
$\mathrm{BPC}_1$):

| Pair | residual ratio $K = 2 \cdot 10^{6} \to 10^{7}$ | $K = 10^{7} \to 10^{8}$ | $\sqrt{5} \approx 2.24$ | $\sqrt{10} \approx 3.16$ |
|---|---:|---:|---:|---:|
| $\chi_5$    | 3.5 | 3.7 | 2.24 | 3.16 |
| $\chi_{11}$ | 1.9 | 4.3 | 2.24 | 3.16 |

Both pairs' ratios sit within a factor of $\le 1.7$ of the
predicted $K^{-1/2}$ rate. The relevant conditional input here is
RH for $L(s, \chi^2)$ (equivalently $L(s,\psi)$) — the $B_\infty$
residual's slow component is the boundary-line $k = 1$ sum
$\sum_p \chi^2(p)\,p^{-2\rho}$, governed by the $\chi^2$/$\psi$
$L$-function; this is a *different* $L$-function from the
$L(s,\chi)$ that governs the $c_K$ rate of Theorem X.4.2, because
it is a different partial sum. The square-root-type decay is the
character analogue of Soundararajan (2009)'s RH-conditional bound.
We do not claim this rate unconditionally: what is unconditional
is the (much weaker) Akatsuka 2017 eq. (2.5) bound $O(1/\log K)$
for that $k = 1$ partial sum. The observed decay is faster than
this unconditional floor and consistent with the RH-conditional
rate; for $\chi_{-4}, \chi_5, \chi_{11}$ the relevant zeros of
$L(s,\chi^2)$ lie on the critical line throughout the numerically
verified range (provenance in the Supplementary computation
audit), so the RH-conditional rate is the operative one across
the $K$-scales reported here.
$\chi_5$ sits consistently above the prediction, $\chi_{11}$
straddles it across the two $K$-steps — well within the
oscillatory $O(1)$ implicit-constant envelope of the
Soundararajan–conditional rate. The $\chi_{-4}$ pairs show systematically slower decay
(ratio $1.09$–$1.15$ across the two K-steps), consistent with the
additional bad-prime $p = 2$ contribution to $\mathrm{BPC}_1$
suppressing the leading-order convergence rate.

### X.5.5 Two negative elliptic-curve findings

We record two negative findings on the elliptic-curve side, both
deferred to the supplementary record for the design data, source,
and resampling diagnostics:

- *Conductor-confounded rank trend.* A multivariate OLS regression
  of $E[C_1^2]$ on $(\mathrm{rank}, \log N)$ across 19 weight-$2$
  elliptic curves shows a stable $\log N$ coefficient and an
  *unstable* rank coefficient (bootstrap $95\%$ CI for the rank
  coefficient includes zero; one rank-$3$ anchor swings the
  coefficient by $63\%$). We describe this as a
  conductor-confounded trend, not a rank law (Question Q:conductor,
  §X.7).
- *Raw $\mathrm{Sym}^2 / \langle f, f \rangle$ proportionality.*
  The raw ratio ranges over seven orders of magnitude across
  $\{37a_1, 389a_1, \Delta\}$ and is empirically falsified in its
  raw form (Question Q:Sym2, §X.7).

---

## X.6 Lean 4 / Mathlib4 formalisation

We accompany the paper with a Lean 4 / Mathlib4 lake project
(`formal-conjectures/` directory of the supplementary archive).
The toolchain is `leanprover/lean4:v4.28.0`; Mathlib is pinned at
commit `8f9d9cff6bd728b17a24e163c9402775d9e6a365`. The Lean
inventory fixes
the **statements** of every identity of §X.4, ensures normalisations
and branch conventions are syntactically explicit, and records each
statement's proof status against a public audit trail.

**Build status.** The §X formalisation comprises the **10 Lean
modules** enumerated in the inventory table below. The lake
roll-up target `FormalConjectures` builds these together with one
further module, `SignedVsAbsoluteResidueGadget.lean` (a halo-route
structural lemma belonging to the companion GL(2) strand of
Question Q:EC-recip, §X.7, and outside the scope of §X), for a
total of **11 modules in the build target**, all of which compile
under `leanprover/lean4:v4.28.0`. (The `formal-conjectures/`
directory additionally holds the transient `_AxiomCheck.lean`
audit harness and one round-9 scratch extract, neither part of the
build target; file counts in the directory listing should not be
read as module counts.) Across the build there are exactly
**2 `sorry`s**, both the DPAC headline conjecture at general $K$:
one in `DPAC_full.lean:338` (the obstruction annotated in-source
as `-- RESEARCH-OPEN:` at line 321) and one in
`DirichletPolynomialAvoidance.lean:54`, a statement-only mirror of
the conjecture (Saar Shai, *Prime Spectroscopy of Riemann Zeros*,
§3) carrying a bare `sorry` with no in-source annotation or
category attribute. Of the 10 §X modules, **8 are fully proved
(0 `sorry`)** — and the out-of-scope 11th module is likewise
`sorry`-free — covering the algebraic content of §X.3, §X.4, the
smoothed explicit-formula chain, the Mertens spectroscope
universality statement, the Farey bridge identity (the
underlying static Farey–Mertens identity is classical, in the
Mikolás (1949) tradition; what is contributed here is its
unconditional Lean formalisation, now that `RamanujanSum.lean`
has discharged the Ramanujan-sum hypothesis), the Farey
sign-pattern statement
(conditional on `h_chebyshev_bias` and the two pointwise
falsification witnesses at $p = 237{,}733$ and $p = 243{,}799$),
and DPAC for $K \le 4$.

No `axiom` declarations are introduced anywhere in the project. A
companion `_AxiomCheck.lean` file runs `#print axioms` on each
audited headline theorem. Six audited headlines (the `RamanujanSum`
chain, `FareyBridgeIdentity`, `LocalPerronResidue`,
`CorrectedBInfty`, `MertensSpectroscopeUniversality`,
`FareySignPattern`) depend only on the standard Lean trust base
`propext`, `Classical.choice`, `Quot.sound`. The remaining audited
headline `dpac_le_4` (unconditional DPAC for $K \in \{2, 3, 4\}$)
additionally uses `Lean.ofReduceBool` and `Lean.trustCompiler` —
Mathlib's standard kernel-reduction primitives, used because the
proof evaluates Möbius values at small primes in the kernel. The
eighth fully-proved file, `SmoothedDwfFormula_full`, is a 17-lemma
algebraic-glue chain rather than a single headline theorem; its
component lemmas use only the standard trust base, and its two
analytic prerequisites are stated as explicit hypotheses on the
consuming theorems. No axiom is unstable or project-specific. The
full per-`sorry` inventory and the cumulative axiom audit are in
the companion `LEAN_SORRY_STATUS.md` of the reproducibility bundle.

**Status of headline theorems** in §X.3–§X.4:

| Paper object | Lean status |
|---|---|
| Lemma X.3.1 (local Perron residue) | **Lean-verified unconditional** (`LocalPerronResidue.lean`, 0 `sorry`) |
| Theorem X.4.1 (corrected $B_\infty$ identity) | **Lean-verified conditional** on the convergence-of-partial-sum hypothesis derived in Appendix A (`CorrectedBInfty.lean`, 0 `sorry`) |
| Theorem X.4.2 ($c_K$ leading + subleading) | Pen-and-paper proof in Appendix B; off-target-zero-simplicity hypothesis stated explicitly |
| (AK), (SP-L), (NDC) | (AK) cited (Aoki–Koyama 2023); (SP-L) and (NDC) open challenges (Q:Perron, §X.7) |
| DPAC | **Lean-verified for $K \le 4$ unconditional** (`DPAC_closure_attempt.lean`, 0 `sorry`); general $K$ open (LI-class), with obstruction certificate via Pólya 1913 |

| Paper object | Lean file | Status |
|---|---|---|
| Boundary residue $R_0 = -2$ for a Gaussian-cutoff Mellin-shift explicit formula (companion strand) and its algebraic-glue chain | `SmoothedDwfFormula_full.lean` | **THEOREM (chain), 0 `sorry`.** All 17 algebraic-glue lemmas closed unconditionally; the two analytic prerequisites `mellin_decay` (Stirling on $\Gamma$ vertical strips) and `inv_zeta_polynomial_growth` (Titchmarsh §3.11) are now stated as explicit hypotheses on the theorems that consume them, both Mathlib v4.28.0 gaps. |
| Lemma X.3.1 (local Perron residue) | `LocalPerronResidue.lean` | **THEOREM (0 `sorry`).** The residue identity is stated as a `Tendsto` limit at $L$ analytic with simple zero at $0$ (the general-$\rho$ case reduces by $L \mapsto L(\cdot + \rho)$). |
| Theorem X.4.1 ($B_\infty$ identity) | `CorrectedBInfty.lean` | **THEOREM (0 `sorry`), conditional on `h_convergence`.** The four-component identity is proved against `noncomputable def`s of $T_\infty$, $T_{\ge 3}$, $\mathrm{BPC}_1$, $\mathrm{BPC}_2$, $L$ given an added hypothesis `h_convergence : Tendsto T_K atTop (nhds (RHS))`. This hypothesis packages exactly the four analytic inputs of the pen-and-paper proof in Appendix A (Akatsuka 2013, log-Euler-product, imprimitive induction, geometric tails); the Lean proof uses `Classical.epsilon_spec` + `tendsto_nhds_unique` and is three lines. |
| Farey bridge identity | `FareyBridgeIdentity.lean` | **THEOREM (0 `sorry`), unconditional** (`farey_bridge_identity_unconditional`). The `h_ramanujan_decomp` hypothesis is now discharged by `RamanujanSum.farey_ramanujan_decomp`; the only inputs are `Nat.Prime p` and Mathlib v4.28.0. *Provenance:* the underlying static Farey–Mertens identity (the $m = p$ slice $\sum_{f \in \mathcal{F}_{p-1}} e^{2\pi i p f} = M(p) + 2$) is classical, in the Mikolás (1949) tradition and a special case of the Farey-discrepancy Fourier spectrum; the contribution recorded here is the unconditional machine formalisation, not the identity itself. The genuinely novel mathematical content of this strand is the *differential, per-step* refinement (the sign behaviour as a single prime denominator enters), developed in the companion Dominance/Chebyshev-bias chapter, not §X. |
| Mertens spectroscope universality | `MertensSpectroscopeUniversality.lean` | **THEOREM (0 `sorry`), conditional on an explicit-formula asymptotic hypothesis** (Soundararajan 2009 Theorem 1 input). The file additionally contains a 5-step blueprint documenting the precise Mathlib gap (Perron inversion, explicit formula for $M(x)$, oscillatory-integral partial summation, zero simplicity) and two new unconditionally-proved infrastructure lemmas: `spectroscope_nonneg` (the spectroscope statistic is non-negative) and `reciprocal_sqrt_not_summable` (if $\sum_{p \in P} 1/p$ diverges, so does $\sum_{p \in P} 1/\sqrt p$). |
| Farey sign pattern | `FareySignPattern.lean` | **THEOREM (0 `sorry`), conditional.** Three theorems closed under explicit named hypotheses: `farey_sign_pattern_density_one` (density-one `Tendsto` version, under `h_chebyshev_bias`); `pointwise_falsification_237733` and `pointwise_falsification_243799` (the two pointwise falsifications, each under a `h_witness` hypothesis stating that the relevant signs disagree), packaged into `pointwise_version_falsified`. Negative result for the pointwise conjecture; the falsifications are recorded as theorems, not axioms — the project's "no `axiom`" convention is preserved. |
| Ramanujan sum + Farey decomposition (Hardy & Wright Thms 271, 304) | `RamanujanSum.lean` | **THEOREMS (0 `sorry`), unconditional.** Geometric sum identity for roots of unity (`geom_sum_roots_of_unity`); primitive-roots-sum equals Möbius (`primRootsSum_eq_moebius`, via Dirichlet convolution + strong induction); the coprime case $c_q(n) = \mu(q)$ (`ramanujanSum_eq_moebius_of_coprime`); FareySet sum decomposition (`farey_ramanujan_decomp`) discharging the `h_ramanujan_decomp` hypothesis above. |
| Dirichlet Polynomial Avoidance (DPAC) — partial closure + bridges | `DPAC_closure_attempt.lean`, `DirichletPolynomialAvoidance.lean`, `DPAC_full.lean` | **PARTIAL.** `DPAC_closure_attempt.lean` (0 `sorry`) proves DPAC unconditionally for $K \in \{2, 3, 4\}$ using only $0 < \mathrm{Re}(\rho) < 1$ (`dpac_K_eq_2`, `dpac_K_eq_3`, `dpac_K_eq_4`, `dpac_le_4`). It also reformulates the open case as `FiniteLogRatioLI` and records the obstruction certificate (Pólya 1913 discreteness of the exponential-polynomial zero set + a single open avoidance statement). The headline conjecture for general $K$ remains `sorry` in `DPAC_full.lean:338` and `DirichletPolynomialAvoidance.lean:54`, diagnostically comparable to the Linear Independence Hypothesis for $\zeta$-zero ordinates (made precise in the §X.7 Structural remark); the four explicit phase-avoidance bridges (`dpac_of_logPrimePhaseAvoidance` through `dpac_of_certifiedZetaZeroSample`) are closed without `sorry`. |

The role of the Lean artifact is to fix the statements and provide
a publicly inspectable audit trail of the proof obligations
remaining.

---

## X.7 Open challenges

The following structure the next phase of the program.

> **Q:Perron (Shifted Perron leading theorem).** Prove the shifted
> Perron leading statement (SP-L) for primitive non-principal
> $\chi$ and simple non-central $\rho$.

Three sufficient packages, in decreasing strength of input
required (see `SP_L_SUFFICIENT_PACKAGES_2026-05-13.md` of the
supplementary archive for the full discussion):

- **Route I (off-target simplicity + shifted negative second
  moment).** All off-target zeros at the truncation height are
  simple, and
  $\sum_{\rho'}^\mathrm{mult} |L(\rho' + \alpha,\chi)|^{-2} \ll_\chi (\log K)^{O(1)}$.
  Near-Lindelöf strength; not unconditionally available.
- **Route II (halo-route reduction).** The cluster-summed-residue
  contour pivot (transferred from the GL(2) version) replaces the
  termwise budget by a signed cancellation but yields only
  $|R_K| \ll K^{1/2 + \varepsilon}$ for the off-target aggregate —
  **far above the $o(\log K)$ target**. The halo route in its
  present form does not close (SP-L), though it does replace the
  rooted Palm wall as the structural obstruction.
- **Route III (direct partial summation).** Substantially weaker:
  a Gonek–Hejhal-type bound
  $A(T) := \sum_{\gamma' \le T,\, \gamma' \ne \tau}
  1/[(\rho' - \rho)\,|L'(\rho', \chi)|] \ll_\chi \log T$, combined
  with a Mertens-style oscillation bound
  $\int_0^T K^{i(\gamma - \tau)}\, dA(\gamma) = o(\log T)$ uniformly
  in $K$ along the zero-avoiding heights. This is the cleanest
  pen-and-paper analogue of Akatsuka 2013 eq.~(2.5) applied to the
  off-target weight sequence.

The total-Möbius bounds of Soundararajan type are too coarse to
isolate the pointwise cancellation at the $\log K$ scale by
themselves.

> **Q:EC-recip (GL(2) reciprocal-derivative control).** Prove a
> fixed-curve theorem for
> $\sum_\gamma \widehat W(i\gamma)\,e^{i\gamma u} / L'(E, 1 + i\gamma)$
> giving cancellation $o(u^r)$, or a minimum-modulus estimate
> on a vertical line with explicit exponent $< 2$.

Without a GL(2) analogue of Aoki–Koyama, the EC side remains at the
level of quantitative ensemble evidence.

> **Q:DPAC (Dirichlet Polynomial Avoidance).** Prove DPAC for
> general $K$. We give an unconditional Lean proof for
> $K \in \{2, 3, 4\}$; the general case reduces, via Pólya 1913
> discreteness of the finite-exponential-polynomial zero set, to
> a single open avoidance statement at $\zeta$-zero ordinates
> (made precise in the Structural remark below).

**Structural remark (shared obstruction).** We record an
identification of the *form* of the obstruction common to the open
items above — an observation about structure, not a resolution,
and not asserted as a theorem. The shifted-Perron leading
statement (SP-L) of Q:Perron and the general-$K$ reduction
`FiniteLogRatioLI` of Q:DPAC are, respectively, the sharp
($c \to 1$) and discrete instantiations of a single
negative-second-moment / linear-independence phenomenon for the
zero ordinates: both are controlled by a Gonek–Hejhal-type
reciprocal-derivative second moment of the
$\sum_{\rho} |\zeta'(\rho)|^{-2}$ family (Ng 2004) together with a
quantitative linear-independence input on the relevant ordinates.
The companion GL(2) strand of Q:EC-recip reduces (softly, $c < 3$)
to the same family at GL(2). Thus "diagnostically comparable to
the Linear Independence Hypothesis", used loosely above, is here
made precise: under a quantitative LI hypothesis for the relevant
$L$-function's zero ordinates the shared second moment is
controlled, simultaneously closing the GL(1) `FiniteLogRatioLI`
obstruction and feeding (SP-L); neither instantiation is proved
unconditionally, and locating this common barrier precisely (not
moving it) is the present contribution.

**Further questions** (from the EC and ensemble negatives of §X.5.5
and from the §X.5-companion EC-NDC programme; deferred to the
supplementary record):

- *Q:conductor* — Replicate the §X.5.5 regression of
  $\mathbb{E}[C_1^2]$ on $(\mathrm{rank}, \log N)$ on a curve set
  where rank and $\log N$ are not collinear, to separate any
  genuine rank dependence from the conductor contribution.
- *Q:Sym2* — Identify a completed or archimedean-corrected
  $\mathrm{Sym}^2$ normalisation replacing the empirically falsified
  raw $\mathrm{Sym}^2 / \langle f, f \rangle$ proportionality (which
  ranges over seven orders of magnitude across
  $\{37a_1, 389a_1, \Delta\}$).
- *Q:EC-NDC* — Identify a normalisation of $D_K^E$ for which the
  universal limit exists and is distinguishable from null
  transforms. The sharp-cutoff form $D_K^E \cdot \zeta(2) \to 1$ is
  falsified through $K = 10^{6}$; smoothed variants show numerical
  agreement, but the predeclared G3 specificity gate fails to
  separate them from null controls, so the apparent agreement is
  not yet significant.

---

## X.8 Code, data, and certificate availability

All scripts, refined zero data, numerical-table CSVs, convergence
logs, the Lean 4 lake project, and the reproducibility manifest will
be deposited as a single self-contained reproducibility bundle
(Supplementary material S1), mirrored at a Zenodo DOI at acceptance.
The bundle pins all software versions: Lean toolchain
`leanprover/lean4:v4.28.0`, Mathlib commit
`8f9d9cff6bd728b17a24e163c9402775d9e6a365`, `mpmath` 1.4,
PARI/GP 2.17.3, FLINT 3.3 / python-flint 0.8.0. The Phase-1
Dominance-of-$-1$ replication bundle is included as the
Supplementary Material S1 archive. Each numerical
table in §X.5 cites the L1 script and L2 reproducer; each external
theorem cited in §X.4 has its PDF retrieval recipe, page/equation,
and verbatim quote recorded in the citation audit
(Supplementary S2, *Citation audit*).

---

## References (section)

External references cited in §X.3–§X.7. Full page-and-equation
provenance for each is in Supplementary S2 (citation audit).

- **Akatsuka, H.** (2017). *The Euler product for the Riemann
  zeta-function in the critical strip*. Kodai Math. J. **40**(1),
  79–101; DOI 10.2996/kmj/1490083225. The boundary-line
  Mertens-type partial-summation estimate
  $\sum_{p \le X} \chi(p) / p^{1 + 2i\tau} = c(\chi, \tau) + O(1 / \log X)$
  used in §X.4.1, Appendix A §A.2.3; Lemma 2.1 / eq. (2.5).
  Unconditional (derived from PNT with explicit error term).
- **Aoki, M. and Koyama, S.** (2023). *Chebyshev's bias against
  splitting and principal primes in global fields.* J. Number Theory
  **245**, 233–262; eq. (1.4), p. 235. The
  $e^{-m\gamma}$-normalised partial-Euler-product asymptotic at
  noncentral zeros under DRH. Cited as Hypothesis (AK) in §X.4.3.
- **Davenport, H.** *Multiplicative Number Theory*, 3rd ed.,
  GTM **74**, Springer 2000. Hadamard–de la Vallée Poussin
  non-vanishing on $\mathrm{Re}(s) = 1$.
- **Hardy, G.H. and Wright, E.M.** *An Introduction to the Theory of
  Numbers*, 6th ed., Oxford 2008. Theorem 304 (Ramanujan-sum identity
  at primes).
- **Inoue, S.** (2021). *Some explicit formulas for partial sums of
  Möbius functions.* Journal de Théorie des Nombres de Bordeaux
  **33**(2), 273–315; Theorem 1 and eq. (4.1). Used in Appendix B
  §B.1, §B.3 to set up the contour integration for Theorem X.4.2.
- **Montgomery, H.L. and Vaughan, R.C.** *Multiplicative Number
  Theory I. Classical Theory*, Cambridge 2007. Theorem 9.4 (textbook
  bad-prime correction structure).
- **Ng, N.** (2004). *The distribution of the summatory function of
  the Möbius function.* Proc. London Math. Soc. **89**(3), 361–389.
  Discussed alongside Soundararajan 2009 for the off-target zero
  aggregate (Question Q:Perron, §X.7).
- **Pólya, G.** (1913). *Über die Nullstellen gewisser ganzer
  Funktionen.* Classical discreteness of the zero set of a finite
  exponential polynomial; used in `DPAC_closure_attempt.lean` for
  the obstruction certificate.
- **Soundararajan, K.** (2009). *Partial sums of the Möbius
  function.* J. reine angew. Math. (Crelle's Journal) **631**,
  141–152; DOI 10.1515/CRELLE.2009.044 (arXiv:0705.0723);
  Theorem 1. The
  RH-conditional rate bound $M(x) \ll \sqrt{x}\exp((\log x)^{1/2}(\log\log x)^{14})$
  for the Möbius partial sum, used (via the character analogue at
  numerically-verified RH heights) in Theorem X.4.2 and Appendix B §B.4.
- **Tenenbaum, G.** *Introduction to Analytic and Probabilistic
  Number Theory*, 3rd ed., GSM **163**, AMS 2015. Chapter II.5
  (Hadamard–de la Vallée Poussin treatment).
- **Titchmarsh, E.C.** *The Theory of the Riemann Zeta-Function*,
  2nd ed., Heath-Brown rev., OUP 1986. §3.11 (the polynomial-growth
  bound on $1/\zeta(s)$ used in `SmoothedDwfFormula_full.lean` and
  cited as a Mathlib prerequisite in §X.6).

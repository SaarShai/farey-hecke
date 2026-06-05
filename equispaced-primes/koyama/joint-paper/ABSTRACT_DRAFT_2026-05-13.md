# Abstract — first prose draft (discussion document)

A first prose drafting of the Abstract for the joint paper, written
against the bullet skeleton in `INTRO_AND_ABSTRACT_OUTLINE_2026-05-13.md`.
Intended as a drop-in starting point that can be edited, tightened, or
discarded. Updated 2026-05-14 with the corrected 8-of-10 Lean count
and a single recommended variant.

## Recommended — tight version (≈ 165 words)

Let $\chi$ be a primitive non-principal Dirichlet character of
conductor $q$ and let $\rho = \tfrac12 + i\tau$ ($\tau\neq 0$) be a
simple zero of $L(s,\chi)$. We prove unconditionally a four-component
identity for the prime-power tail $T_\infty(\chi,\rho)$, isolating
the primitive companion factor $\tfrac12 \log L(2\rho,\psi)$.
Combined with the local Perron double-pole residue, this yields
$c_K(\chi,\rho) = \log K / L'(\rho,\chi) + C_1(\chi,\rho) + o(1)$
with $C_1 = -L''(\rho,\chi)/(2L'(\rho,\chi)^2)$. The corrected
asymptotic target for the Dirichlet duality statistic
$D_K = c_K E_K$ is the Aoki–Koyama–Mertens constant $e^{-\gamma}$
(Aoki–Koyama 2023); the modulus $|D_K|\cdot\zeta(2)$ drifts from
$0.992$ at $K = 2\cdot 10^{6}$ to $0.974$ at $K = 10^{7}$,
incompatible with $1$ and consistent with $\zeta(2)\,e^{-\gamma}
\approx 0.9237$. The shifted Perron leading remainder (SP-L) and the
Dirichlet Polynomial Avoidance Conjecture remain open; we identify
each with a precise sufficient package. A Phase-1 prime-residue
replication of the Dominance-of-$-1$ tables at $x = 1.3\cdot 10^{13}$,
and a Lean 4 / Mathlib v4.28.0 lake project in which eight of ten
files are machine-verified end-to-end, accompany the analytic
results.

## Alternative 1 — long form (≈ 235 words)

Use this if the venue accepts longer abstracts (e.g. J. Number
Theory, where the joint paper is likely targeted).

> We develop the analytic framework that controls the partial Euler
> product and the partial Möbius dual at simple noncentral zeros of
> Dirichlet $L$-functions. Our main algebraic result is an
> unconditional identity for the prime-power tail
> $T_\infty(\chi,\rho)$ at a primitive non-principal character $\chi$
> and a simple critical-line zero $\rho$: $T_\infty$ decomposes as
> $\tfrac12\log L(2\rho,\psi) + \mathrm{BPC}_1 + \mathrm{BPC}_2 +
> T_{\ge 3}$, where $\psi$ is the primitive character inducing $\chi^2$
> and the three correction terms are individually finite. Combined
> with a local Perron double-pole residue identity for the partial
> Möbius sum, this yields the leading + subleading asymptotic
> $c_K(\chi,\rho) = \log K / L'(\rho,\chi) + C_1(\chi,\rho) + o(1)$,
> with $C_1 = -L''(\rho,\chi)/(2L'(\rho,\chi)^2)$. The asymptotic
> target for the corresponding Dirichlet duality statistic
> $D_K(\chi,\rho)$ is the Aoki–Koyama–Mertens constant $e^{-\gamma}$
> (Aoki–Koyama 2023, eq. (1.4)), which corrects the earlier
> $\zeta(2)^{-1}$ target; the modulus $|D_K|\cdot\zeta(2)$ drifts from
> $0.992$ at $K = 2\cdot 10^{6}$ to $0.974$ at $K = 10^{7}$, consistent
> with $\zeta(2)\,e^{-\gamma}\approx 0.9237$ and incompatible with $1$.
> We identify the shifted Perron leading remainder (SP-L) and the
> Dirichlet Polynomial Avoidance Conjecture (DPAC) as the load-bearing
> open challenges; we also independently replicate the residue-count
> tables underlying the Dominance-of-$-1$ framework at $x = 1.3\cdot 10^{13}$.
> Eight of the ten accompanying Lean 4 / Mathlib v4.28.0 files in the
> reproducibility bundle are machine-verified end-to-end.

## Alternative 2 — minimal / arXiv-announcement (≈ 115 words)

Use this for an arXiv abstract or a short conference-proceedings
companion.

> We prove a four-component identity for the prime-power tail
> $T_\infty(\chi,\rho)$ at simple noncentral zeros of Dirichlet
> $L$-functions, isolating the primitive companion factor
> $\tfrac12 \log L(2\rho,\psi)$. The corresponding partial Möbius sum
> admits the leading + subleading expansion
> $c_K(\chi,\rho) = \log K/L'(\rho,\chi) + C_1(\chi,\rho) + o(1)$,
> with $C_1 = -L''/(2(L')^2)$. The asymptotic target for the
> Dirichlet duality statistic $D_K = c_K E_K$ is the
> Aoki–Koyama–Mertens constant $e^{-\gamma}$, corrected from the
> earlier $\zeta(2)^{-1}$ target. The shifted Perron leading
> remainder (SP-L) and the Dirichlet Polynomial Avoidance Conjecture
> (DPAC) remain open. A Phase-1 replication of the Dominance-of-$-1$
> residue-count tables at $x = 1.3\cdot 10^{13}$ and a Lean 4 lake
> project (eight of ten files fully proved) accompany the analytic
> results.

## Notes

- **All three drafts** emphasize the unconditional algebraic content
  (Theorem X.4.1 + Lemma X.3.1 + Theorem X.4.2) first, the
  $e^{-\gamma}$ correction (the visible numerical signature) second,
  the open challenges third, and the Phase-1 / Lean material fourth.
- **What's missing from all three**: any reference to the broader
  Dominance-of-$-1$ programme as motivation, the Chebyshev-bias
  context (Rubinstein–Sarnak, Stark, Littlewood), or the
  log-discrepancy / cusp-form ensemble side. These belong in the
  Introduction (which references them already via the bib).
- **Why the tight version is recommended.** §X is one section of the
  joint paper; the Abstract sits at whole-paper level. The §X
  analytic contribution is best summarised with the tight 165-word
  form, leaving room for the Dominance-of-$-1$ framing material that
  is yours to lead with. If you prefer a §X-only abstract for a
  satellite/standalone version of the analytic chapter, the long
  form is the starting point; the minimal form is the arXiv
  announcement.
- **What needs your input**: the framing of the paper as a whole.
  If this is *your* programme paper with our analytic contribution as
  one substantial chapter, the joint-paper Abstract should foreground
  the Dominance-of-$-1$ result (which is yours), not the corrected
  $B_\infty$ identity (which is ours). The Recommended variant is
  written so it can be either prepended (after your Dominance-of-$-1$
  paragraph) or used as a §X-standalone synopsis.

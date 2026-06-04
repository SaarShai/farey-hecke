# Abstract + Introduction — proposed outline (discussion document)

A skeleton for the Abstract and Introduction of the joint paper, drafted
as a starting point for our integration pass. Bullet form is deliberate:
each line is a candidate claim or topic to keep / cut / rephrase, not
committed prose. The §X technical/computational section is taken as the
load-bearing computational contribution; the larger framing of the paper
(your Dominance-of-$-1$ programme, the connection to Aoki–Koyama 2023,
the broader Chebyshev-bias context) sits at a level you are the natural
author for.

## Proposed Abstract (6–7 sentences)

1. **One-sentence headline.** We establish a corrected analytic
   framework for the partial Euler product / partial Möbius dual at
   simple non-central zeros of Dirichlet $L$-functions, supplied with
   rigorous numerical verification at the analytic scale $K \le 10^{7}$
   and a Phase-1 prime-residue replication of the Dominance-of-$-1$
   tables at $x = 1.3 \cdot 10^{13}$.

2. **Algebraic content.** We prove unconditionally a four-component
   identity (Theorem X.4.1) for the prime-power tail $T_\infty(\chi,
   \rho)$, isolating a primitive $L$-factor $\tfrac{1}{2}\log L(2\rho,
   \psi)$, a finite bad-prime correction, an absolutely convergent
   $\mathrm{BPC}_2$ residue, and a $k \ge 3$ tail; together with a
   local Perron double-pole residue lemma giving the subleading
   constant $C_1(\chi, \rho) = -L''(\rho, \chi) / (2L'(\rho,\chi)^2)$.

3. **Asymptotic correction.** The Aoki–Koyama–Mertens
   $e^{-\gamma}$ normalisation (Aoki–Koyama 2023 eq. (1.4))
   corrects the earlier $\zeta(2)^{-1}$ target; the corrected
   $|D_K| \cdot \zeta(2)$ statistic drifts from $0.992$ at
   $K = 2 \cdot 10^{6}$ to $0.974$ at $K = 10^{7}$, consistent with
   convergence to $\zeta(2)\,e^{-\gamma} \approx 0.9237$ and
   incompatible with $1$.

4. **Open challenges identified.** We identify the shifted Perron
   leading remainder (SP-L) as the load-bearing analytic obstruction,
   precisely stated; we identify the Dirichlet Polynomial Avoidance
   Conjecture (DPAC) as a related open problem, comparable to the
   Linear Independence Hypothesis for $\zeta$-zero ordinates; we
   identify a GL(2) reciprocal-derivative control as the analogous
   obstruction on the elliptic-curve side.

5. **Phase-1 replication.** Two independent prime-enumeration
   implementations agree on the residue counts $\pi(x; N, a)$ of
   the Dominance-of-$-1$ tables for $N \in \{7, 8, 11, 19, 23\}$ at
   $x = 1.3 \cdot 10^{13}$; identity (3.1) is verified across $495$
   cells; cell-by-cell match with the published tables is $\ge 91\%$.

6. **Lean 4 formalisation.** Six headline algebraic statements
   (Lemma X.3.1, Theorem X.4.1, Theorem X.4.2 algebraic skeleton, the
   smoothed-$\Delta w_f$ explicit-formula chain, the Mertens
   spectroscope universality, the Farey bridge identity, and DPAC for
   $K \in \{2, 3, 4\}$) are machine-verified in Lean 4 / Mathlib
   v4.28.0; two `sorry`s remain, both the DPAC headline conjecture
   (LI-class).

7. **Closing tag.** Optional one-sentence forward look (e.g., what
   completes the (NDC) limit, or what closes (SP-L)).

## Proposed Introduction (5 sections)

### §1 Motivation
- The Dominance-of-$-1$ programme and Chebyshev's bias at
  $w = 1/2$ (Aoki–Koyama 2023, Shimada–Koyama 2025).
- Why the partial-Euler-product / partial-Möbius dual is the right
  object: it carries both the $\log L(1, \chi_{a,1})$ scaling that
  governs the strength of bias and the analytic-residue structure
  that drives the convergence rate.
- The numerical question that motivates the paper: what is the
  correct asymptotic target for $D_K(\chi, \rho)$?

### §2 Prior work and the $e^{-\gamma}$ correction
- Brief account of Aoki–Koyama 2023 eq. (1.4) and the
  $e^{-m\gamma}$ normalisation.
- The earlier $\zeta(2)^{-1}$ target and why it is incompatible
  with the $1/\log K$ finite-size drift.
- A one-paragraph statement of (AK), placing it as the analytic
  input.

### §3 Main results (this paper)
- Theorem X.4.1 stated in one display (forward reference to §X.4.1).
- Theorem X.4.2 stated in one display (forward reference to §X.4.2).
- The (NDC) limit displayed once, with the conditional clause on
  (SP-L).
- The Phase-1 replication summarised in one paragraph.
- The Lean 4 inventory summarised in one paragraph.

### §4 Open challenges
- (SP-L), DPAC, GL(2) reciprocal-derivative control, each in two
  to three sentences (the corresponding "Q:" labels live in §X.7).

### §5 Paper structure
- One-paragraph roadmap pointing forward to §2 (notation), §3
  (your Dominance-of-$-1$ framework if it's its own section), §X
  (this section), etc.

## Notes for the integration pass

- **Author-voice.** The §X technical material is written in collective
  "we"; the Introduction will inherit the same voice.
- **Citation density.** §X already has 11 references; the Introduction
  may add Rubinstein–Sarnak 1994, Littlewood 1914, Stark 1971,
  Feuerverger–Martin 2000, and the Aoki–Koyama 2023 + Shimada–Koyama
  2025 pair from your *nontriv.pdf*.
- **What to keep vs cut.** The Abstract above is dense (Lean +
  Phase-1 + (SP-L) + Dominance signal); a tighter Abstract might drop
  one of these (probably Lean) and put it in §6 instead. Up to you.
- **Numbering.** All `X.N` placeholders in §X will resolve on
  integration.

This document is a working sketch — feel free to rewrite, reorder, or
discard. I will draft a first full Abstract + Introduction in prose
once we have alignment on this skeleton.

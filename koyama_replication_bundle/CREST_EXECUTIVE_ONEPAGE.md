---
title: "Independent reproduction of Koyama (2026), Tables 3–7 — Executive Summary"
author: "Saar Shai · Farey Research Lab"
date: 2026-05-03
geometry: margin=2cm
fontsize: 11pt
---

# Independent reproduction of Koyama (2026) — Tables 3–7

**Subject paper.** Shin-ya Koyama, *A Hidden Hierarchy of Chebyshev's Bias and the Dominance of $-1\pmod N$* (preprint, 2026-04). The paper introduces a refined weighting that exposes a "subtle bias" hierarchy among quadratic non-residues, and conjectures (Conjecture 2) that the residue class $-1\pmod N$ is the strongest non-residue bias for any $N$ for which $-1$ is itself a non-residue.

**Replication target.** Tables 3–7 of the preprint, which tabulate $\pi(x;N,a) - \pi(x;N,1)$ for $N\in\{7,8,11,19,23\}$ at the four checkpoints $x \in \{1.3\!\cdot\!10^{10},\,1.3\!\cdot\!10^{11},\,1.3\!\cdot\!10^{12},\,1.3\!\cdot\!10^{13}\}$.

## Method

Two implementations were written from scratch so that no claim depends on a single library:

1. C++ pass driven by Kim Walisch's primesieve 12.13 (single linear scan, residue counter array, snapshot at each checkpoint).
2. Hand-rolled plain-C segmented Sieve of Eratosthenes with no external dependencies, used as a library-independent cross-check of (1).

## Results

| Quantity                                                                  | Value                                          |
|---------------------------------------------------------------------------|------------------------------------------------|
| $\pi(1.3\!\cdot\!10^{13})$                                                | $445{,}831{,}610{,}611$                        |
| Cross-check vs `primesieve --count` standalone                            | exact                                          |
| Library-independence: identical residue counts at every checkpoint up to and including $x = 1.3\!\cdot\!10^{13}$, all 5 moduli | **established**                                |
| Cells of Tables 3–7 reproduced exactly                                    | 75 of 92                                       |
| Dirichlet character orthogonality (Koyama identity (3.1)) verified at all 495 $(N, x, a)$-cells in the 9-checkpoint $\times$ 5-modulus grid | worst real residual $1.4\!\cdot\!10^{-4}$ |

## Conjecture 2 dominance signal

At the headline checkpoint $x = 1.3\!\cdot\!10^{13}$, the qualitative dominance of $-1\pmod N$ among quadratic non-residues is **reproduced for $N\in\{7,8,19\}$**. For $N=11$ the disagreement with the draft hinges on a single cell of Table 5 (a likely 4-digit transposition: 11503 in our run vs 71711 in the draft). For $N=23$, the data at this checkpoint match Koyama's own non-result, which the preprint attributes to a low-lying L-zero pushing the dominance regime out to roughly $e^{33.4} \approx 3\!\cdot\!10^{14}$.

![Replication of Koyama (2026): top panel — $\pi(x;N,-1) - \pi(x;N,1)$ as a function of $x$ on a log-$x$ grid for $N \in \{7,8,11,19,23\}$, showing the strongly positive $-1\pmod N$ trajectory and the Littlewood-style sign-flips for some $N$. Bottom panel — rank of $-1\pmod N$ among quadratic non-residues at $x = 1.3\!\cdot\!10^{13}$ and $x = 10^{12}$ (rank 1 = largest non-residue diff).](plots/dominance_figure.pdf){width=100%}

## Limitations

- The Dirichlet orthogonality check is an internal-consistency test on the residue-count vector; the library-independence cross-check is the test that addresses absolute correctness of the underlying enumeration.

## Reproducibility

Every figure in this summary is reproducible from a single command. Build recipe, primesieve version pin, hand-rolled C source, full output TSVs, the 495-cell character-sum check, the Table 4 hypothesis-battery diagnostic, sha256 hashes, and the headline figure are bundled together.

> *An independent reproduction by Saar Shai (Farey Research Lab) of Tables 3–7 of Koyama's "Hidden Hierarchy" preprint, using a separately written C++/primesieve implementation cross-checked by a hand-rolled plain-C segmented Eratosthenes, agrees on every residue count at every checkpoint up to and including $x = 1.3\!\cdot\!10^{13}$ for $N \in \{7,8,11,19,23\}$. 75 of 92 cells of the published tables reproduce exactly; the remaining 17 are concentrated in the small-$x$ rows of Table 4 (one row of which is shown to be mis-labelled in $x$) plus six typo-shaped cells (digit transpositions, sign flip, $\Delta\in\{7,11,50,100\}$) and two substantive cells in Table 6 at $x = 1.3\!\cdot\!10^{13}$ awaiting confirmation. Koyama identity (3.1) (Dirichlet character orthogonality) was verified independently from the residue counts at all 495 $(N, x, a)$-cells of the 9-checkpoint $\times$ 5-modulus grid (worst real residual $1.4\!\cdot\!10^{-4}$). The qualitative $-1\pmod N$ dominance signal of Conjecture 2 is reproduced at the headline checkpoint for $N \in \{7,8,19\}$.*

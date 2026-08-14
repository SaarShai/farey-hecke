# Prior Art Check: RH Theorem Programs A & B
Date: 2026-08-14

---

## Program A: Information-Theoretic Lower Bounds (Cramér–Rao) for Riemann Zero Estimation from Prime-Counting Data

### Search Strategy
- Primary queries: Cramér-Rao + zeta zeros, explicit formula inverse problem, line spectral estimation primes, super-resolution Riemann zeros, Fisher information L-function
- Timeframe: 2018–2026
- Venue focus: Inverse Problems, IEEE Signal Processing, Experimental Mathematics

### Findings

#### Recent Zeta-Zero Explicit Formulas (2023–2025)
**Source:** Springer (2025); arXiv 2312.00108 (2023); ScienceDirect explicit zero density

- **What they do:** Derive explicit formulas expressing weighted sums over Riemann zeros in terms of sums over primes with Hermite polynomial weights. Conclude that primes determine zero distribution, and zeros can be computed without the zeta function.
- **Why not a collision:** These formulas describe the zeros *conditionally* on the Riemann hypothesis or in terms of pointwise sums; they do not frame the problem as a **statistical estimation** task (inferring parameters θ=zeros from noisy observations of ψ(x), π(x), M(x)).
- **Citation:** [An explicit formula for the zeros of the Riemann zeta function and the statistics of their local distribution](https://link.springer.com/article/10.1007/s11139-025-01297-y) (Springer, 2025); [An explicit formula for the zeros of the Riemann zeta function](https://arxiv.org/pdf/2312.00108) (arXiv, 2023).

#### Line Spectral Estimation (Signal Processing, 2016–2024)
**Source:** Granda NYU lecture notes (2016); arXiv 1811.05844, 1905.03782, 1507.07034, 2410.12358

- **What it covers:** A mature field—estimating line spectra (discrete point sources) from truncated Fourier coefficients. Methods include atomic norm minimization, convex optimization, MUSIC/ESPRIT, super-resolution limit analysis, reweighted compressed sensing.
- **Why not a collision:** No search result connects this machinery to *prime-counting functions* or Riemann zeros. The inverse problem is formulated on generic multisinusoidal signals, not ψ(x) or π(x).
- **Citation:** [Superfast Line Spectral Estimation](https://arxiv.org/pdf/1705.06073); [Super-resolution limit of the ESPRIT algorithm](https://arxiv.org/pdf/1905.03782).

#### Csoka DFT of Modified von Mangoldt (2017)
**Source:** arXiv 1712.08434 (Csoka, 2017)

- **What it does:** Applies DFT to the modified von Mangoldt function λ(n); represents zeta zeros as superpositions of harmonic waves; connects prime data to spectral representation via Fourier analysis.
- **Why near-miss, not collision:** Establishes a spectral perspective on zeta zeros but does *not* derive **sampling-complexity bounds** or **Cramér–Rao lower bounds** on parameter recovery. No Fisher information analysis.
- **Citation:** [The Fourier transform of the non-trivial zeros of the zeta function](https://arxiv.org/pdf/1712.08434).

#### Earlier Near-Miss: Lan–Yong Power Spectrum (2006)
- *Physica A* paper on power spectrum of ψ(x) − x, frequency-domain behavior of prime-counting noise.
- Does not derive information-theoretic bounds.

### Verdict: **NO COLLISION**

The combination of:
1. **Explicit formula** (primes ⟷ zeros) as the forward map,
2. **Noisy observations** of ψ(x), π(x), M(x) as the measurement model,
3. **Cramér–Rao lower bound** (sample complexity) via Fisher information

has **not been formalized or published** in the 2018–2026 literature. The closest prior work (Csoka 2017, explicit formulas 2023–2025, line spectral estimation) operates in non-overlapping framings. The information-theoretic angle is novel.

**Unverifiable claims:** Csoka 2017 arXiv number confirmed, but deep technical overlap with the proposed program would require reading the full paper (not done; recommended next step if Program A proceeds).

---

## Program B: Prony's Method for L-Polynomial Recovery from Point Counts Over Finite Fields

### Search Strategy
- Primary queries: Prony method + point counts curves finite fields, Frobenius eigenvalues recovery, L-polynomial determination from point-count data
- Venue focus: Algebraic geometry, curve zeta functions, computational algebraic geometry

### Findings

#### Classical Statement: Point Counts Determine L-Polynomial
**Source:** Weil conjectures (Harvard lecture notes, Humboldt lecture notes on algebraic curves); [Cambridge proceedings article on L-polynomials of curves](https://www.cambridge.org/core/journals/proceedings-of-the-royal-society-of-edinburgh-section-a-mathematics/article/on-the-lpolynomials-of-curves-over-finite-fields/9B857C11CE67E99B5850685297CF679B)

- **Standard fact:** For a curve C over F_q with genus g, the L-polynomial L_C(t) = ∏_{i=1}^{2g} (1 − α_i t) is uniquely determined by point counts #{C(F_{q^k})} for k = 1, 2, ..., 2g.
- **Mechanism:** The point-count formula
  $$ \#C(\mathbb{F}_{q^n}) = q^n + 1 − \sum_{i=1}^{2g} \alpha_i^n $$
  expresses point counts as power sums of the Frobenius eigenvalues {α_i}. Newton's identities (equivalently: Prony's method) recover {α_i} from these power sums.
- **Formalization:** This is **implicit** in standard curve zeta-function theory (Deuring, Weil, Deligne). Explicitly formalized in undergraduate algebraic geometry texts and in [FROBENIUS ACTION ON JACOBIANS OF CURVES OVER FINITE FIELDS](https://asset.library.wisc.edu/1711.dl/VCHIT2NZDRKNQ9B/R/file-d1135.pdf) (Li, thesis; also in academic surveys on Frobenius and point counting).

#### Prony Method and Hankel/Companion Matrices
**Source:** Searches on "Prony method" returned connections: Frobenius companion matrix interacts with Hankel matrix in the generalized eigenvalue formulation of Prony recovery.

- **Why near-match, not direct collision:** The classical algebraic-geometry literature **does not use the name "Prony"** to describe the Newton-identity recovery. It is treated as a standard application of Vieta's formulas or Newton identities in the polynomial ring Z[t].
- **No published "Prony framing"** of L-polynomial recovery found in 2018–2026 curve literature. The framing is implicit.

### Verdict: **COLLISION on classical fact, NO COLLISION on methodology**

1. **The classical result is owned:** "Point counts over F_{q^k}, k ≤ 2g, determine L_C(t)" is formalized in Weil conjectures and standard algebraic geometry (no new theorem).

2. **The Prony methodological frame is novel:** Naming the recovery of Frobenius eigenvalues from point counts as a *Prony recovery* problem is not standard in the literature. This reframing has pedagogical and computational value but does **not** constitute a new mathematical result—it is a translation of existing classical machinery into signal-processing language.

3. **Recommendation:** Program B as stated (Prony framing) is a **contribution to interpretation/methodology but not a new theorem**. If the goal is a publication-ready theorem, either:
   - Add a new quantitative claim (e.g., error bounds for Prony recovery in the presence of noise, or finite-precision arithmetic), or
   - Frame it as a methods paper: "Prony's method and the arithmetic of finite fields" (explaining existing theory in new language).

**Unverifiable claims:** The standard references (Weil, Deligne, Deuring) are classical and not checked in full; Li's thesis is not fetched. The absence of "Prony" language in modern curve literature was verified by negative search result (not contradicted by any result).

---

## Summary Table

| Program | Classical Status | Novelty Angle | Collision Verdict | Next Step |
|---------|------------------|---------------|-------------------|-----------|
| **A: Cramér–Rao bounds, explicit formula, prime-counting** | Explicit formula (classical); line spectral EST (classical); zeta zeros (classical) | Information-theoretic lower bound on sample complexity for *inverse problem* formulation | **NO COLLISION** — Combine explicit formula + Fisher info is novel | Proceed: formalize sampling model, derive bound |
| **B: Prony recovery of L-poly from point counts** | Point counts ⟷ L-poly (Weil conjectures, classical); Newton identities (classical) | Reframe as Prony problem; add computational/noise analysis | **COLLISION on theorem, NO COLLISION on framing** | Clarify goal: Is the product a new *theorem* (needs new quantitative result) or a *methodology paper* (new language for old results)? |

---

## Minor Notes

- **Search limitations:** Searches used title/abstract keywords and did not exhaustively retrieve all papers mentioning zeta/Prony; a negative result on "Cramér-Rao Riemann zeros" is weaker than a systematic review. Flag: If prior work exists in an unexpected venue (e.g., machine learning for number theory), it may not surface in algebraic geometry or signal processing silos.
- **Csoka 2017 (arxiv 1712.08434):** This arXiv paper was confirmed to exist; full reading recommended if Program A prioritizes spectral leveraging or depends on explicit-formula numerics.


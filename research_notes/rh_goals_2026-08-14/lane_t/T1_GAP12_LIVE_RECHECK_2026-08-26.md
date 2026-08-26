# T1 GAP12 Live Prior-Art Re-Check — 2026-08-26

## Research Question
Is there existing published work stating a Cramér–Rao / Fisher-information lower bound for estimating the location (real part or ordinate) of Riemann zeta zeros, or an 'information cost' law for detecting zeta zeros from truncated explicit-formula / Riesz-kernel data?

---

## Search Results & Collision Assessment

### Search 1: "Cramér-Rao Riemann zeta zeros estimation"
**Hit:** [Accurate estimation of sums over zeros of the Riemann zeta-function](https://arxiv.org/abs/2009.13791) — Lehmer & Lehmer; arXiv:2009.13791.  
**Verdict:** SETUP-ONLY — Paper focuses on numerical acceleration of computing sums Σφ(γ) over zero ordinates γ, not statistical parameter estimation via Cramér-Rao bounds or Fisher information. Components exist separately; no unified information-theoretic framework for zero-ordinate estimation.

### Search 2: "Fisher information Riemann zeros ordinate"
**Searches returned:** Fisher information papers (theory), Riemann zero ordinate papers (computation) — no unified source.  
**Verdict:** NONE — Fisher information machinery and zeta-zero ordinate computation are treated independently in the literature. No direct connection found.

### Search 3: "explicit formula frequency estimation zeta zeros"
**Hits:** Riemann-von Mangoldt explicit formula, pair-correlation statistics, zero-counting function work (Alhargan, Tao notes, Springer 2025 paper on local distribution).  
**Verdict:** SETUP-ONLY — Explicit formulas for zeta zeros are well-studied; frequency/statistical properties of zeros are classical (pair correlation, spacing statistics). No information-theoretic lower-bound framework applied to zero ordinate estimation from truncated explicit-formula data.

### Search 4: "Riesz kernel zero detection information"
**Hits:** Riesz criterion for RH (oscillatory sum bounds; Möbius function), Bochner-Riesz kernels in harmonic analysis.  
**Verdict:** NONE — Riesz kernels studied in analytic number theory and harmonic analysis; zero detection via Riesz criterion is qualitative. No information-theoretic quantification (Fisher information, Cramér-Rao, information cost) found.

### Search 5: "information cost detecting Riemann hypothesis"
**Hits:** Machine learning approaches (MDPI 2024, attribution methods); Shannon information / Liouville function white-noise interpretation.  
**Verdict:** SETUP-ONLY — Information theory and RH-detection exist as separate research threads. ML attribution studies focus on classification/explanation, not parameter-estimation lower bounds. No formal Cramér-Rao or Fisher-information framework identified.

---

## Overall Verdict

**COLLISION STATUS: NONE / SETUP-ONLY**

The literature contains:
- **Cramér-Rao / Fisher information:** Classical statistical estimation theory, well-developed.
- **Explicit formulas for zeta zeros:** Riemann-von Mangoldt, modern refinements, pair-correlation statistics.
- **Riesz kernels in analytic number theory:** Criterion for RH, but qualitative.
- **Machine-learning detection of zeros:** Recent (2024–2025), but not information-theoretically bounded.

**No direct published work combines these into an information-cost law for estimating Riemann zeta-zero ordinates from truncated explicit-formula or Riesz-kernel data.** The specific statement of a Cramér–Rao or Fisher-information lower bound for this problem appears unoccupied.

**Implication:** If Lane T develops such a bound (Fisher information for zeta-zero ordinate estimation, quantifying the sample-size and truncation-length information cost), it would be novel. Prior-art collision risk is **minimal**.

---

## Sources
- [Accurate estimation of sums over zeros of the Riemann zeta-function](https://arxiv.org/abs/2009.13791) — arXiv:2009.13791
- [Riemann Zeta Function Zeros](https://mathworld.wolfram.com/RiemannZetaFunctionZeros.html) — Wolfram MathWorld
- [An explicit formula for the zeros of the Riemann zeta function](https://arxiv.org/abs/2312.00108) — arXiv:2312.00108
- [An explicit formula for the zeros of the Riemann zeta function and the statistics of their local distribution](https://link.springer.com/article/10.1007/s11139-025-01297-y) — The Ramanujan Journal, Springer Nature, 2025
- [Notes on Pair Correlation of Zeros and Prime Numbers](https://arxiv.org/abs/math/0412313) — arXiv:math/0412313
- [The Riemann Hypothesis, the Biggest Problem in Mathematics, Is a Step Closer to Being Solved](https://www.scientificamerican.com/article/the-riemann-hypothesis-the-biggest-problem-in-mathematics-is-a-step-closer/) — Scientific American
- [Empirical Investigation of the Riemann Hypothesis Using Machine Learning](https://www.mdpi.com/2227-7390/13/17/2824) — Mathematics (MDPI), 2024

## FRONTIER NOTE 2026-08-26 (fable)
- Authorship caution: arXiv:2009.13791 "Accurate estimation of sums over zeros of the Riemann zeta-function" is Brent–Platt–Trudgian, not "Lehmer & Lehmer" as stated above — verify citation details before any bibliography use. Verdict (SETUP-ONLY) unaffected.
- Overall verdict NONE/SETUP-ONLY is consistent with the earlier grok scout (PARTIAL-COLLISION: bound unoccupied, setup occupied). GAP-12 considered CLOSED for pre-submission purposes; cite imports (Hardy–Riesz, Ingham, Titchmarsh, Ng 2004, Odlyzko–te Riele 1985, Rife–Boorstyn/Kay).

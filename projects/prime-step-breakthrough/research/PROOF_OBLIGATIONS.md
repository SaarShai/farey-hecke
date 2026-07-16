# Proof-obligation ledger

Status values: `proved-on-paper`, `finite-certified`, `review-needed`, `open`,
or `not-a-claim`.

| ID | Obligation | Status | Required evidence |
|---|---|---|---|
| P1 | Fourier numerator equals \(\sum_{2\le b<p}c_b(h+\ell p)\) | proved-on-paper | Direct expansion and small exact tests |
| P2 | Ramanujan box bound is uniform and excludes resonance | proved-on-paper | ETK cutoff \(L<p\), divisor formula, independent review |
| P3 | \(D^*(P_p)=O_\varepsilon(p^{-1+\varepsilon})\) | proved-on-paper | Full ETK weight calculation and independent advisor audit |
| P3b | \(D^*(P_p)\ge1/(p-1)\) and the rate is exponent-optimal | proved-on-paper | Empty anchored rectangle at the smallest old fraction |
| P4 | Even moment quantitative error follows by Koksma--Hlawka | proved-on-paper | Hardy--Krause hypothesis and normalization check |
| P5 | Odd moments vanish exactly | proved-on-paper | Involution and exact Fraction tests |
| P6 | Raw shift moment constant is \(3/[\pi^2(r+1)(2r+1)]\) | proved-on-paper | P3--P5 plus totient asymptotic |
| P7 | Kernel Fourier/Parseval constant is \(1/(2\pi^2)\) | proved-on-paper | Independent piecewise-rational oracle |
| P8 | Divisor kernel constant is \(1/12\) | proved-on-paper | Divisor-sum and local-factor cross-checks |
| P9 | Every local Euler factor in T3 is correct and \(12K\), not \(K\), is pair-multiplicative | proved-on-paper | Exhaustive pair checks, symbolic case split, and \(K(6,6)\) countercheck |
| P10 | \(\sqrt{E_S}/P_S\) is a sharp \(H^1\) error | proved-on-paper | Integration by parts and explicit equality witness |
| P11 | Prime energy-step formula has the `2-A(p-1)` convention | proved-on-paper | Direct kernel sums and endpoint audit |
| P12 | First negative prime is 8501 | finite-certified | Exact Fraction scan through 8501 and machine-readable artifact |
| P13 | Zeta-ratio Dirichlet series is correct for \(\Re s>1\) | proved-on-paper | Euler-factor check |
| P14 | RH equivalence for \(A(x)\) | proved-on-paper | Analytic continuation/partial summation audit; labelled standard machinery |
| P15 | Farey-shear theorem is externally new | open | Professional formula-level literature review |
| P16 | Kernel identity itself is externally new | not-a-claim | Classical ingredients credited; synthesis only |
| P17 | Batch optimizer has practical value within constraints | finite-certified | Preregistered benchmarks and mandatory negative controls passed |
| P18 | Generic or multidimensional QMC superiority | not-a-claim | Explicitly excluded |
| P19 | Historical full wobble sign theorem | not-a-claim | Excluded; counterexample reproduction is separate |
| P20 | T5 permutation-average quadratic identity | proved-on-paper | Sampling-without-replacement proof and exhaustive exact permutations |
| P21 | T5 continuous \(L^2\) expectation has constants \(1/(3N^2)\) and \((N+1)/6\) | proved-on-paper | Direct interval oracle and permutation enumeration |
| P22 | T5's sharp \(s_2^2/3\) fourth-moment bound and interpolation prove the lower-order half of García's conjecture with \(c_1=9/160\) | proved-on-paper | Coefficient expansion, endpoint quadratics, central-index count, equality witness, low-\(N\) cases, and cold inequality audit |
| P22b | T5's Cauchy--Schwarz argument proves the upper-order half of García's conjecture | proved-on-paper | Inequality audit; explicit exclusion of García's sharper proposed constants |
| P23 | Gap certificate avoids factorial enumeration and scales linearly | finite-certified | Million-gap fresh benchmark and live UI/CLI/API parity |
| P24 | CoprimeBatch beats generic or unrestricted complete-batch rules | not-a-claim | Midpoint, prime-layer, and divisor-portfolio losses must remain visible |

No row is promoted by a successful numerical fit.  `review-needed` is not a
stylistic caveat; it blocks publication wording until a cold reviewer signs off.

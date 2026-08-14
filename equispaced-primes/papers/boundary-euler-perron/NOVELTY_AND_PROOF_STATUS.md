# Boundary Euler--Perron note: novelty and proof-status gate

Audit date: 2026-08-01

## Verdict

The boundary prime-power decomposition is **proved unconditionally** after
fixing the logarithm by a horizontal limit from the Euler-product half-plane.
The theorem is stronger than the zero-specialized draft: the evaluation point
need not be a zero and simplicity is unused.

The standalone novelty gate nevertheless **fails**. The exact four-term
display was not found verbatim, but it is a short specialization of existing
boundary Euler-product results plus the standard primitive/imprimitive
Euler-factor identity. The local Perron residue is standard Laurent algebra.
These results should be used as a technical appendix or reproducibility
certificate, not advertised as a new standalone theorem.

## Two-column novelty matrix

| Candidate contribution | Closest primary source and audit verdict |
|---|---|
| Ordinary convergence of the principal boundary prime sum at `1+it`, `t != 0` | [Akatsuka, *Kodai Math. J.* 40 (2017), equations (2.3)--(2.5)](https://doi.org/10.2996/kmj/1490083225) proves the exact `O_t(1/log X)` tail. **Already known.** |
| Boundary value of the naturally ordered logarithmic Dirichlet series | [Conrad, *Canad. J. Math.* 57 (2005), Theorem 4.1](https://doi.org/10.4153/CJM-2005-012-6) gives the boundary Abel/Tauberian statement; Theorem 4.3 and Example 4.6 identify the squared-character second moment. **General framework already known.** |
| Isolation of `k=2`, the bad-prime correction, `BPC_2`, and the absolutely convergent `k>=3` tail | Algebraic decomposition of the logarithmic Euler product and the standard inducing-character Euler factors, inside the Conrad framework. No exact verbatim match found in targeted searches, but the step is routine. **Insufficient independent novelty.** |
| Partial Euler products for primitive Dirichlet characters on/in the critical strip | [Kaneko, *Bull. Aust. Math. Soc.* 106 (2022)](https://doi.org/10.1017/S0004972721001003) treats substantially broader asymptotics and explicitly builds on Conrad's second-moment analysis. **Crowded prior art.** |
| Local coefficient `Res_{w=0} K^w/(wL(rho+w))` | Direct two-term Taylor/Laurent multiplication; the repository also contains a zero-`sorry` Lean theorem for the corresponding limit formulation. **Correct but standard local algebra.** |
| Global asymptotic for `c_K(chi,rho)` from that local residue | [Inoue, *J. Théor. Nombres Bordeaux* 33 (2021)](https://doi.org/10.5802/jtnb.1162) exhibits explicit formulae with zero contributions. Off-target zeros yield non-decaying factors on GRH. **Not proved; excluded.** |

Searches included exact-formula fragments involving `chi(p)^k`, `L(2 rho,
chi^2)`, boundary prime sums, and Dirichlet Euler products, plus direct review
of the sources above. Search non-detection is not evidence of novelty; the
structural prior-art match controls the verdict.

## Proof-status audit

| Gate | Status and reason |
|---|---|
| Finite `k=2` isolation | **Complete.** The inner `k`-series is absolutely convergent for every fixed prime. |
| `k>=3` limit and interchange | **Complete.** Dominated by a constant times `sum_p p^(-3/2)`. |
| Boundary convergence | **Complete at paper level.** Conrad Theorem 4.1 applies to the logarithmic Dirichlet series; Akatsuka independently covers the principal prime-sum case. |
| Abel passage | **Complete at paper level.** The boundary logarithm is defined as the horizontal Euler-product limit and agrees with the ordinary series by the cited Abel theorem. A separate Aristotle attempt targets only this abstract Abel lemma. |
| Imprimitive correction | **Complete.** Take the finite Euler-factor identity in `Re z>1`, then the same horizontal limit. Each bad factor satisfies `|psi(p)p^(-z)|<1`. |
| Branch convention | **Complete after correction.** `Log_*` is canonical by radial continuation. Arbitrary-path independence is explicitly rejected because logarithms have monodromy. |
| Contour displacement | **Not used for the boundary theorem.** For the global `c_K` problem it remains open: off-target residues, zero-sum ordering, horizontal/left-edge bounds, and multiplicities must all be controlled. |
| Local Perron residue | **Complete.** Direct Laurent proof; zero-`sorry` Lean certificate exists in `equispaced-primes/lean/formal-conjectures/LocalPerronResidue.lean`. |
| Standalone publication threshold | **Fail.** Correct theorem, insufficient novelty. |

## Aristotle scope

Project `d84a4795-4fad-42d4-a2d4-d1003a48450d`, task
`8630cf0d-864e-4083-9edc-0e3f6f1d6678`, was dispatched to formalize only the
abstract real-radial Abel passage for an ordinarily convergent series. At the
last bounded poll it remained running (10 percent); no result has been accepted. A
successful result would be an auxiliary formal certificate, not a proof of
Dirichlet `L`-function nonvanishing, the boundary number-theory input, or the
full theorem. Any returned artifact must be compiled and independently
inspected before being cited.

# Pre-reply technical audit of Koyama's 31 July 2026 manuscript

**Internal working document - not yet sent.**

Source reviewed: `/Users/za/Downloads/nontriv2607arXiv.pdf`, 10 pages, SHA-256
`0fae8ae31f086bcfc32ee50b76f7b7a71dd8e8684263fd0087015dd0f8460852`.

## Bottom line

The present draft is **not ready for submission as a joint paper**.  Definition 1.3 contains
a directly checkable inverse-class error, and the proof of Theorem 1.4 does not establish its
claimed asymptotic.  These are load-bearing issues, not editorial polishing.  The promising
next step is a corrected TeX draft plus an independent analytic-number-theory review before
any submission consent or integration of the 300-trillion data.

## Findings

| Priority | Location | Classification | Finding | Required repair |
|---|---|---|---|---|
| 1 | Definition 1.3, eq. (1.3) | **Demonstrably wrong as printed** | The coefficient `(1-chi(a))chi(x)` selects `x=1` minus `x=a^{-1}`, not `x=a`.  Indeed, `chi(a)chi(x)=chi(ax)`, so character orthogonality fires at `ax=1`.  For `N=7, a=3`, the negative class is `5`, because `3^{-1}=5 (mod 7)`. | Replace `1-chi(a)` by `1-conj(chi(a))` (equivalently `1-chi(a^{-1})`) if the intended class is `a`, and propagate that convention through every formula. |
| 2 | Sec. 2.2, eqs. (2.4)-(2.5) | **Unsupported uniform estimate** | For fixed `T`, the Gaussian off-diagonal factor depends on `T^2(log(q^m/p^k))^2`.  Distinct prime powers have logarithmic gaps tending to zero as their size grows, so no positive `c` independent of the summation variables yields the asserted uniform `O(exp(-cT^2))` suppression as `x -> infinity`. | State the actual two-parameter limit, choose and justify a growth regime `T=T(x)` if needed, and prove a summed off-diagonal bound uniform in the full range. |
| 3 | Theorem 1.4 vs. eq. (2.5) | **Internal dependence mismatch** | The theorem says `C_N` depends solely on `N`, but the displayed diagonal term has an explicit factor `T/(4 sqrt(pi))`.  No cancellation removing `T` is shown. | Give the explicit constant and its dependencies.  If it is `C_{N,T}`, state that; if `T` is later optimized or sent to infinity, prove the limiting statement. |
| 4 | Sec. 2.4, eq. (2.11) | **Proof gap** | Equation (2.11) restates the theorem immediately after principal-character cancellation.  Cancellation of the principal character does not evaluate the remaining prime/zero sums or prove the claimed error term. | Supply the missing derivation: legitimate order interchange, diagonal evaluation, off-diagonal estimate, prime-power tails, gamma/conductor terms, and uniform error accounting. |
| 5 | Lemma 2.1 and lines following eq. (2.9) | **Unsupported convergence claim** | The text says DRH controls the non-absolutely convergent `k=1,2` prime-power sum and makes the full sum `O(1)`, but no theorem or estimate establishing this is given. | State the exact DRH consequence used and prove the required convergence/bound with all quantifiers and dependence on `T,N,chi`. |
| 6 | Theorem 1.4 definition of `log L(1,chi_{1,a})` | **Undefined/ambiguous** | For complex characters, `L(1,chi)` and its logarithm are complex.  The logarithm branch, conjugate-pairing, and reality of the claimed ordering statistic are not specified. | Define the logarithm consistently (for example through a convergent Euler-product continuation on a specified branch) and prove the resulting combination is real if a real ordering is claimed. |
| 7 | N=8 examples | **Internal contradiction** | Corollary 1.5 and Sec. 3 give `7 > 3 > 5 > 1`, while Sec. 1.5's printed values imply `7 > 5 > 3 > 1`. | Recompute from one fixed convention and replace every affected table, inequality, and prose statement. |
| 8 | Remark 1.6 vs. Conjecture 1.7 | **Theorem-status contradiction** | Remark 1.6 says universal dominance is rigorously established; the next subsection labels the same unique-minimum statement a conjecture. | Use one status only.  Do not claim a universal theorem without a proof covering every modulus and all relevant classes. |
| 9 | Remark 2.3 | **Heuristic presented too strongly** | The `3.18 x 10^14` scale is obtained from one low-zero phase reaching one destructive node.  It does not prove that all complex-character interference subsides there, nor that a stable ordering begins there. | Label it a one-mode heuristic and compare it to the complete 300-trillion curve without claiming disappearance of the remaining spectrum. |

## Scope warning

The statistic `S_T` is a custom regularized, spectrally weighted statistic.  Even if its
asymptotic is repaired, a separate transfer theorem is needed before interpreting it as a
theorem about eventual rankings or Rubinstein-Sarnak sign densities for the ordinary counts
`pi(x;N,a)-pi(x;N,1)`.  The current 300-trillion data measure the ordinary counts and should
be described as a finite-scale comparison, not as a proof of the regularized theorem.

## Minimum mathematical gate before a joint submission

1. Complete TeX source for the proposed joint draft.
2. Corrected character convention and recomputed examples.
3. A precise theorem with all `N`, `a`, `T`, and limit dependencies explicit.
4. Full proof of the order interchange and summed off-diagonal estimate.
5. Defined complex logarithm and proof of reality of the ranking statistic.
6. Independent review by an analytic number theorist who did not write the proof.
7. Reconciliation of the `N=11, a=10` numerical discrepancy before any table is submitted.


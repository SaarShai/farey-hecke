# A Scoped Farey--Mertens Priority Note

Status tags in this skeleton classify the underlying record as `[LEAN]`, `[EXACT]`, `[NUMERICAL]`, or `[FALSIFIED-CLAIM]`. [EXACT]

## Abstract

For every prime \(p\), the bridge identity
\[
\sum_{f\in\mathcal F_{p-1}} e^{2\pi i p f}=M(p)+2
\]
is recorded as the unconditional Lean theorem `farey_bridge_identity_unconditional`. [LEAN]
The finite witness \(p=92{,}173\) has \(M(p)=-2\) and positive discrete change \(\Delta W(p)=+3.561440773266696686177868\times10^{-11}\). [NUMERICAL]
The witnesses \(p=237{,}733\) and \(p=243{,}799\) have negative R1 cross-term values on the restricted set \(M(p)\leq-3\). [NUMERICAL]
The separate formal integral observable was evaluated exactly: among all \(4{,}617\) primes \(p\leq100{,}000\) with \(M(p)\leq-3\), it agreed with \(\operatorname{sign}(-M(p))\) zero times, and it already fails at \(p=13\). [EXACT]
These witnesses kill the reported pointwise sign conjectures. [FALSIFIED-CLAIM]
They are finite results only; this note is not progress on RH and claims no density-one theorem. [EXACT]
The only novelty claim retained here is the per-step/bridge packaging together with the certified counterexamples; no novelty is claimed for the static Farey--Mertens identity or the prior-art connections. [EXACT]

## Introduction

The Franel--Landau criterion makes the global Farey discrepancy RH-relevant, but the identity and the finite certificates below supply neither a new bound nor a zero-density statement or route to RH. [EXACT]
The scope is therefore a structural and computational note with explicit finite boundaries, not an RH result. [EXACT]

García, “New analytical formulas for the rank of Farey fractions and estimates of the local discrepancy,” *Mathematics* 13(1), article 140 (2025), is prior art for the Farey rank/local-discrepancy side of the Farey--Mertens connection. [EXACT]
Cox--Ghosh--Sultanow, “The Farey Sequence and the Mertens Function,” arXiv:2105.12352 (2021), is prior art for the static Farey--Mertens identities. [EXACT]
Accordingly, the only novelty claim made here is the per-step/bridge packaging plus the certified counterexamples, and nothing more. [EXACT]

## Identities

Let \(\mathcal F_N=\{f_0<\cdots<f_{n-1}\}\), with both endpoints included and \(n=|\mathcal F_N|\). [EXACT]
Define
\[
W(N)=\sum_{j=0}^{n-1}\left(f_j-\frac{j}{n}\right)^2,
\qquad \Delta W(p)=W(p-1)-W(p),
\qquad M(x)=\sum_{m\leq x}\mu(m).
\]
[EXACT]

For every prime \(p\),
\[
\boxed{\displaystyle \sum_{f\in\mathcal F_{p-1}} e^{2\pi i p f}=M(p)+2.}
\]
[LEAN]
The Lean source names the unconditional theorem `FareyBridgeIdentity.farey_bridge_identity_unconditional`; its local `FareySet` represents coprime pairs \((a,b)\) with \(a/b\in[0,1]\) and \(b\leq n\). [LEAN]

The arithmetic decomposition has two endpoint contributions equal to \(2\), while for \(2\leq b<p\) the numerator sum is the Ramanujan sum \(c_b(p)=\mu(b)\) because \((b,p)=1\); hence the sum is \(2+\sum_{b=2}^{p-1}\mu(b)=M(p)+2\). [EXACT]
Taking real parts gives the cosine form, and the imaginary part vanishes under \(f\mapsto1-f\). [EXACT]
The static identity is treated as classical prior art by Cox--Ghosh--Sultanow; the packaging here does not claim that identity as new. [EXACT]

## Counterexamples to pointwise sign claims

The first witness concerns the discrete \(\Delta W\) above. [EXACT]
The other two witnesses concern the distinct R1 cross-term quantity
\[
B_{\mathrm{R1}}(p)=2\sum_{f=a/b\in\mathcal F_{p-1}}
\left(\operatorname{rank}_{\mathrm{R1}}(f)-|\mathcal F_{p-1}|f\right)
\frac{a-(pa\bmod b)}{b},
\]
with \(\operatorname{rank}_{\mathrm{R1}}(0/1)=1\); \(B_{\mathrm{R1}}\) is not \(\Delta W\). [EXACT]

- At \(p=92{,}173\), the recorded output is \(M(p)=-2\) and \(\Delta W(p)=+3.561440773266696686177868\times10^{-11}>0\). [NUMERICAL]
  Therefore the broad pointwise implication \(M(p)<0\Rightarrow\Delta W(p)\leq0\) is killed by this finite witness. [FALSIFIED-CLAIM]
- At \(p=237{,}733\), the recorded output is \(M(p)=-20\) and \(B_{\mathrm{R1}}(p)=-3.018492026640170288085938\times10^{10}<0\). [NUMERICAL]
  Therefore the restricted pointwise assertion \(B_{\mathrm{R1}}(p)\geq0\) for \(M(p)\leq-3\) is killed. [FALSIFIED-CLAIM]
- At \(p=243{,}799\), the recorded output is \(M(p)=-3\) and \(B_{\mathrm{R1}}(p)=-9.190201299936826705932617\times10^{9}<0\). [NUMERICAL]
  This is a second finite witness killing the same restricted R1 positivity assertion. [FALSIFIED-CLAIM]

The two R1 witnesses must not be used as evidence for a universal sign law for the discrete \(\Delta W\), because the quantities and rank conventions differ. [EXACT]
The recorded floating-point signs are computational certificates, not interval-arithmetic or exact-rational proofs. [NUMERICAL]
No frequency, density, limiting probability, universal \(\Delta W\) law, or RH conclusion is claimed. [EXACT]

## Exact integral kill-test data

The separate formal integral observable uses \(\mathcal F_N\subset(0,1]\), including the endpoint \(1\),
\[
D_N(x)=\#\{f\in\mathcal F_N:f\leq x\}-|\mathcal F_N|x,
\qquad W(N)=\int_0^1D_N(x)^2\,dx.
\]
[EXACT]
For this observable,
\[
\Delta W_{\mathrm{int}}(p)=\frac{p-1}{6p}\bigl(A(p-1)-1\bigr),
\qquad
A(x)=\sum_{n\leq x}\frac1n\prod_{q\mid n}(1-q).
\]
[EXACT]

The exact scan found zero agreements with \(\operatorname{sign}(-M(p))\) among all qualifying primes through \(100{,}000\). [EXACT]

| cutoff | qualifying primes with \(M(p)\leq-3\) | agreements |
|---:|---:|---:|
| \(10{,}000\) | \(598\) | \(0\) [EXACT] |
| \(30{,}000\) | \(1{,}732\) | \(0\) [EXACT] |
| \(100{,}000\) | \(4{,}617\) | \(0\) [EXACT] |

The first qualifying prime already fails:
\[
p=13,\qquad M(13)=-3,\qquad A(12)-1=-\frac{95083}{27720},
\]
\[
\Delta W_{\mathrm{int}}(13)=-\frac{95083}{180180}<0,
\qquad \operatorname{sign}(-M(13))=+1.
\]
[EXACT]
Thus the pointwise integral sign relation \(\operatorname{sign}(\Delta W_{\mathrm{int}}(p))=\operatorname{sign}(-M(p))\) is falsified at \(p=13\). [FALSIFIED-CLAIM]
The finite scan is a decisive finite refutation of that pointwise relation, not a proof that any density-one asymptotic is false, and it supplies no numerical support for the submitted direction. [FALSIFIED-CLAIM]

The endpoint \(1\) contributes \(2\langle h_1,h_p\rangle=-(p-1)/(6p)\), changing the load-bearing constant from \(2\) to \(1\); an interior-only Farey portfolio therefore answers a different formal question. [EXACT]
The exact tests compare the closed formula with direct exact piecewise integration at every prime through \(31\), and independently check the Möbius sieve and arithmetic coefficient through \(200\). [EXACT]

## Verification appendix

### A. Lean-proved statement and formal-status boundary

The current Lean source states `farey_bridge_identity_unconditional` as the fully proved version: the conditional `h_ramanujan_decomp` premise is discharged by `RamanujanSum.farey_ramanujan_decomp`, leaving `Nat.Prime p` as the theorem hypothesis. [LEAN]
The named fact ledger records the exact bridge statement but explicitly makes no claim about a freshly checked formalization. [LEAN]
The named fact ledger does not record a `#print axioms` output for this theorem; the exact axiom footprint is therefore unresolved in this assembly and is not guessed here. [LEAN]

### B. Exact-rational computation

The integral scan uses Python `Fraction`; its signs are integer comparisons, while decimal columns are display-only. [EXACT]
The \(p=13\) counterexample and the \(598/0\), \(1{,}732/0\), and \(4{,}617/0\) scan counts above are therefore exact-rational/combinatorial records. [EXACT]

### C. Floating-point computation

The \(92{,}173\), \(237{,}733\), and \(243{,}799\) witnesses were generated by a self-contained C reproducer using a linear Möbius sieve, the standard Farey successor recurrence, and compensated `long double` accumulation. [NUMERICAL]
The recorded signs are stable in those calculations, but the source explicitly says that they are not interval proofs and do not rely on an unrecorded MPFR run. [NUMERICAL]

The recorded reproducer commands are:

```sh
cc -O3 -std=c11 -Wall -Wextra -o /tmp/nw_mertens_reproduce reproduce_numerics.c -lm
/tmp/nw_mertens_reproduce delta 92173
/tmp/nw_mertens_reproduce cross 237733 243799
```
[NUMERICAL]

## References

- R. Tomás García, “New analytical formulas for the rank of Farey fractions and estimates of the local discrepancy,” *Mathematics* 13, no. 1, article 140 (2025). [EXACT]
- D. Cox, S. Ghosh, and E. Sultanow, “The Farey Sequence and the Mertens Function,” arXiv:2105.12352 (2021). [EXACT]
- J. Franel, “Les suites de Farey et le problème des nombres premiers” (1924). [EXACT]
- E. Landau, “Bemerkungen zu der vorstehenden Abhandlung von Herrn Franel” (1924). [EXACT]
- G. H. Hardy and E. M. Wright, *An Introduction to the Theory of Numbers*, 6th ed., Theorem 304, as cited by the Lean source for the Ramanujan-sum step. [EXACT]

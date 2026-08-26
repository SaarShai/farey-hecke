# T1 GAP-13 — dependence on the target dimension d

DRAFT (luna/codex lane) 2026-08-26 — UNREFEREED.

Scope: this note separates the single-tone Fisher coefficient from the actual
\(d\)-dependent constants in T1, derives their asymptotics, and states the
admissible range of \(d\). Upper numerical bounds are rounded UP.

---

## 0. Ruling

The draft's sentence “\(c_d=\sqrt6\) does not grow with \(d\)” is true only
for the **raw single-tone coefficient before evaluating the worst target**.
The headline law has genuine \(d\)-dependence through the ordinate
\(\gamma_d\):

\[
 C_{\rm var}(d)=6\log(\gamma_d/2\pi),\qquad
 C_{\rm RMSE}(d)=\sqrt{6\log(\gamma_d/2\pi)},\qquad
 C_X(d)=\{6\log(\gamma_d/2\pi)\}^{1/3}.
 \tag{0.1}
\]

Here \(C_{\rm RMSE}(d)\) multiplies \(T^{-3/2}\), and \(C_X(d)\) multiplies
\(\varepsilon^{-2/3}\) in \(\log X\). By Riemann–von Mangoldt inversion,

\[
 \log(\gamma_d/2\pi)
 =1+W((d-7/8)/e)+O(\log d/d)
 =\log d-\log\log d+o(1),
 \tag{0.2}
\]

so \(C_{\rm RMSE}(d)\sim\sqrt{6\log d}\) and
\(C_X(d)\sim(6\log d)^{1/3}\).

There is also a separate resolution cost. With

\[
 \Delta_d^+:=\min_{1\le j\le d}(\gamma_{j+1}-\gamma_j),
 \tag{0.3}
\]

the exact (M5) requirement for the first \(d\) targets and a cut above the
last one forces \(T\ge2\pi K/\Delta_d^+\). Consequently the leading-order
combined resource requirement is

\[
 \log X=T\ge
 \max\left\{
   C_X(d)\varepsilon^{-2/3},
   {2\pi K\over\Delta_d^+}
 \right\},
 \tag{0.4}
\]

plus the leakage and regularity hypotheses of T1.

Finally, the draft's claim that the \(O(K^{-1})\) term is **uniform in d** is
not proved by Lemma 3's pairwise estimate. For every fixed finite \(d\), the
argument gives an \(O_d(K^{-1})\) correction. A dimension-uniform
multi-tone frame bound for the frequency-derivative/nuisance family is
**OWED**. Thus the law is presently justified for fixed admissible \(d\),
not for an arbitrary growing sequence \(d=d(T)\).

---

## 1. What d denotes

In the draft,

\[
 \theta=(\gamma_1,\ldots,\gamma_d,A_1,\ldots,A_d,
             \phi_1,\ldots,\phi_d)\in\mathbb R^{3d}.
\]

Thus \(d\in\mathbb N\) is the number of target tones; the statistical
parameter dimension is \(3d\). Clause (M2) assumes a simple point process,
and (M5) separates the target ordinates, so there is no zero multiplicity
inside the claimed theorem. If a zero has multiplicity greater than one,
the line-spectrum parametrization and nonsingular Fisher block used in T1
do not apply; that case is outside the range.

---

## 2. Exact dependence in the displayed T1 law

For each target, the draft derives

\[
 \operatorname{Var}(\widehat\gamma_j)
 \ge {6+O(K^{-1})\over T^3}
       {S_\varepsilon(\gamma_j)\over a_{\gamma_j}^2}.
 \tag{2.1}
\]

Proposition 4.4 gives the exact cancellation

\[
 {S_\varepsilon(\gamma_j)\over a_{\gamma_j}^2}
 =\log(\gamma_j/2\pi)=:L_j.
 \tag{2.2}
\]

Hence, at leading order,

\[
 \operatorname{Var}(\widehat\gamma_j)\ge {6L_j\over T^3},
 \qquad
 \operatorname{RMSE}(\widehat\gamma_j)\ge {\sqrt{6L_j}\over T^{3/2}}.
 \tag{2.3}
\]

Since \(L_j\) increases with \(j\), the maximum lower bound occurs at
\(j=d\), giving (0.1). Solving
\(\sqrt{6L_d}/T^{3/2}\le\varepsilon\) gives

\[
 T\ge(6L_d)^{1/3}\varepsilon^{-2/3},
 \qquad
 X\ge\exp\{(6L_d)^{1/3}\varepsilon^{-2/3}\}.
 \tag{2.4}
\]

This identifies four constants that should not share one symbol:

| quantity | exact leading value | d-dependence |
|---|---:|---|
| single-tone variance coefficient before (2.2) | \(6\) | none |
| draft's raw RMSE coefficient before (2.2) | \(c_d^{\rm raw}=\sqrt6\) | none at leading order |
| headline RMSE numerator | \(C_{\rm RMSE}(d)=\sqrt{6L_d}\) | through \(\gamma_d\) |
| sample-complexity exponent coefficient | \(C_X(d)=(6L_d)^{1/3}\) | through \(\gamma_d\) |

For the draft's tabulated ordinates:

| d | \(L_d\) | \(C_{\rm var}(d)\) | \(C_{\rm RMSE}(d)\) | \(C_X(d)\) |
|---:|---:|---:|---:|---:|
| 1 | 0.810757 | 4.864545 | 2.205571 | 1.694393 |
| 10 | 2.069612 | 12.417674 | 3.523872 | 2.315689 |

The final entry is rounded UP from 2.315688. No amplitude-law or window
factor survives in these leading constants.

---

## 3. Derivation as an explicit function of d

Let \(N_\zeta(H)\) count nontrivial zeros with \(0<\gamma\le H\), with
multiplicity. The Riemann–von Mangoldt formula is

\[
 N_\zeta(H)={H\over2\pi}
       \left(\log{H\over2\pi}-1\right)+{7\over8}+O(\log H).
 \tag{3.1}
\]

Put \(x_d=\gamma_d/(2\pi)\). Away from the endpoint convention at a zero,
(3.1) gives

\[
 d-{7\over8}=x_d(\log x_d-1)+O(\log x_d).
 \tag{3.2}
\]

Ignoring the displayed error for one line and setting \(n=d-7/8\), solve
\(n=x(\log x-1)\). If \(y=\log x-1\), then
\(n=e\,y e^y\), so

\[
 y=W(n/e),\qquad
 x={n\over W(n/e)},\qquad
 \log x=1+W(n/e).
 \tag{3.3}
\]

The derivative of \(x(\log x-1)\) is \(\log x\). Therefore the
\(O(\log x_d)\) error in (3.2) perturbs \(x_d\) by \(O(1)\), and perturbs
\(\log x_d\) by \(O(1/x_d)=O(\log d/d)\). This proves (0.2):

\[
 L_d=1+W((d-7/8)/e)+O(\log d/d).
 \tag{3.4}
\]

Using \(W(z)=\log z-\log\log z+o(1)\),

\[
 \begin{aligned}
 C_{\rm var}(d)&=6\log d-6\log\log d+o(1),\\
 C_{\rm RMSE}(d)&=\sqrt{6\log d}\,(1+o(1)),\\
 C_X(d)&=(6\log d)^{1/3}(1+o(1)).
 \end{aligned}
 \tag{3.5}
\]

Equation (3.4) is asymptotic, not a replacement for the actual ordinate at
small \(d\). A fully explicit two-sided non-asymptotic inversion, with a
chosen published remainder for (3.1), is **OWED** if numerical ranges beyond
the stored zero table are required.

---

## 4. Resolution creates a second d-dependent resource law

For ordered simple targets, define the internal minimum gap

\[
 \Delta_d:=\min_{1\le j<d}(\gamma_{j+1}-\gamma_j),
\]

with \(\Delta_1=+\infty\). Condition (M5) requires

\[
 T\Delta_d\ge2\pi K,
 \qquad
 T(\Gamma-\gamma_d)\ge2\pi K,
 \qquad
 \gamma_d<\Gamma<\gamma_{d+1}.
 \tag{4.1}
\]

Such a cut can exist only if
\(T(\gamma_{d+1}-\gamma_d)>2\pi K\). Combining the internal and top gaps
gives the exact necessary resolution condition

\[
 T\Delta_d^+\ge2\pi K
 \tag{4.2}
\]

up to the strict inequality needed to place \(\Gamma\) above
\(\gamma_d+2\pi K/T\). Equations (2.4) and (4.2) give (0.4), or equivalently

\[
 X\ge\max\left\{
 \exp\{C_X(d)\varepsilon^{-2/3}\},
 \exp\{2\pi K/\Delta_d^+\}
 \right\}.
 \tag{4.3}
\]

This is the precise d-range at fixed \(T\):

\[
 d\le d_{\rm res}(T,K):=\max\left\{m:\
 \min_{1\le j<m}(\gamma_{j+1}-\gamma_j)\ge {2\pi K\over T},\quad
 \gamma_{m+1}-\gamma_m>{2\pi K\over T}\right\},
 \tag{4.4}
\]

and there must also exist a cut satisfying (B1).

At the draft's \(T=17.2167\), \(K=4\),

\[
 {2\pi K\over T}=1.459788<1.460
\]

(upper rounding). Among the first ten targets and the next zero, the smallest
stored gap is
\(\gamma_{10}-\gamma_9=1.768682\), so \(d=10\) passes the gap test. But the
cut \(\Gamma=50\) fails (4.1); it must satisfy

\[
 \Gamma\ge\gamma_{10}+{2\pi K\over T}=51.233620,
\]

so the draft's separately tested \(\Gamma=51.234\) is the admissible one.

The ledger's simpler second law uses the **mean** spacing
\(2\pi/L_d\). Substitution in (4.2) gives the heuristic

\[
 T\gtrsim K L_d,
 \qquad X\gtrsim(\gamma_d/2\pi)^K.
 \tag{4.5}
\]

Equation (4.5) is not a deterministic consequence of Riemann–von Mangoldt:
the minimum of the first \(d\) gaps can be much smaller than the local mean.
Replacing \(\Delta_d^+\) by \(2\pi/L_d\) for actual zeros is **OWED** and
should remain labelled heuristic/model-based.

---

## 5. Does cross-tone coupling add further d-dependence?

Lemma 3 bounds each cross-tone oscillatory integral by a pairwise
\(O(K^{-1})\) term and then says that all blocks invert independently with a
relative \(O(K^{-1})\) error, uniformly in \(d\). Pairwise smallness alone
does not imply a dimension-uniform operator-norm bound: every row contains
\(d-1\) off-diagonal blocks.

For fixed \(d\), finite-dimensional perturbation theory does give

\[
 c_d^{\rm raw}=\sqrt6\{1+O_d(K^{-1})\}.
\tag{5.1}
\]

Writing the actual correction as
\(c_{d,K}^{\rm raw}=\sqrt6\,\kappa_{d,K}\), the corresponding headline and
sample-exponent coefficients are

\[
 C_{{\rm RMSE},K}(d)=\sqrt{6L_d}\,\kappa_{d,K},
 \qquad
 C_{X,K}(d)=(6L_d)^{1/3}\kappa_{d,K}^{2/3}.
 \tag{5.1a}
\]

There is no additional \(\sqrt{\log d}\) “multiple-comparisons” factor in
T1: its loss is the maximum of marginal RMSEs, not a simultaneous confidence
radius or the expectation of the maximum random error.

A conservative summation shows what the current proof sketch can support for
growing \(d\). If the normalized \((j,k)\) block is bounded by
\(C_*/(T|\gamma_j-\gamma_k|)\), then (M5) and ordering imply

\[
 T|\gamma_j-\gamma_k|\ge2\pi K|j-k|,
\]

and the maximum block-row sum is at most

\[
 \eta_d\le {C_*\over\pi K}H_{d-1},
 \qquad H_{d-1}=\sum_{m=1}^{d-1}{1\over m}.
 \tag{5.2}
\]

Provided \(\eta_d<1\), a normalized Gram comparison would change the RMSE
coefficient by at worst a factor \((1+\eta_d)^{-1/2}\). This route requires
\(K\) to dominate \(\log d\), not merely to be a fixed 4.

The constant \(C_*\), the simultaneous normalization of the
\((A_j,\gamma_j,\phi_j)\) blocks, and the matrix comparison used after
(5.2) are **OWED**; (5.2) is a conditional audit bound, not a completed
replacement for Lemma 3.

The draft's true Gram integral is also weighted by
\(1/S_\varepsilon(\nu)\). Lemma 1 whitens one near-tone band at a time, but
the sketch does not derive weighted cross-block estimates over the union of
near bands and the remainder. A spectral dynamic-range factor could
therefore enter \(C_*\). This coloured-weight step is **OWED**.

There is a plausible dimension-free route. Montgomery–Vaughan's generalized
Hilbert inequality gives mean-square/frame bounds independent of the number
of frequencies for a separated family of plain exponentials. T1 needs the
confluent family containing both \(e^{\pm i\gamma_jt}\) and
\(t e^{\pm i\gamma_jt}\), with nuisance-parameter Schur complements and
coloured local whitening. Extending the dimension-free inequality through
those steps is **OWED**. Until then, “uniformly in \(d\)” is underived.

Likewise, “the corrected maximum is attained at \(j=d\)” is automatic only
for the ideal factors \(L_j\). If the unproved corrections
\(\kappa_{j,d,K}\) vary with \(j\), choosing \(j=d\) still gives a valid
candidate lower bound, but actual attainment at \(d\) is **OWED**.

---

## 6. Range of d for which the claims hold

The present proof supports the following precise range.

1. **Integer/simple range:** \(d\ge1\) is finite; the first \(d+1\) zeros
   used to place the cut are simple and ordered. Multiple zeros are outside
   the parametrization.
2. **Resolution range:** \(d\le d_{\rm res}(T,K)\) in (4.4), and a
   \(\Gamma\in(\gamma_d,\gamma_{d+1})\) satisfies the top-margin condition.
3. **Model range:** (RH), (M1)–(M5), (M4′), (M4″), (W′), unbiasedness, and
   the global leakage hypothesis (B1) hold. GAP-9 and the other open T1
   obligations remain model qualifications.
4. **Asymptotic range currently proved by the draft's argument:** each fixed
   admissible \(d\), with \(K\) large enough that the fixed-dimensional
   perturbation is small. Uniformity for \(d=d(T)\to\infty\) is **OWED**.

For the stored low-zero table and the draft's \(T,K\), the first adjacent
gap below \(2\pi K/T\) is
\(\gamma_{20}-\gamma_{19}=1.440150\). Thus the exact contiguous range (4.4)
in that table is **\(d\le18\)**. This is a data-dependent operating range,
not an asymptotic theorem.

There is a second geometry issue in the draft's proof. Its near-tone
intervals have radius \(h=2\pi K/T\), while (M5) requires only gaps at least
\(h\); disjoint near-tone intervals require gaps greater than \(2h\). If
the decomposition in Lemmas 1 and 3 requires disjointness, the stated (M5)
is insufficient. At the same operating point the first gap below \(2h\) is
\(\gamma_5-\gamma_4=2.510186\), so the strengthened contiguous range would
be only \(d\le3\). Whether overlap is harmless under a partitioned
frequency decomposition is **OWED**.

The formal theorem assumes global (B1). The draft's numerical rider reports a
failure at \(\gamma_1\) and a pass at \(\gamma_d\), using per-tone checks.
Those measurements support the headline last-tone constant but do not, as
written, discharge a global \(3d\)-parameter (B1) statement. The global
multi-tone leakage comparison is **OWED** before claiming the every-j law at
the numerical \(d=10\) operating point.

---

## 7. Obligations and status

- **DERIVED:** the exact leading d-dependence (0.1), the sample-complexity
  coefficient, and the Lambert-W asymptotic (0.2).
- **DERIVED:** the exact gap-based admissible range (4.2)–(4.4) and the
  combined accuracy/resolution resource law (4.3).
- **OWED:** a dimension-uniform confluent Ingham/Montgomery–Vaughan bound for
  the full nuisance-parameter Fisher matrix, or an explicit
  \(d\)-dependent replacement for the draft's \(O(K^{-1})\).
- **OWED:** a theorem replacing the minimum gap by the mean-spacing
  surrogate in (4.5); Riemann–von Mangoldt alone cannot do this.
- **OWED:** a global multi-tone verification of (B1).
- **OWED:** an explicit non-asymptotic inversion of the zero-counting
  remainder if (3.4) is to be used for certified numerical d-ranges.

**Status: GAP-13 is closed for the leading fixed-d algebra and remains OPEN
for the claimed uniform-in-d correction.** The correct full leading constant
is \(\sqrt{6\log(\gamma_d/2\pi)}\), asymptotic to
\(\sqrt{6\log d}\), and the law applies only on the gap-admissible range
(4.4) unless stronger multi-tone analysis is supplied.

---

## Sources

- `T1_CRAMER_RAO_DRAFT.md`, Theorem T1, Lemma 3, Proposition 4.4, and GAP-13.
- `G1_MODEL_SPEC.md`, §3-N2 and amendments A1–A2.
- NIST DLMF, §25.10, zero counting and references:
  <https://dlmf.nist.gov/25.10>.
- H. L. Montgomery and R. C. Vaughan, “Hilbert's Inequality,” *J. London
  Math. Soc.* (2) 8 (1974), 73–82, Theorem 2 and Corollary 2:
  <https://doi.org/10.1112/jlms/s2-8.1.73>.
- D. C. Rife and R. R. Boorstyn, “Multiple Tone Parameter Estimation from
  Discrete-Time Observations,” *Bell System Technical Journal* 55 (1976),
  1389–1410 (context for the imported multi-tone CR calculation):
  <https://doi.org/10.1002/j.1538-7305.1976.tb02941.x>.
- Stored ordinate table used for the finite range:
  `lane_k/mertens-zeros-n100k-part2b/zeros1.txt`.

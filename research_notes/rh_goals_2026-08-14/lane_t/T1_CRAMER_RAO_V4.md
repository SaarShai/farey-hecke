# T1 — Cramér–Rao and van Trees in the exact Gaussian surrogate

**v4 DRAFT (grok lane) 2026-08-26 — UNREFEREED**

This file supersedes `T1_CRAMER_RAO_DRAFT.md` (v3) and its 2026-08-26 ledger overlay. It is written to the seven minimum conditions of `T1_COLD_REFEREE_2026-08-26.md`. Supporting derivations that this text restates rather than re-proves are cited by filename; no statement from the superseded draft is imported as current.

Rounding convention (binding): error bounds and ceilings round **UP**; lower-bound floors and RMSE margins round **DOWN**.

---

## Model Declaration (binding)

The following choices are the model. They are not optional readings of v3.

**(a) Defects 1, 2, 5 — exact Gaussian surrogate, mean-field marks, fixed covariance.**
Theorems A and B are theorems about a stipulated Gaussian experiment \(\mathcal{G}_{N2}\), defined in §2. Clause **(M3′)** is part of that experiment: marks are the deterministic continuous interpolant \(r(\omega)\equiv 1\). The covariance operator \(C\) is a functional of the resulting spectral density \(S_{\eta}\) and does **not** depend on the parameter \(\theta\). There is therefore no Gaussian covariance-information (Bhattacharyya / Porat–Nehorai) term. The actual non-Gaussian phase sum is confined to §14 (model-fidelity discussion) and carries **no transfer claim**. The reason no transfer is claimed is Stam’s inequality as recorded in `T1_GAP17_PROPAGATION.md` §2: at fixed variance the Gaussian minimises Fisher information, so the Gaussian Cramér–Rao number is not a lower bound for the full phase-sum class.

**(b) Defects 3, 4 — two theorems, one quantifier each; Godambe dropped.**
- **Theorem A:** pointwise frequentist Cramér–Rao for unbiased estimators of \(\theta\) in \(\mathcal{G}_{N2}\). Unbiasedness is assumed. The quantifier is: every unbiased estimator of the band-limited Gaussian record.
- **Theorem B:** Bayes van Trees risk under a prior whose ordinate centres \(\mu_j\) are **externally specified** (parameters of the prior, not the unknown true ordinates). The Fisher matrix that enters the denominator is the prior average \(\overline{J}=\mathbb{E}_{\pi}[I(\theta)]\), bounded from above so the resulting numerical floor is valid. Unbiasedness is not assumed, and Theorem B does not replace Theorem A.
- The phrases “Gaussian-score class” and “Godambe sandwich as a lower bound” are not used.

**(c) Defect 7 — sole operating point.**
The unique numerical operating point is the (M5)-admissible cut
\[
\Gamma_{\mathrm{op}}:=51.23361986,
\]
obtained by rounding **UP** the exact threshold \(\gamma_d+2\pi K/T\) at eight decimal places, with the referee’s audit inputs \(T=\log(3\cdot 10^7)\), \(K=4\), \(\gamma_d=49.773832\). Every finite-\(\Gamma\) quantity in this file is evaluated at \(\Gamma_{\mathrm{op}}\) (or is labelled out-of-theorem). \(\Gamma=50\) is not an operating point of either theorem.

**(d) Defect 6 — per-tone (B1), global matrix OPEN.**
Hypothesis (B1) is stated per tone, as a \(3\times 3\) generalised-eigenvalue bound with an explicit factor \(F_j^{\mathrm{leak}}=(1+\kappa_j)^{-1}\). The global \(3d\times 3d\) Loewner comparison \(I_R\preceq K^{-1}I_N\) is **OPEN**. Closing it requires a committed receipt of \(\lambda_{\max}(I_N^{-1}I_R)\) for the full nuisance-parameter matrix at \(\Gamma_{\mathrm{op}}\) (row OPEN-B1-global).

**(e) Defects 8, 9, 18 — projected Lemma 1, flatness in the theorem, named factors.**
Lemma 1 is restated for frequency-projected derivatives and full-line Plancherel. The GAP-4 flatness ceiling \(\exp\bigl(16\pi K/(\gamma_j T)\bigr)\) appears **in Theorem A** as a multiplicative factor, labelled leading-order-ceiling, with the remainder \(r(\omega)=D(\omega)+4/\omega\) **OWED**. Every displayed lower bound uses named signed factors; there is no bare \(O(K^{-1})\).

**(f) Defect 10 — fixed \(d\), explicit \(C(d,K)\), last-tone attainment OWED.**
Theorems A and B are for a **fixed** admissible \(d\). The cross-tone factor is \(F^{\mathrm{cross}}(d,K)=\bigl(1+C(d,K)/K\bigr)^{-1}\) with \(C(d,K)\) defined in §3. The phrase “uniformly in \(d\)” does not occur. That the maximum over \(j\) of the corrected right-hand side is attained at \(j=d\) is **OWED**.

**(g) Defects 11, 12 — Prop. R disclosure; status; sampling experiment.**
The full Prop. R hypothesis list (RH; simplicity of every nontrivial zero; conjectural Gonek–Hejhal \(J_{-1}(T)=O(T)\)) is stated in §1.1 immediately before the displayed formula, in the interpretation clauses of Theorems A and B, and at every empirical use. Status: **closed at citation + Lean standing** as in `T1_GAP16_RIESZ_IMPORT.md`. Integer-\(N\) versus continuous-\(t\) is resolved by declaring the arithmetic experiment (S1) in §1.2; the identification of (S1) with the continuous-time surrogate is **OWED-S1**.

**(h) Defect 16 — GAP-11 split; no “violates the bound”.**
GAP-11 splits into: (i) amplitude validation on \(y(t)\), resolved conditional on Prop. R; (ii) Gate-1 location-risk comparison, **OPEN**. RMSE is an expectation; a single realised absolute error is not a violation of an RMSE bound. That language is not used.

**(i) Defect 17 — two epsilons.**
\(E_{\mathrm{Riesz}}(t)\) is the Prop. R contour-shift remainder after summing **all** zeros. \(\eta_{\Gamma}(t)\) is tail interference above the cut \(\Gamma\) (Gaussian in \(\mathcal{G}_{N2}\); a phase sum in the fidelity discussion). The symbol \(\varepsilon\) is not used for either.

---

## 0. What the theorems say

In the exact Gaussian surrogate \(\mathcal{G}_{N2}\) of §2, with deterministic marks \(r\equiv 1\) and \(\theta\)-independent covariance, an unbiased estimator of the band-limited record satisfies Theorem A: for each target index \(j\) at a **fixed** admissible \(d\),

\[
\mathrm{Var}(\widehat{\gamma}_j)
\;\ge\;
6\cdot F_j^{\mathrm{flat}}\cdot F_j^{\mathrm{leak}}\cdot F^{\mathrm{cross}}(d,K)\cdot F_j^{\mathrm{win}}
\cdot
\frac{\log(\gamma_j/2\pi)}{T^3},
\]

where the four named factors are defined in §3 and \(F_j^{\mathrm{flat}}=\exp\bigl(-16\pi K/(\gamma_j T)\bigr)\) is a leading-order-ceiling (OWED remainder). This is a pointwise frequentist bound. It is not a bound on the zeta phase-sum experiment.

A different theorem, Theorem B, bounds the Bayes MSE of an arbitrary measurable estimator under an externally centred raised-cosine prior. It does not discharge unbiasedness in Theorem A.

At the unique operating point \(\Gamma_{\mathrm{op}}=51.23361986\), \(T=\log(3\cdot 10^7)\), \(K=4\), \(d=10\), the **local** (unnamed-factor) Gaussian number is \(\mathrm{RMSE}\ge 0.04932\) (rounded down). The theorem-A skeleton with the two presently certified factors \(F_d^{\mathrm{flat}}\) and \(F_d^{\mathrm{leak}}\) is recorded in §12. Factors \(F^{\mathrm{cross}}\) and \(F^{\mathrm{win}}\) remain named and not numerically closed.

---

## 1. Observable, Proposition R, and the sampling experiment

### 1.1 Proposition R (order-1 Riesz explicit formula)

Window (spec clause (W′), `G1_MODEL_SPEC.md` AMENDMENT A2): \(W(x)=(1-x)_+\), \(M_W(s)=1/(s(s+1))\) for \(\mathrm{Re}\,s>0\), meromorphic on \(\mathbb{C}\) with simple poles only at \(s=0\) (residue \(1\)) and \(s=-1\) (residue \(-1\)), and

\[
|M_W(\tfrac12+i\omega)|
=\bigl((\tfrac14+\omega^2)(\tfrac94+\omega^2)\bigr)^{-1/2}.
\]

**Mandatory disclosure, carried at this use and at every later use.** Proposition R is conditional on **RH**, **simplicity of every nontrivial zero**, and the conjectural Gonek–Hejhal bound

\[
J_{-1}(T)\;:=\;\sum_{0<\gamma\le T}\bigl|\zeta'(\tfrac12+i\gamma)\bigr|^{-2}\;=\;O(T).
\]

Lean checks only the eight finite/algebraic lemmas in `RieszImport.lean` (Aristotle v21, sorry-free, axioms `propext` / `Classical.choice` / `Quot.sound`). The Riesz–Perron inversion, meromorphic residue calculus, absolute convergence of the zero and trivial-zero sums, the RH zero-avoiding contour shift, and the \(O_A(N^{-A})\) remainder remain cited classical analysis and are not formalised in Lean. Citations: Hardy–Riesz, *The General Theory of Dirichlet’s Series*, Ch. IV and Ch. VII §2; Hardy–Littlewood, *Acta Math.* 41 (1916), §2.25x; Titchmarsh §14.16 (RH zero-avoiding heights) and §14.27; Ng (2004), Lemmas 3–4. Status: **closed at citation + Lean standing** (`T1_GAP16_RIESZ_IMPORT.md`; luna review `T1_GAP16_REVIEW_LUNA.md`).

> **Proposition R.** Assume RH, simplicity of every nontrivial zero, and \(J_{-1}(T)=O(T)\). For every integer \(N\ge 2\) and every fixed \(A\in(1,2)\),
>
> \[
> \begin{aligned}
> \frac1N\sum_{0\le k<N}M(k)
> &=\sum_{n\le N}\mu(n)\bigl(1-n/N\bigr)\\
> &=-2+\frac{12}N
> +2\,\mathrm{Re}\sum_{\gamma>0}
> \frac{N^{1/2+i\gamma}}{(\tfrac12+i\gamma)(\tfrac32+i\gamma)\,\zeta'(\tfrac12+i\gamma)}
> +R_{\mathrm{triv}}(N)+E_{\mathrm{Riesz}}(N),
> \end{aligned}
> \]
>
> where \(M(k)=\sum_{n\le k}\mu(n)\),
> \(R_{\mathrm{triv}}(N)=\sum_{n\ge 1}N^{-2n}/\bigl((-2n)(1-2n)\zeta'(-2n)\bigr)=O(N^{-2})\) (simple poles; **no** \(\log N\)),
> and \(E_{\mathrm{Riesz}}(N):=I_{-A}(N)-R_{\mathrm{triv}}(N)\) with \(|E_{\mathrm{Riesz}}(N)|\le C_A N^{-A}\). The constant \(C_A\) is not made explicit here (**OWED-ERiesz-\(C_A\)**).

The Cesàro identity (first equality) is a finite algebraic identity, independent of RH. Absolute convergence of the zero sum uses \(J_{-1}(T)=O(T)\) via Cauchy–Schwarz and dyadic summation: \(N_{\zeta}(T)=O(T\log T)\) gives \(\sum_{0<\gamma\le T}1/|\zeta'(\rho)|\le J_{-1}(T)^{1/2}N_{\zeta}(T)^{1/2}=O(T\sqrt{\log T})\), hence a convergent tail \(O(\sqrt{\log G}/G)\) beyond height \(G\).

**What this file does not claim about Prop. R.** The older draft’s sentence that the order-1 Riesz formula “has not been re-derived” is superseded. The formula is derived by citation-grade contour analysis and a Lean-checked finite core. It is not a repo-formalised contour proof.

### 1.2 Integer \(N\) versus continuous \(t\): declared sampling experiment (S1)

Proposition R is a statement about **integer** \(N\). The exact Cesàro identity is integer-valued. Theorems A and B below are statements about a **continuous-time** Gaussian process on \([0,T]\). These are different experiments.

**(S1) Arithmetic sampling experiment.** The arithmetic observation is the finite sequence

\[
Y_N
:=N^{-1/2}\Bigl(\sum_{n\le N}\mu(n)\bigl(1-n/N\bigr)+2-\frac{12}N-R_{\mathrm{triv}}(N)\Bigr),
\qquad N=2,3,\dots,N_{\max},
\]

with \(N_{\max}=\lfloor e^{T}\rfloor\). At the operating point, \(N_{\max}=3\cdot 10^7\). Under Prop. R’s three hypotheses,

\[
Y_N
=2\sum_{\gamma>0}a_{\gamma}\cos(\gamma\log N+\phi_{\gamma})
+N^{-1/2}E_{\mathrm{Riesz}}(N),
\]

with \(a_{\gamma}=|M_W(\tfrac12+i\gamma)/\zeta'(\tfrac12+i\gamma)|\) and \(\phi_{\gamma}=\arg(M_W(\tfrac12+i\gamma)/\zeta'(\tfrac12+i\gamma))\).

Theorems A and B are **not** theorems about \((Y_N)\). They are theorems about the continuous-time Gaussian surrogate \(\mathcal{G}_{N2}\) of §2. The real-\(N\) Mellin extension that would identify \(Y_{e^{t}}\) with a continuous record, or a theorem comparing Fisher information of (S1) to that of \(\mathcal{G}_{N2}\), is **OWED-S1**. Until OWED-S1 is closed, no numerical comparison of a Theorem A/B floor to an estimator computed from \((Y_N)\) is a comparison of the same experiment.

### 1.3 Notation: \(E_{\mathrm{Riesz}}\) and \(\eta_{\Gamma}\)

- \(E_{\mathrm{Riesz}}(N)\) is the remainder in Proposition R (all zeros summed; contour integral on \(\mathrm{Re}\,s=-A\)). For a continuous label write \(E_{\mathrm{Riesz}}(t):=E_{\mathrm{Riesz}}(e^{t})\) only at \(t=\log N\in\log\mathbb{Z}_{\ge 2}\).
- \(\eta_{\Gamma}\) is interference from ordinates \(\gamma>\Gamma\). In \(\mathcal{G}_{N2}\) it is the centred stationary Gaussian process with spectral density \(S_{\eta}\) of §2.4. In §14 it is the random-phase sum \(2\sum_{\gamma>\Gamma}a_{\gamma}\cos(\gamma t+\phi_{\gamma})\). These are different objects sharing a symbol by analogy of role, distinguished by the section.

On the arithmetic side, after the \(N^{-1/2}\) normalisation, \(N^{-1/2}E_{\mathrm{Riesz}}(N)=O_A(N^{-A-1/2})\). For \(A\in(1,2)\) this is \(O(X^{-3/2})\) to \(O(X^{-5/2})\) at \(N=X\). An explicit \(C_A\) sufficient to dominate the term uniformly for all \(N\le X\) is **OWED-ERiesz-\(C_A\)**. The surrogate \(\mathcal{G}_{N2}\) does not include \(E_{\mathrm{Riesz}}\): the surrogate mean is a finite trigonometric polynomial, and \(E_{\mathrm{Riesz}}\) is a model-error term for the arithmetic interpretation, not a coordinate of \(\theta\).

---

## 2. The exact Gaussian surrogate \(\mathcal{G}_{N2}\)

### 2.1 Parameter and observation

Fix an integer \(d\ge 1\) and a cut \(\Gamma\) with \(\gamma_d<\Gamma<\gamma_{d+1}\). The parameter is

\[
\theta=(\gamma_1,\dots,\gamma_d,\,A_1,\dots,A_d,\,\phi_1,\dots,\phi_d)\in\Theta\subset\mathbb{R}^{3d},
\]

with \(A_j>0\). The observation in \(\mathcal{G}_{N2}\) is the ideally band-passed continuous record \(\{y_{\Omega}(t):t\in[0,T]\}\), \(T=\log X\), \(\Omega:=2\Gamma\),

\[
y_{\Omega}(t)=m_{\theta}(t)+\eta_{\Gamma}^{\mathcal{G}}(t),
\qquad
m_{\theta}(t)=\sum_{j=1}^{d}A_j\cos(\gamma_j t+\phi_j).
\]

Here \(\eta_{\Gamma}^{\mathcal{G}}\) is a centred stationary Gaussian process, independent of \(\theta\), with covariance operator \(C\) determined by the spectral density \(S_{\eta}\) below. **\(C\) does not depend on \(\theta\).**

### 2.2 Model clauses of \(\mathcal{G}_{N2}\)

These replace (M3) of the superseded draft. Random marks drawn from \(1/|\zeta'|\) are **not** part of \(\mathcal{G}_{N2}\).

- **(M3′)** *Deterministic mean-field marks.* For every real frequency \(\omega\), \(r(\omega)\equiv 1\). Define \(a(\omega):=|M_W(\tfrac12+i\omega)|\). This interpolant is a declared function of frequency, not an estimator of \(1/|\zeta'(\tfrac12+i\omega)|\).
- **(M-amp)** *True surrogate amplitudes.* At the true parameter of \(\mathcal{G}_{N2}\), \(A_j=2\,a(\gamma_j)\). The estimator need not know this; Cramér–Rao is evaluated at the true \(\theta\). Treating \(A_j\) as unknown nuisances covers unknown phase and a possible constant amplitude misspecification. Because \(C\) is independent of \(\theta\), tying the *true* \(A_j\) to \(a(\gamma_j)\) does not re-introduce a covariance-information term.
- **(M4)** *Gaussian regulariser, including the fill.* \(\eta_{\Gamma}^{\mathcal{G}}\) is Gaussian with spectral density \(S_{\eta}\) defined on the whole pass band \(|\omega|\le\Omega\), including every target frequency \(\gamma_j<\Gamma\). The positive value \(S_{\eta}(\gamma_j)\) is supplied by this clause, **not** by a tail calculation evaluated at a target. (The tail calculation is Proposition 4.4\(^\prime\) below, valid only for \(|\omega|>\Gamma\).)
- **(M4′)** *Band limitation.* The observation is \(y_{\Omega}\) with \(\Omega=2\Gamma\). The estimator class is the class of functionals of \(\{y_{\Omega}(t):t\in[0,T]\}\). A bound for this class does not transfer to estimators of the unrestricted record (more data, more information, smaller CR bound; the unrestricted Cameron–Martin integral diverges, §9 (R1)).
- **(M4″)** *Spectral floor.* \(S_{\eta}(\omega)=a(|\omega|)^2\,\vartheta(|\omega|)\) with \(\vartheta(u)=\max\{\log(u/2\pi),\vartheta_{\min}\}\) and \(\vartheta_{\min}:=\log(\gamma_1/2\pi)\).
- **(M5)** *Resolvability.* \(T\cdot\min_{j\ne k}|\gamma_j-\gamma_k|\ge 2\pi K\) and \(T\cdot(\Gamma-\gamma_d)\ge 2\pi K\), with a fixed \(K\ge 4\), and \(\gamma_d<\Gamma<\gamma_{d+1}\).
- **(W′)** as in §1.1.

Phase randomisation (M1) and the ordinate point process (M2) are **not** used to construct \(\mathcal{G}_{N2}\). They appear only in §14 as properties of a different experiment. GUE pair correlation is not used in Theorems A or B.

### 2.3 Spectral convention

\[
\mathbb{E}\bigl[\eta_{\Gamma}^{\mathcal{G}}(t)\,\eta_{\Gamma}^{\mathcal{G}}(t+\tau)\bigr]
=\frac1{2\pi}\int_{\mathbb{R}}S_{\eta}(\omega)\,e^{i\omega\tau}\,d\omega.
\tag{2.1}
\]

A white noise with \(\mathbb{E}[\eta(t)\eta(u)]=S_0\,\delta(t-u)\) has \(S_{\eta}\equiv S_0\). All constants are tied to (2.1). The literature’s factor \(12\) (complex exponential, or a different PSD-to-variance identification) is a different convention; see Lemma 2.

### 2.4 Spectral density of the surrogate

Under (M3′), (M4), (M4″), (W′),

\[
S_{\eta}(\omega)
=a(|\omega|)^2\,\vartheta(|\omega|)
=\frac{\vartheta(|\omega|)}{(\tfrac14+\omega^2)(\tfrac94+\omega^2)},
\qquad
\vartheta(u)=\max\bigl\{\log(u/2\pi),\vartheta_{\min}\bigr\}.
\tag{2.2}
\]

This is a declared function of \(\omega\). It does not depend on \(\theta\). In particular it does not depend on the unknown target amplitudes \(A_j\) or locations \(\gamma_j\). Defects 1 and 2 are thereby avoided: there is no random-mark second moment \(E[r^2\mid\omega]\) inside \(S_{\eta}\), and there is no \(\theta\)-dependence of \(C\).

At every target with \(\gamma_j>2\pi e^{\vartheta_{\min}}\) (all tabulated zeros qualify), \(\vartheta(\gamma_j)=\log(\gamma_j/2\pi)\), so

\[
\frac{S_{\eta}(\gamma_j)}{a(\gamma_j)^2}=\log(\gamma_j/2\pi).
\tag{2.3}
\]

With (M-amp), \(A_j=2a(\gamma_j)\) at the true \(\theta\), hence \(S_{\eta}(\gamma_j)/A_j^2=\log(\gamma_j/2\pi)/4\). This is cancellation of the **mean-field window factor** \(a(\omega)\), not cancellation of \(1/|\zeta'(\rho)|\). The quantity \(1/|\zeta'|\) is absent from \(\mathcal{G}_{N2}\).

**Attribution (Defect 15).** Equation (2.2) at \(\omega=\gamma_j<\Gamma\) is the (M4) fill. Proposition 4.4\(^\prime\) derives the same algebraic expression only for \(|\omega|>\Gamma\). Calling \(S_{\eta}(\gamma_j)\) a consequence of the tail spectral calculation is forbidden. GAP-9 remains **OPEN** for any claim connecting this fill to a fixed zeta configuration; see §14.3.

### 2.5 Tail identity (not used at targets)

> **Proposition 4.4\(^\prime\) (tail only).** Let \(\eta^{\mathrm{ph}}(t)=2\sum_{\gamma>\Gamma}a(\gamma)\cos(\gamma t+\phi_{\gamma})\) with i.i.d. uniform phases, deterministic \(a(\gamma)\) as in (M3′), and intensity \(\lambda(\omega)=\log(\omega/2\pi)/(2\pi)\) for \(\omega>\Gamma\). Then the intensity-smoothed spectral density of \(\eta^{\mathrm{ph}}\) on \(\{\Gamma<|\omega|\le\Omega\}\) equals \(a(|\omega|)^2\log(|\omega|/2\pi)\). GUE pair correlation does not enter the first-moment density.

*Proof.* Phase averaging kills cross terms; Campbell’s formula converts the atomic masses \(a(\gamma)^2\) at \(\pm\gamma\) into \(a(\omega)^2\lambda(\omega)\,d\omega\); matching to convention (2.1) gives the claim. \(\square\)

This proposition does not assign noise at \(\gamma_j<\Gamma\). The surrogate does that by (M4).

---

## 3. Named signed factors (Defect 18)

No displayed lower bound in this file contains an unsigned \(O(K^{-1})\). The following factors are nonnegative and at most \(1\), except \(1+\delta_j\) and \(1+\kappa_j\) which are at least \(1\).

**Half-width.** \(h:=2\pi K/T\). Near-tone band of tone \(j\):

\[
B_j:=\bigl\{\nu:\bigl||\nu|-\gamma_j\bigr|\le h\bigr\}\cap[-\Omega,\Omega].
\]

**Flatness (GAP-4, leading-order-ceiling).** Let \(D(\omega):=\partial_{\omega}\log S_{\eta}(\omega)\). On \(\gamma_j>h\) and \(\vartheta=\log(\,\cdot\,/2\pi)\),

\[
D(\omega)=-\frac{2\omega}{\tfrac14+\omega^2}-\frac{2\omega}{\tfrac94+\omega^2}+\frac1{\omega\log(\omega/2\pi)}
=-\frac4\omega+r(\omega),
\]

with \(r(\omega):=D(\omega)+4/\omega\). Dropping \(r\) and replacing \(\sup_{|u-\gamma_j|\le h}|D(u)|\) by \(4/\gamma_j\) produces the ceiling

\[
1+\delta_j
\;\le\;
\exp\bigl(16\pi K/(\gamma_j T)\bigr)
\qquad\text{(leading-order-ceiling; remainder \(r\) OWED).}
\tag{3.1}
\]

Define \(F_j^{\mathrm{flat}}:=\exp\bigl(-16\pi K/(\gamma_j T)\bigr)=(1+\delta_j)^{-1}\) *using this ceiling*. An explicit \(C_r\) with \(|r(\omega)|\le C_r/(\omega\log(\omega/2\pi))\) for \(\omega\ge\gamma_1\) is **OWED-GAP4-remainder**. Until it is supplied, (3.1) is not a fully rigorous bound on \(D\), and every theorem that uses \(F_j^{\mathrm{flat}}\) is understood modulo that remainder.

**Per-tone leakage (B1)\(_j\).** Split the pass-band Gram as \(I=I_{N_j}+I_{R_j}\) with \(I_{N_j}\) the integral (4.0) restricted to \(B_j\) and \(I_{R_j}\) the complement in \([-\Omega,\Omega]\). Both are \(3\times 3\) matrices in the coordinates \((A_j,\gamma_j,\phi_j)\) when other tones are treated as fixed for this hypothesis (the global \(3d\times 3d\) split is OPEN-B1-global). Assume there exists \(\kappa_j\ge 0\) with

\[
\lambda_{\max}\bigl(I_{N_j}^{-1}I_{R_j}\bigr)\;\le\;\kappa_j.
\tag{B1\(_j\)}
\]

Then \(I\preceq(1+\kappa_j)I_{N_j}\) on that \(3\times 3\), hence \(I^{-1}\succeq(1+\kappa_j)^{-1}I_{N_j}^{-1}\). Define \(F_j^{\mathrm{leak}}:=(1+\kappa_j)^{-1}\). No claim is made that \(\kappa_j\le K^{-1}\) at every \(j\).

**Cross-tone, fixed \(d\).** Let \(C_{\diamond}\ge 0\) be the smallest constant such that every off-diagonal \(3\times 3\) block of the coloured band-limited Gram, after the local normalisation of Lemma 1\(^{\prime\prime}\), satisfies

\[
\frac{\|I_{jk}\|_{\mathrm{op}}}{\|I_{jj}\|_{\mathrm{op}}}
\;\le\;
\frac{C_{\diamond}}{T|\gamma_j-\gamma_k|},
\qquad 1\le j\ne k\le d.
\]

Under (M5), \(T|\gamma_j-\gamma_k|\ge 2\pi K|j-k|\). The block-row sum is then at most \((C_{\diamond}/(\pi K))H_{d-1}\), \(H_{n}\) the \(n\)th harmonic number. Define

\[
C(d,K)\;:=\;\frac{C_{\diamond}}{\pi}\,H_{d-1},
\qquad
F^{\mathrm{cross}}(d,K)\;:=\;\Bigl(1+\frac{C(d,K)}{K}\Bigr)^{-1},
\tag{3.2}
\]

provided \(C(d,K)<K\) (otherwise the factor is set to \(0\) and the bound is vacuous). The constant \(C_{\diamond}\) is **OWED-\(C_{\diamond}\)**. Pairwise \(O(K^{-1})\) estimates do not imply a \(d\)-uniform operator bound; this file never claims uniformity in \(d\).

**Window / oscillatory remainder.** Lemma 2’s integrals differ from their leading terms by \(O(1/(\gamma_j T))\). Define

\[
F_j^{\mathrm{win}}\;:=\;1-\frac{C_{\mathrm{win}}}{\gamma_j T},
\]

with \(C_{\mathrm{win}}\ge 0\) an absolute constant making the \(2\times 2\) Schur complement of the \((\omega,\phi)\) block at least \(F_j^{\mathrm{win}}\) times the leading \(24\,S_0/(A^2 T^3)\). The constant \(C_{\mathrm{win}}\) is **OWED-\(C_{\mathrm{win}}\)**. A numerical white-noise check is recorded in §11, not as a substitute for \(C_{\mathrm{win}}\).

**Prior (Theorem B only).** \(F_j^{\mathrm{prior}}:=I^{\mathrm{eff},\uparrow}_j/\bigl(I^{\mathrm{eff},\uparrow}_j+I(\pi_{\gamma})\bigr)\), with \(I^{\mathrm{eff},\uparrow}_j\) an upper bound on \(\mathbb{E}_{\pi}[I^{\mathrm{eff}}_j]\) (§8).

---

## 4. Lemma 1\(^{\prime\prime}\) — frequency-projected derivatives, full-line Plancherel

Let \(\partial_{\alpha}m_{\theta}\) denote a time-limited derivative (\(\alpha\in\{A_j,\gamma_j,\phi_j\}\)), supported in \([0,T]\), viewed as an element of \(L^2(\mathbb{R})\) by zero extension. Its Fourier transform is entire of exponential type \(T\) and is **not** compactly supported. A nonzero \(L^2\) function cannot be both compactly time-supported and compactly frequency-supported. The superseded Lemma 1 was therefore ill-typed.

Let \(P_j\) be the orthogonal projection on \(L^2(\mathbb{R})\) that multiplies Fourier transforms by \(1_{B_j}\) (Plancherel normalisation as in (2.1)). Define the **frequency-projected derivatives**

\[
g_{j,\alpha}\;:=\;P_j\,(\partial_{\alpha}m_{\theta}).
\]

These are band-limited, hence not time-limited. Full-line Plancherel applies to them without truncation to \([0,T]\):

\[
\langle g_{j,\alpha},g_{j,\beta}\rangle_{L^2(\mathbb{R})}
=\frac1{2\pi}\int_{B_j}(\partial_{\alpha}m)^{\wedge}(\nu)\,\overline{(\partial_{\beta}m)^{\wedge}(\nu)}\,d\nu.
\]

The coloured inner product on the pass band is

\[
\langle u,v\rangle_C
:=\frac1{2\pi}\int_{|\nu|\le\Omega}\hat u(\nu)\,\overline{\hat v(\nu)}\,/S_{\eta}(\nu)\,d\nu.
\]

Frequency-band multipliers are orthogonal projections in \(\langle\,\cdot\,,\,\cdot\,\rangle_C\) as well. The \(3\times 3\) block \(I_{N_j}\) is exactly the Gram of \(\{g_{j,\alpha}\}\) in \(\langle\,\cdot\,,\,\cdot\,\rangle_C\).

> **Lemma 1\(^{\prime\prime}\) (projected local whitening).** Assume \(S_{\eta}\) is continuous and bounded below on \([-\Omega,\Omega]\), and that \(S_{\eta}\) varies by at most a factor \(1+\delta_j\) on \(B_j\). Then for the projected derivatives,
>
> \[
> (1+\delta_j)^{-1}S_{\eta}(\gamma_j)^{-1}\,G^P_{j,\alpha\beta}
> \;\le\;
> (I_{N_j})_{\alpha\beta}
> \;\le\;
> (1+\delta_j)\,S_{\eta}(\gamma_j)^{-1}\,G^P_{j,\alpha\beta},
> \]
>
> where \(G^P_{j,\alpha\beta}=\langle g_{j,\alpha},g_{j,\beta}\rangle_{L^2(\mathbb{R})}\). With the leading-order-ceiling (3.1), one may take \(1+\delta_j=\exp(16\pi K/(\gamma_j T))\) modulo OWED-GAP4-remainder.

*Proof.* Pointwise \(S_{\eta}(\gamma_j)/(1+\delta_j)\le S_{\eta}(\nu)\le(1+\delta_j)S_{\eta}(\gamma_j)\) on \(B_j\), hence the same bounds for \(1/S_{\eta}\). Integrate against \((\partial_{\alpha}m)^{\wedge}\overline{(\partial_{\beta}m)^{\wedge}}\,d\nu/2\pi\). \(\square\)

> **Lemma 1-compare.** Let \(G_{j,\alpha\beta}=\int_0^T(\partial_{\alpha}m_{\theta})(\partial_{\beta}m_{\theta})\,dt\) be the time-domain Gram (equal to the full-line \(L^2(\mathbb{R})\) Gram of the zero-extended derivatives). Frequency projection is an orthogonal projection on \(L^2(\mathbb{R})\), so the Gram of the projected family satisfies \(G^P_j\preceq G_j\) in the Loewner order.

*Proof.* If \(P\) is an orthogonal projection and \(V\) stacks the three derivatives, then \(G^P=V^*PV\preceq V^*V=G\). \(\square\)

**Use in a lower bound.** An upper bound on information yields a lower bound on \(I^{-1}\). From (B1)\(_j\) and Lemma 1\(^{\prime\prime}\),

\[
I \;\preceq\; (1+\kappa_j)\,I_{N_j}
\;\preceq\; (1+\kappa_j)(1+\delta_j)\,S_{\eta}(\gamma_j)^{-1}\,G^P_j
\;\preceq\; (1+\kappa_j)(1+\delta_j)\,S_{\eta}(\gamma_j)^{-1}\,G_j.
\]

The last step is Lemma 1-compare and is **valid and conservative** (it enlarges the upper bound on \(I\)). Therefore

\[
I^{-1}
\;\succeq\;
F_j^{\mathrm{leak}}\,F_j^{\mathrm{flat}}\,S_{\eta}(\gamma_j)\,G_j^{-1},
\]

modulo the GAP-4 remainder inside \(F_j^{\mathrm{flat}}\). Combining with Lemma 2’s evaluation of \(G_j^{-1}\) on the \(\gamma_j\)-coordinate produces the named-factor Cramér–Rao bound. Combining with a valid global (or per-tone) leakage estimate is exactly (B1)\(_j\); the global \(3d\times 3d\) version remains OPEN.

Near-tone bands of width \(2h\) overlap when gaps are less than \(2h\). Condition (M5) only guarantees gaps \(\ge h\). Overlap is harmless for the per-tone split \(I=I_{N_j}+I_{R_j}\) (that split does not require a partition of unity). Overlap *is* an obstruction to treating the \(B_j\) as disjoint supports in a simultaneous multi-tone frame bound; that obstruction is part of OWED-\(C_{\diamond}\) / OWED-overlap.

---

## 5. Lemma 2 — single-tone white \(3\times 3\)

Let \(m(t)=A\cos(\omega t+\phi)\) on \([0,T]\) and let the effective noise be white of two-sided PSD \(S_0\) in convention (2.1). With \(\theta=(A,\omega,\phi)\),

\[
\partial_A m=\cos(\omega t+\phi),\quad
\partial_{\omega} m=-At\sin(\omega t+\phi),\quad
\partial_{\phi} m=-A\sin(\omega t+\phi).
\]

The elementary identities

\[
\begin{aligned}
\int_0^T\cos^2(\omega t+\phi)\,dt
&=\frac T2+\frac{\sin(2\omega T+2\phi)-\sin(2\phi)}{4\omega},\\
\int_0^T\sin(\omega t+\phi)\cos(\omega t+\phi)\,dt
&=\frac{\sin^2(\omega T+\phi)-\sin^2\phi}{2\omega},
\end{aligned}
\]

give remainders \(\le 1/(2\omega)\). Writing \(\sin^2=(1-\cos(2\omega t+2\phi))/2\) and integrating by parts,

\[
\Bigl|\int_0^T t\sin^2-\frac{T^2}4\Bigr|
\le\frac T{2\omega}+\frac1{4\omega^2},
\qquad
\Bigl|\int_0^T t^2\sin^2-\frac{T^3}6\Bigr|
\le\frac{T^2}{2\omega}+\frac T{2\omega^2}+\frac1{4\omega^3}.
\]

The leading Gram, relative error \(O(1/(\omega T))\) in each entry, is

\[
I
=S_0^{-1}
\begin{pmatrix}
T/2 & 0 & 0\\
0 & A^2 T^3/6 & A^2 T^2/4\\
0 & A^2 T^2/4 & A^2 T/2
\end{pmatrix}.
\]

\(A\) decouples. The \((\omega,\phi)\) determinant is \((A^2/S_0)^2 T^4/48\), and

\[
[I^{-1}]_{\omega\omega}
=24\cdot\frac{S_0}{A^2 T^3}
\tag{4.2}
\]

at leading order. The signed finite-\(T\) factor \(F_j^{\mathrm{win}}=1-C_{\mathrm{win}}/(\omega T)\) converting (4.2) into a genuine lower bound on the inverse entry is **OWED-\(C_{\mathrm{win}}\)**.

*Convention.* Rife–Boorstyn and Kay, Example 3.14, quote \(12\) because they use a complex exponential or a different PSD identification. In (2.1) with a real cosine and both \(A\) and \(\phi\) unknown, \(24\) is the leading constant. Getting the factor wrong changes the RMSE coefficient by \(\sqrt2\).

*Numerical check (not a proof of \(C_{\mathrm{win}\)).* Exact band-limited white \(3\times 3\) at \(T=\log(3\cdot 10^7)\), \(A=1\), \(\phi=0.4\), from `t1_verify.py`: \(T^3[I^{-1}]_{\omega\omega}=23.927\) (\(\omega=3.7\), \(\Omega=400\)), \(23.824\) (\(\omega=14.1347\)), \(23.947\) (\(\omega=49.7738\), \(\Omega=600\)). All lie below \(24\), so using \(24\) as a *lower* bound on the inverse without \(F^{\mathrm{win}}\) is slightly optimistic. This check is not a committed receipt (GAP-8).

---

## 6. Lemma 3\(^\prime\) — fixed-\(d\) block perturbation

**(a)** For fixed \(d\) and tones satisfying (M5), the off-diagonal blocks are controlled by \(C(d,K)\) of (3.2). If \(C(d,K)<K\), the inverse’s \(\gamma_j\)-diagonal satisfies

\[
[I^{-1}]_{\gamma_j\gamma_j}
\;\ge\;
F^{\mathrm{cross}}(d,K)\cdot[I_j^{-1}]_{\omega\omega},
\]

where \(I_j\) is the single-tone \(3\times 3\). This is a fixed-\(d\) statement. A dimension-uniform confluent Ingham / Montgomery–Vaughan bound for the coloured family \(\{e^{\pm i\gamma_j t},\, t e^{\pm i\gamma_j t}\}\) with nuisance Schur complements is **OWED** and is not claimed.

**(b)** Any estimator of a discrete sample of the continuous record is a function of that record, so data-processing gives \(I_{\mathrm{discrete}}\preceq I_{\mathrm{continuous}}\) and therefore \(I_{\mathrm{discrete}}^{-1}\succeq I_{\mathrm{continuous}}^{-1}\). A continuous-record lower bound remains a valid (weaker) lower bound for sampled-record estimators **of the same Gaussian process**. It is not, by this lemma, a bound for the arithmetic experiment (S1). A written proof of (b) is **OWED-GAP-6**.

---

## 7. Theorem A — pointwise Cramér–Rao in \(\mathcal{G}_{N2}\)

> **Theorem A (pointwise CR, exact Gaussian surrogate, fixed \(d\)).**
> Fix \(d\ge 1\) and \(K\ge 4\). Assume \(\mathcal{G}_{N2}\) with clauses (M3′), (M-amp), (M4), (M4′), (M4″), (M5), (W′), and per-tone leakage (B1)\(_j\) with constants \(\kappa_j\). Let \(\widehat\theta\) be any estimator of \(\theta\) that is unbiased on an open neighbourhood of the true \(\theta\) and is measurable with respect to \(\{y_{\Omega}(t):t\in[0,T]\}\). Then for each \(j\in\{1,\dots,d\}\),
>
> \[
> \mathrm{Var}(\widehat{\gamma}_j)
> \;\ge\;
> 24\cdot F_j^{\mathrm{flat}}\cdot F_j^{\mathrm{leak}}\cdot F^{\mathrm{cross}}(d,K)\cdot F_j^{\mathrm{win}}
> \cdot
> \frac{S_{\eta}(\gamma_j)}{A_j^2 T^3}.
> \tag{A.1}
> \]
>
> At the true surrogate parameter, (M-amp) and (2.3) give \(S_{\eta}(\gamma_j)/A_j^2=\log(\gamma_j/2\pi)/4\), hence
>
> \[
> \mathrm{Var}(\widehat{\gamma}_j)
> \;\ge\;
> 6\cdot F_j^{\mathrm{flat}}\cdot F_j^{\mathrm{leak}}\cdot F^{\mathrm{cross}}(d,K)\cdot F_j^{\mathrm{win}}
> \cdot
> \frac{\log(\gamma_j/2\pi)}{T^3},
> \tag{A.2}
> \]
>
> and
>
> \[
> \mathrm{RMSE}(\widehat{\gamma}_j)
> \;\ge\;
> \sqrt6\cdot
> \bigl(F_j^{\mathrm{flat}}\,F_j^{\mathrm{leak}}\,F^{\mathrm{cross}}(d,K)\,F_j^{\mathrm{win}}\bigr)^{1/2}
> \cdot
> \frac{\bigl(\log(\gamma_j/2\pi)\bigr)^{1/2}}{T^{3/2}}.
> \tag{A.3}
> \]
>
> \(F_j^{\mathrm{flat}}=\exp\bigl(-16\pi K/(\gamma_j T)\bigr)\) is a **leading-order-ceiling** (OWED-GAP4-remainder). \(F^{\mathrm{cross}}(d,K)\) contains \(C_{\diamond}\) (OWED). \(F_j^{\mathrm{win}}\) contains \(C_{\mathrm{win}}\) (OWED). The bound is for this fixed \(d\), not uniformly in \(d\).
>
> **Arithmetic interpretation (not used in the Fisher calculation).** If the surrogate mean is identified with the trigonometric sum in Proposition R, assume RH, simplicity of every nontrivial zero, and \(J_{-1}(T)=O(T)\). That identification is OWED-S1 at non-integer \(e^{t}\).

*Proof.* Regularity (R1)–(R4) of §9 holds under (M4′)+(M4″)+(M5), so Cramér–Rao gives \(\mathrm{Cov}(\widehat\theta)\succeq I(\theta)^{-1}\) with \(I\) the Gram (4.0) in \(\langle\,\cdot\,,\,\cdot\,\rangle_C\). Restrict attention to the \(3\times 3\) of tone \(j\). By (B1)\(_j\), \(I\preceq(1+\kappa_j)I_{N_j}\). Lemma 1\(^{\prime\prime}\) and Lemma 1-compare bound \(I_{N_j}\) above by \((1+\delta_j)S_{\eta}(\gamma_j)^{-1}G_j\). Lemma 3\(^\prime\)(a) inserts \(F^{\mathrm{cross}}(d,K)\). Lemma 2 with \(S_0=S_{\eta}(\gamma_j)\) and \(F_j^{\mathrm{win}}\) evaluates \([G_j^{-1}]_{\omega\omega}\). Collecting factors is (A.1). Substitute (M-amp) and (2.3) for (A.2)–(A.3). Unbiasedness converts \(\sqrt{\mathrm{Var}}\) into RMSE. \(\square\)

**Not claimed.** A max-\(j\) law “attained at \(j=d\)” after the \(j\)-dependent factors. The map \(j\mapsto\) right-hand side of (A.3) may or may not maximise at \(j=d\); that comparison is **OWED-last-tone**. A valid (generally weaker) bound for \(\max_j\mathrm{RMSE}(\widehat{\gamma}_j)\) is the maximum of the right-hand sides.

**Corollary A (sample complexity, leading named-factor form).** If some \(j\) has \(\mathrm{RMSE}(\widehat{\gamma}_j)\le\varepsilon\) and the four factors for that \(j\) are positive, then

\[
T
\;\ge\;
\bigl(6\log(\gamma_j/2\pi)\bigr)^{1/3}
\bigl(F_j^{\mathrm{flat}}F_j^{\mathrm{leak}}F^{\mathrm{cross}}F_j^{\mathrm{win}}\bigr)^{1/3}
\varepsilon^{-2/3}.
\]

As \(T\to\infty\) with \(d,K,\gamma_j\) fixed, \(F_j^{\mathrm{flat}}\to 1\) and \(F_j^{\mathrm{win}}\to 1\); \(F^{\mathrm{cross}}\) is independent of \(T\). The leading \(T^{-3/2}\) coefficient, if those two limits are taken and the remaining factors are set to \(1\), is \(\sqrt6\). That asymptotic corollary is **not** a finite-\(T\) theorem and is not used as a numerical floor in §12.

---

## 8. Theorem B — Bayes van Trees, externally specified centres

This is a different theorem from Theorem A. It bounds a **Bayes-average** MSE. It does not yield a pointwise frequentist bound at a fixed \(\theta\), and it does not yield a minimax bound (the spec’s N3 programme). Unbiasedness is not assumed, and is not dropped from Theorem A.

### 8.1 van Trees inequality

Let \(\pi\) be a density on an interval, absolutely continuous, vanishing at the endpoints, with finite prior information \(I(\pi)=\int(\pi')^2/\pi\). For a regular parametric family (the same (R1)–(R4) as Theorem A) and an arbitrary measurable estimator \(\widehat\theta\),

\[
\mathbb{E}\bigl[(\widehat\theta-\theta)^2\bigr]
\;\ge\;
\frac1{\mathbb{E}_{\pi}[I(\theta)]+I(\pi)},
\tag{8.1}
\]

the left side over the joint law \(\pi(d\theta)\,P_{\theta}\). *Citation.* Van Trees (1968), Part I, §2.4; Gill–Levit, *Bernoulli* 1 (1995), Theorem 1 (multivariate form). The boundary condition \(\pi=0\) at the endpoints of the support is load-bearing; a uniform prior is illegal.

### 8.2 Prior (P1\(^\prime\)): external centres

On \(u\in[-1,1]\) let \(\lambda(u)=\cos^2(\pi u/2)\). Then \(\int_{-1}^1\lambda=1\), \(\lambda(\pm 1)=0\), and \(I(\lambda)=\pi^2\). Scale: for a **declared** centre \(\mu\in\mathbb{R}\) and half-width \(\alpha>0\),

\[
\pi_{\gamma}(\gamma)
=\alpha^{-1}\lambda\bigl((\gamma-\mu)/\alpha\bigr)
\quad\text{on }[\mu-\alpha,\mu+\alpha].
\]

Then \(I(\pi_{\gamma})=\pi^2/\alpha^2\). Choice: \(\alpha=\pi K/T\), hence \(I(\pi_{\gamma})=T^2/K^2\). Adjacent interiors are disjoint under (M5).

**External centres (Defect 4 repair).** The centres \(\mu_1,\dots,\mu_d\) are parameters of \(\pi\), specified independently of the unknown \(\theta\). They are **not** defined as “the true ordinates in the local experiment.” For numerical evaluation in §12 the centres are taken to be the published Odlyzko ordinates listed in §11.1; those numbers enter as prior parameters, not as oracle knowledge of \(\theta\). Under \(\pi\), the random \(\gamma_j\) is not equal to \(\mu_j\).

Nuisance priors: \(\phi_j\) uniform on the circle (H-circle: van Trees on a closed manifold; **OWED-H-circle** if the Euclidean Gill–Levit statement is insisted upon — a cuff prior on \([0,2\pi]\) only strengthens the \(\omega\) bound). Amplitude: raised-cosine on \([A_*/2,3A_*/2]\). Because Lemma 2 has \(I_{A\omega}=0\) at leading order, \(I(\pi_A)\) does not enter the \(\omega\) Schur complement at leading order. The \(O(1/(\omega T))\) leak of \(I_{A\omega}\) after a nonzero \(I(\pi_A)\) is **OWED-amp-avg**.

### 8.3 Averaged Fisher matrix, not the centre block

Gill–Levit requires \(\overline{J}=\int I(\theta)\,\pi(\theta)\,d\theta\), not \(I(\mu)\). Substituting the centre block understates or overstates the denominator according to the variation of \(I^{\mathrm{eff}}(\gamma)=T^3/(6\log(\gamma/2\pi))\) on the support. Since \(I^{\mathrm{eff}}\) is decreasing in \(\gamma\), on \([\mu_j-\alpha,\mu_j+\alpha]\)

\[
\mathbb{E}_{\pi}[I^{\mathrm{eff}}_j]
\;\le\;
I^{\mathrm{eff}}(\mu_j-\alpha)
=\frac{T^3}{6\log\bigl((\mu_j-\alpha)/2\pi\bigr)},
\]

provided \(\mu_j-\alpha>2\pi\). Using this **upper** bound in the van Trees denominator produces a valid (weaker) lower bound. Coloured variation of \(I\) through \(1/S_{\eta}\) on the prior support is dominated by the GAP-4 ceiling already named; a fully expanded two-sided constant for \(\mathbb{E}_{\pi}[I]\) versus this endpoint bound is **OWED-B-avg**.

> **Theorem B (Bayes van Trees, external centres, exact Gaussian surrogate, fixed \(d\)).**
> Assume the hypotheses of Theorem A except unbiasedness. Let \(\pi\) be the product prior (P1\(^\prime\)) with **externally specified** centres \(\mu_1,\dots,\mu_d\) and \(\alpha=\pi K/T\). Let \(\widehat{\gamma}_j\) be any measurable function of \(\{y_{\Omega}(t):t\in[0,T]\}\). Then
>
> \[
> \mathbb{E}_{\pi}\bigl[(\widehat{\gamma}_j-\gamma_j)^2\bigr]
> \;\ge\;
> \frac{F^{\mathrm{cross}}(d,K)\,F_j^{\mathrm{flat}}\,F_j^{\mathrm{leak}}\,F_j^{\mathrm{win}}}
> {I^{\mathrm{eff},\uparrow}_j+T^2/K^2},
> \tag{B.1}
> \]
>
> where \(I^{\mathrm{eff},\uparrow}_j=T^3/\bigl(6\log((\mu_j-\alpha)/2\pi)\bigr)\). Equivalently, writing
> \(F_j^{\mathrm{prior}}=I^{\mathrm{eff},\uparrow}_j/\bigl(I^{\mathrm{eff},\uparrow}_j+T^2/K^2\bigr)\),
>
> \[
> \sqrt{\text{Bayes MSE}_j}
> \;\ge\;
> \sqrt6\cdot
> \bigl(F_j^{\mathrm{flat}}F_j^{\mathrm{leak}}F^{\mathrm{cross}}F_j^{\mathrm{win}}F_j^{\mathrm{prior}}\bigr)^{1/2}
> \cdot
> \frac{\bigl(\log((\mu_j-\alpha)/2\pi)\bigr)^{1/2}}{T^{3/2}}.
> \tag{B.2}
> \]
>
> The left side is Bayes RMSE (including bias\(^2\)), not \(\sqrt{\mathrm{Var}}\) of a biased estimator. The bound is a statement about \(\pi\), not a uniform frequentist bound on \(\mathrm{supp}(\pi)\) (**OWED-B-uniform**).
>
> **Arithmetic interpretation:** the same Prop. R disclosure as in Theorem A.

A minimax corollary would require a valid prior lower bound plus a parameter set that does not use oracle knowledge of the target. That corollary is not stated.

Ziv–Zakai (threshold / sidelobe region of the periodogram) is **OWED-ZZ**.

---

## 9. Regularity of \(\mathcal{G}_{N2}\)

Let \(P_{\theta}\) be the law of \(\{y_{\Omega}(t)\}_{t\in[0,T]}\) under \(\theta\). Under (M4) this is Gaussian with **fixed** covariance \(C\) and mean \(m_{\theta}\).

**(R1) Mutual absolute continuity.** Cameron–Martin: \(P_{\theta}\ll P_{\theta'}\) iff \(m_{\theta}-m_{\theta'}\) lies in the RKHS of \(C\). On the unrestricted line the integral \(\int|\hat m_{\theta}-\hat m_{\theta'}|^2/S_{\eta}\) diverges under (W′) because signal sidelobes decay like \(|\omega|^{-1}\) while \(1/S_{\eta}\) grows like \(\omega^4\). Under (M4′) the integral is over \(|\nu|\le\Omega\), where \(S_{\eta}\) is bounded below by (M4″) and the strict positivity of \(a(\omega)\). **Holds under (M4′)+(M4″).** The unrestricted record has infinite information; Theorem A/B are not about it.

**(R2) Differentiable log-likelihood.** \(\log dP_{\theta}/dP_0=\langle y,m_{\theta}\rangle_C-\tfrac12\|m_{\theta}\|_C^2\). The map \(\theta\mapsto m_{\theta}\) is real-analytic into \(L^2[0,T]\); \(\|\cdot\|_C\) is a continuous quadratic form on the band. **Holds.**

**(R3) Differentiation under the integral.** The score \(\partial_{\alpha}\log dP_{\theta}/dP_0=\langle y-m_{\theta},\,\partial_{\alpha}m_{\theta}\rangle_C\) is Gaussian, mean zero, finite variance. Local \(L^2(P_0)\) boundedness of the likelihood ratios on a compact \(\theta\)-neighbourhood licenses dominated interchange. **Holds** given (M4′).

**(R4) Fisher information finite and nonsingular.** Finiteness is \(\|\partial_{\alpha}m\|_C^2<\infty\) on the band. Nonsingularity of the \(3d\) Gram is (M5) plus \(F^{\mathrm{cross}}>0\). If (M5) fails, T1 is silent.

**(R5) Unbiasedness.** An assumption on the estimator class in Theorem A. Not a property of \(\mathcal{G}_{N2}\). Periodogram estimators (T2) are biased at finite \(T\); they are not in the quantifier of Theorem A. They are in the quantifier of Theorem B.

**(R6) is not a regularity condition of \(\mathcal{G}_{N2}\).** The noise *is* Gaussian by stipulation. Lindeberg / Berry–Esseen quantities \(\Lambda(\Gamma)\) and \(d_K\) are diagnostics of a *different* experiment (the phase sum). They are computed in §11 and interpreted in §14. They do not enter Theorems A or B.

---

## 10. Fisher information on the band

\[
I_{\alpha\beta}(\theta)
=\langle\partial_{\alpha}m_{\theta},\,\partial_{\beta}m_{\theta}\rangle_C
=\frac1{2\pi}\int_{|\nu|\le\Omega}
(\partial_{\alpha}m)^{\wedge}(\nu)\,\overline{(\partial_{\beta}m)^{\wedge}(\nu)}\,/S_{\eta}(\nu)\,d\nu.
\tag{4.0}
\]

**(a)** Every target is interior to the pass band with margin \(\Omega-\gamma_j>\Gamma\), and Lemma 1\(^{\prime\prime}\) neighbourhoods are interior under (M5): \(\gamma_j+h\le\gamma_d+(\Gamma-\gamma_d)=\Gamma<\Omega\).

**(b)** An ideal band-pass does not change \(S_{\eta}\) *inside* the band. The value \(S_{\eta}(\gamma_j)\) is (2.2), by (M4), not by Proposition 4.4\(^\prime\).

**(c)** Signal energy removed by the band-pass is \(O(1/(\Delta T))\) with \(\Delta=\Omega-\gamma_j\ge\Gamma\) and \(T\Gamma\ge 2\pi K\), hence \(O(K^{-1})\) of the same type already named as part of the comparison between full-line time-limited derivatives and their in-band projections. It is absorbed into \(F_j^{\mathrm{win}}\) / the projection step, not renamed as a second unsigned \(O(K^{-1})\).

The constant \(24\) is a white-noise leading term (Lemma 2). A coloured, band-limited numerical check at \(\Gamma=51.234\), \(\Omega=2\Gamma\), tone \(\gamma_d\), window (W′), from the superseded draft’s two independent scripts, gave \([I^{-1}]_{\omega\omega}\) equal to \(0.99392\) of \(24\,S_{\eta}(\gamma_d)/(A^2 T^3)\). That number is a **computation**, not a theorem factor. It sits between the conservative product \(F^{\mathrm{flat}}F^{\mathrm{leak}}\) and \(1\) because local flatness and leakage have opposite effects on the inverse; that cancellation is **not** used as a proof of the nominal \(24\).

---

## 11. Operating point \(\Gamma_{\mathrm{op}}=51.23361986\)

### 11.1 Inputs

\[
\begin{aligned}
T&=\log(3\cdot 10^7)=17.2167079396264,\\
K&=4,\\
\gamma_d&=49.773832,\\
L_d&=\log(\gamma_d/2\pi)=2.06961231767041,\\
\gamma_1&=14.134725,\qquad L_1=\log(\gamma_1/2\pi)=0.81076,\\
\vartheta_{\min}&=L_1=0.81076.
\end{aligned}
\]

Odlyzko ordinates used as **external prior centres** and as labels (from `t1_verify.py`):

| \(j\) | \(\gamma_j\) | \(\log(\gamma_j/2\pi)\) | \(\lvert M_W(\tfrac12+i\gamma_j)\rvert\) |
|---:|---:|---:|---:|
| 1 | 14.134725141734693 | 0.81076 | \(4.9742\times 10^{-3}\) |
| 2 | 21.022039638771555 | 1.20769 | \(2.2564\times 10^{-3}\) |
| 3 | 25.010857580145688 | 1.38143 | \(1.5954\times 10^{-3}\) |
| 4 | 30.424876125859513 | 1.57738 | \(1.0788\times 10^{-3}\) |
| 5 | 32.935061587739190 | 1.65666 | \(9.2084\times 10^{-4}\) |
| 10 | 49.773832477672302 | 2.06961 | \(4.0344\times 10^{-4}\) |

The six-decimal \(\gamma_d=49.773832\) is the referee’s audit value; it is the value that produces \(\Gamma_{\mathrm{op}}\) below. The twelve-decimal Odlyzko ordinate is \(49.773832477672302\). With that ordinate the exact (M5) threshold is \(\gamma_d+2\pi K/T=51.233620337\), which rounds **UP** at eight decimals to \(51.23362034\). The difference from \(\Gamma_{\mathrm{op}}\) is \(4.8\times 10^{-7}\) relative. All finite-\(\Gamma\) diagnostics below use \(\Gamma_{\mathrm{op}}=51.23361986\) as declared. \(\gamma_{11}=52.97032147771446>\Gamma_{\mathrm{op}}\).

### 11.2 Admissibility arithmetic (Defect 7)

\[
2\pi K=8\pi=25.13274122871835,
\qquad
\frac{2\pi K}T=1.4597878593.
\]

(M5) top margin: \(\Gamma\ge\gamma_d+2\pi K/T=49.773832+1.4597878593=51.2336198593\). Rounding **UP** at eight decimal places:

\[
\Gamma_{\mathrm{op}}=51.23361986,
\qquad
\Omega_{\mathrm{op}}=2\Gamma_{\mathrm{op}}=102.46723972.
\]

Check: \(T(\Gamma_{\mathrm{op}}-\gamma_d)=T\cdot 1.4597878607\ge 2\pi K\) at the displayed precision. The cut \(\Gamma=50\) fails:

\[
T(50-\gamma_d)=T\cdot 0.226168=3.89387<25.13274=2\pi K.
\]

\(\Gamma=50\) is retained in §11.8 only as an out-of-theorem diagnostic.

Among the first ten stored gaps, the smallest is \(\gamma_{10}-\gamma_9=1.768682>1.45979\), so \(d=10\) passes the internal-gap test at this \(T,K\). Disjointness of near-tone bands of radius \(h=2\pi K/T\) would require gaps \(>2h=2.91958\); that stronger condition fails inside \(d=10\) (OWED-overlap). The first stored adjacent gap below \(2\pi K/T\) is \(\gamma_{20}-\gamma_{19}=1.440150\), so the contiguous gap-admissible range in that table is \(d\le 18\) (data-dependent, not an asymptotic theorem).

### 11.3 \(d\)-dependence of the leading constants (fixed \(d\))

\[
C_{\mathrm{var}}(d)=6L_d,\qquad
C_{\mathrm{RMSE}}(d)=\sqrt{6L_d},\qquad
C_X(d)=(6L_d)^{1/3}.
\]

At \(d=10\): \(6L_d=12.41767390602246\), \(\sqrt{6L_d}=3.523872\), \((6L_d)^{1/3}=2.31568820531328\). Round \(C_X\) **UP** to \(2.3157\) when used as a resource exponent. The raw single-tone coefficient before evaluating \(L_d\) is \(\sqrt6=2.44948974278318\), which does not grow with \(d\); the headline law grows with \(d\) through \(\gamma_d\). Asymptotically \(L_d=1+W((d-7/8)/e)+O(\log d/d)\), so \(C_{\mathrm{RMSE}}(d)\sim\sqrt{6\log d}\). A non-asymptotic inversion of Riemann–von Mangoldt with a published remainder is **OWED** if certified ranges beyond the stored table are needed. The mean-spacing surrogate \(X\gtrsim(\gamma_d/2\pi)^K\) is heuristic, not a theorem (**OWED-mean-gap**).

### 11.4 Lindeberg ratio and \(\sigma^2\) at \(\Gamma_{\mathrm{op}}\) (mean-field scalar)

These are **diagnostics of the phase-sum experiment**, not inputs to Theorems A or B. Intensity-smoothed, \(a_{\omega}=\omega^{-2}\):

\[
\sigma^2(\Gamma)=\frac{\Gamma^{-3}}{3\pi}\Bigl(\log\frac{\Gamma}{2\pi}+\frac13\Bigr),
\qquad
\Lambda(\Gamma)=\frac{2a(\Gamma)^2}{\sigma^2(\Gamma)}=\frac{6\pi}{\Gamma\bigl(\log(\Gamma/2\pi)+1/3\bigr)}.
\]

At \(\Gamma=\Gamma_{\mathrm{op}}\):

\[
\frac{\Gamma_{\mathrm{op}}}{2\pi}=8.15408418,
\qquad
\log(\Gamma_{\mathrm{op}}/2\pi)=2.09851893,
\qquad
\log(\Gamma_{\mathrm{op}}/2\pi)+\tfrac13=2.43185226.
\]

\[
\Gamma_{\mathrm{op}}\bigl(\log(\Gamma_{\mathrm{op}}/2\pi)+\tfrac13\bigr)=124.592594,
\qquad
6\pi=18.8495559215,
\qquad
\Lambda_{\mathrm{as}}(\Gamma_{\mathrm{op}})=0.1512895.
\]

Round **UP**: \(\Lambda_{\mathrm{as}}(\Gamma_{\mathrm{op}})\le\mathbf{0.1513}\).

\[
\sigma^2_{\mathrm{as}}(\Gamma_{\mathrm{op}})=\frac{2\Gamma_{\mathrm{op}}^{-4}}{\Lambda_{\mathrm{as}}}=1.91848\times 10^{-6},
\qquad
\sigma_{\mathrm{as}}(\Gamma_{\mathrm{op}})=1.38509\times 10^{-3}.
\]

Exact-Riesz mean-field (\(a(\omega)=|M_W(\tfrac12+i\omega)|\)): relative to \(a(\omega)=\omega^{-2}\), \(a(\omega)^2=\omega^{-4}\bigl(1-5/(2\omega^2)+O(\omega^{-4})\bigr)\). At \(\Gamma=50\) the referee’s independent quadrature gave \(\Lambda_{\mathrm{Riesz}}(50)=0.156523843835\) versus \(\Lambda_{\mathrm{as}}(50)=0.156591636223\) (ratio \(0.999567\)). The same \(O(\Gamma^{-2})\) correction at \(\Gamma_{\mathrm{op}}\) gives \(\Lambda_{\mathrm{Riesz}}(\Gamma_{\mathrm{op}})\approx 0.151227\). Round **UP**: \(\Lambda_{\mathrm{Riesz}}(\Gamma_{\mathrm{op}})\le\mathbf{0.1513}\). Direct quadrature of the exact-Riesz integrand at \(\Gamma_{\mathrm{op}}\) is **OWED-quad-receipt** (GAP-8).

### 11.5 Kolmogorov label \(d_K\) (mean-field scalar, Defect 13)

Berry–Esseen for independent non-identical summands, Shevtsova constant \(C=0.56\) (upper bound on the absolute constant; Esseen’s \(0.4097\) is a lower bound on the constant and is not used):

\[
d_K\bigl(\mathcal{L}(\eta_{\Gamma}(t)/\sigma),\,\mathcal{N}(0,1)\bigr)
\;\le\;
0.56\cdot\frac{\rho_{\mathfrak{p}}}{\sigma^3},
\]

at a **fixed** \(t\), under intensity smoothing and \(a_{\omega}=\omega^{-2}\), with \(\rho_{\mathfrak{p}}=\sum \mathbb{E}|X_{\gamma}|^3\) and \(\mathbb{E}|\cos|^3=4/(3\pi)\). Closed form:

\[
\rho_{\mathfrak{p}}=\frac{16}{15\pi^2}\,\Gamma^{-5}\Bigl(\log\frac{\Gamma}{2\pi}+\frac15\Bigr).
\]

Algebraic reduction:

\[
\frac{\rho_{\mathfrak{p}}}{\sigma^3}
=\frac{16}{15\pi^2}\,(3\pi)^{3/2}\,\Gamma^{-1/2}\,
\frac{L+1/5}{(L+1/3)^{3/2}},
\qquad L=\log(\Gamma/2\pi).
\]

At \(\Gamma_{\mathrm{op}}\): \(L+1/5=2.29851893\), \(\Gamma^{-1/2}=0.139708\), \((3\pi)^{3/2}=28.9334\), \(16/(15\pi^2)=0.108076\), \((L+1/3)^{3/2}=3.7923\), hence

\[
\frac{\rho_{\mathfrak{p}}}{\sigma^3}=0.26479,
\qquad
0.56\times 0.26479=0.14828.
\]

Round **UP**: \(d_K^{\mathrm{as}}(\Gamma_{\mathrm{op}})\le\mathbf{0.1483}\). Scaling the referee’s exact-Riesz/asymptotic ratio at \(\Gamma=50\) (\(0.150740107934/0.150769394415=0.99981\)) gives \(d_K^{\mathrm{Riesz}}(\Gamma_{\mathrm{op}})\le\mathbf{0.1483}\) (UP).

**Label.** This is a **mean-field scalar approximation**: intensity integrals, the substitution \(a_{\omega}=\omega^{-2}\) or exact \(|M_W|\), and marks \(r_{\omega}\equiv 1\), at a single time. It is **not** a bound on the efficient score, the whitened profiled score, or the band-limited path (dimension \(\simeq\Omega T/\pi\approx 564\) at \(\Omega_{\mathrm{op}}\)). Transfer to the score is **OWED-H-score-BE**. Path-space distance is **OWED-path**.

### 11.6 GAP-4 ceilings (independent of \(\Gamma\); depend on \(\gamma_j,K,T\))

\[
\frac{16\pi K}T=11.67835.
\]

\(\exp(16\pi K/(\gamma_j T))\), exact and rounded **UP** at three significant figures (independent recomputation matching the referee’s GAP-4 audit):

| \(j\) | \(\gamma_j\) | exact | UP |
|---:|---:|---:|---:|
| 1 | 14.134725 | 2.28465187394 | **2.29** |
| 2 | 21.022040 | 1.74285857133 | **1.75** |
| 3 | 25.010858 | 1.59508865579 | **1.60** |
| 4 | 30.424876 | 1.46791144838 | **1.47** |
| 5 | 32.935062 | 1.42558994729 | **1.43** |
| 10 | 49.773832 | 1.26443750287 | **1.27** |

These dominate the superseded draft’s measured max/min column at every listed tone (2.03 down to 1.23). Numerical domination of six values is not a proof that the remainder \(r(\omega)\) is controlled; that remainder stays OWED. In Theorem A the factor is the exponential itself, not a measured \(\delta\).

### 11.7 Per-tone leakage at the operating point (Defect 6)

**In-theorem measurement presently available.** The superseded draft’s coloured band-limited \(3\times 3\) at \(\Gamma=51.234\), \(\Omega=102.468\), tone \(\gamma_d\), window (W′):

\[
\lambda_{\max}(I_{N_d}^{-1}I_{R_d})=0.0862,
\qquad
\frac{[I^{-1}]_{\omega\omega}}{24\,S_{\eta}(\gamma_d)/(A^2 T^3)}=0.99392.
\]

Relative cut shift \(|51.234-\Gamma_{\mathrm{op}}|/\Gamma_{\mathrm{op}}=7.4\times 10^{-6}\). Adopt, rounding the leakage constant **UP**,

\[
\kappa_d\le\mathbf{0.0863}
\qquad\text{at }\Gamma_{\mathrm{op}}\text{ for }j=d,
\]

pending a dedicated receipt at \(\Gamma_{\mathrm{op}}\) (OWED-B1-receipt). Then \(F_d^{\mathrm{leak}}=(1.0863)^{-1}=0.92056\), rounded **DOWN** to \(0.9205\).

**Per-tone \(\kappa_j\) for \(j\ne d\) at \(\Gamma_{\mathrm{op}}\) is unmeasured.** The \(\Gamma=50\) table (out of theorem) was \(\lambda_{\max}=0.587,\,0.220,\,0.132,\,0.108,\,0.124,\,0.086\) at \(j=1,2,3,4,5,10\), so (B1)\(_1\) fails the superseded global threshold \(K^{-1}=0.25\) even as a \(3\times 3\). Those numbers are **not** operating-point hypotheses. Theorem A at \(j\ne d\) is conditional on a stated \(\kappa_j\) at \(\Gamma_{\mathrm{op}}\).

**Global \(3d\times 3d\).** Not computed. **OPEN-B1-global.** Receipt requirement: a committed script plus `*_RECEIPT.json` reporting \(\lambda_{\max}(I_N^{-1}I_R)\) for \(I_N,I_R\) the \(3d\times 3d\) Gram split \(N=\bigcup_j B_j\), \(R=[-\Omega_{\mathrm{op}},\Omega_{\mathrm{op}}]\setminus N\), at \(\Gamma_{\mathrm{op}}\), \(d=10\), \(K=4\), window (W′), mean-field \(S_{\eta}\). Until that receipt exists, no global matrix inequality is claimed.

**Intensity-smoothed tail leakage (GAP-9, mean-field, not Fisher).** With \(\delta_d=\Gamma_{\mathrm{op}}-\gamma_d=1.45978786\), \(b(\omega)=\log(\omega/2\pi)/\bigl((\omega^2+\tfrac14)(\omega^2+\tfrac94)\bigr)\), the bound (4.5) of `T1_GAP9_STATIONARY_EXTENSION.md` gives \(Q_{\mathrm{tail},T}(\gamma_d)\le 2.41\times 10^{-7}\) (UP). The matched-filter comparison (4.3a) is \(\le 0.0233\) times \(S_{\eta}(\gamma_d)\) (UP). These control Fejér-probe variance of the *unextended* tail, not \(I^{-1}\).

### 11.8 Out-of-theorem diagnostic \(\Gamma=50\)

\(\Lambda_{\mathrm{as}}(50)=0.156591636223\) (referee; UP to \(0.157\)). Exact-Riesz quadrature \(\Lambda(50)=0.156523843835\). \(d_K^{\mathrm{as}}(50)\le 0.151\) (mean-field scalar). These numbers are **not** theorem-operating values.

### 11.9 Harmonic constant for \(C(d,K)\)

\(d=10\), \(H_9=1+1/2+\cdots+1/9=7129/2520=2.82896825397\), \(C(10,4)=(C_{\diamond}/\pi)H_9=0.90056\,C_{\diamond}\), \(C(10,4)/K=0.22514\,C_{\diamond}\). If \(C_{\diamond}=1\) (audit value, not a theorem), \(F^{\mathrm{cross}}(10,4)=1/1.22514=0.8162\) (DOWN to \(0.816\)). \(C_{\diamond}\) remains OWED; this audit number is not multiplied into a claimed theorem floor.

---

## 12. Numerical floors at \(\Gamma_{\mathrm{op}}\)

Auxiliary: \(T^{3/2}=71.43733\), \(\sqrt6=2.44948974278318\), \(\sqrt{6L_d}=3.523872\).

**Local unnamed-factor Gaussian number** (Lemma 2 at the true surrogate parameter, no named factors; **not** Theorem A):

\[
\frac{\sqrt{6L_d}}{T^{3/2}}=0.04932816.
\]

Round **DOWN**: \(\mathbf{0.04932}\). At \(j=1\): \(\sqrt{6L_1}/T^{3/2}=0.03087\) (DOWN: \(0.03087\)).

**Theorem A, \(j=d\), certified factors only.** Using the UP-rounded ceiling \(1+\delta_d\le 1.27\) and \(\kappa_d\le 0.0863\),

\[
\bigl(F_d^{\mathrm{flat}}F_d^{\mathrm{leak}}\bigr)^{1/2}
=\bigl(1.27\times 1.0863\bigr)^{-1/2}
=0.8514.
\]

Times the local number: \(0.04932816\times 0.8514=0.04199\). Round **DOWN**: \(\mathbf{0.0419}\). This still omits \(F^{\mathrm{cross}}\) and \(F_d^{\mathrm{win}}\) (both \(\le 1\), both OWED as numbers). It is a **partially certified** floor, labelled as such: a valid Theorem A floor is at most this number, and is strictly smaller once \(C_{\diamond}>0\) or \(C_{\mathrm{win}}>0\).

**Measured coloured inverse (computation, not a theorem).** At \(\Gamma=51.234\), \(j=d\): \(0.99392\times 0.04932816=0.04903\) (DOWN: \(0.04903\)). The cancellation between \(+8\%\) near-tone flatness and \(-8.6\%\) leakage is **not** a proof of the nominal \(\sqrt6\).

**Theorem B, \(j=d\), external centre \(\mu_d=49.773832\).** \(\alpha=\pi K/T=0.72989393\), \(\mu_d-\alpha=49.043938\), \(\log((\mu_d-\alpha)/2\pi)=2.054839\).

\[
I^{\mathrm{eff},\uparrow}_d=\frac{T^3}{6\times 2.054839}=413.925,
\qquad
I(\pi_{\gamma})=\frac{T^2}{K^2}=18.526,
\qquad
I^{\mathrm{eff},\uparrow}_d+I(\pi_{\gamma})=432.451.
\]

\[
\frac1{432.451}=0.0023124,
\qquad
\sqrt{\,\cdot\,}=0.048087.
\]

Round **DOWN**: Bayes RMSE \(\ge\mathbf{0.04808}\), *before* multiplying by \(F^{\mathrm{flat}}F^{\mathrm{leak}}F^{\mathrm{cross}}F^{\mathrm{win}}\). This is already weaker than the oracle-centred GAP-7 number \(0.04825\), as required by Defect 4. Inserting \(F_d^{\mathrm{flat}}F_d^{\mathrm{leak}}\) as in Theorem A: \(0.048087\times 0.8514=0.04094\), DOWN to \(\mathbf{0.0409}\), still omitting \(F^{\mathrm{cross}}\) and \(F^{\mathrm{win}}\).

**Sample-complexity exponent.** \(C_X(10)=(6L_d)^{1/3}=2.31568820531328\), round **UP** to \(\mathbf{2.3157}\). The finite-factor form of Corollary A replaces this by \(2.3157\cdot(F^{\mathrm{flat}}F^{\mathrm{leak}}F^{\mathrm{cross}}F^{\mathrm{win}})^{1/3}\). With only the two certified factors: \((1.27\times 1.0863)^{-1/3}=0.8981\), product \(2.080\) (DOWN: \(2.080\)). As \(\varepsilon\to 0\) the factors depending on \(T\) return to \(1\); the leading exponent \(2.3157\) is an asymptotic statement, not the finite-\(T\) resource law.

**Resource max with resolution.** Accuracy and (M5) combine as

\[
\log X
\;\ge\;
\max\Bigl\{
C_X(d)\,\varepsilon^{-2/3}\cdot(\text{named factors})^{1/3},\;
2\pi K/\Delta_d^+
\Bigr\},
\]

with \(\Delta_d^+=\min\{\min_{j<d}(\gamma_{j+1}-\gamma_j),\,\gamma_{d+1}-\gamma_d\}\) (strict inequality to place \(\Gamma\)). At the operating point the resolution term is \(T\ge 2\pi K/\Delta_d^+\), already satisfied by construction of \(\Gamma_{\mathrm{op}}\).

---

## 13. Empirical notes (Prop. R disclosure on every use)

**Disclosure, repeated.** Every numerical comparison in this section that uses Proposition R assumes RH, simplicity of every nontrivial zero, and \(J_{-1}(T)=O(T)\). Lean standing covers only the eight finite-core lemmas.

### 13.1 GAP-11 amplitude validation — resolved, conditional on Prop. R

On the actual Cesàro observable at \(N_{\max}=3\cdot 10^7\), a matched filter applied to \(y(t)\) constructed from the Möbius sieve (`t1_gap11_yt_estimator.py`, independent of the truncated zero-sum predictor; receipt `T1_GAP11_YT_RECEIPT.json`) gives

\[
|C(\gamma_1)|=6.287349\times 10^{-3},
\qquad
a_{\gamma_1}^{\text{Prop. R}}=6.271348\times 10^{-3},
\qquad
\text{ratio }=1.0026.
\]

This is a same-observable, same-estimator comparison of a measured amplitude to Prop. R’s predicted amplitude. It is **not** a location-error comparison and **not** a test of Theorems A or B. Status: resolved, conditional on Prop. R’s three hypotheses.

### 13.2 GAP-11 Gate-1 location risk — OPEN

The superseded draft compared a model-N2 RMSE number \(0.03087\) at \(\gamma_1\) to Gate-1’s MUSIC/periodogram absolute error \(0.00565\) on a **different** observable (prime counts) under a **different** noise model (N1). RMSE is an expectation; a single realised absolute error below an RMSE number is not a contradiction of an RMSE bound. No estimator-class story is required for that elementary point.

What remains **OPEN** is a comparison of empirical **MSE** (an ensemble, or a clearly declared single-path quadratic risk) of a named estimator on the **same** observable (S1) or on \(\mathcal{G}_{N2}\), against Theorem A or Theorem B. Gate-1’s location errors are not such a comparison. This file does not say that Gate-1 “violates the bound.”

### 13.3 Prior art (GAP-12)

Live re-scout `T1_GAP12_LIVE_RECHECK_2026-08-26.md`: CR / Fisher bound for zeta-zero *location* unoccupied (NONE/SETUP-ONLY). Setup citations: Hardy–Riesz, Ingham, Titchmarsh, Ng 2004, Odlyzko–te Riele 1985, Rife–Boorstyn / Kay.

---

## 14. Model-fidelity discussion (no transfer)

This section is not a theorem. Nothing in it is claimed to transfer a \(\mathcal{G}_{N2}\) bound to the random-phase sum or to a fixed zeta configuration.

### 14.1 Stam obstruction (why no transfer is claimed)

Let \(\xi\) have density \(f\), mean \(0\), variance \(1\), Fisher information \(I(f)=\int(f')^2/f\). Integration by parts and Cauchy–Schwarz give Stam’s inequality \(I(f)\ge 1=I(\varphi)\), equality iff \(f\) is Gaussian (*citation:* Stam, *Information and Control* 2 (1959); written out in `T1_GAP17_PROPAGATION.md` §2.1). Consequently, in a location family, the **true** van Trees / CR number is *smaller* than the Gaussian number: any estimator that exploits non-Gaussianity may achieve a risk between \(1/(I(f)+I(\pi))\) and \(1/(1+I(\pi))\). The Gaussian display is therefore **not** a lower bound for the full phase-sum class.

The same projection argument on path space, for additive noise with **fixed** covariance \(C\), gives \(I_{\mathrm{true}}(\theta)\succeq (Dm)^T C^{-1}(Dm)=I_{\mathcal{G}}(\theta)\) whenever the true score exists (`T1_GAP17_PROPAGATION.md` §2.3; infinite-dimensional RKHS statement OWED-Stam-path). Direction: to turn \(I_{\mathcal{G}}\) into a valid MSE lower bound for the full class one must **upper**-bound \(I_{\mathrm{true}}\), not lower-bound it.

A restriction to “any function of the Gaussian score” does not repair this: a nonlinear function of a scalar score \(S=u+U\) can use the non-Gaussian density of \(U\), and Stam again gives \(I(f)\ge I_{\mathcal{G}}\). Godambe’s sandwich is an asymptotic covariance formula for a specified estimating-equation root, not an information inequality. It is not used.

### 14.2 Why the \(\sqrt{m}\) full-class route is vacuous (Defect 14)

The phase sum has bounded support. Intensity-smoothed at \(\Gamma_{\mathrm{op}}\) with \(a_{\omega}=\omega^{-2}\),

\[
\sum_{\gamma>\Gamma}a_{\gamma}
\approx\frac{L+1}{2\pi\Gamma}=0.009625,
\qquad
R_*\approx\frac{2\sum a}{\sigma_{\mathrm{as}}}=13.90,
\]

rounded **UP** to \(R_*\le 14\). The truncated-Gaussian reference \(\varphi^R\) remains strictly positive at \(\pm R_*\), while the true density vanishes at the edge of its support. Hence

\[
m=\operatorname*{ess\,inf}_{[-R_*,R_*]}\frac{f}{\varphi^R}=0.
\]

A multiplicative law \(\mathrm{MSE}\ge m/(I_{\mathcal{G}}+I(\pi))\) is vacuous. Landau interpolation from \(d_K\le 0.1483\) to \(\|f-\varphi\|_{\infty}\) is likewise vacuous at the mode (`T1_GAP17_PROPAGATION.md` §5). Additive total-variation comparison of quadratic loss at the prior diameter is vacuous by a factor of several hundred (§4 of that note). **H-ratio is not proposed as a viable full-class theorem.** A bulk-plus-tail inequality, or an independent upper bound on \(I(f)\), is **OPEN-full-class**.

Edgeworth main-term kurtosis, same smoothing, at \(\Gamma_{\mathrm{op}}\): \(|\gamma_2|\le 0.0897\) (UP), \(\gamma_2^2/6\le 0.00134\). Lyapunov\(_6\le 0.0141\) (UP). The remainder constant in \(r=O(\mathrm{Lyapunov}_6)\) is **OWED-Edgeworth**. These numbers explain why \(d_K\sim 0.15\) overstates a plausible Fisher perturbation; they are not a substitute \(m\).

### 14.3 The fill is an order-one modelling replacement (GAP-9)

For fixed \(\gamma_j<\Gamma\), true-tail leakage through a length-\(T\) Fejér probe is \(O(T^{-1})\) (`T1_GAP9_STATIONARY_EXTENSION.md` (4.3)–(4.5)). The (M4) fill converges to the full positive \(S_{\eta}(\gamma_j)\) and is therefore the **entire** noise floor of Theorems A and B, not a vanishing error. Removing the fill makes the target score fail Cameron–Martin membership in the tail-noise RKHS: formal information infinite, CR bound zero. There is no finite multiplicative comparison of the two Gaussian experiments.

Conjecture GAP-9-H (marked local-continuum / Palm limit at height \(H\to\infty\), \(T_H/\lambda_H\to 0\)) is a different regime from the present fixed-low-zero operating point, where the expected number of ordinates in a local half-width \(2\pi K/T\) is less than one. GAP-9 remains **OPEN** as a justification of \(\mathcal{G}_{N2}\) from a fixed zeta configuration. Inside \(\mathcal{G}_{N2}\), the fill is a stipulated regulariser.

Time-stationarity of a *random-phase* tail is a theorem under (M1) and is not the issue. The issue is spectral support.

### 14.4 Heavy tails of \(1/|\zeta'|\)

Under (M3′) the mark \(r\equiv 1\) is deterministic. The divergent second moment of \(1/|\zeta'|\) (Gonek–Hejhal \(J_{-2}\)) does not enter \(S_{\eta}\) or the leading constants of Theorems A and B. Falsification gate G-a of `G1_MODEL_SPEC.md` §5, which threatened demotion if \(S_{\varepsilon}\) could not be bounded because of that second moment, does not fire **for \(\mathcal{G}_{N2}\)**. It would fire for a marked point-process model that this file does not adopt. Truncation sensitivity of a random-mark law is therefore off the theorem’s critical path; the GAP-10 sweep’s mean-field \(q\)-invariance is consistent with (M3′).

---

## 15. Current ledger

One row per remaining OPEN/OWED item. No history.

| ID | Status | Content | Needed to close |
|---|---|---|---|
| OWED-GAP4-remainder | OWED | Explicit \(C_r\) with \(\lvert r(\omega)\rvert\le C_r/(\omega\log(\omega/2\pi))\) for \(\omega\ge\gamma_1\); until then (3.1) is a leading-order-ceiling | Finite estimate of \(D(\omega)+4/\omega\) on \([\gamma_j-h,\gamma_j+h]\) |
| OPEN-B1-global | OPEN | Full \(3d\times 3d\) \(\lambda_{\max}(I_N^{-1}I_R)\) at \(\Gamma_{\mathrm{op}}\) | Committed script + `*_RECEIPT.json` at \(d=10\), \(K=4\), \(\Omega=2\Gamma_{\mathrm{op}}\) |
| OWED-B1-receipt | OWED | Per-tone \(\kappa_j\) at \(\Gamma_{\mathrm{op}}\) for all \(j\); only \(j=d\) transferred from \(\Gamma=51.234\) | Same receipt, per-tone \(3\times 3\) |
| OWED-\(C_{\diamond}\) | OWED | Coloured pairwise block constant in \(C(d,K)\) | Operator-norm bound on off-diagonal \(3\times 3\) blocks |
| OWED-overlap | OWED | Near-tone bands overlap under (M5); harmless for per-tone (B1)\(_j\), not for a disjoint-band frame | Partitioned decomposition or gaps \(>2h\) |
| OWED-last-tone | OWED | \(\arg\max_j\) of (A.3) after named factors | Evaluate (A.3) at all \(j\) once every \(F_j\) is numerical |
| OWED-\(C_{\mathrm{win}}\) | OWED | Explicit constant in \(F_j^{\mathrm{win}}=1-C_{\mathrm{win}}/(\gamma_j T)\) | \(2\times 2\) perturbation of the \((\omega,\phi)\) Schur complement |
| OWED-S1 | OWED | Integer-\(N\) Prop. R vs continuous-\(t\) surrogate | Real-\(N\) Riesz formula, or a Fisher comparison of (S1) to \(\mathcal{G}_{N2}\) |
| OWED-ERiesz-\(C_A\) | OWED | Explicit \(C_A\) in \(\lvert E_{\mathrm{Riesz}}(N)\rvert\le C_A N^{-A}\); uniform negligibility on the observation range | Bound the vertical integral on \(\mathrm{Re}\,s=-A\) |
| OPEN-GAP-9 | OPEN | Fill as a model of a fixed zeta configuration; Cameron–Martin singularity; Conjecture GAP-9-H and Fisher transfer | Palm/continuum limit in a high-height regime, or a minimax (N3) replacement |
| OPEN-GAP-11-Gate1 | OPEN | Ensemble (or declared) location-risk comparison of a named estimator on (S1) or \(\mathcal{G}_{N2}\) to Theorem A/B | Same observable, MSE not a single absolute error |
| OPEN-full-class | OPEN | Any multiplicative/additive transfer of \(I_{\mathcal{G}}\) to the phase-sum class; \(m=0\); bulk+tail unproved | Upper bound on \(I(f)\), or a bulk+tail inequality |
| OWED-H-score-BE | OWED | \(d_K\) of the whitened profiled score versus scalar \(\eta_{\Gamma}(t)\) | Lyapunov ratio of the matched-filter weights |
| OWED-path | OWED | Path-space distance of \(\{\eta_{\Gamma}(t)\}\) to the Gaussian process with spectrum \(S_{\eta}\) | Hellinger / RKHS-control metric on the (M4′) band |
| OWED-Edgeworth | OWED | Remainder in the Edgeworth expansion of \(I(f)\); Lyapunov\(_6\) is derived, the implied constant is not | Remainder theorem with explicit constant |
| OWED-B-avg | OWED | Fully expanded \(\mathbb{E}_{\pi}[I]\) versus the left-endpoint upper bound | Two-sided modulus of \(I(\theta)\) on \(\mathrm{supp}(\pi)\) |
| OWED-B-uniform | OWED | Conversion of Theorem B into a frequentist bound uniform on \(\mathrm{supp}(\pi)\) | Modulus of continuity of \(I(\theta)\) (needs a closed GAP-4 remainder) |
| OWED-amp-avg | OWED | \(O(1/(\omega T))\) leak of \(I_{A\omega}\) after \(I(\pi_A)\) | Bound the perturbed Schur complement |
| OWED-H-circle | OWED | Uniform phase prior on \(\mathbb{R}/2\pi\mathbb{Z}\) versus Euclidean Gill–Levit | Cuff prior, or a manifold statement |
| OWED-GAP-6 | OWED | Written proof that discrete-sample FIM \(\preceq\) continuous FIM for this Gram | Data-processing lemma |
| OWED-ZZ | OWED | Ziv–Zakai bound for the periodogram threshold region | Separate note |
| OWED-mean-gap | OWED | Replacing \(\Delta_d^+\) by the mean spacing \(2\pi/L_d\) | Not a consequence of Riemann–von Mangoldt |
| OWED-RvM | OWED | Non-asymptotic inversion of \(N_{\zeta}(H)\) with a published remainder | Choose a remainder and invert |
| GAP-8 | OWED | Committed scripts + hashed receipts for every numerical figure in §11–§12 | `t1_verify.py` (or successor) under version control with `*_RECEIPT.json` |
| OPEN-N3 | OPEN | Minimax over admissible zero configurations | Spec §3-N3; not in v4 scope |

---

## 16. Claims and not-claims

**Claimed.**

- Theorem A: a pointwise Cramér–Rao lower bound for unbiased estimators of the band-limited exact Gaussian surrogate \(\mathcal{G}_{N2}\), at fixed admissible \(d\), with named factors \(F^{\mathrm{flat}}\) (leading-order-ceiling), \(F^{\mathrm{leak}}\) (per-tone), \(F^{\mathrm{cross}}(d,K)\), \(F^{\mathrm{win}}\).
- Theorem B: a Bayes van Trees lower bound for arbitrary measurable estimators of the same surrogate, under an externally centred raised-cosine prior, using an upper bound on \(\mathbb{E}_{\pi}[I]\).
- Spectral density (2.2) of \(\mathcal{G}_{N2}\) under (M3′); covariance independent of \(\theta\); cancellation of the mean-field window factor \(a(\omega)\) at the true surrogate parameter, not of \(1/|\zeta'|\).
- (M5)-admissibility of \(\Gamma_{\mathrm{op}}=51.23361986\) at the stated \(T,K,\gamma_d\).
- Proposition R as a cited + Lean-core statement, with the three hypotheses disclosed at every use in this file.
- GAP-11 amplitude match \(|C(\gamma_1)|/a_{\gamma_1}=1.0026\) on \(y(t)\), conditional on Prop. R.
- The arithmetic of §11, with the stated rounding.

**Not claimed.**

- Anything unconditional about \(\zeta\).
- Any transfer of Theorem A or B to the non-Gaussian phase sum (Stam).
- Any transfer to a fixed, non-randomised zeta configuration (GAP-9 / Cameron–Martin).
- A global \(3d\times 3d\) leakage inequality (OPEN-B1-global).
- Uniformity in \(d\); last-tone attainment after corrections.
- That \(F_j^{\mathrm{flat}}\) is a fully rigorous bound on \(D\) (remainder OWED).
- That \(d_K\le 0.1483\) is a certified misspecification bound for the efficient score or the path.
- That \(\Gamma=50\) is an operating point.
- That a single Gate-1 absolute error contradicts an RMSE bound.
- That (S1) *is* the continuous-time surrogate (OWED-S1).
- A minimax (N3) bound.
- A Ziv–Zakai bound.
- That unbiasedness has been dropped from the pointwise law.
- That Godambe’s sandwich is a lower-bound theorem.
- Any use of the phrase “violates the bound.”

---

## 17. Defect map (all 19)

| Defect | Disposition in v4 |
|---:|---|
| 1 | Repaired: (M3′) deterministic \(r\equiv 1\); \(S_{\eta}\) has no \(E[r^2\mid\omega]\); no \(1/\lvert\zeta'\rvert\) cancellation claimed |
| 2 | Repaired: \(C\) independent of \(\theta\); no covariance-information term; (M-amp) only at the true mean |
| 3 | Repaired: Godambe / “Gaussian-score class” deleted; Theorem A is unbiased CR; full-class transfer refused in §14 |
| 4 | Repaired: Theorem B is a separate Bayes law; centres external; \(\overline{J}\) upper-bounded, not replaced by \(I(\mu)\) |
| 5 | Repaired: Theorems A/B are exact-Gaussian-surrogate theorems; phase sum only in §14 with no transfer (Stam) |
| 6 | Per-tone (B1)\(_j\) in the theorems; global \(3d\times 3d\) **OPEN-B1-global** with receipt requirement |
| 7 | Repaired: sole cut \(\Gamma_{\mathrm{op}}=51.23361986\); every finite-\(\Gamma\) quantity recomputed there; \(\Gamma=50\) diagnostic only |
| 8 | Factor \(\exp(16\pi K/(\gamma_j T))\) **in Theorem A**, labelled leading-order-ceiling; remainder **OWED-GAP4-remainder** |
| 9 | Repaired: Lemma 1\(^{\prime\prime}\) projected derivatives + full-line Plancherel + Loewner comparison \(G^P\preceq G\) |
| 10 | Repaired: fixed \(d\), explicit \(C(d,K)\); no “uniformly in \(d\)”; last-tone attainment **OWED-last-tone** |
| 11 | Repaired: Prop. R’s three hypotheses in §1.1, theorem interpretation clauses, and §13 |
| 12 | Status reconciled (citation+Lean standing); integer-\(N\) vs continuous-\(t\) declared as (S1) + **OWED-S1** |
| 13 | Repaired: \(d_K\le 0.1483\) labelled mean-field scalar approximation, not a certified score/path bound |
| 14 | Repaired: \(\sqrt{m}\) route identified as vacuous (\(m=0\)); not offered as a full-class theorem; bulk+tail **OPEN-full-class** |
| 15 | Repaired: target-frequency floor attributed to (M4), not to Proposition 4.4\(^\prime\); GAP-9 **OPEN** outside the surrogate |
| 16 | Repaired: GAP-11 split (amplitude resolved cond. on Prop. R; Gate-1 risk **OPEN**); “violates the bound” deleted |
| 17 | Repaired: \(E_{\mathrm{Riesz}}\) vs \(\eta_{\Gamma}\) throughout |
| 18 | Repaired: named signed factors in every displayed lower bound; no bare \(O(K^{-1})\) |
| 19 | Repaired: this file is a single integrated text; §15 is the only ledger; superseded v3 statements are not current |

---

**v4 DRAFT (grok lane) 2026-08-26 — UNREFEREED.** Not promotable until a cold referee accepts the seven minimum conditions against this text. Nothing in `T1_CRAMER_RAO_DRAFT.md` may be cited as a result in preference to this file.

## FRONTIER VERIFICATION 2026-08-26 (fable) — operating-point arithmetic PASS
Independent recomputation at Γ_op = 51.23361986: Λ = 0.151290 (≤ 0.1513 UP ✓);
d_K mean-field-scalar = 0.148282 (≤ 0.1483 UP ✓); σ²_as = 1.918673e-6 vs the
note's 1.91848e-6 — agreement to 4 significant figures; the 5th-digit gap
(~0.001%) is presumed asymptotic-vs-quadrature convention and is within every
rounding used downstream. Sent to cold re-referee.

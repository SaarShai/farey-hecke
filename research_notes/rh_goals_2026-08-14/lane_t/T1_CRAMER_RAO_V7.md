# T1 — Cramér–Rao and van Trees in the exact Gaussian surrogate

**v7 DRAFT (grok lane) 2026-08-26 — UNREFEREED**

This file supersedes `T1_CRAMER_RAO_V6.md`. It is a copy of v6 with **only** the four remaining defects named by the governing report `T1_V6_REFEREE_2026-08-26.md`. Absolute rules: (i) for each faulted affirmative claim, either supply exactly the missing step the referee names or demote the claim to an explicit OWED ledger row — no third option; (ii) never vacate an OWED row without a displayed proof in this document; (iii) claims may only get weaker. Everything the v6 referee ruled REPAIRED/passing is kept. Supporting derivations cited by filename are not imported as current theorems. No statement from v3, v4, v5, or v6 is current except as restated here.

Rounding convention (binding): error bounds and ceilings round **UP**; lower-bound floors, RMSE margins, and sample-complexity coefficients that multiply a lower bound on \(T\) round **DOWN**.

v6→v7 map (the four remaining defects): **V6-R4-B1** the upper half of (A\(\infty\).1) is the Loewner inversion of the passing sandwich (A\(\infty\).0) on the free-amplitude \(3\times 3\), evaluated at the \((\omega,\omega)\) entry — not the \(2\times 2\) bound (5.5); closed-form promotion of that entry through (5.5) is **OWED-Ainfinity-validity**. **V6-R4-B2/M4** Theorem B uses the (M5)-admissible half-widths \(\rho_j\) with \(I(\pi_j)=\pi^2/\rho_j^2\), and is stated for \(j\in\{2,\dots,d\}\) only. **V6-R4-m1** \(\varepsilon_a^{\mathrm{Riem}}\) is recomputed from Lemma 6. **V6-R4-M1/M2/M3** Lemma 2 displays the Abel step \(2(n-1)^2\) and a consistent normalised Gram; Lemma 4 is piecewise at the spectral floor.

---

## Model Declaration (binding)

The following choices are the model.

**(a) Defects 1, 2, 5 — exact Gaussian surrogate, mean-field marks, fixed covariance (v4 repair, kept).**
Theorems A and B are theorems about a stipulated Gaussian experiment \(\mathcal{G}_{N2}^{n}\), defined in §2. Clause **(M3′)** is part of that experiment: marks are the deterministic interpolant \(r(\omega)\equiv 1\). The covariance \(\Sigma=\Sigma_{\eta}+\sigma_s^2 I_n\) does **not** depend on \(\theta\). There is no Gaussian covariance-information term. The actual non-Gaussian phase sum is confined to §14 and carries **no transfer claim**, by Stam (`T1_GAP17_PROPAGATION.md` §2).

**(b) N1 — discrete sampling, not a continuous band-limited record.**
The observation is \(n\) samples of the trigonometric mean plus **two** stipulated noises: the sampled tail Gaussian \(\eta\) *and* i.i.d. sampling noise \(\varepsilon_k\sim N(0,\sigma_s^2)\). Mean shifts lie in \(\mathbb{R}^n\), which is the Cameron–Martin space of the nondegenerate law \(N(0,\Sigma)\). The exact Fisher is the finite-dimensional Gram (4.0n). The continuous band-limited formula (v4 (4.0)) is **not** the Fisher of this experiment. The \(T^3\) scaling is **Proposition A\(\infty\)**: a comparison envelope of (4.0n) with a closed-form sampling-noise lower bound and a Loewner upper bound against the discrete Gram inverse. It is not Theorem A and not a limiting equality.

**(c) Defects 3, 4, N2 — two theorems, one quantifier each; Godambe dropped; prior compatible with (M-amp) and (M5).**
- **Theorem A:** pointwise frequentist Cramér–Rao for unbiased estimators of \(\theta\) in \(\mathcal{G}_{N2}^{n}\). Quantifier: every unbiased estimator of the \(n\)-sample Gaussian vector.
- **Theorem B:** Bayes van Trees risk under a prior on the ordinates \(\gamma_j\) only, with \(A_j:=2a(\gamma_j)\) a deterministic function of the drawn \(\gamma_j\) (so (M-amp) holds \(\pi\)-almost surely), with the tied-submodel Fisher \(I_{\mathrm{tied},j}\), **conditional on (H-circle)**, with prior support inside the (M5)-admissible set of half-widths \(\rho_j\) declared in (P1″), and **only for target indices \(j\in\{2,\dots,d\}\)**. Centres \(\mu_j\) are externally specified. Unbiasedness is not assumed. The index \(j=1\) is excluded (v6 referee §II.3 / V6-R4-M4): the \(j=1\) prior mass below the spectral-floor anchor is not repaired.
- The phrases “Gaussian-score class” and “Godambe sandwich as a lower bound” are not used.

**(d) Defect 7, N3 — sole operating point, full stored ordinate.**
\[
\Gamma_{\mathrm{op}}:=51.23362034,
\]
which is the eight-decimal **UP** rounding of the (M5) threshold at the **full** stored tenth ordinate \(\gamma_{10}=49.773832477672302\). Every finite-\(\Gamma\) quantity is evaluated at \(\Gamma_{\mathrm{op}}\) unless labelled out-of-theorem. \(\Gamma=50\) is not an operating point. The truncated six-decimal \(\gamma_d=49.773832\) is not used to pass (M5).

**(e) Defect 6, N5 — Schur reduction to the per-tone \(3\times 3\); global matrix OPEN.**
Theorem A estimates the full \(3d\)-parameter vector. The step from \(I\in\mathbb{R}^{3d\times 3d}\) to the principal \(3\times 3\) of tone \(j\) is the nuisance Schur-complement inequality of Lemma 3′(a): \([I^{-1}]_{\gamma_j\gamma_j}\ge[I_{jj}^{-1}]_{\gamma_j\gamma_j}\). Hypothesis (B1)\(_j\) is optional and is **not** inserted into Theorem A. The global \(3d\times 3d\) Loewner comparison remains **OPEN-B1-global**. The factor \(F^{\mathrm{cross}}\) is **not** a theorem factor.

**(f) Defects 8, 9, 18, N4, N6 — exact flatness, Loewner Lemma 1″, no fake floor.**
Lemma 1″ is a **Loewner-order** Gram inequality. GAP-4 is closed by an elementary bound on the exact logarithmic derivative \(D(\omega)\), piecewise: log-branch (3.0) on \(\{\omega>\gamma_1^{\mathrm{anchor}}\}\), floor-branch \(D=-R\) on \(\{\omega\le\gamma_1^{\mathrm{anchor}}\}\), each by endpoint evaluation (no remainder \(r(\omega)\), no “modulo OWED” in any theorem factor). \(C_{\mathrm{win}}\) is certified in Lemma 2 by a displayed Abel bound. Theorem A displays **no numerical floor**. Certified multiplicative factors and missing ones are labelled separately in §12.

**(g) Defect 10 — fixed \(d\), last-tone attainment OWED.**
Theorems A and B are for a **fixed** admissible \(d\). The bound is not asserted uniformly in \(d\). That the maximum over \(j\) of a corrected right-hand side is attained at \(j=d\) is **OWED-last-tone**. Theorem B’s quantifier is further restricted to \(j\in\{2,\dots,d\}\).

**(h) Defects 11, 12 — Prop. R disclosure; (S1) distinct from \(\mathcal{G}_{N2}^{n}\).**
The full Prop. R list (RH; simplicity of every nontrivial zero; conjectural Gonek–Hejhal \(J_{-1}(T)=O(T)\)) is stated in §1.1, in the interpretation clauses of Theorems A and B, and at every empirical use. The arithmetic experiment (S1) is not \(\mathcal{G}_{N2}^{n}\). Identification is **OWED-S1**.

**(i) Defect 16 — GAP-11 split; no “violates the bound”.**
As in v4: amplitude validation on \(y(t)\) is resolved conditional on Prop. R; Gate-1 location-risk comparison is **OPEN**. A single realised absolute error is not a violation of an RMSE bound.

**(j) Defect 17 — two epsilons.**
\(E_{\mathrm{Riesz}}\) is the Prop. R remainder. \(\eta_{\Gamma}\) is tail interference. The symbol \(\varepsilon\) is not used for either. Sampling noise is \(\sigma_s^2\), never called \(\varepsilon\) as a process.

---

## 0. What the theorems say

In the discrete Gaussian experiment \(\mathcal{G}_{N2}^{n}\) of §2, with deterministic marks \(r\equiv 1\) and \(\theta\)-independent covariance \(\Sigma=\Sigma_{\eta}+\sigma_s^2 I_n\succ 0\), an unbiased estimator of the \(n\)-sample vector satisfies Theorem A: for each target index \(j\) at a **fixed** admissible \(d\),

\[
\mathrm{Var}(\widehat{\gamma}_j)
\;\ge\;
\bigl[I(\theta)^{-1}\bigr]_{\gamma_j\gamma_j}
\;\ge\;
\bigl[I_{jj}(\theta)^{-1}\bigr]_{\gamma_j\gamma_j}
\;\ge\;
F_j^{\mathrm{win}}
\cdot
\frac{24\,\sigma_s^2}{A_j^2 n T^2},
\]

where \(I(\theta)\) is the exact \(3d\times 3d\) Fisher (4.0n), \(I_{jj}\) is its principal \(3\times 3\) at tone \(j\), the second inequality is the Schur step (Lemma 3′(a)), and the third is the sampling-noise envelope with certified \(F_j^{\mathrm{win}}=1-C_{\mathrm{win}}/(\gamma_j T)\) and \(C_{\mathrm{win}}=84\) (Lemma 2). This is a pointwise frequentist bound in \(\mathcal{G}_{N2}^{n}\). It is not a bound on the zeta phase-sum experiment, and it is not the \(T^{-3}\) law.

The \(T^{-3}\) scaling is **Proposition A\(\infty\)**: a comparison envelope of the exact finite-\(n\) Fisher (4.0n). The lower side is the closed-form sampling-noise bound of Lemma 2. The upper side is Loewner inversion of (A\(\infty\).0) on the free-amplitude \(3\times 3\), taking the \((\gamma_j,\gamma_j)\) entry. It is not Theorem A, and it is not a limiting equality. A closed-form Abel upper bound converting the discrete-Gram inverse into the \(2\times 2\) factor \(F^{\mathrm{win},\uparrow}\) of (5.5) is **OWED-Ainfinity-validity**.

Theorem B bounds the Bayes **MSE** of an arbitrary measurable estimator under an externally centred raised-cosine prior on the ordinates \(j\in\{2,\dots,d\}\) only, with admissible half-widths \(\rho_j\), with \(A_j=2a(\gamma_j)\), the tied-submodel Fisher \(I_{\mathrm{tied},j}\), and **hypothesis (H-circle)**. The expectation in (B.0) is the joint \((\pi_{\gamma}\otimes\pi_{\phi})\) expectation. It does not discharge unbiasedness in Theorem A. It does not apply to \(j=1\).

At the unique operating point \(\Gamma_{\mathrm{op}}=51.23362034\), \(T=\log(3\cdot 10^7)\), \(K=4\), \(d=10\), the **comparison skeleton** (locally-white unnamed-factor coefficient at \(S_s=0\); not a proved A\(\infty\) limit) is \(\mathrm{RMSE}\ge 0.04932\) (rounded down). This number is **not** a Theorem A floor. Section 12 lists certified factors and missing factors separately and displays **no** numerical product floor for Theorem A.

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

### 1.2 Integer \(N\) versus the discrete Gaussian experiment (S1)

Proposition R is a statement about **integer** \(N\). Theorems A and B below are statements about the **discrete-time** Gaussian vector of §2. These are different experiments.

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

Theorems A and B are **not** theorems about \((Y_N)\). They are theorems about \(\mathcal{G}_{N2}^{n}\). A Fisher comparison of (S1) to \(\mathcal{G}_{N2}^{n}\) is **OWED-S1**. Until OWED-S1 is closed, no numerical comparison of a Theorem A/B number to an estimator computed from \((Y_N)\) is a comparison of the same experiment.

### 1.3 Notation: \(E_{\mathrm{Riesz}}\) and \(\eta_{\Gamma}\)

- \(E_{\mathrm{Riesz}}(N)\) is the remainder in Proposition R. For a continuous label write \(E_{\mathrm{Riesz}}(t):=E_{\mathrm{Riesz}}(e^{t})\) only at \(t=\log N\in\log\mathbb{Z}_{\ge 2}\).
- \(\eta_{\Gamma}\) is interference from ordinates \(\gamma>\Gamma\). In \(\mathcal{G}_{N2}^{n}\) it is the centred Gaussian vector obtained by sampling the stationary process with spectral density \(S_{\eta}\) of §2.4. In §14 it is the random-phase sum \(2\sum_{\gamma>\Gamma}a_{\gamma}\cos(\gamma t+\phi_{\gamma})\). These are different objects sharing a symbol by analogy of role.

On the arithmetic side, after the \(N^{-1/2}\) normalisation, \(N^{-1/2}E_{\mathrm{Riesz}}(N)=O_A(N^{-A-1/2})\). An explicit \(C_A\) is **OWED-ERiesz-\(C_A\)**. The surrogate \(\mathcal{G}_{N2}^{n}\) does not include \(E_{\mathrm{Riesz}}\).

---

## 2. The exact Gaussian surrogate \(\mathcal{G}_{N2}^{n}\)

### 2.1 Parameter and observation (N1)

Fix an integer \(d\ge 1\) and a cut \(\Gamma\) with \(\gamma_d<\Gamma<\gamma_{d+1}\). The parameter is

\[
\theta=(\gamma_1,\dots,\gamma_d,\,A_1,\dots,A_d,\,\phi_1,\dots,\phi_d)\in\Theta\subset\mathbb{R}^{3d},
\]

with \(A_j>0\). Fix an integer \(n\ge n_{\star}\) (declared in (M-n) below) and a sampling-noise variance \(\sigma_s^2>0\). Set \(\Delta:=T/n\) and \(t_k:=k\Delta\) for \(k=0,\dots,n-1\). The observation in \(\mathcal{G}_{N2}^{n}\) is the \(\mathbb{R}^n\)-valued vector \(Y=(Y_0,\dots,Y_{n-1})\) with

\[
Y_k
=m_{\theta}(t_k)+\eta_k+\varepsilon_k,
\qquad
m_{\theta}(t)=\sum_{j=1}^{d}A_j\cos(\gamma_j t+\phi_j).
\]

Both noise sources are part of the model:

- \((\eta_0,\dots,\eta_{n-1})\sim N(0,\Sigma_{\eta})\), where \(\Sigma_{\eta}\) is the Gram of the stipulated tail process at the sample times,
\[
(\Sigma_{\eta})_{k\ell}
=\frac1{2\pi}\int_{-\Omega}^{\Omega}S_{\eta}(\omega)\,e^{i\omega(t_k-t_{\ell})}\,d\omega,
\qquad
\Omega:=2\Gamma.
\]
- \(\varepsilon_k\) are i.i.d. \(N(0,\sigma_s^2)\), independent of \(\eta\) and of \(\theta\).

The law of \(Y\) is \(N\bigl(m(\theta),\,\Sigma\bigr)\) with \(\Sigma=\Sigma_{\eta}+\sigma_s^2 I_n\). Since \(\sigma_s^2>0\), one has \(\Sigma\succeq\sigma_s^2 I_n\succ 0\). The experiment is a nondegenerate finite-dimensional Gaussian location family. Every mean shift \(m(\theta)-m(\theta')\) lies in \(\mathbb{R}^n\), which is the Cameron–Martin space of \(N(0,\Sigma)\). The laws \(P_{\theta}\) are mutually equivalent. Regularity (R1)–(R4) is elementary and is recorded in §9.

### 2.2 Model clauses of \(\mathcal{G}_{N2}^{n}\)

Random marks drawn from \(1/|\zeta'|\) are **not** part of \(\mathcal{G}_{N2}^{n}\).

- **(M3′)** *Deterministic mean-field marks.* For every real frequency \(\omega\), \(r(\omega)\equiv 1\). Define \(a(\omega):=|M_W(\tfrac12+i\omega)|\). This interpolant is a declared function of frequency, not an estimator of \(1/|\zeta'(\tfrac12+i\omega)|\).
- **(M-amp)** *True surrogate amplitudes.* At the true parameter of \(\mathcal{G}_{N2}^{n}\), and at every prior draw in Theorem B, \(A_j=2\,a(\gamma_j)\). The estimator need not know this. Treating \(A_j\) as unknown nuisances in Theorem A covers unknown phase and a possible constant amplitude misspecification. Because \(\Sigma\) is independent of \(\theta\), tying \(A_j\) to \(a(\gamma_j)\) does not re-introduce a covariance-information term.
- **(M4)** *Gaussian tail regulariser, including the fill.* The process whose samples form \(\eta\) is Gaussian with spectral density \(S_{\eta}\) on \(|\omega|\le\Omega\), including every target frequency \(\gamma_j<\Gamma\). The positive value \(S_{\eta}(\gamma_j)\) is supplied by this clause, **not** by a tail calculation evaluated at a target. (The tail calculation is Proposition 4.4\(^\prime\), valid only for \(|\omega|>\Gamma\).)
- **(M-n)** *Sampling design.* \(n\ge n_{\star}:=\bigl\lceil 2\Omega T/\pi\bigr\rceil\), so that \(|\omega|\le\Omega\) implies \(\omega\Delta\le\pi/2\). Both \(\eta\) and \(\varepsilon\) are observed; neither is optional.
- **(M4″)** *Spectral floor, external anchor.* Let \(\gamma_1^{\mathrm{anchor}}:=14.134725141734693\) be the published Odlyzko first ordinate, a **design constant** independent of \(\theta\) and of \(\pi\). Set \(S_{\eta}(\omega)=a(|\omega|)^2\,\vartheta(|\omega|)\) with \(\vartheta(u)=\max\{\log(u/2\pi),\vartheta_{\min}\}\) and \(\vartheta_{\min}:=\log(\gamma_1^{\mathrm{anchor}}/2\pi)\). The floor does not follow a random parameter.
- **(M5)** *Resolvability.* \(T\cdot\min_{j\ne k}|\gamma_j-\gamma_k|\ge 2\pi K\) and \(T\cdot(\Gamma-\gamma_d)\ge 2\pi K\), with a fixed \(K\ge 4\), and \(\gamma_d<\Gamma<\gamma_{d+1}\).
- **(W′)** as in §1.1.

Phase randomisation (M1) and the ordinate point process (M2) are **not** used to construct \(\mathcal{G}_{N2}^{n}\). They appear only in §14. GUE pair correlation is not used in Theorems A or B.

The continuous band-limited record of v4 is **not** an observation of \(\mathcal{G}_{N2}^{n}\). It is not used to define Fisher information.

### 2.3 Spectral convention

\[
\mathbb{E}\bigl[\eta(t)\,\eta(t+\tau)\bigr]
=\frac1{2\pi}\int_{\mathbb{R}}S_{\eta}(\omega)\,e^{i\omega\tau}\,d\omega
\tag{2.1}
\]

for the underlying tail process (restricted to \(|\omega|\le\Omega\) in \(\Sigma_{\eta}\)). A white sequence with \(\mathrm{Var}(\varepsilon_k)=\sigma_s^2\) has discrete-time covariance \(\sigma_s^2\delta_{k\ell}\). The continuous-equivalent two-sided PSD of the sampling noise, in convention (2.1) on the Nyquist band \(|\omega|\le\pi/\Delta\), is \(S_s:=\sigma_s^2\Delta\). This identification is used only in Proposition A\(\infty\); Theorem A is stated in \((\sigma_s^2,n)\) directly.

### 2.4 Spectral density of the tail

Under (M3′), (M4), (M4″), (W′),

\[
S_{\eta}(\omega)
=a(|\omega|)^2\,\vartheta(|\omega|)
=\frac{\vartheta(|\omega|)}{(\tfrac14+\omega^2)(\tfrac94+\omega^2)},
\qquad
\vartheta(u)=\max\bigl\{\log(u/2\pi),\vartheta_{\min}\bigr\}.
\tag{2.2}
\]

This is a declared function of \(\omega\). It does not depend on \(\theta\). Defects 1 and 2 are thereby avoided.

At every target with \(\gamma_j>\gamma_1^{\mathrm{anchor}}\) (equivalently \(\gamma_j>2\pi e^{\vartheta_{\min}}\)), \(\vartheta(\gamma_j)=\log(\gamma_j/2\pi)\), so

\[
\frac{S_{\eta}(\gamma_j)}{a(\gamma_j)^2}=\log(\gamma_j/2\pi).
\tag{2.3}
\]

With (M-amp), \(A_j=2a(\gamma_j)\), hence \(S_{\eta}(\gamma_j)/A_j^2=\log(\gamma_j/2\pi)/4\). This is cancellation of the **mean-field window factor** \(a(\omega)\), not of \(1/|\zeta'(\rho)|\). The quantity \(1/|\zeta'|\) is absent from \(\mathcal{G}_{N2}^{n}\). Equation (2.3) is a comparison identity used in the named one-sided factors of Proposition A\(\infty\) and in Theorem B’s comparison skeleton **for \(j\ge 2\)**; it is not an envelope constant of the exact finite-\(n\) Fisher (4.0n), and it is not required for the sampling-noise envelope in Theorem A. It is **not** claimed \(\pi\)-almost surely on the \(j=1\) prior support (that support meets the floor; Theorem B excludes \(j=1\)).

**Attribution (Defect 15, kept).** Equation (2.2) at \(\omega=\gamma_j<\Gamma\) is the (M4) fill. Proposition 4.4\(^\prime\) derives the same algebraic expression only for \(|\omega|>\Gamma\). GAP-9 remains **OPEN** for any claim connecting this fill to a fixed zeta configuration; see §14.3.

### 2.5 Tail identity (not used at targets)

> **Proposition 4.4\(^\prime\) (tail only).** Let \(\eta^{\mathrm{ph}}(t)=2\sum_{\gamma>\Gamma}a(\gamma)\cos(\gamma t+\phi_{\gamma})\) with i.i.d. uniform phases, deterministic \(a(\gamma)\) as in (M3′), and intensity \(\lambda(\omega)=\log(\omega/2\pi)/(2\pi)\) for \(\omega>\Gamma\). Then the intensity-smoothed spectral density of \(\eta^{\mathrm{ph}}\) on \(\{\Gamma<|\omega|\le\Omega\}\) equals \(a(|\omega|)^2\log(|\omega|/2\pi)\). GUE pair correlation does not enter the first-moment density.

*Proof.* Phase averaging kills cross terms; Campbell’s formula converts the atomic masses \(a(\gamma)^2\) at \(\pm\gamma\) into \(a(\omega)^2\lambda(\omega)\,d\omega\); matching to convention (2.1) gives the claim. \(\square\)

---

## 3. Named signed factors

No displayed lower bound in this file contains an unsigned \(O(K^{-1})\). Factors used *inside a theorem* are certified or are explicit hypotheses. Factors used only as one-sided comparison slacks in Proposition A\(\infty\) are labelled as such.

**Half-width.** \(h:=2\pi K/T\). Near-tone band of tone \(j\):

\[
B_j:=\bigl\{\nu:\bigl||\nu|-\gamma_j\bigr|\le h\bigr\}\cap[-\Omega,\Omega].
\]

**Flatness (GAP-4, piecewise).** Write \(R(\omega)=2\omega/(\omega^2+1/4)+2\omega/(\omega^2+9/4)>0\). The logarithmic derivative of \(S_{\eta}\) is piecewise at the external floor:

\[
D(\omega)
:=
\partial_{\omega}\log S_{\eta}(\omega)
=
\begin{cases}
-R(\omega), & 0<\omega\le\gamma_1^{\mathrm{anchor}},\\[4pt]
-R(\omega)+\dfrac{1}{\omega\log(\omega/2\pi)}, & \omega>\gamma_1^{\mathrm{anchor}}.
\end{cases}
\tag{3.0}
\]

The second line is the log-branch formula of v6, now restricted to the region where it is the declared model. Lemma 4 bounds \(D\) on each \(B_j\) by an endpoint evaluation on the correct branch. Define

\[
1+\delta_j
\;:=\;
\exp\bigl(2h\cdot\bigl(-D(\gamma_j-h)\bigr)\bigr),
\qquad
F_j^{\mathrm{flat}}
\;:=\;
(1+\delta_j)^{-1}
=\exp\bigl(2h\,D(\gamma_j-h)\bigr),
\tag{3.1}
\]

with \(D(\gamma_j-h)\) the piecewise value from (3.0). There is no remainder \(r(\omega)\) and no “modulo OWED” in (3.1). The factor \(F_j^{\mathrm{flat}}\) is a **one-sided (in fact two-sided Loewner) comparison slack** for the symbol Gram of Lemma 1″ in Proposition A\(\infty\); it is not a multiplicative identity for the exact Fisher (4.0n), and it does not enter Theorem A. For \(j=1\) the left endpoint \(\gamma_1-h\) lies on the floor branch; the certified factor is the weaker floor-branch ceiling of Lemma 4(b), not the log-branch row of v6.

**Window (certified).** Lemma 2 supplies an absolute constant \(C_{\mathrm{win}}=84\) such that the discrete single-tone inverse satisfies the lower bound of (5.3) with

\[
F_j^{\mathrm{win}}\;:=\;1-\frac{C_{\mathrm{win}}}{\gamma_j T},
\]

provided \(\gamma_j T>C_{\mathrm{win}}\) (true for every tabulated tone at the operating \(T\)). This factor **does** enter Theorem A. A tighter continuous comparison constant \(C_{\mathrm{win}}^{\infty}=32\) is recorded as a **lower** comparison envelope for Proposition A\(\infty\) only; it is not the exact continuous-window ratio.

**Per-tone leakage (optional hypothesis, not a theorem factor).** Split the \(3\times 3\) block \(I_{jj}=I_{N_j}+I_{R_j}\) by near-tone versus complement frequency content of the sampled Gram. If there exists \(\kappa_j\ge 0\) with \(\lambda_{\max}(I_{N_j}^{-1}I_{R_j})\le\kappa_j\), set \(F_j^{\mathrm{leak}}:=(1+\kappa_j)^{-1}\). This hypothesis is **not** used in Theorem A. It is a **one-sided** comparison slack in Proposition A\(\infty\): it is never replaced by \(1\) in an equality when (B1)\(_j\) is not assumed. A numerical \(\kappa_d\) transferred from a nearby cut is **OWED-B1-receipt**, not a theorem input.

**Cross-tone (not a theorem factor).** The constant \(C_{\diamond}\) and the factor \(F^{\mathrm{cross}}(d,K)\) of v4 are **OWED-\(C_{\diamond}\)**. They are not inserted into Theorem A: the Schur step already yields a valid weaker bound from the principal \(3\times 3\). A dimension-uniform frame bound is **OWED-frame-uniform**. Schur slack is one-sided: there is no matching upper bound on \([I^{-1}]_{\gamma_j\gamma_j}\) without this row.

**Prior (Theorem B only).** The named ratio \(F_j^{\mathrm{prior}}:=I^{\mathrm{skel},\uparrow}_j/\bigl(I^{\mathrm{skel},\uparrow}_j+I(\pi_{\gamma_j})\bigr)\) is a **comparison skeleton**, not a theorem factor of Theorem B. Here \(I^{\mathrm{skel},\uparrow}_j\) is the locally-white leading-term envelope of §8.3, which is **not** identified with \(\mathbb{E}_{\pi}[I_{\mathrm{tied},j}]\), and \(I(\pi_{\gamma_j})=\pi^2/\rho_j^2\) with the admissible half-width \(\rho_j\) of (P1″).

---

## 4. Lemma 1″ (Loewner) and Lemma 4 (exact \(D\), piecewise)

### 4.1 Lemma 1″ — Loewner order, not entrywise (N6)

Let \(\partial_{\alpha}m_{\theta}\) denote a coordinate derivative, sampled at \((t_k)\) to give a vector in \(\mathbb{R}^n\). Write \(D_j\in\mathbb{R}^{n\times 3}\) for the three sampled derivatives of tone \(j\). The principal block is \(I_{jj}=D_j^{\mathsf T}\Sigma^{-1}D_j\).

For the fine-sampling analysis, let \(G^P_j\) denote the (continuous or discrete) near-tone Euclidean Gram of those derivatives after frequency projection onto \(B_j\). Pointwise bounds on a positive continuous spectral density imply a **Loewner** sandwich, not an entrywise one: cross-Gram integrands have no fixed sign.

> **Lemma 1″ (projected local whitening, Loewner order).** Assume \(S_{\eta}\) is continuous and bounded below on \([-\Omega,\Omega]\), and that \(S_{\eta}\) varies by at most a factor \(1+\delta_j\) on \(B_j\). Then
>
> \[
> (1+\delta_j)^{-1}S_{\eta}(\gamma_j)^{-1}\,G^P_j
> \;\preceq\;
> I_{N_j}^{\mathrm{(sym)}}
> \;\preceq\;
> (1+\delta_j)\,S_{\eta}(\gamma_j)^{-1}\,G^P_j
> \]
>
> in the Loewner order on \(3\times 3\) symmetric matrices, where \(I_{N_j}^{\mathrm{(sym)}}\) is the Gram of the \(B_j\)-projected derivatives in the inner product with weight \(1/S_{\eta}\). With (3.1), one may take this \(1+\delta_j\).

*Proof.* Pointwise \(S_{\eta}(\gamma_j)/(1+\delta_j)\le S_{\eta}(\nu)\le(1+\delta_j)S_{\eta}(\gamma_j)\) on \(B_j\), hence the same bounds for \(1/S_{\eta}\). If \(g(\nu)\in\mathbb{C}^3\) stacks the three Fourier transforms, the Gram is \(\int_{B_j} g(\nu)g(\nu)^*\,S_{\eta}(\nu)^{-1}\,d\nu/(2\pi)\). For a positive scalar \(m(\nu)\) with \(m_{-}\le m(\nu)\le m_{+}\), one has \(m_{-}GG^*\preceq \int m\,gg^*\preceq m_{+}GG^*\) in Loewner order. Entrywise inequalities are not claimed. \(\square\)

> **Lemma 1-compare.** Frequency projection is an orthogonal projection on \(L^2\), so \(G^P_j\preceq G_j\) in the Loewner order.

### 4.2 Lemma 4 — exact bound on \(D\) by endpoint evaluation (GAP-4, piecewise)

> **Lemma 4 (exact logarithmic derivative on the Lemma-1 band; two branches).** Let \(h=2\pi K/T\). Write \(R(\omega)=2\omega/(\omega^2+1/4)+2\omega/(\omega^2+9/4)\).
>
> **(a) Log branch.** On \([\gamma_1^{\mathrm{anchor}},\Omega]\), with \(D\) the second line of (3.0),
> \[
> D(\omega)<0,
> \qquad
> D'(\omega)>0,
> \qquad
> \sup_{\omega\in[\gamma_j-h,\gamma_j+h]\cap[\gamma_1^{\mathrm{anchor}},\Omega]}\lvert D(\omega)\rvert
> =-D(\text{left endpoint of that interval}).
> \]
> For every \(j\ge 2\) at the operating point, \(B_j\subset(\gamma_1^{\mathrm{anchor}},\Omega]\), so this is the full band, the left endpoint is \(\gamma_j-h\), and (3.1) holds with the log-branch \(D\).
>
> **(b) Floor branch.** On \((0,\gamma_1^{\mathrm{anchor}}]\), \(D=-R\). For \(\omega>3/2\), \(R'(\omega)<0\), hence \(D'=-R'>0\) and \(\lvert D\rvert=R\) is strictly decreasing. On the \(j=1\) band \([\gamma_1-h,\gamma_1+h]\), \(\sup\lvert D\rvert=R(\gamma_1-h)\). Consequently
> \[
> 1+\delta_1\le\exp\bigl(2h\,R(\gamma_1-h)\bigr).
> \]
> This is (3.1) on the floor branch. It is weaker than the (invalid) log-branch evaluation at \(\gamma_1-h\).

*Proof of (a).* Write \(D=-R+P\) with \(P(\omega)=1/(\omega L(\omega))\), \(L(\omega)=\log(\omega/2\pi)\). For \(\omega\ge\omega_{\min}:=\gamma_1^{\mathrm{anchor}}\), one has \(L\ge L_1:=\log(\gamma_1^{\mathrm{anchor}}/2\pi)=0.810757479321445\) and

\[
R(\omega)
\ge\frac{4\omega}{\omega^2+9/4}
=\frac{4}{\omega+9/(4\omega)}
>\frac{4}{\omega+9/(4\omega_{\min})}.
\]

With \(\omega_{\min}=14.134725141734693\), one has \(9/(4\omega_{\min})=9/56.538900566938772=0.159183\), and \(4L_1=3.243030>1\), hence \(R>P\) and \(D<0\). (This is the same comparison as v6, evaluated at the legal left endpoint \(\gamma_1^{\mathrm{anchor}}\) rather than at \(\gamma_1-h\).)

Differentiating on the log branch,

\[
D'(\omega)
=\frac{2(\omega^2-1/4)}{(\omega^2+1/4)^2}
+\frac{2(\omega^2-9/4)}{(\omega^2+9/4)^2}
-\frac{L+1}{\omega^2 L^2}.
\]

The first two summands are positive for \(\omega>3/2\). A lower bound is \(4(\omega^2-9/4)/(\omega^2+9/4)^2\). The map \(L\mapsto(L+1)/L^2=1/L+1/L^2\) is decreasing for \(L>0\), so on \(\omega\ge\omega_{\min}\) one has \((L+1)/L^2\le(L_1+1)/L_1^2\). Arithmetic:

\[
L_1^2=0.657327698,\qquad
\frac{L_1+1}{L_1^2}=\frac{1.810757479321445}{0.657327698}=2.75472.
\]

Thus \(D'(\omega)>0\) on \([\omega_{\min},\infty)\) as soon as \(4u(u-9/4)\ge 2.75472\,(u+9/4)^2\) for \(u=\omega^2\ge\omega_{\min}^2\). Now \(\omega_{\min}^2=14.134725141734693^2=199.790455\). The difference \(\psi(u)=4u(u-9/4)-2.75472(u+9/4)^2\) has \(\psi'(u)=8u-9-5.50944(u+9/4)=2.49056\,u-21.396>0\) for \(u>9\). At the left endpoint, \(4\times 199.790455\times 197.540455=157869.4\) and \(2.75472\times 202.040455^2=2.75472\times 40820.35=112447\), so \(\psi(\omega_{\min}^2)>0\). Hence \(D'>0\) on the log-branch operating range, \(D\) is strictly increasing, \(\lvert D\rvert=-D\) is strictly decreasing, and the supremum of \(\lvert D\rvert\) on a log-branch band is attained at the left endpoint. Integrating \(D\) along the band gives the log-ratio bound of length at most \(2h\), and exponentiating gives (3.1). \(\square\)

*Proof of (b).* On the floor, \(\vartheta\equiv\vartheta_{\min}\), so \(\partial_{\omega}\log S_{\eta}=-R\). For \(\omega>3/2\),

\[
R'(\omega)
=\frac{2(1/4-\omega^2)}{(\omega^2+1/4)^2}
+\frac{2(9/4-\omega^2)}{(\omega^2+9/4)^2}<0,
\]

hence \(D'=-R'>0\) and \(\lvert D\rvert=R\) decreases. The \(j=1\) band meets the floor on \([\gamma_1-h,\gamma_1^{\mathrm{anchor}}]\) and the log branch on \([\gamma_1^{\mathrm{anchor}},\gamma_1+h]\). On the log side \(\lvert D\rvert=R-P<R\). The global supremum on the band is therefore \(R(\gamma_1-h)\). Since \(S_{\eta}\) is continuous (\(C^0\) at the kink) and absolutely continuous, \(\lvert\log S_{\eta}(\omega)-\log S_{\eta}(\gamma_1)\rvert\le 2h\cdot R(\gamma_1-h)\). Exponentiating is the displayed ceiling.

Arithmetic at \(\omega_{-}=\gamma_1-h=12.674937282357\):

\[
\omega_{-}^2=160.654035,\quad
\frac{2\omega_{-}}{\omega_{-}^2+1/4}=0.15754654,\quad
\frac{2\omega_{-}}{\omega_{-}^2+9/4}=0.15561232,
\]

\[
R(\omega_{-})=0.31315886,\qquad
2h\,R(\omega_{-})=0.914291,\qquad
\exp\bigl(2h\,R(\omega_{-})\bigr)=2.49500569.
\]

Round **UP**: \(1+\delta_1\le\mathbf{2.49501}\). Then \(F_1^{\mathrm{flat}}\ge 1/2.49500569=0.4008007\), **DOWN** \(\mathbf{0.4008}\). \(\square\)

Widths are \(O(1/T)\). A uniform bound of \(F^{\mathrm{flat}}\) over an interval of length \(O(1/T)\) is therefore the same bound evaluated at the leftmost frequency that appears; this is used in Theorem B as a comparison-factor bound, not as a factor of \(I_{\mathrm{tied}}\), and only for \(j\ge 2\) (log branch).

The superseded leading-order ceiling \(\exp(16\pi K/(\gamma_j T))\) (which dropped \(r(\omega)=D(\omega)+4/\omega\)) is **not** used. The v6 log-branch \(j=1\) row (UP \(1.796\), DOWN \(0.5570\)) is **withdrawn**: it evaluated the wrong branch, and even as a log-branch number its directed roundings were unsafe.

---

## 5. Lemma 2 — discrete single-tone \(3\times 3\), certified \(C_{\mathrm{win}}\)

Let \(m(t)=A\cos(\omega t+\phi)\) on the sample grid \(t_k=k\Delta\), \(k=0,\dots,n-1\), \(\Delta=T/n\), \(n\ge n_{\star}\), and let the envelope noise be white of variance \(\sigma_s^2\) (the sampling-noise envelope \(\Sigma\succeq\sigma_s^2 I_n\)). The discrete Gram \(G^{\mathrm{disc}}\) has entries \(\sum_{k=0}^{n-1}(\partial_{\alpha}m)(t_k)(\partial_{\beta}m)(t_k)\). Write \(\psi:=\omega\Delta\). Under (M-n), \(\omega\le\Omega\) implies \(\psi\le\pi/2\), hence \(\lvert\sin\psi\rvert\ge 2\psi/\pi=2\omega T/(\pi n)\).

The non-oscillatory parts of the **unnormalised** \((\omega,\phi)\) block (replacing \(\sin^2\) by \(1/2\)) are the exact power sums

\[
a_0=\frac{A^2 T^2(n-1)(2n-1)}{12n},\quad
b_0=\frac{A^2 T(n-1)}{4},\quad
c_0=\frac{A^2 n}{2}.
\]

Let \(H\) be the \((\omega,\phi)\) block of \(G^{\mathrm{disc}}/A^2\) (normalised). The corresponding non-oscillatory entries are \(a_0/A^2\), \(b_0/A^2\), \(c_0/A^2\). Their Schur complement has determinant \(T^2(n^2-1)/48\) and inverse \(\omega\omega\)-entry

\[
[H_0^{-1}]_{\omega\omega}
=\frac{24}{n T^2}\cdot\frac{n^2}{n^2-1}
\ge
\frac{24}{n T^2}.
\tag{5.1}
\]

(The unnormalised inverse carries an extra \(A^{-2}\); relative remainder bounds below are homogeneous of degree 0 in \(A\), so they apply equally to \(H\) and to the unnormalised block. This is the normalisation step missing from v6: (5.3) is a statement about the normalised block \(H\), and (5.1) is written for that block.)

Oscillatory remainders are controlled by Abel summation. If \(S_m=\sum_{k=0}^{m-1}e^{ik\theta}\) with \(\theta=2\psi\), then \(\lvert S_m\rvert\le 1/\lvert\sin\psi\rvert\).

**Missing Abel step (v6 referee V6-R4-M2).** Let \(A_m=\sum_{k=0}^{m}e^{ik\theta}\) (so \(A_{-1}=0\)) and \(b_k=k^2\). Abel summation gives
\[
\sum_{k=0}^{n-1}k^2 e^{ik\theta}
=A_{n-1}(n-1)^2-\sum_{k=0}^{n-2}A_k\bigl((k+1)^2-k^2\bigr).
\]
Since \(\lvert A_k\rvert\le 1/\lvert\sin\psi\rvert\) and \((k+1)^2-k^2=2k+1\),
\[
\Bigl\lvert\sum_{k=0}^{n-1}k^2 e^{ik\theta}\Bigr\rvert
\le\frac{(n-1)^2}{\lvert\sin\psi\rvert}+\frac1{\lvert\sin\psi\rvert}\sum_{k=0}^{n-2}(2k+1).
\]
The sum of the first \(n-1\) odd numbers is \((n-1)^2\), hence
\[
\Bigl\lvert\sum_{k=0}^{n-1}k^2 e^{ik\theta}\Bigr\rvert
\le\frac{2(n-1)^2}{\lvert\sin\psi\rvert}.
\]
(The printed v6 bound \(2n^2/\lvert\sin\psi\rvert\) is valid but strictly coarser; it is not used. The same Abel identity with \(b_k=k\) gives \(\lvert\sum k\,e^{ik\theta}\rvert\le 2(n-1)/\lvert\sin\psi\rvert\), and \(\lvert\sum e^{ik\theta}\rvert\le 1/\lvert\sin\psi\rvert\).)

Transferring to \(t_k=\Delta k\) and using \(\lvert\sin\psi\rvert\ge 2\omega T/(\pi n)\): the oscillatory part of the normalised \(a\)-entry has size at most \(\Delta^2(n-1)^2/\lvert\sin\psi\rvert\), so against \(a_0/A^2=T^2(n-1)(2n-1)/(12n)\)
\[
\varepsilon_a
\le\frac{6\pi(n-1)}{\tau(2n-1)}
\le\frac{3\pi}{\tau},
\qquad
\varepsilon_b=\frac{2\pi}{\tau},\qquad
\varepsilon_c=\frac{\pi}{2\tau},
\qquad\tau:=\omega T.
\]
(The inequality \((n-1)/(2n-1)<1/2\) is the last step to \(3\pi/\tau\). Had the coarser \(2n^2\) Abel bound been retained, one would have obtained \(\varepsilon_a\le 6\pi n^2/[\tau(n-1)(2n-1)]\), as the referee computed; that coarser bound is not used.)

> **Lemma 2 (discrete white \(3\times 3\), certified window).** Assume \(n\ge n_{\star}\) and \(\omega T\ge\gamma_1 T-2\pi K\). Let \(H\) be the \((\omega,\phi)\) block of \(G^{\mathrm{disc}}/A^2\). Then
>
> \[
> [H^{-1}]_{\omega\omega}
> \;\ge\;
> F^{\mathrm{win}}(\omega)\cdot\frac{24}{n T^2},
> \qquad
> F^{\mathrm{win}}(\omega)=1-\frac{84}{\omega T}.
> \tag{5.3}
> \]
> Hence under the sampling-noise envelope \(\Sigma\succeq\sigma_s^2 I_n\),
> \[
> \bigl[I_{jj}^{-1}\bigr]_{\omega\omega}
> \;\ge\;
> F_j^{\mathrm{win}}\cdot\frac{24\,\sigma_s^2}{A_j^2 n T^2}.
> \tag{5.4}
> \]
> The constant is \(C_{\mathrm{win}}=84\). (The \(A\)-row of the \(3\times 3\) only increases the \(\omega\omega\) inverse, by the same Schur comparison as Lemma 3′(a); a **lower** bound from the \((\omega,\phi)\) block is therefore valid for the \(3\times 3\). This Schur direction is **not** available for an upper bound; see §7bis.5.)

*Proof of (5.3).* Write \(a=(a_0/A^2)(1+\delta_a)\) etc.\ with \(\lvert\delta_a\rvert\le\varepsilon_a\). For an upper bound on \(\det=ac-b^2\), take the extremes \(a\le (a_0/A^2)(1+\varepsilon_a)\), \(c\le (c_0/A^2)(1+\varepsilon_c)\), \(\lvert b\rvert\ge (b_0/A^2)(1-\varepsilon_b)\). As in the expansion under (5.1), \(b_0^2/\det_0=3(n-1)/(n+1)\le 3\), and

\[
\frac{\det_{\mathrm{hi}}}{\det_0}
\le 1+4\varepsilon_a+4\varepsilon_c+6\varepsilon_b+4\varepsilon_a\varepsilon_c
=1+\frac{26\pi}{\tau}+\frac{6\pi^2}{\tau^2}.
\]

The inverse ratio against \([H_0^{-1}]_{\omega\omega}\) is at least \((1-\varepsilon_c)\) over that quantity. Dropping the favourable factor \(n^2/(n^2-1)\ge 1\) in (5.1), the ratio against \(24/(n T^2)\) is at least

\[
r(\tau)
=\frac{1-\pi/(2\tau)}{1+26\pi/\tau+6\pi^2/\tau^2}.
\]

Then
\[
\tau\bigl(1-r(\tau)\bigr)
=\frac{53\pi/2+6\pi^2/\tau}{1+26\pi/\tau+6\pi^2/\tau^2}
\le\frac{53\pi}{2}+\frac{6\pi^2}{\tau_{\min}}
\]
with the denominator \(>1\) and \(\tau_{\min}=(\gamma_1-h)T\). Arithmetic: \(\gamma_1-h=12.674937282357\), \(\tau_{\min}=12.674937282357\times 17.2167079396264295=218.22069\), \(53\pi/2=83.252182\), \(6\pi^2/\tau_{\min}=59.217626/218.22069=0.271366\), sum \(83.523571\le 83.53<84\) (corrected 2026-08-26; was misprinted 83.523548). Taking \(C_{\mathrm{win}}=84\) gives \(1-84/\tau\le r(\tau)\) for all \(\tau\ge\tau_{\min}\), and \(F^{\mathrm{win}}>0\). \(\square\)

*Convention.* Rife–Boorstyn and Kay, Example 3.14, quote \(12\) because they use a complex exponential or a different PSD identification. In (2.1) with a real cosine and both \(A\) and \(\phi\) unknown, \(24\) is the leading constant of the *continuous* white formula; the discrete leading constant in (5.1) is the matching \(24/(n T^2)\). Getting the factor wrong changes the RMSE coefficient by \(\sqrt{2}\).

**Continuous comparison constant (Proposition A\(\infty\) only, lower envelope).** For the continuous-time \((\omega,\phi)\) Gram of Lemma 2 in v4, the remainder identities

\[
\bigl\lvert\tfrac{T^3}6-\int_0^T t^2\sin^2\bigr\rvert
\le\frac{T^2}{2\omega}+\frac T{2\omega^2}+\frac1{4\omega^3},\quad
\bigl\lvert\tfrac{T^2}4-\int_0^T t\sin^2\bigr\rvert
\le\frac T{2\omega}+\frac1{4\omega^2},\quad
\bigl\lvert\tfrac T2-\int_0^T\sin^2\bigr\rvert
\le\frac1{2\omega}
\]

give, by the identical \(ac-b^2\) envelope, a ratio against \(24/T^3\) whose implied \(C(\omega)=(1-\mathrm{ratio})\,\omega T\) is at most \(32\) on \([\gamma_1-h,\Omega]\) at the operating \(T\). (The three v6 named evaluations \(25.77\), \(31.75\), \(29.27\) are **withdrawn**: they do not follow from the displayed remainder calculation. The constant \(32\) remains a safe **lower** continuous comparison ceiling.) We take \(C_{\mathrm{win}}^{\infty}:=32\) as a certified **lower** continuous comparison constant. It is **not** the theorem constant; the theorem uses \(C_{\mathrm{win}}=84\). It is **not** the exact continuous-window ratio.

A numerical white-noise check of the *continuous* \(3\times 3\) at \(T=\log(3\cdot 10^7)\), from `t1_verify.py` / `T1_VERIFY_RECEIPT.json` block 4, gave \(T^3[I^{-1}]_{\omega\omega}=23.927,\,23.824,\,23.947\) at \(\omega=3.7,14.13,49.77\). All lie below \(24\). That check is not a substitute for \(C_{\mathrm{win}}\) (GAP-8).

---

## 6. Lemma 3′ — Schur reduction and the unused cross-tone factor (N5)

**(a) Nuisance Schur complement (the step from \(3d\times 3d\) to \(3\times 3\)).** Let \(I(\theta)\in\mathbb{R}^{3d\times 3d}\) be positive definite, and let \(I_{jj}\) be the principal \(3\times 3\) corresponding to \((A_j,\gamma_j,\phi_j)\). Partition \(I=\bigl(\begin{smallmatrix}A&B\\B^{\mathsf T}&C\end{smallmatrix}\bigr)\) with \(A=I_{jj}\). The corresponding block of \(I^{-1}\) is the inverse of the Schur complement \(A-BC^{-1}B^{\mathsf T}\). Since \(BC^{-1}B^{\mathsf T}\succeq 0\),

\[
A-BC^{-1}B^{\mathsf T}\;\preceq\;A,
\qquad
\bigl[I^{-1}\bigr]_{jj}
=(A-BC^{-1}B^{\mathsf T})^{-1}
\;\succeq\;
A^{-1}=I_{jj}^{-1}
\]

in the Loewner order. In particular

\[
\bigl[I^{-1}\bigr]_{\gamma_j\gamma_j}
\;\ge\;
\bigl[I_{jj}^{-1}\bigr]_{\gamma_j\gamma_j}.
\tag{6.1}
\]

This is a valid weaker per-tone Cramér–Rao bound: unknown other tones can only increase the \(\gamma_j\)-variance bound. The diagonal block \(I_{jj}=D_j^{\mathsf T}\Sigma^{-1}D_j\) is exactly the single-tone Gram in the same noise (other tones do not enter the \(j\)-derivatives). No unproved \(F^{\mathrm{cross}}\) is required for (6.1). The inequality is **one-sided**; a matching upper bound on \([I^{-1}]_{\gamma_j\gamma_j}\) is **OWED-\(C_{\diamond}\)**.

**(b)** Off-diagonal \(3\times 3\) blocks and a factor \(F^{\mathrm{cross}}(d,K)=(1+C(d,K)/K)^{-1}\) with \(C(d,K)=(C_{\diamond}/\pi)H_{d-1}\) would *tighten* (6.1) toward a block-diagonal approximation. The constant \(C_{\diamond}\) is **OWED-\(C_{\diamond}\)**. A dimension-uniform confluent Ingham / Montgomery–Vaughan bound for the coloured family \(\{e^{\pm i\gamma_j t},\, t e^{\pm i\gamma_j t}\}\) with nuisance Schur complements is **OWED-frame-uniform** and is not claimed. Pairwise \(O(K^{-1})\) estimates do not imply a \(d\)-uniform operator bound.

**(c)** Near-tone bands of width \(2h\) overlap when gaps are less than \(2h\). Condition (M5) only guarantees gaps \(\ge h\). Overlap is harmless for (6.1). Overlap *is* an obstruction to treating the \(B_j\) as disjoint supports in a simultaneous multi-tone frame bound; that obstruction is **OWED-overlap**.

---

## 7. Theorem A — pointwise Cramér–Rao in \(\mathcal{G}_{N2}^{n}\)

> **Theorem A (pointwise CR, discrete Gaussian surrogate, fixed \(d\)).**
> Fix \(d\ge 1\), \(K\ge 4\), \(n\ge n_{\star}\), and \(\sigma_s^2>0\). Assume \(\mathcal{G}_{N2}^{n}\) with clauses (M3′), (M-amp), (M4), (M-n), (M4″), (M5), (W′). Let \(\widehat\theta\) be any estimator of \(\theta\) that is unbiased on an open neighbourhood of the true \(\theta\) and is a measurable function of \(Y\in\mathbb{R}^n\). Then for each \(j\in\{1,\dots,d\}\),
>
> \[
> \mathrm{Var}(\widehat{\gamma}_j)
> \;\ge\;
> \bigl[I(\theta)^{-1}\bigr]_{\gamma_j\gamma_j}
> \;\ge\;
> \bigl[I_{jj}(\theta)^{-1}\bigr]_{\gamma_j\gamma_j}
> \;\ge\;
> F_j^{\mathrm{win}}
> \cdot
> \frac{24\,\sigma_s^2}{A_j^2 n T^2},
> \tag{A.1}
> \]
>
> with \(I_{\alpha\beta}(\theta)=(\partial_{\alpha}m)^{\mathsf T}\Sigma^{-1}(\partial_{\beta}m)\) as in (4.0n), \(F_j^{\mathrm{win}}=1-84/(\gamma_j T)\), and \(\Sigma=\Sigma_{\eta}+\sigma_s^2 I_n\). The first inequality is the Cramér–Rao inequality in a regular finite-dimensional Gaussian location family. The second is Lemma 3′(a). The third is Lemma 2. The bound is for this fixed \(d\); it is not asserted uniformly in \(d\).
>
> **Arithmetic interpretation (not used in the Fisher calculation).** If the surrogate mean is identified with the trigonometric sum in Proposition R, assume RH, simplicity of every nontrivial zero, and \(J_{-1}(T)=O(T)\). That identification is OWED-S1.

*Proof.* The law of \(Y\) is \(N(m(\theta),\Sigma)\) with \(\Sigma\) independent of \(\theta\) and \(\Sigma\succ 0\). The Fisher information of a Gaussian location family is exactly (4.0n); (R1)–(R4) hold as in §9. Cramér–Rao for unbiased estimators gives \(\mathrm{Cov}(\widehat\theta)\succeq I(\theta)^{-1}\). Lemma 3′(a) yields (6.1). Lemma 2 with the envelope \(\Sigma^{-1}\preceq\sigma_s^{-2}I_n\) (equivalently \(\Sigma\succeq\sigma_s^2 I_n\)) yields (5.4). Collecting is (A.1). Unbiasedness converts \(\sqrt{\mathrm{Var}}\) into RMSE. \(\square\)

**Not claimed.** A \(T^{-3}\) law. A numerical product of \(F^{\mathrm{flat}}F^{\mathrm{leak}}F^{\mathrm{cross}}F^{\mathrm{win}}\). A max-\(j\) law attained at \(j=d\) (**OWED-last-tone**). Transfer to the phase sum.

**Corollary A (sample complexity, sampling-noise envelope).** If some \(j\) has \(\mathrm{RMSE}(\widehat{\gamma}_j)\le\varepsilon\) and \(F_j^{\mathrm{win}}>0\), then from (A.1)

\[
n T^2
\;\ge\;
F_j^{\mathrm{win}}\cdot\frac{24\,\sigma_s^2}{A_j^2\varepsilon^2}.
\]

This is a finite-\(n\) resource bound in \((n,T,\sigma_s)\). It is not the \(T\sim\varepsilon^{-2/3}\) law of the continuous locally-white heuristic.

---

## 7bis. Proposition A\(\infty\) — comparison envelope of the exact finite-\(n\) Fisher

Write \(S_s:=\sigma_s^2\Delta=\sigma_s^2 T/n\) for the continuous-equivalent sampling-noise PSD in convention (2.1) on the Nyquist band. Let \(I^{(n)}\) be the exact discrete Fisher (4.0n). Let \(D\in\mathbb{R}^{n\times 3d}\) stack the sampled mean-coordinate derivatives, and write \(G^{\mathrm{disc}}:=D^{\mathsf T}D\), so \(I^{(n)}=D^{\mathsf T}\Sigma^{-1}D\). No limiting equality is claimed.

### 7bis.1 Operator sandwich of (4.0n), no Szegő

On \([0,\gamma_1^{\mathrm{anchor}}]\), \(\vartheta\equiv\vartheta_{\min}\) and the denominator of (2.2) is increasing, so \(S_{\eta}\) is decreasing. On \([\gamma_1^{\mathrm{anchor}},\Omega]\), Lemma 4(a) gives \(D<0\), so \(S_{\eta}\) is decreasing. Hence

\[
S_{\max}
\;:=\;
\operatorname{ess\,sup}_{|\omega|\le\Omega}S_{\eta}(\omega)
=S_{\eta}(0)
=\frac{\vartheta_{\min}}{(\tfrac14)(\tfrac94)}
=\frac{16}{9}\log(\gamma_1^{\mathrm{anchor}}/2\pi).
\]

Arithmetic: \(L_1=\log(\gamma_1^{\mathrm{anchor}}/2\pi)=0.810757479321445\), \(16\times 0.810757479321445=12.97211966914312\), \(12.97211966914312/9=1.441346629904791\). Round **UP**: \(S_{\max}\le\mathbf{1.4414}\). (The v6 intermediates \(L_1=0.81075727\) and \(S_{\max}=1.4413462578\) are replaced by these digits; the final ceiling is unchanged.)

> **Lemma 5 (Parseval sandwich of \(\Sigma\); no Szegő).** Assume (M-n), so \(\Omega\Delta\le\pi/2<\pi\). Then
> \[
> \sigma_s^2 I_n
> \;\preceq\;
> \Sigma
> \;\preceq\;
> \bigl(\sigma_s^2+S_{\max}/\Delta\bigr)I_n.
> \]
> Equivalently, writing \(S_s=\sigma_s^2\Delta\),
> \[
> \frac{\Delta}{S_s+S_{\max}}\,G^{\mathrm{disc}}
> \;\preceq\;
> I^{(n)}
> \;\preceq\;
> \frac{\Delta}{S_s}\,G^{\mathrm{disc}}.
> \tag{A\(\infty\).0}
> \]

*Proof.* The lower bound is \(\Sigma=\Sigma_{\eta}+\sigma_s^2 I_n\succeq\sigma_s^2 I_n\). For the upper bound, let \(D_x(\omega)=\sum_{k=0}^{n-1}x_k e^{i\omega k\Delta}\). Substitute \(\nu=\omega\Delta\):

\[
\frac1{2\pi}\int_{-\pi/\Delta}^{\pi/\Delta}\lvert D_x(\omega)\rvert^2\,d\omega
=\Delta^{-1}\cdot\frac1{2\pi}\int_{-\pi}^{\pi}\Bigl\lvert\sum_{k=0}^{n-1}x_k e^{ik\nu}\Bigr\rvert^2 d\nu
=\Delta^{-1}\|x\|^2,
\]

by orthonormality of Fourier characters on the circle. Then

\[
x^{\mathsf T}\Sigma_{\eta}x
=\frac1{2\pi}\int_{-\Omega}^{\Omega}S_{\eta}(\omega)\lvert D_x(\omega)\rvert^2\,d\omega
\le S_{\max}\cdot\frac1{2\pi}\int_{-\Omega}^{\Omega}\lvert D_x\rvert^2\,d\omega
\le S_{\max}\cdot\frac1{2\pi}\int_{-\pi/\Delta}^{\pi/\Delta}\lvert D_x\rvert^2\,d\omega
=\frac{S_{\max}}{\Delta}\|x\|^2,
\]

using only \(S_{\eta}\le S_{\max}\) and nonnegativity of \(\lvert D_x\rvert^2\). The band-edge jump of \(S_{\eta}\) (positive at \(\Omega\), zero beyond) and the \(n\)-dependence of the discrete-time symbol never enter. Inverting the eigenvalue bounds in Loewner order gives (A\(\infty\).0). \(\square\)

The term \(E_{\mathrm{Sz}}\) of v5 is **OWED-NOT-USED**. No conclusion in this file consumes it. A \(C^1\)-symbol Szegő remainder is not invoked.

### 7bis.2 Named one-sided slacks (not identities)

The following comparison factors are **not** multiplicative identities for \(I^{(n)}\). Each slack is one-sided as stated.

- **Flatness.** Lemma 1″ supplies the two-sided Loewner sandwich of the *comparison* near-tone symbol Gram \(I_{N_j}^{\mathrm{(sym)}}\),
  \[
  F_j^{\mathrm{flat}}\,S_{\eta}(\gamma_j)^{-1}G^P_j
  \;\preceq\;
  I_{N_j}^{\mathrm{(sym)}}
  \;\preceq\;
  \bigl(F_j^{\mathrm{flat}}\bigr)^{-1}S_{\eta}(\gamma_j)^{-1}G^P_j.
  \]
  This Gram is **not** identified with \(I^{(n)}\) or with \(I_{jj}^{(n)}\). For \(j=1\) the factor is the floor-branch value of Lemma 4(b).
- **Continuous window.** \(F_j^{\mathrm{win},\infty}=1-32/(\gamma_j T)\) is a **lower** comparison envelope for the continuous white \((\omega,\phi)\) inverse. It is not the exact continuous-window ratio (which also depends on phase).
- **Leakage.** \(F_j^{\mathrm{leak}}=(1+\kappa_j)^{-1}\) is a one-sided bound under (B1)\(_j\). If (B1)\(_j\) is not assumed, this factor is omitted; it is **not** replaced by \(1\) in any equality.
- **Schur.** \([(I^{(n)})^{-1}]_{\gamma_j\gamma_j}\ge[I_{jj}^{(n)^{-1}}]_{\gamma_j\gamma_j}\) by (6.1), one-sided. A matching upper bound is **OWED-\(C_{\diamond}\)**.
- **\(E_{\mathrm{Sz}}\).** OWED-NOT-USED.

### 7bis.3 Riemann-sum error for the specific Gram integrands (shown; not a theorem factor)

> **Lemma 6 (elementary Riemann comparison).** Let \(f\) be \(C^1\) on \([0,T]\) and \(\Delta=T/n\), \(t_k=k\Delta\). Then
> \[
> \Bigl\lvert\Delta\sum_{k=0}^{n-1}f(t_k)-\int_0^T f(t)\,dt\Bigr\rvert
> \le\frac{T\Delta}{2}\,\|f'\|_{\infty}.
> \]

*Proof.* On each cell \([k\Delta,(k+1)\Delta]\),
\(\bigl\lvert\int_{k\Delta}^{(k+1)\Delta}(f(t)-f(t_k))\,dt\bigr\rvert\le\|f'\|_{\infty}\int_0^{\Delta}u\,du=\|f'\|_{\infty}\Delta^2/2\). Summing \(n\) cells gives the claim. \(\square\)

The specific quadratic-form integrands of the discrete Gram are \(f_c(t)=\sin^2(\omega t+\phi)\), \(f_b(t)=t\sin^2(\omega t+\phi)\), \(f_a(t)=t^2\sin^2(\omega t+\phi)\), with \(\lvert f_c'\rvert\le\omega\), \(\lvert f_b'\rvert\le 1+T\omega\), \(\lvert f_a'\rvert\le 2T+T^2\omega\). Relative to the leading monomials \(T/2\), \(T^2/4\), \(T^3/6\), Lemma 6 yields

\[
\varepsilon_c^{\mathrm{Riem}}\le\frac{\omega T}{n},\qquad
\varepsilon_b^{\mathrm{Riem}}\le\frac{2}{n}+\frac{2\omega T}{n},\qquad
\varepsilon_a^{\mathrm{Riem}}\le\frac{6}{n}+\frac{3\omega T}{n}.
\]

**Recomputation of \(\varepsilon_a^{\mathrm{Riem}}\) (v6 referee §III).** The bound is
\[
\frac{(T\Delta/2)\,(2T+T^2\omega)}{T^3/6}
=\frac{3\Delta(2T+T^2\omega)}{T^2}
=\frac{3}{n}\bigl(2+T\omega\bigr)
=\frac{6}{n}+\frac{3\omega T}{n}.
\]
The v6 display \(6/(nT)+3\omega/n\) omitted a factor \(T\) in the second summand and placed an extra \(T\) in the first; it is withdrawn.

At \(n=n_{\star}=1124\), \(\omega=\Omega=102.46724068\): \(\Omega T/\pi=561.545926124806\), so \(\Omega T=561.545926124806\times\pi=1764.148555\). Then
\[
\frac{6}{1124}=0.005338078,\qquad
\frac{3\times 1764.148555}{1124}=4.70858155,\qquad
\varepsilon_a^{\mathrm{Riem}}\le 4.71391964.
\]
(The withdrawn expression evaluated to \(0.27379913\).) The derivative bound is therefore **not a theorem factor**. It is recorded because it is the elementary summation-vs-integral comparison for these integrands; it is too crude for the \(b\) and \(c\) entries at the band edge, and the \(a\)-entry bound exceeds \(1\).

The comparison actually used for \(G^{\mathrm{disc}}\) is Lemma 2 (Abel remainder against the exact discrete power sums \(a_0,b_0,c_0\)) together with the exact monomial identities

\[
\Delta\sum_{k=0}^{n-1}t_k^2
=\frac{T^3(n-1)(2n-1)}{6n^2},
\qquad
\int_0^T t^2\,dt=\frac{T^3}{3},
\]

so the ratio of left-Riemann to integral for \(t^2\) is \((n-1)(2n-1)/(2n^2)=1-3/(2n)+1/(2n^2)\). At \(n\ge n_{\star}=1124\), \(3/(2n)\le 3/2248=0.0013345\), **UP** \(0.001335\).

### 7bis.4 Two-sided discrete-white inverse of the \(2\times 2\) block \(H\) only

Lemma 2 already supplies the lower comparison \(F^{\mathrm{win},\downarrow}(\omega)=1-84/(\omega T)\) for \([H^{-1}]_{\omega\omega}\). For a matching upper comparison **of that same \(2\times 2\) block**, reverse the Abel extremes: \(a\ge a_0(1-\varepsilon_a)\), \(c\ge c_0(1-\varepsilon_c)\), \(\lvert b\rvert\le b_0(1+\varepsilon_b)\). With \(\rho:=b_0^2/\det_0\le 3\),

\[
\frac{\det}{\det_0}
\ge(1+\rho)(1-\varepsilon_a-\varepsilon_c)-\rho(1+2\varepsilon_b+\varepsilon_b^2)
=1-(1+\rho)(\varepsilon_a+\varepsilon_c)-2\rho\varepsilon_b-\rho\varepsilon_b^2
\ge 1-4(\varepsilon_a+\varepsilon_c)-6\varepsilon_b-3\varepsilon_b^2.
\]

Substitute \(\varepsilon_a=3\pi/\tau\), \(\varepsilon_b=2\pi/\tau\), \(\varepsilon_c=\pi/(2\tau)\): \(4(\varepsilon_a+\varepsilon_c)=14\pi/\tau\), \(6\varepsilon_b=12\pi/\tau\), \(3\varepsilon_b^2=12\pi^2/\tau^2\), hence \(\det/\det_0\ge 1-26\pi/\tau-12\pi^2/\tau^2\). At \(\tau\ge 218.22\) this denominator is at least \(1-0.37431-0.00249=0.62320>0\). Combined with \(c\le c_0(1+\varepsilon_c)\) and \([H_0^{-1}]_{\omega\omega}=(24/(n T^2))\cdot n^2/(n^2-1)\),

\[
[H^{-1}]_{\omega\omega}
\le F^{\mathrm{win},\uparrow}(\omega)\cdot\frac{24}{n T^2},
\qquad
F^{\mathrm{win},\uparrow}(\omega)
=\frac{n^2}{n^2-1}\cdot\frac{1+\pi/(2\tau)}{1-26\pi/\tau-12\pi^2/\tau^2}.
\tag{5.5}
\]

**Scope of (5.5).** This is an upper bound on the inverse of the normalised \((\omega,\phi)\) principal block \(H\). It is **not** an upper bound on \([(G_j^{\mathrm{disc}})^{-1}]_{\omega\omega}\) for the free-amplitude \(3\times 3\) Gram. Partitioning \(G_j=\bigl(\begin{smallmatrix}q_0&r^{\mathsf T}\\ r&H_{\mathrm{un}}\end{smallmatrix}\bigr)\) gives \((H_{\mathrm{un}}-rr^{\mathsf T}/q_0)^{-1}\succeq H_{\mathrm{un}}^{-1}\): the Schur direction increases the inverse, so an upper bound for \(H^{-1}\) does not upper-bound \(G_j^{-1}\). Equation (5.5) is **not** used on the right side of (A\(\infty\).1).

Arithmetic at \(\tau_{\min}=218.22\), \(n=n_{\star}=1124\): \(n^2=1\,263\,376\), \(n^2/(n^2-1)=1\,263\,376/1\,263\,375=1.0000007915\); \(26\pi/\tau=81.681409/218.22=0.374308\); \(12\pi^2/\tau^2=118.43525/47\,619.968=0.002487\); \(1-26\pi/\tau-12\pi^2/\tau^2=0.623205\); \(1+\pi/(2\tau)=1.007198\); \(F^{\mathrm{win},\uparrow}(\tau_{\min})=1.0000007915\times 1.007198/0.623205=1.61616\). Round **UP**: \(F^{\mathrm{win},\uparrow}\le\mathbf{1.617}\) uniformly for \(n\ge n_{\star}\) and \(\tau\ge\tau_{\min}\), as a \(2\times 2\) bound.

At the operating tone \(j=10\), \(\tau=\gamma_{10}T=856.941537\): \(26\pi/\tau=0.095317\); \(12\pi^2/\tau^2=118.43525/734\,348.83=0.000161\); \(1-26\pi/\tau-12\pi^2/\tau^2=0.904522\); \(1+\pi/(2\tau)=1.001833\); \(F^{\mathrm{win},\uparrow}_{10}=1.0000007915\times 1.001833/0.904522=1.10758\). Round **UP**: \(\mathbf{1.1076}\), as a \(2\times 2\) bound. (The sharper Abel step \(2(n-1)^2\) is what permits this rounding; the coarser \(2n^2\) bound would have required UP \(1.1077\).)

### 7bis.5 The comparison envelope, via Loewner inversion of (A\(\infty\).0)

**Loewner inversion (the named missing step).** If \(c_1>0\), \(c_2>0\), and \(c_1 G\preceq I\preceq c_2 G\) in the Loewner order on a common positive-definite space, then
\[
c_2^{-1}G^{-1}\;\preceq\; I^{-1}\;\preceq\; c_1^{-1}G^{-1}.
\]
*Proof.* \(0\prec A\preceq B\) implies \(0\prec B^{-1}\preceq A^{-1}\). Apply this to \(c_1 G\preceq I\) and to \(I\preceq c_2 G\). \(\square\)

Principal submatrices inherit the Loewner order: if \(A\preceq B\) then every principal submatrix satisfies the same inequality, because \(x^{\mathsf T}A_{jj}x=(\iota x)^{\mathsf T}A(\iota x)\) for the coordinate embedding \(\iota\). Thus (A\(\infty\).0) restricts to the free-amplitude \(3\times 3\) of tone \(j\):
\[
\frac{\Delta}{S_s+S_{\max}}\,G_j^{\mathrm{disc}}
\;\preceq\;
I_{jj}^{(n)}
\;\preceq\;
\frac{\Delta}{S_s}\,G_j^{\mathrm{disc}}.
\]
Invert and take the \((\gamma_j,\gamma_j)\) entry (a quadratic form, hence monotone for Loewner):
\[
\frac{S_s}{\Delta}\bigl[(G_j^{\mathrm{disc}})^{-1}\bigr]_{\gamma_j\gamma_j}
\;\le\;
\bigl[(I_{jj}^{(n)})^{-1}\bigr]_{\gamma_j\gamma_j}
\;\le\;
\frac{S_s+S_{\max}}{\Delta}\bigl[(G_j^{\mathrm{disc}})^{-1}\bigr]_{\gamma_j\gamma_j}.
\]
Multiply by \(T^3\) and use \(\Delta=T/n\), so \(T^3/\Delta=n T^2\):
\[
n T^2 S_s\bigl[(G_j^{\mathrm{disc}})^{-1}\bigr]_{\gamma_j\gamma_j}
\;\le\;
T^3\bigl[(I_{jj}^{(n)})^{-1}\bigr]_{\gamma_j\gamma_j}
\;\le\;
n T^2(S_s+S_{\max})\bigl[(G_j^{\mathrm{disc}})^{-1}\bigr]_{\gamma_j\gamma_j}.
\]
This sandwich uses the inverse of the **full free-amplitude \(3\times 3\)** Gram. It does not pass through \(H^{-1}\) or (5.5).

For the **lower** side, the Schur comparison of Lemma 2 applies in the valid direction: adding the amplitude row increases the \(\omega\omega\) inverse, so
\[
\bigl[(G_j^{\mathrm{disc}})^{-1}\bigr]_{\gamma_j\gamma_j}
\ge
A_j^{-2}[H^{-1}]_{\omega\omega}
\ge
F_j^{\mathrm{win},\downarrow}\cdot\frac{24}{A_j^2 n T^2}.
\]
Multiplying by \(n T^2 S_s\) gives the closed form \(C_j^{\downarrow}F_j^{\mathrm{win},\downarrow}\) with \(C_j^{\downarrow}=24 S_s/A_j^2\).

For the **upper** side, that Schur direction is the opposite of what a promotion of (5.5) would need. The proved upper bound is therefore left in terms of \([(G_j^{\mathrm{disc}})^{-1}]_{\gamma_j\gamma_j}\). A closed-form Abel estimate
\[
\bigl[(G_j^{\mathrm{disc}})^{-1}\bigr]_{\gamma_j\gamma_j}
\le
F_j^{\mathrm{win},\uparrow}\cdot\frac{24}{A_j^2 n T^2}
\]
is **OWED-Ainfinity-validity**.

> **Proposition A\(\infty\) (comparison envelope of the exact finite-\(n\) Fisher; not Theorem A; no limiting equality).**
> Assume the hypotheses of Theorem A and \(n\ge n_{\star}\). The exact Fisher \(I^{(n)}\) of (4.0n) satisfies the Loewner sandwich (A\(\infty\).0). Let \(I_{jj}^{(n)}\) be the principal \(3\times 3\) of tone \(j\), and write
> \[
> C_{j}^{\downarrow}\;:=\;\frac{24\,S_s}{A_j^2}.
> \]
> Then
> \[
> C_{j}^{\downarrow}\,F_j^{\mathrm{win},\downarrow}
> \;\le\;
> T^3\bigl[(I_{jj}^{(n)})^{-1}\bigr]_{\gamma_j\gamma_j}
> \;\le\;
> (S_s+S_{\max})\,n T^2\,\bigl[(G_j^{\mathrm{disc}})^{-1}\bigr]_{\gamma_j\gamma_j},
> \tag{A\(\infty\).1}
> \]
> with \(F_j^{\mathrm{win},\downarrow}=1-84/(\gamma_j T)\). The lower envelope constant \(C_j^{\downarrow}\) and the upper prefactor \(S_s+S_{\max}\) are independent of \(n\) at fixed \(S_s\). Equivalently: \([(I_{jj}^{(n)})^{-1}]_{\gamma_j\gamma_j}\) has a \(T^{-3}\) envelope in the sense that \(T^3\) times this entry is bounded below by a multiple of \(S_s\) and above by a multiple of \(S_s+S_{\max}\) times the dimensionless discrete-Gram factor \(n T^2[(G_j^{\mathrm{disc}})^{-1}]_{\gamma_j\gamma_j}\). Do not say that \(T^3 I^{-1}\) scales as \(T^3\). No limiting equality is claimed, and the locally-white coloured coefficient \(24(S_{\eta}(\gamma_j)+S_s)/A_j^2\) is **not** identified with either side (that identification would require an inverse-Toeplitz/Szegő step, which is OWED-NOT-USED). The named slacks of §7bis.2 are not multiplied into (A\(\infty\).1). The v6 closed-form right side \(C_j^{\uparrow}F_j^{\mathrm{win},\uparrow}\) with \(C_j^{\uparrow}=24(S_s+S_{\max})/A_j^2\) and \(F^{\mathrm{win},\uparrow}\) from (5.5) is **not claimed** (**OWED-Ainfinity-validity**).
>
> By (6.1), the efficient inverse satisfies the **lower** bound of (A\(\infty\).1). A matching upper bound on \([(I^{(n)})^{-1}]_{\gamma_j\gamma_j}\) is not claimed (**OWED-\(C_{\diamond}\)**).

*Proof.* The two-sided comparison of \(I_{jj}^{(n)}\) against \(G_j^{\mathrm{disc}}\) is the principal-submatrix restriction of (A\(\infty\).0), inverted by the Loewner lemma above, and evaluated at the \((\gamma_j,\gamma_j)\) entry. The left closed form is Lemma 2 plus the valid Schur comparison that drops the amplitude row. \(\square\)

There is no display (A\(\infty\).2). The v5 limit equality is deleted. The v6 two-sided closed form that used (5.5) on the \(3\times 3\) inverse is deleted.

**Comparison skeleton (not a corollary of a proved limit).** The unnamed-factor locally-white coefficient at \(S_s=0\) has leading \(T^{-3/2}\) factor \(\sqrt{6}\). That skeleton is not a finite-\(T\) floor and is not a consequence of a proved \(n\to\infty\) equality.

---

## 8. Theorem B — Bayes van Trees, ordinates \(j\in\{2,\dots,d\}\), tied amplitude, admissible prior

This is a different theorem from Theorem A. It bounds a **Bayes-average** MSE. Unbiasedness is not assumed, and is not dropped from Theorem A.

### 8.1 van Trees inequality

Let \(\pi\) be a density on an interval, absolutely continuous, vanishing at the endpoints, with finite prior information \(I(\pi)=\int(\pi')^2/\pi\). For a regular parametric family and an arbitrary measurable estimator \(\widehat\theta\),

\[
\mathbb{E}\bigl[(\widehat\theta-\theta)^2\bigr]
\;\ge\;
\frac1{\mathbb{E}_{\pi}[I(\theta)]+I(\pi)},
\tag{8.1}
\]

the left side over the joint law \(\pi(d\theta)\,P_{\theta}\). *Citation.* Van Trees (1968), Part I, §2.4; Gill–Levit, *Bernoulli* 1 (1995), Theorem 1. A uniform prior is illegal.

The multivariate form (Gill–Levit, Theorem 1): for \(\psi(\theta)=\gamma_j\) a coordinate of a Euclidean parameter with a density vanishing on the boundary of its support,

\[
\mathbb{E}\bigl[(\widehat{\gamma}_j-\gamma_j)^2\bigr]
\;\ge\;
\bigl[(\overline{J}+J^{\pi})^{-1}\bigr]_{\gamma_j\gamma_j}
\;\ge\;
\frac1{\overline{J}_{\gamma_j\gamma_j}+J^{\pi}_{\gamma_j\gamma_j}},
\tag{8.2}
\]

the second step because \(M\succ 0\) implies \([M^{-1}]_{jj}\ge 1/M_{jj}\). For a product prior, \(J^{\pi}_{\gamma_j\gamma_j}=I(\pi_{\gamma_j})\).

### 8.2 Prior (P1″): ordinates only, amplitudes tied, (M5)-admissible support

On \(u\in[-1,1]\) let \(\lambda(u)=\cos^2(\pi u/2)\). Then \(\int_{-1}^1\lambda=1\), \(\lambda(\pm 1)=0\), and \(I(\lambda)=\pi^2\). Scale: for a **declared** centre \(\mu\in\mathbb{R}\) and half-width \(\rho>0\),

\[
\pi_{\gamma}(\gamma)
=\rho^{-1}\lambda\bigl((\gamma-\mu)/\rho\bigr)
\quad\text{on }[\mu-\rho,\mu+\rho].
\]

Then \(I(\pi_{\gamma})=\pi^2/\rho^2\).

**(M5)-admissible half-widths.** Let \(\mu_j\) be the external centres (published Odlyzko ordinates). Define the gap margin at \(\mu_j\) by sharing each adjacent slack,
\[
m_j^{\mathrm{gap}}
:=\min\bigl\{\,(\mu_j-\mu_{j-1}-h)/2\text{ if }j>1,\;
(\mu_{j+1}-\mu_j-h)/2\text{ if }j<d\,\bigr\},
\]
and the cut margin at \(\mu_j\) by
\[
m_j^{\mathrm{cut}}:=\Gamma_{\mathrm{op}}-h-\mu_j.
\]
Set
\[
\rho_j
:=\min\bigl(h/2,\; m_j^{\mathrm{gap}},\; m_j^{\mathrm{cut}}\bigr).
\]
Then every independent draw \(\gamma_j\in[\mu_j-\rho_j,\mu_j+\rho_j]\) satisfies \(\min_{k\ne j}\lvert\gamma_j-\gamma_k\rvert\ge h\) and \(\Gamma_{\mathrm{op}}-\gamma_d\ge h\), so \(\mathrm{supp}(\pi)\subset\{\theta:(\mathrm{M5})\}\). Adjacent interiors remain disjoint. (The factor \(1/2\) in \(m_j^{\mathrm{gap}}\) is required for a product prior: independent moves of both endpoints of a gap must share the slack \(g-h\).)

**Operating-point positivity (the six tabulated tones).** With \(h=1.4597878593777017\), \(h/2=0.7298939296888508\), \(\Gamma_{\mathrm{op}}-h-\gamma_{10}=2.94999634\times 10^{-9}\), and stored ordinates of §11.1 together with \(\gamma_6=37.586178158825671\), \(\gamma_7=40.918719012147495\), \(\gamma_8=43.327073280914999\), \(\gamma_9=48.005150881167159\):

| \(j\) | \(h/2\) | \(m_j^{\mathrm{gap}}\) | \(m_j^{\mathrm{cut}}\) | \(\rho_j\) | \(>0\) |
|---:|---:|---:|---:|---:|:---:|
| 1 | \(0.7298939296888508\) | \(2.713763318829580\) | \(35.6391073388876\) | \(0.7298939296888508\) | yes |
| 2 | \(0.7298939296888508\) | \(1.264515040998216\) | \(28.7517928418507\) | \(0.7298939296888508\) | yes |
| 3 | \(0.7298939296888508\) | \(1.264515040998216\) | \(24.7629749004766\) | \(0.7298939296888508\) | yes |
| 4 | \(0.7298939296888508\) | \(0.525198801250987\) | \(19.3489563547628\) | \(0.525198801250987\) | yes |
| 5 | \(0.7298939296888508\) | \(0.525198801250987\) | \(16.8387708928831\) | \(0.525198801250987\) | yes |
| 10 | \(0.7298939296888508\) | \(0.154446868563721\) | \(2.94999634\times 10^{-9}\) | \(2.94999634\times 10^{-9}\) | yes |

All six \(\rho_j\) are positive. (For \(j=1,2,3\) the cap is \(h/2\); for \(j=4,5\) the \(4\)–\(5\) gap binds; for \(j=10\) the cut excess binds.) Correspondingly \(I(\pi_j)=\pi^2/\rho_j^2\):

- \(j=1,2,3\): \(\rho_j=h/2\), so \(I(\pi_j)=4\pi^2/h^2=T^2/K^2=18.5259395173997\).
- \(j=4,5\): \(\rho_j=0.525198801250987\), \(\rho_j^2=0.27583378087\), \(\pi^2/\rho_j^2=35.78099\). Round **UP** as a denominator: \(I(\pi_{4,5})\le\mathbf{35.781}\).
- \(j=10\): \(\rho_{10}=2.94999634\times 10^{-9}\), \(\rho_{10}^2=8.70247841\times 10^{-18}\), \(\pi^2/\rho_{10}^2=1.134114\times 10^{18}\). Round **UP** as a denominator: \(I(\pi_{10})\le\mathbf{1.13412\times 10^{18}}\).

**External centres (Defect 4 repair, kept).** The centres \(\mu_1,\dots,\mu_d\) are parameters of \(\pi\), specified independently of the unknown true \(\theta\). For numerical evaluation the centres are the published Odlyzko ordinates of §11.1.

**Amplitudes (N2 repair).** There is **no** independent prior on \(A_j\). At every \(\gamma_j\) in the support, set

\[
A_j(\gamma_j)\;:=\;2\,a(\gamma_j).
\]

This is (M-amp) pathwise. For \(j\ge 2\), \(\mu_j-\rho_j>\gamma_1^{\mathrm{anchor}}\) at the operating point (e.g. \(\mu_2-\rho_2=20.292145709>14.134725142\)), so (2.3) holds \(\pi_j\)-almost surely as a comparison identity. For \(j=1\), \(\mu_1-\rho_1=13.404831212<\gamma_1^{\mathrm{anchor}}\): the comparison (2.3) fails on a positive-mass set, and Theorem B **excludes** \(j=1\) rather than repairing that branch. The v4 items **OWED-amp-avg** and the independent raised-cosine prior on \(A_j\) remain vacated: there is no independent amplitude coordinate under \(\pi\).

**Hypothesis (H-circle) (V5-N4; load-bearing for Theorem B).** The phase coordinates \((\phi_1,\dots,\phi_d)\) are equipped with a product prior such that the multivariate van Trees inequality (8.2) of Gill–Levit (1995), Theorem 1, applies to the tied parameter
\[
\theta^{\mathrm{tied}}=(\gamma_1,\dots,\gamma_d,\,\phi_1,\dots,\phi_d)\in\mathbb{R}^{2d}.
\]
Concretely, either (i) each \(\phi_j\) carries a cuff density on a fundamental domain \([0,2\pi]\), vanishing at the endpoints, with finite prior information \(I(\pi_{\phi_j})\), or (ii) a manifold form of van Trees holds for the uniform prior on \((\mathbb{R}/2\pi\mathbb{Z})^d\). The Euclidean Gill–Levit statement does not literally cover the torus. Adding phase-prior information makes the sharper full-matrix inverse smaller; it does not enlarge the scalar weakening \(1/M_{\gamma\gamma}\), which is simply unaffected. This hypothesis is **part of Theorem B**; it is not an optional ledger refinement. The symbol \(\mathbb{E}_{\pi}[I_{\mathrm{tied}}]\) means the joint \((\pi_{\gamma}\otimes\pi_{\phi})\) expectation.

### 8.3 Tied score and scalar Fisher \(I_{\mathrm{tied}}\) (V5-N2, kept)

The submodel of Theorem B has no free amplitude coordinate. The mean as a function of \(\gamma_j\) is \(m(t;\,\gamma_j,A_j(\gamma_j),\phi_j)\). The total derivative is the **tied score**

\[
\frac{dm}{d\gamma_j}
=\partial_{\gamma_j}m+A_j'(\gamma_j)\,\partial_{A_j}m.
\tag{8.3}
\]

This is a one-dimensional calculation (other coordinates, including phases, held fixed).

> **Lemma 7 (amplitude Jacobian).** Let \(a(\omega)=\bigl((\tfrac14+\omega^2)(\tfrac94+\omega^2)\bigr)^{-1/2}\) and \(A(\omega)=2a(\omega)\). Write \(u(\omega)=(\tfrac14+\omega^2)(\tfrac94+\omega^2)=\omega^4+\tfrac52\omega^2+\tfrac9{16}\). Then \(u'(\omega)=4\omega(\omega^2+\tfrac54)\), and
> \[
> a'(\omega)=-\tfrac12 u(\omega)^{-3/2}u'(\omega)=-2\omega\bigl(\omega^2+\tfrac54\bigr)\,u(\omega)^{-3/2},
> \]
> hence
> \[
> A'(\omega)=2a'(\omega)=-4\omega\bigl(\omega^2+\tfrac54\bigr)\,u(\omega)^{-3/2},
> \qquad
> \frac{A'(\omega)}{A(\omega)}=\frac{a'(\omega)}{a(\omega)}=-\frac{2\omega\bigl(\omega^2+\tfrac54\bigr)}{(\omega^2+\tfrac14)(\omega^2+\tfrac94)}.
> \]
> Moreover \(\lvert A'/A\rvert<2/\omega\) for every \(\omega>0\), since \(\omega^2(\omega^2+\tfrac54)=\omega^4+\tfrac54\omega^2<(\omega^2+\tfrac14)(\omega^2+\tfrac94)=\omega^4+\tfrac52\omega^2+\tfrac9{16}\).

The **scalar tied Fisher** (other coordinates held fixed) is

\[
I_{\mathrm{tied},j}(\theta)
:=\Bigl(\frac{dm}{d\gamma_j}\Bigr)^{\mathsf T}\Sigma^{-1}\Bigl(\frac{dm}{d\gamma_j}\Bigr)
=I_{\gamma_j\gamma_j}^{\mathrm{free}}+2A_j'(\gamma_j)\,I_{\gamma_j A_j}^{\mathrm{free}}+\bigl(A_j'(\gamma_j)\bigr)^2 I_{A_j A_j}^{\mathrm{free}},
\tag{8.4}
\]

where \(I^{\mathrm{free}}\) denotes the \(3d\)-coordinate Fisher (4.0n) of the free-amplitude parameterisation. This is **not** the efficient information of the \(3d\) model in which \(A_j\) is a free nuisance: that efficient information projects out \(\partial_{A_j}m\), which deletes the \(A'\,\partial_A m\) direction of the tied score.

**White-envelope upper bound.** Since \(\Sigma^{-1}\preceq\sigma_s^{-2}I_n\),

\[
I_{\mathrm{tied},j}
\le\sigma_s^{-2}\bigl\|v_{\gamma_j}+A_j' v_{A_j}\bigr\|^2
=\sigma_s^{-2}\bigl(\|v_{\gamma_j}\|^2+2A_j'\,v_{\gamma_j}\cdot v_{A_j}+(A_j')^2\|v_{A_j}\|^2\bigr),
\]

with \(v_{\gamma_j,k}=-A_j t_k\sin(\gamma_j t_k+\phi_j)\) and \(v_{A_j,k}=\cos(\gamma_j t_k+\phi_j)\). Then \(\|v_{A_j}\|^2\le n\) and \(\|v_{\gamma_j}\|^2\le A_j^2\sum t_k^2=A_j^2 T^2(n-1)(2n-1)/(6n)\). For the cross term, \(\lvert v_{\gamma_j}\cdot v_{A_j}\rvert=(A_j/2)\lvert\sum t_k\sin(2\psi_k)\rvert\). Abel as in Lemma 2: with \(\theta=2\gamma_j\Delta\), \(\lvert\sum_{k=0}^{n-1}k e^{ik\theta}\rvert\le 2(n-1)/\lvert\sin(\theta/2)\rvert=2(n-1)/\lvert\sin(\gamma_j\Delta)\rvert\). Under (M-n) one has \(\gamma_j\le\Gamma=\Omega/2\), so \(\gamma_j\Delta\le\pi/4\le\pi/2\) and \(\lvert\sin(\gamma_j\Delta)\rvert\ge 2\gamma_j\Delta/\pi=2\gamma_j T/(\pi n)\). Thus \(\lvert\sum k\sin\rvert\le\pi n(n-1)/(\gamma_j T)\) and \(\lvert\sum t_k\sin(2\psi)\rvert=\Delta\lvert\sum k\sin\rvert\le\pi(n-1)/\gamma_j\). Hence \(\lvert 2A_j'\,v_{\gamma_j}\cdot v_{A_j}\rvert\le\lvert A_j'\rvert A_j\pi(n-1)/\gamma_j\), and

\[
I_{\mathrm{tied},j}
\le\sigma_s^{-2}\frac{A_j^2 T^2(n-1)(2n-1)}{6n}\,(1+\delta_j^{\mathrm{tied}}),
\tag{8.5}
\]

with

\[
\delta_j^{\mathrm{tied}}
=\frac{6n\,\lvert A_j'/A_j\rvert\,\pi}{\gamma_j T^2(2n-1)}+\frac{6n^2(A_j'/A_j)^2}{T^2(n-1)(2n-1)}
<\frac{12\pi n}{\gamma_j^2 T^2(2n-1)}+\frac{24 n^2}{\gamma_j^2 T^2(n-1)(2n-1)},
\]

using \(\lvert A'/A\rvert<2/\gamma_j\). For \(n\ge n_{\star}=1124\), \(n/(2n-1)=1124/2247=0.5002225\le 0.5003\) (UP) and \(n^2/((n-1)(2n-1))=1\,263\,376/2\,523\,381=0.500668\le 0.5007\) (UP), so

\[
\delta_j^{\mathrm{tied}}
<\frac{12\pi\cdot 0.5003+24\cdot 0.5007}{\gamma_j^2 T^2}.
\]

Arithmetic: \(12\pi=37.699111843\), \(12\pi\times 0.5003=18.860866\) (UP \(18.861\)); \(24\times 0.5007=12.0168\) (UP \(12.017\)); sum \(30.878\). Hence \(\delta_j^{\mathrm{tied}}<30.878/(\gamma_j^2 T^2)\).

The extras are \(O\bigl((a'/a)^2/T^2\bigr)\)-relative to the one-dimensional white leading term \(A_j^2 n T^2/(6\sigma_s^2)\): the quadratic \((A')^2 I_{AA}\) contributes \(O((a'/a)^2/T^2)\), and the Abel cross term contributes \(O\bigl(\lvert a'/a\rvert/(\gamma T^2)\bigr)=O((a'/a)^2/T^2)\) because \(\lvert a'/a\rvert\asymp 2/\gamma\).

**Operating-point arithmetic, \(j=10\).** \(\gamma_{10}=49.773832477672302\), \(\gamma_{10}^2=2477.4343995\), \(T^2=296.415032\), \(\gamma_{10}^2 T^2=2477.4343995\times 296.415032=734\,348.79\). Then \(30.878/734\,348.79=4.205\times 10^{-5}\). Round **UP**: \(\delta_{10}^{\mathrm{tied}}\le\mathbf{4.21\times 10^{-5}}\).

Exact Jacobian at \(\gamma_{10}\): \(u=(\gamma_{10}^2+\tfrac14)(\gamma_{10}^2+\tfrac94)=2477.6843995\times 2479.6843995=6\,143\,875.355\), \(2\gamma_{10}(\gamma_{10}^2+\tfrac54)=99.547664955\times 2478.6843995=246\,747.244\), \(\lvert a'/a\rvert=246\,747.244/6\,143\,875.355=0.0401615\), versus \(2/\gamma_{10}=0.0401814\). Then \((a'/a)^2=0.00161295\), \((a'/a)^2/T^2=0.00161295/296.415032=\mathbf{5.4415\times 10^{-6}}\), and \(6(a'/a)^2/T^2=3.2649\times 10^{-5}\).

If a tighter identification of \(\mathbb{E}_{\pi}[I_{\mathrm{tied}}]\) with a \(\sigma_s\)-free coloured formula is wanted, that step is **OWED-B-tied-eval**; it is not claimed.

### 8.4 Averaged Fisher, support-uniform comparison factors

The locally-white leading comparison \(I^{\mathrm{skel}}_{\mathrm{leading}}(\gamma)=T^3/\bigl(6\log(\gamma/2\pi)\bigr)\) is strictly decreasing in \(\gamma\) for \(\gamma>2\pi\). On \([\mu_j-\rho_j,\mu_j+\rho_j]\),

\[
I^{\mathrm{skel},\uparrow}_j
:=\frac{T^3}{6\log\bigl((\mu_j-\rho_j)/2\pi\bigr)},
\]

provided \(\mu_j-\rho_j>2\pi\). This is **not** an upper bound on \(\mathbb{E}_{\pi}[I_{\mathrm{tied},j}]\) (the white envelope (8.5) is). It is a named comparison skeleton.

The factors \(F^{\mathrm{flat}}\), \(F^{\mathrm{win}}\), \(F^{\mathrm{leak}}\) vary over the prior support. The support has width \(2\rho_j=O(1/T)\) (and \(O(10^{-9})\) at \(j=10\)). A uniform lower bound is the value at the leftmost frequency that appears.

- \(F^{\mathrm{flat}}(\gamma)\) decreases as \(\gamma\) decreases, and the Lemma-1 band of a point \(\gamma\) extends a further \(h\) to the left. The leftmost frequency is \(\mu_j-\rho_j-h\). For \(j\ge 2\) this point lies on the log branch. By Lemma 4(a), \(\inf_{\mathrm{supp}}F_j^{\mathrm{flat}}=\exp\bigl(2h\,D(\mu_j-\rho_j-h)\bigr)\). This is a single endpoint evaluation.
- \(F^{\mathrm{win}}(\gamma)=1-C_{\mathrm{win}}/(\gamma T)\) is increasing in \(\gamma\). The infimum on the prior support is \(1-C_{\mathrm{win}}/((\mu_j-\rho_j)T)\), again an endpoint evaluation.
- \(F^{\mathrm{leak}}\): without a closed form for \(\kappa_j(\gamma)\), a uniform bound is an additional hypothesis **(B1)\(_{j,\pi}\)**: a single \(\kappa_j^{\pi}\) dominating \(\kappa_j\) on the prior support. Numerically this factor is **missing**.

These are support-uniform bounds on the named *comparison* factors. They are not factors of \(I_{\mathrm{tied}}\).

> **Theorem B (Bayes van Trees, ordinate-only prior, tied amplitude, discrete Gaussian surrogate, fixed \(d\), \(j\in\{2,\dots,d\}\); conditional on (H-circle)).**
> Assume the hypotheses of Theorem A except unbiasedness. Let \(\pi\) be the product prior (P1″) on \((\gamma_1,\dots,\gamma_d)\) with **externally specified** centres \(\mu_1,\dots,\mu_d\), admissible half-widths \(\rho_j\) as above, and \(A_j=2a(\gamma_j)\). Assume **(H-circle)** of §8.2. Let \(j\in\{2,\dots,d\}\) and let \(\widehat{\gamma}_j\) be any measurable function of \(Y\). Then
>
> \[
> \mathbb{E}_{\pi_{\gamma}\otimes\pi_{\phi}}\bigl[(\widehat{\gamma}_j-\gamma_j)^2\bigr]
> \;\ge\;
> \frac{1}{\mathbb{E}_{\pi_{\gamma}\otimes\pi_{\phi}}\bigl[I_{\mathrm{tied},j}(\theta)\bigr]+\pi^2/\rho_j^2},
> \tag{B.0}
> \]
>
> where \(I_{\mathrm{tied},j}\) is the scalar tied Fisher (8.4) of the score (8.3). Under branch (i) of (H-circle) the inequality is Euclidean (8.2) applied to \(\theta^{\mathrm{tied}}\); under branch (ii) it is the assumed manifold analogue. In either branch the scalar weakening \([M^{-1}]_{jj}\ge 1/M_{jj}\) is used. The index \(j=1\) is **not** in the quantifier. Moreover the white-envelope bound (8.5) holds, with \(\delta_j^{\mathrm{tied}}=O\bigl((a'/a)^2/T^2\bigr)\) as displayed. The certified comparison factors admit the support-uniform lower bounds
>
> \[
> \inf_{\mathrm{supp}\,\pi_j}F_j^{\mathrm{flat}}
> =e^{2h\,D(\mu_j-\rho_j-h)},
> \qquad
> \inf_{\mathrm{supp}\,\pi_j}F_j^{\mathrm{win}}
> =1-\frac{84}{(\mu_j-\rho_j)T}.
> \tag{B.2}
> \]
>
> The left side of (B.0) is Bayes **MSE** (including bias\(^2\)). The bound is a statement about \(\pi\), not a uniform frequentist bound on \(\mathrm{supp}(\pi)\) (**OWED-B-uniform**). No numerical product floor is claimed for Theorem B in §12: \(F^{\mathrm{leak}}\) is missing; the locally-white skeleton \(I^{\mathrm{skel},\uparrow}\) is **not** \(\mathbb{E}_{\pi}[I_{\mathrm{tied}}]\); (H-circle) is an explicit hypothesis; and at \(j=10\) the prior information \(\pi^2/\rho_{10}^2\) dominates.
>
> **Arithmetic interpretation:** the same Prop. R disclosure as in Theorem A.

A minimax corollary is not stated. Ziv–Zakai is **OWED-ZZ**.

---

## 9. Regularity of \(\mathcal{G}_{N2}^{n}\)

Let \(P_{\theta}\) be the law of \(Y\in\mathbb{R}^n\) under \(\theta\). This is Gaussian with **fixed** covariance \(\Sigma\succ 0\) and mean \(m(\theta)\in\mathbb{R}^n\).

**(R1) Mutual absolute continuity.** All nondegenerate Gaussians on \(\mathbb{R}^n\) with the same covariance are equivalent. Cameron–Martin is \(\mathbb{R}^n\) itself. **Holds** because \(\sigma_s^2>0\). The v4 continuous band-limited obstruction (pure tones not in the RKHS of a compactly supported spectrum) does not arise. The unrestricted continuous record is not an observation of this experiment.

**(R2) Differentiable log-likelihood.** \(\log dP_{\theta}/dP_0=\langle Y,m(\theta)\rangle_{\Sigma}-\tfrac12\|m(\theta)\|_{\Sigma}^2\). The map \(\theta\mapsto m(\theta)\) is real-analytic into \(\mathbb{R}^n\). **Holds.**

**(R3) Differentiation under the integral.** The score \(\partial_{\alpha}\log dP_{\theta}/dP_0=\langle Y-m(\theta),\,\partial_{\alpha}m(\theta)\rangle_{\Sigma}\) is Gaussian, mean zero, finite variance. **Holds.**

**(R4) Fisher information finite and nonsingular.** Finiteness is \(\|\partial_{\alpha}m\|_{\Sigma}^2<\infty\), automatic in finite dimension. Nonsingularity of the \(3d\) Gram is (M5) plus \(A_j>0\). If (M5) fails, T1 is silent. Theorem B’s prior is supported inside (M5) by construction of \(\rho_j\).

**(R5) Unbiasedness.** An assumption on the estimator class in Theorem A. Periodogram estimators (T2) are biased at finite \(T\); they are not in the quantifier of Theorem A. They are in the quantifier of Theorem B.

**(R6) is not a regularity condition of \(\mathcal{G}_{N2}^{n}\).** The noise *is* Gaussian by stipulation. Lindeberg / Berry–Esseen quantities \(\Lambda(\Gamma)\) and \(d_K\) are diagnostics of a *different* experiment (the phase sum). They are computed in §11 and interpreted in §14. They do not enter Theorems A or B.

---

## 10. Exact Fisher information of the discrete experiment

\[
I_{\alpha\beta}(\theta)
=(\partial_{\alpha}m(\theta))^{\mathsf T}\Sigma^{-1}(\partial_{\beta}m(\theta)),
\qquad
\Sigma=\Sigma_{\eta}+\sigma_s^2 I_n.
\tag{4.0n}
\]

This is the exact Fisher information of \(\mathcal{G}_{N2}^{n}\). It replaces v4’s continuous band-limited integral (4.0), which is not the Fisher of a singular continuous experiment and is not used here.

**(a)** Every target is interior to the pass band with margin \(\Omega-\gamma_j>\Gamma\), and Lemma-4 neighbourhoods of \(j\ge 2\) are interior under (M5): \(\gamma_j+h\le\Gamma<\Omega\). The \(j=1\) neighbourhood meets the spectral-floor kink; Theorem A does not use \(D\) on that neighbourhood.

**(b)** The value \(S_{\eta}(\gamma_j)\) is (2.2), by (M4), not by Proposition 4.4\(^\prime\).

**(c)** The constant \(24\) in (5.1) is a discrete white-noise leading term. A coloured, band-limited numerical check at \(\Gamma=51.234\), \(\Omega=2\Gamma\), tone \(\gamma_d\), window (W′), from the superseded draft’s scripts, gave \([I^{-1}]_{\omega\omega}\) equal to \(0.99392\) of \(24\,S_{\eta}(\gamma_d)/(A^2 T^3)\). That number is a **computation**, not a theorem factor, and it belongs to the continuous formal Gram, not to (4.0n). The conversion of a variance ratio \(0.993916700836\) to an RMSE uses the square root: \(\sqrt{0.993916700836}=0.99695371\) (minor 2).

---

## 11. Operating point \(\Gamma_{\mathrm{op}}=51.23362034\)

### 11.1 Inputs

\[
\begin{aligned}
T&=\log(3\cdot 10^7)=17.2167079396264295,\\
K&=4,\\
\gamma_{10}&=49.773832477672302,\\
L_{10}&=\log(\gamma_{10}/2\pi)=2.06961232726741,\\
\gamma_1^{\mathrm{anchor}}&=14.134725141734693,\qquad L_1=\log(\gamma_1^{\mathrm{anchor}}/2\pi)=0.810757479321445,\\
\vartheta_{\min}&=L_1.
\end{aligned}
\]

Arithmetic for \(T\): \(\log(3\cdot 10^7)=\log 3+7\log 10\), with \(\log 10=2.302585092994045684\), \(7\log 10=16.11809565095831979\), \(\log 3=1.098612288668109691\), sum \(17.21670793962642948\).

Arithmetic for \(L_{10}\): the truncated-ordinate value \(\log(49.773832/2\pi)=2.06961231767041\) (cold-referee independent) plus \(\log(1+4.77672302\times 10^{-7}/49.773832)=\log(1+9.5970\times 10^{-9})=9.5970\times 10^{-9}\) gives \(2.06961232726741\).

Odlyzko ordinates used as **external prior centres** and as labels:

| \(j\) | \(\gamma_j\) | \(\log(\gamma_j/2\pi)\) | \(\lvert M_W(\tfrac12+i\gamma_j)\rvert\) |
|---:|---:|---:|---:|
| 1 | 14.134725141734693 | 0.810757479 | \(4.97414\times 10^{-3}\) |
| 2 | 21.022039638771555 | 1.207624 | \(2.25643\times 10^{-3}\) |
| 3 | 25.010857580145688 | 1.381505 | \(1.59543\times 10^{-3}\) |
| 4 | 30.424876125859513 | 1.577330 | \(1.07886\times 10^{-3}\) |
| 5 | 32.935061587739189 | 1.656668 | \(9.20840\times 10^{-4}\) |
| 10 | 49.773832477672302 | 2.069612327 | \(4.03441\times 10^{-4}\) |

\(\lvert M_W\rvert=\bigl((\gamma^2+1/4)(\gamma^2+9/4)\bigr)^{-1/2}\). At \(j=10\): \(\gamma^2=2477.4344\), product \(2477.6844\times 2479.6844\), square root \(2478.684\), reciprocal \(4.0344\times 10^{-4}\).

Also \(\gamma_9=48.005150881167159\), \(\gamma_{11}=52.97032147771446\). One has \(\gamma_{10}<\Gamma_{\mathrm{op}}<\gamma_{11}\). Auxiliary ordinates used only to form \(m_j^{\mathrm{gap}}\): \(\gamma_6=37.586178158825671\), \(\gamma_7=40.918719012147495\), \(\gamma_8=43.327073280914999\).

### 11.2 Admissibility arithmetic (N3, Defect 7)

\[
2\pi K=8\pi=25.1327412287183459,
\qquad
h=\frac{8\pi}T=1.4597878593777017.
\]

(Receipt for \(h\): independent v4-referee evaluation of \(8\pi/T\), which does not depend on \(\Gamma\).) Full-ordinate (M5) threshold:

\[
\gamma_{10}+h
=49.773832477672302+1.4597878593777017
=51.2336203370500037.
\]

Eight-decimal **UP**: \(\Gamma_{\mathrm{op}}=51.23362034\). Excess over the threshold: \(2.94999634\times 10^{-9}\). Pass-band: \(\Omega_{\mathrm{op}}=2\Gamma_{\mathrm{op}}=102.46724068\). This excess is exactly \(\rho_{10}\).

Explicit (M5) check with the **full** ordinate:

\[
\Gamma_{\mathrm{op}}-\gamma_{10}
=51.23362034-49.773832477672302
=1.459787862327698,
\]

\[
T(\Gamma_{\mathrm{op}}-\gamma_{10})
=17.2167079396264295\times 1.459787862327698
=25.132741279507,
\]

\[
T(\Gamma_{\mathrm{op}}-\gamma_{10})-8\pi
=5.079\times 10^{-8}
>0.
\]

Thus \(T(\Gamma_{\mathrm{op}}-\gamma_{10})\ge 2\pi K\). The cut \(\Gamma=50\) fails: \(T(50-\gamma_{10})=T\cdot 0.226167522=3.89386<25.13274\). \(\Gamma=50\) is retained in §11.8 only as an out-of-theorem diagnostic.

Among the first ten stored gaps, the smallest is \(\gamma_{10}-\gamma_9=1.768681596505143>h\), so \(d=10\) passes the internal-gap test at this \(T,K\). Gaps versus \(2h=2.919575718755\): \(\gamma_5-\gamma_4=2.510185\), \(\gamma_8-\gamma_7=2.408354\), and \(\gamma_{10}-\gamma_9=1.768682\) all lie in \((h,2h)\). Disjointness of near-tone bands of radius \(h\) fails inside \(d=10\) (**OWED-overlap**). The product prior does **not** use radius \(h/2\) at those tight gaps: \(\rho_4=\rho_5=0.525198801250987\) and \(\rho_{10}=2.94999634\times 10^{-9}\) are the admissible values.

Nyquist integers: \(\Omega T/\pi=561.545926124806\), \(2\Omega T/\pi=1123.09185224961\), hence \(n_{\star}=\lceil 2\Omega T/\pi\rceil=1124\).

### 11.3 \(d\)-dependence of the locally-white comparison-skeleton constants (fixed \(d\); not a proved A\(\infty\) limit)

\[
C_{\mathrm{var}}(d)=6L_d,\qquad
C_{\mathrm{RMSE}}(d)=\sqrt{6L_d},\qquad
C_X(d)=(6L_d)^{1/3}.
\]

At \(d=10\): \(6L_{10}=12.417673963604\), \(\sqrt{6L_{10}}=3.523872007\), \((6L_{10})^{1/3}=2.315688209\). Round \(C_X\) **DOWN** to \(2.3156\) when used as a sample-complexity lower-bound coefficient (minor 3: v4 rounded this UP, which is the unsafe direction for a skeleton inversion). The raw single-tone coefficient before evaluating \(L_d\) is \(\sqrt6=2.44948974278318\). A non-asymptotic inversion of Riemann–von Mangoldt is **OWED-RvM**. The mean-spacing surrogate \(X\gtrsim(\gamma_d/2\pi)^K\) is heuristic (**OWED-mean-gap**).

### 11.4 Lindeberg ratio and \(\sigma^2\) at \(\Gamma_{\mathrm{op}}\) (mean-field scalar)

These are **diagnostics of the phase-sum experiment**, not inputs to Theorems A or B. Intensity-smoothed, \(a_{\omega}=\omega^{-2}\):

\[
\sigma^2(\Gamma)=\frac{\Gamma^{-3}}{3\pi}\Bigl(\log\frac{\Gamma}{2\pi}+\frac13\Bigr),
\qquad
\Lambda(\Gamma)=\frac{6\pi}{\Gamma\bigl(\log(\Gamma/2\pi)+1/3\bigr)}.
\]

At \(\Gamma=\Gamma_{\mathrm{op}}\):

\[
\frac{\Gamma_{\mathrm{op}}}{2\pi}=8.15408392960,
\qquad
\log(\Gamma_{\mathrm{op}}/2\pi)=2.09851889740,
\qquad
\log(\Gamma_{\mathrm{op}}/2\pi)+\tfrac13=2.43185223073.
\]

Receipt: old-cut independent values at \(\Gamma=51.23361986\) were \(\Gamma/2\pi=8.15408385321010\), \(L=2.09851888803441\), \(\Gamma(L+1/3)=124.592592265252\) (`T1_V4_REFEREE_2026-08-26.md` §II). The cut shift \(\delta\Gamma=4.8\times 10^{-7}\) gives \(\delta\Gamma/\Gamma=9.368\times 10^{-9}=\delta L\), hence \(\Gamma/2\pi\leftarrow +7.639\times 10^{-8}\), \(L\leftarrow +9.368\times 10^{-9}\), and \(\Gamma(L+1/3)\leftarrow\times(1+1.322\times 10^{-8})\).

\[
\Gamma_{\mathrm{op}}\bigl(\log(\Gamma_{\mathrm{op}}/2\pi)+\tfrac13\bigr)=124.59259391,
\qquad
6\pi=18.84955592153876,
\qquad
\Lambda_{\mathrm{as}}(\Gamma_{\mathrm{op}})=18.84955592153876/124.59259391=0.1512895376.
\]

Round **UP**: \(\Lambda_{\mathrm{as}}(\Gamma_{\mathrm{op}})\le\mathbf{0.1513}\).

\[
\sigma^2_{\mathrm{as}}(\Gamma_{\mathrm{op}})
=\frac{\Gamma_{\mathrm{op}}^{-3}}{3\pi}\bigl(L+\tfrac13\bigr)
=1.91867279\times 10^{-6},
\qquad
\sigma_{\mathrm{as}}(\Gamma_{\mathrm{op}})
=1.38516165\times 10^{-3}.
\]

Receipt: old-cut independent \(\sigma_{\mathrm{as}}^2=1.91867284051605\times 10^{-6}\) (v4-referee §II), times \(1-2.425\times 10^{-8}\) from \(d\log\sigma^2=-3\,\delta\Gamma/\Gamma+\delta(L+1/3)/(L+1/3)\). The identity \(\sigma^2=2\Gamma^{-4}/\Lambda\) holds algebraically and is not an independent evaluation. v4’s displayed \(1.91848\times 10^{-6}\) was not a rounding of this formula (minor 1).

Exact-Riesz mean-field: the v4-referee’s independent quadrature at the old cut was \(\Lambda_{\mathrm{Riesz}}=0.151227204626720\). The relative cut shift \(9\times 10^{-9}\) does not change the UP rounding. Round **UP**: \(\Lambda_{\mathrm{Riesz}}(\Gamma_{\mathrm{op}})\le\mathbf{0.1513}\). A hashed quadrature receipt at the new cut is **OWED-quad-receipt** (GAP-8).

### 11.5 Kolmogorov label \(d_K\) (mean-field scalar, Defect 13)

Berry–Esseen, Shevtsova constant \(C=0.56\):

\[
\frac{\rho_{\mathfrak{p}}}{\sigma^3}
=\frac{16}{15\pi^2}\,(3\pi)^{3/2}\,\Gamma^{-1/2}\,
\frac{L+1/5}{(L+1/3)^{3/2}}.
\]

Ingredients: \(16/(15\pi^2)=0.108076\), \((3\pi)^{3/2}=28.9334\), \(\Gamma_{\mathrm{op}}^{-1/2}=0.139708\), \(L+1/5=2.29851890\), \((L+1/3)^{3/2}=3.7923\). Updating the old-cut independent value \(0.264789314387639\) by the logarithmic differential \(-6.386\times 10^{-9}\) gives \(\rho/\sigma^3=0.264789313\). Then \(0.56\times 0.264789313=0.148282015\). Round **UP**: \(d_K^{\mathrm{as}}(\Gamma_{\mathrm{op}})\le\mathbf{0.1483}\). The old-cut exact-Riesz quadrature \(0.148254612631188\) likewise UP-rounds to \(0.1483\).

**Label.** Mean-field scalar approximation only: intensity integrals, \(a_{\omega}=\omega^{-2}\) or exact \(\lvert M_W\rvert\), marks \(r\equiv 1\), at a single time. Not a bound on the efficient score or the path. Transfer to the score is **OWED-H-score-BE**. Path-space distance is **OWED-path**.

### 11.6 GAP-4 ceilings from exact \(D\) (Lemma 4, piecewise)

Endpoint evaluations of (3.0) at \(\omega_{-}=\gamma_j-h\), with \(h=1.4597878593777\). Intermediates for \(j=10\) (load-bearing, log branch):

\[
\omega_{-}=48.3140446182946,\quad
\omega_{-}^2=2334.24691,\quad
\frac{2\omega_{-}}{\omega_{-}^2+1/4}=0.04139140,\quad
\frac{2\omega_{-}}{\omega_{-}^2+9/4}=0.04135597,
\]

\[
\frac{\omega_{-}}{2\pi}=7.689419,\quad
L=2.039845,\quad
\frac1{\omega_{-}L}=0.01014680,\quad
D(\omega_{-})=-0.07260057.
\]

Then \(2h\cdot(-D)=0.211961\), \(\exp(2h\cdot(-D))=1.23610\). Round **UP** \(1+\delta_{10}\le\mathbf{1.237}\). \(F_{10}^{\mathrm{flat}}\ge 1/1.23610=0.808996\), **DOWN** \(\mathbf{0.8089}\).

| \(j\) | branch | \(\omega_{-}=\gamma_j-h\) | \(-D(\omega_{-})\) | \(2h(-D)\) | \(1+\delta_j\) exact | UP | \(F^{\mathrm{flat}}\) DOWN |
|---:|:---|---:|---:|---:|---:|---:|---:|
| 1 | floor | 12.67493728 | \(0.31315886\) | \(0.914291\) | \(2.49500569\) | **2.49501** | **0.4008** |
| 2 | log | 19.56225178 | \(0.15880115\) | \(0.463632\) | \(1.58983795\) | **1.590** | **0.6289** |
| 3 | log | 23.55106972 | \(0.13732644\) | \(0.400940\) | \(1.49322016\) | **1.494** | **0.6696** |
| 4 | log | 28.96508827 | \(0.11530075\) | \(0.336630\) | \(1.40021986\) | **1.401** | **0.7141** |
| 5 | log | 31.47527373 | \(0.10720657\) | \(0.313001\) | \(1.36751840\) | **1.368** | **0.7312** |
| 10 | log | 48.31404462 | \(0.07260057\) | \(0.211961\) | \(1.23610193\) | **1.237** | **0.8089** |

The \(j=1\) row is Lemma 4(b), not the log-branch formula. The v6 log-branch \(j=1\) display (UP \(1.796\), DOWN \(0.5570\)) is withdrawn (unsafe even as a log-branch number, and the wrong branch). The \(j=2\) floor is **DOWN** \(0.6289\): the exact reciprocal is \(0.628994922349\), so v6’s DOWN \(0.6290\) was unsafe.

(Intermediates for \(j=2,\dots,5\): the same three-term evaluation of the log branch of (3.0) as displayed for \(j=10\). On \([\gamma_1^{\mathrm{anchor}},\Gamma_{\mathrm{op}}]\), \(D'>0\). At the right endpoint,
\[
D'(\Gamma_{\mathrm{op}})=0.001253651
\]
(the v6 figure \(0.001321\) is withdrawn). Arithmetic: \(\omega=\Gamma_{\mathrm{op}}\), \(\omega^2=2624.88385\), \(2(\omega^2-1/4)/(\omega^2+1/4)^2+2(\omega^2-9/4)/(\omega^2+9/4)^2=0.0015217\), \(L=2.09851890\), \((L+1)/(\omega^2 L^2)=0.00026805\), difference \(0.00125365\).) The superseded \(\exp(16\pi K/(\gamma_j T))\) column (e.g. \(1.2644\) at \(j=10\), UP \(1.27\)) is larger than the exact-\(D\) ceiling at \(j=10\) and is not used.

### 11.7 Per-tone leakage (not a theorem input)

The superseded draft’s coloured band-limited \(3\times 3\) at \(\Gamma=51.234\), \(\Omega=102.468\), tone \(\gamma_d\): \(\lambda_{\max}(I_{N_d}^{-1}I_{R_d})=0.0862\), and \([I^{-1}]_{\omega\omega}/\bigl(24 S_{\eta}(\gamma_d)/(A^2 T^3)\bigr)=0.99392\). Relative cut shift \(\lvert 51.234-\Gamma_{\mathrm{op}}\rvert/\Gamma_{\mathrm{op}}=7.4\times 10^{-6}\). Adopt, rounding **UP**, \(\kappa_d\le\mathbf{0.0863}\) at \(\Gamma_{\mathrm{op}}\) for \(j=d\), pending a dedicated receipt (**OWED-B1-receipt**). Then \(F_d^{\mathrm{leak}}=(1.0863)^{-1}=0.920556\), **DOWN** \(0.9205\). This factor is **missing** from Theorem A and from any certified product.

Per-tone \(\kappa_j\) for \(j\ne d\) at \(\Gamma_{\mathrm{op}}\) is unmeasured. Global \(3d\times 3d\): **OPEN-B1-global**. Intensity-smoothed tail leakage numbers of v4 §11.7 are unchanged at this relative cut shift and remain non-Fisher diagnostics (`T1_GAP9_STATIONARY_EXTENSION.md`).

### 11.8 Out-of-theorem diagnostic \(\Gamma=50\)

\(\Lambda_{\mathrm{as}}(50)=0.156591636223\) (v4-referee; UP to \(0.157\)). Exact-Riesz quadrature \(\Lambda(50)=0.156523843835\). \(d_K^{\mathrm{as}}(50)\le 0.151\) (mean-field scalar). Not theorem-operating values.

### 11.9 Harmonic constant (audit only)

\(H_9=7129/2520=2.828968253968254\), \(H_9/\pi=7129/(2520\pi)=0.900488562938192\). If \(C_{\diamond}=1\) (audit, not a theorem), \(C(10,4)/K=H_9/(\pi K)=0.225122\), \(F^{\mathrm{cross}}(10,4)=1/1.225122=0.816245\), **DOWN** \(0.816\). \(C_{\diamond}\) remains OWED; this audit number is not multiplied into any claimed theorem floor.

### 11.10 Certified \(F^{\mathrm{win}}\) at the operating \(T\)

\(\gamma_{10}T=49.773832477672302\times 17.2167079396264295=856.941537\). Then \(84/(\gamma_{10}T)=0.098023\), \(F_{10}^{\mathrm{win}}=0.901977\), **DOWN** \(\mathbf{0.9019}\). At \(j=1\): \(\gamma_1 T=243.353\), \(84/(\gamma_1 T)=0.3452\), \(F_1^{\mathrm{win}}=0.6548\). Continuous comparison: \(32/(\gamma_{10}T)=0.03734\), \(F_{10}^{\mathrm{win},\infty}=0.96266\), **DOWN** \(0.9626\). Upper discrete-white comparison from (5.5), **\(2\times 2\) \(H\)-block only**: \(F_{10}^{\mathrm{win},\uparrow}\le 1.1076\) (UP, §7bis.4). This is not a factor of (A\(\infty\).1).

---

## 12. Numerical displays at \(\Gamma_{\mathrm{op}}\) (no Theorem A floor)

Auxiliary: \(T^{3/2}=71.43733\), \(\sqrt6=2.44948974278318\), \(\sqrt{6L_{10}}=3.523872007\).

**Comparison skeleton (locally-white unnamed-factor coefficient at \(S_s=0\); not a proved A\(\infty\) limit; not Theorem A):**

\[
\frac{\sqrt{6L_{10}}}{T^{3/2}}=0.049328165.
\]

Round **DOWN**: \(\mathbf{0.04932}\). At \(j=1\): \(\sqrt{6L_1}/T^{3/2}=0.03087421\), **DOWN** \(0.03087\).

**Certified Theorem A factors** (all of them): \(F_j^{\mathrm{win}}\) with \(C_{\mathrm{win}}=84\). At \(j=10\): \(F_{10}^{\mathrm{win}}\ge 0.9019\) (DOWN). No other multiplicative factor is certified for Theorem A.

**Certified Proposition A\(\infty\) envelope (V6-R4-B1):** lower constant \(C_{10}^{\downarrow}=24 S_s/A_{10}^2\); upper side \((S_s+S_{\max})\,n T^2\,[(G_{10}^{\mathrm{disc}})^{-1}]_{\gamma_{10}\gamma_{10}}\) with \(S_{\max}\le 1.4414\) (UP). The v6 closed-form upper \(C_{10}^{\uparrow}F_{10}^{\mathrm{win},\uparrow}\) is **OWED-Ainfinity-validity**. Named one-sided comparison slacks: \(F_{10}^{\mathrm{flat}}\ge 0.8089\) (DOWN, log branch), \(F_1^{\mathrm{flat}}\ge 0.4008\) (DOWN, floor branch), \(F_{10}^{\mathrm{win},\infty}\ge 0.9626\) (DOWN, lower envelope), \(F_{10}^{\mathrm{win},\downarrow}\ge 0.9019\) (DOWN). The \(2\times 2\) diagnostic \(F_{10}^{\mathrm{win},\uparrow}\le 1.1076\) (UP) is not a theorem factor of (A\(\infty\).1).

**Missing factors (not inserted, not replaced by 1 in any claimed floor):** \(F^{\mathrm{leak}}\) (OWED-B1-receipt / (B1)\(_j\)); \(F^{\mathrm{cross}}\) (OWED-\(C_{\diamond}\); not a theorem factor). \(E_{\mathrm{Sz}}\) is **OWED-NOT-USED** and is not a missing factor of any displayed equality.

**No numerical Theorem A floor is displayed.** A product that omits a factor in \((0,1]\) is an upper envelope on the unfinished right-hand side, not a weaker certified floor (N4).

**Measured coloured inverse (computation, not a theorem; minor 2).** Variance ratio \(0.993916700836\) at \(\Gamma=51.234\), \(j=d\). RMSE conversion uses the square root: \(\sqrt{0.993916700836}=0.99695371\), times the comparison skeleton \(0.049328165\times 0.99695371=0.04917790\), **DOWN** \(\mathbf{0.04917}\). v4 multiplied the RMSE by the variance ratio and obtained \(0.04903\), which is not a correct RMSE.

**Theorem B, \(j=10\in\{2,\dots,d\}\), external centre \(\mu_{10}=\gamma_{10}\), admissible \(\rho_{10}=2.94999634\times 10^{-9}\), tied score.** \(\mu-\rho_{10}=49.7738324747223\), \(\log((\mu-\rho_{10})/2\pi)=2.069612327\). The locally-white skeleton (not \(I_{\mathrm{tied}}\)) is

\[
I^{\mathrm{skel},\uparrow}_{10}=\frac{T^3}{6\times 2.069612327}=\frac{5103.29103}{12.41767396}=410.970
\quad\text{(UP as a denominator: }411.0\text{)},
\]

\[
I(\pi_{10})=\frac{\pi^2}{\rho_{10}^2}=1.134114\times 10^{18}
\quad\text{(UP as a denominator: }1.13412\times 10^{18}\text{)}.
\]

The sum is \(1.13412\times 10^{18}\) at the displayed precision. Then \(1/I(\pi_{10})\le 8.8174\times 10^{-19}\). This is a **comparison skeleton**, not a Theorem B floor: it is not \(\mathbb{E}_{\pi}[I_{\mathrm{tied}}]\); \(F^{\mathrm{leak}}\) is missing; (H-circle) is an explicit hypothesis; and the bound is prior-dominated because \(\rho_{10}\) is the (M5) cut excess. The v6 display \(0.04808\) used the inadmissible half-width \(h/2\) and is **withdrawn**. The tied extra-term relative size at this operating point remains \(\delta_{10}^{\mathrm{tied}}\le 4.21\times 10^{-5}\) (UP, §8.3).

Support-uniform certified comparison factors for Theorem B at \(j=10\): leftmost frequency \(\mu-\rho_{10}-h=48.31404461534\), coinciding with \(\gamma_{10}-h\) at the displayed precision, so \(F^{\mathrm{flat,unif}}\ge 0.8089\) (DOWN) and \(F^{\mathrm{win,unif}}\ge 0.9019\) (DOWN). (The v6 values \(0.8065\) and \(0.9005\) used \(\mu-h/2\) and are withdrawn with that prior.)

**Sample-complexity coefficient (locally-white skeleton, not Theorem A).** \(C_X(10)=2.315688209\), round **DOWN** to \(\mathbf{2.3156}\).

**Resource max with resolution.** Accuracy and (M5) combine as \(\log X\ge\max\{C_X(d)\,\varepsilon^{-2/3}\cdot(\text{skeleton factors})^{1/3},\; 2\pi K/\Delta_d^+\}\), with \(\Delta_d^+=\min\{\min_{j<d}(\gamma_{j+1}-\gamma_j),\,\gamma_{d+1}-\gamma_d\}\). At the operating point the resolution term is already satisfied by construction of \(\Gamma_{\mathrm{op}}\). This display is not a Theorem A floor.

---

## 13. Empirical notes (Prop. R disclosure on every use)

**Disclosure, repeated.** Every numerical comparison in this section that uses Proposition R assumes RH, simplicity of every nontrivial zero, and \(J_{-1}(T)=O(T)\). Lean standing covers only the eight finite-core lemmas.

### 13.1 GAP-11 amplitude validation — resolved, conditional on Prop. R

On the actual Cesàro observable at \(N_{\max}=3\cdot 10^7\), a matched filter applied to \(y(t)\) constructed from the Möbius sieve (`t1_gap11_yt_estimator.py`; receipt `T1_GAP11_YT_RECEIPT.json`) gives

\[
|C(\gamma_1)|=6.287349\times 10^{-3},
\qquad
a_{\gamma_1}^{\text{Prop. R}}=6.271348\times 10^{-3},
\qquad
\text{ratio }=1.0026.
\]

This is a same-observable, same-estimator comparison of a measured amplitude to Prop. R’s predicted amplitude. It is **not** a location-error comparison and **not** a test of Theorems A or B. Status: resolved, conditional on Prop. R’s three hypotheses.

### 13.2 GAP-11 Gate-1 location risk — OPEN

The superseded draft compared a model-N2 RMSE number \(0.03087\) at \(\gamma_1\) to Gate-1’s MUSIC/periodogram absolute error \(0.00565\) on a **different** observable (prime counts) under a **different** noise model (N1). RMSE is an expectation; a single realised absolute error below an RMSE number is not a contradiction of an RMSE bound.

What remains **OPEN** is a comparison of empirical **MSE** of a named estimator on the **same** observable (S1) or on \(\mathcal{G}_{N2}^{n}\), against Theorem A or Theorem B. This file does not say that Gate-1 “violates the bound.”

### 13.3 Prior art (GAP-12)

Live re-scout `T1_GAP12_LIVE_RECHECK_2026-08-26.md`: CR / Fisher bound for zeta-zero *location* unoccupied (NONE/SETUP-ONLY). Setup citations: Hardy–Riesz, Ingham, Titchmarsh, Ng 2004, Odlyzko–te Riele 1985, Rife–Boorstyn / Kay.

---

## 14. Model-fidelity discussion (no transfer)

This section is not a theorem. Nothing in it is claimed to transfer a \(\mathcal{G}_{N2}^{n}\) bound to the random-phase sum or to a fixed zeta configuration.

### 14.1 Stam obstruction (why no transfer is claimed)

Let \(\xi\) have density \(f\), mean \(0\), variance \(1\), Fisher information \(I(f)=\int(f')^2/f\). Stam’s inequality \(I(f)\ge 1=I(\varphi)\), equality iff \(f\) is Gaussian (*citation:* Stam, *Information and Control* 2 (1959); written out in `T1_GAP17_PROPAGATION.md` §2.1). In a location family, the **true** van Trees / CR number is *smaller* than the Gaussian number. The Gaussian display is therefore **not** a lower bound for the full phase-sum class.

The same projection argument on path space, for additive noise with **fixed** covariance, gives \(I_{\mathrm{true}}(\theta)\succeq I_{\mathcal{G}}(\theta)\) whenever the true score exists (`T1_GAP17_PROPAGATION.md` §2.3). The infinite-dimensional RKHS statement is **OWED-Stam-path** (distinct from **OWED-path**, which is path-space distance of \(\{\eta_{\Gamma}(t)\}\) to the Gaussian process with spectrum \(S_{\eta}\)). Direction: to turn \(I_{\mathcal{G}}\) into a valid MSE lower bound for the full class one must **upper**-bound \(I_{\mathrm{true}}\).

Godambe’s sandwich is not an information inequality. It is not used.

### 14.2 Why the \(\sqrt{m}\) full-class route is vacuous (Defect 14)

The phase sum has bounded support. Intensity-smoothed at \(\Gamma_{\mathrm{op}}\) with \(a_{\omega}=\omega^{-2}\),

\[
\sum_{\gamma>\Gamma}a_{\gamma}
\approx\frac{L+1}{2\pi\Gamma}=0.009625,
\qquad
R_*\approx\frac{2\sum a}{\sigma_{\mathrm{as}}}=13.90,
\]

rounded **UP** to \(R_*\le 14\). The truncated-Gaussian reference \(\varphi^R\) remains strictly positive at \(\pm R_*\), while the true density vanishes at the edge of its support. Hence \(m=\mathrm{ess\,inf}_{[-R_*,R_*]}f/\varphi^R=0\). A multiplicative law \(\mathrm{MSE}\ge m/(I_{\mathcal{G}}+I(\pi))\) is vacuous. **H-ratio is not proposed as a viable full-class theorem.** A bulk-plus-tail inequality is **OPEN-full-class**.

Edgeworth main-term kurtosis, same smoothing, at \(\Gamma_{\mathrm{op}}\): \(\lvert\gamma_2\rvert\le 0.0897\) (UP), \(\gamma_2^2/6\le 0.00134\). Lyapunov\(_6\le 0.0141\) (UP). The remainder constant in \(r=O(\mathrm{Lyapunov}_6)\) is **OWED-Edgeworth**.

### 14.3 The fill is an order-one modelling replacement (GAP-9)

For fixed \(\gamma_j<\Gamma\), true-tail leakage through a length-\(T\) Fejér probe is \(O(T^{-1})\) (`T1_GAP9_STATIONARY_EXTENSION.md` (4.3)–(4.5)). The (M4) fill is the **entire** noise floor of the *coloured* locally-white comparison coefficient, not a vanishing error. In the discrete experiment the sampling noise \(\sigma_s^2\) already regularises Cameron–Martin membership; removing the fill still changes the in-band symbol by an order-one relative amount. GAP-9 remains **OPEN** as a justification of \(\mathcal{G}_{N2}^{n}\) from a fixed zeta configuration. Inside \(\mathcal{G}_{N2}^{n}\), the fill is a stipulated regulariser.

### 14.4 Heavy tails of \(1/|\zeta'|\)

Under (M3′) the mark \(r\equiv 1\) is deterministic. The divergent second moment of \(1/|\zeta'|\) does not enter \(S_{\eta}\) or the leading constants of Theorems A and B. Falsification gate G-a of `G1_MODEL_SPEC.md` §5 does not fire **for \(\mathcal{G}_{N2}^{n}\)**.

---

## 15. Current ledger

One row per remaining OPEN/OWED item. No history.

| ID | Status | Content | Needed to close |
|---|---|---|---|
| OWED-Ainfinity-validity | OWED | Closed-form upper bound \([(G_j^{\mathrm{disc}})^{-1}]_{\gamma_j\gamma_j}\le F_j^{\mathrm{win},\uparrow}\cdot 24/(A_j^2 n T^2)\) converting the Loewner right side of (A\(\infty\).1) into v6’s \(C_j^{\uparrow}F_j^{\mathrm{win},\uparrow}\). The \(2\times 2\) bound (5.5) does not supply this: Schur increases the inverse. v7 proves the Loewner comparison against \([(G_j^{\mathrm{disc}})^{-1}]_{\gamma_j\gamma_j}\) itself. | A \(3\times 3\) amplitude-Schur / Abel upper bound on the free-amplitude Gram inverse |
| OPEN-B1-global | OPEN | Full \(3d\times 3d\) \(\lambda_{\max}(I_N^{-1}I_R)\) at \(\Gamma_{\mathrm{op}}\) | Committed script + `*_RECEIPT.json` at \(d=10\), \(K=4\), \(\Omega=2\Gamma_{\mathrm{op}}\) |
| OWED-B1-receipt | OWED | Per-tone \(\kappa_j\) at \(\Gamma_{\mathrm{op}}\) for all \(j\); \(j=d\) transferred from \(\Gamma=51.234\) | Same receipt, per-tone \(3\times 3\), including a uniform \(\kappa_j^{\pi}\) on Theorem B’s prior support |
| OWED-\(C_{\diamond}\) | OWED | Coloured pairwise block constant in \(C(d,K)\); not a Theorem A factor; matching upper bound on \([I^{-1}]_{\gamma_j\gamma_j}\) | Operator-norm bound on off-diagonal \(3\times 3\) blocks |
| OWED-frame-uniform | OWED | Dimension-uniform confluent-frame bound for the coloured family with nuisance Schur complements (§6(b)) | Distinct from the fixed-\(d\) constant \(C_{\diamond}\) |
| OWED-overlap | OWED | Near-tone bands overlap under (M5); harmless for (6.1), not for a disjoint-band frame | Partitioned decomposition or gaps \(>2h\) |
| OWED-last-tone | OWED | \(\arg\max_j\) of a named-factor right-hand side | Evaluate at all \(j\) once every \(F_j\) is numerical |
| OWED-S1 | OWED | Integer-\(N\) Prop. R vs discrete Gaussian surrogate | Real-\(N\) Riesz formula, or a Fisher comparison of (S1) to \(\mathcal{G}_{N2}^{n}\) |
| OWED-ERiesz-\(C_A\) | OWED | Explicit \(C_A\) in \(\lvert E_{\mathrm{Riesz}}(N)\rvert\le C_A N^{-A}\) | Bound the vertical integral on \(\mathrm{Re}\,s=-A\) |
| OPEN-GAP-9 | OPEN | Fill as a model of a fixed zeta configuration | Palm/continuum limit in a high-height regime, or a minimax (N3) replacement |
| OPEN-GAP-11-Gate1 | OPEN | Ensemble location-risk comparison of a named estimator on (S1) or \(\mathcal{G}_{N2}^{n}\) to Theorem A/B | Same observable, MSE not a single absolute error |
| OPEN-full-class | OPEN | Any multiplicative/additive transfer of \(I_{\mathcal{G}}\) to the phase-sum class; \(m=0\) | Upper bound on \(I(f)\), or a bulk+tail inequality |
| OWED-H-score-BE | OWED | \(d_K\) of the whitened profiled score versus scalar \(\eta_{\Gamma}(t)\) | Lyapunov ratio of the matched-filter weights |
| OWED-path | OWED | Path-space distance of \(\{\eta_{\Gamma}(t)\}\) to the Gaussian process with spectrum \(S_{\eta}\) | Hellinger / RKHS-control metric on the band |
| OWED-Stam-path | OWED | Infinite-dimensional RKHS form of the Stam projection \(I_{\mathrm{true}}\succeq I_{\mathcal{G}}\) (`T1_GAP17_PROPAGATION.md` §2.3) | Distinct from OWED-path |
| OWED-Edgeworth | OWED | Remainder in the Edgeworth expansion of \(I(f)\) | Remainder theorem with explicit constant |
| OWED-Szego | OWED-NOT-USED | \(C^1\)-symbol Toeplitz remainder; the declared symbol is \(n\)-dependent and discontinuous at \(\pm\Omega\) | Not consumed. Proposition A\(\infty\) uses Lemma 5 (Parseval) and Lemma 2 (Abel); Lemma 6 is diagnostic only |
| OWED-B-uniform | OWED | Conversion of Theorem B into a frequentist bound uniform on \(\mathrm{supp}(\pi)\) | Modulus of continuity of \(I(\theta)\) |
| OWED-H-circle | OWED | Load-bearing **hypothesis of Theorem B** (§8.2): uniform phase prior on \(\mathbb{R}/2\pi\mathbb{Z}\) versus Euclidean Gill–Levit | Cuff prior, or a manifold statement. Until closed, Theorem B remains conditional on (H-circle) |
| OWED-B-tied-eval | OWED | Numerical \(\mathbb{E}_{\pi}[I_{\mathrm{tied}}]\) of the discrete experiment (coloured \(\Sigma^{-1}\)) at \((n,\sigma_s,\Gamma_{\mathrm{op}})\) | Evaluate (8.4) along (P1″); the white envelope (8.5) is the proved upper bound |
| OWED-ZZ | OWED | Ziv–Zakai bound for the periodogram threshold region | Separate note |
| OWED-mean-gap | OWED | Replacing \(\Delta_d^+\) by the mean spacing \(2\pi/L_d\) | Not a consequence of Riemann–von Mangoldt |
| OWED-RvM | OWED | Non-asymptotic inversion of \(N_{\zeta}(H)\) with a published remainder | Choose a remainder and invert |
| OWED-quad-receipt | OWED | Hashed quadrature receipt for exact-Riesz \(\Lambda\) and \(d_K\) at \(\Gamma_{\mathrm{op}}\) (distinct from the generic GAP-8 row) | Committed integrator + `*_RECEIPT.json` at \(\Gamma_{\mathrm{op}}=51.23362034\) |
| GAP-8 | OWED | Committed scripts + hashed receipts for every numerical figure in §11–§12; list of missing receipts: new-cut \(\kappa_d\), exact-Riesz integrals at \(\Gamma_{\mathrm{op}}\), discrete Gram (5.3) at \(n=n_{\star}\) | `t1_verify.py` successor under version control with `*_RECEIPT.json` |
| OPEN-N3 | OPEN | Minimax over admissible zero configurations | Spec §3-N3; not in v7 scope |

Vacated v4/v5/v6 rows that this file **displays a proof of**, and therefore does not restore as open:

- **OWED-C_win** (also **OWED-\(C_{\mathrm{win}}\)**): closed by Lemma 2 with the displayed Abel bound \(\lvert\sum k^2 e^{ik\theta}\rvert\le 2(n-1)^2/\lvert\sin\psi\rvert\), normalised \(H=G^{\mathrm{disc}}/A^2\), and \(\tau(1-r)\le 83.53<84\).
- **OWED-GAP4-remainder**: closed by piecewise Lemma 4. Log branch on \([\gamma_1^{\mathrm{anchor}},\Omega]\) with \(D'>0\) proved at \(\omega_{\min}=\gamma_1^{\mathrm{anchor}}\); floor branch \(D=-R\) on \((0,\gamma_1^{\mathrm{anchor}}]\); \(j=1\) ceiling \(1+\delta_1\le 2.49501\) displayed.

Vacated and not reopened: OWED-amp-avg (no independent amplitude prior); OWED-B-avg for the leading comparison skeleton (closed by the decreasing-in-\(\gamma\) endpoint bound on the admissible support); OWED-GAP-6 (Theorem A is already discrete); OWED-B-tied-score (the tied score (8.3) and \(I_{\mathrm{tied}}\) (8.4) are derived; residual evaluation is OWED-B-tied-eval); the v6 product-prior radius \(h/2\) (replaced by \(\rho_j\), not an owed proof); the \(j=1\) Theorem B quantifier (excluded, not repaired).

Restored as an open row, as required: **OWED-Ainfinity-validity**.

---

## 16. Claims and not-claims

**Claimed.**

- Theorem A: a pointwise Cramér–Rao lower bound for unbiased estimators of the discrete exact Gaussian surrogate \(\mathcal{G}_{N2}^{n}\), at fixed admissible \(d\), with exact Fisher (4.0n), the Schur step (6.1), and certified \(F^{\mathrm{win}}\) (\(C_{\mathrm{win}}=84\), Abel step displayed).
- Proposition A\(\infty\): the Loewner sandwich (A\(\infty\).0) and the comparison envelope (A\(\infty\).1) of the exact finite-\(n\) Fisher (4.0n), with closed-form lower constant \(C^{\downarrow}=24 S_s/A_j^2\) and Loewner upper side \((S_s+S_{\max})n T^2[(G_j^{\mathrm{disc}})^{-1}]_{\gamma_j\gamma_j}\). Named one-sided slacks. No limiting equality. Not Theorem A. \(E_{\mathrm{Sz}}\) OWED-NOT-USED. The v6 closed-form right side through (5.5) is not claimed.
- Theorem B, **conditional on (H-circle)**, **for \(j\in\{2,\dots,d\}\)**: a Bayes van Trees lower bound (B.0) for arbitrary measurable estimators of the same surrogate, under an externally centred raised-cosine prior on ordinates with admissible half-widths \(\rho_j\), with \(A_j=2a(\gamma_j)\), the tied-submodel Fisher \(I_{\mathrm{tied},j}\) of the score (8.3), joint \((\pi_{\gamma}\otimes\pi_{\phi})\) expectation, and support-uniform certified comparison factors \(F^{\mathrm{flat}}\), \(F^{\mathrm{win}}\).
- Spectral density (2.2) of the tail under (M3′); covariance independent of \(\theta\); cancellation of the mean-field window factor \(a(\omega)\) at the true surrogate parameter and \(\pi_j\)-almost surely under (P1″) for \(j\ge 2\), not of \(1/|\zeta'|\), and not for \(j=1\).
- (M5)-admissibility of \(\Gamma_{\mathrm{op}}=51.23362034\) at the stated \(T,K\) and the **full** stored \(\gamma_{10}\), via \(T(\Gamma_{\mathrm{op}}-\gamma_{10})-8\pi=5.079\times 10^{-8}>0\); positivity of the six tabulated \(\rho_j\).
- Proposition R as a cited + Lean-core statement, with the three hypotheses disclosed at every use in this file.
- GAP-11 amplitude match \(\lvert C(\gamma_1)\rvert/a_{\gamma_1}=1.0026\) on \(y(t)\), conditional on Prop. R.
- The arithmetic of §11–§12, with the stated rounding and with no Theorem A numerical floor.

**Not claimed.**

- Anything unconditional about \(\zeta\).
- Any transfer of Theorem A, Theorem B, or Proposition A\(\infty\) to the non-Gaussian phase sum (Stam).
- Any transfer to a fixed, non-randomised zeta configuration (GAP-9).
- A global \(3d\times 3d\) leakage inequality (OPEN-B1-global).
- Uniformity in \(d\); last-tone attainment after corrections.
- That \(0.04932\), \(0.0419\), \(0.04808\), or any partial product is a Theorem A or Theorem B floor.
- That \(d_K\le 0.1483\) is a certified misspecification bound for the efficient score or the path.
- That \(\Gamma=50\) is an operating point.
- That a single Gate-1 absolute error contradicts an RMSE bound.
- That (S1) *is* \(\mathcal{G}_{N2}^{n}\) (OWED-S1).
- A minimax (N3) bound.
- A Ziv–Zakai bound.
- That unbiasedness has been dropped from the pointwise law.
- That Godambe’s sandwich is a lower-bound theorem.
- Any use of the phrase “violates the bound.”
- A limiting equality for \(T^3[(I^{(n)})^{-1}]_{\gamma_j\gamma_j}\).
- That \(E_{\mathrm{Sz}}=0\) at finite \(n\), or that \(E_{\mathrm{Sz}}\) is used.
- That \(I^{\mathrm{skel},\uparrow}\) is \(\mathbb{E}_{\pi}[I_{\mathrm{tied}}]\).
- Theorem B without (H-circle).
- Theorem B for \(j=1\).
- That (5.5) upper-bounds the free-amplitude \(3\times 3\) inverse.
- That (2.3) holds \(\pi\)-almost surely on the \(j=1\) prior support.

---

## 17. Defect map (all 19 governing + N1–N7 + V5-N1–V5-N4 + V6-R4)

| Defect | Disposition in v7 |
|---:|---|
| 1 | Repaired (kept): (M3′) deterministic \(r\equiv 1\); \(S_{\eta}\) has no \(E[r^2\mid\omega]\); no \(1/\lvert\zeta'\rvert\) cancellation claimed |
| 2 | Repaired (kept): \(\Sigma\) independent of \(\theta\); no covariance-information term; (M-amp) at the true mean and \(\pi\)-a.s. under (P1″) for \(j\ge 2\) |
| 3 | Repaired (kept): Godambe / “Gaussian-score class” deleted; Theorem A is unbiased CR; full-class transfer refused in §14 |
| 4 | Weakened in v7: Theorem B prior is on \(\gamma_j\) only, on the (M5)-admissible \(\rho_j\)-support, for \(j\in\{2,\dots,d\}\); \(A_j=2a(\gamma_j)\); centres external; Fisher is \(I_{\mathrm{tied}}\) of the tied score; (H-circle) is an explicit theorem hypothesis; \(\mathbb{E}_{\pi}[I_{\mathrm{tied}}]\) is not identified with the locally-white skeleton |
| 5 | Repaired (kept): Theorems A/B are exact-Gaussian-surrogate theorems; phase sum only in §14 with no transfer (Stam) |
| 6 | Per-tone bound via the explicit Schur step (6.1); global \(3d\times 3d\) **OPEN-B1-global**; \(F^{\mathrm{cross}}\) not a theorem factor |
| 7 | Repaired (kept): sole cut \(\Gamma_{\mathrm{op}}=51.23362034\); (M5) checked with the full stored \(\gamma_{10}\) |
| 8 | Repaired (kept, piecewise): Lemma 4 bounds exact \(D(\omega)\) by a left-endpoint evaluation on the correct branch; no \(r(\omega)\) remainder; no “modulo OWED” in a theorem factor |
| 9 | Repaired (kept) and N6: Lemma 1″ is Loewner order, not entrywise |
| 10 | Fixed \(d\); the bound is not asserted uniformly in \(d\); last-tone attainment **OWED-last-tone**; Theorem B further restricted to \(j\in\{2,\dots,d\}\) |
| 11 | Repaired (kept): Prop. R’s three hypotheses in §1.1, theorem interpretation clauses, and §13 |
| 12 | Status reconciled; (S1) vs \(\mathcal{G}_{N2}^{n}\) declared + **OWED-S1** |
| 13 | Repaired (kept): \(d_K\le 0.1483\) labelled mean-field scalar approximation |
| 14 | Repaired (kept): \(\sqrt{m}\) route vacuous (\(m=0\)); bulk+tail **OPEN-full-class** |
| 15 | Repaired (kept): target-frequency floor attributed to (M4); GAP-9 **OPEN** outside the surrogate |
| 16 | Repaired (kept): GAP-11 split; “violates the bound” deleted |
| 17 | Repaired (kept): \(E_{\mathrm{Riesz}}\) vs \(\eta_{\Gamma}\) throughout |
| 18 | Repaired (kept): named signed factors; no bare \(O(K^{-1})\); no numerical Theorem A floor; certified vs missing labelled |
| 19 | Ledger: **OWED-Ainfinity-validity** restored; **OWED-\(C_{\mathrm{win}}\)** and **OWED-GAP4-remainder** closed by displayed proofs; **OWED-Szego** OWED-NOT-USED; **OWED-H-circle** a theorem hypothesis; **OWED-B-tied-eval** residual coloured evaluation |
| N1 | Exact Fisher (4.0n) kept; \(T^{-3}\) is a comparison envelope, not a limit equality (V5-N1 / V6-R4-B1) |
| N2 | Prior on \(\gamma_j\) only, kept; Fisher is \(I_{\mathrm{tied}}\) (V5-N2); support is (M5)-admissible (V6-R4-B2) |
| N3 | Repaired (kept): \(\Gamma_{\mathrm{op}}=51.23362034\) |
| N4 | Repaired (kept): no “partially certified floor” |
| N5 | Repaired (kept): (6.1) stated and used |
| N6 | Repaired (kept): Lemma 1″ Loewner |
| N7 | Ledger updated for the four v6 remaining defects |
| V5-N1 | Weakened further: (A\(\infty\).1) lower side closed-form; upper side Loewner against \(G_j^{-1}\); (5.5) not used as a \(3\times 3\) bound |
| V5-N2 | Kept: Theorem B uses (8.3)–(8.4); extra term \(O((a'/a)^2/T^2)\) shown; residual **OWED-B-tied-eval** |
| V5-N3 | Kept: Szegő unused; Lemma 5 (Parseval) and Lemma 6 (Riemann, \(\varepsilon_a^{\mathrm{Riem}}\) corrected) |
| V5-N4 | Kept: (H-circle) is stated in Theorem B; joint-prior and MSE wording corrected |
| V6-R4-B1 | Repaired by Loewner inversion of (A\(\infty\).0) plus \((\omega,\omega)\) entry; residual closed-form (5.5) promotion **OWED-Ainfinity-validity** |
| V6-R4-B2 | Repaired: \(\rho_j\) support; six positive widths displayed; \(I(\pi)=\pi^2/\rho_j^2\) |
| V6-R4-M1 | Repaired: piecewise \(D\); \(j=1\) floor-branch ceiling \(2.49501\); \(j=2\) DOWN \(0.6289\) |
| V6-R4-M2 | Repaired: Abel step \(2(n-1)^2\) displayed; \(\varepsilon_a\le 3\pi/\tau\) justified |
| V6-R4-M3 | Repaired: \(H\) is \(G^{\mathrm{disc}}/A^2\); (5.1) written for the normalised block |
| V6-R4-M4 | Weakened: \(j=1\) excluded from Theorem B; \(\vartheta_{\min}\) is an external anchor |
| V6-R4-M5 | Ledger restored/closed as above |
| V6-R4-m1 | Repaired: \(\varepsilon_a^{\mathrm{Riem}}\le 6/n+3\omega T/n=4.71391964\) (UP) at \((n,\Omega)\) |
| V6-R4-m2 | Repaired: \(D'(\Gamma_{\mathrm{op}})=0.001253651\); \(j=1,2\) table directions |
| V6-R4-m3 | Weakened: named continuous-envelope evaluations withdrawn; \(C_{\mathrm{win}}^{\infty}=32\) kept |
| V6-R4-m4 | Repaired: joint prior, cuff/manifold branch, “does not enlarge \(1/M_{\gamma\gamma}\)”, MSE not RMSE |
| V6-R4-m6 | Repaired: \(I^{-1}\) has a \(T^{-3}\) envelope; \(T^3 I^{-1}\) is not said to scale as \(T^3\) |

Minors (unfaulted v5/v6 displays, not revised except where a v6 referee figure replaces an unsafe intermediate): (1) \(\sigma_{\mathrm{as}}^2=1.91867279\times 10^{-6}\), \(\sigma_{\mathrm{as}}=1.38516165\times 10^{-3}\); (2) coloured RMSE uses \(\sqrt{0.993916700836}\), display \(0.04917\) DOWN; (3) \(C_X\) DOWN \(2.3156\); (4) wording is “not asserted uniformly in \(d\)”, without a claim that the phrase is absent; (5) \(\Gamma/2\pi=8.15408392960\), \(L=2.09851889740\), \(\Gamma(L+1/3)=124.59259391\), \(H_9/\pi=0.900488562938192\).

---

**v7 DRAFT (grok lane) 2026-08-26 — UNREFEREED.** Not promotable until a cold referee accepts the four v6 remaining repairs against this text. Nothing in `T1_CRAMER_RAO_V6.md`, `T1_CRAMER_RAO_V5.md`, `T1_CRAMER_RAO_V4.md`, or `T1_CRAMER_RAO_DRAFT.md` may be cited as a result in preference to this file.


## POST-REFEREE CORRECTION PASS 2026-08-26 (fable) — round-5 verdict PROMOTABLE-WITH-CORRECTIONS, corrections applied
Referee: T1_V7_REFEREE_2026-08-26.md. Applied: C_win sum 83.523548 -> 83.523571
(constituents were right, the sum was misprinted; still < 83.53 < 84);
eps_a^Riem display and ledger row 4.71391963 -> 4.71391964 (UP);
j=2 intermediate 2h|D| 0.463637 -> 0.463632 (final 0.6289 DOWN unchanged).
NOT applied, with receipts: the referee's recomputed prior widths
rho_{1,2,3}=...851, rho_{4,5}=...989, rho_10=2.9499963e-9 are double-precision
artifacts on the referee's side — 40-digit mpmath recomputation (this pass)
gives rho_{1,2,3}=h/2=0.72989392968885083 (v7's printed float is exact),
rho_{4,5}=0.52519880125098767 (v7's ...987 is the correct DOWN display), and
rho_10=2.9499963406e-9 (v7's 2.94999634e-9 is the correct display; the
referee's 2.9499963 is the same value truncated). No other display changed.
STANDING AFTER ROUND 5: all load-bearing defects repaired or honestly demoted;
remaining open items are the labelled OWED/OPEN ledger rows (notably
OWED-Ainfinity-validity, OWED-B1-receipt, OWED-overlap, conditional H-circle,
prior-dominated j=d at this Gamma_op with Gamma_op=52/n=1140 documented as the
repair path). T1 v7 stands as a CONDITIONAL, PARTIALLY-CERTIFIED result at
this standing.

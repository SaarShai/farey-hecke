# T1 GAP-9 — the stationary-extension idealization

DRAFT (luna/codex lane) 2026-08-26 — UNREFEREED.

Scope: this note makes clause (M4) of `T1_CRAMER_RAO_DRAFT.md` precise. It
distinguishes time stationarity, intensity smoothing, and spectral extension;
then it bounds the finite-window error caused by the extension. Upper numerical
bounds are rounded UP.

---

## 0. Ruling

The phrase **stationary extension** hides three different operations.

1. Under (M1), random phases already make the zero tail stationary in the time
   variable. The fact that the zero intensity
   \(\lambda(\omega)=\log(\omega/2\pi)/(2\pi)\) varies with frequency does not
   make the time process non-stationary.
2. Replacing the atomic spectrum of one zero configuration by its
   intensity-smoothed mean is an ensemble/self-averaging idealization.
3. The load-bearing step for T1 is a further **support extension**: the true
   tail contains only ordinates \(|\omega|>\Gamma\), whereas (M4)–(M4″) fill
   the whole pass band, including every target \(\gamma_j<\Gamma\), with a
   positive density.

For fixed \(\gamma_j<\Gamma\), fixed separation
\(\delta_j:=\Gamma-\gamma_j>0\), and \(T\to\infty\), the intensity-smoothed
true-tail power seen by a length-\(T\) Fourier probe at \(\gamma_j\) is
\(O(T^{-1})\). The power added by the extension converges to
\(S_{\rm ext}(\gamma_j)>0\). Thus the idealization error does **not** vanish;
it converges to the entire noise floor used in T1. At the Gaussian-measure
level the change is even discontinuous: without the fill, the target score is
outside the tail-noise Cameron–Martin space and the formal continuous-record
Fisher information is infinite.

Therefore GAP-9 cannot be closed by a small finite-window correction in T1's
fixed-low-zero regime. A precise high-height/random-shift conjecture under
which the fill could emerge as a local continuum limit is stated in §7. Its
unproved marked-Palm convergence and covariance-inverse stability are marked
**OWED**.

---

## 1. Processes and spectral conventions

Let \(Z=\{\gamma:\gamma>\Gamma\}\) be a locally finite ordinate set and let
\(a_\gamma\ge0\). Under (M1), conditional on \(Z\) and the amplitudes,

\[
 \varepsilon_Z(t)=2\sum_{\gamma\in Z}a_\gamma
       \cos(\gamma t+\phi_\gamma),
 \qquad \phi_\gamma\stackrel{\rm iid}{\sim}{\rm Unif}[0,2\pi).
 \tag{1.1}
\]

The order-1 Riesz window and the truncated mark law in (M3) are assumed to
make the sum converge in the sense needed below. The draft uses

\[
 R(\tau)={1\over2\pi}\int_{\mathbb R}S(\omega)e^{i\omega\tau}\,d\omega.
 \tag{1.2}
\]

Conditional on \(Z\), the covariance and spectral measure are

\[
 R_Z(\tau)=2\sum_{\gamma\in Z}a_\gamma^2\cos(\gamma\tau),
 \qquad
 \mu_Z=\sum_{\gamma\in Z}a_\gamma^2
       (\delta_{\gamma}+\delta_{-\gamma}).
 \tag{1.3}
\]

### Proposition 1 (what is actually stationary)

Conditional on \(Z\) and \(\{a_\gamma\}\), (1.1) is strictly stationary.
In particular, its covariance depends only on the lag, as in (1.3).

*Proof.* For a time shift \(h\), replace every phase by
\(\phi_\gamma+\gamma h\pmod{2\pi}\). The shifted phases remain independent
uniform variables, so every finite-dimensional distribution is unchanged.
The covariance calculation in the draft's Proposition 4.4 gives (1.3). ∎

Restricting the process to \([0,T]\) does not make the underlying process
non-stationary. It produces the truncated covariance operator

\[
 (C_Tf)(t)=\int_0^T R(t-s)f(s)\,ds,
 \tag{1.4}
\]

whose kernel remains a function of \(t-s\); only the domain has endpoints.

---

## 2. The non-constant zero intensity

Under (M2), the ordinate point process has first intensity

\[
 \lambda(\omega)={1\over2\pi}\log {\omega\over2\pi},\qquad \omega>\Gamma.
 \tag{2.1}
\]

Campbell's first-moment identity therefore turns (1.3), in expectation, into
the absolutely continuous **tail** spectrum

\[
 S_{\rm tail}(\omega)
 =b(|\omega|)\mathbf 1_{\{\Gamma<|\omega|\le\Omega\}},
 \qquad
 b(\omega):=m_2(\omega)\log(\omega/2\pi),
 \tag{2.2}
\]

where \(m_2(\omega)=\mathbb E[a_\gamma^2\mid\gamma=\omega]\) is the
conditional second mark moment. Existence of this marked intensity is an
extra integrability requirement on (M3). In the draft's numerical
mean-field convention, \(m_2(\omega)=|M_W(1/2+i\omega)|^2\).

The intensity is inhomogeneous in the frequency coordinate. This is
compatible with time stationarity: a stationary process may have any
nonnegative spectral density; stationarity requires dependence on time lag,
not a flat spectrum.

If one merely freezes (2.1) over a local half-width \(h<\nu\), the error is
explicit. By the mean-value theorem,

\[
 \sup_{|u|\le h}{|\lambda(\nu+u)-\lambda(\nu)|\over\lambda(\nu)}
 \le {h\over(\nu-h)\log(\nu/2\pi)}.
 \tag{2.3}
\]

At the draft's \(K=4\), \(T=\log(3\cdot10^7)=17.2167\), and
\(h=2\pi K/T<1.460\), (2.3) is at most **0.143** at \(\gamma_1\) and
**0.0147** at \(\gamma_{10}\), both rounded UP. This controls local
variation of the *hypothetical continuum intensity*. It does not justify
putting any intensity below \(\Gamma\), where (2.2) is identically zero.

---

## 3. Exact statement of the T1 extension

On the approved pass band \(|\omega|\le\Omega=2\Gamma\), clauses (M4) and
(M4″) use

\[
 S_{\rm ext}(\omega)
 =a_{|\omega|}^2\vartheta(|\omega|)
   \mathbf 1_{\{|\omega|\le\Omega\}},
 \qquad
 \vartheta(u)=\max\{\log(u/2\pi),\vartheta_{\min}\}.
\tag{3.1}
\]

There is a hidden mark convention in (3.1). Clause (M3) defines
\(r_\gamma=1/|\zeta'(1/2+i\gamma)|\) only at zero ordinates; it does not
define a continuous \(r_\omega\) between them. The draft's verification
script uses the additional mean-field convention \(r_\omega\equiv1\).
Any claimed continuity or positive lower bound for the full marked
\(a_\omega\) profile outside that convention is **OWED**.

Above \(\Gamma\), (3.1) agrees with the first-moment formula (2.2). Below
\(\Gamma\), including at each target, it adds

\[
 D(\omega):=S_{\rm ext}(\omega)-S_{\rm tail}(\omega)
 =S_{\rm ext}(\omega)\mathbf 1_{\{|\omega|\le\Gamma\}}.
 \tag{3.2}
\]

Thus the relevant distinction is:

| object | spectral support | status |
|---|---|---|
| fixed zero tail | atoms at \(\pm\gamma\), \(\gamma>\Gamma\) | actual after (M1) randomization |
| intensity-smoothed tail | \(\Gamma<|\omega|\le\Omega\) | ensemble mean from (M2) |
| M4 extended Gaussian noise | all \(|\omega|\le\Omega\) | model assumption; adds (3.2) |

Gaussianization is another part of (M4), treated by GAP-17. GAP-9 is the
addition (3.2).

---

## 4. Finite-window identity and an upper bound for true-tail leakage

For a length-\(T\) Fourier probe define

\[
 Z_T(\nu):={1\over\sqrt T}\int_0^T\varepsilon(t)e^{-i\nu t}\,dt,
 \quad
 K_T(u):={1\over2\pi T}\left|\int_0^Te^{iut}\,dt\right|^2
 ={2\sin^2(uT/2)\over\pi T u^2},
 \tag{4.1}
\]

with \(K_T(0)=T/(2\pi)\) and \(\int_{\mathbb R}K_T=1\). For a process with
density \(S\) in convention (1.2),

\[
 \mathbb E|Z_T(\nu)|^2=\int_{\mathbb R}S(\omega)K_T(\omega-\nu)\,d\omega.
 \tag{4.2}
\]

Before averaging the zero process, phase averaging alone gives the exact
fixed-configuration identity

\[
 Q_{Z,T}(\gamma_j)
 ={1\over T}\sum_{\gamma\in Z}a_\gamma^2
 \left\{|D_T(\gamma-\gamma_j)|^2
       +|D_T(\gamma+\gamma_j)|^2\right\},
 \tag{4.2a}
\]

where \(D_T(u)=\int_0^Te^{iut}dt\). Since \(|D_T(u)|\le2/|u|\),

\[
 Q_{Z,T}(\gamma_j)
 \le {4\over T}\sum_{\gamma\in Z}a_\gamma^2
 \left\{{1\over(\gamma-\gamma_j)^2}
       +{1\over(\gamma+\gamma_j)^2}\right\}.
 \tag{4.2b}
\]

This is the rigorous pathwise finite-window bound whenever the weighted line
mass is finite. A numerical pathwise constant requires the actual marked
tail or a mark envelope, neither of which (M2)–(M3) supplies; that step is
**OWED**.

Let \(\nu=\gamma_j<\Gamma\),
\(\delta_j:=\Gamma-\gamma_j>0\), and
\(B_{\Gamma,\Omega}:=\int_\Gamma^\Omega b(\omega)\,d\omega\). Since
\(K_T(u)\le2/(\pi T u^2)\), (2.2) and (4.2) give

\[
 \begin{aligned}
 Q_{{\rm tail},T}(\gamma_j)
 &:=\int S_{\rm tail}(\omega)K_T(\omega-\gamma_j)\,d\omega\\
 &\le {2\over\pi T}\int_\Gamma^\Omega b(\omega)
 \left({1\over(\omega-\gamma_j)^2}
       +{1\over(\omega+\gamma_j)^2}\right)d\omega\\
 &\le {4B_{\Gamma,\Omega}\over\pi T\delta_j^2}.
 \end{aligned}
\tag{4.3}
\]

If \(b\) is non-increasing on \([\Gamma,\infty)\), the same calculation
gives the sharper bound (and allows \(\Omega=\infty\))

\[
 Q_{{\rm tail},T}(\gamma_j)
 \le {2b(\Gamma)\over\pi T}
 \left({1\over\delta_j}+{1\over\Gamma+\gamma_j}\right).
 \tag{4.3a}
\]

This is a rigorous finite-window leakage bound for the intensity-smoothed
tail, conditional on the marked-intensity assumption above. Under the
draft's mean-field order-1 Riesz convention

\[
 b(\omega)={\log(\omega/2\pi)\over
   (\omega^2+1/4)(\omega^2+9/4)}
 \le {\log(\Omega/2\pi)\over\omega^4},
\]

so (4.3) yields the closed bound

\[
 Q_{{\rm tail},T}(\gamma_j)
 \le {4\log(\Omega/2\pi)\over
          3\pi T\delta_j^2\Gamma^3}.
 \tag{4.4}
\]

If (M5) supplies \(\delta_j\ge2\pi K/T\), then

\[
 Q_{{\rm tail},T}(\gamma_j)
 \le {T\log(\Omega/2\pi)\over3\pi^3K^2\Gamma^3}.
 \tag{4.5}
\]

For the draft's \(d=10\) numbers with the **M5-admissible** cut
\(\Gamma=51.234\), \(\Omega=102.468\), \(K=4\), (4.5) is at most
**\(2.41\cdot10^{-7}\)**, rounded UP. The draft's often-used
\(\Gamma=50\) does not satisfy the top-margin part of (M5) at this \(T\):
\(50-\gamma_{10}=0.2262<2\pi K/T=1.4598\).

In the same mean-field convention, (4.3a) at the M5-admissible cut is at
most **0.0233** times \(S_{\rm ext}(\gamma_{10})\), rounded UP. This is a
matched-filter variance comparison, not an inverse-covariance/Fisher bound.

For fixed \(\Gamma,\Omega,\gamma_j\), (4.3) is \(O(T^{-1})\).

---

## 5. The extension error is order one, not a vanishing remainder

By (3.2) and (4.2), the extra finite-window power assigned by (M4) is exactly

\[
 E_{j,T}:=Q_{{\rm ext},T}(\gamma_j)-Q_{{\rm tail},T}(\gamma_j)
 =\int_{|\omega|\le\Gamma}D(\omega)K_T(\omega-\gamma_j)\,d\omega.
 \tag{5.1}
\]

This identity is already the sharpest error statement available inside the
intensity-smoothed model. It also gives two useful bounds.

First, if
\([\gamma_j-\pi/T,\gamma_j+\pi/T]\subset(-\Gamma,\Gamma)\), then
\(|\sin x|\ge2|x|/\pi\) for \(|x|\le\pi/2\) implies

\[
 E_{j,T}\ge {4\over\pi^2}
 \inf_{|\omega-\gamma_j|\le\pi/T}D(\omega).
 \tag{5.2}
\]

Thus the fill adds a fixed positive fraction of the local extended density
even at finite \(T\); it is not controlled by the tail-leakage bound (4.3).

Second, suppose \(D\) is bounded by \(M\) on the fill and is Lipschitz with
constant \(L\) on \([\gamma_j-h,\gamma_j+h]\). For any such \(h>0\),

\[
 |E_{j,T}-D(\gamma_j)|
 \le Lh+{8M\over\pi T h}.
 \tag{5.3}
\]

*Proof.* On \(|\omega-\gamma_j|\le h\), use the Lipschitz bound and
\(\int K_T=1\). Off that interval use
\(|D(\omega)-D(\gamma_j)|\le2M\) and
\(\int_{|u|>h}K_T(u)du\le4/(\pi T h)\). ∎

Taking \(h=T^{-1/2}\) once it lies inside the fill shows

\[
 E_{j,T}=D(\gamma_j)+O(T^{-1/2}),
 \qquad
 Q_{{\rm tail},T}(\gamma_j)=O(T^{-1}).
 \tag{5.4}
\]

At every target the floor is inactive and

\[
 D(\gamma_j)=S_{\rm ext}(\gamma_j)
 =a_{\gamma_j}^2\log(\gamma_j/2\pi)>0.
 \tag{5.5}
\]

Equations (5.4)–(5.5) prove the negative conclusion: for fixed low targets,
the extension error converges to the full T1 noise value rather than to zero.

The upper operator bound tells the same story. If \(\Delta C_T\) is the
covariance operator added by (3.2), Plancherel gives

\[
 0\preceq\Delta C_T\preceq\|D\|_\infty I,
 \qquad
 {\rm tr}(\Delta C_T)={T\over2\pi}\int_{-\Gamma}^{\Gamma}D(\omega)d\omega.
 \tag{5.6}
\]

The trace grows linearly with the analysis-window length; the added operator
is not a small perturbation in trace norm.

---

## 6. Why no multiplicative Cramér–Rao error bound exists here

Set the unextended Gaussian surrogate's density to zero on an open
neighbourhood \(U\) of \(\gamma_j\), as (2.2) requires. A nonzero target
score, such as

\[
 g_j(t)=-A_jt\sin(\gamma_jt+\phi_j)\mathbf 1_{[0,T]}(t),
\]

has an entire Fourier transform that cannot vanish on all of \(U\). In the
draft's Cameron–Martin criterion,

\[
 \|g_j\|_{C_{\rm tail}}^2
 ={1\over2\pi}\int_{|\omega|\le\Omega}
 { |\widehat g_j(\omega)|^2\over S_{\rm tail}(\omega)}d\omega=+\infty.
 \tag{6.1}
\]

With (3.1), the denominator is positive on the whole pass band and the norm
is finite. Hence the fill changes the Gaussian experiment from singular
(formally infinite information and zero CR lower bound) to regular (finite
information and the positive T1 bound). There is no finite multiplicative
constant comparing the two CR bounds.

This is the named obstruction: **spectral-support/Cameron–Martin
singularity**, not the slow variation of \(\lambda(\omega)\).

For a fixed atomic zero configuration there is an additional discrepancy:
the spectral measure is (1.3), not (2.2). Intensity plus pair correlation
does not supply a deterministic discrepancy bound for every weighted Fejér
linear statistic, and (M3)'s \(1/|\zeta'(\rho)|\) marks require their own
uniform-integrability control. That fixed-configuration bound is **OWED**.

The actual zeta phases are fixed numbers. Without (M1) there is a
deterministic almost-periodic function, not a probability law to which
stationarity or a Cramér–Rao calculation applies. This note therefore proves
stationarity of N2 under its stated random-phase hypothesis, not stationarity
of the literal zeta realization.

---

## 7. Precise conjecture that could justify M4 in a different regime

**Conjecture GAP-9-H (marked local-continuum/Palm limit).** Let \(H\to\infty\)
and choose a random height shift in \([H,2H]\). Put
\(\lambda_H=\log(H/2\pi)/(2\pi)\), unfold ordinates by
\(u=\lambda_H(\gamma-H)\), and condition in the Palm sense on a target zero
near the origin. Assume:

1. the unfolded zero process converges to a stationary sine-kernel process;
2. the truncated amplitude marks in (M3), after division by their local
   deterministic scale, have a stationary marked limit with enough mixing
   and uniform integrability for Fejér linear statistics; and
3. \(T_H\to\infty\) while \(T_H/\lambda_H\to0\), so a Fourier-resolution
   cell contains \(\lambda_H/T_H\to\infty\) interferers.

Then, after deleting any fixed number of target atoms, conjecturally

\[
 {T_H^{-1}\sum_{\gamma\ne\gamma_{\rm target}}
   a_\gamma^2|D_{T_H}(\gamma-H)|^2
  \over a_H^2\log(H/2\pi)}\ \longrightarrow\ 1
 \quad\text{in probability},
 \tag{7.1}
\]

where \(D_T(u)=\int_0^T e^{iut}dt\). Equation (7.1) is the atomic analogue
of the M4 value \(S_{\rm ext}(H)=a_H^2\log(H/2\pi)\).

Even (7.1) would only justify covariance along Fourier probes. Passing from
it to uniform convergence of the full Fisher Gram matrix and then through
matrix inversion is **OWED**.

The obstructions are explicit:

- GUE pair correlation alone is not convergence of the full local point
  process and does not give the concentration in (7.1);
- conditioning on an actual zero requires a Palm, not an unconditioned,
  limit;
- the derivative marks are heavy-tailed before (M3) truncation; and
- T1's fixed-low-zero regime has \(\lambda(\gamma_j)/T\ll1\), the opposite
  of assumption 3.

At the draft's operating point, the smooth-intensity expected number of
ordinates in a local half-width \(2\pi K/T\) is below one (0.375902 at
\(\gamma_1\) and 0.961610 at \(\gamma_{10}\); upper-rounded values are
0.376 and 0.962). Hence the
absolutely continuous fill has no local law-of-large-numbers justification
there. Pair correlation alone does not determine the zero-count or gap
probabilities needed to replace that missing law.

Thus (7.1) is not a claim about the first \(d\) zeros in the present draft.

### Draft-specific support correction

Section 7.3 of the draft calls \(\gamma_2\) the nearest “interferer” to
\(\gamma_1\). For the common \(d=10\) cut, \(\gamma_2,\ldots,\gamma_{10}\)
are target tones, not members of the interference tail. The first tail zero
is \(\gamma_{11}\approx52.970321\), about 38.84 above \(\gamma_1\). This
makes the fixed-configuration support gap larger than §7.3 states; it does
not weaken the negative conclusion above.

---

## 8. Obligations and status

- **PROVED:** (M1) already gives strict time stationarity; finite restriction
  does not alter the lag form of the covariance.
- **PROVED:** the varying intensity has the local relative bound (2.3).
- **PROVED inside the intensity-smoothed mean-field model:** true-tail
  leakage bounds (4.3)–(4.5), the exact extension error (5.1), and the
  non-vanishing conclusion (5.4)–(5.5).
- **PROVED inside the draft's Gaussian spectral criterion:** removing the
  fill causes the Cameron–Martin singularity (6.1), so no multiplicative CR
  error estimate exists.
- **OWED:** a deterministic or high-probability atomic-to-intensity
  discrepancy bound with the (M3) marks.
- **OWED:** Conjecture GAP-9-H and its Fisher-information transfer.

**Status: GAP-9 remains OPEN as a zeta/N3 justification.** It is resolved
negatively as a small-error statement for the fixed-low-zero N2 experiment:
M4 is a pessimistic regularizing model assumption, not a controlled
stationary approximation to the true separated tail.

---

## Sources

- `T1_CRAMER_RAO_DRAFT.md`, §§1.3–1.4, Proposition 4.4, §7.3, and GAP-9.
- `G1_MODEL_SPEC.md`, §3-N2/N3 and amendments A1–A2.
- `t1_verify.py`, header and `log_S`, for the explicitly labelled
  \(r_\omega\equiv1\) mean-field convention used in the numerical examples.
- The Fejér-kernel and stationarity identities used here are derived in
  (1.1)–(5.3), so no external theorem is hidden in the bounds.

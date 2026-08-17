# Prior-art scan: the two sides of the Hecke parameter boundary 

**Scan date:** 2026-08-16  
**Question.** Has the literature treated, as one critical/phase-transition phenomenon, both

* the cofinite branch \(\lambda_q=2\cos(\pi/q)\uparrow2\), where the elliptic order is
  \(q\) (and the usual induced alphabet has the \(\kappa=q-2\) finite part), and
* the free/infinite-volume branch \(w>2\downarrow2\), where fixed-disc transfer-operator
  estimates degenerate,

with the common endpoint the theta group
\(\Gamma_\theta=\langle z\mapsto-1/z,z\mapsto z+2\rangle\), and with a matched
spectral/resonance/determinant statement?

## Conventions and evidentiary rule

Different papers call the parameter \(\lambda\), \(w\), or \(R\).  Here
\(\lambda=w=R=2\) denotes the theta endpoint; \(\lambda_q=2\cos(\pi/q)<2\) is the
cofinite Hecke sequence; and \(w>2\) denotes the non-cofinite/free sequence.  A source
is labelled:

* **(a)** explicit two-sided juxtaposition: it links both one-sided branches at the same
  endpoint and proves a common limiting/phase-transition claim;
* **(b)** one-sided spectral/transfer/metric endpoint result or a partial cross-regime
  overlap; and
* **(c)** adjacent methodology (intermittency, cone degeneration, or determinant
  technology) without the required Hecke two-sided statement.

The entries below report what the source actually states.  “No match found” means no
two-sided theorem was located in the source, not that a negative result is proved.

## Direct Hecke and spectral sources

### 1. Mayer–Mühlenbruch–Strömberg (closest left-limit open-problem reference) — (b)

D. Mayer, T. Mühlenbruch, and F. Strömberg, “The transfer operator for the Hecke
triangle groups,” *Discrete and Continuous Dynamical Systems* 32 (2012), no. 7,
2453–2484, DOI [10.3934/dcds.2012.32.2453](https://doi.org/10.3934/dcds.2012.32.2453),
arXiv [0912.2236](https://arxiv.org/abs/0912.2236).

The paper constructs the finite-q Hurwitz–Nakada/Hecke transfer operator and relates
its Fredholm determinant to Selberg zeta.  Its introduction explicitly says that an
“interesting problem” is the limit as q tends to infinity: the Hecke group tends to
\(\Gamma_\theta\), and the two transfer operators should be related.  Thus it names
the left endpoint and the theta comparison, but leaves the limiting relation as an
open problem; it does not introduce the \(w>2\) branch or a two-sided phase transition.

### 2. Möller–Pohl — (b)

M. Möller and A. D. Pohl, “Period functions for Hecke triangle groups, and the Selberg
zeta function as a Fredholm determinant,” *Ergodic Theory and Dynamical Systems* 33
(2013), 247–283, DOI [10.1017/S0143385711000794](https://doi.org/10.1017/S0143385711000794),
arXiv [1103.5235](https://arxiv.org/abs/1103.5235).

It characterizes Maass cusp forms for every cofinite Hecke triangle group and obtains
the Selberg-zeta/Fredholm-determinant identity through accelerated symbolic dynamics.
This is the finite-q (left) determinant technology; no \(q\to\infty\) plus \(w\downarrow2\)
comparison is made.

### 3. Pohl, unitary representations and the \(\lambda=2\) operator — (b; closest single reference)

A. D. Pohl, “Symbolic dynamics, automorphic functions, and Selberg zeta functions
with unitary representations,” *Contemporary Mathematics* 669 (2016), 205–236,
DOI [10.1090/conm/669](https://doi.org/10.1090/conm/669), arXiv
[1503.00525](https://arxiv.org/abs/1503.00525).

For \(\lambda>2\), Theorem 4.7 proves operator-norm convergence
\(L^{(\lambda)}_{s,\chi}\to L^{(2)}_{s,\chi}\) as \(\lambda\downarrow2\) on a common
pair of function spaces, where the limit is the reduced theta system.  This theorem
concerns the finite-term **slow/reduced** operators, not the nuclear fast operators,
their Fredholm determinants, or Fedosova's Bergman-disc truncations.  The paper also
describes slow/fast systems for cofinite \(\lambda_q<2\), and explicitly says that a
similar cofinite-family convergence result requires a different theta cross-section
and was left to forthcoming work.  It therefore supplies a right-to-theta operator
limit and places both regimes in one framework, but not a proved matched left/right
limit or resonance/determinant theorem.

### 4. Adam–Pohl — (b/c)

A. Adam and A. D. Pohl, “A transfer-operator-based relation between Laplace
eigenfunctions and zeros of Selberg zeta functions,” arXiv [1606.09109](https://arxiv.org/abs/1606.09109).

The paper gives dual slow/fast transfer-operator constructions for finite- and
infinite-area Hecke surfaces and explicitly distinguishes \(\lambda<2\) (cofinite),
\(\lambda=2\) (theta), and \(\lambda>2\) (non-cofinite).  It proves fixed-parameter
operator/eigenfunction correspondences, not continuity across the boundary and not
the proposed two-sided determinant/resonance synthesis.

### 5. Pohl–Wabnitz — (b/c)

A. D. Pohl and P. Wabnitz, “Selberg zeta functions, cuspidal accelerations, and
existence of strict transfer operator approaches,” arXiv [2209.05927](https://arxiv.org/abs/2209.05927).

This develops algorithmic reduction, extension, translation, induction, and
acceleration for geometrically finite non-compact hyperbolic orbisurfaces (including
infinite volume), with nuclear transfer operators whose Fredholm determinant is
Selberg zeta.  It is a general method covering examples on either side, but contains
no parameter-limit theorem at \(\lambda=2\), no q-to-infinity/free matching, and no
claim about a critical phase transition.

### 6. Mayer–Mühlenbruch, nearest \(\lambda_q\)-multiple fractions — (b)

D. Mayer and D. Mühlenbruch, “Nearest \(\lambda_q\)-multiple fractions,” arXiv
[0902.3953](https://arxiv.org/abs/0902.3953).

It treats finite-q nearest-\(\lambda_q\) continued fractions, their natural extension,
geodesic coding, and transfer operators.  This is useful left-branch symbolic prior
art; it does not state a q→∞ endpoint theorem or compare with \(w>2\).

## The cofinite \(q\to\infty\) / elliptic-degeneration side

### 7. Garbin–Jorgenson, spectral asymptotics — (b; exact left endpoint)

D. Garbin and J. Jorgenson, “Spectral asymptotics on sequences of elliptically
degenerating Riemann surfaces,” *L’Enseignement Mathématique* (2) 64 (2018), 161–206,
DOI [10.4171/LEM/64-1/2-7](https://doi.org/10.4171/LEM/64-1/2-7), arXiv
[1603.01494](https://arxiv.org/abs/1603.01494).

The paper treats elliptic orders tending to infinity (cones becoming cusps), including
the Hecke sequence generated by \(z\mapsto-1/z\) and
\(z\mapsto z+2\cos(\pi/N)\), \(3\le N\le\infty\).  It quotes the Hejhal/Selberg
results on accumulation of zeros/poles of the Hecke scattering determinant near the
critical line and proves convergence of suitable Selberg-zeta/small-eigenvalue data
while spectral-zeta and determinant pieces can diverge without regularization.  This
is the exact cofinite-to-theta spectral side; no \(w>2\downarrow2\) side is analyzed.

### 8. Garbin–Jorgenson, heat kernels — (b; exact left endpoint)

D. Garbin and J. Jorgenson, “Heat kernel asymptotics on sequences of elliptically
degenerating Riemann surfaces,” arXiv [1603.01495](https://arxiv.org/abs/1603.01495).

The companion paper proves heat-kernel/trace asymptotics through elliptic degeneration,
including convergence of small eigenvalues and eigenfunctions, and is motivated by
the Hecke q→∞ sequence.  It supplies left-side spectral degeneration only; it does
not mention the free \(w>2\) branch or a two-sided critical law.

### 9. Garbin–von Pippich, elliptic Eisenstein degeneration — (b)

D. Garbin and A.-M. von Pippich, “On the Behavior of Eisenstein Series Through
Elliptic Degeneration,” *Communications in Mathematical Physics* 292 (2009), 511–528,
DOI [10.1007/s00220-009-0892-3](https://doi.org/10.1007/s00220-009-0892-3).

For finite-volume surfaces an elliptic Eisenstein series at a degenerating elliptic
element converges, after an explicit factor, to a parabolic Eisenstein series at the
new cusp.  This is cone-to-cusp (left) asymptotic prior art, not a comparison with
infinite-volume \(w>2\) transfer operators.

### 10. Hejhal, Hecke triangle spectra — (b)

D. A. Hejhal, “Eigenvalues of the Laplacian for Hecke Triangle Groups,” *Memoirs of
the AMS* 97, no. 469 (1992), 165 pp., AMS page
[memo 97-469](https://bookstore.ams.org/memo-97-469), DOI
[10.1090/memo/0469](https://doi.org/10.1090/memo/0469).

This is the foundational computational Selberg-trace/eigenvalue treatment for
cofinite Hecke triangle groups.  The q→∞ scattering accumulation used here is quoted
through Garbin–Jorgenson’s discussion of Hejhal/Selberg results; the memoir itself is
not evidence of a two-sided \(w>2\) boundary theorem.

## The free/infinite-volume \(w\downarrow2\) side

### 11. McMullen, Hausdorff dimension and conformal dynamics III — (b; exact right asymptotic)

C. T. McMullen, “Hausdorff dimension and conformal dynamics III: Computation of
dimension,” *American Journal of Mathematics* 120 (1998), 691–721, DOI
[10.1353/AJM.1998.0031](https://doi.org/10.1353/AJM.1998.0031), author PDF
[dimIII.pdf](https://abel.math.harvard.edu/~ctm/papers/home/text/papers/dimIII/dimIII.pdf).

For the Hecke-commensurable reflection family with \(R=2/r\), Theorem 3.6 gives
\(1-\dim_H(\Lambda_r)\asymp\sqrt{1-r}\) as \(r\to1^-\), and relates the gap to the
ground-state eigenvalue.  Since \(R\to2^+\), this is a sharp one-sided metric/spectral
law at the theta boundary.  It does not juxtapose the cofinite \(\lambda_q\uparrow2\)
sequence and does not analyze fixed-disc truncation errors.

### 12. Soares, Hecke transfer operators and Hausdorff dimension — (b)

L. Soares, “Hecke triangle groups, transfer operators and Hausdorff dimension,”
*Annales Henri Poincaré* 23 (2022), 1239–1281, DOI
[10.1007/s00023-021-01117-1](https://doi.org/10.1007/s00023-021-01117-1), arXiv
[2005.11808](https://arxiv.org/abs/2005.11808).

The introduction records the admissible family \(w=2\cos(\pi/q)\) or \(w\ge2\),
then explicitly restricts the analysis to \(w>2\) (infinite area, with cusp/funnel /
conical geometry).  It constructs the disc transfer operator, Fredholm determinant,
finite-matrix approximations, and asymptotics as \(w\to\infty\).  The shared-family
notation is relevant, but no \(w\downarrow2\) result or left-branch matching appears.

### 13. Fedosova, fixed-disc spectral/dynamical invariants — (b; right error degeneration)

K. Fedosova, “Spectral and dynamical invariants of Hecke triangle groups via transfer
operators,” arXiv [2509.17936](https://arxiv.org/abs/2509.17936).

The paper works only with \(w>2\), using a Bergman-space operator on a fixed unit disc,
\(F_N=\det(1-L_N)\), and gives truncation terms in its equations (8)–(11), including
\(P_N=O\!\left(N^{1/2}(w/2)^{-N}\right)\) and a polylogarithmic factor
\(\operatorname{Li}_{-1/2}(2/w)\).  Consequently the displayed bound loses uniformity
as \(w\downarrow2^+\) (geometric factor tends to one and the polylogarithm diverges),
but the paper does not compare this with q→∞ elliptic degeneration, theta operators,
or resonance convergence.  The last sentence is an inference from the displayed
formulae, not a theorem claimed by Fedosova.

### 14. Naud–Pohl–Soares, fractal Weyl bounds — (b/c)

F. Naud, A. D. Pohl, and L. Soares, “Fractal Weyl bounds and Hecke triangle groups,”
arXiv [1810.04489](https://arxiv.org/abs/1810.04489).

For non-cofinite Hecke groups \(w>2\), it proves growth bounds for Selberg zeta and
fractal-Weyl-type resonance bounds for finite-index torsion-free subgroups.  This is
right-side resonance prior art but contains no \(w\downarrow2\) endpoint theorem and
no cofinite q-sequence comparison.

## Adjacent phase-transition and theta-endpoint literature

### 15. Rugh, intermittency and regularized Fredholm determinants — (c)

H. H. Rugh, “Intermittency and Regularized Fredholm Determinants,” *Inventiones
Mathematicae* 135 (1999), 1–24 (DOI [10.1007/s002220050277](https://doi.org/10.1007/s002220050277)),
arXiv [chao-dyn/9610011](https://arxiv.org/abs/chao-dyn/9610011).

For interval maps with a neutral fixed point it describes continuous spectrum reaching
one, regularized Fredholm determinants on different Riemann sheets, and induced-map
relations.  It is an important analogue for why a parabolic endpoint can destroy
uniform nuclear estimates, but it is not a Hecke \(q/w\) comparison.

### 16. Prellberg–Slawny, indifferent fixed points and phase transitions — (c)

T. Prellberg and J. Slawny, “Maps of Intervals with Indifferent Fixed-Points:
Thermodynamic Formalism and Phase Transitions,” *Journal of Statistical Physics* 66
(1992), 503–514, DOI [10.1007/BF01060077](https://doi.org/10.1007/BF01060077).

It develops pressure singularities, critical exponents, and induced expanding maps for
intermittent systems.  This supplies adjacent thermodynamic language only; it does
not identify the Hecke \(\lambda=2\) boundary or either Hecke spectral branch.

### 17. Kraaikamp–Lopes, theta continued fractions — (c)

C. Kraaikamp and A. Lopes, “The theta group and the continued fraction expansion with
even partial quotients,” *Geometriae Dedicata* 59 (1996), 293–333, DOI
[10.1007/BF00181695](https://doi.org/10.1007/BF00181695).

It studies the theta group, even-partial-quotient coding, geodesic dynamics, and the
associated thermodynamic/Tauberian asymptotics.  This is endpoint dynamics and
intermittency-adjacent context, not a theorem matching \(\lambda_q\uparrow2\) to
\(w\downarrow2\).

### 18. Harmer, triangle-group asymptotics — (c)

M. Harmer, “Asymptotics of the triangle groups and the associated spectra,” Auckland
Department of Mathematics report 523 (2004), PDF
[report 523](https://www.math.auckland.ac.nz/deptdb/department_reports/523.pdf).

For a general triangle-group vertex order tending to infinity it describes convergence
to a non-cocompact cusp and accumulation of eigen-solutions toward continuous
spectrum.  It is useful cone-to-cusp analogy, but it is not the Hecke \(\lambda_q/w\)
two-sided boundary and has no fixed-disc error result.

## Assessment

**Explicit two-sided source (a): not found.**  The scan found no paper that simultaneously
states a cofinite \(q\to\infty\) limit, an infinite-volume \(w\downarrow2^+\) limit, and
a common theta-endpoint theorem for spectra/resonances/Fredholm determinants or for the
Fedosova fixed-disc error.  In particular, no source located a resonance-convergence
statement from the free side to the \(\Gamma_\theta\) spectrum, nor a jointly holomorphic
determinant/error law across \(\lambda=2\).

**What is already owned.**  The left endpoint is well represented by Hejhal and
Garbin–Jorgenson (elliptic order \(q\to\infty\), cones to a cusp, scattering/small
eigenvalue and heat-kernel asymptotics).  The right endpoint is represented by McMullen’s
square-root Hausdorff-dimension/ground-state law and, at the operator level, Pohl’s
Theorem 4.7; Soares and Fedosova provide the free-side transfer-operator setting and
the displayed non-uniform truncation bound.  **Pohl (2016) is the single closest
reference** because it puts the finite- and infinite-area Hecke systems in one framework
and proves the right-to-theta slow-operator limit, while flagging the analogous
cofinite-family result as separate unfinished work.  Mayer–Mühlenbruch–Strömberg is
the closest source on the left-limit problem itself: it explicitly poses the
q→∞ transfer-operator-to-theta comparison.

**Provisional novelty classification.**  The one-sided ingredients are **owned**;
the exact claim that they form a single two-sided critical/phase-transition phenomenon
at \(\Gamma_\theta\), with matched spectral/resonance/determinant/error degeneration,
is **PLAUSIBLY-NEW** (not theorem-grade novelty).  If the proposed claim is weakened to
“both one-sided limits are known,” it is **PARTIALLY-OWNED**.  A proof or publication-level
novelty claim would still require database-level checking and an exact statement of the
operator domain, renormalization, and notion of convergence.

**Search caveat.**  This was a web-only primary/preprint/publisher scan (arXiv, journal or
author PDFs, and publisher pages); MathSciNet/zbMATH and citation-index searches were not
available.  The result is therefore a bounded prior-art boundary, not an exhaustive
bibliographic novelty certification.

# Prior art in certified and validated spectral computation

## Introduction and scope

This survey asks a narrow methodological question: how much prior art exists for a certificate that (i) evaluates a finite-dimensional determinant with outward-rounded interval/ball arithmetic on a complete closed contour, (ii) obtains an integer zero count from its winding number, and (iii) transfers that count to an infinite-dimensional Fredholm determinant using a proven, parameter-uniform nuclear/trace-class truncation bound. The target application is a holomorphic transfer-operator family for a Fuchsian/Hecke group.

The comparison baseline is the repository's q=5 pipeline as documented in `research_notes/rh_goals_2026-08-14/lane_g/R3B_FLAGSHIP_CERT.md`: python-flint Arb/Acb arithmetic, a closed rectangular parameter box of coordinate half-width \(10^{-6}\), a finite-cover winding of one, and a stated input tail bound \(T_{\rm tail}(160)=6.26785788\ldots\times 10^{-22}\). This survey does **not** independently re-prove that certificate. It also preserves the repository's stated scope boundary: the closed-contour determinant computation is distinct from the remaining operator-identification and Selberg-zeta factorization steps. Accordingly, “ours” below means the **methodological package just described**, not an unconditional assertion that every link from the computed determinant to a resonance has already been discharged.

“Certified” or “verified” here means a mathematically justified enclosure or count incorporating rounding error and the relevant discretization/truncation error. A small residual, solver tolerance, mesh-convergence plot, or the word “rigorous” meaning “derived from the governing PDE” is not enough.

The search emphasized primary papers, authors' software pages, official repositories, and vendor documentation. It was broad enough to support a classification, but it is not a proof of bibliographic nonexistence. In particular, an absolute novelty claim would require a systematic MathSciNet/zbMATH/INSPEC and citation-network search.

## INTLAB and Rump's verified matrix eigensolvers

### Capability

Siegfried Rump's INTLAB is a MATLAB/Octave toolbox for reliable computing. Its official feature list includes verified matrix factorizations (`eig`, `schur`, `svd`, and others), eigenvalue problems involving simple eigenvalues and clusters, inner inclusions, and structured matrices. Rump's eigenvalue work supplies residual- and interval-linear-algebra-based enclosures for eigenvalues, eigenvectors/invariant subspaces, and clusters of a **finite matrix**, including difficult clustered or multiple cases.

### Sources

- S. M. Rump, [INTLAB — INTerval LABoratory](https://www.tuhh.de/ti3/intlab/), official software page; canonical software citation: *Developments in Reliable Computing* (1999), pp. 77–104.
- S. M. Rump, [“Computational error bounds for multiple or nearly multiple eigenvalues”](https://www.tuhh.de/ti3/paper/rump/Ru99c.pdf), *Linear Algebra and its Applications* 324 (2001), 209–226.
- S. M. Rump, [“Verification methods: Rigorous results using floating-point arithmetic”](https://doi.org/10.1017/S096249291000005X), *Acta Numerica* 19 (2010), 287–449.

### Comparison with ours

INTLAB directly covers the finite-matrix verification layer that appears inside our computation. It can certify that a computed eigenpair or cluster belongs to a given finite matrix, and its interval primitives can support determinant/nonvanishing tests. It does **not by itself** prove that the spectrum or Fredholm determinant of an infinite-dimensional transfer operator is close to that of the chosen truncation. That operator-specific tail theorem is the decisive extra obligation in our setting. Nor is a closed-contour argument-principle count the characteristic INTLAB eigenvalue interface: the usual output is a local enclosure of matrix eigenvalues/eigenvectors or invariant subspaces.

Thus INTLAB makes outward-rounded finite spectral verification commodity technology, but it does not commoditize the nuclear-operator bridge or the Hecke/Fuchsian application.

## ValEncIA-IVP, the kv library, and VCP

### Capability

The names in this family should not be conflated.

**ValEncIA-IVP** is a validated initial-value-problem solver developed for guaranteed state enclosures of ODEs with uncertain parameters. Published ValEncIA work uses real or complex interval arithmetic and eigen-decompositions to construct exponential enclosures, including cases with multiple conjugate complex eigenvalues. That makes eigenstructure part of its enclosure machinery; it is not, on the sources found, a general package whose main product is certified spectral localization.

**kv** is Masahide Kashiwagi's header-only C++ library for verified numerical computation. Its documented foundation is directed-rounding interval arithmetic, with nonlinear-equation, ODE, automatic-differentiation, affine-arithmetic, and numerical-linear-algebra components. The official documentation expressly warns that using `interval.hpp` with ordinary doubles without the rounding-control header gives unverified results.

**VCP** is a C++ library for computer-assisted PDE proofs built on kv. Its official description provides a common matrix interface for ordinary floating point, BLAS/LAPACK, and kv interval arithmetic, together with Fourier and PDE-verification facilities.

### Sources

- A. Rauh et al., [“Exponential Enclosure Techniques for Initial Value Problems with Multiple Conjugate Complex Eigenvalues”](https://www.informatik.uni-wuerzburg.de/fileadmin/10030000/scan2014/talks/C2_2_update2.pdf), SCAN presentation describing ValEncIA-IVP's validated IVP role and eigenvalue-based exponential enclosures.
- M. Kashiwagi, [kv — a C++ Library for Verified Numerical Computation](https://verifiedby.me/kv/index.html), official project page and repository link.
- M. Kashiwagi, [kv interval arithmetic documentation](https://verifiedby.me/kv/interval/index-e.html), especially the rounding-mode requirements.
- [VCP Library](https://verified.computation.jp/), official project page.

### Comparison with ours

kv can play essentially the same arithmetic-infrastructure role as Arb/Acb, while VCP supplies reusable machinery for finite/infinite decompositions in PDE proofs. ValEncIA illustrates rigorous propagation of sets through time. None of these sources presents the full combination of a Fredholm determinant on a complex parameter contour, an interval-certified winding count, and a nuclear transfer-operator tail bound. They are enabling validated-numerics platforms, not direct anticipation of the target certificate.

The survey found no primary source for a distinct spectral package named simply **“ValEncIA”** that offers general eigenvalue enclosures comparable to INTLAB. The identifiable project is ValEncIA-IVP. Any stronger characterization would be unsupported.

## Arb/Acb and Johansson's rigorous computations

### Capability

Fredrik Johansson's Arb (now integrated into FLINT) implements arbitrary-precision real ball arithmetic and Acb complex rectangular balls, with polynomial/power-series, special-function, integration, and matrix operations. Ball semantics guarantee enclosure of the exact result when the documented hypotheses hold. Arb has been used for rigorous high-precision evaluations of special functions and zeta functions; Johansson's Hurwitz-zeta work includes rigorous error bounds and record computations involving zeta zeros. Arb/Acb also contains a verified finite-matrix eigenpair routine: given an approximate eigenpair, it returns an enclosure guaranteed to contain at least one eigenvalue and a corresponding eigenvector enclosure.

### Sources

- F. Johansson, [“Arb: Efficient Arbitrary-Precision Midpoint-Radius Interval Arithmetic”](https://doi.org/10.1109/TC.2017.269063), *IEEE Transactions on Computers* 66 (2017), 1281–1292.
- [Arb feature overview](https://fredrikj.net/arb/overview.html) and [ball semantics/usage guide](https://fredrikj.net/arb/using.html), official documentation.
- [Arb/FLINT `acb_mat` documentation](https://arblib.org/acb_mat.html), verified eigenvalue/eigenvector enclosure API.
- F. Johansson, [“Rigorous high-precision computation of the Hurwitz zeta function and its derivatives”](https://arxiv.org/abs/1309.2877), *Numerical Algorithms* 69 (2015), 253–270.

### Comparison with ours

Arb is the arithmetic engine, not the operator theorem. It rigorously propagates rounding and evaluation error but does not automatically invent a uniform truncation bound, prove nuclearity, relate a matrix determinant to a Fredholm determinant, or establish that a contour avoids zero. Those are supplied by the application code and analysis. Our use of Arb/Acb is therefore not itself novel. The possible novelty lies in the certified analytic envelope and its assembly with a contour count for this transfer-operator family.

## General rigorous argument-principle zero enclosure

### Capability

Validated zero counting by the argument principle is established prior art. Petković and Petković give a rigorous adaptive method for enclosing all zeros of an analytic function in a rectangle. It uses interval arithmetic to enclose the contour integral of \(f'/f\), thereby certifying the number of enclosed zeros, and refines rectangles to localize them. The paper explicitly discusses the argument principle, guaranteed quadrature error, simple zeros, and clusters.

### Source

- M. S. Petković and L. D. Petković, [“Enclosing all zeros of an analytic function — A rigorous approach”](https://doi.org/10.1016/j.cam.2008.10.014), *Journal of Computational and Applied Mathematics* 228 (2009), 418–423.

### Comparison with ours

This is the clearest prior art against any claim that “certified winding on a closed contour” is new. It is not. The material difference is the function being counted. Petković–Petković assume access to a rigorously evaluable analytic function. For our Fredholm determinant, the implemented function is a finite determinant, so a separate operator-level inequality must prove that its contour image can be homotoped to the true infinite-dimensional determinant without crossing zero. The argument-principle layer is known; the proven nuclear-tail bridge is the specialized layer.

## Certified Laplace and PDE eigenvalues: Nakao, Plum, Oishi, Liu

### Capability

The Nakao–Plum–Oishi school has a mature theory of verified PDE computation. Typical methods split a Hilbert-space problem into a finite-element part and an infinite-dimensional complement, derive explicit projection and inverse-operator bounds, and use interval arithmetic plus fixed-point, Lehmann/Goerisch, Rayleigh–Ritz, or complementarity arguments. These methods can provide upper and lower enclosures for eigenvalues of elliptic operators and can certify exclusion of spectrum from intervals.

Liu and Oishi's polygonal-domain method computes leading Laplacian eigenvalue bounds by conforming/nonconforming FEM and sharpens them with Lehmann's theorem. Nagatou, Plum, and Nakao give a rigorous method that excludes eigenvalues from subregions of spectral gaps for a perturbed periodic Schrödinger operator. Sekine, Nakao, and Oishi formulate an infinite-dimensional Newton operator as finite and infinite blocks, an especially close conceptual analogue to “finite computation plus analytic tail,” though their target is PDE solution verification rather than a determinant winding.

### Sources

- X. Liu and S. Oishi, [“Verified eigenvalue evaluation for the Laplacian over polygonal domains of arbitrary shape”](https://arxiv.org/abs/1204.4119), *SIAM Journal on Numerical Analysis* 51 (2013), 1634–1654.
- K. Nagatou, M. Plum, and M. T. Nakao, [“Eigenvalue excluding for perturbed-periodic one-dimensional Schrödinger operators”](https://doi.org/10.1098/rspa.2011.0159), *Proceedings of the Royal Society A* 468 (2012), 545–562.
- K. Sekine, M. T. Nakao, and S. Oishi, [“A new formulation for the numerical proof of the existence of solutions to elliptic problems”](https://arxiv.org/abs/1910.00759), *Numerische Mathematik* 146 (2020), 615–647.
- S. M. Rump, [“Verification methods: Rigorous results using floating-point arithmetic”](https://doi.org/10.1017/S096249291000005X), *Acta Numerica* 19 (2010), for a broad verified-computation framework including infinite-dimensional problems.

### Comparison with ours

This literature strongly anticipates the **architecture** of our proof: a numerical finite core plus a theorem controlling the infinite complement. It is more than mere rounding-error control. But the spectral objects and proof mechanisms differ. Self-adjoint elliptic PDEs permit variational ordering, min–max principles, complementarity estimates, and real spectral gaps; our transfer-operator family is complex, non-self-adjoint, holomorphic in \(s\), and accessed through a Fredholm determinant. Our contour winding is a natural replacement for eigenvalue ordering, while the nuclear/trace tail replaces FEM projection-error machinery.

Consequently, “finite approximation plus proven infinite tail” is established methodology. Its realization for a holomorphic nuclear transfer operator and a complex zero count is a specialized adaptation, not a wholly new philosophy.

## Dahne–Salvy and related computer-assisted spectral geometry

### Capability

Joel Dahne and Bruno Salvy rigorously enclosed Laplace–Beltrami eigenvalues on spherical triangles to very high precision. Their method of particular solutions uses high-precision interval arithmetic and Taylor models; domain monotonicity certifies the eigenvalue's index, and multiple local expansions handle singular corners. This is a genuine certified spectral computation, including discretization/analytic remainder control rather than only a finite-matrix residual.

Javier Gómez-Serrano's survey documents a broader computer-assisted-proof culture for PDEs, emphasizing exact analytic reductions, interval arithmetic, and explicit finite/infinite estimates. Alberto Enciso and Gómez-Serrano's “Spectral determination of semi-regular polygons” is a rigorous inverse-spectral theorem, but it is analytic rather than a validated numerical eigenvalue-localization algorithm and should not be presented as one.

### Sources

- J. Dahne and B. Salvy, [“Computation of Tight Enclosures for Laplacian Eigenvalues”](https://arxiv.org/abs/2003.08095), *SIAM Journal on Scientific Computing* 42 (2020), A3210–A3232, DOI [10.1137/20M1326520](https://doi.org/10.1137/20M1326520).
- J. Gómez-Serrano, [“Computer-assisted proofs in PDE: a survey”](https://arxiv.org/abs/1810.00745), *SeMA Journal* 76 (2019), 459–484.
- A. Enciso and J. Gómez-Serrano, [“Spectral determination of semi-regular polygons”](https://arxiv.org/abs/1709.05960), *Journal of Differential Geometry* 122 (2022), 273–298.

### Comparison with ours

Dahne–Salvy is close in epistemic standard: interval arithmetic plus explicit treatment of the continuum problem produces a theorem-quality localization, not a convergence heuristic. The differentiator is again structural. Their eigenvalues are real, self-adjoint PDE eigenvalues, and their index certificate uses domain monotonicity. Ours counts complex zeros via the argument principle and requires determinant perturbation bounds for a nuclear operator. Neither dominates the other; they instantiate different certification theorems around a finite numerical core.

The task prompt also named “Barrera-Vega.” Searches of the exact hyphenated and unhyphenated name did not identify a relevant author, package, or paper in certified spectral computation. It may be a misspelling or a conflation of two authors. No claim about that purported item is made here.

## Rigorous and non-rigorous resonance computation in scattering

### Capability

Bindel and Zworski's online text and MATLAB examples explain resonances as scattering-matrix poles and nonlinear eigenvalues, and develop practical computations for one-dimensional Schrödinger scattering, absorbing layers, and nonlinear matrix functions. Bindel and Hood later proved localization theorems for analytic nonlinear matrix eigenvalue problems generalizing Gershgorin, Bauer–Fike, and pseudospectral inclusions; a quantum-resonance example is included. These are rigorous perturbation/localization theorems for a finite analytic matrix-valued function.

The broader scattering literature computes resonances with complex scaling, perfectly matched layers, absorbing potentials, boundary elements, or transfer matrices. Nannen and Wess, for example, explicitly analyze spurious resonances from PML discretization. Such work is mathematically sophisticated but should not automatically be called validated numerics: absent interval enclosures and an a posteriori discretization theorem, computed poles remain approximations.

### Sources

- D. Bindel and M. Zworski, [*Theory and Computation of Resonances in 1D Scattering*](https://www.cs.cornell.edu/~bindel/cims/resonant1d/), 2006 lecture notes and MATLAB codes.
- D. Bindel and A. Hood, [“Localization Theorems for Nonlinear Eigenvalue Problems”](https://doi.org/10.1137/15M1026511), *SIAM Review* 57 (2015), 585–607.
- M. Zworski, [“Quantum resonances and partial differential equations”](https://arxiv.org/abs/math/0304400), survey of the analytic resonance framework.
- L. Nannen and M. Wess, [“Computing scattering resonances using perfectly matched layers with frequency dependent scaling functions”](https://doi.org/10.1007/s10543-018-0694-0), *BIT Numerical Mathematics* 58 (2018), 373–395.

### Comparison with ours

This literature shows that complex resonances, analytic nonlinear eigenvalue problems, and contour or perturbative localization are established. Bindel–Hood is particularly relevant to finite analytic matrix pencils. What was not found in these sources is the exact certificate chain used here: a ball-arithmetic winding of a truncated Fredholm determinant plus a proven trace/nuclear tail uniform over every point of the contour. Scattering discretizations face an analogous “finite artificial problem versus true open-system resonance” bridge, but generally solve it through convergence theory, pollution analysis, or perturbation bounds rather than an interval Fredholm-determinant homotopy.

## Transfer operators, Selberg zeta, and rigorous dynamical numerics

### Capability

Transfer-operator/Fredholm-determinant representations of dynamical and Selberg zeta functions are classical. For Hecke triangle groups specifically, Strömberg implemented numerical computation of Selberg zeta functions using transfer operators. Mayer, Mühlenbruch, and Strömberg developed the transfer-operator factorization relating Hecke-triangle Selberg zeta functions and Laplace eigenfunctions. These sources establish the analytic object and the numerical route, but they do not advertise interval-certified boxes with full truncation-tail/winding receipts.

Rigorous numerical dynamics also uses determinant truncations and explicit error estimates to bound transfer-operator spectra and dynamical quantities. This reinforces that determinant approximation with analytic remainder control is known in the transfer-operator world, even though the exact Hecke resonance certificate searched for here was not located.

### Sources

- F. Strömberg, [“Computation of Selberg zeta functions on Hecke triangle groups”](https://arxiv.org/abs/0804.4837), *Experimental Mathematics* 18 (2009), 197–214.
- D. Mayer, T. Mühlenbruch, and F. Strömberg, [“The transfer operator for the Hecke triangle groups”](https://arxiv.org/abs/0912.2236), *Discrete and Continuous Dynamical Systems* 32 (2012), 2453–2484.
- M. Pollicott, [“A dynamical approach to validated numerics”](https://warwick.ac.uk/fac/sci/maths/people/staff/mark_pollicott/p3/twenty10..pdf), expository account of rigorous bounds from transfer operators and determinant truncations.

### Comparison with ours

This is the nearest application-level prior art. The transfer operator, nuclear/Fredholm determinant, and Hecke-triangle Selberg-zeta connection are known; numerical determinant truncation is known; rigorous error bounds in transfer-operator computations are known; and validated argument-principle counting is known. The apparent contribution is their **end-to-end assembly** into a replayable, interval-certified complex localization for a particular Hecke-group determinant, with a contour-uniform nuclear tail small enough to preserve winding. That points toward a novel application and implementation of known methodology, not a new underlying theorem schema.

## Industrial photonics, MEMS, structural, and acoustic tools

### Capability claimed by vendors

Commercial multiphysics and photonics systems—including COMSOL, Ansys Mechanical, and Ansys/Lumerical MODE—routinely compute eigenfrequencies, damped modes, waveguide modes, and resonances. Their documentation provides solver tolerances, residual/convergence controls, mesh studies, mode-completeness diagnostics, and in some cases checks against missing modes. These are valuable engineering assurance mechanisms.

However, vendor use of **rigorous** commonly means that the numerical method is based on the full Maxwell equations or becomes exact in a limiting discretization, not that the displayed eigenvalue is accompanied by an outward-rounded theorem-level interval including all floating-point and truncation errors. Ansys's EME documentation is explicit that the exact basis is infinite and recommends convergence testing. Its Supernode documentation supplies expected percentage errors and warns that accuracy depends on settings. COMSOL recommends repeated solves, tighter tolerances, and mesh refinement for nonlinear eigenfrequencies.

### Sources

- Ansys Optics, [“EME Convergence Testing — An Intuitive Approach”](https://optics.ansys.com/hc/en-us/articles/4412892724243-EME-Convergence-Testing-An-Intuitive-Approach).
- Ansys Mechanical, [“Eigenvalue and Eigenvector Extraction”](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ans_thry/thy_tool13.html), including Supernode accuracy guidance and Sturm checks.
- COMSOL, [“Eigenfrequency Analysis”](https://doc.comsol.com/6.4/doc/com.comsol.help.rf/rf_ug_modeling.05.37.html), including nonlinear eigenfrequency linearization and iteration guidance.
- COMSOL, [“Solving Eigenvalue Problems”](https://doc.comsol.com/6.3/doc/com.comsol.help.comsol/comsol_ref_equationbased.32.012.html), including Taylor linearization of nonlinear eigenvalue dependence.

### Comparison with ours

No surveyed industrial package was found to make the same theorem-grade claim as our target pipeline. The commercial tools solve much larger multiphysics models and provide excellent practical error diagnostics, but their normal eigenmode outputs are not interval enclosures of the continuum spectrum backed by a proven infinite-dimensional tail. A Sturm count on a discretized symmetric matrix may certify completeness for that matrix or search interval; it does not by itself certify the underlying PDE eigenvalues. On the evidence found, there is no commodity industrial analogue of the full closed-contour-plus-nuclear-tail certificate.

This is a bounded negative finding, not proof that no specialist commercial or proprietary validated solver exists.

## Comparison table

| Prior art | Certified object | Handles continuum/infinite dimension? | Complex contour count? | Proven truncation/discretization bridge? | Relation to ours |
|---|---|---:|---:|---:|---|
| INTLAB / Rump | Finite matrix eigenvalues, eigenvectors, clusters, invariant subspaces | No, unless the user supplies a separate theorem | Not its standard eigensolver output | Finite rounding/residual error only | Commoditizes the finite verified-linear-algebra layer |
| ValEncIA-IVP | Guaranteed ODE state tubes | Time-continuous IVPs, via validated integration | No spectral zero count | Yes for IVP propagation under its hypotheses | Adjacent validated numerics; not a direct eigensolver precedent |
| kv / VCP | Interval arithmetic and PDE-proof building blocks | Yes, in application-specific VCP proofs | Not a standard Fredholm winding workflow | User/application supplies analytic complement bounds | Alternative infrastructure to Arb and custom PDE proof frameworks |
| Arb/Acb | Rigorous real/complex function, polynomial, matrix evaluations; finite eigenpair enclosure | No automatic operator bridge | Can support it, but user implements the certificate | No automatic nuclear tail | Arithmetic engine used by ours; not the methodology by itself |
| Petković–Petković | Number and enclosures of zeros of an analytic function | Only insofar as the function is rigorously evaluable | **Yes** | Function-evaluation error is enclosed; no operator truncation theorem | Direct precedent for certified argument-principle counting |
| Nakao / Plum / Oishi / Liu | Elliptic and Schrödinger PDE eigenvalue bounds and exclusion regions | **Yes** | Usually no; largely self-adjoint real spectra | **Yes**, via FEM/projection/inverse bounds | Strong precedent for finite core plus infinite complement |
| Dahne–Salvy | Tight Laplace–Beltrami eigenvalue enclosures and certified index | **Yes** | No; real self-adjoint eigenvalue | **Yes**, Taylor models and analytic/domain bounds | Same epistemic standard, different spectral geometry |
| Bindel–Hood / scattering numerics | Finite nonlinear eigenvalue localization; approximate scattering resonances | Sometimes, through separate convergence analysis | Analytic matrix methods, but not an interval Fredholm winding receipt | Varies; usually not validated end to end | Strong adjacent precedent for complex resonances and nonlinear pencils |
| Hecke transfer-operator literature | Selberg zeta via nuclear transfer operators; numerical zeta/resonance approximations | **Yes**, analytically | Numerical zero searches; no matching interval certificate found | Analytic nuclearity and numerical truncation methods exist | Closest application background; ours adds end-to-end validated localization |
| COMSOL / Ansys / Lumerical | Engineering eigenmodes/eigenfrequencies/resonances | Discretized PDE models | Some contour/search algorithms internally | Convergence/tolerance diagnostics, not normally theorem-level enclosures | Industrially mature approximation, not a commodity certificate |

## Honest verdict

**Best classification: a novel application and end-to-end assembly of known methodologies, not a fundamentally novel methodology and not a commodity technique.**

The individual ingredients are unmistakably prior art:

1. interval/ball arithmetic and verified finite-matrix eigensolvers are mature (INTLAB, kv, Arb);
2. certified argument-principle zero counting on closed contours is published methodology (Petković–Petković);
3. finite-dimensional approximation plus a proven infinite-dimensional complement is central to verified PDE spectral computation (Nakao/Plum/Oishi/Liu and Dahne–Salvy);
4. analytic nonlinear eigenvalue and resonance localization is established (Bindel–Hood and scattering numerics); and
5. nuclear transfer operators and Fredholm determinants for Hecke-triangle Selberg zeta functions, including numerical computation, are established (Strömberg; Mayer–Mühlenbruch–Strömberg).

For that reason, it would be overstated to market “argument principle + interval arithmetic + tail bound” as a new general methodology. The high-level proof pattern is an expected synthesis of validated numerics, Rouché/homotopy stability, and operator approximation.

What the surveyed literature did **not** reveal is a prior implementation that simultaneously provides, for a Fuchsian/Hecke transfer operator, a complete outward-rounded cover of a closed complex contour, an integer winding certificate for the finite determinant, a parameter-uniform nuclear/trace truncation estimate, and a homotopy transferring that winding to the infinite Fredholm determinant, yielding a small certified resonance/zeta-zero box. If the repository's remaining operator-identification/factorization obligations are closed, that combination is plausibly publication-worthy as a **novel certified application and computational proof pipeline**.

The word “novel” should therefore be attached narrowly:

- **Not novel:** interval evaluation, finite determinant winding, Rouché/homotopy, trace-class determinant perturbation, or analytic truncation bounds considered separately.
- **Plausibly novel:** the concrete quantitative realization and machine-checkable assembly for the specified Hecke/Fuchsian transfer operator, especially at the reported box and tail scale.
- **Not established by this survey:** absolute priority, the validity of every repository proof link, or novelty of the underlying Selberg-zeta/transfer-operator representation.

The defensible external claim is: **“We give a validated-numerics realization of known Fredholm-determinant and argument-principle ideas that appears to be the first rigorous, contour-certified localization of this kind for Hecke-triangle transfer operators.”** Until a formal database-level literature review and the remaining identification gates are complete, “appears to be” is essential.

# Public-repository design for a certified spectral computation engine

Date: 2026-08-16  
Scope: downloadable prior art, plausible users, publication form, v1 boundary, and repository name.  
Method note: the negative claims below are bounded by searches of official project pages, repositories, documentation, and primary papers. They are not claims of bibliographic nonexistence. The local baseline `PRIOR_ART_CERTIFIED_SPECTRAL.md` was read first and is not reproduced here.

## 1. Gaps: what researchers can download today

### What is actually available

| Tool/ecosystem | Downloadable capability | License/access | What it does **not** supply |
|---|---|---|---|
| **INTLAB** | MATLAB/Octave interval arithmetic; verified linear algebra including simple and clustered eigenvalue problems, inner inclusions, structured matrices; verified nonlinear systems through `verifynlss`. | Downloadable for private, purely academic, and internal company use. Embedding INTLAB in a commercial product requires a special license. This is source-available academic software, not an ordinary OSI-style permissive dependency. [Official INTLAB page](https://www.tuhh.de/ti3/intlab/) | No standard interface that takes an analytic Fredholm determinant, certifies its winding on a closed contour, and transfers the count through an operator-specific truncation theorem. `verifynlss` verifies a local finite-dimensional nonlinear-system solution; it is not an argument-principle all-zero counter. |
| **kv** | Header-only C++ library for verified numerics: directed-rounding intervals, nonlinear equations, ODEs, automatic differentiation, quadrature, and numerical linear algebra. Current source and tarballs are public. | Public source at [mskashi/kv](https://github.com/mskashi/kv); the official distribution includes `LICENSE.txt` and downloadable releases. [Official project page](https://verifiedby.me/kv/index-e.html) | Arithmetic and proof-building primitives, not a ready certified resonance/Fredholm-determinant application. No documented portable winding certificate or transfer-operator tail proof. |
| **FLINT/Arb and python-flint** | Arbitrary-precision real balls (`arb`) and complex balls (`acb`), matrices, rigorous complex integration, polynomial root isolation, and verified finite-matrix eigenvalue enclosures. The C `acb_calc_integrate` routine returns a rigorous enclosure when it succeeds; FLINT examples include rigorous polynomial and zeta-zero computations. | FLINT/Arb LGPL-2.1-or-later; python-flint MIT; python-flint publishes wheels/releases and is directly usable from Python. [FLINT Arb documentation](https://flintlib.org/doc/index_arb.html), [`acb_calc`](https://arblib.org/acb_calc.html), [python-flint](https://github.com/flintlib/python-flint) | Arb is an arithmetic kernel, not a turnkey spectral certificate system. Its generic complex calculus is documented as experimental, and its examples do not provide an operator-tail theorem or a domain-specific certificate/checker protocol. |
| **JuliaIntervals** | `IntervalArithmetic.jl` supplies IEEE-1788-style interval arithmetic; `IntervalLinearAlgebra.jl` documents enclosure of eigenvalues of interval matrices and verified eigenpairs of floating-point matrices; `IntervalRootFinding.jl` covers rigorous finite-dimensional root isolation. | Open Julia packages installed with `Pkg.add`; active core ecosystem. [JuliaIntervals overview](https://juliaintervals.github.io/), [IntervalLinearAlgebra.jl](https://juliaintervals.github.io/IntervalLinearAlgebra.jl/) | No identified Julia package combines complex-contour winding certification with an infinite-dimensional Fredholm/transfer-operator tail theorem. The linear-algebra package verifies finite matrices. |
| **ValidatedNumerics.jl** | Historical Julia meta-package for interval arithmetic, root finding, optimization, constraints, and Taylor models. | Public repository, but archived read-only on 2025-11-26; its README directs users to `IntervalArithmetic.jl` and the component packages. [Repository](https://github.com/JuliaIntervals/ValidatedNumerics.jl) | It is no longer the ecosystem entry point and never appears to have been a specialized spectral/resonance certificate engine. |
| **SpecSolve** | Public MATLAB research software for computing spectral measures of self-adjoint operators, designed to avoid spectral pollution and compute spectral information without conventional finite-section failure. [Paper: Colbrook, Horning, Townsend, 2021/2022](https://arxiv.org/abs/2006.01766) | Public research code under the [SpecSolve organization](https://github.com/SpecSolve). | “Solve the problem correctly in the SCI hierarchy” is not the same as outward-rounded proof certification. The cited paper reports high-accuracy numerical computation; it does not define interval certificates, closed-contour winding receipts, or proof-carrying tail bounds. |
| **EigTool** | Free MATLAB GUI/package for matrix pseudospectra and an interface to `eigs`/ARPACK; downloadable version 2.1 beta (2009). [Official page](https://www.cs.ox.ac.uk/pseudospectra/eigtool/) | Free download; the official page gives an “as is” disclaimer but no claim of validated numerics. | Numerical pseudospectral visualization, not rigorous enclosure. It neither controls all rounding/discretization error nor proves infinite-dimensional spectral statements. |
| **cxroots** | Pip-installable Python package that counts and locates roots of a scalar analytic function inside user contours using numerical contour quadrature plus Newton/Muller refinement. [Documentation](https://rparini.github.io/cxroots/) | Public Python package/repository. | **Not a rigorous certificate tool.** Its documentation uses NumPy/SciPy quadrature, permits numerical derivative approximation, assumes no contour zeros/poles, and describes counts as approximations. It supplies neither interval enclosures nor a proved quadrature/nonvanishing certificate. “Reliability” checks and contour subdivision do not change that status. |
| **Rump `verifynlss`** | INTLAB routine that verifies a local inclusion for a finite-dimensional nonlinear system using interval/Krawczyk-type machinery; sparse variants are documented. [Official demo](https://www.tuhh.de/ti3/rump/intlab/demos/html/dsparse.html) | Part of INTLAB and therefore under INTLAB’s access/license terms. | It needs an approximate solution and a finite nonlinear system. It does not count all zeros of an analytic scalar function in a contour and does not bridge an operator truncation. |

Two nearby but different categories are worth keeping visible:

- Petković and Petković, “Enclosing all zeros of an analytic function — A rigorous approach” (2009), gives rigorous argument-principle rectangle subdivision with interval arithmetic. This defeats any novelty claim for certified argument-principle zero counting itself, but the paper is an algorithm paper, not a maintained Python package with portable proof receipts. [DOI](https://doi.org/10.1016/j.cam.2008.10.014)
- Borthwick’s numerical Selberg-zeta computations use transfer-operator/Fredholm-determinant expansions with mathematically established coefficient decay, but the published computation is a numerical experiment rather than an outward-rounded, machine-checkable contour certificate. [“Distribution of resonances for hyperbolic surfaces”](https://arxiv.org/abs/1305.4850)

### The actual open-source gap

I found public components for every *separate* layer:

1. validated arithmetic and finite-matrix eigenpairs (INTLAB, kv, Arb, JuliaIntervals);
2. numerical contour root counting (`cxroots`);
3. rigorous argument-principle algorithms in papers (Petković–Petković);
4. operator-specific spectral approximation theory (for example, Bandtlow–Slipantschuk’s exponential approximation results for holomorphic transfer operators); and
5. numerical resonance packages (Bindel–Zworski tutorial code and PyZeta).

I did **not** identify a usable public open-source tool that accepts a holomorphic transfer-operator family, proves or consumes a parameter-uniform nuclear/trace-class truncation bound, evaluates the finite determinant with outward rounding on a certified complete contour cover, proves a winding number, and emits a portable independently checkable certificate. This is a bounded search conclusion, not an absolute nonexistence theorem. It is also narrower and more defensible than “the first certified resonance code”: validated PDE eigenvalue and resonance methods exist in the literature, and general certified zero counting is prior art.

The restored local code confirms why the distinction matters. `.worktrees/aletheia-restore/code/zeta_cert_rosen_q5.py` extrapolates a geometric “dimension tail” from a short window of observed determinant increments and samples corners/center to claim uniformity; the repository’s later adversarial review records that this extrapolation can be non-monotone and is not a proof. The later R2/R3b path instead binds separately derived tail receipts and covers complete closed sub-arcs by Arb/Jacobi bounds. Public v1 must contain only the latter kind of theorem-backed bridge; it must not export the older heuristic under a `certified` API.

**Recommendation:** Build specifically around the unfilled integration layer—proof-backed operator-tail adapters + certified closed-contour winding + portable receipts—and position Arb, INTLAB, JuliaIntervals, and rigorous argument-principle papers as enabling prior art, not competitors that the project supposedly supersedes.

## 2. Audience and demand

### Primary users, in adoption order

1. **Validated numerics and computer-assisted-proof researchers.** The most direct current demand signal is the ICMS workshop “Validated Numerics for Computer-Assisted Proofs” (Edinburgh, 6–10 July 2026), organized by Andrew Burbanks, Ben Mestel, Mark Pollicott, and Julia Slipantschuk. Its stated goals include comparing software platforms, discussing common standard features, forming a special-interest group, and planning collaboration for the next 10–15 years. [Workshop site](https://vncap.org/). The SCAN series—*International Symposium on Scientific Computing, Computer Arithmetic, and Validated Numerics*—is the established specialist venue; the proceedings index documents the series and its scope. [DBLP SCAN series](https://dblp.org/db/conf/scan/index.html). Related active communities include the GAMM activity group on computer-assisted proofs and symbolic computation. [Official group page](https://www2.math.uni-wuppertal.de/wrswt/gamm/)

   Their standard proof pattern is already compatible with this project: approximate first, then validate using interval arithmetic, a finite/infinite decomposition, explicit norms, and a fixed-point/Krawczyk/Rouché-type theorem. What is usually missing is a reusable artifact boundary between the expensive producer and a small checker. These users would understand and critique tail assumptions immediately.

2. **Transfer-operator and dynamical-systems CAP groups.** Pollicott and Slipantschuk’s “Effective estimates of ergodic quantities illustrated on the Bolyai–Rényi map” (2024) develops rigorous high-precision estimates for top transfer-operator eigenvalues. [Paper](https://arxiv.org/abs/2308.04293). Bandtlow and Slipantschuk’s “Lagrange approximation of transfer operators associated with holomorphic data” (2020/2021) proves exponential convergence of finite-rank approximants for holomorphic transfer operators. [Paper](https://arxiv.org/abs/2004.03534). These are unusually close methodological neighbors: they use analytic contraction/approximation theorems plus finite computation rather than treating a large matrix as the operator. The 2026 ICMS organizer list also shows this community is actively considering shared platforms.

3. **Hyperbolic dynamics, spectral geometry, and quantum-chaos numerical researchers.** David Bindel and Maciej Zworski’s public “Theory and Computation of Resonances in 1D Scattering” includes MATLAB codes and formulates resonances as nonlinear eigenproblems. [Site](https://www.cs.cornell.edu/~bindel/cims/resonant1d/). David Borthwick computes resonances of geometrically finite hyperbolic surfaces as zeros of Selberg zeta using transfer-operator expansions and studies fractal Weyl laws and gaps. [Paper](https://arxiv.org/abs/1305.4850). Tobias Weich’s active spectral-analysis group explicitly spans spectral geometry, dynamical systems, mathematical physics, and resonances. [Group page](https://math.uni-paderborn.de/ag/arbeitsgruppe-spektralanalysis). PyZeta is a current open-source Python project for classical Pollicott–Ruelle, semiclassical, and quantum resonances, including convex obstacle scattering and convex-cocompact hyperbolic surfaces. [Documentation](https://pyzeta.readthedocs.io/).

   Their prevailing public tools are numerical: discretization, nonlinear eigenproblems, complex scaling/absorbing boundaries, cycle expansions, or zeta truncation, followed by convergence checks and comparison with known cases. Borthwick has mathematical convergence/decay theory behind the series, but the individual plotted zero counts are not exported as interval certificates. This group is the largest *application* audience but is less likely than CAP specialists to supply new tail proofs.

4. **Numerical linear algebra and spectral-measure researchers.** SpecSolve and EigTool users care about spectral pollution, nonnormality, pseudospectra, and reliable spectral computation. They are plausible consumers of a generic contour verifier when they can provide a rigorous analytic enclosure, but they should not be promised turnkey infinite-dimensional certification. The distinction between a finite matrix’s characteristic determinant and an operator determinant must remain explicit.

### Would they adopt Python?

Plausibly, yes—but not because Python alone creates demand.

- python-flint already exposes Arb/Acb under an MIT wrapper and distributes Python releases, removing the need for users to write C for ball arithmetic. [Repository](https://github.com/flintlib/python-flint)
- PyZeta demonstrates that the resonance-computation community already accepts Python for research software.
- `cxroots` demonstrates demand for a simple Python contour-root interface, while its lack of rigor creates a clear upgrade path.
- The dominant verified-numerics alternatives remain MATLAB (INTLAB), C++ (kv/CAPD/VCP), and Julia. A Python producer can attract spectral users; an independent, deliberately small checker and documented JSON/CBOR certificate can attract auditors who do not want to trust the Python orchestration layer.

Adoption therefore depends on three things: a paper-grade worked theorem, reproducible installation, and a certificate whose validity can be checked without rerunning the expensive search/escalation process. A broad “rigorous eigenvalues for anything” claim would repel precisely the expert audience most likely to help.

Publication norms reinforce this. The London Mathematical Society’s computer-aided-proof policy requires underpinning code and supplementary files to be deposited and asks for “transparent surveyable code” that minimizes sources of error such as roundoff. [LMS policy](https://www.lms.ac.uk/publications/policies/computeraidedproofs). A compact checker plus immutable certificate is aligned with that review need.

**Recommendation:** Target validated transfer-operator/CAP researchers first, using the G_5 paper as the flagship reproducible case; make resonance and quantum-chaos numerical researchers the second audience through a Python producer API whose honest contract is “bring a proved tail adapter.”

## 3. Primary form

### Comparison

| Form | Strength | Failure mode for this project | Verdict |
|---|---|---|---|
| Pip-installable library | Lowest barrier for Python exploration; natural fit for python-flint; reusable contour and escalation API. | A library API alone hides the proof boundary. Reverification can become “install the same large stack and rerun it,” which asks the reviewer to trust producer logic, dependency versions, adaptive choices, and serialization. | Useful delivery channel, not the primary intellectual form. |
| Research code + notebooks | Fastest route to a paper companion; notebooks can explain the G_5 geometry and visualize contours/margins. | Notebooks are mutable, stateful, awkward to diff, and poor trust anchors. They encourage demonstrations rather than a stable machine contract. | Keep as explanatory material only. |
| **Certificate standard + independent checker, with a producer engine** | Separates discovery from verification; certificates are archival and diffable; the checker can reject malformed coverage, wrong hashes, upward-rounded margins, missing assumptions, and invalid winding transitions without rerunning search. Multiple future engines can emit the same format. | The split is fake if the certificate merely stores the producer’s conclusions or if the checker calls the entire producer. The checker must recompute every cheap logical/arithmetic implication from primitive enclosures and explicitly identify theorem-level assumptions it cannot derive. | Best primary form. |

### DRAT analogy—and its limit

The DRAT ecosystem is the right architectural analogy. SAT solvers emit a proof in a standard clausal format; `drat-trim` independently validates the proof against the DIMACS input. The format was designed to be easy for solvers to emit, compact to store, expressive enough for modern solver techniques, and efficient to check. [Heule, “The DRAT format and DRAT-trim checker,” 2016](https://arxiv.org/abs/1610.06229); [drat-trim repository and format](https://github.com/marijnheule/drat-trim).

The analogy should not be overstated. DRAT steps have a uniform local redundancy rule. A spectral certificate depends on analytic theorems—nuclearity, operator identification, basis normalization, parameter-uniform tail inequalities—that cannot be reconstructed from a bag of floating-point intervals unless they are formalized. Therefore the spectral format needs two explicit layers:

1. **Machine-rechecked facts:** schema/version, canonical encoding, hashes, exact contour closure and orientation, no gaps or overlaps in the accepted sub-arc cover, directed-rounding interval endpoints, nonzero exclusions, derivative/Jacobi inequalities, `rH < 1`, Rouché margins, quadrant/half-plane transitions, total winding, and every numeric margin recomputed then serialized rounded **down**.
2. **Named theorem assumptions/adapters:** the exact operator family, function space, determinant identity, truncation theorem, parameter domain, constants, and a hash of the human-readable proof/source. The checker verifies that the numeric certificate instantiates the adapter’s declared inequalities; it must not claim to prove the analytic theorem from JSON.

The trust anchor should be a small checker package with no plotting, root search, adaptive strategy, or family construction. Ideally it has one command, `check CERTIFICATE`, deterministic canonical parsing, a pinned arithmetic backend, strict failure on unknown fields/versions, and conformance fixtures including salted negative certificates. The producer may be pip-installable and sophisticated; the checker should remain boring.

**Recommendation:** Make the **certificate specification plus tiny independent checker** the primary public artifact, with the Python/Arb engine as the reference producer and notebooks as non-authoritative explanation.

## 4. Honest v1 scope

### Include in v1

1. **A versioned certificate format.** It should bind:
   - theorem/case identifier and epistemic status;
   - source and dependency hashes, python-flint/FLINT versions, precision, platform metadata;
   - exact contour vertices, orientation, and parameterization;
   - every accepted closed sub-arc and its parent/split history;
   - Arb/Acb enclosures needed to recheck nonvanishing and winding transitions;
   - the escalation ladder actually taken (precision, subdivision, truncation dimension), including failed attempts rather than only the winning leaf;
   - tail-adapter identifier, statement version, constants, domain, input hashes, and the computed tail bound;
   - all decisive margins stored conservatively (lower bounds rounded down; upper bounds rounded up), with decimal strings or exact dyadics rather than binary floats;
   - canonical-file digest and hashes of external bound receipts.

2. **A small independent checker.** It must validate canonical encoding/hashes; full closed-cover topology; arithmetic interval syntax; local Jacobi/Taylor or endpoint enclosures; strict inequalities; Rouché dominance; winding accumulation; and conservative margin serialization. It should return a narrow verdict such as `VALID NUMERICAL WINDING CERTIFICATE FOR ADAPTER X`, never `THEOREM PROVED` when determinant identification remains external.

3. **The generic contour engine.** A Python/Arb reference producer accepting a callback that returns certified enclosures (and, where needed, derivative/inverse bounds), supporting rectangles/polygons, adaptive closed-sub-arc subdivision, precision and truncation escalation, deterministic logging, and certificate emission. The generic layer may certify zeros of the supplied finite or enclosed analytic function; it must not infer operator convergence.

4. **Only the proven Hecke/Rosen–Gauss adapters used by the flagship.** Package the exact q=5/G_5 odd-sector construction, normalized bases, exact Hurwitz branch-tail closure, finite matrix determinant, the reviewed parameter-uniform truncation-tail bound, and the R3b closed-contour enclosure method as worked, executable examples. Include the q=3 or other families only if their tail theorem and determinant identification meet the same review standard. Do not generalize from code parameterization alone: `.worktrees/aletheia-restore/code/zeta_cert_rosen.py` being q-generic does not prove a q-uniform operator theorem.

5. **A frozen flagship certificate and one-command verification path.** The release must include the exact G_5 contour, N=160 receipt, accepted sub-arcs, all bound inputs, hashes, and expected checker output. Also include the N=128 failure as a negative fixture so reviewers see that escalation is evidence-driven rather than tuned away.

6. **A proof map.** One page should map each checker predicate to the paper lemma and each external analytic assumption to its source. It must preserve the repository’s current scope warning: a valid local H² determinant winding is not automatically the Mayer–Mühlenbruch–Strömberg Banach-space determinant or a Selberg-zeta resonance unless the common-continuation/determinant-identification bridge is proved.

### Explicitly “bring your own tail bound”

For a new operator family, v1 should require the user to provide a reviewed adapter proving, on the entire contour domain:

- the operator and function space are defined and nuclear/trace class as required;
- the finite representation matches the stated basis/normalization;
- a computable uniform bound controls the true determinant (or operator) versus the truncation;
- the bound’s hypotheses are machine-instantiated by certificate fields; and
- any determinant-to-resonance/eigenvalue identification is separately cited or proved.

The generic engine can check a supplied numeric inequality such as `tail_upper < contour_lower_margin`; it cannot manufacture the analytic bound. Empirical determinant increment ratios, corner sampling plus a safety factor, mesh convergence, and agreement across N are diagnostics only and must be rejected as tail certificates.

### Smallest reviewer-usable G_5 release

The smallest credible v1 for an independent reviewer is not a general spectral library. It is:

1. a frozen, citable release containing the G_5 theorem statement and proof map;
2. the exact source implementing the G_5 finite determinant and the separately proved tail adapter;
3. one portable certificate file binding all inputs by hash and recording the complete N=160 closed contour cover;
4. a minimal checker that recomputes every numerical inequality and the winding from that file;
5. environment lock/container instructions plus `verify-g5` as the single reviewer command;
6. negative fixtures: changed hash, one missing sub-arc, one margin rounded the wrong way, one zero-containing image ball, the real N=128 failure, and one invalid tail bound;
7. an explicit final status line separating (a) certified finite/infinite determinant winding, (b) operator-determinant identification, and (c) resonance/Selberg-zeta interpretation.

This is sufficient for a reviewer to audit the claimed computation without reproducing the expensive adaptive search. It is insufficient for the full flagship theorem if the present determinant-identification gap remains unresolved; the repository must say so in the certificate verdict and README.

**Recommendation:** Ship v1 as a G_5-first certificate/checker release with one generic contour producer and exactly one reviewed tail adapter; label every other operator family **bring your own proved uniform tail bound**, and do not call the full G_5 resonance theorem independently verified until the determinant-identification bridge is closed.

## 5. Name and positioning

GitHub’s repository API could not be queried from the local environment (DNS was blocked), and direct web fetches of the candidate URLs did not resolve through the research tool. Exact-name web searches on 2026-08-16 returned no indexed GitHub repositories for the five strings below. That is weak evidence only: availability must be rechecked immediately before creation, including case-insensitive collisions and organization ownership.

Ranked candidates:

1. **ContourCert** — “Portable, independently checkable winding certificates for analytic determinants, with explicit operator-tail adapters.”
2. **FredholmCert** — “Proof-carrying Fredholm-determinant computations from Arb enclosures and theorem-backed truncation bounds.”
3. **SpectralReceipts** — “Machine-checkable receipts for certified eigenvalue and resonance computations.”
4. **CertSpectra** — “A Python/Arb producer and small checker for rigorous spectral localization.”
5. **ArbWinding** — “Certified closed-contour winding with Arb/Acb, adaptive sub-arcs, and conservative margins.”

`ContourCert` is the strongest name because it is precise without overclaiming the unresolved operator/resonance bridge, remains useful beyond Fredholm determinants, and foregrounds the reusable certified operation. `SpectralReceipts` best expresses the project philosophy but is less immediately legible as mathematical software. `ArbWinding` over-binds the public identity to one arithmetic backend; `FredholmCert` risks implying that every user-supplied determinant identity/tail theorem is certified by the engine; `CertSpectra` is concise but generic.

**Recommendation:** Use **ContourCert** as the primary repository name, subject to a live GitHub API check at creation time, and use the subtitle “proof-carrying winding certificates for spectral determinants.”

## Sources and citations

### Validated-numerics tools

- Siegfried M. Rump, [INTLAB — INTerval LABoratory](https://www.tuhh.de/ti3/intlab/), official software and license page; canonical citation: “INTLAB — INTerval LABoratory,” in *Developments in Reliable Computing* (1999), 77–104.
- Siegfried M. Rump, [“Verification methods: Rigorous results using floating-point arithmetic”](https://doi.org/10.1017/S096249291000005X), *Acta Numerica* 19 (2010), 287–449.
- INTLAB, [`verifynlss` sparse-system demonstration](https://www.tuhh.de/ti3/rump/intlab/demos/html/dsparse.html).
- Masahide Kashiwagi, [kv — a C++ Library for Verified Numerical Computation](https://verifiedby.me/kv/index-e.html); [source repository](https://github.com/mskashi/kv).
- Fredrik Johansson, [“Arb: Efficient Arbitrary-Precision Midpoint-Radius Interval Arithmetic”](https://doi.org/10.1109/TC.2017.269063), *IEEE Transactions on Computers* 66 (2017), 1281–1292.
- FLINT, [Arb/Acb documentation index](https://flintlib.org/doc/index_arb.html) and [`acb_calc` rigorous integration](https://arblib.org/acb_calc.html).
- [python-flint repository](https://github.com/flintlib/python-flint), Python bindings and license information.
- [JuliaIntervals ecosystem overview](https://juliaintervals.github.io/); [`IntervalArithmetic.jl` API](https://juliaintervals.github.io/IntervalArithmetic.jl/dev/manual/api/); [`IntervalLinearAlgebra.jl`](https://juliaintervals.github.io/IntervalLinearAlgebra.jl/).
- [ValidatedNumerics.jl repository](https://github.com/JuliaIntervals/ValidatedNumerics.jl), archived historical meta-package.

### Zero finding and spectral software

- M. S. Petković and L. D. Petković, [“Enclosing all zeros of an analytic function — A rigorous approach”](https://doi.org/10.1016/j.cam.2008.10.014), *Journal of Computational and Applied Mathematics* 228 (2009), 418–423.
- [cxroots documentation](https://rparini.github.io/cxroots/), numerical contour root finding for Python.
- Matthew J. Colbrook, Andrew Horning, Alex Townsend, [“Computing spectral measures of self-adjoint operators”](https://arxiv.org/abs/2006.01766), *SIAM Review* 63 (2021); [SpecSolve organization](https://github.com/SpecSolve).
- Thomas G. Wright, Nick Trefethen et al., [EigTool official site](https://www.cs.ox.ac.uk/pseudospectra/eigtool/).
- David Bindel and Maciej Zworski, [“Theory and Computation of Resonances in 1D Scattering”](https://www.cs.cornell.edu/~bindel/cims/resonant1d/), 2006 tutorial and MATLAB code.
- [PyZeta documentation](https://pyzeta.readthedocs.io/), open-source Python resonance software.

### Transfer operators, resonances, and communities

- Oscar F. Bandtlow and Julia Slipantschuk, [“Lagrange approximation of transfer operators associated with holomorphic data”](https://arxiv.org/abs/2004.03534), 2020 preprint / later publication.
- Mark Pollicott and Julia Slipantschuk, [“Effective estimates of ergodic quantities illustrated on the Bolyai–Rényi map”](https://arxiv.org/abs/2308.04293), *Nonlinearity* 37 (2024) 095013.
- David Borthwick, [“Distribution of resonances for hyperbolic surfaces”](https://arxiv.org/abs/1305.4850), *Experimental Mathematics* 23 (2014), 25–45.
- [Validated Numerics for Computer-Assisted Proofs](https://vncap.org/), ICMS workshop, 6–10 July 2026.
- [SCAN proceedings series](https://dblp.org/db/conf/scan/index.html), International Symposium on Scientific Computing, Computer Arithmetic, and Validated Numerics.
- [GAMM activity group on computer-assisted proofs and symbolic computation](https://www2.math.uni-wuppertal.de/wrswt/gamm/).
- [Tobias Weich spectral-analysis group](https://math.uni-paderborn.de/ag/arbeitsgruppe-spektralanalysis), Paderborn University.
- [London Mathematical Society policy on computer-aided proofs](https://www.lms.ac.uk/publications/policies/computeraidedproofs), updated November 2024.

### Certificate/checker precedent

- Marijn J. H. Heule, [“The DRAT format and DRAT-trim checker”](https://arxiv.org/abs/1610.06229), 2016.
- [drat-trim repository and DRAT format specification](https://github.com/marijnheule/drat-trim).

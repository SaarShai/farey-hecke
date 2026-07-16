# Multidimensional prefix balance: primary-source and claim-scope audit

Date: 2026-07-15.  This is a bounded primary-source audit, not an exhaustive
MathSciNet/zbMATH priority search.  Search absence is not evidence of novelty.

## Audit rule

Each entry separates what the source establishes from what it does **not**
establish for this project.  Publisher pages, author-hosted papers, official
archives, or original papers are linked directly.  Secondary summaries were
used only to locate primary material and are not claim evidence.

## Mathematical and algorithmic sources

### 0. García: the one-dimensional gap-ordering problem

R. Tomás García, “A General Lower Bound for Average Local Discrepancy and an
Application to the Farey Sequence,” *Mathematics* 14 (2026), article 2543,
[DOI 10.3390/math14142543](https://doi.org/10.3390/math14142543),
[publisher page](https://www.mdpi.com/2227-7390/14/14/2543).

- **Establishes:** the fixed-gap permutation formulation, its local prefix
  errors, gap-based lower bounds, and the qualitative permutation-average
  conjecture addressed by the original project preprint.
- **Project use:** equation (1.2) is the exact one-dimensional specialization
  of the contribution/mass formulation, so the new optimizer continues rather
  than replaces the original observation.
- **Does not establish:** multidimensional categorical quotas, EDF scheduling,
  the `<3` factor, constrained optimization, or the two-pass oracle.  Those are
  separate deductions and must not be attributed to García.

### 1. Balinski and Young: house-monotone quota paths

M. L. Balinski and H. P. Young, “Quotatone Apportionment Methods,”
*Mathematics of Operations Research* 4 (1979), 31--38,
[DOI 10.1287/moor.4.1.31](https://doi.org/10.1287/moor.4.1.31).

- **Establishes:** quota means each coordinate is the floor or ceiling of its
  proportional entitlement; house monotonicity means allocations never fall
  when the house grows; the paper characterizes methods satisfying both and
  supplies the classical existence basis for a nested quota path.
- **Project use:** fixing entitlements `n_c/N` and growing house size from zero
  to `N` yields existence of a category word satisfying both prefix quotas.
- **Does not establish:** the occurrence-window formulation, release-aware EDF,
  two-heap implementation, `O(N log C)` bound, exact endpoint scan, or the
  project's `<3` approximation certificate.  Those require the manuscript's
  deductions and tests.

### 2. Horn: scheduling ancestry

W. A. Horn, “Some Simple Scheduling Algorithms,” *Naval Research Logistics
Quarterly* 21 (1974), 177--185,
[DOI 10.1002/nav.3800210113](https://doi.org/10.1002/nav.3800210113).

- **Establishes:** optimal scheduling rules for single-operation jobs in
  maximum-lateness and delay settings, including the classical earliest-
  deadline scheduling line; the paper's general model allows preemption.
- **Project use:** historical scheduling context.  The manuscript gives its own
  exchange proof for nonpreemptive unit jobs with integer release/deadline
  windows.
- **Does not establish:** feasibility of the project's quota windows.  That
  existence comes from the apportionment path; nor does Horn establish head
  compression or the categorical approximation factor.

### 3. Berstel and de Luca: Christoffel, mechanical, and tree structure

J. Berstel and A. de Luca, “Sturmian Words, Lyndon Words and Trees,”
*Theoretical Computer Science* 178 (1997), 171--203,
[DOI 10.1016/S0304-3975(96)00101-6](https://doi.org/10.1016/S0304-3975%2896%2900101-6),
with an [author-hosted paper](https://www-igm.univ-mlv.fr/~berstel/Articles/1997SturmianLyndonTrees.pdf).

- **Establishes:** primitive Christoffel words as finite Sturmian/Lyndon
  objects, their slope/prefix structure, continued fractions, and their tree
  relations.
- **Project use:** after reducing `a/N=p/q`, the nearest-intercept mechanical
  word has a primitive period in the Christoffel conjugacy family; the reduced
  fraction supplies the Farey/Stern-Brocot connection.
- **Does not establish:** that the nearest-intercept word equals the canonical
  lower/Lyndon Christoffel representative.  It need not.  It also does not
  select EDF's tie-dependent output or solve the `C>=3` quota problem.

### 4. Grinberg and Sevastyanov: sharp general-norm Steinitz existence

V. S. Grinberg and S. V. Sevastyanov, “Value of the Steinitz Constant,”
*Functional Analysis and Its Applications* 14 (1980), 125--126,
[MathNet record and paper](https://www.mathnet.ru/eng/faa1805),
[DOI 10.1007/BF01086559](https://doi.org/10.1007/BF01086559).

- **Establishes:** for zero-sum vectors in the unit ball of an arbitrary norm
  on `R^d`, a permutation exists with all partial sums bounded by the
  dimension-order Steinitz constant; the general-norm bound `d` is sharp.
- **Project use:** an unconstrained existential `B<=dR`, and with the elementary
  jump lower bound `OPT>=R/2`, an existential `2d` comparison.
- **Does not establish:** the V1 quota algorithm, a million-scale implemented
  constructor, constraints, `L-infinity` performance better than the classical
  dimension bound, or the categorical `<3` theorem.

### 5. Bárány: a constructive vector-sum route and its actual cost

I. Bárány, “A Vector-Sum Theorem and its Application to Improving Flow Shop
Guarantees,” *Mathematics of Operations Research* 6 (1981), 445--452,
[DOI 10.1287/moor.6.3.445](https://doi.org/10.1287/moor.6.3.445),
[paper copy](https://www.cs.umd.edu/~gasarch/BLOGPAPERS/appsteinitz.pdf).

- **Establishes:** a constructive bounded-prefix vector-sum theorem and an
  application to flow-shop approximation.  The paper reports Kadec's older
  construction with `O(N^d)` dependence and develops a stronger-radius route
  whose displayed linear-dependence machinery leads to quadratic dependence
  on `N` (commonly summarized as `O(N^2 d^3+N d^4)`).
- **Project use:** it falsifies the tempting inference that “constructive
  Steinitz” means a verified `O(Nd)` million-item algorithm.
- **Does not establish:** the frozen runtime gate for `N=1,000,000`, `d=4`, or
  arbitrary V1 constraints.  No such implementation claim is made.

### 6. Dutta, Jha, and Jiang: recent constructive `L2` prefix discrepancy

K. Dutta, A. V. Jha, and H. Jiang, “Near-Optimal Constructive Bounds for
`l2` Prefix Discrepancy and Steinitz Problems via Affine Spectral
Independence,” arXiv:2604.13355 (2026),
[primary preprint](https://arxiv.org/abs/2604.13355).

- **Establishes:** an efficient SDP/spectral-independence construction for
  Euclidean prefix discrepancy, with near-conjectured dimension behavior in a
  stated high-dimension-versus-logarithm regime.
- **Project use:** current evidence that constructive prefix discrepancy is an
  active and technically sophisticated area.
- **Does not establish:** the V1 `L-infinity` theorem, a simple `O(Nd)` method,
  the frozen one-million runtime/RSS threshold, or factors under blocks, pins,
  and arbitrary sparse precedence.

### 7. Kellerer, Kotov, Rendl, and Woeginger: related hardness, not our theorem

H. Kellerer, V. Kotov, F. Rendl, and G. J. Woeginger, “The Stock Size
Problem,” *Operations Research* 46 (1998), S1--S12,
[DOI 10.1287/opre.46.3.S1](https://doi.org/10.1287/opre.46.3.S1).

- **Establishes:** NP-hardness and approximation algorithms for ordering
  resource-consuming/supplying jobs to minimize required stock under that
  paper's feasibility and stock objective.
- **Project use:** a close operational neighbour showing that partial-sum
  sequencing problems can be computationally hard.
- **Does not establish:** NP-hardness of the exact centered two-sided
  `L-infinity` prefix-balance problem, its categorical subproblem, or the V1
  constraint language.  This audit found no checked reduction, so the project
  makes **no hardness claim** for its exact contract.  Exponential subset DP is
  an exact method, not proof of necessity.

## Fair-scheduling sources

### 8. Parekh and Gallager: GPS and packetized fair queueing guarantees

A. K. Parekh and R. G. Gallager, “A Generalized Processor Sharing Approach to
Flow Control in Integrated Services Networks: The Single-Node Case,”
*IEEE/ACM Transactions on Networking* 1 (1993), 344--357,
[DOI 10.1109/90.234856](https://doi.org/10.1109/90.234856),
[author-hosted paper](https://www.cs.utexas.edu/~lam/396m/papers/PG1993.pdf).

- **Establishes:** worst-case throughput/delay guarantees for GPS with traffic
  controls and a packetized discipline approximating the fluid model.
- **Project use:** a serious incumbent model for weighted progressive service.
- **Does not establish:** exact two-sided floor/ceiling prefix quotas for a
  fixed finite inventory, the occurrence windows, or factors with precedence.

### 9. Shreedhar and Varghese: deficit round robin

M. Shreedhar and G. Varghese, “Efficient Fair Queuing Using Deficit
Round-Robin,” *IEEE/ACM Transactions on Networking* 4 (1996), 375--385,
[DOI 10.1109/90.502236](https://doi.org/10.1109/90.502236),
[paper copy](https://www.ecs.umass.edu/ece/wolf/courses/ECE697J/papers/DRR.pdf).

- **Establishes:** an efficient packet scheduling approximation to fair
  queueing with throughput-fairness analysis and constant per-packet work under
  its model.
- **Project use:** operational baseline and warning against equating intuitive
  deficit scores with exact quota.
- **Does not establish:** the project's simultaneous prefix floor/ceiling
  property or `<3` certificate.  Naive deficit and virtual-finish variants were
  therefore treated as hypotheses and attacked by exact small cases.

## Application-neighbour sources and limits

### 10. Christensen, Kensler, and Kilpatrick: progressive rendering samples

P. Christensen, A. Kensler, and C. Kilpatrick, “Progressive Multi-Jittered
Sample Sequences,” *Computer Graphics Forum* 37 (2018), 21--33,
[DOI 10.1111/cgf.13472](https://doi.org/10.1111/cgf.13472),
[Pixar paper](https://graphics.pixar.com/library/ProgressiveMultiJitteredSampling/paper.pdf).

- **Establishes:** progressive two-dimensional sample sequences with explicit
  stratification properties and empirical integration/rendering comparisons.
- **Project use:** primary evidence that prefix quality matters in incremental
  rendering and a mandatory incumbent for any real renderer comparison.
- **Does not establish:** that balancing an arbitrary finite set of joint-cell
  labels improves image error.  The V1 rendering preset is a demonstration,
  not a production renderer result.

### 11. Joy, Boyle, and Tan: quasi-Monte Carlo in numerical finance

C. Joy, P. P. Boyle, and K. S. Tan, “Quasi-Monte Carlo Methods in Numerical
Finance,” *Management Science* 42 (1996), 926--938,
[DOI 10.1287/mnsc.42.6.926](https://doi.org/10.1287/mnsc.42.6.926).

- **Establishes:** deterministic low-discrepancy methods applied and compared
  on derivative-valuation examples.
- **Project use:** evidence that multidimensional progressive sample design is
  relevant to computational finance and that strong established baselines
  already exist.
- **Does not establish:** that joint scenario-cell quota controls pricing
  error, discontinuous payoff/tail coverage, Value-at-Risk, regulatory stress
  adequacy, or money saved.  V1 makes none of those claims.

### 12. Pocock and Simon: sequential covariate balance

S. J. Pocock and R. Simon, “Sequential Treatment Assignment with Balancing for
Prognostic Factors in the Controlled Clinical Trial,” *Biometrics* 31 (1975),
103--115, [DOI 10.2307/2529712](https://doi.org/10.2307/2529712),
[PubMed record](https://pubmed.ncbi.nlm.nih.gov/1100130/).

- **Establishes:** a sequential treatment-assignment procedure designed to
  balance several prognostic factors when full stratification is impractical.
- **Project use:** evidence that multidimensional sequential balance is a real
  design problem, and a warning that randomization and inferential validity are
  load-bearing.
- **Does not establish:** that deterministic quota ordering is valid treatment
  allocation.  V1 is restricted to ordering already available, pre-randomized
  laboratory inventory and makes no clinical or causal claim.

## Claim classification

| Project statement | Classification | Safe scope |
|---|---|---|
| House-monotone quota path exists | Classical | Balinski--Young entitlement path |
| Unit-window EDF exchange rule | Classical scheduling idea plus self-contained specialization | Fixed finite unit jobs after quota existence |
| Window formulas, head compression, endpoint scan | Project deduction/synthesis | Equal-mass finite categorical inventory |
| `L_quota` and strict `<3` combination | Project deduction; external priority unverified | Unconstrained equal-mass one-hot `L-infinity` objective |
| Nearest binary word is exact | Elementary mechanical-word deduction | Two categories only |
| Christoffel/Farey relation | Classical | Primitive reduced period/conjugacy, not canonical EDF |
| Two-pass exact oracle | Project algorithmic deduction | Small exact rational V1 instances |
| General Steinitz bounded order exists | Classical | Unconstrained arbitrary norm |
| Million-scale arbitrary-vector constructor | Not a claim | Deferred |
| NP-hardness of exact V1 objective | Not established | No claim without a direct reduction |
| Rendering/finance/experiment improvement | Not established | Presets demonstrate declared cell balance only |

## Potholes prevented by the audit

1. A quota-existence citation is not an EDF runtime proof.
2. “Mechanical” does not mean “canonical lower Christoffel”; counts `(1,4)`
   separate the lower word from the nearest minimax word.
3. A constructive Steinitz paper is not automatically linear in item count or
   suitable for the selected norm and constraints.
4. Hardness of a neighbouring stock/flow-shop problem is not hardness of this
   exact objective.
5. Weighted fair queueing and deficit round robin solve different arrival,
   packet-size, and service models; they are baselines, not theorem sources.
6. Rendering and finance already have low-discrepancy incumbents.  A cell-
   balancing demo must not be described as downstream accuracy evidence.
7. Treatment balance without randomization/inference safeguards is not a
   clinical design.

## Remaining literature work before publication

- formula-level MathSciNet and zbMATH searches for simultaneous quota words,
  balanced multi-letter words, apportionment sequences, and just-in-time mixed-
  model sequencing;
- citation-graph review around Balinski--Young and multi-colour balanced words
  for the exact occurrence-window/EDF synthesis;
- specialist combinatorics-on-words review of the tie-boundary conjugacy
  wording;
- direct complexity-theory review before making any hardness statement; and
- domain-integrated experiments against PMJ/Sobol, finance QMC, and appropriate
  randomized experimental-design baselines before making value claims.

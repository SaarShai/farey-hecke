# Michael Levin’s “free lunches” and arithmetic payoffs from Farey, prime, and complex fractions

**Research date:** 2026-08-10  
**Status:** source-audited synthesis plus finite reproducible demonstrations.  
**Companion files:** [Levin primary-source map](michael_levin_free_lunch_primary_sources_2026-08-10.md), [probe code](levin_farey_payoff_probe.py), [JSON receipt](levin_farey_payoff_probe.json), [SVG result](levin_farey_payoff_probe.svg), [rendered PNG](levin_farey_payoff_probe.png).

## Bottom line

There is a defensible connection, but it is narrower and more interesting than “simple mathematics gives free intelligence.”

Levin uses **free lunch** in at least three senses:

1. an observer discovers a useful secondary behavior that was not an explicit objective of a simple local rule;
2. a pre-existing structured pattern provides task-relevant guidance for little task-specific design;
3. in his recent Platonic-space proposal, physical systems act as interfaces to mathematical or agential patterns and receive more capability than their construction seems to specify.

Only the first two currently have controlled experimental support, and even there “free” means **not separately instructed**, not zero runtime, energy, information, or selection cost. The third is Levin’s stated research program and metaphysical interpretation, not a result forced by the experiments.

Farey and prime-fraction systems give unusually clean versions of the first two senses:

- the two-denominator Farey recurrence automatically carries exact adjacency certificates, one-step prediction, a limiting gap law, and—under a precise threshold—a forbidden triple of extreme gaps;
- a prime-denominator Farey increment is the complete nonzero regular \(p\)-grid, so adding the already-present zero produces exact Fourier cancellation for every nonresonant mode;
- a Gaussian-prime’s nonzero primitive layer, together with the inherited zero class, completes a finite quotient subgroup of the complex torus, with the same character-orthogonality payoff in two dimensions and strong finite separation;
- the full real and complex Farey clouds have non-Poisson, mathematically predictable nearest-neighbor statistics.

These are real **structural dividends**. Whether they become computational, sampling, robustness, or prediction payoffs depends on the interface and task. They do not contradict no-free-lunch theorems, because the arithmetic family is highly nonuniform and the rule itself supplies a strong prior.

## 1. What Levin actually established

### 1.1 The empirical core: modified, distributed sorting

Zhang, Goldstein, and Levin’s [sorting paper](https://doi.org/10.1177/10597123241269740) does not simply watch an unchanged textbook Bubble Sort. It deliberately changes two assumptions: every array element runs a local “cell-view” sorting policy rather than obeying a global controller, and some elements can be frozen or unreliable. The [open preprint](https://arxiv.org/abs/2401.05375) and [released code](https://github.com/Zhangtaining/cell_research) make the model inspectable.

The main reported effects are:

- cell-view Bubble Sort remains more robust than the corresponding traditional implementation under the tested frozen-cell perturbations;
- its observer-measured **Sortedness** can temporarily decrease before increasing farther—called delayed gratification—and the mean delayed-gratification score rises as frozen barriers are added;
- mixtures of Bubble, Insertion, and Selection “Algotypes” transiently segregate even though no cell can inspect Algotype or execute a clustering instruction.

This is good evidence for **unexpected competencies of a transparent rule system**. It is not evidence that the cells contain an unmeasured reward, conscious intention, or costless computation. Sortedness, delayed gratification, and aggregation are observer-defined probes. The paper itself says the outcomes remain consequences of the rules and analyzes aggregation as one selected emergent observable.

Two qualifications matter:

1. It is a distributed, concurrent rewrite of classical sorting, not the canonical single-controller Bubble Sort.
2. The current repository chooses a left/right probe randomly and inherits thread-scheduling stochasticity, despite the paper’s description of the policy as deterministic/open-loop. The public HEAD is therefore provenance, not proof that it is the exact figure-producing revision.

The strongest reading is: **a rule selected for local numerical ordering also induces context-sensitive rerouting and a second, unencoded spatial correlation.** Calling that correlation a “payoff” is legitimate if we say whose payoff it is and how it is scored.

### 1.2 The paper literally titled “Free Lunch?”

Ertle, Levin, and Scheutz’s [2025 ICDL paper](https://hrilab.tufts.edu/publications/ertleetal25icdl.pdf) feeds a maze agent fixed Halley-fractal or artwork patterns unrelated to the maze. Under a trivial color-to-action mapping, structured fractals and art outperform shuffled versions and uniform noise. That is the cleanest empirical instance of a low-cost external pattern providing useful behavior without maze-specific learning.

The DQN result is weaker than the title can suggest. A 1:1 environment/fractal input outperforms environment-only and pattern-only agents and generalizes to unseen mazes, but replacing the fractal with uniform noise does **not** significantly change either result (single-maze \(p=.096/.999\); generalization \(p=.998/.998\)). Thus:

- **simple mapping:** evidence that spatial structure matters;
- **DQN:** evidence that nonspecific additional input can help, not that fractal structure caused the gain.

The DQN also pays for training, a reward function, a network, and selected input encoding. This is low-cost scaffolding relative to hand-designing a maze policy, not free computation in an absolute ledger.

### 1.3 The larger MCA/TAME mechanism

Levin’s [TAME framework](https://doi.org/10.3389/fnsys.2022.768201), the Fields–Levin [arbitrary-spaces paper](https://doi.org/10.3390/e24060819), and Levin’s [agential-materials synthesis](https://doi.org/10.1007/s00018-023-04790-z) propose a multiscale competency architecture: lower-level agents follow local homeostatic gradients while higher-level organization deforms their option landscape so those local actions can serve a larger goal. Competency is “fixed goal, variable means” in behavioral, physiological, transcriptional, or anatomical spaces.

Shreesha and Levin’s [stress-sharing model](https://doi.org/10.1016/j.bbrc.2024.150396) supplies a concrete mechanism. A stressed cell shares a local error signal; otherwise blocking cells temporarily become permissive, allowing the collective to reach a global target without a central movement script. The model also exposes costs and limits: it spends many more swaps, and its 50×50 systems do not reach maximum fitness within the reported 1,000 generations.

The relevance to the arithmetic systems below is architectural, not biological: **a small local state plus an invariant can reshape which future moves are possible, so an external user can exploit global structure without storing or deriving it afresh at every step.**

### 1.4 The Platonic “free lunch” is a hypothesis

In his 2025 [Platonic-space essay](https://thoughtforms.life/platonic-space-where-cognitive-and-morphological-patterns-come-from-besides-genetics-and-environment/), Levin explicitly includes prime-number facts, mathematical constants, and properties of computation among “free lunches.” In his March 2026 [short argument](https://thoughtforms.life/a-short-argument-on-platonic-space-variable-agency-patterns-that-in-form-physics-biology-computer-science-and-cognitive-science/), he defines the hoped-for effect as paying some physical cost while receiving much more capability than that effort appears to specify, and says quantifying such effects is an open research program.

That interpretation should be kept separate from the measurements. Mathematics certainly constrains every implementation; the experiments do not decide whether those constraints require a nonphysical Platonic ontology. The useful scientific question survives either metaphysics: **which compact interfaces expose which reusable structural dividends, at what full cost, against what null?**

## 2. An operational definition of “payoff”

Let a system have:

- a local rule \(R\);
- an explicit target score \(S_0\), if any;
- a candidate secondary score \(S_1\) not explicitly optimized by \(R\);
- perturbations or task instances \(E\);
- a cost ledger \(C\): runtime, energy, memory, code length, training data, oracle information, and preprocessing;
- a matched null \(R_0\) preserving the relevant parts of \(C\), cardinality, and marginal statistics.

A finite observer-side payoff can be written

\[
\Pi_1 = S_1(R,E)-\mathbb E[S_1(R_0,E)]
\]

at matched cost. A robustness payoff instead compares \(S_0\) after perturbation; a computational payoff compares cost at identical output; a generalization payoff compares held-out tasks.

Four gates prevent the word “emergent” from doing all the work:

1. **Nontriviality:** \(S_1\) was not just a renamed explicit target.
2. **Matched null:** preserve count, marginals, and budget while breaking the proposed structure.
3. **Perturbation:** show the behavior tracks context rather than arising from an arbitrary random walk or metric choice.
4. **Full ledger:** include preprocessing and compare with a fair baseline, not only a convenient implementation.

This definition does not require an internal utility. It states exactly when an observer can exploit a side effect.

## 3. Real Farey sequences: local recurrence → global dividends

### 3.1 The rule and invariant

The Farey sequence of order \(N\) is

\[
F_N=\left\{\frac ab\in[0,1]: 0\le a\le b\le N,\ \gcd(a,b)=1\right\}
\]

in increasing order. If \(a_i/b_i<a_{i+1}/b_{i+1}\) are neighbors, then

\[
a_{i+1}b_i-a_i b_{i+1}=1,
\qquad
\frac{a_{i+1}}{b_{i+1}}-\frac{a_i}{b_i}=\frac1{b_i b_{i+1}}.
\]

The next denominator follows from only the previous two:

\[
b_{i+2}=\left\lfloor\frac{N+b_i}{b_{i+1}}\right\rfloor b_{i+1}-b_i.
\]

After normalizing \((x_i,y_i)=(b_i/N,b_{i+1}/N)\), this is the BCZ map on the Farey triangle. Athreya and Cheung identify it as a first-return map, prove ergodicity and zero entropy, and recover Farey gap statistics from its roof function \(1/(xy)\) in their [primary paper](https://arxiv.org/abs/1206.6597).

This already yields three payoffs from a two-number local state:

- **verification:** determinant one certifies adjacency;
- **prediction/compression:** two denominators determine the next denominator and gap;
- **statistical calibration:** the BCZ invariant measure gives an explicit limiting gap law.

No agent must store the full sequence to obtain those properties. But they are paid for by the coprimality constraint, ordering, and exact recurrence.

### 3.2 A demonstrated side payoff: forbidden extreme triples

Define a gap-position event

\[
E_i(t)=\mathbf 1\!\left[\frac{b_i b_{i+1}}{N^2}<t\right].
\]

Because the actual gap is \(1/(b_i b_{i+1})\), this selects large normalized gaps. A repository-local exact-rational argument establishes that for \(t\le 2/9\), three consecutive events cannot occur. The [proof note](../projects/mimo-mini-project/research_notes/cluster2_exhaustiveness_proof.md) combines analytic lemmas covering the quadrant, tail (including boundary slivers), and corner regions with exact-rational branch-and-bound over the remaining bulk. The [executable certificate](../projects/mimo-mini-project/code/cluster2_exhaustiveness_certificate.py) was independently rerun: 22 boxes certified, 24 skipped by domain constraints, zero undecided, maximum depth 11; because the script shifts boxes touching zero by \(10^{-6}\), that receipt is not standalone whole-triangle coverage. The proof note’s precise statement is an infimum of \(2/9\), approached but not attained; the executable’s header comment incorrectly suggests equality at two points whose maximum product is actually \(2/3\). This is a reproducible **repository-local proof/certificate package**, not a peer-reviewed or formally kernel-checked theorem.

The new finite probe used \(N=250\) and the exact integer predicate \(9b_i b_{i+1}<2N^2\):

| Quantity | Farey order | 500 event-count-preserving shuffles |
|---|---:|---:|
| adjacent pairs | 19,024 | 19,024 each |
| extreme events | 2,616 | 2,616 each |
| maximum run | **2** | median 5; range 3–8 |
| all-true length-3 windows | **0** | median 49; range 28–80 |
| next-denominator recurrence mismatches | **0** | not applicable |

The shuffle null preserves the exact event count and destroys only sequential placement. Therefore zero triples are not a consequence of rarity alone; they arise from Farey dynamics. This is very close to the empirical structure of Levin’s algorithm examples: a simple local rule gives an additional collective constraint that was not a separate objective.

### 3.3 What payoff does the cluster ceiling buy?

If a downstream procedure knows \(t\le2/9\), then after seeing two consecutive extreme gaps it can label the next one non-extreme without evaluating its threshold test. That is exact **conditional work-elision**.

It is not presently a convincing systems speedup. The [original benchmark note](../projects/mimo-mini-project/research_notes/free_lunch.md) reports a 13–17% materialized-loop gain against its nested baseline, but its own vectorized implementation dominates and its streaming version regresses. Inspection of the [benchmark code](../projects/mimo-mini-project/code/cluster2_pruning_demo.py) also shows that the nested baseline rechecks gap flags that a natural one-pass state machine need not recheck. These facts reject the strong speed claim without promoting environment-specific reruns into a new benchmark result. The correct claim is therefore:

> The Farey invariant supplies an exact conditional prediction that can remove a test in a compatible interface. The supplied benchmark does not show a general or even implementation-robust speed payoff.

There is also a quantile caveat. The local certificate is for the finite threshold \(t_N\le2/9\). A critical quantile derived from the continuous BCZ limit does not automatically imply that a finite empirical quantile has crossed that threshold; finite ties and convergence rates must be handled separately.

## 4. Prime fractions: a completed cyclic grid and exact spectral payoff

### 4.1 Why a prime step is special

The new layer at denominator \(n\) is exactly

\[
F_n\setminus F_{n-1}
=
U_n=\left\{\frac an:1\le a<n,\ \gcd(a,n)=1\right\}.
\]

For prime \(p\), every nonzero residue is a unit, so

\[
U_p=\left\{\frac1p,\frac2p,\ldots,\frac{p-1}{p}\right\}.
\]

Since \(0\) is already present, the prime increment completes the cyclic subgroup

\[
G_p=\left\{0,\frac1p,\ldots,\frac{p-1}{p}\right\}\subset\mathbb R/\mathbb Z.
\]

For every Fourier character \(e_m(x)=e^{2\pi i m x}\),

\[
\frac1p\sum_{k=0}^{p-1}e_m(k/p)
=
\begin{cases}
1,&p\mid m,\\
0,&p\nmid m.
\end{cases}
\]

This is finite-group character orthogonality. It gives **exact quadrature/cancellation for all nonresonant Fourier modes**. The nonzero increment alone has normalized coefficient \(-1/(p-1)\) for \(p\nmid m\).

For composite \(n\), the increment includes only units. Define its normalized Fourier coefficient by

\[
\widehat\mu_{U_n}(m)
:=\frac1{\varphi(n)}
\sum_{\substack{1\le a<n\\(a,n)=1}}e^{2\pi i ma/n}
=\frac{c_n(m)}{\varphi(n)}.
\]

Divisor structure therefore creates exact spectral spikes.

### 4.2 Finite demonstration

The reproducible probe found:

- \(p=101\), completed grid, modes \(1,\ldots,100\): maximum coefficient \(1.11\times10^{-14}\) (floating residual; exact value zero); the same-cardinality IID-circle null has median maximum 0.220;
- the \(p=101\) nonzero increment has coefficient magnitude exactly \(1/100=0.01\);
- \(n=105\), \(\varphi(n)=48\): \(c_{105}(35)=-24\), hence an exact normalized spike of magnitude \(1/2\); the same-cardinality IID null at mode 35 has median magnitude 0.121.

The useful payoff is not “primes are magically uniform.” Any complete regular \(n\)-grid has the analogous orthogonality. The prime-specific fact is that **the new primitive Farey layer supplies the entire nonzero grid at once**. In a streaming denominator filtration, primality turns the increment into an exact cyclic design.

Possible interfaces that can cash this dividend are:

- exact integration of nonresonant trigonometric modes;
- deterministic antialiasing or phase-balancing schedules;
- compression of a whole layer by the rule “all nonzero residues mod \(p\)”;
- spectral anomaly detection against composite unit layers.

Each requires a specified frequency band and must account for resonant modes. A random-sampling task with a different loss may prefer a different design.

### 4.3 What remains open in the project’s prime-step work

For an old interior Farey point \(0<f<1\), prime insertion gives the exact rank-discrepancy shear

\[
D_{F_p}(f)=D_{F_{p-1}}(f)+f-\{pf\}.
\]

The local [prime-step preprint](../projects/prime-step-breakthrough/paper/PREPRINT.md) derives useful symmetry and limiting laws for this moving graph, but the global discrepancy-energy change has four interacting terms. A hoped-for universal favorable sign is not established; local computations include counterexamples to simpler sign conjectures. A triangular marginal for \(f-\{pf\}\) is also not enough, because independent uniforms have the same difference marginal. The prime grid’s spectral cancellation is exact; a universal prime-step optimization payoff is not.

## 5. Complex fractions: quotient-group cancellation and global gap laws

### 5.1 A precise meaning of “complex fraction distribution”

There is no canonical linear ordering of complex numbers. The most relevant published analogue is Sayous’s complex Farey set ([open preprint](https://arxiv.org/abs/2407.04380); [International Journal of Number Theory DOI](https://doi.org/10.1142/S1793042125500976)) for an imaginary quadratic field \(K\): primitive fractions \(a/q\) with \(a,q\in\mathcal O_K\), \(0<|q|\le T\), reduced modulo the lattice \(\mathcal O_K\). Nearest-neighbor distance on the complex torus \(\mathbb C/\mathcal O_K\) replaces the one-dimensional consecutive gap.

Sayous proves existence of a limiting nearest-neighbor law after the natural \(T^2\) distance scaling, gives an integral formula for its distribution, and derives explicit tail estimates for Gaussian and Eisenstein fractions. This is a published statistical payoff: a cloud containing on the order of \(T^4\) points has a compressed, predictable gap law. It is not a BCZ map and does not inherit the real cluster-two theorem.

Marklof’s multidimensional Farey paper ([open preprint](https://arxiv.org/abs/1207.0954); [published chapter DOI](https://doi.org/10.1007/978-3-642-36068-8_3)) gives the broader boundary: higher-dimensional Farey point processes have homogeneous-dynamics limits and are non-Poisson, but generally lack the simple explicit density and one-dimensional ordering available in the real case.

### 5.2 A complex prime layer as a finite subgroup

Take the Gaussian integers \(\mathbb Z[i]\) and a Gaussian prime \(\pi\). The completed denominator layer

\[
H_\pi=\left\{z/\pi\pmod{\mathbb Z[i]}:z\in\mathbb Z[i]\right\}
\subset \mathbb C/\mathbb Z[i]
\]

is a finite subgroup of order \(N(\pi)=|\pi|^2\). For a torus character

\[
\chi_{m,n}(x+iy)=e^{2\pi i(mx+ny)},
\]

finite-group orthogonality gives

\[
\frac1{|H_\pi|}\sum_{z\in H_\pi}\chi_{m,n}(z)
=
\begin{cases}
1,&(m,n)\in H_\pi^\perp,\\
0,&(m,n)\notin H_\pi^\perp.
\end{cases}
\]

This is the exact two-dimensional analogue of the prime circle grid. It supports exact quadrature for every character nontrivial on the quotient, while its annihilator identifies the unavoidable resonances.

### 5.3 Finite Gaussian demonstration

For \(\pi=3+2i\), \(N(\pi)=13\). The probe enumerated the 13 classes \(z/\pi\bmod\mathbb Z[i]\) and all 289 integer modes in \([-8,8]^2\):

- 21 modes lie in the annihilator \(3m+11n\equiv0\pmod{13}\);
- across the other 268 modes, the exact coefficient is zero and the floating RMS is \(6.90\times10^{-16}\);
- 500 same-cardinality IID-torus nulls have median RMS 0.275;
- subgroup minimum torus separation is exactly \(1/\sqrt{13}=0.277350\); IID-null median minimum separation is 0.052.

Thus a single Gaussian-prime layer provides two demonstrable payoffs:

1. **spectral balance:** exact cancellation outside the dual/annihilator lattice;
2. **collision avoidance:** a much larger minimum separation than unstructured same-cardinality samples in this finite example.

Again, this is not the full complex Farey cloud. It is a clean denominator-layer mechanism that can be embedded within it. A global algorithmic payoff would need to show that these layerwise symmetries survive accumulation and help a specified task.

## 6. The common mechanism

| System | Simple local ingredient | “Extra” collective structure | Defensible payoff | Main limit |
|---|---|---|---|---|
| Cell-view Bubble | neighbor comparisons/swaps | barrier-sensitive detours; Algotype correlation | robustness and an observer-side secondary behavior | modified concurrent algorithm; toy model; no zero-cost ledger |
| Halley/art simple mapping | fixed pattern → direction | better maze coverage than shuffled/noise patterns | cheap task guidance | narrow maze/mapping family |
| Farey sequence | coprimality + mediant/denominator recurrence | determinant-one adjacency, exact next state, forbidden extreme triples at \(t\le2/9\) | verification, compression, prediction, conditional test-elision | supplied speed benchmark fails against a fair one-pass baseline |
| Prime Farey increment | all nonzero residues mod \(p\) | completed cyclic group and Fourier cancellation | exact quadrature/phase balance; concise layer description | resonant modes; full-grid property itself is not uniquely prime |
| Completed Gaussian-prime layer | nonzero primitive classes plus inherited zero, i.e. \(\mathbb Z[i]/(\pi)\) | finite torus subgroup, dual annihilator, large separation | 2-D quadrature and collision avoidance | the primitive increment alone omits zero; one layer is not global complex Farey dynamics |
| Complex Farey cloud | primitive lattice pairs under a norm cutoff | non-Poisson limiting nearest-neighbor law | calibration/compression of large-cloud gap statistics | no total order or BCZ cluster-two theorem |

The causal chain is:

\[
\text{compact rule}
\longrightarrow
\text{invariant or symmetry}
\longrightarrow
\text{forbidden patterns / exact cancellation / limit law}
\longrightarrow
\text{task-specific interface}
\longrightarrow
\text{payoff}.
\]

The payoff is not an additional causal force. It appears when an external task aligns with a consequence of the invariant that the rule did not separately enumerate. In Levin’s language, the implementation becomes an interface to a richer pattern. In conventional mathematics, the same fact is an exploitable theorem about a biased family. Those descriptions differ metaphysically but predict the same experiment.

## 7. Why this does not violate “no free lunch”

Wolpert and Macready’s original [no-free-lunch theorem](https://doi.org/10.1109/4235.585893) averages optimization performance over a very broad, symmetry-closed family of objective functions. Superior performance on one class is offset elsewhere. Farey sequences, cyclic prime grids, Gaussian quotient groups, and mazes generated by a fixed procedure are highly structured subfamilies. Coprimality, ordering, quotient structure, and the chosen cutoff are prior information.

So “free” must always be relativized:

- free of an additional clustering instruction;
- free of learning a spectral design point by point;
- free of testing a logically forbidden third event;
- not free of the generating rule, representation, proof, preprocessing, or task match.

## 8. Strongest next experiments

1. **Farey structural payoff, not timing theater.** Compare prediction/calibration bits and threshold-test counts for the exact two-state recurrence against event-count-preserving shuffles and equal-marginal Markov nulls. If timing is reported, use a fair one-pass baseline, randomized order, full preprocessing cost, and vectorized/streaming competitors.
2. **Prime layer quadrature.** Pre-register a Fourier band and integration loss. Compare prime increments, composite unit layers, complete composite grids, low-discrepancy designs, and same-cardinality random points. This separates primality from generic regular-grid structure.
3. **Accumulated prime steps.** Test whether layerwise cancellation improves the full Farey empirical measure or a downstream estimator after accounting for old points. The exact rank-shear identity supplies predictions; the global discrepancy sign must remain an outcome, not an assumption.
4. **Complex denominator layers.** Across split and inert Gaussian primes, predict annihilator lattices, exact zero modes, minimum separation, and quadrature error before enumeration. Include random-phase and norm-shell-preserving nulls.
5. **Full complex Farey law.** Fit the \(T^2\)-scaled nearest-neighbor distribution and tail across Gaussian/Eisenstein fields; compare with IID Haar/Poisson, numerator-phase randomization, denominator-shell scrambling, and other lattice processes using KS/Wasserstein distance and held-out tail calibration.
6. **Levin-style perturbation.** Damage/delete a fixed fraction of prime or Gaussian layer points. Measure how spectral error and separation degrade relative to equally damaged random/composite designs. This tests genuine robustness and graceful degradation rather than mere exact symmetry.

## Reproduce the finite demonstrations

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research_notes/levin_farey_payoff_probe.py
rsvg-convert -w 1500 -h 860 research_notes/levin_farey_payoff_probe.svg \
  -o research_notes/levin_farey_payoff_probe.png
```

The probe uses only Python’s standard library, a fixed seed (`20260810`), exact integer checks where available, and 500 matched-null repetitions. A deterministic rerun reproduced byte-identical JSON and SVG hashes. `rsvg-convert` is needed only for the PNG convenience render.

## Evidence labels

- **Published empirical:** sorting, pattern-guided maze exploration, stress-sharing simulation.
- **Published mathematical:** BCZ/Farey dynamics, multidimensional Farey limits, Sayous’s complex nearest-neighbor law, finite-group character orthogonality.
- **Repository-local certificate:** the \(t\le2/9\) extreme-gap triple exclusion and its executable exact-rational certificate.
- **New finite demonstration:** \(F_{250}\) matched shuffle; \(p=101\)/\(n=105\) Fourier comparisons; \(\pi=3+2i\) quotient comparison.
- **Inference:** treating any of these structural dividends as an observer-side Levin-style payoff.
- **Speculation:** a nonphysical Platonic space supplies causal agency or compute beyond what standard mathematics/physics explains.

The evidence supports the inference; it does not require the speculation.

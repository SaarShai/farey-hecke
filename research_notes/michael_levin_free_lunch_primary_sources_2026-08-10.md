# Michael Levin and “free lunch” claims: primary-source research

**Research date:** 2026-08-10. **Scope:** primary/first-party material first; secondary references were used only to locate the underlying paper, code, or interview. This is a bounded search, not a claim of exhaustiveness.

## Executive synthesis

There are three related but importantly different meanings of “free lunch” in Levin’s work.

1. **Sorting algorithms (the bubble-sort example).** Zhang, Goldstein, and Levin do not call the paper a free-lunch paper. They take a familiar sorting objective (put integer values in order), distribute a local rule over one cell per integer, and make the substrate unreliable by freezing cells. They then measure observer-defined trajectories. A cell-view Bubble Sort can temporarily lower its measured Sortedness while routing around a frozen cell, and mixed “Algotypes” can transiently cluster even though no cell reads Algotype. These are empirical emergent competencies of a transparent toy model, not a proof of costless computation or a new reward function. Levin later uses the phrase “free compute”/“intrinsic motivation” in an interview when interpreting the clustering result.

2. **“Free Lunch? Low-Cost Intelligence Through Pattern-Guided Exploration.”** Ertle, Levin, and Scheutz use fixed Halley-fractal and artwork patterns as an unrelated source of structure. With a trivial color-to-action map, structured patterns outperform shuffled/noise controls without task-specific training. A DQN that receives a 1:1 mixture of environmental and fractal input explores and generalizes better than environment-only and pattern-only controls; however, replacing the fractal with uniform noise does **not** significantly change either DQN result. The structured-pattern claim is therefore supported in the simple-mapping lane, while the DQN lane supports only a benefit from nonspecific extra input. The “lunch” is a cheap scaffold or data source, not a free policy: the DQN is trained with explicit rewards, and the inputs are selected, quantized, and evaluated in a narrow maze task.

3. **Multiscale competency architecture (MCA), TAME, and stress sharing.** Levin’s broader framework says that a higher-scale Self can deform the option/energy landscape seen by lower-scale agents. Local homeostatic minimization can then serve a larger-scale goal without micromanagement. Stress sharing is a concrete computational mechanism: a local error signal leaks to neighboring cells, making otherwise blocking cells temporarily plastic and allowing a collective to reach a target. This provides a mechanistic analogy to “simple rules yielding larger payoffs,” but the connection to the bubble experiment is an inference, not a theorem asserted by the MCA papers.

**Guardrail:** neither the sorting paper nor the MCA papers establish zero physical, computational, or energetic cost. “Free lunch,” “free compute,” and “intrinsic motivation” are rhetorical/interpretive labels for useful behavior not explicitly encoded in the local policy. The experiments use explicit observer metrics (Sortedness, error, aggregation, maze exploration, or distance to a target), and only the Free Lunch DQN has an explicit reinforcement-learning reward.

## Bubble-sort setup reconstructed

### Published model

The primary source is Taining Zhang, Adam Goldstein, and Michael Levin, **“Classical Sorting Algorithms as a Model of Morphogenesis: self-sorting arrays reveal unexpected competencies in a minimal model of basal intelligence”** (arXiv v1 submitted 2023-12-15; journal version *Adaptive Behavior*, published online 2024-08-19, volume 33(1), 2025 print, pp. 25–54, DOI `10.1177/10597123241269740`). Open preprint: [arXiv:2401.05375](https://arxiv.org/abs/2401.05375). Journal landing page: [SAGE DOI page](https://doi.org/10.1177/10597123241269740).

The authors explicitly make two substitutions for a conventional sort: (i) no omniscient top-down controller; each element/cell runs a local policy in parallel, and (ii) operations need not succeed; some cells are damaged (“Frozen Cells”). Their declared interpretation is a 1-D abstraction of cells arranging organs along a morphogenetic axis.

State can be represented as an array of cells

\[
x_t=((v_1,a_1,s_1),\ldots,(v_n,a_n,s_n)),
\]

where `v_i` is a fixed integer value, `a_i` is a constant **Algotype** (Bubble, Insertion, or Selection), and `s_i` is Active, movable Frozen, or immovable Frozen. The target is normally increasing order (decreasing variants are used for conflict experiments). The array begins randomized and runs until no cell should move / the measured Sortedness has stabilized.

For **cell-view Bubble Sort**, each active cell can inspect and swap with a left or right neighbor. In the increasing version:

* move left when the cell’s value is smaller than its left neighbor;
* move right when its value is larger than its right neighbor.

This is a distributed, bottom-up rewrite of the familiar central Bubble Sort, not literally the standard single-controller implementation. A main thread activates and monitors one thread per cell. The paper’s description says actions are local and parallel; each cell does not need to know the global array or another cell’s Algotype.

The two Frozen-Cell perturbations are distinct:

* **Movable frozen:** the frozen cell does not initiate a move, but another active cell may move it.
* **Immovable frozen:** it neither initiates nor participates in a swap.

### Metrics (observer-defined, not agent rewards)

* **Total sorting steps:** every comparison or swap (the paper also reports a swaps-only count).
* **Monotonicity error:** count of adjacent violations of the designated increasing/decreasing order.
* **Sortedness Value:** percentage of cells strictly following the designated order.
* **Delayed Gratification (DG):** after a local decrease in Sortedness, the later increase divided by the preceding consecutive decrease (the paper describes numerator `x` = later increase and denominator `y` = preceding decrease). It is intended to detect a route that first goes away from the target and subsequently gains more.
* **Aggregation Value:** in mixed-Algotype arrays, percentage of cells whose directly adjacent neighbors are all the same Algotype.

### Scale and reported outcomes

The headline comparisons use 100-element arrays and 100 repetitions (the exact experiment can vary in frozen-cell count or Algotype mixture).

* Counting swaps only, cell-view Bubble versus traditional Bubble showed no significant efficiency difference (Z = 0.73, p = 0.47). Counting comparisons plus swaps, cell-view Bubble used about 1.5× fewer steps than the traditional version (Z = −68.96, p ≪ 0.01). The authors attribute this to local cells stopping once they are in target positions, whereas the top-down routine continues comparisons.
* With **movable** defects, cell-view Bubble’s mean final monotonicity error was 0 with one frozen cell, 0.8 with two, and 2.64 with three (100 repetitions each). With **immovable** defects, the corresponding means were 1.91, 3.72, and 5.37. Selection is better than Bubble for the immovable case; Bubble is best of the cell-view algorithms for movable defects. All cell-view variants outperformed the corresponding traditional implementations on the reported error-tolerance comparison.
* DG is not just a single accidental backward move: cell-view Bubble’s mean DG rises from 0.24 (no frozen cells) to 0.29, 0.32, and 0.37 with one, two, and three frozen cells. Cell-view Bubble has 0.16 more DG than traditional Bubble (Z = 34.04, p ≪ 0.01). The paper’s short example has value 3 wanting its third position but blocked; it swaps to fourth, temporarily lowering Sortedness, then values 5 and 6 swap and Sortedness rises. The authors call the barrier-sensitive increase a context-dependent rerouting, not random walking.
* In **chimeric arrays**, cells are randomly assigned a fixed Algotype and all still pursue the same numerical sort. Pure cell-view means (100 replicates) are approximately 2448.8 swaps (Bubble), 2482.8 (Insertion), and 1095.5 (Selection); mixed means are 2476.02 (Bubble–Insertion), 1740.9 (Bubble–Selection), and 1534.77 (Insertion–Selection). All mixtures sorted. No cell is given an Algotype-reading or clustering step.
* Aggregation starts at approximately 0.5 and ends at approximately 0.5 when unique values force a final numerical order, but rises significantly during the run above an identical-Algotype negative control (p ≪ 0.01). Peak aggregation was 0.72 (Bubble–Selection), 0.65 (Bubble–Insertion), 0.69 (Insertion–Selection), and 0.62 (all three). With duplicate values (1–10 repeated over 100 cells), clusters can remain after numerical sorting; final values of 0.65 (Bubble–Selection) and 0.70 (Insertion–Selection) support the authors’ efficiency-based explanation. This is a transient or permitted tendency, not evidence that cells optimize an explicitly coded kin-utility.
* When two Algotypes are assigned opposite numerical goals, the collective reaches stable mixed equilibria rather than 100% sorted: reported final Sortedness values are 42.5, 73.73, and 38.31 for the three tested pairings. This is useful evidence that “payoff”/goal compatibility matters, but the payoff is the externally specified order, not a learned scalar reward.

### What is direct and what is inference

Directly stated in the paper: the local rules, frozen-cell perturbations, metrics, DG trend, error tolerance, chimeric sorting, and transient clustering. The paper also stresses that the cell-view algorithms are deterministic, open-loop, and contain no explicit error-handling or progress-monitoring step. It says that all outcomes are consequences of the rules (“no magic”) and that only one emergent behavior (aggregation) was analyzed.

The following are **interpretations**, not measurements of an internal utility: calling DG “planning,” calling aggregation “intrinsic motivation,” calling its computational cost “free,” or treating Sortedness as a payoff known to each cell. Sortedness and Aggregation are calculated by the Probe/observer. The local policy never receives an instruction to maximize aggregation.

### Reproducibility artifact and an implementation caveat

The authors link [Zhangtaining/cell_research](https://github.com/Zhangtaining/cell_research). The public repository’s initial commit is 2023-08-26 and the inspected HEAD is 1fd2bd5 (2024-10-30). In `modules/multithread/BubbleSortCell.py`, `cell_vision = 1`; the rule checks neighboring values and permits an active cell to target Active or Frozen cells. The current `move()` chooses whether to probe right or left with `random.random() < 0.5`; `err_happen = random.random() < 0` disables the injected-error branch. The driver uses `range(100)`, shuffles the values, tests frozen counts 2 and 3 over 100 runs, and waits until `no_cells_should_move` is true. Thus the repository is a useful provenance/reproduction aid, but its current scheduling/random-side detail is not identical to the paper’s prose claim that the algorithm itself is deterministic and non-stochastic. Do not silently treat the current HEAD as the exact code revision used for every published figure.

## Where “free lunch” language appears

### Levin’s interview interpretation (2025)

In Lex Fridman Podcast #486, **“Michael Levin: Hidden Reality of Alien Intelligence & Biological Life,”** published 2025-11-30, Levin walks through the same sort in his own words. Transcript: [Lex Fridman, Michael Levin #2 transcript](https://lexfridman.com/michael-levin-2-transcript). He describes freezing one number without changing the algorithm, observes sorting around it with a temporary Sortedness drop and recovery, and labels this “delayed gratification.” He then describes random Bubble/Selection mixtures: the cells retain the same numerical goal, yet their spatial grouping rises without an Algotype-reading rule. He and Lex discuss this as clustering that came “for free”/“free compute” and as an intrinsic motivation-like behavior.

This is first-person interpretive evidence, not an additional controlled experiment. The transcript is human-generated and warns that it may contain errors. Levin also concedes the important qualification: the phenomenon is not magic and can in principle be modeled or proven from the rules; “free” means that no extra clustering instruction was supplied, not that the physical process has zero cost.

### Ertle–Levin–Scheutz (2025): the paper whose title actually says “Free Lunch?”

Emily A. Ertle, Michael Levin, and Matthias Scheutz, **“Free Lunch? Low-Cost Intelligence Through Pattern-Guided Exploration,”** International Conference on Development and Learning (2025), [Tufts HRI Lab first-party page](https://hrilab.tufts.edu/publications/ertleetal25icdl/), [first-party PDF](https://hrilab.tufts.edu/publications/ertleetal25icdl.pdf), DOI `10.1109/ICDL63968.2025.11204411` ([DOI landing page](https://doi.org/10.1109/ICDL63968.2025.11204411)).

The setup is different from bubble sorting:

* Mazes are randomized modified-Kruskal mazes. Simple-mapping trials use path scale 1; DQN trials use 11×11 mazes with path scale 2. Success is `% explored = visited path squares / total path squares`.
* Halley fractals are generated by Halley iteration with λ = 1, functions `x(x^a − b)` for integer `a ∈ [2,6]`, `b ∈ [1,12]`, 20×20 resolution, and four labels/colors. Sixty National Gallery artworks are color-quantized to four labels; shuffled versions preserve composition but destroy spatial organization; uniform random noise is a control.
* Four simple color-to-action mappings (`[N,E,S,W]` and permutations) produce 400 actions for a 20×20 pattern without task-specific learning. Structured fractals significantly beat their shuffles and noise (fractals p < .0001; art p < .001 vs noise; fractal vs art p = .843); of the top 50 mappings, 46% are fractals and 30% art.
* DQNs have a 25-unit hidden layer and four directional outputs. Rewards include −0.5 for an invalid wall move, a recent-backtrack penalty with window `k = 5`, and (in the later experiments) a +10 target bonus. A 1:1 environmental/fractal input beats environment-only and pattern-only controls (p < .0001) and generalizes from ten training mazes to four novel mazes (p < .0001). But replacing the fractal with uniform noise does not significantly alter the single-maze results (p = .096 for 1:1; p = .999 for pattern-only) or novel-maze results (p = .998 for both comparisons). In the simple-mapping comparison, DQN mean exploration is 0.34 versus 0.26 (p < .001).

Direct claim: structured static patterns can be actionable scaffolds under the simple color-to-action mapping, and mixed nonspecific pattern/sensory input can improve DQN exploration. The DQN ablation does **not** isolate fractal structure as the cause, because uniform noise performs statistically indistinguishably. “Low-cost intelligence” also does not mean no computation—the DQN is extensively trained and has an explicit reward; the input resource is chosen by the experimenter. The paper calls itself an initial attempt and leaves the trade-off between pattern complexity, environment complexity, sensory range, and other success measures open.

## MCA, persuadability, morphospace, and stress sharing

### TAME: goal-directedness across scales

Michael Levin, **“Technological Approach to Mind Everywhere (TAME): an experimentally-grounded framework for understanding diverse bodies and minds,”** *Frontiers in Systems Neuroscience* 16:768201 (published 2022-03-24), DOI `10.3389/fnsys.2022.768201`: [Frontiers full text](https://www.frontiersin.org/journals/systems-neuroscience/articles/10.3389/fnsys.2022.768201/full), [DOI](https://doi.org/10.3389/fnsys.2022.768201), [arXiv:2201.10346](https://arxiv.org/abs/2201.10346).

Direct framework claims:

* A Self is empirically graded by goal pursuit, compound memory, and credit assignment at a scale larger than any one component. Goals and stressors are cybernetic invariants, not necessarily conscious human purposes.
* Selves lie on a continuum of **persuadability**: simple physical systems may be moved by changing conditions; homeostatic circuits by setpoints; animals by reward/training; humans by language and rational argument. The efficient prediction/control method and effort required are empirical questions.
* Biology is a nested holarchy. A higher-level Self can deform the option space/energy landscape for lower-level Selves, so a lower-level unit can follow a local minimization gradient while its behavior serves a higher-scale anatomical or physiological goal.
* Intelligence is competency in navigating arbitrary spaces, including behavioral 3-D space, physiological/transcriptional space, and anatomical **morphospace**, while avoiding local minima. The framework explicitly includes temporary movement away from a goal followed by a larger later gain.

The bridge to bubble sorting is an **inference**: a cell-view local comparison is analogous to a lower-level homeostat, while the externally measured sorted array is an observer-defined higher-level goal. The sorting paper does not instantiate TAME’s bioelectric, memory, or stress machinery.

### Fields & Levin: a mathematical comparison vocabulary

Chris Fields and Michael Levin, **“Competency in Navigating Arbitrary Spaces as an Invariant for Analyzing Cognition in Diverse Embodiments,”** *Entropy* 24(6):819 (published 2022-06-12), DOI `10.3390/e24060819`: [PMC full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC9222757/), [DOI](https://doi.org/10.3390/e24060819).

The paper’s opening formulation is William James’s “fixed goal with variable means.” It treats a problem/action space as observer-constructed states plus a similarity or distance relation, and proposes competency in navigating arbitrary spaces as a scale/substrate-agnostic invariant. Its MCA figure says higher-order systems can distort a subsystem’s energy landscape so that local homeostatic mechanisms achieve goals adaptive at the higher level. It also warns that observer-defined spaces and goals say as much about the observer’s model as about the system.

For comparison, one can write the sorting experiment abstractly as `x_(t+1) = F(x_t, A, η_t)` with observer metric `J(x)` (e.g., monotonicity error) and perturbation `η_t` (frozen cells). DG is a trajectory where `J` first worsens and later improves; aggregation is a second observable `C(x)` not present in the local rule. This equation is my synthesis, not an equation claimed by the sorting paper.

### Darwin’s agential materials: competence as an evolutionary substrate

Michael Levin, **“Darwin’s agential materials: evolutionary implications of multiscale competency in developmental biology,”** *Cellular and Molecular Life Sciences* 80:142 (published 2023-05-08), DOI `10.1007/s00018-023-04790-z`: [PMC full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC10167196/), [DOI](https://doi.org/10.1007/s00018-023-04790-z).

Direct claims include a developmental-physiology layer between genotype and anatomical phenotype; cells, tissues, and organs retain regulative plasticity across metabolic, transcriptional, physiological, and anatomical problem spaces; and an MCA can make evolution’s search more tractable through generalization, reliability, functional intermediates, more linear controls, and pivots to novel problem spaces. Levin’s “Play the Hand You’re Dealt” framing says robust developmental systems handle the conditions they receive rather than assuming a single pristine starting state. The paper also emphasizes that homeostatic measurements, comparison functions, and setpoints can be swapped at different scales while leaving much of the underlying hardware intact.

This is a conceptual/evolutionary rationale for why local competent parts could create a “payoff” at a larger scale. It is not a result that the bubble model is biologically realistic, nor a proof that every simple rule carries useful latent goals.

### Stress sharing: a concrete coordinator for morphogenesis

Lakshwin Shreesha and Michael Levin, **“Stress sharing as cognitive glue for collective intelligences: A computational model of stress as a coordinator for morphogenesis,”** *Biochemical and Biophysical Research Communications* 731:150396 (first publication 2024-07-14; DOI `10.1016/j.bbrc.2024.150396`): [PMC full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC11356093/), [DOI](https://doi.org/10.1016/j.bbrc.2024.150396).

Precise model:

* A 2-D binary grid is initialized by randomly scrambling 0/1 cells. The fixed target is a downsampled smiling-face image (an abstraction related to an “electric face” prepattern).
* Each grid is assigned a developmental marker: (1) stress-sharing competency, (2) movement without stress sharing, or (3) hardwired/no movement. Stressed cells are those whose type/location differs from the target.
* A stressed cell moves through local swaps toward another stressed cell. A fixed, already-correct cell normally blocks movement. With stress sharing, a stressed cell leaks a binary/distress signal; fixed cells in a 3×3 neighborhood can form a temporary tunnel/channel so that the moving cell passes without displacing the fixed cell. Each cell still acts to reduce its own local stress; cooperation does not require an explicit altruism rule.
* Fitness is based on normalized `l2` distance to the target. A genetic algorithm (development → retain the top 10% → random swap mutation) evolves the initial grids and the reorganization marker. Grid sizes are 20×20, 30×30, and 50×50.

Reported outcomes: on 30×30 grids, stress-sharing populations reach the target around generation 400 and use a competency bound of about 4725 swaps, versus roughly 100 swaps without sharing; average cell travel is about 2500 versus 200. On 20×20 grids, stress sharing reaches maximum phenotype around generation 100; without sharing fails to reach maximum by generation 1000. On 50×50, none reaches maximum in 1000 generations, showing a scale/resource limit. Stress sharing expands the modeled “cognitive light cone”: an initial radius around 30 units and influence lasting to about step 85, compared with radius around 5 and termination near step 10 without sharing.

Direct limitation: an external observer cannot reliably infer the target from the stress map alone; visual cues disappear around 50% completion in the tested patterns. The model is a discrete 2-D binary grid, not a biological embryo. The authors list 3-D/higher-dimensional morphospaces, fixed-grid deformation, more cell states, multiscale stress, and computational scaling beyond 50×50 as open problems.

The analogy to the bubble experiment is narrow but useful: both make a barrier/defect visible through local interaction and obtain a larger-scale route without a central controller. Stress sharing adds an explicit communication/feedback channel; the published Bubble model deliberately lacks such feedback, so they should not be conflated.

### 2026 conceptual update: *Mind Everywhere*

Michael Levin and David B. Resnik, **“Mind Everywhere: A Framework for Conceptualizing Goal-Directedness in Biology and Other Domains—Part One”** and **Part Two**, *Biological Theory*, both version-of-record 2026-02-25, DOI `10.1007/s13752-025-00523-6` and `10.1007/s13752-025-00524-5`: [Part One](https://doi.org/10.1007/s13752-025-00523-6), [Part Two](https://doi.org/10.1007/s13752-025-00524-5).

These are conceptual extensions rather than new bubble experiments. The visible abstracts/excerpts restate that goal-directedness is substrate- and scale-independent, that persistence plus plasticity supports minimal intelligence, that “no magic” does not eliminate the usefulness of higher-level generative models, and that a good explanation should be judged by predictive/control fecundity and information-to-effort rather than post-hoc consistency alone. They are useful for terminology and epistemic guardrails; they do not establish a universal free-lunch theorem.

## Source table (primary/first-party)

| Date | Source and identifier | Direct support for this question | Caveat / role in synthesis |
|---|---|---|---|
| 2023-12-15 arXiv; 2024-08-19 online journal | Zhang, Goldstein & Levin, “Classical Sorting Algorithms as a Model of Morphogenesis…” — [arXiv](https://arxiv.org/abs/2401.05375); [DOI](https://doi.org/10.1177/10597123241269740) | Cell-view Bubble rules; frozen defects; DG; chimeric Algotype sorting and aggregation; explicit limitations | Main empirical source. Journal page is publisher-protected from this environment; arXiv is open. |
| 2023-08-26 to 2024-10-30 repository history | [Zhangtaining/cell_research](https://github.com/Zhangtaining/cell_research) | Reproducible implementation details: threads, frozen statuses, random side probe, 100-cell drivers | Current HEAD is not proven to be the exact figure-producing revision; paper’s deterministic prose and code’s side-choice randomness differ. |
| 2025 | Ertle, Levin & Scheutz, “Free Lunch? Low-Cost Intelligence Through Pattern-Guided Exploration” — [Tufts page](https://hrilab.tufts.edu/publications/ertleetal25icdl/), [PDF](https://hrilab.tufts.edu/publications/ertleetal25icdl.pdf), DOI `10.1109/ICDL63968.2025.11204411` | Direct “free lunch” title; Halley fractal/art scaffolds; simple mapping and DQN results | Maze/domain-specific, with explicit DQN training/rewards; in the DQN lane fractal→uniform-noise replacement is nonsignificant; low-cost ≠ zero-cost. |
| 2025-11-30 | Levin interview, Lex Fridman Podcast #486 — [transcript](https://lexfridman.com/michael-levin-2-transcript) | Levin’s own “free compute”/intrinsic-motivation interpretation of sorting aggregation and DG | Human-generated transcript; interpretation, not a new controlled dataset. |
| 2022-03-24 | Levin, “Technological Approach to Mind Everywhere (TAME)” — [Frontiers](https://www.frontiersin.org/journals/systems-neuroscience/articles/10.3389/fnsys.2022.768201/full), [arXiv](https://arxiv.org/abs/2201.10346), DOI `10.3389/fnsys.2022.768201` | MCA, persuadability, goals/stress, option-space deformation, morphospace and temporary detours | Framework/hypotheses; not a sorting experiment. |
| 2022-06-12 | Fields & Levin, “Competency in Navigating Arbitrary Spaces…” — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9222757/), DOI `10.3390/e24060819` | Fixed goal/variable means; observer-defined arbitrary spaces; higher-level energy-landscape deformation | Conceptual invariant, not evidence of costless computation. |
| 2023-05-08 | Levin, “Darwin’s agential materials…” — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10167196/), DOI `10.1007/s00018-023-04790-z` | MCA as an evolutionary substrate; regulative plasticity; search-space smoothing and competency ratchet | Review/perspective; biological claims are broader than the digital toy model. |
| 2024-07-14 | Shreesha & Levin, “Stress sharing as cognitive glue…” — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11356093/), DOI `10.1016/j.bbrc.2024.150396` | Explicit stress-sharing channel; 2-D target-rearrangement model; fitness, competency bounds, light cone, limits | Artificial binary-grid simulation; includes feedback that Bubble deliberately omits. |
| Undated (accessed 2026-08-10) | Levin Lab, “Machine or Living?” — [first-party lab page](https://www.levinlab.dev/machine-or-living) | Plain-language definitions of agency, MCA, persuadability, morphospace, stress and scale | Educational lab page; use papers for formal/dated claims. |
| 2026-02-25 | Levin & Resnik, *Mind Everywhere*, Parts One/Two — [Part One DOI](https://doi.org/10.1007/s13752-025-00523-6), [Part Two DOI](https://doi.org/10.1007/s13752-025-00524-5) | Current conceptual guardrails: no magic, generative explanation, goal-directedness across scales | Recent conceptual articles; not empirical confirmation of “free lunch.” |

## Limitations and interpretive guardrails

1. **No payoff theorem.** The sorting work specifies a target order and calculates external metrics. A cell does not observe a scalar reward, optimize a utility function, or receive an explicit “cluster with kin” instruction. A “payoff” comparison must therefore identify whether the payoff is an observer metric (Sortedness/aggregation), an RL reward (Free Lunch DQN), or an evolutionary fitness function (stress-sharing GA).
2. **No zero-cost claim.** The term “free” means no extra task-specific rule or static pattern source, not no CPU time, energy, memory, or training. The sorting code performs comparisons/swaps and uses threads; the Free Lunch DQN uses 50k–200k training timesteps and explicit rewards; the stress model spends a bounded number of swaps.
3. **Toy-model scope.** Bubble sorting is one-dimensional, integer-valued, and finite. Stress sharing is a fixed 2-D binary grid with a smiling-face target. Neither establishes a general theorem for biology, arbitrary algorithms, or arbitrary tasks.
4. **Observer dependence.** TAME and Fields–Levin explicitly make problem spaces and goals observer-centered. DG and Aggregation are therefore useful behavioral probes, but calling them “intrinsic goals” is an interpretive stance that needs perturbation and control experiments.
5. **Stochasticity/version risk.** The published sorting discussion says deterministic/open-loop; the inspected public repository includes thread scheduling and random left/right probing, although its injected-error branch is disabled. Exact figure provenance should be checked against archived commit/data before claiming that every run is deterministic.
6. **Limited emergent-behavior search.** The sorting paper tests aggregation as its principal unexpected behavior and itself says other behaviors may remain undiscovered. It does not prove that the observed clustering is inevitable rather than a contingent consequence of relative algorithm speeds and the chosen array geometry.
7. **Stress-model scaling.** The stress paper reports no 50×50 run reaching maximum fitness in 1000 generations and lists higher-dimensional morphospaces, deformable grids, more cell states, and multiscale stress as open work. The model also cannot be read backward by an external observer to recover the target from stress maps.
8. **Free Lunch study limits.** Results are maze-exploration percentages under selected mappings, pattern sizes, seeds, and reward functions. The DQN experiment does not establish that fractal structure causes its improvement, because uniform-noise substitution is nonsignificant. The paper calls the work an initial attempt and leaves other environments and success measures unresolved.

## Search boundaries and URL checks

Search terms included `free lunch`, `free intelligence`, `free compute`, `intrinsic motivation`, `delayed gratification`, `competency`, `multiscale competency architecture`, `persuadability`, `stress sharing`, `morphospace`, `goal-directedness`, and `sorting`. I searched Levin/Tufts/HRI lab pages, arXiv, DOI metadata, PMC/Europe PMC, the linked GitHub repository, and the Levin interview transcript. Where a secondary index or search result surfaced a lead, I followed it to the author/lab page, preprint, repository, DOI record, or full-text archive cited here. I did not search private lab notebooks, unpublished branches, all talks/videos, or every citation to Levin; no exhaustiveness claim is made.

The URL checks used `curl -L` on 2026-08-10. Open/redirecting endpoints included arXiv, GitHub, Tufts HRI page/PDF, Lex transcript, Frontiers, Levin Lab, PMC, Elsevier DOI, and Springer DOI pages. The SAGE journal DOI resolved but returned HTTP 403 to this client; the Entropy/MDPI DOI likewise resolved but returned HTTP 403, so the open arXiv/PMC copies were used. The IEEE DOI resolved to an IEEE landing page (HTTP 202). These status codes indicate access behavior, not a broken identifier.

## Compact handoff

* **Changed path:** `research_notes/michael_levin_free_lunch_primary_sources_2026-08-10.md` in `/tmp/farey-levin-research-019fec46` (the only file intentionally created).
* **Strongest evidence:** the bubble paper’s Methods/Results and linked code for the exact local rule, frozen-cell perturbations, DG and aggregation numbers; the first-party HRI PDF for the paper literally titled “Free Lunch?”; TAME/Fields–Levin/Darwin papers for MCA and arbitrary-space competence; stress-sharing PMC for a concrete local-error communication mechanism; Levin’s 2025 interview for his own “free compute” interpretation.
* **Uncertainties:** exact figure-producing GitHub revision and whether repository side-probe randomness was present in every published run; publisher pages blocked by 403; “free” is an interpretive metaphor, not a measured zero-cost quantity; no claim of an exhaustive literature/talk search.
* **Status:** complete for the bounded primary-source research request; no other worktree files were edited.

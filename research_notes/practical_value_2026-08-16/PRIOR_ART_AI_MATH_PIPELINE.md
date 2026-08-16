# Prior-Art Survey: AI-Verified Mathematics Pipeline

**Date:** 2026-08-16  
**Scope:** Comparison of the repository's conjecture-to-certificate workflow with formal-mathematics, validated-numerics, AI-discovery, and industrial-verification prior art.

## Executive Summary

The repository contains a serious collection of ingredients for AI-assisted mathematical research: parallel idea generation, explicit numerical kill tests, Arb/Acb ball arithmetic, analytic tail arguments, Lean 4 projects, Harmonic's Aristotle service, adversarial review rounds, and hash-bearing receipts. It also contains unusually candid negative records. Examples include killed conjectures, explicit separation of high-precision numerics from interval certification, a theorem-grade **NO** for the flagship closed-contour attempt at both attempted matrix sizes, and a lesson requiring an on-disk proof artifact before accepting an Aristotle status claim.

It does **not**, on the evidence inspected, yet constitute a single demonstrated end-to-end software pipeline. `engine/certify/` is empty. Important certification code lives in a side worktree rather than the current branch. The repository's own trust-boundary audit says that exact branch tails and finite Arb matrices are rigorous, while infinite-dimensional determinant control in the audited stack remains heuristic. The flagship q=5 certificate failed its boundary-nonvanishing gate, and its determinant/sector identification retained open scope. The right comparison is therefore:

> a promising, domain-specific research workflow and evidence-governance discipline, not a completed general AI theorem-discovery-and-formal-verification platform.

Most individual components are established prior art. The potentially valuable contribution is their **operational composition**: generate many candidates, try to kill them early, promote only bounded claims, attach machine-readable provenance, submit suitable finite lemmas to Lean automation, and subject the connecting analytic argument to fresh adversarial review. That composition is not obviously unique—recent AI-mathematics programs use similar generate/evaluate/formalize loops—but this repository's emphasis on negative receipts, rounded-down margins, and explicit epistemic tiers is useful and less common in public AI-math demonstrations.

## Local Pipeline: What Is Actually Demonstrated

The requested architecture is visible across the named research tree, but the evidence is uneven.

- **Conjecture generation and falsification:** The synthesis records live conjectures separately from falsified or dead directions, including failed spectroscopy and sign conjectures. This is substantive evidence of a kill-first workflow, although it is a collection of research runs rather than a stable autonomous-scout API. See [`00_SYNTHESIS.md`](../rh_goals_2026-08-14/00_SYNTHESIS.md).
- **Validated numerics:** The audited spectral stack uses python-flint Arb/Acb balls, exact Hurwitz closures for certain infinite branch sums, interval matrix determinants, and closed-contour enclosures. This is real validated-numerics work.
- **Trust boundary:** The repository itself says no audited infinite-operator geometry claim earns pure `[CERTIFIED-INTERVAL]`; relevant results are `[CERTIFIED-MODULO-HEURISTIC]` because a finite window of determinant increments is extrapolated to all later dimensions. See [`CERTIFIED_VS_HEURISTIC.md`](../rh_goals_2026-08-14/lane_b/CERTIFIED_VS_HEURISTIC.md).
- **Failed certificate retained:** The flagship R2/R3 run reports theorem-grade NO at `N=128` and `N=160` because the first closed boundary segment's determinant enclosure contains zero. It also says that even a successful R2/R3 winding result would not by itself close the resonance/zeta theorem because sector/factorization and determinant identification remain outside that verdict. See [`R2R3_FLAGSHIP_CERT.md`](../rh_goals_2026-08-14/lane_g/R2R3_FLAGSHIP_CERT.md).
- **Lean and Aristotle:** There are genuine Lake projects, fresh local builds, and axiom reports. At least one Aristotle-returned Prony project is present as a buildable artifact. This establishes useful service-to-local-replay practice, but not automatic formalization of the whole numerical theorem chain. See [`LEAN_REVERIFY.md`](../rh_goals_2026-08-14/lane_d/LEAN_REVERIFY.md).
- **Adversarial review:** Multiple cold-context reviews locate mathematical and bibliographic defects, preserve theorem-grade NO verdicts, and sometimes validate repaired local lemmas. This is a meaningful governance layer, but reviewers are not a formal trust anchor and their judgments still require source/artifact checks. See [`ADVERSARIAL_REVIEW_V7_R5V3.md`](../rh_goals_2026-08-14/lane_g/ADVERSARIAL_REVIEW_V7_R5V3.md).
- **Receipts:** Hashes, toolchain versions, run parameters, negative controls, exact decimal bindings, and axiom footprints appear frequently. The repository also documents a concrete failure mode: an Aristotle API status was once recorded as proved before the artifact was downloaded, while the repository still contained a sorry-only dispatch. That incident supports the value of “receipts before claims,” while showing the gate is procedural rather than automatically enforced everywhere.

This distinction matters throughout the comparisons below. “Our pipeline has” means “the repository contains and sometimes demonstrates this practice,” not “one command reliably executes the entire architecture.”

## DeepMind AlphaProof

**What AlphaProof has.** AlphaProof couples a Lean proof environment to a learned proof-search system trained with an AlphaZero-style reinforcement-learning loop. For the 2024 IMO, problems were manually formalized; the system generated candidates and proved or disproved them in Lean, with successful proofs feeding back into training. Combined with AlphaGeometry 2, it reached silver-medal level, although some solutions took up to three days and manual translation remained part of the workflow. The later paper reports roughly 80 million formal problems and test-time reinforcement learning. DeepMind published substantial methodology, but the model, weights, training system, and full compute stack have not been made into a generally usable open-source project. [DeepMind's official AlphaProof account](https://deepmind.google/blog/ai-solves-imo-problems-at-silver-medal-level/), [Nature paper](https://www.nature.com/articles/s41586-025-09833-y).

**What this repository has that AlphaProof publicly lacks.** The local workflow addresses a different layer: open-ended research conjecturing, numerical falsification, interval certification, explicit analytic truncation tails, provenance receipts, and adversarial review of the bridge between computation and theorem. Public AlphaProof material emphasizes formal proof search once a statement is formalized; it does not present an Arb-style validated-numerics stage, machine-readable experiment receipts, or a public cold-review protocol.

**What AlphaProof has that this repository lacks.** AlphaProof has a purpose-built, large-scale reinforcement-learning prover, millions of formal training problems, demonstrated performance on independently selected elite problems, and DeepMind-scale search infrastructure. The local repository mostly delegates finite Lean obligations to a third-party service and has no comparable trained proof-search model, benchmark, ablation study, or independent competition-grade evaluation. AlphaProof's final successful Lean proofs also enjoy a clearer kernel-checked endpoint than the local flagship numerical theorem, whose infinite-dimensional bridge remains incomplete.

## DeepMind AlphaEvolve

**What AlphaEvolve has.** AlphaEvolve is an evolutionary coding agent: Gemini models propose programs, automated evaluators run and score them, and a program database drives further evolution. DeepMind reports improvements in data-center scheduling, chip design, AI training, matrix multiplication, and mathematical constructions. Its strength is broad, evaluator-guided optimization over whole codebases. The evaluator establishes the scored property; it does not automatically convert every result into a formal proof. [DeepMind's official AlphaEvolve description](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/).

**What this repository has that AlphaEvolve publicly lacks.** The repository has an explicit ladder from numerical evidence to interval enclosure to Lean lemmas and audit receipts, plus a culture of retaining failed certification margins. AlphaEvolve's public presentation does not expose a comparable mathematical trust ledger, formal-proof endpoint for all discoveries, or reproducible cold-review archive.

**What AlphaEvolve has that this repository lacks.** AlphaEvolve has a coherent evolutionary search engine, systematic evaluator feedback, substantial production deployments, and evidence that the same framework transfers across domains. The local “scouts” are orchestration patterns over language-model agents, not a documented evolutionary population with controlled selection, replayable evaluator benchmarks, or measured discovery efficiency.

The closest published analogue to the local philosophy is DeepMind's later large-scale mathematical exploration with Terence Tao: a corpus of dozens of problems, conservative executable scoring, human inspection, explicit warnings that verifier bugs can be exploited, and a selected case that moved from an evolved construction through informal proof to AlphaProof/Lean. The accompanying repository publishes problem definitions and discovered programs but not the AlphaEvolve runner. This materially weakens any claim that the local generate–falsify–formalize composition is unprecedented. The local differentiator is narrower: Arb-oriented analytic certification plus persistent negative receipts and cold-review gates. [Tao's account](https://terrytao.wordpress.com/2025/11/05/mathematical-exploration-and-discovery-at-scale/), [paper](https://arxiv.org/abs/2511.02864), [problem repository](https://github.com/google-deepmind/alphaevolve_repository_of_problems).

## DeepMind FunSearch

**What FunSearch has.** FunSearch pairs an LLM with executable evaluators and evolves short programs. It produced improved cap-set constructions and bin-packing heuristics; the generated programs made the constructions inspectable. Its correctness story is strongest when the evaluator can exhaustively or mathematically check the finite construction, not when a program score is mistaken for a general theorem. [DeepMind's official FunSearch account and Nature citation](https://deepmind.google/blog/funsearch-making-new-discoveries-in-mathematical-sciences-using-large-language-models/).

**What this repository has that FunSearch lacks.** The local workflow is broader than combinatorial program search: it explicitly tries to move from exploratory numerics through rigorous real/complex enclosures and analytic tails into Lean, while recording the claim boundary. It also includes adversarial review of theorem statements, citations, and hidden analytic assumptions.

**What FunSearch has that this repository lacks.** FunSearch has a clearly specified search algorithm, published scientific case studies, evaluator-defined objective functions, and externally visible new constructions. The repository has not yet reported a comparably clean, independently validated discovery attributable to the full scout-to-Lean chain. Its strongest evidence is process quality and several bounded artifacts, not a headline theorem produced end to end.

## Lean and Mathlib Workflows

**What Lean/mathlib has.** Lean supplies a small trusted kernel; mathlib supplies a large, community-maintained library, tactics, documentation, code review, continuous integration, style conventions, and reusable abstractions. Mathlib reports more than two million lines of formalized mathematics and requires human expert review for contributions. Mature projects typically pin Lean/mathlib revisions, maintain Lake builds, use blueprints or dependency graphs, eliminate `sorry`, inspect axioms, and rely on CI. [Lean's mathlib overview](https://lean-lang.org/use-cases/mathlib/), [mathlib documentation index](https://leanprover-community.github.io/documentation.html), and the [mathlib paper](https://arxiv.org/abs/1910.09336).

**What this repository has that ordinary mathlib workflows lack.** Mathlib is a formal library and review process, not an experimental-discovery pipeline. The repository adds numerical scout stages, falsification gates, Arb receipts, external prover dispatch records, explicit “certified vs heuristic” labels, and cold reviews aimed at the informal analytic bridge. Those are useful pre-formal and extra-formal layers.

**What Lean/mathlib has that this repository lacks.** Mathlib has a coherent public codebase, stable contribution standards, broad reusable foundations, ongoing expert review, and community-level independent scrutiny. The repository's formal artifacts are distributed across multiple Lake projects and dispatch directories; much of the research argument remains in Markdown and Python rather than in the kernel. A local `lake build` and `#print axioms` receipt verifies the proposition actually encoded, but not that it faithfully captures the intended analytic claim. The repo needs statement audits, consolidated dependency maps, pinned reproducible builds, and preferably upstream-quality formal components before it can claim mathlib-level assurance.

## Terence Tao's AI + Lean Experiments

**What Tao's workflows have.** Tao has emphasized blueprint-first formalization: break an informal proof into granular lemmas, use `sorry` placeholders as parallel tasks, and let Lean check independently contributed proofs. His projects combine human mathematical steering, collaborative formalization, CI, and increasing use of AI for localized proof completion. The Equational Theories Project combined Lean with automated theorem provers to settle and formally verify more than 22 million universal-algebra implications. Tao has also stressed that statement mistranslation is not caught merely because a Lean proof typechecks. [Lean 4 proof tour](https://terrytao.wordpress.com/2023/12/05/a-slightly-longer-lean-4-proof-tour/), [Equational Theories Project posts](https://terrytao.wordpress.com/tag/equational-theory-project/).

**What this repository has that Tao's public experiments generally lack.** The local process places validated complex numerics, proven truncation-tail aspirations, parameter/hash receipts, and explicit margin policies at the center. Tao's collaborative Lean projects are primarily proof-engineering and theorem-exploration efforts, not a standard Arb-to-Lean certificate pipeline.

**What Tao's efforts have that this repository lacks.** They have public collaboration, theorem blueprints, GitHub CI, substantial human mathematical review, and results that can be inspected by a wide formalization community. ETP also has scale and a clearly enumerable formal problem universe. The local workflow is more private, heterogeneous, and dependent on agent reports and a commercial prover service. Its cold reviewers are valuable but are not a substitute for sustained domain-expert and community review.

## Flyspeck

**What Flyspeck has.** Flyspeck completed a formal proof of the Kepler conjecture using HOL Light and Isabelle. It formalized the mathematical reduction, checked nonlinear inequalities, and used formally justified computation across a large proof development. It is a landmark demonstration that a theorem previously dependent on extensive computation can be rebuilt to a proof-assistant trust standard. [Official published account](https://www.cambridge.org/core/journals/forum-of-mathematics-pi/article/formal-proof-of-the-kepler-conjecture/78FBD5E1A3D1BCCB8E0D5B0C463C9FBC), [preprint](https://arxiv.org/abs/1501.02155).

**What this repository has that Flyspeck lacks.** Flyspeck predates LLM-driven conjecture scouts, cloud autoformalization, and receipt-oriented agent governance. The local workflow is much faster and more exploratory: it can spawn candidate directions, falsify them numerically, and route bounded lemmas to a prover service.

**What Flyspeck has that this repository lacks.** Flyspeck has a completed, published, end-to-end formal proof of a major theorem, with computational inequalities integrated into the formal argument. The repository's key numerical certificate is not imported into Lean as a verified checker theorem, the infinite-dimensional tail bridge is not closed, and the flagship claim remains NO. Flyspeck therefore dominates on assurance, completeness, publication, and independent review; the local process dominates only on flexible AI-assisted exploration and audit ergonomics.

## Coq/Rocq and Isabelle Certified-Numerics Traditions

**What they have.** The CoqInterval/Rocq Interval library provides reflected tactics for proving real inequalities involving elementary functions, with interval subdivision, Taylor models, and proofs checked by the assistant. Flocq formalizes floating-point arithmetic. Isabelle's Archive of Formal Proofs contains interval-analysis developments and many executable, code-generated verified algorithms. These ecosystems have long distinguished an untrusted fast computation from a small verified checker or a proof-producing tactic. [CoqInterval official site](https://coqinterval.gitlabpages.inria.fr/), [CoqInterval paper](https://guillaume.melquiond.fr/doc/15-jar.pdf), [Isabelle AFP Interval Analysis](https://www.isa-afp.org/browser_info/current/AFP/Interval_Analysis/document.pdf).

Gappa is another important bridge: it proves floating- and fixed-point bounds and can emit Rocq proof certificates for mechanical checking. Its own documentation refuses proof-producing mode for an unconstrained optimization that would introduce unsupported assumptions—a useful precedent for making “fast but unverified” modes visibly incompatible with proof claims. [Flocq](https://flocq.gitlabpages.inria.fr/), [Gappa](https://gappa.gitlabpages.inria.fr/), [Gappa invocation and proof backends](https://gappa.gitlabpages.inria.fr/gappa/invoking.html).

**What this repository has that those traditions usually lack.** The local workflow adds LLM conjecture generation, external AI proof search, adversarial natural-language review, run receipts, and explicit research-portfolio management. It also targets special-function and transfer-operator computations where general proof-assistant interval tactics may not yet offer adequate performance or libraries.

**What those traditions have that this repository lacks.** They reduce the trust placed in the interval implementation by proving the arithmetic or checking generated certificates inside the prover. The local Arb calculations rely on FLINT/Arb and Python bindings as part of the trusted computing base; the receipts record that computation but do not make Lean verify Arb's rounding, every matrix operation, or the analytic tail theorem. A major upgrade would be a small Lean/Rocq/Isabelle checker for exported rational/interval certificates and a formal theorem connecting that checker to the target mathematical statement.

## INTLAB

**What INTLAB has.** INTLAB is a mature MATLAB/GNU Octave environment for interval arithmetic, multiple precision, verified linear algebra, and computer-assisted proofs, with applications ranging from control and PDEs to dynamical systems. It benefits from decades of numerical-analysis expertise and user-facing matrix operations. [Official INTLAB site](https://www.tuhh.de/ti3/intlab/).

**What this repository has that INTLAB lacks.** INTLAB is a validated-numerics toolkit, not an autonomous conjecture/formalization/review system. The repository adds AI idea generation, evidence ledgers, Lean projects, and research claim governance.

**What INTLAB has that this repository lacks.** INTLAB has a mature general-purpose numerical API, extensive literature, broad applications, and established algorithms for verified linear systems and nonlinear problems. The local certificate code is bespoke, distributed, and tied to a narrow spectral problem. It lacks INTLAB's packaging, documentation, user base, and generalized validated solver repertoire.

## Arb/FLINT

**What Arb has.** Arb provides arbitrary-precision real and complex ball arithmetic, special functions, polynomials, power series, matrices, integration, and root finding. Its inclusion contract guarantees that output balls enclose exact results for every input point represented by the input balls. The documentation explicitly explains that users must supply justified bounds for infinite-series tails; ball arithmetic automatically handles rounding, not missing mathematics. Arb was merged into FLINT in 2023. [Arb/FLINT documentation](https://arblib.org/index.html), [ball semantics and tail example](https://fredrikj.net/arb/using.html), [Arb paper](https://arxiv.org/abs/1611.02831).

**What this repository has that Arb lacks.** The repository supplies a domain-specific layer around Arb: transfer-operator formulas, Hurwitz closures, contour gates, receipts, negative controls, candidate discovery, and attempts to connect the numerical objects to Lean theorems.

**What Arb has that this repository lacks.** Arb is the mature numerical foundation doing most of the hard rounding work. The local novelty cannot include “rigorous arbitrary-precision balls” themselves. More importantly, Arb's correctness contract applies only to the implemented finite expression plus correctly supplied analytic error bounds. The repository's own audit shows exactly where a heuristic dimension tail was treated separately from rigorous branch tails. Until the dimension/infinite-operator truncation theorem is proved and bound to the code, “uses Arb” must not be shortened to “the theorem is certified.”

## kv-Library and Related Validated-Numerics Ecosystems

**What kv has.** The kv-library is a C++ library for verified numerical computation, offering interval elementary functions and solvers for nonlinear equations, ODEs, and related problems. Its documentation also makes low-level rounding-mode requirements explicit; using an unsuitable number type can yield unverified results. [Official kv site](https://verifiedby.me/kv/index.html), [interval component documentation](https://verifiedby.me/kv/interval/index-e.html).

**What this repository has that kv lacks.** The repository adds AI scouting, formalization service integration, adversarial review, and provenance policy around domain-specific mathematics.

**What kv has that this repository lacks.** kv has a reusable solver ecosystem and expertise in validated differential equations and nonlinear analysis. The repository has no comparable general numerical library; it is an application built on python-flint. kv's warning about rounding configuration also illustrates why local receipts should bind library versions, architecture-sensitive settings, and exact inputs—not merely report a final interval.

## Commercial and Industrial Verified Computation

This category is heterogeneous; most offerings verify software, hardware, policies, or finite models rather than produce new pure mathematics.

**What industry has.** AWS deploys automated reasoning in access-policy analysis and security tooling; its Bedrock Automated Reasoning checks translate selected natural-language claims into formal logic and report untranslated material, explicitly acknowledging that translation can err. AdaCore's SPARK Pro combines contracts, flow analysis, proof, IDE integration, and standards-oriented assurance for high-integrity software. Wolfram Language supports interval objects and interval-aware elementary functions. Specialist firms such as Galois and formal-methods vendors build verified cryptographic, systems, and assurance artifacts for customers. [AWS Automated Reasoning concepts](https://docs.aws.amazon.com/bedrock/latest/userguide/automated-reasoning-checks-concepts.html), [AWS industrial deployments](https://aws.amazon.com/blogs/security/aws-security-profile-byron-cook-director-aws-automated-reasoning-group/), [SPARK User's Guide](https://docs.adacore.com/spark2014-docs/html/ug/en/introduction.html), [SPARK Pro](https://www.adacore.com/sparkpro), [Wolfram interval documentation](https://reference.wolfram.com/language/guide/IntervalArithmetic.html.en).

**What this repository has that industrial offerings lack.** The repository targets open-ended mathematical discovery and combines conjecture exploration with analytic and formal proof aspirations. Commercial tools usually start from a customer-supplied specification; they do not decide which new theorem is interesting, invent the analytic reduction, or run a research novelty program.

**What industry has that this repository lacks.** Industrial systems have productized workflows, support, stable APIs, defined threat/trust models, qualification evidence, regression suites, access controls, and deployments against real operational consequences. They are typically precise about the verified specification. The repository lacks a service-level contract, supported installation, unified orchestration, systematic certificate checking, and independent security/quality assurance. Its receipt discipline resembles industrial evidence management but is not yet an industrial assurance case.

Validated computation also has commercial scientific products rather than only formal-software tools. COSY INFINITY, for example, offers Taylor-model-based validated integration, range bounding, and optimization for accelerator and dynamical-system applications. These products exceed the local repository in mature numerical UX and deployment history, while lacking its AI/Lean research-orchestration layer. [COSY INFINITY](https://www.bmtdynamics.org/cosy/), [COSY manual](https://www.bmtdynamics.org/cosy/manual/index.html).

## Draft-Sketch-Prove

**What it has.** Draft-Sketch-Prove maps informal proofs into formal proof sketches and uses an automated prover to solve the resulting subgoals. The original work evaluated both human- and language-model-generated drafts and improved proof success on competition problems from 20.9% to 39.3%. It cleanly separates informal planning, formal skeletal structure, and kernel-checked completion. [Paper](https://arxiv.org/abs/2210.12283), [ICLR publication](https://openreview.net/pdf/cfd03f19d20263d9c1d1cc026a2b3528392fc857.pdf).

**What this repository has that DSP lacks.** The local pipeline includes pre-proof empirical science: candidate generation, numerical refutation, validated numerics, truncation-tail analysis, and audit receipts. DSP begins with an informal proof to formalize.

**What DSP has that this repository lacks.** DSP has a named algorithm, benchmark evaluation, ablations, and measured proof-success improvement. The repository has no controlled evaluation showing that its scout/falsifier/reviewer stages improve theorem yield, reduce false claims, or lower Lean cost relative to a baseline.

## LeanDojo

**What LeanDojo has.** LeanDojo is an open-source environment for extracting proof states, premises, and tactics from Lean repositories and interacting with Lean programmatically. It introduced retrieval-augmented proving, datasets, benchmarks, and reproducible tooling; current work is moving to LeanDojo-v2, while the original repository is marked deprecated for new projects. [Official repository](https://github.com/lean-dojo/LeanDojo), [project site](https://leandojo.org/), [LeanDojo-v2 description](https://openreview.net/forum?id=tnx1VvrcAn).

**What this repository has that LeanDojo lacks.** LeanDojo focuses on formal theorem proving and data infrastructure, not numerical discovery, interval certificates, analytic tail derivation, or claim receipts. The local workflow provides those surrounding research stages.

**What LeanDojo has that this repository lacks.** LeanDojo has a public API, datasets, standardized training/evaluation splits, premise retrieval, prover baselines, and reproducibility for learned theorem-proving research. The local pipeline has no comparable formal benchmark and largely treats Aristotle as an external prover endpoint. Integrating LeanDojo-style tracing and benchmarks would make local claims about autoformalization efficiency measurable.

## Morph / Harmonic Aristotle

**What Aristotle has.** Harmonic's Aristotle is a hosted agent that accepts Lean projects and attempts autonomous proving or formalization, advertised as running for up to 24 hours without human intervention. The repository contains SDK/CLI dispatch receipts and downloaded projects, so this is not merely a hypothetical dependency. [Official Aristotle service](https://aristotle.harmonic.fun/).

**Morph is a separate project.** Morph Labs released Morph Prover v0.7B, an open-weight Mistral-based Lean assistant with a local CLI. Its own model card describes limited English-only testing and possible inaccuracies; important data/index infrastructure remained proprietary. It offers a locally inspectable assistant that this repository does not supply, but no public scout-to-validated-numerics-to-formal-proof pipeline. No authoritative source located establishes a relationship between Morph Labs and Harmonic, so they must not be conflated. [Morph model card](https://huggingface.co/typeof/morph-prover-v0-7b-sharded), [Morph CLI](https://github.com/morph-labs/morph-prover-cli).

**What this repository has that Aristotle lacks.** Aristotle is a proving/formalization service, not a complete research method. The repository supplies problem selection, numerical falsification, analytic certificate construction, local replay, axiom inspection, adversarial review, and a receipt policy. The documented incident where an API status preceded the on-disk result is especially instructive: service status is not proof evidence until the exact returned project is downloaded, checked for `sorry`/axioms, built under a pinned toolchain, and tied to the intended statement.

**What Aristotle has that this repository lacks.** Aristotle provides the specialized proof-search capability, infrastructure, and service operation. The local repository has no open replacement, no visibility into model/training/search internals, no availability guarantee, and limited ability to reproduce how a proof was found. Dependence on a closed service is a reproducibility and longevity risk even when the final Lean proof can be replayed locally.

## Other AI-Driven Conjecture and Formalization Pipelines

Automated conjecturing predates LLMs: systems such as Graffiti and MATHsAiD generated conjectures from structured data or theories and sometimes passed them to theorem provers. Modern work adds language models, neuro-symbolic lemma conjecturing, formal statement generation, multi-agent proof search, and proof-assistant feedback. Representative public work includes MATHsAiD's theory-exploration loop and recent systems such as Lemmanaid for useful lemma conjecturing. [MATHsAiD](https://link.springer.com/article/10.1007/s10489-017-0954-8), [Lemmanaid](https://openreview.net/forum?id=QS8X04Q0Ov).

**What this repository has that much of this literature lacks.** The repository treats numerical falsification and validated analysis as first-class stages between conjecture and proof, and it records operational evidence and negative outcomes. Many formal-conjecturing systems stay entirely inside a symbolic theory; many LLM proof agents begin from a fixed theorem statement.

**What the literature has that this repository lacks.** Prior systems provide explicit algorithms, corpora, novelty/interestingness criteria, proof-rate metrics, and peer-reviewed evaluations. The repository's scout process does not yet define a reproducible candidate language, deduplication rule, interestingness measure, contamination control, or prospective success metric. Without those, “autonomous conjecture scout” is a workflow description rather than a scientifically evaluated system.

Two further comparisons sharpen the verdict:

- **Ramanujan Machine** searches systematically for continued-fraction and formula conjectures and re-evaluates candidates at greater depth to reject numerical false positives. Its papers explicitly allow conjectures to remain unproved. The local process has stronger intended promotion gates; Ramanujan Machine has a clearer open search algorithm and larger focused candidate ecosystem. [Paper](https://www.nature.com/articles/s41586-021-03229-4), [code](https://github.com/RamanujanMachine/RamanujanMachine).
- **DeepMind Aletheia / Gemini Deep Think** is a very close contemporary comparator: large-scale autonomous generation, literature search, natural-language verification, revision/restart loops, and human expert screening on open problems. Its own detailed audit found many technically plausible outputs fundamentally flawed or mathematically misdirected, and warned that formal verification cannot by itself establish that the intended theorem was formalized. Public prompts and artifacts exist, but the backend is not reproducible. The local workflow adds explicit numerical falsification, Arb/tail certification, Lean dispatch, and receipt gates; Aletheia has far greater scouting scale and systematic human meaning review. [Overview](https://arxiv.org/abs/2602.10177), [official artifacts](https://github.com/google-deepmind/superhuman/tree/main/aletheia), [Erdős case-study audit](https://arxiv.org/html/2601.22401v3).

## Cross-Cutting Comparison

| Capability | Strongest relevant prior art | Local status |
|---|---|---|
| Large-scale learned Lean proof search | AlphaProof, LeanDojo-family provers, Aristotle | Uses Aristotle; no local trained prover or benchmark |
| Evaluator-guided discovery | FunSearch, AlphaEvolve, older automated conjecturing | Agent scouts and kill tests exist; search algorithm and metrics are not consolidated |
| Formal library and kernel checking | Lean/mathlib, Coq/Rocq, Isabelle, HOL Light | Genuine Lean builds and axiom reports; only bounded parts formalized |
| Validated numerics | Arb/FLINT, INTLAB, kv, CoqInterval | Serious Arb/Acb use; branch tails can be rigorous; audited dimension tail remains heuristic |
| End-to-end computer-assisted theorem | Flyspeck and many domain-specific CAPs | Not yet: flagship certificate is NO and analytic/formal bridges remain open |
| Industrial assurance workflow | SPARK, AWS automated reasoning, specialist formal-methods practice | Strong receipt instincts; no productized assurance case or unified runner |
| Adversarial claim review | Peer review, red teams, independent formal replay | Multiple fresh reviews and explicit negative verdicts; reviewer outputs are not themselves proof |
| Reproducible evidence | Formal CI, proof artifacts, benchmark datasets | Many hashes/receipts, but code is split across branches/worktrees and `engine/certify/` is empty |

## Positioning Verdict

### Commodity

The following are not novel individually:

- LLM or evolutionary generation followed by executable evaluation;
- numerical conjecture testing and counterexample search;
- interval/ball arithmetic with directed error propagation;
- analytic truncation-tail bounds;
- proof-assistant checking and axiom inspection;
- LLM-assisted Lean proof search or cloud autoformalization;
- multi-agent criticism or cold review;
- hashes, manifests, CI logs, and provenance receipts;
- conservative rounding of reported bounds.

All have substantial prior art, often with stronger implementations, publications, benchmarks, or assurance.

### Genuinely valuable, but not yet established as novel research

The most valuable aspect is the **claim-promotion discipline across heterogeneous evidence types**. The repository repeatedly distinguishes statistical evidence, high-precision numerics, finite interval enclosures, heuristic infinite-dimensional extrapolation, Lean-proved propositions, open analytic bridges, and failed theorem gates. It keeps failed runs visible and records review defects instead of silently retuning the claim. That is good research engineering.

The combination of:

1. autonomous breadth-first conjecture scouting,
2. falsification before proof investment,
3. validated numerics with explicit analytic tails,
4. local replay of externally generated Lean proofs,
5. adversarial review of the informal/formal boundary, and
6. receipt-gated public claims

is a coherent and useful operating model. Similar components and partial loops exist elsewhere, so novelty should be claimed only after a systematic literature search for **workflow composition** and after the local implementation is consolidated and evaluated. At present, the defensible phrase is “an evidence-conscious integration of established methods,” not “a new verification paradigm.”

### What prevents a stronger claim

- There is no single runnable end-to-end pipeline in the named `engine/` tree.
- The flagship theorem certificate fails its stated closed-contour gate.
- The local audit explicitly identifies heuristic infinite-dimensional control.
- Numerical certificates are not checked by a proof-assistant-verified certificate checker.
- Formalized lemmas do not yet cover the whole analytic theorem chain.
- External Aristotle proof search is closed and service-dependent.
- There is no benchmark comparing the workflow against human-only, LLM-only, or proof-only baselines.
- There is no independently accepted theorem demonstrated as having traversed the complete chain.

### Bottom line

**Verdict: mostly commodity components, assembled with above-average epistemic hygiene; potentially valuable as a reproducible research-operations system, but not yet a completed or demonstrably novel AI-verified mathematics pipeline.**

The nearest-term publishable contribution is probably not “AI proves deep mathematics.” It is a methods and tooling paper that precisely specifies claim tiers, certificate schemas, failure gates, local replay, and adversarial-review protocol, then prospectively evaluates the system on a corpus of conjectures. A stronger mathematical contribution requires one nontrivial result to pass the entire chain: source-bound scout record, decisive falsification controls, rigorous Arb certificate with a proved infinite tail, proof-assistant linkage to the exact target theorem, clean local replay, and independent expert review.

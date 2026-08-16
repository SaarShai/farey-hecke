# Public Repository Design for an AI-Verified-Mathematics Pipeline

**Research date:** 2026-08-16  
**Interpretation:** “Exists” means publicly downloadable and usable tooling, not a paper, private service, demo, or general framework from which the feature could be built. Absence findings are bounded to the tools and primary sources inspected; they are not claims that no obscure project exists. GitHub counts are volatile snapshots observed on the research date.

This report builds on [`PRIOR_ART_AI_MATH_PIPELINE.md`](./PRIOR_ART_AI_MATH_PIPELINE.md). It does not repeat that survey's comparisons with AlphaProof, AlphaEvolve, FunSearch, Flyspeck, Arb, INTLAB, Lean/mathlib, or Aristotle except where needed to answer the narrower product-design questions.

## 1. Gaps: what is not available as downloadable tooling?

### What the inspected tools actually cover

| Area | Downloadable capability verified | Missing layer relevant to this repository |
|---|---|---|
| Lean proof agents | LeanDojo extracts proof states, tactics, and premises and supports programmatic Lean interaction; its original repository is deprecated for new projects in favor of LeanDojo v2, while the original snapshot showed about 801 stars and 118 forks. [LeanDojo repository](https://github.com/lean-dojo/LeanDojo) | No cross-stage ledger promoting a claim from exploratory evidence through counterexample search, validated numerics, formal proof, and independent review was found in LeanDojo's documented scope. |
| Symbolic discovery | PySR is an installable symbolic-regression system available through pip, conda, Docker, and Apptainer; its repository showed about 3.6k stars. [PySR repository](https://github.com/MilesCranmer/PySR) | PySR optimizes candidate expressions against data; it does not claim to certify theorem truth or manage proof-tier promotion. A maintainer also states that checkpoints cannot be loaded across PySR versions, illustrating why external receipts must bind versions. [PySR issue #941](https://github.com/MilesCranmer/PySR/issues/941) |
| General computational mathematics | SageMath is a large downloadable open-source mathematics system with source, package-manager, container, and cloud installation paths; its repository showed about 2.4k stars and more than 5,000 issues in the inspected snapshot. [Sage repository](https://github.com/sagemath/sage) | The first-party material inspected does not specify a claim-level promotion state machine, hashed research receipt, retained-negative-results ledger, or bridge from notebook output to a statement-audited formal theorem. |
| Generic agent execution | AutoGen provides local and Docker command-line executors and shows agents running generated code, including a conversational math example. [AutoGen command-line executors](https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/components/command-line-code-executors.html), [AutoGen 0.2 math example](https://microsoft.github.io/autogen/0.2/docs/tutorial/code-executors/) | No authoritative AutoGen or LangChain distribution was located that implements mathematical evidence tiers, interval-certificate semantics, exact-statement auditing, or claim promotion. **UNVERIFIED:** an exhaustive absence across all community examples was not established. |
| Formal CI | `leanprover/lean-action` builds, tests, lints, caches Lake projects, can run the independent `nanoda` checker, and can reject `sorryAx`. [lean-action](https://github.com/leanprover/lean-action) The LeanProject template supplies build, blueprint-deployment, release, and dependency-update workflows. [LeanProject](https://github.com/leanprover-community/LeanProject) | These are proof-project CI components, not a multi-evidence research assurance case. They do not natively bind numerical inputs, negative controls, rounded-down margins, reviewer independence, and exact claim hashes into one receipt graph. |
| Open-science compendia | The o2r Executable Research Compendium has a public technical specification for packaging executable research. [ERC specification](https://o2r.info/erc-spec/) Papers with Code's code-completeness guidance asks for dependencies, training and evaluation code, models, and precise reproduction commands. [Papers with Code recommendations](https://github.com/paperswithcode/releasing-research-code) The AAAI checklist explicitly asks whether code used to eliminate or disprove claims is included. [AAAI reproducibility checklist](https://aaai-23.aaai.org/reproducibility-checklist/) | These standards package or assess reproducibility at paper/repository level; the inspected specifications do not define a mathematics-specific claim DAG whose nodes carry epistemic tiers, proof/certificate semantics, conservative margins, failed gates, and adversarial-review lineage. |
| REES | Interpreting REES as repo2docker's **Reproducible Execution Environment Specification**, it recognizes ordinary environment files such as `requirements.txt`, `Project.toml`, and `apt.txt` so software can construct a reproducible environment; its stated goal is environment reproduction from community-standard files. [repo2docker REES](https://repo2docker.readthedocs.io/en/2024.07.0/specification.html) | REES specifies how to reconstruct an execution environment, not how to represent or promote mathematical claims. If “REES” instead meant the Registry of Efficacy and Effectiveness Studies, that registry records causal-study designs and pre-analysis plans in education and is still further from a mathematics certificate ledger. [ICPSR REES](https://www.icpsr.umich.edu/sites/rees/about-rees) |
| AlphaProof-adjacent open source | DeepMind publicly describes AlphaProof's Lean-centered reinforcement-learning approach and manual formalization of the IMO problems. [DeepMind AlphaProof account](https://deepmind.google/blog/ai-solves-imo-problems-at-silver-medal-level/) Public adjacent components include LeanDojo, Lean/mathlib, comparator-style anti-cheating, and theorem datasets, but each addresses a narrower role. | No downloadable AlphaProof runner, weights, and training stack were located in the official public materials inspected. **UNVERIFIED:** this is a bounded public-release finding, not proof that no later or unofficial implementation exists. |

The open-science neighborhood is important but not a substitute. Generic executable-compendium and research-object standards answer “what files and environment reproduce this result?”; this project must additionally answer “what exact claim is supported, at which tier, by which evidence chain, with what remaining gaps, and what failed?” The World Bank's reproducibility-package checklist, for example, requires code, ordered execution, provenance, and in some cases SHA-256-bound precomputed outputs, but it is not a mathematical proof-status system. [World Bank reproducibility package checklist](https://worldbank.github.io/wb-reproducible-research-repository/reproducibility_package_checklist.html)

### The three largest genuinely unfilled niches

#### **PRIMARY GAP 1 — A claim ledger with mechanically enforced evidence promotion**

Build a versioned claim graph in which every node names the exact proposition, tier, assumptions, parent evidence, artifacts, hashes, margins, limitations, and verdict. Promotion should be executable: statistical → numerical → certified → machine-proved should require distinct validators, and no stage should silently inherit the authority of another. Failed gates and counterexamples must remain addressable artifacts rather than disappearing from the current “best” run.

This is the strongest niche because the inspected formal tools begin at the encoded theorem, numerical tools end at a computation, and open-science tooling packages whole studies. None of the inspected downloadable projects joins those trust boundaries with mathematics-specific promotion rules. The baseline survey already established that the individual ingredients are commodity; the ledger is the defensible integration contribution.

#### **GAP 2 — A hardened replay and CI gate for untrusted AI mathematics**

The runner should sandbox generated Lean and scripts; pin toolchains and dependencies; reject `sorry`, `admit`, disallowed axioms, and undeclared network access; hash the informal and formal statements; replay numerical negative controls; verify certificate bundles; and emit a machine-readable result. This need is concrete: a MathOverflow discussion on trusting AI-generated Lean proofs highlights semantic mistranslation and the fact that Lean code can execute commands, while a Formal Conjectures maintainer says its current CI largely runs `lake build` and anti-cheating checks remain an active concern. [MathOverflow: “Should we trust AI-generated formal proofs in Lean 4?”](https://mathoverflow.net/questions/513540/should-we-trust-ai-generated-formal-proofs-in-lean-4/513602) `lean-action` supplies valuable build and independent-checker primitives, but not the broader evidence and threat model. [lean-action](https://github.com/leanprover/lean-action)

#### **GAP 3 — A common discovery-to-proof adapter protocol**

The opportunity is not another CAS, optimizer, LLM agent framework, interval library, or prover. It is a narrow protocol that lets these tools exchange claims and evidence without erasing their distinct semantics. PySR candidates, Sage/SciPy/Hypothesis counterexamples, Arb enclosures, Lean projects, and human/LLM reviews should all produce role-specific artifacts plus a common receipt envelope. PySR's version-bound checkpoint behavior is a useful warning: portability requires declarative artifacts and exact tool metadata, not opaque in-memory objects. [PySR issue #941](https://github.com/MilesCranmer/PySR/issues/941)

### Ranked recommendation

1. **PRIMARY — Implement the claim ledger and promotion validator first.** It is the clearest unmet layer and can create value before sophisticated orchestration exists.
2. **Second — Add the sandboxed replay/CI gate.** This turns the ledger from documentation into enforceable assurance.
3. **Third — Add adapters incrementally around one worked example.** Avoid claiming universal interoperability until each adapter's success semantics and negative controls are demonstrated.

## 2. Demand signals: what mathematicians download, discuss, and need

### Observed adoption and activity

Download/use demand clusters around tools that solve a bounded job with a familiar installation path. On 2026-08-16, PySR showed about 3.6k GitHub stars and offered pip, conda, Docker, and Apptainer installation; LeanDojo showed about 801 stars and a pip installation path; mathlib4 showed about 3.4k stars and documented `lake exe cache get`, `lake build`, and `lake test`; Sage showed about 2.4k stars and multiple installation modes. [PySR](https://github.com/MilesCranmer/PySR), [LeanDojo](https://github.com/lean-dojo/LeanDojo), [mathlib4](https://github.com/leanprover-community/mathlib4), [Sage](https://github.com/sagemath/sage) Stars are attention signals, not proof of active users; GitHub does not expose a reliable “researchers who used this successfully” count on these pages.

The issue record shows that operational friction matters. A PySR issue documents inability to load checkpoints across versions, and a Sage discussion calls dependency installation and version conflicts a barrier to getting started. [PySR issue #941](https://github.com/MilesCranmer/PySR/issues/941), [Sage discussion #39272](https://github.com/sagemath/sage/discussions/39272) This favors a pinned, replayable worked example over an architecture diagram.

### Workflow pain from the Lean community

Lean practitioners describe statement quality, maintainability, and human comprehension as distinct from merely producing compiling code. A Zulip discussion about accelerating the Fermat's Last Theorem effort considers routine prerequisite formalization a plausible AI use while warning about reviewing large, inscrutable generated developments. [Lean Zulip archive: accelerating FLT](https://leanprover-community.github.io/archive/stream/416277-FLT/topic/accelerating.20FLT.20%28with.20tactics.20or.20AI%29.html) A Brownian-motion project discussion reports substantial blueprint effort, reinforcing that organizing and auditing the intended mathematics remains real work even when formal proof labor is accelerated. [Lean Zulip archive: Brownian motion project](https://leanprover-community.github.io/archive/stream/509433-Brownian-motion/topic/Second.20phase.20of.20the.20project.html)

The MathOverflow trust thread had thousands of views and substantial voting in the inspected snapshot, but its more important demand signal is qualitative: contributors distinguish kernel checking from faithful statement translation, definitions, imported assumptions, and safe execution. [MathOverflow thread](https://mathoverflow.net/questions/513540/should-we-trust-ai-generated-formal-proofs-in-lean-4/513602) **UNVERIFIED:** the exact view and vote totals are volatile and should not be used in permanent marketing copy.

### Venue demand

The 2026 AI4Math workshop at ICML says it received 346 submissions, twice the prior year's volume, and its call explicitly includes formal theorem proving, precise autoformalization, verification and evaluation, human–AI collaboration, and scientific agents. [AI4Math 2026](https://ai4math2026.github.io/) AITP 2026 lists AI/big-data methods in theorem proving, collaboration between automated and interactive proving, formal/informal library alignment, and large-scale mathematical understanding among its topics. [AITP 2026](https://aitp-conference.org/2026/) CICM's 2026 AI4Math workshop explicitly solicits integrations spanning proof assistants, theorem provers, mathematical databases, AI tools, conjecture generation, and mathematical software. [CICM AI4Math 2026](https://cicm-conference.org/2026/cicm.php?event=ai4math&menu=general)

These calls establish a live research audience for integration and verification. They do not establish demand for this exact implementation; that must be earned through a runnable artifact and external users.

### What will make the repository used rather than merely starred

#### **PRIMARY — A 10-minute, offline-capable worked example that ends in an inspectable verdict**

The first-run path should install with one command, run without paid APIs, deliberately include one false candidate, shrink or exhibit its counterexample, certify one bounded numerical statement, build one exact Lean theorem, and open a human-readable receipt graph. This recommendation follows the observed preference for pip/Lake-style bounded entry points and the documented installation/version pain above. [PySR](https://github.com/MilesCranmer/PySR), [mathlib4](https://github.com/leanprover-community/mathlib4), [Sage dependency discussion](https://github.com/sagemath/sage/discussions/39272)

Ranked adoption requirements:

1. **PRIMARY: immediate local payoff.** `pipx install … && … demo` should yield a verdict, artifacts, hashes, and a readable explanation without credentials.
2. **A credible trust boundary.** Document exactly what each green check proves and does not prove; expose informal↔formal statement comparison, axioms, toolchain pins, and certificate assumptions. The trust discussion shows that a compiling Lean file alone is not enough. [MathOverflow thread](https://mathoverflow.net/questions/513540/should-we-trust-ai-generated-formal-proofs-in-lean-4/513602)
3. **Bring-your-own-tool adapters.** Researchers should be able to use plain scripts, Sage, local models, hosted LLMs, Arb, or Lean without adopting a monolithic agent stack.
4. **Negative results as useful output.** A failed conjecture should produce a small, citable bundle, not an error log. AAAI's checklist explicitly asks whether code used to eliminate or disprove claims is included, providing a strong publication-facing precedent. [AAAI reproducibility checklist](https://aaai-23.aaai.org/reproducibility-checklist/)
5. **Copyable CI and archival releases.** A green badge should link to the receipt and exact artifacts; releases should be hash-bound and suitable for DOI archiving. JOSS expects installable, documented, tested research software and permanent archival releases. [JOSS submission requirements](https://joss.readthedocs.io/en/latest/submitting.html)
6. **Meaningful examples, not benchmark theater.** Include one small example and one real research case with an honest unresolved or negative outcome. The venue calls emphasize scientific usefulness and integration beyond competition problems. [AI4Math 2026](https://ai4math2026.github.io/), [AITP 2026](https://aitp-conference.org/2026/)

## 3. Form: the packaging pattern most likely to gain uptake

### Decision

#### **PRIMARY RECOMMENDATION — An installable Python CLI/package inside an opinionated template repository, with GitHub Actions enforcing a normative receipt specification**

The primary product should be the small Python package and CLI. The public repository should simultaneously be usable as a template and should contain the normative schemas, CI workflows, and worked example. These are layers of one distribution, not four competing products.

The CLI is primary because the orchestrator and validators need versioned executable behavior, adapter discovery, testability, and ordinary dependency management. PyPA documents `pyproject.toml`-based building and publishing as the standard Python packaging route. [PyPA packaging guide](https://packaging.python.org/en/latest/guides/section-build-and-publish/) A pure template would strand bug fixes in copied repositories; a pure specification would leave users to implement the hard parts; Actions-only gates would couple the product to GitHub and make local replay secondary.

### Ranked forms

1. **PRIMARY: pip-installable package + CLI.** Own the schemas, validation, promotion logic, replay, bundle verification, and adapter protocol. Initial stable commands should be `init`, `validate`, `replay`, `promote`, and `verify-bundle`; sophisticated autonomous orchestration can remain experimental.
2. **Bundled template repository.** Include `claims/`, `runs/`, `artifacts/`, `schemas/`, adapters, pinned environments, the worked example, and workflows. Cookiecutter defines templates as repositories for generating projects, and Cookiecutter Data Science demonstrates the uptake of an opinionated but flexible research structure; its repository showed about 9.9k stars in the inspected snapshot. [Cookiecutter](https://www.cookiecutter.io/), [Cookiecutter Data Science](https://github.com/drivendataorg/cookiecutter-data-science)
3. **Mandatory GitHub Actions gates.** Use required checks for schema validation, replay, Lean build, axiom/`sorry` policy, certificate verification, negative controls, and reviewer independence. GitHub protected branches can require successful status checks and review conditions; artifact attestations bind build artifacts to provenance and digests. [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches), [GitHub artifact attestations](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations) The same checks must remain runnable locally.
4. **Normative documentation/specification.** Publish the evidence-tier definitions, state machine, schemas, trust model, threat model, and conformance tests in the repository. Semantic Versioning shows that a concise normative specification can itself become a widely referenced public artifact; its repository showed about 7.8k stars. [Semantic Versioning repository](https://github.com/semver/semver) Here, however, the standard should accompany working software rather than replace it.
5. **JOSS paper after demonstrated public use.** JOSS requires open-source, installable, documented, tested, maintainable research software and now expects more than six months of public development history and evidence of research use. [JOSS submission requirements](https://joss.readthedocs.io/en/latest/submitting.html) That makes JOSS an excellent later credibility and citation mechanism, not the launch form.

Use pre-commit only as a fast local mirror for deterministic hygiene checks. The project describes itself as a framework for managing multi-language pre-commit hooks, and its repository showed about 15.3k stars; it is not a theorem or certificate trust anchor. [pre-commit repository](https://github.com/pre-commit/pre-commit)

### Minimum launch artifact

The first release should contain one schema version, one CLI, one offline adapter per non-LLM role, optional LLM adapters, one GitHub workflow, one deliberately failing example, one passing end-to-end example, and a static HTML/Markdown receipt report. Do not lead with a plugin marketplace. The core value must work with subprocess adapters before in-process convenience layers or hosted-service integrations are expanded.

## 4. Interfaces: initial adapter targets and contract shape

### Contract decision

#### **PRIMARY RECOMMENDATION — JSON Schema is authoritative; a subprocess CLI is the stable execution boundary; thin Python ABCs are optional ergonomics**

Use JSON Schema Draft 2020-12 for versioned request, artifact, and receipt documents. JSON Schema is a declarative language for validating JSON structure, constraints, and types. [JSON Schema specification](https://json-schema.org/specification) Schema validation must not masquerade as semantic verification: executable validators must still check that hashes match bytes, an interval excludes the forbidden set, a Lean declaration is the exact intended statement, and parent receipts authorize a promotion.

Every adapter should accept a JSON job manifest on stdin or by path, write newline-delimited progress events to stderr or a declared stream, and emit one final JSON result/receipt. This subprocess boundary works for Python, Julia, C/C++, Lean/Lake, containers, and hosted APIs. A small Python ABC may expose `run(request, workspace) -> result` for in-process plugins; Python's standard `abc` module supplies nominal abstract interfaces. [Python `abc`](https://docs.python.org/3/library/abc.html) Tool-specific options belong in namespaced configuration, not in the common base class.

Each adapter manifest should declare `adapter_id`, `adapter_version`, `role`, `capabilities`, input/output schema IDs, determinism, network requirement, sandbox needs, and claimed trust tier. Each receipt should bind the exact claim ID and statement hash, parent receipts, tool/version, command/configuration, input/output hashes, environment/toolchain, timestamps, exit status, role-specific verdict, log references, assumptions, and limitations.

### Initial adapter targets, ranked by role

#### Scout

1. **PRIMARY: OpenAI Responses-compatible scout**, with the same envelope usable by local Ollama. OpenAI supports tool calling and schema-constrained structured outputs; Ollama documents both structured outputs and partial OpenAI Responses compatibility, enabling a hosted/local pair behind one adapter family. [OpenAI Structured Outputs](https://openai.com/index/introducing-structured-outputs-in-the-api/), [Ollama structured outputs](https://docs.ollama.com/capabilities/structured-outputs), [Ollama OpenAI compatibility](https://docs.ollama.com/api/openai-compatibility)
2. **Anthropic Messages API.** Its tool definitions use JSON Schema inputs, making it suitable for emitting candidate records through the same canonical schema. [Anthropic Messages API](https://platform.claude.com/docs/en/api/beta/messages/create)
3. **Optuna ask/tell or PySR candidate import.** Optuna exposes studies, trials, samplers, pruners, and an ask/tell interface; PySR emits interpretable candidate expressions. They cover non-chat search and equation discovery while the pipeline owns evaluation and promotion. [Optuna Study API](https://optuna.readthedocs.io/en/stable/reference/study.html), [Optuna ask/tell](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/009_ask_and_tell.html), [PySR](https://github.com/MilesCranmer/PySR)

#### Falsifier

1. **PRIMARY: Hypothesis.** It generates test cases, retains examples in a database, targets interesting behavior, and shrinks failures, which maps naturally to minimal counterexample receipts. [Hypothesis API](https://hypothesis.readthedocs.io/en/latest/reference/api.html)
2. **SciPy global optimization.** `differential_evolution` and SHGO support bounded global search; their results remain heuristic counterexample searches unless independently certified. [SciPy optimization tutorial](https://docs.scipy.org/doc/scipy/tutorial/optimize.html)
3. **Z3Py.** Z3's official Python API supports SMT solving and is appropriate for exact discrete/logical countermodels or UNSAT results relative to the encoded theory. [Z3Py introduction](https://microsoft.github.io/z3guide/programming/Z3%20Python%20-%20Readonly/Introduction/)

#### Certifier

1. **PRIMARY: python-flint/Arb.** Python-FLINT wraps FLINT and Arb and provides real and complex ball arithmetic with rigorous error tracking; its `arb` type represents midpoint-radius enclosures. [python-flint](https://github.com/flintlib/python-flint), [python-flint `arb`](https://python-flint.readthedocs.io/en/stable/arb.html) A successful adapter certifies only the implemented finite expression plus explicitly supplied analytic assumptions and tails.
2. **CoqInterval.** It supplies proof-producing/reflected interval tactics whose results are checked in the proof assistant. [CoqInterval](https://coqinterval.gitlabpages.inria.fr/)
3. **Gappa.** It proves floating- and fixed-point bounds and supports proof-producing backends, making it a useful certificate-export/check boundary. [Gappa invocation and backends](https://gappa.gitlabpages.inria.fr/gappa/invoking.html)

INTLAB should be a later adapter, not a launch dependency: it is a mature MATLAB/Octave interval and verified-numerics environment, but its distribution and runtime assumptions are less suitable for the default free Python/CI path. [INTLAB official site](https://www.tuhh.de/ti3/intlab/)

#### Prover

1. **PRIMARY: plain Lean 4 + Lake/mathlib build.** This is the smallest durable trust endpoint: a pinned project, local build, exact declaration extraction, axiom report, and `sorry` policy. Mathlib documents `lake exe cache get`, `lake build`, and `lake test`; `lean-action` supplies standard CI and optional independent `nanoda` checking. [mathlib4](https://github.com/leanprover-community/mathlib4), [lean-action](https://github.com/leanprover/lean-action)
2. **LeanDojo v2.** Target v2 for programmatic proof-state and tactic interaction; the original repository explicitly directs new projects to v2. [LeanDojo](https://github.com/lean-dojo/LeanDojo)
3. **Harmonic Aristotle.** Support the hosted service, but accept only a downloaded project that passes the local pinned build, statement, axiom, and placeholder audit; service status alone is not a proof receipt. [Aristotle](https://aristotle.harmonic.fun/)

#### Reviewer

1. **PRIMARY: independent human GitHub pull-request review.** Protected branches can require approvals, resolved conversations, and named checks, providing a concrete governance gate. [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
2. **A second-provider LLM reviewer through the same OpenAI/Anthropic/Ollama structured-output envelope.** A reviewer must be independent of the generating run and must return cited objections, tested claims, and a closed verdict vocabulary; structured-output support makes the record machine-validated but does not make the mathematical judgment trustworthy. [OpenAI Structured Outputs](https://openai.com/index/introducing-structured-outputs-in-the-api/), [Anthropic Messages API](https://platform.claude.com/docs/en/api/beta/messages/create), [Ollama structured outputs](https://docs.ollama.com/capabilities/structured-outputs)
3. **JOSS-style checklist review.** JOSS publicly reviews both software and its short paper and evaluates installation, documentation, tests, CI, licensing, and research utility; adapt that checklist for release readiness while keeping mathematical correctness as a separate domain-review gate. [JOSS about](https://joss.theoj.org/about), [JOSS submission requirements](https://joss.readthedocs.io/en/latest/submitting.html)

### Non-negotiable semantic boundary

Every adapter must state what success means. A scout success means “candidate emitted”; Hypothesis or Z3 success means “counterexample/model relative to this generator or encoding”; Arb success means “this enclosure contains the implemented value under these assumptions”; Lean success means “the kernel accepted this exact proposition under this axiom footprint”; reviewer approval means “this reviewer found no blocking defect under this rubric.” No adapter may promote its own result into another role's evidence tier.

## 5. Name and positioning

GitHub repositories are addressed under an owning user or organization, so the practical availability test is the intended `<owner>/<slug>`, not a globally reserved bare name. [GitHub repository documentation](https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repositories) The checks below mean that an exact-name GitHub repository search returned no indexed match on 2026-08-16; private repositories, indexing lag, trademarks, domains, and package registries remain outside that result. Recheck the intended owner URL immediately before creation.

### Ranked candidates

1. **PRIMARY — LemmaLedger** (`lemma-ledger`)  
   *Positioning:* **The receipt-first, agent-agnostic evidence ledger for AI-assisted mathematics.**  
   It names the most defensible novelty—claim lineage and durable evidence—without promising autonomous theorem proving. [GitHub exact-name search](https://github.com/search?q=%22LemmaLedger%22&type=repositories) returned no indexed exact repository in the bounded check.

2. **ProofBraid** (`proof-braid`)  
   *Positioning:* **Braid agents, checkers, evidence tiers, and negative results into reproducible mathematical investigations.**  
   This is the most distinctive orchestration metaphor and is a strong fallback if the project wants a broader brand than “ledger.” [GitHub exact-name search](https://github.com/search?q=%22ProofBraid%22&type=repositories) returned no indexed exact repository in the bounded check.

3. **VerdictMath** (`verdict-math`)  
   *Positioning:* **Agent-agnostic mathematical investigations that end in supported, refuted, inconclusive, or machine-proved—not vibes.**  
   The name foregrounds honest terminal states and negative-result retention. [GitHub exact-name search](https://github.com/search?q=%22VerdictMath%22&type=repositories) returned no indexed exact repository in the bounded check.

4. **MathReceipt** (`math-receipt`)  
   *Positioning:* **Run the math, keep the receipt: tiered evidence and reproducible checks across interchangeable tools.**  
   This is the clearest literal promise, though “receipt” can sound financial. [GitHub exact-name search](https://github.com/search?q=%22MathReceipt%22&type=repositories) returned no indexed exact repository in the bounded check.

5. **ProofHarbor** (`proof-harbor`)  
   *Positioning:* **A safe harbor for verified claims, failed conjectures, receipts, and reproducible agent runs.**  
   It is friendly and preservation-oriented, though less explicit about orchestration. [GitHub exact-name search](https://github.com/search?q=%22ProofHarbor%22&type=repositories) returned no indexed exact repository in the bounded check.

### Final naming recommendation

Choose **LemmaLedger** and use the descriptor **“A receipt-first, agent-agnostic pipeline for AI-assisted mathematics.”** The name is sober, legible to mathematicians, and aligned with the strongest unfilled niche rather than with the commodity components. Choose **ProofBraid** only if brand distinctiveness and the multi-adapter story matter more than immediate semantic clarity.

Before launch, check the exact owner URL; GitHub repository search; PyPI, npm, crates.io, and relevant package registries; domain and social handles; and appropriate trademark databases or counsel. The search is plausibility screening, not legal clearance.

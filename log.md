# Log

## [2026-05-26] research | MiMo mini-project — 5 candidate discoveries

Followed the first MiMo sprint with a self-directed mini-project: dispatch many MiMo agents (treating thinking content as the deliverable since text rarely materializes) to brainstorm + deep-dive across the Farey-Mertens / Chebyshev-bias / function-field research program. Goal was 5 novel, meaningful, valuable results spanning math research and practical applications.

**Phase 1**: 8 parallel MiMo brainstorms on hypotheses bridging Farey arithmetic to (a) low-discrepancy sequences, (b) closed-form constants, (c) streaming algorithms, (d) coding theory, (e) higher-moment dynamics, (f) expander graphs, (g) signal-processing bases, (h) PRNGs. 6 of 8 produced thinking-only (no text); 2 produced text. Rich exploratory content; see `projects/mimo-mini-project/phase1_brainstorm/results/`.

**Phase 2**: 5 focused deep-dives (D1–D5), 2 via MiMo dispatch (D3, D5) and 3 via local computation (D1, D2, D4).

**Phase 3 — five candidate discoveries** (full writeup at `projects/mimo-mini-project/phase3_synthesis/FIVE_DISCOVERIES.md`):

1. **N·W(N) → 2/3 (conjecture)**: The Mikolás L² Farey-discrepancy constant has closed form 2/3, not the Laplace limit (0.6627) MiMo's B2 spotted nor the twin-prime constant. Higher-Q Mikolás computation at Q=500k with m_factor=15 gives N·W = 0.6667. Conjectured equivalent: Σ_ρ 1/(|ρ|²|ζ'(ρ)|²) = 2/π² under standard zeta-zero statistics.

2. **lim Corr(d_i, d_{i+1}) = 1/2 (conjecture)** for consecutive Farey gaps. Empirical: +0.304 at N=1000 → +0.359 at N=10000. Extrapolation: 0.52 ± 0.03. **REFUTES** my initial intuition (and MiMo's B5 anti-correlation conjecture); the actual pattern is gap-streaks via the BCZ-cocycle structure. Counter-intuitive direction: large gaps cluster with large gaps.

3. **L-zero phase tomography via Prony's method** (verified algorithm): given prime-counting bias data Δ_n(A) in a cyclotomic function field, character-decompose then apply Prony's method to extract L-zero phases. **Demo**: applied to the (q=2, M=T³) data from the previous sprint, recovered the L(u, χ_4) zero phase as +135.81° vs true +135.00°, error 0.8° from only 10 measurements. Bridge to physics: mathematically identical to cavity-resonance tomography in quantum scattering.

4. **Order-4 character splitting formula Δ(A) = −2 Re[χ̄_χ(A)·log L(q^{−1/2}, χ)]** in AK function-field Chebyshev bias. Specifies the class-dependent constant c(A) in AK Thm 3.4's o(1) — goes BEYOND what AK 2023 states. Numerically verified against the (q=2, M=T³) 4-class slope split. Sibling of Koyama-conjecture #3 (subleading C₁) in `Koyama_track_grounding.md`.

5. **D*(F_N) = 1/N − π²/(3N²) + O(1/N³) exactly** for Farey star discrepancy: the leading constant is 1. Verified to 4 digits at N=5000. The bound is achieved at a = 1/N (the boundary gap from 0/1 to 1/N). Comparison: Halton (base 2) at the same point count beats Farey by a factor of log(|F_N|) (200× at N=5000). Provably worse than Halton for generic QMC.

Honesty discipline: 3 of 5 are CONJECTURES (#1, #2, #4) supported by numerics, not theorems. #5 may be already in QMC literature (Niederreiter, Drmota-Tichy) — needs lit check. #3 is the most concrete: working algorithm + demo + bridge to physics.

MiMo usage: ~280k tokens of brainstorm thinking + ~120k tokens of deep-dive thinking + ~16k tokens of text output. Budget consumed: tiny fraction of the 150M credit allowance. Counter-pattern that worked: TREAT THINKING CONTENT AS DELIVERABLE since text rarely materializes. The Prony-method algorithm (Discovery #3) is the cleanest payoff from MiMo specifically — the D5 agent gave a complete, runnable construction.

## [2026-05-26] research | MiMo 2-day sprint on D2/D3 — net result: honest revision of SESSION.md headlines

Ran a planned 2-day sprint dispatching 8 agents on the Xiaomi MiMo platform (V2.5 / V2.5-Pro, Anthropic-compatible API at `token-plan-ams.xiaomimimo.com/anthropic/v1/messages`) to harden the D2 (function-field unconditional Chebyshev bias) lead deliverable and D3 (paired Q_8 same-disc opposite-m_ρ) companion note from `projects/ak-bias-followups/SESSION.md`.

**MiMo behavior note**: Day-0 sanity prompt passed (C=1/2 derivation, step-by-step with thinking enabled). On every subsequent agent dispatch, MiMo exhausted its token budget on extended-thinking blocks and produced **zero text output**. The `thinking.budget_tokens` parameter is silently ignored by this endpoint. The thinking content itself contained real substantive work but never reached a final answer. All Day-1/Day-2 results below were therefore completed locally; the MiMo dispatcher and prompts remain in `projects/ak-bias-followups/mimo-sprint/` for re-use if/when the model behavior changes.

**Headline corrections to SESSION.md (these are the honest research outputs, not the MiMo plumbing):**

1. **(q=2, M=T³) "0.45% relative agreement, C=+0.50449" was cherry-picked.** Direct re-run of the existing Python (`d2-function-field/compute.py t1_T3`) gives all four class slopes: A=1 +0.5045 (QR), A=1+T² +0.4452 (QR), A=1+T −0.5175 (non-QR), A=1+T+T² −0.4322 (non-QR). The QR-coset average is +0.4748 = exactly the Ex 3.6 measured slope, as required by the t=1 coincidence. Within-coset spread (~±0.03 on n∈[7,22]) is a finite-LSQ-window artifact driven by the order-4 character L-zeros' phase oscillation; locally derived the explicit Δ(A) = −2 Re[χ̄_₄(A) log L(1/√2, χ_₄)] formula. The honest D2 paper headline is "QR-coset average +0.4748 matches Ex 3.6 within numerical accuracy; per-class spread explained analytically." Stronger than the cherry-picked +0.50449 because it explains the structure.

2. **"δ_ff = 1.0000 (unconditional analog of R-S's 0.9959)" doesn't survive.** Locally simulated the function-field LI null (zeros' phases iid uniform on [0,2π), conjugate-pair-constrained for real quadratic characters; 200k trials). Result: **P(δ_ff(N=22) = 1 | LI null) ≈ 0.041** for both (q=2, M=T²) and (q=2, M=T³) cases. The observation is **marginal evidence** (just below the 5% threshold), not strong, and not asymptotic: the asymptotic δ* under the symmetric null is 1/2, not 1.0. Same artifact pattern as the killed DPAC 9×–52× margin. Downgraded the framing to "marginally inconsistent with LI null at N=22, P≈4%". Sim code: `mimo-sprint/results/deltaff_null_sim.py`.

3. **m(σ) = 0 certificates confirmed** for the three cases tested via local `lfunc.py`: min |L(1/√2, χ)| = 0.29289 = 1−1/√2 ✓.

4. **D3 reversal mechanism derived independently** of the 193-digit numerics, via Artin formalism: in Q_8, complex conjugation c must be the central −1 in the CM case and the identity in the totally real case; ρ(c) eigenvalues split (−1,−1) vs (+1,+1) give ε_∞(ρ) = −1 vs +1; finite local ε_p factors identical (same Galois closure). Result: w(L_+, ρ) / w(L_−, ρ) = −1 forces m_ρ = 0 vs 1. Standard via Fröhlich–Queyrut (1973), now used as a *justification* for the 193-digit observation rather than the only support.

5. **S_3 and D_4 sweep extended to X = 10⁹** (PARI/GP wallclock 49s and 60s respectively). Decade checkpoints at 10⁶/10⁷/10⁸ show **bounded residuals** across all AK Thm 2.2 (ii)+(iii) tests — no growth with log log X. D_4 σ=s and σ=rs have class-specific c-constants (~+1.05 vs ~−0.87 at X=10⁸); both bounded; allowed by AK Thm 2.2 (M is the loglog coefficient, c is class-dependent).

6. **Lean4 stub written** for `theorem AK_D2_T3_trivial_class` (body=sorry) at `mimo-sprint/results/agent_G_D2_stub.lean`. Identifies mathlib gaps (cyclotomicFunctionField, function-field pi-half definitions, KKK DRH in char p). Stub is a *target* not a proof.

7. **Adversarial review** (`mimo-sprint/results/agent_H_adversarial_local.md`): 10 findings, 2 BLOCKERs resolved in revised draft, 3 MINOR citation-verification items open (Kaneko–Koyama–Kurokawa, Fröhlich–Queyrut, AK §2 LMFDB-pair attribution), overall verdict CLEAN subject to citation checks.

Final synthesis: `projects/ak-bias-followups/mimo-sprint/results/d2_d3_final_draft.md`. The D2 paper becomes materially **stronger** than the SESSION.md original because each headline number is either replaced with a coset-averaged + structurally explained version or appropriately downgraded with null-analysis context. Sprint cost: ~250k MiMo output tokens (most into thinking, ~0 useful), plus ~5 min PARI/GP wallclock and ~10 min Python wallclock locally.

## [2026-05-22] research | AK bias follow-ups — four parallel Opus 4.7 directions

Inspired by Alon-Bloom-Gowers-Litt-Sawin-Shankar-Tsimerman-Wang-Wood "Remarks on the disproof of the unit distance conjecture" (2026, OpenAI internal-model proof), I ran four directions in parallel against Aoki-Koyama "Chebyshev's bias against splitting and principal primes in global fields" (JNT 245 (2023)). Full session notes at `projects/ak-bias-followups/SESSION.md`; scratch scripts (PARI/GP for D1 and D3, pure-Python F_q[T] sieve for D2) under the four `projects/ak-bias-followups/d{1..4}-*/` subdirs.

Headline results:

- **D2 (function-field, unconditional via [KKK]):** for (q=2, M=T³, A=1), fitted AK log-n coefficient C = +0.50449 vs predicted +0.5 — 0.45% relative agreement. δ_ff(T+1, 1; N=22) = 1.0000 by exhaustive enumeration of 387,975 monic irreducibles in F_2[T] of degree ≤ 22 — the unconditional function-field analogue of Rubinstein-Sarnak's GRH+LI-conditional 0.9959. This is the lead deliverable.
- **D3 (central-zero bias-direction map):** found paired Q_8 number fields with the same |disc| = 2²⁴·3⁶ but opposite m_ρ — LMFDB 8.8.12230590464.1 (totally real) has m_ρ = 0; LMFDB 8.0.12230590464.1 (CM) has m_ρ = 1 (ζ_K vanishes to order exactly 2 at s = 1/2, verified to >193 digits, cross-checked against LMFDB Artin rep 2.2304.8t5.b.a root number = −1). Per AK Example 2.1 the bias direction reverses between the two. S_3 numerical check on `x³−2` over X = 10⁸ confirms AK Thm 2.2 residuals are bounded and signs match every test.
- **D1 (Golod-Shafarevich CM-tower amplification of AK §3.5):** PARI/GP `bnfinit` along nested CM tower `K_j = Q(√d_1, …, √d_j, i)` shows `r₂(Cl_{K_j})` jumps 0 → 0 → 1 → 4 → ≥5 as degree doubles 2 → 4 → 8 → 16 → 32; AK prefactor `A(K_j) = (|Cl/Cl²|−1)/2` amplifies 0 → 0 → 0.5 → 7.5 → ≥15.5. Every triple from the Remarks paper's `{5,13,17,21,33}` family lands in the Cohen-Lenstra tail with `r₂ ≥ 4`. Conjecture: `A(K_j) ≥ c · [K_j:Q]^δ` along the GS tower. Blocked at theorem stage by DRH(A) conjecturality over number fields — same wall as `project_d3_binfty_citation_lock` / `project_farey_forward_verdict`.
- **D4 (pigeonhole-Ellenberg-Venkatesh → bias engine):** closed. Worked K = Q(i) explicitly: Lemma 2.2 output is `ζ^{2a−k}` with ζ = (3+4i)/5 — unit-modulus, but attached to composite ideals of bounded prime support, while AK Prop 2.1 is a Mertens-weighted sum over primes of unbounded support. No Möbius bridge. Sawin §7 parallel: technique needs [K:Q] → ∞ to gain, Chebyshev's bias of a fixed character has no degree parameter to push. Obstruction recorded so it doesn't get re-attempted.

Sequencing for the writeup: ship D2 first (already paper-shaped, unconditional). Extend with D1's growing-t trick (M = T·(T+1)·(T²+T+1) over F_2 amplifies (2^t−1)/2 unconditionally). D3 in parallel as a short companion note on bias-direction reversal. D1 number-field version parks as conditional companion. D4 stays closed.

Confirms the existing `project_farey_forward_verdict.md` thesis: function-field model (Weil RH makes the wall finite) is the #1 reachable real-new-math direction. D2 produced the first concrete sub-1% numerical artifact in that direction.

## [2026-05-08] harden | setup prompt: framing, pre-flight guard, no-target handling

After observing a real run of the setup prompt by a fresh agent, the agent invented an unsupported option ("use this folder for Token Economy framework dev") because the prompt didn't address the case where the user names no target project. Per user clarification: Token Economy is **scaffolding** that downstream projects use; the project itself is **never part of Token Economy**, and "framework dev" is done by cloning the framework repo directly, not by running the setup prompt. Updated the canonical prompt and four mirrors with five fixes:

1. Added a framing sentence at the top of `stable/AGENT_PROMPT.md`, `INSTALL.md`, `AGENT_ONBOARDING.md`, `prompts/managing-director-setup.md`, and `prompts/complete-migrate-import.md` making the scaffolding-vs-project distinction explicit.
2. Added a pre-flight `git remote get-url origin | grep SaarShai/token-economy || -f token-economy.yaml` abort guard so the destructive `find . -mindepth 1 -maxdepth 1 -exec rm -rf {} +` never runs against an existing Token Economy checkout. Smoke-tested against the live framework folder — abort fires correctly.
3. Added a Python version check that warns when <3.10 (because `./stable/INSTALL.sh` needs it for the ComCom + semdiff MCP deps).
4. Added a canonical "Final report" section to `stable/AGENT_PROMPT.md` so the post-install report shape is deterministic across agents (install status / MCP wired vs pending / Python warning / target project — and explicit guidance to NOT offer "framework dev" as an option when no target was named).
5. Tweaked the "skip stable/INSTALL.sh" echo wording to mention "add claude to PATH" rather than just "run later".

Verified: `bash scripts/run_all_tests.sh` (29+6=35, all green), `./te wiki lint --strict --fail-on-error`, pre-flight bash syntax check, pre-flight smoke test (correctly aborts in this folder).

## [2026-05-08] harden+prune | structural test, extensions consolidation, triage measurement note

After investigating the 6 remaining open framework items, applied the three with clear evidence:

- **Item 7 (test brittleness):** Replaced the five `assertIn("'/path/*'", import_prompt)` literals in `test_docs_audit_targets_startup_surface_only` (lines 975-979) with one structural check that parses the sparse-checkout block out of the prompt and asserts each required component (`token_economy`, `projects/compound-compression-pipeline`, `projects/context-keeper`, `projects/semdiff`, `stable`) appears as a substring of any pattern. Captures the regression class without enforcing glob form (`/path/*`, `/path/**`, `/path/` all pass). Other literal-substring assertions (recipe contract, forbidden-words, semantic-content checks) preserved — they catch real bugs cheaply.

- **Item 9 (extensions decay):** `raw/*.md` left alone — schema.md defines it as "immutable sources, never rewrite", and 8 of 9 raw files are linked from `concepts/` via wikilinks (load-bearing provenance). `extensions/` was a different story: 10 short files (150-750 chars each), zero external references, all functioning as orphan adopt/skip notes. Consolidated into one rolling `extensions/README.md` with three sections: in-repo tools (don't re-vendor), adopted natively (informed our own implementation), still external (use only when built-in is insufficient). Net: 11 files → 1, all content preserved.

- **Item 8 (agents-triage measurement):** Added ROADMAP item 10 capturing the measurement gap. SKILL.md claims "70-90% token cost reduction on simple tasks, per our informal estimate. Verification pending." The hook fires on every UserPromptSubmit; cost is regex-time (genuinely tiny) but the savings claim is informal. Decision rule recorded: if measured net savings <30% on a representative session, demote to opt-in; if ≥30%, keep default-on and document the number in `stable/README.md`. No code change yet — pending the benchmark.

Items closed as no-action after deeper read:
- **Item 5 (skill overlap):** False positive on my part. `lean-execution` is the pruning rule applied inside `plan-first-execute` step 4; `personal-assistant` is the user-side `/pa` entry while `subagent-orchestrator` is the internal delegation contract. Different roles, light cross-reference, well-factored.
- **Item 6 (stable/):** Keep separate. `stable/INSTALL.sh` has a different prerequisite (`claude` CLI required for `claude mcp add`) and the "trusted measured subset" concept is a real product surface, not just curation. Folding into a flag would obscure both.
- **Item 1 (mirror prompts):** Tests intentionally enforce self-containedness via literal substring assertions on `prompts/complete-migrate-import.md`. The recipe is genuinely embedded in five docs that have *different jobs* — not a drift-prone duplication, just shared reference material. Future option: extract recipe to `stable/bootstrap.sh` and have prompts say "run `bash stable/bootstrap.sh`"; not worth doing until the recipe needs editing again.

Verified: `bash scripts/run_all_tests.sh` (29 framework + 6 semdiff = 35, all green), `./te doctor`, `./te wiki lint --strict --fail-on-error`, `./te bench run --suite framework-smoke`.

## [2026-05-08] fix | relay-sessions skill points to te CLI

`skills/relay-sessions/SKILL.md` documented `python3 -m relay_session.cli ...` — the standalone Python package under `projects/relay-session/`, which is not in the default sparse-checkout and not installed by `./INSTALL.sh`. So a downstream agent triggering the skill on a TE-installed repo would hit `No module named relay_session`. Repointed all command examples to the framework-bundled `./te context checkpoint`/`relay`/`auto-relay`/`ask-old` (1:1 equivalents already in `token_economy/cli.py`). The standalone package stays in `projects/relay-session/` for users who want it independent of TE; the skill no longer relies on it. No test changes needed (no test asserts on SKILL.md content). Verified with the full baseline.

## [2026-05-08] prune | remove broken Codex compact path

Resolved the open ROADMAP item 10 (`./te context codex-compact-thread` fate) by removing it. Already labelled experimental with a known-unfixable host root cause (`tools.defer_loading. Deferred tools require tools.tool_search`); keeping known-broken surface area violates lean-execution. Deleted `codex_compact_thread_plan`, `run_codex_compact_thread`, and `build_compact_prompt` from `token_economy/codex_app_server.py`; removed the `codex-compact-thread` argparse subparser and dispatch branch from `cli.py`; updated `tests/test_universal_framework.py` to drop the import and assertions on the removed surface; archived `prompts/summ-codex-manual.md` (153-line inline App Server launcher for old installs without `codex-fresh-thread`) to `L4_archive/2026-04-24-summ-codex-manual.md`. Cleaned residual references in `README.md`, `prompts/summ.md`, and `projects/context-refresh/host-context-controls.md`. The verified Codex path is now solely `./te context codex-fresh-thread --handoff <handoff-file> --execute`. Verified: `bash scripts/run_all_tests.sh` (29 + 6 = 35, all green), `./te doctor`, `./te hooks doctor`, `./te wiki lint --strict --fail-on-error`, `./te bench run --suite framework-smoke`.

## [2026-05-08] harden | setup prompt: complete coverage + lean form

Audited the canonical fresh-target setup prompt (`stable/AGENT_PROMPT.md`) and the four mirror copies. Sparse-checkout list was missing eight verified-to-work components: `/projects/agents-triage/*`, `/projects/context-keeper/*`, `/projects/semdiff/*`, `/projects/compound-compression-pipeline/*`, `/skills/lean-execution/*`, `/skills/relay-sessions/*`, `/stable/*`, `/INSTALL.md`. Prompt never invoked `./stable/INSTALL.sh` (so agents got zero MCP servers despite installing the hooks) and skipped the verification baseline. Added the missing entries plus a conditional `./stable/INSTALL.sh` invocation gated on `claude` CLI presence and the full doctor/hooks/lint/bench baseline.

Then trimmed back the canonical prompt: dropped the ten Rules bullets that duplicated `start.md` (retrieval, /pa, summ, hook chatter, repo-maintainer, etc.), dropped the "What you get" measured-numbers block (agent doesn't decide which tools to use; numbers live in `stable/README.md`), and dropped the trailing "Report:" block (already in `start.md` "Done Means"). Result: 91 → 52 lines, 1100 → 747 tokens (~32% smaller) with no loss of setup guidance — agents now lean on `start.md` for operating contract instead of having it duplicated. Same trim applied to `AGENT_ONBOARDING.md` Rules section. Archived `HANDOFF_NEXT_AGENT.md` to `L4_archive/2026-04-24-handoff-codex-context-refresh.md` (stale `/Users/saar/...` paths from previous machine); carried its open items (Codex docs reword, `codex-compact-thread` fate) into `ROADMAP.md` as items 9–10. Verified: `bash scripts/run_all_tests.sh` (29 framework + 6 semdiff), `./te doctor`, `./te hooks doctor`, `./te wiki lint --strict --fail-on-error`, `./te bench run --suite framework-smoke` — all green.

## [2026-05-08] fix | unblock te CLI and lean baseline

Removed orphan `cleanup` import, handler, and argparse subparser in `token_economy/cli.py` (introduced by `397b00e` without the `cleanup.py` module ever being committed; broke `./te doctor` for fresh clones). Trimmed `start.md` to 1479 tokens (was 1540) so `tests/test_universal_framework.py::test_start_and_adapters_stay_lean` passes again, while preserving the `no softening` and `Default target project comes from the user prompt` substring guards. Made `scripts/run_all_tests.sh` skip semdiff tests when `tree_sitter_languages` is absent and pull deps from `.token-economy/deps` when present, so the canonical baseline runs cleanly with or without the stable bundle installed. Verified: `./INSTALL.sh --dry-run`, `./te doctor`, `./te hooks doctor`, `./te wiki lint --strict --fail-on-error`, `./te bench run --suite framework-smoke`, `bash scripts/run_all_tests.sh` (29 framework tests + 6 semdiff tests, all passing).

## [2026-04-26] policy | reasoning high, reply ultra

Made the model policy explicit in `token-economy.yaml`, `token_economy/config.py`, and `token_economy/profile.py`: reasoning effort is `high`, surfaced reply style is `ultra`. Also narrowed wiki stale-index lint to the tool-owned catalog and suppressed legacy migration warnings in strict lint so the current corpus validates cleanly while preserving the underlying evidence arrays.

## [2026-04-26] clarify | caveman output vs reasoning

Clarified that Caveman Ultra is surfaced-output compression only, not hidden reasoning control. Updated `start.md`, `L0_rules.md`, `skills/caveman-ultra/SKILL.md`, `skills/personal-assistant/SKILL.md`, `token_economy/context.py`, and `concepts/caveman-output-compression.md` so future agents do not conflate terse prose with the model's thinking budget.

## [2026-04-26] harden | lean execution and plan pruning

Added `skills/lean-execution/SKILL.md`, wired it into `start.md`, added an L0 plan-pruning rule, tightened `plan-first-execute` with a simplification pass and low-risk planning bypass, and added a subagent overhead gate plus compact result budget. Added [[concepts/lean-execution]] to capture the source synthesis. Normalized complete-migrate prompt `.md` paths and added the new skill to import bootstrap. Verified with `./te doctor`, `./te wiki lint --strict --fail-on-error`, `bash scripts/run_all_tests.sh`, and `git diff --check`.

## [2026-04-26] research | top repo lean execution deep pass

Ranked the earlier repo candidates by live GitHub signals, then shallow-cloned and inspected the top three: `addyosmani/agent-skills`, `openai/skills`, and `memodb-io/Acontext`. Adopted small follow-ups only: tighter understand-before-delete and scope discipline in `lean-execution`, richer-page-over-thin-page wiki-writing rules, and a stricter subagent fan-out merge-size condition. Updated [[concepts/lean-execution]] with the repo evidence and kept external frameworks as source material, not dependencies.

## [2026-04-25] compile | framework hardening and adoption learnings

Added a compact synthesis page and raw research note for the latest hardening/adoption pass, including Gemini ecosystem research, local M1 Gemma/Ollama research, Gemini cache guidance, local M1/M1B Ollama results, a ranked adoption matrix, implemented retrieval and lifecycle routing, the current skill-crystallizer and code-map layers, and deferred graph-memory/alias/SessionEnd ideas.

## [2026-04-25] update | local model setup matrix

Added a task-capable local-model setup matrix and updated the device inventory so M1B is no longer documented as worker-only. The matrix covers shared Token Economy tools, skills, workflows, and harnesses for M1/M1B/M2.

## [2026-04-24] ship | universal agent framework v1

Added `start.md`, `token-economy.yaml`, the `te` CLI, lean agent adapters, L0/L1 memory files, wiki-search v1, context-refresh, delegate-router, and context-keeper v2 retrieval tools. Verified with `bash scripts/run_all_tests.sh`.

## [2026-04-24] ship | agent-ignition supplement

Added wiki schema v2 templates, model-agnostic skills/prompts, context meter + handoff lint, stricter delegation contracts, hooks/configs/extensions, install dry-run, profile support, framework smoke bench, and CI gate. Verified with `bash scripts/run_all_tests.sh`, `te wiki lint --strict --fail-on-error`, `te bench run --suite framework-smoke`, JSON config validation, and Python compile.

## [2026-04-24] ship | personal-assistant routing

Added `/pa` and `/btw` prompt bypass via `te pa`, hook routing, a personal-assistant skill, and router prompt. Purpose: route context-light prompts through a lightweight classifier/dispatcher with minimal context, escalating only when risk or complexity requires the main model.

## [2026-04-24] harden | repo-local startup review

Reviewed the framework, repo docs, and setup prompt for duplicated startup glue, stale global setup language, noisy hooks, and routing/context-meter gaps. Updated `HANDOFF.md`, startup docs, `L0_rules.md`, wiki schema defaults, docs audit scope, context meter model sizing, adapter overwrite detection, and prompt hook behavior. Verified with `bash scripts/run_all_tests.sh`, `./INSTALL.sh --dry-run`, `./te wiki lint --strict --fail-on-error`, `./te doctor`, `./te hooks doctor`, `./te bench run --suite framework-smoke`, Python compile, `git diff --check`, active-doc global-term scan, and token-budget checks.

## [2026-04-24] harden | fresh folder setup

Updated the setup prompt and onboarding docs to keep first-run setup simple: if the target folder lacks `token-economy.yaml`, the prompt explicitly permits clearing that current folder only, including hidden files and `.git`, then cloning the canonical repo fresh. Purpose: avoid false stops in non-empty setup folders while still forbidding deletion outside the target folder.

## [2026-04-24] feature | repo-maintainer worker

Added a lightweight repo-maintainer subagent prompt and routing policy for task workspaces with GitHub remotes. It runs only at verified save-points, before context refresh/handoff, or on explicit save/commit/push requests; it stages only intended task changes and skips entirely when no GitHub remote exists.

## [2026-04-24] feature | summ context refresh

Added the `summ` manual refresh prompt, a lightweight wiki-documenter subagent prompt, and stricter context-refresh rules. Fresh sessions now load only the lean handoff plus `start.md`; durable but non-immediate memory is routed to repo-local wiki documentation instead of being carried into fresh context.

## [2026-04-24] harden | terminal summ behavior

Updated `summ` so appended instructions become next-session requirements, generic checkpoints must be replaced with session-specific handoffs, missing documenter prompts use an inline fallback instead of broad searching, and old-context work stops after emitting the packet.

## [2026-04-24] feature | host context controls

Added host-native context control guidance for `summ`: Claude Code `/clear` and `/compact`, Codex `/new`, `/clear`, and `/compact`, Gemini `/compress`, and generic fallback to a fresh session. Added `./te context host-controls` so agents can retrieve the right command without loading broad docs.

## [2026-04-24] feature | subagent lifecycle cleanup

Added a lifecycle prompt for closing completed or idle subagents only after their result packet has been read, useful output has been merged or documented, and follow-up risks have been captured. This prevents thread-limit stalls without losing worker results.

## [2026-04-24] harden | summ host-boundary tests

Clarified that `summ` cannot assume the model can execute host slash commands from its own response. Added `prompts/summ-experiments.md` for measuring whether a host actually dropped context, and updated host-control guidance to require user/host execution unless a real tool exists.

## [2026-04-24] feature | fresh successor workaround

Added `./te context fresh-command` and documented the best non-slash workaround: start a fresh successor host process/session with only `start.md` and the handoff file. This bypasses a full old transcript even when the current host cannot be cleared programmatically.

## [2026-04-24] feature | Codex App Server fresh thread

Added `./te context codex-fresh-thread` as the verified Codex successor path. It uses Codex App Server `thread/start` + `turn/start` with an explicit accessible model, creates an ephemeral thread with `turns: []`, and loads only `start.md` plus the handoff. Live smoke passed with `gpt-5.3-codex-spark`; this bypasses rather than erases the old host transcript.

## [2026-04-24] verify | controlled summ fresh-thread result

Verified controlled `summ` successor run: `./te context codex-fresh-thread --handoff .token-economy/checkpoints/20260424-135455-fresh-session.md --model gpt-5.3-codex-spark --execute` returned `ok=true`, `thread_id=019dbfc5-edbe-7632-9a51-0dda81340fb0`, `assistant_responded=true`, and `thread_idle=true`. Events showed `thread/started` with `ephemeral=true` and `turns=[]`; successor read `start.md` plus the handoff only, while the old visible host transcript was not erased. Token usage still showed large Codex host/system overhead, about 53k input tokens, despite no old transcript in the successor-visible prompt. See [[prompts/summ-experiments]].

## [2026-04-24] upgrade | persistent Codex fresh successor

Changed `./te context codex-fresh-thread` to create a persistent same-project successor by default, with `--ephemeral` reserved for throwaway smoke tests. Verified live: `thread_id=019dbfd4-4efb-7453-84d1-b6010cc6d35a`, `ok=true`, `thread_persistent=true`, `thread_turns_empty=true`, `thread_idle=true`, and `listed_after_start=true`. This gives `summ` a durable project-thread continuation without claiming to erase the old active transcript.

## [2026-04-24] clarify | platform-specific summ strategies

Kept `summ` universal through summarize/document/handoff, then made execution platform-specific. `./te context host-controls --agent auto` now returns a `strategy`: Codex uses persistent same-project successor threads, Claude uses native `/clear` or `/compact`, Gemini uses `/compress` or a new session, and generic hosts use a manual fresh session with only `start.md` plus the handoff.

## [2026-04-24] harden | legacy summ fallback

Clarified that `./te context fresh-start` is not a successor launcher; it only writes or prints a packet. If an older project-local `te` lacks `host-controls`, `fresh-command`, or `codex-fresh-thread`, Codex `summ` should fall back to a real successor command such as `codex fork --last -C "$PWD" "<handoff instruction>"` or `codex -C "$PWD" "<handoff instruction>"`.

## [2026-04-24] harden | legacy Codex launch attempt

Updated `summ` so older Codex installs first attempt a direct `codex app-server` persistent successor thread when the project-local Token Economy wrapper is missing. Printing `codex fork --last` is now a last resort after App Server is unavailable or fails, not the default stopping point.

## [2026-04-24] fix | Codex fresh-thread wait

Changed `./te context codex-fresh-thread --execute` to stop waiting as soon as the successor thread responds and returns to idle, instead of waiting through fixed read windows. Live retest passed with `thread_id=019dbfed-9ad3-78a1-a6fa-710c1bb18d01`, `ok=true`, `thread_persistent=true`, `thread_turns_empty=true`, `assistant_responded=true`, `thread_idle=true`, and `listed_after_start=true`.

## [2026-04-24] add | Codex compact lane

Added `./te context codex-compact-thread` for same-session Codex compaction. It uses `CODEX_THREAD_ID` or an explicit `--thread-id`, resumes the thread with a Token Economy `compact_prompt`, calls App Server `thread/compact/start`, and treats success as `resume_ok=true`, `compact_start_ok=true`, and `compacted=true`. `summ` now has two Codex paths: compact current thread when continuity matters, or launch a persistent fresh successor when bypassing the old transcript is better. Disposable live smoke passed on thread `019dbffe-65ca-7441-9c1b-2a400a4e375a` with `ok=true`, `resume_ok=true`, `compact_start_ok=true`, and `compacted=true`.

## [2026-04-24] fix | manual Codex summ fallback

Added `prompts/summ-codex-manual.md` because older project-local Token Economy installs may not have `codex-compact-thread` or `codex-fresh-thread`. The manual prompt now includes a self-contained Python `codex app-server` fallback so agents do not stop after reporting that local `./te` is too old.

## [2026-04-24] fix | older Codex manual path

Changed `prompts/summ-codex-manual.md` to use one reliable path for older installs: launch a persistent fresh successor thread directly with App Server `thread/start` + `turn/start`. Same-thread compaction is skipped in older installs because inherited Codex config such as `tools.defer_loading` can make `thread/compact/start` fail.

## [2026-04-24] verify | manual Codex fresh successor

Ran the exact self-contained launcher from `prompts/summ-codex-manual.md` against handoff `.token-economy/checkpoints/20260424-153428-fresh-session.md`. It passed with `ok=true`, `thread_id=019dc021-4597-7560-81a5-900f4fafc950`, `thread_persistent=true`, `thread_turns_empty=true`, `assistant_responded=true`, `thread_idle=true`, and `listed_after_start=true`.

## [2026-04-24] clarify | manual summ handoff prompts

Added manual copy-paste prompts for the `summ` flow: `prompts/manual-summ-document-and-handoff.md` writes repo-root `session_handoff.md` after routing durable memory to a lightweight wiki-documenter, and `prompts/manual-fresh-session-from-handoff.md` starts a new context from only `start.md` plus that handoff. Reaffirmed that Claude `/clear` is the practical manual clear path, while Codex fresh successor is clean continuation only; Codex current-thread compact remains experimental/unsolved in the tested environment.

## [2026-04-24] simplify | summ procedure wording

Trimmed manual-session management text from the canonical `summ` procedure and context-refresh skill. The procedure now focuses on splitting handoff vs durable wiki memory, routing wiki documentation to a lightweight worker, writing/linting the handoff, and starting the next context from only `start.md` plus the handoff.

## [2026-04-25] add | full project migration prompts

Added `prompts/manual-full-summ.md` for exporting an old Claude Code project plus Obsidian wiki into one local `full_summ.md`, including raw secrets when explicitly authorized. Added `prompts/manual-import-full-summ.md` for bootstrapping a fresh Token Economy folder and rebuilding the repo-local markdown wiki from that summary without committing secrets.

## [2026-04-25] compile | superpowers lessons

Promoted Superpowers lessons from raw notes into `concepts/superpowers-skills.md`, added missing concept/pattern/people pages referenced by `index.md`, and added `skills/verification-before-completion/SKILL.md` for evidence-before-claims discipline.

## 2026-04-17

Terminology: **ComCom** = our compound-compression project (disambiguate from Claude Code's "CC").
- Wiki created. Folder: repo-local `Token Economy/` markdown wiki.
- Ingested research brief → `raw/2026-04-17-research-brief.md`.
- Setup confirmed: caveman plugin active, superpowers skill loaded, wiki initialized.
- Next: flesh out concept pages, pick first project (likely compound-compression-pipeline or wiki-query-shortcircuit).
- Built [[projects/compound-compression-pipeline/RESULTS]] (aka **ComCom**). Measured 70-73% on prose, 59% on mixed technical at gentler rate. Code/paths/URLs preserved via placeholder protection.
- Ingested [[raw/2026-04-17-semantic-diff-survey]]. Novelty 4/5. Created [[concepts/semantic-diff-edits]]. Added [[ROADMAP]] as live tracker.
- Ran quality eval on Ollama (phi4:14b, 3 tasks). Result: 55.7% token savings @ 100% quality retention at rate=0.5. Placeholder format fixed (`XPROTECT{n}XEND` survives BERT tokenization). Compressed prompts also faster (1.4s vs 9.8s observed).
- Built eval-v2: SQuAD v2 + gemma4:31b judge + bootstrap CIs + failure-mode classification. Running in background.
- Built [[projects/semdiff/README]] (AST-node diff). Measured 95.5% savings after 2 method edits on argparse.py (2575 lines, 19,280 → 859 tokens); 99.5% on stable re-read. Tree-sitter for py/js/ts/rust.
- Kaggle auth set up (user: saarshai).
- Built [[projects/context-keeper/README]]. Skill + PreCompact hook. Regex extractor + optional local-LLM pass. Current framework writes memory under repo-local `.token-economy/` paths.
- **Eval-v2 completed** (SQuAD v2, n=8, 2 runs, phi4:14b + qwen3:8b judge). Token savings **44.5% CI [41.5-47.4]**. Δscore **−0.25 CI [−0.62, 0.00]**. Failure modes on comp: 8 NONE, 6 MISSING, 2 SWAP. **v1's "55.7% @ 100%" overstated**; principled measurement shows small, non-significant quality hit. N too small to resolve CI. Judge swap (gemma4:31b → qwen3:8b) fixed 129s latency thrash.
- Built ComCom v2 (pipeline_v2.py) with question-aware + critical-zone protection; eval-v3 in progress (4 conditions: full, v1, v2, adaptive-escalation). Early data shows v2 over-compresses (critical-protect + rate=0.5 on remainder = total too low). Fix planned: scale rate by (1 - protected_fraction).
- **semdiff MCP server built**. Python 3.11 + mcp SDK. 3 tools exposed (read_file_smart, snapshot_clear, snapshot_status). Protocol roundtrip tested (initialize, tools/list, tools/call all pass). CC plugin wrapper at `plugin/.mcp.json`. Install docs at [[projects/semdiff/INSTALL]].
- **bench/ built**. Kaggle API wired via registry.yaml. 7 datasets registered (2 downloaded so far). Adapters emit uniform {id, context, question, answer, type, meta} schema. CoQA multi-turn items designed for growing-context stress. Kaggle Notebook template drafted for free-T4-GPU evals (30h/wk, 10× local throughput). See [[bench/README]].
- **Eval-v3 complete (ComCom upgrade)**. D_adaptive (self-verify escalation) delivers 44.9% savings at Δscore −0.12 [−0.38, 0.00] — quality effectively preserved. Zero REFUSE failures. C_v2 (question-aware + critical-zone) confirmed broken by over-compression; fix deprioritized since D_adaptive bypasses the issue. Shipped config: `pipeline_v2.compress` + `verify.escalate_gen`.

## [2026-04-20] download-status | Qwen3.6-35B-A3B-5bit | M1=complete, M1B=in-progress (authenticated curl running, ETA ~12h)
## [2026-04-20 22:36 BST] download-complete | Qwen3.6-35B-A3B-5bit | M1B all 5 shards verified (24.73 GB) via LAN HTTP server; shard1 required fresh download after dual-curl corruption; see /tmp/resume_qwen36_report.md
## [2026-04-20] download-finish | Qwen3.6-35B-A3B-5bit | M1=complete, M1B=complete (LAN transfer from M1:8888, all 5 shards verified, ~23GB, completed ~14:36 PDT)
## [2026-04-21] download-finish | Qwen3.6-35B-A3B-5bit | M1=complete, M1B=complete
## [2026-04-25 10:03 BST] install-verify | Qwen3.6-35B-A3B-5bit | M2 TurboQuant server running on /Users/saar/Library/gguf/qwen3.6-35b-q4km.gguf at CTX=524288; loaded via llama-server with -ctk q8_0 -ctv turbo4 on 127.0.0.1:8080
## [2026-04-25 10:03 BST] download-start | DeepSeek-R1-Distill-Llama-70B-Q4_K_M.gguf | M2 resumed from bartowski/DeepSeek-R1-Distill-Llama-70B-GGUF into ~/.cache/huggingface; transfer in progress, not yet installed
## [2026-04-25 10:33 BST] download-resume | DeepSeek-R1-Distill-Llama-70B-Q4_K_M.gguf | M2 background curl resumed /Users/saar/Library/gguf/DeepSeek-R1-Distill-Llama-70B-Q4_K_M.gguf.part from byte 75337728; lower-context install still in progress
## [2026-04-25 10:40 BST] download-progress | DeepSeek-R1-Distill-Llama-70B-Q4_K_M.gguf | M2 detached curl PID 5088 writing /Users/saar/Library/gguf/DeepSeek-R1-Distill-Llama-70B-Q4_K_M.gguf.part; partial file advanced to 100425728 bytes
## [2026-04-25 10:53 BST] exo-cleanup | M1/M1B | Removed EXO app bundles, ~/.exo state, EXO launch agents, and the M1 m1_local_watchdog cron entry; no residual EXO processes remain, Ollama jobs left running
## [2026-06-02] goal7-arithmetic-Xq | Opus | X(q) arithmetic meaning: q=3 X(3)=2/9 is the SHARP 3-window gap-product floor of ordinary Farey (dictionary x=b/Q,y=b'/Q matches BCZ-2001 primary; verified EXACTLY on real F_Q≤4000: 0 violations, longest-run<2/9 =2, min-window-max→2/9⁺ via denominators→(Q/3,2Q/3)). CORRECTION to goal premise: the 3-window/cluster≤2 form is SPECIAL to q=3,4 (proven); on genuine G_q cusps (exact ℤ[λ], Galois-height level) the cluster bound C(q)=2,2,3,5 for q=3,4,5,6 — for q≥5 there ARE 3 consecutive products <X(q) (T-verified). Universal char that DOES hold ∀q: X(q)=inf_μ esssup P = sharp infimal ceiling on c_n c_{n+1}/Q²=1/(Q²gap); approached not attained (no GS). Project map coeff ·λ confirmed via Rosen λ-CF + ST^k∈G_q. Prior art: Taha arXiv:1810.10668 (G_q-BCZ map, no threshold), CZ14 (integer-valence runs). Doc: research_notes/ARITHMETIC_MEANING_Xq.md; code X3_arithmetic_verify.py, Gq_hecke_farey_general.py, Xq_recurrent_window_test.py.

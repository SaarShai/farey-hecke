# The Pipeline as Methodology — an AI-assisted verified-discovery engine

**Date:** 2026-06-14 · **Status:** internal draft (USER-gated; nothing outward) · **Branch:** hecke-goalL-2026-06-03

> **Thesis (one sentence).** The durable contribution of this project is not the Hecke onset
> theorem; it is a *reusable research engine* — autonomous scout → adversarial falsification →
> machine-verification (Lean + Aristotle) over certified exact/transfer-operator numerics, run
> largely hands-off with **honest-negative discipline** — and its distinctiveness in the
> 2024–2026 AI-for-math landscape is the **falsification gate that kills false positives before
> they reach the prover, and records NEGATIVE results as first-class output.**

This note is a draft. Every build/axiom/numeric claim below was re-verified first-hand this
session; the exact verification commands and their quoted output are in §6.

---

## 1. The architecture

The engine is a loop, not a model. Five components, wired through a write-gated memory:

```
                 ┌────────────────────────────────────────────────────────────┐
                 │  WRITE-GATED MEMORY (wiki-memory / MEMORY.md)                │
                 │  verified facts only; reasons required ("because…")          │
                 └──────────────▲───────────────────────────────▲──────────────┘
                                │ (durable, deduped)             │
   ┌────────────┐   candidates ┌┴───────────────┐  survivors  ┌─┴──────────────┐
   │ (1) SCOUT  │─────────────▶│ (2) ADVERSARIAL │────────────▶│ (3) MACHINE-    │
   │ orchestrator│              │   FALSIFICATION │  (only what  │     VERIFY      │
   │ + subagent  │◀─ negatives ─│      GATE       │   survives)  │  Lean+Aristotle │
   │   fan-out   │              │  (kill F.P.s)   │              │  + (4) NUMERICS │
   └────────────┘              └─────────────────┘              └────────┬───────┘
                                                                          │
                                                       ┌──────────────────┴───────┐
                                                       │ (5) COMPUTE FLEET         │
                                                       │ M1/M2 (mpmath/sympy),     │
                                                       │ certified transfer-op /   │
                                                       │ Jenkinson–Pollicott /     │
                                                       │ exact-arithmetic engines  │
                                                       └───────────────────────────┘
```

- **(1) Orchestrator + subagent fan-out.** A workflow script spawns subagents (this report is
  itself a spawned subagent) over a small task graph; each returns a structured result. Multi-host
  adapters (`adapters/{claude,codex,cursor,gemini,universal}`) let the same skill bodies run on
  different model hosts. Token Economy (`te`, `token-economy.yaml`, `skills/`, `hooks/`) is the
  framing/context-management substrate — **tooling only, not the subject.**
- **(2) Adversarial falsification gate.** Before any expensive proof or claim, a candidate is
  attacked: pushed to larger numerical bounds, restated as the *negation* and tested, cross-checked
  against an independent oracle, or vetted by a second fan-out of agents whose job is to break it.
  This is the load-bearing differentiator (§5).
- **(3) Machine-verification.** Lean 4 (Mathlib v4.28.0) for proofs; the Harmonic **Aristotle** CLI
  as a proving subagent for hard obligations. Acceptance = `lake build` exit 0 **and** a clean
  `#print axioms` (`[propext, Classical.choice, Quot.sound]`, no `sorryAx`).
- **(4) Certified numerics.** Validated transfer-operator / Jenkinson–Pollicott dimension engine
  (`code/d3_jp_dimension.py`, recovers dim E₁,₂ = 0.5312805 to 1e-15); exact arithmetic over number
  fields to degree 11; a χ₂ reciprocity oracle (`code/reciprocity_oracle.py`) validated against the
  authors' own PARI/GP; an exact equiangular-lines engine. Numerics *discover and bound*; they do
  not by themselves prove.
- **(5) Compute fleet.** M1 (`ssh new@192.168.1.22`, sympy+mpmath, 10c) and M2
  (`ssh alicia@192.168.1.92`, mpmath, 12c) for the search/certificate hunts the local box can't run.
- **Write-gated memory.** `wiki-memory` + `MEMORY.md` persist only verified facts, each carrying a
  reason; the `write-gate` skill rejects reasonless decisions, so the memory doesn't accumulate
  unfalsifiable lore. Negatives are written with the same weight as positives.

---

## 2. The worked demonstration (this project, this session)

The engine's track record this session — **the positives AND the negatives are both the evidence.**

### Positives (machine-verified)
- **Uniform onset theorem.** `X_Ω(q) ≥ 1/λ_q³` (λ_q = 2cos(π/q)) for the Taha G_q–BCZ map.
  `ToplevelStitch.Xomega_lb_allq` builds and is **axiom-clean** (no `sorryAx`); q = 5..18 is
  fully unconditional, q ≥ 19 carries the genuine-map hypothesis P2 as a *named hypothesis in the
  statement* (`GenuineClassP2` / `hCorr`), not as a sorry. The hard arc-width inequality **L1b**
  (`fcorr_lb` / `B1_target` in `L1bArcCoverage.lean`) is **sealed, sorry-free, axiom-clean** — this
  was the last open piece of mathematics, and it closed only *after two Aristotle prover passes
  failed* and an M1-found certificate / corrected two-regime architecture made it tractable (§5).
- **Arithmeticity dichotomy.** Cluster ceiling = 2 iff q ∈ {3,4,6}; exact witness ladder q = 5..24
  (`code/goal1_q*_witness_exact.py`); submission-ready manuscript
  (`research_notes/PAPER_arithmeticity_dichotomy_SUBMISSION.md`, 632 lines). X(q) = 1/λ³ identified
  as the ergodic ground value = cluster onset.

### Negatives (honest, recorded, do-not-rechase)
These are not failures of the engine — they are the engine *working*, refusing to manufacture a
result and saving the effort that overclaiming would have wasted:
- **Physics / wide-appeal: all falsified.** Aubry–Mather, QRT/integrable-systems, quasicrystals,
  circuit-QED hyperbolic lattices — each killed with a specific contradiction (e.g. BCZ is weakly
  mixing ⇒ not integrable, contradicting any QRT/cluster-algebra framing).
- **Broad-reach-solo: structurally empty.** The pipeline-target scout
  (`pipeline_target_verdict_2026-06-14.md`) concluded the intersection of *real edge* and *broad
  reach* is ~empty for this engine alone — where the edge is real (certified transfer-operator
  dimension) the reach is niche and already owned (Pollicott–Vytnova / MMPV); where the reach is
  broad (Zaremba, sphere-packing) the bottleneck is analytic and unreachable by these tools.
- **N(18) equiangular lines:** machinery validated, N(18) ≥ 57 re-certified, but the bound is **not
  movable at our compute scale** — reported as such, not papered over.
- **χ₂ reciprocity scan: empty.** No new local-global obstruction; the cheap catalogs reduce exactly
  to the published Rickards–Stange Ψ family (the negative is *structurally explained*, not just
  "didn't find one").

The honest-negative count roughly matches the positive count. That ratio is the point.

---

## 3. Falsification caught its own false positives (the self-correction record)

Three concrete cases where the gate killed something the engine itself had produced or was about to
trust — each verified first-hand this session:

1. **8 reciprocity false positives, killed at B = 2,000,000.** A loose inline classifier flagged 128
   semigroup orbits; rigorous reclassification left 8 "non-published alphabet" candidates
   (CF[3,7,11], CF[4,7,8], …). The gate pushed each to a deep orbit (bound 2·10⁶); **all 8 were
   false positives** — χ₂ was not actually constant, an artifact of thin orbits at the cheap bound
   B = 2·10⁴. (`research_notes/reciprocity_scan_2026-06-14.md`, lines 89–92, 145–146.)
2. **The `windowMaxCos_lb` FALSE lemma, caught with an explicit counterexample.** An intermediate
   Lean lemma claimed `windowMaxCos ≥ 2√6/5` uniformly. An Aristotle pass **disproved** it: at
   q = 18, μc = 1.2 (inside the domain), the window-max cosine ≈ −0.14, dropping to ≈ −0.68 near the
   endpoints. The lemma was *removed with a documented counterexample* and the proof re-architected
   into the correct two-regime argument — **not left as an unprovable sorry.** (Aristotle run
   summary `projects/aristotle_dispatch_v15/ARISTOTLE_SUMMARY.md` + `B1_RESULT.md`;
   `L1bArcCoverage.lean:261` records the removal.) This is why the *first two prover passes failed*:
   they were chasing a false intermediate. The gate forced the correction that made L1b sealable.
3. **The ~q/3 → ~q/6 cross-branch artifact, corrected.** The cluster-ceiling growth rate was first
   reported as ~q/3; adversarial re-examination found this was an artifact of a *cross-branch* cluster
   counter (a `P<X`-over-all-branches condition pinned at run-length 8 for q = 19..24, reading as a
   spurious linear jump). The correct *last-branch* counter gives slope ≈ 0.168 (~q/6); the q = 13
   value (B = 4) is identical under both counters — only the *rate* was wrong.
   (`research_notes/goal1.5_uniform_obstruction.md`, lines 103–111.)

A separate earlier "C_q refuted" reciprocity-style claim (in MEMORY) was *itself* a bug (wrong
eigenvalue bisect) caught by adversarial verify — the gate even catches its own gate bugs.

---

## 4. Honest scope

The engine **discovers and verifies**; it does not replace a theory program.

- It excels at producing **certified artifacts** in dynamics / number theory: machine-checked Lean
  theorems, interval-certified numerics, exact witness ladders, and *certified non-existence*
  (the negatives).
- It does **not** crack broad-reach pure-math problems solo: the structural verdict (§2) is that the
  analytic/SDP bottlenecks of broad-reach problems sit outside what scout+falsify+verify can reach.
- The honest positioning is **the Koyama model**: pair the engine with a theory collaborator —
  computation discovers and certifies, theory supplies the mechanism — OR own the **methodology
  narrative** itself (a reusable AI-math verified-discovery engine, demonstrated on the Hecke /
  dichotomy results plus the disciplined negatives). The methodology is the broadest-reach artifact
  the project actually has.

---

## 5. Positioning vs the 2024–2026 AI-for-math landscape

| System | What it does | Discovery? | Falsification gate? | Negatives as output? |
|---|---|---|---|---|
| **AlphaProof** (DeepMind, *Nature* 2025) | RL prover; IMO 2024 silver; trained on ~100M autoformalized problems | No — proves *given* problems | No (RL reward, not adversarial-kill) | No |
| **Aristotle / Harmonic** (arXiv:2510.01346; IMO 2025 gold, 5/6) | Lean proof search + lemma reasoning + geometry; 200B+ MCGS | No — proves given statements | No | No |
| **LeanAgent** (ICLR 2025; arXiv:2410.06209) | Lifelong learning; proved 162 previously-unproved theorems across 23 repos | Partial (picks targets) | No | No |
| **Aletheia** / **FunSearch** (2026; DeepMind/Tao) | Autonomous research; solved Erdős-database problems; program-search constructions | **Yes** | No — optimizes *toward* positives (reward/score loop) | No (negatives discarded) |
| **This pipeline** | scout → adversarial falsify → Lean+Aristotle verify + certified numerics | **Yes** | **Yes — kills false positives before proving** | **Yes — negatives are first-class, recorded, reasoned** |

**Where it sits.** Aristotle is a *component* this pipeline calls, not a competitor; AlphaProof and
LeanAgent are provers (they need the statement handed to them); Aletheia/FunSearch are the closest
relatives — genuinely autonomous discovery — but they run a *positive-reward* loop that optimizes
toward constructions/proofs and discards the misses.

**The distinctive claim (one sentence).**
> *No prominent 2024–2026 AI-for-math system pairs autonomous conjecture discovery with an
> adversarial falsification gate that kills false positives BEFORE the prover is invoked and treats
> certified NEGATIVE results as first-class, reasoned output — which is precisely what keeps this
> pipeline from overclaiming and is the source of its honest, reproducible track record.*

Three honest caveats on the claim: (i) it is a claim about *workflow composition*, not raw proving
power — AlphaProof/Aristotle are stronger provers; (ii) the discovery scout here is LLM-agent-driven,
not a trained search policy, so its *reach* is narrower than a 200B MCGS system; (iii) "first-class
negatives" is a *discipline* (write-gate + honest-negative records), enforced by tooling and review,
not a learned objective — its value is methodological, and it is the part most directly transferable
to other domains.

---

## 6. First-hand verification (quoted this session, 2026-06-14)

All commands run on branch `hecke-goalL-2026-06-03`, toolchain `leanprover/lean4:v4.28.0`,
in `projects/aristotle_dispatch_v15/uniform_q5to18`.

**L1b seal (the hard math) — `lake build L1bArcCoverageLib`, exit 0:**
```
⚠ [8026/8027] Replayed L1bArcCoverage
info: L1bArcCoverage.lean:1588:0: 'L1bArcCoverage.fcorr_lb' depends on axioms: [propext, Classical.choice, Quot.sound]
info: L1bArcCoverage.lean:1589:0: 'L1bArcCoverage.B1_target' depends on axioms: [propext, Classical.choice, Quot.sound]
Build completed successfully (8027 jobs).
```
→ L1b is sealed: `fcorr_lb` / `B1_target` are sorry-free and **axiom-clean** (no `sorryAx`).

**Top-level theorem — `lake build ToplevelStitch`, exit 0:**
```
info: ToplevelStitch.lean:373:0: 'ToplevelStitch.genuine_orbitdata' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ToplevelStitch.lean:374:0: 'ToplevelStitch.perq_Xomega_lb_qge19' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ToplevelStitch.lean:378:0: 'ToplevelStitch.Xomega_lb_allq' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ToplevelStitch.lean:411:0: 'ToplevelStitch.Xomega_lb_allq_clean_modulo_B1' depends on axioms: [propext, Classical.choice, Quot.sound]
Build completed successfully (8046 jobs).
```
→ `Xomega_lb_allq` is **axiom-clean, no `sorryAx`**. (The in-file comment at lines 364–366 still
predicts a trailing `sorryAx` from `fcorr_lb`; that comment is **stale** — it predates the L1b seal
of commit `036c7e4`. The current build shows the `sorryAx` is gone, because `L1b_carried` now
resolves to the proved `B1_target`.) P2 (the q ≥ 19 genuine-map bridge) and the corridor closure
`hCorr` are carried as **explicit named hypotheses in the theorem statement**, not sorries.

**The actual sorry audit (all `*.lean` in the dir):** the only textual `sorry` match outside the
sealed-file docstrings is `BCZHeckeS1_trichotomy.lean:10`, which is **inside the `/-! … -/`
docstring** (a quoted skeleton from the upstream file being *replaced*), not a live tactic. The live
concrete versions (`step_classified_concrete`, `step_trichotomy`) print axioms
`[propext, Classical.choice, Quot.sound]`.

**The three self-caught false positives** are documented in:
`research_notes/reciprocity_scan_2026-06-14.md` (8 F.P.s killed at B = 2·10⁶),
`projects/aristotle_dispatch_v15/ARISTOTLE_SUMMARY.md` + `B1_RESULT.md` (windowMaxCos_lb counterexample),
`research_notes/goal1.5_uniform_obstruction.md` lines 103–111 (q/3 → q/6 correction).

---

## 7. Outline (for an outward methodology write-up, when USER-gated)

1. **Motivation** — why proving power alone overclaims; the missing falsification + honest-negative discipline.
2. **Architecture** — the five components + write-gated memory (§1 diagram).
3. **Worked demonstration** — Hecke uniform onset (axiom-clean modulo named P2) + arithmeticity dichotomy + the matched honest negatives (§2).
4. **Self-correction case studies** — the three false positives the gate killed (§3).
5. **Scope & limits** — discovers + verifies; pairs with theory (Koyama model) (§4).
6. **Positioning** — vs AlphaProof / Aristotle / LeanAgent / Aletheia–FunSearch; the distinctive claim (§5).
7. **Reproducibility appendix** — the verification commands and quoted axiom outputs (§6).

---

### Sources (prior art)
- AlphaProof — Olympiad-level formal reasoning with RL, *Nature* 2025: https://www.nature.com/articles/s41586-025-09833-y
- Aristotle (Harmonic), IMO-level ATP, arXiv:2510.01346: https://arxiv.org/pdf/2510.01346
- LeanAgent — Lifelong Learning for Formal Theorem Proving, arXiv:2410.06209: https://arxiv.org/abs/2410.06209
- Aletheia — Towards Autonomous Mathematics Research (2026): https://arxiv.org/pdf/2602.10177
- AI for Mathematics: Progress, Challenges, Prospects (survey, 2026): https://arxiv.org/html/2601.13209v1

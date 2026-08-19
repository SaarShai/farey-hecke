# Expansion run — 2026-08-15 (owner directive: maximize research value)

## Koyama joint-manuscript integration — 2026-08-16

- [x] Bind the three supplied attachments and identify the latest TeX/PDF pair.
- [x] Reopen the live numerical, spectral, Table 3, and Lean receipts.
- [x] Create an isolated manuscript working copy and preserve source provenance.
- [x] Correct the character selector and propagate its conjugation convention.
- [x] Replace the unsupported fixed-$T$ theorem by an honest two-parameter analytic target.
- [x] Reconcile Table 3 against raw class counts and add the $3\times10^{14}$ endpoint data.
- [x] Integrate the verified low-zero reconstruction, transient correction, and figure.
- [x] Add contribution, Lean-scope, computational-assistance, and data-availability text.
- [x] Build the TeX, inspect warnings/logs, render every page, and visually verify the PDF.
- [x] Add a review/results section recording delivered artifacts and unresolved analytic gates.

Routing receipt: the artifacts are the supplied `nontriv2607.tex`, its two PDFs,
the current `projects/minus1-dominance` receipts, and the new isolated joint-manuscript
directory. The user authorized direct TeX integration. The work is coupled and
judgment-dense; it remains in the main thread. Unrelated dirty-worktree files are excluded.

### Review/results

- Source provenance: supplied TeX SHA-256
  `d6acb7680e4225d1e0d51237a1aacfa14e073ed9edf9a6010f9f9fb93fbb875c`;
  the Downloads copy was not changed.
- Numerical checks: 567/567 baseline cells match; base spectral verifier passes
  55/55 zero checks and 13,578 rows; independent modulus-19 Arb/deep verifier
  passes with 7/7 adversarial tests.
- Formal checks: selector project builds; all four finite nonresidue theorems
  compile against Mathlib v4.28.0.
- Artifact checks: Tectonic build is warning-free; all 8 rendered letter-size
  pages were inspected; the figure, tables, references, and declarations are
  unclipped and correctly ordered.
- Completion gate: 10/10 verification criteria pass; introduced-code security
  triage reports risk `NONE`; blast radius is low and limited to the isolated
  manuscript transformation/build artifacts.
- Open analytic gate: the two-parameter regularized limit, summed off-diagonal
  bound, branch convention, and any transfer to ordinary counts remain
  conjectural. The requested finite-$x$ regularized comparison plot was not
  fabricated.

## Koyama external share packet — 2026-08-16

- [x] Assemble a clean, self-contained packet with manuscript source/PDF,
  figure, numerical data and verifiers, compact Lean sources, and provenance.
- [x] Write an external-facing read-me, technical change log, verification
  report, and concise transmittal memo PDF.
- [x] Draft the reply email, including the unresolved analytic gate and the
  decisions needed before any arXiv replacement or journal submission.
- [x] Generate a deterministic file manifest and checksums, archive the packet,
  and verify archive extraction and all packaged checksums.
- [x] Render and visually inspect every page of the new transmittal PDF; scan
  the packet for internal-only material, credentials, placeholders, and broken
  absolute paths.
- [x] Record final artifacts and verification results here.

Routing receipt: the packet is a new external artifact derived from the already
verified isolated manuscript and receipts. It is SPEC'D/GATED by the user's
request and the manuscript's existing analytic caveats. The work remains in the
main thread because selection, scientific wording, and disclosure boundaries
are coupled and judgment-dense. No correspondence archive or unrelated project
material is in scope.

### Review/results

- Deliverable: `output/koyama_share_packet_2026-08-16.zip` (updated archive),
  SHA-256 `54f16b94803b29545c9320044aee06f7357e376d293d936c5137d92459a2ed76`.
- Contents: 62 files covering the read-me, two-page transmittal
  memo, change log, verification report, eight-page manuscript, figure,
  authoritative curve, independent baseline, all derived spectral/N=19
  outputs, portable scripts, two compact Lean projects, original source, diff,
  and packet-wide checksums.
- The reply email is deliberately outside the packet at
  `output/koyama_reply_email_draft_2026-08-16.md`.
- Archive/integrity: `unzip -t` reports no errors; a fresh extraction passes
  every entry in `support/SHA256SUMS.txt`.
- Numerical live proof from packet paths: baseline 567/567; spectral verifier
  55/55 with 13,578 rows; six base adversarial tests; independent N=19 verifier
  with 17/17 deep checks; seven N=19 adversarial tests.
- Formal live proof: the exact packaged selector source and exact packaged
  four-theorem nonresidue source compile in their pinned Lean 4.28.0/Mathlib
  environments; no `sorry` or `admit` appears in the claimed files.
- PDF live proof: the manuscript rebuilds cleanly to eight letter pages; the
  memo rebuilds cleanly to two letter pages, with no layout warnings. Both memo
  pages were rendered at 144 dpi and visually inspected without clipping,
  overlap, or missing content.
- External-content gate: the reply draft passes all six required criteria
  (scope, corrections, numerics, analytic limits, decisions, tone) at 1.0.
- Security triage: no secret, dangerous sink, dependency, or HIGH/MEDIUM
  finding. Seven lexical REVIEW matches are false positives on mathematical
  uses of “verify”/“role”; there is no authentication or authorization logic.
- Blast radius: LOW and isolated to new external packet artifacts plus this
  task record. No existing source, attachment, or correspondence was modified.

Priority = value to the math research community; significance first.
Routing: Kimi K3 = medium-high lanes; Kaggle = heavy compute; Aristotle =
formalizable lemmas; Opus agents = judgment-dense drafting; frontier = synthesis,
adjudication, gates.

## Ranked goals (this run)

- [ ] **P1 — Family off-line theorem (q = 7 first).** Turn the G₅ first into a
  family statement: rigorously localize an off-line Selberg-zeta zero for the
  non-arithmetic G₇, reusing the declared flagship template (MMS blocks → R2
  envelope → R3b closed-contour winding → K_s gate → determinant transport).
  Fuel: q7/q8 Kaggle scan (harvested). Value: one surface = a first; two+ =
  a program, and evidence the method scales. Lane: Kimi K3 (prep+constants) →
  Kaggle (heavy cert) → frontier gate. Ticket: family-offline-theorem.
- [ ] **P2 — Gonek verdict + Mertens 4–5 digits.** On part2b/3b landing:
  5-gate check, merge 90,001-zero table, J₋₁ secondary-term fits
  (c₁ + c₂·logT/T etc.), Mertens constant final digits. First-ever numerics,
  completed properly. Unblocks constants-paper HITL. Lane: frontier
  (adjudication is judgment-dense; pre-registered in gonek-verdict-call).
- [ ] **P3 — Mechanism: U₄ intertwiner construction (M1 next step).** The
  operator-level q=4 ζ(2s) factorization theorem (Mayer analog) would be a
  genuinely new theorem and the "why" of the dichotomy. Lane: Opus agent
  (derivation draft) + Aristotle for finite algebra joints. Ticket:
  mechanism-m1-factorization.
- [ ] **P4 — Second certified G₅ pin (distinct real part).** Upgrades the
  no-vertical-line corollary from "not the ½-line" to "no single vertical
  line" — a visibly stronger statement for the paper. Reuses R3b machinery at
  a second pin (0.24303 candidate from V1). Lane: Kaggle (cert compute) after
  P1 template prep; frontier gate. NEW ticket: second-g5-pin.
- [ ] **P5 — T1 GAP-16: re-derive the verified explicit-formula import under
  the Riesz window.** Completes T1 post-A2. Parts Aristotle-able. Lane:
  frontier statement design → Aristotle. Ticket: sample-complexity-t1.
- [ ] **P6 — Flagship paper assembly (drafting only; dissemination stays
  owner-gated).** Statement + proof-chain + dependency preamble + MMS q>5
  footnote + constants table into a submission-shaped TeX draft. Lane: Kimi
  K3 after P1 launch. NEW ticket: flagship-paper-draft.
- [ ] **P7 — d3-lean-reverify (Aristotle)** — open prerequisite for the D3
  HITL decision; mechanical. Lane: builder agent + aristotle CLI.

## Standing gates
- Every new claim: receipts + adversarial pass before "declared".
- No dissemination without owner word (Koyama v4 send pending).
- Ledger updated same turn as any status change.

## Overnight run 2026-08-15 (owner AFK; frontier responsible for significant progress)

Closed today: P5 GAP-16 (Riesz import, 12/N, Aristotle v21); M1d (U₄ via
Γ₀(2)◁Γ₀⁺(2); ζ(2s) = scattering determinant, 4/4 predictions); M1e (φ₆
CONFIRMED 4/4 — two-surface family pattern); Koyama v5 FINAL (7 fixes).

Overnight lanes (all launched this turn):
- [ ] **O1 — φ₄/φ₆ Eisenstein first-principles derivation (G5 obligation).**
  Opus 5. The step that turns the scattering mechanism into a theorem.
  Target: lane_g/M1F_EISENSTEIN_DERIVATION.md with proof-or-obligations.
- [ ] **O2 — Certified winding at the 8 predicted resonances.** luna (codex).
  Upgrade M1d/M1e midpoint numerics to rigorous Arb certificates.
  Target: lane_g/M1G_PREDICTION_WINDING_CERTS.md + receipts.
- [ ] **O3 — Flagship paper TeX draft (P6).** Kimi K3 #2 (if bridge allows
  concurrent; else queued behind q=7). Dissemination stays HITL.
- [ ] **O4 — Aristotle v22: M1d's 5 ARISTOTLE-ABLE obligations.** builder
  prepares stubs + dispatches; poll with v21.
- [ ] **O5 — 30m poll loop.** Kimi/Aristotle/Kaggle statuses; harvest part2b/3b
  on landing → 5-gate → merge 90,001 zeros → Gonek verdict + Mertens digits
  (P2, frontier); q=7 cert execution on Kimi report (P1); second G_5 pin (P4)
  after.
Standing: receipts before claims; ledger same turn; no dissemination.

## Q=7 certification pilot lane — 2026-08-15

- [x] Inspect the named q=5 scripts/receipts and bind the minimal q=7 path.
- [x] Measure q=7 float rho-star and the Arb endpoint finite-column bound; stop because `B >= 30`.
- [x] Gate-skipped: do not add `--arcs i:j` or seam logic after the mandatory stop.
- [x] Gate-skipped: do not run a local pilot after the mandatory stop.
- [x] Write `lane_f/F7_PILOT_REPORT.md`, append `EXECUTION_LOG.md`, and verify every requested field.

Routing receipt: artifacts are the q=7 measurement receipts, the named R3b runner,
the pilot report, and one execution-log entry. Scope is SPEC'D/GATED by
`F7_CERT_PLAN.md`; authority is the owner prompt; route/owner is this luna lane;
no delegation because the ordered gate and shared runner edits are coupled.

### Review/results

Stage 1 returned BLOCKED at provisional `N=224`: the finite-column endpoint
bound alone is approximately `1.145e9`, so the full endpoint bound cannot meet
the plan's `B approximately 30` gate. Later stages were intentionally not run.

## RATE effectivization closure — 2026-08-19

Goal: close, refute, or precisely delimit the four ordered RATE lanes in the
owner's `plans/wayfinder/rh-goals/CODEX_ORCHESTRATOR_PROMPT.md`, with every
status change appended to the source ledger and `plans/wayfinder/rh-goals/MAP.md`.

Routing receipt (before mutation): task-defining artifacts read are `start.md`,
`token-economy.yaml`, `plans/wayfinder/rh-goals/CODEX_ORCHESTRATOR_PROMPT.md`,
`plans/wayfinder/rh-goals/MAP.md`, `ATOM_MOMENT_BRIDGE_SOL.md`, and
`RATE_A_REFEREE.md`. Governing authority is the owner prompt plus root/project
`AGENTS.md`. The AM referee, activation closure, constant-chain autopsy, and v30
formalization drafts are each SPEC'D by named targets and GATED by source-hash,
exact-arithmetic, replay, syntax/build, and cold-review checks. Each expected
deliverable exceeds 30 lines, so execution is delegated; the frontier
orchestrator owns ordering, hard mathematical judgment, ledger synthesis, and
commits. Writers use isolated worktrees or return a read-only packet for the
orchestrator to materialize. No worker may change git state. Untracked caches,
`.worktrees/`, `.lake`, tarballs, and `graphify-out/` are out of scope.

- [x] AM: relaunch a cold adversarial referee because `AM_REFEREE.md` is absent;
  attack convention match, marked-code injectivity/decoder, constants, and a
  fresh exact numerical replay. A second cold context checks the referee before
  any RATE-A promotion.
- [x] If and only if AM is confirmed, append (never rewrite) the RATE-A promotion
  block and same-turn MAP entry; verify the balanced/matched boundary scope,
  exponent `6/5`, onset `q_RATE = 12`, unchanged advertised constant, and open
  machine-certification caveat.
- [x] Activation: derive `R5_ACTIVATION_CLOSURE_SOL.md` from the unrounded
  corrected bases, strict-upward thresholds, whole-tail monotonicity, finite
  base-block obligation, and the explicit constants. Return either an explicit
  `q0 = max{...}` or `UNDEFINED` with the exact missing premise. Referee every
  proof claim in a separate file before banking.
- [x] Constant reduction: derive `CR_REDUCTION_SOL.md` by reconstructing every
  factor in `C_R`, ranking losses by log contribution, and distinguishing
  proved substitutions from counterfactual opportunities. Referee any claimed
  improved constant before changing a theorem ledger.
- [x] Formalization: draft v30 `(FW)` and AM marked-coding/decoder targets using
  v29's dispatch pattern, include the escape hatch, syntax-precheck in the v26
  cache, submit only if the dispatch contract is complete, then harvest and
  independently rebuild if a result lands.
- [x] After each returned worker: run the lane git guard, compare against the
  dispatch criteria, record the result in the worker ledger, and quarantine any
  unsupported claim.
- [x] End with fresh tests/receipts, explicit-path commits using recent message
  style, one dated MAP session summary, and a handoff naming every running/open
  item. Do not push unless the tree is clean and the quoted gates pass.

```loop
name: rate-effectivization-closure
topology: closed inner fleet
generator: isolated writer per AM, activation, constant-reduction, and formalization deliverable
verifier: fresh blind cold reviewer plus orchestrator exact-command gate
gate: python3 skills/loop-engineering/tools/loop_lint.py tasks/todo.md && git diff --check && rg -n 'VERDICT|CONJECTURAL|CONFIRMED|REFUTED|UNDEFINED' research_notes/rh_goals_2026-08-14/lane_g plans/wayfinder/rh-goals/MAP.md
stop: each ordered lane is verified, explicitly blocked, or not started because an upstream refutation halted consumers; MAP and commits match the verdicts
budget: max_iterations=2 per lane
quorum: independent referee verdict plus orchestrator receipt audit
anchor_files: plans/wayfinder/rh-goals/CODEX_ORCHESTRATOR_PROMPT.md, tasks/todo.md, plans/wayfinder/rh-goals/MAP.md
state_store: tasks/todo.md worker ledger and append-only MAP entries
recall: read the current task section and MAP tail before each lane
writeback: record worker outcome, verifier verdict, commands, failures, and next action after each lane
state_concurrency: worktree_isolated
output_actions: commit max 8; default deny every other external action
on_error: transient tool failure retries once; malformed proof output returns as evidence; auth or configuration causes interrupt; unexpected failure causes halt and surface
verifier_blind: true
```

| worker | task | status | result captured | wiki/log | close reason |
|---|---|---|---|---|---|
| luna writer, quarantined then repaired | AM adversarial referee | done | `CONFIRMED`, orphaned diagnostics removed | MAP banked | exact-file verifier PASS |
| blind checker + fresh final verifier | AM referee cold check | done | decoder reconstruction `CONFIRMED`; report replay PASS | MAP banked | no open repair |
| activation writer | A0 closure note | done | exact side/A0 thresholds; mixed-domain prompt corrected | MAP banked | separate referee required |
| activation cold referee | activation proof/status audit | done | `CONFIRMED` paper-level analytic tail | MAP banked | finite block remains open |
| C_R constant autopsy | done | done | primary/fallback ceilings and strict A0 candidates isolated | MAP banked | first referee required repair |
| C_R cold referee | done | done | arithmetic `CONFIRMED`; ranked-loss documentation `GAPS` | repair appended | re-referee required |
| C_R repair re-referee | done | done | ranked autopsy `CONFIRMED`; primary `C_R'` banked | MAP banked | machine/full-program gates remain open |
| v30 writer + Aristotle | typed FW/AM dispatch | done | project/task completed; exact result harvested | result committed | cold referee required |
| v30 cold referee | returned Lean scope/build audit | done | finite wire-format targets `CONFIRMED`; paper/analytic scope `GAPS` | MAP banked | exact v26 rebuild and signatures pass |

### Review/results

AM lane closed from fresh commands and two cold judgments. `AM_REFEREE.md` was
quarantined after its writer used the main tree and omitted commands for several
draft-only diagnostics. Those claims were removed; the scalar and `y<=100`
commands replayed exactly, the orphaned-count search was empty, and the final
verifier returned `PASS`. The append-only theorem and MAP promotion now limits
RATE-A to the balanced/matched paper-level boundary result; all machine and
non-RATE activation gates remain open.

Activation lane closed after an exact-domain repair and a separate cold
referee. The analytic A0 tail now has a sourced strict max and a monotone fixed
envelope. The older full all-q R5 objective remains `OPEN / UNDEFINED` because
the true scalar finite-block evaluator/certificates do not exist in the current
artifact set; no determinant surrogate or timing run was promoted.

The constant-reduction lane required two referee passes. The first confirmed
the direct `2^62+1` substitution and exact Arb ceilings but rejected the
solution's missing ranked autopsy. An append-only repair identified `C_4` as
the only banked reduction, kept `F`/`S` diagnostic, showed wrap negligible at
the new scale, and declined speculative `M_0` headroom. The second cold report
confirmed that repair; the sharper alternative RATE-A ceiling and selected
conditional A0 cutoff are now banked, while finite/machine/full-program gates
remain open.

V30 was submitted and harvested rather than left as a draft. The exact
returned `RateCoreV.lean` rebuilds against the v26 cache with no `sorry` or
declared `axiom`, and a cold referee matched all requested signatures. The
promotion is intentionally narrow: executable local `MarkedCode` serialization
and finite algebra are machine-verified, while the paper source-table map,
coverage, canonical/Ford inputs, analytic `(FW)`/`(AM)`, and RATE-A machine
certificate remain `GAPS / CONJECTURAL` at Lean level.

## Unconditional RATE proof push — 2026-08-19

Goal: make a new, referee-audited advance on the smallest load-bearing gate
between the paper-level balanced/matched RATE-A theorem and an unconditional
all-`q` law.  Kaggle and Aristotle are permitted only where they can return a
durable exact certificate or a rebuildable formal artifact; exploratory output
is never promoted to proof.

Routing receipt (before mutation): the task-defining artifacts are `start.md`,
`tasks/lessons.md`, the 2026-08-19 RATE closure section above,
`plans/wayfinder/rh-goals/MAP.md`, `R5_ACTIVATION_CLOSURE_SOL.md`,
`R5_ASSEMBLY_EXECUTION_SOL.md`, `DH2_RENEWAL_PROOF_SOL.md`, and
`HOLOMORPHY_GATE_SOL.md`.  Authority is the owner's new request plus the prior
RATE house rules.  Diagnosis is not yet SPEC'D, so the frontier orchestrator
owns the dependency judgment.  Three bounded read-only scouts gather exact
file/command evidence: finite-certificate inventory, determinant/continuation
theory inventory, and Aristotle-ready formal targets.  No scout may mutate the
tree or git state.  Once a target is selected, any expected 30+ line
construction is delegated with an exact gate; every proof claim gets a separate
cold referee before a MAP status change.  Preserved `.worktrees/`, caches,
tarballs, and `graphify-out/` remain out of scope.

- [ ] Reconstruct the current dependency graph and state the exact first open
  implication needed for an unconditional full law.
- [ ] Audit whether any existing scalar-`phi_q` evaluator plus Arb/interval
  machinery can produce a finite zero-minus-pole certificate; quantify the
  feasible `q` range and the exact missing input.
- [ ] Audit the current Fredholm/scattering determinant identification and
  continuation notes, including all dated errata, and isolate the smallest
  theorem-strength repair that would bypass the astronomical finite block.
- [ ] Select one proof-producing construction lane; if it emits a proof claim,
  run a fresh adversarial referee in a separate `*_REFEREE.md`.
- [ ] Dispatch Aristotle only for a load-bearing formal statement with an exact
  source-to-type map, then harvest and independently rebuild before banking.
- [ ] Dispatch Kaggle only for a bounded exact computation with a local replay
  checker and a harvestable manifest; label all search-only output
  `CONJECTURAL` / `NOT PROOF`.
- [ ] Append dated MAP entries for every status change, run whole-lane receipts,
  commit explicit scoped paths, and leave a one-paragraph running/open handoff.

```loop
name: unconditional-rate-proof-push
topology: closed inner fleet
generator: selected proof or exact-certificate builder after three read-only evidence scouts
verifier: separate cold adversarial referee plus orchestrator command replay
gate: python3 skills/loop-engineering/tools/loop_lint.py tasks/todo.md && git diff --check && rg -n 'PROOF|CONJECTURAL|GAP|OPEN|REFUT' research_notes/rh_goals_2026-08-14/lane_g plans/wayfinder/rh-goals/MAP.md
stop: one load-bearing implication is referee-confirmed or honestly refuted, every attempted computational/formal task is harvested or explicitly open, and MAP matches the evidence
budget: max_iterations=2 per construction/referee pair
quorum: independent referee verdict plus exact local replay or independent Lean rebuild
anchor_files: tasks/todo.md, plans/wayfinder/rh-goals/MAP.md, research_notes/rh_goals_2026-08-14/lane_g/R5_ACTIVATION_CLOSURE_SOL.md
state_store: tasks/todo.md worker ledger and append-only MAP entries
recall: reread this section and the MAP tail before every status change
writeback: record scout evidence, builder artifact, referee verdict, commands, failures, and next action
state_concurrency: single_writer
output_actions: commit scoped proof artifacts and ledgers; default deny push and every other external action except explicitly proof-producing Kaggle/Aristotle tasks
on_error: retry one transient transport failure; preserve mathematical counterexamples; stop consumers on a refutation; surface auth or missing-authority blockers
verifier_blind: true
```

| worker | task | status | result captured | wiki/log | close reason |
|---|---|---|---|---|---|
| finite-certificate scout | scalar evaluator and Kaggle feasibility | complete-with-concerns | true-scalar certified range is empty; current conditional cutoff forces 97418971860452658435229799565334786142 non-arithmetic targets | no wiki write | read-only audit harvested; lane guard PASS |
| determinant-theory scout | continuation/determinant repair inventory | complete-with-concerns | q=5 v3.1 chain is banked; general-q cancellation-safe scalar evaluator is OPEN | no wiki write | cold read-only report harvested; q=8 follow-up requested |
| formalization scout | v31 load-bearing Aristotle target | complete-with-concerns | selected full paper one/two-mark source encoder and inverse decoder; v30 local wire format rejected as insufficient | no wiki write | isolated v31 builder running; no submission yet |

### Review/results

- Concurrency-integrity note: the pre-scout lane-guard snapshot recorded
  `wiki/L1_index.md` at blob
  `fba29a36011143dd671c200bbfe78a3d160d19eb`; a later read-path re-index left
  the file equal to `HEAD`.  `git cat-file -p` recovered the exact snapshot
  blob and `git log --all --find-object=...` showed it is historical generated
  index content, not unique user work.  No restoration is warranted; resnapshot
  before any writer lane.
- Determinant scout verdict: the `q=5` v3.1
  winding-to-resonance chain remains banked at its local stated scope.  The
  first general-`q` scalar-computation theorem, `(SCAT-EVAL_q)`, is
  **CONJECTURAL / OPEN**: it must give a cancellation-safe determinant quotient
  for `phi_q`, compatible continuation/normalization, and explicit determinant
  plus derivative tails.  This is neither Aristotle-ready nor Kaggle-ready;
  downstream finite contour jobs become computationally meaningful only after
  that paper theorem.
- Finite-certificate scout verdict: the largest certified full-`H_0`
  true-scalar `phi_q` range is empty.  Replaying the reduced conditional onset
  gave `q_transport=97418971860452658435229799565334786148`, hence
  `97418971860452658435229799565334786142` non-arithmetic law targets below it
  (the final full-program range remains **UNDEFINED**).  Existing Kaggle
  architecture exactly replays transfer-determinant certificates, but no
  theorem-valid scalar evaluator exists, so a new run would remain **NOT
  EVIDENCE** for the finite scalar gate.  A covering theorem or much smaller
  onset is necessary in addition to `(SCAT-EVAL_q)`.
- Formalization scout verdict: the first non-duplicate Aristotle candidate is
  the actual TWOMARK paper-source encoder/decoder, not v30's local three-status
  `MarkedCode` and not the already-formalized generic `K_s` lattice.  A v31
  source must define the paper atomization and every one/two-mark branch
  executably, use four cut actions, and encode only the bounded paper record.
  The proposed targets remain **CONJECTURAL** until a local syntax gate,
  Aristotle return, independent rebuild, and cold branch-coverage referee all
  succeed.  A builder is running in the isolated
  `codex/law-v31-source-decoder-20260819` worktree; no submission has occurred.
- q=8 follow-up verdict: **REFUTATION CLAIM, PENDING COLD REFEREE**.  The banked
  `CLOSED_CONTOUR_CERTIFIED` interpretation is invalid because the routine
  encloses segment endpoints only and inflates by a dimension-tail routine
  explicitly documented as heuristic/not uniform.  Append-only correction
  blocks now stop q=8 promotion and suspend q=9..12's ported R3B labels as **AT
  RISK**.  The exact same-byte Kaggle outputs remain evidence only for sampled
  finite-section polygon winding.  q=5, the independent q=7 chain, RATE-A, and
  the qualitative Selberg–Hejhal tail are outside the blast radius.

### Scope correction — 2026-08-19

The live MAP defines **LAW** as: every non-arithmetic Hecke group `G_q` has a
Selberg-zeta zero/scattering resonance strictly off the critical line.
Accordingly, the section title's initial RATE-only reading was too narrow.
`(RATE)` remains a load-bearing effective-tail input, but the destination is
the full LAW: an effective uniform tail plus a certified finite base.  The
three already-dispatched RATE scouts are retained as evidence lanes; their
results will be judged against this broader dependency graph.

Fresh artifact inventory also changes the finite-base premise: Kaggle work is
already harvested for `q = 8, 9, 10, 11, 12`.  `F8_CERT_PLAN.md` and
`F9_F12_BASE_EXTENSION.md` certify closed-contour determinant boxes, but their
own scope banners explicitly refuse assembled off-line theorems.  The next
construction candidate is therefore not another Kaggle run: close and referee
the missing determinant-identification / `K_s` / source-factorization links,
starting with `q = 8`, while preserving explicit gaps for `q = 9..12` where
the TB/enlarged-disc layer is absent.

Final verification reran `./te doctor`, the loop linter, all three arithmetic
receipt families, the exact v30 Lean rebuild, forbidden-declaration and axiom
audits, nine signature comparisons, Aristotle completion status, diff/secret/
artifact checks, and tracked-tree status. All functional/status gates passed at
their stated scopes. The local loop's `commit max 8` planning budget was
exceeded by the deliberately granular proof/referee/ledger commits; this is a
recorded orchestration-budget deviation, not a mathematical or artifact gate.
History was not rewritten. No push occurred because the preserved pre-existing
untracked inventory keeps the literal tree non-clean.

## Unconditional LAW proof push — referee harvest 2026-08-19

- [x] Reconstructed the actual LAW dependency and separated RATE-A, the
  true-scalar finite gate, per-q determinant instances, and the qualitative
  Selberg–Hejhal tail.
- [x] Completed the finite-evaluator, determinant-theory, and Aristotle-target
  audits with read-only lane-guard PASS receipts.
- [x] Stopped and corrected a banked false target: the q=8 continuous-contour
  certificate interpretation is referee-confirmed false, and exact driver
  comparison extends the same refutation to q=9..12.  Same-byte Kaggle outputs
  are retained only as sampled finite-section evidence.
- [x] Ran q=7 adversarial round 2.  Numerical Hilbert-side gates replay, but
  the q=7 Hilbert-to-MMS Clause-1 operator binding is OPEN; verdict **GAPS / NOT
  REFUTED**, so no declaration.
- [x] Finish the v31 FALSE-AS-STATED Lean repair and cold-referee its explicit
  counterexamples.  `V31_REFEREE.md` returned **REFUTATION CONFIRMED**; no
  non-false load-bearing paper-source target survived, so Aristotle submission
  was correctly withheld.
- [x] Prove the q=7/q-generic 19-block operator-binding/common-continuation
  theorem, bank MMS primary source text, and re-referee before any q=7 upgrade.
- [ ] Rebuild q=8 from a theorem-valid evaluator/exact box/R2 tail/continuous
  R3b/E1/`K_s` chain before any new Kaggle replay.

| worker | task | status | result captured | wiki/log | close reason |
|---|---|---|---|---|---|
| q=8 refutation referee | endpoint/tail countermodels + q=9..12 blast radius | complete-with-concerns | `REFUTATION CONFIRMED`; local q=8 Kaggle log absent, embedded hashes/receipts checked | MAP + lane correction blocks | banked in `F8_R3B_REFUTATION_REFEREE.md` |
| q=7 referee round 2 | cold full-chain review | complete-with-concerns | `GAPS / NOT REFUTED`; first gap Link 4b operator binding | MAP + assembly correction block | banked in `THEOREM_G7_OFFLINE_REFEREE2.md` |
| v31 builder + cold referee | prove false-target negations, remove impossible submission, independently replay | complete-with-concerns | `REFUTATION CONFIRMED`; valid equal-kind mark collision plus decoder-slice defect | MAP + dispatch correction block | exact paper encoder/decoder remains OPEN / CONJECTURAL; no Aristotle submission |

Session handoff remains open for the q7 Clause-1 operator-binding proof/referee
pair.  No q=8..12 Kaggle job and no v31 Aristotle job is authorized from the
current artifacts.

### Q7 closure review/results — 2026-08-19

- The q=7-specific 19-block MMS operator binding was written, cold-refereed
  `GAPS / NOT REFUTED`, repaired append-only with the full centered-tail
  estimate and determinant citations, and independently re-refereed
  **CONFIRMED**.
- The exact MMS v2 source/version/theorem numbering was fetched, hash-matched,
  and banked without adding the third-party PDF to git.
- A third cold assembly referee returned
  **CONFIRMED_AT_EXACT_Q7_SELBURG_ZERO_AND_STANDARD_RESONANCE_SCOPE**.  The
  q=7 paper theorem is now banked; the full LAW remains open.
- Fresh exact TB replay used the receipt's `K_start=12` and reproduced
  `rho_star=[0.763212029206899202166157 +/- 1.41e-25]` and
  `PASS_RHO_LT_0.80`.  A diagnostic with `K_start=8` was explicitly rejected
  as a parameter mismatch.
- Kaggle was not relaunched because the certified q=7 chunks already matched
  the pinned local bytes.  Aristotle was not submitted because the candidate
  v31 decoder targets were machine-refuted before submission; neither action
  would have closed the analytic Link 4b gap.

Updated handoff: q=7 is referee-confirmed at paper level.  The next
load-bearing full-LAW work is a theorem-valid q=8 replacement chain (continuous
contour enclosure, rigorous tail, E1, operator binding, and `K_s` gate) or an
effective tail onset small enough to reduce the finite base.  q8–12's current
ported contour claims remain refuted, not pending promotion.

## Full unconditional LAW closure campaign — 2026-08-19

Goal: prove at paper level, without conjectural hypotheses, that every
non-arithmetic Hecke group `G_q` has a Selberg-zeta zero/scattering resonance
strictly off the critical line.  Pursue both admissible closure routes in
parallel and preserve the existing q8–12 refutation until a genuinely different
theorem-valid construction passes a cold referee.

- [x] Set the persistent goal and snapshot branch `441fca6`, current ledger,
  preserved untracked inventory, and existing worktrees.
- [x] Dispatch isolated Route-A, Route-B, and `(SCAT-EVAL_q)` construction lanes
  with one primary deliverable each and explicit no-push/referee gates.
- [x] Harvest and cold-judge `(SCAT-EVAL_q)`: require an exact determinant
  quotient, compatible continuation/normalization, and explicit determinant
  plus derivative tails; referee verdict **GAPS / NOT REFUTED**.  The first
  direct-scalar gap is the Teo--Hejhal normalization/divisor bridge; for the
  q>=8 zeta bypass it is code-to-MMS operator/sector identification, followed
  by the determinant and derivative tails.
- [ ] Harvest and cold-judge q=8: require exact even-q operator binding, proven
  R2 tail, continuous (not endpoint-only) contour enclosure, E1, `K_s`, and
  factorization before any Selberg-zero status.
  The first adaptive `N=32` Taylor run was terminated after its own trace
  showed accepted subarcs with `lower=0`; its subdivision predicate checked
  Neumann/Jacobi bounds but did not require zero exclusion.  Repair must reject
  `lower <=` the full determinant-tail allowance, preferably in the exact
  one-component Schur reduction, before a rerun or Kaggle dispatch.
- [ ] Harvest and cold-judge the effective-tail/covering route: require either
  an explicit manageable all-gates onset or a theorem that covers the finite
  block without per-q enumeration; constant-only sensitivity is not closure.
- [ ] Launch Kaggle only after a theorem-valid local evaluator/checker exists;
  launch Aristotle only after a non-false load-bearing statement passes local
  syntax/falsification gates.  Harvest and independently verify every launch.
- [ ] For every proof claim, create a separate cold `*_REFEREE.md`; repair and
  re-referee gaps, and stop downstream consumers on any confirmed refutation.
- [ ] Append dated MAP status blocks, run exact receipts and whole-tree gates,
  commit scoped paths in recent-log style, and continue until the LAW is proved
  or the active-goal blocker threshold is genuinely met.

| lane | isolated branch/worktree | status | required output |
|---|---|---|---|
| q8 q-generic chain | `codex/law-q8-generic-20260819` / `.worktrees/law-q8-generic-20260819` | running | `lane_f/Q8_GENERIC_CERTIFICATION_SOL.md` + exact receipts |
| effective tail/cover | `codex/law-effective-tail-20260819` / `.worktrees/law-effective-tail-20260819` | conditional endpoint candidate at `1059d6a`; cold referee running | `lane_g/LAW_EFFECTIVE_TAIL_COVER_SOL.md` + exact receipts |
| scalar evaluator | `codex/law-scat-eval-20260819` / `.worktrees/law-scat-eval-20260819` | **GAPS / NOT REFUTED; cold-refereed** | `lane_g/SCAT_EVAL_Q_SOL.md` + `SCAT_EVAL_Q_REFEREE.md` |
| symmetric effective tail | `codex/law-symmetric-tail-20260819` / `.worktrees/law-symmetric-tail-20260819` | refutation candidate; cold referee pending | scalar two-wall FE pincer fails; two-channel replacement remains conjectural |

- [ ] Test the exact block-Schur reduction suggested by the MMS sparsity:
  even `q` should reduce the growing `kappa x kappa` block companion to one
  Hardy-space component, and odd `q` to two terminal components.  First gate
  is exact finite-matrix determinant equality at `q=7,8,9,10`; second gate is
  a source-valid Fredholm-determinant factorization by triangular nuclear
  elimination; only then may it support a `q`-uniform contour/tail theorem.
  The route is **CONJECTURAL** until both gates and a cold referee pass.
  The first Arb diagnostic now passes at even `q=8,10` and odd `q=7,9`;
  implementation provenance, theorem-level finite algebra, and the infinite
  Fredholm gate remain open.

- [ ] Cold-scan primary resonance-counting theorems for a general escape:
  require a theorem that actually forces a **nonreal** scattering pole off
  `Re(s)=1/2` for every cofinite one-cusp orbifold, not merely a combined
  eigenvalue/resonance Weyl law or real trivial poles.  Verify elliptic-point
  and Hecke-orbifold hypotheses before treating it as a LAW consumer.

- [ ] Cold-referee the scalar symmetric-tail refutation.  The theta limit is
  a two-cusp scattering matrix; its `(infinity,infinity)` entry has a nonzero
  reciprocal defect, so the finite one-cusp functional equation makes the
  reflected left error order one rather than `O(E_3(q))`.  Only a genuinely
  new two-channel/full-matrix degeneration theorem could correct this route.

- [x] Test the generalized-Dirichlet right-half-plane-zero bypass against
  Saias--Weingartner, Booker--Thorne, and Ramachandra.  None applies to the
  generalized algebraic Hecke-modulus spectrum; positive spacing already
  fails for explicit q=5 word families.  The bypass remains abstractly open,
  with the exact missing theorem recorded as a Hecke-scattering
  right-half-plane zero lemma.
- [x] Recover and terminate the orphaned 100%-CPU Python process after its
  immutable rollout receipt identified it as the completed Route-B geometry
  scan (not a q8 certification run); no output artifact was lost.

Verification gate:

```text
python3 skills/loop-engineering/tools/loop_lint.py tasks/todo.md
git diff --check
./te doctor
rg -n 'PROOF|CONJECTURAL|GAP|OPEN|REFUT|CONFIRMED' \
  research_notes/rh_goals_2026-08-14/lane_f \
  research_notes/rh_goals_2026-08-14/lane_g \
  plans/wayfinder/rh-goals/MAP.md
```

### Schur referee harvest and next exact gate — 2026-08-19

- [x] Bank the finite even/odd Schur identities only after a separate cold
  referee reruns both parity families and checks the source orientation.
- [x] Replace the conditional Hilbert Fredholm claim's undefined similarity by
  exact trace-class left/right unitriangular factors; use Simon Theorem 3.8 for
  multiplication and retain common MMS continuation as an explicit gap.
- [ ] Complete the q=8 Schur-contour construction with a strict finite Taylor
  zero-exclusion test, a transformed trace-norm tail in compatible Hilbert
  norms, and a Woodbury resolvent homotopy; then cold-referee it before Kaggle.
- [ ] If q=8 succeeds, derive the direct terminal induced operator
  `C_h=sum_j A_h...A_{j+1}B_j` on one non-collapsing terminal Hardy disc.  The
  required theorem is an exact composite-branch evaluator plus q-uniform disc
  containment and a proven tail in both Taylor degree and eliminated-chain
  length.  This is the preferred q-generic continuation of Route A; it is
  **CONJECTURAL** until constructed and cold-refereed.
- [ ] Continue Route B independently: cold-referee the endpoint p=3 theorem,
  quantify whether a contradiction-branch Phragmen--Lindelof bound can replace
  the coarse `K_+<125`, and reject it if it still leaves a non-certifiable
  finite onset.

Root replay status receipt:

```text
q=7,8,9,10 full checker: OVERALL_STATUS=PASS failures=0
q=5,6,11,12 opposite-sector edge checker: OVERALL_STATUS=PASS failures=0
cold ledger: FINITE ALGEBRA CONFIRMED; conditional Hilbert proposition
CONFIRMED; abstract Banach wording GAPS / NOT REFUTED; downstream LAW OPEN.
```

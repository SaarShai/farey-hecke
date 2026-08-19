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
- [ ] Constant reduction: derive `CR_REDUCTION_SOL.md` by reconstructing every
  factor in `C_R`, ranking losses by log contribution, and distinguishing
  proved substitutions from counterfactual opportunities. Referee any claimed
  improved constant before changing a theorem ledger.
- [ ] Formalization: draft v30 `(FW)` and AM marked-coding/decoder targets using
  v29's dispatch pattern, include the escape hatch, syntax-precheck in the v26
  cache, submit only if the dispatch contract is complete, then harvest and
  independently rebuild if a result lands.
- [ ] After each returned worker: run the lane git guard, compare against the
  dispatch criteria, record the result in the worker ledger, and quarantine any
  unsupported claim.
- [ ] End with fresh tests/receipts, explicit-path commits using recent message
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
| C_R constant autopsy | evidence complete | done | dominant `C_4` loss and Arb candidates isolated | deliverable pending | no status change yet |
| v30 writer | typed FW/AM dispatch | running externally | syntax exit 0; Aristotle project `97b16c1b-653d-42b9-a5da-4ed765a8eb88` | harvest pending | task at 3% |

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

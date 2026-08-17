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

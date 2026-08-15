# RH goals scouting — 2026-08-14

- [x] Read anthropic.com/research/riemann-zeta (41.6%→67.2% critical-line proportion; fan-out/falsify/verify/Lean methodology)
- [x] Fan out 5 codex gpt-5.6-luna xhigh search agents over repo partitions (research_notes / wiki+facts / engine+code / equispaced-primes / projects)
- [x] Self-read core zeta-adjacent notes (G_5 resonances, prime-Farey verdicts, Koyama)
- [x] Locate + audit the zero-detection method (Mertens spectroscope / MUSIC tomography — tool killed, theory residue live)
- [x] Synthesize inventory: everything zeta/RH-related, status-tagged
- [x] Cross-check goal candidates against DO-NOT-RE-CHASE list
- [x] Define 3 goals for real (modest) RH-adjacent progress
- [x] Draft 3 goal maps (wayfinder skill absent — markdown drafts)

## Review

Output: research_notes/rh_goals_2026-08-14/ — 00_SYNTHESIS.md + GOAL{1,2,3}_MAP.md.
- Goal 1: sample-complexity theory of zero detection from prime data (unscooped residue of the killed spectroscopy tool).
- Goal 2: certified resonance atlas + arithmetic-rigidity law (absorbs Pick B; requires restoring Aletheia stack from b973d56 — not on HEAD/main).
- Goal 3: unconditional Farey–Mertens structure (DiscrepancyStep Kloosterman probe with pre-registered NO-GO gate; ζ′(ρ) zero-sum constant conflict resolution; priority note).
Key repo facts surfaced: engine/ empty on HEAD (stack on codex/declusteraudit* branches only); spectroscope README claims unaudited (artifacts missing); log.md 2/π² conjecture conflicts with mimo E5 probe.

## Lane D — fresh Lean re-verification (2026-08-14)

- [x] Inspect Lake targets, theorem names, cache configuration, and existing axiom-check files.
- [x] Sequentially build the Farey Bridge target and capture exit code, wall time, and warnings.
- [x] Build the Bridge axiom-check target and capture `#print axioms` output.
- [x] Sequentially build the Aristotle Prony target and capture exit code, wall time, and warnings.
- [x] Capture `#print axioms prony_power_sum_uniqueness` output.
- [x] Write `research_notes/rh_goals_2026-08-14/lane_d/LEAN_REVERIFY.md` with verbatim commands/output and per-item verdicts.

### Lane D review/results

Output: `research_notes/rh_goals_2026-08-14/lane_d/LEAN_REVERIFY.md`.
Both requested items are VERIFIED-FRESH. Aristotle cache cloning failed with git exit 128, then the exact local v4.28.0 package set was reused inside `.lake/packages`; the target rebuilt with exit 0 and the requested axiom list.

## Lane G — family prep constants (2026-08-14)

- [x] Read the prescribed K_s and disc-optimization derivations; lock odd/even formulas and q=7/q=8 block structures.
- [x] Implement the light family-prep calculator under the restore worktree's `code/family_prep/`.
- [x] Run and independently verify K_s constants, zero lattices, q=7/q=8 disc optima, and tail N.
- [x] Write `research_notes/rh_goals_2026-08-14/lane_g/FAMILY_PREP_CONSTANTS.md` (manifest first) and its receipt JSON.

### Lane G review/results

Completed. The manifest covers q=5..12; q=7 and q=8 use the requested float disc optimization; q=7..12 all pass the analytic K_s lattice-clear gate. Independent direct read-back reproduces q=7 `rho*=0.782263813617748`, `N=66` and q=8 `rho*=0.820778458003607`, `N=82`.

Outputs:

- `research_notes/rh_goals_2026-08-14/lane_g/FAMILY_PREP_CONSTANTS.md`
- `research_notes/rh_goals_2026-08-14/lane_g/FAMILY_PREP_CONSTANTS_RECEIPT.json`
- `.worktrees/aletheia-restore/code/family_prep/family_prep_constants.py`

## Lane G — repaired weight envelope certification, iteration 2 (2026-08-14)

- [x] Read the repaired L3′ chain and the V2 block-certification receipt; bind the exact eight G_5 boxes and T-c contour bounds.
- [x] Extend `code/tb_certify/` in the Aletheia restore worktree using the certified image-ratio and Hurwitz-closed tail machinery.
- [x] Compute finite `W^(>=1)`, conditioning-only `W^(0)`, repaired `F(W^(>=1), rho*=0.697802, N=48)`, margins, verdicts, and minimal certifying N for all eight boxes.
- [x] Write `research_notes/rh_goals_2026-08-14/lane_g/W_ENVELOPE_CERT_V2.md` and its receipt JSON; verify source/artifact/read-back and leave unrelated work untouched.

### Lane G iteration-2 review/results

Output: `research_notes/rh_goals_2026-08-14/lane_g/W_ENVELOPE_CERT_V2.md`, `W_ENVELOPE_CERT_V2_RECEIPT.json`, and the runner under the Aletheia restore worktree's `code/tb_certify/`.

Evidence: the prescribed 384-bit/512-arc run emitted 8 boxes × 11 blocks; an independent 896-check read-back passed row maxima, F, margins, minimal-N boundaries, V2 ratio bindings, and deep exponents. Per-pin T-c output was absent, so every margin uses the documented TC_PREP fallback `3.939054358191304e-6` and the receipt records that status. All eight N=48 verdicts are `NOT`; minimal certifying N is 567, 1287, 6466, 7360, 10072, 14054, 30232, and 53195 for pins 1–8.

## Lane G — flagship hybrid trace-norm certification (2026-08-14)

- [ ] Bind L3″, W^(≥1), rho*, exact flagship pin, geometry, and the active-process check.
- [ ] Add a separate certified Arb runner under `.worktrees/aletheia-restore/code/tc_rerun/` for the 192-point K=48 box.
- [ ] Execute N=128; if its certified margin fails, execute the prescribed N=160 fallback.
- [ ] Write the verdict-first report and machine-readable receipt with every contour-point T1, tail, F, determinant lower bound, winding result, and wall time.

### Lane G flagship review/results

Pending certified computation and independent read-back.

## Lane G — R2/R3 flagship certification repair relaunch (2026-08-14)

Routing receipt (recorded late, before certification-code mutation):

- task artifacts read: `ADVERSARIAL_REVIEW_V3_TBCHAIN.md`, the `TB_LEMMA_CHAIN.md` status banner, `TB_R1_HILBERT_RESTATEMENT.md`, `start.md`, and the prior partial-run recovery summary;
- state: SPEC'D by the user at the output/interface level, but surviving-code defects remain unresolved diagnosis; GATED by full Acb receipts, closed-cover checks, source hashes, exact tail formulas, and independent JSON/report read-back;
- expected change: more than 30 lines across two existing scripts; governing authority is the user prompt plus repository `AGENTS.md`/`start.md`;
- route: frontier/main owns unresolved mathematical diagnosis, patch integration, heavy compute, and final theorem verdict; two `luna_worker` lanes perform bounded read-only R2/R3 audits in parallel; any later mechanical implementation delegation will be sequential and non-overlapping;
- ownership: main thread is the only writer to the requested existing worktree and report paths;
- process note: the checklist below was the only premature mutation; cold review confirms it records scope only and touches no certification artifact.

Done means:

- [x] Reuse and finish the surviving `certify_r2_flagship.py` and `certify_r3_flagship.py`; no rewrite of their working core.
- [x] R2 certifies center-offset-included summed tail-family column bounds on complete Acb source-contour covers, with a finite certified all-k tail and `T_tail(128)` / `T_tail(160)`.
- [x] Every R2 column-family heavy loop appends recoverable checkpoint JSON while running; interruption still leaves a parseable partial receipt/report.
- [x] R3 covers the full pin-box boundary by 192 closed overlapping Acb segment balls, evaluates determinant enclosures valid on each segment, applies the requested R2-based inflation, and certifies or rejects winding without point-sampling substitution.
- [x] Every R3 arc batch appends recoverable checkpoint JSON while running; interruption still leaves a parseable partial receipt/report.
- [x] Run N=128 first and N=160 only as the prescribed fallback.
- [x] Write `research_notes/rh_goals_2026-08-14/lane_g/R2R3_FLAGSHIP_CERT.md` (verdict first), receipt JSON, and exact failure margins/provenance if any gate fails.
- [x] Independently read back all emitted artifacts, compare source hashes/constants/counts, and run targeted verification plus impact/security triage.

### Relaunch review/results

Completed with the narrow verdict **THEOREM-GRADE (closed-contour, corrected-envelope): NO at attempted N=128, 160**.

R2 production evidence: 384-bit Arb/Acb, 512 closed source-contour arcs, 11/11 block families, exact columns k=0..16, `B_total = 97.766647533940862...`, `T_tail(128) = 5.2715959382383759e-17`, and `T_tail(160) = 6.2678578810114396e-22`. The per-family checkpoint is complete; a fresh forced-termination drill left a parseable `RUNNING` receipt/report and 1/11 checkpoint families.

R3 production evidence: the code constructs the full 192-arc closed overlapping cover and attempted N=128 followed by N=160. Both attempts stop honestly at closed arc 0 because the finite determinant enclosure already contains zero: serialized zero-interior square depth is `0.1230000001378357...` at N=128 and `0.1010000001406297...` at N=160. Consequently requested-F and R1-F inflated boxes also contain zero and no closed-cover winding is claimed. The R1-valid prefactor is `exp(1+2 B_total) T_tail`; the requested `exp(1+T_finite+T_tail) T_tail` is retained as a non-theorem diagnostic because its `T_finite` omits retained-low-input/high-output rows.

Verification: both scripts compile; R2 smoke and R3 synthetic winding tests pass; fresh forced-termination drills write receipt/checkpoint/report for both runners. Independent 384-bit read-back re-summed all 384/480 serialized finite column norms, recomputed both prefactors, reparsed every determinant enclosure/depth, verified report regeneration and checkpoint equality, and matched every recorded SHA-256. Separate read-only adversarial verifier: PASS. Impact analysis is LOW but degraded (no graph); manual caller search finds R3 as the only consumer of R2 and both runners otherwise standalone. Lexical security triage found no introduced issue; exact-file review found only bounded atomic output writes and no network, shell, dynamic-evaluation, or credential sink.

Worker ledger:

- `r2_readonly_audit` (Pauli): accepted the bounded R2 audit/checkpoint implementation; main removed its temporary serialization tolerance and replaced it with receipt-safe read-back closure before the production run.
- `r3_readonly_audit` (Ampere): partial implementation only; interrupted after stalling, then cold-reviewed and completed by main. Not accepted as an independent completion result.
- `final_readonly_verifier`: accepted; independently replayed final R2/R3 artifacts and returned PASS with no false theorem claim or mismatch.

Outputs:

- `research_notes/rh_goals_2026-08-14/lane_g/R2R3_FLAGSHIP_CERT.md`
- `research_notes/rh_goals_2026-08-14/lane_g/R2R3_FLAGSHIP_CERT_RECEIPT.json`
- `research_notes/rh_goals_2026-08-14/lane_g/R2R3_FLAGSHIP_CHECKPOINT.json`
- `research_notes/rh_goals_2026-08-14/lane_g/R2_FLAGSHIP_ENVELOPE_RECEIPT.json`
- `research_notes/rh_goals_2026-08-14/lane_g/R2_FLAGSHIP_ENVELOPE_CHECKPOINT.json`
- `.worktrees/aletheia-restore/code/tb_certify/certify_r2_flagship.py`
- `.worktrees/aletheia-restore/code/tc_rerun/certify_r3_flagship.py`

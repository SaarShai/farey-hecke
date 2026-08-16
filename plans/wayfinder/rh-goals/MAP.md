# RH goals — decision map

## Destination
Deliver article-style, receipts-grade contributions to RH research from this
repo's verified bank: the flagship G_5 off-line-resonance theorem, the
sample-complexity theorem program, the instrument demonstration, and the
constants/priority publications — each verified or falsified at
pre-registered gates. — source: user requests 2026-08-14 ("execute!…", "this
must be top priority… until we have that theorem", "also pursue this
[T1]", "continue down that path until we have a verified and valuable
demonstration", "keep a ledger of all of the goals we are pursuing")

## Notes
- Every "pursue X" from the user lands here as a ticket; statuses update in
  place; nothing gets dropped. — source: user administrative note 2026-08-14
- Aristotle is deployed wherever valuable (T4 Prony already proved this way).
  — source: user reminder 2026-08-14
- Execution telemetry lives in research_notes/rh_goals_2026-08-14/
  EXECUTION_LOG.md; receipts in lane_a/, lane_b/, lane_c/, lane_d/. — source:
  this session's artifacts
- Claim discipline: single orchestrating session (serialized); agent lanes
  are recorded in "claimed by" as lane names. — source: wayfinder local-mode
  rule

## Expansion run 2026-08-15 (owner: "expand as much as possible, priority =
## most value to the math research community")
Priority order: P1 family theorem (q=7 first) → P2 Gonek/Mertens completion
→ P3 U₄ mechanism → P4 second G_5 pin → P5 T1 GAP-16 → P6 flagship paper
draft → P7 d3-lean-reverify. Routing: Kimi K3 medium-high; Kaggle heavy
compute; Aristotle formalizable lemmas. Plan: tasks/todo.md. — source: user
directive 2026-08-15

## Active tickets
- [LAW: off-line resonances for ALL non-arithmetic Hecke groups](tickets/family-law-theorem.md) — **TOP PRIORITY** (owner 2026-08-16: 'aim for a law'); research; finite instances (q=5 DONE, q=7 in flight) + template hardening + instance sweep q=8..12 + UNIFORM tail argument — SCOPED 2026-08-16 (lane_g/LAW_TAIL_SCOPING.md): winner = Rouché continuation from λ=2 ARITHMETIC anchor (theta group; unconditional off-line resonance at ρ₁/2 via dlVP, no RH); onset transplant FALSE-FRIEND closed; child ticket [law-tail-anchor-probe](tickets/law-tail-anchor-probe.md) — (T1) HOLDS (Γ_θ scattering derived, anchor unconditional at ρ₁/2, honest downgrade: same object as G₄, D1 carries discrimination) + D1 MIGRATION-CONSISTENT (q⁻² drift toward anchor, 3 points) + B1 no-plateau + v23 dispatched (2fc741e0). (T2) BLOCKED-AS-POSED 2026-08-16 (3 proved lemmas: no invariant disc at ANY λ — elliptic generator) → REFORMULATED (T2′): Vitali+Hurwitz on the λ_q sequence, transfer operator leaves the tail; mechanism found (parabolic k-sum = truncated ζ(2s)) explains pin migration AND missing Re=¼ pin; three independent q⁻² scalings. New crux U1 (q-uniform growth bound). U3 CLOSED 2026-08-16 TWICE (Hejhal II Ch.X Thm 5.3 p.498 located via BFM 2013 + independent Teo-FE proof; anchor zero order-2m(ρ₁) unconditional; torsion+conjugate hazards handled; V1-V3 library hygiene only). U1 lane RUNNING (q-uniform growth bound — the last crux; elliptic order q→∞ is the danger term); claimed by: lane_f (q=7) + lane_g (tail)
- [M1g upgrade: theorem-grade winding certs for the 8 predicted resonances](tickets/m1g-theorem-grade-certs.md) — research; AFK+frontier gate; open (v2 pass 2026-08-16: χ-sector evaluator built into zeta_cert_rosen_even.py, no regression; uniform tail bound honestly REFUSED — q=5-specific derivation not portable, needs own multi-day ticket; q4 k2 χ box winds 0 vs predicted 1 — OPEN DISCREPANCY, sign-convention vs escalation-ladder question; still 0/8 certified. lane_g/M1G_V2_THEOREM_GRADE.md); blocked by: tail-bound derivation for even-q geometry; claimed by: none
- [Second certified G_5 pin at a distinct real part](tickets/second-g5-pin.md) — research; AFK; open (P4); blocked by: none; claimed by: none
- [Flagship paper draft](tickets/flagship-paper-draft.md) — writing; AFK; open (P6); dissemination stays HITL; claimed by: none
- [T1 GAP-16: explicit-formula import under Riesz](tickets/t1-gap16-riesz-import.md) — research; AFK+frontier; DERIVED+DISPATCHED 2026-08-15 (lane_t/T1_GAP16_RIESZ_IMPORT.md: R₀=−2 survives, new term 12/N confirmed numerically, trivial-zero poles simple under Riesz so no log N; 7 Lean stubs → Aristotle v21 project 24c6e3df; Perron step = citation). CLOSED 2026-08-15: v21 receipt downloaded, 0 sorry, axioms propext/Classical.choice/Quot.sound; all 7 proved (Aristotle noted one unneeded hypothesis, statement untouched). T1 GAP-16 ledger row closes.
- Full adversarial audit of the top ledger items + declared theorem (Kimi K3) — REPORTED 2026-08-15 (lane_g/ADVERSARIAL_AUDIT_KIMI_K3.md): **theorem STANDS**, no theorem-level defect; Kloosterman NO-GO SOUND; M1/M2 SOUND; Kaggle lane latent defect 4-D1 (guards now built + repair running); Koyama draft 3 factual errors (now corrected). All ERRATUM items repaired same day (v18 Lean receipt downloaded from Aristotle — proof existed server-side, was unreceipted; assembly stale directives/citations/margins fixed; framing softened per 2-D1/2-D2/3-D1). — source: user request 2026-08-15
- [Mertens constant to 4–5 significant digits](tickets/mertens-constant-precision.md) — CLOSED 2026-08-15 (lane_k/P2_VERDICT_NOTE.md): **S = 0.029034 ± 0.000011, 4 digits certified** (envelope-limited 5th digit central-only; deep-block caveat recorded)
- [Cramér–Rao lower bound T1 in the frozen model](tickets/sample-complexity-t1.md) — research; AFK; v3 2026-08-15: Amendments A1 (band limit Ω=2Γ) + A2 (triangular window, owner-approved) ENACTED; (R1)/(R6)/(B1) all repaired, GAP-2/3/14/15 closed (13 open, none blocking the bound); Fisher 24 + headline constants (c=1.694/2.316) independently re-verified cold (lane_t/t1_verify.py + T1_VERIFICATION_NOTE.md); one bracket defect found by the verifier and fixed
- [Proven truncation tail bound for the G_5 operator](tickets/flagship-tail-bound.md) — CLOSED 2026-08-15: **THEOREM DECLARED** (V8 THEOREM-GRADE YES after 5 adversarial rounds; assembly v2)
- [Uniform-protocol family re-sweep](tickets/uniform-protocol-resweep.md) — research; AFK; open; blocked by: none; claimed by: none (after B5)
- [Re-certify G_5 boxes with the proven tail radius](tickets/flagship-certify-rerun.md) — CLOSED 2026-08-15: SUBSUMED by the R3b certificate (flagship box certifies with proven F_R at N=160, fails honestly at N=128; non-flagship pins deferred to family-offline-theorem)
- [Fill family-sweep data gaps (G_8 even sector; extended q=4/6)](tickets/instrument-fill-gaps.md) — prerequisite; AFK; claimed; blocked by: none; claimed by: lane B5
- [Run the preregistered blind test](tickets/instrument-blind-test-run.md) — prerequisite; AFK; open; blocked by: [Fill family-sweep data gaps (G_8 even sector; extended q=4/6)](tickets/instrument-fill-gaps.md); claimed by: none
- [Extend Gonek J₋₁ test to the full 100k-zero table](tickets/gonek-extension.md) — CLOSED 2026-08-15: 90,001-zero table merged, 5-gate PASS (max residual 2.955e-20, RvM dev 0.24), consumed by P2 verdict
- [Gonek 1989 first-test verdict call](tickets/gonek-verdict-call.md) — CLOSED 2026-08-15 (lane_k/P2_VERDICT_NOTE.md): **CONSISTENT-WITH-GONEK, convergent** — increment ratio 0.9589 (first half) → 1.0006 (top octave, T≈37.5k–75k); low-T deficit is a transient; first numerical test of Gonek 1989; pre-registered two-term fit reported but collinearity-degenerate
- [No-vertical-line certified corollary](tickets/no-vertical-line-corollary.md) — research; AFK-light; DRAFTED 2026-08-15 (lane_g/NO_VERTICAL_LINE_COROLLARY.md; Corollary 1 = Λ° ⊄ L certified; general single-line refutation stays open pending a second certified pin); frontier-reviewed
- [Fresh Lean re-verification of the Bridge identity](tickets/d3-lean-reverify.md) — CLOSED (ticket file was already resolved: lake build clean, axiom audit [propext, Classical.choice, Quot.sound]; MAP line was stale — synced 2026-08-15, found by the P7 builder). d3-submission-decision is now UNBLOCKED (HITL).
- [D3 priority-note submission decision](tickets/d3-submission-decision.md) — discussion; HITL; open; blocked by: [Fresh Lean re-verification of the Bridge identity](tickets/d3-lean-reverify.md); claimed by: none
- [Kloosterman DiscrepancyStep gate spec + probe](tickets/kloosterman-gate.md) — research; AFK; CLOSED NO-GO 2026-08-14 (frontier adjudication against the pre-registered stop criteria — see ticket erratum 2026-08-15: fluctuation object is a Mertens-weighted Dedekind-sum convolution, RH-coupled; lane_i/V_EXTRACTION.md is the documented reduction → D3 outlook)
- [Constants-paper greenlight and venue](tickets/constants-paper-greenlight.md) — discussion; HITL; **ON HOLD by owner 2026-08-16** ('wait for now; we might have new material to add before publication') — content complete (S 4 digits + Gonek verdict banked), revisit when new material lands
- [Lab distribution decision (repo/DOI vs note vs Koyama-first)](tickets/lab-distribution-decision.md) — discussion; HITL; open; blocked by: [Winding certificates for the q=4/q=6 pins](tickets/winding-certificates-q4q6.md); claimed by: none

- [Family theorem: every non-arithmetic G_q has an off-line resonance](tickets/family-offline-theorem.md) — research; AFK; q=7 prep DONE (lane_f manifest+plan, pin δ≥0.0248342) but stage-1 gate BLOCKED 2026-08-15 (F7_PILOT_REPORT.md: B_finite(N=224)≈1.145e9 vs ~30 gate; zero Kaggle spend); mitigation GO 2026-08-15 (option-2 radii, B_finite flat 20.1696 through N=224, frontier-verified from Arb receipt); pilot2 2026-08-15: stage-2 GO (--arcs CLI + seam closure built, q-independent, unit-verified), stage-3 NO-GO — q=7 R2/TB receipts missing; stages 1-2 CERTIFIED 2026-08-15/16 (F7_TB_R2_RECEIPTS.md: ρ* ≤ 0.763212029206899 Arb 19 blocks; B flat 20.1696; N=224 fails own F_R rule ×40 → N_PRIMARY=256, N_COMP=224 control; ~420 CPU-h). Stage 3 port VERIFIED but smoke STOP 2026-08-16 (stage-4b enlarged-contour ratios >1 on the 6 manifest-flagged full-Markov head blocks; F_R overflow; 0/16 kernels — correct no-launch). 4b FIXED 2026-08-16 (porting defect: enlargement ignored disc radius; rule now min(clearance/4, 0.15R); ρ̂ ≤ 0.9152411837446922 certified all 19, frontier-verified from Arb receipts; radii unchanged; F_R(256) 2.166e-9 ×153 clear). Kaggle launch lane RUNNING (builder: pin regen + smoke + 16 PRIVATE kernels). claimed by: lane_f. NOTE: Kimi K3 quota EXHAUSTED this cycle — medium-high routes to Opus until refresh.
- [M1 — Factorization theorem for arithmetic members](tickets/mechanism-m1-factorization.md) — research; AFK; M1d 2026-08-15 (lane_g/M1D_U4_CONSTRUCTION.md): FM-side U₄ FATAL, repaired via Γ₀(2)◁Γ₀⁺(2) induction (0 failures/335k words); **mechanism is scattering, not cosets** — φ₄ closed form derived, ζ(2s)⁻¹ factor identified, 4/4 new resonance predictions confirmed two-way; sector settled (MMS even); K_s interference gap closed. (C4) NOT proved — 5 FRONTIER obligations remain (Eisenstein φ₄ derivation, resonance→Z_S divisor, MMS sector transport). Follow-up M1e 2026-08-15 (lane_g/M1E_PHI6_FAMILY_PROBE.md): φ₆ analogue CONFIRMED-NUMERICALLY — 4/4 predicted resonances at multiples of iπ/log 3, 12–17 orders vs controls; same MMS even sector. Second-q confidence point, non-rigorous. M1f 2026-08-15 (lane_g/M1F_EISENSTEIN_DERIVATION.md): **G5 CLOSED** — φ forms derived first-principles (E⁺=E_∞+E_0 by coset bijection; two independent routes; sympy-exact; functional eq + residue now proofs; k≠0 exclusion forced). G6 REDUCED; G7–G9 open; N3 scout REPORTED (lane_c/N3_FRICKE_SCATTERING_PRIORART.md): no accessible prior art for the closed forms or p^s=±1 resonances; Hejhal II + Huxley UNRESOLVED (library-only) — novelty label 'plausibly new, unconfirmed'; human library check needed before any paper claim. Aristotle v22 PROVED 2026-08-15 (receipt downloaded, 0 sorry, axiom-clean): M1d's 5 finite obligations machine-verified (coset cocycle, W₂ normalizer, weight-neutral chain rule, block diagonalization, det splitting via Schur complement). M1g REPORTED honest 0/8 (sampled winding=1 ×4 trivial-sector, heuristic tail; χ evaluator absent) — upgrade ticketed.
- [M2 — Certified non-factorization for G_5](tickets/mechanism-m2-nonfactorization.md) — research; AFK; claimed; blocked by: none; claimed by: lane M2

## Decisions so far
- [Independent re-derivation of the mms+ sector convention](tickets/flagship-convention-rederivation.md) — CLOSED: engine convention MMS-correct; pin 0.45390 stands; rival value was a normalization bug.
- [K_s divisor gate for the flagship theorem](tickets/flagship-ks-gate.md) — CLOSED exactly: K_s zero lattice has Re ≤ 0, no strip contamination possible; all 13 pins clear.
- [Exact statement ruling for the flagship theorem](tickets/flagship-statement-ruling.md) — V1: "law" REFUTED as stated (one arithmetic commensurability class; non-comparable protocols); K_s gate mandatory; theorem reframed to "first rigorous resonance localization, Re ≤ 1/2 − δ_gap"; defensible paper phrasing supplied.
- [Winding certificates for the q=4/q=6 pins](tickets/winding-certificates-q4q6.md) — 5/5 certified-modulo-heuristic; tail heuristic shown non-monotone at one box corner (V1 §4.3).
- [Family sweep G_7/G_8 + blind-test protocol design](tickets/instrument-family-sweep.md) — G_7 scatter replicated; G_8 data gap identified; protocol preregistered but ruled failing-by-construction (V1 §2.4) — redesign against the uniform-sweep pool.
- [Zero-sum constant settled](tickets/zero-sum-settled.md) — S = 0.02903 ± 0.00016; 2/π² and 3/π⁴ excluded; likely first computation (triple-scouted).
- [C_W growth law corrected](tickets/cw-growth-corrected.md) — no pointwise limit; persistent Mertens-driven fluctuation; log-average restatement required.
- [Arithmetic controls passed](tickets/b2-arithmetic-controls.md) — q=4/q=6 LINE at ζ(2s) ordinates; signature law supported at 4 surfaces; 1/5 pins winding-certified so far.
- [Certified stack restored and validated](tickets/stack-restore.md) — both June gates reproduce exactly; branch aletheia-stack.
- [Prony anchor lemma machine-proved](tickets/prony-anchor.md) — Aristotle, sorry-free, axiom-clean.
- [Novelty scouts](tickets/novelty-scouts.md) — G1 headline unoccupied; no prior numeric for either constant; no prior rigorous resonance-location proof for hyperbolic surfaces.

## Not yet specified
- M3 — deformation probe (how the factorization mechanism switches off as λ
  leaves the arithmetic points): awaiting M1/M2 to sharpen the question. —
  source: user "absolutely i want it pursued" 2026-08-14
- Precise formulations of T2/T3 after T1's draft exposes the constants. —
  source: G1_MODEL_SPEC.md ladder
- Scope of the law paper (atlas vs law vs theorem-led) pending the V1 ruling
  and flagship outcome. — source: THEOREM_G5_OFFLINE_PLAN.md risks
- Whether the C_W log-average limit exists and equals a nameable constant. —
  source: lane_a/cw_growth_receipt.json follow-up question

## Out of scope
- Claiming progress on an RH proof itself; all outputs are boundary-moving
  contributions. — source: user framing ("we might not be able to prove it,
  but we might make some small breakthroughs")
- All DO-NOT-RE-CHASE items (Veech bridge, twin primes, spectral lever,
  per-step significance pivot, spectroscopy-as-tool, QMC applications). —
  source: memory DO-NOT-RE-CHASE list + kill-gate records
- Practical-value scouting (owner directive 2026-08-16): 4 luna/codex research lanes launched — prior art on (1) AI-verified math pipeline, (2) certified spectral computation, (3) QMC/hyperuniformity crossover; (4) demand assessment for certified transfer-operator numerics (climate/Koopman/MSM/control). Reports land in research_notes/practical_value_2026-08-16/ (file-drop = completion signal; codex unpollable). Frontier to synthesize on landing.
- [Pipeline packaging (public repo)](tickets/pipeline-packaging.md) — open; design-doc first, packaging after flagship paper; owner directive 2026-08-16
- [Certified spectral engine library](tickets/spectral-engine-packaging.md) — open; companion artifact to flagship paper; owner directive 2026-08-16
- [MD timescale certificate pilot](tickets/md-timescale-certificate-pilot.md) — open; KT1 (incumbent check) launched 2026-08-16; kill-first ladder, KT3 owner-gated
- Public-repo builds ACTIVATED (owner 2026-08-16): pipeline-packaging + spectral-engine-packaging upgraded from design-doc to full public repos; 2 codex deep-research lanes (gap/demand/design) → frontier repo specs → Opus 5 builders → secret-scan + frontier review → publish. MD-timescale-certificate pilot unchanged (KT1 in flight). Nothing dropped.
- LAW status 2026-08-16 (post-deciding-tests): U1 CORROBORATED — extended guard q=56/72/100 flat on identified domain (+0.07; Re=1/2 decays −0.57); adverse +1.50 was unidentified-point artifact (LAW_U1_GROWTH.md §10). U1-φ overdetermined 3-height fit brackets −3 (−2.96/−3.13; null needs m=2, measured −0.08). All three deciding tests favorable. U2b lane LAUNCHED (Opus: systole half + counting half, Aristotle-able pieces listed). Remaining after U2b: U5 (Q₀ effectivity), V1-V3 (library hygiene), U4 (proxy identification, demoted).

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

## Active tickets
- [Mertens constant to 4–5 significant digits](tickets/mertens-constant-precision.md) — research; AFK; claimed; blocked by: none; claimed by: lane A4
- [Cramér–Rao lower bound T1 in the frozen model](tickets/sample-complexity-t1.md) — research; AFK; open; blocked by: none; claimed by: none (frontier next block)
- [Proven truncation tail bound for the G_5 operator](tickets/flagship-tail-bound.md) — CLOSED 2026-08-15: **THEOREM DECLARED** (V8 THEOREM-GRADE YES after 5 adversarial rounds; assembly v2)
- [Uniform-protocol family re-sweep](tickets/uniform-protocol-resweep.md) — research; AFK; open; blocked by: none; claimed by: none (after B5)
- [Re-certify G_5 boxes with the proven tail radius](tickets/flagship-certify-rerun.md) — prerequisite; AFK; open; blocked by: [Proven truncation tail bound for the G_5 operator](tickets/flagship-tail-bound.md), claimed by: none
- [Fill family-sweep data gaps (G_8 even sector; extended q=4/6)](tickets/instrument-fill-gaps.md) — prerequisite; AFK; claimed; blocked by: none; claimed by: lane B5
- [Run the preregistered blind test](tickets/instrument-blind-test-run.md) — prerequisite; AFK; open; blocked by: [Fill family-sweep data gaps (G_8 even sector; extended q=4/6)](tickets/instrument-fill-gaps.md); claimed by: none
- [Extend Gonek J₋₁ test to the full 100k-zero table](tickets/gonek-extension.md) — research; AFK; claimed; blocked by: none; claimed by: Kaggle offload (5 kernels running, lane_k)
- [Gonek 1989 first-test verdict call](tickets/gonek-verdict-call.md) — research; AFK+frontier; open; blocked by: [Extend Gonek J₋₁ test](tickets/gonek-extension.md); claimed by: frontier on harvest
- [No-vertical-line certified corollary](tickets/no-vertical-line-corollary.md) — research; AFK-light; open; UNBLOCKED 2026-08-15; claimed by: none
- [Fresh Lean re-verification of the Bridge identity](tickets/d3-lean-reverify.md) — prerequisite; AFK; open; blocked by: none; claimed by: none
- [D3 priority-note submission decision](tickets/d3-submission-decision.md) — discussion; HITL; open; blocked by: [Fresh Lean re-verification of the Bridge identity](tickets/d3-lean-reverify.md); claimed by: none
- [Kloosterman DiscrepancyStep gate spec + probe](tickets/kloosterman-gate.md) — research; AFK; CLOSED NO-GO 2026-08-14 (pre-registered stop condition hit: fluctuation object is a Mertens-weighted Dedekind-sum convolution, RH-coupled; lane_i/V_EXTRACTION.md is the documented reduction → D3 outlook)
- [Constants-paper greenlight and venue](tickets/constants-paper-greenlight.md) — discussion; HITL; open; blocked by: [Mertens constant to 4–5 significant digits](tickets/mertens-constant-precision.md), [Extend Gonek J₋₁ test to the full 100k-zero table](tickets/gonek-extension.md); claimed by: none
- [Lab distribution decision (repo/DOI vs note vs Koyama-first)](tickets/lab-distribution-decision.md) — discussion; HITL; open; blocked by: [Winding certificates for the q=4/q=6 pins](tickets/winding-certificates-q4q6.md); claimed by: none

- [Family theorem: every non-arithmetic G_q has an off-line resonance](tickets/family-offline-theorem.md) — research; AFK; open; UNBLOCKED 2026-08-15 (flagship template declared); claimed by: none — next in line
- [M1 — Factorization theorem for arithmetic members](tickets/mechanism-m1-factorization.md) — research; AFK; claimed; blocked by: none; claimed by: lane S5 → frontier
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

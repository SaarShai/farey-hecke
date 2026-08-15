# Execution log — RH goal triad — started 2026-08-14

Frontier (me): orchestrate, own judgment-dense work (Lane B restore, Kloosterman
gate spec, Aristotle statement design, synthesis, direction changes).
Priority rule: earliest falsification first — every lane's first output is a
confirm/kill signal, not a build-out.

## Lane A — G3-S0: kill-or-confirm the two constants (codex luna xhigh)

- **A1 (agent): zero-sum settlement.** Compute Σ_ρ 1/(|ρ|²|ζ′(ρ)|²) to
  convergence (10⁴+ zeros, mpmath, Odlyzko table in repo), reproduce the E5
  convention, and identify the normalization error in log.md's 2/π² bridge.
  Kill signal: value ≈ 0.03 ⇒ 2/π² conjecture DEAD (replace with corrected
  constant); value ≈ 0.2026 ⇒ E5 was wrong, conjecture LIVE.
  Output: lane_a/ZERO_SUM_REPORT.md + receipt JSON + script.
- **A2 (agent): C_W(N) growth law.** Exact C_W(N)=N·W(N) to N ≥ 10⁶ via a
  Mertens-identity fast route (validated vs direct enumeration ≤ 2000 and
  anchors 0.497/0.635/0.668). Kill signal: bounded → 0.679 (NW conjecture
  LIVE, loglog fit dead) vs tracking 0.16+0.24·loglog N (NW conjecture DEAD).
  Output: lane_a/CW_GROWTH_REPORT.md + csv + scripts.

## Lane B — G2-S0: restore certified stack (me)

Worktree at b973d56, inventory zeta_cert/mayer files, smoke-run the q=3
anchor. Gate: recorded certificates reproduce, else STOP Goal 2 and debug
provenance. Output: lane_b/RESTORE_LOG.md.

## Lane C — prior-art scouts (research-lite, web)

- **S1 (agent):** literature value/status of Σ_ρ 1/(|ρ|²|ζ′(ρ)|²) and the
  (1/x)Σ M(n)² limit constant (Gonek, Ng 2004, successors). Protects A1's
  interpretation + G3-D2 novelty claim.
- **S2 (agent):** prior art on sample-complexity/Cramér–Rao for zero
  estimation from prime data + Prony/power-sum recovery of Frobenius
  eigenvalues. Protects G1's headline before S1 theorem work.

## Lane D — D3 note skeleton (codex luna xhigh)

- **D1 (agent):** assemble the honest-note skeleton from
  equispaced-primes/papers/nw-mertens-note/ (note + FACTS ledger), García
  2025 citation, scope disclaimers intact. NO submission. Output:
  lane_d/D3_NOTE_SKELETON.md.

## Lane E — Aristotle dispatches (async, me)

- **E1:** Prony/power-sum uniqueness (G1 anchor lemma): two multisets of ≤ d
  nonzero complex numbers with equal power sums s_1..s_{2d} are equal.
- **E2 (pending my read of the imported proof):** unconditional C_W(N) ≥ c₀
  (Franel–Landau lower bound) — dispatch only if the imported proof sketch is
  sound; otherwise it goes to a cold audit first.

## VERDICTS (same day)

- **A1 SETTLED — 2/π² DEAD.** Two-sided S = Σ_ρ 1/(|ρ|²|ζ′(ρ)|²) =
  0.02903 ± 0.00016 (3000 refined zeros, PARI/GP, residual gate 1e-15
  0-failures, E5 reproduced to 10 decimals = one-sided convention, factor 2).
  2/π² off 6×; 3/π⁴ = 0.0308 also excluded (~11σ). No published numeric
  found by S1 scout ⇒ likely FIRST receipts-grade computation of the
  Ng/Gonek Mertens mean-square constant. Receipt:
  lane_a/zero_sum_receipt.json.
- **A2 SETTLED — BOTH C_W claims wrong.** To N=10⁷ (fast Mertens-identity
  route, validated vs direct ≤2000): C_W = 0.668(1e5), 0.699(3e5),
  0.679(1e6), 0.682(3e6), 0.696(1e7). NW→0.679±0.002 violated; loglog fit
  0.16+0.24·loglog N overpredicts (0.75–0.83). Truth: persistent
  Mertens-driven fluctuation that does not decay pointwise (elevated C_W
  tracks large |T(N)|) — restate any limit claim as log-averaged/Cesàro.
  Receipt: lane_a/cw_growth_receipt.json + cw_growth_values.csv.
- **E1 PROVED (Aristotle, same day).** prony_power_sum_uniqueness sorry-free,
  axioms [propext, Classical.choice, Quot.sound], lake build clean. Artifact:
  projects/aristotle_dispatch_v16/result/project_aristotle/PronyPowerSums.lean
  (project 964f8c92). Goal-1 anchor machine-verified.
- **B S0 CLOSED (both gates).** 6/6 cert anchor (width 1.22e-05) + geometry
  signature reproduced exactly (q=3 re_std 6.475e-14 vs G_5 0.030).
  lane_b/RESTORE_LOG.md.
- **Scouts:** G1 headline unoccupied (S2); no closed form / no 2/π² in
  literature, J_{-1}(T) never numerically tested (S1) → A3 launched.

## B2 VERDICT (same day): LINE, LINE — RETRACTED-AS-LAW per V1 review

q=4: 3 pins on Re=0.25, re_std 9.83e-12; q=6: 2 pins, re_std 1.03e-11;
q=3 gate passed first. Pinned ordinates = γ/2 of first Riemann zeros.
**CORRECTION (V1 adversarial review, same day — lane_b/ADVERSARIAL_REVIEW_V1.md):**
(i) THREE arithmetic surfaces, not four, and they are ONE commensurability
class (all carry the same ζ) — evidentially one data point, a positive
engine control, NOT independent confirmation; (ii) re_std values were
measured under per-surface protocols/windows and are NOT family-comparable
(q=3 was seeded at the answer, never searched; G_5 band excluded Re<0.30
and omitted a winding-certified G_5 pin at Re=0.24303); (iii) an
independent reimplementation places a G_5 pin at 0.4332 vs 0.4539 —
convention-sensitive. Surviving statement = V1 §1.7 (fixed-window
arithmetic/non-arithmetic contrast, 2 non-arith replications). V1's OWN
new control (q=8/q=10 null: |det|=O(1) at ζ-zero points vs 1e-11 at q=4)
is the strongest evidence and must be promoted into the record. Hardening
plan: uniform-protocol re-sweep, K_s divisor gate, JP tail bound +
convention re-derivation BEFORE any theorem decimal.

## Second wave (launched after verdicts)

- A4: zero-sum to 4–5 sig figs (reuses A3 checkpoints; coordination rules in
  brief). S3: deep prior-art on both constants (Kotnik–van de Lune line).
- P1 DONE: branch `aletheia-stack` → 4c42ca0. P2: REPRODUCE.md +
  DISTRIBUTION_OPTIONS.md (owner-gated memo). P3: CERTIFIED_VS_HEURISTIC.md
  trust-boundary audit + upgrade ladder.
- G1-S0 FROZEN: G1_MODEL_SPEC.md (observable = verified smoothed-Möbius line
  spectrum; headline shape: X(ε) exponential in ε^{-2/3}; ladder T1–T4 with
  T4 done; gates G-a/b/c).

## A3 VERDICT: TOO EARLY, supportive. First-ever J_{-1} numbers.

J_{-1}(T)/T = 0.0918–0.0930 at T≈8.6k–9.9k = ~95% of Gonek's 3/π³
(0.09675); ratio drifting 0.961→0.949. 10,000 zeros, residuals ≤2.4e-18,
checkpointed, sha-stamped. Extension to N=10^5 (T≈75k) feasible for the
paper. lane_a/j_minus1_receipt.json.

## Delivered same wave

- S3: NO-PRIOR-NUMERIC on both constants (Kotnik–van de Lune line checked)
  → first-computation claims triple-scouted. lane_c/S3_DEEP_PRIOR_ART.md.
- P1: branch aletheia-stack @4c42ca0. P2: REPRODUCE.md +
  DISTRIBUTION_OPTIONS.md (note: June receipt 735s at code/out vs today's
  978.6s at code/code/out — relative-path artifact, documented).
- P3: lane_b/CERTIFIED_VS_HEURISTIC.md (trust-boundary audit) on disk.
- G1_MODEL_SPEC.md frozen (see above).

## In flight

A4 (constant 4–5 digits), B3 (winding certificates q=4/6),
A1/A2/P3 wrapper turns. Next frontier block: T1 proof draft;
optional A3 extension to N=10^5 before paper assembly.

## Direction-change triggers

- A1 ⇒ rewrite G3-D2 statement around the confirmed constant; feed Aristotle
  the corrected finite identity.
- A2 bounded-verdict ⇒ NW constant becomes a serious conjecture target
  (closed form hunt); loglog-verdict ⇒ kill NW note, record, move on.
- B failure ⇒ Goal 2 pauses; escalate provenance debugging.
- S2 collision ⇒ re-scope G1 headline before any theorem work.

## Evening wave (2026-08-14 ~20:30, post-outage recovery)

- OUTAGE AUDIT: the 13:37 network outage killed MORE than first thought —
  the R2R3 binding certification (sol) and M1a mechanism draft (luna)
  codex trees were both aborted ("turn_aborted: interrupted", rollouts
  13-01-31/13-03-11/13-36-15) and had NOT been relaunched. Both
  RELAUNCHED ~20:35; R2R3 reuses the near-complete certify_r2_flagship.py
  / certify_r3_flagship.py the dying run left, now under a
  checkpoint-to-disk mandate.
- ARISTOTLE v19 PROVED (project e02e7ec0, task c79a5491): all three
  R1Completion theorems 0-sorry, axiom-clean [propext, Classical.choice,
  Quot.sound] — l2_le_card_mul_sup_sq, coeff_bound_of_uniform,
  geom_tail_le. With v18, the R1 restatement's abstract joints are now
  machine-proved.
- K1 STEP-1 VERDICT ⇒ KLOOSTERMAN GATE CLOSED NO-GO (frontier
  adjudication vs the pre-registered spec): (i) spec defect — the frozen
  integral observable has NO A,B,C,N decomposition (four-term identity
  belongs to the old discrete observable; p=13 witness values differ);
  (ii) structural — the only source-backed fluctuation object is
  V_residue(p) = Σ_c M(⌊(p−1)/c⌋)·s(p,c), a Mertens-weighted Dedekind-sum
  convolution; the frozen paper itself rules the direct Kloosterman
  completion invalid (main.tex:1056-1064). Bounding it at any useful
  power level embeds Mertens cancellation = RH-strength input = the
  binding stop condition. lane_i/V_EXTRACTION.md + exact-rational receipt
  (p = 13, 8501, 92173 zero-error probes) = the documented reduction for
  the D3 outlook. Consistent with the 2026-06-29 verdict; thread folds.
- KAGGLE OFFLOAD LIVE: codex sandbox could not resolve api.kaggle.com, so
  frontier pushed from the main shell — 5/6 kernels up and running
  (saarshai/mertens-zeros-n100k-part1..part5, private). 6th
  (hecke-family-q7-q8-scan) queued on the 5-CPU-session cap; slot-watcher
  running. This supersedes the dead local A5 run.
- KAGGLE CORRECTION + CONFIRMATION: the "5/6 up and running" line above
  was premature — v1 crashed on Kaggle's script rename (part-number
  inference from __file__), v2 on the missing data file (kernel pushes
  upload only the code file; zeros1.txt now ships as private dataset
  saarshai/odlyzko-zeros1), v3 on mp.mpc("0.5", t) rejecting complex
  secant iterates (patched to 1/2 + i*t complex arithmetic;
  local smoke test: residual 3.8e-23, 0.89 s/zero). v4 of all five
  kernels CONFIRMED RUNNING at 7+ min (past all prior crash points),
  2026-08-14 ~21:05. Runtime risk logged: part5 (t up to ~75k) may
  brush Kaggle's session cap; 500-row CSV checkpoints make partial
  harvests usable.
- R2 PHASE CERTIFIED (21:00): all 11 column families, corrected
  center-offset envelope, Hurwitz-closed columns on 512 arcs, 384-bit —
  in 6.2 s. T_tail(128) = 5.27e-17, T_tail(160) = 6.27e-22. Frontier
  forecast from the receipt: crude prefactor B_total = 97.77 makes the
  all-analytic F astronomically large (route dead as W2 foreshadowed);
  the mandated hybrid per-arc F (T_finite ≈ 17.3) gives F(128) ≈ 0.15
  (FAIL) and F(160) ≈ 1.8e-6 vs margin 3.94e-6 (PASS, ~2.2x slack).
  N=160 fallback expected to be decisive; R3 running.
- M1a DELIVERED + ADJUDICATED ACCEPTED (20:52): honest gap map; (C4)/(C6)
  unreachable from published machinery; hardest gap = determinant-
  preserving slow/fast induction intertwiner with zeta block isolated +
  K_s divisor tracked. Takeuchi precision: G_4/G_6 = Fricke overgroups
  Γ₀⁺(2)/Γ₀⁺(3). M1b probe launched: explicit q=4 intertwiner attempt,
  falsification-first (lane_g/M1B_Q4_INTERTWINER.md).
- R3 ATTEMPT 1: NOT_CERTIFIED at N=128 (arc 0), N=160 attempt running —
  frontier diagnosis: ALGORITHMIC, not mathematical. Closed-arc det
  enclosure depth 0.122 vs pointwise det ball radii ~1e-36 at the same
  points = interval wrapping catastrophe of naive ball-matrix Gaussian
  elimination at N=128, NOT arc-width (subsegments ~4e-8 wide; first-
  order det variation negligible). ~34 orders of recoverable headroom.
  Second defect (correctly flagged by the agent): the per-arc T_finite
  prefactor omits high-output rows (V3-A2 pattern); B_tot=97.77 fallback
  is hopeless by construction. REPAIR R3b: (1) arc enclosure = midpoint
  det + width x certified d(det)/ds via Jacobi's formula (or Rump
  preconditioned det + adaptive bisection); (2) valid ||L||_1 via
  computed column 2-norms + geometric output-tail correction from the
  certified clearance-enlarged Cauchy decay. Forecast with ||L||_1 ~ 17.3:
  F(160) ~ 7e-7 < margin 3.9e-6, ~5x slack. R3b launches on process exit.
- M1B DELIVERED + ADJUDICATED ACCEPTED (21:09): q=4 intertwiner probe
  SURVIVES falsification through word length 4. Ordinary-Gauss route
  PROVEN DEAD (length-1 mismatch 2^{-s}(x+n)^{-2s}); Fricke route ALIVE:
  conjugated branches = W_2 T^n, all even first-return words through
  length 4 land in Gamma_0(2) with the EXACT modular 2s-cocycle (scalar
  factors cancel identically — frontier re-derived M_{a,b}=A_aA_b, det=1,
  even lower-left by hand: correct). Correct elementary factor = the
  machine-verified K_s divisor prod(1-(sqrt2-1)^{2s+2m}), not the guessed
  1-2^{-2s}. Remaining gap = the explicit Banach intertwiner U_4 +
  Fricke-plus restriction + P-compatibility + divisor tracking. M1C
  launched: numerical kill-test — does the G_4 determinant-zero set embed
  in the Fraczek-Mayer level-2 vector operator's zero set (3-dim coset
  rep)? REFUTED kills U_4 cheaply; SUPPORTED funds the theory climb.
- M1C KILL-TEST: CONTAINMENT SUPPORTED (21:40, 52 s run). All four q=4
  pins (s=1 + three Re=0.25 pins) vanish in the Fraczek-Mayer level-2
  modular determinant to 1e-17..1e-29, stable N=40->60; controls O(1)
  both sides. Structural finding: W_2 is singular mod 2 — no honest 3x3
  Fricke permutation action exists; U_4 needs a richer model. Route now
  two-for-two vs falsification. lane_g/M1C_Q4_KILLTEST.md + receipt.
- R3B PARTIAL (22:09, running): theorem-valid endpoint bound landed —
  ||L||_1 = ||LP_N||_1 <= 17.2912 (computed columns + enlarged-disc
  output-tail 9.24e-6 + T_tail), giving F_R(160) = 1.7797e-6 (vs
  expected contour margin ~3.94e-6: PASS territory, ~2.2x slack) and
  F_R(128) = 0.1498 (N=128 formally dead). Jacobi M' sanity 15 digits;
  mean-value arc-enclosure lemma stated (rH<1 -> G bound). Remaining:
  192 closed-arc exclusions + winding at N=160 (evaluations=0 at 22:09;
  hours of matrix compute). Immutable-receipt shas verified consumed.

## 2026-08-15 — R3B VERDICT: THEOREM-GRADE closed-contour YES at N=160

- R3b completed 00:59 (the killed codex orchestrator did not matter —
  the detached python driver + 8 arc workers finished and wrote the
  receipt). Complete closed cover TRUE: 284 accepted subarcs (71/edge,
  adaptive splits 92, max depth 8); every finite Taylor enclosure AND
  every F_R-inflated enclosure excludes 0; certified winding 1 (ball
  width 7.81e-114) + homotopy winding 1; min margin (finite lower −
  F_R) = +3.4379e-8 [erratum 2026-08-15: lower bound, quote rounded
  DOWN = 3.43786e-8; receipt ball 3.4378649…e-8]; rH ≤ 0.359 < 1.
  Frontier independent re-checks from raw records: all 284x4 gates
  true, min margin ≥ 3.437864e-8
  reproduced, 71x4 census. N=128 honestly recorded FAIL (F_R=0.1498).
- V4 ADVERSARIAL REVIEW LAUNCHED (sol): the declaration is GATED on it
  — targets: mean-value arc-enclosure lemma + H/Neumann implementation,
  enlarged-disc weight analyticity, cover completeness from raw
  records, argument-increment summation + homotopy, F_R arithmetic,
  2 independent spot-recomputes, MMS pole-set claim.
- THEOREM_G5_OFFLINE_ASSEMBLY.md written (DRAFT): full statement
  (essential-gap form, resonance interpretation), 7-link proof chain
  with per-link verification class, convention honesty, constants
  table. Declaration = single status flip after V4.
- V4 ADVERSARIAL VERDICT (completed 01:41; report recovered from rollout
  — reviewer sandbox was read-only): **THEOREM-GRADE YES DOES NOT
  SURVIVE — one theorem-level GAP; every numerical component
  CONFIRMED-SOUND** (R2 envelope, mean-value lemma + M' branches,
  endpoint norms, 284-record cover with no gaps [achieved split depth
  is 1, not 8 — report wording fixed], winding/homotopy summation, F_R
  arithmetic, MMS pole/K_s locality; reviewer's own 512-bit spot
  recomputes: margins +1.9883e-6 and +1.6204e-6). THE GAP (= R1's own
  listed remaining work): no proof yet that the Hurwitz-closed 11-block
  determinant on ⊕H² IS the MMS Banach-space meromorphic determinant
  that Theorem 6.4 factorizes. REPAIR R5 (frontier, in progress):
  common-continuation theorem — (i) space-independence of the nuclear
  eigenvalue sequence on the absolute-convergence region
  (Bandtlow–Jenkinson-class result for weighted composition operators
  on holomorphic scales), (ii) s-analyticity of both families on a
  connected domain reaching the box (all determinant poles real; box
  at Im 5.76), (iii) identity theorem. Declaration remains BLOCKED.
  Minor receipt-serialization digits note logged for the paper.
- V5 VERDICT on R5 v1 (03:25, report persisted from rollout):
  THEOREM-GRADE NO this round, but "continuation strategy viable, no
  genuine obstruction" — three precise repairs demanded: (a) exact
  operator binding (disc algebra B(D); the 11 reduced symbols with
  squared-denominator weights incl. reflected negative branches —
  the V3-line-249 convention; cite Bandtlow-Jenkinson ETDS 28 (2008)
  Thm 4.2, which identifies the determinant on BOTH Hardy space and
  disc algebra with the dynamical determinant — stronger than v1's
  citation); (b) shrink to Omega* = ({Re s>1/2} u {Re s>0, Im s>1})
  minus real poles (R2 tails need sigma>0); Simon cite -> Notes on
  infinite determinants Thm 3.3; (c) drop the invalid P paragraph,
  compare reduced 3-component operators directly. Steps 3 (MMS poles)
  and 4 (identity theorem) CONFIRMED-SOUND.
- R5 v2 WRITTEN implementing exactly the three repairs (11-block list
  from TB_V2 inlined; squared-denominator weights with certified
  positive-real-part branch bounds; Omega*; direct reduced-sector
  identification). V6 adversarial review launched (fresh sol, third
  round). Declaration still BLOCKED.
- V6 VERDICT on R5 v2 (persisted): NO, but narrowest defect set yet —
  ACCEPTED: Omega* domain/topology, Simon fix, P-removal structure,
  11-block census vs builder calls, weight equivalence
  ((z-nl)^2=(nl-z)^2). Four LOCAL defects, none obstructing:
  duplicated negative-symbol formula (sign flip in prose), wrong tail
  exponent description (must be the 2sigma+1 first-moment bound),
  finite-vs-countable word expansion, t=1 trace-log gap. V6 supplied
  the exact 3-clause minimal lemma.
- R5 v3 WRITTEN: implements the 3 clauses AND deletes the word-trace
  route entirely — replaced by smoothing (reproducing-kernel bound on
  certified enlarged discs) + Jordan-chain spectrum equality + spectral
  determinants (Lidskii on H; Grothendieck order<=2/3 on B), which
  eliminates V6 defects 3 and 4 by construction. B-J ETDS Thm 4.2
  demoted to corroboration. V7 review launched (4th round).
- V7 VERDICT on R5 v3 (persisted, 19KB): **"the seven-link mathematical
  argument survives after a local erratum" — NO MISSING LEMMA.** Clause
  1 binding PASS; smoothing PASS (the reviewer ITSELF ran a fresh
  384-bit check from the immutable TB_V2 receipt: enlargement R_i+0.1
  gives rho_hat <= 0.948343590351, min pole/cut margin >= 1.00238,
  worst branch 3->1(+1); the R3b quarter-clearance contour is NOT
  contractive for 2->3(+2) — the two enlargements must not be
  conflated); envelope/holomorphy PASS; sector identification PASS
  ("an exact identity"; MMS heading '>5' noted as a strict-inequality
  typo vs Lemma 4.2's q>=5). FAIL only on compliance: 5 local
  citation/wording defects (Lidskii-vs-Simon-Thm-4.2 product
  attribution; "order 0<=2/3" notation; false m=0-closure sentence;
  stale TB_R1 trace citation; enlargement provenance). Prescribed
  3-item erratum, after which "the seven-link assembly earns
  THEOREM-GRADE YES".
- R5 v3.1 WRITTEN: the three corrections applied verbatim (D_i^{0.1}
  enlargement named with the head/tail split + reviewer's quantitative
  instance; Simon Thm 4.2/Lidskii Cor 4.3/Grothendieck Resume Thm 8
  attributions + normalization sentence; m=0..k closure sentence).
  E1 LAUNCHED (luna): our own receipted replay of the R_i+0.1
  contraction certification (E1_ENLARGED_CONTRACTION_CERT.md), so the
  declaration rests on a replayable artifact rather than the
  reviewer's read-only diagnostic. V8 final compliance pass after E1.
- E1 DELIVERED (04:27, run IN the main writable session after the codex
  sandbox blocked writes a third time — script recovered verbatim from
  the rejected apply_patch in the rollout, one mangled paren repaired,
  syntax-verified): VERDICT PASS_RHO_HAT_LT_1_AND_CLEARANCE_POSITIVE.
  rho_hat = [0.948343590350471954782853 +/- 4.84e-25], min pole/cut
  margin = [1.00237987356225289328078 +/- 9.41e-25], worst branch
  3->1(+1) head, all 11 families pass, receipt sha cd1dc6f4...d37187.
  Matches V7's independent read-only diagnostic digit-for-digit — the
  smoothing premise now rests on two independent computations plus a
  receipted artifact. R5 v3.1 updated to cite the receipt.
- V8 FINAL COMPLIANCE PASS LAUNCHED — first run under the owner's new
  routing directive (2026-08-15): Opus 5 medium-effort Claude agent,
  NOT codex sol (sol retired for medium-high tasks after three
  read-only-sandbox report losses; luna retained for small tasks;
  Aristotle/Kaggle first-choice where applicable — recorded in
  persistent memory agent-routing-opus5).

## 2026-08-15 ~04:55 — **THEOREM DECLARED**

V8 (Opus 5, per the new routing directive) FINAL RULING: THEOREM-GRADE
YES — erratum verified item-by-item; E1 receipt sha recomputed and its
margins/sups independently reproduced (closed form + 200k-point sweep);
V7 quotations verified faithful; two editorial blockers fixed same
turn (R5 ledger line; assembly link 4b + status flip). DECLARED:
first rigorous localization of an off-line resonance of a
non-arithmetic finite-area hyperbolic surface — G_5 Selberg-zeta zero
s* within 1e-6 of 0.4538951800749447 + 5.7635372417301305i, essential
gap delta >= 0.0461038. Assembly v2 = the citable statement + 8-link
chain (incl. 4b transport) + dependency classes. Koyama draft
{{FLAGSHIP}} filled (send remains owner-gated). flagship-tail-bound
CLOSED; family-offline-theorem and no-vertical-line-corollary
UNBLOCKED. Known cosmetic: E1 md arrow labels double-encoded
(mojibake) — receipt values unaffected; fix at writer if regenerated
(hash would change; re-quote in R5 then).

no-vertical-line-corollary DRAFTED (lane_g/NO_VERTICAL_LINE_COROLLARY.md): certified Corollary 1 — Z_{G_5} has a non-real strip zero s* with Re(s*) <= 0.4538962 < 1/2 (delta >= 0.0461038), so the non-real strip zero set is not contained in Re(s)=1/2; Corollary 2 refutes the c=1/2 line ONLY (one certified pin = one real part), K_s divisor zeros handled as Re<=0 poles outside the strip, real-axis trivial/small-eigenvalue zeros excluded by stating the result for Im != 0; no density, family, or "arithmetic <=> line" claim.

T1 DRAFTED 2026-08-15 (lane_t/T1_CRAMER_RAO_DRAFT.md, lane T-opus): CR bound in frozen model N2 proved with explicit constants — S_eps(omega)=a_|omega|^2 log(|omega|/2pi) makes the zeta-prime amplitudes cancel, giving max_j RMSE >= sqrt(6 log(gamma_d/2pi))/(log X)^{3/2} and X(eps) >= exp((6 log(gamma_d/2pi))^{1/3} eps^{-2/3}), c=1.694 (d=1) / 2.316 (d=10); single-tone FIM constant 24 numerically confirmed to 3 digits; gate G-a does not fire on the leading constant (amplitude-free), gate G-b passes at 5.05x vs Gate-1; 13 gaps logged, 5 ARISTOTLE-ABLE / 8 FRONTIER, the load-bearing ones being a band-limitation repair owed to the spec as an amendment, failure of Gaussian-approximability under the Gaussian smoothing, and N2 being pessimistic at low height (gamma_1 empirical error sits 5.5x below the bound).
- 2026-08-15 frontier SELF-AUDIT (parallel to the Kimi K3 external audit):
  cross-artifact constants sweep CLEAN (s0, delta, T_tail, F_R, ||L||_1,
  E1 sha, R2 sha consistent everywhere); seed-table sha match confirmed
  (local zeros1.txt == Kaggle seed_table_sha256 3436c916...). Two errata
  found+fixed: (1) min-margin quotes rounded UP in 5 places (assembly
  constants table, ticket, corollary x2, this log) — corrected to
  round-down 3.43786e-8 with erratum tags; (2) assembly dependency
  ledger still cited pre-V7 "Simon Trace Ideals Thm 3.4/3.7" —
  corrected to Simon Adv. Math. 24 (1977) Thm 4.2 / Grothendieck Thm 8
  per R5 v3.1. Kaggle lane defect found by new monotonicity gate:
  part4 5 bad rows (2 duplicate zeros), part5 6 bad rows (1 duplicate)
  — residual gate provably blind to neighbor-zero convergence;
  seed-validation repair (mp.zetazero, receipts) running.
- 2026-08-15 KIMI K3 EXTERNAL AUDIT REPORTED (lane_g/
  ADVERSARIAL_AUDIT_KIMI_K3.md): THEOREM STANDS — no theorem-level
  defect in the 8-link chain, code, or citations; margin-vs-F_R
  suspicion dissolved (norms inside the exponential, verified in code
  and by hand over all 284 records); contour closure, ball arithmetic,
  MMS match, all 9 shas independently verified. Five issues all prior
  rounds missed, chief = 1-E1: "Lean-proved v18" had NO local receipt
  (dispatch file with sorries only). RESOLVED same hour: Aristotle
  project e84ced30 shows COMPLETE — both lemmas proved 0-sorry,
  axiom-clean; result downloaded to projects/aristotle_dispatch_v18/
  project_aristotle/ (claim was true, receipt was missing). All other
  errata repaired: assembly stale directives removed, dependency ledger
  completed (4b citations, E1 receipt, R5 proofs), R1 Steps 3-4 marked
  superseded, KS point-vs-box note, MMS q>5 footnote, rho_hat added to
  constants table, TB_LEMMA_CHAIN forward pointer, winding-serialization
  caveat, Kloosterman/M2 framing softened (2-D1, 2-D2, 3-D1/D2),
  Koyama letter factual errors fixed (5-D1..D5: three-not-nine
  witnesses + heuristic qualifier, G_8 dropped, 1e-11..1e-14 honest
  agreement figures, Gonek dating via Ng 2004). Part4/5 harvest
  artifacts committed to lane_k/harvest/.

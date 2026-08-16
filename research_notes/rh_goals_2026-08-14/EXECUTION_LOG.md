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
- 2026-08-15 T1 AMENDMENT A1 ENACTED + T1 REVISED TO v2 (lane_t):
  owner-approved band-limitation clause M4′ (|ω| ≤ Ω := 2Γ, estimator
  class restricted) appended as a dated additive amendment to the
  frozen G1_MODEL_SPEC — repairs regularity (R1) by removing the
  vacuous infinite-information artifact (divergent Cameron–Martin
  integral from the super-exponentially decaying noise floor); frozen
  v0 body untouched; post-freeze/post-hoc status stated. (R6)/GAP-3
  left OPEN with the window replacement logged as proposed amendment
  A2, AWAITING OWNER RULING (not enacted). T1 v2: GAP-2 CLOSED
  (REPAIRED-BY-A1); Fisher information re-derived under the band —
  tones interior with margin ≥ Γ, S_ε(γ_j) unchanged, factor 24
  re-verified independently (band-limited 3×3 FIM, white noise:
  23.93/23.82/23.95). Two new defects found by the re-derivation and
  logged, not smoothed: v1's "band-limiting only removes information
  so the bound transfers" is BACKWARDS (corrected, §A1.3), and at the
  approved Ω = 2Γ band-edge leakage dominates the FIM (measured
  [I^{-1}]_ωω = 7.7e−30 × the local 24-value at Γ=50, T=17.2167) so T1
  carries an explicit leakage hypothesis (B1) that holds only for
  Ω − γ_d = O(1) → GAP-14; plus GAP-15 (positivity of extended S_ε
  below |ω| = 2π, benign). Gaps ledger 15 entries: 1 closed, 14 open.
- 2026-08-15 KAGGLE HARVEST WAVE 2: part1 + q7q8 COMPLETE and
  harvested; parts 2/3 hit the 12h cap with checkpoints intact
  (14000/18000, 16500/18000 rows saved) — gap-filler kernels part2b
  (42000-45999) and part3b (62500-63999) pushed and running. CRITICAL
  FIX before any consumption: CSV index is 1-BASED into the seed table
  (kernel refines seeds[index-1]); gate + repair scripts had assumed
  0-based — the misconvention repair was killed BEFORE writing output;
  scripts fixed (convention pinned in headers), verified empirically.
  Corrected seed-validated repair: 28 wrong-zero rows across the 5
  tables (4/2/3/8/11) re-refined by siegelz bisection in seed-midpoint
  brackets. FULL GATE PASS on all 5 repaired tables (G1 residual, G2
  monotone, G3 seed-match, G4 index, G5 Riemann-von Mangoldt count —
  the RvM check also independently confirms Odlyzko-table completeness
  per audit 4-D2): 84,501 verified zeros to T~74,921. Receipts:
  lane_k/harvest/GATE_RESULTS_2026-08-15.jsonl + per-part repair
  receipts. Also repaired: earlier harvest commit had landed under
  projects/aristotle_dispatch_v18/ via cwd drift — git mv'd to
  lane_k/harvest.
- 2026-08-15 T1 AMENDMENT A2 ENACTED + T1 REVISED TO v3 (lane_t):
  owner ruled on the A2 question left open at G1_MODEL_SPEC §A1.5
  ("i trust your judgement. please do what you recommend"); the
  frontier recommendation was APPROVE, so A2 is enacted as a second
  additive dated amendment — frozen v0 body and A1 untouched. Clause
  (W′) replaces the Gaussian window W = e^{−x²} (M_W = ½Γ(s/2), Mellin
  decay e^{−π|s|/4}) by the order-1 Riesz/Fejér window W = (1−x)_+,
  M_W(s) = 1/(s(s+1)), decay |s|^{−2} — the MILDEST smoothing that
  keeps the observable defined (k=0 sharp cut makes Σ_γ a_γ diverge;
  k≥2 loses the closed form and worsens the GAP-4 flatness, which
  scales like 2(k+1)/(ωT)). R₀ = −2 survives exactly, M_W stays in
  closed form, and the arithmetic side becomes the finite Cesàro mean
  (1/N)Σ_{k<N}M(k) — one Möbius sieve pass, cheaper than the frozen
  observable. Clause (M4″) adds the spectral floor ϑ_min = log(γ_1/2π).
  T1 v3 re-derives everything and MEASURES it (script reproduces every
  v2 Gaussian figure to 5 digits before being applied to (W′)):
  Prop 4.4 is window-INDEPENDENT, so the amplitude cancellation and
  hence EVERY HEADLINE CONSTANT IS UNCHANGED (c_d = √6, c = 1.6944
  d=1 / 2.3157 d=10, X(ε) ≥ exp(2.3157 ε^{−2/3})); factor 24 verified
  a third time, now band-limited AND coloured by the actual new S_ε at
  Ω = 2Γ → [I^{−1}]_ωω = 0.9943 × the local 24-value (was 7.7e−30).
  THREE GAPS CLOSED: GAP-3 (Lindeberg ratio Λ(Γ) = 6π/(Γ(log(Γ/2π)+⅓))
  → 0, measured 0.157/0.0248/3.5e−3/2.4e−4 at Γ = 50/200/1e3/1e4 vs
  4.76 > 1 under the Gaussian); GAP-14 ((B1) measured directly as
  λ_max(I_N^{−1}I_R) = 0.0858 ≤ 1/K = 0.25 at γ_d, admissible out to
  Ω ≈ 8Γ, was 1.73e+29); GAP-15 (clause M4″ + floor sweep, 4e−4
  relative over a factor 40 in ϑ_min). GAP-4 REDUCED not closed
  (flatness 98.2 → 1.23 at γ_d, 2.03 at γ_1; now an explicit
  O(K/(ωT)) constant, tag FRONTIER → ARISTOTLE-ABLE). TWO GAPS OPENED
  BY A2 AND LOGGED AT FULL WEIGHT: GAP-16 (the VERIFIED
  explicit-formula import is Gaussian-only and no longer applies; the
  order-1 Riesz formula — new pole term R_{−1}(N) = 12/N at s = −1,
  absolute convergence resting on J_{−1}(T) = O(T) — is stated but NOT
  re-derived here; largest open item) and GAP-17 (Berry–Esseen rate
  behind the now-valid Lindeberg condition; Λ(50) = 0.157 is not
  negligible at the operating point). Riders kept, not smoothed: (B1)
  as an inequality still fails at the lowest tone γ_1 (λ_max 0.587)
  and is marginal at γ_2 (0.220), but every measured deficit (max
  0.257) sits inside T1's own declared O(K^{−1}) = 0.25 with implied
  constant ≈1.03, and the max_j statement is attained at j = d where
  the deficit is 0.6 %; and the γ_1 empirical tension is numerically
  UNCHANGED and now HARDER to dismiss (at Ω = 2Γ the bound is proved,
  not a local surrogate), with its amplitude leg reversed —
  neighbouring interferers go from 250× weaker to comparable (0.454),
  so N2 is less pessimistic and the residual is isolated to GAP-9.
  Self-serving audit written into spec §A2.6 and draft §7.4: A2 moved
  the MEASURED bound 29 orders of magnitude but changed no displayed
  constant, made the noise model heavier-tailed, was motivated by
  GAP-3 (which has nothing to do with the constant) before GAP-14
  existed, and cost two new gaps. Gate G-a no longer fires. Practical
  payoff: |M_W| at γ_10 up 13.8 orders (5.909e−18 → 4.034e−4), dynamic
  range over γ_1..γ_10 down from 13 orders to a factor 12.3. Ledger:
  17 entries, 4 closed (GAP-2, GAP-3, GAP-14, GAP-15), 13 open.

- 2026-08-15 — **GAP-16 DERIVED + finite core DISPATCHED.** Order-1 Riesz
  explicit formula re-derived (Prop. R): arithmetic side exact and finite,
  Σ_{n≤N}μ(n)(1−n/N) = (1/N)Σ_{k<N}M(k); residues R₀ = −2 (unchanged) and
  the new R_{−1}(N) = 12/N at the s = −1 pole of M_W = 1/(s(s+1)); trivial
  zeros now give SIMPLE poles, R_triv = Σ N^{−2n}/((−2n)(1−2n)ζ′(−2n)) =
  O(N^{−2}) with **no log N** (the Gaussian had double poles); remainder
  O_A(N^{−A}) for fixed A ∈ (1,2), polynomial not superpolynomial. Perron +
  contour shift remains a CITATION (Hardy–Riesz Ch. V, Montgomery–Vaughan
  §5.1, Titchmarsh §3.7/§9.7), not a repo proof. Numeric check (mpmath,
  non-rigorous, N = 2·10³/8·10³/2·10⁴, K = 25→200 zeros): residual monotone
  in K, 3.8e−2 → 5.1e−3 at N = 2·10⁴; the 12/N term is required (dropping it
  moves the N=2000 residual by 6e−3 vs a 5e−4 residual). Artifact
  `lane_t/T1_GAP16_RIESZ_IMPORT.md`; Lean core (7 statements)
  `projects/aristotle_dispatch_v21/RieszImport.lean`, Aristotle project
  24c6e3df-76fd-43d0-a052-b6ddf10d6084. NOT proved; closure pending Aristotle
  + frontier review of the analytic step.

- 2026-08-15 — **M1D U₄ CONSTRUCTION DELIVERED** (P3; lane_g/M1D_U4_CONSTRUCTION.md).
  M1c's obstruction sharpened to FATAL (W₂ ∉ N(PSL(2,Z)), explicit witness w·L·w⁻¹ =
  [[1,−1/2],[0,1]]) — no linear Fricke action on the Fraczek–Mayer 3-coset module exists,
  killing every U₄ whose modular side is Γ₀(2)\PSL(2,Z). Repair: induce along
  Γ₀(2) ◁ Γ₀⁺(2) (2 cosets, W₂ acts by σ); U₄ = (1⊗V)(C⊗1) with C the D₂ composition
  operator (weight-neutral) and V the Z/2 character basis, giving the exact
  det(1−L̂⊗σ) = det(1−L⁽⁴⁾_{s,+})·det(1+L⁽⁴⁾_{s,+}) — divisibility proved, not asserted.
  Coset cocycle ρ⁺(word of length r) = σ^r exact-verified on ALL 335,344 words of length
  1–6 over an 8-letter alphabet plus 46,800 exact Möbius/2s-cocycle identities: 0 failures.
  Genuinely new content: the q=4 scattering determinant derived in closed form,
  φ₄(s) = [√π Γ(s−½)/Γ(s)][ζ(2s−1)/ζ(2s)]·(1+2^{1−s})/(1+2^s) (χ-twist: (2^{1−s}−1)/(2^s−1)),
  which locates ζ(2s) at the CUSP, not in coset combinatorics — so no finite-coset
  intertwiner can ever produce it. It passes 3 self-checks (functional equation to 1e−31,
  residue at s=1 = 1/vol exactly, p→1 degeneration) and makes 4 novel predictions of EXTRA
  resonances at 2^s = −1 (trivial sector) and 2^s = +1 (χ sector): all 4 confirmed to
  20–30 digits with two-way sector discrimination and order-one nearby controls
  (|det(1−L₊)| = 5.7e−30 at iπ/log2 while |det(1+L₊)| = 1.95; reversed at 2iπ/log2).
  Sector assignment settled numerically: the Riemann-zero divisor is in the MMS (P)-EVEN
  sector (|D₄⁺| ≈ 7e−19 at ρ₁/2,ρ₂/2,ρ₃/2 vs |D₄⁻| = 0.25, 2.09, 6.74). Gap closed
  outright: det(1−K_s) has ALL zeros on Re s ∈ Z_{≤0}, so it cannot interfere on
  Re s = 1/4 — a zero of the reduced determinant there IS a zero of Z_{S,4}. Also
  corrects M1c's pin2 (γ₂ was off in the 12th digit; the "shallow zero" was pin precision,
  not the operator). (C4) NOT proved. Ledger: 12 obligations, 4 PROVED, 5 ARISTOTLE-ABLE,
  5 FRONTIER (G5–G9 = the actual theorem: Eisenstein derivation of φ₄, the resonance/Z_S
  divisor theorem, and the MMS-6.4 → Selberg sector transport), 2 cheap compute items
  (certified winding at the 4 prediction points; the q=6 analogue φ₆ with extra resonances
  at iπ/log 3, which would make the mechanism a family statement). Numerics are
  NON-RIGOROUS Arb midpoints via the unmodified zeta_cert_rosen_even.py builder.

- 2026-08-15 — **P1 LAUNCHED: FAMILY OFF-LINE THEOREM q=7 PREP COMPLETE**
  (ticket family-offline-theorem; lane_f/F7_CONSTANTS_MANIFEST.md +
  lane_f/F7_CERT_PLAN.md). K_s lattice for q=7 derived EXACTLY, not by q=5
  analogy: h_7=2 keeps the full Lemma-6.3 word A_s = L_1²L_2L_1L_2 (5-cycle on
  B_5; q=5's L_1^{h−1} factor vanishes at h=1), matrix word M_2M_1M_2M_1M_1
  computed in Z[λ]/(λ³−λ²−2λ+1) giving trace τ_7 = 4λ_7²+3λ_7 =
  18.393731622284383…, det = 1, ell_7 = 0.054527994798052490833925…,
  a_7 = 2.909041043174857…, zero lattice s = −n+iπk/a_7 all Re ≤ 0 (matches
  FAMILY_PREP digit-for-digit; fixed-point/eigenvalue cross-checks pass).
  Block structure at κ_7=5: 19 blocks (9 heads + 10 tails) vs q=5's 11, from
  MMS eq. (34), cross-checked against the builder's captured calls. Primary
  pin from the q7 mms+ scan: s₀ = 0.4751647621098225+4.668743786424289i
  (N22→N28 drift 1e−14, K_s box margin 0.5895480, δ ≥ 0.0248342). Cert plan:
  full G5-constant change table (file:line → q=7 value), provisional
  N = 224/192 pending the R2/endpoint F_R trade-off (ρ* = 0.7823 float,
  0.70-gate re-targeted to 0.80), contour cost ~280 CPU-h at N=224 ⇒ Kaggle
  chunking MANDATORY (16 chunks × 12 base arcs after an `--arcs i:j` CLI
  addition + a pilot chunk to measure true per-eval cost). MMS eq-(34)
  heading q>5 covers q=7 verbatim — the q=5 footnote is unneeded. No
  execution yet; heavy cert awaits owner word / Kaggle slot.

- 2026-08-15 — **M1E: q=6 φ-family probe, G12 closed (compute item).**
  lane_g/M1E_PHI6_FAMILY_PROBE.md. Derived φ₆(s) = g(s)·(1+3^{1-s})/(1+3^s)
  (trivial sector) and φ₆^χ(s) = g(s)·(3^{1-s}-1)/(3^s-1) (χ sector) by the
  same p-generic Fricke-symmetrisation as M1D §5.1, p=3, G₆≅Γ₀⁺(3) (Takeuchi).
  All 3 self-checks pass (functional eq. to ~1e-31, residue at s=1 matches
  1/vol(Γ₀⁺(3)\H)=6/(4π) to 10 digits, degeneration argument p-generic).
  Reused the existing even-q certified builder
  `.worktrees/aletheia-restore/code/zeta_cert_rosen_even.py`
  `build_reduced_matrix_ball(s,N,sign,q=6)` UNMODIFIED — no new engine
  written (q=6 already supported: `lam_ball` has an explicit √3 branch).
  Sector assignment at known ζ pins matches q=4 (D₆⁺≈2e-10 at both pins,
  D₆⁻ order-one; Riemann divisor in MMS (P)-even sector at q=6 too). The 4
  predicted extra resonances (trivial: s=i(2k+1)π/log3; χ: s=i(2k)π/log3,
  π/log3=2.8596009) confirmed 4/4, two-way sector discrimination
  (1e-13..1e-15 on-sector vs 10⁰-10¹ off-sector and at 4 nearby controls),
  N=40→60 stable. Verdict: CONFIRMED-NUMERICALLY, non-rigorous throughout.
  Obligations: G12 closed as compute item; G5-G9 (theory: Eisenstein
  first-principles derivation, Selberg-divisor transport) unchanged/still
  open — this probe adds a second-q confidence point, not a proof.

- 2026-08-15 — **M1D ARISTOTLE-ABLE dispatch, V22 (5 finite-algebra
  obligations from the gaps ledger, lane_g/M1D_U4_CONSTRUCTION.md §9).**
  Extracted the 5 obligations the task named: coset-cocycle constancy
  (`ρ⁺(A_n)=σ` for all `n`, §2.3/§4 C7), the `W₂` normalizer computation
  `wγw⁻¹=[[d,−c],[−2b,a]]` (§2.3), weight-neutrality of the `D₂` composition
  operator via the chain rule (§1), the block-diagonalization identity
  (`VσV⁻¹=diag(1,−1)`, §3.3), and the exact 2×2 determinant splitting
  `det(1−N_s)=det(1−L)·det(1+L)` (§3.3, ledger G1) restated at the finite
  linear-algebra level (`det(1−[[0,A],[A,0]])=det(1−A)det(1+A)` for a general
  `n×n` complex matrix `A`, dropping the note's own nuclear-operator/
  trace-expansion route as out of scope for a finite dispatch). All 5 stated
  self-contained and sorry-stubbed, none skipped
  (`projects/aristotle_dispatch_v22/SKIPPED.md` records the scoping choice
  on obligation 5). New project scaffolded on `aristotle_dispatch_v21`
  (same lakefile.toml/lean-toolchain/lake-manifest.json, Lean/mathlib
  v4.28.0): `projects/aristotle_dispatch_v22/M1DIntertwiner.lean` (7
  theorems covering the 5 obligations). Dispatched via
  `aristotle submit "<prompt>" --project-dir .` (async, not awaited).
  Aristotle project id `a1b1fc0d-a13f-4bde-aa19-42f69835fcaa`
  (`projects/aristotle_dispatch_v22/PROJECT_ID.txt`). G5–G9 (FRONTIER:
  Eisenstein-derivation of `phi_4`, resonance/divisor transport) untouched,
  out of scope per the task's own 5-obligation list.

- 2026-08-15 — **M1F: first-principles Eisenstein derivation of the Γ₀⁺(p)
  scattering determinant; G5 CLOSED (modulo one cited textbook formula).**
  lane_g/M1F_EISENSTEIN_DERIVATION.md. Verdict DERIVED-MODULO-GAPS — the M1D/M1E
  closed forms are CONFIRMED, not refuted, and no discrepancy of any kind was
  found. Chain: (1) W_p normalises Γ₀(p) for general p, [[a,b],[pc,d]] ↦
  [[d,−c],[−pb,a]] (§1.1, generalises M1D's p=2 G2); W_p swaps the cusps ∞↔0
  so Γ₀⁺(p) has ONE cusp (§1.2, PROVED — M1D asserted this); the cusp width is
  unchanged so σ_∞=I for both (§1.3). (2) G_q ≅ Γ₀⁺(p) via the EXPLICIT
  conjugator D=diag(p^{1/4},p^{−1/4}) which is simultaneously the G_q cusp
  scaling matrix ⇒ φ transports with NO λ^{2s−1} scalar (§1.4, a real trap
  closed); two independent volume checks agree ((2,q,∞) triangle area
  π(1−2/q) vs (π/6)(p+1): π/2 and 2π/3 both MATCH, §1.5).
  (3) **The key new result**: E^+ = E_∞ + E_0 proved by a pure coset bijection
  with zero analytic input (§2.2), using the structural coincidence that the
  scaling matrix of Γ₀(p)'s second cusp IS the Fricke involution (§2.1);
  χ-twist gives E^χ = E_∞ − E_0 (§2.3). So M1D §5.1's "symmetrisation" is now a
  THEOREM, not an ansatz, and it is exactly the eigen-decomposition of the 2×2
  Φ(s)=[[A,B],[B,A]] on the W_p-symmetric/antisymmetric vectors in the SAME
  character basis V M1D used on the operator side (§3.1). (4) Both Γ₀(p)
  entries DERIVED from the allowed-moduli constant-term formula + an
  Euler-product restriction lemma: moduli pm with count φ_E(pm) giving
  φ_∞∞ = g(s)(p−1)/(p^{2s}−1) (§3.3), and moduli n√p (p∤n) with count φ_E(n)
  giving φ_∞0 = g(s)(p^s−p^{1−s})/(p^{2s}−1) (§3.4) — both exactly the entries
  M1D had only CITED. φ_00=φ_∞∞ and φ_0∞=φ_∞0 computed, not assumed.
  (5) SECOND independent route: apply the same formula DIRECTLY to Γ₀⁺(p),
  whose modulus set is the disjoint union (rational vs irrational multiples of
  √p — no interference, no recount), never mentioning the Γ₀(p) scattering
  matrix at all (§3.5). Both routes agree. (6) Algebra verified symbolically in
  sympy (exact 0, no floats): A±B → (1+p^{1−s})/(1+p^s), (p^{1−s}−1)/(p^s−1);
  matches M1D §5.1 (p=2) and M1E §1 (p=3) character-for-character (§4).
  (7) g(s) = Λ(2s−1)/Λ(2s) with Λ(w)=π^{−w/2}Γ(w/2)ζ(w) ⇒ g(s)g(1−s)=1 is now
  a ONE-LINE proof from Λ(w)=Λ(1−w), replacing M1D/M1E's ~1e−31 numeric check;
  same for Res_{s=1}φ⁺ = 6/(π(p+1)) = 1/vol (§4.3–4.4). The full divisor of g
  falls out (poles s=ρ/2 at Re=1/4, zeros s=(1+ρ)/2 at Re=3/4, simple zero at
  s=0, simple pole at s=1). (8) Extra resonances re-derived: poles genuine and
  non-removable because g is finite+nonzero on Re s=0∖{0} (Re(2s)=0 and
  Re(2s−1)=−1 both lie OUTSIDE the critical strip where Λ has no zeros) and
  the numerators are 1−p and p−1 ≠ 0; and the χ-sector k≠0 exclusion that M1D
  and M1E both stipulated without reason is FORCED — g has a simple zero at
  s=0 that exactly cancels the elementary factor's simple pole (§5.3b).
  Obligations delta: **G5 CLOSED** modulo the single CITED allowed-moduli
  formula (Iwaniec ch. 3 / Hejhal LNM 1001 ch. 11), whose content is stated
  explicitly but whose NUMBER is unpinned. **G6 REDUCED, still open** — §5.2
  derives "pole of φ at non-real s₀, Re s₀<1/2 ⇒ zero of Z of the same order"
  using only the SHAPE of the elementary factor Ψ in Z(1−s)=Z(s)φ(s)Ψ(s)
  (Γ-ratios × exp(entire) ⇒ zero-free and pole-free off the real axis, and
  every point of interest is non-real); multiplicity now comes for free; the
  residue is a pinned citation for the functional equation. Notably this needs
  NO Selberg-1/4 / spectral-gap input. **G7, G8, G9 UNCHANGED** — §3.1's
  matching Z/2 bases explicitly flagged suggestive-only, no intertwiner
  claimed. New obligations N1 (pin the constant-term formula), N2 (pin the
  Selberg functional equation = G6's residue), **N3 (prior-art: is the Γ₀⁺(N)
  scattering determinant already published? correctness does not depend on it,
  NOVELTY does — standing instruction in §6.1 forbids any novelty claim on
  (PHI) or the extra resonances until Huxley 1984 and arXiv:math/0702030 are
  actually read)**, N4 (Γ₀(p) generators, trivial). A citation-pinning web
  scout was run and **resolved nothing** — GSM 53 / LNM 1001 / Takeuchi PDFs
  all unreadable (binary or image-scanned); outcome recorded in §6.1 so the
  next pass does not repeat it, and NO theorem number is asserted anywhere in
  the note. 7 Aristotle-able items extracted (A-1..A-7; highest-value is A-4,
  the Euler-product restriction lemma). No numerics were produced or relied on;
  this is a derivation note. Not committed.

- 2026-08-15 — **M1G predicted-resonance winding attempt: 0/8 rigorously certified.** Wrote `lane_g/M1G_PREDICTION_WINDING_CERTS.md` and eight receipts under `lane_g/m1g_receipts/`. At `N=60`, 400-bit Arb, `K=24`/edge, and `1e-3` half-width, all four available trivial-sector runs numerically isolated sampled winding 1 with positive sampled contour lower bounds, but the q4/q6 routine's disclosed `4*max(center,corners)` dimension-tail inflation is heuristic rather than a proven uniform contour bound, so all four are `FAILED-TO-CERTIFY`. All four chi-sector `det(1+L_+)` points are `BLOCKED`: the existing winding entry point only evaluates `det(1-L_{s,sign})` (`TypeError: winding_box() got an unexpected keyword argument 'determinant_sector'`), and no evaluator was written or modified. Pure-imaginary evaluation itself succeeded; not committed.

- 2026-08-15 — **F7 q=7 pre-Kaggle pilot gate: BLOCKED at stage 1.**
  Re-measured non-rigorous float `rho*=0.782263813617748` for factors
  `(2.79,2.39,1.90,1.56,1.35)` (passes proposed float `<0.80` re-target).
  The 384-bit whole-box endpoint finite-column computation gave
  `B_finite<=18.0743955713902...` at `N=32`, but
  `B_finite<=1145138630.686644864...` at provisional `N=224`; the production
  endpoint formula only adds nonnegative terms. This exceeds the plan's
  `B approximately 30` stop criterion, so the `--arcs` change and local pilot
  were not run, no Kaggle kernel was generated, and no disc optimization was
  improvised. Report: `lane_f/F7_PILOT_REPORT.md`.

- 2026-08-15 — **F7 q=7 stage-0 mitigation: GO (conditional on option-2 radii).**
  Executed only the two frozen options (deeper grid; per-block/per-class
  radii), all NON-RIGOROUS FLOAT PREPARATION with the pilot's machinery.
  Option 1 (371,293-point grid + 245-start coordinate descent): factors
  `(3.500,2.622,2.210,1.740,1.462)`, float `rho*=0.729128488886` (rounded
  down), but `B_finite(N=224)=68.5653778407` — growth rate cut ~10x (x1.014
  vs x1.155 per column) yet still exponential, ABOVE the `B~30` gate.
  Option 2 per-block floor is 0.1959 (unrealizable: single radius per disc);
  its realizable form — a d_5-constrained scan re-optimizing d_1..d_4 — gave
  `(3.522,2.622,2.372,1.790,1.600)`, float `rho*=0.762251293807` (< 0.80
  gate), with `B_finite` FLAT in N: 20.1664227119 (N=32), 20.1696344570
  (N=128), 20.1696367902 (N=224, build 48.45 s, +norms 48.96 s) — growth
  collapsed, PASSES the `B~30` gate. Endpoint reconstruction validated by
  reproducing the pilot's frozen-factor `B_finite(N=32)=18.0743955713902...`
  bit-for-bit. Diagnosis: the explosion driver is not dimension (1120 vs
  480) or block count (19 vs 11) but exponential growth of the exact-Hurwitz
  tail columns into the last disc, controlled by `|c_5|/rho_5 = 1/d_5`;
  q=5's stage-0 optimum sat at d_3=1.70 (sub-threshold, 0.588) while q=7's
  frozen d_5=1.35 (0.741) sat in the growing regime. Deviation disclosed in
  report: the ticket's `B(32)<5` precondition for the N=224 run was not met,
  but the designated N-scaling diagnostic showed collapse, so N=224 was run
  to settle the verdict. Report: `lane_f/F7_MITIGATION_REPORT.md` (+ scripts
  and JSON receipts in `lane_f/`). Not committed; no Kaggle kernels; no
  other lanes touched.

- 2026-08-15 — **F7 q=7 stages 2-3 (CLI + pilot chunk): CLI done and
  unit-verified; pilot NO-GO (structural, not timing).** Recomputed `N*`
  arithmetic explicitly against the plan's `F_R = T_tail·exp(1+2B)` rule
  using option-2's `B_finite(N=224)=20.1696367902`: reproduced the plan's
  q=5 `F_R=1.78e-6` from its own stated `T_tail`/`B`, confirmed
  `rho*^224=3.8904e-27` is *smaller* (not merely comparable to) q=5's
  `rho*^160≈1e-25`, and — extrapolating `T_tail(N)≈C·rho*^N` at q=5's
  measured order-of-magnitude prefactor `C≈4.6e-3` — got `F_R(224)≈1.6e-11`,
  ~5 orders below q=5's certified margin, so `N*=224` remains the consistent
  provisional freeze (non-rigorous scaling argument; the real `T_tail(N)`
  and `m0` need q=7's not-yet-built R2 envelope, stage 2b/2 of the plan).
  Added `--arcs i:j` to `certify_r3b_flagship.py`
  (`evaluate_closed_cover_parallel` gained an `arc_range` slice + chunk-mode
  status labels `CHUNK_ARCS_CLEAR`/`CHUNK_NOT_CLEAR` distinct from the
  whole-cover `CERTIFIED`/`NOT_CERTIFIED`) and a new
  `merge_chunks_and_verify_closure` seam-closure re-verification helper
  (checks contiguous tiling of the 192-arc base cover, then re-runs the
  adjacent-box winding polygon over the full merged, ordered arc set); both
  unit-tested (malformed/inverted `--arcs` rejected; synthetic seam-gap,
  under-tile, and record-count-mismatch chunk sets all correctly rejected;
  live q=5 base cover confirmed at 192 arcs, matching the plan's chunk
  table) — 122 insertions / 4 deletions,
  `.worktrees/aletheia-restore/code/tc_rerun/certify_r3b_flagship.py`.
  Pilot chunk 0 was **not run**: direct inspection of the runner found it
  hardcoded to q=5 (`ENGINE_PATH` → `zeta_cert_rosen_q5.py`, `EXACT_FACTORS`
  a 3-tuple, `N_PRIMARY/N_COMPARISON`=160/128, q=5 pin box, and
  `verify_immutable_inputs()` hash-pinning `lane_g`'s q=5
  `R2_FLAGSHIP_ENVELOPE_RECEIPT.json`/`TB_BLOCK_CERTIFICATES_V2_RECEIPT.json`
  — no q=7 analogs exist anywhere in the repo). Running against q=7 would
  either hard-fail the hash check or silently certify the wrong (q=5)
  problem; neither is an honest measurement, so no full or reduced pilot was
  attempted at any arc count, and no timing/memory/extrapolation figures
  were produced (the plan's unmeasured `~280 CPU-h` estimate is unchanged
  and not promoted). Verdict: NO-GO on stage 3 pending stage-1 (TB block
  certs) + stage-2 (R2 envelope) q=7 ports per `F7_CERT_PLAN.md` §2; GO on
  the CLI/seam-closure work in isolation (q-independent, no risk of baked-in
  q=5 assumptions). Report: `lane_f/F7_PILOT2_REPORT.md`. Not committed; no
  Kaggle kernels; no other lanes touched.

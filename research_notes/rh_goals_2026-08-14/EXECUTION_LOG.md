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

- **2026-08-15 — Lane F, q=7 certification stages 1 + 2 + 2b (PORTED AND RUN).**
  Ported the q=5 TB/W/R2 chain to q=7 at the ADOPTED radii
  `(3.522, 2.622, 2.372, 1.79, 1.6)` (`F7_MITIGATION_REPORT.md` §7). New
  scripts, all in `lane_f/` with an `f7_` prefix and all importing the q=5
  modules rather than forking them (`f7_tb_disc_sweep.py` — the 19-block
  source, captured from the authoritative `zeta_mayer_rosen.build_reduced_matrix`
  at q=7 and matching `F7_CONSTANTS_MANIFEST.md` §3;
  `f7_certify_tb_blocks.py`; `f7_certify_tb_weights.py`;
  `f7_certify_r2_flagship.py`; `f7_stage2_endpoint_B.py`; `f7_m0_prescan.py`;
  `f7_stage2_FR.py`). No q=5 file was modified.
  **Stage 1 PASS**: certified ρ\* ≤ **0.763212029206899202166157** (Arb, 384
  bits, M=512), worst block (5→3, +1, head) — the same block the float stage-0
  identified; gate re-targeted 0.70 → 0.80 per plan §2, with the rationale
  recorded in the receipt; all 19 blocks, all pole and branch-cut clearances
  pass; every tail family closed at the starting K=12. Float ρ\* 0.762251293807
  reproduced exactly as a NON-RIGOROUS cross-check.
  **W envelope** ported (schema `tb-weight-envelope-cert/v2`, q=7, κ=5, one box
  `g7_pin_1`): W^(≥1) = 7.0850126115, W^(0) = 6.5496061371. q=7 has no T-c
  stage, so the contour-comparison fields carry
  `NOT_APPLICABLE_NO_Q7_TC_STAGE` instead of a manufactured verdict.
  **Stage 2 CERTIFIED**: T_tail(224) ≤ 1.4792e−23, T_tail(238) ≤ 3.2636e−25,
  T_tail(256) ≤ 2.4115e−27; B_total (R2 column sum) = 119.0628556. Endpoint
  B_finite re-run and banked: 20.1696367902 (N=224, reproducing the mitigation
  report to every digit), 20.1696368694 (240), 20.1696369234 (256) — flat in N.
  **Stage 2b** m₀ = 3.313176e−06 (N=32, 96 sampled boundary points — NON-RIGOROUS,
  a sample not a cover). Decision rule `F_R = T_tail·exp(1+2B) ≤ 0.1·m₀`:
  **the plan's provisional N=224 FAILS it** (F_R = 1.33e−05 vs 3.31e−07); the
  rule is first met at N = 238 (×1.13 margin) and clears by ×153 at N = 256.
  **Verdict: GO for stage 3**, with N\* re-frozen to **N_PRIMARY = 256,
  N_COMPARISON = 224** (224 is now a justified NOT_CERTIFIED control arm).
  Contour cost re-estimate ~420 CPU-h, to be replaced by a measured pilot chunk.
  No structural blocker: the q=5 certification design generalizes to κ=5 /
  19 blocks unchanged. Report: `lane_f/F7_TB_R2_RECEIPTS.md`; receipts under
  `lane_f/f7_receipts/`. Not committed; no Kaggle; no other lanes touched.

## 2026-08-15 — F7 STAGE 4b UNBLOCKED (enlarged-contour re-optimization)

- **Blocker** (`f7_receipts/smoke/F7_R3B_SMOKE_CERT.md`): the stage-4b ENLARGED
  contour pushed six full-Markov head/tail blocks' ratios above 1 (worst 2.7353,
  `4→2, +1, head`), so `U_{B,k}` grew like ρ̂^k, the output-tail corrections hit
  7.07e+7 at N=256, and `F_R` overflowed to ~1.98e+61452309.
- **Root cause — a porting defect, not κ=5 geometry.** The enlargement rule
  `e_B = clearance_B/4` referenced only the pole/branch-cut clearance, never the
  disc's own radius. At q=7 the clearances are 1.0–4.4 while the radii are
  0.14–0.29, so a quarter-clearance is **2.4–6.3× the radius**. The q=5 analogue's
  flat `ε = 0.1` had been an implicit ~30–50% relative enlargement; the q=7 port
  silently left that regime.
- **Fix (5 lines, `f7_r3b_endpoint.py`)**: `e_B = min(clearance_B/4, CAP·R_i)`,
  `CAP = 0.15` (`"0"` restores the legacy rule; the rule + cap are written into
  every per-block record). **Radii unchanged** at the adopted
  `(3.522, 2.622, 2.372, 1.79, 1.6)` — deliberately, so d₅ = 1.6 and the
  endpoint tail-column-growth lesson are not regressed.
- Cap scan (Arb 384-bit, M=512, all 19 blocks): ρ̂ = 0.8635 (CAP 0.10),
  **0.9152 (0.15)**, 0.9682 (0.20), 1.0223 (0.25 — FAIL). Binding block is
  `5→3, +1, head` at every cap — the same block that binds the un-enlarged ρ\*.
- **All three gates PASS** (`f7_stage4b_reopt.py`, 174.7 s):
  1. un-enlarged **ρ\* ≤ 0.763212029206899202166157** < 0.80 — TB, W and R2
     receipts all re-run and reproduced **byte-identically**;
  2. **ρ̂ ≤ 0.9152411837446922** (rounded UP), all 19 enlarged ratios < 1,
     η ≤ 0.8695652173913044, all remaining clearances positive — *below* the
     q=5 chain's ρ̂ ≤ 0.9484;
  3. **B_same ≤ 20.1696369234** < 30 and flat (ΔB < 1.4e−7 over N=224→256).
     Output-tail corrections fell from 7.07e+7 to **7.71e−13**.
- **F_R** (= T_tail·exp(1+2·B_same)): 1.328761e−05 (224, fails), **2.931669e−07
  (238, PASS ×1.13)**, **2.166224e−09 (256, PASS ×153)** vs 0.1·m₀ = 3.313176e−07.
  m₀ stays NON-RIGOROUS (96-point N=32 sample), so this is the planning gate for
  freezing N\*, not a certificate. N\* = 238; frozen N_PRIMARY = 256 unchanged.
- **Verdict: GO for the Kaggle closed-contour launch.** Nothing upstream needs
  revision (radii, N\* freeze, and the 16-way chunk table all stand). The winding
  phase remains unexecuted — its ~420 CPU-h cost is still an estimate.
- Report: `lane_f/F7_4B_REOPT_REPORT.md`. New receipts:
  `F7_E1_ENLARGED_CONTRACTION_V2_RECEIPT.json`,
  `F7_R3B_ENDPOINT_V2_RECEIPT.json`, `F7_STAGE2_FR_V2_RECEIPT.json`.
  Old receipts kept; `f7_r3b_endpoint.py` sha256 moved
  `3ad7918899c70bda…` → `3d397de009122966…`, so the smoke receipts' recorded
  hash is now historical. Not committed; no Kaggle; no other lanes touched.

## 2026-08-15 — Lane G: LAW step-4 (uniform tail) attack scoping

- Deliverable: `lane_g/LAW_TAIL_SCOPING.md`. Scoping only — no certificate, no
  commit, no other lane's files. All claims labelled PROVED/CITATION/HEURISTIC/GAP.
- **Ranking: (d)+(a) merged > (b) > (a) alone > (c).**
- **Retired premise (important):** "G_q degenerates toward the parabolic/thin
  limit as q→∞" is FALSE. `vol(G_q\H) = π(1−2/q) → π` (bounded, no pinching),
  and the limit group `G_∞ = ⟨S,T_2⟩` is the theta group — **arithmetic**. What
  degenerates is the TRANSFER OPERATOR: `tr M_1 = λ_q → 2`, so the `n=1` branch
  generator goes elliptic → parabolic (indifferent fixed point).
- **Winner = Rouché/Hurwitz continuation from the λ=2 arithmetic anchor.** The
  anchor has a *provable, unconditional* off-line resonance at `s = ρ₁/2 ≈
  0.25 + 7.0673626 i` (M1F's g(s)=Λ(2s−1)/Λ(2s) factor + de la Vallée Poussin
  `Re ρ < 1`), and the perturbation parameter is explicit: `2−λ_q = π²/q² + O(q⁻⁴)`
  (0.0204 at q=22). Crux = **(T2)**: a determinant holomorphic in `(s,λ)` up to
  λ=2 whose λ=λ_q divisor is the Selberg divisor. Blockers stated: `κ_q → ∞`
  kills the *reduced* MMS operator as a λ-family; `{G_{λ_q}}` is a **discrete**
  family so Kato/Phillips–Sarnak perturbation theory does not apply to the groups.
- **(b) refuted as a tail route** (kept as the finite-base engine): certified/float
  `1−ρ*` = 0.3403 (q=5), 0.2177 (q=7), 0.1792 (q=8) → fits `q^{-1.33..-1.46}`
  (3 points, float, HEURISTIC), mechanism = the parabolic n=±1 branch. Also noted:
  Lemma B would not close an infinite tail even if true (link 1 is per-q).
  Transferable asset: the scale-free cap `e_B = min(clearance/4, 0.15R)`.
- **(c) = FALSE-FRIEND, closed on argument.** Onset's q≥22 uniformity is an
  explicit scalar inequality (`33/256 > 2arccos(2√6/5)/π`) whose margin is
  monotone to `δ_inf = 5.77e−5 > 0`; ours tends to 0. Plus `X_Ω` is an
  inf-over-invariant-measures essSup (L∞ support edge), not spectral.
- Data corrections banked: `δ_q` is **non-monotone** (0.0461, 0.0248, 0.0748 at
  q=5,7,8 — q=8 from the lane_k scan), and "lowest-Im pin" is a conditioning
  artifact, not a canonical family label.
- Next step (ticket `law-tail-anchor-probe`): Leg 1 — derive the `G_∞ = Γ_θ`
  two-cusp scattering matrix by M1F's moduli-count method, closing (T1). Leg 2
  (Probe D1) — narrow-box Arb scan at q=12,16,22 over Re∈[0.15,0.45],
  Im∈[6.6,7.6] and test whether a pin migrates toward `s_∞` like `q^{-2}`.
  Run Probe B1 (float disc optimizer at q=10..30) alongside to test the
  `1−ρ*` extrapolation.

## 2026-08-15 — lane_g LAW leg 1: (T1) Γ_θ two-cusp scattering matrix — **ANCHOR HOLDS**

Ticket `law-tail-anchor-probe.md` Leg 1. Deliverable:
`lane_g/LAW_ANCHOR_T1_THETA.md`. No commit; no other lane's files touched.

- **(T1) HOLDS.** `G_∞ = Γ_θ = ⟨S,T²⟩`: index 3 in PSL(2,Z), `vol = π` (matches
  the `(2,∞,∞)` triangle area — independent cross-check), **two cusps**: `∞`
  (width 2) and `1` (width 1), widths summing to the index. Derived by the M1F
  allowed-moduli constant-term method, run directly in `Γ_θ` with
  `σ_∞ = diag(√2,1/√2)`, `σ_1 = [[1,0],[1,1]]`:
  `Φ_θ = [[A,B],[B,A]]`, `A = g(s)/(4^s−1)`,
  `B = g(s)(2^s−2^{1−s})/(4^s−1)`, `g = Λ(2s−1)/Λ(2s)`;
  `det Φ_θ = g(s)² (4−4^s)/(4^s(4^s−1))`, which equals M1F's `φ⁺₂·φ⁻₂` (sympy, exact).
- **Load-bearing point survives an adversarial read.** The `s = ρ/2` poles come
  from the `Λ(2s)` denominator of `g²` (order `2m(ρ)`). The elementary factor
  `E = (4−4^s)/(4^s(4^s−1))` has **all** zeros on `Re s = 1` and **all** poles on
  `Re s = 0`, so it is finite and non-zero on `Re s = 1/4`. Four candidate
  cancellation channels (E, `Λ(2s−1)`, Γ-factors, zero coincidence) each excluded.
  With de la Vallée Poussin (`Re ρ < 1`): unconditional off-line resonance,
  `s_∞ = ρ₁/2 = 0.25 + 7.0673625708…i`, margin `η = 1/8` for the named `ρ₁`.
- **Self-checks all pass.** `Φ_θ(s)Φ_θ(1−s) = I` proved exactly (`g·g(1−s)=1`,
  `E(s)E(1−s)=1`, sympy) and numerically `< 5e−40` at 5 points (full 2×2, mpmath
  40 dps). `Res_{s=1}φ_{ab} = 1/π = 1/vol` for **all four** entries (exact + 9
  digits). Independent brute force over 26 318 elements of `Γ_θ` (entries ≤ 90)
  reproduces both moduli sets and both counts (`φ_E(2c)` on evens; `φ_E(n)`,
  `n` odd, at moduli `n√2`) — 12/12 digits on truncated Dirichlet series.
- **Pole signature confirmed (NON-RIGOROUS numerics).** `mean|det Φ_θ|` on circles
  about `s_∞`: `4.22e3 / 4.21e5 / 4.21e7 / 4.21e9` at `r = 1e−2…1e−5` — exact
  `r^{−2}` ⇒ order-2 pole; `(s−s_∞)²·det → −0.149433 − 0.393982 i` (finite,
  non-zero). Three controls clean (`|det| = 2.67, 5.38, 123`).
- **CORRECTION to `LAW_TAIL_SCOPING.md` §2.2 (write into lane text).** "`Γ₀(4)`,
  to which `Γ_θ` is conjugate" is **FALSE** — `[PSL(2,Z):Γ₀(4)] = 6 ≠ 3`. The
  correct conjugacy is `Γ_θ = V Γ₀(2) V^{-1}`, `V = [[1,0],[1,1]]` (proved via the
  mod-2 image: two conjugate order-2 subgroups of `S₃`).
- **HONEST DOWNGRADE of the anchor's strategic value.** `det Φ_θ = φ⁺₂φ⁻₂` is
  literally the object M1F already derived for `G_4 = Γ₀⁺(2)`. The `g(s)` factor
  and its `Re = 1/4` poles are common to **every** arithmetic member (`q = 4, 6, ∞`)
  and are `p`-generic in M1F — so the `λ=2` endpoint supplies an off-line
  resonance but **no mechanism distinguishing it** from the arithmetic interior.
  Meanwhile the repo's scanned `q = 7, 8` pins sit at `Re ≈ 0.42–0.48`, nothing
  converging to `Re = 1/4` at `Im ≈ 7.07` (HEURISTIC, inconclusive). Net: (T1) is
  closed, so **Probe D1 now carries the entire discriminating load** of the merged
  (a)+(d) route. Also: **no novelty claim** for `det Φ_θ` — the `Γ₀(2)` scattering
  matrix is the standard textbook example (obligation TN3).
- **Aristotle-able (v23) ledger:** T-1 index-3 mod-2 count; T-2 cusp inventory
  (widths + the `∞ ≁ 1` parity argument); T-3 the `V`-conjugacy and `Γ_θ ≇ Γ₀(4)`;
  **T-4 the two moduli-count lemmas (highest value, brute-verified to bound 90,
  no synthetic proof written)**; T-5 Euler-product restriction at `p=2` (= M1F A-4);
  T-6 the rational-function identities in `X = 2^s`; T-7 divisor of `E`;
  T-8 non-cancellation/order bookkeeping; T-9 the residue evaluations.
  **Not Aristotle-able:** the Selberg-zeta transport (M1F N2/G6, still GAP) and
  the Artin/induction shape check against PSL(2,Z) (non-load-bearing).
- 2026-08-15 — **v23 dispatch submitted**: `projects/aristotle_dispatch_v23/`
  (Lean/mathlib v4.28.0, modeled on v22). `ThetaGroupAnchor.lean` states
  sorry-stubbed finite/algebraic theorems for **T-1** (mod-2 `SL(2,Z)→S₃`
  reduction, index 3), **T-2** (cusp widths `2+1=3`, the `∞ ≁ 1` parity
  argument, `VTV⁻¹` parabolic), **T-3** (`V Γ₀(2) V⁻¹ = Γ_θ` matrix-identity
  family + `Γ_θ ≇ Γ₀(4)` via index `6≠3`), **T-4** (the two moduli-count
  lemmas, stated as the finite per-modulus counting bijection with `φ_E` as an
  unspecified imported totient — the reduction recorded in the doc-comment,
  per the task's fallback instruction), **T-6** (rational-function identities
  in `X=2^s` over `ℚ`), **T-7** (divisor of `E` via `4^s=exp(s·log4)`, finite
  nonzero on `Re s=1/4`), **T-9** (residue evaluations given `Res_{s=1}g=3/π`
  as hypothesis). **Skipped: T-5** (M1F A-4 Euler-product restriction — grepped
  the full `projects/aristotle_dispatch_v*` tree, no prior dispatch found; still
  skipped, since it is a genuine infinite Dirichlet-series identity, not
  finitely stateable — T-4 already carries its finite core) and **T-8**
  (non-cancellation order bookkeeping needs the full divisor of `Λ(2s)`, i.e.
  the nontrivial-ζ-zero multiplicity function `m(ρ)`, not available as a usable
  Mathlib API and not finitely stateable without draining the claim's content —
  see `SKIPPED.md`). Submitted via `aristotle submit --project-dir .`, project
  id `2fc741e0-31f6-4559-a8cc-b4200f6feb25`, not awaited.

## Lane F — q=7 R3b stage-3 Kaggle launch (2026-08-15/16)

- Stage 4b's enlarged-contour fix (`F7_4B_REOPT_REPORT.md`) verified: both
  hardcoded sha256 pins in `f7_certify_r3b_flagship.py` (R2, TB V2 receipts)
  already matched the live files — no pin edit was needed; the fixed
  `f7_r3b_endpoint.py`'s hash is computed live, never pinned, in that script.
- **One-arc smoke (`--arcs 0:1`, N=256/224, 4 workers): PASS.** 2622.9 s
  (43.7 min, under the 45-min ceiling). Base arc 0 at N=256 is FINITE and
  gate-passing (`chunk_gate_pass=True`, no subdivision needed); N=224's
  control arm fails on arc 0 exactly as designed (NOT_CERTIFIED below the m₀
  threshold, `F_R≈1.329e-5` reproducing the stage-4b report's table value).
- Built 16 self-contained private Kaggle bundles (`lane_f/kaggle_f7/`),
  `--arcs 0:12 .. 180:192` per the frozen chunk table. Each embeds its full
  dependency closure (zlib+base64, ≈275–285 KB, under Kaggle's 1 MB script
  cap) at the exact hardcoded absolute paths `f7_certify_r3b_flagship.py`'s
  import graph and hash pins require — discovered iteratively via three
  Kaggle-side `ModuleNotFoundError`/`FileNotFoundError` failures
  (`tc_rerun`, `lane_g/tb_disc_opt.json`, `f7_certify_r2_flagship.py`, etc.),
  each fixed and re-pushed until chunk 00 sustained `RUNNING` past 9.5 min
  (real compute, not an import crash).
- Extrapolated CPU-h/chunk from the smoke arc: ≈5.4 CPU-h optimistic /
  ≈10.7 CPU-h with a 2× subdivision buffer — no chunk needs splitting.
- **Pushed and RUNNING (5/16, Kaggle's concurrent-CPU-session cap):**
  `saarshai/f7-r3b-chunk-00` .. `f7-r3b-chunk-04`. **Queued (11/16, bundles
  built and verified, ready to push as slots free):** chunks 05–15, in
  order. See `lane_f/F7_STAGE3_LAUNCH.md` for the full slug/queue table and
  caveats.

## 2026-08-15/16 — Lane G leg 2: LAW tail falsification probes D1 + B1 (builder)

- **Probe D1 (narrow-box migration scan, q=12,16,22).** Ticket named
  `zeta_cert_rosen.py` (odd-q only); q=12,16,22 are all even, so the sibling
  even-q generalized builder `zeta_cert_rosen_even.py` was used instead
  (flagged, not silent). Two-stage midpoint scan (`N=16` grid → `N=48`
  Newton refine, `N=96` spot-check at q=22 — zero change, stable). Adopted
  pin per q = lowest-`absdet` candidate in the box (independent of distance
  to `s_∞`, checked to coincide with nearest-to-`s_∞` at q=16,22 — no
  selection bias). Distances to `s_∞ = 0.25+7.0674i`: `0.4161 → 0.2797 →
  0.1378` (q=12→16→22), **monotone decreasing**. `q^{-2}` fits best of the
  three tested exponents (SS_log 0.016 vs 0.056 for `q^{-4/3}` vs 0.138 for
  `q^{-1}`); free-regression slope `−1.83`. **Verdict: MIGRATION-CONSISTENT**
  (weak — 3 points, non-rigorous midpoint scan, no winding certificate — but
  unambiguous in direction and closer to `q^{-2}` than the alternatives).
- **Probe B1 (float disc-optimizer scaling curve, q=10,14,18,22,26,30).**
  Coarser search than the q=7 `f7_mitigation_stage0.py` run; corrected
  mid-run when a uniform-inflation start gave `ρ*≥1` for `κ≥6`
  (needs an F7-style large-near-1/small-near-κ profile — recorded, not
  hidden). `1−ρ*(q)`: `0.187 → 0.143 → 0.086 → 0.071 → 0.057 → 0.050`,
  monotone, no plateau through q=30. Fit `1−ρ*(q) ≈ 3.61·q^{-1.268}`,
  `R²=0.975` — shallower than the scoping note's 3-point range
  (`[−1.46,−1.33]`, q=5,7,8), but qualitatively the same story (decay
  continues, not `→ q^{-1.4}` plateau). **Verdict: closes (b) as a tail
  route (no plateau, no uniform `ρ_max<1`), exponent ≈ −1.27 this run** —
  confirms rather than overturns the scoping note's ranking.
- Full tables, residual breakdowns, and the builder-substitution rationale:
  `lane_g/LAW_PROBES_D1_B1.md`. Receipts: `lane_g/law_probes/`. Not
  committed (per instruction).

## 2026-08-15 — Lane G: LAW (T2) determinant — obstruction proved, route replaced

- **Deliverable:** `lane_g/LAW_T2_DETERMINANT.md`. Probe script + receipts:
  `lane_g/law_probes/probe_t2_shape.py`, `t2_shape.json` (L=5, r_max=7),
  `t2_shape_L6.json` (L=6, r_max=9). Not committed (per instruction).
- **(T2) as posed is STRUCTURALLY-BLOCKED**, with three `PROVED` obstructions.
  (a) **Lemma T2-A**: `ψ_1(z) = −1/(z+λ)` has fixed points on the unit circle
  with multiplier of modulus 1 for **every** `λ ∈ (0,2]` (elliptic for `λ<2`,
  parabolic at `λ=2`), so by Denjoy–Wolff/Schwarz **no disc** satisfies
  `ψ_1(cl D) ⊂ D`. The unreduced fixed-disc operator that
  `LAW_TAIL_SCOPING.md` §2.2 named as B-I's rescue **does not exist at any
  `λ`**, not merely at the endpoint. Corollary T2-A′ (exact, verified at
  `q=8,10,12,14,20,22,30,50`): for even `q`, `ψ_1^{q/2}(−λ_q/2) = ∞`.
  (b) **Lemma T2-B**: `ψ_1 = R = S T_λ` **is** the group's elliptic generator,
  of order `q` at `λ_q` and infinite order at `λ=2` — so the *induced*
  alphabet `{ψ_1^k ∘ ψ_n}` is finite (`|k| < q`) at every `λ_q` and infinite
  at `λ=2`, its cardinality being the denominator of the rotation number
  `ν(λ)=arccos(λ/2)/π`. **Inducing is anti-rescue.**
  (c) **Lemma T2-C**: any λ-independent index set (branch alphabet, or words
  in `Z/2 * Z`) has **infinite fibres** at every `λ_q` because `R^q = 1`.
  B-I and B-II are therefore **one** obstruction, not two.
- **Bonus mechanism (explains two open puzzles).** The parabolic `k`-sum at
  `λ=2` **is** `ζ(2s)` — the same `ζ(2s)` whose zeros give the anchor's
  `s=ρ/2` poles via `g = Λ(2s−1)/Λ(2s)`. At `λ_q` that sum is **truncated at
  `k ≍ q`**, so there is no exact `ζ(2s)` factor and hence **no exact pole at
  `s_∞`** — which is why `LAW_ANCHOR_T1_THETA.md` §6.2 found no `q=7,8` pin at
  `Re=0.25` and why D1's pins only *migrate* toward `s_∞`. `HEURISTIC`.
- **Replacement (T2′), CONSTRUCTIBLE.** `{λ_q}` is a *sequence*, so
  **Vitali + Hurwitz replaces Rouché**: no interpolation, no non-group `λ`,
  and **the transfer operator leaves the tail argument entirely** (it is
  needed only for the certified finite base). New crux = **U1**, a
  `q`-uniform order-2 growth bound on `Z_{G_q}`, structurally available
  because `vol(G_q\H) = π(1−2/q) ≤ π` makes the Weyl counting uniform.
- **Numeric probe (NON-RIGOROUS, float64).** The brief's requested probe
  (`det(1−L_{s,λ})` at `λ=1.8,1.9,1.95,2.0`) is **not well-posed** given
  Lemma T2-A — flagged, and redirected. What was run instead: BFS enumeration
  of primitive hyperbolic conjugacy classes of `G_q = Z/2 * Z/q` and of
  `Γ_θ = Z/2 * Z` (the requested `λ` grid ≡ `q ≈ 7, 10, 14, ∞`, all included).
  Results: **`Z_{G_q}(s) → Z_{Γ_θ}(s)` for `Re s > 1` at rate `q^{-2}`**
  (fitted exponents `−2.10/−2.15/−2.18` at three `s`; `< 0.05` change when the
  geodesic count is nearly tripled). Systole: `sys = 2 arccosh λ` **exactly**
  (`PROVED`, class `[S R²]`), gap `= (2/√3)(2−λ_q) + O(ε²)`, measured ratio
  `1.15529` vs `2/√3 = 1.154701`; **monotone increasing ⇒ no pinching**.
  Three independently computed quantities — systole gap, `|Z_q − Z_θ|`, and
  D1's pin migration — all scale as `q^{-2} ≍ (2−λ_q)`.
- **Literature scout (5 questions, honest):** Ruelle 1976 / Fried 1986 /
  Isola 2002 / Wolpert 1992 retrieved and all **inapplicable** as stated.
  **No** published result on (a) jointly-`(s,λ)`-holomorphic determinants
  across a Markov-structure change, (b) spectral behaviour under cone-angle→0
  at bounded area, (c) `lim_{q→∞}` of Hecke spectra/zeta. Re-confirms
  `LAW_TAIL_SCOPING.md` §1.1 — and means **no import will do this for us**.
- **Retire from lane text:** the "unreduced operator may rescue B-I" line
  (`LAW_TAIL_SCOPING.md` §2.2); the framing of B-I/B-II as two blockers;
  "(T3) is a routine Cauchy estimate".
- **Next tickets, in order:** (1) **U3** — scattering-pole → Selberg-zero
  transport for `Γ_θ` (M1F N2/G6, inherited, blocks **both** formulations,
  textbook-shaped, cheapest); (2) **U1** — the `q`-uniform Hadamard bound
  (the real work); (3) **U2b** — uniform systole + geodesic counting.
  **Do not fund further work on a two-variable determinant.**

## 2026-08-15 — Lane G: LAW obligation **U3** — scattering-pole → Selberg-zero transport — **CLOSED**

- **Deliverable:** `lane_g/LAW_U3_TRANSPORT.md`. Probe script:
  `lane_g/law_probes/probe_u3_orders.py` (mpmath, 40 dps). Not committed.
- **Verdict: CLOSED-BY-CITATION *and*, independently, CLOSED-WITH-PROOF.**
  `Z_{Γ_θ}` has a zero at `s_∞ = ρ₁/2 = 0.25 + 7.0673625708673468952…i` of
  order **exactly `2·m(ρ₁)`**, hence **≥ 2** unconditionally and **= 2** given
  `ρ₁` simple. This is exactly the input `LAW_T2_DETERMINANT.md` §3.2's
  Hurwitz step consumes. **U3 = C14 (T1) = G6/N2 (M1F) is discharged.**
- **The divisor identity, found and quoted verbatim (this is what M1F §6.1's
  scout failed to find):** Bruggeman–Fraczek–Mayer, *Perturbation of zeros of
  the Selberg zeta-function for `Γ₀(4)`*, **Exp. Math. 22 (2013) 217–242**,
  §3.4(b): "*At points with `Re β < ½` and `Im β > 0` the function `Z(α,·)` has
  **a zero of the same order as the zero of the determinant of the scattering
  matrix at `1 − β̄`***" — attributed there to **Hejhal LNM 1001 vol. II,
  Chapter X, Theorem 5.3, p. 498**. Corroborated by the full 7-item divisor of
  `Z_Γ` in Friedman–Jorgenson–Smajlović, **LMP 111 (2021) art. 15**, §2.5
  (standing hypothesis "*possibly with elliptic fixed points*"; cites Venkov
  1990 p. 49 and Hejhal vol. II p. 499), whose **item 6 is U3**.
- **M1F obligation N2 discharged in content.** The Selberg-zeta functional
  equation M1F §5.2 assumed only the *shape* of is found in closed form, for
  exactly our class (cofinite, cusps **and ramification points**): Teo,
  **LMP 110 (2020) 61–82**, Prop. 2.5 — `Z(1−s) = κ(s)Z(s)` with `κ` = const ×
  `e^{C(2s−1)}` × `φ(s)` × `sin`-powers (elliptic) × Barnes-`Γ₂` factor
  (identity) × `[Γ(3/2−s)/Γ(s+½)]^n` (parabolic). Every factor but `φ` has all
  its zeros and poles **on the real axis**, so `ord_{s₀}Z = −ord_{s₀}φ` for
  non-real `s₀` with `Re s₀ < ½`. **Second, independent proof of U3.**
- **Hazard found and removed.** The classical statement is about the
  **conjugate** point `1 − β̄`, not the pole at `β`. Rather than import
  "`φ` is real on `R`", `det Φ_θ` was evaluated at `1 − s̄_∞ = (1+ρ₁)/2`
  **directly in closed form**: `Λ(2s−1) = Λ(ρ₁) = 0`, `Λ(2s) ≠ 0,∞`, `E` finite
  and non-zero on `Re s = 3/4` ⇒ **order-2 zero**, confirmed numerically
  (`det/(s−w)² → −0.841624 − 2.218948i`). The transport is applied in the exact
  form in which it is stated.
- **Half-integer / trivial-divisor exclusion made explicit, as asked.**
  `Im s_∞ = 7.0673625708… ≠ 0`, and **every** non-resonance divisor point of
  `Z_Γ` is real (topological poles on `½ − N₀`; `s = ½`; trivial zeros on `−N₀`,
  which is also where the **elliptic** contribution of `S` lands; small-eigenvalue
  and residual zeros). Decisively: `Z_Γ` is **pole-free off the real axis**, so no
  coincident pole exists to cancel the zero.
- **`G_q` version: pure citation, no per-`q` input.** `G_q` is cofinite
  (`vol = π(1−2/q)`), one cusp, elliptic orders `{2,q}` — the same theorem
  applies verbatim for every `q`. **Honest limitation:** the poles of `φ_q` are
  unknown for non-arithmetic `q` (Phillips–Sarnak), so (U3-q) has no known
  input — **but it is not needed**: under (T2′) the `q`-side zeros come from
  Hurwitz, and U3 is consumed **only once, at the anchor `Γ_θ`**.
- **Correction owed to `LAW_ANCHOR_T1_THETA.md` §4.4** (non-load-bearing):
  the poles of `det Φ_θ` at `s = ikπ/log 2` are **simple**, not "order 2 in `E`"
  (`r·E → 3/(2 log 2) = 2.164042`, `r²·E → 0`). So `Z_{Γ_θ}` has **simple**
  zeros there.
- **Citation hygiene still owed (V1–V3, none blocking):** open Hejhal LNM 1001
  vol. II p. 498–499 (Ch. X Thm 5.3) and Venkov 1990 p. 49 to confirm the
  numbers and item 6's multiplicity; confirm Teo's journal numbering. **Note
  for the lane text: the divisor + functional equation of `Z_Γ` are in Hejhal
  vol. II Chapter X, ~pp. 498–499 — not "ch. 6+" or "ch. 11" as M1F guessed.**
- **Next, unchanged and now unblocked:** **U1** (the `q`-uniform order-2 growth
  bound — the real crux), then **U2b** (uniform systole + geodesic counting).

---

## 2026-08-16 — Lane G, obligation **U1** (q-uniform growth bound): `LAW_U1_GROWTH.md`

**Verdict: U1-OPEN-REDUCED, GUARD-ADVERSE. The (T2′) tail route is now AT RISK.**
Deliverable `lane_g/LAW_U1_GROWTH.md`; probes `lane_g/law_probes/probe_u1_growth.py`,
`probe_u1_sup.py`, `u1_stab.py` with receipts `u1_growth.json`, `u1_sup.json`,
`u1_sup_q40.json`, `u1_stab.json` and logs. Nothing committed; `lane_f` untouched.

- **The hypothesis is weaker than advertised.** (T2′-a)'s exponential order-2 shape is never used:
  Vitali needs only local uniform boundedness, and `Ω̃` can be chosen with bounded imaginary part.
  **U1 ⟺ boundedness on ONE compact `0.6 × 1.6` rectangle** plus `Re s ≥ 3/2`, where the Euler
  product already gives `|Z_{G_q}| ≤ e^{0.19144} = 1.211` uniformly (measured, monotone decreasing
  in `q`, maximised at `q = 5`). `PROVED` / `HEURISTIC` respectively.
- **The brief's named danger — the order-`q` elliptic data — is SETTLED, and it is harmless on `U`.**
  Exact identity `E_q(s) = Z_{ell,q}(s)/Z_{ell,q}(1−s)` (`PROVED`), `|E_q(1/2+it)| = 1` (`PROVED`),
  and `log E_q(s) = (2s−1) log(q/2π) + log(Γ(1−s)/Γ(s)) + O(1/q)` (identified numerically to 4 dp
  at 7 points, `q ≤ 4800`, `O(1/q)` residual confirmed by exact halving). Hence `|E_q| ≤ C` and
  `→ 0` on `U`. **But it grows like `q^{2Re s−1}`, i.e. `≍ (q/2π)³` at `Re s = 2`** — so any route
  through the functional equation at `Re s = 2` imports a `q³`.
- **The brief's named fallback — renormalise by `C(q)` — is REFUTED.** If `C(q) → ∞` then
  `Z_{G_q}/C(q) → 0` on `Re s > 1` (since `Z_{G_q} → Z_{Γ_θ} ≢ 0` there), so Vitali forces the
  limit `≡ 0` and Hurwitz says nothing. `PROVED`. **U1 has no soft landing.**
- **Correction owed to `LAW_T2_DETERMINANT.md` §3.3.** Uniform Weyl counting is NOT free from
  `|F_q| ≤ π`. Only the `T²` coefficient is uniform. The elliptic mass
  `M(q) = Σ_k 1/(2q sin(kπ/q)) = (1/π) log(2e^γ q/π) + O(q^{−2})` (`PROVED` numerically, 5 dp,
  `q ≤ 10⁴`) enters the **linear** coefficient: at `T ≈ 8` the `T²` term is `≈ 16` and the elliptic
  term `≈ 17.6` at `q = 1000` — **the same size**. Also `N + M` is the *winding*, not the resonance
  count.
- **U1 reduces to ONE obligation, `(U1-φ)`:** either `|φ_q(2+it)| = O(q^{−3})` (cancelling the
  elliptic `q³`), or a `q`-uniform resonance count on `|s − 1/2| ≤ 8`. Every standard route —
  FE+convexity, Hadamard+counting, Landau's `Z'/Z`, Borel–Carathéodory — was checked and all end
  there; three were shown to be circular or impossible without it (`PROVED`).
- **Falsifiable prediction (5.1):** if U1 holds globally, `φ_q(s) ≍ (π/q)^{2s−1} φ_θ(s) ·
  Γ(s)Γ(3/2−s)/(Γ(1−s)Γ(1/2+s))`. Testable against Hejhal, Memoirs AMS 469 (1992).
- **THE ADVERSE RESULT.** `sup_{∂U}|Z_{G_q}|` was measured with the certified even-`q` Rosen/MMS
  determinant (both `P`-sectors, product), `q = 12, 16, 22, 30, 40`. Dropping `dU_4` (`Re s = 0`,
  exactly on `∂Ω*`, outside R5's identification domain), the sup **increases monotonically**:
  `25.14 → 49.47 → 92.81 → 99.40`, log-log slope **`+1.50`** (`q = 16 → 40`). **U1 requires slope
  `0`.** The slope is the shape the *trivial* `|φ_q| ≤ 1` estimate predicts (`O(q^{2−σ})`).
  **Not a discretisation artefact:** `N = 32, 48, 64` agree to all 9 printed digits at
  `dU_2, dU_3, dU_4, dU_5` for `q = 30`. Caveats: 5 points, ragged per-point pattern, and the proxy's
  identification with `Z_{G_q}` is itself obligation **U4** (`GAP` for `q ≠ 5`).
- **Bonus, unasked:** `|det(1−L^+)·det(1−L^−)|` matches the truncated Selberg Euler product to
  `3e−4 … 2e−3` at two control points with `Re s > 1`, for `q = 12, 16, 22, 30, 40`. **First
  general-`q` numerical evidence for U4** — the repo had it only at `q = 5` (R5).
- **[CORRECTION 2026-08-16]** The two bullets above quote the repo determinant *numerator*
  as if it were `Z_{G_q}`. The MMS identity is
  `det(1−L^+)·det(1−L^−) = Z_{G_q}·det(1−K_q)`, not `= Z_{G_q}`; the repo builders omit the
  `det(1−K_q)` divisor. `det(1−K_q) = Π_{n≥0}(1 − b_q^{s+n})` is **zero-free on `Re s > 0`**,
  so no zero-location claim moves. Magnitudes do: the excl.-`dU_4` guard column
  `25.14 → 49.47 → 92.81 → 99.40` becomes `33.32 → 45.95 → 56.45 → 61.59` and the log-log
  slope `+1.50` becomes **`+0.67`** (endpoint `+0.670`, LSQ `+0.673`) — **still positive,
  the ADVERSE verdict stands.** The U4 bonus *strengthens* (8 of 9 control-point residuals
  improve) once the identity is restated with the divisor. Receipt:
  `lane_g/law_probes/q3impact_u1_sup_corrected.json`; see
  `lane_g/LAW_Q3_BRANCH_DIAGNOSIS.md` (Q3D.2/Q3D.7) and `lane_g/LAW_DETK_IMPACT_AUDIT.md`
  (§3.2, §4). Text above left as originally logged.
- **Next, and the order has CHANGED:** (1) **extend the guard to `q = 56, 72, 100`** — two more `q`
  decide whether (T2′) is alive; cost is background hours, and the answer gates everything else.
  (2) Test prediction (5.1) against Hejhal Memoirs 469. (3) **U2b** — still cheap, still worth
  closing, but **no longer on the critical path**.

## M1G v2 (2026-08-16, builder pass)

- **Item 2 delivered:** `code/zeta_cert_rosen_even.py` (worktree
  `aletheia-restore`) gained a `determinant_sector="trivial"|"chi"` kwarg on
  `cert_det`/`winding_box`, via new local `_det_block_signed` /
  `dim_tail_from_matrix_signed` (Q5's shared primitives untouched). Fixes the
  v1 `TypeError: winding_box() got an unexpected keyword argument
  'determinant_sector'` blocker. Verified functional at small N and at a
  full N=60/K=24/400-bit run (q4 k2 chi point, wall 145.6s).
- **Item 1 NOT delivered.** R3b's proven tail bound is q=5-specific: it rests
  on a multi-day per-disc contraction-margin search
  (`ta_recon.py`/`tb_disc_sweep.py`/`tb_disc_opt.py`) that found the naive
  uniform-safety scheme fatal (a full Markov branch onto the target disc,
  ratio exactly 1) before any lemma chain could be written. No equivalent
  search/proof exists for q=4/q=6's even-q geometry. Faking an analogous
  formula was rejected as dishonest; flagging as its own follow-on ticket.
- **Item 3: 1/8 sampled.** New chi-sector point q4 k2
  (`2i*pi/log(2)`, N=60, K=24, box half-width 0.001) isolates winding **0**,
  not the predicted 1 — an open discrepancy (box escalation vs. sign/
  normalization convention question), not resolved; stopped per the
  two-failed-attempt rule rather than iterating blindly. Remaining 7 boxes
  not run (would only add more heuristic-tail samples pending item 1).
- Receipts/report: `lane_g/m1g_receipts/q4_chi_k2_v2.json`,
  `lane_g/M1G_V2_THEOREM_GRADE.md`. Verdict unchanged at 0/8
  CANDIDATE-CERTIFIED (v1 was 0/8 CERTIFIED).

## 2026-08-16 — Lane G: SECOND_PIN_PREP (prep only, ticket second-g5-pin)

- Prepared (NOT executed) the certification package for a second G_5 pin at
  `0.24302842340131198 + 10.560296779143401 i` (N=22 value; scan source
  `resonance_v2.json g5_even_localization[9]`, winding=1 at scan level).
  Deliverable: `lane_g/SECOND_PIN_PREP.md`.
- Reuse verdicts vs the flagship R3b chain: TB V2 blocks, E1 enlarged, and the
  K_s gate are box-INDEPENDENT and reusable verbatim (sha pins stand); W V2
  envelope, R2 envelope, and the endpoint B bound are box-LOCAL and must be
  re-run — all degrade at the new box (p: 0.908 → 0.486, |t|: 5.76 → 10.56).
- K_s gate at the new pin: exact lattice Re ≤ 0 covers it; point clearance
  **0.481952** (rounded down; NON-RIGOROUS float re-eval of the flagship metric)
  — larger than the flagship's own 0.455100. CLEAR.
- Plan: Phase 0 re-pin at N=22/28/36/44 (scan re_spread 4.5e-6 exceeds the 1e-6
  half-width — box not yet freezable); Phase 1 box-local receipt re-runs in
  copies; Phase 2 local smoke arc (~7 min); Phase 3 16-chunk Kaggle run reusing
  the lane_f kaggle_f7 pattern (~17–27 CPU-h, NON-RIGOROUS flagship
  calibration); Phase 4 merge (helper currently REJECTS subdivided chunks —
  flagship needed 92); Phase 5 control arm + assembly.
- Blockers recorded (B1–B8): box freeze, F_R closure at N=160 not inferable,
  merge-helper subdivision rejection, bundle generator rewrite, hash-pin
  plumbing, K3 latent-hazard guards, V1 convention sensitivity, live-lane
  constraints. No compute run; no receipts touched; nothing committed.

## 2026-08-16 — Lane G: (U1-φ) prediction test — `lane_g/LAW_U1PHI_TEST.md`

- Ran the second deciding test for the LAW tail: the falsifiable prediction (5.1) of
  `lane_g/LAW_U1_GROWTH.md`, `|φ_q(2+it)| = O(q⁻³)` (obligation **U1-φ-a**).
  Independent of the running sup-guard extension; `law_probes/u1_guard_extended.*`
  and `lane_f` untouched; nothing committed.
- **Literature: NEGATIVE and honest.** Hejhal, *Eigenvalues of the Laplacian for Hecke
  triangle groups*, Memoirs AMS 469 (1992) — existence confirmed, **text not obtained**
  (AMS paywall); likewise Hejhal ASPM 21 (1992) and Winkler (1988). No explicit `φ_q`,
  no table, no cusp-width normalisation factor, and no `q → ∞` asymptotic was retrieved
  for non-arithmetic Hecke groups anywhere. **Nothing imported; nothing attributed.**
  `LAW_U1_GROWTH.md` §9's "literature lookup plus one plot" is not executable at this
  access level, so the test was redesigned onto the repo's own machinery.
- **Derivation.** (5.1) re-derived from scratch by comparing Teo Prop. 2.5 for signature
  `(0;1;2,q)` against `(0;2;2)` — exact match including the `π` (= `2π` from `E_q`'s
  asymptotic ÷ `2` from the cusp-count difference `C = −n log 2`). The Γ-skeleton
  satisfies `R(s)R(1−s) = 1` identically (verified to `1.1e−42`), i.e. it is exactly
  unitarity-compatible — the provable-today half. **New: Lemma U1φ-1, `(U1-φ-a) ⟺ U1`**
  (the parent note recorded only sufficiency), which is what made this a deciding test.
- **Method.** On `Re s = 1/2`, `κ_q = exp(−2i·arg Z_q)`, so one determinant evaluation per
  point gives the whole functional-equation kernel and `Re s = −1` is never visited. All
  factors have modulus 1 there, so (5.1) becomes a pure **phase** statement — disjoint from
  what the sup-guard (a modulus) can see. Probe `law_probes/probe_u1phi.py`, N=32, 400-bit,
  two heights `t = 1.5` (10 `q`) and `t = t_∞ = 7.0674` (8 `q`), `q` even, 12…40.
- **VERDICT: PREDICTION-CONSISTENT. Fitted exponent −3.08 (LSQ) / −3.07 (endpoint), vs
  predicted −3, vs null 0.** Model-free: the null demands a monotone 17.02 rad phase drift
  at `t = t_∞`; observed span is 2.02 rad and non-monotone — factor 8.4 too small, wrong shape.
- **Caveats reported, not buried.** The pure-power ansatz *alone* is refuted (slope ratio
  1.37 vs the required 4.71); it is repaired by a `t`-independent additive drift `δ ≈ −0.71`,
  and that two-height repair (`α = 1.026`) is a **zero-degree-of-freedom fit**. Single-height
  fits disagree (−3.79 vs −3.23) and a `γ/q` robustness term flips the slope's sign at
  `t = 1.5`. All float, midpoint, no certificate; the object measured is the transfer-operator
  proxy, so **U4 is promoted** — it now carries a phase, not just a modulus.
- **Unasked-for, and it corrects a parent note.** Broke `u1_sup.json` down **per point** for
  the first time: of the eight `∂U` points, **five decrease** in `q`, and the `+1.50` rise is
  confined to `Re s ≤ 0.0732` — the two points on/beside `∂Ω*` where R5 gives no identification.
  At `Re s = 1/2` the slope is **−0.78**. `LAW_U1_GROWTH.md` §7.3's "the quantity U1 asserts to
  be bounded is growing" over-reads its own data; correction owed there.
- **Also new:** `arg P_q(2.0) = 0` exactly at 14 values of `q`, so the determinant proxy carries
  no spurious `q`-dependent phase (never checked before — earlier probes used `|P_q|` only);
  and `|P_q|` reproduces `u1_sup.log`'s control column to all printed digits on a different
  interpreter.
- **Next, cheapest first:** a **third height** `t = 3.5` (~25 min) to give (4.1) a degree of
  freedom and test `δ`'s `t`-independence; then pin `δ` from the closed-form `t`-independent
  factors of `κ_q`; then extend to `q = 56, 72`. Hejhal Memoirs 469 remains owed to a human
  with library access.

---

## 2026-08-16 — Lane G: **U2b CLOSED** (both halves), and two corrections to `LAW_U1_GROWTH.md` §2.3

**Artifact:** `lane_g/LAW_U2B_CLOSURE.md`. Probes: `lane_g/law_probes/u2b_normal_form.py`,
`u2b_systole.py`, `u2b_monotone.py`, `u2b_counting.py`, `u2b_direction.py` (+ `.json` receipts).
Nothing committed; `lane_f/` and `law_probes/u1_guard_extended.*` untouched.

- **One mechanism did both halves.** In the free-product normal form `G_q ≅ Z/2 * Z/q`,
  `S R^a = −M_a` with `M_a = [[u_a, u_{a+1}],[u_{a−1}, u_a]]`, `u_j = sin(jπ/q)/sin(π/q)` —
  **entrywise nonnegative, `det = 1`**. So `|tr w|` is a sum of nonnegative path products and
  every bound is "keep one path". Verified in **exact integer-polynomial arithmetic** (`a ≤ 25`).
- **(a) SYSTOLE — `PROVED`.** `min |tr γ| = 2λ_q` over primitive hyperbolic `γ ∈ G_q`, `q ≥ 4`,
  equality **iff** `[S R^{±2}]`. Hence **`sys(G_q) = 2 arccosh λ_q` exactly**. Exhaustive check:
  **1 508 638** primitive cyclic words at 18 levels `q = 3…100`, five independent checks, all
  pass. The same proof returns the classical `sys(PSL(2,Z)) = 2 arccosh(3/2)` at `q = 3` — an
  independent confirmation the mechanism is right. **Discharges `LAW_U1_GROWTH.md` U1.4 and
  `LAW_T2_DETERMINANT.md` §3.4's `HEURISTIC`**; the collar-lemma `GAP` there is now moot.
- **No citation closes it.** Literature scout (Schmidt–Sheingorn Math. Z. 220 (1995),
  Haas–Series J. LMS 34 (1986), Schmutz Schaller) found **no published systole of `G_q`**.
  Schmidt–Sheingorn is paywalled and remains a `TODO-VERIFY` on **priority**, not correctness.
- **CORRECTION 1 — Conjecture U1-2 is FALSE as literally stated.** `|tr w(λ)|` is *not*
  nondecreasing on `(1,2]`: `|tr(S R⁵)| = 2|λ⁴−3λ²+1|` runs `2.00 → 2.50 → 0 → 10` across
  `λ = 1 → 1.2434 → λ₅ → 2`. The **correct** version is a theorem, proved here: monotone on
  `[2cos(π/(A+1)), 2]`, `A = max|a_i|` — exactly the levels `q ≥ A+1` where the word is
  normal-form. The 19 765-pair test was restricted to faithful lifts and so never entered the
  false region; the test was right, the statement it was read as supporting was not.
- **CORRECTION 2 — the `Γ_θ` comparison inference is backwards, and it is load-bearing.**
  `ℓ_w(λ_q) ≤ ℓ_w(2)` gives *shorter* `G_q` geodesics, hence **more** below `L`:
  `N_q(L) ≥ N_θ(L)`, not `≤`. Measured independently: `N_θ(4) = 7` (matching the parent note
  exactly) against `N_q(4) = 10, 10, 11, 9, 7, 7, 7`; `N_q ≥ N_θ` at **all 21** `(L,q)` pairs.
  §2.3's "crossover at `q ≈ 22`" is equality reached **from above**. Consequence: the
  "multi-syllable non-faithful excess" the brief asked to bound is **dissolved, not deferred** —
  no bound on it could have worked, because the inequality it repairs points the wrong way.
- **(b) COUNTING — `PROVED` directly, at a stated price.** Two path bounds
  (`|tr w| ≥ 2∏_{heavy}u_{a_i}` and `|tr w| ≥ λ^k∏p_j` over maximal light runs) interpolate to a
  block-multiplicative bound, giving `Σ|tr|^{−2σ} ≤ 2^{−e_h}log(1/(1−W_q))` with
  `W_q = Σ_{a=2}^{q−2}u_a^{−e_h} + 2λ_q^{−e_l}ζ(e_l)`. Result: **`S_q(σ) ≤ 0.4861` and
  `|Z_{G_q}(s)| ≤ 1.6259` for `Re s ≥ 3.5`, every `q ≥ 5`**, explicit constants.
- **The price, stated plainly.** The method's convergence floor is **`σ₀ = 3.05`, not `3/2`**
  (`sup_q W_q = 4.99` at `σ = 3/2`). Lemma U1-0 is restated and re-proved for a general
  threshold (§4.4) — harmless, since Vitali needs only accumulation points, not all of
  `{Re s > 1}` — but the compact rectangle grows `0.6×1.6 → 0.6×3.6`.
- **The one liability created for another lane.** With `σ₀ = 3.5` the functional-equation
  reflection moves to `Re s = −2.5`, so **(U1-φ)'s exponent becomes `q^{−(2σ₀−1)} = q^{−6}`,
  not `q^{−3}`**. `LAW_U1PHI_TEST.md` fitted `−3` at `Re s = 2`. **`TODO-VERIFY`: re-run
  `probe_u1phi.py` at `Re s = 3.5`** — one abscissa change, and it is the cheapest next step.
- **Remaining `GAP`s, both small.** `sup_q W_q < 1` verified at 44 values `q ≤ 3000`, not proved
  for all `q` (both ingredients are already proved above — a writing gap, Aristotle target A4).
  Recovering `σ₀ = 3/2` needs `tr(∏M_{a_i}) ≥ ∏ρ(M_{a_i})`, which is false for general
  nonnegative `SL₂` matrices but may hold on this never-diagonal family; not attempted, not urgent.
- **Aristotle-able, numbered in `LAW_U2B_CLOSURE.md` §6.** A1 (the Chebyshev normal form —
  exact, short, and everything depends on it), A2 (trace ≥ any nonnegative cyclic path product),
  A3 (the systole theorem given A1+A2), A6 (the counterexample). A5 (`t cot t` antitone) is the
  one item that is genuinely analysis; A4 follows from it. **A1 is worth submitting alone.**
- **U2b was never the crux, and closing it does not move the crux.** (U1-φ) is untouched.

---

## 2026-08-16 — Lane G — (U1-φ) PROOF ROUTE: the crux is REFUTED, and relocated
**Artifact:** `lane_g/LAW_U1PHI_PROOF_ROUTE.md`.
**Probes:** `lane_g/law_probes/u1phiproof_eisenstein.py|.json`, `u1phiproof_kappa.py|.json`.
**Brief:** rank routes 1–3 for proving (U1-φ-a), attempt the best. **Verdict: BLOCKED —
(U1-φ-a) is FALSE. Status: REDUCED-TO-(U1-φ-a′) on `σ ∈ (3/4, 1)`.**

- **Route 3 (Eisenstein column direct) won, and it decides the question with the sign reversed.**
  `φ_q` is *computable* for every `q` — arithmetic or not — from the allowed-moduli constant-term
  formula the repo already imports as `M1F_EISENSTEIN_DERIVATION.md` (3.2). It is a Dirichlet
  series with **non-negative** coefficients on `Re s > 1`. The brief's "trivial bounding by
  positivity" works — and yields a **lower** bound.
- **Lemma E2 (`PROVED`).** After scaling the width-`λ_q` cusp to width 1, the least modulus is
  exactly `λ_q < 2` with multiplicity exactly `1` (all `c = 1` elements are `T^αST^δ`, one double
  coset). Confirmed at 15 levels `q = 3…100`.
- **THEOREM E3/E4 (`PROVED`).** `|φ_q(σ+it)| ≥ c(σ) > 0` uniformly in `q`, for every fixed
  `σ > 1`. Hence **(U1-φ-a) is false**: measured `q`-slope of `|φ_q|` is **`−0.054`** at `σ = 2`
  and **`−0.096`** at `σ = 3.5`, against the required `−3` and `−6`; shortfall at `q = 100` is
  `3.6e4` and `4.8e9`. Machinery validated to `1.1e−8` against `g(s)`, `φ_4`, `φ_6` at `q = 3,4,6`.
  Independent corroboration: `Res_{s=1}φ_q = 1/(π(1−2/q)) → 1/π ≠ 0`.
- **Route 2 (FE) is dead for every admissible threshold, and dead in the strong sense.** With
  `E_q` evaluated exactly, `|φ_q E_q|` has log-log slope **`+1.37`** at `σ₀ = 2` and **`+2.71`**
  at `σ₀ = 3.5` where `O(1)` is required; combined with U2b Theorem C's lower bound this **proves**
  `|Z_{G_q}(1−σ₀−it)| → ∞`. The left edge is not badly estimated — it is unbounded. And the right
  edge cannot move to `σ₀ ≤ 1`: the Selberg Euler product's abscissa is `1`.
  **U2b's `TODO-VERIFY` U2b.17 (re-test at the new threshold) is discharged: it fails harder.**
- **CORRECTION 1 — `LAW_U1PHI_TEST.md` Lemma U1φ-1 is WRONG in the necessity direction.**
  Its `(⇐)` proof needs `Z_{G_q}` bounded at `Re s = −1`, a line outside **every** `Ω̃` the lane
  uses (`K` starts at `−1/10`). So `(U1-φ-a) ⟺ U1` is false; only `⟹` holds. The test was
  corroborating, **not deciding**. This is also what **saves U1**: the refutation does not
  propagate. Consistent with the extended guard, which reads U1 as *true* (flat/decaying) while
  (U1-φ-a) is *false* — both are possible only if necessity fails.
- **CORRECTION 2 — `LAW_U1PHI_TEST.md` §4.3's headline aliases.** Branch-safety was checked
  against the *observed* step, not the *null's*: at `t = t_∞` the null's `q = 12→16` step is
  **`4.07` rad `> π`** (and `16→20` is `3.16`). The "`17.02` rad required, `2.02` observed"
  statistic (Uφ.14, "the most robust claim here") is **void at the physical height**. It survives
  on `t = 1.5` (null step `0.46`) and `t = 3.5` (`1.08`), so the null exclusion stands — but must
  be re-attributed.
- **CORRECTION 3 — `LAW_U1_GROWTH.md` §10's dismissal of the adverse guard is wrong.** The rise at
  `Re s ≤ 0.0732` is **predicted** by the functional equation once `φ_q ≍ 1` is known:
  slope `1−2σ`, i.e. `+1.00` at `Re s = 0` and `+0.854` at `0.0732`, against measured `+0.893`
  (all-8 sup, `q = 12…100`) and `+0.84` (`dU_3`). `HEURISTIC`, data ragged, but "unidentified
  domain, therefore artefact" is not supported.
- **THE REDUCTION (the positive deliverable).** `Ω̃` need not reach `Re s ≤ 0`. Shrinking it to
  `{Re s > 1−σ}` forces the crux into **`σ ∈ (3/4, 1)`** — `> 3/4` by `Re s_∞ = 1/4`, `< 1` by
  Theorem E3 — where the Dirichlet series diverges and positivity says nothing. **(U1-φ-a′)**:
  a uniform bound on `|Z_{G_q}|` **and** `|φ_q| = O(q^{−(2σ−1)})` on one vertical segment
  `Re s = σ ∈ (3/4,1)`. Sharper than (U1-φ-a), which was posed where it is false.
- **Aristotle-able:** B1 (the `c = 1` double coset — pure algebra), B2 (positivity lower bound,
  with the constant-term formula as hypothesis), B3 (the triangle split), B4 (the alias bound).
  All downstream of U2b's A1. The tail constant `sup_q T_q(σ) < 1` is *not* Aristotle-able.
- **Not touched:** `lane_f/`, `u1_guard_extended.*`, `probe_u1phi*.py`. No commit, no certificate.

## 2026-08-16 — Lane G (Opus audit lane): MINIMAL-HYPOTHESIS AUDIT of the tail argument

Artifact: `lane_g/LAW_MINIMAL_HYPOTHESES.md`. **Audit only** — no new numerics, no probe run,
no certificate, no commit, `lane_f/` untouched.

**Brief.** Re-derive the (T2′) Vitali+Hurwitz continuation end-to-end and determine the MINIMAL
hypothesis set, rather than continuing to serve "the tail needs U1".

- **VERDICT — split, and both halves matter.** U1 is minimal in **kind** and grossly over-stated
  in **domain**. All three candidate weakenings named in the brief fail: a disc around `s_∞`
  alone is **provably insufficient** (Lemma M-1 — Montel gives a limit that nothing identifies,
  since the only proved convergence set is `Re s > 1`); "one-point bound + equicontinuity" is
  **equivalent, not weaker** (Cauchy estimates both ways; the one point is free from U2b);
  Montel-via-zero-free-right-edge + FE is **dead twice** (disjoint-region witness in
  `LAW_U1_GROWTH.md` §5.3, plus `Uφp.12`'s proved `|Z_{G_q}(1−σ₀−it)| → ∞`). Vitali is already
  at its classical floor; Osgood does not locate the good set.
- **THE CHAIN.** 12 numbered steps with the exact hypothesis each consumes. **Only Step 6
  (local uniform boundedness) is open.** Steps 2,3,4,5,8,9,11 are `PROVED`; 7,10 are classical
  citations; 12 (finite base, `Q₀` effectivity) is off-audit and unchanged.
- **(U1-min), the sharpest true obligation.** `∃ r ∈ (0,1/4), δ, σ_R ≥ 3.5, Q₁, A`: the family
  `{Z_{G_q}}_{q≥Q₁}` is locally uniformly bounded on an open connected corridor
  `(1/4 − r, σ_R+1) × (t_∞ ± δ)`. **No exponential order-2 shape** (already U1.1), **no
  `t`-uniformity** (`δ` arbitrarily small), **no `Re s ≤ 1/8`**. The one irreducible clause is
  connectivity: the boundedness domain and Vitali's accumulation set must be the SAME connected
  domain, and the latter is pinned to `Re s > 1` by the Euler product's abscissa.
- **THE LOAD-BEARING FINDING.** The historical `Ω̃`'s left edge `Re s = −1/10` is required by
  **nothing**. With it, the FE reflection forces `σ ≥ 11/10 > 1` — inside Theorem E3's kill
  zone. **The lane's crux was refuted at an abscissa the theorem never needed to visit.**
  Independently confirms `LAW_U1PHI_PROOF_ROUTE.md` §5.1 by a route not passing through
  `LAW_U1PHI_TEST.md`.
- **SHARPENING of (U1-φ-a′).** `r` is free in `(0,1/4)` — the parent's `r < 1/8` is over-tight
  (true margin is `1/4 − r`, not `1/8 − r`). Sending `r ↓ 0` sends `σ ↓ 3/4` and the required
  `φ_q` decay exponent `2σ−1 ↓ 1/2`, **while enlarging the delivered off-line margin**. No
  trade-off. **Any decay exponent `> 1/2` at any single abscissa in `(3/4,1)` suffices.**
- **THE CRUX, correctly located, is one sentence:** *how large is `φ_q(s)` on `3/4 < Re s < 1`?*
  U1-min and (U1-φ-a′)(ii) are **the same unknown, oppositely signed** — §4.3's adverse
  retrodiction `|κ_q| ≍ q^{1−2σ}` presumes exactly `|φ_q| ≍ 1` at the reflected abscissa. The
  lane has **zero evidence either way**: E3/E4 are proved only for `Re s > 1`; the phase work
  sits at `Re s = 1/2` where unitarity makes the modulus trivial; the `σ = 0.75` receipt rows are
  self-flagged truncation artefacts.
- **DEFECT — (U1-φ-a′) omits the horizontal edges.** The max principle on
  `[1−σ,σ] × [t_∞ ± δ]` needs four sides; (i)+(ii) supply two. Repair = Phragmén–Lindelöf in the
  strip (`PROVABLE`, `Z_Γ` of order 2), **at the price of requiring (i),(ii) for all real `t`**.
  So `t`-uniformity is a feature of the implementation, not of the theorem.
- **DEFECT — `LAW_U1_GROWTH.md` §6 over-claims for (U1-φ-b).** A uniform resonance count on one
  disc controls only local Hadamard factors; the global zero distribution is `PROVED`
  non-uniform at fixed height (U1.16, elliptic mass `(log q)/π ≈ 17.6` vs `T²` term `16.0` at
  `T ≈ 8`, `q = 1000`), and the Hadamard exponential is untouched. **(U1-φ-b) is an ingredient,
  not a closure**, and should be delisted as a live alternative.
- **EVIDENCE RE-SORTED.** Every adverse measurement the lane holds (§7.3's `+1.50`, §4.3's
  `dU_3`/`dU_4` slopes, `Uφp.12`) lives at `Re s ≤ 0.0732`, **outside `Ω̃_min`**. Every
  supportive one (`dU_0` at `Re s = 1/2` slope `−0.574`; the flat `+0.071` identified-domain
  aggregate) lives **inside** it. **One adverse point lies inside:** `dU_2` at `Re s = 1/4` —
  the abscissa of `s_∞` — slope `+0.61` over `q = 12…40`, unreconciled with the flat aggregate
  over `q = 12…100`.
- **CHEAPEST NEXT ACT (named, not run — this is an audit):** read out and refit the **per-point
  `q`-slope at `dU_2` (`Re s = 1/4`) over the full `q = 12…100` range** from the existing
  `law_probes/u1_guard_extended.json`. **No new compute.** It measures U1-min at the only
  abscissa that matters and discriminates between the two contradictory readings the lane
  currently holds.
- **Corrections owed:** `LAW_T2_DETERMINANT.md` §3.2 (`r < 1/4`, margin `1/4 − r`; add the
  unstated hypothesis that `Ω̃` avoids `Z_{Γ_θ}`'s real poles); `LAW_U1_GROWTH.md` §9 (same `r`),
  §6 ((U1-φ-b)), §1.2 + `LAW_U2B_CLOSURE.md` Lemma U2b-8 (left edge `−1/10` → `1/4 − r`);
  `LAW_U1PHI_PROOF_ROUTE.md` §5.1 (`σ > 3/4 + r`; exponent `> 1/2`; all-`t` from P–L).
- **Conditionality, stated:** this audit takes the parents' `PROVED` labels at face value and does
  not re-verify E3/E4, U2b's constants, or U3's citations (`V1`–`V3` still owed).
  `LAW_U1PHI_PROOF_ROUTE.md` is itself PENDING adversarial verification, and findings M.11–M.13
  inherit that pendency.

---

## 2026-08-16 — Lane G · NEGATIVE CONTROL on the pin-migration machinery — **CONTROL-PASS**

Deliverable `lane_g/LAW_NEGATIVE_CONTROL.md`. Script
`lane_g/law_probes/probe_negctrl.py`; receipts
`lane_g/law_probes/negctrl_q{4,6}_d1.json`,
`negctrl_q{4,5,6}_flagship.json` + logs. No commit; `lane_f/` untouched.

**Premise audited.** The D1 scan/Newton locator had only ever been run at
non-arithmetic `q`, i.e. exactly where off-line pins are expected. The
family law asserts arithmetic `q ∈ {3,4,6}` have none. Blind run at
arithmetic `q` = a genuine null.

**Method.** Protocol identical to `probe_d1_scan.py` — same box grid density
(`Re` step 0.02, `Im` step 0.05), `N=16` coarse / `N=48` Newton, same seeding
rule, `sign=+1`, 300-bit Arb midpoints — **pre-registered in §1 before any
run launched**, including acceptance (`|det| < 1e−12` + convergence + in-box)
and classification (`ON-LINE` `≤1e−5` from `Re=1/4` or `1/2`; `OFF-LINE`
`≥1e−3` from both; `GREY` between). Every accepted pin re-refined at `N=96`.
One pre-registered deviation: the Newton clamp `Re ≤ 0.49` → `RE_HI + 0.10`,
because `0.49` lies inside the flagship box.

**Results.**

| q | box | pins | OFF-LINE | location | class |
|--:|---|--:|--:|---|---|
| 4 | D1 `[0.15,0.45]×[6.6,7.6]` | 1 | **0** | `0.25 + 7.067362570867347 i` | ON-LINE `Re=1/4` |
| 6 | D1 | 1 | **0** | `0.25 + 7.067362570867347 i` | ON-LINE `Re=1/4` |
| 4 | flagship `[0.40,0.50]×[5.5,6.0]` | **0** | **0** | — (grid `min|det| = 1.32`, no minimum) | — |
| 6 | flagship | 1 | **0** | `0.5 + 5.098741908729560 i` | ON-LINE `Re=1/2` |
| 5 | flagship | 1 | 1 | `0.453895180075 + 5.763537241730 i` | **OFF-LINE** (positive arm) |

- **Positive arm reproduces exactly**: `q=5` returns the flagship pin to every
  published digit (`THEOREM_G5_OFFLINE_ASSEMBLY.md`), `N`-stable to 16 digits.
- **The arithmetic nulls are correct, not merely empty**: run blind, the
  `G_4` and `G_6` operators put their only D1-box pin at `Re = 1/4` to
  `1e−16` and `Im = 7.067362570867347` — distance to `ρ₁/2` = **`8.9e−16`**,
  i.e. the machinery independently re-derived the first Riemann zero with no
  `ζ` input. Consistent with `M2_NONFACT_WITNESSES.md`'s `G_4` control row.
- **Surface-level discrimination**: flagship-box `min|det|` = `0.057` (`q=5`,
  has a pin) vs `1.32`/`1.24` (`q=4`/`q=6`, none) — a 21–23× gap visible in
  the raw grid, before any acceptance rule.

**Defect found (real, in the lane's own script).** `probe_d1_scan.py`'s
hard-coded Newton clamp `Re ∈ [0.02, 0.49]` would have pinned run D's
`Re = 1/2` root at `0.49` and reported a **false** off-line pin. All seven
`d1_q{12,16,22}` candidates were re-inspected: none touched a clamp boundary,
so **no published D1 number changes** — the defect is latent. Fix owed: port
the relative clamp into `probe_d1_scan.py`.

**Verdict: CONTROL-PASS.** No machinery-artifact alarm. The locator does not
generate off-line pins where the law forbids them, and does find the one it
should. Removes "the scan may be manufacturing roots" from the live
objections to D1; **does not** upgrade D1's rigor (both are non-rigorous
midpoint scans, no winding certificate). Limits stated in §2.6: only
`κ = 1,2` tested, `q = 3` not run, `mms−` sector untested. No claim here
depends on `LAW_U1PHI_PROOF_ROUTE.md`.

**Follow-ups (cheap):** (i) clamp fix in `probe_d1_scan.py`; (ii) `q = 3` as a
third null, which also exercises the odd builder in the negative arm;
(iii) one arithmetic null in the `mms−` sector.

---

## 2026-08-16 — Lane G compute: the crux strip measured, and the U4 mirror test

**Artifact:** `lane_g/LAW_STRIP_AND_MIRROR.md`. **Receipts:** `lane_g/law_probes/strip_*.py|json`,
`mirror_*.py|json`. **Nothing committed; `lane_f/` untouched.**

- **TASK A — `(U1-φ-a′)(ii)` MEASURED, ADVERSE.** `|φ_q(σ+it)|` on the crux strip, `q = 8…56`,
  via main-term-subtracted continuation of the Eisenstein Dirichlet series.
  **The brief's 6-digit gate is unreachable and the note says so with a number:** the continuation
  error is `X^{−(2σ−1)}` (measured exactly at `q=3` against `ζ(2s−1)/ζ(2s)` out to `X = 10⁷`), so
  6 digits at `σ=0.90` needs the `c`-spectrum to `X ≈ 3.7e6`, i.e. `≈1.4e12` group elements; the
  reachable budget is `X = 200`. **What is validated instead is the `q`-SLOPE** — reproduced to
  `≤ 0.07` against the three arithmetic closed forms on the same strip points.
  **Result (`q = 12…56`, truncation-stable to `0.021`, budget-stable to `1.2 %`):** `|φ_q|` decays
  at `t = t_∞` (`−0.785` at `σ=0.90`, `−0.581` at `σ=0.95`) but **GROWS** at `t = 1.5` (`+0.477`,
  `+0.391`) and `t = 3.5`. Since (ii) is a `sup` over `|t| ≤ t_∞+1`, **it fails on the measured
  grid at both abscissae of the corrected window `(7/8,1)`**, by ~1 unit of exponent against the
  minimal-hypothesis bar `< −1/2`. Honest limit: the rise is non-monotone, so growth in the limit
  is NOT established — measured-adverse, not refuted.
- **TASK B — CLEAN DISAGREEMENT; U4-as-identification refuted OR the Teo `κ_q` assembly is wrong.**
  Comparable combination derived first: under U4 + Teo, `P_q(1−s)/P_q(s)` (transfer operator only)
  must equal `|φ_q(s)|·|K_q(s)|` (Eisenstein + Teo kernel only) — no shared machinery.
  **Measured ratio `5.0e12` … `2.6e19`** at `σ = 1.25,1.40,1.50`, `q = 12,16,22,30`, and the two
  sides disagree in **direction**, not only magnitude.
  **Three controls close every cheap escape:** (1) the determinant is **`N`-converged to `1e−16`**
  at `Re s = −0.25,−0.40,−0.50` and at every `∂U` point, `N = 24…64` (pre-registered rule met with
  10 orders to spare); (2) `|K_q(1/2+i t_∞)| = 1.000000000000` at four `q`; (3) **the failure
  survives at arithmetic `q = 4, 6` where `φ_q` is the exact closed form** (`8.5e6`–`1.7e13`),
  eliminating the new evaluator as the cause.
- **`dU_0` is VACUOUS** and is flagged as such: both sides are `1` by Schwarz reflection plus
  unitarity, independent of U4. At `dU_1`/`dU_2` the identity is not checkable (both `s` and `1−s`
  sit in the divergent region), so it is **inverted** to read a U4-conditional `|φ_q|` off the
  guard — giving `≈2.0e3` at the `dU_2` mirror `Re s = 3/4`, against a direct `≈0.097`. A `2e4`
  disagreement at the guard's own point. **On the coordinator's `dU_2` target:** the
  U4-conditional `|φ_q|` slope at `dU_2`'s mirror (`Re s = 3/4`) is **`+1.130`** (`+0.703` at
  `dU_1`), sitting next to the guard refit's flagged `+1.06` — but that is the **same determinant
  read twice**, not independent corroboration, and the underlying sequence is non-monotone
  (`q=16` sits `2.6×` below its neighbours). **The contradiction is what survives:** the
  U4-conditional reading says `|φ_q(3/4−it)|` GROWS like `q^{+1.13}` while the direct evaluator
  says it DECAYS like `q^{−0.79}`, and the two disagree by `2e4` in value.
- **CONSEQUENCE, loud.** `LAW_U1_GROWTH.md` §7.3, its §10 addendum, and
  `LAW_U1PHI_PROOF_ROUTE.md` §4.3 all read `Z_{G_q}` off the proxy at `Re s ≤ 1/2` and argue about
  what its `q`-slope means. The disagreement is `q`-dependent (`q^{+5.6}` at `σ=1.5`), so it does
  **not** cancel in a slope. **That argument cannot be settled on its current terms: the instrument
  has not been shown to measure `Z_{G_q}` anywhere the argument is being conducted.**
- **Fault localised, not separated.** `|K_q|`'s magnitude and its whole `q`-dependence sit in the
  **Barnes bracket** (`3.2e−20` at `s=1.5+i t_∞`) raised to `(1−2/q)/2` — and the `Re s = 1/2`
  assembly check is **structurally blind** to that exponent, because the bracket has modulus `1`
  there for every exponent. Correction owed to `LAW_U1_GROWTH.md` §3.1.
- **CHEAPEST NEXT ACT (named, not run):** repeat the §3.3 mirror test at **`q = 3`** using
  `zeta_cert_rosen.py` (odd-`q` module) instead of `zeta_cert_rosen_even.py`, which raised
  `NotImplementedError` here. `q=3` is `PSL(2,Z)`: `φ_3 = g(s)` exact, `Z` classical, Teo applies
  verbatim. Failure there ⇒ the fault is the **assembly** (an afternoon's fix). Success there with
  failure at `q ≥ 4` ⇒ the fault is **U4**, and the guard literature is measuring the wrong object.
  Six determinant evaluations, under an hour.
- **Conditionality, stated:** `LAW_U1PHI_PROOF_ROUTE.md` is itself PENDING ADVERSARIAL
  VERIFICATION and was not re-verified here; its E2/E3/E4 and its `CITATION(Iwaniec Thm 3.4)` are
  taken at face value. All numbers are float / `mpmath` midpoints — no interval arithmetic, no
  winding certificate, no ball radii.

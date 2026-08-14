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

# GOAL 2026-07-02 — pursue Pick A (Farey-gap EVT) + Pick B (certified G_5 cross-check)

Source: memory `breakthrough-picks-2026-07-02.md`. Papers stay deferred (Koyama+breakthrough gate).

## Track A — extremes/clustering of Farey gaps (refines Marklof–Pollicott, Nonlinearity 38 (2025) 055003)
Analytic skeleton (main agent, 2026-07-02):
- Maxima (gap-product q_i·q_{i+1} < sQ²): consecutive denominators sum >Q ⟹ each small q_j ⟹ exactly 2 consecutive exceedances ⟹ cluster law δ_2, **θ=1/2** (near-theorem); Fréchet-1 tail with log-slowly-varying factor.
- Minima (q_i·q_{i+1} > (1−δ)Q², hard edge 3/π²): region shrinks to parabolic fixed point (1,1) of BCZ (k=2 branch, shear conserves d=y−x) ⟹ in-cluster denominators in arithmetic progression; cluster tail P(L≥n)~C/n; **θ(δ)~c/log(1/δ) → 0**.
Predictions P1–P4 under numeric test (projects/evt-farey-gaps/).

Loop contract: generator = codex numerics; verifier = main agent vs P1–P4; gate = 3 estimators consistent + exact signatures hold; stop = gate pass or 2 corrective iterations; budget = 2 codex calls.

## Track B — independent cross-check of certified G_5 even resonances (step toward CAP)
B1 (GLM) extracts certified state (values, operator conventions, engine entry points) → B2 (codex) recomputes 2–3 even resonances with a DIFFERENT discretization (float64 OK; independence of systematics is the point), projects/g5-crosscheck/.
Loop contract: generator = B2; verifier = main agent vs certified intervals; gate = interval-overlap / |Δ|≤1e-6 on ≥2 resonances; stop = pass or 2 iterations; budget = 2 codex calls.

## done means
1. A: numeric verdict on P1–P4 (each confirmed/refuted with numbers, ≥2 values of Q).
2. A: theorem-candidate statement for θ=1/2 maxima law written down if P1 holds.
3. B: ≥2 even G_5 resonances independently reproduced (or mismatch diagnosed + documented).
4. Synthesis note + memory updated; goal closed with verdict in this file.

## CLOSED 2026-07-03 — verdict vs done-means
1. A numerics on P1–P4: DONE — P1 (θ=1/2, δ₂) + P4 (AP signature) CONFIRMED; P2/P3 REFUTED and corrected → exact θ_edge=2/3, n⁻² tail (see EVT_CLUSTERING_SPECTRUM_2026-07-03.md).
2. θ=1/2 theorem-candidate: EXCEEDED — combinatorial core Lean-PROVED (Aristotle 22e93551); mixing-rate blocker BYPASSED via M–P Thms 2–3 program.
3. B cross-check: DONE — all 3 certified G_5 even resonances independently reproduced (4.1e-9 / 1.4e-7 / table-precision + refinement).
4. Synthesis note + memory: DONE.
Bonus: G_q hard-edge trichotomy (parabolic q=3 unique; q=5 hyperbolic 2λ₅; q=7 elliptic π/7) — preliminary.

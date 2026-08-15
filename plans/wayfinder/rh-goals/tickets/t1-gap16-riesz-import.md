# T1 GAP-16: verified explicit-formula import under the Riesz window

- Type: research
- Mode: AFK+frontier
- Status: DERIVED + DISPATCHED (closure pending)
- Claimed by: none (frontier statement design -> Aristotle)
- Blocked by: none
- Source: Amendment A2 enactment 2026-08-15 (GAP-16 opened at full weight)

## Question
The frozen model's verified explicit-formula import was proved for the
Gaussian window; re-derive/re-verify it for W(x) = (1-x)_+ (Mellin
M_W = 1/(s(s+1)); new pole at s = -1 contributing R_{-1}(N) = 12/N).
Aristotle-able once the finite statement is fixed.

## Resolution
**Derivation written 2026-08-15; finite Lean core dispatched; NOT closed.**

- Artifact: `research_notes/rh_goals_2026-08-14/lane_t/T1_GAP16_RIESZ_IMPORT.md`
  — states what the Gaussian artifact
  (`research_notes/imported_farey_now/Smoothed_Dwf_explicit_formula_VERIFIED.md`)
  proved and where the Gaussian was load-bearing, then derives the order-1
  Riesz analog (Prop. R): R₀ = −2 survives, new pole term R_{−1}(N) = 12/N,
  trivial zeros become SIMPLE poles (R_triv = O(N^{−2}), no log N), remainder
  O_A(N^{−A}) for fixed A ∈ (1,2). Perron + contour shift cited
  (Hardy–Riesz Ch. V; Montgomery–Vaughan §5.1; Titchmarsh §3.7, §9.7), not
  proved here.
- Numeric validation (non-rigorous): §3 of the artifact; script
  `projects/aristotle_dispatch_v21/riesz_numeric_check.py`.
- Lean core: `projects/aristotle_dispatch_v21/RieszImport.lean`, 7
  sorry-stubbed statements (finite Cesàro identity, the k=1 Mellin integral,
  M_W residue algebra, R₀ = −2, R_{−1} = 12/N, simple-pole trivial term).
- Aristotle project id: **24c6e3df-76fd-43d0-a052-b6ddf10d6084** (submitted
  2026-08-15; result not awaited, nothing claimed proved).
- Remaining to close: (i) Aristotle returns the finite core; (ii) frontier
  review of the analytic Perron/contour step, which stays a citation;
  (iii) absolute convergence of the zero sum still rests on
  J_{−1}(T) = O(T).

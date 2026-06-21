# GOAL — g_corr <= g_true realization bridge: the LAST residual for unconditional q>=22

Date 2026-06-20. After the L_blk window (commit 31bb8c1, lake-build-verified axiom-clean): the
genuine lower bound `perq_Xomega_lb_Lblk_GEN` reaches q>=22 CONDITIONAL on ONE named hypothesis =
the realization bridge that discharges `FwindowL (L_blk q) mpoly`. Closing it -> unconditional
q>=22, and (with verified q=5..21 + C-band q>=7) -> ALL q.

## The bridge
- `g_corr(L,q)` (L1bArcCoverage) = continuous corridor arc-width minimum: sInf over the phase
  domain of `fcorr(L,q,mu_c)` (worst-case window-product over the rotation arc).
- L1b_target (PROVED, q>=18): 1/lambda^3 <= g_corr(L_blk q, q).
- `g_true` = the actual GENUINE-orbit window-product (discrete, on the scalar/k=1 corridor part).
- Bridge `g_corr <= g_true`: the continuous minimum is ATTAINED/realized on the actual orbit =>
  1/lambda^3 <= g_corr <= g_true => no sustained sub-threshold window => FwindowL(L_blk).

## Likely decomposition (scout confirms + assesses difficulty)
- **A-realization** — the corridor realization IDENTITY: the genuine scalar-corridor window-product
  = fcorr at the orbit's phase mu_c (the corridor analog of the energy route's pgen_orbit_realization,
  which we PROVED). The deep-mid (k>=2) part already ejects inside genuine_no_sustained_Lwin.
- **B-wire** — the inf step (fcorr(mu_c) >= sInf = g_corr, Mathlib csInf) + chain with L1b_target +
  discharge the FwindowL(L_blk) named hyp in perq_Xomega_lb_Lblk_GEN -> assemble unconditional q>=22.

## CRITICAL HONESTY
This `hbridge (g_corr<=g_true)` is a LONG-STANDING corridor-route residual. Scout MUST assess
whether it is TRACTABLE (a realization identity like pgen_orbit_realization) or the genuine hard
core. If hard, REPORT that precisely; do not force a false closure.

## Verify method (established): genuine chain builds inside the INNER project ->
  cd projects/aristotle_dispatch_v15/uniform_q5to18 && ~/.elan/bin/lake build <Target>
(add a [[lean_lib]] glob for any new file). Self-contained pure-Mathlib pieces: lake env lean.

## Rules (every agent; hooks don't fire in subagents)
READY FOR JUDGING not "done"; attempts+assumptions; quote the lake command + EXIT + #print axioms.
Write ONLY assigned disjoint paths; no git; no key echo. Reuse sealed defs VERBATIM; a vacuous/
weakened statement is the worst failure. Distinguish PROVED / reduced-to-named-hyp / OPEN. Do NOT
claim unconditional unless the assembled theorem carries no non-definitional hypothesis + no sorryAx.

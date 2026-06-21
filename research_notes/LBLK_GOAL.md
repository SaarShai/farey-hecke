# GOAL — L_blk q-dependent window: unconditional X_Ω(q) >= 1/λ³ for q >= 18

Date 2026-06-20. Approach #1 (stays on the genuine multi-branch map; avoids the scalar-vs-genuine
mismatch that stalled the energy route). The genuine engine caps at q<=21 ONLY because it uses a
FIXED 6-window (genuine_no_sustained_6win / Fwindow6). Generalize to the q-dependent window
L_blk(q)=⌈33q/256⌉+2; the analytic content is ALREADY PROVED:
  - L1bArcCoverage.L1b_target : ∀ q>=18, 1/λ³ <= g_corr(L_blk q, q)   (buildable lib L1bArcCoverage)
  - L1bArcCoverage.arc_coverage_ineq : 2·arccos(2√6/5)/π < 33/256       (PROVED)
  - asymptotic margin δ∞ = 5.77e-5 > 0; interval-certified q=18..10000.
So the ONLY gap = the Lean generalization of the no-sustained window lemma from fixed-6 to L_blk(q),
then instantiate + wire to the GEN' discharge (closed_section_lb <- perq_Xomega_lb_qge19_GEN').

## CRITICAL UNKNOWN (scout resolves first): VERIFICATION METHOD
genuine_no_sustained_6win lives in projects/aristotle_dispatch_v15/uniform_q5to18/ToplevelStitchGen.lean,
which is NOT globbed by the v15 lakefile (no .olean; `lake env lean` fails on GenuineMapP2 import).
So unlike our energy-route files, these are NOT main-loop-verifiable. Scout MUST determine: can the
genuine chain be built (a lib glob to add? a sibling project mimo-mini-project with the chain?), is
L1b_target reachable from a buildable lib, and can the generalization be done either (a) self-contained
+ `lake env lean`-verifiable (reproducing genuine facts verbatim, like the energy-route files) or
(b) only via Aristotle. Pick the verifiable path; if only Aristotle, that is the gate (honest caveat).

## Pieces (parallel after scout)
- **A-window** — generalize the no-sustained window lemma to a PARAMETRIC length L:
  `genuine_no_sustained_Lwin (L) (hcover : 1/λ³ <= g_corr(L,q)) ... : no sustained sub-threshold run`.
  Fixed-6 becomes L=6; L_blk becomes L=L_blk(q). Then instantiate L:=L_blk q with the proved L1b_target
  (q>=18) and wire to GEN' to get Xomega >= 1/λ³ for all q>=18.
- **C-band** — derive the band facts (1<λ<2, 9/5<λ for q>=7, λ²>=λ+1) UNIFORMLY from λ_q=2cos(π/q),
  to remove the per-q hmp/band hypotheses (toward a clean uniform statement). Secondary; the per-q
  version suffices for the core result.

## Integration (main loop)
Assemble A (+C) -> unconditional Xomega>=1/λ³ for q>=18; verify by the scout-established method
(no sorryAx; faithful genuine Xomega/Pgen/Tgen). Combined with the verified q=5..21, this would give
ALL q. HONEST: NOT unconditional until the assembled theorem verifies with no non-definitional hyp.

## Rules (every agent; hooks don't fire in subagents)
READY FOR JUDGING not "done"; attempts+assumptions; quote the verify command + EXIT + axioms. Write
ONLY assigned disjoint paths; no git; no key echo. Reuse sealed defs VERBATIM; a vacuous/weakened
statement is the worst failure. Distinguish PROVED / reduced / OPEN. If the genuine chain is not
verifiable by your tools, SAY SO and use Aristotle as the gate.

# GOAL — cross-project close: scalar->corridor collapse + hpin -> unconditional q>=22

Date 2026-06-20. The two remaining residuals of the lake-build-verified q>=22 reduction
(perq_Xomega_lb_Lblk_GEN carries FwindowL(L_blk q); commit 4c07a4c):

1. **Scalar->corridor product collapse + no_sustained_corridor wiring.**
   no_sustained_corridor (projects/mimo-mini-project/lean/BCZHeckeGATE2_L1_skeleton.lean:233) is an
   ABSTRACT lemma: takes a corridor block-boundary state s:N->RxR + its proven closed-form dynamics
   (Chebyshev recurrence, conserved M_W ellipse, product observable) + hbridge, concludes
   g_corr(L_blk q) <= window-sup P. FwindowL(L_blk q) (LblkWindow, uniform_q5to18) is the DISCRETE
   Hecke-CF SCALAR window (c(i+j)*c(i+j+1) < 1/l^3). The collapse: on the k=1 corridor the scalar
   genuine step = the M_W block step, so the scalar c-products = the corridor s-products. Wire:
   port no_sustained_corridor into uniform_q5to18 (it is abstract -> should build with Mathlib +
   the inner lakefile), prove the scalar<->corridor product agreement, discharge FwindowL.

2. **hpin** (the in-domain radius/phase datum feeding hbridge): r*Blam*cos(|muc|+H) >= 1 from the
   in-domain constraint D>1 at the window far-endpoint. The agent found it IRREDUCIBLY phase-coupled
   (no unconditional shortcut). Genuine in-domain orbit geometry.

## Build/verify method (scout confirms): port abstract lemmas into uniform_q5to18 + [[lean_lib]] glob,
   then ( cd projects/aristotle_dispatch_v15/uniform_q5to18 && ~/.elan/bin/lake build <Target> ).

## Pieces (parallel after scout)
- **A-collapse** — port no_sustained_corridor (+ its abstract deps) into uniform_q5to18; prove the
  scalar->corridor product collapse; discharge FwindowL(L_blk q) GIVEN hbridge (as named hyp).
- **B-hpin** — prove hpin (the in-domain radius bound) from the corridor domain invariants
  (corridor_domain_realization / corridor_antidomain_realization already PROVE the D,D' sinusoids +
  amplitude pinning); or report the exact blocking geometry.

## FIRM STOP-GATE (pre-committed)
This is round 5+ of the unconditional push. GATE: either (a) the assembled q>=22 theorem carries
NO non-definitional hypothesis + no sorryAx (=> unconditional, with q=5..21 => all q), OR (b) a
precise honest residual. If this round ALSO merely defers to a new named hyp WITHOUT closing
FwindowL or hpin, STOP and consolidate -- do not loop further. Honesty over closure; no false claim.

## Rules (every agent; hooks don't fire in subagents)
READY FOR JUDGING not "done"; attempts+assumptions; quote lake EXIT + #print axioms. Write ONLY
assigned disjoint paths; no git; no key echo. Reuse sealed defs VERBATIM; a vacuous/weakened
statement is the worst failure. Distinguish PROVED / reduced-to-named-hyp / OPEN. If a piece does
not close, name the EXACT blocking step -- do NOT punt to a disguised named hypothesis.

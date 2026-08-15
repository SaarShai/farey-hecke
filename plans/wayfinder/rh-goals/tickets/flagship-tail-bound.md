# Proven truncation tail bound for the G_5 operator

- Type: research
- Mode: AFK
- Status: claimed
- Claimed by: none (frontier T-a/T-b + Aristotle for finite lemmas)
- Blocked by: none
- Source: user directive 2026-08-14 "this must be top priority ... until we have that theorem"; S4 scout (JP-style bound exists for Gauss map, Hecke version unpublished)

## Question
What explicit bound |det − det_N| ≤ F(C, ρ, N) holds on the certification
contours for the G_5 even-sector MMS operator (λ=φ), with proven constants
(invariant disk + branch contraction), replacing the ×4 dimension-tail
heuristic?

## Resolution
(near-closed: rho* = 0.697802 CERTIFIED (Arb ball, 106 sub-certificates,
clearances 11/11 — TB_BLOCK_CERTIFICATES_V2); lemma chain L1–L3 DRAFTED
with certified constants + citation ledger (TB_LEMMA_CHAIN.md); v17 shell
lemmas Lean-proved. W-cert v1 correctly certified the naive tail aggregation divergent →
L3′ repair (k-column split); W2 then certified the crude Gohberg-Krein
prefactor astronomically large (W 18.6..1926, F~1e75 at N=48; crude-bound
minimal N=567 for pin 1) → L3″ hybrid trace-norm refinement (certified
column norms + analytic tail; classical inequality, Aristotle-able).
V3 sol adversarial review: CHAIN BROKEN AS WRITTEN — A1 confirmed
(finite-section conflation; repair = Fredholm identity det(I−LP_N) =
det(I−P_N L P_N) on a trace-class Hilbert setting), V2 envelope INVALID
(dropped center offset + per-column Hurwitz terms; W, F, N=567 all void),
winding implementation certifies samples not the closed contour. Repair
program R1–R4 in TB_LEMMA_CHAIN banner. R1 WRITTEN (TB_R1_HILBERT_RESTATEMENT.md) and its two abstract joints
MACHINE-PROVED (Aristotle v18, axiom-clean: finite-section det identity +
trace/column bound). TC3 recon: "YES at N=128" with 4 orders of slack
(margin 3.9e-6 vs F 1.6e-10) — but consumed the voided W and sampled
winding, so recon-grade only. BINDING VERDICT = R2R3 (sol-tier,
corrected envelope + closed arcs). R2R3 run 1 was KILLED at 13:37 by the
network outage after 36 min (left near-complete certify_r2_flagship.py +
certify_r3_flagship.py in the worktree); RELAUNCHED 2026-08-14 ~20:35
with a checkpoint-to-disk mandate, reusing the partial code. Aristotle
v19 (R1Completion) PROVED meanwhile: l2_le_card_mul_sup_sq,
coeff_bound_of_uniform, geom_tail_le — 0-sorry, axiom-clean
[propext, Classical.choice, Quot.sound]; with v18 that machine-proves the
R1 chain's abstract joints. R2 phase CERTIFIED (11/11 families,
T_tail(128)=5.27e-17, T_tail(160)=6.27e-22, receipt sha 7eed214e).
R3 attempt 1 NOT_CERTIFIED: naive ball-matrix det over closed arcs
wraps catastrophically (depth 0.122 vs pointwise radii ~1e-36 —
algorithmic, ~34 orders recoverable); per-arc T_finite prefactor also
ruled not theorem-valid (omits high-output rows). R3b repair
DELIVERED 2026-08-15 00:59: **THEOREM-GRADE closed-contour YES at
N=160** — complete closed cover (284 subarcs), all enclosures exclude 0,
winding 1, min margin +3.4379e-8, valid endpoint bound ||L||_1 <=
17.2912, F_R(160)=1.77974e-6. Frontier re-checks from raw records pass.
THEOREM_G5_OFFLINE_ASSEMBLY.md written (statement + 7-link chain).
V4 found one theorem-level gap (determinant
identification); repaired through R5 v1→v2→v3→v3.1 under adversarial
rounds V5/V6/V7, smoothing receipt E1 (rho_hat 0.9483, sha cd1dc6f4)
run in-session and independently reproduced twice. **V8 (Opus 5) FINAL
RULING 2026-08-15 ~04:50: THEOREM-GRADE YES.** THEOREM DECLARED —
assembly v2 status flipped (THEOREM_G5_OFFLINE_ASSEMBLY.md): first
rigorous off-line resonance localization for a non-arithmetic
finite-area hyperbolic surface; s* in the 1e-6 box at
0.4539+5.7635i, gap delta >= 0.0461. TICKET CLOSED. Successors:
family-offline-theorem (now UNBLOCKED), no-vertical-line-corollary
(now UNBLOCKED), paper assembly. Dissemination owner-gated.)

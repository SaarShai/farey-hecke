# Cross-session verification pass — X(q) closed form, #7 cluster law, #1 general LB (2026-06-02)

Independent verification by a separate session (the one finishing the −1 /goal while the M2 sieve
runs). NOT a re-derivation — checks the goal-sessions' outputs against fabrication (the project's #1
failure mode). All artifacts on disk; nothing sent outward.

## 0. ⚠ FEASIBILITY CEILING (added after goal #1's retraction; independently confirmed here)
The `(1^{q−3},2)` family is FEASIBLE only for **q≤11**. Confirmed via the discovery's own
`svalid_range` (which computes the floor UPPER bound `s_hi`): feasible q=4..11; **tangent/degenerate
at q=12** (`s_lo=s_hi=0.5630`, empty open window); **infeasible q≥13** (`s_lo≥s_hi → None`). The
closed-form `X(q)` and `Xq_exact_for_word` keep emitting values for q≥12 because they check only the
lower scale bound `s_lo` — those large-q "X(q)" are **NOT** backed by a feasible orbit (= goal #1's
retraction, `FINDINGS_corrected_2026-06-02.md`). So everything below about X(q) is valid as an
ergodic-optimization value **only for q≤11**; for q≥12 the closed form is just an algebraic
expression with no feasible-orbit meaning. (My §1 geometric anchor was q=4..10 — inside the feasible
range, so it stands; my earlier "strictly increasing q=4..120" was a property of the FORMULA only.)

## 1. Goal #2 — closed form X(q): proof-core RE-VERIFIED (11/11), within the feasible range
`code/Xq_independent_verify.py` (EXIT=0). Beyond the prior numeric 56-digit check, the **analytic
proof-core** is verified SYMBOLICALLY (sympy): eigenvector solves the rotation recurrence + closure
`v_{q−2}=v_0` + defect eqn; cusp identity `(2sinθ+sin3θ)−2sin2θ = sinθ(2cosθ−1)²`; product-to-sum;
`(A)≡(B)` both parities; exact table {3,4,5,6,8,10,12}. PLUS a from-scratch monodromy-nullspace
rebuild (not the discovery module) → eigvec `== sin((n+1)θ)` to ~1e-61, cusp binds
`s_lo=1/(2sin2θ)`, `X == branch(B)`, q=4..10 (all feasible). NOTE: this verifies the closed-form
ALGEBRA + lower-scale geometry; it does NOT check feasibility (`s_hi`) — that is §0 above. Net: the
formula is right and the value is a valid X(q) for q≤11; the {8,10,12} table entries are correct as
formula values but only q≤11 have a feasible realizing orbit (q=12 degenerate).

## 2. Goal #7 — cluster law: q=3 reproduced; q≥4 method-limited
`code/Xq_cluster_crosscheck.py`. q=3 cluster = 2 over 2.24M recurrent-tail products (= the proven
2/9 3-window bound). Naive iteration of the project's ·λ map ESCAPES the domain for q≥4 (no bounded
recurrent set off the cusp family) → independently corroborates #7's reason for needing genuine
ℤ[λ] cusps. C(5)=3, C(6)=5 are NOT independently reconfirmed here — they rest on #7's
`Gq_hecke_farey_general.py` (genuine-cusp generation).

## 3. Goal #1 — general-q lower bound: COMPILE-CONFIRMED + cross-checked
`lean/HeckeGeneralLB_VERIFIED.lean` recompiled in the throwaway full-Mathlib v4.28.0 env
(`/tmp/lean-minus1`, 8018 oleans): **EXIT=0**; `#print axioms` on `hecke_ground_value_pos` AND
`E_conserved_floor_one` = `[propext, Classical.choice, Quot.sound]` (no sorryAx). `diff -q` vs the
in-env copy the #1 session used = identical. So the result is GENUINE:
> **`hecke_ground_value_pos`** — no orbit keeps every product `P n ≤ λ/(2(1+λ)²)`; hence for every
> Hecke `G_q` (every λ>0) the ergodic-optimization infimum `X(q) ≥ λ/(2(1+λ)²) > 0` (uniform,
> all q at once). Plus `E_conserved_floor_one`: rotation invariant `E=c_n²+c_{n+1}²−λ c_n c_{n+1}`
> preserved on floor-1 steps.

**Cross-check vs #2's closed form** (`LB(q)=λ/(2(1+λ)²)` vs `X(q)`), q=3..499:
`LB(q) ≤ X(q)` ALWAYS (no contradiction). Two important caveats given §0: (i) `hecke_ground_value_pos`
is **model-agnostic** — it bounds every orbit in D for any λ>0, so it is valid for ALL q regardless
of whether any parabolic word is feasible (it does NOT depend on the `(1^{q−3},2)` family). (ii) the
`X(q)` used in the comparison for q≥12 is the FORMULA value (no feasible orbit), so the comparison
there is LB-vs-formula, not LB-vs-realized-X. Honest gap: the uniform bound is 55–69% of the formula
at small q but → 1/9 ≈ 0.111 (BOUNDED) as q→∞ while the formula →∞ — a clean "ground value never
collapses to 0", far from sharp; sharp is only meaningful/known for q≤11 anyway.

## 4. What is now PROVEN vs OPEN for #1 (honest)
- **PROVEN (Lean, axiom-clean):** q=3,4 sharp lower bound + no-ground-state (`BCZHecke_…q3q4_VERIFIED`);
  uniform `X(q) ≥ λ/(2(1+λ)²) ∀q` + floor-1 rotation invariant (`HeckeGeneralLB_VERIFIED`).
- **OPEN (the crux #1 stopped at), now scoped to the FEASIBLE range q=5..11:** the SHARP lower bound
  (`X(q)` = parabolic-word value is the infimum) + no-ground-state for q=5..11. Each ≈ a ~1000-line
  g4-style Lean proof with a forced-floor "Middle" case (connected regime `V(q)>1/(4λ)` for q≥5).
  The uniform engine here (one cusp constraint + `K≥1`) provably cannot reach sharp; sharp needs the
  rotation/Chebyshev (`E_conserved`) structure. Live target for a continuation or Aristotle dispatch.
- **INVALID AS POSED (q≥12):** no feasible `(1^{q−3},2)` orbit (confirmed §0); the naive triangle D
  is the true natural-extension domain only for q=3 (≈100% seed-escape for q≥4 — Rosen/Hecke CF
  fact). So "X(q) for all q / →∞ / universal no-GS" is RETRACTED for q≥12. The model-agnostic uniform
  LB `X(q) ≥ λ/(2(1+λ)²)` still holds (it bounds any orbit in D), but for q≥12 there may be no
  parabolic orbit at all in the naive D.

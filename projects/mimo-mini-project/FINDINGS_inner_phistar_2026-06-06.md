# Inner inequality Φ*(q) ≥ 0 — PROVEN outright in Lean for all q ≥ 17 (upgrade from relaxation)

**Date:** 2026-06-06. Self-recompiled in `/tmp/lean-minus1` (Mathlib v4.28.0): EXIT=0,
`#print axioms` on all four declarations = `[propext, Classical.choice, Quot.sound]`, no `sorryAx`.
File: `lean/BCZHeckeRenormFWindowInner_VERIFIED.lean` (upgraded in place).

## The step (one well-understood, low-risk link of the all-q F-window chain)
Before: the file proved only the **relaxed quadratic** `Q(cos²(π/q)) ≥ 0` (`inner_tail_quadratic`),
i.e. the inner inequality AFTER replacing `cos²H` by its bound `(2+√2)/4`.

Now: the file proves the **genuine inner inequality** OUTRIGHT, with the actual floor-window `H`:

    phi_star_nonneg (q : ℕ) (hq : 17 ≤ q) :
        8·cos⁴(π/q) − cos²(H)·(1 + 8·cos²(π/q)) ≥ 0,   H = (⌊q/4⌋+2)·π/(2q).

## How (all elementary, axiom-clean)
- `cos_sq_pi_div_eight` : `cos²(π/8) = (2+√2)/4`, via `Real.cos_pi_div_eight` + `Real.sq_sqrt`.
- `H_bounds` : for q ≥ 17, `π/8 ≤ H ≤ π/2`. Floor handled by `Nat.div_add_mod q 4`
  (`4·(q/4)+q%4 = q`) + `q%4 < 4` cast to ℝ ⟹ `q−3 ≤ 4·⌊q/4⌋ ≤ q`; then
  `π/8 ≤ H ⟺ 4⌊q/4⌋+8 ≥ q` (true, ≥ q+5) and `H ≤ π/2 ⟺ ⌊q/4⌋+2 ≤ q` (true for q ≥ 17).
- `cos_sq_H_le` : `cos²H ≤ (2+√2)/4`, from `π/8 ≤ H ≤ π/2 ≤ π` via
  `Real.cos_le_cos_of_nonneg_of_le_pi` (cos H ≤ cos(π/8)) + `Real.cos_nonneg_of_mem_Icc` (cos H ≥ 0).
- `phi_star_nonneg` : `Φ* − Q = (1+8u)·((2+√2)/4 − cos²H) ≥ 0` (u = cos²(π/q) ≥ 193/200), so
  `Φ* ≥ Q ≥ 0` via the proven `inner_tail_quadratic`. Final `nlinarith`.

## Method
Dynamic workflow `inner-phi-star-allq` (Ultracode): 3 parallel Lean strategies (A floor-via-div_add_mod;
B general-H helper decoupling trig/arithmetic; C free-form). **All three compiled axiom-clean** —
strong corroboration. Installed strategy A; canonical self-recompile of the installed project file:
RC=0, four axiom-clean prints, 0 sorry/error.

## Honest scope — what this does and does NOT do
- DOES: close the inner-inequality link of the all-q F-window crux with the TRUE floor-window `H`
  (not the relaxation), machine-verified for every integer q ≥ 17 in one theorem.
- Does NOT close the all-q main theorem `X_Ω(q)=1/λ³ ∀q`. The two remaining discrete-analysis links
  are unchanged and NOT in this file:
  - **[L4]** `g_closed ≥ inner` — the binding min-over-μ / lattice step, residual O(1/q²) tightness,
    interval-certified (`code/Ngoal_uniform_interval.py`) but not yet Lean-formalized. Genuinely hard.
  - **[L5]** `g ≥ g_closed` — structural (domain-edge radius bound). Not formalized.
  Plus per-q windows q=5..21 (already Lean-proven) cover small q; this inner bound is the q≥17 tail.

## Bottom line
The inner inequality of the renormalization route is now a single axiom-clean theorem over all q ≥ 17
with the genuine floor-window `H` — the relaxation gap is closed. The all-q theorem still rests on the
two unformalized links L4 (binding) and L5; this step does not change their status.

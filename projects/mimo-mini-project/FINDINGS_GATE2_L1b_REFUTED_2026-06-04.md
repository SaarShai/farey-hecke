# GATE-2 (L1b) arc-width inequality — REFUTED; crux re-localized to multi-branch

**Date:** 2026-06-04. Source: workflow `gate2-L1-attack` (wf_4399dac7-4dc), adversarial refuter +
own hand-check. **Honest record. This CORRECTS the session's earlier "(L1b) arc-width = the one
crux" framing (GOAL_GATE2_L1_crux.md, memory).** Value X_Ω(q)=1/λ³ NOT refuted.

## What was refuted
The derived uniform inequality `g_corr(⌈33q/256⌉+2, q) ≥ 1/λ³` (file `code/GATE2_L1b_arcwidth_*.py`,
skeleton `lean/BCZHeckeGATE2_L1_skeleton.lean`) is **numerically true but VACUOUS as an escape
certificate** — `g_corr` is NOT a lower bound on the true corridor window quantity `g_true`
(the load-bearing "g_corr ≤ g_true" claim is FALSE). Independent confirmations (3 methods):
- `q=25 L=6: g_corr=0.13324 > g_true=0.13118`; `q=40 L=8: g_corr=0.12976 > g_true=0.12444 < thr`;
  `q=60 L=10: g_corr=0.12701 > g_true=0.11992 < thr`.
- **Root cause:** the closed forms were built on the 3-step **W_q block-map** relation
  `b_n=(a_{n+1}+λa_n)/(2λ²+1)`, WRONG for the genuine sub-threshold orbit (gives b≈0.11 vs true
  ≈0.34, factor 3). Both monodromies have trace λ (rotation θ=π/q), which disguised the error.
- Window length `L(q)=⌈33q/256⌉+2 ≈ 0.129q` is ~1.7× TOO SHORT (below the true dwell ~0.18–0.22q),
  so proving the inequality excludes nothing.

## The correct object (hand-verified)
On branch i=q−1: X(q−1)=0, X(q−2)=1, X(q)=−1 ⟹ genuine step `(a,b) → (b, kλb − a)`, `P = a·b`.
For k=1 this is **EXACTLY the scalar floor-1 recurrence** `c_{n+1}=λc_n−c_{n−1}`, product `c_n c_{n+1}`.
⇒ the single-(q−1,1) corridor IS **goal-N's scalar floor-1 window, already certified**:
`g_closed(⌈7q/25⌉,q) ≥ 1/λ³` (slope 0.28 > the true dwell slope; validated interval q=18..500) +
per-q Lean q≤16,18,20,21. **That corridor was already done — the (L1b) "genuine-corridor" work was
a wrong re-derivation of a solved object.**

## Corrected GATE-2 status (honest)
GATE-2 (genuine X_Ω(q≥18)=1/λ³, no sustained sub-threshold orbit) decomposes as:
1. **single-(q−1,1) / F-family corridor window — DONE** (= goal-N scalar window, certified + per-q Lean).
2. **(L2) switch glue — PROVEN** (F-family, all q; `BCZHeckeL2_composite_VERIFIED`).
3. **OPEN CRUX: deep-middle MULTI-BRANCH corridors (q≥17) + uniform (L2) over them.** Middle branches
   carry genuine P<thr; the single-corridor window argument must extend to ALL corridors, hardest for
   deep-middle ones where the scalar reduction fails (q≥16). The arc-width route never touched this.
   = exactly the memory's standing "uniform (L2) over deep-middle composites" open item.

## Verified bedrock still stands
`BCZHeckeGATE2Base_VERIFIED.lean` (casorati det=1 area-preservation + two-elliptic-generator
classification) — independently re-compiled, axiom-clean — unaffected by this refutation.

## Net
The workflow did NOT finish GATE-2. Its value: (a) caught a false/vacuous inequality before any
"finish" claim (adversarial verification working), (b) re-localized the real crux from the
arc-width inequality (mis-aimed; single-corridor already solved) to the **deep-middle multi-branch
corridors** — the genuinely hard, still-open piece. The session's "(L1b) is the one crux" framing
was wrong; this is the correction.

## Disposition of artifacts (NOT valid proofs — do not cite as GATE-2 progress)
`code/GATE2_L1b_arcwidth_derive.py`, `code/GATE2_L1b_arcwidth_interval.py` (the refuted derivation),
`lean/BCZHeckeGATE2_L1_skeleton.lean` (compiles modulo 1 `sorry`, but the sorry = the REFUTED target).
Kept as record only.

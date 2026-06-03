# STAGED DISPATCH — per-q floor-1 window certs (extend the proven band past q=17)

**Target:** machine-check, for each `q` in 18..30, the **floor-1 window lemma** (the new q≥18 piece):
no length-`L*(q)` in-domain floor-1 run stays sub-threshold. This is the goal-L window-lemma shape but for
the genuine floor-1 window `L*(q)≈q/4` (single `K=1` case — NO floor branching). Proving these EXTENDS the
machine-checked band concretely past q=17. See `FINDINGS_goalN_2026-06-03.md` §3b for the derivation.

## The statement (per q), Lean schema
`λ = 2cos(π/q)`, minpoly `hps` (degree `d=φ(2q)/2`); `c : ℕ → ℝ`, floor-1 iterates
`c_{n+2} = λ c_{n+1} − c_n`. Window length `L*(q)`. Prove:
```
theorem gq_floor1_window (lam : ℝ) (hps : <minpoly(lam)=0>) (h2 : 1 < lam) (h3 : lam < 2)
    (c : ℕ → ℝ) (hpos : ∀ n, 0 < c n)
    (hrec : ∀ n, c (n+2) = lam * c (n+1) - c n)             -- floor-1 (K=1) recurrence
    (hdom : ∀ n, c n + lam * c (n+1) > 1) :                  -- in-domain
    ¬ (∀ n, n < L* → c n * c (n+1) < 1 / lam^3)
```
Equivalently: the semialgebraic set `{(c0,c1) : c_n>0 ∧ c_n+λc_{n+1}>1 ∧ c_n c_{n+1}<1/λ³, n<L*}` is EMPTY
(all `c_n` linear in `(c0,c1)` via Chebyshev). **2 variables + ~2L* polynomial constraints** ⟹
Positivstellensatz-checkable (find the inconsistency certificate). Closed forms (verified, use as guides):
`c_n=r cos(nθ−ψ)`, `p_n=(r²/2)[λ/2+cos((2n+1)θ−2ψ)]`, domain `=r√(1+2λ²)cos(nθ−ψ+δ)>1`.

## Per-q parameters
| q | L*(q) | deg(minpoly) | note |
|---|---|---|---|
| 18 | 5 | 6  | START HERE (lowest deg) |
| 20 | 6 | 8  | |
| 21 | 6 | 6  | |
| 24 | 7 | 8  | |
| 19 | 6 | 9  | |
| 23 | 7 | 11 | heavy |
| 26 | 7 | 12 | heavy |
| 29 | 8 | 14 | heaviest |
| 30 | 9 | 8  | long window |
(others 22,25,27,28 similar). `L*` is the numeric crossing from `code/Ngoal_gbound.py` (≈q/4); verify the
exact `L*(q)` per q before emitting (use the largest L with `g(L,q)<thr`, then certify window `L*=that+1`).

## CONCRETE RESULT (2026-06-03): q=18 cert GENERATED via the goal-L emitter
The goal-L emitter `code/Lgoal_buildcore.py` is fully parametric in q — adding `WINDOW[18]=6` (and
treating q=18 as multi-root, so it carries `hlo:9/5<λ`, proven by `hecke_lam_lo`) and running
`python3 code/Lgoal_buildcore.py 18` EMITS `/tmp/lean-minus1/G18CORE.lean` (390 lines, W=6, deg-6 minpoly)
with the LP Positivstellensatz cert FOUND. So goal-L's machinery extends to q=18 directly: the scalar
window lemma `g18_no_window_below_genuine` (no 6 consecutive scalar sub-threshold products). Compile per
the HARD RULE (W=6 deg-6 ≈ q=16-heavy; `maxHeartbeats` may need raising). ⚠ GOTCHA: run the emitter from
the project root / `code/` dir, NOT `/tmp` (a stray `/private/tmp/inspect.py` shadows stdlib there).
Same pattern for q=19,20,…: set `WINDOW[q]=L*(q)` (≈⌈q/4⌉+1; verify via `code/Ngoal_gbound.py`), run, compile.

## How to produce (general)
Adapt the goal-L emitter `code/Lgoal_buildcore.py` (which made q=7..16): the floor-1 window is SIMPLER
(single `K=1` case, no floor-branch enumeration — drop the `Kmax`/floor-helper machinery), but the WINDOW
is longer (`L*` vs 4–5) so the Positivstellensatz is over more products. 2-variable, so a `(c0,c1)`-resultant
/ nullspace-LP cert + `linarith`/`linear_combination` (the goal-L/E pattern). W=`L*` files may need
`set_option maxHeartbeats 20000000`. Verify each per the HARD RULE (EXIT=0, axioms clean, no sorryAx).

## Caveat (honest scope)
This certifies the SCALAR floor-1 window only. The full genuine q≥18 lower bound additionally needs the
inter-run chaining (the kicks = the proven `(L2)` parabolic/hyperbolic step, Lean for the F-family). The
floor-1 window is the NEW, dominant difficulty; the chaining is the proven `(L2)`. Together ⟹ `(C′)` ⟹
`X_Ω(q)≥1/λ³` for the certified q, extending the band past 17.

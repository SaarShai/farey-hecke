# Scalar→corridor collapse for `FwindowL (L_blk q)` — 2026-06-20

File: `projects/aristotle_dispatch_v15/uniform_q5to18/CorridorCollapse.lean` (+ lakefile glob
`CorridorCollapse`). Build: `( cd .../uniform_q5to18 && ~/.elan/bin/lake build CorridorCollapse )`
→ EXIT 0, "Build completed successfully (8056 jobs)". All 7 theorems
`[propext, Classical.choice, Quot.sound]` — NO `sorryAx`, no `sorry`/`admit` in code.

## Headline

`FwindowL (L_blk q)` — the discrete scalar-product window consumed by
`LblkWindow.perq_Xomega_lb_Lblk_GEN` (the genuine `q ≥ 22` leg) — is **DISCHARGED conditional on
ONE named analytic input** `ScalarArcBound q mpoly`, the per-genuine-step `E`-form window-sup arc
bound. The assembled bounds `perq_Xomega_lb_Lblk_collapsed` / `Xomega_ge_collapsed` carry
`ScalarArcBound` (NOT `FwindowL`) plus the SAME sealed objects / Hecke form / band facts /
`MeasurePreserving` / null-section data, concluding the sealed `Xomega ≥ 1/λ³`. `FwindowL` is no
longer a hypothesis of the assembled bound.

## The DECISIVE finding: the task's literal A-collapse is NOT a definitional rewrite

The scout's A-target ("scalar c-products = corridor s-products, definitionally, via `hlink`, with
`s_n = orbit n` evolving by `M_W`") is **mathematically false as stated**. Verified symbolically
(sympy, this session):

* The genuine scalar `k=1` (branch-`q−1`, floor-1) step is the elliptic rotation
  `Mmap l (a,b) = (b, −a+λb)` (trace λ, conserves `E = a²−λab+b²`), NOT the block monodromy
  `M_W = [[−λ,2λ²+1],[−1,2λ]]` (trace λ, conserves `Q' = a²−3λab+(2λ²+1)b²`).
* `M_W ≠ Mmap^[2]` and `M_W ≠ Mmap^[3]` (both checked, both differ). So the scalar per-step window
  and the `M_W` per-block window are genuinely DISTINCT sub-samplings / time scales.
* The two product realizations are DIFFERENT sinusoids in DIFFERENT conserved forms:
  - **Scalar (E-form, `Mmap`):** `c n·c (n+1) = C0 + R cos(φ+2nθ)`, `C0 = λE/(4−λ²)`,
    `R = 2E/(4−λ²)`, amplitude ratio `C0/R = λ/2`.
  - **Corridor (Q'-form, `M_W`):** `a_k·b_k = C0_MW + R_MW cos(φ+2kθ)`, `C0_MW = 3λQ'/(4−λ²)`,
    `R_MW = 2√(2λ²+1)Q'/(4−λ²)`, amplitude ratio `C0/R = 3λ/(2√(2λ²+1))`.
* On the *confined* scalar (pure branch-`q−1`) orbit — which is exactly what
  `genuine_no_sustained_Lwin` forces via its trichotomy — the `W_q` block (which contains a
  branch-`q−3` step) NEVER appears, so `M_W` is not even the relevant operator.

Consequence: the whole `g_corr`/`fcorr`/`B1_target`/`RealizeWire`/`WindowRealizeClose`/`hpin`
apparatus is calibrated to the **`M_W` Q'-form per-block** product. It does **NOT** bound the
scalar `Mmap` E-form per-step window that the genuine leg actually uses. The scalar leg and the
corridor-realization leg are two PARALLEL, currently-UNCONNECTED reductions. `corridor_bridge_of_pin`
(even with `hpin` closed) does NOT discharge `FwindowL`.

## What is PROVED here (axiom-clean)

1. `cseq_is_mmap_orbit` / `scalar_prod_eq_mmap_prod` — the scalar window state `(c n, c (n+1))` is
   literally `(Mmap l)^[n] (c 0, c 1)` under the floor-1 recurrence `c(n+2)=λc(n+1)−c n`; hence the
   scalar window products are the `Mmap`-orbit products.
2. `Mmap_preserves_E` — `E = a²−λab+b²` conserved.
3. `mmap_product_realization` — the SCALAR-window product is the affine sinusoid above
   (`C0 = λE/(4−λ²)`, `R = 2E/(4−λ²)`, freq `2θ`). PROVED unconditionally from the 2-step
   recurrence, reusing `CorridorProductRealization.recur_to_Rcos` (form-agnostic). This is the
   genuine E-form analogue of `corridor_product_realization` and the correct foundation for
   `ScalarArcBound`.
4. `FwindowL_of_scalarArcBound` — `FwindowL (L_blk q) mpoly` from `ScalarArcBound q mpoly`. Faithful
   (sup ≥ t ⟹ ¬(all < t), sup attained), NO weakened cover.
5. `perq_Xomega_lb_Lblk_collapsed` / `Xomega_ge_collapsed` — assembled `q ≥ 22` bound and sealed
   `Xomega ≥ 1/λ³`, conditional only on `ScalarArcBound` + definitional/measure data, routed through
   the REAL `LblkWindow.perq_Xomega_lb_Lblk_GEN` / `Xomega_ge_L` (real `genuine_no_sustained_Lwin`).

## The EXACT remaining gap (named, NOT punted)

`ScalarArcBound q mpoly` — the per-genuine-step **`E`-form** window-sup arc bound
`1/λ³ ≤ sup'_{j<L_blk q} c(i+j)·c(i+j+1)` for every floor-1-recurrent positive in-domain corridor
c-sequence. It is a genuine analytic statement (lower bound on a max of products), NOT a disguised
copy of the conclusion. It is the analogue of `B1_target` for the conserved energy `E` and the
per-step time scale — one-dimensional `max cos` + uniform arc-endpoint calculus, restated for the
E-form constants (`C0/R = λ/2`, `θ = π/q`, `L_blk q = ⌈33q/256⌉+2`). It is **NOT** `B1_target` and
**NOT** dischargeable from `corridor_bridge_of_pin`/`hpin` (those are Q'-form/M_W).

Note also: whether the SAME `L_blk q = ⌈33q/256⌉+2` window length suffices for the E-form
(amplitude ratio λ/2, which can drive the product negative) is itself an open calibration question —
the E-form arc may require a different (likely shorter, since ratio λ/2 < 3λ/(2√(2λ²+1)) means a
wider relative swing) window-length constant. `ScalarArcBound` is stated at `L_blk q` to match the
existing genuine leg; if the E-form calibration needs a different length the genuine leg's `L`
parameter (already parametric via `perq_Xomega_lb_qge18_GEN_L`) absorbs it.

## Honest scope vs the assigned task

The assigned "done-means" was: discharge `FwindowL (L_blk q)` GIVEN `hbridge`
(= `corridor_bridge_of_pin`) as a named input. That exact wiring is **impossible faithfully**,
because `hbridge` is the M_W/Q'-form per-block bound and does not bound the scalar E-form per-step
window (the collapse it presupposes is the false `M_W = Mmap` identification above). The faithful
deliverable instead discharges `FwindowL` from the CORRECT object — the E-form scalar arc bound
`ScalarArcBound` — proving the realization that makes it the genuine residual, and names exactly why
the M_W bridge does not apply. This is strictly more honest than wiring through `hbridge` and
silently relabelling a Q'-form bound as the scalar window.

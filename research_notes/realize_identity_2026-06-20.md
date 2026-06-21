# Corridor realization identity (goal A) — 2026-06-20

**Task.** Prove the corridor realization identity that discharges `hbridge` (= `g_corr ≤ g_true`),
the SOLE remaining open input of the `q ≥ 22` lower-bound chain
(`LblkWindow.perq_Xomega_lb_Lblk_GEN`'s `FwindowL (L_blk q) mpoly`).  This is the corridor analog
of the energy-route `pgen_orbit_realization` (PROVED in `hsa_realization_lean/RequestProject/Main.lean`).

## VERIFIED RESULT (axiom-clean, `lake build` EXIT 0)

Two orbit-observable sinusoid identities — the genuine R1 core of `hbridge` — PROVED sorry-free,
`#print axioms = [propext, Classical.choice, Quot.sound]` (NO `sorryAx`):

File `projects/aristotle_dispatch_v15/uniform_q5to18/CorridorProductRealization.lean`
(source also at `projects/realize_identity_lean/CorridorProductRealization.lean`):

1. **`corridor_product_realization`** — the PRODUCT observable `P k = (M_W^[k] s0).1 · (M_W^[k] s0).2`
   along the `M_W`-block rotation orbit is the affine sinusoid
       `P k = C0 + R·cos(φ + 2kθ)`,   `θ = π/q`,
   with EXACT constants `C0 = 3λ·Qp/(4−λ²)`, `R = 2√(2λ²+1)·Qp/(4−λ²)`, `R > 0` (on `Qp > 0`).
   The doubled frequency `2θ` (vs the map's `θ`) is because `P` is degree-2 in the rotating
   coordinates; the product recurrence is `P(k+2) = (λ²−2)·P(k+1) − P(k) + 3λ·Qp` and
   `2cos(2θ) = λ²−2`.  Constants derived + cross-checked symbolically (sympy).

2. **`corridor_domain_realization`** — the in-domain (lower-Taha-edge) observable
   `D k = (M_W^[k] s0).1 + λ·(M_W^[k] s0).2` is the single-frequency sinusoid
       `D k = Damp·cos(ψ + kθ)`,
   amplitude-pinned `Damp²·sin²θ = (6λ²+1)·Qp` (`= r²·Blam²`, the `fcorr`-denominator radius).
   Frequency `θ` (not `2θ`): `D` is degree-1 in the rotating coordinates.

Both built against the inner project (`MW_preserves_Qp` = `M_W` conserves `Qp`, also proved).
Build command (EXIT 0):
```
( cd projects/aristotle_dispatch_v15/uniform_q5to18 && ~/.elan/bin/lake build CorridorProductRealization )
```

### Wiring file (axiom-clean): `RealizeWire.lean`

`projects/aristotle_dispatch_v15/uniform_q5to18/RealizeWire.lean` states the `hbridge` conclusion
in the `L1bArcCoverage` vocabulary (`g_corr`, `fcorr`, `windowMaxCos`) and PROVES it from ONE
precisely-named residual:

* `WindowProductRealizes q hL P` — the value-of-`fcorr` realization: for each window start `N`,
  there is a domain `muc` with `fcorr(muc) ≤ sup'_{j<L} P(N+j)`.
* `hbridge_of_realizes` — `g_corr ≤ sup'_{j<L} P(N+j)` from the residual (the `sInf`-le-value step
  `csInf_le` + `g_corr_image_bddBelow`).  **PROVED axiom-clean.**
* `window_not_subthreshold` — combines with PROVED `B1_target` to give `1/λ³ ≤ sup'_{j<L} P(N+j)`,
  the `FwindowL`-shaped conclusion the genuine chain consumes.  **PROVED axiom-clean** (modulo the
  named residual).

## HONEST SCOPE — what the scout got right, and what it overcalled

**Right:** The genuinely HARD analytic crux of the whole program (the uniform `O(1/q²)`
escape-margin `L1b_target`/`fcorr_lb`) was ALREADY discharged axiom-clean as `B1_target`.  The
remaining `hbridge` is NOT that hard core.  And R1 — the sinusoid realization — IS the direct
analog of `pgen_orbit_realization` and is now PROVED here.

**Overcalled:** the scout framed `hbridge` as a near copy-paste of `pgen_orbit_realization` plus a
trivial `sup'`-le step.  It is more than that.  Reading the actual `g_corr`/`fcorr` construction
(`code/GATE2_L1b_arcwidth_interval.py`, lines 28–44) shows `g_corr ≤ g_true` is an INEQUALITY CHAIN
with THREE genuine sub-steps, not an identity substitution:

  (R2a) product numerator: `sup'_j P(N+j) = (r²/2A2)[3λ/2 + √A2·windowMaxCos(μc)]` — supplied by
        `corridor_product_realization` AFTER reconciling conventions:
        the python `r²` is NOT `Qp` but `r² = 4(2λ²+1)·Qp/(4−λ²)` (verified — both `C0` and `R`
        imply the same `r²`, internally consistent).
  (R2b) **in-domain radius forcing**: `Dom_n > 1` for ALL `L` window steps ⟹ `r² ≥ r_min² =
        1/(Blam²·cos²(|μc|+H))`.  This is the SECOND observable identity
        `corridor_domain_realization` PLUS a window-MIN argument over the in-domain constraint.
        This step is the linchpin that produces `fcorr`'s `cos²(|μc|+H)` denominator and has NO
        analog in the energy route's `pgen_orbit_realization` (which used a fixed `E`-floor, not a
        per-window in-domain min).  It is new work; I proved the identity it rests on but not the
        full window-min forcing.
  (R2c) phase-grid alignment `(φ, N) ↦ μc` matching my `cos(φ+2kθ)` grid to `windowMaxCos`'s
        `cos(2(μc−ξ)+(2n−(L−1))θ+η)` grid, plus `μc ∈ domain`, plus `3λ/2+√A2·windowMaxCos ≥ 0`.

`WindowProductRealizes` packages exactly (R2a)+(R2b)+(R2c).  R1 (both sinusoid identities, the
substantive new mathematics) is PROVED; the residual is the phase-alignment + in-domain-min
assembly, stated precisely as a `Prop` (named, NOT a `sorry`).

## What remains (the exact blocking step, named)

`RealizeWire.WindowProductRealizes q hL P` is the single remaining open input.  Its proof requires:
1. choosing `μc := (φ + 2Nθ + (L−1)θ − η)/2 + ξ` (or the reflection) so the product grid aligns;
2. the in-domain window-min forcing `r² ≥ 1/(Blam²cos²(|μc|+H))` from `corridor_domain_realization`
   + `∀ n<L, Dom(N+n) > 1` (the orbit stays in Taha across the window);
3. `μc ∈ Ioo(...)` and `3λ/2+√A2·windowMaxCos ≥ 0` at the relevant `μc`.
   NOTE (corrected): `3λ/2 > √A2` by a TINY margin (e.g. `+0.0051` at q=18, `→0⁺` as q→∞), so the
   bracket is NOT non-negative for all `windowMaxCos ∈ [−1,1]` — it dips slightly negative only when
   `windowMaxCos ≈ −1`.  At the realized `μc` the numerator is positive because `fcorr ≥ 1/λ³ > 0`
   on the whole domain (PROVED `fcorr_lb`); so the monotone-in-`r²` step (R2a) uses numerator `> 0`
   from `fcorr_lb`, not a naive `≥ 0` bound.  (My earlier `√A2 ≥ 3λ/2` claim was BACKWARDS.)

These are routine-but-real (est. 150–250 lines of `Real.cos`/`Finset.sup'` bookkeeping).  None is
the hard analytic core — that was `B1_target`, already done.

## Files written (disjoint, assigned paths only)
- `projects/realize_identity_lean/CorridorProductRealization.lean`  (source)
- `projects/realize_identity_lean/RealizeWire.lean`                  (source)
- copies in `projects/aristotle_dispatch_v15/uniform_q5to18/` + globs in `lakefile.toml`
  (`CorridorProductRealization`, `RealizeWire`) so they build against the genuine chain.
- this note.

## Numerics cross-check (sympy)
- product recurrence offset `= 3λ·Qp` (k-independent); `C0 = 3λQp/(4−λ²)`, `R² = 4(2λ²+1)Qp²/(4−λ²)²`.
- domain invariant `D0²−λD0D1+D1² = (6λ²+1)·Qp`; `Damp²sin²θ = (6λ²+1)Qp = r²Blam²` with the same `r²`.
- `r² = 4(2λ²+1)Qp/(4−λ²)` reconciles both observable conventions to the python `product_form`.

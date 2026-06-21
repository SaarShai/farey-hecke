# L_blk window parametrization — GEN' window length lifted from fixed 6 to parametric L

Date: 2026-06-20/21 · Author: A-window prover (fleet) · File:
`projects/lblk_window_lean/LblkWindow.lean` (verified inside `uniform_q5to18/`).

## Goal

Generalize the genuine no-sustained window lemma from the FIXED window length 6 (the only
remaining "cap" in the GEN' leg) to a PARAMETRIC length L, wire it back to the sealed
`Xomega ≥ 1/λ³` chain, and instantiate at `L := L_blk q` using the PROVED
`L1bArcCoverage.B1_target` (∀ q≥18, 1/λ³ ≤ g_corr(L_blk q) q).

## What is PROVED (sorry-free, axiom-clean `[propext, Classical.choice, Quot.sound]`)

All inside `LblkWindow.lean`, verified by `lake build LblkWindow` from `uniform_q5to18/`,
EXIT 0, `Build completed successfully (8052 jobs)`, sorryAx GONE on every result:

1. `FwindowL (L : ℕ) (mpoly)` — the window hypothesis at parametric length L, stated in the
   uniform shape `∀ i, ¬ (∀ j < L, c(i+j)·c(i+j+1) < 1/λ³)`. Same band/corridor
   preconditions as the original `Fwindow6`.
2. `Fwindow6_iff_FwindowL6` — bridge `Fwindow6 mpoly ↔ FwindowL 6 mpoly` (exact index
   match: the 6 explicit conjuncts c(i+0)·c(i+1)…c(i+5)·c(i+6) = ∀ j<6).  So L=6 recovers
   the existing window with ZERO loss.
3. `genuine_no_sustained_Lwin (L)` — the genuine no-sustained replay at length L. Body is
   VERBATIM `ToplevelStitchGen.genuine_no_sustained_6win` (trichotomy, scalar→Dcorr P1,
   cusp guards, deep-mid SOS ejection `genuine_hEject_deepmid` — all length-independent);
   the ONLY changed line is the final F-window invocation, which supplies the L-indexed
   family `fun j _ => hsubc j` instead of the hardcoded 6-tuple.
4. `perq_Xomega_lb_qge18_GEN_L (L)` — the L-parametric genuine lower bound on the sealed
   `Tgen`/`Pgen`: `1/l^3 ≤ essSup (Pgen l) μ`. Exactly `perq_Xomega_lb_qge19_GEN'` with
   `Fwindow6 → FwindowL L`. `hGen` discharged internally via `Tgen_orbit_genuine`. Carries
   the SAME hHecke, four band facts, MeasurePreserving(Tgen), μ(section)ᶜ=0 — none weakened.
5. `perq_Xomega_lb_GEN_L6_recovers` — SOUNDNESS: instantiating L:=6 (Fwindow6 via the
   bridge) reproduces `perq_Xomega_lb_qge19_GEN'` exactly. Proves the parametrization did
   not silently change/weaken the q=19,20,21 legs.
6. `closed_section_lb_L (L)` / `XomegaSet_bddBelow_L (L)` / `Xomega_ge_L (L)` — the L-param
   wiring all the way to the SEALED `OnsetEquality.Xomega` (= sInf XomegaSet). Mirror of
   `OnsetEquality.closed_section_lb → XomegaSet_bddBelow → Xomega_ge` with `Fwindow6 →
   FwindowL L` swapped only in the OPEN branch (cusp-line branch is window-independent,
   copied verbatim). Conclusion `1/l^3 ≤ Xomega l m B` on the genuine sealed object.
7. `Lblk_g_corr_bound` — re-export of the PROVED continuous half
   `L1bArcCoverage.B1_target`: ∀ q≥18, 1/λ³ ≤ g_corr(L_blk q) q (axiom-clean).
8. `perq_Xomega_lb_Lblk_GEN (q)` — the genuine lower bound specialized to L := L_blk q,
   taking the discrete length-`L_blk q` window `FwindowL (L_blk q) mpoly` as the single
   named input.

## The HONEST remaining gap (named, NOT a sorry)

The task framing ("instantiate L := L_blk with B1_target to extend to all q≥18") rests on a
bridge that does NOT exist as a proved fact in the buildable genuine chain:

- `B1_target` proves the CONTINUOUS arc-width bound `1/λ³ ≤ g_corr(L_blk q) q`, where
  `g_corr` is an infimum of a cosine functional (the corridor block-window max-product
  LOWER bound).
- `perq_Xomega_lb_qge18_GEN_L` consumes the DISCRETE scalar-product window
  `FwindowL (L_blk q) mpoly` (∀ i, ¬ ∀ j<L_blk, c(i+j)·c(i+j+1) < 1/λ³).
- The bridge `g_corr-bound ⟹ discrete-window` is the corridor REALIZATION `g_corr ≤ g_true`
  (the `product_form` orbit realization). In the repo this is `no_sustained_corridor`'s
  `hbridge` HYPOTHESIS in `mimo-mini-project/lean/BCZHeckeGATE2_L1_skeleton.lean` — which is
  (a) NOT in the buildable `uniform_q5to18/` subproject (no .olean, not globbed), and
  (b) carried as a hypothesis even there, with that file's `L1b_target` itself a `sorry`.

So the chain is: PROVED `FwindowL` parametrization + PROVED L=6 recovery + PROVED wiring to
sealed Xomega + PROVED continuous bound `B1_target`, REDUCED to ONE named open input —
`FwindowL (L_blk q) mpoly` (the corridor `g_corr ≤ g_true` realization). The all-q≥18
extension is NOT unconditional: it is `perq_Xomega_lb_Lblk_GEN` modulo that single discrete
realization, exactly the same gap memory already records for the corridor route ("realization
bridge" / hbridge), now isolated to one hypothesis at parametric length.

## Net status vs prior

- The "fixed 6 window" cap in the GEN' leg is DISSOLVED into a parameter L (PROVED).
- q=19,20,21 unchanged (L=6 recovery PROVED ⟹ no regression).
- q≥22 reduced to ONE discrete corridor-realization input `FwindowL (L_blk q)`; the
  continuous analytic half it would need (`g_corr ≥ 1/λ³`) is PROVED (`B1_target`).
- NOT a fully unconditional all-q≥18 onset bound — the corridor realization
  (`g_corr ≤ g_true` / hbridge) is the residual, and it is NOT in the buildable chain.

## Verify

See `projects/lblk_window_lean/VERIFY.md`. Edits to `uniform_q5to18/` (temp copy + glob)
were reverted; lakefile restored identical to backup, no stray LblkWindow artifacts.

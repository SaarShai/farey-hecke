# Realization-bridge scope: discharging `FwindowL (L_blk q)` for q>=22 — SCOUT 2026-06-20

## The exact residual

`LblkWindow.perq_Xomega_lb_Lblk_GEN` proves the genuine onset lower bound `X_Omega(q) >= 1/lambda^3`
for q>=22 (m>=2, the band 9/5 < lambda < 2 ⟺ q>=22), CONDITIONAL on ONE named hypothesis:

    hFW : FwindowL (L1bArcCoverage.L_blk q) mpoly

`FwindowL L mpoly` (def in LblkWindow.lean §1) is the DISCRETE scalar-product window:

    ∀ lam, mpoly lam → 1<lam<2 → 9/5<lam → ∀ c:ℕ→ℝ, (0<c) (c≤1)
      (c n + lam·c(n+1) > 1) (lam·c n + c(n+1) > 1)
      (c n + c(n+2) = ⌊(1+c n)/(lam·c(n+1))⌋·lam·c(n+1))   -- genuine floor recurrence
      → ∀ i, ¬ (∀ j < L, c(i+j)·c(i+j+1) < 1/lam^3)

i.e. NO genuine corridor orbit keeps the scalar product `c_n·c_{n+1}` strictly below `1/lambda^3`
for `L_blk q` consecutive steps.

## (1) The exact `g_corr <= g_true` statement needed

`g_true` is NOT a Lean def in L1bArcCoverage.lean; it is the prose name for the **true block-window
max-product** along the corridor orbit. The bridge that discharges `FwindowL (L_blk q)` is exactly
`BCZHeckeGATE2_L1_skeleton.no_sustained_corridor`'s hypothesis `hbridge`:

    hbridge : (haCheb: ∀n, s(n+2).1 = lam·s(n+1).1 − s n.1)
            → (hbCheb: ∀n, s(n+2).2 = lam·s(n+1).2 − s n.2)
            → (hQ:     ∀n, Qp lam (s n) = Qp lam (s 0))            -- M_W-ellipse conserved
            → (∀n, 0<s n.1) (∀n, 0<s n.2) (∀n, s n.1 + lam·s n.2 > 1)
            → (hP: ∀n, P n = s n.1 · s n.2)                        -- product observable
            → ∀ N, g_corr (L_blk q) q hLpos
                    ≤ (Finset.range (L_blk q)).sup'
                        (nonempty) (fun j => P (N+j))

In words: **along any M_W-Chebyshev corridor orbit, the block-window max product
`max_{j<L_blk} P(N+j)` is >= `g_corr (L_blk q) q`** (= `sInf_{μc} fcorr`). Call the LHS window-max
`g_true`; the statement needed is the single line `g_corr <= g_true`, i.e.
`g_corr (L_blk q) q <= sup'_{j<L_blk} P(N+j)`.

`no_sustained_corridor` is FULLY PROVED modulo `hbridge` + `L1b_target` (the latter is now PROVED
as `L1bArcCoverage.B1_target`, axiom-clean). So the LAST open input of the q>=22 chain is precisely
`hbridge`, and `hbridge`'s mathematical content is `g_corr <= g_true`.

## (2) DIFFICULTY CALL: TRACTABLE realization identity — NOT the hard corridor core

This is a **tractable realization identity**, the direct corridor analog of the energy-route
`pgen_orbit_realization` which is **already PROVED axiom-clean** in
`projects/hsa_realization_lean/RequestProject/Main.lean` (theorem `pgen_orbit_realization`,
~150-line self-contained proof). Evidence:

- **Same observable-along-orbit mechanism.** Energy route: `Pgen(a,b)=a(a+λb)/λ` is a quadratic
  form; along the `Mmap` rotation orbit `Pgen(M^k p) = C0 + R·cos(φ + 2kθ)` (R>0), proved via the
  2-step linear recurrence `hseq(k+2)=2cos(2θ)·hseq(k+1)−hseq k` → `recur_to_Rcos` closed form,
  with E (the ellipse) conserved giving the amplitude invariant. The CORRIDOR observable
  `P_n = a_n·b_n` is ALSO a quadratic form on the SAME M_W rotation orbit (same Chebyshev
  recurrence `haCheb`/`hbCheb`, same conserved ellipse `Qp`), so the IDENTICAL recurrence→sinusoid
  closed form applies: `P(N+j) = C0' + R'·cos(φ' + 2jθ)`.

- **`fcorr` IS that sinusoid-form, by construction.** `fcorr(L,q,μc) =
  (3λ/2 + √A₂·windowMaxCos(L,q,μc)) / (2·A₂·Blam²·cos²(|μc|+H))` and `windowMaxCos =
  sup'_{n<L} cos(2(μc−ξ) + (2n−(L−1))θ + η)`. The phase grid `2(μc−ξ)+(2n−(L−1))θ+η` is exactly
  the orbit phase `φ'+2nθ` re-centered; `g_corr = sInf_μc fcorr` is the worst-case orbit phase.
  So `fcorr(L,q,μc_orbit) = g_true` (the window-max product, at the orbit's actual phase μc), and
  `g_corr = sInf_μc fcorr <= fcorr(μc_orbit) = g_true` is **definitional sInf-le-value** once the
  orbit-phase identity `P(N+j) = the fcorr numerator at phase μc` is established.

- **The window-max pigeonhole is ALREADY PROVED** in the covering project: `cos_grid_hit`
  (`hsa_covering_lean/aristotle_covering/.../Main.lean`) proves that among the equally-spaced phases
  `φ+2kθ`, k<q, SOME k has `cos(φ+2kθ) >= cos(π/q)` — the exact pigeonhole feeding `windowMaxCos`'s
  lower bound, and `arc_coverage_ineq` (`2·arccos(2√6/5)/π < 33/256`) sizes `L_blk q` so the window
  of `L_blk` phases covers the super-threshold arc. Both PROVED axiom-clean.

- **It is NOT the genuine hard corridor core.** The genuinely hard analytic crux of this program
  was `L1b_target` / `fcorr_lb` (the uniform O(1/q²) escape-margin, the sharp `max cos` +
  arc-endpoint control) — and that is **already discharged** as `B1_target`/`fcorr_lb`, axiom-clean.
  What remains (`hbridge` = `g_corr<=g_true`) is the WIRING that the orbit observable realizes the
  `fcorr` form — pure algebra (quadratic form in rotating coordinates + double-angle), exactly the
  class of `pgen_orbit_realization`, which is done.

**Caveat / the one real subtlety:** the energy route's `pgen_orbit_realization` is stated for the
`Pgen=a(a+λb)/λ` observable; the corridor `hbridge` uses `P=a·b`. These differ by `a²/λ` (i.e.
`Pgen = P + a²/λ`). On branch q−1 the `product_form` collapses the genuine observable to `a·b`
(X(q−1)=0, X(q−2)=1), so `P=a·b` is the right corridor observable; the realization must be redone
for `a·b` (not literally reused from `pgen_orbit_realization`). But `a·b` is the SAME degree-2
quadratic form on the SAME rotation orbit, so the same recurrence→`R·cos` proof applies verbatim
with different constants C0',R',φ' — mechanical, low-risk. This is the only piece of genuine (but
routine) work.

## (3) Targets

### A — realization_target (the corridor identity to PROVE)
`corridor_pgen_realization`: for q=m+2, m>=2, l=lamq q, a corridor block-boundary point
`s0=(a0,b0)` with `a0,b0>0`, on the lower Taha edge `a0+λb0>1`, evolving by the M_W block step
`hblk` (⟺ Chebyshev `haCheb`/`hbCheb` + conserved `Qp`-ellipse), the product observable
`P_k = (s_k).1·(s_k).2` satisfies

    ∃ C0 R phi, 0 < R ∧ ∀ k, P k = C0 + R·cos(phi + 2k·(π/q))

AND the threshold/phase alignment yielding, for the windowMaxCos phase grid,

    g_corr (L_blk q) q  ≤  sup'_{j<L_blk q} P(N+j)     (= g_true)

for every N. (Proof: recurrence `P(k+2)=2cos(2θ)P(k+1)−P k` from `haCheb`/`hbCheb`+`hQ`;
`recur_to_Rcos`; amplitude from `Qp` conservation; then `g_corr=sInf fcorr <= fcorr(μc)=`window-max
via `cos_grid_hit`+`arc_coverage_ineq`. Pattern: clone `pgen_orbit_realization` with observable
`a·b` and supply the windowMaxCos sup'-le step.)

### B — wire_target (assemble unconditional q>=22)
`perq_Xomega_lb_Lblk_GEN_unconditional`: instantiate `LblkWindow.perq_Xomega_lb_Lblk_GEN` (or its
sealed-`Xomega` form `Xomega_ge_L` at `L:=L_blk q`) by discharging `FwindowL (L_blk q) mpoly` from
`corridor_pgen_realization` (A) routed through `BCZHeckeGATE2_L1_skeleton.no_sustained_corridor`
(feeding `hbridge := corridor_pgen_realization`, `L1b_target := B1_target`), obtaining
`¬(∀n, P n < 1/λ^3)` over L_blk-windows = `FwindowL (L_blk q) mpoly`. Then the inf step:
`X_Omega(q) >= 1/λ^3` for all q>=22, axiom-clean (no sorryAx). Combine with the PROVED q<=21
leg for the full all-q unconditional onset lower bound.

## Named hypothesis to discharge (exact)
- In `LblkWindow.perq_Xomega_lb_Lblk_GEN` (LblkWindow.lean §6):
  `hFW : LblkWindow.FwindowL (L1bArcCoverage.L_blk q) mpoly`
  (parametric-length window, def LblkWindow.FwindowL).
- Its mathematical content = `BCZHeckeGATE2_L1_skeleton.no_sustained_corridor`'s
  `hbridge` (the `g_corr <= g_true` window-max realization), with `L1b_target` already PROVED as
  `L1bArcCoverage.B1_target`.

## Files
- `/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v15/uniform_q5to18/LblkWindow.lean`
  (perq_Xomega_lb_Lblk_GEN, FwindowL, Xomega_ge_L, Lblk_g_corr_bound)
- `/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v15/uniform_q5to18/L1bArcCoverage.lean`
  (g_corr, fcorr, windowMaxCos, L_blk, B1_target=L1b PROVED, fcorr_lb PROVED, arc_coverage_ineq)
- `/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v15/uniform_q5to18/ToplevelStitch.lean`
  (L1b_carried; hbridge/g_corr<=g_true NOT here — it lives as hbridge in the skeleton)
- `/Users/za/Documents/farey-hecke/projects/mimo-mini-project/lean/BCZHeckeGATE2_L1_skeleton.lean`
  (no_sustained_corridor + the EXACT hbridge signature; L1b_target sorry there, but PROVED upstream)
- `/Users/za/Documents/farey-hecke/projects/hsa_realization_lean/RequestProject/Main.lean`
  (pgen_orbit_realization — the PROVED energy-route analog, the template for target A)
- `/Users/za/Documents/farey-hecke/projects/mu_close_hSuperArc_lean/aristotle_realization/RequestProject/Main.lean`
  (pgen_orbit_realization as the single `sorry` — confirms it IS the realization residual class)
- `/Users/za/Documents/farey-hecke/projects/hsa_covering_lean/aristotle_covering/RequestProject/Main.lean`
  (cos_grid_hit — PROVED window pigeonhole feeding windowMaxCos)

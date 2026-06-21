# Cross-project close SCOUT — 2026-06-20

## Headline
The skeleton's `no_sustained_corridor` (mimo-mini-project) does **NOT** need porting. The
`uniform_q5to18` project has already INDEPENDENTLY re-implemented its entire functional content,
axiom-clean and lake-build-verified (8030 jobs, EXIT 0, all `[propext, Classical.choice, Quot.sound]`).
The cross-project gap is therefore NOT a port; it is the SAME two residuals already named in
`uniform_q5to18`: (1) the discrete `FwindowL (L_blk q)` window (= `RealizeWire.window_not_subthreshold`
conclusion, conditional on `WindowProductRealizes`), and (2) `hpin` (the in-domain radius/phase datum).

## (1) no_sustained_corridor signature + deps
`BCZHeckeGATE2_L1_skeleton.lean:233-311`, namespace `GATE2L1`. File imports ONLY `Mathlib`.
Hyps: `q≥18`; `s:ℕ→ℝ×ℝ`; `hblk` (M_W block step); `hpos1/hpos2`; `hdom` (a+λb>1); `P:ℕ→ℝ`,
`hP` (P n = a_n·b_n); `hLpos`; `hbridge` (the closed-form realization: derived Chebyshev recurrences
+ conserved Qp ellipse + in-domain + product ⟹ `g_corr (L_blk q) q hL ≤ sup'_{j<L_blk q} P(N+j)`).
Concl: `¬(∀n, P n < 1/λ³)`. PROOF is self-contained: derives `haCheb/hbCheb` (via `arec/brec`),
`hQ` (via `MW_preserves_ellipse`), invokes `L1b_target` (the file's SOLE `sorry`) + `hbridge`,
contradicts sub-threshold by sup'-pigeonhole. Abstract deps = NONE beyond Mathlib; `L1b_target` is a
local `sorry` (the continuous arc bound), `hbridge` is a hypothesis. NOT importing the genuine chain.

## (2) Port method — NOT NEEDED
The functional content already lives in `uniform_q5to18`, split across PROVED files:
- `L1bArcCoverage.B1_target` (= the skeleton's `L1b_target`, here PROVED not sorry): `1/λ³ ≤ g_corr (L_blk q) q`.
- `RealizeWire.hbridge_of_realizes` (= the skeleton's `hbridge`, here PROVED from ONE named Prop
  `WindowProductRealizes`): `g_corr ≤ sup'_{j} P(N+j)`.
- `RealizeWire.window_not_subthreshold`: chains the two → `1/λ³ ≤ sup' P(N+j)` (the sub-threshold contradiction).
- `LblkWindow.genuine_no_sustained_Lwin` + `perq_Xomega_lb_Lblk_GEN`: the genuine-chain replay
  consuming `FwindowL (L_blk q)` (the DISCRETE scalar window), wired to sealed `Xomega`.
If a literal port were ever wanted: copy `BCZHeckeGATE2_L1_skeleton.lean` (Mathlib-only, no cross-deps)
→ rename namespace, add `[[lean_lib]] name="GATE2L1Skel" globs=["BCZHeckeGATE2_L1_skeleton"]` to the inner
lakefile.toml, `lake build GATE2L1Skel`. It would compile (only `L1b_target` sorry). But it is REDUNDANT.

## (3) scalar→corridor product COLLAPSE (the wiring statement)
`FwindowL` (LblkWindow.lean:72) is the DISCRETE SCALAR window over `c:ℕ→ℝ` (= orbit.1 first-coords):
`∀i, ¬(∀ j<L, c(i+j)·c(i+j+1) < 1/λ³)`. `no_sustained_corridor`/`hbridge` use the CORRIDOR product
`P n = s_n.1 · s_n.2` (= a_n·b_n). The COLLAPSE that wires them, on the k=1 corridor:
  **On the genuine scalar branch q−1, the scalar genuine step IS the M_W block step, so the scalar
  block-boundary state `s_n = ((orbit n).1, (orbit (n+1)).1)` and the scalar c-product
  `c(i+j)·c(i+j+1) = (orbit (i+j)).1·(orbit(i+j+1)).1` EQUALS the corridor s-product `P_{i+j} = s.1·s.2`.**
This is exactly `genuine_no_sustained_Lwin`'s `hlink`/`hsubc` step (LblkWindow.lean:186-199):
`hlink n : (orbit (n+1)).1 = (orbit n).2`, giving `c(n)·c(n+1) = (orbit n).1·(orbit n).2 = P_n`.
So the collapse is ALREADY discharged inside `genuine_no_sustained_Lwin` via `orbit_to_cseq_in_Dcorr`
(`hlink`) — the corridor s-product = scalar c-product is the `hlink`-rewrite. The remaining wire is:
feed `RealizeWire.window_not_subthreshold` (corridor side, `1/λ³ ≤ sup' P`) as the `FwindowL (L_blk q)`
input. The exact collapse identity: `(orbit n).1·(orbit(n+1)).1 = (orbit n).1·(orbit n).2 = s_n.1·s_n.2`
under `hlink n : (orbit(n+1)).1 = (orbit n).2`.

## (4) hpin — EXACT statement + tractability
`hpin` (WindowRealizeClose.lean:230-248, the input to `windowProductRealizes_corridor`), per `N`:
∃ base muc, `muc ∈ Ioo(-(π/2−H), π/2−H)` ∧ (phase alignment eqn) ∧ (product window phase = base) ∧
**RADIUS FORCING**: `1 ≤ (4·A2q·Qp/(4−λ²))·Blamq²·cos²(|muc|+H)`  (= `r²·Blam²·cos²(|muc|+H) ≥ 1`).
Equivalently `r·Blam·cos(|muc|+H) ≥ 1`. The amplitude/phase data needed are ALL proved sinusoids:
- `corridor_domain_realization`: `D k = a_k+λb_k = Damp·cos(ψ+kθ)`, `Damp²sin²θ = (6λ²+1)Qp`.
- `corridor_antidomain_realization` (WindowRealizeClose.lean:320): `D' = a−λb = Damp'·cos(ψ'+kθ)`, `Damp'²sin²θ=Qp`.
- product decomposition `a·b = ((a+λb)²−(a−λb)²)/(4λ)` (PROVED, line 386).

### Tractability: GENUINELY BLOCKED (no unconditional shortcut), as the state note says.
The radius forcing `r·Blam·cos(|muc|+H) ≥ 1` needs `D_{N+j} > 1` (in-domain) at the window FAR-ENDPOINT
to pin the conserved radius from below. The sinusoids give `D` as an EXACT cosine of amplitude `Damp`
with `Damp² = r²Blam²` (pinning PROVED), but the lower bound `cos(|muc|+H)` at the specific far-endpoint
phase requires knowing the orbit's actual phase `ψ` lands the window inside the in-domain arc — i.e. the
phase-grid alignment `muc = ψ + Nθ + H` must place `|muc|+H < π/2` (domain membership) AND the endpoint
`D > 1`. This is genuine in-domain orbit GEOMETRY: it is TRUE for any orbit that actually stays in the
corridor for `L_blk q` blocks (that is the hypothesis being contradicted), but proving it unconditionally
from the sinusoids alone is NOT available — the phase `ψ` and offset are orbit-specific, and the
`D>1`-at-far-endpoint is exactly the "no escape before L_blk" content. So `hpin` is the irreducible
analytic residual: provable per-orbit GIVEN it stays in-domain, but the unconditional all-q,all-orbit
form is blocked (matches prior analysis: "hpin is genuine in-domain orbit geometry, no unconditional shortcut").

## Build evidence
`( cd .../uniform_q5to18 && ~/.elan/bin/lake build WindowRealizeClose )` → EXIT 0, Build completed (8030 jobs).
All of `B1_target`, `corridor_{product,domain}_realization`, `hbridge_of_realizes`,
`window_not_subthreshold`, `windowProductRealizes_{of_data,corridor}`, `corridor_antidomain_realization`,
`corridor_bridge_of_pin` → `[propext, Classical.choice, Quot.sound]` (axiom-clean, no sorryAx).

## NET
Two residuals remain, EXACTLY as STATE says, both already named in `uniform_q5to18` (NOT in mimo skeleton):
1. `FwindowL (L_blk q)` discrete window ⟸ `RealizeWire.window_not_subthreshold` ⟸ `WindowProductRealizes`
   ⟸ `windowProductRealizes_corridor` ⟸ **hpin**. The scalar→corridor collapse is the `hlink` rewrite,
   already inside `genuine_no_sustained_Lwin` — so closing `hpin` closes the whole window leg.
2. `hpin` = the in-domain radius forcing `r·Blam·cos(|muc|+H) ≥ 1` — GENUINELY BLOCKED unconditionally.
The mimo `no_sustained_corridor` is a REDUNDANT, less-advanced mirror; nothing to port.

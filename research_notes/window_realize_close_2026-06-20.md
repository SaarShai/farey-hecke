# WindowProductRealizes — corridor realization bridge (2026-06-21)

File: `projects/aristotle_dispatch_v15/uniform_q5to18/WindowRealizeClose.lean`
Build: `( cd projects/aristotle_dispatch_v15/uniform_q5to18 && ~/.elan/bin/lake build WindowRealizeClose )`
EXIT 0. All theorems below `#print axioms` = `[propext, Classical.choice, Quot.sound]` (NO sorryAx).

## Goal

Prove `RealizeWire.WindowProductRealizes q hL P` for the corridor orbit
`P k = (M_W^[k] s0).1 · (M_W^[k] s0).2`, then discharge it into `RealizeWire.hbridge_of_realizes`
to close the corridor bridge `g_corr ≤ window-sup P` with NO named-Prop residual.

## STATUS: NOT fully closed. Reduced to ONE precise analytic residual (`hpin`).

`WindowProductRealizes` is NOT proved sorry-free for an actual orbit. It is REDUCED, with
everything else machine-verified, to a single precise per-`N` datum `hpin` = the **in-domain
arc-width geometry** (phase-link + radius forcing). This is a genuine reduction, NOT a disguised
close. Honest scope below.

## What IS machine-verified (axiom-clean) in `WindowRealizeClose.lean`

1. `windowMaxCos_eq_orbit_sup` — **phase-grid alignment** (task step 1, the fiddly core requested):
   if `muc` is chosen so `2(muc−ξ) − (L−1)θ + η = base`, then
   `windowMaxCos L q hL muc = sup'_{j<L} cos(base + 2jθ)`. Pure `Finset.sup'_congr`. PROVED.

2. `windowProductRealizes_of_data` — **the full ASSEMBLY** (task steps 3,4,5). From the realization
   DATA per `N` (product affine form `P(N+j) = (rr/(2A₂))·[3λ/2 + √A₂·cos(base+2(N+j−N)θ)]`,
   `rr>0`, `muc ∈ domain`, grid alignment, and radius forcing `rr·Blam²·cos²(|muc|+H) ≥ 1`),
   PROVES `WindowProductRealizes`. Mechanism: affine sup-push via `Finset.comp_sup'_eq_sup'_comp`
   (the affine `x ↦ (rr/2A₂)(3λ/2+√A₂ x)` is a sup-hom since monotone on ℝ); then
   `fcorr(muc) = (1/(2A₂Blam²cos²(|muc|+H)))·(2A₂/rr)·(window-sup P) ≤ window-sup P` using
   `P>0` at the sup index + radius forcing. Uses `fcorr`/`windowMaxCos`/`WindowProductRealizes`
   VERBATIM, no weakening. PROVED.

3. `lamq_pos_lt2` — `0 < lamq(m+2) < 2`. PROVED.

4. `windowProductRealizes_corridor` — **corridor instantiation**. Takes the `M_W`-orbit of an
   in-domain start `(a,b)` (`Qp>0`, orbit-product positive) and DISCHARGES the product-form +
   normalization half of `hdata` from `corridor_product_realization`:
     - `C0form = (rr/2A₂)·(3λ/2)`, `Rform = (rr/2A₂)·√A₂`, with `rr = 4A₂·Qp/(4−λ²)` (PROVED here).
   Reduces `WindowProductRealizes` to the single input `hpin` (the per-`N` alignment+forcing datum).
   PROVED (axiom-clean).

## The remaining residual `hpin` (the ONE open piece)

After the reduction, `hpin N` must supply, per window start `N`:
  - `base := φ` (the product realization phase) — **FREE** from `corridor_product_realization`
    (the `hprodphase` conjunct holds with `base = φ`, since `base+2Nθ+2(k−N)θ = φ+2kθ`).
  - `muc := (φ + 2Nθ + (L−1)θ − η + 2ξ)/2` (mod π) — DEFINED by the alignment equation.
  - **(R1) `muc ∈ domain`** `Ioo(−(π/2−H), π/2−H)`.
  - **(R2) radius forcing** `rr·Blam²·cos²(|muc|+H) ≥ 1`, i.e. `r·Blam·cos(|muc|+H) ≥ 1`.

Both R1, R2 are governed by the **phase link** (verified numerically to 1e−15, all q, all orbits):

      φ = 2ψ + (η − 2ξ)          ⟹   muc = ψ + Nθ + H   (mod π)

where `ψ` is the DOMAIN realization phase (`D_k = a_k+λb_k = Damp·cos(ψ+kθ)`,
`corridor_domain_realization`). Given the link:
  - R2 follows from the in-domain hypothesis `D_{N+j} > 1` (∀ j<L) at the window FAR ENDPOINT
    `j₀ ∈ {0, L−1}`: with `muc = ψ+Nθ+H`, `ψ+(N+(L−1))θ = ψ+Nθ+2H = |muc|+H` (when muc≥0),
    so `cos(ψ+(N+j₀)θ) ≤ cos(|muc|+H)`, hence
    `Damp·cos(|muc|+H) ≥ Damp·cos(ψ+(N+j₀)θ) = D_{N+j₀} > 1`, and `Damp = r·Blam`.
    (Verified: 0 endpoint-failures over 1500+ random orbits, q∈{18,22,30,60,100}.)
  - R1 (muc∈domain after mod-π reduction): verified 0 out-of-domain over the same trials.

### Phase link derivation (VERIFIED, not yet formalized)

Self-contained route (no `Complex.arg` comparison of the two realizations directly):
  - `D'_k := a_k − λb_k` is also a θ-sinusoid `Damp'·cos(ψ'+kθ)` with pinning
    `Damp'²·sin²θ = Qp` (coefficient 1; cf. `D`'s `6λ²+1`). [analog of `corridor_domain_realization`]
  - `P_k = a_k·b_k = (D_k² − D'_k²)/(4λ)` (algebraic identity, `ring`).
  - Expanding `cos²` ⟹ `P_k = const + Re[ ((Damp²e^{2iψ} − Damp'²e^{2iψ'})/(8λ))·e^{2ikθ} ]`,
    so the product phase `φ = arg(Damp²e^{2iψ} − Damp'²e^{2iψ'}) = 2ψ + (η − 2ξ)`.
    The last `=` is a fixed trig identity (verified: `arg(Damp²−Damp'²e^{2i(ψ'−ψ)}) = η−2ξ`,
    with `ψ'−ψ` an orbit-independent constant of `θ`). [VERIFIED numerically to 1e−6, all q]

### Phase-link FOUNDATIONS proved this session (axiom-clean)

  - `corridor_antidomain_realization` — the `D' = a−λb` orbit identity (mirror of
    `corridor_domain_realization`): `D'_k = Damp'·cos(ψ'+kθ)`, pinning `Damp'²sin²θ = Qp`. PROVED.
  - `product_eq_domain_sq_diff` — `a·b = ((a+λb)²−(a−λb)²)/(4λ)`. PROVED.

These are the self-contained legs of the link's derivation. What REMAINS for the link is the
single combined-amplitude argument identity
  `arg(Damp²·e^{2iψ} − Damp'²·e^{2iψ'}) = 2ψ + (η − 2ξ)`
(equivalently the fixed `ψ'−ψ`-of-θ + the `arg = η−2ξ` reduction), plus the dual far-endpoint
`Finset` index argument for R2.

### Capstone wiring proved this session (axiom-clean)

  - `corridor_bridge_of_pin` — GIVEN `hpin`, the corridor bridge `g_corr ≤ window-sup P` holds for
    the corridor orbit at every `N`, by feeding `windowProductRealizes_corridor` into the PROVED
    `RealizeWire.hbridge_of_realizes`. Confirms the reduction is type-correct end-to-end: closing
    `hpin` closes the corridor bridge with NO named-Prop residual.

### Why NOT fully closed this session (honest)

R2 is irreducibly **phase-coupled**: as `|muc| → π/2−H` the bound needs `r²→∞`, so there is NO
unconditional radius shortcut — the in-domain hypothesis must be used at the far endpoint, which
requires the phase link. The link's foundations (`D'` realization, product decomposition) are now
PROVED; what remains is the combined-amplitude arg identity (`arg = η−2ξ`, a fixed trig identity
needing `ψ,ψ'` pinned to `a,b`) and the dual far-endpoint index argument. This is the long-flagged
"realization bridge" crux — the genuine remaining mathematics. It was NOT closeable within this
session without high risk of a broken/sorry artifact, so it is left as the precise residual `hpin`,
fully specified and type-wired (capstone above), rather than punted to a vague named Prop.

## Downstream (LblkWindow.perq_Xomega_lb_Lblk_GEN)

`LblkWindow.FwindowL (L_blk q)` (the DISCRETE Hecke-CF scalar window `¬∀j<L, c(i+j)·c(i+j+1)<1/λ³`)
is a SEPARATE object from the corridor `M_W`-orbit product window here. Even with
`WindowProductRealizes` fully closed, discharging `FwindowL(L_blk q)` needs the scalar→corridor
identification (the `product_form` collapse on branch q−1) which lives in the genuine chain
(`no_sustained_corridor` in `mimo-mini-project`, a different Lake project) — NOT directly wireable
from this file. So the q≥22 lower bound's hypothesis list is UNCHANGED by this session: it still
carries `FwindowL (L_blk q) mpoly` as the single named input (`LblkWindow.perq_Xomega_lb_Lblk_GEN`).
What this session delivered is the machine-verified ASSEMBLY + corridor reduction of the corridor
bridge, shrinking the corridor-side residual to the single precise `hpin` (in-domain arc-width
geometry), with the phase link and far-endpoint mechanism fully reverse-engineered and verified.

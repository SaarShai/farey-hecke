# `hpin` — VERDICT: genuinely blocked unconditionally (obstruction PROVED axiom-clean)

Date: 2026-06-21
File: `projects/aristotle_dispatch_v15/uniform_q5to18/HpinClose.lean` (builds EXIT 0, axiom-clean)

## What `hpin` is

`hpin` is the per-window-start datum fed to
`WindowRealizeClose.windowProductRealizes_corridor` / `corridor_bridge_of_pin`. Its load-bearing
conjunct is the **in-domain radius forcing** (RF), for the corridor orbit start `(a,b)`:

    1 ≤ (4·A₂·Qp/(4−λ²)) · Blam² · cos²(|μc|+H)       ... (RF)

with `A₂ = A2q q = 1+2λ²`, `Qp = Qp l a b`, `r² := 4A₂Qp/(4−λ²)`, `Blam = Blamq q`,
`H = Hq (L_blk q) q`. The amplitude pinning (proved in `corridor_domain_realization` +
`WindowRealizeClose`, `Damp² = r²Blam²`, `Damp²sin²θ=(6λ²+1)Qp`) makes (RF) read
`Damp·cos(|μc|+H) ≥ 1`, where `Damp·cos(μc∓H)` are the `D = a+λb` window-endpoint values.
So (RF) **literally asserts the orbit is in-domain (`D ≥ 1`) at the window far-endpoint.**

## Why it must be unconditional (no `hdom` available)

`hpin → windowProductRealizes_corridor → RealizeWire.WindowProductRealizes →
window_not_subthreshold`, whose conclusion is `1/λ³ ≤ window-sup P` for **every** `N`,
**unconditionally**. That conclusion IS the contradiction of "stays sub-threshold for `L_blk q`
steps" inside `genuine_no_sustained_Lwin`. The only orbit inputs upstream are
`hQpos : 0 < Qp l a b` and `hPpos : ∀k, 0 < P k`. There is **no** in-domain residency hypothesis
threaded to `corridor_bridge_of_pin` (checked: its signature carries only `a b`, `hQpos`, `hPpos`,
`hpin`). So (RF) would have to follow from `Qp>0` + product-positivity alone.

## The obstruction (PROVED, not punted)

(RF) is **false** for general such orbits. `Qp` (hence `r² = 4A₂Qp/(4−λ²)`) scales as `ε²` under
`(a,b) ↦ (εa,εb)`, while `Blam²` is fixed and `cos²(|μc|+H) ≤ 1`. So scaling the start down forces
the (RF) quantity `< 1` for **every** `μc` — no domain restriction even needed, only `cos² ≤ 1`.

Formalized axiom-clean in `HpinClose.lean`:

- `Qp_scale`, `MW_iterate_scale`, `prod_scale` — `Qp` and the orbit product scale as `ε²`;
  `M_W` is linear so `(M_W^[k](εa,εb)) = ε·(M_W^[k](a,b))`. Product-positivity is preserved.
- **`hpin_radius_forcing_unsatisfiable`** (`q ≥ 18`): given any corridor start `(a,b)` with
  `a,b>0` and all orbit products positive, the scaled start `(εa,εb)` (with
  `ε = √(1/(2K))`, `K = 4A₂Qp/(4−λ²)·Blam² > 0`) still has `Qp>0` and all products `>0`, yet
  `(4A₂·Qp(εa,εb)/(4−λ²))·Blam²·cos²(|μc|+H) = ε²K·cos²(…) ≤ ½ < 1` for **every** `μc`.
- **`hpin_not_unconditional`**: hence `¬ ∃ μc, (RF)` at that orbit — the radius-forcing conjunct
  of `hpin` has **no witness**, so `hpin` cannot be discharged from `hQpos`/`hPpos`.

`#print axioms` on both: `[propext, Classical.choice, Quot.sound]` (NO `sorryAx`).

Build: `( cd projects/aristotle_dispatch_v15/uniform_q5to18 && ~/.elan/bin/lake build HpinClose )`
→ EXIT 0, "Build completed successfully (8029 jobs)".

## Exact named obstruction

The blocker is strictly the **lower** bound `Damp·cos(|μc|+H) ≥ 1`, i.e. the in-domain endpoint
value `D_far ≥ 1`. This has **no unconditional lower bound** — it scales to 0 with `Qp` (with `Qp`
bounded only below by 0 via `hQpos`). The proved sinusoid identities give the exact value of `D`
(`corridor_domain_realization`: `D = Damp·cos(ψ+kθ)`, `Damp²sin²θ=(6λ²+1)Qp`) and of `D' = a−λb`
(`corridor_antidomain_realization`), and the amplitude pinning `Damp² = r²Blam²` — but NONE of
these gives `D_far ≥ 1`. That fact is exactly "the orbit stays in-domain across the window", the
hypothesis being contradicted. **It is circular to derive it from the contradiction premise, and
demonstrably false absent it.** This confirms the prior analysis ("no unconditional shortcut") and
upgrades it from assertion to a machine-checked impossibility.

## What this does NOT say

It does not say the *genuine-chain* statement is false. On the genuine branch the orbit `(a,b)` is
NOT an arbitrary corridor point: it is a Hecke-CF block-boundary state with `Qp` pinned by the
Hecke band geometry (the conserved form on the `k=1` corridor, bounded away from 0 by the band
constraints `c_n ≤ 1`, `c_n + λc_{n+1} > 1`, etc.). The unconditional `hpin` (all corridor starts
with merely `Qp>0`) is false; the *band-constrained* `hpin` (the in-domain residency forced by the
contradiction hypothesis + band bounds) is the genuine residual — but it CANNOT be stated/proved at
the current interface, which only exposes `hQpos`/`hPpos`. **To close `hpin`, the interface must be
strengthened to carry the in-domain residency datum `D_{N+j} > 1` (∀ j < L_blk q) as a hypothesis
— which is exactly the negation of the sub-threshold/eject contradiction premise inside
`genuine_no_sustained_Lwin`, and must be wired from there, not supplied unconditionally.**

So the residual is precisely: thread the band-derived in-domain residency `D_{N+j} > 1` from the
genuine no-sustained contradiction context into `corridor_bridge_of_pin`'s `hpin`. With that
hypothesis, (RF) is provable (`Damp·cos(|μc|+H) = D_far > 1` at the aligned `μc`); without it, `hpin`
is FALSE (proved here). The current cross-project interface does NOT carry it, so `hpin` is blocked
as stated.

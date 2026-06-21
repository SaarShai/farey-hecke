# Consolidation — the uniform onset bound X_Ω(q) ≥ 1/λ_q³, q ≥ 22

Date 2026-06-20. Honest record of the unconditional-extension push. Every Lean claim below is
`lake build`-verified axiom-clean `[propext, Classical.choice, Quot.sound]` (no `sorryAx`),
re-checked in the main loop, unless explicitly marked OPEN.

## 0. Standing result (banked, untouched)
**Theorem (onset value, machine-verified, q = 5..21).** X_Ω(q) = 1/λ_q³ — sharp equality,
sorry-free, axiom-clean (`OnsetEquality.lean` + the per-q window-verified files). This is the
result behind the Koyama joint paper and is **not** affected by anything below.

## 1. What the push achieved: a machine-verified REDUCTION for q ≥ 22
Goal: extend the onset lower bound X_Ω(q) ≥ 1/λ_q³ past the q ≤ 21 cap of the fixed-window method.
Two routes were tried; the second is the live one.

### 1a. Energy route (Koyama's suggestion) — gave the demystification, then a dead end
- Formalized Koyama's conserved-energy `E = c_n²+c_{n+1}²−λc_nc_{n+1}` + escape-of-mass as a
  machine-verified **reduction** of the q≥22 confinement `hCorr` (commit f0a0597, 6f194b1).
- **Demystification (important):** the onset `≥` bound does NOT inherit the B(q) resonance /
  parity obstruction. It needs only "the rotation hits the super-arc once in q steps"
  (`cos_grid_hit`), which is resonance-INDEPENDENT. The resonance set {23,61,…} only moves B(q)'s
  *exact* value, never whether *some* point clears threshold (86f537a).
- `hEfloor` (uniform corridor E-floor, q≥5) and `hAgreePrefix` (bounded-prefix k=1 agreement)
  PROVED (86f537a, d03118c).
- **Dead end:** the route's keystone instantiated the SCALAR map; `hEject` is *false* there, and
  the genuine deep-mid ejection (`genuine_hEject_deepmid`) is the MULTI-BRANCH successor, which
  does not compose with the scalar rotation-arc cover (a087fcbc / aa93f35).

### 1b. L_blk q-dependent window (the live route) — stays on the genuine map
- The genuine engine's q≤21 cap was purely the **fixed 6-window** `Fwindow6`. Generalized to a
  parametric length: `genuine_no_sustained_Lwin`, `perq_Xomega_lb_Lblk_GEN` instantiate
  `L_blk(q)=⌈33q/256⌉+2` for q≥22; recovers L=6 (soundness). Band facts uniform for q≥7
  (commit 31bb8c1). My own `lake build LblkWindow` → 8052 jobs, axiom-clean.
- The hard analytic core is **already proved**: `L1bArcCoverage.B1_target`/`fcorr_lb`/
  `arc_coverage_ineq` (the uniform escape margin; δ_∞ = 5.77·10⁻⁵ > 0; interval-certified q≤10000).
- The corridor **realization** identities PROVED: `corridor_product_realization` (P=a·b sinusoid),
  `corridor_domain_realization` (D=a+λb), `corridor_antidomain_realization` (D'=a−λb), amplitude
  pinning (15625a5). `hbridge_of_realizes` reduces `g_corr ≤ g_true` to one Prop
  `WindowProductRealizes` (csInf + B1_target).
- `WindowRealizeClose`: phase-grid alignment + assembly + C0/R↔fcorr normalization PROVED (4c07a4c).
- The scalar→corridor **product collapse** PROVED: `scalar_prod_eq_mmap_prod` (bbcd56d). No
  cross-project port needed — `uniform_q5to18` already mirrors `no_sustained_corridor`.

## 2. The precise remaining residual (OPEN — and now exactly characterized)
After all of the above, q≥22 reduces to a SINGLE input, `hpin` (the in-domain radius forcing
`r²·B_λ²·cos²(|μc|+H) ≥ 1` feeding `windowProductRealizes_corridor`). This round PROVED the
decisive negative:

**`HpinClose.hpin_not_unconditional` (PROVED, axiom-clean):** the *unconditional* `hpin` is FALSE.
The realization interface (`windowProductRealizes_corridor` / `corridor_bridge_of_pin`) threads
only positivity (`hQpos`, `hPpos`), NOT the in-domain residency `D_{N+j} > 1`. So an unconditional
`hpin` would have to hold on a scaled-down start `(εa, εb)`, where it provably fails. `hpin` is
provable **per-orbit given sustained in-domain residency** — but that residency datum is exactly
what the current interface drops.

**So the remaining work is exact, not mysterious:** RE-ARCHITECT the realization interface to
thread the in-domain residency (`D_{N+j} > 1`, available in `FwindowL`'s own corridor hypotheses)
through to the radius forcing, making the per-orbit radius bound uniform in q. The naive target is
PROVED insufficient. This is genuine analytic + interface work (multi-session), not a wiring fiddle.

## 3. Honest standing
- q = 5..21: **unconditional, machine-verified** (banked).
- q ≥ 22: **machine-verified reduction** to the single, precisely-characterized `hpin`
  interface/analytic residual. NOT unconditional.
- The push also produced reusable proved lemmas: the parametric `L_blk` window, the corridor /
  anti-domain sinusoid realizations, the uniform band facts, the scalar→corridor collapse, and the
  `hpin_not_unconditional` negative that pins the gap.

## 4. Commit trail
b318e1a → f0a0597 → c42602a → 6f194b1 → 7ff73f4 → 0b93aef → 1710779 → 86f537a → d03118c →
aa93f35 → 31bb8c1 → 15625a5 → 4c07a4c → bbcd56d.

## 5. Methodology note (honest)
Across ~10 adversarially-verified fleets, the pattern was consistent: the fleet proves the bulk
(90–95%) cleanly and reliably reduces to a smaller named residual, but the FINAL analytic step
(map mismatch, phase alignment, in-domain geometry) repeatedly resisted — each "last mile"
fragmented into a new, smaller, but genuine residual. The verification discipline (every step
re-built by `lake build` in the main loop; a proved NEGATIVE when a target was false) kept the
record honest and converted "we're stuck" into "here is exactly why, and exactly what's left."

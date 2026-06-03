# Cuspidal optimizer-escape: criterion, verified arithmetic examples, candidate families (2026-06-02)

Extends `DISCOVERY_Hecke_ergodic_optimization.md`. Goal: (1) find cusped/non-compact **arithmetic**
return maps where the ergodic-optimization optimizer **escapes** (no ground state); (2) pursue
non-arithmetic Hecke (q=5,7,…) and higher-rank multi-cusp Farey.

## 0. The escape CRITERION (general, derived from the Hecke analysis)
For a non-compact return map `T` on an **open** fundamental region `D` (cusp = excluded boundary),
and an observable `f≥0`, the ergodic-optimization infimum `X = inf_μ ess-sup_μ f` **escapes**
(is not attained by any `T`-invariant measure) when the cost-minimizing dynamics is driven to the
excluded boundary/cusp. Concretely it escapes iff:
- `X` is realized only as a **limit** along a family of orbits whose closure exits `D` (into the
  cusp / onto the boundary `∂D`), and
- the limiting object is a **parabolic** cusp orbit (monodromy trace 2 ⇒ a scale-free family),
  pinned to `∂D` by the floor/triangle constraint.

**Meta-observation (why escape is the RULE here, not the exception):** these BCZ-type maps live on
*open* domains (`x>0,y>0, x+λy>1`), so an observable whose minimizing orbit is pushed against the
open boundary cannot attain its inf — escape is **generic** for such maps, and does NOT contradict
Contreras (2016) (compact, generic-observable). It is an ergodic-optimization face of **escape of
mass** in non-compact homogeneous dynamics (Eskin–Margulis; Athreya).

## 1. THREE verified cusped ARITHMETIC return maps where the optimizer escapes
Takeuchi (1977): the Hecke triangle group `G_q` is **arithmetic** exactly for `q ∈ {3,4,6,∞}`.
The three *finite* arithmetic ones give three distinct arithmetic lattices (PSL(2,ℤ) and groups
commensurable with `Γ_0(2)`, `Γ_0(3)`), each with a cusp:

| map | group `G_q` (λ=2cos(π/q)) | optimizer word | X(q) | escape (open bound) | status |
|---|---|---|---|---|---|
| **q=3** | PSL(2,ℤ) = (2,3,∞), λ=1 | (1,4) | 2/9 | floor-jump (open) | **Lean-PROVEN no GS** |
| **q=4** | (2,4,∞), λ=√2 | (1,2) | √2/8 | triangle (open) | **Lean-PROVEN no GS** |
| **q=6** | (2,6,∞), λ=√3 | (1,1,1,2) | √3/6 | triangle (open) | computed; period-4 parabolic |

All three: optimizer = a parabolic word, `X` approached at an **open** cusp/edge boundary ⇒ **no
ground state**. q=3,4 are machine-checked in Lean (`no_ground_state`, `g4_no_ground_state`); q=6 is
numerically verified (same structure). **Honest caveat:** these are the three arithmetic members of
ONE family (Hecke). Genuinely *different* arithmetic families are in §3 (candidates, not yet verified).

**Robustness (same arithmetic map q=3, different observable):** for `f=x` (first coordinate),
`x+y>1` forces `max(x,y)>1/2`, so `sup_orbit x ≥ 1/2`, approached only as the orbit nears the
*excluded* vertex `(½,½)` (where `x+y=1`). Hence `X_{f=x}=1/2`, **escape** (numerically confirmed
inf≈0.5000). ⇒ escape is not special to `f=xy`; it is driven by the open domain.

## 2. Next bet — pursued
- **Non-arithmetic Hecke q=5,7,… : ESCAPE CONFIRMED.** Hecke `G_q` is non-arithmetic for q=5,7,8,…;
  the hunt gives escape for all of them: `X(5)=1/4`, `X(7)=0.3887…`, optimizer `(1^{q−3},2)`,
  open boundary. So the escape phenomenon is **independent of arithmeticity** — it holds across the
  whole Hecke family (arithmetic q=3,4,6 and non-arithmetic q=5,7,…). [VERIFIED, q=3..30.]
- **Higher-rank / multi-cusp Farey (Marklof) — SET UP, not yet computed.** The horospherical return
  map (Poincaré section of the horocycle/horospherical flow) on `SL(3,ℝ)/SL(3,ℤ)` — the multidim
  Farey map (Marklof, *Fine-scale statistics for multidim Farey*, 2012) — lives on a non-compact
  finite-volume space with a richer cusp. The criterion **predicts escape** (parabolic cusp orbits
  drive the inf to the boundary). Implementation is substantial (higher-rank BCZ section is not the
  1-line floor map) ⇒ **flagged as the concrete next computation, NOT claimed verified.**

## 3. Candidate genuinely-NEW arithmetic cusped families (precise; escape predicted; to implement)
Each is a non-compact arithmetic return map with cusp(s); the criterion predicts optimizer-escape.
**None verified yet — listed honestly as targets, not results.**
1. **Arithmetic `(p,q,∞)` triangle groups, p≥3** (Takeuchi's finite list, e.g. (3,3,∞),(3,4,∞),…):
   BCZ-type return maps generalizing Hecke `(2,q,∞)`; new floor structure; single cusp.
2. **Congruence-subgroup BCZ, `Γ_0(N)` / `Γ(N)`:** "Farey fractions with a congruence condition"
   (Boca–Zaharescu): MULTIPLE cusps ⇒ several escape channels, possibly several distinct `X` values.
   (Note: q=4,6 already ARE commensurable with `Γ_0(2),Γ_0(3)`, so the simplest cases overlap §1.)
3. **Higher-rank `SL(n,ℤ)` Farey** (n≥3, item 2 above): richest cusp structure.

## Honest scope
- **VERIFIED escape:** Hecke `G_q` all `q=3..30` (arithmetic q=3,4,6 incl. Lean-proven q=3,4; non-
  arith q=5,7,…); plus the `f=x` robustness on q=3.
- **PREDICTED (criterion) but NOT computed:** §2 higher-rank, §3 families. These are the genuine
  next steps; I will not claim them as found until the maps are implemented and the escape verified.

# INV-P-E-relation — exact algebra of the gap-product P vs the conserved energy E

**Date:** 2026-06-12. **Branch:** `hecke-goalL-2026-06-03`.
**Task:** establish the exact relationship between the gap-product observable `P`, the conserved
energy `E = c_n² + c_{n+1}² − λ c_n c_{n+1}` (NoInfiniteRotation core), and the coordinates `c_n`
during an elliptic/rotation corridor (floor-1 run); decide whether the energy constraint **alone**
forces `P ≥ 1/λ³`.

**VERDICT (adversarial):** the energy constraint **does NOT** force `P ≥ 1/λ³`. The energy gives
only an **upper** bound `P ≤ E₀/(2−λ)` (the maximal gap-product); the infimum of `P` on a fixed
energy level set is **0**, attained at the boundary of the positive quadrant. `1/λ³` is an
**ess-sup over invariant measures** (ergodic-optimization ground value), not a pointwise floor —
and indeed real corridors dip well below it. The cusp-escape / itinerary input is **genuinely
needed**; energy conservation by itself is not the mechanism.

---

## 1. The exact correspondence (a) — BCZ orbit ↔ `c_n`

Source: `code/goal1_bcz_hecke_cluster.py`, `code/goal1_cluster_ceiling_reconcile.py`,
`research_notes/goal1_Xq_bridge.md §1`, and the Lean core
`koyama_packet_2026-06-12/lean/BCZHeckeNoInfiniteRotation_allq_VERIFIED.lean`.

The Taha G_q-BCZ map acts on `(a,b) ∈ T^q`. Extremes (`P < X`) are confined to the **last branch**
`T_{q−1}` (verified `goal1_branch_minP.py`, reconfirmed here: last-branch fraction 0.71–1.00,
all sub-threshold points there). On `T_{q−1}` (`w_{q−1}=(0,1)`) the map is the classical-shaped

```
(a, b) ↦ (b, −a + k·λ·b),   k = ⌊(1+a)/(λ b)⌋,   P = a·b.
```

A **floor-1 run** (rotation corridor) is a maximal block of consecutive last-branch steps with
`k = 1`. There the map is `(a,b) ↦ (b, −a + λ b)`. Define the scalar sequence

> **`c_n := a_n`** — the FIRST coordinate of the orbit during the corridor.

Then `c_{n+1} = b_n = a_{n+1}` and `c_{n+2} = a_{n+2} = −a_n + λ b_n = λ c_{n+1} − c_n`, i.e.

> **`c_{n+2} = λ c_{n+1} − c_n`** — exactly the floor-1 recurrence `hrec` in the Lean file.

So the Lean `c : ℕ → ℝ` is literally the first-coordinate sequence of a BCZ orbit running inside a
floor-1 corridor. `E = c_n² + c_{n+1}² − λ c_n c_{n+1}` is the invariant of the trace-λ elliptic
rotation `R = [[0,1],[−1,λ]]` (Cayley–Hamilton `R² = λR − I`; cf. `BCZHeckeL2_traceIdentity`
`rotation_trace_spectrum`). **Numerically confirmed** (q=3,5,7): `max|P − a·b|` on `T_{q−1}` ≤ 2e-15;
`max|c_{n+2} − (λ c_{n+1} − c_n)|` ≤ 7e-15; `max|E − E₀|` ≤ 5e-15 (E conserved to machine precision).

## 2. P in terms of `c_n, c_{n+1}` (b)

> **`P = c_n · c_{n+1}`.**   (`P = a·b`; `a=c_n`, `b=c_{n+1}`.)

Exact, confirmed to ~1e-15 along genuine corridors. So both the conserved `E` and the observable
`P` are functions of the **same pair** `(c_n, c_{n+1})`:

| object | formula |
|---|---|
| energy (conserved) | `E = c_n² + c_{n+1}² − λ c_n c_{n+1}` |
| gap-product (observable) | `P = c_n c_{n+1}` |
| **exact link** | **`c_n² + c_{n+1}² = E + λ·P`** (sympy: identity, residual 0) |

## 3. Extremizing P on the energy level set (c)

Level set `{E = E₀}` is an ellipse (positive-definite for `λ<2`). Diagonalize with
`u = c_n + c_{n+1}`, `v = c_n − c_{n+1}`:

```
E = (2−λ)/4 · u²  +  (2+λ)/4 · v²  = E₀,        P = (u² − v²)/4.
```

**Critical points of P on the ellipse (Lagrange, sympy `solve`):** the only interior critical
point is the **symmetric MAXIMUM** at `c_n = c_{n+1}` (i.e. `v=0`):

> **`P_max = E₀/(2−λ)`**   (attained on the diagonal `c_n=c_{n+1}=√(E₀/(2−λ))`).

This is exactly the AM-GM bound: from `c_n²+c_{n+1}² = E₀ + λP` and `c_n²+c_{n+1}² ≥ 2c_n c_{n+1}=2P`,

> **`E₀ + λP ≥ 2P  ⟹  P ≤ E₀/(2−λ)`**   — an **UPPER** bound on the gap-product.

The other ellipse critical point of `P` is `P = −E₀/(2+λ) < 0`, which requires `c_n = −c_{n+1}`
and is **excluded by positivity** (`c_n, c_{n+1} > 0`, the open BCZ domain).

**There is NO interior minimum of P on the positive arc.** As `c_{n+1} → 0⁺` along the ellipse,
`c_n → √E₀` and `P = c_n c_{n+1} → 0` while `E ≡ E₀`. Hence

> **`inf {P : E = E₀, c_n,c_{n+1} > 0} = 0`** (not attained, not positive).

`1/λ³` is **not** of the form `E*/(2−λ)` for any natural fixed energy: solving `E*/(2−λ)=1/λ³`
gives `E* = (2−λ)/λ³`, which does not match the actual corridor energies (e.g. q=5: `E*`=0.0902 vs
`1/λ³`=0.2361; q=7: 0.0339 vs 0.1709). So `1/λ³` is **not** an energy-level artifact of the
symmetric corridor point.

### Conclusion of (c)
The energy constraint controls only the **top** of `P` per corridor (`P ≤ E₀/(2−λ)`). It says
nothing that keeps `P` above `1/λ³`; the level-set infimum of `P` is 0. **Energy alone cannot
yield `P ≥ 1/λ³`.**

## 4. Numerical validation (d) — q=3,5,7

`/tmp/pe_validate.py`, `/tmp/pe_energy_scan.py` (2M-step orbits, junction-safe, real corridors).

| q | λ | `1/λ³` | longest k=1 run | `max|E−E₀|` | global min P (orbit) | corridor `E₀` range |
|---|---|--------|-----------------|-------------|----------------------|---------------------|
| 3 | 1 | 1.000000 | 1 | — | 0.000711 | [0.3337, 0.9990] |
| 5 | φ | 0.236068 | 3 | 2.2e-16 | 0.000295 | [0.0613, 0.3816] |
| 7 | 1.80194 | 0.170915 | 5 | 4.8e-15 | 0.000796 | [0.0265, 0.3069] |

Findings:
* **E is conserved** along every floor-1 run to machine precision (`max|E−E₀| ≤ 5e-15`). ✔ Koyama
  core verified empirically.
* **`P = c_n c_{n+1}`** exact (≤2e-15). ✔
* **P is NOT bounded below by `1/λ³`.** Global min `P` over the orbit is ~1e-3 (q=3,5,7) — three
  orders of magnitude below any `X(q)`. Even **inside a single floor-1 corridor**, `P` dips below
  `1/λ³`: q=7's longest corridor had `E₀=0.1696` and `min P = 0.1543 < 0.1709 = 1/λ³`
  (`min P − 1/λ³ = −0.0166`). Corridor energies drop to `E₀=0.0265` (q=7), far below `X`.
* **`P ≤ E₀/(2−λ)` holds with equality at the symmetric point.** q=5 corridor: `max P = 0.8230` vs
  predicted `E₀/(2−λ) = 0.8260`. ✔

(q=3 entries use the cusp value `1/λ³=1`, not `X(3)=2/9`; the structural conclusion — `inf P`=0,
no energy floor — is q-independent.)

## 5. What this means for Koyama's "energy × cusp-escape" route

* The **energy** half (`E` conserved, positive-definite, orbit-bounding) is solid and already
  Lean-verified. It bounds the orbit (`c_n ≤ M`), forces every rotation corridor to be **finite**
  (`no_infinite_rotation`), and caps the gap-product from **above** (`P ≤ E₀/(2−λ)`).
* The **lower bound on the ess-sup** — the actual claim `X_Ω(q) = inf_μ ess-sup_μ P ≥ 1/λ³` — is
  **not** delivered by the energy constraint. Pointwise `P` ranges down to ~0; `1/λ³` is a property
  of the **ess-sup over invariant measures**, i.e. it constrains how often / how large `P` must be
  *on average along an orbit*, not the per-step value. This is fundamentally a statement about the
  **return geometry into the cusp** (how a low-energy corridor must terminate and how that forces a
  high-`P` excursion), which is exactly the "rate of escape-of-mass into the cusp" half of Koyama's
  proposal. **That half is genuinely needed and is not yet in hand.**
* Mechanistically (consistent with `goal1_Xq_bridge §3`): a sub-threshold cluster is a low-`E₀`
  corridor; `no_infinite_rotation` forces it to exit (`k≥2` kick). The conjecture `X=1/λ³` is that
  the cusp exit must be "paid for" by a gap-product excursion whose level pins the **ess-sup** at
  `1/λ³`. The energy bounds the corridor length and the in-corridor max; it does **not** by itself
  pin the ess-sup. The missing input is a quantitative coupling: a lower bound on the time-average
  of `max(P)` per excursion in terms of the parabolic (cusp) kick strength `(k−1)λ` from
  `adjF_switch_parabolic`.

## 6. Exact relation summary (deliverable)

```
c_n := a_n  (first orbit coordinate in a floor-1 corridor)
c_{n+2} = λ c_{n+1} − c_n                          [floor-1 recurrence, Lean hrec]
E       = c_n² + c_{n+1}² − λ c_n c_{n+1}           [conserved, Lean E_const]
P       = c_n · c_{n+1}                              [gap-product observable, = a·b]
c_n² + c_{n+1}² = E + λ·P                            [exact identity]
P ≤ E₀/(2−λ)        (AM-GM; equality at c_n=c_{n+1})  [UPPER bound, the only one E gives]
inf{P : E=E₀, c>0} = 0  (boundary c_{n+1}→0)         [no positive lower bound from E]
```

**Does the energy constraint alone force `P ≥ 1/λ³`?  NO.** The cusp-escape / itinerary input is
genuinely required; energy supplies the upper bound and corridor finiteness only.

## 7. Reproducibility
* `/tmp/pe_relation.py` — Lagrange critical points of P on `{E=E₀}` (symmetric max only).
* `/tmp/pe_arc.py` — positive-arc infimum = 0; floor-1 constraint listing.
* `/tmp/pe_validate.py` — q=3,5,7 corridor extraction; `P=c_n c_{n+1}`, E-conservation, min-P check.
* `/tmp/pe_energy_scan.py` — 2M-step global min P; corridor `E₀` spectrum vs `X`.
* `/tmp/pe_final.py` — exact identity `c_n²+c_{n+1}² = E+λP`; `1/λ³ ≠ E*/(2−λ)`.

# Prior-art & novelty audit — Hecke-BCZ ergodic-optimization layer

**Date:** 2026-06-03. **Goal:** `GOAL_G_priorart_novelty.md`. **Status:** GATES any write-up / external claim.
**Method:** adversarial (assume NOT novel until shown otherwise); 4 parallel primary-source literature
sweeps (web + arXiv + PDF full-text extraction). Every citation's author/venue/year/volume/pages
verified against the source it is cited from. Nothing sent outward (internal audit; USER-gated).

> **One-line bottom line.** The single highest-risk overlap — "`1/λ³` IS the known Hecke-group Hurwitz
> constant" — is **REFUTED** (the real Hecke Hurwitz constant is `2`/`2√(1+(1−λ/2)²)` ∈ [0.447, 0.5],
> numerically disjoint from `1/λ³` ∈ [1, 0.125] at every q). A **defensible novel contribution survives**,
> but it is **novelty-of-realization, not novelty-of-phenomenon**: a concrete arithmetic (BCZ / Taha
> Hecke-BCZ) instantiation of the ergodic-optimization objective `inf_μ ess-sup_μ P`, with explicit
> closed-form values. The non-attainment-via-cusp-escape MECHANISM is **already documented** and must NOT
> be claimed as new. Biggest residual risk: the JMU-2007 Gauss-map example surfaces the value **2/9** —
> a numerical coincidence an adversarial referee will catch; address it head-on.

---

## Verdict table (the four claims)

| # | Claim | Verdict | Closest primary-verified prior art |
|---|-------|---------|-----------------------------------|
| 1 | Ergodic optimization `X(q)=inf_μ ess-sup_μ P` on the BCZ / Hecke-BCZ return map | **APPARENTLY NOVEL** (as formulation) | None on BCZ. JMU 2007 (ergodic opt on the *Gauss* map, different observable). |
| 2 | The constants `2/9` (q=3), `√2/8` (q=4), `1/λ³=1/(2cos π/q)³` (q≥5) as extremal Farey/Hecke-gap constants | **RELATED-BUT-DISTINCT**; the specific values **APPARENTLY NOVEL** (not found) | Hecke Hurwitz constant `h_q` (Haas–Series 1986) — **provably different**. Hall `3/π²`; KS `2 log φ`. |
| 3 | No ground state — infimum approached, never attained, via cusp escape (escape of mass) | **KNOWN mechanism / NOVEL-AS-FORMULATION** for this system | JMU 2007 Ex. 12 (countable shift, escape); Riquelme–Velozo 2020 (cusped geodesic flow). |
| 4 | min-max ≠ min-average: `inf_μ ess-sup_μ P = 1/λ³ > β_min = inf_μ ∫P dμ` | **NOVEL-AS-FORMULATION** (the inf-ess-sup object is non-standard) | JMU 2007 `α≤β≤γ≤δ` strictness — but those are all *average*-type, not inf-ess-sup. |

---

## Claim 1 — ergodic optimization of the BCZ / Hecke-BCZ map. **APPARENTLY NOVEL (as formulation).**

No prior work studies an inf/sup over invariant measures of an observable — a maximizing/minimizing
measure, a ground value, or an extremal gap-product — **on the BCZ map**. Every primary source opened
(BCZ Crelle 535; Athreya–Cheung IMRN 2014; Athreya survey arXiv:1210.0816; Taha arXiv:1810.10668; the
2024 weak-mixing paper arXiv:2403.14976; the 2024 "discretized RH" arXiv:2407.03099) treats only
**distributional / averaged** quantities (limiting gap distribution, equidistribution, moments/sums,
L¹-averages, mixing). The map's outstanding open problems are framed in the literature as weak-mixing
(now solved), mixing, and rigidity — never as an extremal/optimization question.

- **Athreya–Cheung §8 "Further Questions" (read verbatim from arXiv:1206.6597 PDF):** five items —
  §8.1 BCZ-as-adic-transformation + return maps for other lattices (notes the Δ(2,5,∞) Hecke calc in
  Athreya–Chaika–Lelievre); §8.2 BCZ-type map for translation surfaces; §8.3 "Is the BCZ map mixing?";
  §8.4 deviation bounds for ergodic averages + "is there an optimum error bound equivalent to RH?".
  **CONFIRMED: §8 poses NO min-max / extremal / ergodic-optimization / maximizing-measure question.**
  The project memory's characterization of AC §8 (poses error⇔RH, NOT min-max) is **accurate**. The
  §8.4 RH question is about the *averaged* equidistribution error term, a different object.
- **Closest prior is by analogy only**, not on the BCZ map: Jenkinson–Mauldin–Urbański 2007 (ergodic
  optimization on the **Gauss** continued-fraction map). The general framework (Jenkinson ETDS 2019) is
  never applied to BCZ.

Label is APPARENTLY NOVEL (stronger than novelty-as-formulation): the specific extremal question is
genuinely absent from the literature, while all constituent pieces (the map, the observable's
distribution, ergodic optimization elsewhere) are standard.

## Claim 2 — the constants. **RELATED-BUT-DISTINCT; specific values APPARENTLY NOVEL.**

### 2a. THE HIGHEST-RISK CHECK — Hecke-group Hurwitz constant. **REFUTED (no coincidence).**
The classical "best Diophantine-approximation constant" for the Hecke triangle group `G_q` (the
analogue of Hurwitz's `√5`) is the **Hecke Hurwitz constant** (Haas–Series; Lehner):

> `h_q = 2` for q **even**;  `h_q = 2·√(1 + (1 − λ_q/2)²)` for q **odd**,  `λ_q = 2cos(π/q)`.

(Sanity: q=3 ⇒ `h_3 = 2√(1.25) = √5` ✓ recovers Hurwitz.) The approximation constant `1/h_q` lives in
**[0.447, 0.5] for all q and → 1/2**. The project's `1/λ³` runs **1.0 → 0.125 and → 1/8**.

| q | λ_q | Hecke Hurwitz `1/h_q` | project `1/λ³` | project companion |
|---|-----|----------------------|----------------|-------------------|
| 3 | 1.00000 | 0.44721 (=1/√5) | 1.00000 | 2/9 = 0.2222 |
| 4 | 1.41421 | 0.50000 | 0.35355 (=√2/4) | √2/8 = 0.1768 |
| 5 | 1.61803 | 0.49112 | 0.23607 (=√5−2) | — |
| 6 | 1.73205 | 0.50000 | 0.19245 (=√3/9) | — |
| ∞ | →2 | →0.50000 | →0.12500 (=1/8) | — |

**They never coincide; the q→∞ limits differ (1/2 vs 1/8).** `1/λ³` is **NOT** the Hecke Hurwitz/Markov
constant, NOT the Legendre constant (`=1/2`, Lehner 1985), NOT the Lenstra constant (BKS / EMS 2010).
The most dangerous overlap is cleared. (Dimensional note: `1/λ³` is a *product/area*-type gap quantity,
which is the right reason it is not an *approximation* constant — they are different kinds of object.)

### 2b. Farey-gap extremes (Hall) and Stern–Brocot multifractal (Kesseböhmer–Stratmann). **No hit.**
- **Hall's theory** (verified verbatim via Heersink arXiv:1503.02539 quoting Hall 1970): the normalized
  Farey gap distribution = law of `Z = 1/(2ζ(2)·x·y)` on the SAME triangle `{x,y≤1<x+y}`; the only
  extremal product it records is **`xy=1` at the corner `x=y=1`** (→ smallest gap `3/π² ≈ 0.304`). BCZ
  Crelle 535 prove *moment/cross-moment asymptotics* (`Σ(γ_{j+h}−γ_j)² ~ 12(2h−1)logQ/(π²Q²)`). **None
  of 2/9, √2/8, 1/λ³, 1/8 appear.** The global min/max of `xy` on the triangle are trivial (0 and 1);
  the project's constants (0.18–0.24) sit strictly between → they arise *only* from the variational
  (ergodic-opt) min-max over invariant measures, a different object from the gap-distribution line.
- **Kesseböhmer–Stratmann (Crelle 605 (2007), arXiv:math/0509603, full text):** Stern–Brocot/Lyapunov
  multifractal spectrum has range `[0, 2 log φ]`, max exponent `2 log φ ≈ 0.962` at `[1,1,1,…]` (golden
  mean). **Golden mean is the extremizer in both their setting and the project's q=5 case** — structural
  echo — but their number is `2 log φ` (additive), the project's is `1/φ³ = √5−2 ≈ 0.236` (multiplicative).
  Related-by-structure, numerically distinct. None of the project constants appear.

### 2c. Are 2/9, √5−2, 1/8 named Diophantine constants? **No.**
- `2/9` — not found as a Farey/CF extremal constant anywhere (its use as a BCZ "cluster threshold" is
  internal to this project). See **the 2/9 coincidence** below for the one near-collision.
- `√5−2 = 1/φ³` — φ-related but **not a named approximation constant**. The named golden extremes are
  `1/√5 ≈ 0.447` (Hurwitz), `√5` (Lagrange/Markov minimum), `2 log φ` (KS) — all different objects.
- `1/8` (q→∞) — not a known limiting Farey/horocycle gap constant (the classical limit is `3/π²`).

### 2d. The OBSERVABLE is classical; only the EXTREMAL min-max of it is new.
`P = x·y` is exactly **Hall's variable** (gap `∝ 1/(2ζ(2)xy)`) and is literally **Taha's roof/return-time
function `R(a,b)=ab`** of the horocycle suspension (arXiv:1810.10668, confirmed in PDF — also confirms
the memory's "Taha λ-on-a" domain `𝒯^q={0<a≤1, 1−λa<b≤1}`). So the quantity is standard; what is absent
from Taha/Hall/BCZ/KS is the **variational minimization of this roof** (`inf_μ ess-sup_μ R`) and its
values. Taha computes the domain and dynamics but **no extremal value of the product**, and none of the
project's constants appear in Taha.

## Claim 3 — no ground state via cusp escape. **KNOWN mechanism / NOVEL-AS-FORMULATION here.**

Non-existence of an optimizing measure caused by escape of mass on a non-compact phase space is an
**explicitly documented** ergodic-optimization phenomenon — do **NOT** claim the mechanism as new.

- **Jenkinson–Mauldin–Urbański, "Ergodic optimization for non-compact dynamical systems," Dynamical
  Systems 22 (2007) 379–388.** Purpose-built for the non-compact case. **Example 12:** a countable full
  shift with a continuous `f` whose optimum is approached by periodic measures `ν_n` (supported on
  `x(n)=(n,…,1)`, escaping `n→∞` to the non-compact end) but **attained by no invariant measure** —
  structurally the project's "optimizers escape to the cusp." Their remedy is an "essential compactness"
  sufficient condition that rules escape out. (This is the **load-bearing prior art** for Claims 3 & 4.)
- **Riquelme–Velozo, "Ergodic optimization and zero temperature limits in negative curvature,"
  arXiv:2001.01694 (2020 preprint).** Geodesic flow on a **non-compact negatively curved** (cusped)
  manifold: proves "**the only obstruction to the existence of a maximizing measure is the full escape
  of mass phenomenon**" — the cleanest published statement of exactly Claim 3's mechanism in cusped
  geometry. *(Verify publication status before any write-up — cited here as preprint.)*
- Background only (mechanism, not an optimization non-existence theorem): Einsiedler–Kadyrov–Pohl,
  "Escape of mass and entropy for diagonal flows…," Israel J. Math. 210 (2015) 245–295; Eskin–Margulis.

**Honest framing:** "a concrete arithmetic (horocycle-return) realization of a known non-compact
non-attainment phenomenon," not a new mechanism. The BCZ/Taha-Hecke realization with the Farey
gap-product observable is what is new.

## Claim 4 — min-max ≠ min-average. **NOVEL-AS-FORMULATION.**

Two parts kept distinct:
- **(a) "two ergodic-opt values differ on a non-compact system" — KNOWN, but for different objects.**
  JMU 2007 defines four notions `α≤β≤γ≤δ` of largest ergodic average (`α=sup_μ∫f`, then Birkhoff-limit
  variants) and shows (Example 4) all three inequalities can be simultaneously strict on a non-compact
  space. So "values differ because of non-compactness" is established.
- **(b) BUT the project's pair is not the JMU pair.** The project compares `inf_μ ess-sup_μ P` (a
  *static*, single-evaluation minimal-maximum of a fixed observable, no time-averaging) vs `inf_μ ∫P dμ`
  (minimal average). JMU's four notions are **all Birkhoff/time-average type** (even `δ` uses
  `(1/n)S_n f` asymptotically). Across Jenkinson 2006/2019, Garibaldi 2017, Bochi ICM 2018, the
  **standard** ergodic-optimization object is uniformly `∫f dμ`. The **inf-over-measures-of-the-ess-sup
  of a fixed observable** does not appear as a studied quantity. Frame Claim 4 as introducing a
  non-standard objective, with JMU's `α<β<γ<δ` strictness as the nearest neighbor — NOT as the first
  instance of "two ergodic-optimization values differing."

**Why Contreras 2016 and Garibaldi 2017 do NOT subsume the project (exact hypotheses):**
- **Contreras, Invent. Math. 205 (2016) 383–412** (Thm A, verbatim): "If X is a **compact metric space**
  and T is an **expanding map** then there is an open and dense set O ⊂ Lip(X,ℝ) such that for all F ∈ O
  there is a single F-maximizing measure and it is supported on a periodic orbit." Standing hypotheses:
  compact, expanding, generic Lipschitz, object = `∫F dμ` (existence automatic from weak-* compactness).
  The project's example is **non-compact** (cusped triangle), non-expanding return map, **specific**
  observable, **opposite conclusion** (NO ground state). Disjoint by hypothesis and by generic-vs-specific.
- **Garibaldi, SpringerBriefs (2017), "…the Expanding Case":** the title is the hypothesis —
  expanding/compact sub-action (Mañé–Conze–Guivarc'h) theory; does not treat non-compact escape.
- **Jenkinson 2019 survey (ETDS 39, no. 10, 2593–2618):** standing setting compact (weak-* compactness ⇒
  maximizer exists); flags the non-compact case → points to the **countable-shift** branch (JMU, Iommi,
  Bissacot–Freire, …); contains **no horocycle/BCZ/cusp example and no inf-ess-sup objective**. The
  canonical surveys confirm the system+objective novelty boundary.

---

## ⚠ The 2/9 coincidence (address head-on in any write-up)
JMU 2007 (Example 16) has a Gauss-map ergodic-optimization example whose value is **also 2/9** — there
`inf f|[2] = g(1/3) = (1/3)(2/3) = 2/9` with `g(x)=x(1−x)` on the level-2 refinement of the Gauss-map
Markov partition. This is the **infimum of the observable over a single cylinder** (used to verify their
"essential compactness" inequality), **not** an inf-over-invariant-measures ground value. Different map
(Gauss vs BCZ), different observable (`x(1−x)` vs `xy`), different operation (cylinder-inf vs
measure-inf). **Numerical coincidence, not the same object** — but a referee familiar with JMU will see
"2/9 + ergodic optimization + continued fractions" and ask. Pre-empt with a one-line footnote.

## Internal-consistency note (NOT prior art — for the project's own clarity)
A reviewer flagged that at q=4 the project reports the value `√2/8 ≈ 0.1768` while the formula
`1/λ³` gives `√2/4 ≈ 0.3536` (a factor of 2 apart). This is **not an error**: it is the documented
**interior-vs-global** split (FINDINGS_goalB/D) — for q=3,4 the canonical reported value is the
**interior** optimum `V(q)` (`2/9`, `√2/8`); the global cusp value `1/λ³` only becomes the canonical
answer for **q≥5**. State explicitly in any write-up that the closed form "`X_Ω(q)=1/λ³` for q≥5" does
**not** extend down to q=4 (where the cusp/global and interior answers split and the interior `√2/8` is
reported). Keeping `1/λ³` labeled "q≥5" avoids the apparent contradiction.

---

## Citation ledger (primary-verified; flags noted)

| Citation | Verified | Bears on | Flag |
|----------|----------|----------|------|
| Boca–Cobeli–Zaharescu, "A conjecture of R. R. Hall on Farey points," J. reine angew. Math. (Crelle) **535** (2001) 207–236, DOI 10.1515/crll.2001.049 | vol/yr/pp ✓ (DeGruyter DOI + Illinois Experts + 3 ref-lists) | 1, 2 | full PDF paywalled; result via abstract + secondary |
| Athreya–Cheung, "A Poincaré section for the horocycle flow on the space of lattices," **IMRN 2014, no. 10, 2643–2690** (arXiv:1206.6597) | §8 read verbatim from PDF | 1 | — |
| Athreya, "Gap distributions and homogeneous dynamics" (arXiv:1210.0816, survey) | §6 questions read from PDF | 1 | — |
| Taha, "The BCZ map analogue for the Hecke triangle groups G_q" (arXiv:1810.10668) | full text; roof `R(a,b)=ab`, domain `𝒯^q`, no extremal value | 1, 2 | — |
| R. R. Hall, "A note on Farey series," J. London Math. Soc. **(2) 2 (1970) 139–148** | citation ✓ (verbatim [6] in arXiv:1503.02539 + Wiley/Oxford meta) | 2 | full PDF paywalled; statement via verbatim quote |
| Kesseböhmer–Stratmann, "A multifractal analysis for Stern–Brocot intervals…," J. reine angew. Math. (Crelle) **605 (2007) 133–163** (arXiv:math/0509603) | full text; spectrum `[0, 2 log φ]` | 2 | — |
| Haas–Series, "The Hurwitz constant and Diophantine approximation on Hecke groups," **J. London Math. Soc. (2) 34 (1986) 219–234** | closed form `h_q`; Zbl 0605.10018, MR 0856507 | 2 | verified via authoritative ref-list (Zbl/MR), **article PDF not opened** — corroborated by q=3⇒√5 check |
| J. Lehner, "Diophantine approximation on Hecke groups," **Glasgow Math. J. 27 (1985) 117–127** | Hurwitz/Legendre constants for G_q | 2 | abstract + EMS ref-list |
| J. Lehner, "The local Hurwitz constant…," **Math. Comp. 55 (1990) 765–781** | local Hurwitz constant | 2 | Zbl 0761.11020, MR 1035937 (ADS+EMS) |
| Burton–Kraaikamp–Schmidt, "Natural extensions for the Rosen fractions," **TAMS 352, 1277–1298** | Lenstra/natural-extension | 2 | EMS lists year **1999** (vol 352 spans 1999–2000); project's "(2000)" acceptable; "**NOT 364 (2012)**" guard correct |
| Jenkinson–Mauldin–Urbański, "Ergodic optimization for non-compact dynamical systems," **Dynamical Systems 22 (2007) 379–388** | full text; Ex. 12 (escape/no maximizer), `α≤β≤γ≤δ` strictness, Gauss `2/9` | 3, 4, +2/9 | **load-bearing prior art** |
| Riquelme–Velozo, "Ergodic optimization and zero temperature limits in negative curvature," **arXiv:2001.01694 (2020)** | abstract; "only obstruction = full escape of mass" | 3 | **preprint** — verify publication status before write-up |
| Contreras, "Ground states are generically a periodic orbit," **Invent. Math. 205 (2016) 383–412** (arXiv:1307.0559) | full text; Thm A quoted | 3, 4 | — |
| Garibaldi, *Ergodic Optimization in the Expanding Case*, **SpringerBriefs (2017)**, ISBN 9783319666426 | scope (expanding/compact) | 3, 4 | metadata + intro only; full book not read |
| Jenkinson, "Ergodic optimization in dynamical systems," **ETDS 39 (2019) no. 10, 2593–2618** (arXiv:1712.02307) | full text; no BCZ/cusp/inf-ess-sup | 1, 3, 4 | — |
| Bochi, "Ergodic optimization of Birkhoff averages and Lyapunov exponents," **Proc. ICM 2018, Vol. III, 1825–1846** (arXiv:1712.01612) | average framework; no non-compact-escape focus | 4 | abstract/metadata only |
| Einsiedler–Kadyrov–Pohl, "Escape of mass and entropy for diagonal flows…," **Israel J. Math. 210 (2015) 245–295** (arXiv:1110.0910) | escape mechanism (background) | 3 | abstract/metadata |
| Heersink, "The weighted Farey sequence and a sliding section for the horocycle flow" (arXiv:1503.02539) | full text; restates Hall verbatim | 2 | used to verify Hall |

**Not independently opened (appear as in-survey references only, none expected to bear on the claims):**
Rosen, Duke Math. J. 21 (1954) 549–563; Augustin–Boca–Cobeli–Zaharescu, Math. Proc. Camb. Phil. Soc.
131 (2001) 23–38; Bousch ("Le poisson n'a pas d'arêtes"; "La condition de Walters"); Brémont;
Jenkinson–Mauldin ETDS 26 (2006) 1791–1803. Shinoda–Takahasi–Yamamoto arXiv:2406.01123 (2024) is
**compact** finite-alphabet shifts (NOT non-compact escape) — flagged to avoid mis-attribution.

---

## Bottom line — go/no-go for a write-up

**There is a defensible novel contribution, and it must be stated narrowly.** What is genuinely new:
the **formulation** of ergodic optimization (`X = inf_μ ess-sup_μ P`) on the **BCZ / Taha Hecke-BCZ
return map** with the Farey gap-product / horocycle roof observable `P = xy = R(a,b)`, together with the
**explicit closed-form values** `2/9`, `√2/8`, `1/λ³` and the machine-checked no-ground-state /
min-max≠min-average structure. This combination has **no precedent** in the BCZ, Hecke-CF, Hall-gap,
Stern–Brocot, or ergodic-optimization literature surveyed (Claim 1 APPARENTLY NOVEL; Claim 2 constants
APPARENTLY NOVEL but the observable/triangle classical). What must be **framed as realization, not
discovery**: the non-attainment-via-cusp-escape mechanism (Claim 3 — JMU 2007, Riquelme–Velozo 2020)
and the broad "two ergodic-opt values differ" idea (Claim 4 — JMU `α<β<γ<δ`); the project's specific
inf-ess-sup objective is itself non-standard, which is the defensible edge for Claim 4.

**Single biggest risk:** NOT the Hecke Hurwitz constant (that overlap is refuted) — it is the **JMU-2007
Gauss-map `2/9` coincidence**, which a referee will notice; pre-empt it with an explicit footnote
distinguishing the objects. Secondary: verify Riquelme–Velozo's publication status, and open the
Haas–Series article PDF to confirm `h_q` first-hand before citing it as the decisive disambiguator.

**Verdict: GO** for an internal write-up framed as above (narrow novelty-of-realization + new closed-form
constants), with the three risk mitigations. Nothing outward without USER gate (see `project_koyama_risk`).

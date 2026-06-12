# Breakthrough scout 2026-06-12 — 2 picks (workflow wf_cb3d33f5-bd2)

6 literature scouts + 4 adversarial vets (10 agents, full-text checks of key papers,
citation sweeps). Raw structured output:
`/private/tmp/claude-501/-Users-za-Documents-farey-hecke/9d0f51b7-5d5a-44df-b0b4-fea55481e603/tasks/w1rmwej4b.output`
(copy below is the durable record).

## PICK 1 — "First machine-verified theorem in ergodic optimization" (direction C, vet 6.0, NOT refuted)

Assemble the honest top-level Lean statement: `X(3) = inf over BCZ-invariant probability
measures of ess-sup(gap-product) = 2/9`, attainment included, + the q=3/4/6 cluster trio
as corollaries.

- **Novelty confirmed across Lean/Isabelle/Coq, 7 independent search angles, all negative
  (as of 2026-06-12).** Nearest prior art: Gouëzel's Isabelle AFP `Ergodic_Theory`
  (Birkhoff/Kingman/Kac — no optimization); in-progress Lean Birkhoff projects
  (mseri/BET, lua-vr/pointwise-birkhoff); Mathlib has only ergodicity defs + Birkhoff-sum
  algebra. Venue precedents: O. Nash Gallagher (ITP 2023, arXiv:2302.00448); **Annals of
  Formalized Mathematics** (founded 2024, vol. 1 July 2025) — made for exactly this.
- **Audience:** formalization community ~200–400 realistic readers/citers + EO community
  (~50–150; fresh intro survey arXiv:2605.13342 May 2026). Largest audience of any direction.
- **Vet's load-bearing finding (repo inspection):** v10 `BCZOnsetQStar.lean` glues its two
  inputs as **axiom stubs** and defines onset arithmetically (1−μ(S)); nothing in the corpus
  quantifies over invariant measures; bczMap measurability + invariance of 2dxdy unformalized.
  The "first in EO" card = building exactly that wrapper.
- **Vet's easier-than-feared path:** all-invariant-measures lower bound follows from the
  already-proved pointwise cluster bound via `μ(S ∩ T⁻¹S ∩ T⁻²S) = 0` — **no
  Prokhorov/weak-\* compactness needed**; attainment via explicit periodic-orbit atomic measure.
- **Framing constraint:** claim "first in *ergodic optimization*", NOT "thermodynamic
  formalism" — Mathlib already has `Dynamics.TopologicalEntropy` (Bowen–Dinaburg).
  Pre-empt "ess-sup EO is elementary" objection (reduces to inf over minimal closed
  invariant sets of max f) by stating the reduction and showing where it gets nontrivial.
- **Risk:** ~70% publishable AFM/ITP paper in 3–6 months; window risk from
  Gouëzel-adjacent Lean dynamics cell real but no in-flight competitor surfaced.
- **First task:** formalize bczMap measurability + 2dxdy invariance (the genuinely novel
  formalization content), then the faithful inf-over-measures statement.

## PICK 2 — Uniform Hecke onset theorem + arithmeticity dichotomy (directions A+B merged, vets 6.0/5.5, NOT refuted)

Headline (per vet advice): **the arithmeticity dichotomy** (cluster ceiling ≤2 ⟺ q∈{3,4,6})
+ **the uniform bound X_Ω(q) ≥ 1/λ_q³** for all q; explicit X(q) values as corollaries,
not headline.

- **Genuinely open at the statement level:** Taha 1810.10668 + 1906.07250 full-text-checked —
  no support minimum, no 1/λ³ value, no cluster analysis, no EO. Taha 1810.10668 has only
  4 citing papers, none touching this. Marklof–Pollicott 2408.01781 = tails not support edge
  (2 citations). The slope-gap community computes this family **one surface per paper**
  (octagon 2109.04495, double heptagon 2508.19252 Aug 2025) — direct evidence the uniform
  problem is unclaimed AND hard, and a ready-made citing audience.
- **Audience:** translation-surface/slope-gap school (Athreya, Chaika, Sanchez + REU pipeline)
  + homogeneous-dynamics extreme events (Marklof, Pollicott, Strömbergsson) + EO; ~30–60
  active researchers. Clean-niche, not hot-field.
- **Framing landmines (must cite/handle):** Geninska–Leuzinger math/0609477 (arithmeticity ⟺
  bounded trace-set clustering — kills any "first statistic detects arithmeticity" claim);
  ABCZ MPCPS 131 (2001) h-spacing + Cobeli–Zaharescu math/0511363 (q=3 consecutive-gap
  support — q=3 cluster≤2 plausibly implicit there; position against it); Bogomolny–Schmit
  nlin/0312057 (non-arithmetic Hecke also has exponential trace multiplicities — handle
  head-on; actually argues FOR the statistic); Rudnick–Zhang 1509.02989; Marklof–Vinogradov
  1409.3764; Heersink 1403.7502; arXiv:2410.05223 (Schmutz conjecture, 2024).
- **Referee risk:** per-q X(q) value extraction may be judged routine minimization of Taha's
  R_q; 2n-gon paper 2109.04495 is family-uniform-algorithmic precedent. Value concentrates
  on the uniform corridor-classification proof — the 35–50% branch.
- **Normalization trap (internal):** X(3)=2/9 vs 1/λ_3³=1 — interior vs cusp normalization
  differs across q; make explicit in any writeup, referee checks q=3 first.
- **Risk:** full uniform theorem ~35–50%; publishable weaker package (finite-range dichotomy
  + q=5 formal 3-cluster witness + conjecture + first-formalization angle) ~85%.
  Ceiling JMD/ETDS/Monatshefte; GAFA-tier only if uniform all-q witness lands.
- **First task:** machine-verify the q=5 three-cluster witness (finite algebra in Q(φ),
  Aristotle-dispatchable, days-to-weeks) — completes the verified dichotomy through q=6
  and is independently the "other half" of the iff.

## Rejected

- **D certified Hausdorff dimension — REFUTED (4.0).** Collision: Marchese arXiv:1812.11921
  already proves the Hensley-type first-order asymptotic for non-uniform Fuchsian lattices
  via Bowen–Series transfer operators (Hecke G_q not explicitly covered — his Assumption 2.1
  unverified for G_q). Our own C_q data kills the clean headline (drift q≥9). "First
  machine-verified fractal dimension" is scoopable in weeks via Mathlib's existing
  `cantorSet` (dimH = log2/log3). **Salvage (cheap, feeds goal-L):** verify Marchese
  Assumption 2.1 for G_q + compute Θ(G_q) — days of numerics.
- **E ζ-separator — DROP (3).** Farey vs GUE already classical: Hall distribution support
  floor 3/π² (Hall 1970) separates without any new statistic; GUE side settled (Ben
  Arous–Bourgade 1010.1294, Bourgade 1812.10376 — Poisson extreme gaps ⇒ no clustering);
  ζ-side cluster counting needs triple-correlation control unavailable even under RH
  (state of the art: one gap < 0.50895 mean spacing, arXiv:2604.05733). Salvageable core
  (exact extremal-index family for G_q-BCZ) is an EVT-for-dynamics niche note; the REPP
  limit theorem for a zero-entropy parabolic section is genuinely open and 50%+ stall risk.
- **F three-gap/Hecke — DROP (3).** Everything natural already in print: IET Steinhaus done
  (Taha 1708.04380 + IMRN 2023), Hecke Λ_q gap statistics done (Taha), adelic three-gap done
  (2107.05147), restricted-denominator Farey = active conveyor belt (2507.00228 etc.).
  Prime-denominator Farey gap law open but bottleneck = sparse equidistribution at prime
  times (Sarnak–Ubis, Ramanujan-conditional) — wrong toolbox for us. Only unclaimed artifact:
  first Lean three-gap formalization (Coq-only since 2000, Mayero cs/0609124) — ITP-value only.

## Synergy note

Picks 1+2 share one spine: Pick 1's faithful invariant-measure wrapper (measurability,
invariance, inf-over-measures) is exactly the formal infrastructure Pick 2's uniform
X_Ω(q)≥1/λ³ statement needs later. Sequence: Pick 1 first (fast, high-probability,
establishes the formal EO framework + priority), Pick 2's q=5 witness in parallel via
Aristotle, then the uniform corridor program with the framework in hand.

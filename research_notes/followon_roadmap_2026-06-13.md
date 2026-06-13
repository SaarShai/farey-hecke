# Follow-on roadmap — 5 breakthroughs stemming from the uniform onset theorem

**Date:** 2026-06-13. **Precondition:** the central breakthrough closed —
**X_Ω(q) = 1/λ_q³ uniformly for all Hecke G_q** (+ arithmeticity dichotomy corollary).
What that result HANDS us, and what each path stems from:
- **(A) Theorem:** an explicit, family-uniform support-edge / ergodic ground value 1/λ³.
- **(B) Method:** GATE-2 corridor-classification + arc-coverage + energy(=rotation-ellipse) — the
  FIRST family-uniform support-edge technique (field previously did one-surface-per-paper).
- **(C) Bridge:** ergodic-optimization ground value = extreme-gap cluster onset (machine-verified).
- **(D) Dichotomy:** a LOCAL dynamical statistic detecting the GLOBAL arithmetic property.

Each path below is prior-art-gated (run the scout+adversarial-vet before committing), as the
project always does. Reachability is honest, not promotional.

---

## Path 1 — X_Ω(Γ): a new lattice invariant (port the uniform method beyond Hecke)  [HIGHEST CEILING]
- **Stems from:** (B)+(A). **Open problem:** prove X_Ω(Γ)=explicit cusp-geometry value for
  general Veech surfaces / non-uniform Fuchsian lattices; does X_Ω(Γ) detect commensurability
  class (and arithmeticity) universally?
- **Significance:** turns a theorem into a *program* — collapses the one-surface-per-paper
  slope-gap industry into a family theory and defines a genuinely new computable invariant of a
  lattice. The biggest follow-on.
- **Reachability:** moderate-hard — GATE-2 corridor classification is triangle-group-specific;
  the conceptual frame (cusp-vertex ground value, corridor=rotation-ellipse) ports, the
  discreteness input must be re-derived per family.
- **First step:** numerically test the cusp-vertex X_Ω formula on the next family (2n-gon /
  Bouw–Möller Veech surfaces); does X_Ω track commensurability? Gate: Athreya–Chaika 1012.4298,
  KSW 2102.10069, effective slope-gap 2409.15660.

## Path 2 — Ground-state theory for parabolic / zero-entropy ergodic optimization
- **Stems from:** (C). **Open problem:** general existence / attainment / structure of "ground
  states" (minimizers of inf_μ ess-sup) for parabolic, zero-entropy section maps; is the ground
  value ALWAYS a cusp/parabolic-periodic value?
- **Significance:** opens a subfield — EO (Jenkinson/Bochi/Garibaldi) studies only
  sup-of-Birkhoff-averages; the L∞ / zero-temperature end for parabolic dynamics is unstudied.
  The Hecke result is the first worked example.
- **Reachability:** moderate — abstracting the right hypotheses from the Hecke proof.
- **First step:** isolate the minimal axioms under which "ground value = cusp-periodic value"
  holds; test on one non-Hecke section map. Gate: Jenkinson 1712.02307, Bochi, Motonaga 2411.17615.

## Path 3 — Local-statistic arithmeticity criterion for general cofinite Fuchsian groups
- **Stems from:** (D). **Open problem:** a LOCAL / effective dynamical statistic detecting
  arithmeticity for general cofinite Fuchsian groups — refining the GLOBAL trace-set criterion
  (Geninska–Leuzinger math/0609477, Luo–Sarnak 1994) to a local/effective one.
- **Significance:** Koyama's "paradigm shift" generalized; the bridge to arithmetic quantum chaos
  (Poisson vs GOE level statistics) via a *computable* local statistic. The genuine
  mathematical-physics reach.
- **Reachability:** hard — the Hecke dichotomy mechanism is integer cancellation (λ²∈ℤ);
  generalizing to other arithmeticity criteria is nontrivial. High value if it lands.
- **First step:** test the cluster-ceiling statistic on a non-triangle arithmetic-vs-non-arithmetic
  Fuchsian pair — does B=2 still track arithmeticity? Gate: Geninska–Leuzinger, Bogomolny–Schmit
  nlin/0312057, arithmetic-QUE literature, 2410.05223.

## Path 4 — Exactly-solvable extreme-value statistics for homogeneous-dynamics sections
- **Stems from:** (C)+(D). **Open problem:** the full limiting cluster-size distribution /
  extremal index θ_q of the BCZ rare-events point process, exactly and uniformly in q
  (generalizing the exact constant (8ln(3/2)−2)/9 at q=3); rigorous REPP convergence for the
  zero-entropy parabolic section.
- **Significance:** a rare FAMILY of exactly-solved extremal-index models — EVT-for-dynamics
  (Freitas–Freitas–Todd, Lucarini) has very few. The physics deliverable (#4 of the portfolio).
- **Reachability:** the q=3 constant is exact; the REPP limit theorem for a parabolic
  (polynomial-mixing) section is the hard step (~50%, per the E-scout).
- **First step:** compute θ_q exactly for q=4,5 from the invariant measure; check vs the
  cluster-size numerics. Gate: Freitas–Todd, Hsing 1991, Physica D 2023 cluster-distributions.

## Path 5 — Effective onset → effective equidistribution + Rosen-CF dimension spectrum
- **Stems from:** (B) + the validated transfer-operator / Jenkinson–Pollicott engine.
- **Open problem (two-pronged):** (a) make the onset EFFECTIVE — a uniform-in-q convergence rate
  to the gap distribution, feeding effective equidistribution of horocycle sections; (b) does the
  uniform onset constrain the Hausdorff-dimension spectrum of bounded-type Rosen-λ_q continued
  fractions uniformly?
- **Significance:** connects the support edge to the quantitative-equidistribution and
  dimension-theory programs; the JP engine (reproduces dim E_{1,2}=0.5312805062772 to 1e-15) is
  ready. Also the salvage of the dropped certified-dimension direction.
- **Reachability:** (a) moderate (effective tools exist, 2409.15660); (b) EXPLORATORY — our own
  C_q drift (q≥9) means no clean dimension law, and Marchese 1812.11921 governs the asymptotic.
- **First step:** (a) compute the uniform-in-q convergence rate numerically; (b) verify Marchese
  Assumption 2.1 for G_q + compute Θ(G_q). Gate: Marchese 1812.11921, Pollicott–Vytnova 2012.07083.

---

## Honest tiering
Path 1 is the headline (new invariant + program). Paths 2,3 are high-value-high-risk (new
theory / arithmeticity reach). Path 4 is the physics deliverable. Path 5 is quantitative/
exploratory (and reuses parked assets). These are GENUINE breakthrough-stemming directions —
a uniform method + a new invariant legitimately spawns a program — NOT the kind of co-equal
padding the 2026-06-12 scout refuted. Each requires its own prior-art gate before commitment.
Nothing outward without USER gate.

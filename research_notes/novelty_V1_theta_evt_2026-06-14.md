# Citation-grade novelty audit — Candidate V1 (θ = 1/2 universal for parabolic-cusp involution sections)

Date: 2026-06-14. Lens: dynamical extreme-value theory (EVT). Companion to
`research_notes/theta_half_repp_2026-06-14.md`. Default posture: "likely known"; we have
over-claimed novelty repeatedly this session, so near-misses are weighed against the candidate, not for it.

---

## CANDIDATE (V1, restated)

"For a measure-preserving cross-section map with a PARABOLIC (neutral, polynomial-mixing) cusp fixed point
whose cusp-return is a LEADING-ORDER INVOLUTION (period-2 swap), the extremal index of the natural gap
observable is θ = 1/2 UNIVERSALLY (surface/parameter-independent), with a compound-Poisson cluster law
degenerating to a point mass at cluster size 2." Established this session for the Taha G_q-BCZ map.

---

## VERDICT (a): **KNOWN as stated; PARTIAL-with-narrow-scope for one sub-claim.**

The headline "θ = 1/2 because exceedances come in pairs (mean cluster size 2)" is a **classical, textbook EVT
identity**, not a new theorem. The "universal / parameter-independent" framing does not rescue it: a mean
cluster size pinned to 2 by an exact symmetry gives θ=1/2 by definition, in any framework, with no surface
dependence — that is the *expected* behaviour, not a surprising one. The ONLY thing not already in the
literature is the **rigorous derivation of this θ for a PARABOLIC area-preserving cusp cross-section via
operator-renewal / polynomial-mixing-tower EVT** — and that derivation is **explicitly NOT done** in the
candidate note (it is flagged open). So the genuinely-new content is a *gap*, not a *result*.

This matches the honest self-assessment already in `theta_half_repp_2026-06-14.md` §7 (verdict "(b)
proved-modulo-a-named-limit-theorem"). The novelty audit's job here is to confirm that even the *target*
theorem, once proved, would be incremental — a new instance of an established pattern (FFT/CHN periodic-and-
symmetric clustering) extended to the parabolic regime that FFFV-Manneville–Pomeau already opened — not a
new unifying principle.

---

## (b) Closest papers (6)

1. **Freitas, Freitas, Todd — "Extremal index, hitting time statistics and periodicity"**, Adv. Math. (2012),
   arXiv:1008.1350. *The* source of the dynamical extremal-index-at-periodic-points formula
   **θ = 1 − 1/|det Df^p(ζ)|** (equivalently 1 − |det Df^{−p}|). Establishes: θ=1 at non-periodic points,
   θ∈(0,1) ONLY at **repelling** periodic points (needs |det Df^p|>1). — *Why it does/doesn't cover V1:* it
   IS the standard tool, and it **fails exactly as the candidate says**: at a parabolic point |det Df^p|=1 ⇒
   θ=0, vacuous. Confirms the candidate's "FFT degenerates" claim is correct and well-known.

2. **Freitas, Freitas, Todd, Vaienti — "Rare events for the Manneville–Pomeau map"**, arXiv:1503.01372
   (Stoch. Proc. Appl. 2015). The **closest precedent**: full Poisson/compound-Poisson REPP dichotomy for a
   map *with a neutral (parabolic) fixed point*. Result: at the neutral fixed point ζ=0 the **extremal index
   is 0** (degenerate, needs adapted norming); nontrivial compound-Poisson clustering occurs at *other*
   (hyperbolic) periodic points. — *Why it doesn't cover V1:* it studies the **distance-to-ζ / ball**
   observable, gets θ=0 at the parabolic point itself, and does **not** produce a finite nonzero θ (let alone
   1/2) from a period-2 swap *at* the parabolic point. V1's twist (the cusp return is a leading-order
   involution that yields a *finite* θ=1/2 rather than the degenerate 0) is genuinely outside this paper —
   but the *machinery* V1 would need (induce off the cusp, REPP on the tower, renewal back) is exactly this
   paper's program.

3. **Carney, Holland, Nicol — "Extremes and extremal indices for level set observables on hyperbolic
   systems"**, Nonlinearity 34 (2021), arXiv:1909.04748. Derives nontrivial θ for observables maximized on a
   **set** (line segment), with θ from (i) θ=1−λ^{−q} at periodic points and (ii) **geometric
   self-intersection** of the level-set submanifold under iteration — θ tied to the *multiplicity / geometry
   of the maximizing set*, "not arising from any periodicity." — *Why it doesn't cover V1:* **hyperbolic
   systems only** (toral automorphisms, Sinai billiards); no parabolic/neutral case. (CAUTION: a first
   unreliable PDF fetch claimed this paper states "θ=1/2 from a symmetric pair"; the authoritative ar5iv HTML
   does **not** — θ=1/2 is not singled out there. Do not cite CHN as already containing the symmetric-pair
   θ=1/2.) Still the nearest "θ from set-multiplicity, not expansion" idea, which is morally what V1's swap-
   pair does.

4. **Carvalho, Freitas, Holland, Nicol — "Extremal dichotomy for uniformly hyperbolic systems"**,
   arXiv:1501.05023. Hölder observable maximized at a point ⇒ θ=1 (non-periodic) or θ<1 (periodic), uniformly
   hyperbolic. — *Why it doesn't cover V1:* uniformly hyperbolic, point maximizer, same det-formula
   degeneracy at parabolic; no parabolic-cusp / involution case.

5. **Marklof, Pollicott — "Extreme events for horocycle flows"**, arXiv:2408.01781 (2024). EVT for the
   horocycle flow / Farey gaps — but for the **cusp-EXCURSION** (max penetration / large-gap) observable, with
   limit law given by **Hall's Farey-gap formula** (extends Kirsebom–Mallahi-Karai). — *Why it doesn't cover
   V1:* opposite end of the gap spectrum (large-gap / Gumbel-type cusp excursions), **not** the gap-PRODUCT
   small-gap lower-tail clustering of V1, and reports no θ=1/2 period-2 clustering. Confirms the live-literature
   EVT-for-horocycle work targets a *different observable* — which is where V1's only daylight is.

6. **Baravi, Barkai — "Extreme values of infinite-measure processes"**, arXiv:2603.05390 (2026). EVT in the
   *infinite-measure* / intermittent regime (return-exponent-α-controlled, departs from Fréchet/Gumbel/Weibull;
   fractional-Poisson limits). — *Why it doesn't cover V1:* studies the infinite-measure anomalous regime;
   V1's G_q-BCZ section is **finite** invariant measure with a parabolic point — the relevant theory is
   finite-measure polynomial-mixing (operator renewal, Gouëzel–Sarig towers, FFFV), not infinite-measure
   anomalous EVT. Shows the parabolic-EVT field is active but aimed elsewhere.

**Foundational (not dynamical) anchor:** Leadbetter (1983) θ = 1/(mean cluster size); θ=1/2 ⇔ clusters of
mean size 2 is the *single most elementary* illustration of the extremal index in classical stationary-
sequence EVT (O'Brien 1987 characterization, compound-Poisson exceedance process). This is why the bare
"θ=1/2 from period-2 clustering" is textbook and cannot be claimed as new.

---

## (c) Narrowest genuinely-new version that survives

NOT "θ=1/2 for parabolic-involution sections is a new universal theorem." That over-claims.

What survives, at most, as a **technical contribution (not a unifying principle)**:

> "A rigorous REPP / compound-Poisson convergence theorem with extremal index θ=1/2 and limiting multiplicity
> δ_{L=2} for the gap-product observable on the **parabolic, polynomial-mixing G_q-BCZ area-preserving cross-
> section**, where the cluster of size 2 is produced by the exact period-2 cusp-swap involution — obtained via
> operator-renewal/Young-tower EVT, in the regime where the FFFV Manneville–Pomeau dichotomy gives θ=0 at the
> neutral point and the FFT det-formula degenerates."

Even this survives ONLY if the named limit theorem is actually proved (it is currently open in
`theta_half_repp_2026-06-14.md` §6). And it is an *instance-level* extension — "FFFV/CHN-style clustering,
parabolic-cusp case, computed for the BCZ family" — not a new class theorem. The "universal across q" qualifier
adds little: q-independence follows trivially once the swap forces mean cluster size ≡ 2; an exact symmetry
pinning the cluster size is the *reason there is nothing surface-dependent left to compute*.

The "universal class result" ("involution at a parabolic cusp ⇒ θ=1/2 for the whole class") is **not** in the
literature as a stated theorem — but it is also not *proved* here, and as a statement it is close to a
tautology dressed as a theorem (involution ⇒ pairs ⇒ θ=1/2 by Leadbetter). The defensible new object is the
*analysis* (parabolic REPP limit), not the *value* θ=1/2 or its universality.

---

## (d) One honest sentence

This is **repackaging a textbook EVT fact** (θ = 1/(mean cluster size) = 1/2 for symmetry-forced size-2
clusters, Leadbetter/O'Brien) dressed as a unifying theorem; the only part that would be a real — and modest,
instance-level — contribution is the *unproved* rigorous parabolic-cusp REPP limit theorem via operator
renewal, which extends the FFFV Manneville–Pomeau and FFT/CHN periodic-clustering programs to one new family
rather than establishing a new principle.

---

## Sources

- arXiv:1008.1350 — Freitas, Freitas, Todd, *Extremal index, hitting time statistics and periodicity* (θ = 1 − 1/|det Df^p|).
- arXiv:1503.01372 — Freitas, Freitas, Todd, Vaienti, *Rare events for the Manneville–Pomeau map* (parabolic; θ=0 at neutral point).
- arXiv:1909.04748 — Carney, Holland, Nicol, *Extremes and extremal indices for level set observables on hyperbolic systems*.
- arXiv:1501.05023 — Carvalho, Freitas, Holland, Nicol, *Extremal dichotomy for uniformly hyperbolic systems*.
- arXiv:2408.01781 — Marklof, Pollicott, *Extreme events for horocycle flows* (cusp-excursion / Hall's formula).
- arXiv:2603.05390 — Baravi, Barkai, *Extreme values of infinite-measure processes*.
- Leadbetter (1983); O'Brien (1987) — classical extremal-index = 1/(mean cluster size) and compound-Poisson exceedance process.
- arXiv:1008.4113 — Sarig, *Operator renewal theory and mixing rates for dynamical systems with infinite measure* (the renewal machinery V1 would need).

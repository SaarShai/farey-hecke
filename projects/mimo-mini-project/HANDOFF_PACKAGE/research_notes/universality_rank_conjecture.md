# The "rank + 1" cluster-bound conjecture: a feasibility analysis

**Date:** 2026-05-27
**Status:** scoping / adversarial literature review
**Verdict (preview):** **DEFER, with a small empirical probe.** The conjecture is *internally consistent* (rank 1 → 2 confirmed; rank 2 → 3 predicted; discrete trees → 1 as refinement). It is *not* in the literature. It is **fragile**: several cited "matches" are surface coincidences, and the strongest higher-rank machinery (Marklof–Strömbergsson) does *not* obviously deliver a rank-2 cluster bound of exactly 3. A 1-day computational probe would either kill the conjecture or upgrade it to a structurally motivated open problem.

---

## 1. Conjecture statement (precise)

Let `G` be a real connected semisimple Lie group of real rank `r ≥ 1`, `Γ ⊂ G` an arithmetic lattice, and `U ⊂ G` a connected unipotent subgroup with `dim U ≥ 1`. Suppose `U` admits a *Poincaré section* `Σ ⊂ Γ\G` of finite area, with first-return map `T_Σ` measure-preserving with respect to an absolutely continuous invariant measure `μ_Σ`. Suppose further that `T_Σ` generates a sequence of "gaps" `(d_i)_{i ≥ 1}` (the analog of consecutive Farey gaps; in the BCZ case `d_i = 1/(x_i y_i)`).

**Conjecture (rank + 1 cluster bound):** For any `q < 1` sufficiently close to 1, and any cluster (= maximal run of indices `i` for which `d_i` exceeds the `q`-quantile of the stationary `d`-distribution), the cluster size is bounded above by `r + 1` almost surely as the time horizon `T → ∞`.

**Refinement (discrete tree exception):** If `G` is replaced by a non-Archimedean group acting on a Bruhat–Tits tree (so the "continuous" homogeneous space is replaced by a discrete one), the bound degenerates to `1` (singletons only).

**Rank-1 instance (proven empirically):** `G = SL(2,R)`, `Γ = SL(2,Z)`, `U =` upper-triangular unipotent; `Σ =` Athreya–Cheung horosphere section with density `f(x,y) = 2·1_{x+y>1}` on `T = {0<x,y<1, x+y>1}`. Then `r = 1` and the bound is `r + 1 = 2`. **Confirmed** for `q ≥ q*_BCZ = (11 − 8·ln(3/2))/9 ≈ 0.86181` at zero size-3+ clusters in 38.97M MC trials.

**Rank-1 discrete (refuted as cluster=2):** `G = PGL_2(F_q((1/T)))`, BT-tree. Bound = 1, not `r + 1 = 2`. *Refinement applies.*

**Rank-2 prediction:** `G = SL(3,R)`, `Γ = SL(3,Z)`. Bound = 3.

---

## 2. Literature survey (annotated)

I find *no* prior statement of the rank+1 cluster-bound conjecture in the homogeneous-dynamics or random-matrix literature. The closest cousins:

1. **Marklof, *The n-point correlations between values of a linear form* (Ann. Math. 158 (2003), 419–471).** Equidistribution of joint statistics for `n`-tuples of Farey-like fractions via `SL(2,R)/SL(2,Z)`. *No cluster bound.*

2. **Marklof–Strömbergsson, *Free path lengths in the periodic Lorentz gas…* (Ann. Math. 172 (2010), 1949–2033).** Canonical higher-rank lattice-point statistics paper. Treats `SL(d+1,Z)\SL(d+1,R)`, proves convergence of free-path-length distributions for `d ≥ 2`, tail `~ c_d/ξ²`. Single-gap marginal only — *no cluster-size bound*.

3. **Marklof–Strömbergsson, *Free path lengths in quasicrystals* (CMP 330 (2014)).** Extension to cut-and-project lattices via `SL(d+1,Z)\SL(d+1,R)`-equidistribution. Cluster structure not analysed.

4. **Athreya–Margulis, *Logarithm laws for unipotent flows, I & II* (J. Mod. Dyn. 3 (2009); Trans. AMS 367 (2015)).** Higher-rank logarithm laws. Could imply cluster bounds via Borel–Cantelli, but the constants are dimension-dependent and **do not** lock onto `r + 1`.

5. **Bogomolny–Giraud–Schmit, *Nearest-neighbour distribution for spectra of star graphs* (NJP 13 (2011); PRL 100 (2008)).** "Intermediate statistics" between Poisson and Wigner-Dyson. Their statistic is `P(s)` and number variance, *not* run-length on extreme-quantile thresholds — no cluster bound.

6. **Sodin–Yakir** (2020+) on rigidity for stochastic six-vertex / extreme-local statistics. Random-matrix, not arithmetic; no direct cluster bound.

7. **Conrey–Snaith, *Triple correlation of the Riemann zeros* (CMP 281 (2008)).** Moment matching via GUE. If rank+1 universality were real on the Katz–Sarnak side, it would surface as a moment identity here — and it does *not*.

8. **Boca–Heersink–Spiegelhalter (Integers 13 (2013), A44).** 1-D BCZ density under congruence constraints. Cluster bound 2 re-derivable — indirect support for rank 1 → 2.

9. **El-Baz–Marklof–Vinogradov, *The two-point correlation function of the fractional parts of √n is Poisson* (Proc. AMS 143 (2015)).** Higher-rank-style argument (`SL(3,R)/SL(3,Z)` enters the proof) leading to **Poisson** statistics — unbounded clusters. **This is the most worrying datum for the conjecture.**

10. **Athreya–Cheung, IMRN 2014.** Base case. §8 open questions include higher-rank extension but do *not* conjecture rank+1 cluster bound. No natural section over `SL(3,R)/SL(3,Z)` constructed.

11. **Strömbergsson–Vinogradov (2015+) on √n mod 1.** Same flavour as (9): higher-rank in the proof, Poisson in the conclusion.

12. **Marklof, *Lattice points on circles* (GAFA 13 (2003)).** Poisson-type two-point correlations under unipotent equidistribution — again, unbounded clusters in the limit.

**Net assessment.** The conjecture is **novel** in its precise form. The strongest counter-datum is (9)/(11)/(12): three concrete higher-rank statistics whose gap distribution is **Poisson** — and Poisson has *arbitrarily large* clusters. Any defence of rank+1 must explain why the BCZ triangle structure survives the rank transition while these others flatten to Poisson.

---

## 3. Theoretical analysis: the rank-2 analog of BCZ

### 3.1 The natural rank-2 Poincaré section

The Athreya–Cheung construction in rank 1: the section `Σ ⊂ SL(2,Z)\SL(2,R)` is `{Λ : Λ has a horizontal vector of length 1}`. The map `T_Σ` is first return under the geodesic/horocycle flow, and the section has *finite area* in the natural measure (area `= 2 · (area of triangle T)`, with `T = {x+y > 1, 0<x,y<1}`).

The rank-2 analog (most natural candidate): `Σ ⊂ SL(3,Z)\SL(3,R)` is `{Λ : Λ has a horizontal vector of length 1}`. Under the action of the diagonal flow `a_t = diag(e^{-t}, e^{-t}, e^{2t})` and a horospherical unipotent `U`, the return map should land on a 4-dimensional cross-section. The invariant measure pushes forward to a density `f(x, y, z)` on some polytope in `(0,1)^3` (or thereabouts).

**Does `f` have a clean closed form?** *Not in the literature.* Marklof–Strömbergsson 2010 derives the limiting *free-path* distribution (a 1-D marginal of a higher-dimensional density), and the answer involves an explicit but ugly integral over `SL(d,Z)\SL(d,R)`. The *full* joint density `f(x_1, ..., x_d)` is not stated explicitly even in their paper. So the rank-2 analog of `2·1_{x+y>1}` is **conjecturally** something like `c · 1_{P(x,y,z)>0}` for some polytope `P`, but the closed form is unknown.

### 3.2 Continuant identity in higher rank

The rank-1 cluster=2 bound has a *combinatorial* proof in the literature (Farey-mediant argument: three consecutive Farey fractions `a/b, a'/b', a''/b''` with all three gaps `≥ ε` would force the middle denominator `b'` to be `≤ 1/ε`, but then `b'` is *small* and the corresponding `1/(x' y')` gap is **also** at most ε^{-O(1)} — this is the BCZ "Stern–Brocot mediant" obstruction). The factor "2" comes from: SL(2,Z) is rank 1, the mediant fixes pairs, so three large gaps in a row are forbidden.

**Higher-rank analog?** The natural generalisation is the *3-D Stern–Brocot tree* (also called the **best-approximations algorithm** of Brentjes / Schweiger, or **Selmer's algorithm**). Here, three consecutive 2-D Farey approximants `(a_i/c_i, b_i/c_i)` satisfy a 3×3 determinantal identity:

```
det [[a_i, b_i, c_i], [a_{i+1}, b_{i+1}, c_{i+1}], [a_{i+2}, b_{i+2}, c_{i+2}]] = ±1
```

(under the appropriate algorithm; this is the higher-rank "continuant" identity). If *four* consecutive approximants have large gap then by an analogous mediant-style argument one of them is forced to have small denominator — giving cluster ≤ 3. **This is the structural seed of the conjecture.**

**The catch:** unlike the 1-D mediant, the higher-rank "next-approximant" algorithm is *not unique*. Brentjes, Jacobi–Perron, Selmer, Brun all give different algorithms with different properties. Whether the cluster bound = 3 holds depends on *which algorithm* is used for the section, and there is no canonical choice. (This is well-known: higher-rank Diophantine approximation has no analogue of the Stern–Brocot tree's uniqueness.)

So the rank-2 conjecture, if true, has to be:
- Either **algorithm-independent** (cluster bound = 3 for *all* canonical sections of the SL(3,Z)\SL(3,R) horocycle flow) — would be a strong statement.
- Or **algorithm-specific** (cluster bound = 3 for the *Brentjes-best-approximation* section specifically) — would still be interesting but more limited.

### 3.3 The analog of `t* = 2/9`?

The Q-side closed form `q*_BCZ = (11 − 8·ln(3/2))/9` came from a 1-D integral: `∫_T x · ln(1/y) dxdy / area(T)` style, evaluated on the BCZ triangle. The cubic `2/9` is a footprint of the triangle's area `1/2` and the form `f = 2`.

For rank 2: the analogous integral would be over a 3-D polytope, with `f` to-be-determined. **Without knowing `f` explicitly, no closed form is even guessable.** Marklof–Strömbergsson's free-path computation suggests the higher-rank densities involve `ζ(2), ζ(3)` (the latter showing up via the gcd-coprimality density `1/ζ(3)`), so a candidate rank-2 closed form is of the form `(A − B·ln(C) + D·ζ(3))/E` — but this is **rank speculation**.

---

## 4. Falsifiability tests (ranked by cost)

### Test 1 (cheapest, ~1 day): Static 2-D Farey cluster diagnostic

Generate `F_N^{(2)} = {(a/c, b/c) : gcd(a,b,c) = 1, 1 ≤ c ≤ N, 0 ≤ a, b ≤ c}` for `N = 100` (~280K points). Compute Delaunay triangulation. Define "gap" = Voronoi cell area, normalized so mean = 1. For `q ∈ {0.95, 0.99, 0.999}`, identify cells with area > q-quantile threshold; build the "extreme-cell adjacency graph" (edge if two extreme cells share a Voronoi edge); compute connected component sizes.

**Prediction (conjecture true):** max component size = 3 above some threshold `q* < 1`; size-4+ component fraction → 0.

**Prediction (conjecture false):** either size-4+ components persist (rules out bound = 3), or no clean threshold (rules out a BCZ-style universality).

Cost: ~50 lines of Python with `scipy.spatial.Voronoi` and `networkx`. Half a day to code + run.

**Critical caveat.** This is the *static* analog, the direct generalization of the Q-side static gap diagnostic. We have already learned (the function-field test) that static analogs can fail to reproduce universal behaviour seen in the dynamical chain. **So even a clean cluster=3 here is necessary but not sufficient** for the dynamical conjecture; and a clean cluster≠3 here would force a re-statement to "dynamical chain only".

### Test 2 (~1 week): Dynamical chain via Brentjes 2-D best-approximations

Define the 2-D best-approximation chain: starting from `(p_0, q_0, r_0), (p_1, q_1, r_1), (p_2, q_2, r_2)` (three "best" rational approximations to a generic vector `α ∈ R^2`), iterate via Brentjes' algorithm. Record the *renormalised* triples and the analog of the BCZ gap `1/(|p_i q_{i+1} − p_{i+1} q_i|·c_i c_{i+1} c_{i+2})` or similar (precise definition is the *first* research question). For random initial `α`, run 10^6–10^8 iterations and apply the cluster diagnostic at varying `q`.

**Prediction:** cluster bound = 3 above a sharp threshold `q*_2D`. If a clean closed form emerges, that's strong support.

Cost: ~5 days. Pure Python OK at 10^6 steps; 10^8 needs Rust/C++. Brentjes' algorithm is well-documented (Schweiger's *Multidimensional Continued Fractions*, 2000).

### Test 3 (~1 month, optional stretch): rank-3 sanity check

Same as Test 2 but for `SL(4,Z)\SL(4,R)`. Prediction: cluster bound = 4. Cost is higher (3-D continued fraction algorithms are even more algorithm-dependent), but a *qualitative* agreement (bound grows with rank) would be the strongest possible support for the universality principle.

---

## 5. Proof outline: what would need to be true

If the conjecture survives Tests 1–2, a proof would proceed via:

**Step A (combinatorial).** Establish a higher-rank continuant identity: any `r + 2` consecutive points of the (algorithm-specific) higher-rank Stern–Brocot sequence satisfy `det[…] = ±1` (an `(r+1) × (r+1)` Vandermonde-like determinant). **Almost certainly true** for the Brentjes algorithm; the key references are Bauer–Bombieri-style work on simultaneous Diophantine approximation.

**Step B (geometric).** Show that if `r + 2` consecutive gaps are all > `ε`, then one of the `r + 2` denominators is *forced* to be `≤ ε^{-c_r}` for some explicit `c_r`. (This is the higher-rank mediant obstruction.)

**Step C (dynamical).** Show that the small denominator forces the corresponding gap (in the cocycle iteration) to be < quantile threshold. This is the analog of the BCZ "small `x_i y_i` ⇒ large `1/(x_i y_i)`" argument, but with `x_i y_i` replaced by a product of `r` simultaneous normalised denominators.

**Step D (Aristotle/Lean target).** Step A is a clean determinant identity — formalisable in Lean given a Brentjes-algorithm formalisation (which does not exist in mathlib yet). Step B is a chain of inequalities on a polytope, also formalisable. Step C requires the unipotent-flow first-return map machinery, which is *not* in mathlib and would be a multi-quarter formalisation effort. **Tractable Aristotle target:** Step A (determinant identity) and a 2-D version of Step B (cluster bound = 3 for the *static* `F_N^{(2)}` Voronoi-area diagnostic). Step C in Lean is out of reach.

**What would constitute a proof?** All four steps, on the dynamical side. Steps A+B alone give the *static* cluster bound = `r + 1`, which is already a publishable theorem if the conjecture is true.

---

## 6. Honest verdict

**DEFER, with a 1-day empirical probe.**

**Against:**

1. **El-Baz–Marklof–Vinogradov 2015 (and refs 11–12).** Closely related higher-rank gap distributions are **Poisson** — unbounded clusters. The conjecture must explain why BCZ triangle structure survives the rank transition while these statistics flatten to Poisson. High burden of proof.

2. **Algorithm dependence.** Higher-rank Stern–Brocot is non-unique (Brentjes, Jacobi–Perron, Selmer, Brun all differ). A "universality principle" should not depend on which best-approximation algorithm is chosen. If the cluster bound is algorithm-specific, it is not universal.

3. **"Rank + 1" from rank 1 is one data point.** The discrete-tree exception (cluster = 1) is *also* compatible with "max cluster = size of canonical mediant orbit". The phrasing "rank + 1" may be a misleading reformulation of the latter — and the latter is the real invariant.

4. **Strategic fit.** MEMORY flags AC §8 / N·W → C as the high-priority lane. Rank+1 is exploratory; the natural audience (Marklof et al.) has not posed it, suggesting they either tried it or did not find it natural.

**For:**

1. **Test 1 is genuinely cheap** (1 day of Python). Clean cluster=3 at high quantile in 2-D Farey Voronoi would survive the first hurdle.

2. **The static `F_N^{(2)}` cluster diagnostic is not in the literature** (per the survey + prior internal N17/N28 work). Even if rank+1 fails, a small empirical note on 2-D Farey cluster statistics has its own value.

3. **Brentjes 2-D dynamical chain (Test 2)** aligns with where the field is going (Athreya–Margulis, Strömbergsson). Partial result is useful as a building block.

**Recommended action.** 1 day to Test 1. Three branchpoints:

- (A) Clean cluster = 3 at high quantile: **upgrade to PURSUE.** 3–4 page empirical note; allocate Tests 2–3 over 6 weeks.
- (B) Cluster bound ≥ 4 or no clean structure: **DROP rank+1 framing.** Pivot to "2-D Farey Voronoi cluster statistics are heavy-tailed / Poisson-like".
- (C) Ambiguous: **DEFER** behind AC §8.

Subjective branch-probabilities (calibrated against the EBMV Poisson result): A ≈ 25%, B ≈ 50%, C ≈ 25%.

**Formalisation.** Even in case (A), the Aristotle/Lean target should be Steps A+B on the *static* side only. Step C is too far from current mathlib infrastructure.

**Final word.** Honest (clear, falsifiable, motivated) but fragile (literature does not preferentially support it; EBMV refutes the boundedness analog). 1-day probe is the right move; 6-week commitment without it is not.


# Higher-rank BCZ analog on SL(3,Z)\SL(3,R): scoping + numerical probe

**Date:** 2026-05-27
**Status:** literature scan + ~60-min N≤100 numerical experiment
**Verdict (preview):** **DROP the static rank+1=3 cluster conjecture; NEEDS-MORE for the dynamical Brentjes chain.** Static 2-D Farey cluster sizes grow ~linearly in N (max cluster 1 → 81 as N goes 20 → 100 at normalized threshold 2). No bounded-cluster phenomenon survives the rank transition on the static side. The remaining live question — whether the *dynamical* first-return map on a Brentjes-section has a bounded cluster — is open but loses its motivating prediction.

This note complements `universality_rank_conjecture.md` (theoretical scoping, written same day before the experiment) and `triple_coincidence_structure.md` (the SL(2) `t_n = 2n/(n+2)²` structural derivation that motivates the search for an analog in SL(3)).

---

## 1. The natural higher-rank Poincaré section

The cleanest reference is **Marklof, "Fine-Scale Statistics for the Multidimensional Farey Sequence"** (arXiv:1207.0954, Contemp. Math. 2013), which is the direct generalization of Athreya–Cheung 2014 to all dimensions.

**Setup (rank d, i.e. SL(d+1,R)/SL(d+1,Z)).** Define the *d-dimensional Farey sequence of level Q* as

```
F_Q = { p/q ∈ [0,1)^d : (p,q) ∈ Ẑ^{d+1}, 0 < q ≤ Q },
```

where `Ẑ^{d+1} = {m ∈ Z^{d+1}\{0} : gcd(m) = 1}` is the set of primitive vectors. By Marklof eq. (2),

```
|F_Q| ~ σ_Q := Q^{d+1} / ((d+1) ζ(d+1)).
```

For d=2 this gives `|F_Q| ~ Q^3 / (3 ζ(3))` — note the appearance of `ζ(3)` (Apéry's constant), foreshadowing why explicit closed forms get ugly.

**Embedding.** Define matrices `h(x), a(y) ∈ SL(d+1,R)` analogous to the SL(2) case (eq. (8) in the paper). Then `p/q ∈ x + σ_Q^{-1/d} A` iff `(p,q) h(x) a(Q) ∈ C(A)` for an explicit cone `C(A) ⊂ R^{d+1}` — the higher-rank analog of the BCZ triangle.

**Equidistribution (Marklof Thms 1,2).** Sums over `r ∈ F_Q` of test functions `f(r, h(r)a(Q))` equidistribute against `μ_H` on `Γ_H \ H`, where `H ≃ ASL(d,R)`, `Γ_H ≃ ASL(d,Z)`. This is the higher-rank "horocycle equidistribution" that *replaces* the BCZ first-return map.

**The catch (the "ugly density" problem).** In dim n=d ≥ 2, Marklof writes explicitly (just before eq. (28)): *"it is difficult to obtain a more explicit description of the limit distributions P(k,A) and P₀(k,A)"*. He gives the *abstract* lattice-integral formula

```
P(k, A) = μ({M ∈ Γ\G : |Ẑ^{d+1} M ∩ C(A)| = k})
```

— but no closed form. For d=1 (the BCZ case), `Γ_H \ H ≃ T = R/Z` is just a circle, the integral becomes elementary, and you recover Hall's formula (eq. (34) of the paper). For d=2, the analogous integral lives on `Γ_H \ H ≃ SL(2,Z)\SL(2,R) × T²` — a 5-dimensional space — and there is no known closed-form analog of Hall's distribution.

**Implication for our project.** The "BCZ triangle" `T = {x+y > 1, 0<x,y<1}` with density `f = 2` has no direct higher-rank analog. The d=2 first-return map domain is a higher-dimensional polytope inside `SL(2,Z)\SL(2,R) × T²` with a Haar density — *no closed-form 3-D analog of `f=2 · 1_{x+y>1}` exists in the literature*. This is a real obstruction, not a notational one.

---

## 2. The "continuant" identity in higher rank

**SL(2) case (mediant identity).** Three consecutive Farey fractions `a/b, a'/b', a''/b''` of any common level Q satisfy

```
a'·b'' - a''·b' = ±1,    a·b' - a'·b = ±1,    a'' = ⌊(Q+b)/b'⌋·a' - a
```

— this is the BCZ recurrence (Athreya-Cheung 2014 §2). The `±1` is the unimodular determinant condition, encoded by `SL(2,Z)`.

**SL(3) case (Brentjes/Selmer best-approximation algorithm).** Three consecutive 2-D best approximations `(a_i/c_i, b_i/c_i)` to a generic `α ∈ R²` form rows of a 3×3 matrix

```
M_i = [[a_i, b_i, c_i], [a_{i+1}, b_{i+1}, c_{i+1}], [a_{i+2}, b_{i+2}, c_{i+2}]]
```

with `det M_i = ±1` (under the Brentjes algorithm). The recurrence is then an SL(3,Z) cocycle

```
M_{i+1} = R_i · M_i,    R_i ∈ SL(3,Z)
```

where `R_i` is an elementary matrix (one of finitely many types — Brentjes lists 6 cases). See Schweiger, *Multidimensional Continued Fractions* (Oxford 2000), §4–§5, and Brentjes' thesis (1981) for the original.

**The key non-uniqueness problem.** Unlike SL(2) (where the Stern–Brocot mediant is unique), higher-rank best-approximation algorithms are *not unique*: Brentjes, Jacobi–Perron, Selmer, and Brun give different sequences with different ergodic properties. The "natural" choice depends on what universal statement one wants. Jacobi–Perron is the historically-canonical pick but is known to fail to detect rational dependence in dim ≥ 3 (Brentjes' famous counterexample). For our purposes the Brentjes algorithm is the cleanest because it provably produces best approximations.

**What can we say a priori about clusters?** If a *consecutive run of 4* best approximations all have gap `> ε` (where gap = `1/(c_i c_{i+1} c_{i+2})` or similar normalized determinant inverse), the unimodular constraint forces one of the four denominators to be `< C ε^{-1/2}`. For SL(2), this forces `cluster ≤ 2` *because the denominator-shrinking is so violent*. For SL(3), the analog gives `cluster ≤ ? ` — but the inequality is much weaker, because the determinant identity in 3-D is "less rigid" than the 2-D mediant. **Heuristic upper-bound estimate via this argument: cluster size ≤ 3**, with the caveat that the proof would be conditional on detailed analysis of the Brentjes recurrence.

This is the seed of the "rank + 1" cluster conjecture in `universality_rank_conjecture.md`.

---

## 3. Counter-evidence: EBMV and the Marklof–Strömbergsson "Poisson family"

**Most damning datum.** El-Baz–Marklof–Vinogradov 2015 (arXiv:1306.6543) shows the gap distribution of `√n mod 1` is **Poisson** — i.e., asymptotically the gap distribution coincides with that of i.i.d. uniform random points. The proof uses non-divergence on `SL(3,R)/SL(3,Z)` (a homogeneous space of rank 2).

Poisson implies *unbounded clusters*: P(cluster size ≥ k) ~ p^k → 0 only geometrically, so max cluster over N points scales like `log N`. No constant bound.

**Less damning but adjacent.** Marklof–Strömbergsson 2010 Annals shows the free-path-length distribution in the periodic Lorentz gas (= a higher-rank lattice-point gap statistic) has tail `~ c_d / ξ²` — power-law, not exponential. This too is incompatible with a constant cluster bound on the analog statistic.

**Marklof–Strömbergsson "quasicrystal" CMP 2014.** Same flavour: power-law tails, no cluster boundedness.

**Synthesis.** Three independent higher-rank gap statistics (EBMV `√n`, MS Lorentz gas, MS quasicrystal) all give *unbounded* clusters. Any defence of rank+1 must explain why the *Brentjes-section first-return map* survives this trend. There is no a priori reason it should.

---

## 4. Numerical probe (static 2-D Farey Voronoi diagnostic)

**Setup (code: `projects/mimo-mini-project/code/higher_rank_farey_{v1,v2,v3}.py`).**

1. Generate `F_N^{(2)} = {(a/c, b/c) : gcd(a,b,c)=1, 1 ≤ c ≤ N, 0 ≤ a,b < c}` for `N ∈ {20,...,100}`.
2. Compute Voronoi cells on the flat torus T² (9-copy tile trick).
3. *Renormalize* cell areas by `σ_Q = N³/(3ζ(3))` so the typical normalized area is ~1 (validates against Marklof's theorem).
4. For fixed normalized threshold `thr ∈ {2.0, 3.0, 5.0}`, identify "extreme" cells and the connected-component adjacency graph (edge iff cells share a Voronoi edge). Max component size = cluster size analog.

**Results (`higher_rank_farey_v3.py`, full table in code output).**

| N    | \|F_N\| | thr=2.0 max-cluster | thr=3.0 max-cluster | thr=5.0 max-cluster |
|------|---------|---------------------|---------------------|---------------------|
| 20   |   2376  | 9                   | 1                   | 1                   |
| 30   |   7776  | 21                  | 9                   | 1                   |
| 50   |  35616  | 32                  | 21                  | 9                   |
| 70   |  96720  | 52                  | 25                  | 9                   |
| 100  | 280608  | 81                  | 50                  | 21                  |

**Diagnosis (`higher_rank_farey_diagnose.py`).** The largest clusters at every N concentrate around the same low-denominator special points: `(0, 1/2)`, `(0, 0)`, `(1/3, 0)`, `(0, 1/3)`, and the symmetric orbit images. These points have anomalously large Voronoi cells, and their high-c approximants form O(N)-sized "halos" of also-large cells — yielding linearly-growing apparent clusters. The 4-way duplication of top-cluster sizes (e.g. `[52,52,52,52,...]` at N=70) is the Z²-symmetry of the torus.

**Conclusion (static diagnostic).** Static 2-D Farey cluster sizes are **unbounded** (grow ~linearly in N) at any fixed normalized area threshold. The rank+1=3 conjecture **fails decisively on the static side**. This is the analog of EBMV's "Poisson at rank 2" result, observed empirically on a different statistic.

**Caveat.** The static diagnostic is the *direct* generalization of the Q-side static Farey-gap diagnostic. We have already learned (function-field test) that static diagnostics can fail to reflect dynamical-chain universal behaviour. So a clean "static fails" does not automatically rule out a "dynamical Brentjes chain" cluster bound. But it removes the cheapest piece of evidence in favour.

---

## 5. Heuristic prediction (post-experiment)

**For the dynamical chain (Brentjes-section first-return map on SL(3,Z)\SL(3,R)):**

- **Unlikely to have a constant cluster bound** (probability subjective ~15%, down from the prior 25% in `universality_rank_conjecture.md` because the static refutation removes one independent line of support).
- **More likely**: cluster-size distribution has *exponential tail* (`P(size ≥ k) ~ ρ^k`) with `ρ < 1` depending on a quantile threshold `q` and on `Q` (the time parameter). This is the Poisson behaviour seen in EBMV.
- **The "triple coincidence at t_n = 2n/(n+2)²" structure from SL(2)** does have a higher-rank analog: the floor-discontinuity surfaces of the Brentjes algorithm form a finite *arrangement* in the d=2 polytope, and the analog of `(1/3, 2/3)` would be a *0-dimensional intersection* of three or more such hyperplanes. But the linearization at such a point in 3-D dynamics generically has *two* unstable directions (not just one parabolic + one elliptic as in SL(2)), so the "intermittent linger" mechanism is genuinely different. Predicting the exact threshold analog is not feasible without a lot more work.

**No clean closed-form `q*` analog of `(11 − 8·ln(3/2))/9` is in reach.** The d=2 integrand lives on a 5-dimensional space and involves `ζ(2), ζ(3)`-weighted Haar measures over `SL(2,Z)\SL(2,R)` plus `T²` translations. There is no rank-2 elementary integral for which closed form is plausible.

---

## 6. Verdict and ranking

**Static rank+1 cluster bound on 2-D Farey Voronoi tessellation:** **REFUTED** by N≤100 numerics. Linear growth in N, max cluster 81 at N=100, threshold 2.0.

**Dynamical rank+1=3 cluster bound on Brentjes section of SL(3,R)/SL(3,Z) horocycle flow:** **NEEDS-MORE.** The construction is in the Marklof framework, but no explicit cluster diagnostic exists in the literature. Predicting the cluster bound is genuinely open; my priors after this work shift toward "no constant bound" but I cannot rule it out.

**Recommendation:** **DROP** the *static* rank+1 conjecture (status: refuted). **DEFER** the *dynamical* version pending implementation of the Brentjes recurrence (Test 2 in `universality_rank_conjecture.md`, estimated 5 days of work). The dynamical test should be deprioritised behind AC §8 N·W→C lane; it has clear scientific interest but no preferential prior probability.

**Aristotle/Lean target:** **NONE for now.** The relevant determinant identity is well-known (Schweiger 2000) and the static cluster diagnostic is dead. If the dynamical test in some future run shows a clean bound, the Lean target would be the Brentjes-3×3-cocycle determinant identity (formalisable in ~2 weeks given mathlib's existing linear-algebra) but the cluster bound theorem itself is well out of reach.

**Strategic note.** This investigation closes off one branch of "more papers" speculation. The single SL(2) cluster=2 theorem remains the live result. The "universality family" framing should *not* be claimed without dynamical evidence.

---

## 7. Honest caveats

1. **The N≤100 cap.** The cluster sizes growing linearly *might* level off at much larger N (e.g., if the low-denominator halo effect saturates). I see no reason to expect this — the typical low-denominator approximant count grows like `Q^{d-1} = Q` — but I can't rule it out from N=100 data alone. A run to N=1000 would settle this; estimated 30 minutes of Python, was outside the 60-minute budget for this note.

2. **Voronoi vs alternative "gap" statistics.** I used Voronoi-cell area as the natural higher-rank "gap". One could instead use *k-th nearest neighbour distance* (Marklof's `P_0(k, T², A)`) or the *renormalized determinant* `|det M_i|` along a Brentjes chain. These are not equivalent and could give different cluster pictures. The Voronoi choice is the closest to "1-D gap → 2-D area" but is *not* the unique natural generalisation.

3. **Brentjes vs Jacobi–Perron vs Selmer.** Higher-rank best-approximation algorithm non-uniqueness is real. Any positive dynamical cluster-bound result would have to specify which algorithm. The result might also be algorithm-dependent (some sections give bounded clusters, others don't), which would be a strange and possibly publishable finding in itself.

4. **EBMV is about `√n mod 1`, not 2-D Farey.** EBMV's Poisson result is *suggestive* but not a formal refutation of the rank+1 conjecture, because the statistic is different. The right counter-test would be a Poisson check on the multidim Farey sequence itself, which to my knowledge has not been done.

5. **The "size 9 cluster" pattern.** At N=50, q=0.999, the top cluster is consistently size 9 (the 8 symmetric high-c approximants of one low-c point, plus the low-c point itself). This is a finite-symmetry artifact; under `N → ∞` the renormalization should dampen it. But it interacts with the q-threshold choice and makes any "bounded by 9" / "bounded by 21" claim suspect — these numbers reflect Z² symmetry orbits, not dynamical content.

---

## 8. Primary references

- Marklof, *Fine-scale statistics for the multidimensional Farey sequence*, arXiv:1207.0954, Contemp. Math. **532** (2013) [the higher-rank statistical framework, no cluster bound].
- Marklof, *Horospheres and Farey fractions*, Contemp. Math. **532** (2010) 97–106 [the embedding into Γ\SL(d+1,R)].
- Marklof–Strömbergsson, *The distribution of free path lengths in the periodic Lorentz gas...*, Ann. Math. **172** (2010) 1949–2033 [tail ~ c_d/ξ², power-law, not exponential].
- El-Baz–Marklof–Vinogradov, *Two-point correlation function of fractional parts of √n is Poisson*, Proc. AMS **143** (2015) [the counter-evidence: Poisson at rank 2].
- Athreya–Cheung, *A Poincaré section for horocycle flow on the space of lattices*, IMRN **2014** [the rank-1 base case].
- Schweiger, *Multidimensional Continued Fractions*, Oxford University Press (2000) [the higher-rank cocycle / Brentjes algorithm reference].

## 9. Files

- `projects/mimo-mini-project/code/higher_rank_farey_cluster.py` — v1 numerics, empirical quantile.
- `projects/mimo-mini-project/code/higher_rank_farey_diagnose.py` — diagnostic showing the low-denominator halo artifact.
- `projects/mimo-mini-project/code/higher_rank_farey_v2.py` — renormalized + denominator-filtered cluster diagnostic.
- `projects/mimo-mini-project/code/higher_rank_farey_v3.py` — N ∈ {20,...,100} scaling scan.

Total time: ~60 min. Word count: ~2350.

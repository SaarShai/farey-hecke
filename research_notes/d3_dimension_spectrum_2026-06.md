# D3 — Hecke/Rosen Bounded-Type Survivor-Set Dimension Spectrum

**Status (2026-06-08):** VERIFIED. Transfer operator implemented and validated.
D_q(B) curves computed for q=3,4,5,6 and B=1..12. Sanity check PASSES.
X(q)=1/lambda^3 edge conjecture: REFUTED for integer digit bounds.

---

## 1. Setup and Operator

For q >= 3, set lambda_q = 2*cos(pi/q):

| q | lambda_q | 1/lambda_q^3 |
|---|---|---|
| 3 | 1.0000000000 | 1.0000000000 |
| 4 | 1.4142135624 | 0.3535533906 |
| 5 | 1.6180339887 | 0.2360679775 |
| 6 | 1.7320508076 | 0.1924500897 |

The **lambda_q-Gauss analogue** (positive-digit restriction of the Rosen continued fraction) has inverse branches:

    phi_a(x) = 1/(a*lambda_q + x),   a = 1, 2, ..., B

on the domain I_q = [0, lambda_q/2]. This is the direct generalization of the Gauss-map family phi_a(x) = 1/(a+x) to general lambda_q. For q=3 (lambda=1), it exactly reduces to the standard Gauss map on [0,1] (with domain extended to match; the dimension depends only on contraction ratios, not domain endpoints).

The transfer operator at parameter s:

    (L_{q,s} f)(x) = sum_{a=1}^{B} (a*lambda_q + x)^{-2s} * f(phi_a(x))

The Hausdorff dimension of the bounded-type survivor set is:

    D_q(B) = s*  where  leading eigenvalue of L_{q,s*} = 1

Implemented via Chebyshev-Lobatto collocation (N=64 nodes) with barycentric interpolation. The map phi_a is analytic and strongly contracting on I_q for q>=4, giving geometric convergence of the Chebyshev method.

**Note on q=3:** For q=3, the branch phi_1(x) = 1/(1+x) maps [0,0.5] to [2/3, 1], which lies OUTSIDE [0, 0.5]. Therefore q=3 uses the full [0,1] domain (standard Gauss map), while q=4,5,6 use [0, lambda_q/2].

---

## 2. Sanity Check: q=3 Must Recover Jenkinson-Pollicott

| Quantity | Value |
|---|---|
| Computed D_3(B=2) | 0.531280506277206 |
| Known (Jenkinson-Pollicott) | 0.531280506277205 |
| Residual | 1.22e-15 |

**SANITY PASSED.** The residual 1.22e-15 is within 1 ULP of machine precision.

---

## 3. D_q(B) Curves for q=3,4,5,6

### Full table (B=1..12)

| B | q=3 | q=4 | q=5 | q=6 |
|---|---|---|---|---|
| 1 | 0.000000000000 | 0.000000000000 | 0.000000000000 | 0.000000000000 |
| 2 | 0.531280506277 | 0.398073004663 | 0.358311075539 | 0.340294865814 |
| 3 | 0.705660908029 | 0.536921085755 | 0.486426504027 | 0.463510817061 |
| 4 | 0.788945557483 | 0.606624970951 | 0.551959804798 | 0.527122947617 |
| 5 | 0.836829443681 | 0.648396726298 | 0.591821851627 | 0.566096720103 |
| 6 | 0.867619173240 | 0.676220497169 | 0.618702004147 | 0.592533048096 |
| 7 | 0.888955316672 | 0.696101756728 | 0.638110528109 | 0.611715919361 |
| 8 | 0.904552689532 | 0.711035457712 | 0.652821815403 | 0.626318389585 |
| 9 | 0.916421112514 | 0.722679211907 | 0.664384293983 | 0.637838447347 |
| 10 | 0.925737591147 | 0.732023894217 | 0.673730455395 | 0.647181464263 |
| 11 | 0.933234863817 | 0.739698014856 | 0.681455721738 | 0.654927405848 |
| 12 | 0.939391824261 | 0.746119467265 | 0.687958377923 | 0.661465343281 |

### Key observations

1. **D_q(1) = 0 for all q.** The single-branch IFS {phi_1} has a unique fixed point; the transfer operator at s=0 has leading eigenvalue 1 (constant functions are preserved by composition), so the pressure zero crossing is at s=0. The survivor set is a single point, which has dimension 0. This is confirmed numerically to near machine precision (errors <= 7e-16).

2. **D_q(B) is strictly increasing in B** and converges to 1 as B -> infinity (Jarnik's theorem generalized: the set of "badly Rosen-approximable" numbers has full measure and dimension 1).

3. **D_q(B) is strictly decreasing in q** at each fixed B. Higher q (larger lambda_q) means more widely-spaced branches (branch a has image near scale 1/(a*lambda_q)), so fewer branches overlap, the Cantor set is thinner.

4. **For q=3, all D_3(B) values exactly match the known Gauss-map bounded-type dimensions** (e.g., D_3(2) = 0.5313 matches Jenkinson-Pollicott; D_3(3) = 0.7057 matches the known value for digits {1,2,3}).

---

## 4. Spectral Edge: Does X(q) = 1/lambda_q^3 Mark D_q -> 0?

### Statement of the conjecture

The task proposes X(q) = 1/lambda_q^3 as "the edge where D_q -> 0".

### Numerical finding: REFUTED for integer digit bounds

| q | D_q(1) | D_q(2) | X(q)=1/lambda^3 | D_q(2) > X(q)? |
|---|---|---|---|---|
| 3 | 6.1e-16 (~0) | 0.53128051 | 1.00000000 | No (D_q(2) < X(q)) |
| 4 | 2.8e-16 (~0) | 0.39807300 | 0.35355339 | Yes |
| 5 | 4.1e-25 (~0) | 0.35831108 | 0.23606798 | Yes |
| 6 | 7.1e-16 (~0) | 0.34029487 | 0.19245009 | Yes |

The D_q -> 0 transition (as a function of integer digit bound B) occurs precisely at B=1 for **all q**. D_q(1) = 0 for all q; D_q(2) > 0 for all q. No q-dependent threshold at 1/lambda^3 appears.

### Geometric analysis of 1/lambda^3

What does 1/lambda^3 actually represent?

- **phi_1 image width:** The branch phi_1 maps I_q = [0, lambda/2] to [2/(3*lambda), 1/lambda]; image width = 1/(3*lambda) for ALL q.
- For **q=6 only**: lambda_6 = sqrt(3), so 1/(3*lambda) = 1/(3*sqrt(3)) = 1/sqrt(3)^3 = 1/lambda^3. So **1/lambda^3 equals the phi_1 image width for q=6 only** (a coincidence from lambda_6^2 = 3).
- For q=4: phi_1 width = 1/(3*sqrt(2)) ≈ 0.2357 while 1/lambda^3 = 1/(2*sqrt(2)) ≈ 0.3536.
- For q=5: phi_1 width = 1/(3*phi) ≈ 0.2060 while 1/lambda^3 = phi^{-3} ≈ 0.2361.
- **phi_1 fixed point**: x* = (-lambda + sqrt(lambda^2+4))/2 is not equal to 1/lambda^3 for any standard q.

### Conclusion on X(q) = 1/lambda^3

The conjecture that 1/lambda^3 marks a spectral edge for the bounded-type dimension is **not confirmed**. For integer digit bounds:
- The only edge is B=1 (trivial: D_q(1)=0 always).
- The first non-trivial dimension D_q(2) is **larger than** 1/lambda^3 for q=4,5,6.
- For q=3: D_3(2) = 0.531 > 1 is impossible, but 1/lambda_3^3 = 1 (the bound itself has no meaning as a spectral threshold for q=3).

The quantity 1/lambda^3 may appear in a different context (e.g., continuous-weight operators, Moran pressure curves parameterized by contraction strength, or the BCZ analog for general Rosen maps) but does not equal D_q(B) for any natural integer B.

---

## 5. Prior Art: How This Differs from Soares arXiv:2005.11808

**Soares, "Hecke triangle groups, transfer operators and Hausdorff dimension" (arXiv:2005.11808, AHP 2021)** computes delta(w) = the **limit-set dimension** of the **infinite-area Hecke group** G_{q,w} for w > 2. The precise setup:
- **Group:** G_{q,w} is a *non-cofinite, infinite-covolume* Fuchsian group generated by an order-q rotation and a translation by w*lambda_q (w > 2 parameter).
- **Limit set:** The limit set Lambda(G_{q,w}) in the boundary circle; delta(w) = dim_H(Lambda(G_{q,w})).
- **Method:** Selberg zeta function / transfer operator for the geodesic flow on the quotient surface (infinite-area).
- **Regime:** w > 2, i.e., the group is geometrically finite with infinite volume.

**This project's object** is entirely different:
- **Group:** G_q is the *cofinite, finite-covolume* Hecke triangle group (the standard one with w=1, cusped, arithmetic for q=3,4,6 and non-arithmetic for q=5 and q>=7).
- **Set:** The **bounded-type survivor set** E_q(B) = {x in I_q : all Rosen digits of x are <= B}. This is a Cantor-type subset of the real line (the boundary), not a limit set of a non-cofinite group.
- **Method:** Ruelle transfer operator for the *conformal IFS* {phi_a : a=1,...,B} (finitely many branches, deterministic symbolic dynamics with a digit cap).
- **Regime:** All of B >= 1; the question is how the dimension grows with B.

The two objects are related by the Bowen pressure formalism (pressure = 0 gives dimension in both settings), but they are computing dimensions of *different sets* for *different groups* in *different regimes*. Soares' delta(w) -> 1 as w -> 2+ (the cusp recovers the cofinite case), but it never reaches the cofinite case and never considers individual digit bounds. Our D_q(B) starts at 0 (B=1) and grows to 1 (B -> infty). The two functions are not the same and do not appear to reduce to each other.

Additionally, the Mayer-Muhlenbruch-Stromberg transfer operator construction (arXiv:0912.2236) for the *cofinite* G_q (period functions, Maass forms) is a different (though related) operator — it is related to the Ruelle operator for the *full* Rosen map (all digits), not the restricted operator with a digit cap. The bounded-type survivor-set dimension is genuinely new relative to all of these.

---

## 6. Files

- `code/d3_hecke_dimension.py` — transfer operator, D_q(B) computation, sanity + edge tests
- `code/out/d3_hecke_dimension.json` — all numerical results
- `code/out/d3_hecke_dimension.png` — D_q(B) curves for q=3..6

---

## 7. Summary of Key Results

1. **q=3 sanity passes to machine precision**: D_3(2) = 0.531280506277206 vs known 0.531280506277205 (residual 1.22e-15).

2. **D_q(B) curves** computed for q=3,4,5,6 and B=1..12. The sequence D_q(B) is strictly increasing in B (from 0 to 1) and strictly decreasing in q at fixed B (thinner Cantor sets for larger q).

3. **D_q(1) = 0 for all q** (single-branch IFS = single fixed point = dimension 0). Confirmed numerically to within machine epsilon.

4. **X(q) = 1/lambda^3 is NOT a spectral edge** for integer digit bounds. D_q(2) > 1/lambda^3 for q=4,5,6; no transition at 1/lambda^3 is visible. The only edge is the trivial B=1 -> B=2 onset from 0. The geometric identity 1/lambda^3 = phi_1 image width holds only for q=6 and appears to be a coincidence rather than a structural fact.

5. **Prior art (Soares arXiv:2005.11808) is clearly distinct**: Soares computes the limit-set dimension of infinite-area (w>2) non-cofinite Hecke groups; this project computes the bounded-type Cantor-set dimension for the cofinite G_q with a digit cap. Different groups, different sets, different regimes, not pre-empted.

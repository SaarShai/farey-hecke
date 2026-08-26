# T1 GAP-7 — van Trees (Bayesian Cramér–Rao) replacement of unbiasedness

**DRAFT (grok lane) 2026-08-26 — UNREFEREED.**

Scope: replace the unbiasedness hypothesis (R5) of
`T1_CRAMER_RAO_DRAFT.md` by a Bayesian Cramér–Rao (van Trees) inequality,
with an explicit prior on the zero-location parameter matched to the draft's
(M5) / Lemma-1 geometry. Every constant below is derived. This note does
not modify the draft or any other file. Ziv–Zakai is not treated
(OWED-7).

Inputs used as given, not re-derived: the draft's Lemma 2 3×3 (factor 24,
convention (2.1)), A_j = 2 a_{γ_j}, (T1-b) S_ε(γ) = a_γ² log(γ/2π) on the
target tones, operating point T = log(3·10⁷) = 17.2167, K = 4,
log(γ_d/2π) = 2.06961, log(γ_1/2π) = 0.81076. Rounding convention of this
lane: error bounds UP, margins DOWN.

---

## 0. Headline

Under the raised-cosine prior (P1) of §3 (half-width α = πK/T, Fisher
information I(π_γ) = T²/K²), the van Trees bound on the Bayes MSE of γ_j
is

  E_π[(γ̂_j − γ_j)²] ≥ 1 / ( I^eff_j + I(π_γ) )
                      = [ 24 S_ε(γ_j) / (A_j² T³) ] / (1 + r_j)

with the explicit dimensionless ratio

  **r_j = 6 log(γ_j/2π) / (K² T) = O(T^{−1})**.                    (0.1)

As T = log X → ∞, r_j → 0, so the information-cost law's leading
constants are **unchanged**:

  c_d = √6,     X(ε) ≥ exp( (6 log(γ_d/2π))^{1/3} ε^{−2/3} ).

At the draft's finite operating point (T = 17.2167, K = 4, j = d) one has
r_d ≤ **0.0451** (rounded UP) and the RMSE margin (1+r_d)^{−1/2} ≥ **0.978**
(rounded DOWN). That 2.2 % finite-T hit sits inside T1's already-declared
O(K^{−1}) = 0.25 envelope. Unbiasedness is dropped: the bound applies to
every measurable estimator of the band-limited record, including T2.

---

## 1. GAP-7 as logged, and what unbiasedness was doing

Ledger entry (`T1_CRAMER_RAO_DRAFT.md` §6):

> GAP-7 | Unbiasedness (R5). The T2 estimator (windowed periodogram +
> quadratic refinement) is biased at finite T, so T1 as stated does not
> directly bound it. Route: replace CR by a van Trees / Bayesian CR bound
> with a prior on Θ, or by a Ziv–Zakai bound (which also captures the
> threshold effect the periodogram exhibits). Changes constants. | §1.5,
> §3 (R5) | **FRONTIER**

The frequentist Cramér–Rao inequality used in the proof of T1 is: for an
estimator θ̂ that is unbiased on an open neighbourhood of the true θ,

  Cov(θ̂) ⪰ I(θ)^{−1},

hence Var(γ̂_j) ≥ [I^{−1}]_{γ_j γ_j}. Condition (R5) is exactly that
unbiasedness. It is a restriction on the estimator class, not a property
of model N2. Periodogram-type estimators (T2) have a finite-T location
bias of order the window's frequency-domain sidelobe asymmetry, so T1 as
stated does not apply to them.

Two standard repairs exist. This note takes the first; the second is
logged as OWED-7.

- van Trees / Bayesian CR: drop unbiasedness, bound the *Bayes* MSE under
  an explicit prior. Constants can change; they will be computed, not
  asserted.
- Ziv–Zakai: bound the MSE of any estimator via the tail of a binary
  detection error; captures the SNR-threshold / sidelobe-ambiguity
  breakdown of the periodogram. Not derived here.

---

## 2. The van Trees inequality, stated precisely

### 2.1 Univariate form (Van Trees 1968)

Let θ ∈ ℝ carry a prior density π, absolutely continuous on an interval
(θ_min, θ_max), with π(θ_min) = π(θ_max) = 0 and

  I(π) := ∫ (π'(θ))² / π(θ) dθ  < ∞.

Let p(x | θ) be a regular parametric family (the same (R1)–(R4) the draft
already checked under (M4′)+(M4″)+(M5): mutual absolute continuity of
P_θ, differentiable log-likelihood, differentiation under the integral,
finite nonsingular Fisher information I(θ)). Let θ̂ = θ̂(x) be an
arbitrary measurable estimator (no unbiasedness). Then

  **E[(θ̂ − θ)²] ≥ 1 / ( E_π[I(θ)] + I(π) )**,                     (2.1)

the expectation on the left being over the joint law π(dθ) P_θ(dx).

*Citation.* Van Trees, H. L. (1968), *Detection, Estimation, and
Modulation Theory, Part I*, Wiley, Chapter 2, §2.4 (the “unconditional”
or Bayesian Cramér–Rao bound). An earlier statement is Schützenberger
(1957); the form used as a working inequality in statistics is Gill–
Levit (1995), cited next.

*Proof of (2.1), written out so the boundary condition is visible.* Let
λ(x,θ) := ∂_θ log p(x|θ) + ∂_θ log π(θ) be the score of the *joint* law
of (x,θ). Under (R3) and π(θ_min)=π(θ_max)=0,

  E[λ] = ∫ π'(θ) dθ + E[ E[∂_θ log p | θ] ] = [π(θ_max)−π(θ_min)] + 0
        = 0,

and, writing Δ := θ̂ − θ,

  E[Δ λ] = ∫∫ Δ (∂_θ p) π dx dθ + ∫∫ Δ p π' dx dθ
         = − ∫∫ p π (∂_θ Δ) dx dθ     (parts in θ; boundary term
                                       Δ p π vanishes because π does)
         = ∫∫ p π dx dθ
         = 1,

since ∂_θ Δ = −1. Cauchy–Schwarz then gives 1 = (E[Δ λ])² ≤ E[Δ²] E[λ²].
The mixture information is

  E[λ²] = E[ (∂_θ log p)² ] + E[ (π'/π)² ]
        = E_π[I(θ)] + I(π),

cross term zero because E[∂_θ log p | θ] = 0. Rearrangement is (2.1). ∎

The same Cauchy–Schwarz with any other square-integrable test function in
place of λ gives a (weaker) bound; (2.1) is the case that saturates for
the efficient score of the mixture.

### 2.2 Multivariate form (Gill–Levit 1995)

Let Θ ⊂ ℝ^p be open, π a density with compact support in Θ, π = 0 on
∂(supp π), I(θ) the p×p Fisher information matrix, ψ: Θ → ℝ of class C¹.
For any estimator T of ψ(θ),

  E[(T − ψ(θ))²] ≥ ãᵀ ( J̄ + J^π )^{−1} ã,                         (2.2)

where ã := ∫ ∇ψ(θ) π(θ) dθ,  J̄ := ∫ I(θ) π(θ) dθ,  and

  J^π_{jk} := ∫ (∂_j π ∂_k π) / π dθ.

*Citation.* Gill, R. D. and Levit, B. Y. (1995), “Applications of the van
Trees inequality: a Bayesian Cramér–Rao bound”, *Bernoulli* **1** (1/2),
59–79, Theorem 1.

Taking ψ(θ) = γ_j (a coordinate) gives ã = e_{γ_j} and

  E[(γ̂_j − γ_j)²] ≥ [ (J̄ + J^π)^{−1} ]_{γ_j γ_j}.                 (2.3)

If J̄ + J^π is block-diagonal across tones up to relative O(K^{−1})
(draft Lemma 3(a), still OWED as a clean lemma — GAP-5), the
γ_j-diagonal of the inverse is the scalar Schur complement of that
tone's 3×3, which is computed in §4.

### 2.3 What (2.1)–(2.3) are, and what they are not

- A bound on **Bayes MSE** under π, including bias². No unbiasedness.
- Not a pointwise frequentist bound at a fixed θ, and not a minimax bound
  (that is the spec's N3 programme). It becomes uniform on supp(π) to
  relative error equal to the variation of I(θ) there — which, for the
  prior in §3, is the existing GAP-4 flatness factor, not a new van Trees
  term.
- Not a bound on the *unrestricted* record y: the observation remains the
  band-limited record y_Ω of (M4′), as in T1.

---

## 3. The prior (P1), matched to the draft

### 3.1 Why a uniform prior is illegal

The uniform density on a compact interval has π' = 0 in the interior, so
I(π) = 0 formally, but it **fails** π(θ_min)=π(θ_max)=0. The boundary
term in the proof of (2.1) does not vanish, and (2.1) need not hold.
(This is the standard trap; Gill–Levit p. 61 require the vanishing
explicitly.) A smooth bump that *does* vanish is required.

### 3.2 Raised-cosine (Hann) density

On the dimensionless interval u ∈ [−1, 1] set

  λ(u) := cos²(π u / 2) = (1 + cos(π u))/2.

Then ∫_{−1}^{1} λ = [u/2 + sin(πu)/(2π)]_{−1}^{1} = 1, so λ is a
probability density, λ(±1) = 0, and λ'(±1) = 0. The score is

  λ'(u) = −π cos(πu/2) sin(πu/2) = −(π/2) sin(π u),

  (λ')² / λ = π² sin²(π u / 2)     (finite at the endpoints: value π²),

  **I(λ) = ∫_{−1}^{1} π² sin²(π u / 2) du = π²**.                   (3.1)

(The last integral: sin²(πu/2) = (1 − cos(πu))/2, ∫_{−1}^{1} = 1.)

Scale to the ordinate: for a centre μ and half-width α > 0,

  π_γ(γ) := α^{−1} λ((γ − μ)/α)     on [μ − α, μ + α],  0 else.   (3.2)

Then π_γ vanishes at the endpoints of its support and

  **I(π_γ) = I(λ) / α² = π² / α²**.                                 (3.3)

This is the textbook compact-support prior in Van Trees 1968 and in the
frequency-estimation literature (sometimes called a raised-cosine or
Hann prior). It is used here because it is explicit, has a closed-form
I(π), and matches a length scale the draft already carries.

### 3.3 Matching α to (M5) and Lemma 1

The draft's resolvability (M5) is T · min_{j≠k} |γ_j − γ_k| ≥ 2πK with
K ≥ 4, i.e. a minimum separation Δ_min = 2πK/T. Lemma 1's local-whitening
neighbourhood is the interval of half-width 2πK/T about γ_j, the same
length scale.

**Choice (P1).** Independent raised-cosine priors (3.2) on each target
ordinate γ_j, centred at a nominal μ_j (the true ordinate in the local
experiment), with

  **α = π K / T**.                                                  (3.4)

Consequences, all algebraic from (M5) and (3.3):

1. **Interiors of adjacent supports are disjoint.** The sum of two
   half-widths is 2α = 2πK/T = Δ_min, so adjacent supports meet at most
   at an endpoint, where π_γ = 0. The set on which two target frequencies
   coincide therefore has π-measure zero, and the FIM singularity that
   (R4) forbids on that set does not enter E_π[I].
2. **Support sits inside the Lemma-1 neighbourhood.** α = πK/T is half
   the Lemma-1 half-width 2πK/T, so I(θ) on supp(π) varies by at most
   the GAP-4 factor already logged (and, being a narrower band, by a
   strictly smaller factor). Variation of I over the prior is not a new
   van Trees error; it is GAP-4.
3. **I(π_γ) in closed form.**

     I(π_γ) = π² / (π K / T)² = **T² / K²**.                        (3.5)

Nuisance priors, product with (P1):

- **Phase φ_j.** Uniform on the circle ℝ/2πℤ. The circle is a compact
  manifold without boundary, so the vanishing-at-boundary condition is
  vacuous; the density is constant and I(π_φ) = 0. (Gill–Levit's
  Euclidean-with-boundary statement does not literally cover the circle;
  the integration-by-parts has no boundary term on a closed manifold.
  Flagged as H-circle, §8, not as a hidden step.)
- **Amplitude A_j.** Raised-cosine on [A_*/2, 3A_*/2] (so A ≥ A_*/2 > 0,
  Gill–Levit-legal). Lemma 2 of the draft has I_{Aω} = I_{Aφ} = 0 up to
  relative O(1/(ω T)), so I(π_A) enters only the A-block of the 3×3 and
  **does not enter the ω Schur complement at leading order** (§4).

The joint prior is the product of these over j = 1, …, d. This is the
prior “on the zero-location parameter” the gap asked for, extended to the
nuisances T1 already treats as unknown.

---

## 4. Insertion into the T1 3×3: the Schur complement

Draft Lemma 2, white-noise convention (2.1), θ = (A, ω, φ), relative
error O(1/(ω T)) suppressed until the end of the display:

  I = S₀^{−1} · [ T/2      0         0    ]
                 [ 0     A² T³/6   A² T²/4 ]
                 [ 0     A² T²/4   A² T/2 ].

A decouples. The (ω, φ) block has determinant (A²/S₀)² T⁴ / 48 and

  [I^{−1}]_{ωω} = 24 S₀ / (A² T³),     I^eff := A² T³ / (24 S₀).   (4.1)

Van Trees adds J^π = diag(I(π_A), I(π_γ), I(π_φ)) with I(π_φ) = 0. The
(ω, φ) block becomes

  I_ωω = A² T³ / (6 S₀) + I(π_γ),
  I_φφ = A² T / (2 S₀),
  I_ωφ = A² T² / (4 S₀).

The new determinant is the old one plus the prior's contribution to I_ωω:

  det = [A² T³/(6 S₀) + I(π_γ)] [A² T/(2 S₀)] − [A² T²/(4 S₀)]²
      = (A²/S₀)² T⁴ / 48  +  I(π_γ) · A² T / (2 S₀).

The (ω, ω) entry of the inverse is I_φφ / det:

  [I^{−1}]_{ωω}
    = [A² T / (2 S₀)]  /  [ (A²/S₀)² T⁴ / 48  +  I(π_γ) A² T / (2 S₀) ]
    = 1 / ( A² T³ / (24 S₀)  +  I(π_γ) )
    = **1 / ( I^eff + I(π_γ) )**.                                   (4.2)

I(π_A) never appears: the A-row/column is already diagonal. The O(1/(ω T))
relative error of Lemma 2, at the operating point ω T ≈ γ_d T ≈ 857, is
≤ 0.0012, which is absorbed in the O(K^{−1}) T1 already carries and is
not added to r_j.

Cross-tone blocks: draft Lemma 3(a) gives relative O(K^{−1}) on
[I^{−1}]_{γ_j γ_j} versus the single-tone value. The same O(K^{−1})
applies to J̄ + J^π because J^π is diagonal in the tone index under the
product prior (P1). GAP-5 (the clean C in that O(K^{−1})) remains OWED;
this note does not re-open it.

Coloured, band-limited noise: replace S₀ by S_ε(γ_j) as in the draft's
Lemma 1 + (B1). Then I^eff_j = A_j² T³ / (24 S_ε(γ_j)). Under (T1-b) and
A_j = 2 a_{γ_j},

  I^eff_j = T³ / (6 log(γ_j / 2π)).                                 (4.3)

(The amplitude cancellation is the draft's Prop. 4.4; van Trees does not
touch it.) Combining (3.5) and (4.3),

  r_j := I(π_γ) / I^eff_j = (T² / K²) · 6 log(γ_j/2π) / T³
       = **6 log(γ_j/2π) / (K² T)**.                                (4.4)

E_π[I^eff] vs I^eff(μ): on the prior support, γ varies by ±α, and
I^eff ∝ 1/log(γ/2π) varies by the relative amount
log(μ/2π)/log((μ−α)/2π) − 1. At j = d, μ = 49.7738, α = πK/T ≈ 0.730,
μ−α = 49.044, log((μ−α)/2π) = 2.0548, ratio 2.06961/2.0548 = 1.0072 —
seven tenths of a percent, dominated by GAP-4's S_ε-flatness (measured
1.23 at γ_d) which already multiplies I through 1/S_ε. Conservative
reading of (2.1): the denominator is ≤ I^eff_max + I(π_γ). Using the
centre value I^eff(μ) understates the denominator by this 0.72 % plus
GAP-4; both are existing, named errors, not van Trees errors. The van
Trees increment is exactly I(π_γ).

---

## 5. The bound, and the leading constants

### 5.1 Theorem T1-VT (Bayes MSE, model N2, prior (P1))

Assume the hypotheses of Theorem T1 (RH, N2 = (M1)–(M5) with (M4′),
(M4″), (W′), K ≥ 4, (B1)), and prior (P1) of §3 including H-circle.
Let γ̂_j be any measurable function of the band-limited record
{y_Ω(t) : t ∈ [0, T]}. Then

  E_π[(γ̂_j − γ_j)²]
    ≥ (1 − O(K^{−1})) / (I^eff_j + I(π_γ))
    = (24 + O(K^{−1})) S_ε(γ_j) / (A_j² T³) · 1/(1 + r_j)
    = (6 + O(K^{−1}))  S_ε(γ_j) / (a_{γ_j}² T³) · 1/(1 + r_j),

with r_j as in (4.4). Substituting (T1-b),

  **√(Bayes MSE_j)
      ≥ √6 · (1 + O(K^{−1})) · (1+r_j)^{−1/2}
        · (log(γ_j/2π))^{1/2} / T^{3/2}.**                          (5.1)

No unbiasedness. The O(K^{−1}) is the draft's (B1) + Lemma 3, unchanged.

### 5.2 Leading constants of the information-cost law: unchanged

T = log X → ∞ with K fixed and γ_d fixed (d fixed). Then r_d = O(T^{−1}) → 0,
so (1+r_d)^{−1/2} = 1 − (1/2) r_d + O(T^{−2}) = 1 + O((log X)^{−1}).
The leading T^{−3/2} coefficient in (5.1) is therefore **√6**, byte-identical
to (T1-c), and the sample-complexity inversion

  T^{3/2} ≥ √6 (log(γ_d/2π))^{1/2} / ε · (1+r_d)^{−1/2}

gives, as ε → 0 (hence T → ∞, r_d → 0),

  **X(ε) ≥ exp( (6 log(γ_d/2π))^{1/3} ε^{−2/3} )**,                 (5.2)

byte-identical to (T1-d). The information-cost law's leading constants
**do not change**. What van Trees costs is a vanishing relative factor,
not a new √6.

(The ledger's phrase “Changes constants” is therefore true at finite T
and false at leading order. Both statements are made, not one of them.)

### 5.3 Finite-T evaluation at the draft's operating point

T = 17.2167, K = 4, K² T = 275.4672.

| j | log(γ_j/2π) | r_j (exact) | r_j UP | (1+r)^{−1/2} DOWN | √6 · that, DOWN |
|---|---|---|---|---|---|
| 1 | 0.81076 | 0.01766 | **0.0177** | **0.991** | **2.427** |
| 10 = d | 2.06961 | 0.04508 | **0.0451** | **0.978** | **2.395** |

Arithmetic: r_d = 6 · 2.06961 / 275.4672 = 12.41766 / 275.4672 = 0.045078,
rounded UP to 0.0451. Then 1 + 0.0451 = 1.0451, √1.0451 = 1.0223,
1/1.0223 = 0.9782, rounded DOWN to 0.978. √6 × 0.978 = 2.3956, rounded
DOWN to 2.395.

Variance form at j = d: 6/(1+r_d) = 5.741, rounded DOWN to **5.741**;
24/(1+r_d) = 22.96, rounded DOWN to **22.96**. (The draft's coloured
band-limited check at Ω = 2Γ was 24 × 0.9943 = 23.86; van Trees at this
T is a comparable, slightly larger, finite-T hit, from a different
source.)

T1-c at d = 10, T = 17.2167, T^{3/2} = 71.44: the draft's frequentist
floor is 0.04933. The Bayes floor is 0.04933 × 0.978 = 0.04824, rounded
DOWN to **0.0482**.

Comparison with T1's O(K^{−1}) = 0.25: r_d = 0.045 is 5.5× smaller.
Declaring the van Trees correction as an additional O(K^{−1}) term would
be valid but crude; (0.1) is the actual order, O(T^{−1}).

Sample-complexity constant at finite T: (6 log(γ_d/2π))^{1/3} = 2.3157
multiplied by (1+r_d)^{−1/3}. (1.0451)^{1/3} = 1.0148,
(1.0451)^{−1/3} = 0.9854, rounded DOWN to 0.985; 2.3157 × 0.985 = 2.281,
rounded DOWN to **2.281**. This finite-T number is *not* the leading
constant of (5.2); as ε → 0 it returns to 2.3157.

### 5.4 What “RMSE” means after dropping unbiasedness

T1 writes RMSE(γ̂_j) = Var(γ̂_j)^{1/2}, which uses unbiasedness to drop
bias². The van Trees left-hand side is Bayes MSE = E[bias² + variance].
Display (5.1) is therefore a lower bound on √(Bayes MSE), which is the
quantity that actually bounds T2's finite-T error. It is *not* a lower
bound on √Var of a biased estimator (that can be smaller, and is).

---

## 6. Sensitivity to the width α (not a second theorem)

The choice α = πK/T is the largest half-width that (M5) alone guarantees
has disjoint support interiors. Two neighbours, recorded so the match is
falsifiable:

- **Lemma-1-full, α = 2πK/T**, I(π) = T²/(4K²), r_d = 0.0113. Stronger
  bound, but adjacent supports overlap by a full (M5) cell, so the
  product prior charges unresolvable pairs. Legal for a *single*
  coordinate (other γ_k treated as known nuisances); not legal as a
  product prior on all of (γ_1, …, γ_d).
- **One Rayleigh bin, α = 2π/T**, I(π) = T²/4, r_d = (3/2) log(γ_d/2π)/T
  = 0.180. Weaker bound (margin 0.920 on RMSE), K_eff ≥ K−2 ≥ 2 on the
  support even if (M5) is saturated. Legal, more conservative, still
  r = O(T^{−1}), leading constants still unchanged.

The leading-order conclusion of §5.2 does not depend on which of these
three O(1/T) widths is chosen, only that α ≍ 1/T (resolution scale), not
α ≍ T^{−3/2} (CR scale). A prior of CR-scale width would give I(π) ≍ T³,
r = Θ(1), and *would* change the leading constant. That prior would
assert, before seeing y, a location accuracy T1 says is the whole
information-cost of the observation; it is not matched to the draft.

---

## 7. What this does not repair

- GAP-4 (flatness of S_ε on the Lemma-1 band): still open; (P1) lives
  inside that band and inherits it.
- GAP-5 (explicit C in Lemma 3(a)): still open; T1-VT carries the same
  O(K^{−1}).
- GAP-17 (Gaussian misspecification of ε): van Trees as written uses the
  *model* Fisher information I^eff of the Gaussian surrogate (M4).
  Propagation of d_K ≤ 0.151 into that I^eff is the companion note
  `T1_GAP17_PROPAGATION.md`.
- Pointwise frequentist coverage at a fixed θ, and minimax (N3).
- The M4′ restriction to y_Ω: unchanged.

---

## 8. Hypotheses and OWED

**H-circle.** Uniform prior on φ_j ∈ ℝ/2πℤ. Van Trees on a closed
manifold (no boundary term). Standard, not in the Euclidean statement of
Gill–Levit Theorem 1. If refused, put a raised-cosine prior on a
fundamental domain [0, 2π] with tiny un-charged cuffs of width η at 0
and 2π; I(π_φ) = O(1) and the ω Schur complement is unchanged at leading
order because I_{ωφ} is already in the 3×3 and I(π_φ) adds to I_φφ,
which *raises* the denominator of [I^{−1}]_{ωω}'s companion and slightly
*strengthens* the ω bound. Direction is safe; the circle is cleaner.

**H-M5-null.** The π-measure-zero set on which adjacent supports touch
is ignored in E_π[I]. If a referee wants a strictly positive separation
on the whole support, replace α by (1−δ)πK/T; r_j picks up (1−δ)^{−2},
still O(T^{−1}).

**OWED-1.** GAP-5: explicit C in the O(K^{−1}) of Lemma 3(a), inherited.
**OWED-2.** E_π[I^eff(A,γ)] vs I^eff(A_*, μ) as a fully expanded two-sided
constant, rather than the 0.72 % logarithmic variation plus GAP-4
pointer of §4. Not needed for the leading-order claim.
**OWED-3.** The O(1/(ω T)) leak of I_{Aω} into the ω Schur complement
after a non-zero I(π_A) is inserted. Boundable by the draft's own
O(1/(ω T)); not expanded.
**OWED-4.** Conversion of the Bayes bound (5.1) into a frequentist bound
holding uniformly for every θ in supp(π), with an explicit constant
(requires a modulus of continuity of I(θ), i.e. a closed GAP-4).
**OWED-5.** Regularity of the mixture score on path space: (R1)–(R4)
were checked by the draft for P_θ, not re-checked for the π-mixture.
Standard under compact support and (R1)–(R4), but not written as a
lemma.
**OWED-6.** Numerical I(π) at the operating point is arithmetic on the
draft's T, K, log(γ/2π); it is not a committed receipt (GAP-8 still
covers the surrounding T1 numerics).
**OWED-7.** Ziv–Zakai bound for the periodogram's threshold region, the
second route named in the GAP-7 ledger. Not this note.

---

## 9. What was not touched

`T1_CRAMER_RAO_DRAFT.md` is not edited. The GAP-7 ledger entry is not
closed by this file (FRONTIER remains until a referee accepts (P1) and
H-circle). Lemma 2, Lemma 3, Prop. 4.4, (T1-b), and the factor 24 are
used as the draft states them.

## FRONTIER VERIFICATION 2026-08-26 (fable) — constants PASS
Independent recomputation at the operating point (K=4, T=17.2167, γ_d=49.773832):
r_d = 6·log(γ_d/2π)/(K²T) = 0.045079 (≤ 0.0451 UP ✓); (1+r)^{-1/2} = 0.97820
(≥ 0.978 DOWN ✓); effective constant √6·(1+r)^{-1/2} = 2.3961 (note's 2.395 is
rounded DOWN, sound for a lower bound ✓); Bound-1 RMSE floor = 0.048253
(note's 0.0482 DOWN ✓). GAP-7 CLOSED: van Trees replaces unbiasedness with a
2.2% constant hit inside the existing O(K⁻¹) slack; OWED-7 (Ziv–Zakai) disclosed.

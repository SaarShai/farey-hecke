# T1 GAP-17 — propagation of d_K ≤ 0.151 into the van Trees bound

**DRAFT (grok lane) 2026-08-26 — UNREFEREED.**

Scope: take the *corrected* Kolmogorov distance from
`T1_GAP17_BERRY_ESSEEN_DRAFT.md`, section **FRONTIER VERIFICATION 2026-08-26**,

  σ(50) = 1.4295·10^{−3},     ρ/σ³ = 0.2692,     **d_K ≤ 0.151**,

and propagate it into the van Trees / Cramér–Rao bound of
`T1_GAP7_VAN_TREES.md`. The headline 0.0135 in §§3–4 of the Berry–Esseen
note is an arithmetic error (factor-5 slip in σ²) and is **not used**.
This note does not modify any other file.

Rounding: error bounds UP, margins DOWN. Every constant is derived or
marked OWED / hypothesis. A fully rigorous chain from d_K to a numerical
factor on the information bound **requires extra hypotheses**; they are
named, not hidden. Chains that can be completed without those hypotheses
are completed, and where they go vacuous at d_K = 0.151 that vacuity is
computed, not papered over.

---

## 0. Headline

d_K ≤ 0.151 at Γ = 50 is **not a small misspecification** in any metric
that controls Fisher information. Three chains are derived:

1. **Gaussian-score class** (periodogram / T2 / Godambe; no extra
   hypothesis beyond the draft's second-order model). The information is
   determined by Cov(ε) = the model S_ε. **d_K does not enter.** The
   bound is the GAP-7 van Trees bound as written:

     √(Bayes MSE_d) ≥ 0.978 · √6 · (log(γ_d/2π))^{1/2} / T^{3/2}.     (0.1)

2. **Full estimator class, additive Le Cam** (H-sym-unimodal only).
   d_K → d_{TV} ≤ 0.302 → |Bayes risk_true − Bayes risk_G| ≤ 2 D² d_{TV}.
   At the GAP-7 prior diameter this subtracts 1.29 from a Bayes floor of
   0.00233 and the lower bound is **negative (vacuous)**.

3. **Full estimator class, multiplicative** (H-score-BE + H-ratio with
   essential infimum m of the score-density ratio against a truncated
   Gaussian). Then

     √(Bayes MSE_d) ≥ √m · 0.978 · √6 · (log(γ_d/2π))^{1/2} / T^{3/2}. (0.2)

   Landau interpolation from d_K to ‖f−φ‖_∞ is **vacuous at 0.151**
   (§5), so d_K alone does **not** produce a strictly positive m. A
   numerical m is not implied by the Berry–Esseen number.

A structural Edgeworth main term, using only the same intensity-smoothed
moments as the Berry–Esseen note, gives excess kurtosis |γ_2| ≤ 0.0930
and a relative FI perturbation γ_2²/6 ≤ 0.00145 — two orders of
magnitude smaller than d_K. That term is **not** a theorem until the
Edgeworth remainder is bounded (OWED-E). It is recorded as the reason
the BE constant 0.151 is a loose envelope, not as a substitute for (0.2).

**Numerical bound that this note will stand behind, with hypotheses
named:** (0.1) for the T2 / Gaussian-score class; (0.2) for the full
class, with m an explicit hypothesis, not a number extracted from 0.151.

---

## 1. Input, and what d_K is the distance between

From the FRONTIER VERIFICATION (and only from there):

  d_K( L(ε/σ), N(0,1) ) ≤ 0.56 × 0.2692 = 0.150752, rounded UP to
  **d_K ≤ 0.151**,

where ε = 2 Σ_{γ>Γ} a_γ cos(γ t + φ_γ) is the *scalar* interference at a
fixed t, under (M1) and the intensity-smoothed third-moment algebra of
the Berry–Esseen note (a_ω = ω^{−2}, Γ = 50). The constant 0.56 is the
Shevtsova (2011) upper bound on the absolute Berry–Esseen constant;
0.4097 (Esseen 1956) is the known lower bound on that constant and is
not used, because using it would tighten d_K and we are bounding an
error UP.

This d_K is **not** automatically:

- the Kolmogorov distance of the *efficient score* for γ_j (a different
  linear combination of the same random phases),
- the total-variation or Hellinger distance of the *path-space* law of
  {ε(t)}_{t∈[0,T]} from the Gaussian process with spectrum S_ε,
- a bound on |I_true − I_G|.

The CR / van Trees information is a quadratic form on path space. Two
reductions are used below and are labelled as such.

**H-score-BE (hypothesis).** The normalised efficient score for γ_j,
after whitening and profiling (A_j, φ_j),

  U := ⟨ε, ∂_γ m⟩_C   /   ‖∂_γ m‖_C ,

satisfies d_K(L(U), N(0,1)) ≤ 0.151. Justification offered, not proved:
U = Σ_γ β_γ · (2 cos(φ_γ+ψ_γ)) is in the same independent-sum class, and
the Lyapunov ratio ‖β‖_3³/‖β‖_2³ is maximised by sparse β and minimised
by equal weights. The pointwise ε(t) has weights a_γ; if the matched
filter does not concentrate onto fewer interferers than that, 0.151 is
conservative. If it *does* concentrate, H-score-BE can fail (OWED-1:
compute ρ_U/σ_U³ for the actual whitened ∂_γ m). All full-class chains
below are chains from d_K(U, N(0,1)), i.e. they assume H-score-BE.

The path-space law is not used as a primitive. Under (M4′) the
observation is band-limited, hence finite-dimensional of dimension
≍ Ω T / π ≈ 548, but a product of 548 marginals each at d_K = 0.151
would make path-space TV accumulate to 1; the coordinates are not
independent (one phase vector). That bound is not attempted (OWED-2).

---

## 2. Direction: Stam, and why the Gaussian number can fail as a lower bound

### 2.1 Scalar Stam inequality (proved)

Let ξ have density f, E[ξ] = 0, E[ξ²] = 1, Fisher information
I(f) := ∫ (f')²/f = E[(s_f)²], s_f := (log f)'. Integration by parts
(boundary terms vanish if x f(x) → 0 at ±∞, which holds for the
Gaussian and for our compactly supported ε):

  E[s_f ξ] = ∫ x f'(x) dx = −1.

Cauchy–Schwarz: 1 = |E[s_f ξ]|² ≤ E[s_f²] E[ξ²] = I(f). Equality iff
s_f = c ξ iff f is Gaussian. Thus

  **I(f) ≥ 1 = I(φ), equality iff f = φ.**                          (2.1)

*Citation.* Stam, A. J. (1959), “Some inequalities satisfied by the
quantities of information of Fisher and Shannon”, *Information and
Control* **2**, 101–112. The one-line proof above is the standard
projection argument and does not depend on the rest of Stam's paper.

The same identity gives the excess as an L² distance of scores: with
s_φ = −ξ for N(0,1),

  I(f) − 1 = E_f[(s_f − s_φ)²] ≥ 0.                                 (2.2)

### 2.2 Consequence for Cramér–Rao / van Trees

In the local experiment U = u + ξ, u = √I^eff (γ − μ), the Gaussian
model has I_G = 1. The true model has I(f) ≥ 1. Van Trees under the
true law is

  Bayes MSE_u ≥ 1 / (I(f) + I(π_u)) ≤ 1 / (1 + I(π_u)).             (2.3)

The Gaussian van Trees number 1/(1+I(π_u)) is **larger** than the true
van Trees number. A larger “lower bound” is not a lower bound: any
estimator that exploits non-Gaussianity of ξ (bounded support, kurtosis,
higher-order spectra) may achieve a Bayes MSE between 1/(I(f)+I(π_u))
and 1/(1+I(π_u)). **The Gaussian CR / van Trees display is therefore not
automatically valid for the full estimator class.** It is valid as a
lower bound only if one either (i) upper-bounds I(f), or (ii) restricts
the estimator class so that I(f) never enters.

The Berry–Esseen note's §4 asserted the opposite direction (“true FI is
strictly less than Gaussian FI”). That is **false** for location
families of fixed variance, by (2.1). It is withdrawn; the rest of this
note uses Stam's direction.

### 2.3 Additive signal-in-noise on path space

The observation is y = m(θ) + ε, not a scalar location family. For
additive noise with a **fixed covariance** C, among all noise laws, the
Gaussian maximises entropy and, in finite dimension with a location
(mean) parameter, minimises the Fisher information of that mean: the
score of the Gaussian is C^{−1}(y−m), linear, and the same
Cauchy–Schwarz / projection argument as §2.1 gives

  I_true(θ) ⪰ (Dm)ᵀ C^{−1} (Dm) = I_G(θ)                            (2.4)

for the mean-parameter information, provided the true score exists
(finite I). This is the natural extension of Stam; a fully infinite-
dimensional Gaussian-process statement needs the Cameron–Martin
calculus already used by the draft in (R1) and is not re-proved here
(OWED-3). Under (M4′) one is in finite dimension, and (2.4) applies.
Direction: same as (2.3). To turn I_G into a valid MSE lower bound for
the full class, I_true must be upper-bounded, not lower-bounded.

---

## 3. Chain 0 — Gaussian-score class: d_K does not enter

T2 is a windowed periodogram plus quadratic refinement. Its local
linearisation is a function of the Gaussian score
s_G = ⟨y − m, ∂m⟩_C, i.e. of **linear** functionals of ε. Godambe's
information for an estimating equation ψ(y,θ) = 0 is

  J := E[∂_θ ψ],     K := Var(ψ),     sandwich  J^{−1} K J^{−T}.

Take ψ = s_G. Because E[ε] = 0 and Cov(ε) is the model C (Prop. 4.4,
second-order, independent of Gaussianity),

  E[s_G] = 0,    J = K = I_G.

The sandwich equals I_G^{−1}. *Citation.* Godambe, V. P. (1960), “An
optimum property of regular maximum likelihood estimation”, *Ann. Math.
Statist.* **31**, 1208–1211; White, H. (1982), “Maximum likelihood
estimation of misspecified models”, *Econometrica* **50**, 1–25, for the
sandwich under misspecification. Here the mean and covariance are
correctly specified, so the sandwich collapses to the Gaussian inverse
information.

**Theorem (score class).** For any estimator that is a function of the
Gaussian score of the band-limited record (in particular T2, locally),
the van Trees bound of `T1_GAP7_VAN_TREES.md` applies with I^eff = I_G
and **no d_K factor**:

  E_π[(γ̂_d − γ_d)²] ≥ 1 / (I^eff_d + T²/K²)
    = [6 log(γ_d/2π) / T³] / (1 + r_d),                             (3.1)

r_d ≤ 0.0451, (1+r_d)^{−1/2} ≥ 0.978, hence (0.1). Hypotheses: those of
T1-VT (including (P1)), and that the estimator's local estimating
equation is s_G (true of T2's quadratic refinement; not true of an
estimator that uses e.g. the known bounded support of ε).

This is the bound that GAP-7 was asked to supply for T2. GAP-17 does not
degrade it.

---

## 4. Chain A — d_K → TV → additive Le Cam: derived, vacuous

### 4.1 Kolmogorov to total variation under symmetry + unimodality

Always d_K ≤ d_{TV}. The reverse needs structure.

**H-sym-unimodal (hypothesis).** The density f of U (and φ) is even and
unimodal at 0. Evenness is a theorem: each summand 2 a_γ cos(φ_γ+ψ) is
symmetric and the sum is symmetric. Unimodality is not: a finite
trigonometric polynomial can be multimodal. It is expected at Γ = 50
under the CLT, and is not proved (OWED-4: unimodality of the law of U).

**Lemma.** If F and Φ are cdfs of even unimodal densities, then
d_{TV}(F, Φ) ≤ 2 d_K.

*Proof.* Let Δ := F − Φ. Then Δ is odd, Δ(0) = 0, Δ(±∞) = 0, |Δ| ≤ d_K.
Even unimodal densities have concave cdfs on [0, ∞), so Δ|_{[0,∞)} has
at most one turning point. Total variation of Δ on [0, ∞) is therefore
at most 2 d_K (up to the unique extremum of height ≤ d_K and back to 0).
By oddness, TV_ℝ(Δ) ≤ 4 d_K. And d_{TV} = (1/2) TV(Δ) ≤ 2 d_K. ∎

Thus, rounding the error UP,

  **d_{TV}(L(U), N(0,1)) ≤ 2 × 0.151 = 0.302.**                     (4.1)

Location families are TV-shift-invariant, so this is uniform in the
local parameter u.

### 4.2 Bounded-loss comparison

Let Q_u (resp. P_u) be N(u, 1) (resp. u + L(U)). For a loss ℓ with
0 ≤ ℓ ≤ L,

  |E_{P_u} ℓ − E_{Q_u} ℓ| ≤ L · 2 d_{TV} ≤ 0.604 L,                  (4.2)

because |∫ ℓ d(P−Q)| ≤ ‖ℓ‖_∞ ∫ |d(P−Q)| = 2 d_{TV} ‖ℓ‖_∞.
*Citation.* Le Cam, L. (1986), *Asymptotic Methods in Statistical
Decision Theory*, Springer, the elementary property of TV; equivalently
the definition of the Le Cam deficiency of two simple experiments.

Restrict estimators to take values in the GAP-7 prior support
(Bayes-optimal for quadratic loss under a compactly supported prior).
Then |γ̂ − γ| ≤ 2α with α = πK/T, so ℓ = (γ̂−γ)² ≤ D², D := 2α.

At the operating point: α = 4π / 17.2167 = 0.7300, D = 1.460,
D² = 2.131. Then 2 D² d_{TV} ≤ 2 × 2.131 × 0.302 = **1.287** (UP).

GAP-7 Bayes floor: I^eff_d + I(π) = T³/(6 log(γ_d/2π)) + T²/K²
= 410.97 + 18.53 = 429.50, 1/429.50 = **0.002329**.

  E_P[ℓ] ≥ E_Q[ℓ] − 1.287 ≥ 0.002329 − 1.287 < 0.

**The additive chain is vacuous**, by a factor ≃ 550. This is a derived
statement, not a failure to estimate a constant. Optimising the prior
width does not save it: writing β = α², the net floor is
β/(I^eff β + π²) − 8 β d_{TV}, which is positive only if
I^eff β + π² < 1/(8 d_{TV}) = 0.414, but π² = 9.87 > 0.414 already.
**No** compactly supported raised-cosine prior makes Chain A non-vacuous
at d_K = 0.151.

(The same obstruction hits any additive TV comparison of unbounded or
prior-diameter-bounded quadratic loss at this d_K. Truncating the loss
at the CR scale (∼ 0.05)² instead of D² would make the subtracted term
small, but then van Trees on the *truncated* loss is a different
inequality and is OWED-5.)

---

## 5. Chain B — d_K → ‖f−φ‖_∞ via Landau: derived, vacuous

To get a multiplicative factor one wants inf (f/φ). A route without
naming that inf as a hypothesis is: bound ‖f−φ‖_∞ from d_K plus a
Lipschitz bound on the densities, then f ≥ φ − ‖f−φ‖_∞.

**Landau's inequality on ℝ.** If g ∈ C²(ℝ), then
‖g'‖_∞² ≤ 4 ‖g‖_∞ ‖g''‖_∞. *Citation.* Landau, E. (1913), “Ungleichungen
für zweimal differenzierbare Funktionen”. (The constant 4 is the
classical one; using a smaller sharp constant would tighten, and we are
bounding an error UP.)

Apply to g = F − Φ: ‖g‖_∞ ≤ d_K ≤ 0.151, g' = f − φ, g'' = f' − φ'.
**H-Lip (hypothesis).** |f'| ≤ L and |φ'| ≤ L, so ‖g''‖_∞ ≤ 2L. Then

  ‖f − φ‖_∞ ≤ 2 √(d_K · 2L) = 2 √(2 L d_K).                         (5.1)

For the standard normal, |φ'(x)| = |x| φ(x) attains
L_φ = φ(1) = 1/√(2π e) = 0.24197. If one takes L = L_φ as a Gaussian
proxy (H-Lip with L = L_φ, not implied by d_K),

  ‖f−φ‖_∞ ≤ 2 √(2 × 0.24197 × 0.151) = 2 √0.07307 = 0.541.          (5.2)

The Gaussian mode is φ(0) = 1/√(2π) = 0.3989. The bound 0.541 > 0.3989
does not even force f(0) > 0. **Chain B is vacuous at the mode**, hence
vacuous as a bound on inf f/φ. No numerical m comes out of d_K + Landau
at this d_K.

(The same conclusion with any L ≳ 0.13, since 2√(2 L · 0.151) < 0.3989
forces L < 0.132, strictly below L_φ. A density whose derivative is
smaller than the Gaussian's everywhere is not a perturbation we can
assume.)

---

## 6. Chain C — multiplicative transfer under bounded density ratio

This is the chain that gives a non-vacuous full-class bound, at the
price of an explicit extra hypothesis.

### 6.1 Why ess inf dP/dQ on ℝ is zero (not hidden)

ε is a sum of bounded random variables, so U is supported in
[−R_*, R_*]. Intensity-smoothed, with the Berry–Esseen note's a_ω = ω^{−2},

  Σ_{γ>Γ} a_γ ≈ ∫_Γ^∞ ω^{−2} log(ω/2π) / (2π) dω
             = (log(Γ/2π) + 1) / (2π Γ).

At Γ = 50, log(50/2π) = 2.07414 (this is log(Γ/2π), not the verification
note's earlier 2.0696 which was log(γ_d/2π); the verification's σ² used
the correct Γ-value). Then Σ a ≈ 3.07414 / (100π) = 0.009785,
2 Σ a ≈ 0.01957, R_* ≈ 0.01957 / 1.4295·10^{−3} = 13.69, rounded UP to
**R_* ≤ 14**.

N(0,1) is not supported in [−14, 14], so dΦ/dP = ∞ on the Gaussian
tails and ess inf (f/φ) = 0 on ℝ. A multiplicative comparison of P to
the *untruncated* Gaussian is vacuous for the same support reason. One
must compare to a reference that is equivalent to P.

### 6.2 Truncated-Gaussian reference

Let φ^R be the N(0,1) density truncated to [−R, R] and renormalised, with
R := R_* = 14. Then Φ^R ∼ P (both charge [−14, 14] only). The
renormalisation is 1 / (2Φ(14)−1). Mills: 1−Φ(14) ≤ φ(14)/14
= e^{−98}/(14 √(2π)) which is smaller than 10^{−43}. So φ^R = φ / (1 − δ)
with δ < 10^{−42}, and I(φ^R) = 1 + O(δ) (the truncated-Gaussian FI
differs from 1 by a boundary term of size R φ(R) / Φ(R) = O(10^{−42})).
For every numerical purpose of this note, I(φ^R) = 1 and van Trees under
Φ^R equals van Trees under Φ. This replacement is not a hypothesis; it
is a 10^{−42} error, rounded into nothing at the scale of 0.151.

### 6.3 The multiplicative inequality

**H-ratio (hypothesis).** There exist 0 < m ≤ M < ∞ such that

  m ≤ f(u) / φ^R(u) ≤ M     for Lebesgue-almost every u ∈ [−R, R].  (6.1)

Then for every nonnegative measurable ℓ,

  m E_{Φ^R}[ℓ] ≤ E_P[ℓ] ≤ M E_{Φ^R}[ℓ],                             (6.2)

because E_P[ℓ] = E_{Φ^R}[ℓ · (f/φ^R)]. Taking ℓ = (γ̂ − γ)² and the
van Trees lower bound on the Gaussian (truncated) Bayes risk,

  **E_P[(γ̂ − γ)²] ≥ m / (I^eff + I(π_γ)).**                         (6.3)

*This is the rigorous multiplicative perturbation.* It is not O(d_K);
it is the factor m, which d_K does not determine (§5). Combining with
GAP-7's (1+r_d)^{−1/2} ≥ 0.978,

  √(Bayes MSE_d) ≥ √m · 0.978 · √6 · (log(γ_d/2π))^{1/2} / T^{3/2},  (6.4)

which is (0.2). Rounding √m DOWN is the user's job once m is supplied;
this note will not invent m.

**What H-ratio actually says, in the draft's language.** A bounded
density ratio on the 1-D score is a quantitative form of “the Lindeberg
CLT has produced a density, not just a cdf, close to Gaussian on the
whole support.” Compact support plus a C¹ density (true once three or
more arcsine-type laws have been convolved) implies M < ∞ and, provided
f is bounded below on [−R, R] — which fails near ±R_* where f vanishes
as a power of (R_* − |u|) — m = 0 still, unless the infimum is taken on
a strictly smaller interval.

**H-ratio-bulk (stricter, usable).** For a chosen R_0 < R_* (e.g. R_0 = 4),
m_0 := inf_{|u|≤R_0} f(u)/φ(u) > 0, and the tail contribution to the
Bayes risk under P is controlled separately. The tail mass under P is
≤ d_K + (1−Φ(R_0)) ≤ 0.151 + 3.17·10^{−5} = 0.1511 at R_0 = 4, which is
not small: Kolmogorov does not give Gaussian tails, only Gaussian tails
plus d_K. A tail-truncated multiplicative bound therefore still loses a
relative 0.151 unless one uses the *actual* compact support and a
density lower bound on [−R_0, R_0] from smoothness (OWED-6).

H-ratio is the extra hypothesis the task description named (“e.g. bounded
density ratio”). It is required. It is not implied by d_K ≤ 0.151.

---

## 7. Chain D — structural kurtosis, Edgeworth main term (remainder OWED)

This chain does not start from d_K. It starts from the same
intensity-smoothed moment algebra the Berry–Esseen note used, and shows
that the *actual* information perturbation, if an Edgeworth expansion
holds, is O(10^{−3}) not O(10^{−1}). It is included so that 0.151 is not
mistaken for the size of the FI error. The remainder constant is OWED;
without it this is not a theorem.

### 7.1 Fourth cumulant, derived

Each summand X_γ = 2 a_γ cos Φ_γ, Φ_γ uniform. E[cos⁴] = 3/8, so
E[X_γ⁴] = 16 a_γ⁴ · 3/8 = 6 a_γ⁴. E[X_γ²] = 2 a_γ². The fourth cumulant
is

  κ_4(X_γ) = E[X⁴] − 3 (E[X²])² = 6 a⁴ − 12 a⁴ = −6 a_γ⁴.

Independence: κ_4(ε) = −6 Σ_{γ>Γ} a_γ⁴. Excess kurtosis of the
normalised sum:

  γ_2 := κ_4(ε) / σ⁴ = −6 Σ a_γ⁴ / σ⁴.                              (7.1)

Intensity-smoothed, a_ω = ω^{−2} (same convention as the BE note):

  Σ a⁴ ≈ ∫_Γ^∞ ω^{−8} log(ω/2π) / (2π) dω.

The integral: ∫_Γ^∞ ω^{−8} log(ω/2π) dω = Γ^{−7}/7 (log(Γ/2π) + 1/7),
because ∫_1^∞ u^{−8} du = 1/7 and ∫_1^∞ u^{−8} log u du = 1/49. Thus

  Σ a⁴ ≈ Γ^{−7} (L + 1/7) / (14 π),     L := log(Γ/2π).

The BE note's σ² = Γ^{−3}(L+1/3)/(3π) (FRONTIER VERIFICATION:
2.0435·10^{−6}), so σ⁴ = Γ^{−6} (L+1/3)² / (9 π²) and

  6 Σ a⁴ / σ⁴
    = (27 π / 7) · Γ^{−1} · (L + 1/7) / (L + 1/3)².                (7.2)

At Γ = 50, L = 2.07414, 27π/7 = 12.117, (L+1/7)/(L+1/3)² = 0.3825,
(7.2) = 12.117 × 0.02 × 0.3825 = 0.0927. Rounding the error UP,

  **|γ_2| ≤ 0.0930.**                                                (7.3)

(Sign: γ_2 < 0, platykurtic, as expected for bounded summands.)

### 7.2 Edgeworth main term for the density and for I(f)

Symmetry kills the skewness (He_3) term. The Edgeworth density to this
order is

  f(x) = φ(x) [ 1 + (γ_2 / 24) He_4(x) ] + r(x),                    (7.4)

He_4(x) = x⁴ − 6 x² + 3. *Citation.* Feller, W. (1971), *An Introduction
to Probability Theory and Its Applications*, Vol. II, Ch. XVI; Petrov,
V. V., *Limit Theorems of Probability Theory*, the independent non-iid
Edgeworth expansion. The remainder r is O(Lyapunov_6) under additional
smoothness. Lyapunov_6 := Σ E|X_γ|⁶ / σ⁶ is computed in OWED-E and equals
**0.0151** at Γ = 50 (intensity-smoothed, rounded UP); the implied
constant in r = O(Lyapunov_6) is **not** derived (OWED-E). A constant of
order 10 would make the remainder comparable to d_K, so the smallness of
the *main* term 0.00145 is not a licence to drop the remainder.

On [−2, 2], |He_4| attains 6 at |x| = √3. The relative main term is at
most |γ_2| · 6 / 24 = 0.0930 × 0.25 = 0.0233 (UP). That would give
m_bulk ≥ 1 − 0.0233 − ‖r/φ‖_∞ on [−2, 2], which is a number only after
OWED-E.

For Fisher information: (log f)' = −x + (γ_2/6) He_3(x) + O(γ_2², r),
He_3(x) = x³ − 3x, and E_φ[He_3²] = 6, E_φ[x He_3] = 0, so the
Gaussian-measure calculation is

  I(f) = 1 + γ_2² / 6 + O(γ_2² from changing measure) + remainder.   (7.5)

|γ_2|² / 6 ≤ 0.0930² / 6 = 0.001442, rounded UP to **0.00145**. If the
O(γ_2²) and remainder were hypothetically absorbed into the same 0.00145
(they are not: that absorption is OWED-E), one would have I(f) ≤ 1.0029
and a full-class RMSE factor 1/√I(f) ≥ 0.9985, negligible against
GAP-7's 0.978.

**Status of Chain D.** The number |γ_2| ≤ 0.0930 is derived, by the same
rules as the BE note's ρ_p. The passage |γ_2| → |I(f)−1| ≤ 0.00145 is
the Edgeworth *main term* and is **not a theorem** of this note. It is
the quantitative reason d_K ≤ 0.151 (a worst-case Berry–Esseen envelope
with C = 0.56) overstates the likely FI perturbation by two orders of
magnitude. It does not license replacing m in (6.4) by 0.998.

---

## 8. The perturbed bound, assembled

Let B_G := 6 log(γ_d/2π) / T³ and r_d ≤ 0.0451. Variance margin
(1+r_d)^{−1} = 1/1.0451 = 0.95685, rounded DOWN to **0.956**. RMSE margin
(1+r_d)^{−1/2} ≥ **0.978** as in GAP-7 (0.978² = 0.9565, consistent with
the variance rounding to three places).

**Bound 1 (score class; T2). No extra GAP-17 hypothesis.**

  E[(γ̂_d − γ_d)²] ≥ 0.956 · B_G = 0.956 · 6 log(γ_d/2π) / T³,
  √(Bayes MSE_d) ≥ 0.978 · √6 · (log(γ_d/2π))^{1/2} / T^{3/2}
                 ≥ **2.395 · (log(γ_d/2π))^{1/2} / T^{3/2}.**        (8.1)

At the operating point T = 17.2167 this is **0.0482** (GAP-7 §5.3),
against T1's unbiased 0.04933. d_K does not appear.

**Bound 2 (full class; H-score-BE + H-ratio with infimum m).**

  E[(γ̂_d − γ_d)²] ≥ m · 0.956 · B_G,
  √(Bayes MSE_d) ≥ √m · 2.395 · (log(γ_d/2π))^{1/2} / T^{3/2}.      (8.2)

m is a hypothesis, not a number. Landau and additive Le Cam do not
supply one at d_K = 0.151. If a later computation establishes H-ratio
with a specific m_0, substitute √m_0 (rounded DOWN) into (8.2).

**Bound 3 (full class; additive TV; H-sym-unimodal only).** Vacuous
(§4.2). Not displayed as a bound.

**Not claimed.** Any statement of the form “I_G is perturbed by O(d_K)”
or “the CR bound loosens by 15 %”. d_K = 0.151 does not imply a 15 %
move in I: Chain D's main term is 0.14 %, and Chain C refuses to invent
the rest.

---

## 9. Hypotheses and OWED

**H-score-BE.** d_K(L(U), N(0,1)) ≤ 0.151 for the efficient score U, not
just for ε(t). Needed by Chains A–C. False if the matched filter
sparsifies the interferer weights enough that ρ_U/σ_U³ > 0.2692.

**H-sym-unimodal.** f even and unimodal. Evenness proved; unimodality
not. Needed by Chain A (TV ≤ 2 d_K) only.

**H-Lip.** |f'| ≤ L. Needed by Chain B, which is vacuous at L = L_φ
anyway.

**H-ratio.** m ≤ f/φ^R ≤ M on [−R, R]. Needed by Chain C / Bound 2. Not
implied by d_K ≤ 0.151 (Chain B). The task's “e.g. bounded density
ratio” is exactly this. Near ±R_* one has f → 0 and φ^R > 0, so the
unrestricted infimum on the whole support is 0; a usable m requires
either a bulk restriction (H-ratio-bulk) or a strictly positive lower
bound on f up to the edge, which a power-law edge does not give.

**H-circle, (P1), T1 hypotheses.** Inherited from
`T1_GAP7_VAN_TREES.md` and the T1 draft.

**OWED-1.** Compute ρ_U/σ_U³ for U = ⟨ε, ∂_γ m⟩_C / ‖∂_γ m‖_C under
(W′) at Γ = 50, to prove or refute H-score-BE. Aristotle-able once the
filter is written.
**OWED-2.** Path-space distance of {ε(t)} from the Gaussian process with
spectrum S_ε, in a metric that controls the Cameron–Martin information
(e.g. Hellinger on the (M4′) band). Not attempted; 548-dimensional
product-TV is the wrong bound.
**OWED-3.** Infinite-dimensional Stam / I_true ⪰ I_G for a Gaussian
process with given covariance, in the draft's RKHS. Finite-dimensional
(M4′) case is the projection argument of §2.3.
**OWED-4.** Unimodality of L(U) (to close H-sym-unimodal).
**OWED-5.** van Trees for truncated quadratic loss, the only remaining
route that could salvage an additive TV comparison at this d_K.
**OWED-6.** A density lower bound on [−R_0, R_0] from the characteristic
function ψ(t) = ∏_{γ>Γ} J_0(2 a_γ t / σ), which would convert H-ratio-bulk
into a theorem. Inversion ‖f−φ‖_∞ ≤ (1/2π) ∫ |ψ(t) − e^{−t²/2}| dt is
the identity; the tail of that integral is not bounded in this note.
**OWED-E.** Edgeworth remainder in (7.4)–(7.5), including the constant
in r = O(Lyapunov_6). Lyapunov_6 itself is derived, same smoothing as
ρ_p: E[|cos|⁶] = 5/16 (Wallis), E[|X_γ|⁶] = 64 a_γ⁶ · 5/16 = 20 a_γ⁶,
Σ a⁶ ≈ ∫_Γ^∞ ω^{−12} log(ω/2π)/(2π) dω = Γ^{−11}(L+1/11)/(22π),
σ⁶ = [σ²]³ = Γ^{−9}(L+1/3)³/(27 π³), hence
Lyapunov_6 = (10/11) · 27 π² · Γ^{−2} · (L+1/11)/(L+1/3)³
= 242.25 · Γ^{−2} · 0.1552 = 0.01504 at Γ = 50, rounded UP to **0.0151**.
The implied constant in the remainder theorem is not derived. Until it
is, Chain D does not produce a legal m; a constant ≳ 10 would make the
remainder as large as d_K itself.
**OWED-7.** Sensitivity of |γ_2| to replacing a_ω = ω^{−2} by the exact
|M_W(½+iω)| = ((¼+ω²)(9/4+ω²))^{−1/2}. At Γ = 50 the two agree to
relative O(Γ^{−2}) = 4·10^{−4}; not expanded.
**OWED-8.** GAP-10's truncation quantile q enters the BE constant through
max |X_γ|; the BE note already flags this. Propagation of q into m or
into ρ/σ³ is not redone here. (The GAP-10 sweep showed the *mean-field*
I^eff is q-invariant; the Berry–Esseen numerator is not.)

---

## 10. What was not touched

`T1_CRAMER_RAO_DRAFT.md`, `T1_GAP17_BERRY_ESSEEN_DRAFT.md`, and
`T1_GAP7_VAN_TREES.md` are not edited. The 0.0135 figure in the
Berry–Esseen note is not used. No leading constant of (T1-c) or (T1-d)
is altered by this propagation beyond the GAP-7 factor 0.978 already
computed for van Trees at finite T, and, for the full class only, the
undetermined √m of H-ratio.

## FRONTIER VERIFICATION 2026-08-26 (fable) — structure PASS, direction correction banked
Key correction accepted: by Stam, the Gaussian MINIMIZES Fisher information at
fixed variance, so I(f) ≥ I_G — the Berry–Esseen note's §4 claim ("true Fisher
information strictly less than Gaussian") had the direction WRONG; the Gaussian
CR number is not automatically a valid floor for the full noise class. Standing:
the T1 headline bound holds for the Gaussian-score/Godambe estimator class
(Bound 1, RMSE ≥ 0.0482 at the operating point, verified above in GAP-7); the
full-class multiplicative factor √m stays an explicit hypothesis (H-ratio),
since d_K ≤ 0.151 is too large for the Landau interpolation to give m > 0.
GAP-17 CLOSED-AT-CLASS-RESTRICTED standing: quantifier "over the Gaussian-score
class" is MANDATORY in the T1 law statement; Edgeworth remainder OWED.

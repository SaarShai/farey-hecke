# T1 — Cramér–Rao lower bound in the frozen model N2

Draft v3, 2026-08-15. Lane T (T-opus). Status: RE-DERIVED under owner-approved
amendments A1 **and A2**; not adversarially reviewed, not machine-verified.
Ticket: `plans/wayfinder/rh-goals/tickets/sample-complexity-t1.md`.
Model authority: `research_notes/rh_goals_2026-08-14/G1_MODEL_SPEC.md` (v0,
FROZEN 2026-08-14, **+ AMENDMENT A1** (clause M4′, band limit) **+ AMENDMENT
A2** (clause W′, window replacement; clause M4″, spectral floor), both
2026-08-15).

**Changes v2 → v3.** Amendment A2 replaces the Gaussian window
W(x) = e^{−x²} by the order-1 Riesz (Fejér) window W(x) = (1−x)_+,
M_W(s) = 1/(s(s+1)). Consequences, all re-derived here rather than asserted:
(i) §1.1's observable is restated under (W′) — it becomes the Cesàro mean
(1/N)Σ_{k<N}M(k), R₀ = −2 survives, one new polar term 12/N appears.
(ii) **Prop. 4.4 and the amplitude cancellation survive untouched** — they
never used the Gaussian form — so **the headline constants are unchanged**
(§0, §5.1). (iii) The factor 24 is re-verified numerically a third time, now
band-limited *with the model S_ε of (W′)* rather than white (§4.0(c)).
(iv) **GAP-3 CLOSED**: the Lindeberg ratio now vanishes, measured (§3 (R6)).
(v) **GAP-14 CLOSED**: (B1) is measured directly as λ_max(I_N^{−1}I_R) and
**holds** at the approved cut Ω = 2Γ (§4.0(d)). (vi) **GAP-15 CLOSED** by
clause (M4″) with a sensitivity measurement (§4.0(e)). (vii) GAP-4 reduced
from a factor 98 to a factor 1.23–2.03, stated as an explicit two-sided
constant, but **not closed**. (viii) Two new gaps that A2 *creates* and that
are logged rather than absorbed: **GAP-16** (the VERIFIED explicit-formula
import no longer applies to the new window) and **GAP-17** (finite-Γ
Berry–Esseen rate behind the now-valid Lindeberg condition).

**Honest label carried throughout:** this is a Cramér–Rao bound *in model N2*.
N2 contains stochastic hypotheses about the zeros that are not theorems. The
result is a statement about the model, not an unconditional statement about
ζ. G1_MODEL_SPEC §3 requires exactly this labelling. **A2 does not change
that label, and does not change a single displayed constant** — see the
self-serving audit at G1_MODEL_SPEC §A2.6, restated in §7.4 below.

---

## 0. Headline (for the reader in a hurry)

In model N2 the ζ′-amplitudes **cancel** between the signal and the
interference noise. The bound reduces to

  max_j RMSE(γ̂_j) ≥ √6 · (log(γ_d/2π))^{1/2} / (log X)^{3/2},

with no dependence on a_γ, hence no dependence on 1/|ζ′(ρ)|. This
substantially defuses falsification gate G-a (the heavy-tail worry of
G1_MODEL_SPEC §3/§5): the heavy tail enters the *validity* of the Gaussian
approximation, but not the leading constant. The sample-complexity corollary
is X(ε) ≥ exp( (6 log(γ_d/2π))^{1/3} · ε^{-2/3} ).

**This display is byte-identical to v1 and v2.** Amendment A2 changed the
window and therefore the observable, the amplitudes a_γ, and the noise
spectrum S_ε — and changed *nothing* here, because Prop. 4.4 gives
S_ε(γ)/a_γ² = log(γ/2π) with the window cancelling identically. A2 bought
validity, not size.

**One caveat the reader must carry from here (v2 had two; A2 discharged one).**
The bound is for the *band-limited* estimator class of spec clause M4′
(amendment A1) — it is **not** a bound on estimators that see the
unrestricted record, and that restriction does not transfer upward. The
second v2 caveat — that the band-edge leakage hypothesis (B1) *failed by ~29
orders of magnitude* at the approved cut under the frozen Gaussian window —
is **discharged by amendment A2**: under the order-1 Riesz window (B1) is
measured to hold at Ω = 2Γ (λ_max(I_N^{−1}I_R) = 0.0858 ≤ 1/K = 0.25 at
γ_d), and the band-limited [I^{−1}]_{ωω} is **0.9943** of the local 24-value
instead of 7.7·10^{−30} of it (§4.0(d)). The displayed constants are now the
constants of the actual band-limited problem at the approved cut, not merely
of a local surrogate.

---

## 1. The frozen model, restated

Restated from `G1_MODEL_SPEC.md` §1–§3. Where I paraphrase, the spec's own
wording is quoted; where I add anything the spec does not say, it is marked
**[ADDED]** and appears again in §6.

### 1.1 Observable (spec §1 as amended by A2 clause W′)

**Under amendment A2** the window is W(x) = (1−x)_+ with M_W(s) = 1/(s(s+1))
(G1_MODEL_SPEC §A2.1). For t = log N,

  y(t) := e^{−t/2} · [ Σ_{n≤N} μ(n)(1 − n/N) − R₀ − R_{−1}(N) − R_triv(N) ]
        = 2 Σ_{γ>0} a_γ cos(γ t + φ_γ) + ε(t),   N = e^t,           (1.1)

  a_γ = | M_W(½+iγ) / ζ′(½+iγ) | = 1 / ( |½+iγ| · |3/2+iγ| · |ζ′(½+iγ)| ),
  φ_γ = arg( M_W(½+iγ)/ζ′(½+iγ) ),   R₀ = −2,  R_{−1}(N) = 12/N,

R_triv(N) = Σ_{n≥1} N^{−2n}/((−2n)(1−2n)ζ′(−2n)). Three differences from the
frozen v0 display, all from §A2.1: the arithmetic side is now the *finite*
order-1 Riesz (Cesàro) mean Σ_{n≤N}μ(n)(1−n/N) = (1/N)Σ_{0≤k<N}M(k); R₀ = −2
is unchanged (the s = 0 residue of M_W is W(0) = 1 for either window); and
M_W's new pole at s = −1 contributes the explicit term R_{−1}(N) = 12/N,
which the Gaussian did not have. Under RH, (1.1) is *exactly* a multi-tone
line spectrum in t whose frequencies are the zero ordinates — the form spec
§1 froze, preserved verbatim.

**What ε(t) now is, and what is owed.** For the Gaussian window the import
`research_notes/imported_farey_now/Smoothed_Dwf_explicit_formula_VERIFIED.md`
gave ε = E_A with |E_A(N)| ≤ C_{A,W}N^{−A} for every A under H1–H3. That
artifact is **for the Gaussian window and no longer applies** (§A2.5.1).
Under (W′) the arithmetic side is exact and finite, the zero sum converges
absolutely given J_{−1}(T) = O(T) (§A2.1.4), and ε is the contour-shift
remainder, which is classical in form for an order-1 Riesz mean but **has not
been re-derived or re-verified in this repo**. This is **GAP-16**, a debt A2
creates. Everything below is the *estimation-theoretic* content of T1 and is
independent of GAP-16 except through the claim that (1.1) holds with ε
negligible on [0,T].

Standing assumption **(RH)**: all nontrivial zeros are ½+iγ, γ ∈ ℝ. The spec
freezes the line-spectrum form, which presupposes RH; T3 is where RH failure
is treated.

### 1.2 Resources (spec §2)

- Arithmetic range X: y(t) needs μ(n) for n ≲ X = e^T. The observation window
  in t is [0, T], **T = log X**. This is the fundamental resource.
- Sample count n_s on the window and per-sample precision — "cheap relative
  to X". We therefore take the *continuous-observation* limit on [0,T],
  which is the information-theoretically strongest (most favourable to the
  estimator) reading and hence gives a valid lower bound for any n_s. See
  Lemma 3 for the discrete-to-continuous statement.

### 1.3 Noise model N2 (spec §3, PRIMARY for T1)

Estimate the d lowest zeros γ_1 < … < γ_d. Fix a cut Γ with γ_d < Γ < γ_{d+1}.
Zeros above Γ are treated as a stochastic interference process:

- zero density near height γ is log(γ/2π)/(2π) per unit ordinate;
- (for constants) GUE pair correlation;
- amplitudes a_γ from the ζ′ empirical blocks (lane_a data);
- the interference sum is "an almost-periodic Gaussian-approximable process
  with computable spectral density S_ε(ω) near ω = γ_j";
- Fisher information / CR bound computed against it;
- "All probabilistic assumptions STATED as model hypotheses."

Spec §3 also carries forward, explicitly, the complication that a_γ involves
1/|ζ′(ρ)| whose second moment diverges under Gonek–Hejhal (J_{−2}), so the
interference process is heavy-tailed; v0 "handles this by truncating at a
quantile and reporting sensitivity."

### 1.4 The model hypotheses, named

I make the spec's "STATED as model hypotheses" concrete. N2 =
(M1)–(M5) below.

- **(M1) Phase randomisation.** The phases {φ_γ : γ > Γ} are i.i.d. uniform
  on [0,2π) and independent of the ordinates.
- **(M2) Ordinate point process.** {γ : γ > Γ} is a simple point process on
  (Γ,∞) with intensity λ(ω) = log(ω/2π)/(2π) and GUE pair correlation.
- **(M3) Amplitude law.** a_γ = |M_W(½+iγ)| · r_γ with r_γ = 1/|ζ′(½+iγ)|
  drawn from the empirical lane_a law, truncated at a quantile q (spec §3),
  independent of φ.
- **(M4) Stationary-Gaussian extension.** ε is replaced by the stationary
  centred Gaussian process with the same second-order structure, and its
  spectral measure is replaced by its intensity-smoothed absolutely
  continuous version S_ε(ω)dω/2π, extended to all ω ∈ ℝ — in particular to
  ω = γ_j, where a realisation carries no atom.
- **(M4′) Band limitation** *(spec clause since AMENDMENT A1, 2026-08-15,
  owner-approved; it was an undeclared addition in v1)*. The observation is
  the ideally band-passed record y_Ω, pass band ω ∈ [−Ω, Ω] with **Ω := 2Γ**.
  All statements below are about y_Ω. See G1_MODEL_SPEC §A1 for the clause,
  what it repairs ((R1)), and the honesty note that it is post-freeze.
  **A2 does not retire this clause** — under (W′) the full-line
  Cameron–Martin integral still diverges, now because the signal's sidelobes
  outrun the noise floor rather than the reverse (§3 (R1), §A2.7).
- **(M4″) Spectral floor** *(spec clause since AMENDMENT A2)*.
  S_ε(ω) := a_{|ω|}²·ϑ(|ω|) with ϑ(ω) := max{log(ω/2π), ϑ_min},
  ϑ_min := log(γ_1/2π) = 0.81076. This is the positivity convention that
  makes the (M4) extension a genuine spectral density on the whole pass band
  (it was GAP-15; see §4.0(e)).
- **(M5) Resolvability.** T · min_{j≠k} |γ_j − γ_k| ≥ 2πK for a constant
  K ≥ 4, and T · (Γ − γ_d) ≥ 2πK.
- **(W′) Window** *(spec clause since AMENDMENT A2)*. W(x) = (1−x)_+,
  M_W(s) = 1/(s(s+1)), |M_W(½+iω)| = ((¼+ω²)(9/4+ω²))^{−1/2} ≍ |ω|^{−2}.
  Enters (M3)'s amplitude law and hence S_ε. See §1.1 and G1_MODEL_SPEC §A2.

(M4) is the single load-bearing idealisation. It is exactly the step the
spec gestures at with "computable spectral density S_ε(ω) **near ω = γ_j**".
It is flagged FRONTIER in §6 and its failure direction is analysed in §7.3.

### 1.5 Parameter and estimator class

θ = (γ_1,…,γ_d, A_1,…,A_d, φ_1,…,φ_d) ∈ Θ ⊂ ℝ^{3d}, with A_j := 2a_{γ_j} > 0
the observed tone amplitude. Amplitudes and phases are **unknown nuisance
parameters** — they involve ζ′(½+iγ_j), which is not available to an
estimator that only sees y. Estimators: any θ̂ measurable w.r.t.
**{y_Ω(t) : t ∈ [0,T]}** — the band-limited record of (M4′) — that is
unbiased on an open neighbourhood of the true θ in Θ (Cramér–Rao's own
regularity requirement; the biased-estimator variant is noted in §6, GAP-7).

**The band limitation restricts the estimator class; it is not free.** More
data means more Fisher information means a *smaller* CR bound, so a bound
proved for y_Ω does **not** transfer to estimators that see the full record
y. (v1 asserted the transfer in §3; that was backwards.) The restriction is
forced rather than convenient: on the full record the information is infinite
(§3 (R1)) and the only valid bound is 0. Every statement of T1 is therefore a
statement about the M4′ class, and is labelled as such.

---

## 2. Statement of T1

Write S_ε for the model-N2 interference spectral density in the convention

  E[ε(t)ε(t+τ)] = (1/2π) ∫_ℝ S_ε(ω) e^{iωτ} dω.                     (2.1)

(In this convention a white noise with E[ε(t)ε(u)] = S₀·δ(t−u) has
S_ε ≡ S₀. All constants below are tied to (2.1); a one-sided or a
per-sample-variance convention changes them by explicit factors of 2 — see
§6, GAP-1.)

Two hypotheses beyond the model are needed and are stated up front rather
than buried:

- **(M4′)** — band limitation, Ω = 2Γ. Since AMENDMENT A1 this is a clause of
  the frozen spec, not an addition of this draft. It fixes the estimator
  class (§1.5).
- **(B1) Band-edge leakage negligibility** *(theorem hypothesis, not a model
  clause)*. Split the pass band into the near-tone part
  N := ∪_j {ω : ||ω| − γ_j| ≤ 2πK/T} and the rest R := {|ω| ≤ Ω} \ N, and let
  I_N, I_R be the corresponding Fisher-information Gram matrices (both PSD,
  I = I_N + I_R). Assume **I_R ⪯ K^{-1} I_N**, equivalently

    **λ_max( I_N^{-1} I_R ) ≤ K^{-1}.**                               (2.2)

  *v2 carried an analytic surrogate for (2.2),
  ρ_j := (3/2π²)S_ε(γ_j)/((Ω−γ_j)²T S_ε(Ω)). That surrogate is calibrated to
  a 1/S_ε that grows **exponentially**, where the ν-integral concentrates at
  the band edge with effective width 2/π. Under (W′) 1/S_ε grows only like
  ν^4, the whole band contributes, and ρ_j understates the true leakage by
  ≈10²·. v3 therefore drops the surrogate and uses the defining quantity
  (2.2), measured directly.*

  **(B1) HOLDS at the approved cut Ω = 2Γ under amendment A2.** Measured
  (§4.0(d)): λ_max(I_N^{-1}I_R) = **0.0858** at γ_d against K^{-1} = 0.25 — a
  factor 2.9 of margin, and the admissible band extends to Ω ≈ 400 = 8Γ. Under
  the *frozen Gaussian* window the same quantity was 1.73·10^{+29}. This is
  the closure of GAP-14, which the v2 audit opened.

  Rider, stated because the theorem quantifies over all j: at the approved cut
  (B1) holds comfortably for γ_3…γ_d, is marginal at γ_2 (λ_max = 0.220) and
  **fails at the lowest tone γ_1 (λ_max = 0.587)**. The consequence is a
  constant, not a collapse: the measured [I^{-1}]_{ωω}/local ratios are 0.743
  (γ_1), 0.896, 0.957, 0.976, 0.962, 0.9943 (γ_d), i.e. deficits ≤ 0.257
  against the theorem's own O(K^{-1}) = 0.25 — the O(K^{-1}) of T1 is
  therefore verified with implied constant ≈ 1.03. The **max_j** statement
  (T1-c), which is what the headline and the corollary use, is attained at
  j = d where the deficit is 0.6 %.

> **Theorem T1 (CR lower bound, model N2 as amended by A1 and A2).**
> Assume (RH), model N2 = (M1)–(M5) **with clauses (M4′), (M4″), (W′)**, the
> resolvability constant K ≥ 4, and the leakage hypothesis (B1). Let θ̂ be any
> unbiased
> estimator of θ from the band-limited record {y_Ω(t) : t ∈ [0,T]},
> T = log X. Then for every j ∈ {1,…,d},
>
>   Var(γ̂_j) ≥ (24 + O(K^{-1})) · S_ε(γ_j) / (A_j² T³)
>            = (6 + O(K^{-1})) · S_ε(γ_j) / (a_{γ_j}² T³),
>
> hence
>
>   **max_{1≤j≤d} RMSE(γ̂_j) ≥ c_d · S_ε(γ_j)^{1/2} / ( a_{γ_j} (log X)^{3/2} )**
>   with **c_d = √6 · (1 + O(K^{-1}))**, uniformly in d.       (T1-a)
>
> **Evaluation of S_ε (Prop. 4.4).** Under (M1)–(M4) and (M4″),
>
>   **S_ε(ω) = a_{|ω|}² · ϑ(|ω|),  ϑ(ω) = max{log(ω/2π), ϑ_min}**,  (T1-b)
>
> which at every target tone (all γ_j > 2π e^{ϑ_min}) is
> S_ε(γ_j) = a_{γ_j}² log(γ_j/2π). **(T1-b) is window-independent**: its
> derivation (Prop. 4.4) uses only (M1)–(M4), never the form of M_W, so A2
> leaves it exactly as v1 and v2 had it. Hence the amplitudes cancel in (T1-a)
> and
>
>   **max_j RMSE(γ̂_j) ≥ √6 · ( log(γ_d/2π) )^{1/2} / (log X)^{3/2}.**  (T1-c)
>
> **Corollary (sample complexity).** If max_j RMSE(γ̂_j) ≤ ε then
>
>   **X ≥ exp( (6 log(γ_d/2π))^{1/3} · ε^{−2/3} ).**              (T1-d)

Constants are explicit: 24 in the variance bound (Lemma 2), √6 in (T1-a)
after A_j = 2a_{γ_j}, and (6 log(γ_d/2π))^{1/3} in (T1-d). The O(K^{-1})
terms are the cross-tone and window-edge corrections controlled in Lemma 2.

Note that c_d = √6 does **not** grow with d. The number of targets enters
only through (M5) (they must be resolvable) and through which γ_j one
evaluates at. Taking j = d maximises log(γ_j/2π) and gives (T1-c).

---

## 3. Regularity conditions — checked, not assumed

The Cramér–Rao inequality is not free. I check each condition against the
model as frozen, and record the two that need care.

Let P_θ denote the law of {y(t)}_{t∈[0,T]} under θ. Under (M4) the noise is
a centred stationary Gaussian process, so P_θ is a Gaussian measure with
fixed covariance operator C (independent of θ) and mean m_θ(t) = Σ_j A_j
cos(γ_j t + φ_j).

**(R1) Common support / mutual absolute continuity.**
Needed: P_θ ≪ P_{θ'} for θ, θ' in a neighbourhood, with support not depending
on θ. For a Gaussian measure with θ-independent covariance, Cameron–Martin
gives: P_θ ≪ P_{θ'} iff m_θ − m_{θ'} ∈ H(C), the reproducing-kernel Hilbert
space of C. **CHECK:** m_θ − m_{θ'} is a finite sum of pure tones restricted
to [0,T]. Its Fourier transform is entire of exponential type T and decays
like |ω|^{-1} off the tones; membership in H(C) requires
∫ |m̂_θ(ω) − m̂_{θ'}(ω)|² / S_ε(ω) dω < ∞. **The integral DIVERGES under
either window, so (R1) FAILS as literally stated — but for opposite
reasons**, and the distinction matters for what A2 does and does not do:

  - *frozen Gaussian W:* a_ω ≍ e^{−πω/4}, so 1/S_ε grows like e^{+πω/2}
    while the numerator decays only polynomially. The **noise outruns the
    signal**: the model is "too clean" at high ω, θ becomes perfectly
    identifiable, the information is infinite and the CR bound is ≡ 0.
  - *A2 window (W′):* a_ω ≍ ω^{−2}, so 1/S_ε grows like ω^4 while the
    numerator decays like ω^{−2}; ∫ω² dω diverges. Here the **signal's
    window-truncation sidelobes outrun the noise floor**.

  *Repair, unchanged by A2.* Spec clause **(M4′)** (§1.4): ideal band-pass
  onto ω ∈ [−Ω,Ω], Ω := 2Γ. **A2 does not retire A1** (G1_MODEL_SPEC §A2.7);
  it makes A1's cut usable.

  **Status: REPAIRED. (R1) HOLDS under (M4′) + (M4″).** On the pass band S_ε
  is bounded below by a positive constant — under (W′) this is now
  unconditional on the *whole* band, since a_ω = |M_W(½+iω)|r_ω is continuous
  and strictly positive there (|M_W(½+iω)| ∈ [9.999·10^{−5}, 4/3] for
  |ω| ≤ 100 — the minimum is at the band edge ω = 100; the value at
  γ_d = 49.77 is 4.034·10^{−4}; bracket corrected 2026-08-15 by the
  independent verification pass, t1_verify.py) and clause (M4″) floors
  the density factor at ϑ_min > 0. So
  1/S_ε is bounded, the Cameron–Martin integral is finite, and all P_θ are
  equivalent Gaussian measures on the band. **The "modulo GAP-15" rider that
  v2 had to attach here is discharged by clause (M4″).**

  *Provenance, and a v1 correction.* (M4′) was **[ADDED]** by v1 of this
  draft and was not in the frozen spec; the required amendment has since been
  made and approved — G1_MODEL_SPEC **AMENDMENT A1** (2026-08-15,
  owner-approved, post-freeze, so labelled). **GAP-2 is therefore CLOSED
  (REPAIRED-BY-A1).** v1 added, wrongly, that "band-limiting only *removes*
  information, so any lower bound proved for y_Ω is a valid lower bound for
  y". The direction is backwards: removing information *raises* the CR
  bound, so the y_Ω bound does not transfer to estimators seeing y. See
  §1.5 — M4′ restricts the estimator class, and that restriction is forced,
  because on the unrestricted record the only valid bound is 0.

  *What A1 does not do, and what A2 then did.* Making the information finite
  is not the same as making the local white-noise computation of §4 correct.
  Under the frozen Gaussian window, at Ω = 2Γ the information was finite but
  astronomically larger than the local value (v2's GAP-14). Amendment A2
  removes that gap at the root: under (W′) the measured band-limited
  [I^{-1}]_{ωω} at γ_d is 0.9943 of the local 24-value (§4.0(d)).

**(R2) Differentiability of the log-likelihood in θ.**
Under (M4′), with W_C the whitening operator,

  log dP_θ/dP_0 (y) = ⟨y, m_θ⟩_C − ½‖m_θ‖²_C,  ⟨u,v⟩_C := (1/2π)∫_{|ω|≤Ω} û(ω) conj(v̂(ω))/S_ε(ω) dω.
                                                                      (3.1)

**CHECK:** θ ↦ m_θ is real-analytic (finite sum of cos(γ_j t + φ_j), analytic
in γ_j, φ_j, linear in A_j) into L²[0,T]; ‖·‖_C is a continuous quadratic
form on L²[0,T] because S_ε is bounded below on the band. Hence the map
θ ↦ log dP_θ/dP_0 is a.s. real-analytic in θ, and (3.1) is quadratic in θ's
analytic image. **HOLDS.**

**(R3) Interchange of ∂_θ and ∫ (differentiation under the integral sign).**
Needed: ∂_θ ∫ dP_θ = 0 and ∂_θ ∫ θ̂ dP_θ = ∫ θ̂ ∂_θ dP_θ.
**CHECK:** With (3.1), the score is ∂_j log dP_θ/dP_0 = ⟨y − m_θ, ∂_j m_θ⟩_C,
a *Gaussian* random variable with mean 0 and variance ‖∂_j m_θ‖²_C < ∞. The
family {dP_θ/dP_0} is dominated and locally uniformly L²(P_0)-bounded on a
compact θ-neighbourhood (the exponent is a continuous quadratic form in a
compact set of directions). Dominated convergence then licenses both
interchanges. **HOLDS**, given (M4′). Without (M4′) it fails together with
(R1).

**(R4) Fisher information finite and nonsingular.**
**CHECK:** finiteness is ‖∂_j m_θ‖²_C < ∞, immediate on the band.
Nonsingularity: the 3d vectors {∂_{γ_j} m, ∂_{A_j} m, ∂_{φ_j} m} are linearly
independent in L²[0,T] provided the tones are resolvable — this is exactly
(M5), and Lemma 2 exhibits the inverse block explicitly. **HOLDS under (M5).**
If (M5) fails (two zeros closer than 2πK/T) the FIM degenerates and T1 says
nothing — the correct behaviour, and the reason (M5) is a hypothesis and not
a convenience.

**(R5) Unbiasedness on an open set.**
Assumed by hypothesis on the estimator class. Not a property of the model.
Genuinely restrictive: periodogram-type estimators (T2) are biased at finite
T. See §6, GAP-7 for the van-Trees/Bayesian route that removes it.

**(R6) Gaussianity of ε (the approximation that (M4) makes). — REPAIRED BY
AMENDMENT A2. GAP-3 CLOSED.**
Not a regularity condition for CR, but a validity condition for the model.
ε = 2Σ_{γ>Γ} a_γ cos(γ t + φ_γ) is a sum of infinitely many independent
(under M1) bounded terms; a Lindeberg condition gives a CLT provided no
single term dominates. The diagnostic is the ratio of the largest single
term's variance contribution to the total,

  **Λ(Γ) := 2 a_Γ² / σ²(Γ),  σ²(Γ) := 2 Σ_{γ>Γ} a_γ²
           ≈ 2 ∫_Γ^∞ a_ω² · log(ω/2π)/(2π) · dω**              (3.2)

(the intensity-smoothed variance of (M2)). Lindeberg requires Λ(Γ) → 0.

*Under the frozen Gaussian window — FAILS.* a_γ ≍ e^{−πγ/4} decays
geometrically, so the *first* few terms above Γ dominate the sum absolutely.
Measured: **Λ(50) = 4.76**, Λ(200) = 2.85. A ratio exceeding 1 says a single
term carries more than the model's entire smoothed variance. ε is not close
to Gaussian; it is close to a small sum of a few random phases. This was the
single most serious honest defect of T1 v1/v2.

*Under (W′) — HOLDS.* a_ω ≍ ω^{−2}, so a_ω² ≍ ω^{−4} and (3.2) evaluates in
closed form:

  σ²(Γ) ≈ Γ^{−3}( log(Γ/2π) + ⅓ )/(3π),  2a_Γ² = 2Γ^{−4},

  **Λ(Γ) ≈ 6π / ( Γ · ( log(Γ/2π) + ⅓ ) )  →  0.**              (3.3)

Numerically (direct quadrature of (3.2), not the closed form):
Λ(50) = **0.1565**, Λ(200) = 0.02484, Λ(10³) = 3.489·10^{−3},
Λ(10⁴) = 2.446·10^{−4}. The closed form (3.3) predicts 0.1568, 0.02487,
3.49·10^{−3}, 2.45·10^{−4} — agreement to 3 digits, so (3.3) is a usable
analytic diagnostic and not a fit. The mechanism is the one A2 was chosen
for: with polynomial amplitude decay the number of interferers of comparable
size in [Γ, 2Γ] is ≍ Γ log Γ / 2π ≫ 1, so no finite set dominates.

  **Status: (R6) HOLDS under A2, and GAP-3 is CLOSED.** The frozen spec §3
  claim that the interference is "Gaussian-approximable" is no longer
  known-false; it is now supported by a Lindeberg condition that is checkable
  and checked. T1 v3 therefore drops the "Gaussian **surrogate** of N2"
  hedge that v2 carried in §0/§3/§8, and reverts to the spec's own label,
  "CR bound in model N2".

  *Residual, logged not hidden.* Λ(50) = 0.157 is small but not negligible at
  the concrete operating point of §5 (Γ = 50). Lindeberg gives convergence,
  not a rate; the Berry–Esseen-type error at finite Γ — plausibly O(√Λ) ≈ 0.4
  at Γ = 50 — is **not** established. That is **GAP-17**, new in v3, created
  by A2 rather than inherited. (M3)'s quantile truncation is what keeps the
  individual terms uniformly bounded and is load-bearing for the Lindeberg
  condition, which links GAP-17 to GAP-10.

**Summary of the regularity audit.** (R2),(R3),(R4) hold. (R1) failed as
stated and is REPAIRED by spec clause (M4′) (amendment A1) plus (M4″)
(amendment A2, which discharges the low-frequency residue) — at the cost of
restricting the estimator class, which is a real cost and is declared in
§1.5, not a free reduction. (R5) is a restriction on the estimator class,
declared. **(R6) failed under the frozen window and is REPAIRED by amendment
A2** (clause W′): the Lindeberg ratio now vanishes like 6π/(Γ log Γ),
measured. What remains at (R6) is a rate, not a validity, question (GAP-17).
Separately, (R1)'s repair was *qualitative* under A1 alone — it restored
absolute continuity but left the information far above the local white-noise
value at Ω = 2Γ; **A2 closes that too** (§4.0(d), GAP-14 CLOSED).

---

## 4. Fisher information — computed

### 4.0 Re-derivation under the band limit (M4′) and the A2 window (W′)

Everything below §4.1 was computed in v1 without a band limit. Clause (M4′)
changed the ambient space; clause (W′) changes S_ε itself. Each step is
re-checked here — measured, not asserted.

**Provenance of the numbers in this section.** The figures were produced by a
script written this session (`scratchpad/a2_verify.py`, `scratchpad/a2_b1.py`;
uncommitted — GAP-8). It reimplements log Γ from scratch (recurrence +
Stirling) and, **before** being applied to (W′), reproduces every
Gaussian-window figure of v2 independently: the §5.1 amplitude table
(1.1602e−5, 4.7010e−8, 1.9622e−9, 2.6594e−11, 3.6304e−12, 5.9090e−18), the
white-noise factor-24 checks (23.9268 / 23.8236 / 23.9467), and the v2
leakage measurement (7.68·10^{−30} at Γ = 50, 1.60·10^{−31} at Γ = 51.234).
The v2 → v3 comparisons below are therefore like-for-like.

**Second, independent implementation — agrees to every reported digit.** A
separately written re-verification, `lane_t/t1_verify.py` (also uncommitted;
its header states it was written from scratch without reuse of the first
script), was executed against every A2 claim in this draft. Agreement is
exact at the precision printed: Lindeberg 4.76 / 0.1565 / 0.02484 /
3.489e−3 / 2.446e−4; flatness 97.07 / 2.033 (γ_1), 98.2 / 1.229 (γ_d);
white-noise 24-checks 23.9268 / 23.8237 / 23.9466; (B1) λ_max 0.5867 /
0.2203 / 0.1323 / 0.1083 / 0.1235 / 0.0858 and ratios 0.7431 … 0.9943;
Gaussian control 1.7294e+29 and 7.6795e−30; the Ω-sweep; the ϑ_min sweep; and
the headline constants 1.694393 / 2.315688. It additionally reports **all
ten** tones rather than the six tabulated here — λ_max = 0.587, 0.220, 0.132,
0.108, 0.123, 0.093, 0.102, 0.100, 0.089, 0.086 — confirming that γ_1 is the
*only* tone at which (B1) fails as an inequality and γ_2 the only marginal
one. Two independent implementations is evidence, not a receipt; GAP-8
stands.

Under (M4′) the Fisher information is the Gram matrix

  I_{jk}(θ) = ⟨∂_j m_θ, ∂_k m_θ⟩_C
            = (1/2π) ∫_{|ν| ≤ Ω} ∂̂_j m(ν) · conj(∂̂_k m(ν)) / S_ε(ν) dν,   (4.0)

where ∂̂_j m is the Fourier transform of the *time-limited* derivative
(supported in t ∈ [0,T], hence spread over all ν).

**(a) The target tones are interior to the band, with margin ≥ Γ.**
(M3)/N2 fix γ_d < Γ, and (M4′) sets Ω = 2Γ, so for every j ≤ d

  Ω − γ_j = 2Γ − γ_j > 2Γ − Γ = Γ > 0,

and the mirror tones at −γ_j are interior by symmetry. The Lemma-1
neighbourhoods [γ_j − 2πK/T, γ_j + 2πK/T] are interior too: (M5) gives
T(Γ − γ_d) ≥ 2πK, hence γ_j + 2πK/T ≤ γ_d + (Γ − γ_d) = Γ < Ω, with slack
Ω − Γ = Γ. So the band-pass touches neither a tone nor its Lemma-1
neighbourhood. **Verified.**

**(a′) (W′) does not disturb (a).** The band geometry is set by Γ, Ω and T
only; the window enters nowhere in (a). The tones remain interior with margin
≥ Γ. **Verified.**

**(b) S_ε(γ_j) is unchanged — by the band-pass, and in form by (W′).** An
ideal band-pass multiplies the spectrum by 1_{|ν| ≤ Ω}; it leaves the
spectral density *inside* the band pointwise untouched. By (a), γ_j is
interior, so S_ε(γ_j) in (T1-a)/(T1-b) is exactly the pre-amendment
expression a_{γ_j}² log(γ_j/2π). Under (W′) the *value* of a_{γ_j} changes
(from 5.909·10^{−18} to 4.034·10^{−4} at γ_d, §5.1) but the *expression* does
not, and **the amplitude cancellation of §0 and Prop. 4.4 is unaffected**:
Prop. 4.4 derives S_ε from (M1)–(M4) alone and never uses the form of M_W,
so S_ε(γ_j)^{1/2}/a_{γ_j} = (log(γ_j/2π))^{1/2} identically, for any window.
**Verified.** (One rider survives: (M4)'s extension of S_ε to ω = γ_j, where
no interference atom lives, is still GAP-9. The other v2 rider — the low-ω
positivity convention, GAP-15 — is discharged by clause (M4″), see (e).)

**(c) The constant 24 survives the band-pass, with an O(K^{-1}) correction.**
The band-pass removes the out-of-band energy of each ∂_j m. For a tone at ω
with Δ := Ω − ω, the time-limited derivatives have |∂̂_A m|, |∂̂_φ m| ≲ A/|ν−ω|
and |∂̂_ω m| ≲ AT/(2|ν−ω|), so

  removed fraction of ‖∂_ω m‖²  ≤  [ (A²T²/4)·(2/Δ)/2π ] / (A²T³/6)
                                =  6/(4π Δ T)  =  O(1/(ΔT)),
  removed fraction of ‖∂_A m‖², ‖∂_φ m‖²  ≤  2/(π Δ T)  =  O(1/(ΔT)).

By (a), Δ ≥ Γ and TΓ ≥ 2πK (from T(Γ−γ_d) ≥ 2πK and γ_d > 0), so both
fractions are ≤ 0.08/K = O(K^{-1}) — the same order as the cross-tone error
already carried in Lemma 3(a), hence absorbed, and *smaller* than the
O(1/(ωT)) relative error already carried inside Lemma 2 (since Δ ≥ Γ > γ_j).
At the §5 numbers (γ_d = 49.7738, Γ = 50, Ω = 100, T = 17.2167) the two
fractions are 5.5·10^{−4} and 7.4·10^{−4}. So the truncation of the *signal*
by the band-pass is harmless and **the algebra of Lemma 2 — det = (A²/S₀)²T⁴/48,
[I^{-1}]_{ωω} = 24 S₀/(A²T³) — goes through unchanged. Verified.**

Independent numerical re-check of the constant under (4.0), this session:
exact 3×3 band-limited FIM assembled from the closed-form transforms of
cos(ωt+φ), −At sin(ωt+φ), −A sin(ωt+φ) on [0,T] (T = 17.2167, A = 1,
φ = 0.4), white S_ε ≡ 1, band Ω large:

| ω | Ω | T³·[I^{-1}]_{ωω} |
|---|---|---|
| 3.7 | 400 | 23.927 |
| 14.1347 | 400 | 23.824 |
| 49.7738 | 600 | 23.947 |

→ 24. Consistent with v1's time-domain check (23.24…23.92). **Factor 24
re-verified under the band-limited formulation.**

*Third verification, new in v3: band-limited AND coloured by the actual (W′)
model S_ε.* The two checks above are white-noise checks — they confirm the
algebra of Lemma 2 but not that the coloured, band-limited problem at the
approved cut has the same constant. Under (W′) it does. With the model
S_ε(ν) = |M_W(½+iν)|²ϑ(|ν|) of (T1-b)/(M4″), tone at γ_d = 49.7738,
T = 17.2167, Ω = 2Γ:

| Γ | Ω = 2Γ | [I^{-1}]_{ωω} ÷ 24 S_ε(γ_d)/(A²T³) |
|---|---|---|
| 50 | 100 | **0.99432** |
| 51.234 (M5-tight) | 102.468 | **0.99392** |

so the effective constant is 24 × 0.9943 = **23.86**, inside the O(K^{-1})
tolerance the theorem already declares. Under the *frozen Gaussian* window
the same measurement gave 7.68·10^{−30} and 1.60·10^{−31}. **The factor 24
is now verified in the setting T1 actually claims it, not only in a local
white-noise surrogate.** (Decomposition of the 0.9943: the near-tone block
alone gives [I_N^{-1}]_{ωω}/local = 1.0794, a +8 % excess from the Lemma-1
flatness δ of GAP-4, and the band-edge leakage removes 8.6 % of that. The two
residual defects partially cancel; both are reported separately below rather
than netted.)

**(d) The band-edge leakage term — the v2 failure, and its repair by A2.**
(a)–(c) say the band-pass loses little *signal*. They do not say the retained
out-of-band frequencies are uninformative. Split I = I_N + I_R as in (B1).

*Why it failed under the frozen window.* On R the Gaussian-window noise is
exponentially quieter than at the tone: 1/S_ε(ν) ≍ e^{+πν/2}, while
|∂̂_ω m(ν)|² ≍ A²T²/(4(ν−ω)²) decays only quadratically. The ν-integral in
(4.0) was therefore dominated by the band EDGE, and the model handed the
estimator an arbitrarily quiet channel there.

*Why it holds under (W′).* 1/S_ε(ν) now grows only like ν^4. The edge no
longer dominates — the whole band contributes comparably — and the leakage
information stays a bounded fraction of the near-tone information. Measured
directly as the defining quantity (2.2) (not via the v2 surrogate ρ, which
is calibrated to exponential growth and understates the polynomial case by
≈10²·):

| window | Γ | Ω = 2Γ | S_ε(γ_d) | S_ε(Ω) | **λ_max(I_N^{-1}I_R)** | [I^{-1}]_{ωω} ÷ 24S_ε(γ_d)/(A²T³) |
|---|---|---|---|---|---|---|
| Gaussian (frozen) | 50 | 100 | 7.226e−35 | 3.714e−69 | 1.73e+29 | 7.68e−30 |
| Gaussian (frozen) | 51.234 | 102.468 | 7.226e−35 | 7.669e−71 | 7.43e+30 | 1.60e−31 |
| **(W′) Riesz k=1** | **50** | **100** | **3.369e−07** | **2.767e−08** | **0.0858** | **0.99432** |
| **(W′) Riesz k=1** | **51.234** | **102.468** | **3.369e−07** | **2.532e−08** | **0.0862** | **0.99392** |

(B1) requires λ_max ≤ K^{-1} = 0.25. **(B1) HOLDS under A2 at the approved
cut, with a factor 2.9 of margin. GAP-14 is CLOSED.**

*How much band width the margin buys* (same measurement, tone at γ_d, (W′)):

| Ω | 100 | 200 | 300 | **400** | 600 | 1000 | 3000 | 15000 |
|---|---|---|---|---|---|---|---|---|
| λ_max(I_N^{-1}I_R) | 0.086 | 0.106 | 0.153 | **0.250** | 0.624 | 2.36 | 49.8 | 4.9e+3 |
| [I^{-1}]_{ωω} ÷ local | 0.994 | 0.980 | 0.961 | 0.935 | 0.873 | 0.768 | 0.644 | 0.518 |

so (B1) at K = 4 holds out to **Ω ≈ 400 = 8Γ**, and the approved cut sits
inside with a factor 4 of band-width margin. Contrast v2's Gaussian-window
sweep, where the admissible band was Ω = γ_d + O(1) (ratio 1.00 at
Ω−γ_d = 1, 0.36 at 4, 6·10^{−2} at 6, 7.7·10^{−30} at Ω = 2Γ). Note also
that the failure beyond Ω ≈ 400 is now **soft**: the bound degrades to 0.52
of the local value at Ω = 1.5·10⁴, because the leakage information sits
largely in directions other than ω. Under the Gaussian window the same
excursion cost 29 orders of magnitude.

*Per-tone rider (the theorem quantifies over all j).* At Ω = 2Γ = 100 under
(W′):

| tone | γ_1 | γ_2 | γ_3 | γ_4 | γ_5 | γ_10 = γ_d |
|---|---|---|---|---|---|---|
| λ_max(I_N^{-1}I_R) | **0.587** | 0.220 | 0.132 | 0.108 | 0.124 | 0.0858 |
| [I^{-1}]_{ωω} ÷ local | 0.743 | 0.896 | 0.957 | 0.976 | 0.962 | 0.9943 |
| deficit 1 − ratio | 0.257 | 0.104 | 0.043 | 0.024 | 0.038 | 0.006 |

(B1) as an inequality **fails at γ_1** (0.587 > 0.25) and is marginal at γ_2.
Reported, not smoothed. But the consequence is a constant and not a
collapse: every deficit is ≤ 0.257 against the theorem's own O(K^{-1}) with
K^{-1} = 0.25, so T1's O(K^{-1}) correction term is *verified* with implied
constant ≈ 1.03 — the statement T1 makes is true at every tone, including
the one where the sufficient condition (B1) is violated. The **max_j**
statement (T1-c) and the corollary (T1-d) are attained at j = d, where the
deficit is 0.6 %.

**Conclusion of the re-derivation.** Under A2 the band-limited CR bound at
the approved cut Ω = 2Γ agrees with the displayed (T1-a) constants to within
0.6 % at j = d and within the declared O(K^{-1}) at every j. The v2 verdict —
"T1's constants are the constants of the local problem, not a proved bound
for the M4′ class at Ω = 2Γ" — is **superseded**: they are now both.

**(e) The low-frequency end of the band (GAP-15) — closed by clause (M4″),
with the sensitivity measured.** v2 noted that (M4)'s extension of
S_ε(ω) = a_{|ω|}²log(|ω|/2π) to the whole pass band is *negative* for
|ω| < 2π and therefore not a spectral density, and that taking it to 0 there
reopens a low-frequency copy of the (R1) divergence. Amendment A2 fixes the
convention rather than arguing it away: clause (M4″) sets
ϑ(ω) := max{log(ω/2π), ϑ_min} with ϑ_min = log(γ_1/2π) = 0.81076.

Two facts make this benign under (W′), and the second is measured rather than
argued:

1. a_ω = |M_W(½+iω)|·r_ω is continuous and strictly positive on the band
   (|M_W(½+iω)| runs monotonically from 4/3 at ω = 0 to 9.999·10^{−5} at
   ω = Ω = 100; 4.034·10^{−4} is its value at γ_d = 49.77 — corrected
   2026-08-15, t1_verify.py), so with the floor, S_ε is bounded below by a positive
   constant on all of [−Ω,Ω] — the (R1) repair is complete on the whole band.
2. The floor's *value* does not matter. Band-limited [I^{-1}]_{ωω} ÷ local at
   γ_d, Ω = 2Γ = 100, under (W′), as ϑ_min is swept:

   | ϑ_min | 0.05 | 0.20 | 0.81076 | 1.00 | 2.00 |
   |---|---|---|---|---|---|
   | ratio | 0.994312 | 0.994313 | 0.994315 | 0.994317 | 0.994685 |

   a relative spread of 4·10^{−4} over a factor 40 in the floor.

**GAP-15 CLOSED.** Note that v2's argument for benignity was window-specific
and does *not* survive A2 — it relied on a_ω² being larger at small ω by
e^{π(γ_1−ω)/2} (a factor 3.7·10⁹ at ω = 1), which made the sub-2π band
automatically far noisier than the tone. Under (W′) that factor is only
(γ_1/1)² ≈ 200, so the old argument would no longer carry and an explicit
convention is genuinely required. The gap is closed by the clause, not by the
old reasoning.

### Lemma 1 (local whitening).
Let S_ε be continuous and bounded below on the band, and suppose S_ε varies
by at most a factor (1+δ) over the interval [γ_j − 2πK/T, γ_j + 2πK/T].
Then for any u, v supported in that frequency band around ±γ_j,

  (1+δ)^{-1} S_ε(γ_j)^{-1} ∫_0^T u v dt ≤ ⟨u,v⟩_C ≤ (1+δ) S_ε(γ_j)^{-1} ∫_0^T u v dt.

*Proof.* Plancherel on [0,T] plus the pointwise bound on 1/S_ε over the
support. ∎

Interpretation: near γ_j the coloured noise acts exactly like white noise of
two-sided PSD S₀ = S_ε(γ_j), and

  **I_{jk}(θ) = S_ε(γ_j)^{-1} ∫_0^T ∂_j m_θ(t) ∂_k m_θ(t) dt · (1 + O(δ)).**  (4.1)

**[Flatness estimate, re-derived under (W′) in v3.]** The relevant quantity
is the log-slope of S_ε. Under the *frozen Gaussian* window
d/dω log S_ε = −π/2 + O(1/ω): π/2 per unit ω is not small, and over the
width-4πK/T band (≈ 2.92 at K = 4, T = 17.22) S_ε varies by a **factor 98.2**
at γ_d (93.7–98.2 across γ_1…γ_d). The "O(δ) negligible" claim of (4.1) was
unjustified. Under **(W′)**, a_ω² = 1/((¼+ω²)(9/4+ω²)) gives

  d/dω log S_ε = −2ω/(¼+ω²) − 2ω/(9/4+ω²) + 1/(ω log(ω/2π))
               = **−4/ω + O(1/(ω log ω))**,

so the variation over the band is at most e^{16πK/(ωT)} — an explicit
**O(K/(ωT))**, the *same order as the relative error O(1/(ωT)) that Lemma 2
already carries*, and vanishing in T. Measured max/min of S_ε over
[γ_j − 2πK/T, γ_j + 2πK/T]:

| tone | γ_1 | γ_2 | γ_3 | γ_4 | γ_5 | γ_d |
|---|---|---|---|---|---|---|
| Gaussian (frozen) | 97.1 | 93.7 | 95.6 | 96.8 | 97.2 | 98.2 |
| **(W′)** | **2.03** | 1.55 | 1.46 | 1.38 | 1.35 | **1.23** |

**GAP-4 is REDUCED by A2 but NOT closed.** A factor 1.23 at γ_d (2.03 at
γ_1) is a genuine two-sided constant, not "negligible", and Lemma 1 should
be restated with S_ε evaluated at the band edge rather than at the centre.
What A2 changes is that this is now a bounded, computable,
T→∞-vanishing constant instead of a factor of 98. Its measured effect on the
final number is +8 % ([I_N^{-1}]_{ωω}/local = 1.0794, §4.0(c)).

**[Scope warning, added in v2; status updated in v3.]** Lemma 1 is stated for
u, v *supported* in the neighbourhood of ±γ_j. The derivatives ∂_j m_θ are
time-limited to [0,T] and hence have tails at every frequency, so (4.1) is
the information of the near-tone part I_N only. Using (4.1) as the whole
Fisher information is exactly hypothesis (B1) — which **failed** at Ω = 2Γ
under the frozen window and **holds** under A2 (§4.0(d), GAP-14 CLOSED).
GAP-4 (the δ inside the neighbourhood) and GAP-14 (the leakage outside it)
were the short-range and long-range halves of one defect; A2 closes the
long-range half outright and shrinks the short-range half by a factor ≈ 80.

### Lemma 2 (single-tone FIM with nuisance amplitude and phase).
Let m(t) = A cos(ωt + φ) on [0,T] and let the effective noise be white with
two-sided PSD S₀ in convention (2.1). Then with θ = (A, ω, φ),

  ∂_A m = cos(ωt+φ),  ∂_ω m = −A t sin(ωt+φ),  ∂_φ m = −A sin(ωt+φ),

and, using ∫_0^T cos²(ωt+φ)dt = T/2 + O(1/ω), ∫_0^T sin(ωt+φ)cos(ωt+φ)dt =
O(1/ω), ∫_0^T t sin²(ωt+φ)dt = T²/4 + O(T/ω), ∫_0^T t² sin²(ωt+φ)dt =
T³/6 + O(T²/ω):

  I = S₀^{-1} · [ T/2                          0                0
                  0          A²T³/6      A²T²/4
                  0          A²T²/4      A²T/2 ]  + (relative error O(1/(ωT))).

A decouples. For the (ω,φ) block,

  det = (A²/S₀)² ( T³/6 · T/2 − (T²/4)² ) = (A²/S₀)² ( T⁴/12 − T⁴/16 )
      = (A²/S₀)² T⁴ / 48,

  [I^{-1}]_{ωω} = I_{φφ} / det = (A²T/(2S₀)) · 48 / ( (A²/S₀)² T⁴ )

  **[I^{-1}]_{ωω} = 24 · S₀ / (A² T³).**                             (4.2)

*Numerical verification of the constant 24.* Exact discrete FIM assembled and
inverted for A = 1, ω = 3.7, φ = 0.4, S₀ = 1, N = 2·10⁵ samples:
T³·[I^{-1}]_{ωω} = 23.238 (T=20), 23.884 (T=50), 23.876 (T=100), 23.922
(T=200) → 24. Confirmed. (Script: this session, not committed; see GAP-8.)

*Convention warning.* Several standard references (Rife–Boorstyn; Kay,
*Fundamentals of Statistical Signal Processing*, Ex. 3.14) quote 12, not 24,
because they either use a complex exponential (one nuisance phase but complex
circular noise) or a per-sample noise variance σ² with a different
PSD-to-variance identification. In convention (2.1) with a *real* cosine and
*both* A and φ unknown, 24 is correct, as the numerical check confirms.
Getting this factor wrong changes c_d by √2. **This is why (2.1) is pinned
in §2.** ∎

### Lemma 3 (multi-tone block-diagonality, and discrete ≤ continuous).
(a) With d tones satisfying (M5), the cross-tone FIM entries between
parameters of tone j and tone k ≠ j are O(T³ /(K)) relative to the diagonal
block, i.e. the FIM is block diagonal up to relative error O(K^{-1}).
*Proof sketch:* every cross entry is an integral of the form
∫_0^T t^p cos((γ_j ± γ_k)t + ψ) dt, p ≤ 2, which is ≤ T^p/|γ_j ± γ_k| ≤
T^{p+1}/(2πK) by (M5), against a diagonal entry of order T^{p+1}. Blocks
therefore invert independently to relative accuracy O(K^{-1}), and
[I^{-1}]_{γ_jγ_j} ≥ (1 − CK^{-1}) · [I_j^{-1}]_{ωω}.
(b) Any estimator from n_s samples is a function of the continuous record, so
its FIM is dominated by the continuous FIM (data-processing for Fisher
information). Hence the continuous bound is valid for every n_s. ∎

### Proposition 4.4 (the interference spectral density S_ε).
Under (M1)–(M4), for |ω| > Γ,

  E[ε(t)ε(t+τ)] = E[ 4 Σ_{γ,γ'>Γ} a_γ a_{γ'} cos(γt+φ_γ)cos(γ'(t+τ)+φ_{γ'}) ]
                = 4 Σ_{γ>Γ} a_γ² · E[cos(γt+φ_γ)cos(γt+γτ+φ_γ)]     [(M1): cross terms vanish]
                = 4 Σ_{γ>Γ} a_γ² · ½ cos(γτ)
                = 2 Σ_{γ>Γ} a_γ² cos(γτ)
                = Σ_{γ>Γ} a_γ² ( e^{iγτ} + e^{−iγτ} ).

So the spectral measure μ (defined by E[ε(t)ε(t+τ)] = ∫ e^{iωτ} dμ(ω)) is
**purely atomic**, with mass a_γ² at each of ±γ. Under (M4) replace μ by its
intensity-smoothed version: the expected mass in [ω, ω+dω], ω > 0, is
a_ω² · λ(ω) dω = a_ω² · log(ω/2π)/(2π) · dω. Matching to
dμ = S_ε(ω) dω / 2π gives

  **S_ε(ω) = a_{|ω|}² · log(|ω|/2π).**                              (4.3)

**Window-independence (the reason A2 leaves the headline alone).** The
derivation above uses (M1) (phase randomisation kills cross terms), (M2)
(the intensity λ), (M3) (a_γ, whatever its value) and (M4) (smoothing). **It
never uses the form of M_W.** So (4.3) holds verbatim under (W′), with a_ω
now ≍ ω^{−2} rather than ≍ e^{−πω/4}, and

  S_ε(γ_j)^{1/2} / a_{γ_j} = ( log(γ_j/2π) )^{1/2}

identically, for any admissible window. This is why amendment A2 changes the
observable, the amplitudes and the noise spectrum while leaving (T1-a),
(T1-c), (T1-d) and every displayed constant untouched (§7.4).

**Under (M4′) and (M4″).** (4.3) is derived for |ω| > Γ from the actual
interference and then extended to all ω by (M4). The band-pass does not
modify it inside the band, and by §4.0(a),(b) the evaluation point γ_j is
interior, so S_ε(γ_j) = a_{γ_j}² log(γ_j/2π) stands exactly as in v1. Two
riders that the band limit made visible, both now resolved:

- the pass band explicitly includes |ω| < 2π, where (4.3) is **negative**
  (log(|ω|/2π) < 0) and therefore not a spectral density. This was
  **GAP-15**; amendment A2's clause **(M4″)** supplies the convention
  (ϑ = max{log(ω/2π), ϑ_min}, ϑ_min = log(γ_1/2π)), and §4.0(e) measures the
  sensitivity at 4·10^{−4} relative over a factor 40 in the floor.
  **CLOSED.** (v2's argument that the floor is harmless *because* a_ω² is
  larger at small ω by e^{π(γ_1−ω)/2} was window-specific and does not
  survive A2 — see §4.0(e).)
- the *upper* end of the band was not benign under the frozen window — that
  was GAP-14, and it is **CLOSED by A2**; see §4.0(d).

Note GUE pair correlation (M2) does **not** enter (4.3): the first moment of
the point process determines the mean spectral density; pair correlation
affects only the *fluctuation* of the periodogram about it (relevant to T2's
constants, not T1's). ∎

### Proof of Theorem T1.
By (R1)–(R4) under (M4′), (M4″) and (M5), the CR inequality applies to θ̂ on
the band-limited record: Cov(θ̂) ⪰ I(θ)^{-1}, I as in (4.0). By hypothesis
(B1), I = I_N + I_R ⪯ (1 + K^{-1}) I_N, hence I^{-1} ⪰ (1 + K^{-1})^{-1}
I_N^{-1} and [I^{-1}]_{γ_jγ_j} ≥ (1 − O(K^{-1})) [I_N^{-1}]_{γ_jγ_j}: the
leakage outside the tone neighbourhoods is absorbed into the O(K^{-1}) terms.
(This is the step that *failed* at Ω = 2Γ under the frozen Gaussian window
and **holds under amendment A2**, λ_max(I_N^{-1}I_R) = 0.0858 ≤ K^{-1} at
γ_d — §4.0(d), GAP-14 CLOSED.) By §4.0(c) the
band-pass loses only an O(K^{-1}) fraction of each ‖∂_j m‖². By Lemma 3(a),
[I_N^{-1}]_{γ_jγ_j} equals the single-tone value up to relative error
O(K^{-1}). By Lemma 1 the noise near γ_j is white of PSD S₀ = S_ε(γ_j),
unchanged by the band-pass (§4.0(b)). By Lemma 2 with A = A_j,

  Var(γ̂_j) ≥ (24 + O(K^{-1})) S_ε(γ_j) / (A_j² T³).

Since A_j = 2 a_{γ_j}, A_j² = 4 a_{γ_j}², giving 24/4 = 6:

  Var(γ̂_j) ≥ (6 + O(K^{-1})) S_ε(γ_j) / (a_{γ_j}² T³).

RMSE(γ̂_j) = Var(γ̂_j)^{1/2} for unbiased θ̂, so
RMSE(γ̂_j) ≥ √6 · S_ε(γ_j)^{1/2}/(a_{γ_j} T^{3/2}), which is (T1-a) with
c_d = √6(1+O(K^{-1})). Substituting (4.3),
S_ε(γ_j)^{1/2}/a_{γ_j} = (log(γ_j/2π))^{1/2}, giving

  RMSE(γ̂_j) ≥ √6 (log(γ_j/2π))^{1/2} / T^{3/2}   for each j,

and max_j of the right side is attained at j = d, which is (T1-c) with
T = log X. For the corollary, max_j RMSE ≤ ε forces
T^{3/2} ≥ √6 (log(γ_d/2π))^{1/2}/ε, i.e. T ≥ (6 log(γ_d/2π))^{1/3} ε^{−2/3},
i.e. X = e^T ≥ exp((6 log(γ_d/2π))^{1/3} ε^{−2/3}). ∎

---

## 5. Numerical evaluation and comparison with the lane numerics

### 5.1 The constants, evaluated

Zero ordinates (Odlyzko standard values). Both windows tabulated, because the
comparison is the practical payoff of A2: the frozen
|M_W(½+iγ)| = ½|Γ(¼+iγ/2)| (log-Γ by recurrence + Stirling this session,
agreeing with v2 to 5 digits), and the A2 window's
|M_W(½+iγ)| = ((¼+γ²)(9/4+γ²))^{−1/2}.

| j | γ_j | \|M_W\| **frozen Gaussian** | \|M_W\| **(W′) Riesz k=1** | ratio | log(γ_j/2π) |
|---|---|---|---|---|---|
| 1 | 14.134725 | 1.1602e−05 | 4.9742e−03 | 4.29e+02 | 0.81076 |
| 2 | 21.022040 | 4.7010e−08 | 2.2564e−03 | 4.80e+04 | 1.20769 |
| 3 | 25.010858 | 1.9622e−09 | 1.5954e−03 | 8.13e+05 | 1.38143 |
| 4 | 30.424876 | 2.6594e−11 | 1.0788e−03 | 4.06e+07 | 1.57738 |
| 5 | 32.935062 | 3.6304e−12 | 9.2084e−04 | 2.54e+08 | 1.65666 |
| 10 | 49.773832 | 5.9090e−18 | 4.0344e−04 | **6.83e+13** | 2.06961 |

The **dynamic range across γ_1…γ_10 collapses from 13 orders of magnitude to
a factor 12.3**, and the raw amplitude at γ_10 rises by 13.8 orders. This is
the resolution of §7.1's complaint. It changes no constant in T1 — the
amplitudes cancel — but it is the difference between an observable that is a
thought experiment and one that is an instrument.

Sample-complexity constant c = (6 log(γ_d/2π))^{1/3} in (T1-d) — **unchanged
by A2**, since c depends on the window through nothing:

- d = 1:  c = **1.6944**, so X(ε) ≥ exp(1.6944 · ε^{−2/3}).
- d = 10: c = **2.3157**, so X(ε) ≥ exp(2.3157 · ε^{−2/3}).

Worked instance: to pin γ_1..γ_10 to ε = 10^{−3} requires
X ≥ exp(2.3157 · 100) = e^{231.6} ≈ 10^{100.6}. To ε = 10^{−6},
X ≥ exp(2.3157 · 10⁴) = 10^{10057}. This is the headline "primes are a
terrible channel to the zeros" statement, now with an explicit constant.

### 5.2 Comparison against the recorded empirical numbers

Source: `projects/mimo-mini-project/SPECTROSCOPY_GATE_RESULTS.md` (Gate 1
PASS, non-circular, null-tested), cited by `GOAL1_MAP.md` §"What we already
hold": MUSIC and a fair windowed periodogram recover 10/10 ζ zeros to
0.04–0.5 % relative error, at X = 3·10⁷ (the figure quoted for the χ_4 run
in the same block).

T = log(3·10⁷) = 17.2167, T^{3/2} = 71.44.

| quantity | T1 bound | Gate-1 empirical | ratio |
|---|---|---|---|
| max_j abs. error, d = 10 | √6·√2.0696/71.44 = **0.04933** | 0.5 % × 49.774 = **0.2489** | **5.05×** |
| abs. error at γ_1 | √6·√0.81076/71.44 = **0.03087** | 0.04 % × 14.135 = **0.00565** | **0.18×** |

Two readings, both worth recording:

1. **Gate G-b (spec §5) PASSES on the max_j statistic.** The gate requires
   T2's achieved constants within 10× of the CR bound. The observed 5.05×
   at d = 10 is inside that. T1 and T2 are telling a coherent story at the
   headline statistic.
2. **The γ_1 row VIOLATES the bound by 5.5×.** A single-realisation error of
   0.00565 sits below the claimed RMSE floor of 0.03087. This is not a
   contradiction *of a theorem* — the bound is a bound in model N2, and the
   Gate-1 run is a different (deterministic, N1) noise realisation on a
   different observable (prime counts, not the smoothed Möbius sum) — but it
   is strong evidence that **N2 overstates the interference at low height**.
   Diagnosis in §7.3. Recorded here, not buried.

**Status of this table after A2 (v3).** Both rows are **numerically
unchanged**: the bound column depends on the window through nothing (§5.1),
and the empirical column is an independent measurement. So the honest tension
at γ_1 is neither created nor relieved by A2, and it stays on the record at
the same size. Two things about it *do* change:

- The bound row now applies at Ω = 2Γ as a proved statement rather than as a
  local surrogate (§4.0(d)), so the comparison is a fairer one than v2 could
  offer — under v2's own audit the true bound at the approved cut was
  7.7·10^{−30} of the displayed value, which would have made the "violation"
  vacuous. Under A2 the tension is real and must be explained, not
  explained away. That raises, not lowers, the priority of GAP-11.
- GAP-11's remedy becomes cheap. The obstacle was that the frozen observable
  is a Gaussian-smoothed Möbius sum which the Gate-1 run did not compute;
  under (W′) the observable is (1/N)Σ_{k<N}M(k), one pass over a Möbius sieve
  to N = 3·10⁷. An N1 (deterministic) re-run of Gate 1 **on the actual
  frozen observable** is now a small job rather than a research task.

The lane_a ζ′ data is consistent with (4.3)'s use of the mean amplitude
scale: `lane_a/J_MINUS1_GONEK_REPORT.md` gives J_{−1}(T) = Σ_{0<γ≤T}
1/|ζ′(ρ)| with fitted slope 0.09278 vs the Gonek target 3/π³ = 0.096755
(ratio 0.949 at T = 9878, classified TOO EARLY). Since (4.3) uses only the
*first* moment of 1/|ζ′|, the divergent second moment (J_{−2}) never enters
the leading constant — see §7.2.

---

## 6. Gaps and obligations

Every step that is sketched rather than proved, tagged **ARISTOTLE-ABLE**
(finite / algebraic / analytic lemma with a self-contained statement,
suitable for Lean formalisation via Aristotle) or **FRONTIER** (needs human
or frontier judgement, or a modelling decision).

**Ledger state after amendment A2 (v3). 17 entries. 4 closed. 13 open.**

| version | entries | closed | open |
|---|---|---|---|
| v1 | 13 | 0 | 13 |
| v2 (after A1) | 15 | 1 (GAP-2) | 14 |
| **v3 (after A2)** | **17** | **4** (GAP-2, GAP-3, GAP-14, GAP-15) | **13** |

A2 **closes three** (GAP-3 (R6)/Lindeberg; GAP-14 band-edge leakage; GAP-15
low-ω positivity), **reduces but does not close one** (GAP-4, factor 98 →
factor 1.23–2.03), and **opens two of its own** (GAP-16, the VERIFIED
explicit-formula import no longer applies to the new window; GAP-17, the
finite-Γ rate behind the now-valid Lindeberg condition). Net 14 → 13 open.

The two new entries are the honest price of A2 and are listed at full weight,
not as footnotes to the three closures. Recording an amendment that closes
three gaps while quietly creating two would be exactly the bookkeeping this
ledger exists to prevent.

| # | Gap | Where | Tag |
|---|---|---|---|
| GAP-1 | The PSD convention (2.1) and the resulting constant 24 vs the literature's 12. Numerically checked to 3 digits, not proved. Needs a written lemma fixing convention and deriving (4.2) exactly, including the exact-N discrete version with the (N²−1) correction. | §2, Lemma 2 | **ARISTOTLE-ABLE** |
| ~~GAP-2~~ | **CLOSED — REPAIRED-BY-A1 (2026-08-15).** (R1) fails without band limitation; the repair (M4′) with Ω = 2Γ was **[ADDED]** by v1 and not in the frozen spec. The required amendment is now logged and owner-approved: G1_MODEL_SPEC **AMENDMENT A1**. (M4′) is a spec clause, cited in T1's hypothesis set (§2), and (R1) HOLDS. Two residues were *not* closed with it and are carried as new entries: the sub-question "is Ω = 2Γ the right cut?" → **GAP-14**; the positivity of the extended S_ε at the low end of the band → **GAP-15**. | §3 (R1), §1.4 | **CLOSED** |
| ~~GAP-3~~ | **CLOSED — REPAIRED-BY-A2 (2026-08-15).** (R6) failed under the frozen Gaussian window: a_γ ≍ e^{−πγ/4} made the first few tail terms dominate, Lindeberg ratio Λ(50) = 4.76 > 1, so ε was close to a small sum of random phases and the spec §3 claim "Gaussian-approximable" was known-false. Route (i) of the three v2 listed — replace W by a window with polynomially decaying M_W — is now **owner-approved and ENACTED as AMENDMENT A2** (clause W′, order-1 Riesz window). Under it a_γ ≍ γ^{−2}, the number of comparable interferers in [Γ,2Γ] is ≍ Γ log Γ/2π, and **Λ(Γ) = 6π/(Γ(log(Γ/2π)+⅓)) → 0**, measured 0.157 / 0.0248 / 3.5e−3 / 2.4e−4 at Γ = 50 / 200 / 10³ / 10⁴ (§3 (R6)). Routes (ii) and (iii) are no longer needed; v3 drops the "Gaussian surrogate" label. One residue is carried as a new entry: the finite-Γ rate → **GAP-17**. | §3 (R6) | **CLOSED** |
| GAP-4 | Lemma 1's local-flatness parameter δ. **REDUCED by A2, still open.** Under the frozen window log S_ε had slope −π/2 in ω and S_ε varied by a **factor 98.2** across the Lemma-1 band, so (4.1)'s "O(δ) negligible" was unjustified. Under clause (W′) the slope is **−4/ω + O(1/(ω log ω))**, the variation is at most e^{16πK/(ωT)} = **O(K/(ωT))** — the same order as the O(1/(ωT)) relative error Lemma 2 already carries, and vanishing in T — and it is measured at **1.23** (γ_d) to **2.03** (γ_1); effect on the final number +8 % ([I_N^{-1}]_{ωω}/local = 1.0794). That is a bounded, computable constant, not a negligible one, so the obligation stands: restate Lemma 1 with S_ε at the band edge and carry the explicit two-sided constant. The tag drops from FRONTIER to ARISTOTLE-ABLE because no modelling decision is left — only a finite estimate. Note the flatness worsens with window smoothness (δ ∝ 2(k+1)/(ωT) for Riesz order k), which is why A2 chose the mildest admissible k = 1 (G1_MODEL_SPEC §A2.2). Its long-range twin GAP-14 is closed. | §4 (4.1), Lemma 1 | **ARISTOTLE-ABLE** |
| GAP-5 | Lemma 3(a) cross-tone block-diagonality is proved by an order-of-magnitude sketch. A clean statement — "if T·Δγ ≥ 2πK then [I^{-1}]_{γγ} ≥ (1−CK^{-1})[I_j^{-1}]_{ωω} with C explicit" — is a finite linear-algebra + oscillatory-integral lemma. | §4, Lemma 3(a) | **ARISTOTLE-ABLE** |
| GAP-6 | Lemma 3(b) (data-processing: discrete-sample FIM ⪯ continuous FIM) is stated, not proved. Standard, but load-bearing for the spec's §2 claim that samples are "cheap". | §4, Lemma 3(b) | **ARISTOTLE-ABLE** |
| GAP-7 | Unbiasedness (R5). The T2 estimator (windowed periodogram + quadratic refinement) is biased at finite T, so T1 as stated does not directly bound it. Route: replace CR by a van Trees / Bayesian CR bound with a prior on Θ, or by a Ziv–Zakai bound (which also captures the threshold effect the periodogram exhibits). Changes constants. | §1.5, §3 (R5) | **FRONTIER** |
| GAP-8 | The numerical FIM verification (Lemma 2) and the Γ-amplitude table (§5.1) were computed this session by throwaway scripts and are not committed as receipts. Repo convention elsewhere in this program is a `*_RECEIPT.json` with hashes. **v2 adds a third uncommitted computation**: the exact band-limited 3×3 FIM of (4.0) used for the tables in §4.0(c),(d) (white-noise re-verification of 24, ρ_d at Ω = 2Γ, and the Ω-sweep). **v3 adds a fourth and largest**: `scratchpad/a2_verify.py` + `scratchpad/a2_b1.py`, which produce every A2 figure in §3 (R6), §4.0(c),(d),(e), §5.1 — the Lindeberg ratios, the (B1) measurement λ_max(I_N^{-1}I_R) per tone and per Ω, the coloured band-limited factor-24 check, the flatness table and the ϑ_min sweep. These scripts are *self-validating* in one useful respect (they reproduce v2's independent Gaussian numbers to 5 digits before being applied to (W′)), and a **second, independently written implementation — `lane_t/t1_verify.py`, also uncommitted — reproduces every A2 figure to all digits reported** (§4.0 provenance note). Two agreeing implementations is strong evidence but still not a receipt: no committed script, no `*_RECEIPT.json`, no hashes, and the scripts do not live under version control. Same obligation, now four items, and the v3 ones are load-bearing for three gap closures — so this entry is promoted in priority even though its text is unchanged in kind. | §3, §4, §4.0, §5.1 | **ARISTOTLE-ABLE** (reproduce as a committed script + receipt) |
| GAP-9 | (M4)'s stationary extension to ω = γ_j: the whole content of "S_ε(γ_j)". A realisation has no interference atom at γ_j, so the model assigns noise where a fixed zero configuration has none. Justifiable as a minimax-over-shifts idealisation, but not justified here. This is the honest reason the spec's N3 (minimax over admissible zero configurations) exists. | §1.4 (M4), §7.3 | **FRONTIER** |
| GAP-10 | The amplitude truncation of (M3) at a quantile q: the sensitivity report the spec §3 promises has not been produced. Argued moot for the leading constant in §7.2, but not shown. **Raised in importance by A2**: the truncation is what keeps the Lindeberg summands uniformly bounded, so it is now load-bearing for the GAP-3 closure and its level q enters GAP-17's Berry–Esseen constant. | §1.4 (M3), §7.2, GAP-17 | **CLOSED-WITH-CAVEAT 2026-08-26** — sweep run (T1_GAP10_TRUNCATION_SWEEP.md, receipt banked, cold-re-run verified): the leading constant and Λ(50) are EXACTLY q-invariant because v3's machinery uses the mean-field amplitude convention r_γ ≡ 1 (§7.2 mootness borne out, stronger than claimed); the truncation is load-bearing ONLY through GAP-17's Berry–Esseen constant, where max 2a_γ/σ grows 1.77 → 17.7 → ∞ over q = 0.90 → 0.999 → 1 under a labelled Pareto(α=2) nearest-analogue tail (no per-zero r_γ export exists in-repo — that caveat carries to GAP-17). |
| GAP-11 | The γ_1 empirical violation (§5.2, row 2). Needs either an N1 (deterministic) re-run of Gate 1 on the *actual* frozen observable y(t) of §1.1, or an explanation why the comparison is not apples-to-apples. Currently the latter is asserted. **Changed by A2 in both directions** (§5.2): the tension is *sharper*, because at Ω = 2Γ the bound is now proved rather than a local surrogate (under v2's audit the true bound there was 7.7·10^{−30} of the displayed value, which made the violation vacuous); and the remedy is *cheap*, because the new observable is (1/N)Σ_{k<N}M(k), one pass over a Möbius sieve to N = 3·10⁷ rather than a Gaussian-smoothed sum. Highest-value open item after GAP-16. | §5.2 | **FRONTIER** |
| GAP-12 | Prior-art tripwire G-c: spec §5 requires a re-scout "at first-draft time". This is first-draft time. `lane_c/S2_PRIOR_ART.md` (2026-08-14, NO-COLLISION) is one day old and its own limitations section flags that a negative on "Cramér–Rao Riemann zeros" is weaker than a systematic review. Re-scout not run for this draft. **A2 widens the required search**: the observable is now the order-1 Riesz/Cesàro mean of Mertens, a classical object with its own literature (Riesz means of 1/ζ, ψ_1(x)), so the re-scout must cover that as well as the estimation-theoretic angle. | §5 of spec | **FRONTIER** |
| ~~GAP-14~~ | **CLOSED — REPAIRED-BY-A2 (2026-08-15).** Band-edge leakage. Under the frozen window (M4′) made the Fisher information finite but not small: 1/S_ε grew like e^{+πω/2} across the pass band while each tone's window-truncation tails decay only like 1/(ν−γ_j), so the information was dominated by the band edge — measured λ_max(I_N^{-1}I_R) = 1.73·10^{+29} at γ_d, band-limited [I^{-1}]_{ωω} = 7.7·10^{−30} of the local 24-value, and the admissible band was only Ω = γ_d + O(1). Route (i) of the three v2 listed — amendment A2, polynomial M_W — is **ENACTED**. Under clause (W′) 1/S_ε grows only like ν^4, and **(B1) HOLDS at the approved cut Ω = 2Γ**: λ_max(I_N^{-1}I_R) = **0.0858** ≤ K^{-1} = 0.25 at γ_d, [I^{-1}]_{ωω} = **0.9943** of the local value, admissible out to Ω ≈ 400 = 8Γ (§4.0(d)). Routes (ii) (narrow Ω) and (iii) are no longer needed and the open question of G1_MODEL_SPEC §A1.4 ("is Ω = 2Γ the right cut?") is answered YES under A2. Rider carried in §2 and §4.0(d), not dropped: as an inequality (B1) still fails at the *lowest* tone γ_1 (λ_max = 0.587) and is marginal at γ_2 (0.220); the resulting deficits (max 0.257) are within T1's own declared O(K^{-1}) = 0.25 with implied constant ≈ 1.03, and the max_j statement is attained at j = d where the deficit is 0.6 %. | §2 (B1), §4.0(d) | **CLOSED** |
| ~~GAP-15~~ | **CLOSED — REPAIRED-BY-A2 (2026-08-15).** Positivity of the extended S_ε at the low end of the band: (M4′)'s pass band contains \|ω\| < 2π where a_{\|ω\|}²log(\|ω\|/2π) is **negative**, and taking it to 0 reopened a low-frequency copy of the (R1) failure. Amendment A2 adds clause **(M4″)**: S_ε(ω) := a_{\|ω\|}²·max{log(\|ω\|/2π), ϑ_min} with ϑ_min := log(γ_1/2π) = 0.81076. Under (W′), a_ω is continuous and strictly positive on the band, so the floor makes S_ε bounded below by a positive constant on all of [−Ω,Ω] and the (R1) repair is complete. Sensitivity measured (§4.0(e)): sweeping ϑ_min over [0.05, 2.0] moves [I^{-1}]_{ωω} by 4·10^{−4} relative. **NB the v2 benignity argument did not survive A2** and was replaced, not reused: it relied on a_ω² being larger at small ω by e^{π(γ_1−ω)/2} (3.7·10⁹ at ω=1), which under (W′) is only ≈ 200. | §4.0(e), Prop. 4.4 | **CLOSED** |
| **GAP-16** | **NEW (v3, created by amendment A2).** The explicit formula for the new window has not been re-derived. `imported_farey_now/Smoothed_Dwf_explicit_formula_VERIFIED.md` is verified **for the Gaussian window** (M_W = ½Γ(s/2), R₀ = −2, \|E_A(N)\| ≤ C_{A,W}N^{−A} for all A under H1–H3); under clause (W′) it is out of scope. What is owed: the order-1 Riesz explicit formula with M_W(s) = 1/(s(s+1)) — arithmetic side Σ_{n≤N}μ(n)(1−n/N) = (1/N)Σ_{k<N}M(k) (finite and exact), residues R₀ = −2 at s = 0 **and the new R_{−1}(N) = 12/N at s = −1**, trivial-zero term R_triv, absolute convergence of the zero sum from J_{−1}(T) = O(T) (Gonek–Hejhal; lane_a slope 0.0928 vs 3/π³ = 0.0968), and the contour-shift remainder, which is now only polynomially small rather than superpolynomially. §1.1 and G1_MODEL_SPEC §A2.1 state the target. **Status 2026-08-15: DERIVATION WRITTEN, LEAN CORE DISPATCHED, NOT CLOSED.** `lane_t/T1_GAP16_RIESZ_IMPORT.md` derives the order-1 Riesz analog (Prop. R): R₀ = −2 survives, the new s = −1 pole gives R_{−1}(N) = 12/N, the trivial zeros become **simple** poles so R_triv = Σ N^{−2n}/((−2n)(1−2n)ζ′(−2n)) = O(N^{−2}) with **no log N**, and the contour-shift remainder is O_A(N^{−A}) for fixed A ∈ (1,2). Numerically validated (non-rigorous, mpmath, K ≤ 200 zeros, N ≤ 2·10⁴: residual monotone in K, 5·10^{−3} at N = 2·10⁴; the 12/N term is required). The finite/algebraic core — Cesàro identity, the k=1 Mellin integral, the M_W residue algebra, R₀ = −2, R_{−1} = 12/N, simple-pole trivial term — is dispatched as 7 sorry-stubbed statements, `projects/aristotle_dispatch_v21/RieszImport.lean`, Aristotle project 24c6e3df-76fd-43d0-a052-b6ddf10d6084. **Status 2026-08-26: CLOSED AT CITATION+LEAN STANDING.** Aristotle v21 returned all 8 finite-core theorems sorry-free (harvested, locally re-elaborated, axioms clean); the luna frontier review (T1_GAP16_REVIEW_LUNA.md) confirmed the residue calculus and required six repairs, all applied to T1_GAP16_RIESZ_IMPORT.md + G1_MODEL_SPEC.md (RH added to Prop. R; J_{−1} notation corrected to Σ1/\|ζ′(ρ)\|² with the Cauchy–Schwarz/dyadic argument; citations corrected to Hardy–Riesz Ch. IV/VII§2 + Hardy–Littlewood Acta 41 + Titchmarsh §14.16/§14.27 + Ng Lemmas 3–4; E_A := I_{−A} − R_triv; ζ′(−2n) asymptotic and leading coefficient fixed). **Mandatory disclosure (carried wherever Prop. R is consumed):** Proposition R is conditional on RH, simplicity of every nontrivial zero, and the conjectural Gonek–Hejhal bound J_{−1}(T) := Σ_{0<γ≤T}\|ζ′(½+iγ)\|^{−2} = O(T). Lean checks only the eight finite/algebraic lemmas in RieszImport.lean; the Riesz–Perron inversion, meromorphic residue calculus, absolute convergence of the zero and trivial-zero sums, the RH zero-avoiding contour shift, and the O_A(N^{−A}) remainder remain cited classical analysis and are not formalized in Lean. Empirical validation: the GAP-11 N1 re-run matched Prop. R's γ₁ amplitude to 0.26% at N = 3·10⁷. | §1.1, §A2.1/§A2.5 | **CLOSED (citation+Lean standing, disclosure carried)** |
| **GAP-17** | **NEW (v3, created by amendment A2).** Rate behind the now-valid Lindeberg condition. A2 makes Λ(Γ) = 2a_Γ²/σ²(Γ) → 0 (closing GAP-3), but Lindeberg gives convergence, not a rate, and at the concrete operating point of §5 (Γ = 50) the ratio is **0.157**, not negligible — a Berry–Esseen-type error plausibly O(√Λ) ≈ 0.4. What is owed: a quantitative CLT for ε = 2Σ_{γ>Γ}a_γcos(γt+φ_γ) with an explicit total-variation or Kolmogorov distance in Γ, and a statement of how that error propagates into the CR bound (a Gaussian-surrogate mis-specification term). Interacts with **GAP-10**: (M3)'s quantile truncation is exactly what keeps the summands uniformly bounded, so the Berry–Esseen constant depends on the truncation level q. | §3 (R6) | **ARISTOTLE-ABLE** (Berry–Esseen for a random-phase almost-periodic sum) |
| GAP-13 | Whether c_d should carry a genuine d-dependence. Here it does not (Lemma 3 makes blocks independent). If (M5) is relaxed toward the true zero spacing 2π/log(γ/2π), which shrinks with height, d-dependence returns through the resolution condition: T ≥ K log(γ_d/2π) is needed, i.e. X ≥ (γ_d/2π)^K. Worth stating as a second, separate resource bound. | §2 | **FRONTIER** |

---

## 7. Discussion of the known complications (three, plus the v3 amendment audit)

### 7.1 The Gaussian smoothing suppressed everything — RESOLVED by A2

|M_W(½+iγ)| = ½|Γ(¼+iγ/2)| ≍ √(2π)/2 · (γ/2)^{−1/4} e^{−πγ/4}. From
γ_1 = 14.13 to γ_10 = 49.77 the amplitude dropped by 13 orders of magnitude
(§5.1). Consequences: (i) the *raw* SNR at γ_10 was astronomically bad, so
the frozen observable was a poor practical instrument even though the T1
*rate* is clean; (ii) GAP-3, GAP-4 and GAP-14 all traced to this one decay.
v1 recommended a W with polynomially decaying M_W as "the highest-value
change to the frozen model"; v2 recorded it as proposed amendment A2.

*Status 2026-08-15, after the owner ruling: **A2 is approved and enacted**.*
Clause (W′) gives |M_W(½+iγ)| = ((¼+γ²)(9/4+γ²))^{−1/2}, and the three
symptoms resolve as follows:

| symptom | outcome |
|---|---|
| GAP-3 (Gaussianity) | **CLOSED** — Λ(Γ) = 6π/(Γ(log(Γ/2π)+⅓)) → 0 (§3 (R6)) |
| GAP-14 (band-edge leakage, long range) | **CLOSED** — λ_max(I_N^{-1}I_R) = 0.0858 ≤ 1/K at Ω = 2Γ (§4.0(d)) |
| GAP-4 (local flatness, short range) | **REDUCED** 98.2 → 1.23, not closed (Lemma 1 note) |
| raw instrument SNR | amplitude at γ_10 up **13.8 orders**; dynamic range over γ_1…γ_10 down from 13 orders to a factor **12.3** (§5.1) |

The last row is the one that matters outside T1. The frozen observable was
not measurable at γ_10 by any means; the amended one is a plain Cesàro mean
of Mertens, computable by one sieve pass, with all ten target tones within a
factor 12 of each other in amplitude. The *rate* T^{−3/2} and the constant √6
are unchanged — A2 does not make the channel less inefficient, it makes the
instrument usable at the precision the channel allows.

Note the ordering the two amendments expose: **A1 makes the model
non-singular; A2 makes the §2 constants true at A1's approved band Ω = 2Γ.**
Neither alone suffices, and neither changes what T1 claims.

### 7.2 The heavy tail (falsification gate G-a) is largely defused

Spec §5 gate G-a threatens demotion of T1 if S_ε "cannot be bounded" because
of the divergent second moment of 1/|ζ′(ρ)| (Gonek–Hejhal J_{−2}).
Proposition 4.4 shows S_ε enters T1 only through the ratio
S_ε(γ_j)^{1/2}/a_{γ_j}, in which a cancels identically. What survives is
log(γ_j/2π) — the zero *density*, which is a classical theorem, not an
empirical amplitude law. So:

- the leading constant of T1 is **amplitude-free**;
- the heavy tail affects only (M3)'s role inside the Gaussian
  approximation (GAP-3) and the fluctuation of realised S_ε about its mean;
- lane_a's J_{−1} data (first moment, finite, Gonek slope 3/π³) is the only
  moment T1 uses, and it is the one that converges.

**Verdict on G-a: does not fire for the leading constant.** Under v1/v2 it
still fired for the Gaussian-approximability claim (GAP-3). **Under amendment
A2 it no longer fires at all**: the Lindeberg condition holds (§3 (R6),
GAP-3 CLOSED), subject only to the finite-Γ rate obligation GAP-17. See
G1_MODEL_SPEC §A2.8.

### 7.3 Why N2 is not conservative at low height (the γ_1 violation)

Model (M4) puts noise power a_{γ_1}² log(γ_1/2π) at ω = γ_1. The real
configuration has *no* zero within ±6.9 of γ_1, and the nearest interferer
γ_2 is 6.89 away — far outside the window resolution 2π/T ≈ 0.36 at
X = 3·10⁷. So a real estimator at γ_1 faces almost no interference, and beats
the N2 floor. This is exactly the observed 0.18× ratio in §5.2.

Interpretation: **N2 is a good model at heights where the zero spacing is
comparable to the window resolution (log(γ/2π) ≳ T), and pessimistic below
that.** With T = log X ≈ 17 and log(γ/2π) ≈ 2 for the first ten zeros, we are
deep in the pessimistic regime. T1 is therefore honest as a statement about
the model but should not be quoted as a bound on what a real computation can
achieve for the lowest zeros. The N3 (minimax) programme of spec §3 is the
correct fix, and this analysis is the concrete argument for prioritising it.

**Re-checked under A2 (v3): the diagnosis holds, and one of its two legs is
now stronger, the other weaker.** The argument above has two legs — spacing
(the nearest interferer is 6.89 away, far outside the resolution 2π/T ≈ 0.36)
and amplitude. The spacing leg is window-independent and stands. The
amplitude leg *reverses sign*:

| | frozen Gaussian W | (W′) Riesz k=1 |
|---|---|---|
| \|M_W(½+iγ_2)/M_W(½+iγ_1)\| | 4.05·10^{−3} (interferer 250× weaker) | **0.454** (comparable) |

Under the frozen window the nearest interferer was 250× weaker than the
target, so N2's assignment of interference power a_{γ_1}²log(γ_1/2π) at
ω = γ_1 was doubly unrealistic. Under (W′) the neighbouring zeros are of
comparable amplitude, so **N2's premise is now much closer to true and the
model is correspondingly less pessimistic at low height** — the amendment
makes the setting stricter, not laxer. The residual pessimism is the spacing
leg alone, i.e. GAP-9's stationary-extension idealisation, which is exactly
what N3 exists to replace. The empirical tension of §5.2 is therefore not
explained away by A2; it is narrowed to a single identified cause.

### 7.4 Did A2 make the theorem easier? — the self-serving audit

A second post-freeze amendment, approved post hoc, which converts a
29-orders-of-magnitude failure into a pass, has to answer this directly.
Restated from G1_MODEL_SPEC §A2.6, with the numbers that live in this draft:

1. **No displayed constant changed.** c_d = √6, (T1-c), (T1-d),
   c = 1.6944 (d=1), 2.3157 (d=10), bound 0.04933 at d = 10 — all identical to
   v1 and v2. The mechanism is structural: Prop. 4.4 gives
   S_ε(γ)/a_γ² = log(γ/2π), and the window cancels identically for *any*
   admissible W. A2 could not have inflated these even if it had been chosen
   to. They were derived in v1, before either defect was known.
2. **The noise model got heavier-tailed, not lighter.** The interference
   floor now decays like ω^{−4} instead of e^{−πω/2}; at every frequency
   above the targets the model carries more interference power relative to
   the signal than the frozen model did. A2 grants the estimator a noisier
   world.
3. **What did move by 29 orders is the *measured* bound at Ω = 2Γ**
   (7.7·10^{−30} → 0.9943 of the local value). That is the deletion of a
   modelling artifact, not the purchase of a theorem. The frozen model
   asserted that zeros above height Ω contribute super-exponentially little
   noise while the targets' window-truncation sidelobes persist only
   polynomially — an arbitrarily quiet channel at the band edge through which
   *the model*, not the primes, let an estimator read the ordinates. It is
   the same pathology as the infinite-information singularity A1 removed
   (§3 (R1)), one band-width down.
4. **The motive was independent of the constant.** A2 was recommended in
   v1 §7.1 for GAP-3 — the falsity of the Gaussian-approximability claim,
   which has nothing to do with band edges, Ω, or leading constants. GAP-14
   did not yet exist. The leakage repair is a consequence of the fix, not its
   reason.
5. **A2 was not free.** It voids the VERIFIED explicit-formula import
   (GAP-16, now the largest open item), makes absolute convergence of the
   zero sum conditional on J_{−1}(T) = O(T), and leaves a rate obligation
   behind the CLT (GAP-17). Net open gaps fell only 14 → 13.
6. **Two things A2 did not fix, stated where they can be seen.** GAP-4
   (flatness) is reduced by ≈ 80× but open; the γ_1 empirical tension of
   §5.2 is numerically unchanged and, if anything, harder to dismiss now
   (§5.2, §7.3).

---

## 8. What is claimed, and what is not

**Claimed.** In model N2 = (M1)–(M5) with spec clauses (M4′) (amendment A1)
and (M4″), (W′) (amendment A2), *and under the leakage hypothesis (B1)*, for
any unbiased estimator **of the band-limited record y_Ω**:
max_j RMSE(γ̂_j) ≥ √6 (log(γ_d/2π))^{1/2}(log X)^{−3/2}, hence
X(ε) ≥ exp((6 log(γ_d/2π))^{1/3} ε^{−2/3}). The amplitudes cancel — and
cancel for *any* admissible window, which is why A2 changed no constant. The
Fisher-information computation is (4.0)–(4.3) with the constant 24 now
numerically confirmed **three** times (time-domain white, v1; band-limited
frequency-domain white, v2 §4.0(c); band-limited **and coloured by the actual
(W′) model S_ε at the approved cut**, v3 §4.0(c), giving 0.9943 × the local
value), and S_ε(γ_j) unchanged by the band-pass because the tones are
interior with margin ≥ Γ (§4.0(a),(b)).

**New in v3, and the most important line here:** **(B1) now HOLDS at the
approved cut Ω = 2Γ** — measured λ_max(I_N^{−1}I_R) = 0.0858 ≤ K^{−1} = 0.25
at γ_d, admissible out to Ω ≈ 8Γ (§4.0(d)) — so at Ω = 2Γ the displayed
constants are a proved bound for the M4′ estimator class, not merely the
constants of a local surrogate. That is the single substantive change from
v2, and it is what amendment A2 was approved to buy.

**Not claimed.** Nothing unconditional about ζ. Nothing about biased
estimators. Nothing about heights where (M5) fails. No claim that the bound
applies to the Gate-1 numerics, which ran a different observable under N1.
No claim that the bound holds for estimators seeing the *unrestricted* record
y — the M4′ restriction does not transfer upward (§1.5), and A2 does not
retire M4′ (§3 (R1)). No claim that (B1) holds *at the lowest tone* γ_1 at
Ω = 2Γ: as an inequality it fails there (λ_max = 0.587), and what is claimed
instead is the measured deficit 0.257, inside T1's own O(K^{−1}) (§4.0(d)).
**And a claim v2 could make that v3 cannot make for free:** the line-spectrum
form (1.1) itself. Under the frozen window it rested on a VERIFIED import;
under (W′) that import is out of scope and the explicit formula for the
order-1 Riesz mean is stated but **not re-derived in this repo** (GAP-16).
Finally, the Gaussian approximation in (M4) is now *supported* (Lindeberg
holds, GAP-3 closed) but not *quantified* — no Berry–Esseen rate is claimed
at the finite Γ = 50 of §5, where the Lindeberg ratio is 0.157 (GAP-17).

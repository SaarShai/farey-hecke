# T1 — Cramér–Rao lower bound in the frozen model N2

Draft v2, 2026-08-15. Lane T (T-opus). Status: REVISED under owner-approved
amendment A1; not adversarially reviewed, not machine-verified.
Ticket: `plans/wayfinder/rh-goals/tickets/sample-complexity-t1.md`.
Model authority: `research_notes/rh_goals_2026-08-14/G1_MODEL_SPEC.md` (v0,
FROZEN 2026-08-14, **+ AMENDMENT A1 of 2026-08-15** which adds clause M4′).

**Changes v1 → v2.** (i) Band limitation (M4′) is now a *spec clause* via
amendment A1, cited in the hypothesis set of T1 instead of being an
undeclared addition — GAP-2 CLOSED. (ii) v1's claim that band-limiting gives
a bound valid for the unrestricted record is **wrong in direction** and is
corrected: M4′ restricts the estimator class (§1.5, §3 (R1)). (iii) The
Fisher computation is re-derived under the band limit (new §4.0): the tones
are interior, S_ε(γ_j) is unchanged, and the constant 24 survives — but the
band-edge *leakage* term does not vanish at Ω = 2Γ, so T1 now carries an
explicit leakage hypothesis (B1) and a new GAP-14. (iv) New GAP-15
(positivity of the extended S_ε at low ω inside the band). (v) (R6)/GAP-3
remains OPEN with a pointer to proposed amendment A2 (not approved, not
enacted).

**Honest label carried throughout:** this is a Cramér–Rao bound *in model N2*.
N2 contains stochastic hypotheses about the zeros that are not theorems. The
result is a statement about the model, not an unconditional statement about
ζ. G1_MODEL_SPEC §3 requires exactly this labelling.

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

**Two caveats the reader must carry from here (both sharpened in v2).** The
bound is for the *band-limited* estimator class of spec clause M4′
(amendment A1) — it is not a bound on estimators that see the unrestricted
record. And within that class it holds only when the band-edge leakage
hypothesis (B1) of §2 holds; at the approved cut Ω = 2Γ, with the frozen
Gaussian window, **(B1) fails by ~29 orders of magnitude** (§4.0, GAP-14).
The displayed constants are therefore the correct constants of the *local*
(white-noise-equivalent) problem, and T1 is proved only for bands narrow
enough that (B1) holds.

---

## 1. The frozen model, restated

Restated from `G1_MODEL_SPEC.md` §1–§3. Where I paraphrase, the spec's own
wording is quoted; where I add anything the spec does not say, it is marked
**[ADDED]** and appears again in §6.

### 1.1 Observable (spec §1, verbatim-faithful)

Import: `research_notes/imported_farey_now/Smoothed_Dwf_explicit_formula_VERIFIED.md`
(Gaussian W(x) = e^{−x²}, M_W(s) = ½Γ(s/2), R₀ = −2). For t = log N,

  y(t) := e^{−t/2} · [ Σ_{n≥1} μ(n) W(n/e^t) − R₀ − R_triv(e^t) ]
        = 2 Σ_{γ>0} a_γ cos(γ t + φ_γ) + ε(t),                      (1.1)

  a_γ = | M_W(½+iγ) / ζ′(½+iγ) |,  φ_γ = arg( M_W(½+iγ)/ζ′(½+iγ) ),

and ε(t) collects the truncation error E_A, which the imported derivation
bounds by |E_A(N)| ≤ C_{A,W} N^{−A} for every A > 0 under its hypotheses
H1–H3. Under RH, (1.1) is *exactly* a multi-tone line spectrum in t whose
frequencies are the zero ordinates. Spec §1: "this is the model we freeze."

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
- **(M5) Resolvability.** T · min_{j≠k} |γ_j − γ_k| ≥ 2πK for a constant
  K ≥ 4, and T · (Γ − γ_d) ≥ 2πK.

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
  I = I_N + I_R). Assume **I_R ⪯ K^{-1} I_N**. The diagnostic quantity is

    ρ_j := (3/2π²) · S_ε(γ_j) / ( (Ω − γ_j)² · T · S_ε(Ω) ),          (2.2)

  and (B1) requires ρ_j ≲ K^{-1}. **(B1) is FALSE at Ω = 2Γ under the frozen
  Gaussian window** — §4.0 measures ρ_d ≈ 7·10^{28} — so T1 below is proved
  for bands satisfying (B1) and is, at the approved cut, an *unproved*
  statement. This is GAP-14, opened by the v2 audit.

> **Theorem T1 (CR lower bound, model N2 as amended by A1).**
> Assume (RH), model N2 = (M1)–(M5) **with clause (M4′)**, the resolvability
> constant K ≥ 4, and the leakage hypothesis (B1). Let θ̂ be any unbiased
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
> **Evaluation of S_ε (Prop. 4.4).** Under (M1)–(M4),
>
>   **S_ε(ω) = a_{|ω|}² · log(|ω|/2π)** for all ω,               (T1-b)
>
> so the amplitudes cancel in (T1-a) and
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
∫ |m̂_θ(ω) − m̂_{θ'}(ω)|² / S_ε(ω) dω < ∞. Since (T1-b) gives S_ε(ω) =
a_ω² log(ω/2π) with a_ω ≍ e^{−πω/4} (§7.1), 1/S_ε grows *doubly* fast
(e^{+πω/2}) while the numerator decays only polynomially. **The integral
DIVERGES. (R1) FAILS as literally stated.**

  *Consequence and repair.* This is not a defect of the CR argument but of
  extending (M4) to arbitrarily high ω. The observable's high-frequency
  content is superpolynomially suppressed by the Gaussian smoothing, so the
  model noise is "too clean" at high ω and the model becomes *singular*
  (θ perfectly identifiable, information infinite, CR bound ≡ 0) if all
  frequencies are admitted. The frozen model must therefore be band-limited.
  The repair is spec clause **(M4′)** (§1.4): ideal band-pass onto
  ω ∈ [−Ω,Ω], Ω := 2Γ.

  **Status: REPAIRED. (R1) HOLDS under (M4′).** On the pass band S_ε is
  bounded below by the positive constant S_ε(Ω) = a_Ω² log(Γ/π) (using
  Ω = 2Γ, and modulo the low-frequency positivity convention of GAP-15),
  1/S_ε is bounded, the Cameron–Martin integral is finite, and all P_θ are
  equivalent Gaussian measures on the band.

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

  *What A1 does not do.* Making the information finite is not the same as
  making the local white-noise computation of §4 correct. At Ω = 2Γ the
  information is finite but astronomically larger than the local value; see
  §4.0 and GAP-14.

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

**(R6) Gaussianity of ε (the approximation that (M4) makes). — OPEN, see
proposed amendment A2.**
Not a regularity condition for CR, but a validity condition for the model.
ε = 2Σ_{γ>Γ} a_γ cos(γ t + φ_γ) is a sum of infinitely many independent
(under M1) bounded terms; a Lindeberg condition would give a CLT provided no
single term dominates. **CHECK:** a_γ ≍ e^{−πγ/4} decays geometrically, so
the *first* few terms above Γ dominate the sum absolutely — the Lindeberg
ratio does **not** vanish. **(R6) FAILS: ε is not close to Gaussian; it is
close to a small sum of a few random phases.** This is the single most
serious honest defect of T1 as drafted. See §6, GAP-3 (FRONTIER) and §7.3.

  *Status after A1: STILL OPEN, and deliberately not amended.* Band
  limitation is orthogonal to Gaussianity, so A1 does not touch this. The
  repair recommended by this draft — replace W by a window whose Mellin
  transform decays polynomially — is recorded in G1_MODEL_SPEC §A1.5 as
  **proposed amendment A2, AWAITING OWNER RULING**. It is *not* approved and
  *not* enacted; nothing in v2 assumes it. Until a ruling, the frozen spec's
  §3 claim that the interference is "Gaussian-approximable" stands as
  KNOWN-FALSE AS WRITTEN, and T1 is labelled "CR bound in the **Gaussian
  surrogate** of N2".

**Summary of the regularity audit.** (R2),(R3),(R4) hold. (R1) failed as
stated and is now REPAIRED by spec clause (M4′) (amendment A1) — at the cost
of restricting the estimator class, which is a real cost and is declared in
§1.5, not a free reduction. (R5) is a restriction on the estimator class,
declared. (R6) fails; the Gaussian step is a genuine modelling assumption,
not an approximation theorem, and T1 must be read as "CR bound in the
Gaussian surrogate of N2" — proposed amendment A2, awaiting owner ruling.
Separately, (R1)'s repair is *qualitative*: it restores absolute continuity
but leaves the information far above the local white-noise value at the
approved cut Ω = 2Γ (§4.0, GAP-14).

---

## 4. Fisher information — computed

### 4.0 Re-derivation under the band limit (M4′) — verification, not assertion

Everything below §4.1 was computed in v1 without a band limit. Clause (M4′)
changes the ambient space, so each step is re-checked here against
Ω = 2Γ. Under (M4′) the Fisher information is the Gram matrix

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

**(b) S_ε(γ_j) is unchanged.** An ideal band-pass multiplies the spectrum by
1_{|ν| ≤ Ω}; it leaves the spectral density *inside* the band pointwise
untouched. By (a), γ_j is interior, so S_ε(γ_j) in (T1-a)/(T1-b) is exactly
the pre-amendment value a_{γ_j}² log(γ_j/2π), and the amplitude cancellation
of §0 and Prop. 4.4 is unaffected. **Verified.** (Two riders: the low-ω end
of the band needs a positivity convention, GAP-15; and (M4)'s extension of
S_ε to ω = γ_j, where no interference atom lives, is still GAP-9.)

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

**(d) What does NOT survive: the band-edge leakage term.** (a)–(c) say the
band-pass loses little *signal*. They do not say the retained out-of-band
frequencies are uninformative. Split I = I_N + I_R as in (B1). On R the
noise is exponentially quieter than at the tone: with the frozen Gaussian W,
1/S_ε(ν) ≍ e^{+πν/2}, while |∂̂_ω m(ν)|² ≍ A²T²/(4(ν−ω)²) decays only
quadratically. The ν-integral in (4.0) is therefore dominated by the band
EDGE, giving

  I_R,ωω ≈ A²T² / ( 4π² (Ω−ω)² S_ε(Ω) ),
  ρ_ω := I_R,ωω / I_N,ωω ≈ (3/2π²) · S_ε(ω) / ( (Ω−ω)² T S_ε(Ω) ),        (4.0′)

which is (2.2). Because S_ε(ω)/S_ε(Ω) ≍ e^{π(Ω−ω)/2}, ρ grows
*exponentially* in the band width Ω − ω and only the T^{-1}(Ω−ω)^{-2} prefactor
opposes it. Evaluated at the approved cut Ω = 2Γ with the §5 numbers:

| Γ | Ω = 2Γ | S_ε(γ_d) | S_ε(Ω) | ρ_d (4.0′) | measured [I^{-1}]_{ωω} ÷ 24S_ε(γ_d)/(A²T³) |
|---|---|---|---|---|---|
| 51.234 (M5-tight) | 102.467 | 7.23e−35 | 7.68e−71 | 3.0e+30 | 1.6e−31 |
| 50 | 100 | 7.23e−35 | 3.71e−69 | 6.8e+28 | 7.7e−30 |

(The last column is the exact band-limited 3×3 FIM of (4.0) inverted
numerically with the model S_ε, same session, same script as (c).) Analytic
diagnostic and measurement agree to within a factor ≈ 2 at the approved cut.

**Conclusion of the re-derivation.** At Ω = 2Γ the true CR bound in the
amended model is smaller than the claimed (T1-a) by ~29 orders of magnitude:
**(B1) FAILS at the approved cut, and T1's constants are therefore the
constants of the local problem, not a proved bound for the M4′ class at
Ω = 2Γ.** The band width that preserves them, measured the same way with the
tone at γ_d:

| Ω − γ_d | 0.5 | 1 | 1.5 | 2 | 3 | 4 | 6 | 10 |
|---|---|---|---|---|---|---|---|---|
| [I^{-1}]_{ωω} ÷ local 24-value | 1.158 | 1.001 | 0.870 | 0.781 | 0.566 | 0.357 | 0.061 | 4e−4 |

i.e. Ω = γ_d + O(1) — not 2Γ. This is **GAP-14**. It is the same root cause
as GAP-3 and GAP-4 (the Gaussian window's exponentially decaying Mellin
transform), and proposed amendment A2 would control it polynomially. The cut
Ω = 2Γ is the one the owner approved, so it is what this draft assumes;
changing it needs a further amendment (G1_MODEL_SPEC §A1.4).

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

Under (M2) and (T1-b), S_ε varies over a band of width 4πK/T by a factor
1 + O(K/T) since d/dω log S_ε = −π/2 + O(1/ω); so δ = O(K/T) — negligible.
**[This δ estimate is the one place where the exponential decay of a_ω hurts:
π/2 per unit ω is not small. With K = 4, T = 17 the band is width ≈ 3 and
δ ≈ e^{π·3/2·(1/2)} — NOT negligible. See GAP-4.]**

**[Scope warning, added in v2.]** Lemma 1 is stated for u, v *supported* in
the neighbourhood of ±γ_j. The derivatives ∂_j m_θ are time-limited to [0,T]
and hence have tails at every frequency, so (4.1) is the information of the
near-tone part I_N only. Using (4.1) as the whole Fisher information is
exactly hypothesis (B1), which fails at Ω = 2Γ — §4.0(d), GAP-14. GAP-4
(the δ inside the neighbourhood) and GAP-14 (the leakage outside it) are the
short-range and long-range halves of one defect.

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

**Under (M4′).** (4.3) is derived for |ω| > Γ from the actual interference and
then extended to all ω by (M4). The band-pass does not modify it inside the
band, and by §4.0(a),(b) the evaluation point γ_j is interior, so
S_ε(γ_j) = a_{γ_j}² log(γ_j/2π) stands exactly as in v1. Two riders that the
band limit makes visible:

- the pass band now explicitly includes |ω| < 2π, where (4.3) is **negative**
  (log(|ω|/2π) < 0) and therefore not a spectral density. (M4)'s "extended to
  all ω" needs a positivity convention there. This is **GAP-15**. It is
  benign but must be written: any floor S_min contributes to I_{γ_jγ_j} a
  relative term ≈ 3 S_ε(γ_j)/((γ_j − 2π)² T S_min), which at γ_1 = 14.1347,
  T = 17.2167 is 2.8·10^{−3}·S_ε(γ_1)/S_min — and since a_ω² is *larger* at
  small ω by e^{π(γ_1−ω)/2} (a factor 3.7·10⁹ at ω = 1), every natural
  continuation of (4.3) makes the sub-2π band far noisier than the tone, so
  the term is negligible. The defect is bookkeeping, not substance;
- the *upper* end of the band is not benign — see §4.0(d), GAP-14.

Note GUE pair correlation (M2) does **not** enter (4.3): the first moment of
the point process determines the mean spectral density; pair correlation
affects only the *fluctuation* of the periodogram about it (relevant to T2's
constants, not T1's). ∎

### Proof of Theorem T1.
By (R1)–(R4) under (M4′) and (M5), the CR inequality applies to θ̂ on the
band-limited record: Cov(θ̂) ⪰ I(θ)^{-1}, I as in (4.0). By hypothesis (B1),
I = I_N + I_R ⪯ (1 + K^{-1}) I_N, hence I^{-1} ⪰ (1 + K^{-1})^{-1} I_N^{-1}
and [I^{-1}]_{γ_jγ_j} ≥ (1 − O(K^{-1})) [I_N^{-1}]_{γ_jγ_j}: the leakage
outside the tone neighbourhoods is absorbed into the O(K^{-1}) terms. (This
is the step that fails at Ω = 2Γ — §4.0(d), GAP-14.) By §4.0(c) the
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

Zero ordinates (Odlyzko standard values); |M_W(½+iγ)| = ½|Γ(¼ + iγ/2)|
computed by Lanczos log-Γ this session:

| j | γ_j | \|M_W(½+iγ_j)\| | log(γ_j/2π) |
|---|---|---|---|
| 1 | 14.134725 | 1.160e−05 | 0.81076 |
| 2 | 21.022040 | 4.701e−08 | 1.20769 |
| 3 | 25.010858 | 1.962e−09 | 1.38143 |
| 4 | 30.424876 | 2.659e−11 | 1.57738 |
| 5 | 32.935062 | 3.631e−12 | 1.65666 |
| 10 | 49.773832 | 5.909e−18 | 2.06961 |

Sample-complexity constant c = (6 log(γ_d/2π))^{1/3} in (T1-d):

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
   different observable (prime counts, not the Gaussian-smoothed Möbius
   sum) — but it is strong evidence that **N2 overstates the interference at
   low height**. Diagnosis in §7.3. Recorded here, not buried.

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

**Ledger state after amendment A1 (v2).** 15 entries. **1 closed** (GAP-2,
REPAIRED-BY-A1). **14 open**: the 12 surviving from v1's 13, plus GAP-14 and
GAP-15 opened by the v2 amendment audit. (The ticket anticipated 12 open on
the arithmetic 13 − 1; the audit that A1 required found two more, and hiding
them to hit the predicted number would defeat the purpose of the ledger.)

| # | Gap | Where | Tag |
|---|---|---|---|
| GAP-1 | The PSD convention (2.1) and the resulting constant 24 vs the literature's 12. Numerically checked to 3 digits, not proved. Needs a written lemma fixing convention and deriving (4.2) exactly, including the exact-N discrete version with the (N²−1) correction. | §2, Lemma 2 | **ARISTOTLE-ABLE** |
| ~~GAP-2~~ | **CLOSED — REPAIRED-BY-A1 (2026-08-15).** (R1) fails without band limitation; the repair (M4′) with Ω = 2Γ was **[ADDED]** by v1 and not in the frozen spec. The required amendment is now logged and owner-approved: G1_MODEL_SPEC **AMENDMENT A1**. (M4′) is a spec clause, cited in T1's hypothesis set (§2), and (R1) HOLDS. Two residues were *not* closed with it and are carried as new entries: the sub-question "is Ω = 2Γ the right cut?" → **GAP-14**; the positivity of the extended S_ε at the low end of the band → **GAP-15**. | §3 (R1), §1.4 | **CLOSED** |
| GAP-3 | (R6) fails: ε is not Gaussian-approximable, because a_γ ≍ e^{−πγ/4} makes the first few tail terms dominate — no Lindeberg. The spec asserts "Gaussian-approximable" (§3); the Gaussian smoothing W = e^{−x²} contradicts it. Either (i) change W to one with polynomially decaying M_W (then Lindeberg may hold), or (ii) prove a non-Gaussian CR/Barankin bound, or (iii) demote T1's label to "Gaussian surrogate of N2". **Status 2026-08-15: OPEN, NOT amended.** Route (i) is recorded as **proposed amendment A2 (G1_MODEL_SPEC §A1.5), AWAITING OWNER RULING — not approved, not enacted**; nothing in v2 assumes it. Route (iii) is what v2 does in the meantime (label carried in §0, §3, §8). | §3 (R6) | **FRONTIER** |
| GAP-4 | Lemma 1's local-flatness parameter δ. Because log S_ε has slope ≈ −π/2 in ω, S_ε varies by e^{π·(bandwidth)/2} across the Lemma-1 band; with K = 4, T ≈ 17 this is **not** small, so the "O(δ) negligible" claim in (4.1) is unjustified at realistic T. Needs either an honest two-sided constant (S_ε evaluated at the band edge) or, again, a different W. Interacts with GAP-3: both are caused by the Gaussian smoothing's exponential Mellin decay. **Unchanged by A1** — band limitation acts outside the Lemma-1 neighbourhood and cannot flatten S_ε inside it. The flatness range is set by K/T, not by Ω, so the amendment neither helps nor hurts here. GAP-4 is now the short-range half of one defect whose long-range half is **GAP-14**; both are cured by A2 and by nothing else on offer. | §4 (4.1), §4.0(d) | **FRONTIER** |
| GAP-5 | Lemma 3(a) cross-tone block-diagonality is proved by an order-of-magnitude sketch. A clean statement — "if T·Δγ ≥ 2πK then [I^{-1}]_{γγ} ≥ (1−CK^{-1})[I_j^{-1}]_{ωω} with C explicit" — is a finite linear-algebra + oscillatory-integral lemma. | §4, Lemma 3(a) | **ARISTOTLE-ABLE** |
| GAP-6 | Lemma 3(b) (data-processing: discrete-sample FIM ⪯ continuous FIM) is stated, not proved. Standard, but load-bearing for the spec's §2 claim that samples are "cheap". | §4, Lemma 3(b) | **ARISTOTLE-ABLE** |
| GAP-7 | Unbiasedness (R5). The T2 estimator (windowed periodogram + quadratic refinement) is biased at finite T, so T1 as stated does not directly bound it. Route: replace CR by a van Trees / Bayesian CR bound with a prior on Θ, or by a Ziv–Zakai bound (which also captures the threshold effect the periodogram exhibits). Changes constants. | §1.5, §3 (R5) | **FRONTIER** |
| GAP-8 | The numerical FIM verification (Lemma 2) and the Γ-amplitude table (§5.1) were computed this session by throwaway scripts and are not committed as receipts. Repo convention elsewhere in this program is a `*_RECEIPT.json` with hashes. **v2 adds a third uncommitted computation**: the exact band-limited 3×3 FIM of (4.0) used for the tables in §4.0(c),(d) (white-noise re-verification of 24, ρ_d at Ω = 2Γ, and the Ω-sweep). Same obligation, now three items. | §4, §4.0, §5.1 | **ARISTOTLE-ABLE** (reproduce as a committed script + receipt) |
| GAP-9 | (M4)'s stationary extension to ω = γ_j: the whole content of "S_ε(γ_j)". A realisation has no interference atom at γ_j, so the model assigns noise where a fixed zero configuration has none. Justifiable as a minimax-over-shifts idealisation, but not justified here. This is the honest reason the spec's N3 (minimax over admissible zero configurations) exists. | §1.4 (M4), §7.3 | **FRONTIER** |
| GAP-10 | The amplitude truncation of (M3) at a quantile q: the sensitivity report the spec §3 promises has not been produced. Argued moot for the leading constant in §7.2, but not shown. | §1.4 (M3), §7.2 | **ARISTOTLE-ABLE** (numeric sensitivity sweep) |
| GAP-11 | The γ_1 empirical violation (§5.2, row 2). Needs either an N1 (deterministic) re-run of Gate 1 on the *actual* frozen observable y(t) of §1.1, or an explanation why the comparison is not apples-to-apples. Currently the latter is asserted. | §5.2 | **FRONTIER** |
| GAP-12 | Prior-art tripwire G-c: spec §5 requires a re-scout "at first-draft time". This is first-draft time. `lane_c/S2_PRIOR_ART.md` (2026-08-14, NO-COLLISION) is one day old and its own limitations section flags that a negative on "Cramér–Rao Riemann zeros" is weaker than a systematic review. Re-scout not run for this draft. | §5 of spec | **FRONTIER** |
| **GAP-14** | **NEW (v2, opened by the A1 audit).** Band-edge leakage. (M4′) makes the Fisher information finite but not small: 1/S_ε grows like e^{+πω/2} across the pass band while each tone's window-truncation tails decay only like 1/(ν−γ_j), so the information is dominated by the band edge. Hypothesis (B1) of §2 is what the proof needs; at the approved cut Ω = 2Γ it **FAILS**, ρ_d ≈ 6.8·10^{28} and the measured band-limited [I^{-1}]_{ωω} is 7.7·10^{−30} of the local 24-value (§4.0(d)). Consequences: T1's constants are proved only for bands with Ω − γ_d = O(1) (measured ratio 1.00 at Ω−γ_d = 1, 0.36 at 4, 6·10^{−2} at 6); at Ω = 2Γ the displayed bound is *not* a proved CR bound. Routes: (i) proposed amendment A2 (polynomial M_W) makes the growth polynomial and (B1) attainable at Ω = 2Γ; (ii) a further amendment narrowing Ω — owner-gated, see G1_MODEL_SPEC §A1.4; (iii) keep (B1) as an explicit hypothesis and state where it holds. Long-range twin of GAP-4. | §2 (B1), §4.0(d) | **FRONTIER** |
| **GAP-15** | **NEW (v2, opened by the A1 audit).** Positivity of the extended S_ε at the low end of the band. (M4) extends S_ε(ω) = a_{\|ω\|}² log(\|ω\|/2π) "to all ω", and (M4′)'s pass band now explicitly contains \|ω\| < 2π where that expression is **negative** — not a spectral density; taken as →0 it also reopens a (logarithmic) Cameron–Martin divergence, i.e. a low-frequency copy of the (R1) failure A1 was approved to fix. A positivity convention (a floor S_min) is needed for the (R1) repair to be complete on the whole band. Quantitatively benign: the induced relative term in I_{γ_jγ_j} is ≈ 3S_ε(γ_j)/((γ_j−2π)²T S_min) = 2.8·10^{−3}·S_ε(γ_1)/S_min at j = 1, and every natural continuation makes S_min ≫ S_ε(γ_1) because a_ω² is larger by e^{π(γ_1−ω)/2} at small ω. Needs to be written into the spec at the next amendment, not left implicit. | §4, Prop. 4.4 | **ARISTOTLE-ABLE** (state the convention + the bound) |
| GAP-13 | Whether c_d should carry a genuine d-dependence. Here it does not (Lemma 3 makes blocks independent). If (M5) is relaxed toward the true zero spacing 2π/log(γ/2π), which shrinks with height, d-dependence returns through the resolution condition: T ≥ K log(γ_d/2π) is needed, i.e. X ≥ (γ_d/2π)^K. Worth stating as a second, separate resource bound. | §2 | **FRONTIER** |

---

## 7. Discussion of the three known complications

### 7.1 The Gaussian smoothing suppresses everything

|M_W(½+iγ)| = ½|Γ(¼+iγ/2)| ≍ √(2π)/2 · (γ/2)^{−1/4} e^{−πγ/4}. From
γ_1 = 14.13 to γ_10 = 49.77 the amplitude drops by 13 orders of magnitude
(§5.1). Consequences: (i) the *raw* SNR at γ_10 is astronomically bad, so
the frozen observable is a poor practical instrument even though the T1
*rate* is clean; (ii) GAP-3 and GAP-4 both trace to this decay. A W with
polynomially decaying M_W (e.g. a compactly supported bump, whose Mellin
transform decays like |s|^{−k}) would fix both and is the obvious first
amendment to consider. **Recommendation to the spec owner: this is the
highest-value change to the frozen model.**

*Status 2026-08-15.* The v2 audit adds a third symptom of the same root
cause — GAP-3 (Gaussianity), GAP-4 (local flatness inside the tone
neighbourhood), GAP-14 (band-edge leakage outside it). The recommendation is
now on the record as **proposed amendment A2** (G1_MODEL_SPEC §A1.5),
awaiting an owner ruling; it is not approved and not enacted, and v2 assumes
nothing from it. Note the ordering that A1 exposes: A1 (approved, enacted)
makes the model non-singular; A2 (proposed) is what would make the §2
constants defensible at the approved band Ω = 2Γ.

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

**Verdict on G-a: does not fire for the leading constant.** It still fires
for the Gaussian-approximability claim, which is GAP-3.

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

---

## 8. What is claimed, and what is not

**Claimed.** In model N2 = (M1)–(M5) with spec clause (M4′) (amendment A1),
*and under the leakage hypothesis (B1)*, for any unbiased estimator **of the
band-limited record y_Ω**: max_j RMSE(γ̂_j) ≥ √6 (log(γ_d/2π))^{1/2}
(log X)^{−3/2}, hence X(ε) ≥ exp((6 log(γ_d/2π))^{1/3} ε^{−2/3}). The
amplitudes cancel. The Fisher-information computation is (4.0)–(4.3) with
the constant 24 numerically confirmed twice (time-domain, v1; band-limited
frequency-domain, v2 §4.0(c)), and S_ε(γ_j) unchanged by the band-pass
because the tones are interior with margin ≥ Γ (§4.0(a),(b)).

**Not claimed.** Nothing unconditional about ζ. Nothing about biased
estimators. Nothing about heights where (M5) fails. No claim that the
Gaussian approximation in (M4) is justified — it is not (GAP-3; proposed
amendment A2 is not approved). No claim that the bound applies to the Gate-1
numerics, which ran a different observable under N1. **New in v2, and the
most important line here:** no claim that the bound holds for estimators
seeing the *unrestricted* record y (the M4′ restriction does not transfer
upward — §1.5), and **no claim that (B1) holds at the approved cut Ω = 2Γ —
it does not** (§4.0(d), GAP-14), so at Ω = 2Γ the displayed constants are the
constants of the local problem rather than a proved bound.

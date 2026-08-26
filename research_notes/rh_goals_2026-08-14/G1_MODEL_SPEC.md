# G1-S0 — Frozen model spec: sample complexity of zeros-from-primes
v0, 2026-08-14. Author: frontier. Status: FROZEN for T1–T3 drafting; changes
require a logged amendment.

## 1. The observable (primary channel)

Use the VERIFIED smoothed Möbius explicit formula (imported,
Smoothed_Dwf_explicit_formula_VERIFIED.md; Gaussian W, M_W(s)=½Γ(s/2),
R₀=−2): for t = log N,

  y(t) := e^{−t/2} · [ Σ_{n≥1} μ(n) W(n/e^t) − R₀ − R_triv(e^t) ]
        = 2 Σ_{γ>0} a_γ cos(γ t + φ_γ) + ε(t),

with a_γ = |M_W(½+iγ)/ζ′(½+iγ)|, φ_γ = arg(...), and ε the truncation error
E_A (superpolynomially small under the formula's hypotheses H1–H3).

Under RH the observable is EXACTLY a multi-tone line spectrum in t whose
frequencies are the zero ordinates. This is the cleanest possible statement
of "primes are measurements of the zeros," and it is the model we freeze.

## 2. Resources (two axes, both counted)

- Arithmetic range X: computing y(t) requires μ(n) for n ≤ ~X = e^{T};
  the observation WINDOW in t is [0, T] with T = log X. This is the
  fundamental resource.
- Samples n_s on the window and per-sample precision (cheap relative to X).

KEY STRUCTURAL FACT the theorems must exhibit: the window grows only like
log X. Classical frequency-estimation scaling (Cramér–Rao for a single tone:
error ≍ σ / (A · T^{3/2} √n_s)) then forces

  precision ε in γ  ⇒  X ≈ exp(c · (σ/(a_γ ε))^{2/3}),

i.e., SAMPLE COMPLEXITY IS EXPONENTIAL IN THE TARGET PRECISION. This — made
rigorous with the right noise model — is the headline: a quantitative law for
how inefficient the prime-side channel to the zeros is. (It also gives the
honest converse: why numerics on primes alone will never "see" fine zero
structure — a statement RH researchers can cite when calibrating what
computations can and cannot establish.)

## 3. Noise model (the crux; one primary + one validator + one aspiration)

- N2 (PRIMARY, for T1): estimate the d lowest zeros; treat zeros above a cut
  Γ as a stochastic interference process consistent with the zero-density
  ~log(γ/2π)/2π and (for constants) GUE pair correlation; amplitudes a_γ
  from the ζ′ empirical blocks (lane_a data). The interference sum is an
  almost-periodic Gaussian-approximable process with computable spectral
  density S_ε(ω) near ω=γ_j. Fisher information / CR bound computed against
  it. All probabilistic assumptions STATED as model hypotheses — the theorem
  is "CR bound in model N2," honestly labeled.
- N1 (VALIDATOR): fully deterministic truncation — numerics with synthetic
  zero sets and with real Odlyzko zeros validate the N2 constants.
- N3 (ASPIRATION, not in v0 scope): minimax over admissible zero
  configurations (no stochastic assumption). Only if T1/T2 land.

Known complication to carry, not hide: the amplitudes a_γ involve 1/|ζ′(ρ)|,
whose second moment diverges under Gonek–Hejhal (J_{-2}); the interference
process is heavy-tailed. v0 handles this by truncating at a quantile and
reporting sensitivity; a clean treatment is future work.

## 4. Theorem ladder (drafting order)

- T4 (DONE): finite exact anchor — Prony/power-sum uniqueness, machine-proved
  (projects/aristotle_dispatch_v16/result/project_aristotle/PronyPowerSums.lean,
  axiom-clean). FF version: 2g point counts determine the L-polynomial.
- T1 (CR lower bound, model N2): for any estimator of (γ_1..γ_d) from
  {y(t): t ∈ [0, log X]}: max_j RMSE ≥ c_d · S_ε(γ_j)^{1/2} /
  (a_{γ_j} (log X)^{3/2}), constants explicit. Corollary: X(ε) is
  exponential in ε^{-2/3}.
- T2 (upper bound): the Hann-windowed periodogram + local quadratic
  refinement achieves the same (log X)^{-3/2} rate up to constants (the
  Gate-1/2 numerics already exhibit this empirically — reuse as the
  validation suite).
- T3 (unconditional detection): without RH, a zero ρ = β+iγ with β > 1/2
  contributes envelope e^{(β−1/2)t} to y(t); therefore (i) some nontrivial
  zero is always detectable; (ii) an RH-violating zero eventually DOMINATES
  the observable with SNR growing like X^{β−1/2}: RH failure is loudly
  visible in this channel. Finite-lemma parts → Aristotle.

## 5. Falsification gates

- G-a: if the N2 spectral density near target frequencies cannot be bounded
  (heavy-tail issue), demote T1 to "CR bound under truncated-amplitude
  model" and say so. If even that degenerates → drop T1, keep T2/T3
  (detection-only program). Decision by numerics, 1 week.
- G-b: T2 constants must be within 10× of the CR bound in simulations, else
  the pair (T1,T2) is not telling a coherent story — rework before writing.
- G-c: standing prior-art tripwire (S2 scout verdict NO-COLLISION, 2026-08-14;
  re-scout at first-draft time).

## 6. Immediate next actions

1. N2 spectral-density computation + heavy-tail sensitivity (numeric, can
   fan out; uses lane_a ζ′ blocks).
2. T1 proof draft in model N2 (frontier work, me).
3. T3 statement + finite-lemma decomposition for Aristotle dispatch.

---

# AMENDMENT A1 (2026-08-15, owner-approved)

**Status: ENACTED.** This section is *additive*. The v0 body above is frozen
and is NOT rewritten: the difference between what was frozen on 2026-08-14
and what T1 actually assumes must stay readable at a glance.

- **Approval:** owner, 2026-08-15 ("i approve M4"), logged at
  `plans/wayfinder/rh-goals/tickets/sample-complexity-t1.md`.
- **Origin:** found during the T1 proof
  (`lane_t/T1_CRAMER_RAO_DRAFT.md` §3 (R1), GAP-2) — i.e. AFTER the freeze,
  by the drafting work, not before it.
- **Honesty note (preregistration discipline).** This is a POST-FREEZE
  amendment, approved POST HOC. It is recorded as a dated additive clause,
  not folded into §1–§6, precisely so that a reader can see that the frozen
  model as written on 2026-08-14 did *not* support T1 and had to be changed.
  A1 is a RESTRICTION of the model and of the estimator class, not a
  strengthening: it does not make any earlier claim easier to prove, it makes
  T1's claim a claim about strictly less data.

## A1.1 Clause M4′ (band limitation)

> **(M4′) Band limitation.** The observation is band-limited. The estimator
> sees only the ideally band-passed record y_Ω, with pass band
> ω ∈ [−Ω, Ω] and
>
>   **Ω := 2Γ**,
>
> where Γ is the interference cut of §3-N2 (γ_d < Γ < γ_{d+1}; Γ is the top
> target ordinate's cut, so every target tone γ_1 < … < γ_d lies strictly
> inside the band). All T1 statements are statements about y_Ω, and **the T1
> estimator class is restricted accordingly** to estimators measurable with
> respect to {y_Ω(t) : t ∈ [0,T]}.

## A1.2 What A1 repairs: regularity (R1)

Cramér–Rao needs mutual absolute continuity of the laws P_θ (common support,
θ-independent). Under §3-N2's Gaussian surrogate the P_θ are Gaussian
measures with θ-independent covariance, so Cameron–Martin gives
P_θ ≪ P_{θ′} iff ∫ |m̂_θ(ω) − m̂_{θ′}(ω)|² / S_ε(ω) dω < ∞. With the frozen
Gaussian window W(x) = e^{−x²} the amplitudes obey
a_ω = |M_W(½+iω)| · r_ω ≍ e^{−πω/4}, hence S_ε(ω) ≍ e^{−πω/2}·log(ω/2π) and
1/S_ε grows like e^{+πω/2}, while the numerator (a finite sum of tones cut to
[0,T]) decays only like |ω|^{−2}. **The integral diverges: (R1) fails on the
full band.**

The failure is not a defect of the CR argument. It says the *model* is
singular: admitting arbitrarily high frequencies gives a noise floor that
decays super-exponentially, so θ becomes perfectly identifiable, the Fisher
information is infinite and the CR bound is identically 0. That is a
**vacuous infinite-information artifact** of extending the noise model to all
ω, not a statement about primes.

With (M4′), S_ε is bounded below by a positive constant on the pass band
(S_ε(ω) ≥ S_ε(Ω) > 0 for Γ ≤ |ω| ≤ Ω), so 1/S_ε is bounded, all P_θ are
equivalent Gaussian measures on the band, and

- **(R1) HOLDS** (mutual absolute continuity),
- **(R3) HOLDS** (differentiation under the integral, by domination),
- **(R4) finiteness HOLDS** (‖∂_j m‖²_C < ∞).

## A1.3 Direction of the restriction (a correction carried into T1 v2)

Band limitation **removes** information. More data ⇒ larger Fisher
information ⇒ *smaller* CR bound. Therefore a lower bound proved for y_Ω is
**not** automatically a lower bound for the unrestricted record y. T1 draft
v1 §3 asserted the opposite ("band-limiting only removes information, so any
lower bound proved for y_Ω is a valid lower bound for y"); that sentence is
wrong and is corrected in T1 v2.

The correct reading is the one written into A1.1: M4′ **restricts the
estimator class**, and T1 is a theorem about that restricted class. This is
forced, not optional — the unrestricted class admits no positive bound at all
(its information is infinite, per A1.2).

## A1.4 Open inside A1: is Ω = 2Γ the right cut?

Approved as Ω = 2Γ, and enacted as approved. The T1 v2 audit (draft §4.0,
GAP-14) then shows that Ω = 2Γ makes the Fisher information **finite but not
small**: 1/S_ε grows like e^{+πω/2} across the pass band, while the window
truncation gives every tone spectral tails decaying only like 1/(ω − γ_j), so
the *band-edge* leakage dominates the information. Measured directly (exact
3×3 band-limited FIM, single tone at γ_d = 49.7738, T = log 3·10⁷ = 17.2167,
Γ = 50, Ω = 100): [I^{-1}]_{ωω} is **7.7·10^{−30} times** the local
white-noise value 24·S_ε(γ_d)/(A²T³). The band that preserves the constant is
Ω ≈ γ_d + O(1) (measured ratio 1.00 at Ω − γ_d = 1, 0.78 at 2, 0.36 at 4,
6·10^{−2} at 6).

Recorded, **not enacted** — any change to Ω requires a further owner-approved
amendment. T1 v2 therefore carries the leakage condition as an explicit,
checkable theorem hypothesis (B1) and flags it as GAP-14 (currently FAILING
at Ω = 2Γ under the Gaussian W). The root cause is the same as GAP-3/GAP-4:
the Gaussian window's exponentially decaying Mellin transform.

## A1.5 (R6) / GAP-3 is NOT amended — proposed amendment A2, AWAITING OWNER RULING

§3 asserts that the interference "is an almost-periodic **Gaussian-
approximable** process". T1 v2 §3 (R6) shows this **fails as written** under
the frozen Gaussian window: ε = 2Σ_{γ>Γ} a_γ cos(γt+φ_γ) with
a_γ ≍ e^{−πγ/4}, so the first few terms above Γ dominate the sum absolutely,
the Lindeberg ratio does not vanish, and ε is close to a small sum of random
phases rather than to a Gaussian.

**Status of §3's Gaussian-approximability claim: OPEN / KNOWN-FALSE AS
WRITTEN.** It is *not* repaired by A1 (band limitation is orthogonal to
Gaussianity).

> **Proposed amendment A2 — NOT APPROVED, NOT ENACTED.** Replace the Gaussian
> window W(x) = e^{−x²} by a window whose Mellin transform M_W(s) decays only
> polynomially in |s| (e.g. a compactly supported bump, M_W ≍ |s|^{−k}). Then
> a_γ decays polynomially, no finite set of tail terms dominates, a Lindeberg
> condition becomes plausible, and (by the same mechanism) GAP-4's
> local-flatness parameter and GAP-14's band-edge leakage both become
> polynomially controlled instead of exponentially out of control.
> This would change the imported explicit formula
> (`Smoothed_Dwf_explicit_formula_VERIFIED.md`, M_W(s) = ½Γ(s/2), R₀ = −2) and
> therefore is a substantially larger amendment than A1. **Awaiting owner
> ruling.**

Until that ruling, T1 must be read as "CR bound in the **Gaussian surrogate**
of N2", GAP-3 stays open, and falsification gate G-a (§5) remains fired for
the Gaussian-approximability claim (it does *not* fire for the leading
constant — see T1 v2 §7.2).

**Superseded 2026-08-15 by AMENDMENT A2 below (owner-approved, ENACTED).**
The paragraph above records the state of §A1.5 at the time A1 was written and
is left standing unaltered; A2 is what is now in force.

---

# AMENDMENT A2 (2026-08-15, owner-approved)

**Status: ENACTED.** Additive, like A1. Neither the frozen v0 body (§1–§6) nor
AMENDMENT A1 is rewritten. A2 is the *second* post-freeze amendment; the
distance between the model frozen on 2026-08-14 and the model T1 v3 actually
assumes must stay readable at a glance, so it is appended, not merged.

- **Approval:** owner, 2026-08-15 — "i trust your judgement. please do what
  you recommend", ruling on the A2 question left open in §A1.5. The frontier
  recommendation on the table was: APPROVE A2. Logged at
  `plans/wayfinder/rh-goals/tickets/sample-complexity-t1.md`.
- **Origin:** forced by the T1 proof, twice over. (R6)/GAP-3 (the frozen §3
  claim that the interference is "Gaussian-approximable" is false under the
  Gaussian window) was found by the v1 audit; (B1)/GAP-14 (band-edge leakage
  dominates the Fisher information at the A1 cut Ω = 2Γ) was found by the v2
  audit. Both trace to one cause — `M_W(s) = ½Γ(s/2)` decays like
  e^{−π|Im s|/4}. A2 removes the cause.
- **Effect on the theorem ladder:** none on the *statements*. T1's headline
  constants are **unchanged** by A2 (§A2.6). What changes is which hypotheses
  are discharged.

## A2.1 Clause (W′) — replacement of the smoothing window

> **(W′) Window.** The Gaussian window of §1 is replaced by the **order-1
> Riesz (Fejér / Cesàro) window**
>
>   **W(x) := (1 − x)_+ = max(0, 1 − x)**,
>
> whose Mellin transform is, for Re s > 0 and by continuation,
>
>   **M_W(s) = ∫_0^∞ (1−x)_+ x^{s−1} dx = 1/s − 1/(s+1) = 1/(s(s+1))**,
>
> meromorphic on ℂ with simple poles only at s = 0 (residue 1) and s = −1
> (residue −1), and **|M_W(½+iω)| = ( (¼+ω²)(9/4+ω²) )^{−1/2} ≍ |ω|^{−2}**.

Consequences for §1's observable, spelled out because they are what the rest
of the program consumes:

1. **The arithmetic side becomes a finite Cesàro mean of Mertens.** Since W is
   supported in [0,1],

     Σ_{n≥1} μ(n) W(n/N) = Σ_{n≤N} μ(n)(1 − n/N) = (1/N) Σ_{0≤k<N} M(k),

   M(k) = Σ_{n≤k} μ(n). One pass over a Möbius sieve; no transcendental
   evaluations. This is *cheaper* than the frozen observable, so requirement
   (b) of the amendment brief ("computable in the existing pipeline") is not
   merely met, it improves.
2. **R₀ = −2 is unchanged.** The s = 0 residue of X^s M_W(s)/ζ(s) is
   Res_{s=0} M_W · 1/ζ(0) = 1 · (−2) = −2, exactly as for the Gaussian
   (the residue of M_W at 0 is W(0) = 1 for any window continuous at 0).
3. **One new explicit polar term.** M_W now has a pole at s = −1, which
   ½Γ(s/2) did not. It contributes
   Res_{s=−1} M_W · N^{−1}/ζ(−1) = (−1)·N^{−1}/(−1/12) = **12/N**.
   Write R_{−1}(N) := 12/N. The observable of §1 becomes

     **y(t) := e^{−t/2} · [ Σ_{n≤e^t} μ(n)(1 − n e^{−t}) − R₀ − R_{−1}(e^t) − R_triv(e^t) ]**
             = 2 Σ_{γ>0} a_γ cos(γ t + φ_γ) + ε(t),   R₀ = −2,

   with the *same* form as frozen §1 and
   **a_γ = |M_W(½+iγ)/ζ′(½+iγ)| = 1/( |½+iγ| · |3/2+iγ| · |ζ′(½+iγ)| )**,
   φ_γ = arg(M_W(½+iγ)/ζ′(½+iγ)). R_triv(N) = Σ_{n≥1} N^{−2n}/((−2n)(1−2n)ζ′(−2n)).
   After the e^{−t/2} normalisation both R_{−1} and R_triv are O(e^{−3t/2}).
4. **Absolute convergence of the zero sum is now a hypothesis, not automatic.**
   Σ_γ a_γ ≍ Σ_γ γ^{−2}/|ζ′(ρ)| converges given
   the conjectural Gonek–Hejhal bound J_{−1}(T) := Σ_{0<γ≤T} 1/|ζ′(ρ)|² =
   O(T) via Cauchy–Schwarz with N_ζ(T) = O(T log T) and dyadic summation
   (notation corrected 2026-08-26 per the luna GAP-16 review: the earlier
   text misnamed the first-absolute-moment sum "J_{−1}"; lane_a measured the
   squared-reciprocal slope 0.0928 against the conjectured 3/π³ = 0.0968).
   Under the Gaussian window the e^{−πγ/4} factor made this free. Stated,
   not hidden.

## A2.2 Why this window, and what was rejected

The brief required a window that (a) has polynomially decaying Mellin
transform, (b) keeps the observable computable, (c) changes the frozen
observable as little as possible. Any A2-compliant window has *finite*
smoothness in the multiplicative variable u = log x — that is the whole
mechanism, since M_W(σ+iτ) is the Fourier transform of W(e^u)e^{σu} — so
every candidate is a qualitative break from the analytic Gaussian. Given
that, "as little as possible" means preserving the *structure*: the form of
§1's display, R₀ = −2, a closed-form M_W, and Prop. 4.4's derivation. The
order-1 Riesz window preserves all four. Weighed against it:

| candidate | M_W | decay | verdict |
|---|---|---|---|
| **(1−x)_+ (Fejér / Riesz k=1)** | **1/(s(s+1))**, closed form | **\|s\|^{−2}** | **CHOSEN** |
| 1_{[0,1]} (Riesz k=0, sharp cut) | 1/s, closed form | \|s\|^{−1} | **REJECTED**: Σ_γ a_γ ≍ Σ 1/γ diverges, so the line-spectrum representation is not absolutely convergent and ε(t) is not an a.s.-finite process. k = 2 is the smallest Mellin exponent that keeps the frozen observable *defined*. |
| (1−x)^k_+, k ≥ 2 | Γ(s)k!/Γ(s+k+1) | \|s\|^{−(k+1)} | available if more decay is ever needed, but **not chosen**: the Lemma-1 flatness defect (GAP-4) scales like 2(k+1)/(ω T), so extra decay makes the one defect A2 does *not* fully close strictly worse. |
| cos²(πx/2)·1_{[0,1]} (Hann) | ½/s + ½∫_0^1 cos(πx)x^{s−1}dx | \|s\|^{−3} | **REJECTED**: no closed form (a generalised cosine integral), so every a_γ would need numerical Mellin quadrature; and it is a k = 2-equivalent, so worse on GAP-4. Strictly more cost, no benefit. |
| compactly supported C^∞ bump | — | faster than any polynomial (Gevrey e^{−c\|s\|^α}) | **REJECTED**: reproduces the Gaussian pathology in weakened form — the noise floor again outruns the signal's window sidelobes — and has no closed form. |

Decision rule that picked the winner: **take the mildest smoothing that keeps
the observable well-defined.** k = 0 is too mild (observable undefined),
k ≥ 2 is gratuitously smooth (GAP-4 worsens, closed form lost at Hann). k = 1
is the unique minimum.

## A2.3 Clause (M4″) — the low-frequency positivity convention (closes GAP-15)

A1's pass band contains |ω| < 2π, where §3-N2's density factor log(|ω|/2π) is
negative and (4.3)'s S_ε is not a spectral density. A2 fixes the convention
rather than leaving it implicit:

> **(M4″) Spectral floor.** The (M4) extension of the interference spectral
> density to the whole pass band is
>
>   **S_ε(ω) := a_{|ω|}² · ϑ(|ω|),   ϑ(ω) := max{ log(ω/2π), ϑ_min }**,
>
> with the fixed floor **ϑ_min := log(γ_1/2π) = 0.81076** ("no part of the
> band is modelled as quieter than the height of the lowest actual zero").

Under (W′), a_ω = |M_W(½+iω)|·r_ω is continuous and **strictly positive** on
the whole band (M_W(½+iω) = 1/((½+iω)(3/2+iω)) never vanishes and is bounded
by 4/3 at ω = 0), so (M4″) makes S_ε bounded below by a positive constant on
[−Ω,Ω]. That completes the (R1) repair of A1 on the *whole* band rather than
only above 2π. T1 v3 §4.0(e) measures the sensitivity: varying ϑ_min over
[0.05, 2.0] moves the band-limited [I^{-1}]_{ωω} by 4·10^{−4} relative. The
convention is therefore fixed for definiteness, not for effect.

## A2.4 What A2 repairs, measured

All figures re-derived and re-measured in T1 v3 §4.0 (γ_d = 49.7738,
Γ = 50, Ω = 2Γ = 100, T = log 3·10⁷ = 17.2167, K = 4). The script reproduces
every Gaussian-window number of T1 v2 independently before being applied to
(W′), so the comparison is like-for-like.

| defect | under frozen Gaussian W | under (W′) | status |
|---|---|---|---|
| **(R6)/GAP-3** Lindeberg ratio Λ(Γ) = 2a_Γ²/σ²(Γ) | **4.76** at Γ = 50 (> 1: one term carries more than the modelled total variance) — no CLT | **0.157** at Γ = 50, and Λ(Γ) = 6π/(Γ(log(Γ/2π)+⅓)) → 0 (0.0248 at Γ=200, 3.5·10^{−3} at 10³, 2.4·10^{−4} at 10⁴) | **CLOSED** — Lindeberg holds |
| **(B1)/GAP-14** band-edge leakage, λ_max(I_N^{−1} I_R) at Ω = 2Γ, tone γ_d | **1.73·10^{+29}** | **0.0858** ≤ 1/K = 0.25 | **CLOSED** |
| same, as [I^{−1}]_{ωω} ÷ the local 24-value | **7.7·10^{−30}** | **0.9943** | **CLOSED** |
| **GAP-4** Lemma-1 flatness: S_ε max/min over the width-4πK/T tone band | **98.2** at γ_d (93.7–98.2 across γ_1..γ_d) | **1.23** at γ_d (1.23–2.03 across γ_1..γ_d); slope d log S_ε/dω = −4/ω + O(1/(ω log ω)), so δ = O(K/(ω T)) → 0 | **REDUCED, not closed** — now an explicit two-sided constant of the same order as the O(1/(ωT)) error Lemma 2 already carries |
| **GAP-15** low-ω positivity | convention missing | clause (M4″), sensitivity 4·10^{−4} | **CLOSED** |
| **§7.1** raw instrument SNR: \|M_W(½+iγ_10)\| | 5.909·10^{−18} | **4.034·10^{−4}** (×6.8·10^{13}); dynamic range over γ_1..γ_10 falls from **13 orders** to a factor **12.3** | practically transformed |

## A2.5 What A2 costs

Stated plainly, because A2 is the larger amendment §A1.5 warned it would be:

1. **The VERIFIED import no longer applies.**
   `research_notes/imported_farey_now/Smoothed_Dwf_explicit_formula_VERIFIED.md`
   is a verified derivation *for the Gaussian window* (M_W(s) = ½Γ(s/2),
   R₀ = −2, error |E_A(N)| ≤ C_{A,W}N^{−A} for all A under H1–H3). Under (W′)
   that artifact is out of scope. The explicit formula for the order-1 Riesz
   mean is classical in form, and §A2.1 records what its residue structure
   must be, but **it has not been re-derived or re-verified in this repo.**
   This is a genuine new obligation, logged as **GAP-16** in T1 v3 §6, and it
   is a debt A2 creates, not one it discharges.
2. **The truncation error changes character.** The Gaussian gave a
   superpolynomially small E_A. Under (W′) the arithmetic side is *exact and
   finite*, but the contour-shift remainder is only polynomially controlled and
   its exact form is part of the GAP-16 obligation.
3. **Absolute convergence of the zero sum now rests on the conjectural
   J_{−1}(T) := Σ 1/|ζ′(ρ)|² = O(T)** (§A2.1.4, notation corrected
   2026-08-26) — a conjecture with lane_a empirical support, not a theorem.
4. **A residual on (R6).** Lindeberg now *holds*, but Λ(50) = 0.157 is not
   small at the operating point of §5; the finite-Γ Berry–Esseen rate is a new
   quantitative obligation, **GAP-17**.

## A2.6 Direction of the change — the self-serving audit

The honesty requirement on a post-freeze amendment is to say whether it made
the result easier. Here it did *not* make the claim bigger, and it *did* make
one measured quantity move ~29 orders of magnitude in the program's favour, so
both facts are put on the record together.

- **The headline is untouched.** T1's constants are unchanged by A2:
  c_d = √6, X(ε) ≥ exp((6 log(γ_d/2π))^{1/3} ε^{−2/3}), c = 1.6944 (d=1),
  2.3157 (d=10). The reason is structural — Prop. 4.4 gives
  S_ε(γ)/a_γ² = log(γ/2π), in which the window cancels identically. A2 cannot
  inflate a window-free constant. Those constants were derived in v1, *before*
  either defect was found.
- **The noise model becomes heavier-tailed.** The modelled interference floor
  now decays like ω^{−4} instead of e^{−πω/2}: at every frequency above the
  targets the model carries *more* interference power relative to the targets
  than the frozen model did. In that sense A2 is a weakening — it grants the
  estimator a noisier world, not a quieter one.
- **And yet the measured CR bound rises by ~29 orders of magnitude** at
  Ω = 2Γ (7.7·10^{−30} → 0.9943 of the local 24-value). This must not be
  read as A2 buying a stronger theorem. What it removes is a *modelling
  artifact*: under the Gaussian window the model asserted that zeros above
  height Ω contribute super-exponentially little noise while the target
  tones' window-truncation sidelobes persisted only polynomially — an
  arbitrarily quiet channel at the band edge through which the model, not the
  primes, let an estimator read the ordinates. It is the same pathology family
  as the infinite-information singularity A1 was approved to remove (§A1.2),
  one band-width down. A2 deletes the artifact; the bound then lands on the
  local white-noise value it was always claimed to have.
- **The change was forced by a defect with no bearing on the constant.**
  (R6)/GAP-3 — the falsity of §3's Gaussian-approximability claim — is
  independent of band edges, of Ω, and of the leading constant. A2 was
  recommended for GAP-3 in T1 v1 §7.1, *before* GAP-14 existed. The leakage
  repair is a consequence, not the motive.
- **A2 also makes the model harder to satisfy in one respect worth naming.**
  Under the Gaussian window the interferers next to γ_1 were ~250× weaker than
  the target (|M_W(½+iγ_2)/M_W(½+iγ_1)| = 4.05·10^{−3}); under (W′) they are
  comparable (0.454). N2's premise — that neighbouring zeros are genuine
  interference — is now *more* nearly true, which is a stricter, not a laxer,
  setting.

## A2.7 A1 is not superseded

(M4′) remains in force and remains necessary. Under (W′), 1/S_ε grows like
ω^4 while the time-limited signal's sidelobes decay only like |ω|^{−1} in
amplitude, so the Cameron–Martin integral over the *whole line* still
diverges and (R1) still fails without a band limit — for the opposite reason
to A1.2's (signal outrunning noise rather than noise outrunning signal), but
with the same consequence. A2 does not remove the need for A1; it makes A1's
approved cut Ω = 2Γ *usable*. The band cannot be widened indefinitely: the
measured λ_max(I_N^{−1}I_R) at γ_d grows 0.086 (Ω=100) → 0.106 (200) →
0.153 (300) → **0.250 (400)** → 0.624 (600) → 2.36 (10³) → 4.9·10^{+3}
(1.5·10⁴). So (B1) at K = 4 holds out to **Ω ≈ 400 = 8Γ**: the approved cut
Ω = 2Γ = 100 sits inside the admissible region with a factor 4 of band-width
margin. Beyond it the failure is now *soft* — the bound degrades to 0.52 of
the local value at Ω = 1.5·10⁴, not to 10^{−30}.

## A2.8 Falsification gate G-a (§5) — updated

G-a fired under A1 for the Gaussian-approximability claim (GAP-3). Under A2
the interference is Gaussian-approximable with a Lindeberg ratio that
provably vanishes, so **G-a no longer fires**, subject to the finite-Γ rate
obligation GAP-17. It never fired for the leading constant (T1 §7.2).

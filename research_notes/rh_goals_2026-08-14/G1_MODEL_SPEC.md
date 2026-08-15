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

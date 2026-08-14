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

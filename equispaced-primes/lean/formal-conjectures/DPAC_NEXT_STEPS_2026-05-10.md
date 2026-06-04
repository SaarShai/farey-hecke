---
title: "DPAC next steps - hygiene patch plan"
date: 2026-05-10
type: patch-plan
tier: claim-safe
scope: "DPAC Lean/doc hygiene after unsafe LI bridge audit"
sources:
  - handoff-2026-05-09-followup/KOYAMA_RESEARCH_DECISION_MEMO_2026-05-10.md
  - formal-conjectures/DPAC_full.lean
  - formal-conjectures/DPAC_dispatch_receipt.md
  - formal-conjectures/DPAC_HYGIENE_STATUS_2026-05-10.md
tags: [dpac, lean, hygiene, li, phase-independence, density-one]
---

# DPAC next steps - hygiene patch plan

## Verdict

Patch target: prevent future overclaiming from `dpac_of_LI`.

`dpac_of_LI` must not be advertised as an LI-to-DPAC reduction.  The current
LI hypothesis only concerns rational linear relations among zeta-zero
ordinates.  DPAC at a fixed zero depends on the finite log-prime phase vector

```text
theta_p(gamma) = gamma * log p / (2*pi) mod 1,  p <= K,
```

through the exact finite expression

```text
c_K(beta + i gamma)
  = sum_{2 <= n <= K} mu(n) * n^(-beta) * exp(-i * gamma * log n).
```

Any replacement bridge must state this phase input directly, or cite a theorem
that proves it.  Plain LI for zeta ordinates is not that theorem.

## Safe replacement hypotheses

Use one of the following, in this order of honesty.

### 1. Pointwise log-prime phase avoidance

For a fixed cutoff `K`, zeta zero `rho = beta + i gamma`, and prime set
`P_K = {p prime : p <= K}`, define

```text
Q_{K,beta}(z)
  = sum_{2 <= n <= K, n squarefree}
      mu(n) * n^(-beta) * product_{p | n} z_p.
```

Safe hypothesis:

```text
LogPrimePhaseAvoidance(K, rho) :
  Q_{K,rho.re}((exp(-i * rho.im * log p))_{p in P_K}) != 0.
```

Safe theorem name:

```text
dpac_of_logPrimePhaseAvoidance
```

This is deliberately close to the target statement.  It is claim-safe because
it does not pretend that zeta-zero LI supplies missing phase information.

### 2. Structural finite phase nonvanishing

For fixed `K` and `beta`, define the zero locus

```text
Z_{K,beta}
  = {theta in (R/Z)^(P_K) :
       Q_{K,beta}((exp(-2*pi*i*theta_p))_p) = 0 }.
```

Safe hypothesis:

```text
FiniteLogPrimePhaseIndependence(K, rho) :
  ((rho.im * log p / (2*pi)) mod 1)_{p in P_K}
    notin Z_{K,rho.re}.
```

Safe theorem name:

```text
dpac_of_finiteLogPrimePhaseIndependence
```

This is the preferred mathematical packaging if a future note wants a real
"phase independence" phrase: it names the exact finite obstruction.

### 3. External theorem bridge

Safe hypothesis:

```text
LogPrimePhaseTheorem :
  forall K rho,
    riemannZeta rho = 0 ->
    0 < rho.re /\ rho.re < 1 ->
    FiniteLogPrimePhaseIndependence(K, rho).
```

Safe theorem name:

```text
dpac_of_logPrimePhaseTheorem
```

Only this form may be described as a bridge theorem, and only after the
external theorem is actually available.

## Unsafe wording to remove

Do not write:

```text
Linear independence of zero ordinates alone gives DPAC.
LI prevents vanishing of the finite exponential sum.
Kronecker/Bohr plus LI gives DPAC.
```

Safe replacement:

```text
DPAC follows from an explicit finite log-prime phase-avoidance hypothesis.
The current LI hypothesis for zeta-zero ordinates does not imply that
hypothesis.
```

## Density-one packaging

Keep density-one as an abstract conditional counting lemma.

For fixed `K >= 2`, let:

```text
bad_K(T)  = number of nontrivial zeta zeros rho with 0 < Im(rho) <= T
            and c_K(rho) = 0,
N_zeta(T) = number of nontrivial zeta zeros rho with 0 < Im(rho) <= T.
```

Safe hypotheses:

```text
BadCountBound(K) :
  exists A_K T0, forall T >= T0,
    bad_K(T) <= A_K * T * log K.

ZetaCountAsymptotic :
  exists B > 0,
    N_zeta(T) / (T * log T) -> B as T -> infinity.
```

Safe conclusion:

```text
DensityZeroBadZeros(K) :
  bad_K(T) / N_zeta(T) -> 0 as T -> infinity.
```

Important limits:

- `K` is fixed.
- This proves density-zero bad coincidences, not pointwise DPAC.
- The Lean lemma may prove only the real-analysis comparison until Langer,
  Riemann-von Mangoldt, multiplicity conventions, and the intersection bound
  are formalized.

## Tiny future implementation patch plan

Do not perform this in the current sprint.

1. In `DPAC_full.lean`, rename or de-emphasize `dpac_of_LI`.
   Suggested replacement: add a deprecated wrapper comment and introduce
   `dpac_of_logPrimePhaseAvoidance` with the exact finite phase hypothesis.
2. Replace the `dpac_of_LI` docstring with a warning that LI over ordinates is
   insufficient for log-prime phases.
3. Rename the R3 section from
   `Linear Independence Hypothesis => DPAC`
   to
   `Finite log-prime phase avoidance => DPAC`.
4. Keep `LinearIndependenceHypothesis` only as background, or remove it if no
   theorem uses it after cleanup.
5. Keep `density_zero_from_growth_comparison` as an abstract comparison lemma;
   add comments listing the missing number-theoretic inputs instead of calling
   it an unconditional DPAC result.
6. Leave the original
   `dirichlet_polynomial_avoidance_conjecture`
   theorem statement and `research_open` status unchanged.

## Claim-safe status labels

```text
Full DPAC: research-open / defer.
dpac_of_LI: unsafe as stated / downgrade.
Log-prime phase avoidance bridge: safe conditional.
Density-one package: safe abstract conditional counting lemma.
Aristotle result: scaffold with two expected sorry holes, not a proof.
```

## Verification notes

This file is documentation only.  No Lean files were modified and no Lean
build was attempted; local `lean`/`lake` are unavailable for this sprint.

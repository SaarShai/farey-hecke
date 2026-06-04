---
title: "DPAC phase bridge Lean patch"
date: 2026-05-11
type: lean-hygiene-patch
tier: claim-safe
scope: "Tombstone unsafe LI bridge; add explicit finite phase bridge names"
targets:
  - formal-conjectures/DPAC_full.lean
tags: [dpac, lean, phase-bridge, claim-safe]
---

# DPAC phase bridge Lean patch

## Status

`DPAC_full.lean` was patched claim-safely.

No commit or push was made.  No Lean build was run: local `lean` and `lake`
were unavailable in this environment.

## Claim

The old LI bridge is not a theorem in this scaffold anymore.  The former
`dpac_of_LI` declaration was removed and replaced by a searchable tombstone:

```lean
DPAC_LI_BRIDGE_DEPRECATED, 2026-05-11
```

The file now states that DPAC at a fixed zero follows only from explicit finite
log-prime phase avoidance, a finite certified-sampling bridge, or an external
all-zero phase theorem.  The main DPAC theorem remains `research_open` and
still ends in `sorry`.

## Exact edited names

Tombstoned:

```lean
dpac_of_LI
```

Added definitions:

```lean
gammaExponentialPoly
badGammaSet
LogPrimePhaseAvoidance
FiniteLogPrimePhaseIndependence
ExternalZetaZeroPhaseAvoidance
```

Added/edited theorem statements:

```lean
moebiusDirichletPoly_eq_gammaExponentialPoly
dpac_of_logPrimePhaseAvoidance
dpac_of_finiteLogPrimePhaseIndependence
dpac_of_externalZetaZeroPhaseAvoidance
dpac_of_certifiedZetaZeroSample
dirichlet_polynomial_avoidance_conjecture
```

Reserved analytic-layer names in comments only:

```lean
badGammaSet_discrete_or_identically_zero
badGammaSet_measureZero_of_not_identically_zero
gammaExponentialPoly_not_identically_zero
badGammaSet_measureZero_moebius
ae_logPrimePhaseAvoidance_fixed_beta
```

## Verification

Readback/grep only:

```text
sed -n '1,270p' formal-conjectures/DPAC_full.lean
sed -n '270,430p' formal-conjectures/DPAC_full.lean
rg -n "dpac_of_LI|DPAC_LI_BRIDGE_DEPRECATED|LogPrimePhaseAvoidance|FiniteLogPrimePhaseIndependence|ExternalZetaZeroPhaseAvoidance|dpac_of_|gammaExponentialPoly|badGammaSet|sorry|Under LI|LI ⟹|unconditionally|Unconditional" formal-conjectures/DPAC_full.lean
command -v lean || true
command -v lake || true
```

Result:

- `dpac_of_LI` now appears only in tombstone/comment text.
- `LogPrimePhaseAvoidance` and safe bridge names are present.
- No `Under LI` or `LI ⟹` claim remains.
- The density-one section is labeled as a comparison skeleton, not an
  unconditional theorem.
- Known `sorry` sites remain for scaffolded proof obligations.

## Changed files

- `formal-conjectures/DPAC_full.lean`
- `formal-conjectures/DPAC_PHASE_BRIDGE_PATCH_2026-05-11.md`

## Risks

- Syntax was edited without Lean/Lake verification.
- `gammaExponentialPoly` uses `Real.rpow` and `Complex.log`; the exact Mathlib
  spelling may need adjustment under Lean 4.28.0.
- `moebiusDirichletPoly_eq_gammaExponentialPoly` is intentionally left as a
  scaffolded `sorry`; proving it requires complex-power convention work.
- Removing the `dpac_of_LI` theorem declaration can break downstream references.
  That break is intentional: callers must choose a real phase hypothesis,
  sampling certificate, or external phase theorem.

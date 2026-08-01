# RH-facing formal package: verification report (2026-07-18)

## 2026-07-19 matched-observable correction

The concrete submission observable has now been evaluated exactly.  For prime
`p`, including the endpoint `1` in `fareySet`,

```text
DeltaW(p) = (p - 1)/(6p) * (A(p - 1) - 1),
A(x) = sum_{n <= x} prod_{q | n}(1 - q)/n.
```

Direct exact integration checks this formula through `p = 31`.  At `p = 13`,
`M(p) = -3` but `DeltaW(p) = -95083/180180 < 0`, so the stronger pointwise
claim is false.  The frozen scan found zero agreements among all 4,617
qualifying primes through `100000`; its predeclared finite density-support
gate is `NO_SUPPORT_TO_LIMIT`.

Consequently, `FareyDiscrepancySign.lean` and
`SUBMITTED_FareySignPattern.lean` are retained only as withdrawn historical
artifacts and are marked `DO NOT SUBMIT`.  A finite range does not logically
refute the density-one theorem, but the package no longer describes it as a
submission-ready conjecture.  See
`papers/nw-mertens-note/INTEGRAL_FAREY_KILL_TEST_REPORT_2026-07-19.md`.

## Verdict

No Riemann-Hypothesis theorem, global zeta-zero avoidance theorem, or
Farey-discrepancy sign theorem is established by the current local package.
The narrower formal target is an unconditional finite Farey
exponential-sum/Mertens identity. The RH-facing and density claims are either
conditional bridges or research-open `sorry` statements.

Fresh build and axiom evidence was obtained after the Mathlib bootstrap. The
strict whole-project build fails because `lake --wfail build` treats existing
warnings as errors; the separate axiom checks complete successfully and are
recorded below.

## Exact formal status

| Layer | Current status | Evidence |
| --- | --- | --- |
| Farey bridge | `FareyBridgeIdentity.farey_bridge_identity_unconditional` states the prime-indexed exponential-sum identity `= M(p)+2` without an RH hypothesis and discharges its local decomposition premise using `RamanujanSum.farey_ramanujan_decomp`. It is not a claim about `DeltaW`, signs, density, or RH. | `FareyBridgeIdentity.lean:175-205` |
| DPAC pointwise avoidance | `DPAC_full.dirichlet_polynomial_avoidance_conjecture` and the shorter local statement end in `sorry`. The safe theorems prove avoidance only after an explicit per-zero phase-avoidance premise, a global external premise, or bounded certified-sample premises. | `DPAC_full.lean:175-238`, `302-338`; `DirichletPolynomialAvoidance.lean:45-54` |
| DPAC density-one discussion | `density_zero_from_growth_comparison` is a generic real-analysis lemma. Its application to zeta zeros needs external polynomial-zero counting, Riemann--von Mangoldt, and an intersection bound; none is formalized. | `DPAC_full.lean:254-294`, `317-330` |
| Local Farey sign statement | `FareySignPattern.farey_sign_pattern_density_one` only returns the supplied `h_chebyshev_bias` premise; moreover `DeltaW` is `opaque`. It is not an unconditional density result. | `FareySignPattern.lean:70-150` |
| Submission Farey statement | `FareyDiscrepancySign.lean` has concrete `fareySet`, `W`, `DeltaW`, `mertens`, and a density-one theorem whose body is `sorry`. It is now a withdrawn historical proposal; the associated pointwise sign claim is exactly false at `p=13`. | `FareyDiscrepancySign.lean`; matched-observable report |

## Do not merge these three claims

1. **Broad negative-Mertens regime, `M(p) < 0`.** This is broader than the
   formal submission qualifier. The current files do not state a theorem for
   all such primes. A `p = 92173` record concerns a different discrete-sum
   observable and is not evidence about this package's integral-count `ΔW`.

2. **Stronger pointwise `M(p) <= -3` assertion.** The concrete proposition is
   false. Exact arithmetic gives `M(13)=-3` and
   `DeltaW(13)=-95083/180180<0`. The older `p = 237733` and `p = 243799`
   crossTerm records remain irrelevant; the new witness uses the matched
   integral-count observable.

3. **Density-one `M(p) <= -3` assertion.** The formal statement quantifies
   `epsilon > 0` and eventually bounds the agreement ratio among qualifying
   primes by `1 - epsilon`. It remains open (`sorry` in the submission; an
   assumed Chebyshev-bias hypothesis locally). The observable is now matched:
   zero of 4,617 qualifying primes through `100000` agree. This does not
   logically refute density one, but it fails the frozen numerical-support
   gate and warrants withdrawal rather than submission.

## Hygiene audit (source-level, fresh)

- No executable `axiom` declarations found in either owned directory.
- No executable `sorryAx` occurrence found.
- `opaque DeltaW : Nat -> Real` remains in local `FareySignPattern.lean:74`.
- Research-open theorem bodies using `sorry`:
  - local: `DPAC_full.lean:338`, `DirichletPolynomialAvoidance.lean:54`;
  - submission: `FareyDiscrepancySign.lean:108`,
    `SUBMITTED_FareySignPattern.lean:101`,
    `SUBMITTED_DirichletPolynomialAvoidance.lean:49` (and the duplicate
    `_buildcheck_FareyDiscrepancySign.lean:108`).
- Two vacuous `: True := trivial` diagnostics remain in unrelated local
  `SmoothedDwfFormula_full.lean:425,442`; they are not an RH-facing theorem,
  but they mean a blanket “no vacuous True” claim for the whole directory
  would be false.

## Fresh verification record

Executed from `equispaced-primes/lean`:

```text
timeout 300 lake --wfail build
lake env lean formal-conjectures/_AxiomCheckBridge.lean
lake env lean formal-conjectures/_AxiomCheck.lean
lake env lean /dev/stdin  # DPAC `#print axioms` commands
```

`lake --wfail build` completed with exit `1`. It replayed all 8037 targets
and reported required target failures caused by warnings under `--wfail`:
`DPAC_full` and `DirichletPolynomialAvoidance` use `sorry`; `RamanujanSum`
has unused simp arguments; `SignedVsAbsoluteResidueGadget` has unused
variables. Thus the strict build is not green.

The separate plain `timeout 300 lake build` completed successfully with exit
`0` (`Build completed successfully (8037 jobs)`). Its warnings are the same
research-open `sorry` declarations and linter findings; they do not prevent
ordinary compilation.

`_AxiomCheckBridge.lean` exited `0`. Each of
`RamanujanSum.primRootsSum_eq_moebius`,
`RamanujanSum.ramanujanSum_eq_moebius`,
`RamanujanSum.farey_ramanujan_decomp`, and
`FareyBridgeIdentity.farey_bridge_identity_unconditional` depends exactly on
`[propext, Classical.choice, Quot.sound]`.

`_AxiomCheck.lean` exited `0`. Its listed bridge theorem has the same three
axioms. `dpac_le_4` additionally uses `Lean.ofReduceBool` and
`Lean.trustCompiler`; the local density wrapper uses the same three standard
axioms. The separate DPAC check exited `0`: each conditional bridge and
`density_zero_from_growth_comparison` has the same three standard axioms,
while `dirichlet_polynomial_avoidance_conjecture` depends on
`[propext, sorryAx, Classical.choice, Quot.sound]`.

The source audit found no literal executable `sorryAx` declaration. Its
research-open `sorry` bodies are limited to the named open avoidance/density
conjectures listed above and their submission copies; no axiom check showed
`sorryAx` for the bridge stack, conditional DPAC bridges, generic density
lemma, or local density wrapper.

## Exact blockers and follow-up priority

1. Do not identify `crossTerm B(p)` or a discrete-sum `W` with the concrete
   integral-count `DeltaW p` without a proved link; at `N = 2` they are
   already distinct (`5/36` versus `1/3`).
2. Resolve the strict-build warnings before asserting `--wfail` success.
3. Replace the local opaque `DeltaW`/assumed-bias wrapper with either a
   concrete formal definition and proof, or clearly keep it out of a
   proof-status claim.
4. DPAC needs an all-zero phase-avoidance theorem; its present bridges do not
   derive one from RH or LI.

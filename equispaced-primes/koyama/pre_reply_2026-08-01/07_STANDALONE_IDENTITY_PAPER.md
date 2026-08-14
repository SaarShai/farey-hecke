# Standalone analytic-identity paper: scoped extraction plan

**Recommended authorship now: Saar Shai, single author.**  Add a coauthor only after a
substantial, documented contribution to the mathematics or manuscript.

## Proposed title

**Boundary Euler-Product Identities and Local Perron Residues at Dirichlet `L`-Zeros**

## One-sentence spine

Prove and numerically audit a boundary prime-power identity at a simple Dirichlet
`L`-zero, isolate the exact local double-pole residue, and publish machine-checkable
algebraic/provenance certificates without claiming that the local residue controls the full
partial Möbius sum.

## Candidate theorem package

### Theorem A: corrected `B_infinity` boundary identity

Candidate source:
`equispaced-primes/koyama/joint-paper/APPENDIX_A_BINFTY_PROOF.md`.

Scope to retain:

- primitive nonprincipal `chi`;
- a nonreal simple critical-line zero `rho`;
- explicit primitive character inducing `chi^2`;
- fixed logarithm branch;
- explicit bad-prime corrections;
- absolutely convergent `k>=3` tail;
- an independently checked boundary passage for the `k=2` prime sum.

This is the strongest near-finished candidate, but it is not cleared for submission until an
independent analyst verifies the boundary continuation and prior art.

### Lemma B: local Perron double-pole residue

For `L(rho)=0` and `L'(rho) != 0`, the local Laurent calculation gives

```text
Res_(w=0) K^w / (w L(rho+w))
  = log(K)/L'(rho) - L''(rho)/(2 L'(rho)^2).
```

This is elementary, exact, and already represented by a zero-`sorry` Lean theorem.  Present
it as a local lemma, not as an asymptotic for a global partial sum.

### Proposition C: reproducible numerical audit

Use the existing four character/zero pairs to verify:

- the boundary identity and each correction term separately;
- convergence versus `K` with unconditional and conditional rates clearly separated;
- the local residue numerically from finite differences or high-precision derivatives;
- hashes, versions, precision, inputs, and independent recomputation receipts.

## Critical exclusion: do not use the current full `c_K` asymptotic as the headline

The current Appendix B proposes

```text
c_K(chi,rho) = log(K)/L'(rho,chi) + C_1(chi,rho) + o(1).
```

A contour shift also crosses every off-target zero `rho'`.  Its residue has a factor of the
form

```text
K^(rho'-rho) / ((rho'-rho) L'(rho',chi)).
```

Under RH, `Re(rho'-rho)=0`, so this factor is oscillatory with modulus one rather than
automatically `o(1)`.  The local double pole is correct, but it does not by itself dominate
the global sum.  The full asymptotic must be removed or independently repaired before this
paper is viable.

## Proposed 8-12 page structure

1. **Introduction and exact contribution** - one identity, one local residue lemma, one audit.
2. **Notation and branch conventions** - primitive/imprimitive characters and simple zeros.
3. **Boundary prime-power identity** - complete proof with every convergence input named.
4. **Local Perron residue** - short Laurent calculation and Lean certificate.
5. **Numerical audit** - four examples, convergence plots, term-by-term residuals.
6. **Formal and computational scope** - what Lean proves, code/data manifest, limitations.
7. **Open problem** - correct treatment of the full off-target-zero sum.

## What should not be bundled into this paper

- the failed elliptic-curve rank law: every predeclared B1/B2 gate failed on the valid
  17-row control dataset;
- the prime-bias universal-dominance conjecture;
- broad spectroscope performance claims;
- an unspecified Decision-Audit SDK.

The audit method can be the paper's reproducibility layer, but it is not a mathematical
result.  No identifiable Decision-Audit SDK implementation is present in this workspace
beyond its mention in the correspondence gate, so it should not be cited as released
software until its source location, version, license, tests, and archival identifier exist.

## Fast extraction path

1. Copy only the definitions and proof of Theorem A from Appendix A into a clean TeX file.
2. Copy only the local Laurent calculation from Appendix B; omit the global contour claim.
3. Re-run the four numerical examples from raw inputs and issue a term-level residual table.
4. Run a primary-source prior-art check focused on boundary Euler products at Dirichlet
   zeros and partial Möbius sums.
5. Obtain an independent analytic review.
6. Publish the proof, code, data, Lean file, and manifest together.

## Go/no-go gates

| Gate | Current status |
|---|---|
| Coherent single theorem spine | **PASS, candidate** |
| Local residue algebra | **PASS, Lean-certified** |
| `B_infinity` boundary proof independent review | **OPEN** |
| Prior-art/novelty search | **OPEN** |
| Four examples rerun from raw inputs | **OPEN** |
| Full `c_K` asymptotic | **FAIL / excluded** |
| Elliptic-curve positive rank claim | **FAIL / excluded** |
| Decision-Audit SDK release artifact | **MISSING / optional companion** |

This outline is materially closer to a defensible preprint than an omnibus paper combining
elliptic curves, software, prime bias, and analytic identities.


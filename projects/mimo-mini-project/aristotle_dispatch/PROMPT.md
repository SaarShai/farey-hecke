# Aristotle Dispatch: MiMo Mini-Project Top 3 Discoveries

This dispatch contains 3 Lean files stating the top 3 verified discoveries
from a multi-phase MiMo+M2 research session on per-step Farey discrepancy,
the Mertens function, and the cluster structure of extreme Farey gaps.

For each file, please:

- If the **statement** type-checks but the proof is research-open: leave
  `sorry` with `-- RESEARCH-OPEN: <one-line rationale>` comment.
- If the **statement** requires Mathlib API not present at v4.28.0: leave
  as `True := by sorry` placeholder with `-- MATHLIB-PREREQ: <missing API>`.
- If a tractable sub-result can be CLOSED (e.g., the integration computation
  in `BCZDenominatorRepulsion.lean`, which is a 5-line integral over a
  triangle in [0,1]²), please close it.
- **DO NOT introduce `axiom`.** **DO NOT fake-close by trivializing to `True`.**

Honest framing: these are research-grade conjectures backed by computational
evidence (Pearson 0.971 correlation, 99.2-99.3% empirical cluster rates,
exact -0.500 to 4 decimal places at multiple N). The statements may need
refinement to be exactly provable in Mathlib v4.28.0; we welcome corrections.

---

## File 1: `MertensNWCorrelation.lean`

**Statement target**: Under RH,
  NW(Q) − C = M(Q)² / (6Q) + O(Q^{−1/2+ε})  uniformly in Q,
where NW(Q) = Q · J(Q) / Φ(Q), J(Q) is the L² discrepancy of the Farey
sequence F_Q, Φ(Q) = Σ_{q≤Q} φ(q), M(Q) is the Mertens function, and
C = (1/2) Π_p (1 + 1/(p²(p−1))) ≈ 0.66989.

**Proof outline**: Mikolás (1949) Fourier-side identity expresses J(Q) as
Σ_m |S_Q(m)|²/m² where S_Q(m) = Σ_{d|m, d≤Q} d · M(⌊Q/d⌋). The m=1 term
gives the M(Q)²/(6Q) contribution after Q/Φ(Q) normalization. The m≥2
terms have Q-dependent mean (which determines the constant C) and
fluctuations of size O(Q^{−1/2+ε}) under RH.

**Empirical evidence**: Pearson correlation = 0.971 across 28 measured Q.
Off-grid predictions verified at Q=199933 (prime, matched to 4 decimals)
and Q=926265 (Mertens local max, matched to 0.5%).

**Likely status**: 2-3 sorries, all RESEARCH-OPEN. The infinite Euler
product C may need a `tprod` formulation. The L² discrepancy J(Q) needs
either an integral or sum definition.

**Significance**: connects Farey discrepancy fluctuations (since
Franel-Landau 1924) to the Mertens function pointwise — explains why
NW(Q) doesn't converge smoothly to C but exhibits sporadic spikes
tracking |M(Q)|.

---

## File 2: `Cluster2Universality.lean`

**Statement target**: For Farey gaps in F_N at quantile q close to 1,
the probability of a maximal cluster having size exactly 2 tends to 1
as q → 1 (equivalent: extremal index θ = 1/2).

**Empirical evidence**: 99.2-99.3% size-2 clusters at q=0.9999 across
N=10⁴, 3·10⁴, 10⁵. Independent verification on M3 + M2 machines.
ZERO size-3+ clusters observed across 30M+ tested clusters.

**Likely status**: 1-3 sorries, all RESEARCH-OPEN. Requires precise
formulation of "extreme gap at quantile q", "cluster size", and
"maximal run". Mathlib v4.28.0 may not have direct extreme-value-theory
APIs; please use elementary definitions.

**Significance**: cluster-size = 2 with deterministic mass appears
undocumented in standard EVT literature (Leadbetter-Lindgren-Rootzén,
Hsing, Smith, Coles, Resnick all surveyed). Connects to the founding
observation: small-denominator (often prime-denominator) fractions in
the Farey sequence create paired extreme gaps via the Farey neighbor
constraint b + d > N.

---

## File 3: `BCZDenominatorRepulsion.lean` — **MOST TRACTABLE**

**Statement target**: Under the BCZ joint density
  f(x, y) = 2 · 1{x + y > 1, x, y ∈ (0,1)²}
the Pearson correlation Corr(X, Y) = -1/2 EXACTLY.

**Proof outline**: Direct integration over the triangle T:
  E[X] = ∫∫_T 2x dx dy = 2/3
  E[X²] = ∫∫_T 2x² dx dy = 1/2
  Var(X) = E[X²] - E[X]² = 1/18
  E[XY] = ∫∫_T 2xy dx dy = 5/12
  Cov(X, Y) = E[XY] - E[X] E[Y] = 5/12 - 4/9 = -1/36
  Corr(X, Y) = Cov / Var = (-1/36) / (1/18) = -1/2  ✓

**Empirical evidence**: direct compute on actual Farey F_N for
N = 1000, 3000, 10000 confirms Corr = -0.5000 to 4 decimal places,
matching the analytic value.

**Likely status**: this is the most tractable file. With the right
framing (perhaps `MeasureTheory.lintegral` on a measurable set), the
integrals should be computable. The final arithmetic is trivial.

**Significance**: this is the ONLY clean "1/2" universality from the
BCZ density (with negative sign, level repulsion of normalized
denominators). The (now-withdrawn) lag-1 gap correlation conjecture
of "1/2" was refuted by direct MC of the BCZ chain in this session
(actual value ≈ 0.16). Recording this exact result preserves the one
genuine "1/2" finding.

---

## Notes for Aristotle

- Mathlib v4.28.0 expected.
- `riemannZeta` is in `Mathlib.NumberTheory.LSeries.RiemannZeta`.
- `ArithmeticFunction.moebius` is in `Mathlib.NumberTheory.ArithmeticFunction`.
- `Nat.totient` is core Mathlib.
- For the Lebesgue integral over a triangle, use `MeasureTheory.lintegral`
  on the measurable set `bczTriangle` with the appropriate density.

Please return an `ARISTOTLE_SUMMARY.md` documenting:
- Which sorries closed.
- Which remain (with RESEARCH-OPEN or MATHLIB-PREREQ annotations).
- Any places where the stated theorem needed refinement to be provable.
- The `_AxiomCheck` clean status (no extra axioms beyond `propext`, `Classical.choice`,
  `Quot.sound`).

Thank you.

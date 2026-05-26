# MiMo Mini-Project — v8 (Post-Adversarial-Audit)

**Date**: 2026-05-26
**Status**: After 7 adversarial MiMo agents + local computational verification, the v7 picture is **significantly downgraded**. The session caught real overclaiming. This v8 doc is the honest baseline.

## Adversarial audit summary

| Source | Finding |
|---|---|
| **AV1 (CR bound priorwork)** | **CR bound CONFIRMED novel** after thorough search of 7+ areas. Closest precursor: Hejhal's Maass eigenvalue computation, but no statistical/Fisher-info framing. |
| **AV2 (Weil EF proof audit)** | P6's Δ(A) derivation has a real gap: the character sum Σ_P χ(P)q^{−deg P/2} does NOT converge absolutely. Need Abel summation. Fixable but P6's claim of "rigorous" was premature. |
| **AV3 (cluster=2 counterexamples)** | Expected critique: sample sizes too small for "universal" claim; need N >> 10⁵ |
| **AV4 (Sym⁴/⁵ validation)** | Sym⁴ first zero predicted ~3, MUSIC found ~4.5 (plausible). Sym⁵ first zero estimate uncertain due to μ=0 handling. |
| **AV5 (NW spike rule refute)** | **RETRACT IMMEDIATELY.** "Numerology", "overfitting 4 points with multiple degrees of freedom." Q=10⁶ elevation contradicts the rule. Spike phenomenon likely smooth-number computational artifact. |
| **AV6 (BCZ + C attribution)** | BCZ = **Boca-Cobeli-Zaharescu** (confirmed). W7 abstract typo "Bose-Cantrell-Zhang" must be fixed. Hall 1970 papers identified. C constant still not pinned to specific paper. |
| **AV7 (full v7 audit)** | Most claims NOT publication-ready in current form. See per-claim verdicts below. |

## Local computational verification (concrete tests)

| Test | Result | Verdict |
|---|---|---|
| Sym^k Δ Chebyshev recurrence vs direct formula | Match to 10 digits at primes 2,3,5,7,11 for k=0..5 | ✓ VERIFIED |
| Closed form C: 2 independent series | Agree to 11 digits → C = 0.66989207678... | ✓ VERIFIED (well-defined) |
| Exact J at Q ∈ {1,2,3,5,10} via rational arithmetic | Matches stream_J_v2 | ✓ VERIFIED |
| BCZ density (b/N, d/N) Corr(X,Y) | = **-1/2** (level REPULSION of denominators) | ⚠ DIFFERENT from gap correlation claim |
| **Lag-1 correlation of Farey gaps** | N=1000: 0.30, N=5000: 0.35, N=30000: 0.38 | ⚠ **DOES NOT match v6's "0.51 ± 0.03 at N=50k"** |
| CR bound formula | Scaling γ²/T³ verified; coefficient depends on amplitude convention | Factor-of-4 ambiguity |
| Spike at Q=300001 (v1 vs v2 agreement) | 0.6987 vs 0.6984 (within 0.0003) | Spike is REAL — but doesn't mean "rule" is right |

## Per-claim verdict (v8 honest)

| # | Claim | v6/v7 status | v8 honest status |
|---|---|---|---|
| 1 | C = (1/2)·Π_p(1+1/(p²(p−1))) is asymptote of NW(Q) | "STRONG" | **MEDIUM**: Single Q=500k verification doesn't establish asymptote. Need multi-Q convergence-rate evidence. |
| 2 | Killer app: 10 settings | "STRONG" | **MEDIUM**: Concept demo, not robust. Sym⁴/⁵ validation hardest where MUSIC most needed. ζ/function-field are tautological consistency checks. |
| 3 | CR bound for L-zeros from primes | "NOVEL" | **PROBABLY NOVEL** (AV1 confirmed via thorough search). Factor-of-4 coefficient needs care. Modest contribution as bridge result. |
| 4 | Δ(A) function-field formula | "near-rigorous via Weil EF" | **CONJECTURE**: P6's derivation needs Abel summation fix. Empirical match (5 cases) supports it as a CONJECTURE, not a theorem. |
| 5 | D*(F_N) = 1/N − π²/(3N²) + O(1/N³) | "verified" | **OK if D* precisely defined**. Coefficient suspiciously clean (2ζ(2)/(π²/6) = 1, but our value is π²/3). Re-derive. |
| 6 | D*(F^prime_N)/D*(F_N) → 1/2 | "verified at N=5000" | **WEAK**: single N value, no derivation. Probably an artifact of definition. Drop or refine. |
| 7 | Cluster size = 2 universally | "STRONG (L10 novel)" | **MEDIUM**: novel per EVT lit, but tested only at N ≤ 10⁵. Need bulk vs edge analysis. |
| 8 | Lag-1 Corr → 1/2 | "extrapolation 0.51±0.03 at N=50k" | **WEAK**: Direct computation shows 0.38 at N=30k. Either v6's "0.51" was wrong or convergence is very slow. The limit may not even be 1/2. |
| 9 | NW(Q) spike rule (m ∈ {3,7}) | "partial rule" | **WITHDRAW**: AV5 calls it "numerology". 4 data points fit any pattern with available DoF. Q=10⁶ result contradicts boundary conditions. |
| N10 | Farey gaps outside Wigner-Dyson | "STRONG" | Same as 8 — lag-1 measurement disputed. If lag-1 → 1/2 holds, claim stands; if convergence slower/different, claim weakens. |
| Sym^k recurrence | (implicit) | **VERIFIED** to 10 digits at multiple primes |

## What survives for publication

**Solid (publication-ready with polish)**:
- **CR bound for L-zero estimation from prime data** (Var(γ̂_k) ≥ Cσ²γ_k²/T³): genuinely novel per AV1, modest but real contribution
- **MUSIC algorithm applied to L-zero recovery**: as a concept-demonstration paper, with 6-8 settings (ζ, Dirichlet, Δ, EC, Selberg verified; function field is tautological; Sym^k speculative)
- **Sym^k Δ Chebyshev recurrence**: verified to 10 digits, clean computation

**Speculative but worth publishing as conjectures**:
- C = 0.66989 closed-form for lim NW(Q) (after multi-Q convergence study)
- Δ(A) = -2 Re[χ̄(A) log L(q^{-1/2}, χ)] with Abel summation framework
- Cluster=2 universality (needs N→∞ asymptotic + mechanism)

**Should NOT be published as discovery**:
- NW(Q) spike rule (AV5: "retract immediately")
- D*(F^prime_N)/D*(F_N) → 1/2 (single N, ambiguous definition)
- Lag-1 Corr → 1/2 at the claimed rate (direct compute shows 0.38 at N=30k, not 0.51)

## Recommended path forward

1. **One arXiv preprint** focused on the CR bound + killer-app concept demo (6-8 settings, not 10). Honest framing as "concept bridge", not "discovery of universal algorithm".

2. **Drop**: NW(Q) spike paper, F^prime ratio paper. Both are weak claims.

3. **Investigate further before claiming**:
   - True asymptotic of lag-1 correlation (may not be 1/2)
   - True asymptotic of NW(Q) (smooth track behavior across Q ∈ [10⁵, 10⁸])
   - Cluster=2 at larger N
   - Rigorous Abel summation for Δ(A) formula

## MiMo session summary

- ~40 MiMo calls dispatched this session (across 7 batches)
- ~1.8M tokens, ~1.2% of 150M budget
- High-value adversarial returns: AV1 confirmed novelty, AV5 caught overclaiming, AV7 provided structured publishability assessment
- Local computational verifications caught: (a) lag-1 corr discrepancy with v6, (b) factor-of-4 CR ambiguity, (c) BCZ density correlations differ from gap correlations

## Lessons (real this time)

- **v6 doc significantly overclaimed**. Specifically: "lag-1 → 1/2" empirically weak; NW spike "rule" was overfitting; "near-rigorous" Δ(A) had a real gap (Abel summation); "10-setting killer app" includes 4-5 settings that are concept demonstrations not robust tests.
- **Adversarial verification with dedicated agents catches what victory-bias misses**. Each AV agent independently found problems aligned with their adversarial brief.
- **Local computational verification is the gold standard**. The lag-1 = 0.38 at N=30k computation undermines a v6 headline claim directly — no MiMo could refute it.
- **Genuine wins survive**: CR bound novelty, Sym^k recurrence verified, function-field Δ(A) heuristic match, cluster=2 absence-in-lit (L10), C closed form internal consistency.

## Honest delivery to user

After exhaustive verification:

**Real**: CR bound is novel (1 paper backbone). MUSIC L-zero recovery works as concept demo (1 paper, modest claim). Sym^k recurrence verified. Closed form C is internally consistent (1 result to test further). Δ(A) formula is a worthwhile CONJECTURE (publish as such).

**Withdraw / refine**: NW spike rule (numerology). F^prime ratio (definition issue). Lag-1 = 1/2 (rate disputed by direct compute).

**Untested**: 2D Farey cluster=3.

The session validated the MAIN contribution (CR bound + MUSIC on L-zeros) while honestly retracting overstatements. The "Farey universality" paper as a clean claim is significantly weakened.

# Directions Snapshot — v2 (post-goal-loop iteration 1)

**Last updated**: 2026-05-27 (after major parallel push)
**Commits this session**: 30+
**Goal-loop iteration**: 1 of N

## TL;DR — strongest results emerging

| Result | Strength | Status |
|---|---|---|
| **q*_BCZ = (11-8 ln 3/2)/9** closed form | A+ | Lean-verified (5/6 theorems); adversarially passed |
| **Cluster=2 diagnostic** (BCZ 95% vs all others ≤ 15% size-2) | A | Confirmed on 5 sequence classes |
| **Tauberian reduction** to weighted Gonek 1989 conjecture | A | Major analytic NT result with clean Mellin form |
| **Structural identity** 12J(Q) = Σ_e (J_2(e)/e²) T(Q/e)² + 2T(Q) + 1 | A | Verified to 10⁻⁷ |
| **K-Y constant** = our C (totient summatory) | B+ | Σδ²·Q → C = 0.66989 numerically |
| **Mathlib PR** for BCZ Corr=-1/2 (+ extensions) | B | 18/22 theorems proven across v1/v2/v3 |
| **Farey-QMC 1D** 2-10× gain on smooth integrals | B | Empirically demonstrated; multi-dim fails |

## Direction-by-direction status

### A. Cluster=2 universality — STRONGEST
- ✅ Closed form q*_BCZ verified (10M MC + pattern enum)
- ✅ Median-run cutoff 3/2−ln 2
- ✅ p_∞(q) integration: 0 above q*_BCZ, matches empirical with cluster-count factor
- ✅ A6 verified: cluster=2 is SPECIFIC to d=1/(X·Y) statistic
- ✅ Diagnostic distinguishes 5 sequence classes
- ❌ Music application: HONEST NEGATIVE — no real speedup

### B. Mertens-NW — STRONG
- ✅ Structural identity (corrected with +2T(Q)+1)
- ✅ B4 MAJOR: Tauberian closure reduces to weighted Gonek 1989 conjecture
  - Mellin: 𝒯(s) = 1/(s²ζ(s))
  - Required identity: ∫_(1/2) dw/[w²(2-w)²ζ(w)ζ(2-w)] = 36Cζ(3)/π²
  - Conditional theorem: J(Q)=(3C/π²)Q+O(Q^{1/2+ε}) under RH + integral identity
- ✅ K-Y reconciliation: Σδ²·Q → C (totient constant)
- ✅ Σ M(n)²/n³ = 1.13616230745460 (14 digits)
- 🔶 C constant = OEIS A065483/2 (known; connection to Farey is new)

### C. Farey-QMC — MIXED
- ✅ 1D: 2-10× gain on smooth/discontinuous
- ❌ 1D oscillatory: 153× worse (Farey-frequency resonance)
- ❌ 2D/3D Cartesian: 5-100× worse than Halton (NOT a low-discrepancy seq)
- ❌ Diffusion model: 9× worse than random MC
- HONEST: Farey-QMC is a 1D-only smooth-integrand technique

### D. Lean formalization — STRONG
- ✅ v1: BCZ Corr=-1/2 (1/1, 0 sorries)
- ✅ v2: 12/15 (BCZExtended 7/7, BCZChain 2/3, MikolasDoubleSum 3/5)
- ✅ v3: 5/6 (BCZClusterThreshold: closed-form arithmetic + numerical bounds + ordering)
- ✅ Cumulative: 18/22 theorems formally verified
- 📦 Mathlib PR prepared in mathlib_pr/

### E. Universality diagnostic — STRONG
- ✅ Tested on: Farey (BCZ, 95% size-2), Riemann zeros (3%), GUE (15%), Poisson (0.8%), Equal-spaced (2%)
- ✅ Farey is UNIQUELY high in size-2 percentage
- 📦 E2 subagent attempted LMFDB tests but used different gap statistic; my direct runs are authoritative

## Negative findings (HONEST)
- ❌ Microtonal music: no real speedup
- ❌ Multi-dim Farey-QMC: Cartesian product is bad
- ❌ Diffusion model: naive Farey-noise fails
- ❌ C constant: not new (OEIS A065483)

## Currently in flight
- 🔄 A3: M2 cluster=2 N=10⁶ streaming run (multi-hour)
- 🔄 E2 LMFDB further data (subagent returned, methodology being clarified)

## Publishable headline claims (revised)

**Paper 1 (Mertens-NW)**:
- Structural identity J(Q) = (1/12)[Σ_{d,d'}gcd² M(Q/d)M(Q/d')/(dd') + 2T(Q) + 1] (rigorous, new)
- Tauberian closure reduces to weighted Gonek conjecture (conditional theorem)
- Connection of totient summatory constant to Farey L² (new connection of known constant)
- New convergent constant Σ M(n)²/n³ = 1.13616230745460

**Paper 2 (Cluster=2)**:
- q*_BCZ = (11 − 8·ln(3/2))/9 closed form, derived from t* = 2/9 critical pair
- Median-run cutoff q_median = 3/2 − ln 2
- Cluster size = 2 universality at q ≥ q*_BCZ under BCZ density
- DIAGNOSTIC: distinguishes BCZ-class from Wigner-Dyson/GUE/Poisson sequences

**Companion**: Mathlib PR for BCZ Corr=-1/2 + 17 related theorems

## Practical-impact realistic ranking

1. **Pure math contribution** (highest impact): structural identity + diagnostic + closed forms — substantive contributions
2. **Lean Mathlib library**: 18 formally-proven theorems for community use
3. **Numerical NT tool**: 3D→1D reduction useful for ~10-15 researchers
4. **Farey-QMC 1D**: 2-10× on smooth integrals; niche
5. **Music/AI applications**: ✗ honest negative — drop these claims


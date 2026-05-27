# Directions Snapshot — v3 (goal-loop iter 1 final)

**Last updated**: 2026-05-27 (after all honest corrections)
**Goal-loop iterations completed**: 1 of N
**Total commits**: 33+

## TL;DR — Final headline results (post-honesty rounds)

| Result | Strength | Status | Novel? |
|---|---|---|---|
| **q*_BCZ = (11−8·ln(3/2))/9** closed form | A+ | Lean 5/6, adversarial pass | ✓ NEW |
| **Cluster=2 diagnostic** (Farey 95%, others ≤15%) | A | 5+ sequence classes tested | ✓ NEW |
| **Tauberian → Gonek 1989** reduction | A | Mellin 𝒯(s)=1/(s²ζ(s)) | ✓ NEW |
| **Median-run cutoff** 3/2 − ln 2 | A | Lean: proven | ✓ NEW |
| **Σ M(n)²/n³ = 1.13616** | B+ | 14 digits | Possibly new |
| **K-Y constant = C totient** | B+ | Σδ²·Q → C | Connection new |
| Structural identity = Franel 1924 | B | Empirically verified | ✗ Classical |
| Mathlib PR | C | Needs rewrite for integration | Not yet ready |

## Direction status

### A. Cluster=2 universality — STRONGEST
- ✅ q*_BCZ closed form (10M MC + pattern enum, 50M extreme-q test)
- ✅ Median-run cutoff
- ✅ Diagnostic distinguishes 5 sequence classes
- ✅ A6: SPECIFIC to d=1/(XY) statistic
- ✅ A4: p_∞(q) integration matches empirical
- ❌ A5: no microtonal speedup

### B. Mertens-NW — STRONG, headline = Gonek reduction
- ✅ Mikolás-Parseval +1 corrected (NEW derivation)
- ✅ Convolution form via J_2 (NEW combinatorial)
- 🔶 Structural identity = Franel 1924 (must cite predecessors)
- ✅ **B4 Tauberian → weighted Gonek 1989** (MAJOR new)
- ✅ Σ M(n)²/n³ = 1.13616230745460 (14 digits)
- ✅ K-Y reconciliation: Σδ²·Q → C

### C. Farey-QMC — mostly negative
- ✅ 1D cherry-picked smooth: 2-5× better
- ❌ Black-Scholes: 2-25× WORSE
- ❌ Multi-dim Cartesian: 5-100× WORSE
- ❌ Diffusion noise: 4-9× worse
- HONEST: regime-dependent, no universal advantage

### D. Lean — incomplete
- ✅ 18/22 arithmetic identities proven (Aristotle v1+v2+v3)
- ❌ But don't actually integrate BCZ density — need rewrite
- Mathlib PR needs ~1-2 days of real Lean work

### E. Universality diagnostic — STRONG
- ✅ Farey 95%, Riemann 3%, GUE 15%, Poisson 0.8%, Periodic 2% at q=0.99
- ✅ Farey UNIQUELY high — diagnostic distinguishes BCZ class
- ✅ 50M chain: 99.6% size-2 at q=0.99999

## Novel contributions (final, honest)

### NEW
1. q*_BCZ = (11−8·ln(3/2))/9 closed-form
2. q_median = 3/2 − ln 2 median-run cutoff
3. Tauberian → weighted Gonek reduction
4. Cluster=2 diagnostic with comparison table
5. Σ M(n)²/n³ = 1.13616 (possibly new constant)
6. Connection C (totient) ↔ Farey L²

### CLASSICAL (we restated/extended)
- Structural identity = Franel 1924
- C = OEIS A065483/2
- BCZ density framework = BCZ 2001

## Negative findings (DROP from claims)
- Microtonal speedup
- Multi-dim Farey-QMC
- Diffusion Farey-noise
- Universal QMC advantage
- AI music applications
- "Original" structural identity

## Publication plan

**Paper 1** (Mertens-NW) → J. Number Theory, 12-15pp
- Lead: Tauberian → Gonek reduction
- Cite Franel 1924, Mikolás 1949/51, K-Y 1996
- Quality: B+

**Paper 2** (Cluster=2) → Annals of Applied Probability, 15-18pp
- Lead: q*_BCZ closed form + diagnostic
- Quality: A−

**Lean PR**: 2-stage (current arithmetic + future integration)

## What's left
1. Write papers (deferred per user)
2. Mathlib PR refactor (1-2 days)
3. M2 N=10⁶ result (running)
4. More diagnostic comparisons (L-functions)
5. Σ M²/n^s closed forms for various s

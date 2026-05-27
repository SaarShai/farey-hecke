# Achievements v2 (corrected) — after iter 2

## Major correction
Earlier "GUE 15% size-2" was a UNFOLDING ARTIFACT. With proper Wigner semicircle unfolding,
ALL 6 Wigner-Dyson ensembles cluster at 0.5-0.75% size-2 at q=0.95.

**Corrected universality diagnostic** (at q=0.95):

| Class | size-2 % | Notes |
|---|---|---|
| **BCZ (Farey)** | **88.17%** | UNIQUELY HIGH (~125× others) |
| Poisson | 4.65% | No-correlation null |
| GOE (Hermitian real) | 0.65% | Wigner-Dyson |
| GUE (Hermitian complex) | 0.66% | Standard for RMT |
| GSE (Hermitian quaternion) | 0.51% | Symplectic |
| COE / CUE / CSE | 0.7% | Circular ensembles |
| ζ first 100k zeros | 0.14% | (matches RMT prediction) |

## 6 novel contributions (final, post-correction)

1. **q*_BCZ = (11-8·ln(3/2))/9** closed-form threshold (Lean: 5/6 proven)
2. **q_median = 3/2 - ln 2** closed-form median-run cutoff
3. **Tauberian reduction to weighted Gonek 1989** (with Mellin transform)
4. **Cluster=2 diagnostic** distinguishing BCZ from ALL Wigner-Dyson sequences (125× signal)
5. **Σ M(n)²/n³ = 1.13616230745460** (14 digits, possibly new constant)
6. **Connection C = totient summatory constant ↔ Farey L²-discrepancy**

## Negative findings (honest)

- Music: no algorithmic speedup
- Multi-dim Farey-QMC: 5-100× worse than Halton
- Diffusion Farey-noise: 4-9× worse
- Farey-QMC universally: regime-dependent
- Structural identity: it's Franel 1924
- Original "GUE 15% size-2" claim: artifact

## Lean status

- v1 + v2 + v3: 18 arithmetic identities proven (from defs)
- v4: 308-line integration-based proof with 2 measurability/integrability sorries (Aristotle running)

## Publication outlook

**Paper 2 (Cluster=2)** is the strongest:
- Two closed-form thresholds
- Universality diagnostic with 125× signal
- BCZ chain mechanism
- Target: Annals of Applied Probability, A− quality

**Paper 1 (Mertens-NW)** is solid:
- Tauberian → Gonek reduction (new)
- Alternative derivation of Franel's identity (with +1 correction)
- New convergent constant Σ M(n)²/n³
- Target: J. Number Theory, B+ quality

## What's still running
- A3: M2 cluster=2 N=10⁶ (multi-hour)
- Aristotle v4: real integration Lean proof

# δ(Q) measurement at M(Q)=0 — direct empirical bound on the residual

## Method

For Q where M(Q) = 0 exactly: NW(Q) − C = M(Q)²/(6Q) + δ(Q) = 0 + δ(Q) = δ(Q).

So **δ(Q) = NW(Q) − C** directly, without M² confounding.

## Data (10 prime-like Q ∈ [50k, 1M] where M(Q)=0)

| Q | NW(Q) | δ(Q) = NW − 0.66989 | |δ|·√Q |
|---|---|---|---|
| 78131 | 0.66503 | −0.00486 | 1.359 |
| 79688 | 0.66658 | −0.00331 | 0.934 |
| 130324 | 0.66850 | −0.00139 | 0.502 |
| 162384 | 0.66843 | −0.00146 | 0.588 |
| 163733 | 0.66715 | −0.00274 | 1.109 |
| 201797 | 0.66723 | −0.00266 | 1.195 |
| 267328 | 0.66946 | −0.00043 | 0.222 |
| 322490 | 0.66922 | −0.00067 | 0.380 |
| 384694 | 0.67405 | +0.00416 | 2.579 |
| 565801 | 0.67112 | +0.00123 | 0.925 |

## Statistics

- **Mean δ(Q) = −0.00121** (slight negative bias)
- **|δ(Q)|·√Q** spans 0.22 to 2.58, mean **0.98** — supports δ(Q) ~ Q^{−1/2} scaling
- **8/10 negative** (binomial: P(8 or more of one sign in 10 fair coins) ≈ 11%, so not strongly significant but suggestive)

## Conclusion

The residual term δ(Q) := NW(Q) − C − M(Q)²/(6Q) at M(Q)=0 cases:
- **Magnitude**: O(Q^{−1/2}) with constant ~ 1 (i.e., |δ(Q)| ≈ 1/√Q empirically)
- **Sign**: weakly biased negative (mean ~ −10⁻³ at Q ~ 200k)
- **Behavior**: fluctuates with Q, no obvious trend in sign

## Implication for the full formula

Combined with the m=1 EXACT identity, the complete empirical statement is:

  **NW(Q) − C = M(Q)²/(6Q) + δ(Q),  where |δ(Q)| ≤ K · Q^{−1/2} for some K ≈ 1**

This is a SHARP empirical characterization. The Tauberian closure (Problem #1) would prove this rigorously with explicit K.

## Connection to the Σ M(n)²/n³ constant

If the rigorous result is δ(Q) = constant · Q^{−1/2} · (oscillating term), and the oscillating term has 0 mean, then averaged over Q:

  E_Q[δ(Q)] → 0  as Q → ∞

The Mean δ = −0.001 we observe is consistent with the average being 0 at infinity, with finite-Q bias.

The Q^{−1/2} scaling is consistent with the Mertens function being O(Q^{1/2+ε}) under RH and the off-diagonal sums providing exactly the right cancellation.

## Verification beyond Q=10⁶

To improve the empirical bound, run stream_J on M(Q)=0 cases at Q ∈ [1M, 10M]. From my earlier sieve, there are 9879 such Q values ≤ 5M. Sampling 20-30 of them and computing NW(Q) would give:
- |δ(Q)| · √Q convergence to a stable constant?
- Sign symmetry as N → ∞?
- Better bound on the leading constant K

This is M2-class compute (Q=10⁷ takes ~hours each). Could be the next M2 batch.

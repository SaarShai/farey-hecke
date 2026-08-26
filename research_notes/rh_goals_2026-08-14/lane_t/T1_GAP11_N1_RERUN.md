# GAP-11 N1 (deterministic) re-run of the frozen T1 observable

Lane T. 2026-08-26. Script: `lane_t/t1_gap11_rerun.py`. Receipt:
`lane_t/T1_GAP11_N1_RECEIPT.json`.

## What this computes

The **actual frozen observable** of T1 draft §1.1 under amendment A2 (window
W'), following the Proposition R explicit formula of
`T1_GAP16_RIESZ_IMPORT.md` §2.4:

    S(N) := Sum_{n<=N} mu(n) (1 - n/N) = (1/N) Sum_{0<=k<N} M(k)

    y(t) := N^{-1/2} * [ S(N) - R0 - R_{-1}(N) - R_triv(N) ]
          = 2 Sum_{gamma>0} a_gamma cos(gamma t + phi_gamma) + eps(t),  N = e^t

    R0 = -2,  R_{-1}(N) = 12/N,  R_triv(N) = leading term N^{-2}/(2 zeta'(-2))
    a_gamma * e^{i phi_gamma} = 1 / ( (1/2+i gamma)(3/2+i gamma) zeta'(1/2+i gamma) )

This is a **deterministic** re-run (N1), not a model-N2 comparison: it
computes the exact quantity y(t), on the exact arithmetic side (Mobius
function, sieved directly to N_MAX = 3e7), with no stochastic model
attached. It answers GAP-11's question directly: does the observable T1
actually defines behave the way Proposition R says it should, at the scale
(X = 3e7) where the earlier Gate-1 comparison (draft §5.2) was made.

## Method

1. Sieve mu(n) for n = 1..3e7 with a standard numpy prime/prime-square
   sieve (1.7 s).
2. M(k) = cumulative sum of mu; a second cumulative sum gives
   `prefix2(N) = Sum_{k<N} M(k)`, so `S(N) = prefix2(N)/N` for any integer N
   in one array lookup.
3. Sample S(N) on a log-spaced grid of 200 integers N in [1000, 3e7]
   (log-spaced in N = uniform in t = log N, needed for the periodogram step).
4. Subtract R0, R_{-1}(N), and the leading term of R_triv(N)
   (n=1 term only; the n=2 term is O(N^-4)/zeta'(-4), utterly negligible at
   N >= 1000 and is not computed — this is a deliberate, stated truncation,
   not an omission).
5. Compare y(t) against the K-zero-truncated Prop R prediction using
   a_gamma, phi_gamma computed from `mpmath.zeta(s, derivative=1)` at the
   first 10 Odlyzko zero ordinates (mp.dps = 30).
6. Independently extract the amplitude at gamma_1 = 14.134725 directly from
   y(t) by a matched filter (windowed periodogram: trapezoidal estimate of
   `(1/T) int y(t) e^{-i*gamma_1*t} dt` over the sampled grid), with no
   dependence on the truncated prediction of step 5, and with an off-tone
   control at gamma = 17.0.

## Results

**Prop R residual, K-zero truncation** (RMSE over the grid, N >= 1000):

| K (zeros used) | residual RMSE |
|---|---|
| 1 | 3.73e-03 |
| 3 | 1.98e-03 |
| 10 | 6.89e-04 |

Monotone decrease with K, consistent with the residual being the
zero-truncation tail (exactly the behavior GAP-16 §3's small-N mpmath check
already showed) — this is now confirmed at the actual scale N_MAX = 3e7 with
an exact sieve rather than a 2e4-scale mpmath check.

**Matched filter at gamma_1**, independent of the truncated prediction:

- `|C(gamma_1)|` (measured directly from y(t)) = **6.287349e-03**
- predicted `a_gamma_1` (from Prop R + mpmath zeta') = **6.271348e-03**
- ratio = **1.0026** (0.26% agreement)
- off-tone control at gamma = 17.0: `|C|` = 3.27e-04, an order of magnitude
  below the on-tone value — confirms this is a genuine resonance, not an
  artifact of the windowed integral.

This is a strong, deterministic, non-circular confirmation of Proposition R
(GAP-16): the actual Mobius-sieve observable, at the scale used in the
earlier empirical comparison, reproduces the predicted single-tone amplitude
at gamma_1 to better than 1%.

## Bearing on GAP-11 / §5.2's tension

The draft's §5.2 table compared the T1 model-N2 RMSE bound against a
**different** observable's empirical error (Gate-1's MUSIC/periodogram
recovery of zero locations from prime counts, not from this Mobius-Cesàro
sum). This re-run does not resolve that comparison — it was never a
comparison of like observables, which is exactly what GAP-11 flagged.

What this re-run adds: it confirms that **y(t) itself behaves as claimed**
(Prop R holds to sub-percent accuracy at N = 3e7), so the amplitude scale
`a_gamma_1` that the T1 bound uses is not in question — the bound's
input data is verified deterministically. The open tension recorded in
draft §5.2 (T1 bound RMSE at gamma_1 = 0.030874 vs. the unrelated Gate-1
empirical figure 0.005654) is therefore **not explained by this re-run**,
because Gate-1's estimator does not operate on y(t) — it is still an
apples-to-oranges comparison, now demonstrated more precisely rather than
resolved. A genuine like-for-like test would require running an estimator
(e.g. MUSIC or a windowed periodogram) *on this y(t) series itself* to
recover gamma_1 and report ITS empirical error against the T1 bound — that
is a natural next step, not attempted here (out of scope for the requested
deterministic re-run of the observable).

## Ambiguities encountered

None requiring a stop. The observable's normalization (§1.1's y(t) formula
and R0/R_{-1}/R_triv) and the Prop R prediction (GAP-16 §2.4) are both
stated exactly in the source documents; no guess was needed.

## Files

- `lane_t/t1_gap11_rerun.py` — the script (sieve + Prop R comparison +
  matched filter).
- `lane_t/T1_GAP11_N1_RECEIPT.json` — machine-readable receipt (inputs, N
  grid, script sha256, key numbers).

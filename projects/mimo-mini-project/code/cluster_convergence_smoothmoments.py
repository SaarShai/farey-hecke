#!/usr/bin/env python3
"""
SHARPEN the convergence-exponent question with SMOOTH moments of the BCZ
denominator pair, which have exact limits and whose error is bias-dominated
(not quantile/threshold/sampling-noise dominated).

Let X=b_i/N, Y=b_{i+1}/N.  Under BCZ, (X,Y) equidistributes with density 2 on
T={0<x,y<=1, x+y>1}.  Exact limit moments (integral of g*2 over T):
  E[XY]   = 2*int_T xy        = 5/12
  E[X+Y]  = 2*int_T (x+y)     = 4/3
  E[1/(XY)] (the NORMALISED gap N^2/(b b')) diverges, so we instead track
  E[ (XY) ]  and  E[ (XY)^2 ]  and the CDF F(t)=P(XY<t) at several t.

Two things this script does that the first did not:
  (1) Fits |moment_N - moment_inf| ~ C N^{-delta} for SMOOTH moments E[XY],
      E[(X+Y)] -- bias-dominated, no quantile noise.
  (2) Separates BIAS from FLUCTUATION for the CDF observable: it computes the
      same F_N(t) but ALSO an estimate of the sampling-fluctuation scale by
      block-splitting (variance of F over K equal contiguous blocks).  If the
      total error |F_N - F_inf| tracks the block-fluctuation 1/sqrt(M) rather
      than a separate bias power, then the apparent delta~1 is the sampling
      floor, NOT a spectral bias exponent.
A denser N ladder (geometric, ratio ~1.5) gives a longer lever arm.
"""
import json
import math
import os
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RESULT_JSON = os.path.join(HERE, "cluster_convergence_smoothmoments_results.json")


def farey_denominators(N):
    a, b, c, d = 0, 1, 1, N
    yield b
    while c <= N:
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
        yield b


def pass_stats(N, cdf_ts, n_blocks=20):
    """Streaming O(1)-mem pass.  Returns:
      ngaps, mean_XY, mean_sumXY (X=b/N), mean_XY2,
      F_N[t] for each t, and block-wise F estimates for fluctuation scale."""
    N2 = float(N) * float(N)
    s_xy = 0.0
    s_sum = 0.0
    s_xy2 = 0.0
    cdf_thr = {t: t * N2 for t in cdf_ts}
    cdf_cnt = {t: 0 for t in cdf_ts}
    # block accounting for the t=0.20 CDF fluctuation estimate
    t_block = 0.20
    thr_block = t_block * N2
    block_cnt = []
    block_tot = []
    blk_c = 0
    blk_t = 0

    gen = farey_denominators(N)
    prev = next(gen)
    ngaps = 0
    # we need block boundaries; approximate by counting and splitting evenly
    # using a target block size derived from |F_N| ~ 3N^2/pi^2
    approx_total = max(1, int(3.0 * N2 / (math.pi ** 2)))
    block_size = max(1, approx_total // n_blocks)
    for cur in gen:
        b1 = prev
        b2 = cur
        prod = b1 * b2
        xy = prod / N2
        s_xy += xy
        s_sum += (b1 + b2) / N
        s_xy2 += xy * xy
        for t, c in cdf_thr.items():
            if prod < c:
                cdf_cnt[t] += 1
        # block fluctuation
        blk_t += 1
        if prod < thr_block:
            blk_c += 1
        if blk_t >= block_size:
            block_cnt.append(blk_c)
            block_tot.append(blk_t)
            blk_c = 0
            blk_t = 0
        ngaps += 1
        prev = cur
    if blk_t > 0:
        block_cnt.append(blk_c)
        block_tot.append(blk_t)

    block_F = [c / t for c, t in zip(block_cnt, block_tot) if t > 0]
    return dict(
        ngaps=ngaps,
        mean_XY=s_xy / ngaps,
        mean_sumXY=s_sum / ngaps,
        mean_XY2=s_xy2 / ngaps,
        F_N={t: cdf_cnt[t] / ngaps for t in cdf_ts},
        block_F=block_F,
    )


def fit_power(Ns, errs):
    Ns = np.asarray(Ns, float)
    errs = np.asarray(errs, float)
    m = errs > 0
    if m.sum() < 3:
        return None
    x, y = np.log(Ns[m]), np.log(errs[m])
    A = np.vstack([x, np.ones_like(x)]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    slope, intercept = coef
    yhat = A @ coef
    ss_res = float(((y - yhat) ** 2).sum())
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    n = len(x)
    sxx = float(((x - x.mean()) ** 2).sum())
    se = math.sqrt((ss_res / (n - 2)) / sxx) if n > 2 and sxx > 0 else float("nan")
    return dict(delta=-slope, se=se, r2=r2, n=n)


def main():
    t0 = time.time()
    # exact limits  (verified: area(T)=1 under density 2)
    EXY = 5.0 / 12.0     # 2*int_T x y  = 5/12
    Esum = 4.0 / 3.0     # 2*int_T (x+y) = 4/3
    # E[(XY)^2] = 2*int_T x^2 y^2  -- compute numerically once
    from scipy import integrate
    EXY2 = integrate.dblquad(lambda y, x: 2 * (x * y) ** 2 if x + y > 1 else 0.0,
                             0, 1, 0, 1)[0]
    Finf = {0.10: None, 0.20: None, 0.35: None}
    # reuse exact CDF values from the companion script's integrator
    def P_BCZ_XY_less(t):
        if t <= 0:
            return 0.0
        if t >= 0.5:
            return 1.0
        def integ(x):
            yl = max(0.0, 1 - x)
            yh = 1.0 if x <= t else t / x
            return 2.0 * max(0.0, yh - yl)
        return integrate.quad(integ, 0, 1, limit=400)[0]
    Finf = {t: P_BCZ_XY_less(t) for t in (0.10, 0.20, 0.35)}

    print(f"Exact: E[XY]={EXY}  E[X+Y]={Esum:.6f}  E[(XY)^2]={EXY2:.6f}")
    for t, v in Finf.items():
        print(f"  F_inf({t})={v:.8f}")
    print()

    # denser geometric ladder
    Ns = [700, 1000, 1500, 2200, 3300, 5000, 7500, 11000, 16000, 24000]
    cdf_ts = (0.10, 0.20, 0.35)
    recs = []
    print(f"{'N':>7} | {'ngaps':>11} | {'E[XY]err':>10} | {'Esum err':>10} | "
          f"{'F.20 err':>10} | {'blkstd*sqrtM':>12} | {'sec':>6}")
    for N in Ns:
        tn = time.time()
        r = pass_stats(N, cdf_ts)
        dt = time.time() - tn
        eXY = abs(r["mean_XY"] - EXY)
        eS = abs(r["mean_sumXY"] - Esum)
        eF = abs(r["F_N"][0.20] - Finf[0.20])
        # fluctuation scale: std of block-F times sqrt(block count) ~ the
        # 1-block-relative sampling sigma; compare its 1/sqrt(M) projection.
        bF = np.asarray(r["block_F"])
        blk_std = float(bF.std(ddof=1)) if len(bF) > 1 else float("nan")
        M = r["ngaps"]
        # predicted whole-sample sampling sigma = blk_std / sqrt(n_blocks)
        samp_sigma = blk_std / math.sqrt(len(bF)) if len(bF) > 0 else float("nan")
        recs.append(dict(N=N, ngaps=M, mean_XY=r["mean_XY"],
                         mean_sumXY=r["mean_sumXY"], mean_XY2=r["mean_XY2"],
                         F_N=r["F_N"], eXY=eXY, eS=eS, eF=eF,
                         blk_std=blk_std, samp_sigma=samp_sigma))
        print(f"{N:7d} | {M:11d} | {eXY:10.3e} | {eS:10.3e} | "
              f"{eF:10.3e} | {samp_sigma:12.3e} | {dt:6.1f}")

    Narr = [r["N"] for r in recs]
    print("\n" + "=" * 72)
    print("SMOOTH-MOMENT CONVERGENCE FITS  |m_N - m_inf| ~ C N^{-delta}")
    print("=" * 72)
    fits = {}
    for key, label in [("eXY", "E[XY] -> 1/4"),
                       ("eS", "E[X+Y] -> 4/3")]:
        errs = [r[key] for r in recs]
        f = fit_power(Narr, errs)
        fits[key] = f
        print(f"  {label:16s}: delta={f['delta']:.4f}  se={f['se']:.4f}  "
              f"R^2={f['r2']:.4f}")

    # CDF total error vs sampling-sigma: are they the same power?
    print("\nCDF F(0.20): TOTAL error vs predicted SAMPLING sigma")
    eF = [r["eF"] for r in recs]
    sig = [r["samp_sigma"] for r in recs]
    fF = fit_power(Narr, eF)
    fSig = fit_power(Narr, sig)
    fits["F0.20_total"] = fF
    fits["F0.20_sampling_sigma"] = fSig
    print(f"  total |F_N-F_inf|     : delta={fF['delta']:.4f}  R^2={fF['r2']:.4f}")
    print(f"  sampling sigma scale  : delta={fSig['delta']:.4f}  R^2={fSig['r2']:.4f}")
    print(f"  -> if these two deltas match (~1), the CDF 'convergence exponent'")
    print(f"     is the SAMPLING-NOISE FLOOR (sigma~1/sqrt(M), M~N^2 => N^-1),")
    print(f"     NOT a deterministic spectral bias exponent.")

    def clean(o):
        if isinstance(o, dict):
            return {str(k): clean(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [clean(v) for v in o]
        if isinstance(o, (np.floating, np.integer)):
            return o.item()
        return o
    payload = dict(EXY=EXY, Esum=Esum, EXY2=EXY2,
                   Finf={str(k): v for k, v in Finf.items()},
                   Ns=Ns, records=clean(recs), fits=clean(fits),
                   elapsed_s=time.time() - t0)
    with open(RESULT_JSON, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"\nSaved -> {RESULT_JSON}  ({time.time()-t0:.1f}s)")


if __name__ == "__main__":
    main()

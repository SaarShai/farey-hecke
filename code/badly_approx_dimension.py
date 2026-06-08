"""
badly_approx_dimension.py
=========================

The dark band in exp(2) (worst-approximable map, dedekind_cut_explore.py) is not a
curve -- it is a Cantor set: the bounded-type continued fractions
    E_{<=B} = { x in (0,1) : a_k(x) <= B for all k }.
This script MEASURES its Hausdorff dimension two independent ways and overlays the
result on the exp(2) map, turning the ASCII band into a measured fractal.

(A) TRANSFER OPERATOR (Ruelle / thermodynamic formalism -- accurate).
    Inverse branches of the Gauss map: psi_a(x) = 1/(a+x), |psi_a'(x)| = (a+x)^{-2}.
    Transfer operator at parameter s:
        (L_s f)(x) = sum_{a in A} (a+x)^{-2s} f(1/(a+x)).
    dim_H(E_A) = the unique s with leading eigenvalue lambda(s) = 1.
    Discretized by Chebyshev collocation + barycentric interpolation (eigenfunction
    is analytic, maps are strong contractions => geometric convergence).
    Validation anchor: dim_H(E_{1,2}) = 0.5312805062772051416...  (Jenkinson-Pollicott).

(B) BOX-COUNTING (elementary, independent check).
    Cover E_{<=B} by its depth-d cylinder intervals (exact endpoints via the convergent
    recurrence), then count dyadic boxes hit at scales eps=2^-m; slope of log N vs log(1/eps).
    Crude (log corrections) but confirms the transfer value is a real dimension.

Reproduce:  python3 code/badly_approx_dimension.py
"""

from __future__ import annotations
import math, json, os
import numpy as np

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)
try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    HAVE_MPL = True
except Exception:
    HAVE_MPL = False

KNOWN_E12 = 0.5312805062772051416  # dim_H of {a_k in {1,2}}, Jenkinson-Pollicott


# ---- (A) transfer-operator dimension ----------------------------------------
def _cheb(N):
    """Chebyshev-Lobatto nodes on [0,1] + barycentric weights."""
    k = np.arange(N)
    x = 0.5 * (1 - np.cos(np.pi * k / (N - 1)))
    w = np.ones(N); w[1::2] = -1.0; w[0] *= 0.5; w[-1] *= 0.5
    return x, w


def _bary(x, w, Y):
    """Barycentric Lagrange basis matrix L[q,j] = ell_j(Y[q])."""
    diff = Y[:, None] - x[None, :]
    small = np.abs(diff) < 1e-13
    with np.errstate(divide="ignore", invalid="ignore"):
        T = w[None, :] / diff
        denom = np.sum(T, axis=1)
        L = T / denom[:, None]
    for r in np.where(np.any(small, axis=1))[0]:   # exact node hits -> one-hot
        j = int(np.argmax(small[r])); L[r, :] = 0.0; L[r, j] = 1.0
    return L


def transfer_dim(A, N=56):
    """dim_H(E_A) via leading eigenvalue lambda(s)=1 of the transfer operator."""
    x, w = _cheb(N)
    A = list(A)

    def lam(s):
        M = np.zeros((N, N))
        for a in A:
            y = 1.0 / (a + x)
            M += ((a + x) ** (-2.0 * s))[:, None] * _bary(x, w, y)
        return np.max(np.linalg.eigvals(M).real)

    lo, hi = 1e-3, 1 - 1e-9          # lambda(s) decreasing in s
    for _ in range(70):
        mid = 0.5 * (lo + hi)
        if lam(mid) > 1.0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# ---- (B) cylinders + box-counting -------------------------------------------
def cylinders(B, depth):
    """All depth-`depth` cylinder intervals of E_{<=B}, as (lo,hi) sorted.
    Word a_1..a_d -> endpoints p_d/q_d and (p_d+p_{d-1})/(q_d+q_{d-1})."""
    out = []
    # DFS over words, carrying (p_{k-1},q_{k-1}),(p_k,q_k)
    def rec(k, pkm1, qkm1, pk, qk):
        if k == depth:
            a = pk / qk
            b = (pk + pkm1) / (qk + qkm1)
            lo, hi = (a, b) if a < b else (b, a)
            out.append((lo, hi))
            return
        for ai in range(1, B + 1):
            rec(k + 1, pk, qk, ai * pk + pkm1, ai * qk + qkm1)
    rec(0, 1, 0, 0, 1)   # p_{-1}/q_{-1}=1/0, p_0/q_0=0/1
    out.sort()
    return out


def boxcount_dim(intervals, m_lo=5, m_hi=14):
    """Box-count dimension: slope of log N(eps) vs log(1/eps), eps=2^-m."""
    xs, ys = [], []
    for m in range(m_lo, m_hi + 1):
        M = 1 << m
        eps = 1.0 / M
        hit = np.zeros(M, dtype=bool)
        for lo, hi in intervals:
            i0 = max(0, int(lo / eps))
            i1 = min(M - 1, int(hi / eps))
            hit[i0:i1 + 1] = True
        N = int(hit.sum())
        xs.append(math.log(M)); ys.append(math.log(N))
    xs = np.array(xs); ys = np.array(ys)
    # fit upper half (finer scales, where cylinders << eps)
    h = len(xs) // 2
    A = np.vstack([xs[h:], np.ones(len(xs) - h)]).T
    slope = np.linalg.lstsq(A, ys[h:], rcond=None)[0][0]
    return slope, (xs / math.log(2), ys / math.log(2))


# ---- exp(2) map (max partial quotient over circle) --------------------------
def cf_terms(alpha, k_terms=16):
    x = alpha; out = []
    for _ in range(k_terms):
        a = math.floor(x); out.append(a)
        f = x - a
        if f < 1e-12: break
        x = 1.0 / f
    return out


def max_pq(alpha, k=14, cap=40):
    t = cf_terms(alpha, k)[1:]
    return min(cap, max(t)) if t else 0


def main():
    print("===== (A) TRANSFER-OPERATOR Hausdorff dimensions =====")
    d12 = transfer_dim([1, 2])
    print(f"  dim E_{{1,2}}      = {d12:.13f}   (known {KNOWN_E12:.13f}, "
          f"err {abs(d12-KNOWN_E12):.2e})")
    rows = []
    for B in range(2, 11):
        dB = transfer_dim(list(range(1, B + 1)))
        hens = 1 - 6.0 / (math.pi ** 2 * B)        # Hensley leading term
        rows.append((B, dB, hens))
        print(f"  dim E_<=B  B={B:2d}  = {dB:.10f}   Hensley 1-6/(pi^2 B) = {hens:.6f}")
    print("  (Jarnik: dim E_<=B -> 1 as B -> oo  ==  badly-approximable set has full dim)")

    print("\n===== (B) BOX-COUNTING cross-check =====")
    box = {}
    depths = {2: 20, 3: 13, 5: 9}
    for B in (2, 3, 5):
        ivs = cylinders(B, depths[B])
        slope, curve = boxcount_dim(ivs)
        dT = transfer_dim(list(range(1, B + 1)))
        box[B] = (slope, dT, curve, len(ivs))
        print(f"  E_<=B  B={B}: box-count dim = {slope:.4f}   transfer dim = {dT:.6f}"
              f"   ({len(ivs)} cylinders @ depth {depths[B]})")

    json.dump({"E12": d12, "known_E12": KNOWN_E12,
               "dim_table": rows,
               "boxcount": {str(B): {"box": box[B][0], "transfer": box[B][1]} for B in box}},
              open(os.path.join(OUT, "badly_approx_dim.json"), "w"), indent=2)

    if not HAVE_MPL:
        print(f"\noutputs in {OUT}"); return

    # ---- overlay figure ----
    W = 1400
    xs = (np.arange(W) + 0.5) / W
    mpq = np.array([max_pq(x) for x in xs])
    fig = plt.figure(figsize=(12, 8))
    gs = fig.add_gridspec(3, 2, height_ratios=[1.1, 1.4, 1.4], hspace=0.45, wspace=0.25)

    # top: exp(2) map + the E_<=B bands measured
    ax0 = fig.add_subplot(gs[0, :])
    ax0.imshow(mpq.reshape(1, -1), aspect="auto", cmap="magma", extent=[0, 1, 0, 1])
    ax0.set_yticks([])
    PHI = (math.sqrt(5) - 1) / 2
    for r in (PHI, 1 - PHI):
        ax0.axvline(r, color="cyan", lw=0.7, ls="--")
    ax0.set_title("exp(2) worst-approximable map: brightness = max partial quotient. "
                  "Dark band = bounded-type Cantor set E_<=B (dashed = golden)", fontsize=9)
    ax0.set_xlabel("position on fractured circle")

    # mid-left: dim(E_<=B) vs B  (transfer + box + Hensley + Jarnik limit)
    ax1 = fig.add_subplot(gs[1, 0])
    Bs = [r[0] for r in rows]
    ax1.plot(Bs, [r[1] for r in rows], "o-", color="tab:blue", label="transfer dim")
    ax1.plot([B for B in box], [box[B][0] for B in box], "s", color="tab:red",
             ms=8, label="box-count")
    ax1.plot(Bs, [r[2] for r in rows], ":", color="0.5", label="Hensley 1-6/(π²B)")
    ax1.axhline(1.0, color="k", lw=0.8, ls="--")
    ax1.text(8, 0.965, "Jarník limit → 1", fontsize=7)
    ax1.scatter([2], [KNOWN_E12], marker="*", s=120, color="gold", zorder=5,
                label=f"known E_{{1,2}}={KNOWN_E12:.5f}")
    ax1.set_xlabel("B (max partial quotient)"); ax1.set_ylabel("Hausdorff dim")
    ax1.set_title("dim_H(E_<=B): two methods agree", fontsize=9)
    ax1.legend(fontsize=6)

    # mid-right: box-count log-log lines
    ax2 = fig.add_subplot(gs[1, 1])
    for B, col in zip((2, 3, 5), ("tab:green", "tab:orange", "tab:purple")):
        lx, ly = box[B][2]
        ax2.plot(lx, ly, "o-", ms=3, color=col, label=f"B={B} (slope {box[B][0]:.3f})")
    ax2.set_xlabel("log2(1/eps)"); ax2.set_ylabel("log2 N(eps)")
    ax2.set_title("box-count: slope = dimension", fontsize=9); ax2.legend(fontsize=6)

    # bottom: the actual Cantor sets E_<=B as cylinder unions, labeled with dim
    ax3 = fig.add_subplot(gs[2, :])
    for i, B in enumerate((2, 3, 5)):
        ivs = cylinders(B, {2: 14, 3: 9, 5: 7}[B])
        y = len((2, 3, 5)) - 1 - i
        for lo, hi in ivs:
            ax3.add_patch(plt.Rectangle((lo, y + 0.1), hi - lo, 0.8,
                          color=["tab:green", "tab:orange", "tab:purple"][i]))
        ax3.text(1.005, y + 0.5, f"E_<=" + f"{B}  dim={box[B][1]:.4f}", fontsize=8,
                 va="center")
    ax3.set_xlim(0, 1); ax3.set_ylim(0, 3); ax3.set_yticks([])
    ax3.set_title("the Cantor sets themselves (cylinder unions) -- self-similar gaps at every scale",
                  fontsize=9)
    ax3.set_xlabel("x")

    p = os.path.join(OUT, "badly_approx_dimension.png")
    fig.savefig(p, dpi=120, bbox_inches="tight"); plt.close(fig)
    print(f"\n  [plot] {p}\noutputs in {OUT}")


if __name__ == "__main__":
    main()

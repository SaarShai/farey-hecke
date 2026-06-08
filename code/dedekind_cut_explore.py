"""
dedekind_cut_explore.py
=======================

Irrationals as Dedekind cuts on the fractured (Farey/Stern-Brocot) circle.

Three experiments, all hung off the existing CF / Stern-Brocot bracketing
machinery (cf. code/hardware_approx_demo.py cf_convergents, and
projects/mimo-mini-project/code/E6_prime_denom_farey.py prime-denominator Farey):

  (1) CF READOUT / DWELL   -- bracket a target irrational alpha by the mediant
      walk; show the "dwell" of each convergent == its partial quotient a_k;
      log(gap) vs step slope == irrationality measure. Confirms: a spike in the
      per-step delta IS a large partial quotient IS an exceptional rational
      approximation.

  (2) WORST-APPROXIMABLE MAP -- color the circle [0,1) by max partial quotient
      over the first K CF terms. Noble numbers (golden translates) stay dark
      (badly approximable); neighborhoods of low rationals spike bright.

  (3) PRIME vs FULL -- bracket the same alpha with full Farey (any q<=N) vs
      prime-denominator Farey (q prime <=N). The gap-shrink gap_prime/gap_full
      is the arithmetic signal beyond the bare Dedekind cut.

Outputs: code/out/*.png (if matplotlib) + code/out/*.json + an ASCII summary
to stdout (headless-friendly).

Reproduce:  python3 code/dedekind_cut_explore.py
"""

from __future__ import annotations
import math, json, os
from fractions import Fraction

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAVE_MPL = True
except Exception:
    HAVE_MPL = False

# ---- targets (fractional parts, all in (0,1)) -------------------------------
PHI = (math.sqrt(5) - 1) / 2          # 1/phi = [0;1,1,1,...]  -- worst approximable
TARGETS = {
    "phi-1  (golden)": PHI,
    "sqrt2-1":         math.sqrt(2) - 1,
    "pi-3":            math.pi - 3,
    "e-2":             math.e - 2,
    "liouville":       sum(10.0 ** (-math.factorial(k)) for k in range(1, 8)),
}


# ---- continued fraction (independent cross-check) ---------------------------
def cf_terms(alpha: float, n_terms: int = 25):
    """Simple continued fraction [a0; a1, a2, ...] of alpha (float)."""
    x = alpha
    out = []
    for _ in range(n_terms):
        a = math.floor(x)
        out.append(a)
        frac = x - a
        if frac < 1e-12:
            break
        x = 1.0 / frac
    return out


def convergents(terms):
    """Convergents p_k/q_k from CF terms."""
    p_m1, p_m2 = 1, 0
    q_m1, q_m2 = 0, 1
    out = []
    for a in terms:
        p = a * p_m1 + p_m2
        q = a * q_m1 + q_m2
        out.append((p, q))
        p_m2, p_m1 = p_m1, p
        q_m2, q_m1 = q_m1, q
    return out


# ---- (1) mediant walk: the Dedekind cut, realized one bit at a time ----------
def mediant_walk(alpha: float, steps: int = 60):
    """Stern-Brocot bracket of alpha in (0,1). Returns per-step records.

    Bracket left=a/b < alpha < c/d=right, always unimodular (bc - ad = 1),
    so gap = c/d - a/b = 1/(b*d)  -- exactly the Lean gap formula
    Unimodular.rat_sub. Each step inserts the mediant (a+c)/(b+d). A run of
    same-direction moves with one endpoint frozen == one partial quotient.
    """
    a, b, c, d = 0, 1, 1, 1          # 0/1 .. 1/1
    recs = []
    last_dir = None
    run = 0
    for k in range(steps):
        mp, mq = a + c, b + d        # mediant
        gap = 1.0 / (b * d)          # = c/d - a/b
        m = mp / mq
        if alpha > m:                # cut lies right -> raise the left endpoint
            a, b = mp, mq
            direction = "R"
        else:                        # cut lies left -> lower the right endpoint
            c, d = mp, mq
            direction = "L"
        if direction == last_dir:
            run += 1
        else:
            if last_dir is not None:
                recs.append({"dir": last_dir, "run": run})
            last_dir = direction
            run = 1
        recs.append({"step": k, "gap": gap, "mediant_q": mq,
                     "left": (a, b), "right": (c, d), "dir": direction})
    runs = [r for r in recs if "run" in r]
    walk = [r for r in recs if "step" in r]
    return walk, runs


def run_lengths(walk):
    """Collapse the L/R move string into run lengths (== CF partial quotients,
    up to the standard first-term / last-term convention)."""
    moves = "".join(r["dir"] for r in walk)
    out, i = [], 0
    while i < len(moves):
        j = i
        while j < len(moves) and moves[j] == moves[i]:
            j += 1
        out.append((moves[i], j - i))
        i = j
    return out


def experiment_1():
    print("\n===== (1) CF READOUT / DWELL =====")
    report = {}
    for name, a in TARGETS.items():
        walk, _ = mediant_walk(a, steps=60)
        rl = run_lengths(walk)
        terms = cf_terms(a, 14)
        gaps = [r["gap"] for r in walk]
        # log-gap slope per step == approximation rate (steeper => more approximable)
        ks = list(range(len(gaps)))
        loggaps = [math.log10(g) for g in gaps]
        n = len(ks)
        mx = sum(ks) / n
        my = sum(loggaps) / n
        slope = (sum((ks[i] - mx) * (loggaps[i] - my) for i in range(n))
                 / sum((ks[i] - mx) ** 2 for i in range(n)))
        run_seq = [c for _, c in rl]
        maxpq = max(terms[1:]) if len(terms) > 1 else 0
        print(f"\n  {name}")
        print(f"    CF terms          : {terms}")
        print(f"    walk run-lengths  : {run_seq[:12]}   == CF a_k (up to leading/last-term convention)")
        print(f"    max partial quot. : {maxpq:>7}   (large = exceptional rational approximation)")
        print(f"    log10(gap)/step   : {slope:+.3f}   (steep = steady shrink/golden;"
              f" flat = long dwell on a big a_k)")
        report[name] = {"cf_terms": terms, "run_lengths": run_seq,
                        "max_pq": maxpq, "loggap_slope": slope}
    json.dump(report, open(os.path.join(OUT, "exp1_dwell.json"), "w"), indent=2)

    if HAVE_MPL:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.2))
        for name, a in TARGETS.items():
            walk, _ = mediant_walk(a, steps=60)
            gaps = [r["gap"] for r in walk]
            ax1.semilogy(range(len(gaps)), gaps, label=name, lw=1.4)
            rl = [c for _, c in run_lengths(walk)]
            ax2.plot(range(len(rl)), rl, marker="o", ms=3, label=name, lw=1.0)
        ax1.set_title("(1) bracket gap = 1/(b·d) vs mediant step\n"
                      "flatter = badly approximable (golden); cliffs = big a_k")
        ax1.set_xlabel("mediant step"); ax1.set_ylabel("gap"); ax1.legend(fontsize=7)
        ax2.set_title("dwell per convergent  ==  partial quotient a_k\n"
                      "spikes = exceptional rational approximation")
        ax2.set_xlabel("convergent index"); ax2.set_ylabel("dwell = a_k")
        ax2.legend(fontsize=7)
        fig.tight_layout()
        p = os.path.join(OUT, "exp1_dwell.png")
        fig.savefig(p, dpi=120); plt.close(fig)
        print(f"\n  [plot] {p}")


# ---- (2) worst-approximable map over the circle -----------------------------
def max_pq(alpha: float, k_terms: int = 12, cap: int = 30):
    t = cf_terms(alpha, k_terms)[1:]   # drop a0 (integer part = 0 here)
    if not t:
        return 0
    return min(cap, max(t))


def experiment_2(width: int = 1200):
    print("\n===== (2) WORST-APPROXIMABLE MAP =====")
    xs = [(i + 0.5) / width for i in range(width)]
    val = [max_pq(x) for x in xs]
    # noble band: smallest max-PQ; report the darkest x (should hug golden translates)
    order = sorted(range(width), key=lambda i: val[i])
    dark = [round(xs[i], 5) for i in order[:8]]
    print(f"  darkest (most badly-approximable) x ~ {dark}")
    print(f"  golden 1/phi = {PHI:.5f}, 1-1/phi = {1-PHI:.5f}  (expect near darkest)")
    json.dump({"x": xs, "max_pq": val}, open(os.path.join(OUT, "exp2_map.json"), "w"))

    # ASCII sparkline: use MIN over each segment so badly-approximable (noble)
    # bands survive as dark dips instead of saturating.
    bins = 100
    ramp = " .:-=+*#%@"
    line = []
    for b in range(bins):
        seg = val[b * width // bins:(b + 1) * width // bins]
        m = min(seg) if seg else 0
        line.append(ramp[min(len(ramp) - 1, m * (len(ramp) - 1) // 6)])
    print("  circle [0..1], brightness = local floor of max-PQ (dark dips = noble/golden):")
    print("  " + "".join(line))
    g1, g2 = int(PHI * bins), int((1 - PHI) * bins)
    pointer = "".join("^" if i in (g1, g2) else " " for i in range(bins))
    print("  " + pointer + "   (^ = golden translates)")

    if HAVE_MPL:
        import numpy as np
        img = np.array(val).reshape(1, -1)
        fig, ax = plt.subplots(figsize=(12, 1.8))
        ax.imshow(img, aspect="auto", cmap="magma", extent=[0, 1, 0, 1])
        for r in [PHI, 1 - PHI]:
            ax.axvline(r, color="cyan", lw=0.8, ls="--")
        ax.set_yticks([])
        ax.set_title("(2) circle colored by max partial quotient (bright=well approximable; "
                     "dark=noble/golden, dashed)")
        ax.set_xlabel("position on fractured circle")
        fig.tight_layout()
        p = os.path.join(OUT, "exp2_map.png")
        fig.savefig(p, dpi=120); plt.close(fig)
        print(f"  [plot] {p}")


# ---- (3) prime-denominator vs full Farey bracketing -------------------------
def primes_upto(N):
    s = bytearray([1]) * (N + 1)
    s[0] = s[1] = 0
    for i in range(2, int(math.isqrt(N)) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return [i for i in range(2, N + 1) if s[i]]


def best_approx_full(alpha: float, N: int):
    """Best p/q, q<=N, to alpha (Farey neighbor) via convergents+semiconvergents."""
    best_err, best = 1.0, (0, 1)
    p_m1, p_m2, q_m1, q_m2 = 1, 0, 0, 1
    x = alpha
    for _ in range(64):
        a = math.floor(x)
        # semiconvergents a'=1..a refine without exceeding denominators too fast
        for ap in range(1, a + 1):
            q = ap * q_m1 + q_m2
            if q > N:
                break
            p = ap * p_m1 + p_m2
            e = abs(alpha - p / q)
            if e < best_err:
                best_err, best = e, (p, q)
        p = a * p_m1 + p_m2
        q = a * q_m1 + q_m2
        if q > N:
            break
        p_m2, p_m1, q_m2, q_m1 = p_m1, p, q_m1, q
        frac = x - a
        if frac < 1e-12:
            break
        x = 1.0 / frac
    return best_err, best


def best_approx_prime(alpha: float, N: int, primes):
    best_err, best = 1.0, (0, 1)
    for q in primes:
        if q > N:
            break
        p = round(alpha * q)
        for pp in (p - 1, p, p + 1):
            if 0 <= pp <= q:
                e = abs(alpha - pp / q)
                if e < best_err:
                    best_err, best = e, (pp, q)
    return best_err, best


def experiment_3():
    print("\n===== (3) PRIME vs FULL FAREY =====")
    Ns = [2 ** k for k in range(3, 13)]      # 8 .. 4096
    primes = primes_upto(Ns[-1])
    report = {}
    for name, a in TARGETS.items():
        rows = []
        for N in Ns:
            ef, bf = best_approx_full(a, N)
            ep, bp = best_approx_prime(a, N, primes)
            rows.append((N, ef, ep, ef / ep if ep else float("inf")))
        report[name] = rows
        # slope of log err vs log N (full ~ -2 by Dirichlet)
        def slope(idx):
            xs = [math.log10(r[0]) for r in rows]
            ys = [math.log10(r[idx]) for r in rows]
            n = len(xs); mx = sum(xs) / n; my = sum(ys) / n
            return (sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
                    / sum((xs[i] - mx) ** 2 for i in range(n)))
        sf, sp = slope(1), slope(2)
        ratio_last = rows[-1][1] / rows[-1][2] if rows[-1][2] else float("inf")
        print(f"\n  {name}")
        print(f"    log-log err slope  full={sf:+.2f}  prime={sp:+.2f}  "
              f"(full→-2 Dirichlet; prime shallower = thinner set)")
        print(f"    err_full/err_prime at N={Ns[-1]}: {ratio_last:.3e}  (arithmetic signal)")
    json.dump(report, open(os.path.join(OUT, "exp3_prime_vs_full.json"), "w"), indent=2)

    if HAVE_MPL:
        fig, ax = plt.subplots(figsize=(8, 5))
        for name in TARGETS:
            rows = report[name]
            ax.loglog([r[0] for r in rows], [r[1] for r in rows],
                      "-o", ms=3, label=f"{name} full")
            ax.loglog([r[0] for r in rows], [r[2] for r in rows],
                      "--s", ms=3, label=f"{name} prime")
        ax.set_title("(3) best-approx error vs N: full Farey (q≤N) vs prime-denominator")
        ax.set_xlabel("N (denominator bound)"); ax.set_ylabel("|α - p/q| best")
        ax.legend(fontsize=6, ncol=2)
        fig.tight_layout()
        p = os.path.join(OUT, "exp3_prime_vs_full.png")
        fig.savefig(p, dpi=120); plt.close(fig)
        print(f"\n  [plot] {p}")


# ---- (4) per-step / delta time series: the plateau-cliff trace --------------
def step_trace(alpha: float, steps: int = 80):
    """Per mediant step return: gap, per-step log-decrement s_k (how much the
    gap shrank this step), delta_k (change in s_k = second difference), and the
    run-boundary steps with their partial quotient a_k.
    """
    walk, _ = mediant_walk(alpha, steps=steps)
    gaps = [r["gap"] for r in walk]
    dirs = [r["dir"] for r in walk]
    lg = [math.log10(g) for g in gaps]
    s = [0.0] + [lg[k - 1] - lg[k] for k in range(1, len(lg))]   # per-step decrement ≥0
    delta = [0.0] + [s[k] - s[k - 1] for k in range(1, len(s))]  # second difference
    # run boundaries: a run of equal dir == one partial quotient a_k
    bounds, i = [], 0
    while i < len(dirs):
        j = i
        while j < len(dirs) and dirs[j] == dirs[i]:
            j += 1
        bounds.append((j - 1, j - i))   # (step where run ends, a_k)
        i = j
    return gaps, s, delta, bounds


def _spark(vals, lo, hi):
    ramp = " .:-=+*#%@"
    out = []
    span = (hi - lo) or 1.0
    for v in vals:
        t = max(0.0, min(1.0, (v - lo) / span))
        out.append(ramp[int(t * (len(ramp) - 1))])
    return "".join(out)


def experiment_4():
    print("\n===== (4) PER-STEP / DELTA TRACE (plateau-cliff) =====")
    sel = ["pi-3", "e-2", "phi-1  (golden)"]
    report = {}
    for name in sel:
        a = TARGETS[name]
        gaps, s, delta, bounds = step_trace(a, steps=80)
        report[name] = {"per_step_decrement": s, "delta": delta, "runs": bounds}
        smax = max(s) if s else 1.0
        ak = [b[1] for b in bounds]
        print(f"\n  {name}   partial quotients read off at run-ends: {ak[:10]}")
        print(f"    per-step shrink (flat=plateau/dwell, tall=cliff):")
        print("    " + _spark(s, 0.0, smax))
        # mark run-end steps under the sparkline
        mark = [" "] * len(s)
        for bstep, _a in bounds:
            if bstep < len(mark):
                mark[bstep] = "^"
        print("    " + "".join(mark) + "   (^ = a convergent completes)")
    json.dump(report, open(os.path.join(OUT, "exp4_step_trace.json"), "w"), indent=2)

    if HAVE_MPL:
        fig, axes = plt.subplots(len(sel), 1, figsize=(11, 3.0 * len(sel)), sharex=True)
        for ax, name in zip(axes, sel):
            a = TARGETS[name]
            gaps, s, delta, bounds = step_trace(a, steps=80)
            ks = list(range(len(gaps)))
            ax.semilogy(ks, gaps, color="0.3", lw=1.6, label="gap = 1/(b·d)")
            axr = ax.twinx()
            axr.bar(ks, s, color="tab:orange", alpha=0.5, width=0.9,
                    label="per-step log-decrement s_k")
            axr.plot(ks, delta, color="tab:red", lw=0.8, label="delta = Δs_k")
            for bstep, akv in bounds:
                if bstep < len(gaps):
                    ax.axvline(bstep, color="tab:blue", lw=0.6, ls=":")
                    ax.annotate(str(akv), (bstep, gaps[bstep]), fontsize=6,
                                color="tab:blue", ha="center", va="bottom")
            ax.set_ylabel("gap"); axr.set_ylabel("s_k / delta")
            ax.set_title(f"(4) {name}: staircase + per-step shrink + delta "
                         f"(blue ticks = convergent completes, labeled a_k)",
                         fontsize=9)
            ax.legend(fontsize=6, loc="lower left")
            axr.legend(fontsize=6, loc="upper right")
        axes[-1].set_xlabel("mediant step")
        fig.tight_layout()
        p = os.path.join(OUT, "exp4_step_trace.png")
        fig.savefig(p, dpi=120); plt.close(fig)
        print(f"\n  [plot] {p}")


if __name__ == "__main__":
    experiment_1()
    experiment_2()
    experiment_3()
    experiment_4()
    print(f"\noutputs in {OUT}")

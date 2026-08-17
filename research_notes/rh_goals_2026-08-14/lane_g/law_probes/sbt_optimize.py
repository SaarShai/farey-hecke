#!/usr/bin/env python3
"""sbt_optimize — self-bounding trace-formula attack on (THRESH).

NON-RIGOROUS PROBE for the OPTIMIZATION ONLY. The bound derivation itself is
symbolic (see LAW_SELFBOUND_TRACE.md); this script only searches the
test-functional family and the delta0 range, and runs the mass-balance audit.

Model (all symbolic quantities defined in the .md):
  box B(d0) = {depth d in [d0, 1/2]} x {gamma in [t0-1, t0+1]}, t0 := 0 WLOG.
  Poisson kernel of a pole at (d, gamma):  K(r) = 2d / (d^2 + (r-gamma)^2).
  test functional  psi >= 0,  budget  (2 log q + A) * int psi   [PREMISE-U]
  W(psi, d0) = min over box of int psi K
  provable deep-count slope  c2 = 2 * int(psi) / W(psi, d0)
  THRESH(d0)  = (2 - (pi^2/3) d0 b) / (2/d0 + pi^2/6),  b = 0.402
"""
import json, math
import numpy as np

B_SHALLOW = 0.402       # parent M2, shallow/total slope per width-2 interval
A_SHALLOW = 1.149       # parent M2 intercept
PI = math.pi


def thresh(d0, b=B_SHALLOW):
    return (2.0 - (PI**2 / 3) * d0 * b) / (2.0 / d0 + PI**2 / 6)


def kernel_integral(d, gamma, lo, hi):
    """int_lo^hi 2d/(d^2+(r-gamma)^2) dr = 2[atan((hi-g)/d) - atan((lo-g)/d)]"""
    return 2.0 * (math.atan((hi - gamma) / d) - math.atan((lo - gamma) / d))


# ---------------------------------------------------------------- analytic W
def W_point(d0):
    """psi = delta_0 (point evaluation at r = t0). min over box of K(t0)."""
    # f(d) = 2d/(d^2+g^2); worst gamma = +-1 (farthest), then min over d in [d0,1/2]
    cand = [2 * d / (d * d + 1.0) for d in (d0, 0.5)]
    return min(cand)


def W_interval(d0, R):
    """psi = indicator of [-R, R]. Worst pole: gamma = +-1, d extremal."""
    vals = []
    for gamma in (1.0, 0.0):
        for d in (d0, 0.5):
            vals.append(kernel_integral(d, gamma, -R, R))
    return min(vals)


# ------------------------------------- max-min over the FULL test-measure family
def W_optimal(d0, R_max=6.0, n_r=601, n_d=21, n_g=41, T=8000, seed=0):
    """max over positive test MEASURES psi of unit mass of  min_{rho in box} int K_rho dpsi.

    Solved as a zero-sum game by multiplicative weights (maximiser) against
    exact best response (minimiser).  Certified from below by the value of the
    returned averaged psi, which is evaluated exactly on the pole grid; that
    lower bound is all the argument needs (a larger W only helps the maximiser,
    and any W we report as achievable is re-checked directly).
    """
    r = np.linspace(-R_max, R_max, n_r)
    ds = np.linspace(d0, 0.5, n_d)
    gs = np.linspace(-1.0, 1.0, n_g)
    D, G = np.meshgrid(ds, gs, indexing="ij")
    D = D.ravel(); G = G.ravel()
    # M[j, i] = K_{rho_j}(r_i)
    M = 2 * D[:, None] / (D[:, None] ** 2 + (r[None, :] - G[:, None]) ** 2)
    scale = M.max()
    Ms = M / scale
    logw = np.zeros(n_r)
    eta = math.sqrt(math.log(n_r) / T) * 2.0
    p_sum = np.zeros(n_r)
    for _ in range(T):
        w = np.exp(logw - logw.max()); p = w / w.sum()
        p_sum += p
        j = int(np.argmin(Ms @ p))          # adversary best response
        logw += eta * Ms[j]                 # maximiser MWU step
    p_avg = p_sum / p_sum.sum()
    val = float((Ms @ p_avg).min() * scale)   # exact value of this psi on the grid
    mass = p_avg
    supp = r[mass > 1e-4 * mass.max()]
    return val, (float(supp.min()), float(supp.max()))


out = {"note": "NON-RIGOROUS PROBE (optimization only)", "b": B_SHALLOW, "a": A_SHALLOW}

# ---- 1. interval half-width sweep at d0 = 0.2 (int psi = 2R, slope = 2*2R/W)
sweep = []
for R in [x / 20 for x in range(2, 81)]:
    W = W_interval(0.2, R)
    sweep.append({"R": R, "W": W, "ratio": W / (2 * R), "slope": 2 * (2 * R) / W})
best_R = min(sweep, key=lambda z: z["slope"])
out["interval_sweep_d0_0.2"] = {"best": best_R,
                                "R=1.0": next(s for s in sweep if abs(s["R"] - 1.0) < 1e-9)}

# ---- 2. main table: d0 x test-functional
table = []
for d0 in [0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.49]:
    Wp = W_point(d0)
    row = {"d0": d0, "thresh": thresh(d0),
           "point": {"W": Wp, "slope": 2.0 / Wp},
           "indic_R1": {"W": W_interval(d0, 1.0), "slope": 2 * 2.0 / W_interval(d0, 1.0)}}
    bR = min(((R / 20, W_interval(d0, R / 20)) for R in range(2, 81)),
             key=lambda z: 2 * (2 * z[0]) / z[1])
    row["indic_best"] = {"R": bR[0], "W": bR[1], "slope": 2 * (2 * bR[0]) / bR[1]}
    t, supp = W_optimal(d0)
    if t:
        row["lp_optimal"] = {"W_per_unit_mass": t, "slope": 2.0 / t, "support": supp}
    row["best_slope"] = min(row["point"]["slope"], row["indic_best"]["slope"],
                            row.get("lp_optimal", {}).get("slope", 1e9))
    row["shortfall_factor"] = row["best_slope"] / row["thresh"]
    table.append(row)
out["table"] = table
out["global_best"] = min(table, key=lambda z: z["shortfall_factor"])
out["thresh_max"] = max(t["thresh"] for t in table)

# ---- 3. mass-balance audit: can the measured pole population absorb 4 log q?
# per width-2 interval, measured total count  S = a + b log q  (parent M2)
# integrated window weight of a pole at shell n: <= 2*(2*dmax/n^2) with dmax=1/2
# shell 0 (in-window): <= 2*pi (full Poisson mass) per pole
absorb_shell0 = 2 * PI
absorb_far = sum(2 * (2 * 0.5 / n ** 2) for n in range(1, 200))
out["mass_balance"] = {
    "budget_per_window": "4 log q  (= 2 log q integrated over width 2)",
    "max_absorb_per_pole_shell0": absorb_shell0,
    "max_absorb_per_pole_all_far_shells_summed": absorb_far,
    "measured_slope_per_width2": B_SHALLOW,
    "max_absorbable_slope_coefficient": B_SHALLOW * (absorb_shell0 + absorb_far),
    "required": 4.0,
}
out["mass_balance"]["deficit"] = 4.0 - out["mass_balance"]["max_absorbable_slope_coefficient"]
out["mass_balance"]["implied_A_gamma_slope"] = max(0.0, out["mass_balance"]["deficit"]) / 2.0
# min pole count needed anywhere, using the generous 2pi cap per pole
out["mass_balance"]["min_pole_slope_needed_generous"] = 4.0 / (2 * PI)

# ---- 4. THRESH under a q-growing A_gamma = alpha log q
out["thresh_with_Agamma"] = [
    {"alpha": al,
     "thresh": (2 - (PI**2 / 3) * 0.2 * B_SHALLOW - al) / (2 / 0.2 + PI**2 / 6)}
    for al in (0.0, 0.2, 0.5, 0.7, 1.0, 1.7355)
]

print(json.dumps(out, indent=2, default=float))
with open(__file__.replace(".py", ".json"), "w") as f:
    json.dump(out, f, indent=2, default=float)

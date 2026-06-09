"""
verify_d3_round3.py
===================
Independent adversarial verification of d3_rosen_round3.py.

Checks:
  (A) Guardrail anchors: q=3 B=2 -> 0.5312805062772, q=5 B=2/4/8 -> 0.696/0.881/0.949
  (B) Branch image containment: psi_{a,+} and psi_{a,-} maps stay in [-L, L]
  (C) N-convergence of eigenvalues at several (q,B) pairs
  (D) Eigenvalue target is 1, not 0.5 (no "factor-2 symmetry" relapse)
  (E) Re-do C_q fit independently using only the reliable B range
  (F) B*(1-D) monotone behavior check
"""

import math, sys, json, os
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# We reproduce the operator ourselves rather than importing, to be truly independent

KNOWN_E12 = 0.5312805062772051416   # Jenkinson-Pollicott exact value

# ─── Chebyshev-Lobatto collocation ──────────────────────────────────────────

def cheb_nodes_weights(N, a=0.0, b=1.0):
    k = np.arange(N)
    x01 = 0.5 * (1.0 - np.cos(np.pi * k / (N - 1)))
    x = a + (b - a) * x01
    w = np.ones(N); w[1::2] = -1.0; w[0] *= 0.5; w[-1] *= 0.5
    return x, w

def bary_interp_matrix(x_nodes, w_bary, query):
    diff = query[:, None] - x_nodes[None, :]
    small = np.abs(diff) < 1e-13
    with np.errstate(divide="ignore", invalid="ignore"):
        T = w_bary[None, :] / diff
        rs = T.sum(axis=1, keepdims=True)
        P = T / rs
    for r in np.where(small.any(axis=1))[0]:
        j = int(np.argmax(small[r])); P[r,:]=0.; P[r,j]=1.
    return P

# ─── Gauss map (q=3) operator ────────────────────────────────────────────────

def gauss_q3_operator(s, B, N):
    """Standard Gauss map on [0,1], bisect to ev=1."""
    x, w = cheb_nodes_weights(N, 0., 1.)
    M = np.zeros((N, N))
    for a in range(1, B+1):
        denom = a + x
        phi = np.clip(1./denom, 0., 1.)
        wt = denom**(-2.*s)
        M += wt[:,None] * bary_interp_matrix(x, w, phi)
    return M

# ─── Full Rosen operator (q>=4) ──────────────────────────────────────────────

def rosen_operator(s, lam, B, N):
    """
    Full Rosen operator on [0, L=lam/2].
    psi_{a,+}(y) = 1/(a*lam + y):   active when y >= (2 - a*lam^2)/lam (lower_p)
    psi_{a,-}(y) = 1/(a*lam - y):   active when y <= (a*lam^2 - 2)/lam (upper_m)
    Eigenvalue target = 1 (NOT 0.5).
    """
    L = lam / 2.
    x_unit, w = cheb_nodes_weights(N, 0., 1.)
    x = x_unit * L
    M = np.zeros((N, N))
    for a in range(1, B+1):
        al = a * lam

        # psi_{a,+}
        lower_p = (2. - a * lam**2) / lam
        ind_p = (x >= lower_p).astype(float)
        dp = al + x
        phi_p = 1./dp
        phi_p_u = np.clip(phi_p / L, 0., 1.)
        wt_p = dp**(-2.*s)
        P_p = bary_interp_matrix(x_unit, w, phi_p_u)
        M += (wt_p * ind_p)[:,None] * P_p

        # psi_{a,-}
        upper_m = (a * lam**2 - 2.) / lam
        ind_m = (x <= upper_m).astype(float)
        dm = al - x
        safe = dm > 1e-10
        phi_m = np.where(safe, 1./dm, L)
        phi_m_u = np.clip(phi_m / L, 0., 1.)
        wt_m = np.where(safe, dm**(-2.*s), 0.)
        P_m = bary_interp_matrix(x_unit, w, phi_m_u)
        M += (wt_m * ind_m)[:,None] * P_m

    return M

def leading_ev(M):
    return float(np.max(np.linalg.eigvals(M).real))

def bisect_dim(build_fn, kwargs, target=1., lo=0., hi=1.-1e-12, iters=80):
    def ev(s):
        M = build_fn(s=s, **kwargs)
        return leading_ev(M)
    if ev(lo) < target: return 0.
    if ev(hi) > target: return float(hi)
    for _ in range(iters):
        mid = .5*(lo+hi)
        if ev(mid) > target: lo=mid
        else: hi=mid
    return .5*(lo+hi)

def dim_q(q, B, N=80):
    lam = 2.*math.cos(math.pi/q)
    if q==3:
        return bisect_dim(gauss_q3_operator, {'B':B,'N':N})
    else:
        return bisect_dim(rosen_operator, {'lam':lam,'B':B,'N':N})

# ─── CHECK A: Guardrail anchors ───────────────────────────────────────────────

print("=" * 68)
print("CHECK A: Guardrail anchors")
print("=" * 68)

# A1: q=3, B=2
d_a1 = dim_q(3, 2, N=80)
res_a1 = d_a1 - KNOWN_E12
print(f"\nA1  q=3 B=2: computed={d_a1:.15f}")
print(f"    known   ={KNOWN_E12:.15f}")
print(f"    residual={res_a1:.2e}  {'PASS' if abs(res_a1)<1e-10 else 'FAIL *** BAD ***'}")

# A2: q=5 full Rosen
print("\nA2  q=5 full Rosen:")
anchors5 = {1:0.000, 2:0.696, 4:0.881, 8:0.949}
a2_ok = True
for B, tgt in anchors5.items():
    d = dim_q(5, B, N=80)
    err = abs(d - tgt)
    ok = (B==1 and d<0.01) or err<0.005
    if not ok: a2_ok=False
    print(f"    B={B:2d}: {d:.6f}  target~{tgt:.3f}  err={err:.4f}  {'OK' if ok else 'FAIL'}")
print(f"    A2 overall: {'PASS' if a2_ok else 'FAIL *** BAD ***'}")

# ─── CHECK B: Branch images stay in [0, L] ───────────────────────────────────

print("\n" + "=" * 68)
print("CHECK B: Branch image containment in [0, L=lam/2]")
print("=" * 68)

for q in [4, 5, 6, 8, 10, 12]:
    lam = 2.*math.cos(math.pi/q)
    L = lam/2.
    viol = []
    test_x = np.linspace(0., L, 500)
    for a in range(1, 5):
        al = a*lam
        # psi_{a,+}: active for x >= lower_p, image = 1/(a*lam+x)
        lower_p = (2. - a*lam**2)/lam
        mask_p = test_x >= lower_p
        if mask_p.any():
            imgs_p = 1./(al + test_x[mask_p])
            if imgs_p.max() > L+1e-12 or imgs_p.min() < -1e-12:
                viol.append(f"a={a} psi+ out of [0,L]: max={imgs_p.max():.6f}")
        # psi_{a,-}: active for x <= upper_m, image = 1/(a*lam-x)
        upper_m = (a*lam**2 - 2.)/lam
        mask_m = test_x <= upper_m
        if mask_m.any():
            dm = al - test_x[mask_m]
            imgs_m = 1./dm
            if imgs_m.max() > L+1e-12 or imgs_m.min() < -1e-12:
                viol.append(f"a={a} psi- out of [0,L]: max={imgs_m.max():.6f}")
    status = "OK (no violations)" if not viol else f"VIOLATION: {viol}"
    print(f"  q={q:2d} lam={lam:.4f} L={L:.4f}: {status}")

# ─── CHECK C: N-convergence ──────────────────────────────────────────────────

print("\n" + "=" * 68)
print("CHECK C: N-convergence at multiple (q, B)")
print("=" * 68)

test_cases = [(3,2), (5,4), (5,8), (6,8), (8,16), (5,64)]
N_vals = [40, 60, 80, 100, 120]

for (q, B) in test_cases:
    dims_n = []
    for N in N_vals:
        dims_n.append(dim_q(q, B, N=N))
    print(f"\n  q={q} B={B}:")
    print(f"    {'N':>5}  {'D':>12}  {'delta':>12}")
    for i,(N,d) in enumerate(zip(N_vals, dims_n)):
        dlt = abs(d-dims_n[i-1]) if i>0 else float('nan')
        dlt_s = f"{dlt:.2e}" if not math.isnan(dlt) else "        ---"
        print(f"    {N:5d}  {d:12.9f}  {dlt_s}")
    # Reliable if last delta < 1e-4
    last_delta = abs(dims_n[-1]-dims_n[-2])
    reliable = last_delta < 1e-4
    print(f"    => N-convergence: {'RELIABLE (delta<1e-4)' if reliable else f'UNRELIABLE (delta={last_delta:.2e})'}")

# ─── CHECK D: Eigenvalue target 1, not 0.5 ───────────────────────────────────

print("\n" + "=" * 68)
print("CHECK D: Eigenvalue target is 1, not 0.5")
print("=" * 68)

# At the bisected s=dim, leading eigenvalue should be ~1
for (q, B) in [(3,2),(5,4),(6,8)]:
    N=80
    s_star = dim_q(q, B, N=N)
    lam = 2.*math.cos(math.pi/q)
    if q==3:
        M = gauss_q3_operator(s=s_star, B=B, N=N)
    else:
        M = rosen_operator(s=s_star, lam=lam, B=B, N=N)
    ev = leading_ev(M)
    print(f"  q={q} B={B}: s*={s_star:.8f}  leading_ev(s*)={ev:.8f}  "
          f"{'TARGET=1 OK' if abs(ev-1.)<1e-3 else 'ERROR: ev not near 1'}")
    # Also check at s=0: should be > 1 (2B branches contribute)
    if q==3:
        M0 = gauss_q3_operator(s=0., B=B, N=N)
    else:
        M0 = rosen_operator(s=0., lam=lam, B=B, N=N)
    ev0 = leading_ev(M0)
    print(f"           leading_ev(s=0)={ev0:.4f}  [expect > 1, = number of branch weights summed]")

# ─── CHECK E: Independent C_q fit ────────────────────────────────────────────

print("\n" + "=" * 68)
print("CHECK E: Independent C_q fit at reliable B range")
print("=" * 68)

# Compute dims for q=3..12 at B=8,12,16,20,24 (reliable range per agent's report)
B_reliable = [8, 12, 16, 20, 24]
q_vals = list(range(3, 13))

print(f"\nComputing D_q(B) for q=3..12, B in {B_reliable}...")
dim_data = {q: {} for q in q_vals}
for q in q_vals:
    for B in B_reliable:
        d = dim_q(q, B, N=80)
        dim_data[q][B] = d
        sys.stdout.write(f"  q={q} B={B:3d} D={d:.6f}\n")
        sys.stdout.flush()

print("\n--- C_q fit results (B in [8,24], linear regression B*(1-D) = C + c1/B) ---")
print(f"{'q':>3}  {'lam':>7}  {'C_conj':>8}  {'C_fit':>8}  {'ratio':>7}  {'verdict':>12}  {'B*(1-D) at B=24':>18}")
print("-"*75)

C3 = 6./math.pi**2
fit_results = {}
for q in q_vals:
    lam = 2.*math.cos(math.pi/q)
    C_conj = C3/lam
    Bs = np.array(B_reliable, dtype=float)
    Ds = np.array([dim_data[q][B] for B in B_reliable])
    y = Bs*(1.-Ds)
    # Only use points where D < 1 - 1e-6
    mask = Ds < 1.-1e-6
    if mask.sum() >= 3:
        X = np.column_stack([np.ones(mask.sum()), 1./Bs[mask]])
        c,_,_,_ = np.linalg.lstsq(X, y[mask], rcond=None)
        C_fit = float(c[0])
        ratio = C_fit/C_conj
        if 0.90<=ratio<=1.10: verdict="CONFIRMED"
        elif 0.80<=ratio<=1.20: verdict="BORDERLINE"
        else: verdict="REFUTED"
    else:
        C_fit=float('nan'); ratio=float('nan'); verdict="SATD(D~1)"
    y24 = 24.*(1.-dim_data[q][24])
    r24 = y24/C_conj
    fit_results[q] = {'lam':lam,'C_conj':C_conj,'C_fit':C_fit,'ratio':ratio,'verdict':verdict}
    if not math.isnan(ratio):
        print(f"  {q:2d}  {lam:7.4f}  {C_conj:8.5f}  {C_fit:8.5f}  {ratio:7.4f}  {verdict:>12}  y24={y24:.5f}(={r24:.3f}*C)")
    else:
        print(f"  {q:2d}  {lam:7.4f}  {C_conj:8.5f}  {'   N/A':>8}  {'   N/A':>7}  {verdict:>12}  y24={y24:.5f}")

# ─── CHECK F: B*(1-D) monotone check for q=3,5,7 ────────────────────────────

print("\n" + "=" * 68)
print("CHECK F: B*(1-D) monotone behavior — converging or diverging?")
print("=" * 68)

B_check = [4,8,12,16,20,24]
for q in [3,5,7,10]:
    lam = 2.*math.cos(math.pi/q)
    C_conj = C3/lam
    print(f"\n  q={q} C_conj={C_conj:.5f}:")
    prev_y = None
    for B in B_check:
        d = dim_data[q].get(B, dim_q(q,B,N=80))
        if d >= 1.-1e-9:
            print(f"    B={B:3d}: D~1 (saturated)")
            continue
        y = B*(1.-d)
        r = y/C_conj
        trend = ""
        if prev_y is not None:
            if y > prev_y: trend = "↑ (overshooting or approaching from below)"
            else: trend = "↓ (decreasing = may undershoot C)"
        print(f"    B={B:3d}: D={d:.6f}  B*(1-D)={y:.5f}  ratio={r:.4f}  {trend}")
        prev_y = y

print("\n" + "=" * 68)
print("SUMMARY OF INDEPENDENT VERIFICATION")
print("=" * 68)
n_conf = sum(1 for q in q_vals if fit_results[q]['verdict']=="CONFIRMED")
n_bord = sum(1 for q in q_vals if fit_results[q]['verdict']=="BORDERLINE")
n_refu = sum(1 for q in q_vals if fit_results[q]['verdict']=="REFUTED")
n_sat  = sum(1 for q in q_vals if "SATD" in fit_results[q]['verdict'])
print(f"Confirmed: {n_conf}  Borderline: {n_bord}  Refuted: {n_refu}  Saturated: {n_sat}")
print("(using reliable B range 8..24 only)")

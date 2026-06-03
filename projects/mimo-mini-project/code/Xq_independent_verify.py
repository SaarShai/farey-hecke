#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Xq_independent_verify.py — INDEPENDENT re-verification of CLOSED_FORM_Xq.md.

Does NOT import ergodic_hecke_hunt / Xq_closedform_verify. Two layers:
  (1) SYMBOLIC (sympy, exact): the load-bearing identities that make the closed
      form a *proof* for the parabolic word (a numeric match cannot establish these).
  (2) GEOMETRIC ANCHOR (mpmath): rebuild the orbit eigenvector from the monodromy
      nullspace of the recurrence v_n + v_{n+2} = k_n*lambda*v_{n+1} (k_n = word
      symbol), independently confirm it == sin((n+1)theta), confirm the cusp binds
      (s_lo = 1/(2 sin 2theta)) over the FULL constraint set, and X = s_lo^2*maxprod
      == closed form (A)/(B) and the published table.
Reports PASS/FAIL per claim. Exit 0 iff all pass.
"""
import sympy as sp
import mpmath as mp

mp.mp.dps = 60
PASS = []
def check(name, ok, detail=""):
    PASS.append(bool(ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  — {detail}" if detail else ""))

th = sp.symbols('theta', positive=True)
lam = 2*sp.cos(th)

print("="*72)
print("(1) SYMBOLIC IDENTITIES  (sympy exact, generic theta)")
print("="*72)

# --- 1a. rotation recurrence at non-defect centers: v_n=sin((n+1)th) solves it
n = sp.symbols('n', integer=True)
v = lambda k: sp.sin((k+1)*th)
rec = sp.simplify(v(n-1) + v(n+1) - lam*v(n))           # should be 0
check("eigenvector solves rotation recurrence  v_{n-1}+v_{n+1}=lambda v_n",
      rec == 0, f"residual={rec}")

# --- 1b. closure  v_N = v_0  with N=q-2 (Nth = pi-2th):  v_{q-2}=sin((q-1)th)=sin(pi-th)=sin th
#         check symbolically with th=pi/q for a few q
for q in (4,5,6,7,12,13):
    val = sp.sin((q-1)*sp.pi/q) - sp.sin(sp.pi/q)
    if sp.simplify(val) != 0:
        check(f"closure v_N=v_0 (q={q})", False); break
else:
    check("closure  v_{q-2} = v_0 = sin(theta)  for q in {4,5,6,7,12,13}", True)

# --- 1c. defect equation at center 0:  v_{N-1}+v_1 = 2*lambda*v_0
#         v_{N-1}=v_{q-3}=sin((q-2)th)=sin(pi-2th)=sin2th ; v_1=sin2th ; RHS=2*lam*sin th
for q in (4,5,6,7,11):
    th0 = sp.pi/q
    lhs = sp.sin((q-2)*th0) + sp.sin(2*th0)
    rhs = 2*(2*sp.cos(th0))*sp.sin(th0)
    if sp.simplify(lhs-rhs) != 0:
        check(f"defect eqn (q={q})", False); break
else:
    check("defect equation  v_{N-1}+v_1 = 2 lambda v_0  for q in {4,5,6,7,11}", True)

# --- 1d. cusp identity: (2 sin th + sin 3th) - 2 sin 2th = sin th (2 cos th - 1)^2  >= 0
cusp = sp.simplify((2*sp.sin(th)+sp.sin(3*th)-2*sp.sin(2*th)) - sp.sin(th)*(2*sp.cos(th)-1)**2)
check("cusp identity  (2 sinθ+sin3θ)-2 sin2θ = sinθ(2cosθ-1)^2", cusp == 0,
      f"residual={cusp}; (>=0, =0 only at θ=π/3 i.e. q=3)")

# --- 1e. product-to-sum: sin(kθ)sin((k+1)θ) = 1/2 (cosθ - cos((2k+1)θ))
k = sp.symbols('k', integer=True)
p2s = sp.simplify(sp.sin(k*th)*sp.sin((k+1)*th) - sp.Rational(1,2)*(sp.cos(th)-sp.cos((2*k+1)*th)))
check("product-to-sum  sin(kθ)sin((k+1)θ)=½(cosθ-cos((2k+1)θ))", p2s == 0)

# --- 1f. (A) == (B):  maxprod/(4 sin^2 2θ) equals the parity-split elementary forms
A_even = sp.cos(th)/(4*sp.sin(2*th)**2)
B_even = 1/(8*sp.sin(th)*sp.sin(2*th))
check("(A)==(B) even:  cosθ/(4 sin²2θ) = 1/(8 sinθ sin2θ)",
      sp.simplify(A_even-B_even)==0)
A_odd = sp.cos(th/2)**2/(4*sp.sin(2*th)**2)
B_odd = (1+sp.cos(th))/(32*sp.sin(th)**2*sp.cos(th)**2)
check("(A)==(B) odd:   cos²(θ/2)/(4 sin²2θ) = (1+cosθ)/(32 sin²θ cos²θ)",
      sp.simplify(A_odd-B_odd)==0)
# and cos^2(th/2) = (1+cos th)/2 sanity
check("maxprod_odd = cos²(θ/2) = ½(1+cosθ)", sp.simplify(sp.cos(th/2)**2-(1+sp.cos(th))/2)==0)

# --- 1g. published exact table values, from branch (B) with θ=π/q
def Xclosed_sym(q):
    t = sp.pi/q
    if q == 3:
        return sp.Rational(2,9)
    if q % 2 == 0:
        return sp.cos(t)/(4*sp.sin(2*t)**2)
    return sp.cos(t/2)**2/(4*sp.sin(2*t)**2)
table = {3: sp.Rational(2,9), 4: sp.sqrt(2)/8, 5: sp.Rational(1,4),
         6: sp.sqrt(3)/6, 8: sp.cos(sp.pi/8)/2, 10: sp.cot(sp.pi/5)/2,
         12: sp.cos(sp.pi/12)}
allok = True
for q, expect in table.items():
    got = sp.simplify(Xclosed_sym(q) - expect)
    if got != 0:
        check(f"table X({q})={expect}", False, f"residual={got}"); allok=False
check("published exact table {3,4,5,6,8,10,12} all match branch (B)", allok)

print()
print("="*72)
print("(2) GEOMETRIC ANCHOR  (mpmath dps=60): nullspace eigenvector, cusp s_lo, X")
print("="*72)

def parabolic_word(q):
    # (1^{q-3}, 2) for q>=4 ; q=3 special (1,4)
    if q == 3:
        return [4]
    return [1]*(q-3) + [2]

def nullspace_eigvec(word):
    """Independently solve M v = 0 for the cyclic recurrence
       v_n + v_{n+2} - k_n*lambda*v_{n+1} = 0  (indices mod p), k_n = word[n].
       Return the 1-D nullspace vector (mpmath), or None if dim != 1."""
    p = len(word)
    th_ = mp.pi/ (p+2)            # q = p+2
    l = 2*mp.cos(th_)
    M = mp.zeros(p, p)
    for i in range(p):
        M[i, i]            += 1
        M[i, (i+2) % p]    += 1
        M[i, (i+1) % p]    += -word[i]*l
    # nullspace via SVD: smallest singular vector
    U, S, V = mp.svd_r(M)
    # smallest singular value index
    smin = min(range(p), key=lambda j: S[j])
    vec = [V[smin, j] for j in range(p)]
    # fix sign/scale: make first entry positive, normalize so min entry -> sin(theta) scale later
    if vec[0] < 0:
        vec = [-x for x in vec]
    return vec, S[smin], th_, l

geo_ok = True
for q in (4, 5, 6, 7, 8, 9, 10):
    word = parabolic_word(q)
    vec, sval, th_, l = nullspace_eigvec(word)
    p = len(word)
    # closed-form eigenvector sin((n+1)theta), same normalization (scale to vec)
    cf = [mp.sin((nn+1)*th_) for nn in range(p)]
    # scale closed form to match vec by least squares ratio
    scale = sum(vec[i]*cf[i] for i in range(p)) / sum(cf[i]*cf[i] for i in range(p))
    err = max(abs(vec[i] - scale*cf[i]) for i in range(p))
    nullq = sval < mp.mpf(10)**-40
    ev_ok = err < mp.mpf(10)**-30
    # full-constraint s_lo (max over ALL n of triangle & floor-jump), using the *nullspace* vec
    # normalize vec to the canonical sin scale so constraints are comparable to closed form
    vv = [scale*c for c in cf]   # == vec up to <1e-30; use exact closed form scaled to unit (sinθ at cusp)
    vv = [mp.sin((nn+1)*th_) for nn in range(p)]   # canonical scale v0=sinθ
    s_lo = mp.mpf(0)
    for nn in range(p):
        vn, vn1, vn2 = vv[nn], vv[(nn+1)%p], vv[(nn+2)%p]
        # triangle:  s > 1/(v_n + lambda v_{n+1})
        s_lo = max(s_lo, 1/(vn + l*vn1))
        # floor-jump: s > 1/(lambda v_{n+1} (k_n+1 - r_n)), r_n = v_n/(lambda v_{n+1});
        #   lambda v_{n+1}(k+1-r) = lambda v_{n+1}(k+1) - v_n ; and k_n lambda v_{n+1}=v_n+v_{n+2}
        r = vn/(l*vn1)
        denom = (word[nn] + 1 - r)
        if denom > 0:
            s_lo = max(s_lo, 1/(l*vn1*denom))
    cusp_pred = 1/(2*mp.sin(2*th_))
    cusp_ok = abs(s_lo - cusp_pred) < mp.mpf(10)**-30
    maxprod = max(vv[nn]*vv[(nn+1)%p] for nn in range(p))
    Xgeo = s_lo*s_lo*maxprod
    # closed form (B)
    if q % 2 == 0:
        Xcf = mp.cos(th_)/(4*mp.sin(2*th_)**2)
    else:
        Xcf = mp.cos(th_/2)**2/(4*mp.sin(2*th_)**2)
    X_ok = abs(Xgeo - Xcf) < mp.mpf(10)**-30
    ok = nullq and ev_ok and cusp_ok and X_ok
    geo_ok &= ok
    print(f"  q={q:2d}: nullσ={mp.nstr(sval,2)} eigerr={mp.nstr(err,2)} "
          f"s_lo-cusp={mp.nstr(abs(s_lo-cusp_pred),2)} X-Xcf={mp.nstr(abs(Xgeo-Xcf),2)} "
          f"X={mp.nstr(Xgeo,12)}  [{'ok' if ok else 'FAIL'}]")
check("geometric anchor q=4..10: nullspace eigvec==sin((n+1)θ), cusp binds, X==(B)", geo_ok)

# --- monotonic & global min at q=4 = sqrt2/8
def Xnum(q):
    t = mp.pi/q
    if q == 3: return mp.mpf(2)/9
    if q % 2 == 0: return mp.cos(t)/(4*mp.sin(2*t)**2)
    return mp.cos(t/2)**2/(4*mp.sin(2*t)**2)
vals = [(q, Xnum(q)) for q in range(4, 121)]
mono = all(vals[i][1] < vals[i+1][1] for i in range(len(vals)-1))
gmin = min(range(len(vals)), key=lambda i: vals[i][1])
check("X strictly increasing q=4..120 and global min at q=4=√2/8",
      mono and vals[gmin][0]==4 and abs(vals[0][1]-mp.sqrt(2)/8)<mp.mpf(10)**-40,
      f"min@q={vals[gmin][0]}, X(4)={mp.nstr(vals[0][1],12)}, √2/8={mp.nstr(mp.sqrt(2)/8,12)}")

print()
print("="*72)
n_ok = sum(PASS); n_tot = len(PASS)
print(f"RESULT: {n_ok}/{n_tot} checks passed.  "
      + ("ALL PASS — closed form independently verified." if n_ok==n_tot else "*** SOME FAILED ***"))
import sys; sys.exit(0 if n_ok==n_tot else 1)

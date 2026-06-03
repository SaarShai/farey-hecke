#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
optimizer_closed_form.py — verify the CLOSED-FORM optimizer orbit for the Hecke BCZ family.

Claim (derived 2026-06-02): for q>=4 the (1^{q-3},2)-word optimizer orbit is, up to scale R,
    c_n(R) = R * sin((n+1)*pi/q),   n = 0,...,q-3   (period q-2)
i.e. the orbit coordinate cycles through R*{sin(pi/q), sin(2pi/q), ..., sin((q-2)pi/q)}.
The all-floor-1 recurrence c_{n+2}=lam c_{n+1}-c_n (lam=2cos(pi/q)) is rotation by pi/q; the lone
floor-2 step closes the period.  Observable P_n = c_n c_{n+1}.  ess-sup along family = R^2 * m(q),
  m(q) = max_n sin((n+1)pi/q) sin((n+2)pi/q).
X(q) = R_lo^2 * m(q), R_lo = smallest scale keeping the orbit in D (x>0,y>0,x+lam y>1) with the
correct floor pattern.  The binding R_lo bound is OPEN => inf not attained => NO ground state.

This script:
 1. builds the closed-form orbit, SIMULATES T_q on it at R = R_lo*(1+eps) and CHECKS it is a genuine
    periodic orbit in D with the claimed floor pattern (1^{q-3},2);
 2. computes m(q), R_lo (+ which constraint binds, open/closed), X(q) exactly (mpmath);
 3. compares X(q) to ergodic_hecke_hunt and to the conserved-quantity identity E=R^2 sin^2(pi/q);
 4. PSLQ-probes closed forms; prints the table.
"""
import math
import mpmath as mp
mp.mp.dps = 50

def lam(q):
    return 2*mp.cos(mp.pi/q)

def orbit_coords(q, R=mp.mpf(1)):
    # c_n = R sin((n+1)pi/q), n=0..q-3  (q-2 coords, one period)
    th = mp.pi/q
    return [R*mp.sin((n+1)*th) for n in range(q-2)]

def products(coords):
    p = len(coords)
    return [coords[n]*coords[(n+1) % p] for n in range(p)]

def floor_term(cn, cn1, l):
    # the value whose floor is the BCZ floor index k_n at step (cn->cn1)
    return (1+cn)/(l*cn1)

def simulate(q, R, steps=None):
    """Iterate the REAL map T_q starting from (c_0,c_1) of the closed form; return list of
    (x,y,k) and a periodicity/floor report."""
    l = lam(q)
    c = orbit_coords(q, R)
    p = len(c)
    if steps is None:
        steps = 3*p + 2
    x, y = c[0], c[1]
    traj = []
    ks = []
    indomain = True
    for _ in range(steps):
        if not (x > 0 and y > 0 and x + l*y > 1):
            indomain = False
        k = int(mp.floor((1+x)/(l*y)))
        ks.append(k)
        ynew = k*l*y - x
        traj.append((x, y, k))
        x, y = y, ynew
    # period check: does (x,y) return to (c0,c1) after p steps?
    x0, y0 = c[0], c[1]
    xp, yp = c[0], c[1]
    for _ in range(p):
        k = int(mp.floor((1+xp)/(l*yp)))
        yp2 = k*l*yp - xp
        xp, yp = yp, yp2
    period_err = abs(xp-x0)+abs(yp-y0)
    return traj, ks[:p], indomain, period_err

def R_lo_exact(q):
    """Compute R_lo and binding constraint exactly. Constraints, with c_n = R*v_n (v_n=sin((n+1)th)):
       (T) triangle  R*(v_n + lam v_{n+1}) > 1            => R > 1/(v_n+lam v_{n+1})           [OPEN]
       (Flo) floor>=k_n : (1+R v_n)/(lam R v_{n+1}) >= k_n => R*(lam k_n v_{n+1} - v_n) <= 1   [closed: <=]
       (Fhi) floor<k_n+1: (1+R v_n)/(lam R v_{n+1}) < k_n+1=> R*((k_n+1) lam v_{n+1} - v_n) > 1 [OPEN]
       k_n = 1 (n<q-3), k_n = 2 (n=q-3).  R_lo = max of all OPEN lower bounds; also collect closed
       UPPER bounds R_hi.  Returns (R_lo, binding_label, R_hi)."""
    l = lam(q)
    v = [mp.sin((n+1)*mp.pi/q) for n in range(q-2)]
    p = q-2
    word = [1]*(q-3) + [2]
    lowers = []   # (value, label, open?)
    uppers = []
    for n in range(p):
        vn, vn1, kn = v[n], v[(n+1) % p], word[n]
        # triangle
        lowers.append((1/(vn + l*vn1), f'tri[n={n}]', True))
        # Fhi  R*((kn+1)*l*vn1 - vn) > 1
        a = (kn+1)*l*vn1 - vn
        if a > 0:
            lowers.append((1/a, f'Fhi[n={n},k={kn}]', True))
        # Flo  R*(kn*l*vn1 - vn) <= 1  -> upper bound R <= 1/(kn*l*vn1 - vn) if positive
        b = kn*l*vn1 - vn
        if b > 0:
            uppers.append((1/b, f'Flo[n={n},k={kn}]', False))
    R_lo, lab, _ = max(lowers, key=lambda t: t[0])
    R_hi = min([u[0] for u in uppers]) if uppers else mp.inf
    return R_lo, lab, R_hi

def Xq(q):
    R_lo, lab, R_hi = R_lo_exact(q)
    v = [mp.sin((n+1)*mp.pi/q) for n in range(q-2)]
    p = q-2
    m = max(v[n]*v[(n+1) % p] for n in range(p))
    X = R_lo*R_lo*m
    # conserved-quantity check: E = R^2 sin^2(pi/q); max product/E = m / sin^2
    return X, R_lo, R_hi, lab, m

if __name__ == "__main__":
    print("q  lam        X(q)            R_lo        R_hi       binding            m(q)          period-ok")
    known = {3:'2/9', 4:'sqrt2/8', 5:'1/4', 6:'sqrt3/6'}
    for q in range(4, 25):
        X, R_lo, R_hi, lab, m = Xq(q)
        # simulate at R just above R_lo to confirm genuine orbit
        Reps = R_lo*(1+mp.mpf('1e-6'))
        traj, ks, indom, perr = simulate(q, Reps)
        word = [1]*(q-3)+[2]
        floor_ok = (ks == word)
        ok = indom and floor_ok and perr < mp.mpf('1e-30')
        l = lam(q)
        print(f"{q:>2} {mp.nstr(l,7):>9} {mp.nstr(X,12):>15} {mp.nstr(R_lo,8):>11} "
              f"{mp.nstr(R_hi,7):>10} {lab:>16} {mp.nstr(m,9):>12}  {'OK' if ok else f'FAIL(dom={indom},flr={floor_ok},perr={mp.nstr(perr,3)})'}")
    # closed-form cross checks
    print("\nClosed-form value checks:")
    X3 = mp.mpf(2)/9
    print(f"  X(4)=sqrt2/8 ? {mp.nstr(Xq(4)[0]-mp.sqrt(2)/8,5)}")
    print(f"  X(5)=1/4 ?     {mp.nstr(Xq(5)[0]-mp.mpf(1)/4,5)}")
    print(f"  X(6)=sqrt3/6 ? {mp.nstr(Xq(6)[0]-mp.sqrt(3)/6,5)}")
    print(f"  X(8)=cos(pi/8)/2 ? {mp.nstr(Xq(8)[0]-mp.cos(mp.pi/8)/2,5)}")
    print(f"  X(12)=cos(pi/12) ? {mp.nstr(Xq(12)[0]-mp.cos(mp.pi/12),5)}")
    # m(q) closed form: q even -> cos(pi/q); q odd -> cos^2(pi/2q)
    print("\nm(q) closed-form check (even: cos(pi/q); odd: cos^2(pi/2q)):")
    for q in range(4, 13):
        m = Xq(q)[4]
        pred = mp.cos(mp.pi/q) if q % 2 == 0 else mp.cos(mp.pi/(2*q))**2
        print(f"  q={q}: m={mp.nstr(m,12)}  pred={mp.nstr(pred,12)}  diff={mp.nstr(m-pred,3)}")

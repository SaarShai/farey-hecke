#!/usr/bin/env python3
"""
CRUX numerics for X_Omega(q) = 1/lambda^3 vs  > 1/lambda^3.

Two engines / two observables (this distinction is the whole resolution):

  (A) SCALAR engine   Tmap(a,b) = (b, floor((1+a)/(lam b))*lam b - a),  observable Pprod = a*b,
      domain Dcorr = {0<a<=1, 0<b<=1, a+lam b>1, lam a+b>1}.   << the audit's 1.39 figure lives here >>

  (B) GENUINE engine  Tgen on the active branch, observable Pgen(a,b) = a(a+lam b)/lam,
      domain Taha = {0<a<=1, 1-lam a < b <= 1, b<=1}.          << the verified >= 1/lam^3 lives here >>

The verified Lean lower bound is for Pgen on Taha (genuine engine).  The cusp tip
(s,0), s in (1/lam, 1], is Tcusp-invariant AND in Taha (since 1-lam*s < 0 = b for s>1/lam),
with Pgen(s,0) = s^2/lam.  As s -> (1/lam)+, Pgen(s,0) -> 1/lam^3 from ABOVE.

We test:  does inf over near-cusp orbits of (max Pgen along orbit) descend to 1/lam^3?

mpmath dps>=60, exact algebraic lambda = 2 cos(pi/q).
"""
import mpmath as mp
mp.mp.dps = 60

def lam(q):
    return 2*mp.cos(mp.pi/q)

def floor_mp(x):
    return mp.floor(x)

# ---------- SCALAR engine (Pprod = a*b, Tmap, Dcorr) ----------
def Tmap(l, a, b):
    if b == 0:
        return (b, -a)  # Lean junk convention x/0=0
    k = floor_mp((1+a)/(l*b))
    return (b, k*l*b - a)

def Pprod(l, a, b):
    return a*b

def in_Dcorr(l, a, b):
    return (0 < a <= 1) and (0 < b <= 1) and (a+l*b > 1) and (l*a+b > 1)

# ---------- GENUINE observable ----------
def Pgen(l, a, b):
    return a*(a+l*b)/l

def in_Taha(l, a, b):
    return (0 < a <= 1) and (1 - l*a < b <= 1)

# ============================================================
# PART 1.  Cusp-tip Dirac value (the genuine UPPER-bound witness).
#   Pgen(s,0) = s^2/lam,  s in (1/lam, 1].  inf over s of s^2/lam attained as s->1/lam+.
# ============================================================
def part1():
    print("="*78)
    print("PART 1: Genuine cusp-tip Dirac.  Pgen(s,0)=s^2/lam,  ground = 1/lam^3 at s=1/lam+")
    print("="*78)
    print(f"{'q':>3} {'1/lam^3':>16} {'Pgen(s=1/lam)':>16} {'ratio':>10}  {'in Taha?(s=1/lam)':>18}")
    for q in [5,7,8,13]:
        l = lam(q)
        inv = 1/l**3
        s = 1/l            # the tip itself
        val = s**2/l       # = 1/lam^3 exactly
        # Taha at the exact tip needs 1-lam*s < 0  i.e. s>1/lam STRICT -> tip itself is boundary
        taha_tip = in_Taha(l, s, mp.mpf(0))
        print(f"{q:>3} {mp.nstr(inv,12):>16} {mp.nstr(val,12):>16} {mp.nstr(val/inv,8):>10}  {str(taha_tip):>18}")
    print()
    print("Now scan s -> (1/lam)+ : Pgen(s,0)=s^2/lam descends to 1/lam^3 from ABOVE,")
    print("and (s,0) is in Taha for every s>1/lam (genuine engine). This realizes inf<=1/lam^3.")
    for q in [5,7,13]:
        l = lam(q); inv = 1/l**3
        print(f"  q={q}, lam={mp.nstr(l,10)}, 1/lam^3={mp.nstr(inv,10)}")
        for eps in [mp.mpf('1e-1'), mp.mpf('1e-2'), mp.mpf('1e-3'), mp.mpf('1e-6')]:
            s = 1/l + eps
            val = s**2/l
            taha = in_Taha(l, s, mp.mpf(0))
            print(f"    s=1/lam+{mp.nstr(eps,2)}: Pgen(s,0)={mp.nstr(val,12)}  ratio={mp.nstr(val/inv,10)}  inTaha={taha}")
    print()

# ============================================================
# PART 2.  Near-cusp ORBIT segments: inf over orbits of (max Pgen).
#   Build interior orbits that SHADOW the cusp for k steps. We approach the
#   cusp parabolic fixed line along the genuine map and measure max Pgen.
#   Reconcile the audit's "1.39" (which was Pprod on the scalar engine).
# ============================================================
def part2_scalar():
    print("="*78)
    print("PART 2a: SCALAR engine reconciliation (the audit's 1.39 figure).")
    print("  inf over staying-in-Dcorr orbits of (running-sup Pprod) / (1/lam^3).")
    print("="*78)
    import random
    random.seed(11)
    print(f"{'q':>3} {'1/lam^3':>14} {'inf sup Pprod':>16} {'ratio':>10} {'#staying':>9}")
    for q in [5,7,8]:
        l = lam(q); inv = 1/l**3
        best = None; nstay = 0
        NSEED = 4000; STEPS = 1500
        for _ in range(NSEED):
            # corridor-edge biased seed
            a = mp.mpf(random.random())*0.5+0.4
            b = mp.mpf(random.random())*0.5+0.4
            if not in_Dcorr(l,a,b): continue
            sup = mp.mpf(0); ok = True
            ca, cb = a, b
            for _ in range(STEPS):
                if not in_Dcorr(l,ca,cb): ok=False; break
                p = Pprod(l,ca,cb)
                if p>sup: sup=p
                ca, cb = Tmap(l,ca,cb)
            if ok:
                nstay += 1
                if best is None or sup<best: best=sup
        if best is not None:
            print(f"{q:>3} {mp.nstr(inv,10):>14} {mp.nstr(best,12):>16} {mp.nstr(best/inv,8):>10} {nstay:>9}")
        else:
            print(f"{q:>3} {mp.nstr(inv,10):>14} {'(none stayed)':>16} {'--':>10} {nstay:>9}")
    print()

def part2_genuine_orbits():
    """
    Genuine-engine near-cusp orbits via the scalar branch closed form
    (a,b)->(b, -a + k lam b), k=floor((1+a)/(lam b)), with Pgen=a(a+lam b)/lam.
    Build orbits whose ENTRY shadows the cusp parabolic line longer and longer:
    start near the cusp tip (1/lam, eps) and follow the floor-1 corridor (rotation).
    Measure min over such orbits of (max Pgen).
    """
    print("="*78)
    print("PART 2b: GENUINE-observable near-cusp orbits.  Pgen=a(a+lam b)/lam.")
    print("  Start near cusp tip; longer shadowing => does max Pgen -> 1/lam^3 from above?")
    print("="*78)
    for q in [5,7,13]:
        l = lam(q); inv = 1/l**3
        print(f"  q={q}  lam={mp.nstr(l,12)}  1/lam^3={mp.nstr(inv,12)}")
        print(f"    {'b0 (cusp dist)':>16} {'len in Taha':>12} {'max Pgen':>16} {'ratio':>10} {'min Pgen':>16}")
        for b0 in [mp.mpf('0.2'),mp.mpf('0.1'),mp.mpf('0.05'),mp.mpf('0.02'),
                   mp.mpf('0.01'),mp.mpf('0.005'),mp.mpf('0.001'),mp.mpf('0.0001')]:
            a0 = 1/l + b0*0   # sit a at 1/lam (cusp first coord); vary b -> 0
            a0 = 1/l
            # ensure in Taha: need 1-lam*a0 < b0  -> 1-1=0<b0 OK
            ca, cb = a0, b0
            mx = mp.mpf('-inf'); mn = mp.mpf('inf'); length=0
            for _ in range(4000):
                if not in_Taha(l,ca,cb): break
                p = Pgen(l,ca,cb)
                if p>mx: mx=p
                if p<mn: mn=p
                length+=1
                # scalar-branch genuine step
                if cb==0: break
                k = floor_mp((1+ca)/(l*cb))
                na, nb = cb, -ca + k*l*cb
                ca, cb = na, nb
            if length>0 and mp.isfinite(mx):
                print(f"    {mp.nstr(b0,10):>16} {length:>12} {mp.nstr(mx,12):>16} {mp.nstr(mx/inv,8):>10} {mp.nstr(mn,12):>16}")
            else:
                print(f"    {mp.nstr(b0,10):>16} {length:>12} {'(escaped)':>16} {'--':>10} {'--':>16}")
        print()

# ============================================================
# PART 3.  THEORY CHECK: energy ellipse = rotation by pi/q.
#   On a floor-1 corridor (c,d)->(d, lam d - c); conserved E = c^2 - lam c d + d^2.
#   As the corridor entry -> cusp tip, E -> tip energy; does max Pgen along the
#   discrete arc -> Pgen(tip)=1/lam^3, or overshoot (positive gap)?
# ============================================================
def part3_energy_arc():
    print("="*78)
    print("PART 3: Energy-ellipse arc near the cusp.  E=c^2-lam c d+d^2 (rotation by pi/q).")
    print("  Pgen along a floor-1 corridor; as entry->cusp tip, does sup Pgen->1/lam^3?")
    print("="*78)
    for q in [5,7,13]:
        l = lam(q); inv = 1/l**3
        theta = mp.pi/q   # rotation angle of R=[[0,1],[-1,lam]] is pi/q (eigenvalues e^{+-i pi/q})
        print(f"  q={q}  lam={mp.nstr(l,12)}  rotation angle pi/q={mp.nstr(theta,10)}  1/lam^3={mp.nstr(inv,12)}")
        # Pure rotation corridor: parametrize the energy ellipse, take discrete pi/q steps.
        # Entry near cusp tip (a~1/lam, b~0). On a corridor Pgen(c,d)=c(c+lam d)/lam.
        # As b0->0 the corridor is a tiny arc near (1/lam,0); supPgen -> Pgen(1/lam,0)=1/lam^3.
        print(f"    {'entry b0':>12} {'supPgen/inv':>14} {'#steps floor=1':>15}")
        for b0 in [mp.mpf('0.1'),mp.mpf('0.01'),mp.mpf('0.001'),mp.mpf('1e-4'),mp.mpf('1e-5'),mp.mpf('1e-6')]:
            c, d = 1/l, b0
            sup = mp.mpf('-inf'); steps=0
            for _ in range(8000):
                if not in_Taha(l,c,d): break
                p = Pgen(l,c,d)
                if p>sup: sup=p
                if d==0: break
                k = floor_mp((1+c)/(l*d))
                if k!=1: break   # only the pure-rotation (floor-1) corridor
                nc, nd = d, l*d - c
                c, d = nc, nd
                steps+=1
            if mp.isfinite(sup):
                print(f"    {mp.nstr(b0,4):>12} {mp.nstr(sup/inv,10):>14} {steps:>15}")
            else:
                print(f"    {mp.nstr(b0,4):>12} {'(none)':>14} {steps:>15}")
        print()

if __name__ == "__main__":
    part1()
    part2_scalar()
    part2_genuine_orbits()
    part3_energy_arc()

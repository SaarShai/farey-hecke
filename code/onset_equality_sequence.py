#!/usr/bin/env python3
"""
DECISIVE TEST: does there exist a SEQUENCE of Tgen-invariant probability measures
mu_n supported on the OPEN section D = Taha ∩ {0<b} (b STRICTLY positive) with
ess-sup_{mu_n} Pgen -> 1/lam^3 ?

The verified lower-bound theorem (perq_Xomega_lb_qge19_GEN') quantifies over EXACTLY
mu with mu((Taha ∩ {0<b})^c)=0.  The cusp tip Dirac has b=0 -> INADMISSIBLE there.
So the upper bound = inf <= 1/lam^3 must be realized by measures with b>0.

A genuinely Tgen-INVARIANT probability measure on a finite point set = a PERIODIC orbit
(uniform measure on the cycle).  We search for periodic Tgen-orbits in D with all b>0
whose ess-sup Pgen (= max Pgen over the cycle) approaches 1/lam^3.

Candidate construction: NEAR-CUSP periodic orbits.  The cusp tip (1/lam,0) is a parabolic
FIXED point. Just off it (b>0 small) the genuine cusp-branch orbit shadows the parabolic
line. We look for short cycles hugging the cusp and measure max Pgen / (1/lam^3).

mpmath dps=60.
"""
import mpmath as mp
mp.mp.dps = 60

def lam(q): return 2*mp.cos(mp.pi/q)
def Pgen(l,a,b): return a*(a+l*b)/l
def in_Taha(l,a,b): return (0 < a <= 1) and (1 - l*a < b <= 1)
def in_D(l,a,b): return in_Taha(l,a,b) and (b > 0)

def Tmap(l,a,b):
    # genuine scalar-branch step (the closed form on the cusp/last branch)
    if b<=0: return None
    k = int(mp.floor((1+a)/(l*b)))
    return (b, -a + k*l*b)

def part_A_cusp_periodic():
    """
    The cusp parabolic point (1/lam,0): just inside (b=eps>0) the orbit drifts ALONG the
    parabolic line then ejects. It is NOT periodic for generic eps (parabolic => drift).
    Instead we use the structural fact: a measure SEQUENCE need not be periodic-orbit
    measures; normalized orbit-segment empirical measures along an orbit that shadows the
    cusp for n steps give ess-sup -> sup of Pgen over the shadowed segment.

    KEY: the cusp Dirac is a WEAK-* LIMIT of measures with b>0?  A parabolic fixed point
    on the boundary of D: can it be approximated by invariant measures INSIDE D?
    For a PARABOLIC point the answer is the crux. We test empirically.
    """
    print("="*78)
    print("PART A: near-cusp orbit segments, ess-sup Pgen of the SHADOWED segment.")
    print("  An empirical orbit-segment measure mu_n (uniform on n shadow points, all b>0)")
    print("  has ess-sup Pgen = max Pgen over the segment. Does inf over such segments -> 1/lam^3?")
    print("="*78)
    for q in [5,7,13]:
        l = lam(q); inv = 1/l**3
        print(f"  q={q}  lam={mp.nstr(l,12)}  1/lam^3={mp.nstr(inv,12)}")
        print(f"    {'b0 (cusp gap)':>14} {'shadow len(b>0)':>16} {'max Pgen seg':>16} {'ratio':>12}")
        for b0 in [mp.mpf('1e-2'),mp.mpf('1e-3'),mp.mpf('1e-4'),mp.mpf('1e-6'),
                   mp.mpf('1e-8'),mp.mpf('1e-10'),mp.mpf('1e-12')]:
            a,b = 1/l + b0, b0   # just inside Taha (a>1/lam ensures 1-lam a<0<b)
            # follow orbit; collect the contiguous near-cusp shadow (Pgen close to inv)
            seg_max = mp.mpf('-inf'); n=0
            ca,cb=a,b
            while n < 200000:
                if not in_D(l,ca,cb): break
                p = Pgen(l,ca,cb)
                # the shadow = while we are still near the cusp (Pgen < 2*inv, i.e. before ejection)
                if p > 2*inv:
                    break
                if p>seg_max: seg_max=p
                nxt = Tmap(l,ca,cb)
                if nxt is None: break
                ca,cb = nxt; n+=1
            if n>0 and mp.isfinite(seg_max):
                print(f"    {mp.nstr(b0,4):>14} {n:>16} {mp.nstr(seg_max,12):>16} {mp.nstr(seg_max/inv,10):>12}")
            else:
                print(f"    {mp.nstr(b0,4):>14} {n:>16} {'(ejected immediately)':>16} {'--':>12}")
        print()

def part_B_parabolic_dwell():
    """
    Direct dwell test: start a (with b0>0) -> how long can the orbit keep Pgen <= (1+delta)/lam^3
    while staying in D with b>0?  If for every delta>0 the dwell length -> infinity as b0->0,
    then normalized empirical measures on those dwells give ess-sup Pgen -> 1/lam^3 with b>0,
    PROVING inf <= 1/lam^3 in the OPEN section -> EQUALITY.
    """
    print("="*78)
    print("PART B: parabolic dwell.  longest run with Pgen <= (1+delta)/lam^3, all b>0.")
    print("  If dwell -> infinity as b0 -> 0 for each delta, then ess-sup over the empirical")
    print("  dwell measure -> 1/lam^3 from inside {b>0}  ==> inf <= 1/lam^3  ==> EQUALITY.")
    print("="*78)
    for q in [5,7,13]:
        l=lam(q); inv=1/l**3
        print(f"  q={q}  1/lam^3={mp.nstr(inv,10)}")
        for delta in [mp.mpf('0.1'),mp.mpf('0.01'),mp.mpf('0.001')]:
            thr = (1+delta)*inv
            print(f"    delta={mp.nstr(delta,3)}  threshold=(1+d)/lam^3={mp.nstr(thr,10)}")
            print(f"      {'b0':>10} {'dwell len (b>0, Pgen<=thr)':>28} {'min b on dwell':>16}")
            for b0 in [mp.mpf('1e-3'),mp.mpf('1e-5'),mp.mpf('1e-8'),mp.mpf('1e-12'),mp.mpf('1e-16')]:
                a,b=1/l+b0,b0
                ca,cb=a,b; n=0; minb=cb
                while n<500000:
                    if not in_D(l,ca,cb): break
                    if Pgen(l,ca,cb)>thr: break
                    if cb<minb: minb=cb
                    nxt=Tmap(l,ca,cb)
                    if nxt is None: break
                    ca,cb=nxt; n+=1
                print(f"      {mp.nstr(b0,2):>10} {n:>28} {mp.nstr(minb,6):>16}")
        print()

if __name__=="__main__":
    part_A_cusp_periodic()
    part_B_parabolic_dwell()

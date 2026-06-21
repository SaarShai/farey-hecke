"""
FINAL uniform-inequality validation (dps=50), q=22..60 (and beyond).

Two inequalities underpinning the energy-route uniform hCorr:

(I)  COVERING (q-independent measure wrapper, PROVED in Lean as covering_pos_measure):
     a rotation by alpha=2pi/q of a super-arc of width 2w covers the circle iff 2w>=alpha,
     i.e. super-arc HALF-width fraction (of the period pi in the 2phi var) >= 1/q.
     Block super-arc half-fraction ~ (1-C)/2, C=2arccos(2sqrt6/5)/pi. Check >= 1/q.

(II) L1b super-arc NONEMPTINESS (the SEALED hard input hSuperArc): window of L_blk(q)=
     ceil(33q/256)+2 blocks (half-span fraction (L_blk-1)/q) exceeds the sub-arc
     half-fraction C/2, so window-max reaches threshold. Check (L_blk-1)/q > C/2.

PASS on both for all q in range = the uniform argument's numeric backing.
"""
import mpmath as mp
mp.mp.dps = 50
C = 2*mp.acos(2*mp.sqrt(6)/5)/mp.pi
print(f"C = 2 arccos(2 sqrt6/5)/pi = {mp.nstr(C,15)}")
print(f"super-arc half-fraction (1-C)/2 = {mp.nstr((1-C)/2,12)}")
print(f"sub-arc   half-fraction  C/2     = {mp.nstr(C/2,12)}")
print()
all_ok=True
worst_I=mp.inf; worst_II=mp.inf
for q in range(22,61):
    Lblk = int(mp.ceil(mp.mpf(33)*q/256))+2
    # (I) covering: (1-C)/2 >= 1/q
    margI = (1-C)/2 - mp.mpf(1)/q
    # (II) L1b: (Lblk-1)/q > C/2
    margII = (mp.mpf(Lblk-1)/q) - C/2
    okI = margI>0; okII = margII>0
    all_ok = all_ok and okI and okII
    worst_I=min(worst_I,margI); worst_II=min(worst_II,margII)
    if q in (22,23,30,47,60):
        print(f"q={q:3d} L_blk={Lblk:3d}  (I)cover margin={mp.nstr(margI,6)} ok={okI}   (II)L1b margin={mp.nstr(margII,6)} ok={okII}")
print()
print(f"q=22..60: ALL PASS = {all_ok}")
print(f"worst covering margin (I)  = {mp.nstr(worst_I,8)}  (>0 required)")
print(f"worst L1b margin     (II) = {mp.nstr(worst_II,8)}  (>0 required)")

# Extend to large q to show asymptotic safety of (I); (II)=L1b is sealed for q<=3000.
print("\nasymptotic (I) covering margin (always huge, ->0.436):")
for q in [100,1000,10**6]:
    print(f"  q={q}: (1-C)/2 - 1/q = {mp.nstr((1-C)/2-mp.mpf(1)/q,8)}")

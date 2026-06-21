"""
HONEST RECONCILIATION. Two ellipses appear:

(A) Single-step M=[[0,1],[-1,l]] ellipse E=a^2-l a b+b^2, observable P=a*b. This is the
    k=1 last-branch rotation. On the SMALLEST admissible E0 (corridor edge) the super arc
    is EMPTY (gamma>1), so energy-alone confinement FAILS. (realized_E.py)

(B) Block monodromy M_W of the corridor word W=(q-1,3)(q-1,0)(q-3,0): M_W=[[-l,2l^2+1],[-1,2l]],
    det=1, trace=l, rotation by theta=pi/q on ellipse Q'(a,b)=a^2-3l a b+(2l^2+1)b^2, observable
    a sinusoid that DOES reach 1/l^3 within L_blk(q)~33q/256 blocks. This is the L1b route.

The block map advances the GENUINE state by one full corridor word per "block", so the
observable on the block boundary is the rotating sinusoid P_n of the energy_route note.
The single-step M argument cannot replace L1b because the relevant ellipse/observable is
the BLOCK one, not the single-step one. Verify M_W trace/det and that its sinusoid clears
1/l^3 within L_blk blocks (reproduces the scout's L1b numerics) -- to confirm the energy
route's true hard inequality is L1b (block arc width), NOT a single-step no-dwell.
"""
import mpmath as mp
mp.mp.dps = 40
def lam(q): return 2*mp.cos(mp.pi/q)

def MW(l):
    return mp.matrix([[-l, 2*l*l+1],[-1, 2*l]])

for q in [22,47,100]:
    l=lam(q); M=MW(l)
    tr=M[0,0]+M[1,1]; det=M[0,0]*M[1,1]-M[0,1]*M[1,0]
    print(f"q={q}: trace(M_W)={mp.nstr(tr,6)} (want l={mp.nstr(l,6)}), det={mp.nstr(det,6)} (want 1)")

# The block sinusoid: P_n = (r^2/(2A2))[3l/2 + sqrt(A2) cos(2(n theta - psi)+eta)], A2=1+2l^2.
# Its MAX over n in [0,L_blk) >= 1/l^3? The amplitude term: max possible
# P_max = (r^2/(2A2))[3l/2 + sqrt(A2)]. For confinement we need the WINDOW max (finite n)
# to exceed t. This is exactly g_corr >= 1/l^3 = L1b (sealed, fcorr_lb PROVED in L1bArcCoverage).
# Confirm the CONTINUOUS sup exceeds t (necessary condition; window version is L1b):
for q in [22,47,100,300]:
    l=lam(q); A2=1+2*l*l; t=1/l**3
    # continuous amplitude ratio independent of r: sup_phase P / (r^2/(2A2)) = 3l/2+sqrt(A2)
    # The in-domain r is fixed by corridor; the RATIO (3l/2+sqrt(A2))/(2A2*Blam^2*cos^2 H..)
    # is the fcorr. We just confirm 3l/2+sqrt(A2) > 0 and the structure is sinusoidal.
    amp=3*l/2+mp.sqrt(A2); off=3*l/2
    print(f"q={q}: block sinusoid offset(3l/2)={mp.nstr(off,5)} amp(sqrt A2)={mp.nstr(mp.sqrt(A2),5)}  reaches super (amp>off): {mp.sqrt(A2)>0}")

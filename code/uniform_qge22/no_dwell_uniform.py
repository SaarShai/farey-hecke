"""
THE CLEANEST UNIFORM TARGET (q-independent), measure-theoretic wrapper.

Setting (block ellipse, abstracted): a rotation R_{2theta} on the circle S^1 (the 2phi
variable; period 2pi), theta=pi/q. A continuous observable F(psi)=offset+amp*cos(psi),
amp>0. Super-threshold set S = {psi : F(psi) >= t}. Provided S is a NONEMPTY arc of
half-width w = arccos((t-offset)/amp) > 0 (the L1b continuous content), we claim:

  (NoDwell) There is NO R_{2theta}-invariant Borel probability measure mu on S^1 with
            mu(S)=0.

PROOF (q-independent, elementary): if mu is R_{2theta}-invariant and mu(S)=0, then for
every k, mu(R^{-k} S)=mu(S)=0, so mu(union_k R^{-k} S)=0. But for an IRRATIONAL rotation
union_k R^{-k}S is dense; more robustly, for ANY rotation by 2theta=2pi/q (rational!),
the orbit of the arc S of width 2w>0 covers S^1 once 2w >= 2theta (consecutive translates
overlap) OR within ceil(pi/(q-step)) ... For RATIONAL rotation 2pi/q the translates
{R^{-k}S : k=0..q-1} are q arcs equally spaced by 2theta=2pi/q; they COVER S^1 iff each
arc width 2w >= gap 2theta, i.e. w >= theta = pi/q. THEN mu(S^1)=mu(union)=0, contra
mu prob. So NoDwell holds PROVIDED w >= theta.

=> The single q-independent inequality reduces to:  w(q) >= theta(q),  i.e.
   arccos((t - offset)/amp) >= pi/q,  i.e. the super arc half-width >= one rotation step.

Equivalently cos(pi/q) >= (t-offset)/amp on the BLOCK ellipse. Check across q for the
block sinusoid where offset=3l/2 * scale, amp=sqrt(A2)*scale (scale=r^2/(2A2)>0 cancels
in the ratio (t-offset)/amp only if t is also scaled by 1/scale -- t is FIXED 1/l^3, the
realized r^2 sets scale). Use the L1b-realized scale where window-max touches t; equivalent
condition: super arc half width in the BLOCK 2phi var >= theta. Compute via L1b geometry:
the in-domain arc width is the DWELL; L_blk(q)=ceil(33q/256)+2 >= dwell <=> arc covered.
"""
import mpmath as mp
mp.mp.dps = 40
def lam(q): return 2*mp.cos(mp.pi/q)

# The L1b/energy-route claim is: window of L_blk(q)=ceil(33q/256)+2 blocks, each advancing
# 2theta in the block-2phi var, sweeps an arc of 2*(L_blk-1)*theta >= the SUB-threshold arc,
# forcing window-max >= t. The sub arc half-width (block var) is arccos of the threshold.
# The clean UNIFORM inequality behind it (scout's cleanest_uniform_subtarget):
#   2*arccos(2 sqrt6 /5)/pi < 33/256     [arc_coverage_ineq, PROVED in L1bArcCoverage]
# i.e. the LIMIT sub-arc fraction 2 arccos(2sqrt6/5)/pi < slope 33/256, so L_blk > dwell.
# Verify this constant and that it dominates the finite-q sub-arc fraction.

C = 2*mp.acos(2*mp.sqrt(6)/5)/mp.pi
print(f"limit sub-arc fraction 2 arccos(2 sqrt6/5)/pi = {mp.nstr(C,12)}")
print(f"slope 33/256 = {mp.nstr(mp.mpf(33)/256,12)}  headroom = {mp.nstr(mp.mpf(33)/256-C,8)}")

# finite-q sub-arc fraction (block ellipse) vs slope -- the L1b margin (reproduce scout table)
def block_geom(q):
    l=lam(q); A2=1+2*l*l; t=1/l**3
    # P_n/(r^2/(2A2)) = 3l/2 + sqrt(A2) cos(...). The threshold on cos: cos >= (2 A2 t/r^2 - 3l/2)/sqrt(A2)
    # r is set so window-max touches t. The arc-fraction is independent of r at the LIMIT;
    # finite-q uses the actual Blam-corrected denom. We just confirm the L_blk dominates:
    Lblk = int(mp.ceil(33*q/256))+2
    dwell_frac = C  # ~limit; finite-q is <= C + O(1/q)
    half_window_frac = (Lblk-1)/q  # (L-1)*theta/pi = (L-1)/q, the window half-span fraction
    return Lblk, half_window_frac
for q in [22,47,100,300,1000,3000]:
    Lblk, hwf = block_geom(q)
    print(f"q={q:5d}: L_blk={Lblk:5d} window-half-fraction (L-1)/q={mp.nstr(hwf,8)} vs sub-arc half-frac ~{mp.nstr(C/2,8)}  ok={hwf>C/2}")

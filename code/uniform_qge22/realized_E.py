"""
The dwell (consecutive sub-threshold M-steps) grows like q ONLY on ellipses with E0 -> 0.
But the genuine BCZ cluster has a FLOOR on E0: the cluster lives in the corridor
   0 < a, 0 < b, b <= 1 (last branch),  corridor edge l*a + b > 1 (in-domain),
and the BCZ recurrence. The conserved E0 = a^2 - l a b + b^2 at the realized cluster.

Question: across q=22..200, what is the MINIMUM E0 over the realized sub-threshold
last-branch clusters, and does the resulting dwell stay bounded?

We reconstruct the cluster the way the memory/scout describes: the maximal run of
consecutive last-branch sub-threshold points with k-pattern [1,...,1,2]. We do a direct
BCZ-corridor simulation to find realized clusters and read off E0 and length.

Simpler faithful proxy: the cluster's E0 is determined by the ENTRY point (the first
sub-threshold last-branch point after a floor>=2 / corridor switch). Empirically (memory)
B(q) ~ 0.216 q and the cluster IS a single M-rotation arc, so the realized E0 must be
the one giving dwell ~ 0.216 q, i.e. gamma ~ cos(2*0.216*pi*?) ... let's just measure.

We instead bound the realized E0 from BELOW using the corridor geometry directly:
on the last branch the genuine entry point has a in [a_min, a_max], b in (0,1]. The
cusp-tip (1/l, 0) is the high-P boundary; the realized cluster's points all satisfy
P = a*b < 1/l^3 AND corridor edge l a + b > 1. The minimal E0 over the corridor-edge
boundary l a + b = 1 with P<=1/l^3:
   minimize E0 = a^2 - l a b + b^2  s.t. l a + b = 1, 0<b<=1.
"""
import mpmath as mp
mp.mp.dps = 40

def lam(q): return 2*mp.cos(mp.pi/q)

def minE_on_edge(q):
    """min of E=a^2-l a b+b^2 on the corridor edge l a + b = 1, b in (0,1)."""
    l=lam(q)
    # a = (1-b)/l. E(b) = ((1-b)/l)^2 - l*((1-b)/l)*b + b^2
    def E(b):
        a=(1-b)/l
        return a*a - l*a*b + b*b
    # minimize over b in (0,1)
    best=mp.inf; bb=None
    N=20000
    for i in range(1,N):
        b=mp.mpf(i)/N
        e=E(b)
        if e<best: best=e; bb=b
    return best, bb

# But the edge l a + b = 1 is the IN-DOMAIN boundary (l a + b > 1 required), so the
# realized cluster has E0 > minE_on_edge strictly. The dwell is monotone DECREASING in E0
# (larger E0 -> larger super arc -> smaller dwell), so the WORST dwell is at the smallest
# admissible E0 ~ minE_on_edge. Compute the dwell there.
def gamma(q,E0):
    l=lam(q); t=1/l**3
    return 2*(1-l*l/4)*t/E0 - l/2

for q in [22,30,47,61,100,200]:
    l=lam(q); theta=mp.pi/q
    Emin,bb = minE_on_edge(q)
    g = gamma(q,Emin)
    if g>=1:
        print(f"q={q:3d} Emin_edge={mp.nstr(Emin,5)} gamma={mp.nstr(g,6)} -> super arc EMPTY at edge (dwell unbounded)")
    elif g<=-1:
        print(f"q={q:3d} Emin_edge={mp.nstr(Emin,5)} gamma={mp.nstr(g,6)} -> ALL super")
    else:
        hw=mp.acos(g); dwell=(mp.pi-hw)/theta
        print(f"q={q:3d} Emin_edge={mp.nstr(Emin,5)} gamma={mp.nstr(g,6)} superHW={mp.nstr(hw,5)} dwell={mp.nstr(dwell,5)}")

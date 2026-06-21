"""
On the conserved ellipse, with whitened angle phi advancing by theta = pi/q per M-step,
the genuine observable is

   P(phi) = (E0/2)/(1 - l^2/4) * [ l/2 + cos(2 phi) ],   l = 2 cos(pi/q).

The orbit is sub-threshold (P < t = 1/l^3) iff cos(2 phi) < c*(E0), where

   c*(E0) = t * (1 - l^2/4) / (E0/2) * ... -> threshold on cos(2phi):
   l/2 + cos(2phi) < t * 2 * (1-l^2/4) / E0
   cos(2phi) < (2(1-l^2/4) t)/E0 - l/2 =: gamma(E0).

The cluster lives on the GOVERNING sub-threshold ellipse. The relevant E0 is the one
realized by the genuine sub-threshold last-branch cluster. The R1 file uses the bound
E0 <= (2-l)/l^3 (the governing/sub-threshold ellipse cap). At the cluster the cusp-tip
value P=1/l^3 sits at the ellipse a^2-l a b+b^2 with the tip (1/l,0): E_tip = 1/l^2.

We want: the SUPER-threshold set {cos(2phi) >= gamma} is a NONEMPTY arc whose angular
width (in the phi variable, period pi) is bounded BELOW uniformly in q by a positive
multiple of theta=pi/q. Equivalently arccos(gamma) > 0 with a uniform lower bound,
AND gamma < 1 (super arc nonempty) AND gamma > -1 (sub arc nonempty, so confinement
is non-trivial).

The per-step phase advance is theta = pi/q. In the 2phi variable the advance is 2theta
= 2pi/q and the period is 2pi. The super arc in 2phi has half-width arccos(gamma).
Number of consecutive sub-threshold steps (dwell) ~ (2pi - 2 arccos(gamma))/(2 theta)
= (pi - arccos(gamma))/theta.  The MEASURE-THEORETIC no-dwell needs only:
  super arc width 2*arccos(gamma) > 0 uniformly, i.e. gamma < 1 with margin.
"""
import mpmath as mp
mp.mp.dps = 50

def lam(q): return 2*mp.cos(mp.pi/q)

def gamma(q, E0):
    l = lam(q)
    t = 1/l**3
    return 2*(1-l*l/4)*t/E0 - l/2

# E0 candidates: the actual cluster ellipse. Use E_tip = 1/l^2 (the cusp-tip energy,
# where P=1/l^3 is exactly attained) -- this is the boundary case. And the governing
# cap E_cap = (2-l)/l^3.
def report(q):
    l=lam(q); t=1/l**3
    E_tip = 1/l**2
    E_cap = (2-l)/l**3
    g_tip = gamma(q,E_tip)
    g_cap = gamma(q,E_cap)
    theta = mp.pi/q
    # super arc half width in 2phi at E_tip
    def info(g):
        if g>=1: return None  # super arc empty
        if g<=-1: return ("ALL-SUPER", None)
        hw = mp.acos(g)  # half-width of super arc in the 2phi variable
        dwell = (mp.pi - hw)/theta  # consecutive sub-threshold M-steps (phi advances theta)
        return (hw, dwell)
    it=info(g_tip); ic=info(g_cap)
    print(f"q={q:3d} l={mp.nstr(l,8)} theta={mp.nstr(theta,6)}")
    print(f"     E_tip={mp.nstr(E_tip,6)} gamma_tip={mp.nstr(g_tip,6)} -> {('superHW(2phi)='+mp.nstr(it[0],6)+' dwell='+mp.nstr(it[1],6)) if it and it[0]!=None else it}")
    print(f"     E_cap={mp.nstr(E_cap,6)} gamma_cap={mp.nstr(g_cap,6)} -> {('superHW(2phi)='+mp.nstr(ic[0],6)+' dwell='+mp.nstr(ic[1],6)) if ic and ic[0]!=None else ic}")
    return g_tip, g_cap

for q in [22,23,30,40,47,60,100,300,1000]:
    report(q)

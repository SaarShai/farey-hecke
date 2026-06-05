"""
D3 Q1 (decisive probe): FF BCZ / Bruhat-Tits-tree Farey COCYCLE Birkhoff variance.

Question: is the FF Farey-discrepancy cocycle Birkhoff variance a DIFFERENT
statistic from the Keating-Rudnick single-degree twisted-Mobius variance?

Construction (exact, Fraction arithmetic):
 - Farey set F_D over A=F_q[t]: h/g, g monic deg<=D, deg h<deg g, gcd=1, plus 0.
 - K_inf order: alpha = sum_{j>=1} c_j t^{-j}  ->  exact key (c_1,c_2,...) in F_q,
   computed by the long-division recurrence (g monic):
       R <- h ; repeat:  c_j = R_{n-1}; R <- R*t - c_j*g  (then deg R < n).
   Real coordinate x = sum c_j / q^j  (exact Fraction, finite digits).
 - Sort F_D by lexicographic c-sequence (exact). Phi = |F_D|.
 - Discrepancy at node j (j-th smallest): E_j = j - Phi * x_j.
 - Cocycle g_j = 1 - Phi*(x_j - x_{j-1}); Birkhoff S_j = sum_{i<=j} g_i.
   Structural check: S_j == E_j exactly (telescoping, x_0=0)  [FF analogue of D1 V4].
 - Second moment W_D = (1/Phi) * exact integral of E_D(x)^2 (piecewise linear).
 - Cocycle autocovariance c_l (centered) along the orbit; running Green-Kubo
   sigma^2(L) = c_0 + 2 sum_{l<=L} c_l ; decay exponent of c_l.

CHAR-0 BASELINE (from D1): raw cocycle NOT uniformly L^2, c_l ~ 1/l (alpha~1/2),
sigma^2 drifts, NO CLT -> theorem (R) died.
FF DISCRIMINATOR: Deligne gives a spectral gap; if the FF cocycle correlations
are SUMMABLE (alpha effectively >=1, sigma^2 stabilizes, c_0 Q-stable) that is a
QUALITATIVELY DIFFERENT statistic from char-0 AND its variance law can be
compared to the twisted-Mobius q^n / U(N) law to decide KR-transcription vs new.
"""

from itertools import product
from functools import lru_cache
from fractions import Fraction

# ---------- F_q[t] arithmetic ----------
def normalize(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0: p.pop()
    return tuple(p)
def deg(p):
    p = normalize(p)
    return -1 if (len(p)==1 and p[0]==0) else len(p)-1
def is_zero(p): return deg(p)==-1
def pmul(a,b,q):
    if is_zero(a) or is_zero(b): return (0,)
    r=[0]*(len(a)+len(b)-1)
    for i,ai in enumerate(a):
        if ai:
            for j,bj in enumerate(b): r[i+j]=(r[i+j]+ai*bj)%q
    return normalize(tuple(r))
def pdivmod(a,b,q):
    a=list(normalize(a)); b=normalize(b); db=deg(b)
    inv=pow(b[-1],q-2,q); quot=[0]
    while deg(tuple(a))>=db and not is_zero(tuple(a)):
        da=deg(tuple(a)); sh=da-db; f=(a[da]*inv)%q
        if sh>=len(quot): quot+=[0]*(sh+1-len(quot))
        quot[sh]=f
        for i,bi in enumerate(b): a[i+sh]=(a[i+sh]-f*bi)%q
        a=list(normalize(tuple(a)))
        if is_zero(tuple(a)) and sh==0: break
    return normalize(tuple(quot)), normalize(tuple(a))
def pmod(a,b,q): return pdivmod(a,b,q)[1]
def pgcd(a,b,q):
    a,b=normalize(a),normalize(b)
    while not is_zero(b): a,b=b,pmod(a,b,q)
    return normalize(a)
def monic_polys(d,q):
    if d==0: yield (1,); return
    for lo in product(range(q),repeat=d): yield tuple(lo)+(1,)
def polys_deg_lt(d,q):
    if d<=0: yield (0,); return
    for c in product(range(q),repeat=d): yield normalize(c)

# ---------- K_inf coefficient sequence of h/g ----------
def coeff_seq(h, g, q, L):
    """c_1..c_L of (h/g) in t^{-1}, g monic deg n, deg h < n. Exact."""
    g = normalize(g); n = deg(g)
    R = list(normalize(h)) + [0]*(n+2)
    cs = []
    for _ in range(L):
        c = R[n-1] % q if n-1>=0 else 0
        cs.append(c)
        # R <- R*t - c*g   (shift up by one), keep length, then it has deg<n
        Rt = [0]+R
        for i in range(len(g)):
            Rt[i] = (Rt[i] - c*g[i]) % q
        # now deg Rt <= n ; top coeff (index n) should be 0 by choice of c
        R = (Rt[:n] + [0]*(n+2))[:n+2]
    return tuple(cs)

def x_real(cs, q):
    x = Fraction(0); base = Fraction(1)
    for c in cs:
        base /= q
        x += c*base
    return x

# ---------- Farey set, order, cocycle ----------
def build_farey(D, q, L):
    pts = [((0,)*1, Fraction(0), (1,), (0,))]  # 0 = 0/1
    # represent each as (key_tuple, x, g, h)
    items = [( (0,)*L, Fraction(0) )]
    for e in range(1, D+1):
        for g in monic_polys(e, q):
            for h in polys_deg_lt(e, q):
                if is_zero(h): continue
                if deg(pgcd(h,g,q))==0:
                    cs = coeff_seq(h,g,q,L)
                    items.append((cs, x_real(cs,q)))
    # dedup by key, sort lexicographically by coeff sequence (exact)
    items = sorted(set(items), key=lambda z: z[0])
    xs = [z[1] for z in items]
    return xs

def analyse(D, q):
    L = 3*D + 8
    xs = build_farey(D, q, L)
    Phi = len(xs)
    # node discrepancy E_j = j - Phi*x_j  (j=1..Phi-1 interior; x sorted, x_0=0)
    # cocycle g_j = 1 - Phi*(x_j - x_{j-1});  S_j = sum_{i<=j} g_i  should == E_j
    S = Fraction(0); Eok = True
    gs = []
    for j in range(1, Phi):
        gap = xs[j]-xs[j-1]
        gj = 1 - Phi*gap
        gs.append(gj)
        S += gj
        Ej = j - Phi*xs[j]
        if S != Ej: Eok = False
    # second moment W_D = (1/Phi) * sum_j integral_{x_{j-1}}^{x_j} E(x)^2 dx
    # E linear between nodes: at x_{j-1} value = E_{j-1}=S_{j-1}; slope -Phi
    # integral of (a - Phi*(x-x0))^2 over [x0,x0+gap] = gap*(a^2 - a*Phi*gap + (Phi*gap)^2/3)
    W = Fraction(0); a = Fraction(0)
    for j in range(1, Phi):
        gap = xs[j]-xs[j-1]
        term = gap*(a*a - a*Phi*gap + Fraction((Phi*gap)**2,1)/3)
        W += term
        a = a - Phi*gap + 1  # E at next node = a - Phi*gap + 1  (E_j = E_{j-1} + g_j)
    W = W/Phi
    # cocycle autocovariance (centered) and Green-Kubo
    gf = [float(g) for g in gs]
    n = len(gf)
    mean = sum(gf)/n
    cg = [v-mean for v in gf]
    c0 = sum(v*v for v in cg)/n
    def cov(l):
        return sum(cg[i]*cg[i+l] for i in range(n-l))/(n-l) if n-l>0 else 0.0
    cl = {l: cov(l) for l in (1,2,4,8,16)}
    # Green-Kubo running sum
    sig = {}
    acc = c0
    Lmax = min(64, n-1)
    for l in range(1, Lmax+1):
        acc += 2*cov(l)
        if l in (4,8,16,32,64): sig[l]=acc
    # crude decay exponent alpha from c_l ~ l^{-alpha} using l=2,16
    import math
    a2, a16 = abs(cov(2)), abs(cov(16))
    alpha = (math.log(a2)-math.log(a16))/(math.log(16)-math.log(2)) if a2>0 and a16>0 else float('nan')
    return dict(D=D,q=q,Phi=Phi,Eok=Eok,W=float(W),NW=float(W)*(q**D),
                c0=c0,cl=cl,sig=sig,alpha=alpha)

def run():
    print("="*86)
    print("Q1 PROBE: FF Farey-discrepancy COCYCLE Birkhoff variance & correlation decay")
    print("Char-0 baseline (D1): c0 grows w/ Q, c_l~1/l (alpha~0.5), sigma^2 drifts, NO CLT.")
    print("FF discriminator: Deligne spectral gap => expect summable corr (alpha>=1),")
    print("c0 D-stable, sigma^2 converges  =>  QUALITATIVELY different statistic.")
    print("="*86)
    plans = [(2,[2,3,4,5]),(3,[2,3,4]),(5,[2,3])]
    for q,Ds in plans:
        print(f"\n--- q={q} ---")
        print(f"{'D':>2} {'Phi':>7} {'S==E':>5} {'W_D':>10} {'(q^D)W_D':>10} "
              f"{'c0':>8} {'c_l: l=1,2,4,8,16':>34} {'alpha':>6} {'GK sig(8/16/32)':>22}")
        prev_c0=None
        for D in Ds:
            r=analyse(D,q)
            cls=" ".join(f"{r['cl'][l]:+.3f}" for l in (1,2,4,8,16))
            sg=r['sig']
            sigs=f"{sg.get(8,float('nan')):+.3f}/{sg.get(16,float('nan')):+.3f}/{sg.get(32,float('nan')):+.3f}"
            print(f"{D:>2} {r['Phi']:>7} {str(r['Eok']):>5} {r['W']:>10.5f} "
                  f"{r['NW']:>10.4f} {r['c0']:>8.4f}  {cls:>32}  {r['alpha']:>6.3f}  {sigs:>22}")
            prev_c0=r['c0']
    print("\n"+"="*86)
    print("READING / DECISION:")
    print(" - S==E True everywhere  => FF discrepancy IS the Birkhoff sum of the cocycle (structural, [PROVEN]-exact).")
    print(" - If c0 D-STABLE & alpha>=~1 & GK sigma^2 CONVERGES: FF cocycle is uniformly")
    print("   L2 with SUMMABLE correlations -> a CLT/variance theorem is reachable here")
    print("   (UNLIKE char-0 where theorem (R) died). Then compare (q^D)W_D growth law")
    print("   vs twisted-Mobius q^n: same exponent => same statistic (KR); different")
    print("   exponent/structure => candidate NEW statistic (proceed Q3).")
    print(" - If c0 grows with D & alpha~0.5: FF reproduces the char-0 obstruction =>")
    print("   no new theorem; D3 stays dictionary-tier (proceed Q4 only).")
    print("="*86)

if __name__=="__main__":
    run()

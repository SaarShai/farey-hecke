"""
D3 function-field model -- GATE 2(a): non-triviality of the twisted (family) object.

G1 proved the GLOBAL Farey-Mertens object trivializes exactly: untwisted
M_A(n) = 1-q (constant, no fluctuation, RH-depth gone).

G2 live object: twist by a Dirichlet character chi mod Q (Q monic irreducible,
deg Q = d). Twisted Mertens:
    M_A(n, chi) = sum_{f monic, deg f <= n} mu(f) chi(f mod Q).
Generating fn: sum_f mu(f)chi(f) u^{deg f} = 1/L(u,chi), L(u,chi)=sum_{f monic} chi(f) u^{deg f}
is a polynomial in u of degree (deg Q - 1) whose inverse roots are Frobenius
eigenvalues with |alpha_i| = sqrt(q)  (Deligne / Weil II -- UNCONDITIONAL).
=> |M_A(n,chi)| ~ q^{n/2} (square-root cancellation), and the normalized
character-variance  V(n) = mean_chi |M_A(n,chi)|^2 / q^n  stabilizes to an
O(1) constant (the Katz-Sarnak matrix-integral signature).

Farey-specific object (G0 identity carried through the twist):
    S_D(m, chi) = sum_{e | m monic} q^{deg e} * M_A(D - deg e, chi).
We also report Var_chi S_D as the genuine *Farey-discrepancy* family statistic.

PASS(G2a) = twisted object is NON-trivial: |M_A(n,chi)| grows ~ q^{n/2}
(not constant), normalized variance V(n) stabilizes (Deligne sqrt-cancellation
visible, UNCONDITIONALLY). Contrast vs G1 constant printed side by side.
"""

from itertools import product
from functools import lru_cache
import cmath

# ---------- F_q[t] arithmetic (same as G0 script) ----------

def normalize(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return tuple(p)

def deg(p):
    p = normalize(p)
    if len(p) == 1 and p[0] == 0:
        return -1
    return len(p) - 1

def is_zero(p):
    return deg(p) == -1

def pmul(a, b, q):
    if is_zero(a) or is_zero(b):
        return (0,)
    r = [0]*(len(a)+len(b)-1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                r[i+j] = (r[i+j] + ai*bj) % q
    return normalize(tuple(r))

def pdivmod(a, b, q):
    a = list(normalize(a)); b = normalize(b)
    db = deg(b)
    inv_lead = pow(b[-1], q-2, q)
    quot = [0]
    while deg(tuple(a)) >= db and not is_zero(tuple(a)):
        da = deg(tuple(a))
        shift = da - db
        factor = (a[da] * inv_lead) % q
        if shift >= len(quot):
            quot += [0]*(shift+1-len(quot))
        quot[shift] = factor
        for i, bi in enumerate(b):
            a[i+shift] = (a[i+shift] - factor*bi) % q
        a = list(normalize(tuple(a)))
        if is_zero(tuple(a)) and shift == 0:
            break
    return normalize(tuple(quot)), normalize(tuple(a))

def pmod(a, b, q):
    return pdivmod(a, b, q)[1]

def pgcd(a, b, q):
    a, b = normalize(a), normalize(b)
    while not is_zero(b):
        a, b = b, pmod(a, b, q)
    return normalize(a)

def monic_polys(d, q):
    if d == 0:
        yield (1,); return
    for lower in product(range(q), repeat=d):
        yield tuple(lower) + (1,)

@lru_cache(maxsize=None)
def irreducibles_upto(maxdeg, q):
    irr = []
    for d in range(1, maxdeg+1):
        for f in monic_polys(d, q):
            ok = True
            for g in irr:
                if deg(g) > d//2:
                    break
                if is_zero(pmod(f, g, q)):
                    ok = False; break
            if ok:
                irr.append(f)
    return tuple(irr)

def factor_monic(f, q):
    f = normalize(f); facs = {}
    d = deg(f)
    irr = irreducibles_upto(max(1, d), q)
    cur = f
    for p in irr:
        if deg(cur) == 0: break
        while deg(cur) >= deg(p):
            qo, ro = pdivmod(cur, p, q)
            if is_zero(ro):
                facs[p] = facs.get(p, 0)+1; cur = qo
            else:
                break
    if deg(cur) >= 1:
        facs[cur] = facs.get(cur, 0)+1
    return facs

def mu(f, q):
    f = normalize(f)
    if deg(f) == 0: return 1
    facs = factor_monic(f, q)
    if any(e >= 2 for e in facs.values()): return 0
    return (-1)**len(facs)

def divisors_monic(m, q):
    m = normalize(m)
    if deg(m) == 0: return [(1,)]
    facs = factor_monic(m, q)
    divs = [(1,)]
    for p, e in facs.items():
        new = []; pe = (1,)
        for k in range(e+1):
            for dd in divs:
                new.append(pmul(dd, pe, q))
            pe = pmul(pe, p, q)
        divs = new
    seen=set(); out=[]
    for dd in divs:
        dd=normalize(dd)
        if dd not in seen: seen.add(dd); out.append(dd)
    return out

# ---------- field F_{q^d} = F_q[t]/(Q), characters ----------

def field_key(x, d):
    x = list(normalize(x))
    return tuple((x + [0]*d)[:d])

def build_field(Q, q):
    d = deg(Q)
    N = q**d - 1
    elems = []
    for coeffs in product(range(q), repeat=d):
        elems.append(normalize(coeffs))
    # find a multiplicative generator
    def mulmod(a, b):
        return pmod(pmul(a, b, q), Q, q)
    gen = None
    for cand in elems:
        if is_zero(cand): continue
        seen = set(); x = (1,); order = 0
        for _ in range(N):
            x = mulmod(x, cand); order += 1
            k = field_key(x, d)
            if k in seen: break
            seen.add(k)
            if k == field_key((1,), d):
                break
        if order == N:
            gen = cand; break
    assert gen is not None, "no generator found"
    # discrete log table
    dlog = {}
    x = (1,)
    for k in range(N):
        dlog[field_key(x, d)] = k
        x = mulmod(x, gen)
    return d, N, dlog

def chi_value(f, Q, q, d, dlog, N, j):
    """chi_j(f) : 0 if Q | f, else exp(2 pi i j * dlog(f mod Q)/N)."""
    r = pmod(f, Q, q)
    if is_zero(r):
        return 0.0+0.0j
    k = dlog[field_key(r, d)]
    return cmath.exp(2j*cmath.pi*(j*k % N)/N)

# ---------- twisted Mertens & variances ----------

def twisted_mertens_table(Q, q, nmax):
    d, N, dlog = build_field(Q, q)
    # M[n][j] = sum_{deg f <= n} mu(f) chi_j(f)
    Mvals = [[0j]*N for _ in range(nmax+1)]
    running = [0j]*N
    for n in range(0, nmax+1):
        for f in monic_polys(n, q):
            mf = mu(f, q)
            if mf == 0:
                continue
            for j in range(N):
                running[j] += mf * chi_value(f, Q, q, d, dlog, N, j)
        Mvals[n] = running[:]
    return d, N, Mvals

def run():
    cases = [
        (2, (1,1,0,1)),   # q=2, Q = 1 + t + t^3  (irreducible /F2), d=3, N=7
        (3, (1,0,1)),     # q=3, Q = 1 + t^2      (irreducible /F3), d=2, N=8
        (5, (2,0,1)),     # q=5, Q = 2 + t^2      (irreducible /F5), d=2, N=24
    ]
    for q, Q in cases:
        Q = normalize(Q); d = deg(Q); N = q**d - 1
        nmax = 8 if q == 2 else (7 if q == 3 else 6)
        d, N, Mvals = twisted_mertens_table(Q, q, nmax)
        print("="*78)
        print(f"q={q}  Q={Q} (deg {d}, irreducible)  #chars N={N}  "
              f"L-deg = deg Q - 1 = {d-1}; Deligne |alpha|=sqrt(q)={q**0.5:.4f}")
        print("="*78)
        print(f"{'n':>2} | {'untwisted M_A(n)':>16} | {'mean|M(n,chi)|^2':>16} | "
              f"{'V=mean/q^n':>11} | {'max|M|/q^(n/2)':>15}")
        print("-"*78)
        for n in range(1, nmax+1):
            nonpr = [Mvals[n][j] for j in range(1, N)]  # exclude principal j=0
            mean_sq = sum(abs(z)**2 for z in nonpr)/len(nonpr)
            Vn = mean_sq/(q**n)
            maxnorm = max(abs(z) for z in nonpr)/(q**(n/2))
            untw = 1-q  # G1 exact constant
            print(f"{n:>2} | {untw:>16} | {mean_sq:>16.4f} | {Vn:>11.5f} | {maxnorm:>15.4f}")
        # Farey-specific: Var_chi S_D(m,chi), m chosen, D=nmax
        Dm = nmax
        for m in [(0,1), normalize((1,1,1))]:  # m=t (deg1), m=1+t+t^2 (deg2)
            S = [0j]*N
            for e in divisors_monic(m, q):
                de = deg(e)
                for j in range(N):
                    S[j] += (q**de) * Mvals[Dm-de][j] if Dm-de >= 0 else 0
            nonpr = [S[j] for j in range(1, N)]
            varS = sum(abs(z)**2 for z in nonpr)/len(nonpr)
            print(f"  Farey S_D(m={m},D={Dm}): Var_chi = {varS:.3f}  "
                  f"(/q^D = {varS/q**Dm:.5f})  [non-constant in chi => Farey family non-trivial]")
        print()
    print("="*78)
    print("READING: untwisted column is the G1 exact constant (1-q): NO fluctuation.")
    print("Twisted: mean|M|^2 ~ q^n  <=>  |M_A(n,chi)| ~ q^{n/2}  =  Deligne/Weil-II")
    print("square-root cancellation, UNCONDITIONAL (no RH assumed). V=mean/q^n")
    print("stabilizing to O(1) = Katz-Sarnak matrix-integral signature.")
    print("=> GATE 2(a) PASS iff V(n) bounded/stabilizing AND max|M|/q^(n/2) bounded.")
    print("="*78)

if __name__ == "__main__":
    run()

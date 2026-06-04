"""
D3 function-field model -- Gate 0 (exact Farey-Mertens identity) + Gate 1 (global trivialization).

Setting: A = F_q[t], q prime. Monic polynomials play the role of positive integers,
|f| = q^deg f. Mobius mu over monic polynomials. Mertens M_A(n) = sum_{f monic, deg<=n} mu(f).

Farey set F_D = { h/g : g monic, deg g <= D, deg h < deg g, gcd(h,g)=1 } u {0}.
"Circle" character: psi(alpha) = omega^{ res_inf(alpha) }, omega = exp(2 pi i / q),
res_inf(r/g) for deg r < deg g, g monic = coefficient of t^{deg g - 1} in r
(derived: r = g * sum c_j t^{-j}, g monic => c_1 = r_{deg g - 1}).

A_D(m) := sum_{f in F_D} psi(m f).

CLAIMED EXACT IDENTITY (FF analogue of A_Q(m)=sum_{d|m} d M(floor(Q/d))):
    A_D(m) = sum_{e | m, e monic} q^{deg e} * M_A(D - deg e),     M_A(k<0):=0.

Polynomials represented as tuples of F_q coefficients, low degree first; monic => last entry 1.
"""

from itertools import product
from functools import lru_cache
import cmath

# ---------- F_q[t] arithmetic ----------

def normalize(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return tuple(p)

def deg(p):
    p = normalize(p)
    if len(p) == 1 and p[0] == 0:
        return -1  # zero polynomial
    return len(p) - 1

def is_zero(p):
    return deg(p) == -1

def padd(a, b, q):
    n = max(len(a), len(b))
    a = list(a) + [0]*(n-len(a)); b = list(b) + [0]*(n-len(b))
    return normalize(tuple((a[i]+b[i]) % q for i in range(n)))

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
    inv_lead = pow(b[-1], q-2, q)  # q prime
    quot = [0]*max(1, len(a)-db+0)
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
    """all monic polynomials of degree exactly d (d>=0)."""
    if d == 0:
        yield (1,)
        return
    for lower in product(range(q), repeat=d):
        yield tuple(lower) + (1,)

def all_polys_deg_lt(d, q):
    """all polynomials of degree < d (includes 0); represented length-normalized."""
    if d <= 0:
        yield (0,)
        return
    for coeffs in product(range(q), repeat=d):
        yield normalize(coeffs)

# ---------- mu, M_A ----------

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
                    ok = False
                    break
            if ok:
                irr.append(f)
    return tuple(irr)

def factor_monic(f, q):
    """return dict {irreducible: exponent} for monic f, deg f >= 1."""
    f = normalize(f)
    facs = {}
    d = deg(f)
    irr = irreducibles_upto(max(1, d), q)
    cur = f
    for p in irr:
        if deg(cur) == 0:
            break
        while deg(cur) >= deg(p):
            qo, ro = pdivmod(cur, p, q)
            if is_zero(ro):
                facs[p] = facs.get(p, 0) + 1
                cur = qo
            else:
                break
    if deg(cur) >= 1:  # leftover irreducible (deg > maxdeg/2 case)
        facs[cur] = facs.get(cur, 0) + 1
    return facs

def mu(f, q):
    f = normalize(f)
    if deg(f) == 0:
        return 1  # mu(1)=1
    facs = factor_monic(f, q)
    if any(e >= 2 for e in facs.values()):
        return 0
    return (-1)**len(facs)

@lru_cache(maxsize=None)
def M_A(n, q):
    if n < 0:
        return 0
    s = 0
    for d in range(0, n+1):
        for f in monic_polys(d, q):
            s += mu(f, q)
    return s

def divisors_monic(m, q):
    """all monic divisors e of monic m."""
    m = normalize(m)
    if deg(m) == 0:
        return [(1,)]
    facs = factor_monic(m, q)
    divs = [(1,)]
    for p, e in facs.items():
        new = []
        pe = (1,)
        for k in range(e+1):
            for d in divs:
                new.append(pmul(d, pe, q))
            pe = pmul(pe, p, q)
        divs = new
    # dedup
    seen = set(); out = []
    for d in divs:
        d = normalize(d)
        if d not in seen:
            seen.add(d); out.append(d)
    return out

# ---------- Farey set and character sum ----------

def res_inf(num, g, q):
    """res at infinity of num/g, deg num < deg g, g monic => coeff of t^{deg g -1} in num."""
    n = deg(g)
    num = list(normalize(num)) + [0]*(n)
    return num[n-1] % q if n-1 >= 0 else 0

def A_D_direct(m, D, q):
    """A_D(m) = sum_{f in F_D} psi(m f), computed via exact residue counts."""
    omega = cmath.exp(2j*cmath.pi/q)
    counts = [0]*q
    # f = 0  (g=1, h=0): psi(0)=omega^0
    counts[0] += 1
    for e in range(1, D+1):
        for g in monic_polys(e, q):
            for h in all_polys_deg_lt(e, q):
                if is_zero(h):
                    continue
                if deg(pgcd(h, g, q)) == 0:  # gcd is a nonzero constant => coprime
                    mh = pmul(m, h, q)
                    r = pmod(mh, g, q)
                    c = res_inf(r, g, q)
                    counts[c] += 1
    val = sum(counts[c]*omega**c for c in range(q))
    total = sum(counts)
    return val, total

def A_D_identity(m, D, q):
    """claimed closed form: sum_{e|m monic} q^{deg e} M_A(D - deg e)."""
    s = 0
    for e in divisors_monic(m, q):
        s += (q**deg(e)) * M_A(D - deg(e), q)
    return s

def sigma_A(m, q):
    """sum of |e| over monic divisors e of m  =  sum q^{deg e}."""
    return sum(q**deg(e) for e in divisors_monic(m, q))

# ---------- run gates ----------

def run():
    print("="*72)
    print("GATE 0  -- exact FF Farey-Mertens identity   A_D(m) = sum_{e|m} q^deg e * M_A(D-deg e)")
    print("="*72)
    allok = True
    for q in (2, 3, 5):
        # sanity: M_A(n) should be 1 (n=0), 1-q (n>=1)
        mvals = [M_A(n, q) for n in range(0, 5)]
        pred = [1] + [1-q]*4
        print(f"q={q}: M_A(0..4) = {mvals}  predicted {pred}  {'OK' if mvals==pred else 'FAIL'}")
        if mvals != pred:
            allok = False
        # identity check over many m, D
        Dmax = 4 if q == 2 else (3 if q == 3 else 2)
        tested = 0
        for D in range(1, Dmax+1):
            ms = [(1,)]  # m=1
            for dm in range(1, D+2):  # include deg m < D, = D, > D
                ms += list(monic_polys(dm, q))
            for m in ms:
                if deg(m) > D+1:
                    continue
                direct, total = A_D_direct(m, D, q)
                ident = A_D_identity(m, D, q)
                ok = abs(direct - ident) < 1e-6
                tested += 1
                if not ok:
                    allok = False
                    print(f"  FAIL q={q} D={D} m=deg{deg(m)}{m}: direct={direct:.4f} ident={ident} |F_D|={total}")
        print(f"  -> {tested} (m,D) cases checked, all match: {'YES' if allok else 'NO'}")
    print()
    print("="*72)
    print("GATE 1  -- global trivialization:  D > deg m  =>  A_D(m) = (1-q) * sigma_A(m), D-independent")
    print("="*72)
    triv_ok = True
    for q in (2, 3, 5):
        for m in list(monic_polys(1, q)) + list(monic_polys(2, q))[:3]:
            vals = []
            for D in range(deg(m)+1, deg(m)+4):
                v = A_D_identity(m, D, q)
                vals.append(v)
            target = (1-q)*sigma_A(m, q)
            const = len(set(vals)) == 1 and vals[0] == target
            if not const:
                triv_ok = False
            print(f"q={q} m=deg{deg(m)}{m}: A_D for D=deg m+1..+3 = {vals} ; (1-q)*sigma_A = {target} ; {'STABLE' if const else 'NOT STABLE'}")
    print()
    print("="*72)
    print(f"GATE 0 (identity exact):        {'PASS' if allok else 'FAIL'}")
    print(f"GATE 1 (global trivializes):    {'PASS' if triv_ok else 'FAIL'}")
    print("="*72)

if __name__ == "__main__":
    run()

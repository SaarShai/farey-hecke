"""
Robust c_chi: Method B (analytic, mpmath.diff) vs Method A (zero summation).
Focus first on the QUADRATIC (real) characters, which are what the -1 race uses.
"""
import mpmath as mp
mp.mp.dps = 40
import math, cmath
from sympy.ntheory.residue_ntheory import primitive_root
from sympy import totient

def char_mod(q):
    phi = int(totient(q)); g = primitive_root(q)
    dlog = {}; x = 1
    for k in range(phi):
        dlog[x] = k; x = (x*g) % q
    chars = []
    for j in range(1, phi):
        def make(j):
            def chi(n):
                n %= q
                if math.gcd(n, q) != 1: return 0
                return mp.e**(2j*mp.pi*dlog[n]*j/phi)
            return chi
        chi = make(j)
        is_even = abs(complex(chi(q-1)) - 1) < 1e-9
        order = phi//math.gcd(j,phi)
        chars.append((f"chi[j={j}]", chi, is_even, order))
    return chars, phi

def L_value(chi, q, s):
    total = mp.mpf(0)
    for r in range(1, q+1):
        c = chi(r)
        if c == 0: continue
        total += c * mp.zeta(s, mp.mpf(r)/q)
    return total * mp.power(q, -s)

def LpoverL(chi, q, s):
    f = lambda z: mp.log(L_value(chi, q, z))
    return mp.diff(f, s)

def c_chi_B(chi, q, is_even):
    a = 0 if is_even else 1
    arch = mp.log(mp.mpf(q)/mp.pi) + mp.digamma((1+a)/mp.mpf(2))
    fin = 2*mp.re(LpoverL(chi, q, mp.mpf(1)))
    return mp.re(arch + fin)

# ---------- Method A: sum over zeros via Z-function sign changes ----------
def completed_root_number(chi, q, is_even):
    pass

def Zfun_real(chi, q, is_even, t):
    """Hardy Z for a real primitive char: |Lambda(1/2+it)| with sign. We use
       Lambda(s)=(q/pi)^{(s+a)/2} Gamma((s+a)/2) L(s,chi). On the line s=1/2+it,
       Lambda(1/2+it) = epsilon^{1/2} * (real) when chi real & primitive; we just
       track sign changes of the rotated value Re( e^{-i theta(t)} Lambda(1/2+it) )."""
    a = 0 if is_even else 1
    s = mp.mpc(0.5, t)
    Lam = mp.power(mp.mpf(q)/mp.pi,(s+a)/2)*mp.gamma((s+a)/2)*L_value(chi,q,s)
    # root number for real primitive char is +1 (even) since Gauss sum tau(chi)=sqrt(q) (even) or i*sqrt(q)(odd)
    # epsilon = tau(chi)/(i^a sqrt(q)) = +1 for real primitive chi. So Lambda(1/2+it) e^{-i*?}...
    # For real chi, Lambda(1/2+it) is real-valued up to a fixed phase; use Z(t)=Lambda/|archimedean phase|.
    # Simplest robust: Z(t) = real-rotated. Since eps=1, Lambda(1/2+it) = conj(Lambda(1/2-it)),
    # so g(t):=Lambda(1/2+it) satisfies g(-t)=conj g(t) => g(t) e^{-i arg of gamma factor} is real.
    gphase = mp.power(mp.mpf(q)/mp.pi,(s+a)/2)*mp.gamma((s+a)/2)  # complex
    Z = mp.re(Lam / gphase * abs(gphase))  # rotate out arch phase
    return Z

def find_gammas(chi,q,is_even,Tmax=60,step=mp.mpf('0.05')):
    gammas=[]
    t=mp.mpf('0.0001'); prev=Zfun_real(chi,q,is_even,t)
    while t<Tmax:
        t2=t+step; cur=Zfun_real(chi,q,is_even,t2)
        if mp.re(prev)*mp.re(cur)<0:
            g=mp.findroot(lambda x: mp.re(Zfun_real(chi,q,is_even,x)),(t+t2)/2)
            gammas.append(mp.re(g))
        prev=cur; t=t2
    return gammas

def c_chi_A(chi,q,is_even,Tmax=200):
    gammas=find_gammas(chi,q,is_even,Tmax=Tmax)
    s=mp.mpf(0)
    for g in gammas:
        s+= 1/(mp.mpf(1)/4+g**2)
    # tail estimate: N(T)~ (T/pi) log(qT/2pi e); density n(t)~(1/pi)log(qt/2pi)
    # tail sum ~ integral_Tmax^inf (1/pi)log(q t/2pi)/t^2 dt
    def tail():
        import mpmath
        return mp.quad(lambda t: (1/mp.pi)*mp.log(q*t/(2*mp.pi))/t**2,[Tmax,mp.inf])
    return s, 2*tail(), gammas  # factor 2 for +-gamma pairs

print("=== Quadratic / real characters: Method A vs Method B ===")
for q in [3,4,5,7,8,11]:
    chars,phi=char_mod(q)
    for name,chi,even,order in chars:
        if order!=2:   # only real (quadratic) chars
            continue
        cB=c_chi_B(chi,q,even)
        cA,tail,gammas=c_chi_A(chi,q,even,Tmax=150)
        print(f"q={q} {name} order={order} {'even' if even else 'odd'}: "
              f"cB={mp.nstr(cB,9)}  cA(|g|<150,x2)={mp.nstr(2*cA,9)} +tail{mp.nstr(tail,3)} "
              f"=> cA_tot={mp.nstr(2*cA+tail,9)}  first gammas={[mp.nstr(g,6) for g in gammas[:3]]}")

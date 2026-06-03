"""
Rubinstein-Sarnak covariance structure of the limiting distribution, and the
DIFFERENCE race E(-1) - E(a) among non-residues.

EXPLICIT FORMULA.  With psi(x;N,a) the weighted prime count and the standard
reduction to pi, the normalized error
   E(x;N,a) = (phi(N) log x / sqrt x)( pi(x;N,a) - pi(x;N,1) )
has the explicit-formula expansion (Rubinstein-Sarnak 1994, Sec 2-3):

   E(e^y; N,a) = -c(a)  -  sum_{chi != chi0} (conj chi(a) - 1) * sum_{gamma_chi}
                   2 Re( e^{i gamma_chi y} / (1/2 + i gamma_chi) ) + o(1)

where gamma_chi runs over imaginary parts of nontrivial zeros of L(s,chi) on
the critical line (GRH), and c(a) = -mu(a) = 1 - #sqrt(a).

Under LI (linear independence of the gamma's over Q), the {cos(gamma y),
sin(gamma y)} behave like independent uniform phases. The limiting random
variable is therefore

   X_a = -c(a) + sum_{chi != chi0} (conj chi(a) - 1) * Z_chi

NOTE on pairing: zeros come in conjugate pairs gamma, -gamma and chi pairs with
conj chi.  Combining chi and conj chi: the random contribution to X_a is

   X_a = mu(a) + sum_{chi != chi0}  b(chi,a) * V_chi ,
   V_chi = sum_{gamma_chi>0} (2/sqrt(1/4+gamma^2)) * (independent mean-0 unit r.v.)

The COVARIANCE that matters:  Var(X_a - X_b).  Since the leading means are equal
for two non-residues a,b (mu=-1 both), the race  D(-1)>D(a)  i.e. X_{-1} > X_a
is decided ENTIRELY by the fluctuation term  X_{-1} - X_a, a mean-ZERO random
variable, plus the SKEWNESS of the joint law.

The covariance of the RS limiting vector (Rubinstein-Sarnak Thm/Lemma; also
Fiorilli-Martin) is:

   Cov(X_a, X_b) = sum_{chi != chi0}  conj(chi(a)) chi(b) * V(chi)     [Hermitian form]

with V(chi) = sum_{gamma_chi} 1/(1/4 + gamma_chi^2)  =  b(1,chi)  (a positive
real depending only on chi, = 2*sum_{gamma>0}1/(1/4+gamma^2)).

Because V(chi)=V(conj chi) and we sum chi with conj(chi(a))chi(b), Cov is real.

KEY COMPUTABLE OBJECT for the difference race:
   Var(X_{-1} - X_a) = Cov(-1,-1) - 2 Cov(-1,a) + Cov(a,a)
                     = sum_chi V(chi) |chi(-1) - chi(a)|^2.

Since chi(-1) = +-1 always (as (-1)^2=1), chi(-1) in {+1,-1}.
   |chi(-1)-chi(a)|^2 = |+-1 - chi(a)|^2.

We compute Var(X_{-1}-X_a) symbolically in terms of the V(chi)'s, and identify
which characters separate -1 from a generic non-residue a.
"""
import sympy
from sympy import Rational, exp, I, pi, gcd

def units(N):
    return [a for a in range(1,N) if gcd(a,N)==1]

def dirichlet_chars(N):
    """All Dirichlet characters mod N as dict a->value (exact cyclotomic via sympy).
    Use group structure: decompose (Z/N)* generators. We'll use sympy's
    representation via discrete log over the unit group built explicitly."""
    U = units(N)
    # Build the abelian group (Z/N)* and its character table by brute force:
    # find generators via Smith / just enumerate characters as homomorphisms.
    # Simpler: use the structure that characters are indexed by elements of the
    # dual; we construct them via the group's cyclic decomposition.
    from sympy.combinatorics import Permutation
    # Build multiplication and find independent generators with their orders.
    # Use a direct approach: represent each unit by exponent vector over chosen gens.
    import itertools
    # find a generating set by greedy
    gens=[]
    orders=[]
    covered={1}
    def order(g):
        o=1; x=g
        while x!=1:
            x=(x*g)%N; o+=1
        return o
    rem=set(U)-{1}
    # greedy independent generators
    basis=[]  # list of (g, order)
    subgroup={1}
    def gen_subgroup(elems):
        S={1}
        changed=True
        while changed:
            changed=False
            for e in elems:
                for s in list(S):
                    v=(s*e)%N
                    if v not in S:
                        S.add(v); changed=True
        return S
    for g in U:
        if g==1: continue
        newS=gen_subgroup([x for x,_ in basis]+[g])
        if len(newS)>len(subgroup):
            basis.append((g,order(g)))
            subgroup=newS
            if len(subgroup)==len(U):
                break
    # exponent-vector coordinates for each unit
    coords={}
    gen_elems=[g for g,_ in basis]
    gen_ords=[o for _,o in basis]
    ranges=[range(o) for o in gen_ords]
    for exps in itertools.product(*ranges):
        val=1
        for g,e in zip(gen_elems,exps):
            val=(val*pow(g,e,N))%N
        coords[val]=exps
    # characters: choose root-of-unity exponent for each generator
    chars=[]
    for kexps in itertools.product(*[range(o) for o in gen_ords]):
        def make_chi(kexps=kexps):
            def chi(a):
                a%=N
                e=coords[a]
                # value = prod exp(2pi i * k_j e_j / o_j)
                val=sympy.Integer(1)
                arg=sympy.Integer(0)
                for kj,ej,oj in zip(kexps,e,gen_ords):
                    arg+=Rational(kj*ej,oj)
                return sympy.exp(2*sympy.pi*sympy.I*arg)
            return chi
        chars.append(make_chi())
    return chars, gen_elems, gen_ords, coords

def chi_val(kexps, a, coords, gen_ords):
    e=coords[a%list(coords.keys()) and 0]  # placeholder
    return None

# Simpler explicit character values via coords:
def build(N):
    U=units(N)
    import itertools
    def order(g):
        o=1;x=g
        while x!=1: x=(x*g)%N; o+=1
        return o
    def gen_subgroup(elems):
        S={1}; changed=True
        while changed:
            changed=False
            for e in elems:
                for s in list(S):
                    v=(s*e)%N
                    if v not in S: S.add(v); changed=True
        return S
    basis=[]; subgroup={1}
    for g in U:
        if g==1: continue
        newS=gen_subgroup([x for x,_ in basis]+[g])
        if len(newS)>len(subgroup):
            basis.append((g,order(g))); subgroup=newS
            if len(subgroup)==len(U): break
    gen_elems=[g for g,_ in basis]; gen_ords=[o for _,o in basis]
    coords={}
    for exps in itertools.product(*[range(o) for o in gen_ords]):
        val=1
        for g,e in zip(gen_elems,exps): val=(val*pow(g,e,N))%N
        coords[val]=exps
    chars=list(itertools.product(*[range(o) for o in gen_ords]))
    def chi_value(kexps,a):
        e=coords[a%N]
        arg=sum(Rational(kj*ej,oj) for kj,ej,oj in zip(kexps,e,gen_ords))
        return sympy.exp(2*sympy.pi*sympy.I*arg)
    def is_principal(kexps):
        return all(k==0 for k in kexps)
    def is_real(kexps):
        # chi real iff chi^2 principal iff 2*kexps == 0 mod ords
        return all((2*kj)%oj==0 for kj,oj in zip(kexps,gen_ords))
    return U,gen_elems,gen_ords,coords,chars,chi_value,is_principal,is_real

for N in [7,8,11,12]:
    U,ge,go,coords,chars,chi_value,is_principal,is_real=build(N)
    print(f"\n===== N={N}  units={U}  gens={ge} orders={go}  #chars={len(chars)} =====")
    m1=(N-1)  # -1 mod N
    # For each non-residue a, compute |chi(-1)-chi(a)|^2 for each non-principal chi,
    # and which chars are 'active' (contribute) and whether chi(-1) distinguishes.
    sq=set((b*b)%N for b in U)
    nqr=[a for a in U if a not in sq]
    # chi(-1): real char value +-1
    print("chi(-1) for each char:")
    for k in chars:
        if is_principal(k): continue
        v=sympy.simplify(chi_value(k,m1))
        print(f"  chi_{k}: chi(-1)={v}   real_char={is_real(k)}")

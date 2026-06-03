"""
WHY is a=-1 special among non-residues?  Pin down the exact mechanism.

The race a-vs-1: D_a = X_a - X_1.
  mean(D_a) = mu_a - mu_1, mu_a=-1+#sqrt(a). For NR a: mu_a=-1. For a=1: mu_1=-1+#sqrt(1).
  So mean(D_a) = -#sqrt(1) for EVERY non-residue (same).  [#sqrt(1)=#{b:b^2=1}=2^t]
  Var(D_a) = sum_chi c_chi |chi(a)-1|^2.

KEY STRUCTURE:  chi(a)-1 and the variance.
  - For a REAL character chi (chi^2=chi0, i.e. chi quadratic), chi(a) in {+1,-1}.
       |chi(a)-1|^2 = 0 if chi(a)=1, = 4 if chi(a)=-1.
  - For a COMPLEX character chi, |chi(a)-1|^2 = 2-2cos(arg) in (0,4].

Now: a=-1.  For ANY character chi, chi(-1)=+1 (chi even) or -1 (chi odd).
  => chi(-1)-1 = 0  for even chi,  = -2 for odd chi.
  So in Var(D_{-1}) = sum_{chi odd} c_chi * 4   -- ONLY ODD characters contribute,
  each with the MAXIMAL weight |chi(-1)-1|^2 = 4.

Compare a generic non-residue a != -1: chi(a) is spread over roots of unity;
|chi(a)-1|^2 averages to 2 (= E|zeta-1|^2 over roots of unity) and only hits the
max 4 when chi(a)=-1.

CLAIM TO TEST:  among non-residues, a=-1 MAXIMIZES the variance Var(D_a)?  Or
MINIMIZES it?  And does the winner of the density race correspond to max or min
variance (given equal, negative mean)?

With equal negative mean m<0 and variance V:  delta = P(D>0).  For a symmetric-ish
distribution, larger V -> more spread -> P(D>0) CLOSER to 1/2 from below -> LARGER
(less negative-dominated).  So if -1 has the LARGEST variance among NR, it has the
LARGEST density -> -1 leads.  TEST THIS with actual c_chi WEIGHTING.

We need c_chi per character. We approximate c_chi by its DOMINANT behaviour:
c_chi ~ depends weakly on chi (all O(0.1-0.3)); the DISCRIMINATING factor is the
COMBINATORICS of |chi(a)-1|^2 summed over chi, weighted by c_chi.  First test with
c_chi=1 for all chi (pure combinatorics), then with realistic c_chi (odd chars have
slightly larger c_chi than even -- digamma(1/2) vs digamma(1) differ).
"""
import math, cmath
from sympy.ntheory.residue_ntheory import primitive_root
from sympy import totient

def all_chars(q):
    """All nonprincipal Dirichlet chars mod q for q with a primitive root (q=p, 2p, 4, ...).
       Returns list of (chi as dict a->complex, is_odd)."""
    phi=int(totient(q)); g=primitive_root(q)
    if g is None: raise ValueError(f"no primitive root mod {q}")
    dlog={}; x=1
    for k in range(phi):
        dlog[x%q]=k; x=(x*g)%q
    units=[a for a in range(1,q) if math.gcd(a,q)==1]
    chars=[]
    for j in range(1,phi):
        chi={a: cmath.exp(2j*math.pi*dlog[a]*j/phi) for a in units}
        is_odd = abs(chi[(q-1)%q]+1)<1e-9
        chars.append((chi,is_odd))
    return chars, units, phi

def variance_combinatoric(q, c_even=1.0, c_odd=1.0):
    """Var(D_a)/ (scale) = sum_chi c_chi |chi(a)-1|^2 with c_chi=c_even or c_odd."""
    chars, units, phi = all_chars(q)
    sqs=set((b*b)%q for b in units)
    out={}
    for a in units:
        V=0.0
        for chi,is_odd in chars:
            c = c_odd if is_odd else c_even
            V += c*abs(chi[a]-1)**2
        out[a]=(V, a in sqs)
    return out, sqs

def report(title, c_even, c_odd):
    print(title)
    for q in [7,11,19,23]:   # primes 3 mod 4, so -1 is a NON-residue
        out,sqs=variance_combinatoric(q, c_even=c_even, c_odd=c_odd)
        minus1=(q-1)%q
        assert minus1 not in sqs, f"-1 should be NR for q={q}"
        nrs=sorted([(V,a) for a,(V,isq) in out.items() if not isq], reverse=True)
        order=[a for V,a in nrs]
        rank_m1=order.index(minus1)+1
        vmax=nrs[0][0]; vm1=out[minus1][0]
        tag="LARGEST" if rank_m1==1 else f"rank {rank_m1}"
        print(f"  q={q}: V(-1)={vm1:.4f}  max NR V={vmax:.4f}  -1 is {tag} of {len(nrs)} NR"
              + ("  <== -1 has MAX variance" if rank_m1==1 else ""))

# digamma(1)= -gamma_E = -0.5772; digamma(1/2)= -gamma_E -2 ln2 = -1.9635.
# c_chi = log(q/pi) + digamma((1+a)/2) + 2 Re L'/L(1,chi).  ODD (a=1) has digamma(1)
# = -0.5772 which is LARGER (less negative) than EVEN (a=0) digamma(1/2)=-1.9635.
# So at fixed q, the archimedean part makes c_chi LARGER for ODD characters.
report("Test 1: c_chi=1 for all (pure combinatorics):", 1.0, 1.0)
report("\nTest 2: realistic parity split -- odd chars heavier (c_odd > c_even):", 0.7, 1.0)
report("\nTest 3: exaggerated parity split (c_odd >> c_even):", 0.3, 1.0)

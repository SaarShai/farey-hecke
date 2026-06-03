"""
RS limiting-distribution Monte Carlo for delta(N; b, a) = P(X_b > X_a),
built directly from the explicit formula under GRH+LI.

X_a = mu(a) + sum_{chi != chi0} conj(chi(a)) * Y_chi ,
 Y_chi = sum_{gamma_chi > 0} (2 / sqrt(1/4+gamma^2)) * cos(theta_{chi,gamma})  [real part bundling]
Actually the precise RS form: contribution of zeros of L(s,chi) (with conj pair
combined) to E(e^y;N,a) is
   - sum_{gamma_chi>0} 2 * [ cos(gamma y) ... ] ... .
We use the standard reduction (Rubinstein-Sarnak 1994, eq 2.1; Fiorilli-Martin):
the random variable for the *vector* (E_a) is, under LI, with iid phases
U_{chi,gamma} ~ Uniform(0,2pi) (one per zero of each chi, conj-paired):

  X_a = mu(a) + sum_{chi!=chi0} sum_{gamma_chi>0} (2/sqrt(1/4+gamma^2)) *
          Re( conj(chi(a)) * e^{i U_{chi,gamma}} )

with the constraint U_{conj chi, gamma} = - U_{chi, gamma} so that X_a is real
and chi, conjchi are coupled. Equivalently, for each unordered conj-pair we draw
ONE phase. For a self-conjugate (real) chi, chi(a)=+-1 and the term is
(2/sqrt(1/4+gamma^2)) chi(a) cos(U).

This is exactly the standard model. We Monte-Carlo it.
"""
import mpmath as mp
import numpy as np
import json, sys
from get_zeros import char_table

def cval_c(k,a,coords,go):
    e=coords[a%999999] if False else coords[a]
    arg=sum((kj*ej)/oj for kj,ej,oj in zip(k,e,go))
    return np.exp(2j*np.pi*arg)

def units(N):
    from math import gcd
    return [a for a in range(1,N) if gcd(a,N)==1]

def mu_vec(N):
    # RS mean of normalized X_a (race a vs 1): squares of primes inflate
    # square classes; the limiting mean is -#sqrt(a). Differences against class 1
    # then give the correct +bias toward non-residues. (The additive -1 offset used
    # earlier cancels in any difference and is dropped here for correct sign.)
    U=units(N); sc={a:0 for a in U}
    for b in U: sc[(b*b)%N]+=1
    return {a:-sc[a] for a in U}

def run(N, zeros_json, M=400000, seed=0):
    U,ge,go,coords,chars,cval=char_table(N)
    z=json.load(open(zeros_json))
    rng=np.random.default_rng(seed)
    nonp=[k for k in chars if not all(x==0 for x in k)]
    # group into conjugate pairs. conj of char k is (-k mod ord) componentwise.
    def conj(k): return tuple((-kj)%oj for kj,oj in zip(k,go))
    seen=set(); pairs=[]
    for k in nonp:
        if k in seen: continue
        kc=conj(k)
        seen.add(k); seen.add(kc)
        pairs.append((k,kc))
    # Precompute, for each pair, the zero weights and chi(a) values.
    mu=mu_vec(N)
    # character value table
    def chival(k,a):
        e=coords[a]; arg=sum((kj*ej)/oj for kj,ej,oj in zip(k,e,go))
        return np.exp(2j*np.pi*arg)
    # Build samples of X_a for all a simultaneously.
    X={a:np.full(M, mu[a], dtype=float) for a in U}
    for (k,kc) in pairs:
        gammas=np.array(z[str(k)])
        if len(gammas)==0:
            # imprimitive real char may be stored under k; if missing use kc
            gammas=np.array(z.get(str(kc),[]))
        w=2.0/np.sqrt(0.25+gammas**2)   # per-zero amplitude
        # draw phases: one per zero, shared across all a (the SAME zeros drive all classes)
        # term for class a from this pair: sum_gamma w * Re( conj(chi(a)) e^{iU} )
        # plus the conj pair kc contributes conj(chi(a)) with conj -> together:
        # if k != kc (complex pair): total = sum_gamma w*2*Re( conj(chi(a)) e^{iU} )? 
        # Careful: pair already bundles chi and conjchi. Each has its OWN zeros but
        # zeros of conjchi are the same set (conjugate symmetry: gamma of conjchi =
        # gamma of chi). Contribution chi: Re(conj chi(a) e^{iU}); conjchi:
        # Re(conj conjchi(a) e^{iU'}) with U'=-U => Re(chi(a) e^{-iU}) = Re(conj(chi(a) e^{iU}))
        # = same as first. So pair gives 2*Re(conj chi(a) e^{iU}). For real char k=kc
        # it gives 1*Re(...) = chi(a) cos U.
        for gi in range(len(gammas)):
            U_phase=rng.uniform(0,2*np.pi,M)
            cosU=np.cos(U_phase); sinU=np.sin(U_phase)
            for a in U:
                ca=chival(k,a)  # chi(a)
                conj_ca=np.conj(ca)
                # Re(conj_ca * e^{iU}) = Re(conj_ca)cosU - Im(conj_ca)sinU
                re_term=conj_ca.real*cosU - conj_ca.imag*sinU
                mult = w[gi]*(2.0 if k!=kc else 1.0)
                X[a]+= mult*re_term
    return X, mu

if __name__=="__main__":
    N=int(sys.argv[1])
    M=int(sys.argv[2]) if len(sys.argv)>2 else 300000
    X,mu=run(N, f"zeros_N{N}.json", M=M)
    U=units(N)
    sq=set((b*b)%N for b in U); nqr=[a for a in U if a not in sq]
    m1=N-1
    print(f"N={N}  non-residues={nqr}  (-1 = {m1})")
    print(f"sample means (should ~ mu): "+", ".join(f"{a}:{np.mean(X[a]):+.3f}(mu{mu[a]:+d})" for a in U if a!=1))
    print(f"\ndelta(N;-1,a)=P(X_-1 > X_a) for non-residues a != -1:")
    for a in nqr:
        if a==m1: continue
        d=np.mean(X[m1]>X[a])
        # also skewness of difference
        W=X[m1]-X[a]
        s=np.std(W); sk=np.mean((W-np.mean(W))**3)/s**3 if s>0 else 0
        print(f"  a={a:3d}: delta={d:.4f}   meanW={np.mean(W):+.4f} sdW={s:.3f} skew(W)={sk:+.4f}")
    # also -1 vs every QR for context
    print("for reference, delta(-1, QR):")
    for a in U:
        if a in nqr or a==1: continue
        d=np.mean(X[m1]>X[a]); print(f"  a={a:3d}(QR): delta={d:.4f}")

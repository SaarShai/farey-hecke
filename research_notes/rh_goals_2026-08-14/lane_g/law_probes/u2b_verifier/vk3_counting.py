# INDEPENDENT test of THEOREM U2b-C: compare the CLAIMED bound against a direct
# partial sum over primitive cyclic words (a partial sum can only refute, never confirm).
import math, itertools, sys

def zeta(s,N=200000):
    tot=sum(k**-s for k in range(1,N))
    tot+=N**(1-s)/(s-1)+0.5*N**-s+s*N**(-s-1)/12.0
    return tot

def W(q,e_h,e_l):
    s=math.sin(math.pi/q); lam=2*math.cos(math.pi/q)
    h=sum((math.sin(a*math.pi/q)/s)**-e_h for a in range(2,q-1))
    return h+2*(lam**-e_l)*zeta(e_l)

def direct(q,MMAX,sig):
    lam=2*math.cos(math.pi/q)
    s=math.sin(math.pi/q); uu=[math.sin(j*math.pi/q)/s for j in range(q+2)]
    M={a:((uu[a],uu[a+1]),(uu[a-1],uu[a])) for a in range(1,q)}
    tot_tr=0.0; tot_S=0.0; n=0
    for m in range(1,MMAX+1):
        for w in itertools.product(range(1,q),repeat=m):
            rots=[w[i:]+w[:i] for i in range(m)]
            if w!=min(rots) or len(set(rots))!=m: continue
            P=((1.0,0.0),(0.0,1.0))
            for a in w:
                B=M[a]
                P=((P[0][0]*B[0][0]+P[0][1]*B[1][0],P[0][0]*B[0][1]+P[0][1]*B[1][1]),
                   (P[1][0]*B[0][0]+P[1][1]*B[1][0],P[1][0]*B[0][1]+P[1][1]*B[1][1]))
            t=abs(P[0][0]+P[1][1])
            if t<=2+1e-12: continue
            n+=1
            tot_tr+=t**(-2*sig)
            l=2*math.acosh(t/2)
            tot_S+=math.exp(-sig*l)/(1-math.exp(-l))
    return tot_tr,tot_S,n

e_h,e_l=3.0,4.0; sig=3.5
lam5=2*math.cos(math.pi/5); t0=2*lam5
c0=(1+math.sqrt(1-4/t0**2))/2
sys5=2*math.acosh(lam5)
print(f"claimed bound on sum|tr|^-2sig : {(2**-e_h)*math.log(1/(1-max(W(q,e_h,e_l) for q in list(range(5,41))+[50,60,80,120,200,400,1000,3000]))):.6f}")
for q,MM in [(5,11),(6,9),(7,8),(8,7),(9,7),(10,6),(12,6),(16,5),(20,5)]:
    tt,ss,n=direct(q,MM,sig)
    wq=W(q,e_h,e_l)
    bnd_tr=(2**-e_h)*math.log(1/(1-wq))
    bnd_S=(c0**(-2*sig))*bnd_tr/(1-math.exp(-sys5))
    print(f"q={q:3d} m<={MM} nhyp={n:8d} W_q={wq:.6f} | direct sum|tr|^-7={tt:.6e} <= per-q bound {bnd_tr:.6e} ? {tt<=bnd_tr}"
          f" | direct S_q(3.5)={ss:.6e} <= 0.4861 ? {ss<=0.4861}")
    sys.stdout.flush()

# Theorem U2b-B with MIXED-SIGN syllables (the case the author's probe never tested).
import math, itertools
def u(j,lam):
    th=math.acos(min(1.0,max(-1.0,lam/2.0)))
    return float(j) if th<1e-14 else math.sin(j*th)/math.sin(th)
viol=0; tested=0; worst=0.0
for A in range(1,8):
    for m in range(1,5):
        alpha=[a for a in range(-A,A+1) if a!=0]
        for w in itertools.product(alpha,repeat=m):
            if max(abs(a) for a in w)!=A: continue
            rots=[w[i:]+w[:i] for i in range(m)]
            if w!=min(rots) or len(set(rots))!=m: continue
            lo=2*math.cos(math.pi/(A+1)); prev=None; tested+=1
            for i in range(401):
                lam=lo+(2.0-lo)*i/400
                uu={j:u(j,lam) for j in range(0,A+2)}
                P=((1.0,0.0),(0.0,1.0))
                for a in w:
                    aa=abs(a)
                    B=((uu[aa],uu[aa+1]),(uu[aa-1],uu[aa])) if a>0 else ((uu[aa],uu[aa-1]),(uu[aa+1],uu[aa]))
                    P=((P[0][0]*B[0][0]+P[0][1]*B[1][0],P[0][0]*B[0][1]+P[0][1]*B[1][1]),
                       (P[1][0]*B[0][0]+P[1][1]*B[1][0],P[1][0]*B[0][1]+P[1][1]*B[1][1]))
                t=abs(P[0][0]+P[1][1])
                if prev is not None and t<prev-1e-9:
                    viol+=1; worst=max(worst,prev-t)
                prev=t
print(f"mixed-sign words tested={tested}  monotonicity violations={viol}  worst drop={worst}")
# literal (1,2] claim, exact
import math as M
f=lambda x: abs(2*(x**4-3*x**2+1))
print("|tr(SR^5)| at 1.2434 ->",f(1.2434)," at 1.5 ->",f(1.5)," => nondecreasing on (1,2]?",f(1.5)>=f(1.2434))
print("2*arccosh(3/2) =",2*M.acosh(1.5),"   (note asserts 1.08707)")

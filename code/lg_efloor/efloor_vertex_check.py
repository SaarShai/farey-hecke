"""
(A) Confirm V is the global Eform-min vertex of region R (all q>=5), by enumerating
    ALL feasible vertices and confirming V gives the min.
(B) Confirm q=3,4 region R is NONEMPTY (violation is real, not vacuous) and that
    the actual min there is < EfloorQ -> genuine failure for q=3,4.
(C) Cross-check: is V even IN the closure? need a>0,b>0,b<=1,a<=1,a+lb>=1 (other Dcorr edge),
    lb<=1+a (bracket lower). Verify all q>=5.
"""
import mpmath as mp
mp.mp.dps=50
def lamq(q): return 2*mp.cos(mp.pi/q)
def alphaC(l): return (l**2+2)/(l*(4-l**2))
def rhoC(l): return 2*mp.sqrt(2*l**2+1)/(l*(4-l**2))
def EfloorQ(l): return 1/(l**3*(alphaC(l)+rhoC(l)*(l/2)))
def Eform(l,a,b): return a**2-l*a*b+b**2

def feasible(l,a,b,tol):
    return (a>=-tol and a<=1+tol and b>=-tol and b<=1+tol
            and a+l*b>=1-tol and l*a+b>=1-tol
            and l*b<=1+a+tol and 1+a<=2*l*b+tol)

def line_intersect(L1,L2):
    (a1,b1,c1),(a2,b2,c2)=L1,L2
    det=a1*b2-a2*b1
    if abs(det)<mp.mpf(10)**(-40): return None
    return ((c1*b2-c2*b1)/det,(a1*c2-a2*c1)/det)

def vertices(l):
    lines=[(1,0,mp.mpf(0)),(1,0,mp.mpf(1)),(0,1,mp.mpf(0)),(0,1,mp.mpf(1)),
           (1,l,mp.mpf(1)),(l,1,mp.mpf(1)),(-1,l,mp.mpf(1)),(-1,2*l,mp.mpf(1))]
    names=['a=0','a=1','b=0','b=1','a+lb=1','la+b=1','lb=1+a','1+a=2lb']
    tol=mp.mpf(10)**(-30)
    out=[]
    for i in range(len(lines)):
        for j in range(i+1,len(lines)):
            pt=line_intersect(lines[i],lines[j])
            if pt is None: continue
            a,b=pt
            if feasible(l,a,b,tol):
                out.append((Eform(l,a,b),a,b,names[i],names[j]))
    out.sort()
    return out

def V(l):
    D=1+2*l**2; return ((2*l-1)/D,(1+l)/D)

print("(A) min vertex for q>=5 -- is it V (la+b=1 ∩ 1+a=2lb)?")
for q in [5,6,8,12,25,60,300]:
    l=lamq(q); vs=vertices(l)
    e,a,b,n1,n2=vs[0]
    va,vb=V(l)
    isV = abs(a-va)<mp.mpf(10)**(-20) and abs(b-vb)<mp.mpf(10)**(-20)
    print(f"q={q:>4}: min vertex E={float(e):.6e} at ({n1})∩({n2}) ; matchesV={isV}")

print("\n(B) q=3,4 region nonempty + min vertex < EfloorQ?")
for q in [3,4]:
    l=lamq(q); ef=EfloorQ(l); vs=vertices(l)
    print(f"q={q}: #feasible vertices={len(vs)}, EfloorQ={float(ef):.6e}")
    for e,a,b,n1,n2 in vs[:5]:
        print(f"    E={float(e):.6e} a={float(a):.4f} b={float(b):.4f} ({n1})∩({n2}) {'<EfloorQ VIOLATION' if e<ef else ''}")
    # interior sample to confirm nonempty area
    cnt=0
    for i in range(1,60):
        for j in range(1,60):
            a=mp.mpf(i)/60; b=mp.mpf(j)/60
            if feasible(l,a,b,mp.mpf(0)): cnt+=1
    print(f"    interior grid points feasible: {cnt}  (region {'NONEMPTY' if cnt>0 else 'EMPTY'})")

print("\n(C) V in closure for q>=5?")
for q in [5,6,10,50,500]:
    l=lamq(q); a,b=V(l)
    print(f"q={q:>4}: a={float(a):.4f} b={float(b):.4f} feasible={feasible(l,a,b,mp.mpf(10)**(-25))}")

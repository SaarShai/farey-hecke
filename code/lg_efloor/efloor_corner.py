"""
Locate the exact Eform-minimizer over the closed k=1 corridor region and check
the boundary structure.  The region:
  R = { 0<a<=1, 0<b<=1, a+l b>=1, l a+b>=1, l b <= 1+a, 1+a <= 2 l b }  (closure)
Eform is a positive-definite quadratic; its unconstrained min is 0 at origin,
so the constrained min is on the boundary, at a vertex of the polygon
(intersection of constraint lines), since Eform restricted to a segment is convex
=> min at an endpoint => vertex.  Enumerate all pairwise constraint intersections,
keep feasible ones, take min Eform.
"""
import mpmath as mp
mp.mp.dps = 60

def lamq(q): return 2*mp.cos(mp.pi/q)
def alphaC(l): return (l**2+2)/(l*(4-l**2))
def rhoC(l): return 2*mp.sqrt(2*l**2+1)/(l*(4-l**2))
def EfloorQ(l,q):
    c = mp.cos(mp.pi/q); return 1/(l**3*(alphaC(l)+rhoC(l)*c))
def Eform(l,a,b): return a**2 - l*a*b + b**2

# constraint lines as (coefA, coefB, rhs, sense) meaning coefA*a+coefB*b ?? rhs
# we represent each boundary line; feasibility tested by all inequalities.
def feasible(l,a,b,tol):
    return (a>=-tol and a<=1+tol and b>=-tol and b<=1+tol
            and a+l*b>=1-tol and l*a+b>=1-tol
            and l*b<=1+a+tol and 1+a<=2*l*b+tol)

def line_intersect(L1,L2):
    (a1,b1,c1),(a2,b2,c2)=L1,L2
    det=a1*b2-a2*b1
    if abs(det)<mp.mpf(10)**(-40): return None
    x=(c1*b2-c2*b1)/det
    y=(a1*c2-a2*c1)/det
    return (x,y)

def analyze(q):
    l=lamq(q); ef=EfloorQ(l,q)
    # boundary lines (as equalities a*coefA + b*coefB = rhs):
    lines=[
        (1,0,mp.mpf(0)),    # a=0
        (1,0,mp.mpf(1)),    # a=1
        (0,1,mp.mpf(0)),    # b=0
        (0,1,mp.mpf(1)),    # b=1
        (1,l,mp.mpf(1)),    # a+l b=1
        (l,1,mp.mpf(1)),    # l a+b=1
        (-1,l,mp.mpf(1)),   # -a+l b=1  (l b=1+a)
        (-1,2*l,mp.mpf(1)), # -a+2 l b=1 (1+a=2 l b)
    ]
    tol=mp.mpf(10)**(-30)
    best=None;bestpt=None
    for i in range(len(lines)):
        for j in range(i+1,len(lines)):
            pt=line_intersect(lines[i],lines[j])
            if pt is None: continue
            a,b=pt
            if feasible(l,a,b,tol):
                e=Eform(l,a,b)
                if best is None or e<best:
                    best=e;bestpt=(a,b,i,j)
    return l,ef,best,bestpt

for q in [3,4,5,6,10,30,100,1000]:
    l,ef,best,pt=analyze(q)
    if best is None:
        print(f"q={q}: region empty (no feasible vertex)"); continue
    diff=best-ef
    print(f"q={q:>5} l={float(l):.6f} EfloorQ={float(ef):.8e} minE(vertex)={float(best):.8e} diff={float(diff):.3e} ratio={float(best/ef):.6f}")
    a,b,i,j=pt
    print(f"        minimizer a={float(a):.6f} b={float(b):.6f}  (lines {i},{j})  {'VIOLATION' if diff<0 else 'OK'}")

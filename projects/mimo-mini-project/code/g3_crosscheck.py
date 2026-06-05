import numpy as np, math

# Chebyshev X for general q: X(-1)=0,X(0)=1,X(i+1)=lam X(i)-X(i-1)
def Xtab(q):
    lam=2*math.cos(math.pi/q)
    X={-1:0.0,0:1.0}
    for i in range(1,q+2): X[i]=lam*X[i-1]-X[i-2]
    return X,lam

def step(a,b,q,X,lam):
    # find branch i in [2,q-1]: smallest with a X(i-1)+b X(i-2)>1 and a X(i)+b X(i-1)<=1
    for i in range(2,q):
        if a*X[i-1]+b*X[i-2] > 1+1e-12 and a*X[i]+b*X[i-1] <= 1+1e-12:
            br=i; break
    else:
        return None
    Li  = a*X[br]+b*X[br-1]
    Li1 = a*X[br+1]+b*X[br]
    if abs(X[br-1])<1e-15: return None
    P = a*Li/X[br-1]
    k = math.floor((1-Li1)/(lam*Li))
    ap=Li; bp=Li1+k*lam*Li
    return ap,bp,P,br,k

# ---- q=3 focused ----
q=3; X,lam=Xtab(q)
print(f"q={q} lam={lam:.6f} thr=1/lam^3={1/lam**3:.6f}")
print("X:",{k:round(v,4) for k,v in X.items()})

# verify map reduces to (a,b)->(b,kb-a), k=floor((1+a)/b), P=ab
def s3(a,b):
    k=math.floor((1+a)/b); return b, k*b-a, a*b, k

# search global min of sup-P over orbits: grid seeds in triangle, iterate, asymptotic sup
def supP_orbit(a,b,N=4000,skip=1000):
    m=0.0
    for n in range(N):
        if not(0<a<=1.0+1e-9 and b>1-a-1e-9 and b<=1+1e-9):
            # renormalize into fundamental strip if drift; clamp check
            pass
        b2=b; a2,b2,p,k=s3(a,b)[0],None,None,None
        a,bn,p,k=s3(a,b)
        b=bn
        if n>skip: m=max(m,p)
        if not np.isfinite(a) or abs(a)>1e6: return np.inf
    return m

# coarse grid over triangle
best=(np.inf,None)
for a in np.linspace(0.02,0.999,400):
    for b in np.linspace(max(1e-3,1-a)+1e-4,1.0,200):
        try:
            m=supP_orbit(a,b,N=2500,skip=800)
        except Exception:
            m=np.inf
        if m<best[0]: best=(m,(a,b))
print("grid min sup-P =",round(best[0],6),"at seed",tuple(round(x,5) for x in best[1]))
print("  2/9 =",2/9, " 1/4 =",0.25)

# the candidate boundary 2-cycle {(1/3,2/3),(2/3,1/3)} -> monodromy
def Mk(k): return np.array([[0,1],[-1,k]],float)
# (1/3,2/3): k=floor((1+1/3)/(2/3))=floor(2)=2? check
for (a,b) in [(1/3,2/3),(2/3,1/3),(0.34,0.66),(0.4,0.6)]:
    nb,nc,p,k=s3(a,b)
    print(f"  ({a:.4f},{b:.4f}) k={k} -> ({nb:.4f},{nc:.4f}) P={p:.5f}")

# trace of period-2 monodromy for the near-(1/3,2/3) orbit
a,b=0.3334,0.6666
seq=[]
for _ in range(2):
    nb,nc,p,k=s3(a,b); seq.append(k); a,b=nb,nc
M=np.eye(2)
for k in seq[::-1]: M=M@Mk(k)
print("period-2 ks:",seq,"monodromy trace=",round(np.trace(M),4),
      "->", "elliptic" if abs(np.trace(M))<2-1e-9 else ("parabolic" if abs(abs(np.trace(M))-2)<1e-6 else "hyperbolic"))

# also the exact boundary cycle ks
a,b=1/3+1e-6,2/3
seq=[]
for _ in range(2):
    nb,nc,p,k=s3(a,b); seq.append(k); a,b=nb,nc
M=np.eye(2)
for k in seq[::-1]: M=M@Mk(k)
print("boundary cycle ks:",seq,"trace=",round(np.trace(M),6))

"""
Test whether B(q) is a Beatty/Fraenkel sequence floor(alpha*q + beta) and characterize
the resonant set as a three-distance / equidistribution object rather than a modular rule.
Reads 'D8 q B wqp P1 P2' lines.
"""
import math, sys
import numpy as np
from collections import Counter
try:
    from sympy import isprime
except Exception:
    def isprime(n):
        if n<2: return False
        for p in range(2,int(n**0.5)+1):
            if n%p==0: return False
        return True

rows={}
for fn in sys.argv[1:]:
    for line in open(fn):
        if line.startswith("D8 "):
            _,q,B,wqp,P1,P2=line.split()
            rows[int(q)]=(int(B),float(wqp),int(P1),int(P2))
qs=sorted(rows)
B={q:rows[q][0] for q in qs}; WQP={q:rows[q][1] for q in qs}
P1={q:rows[q][2] for q in qs}; P2={q:rows[q][3] for q in qs}
print(f"q range {qs[0]}..{qs[-1]} ({len(qs)})")
print("B(q):", [B[q] for q in qs])

# --- Beatty fit: best alpha,beta minimizing #mismatches of floor(alpha q+beta) ---
best=None
for alpha in np.linspace(0.205,0.225,401):
    for beta in np.linspace(0.0,1.5,151):
        mm=sum(1 for q in qs if int(math.floor(alpha*q+beta))!=B[q])
        if best is None or mm<best[0]: best=(mm,alpha,beta)
mm,alpha,beta=best
print(f"\nBest Beatty floor(alpha*q+beta): alpha={alpha:.5f} beta={beta:.4f}  mismatches={mm}/{len(qs)}")
mismB=[q for q in qs if int(math.floor(alpha*q+beta))!=B[q]]
print("  Beatty mismatches at q:", mismB)

# --- compare to round(Winf/pi * q + c) ---
print("\nW_inf/pi from large-q wqp/q:", np.mean([WQP[q]/q for q in qs if q>=80]))

# --- jump points of B ---
jumps=[q for q in qs if q-1 in B and B[q]>B[q-1]]
print("\nB jump points:", jumps)
print("jump gaps:", [jumps[i+1]-jumps[i] for i in range(len(jumps)-1)])
gapc=Counter(jumps[i+1]-jumps[i] for i in range(len(jumps)-1))
print("gap multiset (three-distance => few distinct values):", dict(sorted(gapc.items())))

# --- P1-resonance set (the deep one) ---
R1=[q for q in qs if B[q]>P1[q]]
R1anti=[q for q in qs if B[q]<P1[q]]
print("\n=== R1 = {B>floor(Wq/pi)+1} (lattice-vs-notch resonance) ===")
print("R1:",R1)
print("R1 anti (B<P1):",R1anti)
print("frac{Wq/pi} at R1:", [(q, round(WQP[q]-math.floor(WQP[q]),3)) for q in R1])
print("frac{Wq/pi} at R1anti:", [(q, round(WQP[q]-math.floor(WQP[q]),3)) for q in R1anti])

# --- residue tests on R1 ---
if R1:
    for n in [2,3,4,5,6,7,8,9,10,12]:
        c=Counter(q%n for q in R1)
        print(f"  R1 mod {n}: {dict(sorted(c.items()))}")
    print("  R1 primes:", [q for q in R1 if isprime(q)])
    print("  R1 diffs:", [R1[i+1]-R1[i] for i in range(len(R1)-1)])

# --- P2-resonance set (task stated) ---
R2=[q for q in qs if B[q]>P2[q]]
print("\n=== R2 = {B>2+floor((q-1)/6)} (task-stated; baseline slope 1/6<0.216 => grows) ===")
print("R2:",R2)
print("density R2:", len(R2)/len(qs))
D2=[B[q]-P2[q] for q in qs]
print("D2=B-P2 range:", min(D2),"..",max(D2), " (grows => NOT sparse arithmetic set)")

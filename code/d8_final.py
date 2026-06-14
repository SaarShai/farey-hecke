import math, sys
import numpy as np
from collections import Counter
def isprime(n):
    if n<2: return False
    if n%2==0: return n==2
    for p in range(3,int(n**0.5)+1,2):
        if n%p==0: return False
    return True

rows={}
for fn in sys.argv[1:]:
    try:
        for line in open(fn):
            if line.startswith("D8 "):
                _,q,B,wqp,P1,P2=line.split()
                q=int(q)
                rows[q]=(int(B),float(wqp),int(P1),int(P2))
    except FileNotFoundError: pass
qs=sorted(rows)
B={q:rows[q][0] for q in qs}; WQP={q:rows[q][1] for q in qs}
P1={q:rows[q][2] for q in qs}; P2={q:rows[q][3] for q in qs}
print(f"FULL RANGE q={qs[0]}..{qs[-1]} ({len(qs)} values)")

# R1 = genuine resonance: B > floor(Wq/pi)+1
R1=[q for q in qs if B[q]>P1[q]]
R1anti=[q for q in qs if B[q]<P1[q]]
print("\n===== R1 = {q: B(q) > floor(W(q)q/pi)+1}  (lattice-vs-notch / Beatty-boundary resonance) =====")
print("R1 =", R1)
print("R1 anti (B<P1) =", R1anti)
print("R1 fracs {Wq/pi}:", [(q, round(WQP[q]%1,3)) for q in R1])
if R1:
    print("R1 diffs:", [R1[i+1]-R1[i] for i in range(len(R1)-1)])
    print("R1 all prime?:", all(isprime(q) for q in R1), " primes:", [q for q in R1 if isprime(q)])
    for n in [2,3,4,5,6,7,12]:
        print(f"  R1 mod {n}: {dict(sorted(Counter(q%n for q in R1).items()))}")

# Beatty fit of B over full range
best=None
for alpha in np.linspace(0.205,0.222,341):
    for beta in np.linspace(0.5,1.6,221):
        mm=sum(1 for q in qs if int(math.floor(alpha*q+beta))!=B[q])
        if best is None or mm<best[0]: best=(mm,alpha,beta)
mm,al,be=best
print(f"\n===== Beatty fit B(q)=floor({al:.4f} q + {be:.3f}): mismatches {mm}/{len(qs)} =====")
print("  Beatty-mismatch q:", [q for q in qs if int(math.floor(al*q+be))!=B[q]])

# jump structure (three-distance test)
jumps=[q for q in qs if q-1 in B and B[q]>B[q-1]]
gaps=[jumps[i+1]-jumps[i] for i in range(len(jumps)-1)]
print("\n===== B(q) jump points & gaps (three-distance signature) =====")
print("jumps:", jumps)
print("gap multiset:", dict(sorted(Counter(gaps).items())), "(<=3 distinct values => three-distance)")

# slope estimate
sl=np.polyfit(qs[-40:],[B[q] for q in qs[-40:]],1)[0]
print(f"\nempirical slope (last 40): {sl:.4f}   W/pi at q={qs[-1]}: {WQP[qs[-1]]/qs[-1]:.4f}")

# R2 (task stated) density
R2=[q for q in qs if B[q]>P2[q]]
print(f"\n===== R2 = {{B>2+floor((q-1)/6)}}: {len(R2)}/{len(qs)} (density {len(R2)/len(qs):.2f}); D2 max {max(B[q]-P2[q] for q in qs)} =====")
print("  R2 head:", R2[:15], "...")

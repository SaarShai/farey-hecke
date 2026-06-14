"""
Analyze the resonance number theory once B(q), P1, P2 are loaded from the sweep files.
Reads 'D8 q B wqp P1 P2' lines.
Searches for arithmetic structure in:
  R1 = {q: B>P1}  (continuous-arc / lattice-vs-notch resonance, the deep one)
  R2 = {q: B>P2}  (vs 2+floor((q-1)/6), the task's stated set)
Also analyzes B(q) jump structure and the fractional-part {0.216 q}.
"""
import math, sys, glob
from sympy import isprime, continued_fraction_iterator, Rational, primerange

rows={}
for fn in sys.argv[1:]:
    with open(fn) as f:
        for line in f:
            if not line.startswith("D8 "): continue
            _,q,B,wqp,P1,P2=line.split()
            rows[int(q)]=(int(B),float(wqp),int(P1),int(P2))

qs=sorted(rows)
print(f"loaded q={qs[0]}..{qs[-1]}  ({len(qs)} values)")

B={q:rows[q][0] for q in qs}
P1={q:rows[q][2] for q in qs}
P2={q:rows[q][3] for q in qs}

R1=[q for q in qs if B[q]>P1[q]]
R1neg=[q for q in qs if B[q]<P1[q]]
R2=[q for q in qs if B[q]>P2[q]]
print("\n=== R1 = {q: B(q) > floor(Wq/pi)+1}  (lattice-vs-notch resonance) ===")
print("R1 =", R1)
print("B<P1 (anti) =", R1neg)
print("\n=== R2 = {q: B(q) > 2+floor((q-1)/6)} (task stated set) ===")
print("R2 =", R2)

# B(q) jump points: q where B(q) > B(q-1)
jumps=[q for q in qs if q-1 in B and B[q]>B[q-1]]
print("\n=== B(q) jump points (B increments) ===")
print("jumps =", jumps)
gaps=[jumps[i+1]-jumps[i] for i in range(len(jumps)-1)]
print("gaps between jumps =", gaps)

def analyze_set(name, S):
    print(f"\n##### arithmetic analysis of {name} ({len(S)} elts) #####")
    if not S: return
    print(" set:", S)
    # residues mod n
    for n in range(2,13):
        from collections import Counter
        c=Counter(q%n for q in S)
        # which residues present / absent
        present=sorted(c)
        allres=set(range(n))
        absent=sorted(allres-set(present))
        # is it concentrated?
        print(f"  mod {n:2d}: residues present {present}  (absent {absent})  counts={dict(sorted(c.items()))}")
    # primality
    np_=sum(1 for q in S if isprime(q)); print(f"  primes in set: {np_}/{len(S)}  -> {[q for q in S if isprime(q)]}")
    # consecutive runs
    runs=[]; cur=[S[0]]
    for q in S[1:]:
        if q==cur[-1]+1: cur.append(q)
        else: runs.append(cur); cur=[q]
    runs.append(cur)
    print(f"  consecutive runs: {[ (r[0],r[-1]) if len(r)>1 else r[0] for r in runs]}")

analyze_set("R1", R1)
analyze_set("R2", R2)

# CF of 2/pi and of Winf/pi
print("\n=== continued fractions of key constants ===")
import mpmath as mp
mp.mp.dps=40
for name,x in [("2/pi", 2/mp.pi), ("pi/2",mp.pi/2), ("Winf/pi~0.216", mp.mpf("0.216"))]:
    cf=[];
    it=mp.mpf(x)
    for _ in range(15):
        a=int(mp.floor(it)); cf.append(a);
        fr=it-a
        if fr<mp.mpf("1e-30"): break
        it=1/fr
    print(f"  {name}: CF = {cf}")

# The deviation D2 = B - P2 (grows ~0.05q). Print to see slope.
print("\n=== deviation D2(q)=B-P2 (should grow ~0.05q, NOT sparse) ===")
D2=[(q,B[q]-P2[q]) for q in qs]
print("  D2 sample:", [d for (_,d) in D2][::10], "...")
print(f"  D2 range: {min(d for _,d in D2)}..{max(d for _,d in D2)}")

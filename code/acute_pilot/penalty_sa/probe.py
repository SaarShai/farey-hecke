import re
txt=open('../a089676_witnesses.txt').read()
parts=re.split(r'a\((\d+)\)\s*>=\s*(\d+):', txt)
W={}
for i in range(1,len(parts),3):
    nn=int(parts[i]); rows=re.findall(r'\(([01\s]+)\)', parts[i+2]); masks=[]
    for r in rows:
        bits=[c for c in r if c in '01']; v=0
        for j,c in enumerate(bits):
            if c=='1': v|=(1<<j)
        masks.append(v)
    W[nn]=masks

def energy(S):  # unordered (apex; legpair) violations
    m=len(S); e=0
    for j in range(m):
        q=S[j]
        for a in range(m):
            if a==j: continue
            xa=S[a]^q
            for b in range(a+1,m):
                if b==j: continue
                if (xa&(S[b]^q))==0: e+=1
    return e

R=W[13]; full=1<<13; Rset=set(R)
def added(v):
    e=0
    for a in range(len(R)):
        xa=R[a]^v
        for b in range(a+1,len(R)):
            if (xa&(R[b]^v))==0: e+=1
    for j in range(len(R)):
        q=R[j]; xv=v^q
        for b in range(len(R)):
            if b==j: continue
            if (xv&(R[b]^q))==0: e+=1
    return e
v=min((added(x),x) for x in range(full) if x not in Rset)[1]
S0=R+[v]
E0=energy(S0)
print("base E (R+best v) =",E0)
# Exhaustive 1-vertex change: for each position, try all 2^13 values, record best total energy
best=E0; bestmove=None
for idx in range(len(S0)):
    orig=S0[idx]
    for nv in range(full):
        if nv==orig: continue
        if nv in set(S0)-{orig}: continue
        S0[idx]=nv
        e=energy(S0)
        if e<best:
            best=e; bestmove=(idx,nv)
    S0[idx]=orig
print("best after ONE exhaustive single-vertex change:",best,"move",bestmove)

import sys
sys.path.insert(0,'/Users/za/Documents/farey-hecke/code/acute_pilot/exact_cp')
from core import is_acute_masks

def exact_max(n):
    V=list(range(1<<n))
    best=[0,None]
    def dfs(S,start):
        if len(S)>best[0]:
            best[0]=len(S); best[1]=list(S)
        # prune: remaining can't beat
        for i in range(start,len(V)):
            v=V[i]
            ok=True
            # incremental acute check: only need to check triples involving v
            if is_acute_masks(S+[v]):
                dfs(S+[v],i+1)
    dfs([],0)
    return best
for n in range(1,6):
    b=exact_max(n)
    print(f"n={n}: max={b[0]}  set={b[1]}")

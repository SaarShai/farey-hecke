#!/usr/bin/env python3
"""
Independent witness checker. Given (n,k) and a JSON dict of vertex coordinates,
recompute the straight-line crossing count from scratch (no trust in the search code).
Usage: python3 check_witness.py n k '{"0":[x,y],...}'
Prints the crossing count and lists every crossing pair, so a third party can verify.
"""
import sys, json, itertools

def pnk(n,k):
    V=list(range(n)); E=[(a,b) for a in V for b in V if a<b and b-a<=k]; return V,E

def properly_cross(p1,p2,p3,p4):
    def o(a,b,c):
        return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    d1=o(p3,p4,p1); d2=o(p3,p4,p2); d3=o(p1,p2,p3); d4=o(p1,p2,p4)
    eps=1e-9
    if abs(d1)<eps or abs(d2)<eps or abs(d3)<eps or abs(d4)<eps:
        return False  # degenerate; witness should be generic
    return (d1>0)!=(d2>0) and (d3>0)!=(d4>0)

def main():
    n=int(sys.argv[1]); k=int(sys.argv[2]); coords=json.loads(sys.argv[3])
    V,E=pnk(n,k)
    pos={int(v):tuple(coords[v]) for v in coords}
    crs=[]
    for e,f in itertools.combinations(E,2):
        if set(e)&set(f): continue
        if properly_cross(pos[e[0]],pos[e[1]],pos[f[0]],pos[f[1]]):
            crs.append((e,f))
    print(f"P_{n}^{k}: {len(crs)} crossings (independent recompute)")
    for e,f in crs: print("  ",e,"x",f)

if __name__=="__main__": main()

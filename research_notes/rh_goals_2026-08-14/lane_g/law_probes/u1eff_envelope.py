"""u1eff_envelope.py -- test the ENVELOPE half of the entry-wise hypothesis.

The hypothesis is  |M_q - M_inf|[block][m,k] <= C q^{-alpha} r^{m+k}, r<1.
u1eff_fit establishes alpha ~ 2.  This script reads u1eff_entries.json and, per
block, fits the geometric ratio r of the ENTRY DIFFERENCE in the Taylor index
sum m+k (using the successive difference at the largest available q as the
proxy for |M_q - M_inf|).  r >= 1 for any block kills the envelope.
"""
import json, math, os
HERE=os.path.dirname(os.path.abspath(__file__))
D=json.load(open(os.path.join(HERE,"u1eff_entries.json")))
qs=sorted(int(q) for q in D["points"]["s1"])
out={}
for pt,rows in D["points"].items():
    qa,qb=qs[-2],qs[-1]
    blocks={}
    for k in rows[str(qa)]["right_entries"]:
        blk,idx=k.split("|"); m,kk=[int(x) for x in idx.split(",")]
        va=complex(*rows[str(qa)]["right_entries"][k])
        vb=complex(*rows[str(qb)]["right_entries"][k])
        blocks.setdefault(blk,{})[m+kk]=abs(vb-va)
    res={}
    for blk,dd in blocks.items():
        pts=[(t,v) for t,v in sorted(dd.items()) if v>0]
        if len(pts)<3: continue
        n=len(pts); sx=sum(p[0] for p in pts); sy=sum(math.log(p[1]) for p in pts)
        sxx=sum(p[0]**2 for p in pts); sxy=sum(p[0]*math.log(p[1]) for p in pts)
        slope=(n*sxy-sx*sy)/(n*sxx-sx*sx)
        res[blk]={"r":math.exp(slope),"diffs":{str(t):v for t,v in pts}}
    out[pt]=res
    print("POINT",pt,f" (successive diff q={qa}->{qb})")
    for blk,v in sorted(res.items()):
        flag="  <== ENVELOPE FAILS (r>=0.9)" if v["r"]>=0.9 else ""
        print(f"   block {blk:8s} r = {v['r']:.4f}{flag}")
json.dump(out,open(os.path.join(HERE,"u1eff_envelope.json"),"w"),indent=1)

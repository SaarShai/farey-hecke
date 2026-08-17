"""u1eff_dconv.py -- is the q-trend in u1eff_det a real trend or an N-truncation artefact?

Re-evaluates det(1 - L_{s,+}) at large q with a LARGER per-component
truncation d, so the q-trend measured at d=12 can be separated from the
dimension tail.  Also reports det(1-K_s) (MMS denominator) so the trend can be
read on the Selberg zeta rather than on the raw numerator.

Read-only probe; writes only its own JSON next to itself.
"""
import json, math, os, sys, time
sys.path.insert(0,"/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code")
from flint import acb, ctx
import zeta_cert_rosen as RO
ctx.prec=300
N=int(os.environ.get("NN","20"))
QS=[int(x) for x in (os.environ.get("QS") or "41,81").split(",")]
out=[]
for name,sr,si in [("s1",0.25,7.0674)]:
    s=acb(sr,si)
    for q in QS:
        t0=time.time(); M,k=RO.build_reduced_matrix_ball(s,N,+1,q,n_head=4)
        rec={"pt":name,"q":q,"kappa":k,"N":N,"build_s":round(time.time()-t0,1),"d":{}}
        for d in [8,12,16,N]:
            if d>N: continue
            t1=time.time(); z=RO._det_block(M,N,k,d)
            v=complex(float(z.real.mid()),float(z.imag.mid()))
            rec["d"][str(d)]={"dim":k*d,"re":v.real,"im":v.imag,"abs":abs(v),"sec":round(time.time()-t1,1)}
            print(name,q,"d",d,"dim",k*d,f"|det|={abs(v):.8g}",f"({time.time()-t1:.0f}s)",flush=True)
        bk=RO.det_K(q,acb(sr,si)); bv=complex(float(bk.real.mid()),float(bk.imag.mid()))
        rec["det_K"]={"re":bv.real,"im":bv.imag,"abs":abs(bv)}
        print("   det_K",q,abs(bv),flush=True)
        out.append(rec)
json.dump(out,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"u1eff_dconv.json"),"w"),indent=1)
print("done")

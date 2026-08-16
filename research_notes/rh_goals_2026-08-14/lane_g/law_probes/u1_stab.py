import sys, time, math, cmath, json
from pathlib import Path
REPO = Path("/Users/za/Documents/farey-hecke")
sys.path.insert(0, str(REPO/".worktrees/aletheia-restore/code"))
import zeta_cert_rosen_even as E
from flint import acb, arb, ctx
ctx.prec = 400
S_INF = complex(0.25, 7.0673625708673465)
bd = [S_INF + 0.25*cmath.exp(2j*math.pi*j/8) for j in range(8)]
out=[]
for q in (30,):
    for j in (2,3,4,5):
        s = bd[j]
        row={"q":q,"j":j,"re":s.real,"im":s.imag}
        for N in (32,48,64):
            t=time.time(); vals={}
            for sg in (1,-1):
                v=E.cert_det_complex_mid(acb(arb(s.real),arb(s.imag)),N,sg,q,n_head=4)
                vals[sg]=abs(complex(float(v.real),float(v.imag)))
            row[f"N{N}"]=[vals[1],vals[-1],vals[1]*vals[-1]]
            print(f"q={q} dU_{j} s={s.real:.6f}{s.imag:+.6f}i N={N}  |+|={vals[1]:.8e} |-|={vals[-1]:.8e} prod={vals[1]*vals[-1]:.8e}  t={time.time()-t:.0f}s", flush=True)
        out.append(row)
json.dump(out, open("u1_stab.json","w"), indent=1)

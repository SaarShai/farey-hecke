#!/usr/bin/env python3
"""5-variable phi-form certificate -> Lean case lemma with NATURAL interface (c,d,e as
variables + recurrence), so g5_core dispatches by a clean `exact`.
Generators on (a,b,c,d,e); cert = pairwise products (reduced) + recurrence*monomial (free).
Emit: derive 0<= generators, product `have`s (linear_combination M*hps), recurrence-monomial
`have`s (linear_combination), final linarith."""
import sympy as sp, numpy as np, sys
from itertools import combinations_with_replacement
from scipy.optimize import linprog
phi,a,b,c,d,e=sp.symbols('phi a b c d e'); V=[a,b,c,d,e]
def redp(expr):
    p=sp.Poly(sp.expand(expr),phi); r=sp.Integer(0); fib={0:(0,1),1:(1,0)}
    def f(k):
        if k in fib: return fib[k]
        x,y=f(k-1); fib[k]=(x+y,x); return fib[k]
    for (k,),co in p.terms(): cp,c1=f(k); r+=co*(cp*phi+c1)
    return sp.expand(r)
def monos(expr):
    expr=redp(expr); p=sp.Poly(expr,phi)
    parts={0:p.coeff_monomial(1),1:p.coeff_monomial(phi)}; out={}
    for w,part in parts.items():
        if sp.expand(part)==0: continue
        for mono,co in sp.Poly(sp.expand(part),*V).terms():
            out.setdefault(mono,[sp.Integer(0),sp.Integer(0)]); out[mono][w]+=co
    return out
def base(K):
    K0,K1,K2=K
    return [('ha','a',a),('hbp','b',b),('hc','c',c),('hd','d',d),('he2','e',e),
       ('ca','ca',1-a),('cb','cb',1-b),('cc','cc',1-c),('cdc','cd',1-d),('ce','ce',1-e),
       ('rab','reg_ab',a+phi*b-1),('rbc','reg_bc',b+phi*c-1),('rcd','reg_cd',c+phi*d-1),('rde','reg_de',d+phi*e-1),
       ('gab','gen_ab',phi*a+b-1),('gbc','gen_bc',phi*b+c-1),('gcd','gen_cd',phi*c+d-1),('gde','gen_de',phi*d+e-1),
       ('hf0','f0',(K0+1)*phi*b-1-a),('hf1','f1',(K1+1)*phi*c-1-b),('hf2','f2',(K2+1)*phi*d-1-c),
       ('hs0','s0',1-a*b*(2*phi+1)),('hs1','s1',1-b*c*(2*phi+1)),('hs2','s2',1-c*d*(2*phi+1)),('hs3','s3',1-d*e*(2*phi+1))]
def eqs(K):
    K0,K1,K2=K
    return [('r0',a+c-K0*phi*b),('r1',b+d-K1*phi*c),('r2',c+e-K2*phi*d)]
def cert(K):
    B=base(K); E=eqs(K)
    terms=[]
    for i,j in combinations_with_replacement(range(len(B)),2):
        ex=redp(B[i][2]*B[j][2])
        terms.append((('P',i,j),ex))
        terms.append((('Pp',i,j),redp(phi*ex)))
    nNon=len(terms)
    monosE=[sp.Integer(1)]+V
    free=[(('E',en,str(m)),redp(ee*m)) for en,ee in E for m in monosE]
    free+=[(('Ep',en,str(m)),redp(phi*ee*m)) for en,ee in E for m in monosE]
    allt=terms+free
    sp_=[monos(ex) for _,ex in allt]
    mset=set()
    for s in sp_:
        for mm in s: mset.add(mm)
    ml=sorted(mset); mi={m:i for i,m in enumerate(ml)}; M=len(ml)
    const=(0,0,0,0,0); A=sp.zeros(2*M,len(allt))
    for k,s in enumerate(sp_):
        for mm,(c1,cp) in s.items(): A[2*mi[mm],k]=c1; A[2*mi[mm]+1,k]=cp
    nc=[i for i in range(2*M) if i//2!=mi[const]]
    ns=A[nc,:].nullspace()
    if not ns: return None
    Nb=sp.Matrix.hstack(*ns); dim=Nb.shape[1]
    cr0=A[2*mi[const],:]; cr1=A[2*mi[const]+1,:]
    PHIN=(1+sp.sqrt(5))/2
    cfun=[((cr0+PHIN*cr1)*Nb)[k] for k in range(dim)]
    Lf=np.array(Nb.tolist(),dtype=float); cf=np.array([float(x) for x in cfun]); nT=len(allt)
    # sparsify over nonneg (first nNon); free vars unconstrained
    Aub=np.vstack([-Lf[:nNon],cf.reshape(1,-1)]); bub=np.concatenate([np.zeros(nNon),[-1.0]])
    res=linprog(c=Lf[:nNon].sum(axis=0),A_ub=Aub,b_ub=bub,bounds=[(None,None)]*dim,method='highs')
    if not res.success: return ('fail',)
    x=Lf@res.x
    usedP=[(terms[k][0],terms[k][1]) for k in range(nNon) if x[k]>1e-7]
    usedF=[allt[k][0] for k in range(nNon,len(allt)) if abs(x[k])>1e-7]
    return ('ok',usedP,B,E,usedF)
def lx(ex): return str(sp.expand(ex)).replace('**','^')
def emit(K,name):
    r=cert(K)
    if r is None or r[0]=='fail': return None
    _,usedP,B,E,usedF=r; K0,K1,K2=K
    usedFset=set(usedF)
    Bexpr={n:x for n,l,x in B}; Bord=[(n,x) for n,l,x in B]
    L=[]
    L.append(f"lemma {name} (a b c d e phi : ℝ) (hps : phi^2 = phi+1) (h2 : (1:ℝ) < phi) (h3 : phi < 2)")
    L.append("    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d) (he2 : 0 < e)")
    L.append("    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1) (he1 : e ≤ 1)")
    L.append("    (hab : a+phi*b > 1) (hbc : b+phi*c > 1) (hcd : c+phi*d > 1) (hde : d+phi*e > 1)")
    L.append("    (hab' : phi*a+b > 1) (hbc' : phi*b+c > 1) (hcd' : phi*c+d > 1) (hde' : phi*d+e > 1)")
    L.append(f"    (hk0 : a+c = {K0}*phi*b) (hk1 : b+d = {K1}*phi*c) (hk2 : c+e = {K2}*phi*d)")
    L.append(f"    (hk0f : 1+a < ({K0}+1)*(phi*b)) (hk1f : 1+b < ({K1}+1)*(phi*c)) (hk2f : 1+c < ({K2}+1)*(phi*d))")
    L.append("    (hP0 : a*b < 1/phi^3) (hP1 : b*c < 1/phi^3) (hP2 : c*d < 1/phi^3) (hP3 : d*e < 1/phi^3) :")
    L.append("    False := by")
    L.append("  have hpos : (0:ℝ) < phi := by linarith")
    L.append("  have hcube : phi^3 = 2*phi+1 := by nlinarith [hps]")
    L.append("  have hp3 : (0:ℝ) < phi^3 := by positivity")
    # derive 0<= generators (lx forms, ordering-robust nlinarith)
    Bexpr2={n:x for n,l,x in base(K)}
    gsrc={'gab':'hab',"gbc":'hbc','gcd':'hcd','gde':'hde','rab':'hab',
          'rbc':'hbc','rcd':'hcd','rde':'hde','ca':'ha1','cb':'hb1','cc':'hc1','cdc':'hd1','ce':'he1',
          'hf0':'hk0f','hf1':'hk1f','hf2':'hk2f'}
    # edges: gen_xy uses primed (phi*x+y), reg_xy uses unprimed (x+phi*y). map correctly:
    gsrc={'gab':"hab'","gbc":"hbc'",'gcd':"hcd'",'gde':"hde'",'rab':'hab',
          'rbc':'hbc','rcd':'hcd','rde':'hde','ca':'ha1','cb':'hb1','cc':'hc1','cdc':'hd1','ce':'he1',
          'hf0':'hk0f','hf1':'hk1f','hf2':'hk2f'}
    for nm in ['gab','gbc','gcd','gde','rab','rbc','rcd','rde','ca','cb','cc','cdc','ce','hf0','hf1','hf2']:
        L.append(f"  have {nm} : (0:ℝ) ≤ {lx(Bexpr2[nm])} := by nlinarith [{gsrc[nm]}]")
    # slacks
    slk={'hs0':('hP0','a*b'),'hs1':('hP1','b*c'),'hs2':('hP2','c*d'),'hs3':('hP3','d*e')}
    for sn,(pn,co) in slk.items():
        rhs=lx(sp.expand(sp.sympify(co)*(2*phi+1)))
        L.append(f"  have {sn} : (0:ℝ) ≤ {lx(Bexpr2[sn])} := by")
        L.append(f"    have hh : {co}*phi^3 < 1 := (lt_div_iff₀ hp3).mp {pn}")
        L.append(f"    have he : {co}*phi^3 = {rhs} := by rw [hcube]; ring")
        L.append(f"    linarith [hh, he]")
    strict={'ha','hbp','hc','hd','he2'}
    def t(h): return f"{h}.le" if h in strict else h
    names=[]
    for n,((kind,i,j),red) in enumerate(usedP):
        nm=f"q{n}"; names.append(nm)
        ei=Bord[i][1]; ej=Bord[j][1]; eis=lx(ei); ejs=lx(ej)
        hi=Bord[i][0]; hj=Bord[j][0]
        if kind=='P':
            raw=sp.expand(ei*ej); rawstr=f"({eis})*({ejs})"; mnt=f"mul_nonneg {t(hi)} {t(hj)}"
        else:
            raw=sp.expand(phi*ei*ej); rawstr=f"phi*(({eis})*({ejs}))"; mnt=f"mul_nonneg hpos.le (mul_nonneg {t(hi)} {t(hj)})"
        Mc=sp.expand(sp.cancel((raw-red)/(phi**2-phi-1)))
        L.append(f"  have {nm} : (0:ℝ) ≤ {lx(red)} := by")
        L.append(f"    have hr : (0:ℝ) ≤ {rawstr} := {mnt}")
        L.append(f"    have he : {rawstr} = {lx(red)} := by linear_combination ({lx(Mc)})*hps")
        L.append(f"    linarith [hr, he]")
    # recurrence-monomial equalities (and phi-scaled), reduced
    hkname={'r0':'hk0','r1':'hk1','r2':'hk2'}
    enames=[]
    cnt=0
    for en,ee in E:
        for m in [sp.Integer(1),a,b,c,d,e]:
            for scal,sname,tag in [(sp.Integer(1),'1','E'),(phi,'phi','Ep')]:
                if (tag,en,str(m)) not in usedFset: continue
                raw=sp.expand(scal*ee*m); red=redp(raw)
                Mc=sp.expand(sp.cancel((red-raw)/(phi**2-phi-1))) if sp.expand(raw-red)!=0 else sp.Integer(0)
                nm=f"E{cnt}"; cnt+=1; enames.append(nm)
                mstr=('' if m==1 else lx(m)+'*') + sname
                if Mc==0:
                    L.append(f"  have {nm} : {lx(red)} = 0 := by linear_combination ({mstr})*{hkname[en]}")
                else:
                    L.append(f"  have {nm} : {lx(red)} = 0 := by linear_combination ({mstr})*{hkname[en]} + ({lx(Mc)})*hps")
    L.append(f"  linarith [{', '.join(names+enames)}, h2, h3]")
    return "\n".join(L)
if __name__=='__main__':
    K=tuple(int(x) for x in sys.argv[1].split(',')); print(emit(K,sys.argv[2]) or "FAILED")

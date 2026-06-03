#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GOAL H — CRUX TEST: is the observed sustained word W_q=[(q-1,3),(q-1,0),(q-3,0)]
a periodic orbit whose min-esssup < 1/lam^3 ?  (would REFUTE X_Omega=1/lam^3 for q>=16)
or = 1/lam^3 (second realization of the infimum, consistent)?

Uses the genuine-map matrix machinery (same as Bgoal_genuine_hunt): word=list of (i,k),
monodromy product of M_{i,k}, eigen-family s*v_n; esssup over the scale family is
s^2 * max_n Phat_n, minimized at s->s_lo (lower edge of the feasible scale window).
Also: exhaustive search WITH digit up to 4 over branches near the top {q-4..q-1},
periods up to 6, to see if ANY word beats 1/lam^3.
"""
import itertools, math
import numpy as np

def lam(q): return 2*math.cos(math.pi/q)
def ellipse_vecs(q,l):
    U=np.array([[l,-1.0],[1.0,0.0]]); w=[np.array([1.0,0.0])]
    for _ in range(q+3): w.append(U@w[-1])
    return w
def Mik(i,k,w,l):
    xi,yi=w[i]; xi1,yi1=w[i+1]
    return np.array([[xi,yi],[xi1+k*l*xi,yi1+k*l*yi]])
def eig1_vector(M):
    A=M-np.eye(2); _,sv,Vt=np.linalg.svd(A)
    if sv[-1]>1e-7: return None
    v=Vt[-1]
    if v[0]<0: v=-v
    return v
def word_family(word,w,l):
    p=len(word); M=np.eye(2)
    for (i,k) in word: M=Mik(i,k,w,l)@M
    tr=np.trace(M)
    if abs(tr-2.0)>1e-6: return None,tr
    v0=eig1_vector(M)
    if v0 is None: return None,tr
    vs=[v0]
    for (i,k) in word[:-1]: vs.append(Mik(i,k,w,l)@vs[-1])
    vp=Mik(word[-1][0],word[-1][1],w,l)@vs[-1]
    if np.linalg.norm(vp-v0)>1e-6*(1+np.linalg.norm(v0)): return None,tr
    if any(v[0]<=1e-9 for v in vs): return None,tr
    return vs,tr
def feasible_window(word,vs,w,q,l):
    p=len(word); s_lo=0.0; s_hi=math.inf; EPS=1e-12
    for n in range(p):
        vx,vy=vs[n]; i,k=word[n]
        s_hi=min(s_hi,1.0/vx)
        if vy>EPS: s_hi=min(s_hi,1.0/vy)
        edge=vy+l*vx
        if edge>EPS: s_lo=max(s_lo,1.0/edge)
        dprev=vx*w[i-1][0]+vy*w[i-1][1]; dcur=vx*w[i][0]+vy*w[i][1]
        if dprev>EPS: s_lo=max(s_lo,1.0/dprev)
        if dcur>EPS: s_hi=min(s_hi,1.0/dcur)
        else: return None
        A=dcur; B=vx*w[i+1][0]+vy*w[i+1][1]
        up=B+k*l*A
        if up>EPS: s_hi=min(s_hi,1.0/up)
        lo=B+(k+1)*l*A
        if lo>EPS: s_lo=max(s_lo,1.0/lo)
    if s_lo>=s_hi-1e-14: return None
    return s_lo,s_hi
def Phat(vn,i,w):
    ti=vn[0]*w[i][0]+vn[1]*w[i][1]
    return vn[0]*ti/w[i][1]

def test_word(q,word):
    l=lam(q); w=ellipse_vecs(q,l); thr=1/l**3
    vs,tr=word_family(word,w,l)
    if vs is None:
        return f"  q={q} {word}: NOT a valid parabolic family (trace={tr:.5f})"
    win=feasible_window(word,vs,w,q,l)
    if win is None:
        return f"  q={q} {word}: parabolic (tr={tr:.4f}) but EMPTY scale window"
    s_lo,s_hi=win
    mph=max(Phat(vs[n],word[n][0],w) for n in range(len(word)))
    Xc=s_lo*s_lo*mph
    # per-step P at s_lo
    Ps=[s_lo*s_lo*Phat(vs[n],word[n][0],w) for n in range(len(word))]
    return (f"  q={q} {word}: tr={tr:.5f} s in ({s_lo:.5f},{s_hi:.5f}] "
            f"min-esssup={Xc:.6f}  thr={thr:.6f}  ratio={Xc/thr:.5f} "
            f"{'<<< BELOW thr!!' if Xc<thr-1e-7 else '(>=thr OK)'}\n"
            f"        per-step P at s_lo = {[round(p,5) for p in Ps]}")

print("=== TEST the observed sustained word W_q=[(q-1,3),(q-1,0),(q-3,0)] ===")
for q in [16,20,30,50]:
    W=[(q-1,3),(q-1,0),(q-3,0)]
    print(test_word(q,W))
print()
print("=== also the cusp word [(q-2,0)] (known: realizes 1/lam^3) ===")
for q in [16,20,30]:
    print(test_word(q,[(q-2,0)]))

print("\n=== exhaustive: ANY word over top branches {q-4..q-1}, digit<=4, period<=5, beats thr? ===")
for q in [16,20,30]:
    l=lam(q); w=ellipse_vecs(q,l); thr=1/l**3
    branches=[q-4,q-3,q-2,q-1]
    alphabet=[(i,k) for i in branches for k in range(0,5)]
    best=None; seen=set()
    def canon(wd):
        return min(tuple(wd[j:]+wd[:j]) for j in range(len(wd)))
    cnt=0
    for p in range(1,6):
        for word in itertools.product(alphabet,repeat=p):
            c=canon(list(word))
            if c in seen: continue
            seen.add(c); cnt+=1
            vs,tr=word_family(list(c),w,l)
            if vs is None: continue
            win=feasible_window(list(c),vs,w,q,l)
            if win is None: continue
            s_lo,s_hi=win
            mph=max(Phat(vs[n],c[n][0],w) for n in range(len(c)))
            Xc=s_lo*s_lo*mph
            if best is None or Xc<best[0]-1e-12:
                best=(Xc,list(c),s_lo,s_hi)
    print(f"  q={q}: searched {cnt} words; best min-esssup={best[0]:.6f} thr={thr:.6f} "
          f"ratio={best[0]/thr:.5f} word={best[1]} {'<<<BELOW' if best[0]<thr-1e-7 else 'OK'}")

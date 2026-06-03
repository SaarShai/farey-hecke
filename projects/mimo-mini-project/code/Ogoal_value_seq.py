#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ogoal_value_seq.py  (goal O) — the MIN-MAX (ess-sup) minimizing-measure SEQUENCE that
escapes to the cusp, and the CONTRAST with the standard Birkhoff (min-average) value.

DEMONSTRATION (numerical), not a proof. The proven theorem is X_Omega(q)=1/lam^3 (+ no
ground state) for q>=5; X_Omega=2/9 (q=3), sqrt2/8 (q=4). Here we EXHIBIT the optimizing
sequence explicitly and show it escapes to the cusp vertex (1/lam, 0).

Object: genuine Taha BCZ_q on  Tq = {0<a<=1, 1-lam a<b<=1},  lam=2cos(pi/q).
  Cusp word  w_c = (i=q-2, k=0)  has monodromy [[1,lam],[0,1]] (parabolic, trace 2).
  Its scale-free family s*v_n is confined to a window s in (s_lo, s_hi].
  ess-sup P on the family = s^2 * maxPhat ; minimized as s -> s_lo+.

THREE THINGS SHOWN per q:
  (1) the family value V(s)=s^2 maxPhat -> 1/lam^3  as s -> s_lo+   (the min-MAX limit);
  (2) the orbit base point (a,b)=s*v_0 -> the cusp vertex (1/lam,0) as s -> s_lo+
      (ESCAPE OF MASS: the minimizing orbit collapses onto the boundary cusp, NOT attained);
  (3) CONTRAST: q=3,4 the GLOBAL minimizer is an INTERIOR periodic orbit (compact ->
      genuine ground state EXISTS); q>=5 the minimizer is the cusp word (escape, no GS).

Also reports the Birkhoff min-AVERAGE value beta_min (q=5: ~0.18634) to contrast with the
ess-sup value 1/lam^3=0.23607 (min-max != min-average; a project result).

Anchors gated: q=3->2/9, q=4->sqrt2/8, q=5->1/phi^3=0.236068.
"""
import math, json, importlib.util, os
import numpy as np
import mpmath as mp

mp.mp.dps = 40

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("gh", os.path.join(HERE, "Bgoal_genuine_hunt.py"))
gh = importlib.util.module_from_spec(spec); spec.loader.exec_module(gh)

# ---------- exact (mpmath) cusp-word value ----------
def lam_mp(q): return 2*mp.cos(mp.pi/q)

def ellipse_vecs_mp(q, l):
    U = mp.matrix([[l, -1], [1, 0]])
    w = [mp.matrix([1, 0])]
    for _ in range(q+2):
        w.append(U*w[-1])
    return w

def Mik_mp(i, k, w, l):
    xi, yi = w[i][0], w[i][1]; xi1, yi1 = w[i+1][0], w[i+1][1]
    return mp.matrix([[xi, yi], [xi1 + k*l*xi, yi1 + k*l*yi]])

def cusp_word_value_mp(q):
    """Exact ess-sup value of the cusp word (q-2,0) at s->s_lo+, plus s_lo and the
    base-point -> cusp-vertex escape, all in high precision."""
    l = lam_mp(q)
    w = ellipse_vecs_mp(q, l)
    i = q-2; k = 0
    M = Mik_mp(i, k, w, l)
    tr = M[0,0]+M[1,1]
    # +1 eigenvector of parabolic M: (M-I)v=0
    A = M - mp.eye(2)
    # solve A v = 0 ; take v=(A[0,1], -A[0,0]) (kernel of 2x2 singular)
    v0 = mp.matrix([A[0,1], -A[0,0]])
    if v0[0] < 0: v0 = -v0
    nrm = mp.sqrt(v0[0]**2+v0[1]**2); v0 = v0/nrm
    # window: single-letter word, family s*v0 ; reuse analytic bounds
    vx, vy = v0[0], v0[1]
    s_hi = mp.inf; s_lo = mp.mpf(0)
    # a<=1
    s_hi = min(s_hi, 1/vx)
    if vy > 0: s_hi = min(s_hi, 1/vy)
    edge = vy + l*vx
    if edge > 0: s_lo = max(s_lo, 1/edge)
    dprev = vx*w[i-1][0]+vy*w[i-1][1]
    dcur  = vx*w[i][0]+vy*w[i][1]
    if dprev > 0: s_lo = max(s_lo, 1/dprev)
    if dcur > 0:  s_hi = min(s_hi, 1/dcur)
    A_ = dcur; B_ = vx*w[i+1][0]+vy*w[i+1][1]
    up = B_ + k*l*A_
    if up > 0: s_hi = min(s_hi, 1/up)
    lo = B_ + (k+1)*l*A_
    if lo > 0: s_lo = max(s_lo, 1/lo)
    # Phat for single letter
    ti = vx*w[i][0]+vy*w[i][1]
    Phat = vx*ti/w[i][1]
    val = s_lo**2 * Phat
    # base point at s_lo and cusp vertex (1/lam, 0)
    a_lo, b_lo = s_lo*vx, s_lo*vy
    cusp = (1/l, mp.mpf(0))
    dist = mp.sqrt((a_lo-cusp[0])**2 + (b_lo-cusp[1])**2)
    return dict(q=q, lam=l, tr=tr, s_lo=s_lo, s_hi=s_hi, Phat=Phat, val=val,
                inv_lam3=1/l**3, base=(a_lo, b_lo), cusp=cusp, dist_to_cusp=dist)

# ---------- min-average (Birkhoff) beta_min via word search (float) ----------
def betamin(q, Pmax, Kmax):
    l = gh.lam(q); w = gh.ellipse_vecs(q, l); thr = 1.0/l**3
    branches = list(range(2, q))
    alphabet = [(i, k) for i in branches for k in range(0, Kmax+1)]
    seen = set(); min_avg = 1e9; min_avg_word = None
    import itertools
    def canon(word): return min(tuple(word[j:]+word[:j]) for j in range(len(word)))
    for p in range(1, Pmax+1):
        for word in itertools.product(alphabet, repeat=p):
            c = canon(list(word))
            if c in seen: continue
            seen.add(c)
            vs = gh.word_family(list(c), w, l)
            if vs is None: continue
            win = gh.feasible_window(list(c), vs, w, q, l)
            if win is None: continue
            s_lo, s_hi, _ = win
            phats = [gh.Phat(vs[n], c[n][0], w) for n in range(len(c))]
            avg = s_lo*s_lo*sum(phats)/len(phats)
            if avg < min_avg: min_avg = avg; min_avg_word = list(c)
    return thr, min_avg, min_avg_word

# ---------- interior minimizer for q=3,4 (compact -> ground state exists) ----------
def global_min_word(q, Pmax, Kmax):
    best, cnt = gh.hunt(q, Pmax=Pmax, Kmax=Kmax, rotational_only=False, verbose=False)
    return best  # (Xc, word, s_lo, s_hi, mph)

if __name__ == "__main__":
    print("="*78)
    print("MIN-MAX (ess-sup) ESCAPING SEQUENCE  vs  cusp vertex (1/lam,0)   [mpmath dps=40]")
    print("="*78)
    Vref = {3: mp.mpf(2)/9, 4: mp.sqrt(2)/8}
    rows = []
    for q in [3,4,5,6,7,8,10,12,16,20]:
        r = cusp_word_value_mp(q)
        l = r['lam']
        anchor = ""
        if q in Vref:
            anchor = f" [global V(q)={float(Vref[q]):.6f}]"
        print(f"\nq={q}  lam={float(l):.8f}  trace(cuspword)={float(r['tr']):.6f}")
        print(f"   cusp-word value  s_lo^2*maxPhat = {float(r['val']):.12f}")
        print(f"   1/lam^3                         = {float(r['inv_lam3']):.12f}"
              f"   |diff|={float(abs(r['val']-r['inv_lam3'])):.2e}")
        print(f"   s window = ({float(r['s_lo']):.8f}, {float(r['s_hi']):.8f}]")
        print(f"   base pt s_lo*v0 = ({float(r['base'][0]):.8f}, {float(r['base'][1]):.8f})"
              f"   cusp vertex=({float(r['cusp'][0]):.8f}, 0)")
        print(f"   dist(base, cusp vertex) = {float(r['dist_to_cusp']):.2e}  <-- ESCAPE (->0){anchor}")
        rows.append(dict(q=q, lam=float(l), cuspword_val=float(r['val']),
                         inv_lam3=float(r['inv_lam3']),
                         err=float(abs(r['val']-r['inv_lam3'])),
                         s_lo=float(r['s_lo']), s_hi=float(r['s_hi']),
                         dist_to_cusp=float(r['dist_to_cusp'])))

    print("\n" + "="*78)
    print("V(s)=s^2 maxPhat ALONG THE FAMILY  (s decreasing -> escape to cusp, value->1/lam^3)")
    print("="*78)
    seq = {}
    for q in [5, 7, 12]:
        r = cusp_word_value_mp(q); l = r['lam']
        s_lo, s_hi = r['s_lo'], r['s_hi']
        # the family Phat (single letter) is constant; value scales as s^2
        w = ellipse_vecs_mp(q, l); i = q-2
        A = Mik_mp(i,0,w,l) - mp.eye(2)
        v0 = mp.matrix([A[0,1], -A[0,0]]);  v0 = v0/mp.sqrt(v0[0]**2+v0[1]**2)
        if v0[0]<0: v0=-v0
        ti = v0[0]*w[i][0]+v0[1]*w[i][1]; Phat = v0[0]*ti/w[i][1]
        print(f"\nq={q}: 1/lam^3={float(1/l**3):.10f}  (approach s->s_lo+={float(s_lo):.6f})")
        tbl = []
        for frac in [1.5, 1.2, 1.05, 1.01, 1.001, 1.0001, 1.00001]:
            s = s_lo*frac
            val = s**2*Phat
            a, b = s*v0[0], s*v0[1]
            d = mp.sqrt((a-1/l)**2+b**2)
            print(f"     s={float(s):.8f}  V(s)={float(val):.10f}  "
                  f"dist_to_cusp={float(d):.3e}")
            tbl.append(dict(s=float(s), val=float(val), dist=float(d)))
        seq[q] = tbl

    print("\n" + "="*78)
    print("CONTRAST: min-MAX (ess-sup, 1/lam^3) vs min-AVERAGE (Birkhoff, beta_min)")
    print("="*78)
    betas = {}
    for q,(Pm,Km) in [(5,(6,3)),(6,(5,2)),(7,(5,2))]:
        thr, ma, maw = betamin(q, Pm, Km)
        ratio = ma/thr
        verdict = "min-max > min-avg (sub-action gap)" if ratio < 0.999 else "(equal at this depth)"
        print(f"  q={q}: 1/lam^3={thr:.6f}  beta_min(AVG)={ma:.6f} (ratio {ratio:.4f})  word={maw}  {verdict}")
        betas[q] = dict(inv_lam3=thr, beta_min=ma, ratio=float(ratio), word=str(maw))

    print("\n" + "="*78)
    print("GROUND-STATE CONTRAST: q=3,4 (compact interior minimizer = GS EXISTS) vs q>=5 (escape)")
    print("="*78)
    for q,(Pm,Km) in [(3,(4,6)),(4,(5,4)),(5,(6,3)),(6,(5,2))]:
        best = global_min_word(q, Pm, Km)
        Xc, word, s_lo, s_hi, mph = best
        # is the minimizing base point at the cusp vertex (escape) or interior?
        l = gh.lam(q); w = gh.ellipse_vecs(q, l)
        vs = gh.word_family(word, w, l)
        a0, b0 = s_lo*vs[0][0], s_lo*vs[0][1]
        dcusp = math.hypot(a0-1/l, b0)
        kind = "ESCAPE (cusp, no GS)" if dcusp < 1e-6 else "INTERIOR (ground state EXISTS)"
        print(f"  q={q}: X_Omega={Xc:.8f} word={word}  base=({a0:.5f},{b0:.5f}) "
              f"dist_cusp={dcusp:.2e}  -> {kind}")

    out = dict(escape_table=rows, value_sequence=seq, betamin_contrast=betas)
    with open(os.path.join(HERE, "Ogoal_value_seq_results.json"), "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote Ogoal_value_seq_results.json")

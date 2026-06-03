#!/usr/bin/env python3
"""
q=5 (Hecke G5, lam=phi) 4-window pre-check for the Lean lemma `g5_core`.

Goal C numeric pre-check. Confirms BEFORE Lean:
  (1) optimizer family c_n = R*sin((n+1)*pi/5) gives 4-window max -> 1/4+ as R->R_lo,
      and cluster (longest run of products < 1/4) is exactly 3 (so 4-window bound holds).
  (2) DIRECT constrained feasibility of the g5_core hypotheses: is there ANY
      (a,b,c,d,e>0) with floors k0,k1,k2>=1 (floor-consistent), region a+phi*b>1 etc.,
      and ALL FOUR products ab,bc,cd,de < 1/4 ? If none -> the window bound is true.
      Also reports, per floor-triple, the achievable min over windows of max(4 products),
      i.e. how tight 1/4 is and which floor pattern binds.

No external deps beyond mpmath/numpy/scipy if present; falls back to pure-python grid.
"""
import math

phi = (1 + math.sqrt(5)) / 2          # lam_5 = 2cos(pi/5)
assert abs(phi*phi - (phi+1)) < 1e-12  # phi^2 = phi+1
T = 0.25                               # threshold V(5) = 1/4

# ---------------------------------------------------------------------------
# (1) Optimizer family  c_n = R * sin((n+1)*pi/5),  period q-2 = 3 word (1,1,2)
# ---------------------------------------------------------------------------
def optimizer_check():
    print("="*72)
    print("(1) OPTIMIZER FAMILY  c_n = R*sin((n+1)*pi/5)   word (1,1,2), period 3")
    print("="*72)
    s = [math.sin((n+1)*math.pi/5) for n in range(3)]   # sin36, sin72, sin108=sin72
    # the eigen-orbit cycles through R*{sin36, sin72, sin72} (n=0,1,2 then repeats)
    vbase = [math.sin(math.pi/5), math.sin(2*math.pi/5), math.sin(3*math.pi/5)]
    print("  v = sin{36,72,108} deg =", [round(x,6) for x in vbase])
    # products of the periodic orbit v_n*v_{n+1} (indices mod 3)
    def orbit_v(n):  # period-3 pattern of sin values, but recurrence has the '2' defect
        return vbase[n % 3]
    # build a long orbit by the actual recurrence to get the real product sequence
    # c_0=v0,c_1=v1; floors word repeats (1,1,2): k_n known. Use scale R.
    def build(R, N=60):
        c = [R*vbase[0], R*vbase[1]]
        floors = [1,1,2]
        for n in range(N):
            k = floors[n % 3]
            c.append(k*phi*c[n+1] - c[n])
        return c
    # find R_lo: smallest R with all region constraints c_n+phi c_{n+1}>1 satisfied
    def region_ok(R):
        c = build(R, 30)
        return all(c[n] + phi*c[n+1] > 1 - 1e-12 for n in range(28)) and all(x>1e-12 for x in c)
    # binary search R_lo (region binds from below: larger R => bigger coords => region easier)
    lo, hi = 0.0, 5.0
    for _ in range(200):
        mid = (lo+hi)/2
        if region_ok(mid): hi = mid
        else: lo = mid
    R_lo = hi
    print("  R_lo (region binding, open) ~= %.10f" % R_lo)
    for R in [R_lo*1.0001, R_lo*1.01, R_lo*1.1, R_lo*1.5]:
        c = build(R, 60)
        P = [c[n]*c[n+1] for n in range(58)]
        # 4-window max over windows (skip first few transients = none, it's exact periodic)
        wins = [max(P[i:i+4]) for i in range(len(P)-3)]
        maxprod = max(P[10:50]); minwin = min(wins[10:50])
        # cluster: longest run of consecutive products < T
        run=best=0
        for p in P[10:50]:
            run = run+1 if p < T-1e-12 else 0
            best=max(best,run)
        print("  R=%.6f (R/R_lo=%.4f): max P=%.8f  min(4-win max)=%.8f  cluster=%d"
              % (R, R/R_lo, maxprod, minwin, best))
    print("  -> expect min(4-window max) -> 0.25+ as R->R_lo, cluster=3 (4-win HOLDS).")

# ---------------------------------------------------------------------------
# (2) DIRECT feasibility of g5_core hypotheses (the Lean lemma itself)
# ---------------------------------------------------------------------------
def floor_consistent(x, y, k):
    """k == floor((1+x)/(phi*y)) ?  i.e.  k <= (1+x)/(phi*y) < k+1."""
    val = (1+x)/(phi*y)
    return k <= val + 1e-12 and val < k+1 - 1e-12

def core_search(Kmax=5, grid=400):
    print("="*72)
    print("(2) DIRECT g5_core feasibility:  exists a,b,c,d,e>0, floors k0,k1,k2>=1,")
    print("    region (4 ineqs), floor-consistent, ALL FOUR products < 1/4 ?")
    print("="*72)
    # free params (b,c); a=k0*phi*b - c, d=k1*phi*c - b, e=k2*phi*d - c
    any_feasible = False
    summary = []
    # grid for b,c in (0, 0.7] (since b^2,c^2 < 1/(2phi)~0.309 => b,c<0.556)
    bs = [0.7*(i+1)/grid for i in range(grid)]
    for k0 in range(1, Kmax+1):
        for k1 in range(1, Kmax+1):
            for k2 in range(1, Kmax+1):
                best_maxprod = math.inf
                best_cfg = None
                feas_all_below = False
                for b in bs:
                    for c in bs:
                        a = k0*phi*b - c
                        d = k1*phi*c - b
                        e = k2*phi*d - c
                        if a<=1e-9 or b<=1e-9 or c<=1e-9 or d<=1e-9 or e<=1e-9: continue
                        # region
                        if not (a+phi*b>1 and b+phi*c>1 and c+phi*d>1 and d+phi*e>1): continue
                        # floor consistency for the three recurrences
                        if not floor_consistent(a,b,k0): continue
                        if not floor_consistent(b,c,k1): continue
                        if not floor_consistent(c,d,k2): continue
                        P = [a*b, b*c, c*d, d*e]
                        mp = max(P)
                        if mp < best_maxprod:
                            best_maxprod = mp; best_cfg=(a,b,c,d,e)
                        if mp < T - 1e-9:
                            feas_all_below = True
                if best_cfg is not None:
                    summary.append((k0,k1,k2,best_maxprod,feas_all_below))
                    if feas_all_below:
                        any_feasible = True
                        print("  !! ALL-BELOW FEASIBLE at floors (%d,%d,%d): maxP=%.6f cfg=%s"
                              % (k0,k1,k2,best_maxprod, tuple(round(x,4) for x in best_cfg)))
    print("\n  Per floor-triple: min over (b,c) grid of max(4 products) "
          "[only triples with a nonempty floor-consistent region]:")
    summary.sort(key=lambda r: r[3])
    for k0,k1,k2,mp,fb in summary[:25]:
        flag = "  <-- ALL 4 BELOW 1/4 (BOUND VIOLATED)" if fb else ""
        print("    (%d,%d,%d): min max(4P) = %.6f%s" % (k0,k1,k2,mp,flag))
    print()
    if any_feasible:
        print("  RESULT: window bound APPEARS FALSE on the grid (found 4-below config). "
              "INVESTIGATE before Lean.")
    else:
        print("  RESULT: NO floor-consistent config has all 4 products < 1/4 on the grid.")
        print("          => g5_core 4-window bound is NUMERICALLY CONFIRMED.")
        # report the global min over all triples (tightest = binding pattern)
        gm = min(summary, key=lambda r:r[3])
        print("          Tightest floor pattern: (%d,%d,%d) with min max(4P)=%.6f (-> 0.25)"
              % (gm[0],gm[1],gm[2],gm[3]))
    return summary

if __name__ == "__main__":
    optimizer_check()
    print()
    core_search(Kmax=5, grid=500)

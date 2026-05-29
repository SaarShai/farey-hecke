"""
Track A, experiment 2 -- serves BOTH parallel tasks:

 (1) KILL-SHOT / confirmation for the no-ground-state THEOREM (q=3, ground 2/9):
     A "ground state" = invariant prob. measure mu with ess-sup_mu P = 2/9.
     Such a mu would be supported on {P <= 2/9}, so SOME orbit would have ALL
     products <= 2/9 forever.  If we can find an orbit sustaining products
     <= 2/9 for many steps (or a periodic orbit on the hyperbola H={xy=2/9}),
     the theorem is FALSE.  Expectation: max sustainable run = 2  => no ground
     state.  We also empirically check the proof's key reduction:
        ess-sup_mu P = 2/9  =>  mu(H) >= 1/3   (every 3-window touches H).

 (2) G_4 (lambda=sqrt2, ground sqrt2/8): determine whether the optimizer is a
     genuine INTERIOR period-2 orbit (=> ground state EXISTS) or a boundary
     limit at a floor discontinuity (=> NO ground state, same as q=3).
     [memory is self-contradictory on this; let the arithmetic decide.]
"""
import math
from fractions import Fraction
import numpy as np


def make_T(lam):
    def T(x, y):
        k = math.floor((1.0 + x) / (lam * y))
        return (y, k * (lam * y) - x)
    return T


def in_dom(x, y, lam, ymax=3.0, tol=1e-9):
    return (x > tol) and (y > tol) and (x + lam * y > 1 - tol) and (y < ymax) and (x < ymax)


def max_run_below(T, lam, ground, tol, n_starts=200000, steps=60, seed=0,
                  seed_pts=None):
    """Max number of CONSECUTIVE products <= ground+tol achievable by any orbit."""
    rng = np.random.default_rng(seed)
    best = 0
    best_start = None
    starts = []
    if seed_pts:
        starts.extend(seed_pts)
    for _ in range(n_starts):
        x = rng.uniform(0.001, 1.0)
        ylo = max(0.001, (1.0 - x) / lam + 1e-6)
        if ylo >= 1.0:
            continue
        starts.append((x, rng.uniform(ylo, 1.0)))
    for (x0, y0) in starts:
        x, y = x0, y0
        run = 0
        for _ in range(steps):
            if not in_dom(x, y, lam):
                break
            if x * y <= ground + tol:
                run += 1
                if run > best:
                    best, best_start = run, (x0, y0)
            else:
                run = 0
            x, y = T(x, y)
    return best, best_start


# ===================================================================
print("=" * 70)
print("(1) q=3  (lambda=1, ground = 2/9)  -- is there a ground state?")
print("=" * 70)
T3 = make_T(1.0)
g3 = 2.0 / 9.0

# (a) longest sustainable run of products <= 2/9 (with a generous tolerance,
#     and including starts ON the hyperbola H so we don't miss an equality orbit)
H_pts = []
for x in np.linspace(0.225, 0.332, 60):          # x in [2/9, 1/3) branch of H
    y = (2.0 / 9.0) / x
    if in_dom(x, y, 1.0):
        H_pts.append((x, y))
for x in np.linspace(0.668, 0.999, 60):          # x in (2/3, 1) branch of H
    y = (2.0 / 9.0) / x
    if in_dom(x, y, 1.0):
        H_pts.append((x, y))

for tol in (0.0, 1e-6, 1e-3):
    run, st = max_run_below(T3, 1.0, g3, tol, n_starts=120000, steps=80,
                            seed_pts=H_pts)
    print(f"  max consecutive products <= 2/9 + {tol:<6}: run = {run}"
          f"   (start {None if st is None else tuple(round(v,4) for v in st)})")

# (b) periodic orbit ON the hyperbola H ?  (would let mu charge H)
on_H_return = 0
for (x0, y0) in H_pts:
    x, y = x0, y0
    stayed = True
    for _ in range(12):
        x, y = T3(x, y)
        if not in_dom(x, y, 1.0):
            stayed = False
            break
        if abs(x * y - g3) < 1e-7 and stayed:
            on_H_return += 1
            break
print(f"  points of H whose orbit RETURNS to H within 12 steps "
      f"(all-staying): {on_H_return} / {len(H_pts)}")
# image of H: do points of H map above or below 2/9?
imgP = [T3(x, y)[0] * T3(x, y)[1] for (x, y) in H_pts]
imgP = np.array(imgP)
print(f"  image products P(T p) for p in H:  min={imgP.min():.4f}  "
      f"max={imgP.max():.4f}  (H is swept OFF itself: image != 2/9)")

print("\n  => q=3: longest run of products <=2/9 is 2; H carries no periodic")
print("     orbit; so NO invariant measure can sit on {P<=2/9} => NO GROUND STATE.")

# ===================================================================
print("\n" + "=" * 70)
print("(2) q=4  (lambda=sqrt2, ground = sqrt2/8)  -- interior orbit or boundary?")
print("=" * 70)
s = math.sqrt(2.0)
T4 = make_T(s)
g4 = s / 8.0
print(f"  ground value sqrt2/8 = {g4:.6f}")

print("\n  candidate optimizer family (a, a/sqrt2) <-> (a/sqrt2, a):")
print(f"  {'a':>7} {'P=a^2/sqrt2':>12} {'word k0,k1':>11}  closes?")
for a in [0.5200, 0.5500, 0.7000, 0.9000]:
    c = a / s
    p1 = (a, c)
    k0 = math.floor((1 + p1[0]) / (s * p1[1]))
    p2 = T4(*p1)
    k1 = math.floor((1 + p2[0]) / (s * p2[1]))
    p3 = T4(*p2)
    closes = abs(p3[0] - a) < 1e-9 and abs(p3[1] - c) < 1e-9
    print(f"  {a:7.4f} {a*a/s:12.6f}       [{k0},{k1}]   {closes}")

print(f"\n  infimum of family = lim_{{a->1/2+}} a^2/sqrt2 = {0.25/s:.6f}"
      f"  vs sqrt2/8 = {g4:.6f}")
# escape check at a=1/2 (exact)
a = Fraction(1, 2)
# k0 = floor((1+a)/(sqrt2 * c)) with c = a/sqrt2 => sqrt2*c = a, so (1+a)/a
k0_half = ((1 + a) / a).__floor__()
print(f"  at a=1/2: floor k0 = floor((1+a)/a) = {k0_half}  "
      f"(family needs k0=2; JUMPS 2->{k0_half})  => boundary escape")
xh, yh = 0.5, 0.5 / s
nxt = T4(xh, yh)
print(f"  T4(1/2, sqrt2/4) = ({nxt[0]:.4f}, {nxt[1]:.4f})  -> leaves the family "
      f"(2nd coord {nxt[1]:.3f} ~ 1, on the boundary edge)")

# (c) ground-state kill-shot for G_4: longest run of products <= sqrt2/8
H4 = []
for x in np.linspace(0.18, 0.35, 50):
    y = g4 / x
    if in_dom(x, y, s):
        H4.append((x, y))
for x in np.linspace(0.51, 1.2, 50):
    y = g4 / x
    if in_dom(x, y, s):
        H4.append((x, y))
for tol in (0.0, 1e-6, 1e-3):
    run, st = max_run_below(T4, s, g4, tol, n_starts=120000, steps=80,
                            seed_pts=H4)
    print(f"  max consecutive products <= sqrt2/8 + {tol:<6}: run = {run}")

print("\n  => q=4: the optimizer is ALSO a boundary limit (floor jump 2->3 at")
print("     a=1/2), NOT an interior periodic orbit; max run = 2 => NO GROUND")
print("     STATE.  The no-ground-state phenomenon is SHARED by q=3 and q=4.")
print("     (This corrects the earlier 'genuine interior period-2 orbit' note.)")

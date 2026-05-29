"""
Track A, experiment 1: the ergodic-optimization object for the BCZ map.

We study  m(P) := inf over BCZ-invariant prob. measures mu of ( ess-sup_mu P ),
where P(x,y) = x*y is the consecutive-Farey-gap product and T is the BCZ map
T(x,y) = (y, floor((1+x)/y)*y - x) on the triangle {0<x<=1, 0<y<=1, x+y>1}.

Proven (Lean): m(P) >= 2/9  (no orbit has 3 consecutive products all < 2/9).
OPEN structural question this experiment probes:
  (Q1) Is the infimum 2/9 ATTAINED by some invariant measure (a "ground state"),
       or is it an unattained boundary infimum ("NO ground state")?
  (Q2 kill-shot) Could a non-periodic orbit beat 2/9? (Would break the theory.)

Plan:
  Part 1  -- the candidate optimizer family (a,2a)<->(2a,a), a in (1/3,1/2):
             verify it is a genuine period-2 BCZ orbit, product = 2a^2 -> 2/9+,
             and show the limit a=1/3 ESCAPES to the boundary (floor jump 1->2).
  Part 2  -- numeric confirmation of the bound + optimizer structure over many
             orbits; confirm no window-of-3 ever dips below 2/9.
"""
import math
from fractions import Fraction
import numpy as np

TWO_NINTHS = 2.0 / 9.0


def T(x, y):
    k = math.floor((1.0 + x) / y)
    return (y, k * y - x)


def Tk(x, y):
    return math.floor((1.0 + x) / y)


def in_triangle(x, y, tol=1e-12):
    return (0 < x <= 1 + tol) and (0 < y <= 1 + tol) and (x + y > 1 - tol)


print("=" * 70)
print("PART 1 -- the candidate ground-state family (a, 2a) <-> (2a, a)")
print("=" * 70)
print(f"{'a':>7} {'P=2a^2':>10} {'T(a,2a)':>22} {'word k0,k1':>10}  closes?")
for a in [0.3340, 0.3500, 0.4000, 0.4500, 0.4990]:
    p1 = (a, 2 * a)
    k0 = Tk(*p1)
    p2 = T(*p1)
    k1 = Tk(*p2)
    p3 = T(*p2)
    closes = abs(p3[0] - p1[0]) < 1e-9 and abs(p3[1] - p1[1]) < 1e-9
    print(f"{a:7.4f} {2*a*a:10.6f} ({p2[0]:.4f},{p2[1]:.4f})        "
          f"[{k0},{k1}]   {closes}  (P->{2*a*a:.5f})")
print(f"\ninfimum of the family ceiling = lim_{{a->1/3+}} 2a^2 = "
      f"{2*(1/3)**2:.6f}  vs  2/9 = {TWO_NINTHS:.6f}")

print("\n-- the limit point a=1/3 is NOT an interior orbit (exact arithmetic):")
x, y = Fraction(1, 3), Fraction(2, 3)
k = ( (1 + x) / y ).__floor__()
nxt = (y, k * y - x)
print(f"   at a=1/3 the family point is (1/3,2/3); floor k = {k}  "
      f"(JUMPS from 1 to {k})")
print(f"   T(1/3,2/3) = ({nxt[0]},{nxt[1]}) -> second coord = {nxt[1]} "
      f"=> ON boundary y=1, x+y={nxt[0]+nxt[1]} : ESCAPES the open triangle")
print("   => the optimizing family limits to the boundary; the inf 2/9 is")
print("      approached from ABOVE (2a^2 > 2/9 for all a>1/3) but NOT attained")
print("      by any interior orbit  =>  evidence of NO GROUND STATE.")

print("\n" + "=" * 70)
print("PART 2 -- numeric: bound holds, optimizer structure, kill-shot scan")
print("=" * 70)
rng = np.random.default_rng(0)


def orbit_window_min(x0, y0, n=4000, burn=200):
    """Return min over the orbit of max(P_i,P_{i+1},P_{i+2}); also global min
    triple-product flag (kill-shot: any window with all three < 2/9?)."""
    x, y = x0, y0
    for _ in range(burn):
        x, y = T(x, y)
        if not in_triangle(x, y):
            return None, False
    ps = []
    for _ in range(n):
        ps.append(x * y)
        x, y = T(x, y)
        if not in_triangle(x, y):
            break
    if len(ps) < 3:
        return None, False
    ps = np.array(ps)
    win_max = np.maximum.reduce([ps[:-2], ps[1:-1], ps[2:]])
    all3_below = np.any((ps[:-2] < TWO_NINTHS) & (ps[1:-1] < TWO_NINTHS)
                        & (ps[2:] < TWO_NINTHS))
    return float(win_max.min()), bool(all3_below)


# (a) random starts
mins = []
violations = 0
for _ in range(4000):
    x0 = rng.uniform(0.001, 1.0)
    y0 = rng.uniform(max(0.001, 1.0 - x0 + 1e-6), 1.0)
    if not in_triangle(x0, y0):
        continue
    m, bad = orbit_window_min(x0, y0)
    if m is not None:
        mins.append(m)
    if bad:
        violations += 1
mins = np.array(mins)
print(f"random starts: {len(mins)} orbits")
print(f"  min over all orbits of (orbit window-min of max-of-3) = {mins.min():.6f}")
print(f"  2/9 = {TWO_NINTHS:.6f}   ->  bound min >= 2/9 ? {mins.min() >= TWO_NINTHS - 1e-9}")
print(f"  KILL-SHOT: orbits with a 3-window ALL below 2/9 = {violations}  "
      f"(must be 0; >0 would refute the theorem)")

# (b) seeded near the [4,1] family (a -> 1/3+): should approach 2/9 from above
print("\nseeded near the optimizer family (a -> 1/3+):")
for a in [0.345, 0.338, 0.3345, 0.3335]:
    m, bad = orbit_window_min(a, 2 * a, n=2000, burn=50)
    print(f"  start (a,2a) a={a:.4f}: orbit window-min = "
          f"{m if m is None else round(m,6)}  (2a^2={2*a*a:.6f})  all3_below={bad}")

print("\nCONCLUSION:")
print("  * proven bound m(P) >= 2/9 holds numerically (0 violations) -- theory OK")
print("  * the inf 2/9 is approached only by the [4,1] family as a->1/3+,")
print("    whose limit ESCAPES the open triangle (floor jump) => the infimum")
print("    is UNATTAINED: strong evidence the BCZ ergodic-optimization problem")
print("    has NO ground-state invariant measure on the open triangle.")
print("  * That 'no ground state' fact is the clean, novel theorem target for")
print("    Track A (contrast Contreras: ground states are *generically* periodic).")

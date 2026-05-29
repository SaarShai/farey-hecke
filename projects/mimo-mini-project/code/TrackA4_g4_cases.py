"""
Track A, experiment 4 -- can the q=3 no-ground-state PROOF transfer to G_4?

q=3 proof worked because on H={xy=2/9} the region x+y>1 EXCLUDES the interval
y in (1/3,2/3): every 2/9-point has y<1/3 (=> x>2/3, backward kills) or y>2/3
(forward kills).  CLEAN dichotomy, no middle.

G_4: H_4={xy=s/8}, region x + s*y > 1 (s=sqrt2).  Check whether the analogous
two cases (y>1/2 forward, x>1/2 backward) cover ALL t-points, or leave a MIDDLE.

Forward identity (floor=k): P(T4(x,y)) = k*s*y^2 - s/8.  With k>=1 (forced by
orbit positivity), this is > t=s/8  iff  k*y^2 > 1/4.
  * y>1/2  => y^2>1/4 => works for any k>=1.
  * y in (s/4,1/2], k>=2 => k*y^2 >= 2*(s/4)^2 = 1/4 (>1/4 for y>s/4) => works.
  * y in (s/4,1/2], k=1 => y^2<=1/4 => P_next <= t => NO forward contradiction.
At a t-point the forward floor is k=floor(4x(1+x)) (since s*y=1/(4x) on H_4).
"""
import math
import numpy as np

s = math.sqrt(2.0)
t = s / 8.0

def g4(x, y):
    k = math.floor((1.0 + x) / (s * y))
    return (y, k * (s * y) - x), k

# sample t-points on H_4 inside g4Triangle (x+ s y >1, x,y>0)
ys = np.linspace(0.20, 1.2, 20000)
pts = []
for y in ys:
    x = t / y
    if x > 0 and y > 0 and x + s * y > 1 + 1e-12:
        pts.append((x, y))

caseA = caseB = middle = 0
mids = []
for (x, y) in pts:
    fwd_ok = y > 0.5 + 1e-12                       # forward kills (any k>=1)
    bwd_ok = x > 0.5 + 1e-12                       # backward kills (predecessor y=x>1/2)
    # also forward kills if floor k>=2 and y>s/4:
    _, k = g4(x, y)
    fwd_k2 = (k >= 2) and (y > s/4 + 1e-12)
    if fwd_ok or fwd_k2:
        caseA += 1
    elif bwd_ok:
        caseB += 1
    else:
        middle += 1
        mids.append((x, y, k))

print(f"t-points sampled on H_4: {len(pts)}")
print(f"  covered by FORWARD (y>1/2 or [k>=2 & y>s/4]): {caseA}")
print(f"  covered by BACKWARD (x>1/2):                  {caseB}")
print(f"  MIDDLE (neither simple case works):           {middle}")
if mids:
    xs_ = [m[0] for m in mids]; ys_ = [m[1] for m in mids]; ks_ = [m[2] for m in mids]
    print(f"  middle x-range: [{min(xs_):.4f},{max(xs_):.4f}]  "
          f"y-range: [{min(ys_):.4f},{max(ys_):.4f}]  floors: {sorted(set(ks_))}")
    # confirm: middle points have forward floor 1 and P_next <= t (no forward kill)
    bad = 0
    for (x, y, k) in mids:
        (u, v), kf = g4(x, y)
        Pnext = u * v
        if not (kf == 1 and Pnext <= t + 1e-12):
            bad += 1
    print(f"  middle pts with forward k=1 & P_next<=t (no fwd kill): "
          f"{len(mids)-bad}/{len(mids)}")

# But is the THEOREM still true? longest run of products <= t over many orbits.
def in_dom(x, y):
    return x > 1e-9 and y > 1e-9 and x + s*y > 1 - 1e-9 and y < 5 and x < 5
rng = np.random.default_rng(2)
best = 0
for _ in range(120000):
    x = rng.uniform(0.001, 1.2); y = rng.uniform(0.001, 1.2)
    if not in_dom(x, y):
        continue
    run = 0
    for _ in range(120):
        if not in_dom(x, y):
            break
        if x * y <= t + 1e-12:
            run += 1; best = max(best, run)
        else:
            run = 0
        (x, y), _ = g4(x, y)
print(f"\nlongest run of products <= s/8 over orbits: {best}  "
      f"(theorem G=empty still TRUE if bounded)")
print("\nVERDICT:", "two-case proof TRANSFERS (no middle)" if middle == 0
      else "MIDDLE CASE EXISTS -> q=3 proof does NOT mechanically transfer to G_4")

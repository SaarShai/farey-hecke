"""
Track A, exp 5 -- close the G_4 middle case (the part q=3's proof doesn't cover).

The middle t-points (xy=t=s/8, both coords in [s/4,1/2]) split by forward floor
k = floor(4x(1+x)):
  * k>=2 (y in (s/4, ~0.483]): P_{m+1} = k*s*y^2 - t >= 2*s*y^2 - t > s/4 - t = t. KILLED forward (1 step).
  * k=1  (y in (~0.483, 1/2]): P_{m+1} = s*y^2 - t <= t  (no 1-step kill).
        For these we go 2 steps: claim the floor at m+1 is exactly 3 and P_{m+2} > t.
We verify the full case partition kills EVERY t-point, and pin the m+1 floor.
"""
import math
import numpy as np

s = math.sqrt(2.0)
t = s / 8.0

def g4(x, y):
    k = math.floor((1.0 + x) / (s * y))
    return (y, k * (s * y) - x), k

ys = np.linspace(0.20, 1.3, 40000)
H = [(t / y, y) for y in ys if (t / y) > 0 and (t / y) + s * y > 1 + 1e-12]

n_fwd1 = n_bwd1 = n_mid = 0
mid_floor_at_m1 = set()
mid_bad = 0          # middle points where 2-step does NOT give P_{m+2} > t
for (x, y) in H:
    (_, _), k = g4(x, y)
    if y > 0.5:                                   # forward 1-step (any k>=1): P_{m+1}=k s y^2 - t > t
        n_fwd1 += 1
    elif x > 0.5:                                 # backward 1-step: P_m = k' s x^2 - P_{m-1} > t
        n_bwd1 += 1
    elif k >= 2:                                  # forward 1-step via k>=2 & y>s/4
        n_fwd1 += 1
    else:
        # MIDDLE, k=1: go two steps forward
        n_mid += 1
        pt1, _ = g4(x, y)                         # pt1 = (y, s*y - x)
        pt2, k1 = g4(*pt1)
        P2 = pt2[0] * pt2[1]
        mid_floor_at_m1.add(k1)
        if not (P2 > t + 1e-12):
            mid_bad += 1

print(f"t-points sampled: {len(H)}")
print(f"  forward 1-step (y>1/2 or k>=2): {n_fwd1}")
print(f"  backward 1-step (x>1/2):        {n_bwd1}")
print(f"  MIDDLE (k=1, both coords<=1/2): {n_mid}")
print(f"    floor at step m+1 for middle pts: {sorted(mid_floor_at_m1)}  (claim: {{3}})")
print(f"    middle pts where P_{{m+2}} > t FAILS: {mid_bad}  (must be 0)")

# also pin: for middle, is P_{m+2} = 3 s a^2 - (s y^2 - t) with a = s y - x, and > t ?
# closed check of the inequality 3 s (s y - x)^2 - (s y^2 - t) > t on the middle range
viol = 0
for (x, y) in H:
    if not (x <= 0.5 and y <= 0.5):
        continue
    (_, _), k = g4(x, y)
    if k != 1:
        continue
    a = s * y - x
    lhs = 3 * s * a * a - (s * y * y - t)   # predicted P_{m+2} with floor 3
    if not (lhs > t + 1e-12):
        viol += 1
print(f"  closed-form middle check  3 s (sy-x)^2 - (s y^2 - t) > t : violations = {viol}")

print("\nVERDICT:", "COMPLETE -- every t-point killed (fwd-1 / bwd-1 / mid-2step)"
      if mid_bad == 0 and viol == 0 else "INCOMPLETE -- middle not closed")

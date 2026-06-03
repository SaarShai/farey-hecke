#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
q5_tpoint_trace.py — trace forward orbits from q=5 t-points (P=1/4) across the band y in [a,b],
x=1/(4y). At each t-point forward floor MUST be 1 (proven: floor2 gives P>0.4>1/4). Continue the
orbit; record how many steps until P_n>1/4, and the floor sequence. Goal: find the exact finite case
structure for the q=5 lower-bound proof (which step exceeds, under which floor).
"""
import mpmath as mp
mp.mp.dps = 40
phi = (1+mp.sqrt(5))/2          # = lam(5)
l = phi
V = mp.mpf(1)/4
b = mp.sqrt(1/(2*l))            # band top = sqrt(1/(2phi))
a = 1/(4*b)                     # band bottom, a*b=1/4

def in_D(x,y): return x>0 and y>0 and (x+l*y)>1
def step(x,y):
    k = int(mp.floor((1+x)/(l*y)))
    return k*l*y - x, k

print(f"phi={mp.nstr(phi,10)} band a={mp.nstr(a,8)} b={mp.nstr(b,8)} (a*b={mp.nstr(a*b,6)})")
print("Trace forward from t-point (x=1/(4y), y); stop when P>1/4 (success) or leave D (FAIL=sustains).")
print(f"{'y':>9} {'x':>9} {'steps_to_>V':>11} {'floors':>16} {'maxP/V_seen':>11} {'inD?':>5}")

N = 41
sustain_fail = 0
maxsteps_needed = 0
for i in range(N+1):
    y = a + (b-a)*mp.mpf(i)/N
    x = 1/(4*y)
    if not in_D(x,y):
        print(f"{mp.nstr(y,7):>9} {mp.nstr(x,7):>9}  t-point not in D"); continue
    floors=[]; maxr=mp.mpf(0); steps=None; left=False
    cx,cy=x,y
    for s in range(1,60):
        yn,k = step(cx,cy)
        floors.append(k)
        if yn<=0 or not in_D(cy,yn):
            left=True; break
        P = cy*yn
        if P/V>maxr: maxr=P/V
        if P > V*(1+mp.mpf('1e-25')):
            steps=s; break
        cx,cy=cy,yn
    fl=''.join(str(f) for f in floors[:8])
    tag = '' if steps else '  <-- SUSTAINS/leaves'
    if steps is None: sustain_fail+=1
    else: maxsteps_needed=max(maxsteps_needed,steps)
    print(f"{mp.nstr(y,7):>9} {mp.nstr(x,7):>9} {str(steps):>11} {fl:>16} {mp.nstr(maxr,6):>11} {str(in_D(x,y)):>5}{tag}")

print(f"\nmax steps to exceed V from any t-point = {maxsteps_needed}; #sustain/leave-without-exceeding = {sustain_fail}")

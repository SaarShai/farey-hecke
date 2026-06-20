"""
q=11 GENUINE realization witness (corrected), dps=60.

B(11)=3 (genuine ground truth, k-pattern [1,1,2]).  This script verifies the CORRECT
length-3 (N=2) cluster witness used in the Lean realization, and documents the rejection
of an earlier invalid length-4 candidate.

KEY CORRECTNESS CHECK (this is what distinguishes B(11)=3 from an over-count):
a genuine cluster point must lie in the BCZ cross-section domain
    0 < a <= 1   AND   1 - lam*a < b <= 1   AND   b > 0,
and the cluster START's predecessor (under M^{-1}) must NOT be on the last branch.

The earlier candidate start (19/61, 22/61) FAILS the domain condition (b=0.3607 < 1-lam*a=0.4023)
and its M-orbit leaves the cross-section -> it is a transient, giving a spurious length-4 run.
The correct start (34/101, 37/101) is a genuine valid-domain cluster start.
"""
import mpmath as mp
mp.mp.dps = 60

q = 11
lam = 2*mp.cos(mp.pi/q); t = 1/lam**3

def M(p): a,b = p; return (b, -a + lam*b)
def Minv(p): a,b = p; return (lam*a - b, a)
def valid(p): a,b = p; return (0 < a <= 1) and (1 - lam*a < b <= 1) and (b > 0)
def kfloor(p): a,b = p; return int(mp.floor((1+a)/(lam*b)))

print(f"q={q}  lam=2cos(pi/11)={mp.nstr(lam,30)}  t=1/lam^3={mp.nstr(t,30)}")
print(f"minpoly residual lam^5-lam^4-4lam^3+3lam^2+3lam-1 = "
      f"{mp.nstr(lam**5-lam**4-4*lam**3+3*lam**2+3*lam-1,6)}")
print()

# ---- CORRECT length-3 witness ----
r0 = (mp.mpf(34)/101, mp.mpf(37)/101)
pts = [r0]
for _ in range(2): pts.append(M(pts[-1]))
print("CORRECT length-3 (N=2) witness, start (34/101, 37/101)  ->  realizes B(11)=3:")
allok = True
for i,p in enumerate(pts):
    a,b = p
    lb = a + lam*b - 1; gap = t - a*b
    kf = kfloor(p) if i < 2 else None
    ok = (lb > 0) and (gap > 0) and valid(p) and (i == 2 or kf == 1)
    allok = allok and ok
    print(f"  i={i}: lb-1={mp.nstr(lb,12)} (>0)  t-P={mp.nstr(gap,12)} (>0)  "
          f"valid_domain={valid(p)}  kfloor={kf}")
pred = Minv(r0)
pred_lb = pred[0] + lam*pred[1] - 1
print(f"  predecessor (lam*a0-b0, a0): lb-1={mp.nstr(pred_lb,8)}  "
      f"(<0 required => r0 is a genuine cluster START): {pred_lb < 0}")
print(f"  ALL CHECKS PASS: {allok}")
print()

# ---- rejected length-4 candidate ----
bad0 = (mp.mpf(19)/61, mp.mpf(22)/61)
print("REJECTED length-4 candidate, start (19/61, 22/61):")
a,b = bad0
print(f"  domain condition b > 1-lam*a ?  b={mp.nstr(b,8)}  1-lam*a={mp.nstr(1-lam*a,8)}  "
      f"-> valid_domain={valid(bad0)} (FALSE => transient, not a genuine cluster)")

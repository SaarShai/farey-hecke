"""
goal1_q4_proof_verify.py — DIRECT verification of the 5 inequality-lemmas of the
q=4 cluster<=2 proof, independent of orbit dynamics. Each lemma is checked by
dense sampling of its feasible region; we report min margins (must be > 0).

X = sqrt2/8.  lam = sqrt2.  T^4 = {0<a<=1, 1-lam*a < b <= 1}.
inT3(a,b) := a+lam*b > 1   (else T_2).

PROOF (cluster of >=2 extremes => 3rd is non-extreme):
 Let x_i=(a,b), x_{i+1}=(b,c)=bczMap(x_i), x_{i+2}=(c,d)=bczMap(x_{i+1}).
 P(a,b)=a*b on T3, = a(a+lam b)/lam on T2. Extreme := P<X.

 L_A  (T2 non-extreme):  on T^4 with a+lam*b<=1,  P = a(a+lam b)/lam >= 1-lam/2 > X.
       key: s=a+lam b, domain lam a+b>1 <=> a+s>lam; (1-a)(1-s)>=0 => a*s>=a+s-1>lam-1.
 => extreme => inT3.   So x_i, x_{i+1} in T3.
 On T3: c = -a + k*lam*b,  k=floor((1+a)/(lam b)).  a+c = k*lam*b.
 L_1  k>=1:  c>0 (since x_{i+1} in T^4∩T3 => c>(1-b)/lam>0) and a>0 => k*lam*b=a+c>0 => k>=1.
 L_2  k*b^2 < 1/4:  ab+bc=b(a+c)=k*lam*b^2 < 2X = lam/4 => k b^2 < 1/4.
 L_3  k>=2 (rule out k=1): if k=1 then a+c=lam*b; domain(a,b): lam a+b>1 => a>(1-b)/lam;
       T3(b,c): b+lam c>1 => c>(1-b)/lam; so lam*b=a+c>2(1-b)/lam=lam(1-b) => b>1/2.
       But L_2 with k=1: b^2<1/4 => b<1/2.  Contradiction. So k>=2.
 L_4  c>1/2:  k>=2 => b^2<1/8 => b<lam/4 => (domain x_{i+1}) c>1-lam*b>1-lam*(lam/4)=1/2.
 L_5  3rd non-extreme:
       x_{i+2}=(c,d), d=-b+l*lam*c, l=floor((1+b)/(lam c)).
       if (c,d) in T2: P>=1-lam/2>X  (L_A).
       if (c,d) in T3: c+lam*d>1; d=-b+l*lam*c; l=0 => c+lam*d=c-lam*b<=c<1 (not T3) so l>=1;
            P=cd=l*lam*c^2 - bc >= lam c^2 - bc > lam c^2 - X > lam*(1/4) - X = 2X - X = X.
"""
from __future__ import annotations
import math
import numpy as np

rng = np.random.default_rng(20260609)
LAM = math.sqrt(2.0)
X = LAM / 8.0
TWOX = LAM / 4.0


def sample_T4(n):
    a = rng.uniform(0, 1, n)
    lo = 1 - LAM * a
    b = lo + rng.uniform(0, 1, n) * (1 - lo)   # b in (1-lam a, 1]
    return a, b


# ---- L_A: on T2, P >= 1-lam/2 (> X) ----
def check_LA(n=20_000_000):
    a, b = sample_T4(n)
    s = a + LAM * b
    inT2 = s <= 1.0
    a, b, s = a[inT2], b[inT2], s[inT2]
    P = a * s / LAM
    margin_strong = P - (1 - LAM / 2)      # >= 0  (>= bound)
    margin_X = P - X                        # > 0
    # also verify the algebraic identity route: a*s - (a+s-1) = (1-a)(1-s) >= 0
    ident = a * s - (a + s - 1) - (1 - a) * (1 - s)
    return dict(n=int(inT2.sum()), minP=float(P.min()),
                min_margin_strong=float(margin_strong.min()),
                min_margin_X=float(margin_X.min()),
                max_ident_err=float(np.abs(ident).max()),
                a_plus_s_gt_lam_min=float((a + s - LAM).min()))


# ---- direct cluster check on feasible (a,b,k) triples (NOT orbit) ----
# Enumerate: for (a,b) in T^4∩T3 with ab<X, k=floor((1+a)/(lam b)), c=-a+k lam b.
# Require (b,c) in T^4∩T3 and bc<X. For all such, check k>=2, b<lam/4, c>1/2, and
# the 3rd point non-extreme.
def check_cluster_chain(n=40_000_000):
    a, b = sample_T4(n)
    s_i = a + LAM * b
    inT3_i = s_i > 1.0
    # x_i extreme & T3
    Pi = a * b
    m = inT3_i & (Pi < X) & (b > 0)
    a, b = a[m], b[m]
    k = np.floor((1 + a) / (LAM * b))
    c = -a + k * LAM * b
    # x_{i+1}=(b,c) must be in T^4 and T3, and extreme
    inT4_1 = (b > 0) & (b <= 1 + 1e-12) & (1 - LAM * b < c) & (c <= 1 + 1e-12)
    inT3_1 = (b + LAM * c > 1.0)
    P1 = b * c
    cl = inT4_1 & inT3_1 & (P1 < X)
    a, b, c, k = a[cl], b[cl], c[cl], k[cl]
    res = dict(n_clusters=int(cl.sum()))
    if cl.sum() == 0:
        return res
    res["min_k"] = float(k.min())
    res["L2_kb2_max"] = float((k * b * b).max())          # < 1/4
    res["L4_min_c"] = float(c.min())                        # > 1/2
    res["max_b"] = float(b.max())                           # < lam/4
    # third point
    ell = np.floor((1 + b) / (LAM * c))
    d = -b + ell * LAM * c
    s_2 = c + LAM * d
    inT3_2 = s_2 > 1.0
    # branch T3: P3 = c*d ; require >= X
    P3_T3 = c * d
    P3_T2 = c * s_2 / LAM
    P3 = np.where(inT3_2, P3_T3, P3_T2)
    res["L5_min_P3_minus_X"] = float((P3 - X).min())        # > 0  (3rd non-extreme)
    res["min_ell_when_T3"] = float(ell[inT3_2].min()) if inT3_2.any() else None
    res["frac_3rd_in_T2"] = float((~inT3_2).mean())
    return res


if __name__ == "__main__":
    print(f"X=sqrt2/8={X:.10f}  2X=lam/4={TWOX:.10f}  1-lam/2={1-LAM/2:.10f}  lam/4={LAM/4:.10f}")
    print("\n[L_A] T2 non-extreme  (P >= 1-lam/2 > X):")
    la = check_LA()
    for k_, v in la.items():
        print(f"   {k_} = {v}")
    assert la["min_margin_strong"] >= -1e-9, "L_A strong bound FAILS"
    assert la["min_margin_X"] > 0, "L_A > X FAILS"

    print("\n[Cluster chain] L_1..L_5 over feasible double-extreme T3 configs:")
    cc = check_cluster_chain()
    for k_, v in cc.items():
        print(f"   {k_} = {v}")
    if cc.get("n_clusters", 0) > 0:
        assert cc["min_k"] >= 2, f"L_3 k>=2 FAILS (min_k={cc['min_k']})"
        assert cc["L2_kb2_max"] < 0.25, "L_2 kb^2<1/4 FAILS"
        assert cc["L4_min_c"] > 0.5, "L_4 c>1/2 FAILS"
        assert cc["max_b"] < LAM / 4, "b<lam/4 FAILS"
        assert cc["L5_min_P3_minus_X"] > 0, "L_5 3rd non-extreme FAILS"
        print("\n   ALL PROOF LEMMAS VERIFIED (margins positive).")

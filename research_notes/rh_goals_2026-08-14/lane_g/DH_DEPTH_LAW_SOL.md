# `(DH)` comparison-weighted depth law: sine-envelope consequence, false shortcut, and exact remaining gap

**Date:** 2026-08-18
**Program:** `(RATE)`, lane G
**Interpreter:** `/Users/za/.venvs/farey-rh/bin/python`
**Write scope:** this file only

## 0. Verdict

The requested global comparison-weighted law

\[
 B_q(Y):=
 \sum_{X\in\mathcal C_q:\,m_X\le Y}
 k_X^2\frac{x_X}{m_X}
 \le C_0Y^2\min(Y,q)
       \bigl(1+\log_+(Y/q)\bigr)                       \tag{DH}
\]

is **NOT PROVED** by the new v29 assets.  It remains **CONJECTURAL / OPEN**.
The obstruction is not a missing trigonometric estimate: v29 proves the sharp
one-word estimate.  The missing statement is still a joint count over the
canonical balanced section, with all three load-bearing features retained:

1. raw deformation depth (k_X), not free-product syllable length;
2. the minimum height (m_X=\min(x_X,y_X));
3. the comparison factor (x_X/m_X).

What is proved here is the following.

* For (k\le q/2), v29 implies the explicit pointwise estimate

  \[
  k\le a_q^{-1}|c_w(\lambda_q)|,
  \qquad
  a_q:=\frac4\pi-\frac{2\pi}{q^2}.                     \tag{0.1}
  \]

  **only for words which satisfy the Lean hypothesis (k\le q-1)**.  Route-B
  matching does not imply that hypothesis.  At (q=12), the balanced matched
  word

  \[
  (2,Q,2,Q,2,Q,2,Q,2)
  \]

  has raw (Q)-depth (14>q-1), with
  (|c_q|=571.7883832488647\ldots) and (|c_\theta|=724).  Thus (0.1) is
  not a bound on every matched term.

* Even in the favorable subpopulation (m_X=x_X\), inserting (0.1) into the
  (k^2) drift envelope and then using Ford counting gives

  \[
  E_{\rm head}(q,X)=O(q^{-2}X^{4-2\sigma}).             \tag{0.2}
  \]

  At the natural (X=q), this is (O(q^{2-2\sigma})), exactly one power
  weaker than (O(q^{1-2\sigma})).

* The suggested replacement, “continuants grow Fibonacci-fast unless every
  digit is (\pm1),” is **FALSE**.  The one-defect family

  \[
  w_{a,k}=(a,1,\ldots,1),\qquad a\ge2,
  \]

  has

  \[
  c_{w_{a,k}}(2)
   =2\bigl((2a-1)(k-1)+1\bigr),                         \tag{0.3}
  \]

  so (k\asymp |c|), although the word is not all-unit.  Thus an exceptional
  split containing only the two Chebyshev words does not prove a logarithmic
  depth law.

* The two constant-sign Chebyshev families themselves can be treated exactly.
  Their whole pre-turnover contribution is

  \[
  E_{\rm Cheb}(q,s)=O_{\sigma,|s|}(q^{1-2\sigma})
  \qquad(1<\sigma<3/2),                                 \tag{0.4}
  \]

  with an explicit constant below.  Hence these extremals force the cubic
  low-height scale but do not obstruct RATE.  They do not, however, exhaust
  the near-parabolic families.

* A corrected post-(q) envelope with a second relative logarithm would still
  suffice for RATE:

  \[
  B_q(Y)\le C Y^2
  \left[q\bigl(1+L\bigr)+\bigl(1+L\bigr)^2\right],
  \quad L=\log(Y/q),\quad Y\ge q.                       \tag{DH\(_2\)}
  \]

  `(DH_2)` is **CONJECTURAL**, not proved here.  It is recorded because a
  genuine typical depth (k\asymp\log Y) naturally creates a
  (Y^2\log^2Y) second moment; omitting that term requires proof, not
  intuition.  Importantly, `(DH_2)` would introduce no loss in the final
  (q^{1-2\sigma}) exponent.

Consequently the honest final `(RATE)` status is:

| component | status |
|---|---|
| sharp pre-turnover sine envelope and continuant bridge | **MACHINE-VERIFIED** in v29, but its depth hypothesis is not automatic on the matched section |
| naïve Ford/sine route | **PROVED one power short:** (q^{2-2\sigma}) at (X=q) |
| Chebyshev-family paired drift | **PROVED:** (q^{1-2\sigma}) for (1<\sigma<3/2) |
| global `(DH)` or `(DH_2)` | **CONJECTURAL / OPEN** |
| N1-RATE interval derivative envelope on the canonical section | **CONJECTURAL** in the current graph |
| `(FW)` | claimed proved in `FW_RENEWAL_COUNT_SOL.md`, referee running; **not assumed here** |
| full `(RATE)` | **CONJECTURAL**; no proved exponent for the entire comparison sum |
| endpoint (sigma=3/2) by positive (k^2)-majorization | at best (q^{-2}\log q), already forced by Chebyshev |

## 1. Receipts before claims

### 1.1 Definition and machine-verified inputs

The defining source was read exactly at the requested range:

```bash
sed -n '963,1055p' \
  research_notes/rh_goals_2026-08-14/lane_g/M1_ROUTE_B_REPAIR_SOL.md
```

The relevant output is:

```text
Define the comparison-weighted cumulative depth count

 B_q(Y):=
 sum_{X in C_q: m_X <= Y} k_X^2 x_X/m_X.               (5.7)

... B_q(Y) <= C_0 Y^2 min(Y,q)
       (1+log_+(Y/q)), Y>=1.                            (DH)

Statements (DH) and (FW) are CONJECTURAL.
```

The v29 result file is
`projects/aristotle_dispatch_v29/result/v29sub_aristotle/RateCoreIV.lean`.
The exact theorem declarations and artifact hash were checked by:

```bash
rg -n "^[[:space:]]*sorry|theorem c_eq_lam_mul_continuant|theorem sharp_no_wrap|theorem sharp_no_wrap_eq" \
  projects/aristotle_dispatch_v29/result/v29sub_aristotle/RateCoreIV.lean
sha256sum projects/aristotle_dispatch_v29/result/v29sub_aristotle/RateCoreIV.lean
```

Output:

```text
122:theorem c_eq_lam_mul_continuant (lam : ℝ) (w : List ℤ) :
405:theorem sharp_no_wrap
549:theorem sharp_no_wrap_eq_chebyshev_words
fee8a039c0cc7140a9b9d63a669653cfb83b060e4f6526bb882ecf21817ce88c  projects/aristotle_dispatch_v29/result/v29sub_aristotle/RateCoreIV.lean
```

There is no code-line `sorry` match; occurrences of the word in the prose
header were excluded by the anchored pattern.  The proved statements are:

\[
 c_w(\lambda)=\lambda K_w(\lambda),                    \tag{1.1}
\]

and, for a syntactically reduced exponent list of raw (Q)-depth
(1\le k\le q-1),

\[
 |c_w(\lambda_q)|\ge
 \lambda_q\frac{\sin(k\pi/q)}{\sin(\pi/q)}.            \tag{1.2}
\]

Both constant-sign unit words attain equality.  The scope (k\le q-1) is
part of the theorem.  The lower bound turns over after (q/2) and approaches
zero at (k=q); it is not a global raw-depth bound.

The parenthetical premise in the task, “matched words are no-wrap,” is false
if it is meant to supply the theorem's numerical depth hypothesis.  Here is a
fresh direct matrix receipt.  `R=QS`; hence the displayed balanced `R,Q` word
contains (5\cdot2+4=14) raw (Q)'s.

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from mpmath import mp
mp.dps=50
def mm(A,B):
 return [[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)]
         for i in range(2)]
def pw(A,n):
 Z=[[mp.mpf(1),0],[0,mp.mpf(1)]]
 while n:
  if n&1: Z=mm(Z,A)
  A=mm(A,A); n//=2
 return Z
def cv(lam):
 Q=[[0,-1/lam],[lam,0]]; R=mm(Q,[[1,1],[0,1]])
 M=[[mp.mpf(1),0],[0,mp.mpf(1)]]
 for z in (2,'Q',2,'Q',2,'Q',2,'Q',2):
  M=mm(M,Q if z=='Q' else pw(R,z))
 return abs(M[1][0])
for q,lam in [(12,2*mp.cos(mp.pi/12)),('theta',mp.mpf(2))]:
 print(q,mp.nstr(cv(lam),30))
print('raw_Q_depth=',5*2+4,'Lean_limit=',12-1)
PY
```

Output:

```text
12 571.788383248864753432028646348
theta 724.0
raw_Q_depth= 14 Lean_limit= 11
```

All five `R`-digits are (2), inside the (q=12) balanced alphabet, so this is
a matched Route-B class.  Consequently §2 below is deliberately only a
favorable **subpopulation** calculation; applying it to the whole paired sum
would be invalid.

### 1.2 Exact-window artifact

The requested artifact hashes as follows:

```bash
sha256sum \
  research_notes/rh_goals_2026-08-14/lane_g/law_probes/r1_coset_enum_complete_X50.json
```

Output:

```text
c1efc1336b1c2a1ccdcb9698653442788270e0f1466738b119d747f2acacaf20  research_notes/rh_goals_2026-08-14/lane_g/law_probes/r1_coset_enum_complete_X50.json
```

Its own status is deliberately limited:

```text
theta_window: PROVED exact target count plus enumerator equality
finite_q_windows: CERTIFIED-FINITE within the all-integer quotient-state in-window regime
global_no_outside_then_reentry_claim: CONJECTURAL; not proved by this finite computation
```

The stored `witness_depth` joint histograms were recomputed by:

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
import json,math,statistics,collections
p='research_notes/rh_goals_2026-08-14/lane_g/law_probes/r1_coset_enum_complete_X50.json'
J=json.load(open(p))
for q in ('5','8','12','inf'):
 rows=J['groups'][q]['cosets']; H=sum(z['witness_depth']**2 for z in rows)
 hist=collections.Counter(z['witness_depth'] for z in rows)
 ratios=[z['witness_depth']/math.log(float(z['c_abs']))
         for z in rows if float(z['c_abs'])>1]
 kc=[z['witness_depth']/float(z['c_abs']) for z in rows]
 print(f"q={q} n={len(rows)} H={H} kmax={max(hist)} hist="+
       ' '.join(f'{k}:{hist[k]}' for k in sorted(hist)))
 print(f"  k/logc median={statistics.median(ratios):.6f} "
       f"mean={statistics.mean(ratios):.6f} max={max(ratios):.6f}; "
       f"k/c median={statistics.median(kc):.6f} max={max(kc):.6f}")
PY
```

Output:

```text
q=5 n=428 H=6451 kmax=6 hist=1:1 2:38 3:126 4:169 5:84 6:10
  k/logc median=1.099076 mean=1.116074 max=2.078087; k/c median=0.111456 max=0.763932
q=8 n=330 H=6411 kmax=8 hist=1:1 2:28 3:72 4:95 5:80 6:42 7:10 8:2
  k/logc median=1.270228 mean=1.253814 max=2.540456; k/c median=0.129476 max=0.828427
q=12 n=318 H=8047 kmax=9 hist=1:1 2:26 3:60 4:72 5:58 6:47 7:30 8:18 9:6
  k/logc median=1.331502 mean=1.384158 max=2.984919; k/c median=0.143594 max=0.803848
q=inf n=263 H=15961 kmax=25 hist=1:1 2:24 3:56 4:52 5:38 6:24 7:16 8:10 9:10 10:2 11:2 12:2 13:2 14:2 15:2 16:2 17:2 18:2 19:2 20:2 21:2 22:2 23:2 24:2 25:2
  k/logc median=1.337732 mean=1.766655 max=6.390555; k/c median=0.142857 max=0.500000
```

This is a finite diagnostic, not `(DH)`.  More strongly, the JSON witness is
the first word retained by the enumerator for a canonical matrix key.  It is
not a theorem that `witness_depth` equals the raw depth of the Route-B
balanced canonical section, nor that it is minimal double-coset depth.  The
finite (q) rows also include (x\le50) classes whose theta lifts have
(y>50).  Therefore these histograms cannot be inserted into (5.7) as a
proof of a matched cumulative bound.

The exact theta-side canonical census in
`DENSITY_GAIN_ATTACK_SOL.md:340-499` separates these notions.  Within
(y\le50), the exact image counts are

\[
98,164,204,223,236,244,260
\]

for (q=5,8,12,16,24,32,48), whereas the finite (x\le50) JSON counts for
(q=5,8,12) are (428,330,318).  Equality of these two different windows
would be a false assumption.

For the actual Route-B image in the exact (q=12, y\le50) window, replaying
the canonical-word test from `DENSITY_GAIN_ATTACK_SOL.md:340-499` and the
centered-Euclidean depth recurrence from
`M1_ROUTE_B_REPAIR_SOL.md:747-813` gives:

The fresh command was the following self-contained stdout-only heredoc:

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from collections import Counter
from math import gcd
from mpmath import mp
mp.dps=50

def red(t):
 o=[]
 for z,a in t:
  if z=='Q':
   if o and o[-1][0]=='Q':o.pop()
   else:o.append(('Q',1))
  elif a:
   if o and o[-1][0]=='R':
    b=o.pop()[1]+a
    if b:o.append(('R',b))
   else:o.append(('R',a))
 return o
def canon(t):
 t=red(t)
 while True:
  if not t:return ()
  if len(t)==1 and (t[0][0]=='Q' or abs(t[0][1])==1):return ('Q',)
  old=t[:]
  if t[0][0]=='Q':t=red([('R',t[1][1]-1)]+t[2:])
  elif t[0]==('R',-1):t=red(t[2:])
  if not t:return ()
  if len(t)==1 and (t[0][0]=='Q' or abs(t[0][1])==1):return ('Q',)
  if t[-1][0]=='Q':t=red(t[:-2]+[('R',t[-2][1]+1)])
  elif t[-1]==('R',1):t=red(t[:-2])
  if t==old:return tuple(a if z=='R' else 'Q' for z,a in t)
def from_cd(c,d):
 ns=[]
 while c:
  if c<0:c,d=-c,-d
  r=d%(2*c)
  if r>c:r-=2*c
  ns.append((r-d)//(2*c));c,d=r,-c
 t=[]
 for n in reversed(ns):
  t.append(('Q',1));m=-n
  t += [('Q',1),('R',1)]*m if m>0 else [('R',-1),('Q',1)]*(-m)
 return canon(t)
def mm(A,B):
 return [[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)]
         for i in range(2)]
def inv(A):return [[A[1][1],-A[0][1]],[-A[1][0],A[0][0]]]
def pw(A,n):
 if n<0:return pw(inv(A),-n)
 Z=[[mp.mpf(1),0],[0,mp.mpf(1)]]
 while n:
  if n&1:Z=mm(Z,A)
  A=mm(A,A);n//=2
 return Z
def c_eval(w,lam):
 Q=[[0,-1/lam],[lam,0]];R=mm(Q,[[1,1],[0,1]])
 M=[[mp.mpf(1),0],[0,mp.mpf(1)]]
 for z in w:M=mm(M,Q if z=='Q' else pw(R,z))
 return abs(M[1][0])
def balmod(a,m):
 r=a%m
 return r-m if 2*r>m else r
def depth(c,d):
 a,b,k=c,abs(balmod(d,2*c)),1
 while b:a,b,k=b,abs(balmod(a,2*b)),k+1
 return k
q=12; A=set(range(-5,0))|set(range(1,7)); rows=[]
for c in range(1,26):
 for d in range(2*c):
  if gcd(c,d)==1 and (c+d)%2:
   w=from_cd(c,d)
   if all(z=='Q' or z in A for z in w):
    rows.append((c,d,depth(c,d),c_eval(w,2*mp.cos(mp.pi/q))))
h=Counter(k for c,d,k,x in rows)
print('n=',len(rows),'hist='+' '.join(f'{k}:{h[k]}' for k in sorted(h)))
print('depth_gt_q_over_2=',sum(k>q/2 for c,d,k,x in rows),
      'sum_k2=',sum(k*k for c,d,k,x in rows))
print('x_gt_y=',sum(x>2*c for c,d,k,x in rows))
PY
```

Output:

```text
n= 204 hist=1:1 2:24 3:56 4:52 5:38 6:22 7:10 8:1
depth_gt_q_over_2= 11 sum_k2= 3729
x_gt_y= 0
```

The count and histogram are exact integers.  The last comparison is a
50-digit `mpmath` replay and is therefore only a finite diagnostic.  Even in
this tiny matched window, 11 of 204 depths lie beyond (q/2), so the linear
sine corollary cannot simply be summed over the whole window.

The fixed-level theta computation also answers the “typical depth” question
in the only way relevant to a (k^2)-weighted law.  Fresh exact-integer receipt:

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from math import gcd,sqrt
from statistics import median
def balmod(a,m):
 r=a%m
 return r-m if 2*r>m else r
def depth(c,d):
 a,b,k=c,abs(balmod(d,2*c)),1
 while b:a,b,k=b,abs(balmod(a,2*b)),k+1
 return k
c=2000
ks=[depth(c,d) for d in range(2*c) if gcd(c,d)==1 and (c+d)%2]
hi=[k for k in ks if k>sqrt(c)]
print('cH=',c,'n=',len(ks),'median_k=',median(ks),'max_k=',max(ks))
print('k_gt_sqrt_cH=',len(hi),
      'sumk2_share=',sum(k*k for k in hi)/sum(k*k for k in ks))
PY
```

Output:

```text
cH= 2000 n= 1600 median_k= 12.0 max_k= 2000
k_gt_sqrt_cH= 98 sumk2_share= 0.9695686823853215
```

Thus the median depth is indeed logarithmic-looking, but the 98 depths above
(\sqrt{c_H}) carry (96.9568\%) of the (k^2) mass.  “Typical depth” in an
unweighted histogram is not evidence for the second moment required by
`(DH)`.

## 2. What the sine envelope actually proves

Put

\[
 \theta=\frac\pi q,\qquad \lambda_q=2\cos\theta.
\]

For (1\le k\le q/2), concavity of sine on ([0,\pi/2]) gives

\[
 \sin(k\theta)\ge\frac{2k\theta}{\pi}=\frac{2k}{q},
 \qquad \sin\theta\le\theta=\frac\pi q.                \tag{2.1}
\]

Also (cos\theta\ge1-\theta^2/2), hence

\[
 \lambda_q\ge2-\frac{\pi^2}{q^2}.                     \tag{2.2}
\]

Substitution in (1.2) proves

\[
 |c_w(\lambda_q)|
 \ge\left(\frac4\pi-\frac{2\pi}{q^2}\right)k
 =a_qk.                                                 \tag{2.3}
\]

For (q\ge12), one may use the uniform downward-rounded coefficient

\[
 a_q\ge a_{12}
 =\frac4\pi-\frac{\pi}{72}
 =1.2296063134\ldots,\qquad a_{12}^{-1}<0.814.          \tag{2.4}
\]

This is the promised (k\le(\pi/4+o(1))|c|) statement, with the direction
of the rounding correct.  It is pointwise and pre-turnover only.

### 2.1 Honest Ford exponent

Let (p=2\sigma\in(2,3)), and temporarily restrict to terms satisfying all
of the following favorable conditions:

* the selected raw word has (k\le q/2);
* (m_X=x_X=|c_w(\lambda_q)|), so (x_X/m_X=1);
* the **CONJECTURAL** N1-RATE envelope is granted with constant (A):

  \[
  \Delta_X:=|x_X-y_X|
   \le A(2-\lambda_q)k_X^2x_X.                         \tag{2.5}
  \]

The MVT estimate then gives

\[
 |x_X^{-2s}-y_X^{-2s}|
 \le2|s|A(2-\lambda_q)k_X^2x_X^{-p}.                  \tag{2.6}
\]

By (2.3), (k_X^2\le a_q^{-2}x_X^2).  If
(A_x(T)=\#\{X:x_X\le T\}\le T^2) is the width-one Ford count, Stieltjes
summation gives

\[
\begin{aligned}
 \sum_{x_X\le X}x_X^{2-p}
 &=X^{2-p}A_x(X)+(p-2)\int_1^X A_x(t)t^{1-p}\,dt\\
 &\le X^{4-p}+\frac{p-2}{4-p}(X^{4-p}-1)\\
 &\le\frac{2}{4-p}X^{4-p}.                             \tag{2.7}
\end{aligned}
\]

Since (2-\lambda_q\le\pi^2/q^2), (2.6)--(2.7) prove

\[
 \boxed{
 E_{\rm fav}(q,X)
 \le \frac{4\pi^2A|s|}{a_q^2(4-p)}
       q^{-2}X^{4-p}.}                                  \tag{2.8}
\]

At (X=q),

\[
 E_{\rm fav}(q,q)
 \le \frac{4\pi^2A|s|}{a_q^2(4-p)}q^{2-p}.            \tag{2.9}
\]

Thus the proposed pointwise substitution produces (q^{2-2\sigma}), not
(q^{1-2\sigma}).  This is the honest exponent.  It is already one power
short on a favorable subpopulation, before the post-turnover terms and the
ratio (x_X/m_X) are restored.

### 2.2 Why this does not even bound all of (B_q(Y))

The condition (m_X\le Y) is the union of (x_X\le Y) and (y_X\le Y).
When (m_X=y_X<x_X), Ford counting in (x_X) does not constrain the term,
and

\[
 k_X^2\frac{x_X}{m_X}
\]

retains the possibly large ratio (x_X/y_X).  The sine envelope is a lower
bound for (x_X); it gives neither (x_X\ll y_X) nor a count of
(y_X\le Y<x_X).  N1-RATE would imply

\[
 y_X\ge x_X\bigl(1-A(2-\lambda_q)k_X^2\bigr),          \tag{2.10}
\]

but this is useful only while the parenthesis is positive and bounded away
from zero.  At (k\asymp q), the product
((2-\lambda_q)k^2\asymp1), so (2.10) is not a global comparison theorem.

Therefore replacing (m_X) by one endpoint height, or deleting (x_X/m_X),
would round the required upper bound downward.

## 3. The proposed Fibonacci repair is false

At (lambda=2), the negative continuant satisfies

\[
 K(n_1,n_2,\ldots)=2n_1K(n_2,\ldots)-K(n_3,\ldots),
 \qquad c_w(2)=2K_w(2).                                 \tag{3.1}
\]

For

\[
 w_{a,k}=(a,\underbrace{1,\ldots,1}_{k-2}),
 \qquad a\ge1,\quad k\ge2,
\]

an induction using (3.1) gives

\[
 K_{w_{a,k}}(2)=(2a-1)(k-1)+1.                         \tag{3.2}
\]

Fresh exact-integer receipt:

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
def K(w):
 if not w:return 1
 if len(w)==1:return 2*w[0]
 return 2*w[0]*K(w[1:])-K(w[2:])
for a in (1,2,3):
 for k in (2,3,5,10,25):
  w=(a,)+(1,)*(k-2)
  exact=K(w); formula=(2*a-1)*(k-1)+1
  print(f'a={a} k={k} K={exact} formula={formula} c_theta={2*exact}')
PY
```

Selected output:

```text
a=1 k=25 K=25 formula=25 c_theta=50
a=2 k=10 K=28 formula=28 c_theta=56
a=2 k=25 K=73 formula=73 c_theta=146
a=3 k=10 K=46 formula=46 c_theta=92
a=3 k=25 K=121 formula=121 c_theta=242
```

For every fixed (a\ge2), (3.2) is linear in (k), and the word contains a
nonunit digit.  Hence:

> **FALSE:** every non-Chebyshev word has (k=O(\log|c|)).
>
> **NEGATION:** the explicit family (w_{2,k}) has
> (c_{w_{2,k}}(2)=6k-4), so (k/\log|c|\to\infty).
>
> **CORRECTED requirement:** a successful proof must count a hierarchy of
> finitely perturbed parabolic runs.  Isolating only the two all-sign words is
> insufficient.

This does not refute the cubic aggregate (\sum_{|c|\le Y}k^2=O(Y^3)): each
fixed one-defect family is sparse.  It refutes the proposed pointwise route
to that aggregate.

It is not merely an irrelevant raw-word family.  For (a=2), the Route-B
boundary reduction of the same double coset is

\[
 (1,Q,k)=RQR^k,
\]

and direct multiplication at (\lambda=2) gives the same
(|c_\theta|=6k-4).  Hence it is in the balanced matched image whenever
(k\le\lfloor q/2\rfloor).  So the proposed “Chebyshev terms exactly, every
other term logarithmic” split is false even on the paired section.  A valid
split must control all bounded-defect parabolic families in aggregate; no
such weighted renewal bound is proved here.

## 4. Exact treatment of the true Chebyshev extremals

Let

\[
 w_k^{\pm}=(\pm1,\ldots,\pm1),\qquad 1\le k\le h:=\lfloor q/2\rfloor.
\]

The v29 equality theorem gives

\[
 x_k=|c_{w_k^\pm}(\lambda_q)|
 =\lambda_q\frac{\sin(k\pi/q)}{\sin(\pi/q)},
 \qquad y_k=|c_{w_k^\pm}(2)|=2k.                       \tag{4.1}
\]

Since (sin(k\theta)\le k\sin\theta) for
(0\le k\theta\le\pi/2) and (lambda_q\le2), one has (x_k\le y_k),
so (m_k=x_k).  A fully explicit drift bound follows without assuming the
global N1 envelope.  Use

\[
 \sin(k\theta)\ge k\theta-\frac{k^3\theta^3}{6},
 \quad \cos\theta\ge1-\frac{\theta^2}{2},
 \quad \sin\theta\le\theta.
\]

Then

\[
 x_k\ge
 2\left(1-\frac{\theta^2}{2}\right)
  \left(k-\frac{k^3\theta^2}{6}\right)
 \ge2k-\theta^2\left(k+\frac{k^3}{3}\right),          \tag{4.2}
\]

and hence

\[
 0\le y_k-x_k
 \le\frac{\pi^2}{3q^2}k(k^2+3).                       \tag{4.3}
\]

Combining (4.3), (x_k\ge a_qk), and MVT gives

\[
 |x_k^{-2s}-y_k^{-2s}|
 \le\frac{2\pi^2|s|}{3q^2}a_q^{-p-1}
       \left(k^{2-p}+3k^{-p}\right).                   \tag{4.4}
\]

There are at most two sign choices at each (k).  Therefore

\[
\begin{aligned}
 E_{\rm Cheb}(q,s)
 &\le\frac{4\pi^2|s|}{3q^2}a_q^{-p-1}
 \left(\sum_{k\le h}k^{2-p}+3\sum_{k\le h}k^{-p}\right)\\
 &\le\frac{4\pi^2|s|}{3q^2}a_q^{-p-1}
 \left(1+\frac{h^{3-p}}{3-p}+3\zeta(p)\right).         \tag{4.5}
\end{aligned}
\]

Because (h\le q/2) and (q^{-2}\le q^{1-p}) for (2<p<3), (4.5) yields
the explicit RATE-scale bound

\[
 \boxed{
 E_{\rm Cheb}(q,s)
 \le \frac{4\pi^2|s|}{3}a_q^{-p-1}
 \left(1+\frac{2^{p-3}}{3-p}+3\zeta(p)\right)
 q^{1-p}.}                                              \tag{4.6}
\]

Thus the sharp equality cases are not the missing obstruction.  They explain
why a (Y^3) low-height second moment is optimal.  At (p=3), (4.5) becomes
(O(q^{-2}\log q)), so a positive termwise proof cannot be uniform through
(sigma=3/2) without a logarithm or cancellation.

## 5. What a valid aggregate proof still has to establish

The exact layer-cake identity from `M2_LOCALIZATION_THEOREM_SOL.md` remains
the correct target.  If

\[
 \mathcal B_q(Y,K):=
 \#\{X:m_X\le Y,\ k_X\ge K\}
\]

were unweighted, then

\[
 \sum_{m_X\le Y}k_X^2
 =\sum_{K\ge1}(2K-1)\mathcal B_q(Y,K).                 \tag{5.1}
\]

For `(DH)`, however, the counted measure must carry (x_X/m_X).  A sufficient
pointwise tail law has to be of the form

\[
 \sum_{\substack{m_X\le Y\\k_X\ge K}}
 \frac{x_X}{m_X}
 \le C\frac{Y^2R}{K}
 \min\left\{1,\left(\frac{L}{K}\right)^2\right\},
 \quad L=\min(Y,q),\quad R=1+\log_+(Y/q).               \tag{5.2}
\]

Summing (5.2) by (5.1) would give `(DH)`.  Neither sharp no-wrap nor Ford
proves (5.2): sharp no-wrap is pointwise and turns over; Ford is the
(K=1), unweighted marginal only.

The first-overflow factorization used in the claimed `(FW)` proof does not
automatically give (5.2).  `(FW)` marks one digit satisfying
(|a|\ge q/2), and that large coefficient forces a product constraint.
Every image digit is instead bounded by (q/2); long chains of digits
(pm1) have no analogous one-letter gain.  A matched proof needs a genuine
renewal theorem with a depth cost, together with control of endpoint
comparison.

### 5.1 A safer sufficient cumulative shape

If a renewal proof naturally returns the square of a logarithmic typical
depth, the following would still close RATE:

\[
 B_q(Y)\le C
 \begin{cases}
 Y^3,&1\le Y\le q,\\
 Y^2\left[q(1+L)+(1+L)^2\right],&Y\ge q,
 \end{cases}
 \qquad L=\log(Y/q).                                   \tag{5.3}
\]

This is `(DH_2)` and is **CONJECTURAL**.  For (2<p<3), its extra term has

\[
\begin{aligned}
 p\int_q^\infty t^{1-p}(1+\log(t/q))^2\,dt
 ={}&p q^{2-p}
 \left(
  \frac1{p-2}+\frac2{(p-2)^2}+\frac2{(p-2)^3}
 \right).                                               \tag{5.4}
\end{aligned}
\]

Since (q^{2-p}\le q^{3-p}), (5.4) is smaller than the required cumulative
scale.  After multiplying by (2-\lambda_q\le\pi^2/q^2), it is
(O(q^{-p})\), hence smaller than (O(q^{1-p})).  Therefore an honest second
logarithm in the far tail would not damage RATE.  What cannot be done is to
delete it without either a proof or a different moment argument.

## 6. Conditional assembly, with constants visible

This section is conditional bookkeeping only.  It does **not** assume the
parallel `(FW)` referee will accept that proof.

Assume:

1. N1-RATE with constant (A);
2. `(DH)` with constant (C_0);
3. `(FW)` with constant (C_1).

Let

\[
 F(p)=\frac1{3-p}+\frac1{p-2}+\frac1{(p-2)^2},
 \qquad
 G(p)=\frac1{p-2}+\frac1{(p-2)^2}.                     \tag{6.1}
\]

Then Stieltjes summation and MVT give

\[
 E_{\rm paired}(q,s)
 \le 2\pi^2A|s|\,pC_0F(p)\,q^{1-p},                   \tag{6.2}
\]

while conditional `(FW)` gives

\[
 E_{\rm wrap}(q,s)
 \le pC_1G(p)\,q^{1-p}.                                \tag{6.3}
\]

Thus the conditional Dirichlet comparison is

\[
 |D_q(s)-D_\theta(s)|
 \le p\left(2\pi^2A|s|C_0F(p)+C_1G(p)\right)q^{1-p}.  \tag{6.4}
\]

The scattering comparison carries the additional factor

\[
 |M(s)|=\left|\sqrt\pi\,\frac{\Gamma(s-1/2)}{\Gamma(s)}\right|. \tag{6.5}
\]

At (s=1.1+1.5i), (p=2.2), (F(p)=31.25), (G(p)=30).  With the
still-conjectural (A=11/20), the paired coefficient before (C_0) and
(|M(s)|) is about (1388.37).  If the claimed explicit
(C_1=128(1+\log2)) survives referee, the wrap coefficient before
(|M(s)|) is about (14303.71).  These deliberately unoptimized constants
show why a measured small-(q) constant cannot be substituted for the proof
constant.

If `(DH_2)` replaces `(DH)`, (5.4) adds a (q^{-p}) term to (6.2); the
leading paired exponent remains (q^{1-p}), with no external (log q).

## 7. Numerical comparison with `LAW_RATE_MEASURE`

These values are evaluator output, not evidence for `(DH)`.  The raw file is
`law_probes/rate_measure_data.json`; it hashes to

```text
e117b418cb2bbbf8cde8ecbb7c4977b4865740c30b890a9c6e669203394d339d  research_notes/rh_goals_2026-08-14/lane_g/law_probes/rate_measure_data.json
```

Fresh extraction:

```bash
/Users/za/.venvs/farey-rh/bin/python - <<'PY'
import json,math
p='research_notes/rh_goals_2026-08-14/lane_g/law_probes/rate_measure_data.json'
rows=[r for r in json.load(open(p))
      if r['sigma']==1.1 and r['t']==1.5 and r['q'] in (12,16,24,32,48)]
for r in rows:
 q=r['q']; D=r['D']
 print(f"q={q} D={D:.16g} conv={r['convergence_reldiff']:.16g} "
       f"D*q^1.2={D*q**1.2:.12f}")
x=[math.log(r['q']) for r in rows]; y=[math.log(r['D']) for r in rows]
xb=sum(x)/len(x); yb=sum(y)/len(y)
sl=sum((a-xb)*(b-yb) for a,b in zip(x,y))/sum((a-xb)**2 for a in x)
print(f'OLS_slope_logD_logq={sl:.12f}')
print(f'max_scaled_up_to_2dp={math.ceil(max(r["D"]*r["q"]**1.2 for r in rows)*100)/100:.2f}')
PY
```

Output:

```text
q=12 D=0.05520810667794957 conv=1.228877587814443e-06 D*q^1.2=1.088981116273
q=16 D=0.05061603668627486 conv=1.310847628390323e-06 D*q^1.2=1.410042215970
q=24 D=0.03616602887987237 conv=1.003664501594276e-06 D*q^1.2=1.638907017534
q=32 D=0.02506274791163597 conv=1.08921267162404e-06 D*q^1.2=1.604015866345
q=48 D=0.01377995541936121 conv=1.50437307493386e-06 D*q^1.2=1.434621375423
OLS_slope_logD_logq=-1.009962259571
max_scaled_up_to_2dp=1.64
```

The fresh five-point slope is (-1.010), not the stale (-0.81) printed in
the older prose fit.  The RATE target at (sigma=1.1) is (-1.2).
The scaled values (Dq^{1.2}\le1.64) over these five points are compatible
with the target but neither monotone nor a bound beyond the sample.

The convergence receipts are (1.00\times10^{-6}) to
(1.50\times10^{-6}).  Several exceed the literal pre-registered
(10^{-6}) N=24 gate.  The later N=40 validation passes on the exact
(q=3,4,6) comparator grid, but these (q>6) rows themselves remain
author-reported N=24 values with per-row doubling receipts.  They are
**MEASUREMENT ONLY**.

## 8. R5 arithmetic versus the `0.66` defect

Let

\[
 t_0=\gamma_1/2
 =7.0673625708673468952\ldots .                         \tag{8.1}
\]

The RATE measurements above are at (t=1.5), not at (t_0).  The old
near-target row used (t=7.0665), a displacement

\[
 t_0-7.0665=0.0008625708673468952\ldots,                \tag{8.2}
\]

and those rows were not converged at N=24.  Therefore neither table
calibrates the R5 boundary constant.

The older (0.6604) number is only a sampled-grid witness.  The current R3
file instead contains a continuous Arb certificate

\[
 d_*:=\inf_{|t-t_0|\le0.025}(1-|\phi_\infty(1/2+it)|)
 >0.6603,                                                \tag{8.3}
\]

with raw lower endpoint
(0.660309770144522190093994140625\ldots).  Thus the safe strict R5 test is
(E_3(q)<0.6603), not a comparison with (0.6604).  Receipt:

```bash
rg -n "c_0=|661462|d_\\*:=|q_C&=|defect_lower=" \
  research_notes/rh_goals_2026-08-14/lane_g/R3_ROUTE_B_TRANSPORT_SOL.md
```

Selected output:

```text
501: c_0=0.03156\cdot0.000579=1.827324\times10^{-5}.
523: 1-|\phi_\infty(z_c)|>0.6614628229868551509.
533: d_*:=\inf(1-|\phi_\infty|)>0.6603.
567: q_C&=\left\lfloor
618:critical_defect_lower= [0.66146282298685515096542480851789701253689729523684257506510131546737399100506063 +/- 3.86e-81]
650:defect_lower= 0.660309770144522190093994140625000000...
```

Thus the pointwise defect at (t_0) is certified above
(0.6614628229868551509), while the smaller (0.6603) is the uniform constant
that survives throughout the whole interval required by R5.

If RATE were proved in the form (E_R(q)\le C_Rq^{-\alpha}), the two
propagation stages in that file give

\[
 \log E_3(q)<56155+c_0\log C_R-\alpha c_0\log q,
 \qquad c_0=1.827324\times10^{-5}.                       \tag{8.4}
\]

Solving the strict certified-margin inequality, with the integer boundary
rounded upward, gives

\[
 q_C=\left\lfloor
 \exp\!\left(\frac{56155-\log(0.6603)}{\alpha c_0}\right)
 C_R^{1/\alpha}\right\rfloor+1.                         \tag{8.5}
\]

This is the relevant R5 arithmetic.  Even if DH supplied the desired RATE
exponent (\alpha=1.2) at the needed boundary, the tiny multiplier (c_0)
makes the threshold enormous.  With (C_R) left symbolic, the arithmetic is:

```bash
/Users/za/.venvs/farey-rh/bin/python - <<'PY'
import math
c0=0.03156*0.000579
num=56155-math.log(0.6603)
for alpha in (1.2,0.2):
 print('alpha=',alpha,
       'log_q_base=',num/(alpha*c0),
       'log10_q_base=',num/(alpha*c0*math.log(10)),
       'C_R_power=',1/alpha)
PY
```

Output (binary64 evaluation; the rigorous displayed threshold below is rounded
upward separately):

```text
alpha= 1.2 log_q_base= 2560913073.844676 log10_q_base= 1112190416.6046376 C_R_power= 0.8333333333333334
alpha= 0.2 log_q_base= 15365478443.068054 log10_q_base= 6673142499.627825 C_R_power= 5.0
```

Hence the desired conditional exponent would already require

\[
 \log q>2.560914\times10^9+\frac56\log C_R.                \tag{8.6}
\]

The second row only shows the arithmetic consequence *if* the weak
(\alpha=0.2) behavior were available as a full uniform RATE bound; (2.9)
does not prove such a bound.  More importantly,
(C_R,\alpha,q_{\rm RATE}) are not proved because DH/N1-RATE remain open.
Therefore (q_0) is **UNDEFINED**, not merely large.  The complement-only
`210980852` calculation in `M1_ROUTE_B_REPAIR_SOL.md` uses the weak
(q^{-0.2}) Ford exponent and is explicitly not an R5 threshold.

## 9. Final claim ledger

| Claim | Verdict | Reason |
|---|---|---|
| (k\le a_q^{-1}|c_q|) for (k\le q/2), under the Lean syntactic hypotheses | **PROVED** | v29 `sharp_no_wrap` plus elementary sine inequalities; not automatic for all matched words |
| Naïve pointwise depth + Ford gives paired RATE | **FALSE** | exact calculation (2.8): (q^{-2}X^{4-p}), hence (q^{2-p}) at (X=q) |
| Every non-all-unit continuant has logarithmic depth | **FALSE** | one-defect identity (3.2) |
| Two Chebyshev families are the only exceptional families needed | **FALSE as a proof route** | (w_{a,k}), (a\ge2), is also linear depth-height |
| Chebyshev subfamily contributes (O(q^{1-p})) | **PROVED** for (2<p<3) | explicit trigonometric bound (4.6) |
| `(DH)` | **CONJECTURAL / OPEN** | no weighted renewal estimate (5.2); comparison ratio remains |
| `(DH_2)` | **CONJECTURAL / OPEN**, but sufficient | explicit integral (5.4) preserves RATE |
| `(FW)` | **not assumed** | separate proof is under referee |
| full `(RATE)` (O(q^{1-2\sigma})) | **CONJECTURAL** | depends at least on N1-RATE, `(DH)`/`(DH_2)`, accepted `(FW)`, and R3 uniformity |
| full positive-majorant endpoint at (sigma=3/2) | **exponent with log:** (q^{-2}\log q) | Chebyshev harmonic sum |
| finite R5 threshold from the certified `0.6603` defect | **UNDEFINED** | (C_R,\alpha,q_{\rm RATE}) and activation gates remain unproved; `0.6604` is sampled only |

The final conjectural lemma is therefore not closed.  The v29 theorem removes
the pointwise algebraic doubt and proves the extremal family exactly; it does
not supply the comparison-weighted renewal count.  Any promotion of `(DH)`
from these assets would conflate a one-word height bound with a two-parameter
second-moment theorem and would omit (x_X/m_X).

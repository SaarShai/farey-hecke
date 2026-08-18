# The last open RATE lemma: attack on the missing \(q^{-1}\) density gain

**Date:** 2026-08-18
**Interpreter:** `/Users/za/.venvs/farey-rh/bin/python`
**Write scope:** this file only.

## 0. Verdict

The target

\[
 |\phi_q(s)-\phi_\theta(s)|\ll_{\sigma,|s|}q^{1-2\sigma},
 \qquad 1<\sigma<\frac32,
 \tag{RATE}
\]

is **CONJECTURAL**.  None of the three proposed mechanisms proves the missing
factor \(q^{-1}\).

1. **(A) DRIFT WEIGHTING does not close RATE.**  The \(q^{-2}\) parameter
   drift applies only to paired terms.  Balanced-section overflow is unpaired,
   so it carries its full positive mass.  Even under favorable extra
   comparison hypotheses, optimizing the shallow/deep split with Ford plus the
   sharp no-wrap law returns \(q^{2-2\sigma}\), exactly one power short.
2. **(B) EQUIDISTRIBUTION/SECOND MOMENT is refuted for the present absolute
   majorant.**  The residue weights are nonnegative and the raw theta weight is
   constant on a complete \(d\bmod c\) fiber.  Cauchy--Schwarz is equality on
   such a fiber and is worse globally.  A large sieve can help only after a new
   signed, mean-zero reorganization before absolute values.
3. **(C) GEOMETRIC DIFFERENCE DENSITY is the data-selected future route, but
   remains CONJECTURAL.**  Exact theta canonicalization agrees on all 263 keys
   at \(X=50\); the finite-\(q\) Route-B image covers 164 through 260 of them
   over \(q=8,\ldots,48\).  A moving-window census has overflow count
   essentially linear in \(q\) when \(Y=uq\).  This is striking support for
   `(FW)` below, not an asymptotic proof.  The shared parabolic alone does not
   imply transversality because the finite elliptic relator creates endpoint
   collisions.

The strongest proved/paper-level statement reached on this obstruction is the
already-confirmed raw overflow theorem

\[
 \boxed{
 E_{\rm wrap}(q,\sigma)
 \le \frac{\sigma}{\sigma-1}q^{2-2\sigma}.}
 \tag{0.1}
\]

This is a theorem about the unpaired complement, not a full weak RATE theorem:
the full matched drift still needs the comparison-weighted depth law `(DH)`
and a proved interval derivative envelope.  Consequently it would be false to
claim that a complete bound
\(\epsilon(q)\ll q^{2-2\sigma}\) is presently proved.

The exact lemma still missing is a renewal/first-overflow count such as

\[
 \boxed{
 A_{{\rm wrap},q}(Y)
 \le C_1\frac{Y^2}{q}
       \bigl(1+\log_+(Y/q)\bigr),\qquad Y\ge q.}
 \tag{FW}
\]

Together with the already isolated comparison-weighted depth law `(DH)`, this
would prove RATE with no external \(\log q\) loss.  Both remain **CONJECTURAL**
(`M1_ROUTE_B_REPAIR_SOL.md:963-1055`).

## 1. Exact object and the theorem that is actually proved

Put \(p=2\sigma>2\).  For a finite Route-B class \(X\), write

\[
 x_X=|c_q(X)|,\qquad y_X=|c_\theta(L_qX)|,qquad
 m_X=\min(x_X,y_X),
\]

and let \(k_X\) be the \(Q\)-depth used in P2/P3.  The repaired structural
decomposition is

\[
 D_q(s)-D_\theta(s)
 =\sum_{X\in\mathcal C_q}(x_X^{-2s}-y_X^{-2s})
  -\sum_{H\notin\operatorname{im}L_q}y_H^{-2s}.
 \tag{1.1}
\]

Route B is injective on every nontrivial finite class, so there is no
finite-side unmatched mass (`M1_ROUTE_B_REPAIR_SOL.md:808-825`).  The second
sum is the exact balanced-section overflow complement.

For a matched pair, P2--P5 give, subject to the stated derivative envelope,

\[
 |x_X^{-2s}-y_X^{-2s}|
 \le 2|s|A(2-\lambda_q)
      k_X^2\frac{x_X}{m_X}m_X^{-p}.
 \tag{1.2}
\]

The comparison factor \(x_X/m_X\) is load-bearing; deleting it rounds the
bound down (`M1_ROUTE_B_REPAIR_SOL.md:828-862`).

For an omitted theta class, Route B proves \(y_H\ge q\).  The Ford cylinder
count gives

\[
 A_{{\rm wrap},q}(Y)=0\quad(Y<q),\qquad
 A_{{\rm wrap},q}(Y)\le Y^2.
\]

Stieltjes summation, including a possible atom at \(Y=q\), then gives

\[
\begin{aligned}
 E_{\rm wrap}(q,\sigma)
 &=p\int_q^\infty A_{{\rm wrap},q}(t)t^{-p-1}\,dt\\
 &\le p\int_q^\infty t^{1-p}\,dt
 =\frac{p}{p-2}q^{2-p}
 =\frac{\sigma}{\sigma-1}q^{2-2\sigma}.
\end{aligned}
\tag{1.3}
\]

This reproduces the paper-level derivation at
`M1_ROUTE_B_REPAIR_SOL.md:866-902`, using the Ford count proved at
`M2_FORD_PACKING_REFEREE.md:81-145`.

**FALSE target:** “first-wrap support \(y\ge q\), Ford, and the matched drift
factor already imply \(q^{1-2\sigma}\).”
**NEGATION:** Ford gives (1.3), \(q^{2-2\sigma}\).  The drift factor does not
multiply the unpaired sum.
**CORRECTED version:** RATE follows conditionally from the separate `(FW)` and
`(DH)` counts, not from support plus Ford.

## 2. Mechanism A — drift weighting and the honest split

### 2.1 Falsification experiment

The stored R2 drift receipt uses the same-word endpoint pairing at \(X=50\),
depth at most 12.  I re-read it and fitted the aggregate drift only; the window
repair adds unmatched theta keys but does not change these matched drift rows.

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
import json,math
p='research_notes/rh_goals_2026-08-14/lane_g/law_probes/r2_drift_data.json';d=json.load(open(p));xy=[]
print('q matched kmax drift drift*q^1.2')
for q in (12,16,24,32,48):
 r=d['per_q'][str(q)];v=r['drift_sum'];xy.append((math.log(q),math.log(v)))
 print(q,r['n_matched'],r['kmax_matched'],f'{v:.12g}',f'{v*q**1.2:.9g}')
mx=sum(x for x,y in xy)/len(xy);my=sum(y for x,y in xy)/len(xy)
s=sum((x-mx)*(y-my) for x,y in xy)/sum((x-mx)**2 for x,y in xy)
print('fixed_X50_loglog_slope=',f'{s:.12f}')
PY
```

Output:

```text
q matched kmax drift drift*q^1.2
12 204 7 0.33362147409 6.5806909
16 224 9 0.204971615242 5.71002096
24 236 12 0.101236927695 4.58767292
32 237 12 0.0480531570454 3.07540205
48 237 12 0.0187250243713 1.94944899
fixed_X50_loglog_slope= -2.081939267215
```

This is the expected fixed-window \(q^{-2}\)-like behavior: the depth is
capped.  It is **MEASURED**, not evidence for the moving full series.  The
Chebyshev family already shows why a moving depth range can lose one power:
its contribution is

\[
 q^{-2}\sum_{k<q}k^{2-p}\asymp q^{1-p}.
\]

### 2.2 Split optimization

Give the method every favorable input: assume the P2/P3 envelope in (1.2), a
uniform comparison \(x_X/m_X=O(1)\), and use a cutoff \(X\asymp q\).  Split at
\(K=q^a\), \(0\le a\le1\).

- Shallow terms \(k\le K\): the full Ford mass is bounded for \(p>2\), so
  (1.2) gives \(O(q^{-2}K^2)=O(q^{-2+2a})\).
- In the pre-half deep range, the referee-confirmed no-wrap law gives
  \(m_X\gg k_X\).  Ford applied to the positive \(k^2m^{-p}\) majorant up to
  height \(q\) gives \(O(q^{4-p})\), hence drift \(O(q^{2-p})\).
- Beyond the half-window the sine envelope turns over, so this argument
  supplies no stronger global bound.
- Independently, the unpaired overflow is already (1.3).

Thus, even on the favorable controlled part, the displayed upper bound has
exponent

\[
 \max\{-2+2a,\,2-p\},
\]

whose optimum is \(2-p=2-2\sigma\), not \(1-p\).  The uncontrolled
beyond-half matched range cannot improve that conclusion into a full upper
bound.

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
print('model=Ford+no-wrap drift split; X=q; K=q^a, 0<=a<=1')
print('shallow exponent=-2+2a; deep/tail exponent=2-2sigma')
for sigma in (1.10,1.25,1.49,1.50):
 d=2-2*sigma;t=1-2*sigma
 vals=[max(-2+2*a,d) for a in (0,.25,.5,.75,1)]
 print(f'sigma={sigma:.2f} deep={d:.3f} target={t:.3f} totals={vals} best={min(vals):.3f} gap={d-t:.3f}')
PY
```

Output:

```text
model=Ford+no-wrap drift split; X=q; K=q^a, 0<=a<=1
shallow exponent=-2+2a; deep/tail exponent=2-2sigma
sigma=1.10 deep=-0.200 target=-1.200 totals=[-0.20000000000000018, -0.20000000000000018, -0.20000000000000018, -0.20000000000000018, 0] best=-0.200 gap=1.000
sigma=1.25 deep=-0.500 target=-1.500 totals=[-0.5, -0.5, -0.5, -0.5, 0] best=-0.500 gap=1.000
sigma=1.49 deep=-0.980 target=-1.980 totals=[-0.98, -0.98, -0.98, -0.5, 0] best=-0.980 gap=1.000
sigma=1.50 deep=-1.000 target=-2.000 totals=[-1.0, -1.0, -1.0, -0.5, 0] best=-1.000 gap=1.000
```

This does not prove that the true matched sum is as large as
\(q^{2-2\sigma}\); it proves that the proposed Ford/no-wrap positive-majorant
argument does not recover the missing power.  Without `(DH)` and the comparison
factor control, even a full weak matched theorem is still **CONJECTURAL**.

## 3. Mechanism B — residue equidistribution and second moment

### 3.1 Falsification experiment

At conjugated theta height \(C=2c_H\), the exact fiber has
\(\varphi(C)=\varphi(2c_H)\) keys.  I checked all 25 fibers in the exact
263-key window and compared the positive \(L^1\) mass with its Cauchy--Schwarz
upper bound.

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
import json,math
from collections import defaultdict
p='research_notes/rh_goals_2026-08-14/lane_g/law_probes/r1_coset_enum_complete_X50.json';x=json.load(open(p));fib=defaultdict(list)
for z in x['groups']['inf']['cosets']:fib[round(float(z['c_abs']))].append(round(float(z['d_mod_c'])))
def phi(n):
 o=n;a=n;p=2
 while p*p<=a:
  if a%p==0:
   o=o//p*(p-1)
   while a%p==0:a//=p
  p+=1
 if a>1:o=o//a*(a-1)
 return o
print('theta_n=',sum(map(len,fib.values())),'fibers=',len(fib),'exact=',all(len(v)==phi(C) for C,v in fib.items()))
for X in (10,20,30,40,50):
 a=[C**(-2.2) for C,v in fib.items() if C<=X for _ in v];N=len(a);L1=sum(a);L2=sum(t*t for t in a);CS=math.sqrt(N*L2)
 print(f'X={X} N={N} L1={L1:.10g} L2={L2:.10g} CS={CS:.10g} ratio={CS/L1:.6f}')
PY
```

Output:

```text
theta_n= 263 fibers= 25 exact= True
X=10 N=13 L1=0.417666571 L2=0.053191203 CS=0.831556155 ratio=1.990957
X=20 N=45 L1=0.4919460681 L2=0.05339028603 CS=1.550020281 ratio=3.150793
X=30 N=95 L1=0.5320507476 L2=0.05342426273 CS=2.252843749 ratio=4.234265
X=40 N=173 L1=0.562025977 L2=0.05343614674 CS=3.040469271 ratio=5.409838
X=50 N=263 L1=0.5817886021 L2=0.05344055826 CS=3.748982105 ratio=6.443891
```

The exact fiber identity agrees with the machine theorem
`theta_coset_count` (`RateCoreII.lean:159-214`).  Cauchy--Schwarz worsens the
positive bound by a factor rising from 1.99 to 6.44 on these windows.

### 3.2 Rigorous obstruction

Let \(R_C\) be one exact residue fiber and take a constant nonnegative weight
\(a_{C,d}=a_C\), as in the raw theta mass.  Then

\[
 \sum_{d\in R_C}|a_{C,d}|=\varphi(C)a_C,
\]

while fiberwise Cauchy--Schwarz gives equality:

\[
 \sqrt{\varphi(C)\sum_{d\in R_C}a_C^2}
 =\varphi(C)a_C.
\]

Fourier expansion does not help.  Parseval includes the zero mode

\[
 \widehat a_C(0)=\sum_{d\in R_C}a_C=\varphi(C)a_C,
\]

which is exactly the RATE mass.  Large-sieve and Ramanujan-sum estimates
control oscillatory modes; they do not erase \(h=0\).  For the matched drift,
the depth can vary with \(d\), but equidistribution alone supplies neither a
mean-zero condition nor a favorable correlation with that depth.

**FALSE target:** “exact equidistribution of \(d\bmod C\) supplies a
square-root, hence \(q^{-1}\), gain.”
**NEGATION:** the relevant majorant is nonnegative and contains its full zero
mode; Cauchy--Schwarz is equality for constant fiber weights.
**CORRECTED version:** a large-sieve route would require a new signed
fiberwise formula for the complex difference, a proved mean-zero condition,
and uniform control before taking absolute values.  That would be a different
RATE proof, and is presently **CONJECTURAL**.

## 4. Mechanism C — exact difference census and geometric route

### 4.1 Correct difference object

Route B changes the geometry of the question.  Every nontrivial finite class
has a theta image under the balanced section.  The actual difference set is

\[
 \mathcal H_\theta\setminus\operatorname{im}L_q
 =\{\text{theta canonical words with an }R\text{-exponent outside }
       \mathcal A_q\},
\]

where

\[
 \mathcal A_q={-\lfloor(q-1)/2\rfloor,\ldots,-1,
                  1,\ldots,\lfloor q/2\rfloor\}.
\]

Thus “near a theta coset” is not a metric nearest-neighbor problem.  It is an
exact same-canonical-word pairing, followed by the P3 drift inequality.  The
common two-sided window count below requires both \(y\le50\) and the finite
replay \(x\le50\); it deliberately does not claim to enumerate every finite
class with \(x\le50\) whose theta lift lies outside the 263-key target.

### 4.2 Exact canonical census and finite replay, \(q=8,\ldots,48\)

I reconstructed the theta canonical \(R,Q\) word from each exact Hejhal pair
\((c_H,d_H)\) using the centered Euclidean recurrence and the proved boundary
reductions.  Independent canonicalization of the JSON witness word agreed on
all 263 keys.  The moving census uses the exact arithmetic key condition
\(0\le d<2c\), \((c,d)=1\), \(c+d\) odd, through \(c_H=384\).

Command (stdout only):

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
import json,math
from math import gcd,log
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
def from_qs(word):
 t=[('Q',1)]
 for n in word:t+=([('Q',1),('R',1)]*n if n>0 else [('R',-1),('Q',1)]*(-n))+[('Q',1)]
 return canon(t)
def mm(A,B):return [[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def inv(A):return [[A[1][1],-A[0][1]],[-A[1][0],A[0][0]]]
def pw(A,n):
 if n<0:return pw(inv(A),-n)
 Z=[[mp.mpf(1),0],[0,mp.mpf(1)]]
 while n:
  if n&1:Z=mm(Z,A)
  A=mm(A,A);n//=2
 return Z
def c_eval(w,lam):
 Q=[[0,-1/lam],[lam,0]];R=mm(Q,[[1,1],[0,1]]);M=[[mp.mpf(1),0],[0,mp.mpf(1)]]
 for z in w:M=mm(M,Q if z=='Q' else pw(R,z))
 return abs(M[1][0])
P='research_notes/rh_goals_2026-08-14/lane_g/law_probes/r1_coset_enum_complete_X50.json';J=json.load(open(P));theta=J['groups']['inf']['cosets']
mis=0
for z in theta:
 c=round(float(z['c_abs'])/2);d=round(float(z['d_mod_c']))
 mis+=from_cd(c,d)!=from_qs(z['word'])
print('JSON_theta=',len(theta),'canonical_integer_crosscheck_mismatch=',mis)
rec=[]
for c in range(1,385):
 for d in range(2*c):
  if gcd(c,d)==1 and (c+d)%2:rec.append((c,from_cd(c,d)))
print('exact_keys_cH_le_384=',len(rec))
print('q image_y<=50 both_x_y<=50 omitted_y<=50')
for q in range(8,49):
 A=set(range(-((q-1)//2),0))|set(range(1,q//2+1));lam=2*mp.cos(mp.pi/q)
 im=[(c,w) for c,w in rec if c<=25 and all(z=='Q' or z in A for z in w)]
 both=sum(c_eval(w,lam)<=50 for c,w in im)
 print(q,len(im),both,263-len(im))
print('moving Y=u*q: u slope_log_A_vs_log_q max[A*q/(Y^2*(1+log u))]')
for u in (2,4,8,16):
 xy=[];norm=[]
 for q in range(8,49):
  A=set(range(-((q-1)//2),0))|set(range(1,q//2+1));Y=u*q
  n=sum(1 for c,w in rec if 2*c<=Y and any(z!='Q' and z not in A for z in w))
  xy.append((math.log(q),math.log(n)));norm.append(n*q/(Y*Y*(1+log(u))))
 xb=sum(x for x,y in xy)/len(xy);yb=sum(y for x,y in xy)/len(xy)
 slope=sum((x-xb)*(y-yb) for x,y in xy)/sum((x-xb)**2 for x,y in xy)
 print(u,f'{slope:.6f}',f'{max(norm):.6f}')
PY
```

Output:

```text
JSON_theta= 263 canonical_integer_crosscheck_mismatch= 0
exact_keys_cH_le_384= 59931
q image_y<=50 both_x_y<=50 omitted_y<=50
8 164 164 99
9 181 181 82
10 190 190 73
11 199 199 64
12 204 204 59
13 209 209 54
14 214 214 49
15 219 219 44
16 223 223 40
17 227 227 36
18 229 229 34
19 231 231 32
20 232 232 31
21 233 233 30
22 234 234 29
23 235 235 28
24 236 236 27
25 237 237 26
26 238 238 25
27 239 239 24
28 240 240 23
29 241 241 22
30 242 242 21
31 243 243 20
32 244 244 19
33 245 245 18
34 246 246 17
35 247 247 16
36 248 248 15
37 249 249 14
38 250 250 13
39 251 251 12
40 252 252 11
41 253 253 10
42 254 254 9
43 255 255 8
44 256 256 7
45 257 257 6
46 258 258 5
47 259 259 4
48 260 260 3
moving Y=u*q: u slope_log_A_vs_log_q max[A*q/(Y^2*(1+log u))]
2 0.952072 0.166111
4 0.971684 0.124408
8 0.980461 0.109725
16 0.992744 0.100437
```

The canonical image/omitted columns and the moving-overflow counts are exact
integer counts within the stated finite boxes.  The `both_x_y<=50` column is a
50-digit `mpmath` replay diagnostic, not an interval certificate; it happens
to equal the exact image count in every displayed row.  For the moving
windows, the observed overflow exponent is 0.95--0.99 in \(q\), while the full
theta population at \(Y=uq\) is quadratic.  The largest displayed normalized
ratio is below the safely rounded-up empirical ceiling 0.167.  This is
precisely the shape of `(FW)`.

### 4.3 Why this is not yet a proof

1. Fixed \(X=50\) saturates: for \(q>50\) the complement in this window must
   vanish.  Its excellent decrease is not a \(q\to\infty\) rate theorem.
2. The moving experiment covers only \(q\le48\), \(Y/q\le16\).  Finite exact
   computation cannot prove a uniform tail.
3. The relation \(R^q=(QS)^q=1\) identifies distinct theta words after finite
   specialization.  For example, \(Q\) and \(R^qQ\) are the same finite class
   but distinct theta classes.  Thus an unsectioned “endpoint closeness” or
   generic-transversality argument is false; the balanced section is essential.
4. A shell count derived only from
   \(|x-y|\le(\pi^2/q^2)\sup|c'_w|\) still inherits the uncontrolled depth.
   With the crude \(\sup|c'_w|\sim k^2c\), it does not yield `(FW)`.

**FALSE target:** “the shared parabolic and angular separation alone imply a
\(1/q\)-sparse difference set.”
**NEGATION:** the finite relator creates nontransverse endpoint collisions, and
fixed-window shell fits are not asymptotics.
**CORRECTED version:** the data supports a first-large-balanced-digit renewal
theorem.  Proving `(FW)` requires a cylinder/continued-fraction count with the
first overflow digit marked and the relative \(\log(Y/q)\) retained.

## 5. What `(FW)` would give

If `(FW)` holds, then Stieltjes summation gives, with \(p=2\sigma\),

\[
\begin{aligned}
E_{\rm wrap}(q,\sigma)
&\le \frac{pC_1}{q}
 \int_q^\infty t^{1-p}\bigl(1+\log(t/q)\bigr)\,dt\\
&=pC_1q^{1-p}
 \left(\frac1{p-2}+\frac1{(p-2)^2}\right).
\end{aligned}
\tag{5.1}
\]

There is no external \(\log q\): substituting \(t=qu\) absorbs the relative
logarithm.  If the only provable count instead had an external \(\log q\), the
honest conclusion would be \(q^{1-2\sigma}\log q\), which would still decay
for \(\sigma>1/2\) but would not be the stated RATE theorem.

For the matched sum one still needs

\[
B_q(Y):=
\sum_{m_X\le Y}k_X^2\frac{x_X}{m_X}
\le C_0Y^2\min(Y,q)\bigl(1+\log_+(Y/q)\bigr).
\tag{DH}
\]

Then (1.2) gives \(q^{1-p}\) for the matched drift.  The current experiment
supports `(FW)` only; it does not prove `(DH)` or the interval derivative
envelope.

## 6. R5 consequence of the best presently supported power

Let a hypothetical full weak RATE bound have exponent

\[
 \alpha_{\rm weak}=2\sigma_R-2.
\]

At the working line \(\sigma_R=1.1\), \(\alpha_{\rm weak}=0.2>0\).  R5's
conditional algebra gives

\[
 p_3=0.2\,\nu_{\rm seed}\omega_*>0,
\qquad
 q_C=\left\lfloor
 \left(\frac{C_3}{d_\delta}\right)^{1/p_3}
 \right\rfloor+1.
\tag{6.1}
\]

Therefore the weak power would still eventually beat every proved continuous
defect \(d_\delta>0\).  The pincer does **not** fail asymptotically; its onset
can become enormous.

To isolate exponent sensitivity, retain exactly R5's explicitly
counterfactual regime-iii constants

\[
C_R=2,\quad K_+=K_F=1,\quad
\nu_{\rm seed}=\omega_*=\frac12,\quad d_\delta=0.6604.
\]

The defect is rounded down as in R5.  Command:

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from decimal import Decimal,getcontext
getcontext().prec=50
C3=Decimal(2)**(Decimal(1)/4);d=Decimal('0.6604')
for alpha in (Decimal('1.2'),Decimal('.2')):
 p=alpha/4;cross=(C3/d)**(Decimal(1)/p)
 print('alpha',alpha,'C3',C3,'p3',p,'crossing',cross,'N_C',int(cross)+1)
PY
```

Output:

```text
alpha 1.2 C3 1.1892071150027210667174999705604759152929720924638 p3 0.3 crossing 7.1039753815850701568908458039140465938357930399919 N_C 8
alpha 0.2 C3 1.1892071150027210667174999705604759152929720924638 p3 0.05 crossing 128531.23677544274806585332307521414834854725027808 N_C 128532
```

Thus the same optimistic model changes the contradiction crossing from 8 to
**128,532**; with the model's prerequisite 24, its counterfactual
\(N_0\) is also 128,532.  This is **CONJECTURAL / COUNTERFACTUAL**, not an
effective theorem threshold.  In the proved/paper-level-only regime the
effective \(N_0\) remains undefined: a full weak RATE constant, continuous
R4 defect, transport constants, monotonicity, and activation gates are not
numerically certified (`R5_ASSEMBLY_EXECUTION_SOL.md:148-225,320-337`).

## 7. Final claim ledger

| Claim | Verdict | Reason |
|---|---|---|
| P2/P3/P5 supply a \(q^{-2}\) drift on each matched term | **PROVED at the stated paper/machine level** | Product rule, mean value, \(2-\lambda_q\le\pi^2/q^2\); the global interval envelope remains a separate hypothesis. |
| Drift weighting alone proves RATE | **FALSE as a proof route** | It does not act on the unpaired complement; the favorable split still returns \(q^{2-2\sigma}\). |
| Exact residue-fiber counting gives a second-moment \(q^{-1}\) gain | **FALSE for the current positive majorant** | Zero mode survives; fiberwise Cauchy--Schwarz is equality. |
| Generic parabolic transversality proves density \(1/q\) | **FALSE as stated** | The finite elliptic relator creates collisions; a canonical section and renewal count are required. |
| Raw overflow mass is \(O(q^{2-2\sigma})\) | **PROVED / paper-level confirmed** | Equation (1.3). |
| `(FW)` has the correct scale | **MEASURED, strongly supported** | Slopes fitted from exact integer counts are 0.95--0.99, with normalized ratios below 0.167 on the tested box. |
| `(FW)` and `(DH)` hold uniformly | **CONJECTURAL** | No renewal/cylinder proof is present. |
| Full RATE \(q^{1-2\sigma}\) | **CONJECTURAL** | Exactly `(FW)`, `(DH)`, and the interval envelope remain. |
| A full weak \(q^{2-2\sigma}\) RATE theorem | **CONJECTURAL** | Only the raw complement theorem is proved; matched comparison/depth control remains open. |
| Weak exponent would beat any proved \(d_\delta>0\) | **PROVED conditional algebra** | Any \(\alpha>0\) survives transport if \(\nu_{\rm seed}\omega_*>0\); 0.6604 and the displayed 128,532 are counterfactual sensitivity inputs only. |

**Data-selected next attack:** prove `(FW)` by coding the first balanced
\(R\)-digit outside \(\mathcal A_q\) and counting the associated theta
continued-fraction cylinders.  A valid proof must be uniform in the moving
ratio \(Y/q\), must retain first-overflow uniqueness to avoid a word-length
union-bound loss, and must be paired with `(DH)` for the matched sum.  Until
then, the last \(q^{-1}\) density gain is open.

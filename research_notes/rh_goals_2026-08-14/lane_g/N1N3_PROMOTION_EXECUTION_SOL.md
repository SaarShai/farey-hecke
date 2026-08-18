# (RATE) N1--N3 promotion execution

**Date:** 2026-08-18

**Scope:** execution of §§3--5 of `M3_N1N4_PROMOTION_PLAN_SOL.md`.

**Status convention:** `PROVED` below means a complete paper proof is written
here or in the cited source.  `MACHINE-VERIFIED` is used only for a checked Lean
theorem.  Every remaining unproved mathematical assertion is marked
`CONJECTURAL`.  Finite program output is not promoted to a theorem.

## 0. Verdict ledger

| Gap | Verdict | Corrected endpoint |
|---|---|---|
| N1-strong | **REFUTED** | No finite constant independent of $q$ can hold over every syntactically reduced $Q,S$-word. |
| N1-RATE | **CONJECTURAL with $A=11/20$** | Restrict to the canonical representative supplied by corrected coset-level M1. |
| N2-finite as stated | **REFUTED** | The depth-$\le12$ theta target has 237 emitted keys but the complete $|C|\le50$ theta window has 263 cosets; an explicit missing target has theta depth 13. |
| N2-global | **CONJECTURAL** | This is the surjectivity/localization part of corrected M1, not an independent numerical promotion. |
| N3-shell | **CONJECTURAL; retired from RATE** | Ford packing does not prove the empirical factor-two shell contraction. |
| N3 absolute RATE tail | **PROVED at paper level; Lean formalization open** | With independent truncations, the full two-sided remainder is at most $\frac{2\sigma}{\sigma-1}X^{2-2\sigma}$; $X(q)=q^6$ gives at most $22q^{1-2\sigma}$ on $11/10\le\sigma\le5/4$. |

The Ford status is not upgraded beyond `M2_FORD_PACKING_REFEREE.md:1-6`:
the packing and tail argument are confirmed at paper level, while Lean
formalization remains open.  Likewise, the Chebyshev $c$-identity is
machine-verified, but the derivative-at-two formula below is paper algebra;
see `LAW_R2_RATE_LEMMA_DRAFT.md:168-181`.

## 1. N1 -- the universal derivative envelope is false

### 1.1 Exact counterexample family

Let

\[
 w_m=(1,\ldots,1),\qquad k_w=m,
\]

where the exponent list has $m-1$ entries.  Every exponent is nonzero, so
this is a reduced word under the literal word domain at
`LAW_R2_RATE_LEMMA_DRAFT.md:128-133`.  The machine-verified Chebyshev identity
(`projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle/RateCore.lean:271-345`)
is

\[
 c_{w_m}(\lambda)=\lambda U_{m-1}(\lambda/2)
 =\lambda\frac{\sin(m\theta)}{\sin\theta},
 \qquad \lambda=2\cos\theta.
\]

Differentiating this polynomial identity and using
$U_{m-1}(1)=m$ and
$U'_{m-1}(1)=m(m^2-1)/3$ gives, by paper algebra,

\[
 c'_{w_m}(2)=m+\frac{m^3-m}{3}=\frac{m(m^2+2)}3.
\]

Set $m=q-1$.  Then

\[
 c_{w_{q-1}}(\lambda_q)
 =\lambda_q\frac{\sin((q-1)\pi/q)}{\sin(\pi/q)}
 =\lambda_q\ne0.
\]

Consequently

\[
 \frac{\sup_{\lambda\in[\lambda_q,2]}|c'_{w_{q-1}}(\lambda)|}
      {(q-1)^2|c_{w_{q-1}}(\lambda_q)|}
 \ge
 \frac{(q-1)^2+2}{3(q-1)\lambda_q}
 >\frac{(q-1)^2+2}{6(q-1)}\longrightarrow\infty.
\]

Thus **no finite universal $C$** works on the literal all-word domain; in
particular $C=11/20$ is false.  For the single exact witness $q=12,m=11$,

\[
 \sup|c'|\ge451,
 \qquad
 \frac{11}{20}m^2|c(\lambda_{12})|
 <\frac{11}{20}\,121\,2=\frac{1331}{10}<451.
\]

P2 and P3 cannot repair this.  P2 is the product-rule identity for $Q'$, and
P3 bounds endpoint drift *by* the derivative supremum.  Neither supplies a
representation-stable lower bound for $|c_w(\lambda_q)|$.

The failure is exactly a normal-form failure.  Put $R=QS$.  In PSL,
$R^q=1$, $S=QR$, and $w_{q-1}=R^{q-2}Q$.  Hence

\[
 S w_{q-1} S=(QR)R^{q-2}(QS)=Q R^q=Q.
\]

The bad long word is the same double coset as the depth-one word $Q$.  A
coset derivative bound therefore must first fix a canonical representative.

### 1.2 Fresh exact/Arb counterexample receipt

Command run from the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from fractions import Fraction
from flint import arb, ctx
ctx.prec=160
for q in (12,16,24,32,48):
    m=q-1
    lam=2*(arb.pi()/q).cos()
    deriv2=m+(m**3-m)//3
    ratio=arb(deriv2)/(arb(m*m)*lam)
    print(f'q={q} m={m} cprime_at_2={deriv2} ratio={ratio}')
m=11
lower=Fraction(m*m+2,6*m)
print(f'q=12 exact_lower={lower} compare_11_over_20={lower > Fraction(11,20)}')
PY
```

Output:

```text
q=12 m=11 cprime_at_2=451 ratio=[1.9293783362187911375099731531974511749657863553 +/- 8.60e-48]
q=16 m=15 cprime_at_2=1135 ratio=[2.5716354768143140299960074556720126312434310592 +/- 2.16e-47]
q=24 m=23 cprime_at_2=4071 ratio=[3.8810288265801528601625665074677430097796419833 +/- 4.35e-47]
q=32 m=31 cprime_at_2=9951 ratio=[5.2024706731096123054595518802877037456654345933 +/- 2.31e-47]
q=48 m=47 cprime_at_2=34639 ratio=[7.8572485040955299155365973868969782307460099247 +/- 3.23e-47]
q=12 exact_lower=41/22 compare_11_over_20=True
```

The displayed Arb balls are outward-rounded cross-checks.  The refutation
itself is the exact inequality above and does not depend on their decimal
values.

### 1.3 The previously untested escaping population

The current $X=50$, depth-$\le12$ program emits 246 escaping
representatives over $q\in\{12,16,24,32,48\}$.  For every emitted escaping
word, the following run enclosed $c'_w$ over the whole interval
$[\lambda_q,2]$ by 512 Arb subintervals and divided an outward-rounded upper
bound by a lower bound for $k^2|c_w(\lambda_q)|$.

This certifies the continuous derivative inequality for the **emitted word
list**, conditional on the program's numerical escaping classification.  It
does not certify completeness of the BFS population or exactness of its
floating canonical keys (`r1_coset_enum.py:17-25,87-127`).

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research_notes/rh_goals_2026-08-14/lane_g/law_probes /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import arb, ctx
from mpmath import mp
import r2_drift as d
ctx.prec=160; mp.dps=80
Z=arb(0); O=arb(1)
def mm(A,B):
 return [[sum((A[i][k]*B[k][j] for k in range(2)),Z) for j in range(2)] for i in range(2)]
def add(A,B):
 return [[A[i][j]+B[i][j] for j in range(2)] for i in range(2)]
def cd_ball(word,x):
 Q=[[Z,-O/x],[x,Z]]; DQ=[[Z,O/(x*x)],[O,Z]]
 M=Q; D=DQ
 for n in word:
  S=[[O,arb(n)],[Z,O]]
  M,D=mm(M,S),mm(D,S)
  M,D=mm(M,Q),add(mm(D,Q),mm(M,DQ))
 return M[1][0],D[1][0]
def interval(a,b):
 return arb((a+b)/2,(b-a)/2)
X=mp.mpf(50); depth=12; slabs=512
th,_=d.enumerate_with_words(None,X,depth); thkeys=set(th)
for q in (12,16,24,32,48):
 lam_ball=2*(arb.pi()/q).cos(); lo=lam_ball.lower(); hi=arb(2).upper()
 found,_=d.enumerate_with_words(q,X,depth); claimed=set(); esc=[]
 for key,(ac,w,M) in sorted(found.items(),key=lambda kv:kv[1][0]):
  tk,ct=d.theta_key(w,X)
  if tk is not None and tk in thkeys and tk not in claimed:
   claimed.add(tk); continue
  cq,_=cd_ball(w,lam_ball); cqlo=cq.abs_lower(); du=None
  for j in range(slabs):
   a=lo+(hi-lo)*j/slabs; b=lo+(hi-lo)*(j+1)/slabs
   _,db=cd_ball(w,interval(a,b)); u=db.abs_upper()
   if du is None or u>du: du=u
  ratio=arb(du)/(arb((len(w)+1)**2)*arb(cqlo))
  esc.append((ratio.upper(),ratio,w,cq,ct,len(w)+1))
 e=max(esc,key=lambda z:z[0])
 print(f'q={q} escaping={len(esc)} certified_A_upper={e[1]} k={e[5]} c_q={e[3]} c_theta={e[4]} word={e[2]} slabs={slabs}')
PY
```

Output:

```text
q=12 escaping=114 certified_A_upper=[0.26794919243119559679278347083530793613351029135 +/- 4.78e-48] k=2 c_q=[-48.516660498395404815856802439576340770256468299 +/- 5.84e-46] c_theta=52.0 word=(-13,) slabs=512
q=16 escaping=72 certified_A_upper=[0.24700051916807886630936242861465844392016797882 +/- 3.36e-48] k=9 c_q=[49.3074057346688408974388772387837757710255508 +/- 8.59e-44] c_theta=82.0 word=(-3, -1, -1, -1, -1, -1, -1, -1) slabs=512
q=24 escaping=40 certified_A_upper=[0.23389880296379631078378700545770120324463113756 +/- 3.57e-48] k=12 c_q=[-45.056886586145861118460717167280674368172410 +/- 4.67e-43] c_theta=68.0 word=(-2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1) slabs=512
q=32 escaping=16 certified_A_upper=[0.17801239690046972532234477057732454369174620563 +/- 3.08e-48] k=10 c_q=[-48.1269618465486334509776125146298188567670422 +/- 9.29e-44] c_theta=56.0 word=(-2, -1, -1, -1, -1, -1, -1, -1, -1) slabs=512
q=48 escaping=4 certified_A_upper=[0.14100587331790761766521843322141986142714178744 +/- 2.14e-48] k=10 c_q=[-49.0899125529479649515391462816770703298372897 +/- 6.94e-44] c_theta=52.0 word=(-1, 1, 1, 1, 1, 1, 1, 1, 1) slabs=512
```

No displayed upper endpoint reaches $11/20$.  This closes the omitted
finite escaping-word test, but it does **not** rescue N1-strong: the exact
near-relation family lies outside the chosen canonical representatives.

### 1.4 Corrected N1 statement

> **N1-RATE -- CONJECTURAL with explicit constant $A=11/20$.**  For every
> $q\ge12$ and every canonical representative $w_{\rm can}$ of an
> M1-matched double coset,
> \[
> \sup_{\lambda\in[\lambda_q,2]}|c'_{w_{\rm can}}(\lambda)|
> \le \frac{11}{20}k_{\rm can}^2|c_{w_{\rm can}}(\lambda_q)|.
> \]

This is the strongest current RATE-use formulation.  It remains
`CONJECTURAL` because M1 has not yet supplied the canonical normal-form domain
and no cancellation-stable analytic induction has been proved.  Escaping and
near-relation classes must be bounded by their full masses, not by an
arbitrary-word derivative envelope.

## 2. N2 -- onto matching in the theta window is false as stated

### 2.1 Exact theta target and explicit missing coset

At the theta endpoint every lower-left entry is $C=2n$; this is
`c_two_even`, machine-verified at
`projects/aristotle_dispatch_v27/result/aristotle_dispatch_v27_aristotle/RateCoreII.lean:154-157`.
For fixed $n>0$, `theta_coset_count` at the same file's lines 159--214 proves

\[
 \#\{0\le d<2n:\gcd(n,d)=1,\ n+d\text{ odd}\}=\varphi(2n).
\]

Therefore the complete $|C|\le50$ theta window has exactly

\[
 \sum_{n=1}^{25}\varphi(2n)=263
\]

double cosets, not 237.

There is also a direct normal-form obstruction, requiring no cardinality
argument.  At $\lambda=2$, the all-ones theta word with $m=13$ has depth
13 and bottom row

\[
 (C,D)=(26,-12),\qquad (C,D\bmod C)=(26,14).
\]

Indeed the recurrence from depth $m$ to $m+1$ sends
$(2m,-(m-1))$ to $(2(m+1),-m)$.  The pair is admissible because
$\gcd(13,14)=1$ and $13+14$ is odd.  The theta group is
$\mathbb Z_2*\mathbb Z$, so its reduced double-coset normal form is unique;
this coset has minimum theta depth 13.  Specializing a depth-$\le12$ q-word
to $\lambda=2$ cannot increase its reduced depth.  Hence this target has no
preimage in the proposed depth-$\le12$ source, for either $q=32$ or
$q=48$.  N2-finite is therefore **REFUTED**.

### 2.2 Fresh enumeration/count receipt

The following exact integer target construction was compared with the current
floating BFS output.

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research_notes/rh_goals_2026-08-14/lane_g/law_probes /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from math import gcd
from mpmath import mp
import r2_drift as d
mp.dps=80; X=mp.mpf(50); depth=12
expected={(2*n,r) for n in range(1,26) for r in range(2*n)
          if gcd(n,r)==1 and (n+r)%2==1}
th,_=d.enumerate_with_words(None,X,depth)
got={(int(round(float(k[0]))),int(round(float(k[1])))) for k in th}
missing=sorted(expected-got)
print(f'complete_theta={len(expected)} bfs_theta={len(got)} missing={len(missing)} extra={len(got-expected)}')
print('first_missing=',missing[:8])
for q in (32,48):
    found,_=d.enumerate_with_words(q,X,depth); claimed=set()
    for key,(ac,w,M) in sorted(found.items(),key=lambda kv:kv[1][0]):
        tk,ct=d.theta_key(w,X)
        if tk is not None and tk in th and tk not in claimed: claimed.add(tk)
    print(f'q={q} bfs_source={len(found)} claimed_in_incomplete_theta={len(claimed)} complete_theta={len(expected)} cardinality_deficit={len(expected)-len(found)}')
PY
```

Output:

```text
complete_theta=263 bfs_theta=237 missing=26 extra=0
first_missing= [(26, 12), (26, 14), (28, 13), (28, 15), (30, 14), (30, 16), (32, 15), (32, 17)]
q=32 bfs_source=253 claimed_in_incomplete_theta=237 complete_theta=263 cardinality_deficit=10
q=48 bfs_source=241 claimed_in_incomplete_theta=237 complete_theta=263 cardinality_deficit=22
```

A deeper theta replay reaches the independently proved target cardinality and
shows exactly what the depth-12 comparison omitted.

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research_notes/rh_goals_2026-08-14/lane_g/law_probes /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from mpmath import mp
import r2_drift as d
mp.dps=80; X=mp.mpf(50)
th,_=d.enumerate_with_words(None,X,25)
print('theta_depth25=',len(th))
for q in (32,48):
 found,_=d.enumerate_with_words(q,X,12); claimed=set(); outside=0; collisions=0
 for key,(ac,w,M) in sorted(found.items(),key=lambda kv:kv[1][0]):
  tk,ct=d.theta_key(w,X)
  if tk is None or tk not in th: outside+=1
  elif tk in claimed: collisions+=1
  else: claimed.add(tk)
 print(f'q={q} source_depth12={len(found)} claimed_complete_theta={len(claimed)} unmatched_complete_theta={len(th)-len(claimed)} outside={outside} collisions={collisions}')
PY
```

Output:

```text
theta_depth25= 263
q=32 source_depth12=253 claimed_complete_theta=237 unmatched_complete_theta=26 outside=16 collisions=0
q=48 source_depth12=241 claimed_complete_theta=237 unmatched_complete_theta=26 outside=4 collisions=0
```

The exact theorem supplies the cardinality; depth-25 saturation is only a
fresh numerical cross-check.  The current JSON is not a bijection receipt:
`r2_drift.py:214-233` stores scalar counts and only a truncated
`matched_sample`, not complete source/target key lists and witnesses.

### 2.3 Corrected N2 status

The strongest valid statement about the existing run is:

> **REPLAYED FINITE OBSERVATION.**  Under the current floating
> canonicalization and depth-12 BFS outputs, the greedy procedure claims all
> 237 theta keys emitted by that same incomplete depth-12 theta BFS for
> $q=32,48$.

This is not `CERTIFIED-FINITE`.  Completeness, exact algebraic
canonicalization, and a complete map receipt are absent.

> **N2-global -- CONJECTURAL.**  Surjectivity below a proved cutoff
> $c_*(q)$, together with complement localization, remains exactly the
> corrected coset-level M1 obligation (`LAW_R2_RATE_LEMMA_DRAFT.md:405-425`).

No finite grid promotes that global statement.

## 3. N3 -- replace the shell rule by independent Ford tails

### 3.1 Paper proof of the raw tail

For either the width-one finite Hecke group or the theta endpoint, let

\[
 A_\Gamma(Y)=\#\{[\gamma]\in
 \Gamma_\infty\backslash\Gamma/\Gamma_\infty:
 0<|c_\gamma|\le Y\}.
\]

The Ford-horoball argument in `M2_FORD_PACKING_REFEREE.md:81-126` proves

\[
 A_\Gamma(Y)\le Y^2\qquad(Y\ge1)
\]

with constant one in the PSL double-coset convention.  For
$p=2\sigma>2$, Stieltjes summation with the strict tail gives

\[
 \begin{aligned}
 \sum_{X<|c_\gamma|\le Y}|c_\gamma|^{-p}
 &=Y^{-p}A_\Gamma(Y)-X^{-p}A_\Gamma(X)
   +p\int_X^Y A_\Gamma(t)t^{-p-1}\,dt.
 \end{aligned}
\]

Letting $Y\to\infty$, dropping the nonpositive $X$-boundary, and using
$A_\Gamma(t)\le t^2$ proves, for every $\sigma>1,X\ge1$,

\[
 F_\sigma(X):=
 \sum_{|c_\gamma|>X}|c_\gamma|^{-2\sigma}
 \le\frac{\sigma}{\sigma-1}X^{2-2\sigma}.
\]

The strict $>X$ boundary is essential and exact; an atom at $X$ is
canceled by $-X^{-p}A_\Gamma(X)$.  No integer-grid hypothesis and no N4
multiplicity estimate enter this proof.

### 3.2 Exact R2 replacement

Define the two Dirichlet tails **independently**:

\[
 R_{q,X}(s)=\sum_{[\gamma]_q:\,|c_q|>X}|c_q|^{-2s},
 \qquad
 R_{\theta,X}(s)=\sum_{[\gamma]_\theta:\,|c_\theta|>X}|c_\theta|^{-2s}.
\]

Then, without a matching map,

\[
 \boxed{
 |R_{q,X}(s)-R_{\theta,X}(s)|
 \le \frac{2\sigma}{\sigma-1}X^{2-2\sigma}.}
\]

Indeed, take absolute values termwise and apply the preceding Ford bound once
to each group.  Therefore the full scattering tail satisfies

\[
 \boxed{
 |M(s)|\,|R_{q,X}(s)-R_{\theta,X}(s)|
 \le |M(s)|\frac{2\sigma}{\sigma-1}X^{2-2\sigma}.}
\]

This is the exact N3 statement needed by R2.  It replaces the empirical
$T_X=2\Delta_X^{\rm outer}$; it does not prove that shell rule.

The finite head must be rewritten consistently: include every q-term with
$|c_q|\le X$ and every theta-term with $|c_\theta|\le X$.  A matched pair
with one denominator at most $X$ and the other above $X$ is a
cross-boundary head/escape term and must be charged at full mass on the
appropriate side.  It may not disappear under an ambiguous
`min(c_q,c_theta)<=X` convention.

### 3.3 Explicit growing cutoff

For a fixed $\sigma>1$, the choice

\[
 X_\sigma(q)=
 \left\lceil q^{(2\sigma-1)/(2\sigma-2)}\right\rceil
\]

gives

\[
 \frac{2\sigma}{\sigma-1}X_\sigma(q)^{2-2\sigma}
 \le \frac{2\sigma}{\sigma-1}q^{1-2\sigma}.
\]

Uniformly on the current RATE band $11/10\le\sigma\le5/4$, take the integer
cutoff

\[
 \boxed{X(q)=q^6.}
\]

Since $2\sigma/(\sigma-1)\le22$ and
$12-12\sigma\le1-2\sigma$ on this band, for $q\ge1$

\[
 \boxed{
 \frac{2\sigma}{\sigma-1}X(q)^{2-2\sigma}
 \le22q^{1-2\sigma}.}
\]

Thus N3's full beyond-window contribution has the required RATE exponent,
with an explicit, deliberately crude cutoff.  The other RATE gaps still
govern the independently truncated finite head; this tail result does not
promote M1, N1-RATE, N4-scale, or M3.

### 3.4 Fresh Arb cross-check

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import arb, ctx
ctx.prec=160
for sigma in (arb(11)/10, arb(5)/4):
    C=2*sigma/(sigma-1)
    print('sigma=',sigma,'C_two_sides=',C)
    for q in (12,32,48):
        X=arb(q)**6
        B=C*X**(2-2*sigma)
        R=arb(22)*arb(q)**(1-2*sigma)
        print('q=',q,'X=',X,'B=',B,'22q=',R,'B/22q=',B/R)
PY
```

Output:

```text
sigma= [1.1000000000000000000000000000000000000000000000 +/- 2.47e-48] C_two_sides= [22.000000000000000000000000000000000000000000000 +/- 5.70e-46]
q= 12 X= 2985984.0000000000000000000000000000000000000000 B= [1.1153346268042105586946613652881250701581292269 +/- 7.12e-47] 22q= [1.1153346268042105586946613652881250701581292269 +/- 5.51e-47] B/22q= [1.000000000000000000000000000000000000000000000 +/- 1.15e-46]
q= 32 X= 1073741824.0000000000000000000000000000000000000 B= [0.3437500000000000000000000000000000000000000000 +/- 4.93e-47] 22q= [0.3437500000000000000000000000000000000000000000 +/- 1.04e-47] B/22q= [1.000000000000000000000000000000000000000000000 +/- 1.56e-46]
q= 48 X= 12230590464.000000000000000000000000000000000000 B= [0.2113163963812292796327474133379400658620090822 +/- 3.14e-47] 22q= [0.21131639638122927963274741333794006586200908220 +/- 5.12e-48] B/22q= [1.000000000000000000000000000000000000000000000 +/- 1.68e-46]
sigma= 1.2500000000000000000000000000000000000000000000 C_two_sides= 10.000000000000000000000000000000000000000000000
q= 12 X= 2985984.0000000000000000000000000000000000000000 B= [0.0057870370370370370370370370370370370370370370370 +/- 3.94e-50] 22q= [0.52923774675715695080005304879346100101030160533 +/- 2.22e-48] B/22q= [0.010934664189197457661158120842840103326659124077 +/- 1.28e-49]
q= 32 X= 1073741824.0000000000000000000000000000000000000 B= 0.00030517578125000000000000000000000000000000000000 22q= [0.12153397801643785575639512473677092862708117679 +/- 3.89e-49] B/22q= [0.0025110326036454102429007257177018786906421730742 +/- 3.06e-50]
q= 48 X= 12230590464.000000000000000000000000000000000000 B= [9.0422453703703703703703703703703703703703703704e-5 +/- 3.65e-52] 22q= [0.066154718344644618850006631099182625126287700666 +/- 5.27e-49] B/22q= [0.0013668330236496822076447651053550129158323905096 +/- 4.10e-50]
```

### 3.5 What Ford does not prove

The literal nonnegative matched-drift shell statement

\[
 \sum_{\min(c_q,c_\theta)>X}\delta_w
 \le2\sum_{X/2<\min(c_q,c_\theta)\le X}\delta_w
\]

remains **CONJECTURAL**.  Ford controls unweighted raw mass, not $k^2$ or a
denominator-ratio weight.  If that paired decomposition is retained instead
of the independent-tail replacement, let $m_w=\min(c_q,c_\theta)$.  Under
N1-RATE with constant $A$, the correct drift weight is

\[
 \delta_w\le
 2|s|A(2-\lambda_q)k_w^2\frac{c_q}{m_w}m_w^{-2\sigma}.
\]

Equivalently, in $c_q^{-2\sigma}$ form, its comparison factor is

\[
 \left(\frac{c_q}{m_w}\right)^{2\sigma+1}
 =\max\!\left(1,\frac{c_q}{c_\theta}\right)^{2\sigma+1},
\]

not the inverse ratio printed schematically at
`LAW_R2_RATE_LEMMA_DRAFT.md:268-274`.  Bounding this weighted paired tail
would still require corrected M1 and ratio-inclusive N4-scale.  The
independent Ford-tail split above is what removes that unnecessary N3
dependency.

## 4. Promotion result

1. **Retire N1-strong.**  It is false for every $q\ge12$ along the explicit
   $m=q-1$ Chebyshev family, and in fact admits no q-uniform finite constant.
2. **Keep N1-RATE explicitly conjectural with $A=11/20$** on the future M1
   canonical matched-coset domain.  The emitted escaping list has now been
   interval-tested, but no completeness theorem follows.
3. **Retire the N2 depth-12 onto claim.**  It compares against an incomplete
   237-key theta target; the exact window has 263 cosets, including explicit
   depth-13 targets.  N2-global remains under M1.
4. **Discharge the RATE-use form of N3 at paper level** by replacing the
   empirical paired shell with independently truncated Ford tails.  Use
   $X(q)=q^6$ on the current sigma band and charge cross-boundary head terms
   explicitly.  N3-shell itself remains conjectural and should not appear in
   a proved R2 statement.

No conclusion here promotes the assembled (RATE) lemma: M1, N1-RATE,
N4-scale, and M3 remain open exactly at their cited scopes.

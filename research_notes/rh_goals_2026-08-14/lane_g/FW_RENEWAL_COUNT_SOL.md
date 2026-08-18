# The balanced-section renewal count `(FW)`

**Date:** 2026-08-18  
**Program:** `(RATE)`, lane G  
**Interpreter:** `/Users/za/.venvs/farey-rh/bin/python`  
**Write scope:** this file only

## 0. Receipts before claims

### 0.1 Bound objects read

The proof below uses the already proved theta canonical normal form, not the
older isolated-code `firstWrap` predicate.

- `M1_ROUTE_B_FREEPRODUCT_SOL.md:346-440` gives the source matrices, the
  canonical word
  \(R^{a_0}Q\cdots QR^{a_k}\), and the strict prefix recurrence
  \(|U_j|>|U_{j-1}|\).
- `M1_ROUTE_B_FREEPRODUCT_SOL.md:442-528` identifies
  \(\operatorname{im}L_q\) exactly with the canonical words whose
  \(R\)-exponents lie in the balanced alphabet
  \(\mathcal A_q\). Thus the complement consists exactly of words with a
  boundary-reduced exponent outside that alphabet.
- `M1_ROUTE_B_REPAIR_SOL.md:963-1055` defines `(DH)`, `(FW)`, and their
  separate roles in the conditional `(RATE)` argument.
- `M2_LOCALIZATION_THEOREM_SOL.md:484-721` proves the finite sine envelope and
  its turnover. It is a consistency check here; the proof of `(FW)` below
  uses the stronger factorization available after marking the overflow
  \(R\)-letter.

The relevant source-line receipt was:

```bash
nl -ba research_notes/rh_goals_2026-08-14/lane_g/M1_ROUTE_B_FREEPRODUCT_SOL.md \
  | sed -n '346,528p'
nl -ba research_notes/rh_goals_2026-08-14/lane_g/M1_ROUTE_B_REPAIR_SOL.md \
  | sed -n '963,1055p'
```

Selected output:

```text
361  ### Lemma 4.1 (canonical digits are bounded by theta height) — PROVED
366  w = R^{a_0} Q R^{a_1} Q ... Q R^{a_k}
381  Q = [[0,-1],[1,0]],      S = [[1,2],[0,1]],
382  R = QS = [[0,-1],[1,2]].
388  R^a = [[1-a,-a],[a,1+a]].
395  U_{-1}=-1,
396  U_0=2a_0+1,
397  U_j=-2a_j U_{j-1}-U_{j-2}.
416  |U_j| >= 2|U_{j-1}|-|U_{j-2}| > |U_{j-1}|.
447  A_q = {-floor((q-1)/2),..., -1, 1,...,floor(q/2)}.
482  im(L_q)
483   = {theta double cosets whose canonical R-exponents all lie in A_q}.
1017 A_{\rm wrap,q}(Y)
1018 \le {C_1Y^2\over q}
1019      \bigl(1+\log_+(Y/q)\bigr),\qquad Y\ge q.          \tag{FW}
```

### 0.2 Exact factorization replay and moving census

The following fresh run reconstructed every admissible theta key with
\(c_H\le384\), checked the matrix height, and tested every marked digit cut.
The assertions include

\[
 |c_P|<A,\qquad |\gamma_V|<B,\qquad
 |c(PV)|<2AB,\qquad
 |c(W)|\ge (|a|-2)AB.
\]

It then recomputed the exact overflow census for every
\(q=8,\ldots,48\) and \(Y/q\in\{1,2,4,8,16\}\). No files were written.

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
import math
from math import gcd
I=((1,0),(0,1)); Q=((0,-1),(1,0))
def mm(A,B):
 return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)) for i in range(2))
def Rp(a): return ((1-a,-a),(a,1+a))
def red(t):
 o=[]
 for z,a in t:
  if z=='Q':
   if o and o[-1][0]=='Q': o.pop()
   else: o.append(('Q',1))
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
def wordmat(a):
 M=I
 for j,x in enumerate(a):
  if j:M=mm(M,Q)
  M=mm(M,Rp(x))
 return M
records=[]; occurrences=0; pre={};suf={};max_c0_ratio=0.0
for c in range(1,385):
 for d in range(2*c):
  if gcd(c,d)!=1 or (c+d)%2==0:continue
  w=from_cd(c,d);records.append((c,w))
  if w==('Q',):continue
  a=tuple(x for x in w if x!='Q');m=len(a);W=wordmat(a)
  assert abs(W[1][0])==c
  P=[I]
  for x in a:P.append(mm(mm(P[-1],Rp(x)),Q))
  V=[None]*m;V[-1]=I
  for j in range(m-2,-1,-1):V[j]=mm(mm(Q,Rp(a[j+1])),V[j+1])
  for j,x in enumerate(a):
   p=P[j];v=V[j];A=abs(p[1][1]-p[1][0]);B=abs(v[0][0]+v[1][0])
   pre.setdefault(A,set()).add(p);suf.setdefault(B,set()).add(v)
   c0=mm(p,v)[1][0];AB=A*B
   assert A and B and abs(p[1][0])<A and abs(v[1][0])<B
   assert abs(c0)<2*AB and abs(W[1][0]) >= (abs(x)-2)*AB
   max_c0_ratio=max(max_c0_ratio,abs(c0)/AB);occurrences+=1
assert all(len(s)<=4*A for A,s in pre.items())
assert all(len(s)<=4*B for B,s in suf.items())
print('exact_keys_cH_le_384=',len(records))
print('marked_digit_occurrences_checked=',occurrences)
print('factorization_assertions=PASS')
print('max_abs_cPV_over_AB=',f'{max_c0_ratio:.12f}')
print('observed_prefix_choice_max_ratio=',f'{max(len(s)/(4*A) for A,s in pre.items()):.12f}')
print('observed_suffix_choice_max_ratio=',f'{max(len(s)/(4*B) for B,s in suf.items()):.12f}')
print('u exact_counts_q8_to_q48 slope max_normalized')
for u in (1,2,4,8,16):
 counts=[];xy=[];norm=[]
 for q in range(8,49):
  lo=-((q-1)//2);hi=q//2;Y=u*q
  n=sum(1 for c,w in records if 2*c<=Y and any(x!='Q' and not(lo<=x<=hi) for x in w))
  counts.append(n)
  if n:xy.append((math.log(q),math.log(n)))
  norm.append(n*q/(Y*Y*(1+math.log(u))))
 xb=sum(x for x,y in xy)/len(xy);yb=sum(y for x,y in xy)/len(xy)
 slope=sum((x-xb)*(y-yb) for x,y in xy)/sum((x-xb)**2 for x,y in xy) if len(xy)>1 else float('nan')
 print(f'u={u:<2} counts={",".join(map(str,counts))}')
 print(f'u={u:<2} slope={slope:.6f} max_norm={max(norm):.6f} at_q={8+norm.index(max(norm))}')
PY
```

Output:

```text
exact_keys_cH_le_384= 59931
marked_digit_occurrences_checked= 506750
factorization_assertions=PASS
max_abs_cPV_over_AB= 0.997389033943
observed_prefix_choice_max_ratio= 0.250000000000
observed_suffix_choice_max_ratio= 0.250000000000
u exact_counts_q8_to_q48 slope max_normalized
u=1  counts=1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1
u=1  slope=0.000000 max_norm=0.125000 at_q=8
u=2  counts=9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49
u=2  slope=0.952072 max_norm=0.166111 at_q=8
u=4  counts=38,40,47,50,53,60,63,66,73,76,79,86,89,92,99,102,105,112,115,118,125,128,131,138,141,144,151,154,157,164,167,170,177,180,183,190,193,196,203,206,209
u=4  slope=0.971684 max_norm=0.124408 at_q=8
u=8  counts=173,184,211,230,251,268,289,306,330,352,367,390,409,428,451,470,489,508,535,550,569,592,607,634,653,672,691,710,733,752,775,790,813,836,851,874,893,912,935,958,973
u=8  slope=0.980461 max_norm=0.109725 at_q=8
u=16 counts=776,845,964,1047,1154,1247,1344,1427,1545,1622,1724,1820,1909,1998,2099,2194,2284,2378,2478,2564,2666,2754,2847,2950,3042,3132,3241,3316,3415,3514,3613,3692,3797,3892,3979,4084,4171,4266,4369,4460,4555
u=16 slope=0.992744 max_norm=0.100437 at_q=8
```

The counts are exact integers in the displayed box. The slopes and normalized
ratios are finite diagnostics only. The proof starts now and does not use
those fitted slopes.

## 1. Theorem `(FW)` — PROVED

Let \(q\ge3\) be an integer, let

\[
 \mathcal A_q=
 \{-\lfloor(q-1)/2\rfloor,\ldots,-1,
       1,\ldots,\lfloor q/2\rfloor\},
\]

and let \(A_{{\rm wrap},q}(Y)\) count theta double cosets outside
\(\operatorname{im}L_q\) whose conjugated theta height
\(y=2c_H\) is at most \(Y\). Then, uniformly for \(Y\ge q\),

\[
 \boxed{
 A_{{\rm wrap},q}(Y)
 \le C_1\frac{Y^2}{q}
       \bigl(1+\log_+(Y/q)\bigr),
 \qquad C_1=128(1+\log2).}
 \tag{FW}
\]

The constant is explicit and deliberately rounded upward at every counting
step; it is not optimized.

### 1.1 Canonical first-overflow cut

Every nonexceptional theta class has a unique boundary-reduced canonical word

\[
 W=R^{a_0}Q R^{a_1}Q\cdots Q R^{a_k},                 \tag{1.1}
\]

where every \(a_i\ne0\), \(a_0\ne-1\), and \(a_k\ne1\). The exceptional
word \(Q\) has no \(R\)-digit and is never an overflow word.

By the proved image characterization, a class is omitted exactly when some
\(a_i\notin\mathcal A_q\). Mark the first such index \(j\). This makes the
decomposition

\[
 W=P R^a V,
 \qquad a=a_j,                                           \tag{1.2}
\]

unique, where

\[
\begin{aligned}
 P&=1
   \quad\hbox{or}\quad
   R^{a_0}Q\cdots R^{a_{j-1}}Q,\\
 V&=1
   \quad\hbox{or}\quad
   QR^{a_{j+1}}Q\cdots QR^{a_k}.
\end{aligned}                                            \tag{1.3}
\]

Put

\[
 h=\lceil q/2\rceil.
\]

Every overflow digit satisfies \(|a|\ge h\). For even \(q\), the positive
digit \(+q/2\) is still in \(\mathcal A_q\), whereas \(-q/2\) is not. Counting
both signs when \(|a|=h\) only enlarges the upper bound.

### 1.2 Prefix and suffix scale lemma

Write the bottom row of \(P\) as \((c_P,d_P)\), the first column of \(V\) as
\((\alpha_V,\gamma_V)^t\), and define the signed nonzero integers

\[
 A=d_P-c_P,\qquad B=\alpha_V+\gamma_V.                  \tag{1.4}
\]

For an empty fragment, \(P=V=1\) and the corresponding scale is \(1\).

We claim

\[
 |c_P|<|A|,\qquad |\gamma_V|<|B|,                       \tag{1.5}
\]

and, for each positive integer \(r\),

\[
 \#\{P:|A|=r\}\le4r,\qquad
 \#\{V:|B|=r\}\le4r.                                  \tag{1.6}
\]

#### Prefix inequality

For a nonempty prefix, write

\[
 W_r=R^{a_0}Q\cdots Q R^{a_r},\qquad P=W_rQ.
\]

The recurrence already proved in `M1_ROUTE_B_FREEPRODUCT_SOL.md` is

\[
 U_{-1}=-1,\quad U_0=2a_0+1,\quad
 U_i=-2a_iU_{i-1}-U_{i-2},                              \tag{1.7}
\]

with

\[
 |U_i|>|U_{i-1}|,qquad
 (c_r,d_r)=\left({U_r+U_{r-1}\over2},
                 {U_r-U_{r-1}\over2}\right).           \tag{1.8}
\]

Right multiplication by \(Q\) makes the bottom row of \(P\) equal to
\((d_r,-c_r)\). Hence

\[
 A=-c_r-d_r=-U_r,qquad
 c_P=d_r={U_r-U_{r-1}\over2}.                            \tag{1.9}
\]

The strict inequality in (1.8) gives \(|c_P|<|A|\). This also proves
\(A\ne0\).

#### Prefix multiplicity

If \(|A|=r\), then (1.5) leaves fewer than \(2r\) choices for the integer
\(c_P\), two choices for the sign of \(A\), and then
\(d_P=c_P+A\) is fixed. Thus there are fewer than \(4r\) candidate bottom
rows.

There is at most one admissible prefix for each bottom row. Indeed, if
\(P_i=\left(\begin{smallmatrix}*&*\\c&d\end{smallmatrix}\right)\), then a
direct multiplication gives
\(P_2P_1^{-1}=\left(\begin{smallmatrix}1&m\\0&1\end{smallmatrix}\right)\).
It lies in the theta group, so the proved width-two cusp-stabilizer lemma
(`M1_ROUTE_B_REPAIR_SOL.md:369-460`) forces it to be a power \(S^\ell\).
If \(\ell>0\), the reduced word
\(S^\ell P=(QR)^\ell P\) begins with \(Q\), because the last \(R\) in
\(S^\ell\)
combines with \(R^{a_0}\) to \(R^{a_0+1}\ne1\). It cannot be another
admissible prefix. If \(\ell<0\), the reduced word begins with \(R^{-1}\),
which violates the prefix condition \(a_0\ne-1\). Thus \(\ell=0\). The empty
prefix is covered separately. This proves the first bound in (1.6).

#### Suffix inequality and multiplicity

If \(V\ne1\), then in \(PSL_2(\mathbb Z)\)

\[
 V^{-1}=R^{-a_k}Q\cdots Q R^{-a_{j+1}}Q.                \tag{1.10}
\]

This is an admissible prefix: its initial exponent is \(-a_k\ne-1\) because
the canonical terminal condition is \(a_k\ne1\). The bottom row of the exact
matrix inverse is \((-\gamma_V,\alpha_V)\), up to the harmless common
\(PSL\) sign. Applying the prefix result gives

\[
 |\gamma_V|<|\alpha_V+\gamma_V|=|B|.
\]

Inversion is injective and preserves the scale \(|B|\), so the prefix
multiplicity bound also gives the second inequality in (1.6).

### 1.3 The overflow letter supplies the product gain

In source coordinates,

\[
 R^a=
 \begin{pmatrix}1-a&-a\\a&1+a\end{pmatrix}
 =I+a
 \binom{-1}{1}(1,1).                                    \tag{1.11}
\]

This rank-one identity makes the lower-left entry affine in the marked
digit:

\[
 c(W)=c(PV)+aAB.                                         \tag{1.12}
\]

Moreover,

\[
 c(PV)=c_P\alpha_V+d_P\gamma_V
      =c_PB+A\gamma_V.                                  \tag{1.13}
\]

By (1.5),

\[
 |c(PV)|<2|AB|.
\]

Consequently, with \(n=|a|\),

\[
 c_H(W)=|c(W)|>(n-2)|AB|.                                \tag{1.14}
\]

For \(q\ge8\), one has \(h\ge4\), so \(n-2\ge n/2\). Since
\(y(W)=2c_H(W)\le Y\), (1.14) forces

\[
 n|A||B|\le Y.                                          \tag{1.15}
\]

This is the missing renewal product. It comes from the parabolic overflow
letter itself, while the two fragment scales record the no-overflow prefix
and arbitrary continuation. No independence assumption is made.

### 1.4 Convolution count

Every overflow word has one unique first-overflow triple \((P,a,V)\). Dropping
the restriction that \(P\) is no-wrap only increases the count. Equations
(1.6) and (1.15), with two possible signs for \(a\), give

\[
 A_{{\rm wrap},q}(Y)
 \le32\sum_{n=h}^{\lfloor Y\rfloor}
       \sum_{rs\le Y/n}rs.                              \tag{1.16}
\]

For every real \(T\ge1\),

\[
\begin{aligned}
 \sum_{rs\le T}rs
 &\le \sum_{r\le T}r
       \left\lfloor{T\over r}\right\rfloor^2\\
 &\le T^2\sum_{r\le T}{1\over r}
 \le T^2(1+\log T).                                    \tag{1.17}
\end{aligned}
\]

Here the first inequality uses
\(1+\cdots+m=m(m+1)/2\le m^2\) for \(m\ge1\). Therefore

\[
\begin{aligned}
 A_{{\rm wrap},q}(Y)
 &\le32Y^2\sum_{n=h}^{\lfloor Y\rfloor}
      {1+\log(Y/n)\over n^2}\\
 &\le {32Y^2\over h-1}\bigl(1+\log(Y/h)\bigr).         \tag{1.18}
\end{aligned}
\]

For \(q\ge8\),

\[
 h-1\ge q/4,\qquad
 \log(Y/h)\le\log(Y/q)+\log2.                           \tag{1.19}
\]

Since \(Y\ge q\),

\[
 1+\log(Y/h)
 \le(1+\log2)(1+\log(Y/q)).                             \tag{1.20}
\]

Substituting (1.19)--(1.20) into (1.18) proves `(FW)` for \(q\ge8\) with
\(C_1=128(1+\log2)\).

For the finitely many \(3\le q\le7\), the proved Ford bound
\(A_{{\rm wrap},q}(Y)\le Y^2\) gives

\[
 A_{{\rm wrap},q}(Y)
 \le {7Y^2\over q}\bigl(1+\log(Y/q)\bigr),
\]

and \(7<C_1\). This completes the proof for every Hecke index \(q\ge3\).
\(\square\)

## 2. Weighted overflow consequence — PROVED

Put \(p=2\sigma>2\). The structural support is \(y\ge q\), and layer-cake
summation includes a possible atom at \(y=q\):

\[
 E_{\rm wrap}(q,\sigma)
 =p\int_q^\infty A_{{\rm wrap},q}(t)t^{-p-1}\,dt.       \tag{2.1}
\]

Applying `(FW)` and substituting \(t=qu\) gives

\[
\begin{aligned}
 E_{\rm wrap}(q,\sigma)
 &\le {pC_1\over q}\int_q^\infty
       t^{1-p}\bigl(1+\log(t/q)\bigr)\,dt\\
 &=pC_1q^{1-p}
   \left({1\over p-2}+{1\over(p-2)^2}\right).          \tag{2.2}
\end{aligned}
\]

Thus the balanced-section overflow contribution has the required
\(q^{1-2\sigma}\) scale with no external \(\log q\) loss.

## 3. False target, negation, and corrected mechanism

**FALSE target:** “First-wrap support \(y\ge q\), the sine-envelope depth
threshold, and Ford counting already imply `(FW)`.”

**NEGATION:** support plus Ford gives only \(A(Y)\le Y^2\), hence
\(E_{\rm wrap}=O(q^{2-2\sigma})\), one power too weak. The sine envelope
turns over and does not by itself count continuation states.

**CORRECTED mechanism:** mark the first boundary-reduced overflow exponent,
cut the canonical word as \(P R^aV\), and use the exact rank-one dependence
on \(a\). Canonical boundary reduction gives \(O(A)\) prefix states and
\(O(B)\) suffix states, while the overflow height forces
\(|a|AB\le Y\). The resulting divisor convolution is exactly
\(Y^2q^{-1}(1+\log(Y/q))\).

No horoball-shadow or transfer-operator hypothesis is needed for `(FW)`.

## 4. Program consequence and remaining co-requisite

The previous status “`(FW)` is CONJECTURAL” in
`DENSITY_GAIN_ATTACK_SOL.md` and `M1_ROUTE_B_REPAIR_SOL.md:1035-1039` is
superseded by the proof above.

This does **not** by itself prove full `(RATE)`. The matched sum still requires
the separately isolated comparison-weighted law

\[
 B_q(Y)=
 \sum_{m_X\le Y}k_X^2{x_X\over m_X}
 \le C_0Y^2\min(Y,q)
       \bigl(1+\log_+(Y/q)\bigr),                         \tag{DH}
\]

together with the interval derivative envelope/N1 input retained in
`M1_ROUTE_B_REPAIR_SOL.md:828-862,963-1055`. `(DH)` remains
**CONJECTURAL / OPEN**. Therefore full `(RATE)` and the effective R5 threshold
remain **CONJECTURAL**; the unpaired overflow obstruction is now closed.

## 5. Claim ledger

| Claim | Verdict | Receipt/proof |
|---|---|---|
| Exact overflow class is “canonical \(R\)-exponent outside \(\mathcal A_q\)” | **PROVED upstream** | `M1_ROUTE_B_FREEPRODUCT_SOL.md:442-528` |
| Prefix/suffix fragment scale bounds and \(O(r)\) multiplicity | **PROVED here** | (1.5)--(1.10) |
| Overflow product constraint \(|a|AB\le Y\) for \(q\ge8\) | **PROVED here** | (1.11)--(1.15) |
| `(FW)` with \(C_1=128(1+\log2)\) | **PROVED** | (1.16)--(1.20), Ford for \(q\le7\) |
| \(E_{\rm wrap}(q,\sigma)=O_\sigma(q^{1-2\sigma})\) | **PROVED** | (2.1)--(2.2) |
| Finite census agrees with the renewal scale | **MEASURED / EXACT IN THE DISPLAYED BOX** | 59,931 exact keys; five moving ratios; command/output in Section 0.2 |
| `(DH)` | **CONJECTURAL / OPEN** | Not implied by `(FW)`; comparison factor \(x_X/m_X\) remains load-bearing |
| Full `(RATE)` | **CONJECTURAL** | Conditional on `(DH)` and the retained interval/N1 inputs |

# Two-mark finite-height renewal: a log-weakened theorem sufficient for `(RATE)`

**Date:** 2026-08-18

**Program:** `(RATE)`, lane G

**Interpreter:** `/Users/za/.venvs/farey-rh/bin/python`

**Write scope:** this file only

## 0. Verdict

Put

\[
 B_q(Y)=\sum_{X\in\mathcal C_q:x_X\le Y}k_X^2 .       \tag{0.1}
\]

The equality with the comparison-weighted definition follows from the proved
endpoint theorem in `DH2_RENEWAL_PROOF_SOL.md`: `x_X\le y_X`, hence
`m_X=x_X` and `x_X/m_X=1`.

The exact bound called `(DH_2)` there,

\[
 B_q(Y)\ll Y^2
 \begin{cases}
 Y,&Y\le q,\\
 q(1+L)+(1+L)^2,&Y\ge q,
 \end{cases}
 \qquad L=\log(Y/q),                                  \tag{0.2}
\]

is **NOT PROVED here** and remains **CONJECTURAL**.  What is proved is the
following log-weakened form, directly at the required finite height `x<=Y`.

### Two-mark finite-height renewal theorem — PROVED

For every integer `q>=3` and every `Y>=1`, with

\[
 R=1+\log_+(Y/q),\qquad C_4=2^{100},
\]

one has

\[
 \boxed{
 B_q(Y)\le C_4Y^2
 \begin{cases}
 Y,&1\le Y\le q,\\[2mm]
 qR^2+R^4,&Y\ge q.
 \end{cases}}                                        \tag{DH_{2,4}}
\]

The proof is paper-level.  It uses only:

1. the proved nonnegative Chebyshev-block factorization from
   `DH2_RENEWAL_PROOF_SOL.md` Section 3;
2. the proved reduced-depth block bound (6.6) there;
3. the paper/referee-confirmed width-one Ford count `A_q(T)<=T^2`;
4. an injective endpoint-normalized two-cut coding proved below.

No theta-height cutoff is substituted for the finite-height cutoff.  That
substitution is false as an inference and can miss arbitrarily distorted
terms.

The extra powers of the **relative** logarithm are harmless for `(RATE)`.
If `2<p=2sigma<3`, define

\[
\begin{aligned}
 J_2(p)&={1\over p-2}+{2\over(p-2)^2}+{2\over(p-2)^3},\\
 J_4(p)&={1\over p-2}+{4\over(p-2)^2}+{12\over(p-2)^3}
          +{24\over(p-2)^4}+{24\over(p-2)^5}.
\end{aligned}                                         \tag{0.3}
\]

Then layer cake gives

\[
 \sum_X k_X^2x_X^{-p}
 \le pC_4\left[
 \left({1\over3-p}+J_2(p)\right)q^{3-p}
 +J_4(p)q^{2-p}\right].                               \tag{0.4}
\]

Consequently the conditional `(RATE)` exponent is unchanged:

\[
 \boxed{\alpha=p-1=2\sigma-1.}                        \tag{0.5}
\]

At `sigma=1.1`, `alpha=1.2`.  The strict R5 arithmetic remains

\[
 \boxed{\log q>2.560914\times10^9+{5\over6}\log C_R}  \tag{0.6}
\]

for the full scattering constant `C_R`.  This is still conditional on the
other `(RATE)` inputs, in particular the stated N1-RATE drift envelope; it is
not an unconditional R5 certificate.

## 1. Receipts before claims

### 1.1 Inputs and hashes

The required sources were read in the requested order.  The current inputs
were then hashed:

```bash
/Users/za/.venvs/farey-rh/bin/python --version
shasum -a 256 \
  research_notes/rh_goals_2026-08-14/lane_g/DH2_RENEWAL_PROOF_SOL.md \
  research_notes/rh_goals_2026-08-14/lane_g/DH_DEPTH_LAW_SOL.md \
  research_notes/rh_goals_2026-08-14/lane_g/FW_RENEWAL_COUNT_SOL.md \
  research_notes/rh_goals_2026-08-14/lane_g/M2_FORD_PACKING_REFEREE.md \
  projects/aristotle_dispatch_v29/result/v29sub_aristotle/RateCoreIV.lean
```

Output:

```text
Python 3.13.13
096d389905ad21505e2c25c30aa37b5a2fa3d3f6d054bcb30229096fc5c8d885  DH2_RENEWAL_PROOF_SOL.md
9146ecebfdb976ceb3df49c0e7789bc5a82ef2116ceb1f02d6a89d32f6c602d8  DH_DEPTH_LAW_SOL.md
70cf0a9d12cdc6938c431bd1246b0ca18d929c151fb98399a8e94a75d7f6fd3c  FW_RENEWAL_COUNT_SOL.md
ebb38cf55ea4e4132df7e0f3f68901c196b8c623b1b4f4b24b5b11b2a2318345  M2_FORD_PACKING_REFEREE.md
fee8a039c0cc7140a9b9d63a669653cfb83b060e4f6526bb882ecf21817ce88c  RateCoreIV.lean
```

The abbreviated output names have the full paths displayed in the command.
The v29 theorem is machine-verified only in its stated finite no-wrap range;
the proof below does not apply it to a whole word outside that range.

### 1.2 Exact `y<=100` split: same run versus different run

For a theta key `(c,d)`, the centered Euclidean quotients recover the raw
RateCore exponent list `w`; `len(w)+1=k`.  In the ordered raw-digit pair mass
`(k-1)^2`, split unit digits into maximal constant-sign `+1` or `-1` runs.
The three disjoint pieces are:

* `same_unit_run = sum r^2`;
* `diff_unit_run = (sum r)^2-sum r^2`;
* `heavy_involved = (k-1)^2-(sum r)^2`.

The exact replay was:

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from pathlib import Path
from math import gcd
P=Path('research_notes/rh_goals_2026-08-14/lane_g/DH_DEPTH_LAW_SOL.md')
s=P.read_text()
a=s.index('from collections import Counter',s.index('self-contained stdout-only'))
b=s.index('\nPY\n',a)
exec(s[a:b].split('q=12;')[0])

def steps(c,d):
 out=[]
 while c:
  if c<0:c,d=-c,-d
  r=d%(2*c)
  if r>c:r-=2*c
  out.append((r-d)//(2*c));c,d=r,-c
 return out
def raw(c,d):return tuple(-n for n in reversed(steps(c,d)[1:]))
def split(w):
 runs=[];i=0
 while i<len(w):
  if abs(w[i])==1:
   e=w[i];j=i+1
   while j<len(w) and w[j]==e:j+=1
   runs.append(j-i);i=j
  else:i+=1
 u=sum(runs);n=len(w)
 return sum(r*r for r in runs),u*u-sum(r*r for r in runs),n*n-u*u,max(runs,default=0)

base=[]
for c in range(1,51):
 for d in range(2*c):
  if gcd(c,d)==1 and (c+d)%2:
   z=raw(c,d);cw=from_cd(c,d)
   assert len(z)+1==len(steps(c,d))
   base.append((cw,z))
print('exact_theta_keys_y_le_100=',len(base))
print('q n B raw_pair same_unit_run diff_unit_run heavy_involved boundary_linear max_run')
for q in (8,12,16,24,32,48):
 A=set(range(-((q-1)//2),0))|set(range(1,q//2+1))
 rows=[z for cw,z in base if all(t=='Q' or t in A for t in cw)]
 B=rawpair=same=diff=heavy=boundary=mr=0
 for w in rows:
  k=len(w)+1;s0,d0,h0,m=split(w)
  B+=k*k;rawpair+=len(w)**2;same+=s0;diff+=d0;heavy+=h0
  boundary+=2*len(w)+1;mr=max(mr,m)
 assert B==rawpair+boundary and rawpair==same+diff+heavy
 print(q,len(rows),B,rawpair,same,diff,heavy,boundary,mr)
 print(' shares %.6f %.6f %.6f'%(same/rawpair,diff/rawpair,heavy/rawpair))
PY
```

Output:

```text
exact_theta_keys_y_le_100= 1037
q n B raw_pair same_unit_run diff_unit_run heavy_involved boundary_linear max_run
8 588 11049 6759 2140 1710 2909 4290 4
 shares 0.316615 0.252996 0.430389
12 764 18821 12415 5060 3184 4171 6406 6
 shares 0.407571 0.256464 0.335965
16 847 24529 16842 7973 4008 4861 7687 8
 shares 0.473400 0.237976 0.288624
24 920 32817 23659 13389 4698 5572 9158 12
 shares 0.565916 0.198571 0.235513
32 960 41661 31359 20241 5130 5988 10302 16
 shares 0.645461 0.163589 0.190950
48 984 50533 39339 27973 5256 6110 11194 23
 shares 0.711076 0.133608 0.155317
```

These are exact integers in the theta window.  They are **DATA, NOT THE
THEOREM**.  Their role was to expose the shared-run obstruction and to force a
separate one-cut/two-cut audit.  The proof does **not** identify this raw split
term by term with the canonical-atom split below; it first passes through the
proved upper bound (2.7).  At `q=48`, the same-run part is already more than 71
percent of the raw ordered pair mass.

### 1.3 The finite cutoff cannot be replaced by a theta cutoff

At `q=3`, take the valid balanced canonical sequences

\[
 (1,-1)^4,\qquad (1,-1)^5.
\]

An exact integer matrix replay gives:

```bash
/Users/za/.venvs/farey-rh/bin/python - <<'PY'
def mm(A,B):
 return [[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def N(a,lam):
 U=[0,1]
 for _ in range(1,abs(a)+1):U.append(lam*U[-1]-U[-2])
 n=abs(a);M=[[U[n],U[n+1]],[U[n-1],U[n]]]
 return M if a>0 else [[M[0][0],M[1][0]],[M[0][1],M[1][1]]]
for r in (4,5):
 a=[1,-1]*r
 print('digits=',len(a),end=' ')
 for lam in (1,2):
  P=[[1,0],[0,1]]
  for z in a:P=mm(P,N(z,lam))
  print(('x' if lam==1 else 'y')+'='+str(lam*P[0][0]),end=' ')
 print()
PY
```

Output:

```text
digits= 8 x=34 y=1970
digits= 10 x=89 y=11482
```

Thus `x<=Y` does not imply `y<=Y`, even remotely.  The proof below stays at
`x` throughout.

## 2. Positive blocks and the depth atoms

Let

\[
 \theta={\pi\over q},\qquad \lambda=2\cos\theta,qquad
 u_j={\sin(j\theta)\over\sin\theta},\qquad h=\lfloor q/2\rfloor.
\]

For `q>=3`, `1<=lambda<2`; the lower inequality is used below when shear
gains are rounded downward.

For `n>=1`, put

\[
 M_n=\begin{pmatrix}u_n&u_{n+1}\\u_{n-1}&u_n\end{pmatrix},
 \qquad N_n=M_n,\qquad N_{-n}=M_n^t.                  \tag{2.1}
\]

Section 3 of `DH2_RENEWAL_PROOF_SOL.md` proves that, for a balanced canonical
word with exponent sequence `a=(a_0,...,a_r)`, up to a harmless common sign,

\[
 W=Q N_{a_0}\cdots N_{a_r},\qquad
 x(W)=\lambda\bigl(N_{a_0}\cdots N_{a_r}\bigr)_{11}. \tag{2.2}
\]

Every entry in (2.1) is nonnegative in the balanced range.  If `q>=4` and
`2<=n<=h`, then every entry satisfies

\[
 \boxed{(N_{\pm n})_{ij}\ge {n\over\pi}.}             \tag{2.3}
\]

Indeed, for `j<=q/2`, concavity gives

\[
 u_j\ge {2j\over\pi}.
\]

Hence `u_{n-1}>=n/pi`, `u_n>=2n/pi`.  The same bound for `u_{n+1}` is
immediate unless `n=h`; at that endpoint reflect sine:

\[
 u_{h+1}=u_{h-1}\quad(q=2h),\qquad
 u_{h+1}=u_h\quad(q=2h+1).
\]

The even case uses `h>=2`.  For `q=3` there is no heavy digit.

Also

\[
 U:=N_1=\begin{pmatrix}1&\lambda\\0&1\end{pmatrix},
 \qquad
 L:=N_{-1}=\begin{pmatrix}1&0\\\lambda&1\end{pmatrix},              \tag{2.4}
\]

so

\[
 U^t=\begin{pmatrix}1&t\lambda\\0&1\end{pmatrix},qquad
 L^t=\begin{pmatrix}1&0\\t\lambda&1\end{pmatrix}.                  \tag{2.5}
\]

Decompose the canonical exponent sequence into the following **atoms**:

* every heavy digit `a_j`, `|a_j|>=2`, is one atom of weight `|a_j|`;
* every maximal constant-sign run of `+1` or `-1` digits is one atom of
  weight `1`.

Write

\[
 A(W)=\sum_{\text{atoms }\alpha}w(\alpha)
     =\sum_{|a_j|\ge2}|a_j|+\ell(W).                  \tag{2.6}
\]

The proved block estimate (6.6) of `DH2_RENEWAL_PROOF_SOL.md` is

\[
 k(W)\le1+2A(W),
\]

and therefore

\[
 k(W)^2\le2+8A(W)^2.                                  \tag{2.7}
\]

The atom decomposition is applied only to the right side of the already
proved inequality (2.7).  In particular, no equality between raw unit-run
pairs and heavy canonical digits is asserted.  This avoids precisely the
endpoint-canonicalization ambiguity visible in the data-first split.  The
global v29 theorem is not applied beyond its `k<=q-1` hypothesis.

## 3. Endpoint-normalized cores

For any consecutive exponent fragment `F`, delete its maximal leading
`-1` run and maximal trailing `+1` run.  There are unique integers `r,s>=0`
and a unique core `F_0` such that

\[
 F=(-1)^r\,F_0\,(+1)^s,                               \tag{3.1}
\]

where `F_0` is empty or begins with a digit different from `-1` and ends
with a digit different from `+1`.

This is exactly the theta double-coset boundary normalization.  A nonempty
core is therefore a balanced canonical word: it neither begins with `-1` nor
ends with `+1`.  There is no exceptional nonempty singleton `(+1)` or `(-1)`,
because the former is deleted as a trailing run and the latter as a leading
run.  By the proved Route-B section theorem the core determines one finite
double coset injectively, and conversely its exponent sequence is recovered
from that finite canonical word.  Empty cores are kept as one extra symbol.

In matrices, (3.1) is

\[
 N(F)=L^rN(F_0)U^s,
\]

and the deleted boundary runs are invisible to the `(1,1)` entry:

\[
 N(F)_{11}=N(F_0)_{11}.                               \tag{3.2}
\]

Define the core height

\[
 \rho(F_0)=
 \begin{cases}
 1,&F_0=\varnothing,\\
 \lambda N(F_0)_{11},&F_0\ne\varnothing.
 \end{cases}                                          \tag{3.3}
\]

The referee-confirmed Ford packing theorem gives, for every `T>=1`,

\[
 \#\{F_0:\rho(F_0)\le T\}\le1+T^2\le2T^2.           \tag{3.4}
\]

There is no one-sided-coset misuse here: endpoint normalization first makes
`F_0` a double-coset canonical word, and only then is Ford applied.

### 3.1 Product convolution of cores

Let `C_j(Z)` count ordered `j`-tuples of cores with product of core heights
at most `Z`.  Set `C_0(Z)=1` for `Z>=1` and `C_0(Z)=0` for `Z<1`.  For
`0<=j<=3` and `Z>=1`,

\[
 \boxed{C_j(Z)\le2^{12}Z^2(1+\log Z)^2.}              \tag{3.5}
\]

Proof: put each height in a dyadic shell `[2^i,2^{i+1})`.  By (3.4), a
shell contains at most `8*4^i` cores.  If `L=floor(log_2 Z)`, the `j=3`
sum is at most

\[
 8^3\sum_{i_0+i_1+i_2\le L}4^{i_0+i_1+i_2}
 \le {2048\over3}Z^2(L+2)^2
 \le2^{12}Z^2(1+\log Z)^2.                            \tag{3.6}
\]

The cases `j=1,2` are smaller, and the declared `j=0` case also obeys the
right side of (3.5).  Notice that no shell derivative such as `O(T)` was
inferred from the cumulative Ford bound.

## 4. The one-cut and two-cut coding lemma

### Lemma 4.1 — boundary-core marked coding

Fix a canonical balanced word and either one marked atom (the same-atom
part of `A(W)^2`) or two distinct ordered marked atoms.  There is an
injective encoding by:

1. at most three endpoint-normalized cores;
2. fewer than `2^20` finite type tags;
3. at most four auxiliary nonnegative integers, each entering a product gain
   as either `r` (when positive) or `1+r`;
4. the magnitude `n<=h` of each marked heavy atom;

such that, if `D` is the product of the **integer** gains recorded below and
`rho_i` are the core heights, then

\[
 \boxed{D\prod_i\rho_i\le4\pi^2x(W)<40x(W).}          \tag{4.1}
\]

If a marked light run is absorbed into a core, its length is not an
auxiliary integer: it is recovered as the tagged maximal boundary run of
that core.

#### Proof: one marked atom

Write the word as `P alpha V`.  Normalize

\[
 P=P_0U^p,\qquad V=L^vV_0.                            \tag{4.2}
\]

The global canonical endpoint rules imply that no leading `L` was removed
from `P` and no trailing `U` was removed from `V`.

The complete bridge table is:

| marked atom `alpha` | forced condition | encoding and gain |
|---|---|---|
| heavy `H_{\pm n}` | none | keep `U^pH_{\pm n}L^v`; `D`-gain `n(1+p)(1+v)` |
| light `U^t` | `p=0` | if `v>0`, keep `U^tL^v`, gain `tv`; if `v=0`, prepend `U^t` to `V_0` |
| light `L^t` | `v=0` | if `p>0`, keep `U^pL^t`, gain `pt`; if `p=0`, append `L^t` to `P_0` |

For a heavy bridge, (2.3)--(2.5) give the `D`-gain divided by `pi`:

\[
 (U^pH_{\pm n}L^v)_{11}
 \ge {n\over\pi}(1+p)(1+v).                           \tag{4.3}
\]

For a light bridge,

\[
 (U^tL^v)_{11}=1+tv\lambda^2\ge tv.                  \tag{4.4}
\]

If `U^t` is absorbed, `V_0` is nonempty and begins with a heavy atom: it
cannot begin with `L` by normalization, cannot begin with `U` by maximality,
and cannot be empty because a canonical word cannot end in `U`.  Hence the
enlarged core is canonical and its initial maximal `U` run recovers `t`.
The `L^t` case is symmetric.  This proves injectivity and the gain for one
mark.

#### Proof: two distinct marked atoms

Write the word as `P alpha M beta V` and normalize

\[
 P=P_0U^p,\qquad
 M=L^rM_0U^s,\qquad
 V=L^vV_0.                                             \tag{4.5}
\]

Use the following left and right bridge tables.

| atom | bridge/absorption rule |
|---|---|
| `alpha=H_{\pm n}` | `D`-gain `n(1+p)(1+r)` |
| `alpha=U^t` | `p=0`; gain `tr` if `r>0`, otherwise prepend it to `M_0` |
| `alpha=L^t` | `r=0`; gain `pt` if `p>0`, otherwise append it to `P_0` |
| `beta=H_{\pm m}` | `D`-gain `m(1+s)(1+v)` |
| `beta=U^t` | `s=0`; gain `tv` if `v>0`, otherwise prepend it to `V_0` |
| `beta=L^t` | `v=0`; gain `st` if `s>0`, otherwise append it to `M_0` |

If `M_0` is empty but `M=L^rU^s` is nonempty, maximality forces a marked
left `U` to have `r>0` and a marked right `L` to have `s>0`; the corresponding
`tr` or `st` bridge in the table applies.  Thus the only time a proposed
absorption into `M_0` would create a noncanonical singleton boundary core is
when `M_0` is empty and `r=s=0`, so the marked atoms are adjacent.  The
complete coupled table is then:

| adjacent marked pair | combined bridge gain |
|---|---|
| `U^t,H_{\pm n}` | `D`-gain `n(1+t)(1+v)` from `U^tH_{\pm n}L^v` |
| `H_{\pm n},L^u` | `D`-gain `n(1+p)(1+u)` from `U^pH_{\pm n}L^u` |
| `U^t,L^u` | `tu` from `U^tL^u` |

There is one apparently dangerous reverse junction, `L^u,U^t`, whose matrix
has `(L^uU^t)_{11}=1` and hence supplies no `ut` gain.  It is nevertheless
already covered, not discarded: the left marked `L^u` is either paired with
the terminal `U^p` of `P` (when `p>0`) or appended, with a tag, to the
nonempty core `P_0`; independently, the right marked `U^t` is either paired
with the initial `L^v` of `V` (when `v>0`) or prepended, with a tag, to the
nonempty core `V_0`.  The endpoint rules force those outer cores to be
nonempty in the two absorption subcases, and maximality says their adjacent
digits are heavy, so the enlarged cores remain canonical.  Thus the missing
direct gain is charged to the neighboring bridges or to Ford-counted tagged
cores.  The only absorptions into the *same* empty middle core are the three
cases in the displayed coupled table.  Equal adjacent light signs would have
been one maximal atom, so the case list is exhaustive.

Every absorption is uniquely reversible.  For example, a prepended marked
`U` run cannot merge into the old core, by maximality of the original atom;
the finite tag designates that initial maximal run as the selected atom, so
its exact length is read from the stored canonical core.  The same argument
applies to the other three boundary absorptions, including the two separate
outer-core tags in the reverse `L,U` case.  Thus Ford counts the ordinary
enlarged core, while the finite tag retains the marked/unmarked distinction.
Together with the unique decompositions (4.2) and (4.5), this proves
injectivity.

For completeness, the promised finite ceiling is explicit.  There are at
most `4^2` ordered marked-kind/sign choices (`H_+`,`H_-`,`U`,`L`), at most
`3^4` bridge/absorption statuses at the four cut boundaries, at most `2^3`
empty-core flags, four coupled-case selectors, and two one-mark/two-mark
selectors.  Their product is

\[
 4^2 3^4 2^3\cdot4\cdot2=82944<2^{17}<2^{20}.          \tag{4.6}
\]

Place state `1` at every core/bridge boundary in the nonnegative matrix
product.  If `b` is the number of heavy bridges, the path expansion gives

\[
 N(W)_{11}\ge \pi^{-b}
 \left(\prod_iN(F_i)_{11}\right)
 \left(\prod_{\text{bridges}}\text{integer gain}\right). \tag{4.7}
\]

There are at most three cores and at most two heavy bridges.  Since
`x=lambda N(W)_{11}` and `1<=lambda<=2`, (4.7) gives

\[
 D\prod_i\rho_i\le \lambda^2\pi^2x\le4\pi^2x<40x.
\]

At most four run-length parameters occur: `p,r,s,v` for two heavy bridges,
or two lengths per light bridge.  The displayed tables use far fewer than
`2^20` finite tags.  Every integer gain is positive, so `D>=1`.  Lemma 4.1
follows. `square`

## 5. Summing the marked encodings

Expand

\[
 A(W)^2=\sum_\alpha w(\alpha)^2
       +2\sum_{\alpha<\beta}w(\alpha)w(\beta).         \tag{5.1}
\]

Fix a coding type and all its integer parameters.  Lemma 4.1 and (3.5), with
`Z=40Y/D`, bound its core tuples by

\[
 2^{12}\left({40Y\over D}\right)^2
 \left(1+\log_+{40Y\over D}\right)^2.                \tag{5.2}
\]

Every unweighted auxiliary run length enters `D`; summing it costs

\[
 \sum_{r\ge1}{1\over r^2}<2,
 \qquad
 \sum_{r\ge0}{1\over(1+r)^2}<2.                       \tag{5.3}
\]

There are at most four such parameters.

For a same heavy atom of magnitude `n`, the mark weight `n^2` exactly
cancels the `n^{-2}` in (5.2).  Since `D<=40Y` for every nonempty encoding,
only `n<=40Y` can occur.  Put

\[
 H=\min(h,\lfloor40Y\rfloor).
\]

Its total remaining sum is at most

\[
 \sum_{n=2}^{H}\left(1+\log{40Y\over n}\right)^2
 \le H\left[A^2+2A+2\right],\qquad
 A=1+\log{40Y\over H}.                                \tag{5.4}
\]

This follows by comparing the decreasing summand with its integral; the
antiderivative of `(1+log(Z/t))^2` is
`t[(1+log(Z/t))^2+2(1+log(Z/t))+2]`.

A same light atom leaves weight `1`.  For two distinct heavy atoms, the
residual marked weight is `1/(nm)`.  Heavy--light and light--light pairs leave
respectively `1/n` and `1`.  All non-heavy-diagonal contributions are bounded
by

\[
 \left(1+\log(40Y)\right)^4,                           \tag{5.5}
\]

because `sum_{n<=40Y}1/n<=1+log(40Y)` and the convolution logarithm in
(5.2) is no larger than the same quantity.  This includes a light atom
absorbed into a tagged core: its run length is then counted by that core in
`C_j`, not by an omitted auxiliary sum.

### 5.1 Converting absolute logs to the required two regimes

If `1<=Y<=q`, then

\[
 {\left(1+\log(40Y)\right)^4\over Y}
 \le(1+\log40)^4<484,                                 \tag{5.6}
\]

because the ratio decreases for `Y>=1`.  The heavy-diagonal sum itself is at
most `2^8Y`.  Indeed, by (5.4), with `t=H/Y<=40`,

\[
 \sum_{n=2}^H\left(1+\log{40Y\over n}\right)^2
 \le H(A^2+2A+2)
 =Yt\left[\left(1+\log{40\over t}\right)^2
   +2\left(1+\log{40\over t}\right)+2\right]
 \le200Y<2^8Y.                                        \tag{5.7}
\]

The last function is increasing on `0<t<=40`, since its derivative after
multiplication by `Y` is `(1+log(40/t))^2>=0`.  The case `q=3` has no heavy
sum.

If `Y>=q`, put `L=log(Y/q)` and `R=1+L`.  The heavy-diagonal sum in (5.4) is
at most

\[
 2^5qR^2.                                               \tag{5.8}
\]

Here `H=h`, `h<=q/2`, and `q/h<=5/2`.  Thus
`A=1+log(40Y/h)<=R+log100`, and the same integral calculation gives

\[
 {H(A^2+2A+2)\over qR^2}
 \le {1\over2}\left[1+{2(1+\log100)\over R}
 +{(\log100)^2+2\log100+2\over R^2}\right]<32.        \tag{5.9}
\]

The bracketed expression decreases for `R>=1`; the strict last inequality is
checked at `R=1`.

Furthermore

\[
 (1+\log(40Y))^4
 \le2^{13}\bigl(q+R^4\bigr).                          \tag{5.10}
\]

Indeed, `(a+b+c)^4<=27(a^4+b^4+c^4)`,
`1+log40<4.7`, and

\[
 (\log q)^4\le5q                                      \tag{5.11}
\]

for `q>=3`; the continuous maximum of `(log q)^4/q` occurs at `q=e^4` and
is `4^4/e^4<4.689`.

Since `R>=1`, the `q` in (5.10) is at most `qR^2`; together with (5.8) this
is exactly the high-regime shape `qR^2+R^4` in `(DH_{2,4})`.

### 5.2 Constant audit and conclusion

The deliberately loose ceilings are:

| source | factor ceiling |
|---|---:|
| core convolution (3.5) | `2^12` |
| finite coding tags | `2^20` |
| `(4pi^2)^2<40^2` | `<2^11` |
| four auxiliary zeta sums | `<2^4` |
| harmonic/regime conversion | `2^13` |
| pair ordering and (2.7) | `<2^5` |

Their product is below `2^65`.  The Ford term `2#\{x<=Y\}<=2Y^2`, empty
cores, omitted endpoints, and all earlier inequalities are therefore covered
upward by

\[
 C_4=2^{100}.                                          \tag{5.12}
\]

Combining (2.7), (5.1)--(5.12), and Ford proves `(DH_{2,4})`. `square`

The numerical ceiling check was:

```bash
/Users/za/.venvs/farey-rh/bin/python - <<'PY'
import math
print('pi_lt_22_over_7=',math.pi < 22/7)
print('forty_bound=',4*math.pi**2,'< 40')
print('log_envelopes_at_1=',(1+math.log(40))**4)
print('sup_logq4_over_q_at_e4=',4**4/math.e**4)
print('C4=',2**100)
PY
```

Output:

```text
pi_lt_22_over_7= True
forty_bound= 39.47841760435743 < 40
log_envelopes_at_1= 483.36619118199474
sup_logq4_over_q_at_e4= 4.688803555515951
C4= 1267650600228229401496703205376
```

## 6. Layer cake and conditional `(RATE)` assembly

Shimizu gives `x_X>=1`.  Tonelli's theorem gives the exact positive layer
cake

\[
 \sum_X k_X^2x_X^{-p}
 =p\int_1^\infty B_q(t)t^{-p-1}\,dt.                  \tag{6.1}
\]

For the low part of `(DH_{2,4})`,

\[
 \int_1^q t^{2-p}\,dt
 \le {q^{3-p}\over3-p}.                               \tag{6.2}
\]

For `a=p-2>0` and every integer `j>=0`,

\[
 \int_1^\infty u^{1-p}(\log u)^j\,du={j!\over a^{j+1}}. \tag{6.3}
\]

Expanding `(1+log u)^2` and `(1+log u)^4` gives exactly `J_2,J_4` in
(0.3).  Substitution `t=qu` proves (0.4).

Separate the two pure Chebyshev families and retain their already proved
exact trigonometric drift bound

\[
 E_{\rm Cheb}\le78.196133\,q^{-1.2}                  \tag{6.4}
\]

at the working point.  On the remaining matched population, assume the
N1-RATE relative drift envelope with constant `A`.  The MVT and
`2-lambda_q<=pi^2/q^2` give

\[
 E_{\rm match}
 \le2\pi^2A|s|pC_4
 \left[
 \left({1\over3-p}+J_2(p)\right)q^{1-p}
 +J_4(p)q^{-p}\right].                                \tag{6.5}
\]

Add the referee-confirmed `(FW)` contribution

\[
 E_{\rm wrap}\le pC_1G(p)q^{1-p},\quad
 C_1=128(1+\log2),\quad
 G(p)={1\over p-2}+{1\over(p-2)^2}.                   \tag{6.6}
\]

Thus the leading exponent is `p-1`.  The fourth relative logarithm changes
the constant through `J_4`; it does not change the power of `q`.

At `s=1.1+1.5i`, `p=2.2`,

\[
 J_2=305,\qquad J_4=91605,\qquad
 {1\over3-p}+J_2=306.25.                               \tag{6.7}
\]

For `q>=12`, absorb the `q^{-p}` term using `1/q<=1/12`.  With every decimal
rounded upward,

 \[
 E_D(q)\le
 \left(641373.444\,A C_4+14381.904\right)q^{-1.2}.     \tag{6.8}
\]

Using the prior high-precision evaluation
`|M(1.1+1.5i)|=1.436942099375310694...<1.436942100` and multiplying the
already upward-rounded coefficients in (6.8), the corresponding scattering
bound is

\[
 \boxed{
 E_R(q)\le C_Rq^{-1.2},\qquad
 C_R=921616.504\,A C_4+20665.964.}                    \tag{6.9}
\]

This constant is intentionally enormous because `C_4` was rounded to
`2^100`.  The point of the theorem is the uniform exponent and the closure of
the finite-height two-mark logic, not constant optimization.

The upward-rounded coefficients and the new high-regime integral ceiling were
replayed together:

```bash
/Users/za/.venvs/farey-rh/bin/python - <<'PY'
from mpmath import mp
mp.dps=50
p=mp.mpf('2.2'); sig=mp.mpf('1.1')
sabs=mp.sqrt(sig**2+mp.mpf('1.5')**2); a=p-2
J2=1/a+2/a**2+2/a**3
J4=1/a+4/a**2+12/a**3+24/a**4+24/a**5
F=1/(3-p)+J2+J4/12
match=2*mp.pi**2*sabs*p*F
C1=128*(1+mp.log(2)); G=1/a+1/a**2
wrap=p*C1*G; cheb=mp.mpf('78.196133')
M=mp.mpf('1.436942100') # upward ceiling
c=mp.log(100)
high=mp.mpf('.5')*(1+2*(1+c)+(c*c+2*c+2))
base=(mp.mpf(56155)-mp.log(mp.mpf('.6603')))/(mp.mpf('1.2')*mp.mpf('1.827324e-5'))
for key,val in [('J2',J2),('J4',J4),('F_absorbed_q_ge_12',F),
 ('match_coefficient',match),('wrap',wrap),('wrap_plus_cheb',wrap+cheb),
 ('scattering_from_rounded_match',M*mp.mpf('641373.444')),
 ('scattering_from_rounded_fixed',M*mp.mpf('14381.904')),
 ('high_diag_ratio_R1',high),('R5_base',base)]:
 print(key,mp.nstr(val,30))
PY
```

Output:

```text
J2 305.0
J4 91605.0
F_absorbed_q_ge_12 7940.0
match_coefficient 641373.443484015054908695422243
wrap 14303.7073813704179739567769621
wrap_plus_cheb 14381.9035143704179739567769621
scattering_from_rounded_match 921616.5035055924
scattering_from_rounded_fixed 20665.9633357584
high_diag_ratio_R1 22.3141365929329787571952985959
R5_base 2560913073.84467585803874126417
```

## 7. R5 arithmetic against the continuous certificate

The binding certificate is the strict downward-rounded margin

\[
 d_*>0.6603.
\]

The propagated R5 inequality from `DH2_RENEWAL_PROOF_SOL.md` is

\[
 \log E_3(q)<56155+c_0\log C_R-\alpha c_0\log q,
 \qquad c_0=1.827324\times10^{-5}.                     \tag{7.1}
\]

With `alpha=1.2`, the exact base calculation is

```text
(56155-log(0.6603))/(1.2*1.827324e-5)
= 2560913073.844676...
```

Rounding the required lower bound on `log q` upward gives (0.6):

\[
 \log q>2.560914\times10^9+{5\over6}\log C_R.         \tag{7.2}
\]

Even if `A=1`, the huge explicit `C_4` adds only about `69.21` to the
right-hand side.  This does **not** certify an R5 threshold: N1-RATE, its
activation threshold, and the remaining R5 gates must still be supplied.

## 8. The proposed alternative routes

### 8.1 Global `sharp_no_wrap`

**FALSE as an inference.**  The machine theorem assumes total raw depth
`k<=q-1`; matched words need not satisfy it.  The valid use here is local:
balanced heavy blocks have `n<=h`, so their sine entries obey (2.3).

### 8.2 Induction on marks

A second application of the theta one-mark theorem would retain the wrong
`y<=Y` cutoff and would distort the marked measure at endpoint
normalization.  The endpoint-core coding above is the corrected
renewal-of-renewals: normalize every fragment, retain the deleted run lengths
in bridge gains, and apply Ford only to the resulting finite double cosets.

### 8.3 Holder interpolation

**FALSE as a closure argument.**  The exactly computable fourth moment is on
the pure Chebyshev subset.  Holder would require an upper fourth moment on the
same full finite-height population.  A subset fourth moment points in the
wrong direction.  The one-defect family `w_(2,k)` also disproves the claim
that every non-Chebyshev word has logarithmic depth.

## 9. Self-grade against `DH2_RENEWAL_PROOF_SOL.md` Section 10

| requirement | result | grade |
|---|---|---|
| retain `x/m` | used the proved identity `x/m=1` | **PASS** |
| control endpoint comparison | counted directly at `x<=Y`; no theta-cutoff transfer | **PASS** |
| survive the one-defect identity | heavy same-atom diagonal and two-cut coding include it | **PASS** |
| genuine renewal theorem with depth cost | Lemma 4.1 plus Ford convolution controls the full second moment | **PASS** |
| treat Chebyshev extremals exactly | retained the exact trigonometric sub-bound before applying N1 to the residual | **PASS** |
| prove the exact all-height tail (5.2) | no pointwise tail; proved cumulative `(DH_{2,4})` | **PARTIAL** |
| complete conditional assembly honestly | exponent, constants, and R5 arithmetic displayed; remaining assumptions named | **PASS** |

**Grade for exact `(DH_2)`: PARTIAL — its sharper log powers remain
CONJECTURAL.**

**Grade for the two-mark finite-height ingredient needed by `(RATE)`: PASS,
paper-level, via `(DH_{2,4})`.**

## 10. Claim ledger

| claim | verdict | proof/receipt |
|---|---|---|
| exact `y<=100` same/different-run split | **CERTIFIED-FINITE** | Section 1.2 exact integer replay |
| `x<=Y` may be replaced by `y<=Y` | **FALSE as an inference** | `q=3`: `(x,y)=(34,1970),(89,11482)` |
| whole-word v29 no-wrap applies to every matched word | **FALSE** | its hypothesis is `k<=q-1` |
| heavy block entry lower bound `N_{ij}>=n/pi` | **PROVED** | sine concavity and endpoint reflection, (2.3) |
| endpoint-normalized core count `<=2T^2` | **PROVED, paper-level dependency** | Route-B injection plus Ford, (3.4) |
| one-/two-cut coding and product gain | **PROVED here** | complete boundary tables, Lemma 4.1 |
| log-weakened finite-height renewal `(DH_{2,4})` | **PROVED here** | Sections 2--5 |
| exact sharper `(DH_2)` | **CONJECTURAL** | extra log powers not removed |
| conditional epsilon exponent at `sigma=1.1` | **`alpha=1.2`** | Section 6 |
| strict R5 threshold | **NOT CERTIFIED** | Section 7; other gates remain |

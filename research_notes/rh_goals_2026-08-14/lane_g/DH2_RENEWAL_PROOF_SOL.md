# `(DH_2)` weighted renewal: endpoint monotonicity, the proved one-mark diagonal, and the remaining two-mark gap

**Date:** 2026-08-18

**Program:** `(RATE)`, lane G

**Interpreter:** `/Users/za/.venvs/farey-rh/bin/python`
**Write scope:** this file only

## 0. Verdict

The requested uniform estimate

\[
 B_q(Y):=
 \sum_{X\in\mathcal C_q:m_X\le Y}
 k_X^2\frac{x_X}{m_X}
 \le C Y^2
 \begin{cases}
 Y,&1\le Y\le q,\\
 q(1+L)+(1+L)^2,&Y\ge q,
 \end{cases}
 \qquad L=\log(Y/q),                                    \tag{DH_2}
\]

is **NOT PROVED**. It remains **CONJECTURAL / OPEN**. I found no
counterexample: the complete exact theta windows through `y=50`, the fresh
exact theta windows through `y=100`, and the finite-level quotient-state
replays all fit `(DH_2)` with substantial margin. Finite data do not supply
the missing uniform tail theorem.

Three rigorous corrections/advances are proved here.

1. **Endpoint comparison is closed.** For every balanced Route-B matched
   class,

   \[
   \boxed{x_X\le y_X.}                                  \tag{E}
   \]

   Therefore `m_X=x_X` and the allegedly load-bearing comparison factor is
   exactly

   \[
   \boxed{x_X/m_X=1.}                                   \tag{E'}
   \]

   The remaining count is the finite-height count
   `B_q(Y)=sum_{x_X<=Y} k_X^2`; one still cannot replace its cutoff by
   `y_X<=Y`, because (E) has the wrong direction for that replacement.

2. **The marked-letter product in `(FW)` sharpens.** With the notation of
   `FW_RENEWAL_COUNT_SOL.md`, canonical signs give

   \[
   |c(PV)|<|AB|,\qquad
   |c(PR^aV)|>(|a|-1)|AB|.                              \tag{F+}
   \]

   Hence `|a||A||B|<Y` already for every marked digit `|a|>=2`, not only
   for `|a|>=4`.

3. **The one-mark diagonal has exactly the required renewal scale.** If
   `D_q^theta(Y)` sums `a_j^2` over all marked canonical digits `|a_j|>=2`
   in the balanced theta image with `y<=Y`, then

   \[
   \boxed{
   D_q^\theta(Y)
   \le 32(2+\log3)Y^2\min(Y,q)
       \bigl(1+\log_+(Y/q)\bigr).}                     \tag{D}
   \]

The proof stops at a precise, smaller gap. Raw deformation depth is bounded
by the sum of heavy canonical-letter costs plus the number of light runs.
Squaring produces (i) the diagonal in (D), (ii) pairs of marked heavy
letters, and (iii) the second moment of the light-run count. A genuine
**two-mark renewal theorem at the finite height `x<=Y`** is still required
for (ii)--(iii). Neither `(FW)`, log-convexity, nor Cauchy--Schwarz proves it.

Thus the honest program verdict is:

| statement | verdict |
|---|---|
| matched endpoint inequality `x<=y`, hence `x/m=1` | **PROVED here, paper-level** |
| sharpened marked-letter gain `(F+)` | **PROVED here, paper-level** |
| one-mark diagonal count `(D)` | **PROVED here, paper-level** |
| full pointwise tail (5.2) / `(DH_2)` | **CONJECTURAL / OPEN** |
| full `(RATE)` exponent | **UNDEFINED without `(DH_2)` and N1-RATE** |
| conditional exponent at `sigma=1.1` | **`alpha=1.2`** |
| strict R5 test `E_3(q)<0.6603` | **NOT CERTIFIED** |

## 1. Receipts before claims

### 1.1 Bound inputs and hashes

The required reading order was `DH_DEPTH_LAW_SOL.md` Section 5, then Section
3, then Section 4, followed by `FW_RENEWAL_COUNT_SOL.md` and
`FW_REFEREE.md`. The executable inputs were checked by:

```bash
/Users/za/.venvs/farey-rh/bin/python --version
sha256sum \
  research_notes/rh_goals_2026-08-14/lane_g/DH_DEPTH_LAW_SOL.md \
  research_notes/rh_goals_2026-08-14/lane_g/FW_RENEWAL_COUNT_SOL.md \
  research_notes/rh_goals_2026-08-14/lane_g/FW_REFEREE.md \
  research_notes/rh_goals_2026-08-14/lane_g/law_probes/r1_coset_enum.py \
  research_notes/rh_goals_2026-08-14/lane_g/law_probes/r1_coset_enum_complete_X50.json
```

Output:

```text
Python 3.13.13
9146ecebfdb976ceb3df49c0e7789bc5a82ef2116ceb1f02d6a89d32f6c602d8  DH_DEPTH_LAW_SOL.md
70cf0a9d12cdc6938c431bd1246b0ca18d929c151fb98399a8e94a75d7f6fd3c  FW_RENEWAL_COUNT_SOL.md
39c2e0d10a2ef1bb880e34cd4ca53bc280b451305cac871eb2244bb52e490058  FW_REFEREE.md
4d068726142d945e846a336b5e3e6e8fd34233e16e3e0c7ffbb405411114732b  r1_coset_enum.py
c1efc1336b1c2a1ccdcb9698653442788270e0f1466738b119d747f2acacaf20  r1_coset_enum_complete_X50.json
```

The abbreviated filenames in the displayed output have the full paths from
the command. `FW_REFEREE.md` confirms `(FW)` only at paper level; no claim
below upgrades it to machine formalization.

### 1.2 Exact `q=8,...,48` joint-window replay

The following command reuses only the self-contained canonicalizer already
printed in `DH_DEPTH_LAW_SOL.md`, enumerates all 263 exact theta keys with
`y<=50`, applies the proved balanced-image test, computes `(k,x,y,m)`, and
tests both (5.2) and `(DH_2)` at every event cutoff. The loop is over every
integer `q=8,...,48`, not a sampled grid.

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from pathlib import Path
P=Path('research_notes/rh_goals_2026-08-14/lane_g/DH_DEPTH_LAW_SOL.md')
s=P.read_text(); a=s.index('from collections import Counter',s.index('self-contained stdout-only'))
b=s.index('\nPY\n',a); exec(s[a:b].split('q=12;')[0])
base=[(c,d,from_cd(c,d),depth(c,d)) for c in range(1,26)
      for d in range(2*c) if gcd(c,d)==1 and (c+d)%2]
out=[]
for q in range(8,49):
 A=set(range(-((q-1)//2),0))|set(range(1,q//2+1)); lam=2*mp.cos(mp.pi/q); z=[]
 for c,d,w,k in base:
  if all(t=='Q' or t in A for t in w):
   x=c_eval(w,lam); y=mp.mpf(2*c); m=min(x,y); z.append((m,k,x/m,y/x))
 B=sum(k*k*r for m,k,r,yx in z); dh=tail=mp.mpf(0)
 for Y in sorted({m for m,k,r,yx in z}):
  R=1+max(mp.log(Y/q),0); L=min(Y,q)
  BY=sum(k*k*r for m,k,r,yx in z if m<=Y); dh=max(dh,BY/(Y*Y*(q*R+R*R)))
  for K in range(1,max(k for m,k,r,yx in z)+1):
   T=sum(r for m,k,r,yx in z if m<=Y and k>=K)
   tail=max(tail,T/(Y*Y*R/K*min(1,(L/K)**2)))
 out.append((q,len(z),max(k for m,k,r,yx in z),B,max(r for m,k,r,yx in z),tail,dh))
print('theta_y<=50',len(base),'q_rows',len(out),'all_x_over_m=',max(r[4] for r in out))
print('q n kmax B tailmax DH2max')
for r in out:
 if r[0] in (8,12,16,24,32,40,48):
  print(r[0],r[1],r[2],mp.nstr(r[3],10),mp.nstr(r[5],9),mp.nstr(r[6],9))
print('ranges tail=',mp.nstr(min(r[5] for r in out),9),mp.nstr(max(r[5] for r in out),9),
      'DH2=',mp.nstr(min(r[6] for r in out),9),mp.nstr(max(r[6] for r in out),9))
PY
```

Output:

```text
theta_y<=50 263 q_rows 41 all_x_over_m= 1.0
q n kmax B tailmax DH2max
8  164 7  2369.0  0.428932188 0.204934268
12 204 8  3729.0  0.394882233 0.211248188
16 223 9  4867.0  0.385769766 0.214704440
24 236 12 6067.0  0.364024621 0.215736890
32 244 16 7647.0  0.338762921 0.219364858
40 252 20 10251.0 0.338740552 0.222718135
48 260 24 14135.0 0.329826058 0.222183672
ranges tail= 0.322838329 0.428932188 DH2= 0.199830613 0.226352570
```

Here `B` is the restricted joint-window sum, not the global `B_q(50)`:
the window is exact on the theta side (`y<=50`), while `x<=50<y` classes are
not included. The integer counts and depths are exact. Before Theorem (E),
the endpoint evaluations were 60-digit diagnostics; Theorem (E) proves their
observed direction globally.

### 1.3 Fresh deeper exact theta window

The following deeper replay changes the exact theta range to `c=1,...,50`,
equivalently `y<=100`:

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from pathlib import Path
from math import gcd
import mpmath as mp
P=Path('research_notes/rh_goals_2026-08-14/lane_g/DH_DEPTH_LAW_SOL.md')
s=P.read_text(); a=s.index('from collections import Counter',s.index('self-contained stdout-only'))
b=s.index('\nPY\n',a); exec(s[a:b].split('q=12;')[0])
base=[(c,d,from_cd(c,d),depth(c,d)) for c in range(1,51)
      for d in range(2*c) if gcd(c,d)==1 and (c+d)%2]
print('exact_theta_keys_y_le_100=',len(base))
print('q n kmax B100 max_x_over_m')
for q in (8,12,16,24,32,48):
 A=set(range(-((q-1)//2),0))|set(range(1,q//2+1)); lam=2*mp.cos(mp.pi/q); z=[]
 for c,d,w,k in base:
  if all(t=='Q' or t in A for t in w):
   x=c_eval(w,lam); y=mp.mpf(2*c); z.append((k,x/min(x,y)))
 print(q,len(z),max(k for k,r in z),
       mp.nstr(sum(k*k*r for k,r in z),10),mp.nstr(max(r for k,r in z),10))
PY
```

Output:

```text
exact_theta_keys_y_le_100= 1037
q n kmax B100 max_x_over_m
8  588 8  11049.0 1.0
12 764 10 18821.0 1.0
16 847 11 24529.0 1.0
24 920 14 32817.0 1.0
32 960 18 41661.0 1.0
48 984 24 50533.0 1.0
```

The finite-level quotient-state replay through `x<=100` independently found
maximal restricted `(DH_2)` ratios `0.204934, 0.211248, 0.215737, 0.222184`
at `q=8,12,24,48`, and (5.2) ratios
`0.428932, 0.394882, 0.364025, 0.329826`. Its pruned state graph exhausted in
the displayed finite box, but `M2_LOCALIZATION_THEOREM_SOL.md` already gives
an outside-then-reentry counterexample to treating height pruning as a global
completeness theorem. These values are **FINITE DIAGNOSTICS**, not proof.

## 2. The exact target and layer cake

Put

\[
 T_q(Y,K):=
 \sum_{\substack{X:m_X\le Y\\k_X\ge K}}\frac{x_X}{m_X}.
\]

The exact identity is

\[
 B_q(Y)=\sum_{K\ge1}(2K-1)T_q(Y,K).                   \tag{2.1}
\]

The pointwise tail requested in `DH_DEPTH_LAW_SOL.md` is

\[
 T_q(Y,K)\le C\frac{Y^2R}{K}
 \min\left\{1,\left(\frac{L}{K}\right)^2\right\},
 \quad L=\min(Y,q),\quad R=1+\log_+(Y/q).              \tag{2.2}
\]

Splitting (2.1) at `K=L` gives `O(Y^2RL)`: below `L`, each summand is
`O(Y^2R)`; above `L`, it is `O(Y^2RL^2/K^2)`. Thus (2.2) genuinely proves
`(DH)` and hence `(DH_2)`. Conversely, a moment-generating-function slogan
does not replace (2.2); the upper tail or an equivalent second-derivative
bound is the theorem that must be supplied.

## 3. Endpoint comparison — proved

### 3.1 Nonnegative normal form

Work first in source coordinates:

\[
 Q=\begin{pmatrix}0&-1\\1&0\end{pmatrix},\qquad
 R_\lambda=\begin{pmatrix}0&-1\\1&\lambda\end{pmatrix}.
\]

Set `u_0=0`, `u_1=1`, `u_{j+1}=lambda u_j-u_{j-1}` and

\[
 M_a(\lambda)=
 \begin{pmatrix}u_a&u_{a+1}\\u_{a-1}&u_a\end{pmatrix}.
\]

`LAW_U2B_CLOSURE.md` proves the exact polynomial identities

\[
 QR_\lambda^a=-M_a(\lambda),\qquad
 QR_\lambda^{-a}=M_a(\lambda)^t\qquad(a\ge1).          \tag{3.1}
\]

For a signed nonzero integer `a`, let `N_a` be `M_a` for `a>0` and
`M_|a|^t` for `a<0`. A canonical Route-B word is

\[
 W=R^{a_0}QR^{a_1}Q\cdots QR^{a_r}.
\]

Using `Q^2=-I`, (3.1) gives, up to a harmless common sign,

\[
 W=Q N_{a_0}N_{a_1}\cdots N_{a_r}.                   \tag{3.2}
\]

Consequently its absolute source lower-left entry is

\[
 C_\lambda(W)=
 \left(N_{a_0}(\lambda)\cdots N_{a_r}(\lambda)\right)_{11}. \tag{3.3}
\]

### 3.2 Monotonicity on the balanced alphabet

For `lambda=2cos(theta)`,

\[
 u_j(\lambda)=\frac{\sin(j\theta)}{\sin\theta}.
\]

The proved monotonicity lemma in `LAW_U2B_CLOSURE.md` says that `u_j` is
nonnegative and nondecreasing in `lambda` on
`[2cos(pi/j),2]`. In the Route-B image,

\[
 |a_i|\le h:=\lfloor q/2\rfloor.
\]

Every entry in `N_ai` is one of `u_|a|-1,u_|a|,u_|a|+1`; its index is at
most `h+1<=q`. Hence every factor is entrywise nonnegative and entrywise
nondecreasing throughout `[lambda_q,2]`. Expanding the `(1,1)` entry of the
product as a sum over state paths proves

\[
 C_{\lambda_q}(W)\le C_2(W).                           \tag{3.4}
\]

Width-one conjugation multiplies a source lower-left entry by `lambda`.
Therefore

\[
 x_X=\lambda_q C_{\lambda_q}(W)
 \le2C_2(W)=y_X,                                       \tag{3.5}
\]

which proves (E). No numerical monotonicity assumption is used.

**Consequence.** For every matched class,

\[
 m_X=x_X,\qquad \frac{x_X}{m_X}=1,\qquad
 B_q(Y)=\sum_{X:x_X\le Y}k_X^2.                       \tag{3.6}
\]

This closes the comparison **weight**, not the comparison **cutoff**. From
`x<=y`, `y<=Y` implies `x<=Y`; the converse needed to replace the finite
cutoff by a theta cutoff is false as a logical inference and is not proved.

## 4. A depth correction: the old `14>q-1` witness is invalid

`DH_DEPTH_LAW_SOL.md` counts the unreduced expansion of

```text
(2,Q,2,Q,2,Q,2,Q,2)
```

as `5*2+4=14` copies of `Q`. This is not the reduced RateCore depth.
With `R=QS`, cancelling adjacent `Q^2` gives the reduced exponent list

```text
[1,2,2,2,2]
```

in `Q S^{n_1}Q...S^{n_5}Q`, so the true depth is `6`, not `14`. Fresh
receipt:

```text
q 12 n 5 true_reduced_depth 6 x 571.7883832488647534320286 y 724
n=5_reduced_exponent_list= [1, 2, 2, 2, 2]
```

Thus the stated witness does not show that matched depth exceeds `q-1`.

The global conclusion remains true, with a corrected witness. Let
`W_n=(R^2Q)^{n-1}R^2`. Every canonical exponent is `2`, so `W_n` is in the
balanced image for every `q>=4`; its reduced RateCore list is
`[1,2,...,2]` and its true depth is `n+1`. Taking `n=q` gives
`k=q+1>q-1`. At `q=12,n=12`:

```text
q 12 n 12 true_reduced_depth 13
x 4349511.893884617017366506
y 7300802
```

The theta heights satisfy `y_0=2`, `y_1=4`,
`y_{n+1}=4y_n-y_{n-1}`. The corrected family is therefore exponentially
high; it invalidates a global application of `sharp_no_wrap` but does not
violate `(DH_2)`.

The one-defect identity from Section 3 of `DH_DEPTH_LAW_SOL.md` is unchanged:
it is already stated in the reduced exponent-list convention. In particular,
`w_(2,k)=(2,1,...,1)` has true depth `k` and theta height `6k-4`; its
Route-B boundary reduction contains a canonical exponent of size `k`, so it
is matched up to the balanced cutoff. Any proof must still count it.

## 5. Sharpening the `(FW)` factorization

Use the notation of `FW_RENEWAL_COUNT_SOL.md`. At an arbitrary marked
canonical digit,

\[
 W=PR^aV,\qquad A=d_P-c_P,\qquad B=\alpha_V+\gamma_V,
\]

and

\[
 c(W)=c(PV)+aAB,\qquad c(PV)=c_PB+A\gamma_V.           \tag{5.1}
\]

For a nonempty prefix, the proved recurrence gives

\[
 A=-U_r,\qquad c_P=\frac{U_r-U_{r-1}}2,\qquad
 \left|\frac{U_{r-1}}{U_r}\right|<1.
\]

Therefore

\[
 \frac{c_P}{A}=-\frac12+\frac{U_{r-1}}{2U_r}\in(-1,0). \tag{5.2}
\]

For the empty prefix the ratio is `0`. Applying the same result to `V^-1`,
whose bottom row is `(-gamma_V,alpha_V)` and whose scale is `B`, gives

\[
 \frac{\gamma_V}{B}\in(0,1)                           \tag{5.3}
\]

for a nonempty suffix, and `0` for the empty suffix. Dividing (5.1) by
`AB` now gives

\[
 \frac{c(PV)}{AB}=\frac{c_P}{A}+\frac{\gamma_V}{B}
 \in(-1,1).
\]

Hence

\[
 \boxed{|c(PV)|<|AB|},\qquad
 \boxed{|c(W)|>(|a|-1)|AB|}.                          \tag{5.4}
\]

For `n=|a|>=2`, `n<=2(n-1)`. If theta height `y(W)=2|c(W)|<=Y`, then

\[
 \boxed{n|A||B|<Y.}                                   \tag{5.5}
\]

This proves the marked product gain for every nonunit digit. It also removes
the small-`q` Ford patch from the symbolic `(FW)` proof, although the already
confirmed `(FW)` statement and its safely rounded constant are left unchanged.

## 6. The proved one-mark diagonal renewal theorem

Let `I_q` be the canonical theta image and define

\[
 D_q^\theta(Y):=
 \sum_{\substack{W\in I_q\\y(W)\le Y}}
 \sum_{j:|a_j|\ge2}|a_j|^2.                           \tag{6.1}
\]

For fixed `n>=2`, count marked occurrences `(W,j)` with `|a_j|=n`. The cut
is injective at the marked-word level. The prefix and suffix multiplicity
bounds from `(FW)` give at most `4r` and `4s` choices at scales `r=|A|` and
`s=|B|`; there are two signs of `a`. By (5.5),

\[
 N_n(Y)
 \le32\sum_{rs\le Y/n}rs
 \le32\left(\frac Yn\right)^2
       \left(1+\log\frac Yn\right).                   \tag{6.2}
\]

Put `H=min(floor(Y),floor(q/2))`. Summing `n^2 N_n(Y)` gives

\[
 D_q^\theta(Y)
 \le32Y^2\sum_{n=2}^{H}\left(1+\log\frac Yn\right).  \tag{6.3}
\]

The integral lower bound

\[
 \log(H!)\ge\int_1^H\log t\,dt=H\log H-H+1
\]

implies

\[
 \sum_{n=2}^{H}\left(1+\log\frac Yn\right)
 \le H\left(2+\log\frac YH\right).                   \tag{6.4}
\]

If the sum is nonempty, then `q>=4`, `Y>=2`, and

\[
 H\le\min(Y,q),\qquad
 \log(Y/H)\le\log3+\log_+(Y/q).
\]

Combining (6.3)--(6.4), and rounding the upper constant upward, proves

\[
 D_q^\theta(Y)
 \le32(2+\log3)Y^2\min(Y,q)
       \bigl(1+\log_+(Y/q)\bigr),                     \tag{6.5}
\]

with `32(2+log3)<99.156`. For `q=3` or `Y<2`, the left side is zero.

This is a genuine weighted renewal count and it survives the one-defect
family: the long parabolic run is charged to its large canonical exponent.
It is not yet the depth second moment.

### 6.1 Exact residual after the diagonal

Expanding `R=QS` and cancelling `Q^2` proves the elementary block bound

\[
 k(W)\le1+2
 \sum_{j:|a_j|\ge2}|a_j|+2\ell(W),                    \tag{6.6}
\]

where `ell(W)` is the number of maximal same-sign runs made entirely of
`+1` or entirely of `-1` canonical exponents. This deliberately loose upper
bound follows by expanding `R=QS`: same-sign light letters merge into one raw
`S`-exponent, every heavy letter pays its full unreduced `Q`-cost, and the
factor `2` pays every intervening sign-change separator. No cancellation is
used to round the upper bound downward.

Writing `s(W)=sum_heavy |a_j|`,

\[
 s(W)^2=
 \sum_{j:|a_j|\ge2}|a_j|^2
 +2\sum_{i<j\atop |a_i|,|a_j|\ge2}|a_i a_j|.          \tag{6.7}
\]

Equation (6.5) controls the first term after summing over `y<=Y`. The open
terms are

\[
 \sum_{y\le Y}\sum_{i<j}|a_i a_j|,
 \qquad
 \sum_{y\le Y}\ell(W)^2,                              \tag{6.8}
\]

and, for `(DH_2)`, they must be controlled with the finite cutoff `x<=Y`,
not merely `y<=Y`. A one-mark estimate cannot bound the first expression:
it is intrinsically a two-mark renewal count. Pulling out the pointwise
number of marks introduces an external `log Y` and misses the claimed scale.

This is the exact place where the block-renewal proof remains open.

## 7. Why the other proposed strategies do not close the gap

### 7.1 Transfer operator / log-convexity

For the finite weighted measure, put

\[
 M_q(u;Y)=\sum_{x_X\le Y}e^{u k_X}.
\]

Then `M_q''(0;Y)=B_q(Y)`. Log-convexity gives

\[
 M_q(0)M_q''(0)\ge M_q'(0)^2,                         \tag{7.1}
\]

a **lower** bound on the desired second moment. An upper bound on the second
derivative at the `q`-uniform spectral radius would be a valid route, but it
is precisely a depth-cost renewal theorem equivalent in strength to (2.2).
A fixed-`q` finite truncation can enumerate; it does not prove uniformity as
the parabolic state degenerates when `q` grows.

**Verdict:** promising formalism, **UNCLOSED**, not refuted in principle.

### 7.2 Direct Cauchy--Schwarz

Cauchy--Schwarz gives

\[
 B_q(Y)^2\le
 \left(\sum_{x_X\le Y}1\right)
 \left(\sum_{x_X\le Y}k_X^4\right).                  \tag{7.2}
\]

Ford controls the first factor but the second is an unproved fourth moment,
strictly harder than the target. In the residue-fiber formulation from
`DENSITY_GAIN_ATTACK_SOL.md`, the weights are constant on a fixed fiber, so
the elementary Cauchy--Schwarz step is equality and supplies no density gain;
Parseval's zero mode is the full positive mass.

**Verdict:** the proposed positive-majorant Cauchy--Schwarz route is
**INSUFFICIENT**. A signed mean-zero reorganization would be a different,
currently conjectural argument.

## 8. Best proved comparison bound and conditional `(RATE)` assembly

Let `p=2sigma` with `2<p<3`. Two full subpieces are proved.

1. Referee-confirmed `(FW)` gives

   \[
   E_{\rm wrap}(q,s)
   \le pC_1G(p)q^{1-p},\qquad
   C_1=128(1+\log2),\quad
   G(p)=\frac1{p-2}+\frac1{(p-2)^2}.                  \tag{8.1}
   \]

2. The exact Chebyshev calculation in `DH_DEPTH_LAW_SOL.md` gives

   \[
   E_{\rm Cheb}(q,s)
   \le C_{\rm Cheb}(p,s)q^{1-p}.                      \tag{8.2}
   \]

Thus the rigorously established decomposition is

\[
 |D_q(s)-D_\theta(s)|
 \le E_{\rm wrap}+E_{\rm Cheb}+E_{\rm pair,res},      \tag{8.3}
\]

where the first two terms are `O(q^(1-p))` and no full bound is proved for
the nonnegative residual majorant.

At `s=1.1+1.5i`, `p=2.2`, and `q>=12`, fresh high-precision evaluation gives

```text
C1=216.7228391116729996054057115466466007137
C_wrap=14303.7073813704179739567769620786756471
C_Cheb=78.19613298153422645023317626336944426321
C_known_D=14381.90351435195220040701013834204509137
|M(s)|=1.436942099375310694140786290868275001847
C_known_scattering=20665.96262892605301063776279450410111606
```

Safe upward-rounded statement:

\[
 E_{\rm wrap}+E_{\rm Cheb}
 \le14381.904\,q^{-1.2},                               \tag{8.4}
\]

and the corresponding scattering subpiece is at most
`20665.963 q^-1.2`. These are **PARTIAL** constants, not a full epsilon.
Accordingly the best proved full exponent is **UNDEFINED**.

### 8.1 Conditional consequence of `(DH_2)`

Assume N1-RATE with constant `A`, `(DH_2)` with constant `C_2`, and the
confirmed `(FW)`. Define

\[
 F(p)=\frac1{3-p}+\frac1{p-2}+\frac1{(p-2)^2},
\]

\[
 H(p)=\frac1{p-2}+\frac2{(p-2)^2}+\frac2{(p-2)^3}.
\]

Layer cake, with every upper bound rounded upward, gives

\[
\begin{aligned}
 |D_q(s)-D_\theta(s)|
 \le{}&
 \left(2\pi^2A|s|pC_2F(p)+pC_1G(p)\right)q^{1-p}\\
 &+2\pi^2A|s|pC_2H(p)q^{-p}.                          \tag{8.5}
\end{aligned}
\]

The second relative logarithm contributes only `q^-p`; it does not change
the leading exponent. Therefore, **conditionally**,

\[
 \epsilon(q)=O(q^{-(p-1)}),\qquad
 \alpha=p-1=2\sigma-1.                                \tag{8.6}
\]

At `sigma=1.1`, `alpha=1.2`. This is conditional, not a RATE theorem.

## 9. R5 against the continuous defect certificate

The binding certificate is

\[
 d_*:=\inf_{|t-t_0|\le0.025}
 \left(1-|\phi_\infty(1/2+it)|\right)>0.6603,
\]

with raw lower endpoint
`0.660309770144522190093994140625...`. The strict R5 test is therefore

\[
 \boxed{E_3(q)<0.6603},                                \tag{9.1}
\]

not comparison with the sampled `0.6604` value.

If a full RATE estimate `E_R(q)<=C_R q^-alpha` were proved, the two R3/R5
propagation stages give

\[
 \log E_3(q)<56155+c_0\log C_R-\alpha c_0\log q,
 \qquad c_0=1.827324\times10^{-5}.                    \tag{9.2}
\]

For the conditional `alpha=1.2`, the strict upward-rounded requirement is

\[
 \log q>
 2.560914\times10^9+\frac56\log C_R.                  \tag{9.3}
\]

Because `(DH_2)`, N1-RATE, the full `C_R`, the RATE activation threshold,
and the remaining R5 gates are not proved, `q_0` is **UNDEFINED** and the
R5 verdict is **NOT CERTIFIED**. The partial bound (8.4) cannot be inserted
for the missing residual.

## 10. Self-grade against Section 5's requirements

| Section 5 requirement | result | grade |
|---|---|---|
| retain the exact weighted measure `x/m` | proved `x/m=1` on the whole balanced image | **PASS** |
| control endpoint comparison | proved `x<=y`; did not transfer `x<=Y` to `y<=Y` | **PARTIAL** |
| survive the one-defect identity | sharpened nonunit marked gain and diagonal count include it | **PASS** |
| supply a genuine renewal theorem with a depth cost | one-mark diagonal only; two-mark cross moment open | **FAIL** |
| treat Chebyshev extremals exactly | quoted the already proved `O(q^(1-p))` bound without weakening it | **PASS** |
| prove a uniform all-height tail such as (5.2) | finite tests only | **FAIL** |
| complete conditional Sections 6--8 honestly | exponent and R5 arithmetic stated conditionally; full exponent left undefined | **PASS** |

**Overall grade for the requested theorem: FAIL / OPEN.**
**Overall grade for gap reduction: 4 PASS, 1 PARTIAL, 2 FAIL.**

## 11. Final claim ledger

| claim | verdict | proof/receipt |
|---|---|---|
| old `(2,Q,...,2)` word has true depth 14 | **FALSE** | reduced list `[1,2,2,2,2]`, depth 6 |
| matched words always satisfy the v29 depth cutoff | **FALSE** | `W_q=(R^2Q)^(q-1)R^2`, true depth `q+1` |
| one-defect family is logarithmic in height | **FALSE** | `c_theta=6k-4` |
| matched endpoint order `x<=y` | **PROVED here** | nonnegative Chebyshev-block factorization, (3.1)--(3.5) |
| matched comparison factor `x/m=1` | **PROVED here** | immediate from `x<=y` |
| sharpened `|c(PV)|<|AB|` | **PROVED here** | signed prefix/suffix ratios, (5.2)--(5.4) |
| nonunit marked product `|a|AB<Y` | **PROVED here** | (5.4)--(5.5) |
| diagonal digit-square count `(D)` | **PROVED here** | (6.1)--(6.5) |
| transfer-operator log-convexity proves the upper second moment | **FALSE as an inference** | inequality points downward, (7.1) |
| Cauchy--Schwarz closes the second moment with current inputs | **FALSE as an inference** | requires an unproved fourth moment, (7.2) |
| `(DH_2)` | **CONJECTURAL / OPEN** | missing two-mark finite-height renewal theorem |
| full epsilon exponent | **UNDEFINED** | residual paired majorant unbounded |
| conditional epsilon exponent at `sigma=1.1` | **`alpha=1.2`** | (8.5)--(8.6) |
| strict R5 conclusion | **NOT CERTIFIED** | full RATE constant and activation gates absent |

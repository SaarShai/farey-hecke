# M2 localization theorem: sharp pre-wrap law, weighted-count criterion, and false global target

**Date:** 2026-08-18  
**Program:** (RATE), lane G, M2 critical path  
**Normalization:**

\[
 S=\begin{pmatrix}1&1\\0&1\end{pmatrix},\qquad
 Q_\lambda=\begin{pmatrix}0&-1/\lambda\\ \lambda&0\end{pmatrix},
 \qquad \lambda_N=2\cos(\pi/N).
\]

## 0. Verdict

The requested global geometric depth--height theorem is **FALSE**.  What is
true is a sharp finite no-wrap inequality:

\[
 \boxed{
 |c_w(\lambda_N)|\ge
 \lambda_N{\sin(k\pi/N)\over\sin(\pi/N)}
 \quad(1\le k\le N-1),}
 \tag{0.1}
\]

for every syntactically reduced word of \(Q\)-depth \(k\).  Equality is
attained by the all-\(+1\) and all-\(-1\) Chebyshev words.  In particular,

\[
 |c_w(\lambda_N)|\ge {2\lambda_N\over\pi}k
 \ge \left({4\over\pi}-{2\pi\over N^2}\right)k
 \qquad(1\le k\le N/2).
 \tag{0.2}
\]

The bound turns over after \(N/2\) and vanishes at the elliptic relation.
There is no positive lower bound growing with unrestricted raw depth.

The proposed full \(k^2\)-weighted summation on
\(1<\sigma\le3/2\) is also **FALSE** without an \(N\)-dependent restriction.
At the theta endpoint the distinct Chebyshev cosets, represented by the
selected raw words \(w_k=(QS)^{k-1}Q\), have depth \(k\) and \(c_k=2k\).
Thus this selected-word positive majorant contains

\[
 \sum k^2(2k)^{-2\sigma}
 \tag{0.3}
\]

diverges for \(1<\sigma\le3/2\).  At \(\sigma=3/2\), even the natural
depth-\(N\) truncation is logarithmic.  Thus the absolute per-term route can
at best give

\[
 N^{-2}\log N
 \tag{0.4}
\]

at the endpoint, not \(C N^{-2}\).  An endpoint estimate without the logarithm
would require cancellation or another argument not based on the positive
\(k^2\)-majorant.

The missing \(N\)-dependent localization profile is now isolated.  If
\({\cal I}_N\) is a canonical matched image, \(y_w=|c_w(2)|\), and \(k_w\) is
the raw \(Q\)-count of its selected boundary-reduced theta \(Q,S\)-lift, set

\[
 H_N(T):=\sum_{w\in{\cal I}_N:\ y_w\le T}k_w^2.
 \tag{0.5}
\]

One clean sufficient statement is

\[
 \boxed{H_N(T)\le C_{\rm loc}T^2\min(T,N).}
 \tag{LOC_0}
\]

`(LOC_0)` is **CONJECTURAL**.  With
\(\log_+u:=\max(\log u,0)\), the more flexible, Route-B-compatible sufficient
statement is

\[
 \boxed{H_N(T)\le C_{\rm loc}T^2\min(T,N)
 \bigl(1+\log_+(T/N)\bigr),\qquad T\ge1.}
 \tag{LOC}
\]

`(LOC)` is **CONJECTURAL**.  It does not follow from Ford counting.  If it
were proved, it would give, for \(p=2\sigma\in(2,3)\),

\[
 \sum_{w\in{\cal I}_N}k_w^2y_w^{-p}
 \le pC_{\rm loc}N^{3-p}
 \left({1\over3-p}+{1\over p-2}+{1\over(p-2)^2}\right),
 \tag{0.6}
\]

and the deformation factor \(N^{-2}\) would produce the desired
\(N^{1-p}=N^{1-2\sigma}\).  At \(p=3\), `(LOC)` gives the corrected bound

\[
 \sum_{w\in{\cal I}_N}k_w^2y_w^{-3}
 \le 3C_{\rm loc}\bigl(2+\log(N/2)\bigr).
 \tag{0.7}
\]

The numerical histograms at \(q=5,8,12\), \(X=50\), and search cap \(16\)
are consistent with `(LOC)`, but they are **NOT EVIDENCE OF COMPLETENESS**.
The enumerator's branch-pruning assertion is false: a branch can cross above
\(X\) and later re-enter below \(X\).  An explicit Arb-certified example is
given in Section 2.3.

Consequently the headline localization theorem remains **CONJECTURAL**.
The proved deliverables here are (0.1)--(0.2), the exact layer-cake reduction,
the sharp false-target/endpoint obstructions, and the strongest Ford-only
fallback with its honest \(N\)-power.

## 1. The precise hole inherited from `M2_NATIVE_PERTERM_SOL.md`

The read-first receipt was:

```bash
sed -n '1,12p' research_notes/rh_goals_2026-08-14/lane_g/M2_NATIVE_PERTERM_SOL.md
```

Output:

```text
# M2 native per-term majorant in the conjugated width-one model

**Date:** 2026-08-18
**Route:** native matrix/continuant argument; no use of Hejhal Ch. 6 §12
**Verdict:** **PER-TERM AND FINITE-WINDOW THEOREM PROVED. THE CLAIM THAT THE
RESULTING \(k^2\)-WEIGHTED MAJORANT CONVERGES ON ALL \(\Re s>1\) IS FALSE.**
Ford packing proves the corrected weighted-tail statement only for
\(\Re s>2\). The desired \(N^{1-2\sigma}\) full-series estimate still
requires a new \(N\)-dependent weighted-count/localization theorem; the
owned matched/escaping data do not prove it.
```

That file proves the per-term estimate

\[
 |x_w^{-2s}-y_w^{-2s}|
 \le {2\pi^2|s|\over N^2}D(w)\mu_w^{-2\sigma-1},
 \qquad
 \mu_w=\min(x_w,y_w),
 \tag{1.1}
\]

and the endpoint derivative estimate

\[
 |c'_w(2)|\le{k_w^2+2\over6}|c_w(2)|.
 \tag{1.2}
\]

It does **not** prove the interval replacement

\[
 D(w)\le A k_w^2y_w,
 \tag{1.3}
\]

nor a comparison \(y_w/\mu_w=O(1)\), nor a global matched-coset section in
the conventions used there.  A depth--height count for \(y_w\) alone cannot
silently replace a count for \(\mu_w\): near an elliptic wrap, \(y_w\) can be
of order \(N\) while \(x_w\), and hence \(\mu_w\), is of order one.

For an eventual application of (1.1), the honest weighted aggregate is

\[
 \widetilde H_N(T):=
 \sum_{w\in{\cal M}_N:\ \mu_w\le T}
 k_w^2{y_w\over\mu_w}.
 \tag{1.4}
\]

The direct RATE-use hypothesis is therefore

\[
 \boxed{
 \widetilde H_N(T)\le \widetilde C_{\rm loc}T^2\min(T,N)
 \bigl(1+\log_+(T/N)\bigr),\qquad T\ge1,}
 \tag{\mathrm{LOC}_\mu}
\]

together with the interval estimate (1.3).  Neither statement is proved
here.  `(LOC)` is the cleaner theta-height model; `(LOC_mu)` is what (1.1)
actually consumes.

### 1.1 Three inequivalent notions of depth

They must not be conflated.

1. **Raw \(Q,S\)-syntax depth.**  In
   
   \[
   Q S^{n_1}Q\cdots S^{n_{k-1}}Q,
   \qquad n_j\ne0,
   \]
   
   \(k\) is the number of \(Q\)'s.  This is the depth in the continuant and
   derivative formulas.
2. **Finite free-product depth.**  Put \(R=QS\).  In PSL,
   \(G_N=C_2*C_N=\langle Q,R:Q^2=R^N=1\rangle\).  Its normal form counts
   alternating \(Q\)- and \(R\)-syllables, not raw \(Q,S\)-depth.
3. **Minimal double-coset \(Q,S\)-depth.**  One may minimize raw \(Q\)-count
   over a fixed \(\langle S\rangle\)-double coset.  This is canonical by
   definition, but the current assets do not provide a global formula for it.

The Route-B balanced lift in `M1_ROUTE_B_FREEPRODUCT_SOL.md` gives a useful
paper-level section into theta canonical words.  If that section is used,
the relevant deformation depth is the raw \(Q\)-count of the selected theta
\(Q,S\)-lift, not the number of finite \(R\)-syllables.  A different choice
that minimizes raw depth over the entire theta double coset would require a
separate theorem identifying it with this selected depth.

## 2. Numerical joint distribution at \(q=5,8,12\), \(X=50\)

### 2.1 Method and exact scope

The supplied `law_probes/r1_coset_enum.py` was exercised through the same
bottom-row recurrence

\[
 (C,D)\mapsto\bigl(\lambda_N(D+nC),-C/\lambda_N\bigr).
 \tag{2.1}
\]

The literal BFS becomes prohibitively redundant at these depths.  A
stdout-only acceleration deduplicated frontier states by the normalized
bottom row \((C,D)\), not by the double-coset key \((C,D\bmod C)\).  This
deduplication is transition-safe inside the finite model: identical bottom
rows have identical descendants under every appended \(S^nQ\).  At depth
eight it reproduced the literal enumerator's keys and first witness words
exactly:

```text
q 5  raw 428 fast 428 missing_fast 0 extra_fast 0
witness_word_diffs 0 []
q 8  raw 330 fast 330 missing_fast 0 extra_fast 0
witness_word_diffs 0 []
q 12 raw 312 fast 312 missing_fast 0 extra_fast 0
witness_word_diffs 0 []
```

The cap-16 command used `PYTHONDONTWRITEBYTECODE=1`,
`/Users/za/.venvs/farey-rh/bin/python`, `mp.dps=50`, the source
`m_max=max(4,int(50/lambda_N)+4)`, the source zero threshold, the source
18-digit double-coset key, and a 35-digit left-state key.  The operative
command was:

```bash
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=research_notes/rh_goals_2026-08-14/lane_g \
/Users/za/.venvs/farey-rh/bin/python - <<'PY'
from mpmath import mp,mpf
import law_probes.r1_coset_enum as r1,time
mp.dps=50

def E(q,X=50,maxd=16):
    L=r1.lam_of_q(q); X=mpf(X)
    mm=max(4,int(X/float(L))+4)
    eps=mpf(10)**(-int(mp.dps*.4)); found={}; seen=set()
    def state(C,D):
        if C<0: C,D=-C,-D
        return mp.nstr(C,35),mp.nstr(D,35)
    def coset_key(C,D):
        if C<0: C,D=-C,-D
        b=int(mp.floor(D/C)); d=D-b*C
        if d<0: d+=C
        if d>=C: d-=C
        z=C*mpf(10)**(-int(mp.dps*.5))
        if d<z or C-d<z: d=mpf(0)
        return mp.nstr(C,18),mp.nstr(d,18)
    def record(w,C,D,k):
        a=abs(C)
        if a<eps or a>X: return
        z=coset_key(C,D)
        if z not in found: found[z]=(a,w,k)
    def digit_range(C,D):
        if abs(C)<eps: return range(-mm,mm+1)
        lo=(-X/L-D)/C; hi=(X/L-D)/C
        if lo>hi: lo,hi=hi,lo
        return range(max(-mm,int(mp.floor(lo))-1),
                     min(mm,int(mp.ceil(hi))+1)+1)
    C,D=L,mpf(0); record((),C,D,1)
    frontier=[((),C,D)]; seen.add(state(C,D)); reached=1
    while frontier and reached<maxd:
        reached+=1; nxt=[]
        for w,C,D in frontier:
            for n in digit_range(C,D):
                if not n: continue
                c=L*(D+n*C); d=-C/L
                if abs(c)>X: continue
                z=state(c,d)
                if z in seen: continue
                seen.add(z); nw=w+(n,)
                record(nw,c,d,reached); nxt.append((nw,c,d))
        frontier=nxt
    return found,reached

for q in (5,8,12):
    t=time.time(); F,reached=E(q)
    rows=[(v[2],float(v[0]),v[1]) for v in F.values()]
    ks=range(1,max(k for k,c,w in rows)+1)
    print(f'q={q} reached={reached} total={len(rows)} '
          f'elapsed={time.time()-t:.6f}')
    print('counts',' '.join(f'{k}:{sum(a==k for a,c,w in rows)}'
                            for k in ks))
    print('tail',' '.join(f'{k}:{sum(a>=k for a,c,w in rows)}'
                          for k in ks))
    print('minheight',' '.join(f'k{k}={min(c for a,c,w in rows if a==k):.12g}'
                               for k in ks))
PY
```

The run completed in `real 0.43`, `user 0.33`, `sys 0.02` seconds.  Its
output was as follows (the long `minheight` lines are wrapped for display):

```text
q=5 reached=10 total=428 elapsed=0.163848
counts 1:1 2:38 3:126 4:169 5:84 6:10
tail   1:428 2:427 3:389 4:263 5:94 6:10
minheight k1=1.61803398875 k2=2.61803398875 k3=5.85410196625
          k4=8.47213595500 k5=20.5623058987 k6=41.7426457862

q=8 reached=13 total=330 elapsed=0.080379
counts 1:1 2:28 3:72 4:95 5:80 6:42 7:10 8:2
tail   1:330 2:329 3:301 4:229 5:134 6:54 7:12 8:2
minheight k1=1.84775906502 k2=3.41421356237 k3=4.46088499478
          k4=4.82842712475 k5=13.3826549843 k6=19.8994949366
          k7=23.3868171742 k8=46.6274169980

q=12 reached=16 total=318 elapsed=0.061825
counts 1:1 2:26 3:60 4:72 5:58 6:47 7:30 8:18 9:6
tail   1:318 2:317 3:291 4:231 5:159 6:101 7:54 8:24 9:6
minheight k1=1.93185165258 k2=3.73205080757 k3=5.27791686753
          k4=6.46410161514 k5=7.20976852011 k6=7.46410161514
          k7=21.6293055603 k8=34.3205080757 k9=44.6728246830
```

Here `reached` is exhaustion in the accelerated **pruned** state graph: the
new frontier was empty at depths \(10,13,16\), respectively.  It is not a
proof of exhaustion of the unpruned all-word graph.

The deepest first-emitted witnesses included

```text
q=5, k=6, c=41.742645786248:
  (-1,-2,-1,1,-1), (-1,1,-1,-2,-1),
  (1,-2,-1,-2,-1), (-1,-2,-1,-2,1)

q=8, k=8, c=46.6274169979695:
  (-1,-1,-1,1,-1,-1,-1),
  (-1,-1,-1,-3,-1,-1,-1)

q=12, k=9, c=44.6728246830181:
  (-1,-1,-1,-1,-1,-2,-1,-1),
  (1,1,1,-1,-1,-1,-1,-1),
  (-1,-1,-2,-1,-1,-1,-1,-1),
  (-1,-1,-1,-1,-1,1,1,1).
```

Thus the finite model shows a conspicuous rise in the smallest height of new
deep cosets.  It does **not** show geometric growth, and it is not a
certificate.

### 2.2 Finite diagnostic against the candidate aggregate

From the emitted histograms define

\[
 H^{\rm emit}_N(50)=\sum k^2\#\{\hbox{emitted keys at depth }k\}.
\]

Receipt:

```bash
/Users/za/miniforge3/envs/pari-arb/bin/python3 - <<'PY'
from fractions import Fraction
hist={
 5:{1:1,2:38,3:126,4:169,5:84,6:10},
 8:{1:1,2:28,3:72,4:95,5:80,6:42,7:10,8:2},
 12:{1:1,2:26,3:60,4:72,5:58,6:47,7:30,8:18,9:6}}
for N,h in hist.items():
 H=sum(k*k*v for k,v in h.items())
 B={K:sum(v for k,v in h.items() if k>=K) for K in range(1,max(h)+1)}
 print(f'N={N} H50={H} H/(50^2*N)={float(Fraction(H,2500*N)):.6f} '
       f'max_KB/X2={max(K*b for K,b in B.items())/2500:.6f}')
PY
```

Output:

```text
N=5 H50=6451 H/(50^2*N)=0.516080 max_KB/X2=0.466800
N=8 H50=6411 H/(50^2*N)=0.320550 max_KB/X2=0.366400
N=12 H50=8047 H/(50^2*N)=0.268233 max_KB/X2=0.369600
```

The ratios are compatible with \(H_N(50)\ll50^2N\) and
\(B_N(50,K)\ll50^2/K\).  This is only a falsification test: the sample is
one cutoff, three small \(N\)'s, floating, digit-bounded, and pruned.

### 2.3 The enumerator pruning claim is false

The source prunes a branch whenever its current \(|c|\) exceeds \(X\).  That
would be safe only if future heights could not decrease back through \(X\).
They can.

Fresh Arb receipt:

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import arb, ctx
ctx.prec=160
N=5; lam=2*(arb.pi()/N).cos(); km2=arb(0); km1=arb(1)
print('q=5 X=50 word=(-2,4,1,1)')
print(f'depth=1 |c|={abs(lam*km1)}')
for depth,n in enumerate((-2,4,1,1),2):
    km2,km1=km1,lam*n*km1-km2
    print(f'depth={depth} n={n:+d} |c|={abs(lam*km1)} '
          f'keep={abs(lam*km1).upper() <= 50}')
PY
```

Output:

```text
q=5 X=50 word=(-2,4,1,1)
depth=1 |c|=[1.6180339887498948482045868343656381177203091798 +/- 6.14e-48]
depth=2 n=-2 |c|=[5.2360679774997896964091736687312762354406183596 +/- 1.72e-47] keep=True
depth=3 n=+4 |c|=[35.506577808748212419477976184215848001245256057 +/- 6.08e-46] keep=True
depth=4 n=+1 |c|=[52.214781741247581508705497190409676707567111135 +/- 7.15e-46] keep=False
depth=5 n=+1 |c|=[48.97871376374779181229632352167840047212649278 +/- 5.52e-45] keep=True
```

This proves that the branch predicate is non-monotone.  The final
double-coset key happens to have a shorter retained witness in this small
run, so the receipt does **not** prove that the final key is absent.  It
proves the logically necessary negative statement: the pruning rule is not
a completeness theorem.

There is a second independent limitation.  At \(q=5\), the source heuristic
has `m_max=34`.  The following 80-digit replay used the same recurrence:

```bash
PYTHONDONTWRITEBYTECODE=1 \
/Users/za/miniforge3/envs/pari-arb/bin/python3 - <<'PY'
from mpmath import mp
mp.dps=80; q=5; X=mp.mpf(50)
lam=2*mp.cos(mp.pi/q); word=(-100,-1,-1,-1,-1)
a,b=mp.mpf(0),mp.mpf(1); heights=[abs(lam*b)]
for n in word:
    a,b=b,lam*n*b-a; heights.append(abs(lam*b))
print('q=5 m_max=',max(4,int(X/float(lam))+4),'word=',word)
print('prefix_abs_c=',','.join(mp.nstr(x,31) for x in heights))
PY
```

Output:

```text
q=5 m_max= 34 word= (-100, -1, -1, -1, -1)
prefix_abs_c= 1.618033988749894848204586834366,261.8033988749894848204586834366,421.9887637612290747927127800388,420.9887637612290747927127800388,259.1853648862395899722540966022,1.618033988749894848204586834366
```

Thus a digit outside `m_max` can also return to the low window through the
elliptic relation.  Again its final key has a short representative; the point
is that `m_max` is not a proof of domain completeness.

The reported depths are therefore exactly:

> first-emitted/minimal within the finite floating, `m_max`-bounded,
> height-pruned BFS (and its depth-eight-validated left-state quotient).

They are **not** proved minimal double-coset depths.  Floating
canonicalization (`EPS_ZERO`, `floor(D/C)`, boundary snap, and 18-digit keys)
adds a further near-relation limitation.

## 3. Proved sharp finite no-wrap depth--height theorem

Let

\[
 w=Q_{\lambda_N}S^{n_1}Q_{\lambda_N}\cdots
 S^{n_{k-1}}Q_{\lambda_N},\qquad n_j\in\mathbb Z\setminus\{0\}.
\]

Put

\[
 K_{-1}=0,\qquad K_0=1,\qquad
 K_j=\lambda_Nn_jK_{j-1}-K_{j-2}.
 \tag{3.1}
\]

Then \(c_w(\lambda_N)=\lambda_NK_{k-1}\).

### Theorem 3.1 (optimal sine envelope) -- PROVED

For every \(N\ge3\), every such word, and \(1\le k\le N-1\),

\[
 \boxed{
 |c_w(\lambda_N)|\ge
 f_N(k):=\lambda_N{\sin(k\pi/N)\over\sin(\pi/N)}.}
 \tag{3.2}
\]

The lower envelope is attained by \(n_j=1\) for every \(j\), and by
\(n_j=-1\) for every \(j\).

#### Proof

Write \(\theta=\pi/N\) and

\[
 u_j={\sin((j+1)\theta)\over\sin\theta},\qquad
 p_j={u_j\over u_{j-1}}.
\]

For \(1\le j\le N-2\), \(u_j,p_j>0\), \(p_1=\lambda_N\), and, for
\(2\le j\le N-2\), the Chebyshev recurrence gives

\[
 p_j=\lambda_N-{1\over p_{j-1}}.
 \tag{3.3}
\]

Whenever \(K_{j-1}\ne0\), put \(r_j=K_j/K_{j-1}\).  The induction below in
fact proves \(K_{j-1}\ne0\), and

\[
 r_j=\lambda_Nn_j-{1\over r_{j-1}}.
 \tag{3.4}
\]

The base case is

\[
 |r_1|=\lambda_N|n_1|\ge\lambda_N=p_1.
\]

Assume \(|r_{j-1}|\ge p_{j-1}\).  If the two terms on the right side of
(3.4) reinforce, then \(|r_j|\ge\lambda_N\ge p_j\).  If they subtract, then

\[
 |r_j|\ge\lambda_N-{1\over|r_{j-1}|}
 \ge\lambda_N-{1\over p_{j-1}}=p_j.
\]

Therefore

\[
 |K_{k-1}|=\prod_{j=1}^{k-1}|r_j|
 \ge\prod_{j=1}^{k-1}p_j=u_{k-1},
\]

which proves (3.2).  The constant-sign unit-digit words satisfy the same
recurrence as \(u_j\), so equality holds.  \(\square\)

### Corollary 3.2 (linear pre-wrap law) -- PROVED

For \(1\le k\le N/2\), concavity of sine on \([0,\pi/2]\) and
\(\sin\theta\le\theta\) give

\[
 f_N(k)\ge {2\lambda_N\over\pi}k.
\]

Since \(2-\lambda_N\le\pi^2/N^2\),

\[
 \boxed{
 |c_w(\lambda_N)|\ge
 \left({4\over\pi}-{2\pi\over N^2}\right)k.}
 \tag{3.5}
\]

Also \(\lambda_N\ge1\) for \(N\ge3\), so the simple uniform form

\[
 |c_w(\lambda_N)|\ge{2\over\pi}k>0.6366\,k
 \tag{3.6}
\]

is valid throughout the pre-wrap half-window.

Using
\(\sin x\ge x-x^3/6\), \(\cos\theta\ge1-\theta^2/2\), and
\(\sin\theta\le\theta\) gives the additive degradation

\[
 \boxed{
 |c_w(\lambda_N)|\ge
 2k-\left({k^3\over3}+k\right){\pi^2\over N^2},
 \qquad k\le N/2.}
 \tag{3.7}
\]

The sine-linear bound (3.5), rather than (3.7), should be used when the
right side of (3.7) becomes weak near \(N/2\).

### 3.1 Arb falsification check

The following exhaustive finite check used digits
\(\{-2,-1,1,2\}\).  It is not the proof; it checks the sharp witnesses and
the turn-over numerically.

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import arb,ctx
from itertools import product
ctx.prec=160
for N in (5,8,12):
 th=arb.pi()/N; lam=2*th.cos()
 print('N',N)
 for k in range(1,min(N-1,8)+1):
  env=lam*(arb(k)*th).sin()/th.sin(); best=None; witness=None
  for ns in product((-2,-1,1,2),repeat=k-1):
   a,b=arb(0),arb(1)
   for n in ns: a,b=b,lam*n*b-a
   c=abs(lam*b)
   if best is None or c.upper()<best.upper(): best,witness=c,ns
  print(k,best,env,witness)
PY
```

Selected center digits (abridged; the command prints the full Arb balls):

```text
N 5
1 1.61803398874989... 1.61803398874989... ()
2 2.61803398874989... 2.61803398874989... (-1,)
3 2.61803398874989... 2.61803398874989... (-1,-1)
4 1.61803398874989... 1.61803398874989... (-1,-1,-1)

N 8
4 4.82842712474619... 4.82842712474619... (-1,-1,-1)
5 4.46088499477533... 4.46088499477533... (-1,-1,-1,-1)
7 1.84775906502257... 1.84775906502257... (-1,-1,-1,-1,-1,-1)

N 12
6 7.46410161513775... 7.46410161513775... (-1,-1,-1,-1,-1)
7 7.20976852010750... 7.20976852010750... (-1,-1,-1,-1,-1,-1)
8 6.46410161513775... 6.46410161513775... (-1,-1,-1,-1,-1,-1,-1)
```

### 3.2 Global geometric growth is false

For

\[
 w_k=(Q_{\lambda_N}S)^{k-1}Q_{\lambda_N}
\]

one has exactly

\[
 c_{w_k}(\lambda_N)
 =\lambda_N{\sin(k\pi/N)\over\sin(\pi/N)}.
 \tag{3.8}
\]

If \(R_N=Q_{\lambda_N}S\), then \(R_N^N=-I\) in SL and \(R_N^N=1\)
in PSL.  Hence

\[
 w_{k+mN}=(-1)^mw_k,\qquad c_{w_N}(\lambda_N)=0.
 \tag{3.9}
\]

In particular, the syntactically reduced words \(w_{mN+1}\) have
arbitrarily large raw depth but represent the same PSL class as \(Q\), with
\(|c|=\lambda_N\).  This is the promised negation of every globally growing
raw-depth lower bound.

It is not a counterexample in finite free-product syllable depth:
\(w_k=R_N^{k-1}Q\), and right multiplication by \(S\) gives \(R_N^k\), a
single \(R\)-syllable after reducing \(k\bmod N\), except when the residue is
zero and the word is the identity.  The relation therefore shows why raw and
canonical depths cannot be identified.

At the theta endpoint the relation disappears and (3.8) becomes

\[
 \boxed{c_{w_k}(2)=2k.}
 \tag{3.10}
\]

Thus even the canonical theta depth has linear, not geometric, extremal
growth.  Fibonacci-type growth is the wrong continuant intuition here: this
is the negative continuant at its parabolic digit \(2\), whose all-unit
solution is linear.

For fixed \(k\), (3.8) also gives

\[
 c_{w_k}(\lambda_N)
 =2k-{k^3+2k\over3}(2-\lambda_N)
 +O_k\bigl((2-\lambda_N)^2\bigr),
 \tag{3.11}
\]

matching \(c'_{w_k}(2)=(k^3+2k)/3\).

## 4. Exact weighted-count reduction

Put \(p=2\sigma\).  First work at theta, where every canonical reduced word
satisfies \(k_w\le |c_w|/2\).  Define

\[
 B(X,K):=\#\{w:0<|c_w|\le X,\ k_w\ge K\},
 \tag{4.1}
\]

and

\[
 W_2(X):=\sum_{0<|c_w|\le X}k_w^2.
 \tag{4.2}
\]

The integer identity

\[
 k^2=\sum_{K=1}^k(2K-1)
\]

gives the exact layer-cake formula

\[
 \boxed{
 W_2(X)=\sum_{K=1}^{\lfloor X/2\rfloor}(2K-1)B(X,K).}
 \tag{4.3}
\]

Stieltjes summation then gives

\[
\begin{aligned}
 S_p(X)&:=\sum_{0<|c_w|\le X}k_w^2|c_w|^{-p}\\
 &=X^{-p}W_2(X)+p\int_2^XW_2(t)t^{-p-1}\,dt\\
 &=\sum_{K\le X/2}(2K-1)
 \left[X^{-p}B(X,K)+p\int_{2K}^XB(t,K)t^{-p-1}\,dt\right].
\end{aligned}
 \tag{4.4}
\]

Equations (4.3)--(4.4) identify the precise joint-distribution object.  Ford
controls only \(B(X,1)\le X^2\).

### Theorem 4.1 (conditional scale-sharp joint count)

Assume

\[
 B(X,K)\le C_B{X^2\over K}
 \qquad(1\le K\le X/2).
 \tag{4.5}
\]

Then

\[
 W_2(X)\le C_BX^2
 \sum_{K\le X/2}{2K-1\over K}
 \le C_BX^3.
 \tag{4.6}
\]

Consequently, for \(2<p<3\),

\[
 \boxed{
 S_p(X)\le{C_B\over3-p}
 \left(3X^{3-p}-p\,2^{3-p}\right)
 \le {3C_B\over3-p}X^{3-p}.}
 \tag{4.7}
\]

At \(p=3\),

\[
 \boxed{S_3(X)\le C_B\bigl(1+3\log(X/2)\bigr).}
 \tag{4.8}
\]

For \(p>3\), the same hypothesis gives the global tail

\[
 \sum_{|c_w|>X}k_w^2|c_w|^{-p}
 \le {pC_B\over p-3}X^{3-p}.
 \tag{4.9}
\]

The hypothesis (4.5) is **CONJECTURAL**.  The implications
(4.6)--(4.9) are proved.

### 4.1 The \(1/K\) scale is forced

The theta Chebyshev cosets are distinct, and their selected raw words have
\((k,c)=(k,2k)\).  For this family, depth \(k\) is in fact minimal even if
one minimizes over all raw representatives of the theta double coset.  To
see this, the case \(k=1\) is immediate.  For \(k\ge2\), a representative
of the same coset cannot have depth one because its height is \(2k>2\).
Let a
depth-\(h\) representative have theta continuants
\((K_{h-1},K_{h-2})\).  Its bottom row is
\((2K_{h-1},-K_{h-2})\).  Equality of its normalized double-coset key with
that of \(R^k\) gives

\[
 K_{h-1}=k,\qquad -K_{h-2}\equiv k+1\pmod{2k}.
\]

The theta version of the ratio induction in Theorem 3.1 gives

\[
 |K_{h-2}|\le {h-1\over h}|K_{h-1}|<k,
\]

so the congruence forces \(K_{h-2}=k-1\).  Reversing
\(K_j=2n_jK_{j-1}-K_{j-2}\) and writing \(A_j=|K_j|\) gives

\[
 A_{j-2}\ge2A_{j-1}-A_j.
\]

Starting from \(A_{h-1}=k\), \(A_{h-2}=k-1\), induction yields
\(A_{h-1-r}\ge k-r\).  Since \(A_0=1\), necessarily \(h\ge k\), while the
all-unit word has depth \(k\).  Thus the minimum is exactly \(k\).

It follows that taking \(X=4m\) and \(K=m\) gives

\[
 B(4m,m)\ge m+1.
 \tag{4.10}
\]

Therefore no bound \(B(X,K)\le CX^2/K^{1+\delta}\), \(\delta>0\), can hold
uniformly.  Moreover,

\[
 W_2(X)\ge\sum_{k\le X/2}k^2\sim{X^3\over24}.
 \tag{4.11}
\]

Thus \(W_2(X)=O(X^3)\) is not merely sufficient; its exponent is optimal.
For \(2<p<3\),

\[
 S_p(X)\ge2^{-p}\sum_{k\le X/2}k^{2-p}
 \sim {X^{3-p}\over8(3-p)},
 \tag{4.12}
\]

and at the endpoint

\[
 S_3(X)\ge {1\over8}\sum_{k\le X/2}{1\over k}
 ={1\over8}\log X+O(1).
 \tag{4.13}
\]

This proves the logarithmic endpoint obstruction for the selected-word
\(k^2\)-majorant used by the deformation estimate.  It does not prove the
same lower bound for a different depth obtained by minimizing over all raw
representatives of each theta double coset.

## 5. An explicit sufficient \(N\)-dependent localization profile

A bound only for \(X\lesssim N\) does not make the full image series
converge.  The following two-regime profile is sufficient and allows the
relative-scale logarithm used by the Route-B repair:

\[
 H_N(T)\le C_{\rm loc}
 \begin{cases}
 T^3,&1\le T\le N,\\
 NT^2\bigl(1+\log(T/N)\bigr),&T\ge N.
 \end{cases}
 \tag{5.1}
\]

The first regime is forced by the Chebyshev family.  More concretely, the
Route-B balanced image contains the singleton words \(R^k\) for
\(2\le k\le\lfloor N/2\rfloor\); the selected boundary representative
\(R^{k-1}Q\) has \((k_w,y_w)=(k,2k)\).  Thus already
\(H_N(N)\gg\sum_{k\le N/2}k^2\asymp N^3\).  The second regime says that
after the elliptic scale \(N\), the mean squared selected depth no longer
grows like the height itself.  This is the precise one-power localization
missing from Ford.

A pointwise depth-tail statement sufficient for (5.1) is the following.
Define

\[
 B_N(T,K):=\#\{w\in{\cal I}_N:y_w\le T,\ k_w\ge K\}.
\]

Put \(L=\min(T,N)\), \(R=1+\log_+(T/N)\), and assume

\[
 \boxed{
 B_N(T,K)\le C_*{T^2R\over K}
 \min\left\{1,\left({L\over K}\right)^2\right\}.}
 \tag{5.2}
\]

Indeed, (4.3), split at \(K=L\), gives

\[
\begin{aligned}
 H_N(T)
 &\le 2C_*T^2R\sum_{K\le L}1
   +2C_*T^2RL^2\sum_{K>L}{1\over K^2}\\
 &\le4C_*T^2LR.
\end{aligned}
 \tag{5.3}
\]

Neither (5.1) nor (5.2) is proved by the finite histograms.

### Theorem 5.1 (`(LOC)` implies the RATE weighted scale) -- CONDITIONAL

Assume `(LOC)` for the canonical matched image.  For \(2<p<3\), Stieltjes
summation to infinity gives

\[
\begin{aligned}
 \sum_{w\in{\cal I}_N}k_w^2y_w^{-p}
 &=p\int_2^\infty H_N(t)t^{-p-1}\,dt\\
 &\le pC_{\rm loc}
 \left(\int_2^Nt^{2-p}\,dt
 +N\int_N^\infty t^{1-p}
       \bigl(1+\log(t/N)\bigr)\,dt\right)\\
 &\le pC_{\rm loc}N^{3-p}
 \left({1\over3-p}+{1\over p-2}+{1\over(p-2)^2}\right).
\end{aligned}
 \tag{5.4}
\]

At \(p=3\),

\[
 \sum_{w\in{\cal I}_N}k_w^2y_w^{-3}
 \le3C_{\rm loc}\bigl(\log(N/2)+2\bigr).
 \tag{5.5}
\]

If, in addition, the interval estimate \(D(w)\le A k_w^2y_w\) and the
weighted \(\mu\)-profile `(LOC_mu)` hold, then (1.1) gives, for
\(2<p<3\),

\[
 \sum_{w\in{\cal M}_N}|x_w^{-2s}-y_w^{-2s}|
 \le
 2\pi^2A|s|\,p\widetilde C_{\rm loc}
 \left({1\over3-p}+{1\over p-2}+{1\over(p-2)^2}\right)N^{1-p}.
 \tag{5.6}
\]

Here the Stieltjes integral for `(LOC_mu)` starts at \(1\), because Shimizu
only supplies \(\mu_w\ge1\).  Integrating from \(1\), rather than \(2\),
still gives the displayed upper bound after the negative lower-end term is
dropped.  The theta-height profile `(LOC)` starts at \(y_w\ge2\).

The scattering factor \(|m(s)|\) must be multiplied into (5.6).  Uniformity
requires a compact \(s\)-set and an explicit bound on \(|s\,m(s)|\).

At \(p=3\), the same argument gives only

\[
 O\bigl(N^{-2}\log N\bigr).
 \tag{5.7}
\]

The constant in (5.6) also blows up like \(1/(3-p)\) as
\(p\uparrow3\).  Hence there is no uniform constant on a compact set touching
\(\sigma=3/2\) from this positive majorant.

## 6. What Ford alone proves, with the \(N\)-power exposed

Ford gives

\[
 A(X):=\#\{w:0<|c_w|\le X\}\le X^2.
 \tag{6.1}
\]

At theta, \(k_w\le|c_w|/2\).  Therefore, for \(2<p<4\),

\[
\begin{aligned}
 \sum_{0<|c_w|\le X}k_w^2|c_w|^{-p}
 &\le{1\over4}\sum_{0<|c_w|\le X}|c_w|^{2-p}\\
 &\le {1\over2(4-p)}X^{4-p}.
\end{aligned}
 \tag{6.2}
\]

This is exactly

\[
 {1\over4(2-\sigma)}X^{4-2\sigma}.
 \tag{6.3}
\]

At the natural cutoff \(X\asymp N\), multiplying by the deformation factor
\(N^{-2}\) gives

\[
 \boxed{N^{2-p}=N^{2-2\sigma},}
 \tag{6.4}
\]

one full power worse than \(N^{1-p}\).  This loss is logical, not an
integration mistake: Ford controls only \(B(X,1)\), while the target requires
the aggregate (4.3) to be \(O(X^3)\), not its Ford-only worst case \(O(X^4)\).

For the unweighted strict tail, Ford gives

\[
 \sum_{|c|>X}|c|^{-p}\le{p\over p-2}X^{2-p}.
 \tag{6.5}
\]

Thus mere support of an escaping population above \(c\asymp N\) gives only
\(N^{2-p}\), again one power too weak.  The one-sided first-wrap height bound
in `M1_ROUTE_B_FREEPRODUCT_SOL.md` is valuable structural information, but
support plus Ford does not prove the required escaping mass
\(O(N^{1-p})\).  That is a separate localization obligation.

One may force the Ford tail itself to the target by taking

\[
 X\asymp N^{(p-1)/(p-2)},
 \tag{6.6}
\]

but then the matched head is far beyond the natural \(N\)-scale.  This is a
true tail theorem, not the desired local \(X\asymp N\) mechanism.

## 7. False targets and corrected versions

| Proposed target | Verdict | Corrected statement |
|---|---|---|
| \(|c_w|\gtrsim\rho^k\), \(\rho>1\), for all reduced words | **FALSE** | At theta, \(c_{w_k}=2k\).  At finite \(N\), the optimal raw pre-wrap envelope is (3.2), and the elliptic relation destroys global raw-depth growth. |
| Continuants give Fibonacci growth at \(\lambda=2\) | **FALSE** | The relevant negative continuant has parabolic coefficient \(2\); the extremal all-unit solution is \(K_j=j+1\). |
| The supplied BFS height prune is complete | **FALSE** | Section 2.3 gives a certified \(52.21\to48.98\) re-entry.  Histograms are finite diagnostics only. |
| Ford plus \(k\le c/2\) gives \(X^{3-p}\) | **FALSE** | The proved Ford-only bound is \(X^{4-p}/[2(4-p)]\). |
| \(\sum k^2c^{-p}\) converges for every \(p>2\) | **FALSE** | Theta Chebyshev forces divergence for \(p\le3\).  A global tail follows from (4.5) only for \(p>3\). |
| \(O(N^{1-p})\) by absolute \(k^2\)-summation through \(p=3\) | **FALSE** | For \(2<p<3\), `(LOC_mu)` would give \(O(N^{1-p})\).  At \(p=3\), the sharp absolute scale is \(O(N^{-2}\log N)\). |
| \(B(T,K)\ll T^2/K^{1+\delta}\) | **FALSE** for every \(\delta>0\) | The scale-sharp theta candidate is \(T^2/K\); finite-\(N\) summability additionally needs the post-\(N\) suppression and permitted relative-scale logarithm in (5.2). |
| First-wrap support \(c\ge\kappa N\) plus Ford proves RATE escaping mass | **FALSE** | It gives \(O(N^{2-p})\).  A direct exceptional-mass localization theorem of order \(N^{1-p}\) is still required. |

## 8. Final disposition

### PROVED

1. The optimal no-wrap lower envelope (3.2) for every raw reduced word of
   depth \(k\le N-1\).
2. The explicit linear half-window laws (3.5)--(3.7), including honest
   \(2-\lambda_N\) degradation.
3. The global negation furnished by the elliptic relation and the linear
   theta extremal law.
4. The exact joint-count/layer-cake identities (4.3)--(4.4).
5. The conditional implications (4.6)--(4.9) and (5.4)--(5.7).
6. The optimality of the \(X^3\) aggregate exponent and the endpoint
   logarithm from the Chebyshev family.
7. The Ford-only bound (6.2) and its one-power \(N\)-loss.
8. The enumerator's height-pruning completeness claim is false.

### FINITE DIAGNOSTIC ONLY

The cap-16, \(X=50\) histograms for \(q=5,8,12\) are compatible with
\(H_N(50)\ll50^2N\) and \(B_N(50,K)\ll50^2/K\).  They are not certified
complete and do not promote `(LOC)`.

### CONJECTURAL / OPEN

1. The canonical two-regime depth localization `(LOC)`, or the pointwise
   sufficient condition (5.2).  The stronger log-free `(LOC_0)` would also
   suffice but is not required.
2. The actual per-term aggregate `(LOC_mu)`, which must retain
   \(y_w/\mu_w\).
3. The interval derivative estimate (1.3).
4. Escaping/first-wrap mass \(O(N^{1-p})\), not merely support at height
   \(\asymp N\).
5. The full RATE estimate \(C_{\cal K}N^{1-2\sigma}\) for
   \(1<\sigma<3/2\).
6. At \(\sigma=3/2\), any removal of the unavoidable logarithm by a mechanism
   other than positive termwise majorization.

The strongest honest conclusion is therefore negative but useful: the
candidate geometric theorem is false, the exact pre-wrap law is now proved,
and the missing global theorem has been reduced to the interval estimate
(1.3), the explicit two-regime joint count `(LOC_mu)`, and a separate
first-wrap mass bound.  Any proof that does not establish those
\(N\)-dependent statements still loses one power under Ford counting alone.

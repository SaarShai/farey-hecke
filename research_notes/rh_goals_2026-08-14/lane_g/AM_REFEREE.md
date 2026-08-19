# Adversarial referee report: atom-moment bridge

**Date:** 2026-08-19

**Target:** `ATOM_MOMENT_BRIDGE_SOL.md`

**Verdict:** **CONFIRMED — paper-level, conditional on the already accepted Route-B/Ford inputs; not machine-verified.**

I found no convention mismatch, coding collision, omitted divergent sum,
forbidden inference from the displayed \((DH_{2,4})\) theorem, theta-cutoff
substitution, or numerical counterexample.  The direct marked-object argument
proves

\[
 \sum_{X\in\mathcal C_q:x_X\le Y}(1+A_X^2)
 <2^{63}Y^2\Phi_q(Y),
\]

with the target's two regimes for \(\Phi_q\).  Since \(2^{63}<2^{100}\), it
supplies exactly the missing paper-level input to RATE-A without changing the
declared RATE-A constant.

## 0. Audited source state

Fresh command:

```bash
shasum -a 256 research_notes/rh_goals_2026-08-14/lane_g/{ATOM_MOMENT_BRIDGE_SOL,RATE_A_REFEREE,BOUNDARY_ALPHA_THEOREM_SOL,TWOMARK_RENEWAL_SOL,TWOMARK_REFEREE,M2_FORD_PACKING_REFEREE}.md
```

Fresh output:

```text
59ce32f7c6fa86580055d9049e609a2189ecc1645528dd4136758fcf547fbbbb  research_notes/rh_goals_2026-08-14/lane_g/ATOM_MOMENT_BRIDGE_SOL.md
b835804104f502f54cc757336ba8fe54a82a05eaa18261a4d78f697aba358590  research_notes/rh_goals_2026-08-14/lane_g/RATE_A_REFEREE.md
021e87e55cad86a1bfc78c74b450857b3285492af00bf728f310bee6f711fd36  research_notes/rh_goals_2026-08-14/lane_g/BOUNDARY_ALPHA_THEOREM_SOL.md
7a553a9c3ed289b513ad8dd7e3a118b0c0d50f92080a1f89a6749fbce44a692b  research_notes/rh_goals_2026-08-14/lane_g/TWOMARK_RENEWAL_SOL.md
07ae98864b6963b14a279cfc463c9d047d0c5e75bc4f8fac876781f34bd28263  research_notes/rh_goals_2026-08-14/lane_g/TWOMARK_REFEREE.md
ebb38cf55ea4e4132df7e0f3f68901c196b8c623b1b4f4b24b5b11b2a2318345  research_notes/rh_goals_2026-08-14/lane_g/M2_FORD_PACKING_REFEREE.md
```

Paths below are relative to
`research_notes/rh_goals_2026-08-14/lane_g/` unless stated otherwise.

## 1. Attack (a): the definition of \(A_X\)

**Result: CONFIRMED.**

The target defines the cost from the **full canonical exponent sequence**:
each heavy digit contributes its magnitude and each maximal constant-sign unit
run contributes one (`ATOM_MOMENT_BRIDGE_SOL.md:80-117`).  Thus

\[
 A_X=\sum_{|a_j|\ge2}|a_j|+\ell(W_X),\qquad w_X=1+A_X^2.
\]

This is verbatim the mathematical convention in
`TWOMARK_RENEWAL_SOL.md:333-344`.  More importantly, it is exactly the quantity
actually consumed by the boundary proof: `BOUNDARY_ALPHA_THEOREM_SOL.md:315-331`
defines

\[
 A(W)=\sum_{|a_i|\ge2}|a_i|+\ell(W),\qquad w(W)=1+A(W)^2,
\]

and `BOUNDARY_ALPHA_THEOREM_SOL.md:371-395` uses that same \(A(W)^2\) in the
derivative bound.  Its required counting function is then explicitly
\(\sum_{x_W\le Y}w(W)\) at `BOUNDARY_ALPHA_THEOREM_SOL.md:403-419`.

There is no silent \(A\) versus \(A^2\) error: \(A\) is the atom cost, the
weight is \(1+A^2\), and the marked expansion is of \(A^2\).  There is also no
\(x\) versus \(m\) error.  On the matched balanced image,
`DH2_RENEWAL_PROOF_SOL.md:334-349` proves \(x_X\le y_X\), hence \(m_X=x_X\),
and the target keeps the cutoff \(x_X\le Y\).

The class-to-word bridge is legitimate.  The canonical finite double-coset
representative is unique by `M1_ROUTE_B_FREEPRODUCT_SOL.md:275-340`; the
balanced lift is an injective section with exactly the balanced canonical image
by `M1_ROUTE_B_FREEPRODUCT_SOL.md:444-495`.  Therefore defining
\(A_X:=A(W_X)\) does not change multiplicity or identify different \(X\)'s.

The notational warning at `ATOM_MOMENT_BRIDGE_SOL.md:119` is accurate:
`RATE_A_REFEREE.md:119-129` writes \(A(X)\), whereas the source proof writes
\(A(W)\).  Equation (1.2) supplies the missing notation, not a new statistic.

## 2. Attack (b): marked coding, injectivity, and every constant

### 2.1 Lemma 4.1 is used inside its hypotheses

**Result: CONFIRMED.**

The input population is balanced and canonical
(`ATOM_MOMENT_BRIDGE_SOL.md:80-117`).  Its matrix factorization and finite
height are the ones proved at `DH2_RENEWAL_PROOF_SOL.md:289-339` and restated at
`TWOMARK_RENEWAL_SOL.md:287-299`.  In the balanced alphabet every matrix entry
is nonnegative; the heavy-entry lower bound applies for \(q\ge4\), while
\(q=3\) has no heavy digit (`TWOMARK_RENEWAL_SOL.md:295-316`).

Endpoint normalization produces an empty core or a genuine balanced canonical
double-coset word, after which the cumulative Ford bound is applied
(`TWOMARK_RENEWAL_SOL.md:364-414`).  The Ford input itself is a width-one,
finite-\(q\), double-coset count—not a one-sided count and not a theta count
(`M2_FORD_PACKING_REFEREE.md:64-116`).

Lemma 4.1 applies to exactly one marked atom or two distinct left-to-right
marked atoms and provides at most three cores, fewer than \(2^{20}\) finite
tags, at most four gain-bearing integers, and each marked heavy magnitude
(`TWOMARK_RENEWAL_SOL.md:440-463`).  Those are precisely the objects used at
`ATOM_MOMENT_BRIDGE_SOL.md:203-265`.  The target's separate factor 2 for a
distinct pair is conservative whether “ordered” is read as left-to-right order
or as both orientations.

### 2.2 Collision attack

The inverse decoder survives every boundary case in the source tables:

- a bridged run is recovered from its recorded integer;
- an absorbed run is recovered as the tagged maximal boundary run of the
  enlarged core;
- maximality prevents the absorbed run from merging with an old run;
- adjacent \(U,H\), \(H,L\), and \(U,L\) use the coupled tags;
- at the reverse adjacent \(L,U\) junction, the global endpoint exclusions
  force the relevant outer core to be nonempty whenever its outer gain is
  absent, so the two absorptions are independently reversible.

These are the complete one-mark and two-mark branches at
`TWOMARK_RENEWAL_SOL.md:465-560`.  The product-gain conclusion, including the
at-most-three-core and at-most-two-heavy factors, is at
`TWOMARK_RENEWAL_SOL.md:572-590`.

The all-height conclusion here rests on the reversible decoder, not a bounded
collision search.  Earlier draft-only search totals had no preserved runnable
command and are therefore **NOT EVIDENCE**; they are deliberately excluded
from this report's claim ledger.

### 2.3 Summation and constant ledger

**Result: CONFIRMED.**

For a fixed tag and fixed integer data, the core convolution gives

\[
 2^{12}(40Y/D)^2(1+\log_+(40Y/D))^2
\]

(`ATOM_MOMENT_BRIDGE_SOL.md:267-281`).  The convolution constant follows
directly from the cumulative Ford bound: a shell
\([2^i,2^{i+1})\) contains at most \(8\,4^i\) cores, and for three ordered
cores

\[
 8^3\sum_{s=0}^{L}{s+2\choose2}4^s
 \le {2048\over3}Z^2(L+2)^2
 \le2^{12}Z^2(1+\log Z)^2.
\]

No cumulative count is differentiated.

Every unabsorbed auxiliary length contributes a factor \(r^{-2}\) or
\((1+r)^{-2}\); at most four such sums cost less than \(2^4\)
(`ATOM_MOMENT_BRIDGE_SOL.md:283-291`).  Absorbed lengths are not silently
summed: injectivity puts them inside a tagged Ford-counted core.

For a same-heavy diagonal mark, \(n^2\) cancels the \(n^{-2}\) from \(D^{-2}\),
leaving the explicit \(n\)-sum in `ATOM_MOMENT_BRIDGE_SOL.md:302-327`.  For the
remaining fixed tag types:

- distinct heavy-heavy leaves \(1/(nm)\);
- heavy-light leaves \(1/n\);
- light-light and the same-light diagonal leave 1.

The two possible harmonic sums and the squared core-convolution logarithm are
therefore bounded by \((1+\log(40Y))^4\).  Mark types, signs, bridge states,
empty flags, and coupled cases are already summed by the finite-tag factor; no
additional category multiplicity is missing.

The regime conversions at `ATOM_MOMENT_BRIDGE_SOL.md:345-451` are valid.  In
the low regime the rest term decreases after division by \(Y\), and the heavy
integral is maximized at \(H/Y=40\).  In the high regime \(q=3\) is separated
before using \(q/\lfloor q/2\rfloor\le5/2\); for \(q\ge4\) the heavy ratio is
maximal at \(R=1\).  The remaining fourth power uses
\((\log q)^4\le5q\), whose continuous maximum is \(4^4/e^4<5\).

Fresh scalar replay command:

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from mpmath import mp
mp.dps=80
base_exp=12+20+11+4
low_exp=11+1
high_exp=14+1
A2_exp=base_exp+max(low_exp,high_exp)
word_exp=A2_exp+1
print('tag_count=',4**2*3**4*2**3*4*2,'lt_2^17=',4**2*3**4*2**3*4*2 < 2**17)
print('4pi^2=',mp.nstr(4*mp.pi**2,30),'lt_40=',4*mp.pi**2<40)
print('low_log=',mp.nstr((1+mp.log(40))**4,30),'lt_2^10=',(1+mp.log(40))**4<2**10)
c=mp.log(100)
high_diag=mp.mpf(1)/2*(1+2*(1+c)+(c*c+2*c+2))
print('high_diag_R1=',mp.nstr(high_diag,30),'lt_2^5=',high_diag<2**5)
print('base_exp=',base_exp,'low_with_order_exp=',low_exp,'high_with_order_exp=',high_exp)
print('direct_A2_ceiling=2^%d'%A2_exp,2**A2_exp)
print('direct_1_plus_A2_ceiling=2^%d'%word_exp,2**word_exp)
print('RATE_A_C4=2^100',2**100)
print('slack_factor=',2**(100-word_exp),'proved_constant_fits=',2**word_exp<=2**100)
PY
```

Fresh stdout:

```text
tag_count= 82944 lt_2^17= True
4pi^2= 39.4784176043574344753379639995 lt_40= True
low_log= 483.366191181994915204489782827 lt_2^10= True
high_diag_R1= 22.3141365929329787571952985959 lt_2^5= True
base_exp= 47 low_with_order_exp= 12 high_with_order_exp= 15
direct_A2_ceiling=2^62 4611686018427387904
direct_1_plus_A2_ceiling=2^63 9223372036854775808
RATE_A_C4=2^100 1267650600228229401496703205376
slack_factor= 137438953472 proved_constant_fits= True
```

Thus the complete high-regime \(A_X^2\) factor is

\[
 2^{12+20+11+4}\,2^{14}\,2=2^{62}.
\]

The low regime costs only \(2^{59}\).  Ford supplies the unit term
\(\#\{X:x_X\le Y\}\le Y^2\); both regime factors are at least one, so
\(2^{62}+1<2^{63}\).  The constant in `(AM)` is sound.

## 3. Attack (c): forbidden proof routes

**Result: CONFIRMED.**

The displayed \((DH_{2,4})\) theorem is not used as an inequality.  The target
states the direction failure explicitly at `ATOM_MOMENT_BRIDGE_SOL.md:148-154`:
\(k_X^2\le2+8A_X^2\) cannot bound \(A_X^2\) from a \(k_X^2\) moment.  The proof
instead invokes Lemma 4.1, proves the product gain, expands \(A_X^2\), and sums
the codes directly (`ATOM_MOMENT_BRIDGE_SOL.md:203-489`).  The symbol
\((DH_{2,4})\) otherwise names the common population or explains what is not
being used.

There is also no theta-cutoff substitution.  The symbolic proof uses
\(x_X\le Y\) when converting the gain to the core cutoff
(`ATOM_MOMENT_BRIDGE_SOL.md:253-280`) and again in its final moment and Ford
terms (`ATOM_MOMENT_BRIDGE_SOL.md:472-489`).  The target explicitly records the
false converse at `ATOM_MOMENT_BRIDGE_SOL.md:121`; the known \(q=3\) witnesses
\((x,y)=(34,1970),(89,11482)\) are proved at
`TWOMARK_RENEWAL_SOL.md:228-266`.  Theta height appears only in the separately
labelled numerical falsification window, which the target correctly disclaims
at `ATOM_MOMENT_BRIDGE_SOL.md:704-717`.

## 4. Attack (d): numerical falsification

### 4.1 Verbatim replay of the target's \(y\le100\) command

Fresh command, executed from the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from pathlib import Path
from math import gcd
from mpmath import mp
mp.dps=100
P=Path('research_notes/rh_goals_2026-08-14/lane_g/DH_DEPTH_LAW_SOL.md')
s=P.read_text()
a=s.index('from collections import Counter',s.index('self-contained stdout-only'))
b=s.index('\nPY\n',a)
exec(s[a:b].split('q=12;')[0])
mp.dps=100

def N(a,lam):
 u=[mp.mpf(0),mp.mpf(1)]
 for _ in range(1,abs(a)+1):u.append(lam*u[-1]-u[-2])
 n=abs(a); M=[[u[n],u[n+1]],[u[n-1],u[n]]]
 return M if a>0 else [[M[0][0],M[1][0]],[M[0][1],M[1][1]]]
def x_of(ds,lam):
 P=[[mp.mpf(1),0],[0,mp.mpf(1)]]
 for z in ds:P=mm(P,N(z,lam))
 return lam*P[0][0]
def aw(ds):
 heavy=sum(abs(z) for z in ds if abs(z)>=2); ell=0; i=0
 while i<len(ds):
  if abs(ds[i])==1:
   ell+=1; z=ds[i]; i+=1
   while i<len(ds) and ds[i]==z:i+=1
  else:i+=1
 A=heavy+ell
 return A,1+A*A

base=[]
for c in range(1,51):
 for d in range(2*c):
  if gcd(c,d)==1 and (c+d)%2:
   W=from_cd(c,d)
   base.append((c,tuple(z for z in W if z!='Q')))
assert len(base)==1037
print('exact_theta_keys_y_le_100=',len(base))
print('q matched exact_W_window_100 max_A max_event_Creq_up_1e-12 event_x cumulative_W')
global_best=(mp.mpf(0),None)
for q in range(3,51):
 alphabet=set(range(-((q-1)//2),0))|set(range(1,q//2+1))
 lam=2*mp.cos(mp.pi/q); rows=[]
 for c,ds in base:
  if all(z in alphabet for z in ds):
   A,w=aw(ds); x=x_of(ds,lam)
   assert x<=2*c+mp.mpf('1e-80')
   rows.append((x,w,A))
 rows.sort(key=lambda z:z[0])
 exact_total=sum(w for x,w,A in rows)
 best=(mp.mpf(0),None,None); T=0; i=0
 while i<len(rows):
  x=rows[i][0]; j=i
  while j<len(rows) and abs(rows[j][0]-x)<mp.mpf('1e-80'):
   T+=rows[j][1]; j+=1
  R=1+max(mp.mpf(0),mp.log(x/q))
  f=x if x<=q else q*R**2+R**4
  ratio=T/(x*x*f)
  if ratio>best[0]:best=(ratio,x,T)
  i=j
 if best[0]>global_best[0]:global_best=(best[0],q)
 if q in (3,4,5,6,8,12,16,24,32,48,50):
  up=mp.ceil(best[0]*10**12)/10**12
  print(q,len(rows),exact_total,max(A for x,w,A in rows),
        mp.nstr(up,14),mp.nstr(best[1],18),best[2])
print('global_q_3_to_50_max_Creq_up_1e-12=',
      mp.nstr(mp.ceil(global_best[0]*10**12)/10**12,14),'at_q=',global_best[1])
print('diagnostic_only=finite_y_window_not_full_x_cutoff')
PY
```

Fresh output:

```text
exact_theta_keys_y_le_100= 1037
q matched exact_W_window_100 max_A max_event_Creq_up_1e-12 event_x cumulative_W
3 39 227 4 1.000000000001 1.0 1
4 139 2249 7 0.75 2.0 6
5 322 7170 8 0.61300899001 2.61803398874989485 11
6 418 10569 8 0.505181485541 3.46410161513775459 21
8 588 17440 8 0.426406871193 4.8284271247461901 48
12 764 27645 11 0.418424030654 7.46410161513775459 174
16 847 34546 11 0.391542080148 10.0546789842516962 398
24 920 43888 14 0.372963623415 15.4594574178814236 1378
32 960 53252 18 0.378824595609 20.3063407752177209 3172
48 984 62360 24 0.374630408826 30.5141033765310782 10644
50 986 63563 25 0.382295738099 31.7890896877306069 12281
global_q_3_to_50_max_Creq_up_1e-12= 1.000000000001 at_q= 3
diagnostic_only=finite_y_window_not_full_x_cutoff
```

This matches `ATOM_MOMENT_BRIDGE_SOL.md:684-701` row for row.  The
\(q=3,x=1,T=1\) event has exact ratio 1; the target's
`1.000000000001` is a conservative artifact of evaluating
\(2\cos(\pi/3)\) numerically and then applying `ceil`, exactly as the target
states at `ATOM_MOMENT_BRIDGE_SOL.md:704-715`.

## 5. Attack (e): RATE-A promotion logic

**Result: CONFIRMED, with the target's stated paper-level qualifier.**

`RATE_A_REFEREE.md:14-17` identifies the exact missing analytic item: the
needed \(\sum_{x\le Y}(1+A^2)\) moment must be separately obtained from the
direct \(A^2\) coding, because it is not the literal displayed
\((DH_{2,4})\) statement.  The present target states and proves exactly that
corollary.  It does not alter \(p=11/5\), the exponent \(6/5\), activation 12,
or the RATE ledger's declared \(C_4=2^{100}\).

The target does **not** erase the second referee qualification.
`RATE_A_REFEREE.md:18-25` says the fresh \(\phi_q\) computations are not
certified infinite-dimensional Arb enclosures and that the theorem remains
paper-level conditional on the two-mark/Ford proof.  Section 6 of the target
retains both qualifications, keeps standalone N1-RATE conjectural, and says
that divisor/holomorphy/geometry/monotonicity gates for the full program are not
promoted (`ATOM_MOMENT_BRIDGE_SOL.md:719-721`).

Accordingly, the justified status change is exactly:

- **RATE-A analytic inequality:** `CONFIRMED` at paper level on the stated
  balanced/matched boundary scope;
- **machine formalization and certified full-operator numerical enclosure:**
  still open;
- **standalone N1-RATE and non-RATE full-program gates:** not promoted.

This is no broader than the conditional conclusion already allowed at
`RATE_A_REFEREE.md:386-392` once the direct atom moment is separately stated and
refereed.

## 6. Final claim ledger

| Attack | Verdict | Receipt |
|---|---|---|
| \(A_X\) convention and RATE-A usage | **CONFIRMED** | target `:80-119`; boundary theorem `:315-331,371-395,403-419` |
| \(X\leftrightarrow W_X\), \(x\) versus \(m\) | **CONFIRMED** | M1 `:275-340,444-495`; DH2 `:334-349` |
| Lemma 4.1 hypotheses | **CONFIRMED** | TWOMARK `:287-316,364-463`; M2 Ford `:64-116` |
| Marked-code injectivity | **CONFIRMED, paper-level** | TWOMARK `:465-590`; reversible decoder in Section 2.2 |
| Direct summation and \(2^{63}\) | **CONFIRMED** | target `:267-489`; fresh scalar ledger above |
| Inference from displayed \(k^2\) bound | **NOT USED** | target `:148-154,203-489` |
| Theta-cutoff substitution | **NOT USED** | target `:121,253-280,472-489,704-717` |
| Stated \(y\le100\) numerics | **REPRODUCED** | verbatim command/output above |
| RATE-A promotion | **CONFIRMED at paper level only** | RATE referee `:14-25,386-392`; target `:719-721` |

**Final verdict: CONFIRMED.**  The atom-moment bridge closes reason 1 of
`RATE_A_REFEREE.md:14-17`.  The result remains a paper theorem resting on the
already referee-confirmed canonical coding and Ford count; no machine-proof or
full-operator numerical-certification status is implied.

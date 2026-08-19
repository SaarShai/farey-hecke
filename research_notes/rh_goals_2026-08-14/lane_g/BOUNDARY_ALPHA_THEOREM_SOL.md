# The boundary RATE theorem on \(\Gamma_R\)

**Date:** 2026-08-19  
**Program:** `(RATE)`, lane G  
**Interpreter:** `/Users/za/.venvs/farey-rh/bin/python`  
**Write scope:** this file only

## 0. Verdict

The requested boundary theorem is **PROVED at paper level**, conditional only
on the already referee-confirmed paper inputs named below.  The previously
conjectural pointwise N1-RATE statement is **not proved**.  It is bypassed on
the boundary by a theta-endpoint derivative estimate and a shallow/deep split
using the atom moment already proved inside `(DH_{2,4})`.

Let

\[
 \Gamma_R^A=\{1.1+it:|t-t_0|\le\tfrac12\},\qquad
 \Gamma_R^B=\{1.1+it:|t-t_0|<\tfrac14\},
 \qquad t_0=\gamma_1/2.
\]

For every integer \(q\ge12\),

\[
 \boxed{
 \sup_{s\in\Gamma_R^A}|\phi_q(s)-\phi_\infty(s)|
 \le C_R q^{-6/5},
 \qquad
 C_R=10489412368759562746433608215977724802.}
 \tag{RATE-A}
\]

Since \(\Gamma_R^B\subset\Gamma_R^A\), the same bound holds on Route B.
Thus

\[
 \boxed{\alpha=6/5=1.2,\qquad q_{\rm RATE}=12.}
\]

For the best current transport, A0 with the safe ledger constant
\(K_+=117\), the repaired unrounded strict formula gives

\[
 \boxed{
 q_{\rm transport}
 =332093267419812025416641789732742045430624465595.}
 \tag{T}
\]

This is a finite analytic transport cutoff.  It is not, by itself, a final
all-gates \(q_0\): the A0 implication still assumes its stated
closed-rectangle holomorphy/divisor hypotheses.  No such conditional gate is
silently promoted here.

## 1. Fresh receipts before claims

### 1.1 Source state

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
import sys, flint
print(sys.version.split()[0])
print('python-flint', flint.__version__)
PY
shasum -a 256 \
 research_notes/rh_goals_2026-08-14/lane_g/M1_ROUTE_B_REPAIR_SOL.md \
 research_notes/rh_goals_2026-08-14/lane_g/M1_LOCALIZATION_TRIPLE_REFEREE.md \
 research_notes/rh_goals_2026-08-14/lane_g/DH2_RENEWAL_PROOF_SOL.md \
 research_notes/rh_goals_2026-08-14/lane_g/TWOMARK_RENEWAL_SOL.md \
 research_notes/rh_goals_2026-08-14/lane_g/TWOMARK_REFEREE.md \
 research_notes/rh_goals_2026-08-14/lane_g/FW_RENEWAL_COUNT_SOL.md \
 research_notes/rh_goals_2026-08-14/lane_g/FW_REFEREE.md \
 research_notes/rh_goals_2026-08-14/lane_g/M3_UNIFORMITY_EXECUTION_SOL.md \
 research_notes/rh_goals_2026-08-14/lane_g/R3_BOUNDARY_RATE_CAMPAIGN_SOL.md \
 research_notes/rh_goals_2026-08-14/lane_g/KF_WALL_ATTACK_SOL.md \
 research_notes/rh_goals_2026-08-14/lane_g/KF_WALL_REFEREE.md
```

Output:

```text
3.13.13
python-flint 0.9.0
7eb760d6c7314deb7e01cfbc8b07fe3672c2489bbba03abe1eb65f6c6fa96335  research_notes/rh_goals_2026-08-14/lane_g/M1_ROUTE_B_REPAIR_SOL.md
c6ccf070ebe91bed0111036fec2f0561089b0d1dc917398c193cb873c6e8a5d1  research_notes/rh_goals_2026-08-14/lane_g/M1_LOCALIZATION_TRIPLE_REFEREE.md
096d389905ad21505e2c25c30aa37b5a2fa3d3f6d054bcb30229096fc5c8d885  research_notes/rh_goals_2026-08-14/lane_g/DH2_RENEWAL_PROOF_SOL.md
7a553a9c3ed289b513ad8dd7e3a118b0c0d50f92080a1f89a6749fbce44a692b  research_notes/rh_goals_2026-08-14/lane_g/TWOMARK_RENEWAL_SOL.md
07ae98864b6963b14a279cfc463c9d047d0c5e75bc4f8fac876781f34bd28263  research_notes/rh_goals_2026-08-14/lane_g/TWOMARK_REFEREE.md
70cf0a9d12cdc6938c431bd1246b0ca18d929c151fb98399a8e94a75d7f6fd3c  research_notes/rh_goals_2026-08-14/lane_g/FW_RENEWAL_COUNT_SOL.md
39c2e0d10a2ef1bb880e34cd4ca53bc280b451305cac871eb2244bb52e490058  research_notes/rh_goals_2026-08-14/lane_g/FW_REFEREE.md
3fb8f625264d2096ee2a27a252916ec4e4c33801adf8fd638b1f5c2ef47ca208  research_notes/rh_goals_2026-08-14/lane_g/M3_UNIFORMITY_EXECUTION_SOL.md
8567dfaa4fea82aa8f0cddb53df0371bdcc5e1697d2367952a99c46171f6041d  research_notes/rh_goals_2026-08-14/lane_g/R3_BOUNDARY_RATE_CAMPAIGN_SOL.md
efa518c9908e3c68005c3b7349bdee6c4af63dc7146ef85b13882560c2644aad  research_notes/rh_goals_2026-08-14/lane_g/KF_WALL_ATTACK_SOL.md
73c6eb59b25038f9e23ae38fa8c409af65d50fd0219b45417022663486361710  research_notes/rh_goals_2026-08-14/lane_g/KF_WALL_REFEREE.md
```

The paper-level statuses used here are the `CONFIRMED` verdicts in
`M1_LOCALIZATION_TRIPLE_REFEREE.md:1-20`,
`TWOMARK_REFEREE.md:1-24,368-394`, and
`FW_REFEREE.md:1-10,360-401`.  No machine-verification status is inferred
from those paper referees.

The numerical source inputs used below were freshly extracted from those
hashed files as follows.

Command:

```bash
cd research_notes/rh_goals_2026-08-14/lane_g
rg -n -F \
 -e 'C_4=2^{100}' -e 'C_1=128(1+\log2)' -e 'q\ge12' \
 -e 'A=11/20' -e 'm_z>0.0439' -e '\nu_z>0.1552' \
 -e 'M(1.1)<2.775' -e 'K_+<117' \
 {TWOMARK_RENEWAL_SOL,DH2_RENEWAL_PROOF_SOL,N1N3_PROMOTION_EXECUTION_SOL,M3_UNIFORMITY_EXECUTION_SOL,KF_WALL_ATTACK_SOL}.md \
 | head -n 30
```

Relevant output excerpt:

```text
M3_UNIFORMITY_EXECUTION_SOL.md:275: \sup_{s\in K_{15}}|M(s)|=M(1.1)<2.775.
KF_WALL_ATTACK_SOL.md:6:conditional, \(K_+<117\)) CONFIRMED; see `KF_WALL_REFEREE.md`.
KF_WALL_ATTACK_SOL.md:118:m_z>0.0439,\qquad \nu_z>0.1552.
DH2_RENEWAL_PROOF_SOL.md:619:   C_1=128(1+\log2),\quad
N1N3_PROMOTION_EXECUTION_SOL.md:210:> **N1-RATE -- CONJECTURAL with explicit constant $A=11/20$.**  For every
N1N3_PROMOTION_EXECUTION_SOL.md:211:> $q\ge12$ and every canonical representative $w_{\rm can}$ of an
TWOMARK_RENEWAL_SOL.md:42: R=1+\log_+(Y/q),\qquad C_4=2^{100},
```

### 1.2 Boundary constant and strict transport integer

The following is the complete fresh Arb calculation.  `C_R` is the least
integer selected by this calculation above the displayed analytic
coefficient; no decimal midpoint is used as an upper bound.

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import arb, acb, ctx
ctx.dps=120
def Z(a):
 s=str(a); assert '+/-' not in s and 'e' not in s.lower()
 u,v=s.split('.',1); assert set(v)<=set('0'); return int(u)
p=arb(11)/5; alpha=arb(6)/5; C4=arb(2)**100
S=arb('7.648'); t0=(acb.zeta_zero(1)/2).imag
Strue=(arb('1.1')**2+(t0+arb('.5'))**2).sqrt()
F=arb(1225)/4+arb(91605)/12
pair=2*arb.pi()**2*(S+1)*p*C4*F
wrap=p*128*(1+arb(2).log())*30
CRraw=arb('2.775')*(pair+wrap); CR=Z(CRraw.upper().ceil())
nu=arb('.1552'); m=arb('.0439'); K=arb(117)
T0=((1-nu)*K.log()-m.log())/(alpha*nu)
T=T0+arb(CR).log()/alpha; eT=T.exp()
lo=Z(eT.lower().floor()); hi=Z(eT.upper().floor()); qt=hi+1
ER=arb(CR)*arb(qt)**(-alpha); lhs=K**(1-nu)*ER**nu
print('S_GammaA=',Strue)
print('S_GammaA_lt_7.648=',bool(Strue<S))
print('C4=',Z(C4))
print('F_q_ge_12=',F)
print('C_pair_D_upper=',pair.upper())
print('C_wrap_D_upper=',wrap.upper())
print('C_R_raw_upper=',CRraw.upper())
print('C_R=',CR,'strict_upper=',bool(arb(CR)>CRraw))
print('T0=',T0)
print('T=',T)
print('floor_exp_T_lower=',lo)
print('floor_exp_T_upper=',hi)
print('q_transport=',qt)
print('minimality=',bool(arb(qt).log()>T),bool(arb(qt-1).log()<=T))
print('ER_upper=',ER.upper())
print('A0_lhs_upper=',lhs.upper())
print('A0_strict_pass=',bool(lhs<m))
PY
```

Output:

```text
S_GammaA= [7.64689324359664784257757250829709001545013197505903589917971086208691467760814275858263781971889054003576111614315180519 +/- 3.17e-120]
S_GammaA_lt_7.648= True
C4= 1267650600228229401496703205376
F_q_ge_12= 7940.00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
C_pair_D_upper= [3779968421174617205922020978730697336.34741621557852099891107739414740604452136842302799741605837041702238161629162918098 +/- 2.39e-84]
C_wrap_D_upper= [14303.7073813704179739567769620786756471018251350754363868115047202001893183999809574383333864657450723548285116617811531 +/- 1.60e-116]
C_R_raw_upper= [10489412368759562746433608215977724801.1520633011402735020343095370839724811115472082386662314875764627624675451564278686 +/- 1.10e-83]
C_R= 10489412368759562746433608215977724802 strict_upper= True
T0= [38.3855535814978294420003556267900758051983773340406350057310476940949540845669325281835202839273579004267025611445252549 +/- 6.19e-119]
T= [109.421745040159523743786563571204541418610221760122809740649383677414556636701621643295058126247232491747486173765945251 +/- 3.60e-118]
floor_exp_T_lower= 332093267419812025416641789732742045430624465594
floor_exp_T_upper= 332093267419812025416641789732742045430624465594
q_transport= 332093267419812025416641789732742045430624465595
minimality= True True
ER_upper= [9.89097430637911054877177614823468640968794281344579185756013275732945984464792127524610837468979670054487699612505873990e-21 +/- 2.75e-141]
A0_lhs_upper= [0.0438999999999999999999999999999999999999999999999906971726823547524124317246131129625859299593282570137277179991715092729 +/- 3.75e-122]
A0_strict_pass= True
```

## 2. What was still missing before this note

### 2.1 The exact boundary and the absolutely convergent series

`R3_BOUNDARY_RATE_CAMPAIGN_SOL.md:47-78` defines the two contours and their
supremum norms.  The larger closed contour \(\Gamma_R^A\) safely feeds both
transports.  A single anchor-height evaluation cannot replace either
supremum.

For \(\Re s>1\), the exact normalization is

\[
 \phi_q(s)=M(s)D_q(s),\qquad
 M(s)=\sqrt\pi\,{\Gamma(s-1/2)\over\Gamma(s)},\qquad
 D_q(s)=\sum_{[\gamma],\,c_\gamma\ne0}|c_\gamma|^{-2s}.
 \tag{2.1}
\]

This is `R3_BOUNDARY_RATE_CAMPAIGN_SOL.md:219-228`.  On \(\sigma=1.1\)
all series below converge absolutely.  No strip continuation or
\(s\)-derivative is used in this proof.

### 2.2 The confirmed decomposition and the three terms

`DH2_RENEWAL_PROOF_SOL.md:610-638` proves

\[
 |D_q(s)-D_\theta(s)|
 \le E_{\rm wrap}+E_{\rm Cheb}+E_{\rm pair,res}.       \tag{2.2}
\]

Their exact roles on \(\Gamma_R\) are:

1. \(E_{\rm wrap}\) is the theta-side mass outside the image of the
   balanced Route-B section.  Referee-confirmed `(FW)` gives, for
   \(p=2\sigma\),
   \[
   E_{\rm wrap}(q,s)
   \le pC_1G(p)q^{1-p},\quad
   C_1=128(1+\log2),\quad
   G(p)={1\over p-2}+{1\over(p-2)^2}.                 \tag{2.3}
   \]
2. \(E_{\rm Cheb}\) is the separately extracted pair majorant for the two
   pure Chebyshev extremal families.  Its exact trigonometric estimate is
   already \(O(q^{1-p})\); see
   `DH_DEPTH_LAW_SOL.md:637-709`.
3. \(E_{\rm pair,res}\) is the nonnegative majorant for all remaining
   matched pair differences.  It was the only unbounded term after
   `(FW)`, the endpoint comparison \(x_X\le y_X\), and `(DH_{2,4})` were
   confirmed.

Thus the first two pieces already have exponent \(p-1\).  At
\(p=11/5\), this is \(6/5\).  The old obstruction was not absolute
convergence; it was the lack of a relative endpoint-drift bound for the
third piece.

### 2.3 Exact role and status of N1-RATE

The corrected statement in `N1N3_PROMOTION_EXECUTION_SOL.md:208-220` is

\[
 \sup_{\lambda\in[\lambda_q,2]}|c'_{w_{\rm can}}(\lambda)|
 \le {11\over20}k_{\rm can}^2
       |c_{w_{\rm can}}(\lambda_q)|                 \tag{N1-RATE}
\]

for \(q\ge12\) and canonical representatives of M1-matched double cosets.
It would combine P3, the corrected complex-power MVT, and `(DH_{2,4})` to
bound \(E_{\rm pair,res}\).  Its role is pointwise in the canonical word;
on \(\Gamma_R\), the spectral parameter contributes only the harmless
factors \(2|s|\) and \(|M(s)|\).

The all-reduced-word version is **FALSE**.  The exact all-ones family in
`N1N3_PROMOTION_EXECUTION_SOL.md:29-99` makes its proposed universal ratio
unbounded, although those long words collapse to the double coset of \(Q\).
The canonical N1-RATE statement with \(A=11/20\) remains
**CONJECTURAL**: neither P1--P3 nor `(DH_{2,4})` proves a pointwise lower
bound stable under cancellation.  The corrected claim is:

> N1-RATE is still unproved as a standalone pointwise theorem, but it is no
> longer needed for the boundary sum.

## 3. The new boundary-only argument

### 3.1 Canonical positive blocks and the atom weight

For a balanced canonical Route-B word, write

\[
 P_W(\lambda)=
 \bigl(N_{a_0}(\lambda)\cdots N_{a_r}(\lambda)\bigr)_{11},
 \quad
 x_W(\lambda)=\lambda P_W(\lambda),
 \quad x_W=x_W(\lambda_q),\quad y_W=x_W(2).
 \tag{3.1}
\]

Here

\[
 N_n=M_n,\quad N_{-n}=M_n^t,\qquad
 M_n=\begin{pmatrix}u_n&u_{n+1}\\u_{n-1}&u_n\end{pmatrix},
 \quad
 u_j(\lambda)=U_{j-1}(\lambda/2).
 \tag{3.2}
\]

These are the proved identities in
`DH2_RENEWAL_PROOF_SOL.md:264-348`.  In the balanced alphabet
\(|a_i|\le h=\lfloor q/2\rfloor\), all entries are nonnegative and
nondecreasing on \([\lambda_q,2]\), so \(x_W\le y_W\).

Compress every maximal same-sign run of unit digits into

\[
 U^t=\begin{pmatrix}1&t\lambda\\0&1\end{pmatrix},
 \qquad
 L^t=\begin{pmatrix}1&0\\t\lambda&1\end{pmatrix}.
\]

Keep every digit \(|a_i|=n\ge2\) as one heavy atom.  Define exactly as in
`TWOMARK_RENEWAL_SOL.md:268-355`

\[
 A(W)=\sum_{|a_i|\ge2}|a_i|+\ell(W),qquad
 w(W)=1+A(W)^2,                                      \tag{3.3}
\]

where \(\ell(W)\) is the number of maximal light runs.

### 3.2 Theta-endpoint derivative lemma

**Lemma 3.1 — PROVED.**  For every balanced canonical word and every
\(\lambda\in[\lambda_q,2]\),

\[
 0\le x_W'(\lambda)\le {w(W)\over2}\,y_W.            \tag{3.4}
\]

**Proof.**  For \(j\ge1\),

\[
 u_j(\lambda)
 =\prod_{m=1}^{j-1}
   \left(\lambda-2\cos{m\pi\over j}\right).          \tag{3.5}
\]

Every index occurring in a heavy block is at most \(h+1<q\).  Hence every
factor in (3.5) is positive on \([\lambda_q,2]\).  Differentiating the
product once and twice shows that \(u_j'\ge0\) and \(u_j''\ge0\) there.
Consequently

\[
 0\le u_j'(\lambda)\le u_j'(2)
 ={j(j^2-1)\over6},qquad u_j(2)=j.                  \tag{3.6}
\]

For a heavy atom of magnitude \(n\ge2\), its nonzero entries have
\(j\in\{n-1,n,n+1\}\), and therefore

\[
 {u_j'(\lambda)\over u_j(2)}
 \le {j^2-1\over6}\le {n^2\over3}.                  \tag{3.7}
\]

For a light block, the only nonconstant entry is \(t\lambda\), whose
derivative divided by its value at \(2\) is \(1/2\).

Expand \(P_W\) as a sum over state paths through the atom matrices.  For
each nonzero path, the product rule, entrywise monotonicity, and (3.7) give

\[
 {\text{path derivative at }\lambda
   \over\text{path value at }2}
 \le {1\over3}\sum_{\rm heavy}n^2+{\ell\over2}
 \le {A(W)^2\over2}.                                \tag{3.8}
\]

The last inequality follows by putting \(H=\sum n\):

\[
 {H^2\over3}+{\ell\over2}
 \le{(H+\ell)^2\over2}.
\]

Summing paths yields
\(P_W'(\lambda)\le A(W)^2P_W(2)/2\).  Since
\(0<\lambda\le2\) and \(P_W(\lambda)\le P_W(2)\),

\[
 x_W'(\lambda)=P_W(\lambda)+\lambda P_W'(\lambda)
 \le(1+A(W)^2)P_W(2)={w(W)\over2}y_W.
\]

This proves (3.4). \(\square\)

The lemma is deliberately relative to the theta endpoint \(y_W\), not to
the finite endpoint \(x_W\).  Thus it does not prove N1-RATE and does not
contradict its counterexample.

### 3.3 Atom-moment corollary of `(DH_{2,4})`

**Lemma 3.2 — PROVED from the confirmed two-mark coding.**  Put

\[
 \mathcal W_q(Y)=\sum_{W:x_W\le Y}w(W),\qquad
 R=1+\log_+(Y/q),\qquad C_4=2^{100}.
\]

Then, for \(q\ge3\), \(Y\ge1\),

\[
 \mathcal W_q(Y)\le C_4Y^2
 \begin{cases}
 Y,&1\le Y\le q,\\
 qR^2+R^4,&Y\ge q.
 \end{cases}                                         \tag{3.9}
\]

**Proof.**  The proof of `(DH_{2,4})` does more than its final
\(k(W)^2\)-statement.  It first expands \(A(W)^2\) into one-mark diagonal
and two-distinct-mark terms (`TWOMARK_RENEWAL_SOL.md:593-600`), injectively
encodes those marks (`:440-590`), and sums every term (`:601-715`).  The
published factor budget below \(2^{65}\) at `:717-738` already includes the
extra conversion \(k^2\le2+8A^2\).  Removing that conversion can only lower
the budget.  The additional unit weight is bounded by the Ford count
\(\#\{x_W\le Y\}\le Y^2\), which is below either right-hand regime in
(3.9).  Thus the same declared ceiling \(C_4=2^{100}\) bounds
\(1+A(W)^2\). \(\square\)

For \(2<p<3\), positive layer cake now gives

\[
 \begin{aligned}
 S_w(p,q)&:=\sum_W w(W)x_W^{-p}\\
 &\le pC_4\left[
 \left({1\over3-p}+J_2(p)\right)q^{3-p}
 +J_4(p)q^{2-p}\right],                              \tag{3.10}
 \end{aligned}
\]

where

\[
 \begin{aligned}
 J_2(p)&={1\over p-2}+{2\over(p-2)^2}+{2\over(p-2)^3},\\
 J_4(p)&={1\over p-2}+{4\over(p-2)^2}+{12\over(p-2)^3}
 +{24\over(p-2)^4}+{24\over(p-2)^5}.
 \end{aligned}
\]

This is the same Tonelli calculation as
`TWOMARK_RENEWAL_SOL.md:763-788`, now applied to (3.9).

### 3.4 Shallow/deep absorption

Put \(\delta_q=2-\lambda_q\le\pi^2/q^2\).  Integrating Lemma 3.1 gives

\[
 0\le y_W-x_W\le {\delta_qw(W)\over2}y_W.            \tag{3.11}
\]

Split the paired population into

\[
 \mathcal S=\{W:w(W)\le q^2/\pi^2\},\qquad
 \mathcal D=\{W:w(W)>q^2/\pi^2\}.
\]

On \(\mathcal S\), (3.11) gives \(x_W\ge y_W/2\), hence

\[
 y_W-x_W\le\delta_qw(W)x_W.
\]

The corrected complex-power MVT, valid here because \(\sigma=1.1>-1/2\),
therefore gives

\[
 |x_W^{-2s}-y_W^{-2s}|
 \le2|s|\delta_qw(W)x_W^{-p}.                         \tag{3.12}
\]

On \(\mathcal D\), use absolute convergence and \(x_W\le y_W\):

\[
 |x_W^{-2s}-y_W^{-2s}|
 \le x_W^{-p}+y_W^{-p}
 \le2x_W^{-p}
 <{2\pi^2\over q^2}w(W)x_W^{-p}.                    \tag{3.13}
\]

Adding (3.12)--(3.13) and then enlarging both sub-sums to the full positive
sum proves the unconditional paired bound

\[
 \boxed{
 E_{\rm pair,all}(q,s)
 \le {2\pi^2(|s|+1)\over q^2}S_w(p,q).}              \tag{3.14}
\]

In particular, this bounds \(E_{\rm pair,res}\).  More efficiently, return
to the exact matched-plus-wrap identity
`M1_ROUTE_B_REPAIR_SOL.md:808-854`: (3.14) bounds the whole paired sum,
including the Chebyshev pairs, so the older separate Chebyshev majorant need
not be added a second time.

Combining (3.10) and (3.14) gives, for \(2<p<3\),

\[
 \boxed{
 \begin{aligned}
 E_{\rm pair,all}(q,s)
 \le{}&2\pi^2(|s|+1)pC_4
 \bigg[
 \left({1\over3-p}+J_2(p)\right)q^{1-p}
 +J_4(p)q^{-p}
 \bigg].
 \end{aligned}}                                      \tag{3.15}
\]

This is boundary-only: it uses positivity, absolute convergence, and the
fixed line \(\sigma>1\).  It asserts no strip transport theorem.

## 4. Assembly on \(\Gamma_R\)

Set \(p=11/5\).  Then

\[
 J_2=305,qquad J_4=91605,qquad
 {1\over3-p}+J_2={1225\over4}.
\]

For \(q\ge12\),

\[
 {1225\over4}+{91605\over q}\le7940.                \tag{4.1}
\]

The fresh Arb receipt proves

\[
 \sup_{s\in\Gamma_R^A}|s|<7.648.                    \tag{4.2}
\]

Equations (3.15), (4.1), and (4.2) give

\[
 E_{\rm pair,all}(q,s)
 <3779968421174617205922020978730697336.348\,q^{-6/5}.
 \tag{4.3}
\]

The confirmed `(FW)` bound (2.3), with \(G(11/5)=30\), gives

\[
 E_{\rm wrap}(q,s)<14303.708\,q^{-6/5}.              \tag{4.4}
\]

The beta-integral proof in
`M3_UNIFORMITY_EXECUTION_SOL.md:255-280` gives, uniformly in height,

\[
 |M(1.1+it)|\le M(1.1)<2.775.                        \tag{4.5}
\]

The exact Route-B section identity has no finite-side unmatched mass.
Therefore (4.3)--(4.5), with \(D_\theta\) in the established normalization
of \(\phi_\infty\), give

\[
 \begin{aligned}
 |\phi_q(s)-\phi_\infty(s)|
 &\le |M(s)|\{E_{\rm pair,all}+E_{\rm wrap}\}\\
 &<10489412368759562746433608215977724802\,q^{-6/5}
 \end{aligned}
\]

for every \(q\ge12\) and every \(s\in\Gamma_R^A\).  This proves
`(RATE-A)` and its Route-B restriction.

## 5. Activation and repaired transport cutoff

### 5.1 RATE onset

The two-term estimate (3.15) is valid already in the full stated range of
the confirmed canonical/renewal inputs.  The single-constant theorem
`(RATE-A)` uses exactly the absorption (4.1).  Hence its declared activation
is

\[
 \boxed{q_{\rm RATE}=12.}
\]

No computation for \(12\le q\le48\) is used to prove the tail, and no
finite numerical fit is used to select \(\alpha\).

### 5.2 A0 transport

Use the safe A0 ledger values

\[
 K_+=117,qquad \nu=0.1552,qquad m=0.0439,qquad
 \alpha=6/5.
\]

The strict A0 condition is

\[
 K_+^{1-\nu}(C_Rq^{-\alpha})^\nu<m.
\]

The referee also requires the original side hypothesis
\(0<E_R(q)\le K_+\).  If \(E_R(q)=0\), the desired A0 conclusion is
immediate.  Otherwise, at and beyond the cutoff computed below, the fresh
receipt gives
\[
 E_R(q)\le C_Rq^{-6/5}
 \le 9.891\times10^{-21}<117=K_+,
\]
so this separate hypothesis is satisfied rather than omitted.

Solving without intermediate decimal rounding gives

\[
 \log q>
 T:={(1-\nu)\log K_+-\log m\over\alpha\nu}
       +{1\over\alpha}\log C_R.                     \tag{5.1}
\]

The coefficient of \(\log C_R\) is exactly \(5/6\).  The fresh receipt
encloses

\[
 T=109.4217450401595237437865635712045\ldots
\]

and proves that the lower and upper Arb endpoints of \(e^T\) have the same
integer floor.  Because (5.1) is strict, the repaired referee rule is

\[
 q_{\rm transport}=\lfloor e^T\rfloor+1,
\]

not a rounded display followed by exponentiation.  This gives (T).  The
receipt also proves both minimality statements for this fixed envelope:

\[
 \log q_{\rm transport}>T,qquad
 \log(q_{\rm transport}-1)\le T,
\]

and directly checks the A0 left side is strictly below \(0.0439\).

This uses the best contribution in `KF_WALL_ATTACK_SOL.md:596-661` after the
rounding repairs in `KF_WALL_REFEREE.md:326-371`.  The rebuilt Route-B chain
with the safe constant \(K_F=109\) is not selected because its unrounded
transport base is much larger.  Raw strict suprema \(<117\) and \(<109\)
are not confused with the chosen safe ledger constants \(117\) and \(109\).

The full program onset remains

\[
 q_0=\max\{12,q_{\rm RATE},q_{\rm transport},
 q_{\rm divisor},q_{\rm geometry},q_{\rm monotone},\ldots\}.
\]

This note makes the RATE and transport entries explicit and finite.  Any
still-conditional non-RATE gate remains conditional.

## 6. Claim ledger

| Claim | Verdict | Reason |
|---|---|---|
| Confirmed decomposition \(E_{\rm wrap}+E_{\rm Cheb}+E_{\rm pair,res}\) | **PROVED / paper-level inputs** | `DH2_RENEWAL_PROOF_SOL.md:610-638`; confirmed `(FW)` and endpoint theorem |
| \(E_{\rm wrap}=O(q^{1-p})\) | **PROVED / referee-confirmed** | (2.3) |
| \(E_{\rm Cheb}=O(q^{1-p})\) | **PROVED** | exact trigonometric estimate |
| N1-strong on all reduced words | **FALSE** | exact near-relation family; corrected domain is canonical |
| Canonical N1-RATE with \(A=11/20\) | **CONJECTURAL** | no cancellation-stable pointwise proof |
| Theta-endpoint derivative Lemma 3.1 | **PROVED here** | positive root factorization plus atom path expansion |
| Atom-moment Lemma 3.2 | **PROVED here from confirmed `(DH_{2,4})` coding** | the coding bounds \(A^2\) before its final conversion to \(k^2\) |
| Full paired boundary majorant (3.15) | **PROVED here** | shallow absorption plus deep atom-moment tail |
| Boundary RATE with \(\alpha=6/5\), \(C_R\) above, \(q_{\rm RATE}=12\) | **PROVED here, paper-level** | Sections 3--4 and fresh Arb ceilings |
| A0 \(q_{\rm transport}\) in (T) | **PROVED conditional transport cutoff** | unrounded strict formula; floor agreement and direct Arb check |
| Final all-gates \(q_0=q_{\rm transport}\) | **NOT CLAIMED** | divisor/holomorphy and other declared activation gates remain separate |

## 7. Dated promotion block — 2026-08-19

This append-only block supersedes only the **status** wording in Section 6; it
does not rewrite the proof or enlarge its domain.  The separate adversarial
report `AM_REFEREE.md` confirms the direct atom-moment bridge at paper level
and closes the sole mathematical gap identified by `RATE_A_REFEREE.md`.

Banking receipts, run from the repository root:

```bash
rg -n "^\*\*Verdict|^\*\*Final verdict|RATE-A analytic inequality|machine formalization|standalone N1-RATE" \
  research_notes/rh_goals_2026-08-14/lane_g/AM_REFEREE.md
```

```text
7:**Verdict:** **CONFIRMED — paper-level, conditional on the already accepted Route-B/Ford inputs; not machine-verified.**
375:retains both qualifications, keeps standalone N1-RATE conjectural, and says
381:- **RATE-A analytic inequality:** `CONFIRMED` at paper level on the stated
383:- **machine formalization and certified full-operator numerical enclosure:**
385:- **standalone N1-RATE and non-RATE full-program gates:** not promoted.
405:**Final verdict: CONFIRMED.**  The atom-moment bridge closes reason 1 of
```

```bash
sed -n '187,206p' research_notes/rh_goals_2026-08-14/lane_g/AM_REFEREE.md | bash
```

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

Therefore `(RATE-A)` is now **CONFIRMED at paper level** on the stated
balanced/matched boundary \(\Gamma_R^A\), with exponent \(6/5\), activation
\(q_{\rm RATE}=12\), and the unchanged advertised upward ceiling

\[
C_R=10489412368759562746433608215977724802.
\]

The confirmation remains conditional only on the already referee-confirmed
paper-level Route-B/Ford inputs.  It is not a machine formalization or a
certified full-operator enclosure.  Standalone N1-RATE remains
**CONJECTURAL** and bypassed, not proved.  No whole-tail monotonicity, finite
base block, all-gates activation, or final \(q_0\) status is promoted here.

## 8. Dated reduced-constant promotion — 2026-08-19

This append-only block adds a sharper alternative constant; it does not erase
or invalidate the published ceiling in Sections 4 and 7.  The direct atom
bridge permits the paper-level coefficient

\[
C_4'=2^{62}+1=4611686018427387905.
\]

Keeping the same balanced/matched boundary, \(p=11/5\), \(\alpha=6/5\),
\(q_{\rm RATE}=12\), \(S=7.648\), \(M_0=2.775\), wrap term, and already
accepted Route-B/Ford premises, the positive source-invariant assembly gives
the sharper outward ceiling

\[
\boxed{C_R'=38160259896392973127946053}.
\]

The first cold referee confirmed the coefficient substitution, the combined
ceiling, its one-less failure, and the strict A0 arithmetic.  It found one
documentation gap: `CR_REDUCTION_SOL.md` had not ranked the losses.  Section 8
of that note appended the missing autopsy; the separate
`CR_REDUCTION_REREFEREE.md` then confirmed the repair.  Immutable hashes are:

```text
89fc61e9bc33db55c95856f5412e87c45da72d3623616435575fb494321b3417  CR_REDUCTION_SOL.md
f0f71f09c1c4547805c44f4c649c12a26568fa0f2e8843a90d574ea856dcfa5a  CR_REDUCTION_REFEREE.md
00cebb30a7370e5487575c181be1878d37ea1a99a9ff8fdacbbdeb05f1898de6  CR_REDUCTION_REREFEREE.md
```

Banking command:

```bash
sed -n '273,322p' \
  research_notes/rh_goals_2026-08-14/lane_g/CR_REDUCTION_SOL.md \
  | bash \
  | rg 'primary_2|C_R=|q_transport=|minimality=|A0_strict_pass|delta_T_current_minus_primary'
```

Relevant output:

```text
primary_2^62_plus_1
C_R= 38160259896392973127946053 strict_upper= True
q_transport= 97418971860452658435229799565334786148
minimality= True True
A0_strict_pass= True
delta_T_current_minus_primary_2^62_plus_1= [21.9496607177316014646974500060214427529785413073316637407932482061698093994468646835003356177914108 +/- 5.50e-98]
```

Thus the already paper-level-confirmed `(RATE-A)` statement may use
\(C_R'\) on exactly its prior scope.  Under the selected A0 envelope, the
corresponding strict conditional analytic transport cutoff is

\[
q_{\rm transport}'=97418971860452658435229799565334786148.
\]

This is not a final program \(q_0\).  The old published \(C_R\) remains a
valid ceiling; the \(2^{63}\) fallback remains valid but weaker.  The
counterfactual \(F(q)\), contour-\(S\), and unavailable \(M_0\) tightenings in
the autopsy are not promoted.  Machine formalization, a certified
full-operator enclosure, standalone N1-RATE, the true finite base block, and
the remaining all-gates closure remain **OPEN** or **CONJECTURAL** exactly as
in the prior ledgers.

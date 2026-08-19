# Cold referee: Route-B endpoint effective tail and cover

**Date:** 2026-08-19
**Candidate:** 1059d6af1934a40d8c57aa7773a6535a41745d34
**Reviewed files:** LAW_EFFECTIVE_TAIL_COVER_SOL.md and
law_probes/routeb_endpoint_p3_cover.py
**Write scope:** this referee artifact only.

## Verdict

**CONFIRMED, with the candidate's stated paper-level conditional scope.** The
direct endpoint \(p=3\) estimate, its exact constants, whole-tail
monotonicity, and a sufficient outward-Arb pointwise cover survive the cold
attacks. More precisely, conditional on the already accepted paper-level
matched Route-B/Ford/marked-coding inputs, for every \(q\ge3\) and
\(s=3/2+it\),

\[
 |\phi_q(s)-\phi_\infty(s)|
 \le 12q^{-2}\left[
 \pi^2(|s|+1)(2^{62}+1)
 \left(\log q+5+\frac{65}{q}\right)
 +128(1+\log2)\right].                       \tag{R.1}
\]

On the candidate's right side

\[
 \Gamma_R=\left\{\frac32+it:|t-t_0|\le2.38\right\},
\]

\(|s|\) may be replaced by the outward upper bound

\[
 S_R=\sqrt{(3/2)^2+(t_0+2.38)^2}.
\]

With this \(S_R\), the pointwise two-constants/Rouché pincer is certified for
every integer

\[
 q\ge Q:=31951437654668744792.                \tag{R.2}
\]

This last statement is conditional on the finite-\(q\) difference being
holomorphic on the chosen enlarged rectangle and on the other stated
transport hypotheses. A fresh 120-decimal, refined outward cover below
confirms (R.2) independently of the candidate's very narrow 70-decimal pass.

This verdict is deliberately narrower than the LAW. It confirms a
theorem-level endpoint boundary estimate and a sufficient, astronomically
large conditional tail onset. It does **not** prove the finite block
\(3\le q<Q\), does not prove the enlarged-rectangle analytic hypotheses, does
not establish a least onset, and does not promote the full LAW. Those claims
remain **OPEN**; any stronger formulation remains **CONJECTURAL**.

## 1. Candidate identity and immutable receipts

Commands:

~~~bash
git rev-parse HEAD
git show -s --format='commit=%H%nparent=%P%nsubject=%s' HEAD
shasum -a 256 \
  research_notes/rh_goals_2026-08-14/lane_g/LAW_EFFECTIVE_TAIL_COVER_SOL.md \
  research_notes/rh_goals_2026-08-14/lane_g/law_probes/routeb_endpoint_p3_cover.py \
  research_notes/rh_goals_2026-08-14/lane_g/BOUNDARY_ALPHA_THEOREM_SOL.md \
  research_notes/rh_goals_2026-08-14/lane_g/ATOM_MOMENT_BRIDGE_SOL.md \
  research_notes/rh_goals_2026-08-14/lane_g/AM_REFEREE.md \
  research_notes/rh_goals_2026-08-14/lane_g/FW_RENEWAL_COUNT_SOL.md \
  research_notes/rh_goals_2026-08-14/lane_g/FW_REFEREE.md \
  research_notes/rh_goals_2026-08-14/lane_g/CR_REDUCTION_REREFEREE.md \
  research_notes/rh_goals_2026-08-14/lane_g/M3_UNIFORMITY_EXECUTION_SOL.md \
  research_notes/rh_goals_2026-08-14/lane_g/M2_PERTERM_REFEREE.md \
  research_notes/rh_goals_2026-08-14/lane_g/LAW_HEJHAL_S7_EXTRACT.md \
  research_notes/rh_goals_2026-08-14/lane_p/literature/Hejhal_LNM1001_Vol2_s7_pp568-600.pdf
~~~

Output:

~~~text
1059d6af1934a40d8c57aa7773a6535a41745d34
commit=1059d6af1934a40d8c57aa7773a6535a41745d34
parent=441fca69dc7bd1eacca7bc17b927b817cd801a55
subject=(LAW) add endpoint effective-tail cover candidate
57338bca4aed790a75c33dd6e871e3db7e25deeed69b6ea9521b0a09f11f76e0  research_notes/rh_goals_2026-08-14/lane_g/LAW_EFFECTIVE_TAIL_COVER_SOL.md
c167f48ec53091ba9fab7b3de940c5dc361c3a565294d6f7b33e3b3015ac3a90  research_notes/rh_goals_2026-08-14/lane_g/law_probes/routeb_endpoint_p3_cover.py
1a5a96e6e2a5ca76a917a7e20e8458038e43e5609139b70624ab5a59b8e13c59  research_notes/rh_goals_2026-08-14/lane_g/BOUNDARY_ALPHA_THEOREM_SOL.md
59ce32f7c6fa86580055d9049e609a2189ecc1645528dd4136758fcf547fbbbb  research_notes/rh_goals_2026-08-14/lane_g/ATOM_MOMENT_BRIDGE_SOL.md
3d655f2c05395688be73e8786cd9a954182cc4842005ff9e7662d05cccf503b4  research_notes/rh_goals_2026-08-14/lane_g/AM_REFEREE.md
70cf0a9d12cdc6938c431bd1246b0ca18d929c151fb98399a8e94a75d7f6fd3c  research_notes/rh_goals_2026-08-14/lane_g/FW_RENEWAL_COUNT_SOL.md
39c2e0d10a2ef1bb880e34cd4ca53bc280b451305cac871eb2244bb52e490058  research_notes/rh_goals_2026-08-14/lane_g/FW_REFEREE.md
00cebb30a7370e5487575c181be1878d37ea1a99a9ff8fdacbbdeb05f1898de6  research_notes/rh_goals_2026-08-14/lane_g/CR_REDUCTION_REREFEREE.md
3fb8f625264d2096ee2a27a252916ec4e4c33801adf8fd638b1f5c2ef47ca208  research_notes/rh_goals_2026-08-14/lane_g/M3_UNIFORMITY_EXECUTION_SOL.md
ae8cf73980517ff18554c5d86da3627bfe6f3018252f259be741df05e241c44b  research_notes/rh_goals_2026-08-14/lane_g/M2_PERTERM_REFEREE.md
c65eec51a9131651c81484326932a96615e095cb0ae00d9ed142cc3ede377503  research_notes/rh_goals_2026-08-14/lane_g/LAW_HEJHAL_S7_EXTRACT.md
b0f9a7001b10f5e0eae5e5aca85124c0a233256aa0e08b5c0f04720185a2b1e9  research_notes/rh_goals_2026-08-14/lane_p/literature/Hejhal_LNM1001_Vol2_s7_pp568-600.pdf
~~~

The candidate itself is scoped as CONDITIONAL CANDIDATE and explicitly
denies an unconditional LAW claim at lines 3--6 and 35--46. The endpoint
bound is lines 120--260, the cover is lines 262--360, and the open-gate ledger
is lines 390--423.

The inherited status words were checked directly rather than inferred from
filenames:

~~~bash
rg -n -F -e '**Verdict:**' -e '1/2<=sigma<=3/2' \
  research_notes/rh_goals_2026-08-14/lane_g/{AM_REFEREE,FW_REFEREE,M2_PERTERM_REFEREE}.md
rg -n -F -e "C4'=2^62+1" -e 'full all-q R5 program remains' \
  research_notes/rh_goals_2026-08-14/lane_g/{CR_REDUCTION_REREFEREE,R5_ACTIVATION_CLOSURE_REFEREE}.md
~~~

Output:

~~~text
research_notes/rh_goals_2026-08-14/lane_g/AM_REFEREE.md:7:**Verdict:** **CONFIRMED — paper-level, conditional on the already accepted Route-B/Ford inputs; not machine-verified.**
research_notes/rh_goals_2026-08-14/lane_g/FW_REFEREE.md:5:**Verdict:** **CONFIRMED — paper-level, not machine-formalized.**
research_notes/rh_goals_2026-08-14/lane_g/M2_PERTERM_REFEREE.md:114:epsilon>0,  1/2<=sigma<=3/2,  |t|>=epsilon,  N<infinity,
research_notes/rh_goals_2026-08-14/lane_g/CR_REDUCTION_REREFEREE.md:361:missing ranked-autopsy/documentation item. C4'=2^62+1 and
research_notes/rh_goals_2026-08-14/lane_g/R5_ACTIVATION_CLOSURE_REFEREE.md:10:monotone function. The full all-q R5 program remains **OPEN / UNDEFINED**.
~~~

## 2. Endpoint source-domain attack

### 2.1 Atom moment and exact \(C_4\)

The exact source weight is \(w_X=1+A_X^2\), not a silently substituted depth
weight. BOUNDARY_ALPHA_THEOREM_SOL.md:323-331 defines this weight and its
theta-endpoint derivative lemma; lines 459--502 give the shallow/deep paired
bound. The direct atom bridge proves

\[
 \sum_{x_X\le Y}A_X^2<2^{62}Y^2
 \begin{cases}
 Y,&1\le Y\le q,\\
 qR^2+R^4,&Y>q,
 \end{cases}
\]

and then adds the Ford unit term. The decisive source lines are
ATOM_MOMENT_BRIDGE_SOL.md:472-489:

~~~text
475  sum_{X:x_X<=Y} A_X^2 < 2^62 Y^2 [regime factor]
483  Finally, Ford gives
486  #{X in C_q:x_X<=Y} <= Y^2.
489  Adding ... gives a coefficient 2^62+1<2^63. This proves (AM).
~~~

Thus the candidate's \(C_4=2^{62}+1\) is not a downward rounding of the
published fallback \(2^{63}\). It is the exact sharper coefficient later
banked by CR_REDUCTION_REREFEREE.md:358-370, which says:

~~~text
C4'=2^62+1 ... confirmed as paper-level conditional arithmetic/component
results; C4=2^63 ... remains a weaker confirmed fallback.
~~~

The caveat is unchanged: AM_REFEREE.md confirms this only at paper level,
conditional on the accepted Route-B/Ford inputs, and not by machine proof.

### 2.2 Matched pair at the closed endpoint

For positive \(x\le y\), \(s=\sigma+it\), and \(p=2\sigma\),

\[
 \left|\frac{d}{du}u^{-2s}\right|=2|s|u^{-p-1}.
\]

At \(\sigma=3/2\), the same shallow estimate used in
BOUNDARY_ALPHA_THEOREM_SOL.md:457-502 is legal without a limiting argument:

\[
 |x^{-2s}-y^{-2s}|
 \le 2|s|(y-x)x^{-4}
 \le2|s|\delta_qw_Xx^{-3}.
\]

For deep atoms, positivity gives

\[
 |x^{-2s}-y^{-2s}|\le x^{-3}+y^{-3}\le2x^{-3}
 <\frac{2\pi^2}{q^2}w_Xx^{-3}.
\]

After enlarging both positive sub-sums, the source normalization remains

\[
 E_{\rm pair}\le
 \frac{2\pi^2(|s|+1)}{q^2}S_w(3,q).
\]

There is no singular endpoint step here. Absolute convergence follows from
the \(p=3\) moment estimate proved next. The exact matched-plus-wrap identity
being consumed is the paper-level Route-B identity recorded at
M1_ROUTE_B_REPAIR_SOL.md:808-825; this referee does not strengthen that
source's status.

### 2.3 \(M(3/2)\) and Hejhal's closed strip

M3_UNIFORMITY_EXECUTION_SOL.md:255-270 proves for every
\(\Re s>1/2\)

\[
 M(s)=B(s-1/2,1/2),\qquad |M(\sigma+it)|\le M(\sigma).
\]

At the endpoint this gives exactly

\[
 M(3/2)=B(1,1/2)=\int_0^1(1-u)^{-1/2}\,du=2.
\]

The finite-\(q\) whole-coefficient bound also includes the endpoint.
M2_PERTERM_REFEREE.md:110-125 records the precise domain

~~~text
epsilon>0, 1/2<=sigma<=3/2, |t|>=epsilon, N<infinity,
C6(epsilon)=100[epsilon^-1+sqrt(1+epsilon^-2)].
~~~

For the candidate rectangle,
\(t_0-2.38=4.6873625708\ldots>4.68\). Choosing
\(\epsilon=4.68\) rounds the lower threshold **down**, hence rounds the
decreasing \(C_6(\epsilon)\) bound safely **up**. This use is finite-\(q\) and
whole-coefficient, exactly as the source allows. It is not a per-mode bound
and it does not make Hejhal's qualitative “sufficiently large” theorem
effective by itself.

## 3. Tonelli/layer-cake attack, including the \(Y=q\) atom

Because every term is nonnegative and \(x_X\ge1\),

\[
 x_X^{-3}=3\int_{x_X}^{\infty}Y^{-4}\,dY
\]

and Tonelli gives, with no convergence presupposition,

\[
 S_w(3,q)=3\int_1^\infty W_q(Y)Y^{-4}\,dY.
\]

For \(1\le Y\le q\), the atom bound contributes
\(3C_4\int_1^qY^{-1}dY=3C_4\log q\). For \(Y>q\), substitute
\(Y=qu\) in the high-regime bound to obtain

\[
 3C_4\left[
 \int_1^\infty u^{-2}(1+\log u)^2du
 +q^{-1}\int_1^\infty u^{-2}(1+\log u)^4du\right].
\]

Since

\[
 \int_1^\infty u^{-2}(\log u)^jdu=j!,
\]

binomial expansion gives \(5\) and \(65\). A fresh exact check was:

~~~bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from math import comb, factorial
from fractions import Fraction
for j in (2,4):
    print(f'I{j}=sum(C({j},k)k!)=',
          sum(comb(j,k)*factorial(k) for k in range(j+1)))
p=3
print('p*G(3)=',p*(Fraction(1,p-2)+Fraction(1,(p-2)**2)))
atoms=[(5,7),(8,11)]
lhs=sum(Fraction(w,x**p) for x,w in atoms)
rhs=Fraction(7,5**3)-Fraction(7,8**3)+Fraction(18,8**3)
print('atom_at_q_contribution=',Fraction(7,5**3))
print('direct_sum=',lhs)
print('layer_cake=',rhs)
print('equal=',lhs==rhs)
PY
~~~

Output:

~~~text
I2=sum(C(2,k)k!)= 5
I4=sum(C(4,k)k!)= 65
p*G(3)= 6
atom_at_q_contribution= 7/125
direct_sum= 4959/64000
layer_cake= 4959/64000
equal= True
~~~

An atom with \(x_X=q\) is present in \(W_q(Y)\) for every \(Y\ge q\); it is
therefore integrated on the high side. The single split point has Lebesgue
measure zero, so the source's low-regime Y<=q and high-regime Y>q
conventions create neither an omitted atom nor a boundary term. This proves

\[
 S_w(3,q)\le3C_4\left(\log q+5+\frac{65}{q}\right).    \tag{R.3}
\]

For (FW), FW_RENEWAL_COUNT_SOL.md:475-494 expressly says that its own
layer-cake includes a possible atom at \(y=q\), and proves for every \(p>2\)

\[
 E_{\rm wrap}\le pC_1q^{1-p}
 \left((p-2)^{-1}+(p-2)^{-2}\right).
\]

The exact check above gives \(pG(3)=6\), hence
\(E_{\rm wrap}\le6C_1q^{-2}\). FW_REFEREE.md:358-378 confirms this for
each fixed \(\sigma>1\), with its paper-level dependency caveat. Combining
this with the pair bound, (R.3), and \(M(3/2)=2\) gives (R.1), including the
candidate's factor \(12=2\times6\).

## 4. Geometry, adverse rounding, and independent Arb replay

The harmonic-measure series in candidate lines 279--296 is the right-side
harmonic measure for the \(L=1\), \(H=4.76\) rectangle. Its tail estimate is
safe: for \(x\le1/4+1/40\), the hyperbolic-sine quotient is bounded by

\[
 \frac{e^{-n\pi(L-x)/H}}{1-e^{-2\pi L/H}},
\]

and replacing the odd-step tail by an all-integer geometric tail only enlarges
it. Each circle cell carries its own lower \(m_i\) and lower
\(\underline\nu_i\). Since \(0<E_3(q)<K\), replacing \(\nu_i\) by a lower
bound enlarges \(K^{1-\nu_i}E_3(q)^{\nu_i}\), so the comparison direction in
candidate lines 299--311 is correct.

The declared checker was rerun verbatim:

~~~bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python \
  research_notes/rh_goals_2026-08-14/lane_g/law_probes/routeb_endpoint_p3_cover.py
~~~

Selected output:

~~~text
delta= [2.380000000000000000000000000000000000000000000000000000000000000000000 +/- 5.84e-72]
t0= [7.067362570867346895228625991781235135392128557849621587842783730074982 +/- 4.17e-70]
circle_boxes= 8192 harmonic_boxes= 8192 series_nmax= 101
harmonic_tail_upper= [1.748104603018052326184818127852444898645746998909357406784699706716472e-23 +/- 3.37e-93]
min_phi_lower= 0.011688872138620354235172271728515625...
min_nu_lower= [0.2245322055999083002460647051958323866789050537738555497887256757038436 +/- 4.42e-71]
S_vertical_upper= [9.565702250510690346172375979063921459261526021347426145804246663095551 +/- 3.47e-70]
theta_boundary_sup_upper= 1.1143969334661960601806640625... edge= left cell= 3716
C4= 4611686018427387905
M_endpoint= 2.000000000000000000000000000000000000000000000000000000000000000000000
a_upper= [5770840757117238329716.761706657768159026050115058822218160162626309995 +/- 1.65e-49]
b_upper= [2600.674069340075995264868538559759208563968206377352070329364494581853 +/- 3.60e-67]
C6_epsilon_4.68= [123.6248974799147571158881087298810863558621869397994659653859804025225 +/- 1.58e-68]
Kraw_upper= [124.7392944133809531760687727923810863558621869397994659653859804025225 +/- 1.58e-68]
CERT_Kraw_lt_125= True
q= 31951437654668744792
E_endpoint_upper= [2.821320135145467239778340293440376794614361193523623648195483776832223e-16 +/- 3.14e-86]
max_ratio_q_upper= [0.9999999999999999999883692775839494652069751039144774898937695919613894 +/- 2.88e-71] cell= 4136
PASS_all_cells_q= True
q_minus_1= 31951437654668744791
max_ratio_prev_upper= [1.000000000000000000002283784093023924202037770193596600349355895732696 +/- 1.41e-70] cell= 4136
PREV_CERTIFICATE_FAILS= True
endpoint_derivative_bracket_lower= [570283126614840517431175.2860094782328107385926534955348970232304237454 +/- 2.35e-47]
MONOTONE_FOR_q_ge_12= True
~~~

All ceiling quantities are taken with upper(); all nonvanishing and
harmonic-measure quantities are taken with lower(). The exact integer
\(C_4\) is used, \(K=125\) is above the outward \(K_{\rm raw}\), and no
intermediate decimal is rounded toward the desired conclusion.

### 4.1 Precision-instability attack and refined repair

The declared pass is extremely narrow. Changing only ctx.dps from 70 to
100 while retaining the same wide 8192-cell partition produces wider Arb
special-function enclosures and does not certify the displayed \(Q\):

~~~bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY' |
  rg 'circle_boxes|harmonic_boxes|min_phi_lower|Kraw_upper|q=|max_ratio_q_upper|PASS_all_cells_q'
from pathlib import Path
p=Path('research_notes/rh_goals_2026-08-14/lane_g/law_probes/routeb_endpoint_p3_cover.py')
s=p.read_text().replace('ctx.dps = 70','ctx.dps = 100')
exec(compile(s,str(p),'exec'))
PY
~~~

~~~text
circle_boxes= 8192 harmonic_boxes= 8192 series_nmax= 101
min_phi_lower= 0.0116098793805576860904693603515625...
Kraw_upper= [124.8137993774345840049261946673810863...]
max_ratio_q_upper= [1.0083212801844169152147864605667923...] cell= 4151
PASS_all_cells_q= False
~~~

This is not a contradiction: interval evaluations at different working
precision and on wide complex boxes need not be nested. It does show that the
original receipt should not be advertised as precision-stable.

I therefore independently refined both partitions and increased precision to
120 decimal digits, without editing the tracked checker:

~~~bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY' |
  rg 'circle_boxes|harmonic_boxes|min_phi_lower|min_nu_lower|theta_boundary_sup_upper|Kraw_upper|CERT|q=|max_ratio_q_upper|PASS_all_cells_q|q_minus_1|max_ratio_prev_upper|PREV|MONOTONE'
from pathlib import Path
p=Path('research_notes/rh_goals_2026-08-14/lane_g/law_probes/routeb_endpoint_p3_cover.py')
s=p.read_text()
s=s.replace('ctx.dps = 70','ctx.dps = 120')
s=s.replace('N = 8192','N = 32768')
s=s.replace('Nedge = 4096','Nedge = 16384')
exec(compile(s,str(p),'exec'))
PY
~~~

Output:

~~~text
circle_boxes= 32768 harmonic_boxes= 32768 series_nmax= 101
min_phi_lower= 0.01182221228373236954212188720703125...
min_nu_lower= [0.2245322085177197088673426504230291582850926653768437399578583669194447973674...]
theta_boundary_sup_upper= 1.047700940631330013275146484375... edge= left cell= 14952
Kraw_upper= [124.6725984205460871291632552142560863558621869397994659653859804025224940626592...]
CERT_Kraw_lt_125= True
q= 31951437654668744792
max_ratio_q_upper= [0.9872404746757880935258505797664521038695161412529600471604621395398643874862...] cell= 16457
PASS_all_cells_q= True
q_minus_1= 31951437654668744791
max_ratio_prev_upper= [0.9872404746757880935395869888285898540080836434295288592967111644740644879393...] cell= 16457
PREV_CERTIFICATE_FAILS= False
MONOTONE_FOR_q_ge_12= True
~~~

Thus the independent refined cover has \(K_{\rm raw}<125\) by at least
\(0.3274\) (rounded down) and a worst ratio below one by at least \(0.0127\)
(rounded down). It confirms \(Q\) with a material interval margin. It also
confirms the candidate's warning that \(Q\) is **not** a least-onset result:
the refined certificate passes \(Q-1\) too. The original
PREV_CERTIFICATE_FAILS=True means only that the original coarse 70-digit
certificate fails there, exactly as candidate lines 35--39 and 385--388 say.

## 5. Whole-tail monotonicity and integer scope

Let

\[
 H(q)=a(\log q+5+65/q)+b,\qquad E_3(q)=q^{-2}H(q).
\]

Direct differentiation gives

\[
 E_3'(q)=-q^{-3}\left[
 a\left(2\log q+9+\frac{195}{q}\right)+2b\right].
\]

Here \(a,b>0\), and every term in the bracket is positive for \(q\ge12\).
Therefore the symbolic formula, not merely the check at one huge integer,
proves strict decrease on the entire real tail. For each fixed cover cell,
\(K^{1-\nu_i}E_3(q)^{\nu_i}/m_i\) also decreases because
\(\nu_i>0\). The refined all-cell pass at \(Q\) consequently propagates to
every integer \(q\ge Q\).

No minimal integer has been proved. The only defensible integer statement is
the sufficient onset (R.2). The candidate makes precisely that statement and
does not infer failure of the LAW at \(Q-1\).

## 6. Dated receipt correction — 2026-08-19

Candidate line 353 transcribes the live derivative-bracket digits as

~~~text
...478232810738653495534897...
~~~

but the verbatim checker prints

~~~text
...478232810738592653495534897...
~~~

This is a non-load-bearing receipt transcription error. The live outward
lower enclosure is positive by more than \(5.7\times10^{23}\), and the exact
symbolic derivative already proves the sign. This referee records the
correction rather than silently rewriting the candidate.

## 7. Status ledger and blast radius

| Item | Cold ruling |
|---|---|
| \(p=3\) Tonelli identity, including an atom at \(Y=q\) | **CONFIRMED** |
| Endpoint moment (R.3), constants \(5,65\) | **CONFIRMED**, conditional on (AM) |
| Endpoint pair MVT and normalization | **CONFIRMED**, conditional on the matched Route-B identity |
| Endpoint wrap factor \(6C_1q^{-2}\) | **CONFIRMED**, conditional on (FW) |
| \(M(3/2)=2\) and closed \(\sigma=3/2\) Hejhal interface | **CONFIRMED** in their cited paper-level domains |
| Endpoint scattering estimate (R.1) | **CONFIRMED at paper level**, with inherited Route-B/Ford/AM/FW caveats |
| Original 8192-cell, 70-digit receipt | **REPRODUCED**, but numerically brittle |
| Refined 32768-cell, 120-digit cover at \(Q\) | **CONFIRMED** |
| Strict decrease and propagation to all \(q\ge Q\) | **CONFIRMED** |
| \(Q\) is the least possible onset | **NOT CLAIMED / NOT PROVED** |
| Finite block \(3\le q<Q\) | **OPEN** |
| Enlarged-rectangle finite-\(q\) holomorphy/transport hypotheses | **OPEN in this artifact** |
| Full LAW, all gates, and machine formalization | **OPEN; any proof claim remains CONJECTURAL** |

The blast radius is positive but narrow. The endpoint removes the artificial
\(1/(3-p)\) loss and supplies a reproducible finite tail target. It does not
upgrade any finite-\(q\) case below \(Q\), any enlarged-domain holomorphy
claim, the seed-zero isolation needed by a complete Rouché argument, or the
final all-gates LAW. No currently banked claim is refuted.

## 8. Repository hygiene and security triage

This report contains no credentials, network access, executable payload,
dependency change, or production-code change. The mandated pre-commit tools
were run against the report before this receipt-only appendix:

~~~bash
python3 /Users/za/Documents/farey-hecke/.codex/skills/impact-of-change/tools/impact.py \
  --repo . --diff working
python3 /Users/za/Documents/farey-hecke/.codex/skills/security-oversight/tools/security_scan.py \
  --repo . --diff working
git status --short --branch
~~~

Output:

~~~text
# Impact of change (DEGRADED-MODE)
WARNING: impact estimated WITHOUT graph; results are lexical and unverified.
0 symbol(s) changed, 0 affected caller(s), risk = LOW

# Security oversight (lexical-triage)
WARNING: folded in 1 untracked file(s) git diff omits
(research_notes/rh_goals_2026-08-14/lane_g/LAW_EFFECTIVE_TAIL_COVER_REFEREE.md)
521 added line(s) across 1 file(s); 0 finding(s) — risk = NONE
SOUNDNESS LIMIT: absence of a finding is NOT proof of safety.

## codex/law-effective-tail-referee-20260819
?? research_notes/rh_goals_2026-08-14/lane_g/LAW_EFFECTIVE_TAIL_COVER_REFEREE.md
~~~

The impact result is degraded lexical evidence because no graph index exists.
That limitation is immaterial for a new referee Markdown artifact with no
changed code symbol. The clean security triage is only a floor, not proof of
security; the receipt appendix itself adds only the quoted commands and
outputs above.

Final staging check:

~~~bash
git add -- research_notes/rh_goals_2026-08-14/lane_g/LAW_EFFECTIVE_TAIL_COVER_REFEREE.md
git diff --cached --check
git diff --cached --stat
git status --short --branch
~~~

Output:

~~~text
[git diff --cached --check emitted no diagnostics and exited zero]
 .../lane_g/LAW_EFFECTIVE_TAIL_COVER_REFEREE.md | 570 +++++++++++++++++++++
 1 file changed, 570 insertions(+)
## codex/law-effective-tail-referee-20260819
A  research_notes/rh_goals_2026-08-14/lane_g/LAW_EFFECTIVE_TAIL_COVER_REFEREE.md
~~~

READY FOR JUDGING

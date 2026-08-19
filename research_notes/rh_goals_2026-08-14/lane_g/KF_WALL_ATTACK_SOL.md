# Breaking the \(\log K_F\) wall

**Date:** 2026-08-18

**Referee verdict 2026-08-18:** GAPS not REFUTED — both cores (\(K_F<109\)
conditional, \(K_+<117\)) CONFIRMED; see `KF_WALL_REFEREE.md`.

**Lane:** G / R3--R5

**Interpreter:** `/Users/za/.venvs/farey-rh/bin/python` (`python-flint`/Arb)

**Rounding:** margins DOWN, bounds UP
**Status:** the \(K_F\) wall is broken as a **proved conditional transport
constant**.  A new boundary-Harnack/Poisson argument gives

\[
\boxed{K_F<109,\qquad \log K_F<4.692.}
\]

The unconditional pincer onset is nevertheless still **`UNDEFINED`** because
the full-side positive RATE, finite-family holomorphy/divisor, and certified
finite-evaluator gates remain open.

> **[CORRECTION 2026-08-18 kf-referee]** The headline comparison implying a
> roughly \(10^5\)-fold collapse in the transport threshold is not
> like-for-like. Quoting `KF_WALL_REFEREE.md`: "The advertised roughly
> \(10^5\)-fold collapse is also not like-for-like. The old \(4.711\times10^6\)
> threshold is Route B at the sixth-zero geometry; the new \(38.386\)
> threshold is A0 at the first-zero contour. Like-for-like: A0 improves
> \(86.640\to38.386\), a factor about \(2.26\) in \(\log q\); rebuilt Route B
> improves \(4{,}711{,}753.120\to5599.981\), a factor about \(841\). This
> cross-route headline is rhetorically misleading, but it does not falsify
> either conditional implication."

## 0. Verdict

Two premise corrections are necessary.

1. The statement that the confirmed \(C_6\) is a *per-term* Theorem-12.9
   constant is **FALSE**.  Its correction is better for this task: the
   confirmed
   \[
   C_6(\varepsilon)=100\{\varepsilon^{-1}+
          \sqrt{1+\varepsilon^{-2}}\}
   \]
   is Lemma 7.7's **whole finite-\(q\) scattering-coefficient bound**.  The
   Theorem-12.9(c),(d) per-mode constants, the covering number
   \(k_q(\eta)\), and their family uniformity remain **OPEN**.  Transport needs
   the whole-scattering bound, so the open per-mode constants are avoidable.
2. The statement that \(\log K_F\) is the *last* Route-B obstruction is
   **FALSE**.  The wall can indeed be reduced from \(5259\) to \(<4.692\), but
   the remaining exponent
   \[
   c_0=0.01288\cdot0.06737=0.0008677256
   \]
   still forces \(\log q>5599.981+(5/6)\log C_R\).  Even the impossible ideal
   base zero would leave \(\log q>1098.484\).  Route B's double propagation is
   the corrected structural bottleneck.

The strongest results of this attack are:

| route | new proved constant/result | conditional \(\alpha=1.2\) transport onset |
|---|---:|---:|
| A0 | \(K_+<117\) | \(\log q>38.386+\frac56\log C_R\) |
| direct rebuild of 7.9/7.10 | \(K_F<109\), \(\log K_F<4.692\) | Route B: \(\log q>5599.981+\frac56\log C_R\) |
| finite hybrid today | \(E_R^A<8.4082242\), \(E_R^B<8.2283134\), but only \(\alpha=0\) | no finite onset |

Thus A0 is decisively best.  Its formerly conjectural side supremum is now
proved; what blocks a certified \(q_0\) is no longer \(K_+\), but the full-side
RATE and holomorphy/divisor gates.

## 1. Receipts before claims

### 1.1 Required-source state

All six requested notes were read in full.  Their source state was:

```text
$ shasum -a 256 research_notes/rh_goals_2026-08-14/lane_g/{C0_TRANSPORT_CAMPAIGN_SOL,R3_TRANSPORT_EXECUTION_SOL,R3_ROUTE_B_TRANSPORT_SOL,LAW_HEJHAL_S7_EXTRACT,M2_PERTERM_TRANSCRIPTION_SOL,R3_BOUNDARY_RATE_CAMPAIGN_SOL}.md
91e26f6cd1928a35a6420e319fd2fc7a9ad3911bc6dd5be372ff7bd09a15fd21  research_notes/rh_goals_2026-08-14/lane_g/C0_TRANSPORT_CAMPAIGN_SOL.md
a6b6a1297fc4401e47e194a809064baa5cade1f9effb29fe28e3bde47d3b6345  research_notes/rh_goals_2026-08-14/lane_g/R3_TRANSPORT_EXECUTION_SOL.md
320c21a8d0558418531f23c1ecffd3e489c5c1ff12180ce29c8f9f90d9177468  research_notes/rh_goals_2026-08-14/lane_g/R3_ROUTE_B_TRANSPORT_SOL.md
c65eec51a9131651c81484326932a96615e095cb0ae00d9ed142cc3ede377503  research_notes/rh_goals_2026-08-14/lane_g/LAW_HEJHAL_S7_EXTRACT.md
40c311ae85035b0ae359f50729f3d4e86a045f707b689e2afb01a75dbc4b9f8c  research_notes/rh_goals_2026-08-14/lane_g/M2_PERTERM_TRANSCRIPTION_SOL.md
8567dfaa4fea82aa8f0cddb53df0371bdcc5e1697d2367952a99c46171f6041d  research_notes/rh_goals_2026-08-14/lane_g/R3_BOUNDARY_RATE_CAMPAIGN_SOL.md
```

The decisive source distinction is
`M2_PERTERM_TRANSCRIPTION_SOL.md:186-207,609-622,683-719`:

```text
Lemma 7.7 ... is the whole coefficient phi_N(s), not a Fourier/per-term phi_m.
C6(epsilon) = 100 [epsilon^{-1} + sqrt(1+epsilon^{-2})].
...
This whole-coefficient bound is explicit for every finite N ...
...
The full Theorem 12.9 per-mode certificate and its N-uniformity remain OPEN.
```

No claim below substitutes Proposition 12.4's conjectural common
\(y_0=1000\), or the uninstantiated Theorem-12.9 per-mode prefactor, for this
confirmed finite-\(q\) Lemma-7.7 bound.

## 2. Route 1 — A0 promotion

### 2.1 Numeric feasibility first

A0 uses

\[
t_0=\gamma_1/2,\qquad
\Omega=\{1/2<\sigma<1.1,\ |t-t_0|<1/2\},
\]

and the already certified

\[
m_z>0.0439,\qquad \nu_z>0.1552.
\]

Every non-RATE side satisfies \(|t|>6.5673\), so take the rational
\(\varepsilon=13/2\).  The existing full boundary cover in
`R3_ROUTE_B_TRANSPORT_SOL.md`, Receipt B, proves
\(|\phi_\infty|<0.3825\) on the same rectangle.  Fresh adverse arithmetic is:

```text
$ /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import arb, ctx
ctx.dps=100
eps=arb(13)/2
C6=100*(1/eps+(1+1/eps**2).sqrt())
Kraw=C6+arb('.3825'); K=arb(117)
nu=arb('.1552'); m=arb('.0439'); alpha=arb('1.2')
T=((1-nu)*K.log()-m.log())/(alpha*nu)
ecrit=(m/K**(1-nu))**(1/nu)
E=arb('8.408224199432881')
lhs=K**(1-nu)*E**nu
print('C6_eps_13_over_2_upper=',C6.upper())
print('Kplus_raw_upper=',Kraw.upper())
print('CERT_Kplus_lt_117=',bool(Kraw<117))
print('A0_logq_CR1_upper=',T.upper())
print('A0_ER_required_threshold_lower=',ecrit.lower())
print('finite_A0_contour_upper=',lhs.upper())
print('finite_A0_margin_ratio_upper=',(lhs/m).upper())
PY
C6_eps_13_over_2_upper=116.5611264458915803074037476394545629238392997902260439...
Kplus_raw_upper=116.9436264458915803074037476394545629238392997902260439...
CERT_Kplus_lt_117=True
A0_logq_CR1_upper=38.3855535814978294420003556267900758051983773340406350...
A0_ER_required_threshold_lower=9.8909743063791105487717761482346864096879428134593e-21...
finite_A0_contour_upper=77.7530655363893764233339974978705140580227286332498801...
finite_A0_margin_ratio_upper=1771.1404450202591440394988040517201379959619278644619...
```

Thus the current \(E_R^A<8.4082242\) certificate does not pass A0: the
resulting certified contour upper bound is \(77.754\), not \(<0.0439\).
This is a failure of the available upper certificate, not a lower bound on
the true contour error.

### 2.2 Strongest honest A0 theorem

> **Theorem A0-117 (proved conditional implication).**  For every finite
> \(q\) for which \(F_q=\phi_q-\phi_\infty\) is holomorphic on
> \(\overline\Omega\),
> \[
> |F_q|<117
> \quad\text{on the three non-RATE sides of }\partial\Omega.
> \]
> If additionally \(E_R(q)\le117\), then
> \[
> \sup_{\partial D_z}|F_q|
> \le117^{,1-0.1552}E_R(q)^{0.1552}.
> \]
> Hence
> \(117^{1-0.1552}E_R(q)^{0.1552}<0.0439\) gives an A0 zero and,
> by (7.22), its reflected pole.

If the **CONJECTURAL / OPEN** full-side RATE is inserted as

\[
E_R(q)\le C_Rq^{-1.2},
\]

then a sufficient strict condition is

\[
\boxed{\log q>38.386+\frac56\log C_R.}                 \tag{A0}
\]

For the diagnostic \(C_R=1\), fresh Arb exponentiation gives

```text
logq_upper=38.385553581497829442000355626790075805...
q_upper=46841857142466893.055819411584407187987...
strict_integer_floor_plus_1=46841857142466894
```

This improves the prior conjectural \(86.640+(5/6)\log C_R\) by proving a
much smaller \(K_+\).  It does **not** prove the RATE, its onset
\(q_{\rm RATE}\), or closed-rectangle holomorphy/no-poles
\(q_{\rm divisor}\).  Those are now the exact A0 blockers.

## 3. Route 2 — direct maximum-principle rebuild

### 3.1 Numeric feasibility first

Merely replacing \(242\) by the smaller high-height \(C_6\) inside the old
7.9/7.10 chain does not break the wall.  Even using \(C_6=117\) with the
improved \(C_7=5.286\) and \(r_0=3/4\) gives

```text
routeB_C6_117_Lanchor_upper=8.00086988711526336755330657597268499...
routeB_C6_117_A_upper=47.05477215808903827973075647600198288...
routeB_C6_117_logKH_upper=4792.95973441456765653202050328087494520...
```

The geometric area/submean multiplier, not \(C_6\), still produces thousands.
The replacement below instead controls the positive harmonic function
\(\log(C/|\phi_q|)\) directly.

At the relocated sixth-zero rectangle,

\[
t_c=t_6-0.050005,\qquad \delta=0.9999,
\]

the whole rectangle lies above height \(17\).  With \(C=107\), the direct
constant arithmetic is:

```text
$ /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import acb, arb, ctx
ctx.dps=100
t6=(acb.zeta_zero(6)/2).imag; tc=t6-arb('0.050005'); delta=arb('0.9999')
C6=100*(1/arb(17)+(1+1/arb(17)**2).sqrt())
C=arb(107); H=arb('.356'); m=arb('.07843')
L=(2*C/m).log(); leftlog=H*L
print('tc_minus_delta_lower=',(tc-delta).lower())
print('CERT_tc_minus_delta_gt_17=',bool(tc-delta>17))
print('C6_eps17_upper=',C6.upper())
print('CERT_C6_lt_107=',bool(C6<C))
print('Lanchor_upper=',L.upper())
print('H_Lanchor_upper=',leftlog.upper())
print('reflected_phi_upper=',leftlog.exp().upper())
print('logKF_109_upper=',arb(109).log().upper())
PY
tc_minus_delta_lower=17.7431840794128356286088817403526664107027986754153966...
CERT_tc_minus_delta_gt_17=True
C6_eps17_upper=106.0552139172141245066665989639842512140571481822260095...
CERT_C6_lt_107=True
Lanchor_upper=7.9115247867794134220137274775855919789301277543770827...
H_Lanchor_upper=2.8165028240934711782368869820204707444991254805582414...
reflected_phi_upper=16.7182815471410958579336618342237166633593205666800793...
logKF_109_upper=4.6913478822291437003773164522092016510603488835032311...
```

### 3.2 Why ordinary three-lines on \(F_q\) is insufficient

On a rectangle \(1/2<\sigma<\sigma_R\), the two-constants/three-lines bound
has the form

\[
|F_q(1/2+h+it)|
 \le K^{1-h/L}E_R(q)^{h/L},\qquad L=\sigma_R-1/2.
\]

At the critical line \(h=0\), the RATE exponent is exactly zero.  Thus this
argument returns only \(|F_q|\le K\), no matter how small \(E_R(q)\) becomes.
This is not a removable rounding loss.  It also agrees with the exact
negation of critical-line convergence:

\[
|\phi_q(1/2+it)|=1,qquad
|F_q(1/2+it)|\ge1-|\phi_\infty(1/2+it)|.
\]

The corrected direct argument does not claim critical-line convergence.  It
uses zero-freeness, unitarity, and a boundary-Harnack estimate to bound the
reflected outer disc, after which Route B's second propagation supplies the
contradiction.

### 3.3 Boundary-Harnack replacement for Lemmas 7.9/7.10

Normalize the full zero-free rectangle by

\[
s=\frac12+\delta x+i(t_c+\delta y),\qquad
A=(0,1)\times(-1,1).
\]

The anchor is \(a=(1/2,0)\), and the right half of \(D_0\) is

\[
T_\kappa=\{x\ge0:x^2+y^2\le\kappa^2\},
\qquad \kappa=3/40=0.075.
\]

Assume the contradiction hypothesis \(H_0\), closed-rectangle holomorphy,
and no poles.  Lemma 7.7 with \(\varepsilon=17\) gives
\(0<|\phi_q|<C=107\) on the right rectangle.  Put

> **[CORRECTION 2026-08-18 kf-referee]** Old text did not define which
> inherited \(H_0\) is meant. Quoting `KF_WALL_REFEREE.md`: "the note does
> not define which inherited \(H_0\) is meant. The proof needs the **full**
> width \(1/2\le\sigma\le1/2+\delta=1.4999\), whereas the old Route-B note
> literally defines a narrower \(H_0\) at `R3_ROUTE_B_TRANSPORT_SOL.md:91-120`.
> The assembly plan and Hejhal's theorem do use the full \(R_\delta\)
> (`R3_R5_ASSEMBLY_PLAN_SOL.md:60-69`; `LAW_HEJHAL_S7_EXTRACT.md:43-47,67-76`),
> so this is a repairable statement gap, not a failure of the rebuilt
> argument. Importing the old narrow \(H_0\) literally would invalidate the
> harmonicity step." \(H_0\) here must therefore be read as: \(\phi_q\)
> nonvanishing and holomorphic on the **full** closed Hejhal rectangle
> \(1/2\le\sigma\le1/2+\delta=1.4999\), \(|t-t_c|\le\delta\) — not the
> narrower Route-B \(H_0\).

\[
u=\log\frac{C}{|\phi_q|}\ge0,qquad c=\log C.
\]

On the left side, unitarity gives \(u=c\).  If \(\omega_L\) is harmonic
measure of that side, then

\[
v=u-c\omega_L
\]

is nonnegative harmonic, has zero data on the left, and nonnegative data on
the other three sides.  For their Poisson kernels \(P_j\), the following
certified ratio is the new input:

\[
\sup_{z\in T_\kappa}
\sup_{\xi\in\Gamma_j}\frac{P_j(z,\xi)}{P_j(a,\xi)}<0.356.
                                                               \tag{BH}
\]

For the top/bottom and right Fourier kernels the boundary sine was factored
as

\[
\sin(n\alpha)=\sin\alpha\,U_{n-1}(\cos\alpha),
\]

so the vanishing corner factors cancel before interval division.  This is
essential: an unfactored endpoint box would contain a zero denominator.  The
tails use \(|U_{n-1}(x)|\le n\) for \(|x|\le1\).  The completed Arb cover was:

```text
$ /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import arb, ctx
ctx.dps=60
pi=arb.pi(); kap=arb('0.075')
def tail_sum(N,r,den):
    n=arb(N)
    return r**(N+1)*((N+1)-n*r)/(1-r)**2/den
def Uvals(c,N):
    out=[arb(1)]
    if N>1: out.append(2*c)
    for k in range(2,N): out.append(2*c*out[-1]-out[-2])
    return out
def data(kind,N):
    if kind=='right':
        den=1-(-pi).exp(); rt=(-pi*(1-kap)/2).exp(); ra=(-pi/4).exp()
    else:
        den=1-(-4*pi).exp(); rt=(-pi*(1-kap)).exp(); ra=(-pi).exp()
    return tail_sum(N,rt,den),tail_sum(N,ra,den)
def anchor_min(kind,N,cells=4096):
    _,tail=data(kind,N); best=None
    for j in range(cells):
        a=arb(pi*(arb(j)+arb('.5'))/cells,pi/(2*cells))
        U=Uvals(a.cos(),N); s=arb(0)
        for n in range(1,N+1):
            z=arb(n)
            if kind=='right':
                b=(z*pi/2).sin()*(z*pi/4).sinh()/(z*pi/2).sinh()
            else:
                b=(z*pi/2).sin()*(z*pi).sinh()/(2*z*pi).sinh()
            s += b*U[n-1]
        lo=s.lower()-tail.upper()
        if best is None or lo<best: best=lo
    return best,tail
def numerator_max(kind,N,cells=256):
    tail,_=data(kind,N); Us=[]
    for j in range(cells):
        a=arb(pi*(arb(j)+arb('.5'))/cells,pi/(2*cells))
        Us.append(Uvals(a.cos(),N))
    best=None; where=None
    for i in range(cells):
        th=arb(-pi/2+pi*(arb(i)+arb('.5'))/cells,pi/(2*cells))
        x=kap*th.cos(); Y=1+kap*th.sin(); coeff=[]
        for n in range(1,N+1):
            z=arb(n)
            if kind=='right':
                b=(z*pi*Y/2).sin()*(z*pi*x/2).sinh()/(z*pi/2).sinh()
            else:
                b=(z*pi*x).sin()*(z*pi*Y).sinh()/(2*z*pi).sinh()
            coeff.append(b)
        for j,U in enumerate(Us):
            s=sum((coeff[k]*U[k] for k in range(N)),arb(0))
            up=s.upper()+tail.upper()
            if best is None or best<up: best=up; where=(i,j)
    return best,tail,where
for kind,N in [('right',41),('top',31)]:
    den,atail=anchor_min(kind,N)
    num,ttail,where=numerator_max(kind,N)
    print(kind,'target_tail_upper=',ttail.upper())
    print(kind,'anchor_tail_upper=',atail.upper())
    print(kind,'anchor_factored_den_lower=',den)
    print(kind,'factored_num_upper=',num,'where=',where)
    print(kind,'CERT_GLOBAL_RATIO_UPPER=',num/den)
PY
right target_tail_upper=1.8124533610309091674930692165592535719e-25...
right anchor_tail_upper=3.8852108821797463839343169773530993001e-13...
right anchor_factored_den_lower=0.16384417909602939212118341047691171182...
right factored_num_upper=0.05831631225945842481648954617052637528... where=(128,128)
right CERT_GLOBAL_RATIO_UPPER=0.35592544441434883535848760428346649302...
top target_tail_upper=1.3958034343691459698328536281195920276e-39...
top anchor_tail_upper=7.3266570646900110733408669286792148495e-43...
top anchor_factored_den_lower=0.04289202215633439903963654854295800878...
top factored_num_upper=0.01244129607428639779288510539052153160... where=(150,0)
top CERT_GLOBAL_RATIO_UPPER=0.29006084229230112602729281147182502502...
```

An independent post-write rerun exposed the outward endpoints and the strict
comparison explicitly:

```text
H_right_upper=[0.355925444414348835358487604283466493014668683069797873324459 +/- 3.29e-61]
H_top_bottom_upper=[0.290060842292301126027292811471825025017970766128948044346170 +/- 2.74e-61]
CERT_H_lt_0.356=True
POST_WRITE_ARB_GATE=PASS
```

Bottom is covered by the \(y\mapsto-y\) symmetry and the full semicircle
cover.  For fixed boundary point the Poisson kernel is harmonic in the target;
on the diameter \(x=0\) it vanishes, so covering the semicircle covers all of
\(T_\kappa\).  Poisson representation and (BH) give

\[
v(z)\le0.356\,v(a)\le0.356\,u(a).
\]

Once the first-stage anchor is active,

\[
|\phi_q(a)|>m_a/2,qquad m_a=0.07843,
\]

so

\[
u(a)<L_a:=\log(2\cdot107/0.07843)<7.911525.
\]

Consequently \(u(z)<c+0.356L_a\) on the right half of \(D_0\).  Reflection
then gives on its left half

\[
\log|\phi_q(1/2-h+it)|
=-\log|\phi_q(1/2+h+it)|
\le0.356L_a<2.816503,
\]

hence \(|\phi_q|<16.719\) there.  On the right half Lemma 7.7 gives
\(|\phi_q|<107\).  The existing theta square cover gives
\(|\phi_\infty|<2\) throughout \(D_0\).  Therefore

\[
\boxed{\sup_{D_0}|F_q|<109=:K_F,qquad \log K_F<4.692.}       \tag{KF}
\]

> **[CORRECTION 2026-08-18 kf-referee]** Old text alternated between a raw
> strict bound and a chosen ledger constant. Quoting `KF_WALL_REFEREE.md`:
> "The note alternates between a raw strict bound and a chosen ledger
> constant: `KF_WALL_ATTACK_SOL.md:440-442` writes both
> \(\sup|F_q|<109\) and \(109=:K_F\), while the headline says \(K_F<109\).
> The correct formulation is either 'the raw supremum is \(<109\)' or 'take
> the safe constant \(K_F=109\).'" Read the boxed line above as: the raw
> supremum satisfies \(\sup_{D_0}|F_q|<109\); take the safe constant
> \(K_F=109\), so \(\log K_F=\log109<4.692\) (not the strict inequality
> \(K_F<109\)).

This is a maximum-principle replacement of Lemmas 7.9/7.10.  It uses neither
\(C_7\), their area integral, nor a Cauchy/submean coefficient.

### 3.4 Strongest honest rebuilt Route-B theorem

The same \(C_6(17)<107\) and the certified
\(|\phi_\infty|<1.048\) on the first propagation rectangle give the safe
non-RATE-side bound \(K<109\).  Therefore the C0 geometry yields

\[
E_3(q)
 <109^{1-0.06737}\,
   109^{0.06737(1-0.01288)}E_R(q)^{0.0008677256}.
\]

Equivalently,

\[
\boxed{
\log E_3(q)<4.687278+0.0008677256\log C_R
 -1.2(0.0008677256)\log q.}                              \tag{B-new}
\]

Fresh threshold receipt:

```text
safe_c0=0.0008677256000000000000000000000000000000...
routeB_direct_base_upper=4.68727707957322768732242032506431855023...
routeB_direct_logq_CR1_upper=5599.98072458948676591556126523592642128...
routeB_anchor_activation_logq_CR1_upper=4.37170867223036160838089659973744122...
ideal_routeB_logq_if_base_zero_CR1_upper=1098.48366955539564375050093869153021447...
```

Thus the new strict conditional contradiction threshold is

\[
\boxed{\log q>5599.981+\frac56\log C_R.}                 \tag{B}
\]

The anchor activation is subordinate.  Formula (B) is proved as an
implication under the same full-side RATE, \(H_0\), holomorphy/no-pole, and
reflection gates as Route B.  Since the RATE and divisor gates are open, it is
not an unconditional onset.

## 4. Route 3 — finite-verification hybrid

### 4.1 Numeric feasibility first

The certified campaign currently provides, for every \(12\le q\le48\),

\[
E_R^A(q)<8.408224199432881,
\qquad E_R^B(q)<8.228313336614521.
\]

Insertion into the new bounds gives:

```text
A0: certified contour upper = 77.7530655363893764...
A0: margin                  = 0.0439
Route B: certified log E3 upper = 4.68910588160682817...
Route B: log defect             = -1.14381888150618890...
```

Neither certificate passes.  More importantly, the same Ford majorant is
used for every \(q\), so the only proved exponent is \(\alpha=0\).  These
enclosures cannot supply an asymptotic tail.

Under the **CONJECTURAL diagnostic** \(C_R=1,\alpha=1.2\), A0's new analytic
tail would begin only at

\[
q_{\rm tail}=46{,}841{,}857{,}142{,}466{,}894.
\]

Thus the finite half would require certification through roughly
\(4.68\times10^{16}\), not through \(48\).  This is not a moderate hybrid.
Route B's \(\log q>5599.981\) tail is vastly worse.

### 4.2 What the existing computation does and does not prove

The \(E_R<8.41\) enclosures are genuine Arb/Ford upper bounds for the full
right sides.  They do **not** enclose a narrow, computed value of the true
\(\phi_q\): the current transfer-operator lineage omits the Fredholm
dimension tail, and its branch integration uses floating arithmetic.  Hence
the statement that its returned narrow `selberg_Z` ball contains the true
determinant is **FALSE**.  The corrected current use is a coarse Ford envelope
and falsification check only.

> **Finite-hybrid theorem (current).**  No \(q\in[12,48]\) is certified by the
> present A0 or Route-B transported upper bounds.  No positive RATE exponent is
> proved.  Therefore today's boundary machinery supplies neither a certified
> finite block nor an analytic tail onset.

A finite block becomes certifiable only after all of the following are
provided:

1. a true interval meromorphic-continuation evaluator for each finite \(q\),
   with either a proved Fredholm dimension-tail theorem or a complete exact
   double-coset head plus Ford remainder;
2. interval branch continuation and interval derivative/Taylor variation on
   every adaptive contour box;
3. denominator and pole clearance on every box, with failures labelled
   **`UNVERIFIABLE`**;
4. closed-domain divisor/holomorphy accounting and compatibility with (7.22);
5. either a Rouché certificate
   \(\sup_\Gamma|\phi_q-\phi_\infty|<
     \inf_\Gamma|\phi_\infty|\), or preferably a direct interval winding of
   \(\phi_q(\Gamma)\) with no boundary zero and an integer zero-minus-pole
   count;
6. every finite \(q\) below the eventual analytic onset, unless a separate
   monotonic or covering theorem reduces the block.

## 5. Best achievable \(\log q_0\)

### 5.1 Proved-only constants

The A0 side constant \(K_+<117\), the direct rebuilt \(K_F<109\), the contour
margins, harmonic measures, and the finite \(q=12,\ldots,48\) Ford envelopes
are proved.  But the only proved boundary exponent is \(\alpha=0\).
Consequently

\[
\boxed{q_0=\texttt{UNDEFINED};\qquad \log q_0=\texttt{UNDEFINED}.}
\]

Writing \(+\infty\) would incorrectly turn a missing theorem into a proved
asymptotic statement.

### 5.2 With the CONJECTURAL diagnostics

Assume the missing full-side RATE with \(\alpha=1.2\), explicit \(C_R\), and
its onset, and assume the finite-family holomorphy/divisor gate.  The best
transport contribution is A0:

\[
\boxed{\log q_{\rm transport}>38.386+\frac56\log C_R.}
\]

For \(C_R=1\) this is the diagnostic integer
\(q_{\rm transport}=46{,}841{,}857{,}142{,}466{,}894\).  For comparison, the
new Route-B contribution is

\[
\log q_{\rm transport}>5599.981+\frac56\log C_R.
\]

> **[CORRECTION 2026-08-18 kf-referee]** The displayed three-decimal
> thresholds and integers above do not chain consistently to the rounded
> displays. Quoting `KF_WALL_REFEREE.md`: "The displayed three-decimal
> thresholds are safe when derived from the full-precision receipts, but
> they do not chain consistently to every subsequently printed rounded
> number. In particular, the listed A0 integer does **not** satisfy the
> boxed condition \(\log q>38.386\); it satisfies the unrounded condition
> \(\log q>38.38555358\ldots\). The Route-B threshold \(5599.981\) likewise
> uses the unrounded base, not the displayed \(4.687278\)." Concretely:
> \(\lfloor e^{38.38555358\ldots}\rfloor+1=46{,}841{,}857{,}142{,}466{,}894\)
> is valid for the exact (unrounded) A0 threshold \(\log q>38.38555358\ldots\)
> but does **not** satisfy the rounded boxed condition \(\log q>38.386\)
> (the correct integer for that rounded condition is
> \(46{,}862{,}772{,}882{,}410{,}612\)). Likewise \(5599.981\) is safe only
> from the full-precision base \(4.68727707957322768732\ldots\), not from
> the rounded displayed base \(4.687278\) (chaining from \(4.687278\) alone
> requires \(5599.982\)). The safe statement is: the unrounded thresholds
> \(\log q>38.38555358\ldots\) and \(\log q>5599.98072458\ldots\) hold; the
> rounded three-decimal displays \(38.386\) and \(5599.981\) hold only when
> derived from full-precision receipts, not by chaining previously rounded
> displayed numbers.

The complete onset would still be

\[
q_0=\max\{12,q_{\rm RATE},q_{\rm divisor},q_{\rm transport},
                 q_{\rm monotone}\}.
\]

Because \(q_{\rm RATE},q_{\rm divisor},q_{\rm monotone}\), and \(C_R\) are
not presently certified, even the `+CONJECTURAL diagnostics` row is a
transport ledger, not a current \(q_0\).

## 6. Final claim ledger

| claim | status |
|---|---|
| Lemma-7.7 \(C_6(\varepsilon)\) is whole-scattering and finite-\(q\) uniform | **CONFIRMED SOURCE TRANSCRIPTION** |
| the same \(C_6\) is Theorem-12.9's per-term constant | **FALSE**; per-term prefactor remains open |
| A0 non-RATE-side \(K_+<117\) | **PROVED** from \(C_6(13/2)\) plus certified theta boundary cover |
| A0 transport exponent floor \(0.1552\), margin \(0.0439\) | **ARB-CERTIFIED in source note** |
| boundary-Harnack Poisson ratio \(H<0.356\) | **ARB-CERTIFIED full parameter cover + explicit tails** |
| direct rebuilt \(K_F<109\), \(\log K_F<4.692\) | **PROVED conditional implication** under \(H_0\), anchor activation, holomorphy/reflection |
| direct rebuilt Route-B threshold \(5599.981+(5/6)\log C_R\) | **PROVED conditional on RATE and divisor gates** |
| “\(\log K_F\) was the last Route-B obstacle” | **FALSE**; \(c_0\) is now dominant |
| A0 threshold \(38.386+(5/6)\log C_R\) | **PROVED conditional on RATE and divisor gates** |
| \(E_R^A<8.4082242,E_R^B<8.2283134\) for \(12\le q\le48\) | **RIGOROUS ARB/FORD ENCLOSURES** |
| those enclosures prove a positive RATE or a finite zero/pole block | **FALSE** |
| full target-side RATE, \(C_R,q_{\rm RATE}\) | **OPEN / CONJECTURAL** |
| finite-family holomorphy/divisor and monotonicity thresholds | **OPEN / CONJECTURAL** |
| certified true-\(\phi_q\) finite evaluator and winding block | **OPEN** |
| unconditional effective \(q_0\) | **`UNDEFINED`** |

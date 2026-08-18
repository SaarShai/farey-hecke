# R3 strip transport, Route B: quantitative Hejhal contradiction

**Date:** 2026-08-18.  **Verdict:** the runner-up mechanism can be made fully
explicit *conditional on the target-height right-boundary RATE input*.  The
transport itself is no longer hiding a Vitali, Phragmen--Lindelof, (C_7), or
harmonic-measure constant.  The present repository still does **not** prove

\[
 E_R(q):=\sup_{s\in\Gamma_R}|\phi_q(s)-\phi_\infty(s)|
 \le C_Rq^{-\alpha}
\]

on the required boundary near the exact contradiction height.  Consequently
the current analytic threshold is **`UNDEFINED`**, not a large numerical
(q_0).  All implications below that consume (C_R,\alpha,q_{\rm RATE}) are
marked **`CONDITIONAL`**.

This file is independent of the sibling route.  No sibling output, log, or
handoff was read.

## 1. Route selection and the target-height correction

Section 2 of `R3_R5_ASSEMBLY_PLAN_SOL.md` ranks Candidate A0, the direct
right-half Rouché transport, first.  Its runner-up is Candidate A, the
quantitative version of Hejhal's zero-free contradiction.  That is the route
executed here.  Candidate C, the Blaschke/
\(\omega_q\)/Harnack construction, ranks later and is not silently substituted
for Candidate A.

The exact height is

\[
 t_0=\gamma_1/2
   =7.067362570867346895228625991781\ldots .
\]

Thus (7.0665) is the old rate-sweep height (t_{\rm meas}), not the exact
contradiction height; the offset is

\[
 t_0-t_{\rm meas}=0.0008625708673468952286\ldots .
\]

**Receipt T0 (Arb; intervals printed outwards).**

```text
$ /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import acb, arb, ctx
ctx.dps=100
t0=(acb.zeta_zero(1)/2).imag
print('t0_lower=',t0.lower())
print('t0_upper=',t0.upper())
print('t0_minus_7.0665_lower=',(t0-arb('7.0665')).lower())
print('t0_minus_7.0665_upper=',(t0-arb('7.0665')).upper())
PY
t0_lower= [7.067362570867346895228625991781235135392128557849621587842783730074981714904628382474505196585780506 +/- 2.43e-100]
t0_upper= [7.067362570867346895228625991781235135392128557849621587842783730074981714904628382474505196585780506 +/- 4.72e-100]
t0_minus_7.0665_lower= [0.0008625708673468952286259917812351353921285578496215878427837300749817149046283824745051965857805062999 +/- 3.50e-104]
t0_minus_7.0665_upper= [0.0008625708673468952286259917812351353921285578496215878427837300749817149046283824745051965857805064563 +/- 4.16e-104]
```

The theta entry is the printed Ch. 11, (3.1), ((\infty,\infty))-entry

\[
 \phi_\infty(s)=
 \frac{\sqrt\pi\,\Gamma(s-\tfrac12)\zeta(2s-1)}
      {\Gamma(s)\zeta(2s)(4^s-1)}.                         \tag{1.1}
\]

It is one entry of a two-cusp scattering matrix.  It is not a scalar unitary
scattering determinant.  For every finite one-cusp Hecke group,

\[
 |\phi_q(\tfrac12+it)|=1,\qquad
 |\phi_q-\phi_\infty|\ge 1-|\phi_\infty|.                 \tag{1.2}
\]

Therefore unconditional convergence of this scalar entry to
\(\phi_\infty\) on the critical line is **FALSE**.  Candidate A uses a bound
there only under the zero-free assumption that it will contradict.

## 2. Fixed geometry

Take the Hejhal scale

\[
 d=\frac14,qquad \sigma_R=\frac{11}{10},qquad
 z_c=\frac12+it_0.
\]

Define

\[
 \begin{aligned}
 R^+&=[\tfrac12,\tfrac34]\times[t_0-d,t_0+d],\\
 P&=(\tfrac12,\sigma_R)\times(t_0-d,t_0+d),\\
 D_0&=D(z_c,d/15)=D(z_c,1/60),\\
 I_1&=\{\tfrac12+it:|t-t_0|\le d/20=1/80\},\\
 D_+&=D(z_c+a,r),\qquad a=1/400,\quad r=1/2000.
 \end{aligned}                                             \tag{2.1}
\]

The inclusions are exact:

```text
a-r = 1/500 > 0,
a+r = 3/1000 < 1/60,
```

so \(\overline D_+\subset D_0\cap\{\Re s>1/2\}\).

The contradiction hypothesis is

\[
 H_0(q):\quad \phi_q\ne0\quad\hbox{on the closed rectangle }R^+.
                                                               \tag{2.2}
\]

A boundary zero already proves the desired alternative, so under (H_0) all
subsequent divisions and the reflection step are legitimate.  Hejhal (7.22)
then continues \(\phi_q\) across the line and gives

\[
 \phi_q(\tfrac12-h+it)\,
 \overline{\phi_q(\tfrac12+h+it)}=1.                         \tag{2.3}
\]

The direct Arb boxes used below also certify that no denominator interval in
(1.1) meets zero on the theta rectangles/discs actually used.

## 3. A-priori, Ford, Roelcke, and zero-count inputs

### 3.1 Ch. 6, Proposition 12.4 and Theorem 12.9

Ch. 6, (12.1), sets \(B_H=5+y_0\), (y_0\ge1000).  Proposition
12.4 gives

\[
 |\phi(s)|\le(1+\sqrt2)B_H^2
 \quad(1/2\le\Re s\le3/2,\ |\Im s|\ge1).                  \tag{3.1}
\]

At (y_0=1000), the raw upper bound is

\[
 K_{12.4}<2{,}438{,}417.                                  \tag{3.2}
\]

Hejhal's Lemma 7.7 explicitly says to repeat the same Ch. 6 derivation with
(B=10) for finite (q).  Hence, on the present finite-(q) strip,

\[
 C_6\le100(1+\sqrt2)<242.                                 \tag{3.3}
\]

Thus (3.2) is the conservative Ch. 6 ledger value, while (3.3) is the sharper
finite-family constant actually consumed below.

Theorem 12.9 has the source-supported structure

\[
 \begin{aligned}
 1-|\phi(s)|^2&=O((\sigma-\tfrac12)\omega_q(t)),\\
 \phi_m(s)&=O(\sqrt{\omega_q(t)}e^{3|t|+5\pi|m|/\eta_H}),\\
 E(z;s;\chi)&=y^s+\phi(s)y^{1-s}
        +O(\sqrt{\omega_q(t)}e^{3|t|-2\pi y}),
 \end{aligned}                                             \tag{3.4}
\]

away from its stated divisor discs.  Its hidden constants depend on
\(\Gamma,\chi,\mathcal F,\delta_p\); family-uniform bounds for those data,
\(\eta_H\), and \(\omega_q\) have not been proved.  Candidate A as written
here needs only the explicit scalar bound (3.3), so it does not promote the
hidden constants in (3.4).  A certified Fourier/Eisenstein implementation of
the computation fallback in Section 9 would have to instantiate them.

### 3.2 Ford tail

The paper-level Ford packing result in `M2_FORD_PACKING_REFEREE.md` gives the
uniform double-coset count

\[
 A_\Gamma(X)\le X^2
\]

after width-one conjugation.  Stieltjes summation therefore gives, with every
loss explicit and rounded upward,

\[
 \sum_{|c|>X}|c|^{-2\sigma}
 \le \frac{\sigma}{\sigma-1}X^{2-2\sigma}
 \quad(\sigma>1,\ X\ge1).                                 \tag{3.5}
\]

At (X=50), (3.5) is at most (5.031) for \(\sigma=1.1\) and
(0.708) for \(\sigma=1.25\), per side.  These are genuine upper bounds,
but they are too large at fixed (X) to supply the missing target-height
RATE.  In R2 they must be combined with a proved matching/drift split and an
\(X=X(q)\) choice.

### 3.3 Roelcke and theta zero count

Roelcke's printed theta bound gives

\[
 r_{1,\theta}\ge\sqrt{\pi^2/2-1/4}
   >2.164440.                                               \tag{3.6}
\]

Hejhal Ch. 11, (3.6), gives only

\[
 N_\theta(|\gamma|\le T)
 =\frac{4T}{\pi}\log\frac{T\sqrt2}{\pi e}+O(\log T).      \tag{3.7}
\]

The remainder constant in (3.7) is not explicit, and (3.7) concerns the theta
group rather than a uniform finite-(q) family.  It therefore does not bound
\(\omega_q(t_0)\) pointwise.  Likewise (3.6) excludes low theta spectral
parameters but gives no local divisor clearance near height \(t_0\).  Using
either statement as the missing local clearance or family-uniform
\(\omega_q\) bound would be **`CONJECTURAL`**.

**Receipt C (all directions already rounded correctly in the prose).**

```text
$ /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import arb, ctx
ctx.dps=80
p=arb.pi()
K124=(1+arb(2).sqrt())*arb(1005)**2
C6=(1+arb(2).sqrt())*arb(10)**2
lead=(arb(2).sqrt()/2)*(p/4).sinh()/(p/2).sinh()
tail=(-3*p/5).exp()/((1-(-2*p/5).exp())*(1-(-27*p/10).exp()))
C7=1/(lead-tail)
nu_a=(p/4).sinh()/(6*p/5).sinh()
nu_s=(p/250).sinh()/(6*p/5).sinh()*(p/1000).cos()
omega=(arb(17)/(3*arb(26).sqrt())).log()/(arb(85)/3).log()
rtheta=(p*p/2-arb(1)/4).sqrt()
ford11=arb(11)*arb(50)**(-arb(1)/5)
ford125=arb(5)/arb(50).sqrt()
print('K_12.4_upper=',K124.upper())
print('C6_finite_upper=',C6.upper())
print('C7_upper=',C7.upper())
print('nu_a_lower=',nu_a.lower())
print('nu_seed_lower=',nu_s.lower())
print('omega_star_lower=',omega.lower())
print('r_theta_lower=',rtheta.lower())
print('Ford_1.1_X50_upper=',ford11.upper())
print('Ford_1.25_X50_upper=',ford125.upper())
PY
K_12.4_upper= [2438416.0533358853266659256536699003018073328359276019776102759523640895715586897 +/- 3.06e-74]
C6_finite_upper= [241.42135623730950488016887242096980785696718753769480731766797379907324784621070 +/- 4.52e-78]
C7_upper= [18.306412365761172063537611773202607977724490835805638209037922282203506272130474 +/- 6.49e-80]
nu_a_lower= [0.040074172228456791456492090323569399346316934388434611973443515934946237135900696 +/- 4.27e-82]
nu_seed_lower= [0.00057973351410350818959475453918595651347099957474008429208763745293524659260092117 +/- 3.33e-84]
omega_star_lower= [0.031564460639675570232725004080329858158939930648996164645294098904292857666625007 +/- 4.65e-82]
r_theta_lower= [2.1644403896953778914938033638679498423790055263283349011045706988254848063980580 +/- 1.61e-82]
Ford_1.1_X50_upper= [5.0303555712005898104297255625837258007716346078127123114579921819531526483777627 +/- 4.60e-80]
Ford_1.25_X50_upper= [0.70710678118654752440084436210484903928483593768847403658833986899536623923105352 +/- 9.40e-82]
```

## 4. First two-constants propagation

Let \(\nu\) be harmonic measure of the right side
\(\Gamma_R=\{\sigma_R+it:|t-t_0|<d\}\) in \(P\).  Put

\[
 H=2d=\frac12,\qquad L=\sigma_R-\frac12=\frac35.
\]

With \(x=\sigma-1/2\) and \(y=t-(t_0-d)\), the function

\[
 v(x,y)=\frac{\sinh(\pi x/H)}{\sinh(\pi L/H)}
          \sin(\pi y/H)                                   \tag{4.1}
\]

is harmonic, is zero on the left/top/bottom sides, and is at most one on the
right side.  Hence \(v\le\nu\) by the maximum principle.  This gives the
certified geometry floors

\[
 \begin{aligned}
 \nu_a&:=\nu(5/8+it_0)
   \ge \frac{\sinh(\pi/4)}{\sinh(6\pi/5)}>0.04007,\\
 \nu_s&:=\inf_{D_+}\nu
   \ge\frac{\sinh(\pi/250)}{\sinh(6\pi/5)}
       \cos(\pi/1000)>0.000579.
 \end{aligned}                                             \tag{4.2}
\]

Direct Arb subdivision of the boundary of the larger rectangle
\([1/2,1.1]\times[t_0-0.5,t_0+0.5]\) gives
\(|\phi_\infty|<0.3825\) there.  Since (1.1) is holomorphic on that closed
rectangle, the maximum principle gives the same bound throughout it.  With
(3.3), on every non-RATE side of \(P\),

\[
 |F_q|\le242+0.3825<243=:K.                                \tag{4.3}
\]

Assume the missing right-boundary input

\[
 E_R(q)\le C_Rq^{-\alpha}\le K,
 \qquad q\ge q_{\rm RATE},\quad C_R,\alpha>0.              \tag{RATE}
\]

The two-constants theorem applied to the subharmonic function
\(\log|F_q|\) now gives, using the lower bounds in (4.2) in the safe direction,

\[
 \begin{aligned}
 E_a(q)&:=|F_q(5/8+it_0)|
 \le K^{1-0.04007}E_R(q)^{0.04007},                         \tag{4.4}\\
 E_s(q)&:=\sup_{D_+}|F_q|
 \le K^{1-0.000579}E_R(q)^{0.000579}.                       \tag{4.5}
 \end{aligned}
\]

The theta anchor is safely away from its right-half zero at
\(3/4+it_0\):

\[
 m_a:=|\phi_\infty(5/8+it_0)|>0.09867.                     \tag{4.6}
\]

Activate the Hejhal anchor by requiring

\[
 K^{1-0.04007}(C_Rq^{-\alpha})^{0.04007}<0.09867/2.         \tag{A}
\]

Then \(|\phi_q(5/8+it_0)|>0.09867/2\).

## 5. Making Lemma 7.9 and (7.23) explicit

Hejhal's Lemma 7.9 is stated for
\(A=[0,1]\times[-1,1]\).  For a holomorphic \(f\) with
\(0<|f|\le1\), it bounds

\[
 \sup_{0\le h\le1/10}\int_{-1/2}^{1/2}
 \log\frac1{|f(h+iy)|}\,dy
 \le C_7\log\frac1{|f(1/2)|}.                              \tag{5.1}
\]

The scan asserts existence of \(C_7\), but does not print a number.  Here is
an explicit bound.  For \(A(h)=[h,1]\times[-1,1]\), the Poisson density on
its left side, observed from \(1/2\), is the separated-variables series

\[
 P_h(y)=\sum_{\substack{n\ge1\\n\ \mathrm{odd}}}
 \cos(n\pi y/2)\frac{\sinh(n\pi/4)}
                         {\sinh(n\pi(1-h)/2)}.              \tag{5.2}
\]

For \(0\le h\le1/10\), \(|y|\le1/2\), retain the \(n=1\) term and bound the
remaining odd terms absolutely:

\[
 \begin{aligned}
 P_h(y)&\ge m_7,\\
 m_7&:=\frac{\sqrt2}{2}\frac{\sinh(\pi/4)}{\sinh(\pi/2)}
 -\frac{e^{-3\pi/5}}
 {(1-e^{-2\pi/5})(1-e^{-27\pi/10})}
 >0.0546256.                                                \tag{5.3}
 \end{aligned}
\]

Indeed, for odd \(n\ge3\),

\[
 \frac{\sinh(n\pi/4)}{\sinh(9n\pi/20)}
 \le\frac{e^{-n\pi/5}}{1-e^{-27\pi/10}},
\]

and the remaining odd geometric series gives (5.3).  Green's formula in
Hejhal's proof identifies \(P_h=(2\pi)^{-1}\partial_ng\), so

\[
 C_7\le m_7^{-1}<18.307.                                   \tag{5.4}
\]

This is an upper bound for the source's \(C_7\), not a fitted value.

Under \(H_0\), apply (5.1) to \(f=\phi_q/242\) after the affine scaling

\[
 s=\frac12+d x+i(t_0+d y).
\]

The standard anchor \(x=1/2,y=0\) maps to \(5/8+it_0\).  From (A),

\[
 L_a:=\log\frac{2\cdot242}{0.09867}<8.49806.                \tag{5.5}
\]

Thus

\[
 \sup_{0\le h\le d/10}
 \int_{t_0-d/2}^{t_0+d/2}
 \log\frac{242}{|\phi_q(1/2+h+it)|}\,dt
 \le d\,(18.307)L_a.                                      \tag{5.6}
\]

Let

\[
 B=[\tfrac12-d/10,\tfrac12+d/10]
     \times[t_0-d/2,t_0+d/2].
\]

Reflection (2.3), (5.6), and \(|\phi_q|\le242\) on the right half give the
fully transcribed version of (7.23):

\[
 \iint_B|\log|\phi_q(s)||\,d\sigma\,dt
 \le \frac{d^2}{5}\{18.307L_a+\log242\}.                   \tag{5.7}
\]

Every factor in (5.7) is accounted for: one \(d/10\) integration in \(h\),
one \(d\) scaling in \(t\), a factor two from reflection, and the
\(\log242\) normalization loss.

## 6. Lemma 7.10: explicit disc bound

The disc \(D(z_c,d/10)\) is contained in \(B\).  Scale it to the unit disc.
The unit-disc area integral of \(\log^+|\phi_q|\) is at most

\[
 20\{18.307L_a+\log242\}.                                  \tag{6.1}
\]

The target disc \(D_0=D(z_c,d/15)\) has normalized radius \(2/3\).  Hejhal's
exact Lemma 7.10 coefficient \(2M/(1-r)^2\) therefore gives

\[
 \sup_{D_0}|\phi_q|
 \le K_H:=\exp\{360(18.307L_a+\log242)\}<e^{57983}.         \tag{6.2}
\]

An Arb square cover of the larger disc \(D(z_c,1/30)\) gives

\[
 \sup_{D_0}|\phi_\infty|<0.491.                            \tag{6.3}
\]

Hence

\[
 \sup_{D_0}|F_q|\le K_F:=K_H+0.491<e^{57984}.              \tag{6.4}
\]

This enormous constant is intentional: bounds are rounded upward, and no
unprinted sharpness is assumed.

## 7. Second two-constants propagation

Let \(U=D_0\setminus\overline D_+\), and let \(\omega\) be harmonic measure
of \(\partial D_+\) in \(U\).  Put \(R_0=1/60\).  The harmonic barrier

\[
 h(z)=\frac{\log((R_0-a)/|z-(z_c+a)|)}
             {\log((R_0-a)/r)}
\]

is at most zero on \(\partial D_0\) and equals one on
\(\partial D_+\).  Thus \(h\le\omega\).  For \(z\in I_1\),

\[
 |z-(z_c+a)|\le\sqrt{a^2+(1/80)^2}=\frac{\sqrt{26}}{400}.
\]

Consequently

\[
 \omega_*:=\inf_{I_1}\omega
 \ge\frac{\log(17/(3\sqrt{26}))}{\log(85/3)}
 >0.03156.                                                  \tag{7.1}
\]

Apply the two-constants theorem to \(F_q\) on \(U\), with (4.5) on the inner
circle and (6.4) on the outer circle.  Since \(E_R\le K<K_F\), replacing both
harmonic measures by their lower floors is in the upper-bound direction:

\[
 \begin{aligned}
 E_3(q)&:=\sup_{s\in I_1}|F_q(s)|\\
 &\le K_F^{1-0.03156}
       K^{0.03156(1-0.000579)}
       E_R(q)^{0.03156\cdot0.000579}.                       \tag{7.2}
 \end{aligned}
\]

Set

\[
 c_0=0.03156\cdot0.000579=1.827324\times10^{-5}.           \tag{7.3}
\]

Using \(K=243\), \(\log K_F<57984\), and (RATE), (7.2) becomes the explicit
upper envelope

\[
 \boxed{\quad
 \log E_3(q)
 <56155+c_0\log C_R-\alpha c_0\log q.
 \quad}                                                     \tag{7.4}
\]

No transport loss remains unnamed.

## 8. Certified R4 margin and conditional R3 theorem

At the exact point \(z_c\), Arb gives

\[
 |\phi_\infty(z_c)|
 =0.3385371770131448490\ldots,qquad
 1-|\phi_\infty(z_c)|>0.6614628229868551509.               \tag{8.1}
\]

The prior R4 value \(0.6604\) was only a 41-point sampled-grid witness on
\(|t-t_0|\le0.025\).  A 100,000-cell Arb cover now proves on that *continuous*
interval

\[
 \sup |\phi_\infty(1/2+it)|
 <0.33969022985547781,qquad
 d_*:=\inf(1-|\phi_\infty|)>0.6603.                        \tag{8.2}
\]

This larger interval contains \(I_1\).  Thus the sampled \(0.6604\) is used
only as an orientation point; the theorem consumes the downward-rounded,
interval-certified \(d_*=0.6603\).

Under \(H_0(q)\), (1.2), (7.2), and (8.2) give simultaneously

\[
 0.6603<|F_q(1/2+it)|\le E_3(q),\qquad |t-t_0|\le1/80.
\]

Therefore the strict inequality

\[
 E_3(q)<0.6603                                               \tag{C}
\]

refutes \(H_0(q)\).

> **Conditional R3 theorem.**  Suppose (RATE), the standard finite-(q)
> Ch. 6/Hejhal hypotheses, and the stated holomorphy/reflection hypotheses hold.
> If (A) and (C) hold, then \(\phi_q\) has a zero in
> \([1/2,3/4]\times[t_0-1/4,t_0+1/4]\).  Equation (7.22) supplies the
> reflected pole in the left rectangle.

For a proved pure-power RATE, safe strict integer thresholds would be

\[
 \begin{aligned}
 q_A&=\left\lfloor
 \left(\frac{2\,243^{1-0.04007}C_R^{0.04007}}{0.09867}
 \right)^{1/(0.04007\alpha)}\right\rfloor+1,\\
 q_C&=\left\lfloor
 \exp\left(\frac{56155-\log(0.6603)}{\alpha c_0}\right)
 C_R^{1/\alpha}\right\rfloor+1.                            \tag{8.3}
 \end{aligned}
\]

The rounded constants imply

\[
 \frac{56155-\log(0.6603)}{c_0}<3.073095689\times10^9.      \tag{8.4}
\]

This is a conditional upper construction, not a current \(q_0\).  The
transport is catastrophically lossy even before the unknown \(C_R,\alpha\)
are inserted.

The final onset would be

\[
 q_0=\max(12,q_{\rm RATE},q_A,q_C,q_{\rm divisor},q_{\rm monotone}),
                                                               \tag{8.5}
\]

but the current set of admissible values is empty because
\(C_R,\alpha,q_{\rm RATE}\) and the target-boundary monotonic envelope are not
proved.  Hence **`q0 = UNDEFINED`**.

The existing \(q=64\), \(t=7.0665\) rows cannot be substituted: their
truncation-doubling disagreements are about \(2.5\%\), so both were excluded
from the R2 slope claims.

**Receipt M (the margin and anchor).**

```text
$ /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import acb, arb, ctx
ctx.dps=80
def phi(s):
    h=acb(arb('0.5'))
    return acb.pi().sqrt()*(s-h).gamma()*(2*s-acb(1)).zeta()/(s.gamma()*(2*s).zeta()*(acb(4)**s-acb(1)))
t0=(acb.zeta_zero(1)/2).imag
for label,s in [('critical',acb(arb('0.5'),t0)),('anchor',acb(arb(5)/8,t0))]:
    a=abs(phi(s))
    print(label+'_abs_lower=',a.lower())
    print(label+'_abs_upper=',a.upper())
print('critical_defect_lower=',(arb(1)-abs(phi(acb(arb('0.5'),t0)))).lower())
PY
critical_abs_lower= [0.33853717701314484903457519148210298746310270476315742493489868453262600899492405 +/- 2.35e-81]
critical_abs_upper= [0.33853717701314484903457519148210298746310270476315742493489868453262600899493937 +/- 3.33e-81]
anchor_abs_lower= [0.098677817519175272169392553350782237098325160861115365271584566065494930609764439 +/- 4.06e-82]
anchor_abs_upper= [0.098677817519175272169392553350782237098325160861115365271584566065494930609769032 +/- 1.70e-82]
critical_defect_lower= [0.66146282298685515096542480851789701253689729523684257506510131546737399100506063 +/- 3.86e-81]
```

**Receipt W (continuous-window cover; adjacent cells overlap through outward
Arb endpoints).**

```text
$ /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import acb, arb, ctx
ctx.dps=100
def phi(s):
    h=acb(arb('0.5'))
    return acb.pi().sqrt()*(s-h).gamma()*(2*s-acb(1)).zeta()/(s.gamma()*(2*s).zeta()*(acb(4)**s-acb(1)))
t0=(acb.zeta_zero(1)/2).imag
for Rtxt,n in [('0.005',20000),('0.025',100000)]:
    R=arb(Rtxt); half=R/arb(n); best=None; bestj=None
    for j in range(n):
        center=t0-R+arb(2*j+1)*R/arb(n)
        ti=(center-half).union(center+half)
        a=abs(phi(acb(arb('0.5'),ti))).upper()
        if best is None or best < a: best=a; bestj=j
    print('n=',n,'radius=',R.mid())
    print('max_abs_upper=',best)
    print('defect_lower=',(arb(1)-best).lower())
    print('worst_cell=',bestj)
PY
n= 20000 radius= [0.005000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 +/- 2.26e-105]
max_abs_upper= 0.3388734757900238037109375000000000000000000000000000000000000000000000000000000000000000000000000000
defect_lower= 0.6611265242099761962890625000000000000000000000000000000000000000000000000000000000000000000000000000
worst_cell= 19999
n= 100000 radius= [0.02500000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 +/- 4.48e-104]
max_abs_upper= 0.3396902298554778099060058593750000000000000000000000000000000000000000000000000000000000000000000000
defect_lower= 0.6603097701445221900939941406250000000000000000000000000000000000000000000000000000000000000000000000
worst_cell= 99999
```

**Receipt B (theta rectangle/disc upper bounds).**  The first three lines are
the left, top, and bottom sides of the larger rectangle; the separate right
side is also below the displayed maximum.  The square cover contains
\(D(z_c,1/30)\), hence contains \(D_0\).

```text
$ /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import acb, arb, ctx
ctx.dps=80
def phi(s):
    h=acb(arb('0.5'))
    return acb.pi().sqrt()*(s-h).gamma()*(2*s-acb(1)).zeta()/(s.gamma()*(2*s).zeta()*(acb(4)**s-acb(1)))
def box(c,h): return (c-h).union(c+h)
def edge(kind,n):
    t0=(acb.zeta_zero(1)/2).imag
    lo,hi,fixed=(t0-arb('0.5'),t0+arb('0.5'),arb('0.5') if kind=='left' else arb('1.1')) if kind in ('left','right') else (arb('0.5'),arb('1.1'),t0+(arb('0.5') if kind=='top' else -arb('0.5')))
    step=(hi-lo)/arb(n); half=step/2; best=None; cell=None
    for j in range(n):
        v=lo+(arb(j)+arb('0.5'))*step
        s=acb(fixed,box(v,half)) if kind in ('left','right') else acb(box(v,half),fixed)
        u=abs(phi(s)).upper()
        if best is None or best<u: best,cell=u,j
    print(kind,'n=',n,'max_abs_upper=',best,'cell=',cell)
for kind,n in [('left',40000),('right',40000),('top',24000),('bottom',24000)]: edge(kind,n)
t0=(acb.zeta_zero(1)/2).imag; R=arb(1)/30; n=300; step=2*R/arb(n); half=step/2; best=None; cell=None
for i in range(n):
    xb=box(arb('0.5')-R+(arb(i)+arb('0.5'))*step,half)
    for j in range(n):
        yb=box(t0-R+(arb(j)+arb('0.5'))*step,half)
        u=abs(phi(acb(xb,yb))).upper()
        if best is None or best<u: best,cell=u,(i,j)
print('square_cover_n=',n,'R=',R)
print('K_infty_0_upper=',best)
print('worst_cell=',cell)
PY
left n= 40000 max_abs_upper= 0.38244226248934864997863769531250000000000000000000000000000000000000000000000000 cell= 39999
right n= 40000 max_abs_upper= 0.11071700614411383867263793945312500000000000000000000000000000000000000000000000 cell= 39999
top n= 24000 max_abs_upper= 0.38242738647386431694030761718750000000000000000000000000000000000000000000000000 cell= 0
bottom n= 24000 max_abs_upper= 0.33918082108721137046813964843750000000000000000000000000000000000000000000000000 cell= 0
square_cover_n= 300 R= [0.033333333333333333333333333333333333333333333333333333333333333333333333333333333 +/- 3.95e-82]
K_infty_0_upper= 0.49087123386561870574951171875000000000000000000000000000000000000000000000000000
worst_cell= (0, 207)
```

**Receipt A (rounded transport arithmetic).**

```text
$ python3 - <<'PY'
import math
C6=242.; C7=18.307; m=0.09867; K=243.; nu=0.000579; om=0.03156
L=math.log(2*C6/m)
logKH=360*(C7*L+math.log(C6))
logKF=math.ceil(logKH)+1
base=(1-om)*logKF+om*(1-nu)*math.log(K)
c=nu*om
print('rounded_L_anchor_upper=',L)
print('rounded_log_KH_upper=',math.ceil(logKH))
print('rounded_log_KF_upper=',logKF)
print('rounded_transport_base_upper=',math.ceil(base))
print('rate_exponent_multiplier_lower=',c)
print('margin_rhs_over_multiplier=',(math.ceil(base)-math.log(0.6603))/c)
PY
rounded_L_anchor_upper= 8.498059236829693
rounded_log_KH_upper= 57983
rounded_log_KF_upper= 57984
rounded_transport_base_upper= 56155
rate_exponent_multiplier_lower= 1.827324e-05
margin_rhs_over_multiplier= 3073095688.613611
```

**Receipt R2 (why no target-height RATE can be claimed).**

```text
$ jq '.[] | select(.q==64 and .t==7.0665) | {q,sigma,t,convergence_reldiff,D}' research_notes/rh_goals_2026-08-14/lane_g/law_probes/rate_measure_data.json
{
  "q": 64,
  "sigma": 1.1,
  "t": 7.0665,
  "convergence_reldiff": 0.025405127702252315,
  "D": 0.0006325744768117174
}
{
  "q": 64,
  "sigma": 1.25,
  "t": 7.0665,
  "convergence_reldiff": 0.024478728503171312,
  "D": 0.0005111854277226604
}
```

The displayed \(D\) values are **`NOT EVIDENCE`** for a rate because their
own convergence control fails.

## 9. Third fallback: per-(q) certified contour transport

There is a computation-flavoured fallback, but its scope must be stated
correctly.

For each fixed finite \(q\) in a predeclared range:

1. Represent \(\lambda_q=2\cos(\pi/q)\) as an Arb interval and evaluate a
   rigorously continued \(\phi_q\), not the unconverged fixed-truncation rate
   proxy.
2. Choose a rational contour \(\Gamma\) strictly inside \(\Re s>1/2\)
   surrounding the right-half theta-zero window, or a contour for a direct
   argument-principle count of \(\phi_q\).  Certify all pole clearances.
3. Subdivide every contour edge.  On each segment enclose the finite head,
   use the Ford bound (3.5) for both tails, and bound segment variation by an
   interval derivative or Taylor enclosure.  Failed denominator/residual
   controls make the segment **`UNVERIFIABLE`**, not evidence.
4. For comparison transport, certify

   \[
   B_q=\sup_{\Gamma}|\phi_q-\phi_\infty|,qquad
   m_\Gamma=\inf_{\Gamma}|\phi_\infty|>0.
   \]

   If \(B_q<m_\Gamma\), Rouché gives the theta zero count.  If \(\Gamma\)
   bounds a pole-free domain and only an interior error is needed, the maximum
   principle gives \(\sup_\Omega|F_q|\le B_q\).
5. Prefer a direct certified winding of \(\phi_q(\Gamma)\) when the theta
   comparison margin is thin; record the winding interval and the no-boundary-
   zero certificate.

This is finite mathematics once a certified meromorphic-continuation evaluator
exists.  The present evaluator does not meet that premise at \(t_{\rm meas}\),
as Receipt R2 shows; the raw Dirichlet series is absolutely convergent only to
the right of one, so Ford tails alone do not evaluate the contour near
\(\Re s=1/2\).  A certified Fourier/scattering linear solve would need the
uninstantiated Theorem 12.9 constants, while a transfer-operator evaluator
would need a proved identification with this scattering coefficient.

**Pincer assessment.**  This fallback can replace *uniform analytic transport
on any already fixed finite block* \(q\le Q\), and is an excellent finite-base
certificate.  It cannot replace analytic R3 for the infinite tail
\(q\ge q_0\), nor can it determine \(q_0\) without a separate uniform RATE;
using “compute only up to the eventual \(q_0\)” before an analytic argument
produces \(q_0\) is circular.  If another theorem supplies a finite \(q_0\),
then per-(q) contours for \(q<q_0\) can complete the finite half of the
pincer.  With the present crude Route-B transport scale (8.4), exhaustive
computation up to its conditional threshold would be infeasible anyway.

## 10. Final gap ledger

| Item | Verdict |
|---|---|
| Runner-up identification: Candidate A | **PROVED by plan text** |
| Exact \(t_0\), theta anchor, critical-line defect | **Arb-certified** |
| R4 continuous defect \(d_*>0.6603\) | **Arb-certified**, replaces sampled-grid promotion |
| Prop. 12.4 raw bound and finite \(B=10\) Lemma 7.7 bound | **SOURCE + explicit arithmetic** |
| Ford double-coset tail (3.5) | **Paper-level proved**; Lean formalization open |
| Explicit \(C_7<18.307\) | **PROVED here** by Poisson-kernel lower bound |
| First/second harmonic-measure floors | **PROVED here** by explicit barriers |
| Lemma 7.10 coefficient and \(K_H,K_F\) | **PROVED conditionally on \(H_0\) and (A)** |
| Theta (3.6) zero-count remainder / finite-family \(\omega_q\) | **GAP**; not consumed by Candidate A |
| Roelcke local clearance at \(t_0\) | **DOES NOT FOLLOW** from the global gap |
| Target-boundary \(C_R,\alpha,q_{\rm RATE}\), M1/M3 uniformity | **GAP** |
| Numeric margin at \(t_0\) | lower margin **PASS**; transported upper margin **UNDECIDED** |
| Effective analytic \(q_0\) | **`UNDEFINED`** |
| Per-(q) computation fallback | **CONJECTURAL IMPLEMENTATION**; finite-side only |

## Sources

- `R3_R5_ASSEMBLY_PLAN_SOL.md`, Sections 0, 2, 3.1--3.5, 5.1, 6--8.
- `LAW_HEJHAL_S7_EXTRACT.md`, especially the extraction of (7.22), Lemmas
  7.9--7.10, (7.23), Theorem 7.11, and Corollary 7.12.
- Banked primary scan
  `../lane_p/literature/Hejhal_LNM1001_Vol2_s7_pp568-600.pdf`, printed
  pp. 574--578.
- `LAW_HEJHAL_CH6S12_CH11S3_EXTRACT.md` and banked primary scans
  `../lane_p/literature/Hejhal_LNM1001_Vol2_ch6s12_pp149-166.pdf`,
  `../lane_p/literature/Hejhal_LNM1001_Vol2_ch11s3_pp524-532.pdf`.
- `LAW_R4_THETA_DEFECT.md` and `law_probes/r4_defect.py`.
- `M2_FORD_PACKING_REFEREE.md` and `LAW_M2_TAIL_MAJORANT_DRAFT.md`.

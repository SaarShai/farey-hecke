# R3 strip transport execution: right-half theta-zero route

**Date:** 2026-08-18  
**Lane:** G / R3  
**Mechanism selected:** Candidate A0 of `R3_R5_ASSEMBLY_PLAN_SOL.md`
§§2--4, the plan's highest-ranked mechanism at the named height.  
**Status:** **CONDITIONAL TRANSPORT THEOREM PROVED; CURRENT UNCONDITIONAL R3
REMAINS A GAP.**  The theta contour margin and harmonic-measure loss are
rigorously enclosed below.  The available notes do **not** supply a proved
target-height boundary RATE constant, a family-uniform Ch.6 boundary constant,
or a finite-family no-pole certificate.  Consequently no effective numerical
`q0` is proved.

Every unproved assertion below is labelled **CONJECTURAL**.  All reported
numerics are rounded in the adverse direction and have command/output receipts
in §8.

## 1. Verdict

The preferred R3 mechanism works in the following precise sense.

Let

\[
 \rho _1=\tfrac12+i\gamma _1,\qquad
 t_0=\gamma _1/2,\qquad
 z_0=\frac{1+\rho _1}{2}=\frac34+i t_0,
\]

and

\[
 \phi_\infty(s)=
 \frac{\sqrt\pi\,\Gamma(s-\tfrac12)\zeta(2s-1)}
 {\Gamma(s)\zeta(2s)(4^s-1)}.
\]

Choose

\[
 \delta=\frac12,\qquad r_z=\frac18,
 \qquad D_z=D(z_0,r_z),
\]

and the finite propagation rectangle

\[
 \Omega=\left\{s:\frac12<\Re s<\frac{11}{10},\quad
                  |\Im s-t_0|<\frac12\right\}.
\]

Its right side is

\[
 \Gamma_R=\left\{\frac{11}{10}+it:|t-t_0|\le\frac12\right\}.
\]

The closed disc lies strictly in `Re s > 1/2`, inside the plan's
`R_delta^+`.  The Arb receipt proves

\[
 m_z:=\min_{\partial D_z}|\phi_\infty(s)|\ge 0.0439,
 \qquad
 \nu_z:=\inf_{\partial D_z}
 \omega(s,\Gamma_R;\Omega)\ge 0.1552.                 \tag{1.1}
\]

Let

\[
 F_q=\phi_q-\phi_\infty,qquad
 E_R(q)=\sup_{\Gamma_R}|F_q|,
\]

and let `K_+` be a bound for `|F_q|` on the other three sides of
`\partial\Omega`.  If both scattering functions are holomorphic on
`\overline{\Omega}` and `0<E_R(q)\le K_+`, then the two-constants theorem gives

\[
 \boxed{
 \sup_{\partial D_z}|\phi_q-\phi_\infty|
 \le K_+^{1-\nu_0}E_R(q)^{\nu_0},
 \qquad \nu_0=0.1552 .}                                \tag{R3-Z}
\]

Therefore

\[
 K_+^{1-\nu_0}E_R(q)^{\nu_0}<0.0439                  \tag{1.2}
\]

implies, by Rouché, that `phi_q` has a zero in `D_z`.  Hejhal's exact
reflection identity (7.22) then gives a pole at `1-conj(s_q)`.

This is the corrected R3 result.  It is conditional only on the explicitly
listed gates in §5; it does not use critical-line convergence, `H0`, R4's
sampled-grid defect, Lemmas 7.9/7.10, or a Blaschke-`omega` estimate.

## 2. The theta zero and the contour are certified

### 2.1 The zero at `z0`

At `z_0`,

\[
 2z_0-1=\rho _1,
\]

so the numerator factor `zeta(2z_0-1)` vanishes.  Every other displayed
factor is regular and nonzero there: gamma has no zeros; `2z_0` has real part
strictly larger than one, where the zeta Euler product is nonzero; and
`4^{z_0}-1` cannot vanish because `Re z_0>0`.  Thus

\[
 \phi_\infty(z_0)=0.                                  \tag{2.1}
\]

No simplicity assumption on `rho_1` is used.

On `\overline{D_z}`, the real part of `s` lies in `[5/8,7/8]`.  Consequently
the real part of `2s` lies in `[5/4,7/4]`, so `zeta(2s)` is nonzero there;
the gamma factors avoid their poles; and `4^s-1` is nonzero.  Hence
`phi_infty` is holomorphic on the closed disc.  The interval cover in §8.1
then proves the first inequality in (1.1), so there is no boundary zero.

The local theta zero-count asymptotic (Hejhal (3.6)) is not needed for the
existence conclusion.  It has an unspecified `O(log T)` remainder and by
itself is not an explicit local disc count.  Rouché preserves the complete
count whatever that count is; (2.1) already proves that it is nonzero.

### 2.2 Why Roelcke does not close the finite divisor gate

The printed theta spectral-gap value `r_1 >= 2.164440` is useful global
bookkeeping, but it does not bound the spacing of scattering divisors near the
higher target height.  Using it as a finite-`q` no-pole certificate on
`\overline{\Omega}` would be **CONJECTURAL**.  The finite-family holomorphy gate
is therefore retained explicitly.

## 3. Harmonic-measure calculation and proof of `(R3-Z)`

Translate `Omega` to

\[
 0<x<L,\qquad 0<y<1,qquad L=\frac35,
\]

where `x=Re(s)-1/2` and `y=Im(s)-(t_0-1/2)`.  The harmonic measure of the
right side is

\[
 \nu(x,y)=\sum_{\substack{n\ge1\\ n\ \mathrm{odd}}}
 \frac{4}{n\pi}\frac{\sinh(n\pi x)}{\sinh(n\pi L)}
 \sin(n\pi y).                                         \tag{3.1}
\]

On `\partial D_z`,

\[
 x=\frac14+\frac18\cos\theta,\qquad
 y=\frac12+\frac18\sin\theta.
\]

The §8.1 receipt covers the whole parameter circle by interval boxes, sums
(3.1) through the stated odd index, and subtracts a rigorous geometric tail.
It proves the second inequality in (1.1).

Now suppose the following two analytic bounds hold for a fixed finite `q`:

\[
 |F_q|\le E_R(q)\quad\hbox{on }\Gamma_R,
 \qquad
 |F_q|\le K_+\quad\hbox{on }\partial\Omega\setminus\Gamma_R,             \tag{3.2}
\]

with `F_q` holomorphic on `\overline{\Omega}` and `E_R(q)\le K_+`.  Applying the
two-constants theorem to the subharmonic function `log|F_q|` gives, for every
`s in Omega`,

\[
 |F_q(s)|\le
 E_R(q)^{\nu(s)}K_+^{1-\nu(s)}.                         \tag{3.3}
\]

Because `E_R(q)/K_+<=1`, the right side decreases as `nu(s)` increases.
Using `nu(s)\ge nu_0` on `\partial D_z` proves `(R3-Z)`.

If the missing RATE input is eventually proved in the form

\[
 E_R(q)\le C_Rq^{-\alpha},\qquad
 C_R>0,\quad \alpha>0,\quad q\ge q_{\rm RATE},            \tag{R2*}
\]

then `(R3-Z)` becomes

\[
 \sup_{\partial D_z}|F_q|
 \le C_Zq^{-p_Z},
 \qquad
 C_Z=K_+^{1-\nu_0}C_R^{\nu_0},
 \qquad p_Z=\alpha\nu_0.                               \tag{3.4}
\]

Here `C_R`, `alpha`, and `q_RATE` are currently **CONJECTURAL / MISSING** at
the required target-height boundary.  Equation (3.4) is a proved implication,
not a claim that those constants now exist with the needed uniformity.

## 4. Rouché and reflection

Assume (1.2) and the finite-family holomorphy gate.  On `\partial D_z`,

\[
 |\phi_q-\phi_\infty|<0.0439\le|\phi_\infty|.
\]

Rouché gives equal zero counts for `phi_q` and `phi_infty` in `D_z`, with
multiplicity.  Since (2.1) supplies at least one theta zero, there is at least
one `s_q in D_z` with `phi_q(s_q)=0`.

Hejhal (7.22), in the convention extracted in
`LAW_HEJHAL_S7_EXTRACT.md:67-81`, is

\[
 \phi_q(\tfrac12-h+it)\,
 \overline{\phi_q(\tfrac12+h+i\bar t)}=1.
\]

It follows that `phi_q` has a pole of the same order at

\[
 1-\overline{s_q}.
\]

This proves the desired right-zero/left-pole alternative without ever
asserting convergence on `Re s=1/2`.

## 5. Constant ledger and isolated gaps

| constant/gate | definition or bound | status |
|---|---|---|
| `sigma_R` | `11/10` | chosen exactly |
| `delta` | `1/2` | chosen exactly |
| `r_z` | `1/8` | chosen exactly |
| `m_z` | `min_{\partial D_z}|phi_infty| >= 0.0439` | **PROVED**, Arb interval cover |
| `nu_z` | `inf_{\partial D_z} omega(s,Gamma_R;Omega) >= 0.1552` | **PROVED**, Arb/Fourier interval cover |
| `E_R(q)` | `sup_{Gamma_R}|phi_q-phi_infty|` | definition |
| `C_R, alpha, q_RATE` | `(R2*)` constants on the whole right side | **CONJECTURAL / MISSING** |
| `B_q` | Hejhal `B=5+y_0` for the finite group | source-defined per group |
| `K_12.4(q)` | `(1+sqrt(2))B_q^2` | source bound for each admissible group |
| `K_+` | non-RATE-boundary bound for `|F_q|` | **CONJECTURAL / MISSING family-uniformly** |
| `q_divisor` | activation threshold for finite `phi_q` holomorphy on `\overline{\Omega}` | **CONJECTURAL / MISSING** |
| `C_Z,p_Z` | (3.4) | explicit once the missing inputs are supplied |

### 5.1 Ch.6 gives a mechanism, not the needed family constant

Prop. 12.4 gives

\[
 |\phi(s)|\le(1+\sqrt2)B^2
\]

in the printed strip.  If one additionally assumes a common admissible
`y_0=1000` for both finite and theta sides, then `B=1005` and the adverse
triangle inequality gives

\[
 K_+<4{,}876{,}833.                                    \tag{5.1}
\]

The common-`y_0` family assertion is **CONJECTURAL** in the present repository:
the extraction note expressly says that the Ch.6 constants and geometric data
have not been made uniform across the Hecke family.  Thus (5.1) is a
**CONJECTURAL diagnostic assumption**, not a promoted R3 input.

Thm. 12.9 is no substitute yet: its big-`O` constants depend on the group,
character, fundamental region, and divisor-exclusion distance.  The
Blaschke-`omega` route also retains a group-dependent integral-growth constant
and no pointwise target-window bound.  Candidate C is therefore not more
effective from the available data.

### 5.2 What the Ford tail does and does not close

The Ford-horoball argument proves the raw uniform tail shape recorded in
`M2_G1G2_CLOSURE_SOL.md`.  It does not prove the corrected coset-level M1 map,
the matched derivative estimate N1, the weighted drift tail N3/N4-scale, or
M3 uniformity on `Gamma_R`.  Therefore it does not supply `C_R` in `(R2*)`.
Using the Ford tail alone as the boundary RATE theorem would be
**CONJECTURAL**.

### 5.3 Target-height M3 is still absent

The exact target is

\[
 t_0=7.067362570867346895\ldots,
\]

whereas the existing sweep used `7.0665`; the certified offset is larger than
`0.000862570867346895` after rounding down.  The two recorded large-`q`
target-height rows have N-doubling residuals near two-and-a-half percent and
are explicitly not evidence for `C_R` or `alpha`; see §8.2.  Moving from the
sampled height to exact `t_0`, and from a point to the full side `Gamma_R`, is
the open M3 task.

## 6. Thin-margin calculation at `t0`

There are two different margins, and they must not be conflated.

### 6.1 Critical-line mismatch: large, but unused by A0

The Arb evaluation at the exact target gives

\[
 |\phi_\infty(\tfrac12+it_0)|
 <0.338537177013144850,
\]

where the displayed upper bound is rounded up.  Hence the exact point defect
obeys

\[
 1-|\phi_\infty(\tfrac12+it_0)|>0.661462822986855150,   \tag{6.1}
\]

with the lower bound rounded down.  This improves only the *point* receipt.  It
does not promote R4's `0.6604` sampled-grid witness to a continuous-window
infimum.

For every finite one-cusp group, unitarity gives
`|phi_q(1/2+it_0)|=1`; therefore

\[
 |\phi_q(\tfrac12+it_0)-\phi_\infty(\tfrac12+it_0)|
 \ge 1-|\phi_\infty(\tfrac12+it_0)|
 >0.661462822986855150.                                 \tag{6.2}
\]

Thus the proposed statement

> `phi_q-phi_infty -> 0` on the critical line at `t0`

is **FALSE**.  Equation (6.2) proves its negation.  Candidate A0 avoids this
false statement by keeping the whole Rouché contour in `Re s>1/2`.

### 6.2 A0 contour margin: positive, but transport loss is severe

Under the **CONJECTURAL diagnostic assumption** (5.1), the proved values
`m_0=0.0439` and `nu_0=0.1552` give the sufficient right-boundary condition

\[
 E_R(q)<7.03\times10^{-46}.                             \tag{6.3}
\]

The threshold in (6.3) is rounded down.  It is the direct numerical
thin-margin answer for this chosen rectangle: the contour itself is not close
to collapse, but the raw Ch.6 bound combined with small harmonic measure loses
about forty-five decimal orders before Rouché.

For scale only, insert the plan's **CONJECTURAL AND CURRENTLY FORBIDDEN**
provisional values `C_R=2` and `alpha=6/5`.  Then

\[
 p_Z\ge0.18624,
 \qquad C_Z<497{,}576,
\]

and the sufficient integer condition produced by (6.3) is

\[
 q\ge
 75{,}578{,}028{,}497{,}170{,}725{,}293{,}702{,}300{,}965{,}513{,}602{,}908.
                                                               \tag{6.4}
\]

Equation (6.4) is **CONJECTURAL DIAGNOSTIC ONLY; IT IS NOT `q0`**.  The source
plan already rejects `C_R=2` as a majorant for its displayed assembled
envelope, and no target-height `C_R` exists.  The only valid current verdict is

\[
 \boxed{\text{UNVERIFIABLE: effective }q_0\text{ undefined}.}
\]

## 7. Corrected R3 theorem

> **Theorem R3-Z (proved conditional implication).** Fix the exact geometry of
> §1.  Assume:
>
> 1. `phi_infty` and `phi_q` are holomorphic on `\overline{\Omega}` for every
>    `q>=q_divisor`;
> 2. `|F_q|<=K_+` on the three non-RATE sides, with one explicit
>    `q`-independent `K_+`;
> 3. `(R2*)` holds on all of `Gamma_R` with explicit
>    `C_R>0`, `alpha>0`, and `q_RATE`;
> 4. `E_R(q)<=K_+`.
>
> Put `nu_0=0.1552`, `m_0=0.0439`,
> `C_Z=K_+^(1-nu_0) C_R^nu_0`, and `p_Z=alpha nu_0`.  Every
> `q>=max(q_divisor,q_RATE)` satisfying
>
> \[
> C_Zq^{-p_Z}<m_0
> \]
>
> has a zero of `phi_q` in `D_z`; (7.22) gives a pole at the reflected point
> `1-conj(s_q)`.

The theorem is complete as an implication.  Hypotheses 1--3 are presently
**CONJECTURAL / OPEN** for the Hecke family at this boundary.  Consequently the
unconditional/effective target requested by R3 is not proved.

## 8. Receipts

### 8.1 Arb contour, harmonic measure, exact height, and loss calculation

Command actually run:

```bash
/Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import acb, arb, ctx
ctx.dps = 80
pi = arb.pi()
rho1 = acb.zeta_zero(1)
rho2 = acb.zeta_zero(2)
t0 = rho1.imag / 2
z0 = acb(arb(3)/4, t0)
rz = arb(1)/8

def phi_inf(s):
    return (pi.sqrt() * (s-arb(1)/2).gamma() * (2*s-1).zeta()
            / (s.gamma() * (2*s).zeta()
               * ((acb(4).log()*s).exp()-1)))

# Rigorous interval cover of the whole circle |s-z0|=1/8.
Nphi = 8192
m_lower = None
m_index = None
for k in range(Nphi):
    theta = arb(2*pi*(arb(k)+arb(1)/2)/Nphi, pi/Nphi)
    s = z0 + rz*acb(theta.cos(), theta.sin())
    lo = abs(phi_inf(s)).lower()
    if m_lower is None or lo < m_lower:
        m_lower, m_index = lo, k

# Harmonic measure of the right side x=L for the rectangle
# 0<x<L=3/5, 0<y<1.  Fourier series; subtract a rigorous tail.
L = arb(3)/5
nmax = 101
n0 = nmax + 2
a = pi*arb(9)/40  # pi*(L-x_max), x_max=3/8
tail_upper = (4/pi/arb(n0)/(1-(-2*pi*L).exp())
              * (-arb(n0)*a).exp()/(1-(-a).exp())).upper()
Nhm = 4096
nu_lower = None
nu_index = None
for k in range(Nhm):
    theta = arb(2*pi*(arb(k)+arb(1)/2)/Nhm, pi/Nhm)
    x = arb(1)/4 + rz*theta.cos()
    y = arb(1)/2 + rz*theta.sin()
    u = arb(0)
    for n in range(1, nmax+1, 2):
        nn = arb(n)
        u += (4/(nn*pi) * (nn*pi*x).sinh()/(nn*pi*L).sinh()
              * (nn*pi*y).sin())
    lo = u.lower() - tail_upper
    if nu_lower is None or lo < nu_lower:
        nu_lower, nu_index = lo, k

sline = acb(arb(1)/2, t0)
line_abs = abs(phi_inf(sline))
line_defect = 1-line_abs
B = arb(1005)
K124 = (1+arb(2).sqrt())*B**2
K = 2*K124
K_up = arb(4876833)
m_safe = arb('0.0439')
nu_safe = arb('0.1552')
ecrit = (m_safe/(K_up**(1-nu_safe)))**(1/nu_safe)
ecrit_safe = arb('7.03e-46')
alpha = arb(6)/5
p_safe = alpha*nu_safe
CZ_CR2 = K_up**(1-nu_safe)*arb(2)**nu_safe
q_bound_CR2 = (arb(2)/ecrit_safe)**(1/alpha)
q_int_CR2 = q_bound_CR2.upper().ceil()

print('rho1 =', rho1)
print('rho2 =', rho2)
print('t0 =', t0)
print('t0 - 7.0665 =', t0-arb('7.0665'))
print('disc_Re_range = [5/8, 7/8]; mapped_zeta_disc_radius = 1/4')
print('circle_boxes =', Nphi)
print('raw_min_circle_lower =', m_lower, 'box_index =', m_index)
print('CERT m_z >= 0.0439:', bool(m_lower > m_safe))
print('harmonic_boxes =', Nhm, 'series_nmax =', nmax)
print('harmonic_tail_upper =', tail_upper)
print('raw_min_nu_lower =', nu_lower, 'box_index =', nu_index)
print('CERT nu_z >= 0.1552:', bool(nu_lower > nu_safe))
print('|phi_inf(1/2+i*t0)| =', line_abs)
print('point_defect =', line_defect)
print('K_12.4(B=1005) =', K124)
print('K=2*K_12.4 =', K)
print('CERT K < 4876833:', bool(K < K_up))
print('safe_E_R_threshold_exact =', ecrit)
print('CERT safe_E_R_threshold > 7.03e-46:', bool(ecrit > ecrit_safe))
print('CONJECTURAL alpha=6/5 gives p_safe =', p_safe)
print('CONJECTURAL C_R=2 gives C_Z_safe =', CZ_CR2)
print('CONJECTURAL C_R=2 sufficient integer q >=', q_int_CR2)
PY
```

Output:

```text
rho1 = 0.50000000000000000000000000000000000000000000000000000000000000000000000000000000 + [14.134725141734693790457251983562470270784257115699243175685567460149963429809257 +/- 2.59e-79]j
rho2 = 0.50000000000000000000000000000000000000000000000000000000000000000000000000000000 + [21.022039638771554992628479593896902777334340524902781754629520403587598586068891 +/- 2.49e-79]j
t0 = [7.0673625708673468952286259917812351353921285578496215878427837300749817149046284 +/- 2.93e-80]
t0 - 7.0665 = [0.0008625708673468952286259917812351353921285578496215878427837300749817149046284 +/- 3.18e-80]
disc_Re_range = [5/8, 7/8]; mapped_zeta_disc_radius = 1/4
circle_boxes = 8192
raw_min_circle_lower = 0.043908844760153442621231079101562500000000000000000000000000000000000000000000000 box_index = 8103
CERT m_z >= 0.0439: True
harmonic_boxes = 4096 series_nmax = 101
harmonic_tail_upper = [5.9970302308687936556518358859094786204848381047336562662348377118797908982027391e-34 +/- 2.87e-114]
raw_min_nu_lower = [0.15521443750831436494372143994241251210830039284495292345656560333308798731960290 +/- 4.99e-81] box_index = 2048
CERT nu_z >= 0.1552: True
|phi_inf(1/2+i*t0)| = [0.33853717701314484903457519148210298746310270476315742493489868453262600899493 +/- 9.38e-78]
point_defect = [0.66146282298685515096542480851789701253689729523684257506510131546737399100507 +/- 9.38e-78]
K_12.4(B=1005) = [2438416.0533358853266659256536699003018073328359276019776102759523640895715586897 +/- 5.46e-74]
K=2*K_12.4 = [4876832.1066717706533318513073398006036146656718552039552205519047281791431173793 +/- 3.41e-74]
CERT K < 4876833: True
safe_E_R_threshold_exact = [7.03815769739555232731834992351215133164881880238259839272257715532345638540067e-46 +/- 6.40e-124]
CERT safe_E_R_threshold > 7.03e-46: True
CONJECTURAL alpha=6/5 gives p_safe = [0.18624000000000000000000000000000000000000000000000000000000000000000000000000000 +/- 9.14e-82]
CONJECTURAL C_R=2 gives C_Z_safe = [497575.2155200023361408307510404175484372568913064001687118604447650583960171232 +/- 6.70e-74]
CONJECTURAL C_R=2 sufficient integer q >= 75578028497170725293702300965513602908.000000000000000000000000000000000000000000
```

The Arb API semantics used for the first zero were also checked:

```bash
/Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import acb
print(acb.zeta_zero.__doc__)
PY
```

```text
acb.zeta_zero(n)

Returns the *n*-th nontrivial zero of the Riemann zeta function.

    >>> from flint import showgood
    >>> showgood(lambda: acb.zeta_zero(1), dps=25)
    0.5000000000000000000000000 + 14.13472514173469379045725j
    >>> showgood(lambda: acb.zeta_zero(2), dps=25)
    0.5000000000000000000000000 + 21.02203963877155499262848j
    >>> showgood(lambda: acb.zeta_zero(100), dps=25)
    0.5000000000000000000000000 + 236.5242296658162058024755j
    >>> showgood(lambda: acb.zeta_zero(10**6), dps=25)
    0.5000000000000000000000000 + 600269.6770124449555212339j
```

### 8.2 Existing target-height evaluator cells

Command actually run:

```bash
jq '[.[] | select(.q == 64 and .t == 7.0665) | {q, sigma, t, N_base, N_double, convergence_reldiff, D}]' research_notes/rh_goals_2026-08-14/lane_g/law_probes/rate_measure_data.json
```

Output:

```json
[
  {
    "q": 64,
    "sigma": 1.1,
    "t": 7.0665,
    "N_base": 12,
    "N_double": 24,
    "convergence_reldiff": 0.025405127702252315,
    "D": 0.0006325744768117174
  },
  {
    "q": 64,
    "sigma": 1.25,
    "t": 7.0665,
    "N_base": 12,
    "N_double": 24,
    "convergence_reldiff": 0.024478728503171312,
    "D": 0.0005111854277226604
  }
]
```

The displayed `D` values are **NOT EVIDENCE** because their own N-doubling
gate failed.

### 8.3 Source-constant receipt

Command actually run:

```bash
nl -ba research_notes/rh_goals_2026-08-14/lane_g/LAW_HEJHAL_CH6S12_CH11S3_EXTRACT.md | sed -n '28,53p;84,88p'
nl -ba research_notes/rh_goals_2026-08-14/lane_g/M2_G1G2_CLOSURE_SOL.md | sed -n '30,44p'
nl -ba research_notes/rh_goals_2026-08-14/lane_g/R3_R5_ASSEMBLY_PLAN_SOL.md | sed -n '127,143p'
```

Output:

```text
    28  - Setup (12.1): B = 5 + y₀, y₀ ≥ 1000.
    29  - Lemma 12.1: |K_{s−1/2}(y)| ≤ 3·e^{−y}/√y · (1 + 1/√y) for 1/2 ≤ Re s ≤ 3/2,
    30    y > 0. Fully explicit; proof by v = e^ξ substitution + Gaussian integral.
    31  - Lemma 12.2: ∫_η^∞ |K_{s−1/2}(y)|² dy/y ≥ A·e^{−5η−5|t|} with A = c₉e^{−5};
    32    chain c₁..c₉ traced through Sonine–Gegenbauer (avoids the K-Bessel
    33    asymptotic-regime trouble, Remark 12.3), T = 2(η+|t|+c₅).
    34  - Prop 12.4: |φ(s)| ≤ (1+√2)·B² uniformly on 1/2 ≤ Re s ≤ 3/2, |Im s| ≥ 1.
    35    Proof via Green's identity + Parseval on E₀ (Maass–Selberg style, eq 12.2).
    36  - Props 12.5–12.8: Blaschke-type V(s) (|V|≤1, functional eq, Hadamard
    37    factorization with A ≤ 0, B=0 pinned by the e^{−δξ} sandwich (****)),
    38    ω(r) = 1 + Σ_ρ 2η/(η²+(r−γ)²) ≥ 1, ∫_{−R}^R ω = O(R⁴).
    39  - THEOREM 12.9 (the C₆ source): for 1/2 ≤ σ ≤ 3/2, |s−s_k| ≥ δ:
    40    (a) φ(s) uniformly bounded; (b) 1−|φ(s)|² ≤ O[(σ−1/2)ω(t)];
    41    (c) φ_m(s) = O[√ω(t) · e^{3|t| + 5π|m|/η}] for m ≠ 0;
    42    (d) E(x;s;χ) = y^s + φ(s)y^{1−s} + O[√ω(t) e^{3|t|−2πy}] for y ≥ 10η.
    43    Constants depend solely on Γ, χ, 𝓕, δ — independent of m, σ, t.
    44    η = (1/20)·inf{Im(z): z ∈ 𝓕} (eq 12.6).
    45  - (12.8): explicit product identity for φ(s) (Blaschke form) — for later use.
    46
    47  M2 consequence: the Lemma-7.7/C₆ tail majorant in §7 rests on Thm 12.9(c)+(d),
    48  whose proof route is a POTENTIALLY EFFECTIVE SOURCE ROUTE (no normal-families
    49  step). Promoting M2 requires instantiating every hidden big-O constant in
    50  12.9 and proving uniform bounds for Γ, χ, 𝓕, δ, η and ω(t) across the Hecke
    51  family — plausible-looking but unperformed bookkeeping, not a completed
    52  N-uniformity claim. Ineffectivity census of §7 unchanged: still only the two
    53  Vitali/normal-families steps.
    84  - Bonus (Prop 3.5, Roelcke): λ₁ ≥ π²/2, i.e. r₁ ≥ 2.164440 for the theta
    85    group — a printed spectral-gap constant usable in R5 bookkeeping.
    86  - Bonus (3.6): N[|γ| ≤ T] = (4T/π)·ln(T√2/(πe)) + O(ln T) — theta-group
    87    scattering-zero count; feeds ω(t) bookkeeping if M2 transcription targets
    88    the limit group.
    30  5. **The role of G1+G2 in the tail argument can nevertheless be closed by a
    31     different uniform paper theorem.**  Under the standard defining facts
    32     that each \(\mathcal G_N\) is discrete and non-elementary and has exact
    33     width-one cusp stabilizer \(\langle S\rangle\), a Ford-horoball packing
    34     argument gives the cumulative double-coset bound
    35     \[
    36        A_N(X):=\#\{[\gamma]:0<|c_\gamma|\le X\}\le X^2,
    37     \]
    38     and therefore, for \(\sigma>1\) and \(X\ge1\),
    39     \[
    40        \sum_{|c_\gamma|>X}|c_\gamma|^{-2\sigma}
    41        \le \frac{\sigma}{\sigma-1}X^{2-2\sigma}. \tag{M2.PACK}
    42     \]
    43     This is uniform in finite \(N\) and also covers the theta group.  It
    44     replaces, rather than proves, the draft's conditional formula (M2.T).
   127  R2's M3 gap is exactly the passage from its one validated cell
   128  `s=1.1+1.5i` to `(R2*)`. A constant labelled `C(1.1,1.5)` cannot be used at
   129  `t0`.
   130
   131  There is also an internal numerical obstruction to using the draft's
   132  `C(1.1,1.5) <= 2.0`: the displayed assembled bounds give
   133
   134  | `q` | displayed `epsilon_2(q)` | `q^1.2 epsilon_2(q)` |
   135  |---:|---:|---:|
   136  | 24 | 0.2042 | 9.25 |
   137  | 32 | 0.0973 | 6.23 |
   138  | 48 | 0.0376 | 3.91 |
   139
   140  so `2.0 q^-1.2` does not majorize the displayed assembled envelope. The value
   141  `2.0` appears compatible with the measured `D q^1.2`, not with the printed
   142  one-sided `epsilon_2`. Until reconciled, `C_R=2.0` is **`CONJECTURAL`** and is
   143  forbidden in R5.
```

## 9. Sources used

- `R3_R5_ASSEMBLY_PLAN_SOL.md:11-74,147-182,305-350,541-572,795-880`.
- `LAW_HEJHAL_S7_EXTRACT.md:19-48,62-99` and the banked primary scan
  `../lane_p/literature/Hejhal_LNM1001_Vol2_s7_pp568-600.pdf`.
- `LAW_HEJHAL_CH6S12_CH11S3_EXTRACT.md:11-88` and the banked primary scan
  `../lane_p/literature/Hejhal_LNM1001_Vol2_ch6s12_pp149-166.pdf` (printed
  Prop. 12.4 checked at pp.153--156).
- `LAW_R2_RATE_LEMMA_DRAFT.md:257-310,314-341,345-436`.
- `M2_G1G2_CLOSURE_SOL.md:12-44,298-359,415-425`.
- `M3_N1N4_PROMOTION_PLAN_SOL.md:9-50,52-121`.
- `LAW_R4_THETA_DEFECT.md:32-76,126-182,280-313`.
- `LAW_ANCHOR_T1_THETA.md:14-40`.

---

## Dated correction block (2026-08-21, first cold referee D1–D6, append-only)

Applied per R3_TRANSPORT_EXECUTION_REFEREE.md (verdict GAPS NOT REFUTED;
attacks 1, 2, 4, 5 CONFIRMED — two-constants re-derived with the
subharmonic maximum-principle argument and a series-free Monte Carlo
orientation cross-check; Rouché exact-algebra comparison zero verified;
every numeral reproduced at dps = 60).

### D1 (HIGH, citation/hypothesis repair — supersedes §4's :220-232)

phi_q continues to a meromorphic function on C satisfying the
unconditional functional equation phi_q(s) phi_q(1-s) ≡ 1 (Selberg;
Hejhal LNM 1001 Vol. 2, Cor. 7.12, p. 579).  Since phi_q(s_q) = 0 with
Re s_q ∈ [5/8, 7/8], the identity forces a pole of phi_q of the same
order at 1 − s_q, whose real part lies in [1/8, 3/8], strictly left of
the critical line.  Since phi_q has real Dirichlet coefficients in
(7.5), it also satisfies phi_q(s̄) = conj(phi_q(s)), so 1 − conj(s_q)
is a pole of the same order as well.  Hejhal's printed (7.22) (p. 577)
is NOT invoked: as printed it holds only along the subsequence J on
which phi_N is assumed zero-free on [1/2, 1/2+delta] x [t_0 ± delta],
a hypothesis negated at s_q.  With delta = 1/2 the reflection window of
§1 contains the closure of D_z and its mirror image (h <= 3/8 < delta,
|t − t_0| <= 1/8 < delta).

### D3 (unstated input, now stated)

The conclusion 1 − conj(s_q) requires phi_q(s̄) = conj(phi_q(s)) IN
ADDITION to the functional equation (which alone gives 1 − s_q); the
reality of the (7.5) Dirichlet coefficients supplies it, as stated in
the D1 block above.  Either form gives an off-line pole; the theorem's
substance is unaffected.

### D2 (over-assumption, recorded)

phi_infty's holomorphy on the closed rectangle is bundled into the
CONJECTURAL gate although it is unconditionally provable (left edge
Re(2s) = 1 needs only zeta non-vanishing on Re = 1; the rest is the
Euler product).  Conservative as stated; the only genuinely open
holomorphy gate is the finite-q one.

### D4 (certificate hygiene, recorded)

Both certificates are grid-critical: true infima m_z* ≈ 0.0444414 and
nu_z* ≈ 0.1552145 clear the asserted 0.0439 / 0.1552 by only 0.02% /
0.009%, and coarser covers (N = 3000, 5000) FAIL the assertion.  Valid
as printed (interval arithmetic sound; roundings adverse), but
re-runners must use the note's stated box counts or finer.

### D5/D6 (cosmetic)

:71 and :144 missing backslash in \qquad; :225 i t̄ for printed i t.

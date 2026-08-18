# M3 `s`-uniformity execution note

**Date:** 2026-08-18
**Scope:** execution of §2 of `M3_N1N4_PROMOTION_PLAN_SOL.md`.  This note
uses the paper-level Ford packing replacement in
`M2_FORD_PACKING_REFEREE.md:90-156` and the harvested v26/v27 Lean artifacts
(`RateCore.lean:169-275`, `RateCoreII.lean:130-176`).  It
does not promote the RATE lemma.

## 0. Verdict and frozen domain

Freeze the compact rectangle

\[
 K_{15}:=\{s=\sigma+it:1.1\leq\sigma\leq1.5,\ |t|\leq15\}.
\]

The smaller target rectangle in the promotion plan is contained in this one.
The conclusion reached here is:

* **THEOREM (paper-level, conditional on the stated Hecke group hypotheses).**
  Ford packing gives a `q`-uniform raw Dirichlet-series tail and a
  log-weighted tail.  Consequently the Eisenstein Dirichlet series and its
  `s`-derivative form a `q`-uniform normal family on `K15`.
* **THEOREM (machine-verified algebraic inputs).**  The v26 harvest supplies
  the corrected P3/P4/P5 chain: mean-value drift, the `Re s >= -1/2`
  `|c|^{-2s}` estimate, and `2-lambda_q <= pi^2/q^2`.  The v27 harvest supplies
  theta evenness and the arithmetic `phi(2c)` count.
* **CONJECTURAL (the requested M3 rate).**  The Ford tail plus the P-chain do
  not prove a constant `C_K` with
  `|phi_q(s)-phi_infty(s)| <= C_K q^(1-2 sigma)`.  The missing inputs are a
  coset-level matching map, N1's cancellation-stable depth bound, escaping
  localization, and an N3/N4 `k^2`-weighted tail estimate.  No negation of M3
  is proved here.

The endpoint `sigma=3/2` must remain visible.  In the Chebyshev scaling model,
the value sum is harmonic there (`log q`); differentiating in `s` inserts a
second logarithm.  This blocks promotion by the present route to a pure
`q^(1-2 sigma)` bound at that endpoint unless an additional cancellation
theorem is supplied.  This is a sticking point, not a counterexample.

## 1. Receipts (run before numerical use)

### 1.1 Harvested P-chain: local v26 check

Command actually run:

```text
(cd projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle \
  && lake env lean RateCore.lean); lean_rc=$?; echo EXIT=$lean_rc
```

Output:

```text
RateCore.lean:263:32: warning: unused variable `hq`

Note: This linter can be disabled with `set_option linter.unusedVariables false`

RateCore.lean:415:31: warning: unused variable `hlam`

Note: This linter can be disabled with `set_option linter.unusedVariables false`
EXIT=0
```

The harvested v26 file is the authoritative corrected artifact.  In
particular, use `cpow_neg_two_s_bound'`, not the disproved unconditional
statement.  The v27 harvest (`RateCoreII.lean`) records the proved
`wordMatrix_two_form`, `c_two_even`, and `theta_coset_count`; it does not prove
the word-to-double-coset matching map or the Ford theorem.  A fresh v27
invocation from its result tree attempted to clone the absent Mathlib package
and hit the network restriction; this note relies on the existing v27 harvest
receipt and does not misreport that failed rerun as a new verification.

### 1.2 Beta-prefactor and `|s|` bounds on `K15`

The following Arb calculation was run with the permitted environment:

```text
/Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import arb, ctx
ctx.prec=256
sig=arb('1.1')
M=arb.pi().sqrt()*(sig-arb('.5')).gamma()/sig.gamma()
minus_Mprime=M*(sig.digamma()-(sig-arb('.5')).digamma())
sm=(arb('1.5')**2+arb('15')**2).sqrt()
print('M_1p1_upper=',M.upper())
print('minus_Mprime_1p1_upper=',minus_Mprime.upper())
print('s_abs_upper=',sm.upper())
print('two_s_abs_upper=',(2*sm).upper())
PY
```

Output:

```text
M_1p1_upper= [2.774501918484055737859139776264637993504487999315072019106777588813259132138 +/- 1.23e-76]
minus_Mprime_1p1_upper= [3.098742069462425336242065191121271267612792047538092514175376421133134176616 +/- 2.02e-76]
s_abs_upper= [15.07481343168133540532889736913936428041753520503956593585924244599273684733 +/- 2.03e-75]
two_s_abs_upper= [30.14962686336267081065779473827872856083507041007913187171848489198547369466 +/- 3.77e-75]
```

All rounded constants used below are outward: `M0 < 2.775`,
`M1 < 3.099`, `S := sup_K |s| < 15.075`, and `2S < 30.150`.

The products used for the normal-family bounds were also evaluated directly:

```text
/Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import arb, ctx
ctx.prec=192
M=arb('2.774501918484055737859139776264637993504487999315072019106777588813259132138')
Mp=arb('3.098742069462425336242065191121271267612792047538092514175376421133134176616')
print('M_times_12=',(12*M).upper())
print('Mp_times_12=',(12*Mp).upper())
print('M_times_120=',(120*M).upper())
print('sum=',(12*Mp+120*M).upper())
PY
```

Output:

```text
M_times_12= [33.2940230218086688543096773151756559220538559917808642293 +/- 6.44e-57]
Mp_times_12= [37.1849048335491040349047822934552552113535045704571101701 +/- 1.58e-56]
M_times_120= [332.940230218086688543096773151756559220538559917808642293 +/- 8.48e-56]
sum= [370.125135051635792578001555445211814431892064488265752463 +/- 3.10e-56]
```

For the displayed Arb radii, use the deliberately outward operational
constants `D0 < 12.001` and `D1 < 120.001`; with `M0 < 2.775` and
`M1 < 3.099` this gives:

```text
/Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import arb, ctx
ctx.prec=192
M=arb('2.775'); Mp=arb('3.099')
D=arb('12.001'); Dp=arb('120.001')
print('M0safe_times_D=',(M*D).upper())
print('M1safe_times_D_plus_M0safe_times_Dp=',(Mp*D+M*Dp).upper())
PY
```

Output:

```text
M0safe_times_D= [33.3027750000000000000000000000000000000000000000000000000 +/- 1.37e-56]
M1safe_times_D_plus_M0safe_times_Dp= [370.193874000000000000000000000000000000000000000000000000 +/- 1.51e-55]
```

### 1.3 Ford tail and log-tail arithmetic

For `sigma=1.1` and `X=1`, the same permitted Arb environment gives:

```text
/Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import arb, ctx
ctx.prec=192
sig=arb('1.1'); p=2*sig; d=p-2
R=sig/(sig-1)
L=2*(p-1)/(d*d)
print('R_sigma1p1_X1=',R.upper())
print('L_sigma1p1_X1=',L.upper())
print('D_abs_bound=',(1+R).upper())
print('Dprime_abs_bound=',(2*L).upper())
PY
```

Output:

```text
R_sigma1p1_X1= [11.0000000000000000000000000000000000000000000000000 +/- 5.10e-57]
L_sigma1p1_X1= [60.0000000000000000000000000000000000000000000000000 +/- 4.08e-56]
D_abs_bound= [12.0000000000000000000000000000000000000000000000000 +/- 5.10e-57]
Dprime_abs_bound= [120.000000000000000000000000000000000000000000000000 +/- 8.16e-56]
```

The growth exponent needed if one tried to force the *raw* Ford tail alone
below `q^(1-2 sigma)` was also evaluated:

```text
/Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import arb, ctx
ctx.prec=128
for sig in [arb('1.1'),arb('1.25'),arb('1.5')]:
 print(sig, ((2*sig-1)/(2*sig-2)).upper())
PY
```

Output:

```text
[1.1000000000000000000000000000000000000 +/- 2.36e-39] [6.0000000000000000000000000000000000000 +/- 4.71e-38]
1.2500000000000000000000000000000000000 3.0000000000000000000000000000000000000
1.5000000000000000000000000000000000000 2.0000000000000000000000000000000000000
```

## 2. Ford packing gives a compact-uniform normal family

Write

\[
 D_\Gamma(s):=\sum_{[\gamma]\in\Gamma_\infty\backslash\Gamma/\Gamma_\infty,
                    \,c_\gamma\ne0}|c_\gamma|^{-2s},
 \qquad \phi_\Gamma(s)=M(s)D_\Gamma(s).
\]

The Ford referee note proves, at paper level and uniformly in the Hecke
parameter after width-one conjugation,

\[
 A_\Gamma(X):=\#\{[\gamma]:0<|c_\gamma|\le X\}\le X^2\qquad(X\ge1).
 \tag{F}
\]

The hypotheses are discreteness, non-elementarity, and exact cusp stabilizer
`<S>`; the note sources these to Shimizu/precise invariance and the standard
Hecke-family facts.  The bound counts PSL **double** cosets with
multiplicity; no integer-grid assumption is used.  This is paper-level: the
Lean formalization of Shimizu and the cylinder injection remains open.

Let `p:=2 sigma>2`.  Stieltjes summation applied to (F) gives the strict-tail
bound

\[
 R_\sigma(X):=\sum_{|c_\gamma|>X}|c_\gamma|^{-2\sigma}
 \le {\sigma\over\sigma-1}X^{2-2\sigma}.                 \tag{2.1}
\]

The derivative series needs a log-weighted version.  With
`f(t)=log(t)t^{-p}`, `-f'(t) <= (p log(t)+1)t^{-p-1}` for `t>=1`; hence

\[
\begin{aligned}
L_\sigma(X)&:=\sum_{|c_\gamma|>X}\log|c_\gamma|\,|c_\gamma|^{-2\sigma}\\
 &\le X^{2-2\sigma}\left[
 {\sigma\over\sigma-1}\log X
 +{2\sigma-1\over2(\sigma-1)^2}\right].       \tag{2.2}
\end{aligned}
\]

The possible atom `|c|=1` contributes to (2.1) but contributes zero to (2.2).
At the lower edge of `K15`, use the outward-rounded operational constants
from §1.3; they therefore give

\[
 |D_\Gamma(s)|<12.001,
 \qquad |D_\Gamma'(s)|<120.001.                    \tag{2.3}
\]

These bounds hold for every finite-q group and for the theta endpoint, under
the Ford hypotheses.

### 2.1 Beta-integral control of `M(s)` (including all `t`)

For `Re(s)>1/2`,

\[
 M(s)=B(s-\tfrac12,\tfrac12)
 =\int_0^1 u^{s-3/2}(1-u)^{-1/2}\,du.              \tag{2.4}
\]

Taking absolute values removes the oscillatory factor
`exp(it log u)`:

\[
 |M(\sigma+it)|
 \le \int_0^1u^{\sigma-3/2}(1-u)^{-1/2}\,du=M(\sigma).
\]

The integrand decreases pointwise as `sigma` increases, so

\[
 \sup_{s\in K_{15}}|M(s)|=M(1.1)<2.775.            \tag{2.5}
\]

Equality is attained at `s=1.1`, so this is a genuine supremum statement,
not a point sample.  Differentiating (2.4) under the integral gives

\[
M'(s)=\int_0^1(\log u)u^{s-3/2}(1-u)^{-1/2}\,du,
 \quad
 \sup_{K_{15}}|M'(s)|\le -M'(1.1)<3.099.            \tag{2.6}
\]

The dominating function
`|log u|u^{1.1-3/2}(1-u)^(-1/2)` is integrable, so this differentiation is
legitimate uniformly on the rectangle.

The monotonicity in (2.6) follows from the pointwise decrease of
`(-log u)u^{sigma-3/2}`.  This handles the full `t`-dependence of `M`, rather
than importing the single-cell value at `1.1+1.5i`.

Combining (2.3), (2.5), and (2.6),

\[
 \sup_{K_{15}}|\phi_\Gamma(s)|<33.303,
 \qquad
 \sup_{K_{15}}|\phi_\Gamma'(s)|<370.194.            \tag{2.7}
\]

The two rounded products in (2.7) were evaluated from the displayed Arb
receipts.  Since `K15` is convex, integrating the derivative along the
segment from `s` to `z` gives the explicit equicontinuity estimate
`|phi_Gamma(s)-phi_Gamma(z)| < 370.194 |s-z|` for every `s,z in K15`.
These are only compact-uniform normal-family bounds, not a RATE estimate.

### 2.2 Unconditional finite-prefix reduction and certified-net extension

For `X>=1`, let

\[
 D_\Gamma^{\le X}(s):=
 \sum_{0<|c_\gamma|\le X}|c_\gamma|^{-2s},
 \qquad
 P_q(X):=\sup_{s\in K_{15}}
 |D_q^{\le X}(s)-D_\infty^{\le X}(s)|.
\]

No matching map is needed for this definition.  Splitting both absolutely
convergent series at `X`, applying (2.1) to each strict tail, and then using
(2.5) proves the unconditional paper-level reduction

\[
 \boxed{
 \sup_{s\in K_{15}}|\phi_q(s)-\phi_\infty(s)|
 \le M(1.1)\{P_q(X)+22X^{-1/5}\}.}
 \tag{2.8}
\]

Thus Ford packing completely settles the passage from a finite-prefix bound
to the whole rectangle.  It does not bound `P_q(X)`.  For example, choosing
`X=q^6` makes the proved two-tail contribution in braces equal to
`22q^{-6/5}`, but the required estimate for `P_q(q^6)` is exactly where the
coset-level M1, N1, and escaping/weighted-sum inputs enter.

**THEOREM (conditional compact-uniform modulus).**  If proved quantities
`X_q>=1` and `p_q>=P_q(X_q)` are supplied, then

\[
 \varepsilon(q):=M(1.1)\{p_q+22X_q^{-1/5}\}
\]

satisfies `|phi_q(s)-phi_infty(s)|<=varepsilon(q)` simultaneously for every
`s in K15`.  If additionally `X_q` tends to infinity and `p_q` tends to zero,
then `varepsilon(q)` tends to zero.  The antecedent is the unresolved part;
the implication is proved by (2.8).

There is also a rigorous finite-net extension.  Put
`F_q:=phi_q-phi_infty`.  Equation (2.7) gives

\[
 \sup_{K_{15}}|F_q'(s)|<2(370.126).                  \tag{2.9}
\]

If `Z` is an `r`-net of the convex rectangle `K15` and every value on `Z` is
enclosed by certified interval arithmetic, integration along the line
segment from a nearest net point gives

\[
 \sup_{s\in K_{15}}|F_q(s)|
 \le \max_{z\in Z}|F_q(z)|+2(370.126)r.             \tag{2.10}
\]

Equation (2.10), together with outward-rounded enclosures at the net points,
is a continuum certificate.  An uncertified point sample is not.  The
displayed product receipt in §1.2 supplies the rounded constant; no D-data
value is used.

## 3. Conditional comparison reduction on `K15`

Assume temporarily a **coset-level** matching map at cutoff `X`, with matched
pairs represented by the same reduced word.  In (3.8), `M_q(X)` means pairs
whose two endpoint magnitudes are both at most `X`; a one-sided endpoint below
`X` whose partner is above `X` is charged to the corresponding escaping core
mass.  For one retained pair put

\[
 x:=|c_w(\lambda_q)|,\qquad y:=|c_w(2)|,
 \qquad \delta_w(s):=x^{-2s}-y^{-2s}.
\]

The pair is matched only when `x,y>0`.  The absolute-value map is Lipschitz,
so P3 and P5 give

\[
 |x-y|\le(2-\lambda_q)\sup_{[\lambda_q,2]}|c_w'|
 \le {\pi^2\over q^2}\sup_{[\lambda_q,2]}|c_w'|.       \tag{3.1}
\]

The harvested v26 P4 theorem applies on `K15` because `sigma>=1.1>-1/2`:

\[
 |\delta_w(s)|
 \le2|s|\,m^{-2\sigma-1}|x-y|,
 \qquad m:=\min(x,y).                                \tag{3.2}
\]

If N1 were supplied with a constant `A`,

\[
 \sup_{[\lambda_q,2]}|c_w'|\le A k_w^2x,                \tag{N1}
\]

then, with `rho_w:=m/x=min(1,y/x)`, (3.1)--(3.2) become the explicit
per-term value bound

\[
 |\delta_w(s)|
 \le {2S A\pi^2\over q^2}
 k_w^2x^{-2\sigma}\rho_w^{-(2\sigma+1)}.              \tag{3.3}
\]

The candidate `A=11/20` remains **CONJECTURAL**; no value of `A` is inserted
as a proved constant here.

### 3.1 The `s`-derivative of one drift term

For positive `x,y`, differentiation is literal (real logarithms):

\[
 \partial_s\delta_w(s)
 =-2(\log x)x^{-2s}+2(\log y)y^{-2s}.                 \tag{3.4}
\]

Set `g_s(u):=-2(\log u)u^{-2s}`.  Then

\[
 g_s'(u)=(4s\log u-2)u^{-2s-1}.
\]

For `u>=1`, `s\in K15`, and `m=min(x,y)`, `M=max(x,y)`, the real-variable
mean-value integral gives

\[
 |g_s(x)-g_s(y)|
 \le(2+4S\log M)m^{-2\sigma-1}|x-y|.                 \tag{3.5}
\]

Using (3.1) and (N1), write `kappa_w:=max(1,y/x)` so that
`M=x kappa_w` and `m=x rho_w`.  The fully explicit derivative counterpart of
(3.3) is

\[
 |\partial_s\delta_w(s)|
 \le {A\pi^2\over q^2}k_w^2x^{-2\sigma}
 \rho_w^{-(2\sigma+1)}
 \left[2+4S\{\log x+\log\kappa_w\}\right].             \tag{3.6}
\]

For the actual prefactored term `h_w(s):=M(s)\delta_w(s)`,

\[
 |h_w'(s)|\le M1|\delta_w(s)|+M0|\partial_s\delta_w(s)|. \tag{3.7}
\]

Thus the derivative requires a log-weighted version of the matched `k_w^2`
sum.  It is not legitimate to differentiate a value bound and silently keep
the same constant.

### 3.2 What the Ford tail does and does not close

For any putative finite-cutoff matching decomposition,

\[
\begin{aligned}
 |\phi_q(s)-\phi_\infty(s)|
 \le M0\bigg(&\sum_{w\in\mathcal M_q(X)}|\delta_w(s)|
 +E_q(X,\sigma)+E_\infty(X,\sigma)\\
 &+R_\sigma^{(q)}(X)+R_\sigma^{(\infty)}(X)\bigg),       \tag{3.8}
\end{aligned}
\]

where `E_q,E_infty` are the unpaired core masses.  Ford supplies the last
two terms by `R_sigma(X)` in (2.1), uniformly in `q`; it does **not** supply a
`q`-decay estimate for `E_q`, `E_infty`, or the matched sum in (3.3).

In particular, applying Ford to the raw tail alone would require

\[
 X(q,\sigma)\ \gtrsim\ q^{(2\sigma-1)/(2\sigma-2)}
\]

to make `R_sigma(X(q,sigma))` have the target `q^(1-2 sigma)` size.  The
receipts evaluate this exponent as `6` at `sigma=1.1`, `3` at `sigma=1.25`,
and `2` at `sigma=1.5`.  No source note proves the required matching or
weighted drift control at such a moving cutoff.

The exact conditional assembly is therefore: if one proves, for
`1.1<=sigma<1.5`,

\[
 \sum_{w\in\mathcal M_q}k_w^2x_w^{-2\sigma}
       \rho_w^{-(2\sigma+1)}
 \le B_0(\sigma)q^{3-2\sigma},                         \tag{W0}
\]

and proves `q^(1-2 sigma)` bounds for the two escaping masses and the
moving-cutoff drift tail (with the analogous log-weighted bound for (3.6)),
then (3.3) yields

\[
 |\phi_q(s)-\phi_\infty(s)|
 \le M0\,[2SA\pi^2B_0(\sigma)+B_E(\sigma)]q^{1-2\sigma}. \tag{3.9}
\]

Equation (3.9) is a theorem-grade algebraic reduction **conditional on**
N1, coset-level M1, escaping localization, and the N3/N4 weighted estimate.
Those hypotheses are not proved by Ford or by v26/v27.

## 4. The `sigma=3/2` transition and derivative loss

The R2 depth model uses the formal weight `k^2 c^{-2 sigma}`.  If the
Chebyshev-like branch has `k` and `c` of the same order up to the elliptic
cutoff `k<q`, its value sum is modeled by

\[
 \sum_{m<q}m^{2-2\sigma}.
\]

The elementary integral-test regimes are:

\[
\begin{array}{c|c|c}
\sigma<3/2 & q^{3-2\sigma} & q^{1-2\sigma}\text{ after }2-\lambda_q\\
\sigma=3/2 & \log q & q^{-2}\log q\\
\sigma>3/2 & O(1) & O(q^{-2}).
\end{array}
\]

The derivative formula (3.6) adds `log m`.  The corresponding middle row is
`q^{-2}(log q)^2`, and the subcritical row acquires one factor `log q`.
These are scaling diagnostics, not certified bounds: proving (W0), the
escaping estimate, and the matched ratio control is precisely the open N1/M1/
N3/N4 work.  Therefore the pure M3 rate is left **CONJECTURAL**, not
refuted.

## 5. Remaining promotion gates

1. **Coset-level M1:** define and prove a well-defined, injective, sufficiently
   onto matching of `(c,d mod c)` classes.  v27's word collision refutation
   shows why a word-level injectivity axiom is unusable; `c_two_even` and
   `theta_coset_count` are only theta-side scaffolding.
2. **N1:** prove (N1) on the matched coset normal form, or replace it by a
   different cancellation-stable derivative envelope.
3. **Escaping localization:** prove a q-decaying bound for `E_q+E_infty`; a
   q-uniform Ford mass bound is insufficient.
4. **N3/N4 weighted tail:** prove (W0) and its log-weighted derivative version,
   including the correct transition at `sigma=3/2`.  The raw Ford tail (2.1)
   is an input to this proof, not a substitute for it.
5. **Only then** insert the explicit beta constants (2.5)--(2.7), certify the
   remaining weighted suprema by interval arithmetic, and dispatch the final
   compact-set algebra to Lean.

**Status:** M3 remains **OPEN / CONJECTURAL**.  The completed artifact is the
compact-uniform reduction, the exact `M(s)` and `M'(s)` controls, the
log-weighted Ford tail, and the explicit per-term drift/`s`-derivative
formulae above.  No D-data calibration or RATE promotion is used.

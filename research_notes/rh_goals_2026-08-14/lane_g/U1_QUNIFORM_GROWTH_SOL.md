# U1 q-uniform growth: exact elliptic obstruction to the transfer-operator route

**Date:** 2026-08-25

**Status:** UNREFEREED

**Author:** gpt-5.6-sol via codex

## Executive result

The required scalar normal-family statement U1 is **not proved here**. The
natural transfer-operator derivation does not close it: after the controlled
Hurwitz/parabolic tail is separated, a fixed interior matrix coefficient and
the absolute branch mass of the canonical full cyclic factor of the order-`q`
elliptic generator have exact size

\[
  \Theta_K\!\left(q^{\,1-2\Re s}\right)
  \quad (\Re s<\tfrac12),
\]

locally uniformly for `s` in compact subsets of `Re(s)<1/2`. In particular, at
the theta-anchor point

\[
  s_\infty=\frac{\rho_1}{2}
  =\frac14+i\,7.067362570867346895\ldots,
\]

a fixed interior matrix coefficient of the elliptic block is asymptotic to a
**nonzero** constant times `q^(1/2-2it_infinity)`, so its modulus is
`Theta(q^(1/2))`. The corresponding absolute branch mass is also
`Theta(q^(1/2))`. At `Re(s)=1/2` the absolute mass is `Theta(log q)`; it is
`O(1)` only for `Re(s)>1/2`.

This proves that a termwise or nuclear majorant which dominates that full cyclic
factor cannot establish U1 without a further cancellation/regularization. It does
**not** prove that U1 itself is false: U1 concerns the scalar Selberg zeta
`Z_{G_q}`, and a Fredholm determinant can remain bounded despite growth of an
operator block. The exact remaining obligation is stated in §6.

## 1. Precise statement of U1

### 1.1 Source-state correction

The three files mandated in the task do **not** contain a literal definition
labelled `U1`:

- `plans/wayfinder/rh-goals/tickets/family-law-theorem.md` ends with the
  2026-08-19 closure correction and disclaims a `q`-uniform error;
- `plans/wayfinder/rh-goals/tickets/law-tail-anchor-probe.md` ends at the original
  `(T2)` formulation;
- `LAW_TAIL_SCOPING.md` contains `(T1)`--`(T3)`, not `(T2')` or `U1`.

The first explicit U1 is in `LAW_T2_DETERMINANT.md` §§3.2, 5.2. Its later,
strictly weaker and currently operative form is `U1-min` in
`LAW_MINIMAL_HYPOTHESES.md` §4. I state both so that the norm and the claimed
uniformity are not silently changed.

### 1.2 Original U1 / `(T2'-a)`

There should exist `Q_1` and an open connected domain `Omega_tilde` joining
`s_infinity` to a set with an accumulation point in the Euler-product region,
together with `A,B<infinity` independent of `q`, such that

\[
  |Z_{G_q}(s)|\le A\exp\!\bigl(B(1+|s|)^2\bigr)
  \qquad(q\ge Q_1,\ s\in\widetilde\Omega).
  \tag{U1-original}
\]

This is stronger than Vitali--Hurwitz needs.

### 1.3 Minimal U1 actually consumed by Vitali--Hurwitz

Let `t_infinity=Im(s_infinity)`. Introduce explicit boundary slack. It is enough
that there exist

\[
  0<r<R<\frac14,\qquad r<\delta\le\frac12,\qquad
  \sigma_R\ge3.5,\qquad Q_1<\infty,
\]

all independent of `q`, and the connected rectangle

\[
  \widetilde\Omega
  :=\left\{s:\ \frac14-R<\Re s<\sigma_R+1,
             \ |\Im s-t_\infty|<\delta\right\},
  \tag{1.1}
\]

such that, for every compact `K'` contained in `Omega_tilde`,

\[
  \sup_{q\ge Q_1}\|Z_{G_q}\|_{K'}<\infty,
  \qquad
  \|f\|_{K'}:=\sup_{s\in K'}|f(s)|.
  \tag{U1-min}
\]

Thus:

- the norm in U1 is the **scalar compact-open sup norm in the spectral variable
  `s`**;
- uniformity is over the integer sequence `q>=Q_1`, equivalently over
  `lambda_q=2cos(pi/q)`;
- the constants may depend on the compact `K'`, but not on `q`;
- U1 is **not** a claim that `sup_q ||L_{q,s}||` is finite in an operator norm,
  and it makes no claim for a continuous interval of `lambda` values.

The closed disc `closed D(s_infinity,r)` lies **strictly** in (1.1), with
horizontal slack `R-r` and vertical slack `delta-r`, while the same connected domain
reaches the region `Re(s)>=3.5`, where the banked Euler-product convergence gives
the accumulation set needed by Vitali. If U1-min holds, Hurwitz supplies a zero
within radius `r` and hence an off-line margin `1/4-r>0`.

`LAW_MINIMAL_HYPOTHESES.md` §4 prints the left edge as `1/4-r` while also saying
that the **closed** radius-`r` disc is contained in the open rectangle. Those two
clauses are incompatible at the leftmost point of the disc. The auxiliary
`R>r` above is the conservative repair; it changes no method and can be chosen
arbitrarily close to `r`.

## 2. The transfer operator and the only honest decomposition

Put

\[
  \theta_q=\frac\pi q,\qquad
  \lambda_q=2\cos\theta_q,\qquad
  R_q=ST_{\lambda_q}
     =\begin{pmatrix}0&-1\\1&\lambda_q\end{pmatrix},
\]

and `psi_n(z)=-1/(z+n lambda_q)`. Then `psi_1=R_q`, and

\[
  R_q^q=-I,
\]

so `R_q` has order exactly `q` in `PSL(2,R)`. At `lambda=2`,

\[
  R_\infty^k=
  \begin{pmatrix}1-k&-k\\k&1+k\end{pmatrix},
\]

and the same generator is parabolic of infinite order.

For the usual weight-`s` action

\[
  (\tau_s(g)f)(z)=\bigl((cz+d)^2\bigr)^{-s}f(gz),
  \qquad g=\begin{pmatrix}a&b\\c&d\end{pmatrix},
  \tag{2.1}
\]

the formal first-return/fast alphabet separates into:

1. the full branches `|n|>=2`; their `n`-sum is a finite combination of
   Hurwitz-zeta terms and is already controlled uniformly in `q` on the banked
   continuation domain;
2. excursions through the partial branches `psi_{+1}` and `psi_{-1}` before an
   exit through `|n|>=2`. Here `psi_1=R_q`; `psi_{-1}=ST_{-lambda_q}` is the
   conjugate negative orientation, not literally `R_q^(-1)`. Formally the
   positive orientation contains the factor

   \[
     \mathcal E_{q,s}^{\pm}
       =\sum_{k=0}^{q-1}\tau_s(R_q^{\pm k}).
     \tag{2.2}
   \]

   Equation (2.2) is the **maximal full cyclic factor**. Exact first-return
   incidence may omit, redistribute, or couple its terms to exit branches.
   Therefore (2.2) is a precise obstruction to the full-orbit induced candidate,
   not an assertion that every MMS block is literally equal to this sum.

This is the only honest sense in which the operator is decomposed here. There is
no single unreduced fixed-disc operator on a `q`-independent Banach space:
`R_q` is elliptic with unit-modulus fixed-point multiplier, so an inclusion
`R_q(closed D) compactly contained in D` would force an attracting fixed point
by Schwarz--Pick, a contradiction. The reduced MMS spaces avoid that failure by
using `Theta(q)` Markov components; their dimension therefore changes with `q`
and tends to a countably infinite partition at `lambda=2`.

Consequently, an expression such as `sup_q ||L_{q,s}||` is not even well posed
until a common space and embeddings are supplied. The computation below shows
that the most natural common-space candidate would in any case have an
unbounded elliptic block.

## 3. The controlled parabolic `k`-sum

Use the fixed interior point `z_0=1/2`, which lies in
`[-lambda_q/2,lambda_q/2]` for every `q>=4`. At the endpoint `lambda=2`,

\[
  (c_kz_0+d_k)^{-2s}
  =\left(1+\frac32k\right)^{-2s}.
\]

Thus one orientation of the parabolic excursion sum is exactly

\[
  \sum_{k=0}^{\infty}\left(1+\frac32k\right)^{-2s}
  =\left(\frac23\right)^{2s}\zeta\!\left(2s,\frac23\right).
  \tag{3.1}
\]

The reverse orientation gives, up to its fixed projective phase (and exactly in
absolute value), the companion Hurwitz shift `1/3`. Formula (3.1)
converges absolutely for `Re(s)>1/2` and has the standard meromorphic
continuation past that line. This is the banked truncated-`zeta(2s)` mechanism.
In particular, its continued value at `s_infinity` is finite. Nothing in this
section causes `q`-growth.

The subtlety is that the finite-`q` elliptic orbit is an honest finite sum,
whereas (3.1) at `Re(s)=1/4` exists only after continuation. Limit in `q` and
continuation in `s` need not commute. They do not commute here.

## 4. Exact contribution of the order-`q` elliptic generator

### 4.1 Exact finite-`q` formula

The Chebyshev formula for the powers of `R_q` is

\[
  R_q^k=\frac1{\sin\theta_q}
  \begin{pmatrix}
    -\sin((k-1)\theta_q)&-\sin(k\theta_q)\\
     \sin(k\theta_q)& \sin((k+1)\theta_q)
  \end{pmatrix}.
  \tag{4.1}
\]

It is checked at `k=0,1` and follows for all `k` from
`R_q^2=lambda_q R_q-I`. Applying (2.1) to the constant function `1` and
evaluating at `z_0=1/2` gives the exact elliptic orbit coefficient

\[
  \Xi_q(s)
  :=(\mathcal E_{q,s}^{+}\mathbf1)(z_0)
  =\sum_{k=0}^{q-1}
   \left(
    \frac{\sin\theta_q}
    {\frac12\sin(k\theta_q)+\sin((k+1)\theta_q)}
   \right)^{2s}.
  \tag{4.2}
\]

Every base inside the power in (4.2) is positive, so the logarithm and the
complex power have no branch ambiguity.

### 4.2 Asymptotic theorem

For every compact `K` contained in `{Re(s)<1/2}`, uniformly for `s in K`,

\[
  q^{2s-1}\Xi_q(s)\longrightarrow C(s),
  \tag{4.3}
\]

where

\[
  C(s)
   =\left(\frac{2\pi}{3}\right)^{2s}
     \frac{\Gamma(\frac12-s)}{\sqrt\pi\,\Gamma(1-s)}.
  \tag{4.4}
\]

**Derivation.** Multiply (4.2) by `q^(2s-1)`:

\[
 q^{2s-1}\Xi_q(s)
 =(q\sin\theta_q)^{2s}\frac1q\sum_{k=0}^{q-1}
 \left[
   \frac12\sin(k\theta_q)+\sin((k+1)\theta_q)
 \right]^{-2s}.
 \tag{4.5}
\]

Away from the two endpoints, the summand tends to
`[(3/2)sin(pi x)]^(-2s)` with `x=k/q`, while `q sin(theta_q)` tends to `pi`.
The endpoint singularity is integrable exactly when `Re(s)<1/2`. For completeness,
put

\[
 D_{q,k}:=\tfrac12\sin(k\theta_q)+\sin((k+1)\theta_q),\qquad
 m_{q,k}:=1+\min(k,q-1-k).
\]

The elementary inequality
`2 min(x,1-x) <= sin(pi x) <= pi min(x,1-x)`, applied once from each endpoint,
gives the explicit conservative constants `c_0=1` and `C_0=3pi/2` (for
`q>=4`):

\[
 \frac{m_{q,k}}q\le D_{q,k}\le
 \frac{3\pi}{2}\frac{m_{q,k}}q
 \qquad(0\le k<q).
 \tag{4.5a}
\]

Indeed, after replacing each sine by its distance from the nearer endpoint,
the weighted distance `d(k)/2+d(k+1)` lies between
`m_{q,k}/2` and `3m_{q,k}/2`; the sine inequality supplies the displayed
constants.

If `K` is compact in `Re(s)<1/2`, choose
`sigma_+<1/2` with `Re(s)<=sigma_+` on `K`, and put
`alpha=max(sigma_+,0)<1/2`. Because every `D_{q,k}` is positive,
the chosen logarithm is real and
`|D_{q,k}^{-2s}|=D_{q,k}^{-2 Re(s)}`. The portion with `D_{q,k}>1` is uniformly
bounded because `s` ranges in `K` and has no endpoint singularity. On the
portion with `D_{q,k}<=1`, (4.5a) bounds both endpoint tails of the normalized
Riemann sum by a constant times

\[
 \frac1q\sum_{m\le\varepsilon q}(m/q)^{-2\alpha}
 \le C_K\varepsilon^{1-2\alpha}.
 \tag{4.5b}
\]

The displayed tail tends to zero uniformly in `q` as `epsilon` tends to zero.
On the remaining
bulk interval ordinary Riemann sums converge uniformly in `s in K` because the
summand and its `s`-derivatives are uniformly continuous there. Splitting into
the two endpoint tails and the bulk proves local uniform convergence, rather
than merely pointwise convergence. Therefore

\[
 \int_0^1\sin(\pi x)^{-2s}\,dx
 =\frac{\Gamma(\frac12-s)}{\sqrt\pi\,\Gamma(1-s)}.
\]

Substitution in (4.5) yields (4.3)--(4.4). Since the gamma function has no
zeros and neither gamma factor has a pole at `s_infinity`, `C(s_infinity)` is
nonzero.

Therefore

\[
  \Xi_q(s_\infty)
  =C(s_\infty)q^{1/2-2it_\infty}(1+o(1)),
  \qquad
  |\Xi_q(s_\infty)|
  =|C(s_\infty)|q^{1/2}(1+o(1)).
  \tag{4.6}
\]

This is not merely a triangle-inequality artefact: even the complex orbit sum
itself has a nonzero `sqrt(q)` leading term.

### 4.3 Absolute operator-majorant size

Taking absolute values term by term in (4.2), for fixed real `sigma<1/2`, gives

\[
 q^{2\sigma-1}\sum_{k=0}^{q-1}
 \left|
    \frac{\sin\theta_q}
    {\frac12\sin(k\theta_q)+\sin((k+1)\theta_q)}
 \right|^{2\sigma}
 \longrightarrow
 \left(\frac{2\pi}{3}\right)^{2\sigma}
 \frac{\Gamma(\frac12-\sigma)}{\sqrt\pi\,\Gamma(1-\sigma)}.
 \tag{4.7}
\]

Thus the absolute excursion mass is

\[
 \begin{cases}
   \Theta(q^{1-2\sigma}),&\sigma<1/2,\\
   \frac43\log q+O(1),&\sigma=1/2,\\
   O(1),&\sigma>1/2.
 \end{cases}
 \tag{4.8}
\]

At the anchor abscissa `sigma=1/4`, the exact leading constant in (4.7) is

\[
  \sqrt{\frac23}\,\frac{\Gamma(1/4)}{\Gamma(3/4)},
  \tag{4.9}
\]

so the absolute mass is `Theta(sqrt(q))`. At the leftmost point of the closed
Hurwitz disc, `sigma=1/4-r`, the exponent is

\[
  1-2\sigma=\frac12+2r.
  \tag{4.10}
\]

The surrounding open corridor extends to `Re(s)>1/4-R`, so its worst exponent
on compacts can approach, but never attain, `1/2+2R`.

Hence the order-`q` contribution is polynomially unbounded everywhere in the
part of the U1 corridor with `Re(s)<1/2`; it is not `O(1)` there.

### 4.4 Trivial numerical spot-check (not used in the proof)

Using `/Users/za/.venvs/farey-rh/bin/python` at 50 decimal digits gave

\[
 |C(s_\infty)|=0.307228834413700331\ldots,
 \qquad
 \sqrt{\frac23}\frac{\Gamma(1/4)}{\Gamma(3/4)}
 =2.41574811889345596\ldots.
\]

For `q=64,128,...,2048`, the scaled complex sum in (4.3) approached (4.4),
and the absolute mass divided by `sqrt(q)` rose from `2.3064...` to
`2.3964...`, toward (4.9). These are midpoint checks only, not interval
certificates, and no conclusion depends on their last digits.

## 5. Consequences for U1

### 5.1 What fails

Suppose, contrary to the known geometric obstruction, that the operators
`mathcal E_{q,s}` acted on one `q`-independent Banach space of holomorphic
functions which contains `1`, and evaluation at `z_0=1/2` had a
`q`-independent continuous norm. Then

\[
 \|\mathcal E_{q,s_\infty}\|
 \ge
 \frac{|(\mathcal E_{q,s_\infty}\mathbf1)(z_0)|}
      {\|\operatorname{ev}_{z_0}\|\,\|\mathbf1\|}
 \asymp q^{1/2}.
 \tag{5.1}
\]

So this full cyclic factor cannot be locally bounded in such a common-space
operator norm at the anchor. A
triangle/nuclear majorant fails by the stronger absolute estimate (4.7).
Together with the nonexistence of a common invariant disc and the `Theta(q)`
growth of the reduced Markov partition, this closes the naive operator-norm
route negatively.

### 5.2 What does not follow

Equation (5.1) is **not** a counterexample to U1-min. U1-min asks for
`|Z_{G_q}(s)|`, not `||mathcal E_{q,s}||`. The exact MMS identity also contains
sector products and its Fredholm correction determinant; a Fredholm determinant
may exhibit cancellations not visible in a branch norm or in one matrix
coefficient. No inequality of the form

\[
 |Z_{G_q}(s_\infty)|\ge c\,|\Xi_q(s_\infty)|
\]

is known or asserted. Existing finite-`q` determinant probes are mixed and are
not certificates. Therefore the honest conclusion is obstruction to the
derivation, not failure of the scalar theorem.

There are two other “elliptic sizes” in the lane which must not be conflated
with (4.2):

- the order-`q` cone factor in the Selberg functional equation is an
  `s <-> 1-s` ratio and has modulus exactly `1` on `Re(s)=1/2`; its claimed
  off-line asymptotic still has a banked Euler--Maclaurin remainder obligation;
- the trace-formula elliptic mass is `Theta(log q)`, not `Theta(sqrt(q))`.

They concern different objects. Neither cancels (4.6) at the operator level
without an additional identity.

## 6. Exact remaining obligation

The minimal unresolved statement is precisely:

> Choose `r,R,delta,sigma_R,Q_1` satisfying §1.3. Prove that for every compact
> `K'` contained in `Omega_tilde` there is `A(K')<infinity`, independent of
> `q`, with
> \[
>   \sup_{q\ge Q_1}\sup_{s\in K'}|Z_{G_q}(s)|\le A(K').
> \]

Any transfer-operator proof of this statement must additionally do **all** of
the following:

1. specify a `q`-comparable operator/space or work directly at determinant
   level, because the reduced MMS spaces have `Theta(q)` components and the
   naive fixed-disc space does not exist;
2. identify how the **exact** MMS incidence acts on the cyclic factor (2.2), and
   then prove that omission/redistribution removes the contribution, prove that
   it cancels the nonzero term `C(s) q^(1-2s)` from (4.3), or supply a legitimate
   holomorphic determinant-level regularization, uniformly on compact subsets
   of the connected corridor;
3. prove that the regularized determinant is the Selberg zeta `Z_{G_q}` with
   the correct MMS sector/correction factor;
4. retain the already banked uniform Hurwitz-tail control.

Equivalently, a proof may bypass operators and establish U1-min directly, for
example through a scattering-determinant estimate in the still-open strip
`3/4<Re(s)<1` together with the missing horizontal-edge control. What is not
enough is an `O(q^a)` majorant with any `a>0`: normalizing by such a factor makes
the known Euler-region limit zero, so Vitali--Hurwitz no longer transports the
nonzero theta zeta.

## Verdict

VERDICT: PARTIAL-with-obligation

The parabolic/Hurwitz part is controlled, and the canonical full cyclic
order-`q` factor is proved to be `Theta(q^(1-2 Re(s)))`
(`Theta(sqrt(q))` at `s_infinity`), so any termwise operator majorant containing
that factor fails. Exact MMS incidence and the scalar compact-open bound U1-min
remain unproved and are the obligations in §6.

## What a referee must check

1. **Source/version mismatch:** confirm that the three mandated files indeed
   contain no literal U1 and that `LAW_T2_DETERMINANT.md` plus
   `LAW_MINIMAL_HYPOTHESES.md` are the intended current definitions; check the
   boundary-slack repair in §1.3 against the printed source.
2. **Operator convention:** verify the slash action (2.1), the sign/projective
   convention for `R_q`, the conjugacy used for the negative digit, and how the
   exact fast-operator incidence contains or redistributes the elliptic factor
   (2.2).
3. **Power formula:** check (4.1), especially `R_q^q=-I`, and the exact
   evaluation (4.2) at `z_0=1/2`.
4. **Uniform asymptotic:** supply a fully written dominated-improper-Riemann-sum
   proof of local uniformity in (4.3), including endpoint domination and the
   chosen holomorphic branch in `s`.
5. **Boundary cases:** check the coefficient `4/3` at `Re(s)=1/2` and the
   `O(1)` assertion for the absolute mass when `Re(s)>1/2`.
6. **Norm implication:** do not apply (5.1) unless the proposed common Banach
   space contains `1` and has `q`-uniform evaluation norm at `z_0`; the existing
   reduced spaces do not automatically supply this.
7. **Determinant identity:** verify the exact general-`q` MMS identity,
   including sector multiplicities and the Fredholm correction determinant,
   before inferring anything about `Z_{G_q}` from an operator determinant.
8. **No overreach:** the growth of one operator block does not prove growth of
   `Z_{G_q}`. A referee should demand either the cancellation/regularization in
   §6 or a direct compact-open zeta bound before promoting U1.
9. **Numerics:** the two decimal constants in §4.4 are non-rigorous midpoint
   checks only; recompute with interval arithmetic if they are to be quoted as
   certified bounds.

## Principal repo sources used

- `plans/wayfinder/rh-goals/tickets/family-law-theorem.md`
- `plans/wayfinder/rh-goals/tickets/law-tail-anchor-probe.md`
- `research_notes/rh_goals_2026-08-14/lane_g/LAW_TAIL_SCOPING.md`
- `research_notes/rh_goals_2026-08-14/lane_g/LAW_T2_DETERMINANT.md`, especially
  §§2.2--2.3, 3.2, 5.2
- `research_notes/rh_goals_2026-08-14/lane_g/LAW_U1_GROWTH.md`, especially §§1,
  3--6 and its correction/addendum notices
- `research_notes/rh_goals_2026-08-14/lane_g/LAW_MINIMAL_HYPOTHESES.md`, §4
- `research_notes/rh_goals_2026-08-14/lane_g/LAW_U1EFF_ENTRYWISE.md`
- `research_notes/rh_goals_2026-08-14/lane_g/LAW_INDUCED_FEASIBILITY.md`, §4

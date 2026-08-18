# R3/R5 assembly plan for the `(RATE)` effectivization program

**Status: RESEARCH STRATEGY ONLY. No R3 theorem and no numerical `q0` are
claimed.** All proposed analytic bridges that are not already supplied by the
named sources are marked **`CONJECTURAL`**. The intended output is a proof
obligation stack, not a promotion of the R2/R4 measurements.

**Date:** 2026-08-18. **Lane:** G. **Role:** R3 strip transport and R5
effective-threshold design.

## 0. Decisive reading

At the specified height there are two logically sound R3 abstractions. The
shorter, target-specific one is a **right-half-plane Rouche transport** of the
known theta-limit zero

```text
z_0 = (1+rho_1)/2 = 3/4+i t0.
```

Indeed, the formula

```text
phi_infty(s)
 = sqrt(pi) Gamma(s-1/2) zeta(2s-1)
   / [Gamma(s) zeta(2s) (4^s-1)]
```

has `zeta(2z_0-1)=zeta(rho_1)=0`, while the other displayed factors are
regular there. A boundary-uniform RATE estimate can therefore be propagated
from `Re s=sigma_R` to a small contour about `z_0`; Rouche then gives a finite
`phi_q` zero already in `Re s>1/2`. This is Candidate A0 below and is the
preferred R3 route for this particular `t0`. Its effective constants are not
yet proved, so the route remains **`CONJECTURAL`**.

The general fallback is a **conditional transport inside Hejhal's zero-free
contradiction**, not an unconditional convergence theorem on the critical
line.

For every finite, one-cusp Hecke group,

```text
|phi_q(1/2+it)| = 1.
```

For the theta limit, `phi_infty` is the `(infinity,infinity)` entry of a
two-cusp scattering matrix, not a scalar determinant, and at
`t0 = gamma_1/2` it has modulus about `0.338537`. Therefore, for every finite
`q`,

```text
|phi_q(1/2+it) - phi_infty(1/2+it)|
    >= ||phi_q(1/2+it)| - |phi_infty(1/2+it)||
    =  ||phi_infty(1/2+it)| - 1|.                         (0.1)
```

Thus an **unconditional critical-line** estimate tending to zero is
impossible. The fallback R3 route must instead assume

```text
H0(q,delta): phi_q has no zero in
R_delta^+ = [1/2,1/2+delta] x [t0-delta,t0+delta],
```

derive a *conditional* upper bound smaller than the right side of (0.1), and
thereby refute `H0`. Failure of `H0` supplies the zero in Hejhal's right-hand
rectangle; (7.22) supplies the reflected pole. This is exactly the role of the
two ineffective Vitali steps in the §7 proof skeleton
(`LAW_HEJHAL_S7_EXTRACT.md:62-99`).

Any R3 statement that omits `H0` and nevertheless claims
`phi_q-phi_infty -> 0` on `Re s = 1/2` is **`CONJECTURAL AND FALSE IN THIS
NORMALIZATION`**. Candidate A0 does not make that claim: it transports only
to a compact contour strictly inside `Re s>1/2`.

## 1. Fixed notation and constant ledger

Choose the following before proving anything.

| Name | Definition | Present status |
|---|---|---|
| `gamma_1` | first nontrivial zeta-zero ordinate, `14.13472514173469...` | explicit numerical anchor |
| `t0` | `gamma_1/2 = 7.067362570867346...` | exact target definition |
| `t_meas` | `7.0665` | rounded rate-sweep height; `t0-t_meas = 8.625708673...e-4` |
| `delta` | Hejhal rectangle parameter, `0 < delta < 1` | owner choice; R4 sampled `0.1, 0.5` |
| `sigma_R` | right RATE line `1+eta`; current draft uses `1.1` | `eta=0.1` in R2 |
| `alpha` | decay exponent in `E_R(q) <= C_R q^(-alpha)` | **`CONJECTURAL`**; R2 proposes `alpha=2 sigma_R-1`, hence `1.2` at `1.1` |
| `C_R` | proved, target-height, boundary-uniform RATE constant | **missing**; it is not the R2 single-cell calibration |
| `q_RATE` | first integer from which the proved R2 envelope holds | missing |
| `B_H` | `5+y0`, `y0 >= 1000`, from Ch.6 §12 | source-defined |
| `K_12.4` | `(1+sqrt(2)) B_H^2` | printed Prop. 12.4 bound; if a common `y0=1000` is legitimate, it is about `2.438416e6` |
| `C_6` | Hejhal Lemma 7.7 strip bound | effective in shape, not instantiated family-uniformly |
| `C_7` | Hejhal Lemma 7.9 logarithmic-integral constant | source-named, not transcribed numerically |
| `C_12.9` | collection of hidden constants in Thm 12.9(b)-(d) | missing; depends on `Gamma, chi, F, delta_p` |
| `omega_q(t)` | `1 + sum_rho 2 eta_H/(eta_H^2+(t-gamma)^2)` | printed; only integral-growth shape is extracted |
| `r_theta` | `sqrt(pi^2/2-1/4) = 2.164440389...` | Roelcke/Hejhal printed theta spectral-gap constant |
| `d_delta` | `inf_{|t-t0|<=delta/20} ||phi_infty(1/2+it)|-1|` | must be interval-certified; R4 currently has sampled witnesses only |
| `z_0` | `(1+rho_1)/2 = 3/4+i t0` | exact theta-entry zero used by Candidate A0 |
| `r_z` | rational contour radius with `D(z_0,r_z)` inside the right-half propagation domain | missing geometry choice |
| `m_z` | `min_{|s-z_0|=r_z}|phi_infty(s)|` | must be interval-certified positive |

The Roelcke bound `r_theta >= 2.164440` is useful for excluding low theta
eigenparameters in domain bookkeeping. It does **not** provide a local divisor
clearance at `t0 about 7.067`, because a lower bound on the first spectral
parameter says nothing about spacing near a higher target. Using it as the
entire `t0` pole/zero-clearance proof would be **`CONJECTURAL`**.

### 1.1 The exact R2 input contract

R3 must consume a proved compact-boundary statement, not a point sample:

```text
E_R(q)
 := sup_{s in Gamma_R} |phi_q(s)-phi_infty(s)|
 <= C_R(sigma_R,T_R) q^(-alpha),             q >= q_RATE,       (R2*)
```

where `Gamma_R` is the full right boundary needed by the chosen R3 domain and
`T_R >= t0 + delta + buffer`. The current R2 formula is

```text
epsilon_2(q;s) = |M(s)| [Delta_X(q,s)+E_q(X,sigma)
                         +E_theta(X,sigma)+T_X(q,sigma)],
M(s) = sqrt(pi) Gamma(s-1/2)/Gamma(s).                         (1.1)
```

R2's M3 gap is exactly the passage from its one validated cell
`s=1.1+1.5i` to `(R2*)`. A constant labelled `C(1.1,1.5)` cannot be used at
`t0`.

There is also an internal numerical obstruction to using the draft's
`C(1.1,1.5) <= 2.0`: the displayed assembled bounds give

| `q` | displayed `epsilon_2(q)` | `q^1.2 epsilon_2(q)` |
|---:|---:|---:|
| 24 | 0.2042 | 9.25 |
| 32 | 0.0973 | 6.23 |
| 48 | 0.0376 | 3.91 |

so `2.0 q^-1.2` does not majorize the displayed assembled envelope. The value
`2.0` appears compatible with the measured `D q^1.2`, not with the printed
one-sided `epsilon_2`. Until reconciled, `C_R=2.0` is **`CONJECTURAL`** and is
forbidden in R5.

## 2. Candidate strip-transport mechanisms

### Candidate A0 — direct right-half theta-zero transport: preferred at `t0`

**Status: `CONJECTURAL`; shortest target-specific route.**

Choose `r_z>0` so that the closed disc

```text
D_z = D(z_0,r_z),   z_0=3/4+i t0,
```

lies in `R_delta^+`, strictly in `Re s>1/2`, and avoids every other divisor
on its boundary. This requires `delta>1/4+r_z` for the rectangular geometry
used here, so the R4 choice `delta=0.5` can accommodate it. Interval-certify
`m_z=min_{boundary D_z}|phi_infty|>0`, the theta-zero count inside `D_z`, and
that both `phi_q` and `phi_infty` are holomorphic on the closed disc for every
`q>=q_divisor`. Here `q_divisor` activates a genuine no-pole certificate for
the original functions, not an unspecified pole-clearing modification;
boundary nonvanishing alone is not enough for Rouche.

Propagate `(R2*)` to `boundary D_z` by the finite-rectangle
Phragmen-Lindelof/two-constants estimate with Prop. 12.4 or fully explicit
Thm 12.9 bounds on the remaining boundary. If the resulting contour error is
less than `m_z`, Rouche gives the same nonzero zero count for `phi_q` in
`D_z`. Equation (7.22) then supplies the reflected pole. This route:

- never claims convergence on `Re s=1/2`;
- needs neither `H0` nor the inverse bound from Lemmas 7.9/7.10;
- needs no R4 critical-line defect `d_delta`;
- still needs M1/M2/M3 at the exact target-height boundary and a
  family-uniform Ch.6 bound.

The existence and local count of the theta zero follow from the displayed
formula only after the first zeta zero, all denominator nonvanishing, and the
chosen contour have been certified. Until that receipt and the uniform
transport constants exist, every effective assertion in this candidate is
**`CONJECTURAL`**.

### Candidate A — quantitative Hejhal contradiction: preferred general fallback

**Status:** standard analytic architecture; family-uniform constants and all
RATE inputs remain **`CONJECTURAL`**.

Use `F_q = phi_q-phi_infty`. First propagate `(R2*)` inside the open right
half-strip by a finite-rectangle two-constants/Phragmen-Lindelof estimate,
using Prop. 12.4 or a fully instantiated Thm 12.9 as the large boundary bound.
This makes Hejhal step 3 quantitative. Under `H0`, use (7.22), Lemmas 7.9 and
7.10 to obtain a `q`-uniform bound on a disc crossing `Re s=1/2`. Finally use
a second two-constants estimate on that disc to make the second Vitali step
quantitative.

Why preferred as the fallback/general-height construction:

- It follows the printed §7 proof rather than inventing a new spectral object.
- It uses the scalar finite-group functional identity only under `H0`.
- It turns the scalar/matrix boundary mismatch into the final contradiction.
- It needs only a positive propagation exponent, not a sharp one.

### Candidate B — one-shot reflected rectangle

**Status: `CONJECTURAL`, potentially shorter than A.**

Try to prove a uniform lower bound

```text
m_q^+ := inf_{1/2 <= sigma <= 1/2+a, |t-t0|<=H} |phi_q(s)| >= m_+ > 0
                                                                  (2.1)
```

under `H0`. Equation (7.22) would then give an explicit left-strip upper
bound `|phi_q| <= 1/m_+`, allowing a one-shot harmonic-measure estimate for
`F_q` across the line.

The problem is that right-half closeness degenerates as `sigma -> 1/2`, while
mere nonvanishing gives no quantitative `m_+`. Proving (2.1) requires a
Harnack/log-integral argument essentially equivalent to Hejhal 7.9/7.10 or to
Candidate C. Candidate B is acceptable only if (2.1) is independently proved;
otherwise it silently assumes the hardest part.

### Candidate C — Blaschke `V_q` / `omega_q` / Harnack route

**Status: source-supported mechanism, q-family use `CONJECTURAL`.**

Props. 12.5-12.8 provide a bounded Blaschke-type function `V_q`, its
functional equation and product, while

```text
omega_q(t) = 1 + sum_rho 2 eta_H/(eta_H^2+(t-gamma)^2) >= 1,
integral_{-R}^R omega_q(t) dt = O(R^4).
```

Possible use: under `H0`, factor the known divisors, apply Harnack/Poisson
control to `log|V_q|`, obtain (2.1) or a direct quantitative normal-family
modulus, and then reflect.

Required before this route is real:

1. instantiate every Thm 12.9 big-`O` constant;
2. prove `q`-uniform control of `Gamma_q, chi_q, F_q, eta_H, delta_p`;
3. prove a pointwise or window-averaged bound for `omega_q` near `t0`;
4. compare the finite one-cusp Blaschke factor with the theta two-cusp entry
   without confusing entry, matrix and determinant divisors;
5. show that the divisor factorization does not assume the zero whose
   existence R5 is trying to prove.

The extracted `integral omega = O(R^4)` with an unspecified, group-dependent
constant is insufficient at the fixed target height. A good-height argument
inside the `delta/20` window could be used instead of exact `t0`, but only
after R4 supplies a continuous defect lower bound throughout that window.

### Candidate D — chain of discs / Hadamard three-circle

**Status: `CONJECTURAL` but mechanically explicit fallback.**

After Candidate A has produced a `q`-uniform bound on a reflected disc, cover
a path from the right-half RATE seed disc to the line by overlapping discs and
iterate the three-circle inequality. This replaces an abstract quantitative
Vitali theorem by elementary steps. It is robust and easy to formalize, but
the product of propagation exponents can be extremely small, making `q0`
astronomical. Use it as a proof fallback and a numerical upper-bound baseline,
not as the first optimization target.

### Candidate E — direct Rouché transport at `s_infty=rho_1/2`

**Status: separate, stronger route; currently `CONJECTURAL`.**

Pole-clear `phi_q-phi_infty`, or switch to the Selberg-zeta difference, and
transport a right-half estimate to a contour about
`s_infty=1/4+i t0`. Rouché then moves the theta pole/zero count directly. This
is the route-A/U1-eff program in `LAW_SH_EFFECTIVIZATION_SKELETON.md:73-99,
161-175`, not the minimal Hejhal R3.

It requires a `q`-uniform order-two growth bound outside the Ch.6 strip and,
for the Selberg-zeta version, the still-open U3 scattering-pole-to-zeta-zero
identification. Prop. 12.4, whose domain begins at `Re s=1/2`, cannot by itself
reach `Re s=1/4`.

### Candidate F — resolvent/operator route

**Status: `CONJECTURAL`, not recommended now.**

A common-space norm-resolvent estimate through the one-cusp to two-cusp
degeneration could imply scattering convergence with a rate. None of the read
sources supplies the common Hilbert space, a `q`-uniform resolvent norm, or the
matrix-to-scalar identification. The Roelcke lower bound does not fill those
gaps.

### Non-R3 bypass — winding/positivity

Route B in `LAW_SH_EFFECTIVIZATION_SKELETON.md:102-135` bypasses strip
transport and U1 entirely. Its final inequality has the *shape*
`c0(T) log q` for the winding lower bound against shallow/deep off-window pole
mass, but the source leaves the density constant `0<C<1` and the
`O(1)`, `O((log Q)^(3/4))` remainders non-explicit. Therefore the effective
leading coefficient and threshold are **`CONJECTURAL`**; only the B4
positivity input is explicit. The named blocker remains a `q`-uniform
`o(log q)` upper bound for the deep resonance count. Keep it as the fallback
if the R3 propagation exponent makes the analytic `q0` useless.

## 3. R3 constructions in exact interfaces

Everything in this section is **`CONJECTURAL`** until its listed gates are
proved.

### R3.0 Preferred target-specific interface: Candidate A0

Let `Omega_z` be a rational finite propagation domain whose right boundary is
`Gamma_R`, which contains the closed contour `boundary D_z`, and on whose
other boundary pieces `|F_q|<=K_+` is proved. Both scattering functions must
be certified to have no poles anywhere on the closure of the propagation
region. If instead one uses a common nonvanishing multiplier, its effect on
the zero count must be proved explicitly; separate pole-clearing factors are
not interchangeable with Rouche on the original functions.
Let `nu(z)` be the harmonic measure of `Gamma_R` in `Omega_z` and define

```text
nu_z = inf_{s in boundary D_z} nu(s) > 0,
C_Z  = K_+^(1-nu_z) C_R^nu_z,
p_Z  = alpha nu_z.                                        (3.0a)
```

The finite-domain two-constants theorem gives the contour estimate

```text
sup_{s in boundary D_z}|phi_q(s)-phi_infty(s)|
    <= K_+^(1-nu_z) [C_R q^(-alpha)]^nu_z
     = C_Z q^(-p_Z).                                      (3.0b)
```

Here `K_+`, `C_R`, `alpha`, and `nu_z` must all be positive, explicit, and
independent of `q` after their named activation thresholds. Top and bottom
edges of `Omega_z` are part of `K_+`; Prop. 12.4/Thm 12.9 cannot be invoked
outside their transcribed domains.

If interval arithmetic proves

```text
m_z = min_{s in boundary D_z}|phi_infty(s)| > 0
```

and (3.0b) is strictly less than `m_z`, Rouche proves that `phi_q` and
`phi_infty` have the same number of zeros in `D_z`. The theta-limit count must
be established by an interval argument-principle computation; simplicity of
`rho_1` must not be silently assumed. This is the complete R3 output for the
preferred route. It bypasses R3.3-R3.5.

### R3.1 Geometry and divisor clearance

Choose nested domains with rational endpoints:

```text
R_delta^+ = [1/2,1/2+delta] x [t0-delta,t0+delta],
B_delta   = [1/2-delta/10,1/2+delta/10]
            x [t0-delta/2,t0+delta/2],
D_0       = D(1/2+i t0, delta/15),
D_1       = D(1/2+i t0, delta/20).
```

Choose a right-half seed disc `D_+` with closure contained in
`D_0 intersect {Re s>1/2}` and a finite right propagation rectangle joining
`D_+` to `Gamma_R subset {Re s=sigma_R}`.

Certify:

- `phi_infty` has no pole or zero on every domain where `F_q` is treated as
  holomorphic;
- `H0` covers the closed right rectangle and every boundary/reflected piece
  needed by (7.22); a boundary zero already proves the desired alternative;
- the target domains stay right of the simple theta pole at
  `1/4+i t0` (in particular any reflected half-width must be `<1/4`);
- the Thm 12.9 exclusions `|s-s_k|>=delta_p` hold with an explicit
  `delta_p>0`;
- (7.22) is used in its exact conjugation convention. For real target heights,
  its reflected point has the same `t`; do not silently replace it by a raw
  `phi(s)phi(1-s)=1` formula with an untracked sign change.

### R3.2 First propagation: make Hejhal step 3 quantitative

Let `K_+` be a proved `q`-uniform bound for `|F_q|` on all non-RATE boundary
pieces of the right propagation rectangle. Candidate value:

```text
K_+ <= K_q,+ + K_infty,+,
K_q,+ <= K_12.4 = (1+sqrt(2)) B_H^2,                        (3.1)
```

provided Prop. 12.4 is transcribed in the exact conjugated normalization and
shown uniform in `q`. Otherwise `K_+` remains a named unknown.

Let `nu(z)` be the harmonic measure of `Gamma_R` in that rectangle. For a
compact anchor/seed set `S_+`, put

```text
nu_+ = inf_{z in S_+} nu(z) > 0.
```

The two-constants theorem gives

```text
E_+(q;S_+) := sup_{z in S_+}|F_q(z)|
 <= K_+^(1-nu_+) [C_R q^(-alpha)]^nu_+.                    (3.2)
```

The finite-height top and bottom edges must be included in `K_+`; an infinite
strip PL invocation is not allowed unless its vertical-growth hypotheses are
proved from Thm 12.9.

Choose a Hejhal anchor

```text
s_a = 1/2 + a_a + i t0,       0 < a_a < delta,
m_infty,a = |phi_infty(s_a)| > 0,
nu_a = nu(s_a).
```

The pair `(a_a,delta)` is admissible only after interval certification of
`m_infty,a>0` and all divisor exclusions. In particular,
`delta=0.5, a_a=delta/2=0.25` is **forbidden as a lower-bound anchor**:
then `s_a=z_0` and `phi_infty(s_a)=0`. That point is the Rouche target of
Candidate A0, not a valid anchor for Candidate A. Activate the lower bound on
`phi_q(s_a)` once

```text
K_+^(1-nu_a) [C_R q^(-alpha)]^nu_a < m_infty,a/2.          (A)
```

Then `|phi_q(s_a)| >= m_infty,a/2`.

### R3.3 Zero-free reflection and the printed 7.9/7.10 bound

Assume `H0(q,delta)`. Boundary zeros must also be excluded; if one exists,
the desired zero is already obtained.

Use (7.22) to extend `phi_q` across the line in `B_delta`. Apply Lemma 7.9 to
the normalized function `phi_q/C_6`, using the anchor lower bound from (A),
and retain the exact output as

```text
M_H = M_7.23(delta,t0,C_6,C_7,m_infty,a/2),                (3.3)
```

where `M_H` is the explicit upper bound for the normalized
`double-integral log^+` after the source's conformal rescaling. **No coefficient
inside `M_7.23` may be guessed; it must be transcribed from (7.23).**

Let `r_H<1` be the normalized radius corresponding to `D_0`. The candidate
transcription of Lemma 7.10 is the conditional disc bound

```text
K_H = C_6 exp(2 M_H/(1-r_H)^2),
sup_{D_0}|phi_q| <= K_H.                                  (3.4)
```

The coefficient and normalization in (3.4) remain **`CONJECTURAL`** until
the exact Lemmas 7.9/7.10 and equation (7.23) are checked in the underlying
source, not merely in the present extracts.

Also interval-certify

```text
K_infty,0 = sup_{D_0}|phi_infty|,
K_F = K_H + K_infty,0.                                    (3.5)
```

This is the exact place where the Prop. 12.4/Thm 12.9 bookkeeping enters the
second Vitali replacement. Calling `K_H` explicit before `C_6,C_7,M_H,r_H`
are instantiated is **`CONJECTURAL`**.

### R3.4 Second propagation: quantitative Vitali

Use (3.2) on the seed disc `D_+`:

```text
E_seed(q) <= K_+^(1-nu_seed) [C_R q^(-alpha)]^nu_seed.     (3.6)
```

Set `U = D_0 minus closure(D_+)`. Let

```text
omega(z) = harmonic_measure_U(z, boundary D_+),
omega_*  = inf_{z in D_1, Re z=1/2} omega(z) > 0.          (3.7)
```

Apply the two-constants theorem to `log|F_q|` on `U` with `E_seed` on the
inner boundary and `K_F` on the outer boundary:

```text
E_3(q)
 := sup_{z in D_1, Re z=1/2}|F_q(z)|
 <= K_F^(1-omega_*) E_seed(q)^omega_*

 <= C_3 q^(-p_3),                                         (3.8)

p_3 = alpha nu_seed omega_*,
C_3 = K_F^(1-omega_*)
      K_+^(omega_*(1-nu_seed))
      C_R^(omega_* nu_seed).
```

All domains, `nu_seed` and `omega_*` are geometry-only and can be enclosed by
interval arithmetic. If an implementation returns only floating harmonic
measures, (3.8) remains **`CONJECTURAL`**.

### R3.5 Contradiction and R3 output

R4 must prove

```text
d_delta
 := inf_{|t-t0|<=delta/20} ||phi_infty(1/2+it)|-1|
 > 0.                                                       (R4*)
```

The current `0.6604` is a sampled-grid witness, not `(R4*)`.

Under `H0`, (3.8), finite-group unitarity and (0.1) give simultaneously

```text
d_delta <= |F_q(1/2+it)| <= E_3(q).
```

Therefore

```text
E_3(q) < d_delta                                           (C)
```

refutes `H0`. The R3 theorem should state only this conditional implication:

> If `(R2*)`, the divisor/domain gates, (A), (3.3)-(3.8), and `(R4*)` hold,
> then every finite `q` satisfying (C) has a zero of `phi_q` in
> `R_delta^+`, hence a reflected pole in the left rectangle by (7.22).

It must not state unconditional convergence on the critical line.

## 4. What R3 requires from M2 and M3

| Mechanism | M2 requirement | M3 requirement | Extra requirement |
|---|---|---|---|
| Candidate A0, preferred at `t0` | a proved finite-`q` and theta-side tail majorant feeding `C_R`; all Ch.6 constants used in `K_+` must be family-uniform | uniform `(R2*)` on the entire right boundary of `Omega_z`, with `T_R>=t0+r_z+buffer`; explicit sups of `|M(s)|`, `2|s|`, and every tail ratio | interval-certified `m_z`, theta zero count, `nu_z`, and divisor clearances |
| Candidate A, general fallback | same M2 RATE input; if `C_6` is rebuilt from Ch.6 §12, all hidden 12.9 constants must also be family-uniform | uniform `(R2*)` on the entire right boundary, with `T_R>=t0+delta+buffer`; explicit sups of `|M(s)|`, `2|s|`, and every tail ratio | `C_7`, harmonic measures, divisor clearances, continuous R4 defect |
| Candidate B | same `C_R`; M2 does not itself provide the inverse bound (2.1) | uniformity on a right slab, not one point | independent Harnack/minimum-modulus theorem |
| Candidate C | M2 plus uniform `Gamma,chi,F,eta_H,delta_p` bookkeeping for Thm 12.9 and both finite/theta divisor products | pointwise or window-uniform `omega_q(t)` and exponential-height factors | scalar-entry/matrix/determinant compatibility |
| Candidate D | same as A | same as A | many explicit disc-overlap exponents |
| Candidate E | right boundary RATE can reuse M2 | compact-boundary uniformity | U1 order-two growth; U3 for zeta version; pole-clearing polynomial |
| Winding bypass | none of R2 M2 if derived directly from trace formula | none of R2 M3 | explicit B3 remainder and `o(log q)` deep-count bound |

The current M2 formula

```text
T(X,sigma) = X^(2-2 sigma) [1/(sigma-1)+2/X]
```

is only a candidate conditional on corrected M2.L, G1 and G2, and it covers
the finite side and theta side through different counting inputs. It also
bounds tail size, not the `q`-dependent drift split. Treating it as a proved
`C_R` would be **`CONJECTURAL`**.

M3 is not a cosmetic grid extension. Phragmen-Lindelof/harmonic measure needs
uniform control on whole boundary arcs. At minimum M3 must deliver:

```text
sup_{|t-t0|<=T_R, s on Gamma_R} epsilon_2(q;s)
    <= C_R q^(-alpha),
```

with `C_R`, `alpha`, `q_RATE`, truncation `X(q)` and monotonicity all proved.

## 5. R5: exact assembly inequality and integer threshold

### 5.0 Preferred Candidate-A0 pure-power assembly

Define the route-specific prerequisite threshold

```text
q_pre,Z = max(12,
              q_RATE,
              q_M1,
              q_M2,
              q_M3,
              q_C1,
              q_K+,
              q_divisor,
              q_geometry,
              q_monotone).                                (5.0a)
```

Here `q_K+` activates the family-uniform `K_+` bound on every non-RATE
boundary piece of `Omega_z`; the other constants have the meanings listed
below in Section 5.1. The non-`q` gates (theta zero count, `m_z>0`, domain
holomorphy, and certified geometry) must already be `PASS`; taking a maximum
of integer thresholds cannot encode a failed analytic premise. With
`C_Z,p_Z,m_z` from (3.0a), set

```text
q_Z = floor((C_Z/m_z)^(1/p_Z)) + 1,
q0^(Z) = max(q_pre,Z,q_Z).                                 (5.0b)
```

For every integer `q>=q0^(Z)`, the load-bearing R5 inequality is

```text
K_+^(1-nu_z) C_R^nu_z q^(-alpha nu_z)
    = C_Z q^(-p_Z)
    < m_z.                                                 (R5-Z)
```

Rouche then transfers the certified nonzero theta zero count in `D_z` to
`phi_q`. Every constant in `(R5-Z)` is named: `K_+` is the non-RATE boundary
bound, `nu_z` the minimum harmonic measure of `Gamma_R` on `boundary D_z`,
`C_R,alpha` the R2 rate data, and `m_z` the theta contour minimum. The
floor-plus-one makes the inequality strict even when the real threshold is an
integer.

### 5.1 Candidate-A pure-power fallback

Assume every prerequisite above is proved and the constants are independent
of `q` for `q>=q_pre,H`. Define

```text
A_A = 2 K_+^(1-nu_a) C_R^nu_a / m_infty,a,
p_A = alpha nu_a,

q_A = floor(A_A^(1/p_A)) + 1,                              (5.1)
```

so the strict anchor activation inequality (A) holds for all `q>=q_A`.
`q_A` activates only the anchor lower bound used to construct the conditional
`K_F`; it is not itself a separate bound on `K_F` or the reflected boundary.

Define from (3.8)

```text
A_C = C_3/d_delta,
p_C = p_3 = alpha nu_seed omega_*,

q_C = floor(A_C^(1/p_C)) + 1.                              (5.2)
```

The floor-plus-one is intentional: the needed inequality is strict. A bare
`ceil` is wrong when `A_C^(1/p_C)` is already an integer.

Let

```text
q_pre,H = max(12,
              q_RATE,
              q_M1,
              q_M2,
              q_M3,
              q_C1,
              q_K+,
              q_C6,
              q_C7,
              q_R4,
              q_divisor,
              q_geometry,
              q_monotone).                                 (5.3)
```

Here:

- `q_M1` activates the corrected coset-level matching/localization theorem;
- `q_M2` activates the finite and theta tail majorants;
- `q_M3` activates boundary-uniform RATE;
- `q_C1` activates the universal derivative envelope used by R2;
- `q_K+` activates the family-uniform non-RATE boundary bound;
- `q_C6` activates the family-uniform Ch.6 bound;
- `q_C7` activates the exact Lemmas 7.9/7.10 log-area constants;
- `q_R4` activates the interval-certified critical-line defect;
- `q_divisor` activates all pole/zero clearances;
- `q_geometry` fixes the common conjugated normalization and domains;
- `q_monotone` is the point from which all envelopes used above are proved
  monotone in the required direction.

Then the analytic threshold is exactly

```text
q0^(H) = max(q_pre,H, q_A, q_C).                            (R5-H)
```

For every integer `q>=q0^(H)`, assuming `H0` yields

```text
K_F^(1-omega_*)
K_+^(omega_*(1-nu_seed))
C_R^(omega_*nu_seed)
q^(-alpha omega_*nu_seed)
    < d_delta,                                              (5.4)
```

contradicting (0.1). Equation (5.4) is the load-bearing R5 assembly
inequality with every constant named.

### 5.2 Route selection

Let `J_proved` be the subset of `{Z,H}` whose complete prerequisites and
strict inequality have actually been proved. The final analytic threshold is

```text
q0_analytic = min {q0^(j) : j in J_proved}.                (5.5)
```

For the specified `t0`, route `Z` is preferred because it avoids the
critical-line scalar/matrix mismatch, the R4 defect interpolation, and the
Hejhal 7.9/7.10 inverse-bound layer. If `J_proved` is empty, the minimum is
**undefined** (equivalently `q0_analytic=+infinity`); a numerical `q0` must
not be reported. If route H uses the general envelope below, its entry in
`J_proved` is `q0^(H,env)` rather than `q0^(H)`.

### 5.3 General monotone-envelope case for route H

If R2 produces an explicit envelope `E_R(q)` rather than a pure power, or if
`K_F,nu_seed,omega_*` depend on `q`, do not force them into (5.2). Define

```text
E_3^up(q) = K_F(q)^(1-omega_*(q))
            K_+(q)^(omega_*(q)(1-nu_seed(q)))
            E_R(q)^(omega_*(q)nu_seed(q)),

q0^(H,env) = min {Q in integers, Q >= q_pre,H :
                  sup_{integer q>=Q} E_3^up(q) < d_delta}.  (5.6)
```

R5-H is effective only after the tail supremum in (5.6) is proved. Finite
sampling is not monotonicity evidence. If this set is empty, define
`q0^(H,env)=+infinity` and keep route H **`UNVERIFIABLE`**.

If only lower bounds are to be substituted, first certify

```text
0 < nu_0 <= nu_seed(q) <= nu_1 <= 1,
0 < omega_0 <= omega_*(q) <= omega_1 <= 1,
```

where `nu_1,omega_1` are named certified upper bounds. Then require, pointwise
for every integer `q>=q_pre,H`, positive envelopes satisfying

```text
E_R(q) <= K_+(q),
K_+(q)^(1-nu_0) E_R(q)^nu_0 <= K_F(q).                     (5.7)
```

Then the logarithm of `E_3^up` is nonincreasing separately in `nu_seed` and
`omega_*`, so replacing them by `nu_0,omega_0` gives a valid upper bound. If
either pointwise inequality in (5.7) is unavailable, maximize the displayed
log-bound over the full certified rectangle
`[nu_0,nu_1] x [omega_0,omega_1]` (its maximum is attained at a corner);
do not substitute lower bounds by intuition.

### 5.4 R4 interval loss for route H

If interval certification starts from the sampled value `d_samp=0.6604`, name
the total interpolation/numerical loss `Delta_4` and set

```text
d_delta = d_samp - Delta_4 > 0.
```

The actual threshold inequality is then

```text
E_3^up(q) + Delta_4 < 0.6604,                              (5.8)
```

not `E_3^up(q)<0.6604`. Direct Arb evaluation over the interval is preferable
to a grid-plus-Lipschitz estimate.

### 5.5 Meet in the middle with the finite base

Let `Q_cert` be the largest integer such that every target-class `q` below or
equal to it has a current, reopened, artifact-level resonance certificate.
Do not infer `Q_cert` from “done/assembled/mechanical” prose.

The full family assembly closes exactly when

```text
Q_cert >= q0_analytic - 1.                                 (5.9)
```

Otherwise the honest remaining finite gap is

```text
{q in target class : Q_cert < q < q0_analytic}.
```

Arithmetic `q` and any excluded theorem class must be specified before this
set is enumerated.

## 6. The named `t0` thin-margin risk

> ### `T0 THIN-MARGIN / EVALUATOR-COLLAPSE RISK`

This is presently the highest-risk R5 input, despite the apparently large
theta defect.

1. The exact target is `t0=7.067362570867...`; the RATE sweep used `7.0665`.
   The offset is small and lies inside the sampled R4 windows, but the two
   values are not interchangeable without M3.
2. Both `t=7.0665` q=64 rows have N-doubling disagreement about `2.5e-2`; the
   target-height rows are explicitly excluded from all slope claims. Thus the
   program currently has no trustworthy measured `C_R` or `alpha` at the
   height R5 needs.
3. R4's `0.6604` is a sampled-grid witness, not a continuous lower bound.
   This affects route H. Route Z avoids that defect but replaces it by the
   interval-certified contour margin `m_z`, which can itself be small if
   `r_z` is chosen too tightly.
4. Prop. 12.4's raw bound can be about `2.4e6`. Route Z dilutes the RATE
   exponent by `nu_z`; route H additionally exponentiates a log-area constant
   and dilutes it by `nu_seed omega_*`. Small harmonic measure turns modest
   uncertainty in `C_R`, `K_F`, `m_z`, or `d_delta` into orders of magnitude
   in `q0`.
5. For route H, the scalar mismatch saturates the margin: unconditionally
   `|F_q|>=d_delta` on the line. It succeeds only by proving the opposite
   inequality under `H0`; there is no spare conceptual margin for a
   normalization error between scalar entry, matrix or determinant. Route Z
   avoids this mismatch but must keep the whole Rouche contour strictly in
   `Re s>1/2`.
6. The R2 fixed-`X=50` assembly is explicitly not valid past `q=48` without
   growing `X`. Extrapolating it to the eventual `q0` would invalidate the
   threshold even if the transport algebra were correct.
7. At `delta=0.5`, the tempting fallback anchor
   `1/2+delta/2+i t0` is exactly `z_0` and has zero theta value. It cannot
   activate the Hejhal inverse bound. The same fact is useful only when
   treated as route Z's zero target with a positive contour minimum.

No numerical `q0` should be printed until all seven points have receipts.

## 7. Execution order and falsification gates

1. **Theta contour/defect gate.** For preferred route Z, interval-certify the
   theta zero count in `D_z`, `m_z>0`, and all contour divisor exclusions. For
   fallback route H, Arb-certify `(R4*)`, `m_infty,a>0`, `K_infty,0`, and all
   domain clearances at exact `t0`. `FAIL` a route if a required lower-bound
   interval contains zero. In particular reject the `delta=0.5,a_a=0.25`
   anchor for H.
2. **M3 target-height gate.** Recompute finite-q `phi_q` at
   `t0 +/- (delta+buffer)` with a pre-registered truncation-doubling tolerance.
   `FAIL` if any boundary cell is unconverged; do not fit a rate to failed
   cells.
3. **R2 theorem gate.** Close M1, M2, C1 and M3; emit a symbolic/interval
   `(R2*)` with `C_R,alpha,q_RATE,X(q)`. Reconcile the `C<=2` contradiction.
4. **Ch.6 constant gate.** Prove the exact family-uniform constants used by
   `K_+`. For route H, also transcribe `C_6,C_7,C_12.9` and the exact
   Lemmas 7.9/7.10 coefficients. If H fails, try Candidate C before building
   new resolvent machinery.
5. **R3 geometry gate.** For route Z, interval-compute `nu_z` and verify
   `D_z` and `Omega_z`; evaluate (3.0b). For route H, compute
   `nu_a,nu_seed,omega_*,r_H`, verify every domain inclusion and boundary
   orientation, then evaluate (A) and (3.8).
6. **R5 monotonicity gate.** Prove `(R5-Z)`, `(R5-H)`, or the tail supremum in
   (5.6). Compute the applicable `q_Z` or `q_A,q_C`, then (5.5), with strict
   integer handling.
7. **Finite-base gate.** Reopen each certificate in the gap below `q0`; record
   `Q_cert` only from current artifacts. Apply (5.9).
8. **Adversarial check.** Independently test the normalization, the `H0`
   quantifier, divisor removals, harmonic-measure inequality direction, and
   floor/ceiling arithmetic. Verdict must be `PASS`, `FAIL`, or
   `UNVERIFIABLE`.

## 8. Completion criterion

R3/R5 is theorem-ready only when the repository contains:

- a proved `(R2*)` on the exact target boundary;
- explicit, family-uniform Ch.6/Hejhal constants or a proved substitute;
- either a route-Z contour theorem `(R5-Z)`, or a conditional
  `H0 => E_3(q)` route-H theorem, with all divisors removed;
- an interval-certified `m_z>0` for route Z, or `d_delta>0` for route H;
- a monotone proof of the selected R5 inequality and the resulting integer
  `q0_analytic` from (5.5);
- artifact-level finite certificates through `q0_analytic-1`.

Until then the correct R5 verdict is **`UNVERIFIABLE: q0 UNDEFINED`**, not a
large guessed threshold.

## Sources consumed

- `LAW_SH_EFFECTIVIZATION_SKELETON.md`
- `LAW_R2_RATE_LEMMA_DRAFT.md`
- `LAW_R4_THETA_DEFECT.md`
- `LAW_HEJHAL_CH6S12_CH11S3_EXTRACT.md`
- `LAW_RATE_MEASURE.md`
- Adjacent definition checks: `LAW_HEJHAL_S7_EXTRACT.md`,
  `LAW_M2_TAIL_MAJORANT_DRAFT.md`, `RATE_NOTEGRAPH_REFEREE_AUDIT.md`

# `(SCAT-EVAL_q)` — exact scalar bridge, parity audit, and the lambda-slab test

**Date:** 2026-08-19
**Lane:** G / LAW effectivization
**Status:** **PARTIAL SOURCE THEOREM; `SCAT-EVAL_q` remains OPEN; all proof claims in this
note are AWAITING COLD REFEREE.**
**Scope:** determine exactly what can be obtained from MMS + Hejhal + Teo and the two
`zeta_cert_rosen{,_even}.py` engines, and whether a q-generic determinant on a continuous
lambda slab can replace the missing finite scalar evaluator.

This note does not promote a transfer determinant to the scalar scattering coefficient.
It also does not claim a full-H_0 interval evaluator.  Every item not explicitly sourced or
proved below remains **OPEN** or **CONJECTURAL**.

## 1. Verdict

There are two different uses of a scalar evaluator in the program.

1. The **finite H_0 pincer** needs a theorem-valid way to certify a scalar
   φ_q zero-minus-pole count if it is implemented literally as a scattering computation.
   This is a finite-block need.  It can instead be bypassed for an individual q by a
   theorem-valid Selberg-zeta determinant certificate: MMS identifies the Selberg zeta as a
   quotient of the two signed transfer determinants by the explicit `K_s` factor, and that
   factor is zero-free for `Re s > 0`.  The bypass still requires a general-q operator
   identification and a genuine determinant truncation theorem.
2. The **large-q tail route** does not logically need φ_q at all.  The proposed T2′ route is
   a sequence argument for the Selberg zeta functions `Z_{G_q}` (Vitali/Hurwitz), not a
   deformation in lambda and not a scalar scattering computation.  Its open obligations are
   U1/U2b/U3 in `LAW_T2_DETERMINANT.md`; replacing them by a scalar evaluator would not
   discharge those obligations.

The requested continuous lambda-slab replacement is not source-valid.  MMS's reduced
operators are q-specific reductions of the relation `(ST_q)^q = -I`; their component count
and block equations change with q and parity.  Between lambda values `lambda_q`, the relation
is absent.  The natural unreduced branch carrier has a different structural obstruction:
the `n=1` branch has elliptic multiplier of modulus one for every `lambda < 2` and is
parabolic at `lambda=2`, so no bounded invariant disc exists.  This is the proved Lemma
T2-A in `LAW_T2_DETERMINANT.md`, not a numerical failure.

**Consequence:** path A must be a sequence of q-specific, theorem-valid Selberg-zeta
certificates (or a separately proved Fourier/scattering evaluator).  A single
q-generic determinant homotopy over `[lambda_8,2)` cannot supply the missing bridge.

## 2. The exact source-level candidate

### 2.1 Initial scalar formula (Hejhal)

Hejhal §7, equation (7.5), as recorded in the primary-source extraction
`LAW_HEJHAL_S7_EXTRACT.md`, gives for the width-one conjugated finite Hecke group:

\[
 \phi_q(s)=\sqrt\pi\,\frac{\Gamma(s-1/2)}{\Gamma(s)}
 \sum_{[S]\backslash\mathcal G_q/[S],\ c\ne0}|c|^{-2s},
 \qquad \Re s>1.
\]

This is the true scalar scattering coefficient in its absolutely convergent half-plane.
It is not an analytic-continuation formula on the transport strip.  The extracted source
also records Hejhal Proposition 7.8 (Vitali continuation) and Theorem 7.11 (eventual
off-line zeros), but those statements are ineffective as printed.  In particular, the
source does not supply the finite-q interval continuation and derivative bounds required by
the H_0 pincer.

### 2.2 Selberg-zeta bridge (MMS + Teo)

MMS's primary-source receipt `Q7_MMS_PRIMARY_SOURCE_RECEIPT.md` identifies equation (34),
Theorem 4.10, Lemma 5.1, and Theorem 6.4.  The theorem used by the engines is

\[
 Z_{G_q}(s)=
 \frac{\det(1-L_{s,+}^{(q)})\det(1-L_{s,-}^{(q)})}
      {\det(1-K_{q,s})}.
 \tag{2.1}
\]

The `K` divisor is not optional.  `LAW_Q3_BRANCH_DIAGNOSIS.md` quotes MMS's theorem and
its spectrum proposition, yielding the exact product

\[
 \det(1-K_{q,s})=\prod_{n\ge0}(1-b_q^{s+n}),
 \qquad
 b_q=\prod_{\ell=0}^{\kappa_q-1} f_q^\ell(r_q)^2\in(0,1).
 \tag{2.2}
\]

Its zeros have `Re s` in `-N_0`; therefore it is zero-free on `Re s > 0`.  This zero-free
fact is enough to transfer a zero of the signed determinant numerator into a Selberg-zeta
zero in the right half-plane.  It is not by itself an identification with φ_q.

Teo Proposition 2.5, quoted in `LAW_TEO_KAPPA_CORRECTED.md`, gives

\[
 Z_{G_q}(1-s)=\kappa_q(s)Z_{G_q}(s),
 \qquad \kappa_q(s)=K_q^*(s)\,\phi_q(s),
 \tag{2.3}
\]

where `K_q^*` is the explicit elliptic/gamma/Barnes factor with
`Gamma_2=1/G`.  Solving (2.3) gives the exact candidate

\[
 \boxed{\quad
 \phi_q(s)=\frac{Z_{G_q}(1-s)}{Z_{G_q}(s)K_q^*(s)}.
 \quad}
 \tag{SCAT-EVAL}
\]

The formula is source-valid as a meromorphic identity, subject to the source's
normalization and continuation domains.  It becomes a **certified evaluator** only after
all three quantities on the right have interval enclosures, all denominator clearances
have been proved, and the determinant truncation error is bounded uniformly on a complex
neighborhood of the contour.  The current engines do not yet meet that last condition.

### 2.3 What the source does not identify

The MMS receipt explicitly says that MMS does not identify a Python/Hilbert realization
with the Banach transfer operator.  The q=5 R5 note supplies such a q=5-specific
common-continuation proof, and q=7 has a separate operator-binding chain.  Neither source
closes the same interface for all q.

Likewise, matching a determinant midpoint against a scalar formula, or matching a finite
polygon winding, is not a proof of (SCAT-EVAL).  The Q3 diagnosis found the missing `K_s`
factor by opening MMS; the numerical agreement was diagnostic evidence, not the source
identity itself.

## 3. Odd/even parity and the finite lambda-slab test

### 3.1 Exact integer data

The two engines encode the source's distinct parameterizations:

```text
$ /Users/za/.venvs/farey-rh/bin/python - <<'PY'
import math
for q in range(8,19):
    if q % 2:
        h=(q-3)//2; k=2*h+1; eq='(34) odd'
    else:
        h=(q-2)//2; k=h; eq='(32) even'
    lam=2*math.cos(math.pi/q)
    print(f'q={q:2d} parity={"odd" if q%2 else "even":4s} lambda={lam:.15f} h={h} kappa={k} equation={eq} block_dim={k}N')
PY
q= 8 parity=even lambda=1.847759065022573 h=3 kappa=3 equation=(32) even block_dim=3N
q= 9 parity=odd  lambda=1.879385241571817 h=3 kappa=7 equation=(34) odd block_dim=7N
q=10 parity=even lambda=1.902113032590307 h=4 kappa=4 equation=(32) even block_dim=4N
q=11 parity=odd  lambda=1.918985947228995 h=4 kappa=9 equation=(34) odd block_dim=9N
q=12 parity=even lambda=1.931851652578137 h=5 kappa=5 equation=(32) even block_dim=5N
q=13 parity=odd  lambda=1.941883634852104 h=5 kappa=11 equation=(34) odd block_dim=11N
q=14 parity=even lambda=1.949855824363647 h=6 kappa=6 equation=(32) even block_dim=6N
q=15 parity=odd  lambda=1.956295201467611 h=6 kappa=13 equation=(34) odd block_dim=13N
q=16 parity=even lambda=1.961570560806461 h=7 kappa=7 equation=(32) even block_dim=7N
q=17 parity=odd  lambda=1.965946199367804 h=7 kappa=15 equation=(34) odd block_dim=15N
q=18 parity=even lambda=1.969615506024416 h=8 kappa=8 equation=(32) even block_dim=8N
```

This is also visible directly in the source-bound code:

```text
$ nl -ba research_notes/rh_goals_2026-08-14/lane_g/law_probes/kaggle_boundary_rate/zeta_cert_rosen.py | sed -n '114,121p;214,232p'
    114  def hecke_params(q):
    115      if q % 2 == 0:
    116          hq = (q - 2) // 2
    117          kappa = hq
    118      else:
    119          hq = (q - 3) // 2
    120          kappa = 2 * hq + 1
    ...
    214      twoh = 2 * hq
    215      k_idx = kappa
    216      # (L g)_1 = L_2 g_{2h} + Linf_3 g_k ...
    225      # (L g)_i = L_1 g_{i-2} + Linf_2 g_k ...
    226      for i in range(3, k_idx + 1):
```

and for the even engine:

```text
$ nl -ba research_notes/rh_goals_2026-08-14/lane_g/law_probes/kaggle_boundary_rate/zeta_cert_rosen_even.py | sed -n '94,101p;228,238p'
     94  def hecke_params(q):
     95      if q % 2 == 0:
     96          hq = (q - 2) // 2
     97          kappa = hq
     98      else:
     99          hq = (q - 3) // 2
    100          kappa = 2 * hq + 1
    ...
    228  # ---- MMS eq.(32), even q (h = hq = kappa) ----
    229  # (L g)_1 = Linf_2 g_h + sign * Linf_{-1} g_h
    232  # (L g)_i = L_1 g_{i-1} + Linf_2 g_h ... , 2 <= i <= h
    233  for i in range(2, h + 1):
```

The odd sequence has `kappa=q-2`; the even sequence has `kappa=(q-2)/2`.  Thus a single
finite-dimensional block realization cannot be analytic in lambda across the alternating
sequence.  More importantly, the indexing is not a cosmetic choice: it is the Markov
resolution of the partial `n=±1` branch after imposing the finite-order elliptic relation.

### 3.2 The relation fails inside every lambda slab

Let

\[
 R(\lambda)=ST_\lambda=\begin{pmatrix}0&-1\\1&\lambda\end{pmatrix}.
\]

At `lambda=lambda_q=2 cos(pi/q)`, `R(lambda_q)^q=-I` in `SL_2`, which is the relation used
to obtain the q-specific MMS reductions.  For a generic lambda in the interval between two
successive group values, this relation is false.  The following direct recurrence computes
`tr(R^n)` (`tr(R^0)=2`, `tr(R^1)=lambda`, `tr(R^{n})=lambda tr(R^{n-1})-tr(R^{n-2})`):

```text
$ /Users/za/.venvs/farey-rh/bin/python - <<'PY'
import math
def tr_R_power(lam,n):
    a,b=2.0,lam
    if n==0:return a
    if n==1:return b
    for _ in range(2,n+1): a,b=b,lam*b-a
    return b
for lo,hi in [(8,9),(9,10),(10,11),(11,12)]:
    lm=(2*math.cos(math.pi/lo)+2*math.cos(math.pi/hi))/2
    print(f'interval q={lo}->{hi}: lambda_mid={lm:.15f}')
    for q in [lo,hi]:
        tr=tr_R_power(lm,q)
        print(f'  trace(R^{q}) at midpoint={tr:.15f}; target=-2; defect={tr+2:.6e}')
PY
interval q=8->9: lambda_mid=1.863572153297195
  trace(R^8) at midpoint=-1.971290812211281; target=-2; defect=2.870919e-02
  trace(R^9) at midpoint=-1.959393629949791; target=-2; defect=4.060637e-02
interval q=9->10: lambda_mid=1.890749137081062
  trace(R^9) at midpoint=-1.976605755220804; target=-2; defect=2.339424e-02
  trace(R^10) at midpoint=-1.968061073272618; target=-2; defect=3.193893e-02
interval q=10->11: lambda_mid=1.910549489909651
  trace(R^10) at midpoint=-1.980570169928621; target=-2; defect=1.942983e-02
  trace(R^11) at midpoint=-1.974229487664940; target=-2; defect=2.577051e-02
interval q=11->12: lambda_mid=1.925418799903566
  trace(R^11) at midpoint=-1.983605984436493; target=-2; defect=1.639402e-02
  trace(R^12) at midpoint=-1.978772811176659; target=-2; defect=2.122719e-02
```

The endpoint check is correspondingly different:

```text
$ /Users/za/.venvs/farey-rh/bin/python - <<'PY'
import math
for q in range(8,13):
    lam=2*math.cos(math.pi/q); a,b=2.0,lam
    for _ in range(2,q+1): a,b=b,lam*b-a
    print(f'q={q}: tr(R^q)={b:.15f}, defect={b+2:.3e}')
PY
q=8: tr(R^q)=-2.000000000000000, defect=4.441e-16
q=9: tr(R^q)=-2.000000000000000, defect=0.000e+00
q=10: tr(R^q)=-1.999999999999999, defect=1.332e-15
q=11: tr(R^q)=-1.999999999999999, defect=6.661e-16
q=12: tr(R^q)=-2.000000000000001, defect=-8.882e-16
```

The endpoint equality is the finite-group relation; the midpoint defects are not numerical
noise at the displayed scale.  Therefore extending equation (32) or (34) across a slab would
define an auxiliary matrix family, not the MMS transfer operator of a Hecke group.  No source
theorem identifies its determinant divisor with `Z_{G_lambda}` at those non-group lambdas.

### 3.3 The unreduced carrier does not repair the slab

The tempting q-independent branch family is

\[
 (L_{s,\lambda}f)(z)=
 \sum_{|n|\ge1}((z+n\lambda)^2)^{-s}
 f\!\left(-\frac1{z+n\lambda}\right).
\]

Its `n=1` branch is the Möbius map with trace lambda.  The fixed-disc hypothesis required
for a nuclear transfer determinant fails for every `0<lambda<=2`: `LAW_T2_DETERMINANT.md`
Lemma T2-A proves that both fixed multipliers have modulus one, so a compactly-contained
self-map (which would have an attracting interior fixed point) is impossible.  At the group
values the even-q orbit even reaches infinity at the endpoint after `q/2` steps.  Hence this
carrier cannot support a joint holomorphic determinant on the proposed slab.

The conclusion is not that no conceivable regularized family exists; that stronger statement
would be **CONJECTURAL**.  The conclusion proved by the current source audit is narrower:
the two natural carriers (the reduced MMS family and the unreduced fixed-disc family) do not
provide the requested lambda homotopy.

## 4. Exact tail/derivative interface still required for a finite scalar certificate

For a finite q, a theorem-valid determinant implementation would need a complex neighborhood
`U` of each closed H_0 contour and certified bounds of the form

\[
 \sup_{s\in U}|D_q(s)-D_{q,N}(s)|\le \varepsilon_{q,N},
 \qquad
 \sup_{s\in U}|D_q'(s)-D_{q,N}'(s)|\le \varepsilon'_{q,N},
 \tag{4.1}
\]

for the signed numerator and the `K_s` divisor, together with an interval enclosure for
`K_q^*` and `(K_q^*)'`.  If the first bound is proved on a slightly larger neighborhood,
the derivative bound can be obtained by Cauchy's estimate on a smaller contour:

\[
 \varepsilon'_{q,N}\le\varepsilon_{q,N}/\delta
\]

when every point of the target contour has a complex `delta`-disc inside `U`.  This is an
exact analytic reduction, not a numerical extrapolation.  The quotient rule then gives an
interval enclosure for `(SCAT-EVAL_q)` and its derivative provided the denominator balls
exclude zero.  The argument-principle integral of `phi_q'/phi_q` yields the integer
zero-minus-pole count; the independent Hejhal pole theorem is still required to interpret a
zero winding as zero zeros.

The current code does not prove (4.1).  The key receipt is the even engine's own disclosure:

```text
$ nl -ba research_notes/rh_goals_2026-08-14/lane_g/law_probes/kaggle_boundary_rate/zeta_cert_rosen_even.py | sed -n '278,319p'
    278  def dim_tail_from_matrix_signed(...):
    280      """Same det-increment geometric-ratio tail heuristic ...
    283      -- this is NOT a proven uniform tail bound.
    ...
    315      tail = g_last * q / (1 - q)
```

The odd engine uses the same four-increment extrapolation in
`zeta_cert_rosen_q5.py:419-452`; its current label does not turn the extrapolation into a
Fredholm determinant theorem.  In particular, `selberg_Z` returns determinant midpoints and
does not fold these dimension tails into the returned ball, as its docstring states.  Thus
the present engines can be used for exploration and source debugging, but they are
**NOT EVIDENCE** for a finite scalar winding certificate on H_0.

## 5. What is actually load-bearing for the two program paths

| route | scalar φ_q evaluator logically required? | current blocker |
|---|---|---|
| finite H_0 via direct scattering winding | **Yes** | (4.1), interval `K_q^*`, continuation and derivative tails; all **OPEN** |
| finite H_0 via Selberg-zeta determinant zero | **No**, if the q-specific MMS operator bridge is proved | general-q MMS/Hilbert identification and theorem-level determinant tail; **OPEN** |
| T2′ large-q tail | **No** | U1, U2b, U3 in `LAW_T2_DETERMINANT.md`; **OPEN** |
| continuous lambda-slab determinant | **No valid source route found** | reduced relation changes at each q; unreduced fixed-disc obstruction; **OPEN/structurally blocked for these carriers** |

The scalar evaluator is therefore a finite-base convenience/alternative, not the missing
ingredient in the zeta-only tail theorem.  If the program chooses path B (T2′), work should
move to U3, U1, and U2b rather than widening the scalar engine.  If it chooses path A for
q=8 onward, it should first prove the q-specific Selberg determinant bridge and its dimension
tail; only then is a Kaggle/Arb H_0 winding run load-bearing.

## 6. Status ledger and first remaining gap

| item | status |
|---|---|
| Hejhal (7.5) initial scalar formula in `Re s>1` | **CITED; PROOF CLAIM AWAITING COLD REFEREE** |
| MMS signed determinant quotient with `K_s` correction | **CITED; PROOF CLAIM AWAITING COLD REFEREE** |
| Teo functional equation and formal quotient (SCAT-EVAL) | **CITED/FORMAL; PROOF CLAIM AWAITING COLD REFEREE** |
| Odd/even block structures and q-dependent dimensions | **SOURCE-BOUND; PROOF CLAIM AWAITING COLD REFEREE** |
| Continuous lambda-slab using reduced equations (32)/(34) | **REFUTED as a source-identification route** |
| Continuous lambda-slab using unreduced fixed-disc carrier | **REFUTED for the fixed-disc/nuclear route by Lemma T2-A** |
| General-q interval determinant and derivative tail (4.1) | **OPEN** |
| Certified true scalar φ_q winding on full H_0 | **OPEN** |
| Zeta-only T2′ tail | **CONSTRUCTIBLE in principle; U1/U2b/U3 OPEN** |

**First remaining load-bearing gap for this lane:** prove a theorem-level Fredholm truncation
bound (4.1) for the q-specific signed operators, with the odd/even MMS identifications and
the `K_s` product included.  Without that bound, any scalar values or windings from the
current engines remain **NOT EVIDENCE**.  The continuous lambda homotopy is not a viable
substitute.

## 7. Sources and receipts

Primary-source receipts used:

- `research_notes/rh_goals_2026-08-14/lane_f/Q7_MMS_PRIMARY_SOURCE_RECEIPT.md` — MMS
  arXiv:0912.2236v2, equation/theorem locations and explicit non-claims.
- `research_notes/rh_goals_2026-08-14/lane_g/LAW_HEJHAL_S7_EXTRACT.md` — Hejhal §7
  equation (7.5), Proposition 7.8, Theorem 7.11, and the ineffectivity boundary.
- `research_notes/rh_goals_2026-08-14/lane_g/LAW_TEO_KAPPA_CORRECTED.md` — Teo
  Proposition 2.5, Barnes normalization, and the corrected `K_q^*` factor.
- `research_notes/rh_goals_2026-08-14/lane_g/LAW_Q3_BRANCH_DIAGNOSIS.md` — MMS `K_s`
  divisor and its zero-free right-half-plane consequence.
- `research_notes/rh_goals_2026-08-14/lane_g/LAW_T2_DETERMINANT.md` — fixed-disc
  obstruction and the T2′ zeta-only alternative.

No Kaggle or Aristotle dispatch was launched: the local type/source gate fails before either
external run could close (4.1), so an external numerical result would not be load-bearing.

## 8. Dated correction after cold referee — 2026-08-19

The independent cold report `SCAT_EVAL_Q_REFEREE.md` returns
**GAPS / NOT REFUTED**.  This block supersedes the sequencing and route-status
language above without deleting the original audit.

1.  The Teo rearrangement
    \(\phi_q(s)=Z_{G_q}(1-s)/(Z_{G_q}(s)K_q^*(s))\) remains a formal target,
    not a certified evaluator.  Before it may be consumed, one statement must
    specialize Teo to signature \((0;1;(2,q))\), bind Hejhal's width-one cusp
    scaling and scalar convention to Teo's scattering determinant, spell out
    every branch in \(K_q^*\), and clear the contour divisors.  Hejhal
    Proposition 7.8/Theorem 7.11 do not supply that finite-contour clearance.
2.  The MMS quotient and the right-half-plane zero-freeness of
    \(\det(1-K_{q,s})\) are source-correct at their stated operator scope.
    They do not identify the live generic Python/Hilbert determinant with the
    MMS Banach determinant and do not clear Teo's distinct factor \(K_q^*\).
    The later pinned q=7 binding and assembly are a separately confirmed exact-q
    exception; q=7 must not be downgraded by the older first referee.
3.  A q-specific Selberg determinant can bypass a direct scalar evaluator only
    after operator/sector identification, common continuation, theorem-level
    determinant and derivative tails, and divisor clearance.  This bypass is
    confirmed at q=7, but remains **OPEN / CONJECTURAL** for q>=8 and general q.
4.  The reduced MMS dimensions and the midpoint trace receipts block the
    proposed finite-dimensional lambda slab.  Lemma T2-A blocks the stated
    bounded-disc compact-containment carrier; it does not rule out every
    unbounded domain or regularized operator family.
5.  The current tail-route ledger is `U1 OPEN`, `U2b CLOSED` with its threshold
    caveat, and `U3 CLOSED` for the LAW route.  The older `U1/U2b/U3 OPEN`
    rows above are stale.

Thus the first q>=8 zeta-route gap is the exact code-to-MMS operator/sector
binding and continuation; only after that bridge is equation (4.1) the first
numerical certificate gate.  For a direct scalar route, the Teo--Hejhal
normalization/divisor bridge is earlier still.  No scalar winding, q>=8
Selberg zero, or new LAW case is promoted by this note.

# RATE-A adversarial referee report

**Date:** 2026-08-19  
**Target:** `BOUNDARY_ALPHA_THEOREM_SOL.md`  
**Primary verdict:** **GAPS**

No counterexample, wrong exponent, failed activation inequality, domain mismatch, or
constant-arithmetic error was found.  Conditional on the direct marked-atom
coding inside `TWOMARK_RENEWAL_SOL.md`, the RATE-A argument is a coherent
paper-level proof and the advertised bound is enormously larger than every
available pointwise diagnostic.  I do **not** promote it to an unconditional
`CONFIRMED`, for two reasons:

1. the required \(\sum_{x\le Y}(1+A^2)\) atom moment is not the literal
   \((DH_{2,4})\) statement.  It is a corollary of the proof's internal direct
   \(A^2\)-coding and summation, and it cannot be inferred from the displayed
   final \(k^2\) bound alone;
2. the requested fresh \(\phi_q\) checks are not certified Arb enclosures of
   the full infinite-dimensional quantity.  The local code explicitly omits
   dimension tails and then extracts midpoints.  They are numerical stress
   tests, not proof receipts.

Thus the analytic claim was **not refuted**, but its capstone status must remain
“paper-level conditional on the two-mark coding/Ford input; not machine
certified.”

## Audited-source receipt

The principal files read in this audit had these SHA-256 digests:

```text
021e87e55cad86a1bfc78c74b450857b3285492af00bf728f310bee6f711fd36  BOUNDARY_ALPHA_THEOREM_SOL.md
7a553a9c3ed289b513ad8dd7e3a118b0c0d50f92080a1f89a6749fbce44a692b  TWOMARK_RENEWAL_SOL.md
9146ecebfdb976ceb3df49c0e7789bc5a82ef2116ceb1f02d6a89d32f6c602d8  DH_DEPTH_LAW_SOL.md
096d389905ad21505e2c25c30aa37b5a2fa3d3f6d054bcb30229096fc5c8d885  DH2_RENEWAL_PROOF_SOL.md
e117b418cb2bbbf8cde8ecbb7c4977b4865740c30b890a9c6e669203394d339d  law_probes/rate_measure_data.json
d03fe062d8f7f795b76228807db7b73c0144765f289b5a626fab629e4165a019  law_probes/rate_measure_run.log
```

Paths in this report are relative to
`research_notes/rh_goals_2026-08-14/lane_g/` unless another root is shown.

## 1. N1-RATE bypass: survives the attack

The target does not pretend to prove N1-RATE.  It records the canonical
interval-envelope conjecture as open and the all-reduced version as false at
`BOUNDARY_ALPHA_THEOREM_SOL.md:259-283`.  Lemma 3.1 is a different estimate:

\[
0\le x'_W(\lambda)\le \frac{1+A(W)^2}{2}\,y_W,
\qquad \lambda\in[\lambda_q,2],
\]

proved from the positive path expansion, endpoint root-factor derivatives,
and \(\lambda\le2\) at `BOUNDARY_ALPHA_THEOREM_SOL.md:333-401`.  The important
distinction is real: the right side is the theta endpoint \(y_W\), not the
finite endpoint \(x_W\), and no supremum of \(|c'_W|/|c_W(\lambda_q)|\) over the
whole interval is invoked.

I checked the coefficient that is easiest to lose.  For a heavy block \(n\ge2\),
the largest root-factor ratio is

\[
\frac{u'_{n+1}(2)}{u_{n+1}(2)}
=\frac{(n+1)^2-1}{6}\le\frac{n^2}{3}.
\]

For \(n=3\), the three endpoint ratios are \(1/2,4/3,5/2\), all below
\(3\).  The aggregation used at `BOUNDARY_ALPHA_THEOREM_SOL.md:371-395`,

\[
\frac{H^2}{3}+\frac{\ell}{2}\le\frac{(H+\ell)^2}{2},
\]

has nonnegative difference
\(H^2/6+H\ell+\ell(\ell-1)/2\).  Hence
\(P'\le A^2P(2)/2\) and
\(x'=P+\lambda P'\le(1+A^2)P(2)=(1+A^2)y/2\).  There is no missing factor.

The subsequent shallow/deep split at
`BOUNDARY_ALPHA_THEOREM_SOL.md:457-521` is also internally correct:

- with \(\delta_q=2-\lambda_q\le\pi^2/q^2\) and
  \(w=1+A^2\le q^2/\pi^2\), integration gives \(x\ge y/2\), so the
  mean-value estimate is relative to \(x\);
- with \(w>q^2/\pi^2\), absolute convergence gives
  \(|x^{-2s}-y^{-2s}|\le2x^{-p}\), which is at most
  \(2\pi^2q^{-2}w x^{-p}\).

After summation this is (3.14), conditional only on the finite-\(x\) weighted
atom moment.  It never invokes the forbidden interval derivative envelope.

This construction also avoids the exact traps in the depth-law audit.  The
correct matched family \(W_n=(R^2Q)^{n-1}R^2\) has reduced depth \(n+1\), so
the \(n=q\) term lies beyond the old \(k\le q-1\) cutoff
(`DH2_RENEWAL_PROOF_SOL.md:380-395`).  The one-defect family has
\(c_\theta(w_{2,k})=6k-4\), refuting a logarithmic-depth shortcut
(`DH_DEPTH_LAW_SOL.md:559-635`).  RATE-A does not discard either family by
depth: large atom weight sends it through the deep population and the marked
moment.  **Verdict on (a): CONFIRMED, conditional on that moment.**

## 2. The \((DH_{2,4})\) atom moment and the cutoff

The displayed theorem in `TWOMARK_RENEWAL_SOL.md:37-66` is

\[
B_q(Y)=\sum_{x_X\le Y}k_X^2
\le 2^{100}Y^2
\begin{cases}
Y,&Y\le q,\\
qR^2+R^4,&Y\ge q,
\end{cases}
\qquad R=1+\log_+(Y/q).
\]

That exact statement exists and uses the **finite cutoff \(x_X\le Y\)**.
It is not a theta cutoff.

The target's Lemma 3.2 instead needs

\[
W_q(Y)=\sum_{x_X\le Y}(1+A(X)^2)
\]

with the same functional majorant
(`BOUNDARY_ALPHA_THEOREM_SOL.md:403-455`).  This is **not** a formal consequence
of the final displayed \(B_q\) inequality: the comparison recorded at
`TWOMARK_RENEWAL_SOL.md:348-362` is \(k^2\le2+8A^2\), the wrong direction for
bounding \(A^2\) from a \(k^2\) moment.

There is nevertheless a paper-level route.  The proof directly marks and sums
\(A^2\) before converting to \(k^2\) at
`TWOMARK_RENEWAL_SOL.md:593-738`; its coefficient budget is far below
\(2^{100}\).  `TWOMARK_REFEREE.md:190-225,383-392` independently accepts those
scalar budgets and the result at paper level.  The weak point is presentational
and formal rather than a discovered numerical contradiction: the reverse
\(L^u,U^t\) coding case is charged to outer cores at
`TWOMARK_RENEWAL_SOL.md:538-560`, and the Ford input remains paper-level rather
than Lean-closed (`M2_FORD_PACKING_REFEREE.md:1-8`).  The target should cite the
direct \(A^2\) sub-proof as a separate corollary, not say that the final
\((DH_{2,4})\) statement alone implies Lemma 3.2.

The cutoff usage in RATE-A is correct.  It retains \(x_X\le Y\) through the
layer-cake step; it never replaces this with \(y_X\le Y\).  The substitution is
indeed false: the canonical \(q=3\) examples have
\((x,y)=(34,1970)\) and \((89,11482)\)
(`TWOMARK_RENEWAL_SOL.md:228-266`).  The endpoint inequality \(x\le y\) yields
only \(y\le Y\Rightarrow x\le Y\), not its converse
(`DH2_RENEWAL_PROOF_SOL.md:344-353`).

**Verdict on (b): GAPS for the citation/promotion; CONFIRMED for the finite-\(x\)
cutoff and the direct-paper-level derivation.**

## 3. Recomputed (3.15), (4.1), and \(C_R\)

The literal chain at `BOUNDARY_ALPHA_THEOREM_SOL.md:510-581` is:

\[
p=\frac{11}{5},\quad C_4=2^{100},\quad
F(q)=\frac{1225}{4}+\frac{91605}{q},
\]

\[
E_{\rm pair,all}\le
2\pi^2(|s|+1)pC_4
\left(\frac{1225}{4}q^{-6/5}+91605q^{-11/5}\right),
\]

and, using \(|s|<7.648\) and \(q\ge12\),

\[
C_{\rm pair,D}=
2\pi^2(7.648+1)\frac{11}{5}2^{100}
\left(\frac{1225}{4}+\frac{91605}{12}\right).
\]

The wrap coefficient is

\[
C_{\rm wrap,D}=pC_1G
=\frac{11}{5}\,128(1+\log2)\,30.
\]

Exact-rational recomputation with
`/Users/za/.venvs/farey-rh/bin/python` printed:

```text
p= 11/5
a=p-2= 1/5
1/(3-p)= 5/4
J2= 305
J4= 91605
F0=1/(3-p)+J2= 1225/4
q= 12 F(q)= 7940 F<=7940= True
q= 16 F(q)= 96505/16 F<=7940= True
q= 24 F(q)= 32985/8 F<=7940= True
q= 48 F(q)= 35435/16 F<=7940= True
```

Fresh Arb replay printed:

```text
S_GammaA_lt_7.648= True
C4= 1267650600228229401496703205376
C_pair_D_upper= [3779968421174617205922020978730697336.3474162155785...]
C_wrap_D_upper= [14303.707381370417973956776962...]
M_1p1_upper= [2.774501918484055737859139776264637993504487999315...]
C_R_raw_upper= [10489412368759562746433608215977724801.15206330114027...]
C_R= 10489412368759562746433608215977724802 strict_upper= True
```

An independent 100-decimal mpmath evaluation agreed.  The ceiling margin is
approximately \(0.8479366988597\).  Even replacing the two component
coefficients by their displayed upward roundings `.348` and `.708` leaves
margin \(0.844600\).  The equality \(F(12)=7940\) is exact; an Arb Boolean that
straddles it at radius about \(10^{-137}\) is an interval-comparison artifact,
not a failed inequality.

**Verdict on (c): CONFIRMED.**

## 4. Numerical stress

### 4.1 Existing `LAW_RATE_MEASURE` receipt

The stored data contain 48 unique rows: eight each for
\(q=12,16,24,32,48,64\), all with \(N=12\to24\).  The point
\(s=1.1+7.0665i\) is inside \(\Gamma_R^A\), because the corrected center is
\(t_0=7.067362570867\ldots\), only \(0.000862570867\ldots\) away.  At that
on-contour point:

| \(q\) | stored \(D\) | \(N=12\to24\) residual |
|---:|---:|---:|
| 12 | 0.04618230456925413 | 0.004455321695914483 |
| 16 | 0.009383862173947844 | 0.01500032412892248 |
| 24 | 0.006581561194254793 | 0.0236124386452332 |
| 48 | 0.0024154621152229056 | 0.01856925434261641 |

These rows are at `law_probes/rate_measure_data.json:3-192,195-384,387-576,771-960`;
the method and its downgrade are recorded at
`LAW_RATE_MEASURE.md:205-241`.  The residuals are too large to certify the
listed values, although every value is microscopic relative to RATE-A.
The N=40 validation receipt applies only to the exact small-\(q\) comparator
grid, not to these \(q>6\) contour values
(`LAW_RATE_MEASURE.md:205-217`).  The sampling/fit discussion correctly refuses
to turn the observed slope into a theorem (`LAW_RATE_MEASURE.md:289-332`).

### 4.2 Fresh points on \(\Gamma_R^A\)

I freshly evaluated \(s=1.1+i(t_0+u)\) for
\(u=-1/2,0,1/2\), using the same even-\(q\) engine at \(N=8\to12\).  The
following is stdout from the run; entries in the middle column are the three
\(D_{N=12}\) values in increasing \(u\), and the last column is the largest
relative \(N=8\to12\) change:

| \(q\) | fresh \(D_{N=12}(-1/2,0,1/2)\) | max residual | \(C_Rq^{-6/5}\) | RHS / max \(D\) |
|---:|---|---:|---:|---:|
| 12 | 0.087552202369, 0.046299458411, 0.033595974128 | 0.355564 | \(5.31782037714\times10^{35}\) | \(6.0739\times10^{36}\) |
| 16 | 0.024091051338, 0.010343669104, 0.039297030604 | 0.547939 | \(3.76536585402\times10^{35}\) | \(9.5818\times10^{36}\) |
| 24 | 0.017786316272, 0.008028373137, 0.020151192667 | 0.675593 | \(2.31471576241\times10^{35}\) | \(1.1487\times10^{37}\) |
| 48 | 0.003698495856, 0.003491509116, 0.006524134116 | 0.841902 | \(1.00753855542\times10^{35}\) | \(1.5443\times10^{37}\) |

Thus the numerical majorization test passes by at least \(6\times10^{36}\)
on these points.  The large truncation residuals make this a deliberately weak
diagnostic, not evidence for the theorem.

The certification boundary is explicit in the code.  `law_probes/agp_phi.py:161-168`
extracts `.real.mid()` and `.imag.mid()` from the internal acb result and returns
a Python `complex`; `law_probes/rate_measure.py:112-119` then uses mpmath/cmath.
The underlying even engine says that dimension tails are **not** folded into
the returned ball at
`.worktrees/aletheia-restore/code/zeta_cert_rosen_even.py:487-499`
(the odd engine gives the same warning at `zeta_cert_rosen.py:436-448`).
A direct fresh \(q=12\), \(s=1.1+0.5i\), \(N=12\) call did produce the finite
determinant ball

```text
Z_ball= [1.21433702289168572236576049675539641959025857478355... +/- 2.18e-83]
       + [0.38563384475258383217534454321967817730207186330158... +/- 2.04e-83]j
```

but the tiny displayed radii cover finite-arithmetic rounding only, not the
omitted dimension tail.  It would be false to call the resulting \(D\) a
certified Arb enclosure.  The continuous Arb segment tool likewise labels its
determinant scout non-supremal; its rigorous output is only the old coarse
\(\alpha=0\) Ford envelope (for example, Route A with 256 cells gives
\(E\le8.71154\)), not RATE-A.

### 4.3 Intermediate inequalities

A finite diagnostic over 34 canonical sample words per \(q\), including
one-defect, alternating, long-\(2\), and large-balanced-digit traps, evaluated
Lemma 3.1, the integrated estimate (3.11), and the applicable shallow/deep local
power bound at \(t=t_0+1/2\).  Stdout was:

```text
q=12 words=34 shallow=7 deep=27 max_deriv_ratio=0.52 max_integrated_ratio=0.503830164509 max_local_power_ratio=0.704515021455
q=16 words=34 shallow=11 deep=23 max_deriv_ratio=0.52 max_integrated_ratio=0.510836007465 max_local_power_ratio=0.241976397053
q=24 words=34 shallow=11 deep=23 max_deriv_ratio=0.52 max_integrated_ratio=0.51590524     max_local_power_ratio=0.253334...
q=48 words=34 shallow=11 deep=23 max_deriv_ratio=0.52 max_integrated_ratio=0.5189730      max_local_power_ratio=0.258545...
```

Every ratio is LHS/RHS and is below 1.  This is a non-exhaustive falsification
attempt, not a replacement for the symbolic proof.

**Verdict on (d): numerical majorization CONFIRMED; requested full Arb
certification GAPS because the evaluator has an uncovered dimension tail.**

## 5. Activation and provenance of \(\alpha\)

The dependence chain at `BOUNDARY_ALPHA_THEOREM_SOL.md:527-598` is analytic:

1. select \(p=11/5\), which lies in the proved Chebyshev range \(2<p<3\);
2. the layer-cake/atom estimate gives the leading power
   \(q^{-6/5}\) and a lower-order \(q^{-11/5}\) term;
3. factor out \(q^{-6/5}\), leaving
   \(F(q)=1225/4+91605/q\);
4. for every \(q\ge12\), monotonicity gives \(F(q)\le F(12)=7940\).

Therefore \(q_{\rm RATE}=12\) is the activation of this boundary estimate,
not a numerically selected crossover.  The empirical slope and the old
\(78.196\) Chebyshev anchor are not inputs.  The note also correctly separates
this from any final all-gates onset \(q_0\), which it does not claim.

**Verdict on (e): CONFIRMED.**

## 6. Domain consistency

The theorem's contour is the first-zero segment

\[
\Gamma_R^A=\{1.1+it:|t-t_0|\le1/2\},\qquad
t_0=7.067362570867\ldots,
\]

as defined at `BOUNDARY_ALPHA_THEOREM_SOL.md:24-40`.  This is the exact segment
consumed by the selected A0 transport quantity
(`R3_TRANSPORT_EXECUTION_SOL.md:20-83`; `KF_WALL_ATTACK_SOL.md:108-201`).
The older `7.0665` was only a sampling center; the correction and exact
first-zero convention are explicit at `R3_ROUTE_B_TRANSPORT_SOL.md:30-60`.

The direct rebuilt \(K_F\) route is **not** on that segment: it uses sixth-zero
geometry (`KF_WALL_ATTACK_SOL.md:221-255`).  Its corrected semantics are raw
\(\sup|F|<109\) and safe ledger value \(K_F=109\)
(`KF_WALL_ATTACK_SOL.md:472-481,630-650`).  This would be a domain error if
RATE-A were fed into that sixth-zero contour.  The target does not do so: it
selects A0 and explicitly leaves \(K_F\) unselected at
`BOUNDARY_ALPHA_THEOREM_SOL.md:657-661`.

**Verdict on (f): CONFIRMED for the selected A0 chain; REFUTED only for a
hypothetical substitution into the separate sixth-zero \(K_F\) chain, which the
target does not make.**

## 7. Upstream integrity

- **Chebyshev term.** `DH_DEPTH_LAW_SOL.md:637-709` proves the needed estimate
  for \(2<p<3\); \(p=11/5=2.2\) is strictly inside.  The old numerical anchor
  \(78.196\) is not a uniform \(\Gamma_R^A\) receipt and is not used as one.
- **Wrap term.** The fixed-\(\sigma>1\) Ford/wrap estimate is present at
  `FW_RENEWAL_COUNT_SOL.md:195-216,475-498` and is accepted at paper level by
  `FW_REFEREE.md:1-26`.  The recomputed coefficient is the one used above.
- **Endpoint normalization.** On the balanced matched image,
  `DH2_RENEWAL_PROOF_SOL.md:264-353` proves \(x\le y\), hence
  \(m=\min(x,y)=x\) and \(x/m=1\).  RATE-A uses exactly that scope.  This does
  not license the false theta-cutoff transfer.

**Verdict on (g): CONFIRMED at paper level within the stated balanced/matched
scope.**

## Final claim ledger

| Claim attacked | Verdict | Reason |
|---|---|---|
| Lemma 3.1 avoids N1-RATE | **CONFIRMED** | It is theta-relative, not an interval \(|c'|/|c|\) envelope; coefficients and traps pass. |
| Shallow/deep split | **CONFIRMED conditional** | Algebra is correct once the finite-\(x\) atom moment is admitted. |
| “\((DH_{2,4})\) directly states the atom moment” | **REFUTED** | The displayed theorem states a \(k^2\) moment; the needed \(A^2\) moment comes from proof internals. |
| Atom moment itself | **GAPS / paper-level supported** | Direct marked coding and budgets support it, but the critical promotion is not separately stated or machine closed. |
| No theta-cutoff substitution | **CONFIRMED** | Every layer-cake cutoff remains \(x\le Y\); the known false converse is not used. |
| (3.15), (4.1), \(C_R\) | **CONFIRMED** | Exact rational, Arb, and independent high-precision recomputations agree. |
| \(q_{\rm RATE}=12\), no fitted \(\alpha\) | **CONFIRMED** | It follows from the analytic choice \(p=11/5\) and exact monotonic absorption. |
| Measured/fresh values violate RATE-A | **REFUTED** | All tested point values are smaller than the RHS by at least \(6\times10^{36}\). |
| Fresh values are certified full Arb enclosures | **REFUTED** | Dimension tails are omitted and acb midpoints are converted to Python complex. |
| \(\Gamma_R^A\) feeds selected A0 | **CONFIRMED** | Same first-zero segment and corrected \(t_0\). |
| \(\Gamma_R^A\) is the rebuilt \(K_F\) contour | **REFUTED, but not claimed** | Rebuilt \(K_F\) uses sixth-zero geometry; the target explicitly does not select it. |
| E_Cheb, E_wrap, endpoint \(x/m=1\) | **CONFIRMED paper-level** | Correct parameter and balanced/matched scopes. |

**Bottom line:** I could not refute RATE-A's analytic inequality.  The honest
status is **GAPS**, narrowly: the proof is a paper-level conditional theorem
whose decisive atom-moment input is a direct sub-proof rather than the cited
displayed \((DH_{2,4})\) statement, and its numerical checks are not certified
full-operator Arb enclosures.  Subject to accepting the two-mark/Ford paper
proof, the exponent \(6/5\), activation \(12\), and explicit constant
`10489412368759562746433608215977724802` are confirmed.

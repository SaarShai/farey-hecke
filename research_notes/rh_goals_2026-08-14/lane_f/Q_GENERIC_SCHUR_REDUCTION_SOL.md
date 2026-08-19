# q-generic MMS Schur reduction

Date: 2026-08-19

Status: **FINITE BLOCK ALGEBRA VERIFIED; INFINITE OPERATOR FACTORIZATION IS A
CONDITIONAL PROOF CLAIM — AWAITING COLD REFEREE; q-GENERIC ANALYTIC LINKAGE IS
GAP / CONJECTURAL.**

This lane turns the sparse MMS reduced matrices into a terminal determinant.
It does not certify a resonance, a Selberg zero, the LAW, or a q-uniform
Hardy-disc family.  Every statement below that needs a fixed-q disc margin,
operator realization, or an infinite Fredholm tail remains explicitly
`GAP`, `OPEN`, or `CONJECTURAL`.

## 1. Scope and source boundary

The checker is
`q_generic_schur_check.py`.  It imports only the tracked pinned engines in

```text
research_notes/rh_goals_2026-08-14/lane_g/law_probes/kaggle_boundary_rate/
```

and does not import the old `.worktrees/aletheia-restore` adapters.  The
source bytes used by the checker were fingerprinted with:

```text
$ sha256sum \
    research_notes/rh_goals_2026-08-14/lane_g/law_probes/kaggle_boundary_rate/zeta_cert_rosen.py \
    research_notes/rh_goals_2026-08-14/lane_g/law_probes/kaggle_boundary_rate/zeta_cert_rosen_even.py \
    research_notes/rh_goals_2026-08-14/lane_g/law_probes/kaggle_boundary_rate/zeta_cert_rosen_q5.py \
    research_notes/rh_goals_2026-08-14/lane_f/q_generic_schur_check.py
965c2e5f65ae88b458d79bc425375e31589dcbf50703173664ef0e30901dceac  .../zeta_cert_rosen.py
693d2a88fd525e94c8ab6a63486e82fe0670d9dce142effbd5be5e324597212a  .../zeta_cert_rosen_even.py
c84c5c3f6d9f7a320bca7f1dbfd96a4859c3eea9b3de5420eb4eb223ad0d597  .../zeta_cert_rosen_q5.py
c34814c6f0816f360b1f8c4b108a937fa72ad8803f5e133ebd3a86fb35e05965  .../q_generic_schur_check.py
```

The first three hashes are the pinned engine inputs; the fourth is the new
checker.  The checker has an explicit import-path guard and prints the actual
resolved paths before doing any arithmetic.

The primary abstract source is Mayer–Mühlenbruch–Strömberg (MMS),
arXiv:0912.2236v2, 15 March 2010, DCDS 32 (2012), 2453–2484, SHA-256
`a10020bd084534dc60fc3e887958f1583f2fc115d567961b461df1a59b32e072`.
The durable source receipt identifies the relevant locations as MMS p. 21,
equation (34), Theorem 4.10 on p. 20, Lemma 5.1 on p. 21, and Theorem 6.4 on
p. 28 (`Q7_MMS_PRIMARY_SOURCE_RECEIPT.md:38-62`).  The q=7 binding note
records the branch convention, normalized Hardy basis, and the Simon and
Grothendieck determinant roles (`Q7_R5_OPERATOR_BINDING_SOL.md:137-155,
364-467, 690-712`).  Those q=7 references are source/convention evidence;
they do not silently promote this q-generic lane.

The pinned engines themselves state that they use exact Hurwitz tail closure,
`acb_series` Taylor coefficients, and Arb finite determinants.  Their source
comments and implementation are at
`zeta_cert_rosen_even.py:19-31,146-189,228-246` and
`zeta_cert_rosen.py:9-33,122-174,209-240`.  The old determinant increment
tail remains a separate heuristic and is not used as a proof in this note.

## 2. Actual Hardy-disc maps and the even-q geometry

Write (lambda_q=2cos	heta), (	heta=pi/q).  The branch maps used by
the pinned engines are the actual inverse branches, not abstract symbols:

[
 \theta_{+n}(z)=-\frac1{z+n\lambda_q},
 \qquad
 \theta_{-n}(z)=\frac1{z-n\lambda_q},
 \qquad n\ge1,
]

with principal squared weights

[
 w_{\pm n,s}(z)=((z\pm n\lambda_q)^2)^{-s}.
]

For a source disc (D_i=D(c_i,R_i)) and target disc (D_j), the concrete
unit-disc conjugation is

[
 u=\frac{z-c_i}{R_i},\qquad
 \widehat\theta_{\pm n}^{,i\leftarrow j}(u)
 =\frac{\theta_{\pm n}(c_i+R_i u)-c_j}{R_j}.
]

The Hardy action is therefore

[
 (\widehat T_{\pm n,s}^{,i\leftarrow j}f)(u)
 =w_{\pm n,s}(c_i+R_i u)
   f\!\left(\widehat\theta_{\pm n}^{,i\leftarrow j}(u)\right),
]

whenever the displayed map lands in the unit disc.  The normalized monomials
(u^k) are exactly the columns expanded by the pinned `acb_series` builders.
For a fixed q, a proof that all these maps land strictly in the target discs,
including enlarged discs for a continuation argument, is a separate required
gate.  **q-generic uniform strict containment is GAP / CONJECTURAL.**

### 2.1 Even partition points: exact sine form

For (q=2h+2), the even engine uses the finite continued-fraction chain
(y_m=[0;1^m]_{lambda_q}), (0le mle h), with
(y_0=0) and the recurrence

[
 y_{m+1}=-\frac1{\lambda_q+y_m}.
]

The exact closed form is

[
 \boxed{y_m=-\frac{\sin(m\pi/q)}{\sin((m+1)\pi/q)}}.
\tag{2.1}
]

Indeed (2.1) gives (y_0=0), and

[
 \lambda_q+y_m
 =\frac{2\cos\theta\sin((m+1)\theta)-\sin(m\theta)}
        {\sin((m+1)\theta)}
 =\frac{\sin((m+2)\theta)}{\sin((m+1)\theta)},
]

which is the recurrence.  Since (h	heta=pi/2-	heta),

[
 y_h=-\cos\theta=-\lambda_q/2.
]

Thus the sorted partition is (y_h<\cdots<y_1<y_0=0).  The rightmost
(`terminal`) cell is ([y_1,y_0]).  Since

[
 y_1=-\frac1{2\cos\theta}=-\frac1{\lambda_q}\longrightarrow-\frac12,
]

that cell tends to ([-1/2,0]).  The leftmost cell has width

[
 y_{h-1}-y_h
 =\frac{\sin^2\theta}{\cos\theta}\longrightarrow0.
]

Therefore only the eliminated left cell collapses in the (q\to\infty)
limit; the terminal cell has a non-collapsing limiting size.  This matters for
the q-generic recurrence: the terminal (B_i) blocks do not disappear in a
large-q limit.  The formula is also consistent with the tracked source's
finite-CF loop (`zeta_cert_rosen_even.py:151-173`).

The following Arb replay compares (2.1) to the source finite-CF evaluation
and prints the two limiting-cell diagnostics:

```text
$ PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
... tracked even engine; q in (8,10,20,100); max CF/formula interval ...
PY
q=8 h=3 max_cf_formula_abs_upper=[7.27e-90 +/- 2.86e-179] right_terminal_width=[0.5411961001 +/- 9.46e-91] left_collapsing_width=[0.1585126678 +/- 4.09e-90]
q=10 h=4 max_cf_formula_abs_upper=[6.59e-90 +/- 2.36e-179] right_terminal_width=[0.5257311121 +/- 1.42e-90] left_collapsing_width=[0.1004057079 +/- 2.74e-90]
q=20 h=9 max_cf_formula_abs_upper=[1.22e-89 +/- 3.26e-178] right_terminal_width=[0.5062325629 +/- 4.19e-90] left_collapsing_width=[0.0247767852 +/- 4.41e-91]
q=100 h=49 max_cf_formula_abs_upper=[6.54e-89 +/- 2.96e-178] right_terminal_width=[0.5002468416 +/- 1.97e-90] left_collapsing_width=[0.0009871229 +/- 3.76e-93]
```

The shortened mantissas above are presentation-only; the command's Arb
intervals are the receipt.  The odd-q partition uses two interleaved
continued-fraction families in the tracked generic engine
(`zeta_cert_rosen.py:146-156`); **no one-family sine formula is asserted for
odd q**.

## 3. The exact MMS block patterns

### 3.1 Even (q=2h+2), equation (32)

The source equation-(32) action is

[
 (Lg)_1=B_1g_h,
 \qquad
 (Lg)_i=A_i g_{i-1}+B_i g_h,quad 2\le i\le h,
\tag{3.1}
]

where (A_i=L_{+1}) is the single step-1 branch and (B_i) is the sum of
the positive (L^infty_{+2}) and signed negative (L^infty_{-1}) tails.
The `sign` parameter is the MMS sector sign.  This is the exact source loop,
not an inferred sparsity pattern (`zeta_cert_rosen_even.py:228-246`).

### 3.2 Odd (q\ge5), equation (34)

Put (k=\kappa_q=2h_q+1) and (p=k-1=2h_q).  Accumulate the source
occurrences into three block columns:

[
\begin{array}{ll}
 (Lg)_1=C_1g_p+B_1g_k, &
 C_1=L_{+2}+\operatorname{sign}L_{-1},
 \
 (Lg)_2=C_2g_p+B_2g_k, &
 C_2=\operatorname{sign}L_{-1},
 \
 (Lg)_i=A_i g_{i-2}+C_i g_p+B_i g_k,quad 3\le i\le k,
 &A_i=L_{+1},\
 &C_i=\operatorname{sign}L_{-1},
\end{array}
\tag{3.2}
]

and (B_1=L^infty_{+3}+\operatorname{sign}L^infty_{-2}), while
(B_i=L^infty_{+2}+\operatorname{sign}L^infty_{-2}) for (i\ge2).
The q=7 source/receipt audit already records this as a literal equation-(34)
specialization; the generic odd engine uses the same indexed loop
(`zeta_cert_rosen.py:209-240`).  The two terminal columns (p,k) are kept
distinct even when a step-2 occurrence lands in column (p); the source
builder adds those occurrences before the block extraction.

The former q=8 endpoint-contour route is not this route.  Its cold referee
confirmed that endpoint-only half-turn tests do not enclose a continuous arc
and that its geometric finite-dimension tail was heuristic
(`F8_R3B_REFUTATION_REFEREE.md`, summary and §§2–3).  The Schur reduction
does not repair either defect; it only changes the finite determinant
evaluator after a valid operator/tail certificate exists.

## 4. Finite determinant identities

Let (M_N) be the source matrix on the first (N) normalized Taylor modes per
disc.  The source construction is an exact coefficient extraction in the
normalized variable (u), so (M_N) is the finite matrix of
(P_NL^HP_N) in that basis.  This finite statement does **not** identify
(det(I-M_N)) with an infinite Fredholm determinant.

### 4.1 Even elimination

Set

[
 C_1=B_1,qquad C_i=A_iC_{i-1}+B_iquad(2\le i\le h).
\tag{4.1}
]

For the homogeneous block system ((I-M_N)x=0), the first (h-1) rows
recursively give (x_i=C_i x_h).  Equivalently, perform the block row
operations

[
 R_i\leftarrow R_i+A_iR_{i-1},quad i=2,\ldots,h,
]

in order.  The row-operation matrix is block lower triangular with identity
diagonal.  Its last row has terminal block (I-C_h), and all other diagonal
blocks are identity.  Therefore the exact finite identity is

[
 \boxed{\det(I_{hN}-M_N)=\det(I_N-C_h).}
\tag{4.2}
]

This is ordinary block Gaussian elimination over the Arb ball ring; no
approximation enters.

### 4.2 Odd step-2 elimination

Define (P_i,Q_i) by

[
 P_1=C_1,quad Q_1=B_1,qquad
 P_2=C_2,quad Q_2=B_2,
\tag{4.3}
]

and, for (i\ge3),

[
 P_i=A_iP_{i-2}+C_i,qquad
 Q_i=A_iQ_{i-2}+B_i.
\tag{4.4}
]

Eliminating the step-2 subdiagonals gives identity diagonal blocks except at
the terminal rows (p=k-1) and (k).  On the two terminal variables
((x_p,x_k)), the remaining block is

[
 R=
 \begin{pmatrix}
 I-P_p&-Q_p\\
 -P_k&I-Q_k
 \end{pmatrix}.
\tag{4.5}
]

The exact finite identity is

[
 \boxed{\det(I_{kN}-M_N)=\det_{2N}(R).}
\tag{4.6}
]

The row-operation matrix is block lower triangular separately on the odd and
even step-2 chains.  The checker implements (4.1) and (4.3)–(4.5), extracts
the source blocks, and compares both sides in Arb arithmetic.

### 4.3 Taylor and s-derivative preservation

The source matrix's entries are coefficients of actual `acb_series` expansions
of the maps in §2.  Thus Schur reduction reuses the same Taylor coefficient
balls; it is not a new collocation or endpoint evaluator.  If a source
derivative matrix (M_N'(s)) is supplied (as in the existing q=7 R3b engine),
the same recurrence preserves it by the product rule:

[
 C'_1=B'_1,qquad
 C'_i=A'_iC_{i-1}+A_iC'_{i-1}+B'_i,
\]

and

[
 P'_i=A'_iP_{i-2}+A_iP'_{i-2}+C'_i,qquad
 Q'_i=A'_iQ_{i-2}+A_iQ'_{i-2}+B'_i.
]

Differentiating (4.5) gives (R') blockwise.  This proves only algebraic
preservation of a supplied derivative/Taylor enclosure.  A continuous
contour theorem still needs a valid interval image or resolvent enclosure on
every closed subarc.  **That continuous-contour gate is OPEN.**

## 5. Infinite Fredholm factorization: conditional status

Here is the precise conditional statement the Schur algebra supports.

> **Conditional Schur–Fredholm proposition — AWAITING COLD REFEREE.** Fix q
> and an s-domain on which the actual branch/tail blocks in (3.1), or (3.2),
> act boundedly on the chosen Hardy/Banach direct sum, (I-L_s) is in the
> relevant determinant class, and every displayed (A_i,B_i,C_i) is nuclear
> (trace class in the Hilbert realization).  Then block triangular elimination
> gives (4.2) for even q and (4.6) for odd q with the finite determinant
> replaced by the corresponding Fredholm determinant.

The algebra is short.  In the even case let (E) be the finite block lower
triangular row-operation matrix generated by (R_i\leftarrow R_i+A_iR_{i-1}).
Then (E-I) is strictly block lower triangular and nuclear, so

[
 \det(E)=1,qquad E(I-L_s)
 \sim \operatorname{diag}(I,\ldots,I,I-C_h).
\]

The determinant product rule gives

[
 \det(I-L_s)=\det(E(I-L_s))=\det(I-C_h).
\tag{5.1}
]

For odd q, use the two step-2 row-operation chains.  The corresponding (E-I
) is again strictly block lower triangular and nuclear, and

[
 E(I-L_s)
 \sim \operatorname{diag}(I,\ldots,I,R),
 qquad
 \det(I-L_s)=\det_{H_p\oplus H_k}(R).
\tag{5.2}
]

The word `nuclear` in this paragraph is a hypothesis, not a hidden numerical
claim.  Simon, *Notes on infinite determinants of Hilbert space operators*,
Adv. Math. 24 (1977), Theorem 3.3 and Theorem 4.2, equation (4.2), p. 258,
provide holomorphic trace-class determinants, multiplicativity, and the
canonical spectral product.  On the MMS Banach realization, MMS Theorem 4.10
gives nuclearity of order zero and Lemma 5.1 gives the complemented invariant
(P)-sectors; Grothendieck, *Résumé des résultats essentiels...*, Ann. Inst.
Fourier 4 (1952), Théorème 8, pp. 108–109, gives the genus-zero determinant in
the (p\le2/3) nuclear class.  These are the precise roles already recorded
in `Q7_R5_OPERATOR_BINDING_SOL.md:690-712`; MMS Theorem 6.4 is the separate
Selberg quotient statement.

For a fixed q, the conditional proposition can therefore be read as a clean
operator-algebra reduction once the bounded/nuclear hypotheses are supplied.
The following required implications remain **GAP / CONJECTURAL** here:

1. a q-generic family of enlarged Hardy discs with strict image contraction;
2. the Hardy/Banach common-continuation and determinant-identification lemma
   for every q in the desired range;
3. a uniform transformed Fredholm tail after replacing the full matrix by the
   terminal Schur matrix;
4. a continuous closed-contour enclosure and (K_s) nonvanishing gate;
5. the q-generic MMS factorization and the law's arithmetic transport.

The reduction changes the dimension of the finite determinant from (hN) to
(N) for even q and from (kN) to (2N) for odd q.  It does **not** by
itself prove that the old empirical determinant-increment tail remains valid
after reduction.  A transformed trace/nuclear tail must be proved directly;
the old finite-ratio rule is not such a proof.

### 5.1 The m-tail threshold and meromorphic centering

For a tail beginning at (n_0), binomial expansion of the normalized input
monomial gives terms with exponents (2s+m), (m\ge0).  The raw branch sum is
absolutely summable when

[
 2\Re(s)+m>1\quad\text{for every retained }m,
]

and hence, because the (m=0) term is present, on the full common domain

[
 \Re(s)>1/2.
]

The (m\ge1) terms have weaker individual thresholds, but they do not remove
the (m=0) obstruction.  Below (Re(s)=1/2), the raw branch sum is not the
definition; one must retain the (m=0) Hurwitz term (or an equivalent
centered term) and use its meromorphic continuation.  The pole lattice is the
MMS lattice (s=(1-r)/2), (r=0,1,2,\ldots), subject to the precise
sector/continuation domain.  The q=7 repaired note derives a first-moment
centered estimate on its own (Omega^*), but **a q-generic centered-tail
estimate and the transformed Schur tail are GAP / CONJECTURAL here**.

## 6. Old refutation and dependency boundary

The F8 cold referee's refutation remains binding:

* the former `certify_segment` accepted endpoint determinant balls without a
  continuous subarc enclosure; (f(t)=(t-1/2)^2) is an explicit scalar
  countermodel;
* the former finite determinant tail inferred an infinite bound from a few
  observed increment ratios, which is not a theorem (a future increment can
  violate that extrapolation);
* the TB geometry and the winding engine were not bound to one common theorem.

Those defects are not silently repaired by (4.2) or (4.6).  The new route is a
finite evaluator reduction and an operator-algebra lemma with explicitly
stated hypotheses.  **Continuous contour, full Fredholm tail, and Selberg
factorization remain OPEN.**

## 7. Arb verification receipt

Command (no output file and no bytecode cache):

```text
$ PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python \
    research_notes/rh_goals_2026-08-14/lane_f/q_generic_schur_check.py \
    --q 7 8 9 10 --N 4 8 --s 0.55+2.1i 0.63+4.3i --q8-speed
```

The command printed the following receipt (all rows had `status=PASS`):

```text
ENGINE_DIR=.../research_notes/.../lane_g/law_probes/kaggle_boundary_rate
ODD_ENGINE=.../kaggle_boundary_rate/zeta_cert_rosen.py
EVEN_ENGINE=.../kaggle_boundary_rate/zeta_cert_rosen_even.py
IMPORT_PATH_GUARD=PASS
SCHUR q=7 parity=odd N=4 s=0.55+2.1i full_dim=20 reduced_dim=8 pattern_ok=True difference_abs_upper=[2.88e-87 +/- 4.59e-176] contains_zero=True ... status=PASS
SCHUR q=7 parity=odd N=4 s=0.63+4.3i full_dim=20 reduced_dim=8 pattern_ok=True difference_abs_upper=[9.89e-85 +/- 2.48e-174] contains_zero=True ... status=PASS
SCHUR q=7 parity=odd N=8 s=0.55+2.1i full_dim=40 reduced_dim=16 pattern_ok=True difference_abs_upper=[6.50e-85 +/- 3.63e-174] contains_zero=True ... status=PASS
SCHUR q=7 parity=odd N=8 s=0.63+4.3i full_dim=40 reduced_dim=16 pattern_ok=True difference_abs_upper=[7.94e-84 +/- 3.54e-173] contains_zero=True ... status=PASS
SCHUR q=8 parity=even N=4 s=0.55+2.1i full_dim=12 reduced_dim=4 pattern_ok=True difference_abs_upper=[2.24e-86 +/- 7.60e-176] contains_zero=True ... status=PASS
SCHUR q=8 parity=even N=4 s=0.63+4.3i full_dim=12 reduced_dim=4 pattern_ok=True difference_abs_upper=[4.56e-85 +/- 1.55e-176] contains_zero=True ... status=PASS
SCHUR q=8 parity=even N=8 s=0.55+2.1i full_dim=24 reduced_dim=8 pattern_ok=True difference_abs_upper=[1.42e-84 +/- 3.72e-173] contains_zero=True ... status=PASS
SCHUR q=8 parity=even N=8 s=0.63+4.3i full_dim=24 reduced_dim=8 pattern_ok=True difference_abs_upper=[2.53e-78 +/- 3.14e-167] contains_zero=True ... status=PASS
SCHUR q=9 parity=odd N=4 s=0.55+2.1i full_dim=28 reduced_dim=8 pattern_ok=True difference_abs_upper=[3.82e-87 +/- 1.85e-176] contains_zero=True ... status=PASS
SCHUR q=9 parity=odd N=4 s=0.63+4.3i full_dim=28 reduced_dim=8 pattern_ok=True difference_abs_upper=[1.73e-85 +/- 3.09e-174] contains_zero=True ... status=PASS
SCHUR q=9 parity=odd N=8 s=0.55+2.1i full_dim=56 reduced_dim=16 pattern_ok=True difference_abs_upper=[1.16e-84 +/- 7.63e-174] contains_zero=True ... status=PASS
SCHUR q=9 parity=odd N=8 s=0.63+4.3i full_dim=56 reduced_dim=16 pattern_ok=True difference_abs_upper=[4.80e-84 +/- 3.12e-173] contains_zero=True ... status=PASS
SCHUR q=10 parity=even N=4 s=0.55+2.1i full_dim=16 reduced_dim=4 pattern_ok=True difference_abs_upper=[2.56e-86 +/- 2.35e-175] contains_zero=True ... status=PASS
SCHUR q=10 parity=even N=4 s=0.63+4.3i full_dim=16 reduced_dim=4 pattern_ok=True difference_abs_upper=[3.23e-83 +/- 4.86e-172] contains_zero=True ... status=PASS
SCHUR q=10 parity=even N=8 s=0.55+2.1i full_dim=32 reduced_dim=8 pattern_ok=True difference_abs_upper=[4.72e-84 +/- 1.92e-173] contains_zero=True ... status=PASS
SCHUR q=10 parity=even N=8 s=0.63+4.3i full_dim=32 reduced_dim=8 pattern_ok=True difference_abs_upper=[1.79e-83 +/- 2.84e-172] contains_zero=True ... status=PASS
Q8_SPEED N=16 s=0.4252310423737965+4.345760788321986i full_dim=48 reduced_dim=16 wall_s=0.230027 contains_zero=True status=PASS
OVERALL_STATUS=PASS failures=0
```

The ellipses in this rendered receipt abbreviate only path and timing fields;
the command above is the reproducibility authority.  `contains_zero=True`
means the Arb interval for the full-minus-reduced determinant contains zero;
it is not a floating-point equality claim.  The q=8 speed row measures the
full-versus-reduced check, not a contour theorem.

## 8. Status ledger

| item | status | exact boundary |
|---|---|---|
| Even finite block recurrence (4.1) and determinant (4.2) | **PROVED finite algebra; AWAITING COLD REFEREE** | Applies to the source's sparse matrix, not to an infinite tail. |
| Odd finite step-2 recurrence (4.3)–(4.6) | **PROVED finite algebra; AWAITING COLD REFEREE** | Terminal determinant is exactly (2N\times2N). |
| Arb q=7,8,9,10 checks at N=4,8 and q=8 N=16 | **RECEIPT PASS** | Tracked engines, two sample s-values; diagnostic finite evidence only. |
| Even sine partition formula | **PROVED algebraically; Arb replay PASS** | Fixed even q; no odd-q one-family claim. |
| Derivative/Taylor recurrence | **PROVED algebraically conditional on supplied derivative blocks** | Does not prove a continuous arc enclosure. |
| Infinite triangular Fredholm factorization | **CONDITIONAL PROOF CLAIM — AWAITING COLD REFEREE** | Requires bounded nuclear actual blocks and determinant-class hypotheses. |
| q-generic enlarged discs and Hardy/Banach linkage | **GAP / CONJECTURAL** | No uniform q family or all-q constants supplied. |
| m-tail below (Re s=1/2) | **GAP / CONJECTURAL** | Requires meromorphic centering and transformed-tail bounds. |
| Continuous contour, (K_s), Selberg quotient, law | **OPEN** | Downstream gates remain blocked. |
| Former endpoint-only / empirical-tail route | **REFUTATION CONFIRMED** | Preserved in `F8_R3B_REFUTATION_REFEREE.md`; no silent rewrite. |

**READY FOR COLD JUDGING.**

## 9. Dated formatting correction — 2026-08-19

The first draft of this note used TeX delimiters in a patch transport that
interpreted some backslash sequences as control characters. No mathematical
status or source claim changed. The formulas below are the authoritative
plain-text rendering of the same content:

~~~text
Even q = 2h+2:
  L[i,i-1] = A_i       (2 <= i <= h)
  L[i,h]   = B_i       (1 <= i <= h)
  C_1 = B_1
  C_i = A_i*C_{i-1} + B_i
  det(I - L) = det(I - C_h)

Odd q >= 5, k = kappa, p = k-1:
  L[i,i-2] = A_i       (3 <= i <= k)
  L[i,p]   = C_i       (1 <= i <= k)
  L[i,k]   = B_i       (1 <= i <= k)
  P_1=C_1, Q_1=B_1; P_2=C_2, Q_2=B_2
  P_i=A_i*P_{i-2}+C_i
  Q_i=A_i*Q_{i-2}+B_i
  R = [[I-P_p, -Q_p], [-P_k, I-Q_k]]
  det(I - L) = det(R)

Even partition, q=2h+2, theta=pi/q:
  y_m = -sin(m*theta)/sin((m+1)*theta), 0 <= m <= h
  y_h = -lambda_q/2
  terminal cell [y_1,y_0] -> [-1/2,0]
  left cell width y_{h-1}-y_h = sin(theta)^2/cos(theta) -> 0
~~~

The receipt and status ledger in §§7–8 are unchanged.

## 10. Dated cold-referee promotion and scope correction — 2026-08-19

`Q_GENERIC_SCHUR_REDUCTION_REFEREE.md` reviewed immutable candidate commit
`95dd8736f25bc71538d555eaacd7e5a01aa6c4c3`, reran the documented checker and
an opposite-sector parity-edge suite, and returned the following bounded
verdict:

* the finite even/odd block eliminations, even sine law, and derivative
  recurrences conditional on supplied derivative blocks are **CONFIRMED**;
* the conditional **Hilbert trace-class** Schur--Fredholm proposition is
  **CONFIRMED with the exact factorization below**;
* the original abstract Banach phrase “every block is nuclear” is
  **GAPS / NOT REFUTED** as written; and
* q-generic common continuation, MMS/Hardy determinant identification,
  transformed tails, continuous contour, `K_s`, Selberg, and LAW remain
  **GAP / CONJECTURAL / OPEN**.

The exact Hilbert correction superseding the undefined `~` in §5 is as
follows.  For even q, let `G_i=I+N_i`, where the only nonzero block of `N_i`
is `(N_i)_{i,i-1}=A_i`, and put

~~~text
E_e = G_h G_{h-1} ... G_2.
~~~

Let `F_e` be the identity with terminal-column blocks
`(F_e)_{i,h}=C_i` for `i<h`.  Exact block multiplication gives

~~~text
E_e (I-L_s) F_e = diag(I,...,I,I-C_h).
~~~

For odd q, let `G_i=I+N_i`, now with
`(N_i)_{i,i-2}=A_i`, put `E_o=G_k...G_3`, and let `F_o` be the identity with

~~~text
(F_o)_{i,p}=P_i,  (F_o)_{i,k}=Q_i  for i<p.
~~~

Then exact block multiplication gives

~~~text
E_o (I-L_s) F_o = diag(I,...,I,R).
~~~

Under the stated Hilbert hypothesis, all perturbations in these products are
trace class; `E-I` and `F-I` are finite strictly triangular/nilpotent block
operators and have determinant one.  Simon (1977) Theorem 3.8, equation
(3.9), is the required multiplicativity result.  Simon Theorem 3.3 remains
the analyticity input, and Theorem 4.2, equation (4.2), remains the canonical
spectral-product input.  Thus, at exactly this conditional Hilbert scope,

~~~text
det_H(I-L_s) = det_H(I-C_h)  (even q),
det_H(I-L_s) = det_H(R)      (odd q).
~~~

No Banach determinant multiplication is consumed by this Hilbert-first proof.
To compare it with the MMS determinant on a connected continuation domain, a
future fixed-q or q-generic binding must still prove: a bounded identification
of the selected MMS sector with a Banach space `B` continuously embedded in
`H`; equality
of the actions on `B`; smoothing `L_H(H) subset B` so that all nonzero Jordan
chains transfer; Hilbert trace class; MMS order-`<=2/3` nuclearity; the same
sector/branch convention; and holomorphy of both normalized determinant
families on one common connected domain.  Those hypotheses are not supplied
by the finite checker and remain **GAP / CONJECTURAL** here.

Finally, the phrase in §4.1 calling Arb balls a ring is withdrawn.  The exact
complex matrices obey the determinant identity by row elimination; the Arb
runs independently enclose both evaluations and report that their difference
ball contains zero.  `contains_zero=True` is receipt evidence consistent with
the exact proof, not an equality proof by ball arithmetic.

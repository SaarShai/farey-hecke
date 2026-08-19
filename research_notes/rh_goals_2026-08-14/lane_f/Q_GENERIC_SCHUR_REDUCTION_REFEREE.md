# Cold referee: q-generic MMS Schur reduction

Date: 2026-08-19

Candidate reviewed: commit
`95dd8736f25bc71538d555eaacd7e5a01aa6c4c3`
(`Add q-generic Schur reduction checker`).

## Verdict

**PARTIAL CONFIRMATION; GAPS / NOT REFUTED overall for the q-generic
program.**

The following sharply bounded subresults are **CONFIRMED**:

1. the finite even and odd block eliminations, with the displayed
   noncommutative multiplication order;
2. the even sine partition identity and its two endpoint-width consequences;
3. the derivative recurrences, conditional on derivative blocks actually being
   supplied; and
4. provenance of the exact tracked engines consumed by the checker, together
   with a cold source-to-engine comparison of the equation-(32) and
   equation-(34) block placements; and
5. the **conditional Hilbert trace-class Schur-Fredholm proposition**, under
   the hypotheses stated in the candidate, after replacing its undefined `~`
   by the exact factorization proved in §§6-7.1 of this referee.

The submitted prose at `Q_GENERIC_SCHUR_REDUCTION_SOL.md:342-366` replaces the
needed exact factorization by an undefined `~`, omits the right unitriangular
factor, and `:369-377` cites the wrong Simon theorem for multiplicativity.  The
exact derivation below is a dated referee correction to those lines.  With that
correction, the conditional Hilbert proposition is **CONFIRMED**; the original
vague `~` must not be cited without this correction.

The MMS Banach setting also has a valid multiplicative Fredholm determinant,
but not by the cited Grothendieck 1952 Theorem 8 alone.  Grothendieck's 1956
*La théorie de Fredholm*, formula (4), is the missing multiplicativity result;
formula (11) is the matching invariant-direct-sum factorization.  For the
abstract Banach wording, `nuclear` must be strengthened to an actual
Grothendieck Fredholm kernel in the order-`<= 2/3` determinant algebra (the MMS
blocks are order zero).  A cleaner route keeps the Schur factorization wholly
on the Hilbert Hardy direct sum and compares to MMS only afterward by common
nonzero spectrum.  That comparison is exactly the q-generic linkage still
missing here; no direct Banach row elimination is needed for the confirmed
conditional Hilbert statement.

No q-generic disc family, contraction/tail bound, contour enclosure, `K_s`
nonvanishing result, Selberg quotient, or LAW conclusion is promoted.  The
candidate already marks those gates `GAP / CONJECTURAL` or `OPEN` at
`Q_GENERIC_SCHUR_REDUCTION_SOL.md:381-397,399-439,484-497`; those statuses are
preserved.

## 1. Checkout and review boundary

The candidate and clean starting point were pinned before review:

```text
$ git status --short --branch && git rev-parse HEAD
## codex/law-q-schur-referee-20260819
95dd8736f25bc71538d555eaacd7e5a01aa6c4c3
```

This referee reviewed only the solution, checker, tracked engine loops, the
MMS primary source, and the determinant sources needed for the conditional
operator proposition.  It does not treat a finite computation as proof of an
infinite determinant.

## 2. Finite block extraction and exact elimination

### 2.1 Even q

For `q=2h+2`, the candidate's block pattern is

```text
L[i,i-1] = A_i  (2 <= i <= h),
L[i,h]   = B_i  (1 <= i <= h).
```

This is the authoritative plain-text form at
`Q_GENERIC_SCHUR_REDUCTION_SOL.md:508-514`; the first TeX rendering was damaged
in transport and is explicitly superseded by the dated correction at
`:501-533`.

Put `T=I-L`.  Its rows are

```text
T row 1:  x_1 - B_1 x_h,
T row i:  x_i - A_i x_{i-1} - B_i x_h  (2 <= i <= h).
```

Apply, in increasing `i`,

```text
R_i <- R_i + A_i R_{i-1}.
```

If the transformed preceding row has terminal coefficient `-C_{i-1}`, the
new coefficient is

```text
-B_i + A_i(-C_{i-1}) = -(A_i C_{i-1}+B_i) = -C_i.
```

Thus the multiplication order is necessarily **left** multiplication by
`A_i`; no commutation of blocks is used.  The resulting flattened scalar
matrix is block upper triangular with diagonal

```text
I, ..., I, I-C_h,
```

so

```text
det(I_{hN}-M_N) = det(I_N-C_h).
```

This confirms `Q_GENERIC_SCHUR_REDUCTION_SOL.md:234-258` and the checker
implementation at `q_generic_schur_check.py:123-131`.

### 2.2 Odd q

For odd `q>=5`, put `k=kappa` and `p=k-1`.  The corrected pattern at
`Q_GENERIC_SCHUR_REDUCTION_SOL.md:516-524` is

```text
L[i,i-2] = A_i  (3 <= i <= k),
L[i,p]   = C_i  (1 <= i <= k),
L[i,k]   = B_i  (1 <= i <= k).
```

Starting with

```text
P_1=C_1, Q_1=B_1;  P_2=C_2, Q_2=B_2,
```

apply, in increasing `i`,

```text
R_i <- R_i + A_i R_{i-2}  (3 <= i <= k).
```

The two terminal coefficients become, with the same forced left order,

```text
P_i=A_i P_{i-2}+C_i,
Q_i=A_i Q_{i-2}+B_i.
```

Rows `p,k` on columns `p,k` are therefore exactly

```text
R = [[I-P_p, -Q_p],
     [-P_k, I-Q_k]].
```

The row-operation matrix has scalar determinant one.  Consequently

```text
det(I_{kN}-M_N) = det(R).
```

Again, this is ordinary determinant-preserving row elimination after the block
matrix is flattened over the commutative scalar field.  It does **not** use a
commutative-block determinant formula.  This confirms
`Q_GENERIC_SCHUR_REDUCTION_SOL.md:263-303` and
`q_generic_schur_check.py:134-164`.

### 2.3 Arb wording correction

The proof is exact over the underlying complex scalar matrices.  The sentence
at `Q_GENERIC_SCHUR_REDUCTION_SOL.md:260-261` calling Arb balls a `ring` and
saying that no approximation enters is too strong.  Ball arithmetic encloses
the two evaluations; `contains_zero=True` is not equality.  The candidate
itself correctly gives the latter caveat at `:478-482`.

Smallest textual repair:

> The flattened exact complex matrices obey the identity by row elimination.
> The Arb computations independently enclose the full and reduced
> determinants and verify that their difference ball contains zero.

This wording defect does not refute the exact algebraic proof.

## 3. Derivative recurrence and sine partition

Differentiating the already-confirmed noncommutative recurrences gives

```text
C_i' = A_i' C_{i-1} + A_i C_{i-1}' + B_i',
P_i' = A_i' P_{i-2} + A_i P_{i-2}' + C_i',
Q_i' = A_i' Q_{i-2} + A_i Q_{i-2}' + B_i'.
```

The order is correct, and differentiating the four entries of `R` completes
the algebra.  This confirms only the conditional statement at
`Q_GENERIC_SCHUR_REDUCTION_SOL.md:305-328`; the generic checker does not
construct derivative blocks, and no q-generic continuous-contour conclusion
follows.

For even `q=2h+2`, with `theta=pi/q`, substitution into
`y_{m+1}=-1/(lambda_q+y_m)` gives

```text
y_m = -sin(m theta)/sin((m+1) theta).
```

The identity

```text
2 cos(theta) sin((m+1)theta)-sin(m theta)
  = sin((m+2)theta)
```

proves the recurrence.  Since `h theta=pi/2-theta`, it gives

```text
y_h=-cos(theta)=-lambda_q/2,
y_1 -> -1/2,
y_{h-1}-y_h=sin(theta)^2/cos(theta) -> 0.
```

This confirms the even-family result at
`Q_GENERIC_SCHUR_REDUCTION_SOL.md:102-152,526-530`.  The explicit refusal to
infer a one-family odd formula at `:167-171` is correct.

## 4. Current tracked-engine provenance and MMS orientation

The current bytes and tracking status reproduce the candidate's hashes:

```text
$ shasum -a 256 \
    research_notes/rh_goals_2026-08-14/lane_g/law_probes/kaggle_boundary_rate/zeta_cert_rosen.py \
    research_notes/rh_goals_2026-08-14/lane_g/law_probes/kaggle_boundary_rate/zeta_cert_rosen_even.py \
    research_notes/rh_goals_2026-08-14/lane_g/law_probes/kaggle_boundary_rate/zeta_cert_rosen_q5.py \
    research_notes/rh_goals_2026-08-14/lane_f/q_generic_schur_check.py
965c2e5f65ae88b458d79bc425375e31589dcbf50703173664ef0e30901dceac  research_notes/rh_goals_2026-08-14/lane_g/law_probes/kaggle_boundary_rate/zeta_cert_rosen.py
693d2a88fd525e94c8ab6a63486e82fe0670d9dce142effbd5be5e324597212a  research_notes/rh_goals_2026-08-14/lane_g/law_probes/kaggle_boundary_rate/zeta_cert_rosen_even.py
c84c5c3f6d9f7a320bca7f1dbfd96a4859c3eea9b3de5420eb4eb223ad0d597b  research_notes/rh_goals_2026-08-14/lane_g/law_probes/kaggle_boundary_rate/zeta_cert_rosen_q5.py
c34814c6f0816f360b1f8c4b108a937fa72ad8803f5e133ebd3a86fb35e05965  research_notes/rh_goals_2026-08-14/lane_f/q_generic_schur_check.py

$ git ls-files --error-unmatch <the same four paths> | sed 's#^#TRACKED #'
TRACKED research_notes/rh_goals_2026-08-14/lane_f/q_generic_schur_check.py
TRACKED research_notes/rh_goals_2026-08-14/lane_g/law_probes/kaggle_boundary_rate/zeta_cert_rosen.py
TRACKED research_notes/rh_goals_2026-08-14/lane_g/law_probes/kaggle_boundary_rate/zeta_cert_rosen_even.py
TRACKED research_notes/rh_goals_2026-08-14/lane_g/law_probes/kaggle_boundary_rate/zeta_cert_rosen_q5.py
TRACKED_EXIT_CODE=0
```

The checker resolves only the in-worktree engine directory and prints both
module paths (`q_generic_schur_check.py:40-55,233-237`).  Both generic engines
import the tracked q5 primitives (`zeta_cert_rosen.py:76` and
`zeta_cert_rosen_even.py:96`).

A fresh MMS-v2 fetch reproduced the banked primary-source hash:

```text
$ curl -sSL https://arxiv.org/pdf/0912.2236v2 -o /tmp/mms-0912.2236v2.pdf
$ shasum -a 256 /tmp/mms-0912.2236v2.pdf
a10020bd084534dc60fc3e887958f1583f2fc115d567961b461df1a59b32e072  /tmp/mms-0912.2236v2.pdf
```

Cold comparison with MMS equation (32), p. 21, confirms the even orientation:
row 1 has `L_inf,+2` and sector-signed `L_inf,-1` in terminal column `h`;
rows `2..h` additionally have `L_+1` in column `i-1`.  The tracked code places
exactly these calls at `zeta_cert_rosen_even.py:228-236`.

Cold comparison with MMS equation (34), p. 21, confirms the odd orientation:

```text
row 1: L_+2 in p; L_inf,+3 in k; sign*L_-1 in p; sign*L_inf,-2 in k
row 2: L_inf,+2 in k; sign*L_-1 in p; sign*L_inf,-2 in k
row i: L_+1 in i-2 plus the row-2 terminal terms, 3 <= i <= k.
```

The tracked code implements those exact branch indices, signs, orientations,
and tail starts at `zeta_cert_rosen.py:214-230`.  The abstract block collection
in `Q_GENERIC_SCHUR_REDUCTION_SOL.md:191-217` is therefore correct for the
current pinned bytes.

The checker itself tests the nonzero coordinate pattern and determinant
identity of the matrix returned by those engines
(`q_generic_schur_check.py:99-120,193-230`); it does not independently decode
MMS branch labels.  The source-to-engine conclusion above is a separate cold
source audit, not an inflated interpretation of the numerical checker.

## 5. Independent checker reruns

### 5.1 Documented full run

```text
$ PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python \
    research_notes/rh_goals_2026-08-14/lane_f/q_generic_schur_check.py \
    --q 7 8 9 10 --N 4 8 --s 0.55+2.1i 0.63+4.3i --q8-speed
ENGINE_DIR=/Users/za/Documents/farey-hecke/.worktrees/law-q-schur-referee-20260819/research_notes/rh_goals_2026-08-14/lane_g/law_probes/kaggle_boundary_rate
ODD_ENGINE=/Users/za/Documents/farey-hecke/.worktrees/law-q-schur-referee-20260819/research_notes/rh_goals_2026-08-14/lane_g/law_probes/kaggle_boundary_rate/zeta_cert_rosen.py
EVEN_ENGINE=/Users/za/Documents/farey-hecke/.worktrees/law-q-schur-referee-20260819/research_notes/rh_goals_2026-08-14/lane_g/law_probes/kaggle_boundary_rate/zeta_cert_rosen_even.py
IMPORT_PATH_GUARD=PASS
SCHUR q=7 parity=odd N=4 s=0.55+2.1i full_dim=20 reduced_dim=8 pattern_ok=True difference_abs_upper=[2.8799780800578758739487404240085194861002294041734153388022434240627383675337517748479841e-87 +/- 4.59e-176] contains_zero=True build_s=0.024741 full_det_s=0.000649 reduced_det_s=0.000196 status=PASS
SCHUR q=8 parity=even N=8 s=0.63+4.3i full_dim=24 reduced_dim=8 pattern_ok=True difference_abs_upper=[2.5228322848552458714009722498594196025600950649416531813171750912374160281746838638219106e-78 +/- 3.14e-167] contains_zero=True build_s=0.053618 full_det_s=0.000736 reduced_det_s=0.000248 status=PASS
SCHUR q=9 parity=odd N=8 s=0.55+2.1i full_dim=56 reduced_dim=16 pattern_ok=True difference_abs_upper=[1.1590395272909361849058045765215734998135841999206152460302020324987604063577883679368949e-84 +/- 7.63e-174] contains_zero=True build_s=0.124435 full_det_s=0.020282 reduced_det_s=0.001296 status=PASS
SCHUR q=10 parity=even N=8 s=0.63+4.3i full_dim=32 reduced_dim=8 pattern_ok=True difference_abs_upper=[1.7871187093707067731039018149064783834673241575676530207984745287277697496017824103851059e-83 +/- 2.84e-172] contains_zero=True build_s=0.071466 full_det_s=0.003710 reduced_det_s=0.000344 status=PASS
Q8_SPEED N=16 s=0.4252310423737965+4.345760788321986i full_dim=48 reduced_dim=16 wall_s=0.227974 contains_zero=True status=PASS
OVERALL_STATUS=PASS failures=0
```

Only representative rows are reproduced above; the command is the full
cartesian run.  The checker increments `failures` on every bad pattern or
non-containing difference and returns nonzero when any occur
(`q_generic_schur_check.py:233-271`).  The quoted `failures=0` is finite
diagnostic evidence, not an infinite determinant theorem.

### 5.2 Opposite-sector and parity-edge run

```text
$ PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python \
    research_notes/rh_goals_2026-08-14/lane_f/q_generic_schur_check.py \
    --q 5 6 11 12 --N 3 --s 0.71+1.9i --sign-odd -1 --sign-even -1
IMPORT_PATH_GUARD=PASS
SCHUR q=5 parity=odd N=3 s=0.71+1.9i full_dim=9 reduced_dim=6 pattern_ok=True difference_abs_upper=[3.6653486036357317189438659023616537766015087947025802589312064676105038415869536011131385e-88 +/- 3.67e-177] contains_zero=True build_s=0.008486 full_det_s=0.001859 reduced_det_s=0.000073 status=PASS
SCHUR q=6 parity=even N=3 s=0.71+1.9i full_dim=6 reduced_dim=3 pattern_ok=True difference_abs_upper=[4.6107364039517613855005277995966385862509230566749656383905257957691636897315381864910046e-87 +/- 4.95e-177] contains_zero=True build_s=0.005280 full_det_s=0.000039 reduced_det_s=0.000024 status=PASS
SCHUR q=11 parity=odd N=3 s=0.71+1.9i full_dim=27 reduced_dim=6 pattern_ok=True difference_abs_upper=[1.0545323395079463253361967842642219512400599080003908022965935469978909627422390531329219e-87 +/- 3.75e-176] contains_zero=True build_s=0.022223 full_det_s=0.000404 reduced_det_s=0.000169 status=PASS
SCHUR q=12 parity=even N=3 s=0.71+1.9i full_dim=15 reduced_dim=3 pattern_ok=True difference_abs_upper=[8.0899998734791462833756978732245899828950173265639289544641200571612040151855011525332858e-88 +/- 1.06e-177] contains_zero=True build_s=0.012532 full_det_s=0.000122 reduced_det_s=0.000048 status=PASS
OVERALL_STATUS=PASS failures=0
EXIT_CODE=0
```

## 6. First load-bearing gap: exact infinite factorization

Let `D=I-L_s`.  The following is the smallest complete replacement for the
undefined similarities at `Q_GENERIC_SCHUR_REDUCTION_SOL.md:342-366`.

### 6.1 Even factorization

For `2 <= i <= h`, let `N_i` have the single block

```text
(N_i)_{i,i-1}=A_i
```

and put

```text
G_i=I+N_i,
E_e=G_h G_{h-1} ... G_2.
```

The order is the order of the sequential row operations.  Exact multiplication
gives

```text
E_e D = U_e,
```

where

```text
(U_e)_{ii}=I                         (i<h),
(U_e)_{i,h}=-C_i                     (i<h),
(U_e)_{h,h}=I-C_h,
all other blocks are zero.
```

In particular, relative to `(direct sum_{i<h} H_i) direct-sum H_h`,

```text
U_e = [[I, X_e],
       [0, I-C_h]],
X_e = column(-C_1,...,-C_{h-1}).
```

Now let `F_e` be identity except

```text
(F_e)_{i,h}=C_i  (i<h).
```

Then `(F_e-I)^2=0`, and direct multiplication—not similarity—gives

```text
E_e (I-L_s) F_e = diag(I,...,I,I-C_h).                 (6.1)
```

Equivalently, one may factor

```text
U_e = diag(I,I-C_h) [[I,X_e],[0,I]],
```

which does not require `I-C_h` to be invertible.

### 6.2 Odd factorization

For `3 <= i <= k`, let `N_i` have the single block

```text
(N_i)_{i,i-2}=A_i
```

and put

```text
G_i=I+N_i,
E_o=G_k G_{k-1} ... G_3.
```

Exact multiplication gives

```text
E_o D = U_o.
```

Every nonterminal row `i<p` has `I` in column `i`, `-P_i` in column
`p`, and `-Q_i` in column `k`.  The terminal `p,k` rows are exactly

```text
R = [[I-P_p, -Q_p],
     [-P_k, I-Q_k]].
```

Thus, relative to the nonterminal direct sum and `H_p direct-sum H_k`,

```text
U_o = [[I, X_o],
       [0, R]],
```

where row `i` of `X_o` is `[-P_i,-Q_i]`.  Let `F_o` be identity except

```text
(F_o)_{i,p}=P_i,
(F_o)_{i,k}=Q_i                       (i<p).
```

Again `(F_o-I)^2=0`, and

```text
E_o (I-L_s) F_o = diag(I,...,I,R).                     (6.2)
```

Equations (6.1)-(6.2) expose every sign, orientation, and noncommutative
product.  They are the derivation currently missing from the solution.

## 7. Determinant-class audit

### 7.1 Hilbert trace-class realization

Under the candidate's Hilbert hypothesis that every displayed block is trace
class:

- each `N_i` is trace class and square-zero;
- each finite product `E_e-I` or `E_o-I` is trace class;
- `F_e-I` and `F_o-I` are finite block matrices of trace-class terminal
  coefficients and are square-zero;
- `L_s`, `C_h`, and `R-I` are trace class; and
- all factors in (6.1)-(6.2) therefore lie in `I + S_1`.

The nilpotent perturbations have determinant one.  Barry Simon,
*Notes on infinite determinants of Hilbert space operators*, Adv. Math. 24
(1977), has the precise roles:

```text
Theorem 3.3: trace-class-valued analyticity;
Theorem 3.8, equation (3.9): determinant multiplicativity;
Theorem 4.2, equation (4.2), p. 258: canonical spectral product.
```

Thus multiplicativity applied to (6.1)-(6.2) yields

```text
det(I-L_s)=det(I-C_h)                 (even),
det(I-L_s)=det(R)                     (odd).
```

The candidate's `Q_GENERIC_SCHUR_REDUCTION_SOL.md:369-377` incorrectly
attributes multiplicativity to Theorems 3.3 and 4.2; the needed theorem is
3.8.  Sections 6-7.1 of this cold referee supply the missing derivation and
source correction, so the conditional Hilbert proposition is **CONFIRMED**.
Any later ledger citation must include this correction rather than citing the
candidate's undefined `~` alone.

### 7.2 MMS/Grothendieck Banach realization

The candidate's Grothendieck 1952 citation supplies the spectral-product
identification, not the multiplication law.  A fresh primary-source fetch gave:

```text
$ curl -sSL https://numdam.org/item/10.5802/aif.46.pdf \
    -o /tmp/grothendieck-aif-1952-46.pdf
$ shasum -a 256 /tmp/grothendieck-aif-1952-46.pdf
03834fc3c5f82c047c718811aa7672f79de30a2b7004290149382c49242f3118  /tmp/grothendieck-aif-1952-46.pdf
$ pdfinfo /tmp/grothendieck-aif-1952-46.pdf | rg '^(Title|Author|Pages):'
Title:           Résumé des résultats essentiels dans la théorie des produits tensoriels topologiques et des espaces nucléaires
Author:          Alexander Grothendieck
Pages:           41
```

After `pdftotext -layout`, Theorem 8 at extracted lines 1457-1464 states that
for `p<=2/3` the determinant is genus zero and equals the eigenvalue product.
That is the role correctly used by the q5 common-spectrum precedent at
`lane_g/TB_R5_DETERMINANT_IDENTIFICATION.md:118-136`; it is not, by itself,
the left/right factor multiplicativity used here.

The missing law is in Grothendieck, *La théorie de Fredholm*, Bull. Soc. Math.
France 84 (1956), pp. 319-384, DOI `10.24033/bsmf.1476`.  Fresh receipt:

```text
$ curl -sSL https://www.numdam.org/article/BSMF_1956__84__319_0.pdf \
    -o /tmp/groth-fredholm-1956.pdf
$ shasum -a 256 /tmp/groth-fredholm-1956.pdf
ed38ba04cb7b00848a9e4fa73860efaae76b64873c15aa8a26cd5715d713f9f1  /tmp/groth-fredholm-1956.pdf
$ pdfinfo /tmp/groth-fredholm-1956.pdf | rg '^(Title|Author|Pages):'
Title:           La théorie de Fredholm
Author:          Alexander Grothendieck
Pages:           67
$ pdftotext -layout /tmp/groth-fredholm-1956.pdf - \
    | nl -ba | sed -n '1517,1524p;1685,1700p'
1517  tion définie sur l'hyperplan 1 + E ' (g) E de l'algèbre T (obtenue par adjonc-
1518  tion d'une unité à E ' ( ^ E ) ^ hyperplan stable par multiplication, et l'on a :.
1519  (4)              d é t ( l + ^ ) ( l + F ) = : d é t ( l +^-)dét(l +(-'),
1521  formule qui pourrait s'écrire
1522                             D(u -+-(•+ m ' ) = D(u) D(^).
1685       Nous allons montrer que si u est tel que iï laisse invariant E\ ou E^ on a
1686  (n)           det(l -4- u) ==dét(l 4- M i ) d é t (l 4- u-i)     (Ui=pii/pi)'
1695                         1 + // == 1 4- ^4- w == (l -\-v) (l -+- w)
1698                          dét(l + u) = dét(l + P) dét(l -4- w).
```

The formula at line 1519 is normalized here into unambiguous parentheses; the
PDF's displayed typography and following prose make that grouping explicit.

For the **actual MMS** Banach system, MMS Theorem 4.10 supplies an order-zero
Fredholm kernel for the full operator.  Bounded coordinate projections and
inclusions, finite direct sums, complemented-sector restriction from MMS Lemma
5.1, and bounded conjugacy preserve order-zero nuclearity.  Consequently, once
the selected reduced operator is actually identified with that MMS sector, all
`A_i,B_i,C_i,P_i,Q_i`, `E-I`, `F-I`, and terminal perturbations lie in the same
order-zero Fredholm-kernel algebra.  Grothendieck 1956 formula (4) applies to
(6.1)-(6.2); formula (11) applies to the terminal direct sum; Grothendieck 1952
Theorem 8 gives determinant one for the nilpotent order-zero factors.

The abstract phrase `every ... block is nuclear` at
`Q_GENERIC_SCHUR_REDUCTION_SOL.md:334-340` is nevertheless too weak on an
arbitrary Banach space: a plain 1-nuclear operator need not furnish the unique
order-`<=2/3` spectral determinant used here.  The exact smallest replacement
is:

> On the Banach realization, every displayed block is represented by a
> Grothendieck Fredholm kernel of order at most `2/3` in the common
> multiplicative kernel algebra, and all block coordinate maps/conjugacies are
> bounded.  In the MMS application these kernels are of order zero.

Alternatively, one may assume a Banach approximation/uniqueness property and
state explicitly that the operator determinant agrees with this kernel
determinant.  Merely saying `relevant determinant class` for `I-L_s` does not
show that the elementary row factors belong to that class.

### 7.3 Cleaner Hilbert-first bridge to MMS

Direct Banach multiplicativity is not needed for the downstream identification.
The confirmed conditional proposition may be kept entirely on the Hilbert
Hardy direct sum:

1. prove (6.1)-(6.2) and the terminal determinant identity in Hilbert trace
   class using Simon Theorem 3.8;
2. on a nonempty base domain `Omega_0`, identify the Hilbert and MMS Banach
   determinants from their common nonzero spectrum with algebraic
   multiplicity, using Simon Theorem 4.2 and Grothendieck 1952 Theorem 8; and
3. extend equality only after proving both determinant families holomorphic on
   one connected common continuation domain `Omega*`.

The exact common-spectrum hypothesis is more than equality of formal branch
labels.  It requires a bounded identification of the selected MMS reduced
`P`-sector with a Banach space `B` continuously embedded in the Hardy space
`H`, equality of the two operator actions on `B`, and smoothing

```text
L_H(H) subset B.
```

For every nonzero eigenvalue `lambda`, this sends an eigenvector into `B` by
`v=lambda^{-1}L_H v`.  Inductively, it sends an entire Jordan chain into `B`
by

```text
v_j=lambda^{-1}(L_H v_j-v_{j-1}).
```

The converse uses `B subset H`.  Hence the nonzero spectra, including
algebraic multiplicities, agree.  One also needs Hilbert trace class, Banach
order-`<=2/3`, exact sector/branch conjugacy, and normalized spectral
determinants on `Omega_0`.

This is the fixed-q mechanism proved in the q5 precedent
`lane_g/TB_R5_DETERMINANT_IDENTIFICATION.md:100-136`.  The present candidate
explicitly leaves its q-generic analogue and common continuation as
`GAP / CONJECTURAL` at `Q_GENERIC_SCHUR_REDUCTION_SOL.md:381-391`.  Therefore
the Hilbert Schur proposition is confirmed, while the q-generic MMS bridge is
not.

## 8. Banked scope and required ledger correction

The proof now cold-confirmed is the conditional Hilbert statement consisting
of the candidate hypotheses together with §§6-7.1 above.  Before the solution
ledger restates it, append a dated correction containing:

1. the literal definitions of `G_i,E_e,E_o,F_e,F_o` above;
2. the exact equalities `E(I-L)=U` and `E(I-L)F=diag(...)`;
3. the Hilbert trace-class membership of `E-I` and `F-I`;
4. Simon Theorem 3.8 for Hilbert multiplicativity, with Theorems 3.3 and 4.2
   kept in their analyticity and spectral-product roles; and
5. an explicit statement that q-generic MMS identification still requires the
   common-spectrum/common-continuation hypotheses in §7.3.

If a future proof instead performs row elimination directly on the MMS Banach
space, it must additionally use the order-`<=2/3` kernel hypothesis and
Grothendieck 1956 formulas (4) and (11) audited in §7.2.  That route is
optional, not an unstated prerequisite of the Hilbert-first proof.

The confirmed conditional lemma does **not** close the candidate's
already-listed q-generic strict-disc,
Hardy/Banach common-continuation, transformed-tail, continuous-contour,
`K_s`, Selberg, or arithmetic-transport gaps.

## 9. Blast radius

The finite Schur evaluator may be used as a dimension reduction for the current
pinned finite matrices.  It cannot be cited as an infinite Fredholm-tail bound
or as a q-generic MMS determinant identification.

The first downstream consumer blocked by this referee is any proof that replaces
the full infinite determinant by the terminal `N`- or `2N`-dimensional Schur
object without separately proving:

```text
fixed-q operator identification
  -> common determinant realization
  -> transformed nuclear/Fredholm tail
  -> continuous contour enclosure
  -> K_s nonvanishing
  -> MMS/Selberg quotient.
```

No currently banked q=5 or q=7 fixed-q theorem is refuted by this ruling.  No
q-generic analytic or LAW status may be upgraded from the finite checker.

## 10. Referee status

**FINITE ALGEBRA: CONFIRMED.**

**CONDITIONAL HILBERT SCHUR-FREDHOLM PROPOSITION, WITH §§6-7.1 REFEREE
CORRECTION: CONFIRMED.**

**DIRECT ABSTRACT BANACH WORDING AS SUBMITTED: GAPS / NOT REFUTED; OPTIONAL
ORDER-`<=2/3` REPAIR GIVEN IN §7.2.**

**q-GENERIC ANALYTIC LINKAGE AND DOWNSTREAM LAW: GAP / CONJECTURAL / OPEN,
UNCHANGED.**

### Pre-commit hygiene receipt

```text
$ git diff --cached --check; rc=$?; echo DIFF_CHECK_EXIT=$rc; git status --short
DIFF_CHECK_EXIT=0
A  research_notes/rh_goals_2026-08-14/lane_f/Q_GENERIC_SCHUR_REDUCTION_REFEREE.md
```

**READY FOR JUDGING.**

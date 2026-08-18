# M1 Route B — free-product double-coset normal forms

**Status (2026-08-18).** Route B gives a paper proof of a corrected M1 at the
abstract double-coset level.  It does not use Rosen expansions, geodesic
coding, or rank matching.

The outcome is sharper than the proposed formulation:

* **FALSE:** at finite `q`, there is no unique alternating normal form in
  `Q` and `S`-powers.  The relation `(QS)^q=1` is already a counterexample.
  The free factors are `Q` and `R:=QS`, so the unique element normal form is
  in `Q` and nontrivial `R`-powers.
* **FALSE:** deleting visible leading/trailing `S`-powers does not give a
  unique double-coset word.  The three distinct reduced words `Q`, `R`, and
  `R^{-1}` lie in the same `<S>`-double coset.
* **PROVED below:** after one exceptional convention for that class, every
  `<S>`-double coset has a unique explicit `Q,R` word.  Balanced residue
  lifting then defines an injective section from finite-`q` double cosets to
  theta double cosets.
* **PROVED below:** the image consists exactly of theta canonical words whose
  `R`-exponents lie in a balanced residue alphabet.  It contains every Hejhal
  class with

  ```text
  c_H <= c_*^H(q) := ceil(q/2) - 1,
  ```

  and every omitted theta class has `c_H >= ceil(q/2)`.
* **FALSE:** the earlier two-sided localization
  `min(c_q(replay_q(w)),2c_H(w)) >= kappa q` for every first-wrap word.
  The theta canonical word `R^q` is first-wrap, but it replays to the identity
  in `G_q`, so its finite lower-left entry is zero.  The correct output is a
  **one-sided theta-tail bound**; under the section pairing there is no finite
  unmatched class.

Thus M1-W, M1-I, M1-S, and a corrected M1-L are proved combinatorially.  A
uniform derivative/summability estimate for the paired terms remains R2, not
M1.  Completeness of the finite real-matrix key itself is isolated at the end
as a separate **CONJECTURAL** cusp-stabilizer lemma; it is not needed for the
section or its injectivity.

## 1. Receipts before claims

### 1.1 Exact `[1,2]` / `[2,1]` negative control

This was checked first, in the conjugated normalization

```text
Q_2 = [[0,-1/2],[2,0]],       S = [[1,1],[0,1]].
```

Command (exact rational arithmetic):

```bash
/Users/za/.venvs/farey-rh/bin/python - <<'PY'
from fractions import Fraction as F

def mm(A,B):
    return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))
def mpow(A,n):
    if n < 0:
        A=((A[1][1],-A[0][1]),(-A[1][0],A[0][0])); n=-n
    Z=((F(1),F(0)),(F(0),F(1)))
    while n:
        if n & 1: Z=mm(Z,A)
        A=mm(A,A); n//=2
    return Z

Q=((F(0),F(-1,2)),(F(2),F(0)))
S=((F(1),F(1)),(F(0),F(1)))
def raw(ns):
    A=Q
    for n in ns: A=mm(mm(A,mpow(S,n)),Q)
    return A

for w in ([1,2],[2,1]):
    A=raw(w); C=A[1][0]; D=A[1][1]
    print(w,A,(C,D%C),(C/2,D%C))
PY
```

Output:

```text
[1, 2] ((Fraction(-4, 1), Fraction(1, 2)), (Fraction(14, 1), Fraction(-2, 1))) (Fraction(14, 1), Fraction(12, 1)) (Fraction(7, 1), Fraction(12, 1))
[2, 1] ((Fraction(-2, 1), Fraction(1, 2)), (Fraction(14, 1), Fraction(-4, 1))) (Fraction(14, 1), Fraction(10, 1)) (Fraction(7, 1), Fraction(10, 1))
```

Therefore the old `c`-only map really collides, while the source-coordinate
theta keys are `(7,12)` and `(7,10)` and do separate the two theta double
cosets.  Direct multiplication at a symbolic nonzero `lambda` gives

```text
Q S^n Q S^m Q
  = [[-m lambda, 1/lambda],
     [lambda(nm lambda^2-1), -n lambda]].
```

The equal lower-left entry depends only on `nm`; the lower-right entry keeps
the ordered information.  In `Q,R` double-coset normal form at theta level,

```text
[1,2]  represents  R^2 Q R^2,
[2,1]  represents  R Q R^3.
```

These are distinct canonical words below, exactly as their keys require.

### 1.2 Printed theta double-coset source

The local source is
[`Hejhal_LNM1001_Vol2_ch11s3_pp524-532.pdf`](../lane_p/literature/Hejhal_LNM1001_Vol2_ch11s3_pp524-532.pdf).
The second scan page is printed p. 525 and was visually inspected as well as
text-extracted.  Receipt:

```bash
pdfinfo research_notes/rh_goals_2026-08-14/lane_p/literature/Hejhal_LNM1001_Vol2_ch11s3_pp524-532.pdf | rg '^Pages:'
pdftotext -f 2 -l 2 -layout research_notes/rh_goals_2026-08-14/lane_p/literature/Hejhal_LNM1001_Vol2_ch11s3_pp524-532.pdf - | sed -n '14,42p'
```

Relevant output (the OCR damages the inequality glyphs; the scan visibly
reads `0 <= d < 2c`):

```text
Pages:           9

         LEMMA 3.1.      Consider ordered pairs             <cd>        such that     c > 0 , 0 ;'£ d -c 2c,     c + d:= 1

mod 2          and    (c,d) = 1.       Let     K
                                                   cd
                                                        be ANY matrix in        r whose bottom row is            cd.
...
as a DISJOINT union of double cosets.
```

Thus, excluding the trivial parabolic double coset, Hejhal's Lemma 3.1 gives
the theta bijection

```text
H_infty \ G_infty / H_infty
  <-> {(c_H,d_H): c_H>0, 0<=d_H<2c_H,
                    gcd(c_H,d_H)=1, c_H+d_H odd}.
```

Here `H_infty=<S>`.  Under the conjugation used in the RATE files, a source
matrix `[[a,b],[c_H,d_H]]` becomes
`[[a,b/2],[2c_H,d_H]]`.  Hence the conjugated key is
`(2c_H,d_H mod 2c_H)`, not `(c_H,d_H mod c_H)`.

### 1.3 Lean receipts actually used

The filled v27 result file is
[`RateCoreII.lean`](../../../projects/aristotle_dispatch_v27/result/project_aristotle/RateCoreII.lean),
not the dispatch seed containing `sorry`.  It was checked with the already
materialized v26 Mathlib environment:

```bash
cd projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle
lake env lean ../../../aristotle_dispatch_v27/result/project_aristotle/RateCoreII.lean; code=$?; echo "RATECOREII_EXIT=$code"
```

Output:

```text
../../../aristotle_dispatch_v27/result/project_aristotle/RateCoreII.lean:173:36: warning: unused variable `hc`

Note: This linter can be disabled with `set_option linter.unusedVariables false`
RATECOREII_EXIT=0
```

The axiom-audit command was:

```bash
lake env lean -R /Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v27/result/project_aristotle \
  -o /tmp/RateCoreII.olean \
  /Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v27/result/project_aristotle/RateCoreII.lean
LEAN_PATH=/tmp lake env lean --stdin <<'LEAN'
import RateCoreII
#print axioms RateCoreII.c_depth_three
#print axioms RateCoreII.wordLimitMap_not_injective_depth_three
#print axioms RateCoreII.wordMatrix_two_form
#print axioms RateCoreII.c_two_even
#print axioms RateCoreII.theta_coset_count
LEAN
```

Output:

```text
'RateCoreII.c_depth_three' depends on axioms: [propext, Classical.choice, Quot.sound]
'RateCoreII.wordLimitMap_not_injective_depth_three' depends on axioms: [propext, Classical.choice, Quot.sound]
'RateCoreII.wordMatrix_two_form' depends on axioms: [propext, Classical.choice, Quot.sound]
'RateCoreII.c_two_even' depends on axioms: [propext, Classical.choice, Quot.sound]
'RateCoreII.theta_coset_count' depends on axioms: [propext, Classical.choice, Quot.sound]
```

The v26 result file
[`RateCore.lean`](../../../projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle/RateCore.lean)
also rebuilt with the following receipt:

```bash
lake env lean RateCore.lean; code=$?; echo "RATECORE_EXIT=$code"
```

```text
RateCore.lean:263:32: warning: unused variable `hq`

Note: This linter can be disabled with `set_option linter.unusedVariables false`
RateCore.lean:415:31: warning: unused variable `hlam`

Note: This linter can be disabled with `set_option linter.unusedVariables false`
RATECORE_EXIT=0
```

The specific-results axiom audit was

```bash
lake env lean --stdin <<'LEAN'
import RateCore
#print axioms RateCore.c_eq_scaled_int_poly
#print axioms RateCore.c_chebyshevWord
#print axioms RateCore.c_chebyshevWord_two
LEAN
```

and gave:

```text
'RateCore.c_eq_scaled_int_poly' depends on axioms: [propext, Classical.choice, Quot.sound]
'RateCore.c_chebyshevWord' depends on axioms: [propext, Classical.choice, Quot.sound]
'RateCore.c_chebyshevWord_two' depends on axioms: [propext, Classical.choice, Quot.sound]
```

What these receipts provide, and no more, is:

* the depth-three formula and the failure of the old word-level injection;
* the theta matrix shape `[[a,b/2],[2c,d]]` with integral `a,b,c,d`;
* even conjugated lower-left entries at theta;
* the fixed-height multiplicity `phi(2c_H)`;
* integer-polynomial/Laurent control for a fixed word;
* the exact Chebyshev formula for the all-ones subfamily.

They do **not** formalize the double-coset normal-form theorem proved next.

## 2. Correct free-product object

Work in PSL and put

```text
R := Q S,       S = Q R.
```

Then

```text
G_q      = <Q,R | Q^2=1, R^q=1> = C_2 * C_q,
G_infty  = <Q,R | Q^2=1>         = C_2 * Z,
H_q      = <S> = <QR>.
```

The statement “unique alternating normal form in `Q` and `S`-powers” is
therefore **FALSE** at finite `q`; `(QS)^q=R^q=1` is a nonempty raw word for
the identity.  The true free-product theorem says that every element has a
unique reduced word alternating between `Q` and nonidentity `R`-powers.

The subgroup being quotiented is `<QR>`, not a free factor.  Consequently,
element normal form alone does not yet solve the double-coset problem.

## 3. Canonical `<S>`-double-coset normal form

Write exponents in `C_q=Z/qZ` at finite level and in `Z` at theta level.
All exponent equalities in this section are interpreted in that group.

### Theorem 3.1 (explicit bireduced normal form) — PROVED

Every double coset in `H_q\G_q/H_q` has exactly one representative in the
following list:

1. `1`, for the trivial double coset `H_q`;
2. `Q`, for the exceptional class
   `H_q Q H_q = H_q R H_q = H_q R^{-1} H_q`;
3. a reduced word

   ```text
   R^{a_0} Q R^{a_1} Q ... Q R^{a_k},       k >= 0,
   ```

   where every `a_i` is nonzero, `a_0 != -1`, `a_k != 1`, and, when
   `k=0`, both endpoint restrictions apply (`a_0 != +/-1`).

The same statement holds for `q=infinity`.

#### Proof: existence

Start with the unique reduced free-product word.  The following boundary
operations preserve its `<S>`-double coset and strictly decrease syllable
length, except in the displayed one-syllable exceptional class:

```text
leading Q R^a ...       : multiply on the left by S^{-1}=R^{-1}Q;
leading R^{-1} Q ...    : multiply on the left by S=QR;
... R^a Q trailing      : multiply on the right by S=QR;
... Q R trailing        : multiply on the right by S^{-1}=R^{-1}Q.
```

For example,

```text
S^{-1} Q R^a ... = R^{a-1} ...,
... R^a Q S      = ... R^{a+1}.
```

If an exponent becomes zero, ordinary free-product reduction continues and
decreases the length further.  The process terminates.  A terminal word is
either `1`, one of `Q,R,R^{-1}`, or has exactly the form in item 3.  The
identities

```text
Q S = R,             S^{-1} Q = R^{-1}
```

put the three one-syllable words in one class; choose `Q`.

#### Proof: uniqueness

Let `w` have the form in item 3.  Since its first exponent is not `-1`,
left multiplication by a positive power of `S=(QR)` cannot cancel through
the left boundary.  Left multiplication by a negative power ends in `Q`
and likewise cannot cancel through the initial `R`-syllable.  Thus every
nontrivial left multiplier either increases reduced length or leaves an
uncancelled boundary block.  The terminal condition `a_k != 1` gives the
right-hand analogue.  A direct boundary reduction of `S^m w S^n` therefore
shows that it can be another item-3 word of the same length only when
`m=n=0`.  Unique free-product normal form then gives equality of the words.

For a one-syllable `R^a` with `a!=0,+/-1`, the same boundary check applies.
For the exceptional class, `Q,R,R^{-1}` are its only shortest reduced
representatives, and the convention chooses `Q`.  The trivial class is
immediate.  This proves uniqueness.  `square`

This theorem also proves that the suggested criterion “no visible
leading/trailing `S`-power” is insufficient: `Q`, `R`, and `R^{-1}` all pass
that superficial test but represent the same double coset.

## 4. Theta key and a height lemma from the canonical word

Hejhal's disjoint decomposition proves that the source-coordinate map

```text
thetaKey([g]) = (c_H, d_H mod 2c_H),       c_H>0,
```

is a bijection from nontrivial theta double cosets to the admissible data in
Section 1.2.  Composing it with Theorem 3.1 gives the requested bijection
from canonical words to Hejhal data at `lambda=2`.

The following new elementary estimate turns the word parametrization into
localization.

### Lemma 4.1 (canonical digits are bounded by theta height) — PROVED

Let

```text
w = R^{a_0} Q R^{a_1} Q ... Q R^{a_k}
```

be a canonical theta word of item 3, and let `c_H(w)` be the absolute source
lower-left entry after the PSL sign is chosen.  Then

```text
c_H(w) >= max_i |a_i|.
```

#### Proof

Use source-coordinate matrices

```text
Q = [[0,-1],[1,0]],      S = [[1,2],[0,1]],
R = QS = [[0,-1],[1,2]].
```

Induction gives, for every integer `a`,

```text
R^a = [[1-a,-a],[a,1+a]].
```

After the prefix ending in `R^{a_j}`, write its bottom row as `(c_j,d_j)`
and set

```text
U_{-1}=-1,
U_0=2a_0+1,
U_j=-2a_j U_{j-1}-U_{j-2}.
```

Right multiplication by `Q R^{a_j}` sends

```text
(c,d) -> (d-a_j(c+d), -c-a_j(c+d)).
```

Therefore

```text
c_j=(U_j+U_{j-1})/2,      d_j=(U_j-U_{j-1})/2.
```

The initial restrictions `a_0!=0,-1` give `|U_0|> |U_{-1}|`.  Since every
later `a_j` is a nonzero integer,

```text
|U_j| >= 2|U_{j-1}|-|U_{j-2}| > |U_{j-1}|.
```

At the last digit, `a_k!=0,1`, hence `|2a_k-1|>=3`, and

```text
2c_k = -(2a_k-1)U_{k-1}-U_{k-2}
```

implies `|c_k|>|U_{k-1}|`.  The same recurrence gives
`|U_j|>=2|a_j|` for every interior digit, while
`|U_0|=|2a_0+1|>=|a_0|`.  For the terminal digit, put
`A=|U_{k-1}|>=3` and `B=|U_{k-2}|<A`.  Then

```text
2|c_k| >= |2a_k-1| A-B > (|2a_k-1|-1)A.
```

If `a_k>=2`, the last expression is `2(a_k-1)A`; if `a_k<=-1`, it is
`2|a_k|A`.  In both cases `|c_k|>=|a_k|`.  Hence `|c_k|` dominates every
digit.  For the singleton case `k=0`, the formula for `R^{a_0}` gives
`c_H=|a_0|` directly.  `square`

The exceptional word `Q` has no `R`-digit and causes no exception to the
later localization statement.

## 5. Balanced lift and exact image

Fix the balanced residue section

```text
A_q = {-floor((q-1)/2),..., -1, 1,...,floor(q/2)}.
```

It contains exactly one nonzero representative of every nonzero residue
modulo `q`; when `q` is even, the order-two residue is represented by the
positive endpoint.

Let

```text
pi_q : G_infty -> G_q
```

be the quotient imposing `R^q=1`.  For a finite canonical word from Theorem
3.1, replace every nonzero `R`-residue by its representative in `A_q` and
interpret the resulting word in `G_infty`.  Call this lift `iota_q`.  The
endpoint restrictions are preserved, so `iota_q(w)` is already a theta
canonical word.  Define

```text
L_q(X) := H_infty iota_q(NF_q(X)) H_infty.
```

### Theorem 5.1 (section, injection, and image) — PROVED

The induced projection on double cosets satisfies

```text
bar(pi_q)(L_q(X)) = X.
```

Consequently `L_q` is injective on **all** nontrivial finite double cosets.
Moreover,

```text
im(L_q)
 = {theta double cosets whose canonical R-exponents all lie in A_q}.
```

#### Proof

Projection reduces each lifted exponent to the original residue, so it
recovers the finite canonical word.  This proves the section identity.  If
`L_q(X)=L_q(Y)`, applying `bar(pi_q)` gives `X=Y`.

Conversely, a theta canonical word with all exponents in `A_q` remains a
finite canonical word after projection: no exponent becomes zero and the two
endpoint exclusions persist.  Balanced lifting restores the original word.
This proves the image characterization.  `square`

This argument is the main Route B simplification.  It avoids trying to prove
injectivity from the lower-left entry or from numerical rank matching.
Injection follows formally from “right inverse to a quotient.”

### Corollary 5.2 (explicit Hejhal subrange) — PROVED

Put

```text
c_*^H(q) = ceil(q/2)-1.
```

Every Hejhal theta class with `c_H<=c_*^H(q)` belongs to `im(L_q)`.

Indeed, Lemma 4.1 bounds every canonical digit by `c_H`.  Digits of a class
in this range therefore lie in `A_q`, and Theorem 5.1 applies.  This is
surjectivity by inverse normal-form projection, not by sorted-spectrum rank.

### Corollary 5.3 (exact first-wrap localization) — PROVED

For an omitted theta class, define `firstWrap_q` as the first exponent in its
canonical word which is not in `A_q`.  Then

```text
H_infty \ im(L_q)
 = {H : the canonical word of H has firstWrap_q},

H notin im(L_q)  ==>  c_H(H) >= ceil(q/2).
```

The first equality is Theorem 5.1.  The smallest absolute value of an integer
outside `A_q` is `ceil(q/2)`; Lemma 4.1 gives the height bound.  Thus the
one-sided localization constant can be taken to be `kappa=1/2` after rounding
the integer height downward in the safe direction.

## 6. The four M1 obligations

### M1-W — well-definedness: PROVED (with one separate caveat)

For a matrix `g=[[a,b],[c,d]]`, left multiplication by `S^u` fixes `(c,d)`;
right multiplication by `S^v` sends `(c,d)` to `(c,d+vc)`.  Hence
`(c,[d]_c)` is an invariant of a finite double coset after the PSL sign
`c>0` is chosen.

Theorem 3.1 makes `NF_q` independent of the raw `Q,S` spelling.  Balanced
lifting and evaluation at `lambda=2` then give a unique theta canonical word,
and Hejhal's lemma gives a unique theta key.  Therefore `L_q` is well-defined.

**CONJECTURAL auxiliary statement not used here:** equality of two finite
real-matrix keys implies equality of finite double cosets.  The missing
purely algebraic lemma is

```text
Stab_{G_q}(infinity) = <S>.
```

Given that lemma, equal keys make one matrix differ from the other by a right
integer `S`-power and then by an upper-unipotent element of `G_q`, which the
stabilizer lemma forces to be a left `S`-power.  Free-product normal form by
itself does not identify the Möbius stabilizer of infinity, and none of the
listed Lean identities proves this lemma.  It should not be silently folded
into M1-W.

### M1-I — injectivity: PROVED, stronger than requested

Theorem 5.1 proves injectivity on every finite double coset, not just a
height-truncated “matched” subset.  Equivalently, equality of the two theta
keys implies equality of the theta double cosets by Hejhal, and projection
then gives equality of the finite double cosets.

This is why the `[1,2]` / `[2,1]` collision is harmless after repair: their
`c` values coincide, but their full theta keys and canonical theta words do
not.

### M1-S — surjectivity: PROVED with an explicit safe cutoff

Corollary 5.2 proves surjectivity onto

```text
{(c_H,d_H) in H_infty : c_H <= ceil(q/2)-1}.
```

The inverse is explicit: take the Hejhal double coset, take its canonical
`Q,R` word, reduce each exponent modulo `q`, and use the resulting finite
canonical word.  No wrap occurs in the stated height range, and balanced
lifting returns the starting theta word.

### M1-L — localization: old version FALSE; corrected version PROVED

Under the section pairing, every finite class has a theta partner, so the
finite unmatched set is empty.  The theta complement is exactly the
first-wrap set and lies at `c_H>=ceil(q/2)` by Corollary 5.3.

The proposed symmetric strengthening is **FALSE**.  For every finite `q`,
the theta word `w=R^q` is canonical and first-wrap.  The matrix identity in
Lemma 4.1 gives `c_H(w)=q`, but

```text
replay_q(w)=R_q^q=1,
c_q(replay_q(w))=0.
```

Thus

```text
min(c_q(replay_q(w)), 2c_H(w)) = 0,
```

which cannot be at least `kappa q` for any positive `kappa`.  If replay is
declared only for `c_q>0`, the old statement is undefined on this first-wrap
word rather than true.  The corrected summation split must use the one-sided
theta tail supplied above.

## 7. Controlled deformation for `lambda_q<2`

The combinatorial correspondence controls **which word** is paired.  The
formal matrix results then control evaluation of that fixed word:

1. `RateCore.c_eq_scaled_int_poly` gives an integer polynomial `p_w` with

   ```text
   c_w(lambda) lambda^{depth(w)} = p_w(lambda).
   ```

   Hence a fixed lifted word has an algebraic, unambiguous deformation from
   `lambda_q` to `2`.

2. `RateCoreII.wordMatrix_two_form` gives at theta

   ```text
   wordMatrix(2,w) = [[a,b/2],[2c,d]],       a,b,c,d in Z,
   ```

   which is exactly the normalization needed for the Hejhal key.

3. For the one-block/Chebyshev family, right multiplication by `S` does not
   change the lower-left entry, and the checked Chebyshev theorem yields

   ```text
   c_conj(R_lambda^m)
     = lambda U_{m-1}(lambda/2),
   c_conj(R_2^m)=2m.
   ```

These facts are sufficient for a canonical term-by-term pairing.  They are
**not** a uniform estimate for
`|c_q(X)-2c_H(L_q(X))|` after summing over all words.  The derivative envelope
and the summability of paired-word distortion remain **CONJECTURAL R2/N1
work**.  M1 must not be upgraded into that analytic claim.

## 8. Final corrected Route B statement

For every finite `q>=3`, let `C_q` be the nontrivial
`<S>\G_q/<S>` double cosets and let `H_infty` denote Hejhal's admissible
theta data.  Then the balanced free-product lift defines

```text
L_q : C_q -> H_infty
```

such that:

```text
(W) L_q is well-defined;
(I) L_q is injective;
(S) {(c_H,d_H): c_H<=ceil(q/2)-1} is contained in im(L_q);
(L) H_infty\im(L_q) is exactly the first-wrap set and has
    c_H>=ceil(q/2).
```

The proof is purely free-product/double-coset combinatorics plus the printed
theta key theorem and the checked matrix normalization.  No Rosen/geodesic
claim is used.  The finite key-completeness lemma and the uniform analytic
deformation bound are explicitly left **CONJECTURAL**; neither is needed for
the four corrected structural statements above.

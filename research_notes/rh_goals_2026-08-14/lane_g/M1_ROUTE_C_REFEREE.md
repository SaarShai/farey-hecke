# Adversarial referee report: M1 Route-C rigidity

**Date:** 2026-08-18

**Target:** `research_notes/rh_goals_2026-08-14/lane_g/M1_ROUTE_C_RIGIDITY_SOL.md`

**Verdict:** **CONFIRMED**, with formalization and scope qualifications stated below.

I tried to refute the bounded-complexity claim. I found no counterexample and no
invalid inequality in its proof. Claim (a), the failure of the unsectioned map,
is correct. Claim (b) is a valid **conditional, paper-level** theorem for a
supplied section satisfying the stated bounds. It is not a global M1 theorem,
does not construct such a section, and is not itself machine-verified.

The two qualifications that should remain visible are:

1. The cited Lean files certify the polynomial, one-factor derivative,
   mean-value, cosine, theta-shape, and combinatorial totient statements. They
   do **not** certify the product derivative envelope, Ford separation, a
   section, the bounds `(K,H,D)`, or Theorem 6.1 itself.
2. `theta_coset_count` machine-checks a finite arithmetic cardinality. The
   identification of that filtered residue set with all Hejhal theta double
   cosets is external mathematical input, not a conclusion formalized in
   `RateCoreII.lean`.

Neither qualification refutes the theorem as the note actually labels it:
Theorem 6.1 is explicitly “PROVED at paper level”
(`M1_ROUTE_C_RIGIDITY_SOL.md:295-303`), and the missing global section is
explicitly retained as a gap (`M1_ROUTE_C_RIGIDITY_SOL.md:331-358,440-457`).

**Write-set receipt.** The repository was dirty before this audit. The only
repository path created or changed by this audit is this requested referee
file. The fresh Python script and Lean query files were temporary `/tmp`
artifacts required for execution; they were deleted after their commands,
hash, and outputs were captured below. No `tasks/`, wiki, source, Lean, build,
or graph-index file was created or edited.

## 1. Claim (a): direct recomputation

The note defines `R_lambda = Q_lambda S` and asserts
`R_{lambda_q}^q = -I`, so `Q_{lambda_q}` and
`R_{lambda_q}^q Q_{lambda_q}` are the same PSL element, whereas their theta
specializations have distinct keys (`M1_ROUTE_C_RIGIDITY_SOL.md:88-125`).

I recomputed both matrix products rather than using the displayed closed form.
The fresh script used `Fraction` arithmetic at `lambda=2` and 110-decimal
`mpmath` arithmetic at `lambda_q`. Command:

```text
/Users/za/.venvs/farey-rh/bin/python /tmp/m1_route_c_referee_check.py
```

Relevant output:

```text
RAW_COUNTEREXAMPLE q=13 maxabs((Q_lambda S)^q Q_lambda + Q_lambda)=1.8129595e-109
  theta_short=[[Fraction(0, 1), Fraction(-1, 2)], [Fraction(2, 1), Fraction(0, 1)]]
  theta_long=[[Fraction(-13, 1), Fraction(6, 1)], [Fraction(28, 1), Fraction(-13, 1)]]
  theta_keys=(1, 0),(14, 15) distinct=True
```

The exact theta result is

\[
(Q_2S)^{13}Q_2=
\begin{pmatrix}-13&6\\28&-13\end{pmatrix},
\]

so its source-coordinate key is `(14,15)`, while `Q_2` has key `(1,0)`.
The finite residual is at the 110-digit working precision. Independently of
that numerical residual, Cayley--Hamilton gives the exact identity: `R` has
determinant one and eigenvalues `exp(±i*pi/q)`, hence `R^q=-I`. Both lower-left
entries are nonzero. Claim (a) is therefore confirmed.

## 2. Machine-input audit

### P1: integer-polynomial matrix entries

The authoritative result file defines the word matrix and depth at
`projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle/RateCore.lean:40-64`.
The full matrix theorem `wordMatrix_intPoly` says exactly that, for arbitrary
`w : List Int`, there is an integer-polynomial matrix whose entries have degree
at most `2 * depth w`, and that
`lam ^ depth w * wordMatrix lam w` is its evaluation for `lam != 0`
(`RateCore.lean:83-127`). `c_eq_scaled_int_poly` is the lower-left corollary
(`RateCore.lean:129-136`). This matches the note's P1 statement
(`M1_ROUTE_C_RIGIDITY_SOL.md:41-48`).

The proof of Theorem 3.1 needs the full matrix theorem, not merely the `c`
corollary. The cited range contains the needed full theorem.

### P2, P3, and P5

- `hasDerivAt_Qmat` is the entrywise identity
  `Q'(lam) = lam^(-1) E Q(lam)` under `lam != 0`
  (`RateCore.lean:138-160`).
- `mvt_bound` is a generic scalar mean-value estimate, assuming a derivative
  and a uniform derivative bound throughout `Icc a b`
  (`RateCore.lean:162-177`).
- `two_sub_lam_le` proves
  `2(1-cos(pi/q)) <= pi^2/q^2` for natural `q` with `1 <= q`
  (`RateCore.lean:256-267`).

All hypotheses are available on `[lambda_q,2]` for `q>=3`. The note uses these
statements correctly at `M1_ROUTE_C_RIGIDITY_SOL.md:187-215`. P2 and P3 do not,
by themselves, state the differentiated word-product bound; that bound is the
paper calculation in lines 187-224.

I independently ran the result source through Lean:

```text
cd projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle
lake env lean RateCore.lean
```

Output was empty; exit status was zero. A separate `#print axioms` check for
the five cited declarations returned only:

```text
[propext, Classical.choice, Quot.sound]
```

The file does contain the unrelated, explicit axiom
`wordLimitMap_injective_on_matched` at `RateCore.lean:364-373`. It is not in the
axiom dependency lists of P1/P2/P3/P5 and is not used by this proof. The result
summary itself records this distinction at
`projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle/ARISTOTLE_SUMMARY.md:1-8`.

### `wordMatrix_two_form` and theta counting

The v27 result uses the same matrix conventions
(`projects/aristotle_dispatch_v27/result/aristotle_dispatch_v27_aristotle/RateCoreII.lean:45-63`).
`wordMatrix_two_form` proves, for every integer exponent list,

\[
W_w(2)=\begin{pmatrix}a&b/2\\2c&d\end{pmatrix}
\quad(a,b,c,d\in\mathbb Z)
\]

at `RateCoreII.lean:126-142`; `c_two_even` is its lower-left consequence at
lines 154-157. `theta_coset_count` proves

```text
#{d < 2c : gcd(c,d)=1 and c+d is odd} = phi(2c)
```

at `RateCoreII.lean:159-214`. These are the statements the note quotes at
`M1_ROUTE_C_RIGIDITY_SOL.md:56-66`.

I checked the exact result source with the v26 Mathlib environment; it
elaborated with only the documented unused-`hc` warning. Compiling it to a
temporary `.olean` and running `#print axioms` on `wordMatrix_two_form`,
`c_two_even`, and `theta_coset_count` again returned only the three standard
axioms above.

Limit: `theta_coset_count` is a theorem about the displayed finite filter. It
does not prove within Lean that this filter is the theta double-coset set, that
every key is realized by a word, or that an enumerated list is complete. The
Hejhal identification is described in comments at `RateCoreII.lean:159-164`
and in the surrounding paper notes, not formalized. The Route-C certificate
correctly makes realization and completeness independent inputs
(`M1_ROUTE_C_RIGIDITY_SOL.md:331-353`).

## 3. Line-by-line inequality audit for claim (b)

### 3.1 Algebraic-degree rigidity

Suppose words `w,v` have depths `k_w,k_v <= K` and are related at `lambda_q`
by fixed parabolic exponents and a PSL sign. From P1,

\[
\lambda^K W_w(\lambda)
=\lambda^{K-k_w}P_w(\lambda),
\]

and likewise after multiplying `P_v` by the constant integer matrices
`S^u,S^r`. Each entry is an integer polynomial of degree at most

\[
(K-k_w)+2k_w=K+k_w\le2K.
\]

This verifies `M1_ROUTE_C_RIGIDITY_SOL.md:143-153`. If it vanishes at
`lambda_q` and the algebraic degree
`d_q=[Q(lambda_q):Q]=phi(2q)/2` exceeds `2K`, it is identically zero. Evaluation
at `2` is then legitimate because `2 != 0`. Lines 154-162 are correct.

The explicit degree threshold is also correct. The note uses

\[
\frac{\varphi(n)^2}{n}
=\prod_{p^a\Vert n}p^{a-2}(p-1)^2\ge\frac12.
\]

The only local factor below one is indeed `1/2` for `p=2,a=1`; all other
factors are at least one. Taking `n=2q` gives `phi(2q)>=sqrt(q)`. Hence every
bad `q` with `phi(2q)<=4K` satisfies `q<=16K^2`, proving both finiteness of the
maximum and `q_deg(K)<=16K^2+1`
(`M1_ROUTE_C_RIGIDITY_SOL.md:166-180`). Since `q_deg` is one more than the
largest bad level, every `q>=q_deg(K)` satisfies `d_q>2K` even though totients
are not monotone.

Implicit domain assumptions should be made explicit in a publication version:
`q>=3` and `K>=1`. They hold in the surrounding setup and for every nonempty
word section; they are not a counterexample.

### 3.2 Derivative envelope

For `q>=3`, `lambda` lies in `[1,2]`, and direct calculation gives

\[
\lVert Q_\lambda\rVert_\infty\le2,
\qquad
\lVert Q'_\lambda\rVert_\infty\le1,
\qquad
\lVert S^n\rVert_\infty=1+|n|.
\]

Differentiating a word with `k` copies of `Q` produces exactly `k` summands.
Submultiplicativity of the maximum-row-sum norm bounds each by

\[
2^{k-1}(1+|r_w|)\prod_j(1+|n_j|),
\]

so the displayed `D_w` at `M1_ROUTE_C_RIGIDITY_SOL.md:193-211` is valid and
entrywise. P3 and P5 then give

\[
|\Delta c_w|,|\Delta d_w|
\le(2-\lambda_q)D_w
\le\pi^2D_w/q^2,
\]

as claimed in lines 212-215. Replacing `k,B,R` by upper bounds gives line
224's `D=K 2^(K-1)(B+1)^(K-1)(R+1)`. No Chebyshev derivative estimate is used.

### 3.3 Ford separation

For `g^{-1}H_infinity`, the tangency point is `-d_g/c_g` and the radius is
`1/(2c_g^2)`. Distinct double cosets give distinct disk orbits on the
width-one cylinder. For two disjoint disks with radii `R,R'` and horizontal
separation `x`,

\[
x^2+(R-R')^2\ge(R+R')^2
\quad\Longrightarrow\quad
x^2\ge4RR'=\frac1{c_g^2c_h^2}.
\]

Thus the circular separation is at least `1/|c_gc_h|`. The derivation at
`M1_ROUTE_C_RIGIDITY_SOL.md:235-251` is correct. The underlying Ford/Shimizu
scope and width-one normalization agree with
`M2_FORD_PACKING_REFEREE.md:70-118`. This is paper-level geometry; the target
note explicitly says its Lean formalization remains open at lines 67-75.

The cumulative Ford count is not used as a substitute for separation and is
not used to manufacture a section (`M1_ROUTE_C_RIGIDITY_SOL.md:253-256`).

### 3.4 Ratio perturbation

Write the normalized theta bottom row as `(C,d)`, with `|d|<=C/2`, and let
`|Delta c|,|Delta d|<=e`. If `e<C`, then

\[
\left|\frac{d+\Delta d}{C+\Delta c}-\frac dC\right|
\le \frac{e}{C-e}+\frac{|d|e}{C(C-e)}
\le\frac{3e}{2(C-e)}.
\]

If `e<=C/2`, this is at most `3e/C`. Therefore two words with the same
normalized theta key have finite tangency points at circular distance at most
`6e/C`. This verifies `M1_ROUTE_C_RIGIDITY_SOL.md:260-283`.

The opposite Ford bound uses `|c_q|<=C+e` for both words and is therefore
`1/(C+e)^2`. The sign is safe because the threshold below implies `e<C`, so
`c_q` retains the positive theta sign.

### 3.5 The `27/2` constant and the threshold

Theta arithmetic gives `C` a positive even integer, hence `C>=2`; the section
assumption gives `C<=H`. If

\[
e<\frac{2}{27H},
\]

then

\[
e<\frac{2}{27H}\le\frac{2}{27C}\le\frac C2,
\]

and

\[
\frac{6e}{C}
<\frac{12}{27HC}
\le\frac{12}{27C^2}
=\frac4{9C^2}.
\]

Because `e<C/2`, `C+e<3C/2`, so

\[
\frac4{9C^2}<\frac1{(C+e)^2}.
\]

This contradicts the simultaneous upper and lower separation bounds. The note
writes a weak `<=` in the final comparison at line 291; the hypotheses actually
give the strict inequality needed for the contradiction.

Now put `e=pi^2 D/q^2` and

\[
A=\pi\sqrt{27HD/2}.
\]

If `q>=floor(A)+1`, then `q>A`, including when `A` is an integer, and hence

\[
e=\frac{\pi^2D}{q^2}<\frac{2}{27H}.
\]

This proves the exact threshold at `M1_ROUTE_C_RIGIDITY_SOL.md:285-303`.
The factor `27/2` comes solely from this conservative Ford-gap comparison:
the factor `6` is two ratio errors of size `3e/C`, and `2/27` is chosen to fit
them below the convenient `4/(9C^2)` gap. It does **not** come from a cubic
discriminant, a Chebyshev derivative, or any hidden machine estimate.

Combining this injectivity with the algebraic-degree threshold proves the
stated sectioned W/I implication at lines 305-313. I found no circularity:
Theorem 6.1 first establishes equality of finite classes from equal theta keys;
Theorem 3.1 then promotes the resulting fixed parabolic equality to a
polynomial identity.

The reverse replay estimate at lines 315-329 also checks out. Unequal positive
even heights differ by at least two. At equal height, distinct normalized
residues are separated by at least `1/C`, while the two ratio perturbations
total at most `6e/C`; `e<1/6` preserves distinctness. For `H>=2`, the main
threshold is stronger because `27H/2>=6`.

## 4. Fresh bounded-coset enumeration

The script enumerated every word of depth at most `K` whose exponents lie in
`[-B,B]`, including zero exponents. It used exact rational arithmetic to:

- evaluate at `lambda=2`;
- choose the PSL sign with `C>0`;
- choose the terminal `r_w` putting `d` in `[-C/2,C/2)`;
- compute the theta key and the note's exact `D_w` bound.

It then filtered by `C<=H,D_w<=D`, evaluated at the exact claimed threshold
to 110 decimal digits, and formed numerical finite double-coset classes using
equality of `c` and integrality of `(d_1-d_2)/c`, with tolerance `1e-80`.
For exact matrices this bottom-row condition is complete under the standard
primitive width-one cusp stabilizer used by the note: after a right `S`-power
aligns the two bottom rows, their quotient is an element of the group fixing
infinity, hence an integer `S`-power. The implemented test is nevertheless
numerical, so the enumeration remains a diagnostic, not a proof. Including
zero exponents deliberately tests nonreduced duplicate representatives and
the well-definedness direction.

Script SHA-256:

```text
2708ccabd2bcb72de6b58d50eb19fd517ee2f7b3c111d4a157cf38fa23d8a0c9
```

Command and full bounded-case output:

```text
/Users/za/.venvs/farey-rh/bin/python /tmp/m1_route_c_referee_check.py

CASE K=1 B=1 H=2 D=1 zero_digits=yes q_deg=7 q_sep=17 q1=17
  enumerated_words=1 accepted_words=1 finite_double_cosets=1 theta_keys=1
  within_class_theta_key_failures=0 cross_class_theta_key_collisions=0
  e=0.0341508802806 2/(27H)=0.037037037037 e/target=0.922073767576 min_c(q)=1.96594619937
  largest_equivalent_pair_relative_c_residual=0.0 largest_equivalent_pair_residue_residual=0.0
CASE K=2 B=2 H=8 D=12 zero_digits=yes q_deg=16 q_sep=114 q1=114
  enumerated_words=6 accepted_words=5 finite_double_cosets=5 theta_keys=5
  within_class_theta_key_failures=0 cross_class_theta_key_collisions=0
  e=0.00911320812658 2/(27H)=0.00925925925926 e/target=0.984226477671 min_c(q)=1.99924061405
  largest_equivalent_pair_relative_c_residual=0.0 largest_equivalent_pair_residue_residual=0.0
CASE K=3 B=2 H=14 D=108 zero_digits=yes q_deg=22 q_sep=449 q1=449
  enumerated_words=31 accepted_words=22 finite_double_cosets=13 theta_keys=13
  within_class_theta_key_failures=0 cross_class_theta_key_collisions=0
  e=0.00528726184551 2/(27H)=0.00529100529101 e/target=0.999292488802 min_c(q)=1.99995104407
  largest_equivalent_pair_relative_c_residual=0.0 largest_equivalent_pair_residue_residual=0.0
CASE K=4 B=2 H=30 D=864 zero_digits=yes q_deg=31 q_sep=1859 q1=1859
  enumerated_words=156 accepted_words=98 finite_double_cosets=41 theta_keys=41
  within_class_theta_key_failures=0 cross_class_theta_key_collisions=0
  e=0.0024674860629 2/(27H)=0.00246913580247 e/target=0.999331855475 min_c(q)=1.99999714411
  largest_equivalent_pair_relative_c_residual=0.0 largest_equivalent_pair_residue_residual=3.3265e-111
```

No bounded case produced either failure mode. The `K=3` and `K=4` tests are
close to the proof's strict analytic boundary (`e/target > 0.9992`), so they
also check the floor-plus-one convention rather than a generously oversized
level. This finite computation supports but does not establish the theorem.

## 5. Consistency of `K`, `H`, and `D`

- `K` consistently means the number of `Q` letters, matching the Lean
  definition `depth(w)=w.length+1` (`RateCore.lean:53-64`; target lines 31-37,
  143-162).
- `H` consistently bounds the **conjugated** theta lower-left height
  `C=|c(2)|`, not the source height `c_H=C/2` (target lines 14-16,77-84,
  274-303). Section 7 correctly sets `H=2X` when `X` is a source-coordinate
  cutoff (lines 331-337).
- `D` consistently bounds all entries of the derivative of the
  theta-normalized path `W_w(lambda)S^{r_w}`. The explicit envelope includes
  the terminal factor `(1+|r_w|)` (target lines 193-224), and Theorem 6.1 uses
  the same normalized `D_w` (lines 295-303).

The displayed numerical receipt at target lines 364-417 uses the universal
ceiling `16K^2+1` for `q_deg` in R1, then computes the sharper definition in
R2. It labels that distinction correctly at lines 381-385. R1 also includes
the replay threshold, but for `H>=2` it is dominated by `q_sep`, as proved at
lines 315-329, so this does not change `q_1`.

For maximum precision, the theorem statements should explicitly quantify
`q>=3`, `K>=1`, `H>0`, and `D>=0`. A nonempty section already forces
`C>=2`, `H>=2`, and `D>=D_w>0`, so the omitted typing conditions do not create
a counterexample.

## 6. Honest scope relative to global M1

The scope ledger is accurate.

- **Unsectioned M1-W is false.** The finite relator supplies arbitrarily deep
  representatives of one finite class with different theta images (target
  lines 86-125).
- **Sectioned bounded-depth W is proved only after a depth cap.** It applies
  when every competing accepted witness has depth at most `K`; it supplies no
  canonical representative (target lines 157-164).
- **Sectioned I is conditional on independently certified `H,D` bounds.** The
  theorem does not construct a section or prove those bounds for the global
  matched domain (target lines 295-313,349-358).
- **S is only onto an explicitly supplied replay image.** Surjectivity onto a
  larger Hejhal window is not asserted (target lines 315-329,440-447).
- **L remains open.** Nothing here identifies first-wrap events or proves a
  `kappa q` height lower bound (target lines 440-457). The original strategy
  states those global obligations separately at
  `M1_COSET_STRATEGY_SOL.md:269-359,399-429`.
- **Ford counting does not fill the gap.** It bounds the number of classes
  under a height cutoff but neither proves an enumerated list exhaustive nor
  controls word depth or derivative condition number (target lines 17-19,
  253-256,349-358).

## Final assessment

The requested refutation of (b) fails. The threshold

\[
q_1(K,H,D)=\max\left\{q_{\deg}(K),
\left\lfloor\pi\sqrt{27HD/2}\right\rfloor+1\right\}
\]

is correctly derived for the stated bounded section, and all load-bearing
inequalities close. The fresh enumeration found no small bounded counterexample.
The theorem should be cited only as a **conditional paper-level finite-window
rigidity theorem**. It must not be cited as a machine-verified theorem, as a
construction of the needed section, or as completion of global M1-W/I/S/L.

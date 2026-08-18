# Adversarial referee report: M1 Route B free-product section

**Date:** 2026-08-18
**Target:** `M1_ROUTE_B_FREEPRODUCT_SOL.md`
**Verdict:** **GAPS**

## 0. Bottom line

I did not find a counterexample to the abstract double-coset normal-form
theorem or to the balanced section.  Independent exact searches at `q=5,7`
found no two Route-B canonical words in the same double coset through reduced
free-product syllable depth 8, and an exhaustive theta-key scan found no
collision among all balanced canonical words through eight `Q`-syllables
(196,608 words at `q=5`, 8,398,080 at `q=7`).

That does **not** confirm the target as a proof of the program's original M1.
There are three paper-level gaps.

1. The target asserts, but neither proves nor cites, the full presentation
   `G_q = C_2 * C_q`; the order of `R=QS` is not by itself a proof that there
   are no further relations (`M1_ROUTE_B_FREEPRODUCT_SOL.md:246-268`).  The
   presentation is standard and a suitable source is already identified in
   `M2_FORD_PACKING_REFEREE.md:43-62`, so this is repairable.
2. The original M1 domain consists of finite matrix classes with `c_q>0`
   (`M1_COSET_STRATEGY_SOL.md:269-279`).  Route B explicitly leaves
   `Stab_{G_q}(infinity)=<S>` conjectural
   (`M1_ROUTE_B_FREEPRODUCT_SOL.md:545-558`).  Without importing that lemma,
   the abstract nontrivial-double-coset section does not prove that every
   inverse replay used for M1-S belongs to the `c_q>0` scattering domain, nor
   does it complete the bridge to LAW_R1's finite matrix key.
3. The proved one-sided support `c_H >= ceil(q/2)` is not the quantitative
   localization required for the RATE exponent.  Ford summation at a cutoff
   proportional to `q` gives only `O(q^(2-2 sigma))`, whereas RATE requires
   `O(q^(1-2 sigma))`; the current certified replacement takes `X(q)=q^6`
   (`N1N3_PROMOTION_EXECUTION_SOL.md:354-468`).  Route B itself also leaves
   paired derivative/summability control conjectural
   (`M1_ROUTE_B_FREEPRODUCT_SOL.md:641-645`).

Thus the core abstract construction is strongly supported, but the claims
"M1-W/M1-S/M1-L proved" need qualification.  M1-I is the clean theorem.

## 1. Attack (a): is the free factor really `C_q`?

### Finding

The factor choice is correct in PSL:

```text
R = Q S,
Q^2 = 1,
R^q = 1,
G_q = <Q,R | Q^2=1, R^q=1> = C_2 * C_q.
```

In the displayed SL matrices, the exact identity is `R_q^q=-I`; hence `R`
has order `q` after passage to PSL.  Route C proves that identity at
`M1_ROUTE_C_RIGIDITY_SOL.md:86-97`, and the fresh exact calculation below
reproduced it for `q=5,7`.  There is no generator mistake: the `R`-factor, not
the parabolic `S=QR`, is the finite cyclic factor.

However, `R^q=1` proves only that the presented group maps onto the matrix
group.  The assertion that these are the **only** relations is the
`(2,q,infinity)` triangle-group presentation.  The target simply writes the
isomorphism at `M1_ROUTE_B_FREEPRODUCT_SOL.md:254-265`.  A paper proof must cite
or import the presentation.  The repo already points to Moller-Pohl's
`<T,S | S^2=1=(TS)^q>` presentation and Pohl's fundamental domain in
`M2_FORD_PACKING_REFEREE.md:43-62`.

**Assessment:** mathematically correct; missing imported theorem/citation, not
refuted.

## 2. Attack (b): exceptional class

The convention is well-defined.  In PSL,

```text
Q S = R,
S^-1 Q = R^-1,
```

so `Q`, `R`, and `R^-1` are in one `<S>`-double coset, exactly as stated at
`M1_ROUTE_B_FREEPRODUCT_SOL.md:275-323`.  Choosing `Q` assigns that class the
theta key `(c_H,d mod 2c_H)=(1,0)`, which is admissible in Hejhal's list.

The convention also fixes, rather than creates, a downstream pathology.  The
long word used to refute the universal derivative envelope satisfies

```text
S (R^(q-2) Q) S = Q
```

by `N1N3_PROMOTION_EXECUTION_SOL.md:91-99`; Route B therefore selects the short
representative `Q`.

The proof of uniqueness at `M1_ROUTE_B_FREEPRODUCT_SOL.md:325-340` is terse:
"a direct boundary reduction" is doing the work for arbitrary
`S^m w S^n`.  The endpoint exclusions `a_0 != -1`, `a_k != 1` do block
cancellation from the two boundaries, and the brute-force receipt found no
failure.  For publication, this should be expanded into an explicit
cancellation lemma, including the case where cancellation would otherwise
traverse the entire middle word.

**Assessment:** convention sound; no downstream break found; proof exposition
should be strengthened.

## 3. Attack (c): fresh `q=5,7` brute force

### 3.1 What was enumerated

A fresh stdin script was run with
`/Users/za/.venvs/farey-rh/bin/python`; no existing enumerator or stored result
was reused.

It performed two independent checks.

1. **Finite exact check.**  Enumerate every reduced element normal form in
   `C_2*C_q` of free-product syllable length at most 8.  For each word, scan
   `S^m w S^n` for `-12 <= m,n <= 12`, collect Route-B terminal words, and
   verify the chosen transform by exact matrices up to sign.  Arithmetic used
   the exact fields

   ```text
   q=5: x^2-x-1=0,       x^-1=x-1,
   q=7: x^3-x^2-2x+1=0, x^-1=2+x-x^2.
   ```

   All canonical candidates in that ball were also deduplicated by the exact
   algebraic bottom-row invariant `(c,d mod Z*c)`.  Therefore two canonical
   candidates in the tested ball cannot hide in the same double coset outside
   the multiplier scan: double-coset equality would force the same bottom-row
   invariant.
2. **Balanced-section check.**  Exhaustively enumerate every Route-B finite
   canonical exponent word with at most eight `Q` separators, replace residues
   by the balanced alphabet, evaluate the exact integer theta bottom row, and
   sort the Hejhal keys `(c_H,d mod 2c_H)`.  This is the larger search:
   196,608 words at `q=5` and 8,398,080 at `q=7`.

The finite search is exhaustive only in the stated word ball; it is not a
proof of the global theorem.  The balanced-key search is exhaustive through
the stated `Q`-depth.

### 3.2 Command

Because the task permits only this report as a persistent file, the fresh
script was supplied on stdin rather than retained as a second artifact.

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python -
```

The process command above read the fresh script from standard input.  Its
fixed parameters were `D=8`, `HB=12`, and `QD=8`; the implemented checks are
specified in Section 3.1.  The source was intentionally not persisted as a
second file.

### 3.3 Output

```text
CONFIG exact_free_product_syllable_depth=8 H_multiplier_bound=12 exhaustive_balanced_Q_depth=8
FINITE q=5 reduced_normal_forms_syllable_depth_le_8=1106 distinct_note_candidates=193 missing=0 ambiguous_distinct_candidates=0 max_min_abs_m_plus_n=5
FINITE q=5 exact_matrix_H_transform_checks=1106 failures=0 candidate_bottom_key_collisions=0 R_power_q_equals_minus_I=True first_ambiguity=None
CONTROL q=5 [1,2]_finite_NF='R^2 Q R^2' balanced_lift='R^2 Q R^2' theta_source_key=(7, 12)
CONTROL q=5 [2,1]_finite_NF='R^1 Q R^3' balanced_lift='R^1 Q R^-2' theta_source_key=(8, 5) finite_same_c=True integer_right_S_shift_between_d=None
THETA q=5 balanced_finite_canonical_words_Q_depth_le_8=196608 distinct_theta_keys=196608 duplicate_adjacent_pairs=0 max_c_H=289154
FINITE q=7 reduced_normal_forms_syllable_depth_le_8=4922 distinct_note_candidates=1081 missing=0 ambiguous_distinct_candidates=0 max_min_abs_m_plus_n=5
FINITE q=7 exact_matrix_H_transform_checks=4922 failures=0 candidate_bottom_key_collisions=0 R_power_q_equals_minus_I=True first_ambiguity=None
CONTROL q=7 [1,2]_finite_NF='R^2 Q R^2' balanced_lift='R^2 Q R^2' theta_source_key=(7, 12)
CONTROL q=7 [2,1]_finite_NF='R^1 Q R^3' balanced_lift='R^1 Q R^3' theta_source_key=(7, 10) finite_same_c=True integer_right_S_shift_between_d=None
THETA q=7 balanced_finite_canonical_words_Q_depth_le_8=8398080 distinct_theta_keys=8398080 duplicate_adjacent_pairs=0 max_c_H=8050683
WINDOW q=32 route_B_cutoff_c_H=15 keys_through_cutoff=95 complete_c_H_le_25=263 omitted_in_C_le_50_window=168 R13_in_balanced_alphabet=True
WINDOW q=48 route_B_cutoff_c_H=23 keys_through_cutoff=227 complete_c_H_le_25=263 omitted_in_C_le_50_window=36 R13_in_balanced_alphabet=True
```

Here the last two `omitted` numbers mean "not guaranteed by the displayed
height cutoff," not the exact complement of Route B's larger balanced-word
image.

### 3.4 Numerical verdict

No finite canonical collision was found.  In particular:

- `q=5`: 1,106 reduced normal forms, zero missing canonical images, zero
  ambiguous distinct canonical images, zero exact matrix failures, zero
  candidate bottom-key collisions;
- `q=7`: 4,922 reduced normal forms with the same four zeros;
- all transformations actually needed in the tested ball had
  `|m|+|n| <= 5`, inside the scan bound 12;
- all 8,594,688 balanced canonical words across the two `q` values had
  distinct theta keys through `Q`-depth 8.

This is strong falsification evidence for Theorems 3.1 and 5.1, but finite
enumeration is not their proof.

## 4. Attack (d): key and normalization

### 4.1 The certified `[1,2]` / `[2,1]` collision

The old `c`-only map fails because both words have

```text
c_lambda = lambda (2 lambda^2 - 1),
```

while their `d` entries are different
(`M1_ROUTE_B_FREEPRODUCT_SOL.md:90-108`; the certified formulas are summarized
at `M1_COSET_STRATEGY_SOL.md:431-450`).

The full key separates them at both tested finite groups: the exact script
found the same finite `c` but no integer right-`S` shift relating the two `d`
entries.

There is an important `q=5` nuance absent from the target's displayed raw
theta pair.

- At `q=7`, the balanced alphabet contains `3`, so the section keys are exactly
  `(7,12)` and `(7,10)` in source coordinates.
- At `q=5`, the finite canonical word for `[2,1]` is `R Q R^3`, but balanced
  lifting replaces `3 mod 5` by `-2`.  Its section image is therefore
  `R Q R^-2`, with source key `(8,5)`, not the raw-specialization key `(7,10)`.
  `[1,2]` still maps to `(7,12)`.

Separation survives; the pair of separating keys is simply different at
`q=5`.  The target's lines 90-108 are correct as a statement about the two raw
theta specializations, but they should not be read as the finite-`q=5`
balanced-section images.

### 4.2 LAW_R1 coordinates versus Hejhal coordinates

There is no modulus inconsistency once coordinates are kept straight.

- LAW_R1 works in width-one conjugated coordinates and uses
  `(C,d mod C)`, where `C` is the actual conjugated lower-left entry
  (`LAW_R1_COSET_STRUCTURE.md:76-100`).
- At theta, `C=2c_H`, so Hejhal's source-coordinate key is
  `(c_H,d mod 2c_H)` and the conjugated key is
  `(2c_H,d mod 2c_H)`
  (`M1_ROUTE_B_FREEPRODUCT_SOL.md:137-149,346-356`).

Thus the `q=7` source pairs `(7,12),(7,10)` are the LAW_R1 pairs
`(14,12),(14,10)`.  The `q=5` balanced pairs become
`(14,12),(16,5)` in conjugated coordinates.

The scan of Hejhal Vol. 2, Ch. 11 Section 3, printed p. 525, was visually
checked.  Lemma 3.1 states

```text
c>0, 0<=d<2c, c+d == 1 (mod 2), gcd(c,d)=1,
```

and says the resulting union is disjoint.  `RateCoreII.lean:159-214` proves
that the number of admissible residues at fixed `c_H` is `phi(2c_H)`.  The
controls are consistent:

```text
(7,12): gcd=1, 7+12 odd, 0<=12<14
(7,10): gcd=1, 7+10 odd, 0<=10<14
(8,5):  gcd=1, 8+5  odd, 0<=5<16
```

### 4.3 What the key does not prove

The balanced exponent word is an abstract section; it is not itself the finite
matrix key.  To identify abstract nontrivial double cosets with the
`c_q>0` matrix/scattering classes, and to turn equality of finite real keys
into double-coset equality, one needs the exact cusp stabilizer

```text
Stab_{G_q}(infinity)=<S>.
```

Route B correctly isolates this at `M1_ROUTE_B_FREEPRODUCT_SOL.md:545-558`,
but incorrectly says it is irrelevant to all four original obligations.  It
is irrelevant to the abstract section identity and injectivity; it is relevant
to the bridge back to the original M1-S domain and the LAW_R1 enumeration.
Pohl's cusp-stabilizer statement is already recorded at
`M2_FORD_PACKING_REFEREE.md:49-55`, so this is again repairable by a precise
import.

## 5. Attack (e): W/I/S/L ledger

The answer depends on whether one grades the new abstract theorem or the
program's statement-of-record obligations at
`M1_COSET_STRATEGY_SOL.md:269-359`.

| Obligation | What Route B really proves | Referee status |
|---|---|---|
| **W** | Assuming the standard `C_2*C_q` presentation, Theorem 3.1 gives a raw-word-independent abstract normal form, and balanced lifting gives a well-defined theta double coset (`M1_ROUTE_B_FREEPRODUCT_SOL.md:275-340,470-495,534-543`). | **PROVED abstractly; GAP for the uncited presentation and original finite-matrix/scattering bridge.** |
| **I** | `bar(pi_q) o L_q = id`; hence equality of theta images implies equality of finite abstract double cosets (`M1_ROUTE_B_FREEPRODUCT_SOL.md:470-490,560-569`). | **PROVED**, conditional only on the presentation/normal-form theorem. This is the clean result. |
| **S** | Every theta canonical word with `c_H <= ceil(q/2)-1` has all digits in the balanced alphabet and projects back to a finite abstract class (`M1_ROUTE_B_FREEPRODUCT_SOL.md:501-513,571-582`). | **PROVED abstractly; GAP for showing the replay lies in the original `c_q>0` domain without the cusp-stabilizer import.** |
| **L** | The complement of the abstract image is exactly the first balanced-digit wrap set and has `c_H >= ceil(q/2)` (`M1_ROUTE_B_FREEPRODUCT_SOL.md:515-530,584-608`). The old symmetric `min(c_q,2c_H)>=kappa q` claim is correctly refuted by `R^q`. | **PROVED only as one-sided structural support; GAP for the original RATE-strength localization/replacement inequality.** |

The target is right that the universal paired derivative estimate is separate
R2/N1 work.  But the statement-of-record M1-L explicitly asks for the
two-sided inequality **or a replacement strong enough to sum the complement**
(`M1_COSET_STRATEGY_SOL.md:338-357`).  A lower support cutoff at `q/2` alone
does not provide that exponent.  The certified Ford bound is

```text
sum_{|c|>X} |c|^(-2 sigma)
    <= sigma/(sigma-1) X^(2-2 sigma),
```

at `N1N3_PROMOTION_EXECUTION_SOL.md:354-394`.  Setting `X` proportional to `q`
loses one power of `q`; the current RATE repair sets `X=q^6` on the working
sigma band (`N1N3_PROMOTION_EXECUTION_SOL.md:433-468`).

## 6. Route C and the 237/263 completeness failure

Route C does not contradict Route B.  It proves only bounded-complexity
rigidity and explicitly leaves global S/L open
(`M1_ROUTE_C_RIGIDITY_SOL.md:440-457`).  Route B supplies the structural input
Route C excluded.

The 237/263 receipt also does not refute Route B:

```text
sum_{1<=c_H<=25} phi(2c_H) = 263,
depth-12 theta BFS keys       = 237,
missing keys                 = 26.
```

These exact numbers and the explicit missing key `(C,D mod C)=(26,14)` are at
`N1N3_PROMOTION_EXECUTION_SOL.md:224-260,262-329`.  That depth-13 raw theta
word is double-coset equivalent to the Route-B canonical singleton `R^13`.
Since `13` lies in both `A_32` and `A_48`, Route B predicts its finite preimage
and explains why a depth-12 `Q,S` BFS missed it.  The abstract proof is not
window-enumeration dependent.

Conversely, Route B does **not** rescue the old claim that all 263 keys in the
whole conjugated `C<=50` window were matched.  Its unconditional height
subrange gives

```text
q=32: c_H<=15, sum phi(2c_H)=95;
q=48: c_H<=23, sum phi(2c_H)=227.
```

The exact balanced-word image may contain additional higher classes, but the
displayed cutoff alone proves neither all 263 nor the old depth-12 census.
The existing 237-key comparison remains an incomplete replay observation, as
`N1N3_PROMOTION_EXECUTION_SOL.md:331-350` says.

## 7. Required revision before confirmation

1. Cite/import the `(2,q,infinity)` presentation at the point where
   `G_q=C_2*C_q` is used.
2. Promote the already-sourced cusp-stabilizer fact to an explicit lemma and
   use it to connect abstract nontrivial classes, `c_q>0`, and the finite
   `(c,d mod c)` key.
3. Expand the simultaneous left/right boundary-cancellation argument in
   Theorem 3.1 into a complete lemma.
4. Relabel the obligation ledger:
   - abstract W/I/S and structural one-sided L are the Route-B theorem;
   - original finite-matrix W/S require the cusp bridge;
   - RATE-strength L remains open unless a stronger complement count or the
     independent `q^6` truncation argument is incorporated.
5. Add the `q=5` balanced-lift control `(7,12)` versus `(8,5)` so the raw theta
   pair is not mistaken for the section image at every finite `q`.

With (1)-(3), the abstract free-product theorem would be close to
**CONFIRMED**.  Without (2) and (4), the program's critical M1 closure claim is
not theorem-grade.

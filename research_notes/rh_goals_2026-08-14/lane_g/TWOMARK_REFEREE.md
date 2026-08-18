# Adversarial referee report: two-mark finite-height renewal

**Date:** 2026-08-18
**Target:** `TWOMARK_RENEWAL_SOL.md`
**Verdict:** **CONFIRMED — paper-level, not machine-verified.**

I found no collision in the endpoint-normalized marked coding, no measure
distortion or harmful double counting in the core convolution, no scalar
inequality failure in Section 5, and no numerical violation of
`(DH_{2,4})`.  The explicit constant `C_4=2^100` is finite and more than
sufficient.  Two cautions do not change the verdict:

1. the encoder is specified by reconstruction tables and prose rather than as
   a formal data type/decoder; an explicit decoder would make the central
   injectivity claim easier to audit;
2. the exact `y<=100` census is exact only inside that theta window.  It is not
   the full finite-height count `B_q(Y)`, because the target correctly proves
   that `x<=Y` does not imply `y<=Y`.

The new theorem is therefore a paper theorem resting on Lemma 4.1, the
paper-level Route-B/Ford inputs, and elementary summation.  It is not a theorem
proved by Aristotle v29, and it does not make the other conditional `(RATE)`
inputs unconditional.

## 1. Reproducibility receipts

The current relevant hashes are

```text
7a553a9c3ed289b513ad8dd7e3a118b0c0d50f92080a1f89a6749fbce44a692b  TWOMARK_RENEWAL_SOL.md
096d389905ad21505e2c25c30aa37b5a2fa3d3f6d054bcb30229096fc5c8d885  DH2_RENEWAL_PROOF_SOL.md
9146ecebfdb976ceb3df49c0e7789bc5a82ef2116ceb1f02d6a89d32f6c602d8  DH_DEPTH_LAW_SOL.md
70cf0a9d12cdc6938c431bd1246b0ca18d929c151fb98399a8e94a75d7f6fd3c  FW_RENEWAL_COUNT_SOL.md
ebb38cf55ea4e4132df7e0f3f68901c196b8c623b1b4f4b24b5b11b2a2318345  M2_FORD_PACKING_REFEREE.md
fee8a039c0cc7140a9b9d63a669653cfb83b060e4f6526bb882ecf21817ce88c  RateCoreIV.lean
```

They agree with the target's receipt at
`TWOMARK_RENEWAL_SOL.md:104-134`.  The numerical replays used
`/Users/za/.venvs/farey-rh/bin/python`, Python 3.13.13, with mpmath 1.4.1.

Fresh local typechecking of the harvested v29 `RateCoreIV.lean`, using
`LEAN_PATH` pointed at the already present v26 Mathlib dependency cache and the
read-only command `/Users/za/.elan/bin/lean RateCoreIV.lean`, exited zero.  It
emitted only the four documented unused-variable warnings (`hk0`, `hm`, `ha0`,
`hak`).  An anchored source scan found no `sorry` or `admit`.  This confirms the
current harvested artifact, but only at the theorem signatures it actually
states.

## 2. Attack (a): Lemma 4.1, injectivity, defects, and the heavy diagonal

### 2.1 Endpoint-normalized cores are legitimate counting objects

The upstream normal-form theorem gives exactly one bireduced representative,
with leading exponent not `-1`, trailing exponent not `+1`, and both exclusions
for a singleton (`M1_ROUTE_B_FREEPRODUCT_SOL.md:275-340`).  Its balanced lift is
an injective section, and its image is exactly the theta canonical words whose
digits lie in the balanced alphabet (`M1_ROUTE_B_FREEPRODUCT_SOL.md:442-495`).

Consequently, deleting a fragment's maximal leading `L=(-1)` run and maximal
trailing `U=(+1)` run leaves either the empty core or a genuine balanced
canonical word.  The singleton `U` and `L` cases reduce to the exceptional
class and are deleted, exactly as the target says at
`TWOMARK_RENEWAL_SOL.md:364-395`.  Since

\[
 (L^r A U^s)_{11}=A_{11},
\]

the normalization preserves the relevant matrix entry.  The finite-q Ford
height of a nonempty core is exactly
`rho=lambda*(N(F_0))_{11}`.  The cumulative double-coset Ford bound is uniform
for every finite Hecke group after width-one conjugation
(`M2_FORD_PACKING_REFEREE.md:64-79,81-116`).  Thus

\[
 \#\{F_0:\rho(F_0)\le T\}\le 1+T^2
\]

is the correct finite-q count; it is not a theta-height substitution and not a
one-sided-coset count.

### 2.2 Reconstruction audit of every marked boundary pattern

The code can be inverted from the data listed in Lemma 4.1 as follows.

- The tag records one mark versus two, each marked kind/sign
  (`H_+`,`H_-`,`U`,`L`), the empty-core flags, each bridge-versus-absorption
  status, and the coupled adjacent case.
- A bridge status, together with its auxiliary integers and a heavy magnitude,
  reconstructs the displayed bridge in `TWOMARK_RENEWAL_SOL.md:476-495` or
  `:514-550`.
- An absorption tag identifies an initial or terminal maximal unit run of the
  stored enlarged core.  Removing that designated run recovers both its exact
  length and the old core.
- The removed unmarked endpoint runs `p,r,s,v` are then reattached, and the
  marked bridges are inserted.  This recovers the original exponent word and
  the marked atom or marked pair.

The potentially ambiguous step is absorption.  It is in fact reversible:
maximality of the marked atom prevents the absorbed run from merging with a
same-sign run already in the old core.  If the old middle core is empty, the
three coupled cases `U,H`, `H,L`, and `U,L` are tagged separately.  The reverse
adjacent junction `L,U` cannot use the empty middle core: the canonical global
endpoint exclusions force the relevant outer core to be nonempty whenever an
outer bridge is absent.  Its two outer absorption tags therefore recover the
two marks independently.  These are exactly the cases analyzed at
`TWOMARK_RENEWAL_SOL.md:525-560`.

I found no untagged branch and no pair of distinct marked objects forced to
share a code.  Two independent finite falsification searches agreed:

- all one- and two-mark branches for `q=3,...,8`, canonical exponent length at
  most five: 24,326 words and zero product-gain failures;
- explicit encoding keys including simultaneous middle-core absorption, at
  `q=4,5` and length at most seven: 26,216 and 267,646 encodings respectively,
  with zero collisions.
- all 1,037 exact `y<=100` theta words: 2,620 one-mark objects and 2,344
  distinct left-to-right two-mark objects, encoded only by the allowed tags,
  cores, auxiliary integers, and heavy magnitudes, again with zero collisions.

These computations are diagnostics, not the proof.  The proof is the inverse
construction above.  For publication, the target could improve
`TWOMARK_RENEWAL_SOL.md:552-570` by defining the tag as the displayed finite
tuple and stating this decoder explicitly; the current prose is nevertheless
sufficient at paper level.

### 2.3 Product gain

For a heavy bridge,

\[
 (U^pH_{\pm n}L^v)_{11}
 \ge (n/\pi)(1+p)(1+v),
\]

and for a light bridge `(U^tL^v)_{11}=1+tv lambda^2>=tv`.  Selecting state 1
at core/bridge boundaries in the nonnegative matrix product yields the product
of the selected entries.  With at most three nonempty cores and two heavy
bridges,

\[
 D\prod_i\rho_i\le \lambda^2\pi^2x(W)\le4\pi^2x(W)<40x(W).
\]

This verifies `TWOMARK_RENEWAL_SOL.md:572-590`.  The same exhaustive branch
test above found zero violations of the stronger displayed `4*pi^2` bound.  On
the exact `y<=100` corpus at `q=3,5,8,12`, the largest observed
`D*product(rho_i)/x` was `2.381672660700903...`, versus
`4*pi^2=39.47841760435743...`.

### 2.4 One-defect family and same-atom heavy diagonal

The upstream one-defect identity is genuine:

\[
 w_{2,k}=(2,1,\ldots,1),\qquad c_\theta=6k-4,
\]

and its Route-B boundary reduction is `(1,Q,k)=RQR^k`
(`DH_DEPTH_LAW_SOL.md:559-635`).  When it is balanced, its large exponent `k`
is one marked heavy atom.  The one-cut heavy code records `n=k`; its weight
`n^2` cancels the `n^{-2}` supplied by the squared product gain.  Thus it is
included in the same-heavy diagonal sum (5.4), not lost in a light-run or
theta-cutoff argument.  This validates the use claimed at
`TWOMARK_RENEWAL_SOL.md:620-639,948-956`.

## 3. Attack (b): product convolution of cores

Let a core height lie in `[2^i,2^(i+1))`.  The cumulative Ford bound gives at
most `8*4^i` cores in that shell.  For three cores and
`L=floor(log_2 Z)`, direct grouping by `s=i_0+i_1+i_2` gives

\[
 8^3\sum_{s=0}^{L}{s+2\choose2}4^s
 \le {2048\over3}Z^2(L+2)^2
 \le2^{12}Z^2(1+\log Z)^2.
\]

The one- and two-core cases are smaller; the empty tuple also obeys the same
bound.  This confirms `TWOMARK_RENEWAL_SOL.md:416-438`.

There is no measure distortion: every `rho_i` is the actual finite-q
width-one height of the normalized core, and Lemma 4.1 retains the finite
cutoff through `D product rho_i <=40x(W)`.  Counting all core tuples and all
auxiliary parameters includes unrealized tuples and can double count matrices,
but that is harmless overcount after the marked-object-to-code map has been
shown injective.  No cumulative Ford bound was differentiated.

## 4. Attack (c): Section 5 and `C_4`

Every scalar inequality in Section 5 survives independent recomputation.

| target step | audit |
|---|---|
| (5.2) | follows from `Z=40Y/D>=1`, Lemma 4.1, and the verified core convolution |
| (5.3) | each explicit run parameter contributes either `sum r^-2` or `sum(1+r)^-2`, both `<2`; at most four parameters give `<2^4` |
| (5.4) | the summand is decreasing; comparison with its displayed antiderivative gives the stated heavy-diagonal sum |
| (5.5) | distinct heavy-heavy marks leave `1/(nm)`, heavy-light leaves `1/n`, and light-light leaves `1`; two harmonic logs plus the core-convolution log squared give at most the fourth power |
| (5.6) | `(1+log 40)^4 = 483.36619118199474 < 484`; the ratio decreases for `Y>=1` |
| (5.7) | for `g(t)=t[(1+log(40/t))^2+2(1+log(40/t))+2]`, `g'(t)=(1+log(40/t))^2>=0`; `g(40)=200` |
| (5.8)-(5.9) | the exact loose endpoint ratio at `R=1` is `22.31413659293298 < 32`; `q=3` has an empty heavy sum, so the same bound is vacuous there |
| (5.10)-(5.11) | `(log q)^4/q` has maximum `4^4/e^4=4.6888035555<5`; the three-term fourth-power inequality then gives the declared `2^13(q+R^4)` envelope |

The constant ledger is deliberately redundant:

\[
 2^{12}\cdot2^{20}\cdot2^{11}\cdot2^4\cdot2^{13}\cdot2^5
 =2^{65}.
\]

The base `2` in `k^2<=2+8A^2` is separately bounded by Ford as
`2#\{x<=Y\}<=2Y^2`, exactly as stated at
`TWOMARK_RENEWAL_SOL.md:730-732`.  In the high regime the heavy-diagonal and
nonheavy bounds are added, not multiplied; even charging an extra bit for that
addition leaves at most `2^66`.  The declared pair-ordering/(2.7) reserve and,
more decisively, the final 35-bit pre-addition slack absorb this bookkeeping:

\[
 {2^{100}\over2^{65}}=2^{35}=34,359,738,368.
\]

Thus the literal subtotal `2^65` should not be read as an optimized exact
constant after every addition; even the extra-bit `2^66` reading leaves 34 bits
of slack, so `C_4=2^100` is unquestionably sufficient.
There is no hidden divergent length sum: every unabsorbed length appears in
`D` and is zeta-summed, while every absorbed light length is recovered from a
Ford-counted tagged core.

## 5. Attack (d): theta-cutoff counterexample

The target's `q=3` words `(1,-1)^4` and `(1,-1)^5` satisfy the canonical
endpoint restrictions: they start in `+1`, end in `-1`, and all digits are in
the balanced alphabet.  Rerunning the exact integer script at
`TWOMARK_RENEWAL_SOL.md:238-255` printed

```text
digits= 8 x=34 y=1970
digits= 10 x=89 y=11482
```

Therefore `x<=Y` does not imply `y<=Y`; replacing the finite cutoff by the
theta cutoff is false.  The distortion is in fact unbounded along this family.
Writing `A_lambda=U_lambda L_lambda`, its Perron eigenvalues are
`(3+sqrt(5))/2` at `lambda=1` and `3+2sqrt(2)` at `lambda=2`, so the ratio of
theta to finite heights grows exponentially.  The warning at
`TWOMARK_RENEWAL_SOL.md:228-266` is correct.

## 6. Attacks (e) and (f): layer cake, constants, and numerical stress

### 6.1 Layer-cake algebra

Shimizu gives `x_X>=1`; positivity justifies Tonelli, hence

\[
 \sum_Xk_X^2x_X^{-p}=p\int_1^\infty B_q(t)t^{-p-1}\,dt.
\]

The low regime integrates to at most `q^(3-p)/(3-p)`.  In the high regime,
`t=qu` gives `q^(3-p)J_2(p)` from `qR^2` and `q^(2-p)J_4(p)` from `R^4`.
This reproduces (0.4) and `TWOMARK_RENEWAL_SOL.md:763-787`.  Multiplication by
the stated relative-drift factor `2*pi^2*A*|s|` changes these to the powers
`q^(1-p)` and `q^(-p)` in (6.5); the leading exponent is therefore
`p-1=2sigma-1`.

### 6.2 Verbatim replay of the displayed Section 6 script

Running the heredoc at `TWOMARK_RENEWAL_SOL.md:852-875` with the declared
interpreter printed

```text
J2 305.0
J4 91605.0
F_absorbed_q_ge_12 7940.0
match_coefficient 641373.443484015054908695422243
wrap 14303.7073813704179739567769621
wrap_plus_cheb 14381.9035143704179739567769621
scattering_from_rounded_match 921616.5035055924
scattering_from_rounded_fixed 20665.9633357584
high_diag_ratio_R1 22.3141365929329787571952985959
R5_base 2560913073.84467585803874126417
```

This exactly matches `TWOMARK_RENEWAL_SOL.md:879-890`.  The rounded bounds
`641373.444`, `14381.904`, `921616.504`, `20665.964`, and
`2.560914*10^9` are all upward.  The `(FW)` coefficient is also consistent
with its primary derivation:
`FW_RENEWAL_COUNT_SOL.md:195-216,475-498` proves
`C_1=128(1+log 2)` and
`G(p)=1/(p-2)+1/(p-2)^2`; `FW_REFEREE.md:319-370` independently confirms its
scope and paper-level status.

### 6.3 Exact `y<=100` matched-window stress

I reran the centered-Euclidean canonicalizer and depth recurrence used in
`DH_DEPTH_LAW_SOL.md:307-388`, enumerated the 1,037 exact theta keys with
`y=2c<=100`, and filtered the balanced image at `q=5,8,12`.  Finite-q heights
were represented in the exact fields with minimal polynomials
`lambda^2-lambda-1`, `lambda^4-4lambda^2+2`, and
`lambda^4-4lambda^2+1`; comparisons at every event were certified by rational
enclosures of width below `10^-89`.  Put

\[
 C_{\rm req}(Y)={B_{q,\,y\le100}(Y)\over
 Y^2 f_q(Y)},\qquad
 f_q(Y)=\begin{cases}Y,&Y\le q,\\qR^2+R^4,&Y>q.\end{cases}
\]

The event-grid maxima were

| `q` | matched rows | maximizing `Y` | window `B(Y)` | max `C_req` | window `B(100)` |
|---:|---:|---:|---:|---:|---:|
| 5 | 322 | `(3+sqrt(5))/2 = 2.6180339887498948482...` | 9 | `0.501552810007571` | 4312 |
| 8 | 588 | `2+2sqrt(2) = 4.8284271247461900976...` | 43 | `0.381989488776929` | 11049 |
| 12 | 764 | `4+2sqrt(3) = 7.4641016151377545871...` | 153 | `0.367924578678326` | 18821 |

Selected integer-event output was

```text
q=5:  Y=3 B=9 C_req=.333333333333; Y=20 B=836 C_req=.034319567064; Y=100 B=4312 C_req=.00128816936923
q=8:  Y=5 B=43 C_req=.344;          Y=20 B=895 C_req=.0522021794408; Y=100 B=11049 C_req=.00435051460329
q=12: Y=8 B=153 C_req=.298828125;   Y=20 B=631 C_req=.0483875453216; Y=100 B=18821 C_req=.00889364167325
```

Thus this exact-window data fits even `C_4=1` on its complete event grid, and
therefore easily fits the requested soft comparison `C_4 about 10`.  The
smallest margin from `2^100` at the three maxima is about `2.53*10^30`.

This is not an exact computation of the full `B_q(100)`.  Extending the theta
window while retaining `x<=100` immediately finds omitted terms:

| `q` | `B_{y<=100}(100)` | lower bound from `y<=400` | ratio of latter to the claimed unit-constant RHS at `Y=100` |
|---:|---:|---:|---:|
| 5 | 4312 | 36908 | `0.0110259` |
| 8 | 11049 | 37415 | `0.0147321` |
| 12 | 18821 | 37707 | `0.0178180` |

The increasing lower bounds illustrate exactly why the theta window cannot
certify the finite-height theorem.  They still show no hard violation, even of
a unit constant at this tested height.  Finite data are soft evidence only;
the symbolic marked-code proof is load-bearing.

## 7. Attack (g): upstream DH2, `(FW)`, and v29

The target uses the upstream statements accurately.

- `DH2_RENEWAL_PROOF_SOL.md:270-348` proves the nonnegative Chebyshev-block
  factorization, entrywise monotonicity, `x_X<=y_X`, and hence
  `m_X=x_X`, `x_X/m_X=1`, and
  `B_q(Y)=sum_{x_X<=Y}k_X^2`.  It explicitly warns at `:351-353` that this does
  not transfer the cutoff to `y<=Y`.
- `DH2_RENEWAL_PROOF_SOL.md:526-540` states exactly
  `k(W)<=1+2 sum_heavy |a_j|+2 ell(W)`, which becomes (2.7) after setting
  `A=sum_heavy|a_j|+ell(W)`.
- The same upstream note correctly leaves the two-mark residual open at
  `DH2_RENEWAL_PROOF_SOL.md:542-564,738-746`.  There is no contradiction: the
  target claims to close that precise gap with its new Lemma 4.1.
- `(FW)` has the stated constant and weighted consequence
  (`FW_RENEWAL_COUNT_SOL.md:195-216,411-498`).  Its referee records it as a
  paper theorem and explicitly says v29 does not machine-verify it
  (`FW_REFEREE.md:319-379,392-401`).
- v29's `sharp_no_wrap` theorem contains the explicit hypothesis
  `k<=N-1` (`RateCoreIV.lean:394-421`).  Its boundary-cancellation result is
  only finite free-product list algebra and does not assert the group
  presentation, canonical section, localization, or `(RATE)`
  (`RateCoreIV.lean:755-765`).  The target respects both limitations.

## 8. Claim ledger

| attacked claim | verdict | receipt |
|---|---|---|
| Lemma 4.1 injectivity | **CONFIRMED, paper-level** | reversible branch/tag decoder above; target `:465-590`; no collision in two independent finite searches |
| one-defect `w_(2,k)` and same-heavy diagonal | **CONFIRMED** | `DH_DEPTH_LAW_SOL.md:559-635`; target `:620-639` |
| core convolution and finite-q measure | **CONFIRMED** | target `:364-438`; Ford `M2_FORD_PACKING_REFEREE.md:64-116` |
| all Section 5 inequalities | **CONFIRMED** | independent calculations in Section 4 above |
| `C_4=2^100` sufficient | **CONFIRMED** | base budget `2^65`, with 35 bits of base slack and 34 even after one extra addition bit |
| theta-cutoff substitution | **FALSE, as target claims** | exact `(34,1970)` and `(89,11482)` replay; unbounded family distortion |
| Section 6 `J2/J4/wrap/R5` arithmetic | **CONFIRMED** | verbatim replay above |
| exact-window numerical violation | **NONE** | event-grid maxima `C_req<0.502`; `C=10` easily sufficient in the window |
| `y<=100` computes full finite-height `B_q` | **FALSE** | extended-window lower bounds rise sharply; target does not make this mistake |
| DH2/FW/v29 scope consistency | **CONFIRMED** | exact source lines in Section 7 |

## 9. Final verdict

**CONFIRMED.**  I could not refute `(DH_{2,4})`.  The boundary-core code has a
reversible case split, the finite-q Ford convolution is applied at the right
height and only as an overcount, every summation inequality closes, and the
explicit constant has overwhelming slack.  The finite stress tests find no
counterexample and in fact fit constants far below 10, but they are not used
as proof.  Promotion is justified only as a **paper-level conditional
two-mark theorem**; v29 does not certify it, and the remaining N1-RATE and R5
gates remain open exactly as the target states.

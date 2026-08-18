# Adversarial referee report on the balanced-section renewal count `(FW)`

**Date:** 2026-08-18  
**Target:** `research_notes/rh_goals_2026-08-14/lane_g/FW_RENEWAL_COUNT_SOL.md`  
**Verdict:** **CONFIRMED — paper-level, not machine-formalized.**

I found no counterexample, missing factor, reversed inequality, double count that
invalidates an upper bound, or lost atom. Subject to the already imported
paper-level theta canonical-form, cusp-stabilizer, and Ford-packing theorems,
the target proves

\[
A_{{\rm wrap},q}(Y)
\le 128(1+\log 2)\frac{Y^2}{q}
   \bigl(1+\log_+(Y/q)\bigr),\qquad q\ge3,\quad Y\ge q,
\]

and, for every fixed real \(\sigma>1\),

\[
E_{\rm wrap}(q,\sigma)=O_\sigma(q^{1-2\sigma}).
\]

The proof is not supplied by Aristotle v29: v29 proves a different finite
no-wrap sine envelope. The load-bearing FW step is the exact marked-letter
rank-one factorization in the target. There is no circular use of v29.

## 1. Referee findings

### (a) First-overflow uniqueness and injectivity — survives

The upstream canonical-form theorem gives one representative of every theta
double coset: the trivial word, the exceptional word \(Q\), or one unique word

\[
R^{a_0}Q\cdots QR^{a_k},
\]

with every exponent nonzero and with the two endpoint exclusions. This is the
actual content of
`M1_ROUTE_B_FREEPRODUCT_SOL.md:275-340`; the theta-key bijection is stated at
`:346-356`. The target's abbreviated restatement at
`FW_RENEWAL_COUNT_SOL.md:223-230` omits the singleton's additional
\(a_0\ne+1\) condition, but the proof never relaxes the upstream canonical
class, so this prose omission causes no extra word and no count error.

The image theorem says exactly that a theta class is in \(\operatorname{im}L_q\)
iff every canonical exponent is in the balanced alphabet
(`M1_ROUTE_B_FREEPRODUCT_SOL.md:442-495`). Hence every omitted class has a
unique least overflow index \(j\). The cut

\[
W=P R^{a_j}V
\]

at `FW_RENEWAL_COUNT_SOL.md:232-251` is therefore unique. The triple contains
the exact matrices \(P,R^{a_j},V\), so it reconstructs \(W\). Thus the map from
omitted canonical words to first-overflow triples is injective. Relaxing the
condition that \(P\) contains no earlier overflow can only add triples; it
cannot miss an omitted word. Different relaxed triples may evaluate to the
same matrix, but that is harmless overcount in (1.16), not undercount.

**Finding:** no double-counting or missed-word defect invalidates the upper
bound.

### (b) Prefix/suffix scales and the `O(r)` multiplicity — survives

For a nonempty prefix \(P=W_rQ\), the imported recurrence gives

\[
A=d_P-c_P=-U_r,
\qquad c_P=(U_r-U_{r-1})/2.
\]

The strict inequality \(|U_r|>|U_{r-1}|\) therefore implies
\(|c_P|<|A|\), exactly as claimed at
`FW_RENEWAL_COUNT_SOL.md:288-320`. The recurrence and strict inequality are
indeed present upstream at `M1_ROUTE_B_FREEPRODUCT_SOL.md:391-417`.

If \(|A|=r\), then \(-r<c_P<r\) gives \(2r-1\) possible integral values of
\(c_P\), two signs of \(A\), and then \(d_P=c_P+A\). Thus there are at most
\(4r-2<4r\) candidate signed bottom rows. If two admissible prefixes have the
same exact bottom row, direct multiplication gives

\[
P_2P_1^{-1}=\begin{pmatrix}1&m\\0&1\end{pmatrix}.
\]

Because this is in the theta group, the source-coordinate cusp stabilizer
forces \(m=2\ell\). For \(\ell>0\),
\(S^\ell P=(QR)^\ell P\) begins with an uncancelled \(Q\); the only dangerous
combination would require \(a_0=-1\), excluded canonically. For \(\ell<0\), it
begins with the forbidden \(R^{-1}\). Hence \(\ell=0\). The empty prefix has
scale one and still leaves the \(4r\) bound valid. This verifies
`FW_RENEWAL_COUNT_SOL.md:322-341` without a missing multiplicity factor.

The cited stabilizer proof is genuinely present at
`M1_ROUTE_B_REPAIR_SOL.md:369-460`: before width-one conjugation it gives the
source theta generator \(T_2=\left(\begin{smallmatrix}1&2\\0&1\end{smallmatrix}\right)\).
It is a paper-level geometric import using discreteness and a fundamental
polygon, not a Lean theorem.

For the suffix, in PSL,

\[
V^{-1}=R^{-a_k}Q\cdots QR^{-a_{j+1}}Q.
\]

It is an admissible prefix because \(a_k\ne1\), and its exact inverse bottom
row is \((-\gamma_V,\alpha_V)\), up to common PSL sign. Therefore
\(|\gamma_V|<|\alpha_V+\gamma_V|=|B|\), and inversion transfers the same
\(4r\) multiplicity bound. This validates
`FW_RENEWAL_COUNT_SOL.md:343-361`.

**Finding:** (1.5)--(1.10), including both `O(r)` bounds, are correct given the
cited cusp-stabilizer theorem.

### (c) Marked-letter product gain and the small-`q` patch — survives

The exact identity

\[
R^a=I+a\binom{-1}{1}(1,1)
\]

gives, with \(A=d_P-c_P\) and \(B=\alpha_V+\gamma_V\),

\[
c(PR^aV)=c(PV)+aAB,
\qquad c(PV)=c_PB+A\gamma_V.
\]

The two strict scale inequalities imply \(|c(PV)|<2|AB|\), hence, for
\(n=|a|\),

\[
c_H(W)=|c(W)|>(n-2)|AB|.
\]

These are exact calculations, not independence or generic-position claims
(`FW_RENEWAL_COUNT_SOL.md:363-398`). For \(q\ge8\), every overflow has
\(n\ge h=\lceil q/2\rceil\ge4\), so \(n-2\ge n/2\). Since
\(y=2c_H\le Y\), this yields the stronger strict inequality
\(n|A||B|<Y\); the displayed weak inequality (1.15) is safe
(`FW_RENEWAL_COUNT_SOL.md:400-405`).

For \(3\le q\le7\), the target invokes the cumulative Ford bound
\(A_\Gamma(Y)\le Y^2\). Its PSL double-coset proof, with constant one, is at
`M2_FORD_PACKING_REFEREE.md:81-118`. Therefore, for \(Y\ge q\),

\[
A_{{\rm wrap},q}(Y)\le Y^2
\le \frac{7Y^2}{q}\bigl(1+\log(Y/q)\bigr),
\]

and \(7<128(1+\log2)\). Thus the patch at
`FW_RENEWAL_COUNT_SOL.md:464-472` covers every real \(Y\ge q\), not merely the
tested finite box.

**Finding:** (1.11)--(1.15) and the \(q\le7\) patch are valid. The \(q\ge8\)
split is a convenience for \(n-2\ge n/2\), not an uncovered domain.

### (d) Convolution, constant, logarithm, and domain — survives

At fixed \(n=|a|\), \(r=|A|\), and \(s=|B|\), the relaxed triple count is at
most

\[
2(4r)(4s)=32rs.
\]

Together with \(nrs\le Y\), this proves (1.16). For real \(T\ge1\), putting
\(m=\lfloor T/r\rfloor\),

\[
\sum_{rs\le T}rs
=\sum_{r\le T}r\frac{m(m+1)}2
\le\sum_{r\le T}rm^2
\le T^2\sum_{r\le T}\frac1r
\le T^2(1+\log T).
\]

Thus (1.17) is correct. Monotonicity of \(1+\log(Y/n)\) and
\(\sum_{n\ge h}n^{-2}\le1/(h-1)\) give (1.18). For \(q\ge8\),

\[
h-1\ge q/4,
\qquad \log(Y/h)\le\log(Y/q)+\log2.
\]

Writing \(x=\log(Y/q)\ge0\),

\[
1+x+\log2\le(1+\log2)(1+x).
\]

Consequently

\[
C_1=32\cdot4\cdot(1+\log2)
   =128(1+\log2)
   =216.722839111673\ldots,
\]

with no lost factor (`FW_RENEWAL_COUNT_SOL.md:411-462`). The hypotheses
\(Y\ge q\) ensure both \(Y/h\ge1\) and \(x\ge0\); the proof does not silently
extend below its stated domain.

The logarithm is intrinsic to this relaxed divisor convolution:
\(\sum_{rs\le T}rs=\Theta(T^2\log T)\). It is therefore needed by the proof as
written. The argument does **not** prove that the true overflow count itself
requires a logarithm; removing it by exploiting additional correlations
remains possible and is irrelevant to the validity of the displayed upper
bound.

**Finding:** (1.16)--(1.20), the constant arithmetic, and the \(Y\ge q\)
domain are correct.

### (e) Weighted consequence and `sigma` dependence — survives

Upstream digit localization gives \(y\ge q\) for every omitted class
(`M1_ROUTE_B_FREEPRODUCT_SOL.md:515-530`). For \(p=2\sigma>2\), Tonelli's
theorem/layer cake gives

\[
\sum_H y_H^{-p}
=p\int_q^\infty A_{{\rm wrap},q}(t)t^{-p-1}\,dt.
\]

An atom at \(y=q\) is included: its indicator is present for every
\(t\ge q\), whose integral is exactly \(q^{-p}\). No boundary term is lost at
`FW_RENEWAL_COUNT_SOL.md:475-483`.

Substituting FW and then \(t=qu\) gives

\[
E_{\rm wrap}(q,\sigma)
\le pC_1q^{1-p}
\left(\frac1{p-2}+\frac1{(p-2)^2}\right).
\]

Equivalently, the fixed-\(\sigma\) coefficient is

\[
C_1\left(
  \frac{\sigma}{\sigma-1}
 +\frac{\sigma}{2(\sigma-1)^2}
\right).
\]

It diverges quadratically as \(\sigma\downarrow1\), so the result is not
uniform at that endpoint; the target claims only \(O_\sigma\), for which this
is exact. There is no hidden \(\log q\) (`FW_RENEWAL_COUNT_SOL.md:485-498`).

**Finding:** (2.1)--(2.2) and the stated sigma dependence are correct for every
fixed \(\sigma>1\).

### (f) Exact numerical stress test — no violation

I freshly replayed the exact centered-Euclidean canonicalizer and integer
matrix checks printed in `FW_RENEWAL_COUNT_SOL.md:75-166` with

```bash
sed -n '77,165p' \
  research_notes/rh_goals_2026-08-14/lane_g/FW_RENEWAL_COUNT_SOL.md \
| PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python -
```

Receipt:

```text
exact_keys_cH_le_384= 59931
marked_digit_occurrences_checked= 506750
factorization_assertions=PASS
max_abs_cPV_over_AB= 0.997389033943
observed_prefix_choice_max_ratio= 0.250000000000
observed_suffix_choice_max_ratio= 0.250000000000
```

For \(q=8,\ldots,48\), the fresh exact counts and normalized maxima were:

| \(Y/q\) | maximum of \(Aq/[Y^2(1+\log(Y/q))]\) | attaining \(q\) | exact \(A\) there |
|---:|---:|---:|---:|
| 1 | 0.125000000000 | 8 | 1 |
| 2 | 0.166110780698 | 8 | 9 |
| 4 | 0.124408373433 | 8 | 38 |
| 8 | 0.109724643390 | 8 | 173 |
| 16 | 0.100436670387 | 8 | 776 |

All are below \(0.00077C_1\). I also evaluated ratios
\(1,1.01,1.05,1.125,1.25,1.5,1.75,2,3,5,10,16\). Because the exact count
changes only at even heights \(y=2c_H\), an exhaustive event-grid scan of
\(Y=q\) and every even jump through \(Y=16q\) checks the intervening real
intervals as well: their numerator is constant and their denominator is
increasing. The largest required constant over this whole box was

```text
q=8, Y=12, A_wrap=5, required_C=0.197641176700
```

versus \(C_1=216.722839111673\), a factor \(1096.5\) margin.

Edge cases:

```text
q=8: Y=8  A=1;  Y=9  A=1;  Y=12 A=5;  Y=16 A=9
q=9: Y=9  A=0;  Y=10 A=2;  Y=12 A=4;  Y=18 A=10
```

For \(q=3,\ldots,7\), the same exact enumeration found a maximal theorem
normalization of \(0.291220952767\), at \(q=3,Y=4,A=2\), still far below
\(C_1\). More importantly, the Ford argument above proves the patch for all
\(Y\), independently of this finite experiment.

The census covers \(c_H\le384\), hence \(Y\le768\), and cannot prove a uniform
theorem or tail asymptotic. It is a falsification test only; it found no fatal
violation.

### (g) Upstream and v29 consistency — survives, no circularity

The target accurately uses the upstream source:

- canonical representative and endpoint conditions:
  `M1_ROUTE_B_FREEPRODUCT_SOL.md:275-340`;
- theta-key/canonical-word bijection:
  `M1_ROUTE_B_FREEPRODUCT_SOL.md:346-356`;
- source matrices, recurrence, strict growth, and digit-height bound:
  `M1_ROUTE_B_FREEPRODUCT_SOL.md:361-440`;
- balanced alphabet, exact image, and overflow support:
  `M1_ROUTE_B_FREEPRODUCT_SOL.md:442-530`.

The harvested v29 theorem `sharp_no_wrap` is at
`projects/aristotle_dispatch_v29/result/v29sub_aristotle/RateCoreIV.lean:394-421`.
It concerns syntactically reduced raw \(Q,S\) words at finite
\(\lambda_N=2\cos(\pi/N)\), with depth at most \(N-1\). A fresh stdin
typecheck exited zero, and `#print axioms RateCoreIV.sharp_no_wrap` returned

```text
'RateCoreIV.sharp_no_wrap' depends on axioms:
[propext, Classical.choice, Quot.sound]
```

with no `sorryAx`. But v29 explicitly says its boundary lemma does not assert
the group presentation, canonical section, or a RATE estimate
(`RateCoreIV.lean:755-765`).

The FW proof at `FW_RENEWAL_COUNT_SOL.md:223-473` never invokes
`sharp_no_wrap`, `lamN`, a sine ratio, or finite-depth growth. It instead uses
the theta canonical word and the exact identity
\(c(PR^aV)=c(PV)+aAB\). Its statement that the marked factorization is
"stronger" is accurate operationally—this factorization supplies the product
constraint that the envelope does not—but it should not be read as a formal
logical strengthening of the v29 theorem.

**Finding:** no circular or contradictory use of v29. Machine verification of
v29 does not machine-verify FW.

## 2. Claim ledger

| Claim under attack | Verdict | Receipt |
|---|---|---|
| First-overflow cut is unique/injective | **CONFIRMED** | `FW_RENEWAL_COUNT_SOL.md:221-251`; upstream uniqueness `M1_ROUTE_B_FREEPRODUCT_SOL.md:275-340` and exact image `:470-495` |
| Prefix/suffix inequalities (1.5), (1.7)--(1.10) | **CONFIRMED** | `FW_RENEWAL_COUNT_SOL.md:264-361`; recurrence upstream `M1_ROUTE_B_FREEPRODUCT_SOL.md:391-417` |
| At most `4r` prefix and suffix states | **CONFIRMED, paper-level dependency** | `FW_RENEWAL_COUNT_SOL.md:322-361`; cusp stabilizer `M1_ROUTE_B_REPAIR_SOL.md:369-460` |
| Product constraint \(|a||A||B|\le Y\), \(q\ge8\) | **CONFIRMED** | `FW_RENEWAL_COUNT_SOL.md:363-405` |
| Ford patch, \(3\le q\le7\) | **CONFIRMED, paper-level dependency** | `FW_RENEWAL_COUNT_SOL.md:464-472`; Ford count `M2_FORD_PACKING_REFEREE.md:81-118` |
| Convolution and \(C_1=128(1+\log2)\) | **CONFIRMED** | `FW_RENEWAL_COUNT_SOL.md:411-462` |
| Relative logarithm | **CONFIRMED as an upper-bound factor** | Needed by the relaxed divisor convolution; not proved optimal for the actual count |
| \(Y\ge q\) domain | **CONFIRMED** | Used explicitly in (1.17)--(1.20); small-\(q\) patch also uses it |
| \(E_{\rm wrap}=O_\sigma(q^{1-2\sigma})\) | **CONFIRMED for fixed \(\sigma>1\)** | `FW_RENEWAL_COUNT_SOL.md:475-498`; coefficient displayed above |
| Exact census respects the claimed constant | **CONFIRMED on the tested box** | Fresh 59,931-key replay and exhaustive event grid through \(Y=16q\) |
| Consistency with v29 `sharp_no_wrap` | **CONFIRMED / ORTHOGONAL** | `RateCoreIV.lean:394-421,755-765`; fresh stdin typecheck |

## 3. Nonfatal status cautions

1. **Paper-level, not fully machine-certified.** The theta canonical-form and
   image theorem are paper proofs; the `4r` uniqueness step imports a
   Pohl-based cusp-stabilizer proof; the \(q\le7\) branch imports Ford geometry.
   Aristotle v29 certifies none of the marked-renewal counting argument.
2. **The finite census is not proof.** It is exact inside its displayed box and
   strongly nonviolating, but the theorem rests on the symbolic argument.
3. **Log optimality is open.** The log is unavoidable after the proof's
   relaxation, not shown necessary for the true overflow count.
4. **Some status prose is stale.** `DENSITY_GAIN_ATTACK_SOL.md:634-636` still
   calls FW conjectural, while `FW_RENEWAL_COUNT_SOL.md:520-522` explicitly
   supersedes that earlier status. This is a documentation mismatch, not a
   proof contradiction.
5. **Full `(RATE)` remains open.** FW closes the unpaired-overflow obstruction,
   but `(DH)` and the retained interval/N1 input remain open, as the target
   itself states at `FW_RENEWAL_COUNT_SOL.md:524-537`.

## 4. Final verdict

**CONFIRMED.** I could not refute `(FW)` or its weighted consequence. The
marked-first-overflow factorization is injective at the canonical-word level;
the prefix/suffix multiplicities are genuinely linear in their scales; the
rank-one marked letter supplies the required product gain; all constant and
domain arithmetic closes; the Ford patch covers \(q\le7\); partial summation
has the claimed fixed-\(\sigma\) dependence; and the exact census supplies no
counterexample. The appropriate promotion is **paper-level theorem**, not
"machine-verified FW" and not "full RATE proved."

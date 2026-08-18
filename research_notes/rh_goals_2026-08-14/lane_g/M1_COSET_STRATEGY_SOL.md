# M1 — coset-level normal-form strategy

**Status: STRATEGY ONLY.** This file is a proof plan for the corrected M1
obligation. It is not a proof of M1, not a proof of (RATE), and not a theorem
closure. Every mathematical statement below that is not explicitly marked
`RECEIPTED` or `PROVED` is marked `CONJECTURAL`.

## 0. Scope and source ledger

The working model is Hejhal's conjugated model
`S = [[1,1],[0,1]]`,
`Q_λ = [[0,-1/λ],[λ,0]]`,
`λ_q = 2 cos(π/q)`, with `λ_∞ = 2`. Hejhal's extraction gives the
double-coset Dirichlet series over `[S]\𝒢_q/[S]` and the `N`-independent
analytic majorant that M1 is supposed to make effective:
`LAW_HEJHAL_S7_EXTRACT.md:19-31,87-99,127-142`.

The load-bearing finite-q facts are:

* `c` is unchanged by left or right powers of `S`; right multiplication sends
  `d` to `d + b c`, so the secondary invariant is the orbit `d mod c`:
  `LAW_R1_COSET_STRUCTURE.md:76-88`.
* The raw `Q,S^n` alphabet is not a reduced presentation; the finite group has
  `Q^2 = 1`, `(Q S)^q = 1` in PSL, and the theta limit is parabolic:
  `LAW_R1_COSET_STRUCTURE.md:76-81,90-119`.
* The rank matching in R1 is explicitly a proxy, and the enumerator is not a
  completeness proof: `LAW_R1_COSET_STRUCTURE.md:327-351`.
* R2's `[CORRECTION v27]` replaces the false c-only word map with a coset-level
  normal-form statement having four separate obligations (well-definedness,
  injectivity, surjectivity, localization):
  `LAW_R2_RATE_LEMMA_DRAFT.md:405-425`.
* The referee audit identifies the same defect and says that the `[1,2]` and
  `[2,1]` collision is only for the c-only proxy; their lower-right entries can
  still separate the double cosets:
  `RATE_NOTEGRAPH_REFEREE_AUDIT.md:16-27,200-212`.

The v27 harvest is the boundary of what is already certified. It proves the
depth-three closed form and the c-only refutation, the repaired product
invariant, the `λ=2` evenness shape, and the theta multiplicity count:
`projects/aristotle_dispatch_v27/result/aristotle_dispatch_v27_aristotle/RateCoreII.lean:67-124,128-176`;
the dispatch records an independent zero-sorry build at
`projects/aristotle_dispatch_v27/DISPATCH.md:42-53`.

`LAW_U2B_CLOSURE.md:52-88,246-265` supplies a useful repo-derived algebraic
ingredient: after writing `R = Q S`, the blocks `S R^a` and `S R^{-a}` are
products of the recurrence `u_{j+1}=λu_j-u_{j-1}`. That note is a strategy
input here, not an external source-identification proof of M1.

Primary-source anchors, and their exact evidentiary limits, are:

* **RECEIPTED (Hejhal, Lemma 3.1, printed p. 525).** In the un-conjugated
  theta-group convention, the double cosets are indexed by `c_H>0`,
  `0≤d_H<2c_H`, `gcd(c_H,d_H)=1`, and `c_H+d_H` odd. Source scan:
  `../lane_p/literature/Hejhal_LNM1001_Vol2_ch11s3_pp524-532.pdf`.
* **RECEIPTED (Mayer--Mühlenbruch, arXiv:0902.3953, §§2.2, 2.5, 6.1).**
  This gives the q-regular/dual-q-regular forbidden-block languages, finite
  continued-fraction ambiguity, the group-word conversion, real-line
  equivalence, and conversion to reduced Rosen fractions. It does **not**
  state the Hejhal parabolic-double-coset bridge needed below.
* **RECEIPTED (Kraaikamp--Lopes, DOI 10.1007/BF00181695).** The theta-group
  endpoint has an even-partial-quotient/geodesic coding. It is an endpoint
  anchor, not a proof that finite-q canonical codes specialize bijectively to
  Hejhal's double-coset data.

## 1. Correct object: keys of double cosets, not c-values of words

Put `R_λ := Q_λ S`. In PSL, `Q_λ` has order two; at finite level `R_λ` has
order `q`, while `R_2` is parabolic. The conversion between a raw word
`Q S^{n_1} Q ⋯ S^{n_{k-1}} Q` and a `Q,R` word must be done explicitly using
`S = Q R` (in PSL); an exponent `n_i` in the raw alphabet is **not** silently
identified with a Rosen digit.

For a matrix `g = [[a,b],[c,d]]` with `c ≠ 0`, choose the PSL sign so that
`c > 0` and define

```text
  key_λ(g) := ( c , [d]_c ),
  [d]_c := { d + n c : n ∈ ℤ },
  red_c(d) := d - c floor(d/c) ∈ [0,c).
```

Left multiplication by `S^u` leaves `(c,d)` fixed; right multiplication by
`S^v` leaves `c` fixed and replaces `d` by `d+vc`. Thus `key_λ` is a
well-defined **invariant** of a double coset. Completeness of this invariant
for the finite Hecke double-coset set is not assumed here; it is one of the
normal-form obligations below.

The normalization dictionary is exact. Let the source generators be
`E=[[0,-1],[1,0]]`, `T_λ=[[1,λ],[0,1]]`, and put
`A_λ=diag(λ^{-1/2},λ^{1/2})`. Direct multiplication **PROVES**

```text
  A_λ E A_λ^{-1}   = Q_λ,
  A_λ T_λ A_λ^{-1} = S,
  A_λ [[a,b],[c_H,d_H]] A_λ^{-1}
      = [[a,b/λ],[λ c_H,d_H]].
```

At `λ=2`, this direct dictionary and the certified theorem `c_two_even` give
the conjugated lower-left entry `c_2(g)=2 c_H` with `c_H ∈ ℤ`. Keep the two
normalizations separate:

```text
  C_conj := c_2(g) = 2 c_H,
  D_conj := d_2(g) = d_H.
```

Therefore the conjugated key `(C_conj, D_conj mod C_conj)` is **PROVED** to be
the Hejhal/source key `(c_H, d_H mod 2 c_H)` after division of the first
coordinate by two. Define the source-coordinate theta key by

```text
  thetaKey(g) := ( c_H := c_2(g)/2,
                   d_H := red_{c_2(g)}(d_2(g)) ).
```

The Hejhal coordinate set, **RECEIPTED** from Lemma 3.1, is

```text
  H_∞ := { (c_H,d_H) : c_H > 0, 0 ≤ d_H < 2 c_H,
             gcd(c_H,d_H)=1, c_H+d_H ≡ 1 (mod 2) }.
```

This is the Ch. 11 §3 data transcribed in `RateCoreII.lean:159-176`. The
coordinate experiment in §8 remains a required negative control against an
implementation mixing the two conventions; it is no longer an unproved
scaling assumption.

## 2. Candidate Rosen/geodesic normal form

### 2.1 The coding alphabet

Use the standard `(2,q,∞)` tessellation for the fundamental region
`𝒟_q = {|x|<1/2, |z|>1/λ_q}` from
`LAW_HEJHAL_S7_EXTRACT.md:19-24`. There are two alphabets and they must not be
identified. A Rosen digit `a∈ℤ\{0}` is the inversion--translation block

```text
  D_a(λ) := Q_λ S^a = Q_λ (Q_λ R_λ)^a        in PSL,
  R_λ := Q_λ S.
```

This is the conjugate of the source word `E T_λ^a` in
Mayer--Mühlenbruch (2.2.4). A raw exponent `a` is therefore not an exponent
of `R`. Only after concatenating the `D_a` blocks should the word be converted
with `S=QR` and reduced in the presentation alphabet `{Q,R}`.

The recurrence blocks useful during that second reduction are (up to the PSL
sign)

```text
  M_a(λ) = [[u_a,u_{a+1}],[u_{a-1},u_a]],
  u_0=0, u_1=1, u_{j+1}=λu_j-u_{j-1}.
```

The exact identities and nonnegative-block route are recorded at
`LAW_U2B_CLOSURE.md:70-88`; that note calls the order-two generator `S`,
whereas this file calls it `Q`, so its `S R^{±j}` becomes `Q R^{±j}` here.
Those are presentation-reduction blocks, not Rosen digit blocks. They make the
matrix entries explicit Laurent/polynomial functions of `λ`.

**CONJECTURAL for this strategy:** after a complete Rosen word is converted
and freely reduced in `{Q,R}`, the only additional finite-level group
identification needed is `R^q=1`. This must be proved from the full PSL
presentation and still does not prove that the Rosen forbidden-language
cross-section is complete for parabolic double cosets.

The Rosen digit alphabet stays `ℤ\{0}`. Separately, choose a centered set of
nonzero representatives for exponents of a finite cyclic `R`-syllable,
for example

```text
  E_q = { -⌊(q-1)/2⌋, …, -1, 1, …, ⌈(q-1)/2⌉ },
```

with a fixed `+q/2` representative when `q` is even. For `q=∞`, use
`E_∞=ℤ\{0}`. The Rosen endpoint tie and this cyclic-residue tie are distinct
conventions; both must be carried in a normal-form receipt.

### 2.2 Rosen map and endpoint data

Work first in the un-conjugated Hecke coordinate, where the nearest-
`λ_q` interval is `I_q=[-λ_q/2,λ_q/2]`. Use the source convention

```text
  a_q(x) := nearest integer to -1/(λ_q x),
  f_q(x) := -1/x - a_q(x) λ_q,
  ψ_{a,λ_q}(y) := -1/(y+a λ_q).
```

The half-integer nearest-integer tie must be fixed once. If a signed Rosen
alphabet `(ε,r)` is used later, it must be derived from these integer `a`
digits through the reduced-Rosen conversion of Mayer--Mühlenbruch §6.1; the
different-looking map `ε/x-aλ` is not substituted silently. Conjugate the
branch matrices by `A_λ`; this fixes the scale before comparing `c,d`. The
algorithm is:

1. Start with the two ideal endpoints of the geodesic represented by `g`.
2. Apply `f_q` to the endpoint in `I_q`, recording `a_i` until the
   geodesic reaches the cusp. Remove the initial and terminal parabolic `S`
   runs; this is the double-coset quotient.
3. Convert the digits to the `Q,R` block word, reduce adjacent inverse
   blocks, and apply the centered-residue rule at finite `q`.
4. At a rational endpoint with two finite expansions, use one declared
   terminal convention (the shorter code, then the sign tie-break). Record the
   convention in every receipt.

The regular-language test is not an unspecified rewrite oracle. Put
`h_q=(q-2)/2` for even `q` and `h_q=(q-3)/2` for odd `q`. Equation (2.2.2)
of Mayer--Mühlenbruch **RECEIPTS** the forbidden blocks

```text
  q=3:       (±1), (±2,±m),                         m≥1;
  q even:    (±1)^(h_q+1), ((±1)^h_q,±m),          m≥1;
  q odd≥5:   (±1)^(h_q+1),
              ((±1)^h_q,±2,(±1)^h_q,±m),           m≥1,
```

where every sign inside one block is the same. A forward digit sequence is
q-regular when it avoids these blocks; its reversal must also avoid them to
be dual q-regular. The **CONJECTURAL** step for M1 is that this forward-and-
reverse condition, with the finite terminal ambiguity of Lemma 2.2.2 fixed,
is exactly the required parabolic double-coset cross-section.

The following is the required coding theorem, stated as a target rather than
an assumption.

> **CONJECTURAL NF–Rosen bridge.** For every `q∈{3,4,…,∞}`, the above
> reduction terminates on every `c≠0` double coset, returns a unique code after
> the endpoint tie-break, and two inputs have the same code if and only if
> their `(c,d mod c)` double-coset keys agree. A finite code is q-bireduced
> when its finite replay uses no `R^q` relator, no centered-residue boundary
> tie, and no forbidden rewrite block. It is **stable** when its q-bireduced
> replay remains canonical under theta specialization at `λ=2`. Replacing
> every block's `λ_q` by `2` then gives the theta code with the same integer
> digits.

The bridge has deliberately been split into termination, uniqueness,
double-coset completeness, and the finite-relation criterion; any one may
fail independently and must be falsified independently.

### 2.3 What “near relation” means

For a finite code `w`, define `firstWrap_q(w)` to be the first Rosen reduction
state at which the centered residue rule would invoke `R^q=1`, hit its
boundary tie, or require a forbidden q-rewrite block. Define `near_q` to be
the set of codes with a finite `firstWrap_q` state. This is a computable
symbolic condition on the code; it does not use a floating-point comparison of
`c`.

A floating-point, greedy-representative diagnostic suggests the following
inclusive prefix cutoff in conjugated coordinates:

```text
  c_*^{conj}(q)    := 2 floor((q-1)/2),
  C_crit^{conj}(q) := 2 ceil(q/2).
```

Equivalently, in the source coordinate above,
`c_*^H(q)=floor((q-1)/2)` and `C_crit^H(q)=ceil(q/2)`. This candidate is
**CONJECTURAL**. The diagnostic found the first unmatched conjugated theta
height at `C_crit^{conj}=q` for `q=12,16,24`, and at
`C_crit^{conj}=q+1` for `q=11,13,15,17,23`, with none below. This is not an
exact census: it inherits floating keys, a greedy representative choice, a
finite depth, and a finite cutoff. The proof must replace it with an exact
all-code statement. Matchedness is **not** defined by a height cutoff:
high-height codes with no forbidden/rewrite event may still be stable matches.

## 3. Corrected M1: four separate target obligations

Let `𝒞_q` be finite-level `[S]\𝒢_q/[S]` classes with `c_q>0`, and let
`𝓗_∞(c_*^H) := {H∈H_∞ : c_H(H)≤c_*^H(q)}`. Let `𝒞_q^match` be the
classes whose canonical q-bireduced code is **stable** at `λ=2`; this is not a
height predicate. Define the candidate specialization

```text
  L_q : 𝒞_q^match → H_∞,
  L_q([g]) := thetaKey( eval_{λ=2}( NF_q(g) ) ).
```

The `eval_{λ=2}` operation means “reuse the same block code and matrix
multiply with `Q_2,S`”; it is not a new word search.

### M1-W — well-definedness (CONJECTURAL)

For all representatives `g,g'` and all raw words `w,w'` that represent the
same finite double coset,

```text
  [g] = [g']  ⇒  key_{λ_q}(g) = key_{λ_q}(g'),
  [w] = [w']  ⇒  NF_q(w) = NF_q(w')
                    ⇒ thetaKey(eval_2(NF_q(w)))
                       = thetaKey(eval_2(NF_q(w'))).
```

The middle implication is the finite-q normal-form theorem; the last is the
endpoint/parabolic quotient check. This obligation must include sign choice
`c>0`, the terminal Rosen tie, and invariance under both left and right
parabolic powers. It is stronger than “the same raw word gives the same
limit”, which was already clear from the Laurent-polynomial observation in
`LAW_R2_RATE_LEMMA_DRAFT.md:126-141`.

**CONJECTURAL auxiliary key-completeness target:** on the coding domain, equal
`key_{λ_q}` values imply equal canonical codes. It is intentionally separate
from the elementary statement that equal double cosets have equal keys.

### M1-I — injectivity on matched classes (CONJECTURAL)

For `X,Y ∈ 𝒞_q^match`,

```text
  L_q(X) = L_q(Y)  ⇒  X = Y.
```

The intended proof is: theta Rosen uniqueness gives the same canonical block
code; `q`-faithfulness means no `R^q` relator can identify two different
finite codes; then M1-W converts code equality to equality of the finite
`(c,d mod c)` keys. This is precisely the step that the old c-only axiom got
wrong.

### M1-S — surjectivity onto the Hejhal subrange (CONJECTURAL)

For every `H=(c_H,d_H) ∈ 𝓗_∞(c_*^H)`, let `w_∞(H)` be its canonical theta Rosen
code. Then

```text
  replay_q(w_∞(H)) is q-bireduced and stable at `λ=2`,
  ∃ X ∈ 𝒞_q^match,  L_q(X)=H,
  and key_{λ_q}(X) is the key obtained from replay_q(w_∞(H)).
```

The proof direction must be inverse coding, not rank matching: recover the
theta code from `(c_H,d_H)`, replay exactly the same branch sequence at `λ_q`,
verify the determinant/group relation, and verify that no finite-q wrap was
needed. This is the onto statement needed to replace the R1 sorted-spectrum
proxy.

### M1-L — localization of the complement (CONJECTURAL)

The complement must be localized by the *first relation event*, not merely by
large numerical `|c|` observed in a window:

```text
  𝒞_q \ 𝒞_q^match ⊆ { X : canonical code(X) ∈ near_q },
  H_∞ \ im(L_q) ⊆ { H : w_∞(H) has firstWrap_q }.
```

The quantitative strengthening required by the R2 sum is also a separate
conjecture:

```text
  ∃ κ>0, q₀, ∀q≥q₀, every first-wrap code has
  min( c_q(replay_q(w)), 2 c_H(eval_2(w)) ) ≥ κ q,
```

or an explicit replacement inequality strong enough to sum the complement at
`Re s>1`. No such `κ` is claimed here. The finite-window quantity
`Σ_{10≤|c|≤50}|c|^{-2.2}≤0.26` is only an empirical partial-window mass and
cannot discharge M1-L or M2 (`LAW_R1_COSET_STRUCTURE.md:285-323`).

## 4. Proof route, in dependency order

### Phase A — exact algebra and quotient bookkeeping

1. Define matrices over an explicit coefficient ring (`ℤ[λ]` with the
   relation for `λ_q`, or exact real algebraic numbers for fixed `q`). Prove
   `Q^2=-I`, `R=QS`, and `R^q=±I` for `λ_q`; prove that `R_2` is parabolic.
2. Implement `key_λ` as the orbit under integer translations, with a proof
   that left/right `S` actions have exactly the stated effect on `(c,d)`.
3. Implement the centered residue alphabet and a terminating rewrite system
   for `Q,R` words. Prove each rewrite preserves the matrix in PSL and prove
   confluence by checking all critical overlaps, including the even-q tie.
4. Add endpoint states for `c=0` and `c≠0`; M1 concerns only the latter. A
   `c=0` branch must be rejected, not silently assigned a residue class.

Steps 1–3 are finite algebra/order reasoning and are suitable Lean/Aristotle
targets. They are not yet the NF–Rosen bridge; mark their eventual theorem
names separately from M1.

### Phase B — geodesic/Rosen identification (CONJECTURAL)

1. Prove that the side-crossing sequence of the standard tessellation is the
   Rosen digit sequence generated by `f_q` and that removing the two cusp
   tails is exactly quotienting by left/right `S`.
2. Prove that the block matrix product from the digit sequence equals the
   original matrix up to the endpoint `S` factors. In particular, the lower
   row of the product computes the same `(c,d mod c)` key.
3. Prove termination for finite cusp-to-cusp geodesics and uniqueness after
   the declared rational-endpoint tie-break. Prove the theta limit separately;
   parabolic endpoint cases cannot be obtained by continuity alone.
4. Prove the finite relation criterion: a code is replayable at `λ_q` without
   ambiguity iff no `R^q` wrap/centered-boundary event occurs. This is where
   `ℤ₂ * ℤ_q` versus `ℤ₂ * ℤ` enters; it cannot be replaced by a c-value test.

This is the source-identification/geometry part of M1. It is not discharged
by a finite BFS, by the c-only Lean theorem, or by the nonnegative-block
identities in `LAW_U2B_CLOSURE.md`.

### Phase C — specialization and the four M1 gates (CONJECTURAL)

There is a wrong-way-map trap here. The abstract presentation gives the
quotient `ℤ₂*ℤ → ℤ₂*ℤ_q` by imposing `R^q=1`; there is no homomorphic inverse
sending the order-q generator to the infinite-order theta generator. This
order obstruction is **PROVED** directly from the presentations. Therefore
`λ_q→2` is not a group homomorphism on finite-q classes. `L_q` can only be
defined after choosing the **CONJECTURAL** q-bireduced canonical section and
specializing its code.

For each q-faithful code, specialize the *same* symbolic block product from
`λ_q` to `2`. Laurent-polynomial continuity gives the entrywise limit, while
M1-W/I/S/L supply the class-level assertions. Run the gates in this order:

1. **W:** representative/endpoint invariance and key normalization.
2. **I:** theta-code uniqueness plus no finite relator on the matched domain.
3. **S:** inverse replay of every theta key below the certified `c_*^H(q)`.
4. **L:** first-wrap classification of every remaining class and a proved
   denominator/height inequality for the first-wrap state.

Do not use an unproved injectivity or surjectivity gate to justify the next
one; each receipt must expose its own hypotheses.

### Phase D — only then connect to R2 (CONJECTURAL)

After M1-W/I/S/L are proved, the R2 split becomes a theorem-level partition:
matched pairs receive the P3/P4/P5 mean-value estimate, while first-wrap
classes receive the localization bound. The universal derivative envelope
`(C1)` is still a separate R2/N1 obligation; the tail majorant M2 is still a
separate analytic obligation. Therefore M1 completion alone would not prove
the RATE lemma or the `q^{1-2σ}` exponent.

## 5. Why `[1,2]`/`[2,1]` is a certified failure of the old proxy

This is **PROVED**, not conjectural. The harvested theorem
`c_depth_three` gives

```text
  c_λ([n,m]) = λ ( n m λ² − 1 ).
```

Consequently `[1,2]` and `[2,1]` have the same `c` at every `λ`; at `λ=2`
both have `c=14`. `wordLimitMap_not_injective_depth_three` proves that the
v26 `Set.InjOn (w ↦ c_2(w))` statement is false at `K=3`, and
`c_depth_three_injective_in_product` proves the surviving c-only invariant is
the product `n m`:
`RateCoreII.lean:67-124`.

The same direct multiplication gives the lower-right entries

```text
  d_λ([n,m]) = −n λ,       d_λ([m,n]) = −m λ.
```

At `λ=2` the two certified-control matrices are explicitly

```text
  W_[1,2] = [[-4, 1/2], [14, -2]],   key = (14, 12),
  W_[2,1] = [[-2, 1/2], [14, -4]],   key = (14, 10),
```

where the second key coordinate is reduced modulo the conjugated `c=14`.

For `[1,2]` versus `[2,1]`, the `d` values differ. At `λ=2`, the difference
is `2`, while `c=14`, so no integer right translation `d↦d+b c` identifies
them. Thus the collision is exactly a projection defect: `c` forgets the
endpoint residue, whereas `(c,d mod c)` retains it. This explains why the
coset quotient repairs this particular defect without claiming that every
possible full-key collision has been ruled out; M1-I is precisely the proof
that no further collision occurs on the matched normal-form domain.

## 6. Formalization boundary: algebraic versus geometric/analytic obligations

| Item | Status now | Appropriate proof route |
|---|---|---|
| `c_depth_three`, collision, product invariant | **PROVED** | Existing zero-sorry v27 Lean harvest (`RateCoreII.lean:67-124`). |
| `λ=2` matrix shape, even `c`, `φ(2c_H)` count | **PROVED** | Existing v27 Lean harvest (`RateCoreII.lean:128-176`) plus the direct `A_2` coordinate dictionary in §1. |
| Q/R block identities and recurrence | **RECEIPTED repo algebra** | Lean induction over matrices/polynomials; reuse `LAW_U2B_CLOSURE.md:70-88`. |
| Translation action and arithmetic key normalization | **CONJECTURAL target; Lean-formalizable** | Exact matrix multiplication, integer floor/mod lemmas, PSL sign quotient. |
| Finite Q/R rewrite termination/confluence | **CONJECTURAL target; Lean-formalizable** | Finite critical-pair enumeration for each q plus a uniform residue proof. |
| Rosen branch = tessellation/geodesic coding | **CONJECTURAL; source-identification obligation** | Hyperbolic fundamental-domain proof; cannot be inferred from matrix numerics. |
| Unique theta code, including rational endpoint tie | **CONJECTURAL; analytic/geometric** | Rosen natural-extension/endpoint theorem, then formalize the arithmetic core. |
| M1-W, M1-I, M1-S, M1-L | **CONJECTURAL** | Depend on the preceding coding theorem; prove as four separate theorems. |
| `c_*^H(q)` and a first-wrap height/denominator bound | **CONJECTURAL** | Exact finite-state search first; uniform inequality second. |
| R2 derivative envelope (C1), tail M2, and `q^{1−2σ}` summation | **CONJECTURAL, outside M1** | Analytic estimates and N-uniform majorants; M1 does not discharge them. |

The key boundary is deliberate: Lean can certify finite algebra, exact
normalization, and finite-depth counterexamples; it cannot by itself identify
the geometric Rosen coding or prove a source-dependent Hejhal coordinate
theorem without those definitions and hypotheses being formalized.

## 7. Expected failure modes

These are not hypothetical assurances; each is a named way the proposed
strategy can fail and therefore gets a falsification test before any theorem
promotion.

1. **Width normalization failure.** Mixing the width-one conjugated `S` with
   a width-`λ` source convention changes `d mod c`, the range of `D`, or the
   parity condition. This is the highest-priority source-identification risk.
2. **Rosen endpoint tie failure.** A rational cusp endpoint may have two finite
   expansions. If the terminal tie rule is not applied identically at `λ_q`
   and `2`, well-definedness fails at the boundary.
3. **Residue-alphabet failure.** The centered representative at even `q` can
   be chosen with the wrong sign, creating duplicate codes or silently using
   an `R^q` relation.
4. **c-only collision.** The certified `[1,2]`/`[2,1]` example must remain a
   collision in `c` and a separation in the full key. Any implementation that
   loses this control is testing the obsolete proxy.
5. **Hidden elliptic wrap.** A code that looks short in the raw `Q,S^n`
   alphabet may contain an `R^q` reduction after conversion. Such a class must
   be marked near-relation, not counted as matched.
6. **Cancellation/zero failure.** Signed digits can make `c_{λ_q}` vanish or
   become very small while the theta replay is nonzero. Exact algebraic zero
   tests are required; floating-point thresholds are not a definition of
   matchedness.
7. **Sign and residue duplication.** The PSL `±I` choice and the `d mod c`
   representative can double-count a class unless `c>0` and a half-open
   residue interval are enforced globally.
8. **Non-confluence.** Two rewrite paths can produce different centered codes
   even when the matrices agree. Critical-pair checks and random relator
   insertion are required before using code equality for M1-I.
9. **False localization.** An unmatched class may have no first-wrap event,
   or first-wrap denominators may grow slower than the proposed `κq`. This
   would refute M1-L or force a weaker analytic complement bound.
10. **Finite-window illusion.** Stable counts at `X=50`, depth `≤12` can hide
    a longer code or larger theta denominator. Enumeration saturation must be
    rerun at increasing depth and cutoff with independent coding and matrix
    routes.
11. **Wrong-way specialization.** Treating `λ_q→2` as a homomorphism from
    `ℤ₂*ℤ_q` to `ℤ₂*ℤ` ignores `R^q=1`. Every proposed map must expose its
    canonical code section; otherwise a finite relator can acquire a false
    theta image.

## 8. Falsification-first experiment packet

Every experiment below must emit exact keys, codes, and a failure witness; a
pass is evidence for the next gate, never a theorem.

1. **Coordinate gate (q=3,4,5,6,7,8).** Recheck the diagonal conjugation and
   compare the width-one key `(C_conj=2c_H, d_H mod 2c_H)` with Hejhal's
   `(c_H,d_H)` conditions. Check `c_H=1,2,3` by direct matrices and the certified
   `theta_coset_count`. Falsify immediately on a parity/range mismatch.
2. **Rewrite gate.** Enumerate all `Q,S^n` words up to raw depth 12, convert to
   Q/R codes, and compare exact PSL matrices and canonical keys. Inject
   `R^q` relators at every position. Any changed key for a claimed rewrite is
   a confluence failure.
3. **Known collision control.** Include `[1,2]` and `[2,1]` in every run;
   assert equal `c` but unequal full keys. If a c-only map reports them as
   distinct, the test harness is wrong.
4. **Two-way finite/theta enumeration.** For each q in
   `{3,4,5,6,7,8,12,16,24,32,48}`, enumerate theta keys with
   `c_H≤c_{H,max}` from
   the exact Hejhal conditions, invert each key to its canonical Rosen code,
   replay that code at `λ_q`, and record whether it is q-faithful. Compare
   with an independent matrix BFS keyed by `(c,d mod c)`, not by `|c|`.
   Evaluate in exact number fields (minimal polynomial plus an isolating
   interval); do not use floating equality or any unproved monotone pruning.
5. **Injectivity hunt.** Hash all replayed q-faithful codes by theta key. On
   any bucket of size greater than one, return the shortest pair, both full
   keys, all digits, and the first rewrite state where they diverge. This is
   the direct falsifier of M1-I.
6. **Surjectivity hunt.** Hash all theta keys with `c_H≤c_{H,max}`; subtract the
   image of the q-faithful replay. Emit every missing `(c_H,d_H)` and its theta
   code. A single missing key falsifies the proposed `c_*^H(q)` threshold or M1-S.
7. **Localization hunt.** Enumerate finite q classes beyond the matched
   image, classify the first `R^q`/boundary event, and compare the minimum
   `C_conj=2c_H` and `c_q` of each event type against the proposed first-wrap height
   bound. An unmatched class with no first-wrap event falsifies M1-L.
8. **Adversarial cancellation.** Sweep signed digits with alternating signs,
   long light runs (`a=±1`), near-Chebyshev words, and maximum centered digits.
   Use exact algebraic evaluation at `λ_q`; do not discard words because a
   floating-point `c` is merely small. Any c-zero/near-zero mismatch between
   finite and theta replay is a counterexample to the proposed matched test.
9. **Depth and cutoff saturation.** Repeat all scans at `K=4,8,12,16,20`
   and `c_{H,max}=20,50,100,200`. Require exact stabilization of keys and a
   separate completeness receipt for each `(q,c_{H,max},K)`; the R1 depth-saturation
   check at one q is not a uniform proof (`LAW_R1_COSET_STRUCTURE.md:327-351`).
10. **Source cross-check.** Independently reconstruct the first few Hejhal
    theta representatives from the printed Ch. 11 §3 data and from the
    matrix key. If the two constructions disagree, stop M1 and repair the
    normalization before any RATE calculation.

## 9. Acceptance gate for claiming M1 progress

The only acceptable progression is:

```text
  finite exact receipts
    → NF–Rosen bridge proved (or a named counterexample)
    → M1-W proved
    → M1-I proved
    → M1-S proved for a certified c_*^H(q)
    → M1-L proved with an explicit first-wrap bound
    → only then update the R2 split.
```

Until every arrow is discharged, describe the matched/escaping split as
finite-window evidence and keep the R2 exponent and RATE lemma marked
CONJECTURAL, exactly as required by
`LAW_R2_RATE_LEMMA_DRAFT.md:421-425` and
`RATE_NOTEGRAPH_REFEREE_AUDIT.md:200-212`.

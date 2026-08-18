# Adversarial referee report: the two M2 per-term notes

**Date:** 2026-08-18

**Mode:** read-only source audit apart from this report

**Primary scan read:**
`research_notes/rh_goals_2026-08-14/lane_p/literature/Hejhal_LNM1001_Vol2_ch6s12_pp149-166.pdf`,
all 18 PDF pages / printed pp. 149--166.

**Additional source page read for the claimed Lemma 7.7 constant:** printed
p. 574 in
`research_notes/rh_goals_2026-08-14/lane_p/literature/Hejhal_LNM1001_Vol2_s7_pp568-600.pdf`.

## 0. Verdicts

| note | verdict | controlling reason |
|---|---|---|
| `M2_PERTERM_TRANSCRIPTION_SOL.md` | **CONFIRMED** | The printed inequalities, domains, the provenance of `100`, and the independent `c1,...,c9` replacement chain check. The only wording correction is that the displayed `C6(epsilon)` is an admissible explicit choice for an existential constant, not a source-printed canonical or optimal value. |
| `M2_NATIVE_PERTERM_SOL.md` | **GAPS** | The matrix/continuant per-term theorem, endpoint derivative theorem, divergence counterexample, and Ford correction check. However, the load-bearing assertion that every theta double coset has a unique reduced representative of the Section 1 `Q S^n ... Q` form is not proved by the cited `Z_2 * Z` presentation; without that bridge, `k_w` is not yet proved well-defined for Theorem D. The finite-window scattering statement also omits the domain where `m(s)` is finite / the Dirichlet-series interpretation is valid. Both gaps are repairable and do not refute the formulas. |

These verdicts are deliberately asymmetric: the first note is source-faithful
and carefully limits what is closed; the second contains correct mathematics
but skips one structural proof needed to promote a raw-word depth to a
double-coset statistic.

## 1. Source integrity and page audit

Command and output:

```text
$ shasum -a 256 research_notes/rh_goals_2026-08-14/lane_p/literature/Hejhal_LNM1001_Vol2_ch6s12_pp149-166.pdf
c0dee01cf83e45e5e489e25ea299ccb2ad3654659d284bd9abc031bc6570b62f  research_notes/rh_goals_2026-08-14/lane_p/literature/Hejhal_LNM1001_Vol2_ch6s12_pp149-166.pdf
```

The scan was extracted with `pdftotext -layout` and independently rendered at
200 dpi. The mathematical audit used the rendered pages because the OCR drops
inequality signs, exponents, and Greek letters. Printed pp. 149--153 were read
line by line for Lemmas 12.1--12.2; p. 155 for equation (12.2) and its quadratic
consequence; and pp. 164--166 for Theorem 12.9 and its proof. Printed p. 574 was
read directly for Lemma 7.7.

## 2. `M2_PERTERM_TRANSCRIPTION_SOL.md`: **CONFIRMED**

### 2.1 The source domains are transcribed correctly

The note's lines 211--278 agree with printed pp. 149--153:

* Lemma 12.1: `1/2 <= Re(s) <= 3/2`, `y>0`.
* Lemma 12.2: `s=1/2+h+it`, `0<=h<=1`, `t in R`, `eta>0`.
* The proof first assumes `eta>1`; the final lower-limit shift treats every
  `0<eta<=1`.
* The source states only that `A` is some positive constant and ends with
  `A=c9 exp(-5)`.

Thus the Lemma 12.2 replacement chain has no hidden restriction on `t`; it is
absolute for the whole closed sigma strip and all `eta>0`.

### 2.2 Inequality-by-inequality audit of the replacement `c1,...,c9`

The independent chain at note lines 280--342 is valid. It is not printed by
Hejhal, and the note says so.

| step | source / note locator | referee check |
|---|---|---|
| `c1=e^-1` | printed p. 151; note 283, 286--295 | For `eta>=1`, use `K0(eta)=int_0^infty exp(-eta cosh u)du`, restrict to `0<=u<=1/eta`, and use `cosh u<=1+u^2` on `[0,1]`. Then `eta u^2<=1`, giving `K0(eta)>=e^-1 e^-eta/eta`. |
| `c2=1` | printed p. 151; note 283, 296--301 | `|Gamma(1+it)|^2=2 pi |t| e^(-pi|t|)/(1-e^(-2pi|t|)) >= e^(-pi|t|)` because `1-e^(-2pi|t|)<=2pi|t|`; continuity covers `t=0`. |
| `c3=e^-1` | printed pp. 151--152; note 283, 287 | The Sonine--Gegenbauer lower bound multiplies the preceding two constants, so `c3=c1*c2=e^-1`. |
| `c4=9` | printed p. 152; note 283, 302--303 | On the `eta>1` branch, `T>=1+eta>2`. Lemma 12.1 gives a tail at most `6 int_T^infty e^-y sqrt(y)dy`. Integration by parts bounds this by `6 e^-T sqrt(T)(1+1/(2T))<7.5 e^-T sqrt(T)`, so 9 is safe. |
| `c5=20` | printed p. 152; note 283, 304 | Put `U=eta+|t|+20`, `T=2U`; then `U>21` on the source's `eta>1` branch. This is an explicit admissible replacement for the source's “sufficiently large” `c5`. |
| `c6=1` | printed p. 152; note 283, 304--306, 329--334 | Twice the tail/main ratio is `(2*c4*sqrt(2)/c3) U^(3/2) exp(-(2-pi/2)U)`. It decreases for `U>=21` and is `<0.811` at 21, leaving at least half the main term. The half-main divided by `e^-2U` increases there and is `>71.92` at 21. Hence the remainder is at least `e^-2U`. |
| `c7=4` | printed p. 153; note 283, 306--308 | Cauchy--Schwarz uses `int_eta^T y^(3-2h)dy <= T^4/4` for `eta>1`, `0<=h<=1`; therefore the square of the preceding lower bound gains the factor 4. |
| `c8=1` | printed p. 153; note 283, 307--309 | With `T=2U`, the result is `e^-4U/(4U^4)`. Since `e^U/(4U^4)>1` at `U=21` and increases for `U>4`, this is at least `e^-5U`. |
| `c9=e^-100` | printed p. 153; note 283--284, 309--310 | `e^-5U=e^-100 e^(-5eta-5|t|)`. For `0<eta<=1`, applying the `eta>1` result at lower limit `1+eta` introduces one more `e^-5`, so `A=e^-105`. |

There is no invalid numerical sampling step: the three controlling functions
are monotone on `U>=21`, and the interval calculation checks their endpoint
margins.

### 2.3 Re-run of the Arb receipt

Exact command and output under the required interpreter:

```text
$ /Users/za/.venvs/farey-rh/bin/python -c 'from flint import arb, ctx; ctx.prec=160; pi=arb.pi(); alpha=arb(2)-pi/2; U=arb(21); c3=(-arb(1)).exp(); c4=arb(9); tail=(2*c4*arb(2).sqrt()/c3)*U.sqrt()*U*(-alpha*U).exp(); main=(c3/2)*(alpha*U).exp()/U; poly=U.exp()/(4*U**4); C61=100*(1+arb(2).sqrt()); A=(-arb(105)).exp(); print("alpha =",alpha); print("tail_ratio_U21 =",tail); print("main_over_expminus2U_U21 =",main); print("expU_over_4U4_U21 =",poly); print("C6_epsilon1 =",C61); print("A = exp(-105) =",A)'
alpha = [0.42920367320510338076867830836024855790141530031 +/- 2.51e-48]
tail_ratio_U21 = [0.8109506053764602677306223982496785788301119286 +/- 6.99e-47]
main_over_expminus2U_U21 = [71.92382112914791045775875385987666380836670608 +/- 5.97e-45]
expU_over_4U4_U21 = [1695.3015133653347849018655855138841134756665656 +/- 5.87e-45]
C6_epsilon1 = [241.42135623730950488016887242096980785696718754 +/- 2.75e-45]
A = exp(-105) = [2.5065674758999531731031572443379307585175264602e-46 +/- 2.54e-93]
```

This reproduces note lines 316--327 exactly for the fields used in the proof.

### 2.4 Provenance of `100` and the exact Lemma 7.7 domain

Printed p. 155 gives, with `h=sigma-1/2`,

```text
|phi(s)|^2 B^(-2h) <= B^(2h) + 2h |phi(s)/t|.
```

Solving the positive quadratic after dividing by `B^(2h)` gives

```text
|phi(s)| <= B^(2h) [h/|t| + sqrt(1+h^2/t^2)].
```

Printed p. 574 says verbatim in mathematical effect: repeat that derivation
with `B=10` when `N<infinity`. Therefore, for

```text
epsilon>0,  1/2<=sigma<=3/2,  |t|>=epsilon,  N<infinity,
```

the inequalities `0<=h<=1`, `B^(2h)<=B^2=100`, and
`h/|t|<=epsilon^-1` prove that one may take

```text
C6(epsilon) = 100 [epsilon^-1 + sqrt(1+epsilon^-2)].
```

The factor `100` is exactly `B^2`; it has no provenance in, and no dependence
on, the Lemma 12.2 `c1,...,c9` chain. Note lines 186--207 and 609--622 make
this category distinction correctly.

Two limitations must remain explicit:

1. `C6` is existential in Hejhal. The formula above is a valid explicit
   **choice**, not a recovered printed value and not an optimality claim.
2. The `B=10` sentence covers finite `N`. Printed p. 574 refers the theta
   endpoint to pp. 527 and 508. The target note correctly says that p. 508 was
   not banked and does not promote this derivation to an independently checked
   endpoint constant (`M2_PERTERM_TRANSCRIPTION_SOL.md:617-622`).

### 2.5 Does “CLOSED” overstep?

No, under the note's own carefully limited meaning:

* `M2_PERTERM_TRANSCRIPTION_SOL.md:10-15,713-718` closes one admissible
  finite-`N` Lemma 7.7 constant and one absolute replacement constant for
  Lemma 12.2.
* It does **not** claim that these numbers are source-printed.
* It leaves the Theorem 12.9(c),(d) covering number, low-height estimate,
  divisor clearance, varying geometry, and family uniformity open at
  `:603-607,698-708,713-718`.

The preferred wording is “`C6(epsilon)` **may be taken to be** ...”, but this
is a precision edit, not a mathematical refutation.

## 3. `M2_NATIVE_PERTERM_SOL.md`: **GAPS**

### 3.1 Line-by-line proof audit

| locator | claim | referee result |
|---|---|---|
| `:38-74` | `c_w(lambda)=lambda K_(k-1)(lambda)` and the coefficient derivative bound | **CONFIRMED.** Direct multiplication gives the recurrence. The lower-left entry is in `Z[lambda]` even though other entries can be Laurent. Termwise differentiation and `lambda<=2` give `D_coeff`. |
| `:76-103` | operator-norm derivative bound | **CONFIRMED.** On `[1,2]`, `||Q||<=2`, `||Q'||<=1`, and `||S^n||<=sqrt(n^2+2)<=|n|+1`. The product rule has exactly `k` terms, each with `k-1` undifferentiated `Q` factors. |
| `:108-147` | Theorem A | **CONFIRMED.** Reverse triangle inequality, scalar MVT in `lambda`, and the complex-power MVT give (2.3). The hypothesis `sigma>=-1/2` is exactly what makes `u^(-2sigma-1)` nonincreasing, so its supremum is at `min(x,y)`. Also `2-lambda_N=2(1-cos(pi/N))<=pi^2/N^2`. |
| `:153-165` | arbitrary verified finite pairing | **CONFIRMED AS CONDITIONAL.** It is a finite sum of Theorem A and requires exactly what the note says: distinct, actually verified double-coset terms paired by the same word. |
| `:171-212` | theta height/depth/digit elimination and Corollary A.1 | **CONFIRMED.** The recurrence gives `|H_j|>=(j+1)|H_(j-1)|/j`, hence `|H_j|>=j+1`. From `2n_j H_(j-1)=H_j+H_(j-2)` and monotonicity, `|n_j|<=|H_(k-1)|=y_w/2`. Substitution in `D_mat`, followed by Ford count and `mu>=1`, gives (3.6). |
| `:214-256` | matched/escaping finite scattering comparison | **FORMULA CONFIRMED; DOMAIN GAP.** The triangle inequality and two Ford tails give (3.7)--(3.9) for the intended `sigma>1` RATE region. The theorem as displayed does not state that restriction or exclude poles of `m(s)=sqrt(pi)Gamma(s-1/2)/Gamma(s)`. Restrict it to `sigma>1` (or explicitly to points where the finite expression is defined). |
| `:258-326` | Theorem C endpoint derivative law | **CONFIRMED.** The split-continuant identity, ratio bounds, diagonal-cofactor derivative, and `2/k sum j(k-j)=(k^2-1)/3` yield `|c'_w(2)|/|c_w(2)|<=(k^2+2)/6`. The all-sign-equal Chebyshev words attain equality. The note correctly keeps the interval upgrade (4.5) conjectural. |
| `:328-357` | no geometric denominator growth | **CONFIRMED.** The Chebyshev family has `c(2)=2k` and `c'(2)=(k^3+2k)/3`, disproving geometric growth and attaining Theorem C. |
| `:411-459` | global all-`sigma>1` weighted convergence is false | **CONFIRMED WITH PRECISE SCOPE.** Distinct `c=2k` values imply distinct parabolic double cosets. The subseries is `2^(-2sigma) sum k^(2-2sigma)`, which diverges exactly for `1<sigma<=3/2`. That is enough to refute convergence on every half-plane `sigma>=1+epsilon` when `epsilon<=1/2`; it says nothing adverse about actual convergence for `sigma>3/2`. |
| `:461-513` | corrected Ford weighted bound | **ALGEBRA CONFIRMED; STRUCTURAL GAP at `:463-468`.** If `k_w` is a well-defined canonical theta depth, then `k<=|c|/2` and Ford immediately give (7.1)--(7.4). But the stated presentation does not by itself prove the asserted `Q S^n ... Q` double-coset normal form. |
| `:515-570` | RATE remains open | **CONFIRMED.** Neither the interval derivative comparison, coset pairing, joint depth/denominator count, nor first-wrap localization is proved. The note does not upgrade the finite-window result to the full series. |

### 3.2 The load-bearing normal-form gap

At `M2_NATIVE_PERTERM_SOL.md:463-468`, the inference

```text
theta group = Z_2 * Z
therefore every <S>-double coset has the unique representative of Section 1
```

is not automatic. In the free-product generators `Q,R=QS`, the cusp subgroup
is `<S>=<QR>`, not a free factor. The repo's own structural analysis makes
this explicit in `M1_ROUTE_B_FREEPRODUCT_SOL.md:246-292` and gives a canonical
double-coset word in alternating `R`-powers and `Q`, with endpoint restrictions.
The native note needs a proved bridge from that form to its nonzero `S`-digit
form before `k_w` can be summed as an invariant of double cosets.

There is a clean repair. For a Section 1 theta word, prove its signed bottom
row is

```text
(c,d) = (2 H_r, -H_(r-1)),   H_j=2 n_j H_(j-1)-H_(j-2).
```

Then reverse a nearest-even Euclidean algorithm. The strict inequalities
`|H_(j-2)|<|H_(j-1)|` make the reverse step unique; the possible midpoint tie
would force adjacent `H` values to have the same parity, whereas the recurrence
makes their parities opposite. Prove existence for every admissible theta key
and compatibility with the PSL sign. That would make `k_w` well-defined and
close the present proof gap.

The exact numerical enumeration below strongly corroborates this repair: the
number of Section 1 words at every tested cutoff equals the independent exact
theta double-coset count `sum_(n<=X/2) phi(2n)`. Equality of counts is evidence,
not a substitute for the missing bijection proof.

### 3.3 Re-run of the note's exact diagnostic receipt

The note used a different Python environment. Re-running the same script under
the required interpreter gives identical output:

```text
$ /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from fractions import Fraction
from itertools import product

def sub(p,q):
    z=[0]*max(len(p),len(q))
    for i in range(len(z)):
        z[i]=(p[i] if i<len(p) else 0)-(q[i] if i<len(q) else 0)
    while len(z)>1 and z[-1]==0: z.pop()
    return z
def cpoly(ns):
    km2=[1]
    if not ns: return [0,1]
    km1=[0,ns[0]]
    for n in ns[1:]:
        km2,km1=km1,sub([0]+[n*a for a in km1],km2)
    return [0]+km1
def ev(p,x): return sum(a*x**i for i,a in enumerate(p))
def dev(p,x): return sum(i*a*x**(i-1) for i,a in enumerate(p) if i)

print('k  cheb_c2  cheb_dc2  exhaustive_max_dc_over_k2c2  witness')
for k in range(1,8):
    cheb=cpoly((1,)*(k-1))
    best=Fraction(-1,1); witness=None
    for ns in product((-2,-1,1,2), repeat=k-1):
        p=cpoly(ns)
        ratio=Fraction(abs(dev(p,2)), k*k*abs(ev(p,2)))
        if ratio>best: best,witness=ratio,ns
    print(k, ev(cheb,2), dev(cheb,2), best, witness)
PY
k  cheb_c2  cheb_dc2  exhaustive_max_dc_over_k2c2  witness
1 2 1 1/2 ()
2 4 4 1/4 (-2,)
3 6 11 11/54 (-1, -1)
4 8 24 3/16 (-1, -1, -1)
5 10 45 9/50 (-1, -1, -1, -1)
6 12 76 19/108 (-1, -1, -1, -1, -1)
7 14 119 17/98 (-1, -1, -1, -1, -1, -1)
```

This matches `M2_NATIVE_PERTERM_SOL.md:398-409` exactly.

### 3.4 Derivation of the corrected Ford threshold

Assuming the canonical-depth bridge just identified, (3.3) gives

```text
k_w^2 |c_w|^(-2sigma) <= (1/4)|c_w|^(-2(sigma-1)).
```

Ford's tail with exponent parameter `tau=sigma-1` requires `tau>1`, hence
`sigma>2`, and yields

```text
sum_(|c|>X) k_w^2 |c_w|^(-2sigma)
 <= (1/4) [tau/(tau-1)] X^(2-2tau)
 =  (1/4) [(sigma-1)/(sigma-2)] X^(4-2sigma).
```

This is exactly (7.1). Adding `2 sum |c|^(-2sigma)` and applying the raw Ford
tail gives (7.2). For `1<sigma<2`, Stieltjes summation of the finite window
against `A(X)<=X^2` gives

```text
sum_(0<|c|<=X) k_w^2 |c_w|^(-2sigma)
 <= X^(4-2sigma)/[4(2-sigma)],
```

and at `sigma=2` gives `(1+2 log X)/4`. The constants and threshold in note
lines 470--506 are correct.

Crucially, “Ford proves only `sigma>2`” is a statement about this coarse proof
route. It is not a claim that the actual theta weighted series diverges for
every `sigma<=2`.

### 3.5 Independent numerical test of the weighted theta series

I exhaustively enumerated the Section 1 theta continuants with `|c|<=X`.
Monotonicity of `|H_j|` makes the recursion exhaustive: a word ending below
the cutoff can never have crossed it at an earlier prefix. The `words` count
was checked against the exact coset count `sum_(n<=X/2) phi(2n)`.

Exact command and output:

```text
$ /Users/za/.venvs/farey-rh/bin/python - <<'PY'
def phi(n):
    out=n; p=2
    while p*p<=n:
        if n%p==0:
            while n%p==0: n//=p
            out-=out//p
        p+=1
    if n>1: out-=out//n
    return out

sigmas=(1.25,1.50,1.60,1.75,2.00)
print('X words exact_cosets max_k ' + ' '.join(f'W_{s:.2f}' for s in sigmas))
for X in (256,512,1024,2048,4096):
    M=X//2; stack=[(0,1,1)]; count=0; max_k=0; W=[0.0]*len(sigmas)
    while stack:
        hm,h,k=stack.pop(); count+=1; max_k=max(max_k,k); c=2*abs(h)
        for i,s in enumerate(sigmas): W[i]+=k*k*c**(-2*s)
        nmax=(M+abs(hm))//(2*abs(h))+1
        for n in range(-nmax,nmax+1):
            if n==0: continue
            hn=2*n*h-hm
            if abs(hn)<=M and abs(hn)>abs(h): stack.append((h,hn,k+1))
    exact=sum(phi(2*n) for n in range(1,M+1))
    print(X,count,exact,max_k,*[f'{v:.12f}' for v in W])
PY
X words exact_cosets max_k W_1.25 W_1.50 W_1.60 W_1.75 W_2.00
256 6717 6717 128 10.323822109551 1.610768295439 0.871962118199 0.402371373487 0.154151891820
512 26665 26665 256 15.130137941432 1.861798154759 0.949247461386 0.415613144354 0.154857310571
1024 106517 106517 512 21.854041858293 2.110335818304 1.015884253519 0.424892028409 0.155207178807
2048 425481 425481 1024 31.254322556737 2.356101407385 1.073254608711 0.431381913156 0.155380264519
4096 1701067 1701067 2048 44.430436099646 2.599719184064 1.122764645766 0.435931488147 0.155466076089
```

Interpretation:

* `sigma=1.25`: rapid escape, consistent with the proved power divergence.
* `sigma=1.50`: each doubling adds about `0.25`; this is the expected
  logarithmic divergence and confirms that the FALSE verdict is not merely a
  loose-majorant artifact.
* `sigma=1.60`: dyadic increments shrink
  `0.07729, 0.06664, 0.05737, 0.04951`; this is evidence compatible with
  convergence, not divergence.
* `sigma=1.75`: the values stabilize rapidly (`0.40237` to `0.43593`).
* `sigma=2.00`: strong stabilization (`0.15415` to `0.15547`).

Therefore the analytic and numerical conclusions agree precisely:

```text
PROVED DIVERGENCE: 1 < sigma <= 3/2.
FORD-ONLY GUARANTEE: sigma > 2.
UNRESOLVED BY THE NOTE: 3/2 < sigma <= 2.
NUMERICAL EVIDENCE: compatible with actual convergence throughout that
                    unresolved interval, increasingly clear away from 3/2.
```

The target note itself is mostly careful about this distinction at
`:422-441`. Its headline should never be paraphrased as “the series diverges
for all `1<sigma<=2`.”

## 4. Consistency with each other and with `(RATE)`

There is no mathematical contradiction between the two notes, but there are
three category boundaries that must not be erased.

1. **Different “per-term” objects.**
   `M2_PERTERM_TRANSCRIPTION_SOL.md:609-622` concerns Lemma 7.7's whole
   scattering coefficient `phi_N(s)` and separately Theorem 12.9's Fourier
   modes `phi_m(s)`. `M2_NATIVE_PERTERM_SOL.md:108-147` concerns one
   double-coset Dirichlet term `|c_w|^(-2s)`. None of these constants may be
   substituted for another.

2. **A uniform bound is not a convergence rate.**
   The explicit finite-`N` Lemma 7.7 choice is `O_epsilon(1)` on
   `1/2<=sigma<=3/2`, `|t|>=epsilon`. It does not imply
   `|phi_N-phi_infinity|=O(N^(1-2sigma))` and has no theta-endpoint calculation
   in the banked p. 574 route.

3. **The native scaling is conditional on the missing coset geometry.**
   For `1<sigma<3/2`, the scalar Chebyshev sum
   `sum_(k<N) k^(2-2sigma)` has size `N^(3-2sigma)`; multiplying by
   `2-lambda_N=O(N^-2)` produces the desired formal scale
   `N^(1-2sigma)`. But near elliptic wrap, `mu_w` need not be comparable to the
   theta denominator, the same words need not remain distinct finite double
   cosets, and the interval derivative bound is not proved. The native note
   explicitly preserves these caveats at `:453-459,526-555`.

Ford alone gives an escaping mass of order `N^(2-2sigma)`, one power weaker
than `(RATE)`, and its depth-weighted finite window is of order
`N^(4-2sigma)`, also one power too large before the `N^-2` perturbation factor.
Thus both notes consistently leave the full

```text
|phi_N(s)-phi_infinity(s)| <= C_K N^(1-2sigma)
```

theorem open. The transcription note closes a literal finite-`N` boundedness
constant; the native note closes a conditional wordwise perturbation bound.
Neither closes the coset matching/localization theorem required for `(RATE)`.

## 5. Required corrections before treating both notes as a closed M2 package

1. In `M2_PERTERM_TRANSCRIPTION_SOL.md:10-15,203,614`, replace bare equality
   language by “one may take” if there is any risk that `C6` will be read as a
   canonical or optimal source constant. No mathematical constant changes.
2. In `M2_NATIVE_PERTERM_SOL.md:227-252`, state the `sigma>1` RATE domain (or
   the exact domain excluding poles of `m(s)`) in Theorem B.
3. Before using Theorem D as a theorem about double cosets, insert the
   canonical `Q S^n ... Q` bijection proof sketched in Section 3.2, or cite and
   translate an existing proved theorem that supplies exactly that normal form
   and its depth invariance.
4. Preserve the three-way weighted-series status: divergence through
   `sigma=3/2`, Ford proof only above 2, and no analytic verdict in this note on
   `(3/2,2]`. The fresh computation is evidence for convergence there, not a
   proof.

**Final referee disposition:** transcription note **CONFIRMED**; native note
**GAPS**, with its main analytic formulas confirmed and its remaining defects
localized to a normal-form bridge and a finite-window domain statement.

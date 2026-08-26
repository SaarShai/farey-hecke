# FRONTIER REVIEW — T1 GAP-16 closure ruling

Date: 2026-08-26  
Scope: `T1_GAP16_RIESZ_IMPORT.md`, the GAP-16 ledger entry in
`T1_CRAMER_RAO_DRAFT.md`, the Gaussian predecessor
`Smoothed_Dwf_explicit_formula_VERIFIED.md`, and the harvested Lean file
`projects/aristotle_dispatch_v21/aristotle_dispatch_v21_aristotle/RieszImport.lean`.

## Executive ruling

The local residue calculations are substantially right:

- the order-1 Riesz/Cesàro identity and Mellin kernel are correct;
- the pole at (s=0) contributes (R_0=-2);
- the additional pole at (s=-1) contributes (R_{-1}(N)=12/N);
- every trivial zero (s=-2n) gives a simple, not double, pole, hence no
  (log N) term, and the displayed series for (R_{\mathrm{triv}}) is
  absolutely convergent and (O(N^{-2})).

The proposition is nevertheless **not sound as presently assembled**, and the
named references do not presently close the analytic step in the exact form
consumed. Three defects are load-bearing:

1. Proposition R writes every nontrivial zero as (1/2+i\gamma) but assumes
   only simplicity and a moment bound. It therefore omits RH from its own
   hypotheses. RH is standing in `T1_CRAMER_RAO_DRAFT.md` §1.1, but a
   proposition advertised as the imported analytic formula must state it.
2. The note calls
   \(\sum_{0<\gamma\le T}|\zeta'(\rho)|^{-1}\) by the name
   (J_{-1}(T)) and compares it with (3T/\pi^3). This is not the
   Gonek–Hejhal quantity. Standard notation is
   \[
     J_{-1}(T):=\sum_{0<\gamma\le T}|\zeta'(\rho)|^{-2},
   \]
   and (J_{-1}(T)\sim 3T/\pi^3) is conjectural. The repo's lane-a
   computation also uses the squared reciprocal. The standard conjectural
   bound (J_{-1}(T)=O(T)) is sufficient for the required absolute
   convergence, but a Cauchy–Schwarz step is missing.
3. A shift to \(\Re s=-A\) with (1<A<2) crosses **no** trivial zero.
   The note nevertheless adds the full infinite (R_{\mathrm{triv}}) series
   while identifying (E(N)) with the vertical integral on (Re s=-A).
   Those two assertions cannot both hold. Either the error must be redefined
   by subtracting (R_{\mathrm{triv}}), or an additional shift-to-
   \(-\infty\) argument must be supplied.

Accordingly, citation-level standing is acceptable **in principle** for this
internal gap, but the present text is not yet citation-grade closed. No new
Lean theorem is required for citation-level closure; the analytic statement,
hypotheses, and references must first be repaired exactly as specified below.

## 1. Analytic audit of Proposition R

### 1.1 Finite identity and Mellin kernel

For integer (N\ge2),
\[
 \sum_{n\le N}\mu(n)(1-n/N)
 =\frac1N\sum_{n\le N}\mu(n)(N-n)
 =\frac1N\sum_{0\le k<N}M(k).
\]
The (n=N) term is zero, so the endpoint convention causes no ambiguity.

For \(\Re s>0\),
\[
 M_W(s)=\int_0^1(1-x)x^{s-1}\,dx
       =\frac1s-\frac1{s+1}
       =\frac1{s(s+1)}.
\]
For (c>1), the Dirichlet series for (1/\zeta(s)) is absolutely
convergent and the kernel is (O(|t|^{-2})), so Fubini gives the absolutely
convergent Riesz–Perron integral
\[
 S(N):=\sum_{n\le N}\mu(n)(1-n/N)
   =\frac1{2\pi i}\int_{(c)}\frac{N^s}{s(s+1)\zeta(s)}\,ds.
\]
This step is sound. It is a weighted variant of Perron, not the literal
sharp-cutoff theorem cited from Montgomery–Vaughan.

### 1.2 The (s=0) and (s=-1) residues

At (s=0), (M_W) has residue (1), while
\(\zeta(0)=-1/2\). Hence
\[
 \operatorname*{Res}_{s=0}\frac{N^sM_W(s)}{\zeta(s)}
 =\frac1{\zeta(0)}=-2.
\]
Thus (R_0=-2) survives exactly.

At (s=-1), (M_W) has residue (-1), while
\(\zeta(-1)=-1/12\). Hence
\[
 \operatorname*{Res}_{s=-1}\frac{N^sM_W(s)}{\zeta(s)}
 =N^{-1}\frac{-1}{-1/12}=\frac{12}{N}.
\]
Thus the new (R_{-1}(N)=12/N) term is correct.

The note's broader aside that
\(\operatorname{Res}_{s=0}M_W=W(0)\) for *every* window merely continuous
at zero is stronger than needed and would require a local Mellin hypothesis;
it causes no problem for the explicit window (W(x)=(1-x)_+\).

### 1.3 Nontrivial-zero sum and the Gonek–Hejhal hypothesis

The line-spectrum display
\[
 2\Re\sum_{\gamma>0}
 \frac{N^{1/2+i\gamma}}
 {(1/2+i\gamma)(3/2+i\gamma)\zeta'(1/2+i\gamma)}
\]
requires **RH and simplicity**. Simplicity alone does not put the zeros on
the critical line. Off RH the residue sum must run over all
\(\rho=\beta+i\gamma\), and a moment over critical-line zeros would not
control possible off-line terms.

The note's definition
\[
 \sum_{0<\gamma\le T}\frac1{|\zeta'(\rho)|}=O(T)
\]
is a nonstandard and stronger first-absolute-moment hypothesis. In standard
Gonek–Hejhal notation it is (J_{-1/2}), not (J_{-1}), and the cited
(3/\pi^3) constant does not belong to it. The standard conjectural input is
\[
 J_{-1}(T):=\sum_{0<\gamma\le T}
       \frac1{|\zeta'(1/2+i\gamma)|^2}=O(T).
\]
This is enough. Since (N_\zeta(T)=O(T\log T)), Cauchy–Schwarz gives
\[
 \sum_{0<\gamma\le T}\frac1{|\zeta'(\rho)|}
 \le J_{-1}(T)^{1/2}N_\zeta(T)^{1/2}
 =O(T\sqrt{\log T}).
\]
Consequently, on a dyadic block,
\[
 \sum_{T<\gamma\le2T}
 \frac1{\gamma^2|\zeta'(\rho)|}
 =O\!\left(\frac{\sqrt{\log T}}{T}\right),
\]
and summing over dyadic (T) proves absolute convergence. The tail is
\(O(\sqrt{\log G}/G)\). Thus the intended conclusion is correct after the
definition and proof are repaired.

This hypothesis remains conjectural. Ng states it as the Gonek–Hejhal input,
and current literature records that no full upper bound of this kind is known.
The lane-a measurement is empirical support, not a theorem.

### 1.4 Trivial zeros

At every (s=-2n\), (n\ge1), (M_W) is regular and nonzero, and the
trivial zero of \(\zeta\) is simple. Hence the integrand has a simple pole
with residue
\[
 r_n(N)=\frac{N^{-2n}}
 {(-2n)(1-2n)\zeta'(-2n)}.
\]
There is no double pole and therefore no \(\log N\) term. Formula (2.5) is
correct.

Two supporting sentences in the note are incorrect:

- The functional equation gives
  \[
    \zeta'(-2n)=(-1)^n
      \frac{(2n)!\,\zeta(2n+1)}{2(2\pi)^{2n}},
  \]
  so (1/|\zeta'(-2n)|\) **decays** like
  (2(2\pi)^{2n}/(2n)!\); it does not grow like
  ((2n)!/(2\pi)^{2n}\).
- The leading term is
  \[
    r_1(N)=\frac{N^{-2}}{2\zeta'(-2)}
          =-\frac{2\pi^2}{\zeta(3)}N^{-2},
  \]
  not (N^{-2}/(6\zeta'(-2))\).

With the corrected derivative formula, absolute convergence for (N>1)
and (R_{\mathrm{triv}}(N)=O(N^{-2})) follow immediately. The main
conclusion survives; the stated justification and leading coefficient must
be corrected.

### 1.5 Contour shift and remainder

Fix (1<A<2) and choose (1<c<2). On the line \(\Re s=-A\), the
functional equation and the fact that (1+A>1) give
\[
 \frac1{\zeta(-A+it)}
 =O_A\bigl((1+|t|)^{-A-1/2}\bigr).
\]
Together with
\(M_W(-A+it)=O((1+|t|)^{-2})\), the vertical integral is absolutely
convergent and
\[
 I_{-A}(N):=\frac1{2\pi i}\int_{(-A)}
       \frac{N^sM_W(s)}{\zeta(s)}\,ds
 =O_A(N^{-A}).
\]
This vertical-line estimate is correct.

The horizontal pieces are not justified by the citations currently given.
Titchmarsh Theorem 9.7 supplies a zero-avoiding height with a bound of the
form (1/|\zeta(\sigma+iT)|\ll T^C\), with an unspecified (C), uniformly
only for (-1\le\sigma\le2\). Since the Riesz kernel contributes only
(T^{-2}), this proves horizontal decay only if (C<2), which §9.7 does
not assert. Its §9.8 application succeeds because a Gamma factor supplies
exponential decay; that mechanism is absent here.

Under the standing RH assumption there is a clean repair. Titchmarsh
§14.16 gives, along one height in every unit interval,
\(1/\zeta(\sigma+iT)=O_\varepsilon(T^\varepsilon)\) uniformly for
\(1/2\le\sigma\le2\). The functional equation extends this to the fixed
strip (-A\le\sigma\le1/2\). The horizontal integrals are then
\(O(T^{-2+\varepsilon})\) and tend to zero. Titchmarsh §14.27 demonstrates
the corresponding sequence-of-heights contour mechanism for (M(x)).
Ng's Lemmas 3–4 give a modern, directly readable version under RH.

The finite shift therefore yields
\[
 S(N)=-2+\frac{12}{N}
 +2\Re\sum_{\gamma>0}
   \frac{N^{1/2+i\gamma}}
   {(1/2+i\gamma)(3/2+i\gamma)\zeta'(1/2+i\gamma)}
 +I_{-A}(N),
\]
with (I_{-A}(N)=O_A(N^{-A})\). It crosses no trivial zero.

To retain the exact T1 observable with an explicit full
(R_{\mathrm{triv}}), the minimal repair is to **define**
\[
 E_A(N):=I_{-A}(N)-R_{\mathrm{triv}}(N).
\]
Since (R_{\mathrm{triv}}(N)=O(N^{-2})\) and (A<2), this still gives
\(E_A(N)=O_A(N^{-A})\), and then
\[
 S(N)=-2+\frac{12}{N}+\text{zero sum}
      +R_{\mathrm{triv}}(N)+E_A(N)
\]
is correct. Alternatively, one may supply a separate shift-to-
\(-\infty\) argument, in the style of Titchmarsh §14.27, that actually
crosses and sums all trivial zeros. The present note does neither and instead
calls (I_{-A}) itself (E_A); that is the assembly defect.

The numerical section also says the residual is monotone in (K) at all
three (N), but its own (N=20000) row increases from
(3.82\times10^{-2}) at (K=25) to (3.94\times10^{-2}) at (K=50).
This is non-load-bearing but should be corrected.

## 2. Lean-core coverage

The harvested file contains exactly eight theorems. It is sorry-free. I
re-elaborated it against Lean 4.28.0 / mathlib v4.28.0 using another complete
repo environment with the same toolchain, because the harvested project's own
`.lake/packages/mathlib` checkout is incomplete and its local `lake env lean`
stops in `git` before Lean starts. Re-elaboration returned exit code 0, with
only the expected warning that `hn` is unused in `Rtriv_summand_eq`.

An explicit `#print axioms` pass reports only
`propext`, `Classical.choice`, and `Quot.sound` for every theorem. A scan for
`sorry`, `admit`, and local `axiom` is clean.

| Lean theorem | Prop. R step | What it actually proves | Boundary of coverage |
|---|---|---|---|
| `riesz_cesaro_identity` | (2.2), unnormalised finite rearrangement | The exact finite identity for an arbitrary real sequence (a) | Does not define or instantiate the Möbius function or Mertens function |
| `riesz_weight_eq` | (2.2), normalised Riesz/Cesàro identity | The (1/N)-normalised finite identity for (N>0) | Same instantiation boundary; no analytic content |
| `mellin_riesz_k1` | (2.1) | The real-variable integral for real (s>0) | No complex Mellin inversion, meromorphic continuation, or contour integral |
| `MW_residue_zero` | Algebra preceding the (s=0) residue | The field identity (sM_W(s)=1/(s+1)) away from both poles | Does not state `Complex.residue`, meromorphicity, or the limiting value at the pole |
| `MW_residue_negOne` | Algebra preceding the (s=-1) residue | The field identity ((s+1)M_W(s)=1/s) away from both poles | Same analytic boundary |
| `R0_eq_neg_two` | (R_0=-2) scalar arithmetic | (1/z_0=-2), assuming (z_0=-1/2) | Does not prove (zeta(0)=-1/2) or connect this quotient to a complex residue |
| `Rneg1_eq_twelve_div` | (R_{-1}=12/N) scalar arithmetic | ((-1)N^{-1}/z_{-1}=12/N), assuming (z_{-1}=-1/12) and (N\ne0) | Does not prove (zeta(-1)=-1/12), the (N^s) residue rule, or positivity/integrality of (N) |
| `Rtriv_summand_eq` | Algebra in (2.5) | (M_W(-2n)=1/[(-2n)(1-2n)]) | Does **not** mention (N^{-2n}), (zeta'(-2n)), simplicity of the trivial zero, a complex residue, absence of a log term, convergence, or the (O(N^{-2})) sum bound |

Thus the Lean core covers the finite rearrangements, the real Mellin integral,
and the intended scalar field arithmetic. It does **not** cover:

- the complex Riesz–Perron representation or Fubini step;
- meromorphic continuation of (M_W) or any `Complex.residue` computation;
- the zeta values at (0) and (-1), or simplicity of the trivial zeros;
- RH, simplicity of nontrivial zeros, or the identification of their residues;
- absolute convergence of the nontrivial-zero or trivial-zero sums;
- the zero-avoiding height sequence, horizontal contour limits, vertical-line
  estimate, or (O_A(N^{-A})) remainder;
- the assembly of Proposition R.

The docstrings call the collection “six theorems” because several items are
grouped, but there are eight theorem declarations. More importantly, the
docstring for `Rtriv_summand_eq` describes a simple-pole residue and “no
log (N)”; the formal theorem proves only the evaluation of (M_W(-2n)).
The broader prose must not be presented as machine-verified.

## 3. Citation audit

### Hardy–Riesz

The citation “Hardy–Riesz, Ch. V (Riesz means and their summation formulae)”
is bibliographically inaccurate. In the 1915 book:

- Ch. III treats formulae for sums of Dirichlet coefficients;
- Ch. IV defines typical/Riesz means and identifies the arithmetic order-1
  case with Cesàro;
- Ch. V is *General arithmetic theorems concerning typical means*;
- Ch. VII §2, p. 50 (“Generalisation of Theorem 13”) is the closer
  Riesz/Perron integral result.

These chapters support the general Riesz-mean framework, not the zeta-zero
contour shift, the Gonek–Hejhal hypothesis, the infinite residue sums, or the
claimed (O_A) remainder. An even closer generic kernel reference is Hardy–
Littlewood, Acta Math. 41 (1916), §2.25x, pp. 140–141: its order-
(delta) Riesz formula has kernel
\(\Gamma(\delta+1)/[s(s+1)\cdots(s+\delta)]\), which at (delta=1)
is exactly (1/[s(s+1)]\). It is still a generic kernel formula, not
Proposition R for (1/\zeta\).

### Montgomery–Vaughan §5.1

Theorem 5.1 is the sharp-cutoff Perron formula with kernel (x^s/s), a
vertical-limit interpretation, and half weight at an integral endpoint;
Theorem 5.2 is its truncated form. It does not state the triangular-weight
identity with (1/[s(s+1)]), nor any zeta contour shift. The consumed formula
is an elementary absolutely convergent variant and is acceptable if the note
explicitly proves the scalar inverse-Mellin identity and Fubini step, rather
than saying the cited theorem is literally the same form.

### Titchmarsh §§3.7 and 9.7

Section 3.7 is a particular Mellin/contour argument in the proof of the prime
number theorem, not a general theorem giving Proposition R. Titchmarsh's
Perron lemma is elsewhere (§3.19 in this edition).

Section 9.7 supplies only the unspecified-polynomial zero-avoiding lower
bound described in §1.5 above. Section 9.8 uses it with a Gamma kernel and
also warns that its zero series is obtained with a prescribed bracketing;
ordinary convergence is not thereby proved. These sections do not deliver
the absolutely convergent order-1 Riesz formula consumed here.

Because T1 already assumes RH, the appropriate contour citation is
Titchmarsh §14.16 (the (T^\varepsilon) zero-avoiding sequence under RH),
with §14.27 (the explicit Mertens contour) as the model calculation. Ng 2004,
Lemmas 3–4, makes precisely this RH-dependent route explicit. The vertical
line (Re s=-A<-1) must still be handled by the functional equation as in
§1.5; it is not inside the strip of §9.7.

### Gonek–Hejhal status

Ng defines
\(J_{-k}(T)=\sum|\zeta'(\rho)|^{-2k}\), records the Gonek–Hejhal
conjecture, and states (J_{-1}(T)\sim3T/\pi^3\) and the upper bound
(J_{-1}(T)\ll T\) as conjectural inputs. This is the form the note must use.
The first reciprocal moment currently written in Prop. R is a different
quantity.

Primary-source links checked:

- [Hardy–Riesz, *The General Theory of Dirichlet's Series* (1915)](https://archive.org/download/cu31924060184441/cu31924060184441.pdf)
- [Hardy–Littlewood, Acta Math. 41 (1916), DOI](https://doi.org/10.1007/BF02422942)
- [Montgomery–Vaughan, *Multiplicative Number Theory I*](https://ndl.ethernet.edu.et/bitstream/123456789/23715/1/Hugh%20L.%20Montgomery.pdf)
- [Titchmarsh, *The Theory of the Riemann Zeta-Function*, 2nd ed.](https://sites.math.rutgers.edu/~zeilberg/EM18/TitchmarshZeta.pdf)
- [Ng, *The distribution of the summatory function of the Möbius function*](https://www.cs.uleth.ca/~nathanng/RESEARCH/mobius2b.pdf)
- [Bui–Florea–Milinovich, 2024, on negative moments](https://londmathsoc.onlinelibrary.wiley.com/doi/10.1112/blms.13092)

## 4. Closure condition and mandatory disclosure

Citation-level closure is acceptable after all of the following are on disk:

1. Add RH explicitly to Proposition R.
2. Replace the nonstandard first-moment definition by
   \(J_{-1}(T)=\sum|\zeta'(\rho)|^{-2}=O(T)\), label it
   **conjectural**, and insert the Cauchy–Schwarz/dyadic convergence argument.
   The same notation error is repeated in `G1_MODEL_SPEC.md` and must be
   corrected there so the model authority and Prop. R agree.
3. Replace the current Hardy–Riesz/Titchmarsh section claims with exact
   theorem/page citations: a direct order-1 Riesz kernel source, and the
   RH-dependent (T^\varepsilon) height sequence (§14.16/§14.27 or Ng
   Lemmas 3–4). Do not claim §9.7 alone kills the horizontal sides.
4. Reconcile (R_{\mathrm{triv}}) with the (1<A<2) shift, minimally by
   defining (E_A=I_{-A}-R_{\mathrm{triv}}), or else provide the separate
   shift-to-(-\infty) proof.
5. Correct the reciprocal-(\zeta'(-2n)) asymptotic, the leading
   (R_{\mathrm{triv}}) coefficient, and the numerical monotonicity sentence.
6. Insert the following sentence verbatim wherever GAP-16 is marked closed
   and at the first use of Proposition R in T1:

> **Mandatory disclosure.** Proposition R is conditional on RH, simplicity of every nontrivial zero, and the conjectural Gonek–Hejhal bound (J_{-1}(T):=\sum_{0<\gamma\le T}|\zeta'(\tfrac12+i\gamma)|^{-2}=O(T)). Lean checks only the eight finite/algebraic lemmas in `RieszImport.lean`; the Riesz–Perron inversion, meromorphic residue calculus, absolute convergence of the zero and trivial-zero sums, the RH zero-avoiding contour shift, and the (O_A(N^{-A})) remainder remain cited classical analysis and are not formalized in Lean.

Until items 1–5 are applied, the finite Lean half is closed but the analytic
GAP-16 proposition remains **FRONTIER-CITATION**. Once they are applied, GAP-16
may be marked **CLOSED AT CITATION+LEAN STANDING**, carrying the mandatory
disclosure above; a full Lean formalization of the contour engine is not owed
by that standard.

RULING: KEEP-OPEN

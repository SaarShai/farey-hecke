# General resonance escape: adversarial referee

Date: 2026-08-19
Candidate: `LAW_GENERAL_RESONANCE_ESCAPE_SCOUT.md` at commit
`9ed72df6316ed4adb6ab3de0042970e8015af1d1`
Referee verdict: **GAPS / NOT REFUTED**
Scope judged: scalar scattering poles for the one-cusp Hecke orbifolds
$G_q\backslash\mathbb H$, every finite integer $q\geq3$.

## Executive verdict

The candidate's theorem is **NOT REFUTED**, but its
**CONFIRMED-APPLICABLE** status must not be banked.

The load-bearing defect is exact and narrow.  The candidate does not inspect
Selberg's actual formula or the subscript on the count it uses from p. 42; it
uses a Google Books search fragment whose OCR omits that information.  Its
purported independent check, Bonthonneau (8), is printed with a sign that is
inconsistent with Bonthonneau's own definition of the resonance set.  The
clean modern weighted-zero theorem in Kelmer has precisely the required
$T\log T$ main term, but Kelmer globally assumes a torsion-free lattice.
Hecke triangle groups have elliptic torsion.  Therefore Kelmer's theorem cannot
be cited verbatim for $G_q$.

There is a promising, short repair: specialize Kelmer's analytic proof to the
orbifold scattering determinant using the general cofinite-orbifold
Dirichlet-series and functional-equation inputs recorded by
Friedman--Jorgenson--Smajlovic/Venkov and the Hejhal vertical-strip bound.
That specialization is a new proof bridge, however, not a hypothesis-free
quotation.  It must be written as its own solution and cold-refereed before an
all-$q$ promotion.

The exact state supported by the sources inspected here is:

1. **CONFIRMED:** the Kelmer weighted zero theorem, and hence infinitely many
   nonreal strict-left scattering-determinant poles, for finite-volume
   torsion-free hyperbolic surfaces with a cusp.
2. **CONFIRMED:** $q=3$ separately, from the explicit modular scattering
   determinant (Kelmer's remark identifies its poles with zeros of
   $\zeta(1-2s)$).
3. **CONJECTURAL / NOT REFUTED:** the same conclusion for each elliptic Hecke
   orbifold $q\geq4$, including the arithmetic cases $q=4,6$, until the
   orbifold transfer above or Selberg's actual all-elliptic theorem is supplied.

This is not a request for an effective first pole.  If the qualitative
all-$q$ pole theorem is repaired, it is already sufficient for the user's
accepted scattering-resonance LAW target.  No Selberg-zeta normalization
bridge is required at that scope.

## 1. Provenance and isolation

The referee branch was based exactly on the candidate commit and was clean
before this report was created:

~~~text
$ git rev-parse HEAD
9ed72df6316ed4adb6ab3de0042970e8015af1d1
$ git status --short --branch
## codex/law-general-resonance-referee-20260819
~~~

The candidate itself labels the result `CONFIRMED-APPLICABLE`, calls Selberg a
"searchable primary-source preview", acknowledges that the p. 42 OCR suppresses
part of the subscript, and calls Bonthonneau a "legible independent check":

~~~text
$ rg -n 'CONFIRMED-APPLICABLE|searchable primary-source preview|OCR suppresses|legible$|independent check|paper treats smooth' \
    research_notes/rh_goals_2026-08-14/lane_g/LAW_GENERAL_RESONANCE_ESCAPE_SCOUT.md
5:Verdict: **CONFIRMED-APPLICABLE**, at the qualitative scattering-pole scope below.
39:The searchable primary-source preview gives the following page locations.
52:   \(T\log T\).” The preview OCR suppresses part of the subscript, so this
241:it is not an inference from the total Weyl law (3). This is the legible
242:independent check on the OCR-damaged Selberg p. 42 hit.
244:The paper treats smooth cusp surfaces, so it is not being used to silently
~~~

The line-oriented output demonstrates both that the report itself admits the
OCR loss and that its purported independent check is Bonthonneau's
smooth-surface formula.  A search snippet is not an inspection of the primary
formula.

## 2. Selberg: the candidate did not pin the counted object

The candidate's p. 15 Google Books receipt supports only a general finite-area
setup and a one-dimensional character.  Its p. 42 receipt contains only the
phrase “at least of the order” and the mangled expression $T\log T$; the
formula, the definition of the counting function, the half-plane, weights,
multiplicities, and hypotheses are absent.  There is no actual-page receipt for
the asserted p. 17 reflection statement.

Those omissions matter.  A total resonance count, a combined eigenvalue/pole
count, a scattering-phase count, and a right-half-plane zero count have
different logical consequences.  Only the last, or an equivalently signed
weighted strict-left pole sum, yields the candidate's conclusion without an
additional argument.

The independent Venkov primary source does verify that the surrounding
spectral/scattering framework allows elliptic elements: it treats an arbitrary
Fuchsian group of the first kind and arbitrary one-dimensional unitary
character, explicitly includes elliptic conjugacy classes, and states that the
scattering determinant is meromorphic.  But the theorem visible there is only
an $O(r^2)$ upper bound on poles, not an infinitude theorem.  Thus Venkov
repairs the *setup*, not the missing lower bound.

Receipt (official MathNet English PDF, pp. 131--134 in the printed survey):

~~~text
$ shasum -a 256 /private/tmp/lawref-venkov1979.pdf
1763de67c86a76eeaba6b7552e6a796ce32281a6ef9a3fc122e47231d6b49be0  /private/tmp/lawref-venkov1979.pdf
$ pdftotext -layout /private/tmp/lawref-venkov1979.pdf /private/tmp/lawref-venkov1979.txt
$ rg -n 'arbitrary Fuchsian group|elliptic elements|LEMMA 10.3' /private/tmp/lawref-venkov1979.txt | tail -n 8
2499: function Z r ( s ; χ) for an arbitrary Fuchsian group of the first kind Γ and any
2555:   LEMMA 10.3. The number of poles of<p(s; χ ) in the half-plane
2576:same points of multiplicities depending on the orders of the elliptic classes
~~~

Primary URL: https://www.mathnet.ru/eng/rm7178

### Exact Selberg repair

Either of these would close this source gap:

1. inspect Selberg's actual pp. 15, 17, and 42 and quote the complete theorem,
   definitions, and hypotheses showing that the $T\log T$ object is the
   right-half-plane zero count of $\phi(s,\chi_0)$ for an arbitrary cofinite
   Fuchsian group with elliptic elements; or
2. give the orbifold-specialized Kelmer proof listed in section 8 below.

The current Google Books snippets do neither.

## 3. Bonthonneau equations (3), (5), and (8)

The official published PDF was inspected both as text and as a rendered page:

~~~text
$ shasum -a 256 /private/tmp/law-general-resonance.x2RNPo/bonthonneau2016.pdf
54d6c7412399a8774e3b649deb2e249fc23bf19fef055c9ae4d147169e5ce568  /private/tmp/law-general-resonance.x2RNPo/bonthonneau2016.pdf
$ pdftoppm -f 3 -l 3 -png -r 180 -singlefile \
    /private/tmp/law-general-resonance.x2RNPo/bonthonneau2016.pdf \
    /private/tmp/lawref-bonth-render/p139
$ shasum -a 256 /private/tmp/lawref-bonth-render/p139.png
7ff6c25841a8eb984b404a4438933b457ab2590c5b73c42c55c2a9a6a52f7c51  /private/tmp/lawref-bonth-render/p139.png
~~~

Primary URL: https://ems.press/content/serial-article-files/33566

### Equation (3): total resonances

Equation (3) is a Weyl law for $N_{\mathcal R}(T)$, the total resonance set.
It has a leading $T^2$ term, a $-T\log T$ cusp correction, linear terms,
and $O(T/\log T)$.  Bonthonneau's later definition gives


\[
  N_{\mathcal R}(T)=2N_d(T)+N_\Lambda(T),
\]

where $N_d$ is the discrete $L^2$ count and $N_\Lambda$ is the
scattering-pole count.  Consequently (3) alone permits the leading term to be
carried by $L^2$ eigenvalues.  It cannot prove $N_\Lambda(T)\to\infty$.

### Equation (5): eigenvalues plus scattering phase

Equation (5) is

\[
  2\pi N_d(T)+S(T)
   ={\operatorname{vol}(M)\over2}T^2-2\kappa T\log T+O(T).
\]

It binds the discrete count to the scattering phase; it is not a positive
pole-count identity.  Eigenvalues, phase variation, and cancellations can
supply its leading terms.  It therefore does not repair (3).

Text-extraction receipt for the roles of (3) and (5):

~~~text
$ pdftotext -layout /private/tmp/law-general-resonance.x2RNPo/bonthonneau2016.pdf - | \
    rg -n 'NR .T / D|2.Nd|set of poles of|union of this set' | cat -v
57:   NR .T / D          T          T log.T / C             T CO          :           (3)
62:                        NR .T / D         T C o.T 2 /;
66:                       NR .T / D          T C O.T 3=2C^O /:                         (4)
71:               2^YNd .T / C S.T / D            T        2^TT ln T C O.T /;           (5)
82:                          NR .T / D           T C O.T 3=2 /:                       (7)
164:    The set of poles of ' , ^^ and .Ej /j D1:::^T is the same, we call them them scatter-
166:The union of this set with the set of s 2 C such that s.1 s/ is an L2 eigenvalue, is
~~~

### Equation (8): a printed sign inconsistency

The published p. 139 literally prints

\[
 \sum_{s\in\mathcal R,\ 0\leq\Im s\leq T}
      (\Re s-\tfrac12)
 = {\kappa\over4\pi}T\log(T/\pi)
   -{1\over2\pi}\bigl({\kappa\over2}+\log|c|\bigr)T
   +O(\log T).
\]

But p. 137 defines

\[
  \mathcal R\subset\{\Re s\leq\tfrac12\}\cup(\tfrac12,1].
\]

For all nonreal strict-left scattering resonances the displayed weight
$\Re s-1/2$ is negative.  Critical-line spectral parameters have weight zero.
The right-real interval contains only finitely many exceptional spectral
parameters.  Thus the printed left side cannot tend to positive
$+\kappa T\log T/(4\pi)$.  The intended weight is very likely
$1/2-\Re s$, or an unprinted reflected/right-zero convention is missing, but
the candidate may not silently choose either repair.

The published equation is therefore not an independent confirmation of the
candidate's sign and counted object.  No corrigendum resolving it was located
in the bounded search.  This does not refute Selberg's theorem; it refutes the
candidate's use of Bonthonneau (8) as a literal proof receipt.

## 4. Kelmer: decisive theorem, wrong quoted scope for the Hecke orbifold

Kelmer's Theorem 3 is unambiguous.  If the right-half-plane zeros of the
scattering determinant are $\rho=\beta+i\gamma$, it gives

\[
 \sum_{|\gamma|<T,\ \beta>(d-1)/2}
 \left(\beta-{d-1\over2}\right)
 ={\kappa(d-1)\over2\pi}T\log T+A_\Gamma T+O(\log T).
\]

For $d=2$ and one cusp this is the exact positive weighted law needed.
Critical-line points are absent from the sum, $L^2$ eigenvalue counts do not
appear, and finitely many real exceptions cannot supply a growing
$T\log T$ term.  The functional equation reflects each nonreal right zero to
a nonreal strict-left pole.

However, Kelmer's global setup explicitly says the lattice is torsion-free.
The theorem is not stated for orbifolds with elliptic points.

Primary source and source-code receipts:

~~~text
$ shasum -a 256 /private/tmp/law-general-resonance.x2RNPo/kelmer2015.pdf \
    /private/tmp/lawref-kelmer-srcdir/main.tex
c15fb0c4d1d72cc1e09ee6c70532e27d835afd8a8e01a23668cdb6049f8d5030  /private/tmp/law-general-resonance.x2RNPo/kelmer2015.pdf
951a533051f11acf983457504da67f0ca31d2a99e06ffdfb1377defe3267d02e  /private/tmp/lawref-kelmer-srcdir/main.tex
$ rg -n 'torsion free lattice|begin\{thm\}\\label\{t:ZeroDist1\}|kappa\(d-1\).*T\\log|satisfies all the assumptions' \
    /private/tmp/lawref-kelmer-srcdir/main.tex
194:Any finite volume hyperbolic manifold is of the form $X_\G=\G\bs \Hd$ where $\G<G$ is a torsion free lattice.
237:\begin{thm}\label{t:ZeroDist1}
242:\mathop{\sum_{|\gamma|<T}}_{\beta>\tfrac{d-1}{2}}(\beta-\tfrac{d-1}{2})=\frac{\kappa(d-1)}{2\pi} T\log(T)+A_\Gamma T+ O(\log(T))
724:... $L^*(s)$ satisfies all the assumptions needed for \cite[Lemma 1,2]{Selberg90} ...
~~~

Primary URL: https://arxiv.org/abs/1402.4780

Kelmer's proof, source lines 567--747, is analytic after the scattering
determinant has been normalized to a Dirichlet series $L^*(s)$.  That is why
an orbifold transfer looks viable.  Viability is not the same as an already
cited theorem.

## 5. The Hecke groups and the torsion loophole

The Hejhal scan directly fixes the family:

\[
 G_q=\langle E,S^{\lambda_q}\rangle,\qquad
 \lambda_q=2\cos(\pi/q),\qquad q\geq3,
\]

with the standard finite-area fundamental region, the relation
$(ES^{\lambda_q})^q=I$, the cusp at infinity, and the trivial scalar
character throughout the section.  Its scalar constant term is
$y^s+\phi_q(s)y^{1-s}$.  Hence:

- every finite $q\geq3$ is cofinite and noncompact;
- there is one scalar cusp channel, so $\det\Phi_q=\phi_q$;
- the elliptic relation is present for every finite $q$, including
  $q=3,4,6$.

Receipt:

~~~text
$ shasum -a 256 \
    research_notes/rh_goals_2026-08-14/lane_p/literature/Hejhal_LNM1001_Vol2_s7_pp568-600.pdf
b0f9a7001b10f5e0eae5e5aca85124c0a233256aa0e08b5c0f04720185a2b1e9  research_notes/rh_goals_2026-08-14/lane_p/literature/Hejhal_LNM1001_Vol2_s7_pp568-600.pdf
$ pdfinfo research_notes/rh_goals_2026-08-14/lane_p/literature/Hejhal_LNM1001_Vol2_s7_pp568-600.pdf | rg '^Pages'
Pages:           33
~~~

Primary DOI: https://doi.org/10.1007/BFb0061302

Hejhal's Theorem 7.11 and Corollary 7.12 only assert zeros/poles in the chosen
near-line region when $q$ is sufficiently large.  They do not quantify a
single onset valid for all finite $q$, and they do not prove the claim for
each fixed small $q$.

Arithmeticity does not erase elliptic torsion.  Consequently $q=4$ and
$q=6$ remain inside the same scope gap unless their explicit scalar
determinants are separately supplied.  The case $q=3$ is exceptional only
because the modular determinant is explicit: Kelmer records that its poles
occur at zeros of $\zeta(1-2s)$, which independently gives infinitely many
nonreal strict-left poles.

Passing to a finite-index torsion-free subgroup is not a repair.  The cover's
scattering determinant factors into contributions from representations of the
orbifold group; an infinity of cover poles need not lie in the trivial scalar
factor.  No source inspected supplies that missing implication.

## 6. What the modern orbifold source does and does not prove

Friedman--Jorgenson--Smajlovic explicitly work with a finite-volume,
noncompact orbifold, include elliptic conjugacy classes and their orders, and
allow a finite-dimensional unitary representation.  They state:

- $\phi(s)=\det\Phi(s)$ is meromorphic of order at most two;
- it is holomorphic in $\Re s>1/2$ except for finitely many poles;
- $\phi(s)\phi(1-s)=1$;
- for $\Re s>1$, $\phi$ is a gamma quotient times a generalized Dirichlet
  series with nonzero first coefficient;
- nonreal right zeros and strict-left poles occur in reflected pairs.

These are exactly the orbifold analytic prerequisites one would want for the
Kelmer/Selberg argument.  The paper does **not** state the $T\log T$
weighted-zero asymptotic or explicitly conclude that the nonreal sequence is
infinite.  It therefore supports the repair but is not by itself the missing
lower bound.

Receipt from the official arXiv source:

~~~text
$ shasum -a 256 /private/tmp/lawref-superzeta.tex
f067abad694e066ac5bd524f4c6e98d3b00c94fddc0ccaa40cc216b4bc25cc37  /private/tmp/lawref-superzeta.tex
$ rg -n 'finite volume, non-compact orbifold|elliptic classes|phi\(s\).*meromorphic of order|Thm.~3.5|Poles of the form|Zeros of the form' \
    /private/tmp/lawref-superzeta.tex
226:finite volume, non-compact orbifold quotient space.  Let $\chi$ be finite-dimensional unitary representation of $\Gamma$.
277:of $M$ and by $\{R\}_{\Gamma}$ the set of inequivalent elliptic classes of elements of $\Gamma$.
351:The function $\phi(s)$ is meromorphic of order at most two. Furthermore, $\phi(s)$ is holomorphic for $\Re(s) > \frac{1}{2}$, except for a finite number of poles, and it satisfies the functional equation
360:\begin{thm}  (\cite[Thm.~3.5 p. 59]{Venkov83}) For $\Re(s)> 1$ we have that
397:\item Poles of the form $1-\rho$ and $1-\overline{\rho}$ ...
398:\item Zeros of the form $\rho$ and $\overline{\rho}$ ...
~~~

Primary URL: https://arxiv.org/abs/2011.12795

## 7. Object and cancellation audit

### Scalar pole versus determinant pole

For a one-cusp trivial-character Hecke orbifold, the scattering matrix is
$1\times1$.  Thus a pole of the scalar coefficient $\phi_q$, a pole of
$\det\Phi_q$, and a pole of the scattering matrix are the same meromorphic
event with the same order.  The matrix/determinant distinction creates no gap
*after* one-cusp scalarity is fixed.

### Zero versus pole

The functional equation $\phi_q(s)\phi_q(1-s)=1$ sends a zero
$\rho$ with $\Re\rho>1/2$ to a pole $1-\rho$ with strict
$\Re(1-\rho)<1/2$, preserving nonreality and order.  In the scalar case there
is no determinant cancellation between channels.

### Critical-line and $L^2$ data

Critical-line points cannot supply Kelmer's weighted right-zero sum because
the sum is restricted to $\beta>1/2$.  Embedded $L^2$ eigenvalues appear in
Bonthonneau's total and phase laws but not in Kelmer's right-zero law.  This is
why Kelmer's theorem is decisive and Bonthonneau (3)/(5) are not.

### Real exceptions and multiplicity

The orbifold divisor source lists only finitely many real zeros/poles off the
critical line.  Therefore a positive $T\log T$ weighted right-zero law cannot
be furnished by real exceptional points or by one point of fixed finite
multiplicity.  It forces infinitely many nonreal right zeros counted with
multiplicity, and functional reflection forces infinitely many nonreal
strict-left poles.

### Selberg-zeta divisors

The user accepts a scattering resonance as the LAW target.  This referee does
not impose a separate Selberg-zeta divisor normalization.  If a later document
restates the result as a zero of a project-specific normalized $Z_q$, the
elliptic/parabolic factor convention must still be checked separately.

## 8. Exact repair theorem to write and re-referee

The smallest self-contained repair is a $d=2$, one-cusp orbifold version of
Kelmer's Proposition `p:L*`, Lemma `l:intL*half`, and lines 722--747.
It must check, rather than merely assert, the following.

1. From Hejhal p. 569, fix $G_q$, its single cusp, trivial scalar character,
   and $\kappa=1$, uniformly for every finite $q\geq3$.
2. From the orbifold Venkov/Friedman--Jorgenson--Smajlovic theorem, normalize

   \[
     \phi_q(s)=
     \sqrt\pi\,{\Gamma(s-1/2)\over\Gamma(s)}
     a_q b_q^{-2s}L_q^*(s),
     \qquad L_q^*(s)=1+\sum_{n\geq1}a_{q,n}\lambda_{q,n}^{-s}.
   \]
3. Prove that $L_q^*$ is meromorphic in $\Re s\geq1/2$ with only finitely
   many right-half-plane poles, tends exponentially to $1$ as
   $\Re s\to+\infty$, and has the polynomial vertical bound required by
   Selberg's two complex-analysis lemmas.  Pin the Hejhal/Maass--Selberg bound
   to the elliptic-orbifold setup explicitly.
4. Use $|\phi_q(1/2+it)|=1$ to compute the critical-line modulus of $L_q^*$
   and replay the triangular log integral.  For $\kappa=1,d=2$, obtain

   \[
     \sum_{|\gamma|<T,\ \beta>1/2}(\beta-1/2)
       ={1\over2\pi}T\log T+A_qT+O_q(\log T).
   \]
5. Prove that the real off-line divisor is finite, then invoke
   $\phi_q(s)\phi_q(1-s)=1$ to obtain infinitely many nonreal poles in
   $\Re s<1/2$.
6. Send that proof to a new cold referee.  Do not cite the printed sign in
   Bonthonneau (8).

Until all six checks are present, the all-finite-$q$ statement is
**CONJECTURAL / NOT REFUTED**.

## 9. Counterexample and blast-radius audit

No counterexample was found among cofinite constant-curvature Fuchsian
orbifolds.  The search did find the standard warning that total Weyl laws mix
discrete and scattering data.  Müller's smooth-surface theorem, for example,
uses a combined eigenvalue/pole count and assumes torsion-free geometry; it
does not yield an all-orbifold strict-left scalar-pole lower bound.

The apparent Bonthonneau sign contradiction is not a counterexample to the
target theorem.  It is a source-printing/convention defect that invalidates one
purported receipt.

If the candidate's status were banked unchanged, every downstream claim that
uses “all finite $q$” qualitative scattering-pole existence would inherit an
unrefereed orbifold transfer.  Claims restricted to $q=3$, torsion-free
surfaces, or Hejhal's ineffective sufficiently-large-$q$ family are not hit.

## 10. Source ledger

Primary sources inspected:

- Atle Selberg, *Remarks on the distribution of poles of Eisenstein series*:
  candidate's Google Books search snippets only; actual decisive pages were
  not available for this referee inspection.
- D. Kelmer, *On distribution of poles of Eisenstein series and the length
  spectrum of hyperbolic manifolds*: https://arxiv.org/abs/1402.4780
- Y. Bonthonneau, *A note on the resonance counting function for surfaces
  with cusps*: https://ems.press/content/serial-article-files/33566
- A. B. Venkov, *Spectral theory of automorphic functions, the Selberg
  zeta-function, and some problems...*:
  https://www.mathnet.ru/eng/rm7178
- J. S. Friedman, J. Jorgenson, L. Smajlovic, *Super-zeta functions and
  regularized determinants associated to cofinite Fuchsian groups...*:
  https://arxiv.org/abs/2011.12795
- D. A. Hejhal, *The Selberg Trace Formula for PSL(2,R)*, vol. 2, §7:
  https://doi.org/10.1007/BFb0061302

The local source hashes used in the audit were:

~~~text
$ shasum -a 256 \
    /private/tmp/law-general-resonance.x2RNPo/bonthonneau2016.pdf \
    /private/tmp/law-general-resonance.x2RNPo/kelmer2015.pdf \
    /private/tmp/lawref-kelmer-srcdir/main.tex \
    /private/tmp/lawref-superzeta.tex \
    /private/tmp/lawref-venkov1979.pdf \
    research_notes/rh_goals_2026-08-14/lane_p/literature/Hejhal_LNM1001_Vol2_s7_pp568-600.pdf \
    research_notes/rh_goals_2026-08-14/lane_p/literature/Hejhal_LNM1001_Vol2_ch6s12_pp149-166.pdf
54d6c7412399a8774e3b649deb2e249fc23bf19fef055c9ae4d147169e5ce568  /private/tmp/law-general-resonance.x2RNPo/bonthonneau2016.pdf
c15fb0c4d1d72cc1e09ee6c70532e27d835afd8a8e01a23668cdb6049f8d5030  /private/tmp/law-general-resonance.x2RNPo/kelmer2015.pdf
951a533051f11acf983457504da67f0ca31d2a99e06ffdfb1377defe3267d02e  /private/tmp/lawref-kelmer-srcdir/main.tex
f067abad694e066ac5bd524f4c6e98d3b00c94fddc0ccaa40cc216b4bc25cc37  /private/tmp/lawref-superzeta.tex
1763de67c86a76eeaba6b7552e6a796ce32281a6ef9a3fc122e47231d6b49be0  /private/tmp/lawref-venkov1979.pdf
b0f9a7001b10f5e0eae5e5aca85124c0a233256aa0e08b5c0f04720185a2b1e9  research_notes/rh_goals_2026-08-14/lane_p/literature/Hejhal_LNM1001_Vol2_s7_pp568-600.pdf
c0dee01cf83e45e5e489e25ea299ccb2ad3654659d284bd9abc031bc6570b62f  research_notes/rh_goals_2026-08-14/lane_p/literature/Hejhal_LNM1001_Vol2_ch6s12_pp149-166.pdf
~~~

## 11. Pre-commit scope, diff, and security receipts

The staged change is only this cold-referee report:

~~~text
$ git diff --cached --name-status
A	research_notes/rh_goals_2026-08-14/lane_g/LAW_GENERAL_RESONANCE_ESCAPE_REFEREE.md
$ git diff --cached --check; printf 'diff_check_exit=%s\n' "$?"
diff_check_exit=0
~~~

The repo impact checker sees a documentation-only change.  Its lexical fallback
is explicitly degraded, so the **LOW** label is not presented as graph-verified:

~~~text
$ python3 .codex/skills/impact-of-change/tools/impact.py --repo . --diff working --json | \
    jq '{mode, risk, summary, changed_symbols: (.changed_symbols|length)}'
{
  "mode": "degraded",
  "risk": "LOW",
  "summary": "0 symbol(s) changed, 0 affected caller(s), risk = LOW  [degraded-mode: lexical estimate]",
  "changed_symbols": 0
}
~~~

The staged-diff security triage reports no introduced finding.  This is lexical
triage, not a claim of semantic security:

~~~text
$ python3 .codex/skills/security-oversight/tools/security_scan.py --repo . --diff staged --json | \
    jq '{mode, risk, findings: (.findings|length), review: (.review|length)}'
{
  "mode": "lexical-triage",
  "risk": "NONE",
  "findings": 0,
  "review": 0
}
~~~

## Final referee decision

**GAPS / NOT REFUTED.**  Do not promote
`LAW_GENERAL_RESONANCE_ESCAPE_SCOUT.md` as an all-finite-$q$ proof.  The
claim is mathematically plausible and has a sharply delimited repair, but the
candidate's decisive Selberg count was not inspected in full, its Bonthonneau
cross-check has an unusable printed sign, and the clean Kelmer theorem is
torsion-free.  Bank only the corrected restricted statements in the executive
verdict until the orbifold $L_q^*$ bridge is written and cold-refereed.

READY FOR JUDGING.

# General resonance escape: source audit

Date: 2026-08-19
Lane: general finite-area resonance escape
Verdict: **CONFIRMED-APPLICABLE**, at the qualitative scattering-pole scope below.

## Verdict and exact scope

The following statement is supported by Selberg's finite-area scattering
argument and applies to the scalar one-cusp Hecke triangle groups
\(G_q=\langle E,S^{2\cos(\pi/q)}\rangle\), every finite \(q\geq 3\):

> There are infinitely many nonreal poles of the scalar scattering
> determinant \(\phi_q(s)\) in \(\operatorname{Re}s<1/2\).

Here “nonreal” means \(\operatorname{Im}s\ne0\), and “off-line” means strict
\(\operatorname{Re}s<1/2\). This is a theorem-level conclusion from the
cited source chain, not a finite numerical observation.

The result is **not** the project's stronger effective law. The sources do
not provide a computable first pole for each \(q\), a prescribed depth
\(\operatorname{Re}s\leq1/2-\delta\), a prescribed height, or a finite
\(q\)-generic activation threshold. Those stronger assertions remain
**CONJECTURAL** until the missing effective anchor/depth statement is proved.

If the target is phrased as “a nonreal Selberg-zeta zero,” the scattering-pole
part is confirmed, but the exact orbifold Selberg-zeta divisor normalization
is not re-proved in this note. In the standard normalization, residual
scattering poles are the corresponding residual zeta zeros after the
gamma/parabolic/elliptic trivial factors are removed; extending the exact
convention used by the project to every elliptic \(G_q\) is marked
**CONJECTURAL** here and is the smallest bookkeeping repair if the zeta
wording is mandatory.

## Why the qualitative conclusion follows

Selberg, *Remarks on the distribution of poles of Eisenstein series*, reprinted
in *Collected Papers*, vol. 2, gives the needed general finite-area argument.
The searchable primary-source preview gives the following page locations.

1. On p. 15, Selberg sets \(D\) to be a finite-area fundamental domain and
   lets \(\chi\) be a one-dimensional representation of \(\Gamma\). This is
   the scalar scattering determinant setting. The p. 15 search receipt is
   included below.
2. On p. 17, Selberg states the zero/pole reflection: if
   \(\rho=\beta+i\gamma\) is a zero of \(\phi(s,\chi)\) in the right
   half-plane, then \(1-\overline\rho\) is a pole in the left half-plane.
   The same page records that only finitely many real exceptional poles occur
   in the right-half-plane interval \((1/2,1]\).
3. On p. 42, immediately after (4.26), the preview states that the relevant
   right-half-plane zero count \(N_\chi(\cdot,T)\) is “at least of the order
   \(T\log T\).” The preview OCR suppresses part of the subscript, so this
   report uses only the unambiguous consequence: the right-half-plane zero
   count is unbounded, indeed grows at least on the displayed order.
4. Therefore only finitely many of those zeros can be real. Infinitely many
   have \(\gamma\ne0\), and their reflected poles
   \(1-\overline\rho\) are nonreal with real part \(1-\beta<1/2\).

The one-cusp coefficient is nonzero in Selberg's estimate: the Hecke groups
below have exactly one cusp. No arithmeticity assumption is used in this
qualitative deduction; it therefore includes the nonarithmetic values
\(q\notin\{3,4,6\}\) as well as the arithmetic small values.

The argument is separate from a total resonance Weyl law. A total law counts
scattering poles together with \(L^2\) spectral parameters and can never by
itself be read as a lower bound for nonreal scattering poles. The Selberg
right-half-plane zero count, followed by the functional equation, is the
load-bearing off-line argument here.

## Hecke triangle and elliptic hypotheses

Hejhal, *The Selberg Trace Formula for PSL(2,R)*, vol. 2, §7, p. 569,
defines
\[
  G_N=\langle E,S^\lambda\rangle,\qquad
  \lambda=2\cos(\pi/N),\qquad N\geq3,
\]
with \(N=\infty\) giving the theta group. The finite \(N\) quotient has one
cusp and an elliptic point of order \(N\). Theorem 7.11 (p. 577) and
Corollary 7.12 (p. 579) give the family tail: for every \(t_0\) and
\(0<\delta<1\), zeros immediately to the right and reflected poles
immediately to the left of \(\operatorname{Re}s=1/2\) occur for all
sufficiently large finite \(N\). That theorem is an additional family
check, not the source of the all-finite-\(q\) qualitative conclusion above,
and its onset is ineffective.

Selberg's own p. 33 search hit explicitly describes the same family: for
\(q>q_0(T_0,\varepsilon)\), \(\phi_q(s,\chi_0)\) has a zero near
\(s_0=1/2+it_0\), and “\(\Gamma_q\) has just one cusp” while the limit group
has two cusps. Thus the source's finite-area setup is not being applied to a
different continuous Hecke deformation. Elliptic elements are allowed in
the trace/scattering framework; Lax--Phillips explicitly separates elliptic
and parabolic terms in its trace formula (p. 288).

## Primary-source receipts

### Selberg (primary; decisive qualitative source)

Atle Selberg, “Remarks on the distribution of poles of Eisenstein series,”
in *Collected Papers*, vol. 2 (Springer, 1991), pp. 15--46 in the reprint.

- Google Books preview:
  https://books.google.com/books?id=1jRuJvObawUC
- Springer book record:
  https://link.springer.com/book/9783642410222
- Page-15 receipt, run in this worktree:

~~~text
$ curl -L --silent --show-error \
    'https://books.google.com/books?jscmd=SearchWithinVolume2&q=fundamental%20domain%20of%20Gamma&vid=1jRuJvObawUC'
{"number_of_results":1,"search_results":[{"page_id":"PA15","page_number":"15","snippet_text":"... fundamental domain of I by D = Dr , and its area , assumed to be finite ... x denotes a one-dimensional representation of Γ ..."}]}
~~~

- Hecke/one-cusp receipt, same source:

~~~text
$ curl -L --silent --show-error \
    'https://books.google.com/books?vid=1jRuJvObawUC&jscmd=SearchWithinVolume2&q=one%20cusp'
{"number_of_results":2,"search_results":[{"page_id":"PA33","page_number":"33","snippet_text":"... q_o = q_o(T_o, ε) such that for q > q_o, φ_q(s, χ_o) has a zero in |s - s_o| < ε ... Here the Γ_q has just one cusp, while the limitgroup ... has two cusps ..."}]}
~~~

- Lower-count receipt, same source (the preview's OCR drops some symbols but
  preserves the page and the load-bearing phrase):

~~~text
$ curl -L --silent --show-error \
    'https://books.google.com/books?jscmd=SearchWithinVolume2&q=at%20least%20of%20the%20order&vid=1jRuJvObawUC'
{"number_of_results":3,"search_results":[{"page_id":"PA42","page_number":"42","snippet_text":"... at least of the order Tlog T, while (4.24') shows ..."}]}
~~~

The last receipt is intentionally not used to reconstruct a constant or an
OCR-damaged formula. It is used only together with the page-17 reflection
statement and the independently legible weighted form reproduced in
Bonthonneau (below) to establish unbounded off-line scattering data.

### Hejhal (primary; direct Hecke-orbifold applicability)

D. A. Hejhal, *The Selberg Trace Formula for PSL(2,R)*, vol. 2, Lecture
Notes in Mathematics 1001, Springer (1983), §7, pp. 568--600.

- DOI: https://doi.org/10.1007/BFb0061302
- Local source:
  research_notes/rh_goals_2026-08-14/lane_p/literature/Hejhal_LNM1001_Vol2_s7_pp568-600.pdf
- Receipt:

~~~text
$ shasum -a 256 .../Hejhal_LNM1001_Vol2_s7_pp568-600.pdf
b0f9a7001b10f5e0eae5e5aca85124c0a233256aa0e08b5c0f04720185a2b1e9  ...pdf
~~~

The extracted p. 569 definition is \(G_N=\langle E,S^\lambda\rangle\),
\(\lambda=2\cos(\pi/N)\), \(N\ge3\), with \(G_\infty\) the theta group.
The extracted theorem locations are:

~~~text
$ rg -n 'Theorem 7\.11|Corollary 7\.12|G_N|one cusp|poles' \
    research_notes/rh_goals_2026-08-14/lane_g/LAW_HEJHAL_S7_EXTRACT.md
19: p. 568–569 ... Hecke group G_N = ... λ = 2cos(π/N), N ≥ 3 ...
43: Theorem 7.11 (p. 577) ... contains ZEROS of φ_N(s) whenever N is sufficiently large
46: Corollary 7.12 (p. 579) ... contains POLES of φ_N(s) for N sufficiently large
~~~

This confirms the one-cusp elliptic Hecke family and the reflected
zero/pole convention. It does **not** make the printed ineffective onset
effective, and it does not supply the stronger fixed-depth law.

### Lax--Phillips (primary; scattering continuation and elliptic terms)

P. D. Lax and R. S. Phillips, “Scattering theory for automorphic functions,”
*Bull. Amer. Math. Soc.* 2 (1980), 261--285.

- PDF:
  https://www.ams.org/journals/bull/1980-02-02/S0273-0979-1980-14735-7/S0273-0979-1980-14735-7.pdf
- SHA-256 receipt:

~~~text
$ shasum -a 256 /tmp/law-general-resonance.x2RNPo/lax-phillips1980.pdf
7729c0d956f5b6bf1b0f0ccf80888a787c8c76d06f600fede7d852215b4e2ac3  .../lax-phillips1980.pdf
~~~

Theorem 3.2 and Corollary 3.3 (printed pp. 268--269) give compact resolvent
and meromorphic continuation in the automorphic scattering construction;
Theorem 4.2 (p. 270) gives meromorphic continuation of Eisenstein series.
Their p. 288 trace-formula discussion explicitly has separate hyperbolic,
elliptic, and parabolic contributions. This source is a scope/continuation
check, not the lower-bound proof.

### Müller (primary; a warning against confusing a total Weyl law with a pole lower bound)

Werner Müller, “Spectral geometry and scattering theory for certain complete
surfaces of finite volume,” *Invent. Math.* 109 (1992), 265--305.

- Preprint: https://archive.mpim-bonn.mpg.de/1757/1/preprint_1991_21.pdf
- SHA-256 receipt:

~~~text
$ shasum -a 256 /tmp/law-general-resonance.x2RNPo/muller1991.pdf
151cee817e702882e8d445659721e1db45982e71f89cebd7d6dce959e7b9df1b  .../muller1991.pdf
~~~

Müller's introduction (printed pp. 1--3) defines resonances from the poles
of the scattering determinant and then forms a combined set with the
\(L^2\)-eigenvalue parameters. Theorem 4.23 (p. 24) states
\[
  N(T)+\tfrac12N_p(T)\sim \frac{\operatorname{Area}(M)}{4\pi}T^2.
\]
That is a combined resonance/eigenvalue Weyl law. It does **not** imply
\(N_p(T)\to\infty\), much less nonreal off-line poles, without a separate
argument. Müller assumes torsion-free surfaces in the main geometric setup;
this is why his theorem is used here as a counting warning, not as the
elliptic Hecke applicability source.

### Bonthonneau (primary; explicit separation of scattering poles)

Y. Bonthonneau, “A note on the resonance counting function for surfaces with
cusps,” *J. Spectr. Theory* 6 (2016), 137--144.

- PDF: https://ems.press/content/serial-article-files/33566
- SHA-256 receipt:

~~~text
$ shasum -a 256 /tmp/law-general-resonance.x2RNPo/bonthonneau2016.pdf
54d6c7412399a8774e3b649deb2e249fc23bf19fef055c9ae4d147169e5ce568  .../bonthonneau2016.pdf
~~~

Pages 137--141 define the scattering-pole set \(\Lambda\), the resonance
set \(R\) obtained by adjoining \(L^2\)-eigenvalue parameters, and the
scattering matrix identities \(\Phi(s)\Phi(1-s)=I\) and unitarity on
\(\operatorname{Re}s=1/2\). Equation (3), p. 138, is Selberg's total
resonance Weyl law; equation (5) is the scattering-phase/eigenvalue relation.
Most importantly for the separation audit, equation (8), p. 139, gives
Selberg's weighted sum over left-half-plane resonance parameters with leading
term
\[
  \frac{\kappa}{4\pi}T\log(T/\pi),
\]
up to the displayed lower-order terms. The line parameters contribute zero
weight, and only finitely many exceptional real spectral parameters can
contribute a bounded exceptional part. Thus, for \(\kappa=1\), this
weighted lower bound forces infinitely many left-half-plane scattering poles;
it is not an inference from the total Weyl law (3). This is the legible
independent check on the OCR-damaged Selberg p. 42 hit.

The paper treats smooth cusp surfaces, so it is not being used to silently
extend an orbifold theorem. The orbifold/elliptic applicability is supplied
by Selberg's own finite-area \(\Gamma_q\) passage and Hejhal's Hecke-group
definition above.

## Zeta-zero wording and remaining gap

The conclusion banked here is about poles of \(\phi_q(s)\). For the scalar
cofinite Selberg normalization, the nontrivial residual divisor of the
Selberg zeta function is standardly identified with these scattering poles;
elliptic factors add explicit trivial factors. The exact all-\(q\) orbifold
divisor normalization was not independently reconstructed from a primary
source in this bounded scout, so the sentence

> “each such pole is a nonreal zero of the project's normalized
> \(Z_{G_q}(s)\)”

is **CONJECTURAL** until the project's precise zeta normalization is matched
to the elliptic Selberg trace formula. This does not weaken the scattering
pole theorem above.

The smallest missing theorem for the project's full law is stronger than this
general existence result:

1. Fix an explicit depth/height window (or an explicit anchor defect) and
   prove that every relevant finite \(q\) has a pole in that window; and
2. make the threshold/effectivity explicit, then separately match the pole to
   the project's normalized Selberg-zeta divisor.

Hejhal's Theorem 7.11/Corollary 7.12 only gives an ineffective sufficiently
large-\(q\) family onset. Selberg's order-\(T\log T\) theorem gives infinitely
many poles somewhere, but no computable first-pole location. Neither source
closes the project's quantitative activation gate.

## Ledger correction

**Correction block (2026-08-19).** Any earlier note saying that no general
finite-area theorem forces off-line scattering poles is too broad for the
qualitative statement above: Selberg's right-half-plane zero count plus
reflection gives infinitely many nonreal poles for every one-cusp finite-area
\(\Gamma_q\), including the elliptic Hecke triangle family. The earlier
negative statement remains correct only for the stronger claims of a
\(q\)-effective threshold, a prescribed depth/height, or a fully matched
project-specific orbifold Selberg-zeta normalization. No earlier note is
silently rewritten by this block.

## Source receipt status

~~~text
$ git diff --check
<no output>
~~~

READY FOR JUDGING.

## Referee correction — 2026-08-19

The separate cold report `LAW_GENERAL_RESONANCE_ESCAPE_REFEREE.md` returns
**GAPS / NOT REFUTED**.  The `CONFIRMED-APPLICABLE` label at the head of this
scout is therefore withdrawn and must not be consumed downstream.

The exact source gap is threefold: the Selberg preview does not expose the
counted subscript or complete theorem; Bonthonneau's printed equation (8) has
a sign incompatible with that paper's own definition of its resonance set;
and Kelmer's clean weighted-zero theorem globally assumes a torsion-free
lattice.  Consequently only the modular case `q=3` is independently
**CONFIRMED** at this scout's source level.  Every elliptic Hecke case `q>=4`
remains **CONJECTURAL / OPEN** here.  This is not a refutation of the desired
scattering-pole conclusion: a direct fixed-`q` Hejhal-to-Selberg/Kelmer
analytic bridge is the identified repair, but it requires its own written
proof and cold referee.  This dated block appends the correction without
silently rewriting the original candidate.

# Orbifold scattering zero count: the direct Hejhal--Kelmer bridge

**Date:** 2026-08-19. **Lane:** G / LAW closure. **Scope:** source bridge only.

**Status: PROOF CANDIDATE -- CONJECTURAL until a separate cold referee accepts
the Jensen boundary bookkeeping. READY FOR COLD REFEREE.**

This note records the smallest repair requested after the torsion-free warning
on Kelmer's theorem. It specializes the proof to the actual finite Hecke
orbifolds, using Hejhal's section 7 treatment of those groups before applying
the purely complex-analytic Jensen/Selberg argument. It does not promote a
program status and does not use a torsion-free cover.

## 1. Verdict and target

The direct-count shortcut is not banked here: the Jorgenson--Smajlovic paper
quotes a Hejhal count in its comparison section, but the available text
extraction does not by itself settle the counted-subscript/convention audit.
The repair below uses the following direct-Hecke **CONJECTURAL proof candidate**.

> For every finite integer \(q\ge3\), let \(M_q=G_q\backslash\mathbb H\), and
> let \(\phi_q(s)\) be its scalar scattering determinant for the trivial
> character. Write zeros \(\rho=\beta+i\gamma\) with multiplicity. Then
> \[
> \mathcal N_q(T):=
> \sum_{\substack{\phi_q(\rho)=0,\;|\gamma|<T\\\beta>1/2}}
> (\beta-\tfrac12)
> =\frac{1}{2\pi}T\log T+A_qT+O_q(\log T).
> \tag{C}
> \]
> Hence there are infinitely many nonreal scattering zeros in
> \(\Re s>1/2\), and \(\phi_q\) has strict-left nonreal poles at \(1-\rho\).

The \(O_q\)-notation is intentionally group-dependent; this lane claims no
\(q\)-uniform error or effective height. The leading coefficient is the
\(d=2,\ \kappa=1\) specialization of Kelmer's printed
\[
\frac{\kappa(d-1)}{2\pi}T\log T
\]
coefficient after passing from the weighted Jensen quantity to the unweighted
count. The displayed coefficient is a proof target here, not a new numerical
observation.

## 2. Direct Hejhal identification of \(G_q\)

Hejhal, LNM 1001 Vol. II, section 7, defines the Hecke groups \(G_N\) by
\[
\lambda_N=2\cos(\pi/N),\qquad N\ge3,\quad
E^2=1,\quad (ES^\lambda)^N=1,
\]
and allows \(N=\infty\) only for the theta-group limit. The finite \(N=q\)
groups are exactly the cofinite Hecke triangle orbifolds used in the LAW
program. The order-two and order-\(q\) relations are the elliptic
stabilizers; the parabolic generator gives the cusp. Hejhal's section 7
discussion and MMS's independent group presentation state that the finite
Hecke groups have one cusp.

MMS gives the same convention in an independently accessible primary source:
\[
\lambda_q=2\cos(\pi/q),\quad
S=\begin{pmatrix}0&-1\\1&0\end{pmatrix},\quad
T_q=\begin{pmatrix}1&\lambda_q\\0&1\end{pmatrix},\quad
S^2=(ST_q)^q=1.
\]
Its abstract records \(q=3,4,6\) as the arithmetic exceptions; finite
\(q\notin\{3,4,6\}\) are non-arithmetic. Thus the direct bridge applies to
all finite \(q\ge3\), including the non-arithmetic subfamily.

**Primary sources:** [Hejhal section 7 scan](../lane_p/literature/Hejhal_LNM1001_Vol2_s7_pp568-600.pdf),
[MMS arXiv:0912.2236](https://arxiv.org/abs/0912.2236), and
[MMS DOI](https://doi.org/10.3934/dcds.2012.32.2453).

Receipt:

~~~
$ nl -ba /tmp/hejhal_s7.txt | sed -n '70,112p'
   72  A = 2 cos(pi/N), N is a positive integer >= 3; N = infinity is also allowed.
   80  The defining relations are E^2 = 1 and (ES^lambda)^N = 1.
   86  N = infinity corresponds to the theta group; N = 3 corresponds to PSL(2,Z).
  107  Throughout this section ... N >= 3 ... Let E_N(z;s) be the Eisenstein series.

$ nl -ba /tmp/hecke_transfer_operator.txt | sed -n '200,224p;1940,1948p'
  200  ... cofinite Fuchsian groups ... quotient orbifold ... finite hyperbolic area.
  207  For an integer q >= 3, the Hecke triangle group, Gq, is the cofinite Fuchsian group.
  217  The only relations ... S^2 = (STq)^q = 1.
 1947  ... all the Hecke triangle groups have only one cusp.

$ head -25 /tmp/hecke_transfer_operator.txt
  23  Gq, q = 3, 4, ..., which are non-arithmetic for q != 3, 4, 6.
~~~

## 3. Source-established scattering inputs

FJS is an independent torsion check: it starts with a finite-volume,
noncompact Fuchsian quotient **possibly with elliptic fixed points**, and
calls the quotient an orbifold. In the scalar trivial-character case its
degree of singularity is the number of cusp channels, so \(\mathbf k=\kappa=1\)
for \(G_q\). Venkov is the cited source for the scattering determinant formula
and functional equation; Hejhal section 7 applies those facts directly to
\(G_N\), so no extension from torsion-free lattices is being inferred.

### 3.1 Meromorphic continuation, functional equation, and right poles

FJS section 2.4, citing Venkov's Theorem 3.5 p. 59, states that the determinant
\(\phi(s)\) of the automorphic scattering matrix is meromorphic, is
holomorphic for \(\Re s>1/2\) apart from finitely many poles, and satisfies
\[
\phi(s)\phi(1-s)=1. \tag{F}
\]
The same divisor list gives finitely many real zeros to the right of the
critical line and finitely many real poles in \(1/2<\sigma\le1\). Hejhal's
direct \(G_N\) construction supplies these inputs for the target orbifolds.
Only finiteness is used below; no nonreal-zero count is imported.

### 3.2 Hejhal's direct generalized Dirichlet series

Hejhal equation (7.5), for \(\Re s>1\), writes the one-cusp scattering
coefficient as
\[
\phi_N(s)=\sqrt\pi\,\frac{\Gamma(s-\frac12)}{\Gamma(s)}
\sum_{\substack{W_{\infty}\in[S]\backslash\mathcal G_N/[S]\\
c(W_{\infty})\ne0}}
|c(W_{\infty})|^{-2s}. \tag{H7.5}
\]
Grouping equal positive \(c\)-values gives
\[
\phi_q(s)=\sqrt\pi\,\frac{\Gamma(s-\frac12)}{\Gamma(s)}
\sum_{n\ge1}\frac{d_q(n)}{g_{q,n}^{2s}},
\qquad 0<g_{q,1}<g_{q,2}<\cdots,\quad d_q(1)\ne0.
\tag{D}
\]
The coefficients are real in the scalar case. Normalize the first term by
\[
\lambda_{q,n}=\left(\frac{g_{q,n}}{g_{q,1}}\right)^2>1,\qquad
a_{q,n}=\frac{d_q(n)}{d_q(1)},\qquad
L_q^*(s)=1+\sum_{n\ge2}a_{q,n}\lambda_{q,n}^{-s}. \tag{N}
\]
Then
\[
\phi_q(s)=\sqrt\pi\,\frac{\Gamma(s-\frac12)}{\Gamma(s)}
d_q(1)g_{q,1}^{-2s}L_q^*(s). \tag{NF}
\]
The gamma ratio and \(g_{q,1}^{-2s}\) have no zeros in \(\Re s>1/2\), so
the zeros and poles there are exactly those of \(L_q^*\). Absolute convergence
of the Dirichlet series gives \(L_q^*(s)=1+O_q(e^{-c_q\Re s})\) as
\(\Re s\to+\infty\), which is the right-edge input in Jensen's rectangle.

### 3.3 Unitarity and the vertical polynomial bound

For real scalar coefficients, \(\phi_q(\bar s)=\overline{\phi_q(s)}\). Together
with (F), this gives the critical-line identity
\[
|\phi_q(\tfrac12+it)|=1 \tag{U}
\]
away from a possible central divisor point. This is the scalar form of
critical-line unitarity; it is also the identity used in Hejhal's section 7
proof.

Hejhal Lemma 7.7 gives, for every fixed \(\epsilon>0\), a constant \(C_6(\epsilon)\)
such that
\[
|\phi_N(\sigma+it)|\le C_6(\epsilon),\qquad
\tfrac12\le\sigma\le\tfrac32,\quad |t|>\epsilon. \tag{H7.7}
\]
This is the required Maass--Selberg/a-priori bound for the actual Hecke
orbifold, not an extension of Kelmer's torsion-free theorem. Combining
(H7.7) with (NF) and Stirling gives
\[
L_q^*(\sigma+it)=O_q(|t|^{1/2}),\qquad
\tfrac12\le\sigma\le\tfrac32,\quad |t|>1. \tag{P}
\]
For \(\sigma\ge3/2\), the absolutely convergent series supplies a bounded
right half-plane. Therefore (P), finite right poles, and the right-edge
Dirichlet estimate verify every analytic hypothesis used by Kelmer's
\(d=2\) Jensen/Selberg replay.

Receipt:

~~~
$ nl -ba /tmp/hejhal_s7.txt | sed -n '123,131p;403,417p'
  126  (7.5) ... phi_N(s) = sqrt(pi) Gamma(s-1/2)/Gamma(s)
  128  sum over W_infinity in [S] \ G_N / [S], c(W_infinity) != 0,
  130  Re(s) > 1.
  403  LEMMA 7.7. For each epsilon > 0, there exists a positive constant C6(epsilon) such that
  411  1/2 <= sigma <= 3/2
  412  whenever ... |t| > epsilon.

$ nl -ba /tmp/fjs_2011.12795.txt | sed -n '259,306p'
  261  Let phi(s) denote the determinant of the automorphic scattering matrix.
  263  The function phi(s) is meromorphic of order at most two ...
  264  ... holomorphic for Re(s) > 1/2, except for a finite number of poles ...
  265  phi(s) phi(1-s) = 1.
  266  Theorem 2.1 ... For Re(s) > 1 ...
  273  0 < g1 < g2 < ... and d(n) ... d(1) != 0.
  299  Finitely many real zeros ... to the left of 1/2 (reflected right poles).
  301  Finitely many real zeros of the form rho_i > 1/2, with multiplicity.
  304  Finitely many poles sigma_i in (1/2,1].
  306  Zeros ... Re(rho) > 1/2 and Im(rho) > 0.
~~~

## 4. The Jensen/Selberg replay in \(d=2\)

This is the **CONJECTURAL proof-candidate replay**. It is pure complex
analysis once section 3 is in place, so elliptic stabilizers no longer enter.

### 4.1 Weighted rectangle identity

Fix \(\alpha\ge1/2\), and let
\[
F_q(\alpha,T)=
\sum_{\substack{L_q^*(\rho)=0,\;|\Im\rho|\le T\\
\Re\rho=\beta>\alpha}}
(T-|\Im\rho|)(\beta-\alpha).
\]
Let \(\sigma_j>\alpha\) be the finitely many poles of \(L_q^*\), with
multiplicity. Jensen/Littlewood's rectangle, with the right side sent to
\(+\infty\) using \(L_q^*(s)=1+O_q(e^{-c_q\Re s})\), gives Kelmer's equation
(4.20) specialized to \(d=2\):
\[
F_q(\alpha,T)=
\frac1{2\pi}\int_{-T}^{T}(T-|t|)\log|L_q^*(\alpha+it)|\,dt
+T\sum_{\sigma_j>\alpha}(\sigma_j-\alpha)+O_q(\log T).
\tag{J}
\]
The plus sign on the pole term is essential: poles occur with the opposite
sign in the meromorphic Jensen divisor and are moved to the right side. The
horizontal sides and fixed small divisor detours are the \(O_q(\log T)\)
term, controlled by (P). The possible central point \(s=1/2\) is handled by
a fixed semicircle and then a limit; this is the first cold-referee check.

For
\[
F_{q,1}(\alpha,T)=
\sum_{\substack{L_q^*(\rho)=0,\;|\Im\rho|\le T\\\beta>\alpha}}
(\beta-\alpha),
\]
nonnegativity of the summands gives Kelmer's equation (4.22):
\[
F_q(\alpha,T)-F_q(\alpha,T-1)
\le F_{q,1}(\alpha,T)
\le F_q(\alpha,T+1)-F_q(\alpha,T).
\tag{DIF}
\]

### 4.2 Critical-line integral

At \(s=1/2+it\), (U) and (NF) imply
\[
|L_q^*(\tfrac12+it)|
=\frac{g_{q,1}}{\sqrt\pi\,|d_q(1)|}
\left|\frac{\Gamma(\frac12+it)}{\Gamma(it)}\right|. \tag{G}
\]
The gamma identities
\[
|\Gamma(\tfrac12+it)|^2=\frac{\pi}{\cosh(\pi t)},\qquad
|\Gamma(it)|^2=\frac{\pi}{|t|\sinh(\pi|t|)}
\]
give
\[
\left|\frac{\Gamma(\frac12+it)}{\Gamma(it)}\right|^2
=|t|\tanh(\pi|t|). \tag{GT}
\]
As \(|t|\to\infty\),
\[
\log|L_q^*(\tfrac12+it)|
=\tfrac12\log|t|+C_q+O(e^{-2\pi|t|}).
\]
Near \(t=0\), (GT) instead gives \(\log|L_q^*(\tfrac12+it)|=\log|t|+O_q(1)\),
which is integrable and contributes only a linear \(T\)-term. Kelmer's Lemma
4.5, specialized to \(d=2,\kappa=1\),
therefore gives
\[
\frac1{2\pi}\int_{-T}^{T}(T-|t|)
\log|L_q^*(\tfrac12+it)|\,dt
=\frac1{4\pi}T^2\log T+B_qT^2+C_qT+O_q(\log T).
\tag{I}
\]
The leading coefficient is transparent from
\[
2\int_0^T(T-t)\log t\,dt=T^2\log T-\tfrac32T^2;
\]
the \(1/2\) from (G) and \(1/(2\pi)\) outside give \(1/(4\pi)\). Elliptic
geometry can alter \(B_q,C_q\), but not this coefficient.

### 4.3 Difference and zero count

Substitution of (I) into (J) at \(\alpha=1/2\) gives
\[
F_q(\tfrac12,T)=\frac1{4\pi}T^2\log T+B_qT^2
+\left(C_q+\sum_{\sigma_j>1/2}(\sigma_j-\tfrac12)\right)T
+O_q(\log T). \tag{W}
\]
Applying (DIF) and expanding \(F_q(T\pm1)-F_q(T)\) gives (C), for some
group-dependent real constant \(A_q\); its exact combination of the displayed
\(B_q\), \(C_q\), pole sum, and the derivative of \(T^2\log T\) is not needed
here and is intentionally not asserted. The only endpoint issue is the
harmless \(<T\) versus \(\le T\) convention. The leading
term is
\[
\frac{d}{dT}\left(\frac1{4\pi}T^2\log T\right)
=\frac1{2\pi}T\log T+O(T),
\]
which matches Kelmer's \(\kappa(d-1)/(2\pi)\) at \(d=2,\kappa=1\).

Receipt:

~~~
$ nl -ba /tmp/kelmer_1402.4780.txt | sed -n '997,1006p;1018,1064p;1148,1203p'
 1006  ... kappa(d-1)^2/(4 pi) T^2 log(T) + B_Gamma T^2 + C_Gamma T + O(log(T)).
 1157  ... L*(s) satisfies all the assumptions needed for [Sel90, Lemma 1,2] ...
 1162  (4.20) ... (T-|gamma|)(beta-alpha) = (1/(2 pi)) integral ...
 1167  ... + T sum_{sigma_j>alpha}(sigma_j-alpha) + O(log(T)).
 1180  F(T)-F(T-1) <= F1(T) <= F(T+1)-F(T).
 1197  ... kappa(d-1)/(2 pi) T log(T) + A_Gamma T + O(log(T)).
~~~

## 5. Infinite nonreal zeros and strict-left poles

FJS/Hejhal give only finitely many real zeros of \(\phi_q\) in
\(\Re s>1/2\). Their contribution to (C) is bounded independently of \(T\),
whereas the positive \(T\log T\) term diverges. Therefore (C) forces
infinitely many zeros with \(\gamma\ne0\). This is a **CONJECTURAL consequence
of the proof candidate** until the cold referee accepts the boundary term in
(J); it is not a finite numerical observation.

For a zero \(\rho\) of order \(m\), set \(s_0=1-\rho\). In (F),
\(\phi_q(1-s)\) has a zero of order \(m\) at \(s_0\); the product being one
forces \(\phi_q\) to have a pole of order \(m\) at \(s_0\). Moreover,
\[
\Re(1-\rho)=1-\Re\rho<\tfrac12,\qquad
\Im(1-\rho)=-\Im\rho\ne0.
\]
This local reflection is source-established once (F) and the right zero are
accepted; it does not use Bonthonneau or any torsion extension.

## 6. Cold-referee checklist and ledger caveats

### Source-established

- FJS/Venkov: orbifold scattering determinant, meromorphic continuation,
  functional equation, generalized Dirichlet series, and finite real right
  exceptions.
- Hejhal section 7: the same Dirichlet series and the vertical strip bound for
  the actual Hecke groups \(G_N\), including elliptic stabilizers.
- MMS: cofinite Hecke orbifold convention and one cusp for finite \(q\ge3\).
- Kelmer: the Jensen/Selberg rectangle, gamma integral, and conversion to the
  \(\kappa(d-1)/(2\pi)\) coefficient.

### CONJECTURAL until a separate referee pass

- The exact central-point semicircle and horizontal-edge estimate needed to
  interpret Kelmer's (4.20) at \(\alpha=1/2\) with the Hejhal normalization.
- The endpoint convention \(<T\) versus \(\le T\) and its absorption into
  \(O_q(\log T)\).
- The resulting unconditional LAW bridge (C) for every finite \(q\ge3\).

The Bonthonneau 2016 equation with the opposite-sign counting convention is
**not used**; it remains a ledger warning only. No claim here consumes its
printed sign.

**READY FOR COLD REFEREE.** Attack order: (i) Hejhal (7.5)/(7.15)
normalization, (ii) Kelmer (4.20) at the critical line and central detour,
(iii) the finite real-exception subtraction, and (iv) the order-\(m\) reflection.

## 7. Primary-source receipts and URLs

Downloaded sources were kept in /tmp only; no PDF or cache is a repository
artifact.

~~~
$ file /tmp/fjs_2011.12795.pdf /tmp/kelmer_1402.4780.pdf /tmp/hecke_transfer_operator.pdf
/tmp/fjs_2011.12795.pdf:          PDF document, version 1.4, 21 pages
/tmp/kelmer_1402.4780.pdf:        PDF document, version 1.4, 26 pages
/tmp/hecke_transfer_operator.pdf: PDF document, version 1.4, 30 pages

$ file /tmp/venkov1979.pdf
/tmp/venkov1979.pdf:              PDF document, version 1.4

$ shasum -a 256 /tmp/fjs_2011.12795.pdf /tmp/kelmer_1402.4780.pdf /tmp/hecke_transfer_operator.pdf
36c9d020fcc7d0118264c486330db9936f866670c45c0e77b185cdc2b9127228  /tmp/fjs_2011.12795.pdf
c15fb0c4d1d72cc1e09ee6c70532e27d835afd8a8e01a23668cdb6049f8d5030  /tmp/kelmer_1402.4780.pdf
a10020bd084534dc60fc3e887958f1583f2fc115d567961b461df1a59b32e072  /tmp/hecke_transfer_operator.pdf
322d149b7b4b469da49ecc7930a4b0cf03527b7028703822e1ea176fe46ccda4  /tmp/venkov1979.pdf

$ shasum -a 256 /Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_p/literature/Hejhal_LNM1001_Vol2_s7_pp568-600.pdf
b0f9a7001b10f5e0eae5e5aca85124c0a233256aa0e08b5c0f04720185a2b1e9  .../Hejhal_LNM1001_Vol2_s7_pp568-600.pdf
~~~

Primary URLs:

- [Friedman--Jorgenson--Smajlovic, arXiv:2011.12795](https://arxiv.org/abs/2011.12795), sections 2.1 and 2.4.
- [Venkov, Spectral theory of automorphic functions](https://www.mathnet.ru/eng/rm7178), Russian Math. Surveys 34:3 (1979), DOI [10.1070/RM1979v034n03ABEH004000](https://doi.org/10.1070/RM1979v034n03ABEH004000).
- [Hejhal, The Selberg Trace Formula for PSL(2,R), Vol. 2](https://link.springer.com/book/10.1007/BFb0061302), LNM 1001 (1983), section 7 and the cited scattering discussion.
- [Kelmer, On distribution of poles of Eisenstein series and the length spectrum of hyperbolic manifolds](https://arxiv.org/abs/1402.4780), section 4. Its global setup is torsion-free; only the complex-analytic proof template is reused here.
- [Mayer--Muhlenbruch--Stromberg, The transfer operator for the Hecke triangle groups](https://doi.org/10.3934/dcds.2012.32.2453), group presentation and one-cusp statement.

**Final lane label: PROOF CANDIDATE / CONJECTURAL pending cold referee; READY FOR COLD REFEREE.**

## Cold-referee promotion and wording corrections — 2026-08-19

The separate adverse report
`LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_REFEREE.md` returns **CONFIRMED** for
the accepted scattering-resonance LAW scope. Thus the earlier
`PROOF CANDIDATE / CONJECTURAL` label is superseded as follows:

> **THEOREM (paper-level, unconditional).** For every finite integer
> \(q\ge3\), the scalar trivial-character scattering determinant of the
> one-cusp Hecke triangle orbifold has infinitely many nonreal zeros
> \(\rho\) with \(\Re\rho>1/2\), and therefore infinitely many
> multiplicity-matched scattering poles \(1-\rho\) with
> \(\Re(1-\rho)<1/2\). In particular, every nonarithmetic finite Hecke
> group \(G_q\), \(q\notin\{3,4,6\}\), has a scattering resonance strictly
> off \(\Re s=1/2\).

The referee also confirms the stronger weighted asymptotic (C). For the LAW
existence conclusion, the shorter triangular argument is sufficient:

\[
F_q(\tfrac12,T)=\frac{1}{4\pi}T^2\log T+O_q(T^2),
\]

where finitely many total right zeros would make the defining sum only
\(O_q(T)\).

Three wording repairs are appended without changing the theorem:

1. \(\phi_q\) has no central divisor; the normalization \(L_q^*\) has the
   exactly simple zero at \(s=1/2\).
2. The horizontal \(O_q(\log T)\) term uses the right-edge normalization and
   the Selberg--Titchmarsh argument reproduced by Kelmer, not the modulus
   bound alone.
3. No explicit formula for the group-dependent linear coefficient \(A_q\) is
   consumed; its existence is all that is asserted.

This promotion certifies no effective first height, no \(q\)-uniform error,
no machine formalization, and no project-specific Selberg-zeta normalization.
Those stronger statements remain **OPEN** and are not needed for the stated
scattering-resonance LAW. This dated block preserves rather than silently
rewrites the original candidate status.

---

## Dated correction block — second cold audit repairs (2026-08-20, append-only)

A second, lineage-independent cold audit (LAW_SECOND_AUDIT_REFEREE.md,
2026-08-20) returned **CONFIRMED** on the mathematical statement — every
attack failed, including exact-arithmetic refutation of the c-value
density attack and full numeric instantiation of the chain at q=3 —
while mandating four repairs before any paper-level use.  They are
recorded here append-only; none touches the theorem:

1. ATTRIBUTION: the d=2 counting theorem consumed as "(C)" is due to
   Selberg (Remarks on the distribution of poles of Eisenstein series,
   Piatetski-Shapiro Festschrift, Israel Math. Conf. Proc. 3, 1990), per
   Kelmer Remark 0.2 and §4 opening; Kelmer's contribution is the d ≥ 3
   generalization.  Selberg 1990 itself has NOT been read by the author
   or either referee; the statement is consumed through Kelmer's
   transcription, numerically corroborated at q=3.  Favourable note: at
   κ=1 the Hejhal (7.5) coefficients are positive integers, inside
   Selberg's original positive-coefficient hypothesis class.
2. PRINTED PARTIAL ANTECEDENT: Hejhal LNM 1001, Theorem 7.11 and
   Corollary 7.12 (pp. 577-579, in the in-repo scan) prove zeros/poles
   of φ_N in any prescribed rectangle touching the critical line for all
   sufficiently large N.  Weaker in q-range (large N only), stronger in
   localization.  Must be cited wherever novelty is framed.
3. VENKOV CITATION FIX: the continuation/divisor source is Venkov,
   Spectral theory of automorphic functions, Trudy Mat. Inst. Steklov
   153 (1981) / Proc. Steklov 1982 no. 4(153) — NOT the 1979 Uspekhi
   survey (RM7178 / 10.1070/RM1979v034n03ABEH004000), whose page range
   excludes the cited p. 59.  Not load-bearing (FJS §2.4 + Thm 2.1
   carry the content), but the URL block above conflates two Venkov
   items.
4. RECEIPT RELABELING: the `~~~` source-quotation blocks in this note
   are hand-cleaned transcriptions of pdftotext output, not verbatim
   command output, and Hejhal (7.2)-(7.5) are stated for the conjugated
   group with cusp width 1 and ϰ ≡ 1 (the divisor is invariant under
   the conjugation/normalization, factor c^{1-2s} zero-free).  Treat
   all such blocks in this note as TRANSCRIPTIONS.

Ledger findings from the same audit (consume-side warnings):
- Kelmer's printed B_Γ carries a spurious log π from a /π inside the
  logarithm of (4.18), and his printed A_Γ assembly formula is wrong
  (both errors confirmed independently; correct d=2 values recomputed
  and matched to Riemann-von Mangoldt at q=3 to 12 digits).  Do NOT
  consume A_q, B_q, or C_q numerics from Kelmer.
- The "nonarithmetic in particular" clause is NON-DISCRIMINATING:
  q=3 (arithmetic) has the same off-line property (positive proportion
  at Re s = 1/4).  This LAW must never be used as an arithmeticity
  signature.

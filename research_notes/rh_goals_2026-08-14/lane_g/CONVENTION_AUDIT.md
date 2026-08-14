# Convention audit: MMS \(q=5\) mms+

## Verdict

The MMS-correct convention is the certified engine's \`sign=+1\` route: the
\(P\)-symmetric Markov-partition sector of the \(q=5\) operator in printed
MMS eq. (34), with

\[
s_* = 0.45389518 + 5.76353724i
\quad\text{(flagship display: }0.45390+5.76354i\text{).}
\]

The \(0.43318010+5.67574682i\) value is not an MMS alternative sign/block
convention. It is the zero of the current Sonnet collocation implementation
after a basis-coordinate error: its interpolation nodes are placed at
\(0.5\rho_i\), but the input basis is evaluated and tail-normalized using
\(\rho_j\), not \(0.5\rho_j\). Correcting that one factor sends the Sonnet
calculation back to the \(0.45389518+5.76353724i\) pin.

The theorem should therefore carry the first pin and call the sector
“mms+ / \(P\)-symmetric.” It must not call this \(P\)-sector Maass even parity:
MMS's \(P\) is the reflection of the \(\lambda_q\)-CF Markov partition, not
the geometric \(x\mapsto-x\) Maass parity (MMS §5.1, definition of \(P\) and
the \(B_\pm\) eigenspaces; extraction lines 75–102).

This audit adjudicates the operator convention and the numerical pin. It does
not close the separate \(\det(1-K_s)\ne0\) divisor gate required to promote a
zero of a sector Fredholm determinant to a zero of the Selberg quotient away
from the critical line (MMS Theorem 6.4; extraction lines 26–37; adversarial
review §4.1).

## Source corrections and scope

The fetched primary source is Mayer–Mühlenbruch–Strömberg, “The transfer
operator for the Hecke triangle groups,” arXiv:0912.2236:
<https://arxiv.org/abs/0912.2236>.

The supplied extraction is useful but has two transcription errors that matter
for this audit:

1. Its lines 13–37 label the Selberg quotient/factorization as “eq. (34).”
   In the paper, the reduced odd-\(q\) operator is printed as eq. (34), while
   the quotient/factorization is Theorem 6.4. The extraction's displayed
   reduced operator at lines 108–122 is the relevant eq. (34).
2. Its lines 145–161 write the odd-\(q\) relation as if
   \(h_q=(q-2)/2\), then obtain contradictory values for \(q=5\). For odd
   \(q\ge5\), the paper's eq. (34) context is \(q=2h_q+3\); hence \(q=5\)
   has \(h_q=1\), \(\kappa_q=2h_q+1=3\). The extraction's line 122 has the
   correct \(q=5\) values; line 159 does not.

No sign or exponent ambiguity remains after using the paper's printed p. 20–21
definitions following eq. (34). The source does not, however, prescribe the
code's numerical \`safety=5/2\` disc enlargement; that is an implementation
domain choice and remains a separate domain-nesting verification item.

## 1. MMS derivation for \(q=5\)

### 1.1 Markov cells and domains

MMS defines \(\lambda_q=2\cos(\pi/q)\) (paper eq. (3)); thus
\(\lambda_5=(1+\sqrt5)/2\). For odd \(q=2h_q+3\), the positive Markov
boundaries are the finite \(\lambda_q\)-CF orbit in paper eqs. (30)–(31),
with cells \(\Phi_i=[\phi_{i-1},\phi_i]\) from eq. (13). At \(q=5\),

\[
\begin{aligned}
\phi_0&=-\lambda_5/2=-0.8090169943749475,\\
\phi_1&=[\![0;1]\!]=-1/\lambda_5=-0.6180339887498948,\\
\phi_2&=[\![0;2,1]\!]=-0.38196601125010515,\\
\phi_3&=0.
\end{aligned}
\]

Therefore the reduced positive components are
\(g_1\) on \(\Phi_1\), \(g_2\) on \(\Phi_2\), and \(g_3\) on \(\Phi_3\), with
\(\Phi_{-i}=-\Phi_i\) in the unreduced space (MMS eq. (13), eqs. (30)–(31),
and §4.2; paper pp. 8–9, 17–18).

MMS does not select one numerical disc radius. Lemma 4.4 requires open discs
\(D_i\) with \(\Phi_i\subset D_i\) and
\(\vartheta_n(D_i)\subset D_j\) for every transition
\(n\in N_{i,j}\); it obtains them by first choosing real intervals \(I_i\)
and taking the discs centered on the real axis whose real intersections are
those intervals (MMS Lemma 4.4 and eq. (28), paper p. 16). For odd \(q\), the
pre-perturbation interval templates are given in Lemma 4.9 and the final
choices after enlargement are, for \(q=5\),

\[
\begin{aligned}
I_1&=([\![-1;1,-2,-1,n_1]\!],\lambda_5/4),\\
I_2&=([\![-1;-1,n_2]\!],\lambda_5/4),\\
I_3&=([\![-1;-1,-2,-1,n_3]\!],\lambda_5/4),
\end{aligned}
\]

with the stated sufficiently-large/order constraints on the \(n_i\), and
\(I_{-i}=-I_i\) (MMS Lemma 4.9 and the final paragraph of its Lemma 4.4
proof, paper p. 18).

The two code paths instead use the convenient numerical discs
\(D_i^{\rm code}=\{|z-c_i|<\rho_i\}\), where

\[
c_i=(\phi_{i-1}+\phi_i)/2,
\qquad
\rho_i=(5/2)(\phi_i-\phi_{i-1})/2.
\]

They are

\[
c=(-0.7135254915624212,-0.5,-0.19098300562505258),
\]

\[
\rho=(0.23872875703131582,0.29508497187473703,0.4774575140626314).
\]

This matches the code and the Sonnet metadata
(\`zeta_mayer_rosen.py:161–206\`,
\`zeta_cert_rosen_q5.py:127–154\`,
\`collocation_even_sonnet.py:84–108\`). The
factor \(5/2\) is not an MMS convention; it is a numerical domain/basis
choice.

### 1.2 Branch maps, weights, and tails

MMS's inverse branch is

\[
\vartheta_n(z)=-\frac1{z+n\lambda_q}
\]

for the positive-index family (paper eq. (19)). Its derivative is
\(\vartheta_n'(z)=(z+n\lambda_q)^{-2}\), so the transfer weight is
\((z+n\lambda_q)^{-2s}\), written by MMS as the squared-denominator form
\(((z+n\lambda_q)^2)^{-s}\) in eqs. (26)–(27).

For the negative-index operators that actually occur in the reduced formula,
MMS explicitly gives the post-eq. (34), p. 21 convention

\[
\vartheta_{-n}(z)=+\frac1{z-n\lambda_q},
\qquad
L_{-n,s}g(z)=((z-n\lambda_q)^2)^{-s}
g\!\left(\frac1{z-n\lambda_q}\right).
\]

The same formula summed over \(l\ge n\) defines \(L^\infty_{-n,s}\). This is
the negative-index display transcribed at extraction lines 67–72; it is the
paper's unnumbered continuation immediately after eq. (34), together with
the single/tail definitions in eqs. (26)–(27). The squared form is material:
using \((z-n\lambda_q)^{-2s}\) as a plain principal power would introduce a
phase on the negative real branch and is not the MMS convention (MMS p. 20,
the branch-power convention in the proof of Lemma 5.1).

For \(q=5\), Lemma 4.2 gives the transition sets

\[
\begin{array}{c|c}
\text{transition}&N_{i,j}\\ \hline
1\to2&\{2\}\\
1\to-2&\{-1\}\\
1\to3&\mathbb Z_{\ge3}\\
1\to-3&\mathbb Z_{\le-2}\\
2\to-2&\{-1\}\\
2\to3&\mathbb Z_{\ge2}\\
2\to-3&\mathbb Z_{\le-2}\\
3\to1&\{1\}\\
3\to-2&\{-1\}\\
3\to3&\mathbb Z_{\ge2}\\
3\to-3&\mathbb Z_{\le-2}.
\end{array}
\]

This is Lemma 4.2 specialized using \(h_5=1,\kappa_5=3\). It explains why
the \(L_{-1,s}\) terms are single branches, while
\(L^\infty_{3,s}\), \(L^\infty_{2,s}\), and \(L^\infty_{-2,s}\) are tails
(paper Lemma 4.2, pp. 14–15; extraction lines 108–122).

### 1.3 The \(3\times3\) mms+ operator

MMS defines \(P f\) by \((Pf)_i(z)=f_{-i}(-z)\), and \(P f=+f\) is the
\(P\)-symmetric sector (paper §5.1; extraction lines 75–102). Specializing
printed eq. (34) to \(q=5\), \(h=1\), \(\kappa=3\), gives

\[
\begin{aligned}
(L_{s,+}g)_1={}&L_{2,s}g_2+L^\infty_{3,s}g_3
                 +L_{-1,s}g_2+L^\infty_{-2,s}g_3,\\
(L_{s,+}g)_2={}&L^\infty_{2,s}g_3
                 +L_{-1,s}g_2+L^\infty_{-2,s}g_3,\\
(L_{s,+}g)_3={}&L_{1,s}g_1+L^\infty_{2,s}g_3
                 +L_{-1,s}g_2+L^\infty_{-2,s}g_3.
\end{aligned}
\]

Equivalently, in block-matrix form with columns/rows \(g_1,g_2,g_3\),

\[
L_{s,+}=\begin{pmatrix}
0 & L_2+L_{-1} & L^\infty_3+L^\infty_{-2}\\
0 & L_{-1} & L^\infty_2+L^\infty_{-2}\\
L_1 & L_{-1} & L^\infty_2+L^\infty_{-2}
\end{pmatrix},
\]

where the \(s\) subscript is suppressed in the matrix. The \(P\)-antisymmetric
operator is obtained by changing only the signs in front of the negative-index
terms; it is not obtained by changing \(1-L\) to \(1+L\) (MMS printed
eq. (34), paper p. 20; Theorem 6.4).

## 2. Certified-engine audit

### 2.1 \`code/zeta_mayer_rosen.py\`

| Choice | Source requirement | Implementation and result |
|---|---|---|
| \(q=5\) geometry | \(\lambda_q\) from paper eq. (3); odd-\(q\) cells from eqs. (13), (30)–(31) | \`hecke_params\`, \`partition_points\`, \`disc_centers\`, and \`disc_radii\` at lines 150–206 give \(\lambda_5\), \(h=1\), \(\kappa=3\), the three cells, midpoint centers, and the stated \(5/2\) numerical radius. **MATCH**, with the radius scale noted as a code choice. |
| Positive branch | MMS eqs. (19), (26), (27) | \`_atomic_block\` lines 237–238 uses \`-1/(z+n*lam)\`. **MATCH.** |
| Negative branch | Post-eq. (34) p. 21 negative-index display, with eqs. (26)–(27) for the weight | \`_atomic_block\` lines 239–241 uses \`+1/(z-n*lam)\`. **MATCH.** |
| Weight/exponent | MMS eqs. (26)–(27), p. 20 squared-power convention | Lines 242–245 use \`(denom*denom)**(-s)\` for both signs. **MATCH.** This avoids the negative-branch phase error. |
| Tail populations | Lemma 4.2 and eq. (34) | Lines 344–346 correctly distinguish the single \(L_{-1}\) from the \(L^\infty_2,L^\infty_3,L^\infty_{-2}\) tails. **MATCH.** |
| q=5 block placement | Printed eq. (34) | Lines 347–361 place all three rows exactly as the displayed \(L_{s,+}\) above. **MATCH.** |
| Sector sign | \(P f=\pm f\), paper §5.1 and eq. (34) | \`sign=+1\` is multiplied only into the negative-index terms; \`sign=-1\` gives mms−. Lines 293–300 and 347–361. **MATCH.** The module's older “even/odd” wording is a label issue; its lines 68–84 correctly warn that these are not Maass parity sectors. |
| Conjugation | MMS defines \((Pf)_i(z)=f_{-i}(-z)\), with no complex conjugate (paper §5.1; extraction lines 78–95) | No \(\overline z\), \(\overline s\), or conjugation of function values is inserted in the branch or block builder. The code implements the analytic argument \(-z\) only through the negative-index reduction. **MATCH.** |
| Determinant sign | MMS Theorem 6.4 | \`reduced_det\` lines 370–374 computes \`det(1-M)\`. **MATCH.** |

The one numerical qualification is the tail. \`zeta_mayer_rosen.py\` lines
257–290 closes the remaining tail with a leading Euler–Maclaurin power term,
whereas the Arb module below evaluates the Hurwitz-zeta tail exactly. That is
a truncation/accuracy distinction, not a sign, block, branch, or exponent
convention distinction (MMS eqs. (26)–(27); certified implementation lines
215–260).

### 2.2 \`code/zeta_cert_rosen_q5.py\`

The Arb implementation agrees with the same source choices:

- \`partition_points_ball\`, \`disc_centers_ball\`, and \`disc_radii_ball\` at
  lines 127–154 reproduce the \(q=5\), \(h=1\), \(\kappa=3\) geometry and the
  same numerical radius choice (MMS eqs. (13), (30)–(31), Lemma 4.4).
- \`_single_block_allcols\` at lines 270–288 uses the positive map
  \(-1/(z+n\lambda)\), and the negative map \(+1/(z-n\lambda)\), with
  \`(denom*denom)**(-s)\` at lines 275–282 (MMS eqs. (19), (26)–(27), and the
  post-eq. (34) negative-index display).
- \`_tail_block_allcols\` at lines 291–318 uses \(a_0=n+z/\lambda\) for the
  positive tail and \(a_0=n-z/\lambda\) for the negative tail, with the common
  per-moment factor \((-1/\lambda)^m\). This is the binomial expansion of the
  two MMS branches, and the squared denominator is preserved (MMS eqs. (26)–
  (27); paper p. 21).
- \`build_reduced_matrix_ball\` at lines 328–391 places the exact q=5 eq. (34)
  blocks. The caller-supplied \`sign\` is applied only to the negative-index
  \(L_{-1}\) and \(L^\infty_{-2}\) blocks, exactly as MMS eq. (34) requires.
- The (P)-reduction is an index/argument reflection, not complex conjugation:
  the q5 builder has no conjugation operation on (z), (s), or function
  values. This matches MMS §5.1's ((Pf)_i(z)=f_{-i}(-z)) definition.
- \`_det_block\` at lines 400–412 again computes \(\det(1-L)\), not
  \(\det(1+L)\), as required by Theorem 6.4.

The file's executable \`main\` is an mms−/odd-sign production driver (lines
831–835), so that driver does not itself claim to certify the flagship mms+
pin. The generic builder is sign-parametric, and the off-line G5 caller uses
\`sign=+1\`; the N=22 direct call below confirms that the builder's mms+ route
has the flagship zero.

## 3. Sonnet crosscheck audit and exact divergence

\`results_sonnet.json\` is generated by
\`projects/g5-crosscheck/collocation_even_sonnet.py\` (the file itself names
that output path and the three target pins). Its declared sign and block
convention are correct: \`SIGN_EVEN=+1\` at lines 54–63, the positive/negative
maps and squared weight are at lines 153–168, and the three-row block assembly
at lines 235–266 is a literal transcription of MMS eq. (34). The partition
points, centers, and radii in lines 84–108 also agree with the certified
geometry.

The divergence is in the collocation coordinate, not in MMS's \(+/-\) sign:

1. \`collocation_nodes_and_coeffs\` constructs Lagrange polynomials \(p_b(u)\)
   with nodes on the unit circle, but the physical output nodes are
   \(z=c_i+0.5\rho_i u\) (lines 119–133 and 157).
2. \`single_branch_block\` evaluates those polynomials at
   \`x_arg=(arg-c_j)/r_j\` (line 166), although the nodal coordinate for the
   input basis is \`(arg-c_j)/(0.5*r_j)\`.
3. \`tail_closed_block\` repeats the same mismatch: it constructs the polynomial
   response with \`h[k]=.../(r_j**k)\` (lines 209–216), while its Lagrange
   basis was fitted on the half-radius nodes.

Thus the current Sonnet matrix is not a representation of the same operator
in a different basis. It is a different finite matrix induced by a factor-of-
two input-coordinate mismatch. Replacing each input normalization by
\`radius_scale*r_j\` makes the Sonnet collocation agree with the certified pin
at N=22. The separate \`g5_check_run.py\`/Fable path uses full-radius nodes and
full-radius normalization (e.g. lines 116–126 of that file), so it does not
have this particular half-radius mismatch.

## 4. N=22 determinant confirmation

Command run:

    /Users/za/.venvs/farey-rh/bin/python code/convention_audit/evaluate_n22.py

The certified column is the midpoint of the raw finite Arb determinant
\(\det(I-L_{22})\), with \(n_{\rm head}=4\) and \`sign=+1\`; it is not inflated
by the separate dimension-tail ball. The Sonnet column is the current
float64/30-digit-mpmath collocation determinant at \(N=22\).

| Evaluation | at \(0.45389518+5.76353724i\) | at \(0.43318010+5.67574682i\) |
|---|---:|---:|
| MMS-correct Arb builder, mms+ | \(6.8214825634\times10^{-9}\) | \(3.5542639061\times10^{-1}\) |
| Current Sonnet collocation | \(3.3426510728\times10^{-1}\) | \(6.4605149645\times10^{-9}\) |
| Sonnet after the radius-coordinate correction | \(6.4984137663\times10^{-9}\) | \(3.5542639041\times10^{-1}\) |

The first two rows are the requested four values: each implementation's
current finite determinant vanishes only at its own pin. The third row is the
minimal diagnostic correction and identifies the exact cause of the apparent
convention disagreement.

## 5. Final adjudication

**MMS-correct convention:** \(P\)-symmetric/mms+, \`sign=+1\`, with the eq. (34)
block placement, \(\vartheta_n=-1/(z+n\lambda)\),
\(\vartheta_{-n}=+1/(z-n\lambda)\), squared derivative weight
\(((z\pm n\lambda)^2)^{-s}\), and \`det(1-L)\`.

**Certified engine:** matches all of those choices. Its headline pin is the
MMS-correct numeric pin \(0.45390+5.76354i\).

**Sonnet implementation:** its stated \(+1\) sector convention is also the
MMS convention, but its half-radius nodal basis is mis-normalized. The
\(0.43318+5.67575i\) value is therefore not a competing MMS theorem value and
should not be carried forward as an even-sector convention correction.

**Remaining UNRESOLVED items:** MMS leaves the admissible disc enlargement
noncanonical, so the code's \`5/2\` radius needs a standalone nesting proof if
it is part of a rigorous certificate; and the off-line Selberg interpretation
still needs the \(K_s\) divisor nonvanishing check. Neither unresolved item
changes the convention adjudication or the N=22 pin selection.

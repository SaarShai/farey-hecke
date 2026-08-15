# M1 — Operator-level zeta-factor split attempt for (q=4,6)

**Ticket:** `m1-derivation-draft`
**Scope:** arithmetic Hecke groups (G_4,G_6), MMS transfer operator, (P)-symmetric sector.
**Status convention:** every substantive step below is tagged exactly `PROVED`, `CITED`, or `GAP`.

**[GAP] Candidate identities.** This note tests the requested identities

\[
D_4(s):=\det(1-\mathcal L^{(4)}_{s,+})
 \stackrel{?}{=}\zeta(2s)R_4(s),
\qquad
D_6(s):=\det(1-\mathcal L^{(6)}_{s,+})
 \stackrel{?}{=}\zeta(2s)R_6(s).
\]

**[GAP] Target status.** The arithmetic surfaces are related to the modular
surface by commensurability, but the missing question is whether that relation
has been realized as a determinant-preserving induction/intertwining for the
particular MMS (P)-symmetric operators displayed below.

## 1. What MMS actually gives

**[CITED] MMS starting theorem.** Mayer–Mühlenbruch–Strömberg, “The transfer
operator for the Hecke triangle groups,” *Discrete and Continuous Dynamical
Systems* 32 (2012), 2453–2484, arXiv:0912.2236: Theorem 4.10 gives the
meromorphic nuclear transfer-operator family \(\mathcal L_s\); §5.1 and
Lemma 5.1 define the involution

\[
(P\underline f)_i(z)=f_{-i}(-z)
\]

and state \(P\mathcal L_s=\mathcal L_sP\); equations (32), (33), (34)
give the reduced operators; and Theorem 6.4 gives

\[
Z_{S,q}(s)
 =\frac{\det(1-\mathcal L_s)}{\det(1-\mathcal K_s)}
 =\frac{\det(1-\mathcal L_{s,+})\det(1-\mathcal L_{s,-})}
        {\det(1-\mathcal K_s)}.
\tag{MMS-6.4}
\]

Here (+) and (-) mean the (P)-symmetric and (P)-antisymmetric
Markov-partition sectors. They are not, without another theorem, the
geometric even/odd Maass-parity sectors.

**[PROVED] Algebra of the MMS sector split.** Since \(P^2=1\), define

\[
P_+=\frac{1+P}{2},\qquad P_- =\frac{1-P}{2}.
\]

Then every \(f\) has the unique decomposition \(f=P_+f+P_-f\), with
\(P_+f\in B_+\) and \(P_-f\in B_-\). If \(P\mathcal L_s=\mathcal L_sP\), then
\(\mathcal L_sP_\pm=P_\pm\mathcal L_s\), so both \(B_+\) and \(B_-\) are
invariant. Thus \(\mathcal L_s=\mathcal L_{s,+}\oplus\mathcal L_{s,-}\).
For a nuclear operator,

\[
\operatorname{tr}(\mathcal L_s^n)
 =\operatorname{tr}(\mathcal L_{s,+}^n)
  +\operatorname{tr}(\mathcal L_{s,-}^n).
\]

Substitution into
\(
\det(1-A)=\exp(-\sum_{n\ge1}\operatorname{tr}(A^n)/n)
\)
first in a convergent half-plane and then by meromorphic continuation gives
\(
\det(1-\mathcal L_s)=\det(1-\mathcal L_{s,+})\det(1-\mathcal L_{s,-})
\).
This proves the sector product, but it proves no Riemann-zeta factor.

## 2. The exact q=4 and q=6 MMS operators

**[CITED] Branches and Markov data.** MMS equation (3) defines
\(\lambda_q=2\cos(\pi/q)\); equation (19) uses
\(
\vartheta_n(z)=-1/(z+n\lambda_q)
\);
equations (26)–(27) define the single-branch and tail blocks
\(L_{n,s},L^\infty_{n,s}\), with the negative-index convention printed
immediately after equation (34). The Markov cells and their
\(\lambda_q\)-continued-fraction boundaries are in §2.6, equation (13), and
equations (30)–(31). The discs \(D_i\) are chosen as in Lemma 4.4; no
particular numerical enlargement is part of the theorem.

**[PROVED] Arithmetic parameters.** Directly,

\[
\lambda_4=2\cos(\pi/4)=\sqrt2,\quad \lambda_4^2=2,
\qquad
\lambda_6=2\cos(\pi/6)=\sqrt3,\quad \lambda_6^2=3.
\]

**[CITED] Even-q partition data.** MMS §2.6, equation (13), together with
equations (30)–(32), states that for even \(q=2h_q+2\), the partition has
\(h_q=\kappa_q=(q-2)/2\) and boundaries
\(\phi_i=[\![0;1^{h_q-i}]\!]\), with \(\phi_0=-\lambda_q/2\) and
\(\phi_{h_q}=0\).

**[PROVED] Arithmetic parameter substitution.** Directly,

for (q=4), (h_4=1), so the cited boundary formula gives
(phi_0=-sqrt2/2) and (phi_1=0). For (q=6), (h_6=2), so it gives
(phi_0=-sqrt3/2), (phi_1=-1/lambda_6=-1/sqrt3), and
(phi_2=0). Taking consecutive boundary intervals gives exactly the cells
in the table:

\[
\begin{array}{c|c|c|c}
q&h_q=\kappa_q&\text{boundaries}&\text{cells}\\ \hline
4&1&-\sqrt2/2,\ 0&\Phi_1=(-\sqrt2/2,0)\\
6&2&-\sqrt3/2,\ -1/\sqrt3,\ 0
  &\Phi_1=(-\sqrt3/2,-1/\sqrt3),\ \Phi_2=(-1/\sqrt3,0).
\end{array}
\]

Thus \(G_4\) has one reduced holomorphic component and \(G_6\) has two.

**[CITED] Even-q block formula.** MMS equation (32), for
\(q=2h_q+2\), is

\[
\begin{aligned}
(\mathcal L_{s,\pm}g)_1
  &=L^\infty_{2,s}g_{h_q}\ \pm L^\infty_{-1,s}g_{h_q},\\
(\mathcal L_{s,\pm}g)_i
  &=L_{1,s}g_{i-1}+L^\infty_{2,s}g_{h_q}
       \ \pm L^\infty_{-1,s}g_{h_q},
       &&2\le i\le h_q.
\end{aligned}
\tag{MMS-32}
\]

The sign multiplies the negative-index blocks only. This is the even-q
formula required for both \(q=4\) and \(q=6\); MMS equation (34) is the
different odd-q formula and is not used for these two groups.

**[PROVED] q=4 specialization.** With \(h_4=\kappa_4=1\), equation
(MMS-32) has one row and gives

\[
\mathcal L^{(4)}_{s,+}
 =L^\infty_{2,s}+L^\infty_{-1,s}
 :B(D_1)\longrightarrow B(D_1).
\tag{4+}
\]

Consequently the exact candidate determinant is
\[
D_4(s)=\det_{B(D_1)}
\left(1-L^\infty_{2,s}-L^\infty_{-1,s}\right).
\]

**[PROVED] q=6 specialization.** Put
\(
A_{i,s}:B(D_2)\to B(D_i),
\quad A_{i,s}:=L^\infty_{2,s}+L^\infty_{-1,s}
\)
where the source and target discs are those of row \(i\). With
\(h_6=\kappa_6=2\), (MMS-32) becomes

\[
\mathcal L^{(6)}_{s,+}
 =
 \begin{pmatrix}
  0 & A_{1,s}\\
  L_{1,s}:B(D_1)\to B(D_2) & A_{2,s}
 \end{pmatrix}
 :B(D_1)\oplus B(D_2)\to B(D_1)\oplus B(D_2).
\tag{6+}
\]

Hence
\[
D_6(s)=\det_{B(D_1)\oplus B(D_2)}(1-\mathcal L^{(6)}_{s,+}).
\]

**[GAP] Where the zeta factor could enter.** Nothing in (4+) or (6+)
contains an integer-translation Gauss branch term by inspection; the desired
zeta factor, if present, must come from an induced/quotient reorganization of
the full branch system.

## 3. What arithmetic commensurability contributes

**[PROVED] The \(\lambda_q^2=N\) conjugation.** Let
\[
D_N=\begin{pmatrix}N^{1/4}&0\\0&N^{-1/4}\end{pmatrix},
\quad
T_\lambda=\begin{pmatrix}1&\sqrt N\\0&1\end{pmatrix},
\quad
S=\begin{pmatrix}0&-1\\1&0\end{pmatrix}.
\]
Multiplying the matrices gives

\[
D_N^{-1}T_\lambda D_N
 =\begin{pmatrix}1&1\\0&1\end{pmatrix}=T,
\qquad
D_N^{-1}SD_N
 =\begin{pmatrix}0&-N^{-1/2}\\N^{1/2}&0\end{pmatrix}=W_N.
\]

For \(q=4\), \(N=2\); for \(q=6\), \(N=3\). Therefore, after conjugation,
the two Hecke generators become the modular translation \(T\) and the Fricke
involution \(W_N\). This calculation explains the arithmetic square roots,
but by itself it is only a statement about group generators, not transfer
operators.

**[CITED] Common modular commensurability.** Takeuchi, “Arithmetic triangle
groups,” *Journal of the Mathematical Society of Japan* 29 (1977), 91–106,
Theorem 3 in §5 and the remark following the noncompact list, classifies the
noncompact arithmetic triangle types and places \((2,3,\infty)\),
\((2,4,\infty)\), and \((2,6,\infty)\) in the modular commensurability class.
Thus \(G_4\) and \(G_6\), after the conjugation above, are the Fricke
overgroups usually denoted \(\Gamma_0^+(2)\) and \(\Gamma_0^+(3)\).
The index-two statement is with their congruence subgroups
\(\Gamma_0(2)\) and \(\Gamma_0(3)\), respectively; it is not an assertion
that \(G_4\) or \(G_6\) is literally an index-two subgroup of
\(\mathrm{PSL}(2,\mathbb Z)\).

**[PROVED] What finite-index induction would give if supplied.** Suppose a
transfer operator \(\mathcal T_{q,s}\) for the common subgroup is written on
a finite-dimensional coset module and a finite-order symmetry \(Q\) commutes
with it. If \(Q^2=1\), the projections \((1\pm Q)/2\) give invariant blocks
\(\mathcal T_{q,s,\pm}\). The same trace proof as in §1 gives

\[
\det(1-\mathcal T_{q,s})
 =\det(1-\mathcal T_{q,s,+})\det(1-\mathcal T_{q,s,-}).
\]

More generally, if an invertible intertwiner \(U_q\) produced a block
triangular form

\[
U_q^{-1}\mathcal L^{(q)}_{s,+}U_q
 =\begin{pmatrix}
 \mathcal G_{s}^{\mathrm{mod}}&C_{q,s}\\
 0&\mathcal R_{q,s}
 \end{pmatrix},
\tag{I_q}
\]

then powers of this matrix are block triangular with diagonal blocks
\((\mathcal G_s^{\mathrm{mod}})^n\) and \(\mathcal R_{q,s}^n\). The trace
exponential therefore proves

\[
\det(1-\mathcal L^{(q)}_{s,+})
 =\det(1-\mathcal G_s^{\mathrm{mod}})
  \det(1-\mathcal R_{q,s}).
\]

This is the precise operator mechanism needed: the zeta factor must be the
determinant of an actual modular block, not merely a consequence of group
commensurability.

**[CITED] Fraczek–Mayer symmetry template.** Fraczek–Mayer, “Symmetries of
the transfer operator for \(\Gamma_0(N)\) and a character deformation of the
Selberg zeta function for \(\Gamma_0(4)\),” *Algebra & Number Theory* 6
(2012), 587–610, arXiv:1011.4441, §2, Theorem 2.0.1 and Theorem 2.1.1,
constructs the vector-valued modular transfer operator, permutation symmetries
\(P^2=1\), and reduced Fredholm-determinant factors. Their symmetry is a
finite coset/permutation operator; the theorem is for modular congruence
groups and their characters.

**[GAP] No MMS-to-Fraczek–Mayer intertwiner is present.** The conjugation
\(D_N\) changes the group generators, but it does not identify the MMS
Markov-partition Banach space \(B(D_1)\) or \(B(D_1)\oplus B(D_2)\) with the
finite-coset modular Banach space in Fraczek–Mayer. In particular, the needed
map would have to prove all of the following at once:

1. a slow/fast induction or first-return construction taking the nearest
   \(\lambda_q\)-multiple map to the modular integer-translation map;
2. equality of the branch weights, including the (2s)-Jacobian cocycle,
   after the return-word regrouping;
3. compatibility of the return-word coset action with the MMS reflection
   \(f_i(z)\mapsto f_{-i}(-z)\); and
4. determinant preservation, including the one overcounted orbit represented
   by \(\mathcal K_s\) in MMS Theorem 6.4.

Neither the MMS paper nor Fraczek–Mayer supplies this cross-identification for
the \(G_4/G_6\) MMS operators. The integer values \(\lambda_4^2=2\) and
\(\lambda_6^2=3\) make the construction plausible, but they do not prove it.

## 4. The candidate zeta split and its exact burden

**[CITED] Modular anchor.** Mayer, “The thermodynamic formalism approach to
Selberg’s zeta function for \(\mathrm{PSL}(2,\mathbb Z)\),” *Bulletin of the
AMS* 25 (1991), 55–60, Theorem 2, proves the modular Gauss-map relation

\[
Z_{S,\mathrm{PSL}_2(\mathbb Z)}(s)
 =\det(1-\mathcal G_s)\det(1+\mathcal G_s).
\]

Lewis–Zagier, “Period functions for Maass wave forms. I,” *Annals of
Mathematics* 153 (2001), 191–258, §4, equations (4.20)–(4.22), records the
meromorphic Gauss transfer family, its Fredholm determinants, and the
modular Selberg/zeta-zero connection. This is the (q=3) anchor. It is not a
published (q=4) or (q=6) identity for the MMS (P)-symmetric block.

**[GAP] Zeta normalization.** The cited modular theorem directly identifies a
Selberg-zeta determinant, whereas (C4) and (C6) use the proposed Riemann-zeta
factor \(\zeta(2s)\). A normalization/scattering calculation, including any
elementary Euler factors, is still required to identify those two notions in
the intended remainder \(R_q\). Thus the symbol \(\zeta(2s)\) in this draft is
a candidate factor, not a consequence of the modular citation.

**[PROVED] Formal quotient criterion.** Let \(D(s)\) be meromorphic and let
\(Z(s)=\zeta(2s)\). On any open set where \(Z(s)\ne0\), define
\(R(s)=D(s)/Z(s)\); then \(D(s)=Z(s)R(s)\) by multiplication. At a zero
\(s_0\) of \(Z\), write locally
\[
Z(s)=(s-s_0)^m z_0(s)
\]
with \(z_0(s_0)\ne0\), and write
\[
D(s)=(s-s_0)^a d_0(s),
\]
where \(a=\operatorname{ord}_{s_0}D\in\mathbb Z\) and
\(d_0(s_0)\ne0\); a pole means \(a<0\). Then
\[
R(s)=(s-s_0)^{a-m}d_0(s)/z_0(s)
\]
extends holomorphically through \(s_0\) exactly when \(a\ge m\). Hence an
operator-level “\(\zeta(2s)\) factor” requires not just numerical zeros of
\(D_q\) at several points, but every relevant zeta zero with at least the
correct multiplicity and a globally defined meromorphic/holomorphic
remainder.

**[GAP] Explicit candidate for q=4 and q=6.** The desired statements are

\[
\boxed{
\det\!\left(1-L^\infty_{2,s}-L^\infty_{-1,s}\right)
 =\zeta(2s)R_4(s)}
\tag{C4}
\]

and

\[
\boxed{
\det\!\left[
1-
\begin{pmatrix}
0&A_{1,s}\\ L_{1,s}&A_{2,s}
\end{pmatrix}
\right]
 =\zeta(2s)R_6(s)}.
\tag{C6}
\]

The missing proof is an explicit \(U_4\) or \(U_6\) satisfying (I\(_q\))
whose first diagonal block is the modular zeta/scattering block. The proof
must also decide whether elementary local Euler factors belong to the stated
zeta factor or to \(R_q\), and must track zero multiplicities.

MMS Theorem 6.4 adds a separate divisor condition whenever the argument is
phrased through \(Z_{S,q}\): the factor \(\det(1-\mathcal K_s)\) removes a
doubly counted orbit. A zero of a reduced determinant cannot automatically
be promoted to a zero of the Selberg quotient without locating or excluding
that divisor at the same \(s\). The current lane files contain no symbolic
q=4/q=6 computation of this \(\mathcal K_s\) divisor.

**[GAP] Numerical controls do not close the factorization.** The companion
file `M2_NONFACT_WITNESSES.md` records a q=4 finite-(N) evaluation consistent
with zero at the first modular zeta point, and the lane-b control report
records q=4/q=6 line pins. Those are useful positive controls for the
implementation, but finitely many point evaluations establish neither the
global quotient \(R_q\), the multiplicity condition, nor the missing
MMS-to-modular intertwiner.

## 5. Honest endpoint

**[GAP] Reachability with current machinery.** The exact q=4 and q=6 MMS
operators, their Markov components, the (P)-sector determinant product, the
arithmetic conjugation, and the Fraczek–Mayer symmetry template are all
available. The requested identities (C4) and (C6) are not reachable as
proved operator factorizations from those ingredients alone. The current
machinery supports the expectation that the arithmetic surfaces inherit the
modular zeta/scattering divisor, but it does not supply the determinant-level
split of the MMS (P)-symmetric block.

The single hardest gap is:

> Construct and prove a determinant-preserving slow/fast induction intertwiner
> from the q=4/q=6 MMS (P)-symmetric Markov operator to a finite-state modular
> transfer operator, with the modular zeta/scattering block isolated and the
> MMS (\mathcal K_s) overcounting divisor tracked.

Until that intertwiner exists, “q=4 and q=6 carry the same ζ song” is a
well-motivated arithmetic expectation and a numerical control observation,
not an operator-level factorization theorem.

## References used

**[CITED]** Mayer–Mühlenbruch–Strömberg (2012), arXiv:0912.2236,
Theorem 4.10, Lemma 5.1, equations (3), (13), (19), (26)–(34), Theorem 6.4.

**[CITED]** Takeuchi (1977), “Arithmetic triangle groups,” *J. Math. Soc.
Japan* 29, 91–106, Theorem 3 §5 and the noncompact commensurability remark.

**[CITED]** Fraczek–Mayer (2012), arXiv:1011.4441, §2, Theorems 2.0.1 and
2.1.1.

**[CITED]** Mayer (1991), “The thermodynamic formalism approach to Selberg’s
zeta function for \(\mathrm{PSL}(2,\mathbb Z)\),” *Bull. AMS* 25, 55–60,
Theorem 2.

**[CITED]** Lewis–Zagier (2001), “Period functions for Maass wave forms. I,”
*Ann. Math.* 153, 191–258, §4, equations (4.20)–(4.22).

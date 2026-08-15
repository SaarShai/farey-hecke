# M1B — q=4 slow/fast intertwiner probe

**Ticket:** m1b-q4-intertwiner  
**Parent:** research_notes/rh_goals_2026-08-14/lane_g/M1_DERIVATION_DRAFT.md  
**Scope:** q=4 only; MMS \((P)\)-symmetric operator
\(\mathcal L^{(4)}_{s,+}=L^\infty_{2,s}+L^\infty_{-1,s}\)
on \(B(D_1)\).  
**Status convention:** every substantive claim below is tagged exactly
PROVED, CITED, or GAP.

## 1. q=4 branch system and a candidate first-return regrouping

**[CITED] MMS branch data.** MMS defines
\(\vartheta_n(z)=-1/(z+n\lambda_q)\) and the branch weight
\(\vartheta_n'(z)^s=(z+n\lambda_q)^{-2s}\) in the holomorphic convention.
For q=4, \(\lambda=\lambda_4=\sqrt2\), and the one-cell reduced operator is
\(L^\infty_{2,s}+L^\infty_{-1,s}\), i.e. the branch alphabet is
\[
\mathcal A:=\{n\in\mathbb Z:n\ge2\}\cup\{n\in\mathbb Z:n\le-1\}.
\]
The q=4 transition sets \(N_{1,1}=\mathbb Z_{\ge2}\) and
\(N_{1,-1}=\mathbb Z_{\le-1}\) are printed in MMS, and (26) defines the two
infinite sums \(L^\infty_{2,s}\) and \(L^\infty_{-1,s}\).
See [MMS, (19), (26), (27), and the q=4 case in the proof of Lemma 4.5](https://arxiv.org/pdf/0912.2236).

**[PROVED] Conjugated single branches.** Let
\[
D_2=\begin{pmatrix}2^{1/4}&0\\0&2^{-1/4}\end{pmatrix},
\qquad
C_n:=\begin{pmatrix}0&-1\\1&n\sqrt2\end{pmatrix}=S T_{\sqrt2}^{\,n}.
\]
With \(x=D_2^{-1}z=z/\sqrt2\),
\[
A_n:=D_2^{-1}C_nD_2=W_2T^n,
\qquad
W_2=\begin{pmatrix}0&-2^{-1/2}\\2^{1/2}&0\end{pmatrix},
\qquad
T=\begin{pmatrix}1&1\\0&1\end{pmatrix}.
\]
The induced boundary branch is therefore
\[
\widehat\vartheta_n(x)=D_2^{-1}\vartheta_nD_2(x)
       =-\frac1{2(x+n)},
\qquad
\widehat\vartheta_n'(x)=\frac1{2(x+n)^2}.
\tag{1}
\]
Thus the conjugation changes the translation parameter to an integer, but it
does not turn the branch into the ordinary \(\mathrm{PSL}(2,\mathbb Z)\) Gauss
branch \(-1/(x+n)\); it is the Fricke branch \(W_2T^n\).

**[GAP] Meaning of “slow/fast.”** MMS identifies the q=4 natural extension
with the Hecke continued-fraction dynamics, and identifies the ordinary Gauss
map only in the modular q=3 case. It does not state a q=4 first-return
conjugacy to the standard scalar Gauss map. The construction below is the
explicit candidate induced by the parity of the Fricke coset; proving that it
is conjugate to the particular finite-state modular transfer operator used in
the modular literature remains open.

**[PROVED] Candidate parity induction.** Each \(A_n=W_2T^n\) toggles the
coset parity between the congruence subgroup \(\Gamma_0(2)\) and its Fricke
extension \(\Gamma_0^+(2)=\langle\Gamma_0(2),W_2\rangle\). Adjoin a state
\(\epsilon\in\mathbb Z/2\mathbb Z\) and let one q=4 fast branch send
\(\epsilon\mapsto\epsilon+1\). The first-return section
\(\epsilon=0\) consequently has exactly the even fast words
\[
w(a,b)=A_aA_b,
\qquad
w(a,b,c,d)=A_aA_bA_cA_d,
\qquad a,b,c,d\in\mathcal A.
\tag{2}
\]
There are no first returns of fast-symbol length 1 or 3 to this section.
This is the slow/fast regrouping used below: the slow generators are the
integer parabolic \(T\) and the Fricke jump \(W_2\), while the fast symbols are
the return words \(W_2T^n\).

**[PROVED] Exact word matrices and weights through length 4.** Use the
convention that a word matrix \(A_{a_1}\cdots A_{a_r}\) represents the
composition \(\widehat\vartheta_{a_1}\circ\cdots\circ\widehat\vartheta_{a_r}\).
If \(M_w=\left(\begin{smallmatrix}A&B\\C&D\end{smallmatrix}\right)\), then
\(\widehat\vartheta_w'(x)^s=(Cx+D)^{-2s}\). The exact denominators are:

\[
\begin{array}{c|c|c|c}
 r & \text{fast word} & C_wx+D_w & \text{weight}\\ \hline
1 & (a)
   & \sqrt2(x+a)
   & [\sqrt2(x+a)]^{-2s}=2^{-s}(x+a)^{-2s}\\[2mm]
2 & (a,b)
   & 2ax+2ab-1
   & (2ax+2ab-1)^{-2s}\\[2mm]
3 & (a,b,c)
   & \sqrt2\big((2ab-1)x+2abc-a-c\big)
   & 2^{-s}\big((2ab-1)x+2abc-a-c\big)^{-2s}\\[2mm]
4 & (a,b,c,d)
   & (4abc-2a-2c)x+B(a,b,c,d)
   & \big((4abc-2a-2c)x+B(a,b,c,d)\big)^{-2s}
\end{array}
\tag{3}
\]
where
\[
B(a,b,c,d)=4abcd-2ab-2ad-2cd+1.
\]
The corresponding even-word matrices are
\[
M_{a,b}=A_aA_b
=\begin{pmatrix}-1&-b\\2a&2ab-1\end{pmatrix},
\tag{4}
\]
and
\[
M_{a,b,c,d}=A_aA_bA_cA_d
=\begin{pmatrix}
1-2bc & b+d-2bcd\\
4abc-2a-2c & 4abcd-2ab-2ad-2cd+1
\end{pmatrix}.
\tag{5}
\]
Direct multiplication gives \(\det M_{a,b}=\det M_{a,b,c,d}=1\), and the
lower-left entries in (4) and (5) are even. Hence every even word in (2)
through length 4 is an element of \(\Gamma_0(2)\), with exactly its modular
\(2s\)-Jacobian cocycle.

**[PROVED] Concrete length-1 through length-4 checks.** The first positive
and negative branches are
\[
(2):\quad \sqrt2(x+2),
\qquad
(-1):\quad \sqrt2(x-1).
\]
Representative length-2 return words give
\[
\begin{array}{c|c|c}
\text{word} & M_w & \widehat\vartheta_w'(x)^s\\ \hline
(2,2) & \left(\begin{smallmatrix}-1&-2\\4&7\end{smallmatrix}\right) &(4x+7)^{-2s}\\
(2,-1) & \left(\begin{smallmatrix}-1&1\\4&-5\end{smallmatrix}\right) &(4x-5)^{-2s}\\
(-1,2) & \left(\begin{smallmatrix}-1&-2\\-2&-5\end{smallmatrix}\right) &(-2x-5)^{-2s}\\
(-1,-1) & \left(\begin{smallmatrix}-1&1\\-2&1\end{smallmatrix}\right) &(-2x+1)^{-2s}.
\end{array}
\]
For length 3, for example,
\[
(2,2,2):\quad \sqrt2(7x+12),
\qquad
(2,2,-1):\quad \sqrt2(7x-9),
\]
so these are odd-coset, non-return words. At length 4,
\[
(2,2,2,2):
\quad
M_w=\begin{pmatrix}-7&-12\\24&41\end{pmatrix},
\quad
\widehat\vartheta_w'(x)^s=(24x+41)^{-2s},
\]
and
\[
(2,2,-1,2):
\quad
M_w=\begin{pmatrix}5&12\\-18&-43\end{pmatrix},
\quad
\widehat\vartheta_w'(x)^s=(-18x-43)^{-2s}.
\]
These computations use only \(\lambda^2=2\); no numerical approximation is
involved.

## 2. Weight compatibility and the factor at 2

**[PROVED] Even-word cocycle compatibility.** For two branches the scalar
factors cancel exactly:
\[
\begin{aligned}
&\left[\widehat\vartheta_a'\big(\widehat\vartheta_b(x)\big)
  \widehat\vartheta_b'(x)\right]^s\\
&=\left[2\left(a-\frac1{2(x+b)}\right)^2\right]^{-s}
  \left[2(x+b)^2\right]^{-s}
 =(2ax+2ab-1)^{-2s}.
\end{aligned}
\tag{6}
\]
The same chain-rule identity gives (3) for all word lengths. In particular,
the even return words have the exact modular cocycle \((Cx+D)^{-2s}\); there
is no residual universal factor \(2^{-2s}\) attached to a two-step return.

**[PROVED] Odd-word discrepancy relative to the ordinary Gauss branch.** A
one-step q=4 branch has
\[
\widehat\vartheta_n(x)=-\frac1{2(x+n)},
\qquad
\widehat\vartheta_n'(x)^s=2^{-s}(x+n)^{-2s},
\]
whereas the scalar modular branch has \((x+n)^{-2s}\). At length 2 the
denominator is \(2ax+2ab-1\), not \(x+m\) for an integer \(m\). Therefore a
direct identification with the ordinary \(\mathrm{PSL}(2,\mathbb Z)\) Gauss
operator is false already at lengths 1 and 2. This is not an obstruction to a
\(\Gamma_0^+(2)\) modular-level cocycle: \(W_2T^n\) is itself the relevant
Fricke branch, and (4)–(5) are in \(\Gamma_0(2)\).

**[PROVED] Formal imprimitive Euler factor.** If the modular normalization
uses the level-2-imprimitive Riemann factor
\[
\zeta^{(2)}(2s):=\prod_{p\ne2}(1-p^{-2s})^{-1},
\]
then the exact local relation is
\[
\zeta^{(2)}(2s)=\zeta(2s)(1-2^{-2s}).
\tag{7}
\]
Thus the only precise \(1-2^{-2s}\)-type discrepancy available at this stage
is the choice between primitive and imprimitive arithmetic normalization.

**[GAP] The q=4 Jacobian regrouping does not derive (7).** Equations
(3) and (6) show that the branch cocycle itself produces \(2^{-s}\) on an
odd Fricke branch and no scalar \(2^{-2s}\) on an even return. Neither MMS
nor the checked modular transfer-operator theorem identifies the determinant
of this q=4 branch system with \(\zeta^{(2)}(2s)\), \(\zeta(2s)\), or a
scattering determinant. Consequently (7) is an exact normalization identity,
not an operator-level Euler-factor proof.

**[CITED] The source-backed q=4 elementary correction is different.** MMS
Theorem 6.4 divides by the overcounting operator \(K_s\). For even q, MMS
identifies \(K_s=L_{1,s}^{h_q-1}L_{2,s}\); hence q=4, where \(h_4=1\), has
\(K_s=L_{2,s}\). Its q=4 multiplier is
\[
\ell=\sqrt{\frac{2-\sqrt2}{2+\sqrt2}}=\sqrt2-1,
\]
so
\[
\operatorname{spec}(K_s)=\{\ell^{2s+2m}:m=0,1,2,\ldots\},
\qquad
\det(1-K_s)=\prod_{m\ge0}
\left(1-(\sqrt2-1)^{2s+2m}\right).
\tag{8}
\]
The first elementary factor is \(1-(\sqrt2-1)^{2s}\), not
\(1-2^{-2s}\). See [MMS, Theorem 6.4 and Proposition 2](https://arxiv.org/pdf/0912.2236).

## 3. Candidate block-triangular form \((I_4)\)

**[CITED] Modular-level block available in the congruence model.** For
\(\Gamma_0(2)\), the index is \(\mu_2=2(1+1/2)=3\), and Fraczek–Mayer's
induced representation
\(\rho_2:\mathrm{PSL}(2,\mathbb Z)\to\mathrm{GL}(\mathbb C^3)\)
gives the vector-valued modular operator
\[
\mathcal M_{2,s}=\begin{pmatrix}0&M^+_{2,s}\\M^-_{2,s}&0\end{pmatrix},
\]
where
\[
(M^\pm_{2,s}f)(x)=
\sum_{m\ge1}(x+m)^{-2s}\,
\rho_2(ST^{\pm m})\,f\!\left(\frac1{x+m}\right).
\tag{9}
\]
This is the explicit finite-coset modular \(2s\)-cocycle model from
Fraczek–Mayer, equations (2.0.2)–(2.0.3), specialized to level 2. See
[Fraczek–Mayer, §2](https://arxiv.org/pdf/1011.4441).

**[GAP] Fricke-plus restriction.** The q=4 target is the Fricke overgroup,
not merely \(\Gamma_0(2)\). Formula (9) is therefore only the congruence
subgroup anchor. An explicit action of \(W_2\) on the chosen modular
cross-section, followed by a Fricke-\(+\) restriction, is still required
before (9) can be called the first diagonal block for the q=4 MMS operator.
The cited Fraczek–Mayer theorem treats finite-index subgroups of the modular
group and does not supply this MMS-to-Fricke identification.

**[GAP] Candidate \((I_4)\).** The desired form is
\[
U_4^{-1}\mathcal L^{(4)}_{s,+}U_4
=\begin{pmatrix}
\mathcal G^{\mathrm{Fr},+}_{2,s} & C_{4,s}\\
0 & \mathcal R_{4,s}
\end{pmatrix},
\tag{I_4}
\]
with
\[
U_4:B(D_1)\longrightarrow
\mathcal B_{\mathrm{mod}}\oplus\mathcal B_{\mathrm{res}}.
\]
The candidate modular diagonal block \(\mathcal G^{\mathrm{Fr},+}_{2,s}\)
is the Fricke-\(+\) restriction of the level-2 finite-coset operator whose
congruence anchor is (9). The residual diagonal block \(\mathcal R_{4,s}\)
must contain the complementary q=4 return-word data not represented by that
finite-coset model. The off-diagonal \(C_{4,s}\) is unrestricted by the
Fredholm determinant once the lower-left block is zero.

**[GAP] Diagonal blocks are not yet realized by an explicit \(U_4\).** The
word calculation identifies the required modular matrices and weights, but
does not construct an invertible map \(U_4\) between the MMS disc space and
the modular finite-coset space plus a complement. In particular, it does not
prove that the odd Fricke words, the reflection \(P\), and the MMS
overcounting divisor (8) are compatible with the same block decomposition.
Thus \(\mathcal G^{\mathrm{Fr},+}_{2,s}\) and \(\mathcal R_{4,s}\) are
explicit targets/roles in \((I_4)\), not proved diagonal blocks of
\(\mathcal L^{(4)}_{s,+}\).

## 4. Falsification duty and verdict

**[PROVED] No irrational cocycle obstruction through length 4.** The odd
words in (3) have a factor \(\sqrt2\) in their denominator, but after
raising to the \(2s\)-cocycle they contribute only the scalar \(2^{-s}\)
times an integer polynomial weight. Every even first-return word through
length 4 has an integer determinant-one matrix in \(\Gamma_0(2)\), as shown
in (4)–(5). Therefore the proposed route is not killed by a
\(\sqrt2\)-irrational obstruction at word length \(\le4\).

**[PROVED] Direct ordinary-Gauss route is falsified.** If
“integer-translation Gauss-type” is intended to mean the ordinary scalar
branch \(-1/(x+n)\), the exact length-1 mismatch is
\[
\widehat\vartheta_n(x)=-\frac1{2(x+n)},
\qquad
\widehat\vartheta_n'(x)^s=2^{-s}(x+n)^{-2s},
\]
and the exact length-2 mismatch is the denominator \(2ax+2ab-1\), which is
not \(x+m\). That narrower route is dead. The Fricke modular-level route
remains algebraically viable.

**[GAP] Remaining operator-level gap.** To complete \((I_4)\), one still has
to construct and verify: (i) a genuine q=4 slow map whose first-return coding
is the parity construction above; (ii) an explicit conjugacy from its even
return operator to the chosen finite-coset operator (9) with the Fricke-\(+\)
action; (iii) compatibility with the MMS \((P)\)-symmetric reduction; and
(iv) determinant preservation, including the separate \(K_s\) divisor (8)
and the choice between \(\zeta(2s)\) and \(\zeta^{(2)}(2s)\). No determinant
factorization or standalone \(1-2^{-2s}\) factor is claimed here.

**[GAP] Verdict — construction survives to word length 4.** The exact return
words and weights through length 4 match the appropriate
\(\Gamma_0(2)\subset\Gamma_0^+(2)\) modular cocycle, so no word-length-\(\le4\)
weight obstruction was found. The precise remaining gap is the actual
Banach-space intertwiner \(U_4\), its Fricke-\(+\) modular block, and the
determinant/scattering normalization; the source-backed correction currently
identified is (8), not \(1-2^{-2s}\).

## References

**[CITED]** D. Mayer, T. Mühlenbruch, F. Strömberg, “The transfer operator
for the Hecke triangle groups,” arXiv:0912.2236, especially (19), (26)–(27),
Lemma 4.5, Theorem 4.10, Theorem 6.4, and Proposition 2.

**[CITED]** M. Fraczek, D. Mayer, “Symmetries of the transfer operator for
\(\Gamma_0(N)\) and a character deformation of the Selberg zeta function for
\(\Gamma_0(4)\),” arXiv:1011.4441, §2, equations (2.0.2)–(2.0.3).

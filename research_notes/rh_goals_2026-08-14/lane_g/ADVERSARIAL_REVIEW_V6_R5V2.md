# ADVERSARIAL REVIEW V6 — R5 v2 compliance review
Reviewer: gpt-5.6-sol (xhigh), fresh session, read-only, 2026-08-15
~03:09-03:5x. PROVENANCE: recovered verbatim from codex rollout
(rollout-2026-08-15T03-09-13-01a004e5) by the frontier agent. No edits
beyond this header.

---

## 1. Repair (a) verification — operator binding

**Verdict: PARTIAL; not theorem-grade as written.**

The following parts are correct:

- The eleven listed families—five heads and six tails—match the certificate’s eleven rows and the per-disc builder’s eleven block calls. Compare [R5 v2, lines 18–24](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_R5_DETERMINANT_IDENTIFICATION.md:18), [TB V2, lines 140–170](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_BLOCK_CERTIFICATES_V2.md:140), and [tc_rerun.py, lines 130–145](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/tc_rerun/tc_rerun.py:130).
- \(B(D)\) is now correctly defined as the disc algebra, matching MMS’s Banach space; see [R5 v2, lines 43–47](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_R5_DETERMINANT_IDENTIFICATION.md:43).
- The squared-denominator weights agree with the engine. The engine uses
  \[
  \theta_{-n}(z)=\frac1{z-n\lambda},\qquad
  w_{-n}(z)=((z-n\lambda)^2)^{-s},
  \]
  at [zeta_cert_rosen_q5.py, lines 203–212](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/zeta_cert_rosen_q5.py:203). Because \((z-n\lambda)^2=(n\lambda-z)^2\), the weight written using \(n\lambda-z\) is equivalent under the certified branch convention. The branch-cut table proves \(\Re(n\lambda-z)>0\) for every negative row [TB V2, lines 154–170](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_BLOCK_CERTIFICATES_V2.md:154).

The exact symbol is nevertheless still ambiguous. R5 v2 first gives the correct reduced symbol \(+1/(z-n\lambda)\), then says “precisely” that the engine symbol is \(1/(n\lambda-z)\) [R5 v2, lines 32–36](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_R5_DETERMINANT_IDENTIFICATION.md:32). Those maps differ by a minus sign. The engine unambiguously implements \(+1/(z-n\lambda)\), as does the reduced operator in MMS equation (34). [MMS, pp. 21–22](https://arxiv.org/pdf/0912.2236).

There is also a source-binding weakness: the standalone engine defaults to the \(mms-\) sector and uniform factor \(2.5\), whereas the actual R2/R3b wrappers use sign \(+1\) and factors \(3.14,2.27,1.70\). The certified path itself is consistent—see [R3B report, lines 7–12](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/R3B_FLAGSHIP_CERT.md:7) and [certify_r3b_flagship.py, lines 53–60](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/tc_rerun/certify_r3b_flagship.py:53)—but R5 should bind that wrapper explicitly instead of referring generically to “the engine.”

Thus repair (a) does not satisfy the demanded *unambiguous exact operator binding*.

## 2. Repair (b) verification — \(\Omega_*\) domain

**Verdict: the domain and topology are correct; the local trace-class proof remains inaccurately stated.**

The actual R2 restriction is \(\Re s>0\). Its first-moment tail sets \(p=2\Re s\), rejects \(p\le0\), and uses exponent \(p+1=2\Re s+1\) with an integral proportional to \(1/p\) [certify_r2_flagship.py, lines 486–504](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/tb_certify/certify_r2_flagship.py:486). Therefore
\[
\Omega_*=\{\Re s>1/2\}\cup\{\Re s>0,\ \Im s>1\}
\]
is the correct proposed continuation region.

The topology is sound:

- Both pieces are connected and intersect in \(\Omega_0=\{\Re s>1/2,\Im s>1\}\).
- Every listed real pole \((1-k)/2\) has real part at most \(1/2\) and imaginary part zero, so none belongs to the union. The pole subtraction is therefore vacuous and does not disconnect it.
- From the assembly’s center and half-width [lines 125–126](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/THEOREM_G5_OFFLINE_ASSEMBLY.md:125), the box satisfies
  \[
  \Re s\in[0.4538941800749447,0.4538961800749447],\quad
  \Im s\in[5.7635362417301305,5.7635382417301305],
  \]
  hence the entire box lies in \(\{\Re s>0,\Im s>1\}\).

The Simon correction is also correct: Theorem 3.3 gives analyticity of the determinant for analytic trace-class-valued families; Theorem 3.5 concerns trace-norm continuity. [Simon, “Notes on infinite determinants”](https://www.sciencedirect.com/science/article/pii/0001870877900573).

But R5 v2 says the “deep-tail integrals carry the exponent \(k+2\sigma\)” [lines 107–113](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_R5_DETERMINANT_IDENTIFICATION.md:107). That is not the actual centered R2 envelope. The \(m=0\) term is Hurwitz-closed, and the absolute remainder is controlled by
\[
\sum_n |u_nb_n|\asymp\sum_n n^{-(2\sigma+1)},
\]
leading to
\[
b_k(s)\le A_Kq^k+C_Kk\rho^{k-1}.
\]
The R2 report explicitly warns that the full centered power does **not** have exponent \(2\sigma+k\) [R2R3 report, lines 19–29](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/R2R3_FLAGSHIP_CERT.md:19).

Consequently the \(\Omega_*\) conclusion is right, but v2 has not faithfully supplied the precise locally uniform estimate demanded by V5. It must state the \(2\sigma+1\) first-moment bound and use it to prove uniform trace-norm convergence on every compact \(K\Subset\Omega_*\).

## 3. Repair (c) verification — P-sector removal

**Verdict: CONFIRMED-SOUND structurally.**

R5 v2 no longer defines \(P\) on the reduced three-component space. It compares the already-reduced Banach and Hilbert realizations directly [R5 v2, lines 133–143](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_R5_DETERMINANT_IDENTIFICATION.md:133).

That is exactly the valid repair path identified in V5 [lines 113–125](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/ADVERSARIAL_REVIEW_V5_R5.md:113). MMS defines \(P\) on the full \(\pm i\)-indexed space and only then induces \(L_{s,\pm}\) on the positive-index reduced space. [MMS, §5.1 and equations (32)–(34)](https://arxiv.org/pdf/0912.2236).

This repair is type-correct. Its final claim that the compared operator is *exactly* \(L_{s,+}\) remains conditional on repair (a).

## 4. B-J Thm 4.2 legitimacy + bootstrap soundness

**Verdict: citation legitimate; block extension not sound as written; bootstrap core sound but incompletely closed.**

Bandtlow–Jenkinson Theorem 4.2 really states that a holomorphic map-weight system has the same dynamical determinant on every favourable holomorphic function space, including the disc algebra \(U(D)\) and Hardy \(H^2(D)\). [Bandtlow–Jenkinson, Theorem 4.2](https://arxiv.org/pdf/0802.1468).

It does not literally cover this system. Its hypotheses use scalar functions on one bounded connected domain \(D\), with all maps \(T_i:D\to D\) and \(\sum_i\|w_i\|_\infty<\infty\). R5 instead has a graph-directed operator
\[
\bigoplus_{j=1}^3 X(D_j)\longrightarrow\bigoplus_{j=1}^3X(D_j)
\]
with maps between different discs. A block/direct-sum extension is therefore required.

The proposed extension at [R5 v2, lines 84–92](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_R5_DETERMINANT_IDENTIFICATION.md:84) has two defects:

1. Tail blocks produce **countably**, not finitely, many atomic words. One must prove convergence of the word expansion in \(N_{2/3}\) on \(B\), in trace norm on \(H\), and justify exchanging trace with the countable sum.
2. The identity
   \[
   \det(I-L)=\exp\!\left(-\sum_{n\ge1}\frac{\operatorname{tr}L^n}{n}\right)
   \]
   is initially a local identity in an auxiliary scalar \(t\) for \(\det(I-tL)\); convergence at \(t=1\) is not automatic. The clean proof is equality for small \(|t|\), followed by entire continuation in \(t\) to \(t=1\).

The Jordan-chain bootstrap at [lines 93–98](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_R5_DETERMINANT_IDENTIFICATION.md:93) is algebraically correct, conditional on the asserted enlarged-disc smoothing \(L_s^H:H\to B\). For \(\lambda\ne0\),
\[
v_0=\lambda^{-1}Lv_0,\qquad
v_j=\lambda^{-1}(Lv_j-v_{j-1}),
\]
so induction places every generalized eigenvector in \(B\); conversely \(B(D)\subset H^2(D)\). This gives identical nonzero spectra and algebraic multiplicities. V5 had already validated this conditional argument [lines 30–40](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/ADVERSARIAL_REVIEW_V5_R5.md:30).

That bootstrap could replace the defective word-trace paragraph, but v2 must explicitly add the uniform tail-smoothing proof and invoke spectrality of both canonical determinants.

## 5. Reduced-sector identification with \(L_{s,+}\) / MMS Thm 6.4

**Verdict: formula-level match confirmed; exact theorem-level identification still fails as written.**

For \(q=5\), MMS has \(h_q=1\), \(\kappa_q=3\), and equation (34) gives exactly the eleven block occurrences listed in v2. The certified wrapper passes sign \(+1\), so its six negative-index blocks carry the \(+\) coefficient required for \(L_{s,+}\) [tc_rerun.py, lines 130–145](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/tc_rerun/tc_rerun.py:130). MMS Theorem 6.4 consumes precisely the determinants of those reduced \(L_{s,\pm}\). [MMS, Theorem 6.4](https://arxiv.org/pdf/0912.2236).

The invalid full-space \(P\) argument is gone, and the incidence, coefficients, weights, and certified disc geometry otherwise match.

Nevertheless, because v2 gives two opposite formulas for the reduced negative symbol, it does not uniquely define the operator it identifies with MMS \(L_{s,+}\). The branch-cut certificate cannot repair that: it controls the weight’s logarithm, whereas replacing \(1/(z-n\lambda)\) by \(1/(n\lambda-z)\) changes the composition argument itself.

Therefore the sentence “this reduced system IS \(L_{s,+}\)” [R5 v2, lines 135–141](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_R5_DETERMINANT_IDENTIFICATION.md:135) remains unsupported as an exact identity until the negative map and certified wrapper are bound explicitly.

## 6. New defects introduced by v2

V2 introduces or exposes four new defects:

1. **Sign-flipped “precise” negative symbol:** \(1/(z-n\lambda)\) and \(1/(n\lambda-z)\) are both asserted.
2. **Incorrect R2 exponent description:** \(k+2\sigma\) is substituted for the actual \(2\sigma+1\) first-moment remainder.
3. **Finite/countable word error:** the tail word expansion is described as finite.
4. **Trace-log evaluation at \(t=1\):** no convergence or auxiliary-\(t\) analytic continuation is supplied.

These are local, repairable defects; none demonstrates an obstruction to the continuation strategy.

## 7. FINAL RULING: theorem-grade NO for the full seven-link assembly

**THEOREM-GRADE NO.**

The surrounding V4 review cleared the numerical winding, determinant comparison, \(K_s\), and local MMS facts, while identifying the Hilbert-to-MMS determinant interface as the remaining gap [V4, lines 15–31](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/ADVERSARIAL_REVIEW_V4_R3B.md:15). R5 v2 still does not rigorously transport the Hilbert determinant zero produced at assembly link 4 [assembly, lines 65–68](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/THEOREM_G5_OFFLINE_ASSEMBLY.md:65) to the exact MMS \(L_{s,+}\) determinant used in Theorem 6.4 [assembly, lines 70–80](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/THEOREM_G5_OFFLINE_ASSEMBLY.md:70).

The minimal missing piece is one corrected graph-directed common-continuation lemma that:

1. Defines every certified \(L_{s,+}\) block exactly, with reduced negative map
   \[
   g\!\left(\frac1{z-n\lambda}\right),
   \qquad
   w(z)=((z-n\lambda)^2)^{-s},
   \]
   and explicitly binds sign \(+1\) and radii \(3.14,2.27,1.70\).
2. Proves \(B/H\) determinant equality on \(\Omega_0\), either through a countably summable block-word extension with auxiliary \(t\), or through enlarged-disc smoothing plus the spectral Jordan-chain argument.
3. Proves trace-class holomorphy on \(\Omega_*\) using
   \[
   b_k(s)\le A_Kq^k+C_Kk\rho^{k-1},
   \qquad
   C_K\ \text{from }\sum_n n^{-(2\inf_K\Re s+1)}.
   \]

After those clauses, the identity theorem and links 5–7 can proceed. They do not proceed theorem-gradingly from v2 as currently written. No files were changed.



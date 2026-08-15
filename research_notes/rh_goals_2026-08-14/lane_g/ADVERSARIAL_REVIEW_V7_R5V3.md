# ADVERSARIAL REVIEW V7 — R5 v3 compliance and soundness
Reviewer: gpt-5.6-sol (xhigh), fresh session, read-only, 2026-08-15
~03:30-04:3x. PROVENANCE: recovered verbatim from codex rollout
(rollout-2026-08-15T03-29-52-01a004f8) by the frontier agent. No edits
beyond this header.

---

# ADVERSARIAL REVIEW V7 — R5 v3 compliance and soundness

Reviewer: Codex, fourth-round read-only review, 2026-08-15.

## 1. Summary verdict

**THEOREM-GRADE NO for v3 as written; the seven-link mathematical core is
sound after a local erratum.** Clause 1 now binds the unique reflected
negative symbol and the correct wrapper; Clause 3 now uses the required
\(2\sigma_K+1\) first moment; and deleting the word-trace route removes both of
V6's countability/trace-log defects. The proposed smoothing/Jordan/spectral
strategy is mathematically viable, and no hidden determinant-normalization
factor appears. TB_V2 itself records only original-disc contraction, and the
larger quarter-clearance contour used elsewhere is not contractive; however, a
fresh 384-bit read-only check from the immutable TB_V2 receipt verifies that
the uniformly smaller enlargement \(R_i+0.1\) has
\(\widehat\rho\le0.948343590351<1\) and positive pole/cut margin for every
branch family. This supplies the quantitative instance of v3's qualitative
continuity argument and closes the smoothing premise. Clause 2(c) does cite the
wrong Simon result—Lidskii gives the trace identity, not the determinant
product—and v3 contains several other local wording defects, but the correct
spectral product theorem exists in the cited Simon paper and the determinant
argument itself is sound. No new mathematical lemma is missing, but a revision
that misidentifies the load-bearing spectral theorem and falsely describes its
exact tail closure is not theorem-grade under this review's compliance rules.

## 2. Per-item findings

### (i) Clause 1 binding — **PASS**

**Evidence.** V3 gives exactly one positive and one reflected-negative formula
at [R5 v3, lines 26–38](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_R5_DETERMINANT_IDENTIFICATION.md:26):
\[
\theta_{+n}(z)=-\frac1{z+n\lambda},\qquad
\theta_{-n}(z)=\frac1{z-n\lambda},
\]
with weights \(((z\pm n\lambda)^2)^{-s}\). The engine implements precisely
these two cases at [zeta_cert_rosen_q5.py, lines 199–212](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/zeta_cert_rosen_q5.py:199).
The certified wrapper fixes `N_HEAD_ENGINE = 4`, `SIGN = 1`, and exact factor
strings `("3.14", "2.27", "1.70")` at
[certify_r3b_flagship.py, lines 50–60](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/tc_rerun/certify_r3b_flagship.py:50),
then passes those values to the builder at
[lines 294–305](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/tc_rerun/certify_r3b_flagship.py:294).
The builder's eleven calls are at
[tc_rerun.py, lines 130–145](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/tc_rerun/tc_rerun.py:130).
The wrapper hash printed in v3, `5b1bb085...31945`, matches the current file.

The primary [Mayer–Mühlenbruch–Strömberg paper, equation (34), pp. 20–21](https://arxiv.org/pdf/0912.2236)
defines the reduced reflected negative action with
\(g(1/(z-n\lambda_q))\), and its negative weight is the squared-denominator
weight. TB_V2 separately certifies \(\Re(n\lambda-z)>0\) for every negative
family at [lines 154–170](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_BLOCK_CERTIFICATES_V2.md:154),
which makes the squared-expression branch convention consistent.

**Reasoning.** V6's sign-flipped duplicate has been deleted, the wrapper—not
the standalone engine default—is now the named certified source, and the five
head plus six tail block occurrences match the code. This clause satisfies
V6 clause 1. The inaccurate “m=0 closure” sentence immediately after the
definition is a new implementation-description defect, recorded under (vi),
but it does not change the uniquely defined block sum.

### (ii) Smoothing bound (2a) — **PASS, with a provenance qualification**

**Evidence.** The normalized Hardy basis is stated at
[TB_R1, lines 8–10](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_R1_HILBERT_RESTATEMENT.md:8).
For
\(f=\sum_{k\ge0}a_k((z-c)/R)^k\) and
\(|w-c|/R\le r<1\), Cauchy–Schwarz gives
\[
 |f(w)|\le \|f\|_{H^2}
 \left(\sum_{k\ge0}r^{2k}\right)^{1/2}
 =\frac{\|f\|_{H^2}}{\sqrt{1-r^2}}.
\]
Because the boundary measure is normalized, no extra factor of \(R^{1/2}\)
is missing. Thus the kernel normalization used at
[R5 v3, lines 60–66](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_R5_DETERMINANT_IDENTIFICATION.md:60)
is correct.

TB_V2 certifies only
\(\rho_*=0.6978014199\ldots<0.70\) on the **original closed source discs**
at [TB_V2, lines 1–12](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_BLOCK_CERTIFICATES_V2.md:1),
with original-disc tail bounds at [lines 123–134](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_BLOCK_CERTIFICATES_V2.md:123)
and pole/cut margins at [lines 136–170](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_BLOCK_CERTIFICATES_V2.md:136).
It has no recorded enlarged radius and no recorded \(\widehat\rho\). V3 says
that “the certified image contraction keeps” every image of an enlarged disc
inside radius \(\widehat\rho<1\) and attributes this to the TB_V2 margins at
[lines 65–70](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_R5_DETERMINANT_IDENTIFICATION.md:65).

The distinction is material. The chain's existing R3b enlargement takes one
quarter of the pole/cut clearance
([R3B report, line 25](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/R3B_FLAGSHIP_CERT.md:25)).
For the \(2\to3,+2\) tail, its receipt records enlarged source radius
\(0.8849698602\ldots\) and image ratio
\(1.0757521114\ldots>1\) at
[R3B receipt, lines 41746–41755](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/R3B_FLAGSHIP_CERT_RECEIPT.json:41746).
That contour cannot be the neighborhood required by (2a), so the two
enlargements must not be conflated.

**Reasoning.** The required smaller common neighborhood can be—and in this
review was—verified directly from the current TB_V2 receipt and its generating
geometry. Recomputing all certified finite head branches on source radii
\(R_i+0.1\), retaining the original target radii \(R_j\), and applying the
receipt's first-\(n\) monotone bound to every deep tail gives, at 384-bit Arb
precision,
\[
 \widehat\rho\le
 0.9483435903504719548,\qquad
 \min(\hbox{pole/cut margin})\ge1.0023798735622528932.
\]
The worst branch is the \(3\to1,+1\) head. Stronger checks at
\(\varepsilon=0.01\) and \(0.001\) give respectively
\(\widehat\rho\le0.697840409742\) and
\(0.697805317692\). This fresh diagnostic writes no artifact, but it is a
computed verification against
[the TB_V2 receipt](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_BLOCK_CERTIFICATES_V2_RECEIPT.json)
and the current certificate code, not an inference from the failed R3b
contour.

The qualitative paper proof is also sufficient: split each tail into its
certified finite head and monotone deep tail, use the strict original-disc gap
plus continuity/equicontinuity, and choose one common \(\varepsilon>0\).
Thus v3's existence claim is correct, although “TB_V2 margins” should be
described as inputs to this continuity argument rather than as a pre-existing
\(\widehat\rho\) field. On compact subsets of \(\Omega_0\), the enlarged-disc
weights are uniformly \(O(n^{-2\sigma})\), so
\(\sum_n n^{-2\sigma}\) gives tail-block convergence in the sup norm and hence
an image holomorphic on a neighborhood of the closed source disc. Clause 2(a)
therefore establishes the bounded smoothing map \(L_s^H:H\to B\).

### (iii) Spectral-determinant step (2c) — **FAIL as cited; mathematical core PASS**

**Evidence.** The Jordan-chain argument at
[R5 v3, lines 76–81](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_R5_DETERMINANT_IDENTIFICATION.md:76)
is algebraically correct once (2a) holds. If
\((L-\lambda)v_j=v_{j-1}\), \(\lambda\ne0\), and the preceding chain vectors
are in \(B\), then
\(v_j=\lambda^{-1}(Lv_j-v_{j-1})\in B\). Together with the continuous
inclusion \(B(D)\subset H^2(D)\), this identifies the generalized eigenspaces
and therefore the algebraic multiplicities of all nonzero eigenvalues.

On the Hilbert side, the spectral product is true for trace-class operators,
but v3's attribution is wrong. Simon's determinant product is
**Theorem 4.2, equation (4.2), p. 258**, in
[Simon, “Notes on infinite determinants” (1977)](https://www.sciencedirect.com/science/article/pii/0001870877900573),
whereas Lidskii is the subsequent trace identity (Corollary 4.3). Thus
[R5 v3, lines 83–86](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_R5_DETERMINANT_IDENTIFICATION.md:83)
does not cite the theorem it uses.

On the Banach side, MMS Theorem 4.10 states that the disc-algebra operator is
nuclear of order zero; see the primary
[MMS paper, Theorem 4.10, p. 19](https://arxiv.org/pdf/0912.2236).
Grothendieck's Fredholm theory gives the genus-zero product over eigenvalues,
with algebraic multiplicity, for the \(p\le2/3\) nuclear class; the clean
primary statement is Theorem 8, pp. 108–109, of
[Grothendieck's 1952 “Résumé des résultats essentiels…”](https://aif.centre-mersenne.org/articles/10.5802/aif.46/).
“Nuclear of order zero” means membership for every \(p>0\), hence in
particular for \(p=2/3\). V3's phrase “order \(0\le2/3\)” at
[lines 87–90](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_R5_DETERMINANT_IDENTIFICATION.md:87)
is not the correct definition, although its intended implication is true.

**Reasoning.** With the now-verified (2a), trace class on \(H\), and the corrected spectral
theorems, both determinants are the canonical products over the same nonzero
eigenvalues. Both are normalized to equal one at the auxiliary scalar zero, so
there is no exponential factor or other normalization residue. No word trace,
no countable-word interchange, and no evaluation of a local trace-log at
\(t=1\) is needed. The determinant equality on \(\Omega_0\) is therefore
mathematically established. V3's stated Hilbert attribution is nevertheless
false and must be corrected; it should also cite Clause 3—not stale TB_R1 line
27—for trace class on \(\Omega_0\).

### (iv) Clause 3 envelope and holomorphy — **PASS**

**Evidence.** V3 now states
\[
b_k(s)\le A_Kq^k+C_Kk\rho^{k-1}
\]
and derives \(C_K\) from
\(\sum_n n^{-(2\sigma_K+1)}\) at
[R5 v3, lines 102–121](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_R5_DETERMINANT_IDENTIFICATION.md:102).
That matches the corrected R2 report at
[R2/R3 report, lines 19–28](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/R2R3_FLAGSHIP_CERT.md:19)
and the actual implementation: it sets \(p=2\sigma\), uses exponent
\(p+1\), and bounds the integral by a term proportional to
\(1/(\lambda p)\) at
[certify_r2_flagship.py, lines 478–524](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/tb_certify/certify_r2_flagship.py:478).

**Reasoning.** For every compact \(K\Subset\Omega_*\),
\(\sigma_K=\inf_K\Re s>0\). The finitely many low columns are locally bounded.
For high columns, the Hurwitz-closed \(m=0\) term is locally bounded away from
its possible pole and carries the geometric target-center factor \(q^k\);
the centered difference satisfies the mean-value bound
\(k\rho^{k-1}\) times the first moment, whose deep part is dominated by
\(\sum n^{-(2\sigma_K+1)}\). The angle factors in the squared weights are
bounded on \(K\). Hence \(A_K,C_K<\infty\) and
\(\sum_k b_k(s)\) converges uniformly on \(K\). The columnwise analytic
operator series therefore converges locally uniformly in trace norm, giving a
trace-class-holomorphic family on all of \(\Omega_*\); Simon Theorem 3.3 then
gives determinant analyticity. The old geometric claim
\(b_k\le W\rho_*^k\) in
[TB_R1, lines 27–28](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_R1_HILBERT_RESTATEMENT.md:27)
is stale and false for a \(k\rho^{k-1}\) tail, but Clause 3's corrected
summable envelope replaces it. This does not rescue (2a), which needs a
source-disc neighborhood rather than only trace-norm summability on the
original Hardy discs; that separate requirement was verified in item (ii).

### (v) Sector identification — **PASS, with a source-text caveat**

**Evidence.** The unique formulas and eleven occurrences in Clause 1 agree
with the specialized builder calls at
[tc_rerun.py, lines 130–145](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/tc_rerun/tc_rerun.py:130),
and every reflected-negative occurrence has coefficient `SIGN = +1`. MMS
Lemma 4.2 gives the odd-\(q\) incidence ranges for
\(q=2h_q+3\ge5\), including \(q=5\), while §5 first reduces the full
\(\pm i\)-indexed operator by the involution and then writes the positive-index
operators. The negative reduced symbol following equation (34) is exactly
\(g(1/(z-n\lambda_q))\). MMS Theorem 6.4 consumes the resulting
\(L_{s,+}\) and \(L_{s,-}\) determinants. See
[MMS, Lemma 4.2, equation (34), and Theorem 6.4](https://arxiv.org/pdf/0912.2236).

**Reasoning.** Specializing \(h_5=1\) and \(\kappa_5=3\) yields the builder's
four row-1, three row-2, and four row-3 occurrences. No full-space involution
is applied to the reduced three-component space, so V5's type error remains
removed. The PDF's heading immediately before displayed equation (34) is
printed as \(q=2h_q+3>5\), while Lemma 4.2 states \(q\ge5\) and the preceding
full odd-\(q\) matrix formula applies to \(q=5\). Thus the literal heading is a
source caveat (apparently a strict-inequality typo), but the general incidence
formula and the direct reduction support the \(q=5\) specialization. With the
now-unique formulas, “this reduced system is \(L_{s,+}\)” is an exact identity.

### (vi) New defects — **FAIL: five local defects found**

1. **Imprecise enlarged-disc provenance.** R5 v3 lines 65–70 attributes a
   \(\widehat\rho<1\) enlargement directly to TB_V2, which records only the
   original discs. A smaller common enlargement is valid and has now been
   independently verified, but the existing quarter-clearance enlargement is
   demonstrably not it. V3 should name the continuity step or a concrete
   smaller enlargement.
2. **Wrong Simon/Lidskii attribution.** R5 v3 lines 83–86 calls the determinant
   product “Lidskii's theorem” and points to §3. The product is Simon Theorem
   4.2; Lidskii is the trace identity.
3. **False “m=0 closure implements the sum exactly” sentence.** R5 v3 lines
   39–40 is false for a general input column \(k\). The exact tail formula uses
   every \(m=0,\ldots,k\), as the engine shows at
   [zeta_cert_rosen_q5.py, lines 215–260](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/zeta_cert_rosen_q5.py:215)
   and again in the all-column implementation at
   [lines 291–318](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/zeta_cert_rosen_q5.py:291).
   The \(m=0\) term is merely the specially Hurwitz-closed center term used in
   the R2 envelope.
4. **Nuclear-order notation.** “Order \(0\le2/3\)” is not a valid comparison
   of numeric exponents. The needed statement is “nuclear of order zero, hence
   \(p\)-nuclear for \(p=2/3\).”
5. **Stale R1 trace-class citation.** R5 v3 line 84 invokes TB_R1's certified
   \(\sum b_k\), but TB_R1 lines 27–28 uses the obsolete pure-geometric tail.
   Clause 3 supplies the correct proof, so (2c) must cite Clause 3 instead.

All five are local citation/provenance/wording defects. None is a remaining
mathematical gap after the common-enlargement check above, but defects 2 and 3
are literally false statements in the claimed proof and therefore block a
theorem-grade compliance ruling on the current revision.

## 3. New defects found

The five defects above are new relative to V6's list. They do **not** revive
the deleted word expansion or the forbidden trace-log-at-\(t=1\) route. Nor do
they show a normalization mismatch between the Hilbert and Banach
determinants. The only initially plausible mathematical kill was the smoothing
premise; the fresh all-family check on \(R_i+0.1\) refutes that kill. What
remains is a local erratum, especially the false theorem attribution and the
false “m=0 exact closure” sentence. The inference obtained after that erratum
is sound; the present v3 text is not yet a compliant theorem-grade proof.

## 4. FINAL RULING

**THEOREM-GRADE NO AS V3 IS WRITTEN.** The seven-link mathematical argument
survives after a local erratum, but the supplied v3 cannot itself receive YES.
V4 left exactly the Hilbert/MMS interface
open at
[V4, lines 15–31](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/ADVERSARIAL_REVIEW_V4_R3B.md:15),
and assembly link 4 produces a zero of the Hilbert determinant at
[assembly, lines 65–68](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/THEOREM_G5_OFFLINE_ASSEMBLY.md:65).
V3's mathematical construction supplies the correct exact operator, a valid smoothing map on
\(\Omega_0\), equality of the nonzero spectra with algebraic multiplicities,
spectral canonical determinants with no normalization residue, trace-class
holomorphy on \(\Omega_*\), and the exact reduced \(L_{s,+}\) identification.
After the citation/formula erratum below, the identity theorem transports the
Hilbert determinant zero to the MMS Banach determinant. The prior reviews found
no new obstruction in links 5–7, and this review does not reopen one.

The **precise minimal missing piece** is not another analytic lemma; it is a
short v3.1 erratum containing all of the following corrections:

1. Name a new enlargement such as
   \(D_i^{0.1}=D(c_i,R_i+0.1)\) (not the R3b quarter-clearance enlargement)
   and record, or prove by the stated continuity argument, that uniformly over
   all eleven families every branch is holomorphic there and
   \[
   \sup_{z\in\overline{D_i^{\varepsilon}}}
   \frac{|\theta_n(z)-c_j|}{R_j}\le\widehat\rho<1.
   \]
   For the six tails, state the finite-head/deep-tail split and the monotone
   bound that makes the choice uniform in \(n\). The present read-only check
   gives \(\widehat\rho\le0.948343590351\).
2. Replace the Hilbert determinant citation by Simon Theorem 4.2, state
   order-zero \(\Rightarrow p=2/3\) on the Banach side, and cite Clause 3 for
   Hilbert trace class. State explicitly that both canonical products are
   normalized to one at scalar zero.
3. Correct the tail-closure sentence to say that the exact Hurwitz closure for
   column \(k\) uses all \(m=0,\ldots,k\).

These corrections make the presentation match the already-valid mathematical
argument; they do not add a new lemma on which the conclusion depends. Once
they are made, the seven-link assembly earns THEOREM-GRADE YES. Until then,
the current revision's compliance ruling is NO. No word-expansion lemma,
auxiliary-\(t\) continuation, or determinant-normalization factor is missing.



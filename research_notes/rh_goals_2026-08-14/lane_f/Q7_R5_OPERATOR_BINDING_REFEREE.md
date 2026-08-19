# Q7 R5 OPERATOR BINDING — COLD ADVERSARIAL REFEREE

Date: 2026-08-19
Reviewed commit: `7cb4c49061e1482d6697f80bd6db35009b6140ac` (`Prove q7 MMS operator binding`)
Reviewed file: `research_notes/rh_goals_2026-08-14/lane_f/Q7_R5_OPERATOR_BINDING_SOL.md`
Review mode: cold, read-only as to the submitted proof; no source or receipt was edited.

## Verdict

**GAPS / NOT REFUTED.**

The q=7 five-disc binding, MMS equation-(34) specialization, branch convention,
finite-matrix identification, absolute-convergence smoothing mechanism, pole
exclusion, and connectivity argument survive this review.  The first
load-bearing omission is in Section 5.1: lines 397--421 assert the centered
tail-column estimate needed for trace-class holomorphy on \(\Omega^*\), but do
not derive it.  In particular, the submitted text does not write the
\(b^k-a^k\) decomposition, prove its uniform \(O(1/\ell)\) centered difference,
or turn the q=7 E1 bounds into explicit locally uniform constants.  A second
local omission is at lines 431--456: the spectral-product and determinant-
holomorphy steps omit the exact Simon and Grothendieck results which the
accepted q=5 referee required after finding an earlier false attribution.

These are repairable paper gaps, not a counterexample.  The exact repair is
given below.  Once it and the cited determinant theorems are inserted, I find
no further load-bearing gap in Section 5, conditional on the banked TB/E1
receipts.

## Scope and changed paths

This referee writes only
`research_notes/rh_goals_2026-08-14/lane_f/Q7_R5_OPERATOR_BINDING_REFEREE.md`.
No proof source, receipt, plan, status ledger, or code file was changed.  The
reviewed worktree began at the reviewed commit:

```text
$ git status --short --branch
## codex/law-q7-binding-referee-20260819

$ git rev-parse HEAD
7cb4c49061e1482d6697f80bd6db35009b6140ac
```

## 1. The submitted Section 5 and the first gap

The decisive submitted lines are:

```text
$ git show 7cb4c49:research_notes/rh_goals_2026-08-14/lane_f/Q7_R5_OPERATOR_BINDING_SOL.md \
    | nl -ba | sed -n '397,437p'
397  The finite heads are immediate.  For tails, the exact head-plus-Hurwitz split
398  and the binomial formula in Section 3 give a locally uniform column estimate ...
402    b_k(s) <= A_K rho_hat^k + C_K k rho_hat^(k-1),
407  where b_k is the sum of the H-column norms over the five output discs,
408  A_K bounds the finitely many Hurwitz-closed center columns, and C_K
409  comes from the first-moment remainder.
419  The normalized monomials are an orthonormal Hardy basis, so this column-sum
420  bound makes s |-> L^H_{s,+} a locally uniformly trace-class ... family ...
431  The trace-class Fredholm determinant on H and the order-zero nuclear
432  determinant on B are their genus-zero spectral products.
436    det_H(1-L^H_{s,+}) = det_B(1-L^{MMS}_{s,+}).
```

The convergence of
\(\sum_{\ell\ge n_0}\ell^{-(2\inf_K\Re s+1)}\) stated at lines 409--412 is
necessary but not sufficient by itself.  It controls the centered remainder
only after proving that the normalized branch powers differ from their
\(\ell=\infty\) limit by \(O(k\widehat\rho^{k-1}/\ell)\).  That missing
inequality is the first load-bearing gap: without it, the trace-norm column
sum on \(\Re s>0\) has been asserted rather than proved.

## 2. Smallest rigorous centered-tail repair

There are ten tail occurrences, and every one has input/target component 5.
This was recomputed directly from the banked block list:

```text
$ /Users/za/.venvs/farey-rh/bin/python - <<'PY'
... parse F7_TB_BLOCK_CERTIFICATES_RECEIPT.json and its block list ...
PY
all_tail_targets= [5]
abs_c5_over_R5= [0.62500000000000000000000 +/- 1.73e-24]
center_ratio_lt_rho_hat= True
```

Fix one tail occurrence
\(B=(i,5,n_0,\varepsilon)\), with \(\varepsilon\in\{+,-\}\).  On its
enlarged source disc put

\[
 a:=-\frac{c_5}{R_5},\qquad
 b_{\ell,B}(z):=\frac{\theta_{\varepsilon\ell}(z)-c_5}{R_5}.
\]

The E1 receipt gives \(|b_{\ell,B}(z)|\le\widehat\rho<1\) for every branch in
the family.  The limit as \(\ell\to\infty\), or the direct receipt computation
above, gives \(|a|\le\widehat\rho\).  For every \(k\ge1\), use the exact
identity

\[
 b_{\ell,B}(z)^k-a^k
   =(b_{\ell,B}(z)-a)
     \sum_{r=0}^{k-1}b_{\ell,B}(z)^{k-1-r}a^r.                 \tag{R1}
\]

Let \(p_{\ell,B}(z)=z+\ell\lambda_7\) for a positive branch and
\(p_{\ell,B}(z)=\ell\lambda_7-z\) for a reflected-negative branch.  In both
cases \(\theta_{\varepsilon\ell}(z)=-1/p_{\ell,B}(z)\), while the squared
weight is unchanged.  Let \(\Delta_B>0\) be the E1 lower bound for
\(\Re p_{n_0,B}\) on the enlarged source disc, and define

\[
 \mu_B:=\min\{\lambda_7,\Delta_B/n_0\}>0.
\]

For every \(\ell\ge n_0\),

\[
 \Re p_{\ell,B}(z)
 \ge \Delta_B+(\ell-n_0)\lambda_7
 \ge \mu_B\ell.                                               \tag{R2}
\]

Consequently

\[
 |b_{\ell,B}(z)-a|
 =\frac{|\theta_{\varepsilon\ell}(z)|}{R_5}
 \le \frac{1}{R_5\mu_B\ell},                                  \tag{R3}
\]

and (R1) gives

\[
 |b_{\ell,B}(z)^k-a^k|
 \le \frac{k\widehat\rho^{k-1}}{R_5\mu_B\ell}.                \tag{R4}
\]

Now fix a compact \(K\Subset\Omega^*\) and put

\[
 \sigma_K:=\inf_{s\in K}\Re s>0,\qquad
 T_K:=\sup_{s\in K}|\Im s|<\infty.
\]

The certified positive-real-part branch permits the principal logarithm with
\(|\arg p_{\ell,B}|<\pi/2\).  Hence, once
\(\mu_B\ell\ge1\),

\[
 |p_{\ell,B}(z)^{-2s}|
 \le e^{\pi T_K}\mu_B^{-2\sigma_K}\ell^{-2\sigma_K}.
\]

Absorb the finitely many preceding indices into the constant and define
explicitly

\[
 W_{B,K}:=\max\left\{
 e^{\pi T_K}\mu_B^{-2\sigma_K},
 \max_{n_0\le\ell<\lceil1/\mu_B\rceil+1}
 \sup_{s\in K,z\in\overline{D_i^{e_i}}}
   \ell^{2\sigma_K}|p_{\ell,B}(z)^{-2s}|
 \right\}.
\]

Then for all \(\ell\ge n_0\),

\[
 |w_{\varepsilon\ell,s}(z)|
 \le W_{B,K}\ell^{-2\sigma_K}.                                \tag{R5}
\]

Split the tail column exactly as

\[
 \begin{aligned}
 F_{B,k}(s,z)
 &=\sum_{\ell\ge n_0}w_{\varepsilon\ell,s}(z)
                    b_{\ell,B}(z)^k\\
 &=a^k Z_{B,0}(s,z)
   +\sum_{\ell\ge n_0}w_{\varepsilon\ell,s}(z)
           \bigl(b_{\ell,B}(z)^k-a^k\bigr),                   \tag{R6}
 \end{aligned}
\]

where the center term is the exact \(m=0\) Hurwitz closure

\[
 Z_{B,0}(s,z)
  =(\lambda_7^2)^{-s}\zeta(2s,n_0\pm z/\lambda_7).
\]

It is crucial not to replace this term by an absolutely convergent branch sum
when \(\Re s\le1/2\).  On \(K\), which is disjoint from the real pole lattice,
\(Z_{B,0}\) is holomorphic on the fixed enlarged disc and therefore

\[
 A_{B,K}:=sup_{s\in K,z\in\overline{D_i^{e_i}}}
             |Z_{B,0}(s,z)|<\infty.                            \tag{R7}
\]

By (R4)--(R5), the centered remainder in (R6) converges locally uniformly on
all of \(\Re s>0\) and satisfies

\[
 \begin{aligned}
 \sup_z|F_{B,k}(s,z)|
 &\le A_{B,K}\widehat\rho^k
  +C_{B,K}k\widehat\rho^{k-1},\\
 C_{B,K}
 &:=\frac{W_{B,K}}{R_5\mu_B}
      \sum_{\ell\ge n_0}\ell^{-(2\sigma_K+1)}<\infty.        \tag{R8}
 \end{aligned}
\]

The identity (R6) first holds as a branch sum on \(\Re s>1/2\); its right side
then supplies the same Hurwitz continuation on \(\Omega^*\).  Because it is
holomorphic on an enlarged output disc, its \(H^2(D_i)\) norm is at most the
displayed sup bound.  Each of the finitely many head occurrences similarly
has a bound \(H_{B,K}\widehat\rho^k\).

Define without ambiguity

\[
 b_k(s):=\sum_{j=1}^{5}\|L^H_{s,+}e_{j,k}\|_H,
\]

and sum the finite family constants into \(A_K,C_K\).  Equations (R1)--(R8)
then prove

\[
 b_k(s)\le A_K\widehat\rho^k+C_Kk\widehat\rho^{k-1},
\]

and, explicitly,

\[
 \sup_{s\in K}\sum_{k\ge0}b_k(s)
 \le \frac{A_K}{1-\widehat\rho}
      +\frac{C_K}{(1-\widehat\rho)^2}<\infty.                  \tag{R9}
\]

Finally,

\[
 L^H_{s,+}
 =\sum_{j=1}^{5}\sum_{k\ge0}
   (L^H_{s,+}e_{j,k})\otimes e_{j,k}^*
\]

converges locally uniformly in trace norm.  Each column is holomorphic by
(R6), so the Weierstrass theorem in the trace-class Banach space proves that
\(s\mapsto L^H_{s,+}\) is trace-class holomorphic on \(\Omega^*\).  This is
the missing implication at submitted lines 397--421.

## 3. Smoothing on the absolute-convergence region — PASS

On \(\Omega_0=\{\Re s>1/2\}\), E1 places every branch image in a target
subdisc of ratio \(\widehat\rho<1\).  The normalized Hardy reproducing-kernel
bound therefore gives

\[
 |f(\theta(z))|\le(1-\widehat\rho^2)^{-1/2}\|f\|_{H^2}.
\]

On compact subsets of \(\Omega_0\), (R5) now has
\(\sum_\ell\ell^{-2\sigma_K}<\infty\), so each tail converges uniformly on
the enlarged source disc.  Thus \(L^H_{s,+}:H\to B\) is bounded there and has
the same branch-sum action as \(L^{MMS}_{s,+}\) on \(B\).  The submitted
Jordan-chain induction at lines 424--429 then correctly identifies all
nonzero eigenvalues with algebraic multiplicity.

## 4. Spectral determinants and holomorphy — citation gap and repair

The q7 Section 5 contains no exact determinant attribution:

```text
$ git show 7cb4c49:research_notes/rh_goals_2026-08-14/lane_f/Q7_R5_OPERATOR_BINDING_SOL.md \
    | sed -n '364,468p' \
    | rg -n 'Simon|Grothendieck|Theorem 4\.2|Theorem 3\.3|spectral product'
69:determinant on B are their genus-zero spectral products.
```

By contrast, the accepted q=5 v3.1 proof names all three required results:

```text
$ nl -ba research_notes/rh_goals_2026-08-14/lane_g/TB_R5_DETERMINANT_IDENTIFICATION.md \
    | sed -n '118,136p;146,176p' \
    | rg 'Simon|Grothendieck|Theorem 4\.2|Theorem 3\.3|nuclear of order'
122  ... [CITED: Simon, Notes on infinite determinants ...]
126  On B, L_s^B is nuclear of order ZERO ...
127  p-nuclear for p = 2/3; ... Grothendieck's ...
129  ... [CITED: Grothendieck, Resume des resultats essentiels ...]
164  [CITED: Simon, Notes on infinite determinants ...
165  Theorem 3.3].
```

The q7 repair must inherit these exact sources and roles:

1. Barry Simon, *Notes on infinite determinants*, **Advances in Mathematics**
   24 (1977), Theorem 4.2, equation (4.2), p. 258: the Hilbert trace-class
   Fredholm determinant is the canonical product over eigenvalues with
   algebraic multiplicity.  Lidskii is not the result used here.
2. Alexandre Grothendieck, *Resume des resultats essentiels dans la theorie
   des produits tensoriels topologiques et des espaces nucleaires*, **Annales
   de l'Institut Fourier** 4 (1952), Theoreme 8, pp. 108--109: for the
   \(p\le2/3\) nuclear class, the Banach Fredholm determinant is the genus-zero
   spectral product with algebraic multiplicity.  MMS nuclearity of order zero
   implies membership in the \(p=2/3\) class.
3. Simon, op. cit., Theorem 3.3: a trace-class-holomorphic family has an
   analytic Fredholm determinant.

For complete source matching, add that MMS Theorem 4.10 first gives nuclearity
of order zero for the full \(\pm i\)-indexed operator.  MMS Lemma 5.1 makes the
P-eigenspaces complemented and invariant; bounded restriction and conjugacy
to the reduced five-disc operator preserve nuclearity of order zero.  Hence
Theorem 4.10 applies to the chosen reduced \(L^{MMS}_{s,+}\), not merely to an
unnamed MMS Banach space.

With the Jordan-chain equality, both auxiliary determinants
\(\det(1-tL)\) are the same genus-zero product and are normalized to 1 at
\(t=0\); no exponential normalization factor remains.  Setting \(t=1\) proves
the determinant equality on \(\Omega_0\).

## 5. Chosen discs, equality domain, poles, and connectivity — PASS

The five exact radius multipliers exceed one, so each real partition interval
lies strictly inside its centered disc.  The TB receipt certifies the 19 branch
families on the original discs, and E1 certifies holomorphy and strict image
contraction on enlarged source discs.  Reflecting \(D_j\) to \(D_{-j}=-D_j\)
supplies the negative half of the unreduced MMS space.  These are the
disc-admissibility hypotheses used by MMS Lemma 4.4; no q=5 geometry is being
silently reused.

The submitted domain

\[
 \Omega^*=\{\Re s>1/2\}\cup\{\Re s>0,\Im s>1\}
\]

is open and connected because the two open sets have nonempty intersection.
Every MMS/Hurwitz pole \(s=(1-k)/2\) is real: \(s=1/2\) lies on the excluded
boundary and the remaining points have \(\Re s\le0\).  Thus both determinant
families are analytic on \(\Omega^*\) after the repairs above, and equality on
the nonempty open set \(\Omega_0\) extends to all of \(\Omega^*\) by the
identity theorem.  The equality domain and pole/connectivity arguments pass.

## 6. Exact K_start=12 correction and numerical blast radius

An intermediate hostile diagnostic used `K_start=8` and reported a different
tail maximum.  That run did not use the banked receipt parameters and is not
evidence against the theorem.  The banked receipt records `K_start=12`, and a
fresh read-only aggregation of every stored head and deep-tail ratio gives:

```text
$ jq '{tail_split,rho_star,rho_star_upper_bound,worst_block_label,
       certification_verdict}' \
    research_notes/rh_goals_2026-08-14/lane_f/f7_receipts/F7_TB_BLOCK_CERTIFICATES_RECEIPT.json
tail_split.K_start: 12
tail_split.max_K: 64
rho_star: [0.763212029206899202166157 +/- 1.41e-25]
worst_block_label: 5->3, +1, head
certification_verdict: PASS_RHO_LT_0.80

$ /Users/za/.venvs/farey-rh/bin/python - <<'PY'
... recompute the maximum over every stored head_terms/deep_tail ratio ...
PY
K_start= 12
recomputed_max= [0.763212029206899202166157 +/- 1.41e-25]
recomputed_worst= 5->3, +1, head head n=1
recomputed_lt_0.80= True
```

Section 5 uses the separate enlarged-disc E1 contraction constant, not the
original-disc TB maximum:

```text
$ jq '{schema,precision_bits,M_enlarged_contour_arcs,rho_hat_upper_bound,
       rho_hat_less_than_one,eta_max_upper_bound,verdict}' \
    research_notes/rh_goals_2026-08-14/lane_f/f7_receipts/F7_E1_ENLARGED_CONTRACTION_V2_RECEIPT.json
schema: f7-e1-enlarged-contraction/v2
precision_bits: 384
M_enlarged_contour_arcs: 512
rho_hat_upper_bound:
  [0.9152411837446921486199057183790500874132201822167121491776750120826392648965487186604668777644585600 +/- 3.97e-101]
rho_hat_less_than_one: true
eta_max_upper_bound:
  [0.8695652173913043478260869565217391304347826086956521739130434782608695652173913043478260869565217391 +/- 3.06e-101]
verdict: PASS_RHO_HAT_LT_1
```

Therefore the `K_start=8` diagnostic has **no blast radius**.  The TB
admissibility gate and the E1 smoothing premise retain their stated scopes.

## 7. Blast radius of this referee ruling

The present gaps block only the status upgrade of the q7 Hilbert/Banach common-
continuation implication.  Until a repaired proof receives a fresh cold
referee pass:

- the q7 finite/Hilbert Fredholm-zero certificate remains supported only at
  its already banked Hilbert-side scope;
- transport of that zero to the MMS Banach determinant, and therefore any
  downstream Selberg-zeta zero or resonance claim consuming Link 4b, remains
  **CONJECTURAL / OPEN**;
- the q7 TB, E1, finite-winding, determinant-comparison, and `K_s` numerical
  certificates are not refuted or downgraded by this review;
- the referee-confirmed q=5 common-continuation theorem is unaffected.

The repair is local: insert (R1)--(R9), define the column aggregation over all
five input components, add the three exact determinant citations, and state
the complemented P-sector transfer of MMS nuclearity.  After those changes I
find no further Section 5 obstruction, but the repaired text must receive its
own cold read before banking.

## Final ruling

**GAPS / NOT REFUTED.**  The proof strategy is sound, and the missing centered
estimate has a short rigorous completion, but commit `7cb4c49` does not itself
contain that completion or the determinant citations required by its q=5
precedent.  No status promotion is authorized from this artifact.

READY FOR JUDGING

# Q7 R5 OPERATOR BINDING — SECOND COLD REFEREE

Date: 2026-08-19

Verdict: **CONFIRMED — REPAIRED PROOF CLAIM**

## Scope

I read `Q7_R5_OPERATOR_BINDING_REFEREE.md` in full and reviewed only the
dated repair block appended to `Q7_R5_OPERATOR_BINDING_SOL.md`. The first
referee's ruling was **GAPS / NOT REFUTED**: the centered tail-column estimate
was asserted but not derived, and the Simon/Grothendieck citations and the
complemented MMS \(P\)-sector transfer were missing
(`Q7_R5_OPERATOR_BINDING_REFEREE.md:398-422`). This report checks the repair
against those exact defects. It is not a fresh review of the rest of q7.

## Receipt and numerical audit

The banked TB receipt was checked directly, rather than inferred from a
rounded prose summary:

```
$ jq '{precision_bits,M,tail_split,certification_verdict,worst_block_label,
       rho_less_than_threshold,all_branch_cut_clearances_pass,
       all_head_and_deep_tail_terms_pass,all_pole_clearances_pass}' \
    f7_receipts/F7_TB_BLOCK_CERTIFICATES_RECEIPT.json
{
  "precision_bits": 384,
  "M": 512,
  "tail_split": {"K_start": 12, "deep_first_index": "n0+K+1",
                  "max_K": 64, ...},
  "certification_verdict": "PASS_RHO_LT_0.80",
  "worst_block_label": "5→3, +1, head",
  "rho_less_than_threshold": true,
  "all_branch_cut_clearances_pass": true,
  "all_head_and_deep_tail_terms_pass": true,
  "all_pole_clearances_pass": true
}
```

The same receipt has 19 blocks, of which 10 are tails; all ten tail rows have
`block[1] = 5`. The independent query was:

```
$ jq '{total_blocks:(.blocks|length),
       tail_blocks:([.blocks[]|select(.tail==true)]|length),
       tail_block_inputs:([.blocks[]|select(.tail==true)|.block[1]]|unique),
       all_pass:(all(.blocks[]; .pass == true))}' \
    f7_receipts/F7_TB_BLOCK_CERTIFICATES_RECEIPT.json
{
  "total_blocks": 19,
  "tail_blocks": 10,
  "tail_block_inputs": [5],
  "all_pass": true
}
```

The receipt's reproducibility command records `--precision-bits 384 --M 512
--K-start 12 --max-K 64`
(`F7_TB_BLOCK_CERTIFICATES.md:236-248`). The enlarged-disc receipt
independently gives the exact radius strings
`["3.522","2.622","2.372","1.79","1.6"]`,
`rho_hat_upper_bound =
[0.9152411837446921486199057183790500874132201822167121491776750120826392648965487186604668777644585600 +/- 3.97e-101]`,
`rho_hat_less_than_one = true`, and
`verdict = PASS_RHO_HAT_LT_1`. Therefore the repair's outward bounds
\(\rho_*\le 0.763213\) and
\(\widehat\rho\le0.9152411837446922<1\) are supported; the rejected
`K_start=8` diagnostic is not used.

## R1--R9 algebra and analytic bounds

The repaired block's notation is consistent for every tail row. Its receipt
audit establishes that all tails have input component 5, so the one center
\(a=-c_5/R_5\) is applicable to every tail occurrence.

1. **R1, exact centering.** With
   \(b_{\ell,B}=(\theta_{\varepsilon\ell}-c_5)/R_5\),
   \(b-a=\theta_{\varepsilon\ell}/R_5\). The displayed difference-of-powers
   identity is exact for \(k\ge1\), with no asymptotic remainder hidden.

2. **R2, denominator growth.** For \(p=z+\ell\lambda_7\) or
   \(p=\ell\lambda_7-z\), E1 supplies \(\Re p_{n_0}\ge\Delta_B>0\); adding
   \((\ell-n_0)\lambda_7\) gives
   \(\Re p_\ell\ge\Delta_B+(\ell-n_0)\lambda_7\ge\mu_B\ell\), where
   \(\mu_B=\min(\lambda_7,\Delta_B/n_0)>0\). This is valid on the certified
   right-half-plane branch for both signs.

3. **R3, inverse estimate.** Since \(\Re p_\ell>0\),
   \(|\theta_{\varepsilon\ell}|=|p_\ell|^{-1}\le(\Re p_\ell)^{-1}\), hence
   \(|b-a|\le(R_5\mu_B\ell)^{-1}\).

4. **R4, centered power estimate.** Both \(|a|=5/8\) and
   \(|b|\le\widehat\rho\), so the exact R1 sum gives
   \[
   |b^k-a^k|\le k\widehat\rho^{\,k-1}/(R_5\mu_B\ell).
   \]
   The strict inequality \(5/8<\widehat\rho<1\) is numerically certified.

5. **R5, compact-uniform weights.** For \(K\Subset\Omega^*\), let
   \(\sigma_K=\inf_K\Re s>0\) and \(T_K=\sup_K|\Im s|<\infty\). On the
   positive-real-part branch,
   \[
   |p^{-2s}|=|p|^{-2\Re s}e^{2(\Im s)\arg p}
   \le e^{\pi T_K}(\mu_B\ell)^{-2\sigma_K}
   \quad(\mu_B\ell\ge1).
   \]
   The finitely many indices with \(\mu_B\ell<1\) are absorbed into the
   displayed finite maximum in the repair (with an empty finite submaximum
   omitted). Thus \(W_{B,K}\ell^{-2\sigma_K}\) is a genuine compact-uniform
   weight bound. This is the required Hurwitz/weight estimate, not a false
   \(2\sigma+k\) exponent claim.

6. **R6, exact center plus centered remainder.** The split
   \[
   F_{B,k}=a^k Z_{B,0}+\sum_{\ell\ge n_0}w_{\varepsilon\ell,s}
       (b_{\ell,B}^k-a^k)
   \]
   is algebraically exact. The \(m=0\) center is correctly closed as
   \[
   Z_{B,0}=(\lambda_7^2)^{-s}\zeta(2s,n_0\pm z/\lambda_7),
   \]
   with the sign matching the two branch choices. Absolute convergence is
   used first on \(\Re s>1/2\), then the Hurwitz expression supplies the stated
   continuation on \(\Omega^*\).

7. **R7, center holomorphy.** E1 branch-cut/pole clearance keeps the Hurwitz
   parameter away from its singular set on the enlarged disc. Avoidance of
   the real pole lattice by \(K\Subset\Omega^*\) makes \(Z_{B,0}\) holomorphic
   on a neighborhood of the compact product and therefore bounded by a finite
   \(A_{B,K}\).

8. **R8, local uniform summability and Hardy control.** Combining R4 and R5
   gives
   \[
   \sup_z|F_{B,k}(s,z)|\le A_{B,K}\widehat\rho^k+
      C_{B,K}k\widehat\rho^{\,k-1},\qquad
   C_{B,K}\propto\sum_{\ell\ge n_0}\ell^{-(2\sigma_K+1)}<\infty.
   \]
   The finite head terms have the geometric \(\widehat\rho^k\) bound. The
   enlarged-disc holomorphy gives \(\|F\|_{H^2}\le\sup|F|\) (normalized Hardy
   norm), so no unproved boundary estimate is needed.

9. **R9, trace-class holomorphy.** Summing the finitely many occurrences and
   all five input components gives
   \[
   b_k(s)=\sum_{j=1}^5\|L^H_{s,+}e_{j,k}\|_H
      \le A_K\widehat\rho^k+C_Kk\widehat\rho^{\,k-1},
   \]
   and hence
   \[
   \sup_{s\in K}\sum_{k\ge0}b_k(s)\le
      A_K/(1-\widehat\rho)+C_K/(1-\widehat\rho)^2<\infty.
   \]
   The rank-one column expansion therefore converges locally uniformly in
   trace norm. The center, remainder, and finite heads are holomorphic; the
   Banach-valued Weierstrass theorem consequently proves
   \(s\mapsto L^H_{s,+}\) trace-class holomorphic on \(\Omega^*\).

This closes the first referee's missing compact-uniform estimate. In
particular, the first-moment summability is
\(\sum\ell^{-(2\sigma_K+1)}\), exactly the exponent accepted by the q5
precedent (`TB_R5_DETERMINANT_IDENTIFICATION.md:146-165`).

## Determinant and sector audit

The repair uses the cited results in the same roles already accepted in q5:

- Simon, *Notes on infinite determinants of Hilbert space operators*, Adv.
  Math. 24 (1977), Theorem 4.2, equation (4.2), p. 258, supplies the Hilbert
  trace-class Fredholm determinant as the canonical product over eigenvalues
  with algebraic multiplicity. Simon Theorem 3.3 supplies determinant
  analyticity for a trace-class-holomorphic family. Lidskii is not used; the
  q5 referee explicitly made this distinction
  (`TB_R5_DETERMINANT_IDENTIFICATION.md:118-125`).
- MMS Theorem 4.10 supplies nuclearity of order zero for the full Banach
  operator. MMS Lemma 5.1 supplies complemented, invariant \(P\)-eigenspaces;
  bounded restriction and conjugacy preserve nuclearity, so the reduced
  five-disc operator remains order-zero nuclear and hence \(p\)-nuclear for
  \(p=2/3\).
- Grothendieck, *Résumé des résultats essentiels...*, Ann. Inst. Fourier 4
  (1952), Théorème 8, pp. 108--109, supplies the genus-zero Fredholm product
  with algebraic multiplicity for this \(p\le2/3\) nuclear class. This is the
  same Banach-side role recorded in q5
  (`TB_R5_DETERMINANT_IDENTIFICATION.md:126-136`).

The common nonzero spectrum with algebraic multiplicity is the already accepted
Hilbert/Banach argument; both \(t\)-determinants are normalized to \(1\) at
\(t=0\), so there is no residual exponential factor. Equality at \(t=1\) on
\(\Omega_0\), followed by analyticity of both sides and the identity theorem,
extends the equality to \(\Omega^*\). The repair states these roles at
`Q7_R5_OPERATOR_BINDING_SOL.md:690-712`; they are not new unsupported claims.

## Ruling and blast radius

**CONFIRMED — REPAIRED PROOF CLAIM.** R1--R9 now provide the missing
centered-column derivation, compact-uniform weight/Hurwitz control, locally
uniform trace-norm series, and trace-class holomorphy. The exact Simon,
Grothendieck, and MMS \(P\)-sector roles are supplied and match the accepted
q5 construction. The K-start numerical premise is receipt-backed at
`K_start=12`, not the rejected diagnostic `K_start=8`.

This clears the two gaps identified by the first referee for the q7
Hilbert/Banach operator-binding implication. It does not independently certify
any downstream Selberg-zero, resonance, scattering, automorphic, parity, or LAW
claim; those remain subject to their own gates. No q5 status is changed.

## Verification receipt

Commands run in this worktree:

```
$ ./te doctor
... "ok": true ...

$ git diff --check
(no output; exit 0)
```

Only this file was authored in the isolated worktree. No Aristotle submission,
Kaggle launch, commit, or other repository mutation was performed.

READY FOR JUDGING

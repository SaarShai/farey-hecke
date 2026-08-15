# Numerical determination of the Mertens mean-square constant and a first test of Gonek's conjecture

*Experimental-Mathematics-style paper skeleton; owner-gated fields are intentionally unfilled.*

Author(s): **[OWNER-GATED]**
Affiliations: **[OWNER-GATED]**
Venue and submission decisions: **[OWNER-GATED]**

## Status notation and provenance

- **[RECEIPT]** means a value, convention, computation, or gate copied from a supplied receipt/report or from the supplied cautionary audit.
- **[FITTED-TAIL]** means a value obtained by combining a reported finite sum with the reported central or conservative tail model; it is not a theorem-level bound.
- **[LITERATURE]** means a claim reported by the supplied literature syntheses. Those syntheses establish the provenance boundary for this skeleton; they are not treated as independent numerical verification.

## Abstract

We assemble a reproducible numerical study of the zero-sum constant associated with the conditional Mertens mean-square framework,
\[
S=\sum_{\rho=1/2+i\gamma}\frac{1}{|\rho|^2|\zeta'(\rho)|^2}.
\]
This is the receipt's two-sided zero-sum definition. **[RECEIPT]**
Using the two-sided conjugate-zero convention, the V2 calculation gives
\(S=0.029032731101\pm1.79\times10^{-5}\), with only **3 significant digits** claimed. **[FITTED-TAIL]**
Source: `research_notes/rh_goals_2026-08-14/lane_a/ZERO_SUM_V2_REPORT.md`, `Verdict` and `Error budget`.

We also tabulate \(J_{-1}(T)=\sum_{0<\gamma\le T}|\zeta'(1/2+i\gamma)|^{-2}\) through the supplied \(N=10000\) receipt. A through-origin fit over the upper half of those checkpoints has slope \(0.09278191769461815\), or ratio \(0.9589406036560452\) to the Gonek target used by the computation; the receipt verdict is **TOO EARLY**, not confirmation or refutation. **[RECEIPT]**
Source: `research_notes/rh_goals_2026-08-14/lane_a/j_minus1_receipt.json`, `top_half_linear_fit` and `verdict`.

The supplied prior-art search found no published numerical table for either the weighted zero sum or \(J_{-1}(T)\), while identifying Ng's conditional framework and Gonek's conjectural target as the relevant anchors. **[LITERATURE]**
Source: `research_notes/rh_goals_2026-08-14/lane_c/S3_DEEP_PRIOR_ART.md`, `Findings`, `Verdict`, and `Summary for Both Items`.

## 1. Introduction

The summatory Möbius function \(M(x)=\sum_{n\le x}\mu(n)\) is connected to the nontrivial zeros of the Riemann zeta function through explicit formulas. The supplied synthesis of Ng's work states that, assuming the Riemann Hypothesis and the Gonek--Hejhal conjecture on negative moments of \(\zeta'(\rho)\), the normalized function \(e^{-y/2}M(e^y)\) has a limiting distribution and that the relevant zero data include sums of the form \(\sum_\rho (|\rho|^2|\zeta'(\rho)|^2)^{-1}\). **[LITERATURE]**
Source: `research_notes/rh_goals_2026-08-14/lane_c/S1_ZERO_SUM_LIT.md`, `Ng's Main Result (2004)` and `Relationship to zero sums`.

The purpose of this paper is narrower: report the numerical determination supported by the supplied zero receipts, test the finite-height behavior of \(J_{-1}(T)\) against Gonek's conjectural coefficient, and document the precision and tail limitations without converting a heuristic extrapolation into a proof. The prior-art search found no published numerical verification of either target, but that novelty statement is scoped to the search record supplied here. **[LITERATURE]**
Source: `research_notes/rh_goals_2026-08-14/lane_c/S3_DEEP_PRIOR_ART.md`, `Verdict` sections and `Implications`.

## 2. The constant

### 2.1 Definition and convention

The computed quantity is the two-sided sum over conjugate zeros \(\rho=1/2+i\gamma\), with term
\[
\frac{1}{(1/4+\gamma^2)|\zeta'(\rho)|^2}.
\]
This is the receipt's weighted summand. **[RECEIPT]**
Negative ordinates contribute the same term, so the two-sided value is twice the positive-ordinate sum. **[RECEIPT]**
Source: `research_notes/rh_goals_2026-08-14/lane_a/zero_sum_receipt.json`, `convention`.

In the Mertens discussion, this zero sum is the conditional mean-square constant suggested by the supplied Ng/Mertens connection; the source literature explicitly warns that the direct equivalence is implicit rather than stated as a standalone theorem. We therefore use “Mertens mean-square constant” as the paper's conditional framework label, not as an unconditional theorem claim. **[LITERATURE]**
Source: `research_notes/rh_goals_2026-08-14/lane_c/S1_ZERO_SUM_LIT.md`, `Ng's Main Result (2004)` and `Limitations and Open Questions`, item 4; `research_notes/imported_farey_now/SELBERG_INPUT_DISPROVED.md`, `What IS True About M(n)^2 Mean Square`.

### 2.2 Numerical method

The zero source contains seeds with about **9 decimal digits**. Each used seed was refined by **1** real Newton update on \(\zeta(1/2+i t)\) using PARI/GP **2.17.3** with arbitrary precision through `lfuninit`; the main receipt records `realprecision_digits = 20`. **[RECEIPT]**
Source: `research_notes/rh_goals_2026-08-14/lane_a/zero_sum_receipt.json`, `source`.

The V2 run used **10000** refined zeros, enforced the strict residual gate \(10^{-15}\), observed maximum residual \(1.32504\times10^{-16}\), and recorded **0** failures. **[RECEIPT]**
Source: `research_notes/rh_goals_2026-08-14/lane_a/ZERO_SUM_V2_REPORT.md`, `Residual and source checks`.

The finite part at \(N=10000\) is a positive partial sum of \(0.014507394686525\), hence a two-sided partial sum of \(0.029014789373050\) under the audited convention. **[RECEIPT]**
Source: `research_notes/rh_goals_2026-08-14/lane_a/ZERO_SUM_V2_REPORT.md`, `Partial sum and tail`, row `N = 10000`.

The convention audit reconciles the earlier E5-style one-sided computation: at \(N=100\), the independently reproduced positive sum is \(0.014143636055307528\), matching the displayed E5 value \(0.0141436361\) to absolute difference \(4.4692471945495527\times10^{-11}\); the corresponding two-sided value is \(0.028287272110615058\), with convention factor **2**. **[RECEIPT]**
Source: `research_notes/rh_goals_2026-08-14/lane_a/zero_sum_receipt.json`, `E5_reproduction`.

### 2.3 Central and conservative tail model

The tail calculation uses the average zero density
\[
\frac{dN}{dt}\simeq \frac{\log(t/(2\pi))}{2\pi}
\]
This density convention is copied from the supplied tail model. **[RECEIPT]**
and integrates the observed block mean of \(1/|\zeta'(\rho)|^2\) against the weighted density. The supplied V2 report fits the Gonek-scaled block model on **500-zero** blocks whose lower endpoint has \(N\ge5001\). **[RECEIPT]**
Source: `research_notes/rh_goals_2026-08-14/lane_a/ZERO_SUM_V2_REPORT.md`, `Partial sum and tail`; `zero_sum_receipt.json`, `tail_model`.

At \(T=9877.7826540055011428\), the fitted central one-sided tail is \(8.97086399804113\times10^{-6}\), while the conservative envelope tail is \(1.2835990468773\times10^{-5}\). The envelope is a numerical extrapolation, not a theorem-level bound against an unseen unusually small zeta derivative. **[FITTED-TAIL]**
Source: `research_notes/rh_goals_2026-08-14/lane_a/ZERO_SUM_V2_REPORT.md`, `Partial sum and tail`, `T` and tail fields, and `Error budget`.

Combining the finite two-sided sum with the central tail gives the reported estimate
\[
S=0.029032731101\pm1.79\times10^{-5},
\]
with the displayed estimate understood as a fitted-tail result. **[FITTED-TAIL]**
and the tail-supported precision claim is **3 significant digits**; the displayed decimal places are not all certified significant digits. **[FITTED-TAIL]**
Source: `research_notes/rh_goals_2026-08-14/lane_a/ZERO_SUM_V2_REPORT.md`, `Verdict` and `Partial sum and tail`.

### 2.4 An internally refuted normalization as a control

The earlier \((6/\pi^2)\log x+O(1)\) input for \(\sum_{n\le x}M(n)^2/n^2\) is explicitly marked false in the supplied cautionary audit. At \(N=500000\), that audit records observed value \(2.257\) versus claimed value \(7.977\), with ratio \(0.28\); it attributes the error to confusing \(\mu(n)^2\) with \(M(n)^2\). **[RECEIPT]**
Source: `research_notes/imported_farey_now/SELBERG_INPUT_DISPROVED.md`, `The Claim (FALSE)`, `Root Cause`, and `Numerical Evidence`.

This control is not evidence for the numerical value of \(S\). It is included because the same cautionary audit records a mean-square scale near \(0.03\) under the RH formulation and warns that the squarefree constant \(6/\pi^2\) must not be substituted for the Mertens mean-square quantity. **[RECEIPT]**
Source: `research_notes/imported_farey_now/SELBERG_INPUT_DISPROVED.md`, `Root Cause` and `What IS True About M(n)^2 Mean Square`.

### 2.5 Pending \(N=10^5\) extension

The next zero-sum checkpoint is reserved for the concurrent `lane_a/a5_checkpoints` run. No value is inserted until that run supplies the boundary ordinate, finite sums, tail values, and final estimate. **[FITTED-TAIL]**
Source expected: `research_notes/rh_goals_2026-08-14/lane_a/a5_checkpoints/`; the directory exists but contains no checkpoint files at assembly time.

| Quantity at \(N=10^5\) | Value to insert |
|---|---:|
| Boundary ordinate \(T_{10^5}\) | `{{PLACEHOLDER}}` **[RECEIPT]** |
| Positive partial sum | `{{PLACEHOLDER}}` **[RECEIPT]** |
| Two-sided partial sum | `{{PLACEHOLDER}}` **[RECEIPT]** |
| Central one-sided tail | `{{PLACEHOLDER}}` **[FITTED-TAIL]** |
| Conservative one-sided tail | `{{PLACEHOLDER}}` **[FITTED-TAIL]** |
| Final two-sided estimate and tail bar | `{{PLACEHOLDER}}` **[FITTED-TAIL]** |

## 3. The Gonek test

### 3.1 Target and observable

For positive ordinates, define
\[
J_{-1}(T)=\sum_{0<\gamma\le T}\frac{1}{|\zeta'(1/2+i\gamma)|^2}.
\]
This is the receipt's positive-ordinate observable. **[RECEIPT]**
The literature target is Gonek's conjectural asymptotic \(J_{-1}(T)\sim(3/\pi^3)T\). **[LITERATURE]**
Source: `research_notes/rh_goals_2026-08-14/lane_c/S1_ZERO_SUM_LIT.md`, `Gonek's Prediction (1999)`; `S3_DEEP_PRIOR_ART.md`, `Item 2`.

The numerical receipt uses target coefficient \(3/\pi^3=0.09675460329959848\). The formula is the literature claim; the decimal used for the ratios below is the receipt's computed target field. **[LITERATURE] [RECEIPT]**
Source: formula: `research_notes/rh_goals_2026-08-14/lane_c/S1_ZERO_SUM_LIT.md`, `Gonek's Prediction`; decimal: `research_notes/rh_goals_2026-08-14/lane_a/j_minus1_receipt.json`, `gonek_target`.

### 3.2 Checkpoint table

The following rows are direct values from `j_minus1_receipt.json`; the ratio column is the receipt's `ratio_to_3_over_pi_cubed` field. **[RECEIPT]**

| (N) | (T) | (J_{-1}(T)) | (J_{-1}(T)/T) | ratio to (3/\pi^3) | provenance |
|---:|---:|---:|---:|---:|---|
| 500 | 811.1843588465063 | 75.4356028892844 | 0.09299440018364365 | 0.961136700604193 | [RECEIPT] `table[N=500]` |
| 1000 | 1419.4224809459956 | 134.83699664700254 | 0.09499426594761158 | 0.9818061643378759 | [RECEIPT] `table[N=1000]` |
| 3000 | 3533.3282433958198 | 314.3534700786436 | 0.08896809139264232 | 0.9195230858128228 | [RECEIPT] `table[N=3000]` |
| 5000 | 5447.8619983012995 | 514.4992844744717 | 0.0944405869008609 | 0.9760836557659973 | [RECEIPT] `table[N=5000]` |
| 10000 | 9877.782654005501 | 906.8867748480101 | 0.09181076427919398 | 0.9489033198234919 | [RECEIPT] `table[N=10000]` |
| (10^5) | `{{PLACEHOLDER}}` | `{{PLACEHOLDER}}` | `{{PLACEHOLDER}}` | `{{PLACEHOLDER}}` | [RECEIPT] expected from `lane_a/a5_checkpoints` |

### 3.3 Fit, drift, and interpretation

The through-origin fit is \(J_{-1}(T)=aT\) over the **11** completed checkpoints with \(N\) from **5000** through **10000**. It gives \(a=0.09278191769461815\), target-slope ratio \(0.9589406036560452\), and difference from target \(-0.003972685604980333\). **[RECEIPT]**
Source: `research_notes/rh_goals_2026-08-14/lane_a/j_minus1_receipt.json`, `top_half_linear_fit`.

The block-slope scatter is \(0.01455394223541028\). The first and last three-block means are \(0.1020814566917632\) and \(0.08667512503767985\), respectively, a difference of \(-0.015406331654083352\) against a detection threshold of \(0.00727697111770514\); the receipt therefore flags drift. **[RECEIPT]**
Source: `research_notes/rh_goals_2026-08-14/lane_a/j_minus1_receipt.json`, `top_half_linear_fit.chunk_slope_scatter_std` and `chunk_slope_drift`.

The observed finite-height behavior is therefore compatible in scale with the conjectural coefficient but trends below it in the upper-window diagnostic. The receipt verdict is **TOO EARLY**: finite-(T) corrections are expected to be large, \(T\) approximately \(10^4\) is described as far too low for a definitive asymptotic claim, and the scatter is not a confidence interval or theorem-level error bar. **[RECEIPT]**
Source: `research_notes/rh_goals_2026-08-14/lane_a/j_minus1_receipt.json`, `verdict`, `caveats`, and `uncertainty_note`.

The pending (N=10^5) row is intended to extend this table, not to retroactively change the present verdict. Its four values are reserved above and must be filled from the concurrent checkpoint artifact before any updated interpretation is written. **[RECEIPT]**
Source expected: `research_notes/rh_goals_2026-08-14/lane_a/a5_checkpoints/`.

## 4. Closed-form exclusions

The supplied V2 comparison uses the central estimate and expresses each candidate's absolute residual in units of the final conservative one-sigma-style tail bar. The resulting sigma distances are diagnostic distances from the fitted numerical estimate, not statistical confidence levels. **[FITTED-TAIL]**
Source: `research_notes/rh_goals_2026-08-14/lane_a/ZERO_SUM_V2_REPORT.md`, `Candidate closed forms` and `Error budget`.

| candidate | candidate value | absolute residual | sigma distance | status |
|---|---:|---:|---:|---|
| (2/\pi^2) | 0.202642367285 | 0.17361 | 9676.31 | excluded by the reported comparison **[FITTED-TAIL]** |
| (3/\pi^4) | 0.0307979467641 | 0.00176522 | 98.386 | excluded by the reported comparison **[FITTED-TAIL]** |

The literature synthesis separately reports that (2/\pi^2\) was not found in the zeta-zero, Gonek--Hejhal, or Mertens-function literature, and that no closed form for the relevant (J_{-1}) constant is known there beyond the conjectural coefficient. **[LITERATURE]**
Source: `research_notes/rh_goals_2026-08-14/lane_c/S1_ZERO_SUM_LIT.md`, `Does 2/π² Appear?`, `Summary`, and `Limitations and Open Questions`.

The exclusion of (2/\pi^2) is thus both numerical for the present (S) estimate and cautionary about provenance: it is not a replacement for a derived theorem. The (3/\pi^4) comparison is likewise a numerical candidate test, not a claim that the literature proposed that form. **[FITTED-TAIL]**
Source: `research_notes/rh_goals_2026-08-14/lane_a/ZERO_SUM_V2_REPORT.md`, `Candidate closed forms`.

## 5. Limitations

1. The tail envelope is a numerical average-growth extrapolation and is not a rigorous theorem-level bound against an unseen unusually small value of \(|\zeta'(\rho)|\). **[FITTED-TAIL]**
   Source: `research_notes/rh_goals_2026-08-14/lane_a/ZERO_SUM_V2_REPORT.md`, `Partial sum and tail`, and `research_notes/rh_goals_2026-08-14/lane_a/zero_sum_receipt.json`, `tail_model.interpretation`.
2. The zero seeds have about **9 decimal digits**, and the inherited range through (N=3000) was not fully per-zero propagated with \(\zeta''\) data; the receipt does provide residual gates and a higher-precision displayed-sum cross-check. **[RECEIPT]**
   Source: `zero_sum_receipt.json`, `source`; `ZERO_SUM_V2_REPORT.md`, `Error budget`, inherited-seed note.
3. The V2 report claims only **3 significant digits** for the infinite sum, even though finite sums carry more backend digits. **[FITTED-TAIL]**
   Source: `ZERO_SUM_V2_REPORT.md`, `Verdict`; `zero_sum_receipt.json`, `final_estimate.precision_claim`.
4. The Gonek test reaches (T\approx10^4), which the receipt calls far too low for a definitive asymptotic claim; its drift statistic is a finite-height diagnostic, not a hypothesis test. **[RECEIPT]**
   Source: `j_minus1_receipt.json`, `caveats`, `chunk_slope_drift.note`, and `uncertainty_note`.
5. The Mertens mean-square bridge is presented conditionally and the supplied literature synthesis says that a direct standalone theorem for the exact equivalence has not been located. **[LITERATURE]**
   Source: `S1_ZERO_SUM_LIT.md`, `Ng's Main Result (2004)` and `Limitations and Open Questions`, item 4.
6. “No prior numerical found” is a conclusion of the supplied search record, not a universal proof that no unpublished or unindexed computation exists. **[LITERATURE]**
   Source: `S3_DEEP_PRIOR_ART.md`, `Search completeness` and both `NO-PRIOR-NUMERIC-FOUND` verdicts.
7. The (N=10^5) extension is unavailable at assembly time; no value is inferred from the (N=10000) data. **[RECEIPT]**
   Source expected: `research_notes/rh_goals_2026-08-14/lane_a/a5_checkpoints/`; the current directory is empty.

## 6. Reproducibility appendix

### A. Source receipts

The weighted zero-sum computation is anchored to `zero_sum_receipt.json` and the updated `ZERO_SUM_V2_REPORT.md`; the Gonek checkpoint table and fit are anchored to `j_minus1_receipt.json`. The literature boundary is recorded in `S1_ZERO_SUM_LIT.md` and `S3_DEEP_PRIOR_ART.md`, and the failed normalization is retained from `SELBERG_INPUT_DISPROVED.md`. **[RECEIPT] [LITERATURE]**
Source: the six files named in this paragraph.

The V2 report records source SHA-256 `3436c916a7878261ac183fd7b9448c9a4736b8bbccf1356874a6ce1788541632`, **10000** refined zeros, maximum residual `1.32504e-16`, strict threshold `1e-15`, and **0** failures. **[RECEIPT]**
Source: `research_notes/rh_goals_2026-08-14/lane_a/ZERO_SUM_V2_REPORT.md`, `Residual and source checks`.

### B. Reproduction commands

The supplied report gives the following commands for reproducing the V2 calculation and its backend cross-check. **[RECEIPT]**

```bash
python3 research_notes/rh_goals_2026-08-14/lane_a/zero_sum_v2_driver.py --nmax 10000
python3 research_notes/rh_goals_2026-08-14/lane_a/zero_sum_v2_backend_crosscheck.py --nmax 10000
python3 research_notes/rh_goals_2026-08-14/lane_a/analyze_zero_sum_v2.py
```

The command lines and their **10000**-zero scope are copied from the supplied report; they are not a claim that this skeleton reran them. **[RECEIPT]**
Source: `research_notes/rh_goals_2026-08-14/lane_a/ZERO_SUM_V2_REPORT.md`, `Reproduction`.

### C. Precision and cross-check record

The inherited receipt records a separate `realprecision=30` run through (N=1000) with the same displayed partial sums and maximum residual `5.51057192390154456003139059199e-35`. The V2 report records a backend cross-check contribution of `4.90891e-25`, maximum single-chunk difference `4.74178e-26`, A4 first-order seed/root propagation of `2.12783e-21` two-sided, and maximum A4 root displacement `4.99361e-17`; the report states that the tail term dominates these measured numerical budgets. **[RECEIPT]**
Source: `research_notes/rh_goals_2026-08-14/lane_a/zero_sum_receipt.json`, `source.high_precision_crosscheck`; `ZERO_SUM_V2_REPORT.md`, `Error budget`.

The requested `mpmath` path was unavailable in the supplied Python environment because installation was blocked by DNS/network sandboxing; the receipt records PARI/GP as the fallback rather than hiding that deviation. **[RECEIPT]**
Source: `research_notes/rh_goals_2026-08-14/lane_a/zero_sum_receipt.json`, `source.requested_mpmath`.

### D. Convention and output audit

The E5 reproduction used positive zeros only, the denominator \(|\rho|^2=1/4+\gamma^2\), and no conjugate term; the present paper reports the natural two-sided sum and records the factor-of-**2** conversion explicitly. **[RECEIPT]**
Source: `research_notes/rh_goals_2026-08-14/lane_a/zero_sum_receipt.json`, `convention` and `E5_reproduction`.

Before publication, the owner should replace every (N=10^5) marker with the matching `lane_a/a5_checkpoints` receipt field, rerun the numerical/provenance checks, and decide whether the resulting precision supports any change to the wording above. Author, affiliation, venue, and submission fields remain **[OWNER-GATED]**. **[RECEIPT]**
Source expected: `research_notes/rh_goals_2026-08-14/lane_a/a5_checkpoints/`; the directory is currently empty, and editorial decisions are intentionally outside this assembly task.

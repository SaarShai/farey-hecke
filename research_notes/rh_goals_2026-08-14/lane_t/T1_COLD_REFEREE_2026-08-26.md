# Cold adversarial referee report — T1 information-cost law

Date: 2026-08-26  
Object reviewed: `T1_CRAMER_RAO_DRAFT.md`, including the final “GAPS LEDGER UPDATE 2026-08-26”, with full reads of `T1_GAP4_LEMMA1_RESTATEMENT.md`, `T1_GAP7_VAN_TREES.md`, `T1_GAP9_STATIONARY_EXTENSION.md`, `T1_GAP11_YT_INTERPRETATION.md`, `T1_GAP13_D_DEPENDENCE.md`, `T1_GAP16_RIESZ_IMPORT.md`, and `T1_GAP17_PROPAGATION.md`.

## Executive ruling

The headline arithmetic is mostly correct after the appended Berry–Esseen correction. The law is nevertheless not promotable. The decisive failures are structural:

1. Proposition 4.4 smooths a randomly marked point process as though its mark were a deterministic continuous function. Under the draft's own (M3), the spectral density contains a conditional second mark moment, so the claimed cancellation of `1/|ζ′(ρ)|` does not follow.
2. The final “Gaussian-score class” restriction does not establish a lower bound. Godambe's sandwich is an asymptotic covariance formula for a specified estimating-equation root, not an information inequality for every function of a Gaussian score. A nonlinear function of the score can exploit its non-Gaussian density.
3. Van Trees produces a Bayes-average bound under an oracle-centred, shrinking prior. It does not replace the draft's pointwise frequentist theorem. The raised-cosine density itself is admissible; the claimed transfer of its bound is not.
4. The numerical operating point `Γ=50`, `T=log(3·10^7)`, `K=4`, `d=10` violates (M5), and the claimed global (B1) inequality fails at `γ_1` and has never been checked for the full `3d` Fisher matrix.
5. The body still states the pre-update theorem (“any unbiased estimator”, uniform in `d`, GAP-4 open, GAP-16 underived), while the update asserts incompatible replacements. Mandatory Prop. R hypotheses are not carried at its principal uses.

## Independent arithmetic audit

I recomputed the requested constants from the displayed formulas, using

`T = log(3·10^7) = 17.2167079396264`, `K=4`, `γ_d=49.773832`, and
`L_d=log(γ_d/2π)=2.06961231767041`.

| Quantity | Independent value | Ruling |
|---|---:|---|
| `√6` | `2.44948974278318` | Correct. It is the formal local-Gaussian coefficient `sqrt(24/4)`, not yet a proved coefficient for the stated N2 marked-noise experiment. |
| `r_d=6L_d/(K²T)` | `0.0450785726196` | `r_d ≤ 0.0451` is correct upward rounding. |
| `√6/sqrt(1+r_d)` | `2.39607911365821` | `2.395` is a safe, deliberately coarse downward rounding; it is not the nearest rounding. |
| van-Trees RMSE floor | `0.0482525739896` | `0.0482` is a safe downward rounding. |
| uncorrected Gaussian-model floor | `0.0493281646573` | `0.04933` is correct. |
| `(6L_d)^(1/3)` | `2.31568820531328` | `2.3157` is correct. |
| asymptotic `Λ(50)` | `0.156591636223` | `0.157` is correct upward rounding. |
| exact-Riesz mean-field quadrature `Λ(50)` | `0.156523843835` | Consistent with the draft's `0.1565`. |
| asymptotic mean-field `ρ/σ³` | `0.269231061456` | Consistent with `0.2692`. |
| `0.56 ρ/σ³` | `0.150769394415` | `d_K ≤ 0.151` is correct rounding **inside the asymptotic intensity-smoothed scalar model only**. Exact-Riesz mean-field quadrature gives `0.150740107934`. It is not a proved bound for the discrete marked tail, the efficient score, or path space. |

For the GAP-4 exponential factors, direct evaluation of
`exp(16πK/(γ_jT))` gives:

| `j` | exact value | ledger's upward value |
|---:|---:|---:|
| 1 | `2.28465187394` | `2.29` |
| 2 | `1.74285857133` | `1.75` |
| 3 | `1.59508865579` | `1.60` |
| 4 | `1.46791144838` | `1.47` |
| 5 | `1.42558994729` | `1.43` |
| 10 | `1.26443750287` | `1.27` |

The arithmetic passes. The claim that these numbers are rigorous ceilings does not; see Defect 8.

## Numbered defects

### 1. SEVERITY BLOCKING — the spectral-density calculation drops the random mark law

**Location.** Draft (M3), lines 152–154; Theorem T1-b, lines 267–277; Proposition 4.4, lines 782–809; §7.2, lines 1041–1059. The supporting GAP-9 note identifies the hidden mean-field convention at lines 106–120 and 158–163.

**Defect.** Under (M3), `a_γ=|M_W(1/2+iγ)| r_γ` and `r_γ` is drawn from a truncated empirical law. Smoothing the marked atomic measure therefore gives

`S_ε(ω)=|M_W(1/2+iω)|² E[r_γ² | γ=ω] log(ω/2π)`,

not `a_ω² log(ω/2π)` with the particular target mark silently reused at a nonzero-free frequency. Consequently

`S_ε(γ_j)/a_{γ_j}² = E[r²|γ_j] log(γ_j/2π)/r_j²`,

so the window factor cancels but the `ζ′` mark does not. The divergent/sensitive second moment is exactly the quantity Proposition 4.4 needs. The headline claim “no dependence on `1/|ζ′(ρ)|`” is not derived from N2 as stated. The ledger's admission that the numerics use `r_ω≡1` confirms that the verified constants belong to a different mean-field model.

**Suggested repair.** Choose and state one model: (i) deterministic continuous marks `r(ω)` with an explicit interpolation and no random (M3), or (ii) a marked point process with `m_2(ω)=E[r²|ω]`. Re-derive `S_ε`, the truncation sensitivity, `Λ`, (B1), and the headline coefficient under that model. Do not claim amplitude cancellation beyond the deterministic window factor.

### 2. SEVERITY BLOCKING — fixed covariance and amplitude cancellation cannot both hold under the current parametrisation

**Location.** Draft §1.5, lines 183–191; §3, lines 298–301; (R2)–(R4), lines 356–385; T1-b, lines 267–277.

**Defect.** The CR derivation assumes a covariance operator `C` independent of `θ`, while `θ` includes the unknown target amplitudes `A_j=2a_{γ_j}` and target locations. If `S_ε(γ_j)` is identified with the same `a_{γ_j}²` to obtain cancellation, `C` depends on `A_j` (and on `γ_j`). The Gaussian Fisher information then contains covariance-derivative terms, and the mean-only Gram matrix (4.0) is incomplete. If `C` is instead fixed by an ensemble mean-field profile, the particular nuisance amplitude `A_j` does not cancel, as in Defect 1.

**Suggested repair.** Specify whether target marks are fixed parameters or tied to the covariance law. If covariance varies, include the Gaussian covariance-information term and redo regularity and van Trees. If covariance is fixed, retain the explicit target-amplitude ratio in the bound.

### 3. SEVERITY BLOCKING — the Gaussian-score/Godambe quantifier does not rescue a lower bound

**Location.** Ledger update line 1189; `T1_GAP17_PROPAGATION.md` lines 181–217 and 501–508.

**Defect.** Godambe's sandwich gives the asymptotic covariance of the root of a specified estimating equation under regularity. It is not a nonasymptotic van-Trees or Cramér–Rao lower bound for “any estimator that is a function of the Gaussian score.” Even after reducing to a scalar score `S=u+U`, a general function of `S` can exploit the non-Gaussian density of `U`; its location Fisher information is `I(f)≥I_G` by the very Stam correction recorded in the note. Restricting the data to the score therefore does not make the Gaussian information a universal upper bound. At most, the covariance calculation describes the particular linear/quasi-score estimator. The assertion that T2's periodogram-plus-maximisation is, nonasymptotically, such a root is also unproved.

**Suggested repair.** Either (i) restrict to one explicitly defined estimator/estimating equation and prove its finite-sample Bayes MSE directly from its error representation, or (ii) derive an actual information upper bound for the score experiment. Remove “any function of the Gaussian score” and do not label the Godambe sandwich a lower-bound theorem.

### 4. SEVERITY BLOCKING — van Trees changes the risk and uses an oracle-centred local prior

**Location.** `T1_GAP7_VAN_TREES.md` lines 157–166, 217–254, 313–322, 328–366, and 468–481; ledger update line 1184.

**Defect.** The raised-cosine density is formally admissible: it vanishes at its endpoints and has finite prior information `π²/α²`. But the application does not replace the original theorem. The prior is centred at “the true ordinate in the local experiment”, shrinks like `1/T`, and yields a **Bayes-average** MSE over that oracle-centred neighbourhood. It gives neither a pointwise bound at the actual zero nor a uniform frequentist bound. The note itself lists that conversion as OWED-4. Moreover, the displayed equality substitutes the centre Fisher block for `E_π[I(θ)]` while leaving amplitude-prior averaging and coloured/multi-tone variation as OWED items.

**Suggested repair.** State a separate Bayesian theorem with fixed, externally specified centres and fully averaged Fisher matrix. Do not say “unbiasedness is no longer assumed” in the original pointwise T1 law; say instead that a different Bayes-risk law is available. A minimax corollary would require a valid prior lower bound plus a clearly stated parameter set, not oracle knowledge of the target.

### 5. SEVERITY BLOCKING — the draft has not chosen between an exact Gaussian model and the actual phase-sum noise

**Location.** Draft (M4), lines 155–159; (R6), lines 392–449; §8, lines 1142–1176; ledger update line 1189; `T1_GAP17_PROPAGATION.md` lines 112–177.

**Defect.** If (M4) literally **replaces** the tail by a Gaussian process, then the CR law is a theorem only of that stipulated surrogate and finite-`Γ` Berry–Esseen/Stam corrections are irrelevant to the model theorem. If the law is meant to cover the actual random-phase sum, Stam says the Gaussian CR number is not a full-class floor, and Defect 3 shows the proposed class restriction is insufficient. The body still claims “any unbiased estimator” in N2, while the ledger says a Gaussian-score restriction is mandatory. These are different experiments and different quantifiers.

**Suggested repair.** Publish two separately named results: an exact Gaussian-surrogate theorem under (M4), and a non-Gaussian phase-sum result only after a valid transfer theorem. Do not splice the score-class update onto the old Gaussian theorem.

### 6. SEVERITY BLOCKING — (B1) is globally false at the claimed operating point and only per-tone blocks were measured

**Location.** Draft lines 220–250, 597–639, 833–847, 1155–1169; GAP-14 ledger row line 999; `T1_GAP13_D_DEPENDENCE.md` lines 394–399.

**Defect.** The theorem defines (B1) for the full Fisher Gram matrices. The draft then says `(B1) HOLDS`, but reports `λ_max=0.587>0.25` at `γ_1`. Thus the stated sufficient hypothesis fails even on a coordinate block. Measurements at `γ_d` do not prove the full `3d×3d` Loewner inequality, and the reported inverse-entry deficits are numerical observations, not a substitute proof of the matrix comparison used in Theorem T1. “Inside `O(K^{-1})` with implied constant 1.03” is especially weak because the theorem never supplies that constant or controls cross-tone accumulation.

**Suggested repair.** Compute and receipt the global generalized eigenvalue for the full nuisance-parameter matrix at an (M5)-admissible cut. If it fails, state a per-tone theorem with per-tone hypotheses and explicit correction factors; do not close GAP-14 globally.

### 7. SEVERITY BLOCKING — the advertised `Γ=50` operating point violates (M5)

**Location.** Draft (M5), lines 173–174; lines 535–540, 567–568, and all `Γ=50` finite-`Γ` claims; `T1_GAP9_STATIONARY_EXTENSION.md` lines 287–295; `T1_GAP13_D_DEPENDENCE.md` lines 254–269.

**Defect.** At `T=17.21670794`, `K=4`, `γ_10=49.773832`,

`T(50-γ_10)=3.89387 < 2πK=25.13274`.

The cut must satisfy `Γ≥51.23361986` (and `Γ<γ_11`). Therefore `Γ=50` is not an operating point of Theorem T1. The draft sometimes supplies `Γ=51.234` as an “M5-tight” alternative, but continues to headline `Λ(50)`, `d_K(50)`, and the `Ω=100` leakage results as theorem-operating values.

**Suggested repair.** Use one admissible cut consistently, recompute every dependent finite-`Γ` quantity there, and label `Γ=50` only as an out-of-theorem diagnostic if retained.

### 8. SEVERITY MAJOR — GAP-4 is declared closed by a non-rigorous “ceiling” and its correction is absent from T1

**Location.** Draft lines 695–720, GAP-4 ledger row line 990, update line 1183; `T1_GAP4_LEMMA1_RESTATEMENT.md` lines 90–122, 155–198, and 210–226.

**Defect.** The supporting note explicitly drops `r(ω)=D(ω)+4/ω`, replaces a supremum over `[γ_j-h,γ_j+h]` by `4/γ_j`, and calls the result valid only “modulo” an OWED remainder. It says it “does not attempt to close GAP-4”; the appended verification nevertheless closes it. Numerical domination of six measured values is not a proof of a ceiling. Even if repaired, the flatness error is `O(K/(γ_jT))`, not the theorem's sole `O(K^{-1})`, and at the operating point the near-tone inverse differs by about 8%.

**Suggested repair.** Bound the exact derivative `D` on the entire interval, with an explicit condition `γ_j>h`, and insert the resulting multiplicative factor into the theorem. Reopen GAP-4 until that exact inequality and its propagation through inversion are proved.

### 9. SEVERITY MAJOR — Lemma 1's Plancherel statement is ill-typed for the functions used

**Location.** Draft Lemma 1, lines 680–693, and scope warning lines 722–730; GAP-4 restatement lines 157–181.

**Defect.** If `u,v` have Fourier support in the near-tone band, Plancherel yields a full-line time integral, not `∫_0^T uv`. If `u,v` are the derivatives restricted to `[0,T]`, their Fourier transforms have full support. A nonzero function cannot be both compactly time-supported and compactly frequency-supported. The draft acknowledges the derivative tails but does not repair the lemma's function spaces or the equality used to import the white-noise 3×3 block.

**Suggested repair.** Define frequency-projected derivatives explicitly, use the full-line Plancherel norm for those projections, and prove the comparison between their Gram block and the original time-domain block. Then combine it with a valid global leakage estimate.

### 10. SEVERITY MAJOR — the `d`-uniform theorem and last-tone attainment are underived

**Location.** Draft lines 264–289, Lemma 3 lines 769–780, proof lines 842–860; GAP-13 row line 1003 and update line 1188; `T1_GAP13_D_DEPENDENCE.md` lines 287–359 and 363–422.

**Defect.** Pairwise `O(K^{-1})` cross-block bounds do not imply a dimension-uniform operator bound; row sums can grow like `log d/K` or worse after coloured weighting and nuisance normalization. The supporting note explicitly says only fixed-`d` `O_d(K^{-1})` is supported, that last-tone attainment after corrections is OWED, and that the near-tone intervals overlap under the stated (M5). The body still says “uniformly in d” and “attained at `j=d`.” Closing only the elementary `γ_d` dependence does not close this matrix problem.

**Suggested repair.** Replace uniformity by fixed-`d` with an explicit `C(d,K)`, or prove the needed confluent frame bound for the full coloured nuisance family. Partition overlapping bands or strengthen the separation hypothesis.

### 11. SEVERITY BLOCKING — Prop. R's mandatory hypotheses are not carried at its principal uses

**Location.** Draft §1.1 lines 81–109, especially “Under RH ... exactly” at line 95; theorem hypotheses lines 252–257; §8 lines 1142–1176; GAP-11 update line 1186. The complete disclosure appears only inside the long GAP-16 row at line 1001.

**Defect.** Prop. R is conditional on **RH, simplicity of every nontrivial zero, and the conjectural Gonek–Hejhal bound** `J_{-1}(T)=Σ|ζ′(ρ)|^{-2}=O(T)`. The main observable, exact line-spectrum claim, theorem statement, and same-observable validation do not carry all three. Saying “under RH ... exactly” is materially false relative to the imported proposition. The theorem's N2 simple point-process clause is not a disclosure that the arithmetic explicit formula assumes simplicity of the actual zeta zeros and a conjectural moment bound.

**Suggested repair.** Put the three assumptions in §1.1 immediately before (1.1), in the theorem if the arithmetic realization is part of the theorem, in §8's claim summary, and at every empirical use of Prop. R. Distinguish the finite Lean algebra from the unformalized cited contour analysis.

### 12. SEVERITY MAJOR — Prop. R status and the continuous-record observable contradict the body

**Location.** Draft lines 99–109 and 1170–1176 versus GAP-16 row line 1001 and final update; `T1_GAP16_RIESZ_IMPORT.md` lines 194–213.

**Defect.** The older body still says the order-1 Riesz formula “has not been re-derived” and cannot be claimed, whereas the ledger says it is closed at citation+Lean standing. Separately, Prop. R is stated for integer `N`, and the exact Cesàro identity is integer-valued; T1 assumes a continuous record for every `t∈[0,T]` with `N=e^t`. The Mellin formula may extend to real `N`, but the cited proposition and the displayed `(1/N)Σ_{k<N}M(k)` identity do not presently establish that continuous experiment.

**Suggested repair.** Reconcile the status in the body. State and prove/cite the real-`N` Riesz formula needed for continuous `t`, or define an interpolation/sampling experiment and redo the continuous-information comparison.

### 13. SEVERITY MAJOR — `d_K≤0.151` is not a certified misspecification bound for the experiment used by T1

**Location.** Ledger update line 1189; `T1_GAP17_PROPAGATION.md` lines 64–108 and 529–584; referenced `T1_GAP17_BERRY_ESSEEN_DRAFT.md` lines 29–38 and appended correction.

**Defect.** The rounded arithmetic is correct, but it comes from intensity integrals, the asymptotic substitution `a_ω=ω^{-2}`, and the mean-field mark `r_ω=1`. It is a scalar fixed-time bound, not a bound for the efficient score or the approximately 548-dimensional band-limited path. The propagation note names the score transfer as H-score-BE/OWED-1. Thus the ledger promotes a conditional approximation to a headline `d_K` bound. The original Berry–Esseen body also still displays the wrong `σ²`, `0.0135`, and reversed Fisher direction; only appended corrections repair the reading.

**Suggested repair.** Label `0.151` “mean-field scalar approximation,” not a certified bound. Compute the exact marked discrete Lyapunov ratio for the whitened profiled score at an M5-admissible cut, with the truncation level specified, and replace rather than append-correct the erroneous source displays.

### 14. SEVERITY MAJOR — the full-class `√m` route assumes a positive ratio that the note says is zero

**Location.** `T1_GAP17_PROPAGATION.md` lines 324–403 and 541–546; ledger update line 1189.

**Defect.** The phase sum has bounded support and a density that vanishes at its support edge, while the truncated Gaussian reference remains positive there. Hence the essential infimum `m=ess inf f/φ^R` on the whole support is zero, as the note itself acknowledges. The displayed full-class `√m` version is therefore vacuous for the stated noise, not merely awaiting a numerical estimate. A bulk ratio plus tail control is a different, still-open result.

**Suggested repair.** Remove the suggestion that H-ratio supplies a viable full-class theorem for the current density. Develop the bulk-plus-tail inequality or an independent Fisher-information upper bound before stating a multiplicative law.

### 15. SEVERITY MAJOR — the stationary fill is an order-one modelling replacement, not Proposition 4.4 evaluated at a target

**Location.** Draft lines 513–524, Proposition 4.4 lines 782–826, §7.3 lines 1062–1096; `T1_GAP9_STATIONARY_EXTENSION.md` lines 12–41, 144–183, and 301–409.

**Defect.** Proposition 4.4 derives a tail spectrum only for `|ω|>Γ`; every target has `γ_j<Γ`. The positive `S_ε(γ_j)` is supplied entirely by (M4)'s support fill. GAP-9 proves that, for fixed low targets, actual tail leakage is `O(T^{-1})` while the fill converges to the full positive floor and changes the Gaussian experiment across a Cameron–Martin singularity. Calling `S_ε(γ_j)=...` a window-independent consequence of Proposition 4.4 overstates an unvalidated modelling extension.

**Suggested repair.** Attribute the target-frequency floor explicitly to an N2 regularizing assumption, not to the tail spectral calculation. Keep GAP-9 open for any claim connecting the law to a fixed zeta configuration; do not call it non-blocking outside the stipulated Gaussian surrogate.

### 16. SEVERITY MAJOR — the empirical “violation” is not a violation of an RMSE lower bound, and GAP-11 remains internally contradictory

**Location.** Draft lines 913–948; GAP-11 row line 997 and update line 1186; `T1_GAP11_YT_INTERPRETATION.md` lines 32–56 and 58–68.

**Defect.** A single realized absolute error below an RMSE lower bound is not a violation; RMSE is an expectation. No estimator-class explanation is needed for that elementary point. Moreover, the supporting note says the Gate-1/T1-bound apples-to-oranges comparison “remains open and is untouched,” while the ledger marks GAP-11 resolved. The same-observable result concerns the **amplitude** `0.006287349` versus Prop. R's predicted amplitude, not the Gate-1 location-error comparison.

**Suggested repair.** Remove “violates the bound.” Compare empirical MSE over a declared ensemble if available. Split GAP-11 into amplitude validation (resolved, conditional on Prop. R) and Gate-1 risk comparison (not established).

### 17. SEVERITY MAJOR — `ε` denotes two incompatible objects

**Location.** Draft §1.1 lines 84–109 and (R6)/Proposition 4.4 lines 392–440 and 782–797.

**Defect.** In §1.1, `ε(t)` is the contour-shift remainder left after summing **all** zeros. Later, `ε(t)=2Σ_{γ>Γ}a_γ cos(...)` is the stochastic high-zero interference. The likelihood then uses only the latter covariance and silently drops the former. This notation masks an additional deterministic/model-error term and makes statements such as “ε is Gaussian” ambiguous.

**Suggested repair.** Use distinct symbols, e.g. `E_Riesz(t)` for the Prop. R remainder and `η_Γ(t)` for tail interference. State how the former enters the mean/noise model and why it is negligible uniformly on the observation range, with Prop. R's full assumptions.

### 18. SEVERITY MAJOR — the displayed lower bounds hide unsigned and unquantified error terms

**Location.** Theorem lines 259–285; Lemma 3 lines 769–780; proof lines 833–863.

**Defect.** A statement `Var≥(24+O(K^{-1}))·...` has no usable lower-bound content without the sign and a constant. The proof also has separate flatness `O(K/(γT))`, time-window `O(1/(γT))`, band-truncation `O(1/(ΔT))`, cross-tone/dimension, van-Trees, and leakage errors. They cannot all be silently renamed `O(K^{-1})` under the stated hypotheses. The numerical cancellation between `+8%` local flatness and `−8.6%` leakage is not a proof of the nominal constant.

**Suggested repair.** State an explicit product/additive lower factor with named nonnegative constants and validity conditions. Only after proving each term may an asymptotic corollary display `√6`.

### 19. SEVERITY MAJOR — the final ledger does not update or consistently supersede the draft

**Location.** Draft status/count lines 966–983; GAP rows 990–1003; §7–§8 lines 1007–1176; final update lines 1181–1191.

**Defect.** The document simultaneously says:

- GAP-4 is open and closed;
- unbiasedness is required and no longer assumed;
- GAP-9 remains an unproved load-bearing idealization and is merely “addressed/non-blocking”;
- GAP-11 remains apples-to-oranges and is resolved;
- the correction is uniform in `d` and only fixed-`d` is supported;
- GAP-16 is underived and closed at citation+Lean standing;
- the law covers any unbiased estimator and only a Gaussian-score class;
- GAP-17 is an open finite-`Γ` rate problem and closed-at-class-restricted.

The “17 entries, 4 closed, 13 open” count is also obsolete after the appended wave. A reader cannot determine the actual theorem by treating the update as an informal overlay.

**Suggested repair.** Produce a clean v4 rather than appending another ledger. Rewrite the headline, hypotheses, theorem, proof, numerical section, claim/not-claim section, and a single current ledger. Delete superseded statements.

## Minimum conditions for reconsideration

Reconsideration requires, at minimum:

1. a coherent marked-amplitude model and a re-derived spectral density;
2. a choice between the exact Gaussian surrogate and the actual non-Gaussian phase sum;
3. a valid risk theorem with one unambiguous quantifier (pointwise CR, Bayes van Trees, minimax, or a theorem for one named estimating equation);
4. an M5-admissible operating point and a global full-matrix leakage verification;
5. an exact GAP-4/Fisher-error propagation with explicit signed constants;
6. the full RH+simplicity+Gonek–Hejhal disclosure at every Prop. R use; and
7. a clean integrated draft with no superseded theorem text.

VERDICT: NOT-PROMOTABLE

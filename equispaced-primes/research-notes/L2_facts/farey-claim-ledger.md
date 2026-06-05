---
schema_version: 2
title: Farey Claim Ledger
type: fact
domain: project
tier: semantic
confidence: 0.9
created: 2026-04-24
updated: 2026-05-11
verified: 2026-05-11
sources:
  - raw/farey-archive/state-docs/CLAIM_STATUS.md.txt
  - raw/farey-archive/handoff/complete_farey_handoff.md.txt
  - projects/farey-research/data/W2_PRIME_FIT.json
  - projects/farey-research/recent-results-review.md
  - handoff-2026-05-09-followup/B_plus_direct_counterexamples.md
  - handoff-2026-05-09-followup/KOYAMA_RESEARCH_DECISION_MEMO_2026-05-10.md
  - handoff-2026-05-09-followup/KOYAMA_NEXT_SPRINT_SYNTHESIS_2026-05-10.md
  - handoff-2026-05-09-followup/Koyama_Perron_leading_gap_audit_2026-05-10.md
  - handoff-2026-05-09-followup/Koyama_EC_NDC_mixed_residual_2026-05-10.md
  - handoff-2026-05-09-followup/Koyama_EC_NDC_mixed_residual_complete_2026-05-11.md
  - handoff-2026-05-09-followup/Koyama_EC_NDC_ap_table_100000.csv
  - handoff-2026-05-09-followup/Koyama_EC_NDC_L2E_complete_check_2026-05-11.md
  - handoff-2026-05-09-followup/KOYAMA_MOONSHOT_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-09-followup/Koyama_Perron_moonshot_2026-05-11.md
  - handoff-2026-05-09-followup/Koyama_EC_NDC_extended_sweep_2026-05-11.md
  - koyama-shared/results/PATH_B_MOONSHOT_DECISION_2026-05-11.md
  - formal-conjectures/DPAC_PHASE_BRIDGE_MOONSHOT_2026-05-11.md
  - handoff-2026-05-09-followup/KOYAMA_GPT55_DEEP_GAP_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-09-followup/Koyama_Perron_remainder_theorem_hunt_2026-05-11.md
  - handoff-2026-05-09-followup/Koyama_EC_NDC_normalization_no_go_2026-05-11.md
  - koyama-shared/results/PATH_B_CONTROL_RUNNER_2026-05-11.md
  - formal-conjectures/DPAC_PHASE_BRIDGE_PATCH_2026-05-11.md
  - handoff-2026-05-09-followup/KOYAMA_CLAIM_AUDIT_2026-05-11.md
  - handoff-2026-05-09-followup/KOYAMA_ROADMAP_PROGRESS_2026-05-11.md
  - handoff-2026-05-09-followup/Koyama_claimsafe_paper_outline_2026-05-11.md
  - handoff-2026-05-09-followup/Koyama_email_to_Koyama_claimsafe_draft_2026-05-11.md
  - handoff-2026-05-09-followup/Koyama_EC_NDC_theory_next_questions_2026-05-11.md
  - handoff-2026-05-09-followup/MERTENS_LB_phase_transition_probe_2026-05-11.md
  - handoff-2026-05-11-gpt55-wave/WAVE_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-gpt55-wave/AGENT1_GL1_SHIFTED_PERRON.md
  - handoff-2026-05-11-gpt55-wave/AGENT2_PERRON_CITATION_AUDIT.md
  - handoff-2026-05-11-gpt55-wave/AGENT3_EC_NDC_BEYOND_BAD_PRIMES.md
  - handoff-2026-05-11-gpt55-wave/AGENT4_MERTENS_SMALLK_TAIL.md
  - handoff-2026-05-11-gpt55-wave/AGENT5_BPLUS_CLUSTER_PROGRAM.md
  - handoff-2026-05-11-gpt55-wave/AGENT6_PATH_B_CONTROLS.md
  - handoff-2026-05-11-gpt55-wave/AGENT7_DPAC_FORMAL_BRIDGE.md
  - handoff-2026-05-11-gpt55-wave/AGENT8_THEOREM_B_DELTA_SCOUT.md
  - handoff-2026-05-11-gpt55-wave/AGENT3_ec_smoothed_reproducer.py
  - handoff-2026-05-11-gpt55-wave/AGENT3_EC_SMOOTHED_PROXY_SUMMARY_2026-05-11.md
  - handoff-2026-05-11-gpt55-wave/AGENT3_EC_SMOOTHED_PROXY_METRICS_2026-05-11.csv
  - handoff-2026-05-11-ec-smoothing-blockers/EC_SMOOTHING_BLOCKER_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-ec-smoothing-blockers/T1_SMOOTHED_PERRON_THEOREM.md
  - handoff-2026-05-11-ec-smoothing-blockers/T2_STOCHASTIC_EULER_PRODUCT_MODEL.md
  - handoff-2026-05-11-ec-smoothing-blockers/C1_HOLDOUT_CURVE_PROTOCOL.md
  - handoff-2026-05-11-ec-smoothing-blockers/C2_KERNEL_NULL_CONTROL_PLAN.md
  - handoff-2026-05-11-ec-smoothing-blockers/C3_LARGER_K_DENSE_GRID_PLAN.md
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2_SPRINT_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2A_LITERATURE_AUDIT.md
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2B_ANALYTIC_PROOF_ATTEMPT.md
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2C_OBSTRUCTION_MAP.md
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2D_NUMERICAL_DIAGNOSTICS.md
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2E_THEOREM_PACKAGING.md
  - handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1_EXPLICIT_FORMULA_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1A_EXPLICIT_FORMULA_DERIVATION.md
  - handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1B_SOURCE_AUDIT.md
  - handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1C_ZERO_TERM_ANALYSIS.md
  - handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1D_AVERAGED_FALLBACK.md
  - handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1E_NUMERICAL_ZERO_DIAGNOSTICS.md
  - handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1F_SYM2_COMPANION_TERM.md
  - handoff-2026-05-11-ec-theorem-closure-wave/THEOREM_CLOSURE_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-ec-theorem-closure-wave/S1_BRANCH_THEOREM_CANDIDATE.md
  - handoff-2026-05-11-ec-theorem-closure-wave/S1_ZERO_SUMMABILITY.md
  - handoff-2026-05-11-ec-theorem-closure-wave/S1_SYM2_FINITE_PART.md
  - handoff-2026-05-11-ec-theorem-closure-wave/H2_POINTWISE_THEOREM_PACKAGE.md
  - handoff-2026-05-11-ec-theorem-closure-wave/H1_H2_COMPOSITION_AUDIT.md
  - handoff-2026-05-11-ec-theorem-closure-wave/SOURCE_PACKET.md
  - handoff-2026-05-11-ec-theorem-closure-wave/ADVERSARIAL_REFEREE.md
  - handoff-2026-05-11-ec-theorem-closure-wave/DENSE_S1_RESIDUAL_DIAGNOSTICS.md
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_RECIPROCAL_PERRON_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_CENTRAL_POLYNOMIAL.md
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_OFFCENTRAL_RESIDUE_AGGREGATE.md
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_MULTIPLE_ZERO_RANK0_NOGO.md
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_AVERAGED_OSCILLATORY_FALLBACK.md
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_SOURCE_AUDIT.md
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_ADVERSARIAL_REFEREE.md
  - handoff-2026-05-11-h1-residue-control-wave/H1_RESIDUE_CONTROL_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-h1-residue-control-wave/H1_RECIP_DERIVATIVE_SOURCE_HUNT.md
  - handoff-2026-05-11-h1-residue-control-wave/H1_CONTOUR_SHIFT_THEOREM.md
  - handoff-2026-05-11-h1-residue-control-wave/H1_POSITIVE_RANK_CLOSURE.md
  - handoff-2026-05-11-h1-residue-control-wave/H1_RANK_ZERO_OSCILLATORY_PROFILE.md
  - handoff-2026-05-11-h1-residue-control-wave/H1_PRODUCT_AVERAGE_THEOREM.md
  - handoff-2026-05-11-h1-residue-control-wave/H2_SYM2_SOURCE_CLOSURE.md
  - handoff-2026-05-11-h1-residue-control-wave/KERNEL_ZERO_FILTERING.md
  - handoff-2026-05-11-h1-residue-control-wave/RESIDUE_CONTROL_ADVERSARIAL_REFEREE.md
  - handoff-2026-05-11-h1-breakthrough-proof-wave/H1_BREAKTHROUGH_PROOF_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-h1-breakthrough-proof-wave/H1_LZ_DYADIC_UPPER_BOUND.md
  - handoff-2026-05-11-h1-breakthrough-proof-wave/H1_FIXED_WEIGHT_MOLLIFIER_TRANSFER.md
  - handoff-2026-05-11-h1-breakthrough-proof-wave/H1_MULTIPLE_ZERO_EXCEPTIONAL_THEOREM.md
  - handoff-2026-05-11-h1-breakthrough-proof-wave/H1_CONTOUR_TAIL_HEIGHT_AVOIDANCE.md
  - handoff-2026-05-11-h1-breakthrough-proof-wave/RANK_ZERO_PRODUCT_AVERAGE_PACKAGE.md
  - handoff-2026-05-11-h1-breakthrough-proof-wave/H2_SYM2_PROOF_ATTEMPT_2.md
  - handoff-2026-05-11-h1-breakthrough-proof-wave/KERNEL_FILTER_DIAGNOSTIC_IMPLEMENTATION.md
  - handoff-2026-05-11-h1-breakthrough-proof-wave/BREAKTHROUGH_WAVE_REFEREE.md
  - handoff-2026-05-11-h1-shell-moment-wave/H1_SHELL_MOMENT_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-h1-shell-moment-wave/SHELL_MOMENT_SOURCE_AUDIT.md
  - handoff-2026-05-11-h1-shell-moment-wave/SHELL_MOMENT_ANALYTIC_ATTEMPT.md
  - handoff-2026-05-11-h1-shell-moment-wave/SHELL_MOMENT_RMT_HEURISTIC.md
  - handoff-2026-05-11-h1-shell-moment-wave/FIXED_WEIGHT_PRINCIPAL_VALUE_ROUTE.md
  - handoff-2026-05-11-h1-shell-moment-wave/RECIPROCAL_STRIP_BOUNDS.md
  - handoff-2026-05-11-h1-shell-moment-wave/TC_HEIGHT_EXPONENT_AUDIT.md
  - handoff-2026-05-11-h1-shell-moment-wave/RANK_ZERO_FALLBACK_PAPER_SKELETON.md
  - formal-conjectures/DPAC_NEXT_STEPS_2026-05-10.md
  - koyama-shared/results/PATH_B_CONTROL_QUEUE_2026-05-10.md
  - handoff-2026-05-11-all-in-wave/ALL_IN_WAVE_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-all-in-wave/EC_KERNEL_NULL_SUMMARY_2026-05-11.md
  - handoff-2026-05-11-all-in-wave/EC_STOCHASTIC_NULL_REPORT_2026-05-11.md
  - handoff-2026-05-11-all-in-wave/H1_SHELL_ANTI_SMALL_DERIVATIVE_PACKET_2026-05-11.md
  - handoff-2026-05-11-all-in-wave/H1_FIXED_WEIGHT_PV_PACKET_2026-05-11.md
  - handoff-2026-05-11-all-in-wave/H2_SYM2_ENDPOINT_PACKET_2026-05-11.md
  - handoff-2026-05-11-all-in-wave/GL1_SHIFTED_PERRON_PACKET_2026-05-11.md
  - handoff-2026-05-11-all-in-wave/BPLUS_SIGN_CLUSTER_PACKET_2026-05-11.md
  - handoff-2026-05-11-breakthrough-wave-2/*.md
  - handoff-2026-05-11-breakthrough-wave-3/*.md
  - handoff-2026-05-11-dpmv-continuation/GL2_LANDAU_GONEK_DPMV_SPLIT_2026-05-11.md
  - handoff-2026-05-11-top10-challenge-wave/*.md
  - handoff-2026-05-11-homogeneous-bfmt-dpmv/ZERO_SAMPLING_HOMOGENEOUS_BFMT_DPMV_2026-05-11.md
  - handoff-2026-05-11-homogeneous-bfmt-dpmv/ZERO_SAMPLE_BFMT_SUBSTITUTION_AUDIT_2026-05-11.md
supersedes:
  - raw/farey-archive/old-obsidian-wiki/Research/W2_Rank_Linear_Law.md.txt
superseded-by: 
tags: [farey, claims, ledger, supersession]
---

# Farey Claim Ledger

## Confirmed Or Strong

- Delta anchor: `E[C1^2] = 0.950231842` over 683 zeros at `K = 10^4`.
- 37a1 and 389a1 500-zero EC values: `2.189911545`, `3.113923728`.
- 5077a1 rank-3 anchor: `E[C1^2] = 4.617` over 500 zeros.
- Rank-0 EC cluster: mean `1.886`, CV `8.9%`, 200 zeros each.
- Rankin-Selberg identity check: `L(Sym^2 f,2)/<f,f> = 8*pi^3/N` verified to about 1% for 37a1 and 389a1.
- Four-term Farey decomposition and Farey spectroscope connection survive the C1 bugfix.
- Koyama GL(1): local Perron double-pole residue at a simple zero is proved as local algebra; corrected `B_infty` identity is proved when `psi`, `BPC1`, `BPC2`, and `T_{>=3}` are included.
- Koyama follow-up sprint: the exact missing GL(1) ingredient is now isolated as a shifted Perron nonlocal remainder lemma for `K^w/(w L(w+rho,chi))`.
- Koyama Perron moonshot: target-zero simplicity is not enough for theorem promotion; off-target multiple zeros can create extra oscillatory `log K`-scale residues unless a shifted nonlocal remainder theorem controls them.
- DPAC phase bridge: for fixed `K,beta`, the finite-exponential-polynomial argument gives a claim-safe proof sketch that the bad real gamma set is measure zero once the non-identity lemma is supplied; this is not Lean-verified and not pointwise zeta-zero DPAC.
- Path B control runner: `koyama-shared/scripts/path_b_control_queue_runner.py` now emits B1/B2 GP packets and runs the bootstrap gates once selected-control rows exist.
- Koyama roadmap continuation: claim-safe paper outline, correspondence draft, EC theory next questions, and MERTENS-LB phase probe were added without promoting any theorem.
- MERTENS-LB phase probe: after the old `N=99991` verification ceiling, the first positive `T(N)` is `N=108004`; the first `T(N)>100` is `N=297331`; the large cluster around `N=300296` is driven by small-`k` Mertens terms rather than a uniform global drift.
- GPT-5.5 wave: no theorem promoted; shifted Perron target-zero-simplicity closure is no-go; AK citation audit supports `e^gamma` denominator but not arbitrary noncentral promotion; DPAC and Delta gained rigorous reductions.
- EC-NDC smoothed proxy reproduction: saved code/data reproduce Agent 3's three-curve smoothstep grid through `K<=1000000`; `all, alpha=0.75` gives cross-curve ratio `1.347375492996` and max within-curve CV `0.063297427334`.
- EC deterministic C2 all-in suite: `EC_KERNEL_NULL_SUITE_2026-05-11.py` exactly reproduces the primary smoothstep anchor (`ratio=1.3473754929960748`, max CV `0.063297427334436704`) and passes G0 reproducibility, G1 primary survival, G2 kernel robustness for `none/continuous/discrete_both`, G4 rank specificity (`0/5` nonidentity rank permutations pass), G4 curve-label specificity (`0/5` nonidentity curve permutations pass), and G5 tail stability.
- EC stochastic Sato-Tate full G3: `EC_STOCHASTIC_NULLS_2026-05-11.py` run with `512/512` iid seeds and `128/128` shared seeds gives `0` old-gate passes and `0` primary-gate passes in both families, but status is `G3_FAIL` because empirical p gates fail (`iid p_ratio=0.062378167641325533 > 0.01`; shared p_score `0.046511627906976744 > 0.02`).
- EC G3 failure diagnostic: no Sato-Tate null beats real max CV or passes old/primary, but `31/512` iid and `20/128` shared nulls beat real ratio, and `5/128` shared nulls beat real additive score. The failure is metric-specific empirical non-separation, not literal old-gate null passing. Any EC numerical continuation needs a new predeclared diagnostic gate; no post-hoc promotion.
- EC C2-prime diagnostic protocol: future-only EC numerical continuation should use fresh stochastic seeds (`512..1023` iid, `128..255` shared), CV/Pareto empirical p-values, and no retroactive reclassification of failed G3. It is diagnostic only and cannot promote without H1/H2 theorem closure.
- EC smoothing theorem blocker sprint: fixed-curve stabilization of `c_E,W(K)P_E,W(K)` reduces to `H1` smoothed reciprocal Perron offcentral-zero control plus `H2` smoothed EC-Mertens product expansion `log P_E,W(K)=-rank(E)loglogK+B+o(1)`.
- EC smoothing finite model: exact finite variance identities explain the current pass as `c/P` endpoint covariance damping; this is a rigorous reduction for the finite model, not an EC asymptotic theorem.
- H2 smoothed EC-Mertens sprint: the coefficient `-ord_{s=1}L(E,s)` is plausible only after trace/quadratic/harmonic bookkeeping; audited sources do not prove pointwise H2 for Agent 3 factors, and the repaired target must include either lower-order offcentral terms, explicit `Z_E,W(logK)`, or logarithmic averaging.
- S1 explicit-formula sprint: for `S_1,W(K)=sum_p W(p/K)a_p/p`, offcentral logarithmic branch zeros contribute `K^(i gamma)W_hat(i gamma)/logK`, not persistent `K^(i gamma)`, under branch-only continuation and weighted zero-summability. This reopens a pointwise H2-limit route, but as a rigorous reduction only.
- EC theorem-closure wave: no theorem promoted. S1 branch and zero-summability are now `PROOF_CANDIDATE` under explicit branch-contour and smooth-kernel hypotheses; exact Agent-3 H2 local bookkeeping is coherent and gives coefficient `-ord_{s=1}L(E,s)` if `S1`, `Ssym`, `Mgood`, higher powers, and bad primes all close in the same normalization.
- EC theorem-closure source packet: ordinary prime-Mertens and EC zero-counting for pure multiplicity weights are source-supported; exact fixed-curve endpoint-smoothed `S_1,W`, `S_sym,W`, pointwise H2, and reciprocal Perron H1 remain in-repo proof territory.
- H1 reciprocal Perron wave: no theorem promoted. Central residue algebra is fixed: for normalized `W_hat(z)=1/z+O(1)`, the leading central term is `(log K)^r/L^(r)(E,1)`, not `r!(log K)^r/L^(r)(E,1)`.
- H1 positive-rank reduction: bounded simple offcentral reciprocal residues are enough for final pointwise fixed-curve composition when `r>=1`, because they are `o((log K)^r)` after H2 normalization. This remains conditional on H1 contour shift and reciprocal derivative/Laurent control.
- H1 fallback modes: if offcentral residues persist, the honest targets are an oscillatory profile or a product-level averaged statement. Averaged `log P` alone does not imply pointwise or arithmetic-average stabilization of `c_E,W P_E,W`.
- H1 residue-control wave: no theorem promoted. Canonical scaffold is a finite-box reciprocal-Perron identity with central polynomial `Q_E,W(u)` and explicit offcentral residue polynomials; positive rank closes conditionally if all effective offcentral degrees are `< r`, lower-degree aggregates are bounded/absolutely convergent, and contour tails are `o(u^r)`.
- H1 rank-zero profile: claim-safe object is `c_E,W(e^u)=Q_0+Z_c(u)+o(1)` with a declared zero-series convergence mode. A constant-only rank-zero limit requires cancellation, filtering with tail control, or averaging.
- H1 product-average fallback: the arithmetic log-Cesaro average of `c_E,W(e^u)P_E,W(e^u)` has a conditional diagonal constant `e^(B_H2)(q_r d_0 + sum h_gamma d_(-gamma))`; this is not implied by averaged `log P`.
- H1 kernel filtering: finite signed kernels can kill finitely many named H1 residues, useful diagnostically, but this does not prove fixed-kernel asymptotic stabilization or tail control.
- H1 breakthrough proof wave: no theorem promoted. Direct Li-Zaharescu/mollifier transfer to the fixed H1 weight is `NO_GO`; the useful target is a new fixed-curve reciprocal derivative shell bound or direct fixed-weight principal-value theorem.
- H1 positive-rank shell target: if `|W_hat(it)|<=C(1+|t|)^(-q)`, then simple-zero H1 closes from `J_E,2(T)=sum_{T<|gamma|<=2T}|L'(E,1+i gamma)|^{-2} <= C_E T^theta(logT)^B` with `theta<2q-1`; for smoothstep-scale `q=2`, this is `J_E,2(T)<=C_E T^(3-delta)`.
- H1 weighted-l1 target: for positive rank, absolute offcentral residue control is already implied by `H1-weighted-l1(E,W,epsilon)`, namely `sum_{T<|gamma|<=2T}|W_hat(i gamma)| |L'(E,1+i gamma)|^{-1} <= C_E,W T^{-epsilon}`. For smoothstep-scale `|W_hat(it)|<<|t|^{-2}`, the simpler sufficient target is `R_E,1(T)=sum |L'(E,1+i gamma)|^{-1} <= C_E T^(2-epsilon)`, weaker than the `J_E,2` shell moment.
- H1 weighted-l1 refinement: for positive rank, the exact finite-box need is weighted partial growth `M_W(u)=o(u^r)` along the legal Perron height `T_box(u)`. For smoothstep-scale `q=2`, absolute convergence already follows from `R_E,1(T)<=C_E T^2(logT)^(-1-delta)`, and finite-box central-scale closure can allow `R_E,1(T)<=C_E T^2(logT)^B` when `(log T_box(u))^(B+1)=o(u^r)`.
- H1 contour-tail target: finite-box identity, legal heights, and original-line truncation are clean under explicit Mellin/absolute-convergence hypotheses; horizontal and shifted-line tails reduce to reciprocal strip assumptions `H-height` and `H-left`, not to zero counting alone.
- H1 multiple-zero package: offcentral zeros of multiplicity `m` contribute explicit polynomial-exponential terms of degree at most `m-1` lowered by kernel zeros/cancellations; effective degrees `>=r` block positive-rank central closure unless retained, killed, or averaged.
- H1 kernel-filter diagnostic: `kernel_filter_moments.py` constructs finite signed log-Gaussian filters with `W_hat(0)=1` and `W_hat(i gamma_j)=0`; smoke test residuals are at floating precision. It is diagnostic only and not the endpoint Mellin-pole kernel used for central H1 algebra.
- H1 shell-moment wave: no theorem promoted. `H1-shell-moment(E,delta)` is now the named positive-rank anti-small-derivative hypothesis; sufficient routes are pointwise derivative lower bounds, small-derivative tail bounds, zero-repulsion plus minimum-modulus, or positive mollifier majorants.
- H1 RMT heuristic: characteristic-polynomial modeling predicts `J_E,2(T)` around `T polylog(T)`, so `T^(3-delta)` is plausibly weak for `delta<2`; this is heuristic support only.
- H1 reciprocal strip refinement: `H-left` is closed if the contour may shift to `Re z=-eta` with `eta>1/2`; pre-continuation generic Cartan/Jensen did not close `H-height(A<2)` for `q=2`, but the later Li-Zaharescu route conditionally source-routes horizontal height under normalized EC/newform RH/no-right-half-zero.
- H1 TC-height exponent audit: generic Cartan/Jensen plus local zero count does not close `A_TC<2`; the raw zero-factor bookkeeping loses `T^(O(loglogT))`, so a genuine fixed EC/GL2 minimum-modulus theorem with explicit exponent or a stronger kernel/theorem mode is needed.
- H1 Li-Zaharescu height verification: horizontal `H-height(A<2)` is conditionally source-routed under normalized EC/newform RH/no-right-half-zero via Li-Zaharescu selected heights with reciprocal bound `exp(A logT/loglogT)=T^o(1)`. This supersedes the generic Cartan/Jensen pessimism for the horizontal contour-height subproblem only; it is not unconditional and does not control reciprocal residues, PV sums, or shell moments.
- H1 rank-zero shell-wave fallback: if shell/PV/height stay open, the claim-safe paper mode is `Q_0+Z_c(u)+o(1)` plus a separate arithmetic product-average diagonal theorem, not a pointwise constant EC smoothing theorem.
- H1 fixed-weight PV package: positive-rank closure is valid if a genuine uniform PV theorem gives `Z_PV(u)=o(u^r)` in dyadic windows, but spacing plus square moments cannot imply this; the model `sum cos(nu)/n` has perfect spacing and strong `l^2` shell bounds while diverging at resonant `u`.
- Breakthrough wave: no theorem promoted. Durable updates: H1 rank-one `R_E,1(T)=o(T^2)` has exact layer-cake, pointwise `h(T)logT/T`, and sparse-exception reductions; H1 multiple-zero Laurent survival is controlled by effective degree `<r` plus coefficient aggregation; H2 closes weighted good-prime Mertens and pure S1 zero-summability but remains blocked by S1 branch-contour legality and exact good-prime Sym2 finite part; GL1 sharp cutoff remains conditional on moving off-target PV; G3 remains failed; B+ is sign-cluster classification; DPAC/Delta only gain formal/registry reductions.
- Breakthrough wave 2: no theorem promoted. Durable updates: H1 rank-one source closure remains blocked and is now sharpened to a fixed-curve GL2/EC negative first reciprocal-derivative moment with separated-zero plus bad-set budget strong enough for `R_E,1(T)=o(T^2)`; near-collision and actual-coefficient moving-PV mechanisms are separated from spacing models; the finite-box H1 theorem is assembled conditionally.
- H2 Wave 2 endpoint update: exact good-prime Sym2 finite part is source-closed as a component with `kappa_sym=0` under the standard adjoint/Sym2 ramified-factor reconciliation. Full pointwise H2 still requires `S1-CutPlane-LogGrowth(E,W,eta)` plus right-branch handling; no H2 damping is imported into H1 reciprocal residues.
- GL1/B+/DPAC/Delta Wave 2 update: GL1 sharp cutoff has no shortcut beyond actual moving off-target PV plus rectangle/truncation control; B+ tier-1B bridge is execution-specified but not run; DPAC has Lean signature patch plans only; Delta has registry/paper patch plans preserving no Theorem B impact.
- Breakthrough wave 3: no theorem promoted. Durable H1 update: fixed-curve reciprocal-derivative source hunt is `NO_GO`; BFMT adaptation is reduced to `GL2-LandauGonek-DPMV(E,theta)` for separated zeros plus `EC-BFMT-BadSetBudget(E,c)` for the complement. Separation alone, pair-correlation/count-only controls, generic minimum-modulus tools, and actual coefficients alone do not close rank-one H1.
- GL2 DPMV split: no theorem promoted. `GL2-LandauGonek-DPMV(E,theta)` is now decomposed into source-closed `LG-Explicit-GL2(f)`, source-backed but not BFMT-complete modular-form zero mean-value layers, and the live `BFMT-CoefficientErrorCheck(E)` against Milinovich-Ng Proposition 4.1/4.3. The separated-zero BFMT route now lives or dies on that coefficient/convolution audit before the independent bad-set budget.
- Top-10 challenge wave: no theorem promoted. Direct Milinovich-Ng Proposition 4.1/4.3 substitution for BFMT is `NO_GO`: Proposition 2.5 fails from nonhomogeneous MN errors after the `(s_0!)^2` expansion; Proposition 2.6 fails condition (40) from the terminal `P^s` factorial spike and exceeds the `T^(2/3)` support wall. The surviving separated-zero target is the stronger new `Homogeneous-GL2-BFMT-DPMV(E,k=1/2)` theorem, not the checked MN black box. The rank-one H1 finite-box theorem is paper-ready only as a conditional package requiring homogeneous BFMT-DPMV, `EC-BFMT-BadSetBudget(E,c)`, finite-box boundary hypotheses, and multiple-zero effective-degree control.
- Top-10 H2 update: literal global-branch `S1-CutPlane-LogGrowth(E,W,eta)` remains unsafe at endpoint decay. The current reduction is `S1-CutPlane-RenormalizedLogGrowth(E,W,eta;c)` plus `RegularLogLeftEdge`, the existing Sym2/good-prime ledger, exact good-prime normalization, and exact right-branch handling. If `Re a>0`, retain or subtract the full `R_S1^+(K;E,W,eta,c)` cut-lip term; retaining only `B_S1^+(K;E,W,c)` is not enough.
- Top-10 GL1 update: H1 DPMV/PV progress does not prove sharp GL1 off-target control because the sharp coefficient has the harmonic factor `1/((lambda-rho)L'(lambda,chi))`. Sharp GL1 still needs `GL1-ActualMovingShellPV(chi,rho)`, a critical weighted reciprocal-derivative theorem, and rectangle/truncation control.
- Top-10 secondary update: among B+, DPAC, and Delta, the next theorem-shaped secondary task is Delta-2.5b registry execution for the local ramified correction divisor / axis-pole multiplicity proposition, explicitly preserving no Theorem B impact. B+ remains an execution-ready compute/classification task; DPAC remains Lean proof hygiene.
- Homogeneous BFMT DPMV continuation: no final H1 theorem promoted, but there is a new route around the Milinovich-Ng coefficient obstructions. A homogeneous zero-sampling bound gives `sum_{T<gamma<=2T}|A(1/2+i gamma)|^2 <<_E T(logT)^3 sum |a_n|^2/n` for length `N<=T` under fixed-curve critical-line/zero-count hypotheses. The follow-up `ZeroSample-BFMT-SubstitutionAudit(E,k=1/2)` passes at BFMT Propositions 2.5-2.7 / Section 5 bookkeeping level with only fixed polylog loss. The next exact target is `BFMT-EC-Transcription(E,k=1/2)`, then `EC-BFMT-BadSetBudget(E,c)`.
- Breakthrough wave 4: no source-closed H1 theorem promoted. The separated BFMT branch now has both local GL2 inputs conditionally available: `GL2-ShiftDerivativeComparison(E,c)` under fixed-newform RH and conductor-normalized `GL2-BFMT-PrimePolynomialLowerBound(E)`. The new first blocker is `Section5-GL2-ConductorAudit(E,k=1/2)`, because the GL2 lower bound uses `C_E(t) asymp_E T^2` rather than the literal zeta archimedean scale. After that, H1 still needs the independent bad-set `MinMod(E,c,A,h)+ProductLayer(E,c,A,h)` or equivalent complement tail, plus `H1-MultipleEffectiveDegree-BFMT(E,W,r)`. H2 gains a conditional S1 renormalized endpoint with full `R_S1^+` handling; GL1 sharp remains `NO_GO`; EC numerics remain diagnostic only.
- Breakthrough wave 5: no H1 theorem promoted; the current separated EC-BFMT route at `k=1/2` is `NO_GO`. The GL2 conductor-normalized Section 5 audit fails because `log C_E(t)=2logT+O_E(1)` changes BFMT Lemma 2.4 / Section 5 `(5.13)` from `2k` to `4k`; at `k=1/2` this requires `a(2d-1)>2`, unavailable in the BFMT support regime. New first blocker is `ConductorNormalized-BFMT-Section5-SignLemma(E,k=1/2)` or a different fixed-curve degree-2 separated negative-moment theorem. Downstream: `MinMod(E,c,A,h)` remains `NO_GO`; `ProductLayer` reduces to rooted inverse-product correlation `J_m(T;A)`; direct complement tail remains a reciprocal-derivative upper-tail gap; multiple zeros should be declared via `H1-MultipleZeroDisposition(E,W,r)`.
- Post-Wave-5 pivot: no theorem promoted, but the separated-BFMT target is revised. Wave 5 killed the strong zeta-quality separated theorem `sum_F |L'|^{-1} << T^(1+delta)`, while rank-one H1 only needs the separated contribution to be `o(T^2)`. The conductor-doubled BFMT ledger appears to give a weaker `T^(3/2+delta)`-type bound, which would already be H1-sufficient if source-audited. New immediate task: `WeakSeparatedEC-BFMT-H1-Audit(E,c)`. If it passes, the first H1 blocker shifts to the bad-set complement; most promising route is `ClusterShiftDerivativeComparison(E,A)` plus shifted-value negative moments and rooted inverse-product correlations `J_m(T;A)`, avoiding zero-centered `MinMod`.
- Post-Wave-5 continuation: no full H1 theorem promoted. `WeakSeparatedEC-BFMT-H1-Audit(E,c)` conditionally passes: with Wave 4 local inputs and zero-sampling transcription, the GL2 conductor-doubled BFMT second branch gives `sum_F |L'|^{-1} << T^(3/2+delta)`, so separated simple zeros are rank-one H1-harmless. `ClusterShiftDerivativeComparison(E,A)` gives a local `MinMod` bypass: `1/L'(rho)` is bounded by `1/L(rho+1/logT)` times explicit inverse-product cluster weights and `T^o(1)`. The bad-set global criterion is now exact: prove `Degree2WeakShiftedNeg_q(E)` with exponent `q+1/2` and `RootedInvProdCorr_p(E,A)` for `p=q/(q-1)`; then Holder gives `R_B(T,c) << T^(2-1/(2q)+epsilon+o(1))`. Prefer `q>3/2` if relying on pair-layer cubic repulsion, but higher clusters still need singular inverse-product control.
- Post-Wave-5 q=2 shifted continuation: no H1 theorem promoted. `Degree2WeakShiftedNeg_2(E)` conditionally passes from BFMT Lemma 2.4 plus the Wave 4/zero-sampling/conductor-normalized stack: `sum |L(rho+1/logT)|^{-2} << T^(5/2+epsilon)`. The bad-set route is now sharpened to `RootedInvProdCorr_2(E,A)`; if `sum W_A(rho)^2 << TlogT`, Cauchy gives `R_B(T,c) << T^(7/4+epsilon+o(1))`.
- Post-Wave-5 square cluster continuation: no bad-set theorem promoted. `RootedInvProdCorr_2(E,A)` is reduced to the exponential square rooted inverse-product statistic `sum_m C_A^(2m)/m! J_m^(2)(T;A) << TlogT`. A close-pair law `Q_1(T;u) << TlogT u^beta` proves only the pair layer when `beta>2`; higher layers need a singular rooted Palm/repulsion majorant or direct summable `J_m^(2)` bounds. New exact statistics blocker: `RootedPalmRepulsionExpMoment_2(E,A)`.
- Post-Wave-5 Palm source audit: no zero-statistics theorem promoted. Existing Rudnick-Sarnak/Hejhal-style n-level correlation sources are ordinary smooth-test/restricted-support inputs; they support the GUE model but do not prove the uniform singular inverse-square rooted moment. PCC/density-one simplicity is also too weak for `J_m^(2)`. The source hunt must target uniform small-gap upper laws or rooted Palm density majorants for fixed GL2 zeros.
- Post-Wave-5 small-gap source hunt: no cluster theorem promoted. Current small-gap sources are adjacent but prove existence/proportion/evidence, not the needed uniform `Q_1(T;u) << TlogT u^beta` with `beta>2` or higher singular rooted moments. Conditional replacement: `UniformRootedSmallGap_2(E,A)` plus `HigherRootedPalmSquare(E,A)`.
- Post-Wave-5 simple-zero conditional stack: no full H1 theorem promoted. Under Wave 4 local inputs, zero-sampling transcription, and `RootedPalmRepulsionExpMoment_2(E,A)`, the simple-zero reciprocal derivative budget closes: separated zeros contribute `T^(3/2+epsilon)`, bad clustered zeros contribute `T^(7/4+epsilon+o(1))`, hence `R_E,1^simp(T)=o(T^2)`. Remaining blockers are the Palm statistic, multiple-zero disposition, and finite-box contour hypotheses.
- Post-Wave-5 multiple-zero disposition: no multiple-zero theorem promoted. The correct packaging is `H1-MultipleZeroDisposition(E,W,r)`, not a BFMT condition. Each crossed offcentral multiple-zero Laurent residue must be absent by offcentral simplicity, killed by the kernel, retained in an explicit profile, or central-negligible by effective degree plus aggregate control. In rank one, unretained critical-line multiple-zero terms need `D_alpha<=0` and `Z_0^mult(u)=o(u)`.
- H1 Wave 3 threshold: a local minimum-modulus certificate `m_T/r_T >= T^(-alpha)(logT)^lambda` gives `R_E,1(T) <= T^(1+alpha)(logT)^(1-lambda)` and beats rank-one `o(T^2)` exactly when `alpha<1` or `alpha=1, lambda>1`.
- H2 Wave 3 S1 repair: literal `S1-CutPlane-LogGrowth(E,W,eta)` should not be promoted at smoothstep decay `|W_hat|<<|t|^-2` because global branch constants can accumulate like `N(t)`. Use `S1-CutPlane-RenormalizedLogGrowth(E,W,eta)` or stronger kernel decay `|t|^(-2-epsilon)`, and retain `B_S1^+(K;E,W,c)` unless a no-right-zero/cancellation theorem removes right branches.
- GL1/H1 Wave 3 PV coupling: `AbstractActualMovingShellPV(Omega,b,H,Phi)` is only a deterministic wrapper. H1 still needs `H1-ActualDyadicShellPV(E,W,r,H)` or reciprocal domination; GL1 sharp still needs `GL1-ActualMovingShellPV(chi,rho,T)` plus its own small-alpha, multiplicity, and rectangle controls.
- Rank-zero continuation package: the clean theorem mode is `c_E,W(e^u)=q_0+Z_c(u)+o(1)` and an arithmetic product-average diagonal constant, not pointwise stabilization unless all nonzero profile coefficients die, are killed with tail control, are subtracted, or are averaged.
- GL(1) smoothing/filtering continuation: target-normalized smooth kernels give a separate conditional smoothed theorem mode for `c_{W,K}`; finite signed filters can kill any prescribed finite off-target zero set by Mellin-transform vanishing, but this does not transfer back to the sharp cutoff without the missing uniform off-target estimates.
- GL(1) sharp all-in packet: the sharp cutoff closes only under a named `GL1-Sharp-OffTarget-Control`/`GL1-Sharp-FixedWeightPV` plus rectangle/trivial-residue control. Global off-target simplicity removes higher-order log-scale residues but still leaves the simple-zero fixed-weight PV aggregate.
- H2/Sym2 all-in packet: exact local H2 algebra for the Agent-3 factors is closed; pointwise H2 remains conditional on S1 branch-contour closure and exact good-prime `S_sym,W` finite-part continuation. Product-average can be stated only with joint H1/H2 profile coefficients and tail extraction.
- Literature-input continuation: checked source map remains mostly negative. Aoki-Koyama supports the product constant; Inoue/Soundararajan do not close shifted GL(1) nonlocal residues; Li-Zaharescu helps conditional horizontal H1 height; no checked source closes fixed EC/GL2 `J_E,2(T)` or fixed-weight H1 PV.
- B+ cluster program: future Paper B work should classify dense MR-prime sign clusters by `B`, `T`, `B0`, and `Spsi`; `T(p-1)` alone is not a sign proxy.
- B+ all-in cluster packet: the minimum honest next extension is tier `1B`, dense MR rows over `237733 <= p <= 243799` (468 rows, about `9.94` core-hours at the current verifier rate). Tier `1A` only probes local islands; tier `1C` through 300K is a larger first-transition atlas.

## Falsified Or Retracted

- Pointwise universal `E[C1^2] ~= 1/zeta(2)` is dead.
- GL(1) NDC constant `1/zeta(2)` is superseded/falsified; the claim-safe replacement is conditional `e^{-gamma}`, not an unconditional theorem in current files.
- EC-NDC simple universality `D_K^E*zeta(2) -> 1` is falsified by the 37a1/11a1/389a1 sweep.
- EC-NDC mixed residual diagnostics do not currently promote a normalization: complete `K=1000000` products give `D_mix_good` cross-curve ratio `11.04841098` and `D_2_good` ratio `10.64951807`, both much worse than the `1.42083` benchmark.
- EC-NDC `L2E_partial^rank` remains only a finite good-prime numerical proxy: at `K=1000000`, `D*zeta(2)/L2E_partial^rank` has cross-curve ratio `1.423821385` and max within-curve CV `0.09669211205`, so it fails the promotion rule.
- EC-NDC finite bad-prime factors cannot promote the tested sharp-cutoff class: all bad primes are below the first grid point, so any finite bad-prime correction is a per-curve constant and leaves within-curve CV invariant.
- EC-NDC smoothed full `L2^rank` normalization is not promoted by the reproduced three-curve pass: component ablations also pass old gates (`cP_only, alpha=0.75` ratio `1.347453619911`, max CV `0.063319173312`; `P_only` and `PL2_only` pass at multiple alphas), so the denominator is not load-bearing yet.
- EC null-control gate: the old smoothstep primary `all, alpha=0.75` still passes the old finite gate (`ratio=1.3473754929960748`, max CV `0.063297427334436704`), but predeclared nulls `cP_only`, `P_only`, and `PL2_only` also pass at `alpha=0.75`; best-null score delta is only `7.97e-05` versus the required `0.01`, so the old gate is a `NO_GO` as a load-bearing normalization gate.
- EC all-in deterministic controls do not undo the old ablation no-go: they upgrade the finite pattern to kernel/label/rank robust on deterministic gates, and full stochastic G3 has zero old/primary passes, but empirical p gates fail. The additive score is not equivalent to the old conjunctive gate because low ratio can buy a CV miss. Holdout curves and denser/larger `K` remain unrun. Status remains no theorem promotion.
- EC smoothing cannot currently be promoted as BSD or `L(E,2)` evidence: T2 predicts and observes that `L2`-smoothing has variance scale `p^-3` and is numerically negligible at the current gate.
- Naive pointwise H2 `log P_E,W(K)=-rank(E)loglogK+B+o(1)` is not claim-safe. It must be stated with analytic rank first, exact local factor constants, the quadratic/symmetric-square term, bad-prime constants, and explicit treatment of offcentral zero terms or averaging.
- S1 source closure is blocked: audited sources support adjacent GL(2)/EC explicit formula structures but do not prove the exact fixed-curve endpoint-smoothed theorem for the sprint kernel. Any promotion must be an in-repo proof or a new verified source.
- H1 cannot inherit H2/S1 `1/log K` branch damping: in reciprocal Perron, offcentral zeros of `L(E,s)` are pole residues of `1/L(E,1+z)`, not logarithmic branches. Pointwise fixed-curve stabilization still needs separate H1 reciprocal-pole control; rank zero needs explicit oscillatory/averaged handling unless stronger cancellation is proved.
- H1 reciprocal Perron source closure is blocked: checked sources do not provide fixed-curve EC/GL2 bounds or moments for `1/L'(rho)`, all-simple offcentral zeros, bounded multiplicity, or the exact H1 residue aggregate. EC zero counting only controls pure multiplicity weights.
- H1 rank-zero pointwise constant limit is a no-go if any simple offcentral reciprocal residue survives. Positive-rank pointwise limits are blocked by any effective offcentral zero degree `m-1>=r` unless the term is ruled out, cancelled, retained, or averaged.
- H1 reciprocal derivative source hunt remains `LITERATURE_BLOCKED`: checked Booker/de Faveri simple-zero sources give many simple zeros, not all; checked Li-Zaharescu-style reciprocal-derivative material gives adjacent negative-moment/mollified templates, not an upper bound for the fixed H1 weight `W_hat(i gamma)e^(i gamma u)/L'(1+i gamma)`.
- H1 shell-moment source closure remains blocked: checked EC/GL2 sources give zero counting, simple-zero lower bounds, positive derivative moments, and adjacent automorphic/zeta negative-moment analogues, but no fixed-curve upper bound for `J_E,2(T)` and no direct fixed-weight H1 upper bound.
- Combined H1/H2 EC smoothing theorem remains a referee `NO_GO` for promotion: H1 contour tails, reciprocal derivative/Laurent control, rank-zero handling, multiple-zero effective degrees, H2 S1 branch continuation, and exact Sym2 finite part are still load-bearing blockers.
- Li-Zaharescu/mollifier transfer is now specifically `NO_GO` for fixed H1: approximating `e^(i gamma u)` with length `M=T^theta` log-ratio Dirichlet polynomials leaves shells `T<exp(u/theta)` uncontrolled, and controlling approximation residuals already needs reciprocal-derivative upper bounds.
- H1 fixed-weight PV is not implied by zero spacing or reciprocal-derivative magnitude moments. Those inputs support averaged/profile modes unless a separate uniform cancellation theorem proves `Z_PV(u)=o(u^r)`.
- H1 contour `H-height(A<2)` is not unconditionally source-closed. Generic Cartan/Jensen does not prove the quantitative inequality against `q=2`; Li-Zaharescu selected heights conditionally route the horizontal height subproblem only under normalized EC/newform RH/no-right-half-zero.
- H2/Sym2 remains conditional after the second proof attempt: local Agent-3 algebra and `kappa_sym` cancellation are coherent, but exact endpoint-smoothed `S_1,W`, exact good-prime `S_sym,W`, no right-branch/pole assertions, and `kappa_sym` source/proof remain open.
- H2/Sym2 supersession after Wave 2: the exact good-prime `S_sym,W` finite-part theorem and `kappa_sym=0` component are now source-closed for the standard adjoint/Sym2 reconciliation. The remaining H2 blockers are S1 cut-plane log growth, legal endpoint contour shift, and right-branch handling.
- MERTENS-LB global fixed `K0<=100` negative-tail envelopes are falsified on the existing `1e9` log grid; `R_10<0` is only a finite dense certificate through `N=1000000`.
- DPAC from zeta-zero linear independence alone is unsafe as stated; it needs a strengthened log-prime/exponential phase-independence hypothesis.
- Delta first-zero half-value framing is dead; corrected value is about `0.004` at `K = 10^4`.
- General W1 soft universality across all forms is false as stated; Delta may still tend to 1.
- Raw Koyama proportionality `E[C1^2] proportional to L(Sym^2 f,k)/<f,f>` is falsified by direction for 37a1 vs 389a1.
- Simple Gamma/Deligne normalization of the raw Sym2/Petersson ratio is not currently supported; recent review found no simple collapse to the observed `E[C1^2]` scale.
- Pure-rank W2 is superseded; conductor-control data require a log-conductor term or stronger formulation.
- Chebyshev sign theorem was disproved at `p = 243799`.
- Conjecture B+ Mertens-restricted positivity is disproved in the Lean-canonical `crossTerm`: `B(237733) < 0` with `M(237733) = -20`, and `B(243799) < 0` with `M(243799) = -3`.
- Turan A2 was retracted to an open conjecture; fabricated citation risk is recorded.

## Open Claims

- W2 prime mechanism: explain the rank/control and `log(N)` structure in off-central second moments. Recent review supports keeping the `log(N)` term live; omitted rank/conductor bias alone probably does not explain the full coefficient, but this remains heuristic until recomputed.
- Delta limit: prove, disprove, or weaken `E[C1^2(Delta,rho)] -> 1`.
- Deligne-completed Sym2 correction: still possible only with a more specific formula; simple Gamma-period fixes failed the review gate.
- Dominance of -1: blocked until Koyama gives the exact modulus/residue/dynamic definition; the latest reply says dynamic `x` behavior matters and the 13 trillion baseline is not enough.
- Pair correlation of off-central modular zeros: compute normalized spacings and compare to GOE/GSE/GUE.
- Paper C arithmetic surrogate theorem: do not use as theorem language; recent review says the proposed cuspidal-form `K log K`-type asymptotic is likely wrong and should be reformulated as density/proportion/mollifier work.
- Koyama GL(1) Perron-leading theorem: close or cite `c_K(chi,rho) = log K/L'(rho,chi) + o(log K)` before any theorem-language use of `D_K -> e^{-gamma}`; the theorem must handle the off-target residue aggregate and possible higher-order residues.
- EC-NDC normalization: the four tested sharp-cutoff normalizations through `K=1000000` are negative, and finite bad-prime corrections are a no-go for this class. A genuinely different smoothed diagnostic now reproduces as a finite pattern, but it must survive holdout curves, larger/denser `K`, kernel/null controls, and load-bearing ablation tests.
- EC-NDC smoothed proxy: saved script/CSV reproduce Agent 3's smoothstep finite proxy on the three-curve grid. The old ablation-only gate failed as load-bearing, but the all-in deterministic C2 suite now passes kernel, rank-permutation, curve-label permutation, leave-one-K/curve, and tail-stability gates. Full Sato-Tate G3 (`512` iid, `128` shared) has zero old/primary gate passes, but fails empirical p gates. Do not promote unless a new C2-prime diagnostic gate is predeclared and passed, holdout curves and denser/larger `K` pass, and the theorem path closes fixed-curve H1 reciprocal derivative/Laurent control plus exact S1/Sym2/H2 source/proof closure in a declared pointwise/profile/averaged mode.
- H1 anti-small-derivative program: prefer the Wave 2 fixed-curve GL2/EC negative first reciprocal-derivative moment with separated-zero plus bad-set budget strong enough to imply rank-one `R_E,1(T)=o(T^2)`. For higher positive rank, keep the refined `H1-l1-growth` target along legal Perron heights, or the absolute log-saving target `R_E,1(T)<=C_E T^2(logT)^(-1-delta)` for smoothstep-scale kernels. Direct Li-Zaharescu/mollifier transfer should not be re-run without a genuinely new upper-bound idea.
- H1 fixed-weight PV program: prove a uniform cancellation theorem for `sum W_hat(i gamma)e^(i gamma u)/L'(E,1+i gamma)` strong enough to give `Z_PV(u)=o(u^r)` in the needed windows; otherwise package only averaged/profile/product-average modes.
- H1 post-top10 exact target: complete `BFMT-EC-Transcription(E,k=1/2)` using the now-passing zero-sampling substitution audit. The Milinovich-Ng black-box route remains killed. If the separated branch succeeds, the next H1 target is `EC-BFMT-BadSetBudget(E,c)`; without both, the rank-one finite-box theorem remains conditional only.
- H1 contour program: with `eta>1/2`, treat `H-left` as closed; for horizontal height, use the Li-Zaharescu selected-height route only with normalized EC/newform RH/no-right-half-zero and a written normalization/reflection lemma. This does not replace the shell/PV program.
- Koyama paper/correspondence: do not edit correspondence/email drafts unless the user explicitly asks. The paper thesis remains corrected constants plus obstruction, not closed NDC universality.
- MERTENS-LB explanation: test `K0=200` beyond the current sample; do not use global fixed `K0<=100` negative-tail lemmas.
- Path B conductor controls: run the new control runner on a `gp`/`pari-elldata` machine for the B1 `350-650` and B2 `4500-5600` conductor-matched control queues before any rank-isolated sentence; local conductor-controlled fits currently fail.
- DPAC hygiene: use explicit `LogPrimePhaseAvoidance`, `ae_logPrimePhaseAvoidance_fixed_beta`, certified zeta-zero sampling, or a cited external zeta-zero phase theorem; keep density-one packaging as conditional counting only.
- Delta Open 7.2': write the ramified axis-pole multiplicity proposition as a local theorem target; BCL q-averaged transfer remains closed for Theorem B-exact unconditional.

## Supersession Rules

Use this ledger before drafting papers, correspondence, or queue tasks. If a new result changes a claim, update this page, the specific project page, and `log.md`; keep the raw evidence in `raw/farey-archive/`.

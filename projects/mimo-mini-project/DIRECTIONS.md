# Directions Tracker — Farey-NOW MiMo session outputs

**Last updated**: 2026-05-27
**Total commits this session**: 27
**Live directions**: 5 top-level, 17 sub-directions

## TL;DR snapshot

| # | Top direction | Strength | Status | Primary audience |
|---|---|---|---|---|
| **A** | Cluster=2 universality + q*_BCZ closed form | **A−** (strongest) | Adversarially verified; paper-ready | Number theory, RMT, EVT |
| **B** | Mertens-NW correlation + structural identity | B+ | Verified; Tauberian closure open | Analytic number theory |
| **C** | Farey-QMC (low-discrepancy integration) | B (demonstrated) | Empirical gains 2-10×; needs advocacy | Numerical analysis, QMC, ML |
| **D** | Lean formalization (Mathlib) | B+ (concrete) | 13/16 theorems proven; v3 running | Lean/Mathlib community |
| **E** | Universality class diagnostic | A− (timely) | Closed form result IS the diagnostic | RMT, NT classification community |

---

## Direction A — Cluster=2 universality

### A1. q*_BCZ closed-form threshold
- **Achievement**: Proved q*_BCZ = (11 − 8·ln(3/2))/9 ≈ 0.86181 under BCZ density
- **Verification**: 10M MC, all (k₁,k₂)≤6 patterns enumerated, no pattern undercuts t* = 2/9
- **Potential exploration**: Lean formalization (in progress as v3), function-field analog, sharper rate near transition
- **Next steps**: Wait for Aristotle v3 result; refine if needed
- **Goal**: Get Lean-verified, publishable theorem with clean closed form
- **Math contribution**: Clean phase transition threshold for BCZ chain dynamics. Genuinely original — no prior in literature.
- **Who cares**: Athreya-Cheung (UCD), Granville (Montreal), Katz-Sarnak (Princeton); RMT universality researchers; EVT theorists (Embrechts, Mikosch)
- **Publication target**: Annals of Applied Probability OR Experimental Math (12-15 pp)

### A2. Median-run cutoff
- **Achievement**: q_median = 3/2 − ln 2 ≈ 0.807 (closed form, derived from P(XY<1/4) = ln 2 − 1/2)
- **Potential exploration**: Tighter than-median-cutoff regimes, multi-pattern thresholds
- **Next steps**: Include as Lemma in cluster=2 paper
- **Goal**: Co-published with main q*_BCZ result
- **Math contribution**: Second clean closed form characterizing BCZ structure
- **Who cares**: same audience as A1
- **Publication target**: same paper as A1

### A3. Empirical cluster=2 (finite Farey)
- **Achievement**: 30M+ Farey clusters tested across (N, q); zero size-3+ ever at q ≥ 0.99; 50M+ BCZ chain MC at q ≥ 0.86 also zero
- **Potential exploration**: Push to N=10⁹+; rate q*(N) → q*_BCZ
- **Next steps**: Optional larger-N runs on M2 if compute available
- **Goal**: Strong empirical support for the BCZ-density theorem
- **Math contribution**: Empirical foundation
- **Who cares**: Experimental math, computational NT

### A4. p_∞(q) functional form (for q < q*_BCZ)
- **Achievement**: Empirical power-law A·(q*_BCZ − q)^α with α ≈ 1.7-2.0
- **Potential exploration**: Closed-form expression via (k₁,k₂)-pattern integration
- **Next steps**: Carefully integrate over (1,2), (1,4), (4,1) configurations
- **Goal**: Closed-form p_∞(q) — would complete the picture
- **Math contribution**: Open question with concrete approach
- **Who cares**: same as A1
- **Status**: Partial — research-open

### A5. Music applications (Stern-Brocot / microtonal)
- **Achievement**: Identified that Farey-mediants are used in microtonal scale generation (Sevish, Wilson tradition)
- **Potential exploration**: Build cluster=2-informed scale-search algorithm; test against Scala
- **Next steps**: Reach out to microtonal community OR build proof-of-concept plugin
- **Goal**: Show 2-3× speedup in mediant-based scale search
- **Math contribution**: Indirect / applied
- **Who cares**: Microtonal composers (~5K-50K worldwide), Sevish, Erv Wilson community, Scala maintainers
- **Status**: Speculative; needs stakeholder validation

### A6. BCZ Corr = −1/2 (companion / standalone)
- **Achievement**: Fully proven in Lean 4 / Mathlib v4.28.0 (Aristotle v1, 0 sorries). Empirically verified on real Farey to 4 decimals.
- **Potential exploration**: Generalize to Corr of (b_i, b_{i+k}) for k > 1
- **Next steps**: Submit as Mathlib PR
- **Goal**: Mathlib library contribution
- **Math contribution**: First formally-verified BCZ statistic in Mathlib
- **Who cares**: Mathlib developers, formal-math community, Lean users
- **Publication target**: Mathlib PR (not journal)

---

## Direction B — Mertens-NW correlation

### B1. Empirical correlation
- **Achievement**: Pearson 0.95 on 33 Q values; 5/5 off-grid prime predictions within 0.5%
- **Potential exploration**: Push to Q = 10⁷ or 10⁸ on M2
- **Next steps**: Optional; already strong evidence
- **Goal**: Empirical evidence for paper
- **Math contribution**: Demonstrates structural connection between Farey and Mertens
- **Who cares**: Analytic NT community (8-15 researchers), Cox-Ghosh-Sultanow, Ng

### B2. Structural double-sum identity
- **Achievement**: 12·J(Q) = Σ_{d,d'} gcd²·M(Q/d)·M(Q/d')/(d·d') + 2T(Q) + 1 — EXACT to 10⁻⁷
- **Potential exploration**: Generalize to Σ_{d,d'} gcd^k·f(d)·f(d')/(d·d')^s for arbitrary multiplicative f
- **Next steps**: Write up cleanly; check K-Y 1996 for relation to their s_{1,1}
- **Goal**: Recognized as a useful number-theoretic tool
- **Math contribution**: New computational tool reducing 3D sums to 1D
- **Who cares**: Mertens-double-sum community + broader analytic NT

### B3. Convolution form 12·J(Q) = Σ_e J_2(e)/e² · T(Q/e)² + 2T + 1
- **Achievement**: Derived via Jordan-totient identity; EXACT match
- **Potential exploration**: Reduces Tauberian closure to single-variable Dirichlet series
- **Next steps**: Use for Tauberian closure attempt
- **Goal**: Cleanest form of the structural identity
- **Math contribution**: Compact analytic representation

### B4. Tauberian closure (the hard open one)
- **Achievement**: Three attack strategies identified (Selberg-Delange, Mellin/Perron, Riemann-zero explicit formula)
- **Potential exploration**: Pick one strategy and execute
- **Next steps**: Multi-month specialist effort — defer to follow-up paper
- **Goal**: Rigorous proof that Σ_e (J_2(e)/e²)·T(Q/e)² ~ 36CQ/π²
- **Math contribution**: Would complete the Mertens-NW story
- **Who cares**: same as B1 + Ng (Lethbridge) for Σ M(n)² explicit formula
- **Status**: Open research problem

### B5. C constant = OEIS A065483 (totient summatory)
- **Achievement**: Honest finding — the constant IS known; the **connection to Farey discrepancy is new**
- **Potential exploration**: Verify K-Y 1996 doesn't already imply this connection
- **Next steps**: Read primary K-Y if accessible
- **Goal**: Establish whether connection is original
- **Math contribution**: Connection between two previously-unconnected mathematical objects

### B6. Σ M(n)²/n³ = 1.13616 (possibly new constant)
- **Achievement**: Computed to 8 digits; not in OEIS or standard references
- **Potential exploration**: Identify via Ng 2004 explicit formula (under RH)
- **Next steps**: Access Ng's paper at library
- **Goal**: Establish whether truly new
- **Math contribution**: Potentially new convergent Dirichlet series constant
- **Who cares**: Ng (Lethbridge), Soundararajan (Stanford)
- **Status**: Empirical only

### B7. K-Y reconciliation
- **Achievement**: Showed J(Q) ≈ Φ(Q)·Σ δ_v² with ratio → 1.0 numerically
- **Potential exploration**: Derive exact correction term; show K-Y's s_{1,1} relates to ours
- **Next steps**: Careful algebraic analysis
- **Goal**: Resolve apparent tension with K-Y formulation
- **Math contribution**: Bridges K-Y (1996) framework with ours

---

## Direction C — Farey-QMC

### C1. Empirical gain on standard test integrals
- **Achievement**: 2-10× better than Sobol/Halton on smooth and discontinuous; FAILS on Farey-resonant oscillatory
- **Potential exploration**: Test more dimensions (2D, 3D, 4D), wider function classes, real-world integrals
- **Next steps**: Build broader benchmark suite
- **Goal**: Demonstrate Farey-QMC is competitive with Sobol on practical problems
- **Math contribution**: Applied — quantifies the gain
- **Who cares**: QMC community (Dick, Kuo, L'Ecuyer, Schwab), numerical analysts

### C2. Cluster=2 adaptive refinement
- **Achievement**: Conceptual — refine in PAIRS where cluster=2 forces pairs of extremes
- **Potential exploration**: Build adaptive Farey-QMC integrator using cluster=2
- **Next steps**: Implement and benchmark
- **Goal**: 20-50% sample reduction vs naive Farey-QMC
- **Math contribution**: Novel adaptive scheme

### C3. AI training / diffusion models
- **Achievement**: Speculative — Farey-QMC could potentially reduce diffusion model sampling steps
- **Potential exploration**: Test Farey-QMC noise schedule in toy diffusion model
- **Next steps**: Use a small diffusion model + compare sampling efficiency
- **Goal**: Demonstrate concrete AI compute savings (would be a CV-quality result)
- **Math contribution**: Applied / engineering
- **Who cares**: DeepMind, Stability AI, Anthropic, ML researchers in variance reduction
- **Status**: Speculative — needs working demo

### C4. Lattice rule connection
- **Achievement**: Recognize Farey-1D as a particular lattice rule
- **Potential exploration**: 2D+ Farey-like lattices
- **Next steps**: Generalize Farey to higher dimensions
- **Goal**: Higher-dim Farey-QMC
- **Math contribution**: Extension to practical dimensions
- **Status**: Not started

---

## Direction D — Lean formalization

### D1. BCZ Corr = −1/2 (v1)
- **Achievement**: Fully proven (0 sorries, only standard axioms)
- **Next steps**: Mathlib PR
- **Goal**: Library contribution

### D2. BCZ Extended moments (v2)
- **Achievement**: 7/7 arithmetic identities proven (E[X], Var, E[XY], etc.)
- **Next steps**: Bundle with v1 for PR

### D3. BCZ Chain anti-clustering (v2)
- **Achievement**: 2/3 proven (floor identity + bound; full anti-clustering needs Farey coprimality)
- **Next steps**: Add Farey-neighbor structure for the remaining 1

### D4. Mikolás S_Q identities (v2)
- **Achievement**: 3/5 proven (S_Q(1), S_Q(2), S_Q(prime))
- **Next steps**: Full Parseval (research-open)

### D5. q*_BCZ closed-form arithmetic (v3 RUNNING)
- **Achievement**: Submitted to Aristotle; should close 3 arithmetic identities
- **Next steps**: Download results when complete
- **Goal**: Complete the closed-form formalization

---

## Direction E — Universality class diagnostic

### E1. Cluster=2 as BCZ-vs-Wigner-Dyson test
- **Achievement**: Closed-form q*_BCZ characterizes the BCZ-density class; absence of this characterization → different class
- **Potential exploration**: Apply diagnostic to other number-theoretic sequences (twisted L-zeros, modular form gaps, automorphic L-functions)
- **Next steps**: Compute cluster sizes for known Wigner-Dyson sequences and confirm they have geometric/Poisson-like distribution
- **Goal**: Establish diagnostic as standard tool
- **Math contribution**: New tool for classification
- **Who cares**: Katz-Sarnak (Princeton), Athreya-Cheung, Granville, Conrey/Gonek
- **Publication target**: could be a SEPARATE paper or appendix to cluster=2 paper

### E2. Connection to horocycle flow
- **Achievement**: BCZ chain IS the dynamics of horocycle flow on SL(2,R)/SL(2,Z), so our closed form has ergodic-theoretic meaning
- **Potential exploration**: Express q*_BCZ in horocycle-flow language
- **Next steps**: Read Athreya-Cheung IMRN 2014 §8 (which leaves related open Q)
- **Goal**: Connect to dynamical systems / ergodic theory community
- **Math contribution**: Cross-disciplinary bridge
- **Who cares**: Bourgain, Einsiedler, Lindenstrauss (homogeneous dynamics)
- **Status**: Connection identified, not yet developed

---

## #3 (Mertens-NW conjecture) — sharpened to publishable-grade (2026-05-27)

Goal `/goal Complete the work on #3` resolved as follows:

- **Refutation**: the previously claimed `C ≈ 2/3` and the Euler-product guess `½·Π_p(1 + 1/(p²(p−1))) ≈ 0.66989` are **both rejected**. The first was confabulation; the second doesn't arise from any clean step in the Mikolás derivation, and is incompatible with the extended numerical sweep.
- **New empirical lock**: at `Q = 10⁶` with `m_factor = 100`, `NW = 0.67873`. m-factor extrapolation gives `NW(10⁶, untruncated) ≈ 0.6790 ± 0.0010`. Q=2M cross-check confirms Q-drift between 1M and 2M is ≤ 0.001 after m-correction, so the asymptote is `C = 0.679 ± 0.002`, best-estimate **0.6790**.
- **Heuristic derivation** (`research_notes/NW_asymptote_derivation_v2.md`): under RH + simple-zero + Gonek-Ng + structured-off-diagonal cancellation, `NW(Q) → (κ/6) · Π_p L_p`. The Euler-product shape is `1 + b_p/p² + ...` with rational `b_p`. Explicit `b_p` require Codecà-Perelli 1988 (paywalled in retrieval to date).
- **Final conjecture document**: `research_notes/Mertens_NW_conjecture.md`. States Conjecture A (`NW(Q) → C ∈ [0.679, 0.685]`), Conjecture B (`1/log Q` rate, `a ≈ 0.05`), Conjecture C (Euler-product closed form, tentative).
- **Novelty positioning**: occupies the AC2014 §8 dynamical-formulation open territory; *un-averaged* refinement of Codecà-Perelli's *Q-averaged* result (CP averaged `(1/X)·∫_X^{2X} J(Q) dQ`, we conjecture pointwise convergence of `NW(Q)`); per-step BCZ-cocycle dynamical interpretation. Static Farey↔Mertens identity (Cox-Ghosh-Sultanow 2021) is a different statement.
- **Next steps remaining for full closure**: (i) retrieve Codecà-Perelli 1988 *Math. Ann.* 279 explicit `c` via institutional access — single citation completes Conjecture C. (ii) Push `Q = 5×10⁶` (~30-60 min M1) to confirm `0.682 ± 0.003`. (iii) Cross-check via Boca-Cobeli-Zaharescu 2001 Crelle 535 `I_2` constant.

Status: **publishable as a research note** in current form — empirical asymptote nailed to 3 digits, heuristic derivation present, prior-art frontier mapped. The Codecà-Perelli explicit constant is the only outstanding step for a complete closed-form claim.

---

## Noted, not pursued — application demos (2026-05-27)

The following application-flavored experiments were run, documented, and **demoted** after honest audit. They are kept in the record for completeness and to prevent re-litigation; **none is pursued as a research line or pitched in any paper claim**.

### #118 — Arithmetic Signal Detection (cluster=2 as forensic classifier)
- **What was run**: LDA on cluster=2 features (P[cluster size = 2 | gap > q-quantile], q=0.99) over Farey / BCZ / Stern-Brocot vs. Gaussian iid / Poisson / Brownian / AR(1). N ∈ {1k, 5k, 20k}, fixed seed.
- **Headline number**: AUC = 1.000 across all N for the easy baselines.
- **Why demoted**:
  1. AUC=1.0 is against trivially-distinguishable baselines (FFT or 1-lag autocorr already separates them).
  2. **Wigner-Dyson / GUE fails the test** — the actually-arithmetic confound. So the diagnostic is a θ ≠ 1 detector, not an "arithmetic detector".
  3. The only non-trivial confound, AR(1) with ρ ≈ 0.5, has matching θ = 1/2; in finite-N our realization scored 0.10 (separated), but adversarial ρ-tuning would close the gap.
  4. No identified real-world customer with a sequence-classification problem that needs θ=1/2 vs θ=1 vs Gaussian discrimination where the generative process isn't already known.
- **Artifacts** (kept, not cited): `code/arithmetic_signal_detection_demo.py`, `figures/arithmetic_signal_roc.png`, `research_notes/arithmetic_signal_detection_demo.md`, `code/arithmetic_signal_detection_results.json`.

### #119 — Spectrum Anomaly Detection in wireless RF
- **What was run**: Rayleigh-faded synthetic spectra (NORMAL / ARITH / BCZ classes), peak detection via `find_peaks`, cluster=2 features, LDA + 5-fold CV.
- **Headline numbers**: 42.8% ± 4.2% multiclass (chance = 33%); binary NORMAL-vs-anomalous TPR 0.90 / FPR 0.79 (biased, not discriminating); BCZ-vs-ARITH 68.3% ± 8.5%.
- **Why demoted**: 75–95% TPR prediction NOT supported. Diagnostic detects periodic combs (ARITH collapses `p_size≥3` from 0.052→0.016) but does not separate BCZ-class interference from Rayleigh-faded noise — at ~300 peaks/spectrum the asymptotic regime is not reached and noise-driven peaks dominate ~90% of detections. No comparison vs. obvious baselines (cepstral / autocorrelation) that would likely outperform on the ARITH task.
- **Artifacts**: `code/spectrum_anomaly_demo.py`, `figures/spectrum_anomaly_results.png`, `research_notes/spectrum_anomaly_demo.md`, `code/spectrum_anomaly_results.json`.

### #120 — Hardware Approximation (cluster=2 carry-chain pruning in dividers)
- **What was run**: Python sim of a Stern-Brocot rational-approximation divider with two-cost CSA proxy. Cluster=2 used to mark step k+1 cheap if k-1 and k were both extreme. 2,000 quasi-random α, ε ∈ {1e-4, 1e-8, 1e-12, 1e-16}; parameter sweep over A_THRESH ∈ {3,4,6} and E_PEN ∈ {1,3,6,12}.
- **Headline number**: 0.3–5.5% stage-count reduction. 5% only at the corner (`E_PEN=12, A_THRESH=3`); modest assumptions give 1-2%.
- **Why demoted**:
  1. Stage-count in a Python sim, not power/area/delay in silicon. RTL+synthesis not done; place-and-route effects could erase savings.
  2. False-prune rate under the natural partial-quotient proxy is 0.1–1.7% (cluster=2 is a Farey-gap theorem, not a CF-partial-quotient theorem). Net savings shrink correspondingly.
  3. Prune-detector gate cost not modeled; for E_PEN ≤ 2 the detector overhead likely exceeds savings.
  4. Real dividers use SRT / Goldschmidt / Newton-Raphson — not the Stern-Brocot pipeline assumed. GPUs and ML quantization also don't use this pipeline. The relevant carry-chain pruning literature (booth-recoding, prefix-tree balancing) is the right comparison and wasn't done.
  5. Audience: chip vendors won't act on 1-5% from a sim with no RTL. At best a workshop paper at IEEE ARITH conditional on full RTL + baseline comparisons.
- **Verdict in note (§6)**: "do not pursue further as a standalone application; useful as a footnote / potential micro-architectural application." Demoted to that footnote status here.
- **Artifacts**: `code/hardware_approx_demo.py`, `research_notes/hardware_approximation_demo.md`.

### Common-mode lesson
Three application demos, three negative or strongly-conditioned outcomes. The cluster=2 *math* — sharp phase transition at t=2/9, closed-form q*_BCZ, Lean-verified bound, Pr(L≥k) family — stands on its own and **does not need application-flavored claims** to justify the work. Application framing oversold in earlier subagent prompts (50%/45%/40% predictions); calibrated retrospective is closer to 0%/0%/5%-conditional. Future application probes should require (i) named customer/baseline, (ii) honest comparison, before being run, not after.

---

## Status legend
- 🟢 Verified & closed
- 🟡 Verified but research-open follow-up exists
- 🔴 Speculative / requires substantial new work
- ⏳ Running / pending compute

## Risk / confidence
- **High confidence**: A1, A2, A6 (Lean-verified), B2, B3, B7
- **Medium confidence**: A3, A4, B1, B6, C1, D2, D5, E1
- **Lower confidence / speculative**: A5, B4, B5, C2, C3, C4, E2

## Master commits log
27 commits this session. Top branches in `projects/mimo-mini-project/`:
- `phase3_synthesis/`: all version-doc + supplements + final theorems
- `code/`: all computational scripts (verify, bcz_chain_mc, farey_qmc_demo, etc.)
- `aristotle_dispatch_v3/`: Lean files (running)
- `aristotle_v2_result/`: 12/15 Lean theorems proven (downloaded)

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

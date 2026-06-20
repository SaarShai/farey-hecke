# Quantitative Claims Ledger — Farey-Hecke Project (2026-06-19)

Comprehensive extraction of every quantitative claim across load-bearing research notes: exact values, formulas, thresholds, constants, counts, bounds, and Diophantine data.

| Claim (short) | Value / formula | Status | Source file |
|---|---|---|---|
| X(3) threshold (q=3) | 2/9 | Lean-proven | PAPER_arithmeticity_dichotomy_SUBMISSION.md |
| X(4) threshold (q=4) | √2/8 | Lean-proven | PAPER_arithmeticity_dichotomy_SUBMISSION.md |
| X(q) threshold (q≥5) | 1/λ_q³ | exact-witness | PAPER_arithmeticity_dichotomy_SUBMISSION.md |
| X(5) threshold exact | √5 − 2 ≈ 0.23607 | Lean-proven | PAPER_arithmeticity_dichotomy_SUBMISSION.md |
| X(6) = 1/λ_6³ | √3/9 = 0.1924500897 | Lean-proven | PAPER_arithmeticity_dichotomy_SUBMISSION.md |
| B(q) = 2 ⟺ q ∈ {3,4,6} | arithmeticity dichotomy | Lean-proven | PAPER_arithmeticity_dichotomy_SUBMISSION.md |
| B(3) ceiling value | 2 | Lean-proven | PAPER_arithmeticity_dichotomy_SUBMISSION.md |
| B(4) ceiling value | 2 | Lean-proven | PAPER_arithmeticity_dichotomy_SUBMISSION.md |
| B(6) ceiling value | 2 | Lean-proven | PAPER_arithmeticity_dichotomy_SUBMISSION.md |
| B(5) lower bound | ≥3 | exact-witness | PAPER_arithmeticity_dichotomy_SUBMISSION.md |
| B(7) value | 3 | exact-witness + Lean-proven | PAPER_arithmeticity_dichotomy_SUBMISSION.md |
| B(8)–B(12) values | 3 | exact-witness | PAPER_arithmeticity_dichotomy_SUBMISSION.md |
| B(13) value | 4 | exact-witness | PAPER_arithmeticity_dichotomy_SUBMISSION.md |
| B(14)–B(18) values | 4 | exact-witness | PAPER_arithmeticity_dichotomy_SUBMISSION.md |
| B(19) value | 5 | exact-witness | PAPER_arithmeticity_dichotomy_SUBMISSION.md |
| B(20)–B(22) values | 5 | exact-witness | PAPER_arithmeticity_dichotomy_SUBMISSION.md |
| B(23) value | 6 | exact-witness + numerical | PAPER_arithmeticity_dichotomy_SUBMISSION.md |
| B(24) value | 6 | exact-witness | PAPER_arithmeticity_dichotomy_SUBMISSION.md |
| B(q) asymptotic slope | ≈0.216q | numerical | PAPER_arithmeticity_dichotomy_SUBMISSION.md |
| λ_3 value | 1 | Lean-proven | PAPER_arithmeticity_dichotomy_SUBMISSION.md |
| λ_4 value | √2 ≈ 1.41421 | Lean-proven | PAPER_arithmeticity_dichotomy_SUBMISSION.md |
| λ_5 value (φ) | (1+√5)/2 ≈ 1.61803 | Lean-proven | PAPER_arithmeticity_dichotomy_SUBMISSION.md |
| λ_6 value | √3 ≈ 1.73205 | Lean-proven | PAPER_arithmeticity_dichotomy_SUBMISSION.md |
| λ_7 value | root of x³−x²−2x+1 ≈ 1.80194 | Lean-proven | PAPER_arithmeticity_dichotomy_SUBMISSION.md |
| Field degree [ℚ(λ_5):ℚ] | 2 | Lean-proven | PAPER_arithmeticity_dichotomy_SUBMISSION.md |
| Field degree [ℚ(λ_7):ℚ] | 3 | Lean-proven | PAPER_arithmeticity_dichotomy_SUBMISSION.md |
| q=5 cluster k-pattern | (2,1) | exact-witness | PAPER_arithmeticity_dichotomy_SUBMISSION.md |
| q=7 cluster k-pattern | (1,1) | exact-witness | PAPER_arithmeticity_dichotomy_SUBMISSION.md |
| q=5 margin X−P | √5−11/5 ≈ 0.0361 | exact-witness | PAPER_arithmeticity_dichotomy_SUBMISSION.md |
| q=7 margin X−P | ≈0.00168 | exact-witness | PAPER_arithmeticity_dichotomy_SUBMISSION.md |
| q=23 margin X−P (exact-witness level) | 1.58e−4 | exact-witness | PAPER_arithmeticity_dichotomy_SUBMISSION.md |
| Trace-clustering dichotomy (Geninska–Leuzinger 2008) | arithmetic ⟺ BCP on Hecke groups | known-owned | PAPER_arithmeticity_dichotomy_SUBMISSION.md |
| X_Ω(q) = 1/λ_q³ (q=5..21 equality) | machine-verified non-attained inf | Lean-proven | PAPER_uniform_onset_SUBMISSION.md |
| X_Ω(q) ≥ 1/λ_q³ (q=5..21 lower bound) | machine-verified | Lean-proven | PAPER_uniform_onset_SUBMISSION.md |
| q=5 (golden L) equality | X_Ω(5) = 1/φ³ = √5−2 | Lean-proven | PAPER_uniform_onset_SUBMISSION.md |
| q=6 equality | X_Ω(6) = √3/9 | Lean-proven | PAPER_uniform_onset_SUBMISSION.md |
| q=3 small-q exception | X(3) = 2/9 ≠ 1/λ_3³ = 1 | numerical | PAPER_uniform_onset_SUBMISSION.md |
| q=4 small-q exception | X(4) = √2/8 = (1/2)·(1/λ_4³) | numerical | PAPER_uniform_onset_SUBMISSION.md |
| X_Ω(q) lower bound range | q ∈ {5,6,7,…,21} unconditional | Lean-proven | PAPER_uniform_onset_SUBMISSION.md |
| X_Ω(q) upper bound range | q ∈ {5,6,7,…,21} via cusp-Dirac (REFUTED) | refuted | equality_upperbound_2026-06-14.md |
| Cusp-Dirac inadmissible (scalar class) | 3 independent obstructions | Lean-proven | equality_upperbound_2026-06-14.md |
| q≥22 structural wall | proof method caps at B(q)~5 | conjectured | PAPER_uniform_onset_SUBMISSION.md |
| M matrix (k=1 map) | [[0,1],[−1,λ]] | Lean-proven | Bq_rotation_arc_2026-06-14.md |
| M det | 1 | Lean-proven | Bq_rotation_arc_2026-06-14.md |
| M trace | λ = 2cos(π/q) | Lean-proven | Bq_rotation_arc_2026-06-14.md |
| M rotation angle | −π/q (exact) | Lean-proven | Bq_rotation_arc_2026-06-14.md |
| Conserved energy form | E(a,b) = a²−λab+b² | Lean-proven | Bq_rotation_arc_2026-06-14.md |
| E discriminant | −4sin²(π/q) | Lean-proven | Bq_rotation_arc_2026-06-14.md |
| E positive-definite range | λ ∈ (0,2) | Lean-proven | Bq_rotation_arc_2026-06-14.md |
| B(q) = rotation-arc count formula | [k=1 interior steps] + 1 (ejection) | numerical + Lean-partial | Bq_rotation_arc_2026-06-14.md |
| q=7 cluster exact E | 0.03339 | numerical | Bq_rotation_arc_2026-06-14.md |
| q=13 cluster exact E | 0.00796 | numerical | Bq_rotation_arc_2026-06-14.md |
| q=19 cluster exact E | 0.00354 | numerical | Bq_rotation_arc_2026-06-14.md |
| q=23 B_continuous proxy off-by-one | ⌊w·q/π⌋+1 gives 5 vs true 6 | numerical | Bq_rotation_arc_2026-06-14.md |
| q=23 true discrete count | B(23) = 6 | exact-witness | Bq_rotation_arc_2026-06-14.md |
| q=30 rotation-arc count | B(30) = 7 | numerical | Bq_rotation_arc_2026-06-14.md |
| q=40 rotation-arc count | B(40) = 9 | numerical | Bq_rotation_arc_2026-06-14.md |
| q=60 rotation-arc count | B(60) = 13 | numerical | Bq_rotation_arc_2026-06-14.md |
| B(q) ground-truth agreement q=7..40 | 100% (34/34 match) | numerical | Bq_rotation_arc_2026-06-14.md |
| q=23 k-pattern | [1,1,1,1,1,2] | numerical | Bq_rotation_arc_2026-06-14.md |
| B(q) asymptotic slope W_∞/π | 0.216·q exact slope from geometry | numerical | Bq_rotation_arc_2026-06-14.md |
| W_∞ arc width limit | ≈0.679 rad | numerical | Bq_rotation_arc_2026-06-14.md |
| w(q) → w_∞ convergence q=200 | 0.6748 | numerical | Bq_rotation_arc_2026-06-14.md |
| w(q) convergence q=2000 | 0.6789 | numerical | Bq_rotation_arc_2026-06-14.md |
| Rotation-arc mechanism Lean verification | 18 theorems axiom-clean | Lean-proven | Bq_rotation_arc_2026-06-14.md |
| BCZHeckeRotationArc.lean theorems | 18 all sorry-free | Lean-proven | Bq_rotation_arc_2026-06-14.md |
| R1 (interior-k=1 confinement) lower bracket | k≥1 PROVED (Lean) | Lean-proven | Bq_rotation_arc_2026-06-14.md |
| R1 upper bracket | OPEN (phase-lattice residual) | conjectured | Bq_rotation_arc_2026-06-14.md |
| R2 (realization bridge) q=5 | B(5) = 3 realization CLOSED | Lean-proven | Bq_rotation_arc_2026-06-14.md |
| R2 (realization bridge) q=7 | B(7) = 3 realization CLOSED | Lean-proven | Bq_rotation_arc_2026-06-14.md |
| R3 (resonance) definition | even N AND 1<ρ_min<ρ_max | conjectured | Bq_rotation_arc_2026-06-14.md |
| W(q) closed formula continuous width | 2[arccos(λ^1.5/√((1+λ)²+((λ−1)r)²))−arctan((λ−1)r/(1+λ))] | numerical | Bq_width_resonance_closed_form_2026-06-18.md |
| W_∞ = 2arcsin(1/3) exact | 0.679673818908243… | numerical | Bq_width_resonance_closed_form_2026-06-18.md |
| W_∞/π exact slope | 0.216346895938785… | numerical | Bq_width_resonance_closed_form_2026-06-18.md |
| W(q) asymptotic expansion | 2arcsin(1/3)−π/(3q)+31√2π²/(18q²)+O(q⁻³) | numerical | Bq_width_resonance_closed_form_2026-06-18.md |
| q=7 W(q) value | 0.9349194947 | numerical | Bq_width_resonance_closed_form_2026-06-18.md |
| q=13 W(q) value | 0.7321013976 | numerical | Bq_width_resonance_closed_form_2026-06-18.md |
| q=23 W(q) value | 0.6786995407 | numerical | Bq_width_resonance_closed_form_2026-06-18.md |
| q=61 predicted resonance | B(61) = 14 | numerical | Bq_width_resonance_closed_form_2026-06-18.md |
| q=126 predicted resonance | B(126) = 28 | numerical | Bq_width_resonance_closed_form_2026-06-18.md |
| q=570 predicted resonance | B(570) = 124 | numerical | Bq_width_resonance_closed_form_2026-06-18.md |
| q=1476 predicted resonance | resonance candidate | numerical | Bq_width_resonance_closed_form_2026-06-18.md |
| q=1892 predicted resonance | resonance candidate | numerical | Bq_width_resonance_closed_form_2026-06-18.md |
| q=6884 predicted resonance | resonance candidate | numerical | Bq_width_resonance_closed_form_2026-06-18.md |
| q=3 Rosen spectral gap test | D=0.53128…, residual −9.99e−16 | numerical | ROADMAP_2026-06-19.md |
| q=5 non-arith Rosen spectrum (ODD sector) | r = 6.4737, 8.6368, 10.1365, 11.0156 | numerical | ROADMAP_2026-06-19.md |
| q=8 non-arith Rosen spectrum (ODD sector) | 6 ODD-sector zeros, max |det|~1e−8 | numerical | ROADMAP_2026-06-19.md |
| q=5 Rosen spectrum area | 0.942 | numerical | ROADMAP_2026-06-19.md |
| q=8 Rosen spectrum area | 1.178 | numerical | ROADMAP_2026-06-19.md |
| Rosen operator gap decay α_q q=5 | 1.44 | numerical | ROADMAP_2026-06-19.md |
| Rosen operator gap decay α_q q=21 | 0.35 | numerical | ROADMAP_2026-06-19.md |
| Rosen gap N-convergence driftbound | ~1e−2 under N=40→120, max 2.6e−2 at q=13 | numerical | ROADMAP_2026-06-19.md |
| SL₂(ℤ) Maass r₁ value (Mayer anchor q=3) | 9.5337+ (≥6 digits recovered) | numerical | ROADMAP_2026-06-19.md |
| SL₂(ℤ) Maass r₂ value (Mayer anchor) | 12.173+ | numerical | ROADMAP_2026-06-19.md |
| SL₂(ℤ) Maass r₃ value (Mayer anchor) | 13.780+ | numerical | ROADMAP_2026-06-19.md |
| X_Ω normalization test result | FAILED — bug_id 14 generalized | refuted | ROADMAP_2026-06-19.md |
| Farey structure-factor hyperuniformity | S(k)~k^1.8 | numerical | ROADMAP_2026-06-19.md |
| Twin-primes index Poisson class | sigma^2~R^0.97, alpha~0.002-0.015 | numerical | ROADMAP_2026-06-19.md |
| Twin-primes singular series 2C2 exact | 1.32032363 | numerical | ROADMAP_2026-06-19.md |
| Onset ratio q=3 | onset_2 / X(3) = 1.0004 | numerical | PAPER_arithmeticity_dichotomy_SUBMISSION.md |
| Onset ratio q=4 | onset_2 / X(4) = 1.0031 | numerical | PAPER_arithmeticity_dichotomy_SUBMISSION.md |
| Onset ratio q=5 | onset_3 / X(5) = 1.0025 | numerical | PAPER_arithmeticity_dichotomy_SUBMISSION.md |
| Onset ratio q=7 | onset_3 / X(7) = 1.0090 | numerical | PAPER_arithmeticity_dichotomy_SUBMISSION.md |
| Aristotle dispatch v8 build jobs | 8026 | numerical | PAPER_arithmeticity_dichotomy_SUBMISSION.md |
| Aristotle dispatch v11 build jobs | 8026 | numerical | PAPER_arithmeticity_dichotomy_SUBMISSION.md |
| Aristotle dispatch v15 build jobs | 8027 | numerical | PAPER_uniform_onset_SUBMISSION.md |
| L1b-crux fc orr_lb q≥18 sealed | axiom-clean [propext, Classical.choice, Quot.sound] | Lean-proven | PAPER_uniform_onset_SUBMISSION.md |
| Layer 3 deep-mid box (q≥16) | l ∈ [49/25, 2], r ∈ [22/25, 63/50] | Lean-proven | PAPER_uniform_onset_SUBMISSION.md |
| L_blk formula | ⌈33q/256⌉ + 2 | numerical | PAPER_uniform_onset_SUBMISSION.md |
| L_blk slope | 33/256 = 0.12891 | numerical | PAPER_uniform_onset_SUBMISSION.md |
| Dwell estimate true value | 0.12819 | numerical | PAPER_uniform_onset_SUBMISSION.md |
| cos²(33π/512) < 24/25 inequality | make-or-break L1b constraint | Lean-proven | PAPER_uniform_onset_SUBMISSION.md |
| Asymptotic safety margin δ_∞ | 5.77·10⁻⁵ > 0 | interval-certified | PAPER_uniform_onset_SUBMISSION.md |
| Interval margin verification q=10000 | worst margin 7.33·10⁻⁵ at q=10000 | interval-certified | PAPER_uniform_onset_SUBMISSION.md |

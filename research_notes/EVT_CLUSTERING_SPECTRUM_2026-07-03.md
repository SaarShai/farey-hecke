# EVT clustering spectrum of Farey/Hecke gaps — session record 2026-07-03

Status tags: [LEAN] machine-verified · [NUM] verified numerics · [DERIV] analytic derivation, unformalized · [PROGRAM] proof plan, not yet executed.

## Result 1 — θ = 1/2 for large-gap extremes: core now machine-verified

- [LEAN] `farey_no_triple_large_gap` (projects/evt-farey-gaps/proved/aristotle_pairing_aristotle/FareyPairingLemma.lean, Aristotle project 22e93551, sorry-free, axioms {propext, Classical.choice, Quot.sound}): four consecutive Farey denominators cannot have all three products < Q²/8, given adjacent-sum > Q and the two-sided neighbor-recursion inequalities. ⟹ exceedance clusters at deep thresholds have size ≤ 2. Note: h23 unused by the proof (statement can be tightened later).
- [NUM] projects/evt-farey-gaps/{evt_farey.py,results.json,summary.log} (Q=10⁴, 3·10⁴; 3.0·10⁷ / 2.7·10⁸ gaps): θ_runs = 0.500163 (s=0.01, Q=3·10⁴); clusters 27611/27629 exactly size 2, none ≥3; within-pair product ratio → 1 (1.0002 at s=3·10⁻⁴). Independently reproduced by main agent (clusters=51396 exact match at Q=10⁴, s=0.05 cell).
- Consistent with the prior general-q Taha-section numerics (research_notes/theta_half_repp_2026-06-14.md: θ→0.5013, Pr(L=2)≥0.994, q=4,5,7).

## Result 2 — θ_edge = 2/3 at the hard edge (smallest gaps): NEW exact constant

- [DERIV] Exceedance region {ab>1−δ} shrinks to the parabolic fixed point (1,1) of the BCZ k=2 branch (DT=[[0,1],[−1,2]], double eigenvalue 1). In x=1−a, y=1−b: in-cluster map = shear (x,y)→(y,2y−x), conserving d=y−x ⟹ in-cluster denominators form an arithmetic progression (q_{i+1}=2q_i−q_{i−1}). Exit-set flux integral on the triangle {x+y<δ}: exit fraction = (1/6+1/6)/(1/2) = **2/3 = θ_edge**. Entry flux ∝ |d| ⟹ cluster-size tail P(L≥n) ≍ n^{−2}, E[L]=3/2.
- [NUM] θ_runs → 0.66689 (δ=0.01, Q=3·10⁴); E[L] = 696012/462214 = 1.5058 vs 3/2; tail slope −1.94..−2.01; AP-signature fraction = 1 (ALL clusters of size ≥3, every δ, both Q). Finite-size scaling variable = δQ (θ inflates when δQ ≲ 60 — d-quantization d=m/Q).
- Caveat: Ferro–Segers estimator disagrees (0.38–0.55) — expected bias for rigid deterministic sequences; runs estimator + E[L] reciprocal + exact flux integral are the three concordant routes.
- Distinct from the ONSET regime: B(q) ceilings / arithmeticity dichotomy live at threshold X(q) (elliptic λ-branch); the hard edge is the k=2 parabolic branch. No contradiction with B(3)=2 (different threshold regimes). Parabolicity kλ_q=2 forces λ=1 ⟹ **q=3 is the unique parabolic hard edge**; for q≥5 edge stability type under probe (gq_edge_stability.py, GLM agent, pending) — θ_edge(q) potentially a new q-family invariant.
- Lit check (research-lite, 2026-07-03): 1-D neutral-fixed-point EVT known (FFF arXiv:1503.01372, FFT arXiv:1008.1350); 2-D shear/Jordan-block case: NOTHING FOUND; Farey/BCZ gap extremes: NOTHING FOUND.
- [NUM-preliminary] G_q hard-edge trichotomy (projects/evt-farey-gaps/gq_edge_stability.py + gq_edge_results.json, 10⁷-step orbits): q=3 parabolic (analytic trace 2; script's trace-11195 at q=3 is a finite-difference artifact across a branch boundary — do not cite), mean deep-cluster 1.522 ≈ 3/2 ✓; q=5 hyperbolic, trace = 2λ₅ = 3.236068, mean cluster 1.000; q=7 elliptic, rotation exactly π/7, mean cluster 1.000. Candidate rigidity statement: hard-edge clustering (θ_edge<1) occurs ONLY at the unique parabolic case q=3 (kλ_q=2 ⟹ λ=1); non-arith edges have isolated extremes. NEEDS: exact-section enumeration + deeper thresholds before claiming.

## Result 3 — [PROGRAM] the θ=1/2 THEOREM without the BCZ mixing-rate open problem

Prior blocker (theta_half_repp_2026-06-14.md §8.4) was route-specific (FFFV/operator-renewal needs quantitative BCZ mixing — open). Bypass via homogeneous dynamics:

- Marklof–Pollicott, Nonlinearity 38 (2025) 055003 (arXiv:2408.01781): Thm 1 = max-excursion law; **Thms 2–3 = joint convergence of successive hitting times + impact parameters for shrinking Poincaré sections, ALL finite-covolume Fuchsian groups** (Hecke G_q included). Explicitly NOT proven there (nor in Kirsebom–Mallahi-Karai arXiv:2209.07283, modular-surface max-only): extremal index, Poisson excursion process, k-th order statistics, interexcursion gaps.
- Program: (1) [done, LEAN core] deep exceedance clusters ↔ single cusp-region entries, exactly 2 exceedances per entry (pairing lemma + cusp-swap involution); (2) derive Poisson convergence of the ENTRY process from M–P Thms 2–3 (successive-hits convergence + their exponential ω-bounds ⟹ counting-process convergence on finite windows; factorial-moment bookkeeping); (3) O'Brien/compound-Poisson assembly ⟹ θ=1/2 + k-th deepest laws + interexcursion gaps, uniformly in q.
- Deliverable ladder: reduction draft → check with M–P framework → (Koyama-gate) paper. The BCZ mixing rate REMAINS open — it is simply not needed for this theorem.

## Correction log (honesty)

- Main agent's initial hard-edge predictions θ~c/log(1/δ) and tail n^{−1} were REFUTED by numerics; corrected flux computation (entry flux ∝ |d|) yields the confirmed n^{−2} tail and exact 2/3. One theory-correction cycle, as designed.
- Earlier "Fréchet-1 with log corrections" for spatial large-gap tail was wrong (missed the a+b>1 constraint): tail is quadratic; deepest gaps sit at bounded-denominator fractions ⟹ spatial max framing is degenerate-deterministic; the random-orbit (M–P) frame is the correct probabilistic setting — matches repo convention.

## Track B (session-parallel)

Independent G_5 even-resonance cross-check: codex attempt stalled (runtime hold, no results); reassigned to GLM (results_glm.json pending). Certified targets: 0.45389518+5.76353724i, 0.41054374+7.81976825i, 0.48500000+13.56500000i (table research_notes/certified_hecke_spectrum_table.md; run bx2scmyrr COMPLETED per state brief; extended-band Kaggle kernel prepared but NOT pushed — open item).

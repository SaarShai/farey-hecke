# PS-0 deformation scoping — COLD ADVERSARIAL REFEREE

> Installation note (orchestrator, 2026-08-23): report received verbatim from
> the read-only referee seat and installed unchanged. Referee seat wrote no
> repo files itself.

Date 2026-08-23. Subject: `research_notes/rh_goals_2026-08-14/lane_g/PS0_DEFORMATION_SCOPING_SOL.md` (192 lines, UNREFEREED).
Evidence: arXiv API sweeps (author/abstract queries, 2021–2026 windows), full text of arXiv:1201.2324 (BFM) and 2002.03334, abstracts of 1011.4441 / 1812.05554 / 1110.2150 / 1503.00525 / 1606.09109 / 2509.17936 / 0804.4837 / 1810.04489, repo source `.worktrees/aletheia-restore/engine/certify/certify.py` and `code/zeta_cert_rosen.py`, repo notes `R3B_FLAGSHIP_CERT.md`, `LAW_DEFORMATION_PRIOR_ART.md`, `practical_value_2026-08-16/PRIOR_ART_CERTIFIED_SPECTRAL.md`.

## VERDICT: PROMOTABLE-WITH-CORRECTIONS (8 majors, 5 minors)

The core judgment — narrow, do not kill; the surviving niche is certificates, not mechanism — survives my independent check. The gap (i) off-line resonances + (ii) deformation family with arithmetic point + (iii) interval-certified localization is, on my searches, still unoccupied. But the sweep that produced it missed the single most relevant author in the field, the recommended family is probably the wrong one because of that miss, two prior-art characterizations are materially inaccurate, and one capability claim about our own repo is stronger than the repo's own referee record.

### Criterion-by-criterion

| # | Criterion | Evidence | Grade |
|---|---|---|---|
| 1 | Gap unoccupied 2021–2026 | `au:"Strohmaier" AND cat:math.SP` → no post-2021 resonance-family paper (last: 1812.05554, 2018). `abs:resonances AND abs:"interval arithmetic"`, `abs:"validated numerics" AND abs:resonances`, `abs:"computer-assisted" AND abs:resonance AND cat:math.SP`, `abs:"rigorous error bounds" AND abs:resonances` → nothing in scope. Weich: last resonance papers 2012–13. No certified-resonance-along-a-family paper found. | PASS, with C4 |
| 2 | DROP verdict leaves this alive | `DISCOVERY_SYNTHESIS_2026-06-20` salvage clause explicitly permits "a certified resonance Re-value table (data artifact, not a theorem)". PS-0's gap = that salvage + one parameter. Not a repackaging of the killed mechanism claim. | PASS, with C6 |
| 3 | Kill-trigger / what BFM computed | Full text 1201.2324: Thm 1.4 gives curves only for `k ≥ k1` (k1 unspecified) with `α_k(t) = (1/π)e^{A/2t}e^{−πk/t}(1+O(1/k))`; Thm 1.5 tangency with `δ_k = O(e^{−2πk/t_ℓ})`. | FAIL — C3 |
| 4 | PS-1 port coherent with the Arb engine | `engine/certify/` in the working tree is EMPTY; engine lives only in `.worktrees/aletheia-restore/`. `zeta_cert_rosen.py` is Rosen-CF/λ_q-specific throughout. | FAIL — C1, C5, C7, C8 |
| 5 | Area/Weyl constants | Independently re-derived: `∫_{−λ/2}^{λ/2}∫_{√(1−x²)}^∞ dy/y² dx = 2 arcsin(cos(π/q)) = π − 2π/q = 2π(1/2 − 1/q)`. Weyl `(|F|/4π)T²` standard. | PASS |

### Majors

**C1 — the sweep missed Pohl; the recommended family is probably wrong.** arXiv:1503.00525 (Pohl, "Symbolic dynamics, automorphic functions, and Selberg zeta functions with unitary representations") builds transfer operators and Selberg zeta for **Hecke triangle surfaces with arbitrary finite-dimensional unitary representations χ**; arXiv:1606.09109 (Möller–Pohl conjecture solved) ties eigenvalue-1 eigenfunctions of the fast operator to zeros of `Z(Γ,χ;·)` for **any** Hecke triangle group and **any** unitary χ. §3 item 3 marks the weight/multiplier direction "not swept in depth — OPEN" and §3 item 1 asserts Γ₀(4) is the uniquely instrumented candidate: both are refuted. Consequence: the character variety of our own `G_q` has published coding, so PS-2 becomes "add unimodular χ(γ) weights to the existing Rosen blocks" rather than "import Mayer's Γ₀(4)-induced coding wholesale". Cheaper, less crowded, and it keeps the calibrated q=5/q=7 pins. §6 must be re-decided against this option before compute. No Pohl row exists anywhere in the §2 table; a claim of the form "nobody combines X" is not acceptable from a sweep that omits the field's principal author.

**C2 — "our repo already holds (i)+(iii)" is over-claimed.** §2 line 57–59. `R3B_FLAGSHIP_CERT.md:83`: "this is the R2/R3 closed-contour computation. MMS sector/factorization and the separate closed `det(1−K_s) ≠ 0` identification remain outside this verdict." `practical_value_2026-08-16/PRIOR_ART_CERTIFIED_SPECTRAL.md` repeats the boundary ("'ours' means the methodological package, not an unconditional assertion that every link from the computed determinant to a resonance has been discharged"), and the effective theorem is banked CONFIRMED-**conditional**. What we certify is a winding-1 box for a truncated transfer-operator determinant plus a tail bound — the determinant→resonance link is not fully discharged. Restate as: "(i)+(iii) at fixed groups **at conditional scope**".

**C3 — BFM mischaracterized, and the kill-trigger as written can never fire.** §2 table and §5 call Thms 1.4/1.5 a "rigorous off-line curve theorem". They are rigorous but **asymptotic and non-effective**: valid for `k ≥ k1` with `k1` unspecified, uniformly on a bounded height interval, and the corresponding character values are exponentially small, `α_k(t) ≈ (1/π)e^{A(1/2+it)/2t}e^{−πk/t}`. So BFM never covers a finite α of the size where Fraczek's drift is visible (α ~ 0.1). §6's kill-trigger ("if BFM cover the targeted zero's off-line locus … kill") is therefore vacuous as stated, and — read the other way — the real novelty axis is *effective + finite-α*, not merely *certified*. Rewrite the trigger to something falsifiable, e.g. "kill if an effective version of BFM Thm 1.4 with explicit `k1` appears, or if the target zero's α-range lies inside a proved locus."

**C4 — two competitor lines uncited, one of them a live scoop-in-progress.** (a) Levitin–Strohmaier 1812.05554 do **not** just move in Teichmüller space: their abstract states they "rediscover the four arithmetic surfaces of genus one with one cusp" numerically. That is exactly option 2's family-with-arithmetic-point, already occupied at the numerical tier — so §3's implication that option 2 is "more novel" is wrong; there too our only delta is certification. (b) Bandtlow–Pohl–Schick–Weiße, arXiv:2002.03334, compute resonances of **Schottky-surface families** by transfer operator + Lagrange–Chebyshev; I read the full text and found no interval-certified output (so the gap survives), but Bandtlow–Slipantschuk's explicit a-priori transfer-operator eigenvalue bounds (0802.0994, 2004.03534) are precisely the missing ingredient in the same authors' hands. Record this as the nearest scoop risk with a re-check date.

**C5 — "Selberg-zeta zeros = resonances" is asserted, not established, and it is character-dependent.** §2 table, FM row. For `α ≠ 0` Selberg's character changes which cusps of Γ₀(4) are singular, hence the Eisenstein/continuous-spectrum contribution and hence the divisor of `Z(α,·)` (BFM themselves say for `α=0` the off-line zeros sit at zeros of `ζ(2β)` and at `πiℓ/log 2`, and note in §3.2 that "`β − β²` qualifies better" than calling these eigenvalues). A certificate on `det(1−L_{s,α})` certifies a zeta zero; upgrading it to "resonance" requires the divisor argument — the same identification step C2 says is open at fixed groups. This must be listed as a named PS-2 obligation, not folded into "port and certify".

**C6 — internal contradiction on PS-relevance.** §4 line 111 says "nothing we own currently bears on the PS conjecture itself", then lines 112–114 say a PS-4/PS-5 result would be "evidence-grade for PS". Certified boxes at finitely many α carry zero information about `N_d(T) = o(T²)`. Delete the evidence-grade clause or downgrade it to "illustrative of the dissolution phenomenon, with no bearing on the counting conjecture".

**C7 — the named execution target does not exist.** §6 says PS-2 = "port a published symbolic coding into `engine/certify/`". `ls engine/certify` → empty; the evaluator `_hecke_transfer_operator_evaluator` and `zeta_cert_rosen.py` exist only under `.worktrees/aletheia-restore/`. Either the restore is a precondition of PS-2 (say so, with the path) or the plan is unexecutable as written.

**C8 — the α-certification design is weaker than what the engine already supports.** §6 proposes "interval boxes at a finite grid of α values, plus a perturbation bound gluing adjacent boxes". A perturbation/derivative bound in α is the hard route. The determinant is holomorphic in `s` and real-analytic in α, entries pick up unimodular `χ_α(γ) = e^{2πiα}` factors, and `winding_offline` already runs entirely in `acb` balls — so evaluating the contour with α itself an **interval ball** yields, when the det ball excludes 0 on the whole contour, "for every α in this interval there is exactly one zero in this box". That is the gluing, for free, with no perturbation lemma. What genuinely changes with α: (a) per-block unimodular weights and loss of the real/parity symmetry that the `sign = ±1` reduction exploits (the `λ = ±1` reduced sectors of FM are the α-analogue and must be re-derived), (b) the dimension-tail bound `dim_tail_from_matrix` must be re-proved uniform in α over the ball — unimodularity makes this plausible but it is a theorem, not a port, (c) contour width must exceed the α-induced drift or the winding degrades to 0/undefined.

### Minors

- m1: repo's own `practical_value_2026-08-16/PRIOR_ART_CERTIFIED_SPECTRAL.md` (INTLAB / kv / Arb / Petković argument-principle survey) is the direct antecedent for the "(iii) certified" column and is not cited.
- m2: BFM name arithmetic values `α ∈ {1/8, 1/4, 3/8, 1/2}`, not only `α = 0`. More than one certifiable anchor exists on the same path — an asset the doc misses.
- m3: Fraczek–Mayer–(Strömberg), arXiv:0804.4837, "Computation of Selberg zeta functions on Hecke triangle groups" is uncited here though it is prior art for our *own* `G_q` zeta computations (it is cited in `LAW_INDUCED_FEASIBILITY.md`).
- m4: arXiv:2509.17936 (Sept 2025) approximates `Z_{Γ_w}` by finite determinants with an **explicit exponentially decaying error** for Hecke `Γ_w` — closest published analogue of our tail bound, uncited (infinite-area, so not a scoop, but it belongs in the table).
- m5: no cost estimate anywhere (matrix size N, α-grid density, wall-clock), so "PS-2 becomes squarely our demonstrated capability" is unfalsifiable as a cost claim.

### What passed cleanly

- Area/Weyl: `|F_q| = 2π(1/2 − 1/q)` re-derived independently and exact; the factor-2 correction is right and `(|F_q|/4π)T²` is the correct Weyl normalization.
- Rigidity of triangle groups, `q → ∞` as elliptic degeneration, Γ(2)/thrice-punctured sphere rigid, `PSL(2,Z)'` = once-punctured torus with Teich dim 2: all correct.
- §1's inheritance of the DROP verdict and of the Hejhal 7.11/7.12 + Garbin–Jorgenson mandate matches `LAW_DEFORMATION_PRIOR_ART.md` at source.
- Novelty ceiling in §6 and the caveats ledger are honest and unusually well-calibrated; the "instrument, not mechanism" framing is the correct one.

---

**Final: PROMOTABLE-WITH-CORRECTIONS.**
- C1 Sweep omits Pohl's transfer operators for Hecke triangle groups with unitary reps (1503.00525, 1606.09109) — the Γ₀(4) family recommendation must be re-decided against a `G_q + χ` family that reuses our own coding.
- C2 "Repo already holds (i)+(iii)" ignores `R3B_FLAGSHIP_CERT.md:83`: determinant→resonance identification is outside the certified scope.
- C3 BFM Thms 1.4/1.5 are asymptotic and non-effective (`k ≥ k1` unspecified, `α_k ~ e^{−πk/t}`), so the stated kill-trigger can never fire.
- C4 Uncited competitors: Levitin–Strohmaier already do family+arithmetic-point numerically; Bandtlow–Pohl–Schick–Weiße 2002.03334 + Bandtlow–Slipantschuk bounds are an active scoop risk.
- C5 "Selberg-zeta zeros = resonances" is character-dependent and must be a named PS-2 obligation, not an assumption.
- C6 §4 contradicts itself: "nothing bears on PS" vs "evidence-grade for PS".
- C7 `engine/certify/` is empty in the working tree; the engine exists only in `.worktrees/aletheia-restore/`.
- C8 Use α-ball contour enclosure (already supported by `winding_offline`) instead of grid + perturbation gluing; re-prove the dim-tail bound uniform in α and re-derive the `sign = ±1` sector reduction.

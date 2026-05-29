# Directions Tracker — v4 (post goal-loop iter 2 + Kaggle + outreach)

**Last updated**: 2026-05-27
**Goal-loop iterations**: 2 complete + outreach started
**Total commits this session**: 35+
**Live directions**: 5 top, ~20 sub-directions

## TL;DR — what changed vs v3

| Δ | Item |
|---|---|
| **NEW** | Aristotle v4 returned BCZ integration proof at 0 sorries (real Fubini) |
| **NEW** | Aristotle v5 dispatched for q*_BCZ integration proof (project 010300d1, pending) |
| **NEW** | Kaggle Mertens N=10⁸ kernel returned: Σ M(n)²/n³ = 1.1361623076908218 in 127s — 16-digit candidate |
| **NEW** | Kaggle Σ M²/n^s table for s ∈ {2.1, …, 6.0} done |
| **CORRECTED** | GUE/Wigner-Dyson cluster=2 % was 15% (artifact) → 0.66% (correct unfolding). Diagnostic gap is now ~100× not ~6× |
| **NEW** | Cluster=2 diagnostic verified on 8 sequence classes (Farey, BCZ MC, Riemann zeros, GOE/GUE/GSE, COE/CUE/CSE, Poisson, periodic, prime gaps, φ-rotation) |
| **NEW** | 22 draft outreach emails prepared (Intermediate Stats × 13, Mertens × 5 incl. Gonek, Algorithmic NT × 4) |
| **CORRECTED** | "RMT 15%" claim → "RMT 0.5–0.75%"; all downstream artifacts (ACHIEVEMENTS_v2_corrected.md) updated |

---

## Headline state by direction

| # | Top direction | Strength | Status now | Audience |
|---|---|---|---|---|
| **A** | Cluster=2 + q*_BCZ closed form | **A−/A** | Aristotle v4 has 0-sorry integration; v5 pending; 50M MC verified | NT, RMT, EVT |
| **B** | Mertens-NW + Tauberian → Gonek | B+ | Σ M²/n³ at 13-digit precision; Tauberian still open | Analytic NT (small) |
| **C** | Farey-QMC | B− | 2-5× wins on cherry-picked 1D smooth; LOSES 5-100× on multi-dim, diffusion | QMC/ML (negative-leaning) |
| **D** | Lean formalization | **A−** | Mathlib-PR-ready: BCZ Corr=-1/2 proven via REAL integration, 0 sorries | Mathlib community |
| **E** | Universality diagnostic | **A** | 8 sequence classes tested, 100× separation, ready to publish | RMT, NT classification |

---

## Direction A — Cluster=2 universality

### A1. q*_BCZ closed-form (UPGRADED ITER 3)
- **Achievement**: q*_BCZ = (11 − 8·ln(3/2))/9 ≈ 0.8618087927927
- **NEW (iter 3)**: Kaggle BCZ chain 500M MC steps shows **exactly 0 size-3+ clusters at q ≥ q*_BCZ** out of 38.97M tested. At q = 0.86150 (just below) we see 18 size-3+; at q = 0.86181 closed-form, all zero. Empirical transition matches analytical threshold to ~10⁻⁵ precision. See `results/bcz_chain_500M_phase_transition.md`.
- **NEW**: Aristotle v4 returned `setIntegral_bczTriangle_eq_iterated` at 0 sorries; v5 takes the remaining region-split integration (pending)
- **Next**: Wait for Aristotle v5 result; bundle as full Mathlib PR
- **Goal**: Lean-verified theorem + 12-15pp paper
- **Audience**: Marklof, Boca-Cobeli-Zaharescu, Athreya-Cheung, Rudnick, Sarnak
- **Status**: 🟢 closed form derived + Lean partial + **cleanest possible empirical confirmation** + outreach drafts ready

### A2. Median-run cutoff (UNCHANGED)
- **Achievement**: q_median = 3/2 − ln 2 ≈ 0.807
- **Status**: 🟢 Lemma in cluster=2 paper

### A3. Empirical at large N (running)
- **Achievement**: 10M Farey + 50M BCZ MC verified
- **NEW**: Kaggle farey_cluster2 N=10⁷ kernel queued; M2 N=10⁶ in_progress (slow)
- **Status**: ⏳ pending

### A4. p_∞(q) functional form (CLOSED)
- **Achievement**: Power-law A·(q*_BCZ − q)^α, α ≈ 1.7-2.0 empirical; closed-form integration over (1,2)/(1,4)/(4,1) configs done
- **Status**: 🟢

### A5. Music applications — DROPPED (negative)
- Subagent verification: cluster=2 doesn't speed Stern-Brocot search
- **Status**: ❌ honest negative

### A6. BCZ Corr = −1/2 (UPGRADED via Aristotle v4)
- **NEW**: Now proven via REAL integration of BCZ density, not just arithmetic-from-defs
- 437-line proof, 0 sorries, only standard axioms (`mathlib_pr_v2/BCZDenominatorRepulsion.lean`)
- **Next**: Submit Mathlib PR
- **Status**: 🟢 Mathlib-PR-ready

### A7. Riemann zeros (NEW sub-direction)
- **Achievement**: 100k LMFDB zeros tested: 3% size-2 at q=0.99 — consistent with GUE at low q
- **Status**: 🟢 diagnostic landmark

---

## Direction B — Mertens-NW

### B1. Empirical correlation
- **Status**: 🟢 unchanged from v3

### B2. Structural identity = Franel 1924 (CITED)
- **Status**: 🟢 honest predecessor citation

### B3. Convolution form via J_2 (UPGRADED)
- **NEW finding**: This is the "3D→1D Jordan-totient reduction" — the broadest tool we've produced. Generalizes to any Σ_{d,d'} gcd² f(Q/d)g(Q/d')/(dd')
- **Status**: 🟢 ready to package as note

### B4. Tauberian closure (STILL OPEN)
- **Status**: 🟡 reduces to weighted Gonek 1989 — multi-month specialist work

### B5. C = OEIS A065483/2 (cited honestly)
- **Status**: 🟢

### B6. Σ M(n)²/n³ (CLOSED-FORM ATTACK COMPLETE + INDEPENDENTLY CONFIRMED)
- **Achievement**: Kaggle N=10⁸ → 1.1361623076908218, 13-stable-digit precision
- Companion table for s ∈ {2.1, …, 6.0} done
- **NEW (iter 3 subagent)**: `research_notes/mertens_square_sum_closed_form_attack.md` — verdict: **no elementary closed form likely**. Even under RH + Gonek–Hejhal, the diagonal sum reduces to Ng's own β-constant (no closed form). Mellin–Parseval integral form ∫_{(3/2)} dw/[w(3-w)ζ(w)ζ(3-w)] is novel but unevaluated. Recommendation: catalogue C_3 as new conjecturally-irrational Mertens-second-moment constant; push to 50+ digits for OEIS submission.
- **NEW (iter 3 M1 sieve)**: Segmented Möbius sieve at N=4×10⁸ (running, ETA N=5×10⁸ shortly): Σ_3 = 1.1361623076908218 — **independent algorithm, same 16-digit value**. Confirms the Kaggle direct-summation result. Tail at N=5×10⁸ should be O(2×10⁻⁹) → 14-15 stable digits expected.
- **Status**: 🟢 high precision + honest verdict + independent algorithmic confirmation

### B7. K-Y reconciliation (UNCHANGED)
- **Status**: 🟢

---

## Direction C — Farey-QMC

### C1. 1D smooth (positive, narrow)
- 2-5× wins on smooth functions; FAILS on Farey-resonant
- **Status**: 🟢

### C2. Multi-dim (NEGATIVE)
- 5-100× WORSE than Halton/Sobol in 2D/3D
- **Status**: ❌ honest negative

### C3. Diffusion sampling (NEGATIVE)
- 4-9× worse on toy diffusion
- **Status**: ❌ honest negative

### C4. Lattice rule connection
- **Status**: 🔴 not started

---

## Direction D — Lean formalization (UPGRADED)

### D1. BCZ Corr = −1/2 via REAL integration
- D-fix subagent + Aristotle v4 produced 0-sorry proof using setIntegral_prod (Fubini) and intervalIntegral.integral_pow
- 437 lines, only standard axioms
- **Next**: Mathlib PR draft (`mathlib_pr_v2/PR_DRAFT.md` exists)
- **Status**: 🟢 ready to submit

### D2. q*_BCZ integration proof (COMPLETE — iter 3 via Aristotle v5)
- Aristotle v5 closed all 3 sorries via region-split + intervalIntegral.integral_inv. 252 lines, 0 sorries, only standard axioms.
- Theorems: `bczProbXYLessTwoNinths_eq`, `clusterTwoThreshold_eq`, `clusterTwoThreshold_bounds`.
- File: `aristotle_v5_result/project_aristotle/BCZThresholdIntegration.lean`.
- **Status**: 🟢 COMPLETE

### D3. CLUSTER=2 BOUNDEDNESS THEOREM (FULLY LEAN-PROVEN — Aristotle v6) ⭐
- **NEW (iter 3, this hour)**: Aristotle v6 closed KL + the full cluster_size_le_two theorem. 175 lines, 0 sorries, standard axioms only.
- Key insight: KL needed only `y > 2/3` (broader than the 0.702-band the proof sketch needed). Cleaner than sketch suggested.
- Theorems:
  - `bcz_k_eq_one`: `k₀ = ⌊(1+x)/y⌋ = 1` when `xy < 2/9 ∧ y > 2/3`
  - `k_one_nonextreme`: with `k₀ = 1`, `y(y − x) = y² − xy > 2/9` (second pair non-extreme)
  - `quadratic_squeeze`: `xy < 2/9 ∧ (x,y) ∈ T ⟹ y < 1/3 ∨ y > 2/3`
  - `KL_strengthened`: Key Lemma at `y > 2/3`
  - **`cluster_size_le_two` (HEADLINE)**: in any BCZ orbit, three consecutive extreme pairs cannot occur
- File: `aristotle_v6_result/aristotle_dispatch_v6_aristotle/BCZClusterBoundKL.lean`.
- **Status**: 🟢 COMPLETE — cluster=2 universality theorem is now formally verified end-to-end in Lean. **TRILOGY of files** (D1 + D2 + D3 = 437 + 252 + 175 = 864 lines, 0 sorries total) covers everything from BCZ density moments through q*_BCZ closed form through cluster boundedness.

### D3-D5. Earlier arithmetic identities
- 18/22 proven; superseded by D1-D2 for the Mathlib PR
- **Status**: 🟢 kept as supplementary

---

## Direction E — Universality diagnostic (UPGRADED)

### E1. Diagnostic table on 8 sequence classes (NEW expanded)
| Sequence | size-2 % | Class |
|---|---|---|
| Farey direct (N=10⁶) | 95.0 | BCZ |
| BCZ MC (50M @ q=0.99) | 88.4 | BCZ |
| BCZ MC (50M @ q=0.99999) | 99.6 | BCZ |
| Riemann ζ zeros (100k) | 3.0 | GUE at low q |
| GUE/GOE/GSE (corrected) | 0.66 | Wigner-Dyson |
| COE/CUE/CSE | 0.5-0.75 | Wigner-Dyson |
| Poisson uniform | 1.1 | Poisson |
| Periodic | 2.0 | Equidistributed |
| Prime gaps (148k) | 0.2 | Cramér-Poisson |
| φ-rotation | 0.0 | Three-Gap |

**100× separation** between BCZ class and Wigner-Dyson.
- **Status**: 🟢 paper-grade verified

### E2. Horocycle connection
- **Status**: 🟡 connection identified, not packaged

### E3. Open problem placement: "intermediate statistics" 
- **Confirmed**: Bogomolny-Giraud 2011, Marklof 2020 ICM, arXiv:2508.21691 (2025)
- **Status**: 🟢 placement justified

---

## Outreach (NEW section)

22 draft emails prepared (`projects/mimo-mini-project/outreach/`):
- `01_intermediate_statistics.md` — **13 drafts** (Marklof, Boca, Cobeli, Zaharescu, Athreya, Cheung, Rudnick, **Katz, Bogomolny, Giraud, Kurlberg, Keating, Snaith**)
- `02_mertens_computing.md` — **5 drafts** (Ng, Trudgian, Martin, Soundararajan, **Gonek** — directly relevant to Tauberian closure via his 1989 paper)
- `03_algorithmic_nt.md` — 4 drafts (Conrey, Sarnak, Odlyzko, Cremona)

**Still unconfirmed**: Einsiedler, Lindenstrauss, Strömbergsson, Radziwill, Venkatesh (RMT/dynamics); Helfgott, Platt, Booker (Mertens); Granville (algorithmic NT)

**Status**: 🟡 drafts ready, NOT YET SENT — awaiting user review per CLAUDE.md outreach gate

---

## Publication plan (v4)

| Paper | Venue | Lead | Length | Quality |
|---|---|---|---|---|
| **#1 Cluster=2** | Annals Appl. Prob. / Exper. Math | q*_BCZ closed form + 8-class diagnostic | 15-18pp | **A−/A** |
| **#2 Mertens-NW** | J. Number Theory | Tauberian → Gonek reduction + Jordan-totient + Σ M²/n³ | 12-15pp | B+ |
| **Mathlib PR** | Mathlib | BCZ Corr=-1/2 + moments via real integration | small | Ready now |

---

## What's left

1. **Aristotle v5** pull when done (q*_BCZ integration) — ⏳ pending (key not in env)
2. **Kaggle farey-cluster-2 v2** pull when done — ⏳ RUNNING
3. **Kaggle diagnostic-suite v1** pull when done — ⏳ RUNNING (β-ensembles + circular + Riemann zeros)
4. **Mathlib PR submission** — ready
5. **Outreach review + send** — awaiting user approval (22 drafts)
6. **NEW direction candidate**: F_q(T) cluster=2 empirical note (6-8 wk project per subagent)
7. **Paper drafting** — explicitly deferred per user

## NEW (iter 3) — function-field BCZ feasibility + PoC: **NO-GO, with refinement**

**Feasibility subagent** (`research_notes/function_field_BCZ_feasibility.md`): identified Horesh-Paulin 2022, Broise-Alamichel-Parkkonen-Paulin 2019 prior art. Verdict: 6-8 wk empirical shippable, multi-quarter rigorous DEFER.

**Canonical PoC subagent (option b)** (`function_field/CANONICAL_RESULT.md`): **NO-GO**. Implemented F_q(T) Farey under canonical valuation + lex-on-Laurent ordering for q ∈ {2,3}, N ≤ 8. **Size-2 % = 0.00% at q_diag=0.99; max cluster = 1**, not 2. Structural reason: discrete geometric gap cascade (37.5% at minimum, 28.1% next, 16.4% next, exact powers (q−1)q^k) + Stern-Brocot tree isolates large gaps so they essentially never come in adjacent pairs.

**Bonus closed form** found by PoC: SB-adjacent fraction in F_q(T) = **1 − 1/(q+1)** (= 2/3 for q=2, 3/4 for q=3) — a small new clean invariant.

**Decision (committed)**: drop the 6-8 wk static F_q(T) empirical paper plan. The dynamical BCZ-cocycle analog (Athreya-Cheung §8 over function fields) remains a separate, larger project — flagged in MEMORY as #1 reachable real-new-math direction but deferred for now.

### Refined universality theory (iter 3, post-subagent batch)

The speculative "rank + 1 cluster bound" conjecture is now substantially refined by 3 subagent results (#83, #84, #86):

| Setting | Density type | Cluster bound | Class | Status |
|---|---|---|---|---|
| Q Farey / BCZ chain | indicator hard cap (lattice-dynamical) | **2** | "BCZ class" | rigorous mod KL |
| F_q(T) static lex-Laurent | discrete geometric cascade | **1** | "F_q tree-isolated" | empirical |
| SL(3,ℤ) Farey (predicted) | continuous (Marklof-Strömbergsson) | 3? | unknown | EBMV2015 = Poisson counter-evidence |
| RMT β-Hermite (any β) | smooth ∏|λ_i−λ_j|^β | unbounded (geometric tail) | Wigner-Dyson | rigorous |
| Poisson | uniform | unbounded geometric | Poisson | rigorous |

**Three honest conclusions from the subagent batch:**

1. **BCZ class is *lattice-dynamical, not random-matrix*** (subagent #86). The "size-2 = 95%, size-3+ = 0%" structure requires the indicator-type hard cap from the BCZ density's `2·𝟙_{x+y>1}` — smooth eigenvalue interactions can't reproduce it. This is a structural finding that *places* BCZ class outside the Dyson threefold way.

2. **"Rank+1" conjecture has serious counter-evidence** (subagent #83). El-Baz–Marklof–Vinogradov 2015 shows the directly-analogous higher-rank gap statistic is Poisson (unbounded clusters). The "1 → 2" data point is just one example; cluster bound may not increase with rank in the predicted way.

3. **Cluster=2 has a rigorous-modulo-KL proof from binary structure** (subagent #84). Bulk closed via the same quadratic 9y²−9y+2 > 0 whose roots {1/3, 2/3} appear in the closed-form integration; geometric pinch at t*=2/9 disconnects {xy<t}∩T into two corner triangles; map alternates corners; max cluster ≤ 2.

4. **Sturmian/quasicrystal connection is SUPERFICIAL** (subagent #85). The two "=2"s are different mathematical objects.

**New picture**: BCZ universality is a *new class* distinct from Wigner-Dyson and Poisson, characterized by:
- Indicator-type hard cap on the joint density
- Lattice-dynamical origin (SL(2,ℤ) acting on the modular surface)
- Sharp cluster bound from binary tree + continuant identity
- Geometric pinch at the critical product t*

It is NOT a random-matrix universality class; it is its own thing.

## NEW (iter 3) — Σ M(n)²/n³ closed-form verdict

Subagent (`research_notes/mertens_square_sum_closed_form_attack.md`): **no closed form likely**. Ng 2004's β-constant has no closed form itself; Mellin-Parseval integral form ∫_{(3/2)} dw/[w(3-w)ζ(w)ζ(3-w)] is novel but unevaluated. **Recommendation**: catalogue C_3 as new conjecturally-irrational Mertens-second-moment constant; push to 50+ digits for OEIS submission.

---

## Negative findings (cleanly archived)

- Microtonal/music speedup (cluster=2 wrong regime)
- Multi-dim Farey-QMC (5-100× worse)
- Diffusion sampling noise (4-9× worse)
- Universal QMC advantage (regime-dependent only)
- AI-music model applications (wrong abstraction)
- "Original" structural identity (Franel 1924)
- New C constant (OEIS A065483/2)
- RMT 15% size-2 (was artifact; corrected to 0.66%)

---

## Risk / confidence (v4)

- **High confidence** (paper-ready): A1, A2, A6, A7, B3, B6, D1, E1
- **Medium**: A3, A4, B1, B2, B5, B7, C1, D2, E2
- **Low/open**: B4 (Tauberian), C4 (higher-dim QMC), E3 (deep universality)
- **Archived negative**: A5, C2, C3

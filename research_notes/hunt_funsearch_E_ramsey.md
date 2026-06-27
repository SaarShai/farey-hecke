# FunSearch/AlphaEvolve target hunt — Domain E: extremal graph/hypergraph & Ramsey/Turán

Date 2026-06-27. Agent: domain-E survey (construction-side lower bounds; AVOID SAT turf).
Mandate: find a beatable, exactly-verifiable, NON-OWNED construction-side record a SAMPLE-LIMITED
LLM-proposal + exact-verification fleet (dozens-to-hundreds of structured proposals, NOT a
million-eval DeepMind loop, NOT raw FLOPS) could realistically contribute to in weeks.

Write ONLY this file. No git. Hooks don't fire in subagents — honesty is self-enforced.
KNOWN = published+sourced. CLAIMED = asserted, not yet source-verified. UNVERIFIED = could not confirm.

---

## 0. THE OWNERSHIP MAP (must internalize before picking) — this domain is HOTLY contested

The LLM-evolutionary construction paradigm is **already deployed inside my exact domain**. This is
the single most important fact. What is OWNED / swept as of mid-2026:

- **AlphaEvolve / RGCS** — "Reinforced Generation of Combinatorial Structures: Ramsey Numbers",
  Nagda, Raghavan, Thakurta, **arXiv 2603.09172 (Mar 2026)**. Improved **2-color OFF-DIAGONAL clique**
  Ramsey lower bounds: R(3,13) 60→61, R(3,18) 99→100, R(4,13) 138→139, R(4,14) 147→148,
  R(4,15) 158→159. Method = LLM code-mutation evolving search heuristics. **KNOWN.**
  → Explicitly did NOT touch: multicolor, hypergraph, cycle/book Ramsey, diagonal beyond matched.
- **OpenEvolve / Zarankiewicz** — "New Bounds for Zarankiewicz Numbers via Reinforced LLM
  Evolutionary Search", **arXiv 2605.01120 (May 2026)**. Resolved exact z(11,21;3,3)=116,
  z(11,22;3,3)=121, z(12,22;3,3)=132 + 41 improved lower bounds, m≤16, n≤23. ~$15-30/case.
  **KNOWN.** → Did ONLY s=t=3. Did NOT touch s=t=2, other s,t, or larger ranges.
- **SAT solvers (Heule/Kissat crowd; William Wesley)** own the small-clique / book / design end:
  R(3,3,4)=30 (Codish et al. 2016); R(4,4,4)/R(3,4,5)/R(3,3,6) upper bounds via SAT+modular
  (arXiv 2603.10851, Mar 2026); book Ramsey R(B_m,B_n) via SAT+IP+block-circulant
  (Wesley, arXiv 2410.03625, 2024); new small-multicolor via Kissat+Cayley (Wesley, arXiv
  2509.03784, Sep 2025). **KNOWN.**
- **Radziszowski "Small Ramsey Numbers" dynamic survey (DS1)** — rev #18, **Jan 2026**, 148pp,
  cumulative-knowledge table. Anything in the headline 2-color and small-multicolor tables is
  cultivated. **KNOWN.**

Net: the famous 2-color and small-clique records are SWEPT or SAT-owned. The surviving long tail =
**MULTICOLOR and CYCLE Ramsey, where the lower bound is an OLD explicit ALGEBRAIC construction with
a real gap, and neither AlphaEvolve (2-color only) nor OpenEvolve (z;3,3 only) nor the SAT crowd
(cliques/books) has touched it.**

---

## 1. CANDIDATES (construction-side lower bounds; ranked below in §3)

### Candidate E1 — Multicolor Ramsey for the quadrilateral, **r_k(C_4)**, small open k  ★ TOP PICK
- **Statement.** r_k(C_4) = least n such that every k-edge-coloring of K_n has a monochromatic C_4.
  Equivalently a lower bound r_k(C_4) ≥ n+1 ⟺ K_n decomposes into k **C_4-free** graphs.
- **Current best (KNOWN).**
  - r_2 = 6, r_3 = **11** (exact; Bialostocki–Schönheim), r_4 = **18** (exact; Sun–Yang–Lin–Zheng 2007).
  - **r_5(C_4): 27 ≤ r_5 ≤ 29 — OPEN, gap 2.** (Lazebnik–Woldar lower; upper improved below naive 31.)
  - General LB r_k(C_4) ≥ k²+2 (k prime power) / ≥ k²−k+2 (k−1 prime power), Lazebnik–Woldar 2000,
    via **polarity graphs of finite geometries** (the C_4-free Erdős–Rényi / generalized-quadrangle
    graphs). General UB k²+k+1 (Chung 1974; Irving 1974), improved to **k²+k−1 for even k≥6**.
  - So: r_6 ∈ [32, 41], r_7 ∈ [44, 57] (k=7 LB 7²−7+2=44; UB 7²+7+1=57) — OPEN, wide-ish gaps. (LB
    values CLAIMED from the formulas; exact small-k entries to re-confirm against survey rev #18.)
- **Source / who-when.** Lazebnik & Woldar, "New Lower Bounds on the Multicolor Ramsey Numbers
  r_k(C_4)", J. Combin. Theory A (2000). Upper-bound side: Chung 1974 / Irving 1974, even-k
  improvement in Acta Math. Appl. Sin. 2023 (s10255-023-1074-3). **KNOWN.**
- **Why sample-limited-friendly.** The record is a **structured algebraic decomposition**, not a
  blob: a lower bound = "partition E(K_n) into k C_4-free color classes." Each class is a C_4-free
  graph (≤ ½(1+√(4n−3))·n edges, the Kővári–Sós–Turán / friendship-theorem ceiling), and the good
  constructions are GEOMETRIC (polarity graphs, affine/projective parallel classes, Cayley graphs
  over Z_p). The search is over **"which group + which geometry + which connection sets"** — a tiny,
  reasoning-shaped space where a clever proposal beats FLOPS. This is the FunSearch regime exactly.
- **Concrete verifiable contribution.** A single explicit 5-coloring of K_27 (or K_28) with no
  monochromatic C_4 ⇒ r_5(C_4) ≥ 28 (or 29), closing/improving a 25-year-old open case. Any such
  witness is a 27×27 (resp. 28×28) symmetric matrix over {1..5}; checking "no monochromatic C_4" is
  O(n^4) trivial — anyone can verify. Same for r_6 (K_32..K_40), r_7.
- **Novelty / owned status (brutal).** NOT in AlphaEvolve/RGCS (2-color clique only). NOT in
  OpenEvolve (z;3,3 only). NOT a SAT-owned case (Wesley's multicolor SAT work hit cliques and
  C_4-vs-cliques, NOT the diagonal r_k(C_4) decomposition). The lower bound is 25 yrs old and
  algebraic. **This is the cleanest "neglected, structured, finite-witness, real-gap" target found.**

### Candidate E2 — Multicolor Ramsey for **K_{2,t+1}** (generalized-book / theta), **r_k(K_{2,t+1})**
- **Statement.** r_k(K_{2,t+1}) = least n s.t. every k-coloring of K_n has a monochromatic K_{2,t+1}
  (t=1 is exactly C_4 → K_{2,2}, so E2 ⊃ E1's mechanism, t≥2 is fresher and looser).
- **Current best (KNOWN/recent).** "A new lower bound for the multicolor Ramsey number r_k(K_{2,t+1})",
  **arXiv 2411.14364 (Nov 2024)**: new infinite family of K_{2,t+1}-free graphs (prime power t),
  E(K_n) partitioned into K_{2,t+1}-free parts ⇒ improved LB when k, t are powers of the same prime.
  Construction-side, very recent, bounds NOT tight.
- **Why sample-limited-friendly.** Same decomposition mechanism as E1 but a 2-parameter family
  (k AND t) with LOTS of small open cells and looser-than-C_4 bounds (less cultivated). Each color
  class = an algebraic K_{2,t+1}-free graph; propose + exact-verify.
- **Contribution.** Improve a specific small (k,t) lower bound with an explicit verifiable k-coloring,
  e.g. r_3(K_{2,3}), r_4(K_{2,3}). Witness = colored adjacency matrix; check is polynomial.
- **Owned status.** Construction-side, Nov-2024, NOT touched by AlphaEvolve/OpenEvolve/SAT.
  Younger and broader than E1 but slightly less "famous-number" significance per case.

### Candidate E3 — Multicolor Ramsey for even cycles, **R_k(C_{2m})** / three-color cycle cases
- **Statement.** R_k(C_{2m}) and small 3-color R(C_i,C_j,C_k); lower bounds from circulant colorings.
- **Current best (KNOWN).** R_3(C_{2m}) ≥ 4m (general LB). Dzido, Nowik, Szuca, "New lower bound for
  multicolor Ramsey numbers for even cycles", Electron. J. Combin. v12n13 (2005) — circulant
  constructions, **~20 yrs old**. Several small 3-color cycle numbers resolved very recently by SAT
  (Wesley 2509.03784: R(C_3,C_6,C_6)=15, R(C_5,C_6,C_6)=15), but the LONGER-cycle / more-color cells
  remain open and circulant-driven.
- **Why sample-limited-friendly.** Circulant = single connection-set over Z_n per color → tiny,
  highly structured proposal space; LLM can reason about residue/difference patterns.
- **Contribution.** A new circulant k-coloring beating a Dzido-era LB for a specific small R_k(C_{2m}).
- **Owned status.** Construction LBs 20 yrs old, untouched by AlphaEvolve/OpenEvolve. CAVEAT: the
  SMALL cycle cells are being actively eaten by Wesley's SAT (verification side), so target
  longer-cycle / higher-color cells SAT hasn't reached, where the circulant idea still rules.

### Candidate E4 — Diagonal multicolor triangle Ramsey, **R_4(3)=R(3,3,3,3)**, **R_5(3)**
- **Statement.** R_k(3) = least n s.t. every k-coloring of K_n has a monochromatic triangle.
- **Current best (KNOWN, but re-confirm exact LB values vs survey #18).** R_4(3)=51 (exact), so the
  open small diagonal triangle case is **R_5(3): LB ≥ 162 (Exoo 1990s, Schur-like/block construction)
  ≤ 307 — gap ~145.** Asymptotic LB lim R_r(3)^{1/r} > 3.273 (Schur-product constructions).
- **Why sample-limited-friendly — WEAKLY.** The LB is OLD (Exoo) and algebraic, and untouched by
  AlphaEvolve/OpenEvolve. BUT K_162 with 5 colors is huge; a finite witness improvement is hard, and
  the strong results here are PRODUCT/Schur-set constructions (more theory than small-witness). The
  Schur-number connection (s(5)≥160) overlaps heavily with the SAT-owned Schur-number frontier.
- **Contribution.** Improve R_5(3) LB by 1+ via a new finite 5-coloring (very hard) OR a better Schur
  partition (collides with SAT). Significance high, tractability LOW.
- **Owned status.** Not LLM-swept, but the realistic attack surface is small (FLOPS-bound finite
  witness + SAT-adjacent Schur side). Backup, not lead.

### Candidate E5 (REJECTED) — Book Ramsey R(B_m,B_n); 2-color off-diagonal cliques; z(m,n;3,3)
- **Book R(B_m,B_n):** SAT+IP+block-circulant, Wesley 2410.03625 (2024). **SAT-OWNED. DEAD.**
- **2-color off-diagonal R(3,k)/R(4,k):** AlphaEvolve/RGCS just swept (Mar 2026). **OWNED. DEAD.**
- **z(m,n;3,3):** OpenEvolve just swept (May 2026). **OWNED. DEAD.** (z(m,n;2,2) is projective-plane
  /design-owned classically; small open cells exist but it's a different—coding/geometry—flavor and
  better fits Domain D.)

---

## 2. ADVERSARIAL VERIFICATION of the TOP PICK (E1, r_k(C_4)) — try to KILL it

**Kill-test 1 — Is it secretly owned / already beaten?**
- AlphaEvolve/RGCS abstract + scope: 2-color off-diagonal cliques ONLY. r_k(C_4) NOT present. ✔ survives.
- OpenEvolve: z(m,n;3,3) ONLY. NOT present. ✔ survives.
- Wesley SAT multicolor (2509.03784): improved R(K_4,K_4−e,K_4−e), R(K_3,K_4,C_4,C_4), some 3-color
  cycle exacts — NOT the diagonal r_k(C_4). ✔ survives.
- Risk: the field is OPEN-SOURCE now (OpenEvolve, CodeEvolve arXiv 2510.14150). Someone COULD point an
  evolutionary loop at r_k(C_4) tomorrow. It is unclaimed TODAY but not protected. **Live, time-boxed.**

**Kill-test 2 — Is it secretly FLOPS-bound (the real danger)?**
- A naive coloring search of K_27 with 5 colors = 5^{351} — astronomically FLOPS-bound. A blind /
  random / pure-eval evolutionary loop on raw colorings would NOT find a record in our budget.
- **This is the crux, and the honest answer is conditional:** E1 is sample-limited-friendly ONLY in
  the **STRUCTURED ALGEBRAIC regime** — propose geometry/group-based decompositions (polarity-graph
  variants, affine-plane parallel classes, Cayley graphs over Z_p / small nonabelian groups, blow-ups
  of the r_4 and r_3 extremal colorings), where each proposal is one structured object and the
  proposal space is dozens-to-hundreds, not 5^{351}. A fleet of REASONING agents proposing
  "take GQ(q), polarity π, split the lines into k C_4-free classes by …" is exactly where structure
  beats FLOPS. As a blind numeric search it FAILS the FLOPS filter; as a structured-proposal search
  it PASSES. **Must commit to the structured framing.** ✔ survives, conditionally.

**Kill-test 3 — Is it actually open with room?**
- r_5(C_4) ∈ [27,29], exact value OPEN (KNOWN). r_6, r_7 OPEN with wider gaps. r_3, r_4 are exact
  (closed — do NOT target those). So yes, real open small cells exist. ✔ survives.
- Honest caveat: r_5's gap is only 2, and the LB 27 = q²+2 may be the truth (upper-bound side, not
  lower, may be what's loose). Improving the LOWER bound 27→28 needs a 5-coloring of K_27 that the
  polarity construction doesn't give — genuinely uncertain it exists. Safer EV: target r_6/r_7 where
  gaps are bigger, OR the E2 K_{2,t+1} family where bounds are looser and newer.

**Kill-test 4 — Independently verifiable?**
- A witness is a symmetric n×n matrix over {1..k}; "no monochromatic C_4" is checked in O(n^4) by
  any third party (count common neighbors within each color). Fully, trivially, independently
  verifiable. ✔ survives — strongest property.

**Verdict of adversarial pass:** E1 survives all four tests but with one binding caveat (Kill-test 2):
it is a real target **only as a structured algebraic-proposal search**, not a blind eval loop, and
the surest EV is the looser cells (r_6, r_7, or the E2 K_{2,t+1} generalization) rather than the
tight r_5 gap. It is unclaimed today but the paradigm is open-source, so it is time-sensitive.

---

## 3. RANKING (realistic-shot × not-owned × exactly-verifiable × significance)

1. **E1 — r_k(C_4) small open k (lead on r_6/r_7; r_5 as the famous narrow case).** Best balance:
   structured/algebraic (sample-limited-friendly), finite + trivially verifiable, genuinely
   unclaimed by AlphaEvolve/OpenEvolve/SAT, classical named numbers (real significance). Caveat:
   only friendly in the structured regime; tight r_5 gap is risky, looser cells safer.
2. **E2 — r_k(K_{2,t+1}) small (k,t).** Same mechanism, broader + younger + looser bounds = more open
   cells and more EV, slightly less per-case fame. Strong, possibly the better *first* pilot.
3. **E3 — circulant R_k(C_{2m}) / longer-cycle multicolor.** Tiny structured proposal space
   (single connection set/color), but SAT is actively eating the small cells — aim long-cycle/high-color.
4. **E4 — R_5(3) diagonal triangle.** High significance, low tractability (huge witness, Schur/SAT
   adjacency). Backup only.
5. **E5 — REJECTED** (book/2-color-clique/z;3,3 all freshly OWNED by SAT or DeepMind).

**Pilot recommendation.** Run the structured-proposal fleet on the **E1∪E2 decomposition problem**:
proposer agents emit explicit algebraic k-colorings (polarity-graph / affine-plane / Cayley
decompositions of K_n into C_4-free or K_{2,t+1}-free classes) as adjacency-matrix code; an exact
O(n^4) evaluator certifies "no monochromatic forbidden subgraph"; keep/mutate the structured seed
(group, geometry, connection set); independently re-verify any record. Start at looser cells
(r_6(C_4), r_7(C_4), r_3(K_{2,3})) to validate the pipeline, then push the famous tight one r_5(C_4).

---

## 4. Confidence / data-quality notes (honesty ledger)
- Survey PDFs (Radziszowski DS1, paper61, the 2402.16816 quadrilateral paper) are FlateDecode-
  compressed → NOT text-extractable via fetch. Numbers here come from the HTML version, secondary
  arXiv/journal sources, and abstracts. The headline gap **r_5(C_4) ∈ [27,29]** is corroborated by
  TWO independent sources (the 2402.16816 HTML fetch and the Lazebnik–Woldar search). Exact small-k
  table entries (r_4=18 Sun–Yang–Lin–Zheng 2007; r_3=11 Bialostocki–Schönheim) are KNOWN.
- The formula-derived LB/UB for r_6, r_7 (and R_4(3)=51, R_5(3)≥162) are CLAIMED-from-formula /
  secondary-sourced — RE-CONFIRM against Radziszowski rev #18 (cs.rit.edu/~spr) before any pilot
  commits to a specific cell, since the exact small-k entry can differ from the asymptotic formula.
- AlphaEvolve/OpenEvolve/Wesley scope exclusions (no multicolor cycle, no r_k(C_4)) verified from
  paper abstracts/scope statements — KNOWN, but "absence" is harder to prove than "presence";
  a fresh arXiv listing check is cheap insurance before launch.

---

## READY FOR JUDGING
**REAL target: YES — E1, the multicolor quadrilateral Ramsey number r_k(C_4) (lead small open cells
r_6/r_7, plus the famous tight r_5(C_4) ∈ [27,29]), with the K_{2,t+1} generalization (E2) as the
broader/looser sibling.** Realistic contribution: an explicit, independently O(n^4)-verifiable
algebraic k-coloring (polarity-graph / affine-plane / Cayley decomposition of K_n into C_4-free
classes) that raises a stale (25-yr-old, Lazebnik–Woldar) lower bound by ≥1 on a specific small open
cell. It is finite, trivially checkable, genuinely UNCLAIMED by AlphaEvolve (2-color cliques only),
OpenEvolve (z;3,3 only), and the SAT/Wesley crowd (cliques/books) — but ONLY beatable as a
STRUCTURED algebraic-proposal search (blind eval is FLOPS-bound), and the window is open-source-and-
time-sensitive. Safest EV is the looser cells / the K_{2,t+1} family; the headline prize is r_5(C_4).

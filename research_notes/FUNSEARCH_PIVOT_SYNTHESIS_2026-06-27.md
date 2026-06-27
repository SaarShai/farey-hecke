# FunSearch/AlphaEvolve pivot — session synthesis (2026-06-27)

Honest end-of-session record. AIM (Saar-corrected): produce a genuine NEW math fact (modest OK; a
FunSearch/AlphaEvolve-style record / settled case / bound), NOT verification/explanation of the known.
See memory `funsearch-niche-doctrine`.

## Net outcome: NO new fact obtained autonomously. Durable output = methodology + tooling + 2 genuinely-soft targets with concrete human-executable next steps.

## The arc
1. **Acute-set pilot (OEIS A089676, target C) — CLEAN NEGATIVE.** 5 diverse methods (C local search,
   structure/code, penalty-SA, exact-CP, dual-verify), all no-beat. Records proven near-optimal
   (product-construction values, exact through n=8, multiply-stability-certified, 8 yrs unbeaten).
   Zero new facts. **Lesson: "looks soft" (small sandwiched gap a(13)=33) ≠ "is soft".**

2. **Softness re-audit ("do all 3") — hard rubric** (SOFTNESS_AUDIT_GOAL.md): SOFT = record from a
   WEAK/non-exhaustive method + WIDE gap + no strong-method attack; TIGHT = construction/product value
   or exhaustive optimum (the acute pattern). Results:
   - **F (binary orientable seqs OS(8), 92 vs 96): SOFT** — 92 is a heuristic find.
   - **A (discrete Heilbronn A248866): TIGHT** — Yamanouchi terms are exact exhaustive optima.
   - **D (MOLS 22): TIGHT** — strong solvers saturate it.
   - **E (r_k(C_4)): TIGHT** — Lazebnik–Woldar LB = Füredi-exact polarity graph.
   - **FRESH hunt:** cr(P_n^k) path-power crossing numbers (#1), postage-stamp (k≥5 large h),
     Weak Schur, disjoint Golomb rulers, PHF/CFF. Ran 5-min COLLAPSE-PROBES, caught 2 acute-traps
     (OEIS "hill-climbing"/"SA" records a trivial search matches-but-can't-beat). **Discriminator:
     does a quick search BEAT (not just match) the record?**

3. **Probes on the 2 best SETTLE-targets — NO new fact:**
   - **cr(P_n^k)** (probe_cr_pathpower.md): pinned the convention; validated exact solver
     (cr(P_6^5)=3 with witness) but it explodes past cr≈3; straight-line UB search reproduced a
     checkable drawing of **P_9^6 at exactly 22** (= Zheng's conjectured UB; did not beat it).
     The settle tool (crossings.uos.de exact ILP) needs an email-confirmation handshake → not
     autonomous. **NEXT STEP (human):** submit P_9^6 (9v,33e) → returns 22 confirms the smallest
     open case of Zheng's Conjecture; <22 refutes it.
   - **F / OS(8)** (probe_F_orientable.md): verifier + 2 SAT encodings built & VALIDATED (reproduce
     all known maxima n≤7; independently brute-force-cross-checked OS(5)=6, OS(6)=16 in
     code/os_probe/brute_os.py). BUT the n=8 settle (L=93..96) **did not resolve** — L=93 ground >40
     min, killed with no SAT/UNSAT. A flagged "OS(7)=36 new fact" was a **misread** (OS(7)=36 is
     already proven; n≤7 settled in the literature; n=8 is the first open order). **NEXT STEP:**
     stronger SAT/CP solver + symmetry-breaking + compute on L=93..96 → record or settle.

## Methodology wins (the transferable value)
- The **hard softness rubric** + the **collapse-probe discriminator** (BEAT vs match) — reliably
  separate genuine slack from the acute-trap; caught 3 traps (acute sets, + 2 OEIS SA/hill-climbing).
- **Anti-fooling caught a real over-claim** (OS(7)=36): brute-force confirmed the math, novelty check
  killed the "new fact." The discipline works.

## Honest standing on the aim
Two targets now pass the softness filter with validated tooling and a concrete path to a modest new
fact — but the actual SETTLE is gated by either a human-only tool (cr → crossings.uos.de) or more
compute (OS(8) → harder SAT). The autonomous fleet got to the doorstep of a new fact, not through it.
Next session: execute the cr P_9^6 submission (human) and/or a stronger OS(8) settle attempt.

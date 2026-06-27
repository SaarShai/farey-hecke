# Softness audit — Target A: Discrete Heilbronn triangle on the n×n lattice (OEIS A248866)

**Date:** 2026-06-27 · **Auditor:** subagent (FunSearch-mode softness rubric) · **Status: READY FOR JUDGING**

## VERDICT: **TIGHT** (confidence ~80%)

Same failure mode as the A089676 acute-set negative, with one twist. The neglect axis (S4) is
genuinely strong — the discrete lattice variant is unattacked since 2015 while all 2024–2026 effort
goes to the *continuous* problem. But the decisive axes fail: the known terms a(3..13) are **provably
optimal by exhaustive search** (I independently re-proved a(5..10) as true maxima — see below), so the
record method is NOT weak (S1 fails) and there is NO gap to exploit on the known terms (S2/S3 fail). The
only "soft-looking" deliverables — extend to an exact a(14), or refute the {5,6} conjecture — both require
either an upper-bound / optimality proof (the survey's flagged weak axis) or a lower-bound construction
that nobody has shown is even *reachable*. A FunSearch fleet's natural output is a lower-bound config, and
the data says a config beating the ceiling almost certainly **does not exist** (a(7)=a(9)=5, ceiling sits
at 6). **A construction that can't beat 6 is not a new fact.** This is acute-sets again: record = exact
proven optimum, nearby sizes proven optimal, narrow integer band → TIGHT.

---

## The object (all facts KNOWN, verified from OEIS text dump + independent computation)

- **Definition (KNOWN, %N line):** a(n) = twice the maximal area of the smallest triangle defined by three
  of n points placed on an n×n integer lattice. Offset 3.
- **Data (KNOWN, verified):** a(3..13) = `4, 9, 6, 6, 5, 6, 5, 6, 6, 6, 6`. Keyword `nonn,more`
  (NOT `hard`; `more` = more terms wanted). NO %F formula line, NO upper-bound reference in the entry.
- **Conjecture (KNOWN, %C line, verbatim):** *"It is conjectured that the sequence has an infinite
  repetition of only two integers."* Read against the data, this is the {5,6} claim for the tail n≥5
  (a(4)=9 is the small-n outlier: 4 points, corners of the grid, 2·area = (n−1)² = 9).
- **History (KNOWN, OEIS edit log + discussion):** posed by Gordon Hamilton (MathPickle "Unsolved K-12",
  Grade 8) Mar 04 2015. **a(5), a(7), a(9) corrected and a(10)–a(13) added by Hiroaki Yamanouchi Mar 09
  2015.** a(13) is the last term; **a(14) has never been published or, per the record, attempted.**

### Independent verification I ran (exact, load-bearing)
1. **Data terms (lower bound side):** parsed all 11 Yamanouchi ASCII configs from `a248866.txt`; every one is
   a valid n×n grid with exactly n points, no collinear triple, and 2·min-area **exactly equal** to the OEIS
   value. 11/11 match. (Confirms the published values are *achievable*.)
2. **Optimality (upper bound side) — the decisive check:** wrote an exhaustive branch-and-bound that finds
   the TRUE maximum 2·min-area over ALL ⊂ n×n configs. Results:
   - a(5)=**6**, a(6)=**6**, a(7)=**5**, a(8)=**6**, a(9)=**5**, a(10)=**6** — **all exhaustively proven
     optimal, all match OEIS.** (n=9 took 60 s, n=10 took 200 s with naive code.)
   - This independently confirms Yamanouchi's terms are *exact proven optima*, not heuristic lower bounds.

---

## S-criteria

### S1 — weak record method? **NO (record is exhaustive / proven-optimal).** ✗ for softness
- Yamanouchi's primary-source note on the sequence (OEIS discussion, verbatim): *"@Gordon Hamilton, I could
  not find a pattern such that a(7)=6 or a(9)=6."* — i.e. his corrections came from a search that
  **exhaustively failed to beat** the value, which is exactly what proves optimality. Collaborators (Arndt:
  "good work!") treated it as definitive. He has no published method paper, but his OEIS role is precisely
  extending `more`/`hard` sequences with exact computation.
- **I reproduced the optimality** for n≤10 (true maxima), and a(7)=a(9)=5 — proving 6 is *unreachable*
  there — confirms the corrections are exact. The method is exact exhaustive search (with pruning/symmetry),
  not a one-off heuristic. **This is the acute-set TIGHT signature: record = proven optimum.**

### S2 — wide gap? **NO on known terms; "gap" only at the unattempted a(14).** ✗ for softness
- Known terms have **zero** gap: lower bound = upper bound = published value (proven). There is no
  best-upper-bound vs best-config slack to close.
- The only open quantity is a(14) (and the asymptotic {5,6} conjecture). There is no published upper bound
  for a(14) at all — but that's "no effort," not "wide gap," and the value is morally forced into {5,6} by
  the flat tail a(8..13) = 5,6,5,6,6,6,6 (never exceeds 6).

### S3 — TIGHT red flags? **YES, several.** ✗ for softness (this is the kill shot)
- **Nearby sizes proven optimal:** a(3..13) are exact; I re-proved a(5..10) from scratch. Same as acute
  sets (exact through n=8). 
- **Record is the true optimum,** not a closed-form/product value but worse — it's a *certified maximum*,
  the strongest possible "tight" flag.
- **Deliverable needs an upper-bound argument** (the survey's own flagged weak axis): an exact a(14) requires
  proving no config beats it (C(196,14) ≈ **8.8×10²⁰** — note the goal's "≈1e18" undercounts; even
  C(169,13)≈9.2×10¹⁸ for n=13). Naive enumeration is dead; a SAT/ILP/CP solver is the only route, and
  **there is no moat vs CP/SAT** here — it's a finite-domain feasibility problem (pick n cells, all triples
  ≥ T) that off-the-shelf solvers eat. Whoever points a solver at it gets a(14) first; no special insight.
- **Density regime kills value growth:** #points = grid-side = n, so point density is ~1/n (n points in n²
  cells) — a *fixed sparse density*, not fixed-k. That is the structural reason the min-area ceiling stays
  pinned at {5,6} and the conjecture is plausibly TRUE. Beating 6 means making *all* C(n,3) triangles large
  while density is fixed — and the data (a(7)=a(9)=5) shows even reaching 6 fails at some n.

### S4 — neglected? **YES — genuinely neglected (the one real soft signal).** ✓ for softness
- **Verified:** every 2024–2026 Heilbronn attack targets the **continuous** variant, NOT the discrete
  lattice A248866. Checked and confirmed scope on each:
  - **AlphaEvolve / GigaEvo (2025):** continuous *equilateral-triangle* n=11 (0.0365). Discrete: not touched.
  - **MIP / MINLP, arXiv:2603.11107 (2026):** continuous unit square; certified optimal only n≤9 (n=9 in
    ~15 min–1 day). Explicitly no lattice/grid/integer-coordinate variant, no A248866.
  - **Global optimization, arXiv:2512.14505 (Dec 2025):** continuous unit square; certified to n≤9, n=10
    uncertified. No discrete variant.
  - **Concept-tree search, arXiv:2602.03132 (Feb 2026):** continuous. No discrete variant.
  - **Cohen–Pohoata–Zakharov (2023), higher-dim Zakharov (2024):** asymptotic *upper bounds* for the
    continuous problem; irrelevant to small-n discrete exact values.
- No SAT/ILP/AlphaEvolve/FunSearch/specialist push on A248866 since Yamanouchi 2015. **This axis is real.**

### S5 — still a NEW fact if beaten? **Partially — but the attainable version is weak/likely-empty.** ~½
Two candidate new facts; both unowned NOW (verified), exactly verifiable, but neither is a safe FunSearch win:
1. **Exact a(14) (extended term).** New + exactly verifiable IF certified optimal — but certification needs
   an upper-bound/exhaustive proof (S3), and the value is morally forced to 6 (so even success = "+0 over the
   ceiling, just one more confirming term"). A *lower-bound only* a(14)≥6 config that doesn't prove
   optimality is **not** a new fact (it ties the obvious construction; cf. the lesson "a config that doesn't
   beat anything isn't new").
2. **Refute {5,6}:** find any n with a(n) ≥ 7 (pure construction, no upper bound needed — the FunSearch-ideal
   shape). **But the evidence says 7 is unreachable:** I exhaustively proved 7 INFEASIBLE for n=7,8; for
   n≥9 a naive feasibility search times out (8 s budget) — inconclusive but *not* a found config. The flat
   tail and the fixed-density argument both predict the conjecture is TRUE → a refuting construction probably
   **does not exist**, so a fleet would burn out finding nothing (acute-sets outcome).

---

## What EXACTLY would count as a NEW fact (precise)
- **Best case (real but hard):** a *certified-optimal* a(14) (or a(14)+a(15)) — requires a solver run that
  proves the maximum, i.e. an exhaustive/SAT/ILP optimality certificate, not a config. Owned by whoever runs
  a competent CP/SAT campaign; no insight moat.
- **Glamorous case (almost certainly empty):** a config with 2·min-area ≥ 7 for some n, refuting the
  {5,6} conjecture. Exactly verifiable, unowned — but the data predicts it doesn't exist.
- **NOT new:** any a(n)≥6 lower-bound config (ties the known construction); any "explanation" of why {5,6}
  holds without a proof.

---

## SINGLE cheapest probe (<1 hr) to validate/falsify softness
**Run a real SAT/CP-SAT feasibility campaign on the two questions a naive solver can't close** — this both
(a) tests whether the FunSearch-relevant refutation is even alive, and (b) calibrates whether the moat is
absent. Concretely, with OR-Tools CP-SAT:
1. **Refutation gate (the go/no-go):** for n = 9..18, model "∃ n points on n×n grid with every triple
   2·area ≥ 7" as a CP-SAT feasibility problem (booleans x_{ij} per cell, Σ = n; for each collinear-or-small
   triple add a clause forbidding all three) and let the solver return SAT or **UNSAT** per n. If CP-SAT
   returns UNSAT across the band in minutes → the {5,6} conjecture is locally confirmed and **the only
   FunSearch-shaped deliverable is dead → TIGHT confirmed, do not fleet.** If it finds a SAT config →
   conjecture REFUTED on the spot (and you wouldn't even need a fleet — the probe already won).
2. **Optimality gate:** ask CP-SAT for the exact max T at n=11,12 (maximize-min via the same encoding). If it
   closes n=11,12 in minutes (confirming a(11)=a(12)=6 as optima), it will plausibly close a(14) too →
   confirms "no moat vs CP/SAT, off-the-shelf solver gets the term," i.e. the term is attainable but
   unprotected (whoever runs the solver first owns it).

My naive Python branch-and-bound already proved n≤10 optimal and proved 7 infeasible for n≤8 in seconds;
CP-SAT should extend both several n further within the hour. **Expected outcome (my prediction): UNSAT on
the refutation, solver closes a few more exact terms → TIGHT, niche-trap, do not commit a fleet.** Cost of
the probe is ~30–60 min and it is decisive either way.

---

## Bottom line for the synthesis loop
A248866 is **neglected (S4 ✓) but not soft.** It fails the rubric on the axes that mattered for the acute-set
post-mortem: the record is a **proven exhaustive optimum** (S1 ✗), there is **no gap** on known terms
(S2/S3 ✗), and the only construction a fleet could produce (≥7) is predicted **non-existent** by the data,
while the only solid new fact (certified a(14)) needs an **upper-bound proof with no insight moat vs CP/SAT**
(S3 ✗). This is the acute-set pattern wearing a "more"-tag: *looks* open (tiny integers, conjecture to test,
unattempted a(14)) but is near-closed. **Recommend TIGHT; do not fleet. If anything is done at all, it is the
1-hour CP-SAT probe above — and the most likely result is a clean confirmation that nothing new is reachable.**

### Honest uncertainties (kept explicit)
- I proved optimality only to n=10 myself (naive solver wall); a(11)–a(13) optimality rests on Yamanouchi's
  exact search, which his primary-source note + my n≤10 reproduction make highly credible but I did not
  re-derive. Marked KNOWN-via-Yamanouchi, not independently re-proven here.
- The {5,6} conjecture being TRUE is *inferred* (flat tail + fixed-density argument + n=7,8 infeasibility of
  7), **not proven.** The 20% residual confidence on the verdict is exactly this: if CP-SAT surprisingly
  finds a(n)≥7 at some moderate n, the target flips to SOFT. The cheap probe is designed to settle precisely
  this in under an hour.

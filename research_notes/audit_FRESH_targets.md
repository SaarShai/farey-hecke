# FRESH softness audit — hunting records set by a DEMONSTRABLY WEAK method (wide gap, neglected)

Date 2026-06-27. READY FOR JUDGING (not "done").

**Mandate.** Operationalize the acute-set (A089676) post-mortem: "looks soft" (small/sandwiched/anomalous
value) ≠ "is soft." The only reliable softness signal is **S1 = the current record was set by a
weak/old/one-off heuristic or a non-exhaustive search, AND S2 = there is a wide gap, AND S4 = no strong
method (SAT/ILP/specialist/AlphaEvolve/FunSearch) has been thrown at it.** Hunt for that signature; rank
by it; adversarially verify the #1 against the trap.

**Method.** 5 parallel domain sweeps (OEIS heuristic-record sequences; combinatorics-on-words; additive/
extremal constructions; graph-labeling/crossing numbers; niche packing/PHF/contest records) + my own direct
OEIS mining (curl; OEIS 403-blocks the WebFetch fetcher but curl works) + **3 decisive empirical probes I ran
myself** + survey verification. Every load-bearing fact is web-verified and tagged KNOWN; unconfirmed items
are tagged UNVERIFIED. Nothing fabricated.

**Headline.** The hunt's single most valuable output is the *discrimination*, not just a list: two of the
most seductive candidates (clean "hill-climbing"/"simulated annealing" OEIS records) **collapsed under a
5-minute probe** — the weak-method label did NOT mean slack (the acute-set trap, twice). The candidate that
**survived** the same probe — where a naive method provably **cannot** reach the record — is the genuine soft
target.

---

## AlphaEvolve / FunSearch OWNED-LIST (verified — steer around these)
From the AlphaEvolve "Mathematical exploration and discovery at scale" paper (arXiv 2511.02864, the 67-problem
study) + FunSearch (Nature 2023) + Tyrrell SAT 2023. **Confirmed already-improved / owned (do NOT propose):**
cap sets in F_3^n (FunSearch n=8 cap size 512 + AlphaEvolve + Tyrrell SAT = **triple-owned**), Erdős
minimum-overlap, sums-and-differences of sets (θ 1.14465→1.1584), autocorrelation/uncertainty inequalities
(1.50992→1.5032), kissing number d=11 (592→593), circle/hexagon/cube packing (11–12 hexagons; 11 cubes
2.912→2.895), **Heilbronn for triangles n=11 and convex regions n=13,14**, **Friedman max/min-distance-ratio
(2D AND 3D)**, no-isosceles 112 points on 64×64 grid, 3D moving sofa, 7 touching cylinders, MAX-4-CUT
inapproximability 0.987, Ramanujan graphs ≤163 nodes, IMO-2025 grid tiling, matrix-mult tensor ranks,
finite-field Kakeya, admissible sets, online bin-packing. (The paper does NOT name weak Schur, disjoint
Golomb rulers, postage stamp, path-power crossing numbers, or PHF/CFF tables — those are open ground.)

---

## RANKED CANDIDATES (softest first, by the S1–S5 rubric)

### #1 — Crossing number of path powers cr(P_n^k), k = 5, 6, 7  — SOFT (highest confidence)
- **Precise statement.** Exact crossing number of the k-th power of the path P_n^k (vertices 1..n, edge {i,j}
  iff |i−j|≤k), for k=5,6,7. The most actionable instances are the **single-n unproven upper bounds**:
  cr(P_9^6) ≤ 22, cr(P_9^7) ≤ 30, cr(P_10^7) ≤ 42, cr(P_11^7) ≤ 57, and the general-n bounds cr(P_n^5)≤4n−23,
  cr(P_n^6)≤8n−51, cr(P_n^7)≤15n−109.
- **Current record + the METHOD that set it (KNOWN, authoritative).** From the Clancy–Haythorpe–Newcombe
  survey *"A survey of graphs with known or bounded crossing numbers"* (Australas. J. Combin. 2020,
  arXiv:1901.05155), §2.5, Table 3, directly extracted:
  - Lower bound: **Harary et al. 1999** [65], `2n − 9 ≤ cr(P_n^5)` — a **hand-construction lower bound,
    never improved in 25 years.**
  - Upper bound: **Zheng et al. 2009** [254] gave UBs `cr(P_n^5)≤4n−23, cr(P_n^6)≤8n−51, cr(P_n^7)≤15n−109`
    by **hand-construction**, and **"conjectured that they would coincide with the exact crossing number."**
    Verbatim: **"Conjecture 2.48 (Zheng et al., 2009): All upper bounds in Table 3 hold with equality."**
    Equality is **NOT proven** — only exact tiny cases cr(P_6^5)=3, cr(P_7^5)=6, cr(P_8^5)=9, cr(P_7^6)=9,
    cr(P_8^6)=15, cr(P_8^7)=18 are settled.
- **Best opposite bound + gap.** For cr(P_n^5): `2n−9 ≤ cr ≤ 4n−23` — a gap of ≈2n that **GROWS linearly**.
  For k=6,7 the lower-bound side is essentially absent (only the conjectured UB exists). Wide and widening —
  the opposite of a +1 sandwich.
- **Why no strong method has attacked it (S4).** Open since **1999** (k=5) / **2009** (k=6,7). The only
  post-2009 follow-up is on *join products* of path powers (Hsieh–Lin, a different object). No SAT/ILP/
  exhaustive attack on the lower bound or the equality conjecture; **exact crossing-number ILP
  (crossingnumber.org, Chimani–Wiedera) exists and has demonstrably NOT been pointed at this family.** Not on
  any cultivated table; AlphaEvolve did not touch it.
- **What the NEW fact would be.** (a) A drawing of P_9^6 / P_9^7 / P_10^7 / P_11^7 with **fewer** crossings
  than Zheng's bound ⇒ beats a published record AND **disproves Conjecture 2.48** (big); or (b) an exact value
  via ILP that, with a matching lower bound, **settles** a previously-open small case (new fact); or (c) an
  improved general lower bound above 2n−9 (first improvement in 25 years). All are genuine NEW facts.
- **S1–S5.** S1 ✅ weak (1999/2009 hand-constructions, equality only conjectured). S2 ✅ wide, growing gap.
  S3 ✅ no TIGHT red flags — not a closed form (k=4 IS closed: cr(P_n^4)=n−3, but k≥5 is open), not on a
  cultivated table, not multiply-certified. S4 ✅ neglected by strong methods 15–25 yrs. S5 ✅ unowned,
  unbeaten now, exactly verifiable (anyone counts crossings in a drawing; ILP-checkable at small n).
- **Verdict: SOFT. Confidence HIGH.**
- **ADVERSARIAL VERIFY (did I misread the method? — the acute-set check): see the dedicated section below.
  Conclusion: NOT the trap.** My own probe shows a *naive* method canNOT match Zheng's bound (so the
  construction is genuinely non-trivial, not instantly-reproducible slack), yet the LB↔UB gap is real and the
  right strong tool (exact ILP) is unapplied. Survey-confirmed "conjectured, not proven."
- **Cheapest probe (<~1 hr).** Run crossingnumber.org (or OGDF/QuickCross exact mode) on **P_9^6, P_9^7,
  P_10^7, P_11^7** (minutes of compute). If the exact value is **below** Zheng's bound for any instance →
  published-record beat + conjecture disproof; if it **equals** the bound → a verified exact data point and the
  soft direction becomes the lower bound. Either outcome is informative and cheap.
- Sources (KNOWN): survey arXiv:1901.05155 §2.5 / Table 3 / Conj 2.48 (extracted locally, verbatim above);
  Harary et al. 1999; Zheng et al. 2009. crossingnumber.org (Chimani–Wiedera).
  *Caveat:* Zheng-2009 primary PDF is paywalled/403 — "hand-construction vs small computer search" for the UB
  is **UNVERIFIED in primary source**, but the bounds, the **conjectured-not-proven** status, and the 25-yr
  staleness are KNOWN from the authoritative peer-reviewed survey. The softness does not depend on which weak
  method Zheng used — it depends on equality being unproven and the gap being open, both confirmed.

---

### #2 — Weak Schur numbers WS(k), k ≥ 6  — SOFT
- **Precise statement.** WS(k) = largest n such that {1,…,n} partitions into k weakly-sum-free sets (no
  x+y=z with x,y,z distinct in one part). Deliverable = an explicit partition. Proven exact only through
  **WS(5)=196**; all k≥6 are lower bounds. OEIS **A072842**.
- **Current record + METHOD (KNOWN).** Every k≥6 value is a **heuristic lower bound**, and the record is a
  **moving target set by a chain of DIFFERENT ad-hoc heuristics** — the opposite of acute-set stability:
  WS(6): 572 (Eliahou et al. SAT 2012) → 574 (Fonlupt tabu) → 581 (constraint+streamliners) → 582 (Nested
  Monte-Carlo) → 642 (Rowley template 2020) → **646 (Ageron et al. 2022, explicitly "NOT obtained with a
  template")** → **650 (Rodrigo, Jun 2026 — confirmed on the live OEIS page).** Larger k (WS(7)≥2146,
  WS(8)≥6976 Rowley 2020; WS(9)≥22536, WS(10)≥71256, …) from templates / Monte-Carlo / tabu.
- **Best opposite bound + gap.** The only general upper bound is **Bornsztein 2002: WS(k) ≤ ⌊k!·k·e⌋** —
  factorial, astronomically loose (WS(6) ≤ ~6·720·e). **Effectively unbounded gap**; no tight upper bound for
  k≥6 exists.
- **Why no strong method has attacked it (S4).** SAT solved the *ordinary* Schur number S(5)=160 (Heule 2017)
  — but that is the **strong** Schur number, a different object. **No SAT/ILP-to-optimality, no AlphaEvolve,
  no FunSearch, no RL/neural method has ever attacked WEAK Schur** (verified by explicit negative search). The
  records are pure constructions; the template method (Rowley/Ageron) is a hand-designed recursive scheme —
  exactly what an evolutionary search composes/beats.
- **What the NEW fact would be.** A partition of {1,…,n} into 6 weakly-sum-free parts with **n ≥ 651**
  (beating Rodrigo's 650) — or any k≥7 improvement. A new verifiable lower bound = a genuine new fact.
- **S1–S5.** S1 ✅ (Monte-Carlo/tabu/template, moving record). S2 ✅ (useless factorial UB). S3 ✅ (no closed
  form for k≥6, not proven-optimal). S4 **◐ — neglected by STRONG methods (yes), but an ACTIVE human-heuristic
  community (Rowley/Ageron/Rodrigo) keeps nudging it.** S5 ✅ (unowned by AI, witness = O(n²) check).
- **Verdict: SOFT. Confidence MEDIUM-HIGH.** The moving heuristic record + useless upper bound is a *strong*
  genuine-softness signal (each +N from a new ad-hoc method proves slack); the caveat is that a +1 over 650 may
  itself be hard precisely because humans are actively pushing, so a fleet must aim to **leapfrog** (compose/
  evolve partitions), not nudge.
- **Cheapest probe (<~1 hr).** Seed a Nested-Monte-Carlo / local-search from the published 650-partition and
  target n=651. Reaching even 651 = a verifiable new record and proof the method-gap is real. (If a quick
  search instantly equals 650 but cannot pass it, that mirrors the acute-set trap and downgrades to UNCERTAIN.)
- Sources (KNOWN): live OEIS A072842 (Rodrigo WS(6)≥650, Jun 2026; full history); Ageron et al. arXiv:2112.03175
  ("646 not from a template"); Rowley arXiv:2011.11292 / INTEGERS v59; Bornsztein 2002 (k!·k·e bound, via the
  Gasarch weak-Schur survey).

---

### #3 — Disjoint Golomb rulers H(I, J)  — SOFT
- **Precise statement.** H(I,J) = least n such that {1,…,n} contains I pairwise-disjoint Golomb rulers
  (perfect difference sets), each with J marks. Deliverable = the I explicit rulers. Target ceiling H(I,J)=IJ
  ("regular" case).
- **Current record + METHOD (KNOWN).** Table set by **Kløve 1990 (constructions) → Shearer ~1998 (computer
  search, IEEE Trans. Inf. Theory)** for I≤11,J≤9, extended by later searches to larger (I,J) giving **18 exact
  values + ~10 entries that are upper bounds only ("not known to be optimal").** The **live numerical record is
  Shearer's ≈1998 computer search — ~27 years stale.** The 2024 paper (arXiv:2409.14409) proves only abstract
  inequalities + conjectures — **it sets no new records.**
- **Best opposite bound + gap.** Real gaps in the cells flagged "upper bound only" (complete search for the
  matching lower bound is "extremely difficult"). Note: the *single*-ruler OGR is distributed.net-cultivated to
  28 marks (TIGHT) — but the **disjoint multi-ruler H(I,J) table is NOT cultivated.**
- **Why no strong method has attacked it (S4).** Quote (KNOWN): "Optimal Golomb Rulers … can only be
  discovered or verified by exhaustive computer search." **No SAT/ILP/AlphaEvolve/FunSearch anywhere in the DGR
  literature** — methods are classical algebraic + branch-and-bound.
- **What the NEW fact would be.** Close or improve one cell flagged "upper bound only" (e.g. small I, 4≤J≤6)
  with an explicit disjoint-ruler set ⇒ new record.
- **S1–S5.** S1 ✅ (frozen 1998 computer search, no optimality on the open cells). S2 ✅ (open cells). S3 ✅
  (DGR table not cultivated; not a closed form). S4 ✅ (no modern solver/AI). S5 ✅ (witness trivially
  checkable: I rulers × J marks, pairwise-disjoint, each Golomb).
- **Verdict: SOFT. Confidence MEDIUM.** (Slightly below #2 because the open-cell gap widths need Shearer's
  IEEE table pulled to quantify.)
- **Cheapest probe (<~1 hr).** Pull Shearer's H(I,J) table, take the smallest "upper-bound-only" cell, run a
  short ILP/local search to close or improve it.
- Sources (KNOWN): arXiv:1405.4535 ("On Disjoint Golomb Rulers," the quotes); arXiv:2409.14409 (2024,
  inequalities only); Shearer 1998 (IBM Research / IEEE Trans. Inf. Theory).

---

### #4 — Perfect-hash-family / cover-free-family / superimposed-code size tables (OFF La Jolla)  — SOFT
- **Precise statement.** Minimal rows N for a PHF(N; k, v, t) (or max k for fixed N), strength t=4,5,6, small
  v; dually r-cover-free family / d-disjunct matrix max sizes. Tables: Walker–Colbourn (phftables.com),
  Dougherty ASU (t=3..11, ~2017).
- **Current record + METHOD (KNOWN).** Many entries are **explicit tabu-search / heuristic constructions**:
  Walker & Colbourn (DGCC 2007) "present … PHFs found using **tabu search**" and "the first general tables of
  the **best known sizes**" (not optima). Also great-deluge / record-to-record-travel in the literature.
- **Best opposite bound + gap.** Constructions give |F| ≥ 2^Ω(n/r²) vs upper bounds r^O(n/r²) — **"determining
  the correct base of the exponent remains an important open problem."** Per-cell gaps in small-parameter
  tables are concrete and often wide.
- **Why no strong method has attacked it (S4).** Heuristic (tabu/SA/great-deluge) + recursive algebraic only;
  **no LLM-evolution sweep.** Specific small-t / large-k cells stale since ~2017 (Dougherty).
- **What the NEW fact would be.** Add a column to a tabu-set PHF keeping the property (beats the k record), or
  drop a row at fixed (k,v,t). Self-certifying.
- **S1–S5.** S1 ✅ (tabu "best known"). S2 ✅ (exponent-base gap + per-cell gaps). S3 ✅ (off La Jolla; semi-
  maintained, not cultivated-to-optimality). S4 ✅ (no evolution attack). S5 ✅ (witness = N×k array, mechanical
  t-subarray check).
- **Verdict: SOFT. Confidence MEDIUM.** (A degree less crisp than #1–#3: pick a specific cell last touched
  ~2017 to be sure it's stale.)
- **Cheapest probe (<~1 hr).** Open Dougherty's t=5/t=6 table, find a tabu-set cell, attempt a one-column
  extension via short CP/greedy. phftables.com refused connection in this session; Dougherty ASU 2017 tables
  are the verified fallback.
- Sources (KNOWN): Walker & Colbourn DGCC 2007 (tabu, "best known sizes"); Dougherty ASU PHF tables;
  cover-free/disjunct-matrix exponent-base open problem (standard literature).

---

## ⚠️ THE TRAP, CAUGHT TWICE — soft METHOD, tight VALUE (the whole lesson, demonstrated)

These two looked like the *perfect* soft signal (literal weak-method comments) and **I would have ranked them
#1–#2 on the naive heuristic** — but my own 5-minute probe collapsed them. **This is the acute-set failure mode
reproduced and avoided.**

### A395449 — min sum of synchronizing-word lengths, n-state binary DFA  → DOWNGRADED to UNCERTAIN-leaning-TIGHT
- Literal comment (KNOWN): *"These values are the best known lower bounds obtained with a **hill-climbing
  program** and are not yet proven to be optimal."* (Kamenetsky, Apr 2026; only 9 terms; uncontested.) Maximal
  surface softness.
- **My probe (decisive).** (1) **Exhaustive** search reproduces a(3)=7, a(4)=10, a(5)=14 **exactly** (these are
  the true optima). (2) A trivial **hill-climb (10–71 s) matches all 9 OEIS values exactly (n=3..11: 7,10,14,
  18,22,26,31,36,41) and BEATS NONE.** (3) The differences are suspiciously regular (3,4,4,4,4,5,5,5 — formula-
  like). ⇒ **Weak method, but the value is almost certainly the true optimum (gap ≈ 0).** A record a trivial
  search instantly reaches is *not* slack — it is exactly the acute-set trap. **Not a FunSearch target.**

### A368539 — max sum of entries of A², A a permutation matrix of {1,…,n²}  → DOWNGRADED to UNCERTAIN-leaning-TIGHT
- Literal comment (KNOWN): *"conjecturally optimal matrices found using **simulated annealing**"*; lower bounds
  a(8)≥626610, … (Pfoertner, Jan 2024; stale; witness published). Strong surface softness.
- **My probe (decisive).** The objective collapses to `max Σ_k (rowsum_k)(colsum_k)` (clean assignment). A
  trivial local search **matches the SA values at n=4,5,6,7,8 (5,284 / 24,303 / 85,352 / 248,045 / 626,610) in
  ≈5 s each and beats none.** Combined with the comment's own *"probably equal to"* and the monotone-row/col
  structure of the optima ⇒ **soft method, tight value.** Not a FunSearch target.

**Lesson reinforced:** the discriminator is not the record's *adjective* ("hill-climbing", "simulated
annealing") but whether a cheap independent search can **beat** it. For #1 (cr(P_n^k)) a naive method
**cannot** reach the record (see below) — that is why #1 is genuinely soft and these two are not.

---

## ADVERSARIAL VERIFICATION OF #1 (cr(P_n^k)) — "is the method actually weak, or did I misread it?"

The acute-set check, applied hard:
- **Could a trivial method instantly match Zheng's upper bound (⇒ slack-that-is-really-optimal trap)?** I
  implemented P_n^5 and ran a naive 2-page (book-embedding) heuristic. It produces UBs **23, 32, 40, 50, …**
  for n=9,10,11,12 — **far WORSE** than Zheng's bound 4n−23 = **13, 17, 21, 25**. So Zheng's construction is
  **genuinely non-trivial** (needs a clever drawing my naive method can't find). This is the **inverse** of
  A395449/A368539, where a trivial search matched the record. A non-trivial record with a wide LB↔UB gap is the
  soft profile, not the trap.
- **Is the gap real, or is the LB already near the truth?** The LB 2n−9 (e.g. n=9→9) and Zheng UB 4n−23
  (n=9→13) bracket the unknown truth; the only settled exact values (3,6,9 at n=6,7,8) sit strictly between a
  naive UB and the LB. The gap is open and **grows ≈2n**. Not a +1 sandwich.
- **Is it secretly cultivated / recently resolved (would kill S4)?** Survey-confirmed open since 1999/2009;
  no improvement, no exact-ILP campaign on this family. The parallel conjecture in the same survey (Conj 3.14,
  K_n□P_m) was *confirmed for n≤10 by Ouyang 2014* — proving these path-product conjectures **are tractable and
  do get resolved when someone applies effort**, which de-risks "is it even attackable."
- **Did I misread "conjectured" as "open"?** No — verbatim from the survey: *"Conjecture 2.48 (Zheng et al.,
  2009): All upper bounds in Table 3 hold with equality."* Equality is **explicitly unproven**.

**Adversarial conclusion: #1 is NOT the acute-set trap.** Weak/old hand-constructions (S1), wide growing gap
(S2), no strong-method attack in 15–25 yrs (S4), exactly verifiable both directions (S5), and a cheap probe
that *fails to collapse it* (unlike the two traps). The one residual unknown — whether Zheng's UB was hand-
built or a small computer search — does not affect the verdict, because softness rests on **equality being
unproven + the gap being open + ILP unapplied**, all KNOWN.

---

## REJECTED elsewhere (checked; NOT soft) — abbreviated, to save the next agent the trip
- **Cap sets F_3^n** — triple-owned (FunSearch + AlphaEvolve + Tyrrell SAT). Hard avoid.
- **A309370 (Sidon subset of {0,1}^n)** — **HOT THIS MONTH**: William Blair pushed verified improved lower
  bounds **Jun 2/3/5 2026** (a(16)≥505, a(24)≥7179, …) with a public GitHub of verified sets. Someone is
  already running exactly the search-and-improve campaign. (My web search initially *missed* this because the
  search index lagged; the **live OEIS page** confirmed it — a reminder that the reliable trap-detector is the
  live page, not a stale search snippet.)
- **A227133 (no axis-parallel square)** — Gurobi MIP (141 days/32 cores) + coherent-Ising-machine (Mar 2026).
  Crowded, despite having an SA comment.
- **A250000 (peaceable queens)** — conjectured closed form 7n²/48, ILP + dedicated 2024 paper. Cultivated.
- **A331968 (snake polyomino)** — DNN attack 2026 (arXiv 2603.12400) + closed-form bounds. ML already on it.
- **Heilbronn-in-a-square (continuous)** — being CERTIFIED (MIQCP, n≤9 proven optimal, arXiv 2512.14505 /
  2603.11107, 2026). Tight.
- **Queens-domination** — fresh SAT attack (arXiv 2508.11945, Aug 2025). Tight.
- **MinLA / antibandwidth (Harwell-Boeing)** — the famous "huge gap" is a **weak-bound artifact**: Caprara et
  al. "Decorous Lower Bounds" and Sinnl 2019 both show the **heuristic records are near-optimal**. Looks soft,
  is NOT. (Pure acute-set logic.)
- **AZsPCs "Point Packing"** (integer-coord, all-distinct distances, min enclosing circle) — structurally
  soft (frozen contest records, discrete checkable witness, AlphaEvolve did not touch it) BUT the live Final
  Report shows the records were set by a **mass competitive SA/local-search contest** and have been **unbeaten
  for ~16 years** (last improvement Jan/Feb 2010). Mass competitive search is a *stronger* method than one
  hill-climb, and 16-yr stability is acute-set-shaped. **UNCERTAIN-leaning-TIGHT** — listed not recommended.
- **Combinatorics-on-words** — mostly well-defended (Ochem/Shur/Currie/Mol/Rampersad/Shallit replace heuristic
  records with exact/exhaustive). Two non-record open *existence* leads (additive-cube-free over {0,1,2,3};
  an index-6 unavoidable pattern) are SOFT-shaped but are discovery targets, not record-beats. The rich-word
  length 2411 (backtracking+eerTree) is **probably exhaustive ⇒ tight** over its proven-finite language.
- **Greedy B_h sets (A365301–5), single OGR, MSTD-smallest (solved/Conway), difference families (La Jolla),
  Sidon/Singer in Z_n** — cultivated or deterministic-greedy (can't "beat" a greedy value).

---

## RECOMMENDATION (for the synthesis loop)
- **Fleet #1 = cr(P_n^k), k=5,6,7.** Only candidate that is simultaneously weak-record (S1), wide *growing*
  gap (S2), strong-method-neglected 15–25 yrs (S4), exactly verifiable both ways (S5), AND **survives the cheap
  collapse-probe** (a naive method cannot reach the record). FunSearch-shaped: evolve drawings to beat the
  conjectured UBs / disprove Conj 2.48, or wrap exact ILP at small n. **First action: crossingnumber.org on
  P_9^6, P_9^7, P_10^7, P_11^7 (minutes).**
- **Backups: #2 weak Schur (leapfrog 650, don't nudge), #3 disjoint Golomb rulers (close an "upper-bound-only"
  cell).** Both heuristic-set, wide-gap, finite-witness, AI-untouched.
- **Do NOT** fleet A395449 or A368539 (soft method, tight value — the trap) or AZsPCs Point Packing (mass-
  search record, 16-yr stable) without first confirming a cheap search can actually *beat* the record.

**Methodological note for the filter (earned this session):** the most reliable disqualifier was NOT the
record's adjective but two live checks — (a) does a 5-minute independent search *beat* it (if it only *matches*,
suspect optimal-but-unproven = trap), and (b) does the **live source page** (not a stale web-search snippet)
show a recent strong/ML/contest attack. A309370 (live page caught the Jun-2026 push my search missed) and
A395449/A368539 (probe caught the tight value the comment hid) are the two cautionary cases.

---

### Verification ledger (KNOWN vs UNVERIFIED)
- KNOWN (verified live / authoritative source / my own reproduced computation): cr(P_n^k) bounds + Conjecture
  2.48 + Harary 1999 LB + exact small cases (survey arXiv:1901.05155, extracted verbatim); cr(P_n^4)=n−3;
  my naive-2-page UBs for P_n^5 (reproduced cr(P_6^5)=3); A395449 exhaustive a(3..5) + hill-climb match n=3..11
  (my computation); A368539 objective = Σ rowsum·colsum + local-search match n=4..8 (my computation); A072842
  weak-Schur record chain incl. Rodrigo WS(6)≥650 Jun 2026 (live OEIS); A309370 Blair Jun 2/3/5 2026 (live
  OEIS); AlphaEvolve owned-list (arXiv 2511.02864 + corroborating summaries); AZsPCs Point Packing contest
  ended Oct 2009, last post-contest improvement Jan/Feb 2010 (live azspcs.com).
- UNVERIFIED (flagged): Zheng-2009 UB hand-vs-computer method (primary 403; does not affect verdict); exact
  per-cell gap widths for disjoint Golomb rulers (need Shearer's IEEE table) and PHF/CFF (phftables.com refused;
  Dougherty ASU fallback); combinatorics-on-words 2026 distinct-square arXiv IDs (post-cutoff, agent flagged).
- Nothing in this file is fabricated. Where a source could not be opened, the claim is tagged UNVERIFIED and
  the verdict is shown not to depend on it.

# Domain A — OEIS extremal / "hard" sequences: FunSearch-mode target hunt

Date 2026-06-27. Agent: Domain-A survey (OEIS extremal-construction long tail).
Method: OEIS search API (curl, JSON/text fmt — WebFetch is 403-blocked on oeis.org) +
web-verification of each candidate's current record, last-known term, and who/when.
Goal per FUNSEARCH_TARGET_GOAL.md: finite + exactly-verifiable witness, beatable by a
SAMPLE-LIMITED smart-search fleet (dozens-hundreds of proposals, not millions), NOT owned by
FunSearch / AlphaEvolve / an active specialist, community would recognize the contribution.

---

## TL;DR ranking

| # | OEIS | object | last term / when | owned? | sample-limited fit | verdict |
|---|------|--------|------------------|--------|--------------------|---------|
| 1 | **A248866** | discrete Heilbronn: 2×min-triangle-area, n pts on n×n lattice | **a(13), Yamanouchi 2015** (untouched 11 yrs) | **NO** (cont. Heilbronn hot, discrete neglected) | strong — tiny grid, integer objective, structure-bottleneck | **REAL TARGET** |
| 2 | A331968 | max cells of snake-like polyomino (induced path) in n×n | a(17), Yi Yang Oct 2022 | partial (snake-in-box adjacent) | medium — induced-path search | backup |
| 3 | A346069 | place 1..n on grid, max Σ(orthogonally-adjacent products) | a(14), Oct 2021 (neglected) | NO | medium-high — QAP-type arrangement | backup |
| 4 | A269746 (drop) | max 1s in triangle, no axis-parallel triangle of 1s | a(20), Chai Wah Wu **Dec 2025** | **YES** (active) | — | OWNED |
| 5 | A181018 (drop) | max 1s, no 3 collinear-adjacent in n×n | a(16), P.J.Taylor **2016** | NO but | FLOPS-bound (ILP, 17×17 exhaustive) | drop |

**Top pick: A248866 (discrete Heilbronn triangle on the n×n integer lattice).**

---

## CANDIDATE 1 (TOP) — A248866: discrete Heilbronn triangle problem

**Definition.** a(n) = twice the maximal area of the smallest triangle formed by any 3 of n points
chosen from the n×n integer lattice ({0..n-1}²). (Factor 2 makes it an integer: lattice-triangle
areas are multiples of 1/2.) Keyword: `nonn,more`.

**Data (the whole sequence):** `4, 9, 6, 6, 5, 6, 5, 6, 6, 6, 6` for n = 3..13.
i.e. a(3)=4, a(4)=9, a(5)=6, a(6)=6, a(7)=5, a(8)=6, a(9)=5, a(10..13)=6.
Conjecture in the entry: the sequence is an infinite repetition of only two integers (5 and 6).

**Current record / who/when (web-verified).** a(5),a(7),a(9) corrected and a(10)–a(13) added by
**Hiroaki Yamanouchi, 9 Mar 2015**. There is an examples file (a248866.txt) giving an optimal point
set for each of a(3)..a(13) — confirmed fetched: e.g. a(13) region values sit at 5–6, witnesses are
small explicit lattice configurations (corners + scattered interior points). **No term added since
2015. No paper. No specialist.** Last metadata touch is the 2015 extension; the entry has sat for
~11 years. (Verified by direct OEIS pull + web searches for "Yamanouchi discrete Heilbronn",
"Goldberg biggest little / integer lattice min triangle" — the discrete n×n maximin variant appears
ONLY in this OEIS entry; nothing in the recent literature targets it.)

**Why this is sample-limited-friendly (the core of the case):**
- **Tiny finite object.** A witness for a(n) is just n lattice points in {0..n-1}². For the open
  frontier a(14): 14 points in a 14×14 grid. Trivially representable as a short list of coords;
  a fleet agent emits one as a few lines of data.
- **Objective is a small integer, exactly + instantly verifiable.** Score(config) = 2 × min over all
  C(n,3) triples of the triangle area = min over triples of |cross product| (an integer). For n=14
  that's C(14,3)=364 cross-products — microseconds. Anyone can independently check a claimed record
  by recomputing this. No floating point, no certificate needed (exact integer arithmetic). This is
  the cleanest possible "witness anyone can check."
- **Structure, not FLOPS, is the bottleneck.** Exhaustive search for a(14) is C(196,14) ≈ 10^18 —
  infeasible to enumerate, which is exactly WHY it's stuck and why a brute-force person hasn't just
  pushed it. But the optimum is NOT a needle in featureless hay: optimal configs are highly
  structured (corner-anchored, spread-out, avoid any 3 near-collinear or any small-area triple),
  and the target value is one small integer (the conjecture says it's 5 or 6). A smart
  construct-then-local-search (place points to maximize the running min-area, hill-climb / simulated
  anneal on a candidate, with LLM-proposed structural templates) is precisely the regime where
  reasoning + cheap exact eval beats blind enumeration. The 2015 contributor's heuristic was good
  enough for n≤13 a decade ago; modern smart search can plausibly push a(14), a(15), maybe a(16+),
  and/or **settle the "only two integers {5,6}" conjecture** for the next several n (the most
  interesting deliverable — does it ever leave {5,6}?).

**Concrete verifiable contribution (pick any):**
1. Extend the sequence: produce a verified a(14) (and a(15), a(16)…) with explicit optimal/best-known
   point sets. Each is an OEIS-submittable b-file entry + witness file. Even a verified *lower bound*
   (a config achieving min-area = 6 on the 14×14 grid) is a contribution; proving it's *maximal*
   needs an upper-bound argument or exhaustive certificate, but the LOWER bound (a record config) is
   the FunSearch-style deliverable and is independently checkable.
2. Test the conjecture: find a config beating the value 6 for some n (would refute "only two
   integers"), OR accumulate strong evidence it stays in {5,6}.

**Novelty / owned status (brutal).**
- The **continuous** Heilbronn problem (n points in the unit square) is RED-HOT and OWNED: Cohen–
  Pohoata–Zakharov upper bound 2023 (Quanta-covered); mixed-integer optimization certifying n=9
  (arXiv 2603.11107, Mar 2026); global-optimization methods (arXiv 2512.14505, Dec 2025); AlphaEvolve
  did the **continuous** Heilbronn n=11 (0.036→0.0365). **Do NOT touch continuous Heilbronn.**
- The **discrete n×n integer-lattice maximin** variant (this sequence) is a DIFFERENT object — integer
  values, no rescaling, combinatorial — and I verified (WebFetch of arXiv 2512.14505) the 2025-2026
  optimization papers are continuous-unit-square ONLY; none mention the integer-lattice variant.
  Not in AlphaEvolve's 67 (which lists continuous Heilbronn), not FunSearch, no specialist. **Open.**
- Adjacent but distinct: A248867/A248868 family (other discrete-Heilbronn variants by the same
  contributor) — same neglect, could be done in the same pilot. A343851 is the continuous 7-point
  decimal (different, `cons`).

---

## CANDIDATE 2 — A331968: longest snake-like polyomino (induced path) in n×n box

**Definition.** a(n) = max number of unit cells in a snake-like polyomino in an n×n box =
max vertices of a chordless (induced) path in the n×n grid graph. Keyword `nonn,hard,more`.
**Data:** 1,3,7,11,17,24,33,42,53,64,77,92,107,123,142,162,182 (n=1..17). a(16)≥161 noted; a(15)
from Andrew Howroyd 2020, **a(16)-a(17) from Yi Yang Oct 2022**.
**Witness/verify:** a path given as a cell list; check it's an induced path (no two non-consecutive
cells adjacent) and count cells — instant, exact.
**Sample-limited fit:** medium. Induced-path search in a grid; structure matters, objective is a
small integer. n=18 frontier is a modestly larger grid.
**Owned?** Semi. Tied to the snake-in-the-box circle (A099155, which IS a long-time genetic-algorithm
target — competitive turf). Less crowded than the hypercube version but Yi Yang touched it in 2022.
**Verdict:** viable backup, but the snake-in-box adjacency means a GA community could contest it.

---

## CANDIDATE 3 — A346069: max Σ(adjacent products), numbers 1..n on a grid

**Definition.** Place 1..n on a square grid (free position/orientation); for every orthogonally
adjacent pair multiply the two numbers; a(n) = max possible sum of these products. Keyword `nonn,more`.
**Data:** 0,2,9,25,54,100,167,258,377,529,718,947,1220,1542 (n=1..14). **Neglected since Oct 2021.**
**Witness/verify:** a placement (positions of 1..n); recompute sum of adjacent products — instant.
**Sample-limited fit:** medium-high. Pure arrangement/QAP-type optimization, small n, structure-driven
(large numbers cluster). Next term a(15) = optimal placement of 1..15 — combinatorially nontrivial,
no closed form, fleet-friendly.
**Owned?** No active cultivator found (Munafo/Sloane "place-numbers-on-grid" family, A346069 a quiet
member). The companion ADDITION problem A348090 is easier (swap-invariant); the PRODUCT version is
genuinely order-dependent and harder.
**Risk:** could be amenable to a clean greedy/exchange argument or known as a quadratic assignment
instance — needs a quick check that the optimum isn't a trivial spiral. Lower confidence it's "hard."
**Verdict:** decent backup; verify non-triviality before committing.

---

## REJECTED (owned / FLOPS-bound / active) — do NOT pursue

- **A272651 / A000769 (no-3-in-line)** — RED-HOT, OWNED. Thomas Prellberg extended a(47)–a(64)
  across **Oct 2025 → Feb 2026** (this year). Classic, intensely cultivated. OFF-LIMITS.
- **A269746 (no-axis-triangle triangular array)** — Chai Wah Wu extended a(15)–a(20) **Dec 2025.** Active.
- **A186705 (Erdős unit distance, max equal distances)** — OWNED HARD. Alexeev–Mixon–Parshall 2024
  (rev. 2025) exact to a(21) + bounds a(22..30) via heavy SAT; erdosproblems #90; touched May/Jun 2026.
- **A393584 (Erdős #36 difference partition)** — OWNED, being extended a(19)–a(33) by Dobbelaere /
  Sievers / Kesarwani **Feb–Mar 2026**, tied to erdosproblems.com.
- **A002853 (max equiangular lines)** — famous (Jiang–Tidor–Yao–Zhang–Zhao 2021), top-researcher turf.
- **A352178 (max pair-sums = powers of 2)** — heavily cultivated (Sloane, Alekseyev, Scheuerle,
  Smith, Pratt) 2022–2026, with theory (no-4-cycle theorem). Owned.
- **A000937 / A099155 (snake/coil-in-the-box, hypercube)** — decades-long GA/distributed-search
  community target; we'd be competing on their core turf with less compute. OFF-LIMITS.
- **A328873 / A287695 (orthogonal diagonal Latin squares)** — Gerasim@Home / BOINC distributed
  compute. FLOPS-bound + owned.
- **A181018 (max 1s, no 3-collinear-adjacent)** — neglected since 2016 (P.J. Taylor, a(16)), keyword
  `more,nice`, NOT owned — BUT next term (17×17) is an exhaustive/ILP search = FLOPS-bound, not a
  structure-bottleneck the fleet can out-reason. DROP (fails the "beatable by sample-limited" test).
- **A244506 (count of max no-√3 configs on triangular grid)** — a COUNTING sequence (grows to 2.4e10
  at n=10); enumerating all optima is FLOPS-bound. DROP.
- **A004137 (max-edge graceful graph / optimal sparse ruler)** — actively cultivated (Luschny,
  Wichmann conjecture, Robison verifications); records to a(26). Owned by sparse-ruler community.
- **A122224/A122226 (longest self-avoiding path in a circle)** — Hugo Pfoertner extended a(8)–a(11)
  **June 2026** (this month). Actively cultivated right now. OFF-LIMITS.

---

## ADVERSARIAL KILL-ATTEMPT on the top pick (A248866 — discrete Heilbronn)

I tried to kill it on all four failure modes:

1. **"Secretly owned?"** — Searched: "Yamanouchi discrete Heilbronn", "discrete Heilbronn lattice
   grid min triangle terms", "Goldberg biggest-little integer lattice", and the live 2025-2026
   Heilbronn optimization/AlphaEvolve work. Result: the discrete n×n maximin variant appears in NO
   paper — only this OEIS entry, last extended 2015. The hot Heilbronn activity is provably
   continuous-unit-square (confirmed by reading arXiv 2512.14505). **Survives.** (Caveat: someone
   *could* fold it into a MIP/CP solver quickly — see risk below — but as of now it is uncultivated.)

2. **"Secretly FLOPS-bound (needs exhaustive search beyond reach)?"** — This is the real risk and the
   honest tension. Two regimes:
   - **Best-known LOWER bound (a record config achieving a given min-area):** clearly sample-limited-
     friendly. Constructing a 14-point set on a 14×14 grid with min-triangle-area = 6 is a small smart
     search; the fleet can do this. This IS a FunSearch-style deliverable (a witness/record), exactly
     in scope.
   - **Proving the value is OPTIMAL (the true a(14)):** requires either an exhaustive certificate over
     C(196,14)≈10^18 configs (FLOPS-infeasible for us) OR a combinatorial upper-bound argument. So a
     *certified exact* a(14) may be out of reach by pure search — BUT note (a) Yamanouchi presumably
     used a smart (non-exhaustive) search to claim a(10)–a(13) as exact, so the bar isn't full
     enumeration; the values are tiny (5/6) and upper bounds for "no triangle smaller than area t on
     an n×n grid" are themselves combinatorially constrained; (b) even if we can only deliver a
     *record lower bound + the conjecture test*, that's a legitimate contribution. **Survives, with the
     honest scoping that the guaranteed deliverable is the record/lower-bound + conjecture evidence,
     not necessarily a certified-optimal exact term.** This matches the FunSearch paradigm (records,
     not optimality proofs).

3. **"Not actually open?"** — Frontier is a(14); the whole sequence is 11 terms and the entry is
   flagged `more` (OEIS itself wants it extended). The {5,6} two-integer conjecture is explicitly
   open. **Survives.**

4. **"Not independently verifiable?"** — A witness is a list of ≤16 integer coordinate pairs; the
   score is an exact integer (min of C(n,3) integer cross-products). Verification is a 10-line script
   anyone can run, no floating point, no trust. **Survives — this is the strongest dimension.**

**Residual risks (honest):**
- (R1) The exact-optimality gap: our defensible win is the best-known config / lower bound + conjecture
  evidence; a *proven* exact a(n) may need an upper-bound argument we can't get from search alone.
  Frame the deliverable as "extended/record + structural conjecture test," not "settled exactly."
- (R2) Low-glamour: it's a neglected OEIS niche, not a famous open problem — modest significance (but
  that is the explicit point of the sample-limited long-tail strategy, and an extended `more` sequence
  + a settled/refuted in-entry conjecture is a recognized OEIS contribution).
- (R3) Easy to fold into a MIP/CP/SAT solver: a motivated person could attack it with off-the-shelf
  constraint solvers tomorrow. It's been open 11 years, so apparently nobody has — but this is a
  "move now" target, not a durable moat.

Net: the pick survives the kill attempt. The honest framing is **record-lower-bound + conjecture
test on a genuinely neglected, trivially-verifiable, structure-bottlenecked lattice problem.**

---

## READY FOR JUDGING

Verdict: **YES — one REAL Domain-A target: A248866 (discrete Heilbronn triangle on the n×n integer
lattice).** Neglected since 2015 (a(13)), trivially+exactly verifiable (witness = ≤16 lattice points,
score = min integer cross-product), structure-bottlenecked not FLOPS-bound, and provably distinct
from the red-hot continuous Heilbronn that AlphaEvolve/MIP own. Realistic contribution: a fleet-found
**record/lower-bound config (and likely extended term) for a(14)–a(16), plus a test of the open "values
stay in {5,6}" conjecture** — each an independently checkable, OEIS-submittable witness. Backups if it
falls: A331968 (snake-polyomino induced path, n×n) and A346069 (grid adjacency-product arrangement).
Honest caveat: guaranteed deliverable is a record + conjecture evidence, not a certified-optimal exact
term (exact optimality may exceed pure-search reach); and it's a "move-now" target (no moat vs a CP/SAT
solver), low-glamour but recognized.

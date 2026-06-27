# Domain F hunt — FRESH (2023–2026) extremal-construction problems, no specialist sweep yet

Date 2026-06-27. Agent F. Target: a beatable, exactly-verifiable, NON-OWNED extremal
construction problem POSED/active in the last ~3 years that a SAMPLE-LIMITED smart-search
fleet (dozens–hundreds of LLM-reasoned candidate objects + exact verification, NOT a
million-eval / supercomputer loop) has a realistic shot at contributing a record/witness in weeks.

Method: web-searched recent arXiv (math.CO/NT/MG), recent OEIS construction sequences,
problem columns (Tao/Kalai/Pak/Open Problem Garden/Randomstrasse101), and cross-checked
each candidate against the AlphaEvolve (DeepMind 2025, 67-problem sweep) and FunSearch
owned-lists, plus the newer AI-construction papers (Reinforced Generation 2509.18057,
ImprovEvolve, CodeEvolve). All numbers below are web-verified or flagged UNVERIFIED.

---

## FIRST: what the AI sweep already OWNS (the brutal novelty filter)

Cross-checked. Do NOT propose these — confirmed swept/owned:
- **AlphaEvolve (arXiv 2511.02864 + github.com/google-deepmind/alphaevolve_results):** matrix
  multiplication tensor ranks (<3,3,3>=23, <2,4,5>, <2,4,7>, <2,4,8>, <2,5,6>, <3,4,6>, <3,4,7>),
  autocorrelation inequalities, **difference bases**, kissing numbers, sphere packing,
  **finite-field Kakeya**, **Nikodym sets** (inspired a Tao paper), touching cylinders (6.54),
  Erdős minimum-overlap, ~50+ Erdős-problem bounds. 67 problems total.
- **FunSearch (Nature 2024):** cap sets, admissible sets, online bin packing, Erdős min-overlap.
- **Reinforced Generation of Combinatorial Structures (arXiv 2509.18057, Sep 2025):** MAX-CUT &
  MAX-IndSet certification on random 3-/4-regular graphs (Ramanujan graphs ≤163 nodes),
  MAX-4-CUT (0.987), MAX-3-CUT (0.9649), metric-TSP hardness (111/110). Gadget-inapprox sweep.
- **Specialist-swept (avoid):** Ramsey numbers (Radziszowski survey), **Condorcet domains**
  (arXiv 2601.07336, Jan 2026 — supercomputer inductive search, FLOPS-bound, 9≤n≤25 done),
  **peaceable queens** A250000 (Ainley 1977 constructions unbeaten 47 yrs; Clinch–Drescher–
  Huynh–Saffidine 2024 did the upper bound), no-3-in-line, Heilbronn, Sidon/B_h.

KEY EMPIRICAL FINDING of this hunt: the "famous + finite-witness" extremal problems are
nearly all swept; the genuine fresh long tail lives in NICHE de-Bruijn-adjacent / coding /
sequence-construction corners that the AI fleets and the big specialist groups have NOT touched.
The second sub-agent's blog/problem-column sweep (Tao, Kalai, Pak, Randomstrasse101, Barbados
2025, Steinerberger) confirms: recent open-problem *columns* are dominated by asymptotic
theorems and analysis-bound conjectures (KLS, Paley clique via SOS, Lovász-θ, MUB(6), Zauner) —
structurally NOT finite-smart-search-friendly. The OEIS / niche-arXiv corner is where the
elbow room is.

---

## CANDIDATE 1 (TOP PICK) — Binary orientable sequences: largest period for small order n

**Statement.** An *orientable sequence of order n* (OS(n)) over a k-ary alphabet is a cyclic
(periodic) sequence in which every length-n window appears **at most once across the whole
period, in either reading direction** (forward or reversed). Equivalently each length-n factor
and its reversal each occur ≤ once; in particular the sequence contains **no length-n
palindrome**. Objective: maximize the period (length) M_n,k. Introduced by Dai–Martin–Robshaw–
Wild (robotic position sensing). **The exact maximum is known only for n ≤ 7** (binary).

**Current best (binary, k=2) — web-verified from Gabrić–Sawada, arXiv:2401.14341 Table 2:**

| n  | best construction L_n | best known (search-extended) L*_n | upper bound U_n | exact max? |
|----|----------------------:|----------------------------------:|----------------:|:----------:|
| 7  | 14                    | 40                                | 40              | **known**  |
| 8  | 48                    | **92**                            | **96**          | OPEN (gap 4) |
| 9  | 126                   | **174**                           | 206             | OPEN (gap 32) |
| 10 | 300                   | **416**                           | 443             | OPEN (gap 27) |
| 20 | 509,220               | 519,160                           | 521,964         | OPEN        |

The L*_n records come from a **construction (cycle-joining successor rule) PLUS a heuristic
"extension" step** (their §7), NOT exhaustive search and NOT proven optimal. Trivial upper bound
U_n = 2^{n-1} − 2^{⌊(n-1)/2⌋}; improved upper bounds in Mitchell–Wild (arXiv:2507.02526, 2025).

**Source / when posed.** Active, fast-moving niche: Gabrić–Sawada (arXiv:2401.14341, Jan 2024;
CPM 2024), Mitchell–Wild arXiv:2409.00672 (Discrete Appl. Math. 377 (2025) 242–259) &
2507.02526 (2025), arXiv:2411.17273 & 2407.14866 (non-binary), 2602.04433 (Feb 2026, neg.
orientable upper bounds), 2603.18646 (Mar 2026, asymptotically-optimal constructions).
Live records table maintained at **debruijnsequence.org/db/orientable** (downloadable
sequences + code → independent verification feasible).

**Why no specialist has swept it.** The whole literature is ~6 people pursuing **asymptotic
optimality** (O(1)-amortized constructions, period ~ U_n as n→∞) and **upper bounds**. NO ONE
has run a structured search at the SMALL exact maxima — those have sat at the construction+
heuristic value since 2024. **Adversarially confirmed: NO AlphaEvolve / FunSearch / RL paper
has touched orientable sequences** (search explicitly returned no connection).

**Why sample-limited-friendly.** Object is TINY (n=8: a binary cyclic word of period ≤96; a few
hundred bits). The search space (2^96 necklaces) is FAR too big to brute-force → it is a
**structure/reasoning bottleneck, not a FLOPS bottleneck** — exactly our edge. The constraint is
clean and local (no repeated length-n window in either direction; no length-n palindrome) and
LLM-friendly: propose a seed + extension/swap; an O(period·n) verifier accepts/rejects exactly.
Many handles for smart mutation: extend the §7-style heuristic, lengthen via local edits,
exploit the palindrome-avoidance + de-Bruijn-graph structure, try CP/SAT seeded by LLM ideas.

**Concrete verifiable contribution.** (a) Push the n=8 binary record from 92 toward/at 96 (any
93–96 sequence is a publishable record; 96 would SETTLE n=8 by meeting the upper bound). (b) or
improve n=9 (174→?) or n=10 (416→?). Each is a single cyclic binary word checkable by anyone in
milliseconds. A new largest-known-period OS(8) is a recognized (modest) contribution to this
active sub-field and a clean OEIS update.

**Novelty / owned status.** NOT owned. NOT AI-swept. Small-case records are the explicitly
neglected side (the group optimizes asymptotics). Records are non-exhaustive/heuristic ⇒ beatable.

---

## CANDIDATE 2 — k-ary orientable sequences, small (n,k) records

**Statement.** Same object, alphabet size k ≥ 3, small order n. Maximize period M_n,k.

**Current best.** Constructions in Gabrić–Sawada (non-binary, arXiv:2407.14866 / Springer
Crypt.&Comm. 2024) and "Special orientable sequences" (arXiv:2411.17273; Australas. J. Combin.
94(1) (2026) 122–144) are **asymptotically optimal as k→∞**, but the SMALL exact records (e.g.
n=4,5,6 for k=3,4,5) are not pinned. UNVERIFIED exact small-(n,k) table — one search snippet
mentioned an L*-value 8,315,496 for some (n=8,k=8) cell but I could not confirm the cell or the
upper bound; treat as UNVERIFIED.

**Why niche / sample-limited.** Same structure as Candidate 1, more cells, smaller objects for
small (n,k). Same verifier. Same "asymptotics-not-small-cases" neglect.

**Concrete contribution.** A record period for a specific small (n,k). **Caveat:** must first
hand-extract the authoritative current small-(n,k) table from the papers (the readable arXiv
HTML / debruijnsequence.org) before claiming any record — I could NOT fully verify the small-k
records in this hunt. Weaker than Candidate 1 only because the binary n=8 gap (=4 to the upper
bound, with the upper bound a clean settle target) is the single sharpest, most-verifiable cell.

**Novelty / owned status.** NOT AI-swept; same group owns the asymptotic side, leaves small
exact cells open. Lower confidence than C1 pending exact-table verification.

---

## CANDIDATE 3 — Minwise-independent permutation families (small exact sizes)

**Statement.** Find the maximum size of a family F of permutations of [n] that is *(exactly)
minwise independent*: for every subset X ⊆ [n] and every x ∈ X, Pr_{π∈F}[π(x)=min π(X)] = 1/|X|.
Few exact values known; extending is hard.

**Current best / source.** Active computational push: **Iurlano & Raidl, SAT-based search,
arXiv:2412.11811 (Dec 2024)** — exactly the "still being pushed by exact search" signal. (OEIS
linkage uncertain; the sub-agent's "A036604" tag is WRONG — A036604 is sorting-network
comparisons; treat the OEIS number as UNVERIFIED.)

**Why sample-limited-friendly / why niche.** Small finite objects (sets of permutations of small
[n]); membership is an exactly-checkable linear constraint system. Niche (databases / near-dup
LSH origin), not in any AI sweep. **Risk:** a Dec-2024 SAT paper is already on it ⇒ partly
"owned" by exact solvers; an LLM fleet would have to beat SAT, which is a real bar. Medium.

**Concrete contribution.** A larger exact minwise-independent family for a specific n, or a
record for a relaxed/approximate variant. Verifiable by checking the defining equalities.

**Novelty / owned status.** Fresh-ish and non-AI-swept, BUT a specialist exact-search effort
(SAT, 2024) is live ⇒ weaker on the "no one is on it" axis than C1.

---

## CANDIDATE 4 — Negative orientable sequences (small-order records)

**Statement.** A *negative* orientable sequence: each length-n window appears at most once, and
its **reversal does NOT appear at all** (stricter than OS(n)). Maximize period. Distinct object,
distinct (smaller) records, distinct upper bounds.

**Current best / source.** Brand-new: **arXiv:2602.04433 (Feb 2026) "New upper bounds for the
period of a negative orientable sequence"**, plus 2409.00672 and 2603.18646 (Mar 2026,
constructions). The record/upper-bound GAP for small n is freshly opened (2026) and explicitly
the subject of current papers. Exact small-n record table UNVERIFIED in this hunt (PDFs didn't
render); needs hand-extraction.

**Why sample-limited-friendly.** Identical profile to C1 (tiny cyclic binary words, trivial
exact verifier, structure bottleneck). The 2026 upper-bound paper means the lower-bound
(construction) side is the open complementary target.

**Concrete contribution.** A record-period negative-orientable sequence for small n, or closing
a small-n gap. Same milliseconds-to-verify property.

**Novelty / owned status.** Freshest of all (2026), NOT AI-swept. Lower rank than C1 ONLY because
I could not web-verify the exact current small-n numbers (the readable tables didn't load), so
the "how big is the gap / is it already tight" question is open. Strong runner-up; verify table first.

---

## RANKING (realistic-shot × not-owned × exactly-verifiable × significance)

1. **Candidate 1 — binary OS(n), small-order record (focus n=8: 92 vs 96).** Sharpest,
   most-verified, smallest object, a gap of only 4 with a clean "settle by hitting the upper
   bound" win, records are heuristic (beatable), zero AI/specialist search on the small cells.
2. **Candidate 4 — negative orientable sequences, small n.** Same great structure, freshest
   (2026), but exact current numbers UNVERIFIED here.
3. **Candidate 2 — k-ary OS(n,k), small cells.** More cells, same structure; small-cell exact
   table UNVERIFIED.
4. **Candidate 3 — minwise-independent families.** Fresh-ish and non-AI-swept, but an exact-SAT
   specialist push (Dec 2024) is already live; beating SAT is a real bar. OEIS tag unverified.

---

## ADVERSARIAL VERIFICATION of the top pick (Candidate 1) — trying to KILL it

- **Already improved in a follow-up?** Checked the latest (2025–2026) papers. The 2026 work
  (2411.17273, 2407.14866, 2603.18646) targets **non-binary asymptotics**; 2602.04433 targets
  **negative-orientable upper bounds**; 2507.02526 improves **upper bounds**. NONE re-optimizes
  the SMALL BINARY records — n=8 still sits at L*_8 = 92 (Gabrić–Sawada 2024). **Survives.**
- **Secretly already solved (is 92 actually the max)?** No: literature uniformly states the exact
  maximum is **known only for n ≤ 7**; n=8 is explicitly open with a 92–96 window. **Survives.**
- **Secretly FLOPS-bound (brute force settles it)?** No — 2^96 necklaces is not enumerable; that
  is precisely WHY the maximum is unknown despite a small object. It is a **structure/reasoning**
  problem ⇒ in our wheelhouse, not DeepMind's million-eval lane. **Survives** (this is the point).
  Caveat: a clever *pruned* exact search (branch-and-bound / SAT over the de-Bruijn graph with
  palindrome + reversal constraints) might also crack n=8 — so a competitor with a good solver is
  conceivable; but none is published, and an LLM fleet can ALSO emit such a solver. Net: open.
- **Not verifiable?** Verification is trivial and exact: O(period·n) — slide every length-n
  window, check it and its reversal each occur ≤ once. Downloadable reference sequences/code at
  debruijnsequence.org for cross-checking. **Survives.**
- **Actually owned (AI sweep / big specialist group)?** Adversarial search returned **no
  AlphaEvolve/FunSearch/RL connection** to orientable sequences; the specialist group is small
  and aimed at asymptotics + upper bounds, NOT small-case search. **Survives.**
- **Significance too low?** Modest but real: it is an actively-published 2024–2026 sub-field with
  a live records table; a new largest-known OS(8) (or settling n=8) is a recognized contribution
  and a clean OEIS update. Honest framing: a *modest record*, not a famous breakthrough — exactly
  the long-tail target class the goal asks for. **Survives (as modest).**

**Residual risks (honest).** (i) The 92→96 gap might be genuinely hard to close at the top end
(95–96 could require the true maximum, which may be < 96 — then the "settle" win shrinks to just
nudging the record up by 1–3). (ii) A pruned exact solver, if someone writes one, could scoop the
n=8 settle (no such paper exists today). (iii) Cross-check that nothing on debruijnsequence.org
or a very recent (mid-2026) preprint already lists 93–96 for n=8 before investing — the live
table should be re-read at pilot start.

---

## READY FOR JUDGING

**REAL target: YES — Candidate 1, small-order binary orientable sequences (focus n=8: largest
known period 92 vs upper bound 96, exact maximum OPEN; n=9: 174, n=10: 416).** Tiny exactly-
verifiable cyclic-binary witness, a structure-bottleneck (not FLOPS) problem, records are
heuristic/non-exhaustive (beatable), confirmed NOT swept by any AI fleet or specialist search,
in an active 2024–2026 niche with a live records table. Realistic sample-limited contribution:
a new largest-known OS(8) period in {93,…,96} (96 settles n=8 against the upper bound), or an
improved record for n=9/10 — each a single sequence anyone can verify in milliseconds and a clean
OEIS/record update. Runner-up: negative orientable sequences (Candidate 4, freshest/2026) once
its small-n record table is web-verified.

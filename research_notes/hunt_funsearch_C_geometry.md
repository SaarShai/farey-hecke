# FunSearch/AlphaEvolve target hunt — Domain C: Combinatorial & Discrete Geometry

Date 2026-06-27. Agent: survey for a beatable, exactly-verifiable, NON-OWNED finite point-configuration
problem a SAMPLE-LIMITED smart-search fleet (dozens-to-hundreds of LLM proposals + exact verification)
could contribute a record/witness to in weeks. Web-verified throughout; KNOWN vs CLAIMED flagged.

---

## EXCLUSIONS established up front (web-verified owned/saturated — do NOT pursue)

These eat most of the "obvious" geometry long tail. Verified this session:

- **Heilbronn triangle problem — ALL containers (square, triangle, disk, convex region).** OWNED twice over:
  (a) AlphaEvolve / Novikov-Georgiev-Gómez-Serrano-Tao-Wagner 2025 ("Mathematical exploration and discovery
  at scale", arXiv:2511.02864) explicitly improved n=11 in unit triangle to ≥0.0365, n=13 convex to ≥0.0309,
  n=14 convex to ≥0.0278; (b) Erich Friedman's "Packing Center" cultivates the small-n tables for square/
  circle/triangle/convex. Also a 2026 MIP exact-coordinates paper (arXiv:2603.11107). DEAD.
- **Point packings minimizing max/min distance ratio (optimal spread/dispersion).** Explicitly an AlphaEvolve
  target ("packing N points in a shape to minimize the ratio of max and min distance"). DEAD.
- **Circle/shape packing into containers, polygon-in-polygon packing.** AlphaEvolve (26 circles in unit
  square sum-of-radii 2.635; 11 hexagons; generic polygon packing) + Packomania + Friedman. Heavily
  cultivated; FLOPS/global-optimization bound. DEAD for sample-limited.
- **Kissing numbers (small dim).** AlphaEvolve improved dim-11. Specialist-owned elsewhere. DEAD.
- **no-3-in-line on the n×n grid (does 2n fit?).** Now SAT-OWNED: Marijn Heule (CMU) found solutions for
  all n ≤ 70 in June 2026 (n=70 on Jun 17, n=72 Jun 25); smallest open case pushed to n=61→beyond.
  Plus CSP/constraint-programming papers 2026 (arXiv:2602.07751). This is exactly the "avoid Heule/SAT
  turf" warning. DEAD.
- **Empty convex hexagon (largest 6-hole-free set).** SETTLED + formally verified: h(6)=30 proven, "Formal
  Verification of the Empty Hexagon Number" (arXiv:2403.17370, SAT/Lean). Max 6-hole-free set = 29 (Overmars),
  now closed. DEAD as an open record.
- **Moving sofa, finite-field Kakeya/Nikodym sets, equidistant-vertex polygons, IMO-2024 tiling.** All
  AlphaEvolve repository problems (per Tao's 2025-11-05 blog enumeration). DEAD.
- **Erdős unit-distance / distinct-distance configs.** AI-disproved unit-distance result May 2026 (Kalai
  blog); distance problems are now a hot AI-attack target. Crowded. AVOID.

Net: the "famous" geometry records are swept. The surviving target must be a point-configuration problem
the packing-record specialists, AlphaEvolve, AND the SAT crowd all skipped. Found one cleanly.

---

## CANDIDATE 1 (TOP PICK) — Maximum acute set in the cube {0,1}^n

**Precise statement.** A set S ⊆ {0,1}^n (vertices of the n-cube, viewed in R^n) is *acute* if every angle
∠PQR determined by three distinct points P,Q,R ∈ S is strictly acute — equivalently, NO right angle and
NO obtuse angle occurs. a(n) = max |S|. Verification is pure integer arithmetic:
S is acute  ⟺  for every ordered triple of distinct P,Q,R:  (P−Q)·(R−Q) > 0  (strictly positive integer).
(Perpendicular ⟺ dot product = 0, forbidden; obtuse ⟺ negative, forbidden.) O(|S|³·n) integer ops — a few
hundred points checkable in milliseconds, exactly, by anyone. **This is OEIS A089676.**

**Current state (web-verified, OEIS A089676, last edited May 30 2026):**
- EXACT values known only through n=10:  a(0..10) = 1, 2, 2, 4, 5, 6, 8, 9, 10, 16, 17.
  (a(9)=16 and a(10)=17 are the hardest exact ones; a(10)=17 proven optimal by combinatorial search,
   Cariboni 2017, full enumeration in A289972.)
- For n = 11..15 ONLY LOWER BOUNDS are known, and they are the live records:
  **a(11) ≥ 24, a(12) ≥ 32, a(13) ≥ 33, a(14) ≥ 64, a(15) ≥ 128.**
- Source/method of these records: **D. Kamenetsky, 2018** (a(11–14)); a(15) Kamenetsky & Chubenko 2018 —
  via HEURISTIC numerical search (explicit witnesses are attached to the OEIS entry, file a089676_1.txt;
  I downloaded and inspected all five). For n>15 only Harangi's theoretical lower bounds (Table 3).
- These records have **stood since 2018 with no improvement through June 2026** (verified: no later
  construction paper; the 2018 MIT-PRIMES report Karnik corroborates a(11)≥24 via a *partial* search).

**Why sample-limited-friendly (this is the crux):** The problem's own literature says naive search fails.
Randriambololona (OEIS comment, Israel J. Math 2013): his algebraic-geometry/coding construction beats the
probabilistic method, and "for large n, naive computer search will have exponentially small chance to find
optimal configurations." So this is a **STRUCTURE/REASONING bottleneck**, not a FLOPS bottleneck — exactly
the regime where LLM-proposed *structured* constructions (linear codes, recursive products a(k+2m) ≥
a(k)·a(m), separating-system / (2,1)-separating-system encodings, near-orthogonal {0,1} designs) can beat a
brute heuristic. The search space {0,1}^11 has only 2048 vertices; a candidate set is ~25 of them — small,
human-legible, mutate-friendly. The objects are tiny binary matrices a fleet can emit as data and an exact
checker can score and rank.

**Concrete verifiable contribution.** Beat any one of the standing lower bounds — e.g. exhibit an acute set
of size 25 in {0,1}^11 (improving a(11) ≥ 24), or 34 in {0,1}^13 (improving a(13) ≥ 33). A new witness is a
plain 0/1 matrix; verification is the integer dot-product check above; it updates OEIS A089676 immediately.
**The a(13) ≥ 33 record looks softest** — note the irregularity a(12)≥32 then a(13)≥33 is only +1 while
a(14) jumps to 64; the multiplicative bound a(13) ≥ a(3)a(5) = 24 is weak, so 33 is likely far from optimal
and a clever (e.g. code-based or product) construction has real room. Even a +1 improvement is a genuine,
citable OEIS update.

**Novelty / owned status (BRUTAL).** Clean.
- NOT in AlphaEvolve's 67-problem repository (their geometry = packing/Heilbronn/kissing/sofa/Kakeya/Nikodym;
  no acute-angle or separating-system problem). Verified against Tao's blog enumeration + DeepMind repo.
- NOT in Friedman's Packing Center / Packomania (those are shape-packing-into-containers; acute sets are not
  a packing problem and do not appear). Verified.
- NOT SAT-owned (Heule's geometry work is no-3-in-line; no SAT acute-set table exists).
- Active researchers are theorists (Bevan 2006, Harangi 2011, Ackerman–Ben-Zwi 2009, Randriambololona 2013,
  Gerencsér–Harangi) chasing ASYMPTOTIC exponential constants, plus one hobbyist (Kamenetsky 2018) who set
  the small-n lower-bound records by heuristic. **No specialist is actively pushing the n=11–15 finite
  records.** That is the gap.

**Risks (see adversarial section):** equality vs lower-bound; whether the records are quietly improvable by
trivial random search (NO — see below).

---

## CANDIDATE 2 — Maximum acute set in general R^d (free coordinates, not the cube)

**Statement.** f(d) = max number of points in R^d with all angles strictly acute. KNOWN exactly:
f(1)=2, f(2)=3, f(3)=5 (proven), f(4)=? — the exact value is open for d ≥ 4. Best general lower bound
2^{d-1}+1 (Gerencsér–Harangi); upper bound < 2^d (Danzer–Grünbaum 1962). For d=4, lower bound 9 is recorded
(a "Ukraine enthusiast" example per the literature) but exact f(4) is unsettled.

**Verifiable contribution.** A record acute set in R^4 or R^5 with explicit rational/algebraic coordinates,
or proving a tight small value. Verification: exact dot-product sign over an algebraic number field (still
exact, but no longer pure integers — needs interval/exact-algebraic arithmetic, which this project has).

**Why sample-friendly.** Small d, structured constructions (perturbed cube vertices, simplex-based). But
**weaker than C1**: continuous coordinate search drifts toward FLOPS/optimization, and verification needs
exact-algebraic not integer arithmetic. Novelty OK (not AlphaEvolve/Friedman/SAT), but the cube version (C1)
is strictly cleaner to verify and to mutate. **Rank below C1.**

---

## CANDIDATE 3 — Maximum k-holes in a point set with NO (k+1)-hole (small k=6,7)

**Statement.** h_k(n) = max number of empty convex k-gons (k-holes) over n-point general-position sets that
contain NO empty (k+1)-gon. Fresh 2026 paper (arXiv:2606.05721) proves lower bound exponent ⌊k/3⌋, conjectures
⌈k/3⌉; the gap is open for every k ≥ 6. Small-case extremal configurations (best constructions maximizing
6-holes with no 7-hole, on a fixed modest n) are finite and exactly checkable (convex-position / emptiness
tests on integer or rational coordinates).

**Verifiable contribution.** A construction beating the current best count of k-holes for a specific small
(k,n), narrowing the exponent gap empirically. Witness = integer point set; verification = combinatorial
(enumerate empty convex polygons — exact).

**Why sample-friendly + risk.** Genuinely recent (June 2026), no specialist sweep yet, structure-bottleneck
(Horton-type recursive constructions are reasoning-friendly). BUT this is adjacent to the empty-polygon /
Horton-set world where SAT (Heule/Scheucher) is extremely active and could move in; and "best known count"
baselines are not as cleanly tabulated/citable as an OEIS sequence. Higher novelty-risk than C1. **Rank below
C1; keep as a live backup precisely because it is brand-new.**

---

## (Surveyed, REJECTED) — for the record
- **no-3-in-line (square grid & 3D):** SAT-owned (Heule, n≤70, June 2026). DEAD.
- **Heilbronn / packing / distance-ratio / kissing:** AlphaEvolve + Friedman + Packomania. DEAD.
- **Empty hexagon (6-hole-free max):** settled & formally verified (=29 / h(6)=30). DEAD.
- **General-position subset selection (max in-general-position subset of a fixed point set):** NP-hard and
  APX-hard, but the "record" is an approximation-ratio theorem, not a tabulated small-case witness — no clean
  beatable record-table. Skip.
- **Distinct-distance configs / unit-distance:** hot AI-attack zone (unit-distance AI-disproved May 2026).
  AVOID per the analysis-bound + crowding rule.

---

## RANKING

1. **Acute set in the cube {0,1}^n (OEIS A089676), beat a(11..15) lower bound — esp. a(13) ≥ 33.**
   Best on every axis: integer-exact verification (trivial, anyone-checkable), tiny mutable binary objects,
   explicit current witnesses to seed mutation, records frozen since 2018, structure-bottleneck (literature
   says naive search fails) so LLM-reasoning has a real edge, and an OEIS sequence makes any improvement an
   immediate citable contribution. Clean novelty vs AlphaEvolve / Friedman / Packomania / SAT.
2. **Max k-holes, no (k+1)-hole, small (k,n) (arXiv:2606.05721).** Brand-new (June 2026), unswept, but
   SAT-adjacent and weaker baseline tabulation.
3. **Acute set in R^4/R^5 (free coords).** Good novelty, but continuous + exact-algebraic verification; C1
   dominates it.

---

## ADVERSARIAL VERIFICATION of the top pick (try to KILL acute-set-in-cube)

**Attack 1 — "Secretly owned / records already improved since 2018?"**
Checked: searched 2019–2026 for any acute-set construction improving a(11–15); found none. The only later
touch is Harangi's asymptotic Table 3 (large n) and the 2018 MIT-PRIMES report that merely *corroborates*
a(11)≥24. OEIS A089676 still lists Kamenetsky's 2018 values as best; the page was edited May 30 2026 with no
record change. NOT secretly owned. SURVIVES.

**Attack 2 — "Secretly FLOPS-bound — just throw random {0,1} vectors at it?"**
This is the strongest attack and it FAILS in the project's favor: Randriambololona proved his best
constructions beat the probabilistic/random method and stated explicitly that naive computer search has
"exponentially small chance to find optimal configurations" at large n. Kamenetsky's records came from a
*heuristic* (not exhaustive, not random brute force) — meaning a better-reasoned heuristic/structured
construction is the established way to win here, not more FLOPS. The space is also genuinely small (2^11=2048
candidate vertices, ~25 chosen), so it is NOT a giant-search-space FLOPS regime either. The bottleneck is
*structure* (codes, recursive products, separating systems) — exactly the LLM-fleet edge. SURVIVES — in fact
this attack is the positive case.

**Attack 3 — "Needs floating point, not exact verification?"**
No. Vertices are 0/1; (P−Q)·(R−Q) is an integer; acuteness ⟺ all such integers > 0. Zero floating point,
zero tolerance issues, fully reproducible. SURVIVES decisively.

**Attack 4 — "Not actually open / would a referee care?"**
a(11) and beyond are explicitly listed as LOWER BOUNDS in a live OEIS sequence edited weeks ago — by
definition open. Any improvement (even +1) updates A089676 with a verifiable witness and is a recognized
(modest) contribution; the sequence is connected to a real literature (Erdős–Füredi, Bevan, Harangi,
Randriambololona). It is "modest but real," which is exactly the FunSearch target bar. SURVIVES.

**Attack 5 — "Is the smallest-effort win actually proving a(11)=24 EXACTLY (an upper bound), which IS
FLOPS/SAT-hard?"** Correct caveat: proving EQUALITY (matching upper bound) for a(11) is hard (Cariboni needed
heavy search even for a(10)=17) and is NOT our target. Our target is the LOWER-bound side: a bigger witness.
That side is pure construction + cheap exact check — no upper-bound/optimality proof required. So scope the
goal as "improve a lower bound with a witness," not "settle the value." SURVIVES with scope discipline.

**Residual honest risk:** the records may simply be near-optimal and stubborn (a(11) could genuinely be 24 or
25, leaving almost no room). Mitigation: target the SOFTEST record first — a(13) ≥ 33, where the +1 jump from
a(12)≥32 and the weak multiplicative bound strongly suggest the true value is well above 33; also a(12)≥32 vs
the exact a(11)... pattern leaves room. If a focused fleet can't beat 33 in a pilot, that is itself a fast,
cheap negative (small objects, instant verification) — low downside.

---

READY FOR JUDGING.

**Verdict: REAL target — maximum acute set in the cube {0,1}^n (OEIS A089676).** Improve a standing 2018
lower bound (most promising: a(13) ≥ 33, also a(11) ≥ 24 / a(12) ≥ 32) with an explicit 0/1 witness verified
by an integer dot-product check. Non-owned (skipped by AlphaEvolve, Friedman/Packomania, and SAT solvers),
exactly + trivially verifiable, structure-bottlenecked (literature says naive search fails → LLM-reasoning
edge), tiny mutable objects, immediate OEIS-citable contribution. Realistic sample-limited win in weeks; a
failed pilot is a cheap, clean negative.

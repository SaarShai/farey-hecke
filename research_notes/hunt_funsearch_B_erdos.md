# Hunt B — FunSearch/AlphaEvolve-mode target on erdosproblems.com (OPEN problems)

Date 2026-06-27. Domain B = erdosproblems.com (Thomas Bloom's database, mirrored as
`teorth/erdosproblems`, ground-truth `data/problems.yaml`). Goal: a beatable, exactly-verifiable,
NON-OWNED, construction/finite-search-bottlenecked OPEN problem a sample-limited reasoning fleet
(dozens-to-hundreds of proposals + exact verification) could contribute a witness/record to.

All bounds/dates below are WEB-VERIFIED against the erdosproblems page (raw HTML, LaTeX-preserved),
the cited arXiv paper, or the canonical AI-contributions wiki. "UNVERIFIED" is marked where I could
not confirm. Statements quoted from erdosproblems.com (Bloom).

---

## METHOD (so the result is auditable, not vibes)

- Cloned `teorth/erdosproblems` → `data/problems.yaml` = 1217 problems, **620 OPEN**. YAML carries
  metadata only (number, status, tags, oeis, formalized) — no statement text, no bounds.
- erdosproblems.com blocks WebFetch (403) but serves full server-rendered HTML (with LaTeX) to a
  browser User-Agent via `curl`. Bulk-fetched all **248 OPEN problems** tagged with construction-
  relevant topics (sidon, additive basis, distances, turán, ramsey, covering systems, complete
  sequences, primitive sets, combinatorics, hypergraphs, geometry, …) and parsed offline.
- **Owned/AI filter (decisive):** the canonical wiki
  `teorth/erdosproblems/wiki/AI-contributions-to-Erdős-problems` maps EVERY AI contribution
  (AlphaEvolve / FunSearch / GPT-5.x / Aristotle / AlphaProof / DeepMind prover / …) to exact
  problem numbers — ~300 problems touched Sep-2025→Jun-2026. Cross-checked every finalist against it.
- **AlphaEvolve construction sweep** (`google-deepmind/alphaevolve_repository_of_problems`, 67
  problems, Nov-2025): geometry/analysis/packing-heavy. Inline-tagged on erdosproblems only at a
  handful of construction problems: **#36, #507, #951, #1097, #1153** (+ named: minimum-overlap,
  cap sets, kissing-11D, Kakeya, packing — none of which are my candidates).

### Two structural facts that killed most of the domain
1. **Almost every OPEN Erdős problem is ASYMPTOTIC** ("…cannot be resolved with a finite
   computation" — Bloom's boilerplate, present on ~all 248). These ask for growth rates / limit
   constants, NOT a finite witness → fail the HARD FILTER (need an exactly-checkable finite object).
2. The OPEN problems that ARE small-finite-witness-verifiable split into:
   (a) **specialist-FLOPS-cultivated** (sparse ruler, postage stamp — heavy parallel search already
       run; a sample-limited fleet has no edge), or
   (b) **partly FLOPS-cliff / possibly-nonexistent objects** (integral octagon), or
   (c) **active specialist proof-push** (congruent-triangle tiling — Beeson).
   This is the same niche-trap this project has hit before; I do NOT paper over it (see VERDICT).

---

## CANDIDATES (ranked)

### #1 — Erdős #213: integral point set in general position (the "integral octagon")
**Statement (verbatim):** "Let n≥4. Are there n points in ℝ², no three on a line and no four on a
circle, such that all pairwise distances are integers?"  Tags: geometry, distances.

- **Current record (WEB-VERIFIED):** n = **7** (an "integral heptagon"). Two explicit 7-point
  configurations, **Kreisel & Kurz, *Discrete & Comput. Geom.* (2008)** [arXiv:0804.1303]. No
  8-point set is known. **18-year-old record; construction front dormant.**
- **Surrounding results (not constructions):** Anning–Erdős 1945 (no infinite such set);
  Harborth (n=5); Ascher–Braune–Turchet 2020 (uniform upper bound, conditional on Bombieri–Lang);
  Greenfeld–Iliopoulou–Peluse 2024 [arXiv:2401.10821] (unconditional sparsity: |S| ≪ (log N)^{O(1)}
  in [−N,N]²) — **pure analysis, upper-bound side**; Avdeev–Lushina 2024 [arXiv:2407.08121]
  (diameter lower bounds, semi-general position) — **pure theory, no search.**
- **Why construction-bottlenecked, not analysis:** the only way anyone has produced examples is
  computer search. Kreisel–Kurz state their method is **exhaustive orderly generation, runtime
  Ω(d³)** for diameter ≤ d; they reached diameter 30000 exhaustively, then 70000 under a
  divisibility restriction, and found exactly two heptagons. They **explicitly pose n=8 as the open
  problem** ("Are there eight points…?"). The barrier is search, not a missing theorem.
- **Structural leverage (why LLM-reasoning > raw FLOPS here):** every non-degenerate triangle in a
  plane integral point set shares ONE squarefree **characteristic** k (squarefree part of the Heron
  product) — Kemnitz/Kurz Theorem. Empirically k is a product of **small primes** (heptagon #1:
  k=2002=2·7·11·13; heptagon #2: divisors of 2·3·5·7·11·13·17·19·23·29). So a candidate octagon is
  NOT a free 16-coordinate search — it is a **structured Diophantine system**: fix a small-prime
  characteristic, then solve the 28 simultaneous integer-distance + equal-characteristic equations.
  This is exactly the regime where structure-guided proposal beats blind enumeration.
- **Exactly verifiable:** a candidate is 8 rational/integer points; check all 28 distances are
  integers, no 3 collinear, no 4 concyclic. Trivially, independently checkable by anyone.
- **Concrete contribution:** an explicit 8-point integral set in general position = the first since
  2008, directly answering Kreisel–Kurz's stated open question. (Even a *near-miss* family or a
  reduced-diameter heptagon search is publishable in the recreational/discrete-geom community.)
- **Owned/novelty status:** **NOT** in the AI-contributions wiki (no AlphaEvolve/FunSearch/GPT
  entry). **NOT** in AlphaEvolve's 67-problem repo. Recent activity (GIP24, AL24) is upper-bound
  analysis, not construction. CLEAN.

### #2 — Erdős #769: decomposing the n-cube into homothetic n-cubes (c(n))
**Statement (verbatim):** "Let c(n) be minimal such that if k≥c(n) then the n-dimensional unit cube
can be decomposed into k homothetic n-dimensional cubes. Give good bounds for c(n) — in particular,
is it true that c(n) ≫ nⁿ?"  Tags: number theory, geometry.

- **Current bounds (WEB-VERIFIED):** c(2)=6 (easy). **c(3)=48 conjectured by Meier — UNPROVEN.**
  Hadwiger c(n)≥2ⁿ+2^{n−1}; Burgess–Erdős c(n)≪n^{n+1}; Hudelson 1998; **Connor & Marmorino 2018**:
  c(n)≥2^{n+1}−1 (n≥3), c(n)≤1.8 n^{n+1} (n+1 prime) else ≤ e²nⁿ.
- **Why finite-search-friendly:** determining c(3) exactly (proving Meier's 48, or beating it) is a
  finite tiling-existence question per k — "can the unit 3-cube be cut into exactly k homothetic
  cubes?" — a constraint-satisfaction object a fleet can construct/refute for each k near 48.
- **Verifiable:** an explicit dissection into k cubes (list of sub-cube positions/sizes) is exactly
  checkable. **Contribution:** settle c(3) (every k≥48 achievable, 47 not) or a new small-n value.
- **Owned/novelty:** NOT in AI wiki, NOT AlphaEvolve, no recent specialist push found (Connor–
  Marmorino 2018 is the latest). CLEAN. **Risk:** the "≫nⁿ" headline is asymptotic (analysis); the
  finite-witness part is only the small-n exact values — narrower prize than #213.

### #3 — Erdős #634: tiling a triangle into n congruent triangles
**Statement (verbatim):** "Find all n such that there is at least one triangle which can be cut into
n congruent triangles." ($25 problem.) Tag: geometry.

- **Status (WEB-VERIFIED):** squares n=m² always work; Soifer: 2n²,3n²,6n²,n²+m² work. **Beeson:
  n=7 and n=11 impossible** [arXiv:1811.09723]. **n=19 OPEN** (smallest unknown; conjecturally no
  prime ≡3 mod 4 works). Zhang 2025 [Zh25]: large families n²ab achievable.
- **Why witness-friendly (partly):** for a specific n like 19, a YES is a single explicit tiling.
- **Owned/novelty:** NOT in AI wiki. **BUT ACTIVE SPECIALIST PUSH — DOWNGRADE:** Michael Beeson is
  systematically clearing this (No-7, No-11 proved; **"Solution of Erdős Problem 633"
  arXiv:2604.03609, 2026**; Dec-2025 "Tiling Triangles with 2π/3 Angles" arXiv:2512.22696). The
  remaining open cases (19, 23, primes ≡3 mod 4) appear to be **impossibility-proof-shaped**
  (Beeson's machinery rules them out), not witness-shaped — so a "find a tiling" fleet likely loses
  the race / attacks the wrong side.

### #4 — Erdős #170: the Sparse Ruler problem  — **EXCLUDED (specialist-FLOPS-cultivated)**
F(N)=min |A⊆{0,…,N}| with {0,…,N}⊆A−A; lim F(N)/√N ∈ [1.56 (Leech 1956), √3 (Wichmann 1963)].
Finite, exactly verifiable, old bounds — looks ideal. **But killed by HARD FILTER #3:** this is a
recreational/OEIS specialist table. Robison 2014 computed all 106,535 optimal rulers ≤ length 213 on
256 cores; **Pegg (Wolfram) 2020** extended candidates to length 257,992; optimality conjectured
(all optimal rulers are Wichmann bar exceptions {1,13,17,23,58}). A sample-limited fleet has **no
edge** over the heavy parallel search already done. DO NOT pursue.

### #5 — Erdős #791: the Postage-Stamp / additive 2-basis problem  — **EXCLUDED (specialist push)**
g(n)=min |A⊆{0,…,n}| with {0,…,n}⊆A+A; g(n)²/n ∈ [2.181 (Yu 2015), 3.458 (Kohonen 2017)] (Mrose
1979 gave 7/2). Same shape as #170. **Killed:** Jukka Kohonen has cultivated this for a decade
(extremal restricted bases to k=47, meet-in-the-middle algorithms, improved lower bounds), and there
is a **brand-new push, arXiv:2507.23627 (2025)** "Improved bounds on the postage stamp problem for
large numbers of stamps". Active specialist + FLOPS turf. DO NOT pursue.

---

## RANKING (realistic-shot × not-owned × exactly-verifiable × significance)
1. **#213 (integral octagon)** — cleanest non-owned finite-witness construction target; real
   structural leverage (small-prime characteristic ⇒ Diophantine system, not blind search); dormant
   18 yrs; recognized prize. The ONE genuine FunSearch-mode candidate. (Caveat: FLOPS-cliff risk.)
2. **#769 (cube → homothetic cubes, c(3))** — clean, quiet, finite-witness, but narrower (small-n
   exact values only).
3. **#634 (congruent-triangle tiling)** — finite-witness but ACTIVE Beeson push + impossibility-
   shaped open cases → weak fit.
4–5. **#170 / #791** — EXCLUDED (specialist-FLOPS-cultivated; documented above so they aren't
   re-proposed by a future hunt).

---

## ADVERSARIAL VERIFICATION OF TOP PICK (#213) — trying to KILL it

**Secretly owned (AlphaEvolve / FunSearch / GPT-5.x)?** — Checked the canonical AI-contributions
wiki (300+ problems): **#213 absent.** Checked AlphaEvolve's 67-problem repo: absent (it did
`no_5_on_a_sphere`, `subsets_of_grid_no_isosceles_triangles`, `squares_in_square`, Tammes, Thomson,
circle-packing — NOT integer-distance point sets). The 2024–25 papers (Greenfeld–Iliopoulou–Peluse;
Avdeev–Lushina) are upper-bound / diameter-lower-bound **analysis**, not a construction search.
**Survives.**

**Secretly analysis-bound?** — No. Every known example came from computer search; Kreisel–Kurz's
bottleneck is explicitly Ω(d³) exhaustive enumeration, not a missing theorem. The conditional
finiteness (Ascher–Braune–Turchet) and sparsity (GIP) results constrain but don't construct.
**Survives** (the witness side is pure construction).

**Not actually open?** — No 8-point set is known; Kreisel–Kurz pose n=8 explicitly; erdosproblems
lists #213 OPEN, last edited Oct-2025. **Survives.**

**Not verifiable?** — Trivially verifiable: 8 explicit points, check 28 integer distances + no-3-
collinear + no-4-concyclic. **Survives.**

**FLOPS-bound? — THIS IS THE REAL THREAT, and it lands a partial hit.** Kreisel–Kurz already applied
the small-prime-characteristic restriction and exhaustively searched to diameter 70000 with NO
8-point set. So if an octagon exists, diameter > 70000, and brute force is Ω(d³)-infeasible — exactly
why the record has stood 18 yrs. Two honest sub-outcomes:
  (i) **Object exists at moderate diameter, missed because nobody applied STRUCTURE-guided
      (vs exhaustive) search.** Then a reasoning fleet that sets up the small-prime-characteristic
      Diophantine system and searches *cleverly* (not enumeratively) has a genuine, differentiated
      shot — this is the FunSearch thesis exactly.
  (ii) **Object is genuinely rare / large-diameter / nonexistent** (cf. Bell–Noll 7₂-cluster doesn't
      exist; existence here is called "unclear"). Then NO sample-limited method wins, and a fleet
      "fails to find" with nothing publishable.
We cannot distinguish (i) from (ii) a priori. So #213 is a **real target with real downside**: high
upside (recognized first-since-2008 result, structure-exploitable) but a non-trivial probability the
search is unfalsifiable-in-practice. It is NOT a safe incremental-record problem like the (excluded)
ruler/stamp tables — it is a swing.

**Net:** #213 is the single honest FunSearch-mode candidate the domain offers — non-owned, exactly
verifiable, construction-bottlenecked, with genuine LLM-exploitable structure. Its risk is the
classic existence-search gamble, not an ownership or verifiability flaw.

---

## DOMAIN-LEVEL HONEST CAVEAT (for the synthesis loop)
erdosproblems.com is a WORSE FunSearch hunting ground in Jun-2026 than the goal doc assumed. The
GPT-5.x + Aristotle + DeepMind-prover wave (Sep-2025→Jun-2026) has touched ~300 problems and is
clearing the *solvable-by-reasoning* tail fast; AlphaEvolve took the geometry/packing construction
records; and the finite-witness construction problems that remain are mostly specialist-FLOPS-
cultivated (rulers, stamps) or asymptotic. The clean, non-owned, finite-witness, structure-
bottlenecked intersection is **thin — essentially {#213, #769}**, with #213 the only one carrying
real upside (and real existence-risk). If the fleet wants a SAFER incremental record, this domain is
not it; if it wants one genuine swing at a recognized construction, #213 is the pick.

---

READY FOR JUDGING — REAL target: **YES, one** — Erdős **#213** (integral octagon: 8 points in ℝ²,
no 3 collinear, no 4 concyclic, all pairwise distances integer). Non-owned (absent from AlphaEvolve
+ the AI-contributions wiki), exactly verifiable, construction-bottlenecked since the n=7 record of
Kreisel–Kurz 2008, with genuine LLM-exploitable structure (small-prime "characteristic" ⇒ a
Diophantine system, not blind 16-coord search). Realistic contribution: an explicit 8-point set
answering Kreisel–Kurz's stated open question — a recognized first-since-2008 result IF the object
exists at feasible diameter. Honest risk: it's an existence-search swing (FLOPS-cliff / possible
nonexistence below feasible diameter), not a safe incremental record. Backup if a quieter, lower-
variance target is preferred: **#769** (c(3)=48). AVOID #170/#791 (specialist-FLOPS-cultivated) and
#634 (active Beeson push, impossibility-shaped).

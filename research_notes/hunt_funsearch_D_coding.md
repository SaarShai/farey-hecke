# FunSearch/AlphaEvolve target hunt — Domain D: coding theory / design theory / finite geometry

Date 2026-06-27. Mode: scope a beatable, exactly-verifiable, NON-OWNED open SMALL CASE that a
SAMPLE-LIMITED smart-search fleet (dozens-to-hundreds of LLM-reasoned proposals + exact
verification, NOT a million-eval DeepMind loop, NOT raw FLOPS) has a realistic shot at
contributing a record/witness to in weeks.

Method: 4 parallel survey agents (covering codes; A(n,d)/A(n,d,w) code records; caps/arcs/finite
geometry; designs/MOLS/difference-sets) + main-loop focused web-verification on every load-bearing
number. All bounds web-verified or marked UNVERIFIED. KNOWN vs CLAIMED kept distinct.

---

## CRITICAL CONTEXT — the turf is ALREADY being swept by LLM-fleets (read first)

This domain is the MOST contested for the FunSearch paradigm right now. Two direct competitors:

- **CPro1 — "Automated Discovery of Improved Constant Weight Binary Codes", arXiv 2603.00174
  (Feb 2026).** An LLM-fleet (OpenAI o4-mini, **4000 sampled C-program strategies**, 2 succeeded)
  improved A(n,d,w) lower bounds for **24** triples, n∈[18,35], d∈{6,8,10,12,16,18}. VERIFIED full
  Table-1 list (e.g. (22,8,9):280→292; (24,8,11):1288→1378; (28,8,10):1867→2028; (31,16,14):21→24*
  matching the upper bound). **They explicitly did NOT touch d=4.**
- **CPro1 design paper — "Using Code Generation to Solve Open Instances of Combinatorial Design
  Problems", arXiv 2501.17725 (Jan 2025).** Same method, **16 design types tested, 6 solved**:
  symmetric & skew weighing matrices, equidistant permutation arrays, packing arrays, balanced
  ternary designs, Florentine rectangles. **MOLS was NOT among the 6 solved (and not clearly among
  the 16 — UNVERIFIED which 10 failed).**

Implication: (a) the LLM-fleet method is PROVEN to produce real records in exactly this domain —
strong positive signal; (b) the freshly-swept slices (A(n,d,w) at d∈{6..18}, those 6 design types)
are now OWNED and must be avoided; (c) the OPEN frontier is what these two papers did NOT reach.

- **AlphaEvolve (DeepMind, arXiv 2506.13131, May 2025):** broad math/algorithm sweep (matrix mult,
  packing, autocorrelation, ~50 Erdős-type). VERIFIED: **no covering-code, MOLS, cap/arc, or
  design-existence result** surfaced in its public results repo. Coding theory was essentially
  untouched by AlphaEvolve itself (the coding-theory LLM-fleet work is CPro1, not DeepMind).

---

## CANDIDATES (ranked)

### #1 — Four MOLS of order 22  [N(22) ≥ 4 ?  ⇔  TD(6,22) exists ?]   ★ TOP PICK

- **Precise statement.** N(n) = max number of mutually orthogonal Latin squares of order n.
  KNOWN: **N(22) = 3** (three MOLS(22) constructed; even three mutually orthogonal *idempotent*
  LS(22) known). OPEN: does a **4th** exist, i.e. N(22) ≥ 4? Equivalent to existence of a
  **transversal design TD(6,22)**, equivalent to an OA(6,22). Upper bound: trivially N(22) ≤ 21;
  no proof forbids 4.
- **Current state + source (web-verified).** "22 remains the only value of n (apart from 4) for
  which three MOLS of order n are known but four are not" — standard MOLS references
  (Grokipedia/Handbook lineage). LibreTexts (Morris, *Combinatorics*, §16.2): existence of four
  MOLS(22) "is not known … an open problem, undetermined and unproven." TD(6,m) is KNOWN to exist
  for all m≥5 EXCEPT m∈{6,10,14,18,22}; of these, m=6 is genuinely impossible (no 2 MOLS(6), Euler),
  and **m=22 is the standout still-OPEN case** (14,18 are also open but smaller/more special). No
  resolution found in 2014–2026 search. Colbourn–Dinitz Handbook is the table-of-record; the recent
  curated table is "Implementing the MOLS Table for n up to 500" (MDPI Symmetry 16(12):1678, 2024).
- **Why a clever construction (not FLOPS) could move it.** This is the textbook "structure
  bottleneck, not raw search" case. Naïve exhaustive search over 22×22 LS arrays is astronomically
  large, so brute force is hopeless — meaning the record will come from a STRUCTURED construction,
  exactly what an LLM-reasoned fleet does: prescribe an automorphism group acting on the TD,
  search over **starter blocks / difference matrices / group-orbit unions** in the quotient (tiny
  search), or adapt the **separable-permutation-code** method below. The literature itself says "It
  is possible that four MOLS of order 22 could be obtained by the method in [ref], using a special
  kind of [construction]" — i.e. specialists believe a construction may exist and just hasn't been
  found.
- **Live precedent the fleet would imitate (web-verified).** "Improvements for lower bounds of
  MOLS of sizes 54, 96, 108" (arXiv 2412.00480, Nov 2024; Des. Codes Cryptogr. 2025) jumped
  **N(54): 5→8**, N(96): 9→10, N(108): 8→9, via **separable permutation codes** built from
  **isometry-group orbit representatives** (n=54,96) and a **(108,10,1) difference matrix** (n=108).
  Key fact: an (n,m)-separable (n,n−1)-permutation-array with r=n codewords ⇔ m MOLS(n). This is a
  small, group-structured search — and the authors **explicitly did NOT survey smaller orders**
  (14,18,20,22,26,28). The method is sitting there, unapplied to 22.
- **Why sample-limited-friendly.** The witness is TINY: two (or four) 22×22 Latin squares = ~484
  symbols each. Anyone can verify in seconds: check each is a Latin square, then check the overlay
  of every pair hits all 22² ordered symbol-pairs exactly once. The authors of 2412.00480 note
  verification is "a few lines of GAP or MAGMA." Non-specialist-checkable, no trust required.
- **Concrete verifiable contribution.** Exhibit **4 mutually orthogonal Latin squares of order 22**
  (equivalently a TD(6,22) / OA(6,22)). That single witness SETTLES a named, decades-old open case
  in the Handbook of Combinatorial Designs — a genuine (modest-but-real) record.
- **Novelty/owned status (brutal).** NOT in CPro1 (neither paper tackled MOLS). NOT in AlphaEvolve.
  NOT FLOPS-saturated (full exhaustion is infeasible → it has resisted *because* it needs
  structure). It is the single most-pointed-at small open MOLS case in the literature. Real risk
  documented in the kill section below.

### #2 — N(18) ≥ 4 and N(26) ≥ 5  [neighbouring stuck small composite MOLS orders]

- **Precise/current (web-verified canonical Colbourn–Dinitz small-order values).** N(14)=4 (known),
  N(18)=3, N(20)=4, N(21)=5, N(22)=3, N(24)=6, N(26)=4, N(28)=5 — all vs upper bound n−1, all
  long-standing lower bounds. TD(6,18) is in the SAME open-exception set {6,10,14,18,22} as 22, so
  **N(18) ≥ 4 (TD(6,18))** is also open. N(26)=4 vs upper 25 is a wide soft gap.
- **Why moveable / sample-friendly / contribution.** Same separable-permutation-code / difference-
  matrix / prescribed-automorphism machinery as #1; same tiny exactly-checkable witnesses (18×18,
  26×26). A 4th MOLS(18) settles another open exception; a 5th MOLS(26) is a clean lower-bound
  record. Slightly less "famous" than 22, so lower significance, but more shots on goal.
- **Owned status.** Same un-swept frontier as #1. N(20)→4 came from a *specific* construction
  (Abel, "Four MOLS of orders 20,30,38,44", JCTA 1993) — i.e. these small-order bounds historically
  move by one construction at a time, the beatable pattern. UNVERIFIED whether anyone improved
  18/26 post-2010 (no such paper surfaced).

### #3 — Constant-weight binary codes at d=4  [A(n,4,w), the slice CPro1 skipped]

- **Precise/current (web-verified, Brouwer's table aeb.win.tue.nl/codes/Andw.html).** A(n,4,w) =
  max number of w-subsets of [n] with pairwise intersection ≤ w−2 (a packing). A(n,4,3),A(n,4,4)
  determined; many w≥5 entries are LOWER-bound-only / soft ("s"=shortening, "p"=packing-derived),
  e.g. A(22,4,5)≥1386, A(23,4,5)≥1771, A(26,4,5)≥2816, A(25,4,6)≥7787 (upper bounds often absent).
- **Why interesting / why caution.** CPro1 (2603.00174) **deliberately excluded d=4** — genuinely
  un-swept by the LLM-fleet. The catch for SAMPLE-LIMITED search: these codes are LARGE (1000s of
  codewords), so the "small object" advantage is weaker, and d=4 packings are tightly linked to
  Steiner systems S(2,w,n) where the best constructions are already very strong. Verification is
  still cheap (O(M²) pairwise check). Better as a fallback than the lead.
- **Owned status.** Brouwer's table is decades-cultivated; many d=4 lower bounds are Steiner-optimal
  (dead). The live sub-slice is soft "s"/"p" entries at w=5,6 — but the gap-vs-upper is often
  unproven rather than known, so "beating" requires also pinning the comparison. Medium-risk.

### #4 — Football-pool ternary covering codes  K₃(n,1)  [classic, stale, partly solver-owned]

- **Precise/current (web-verified).** K_q(n,R) = min size of length-n q-ary code, covering radius R.
  K₃(9,1) ≤ **1269** (Östergård–Wassermann, "An improved upper bound for the football pool problem
  for nine matches", JCTA 2003; automorphism group order 648) with a substantial lower-bound gap.
  Lower bounds recently pushed by SDP (arXiv 2504.01932, Apr 2025); upper bounds by MILP (arXiv
  2310.01883, 2023).
- **Why caution (the kill).** The UPPER bounds — the side a construction-fleet would improve — now
  largely come from **MILP / SAT / simulated annealing**, i.e. they are **solver-owned**, not weak
  ad-hoc constructions. K₃(9,1)≤1269 has stood **~20+ years**, signalling genuine hardness. Mid-range
  n (8–10) is too big for brute force yet too small for asymptotics. Verification is exact
  (cover all 3ⁿ vectors) but the record itself is hard to wrest from solvers. WEAK fit.

### #5 — Caps/arcs in PG(k,q) / smallest complete caps PG(4,q)  [finite-geometry graveyard]

- **Current (web-verified).** Smallest complete arcs m(2,q) exhaustively SOLVED for all q ≤ 160,001
  (+ sporadic to 430,007) by the Bartoli–Davydov–Faina–Marcugini–Pambianco group. Small-q caps in
  PG(k,q), k≤5, q≲20 fully CLASSIFIED. Cap-set AG(n,3) is FunSearch turf (n=8 swept).
- **Why dead.** Where a witness is non-specialist-verifiable (small q), exhaustive search already
  OWNS it. Where it's open (PG(3,q)/PG(4,q), q≳17), gaps are a few points and verification needs
  domain machinery. Least-bad slot: smallest complete cap in PG(4,q), q∈{17,19,23} — but low
  significance + specialist-verification overhead. DROP.

---

## RANKING (realistic-shot × not-owned × exactly-verifiable × significance)

| Rank | Target | Beatable by smart-search? | Owned? | Verifiable? | Significance |
|---|---|---|---|---|---|
| **1** | **4 MOLS of order 22 (TD(6,22))** | **Yes — structure-bottleneck, brute force infeasible** | **No** (not CPro1/AlphaEvolve/FLOPS) | **Yes, trivially** | **Real — named open case** |
| 2 | N(18)≥4, N(26)≥5 | Yes — same machinery | No | Yes, trivially | Modest |
| 3 | A(n,4,w) CW codes | Partly (large objects) | d=4 un-swept; many Steiner-tight | Yes (O(M²)) | Modest |
| 4 | K₃(n,1) football pool | Weak — upper bounds solver-owned | Partly (MILP/SAT) | Yes | Modest, hard |
| 5 | Caps/arcs PG(k,q) | No — exhausted or deep | Yes (exhaustive) | Only where owned | Low |

---

## ADVERSARIAL VERIFICATION of TOP PICK (#1: four MOLS of order 22) — trying to KILL it

1. **Is it already settled?** Searched 2014–2026: no construction of 4 MOLS(22) and no impossibility
   proof found. LibreTexts and standard refs (2024–2026) still state it OPEN. → SURVIVES (as of
   web-verifiable record; flagged: I could not access the live 2024 MDPI table behind 403, so a
   2024–2026 closure is *possible but unfound* — treat as KNOWN-open, re-check the MDPI table and
   Colbourn–Dinitz before any pilot).
2. **Is it secretly impossible?** No. TD(6,22) is in the *undetermined* exception set, NOT the
   proven-nonexistent set; only TD(6,6) among small cases is truly impossible. The N(22) ≤ n−4 style
   remark is not a proof barring 4. → SURVIVES.
3. **Is it FLOPS/SAT-owned?** This is the REAL risk, two-sided:
   - Against owned: full exhaustive search over 22×22 arrays is infeasible, so it is NOT settled by
     raw brute force → the door is open for a structured witness (good).
   - For owned: it has been attacked by strong constraint/integer-programming campaigns
     (cf. "Integer and Constraint Programming Revisited for MOLS", arXiv 2103.11018) and by the
     field's best constructors (Abel, Colbourn, Todorov) for decades **without success**. So it may
     be genuinely HARD — possibly 4 MOLS(22) is rare or needs an automorphism group nobody has tried.
     A few-hundred-proposal fleet is NOT guaranteed to find it. **This is the honest central caveat:
     high-value, real, un-owned — but NOT a high-probability quick win.** It is a swing, not a tap-in.
4. **Can a non-specialist verify the witness?** YES, unambiguously — two/four 22×22 arrays,
   Latin-property + pairwise-orthogonality overlay check, a dozen lines of code. Zero trust needed.
5. **Is the significance real?** YES — it is *the* most-cited small open MOLS order ("the only n apart
   from 4 with 3 known but not 4"). A witness is a clean, citable contribution to the Handbook.

**Verdict on the kill attempt:** #1 survives on novelty, verifiability, and significance, but the
"realistic-shot-in-weeks" axis is its weak point — it is genuinely hard and may resist a
sample-limited fleet. RECOMMENDED HEDGE: run the pilot as a **MOLS small-order campaign**, not a
single-target bet — target N(22)≥4 AND N(18)≥4 AND N(26)≥5 (and revisit N(20),N(14) mates) with the
same separable-permutation-code / difference-matrix / prescribed-automorphism engine. Any ONE hit is
a record; pooling the open small orders converts a low-probability single swing into several
correlated shots on the same machinery, which is the right shape for a sample-limited fleet.

Secondary recommendation if a cleaner "likely-yes" win is preferred over the famous-but-hard #22:
the d=4 constant-weight slice (#3) is the un-swept complement of the proven-tractable CPro1 target —
lower significance per hit but higher hit-probability, and directly leverages that CPro1 already
showed the LLM-fleet works on constant-weight codes.

---

## DO-NOT-RE-CHASE (this session's negatives)

- A(n,d,w) at d∈{6,8,10,12,16,18}, n∈[18,35] — SWEPT by CPro1 (2603.00174, Feb 2026).
- Weighing matrices / equidistant permutation arrays / packing arrays / balanced ternary designs /
  Florentine rectangles — SWEPT by CPro1 design paper (2501.17725).
- Small-q caps/arcs (m(2,q) for q≤160001; PG(k,q) classified k≤5 small q) — exhaustive-search OWNED.
- AG(n,3) cap sets — FunSearch turf.
- Football-pool K₃(n,1) UPPER bounds — MILP/SAT solver-owned, 20-yr-stale, weak fit.

---

READY FOR JUDGING — Verdict: REAL target = **four MOLS of order 22 (N(22)≥4 / TD(6,22))**, a named
decades-open small case, exactly checkable by anyone, NOT owned by CPro1/AlphaEvolve/solvers, and
structure-bottlenecked (brute force infeasible) so an LLM-reasoned construction fleet is the right
tool — with the honest caveat that it is genuinely hard (resisted strong CP/IP campaigns), so it is a
high-value SWING; run it as a pooled MOLS small-order campaign (22 + 18 + 26) for several correlated
shots, with the d=4 constant-weight slice as the higher-probability lower-significance fallback.

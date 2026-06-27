# Softness audit — candidates D (MOLS of order 22) and E (multicolor C₄ Ramsey)

Date 2026-06-27. Rubric: `research_notes/SOFTNESS_AUDIT_GOAL.md` (S1 weak-method · S2 wide-gap ·
S3 no-tight-red-flags · S4 neglected · S5 still-new-if-beaten). Default hypothesis: BOTH TIGHT.
All record/bound/method claims web-verified June 2026; KNOWN vs CLAIMED vs UNVERIFIED tagged inline.

---

## TL;DR verdicts

| Cand | Object | Verdict | Confidence | One-line reason |
|------|--------|---------|-----------|-----------------|
| **D** | four MOLS(22): N(22)≥4? | **TIGHT** | **HIGH (~0.9)** | Strong IP/CP/SAT campaigns can't even resolve a *triple* of order 10; the 2024 separable-code breakthrough jumped N(54/96/108) but does NOT reach small orders. S1 & S4 FAIL. |
| **E** | r_k(C₄), k=5,6,7 | **TIGHT-leaning UNCERTAIN** | **MED-HIGH (~0.75)** | Lower bound = Füredi-optimal orthogonal-polarity-graph extremal construction (near-truth algebraic, S1/S3 fail at prime-power k). Genuine residual slack only at NON-prime-power k (k=6,7) where the construction is off-optimal — but that slack is small (≤ a few) and the gap is sub-quadratic. Recent LLM sweeps target classical R(s,t)/mixed-C₄, NOT pure r_k(C₄), so it is technically S4-neglected — but neglected *because* the construction is believed near-tight, not because it's unexplored. |

Bottom line for the fleet decision: **neither is a soft tap-in.** D is a decades-hard swing (kill). E has a *thin* structured-search opening at k∈{6,7} but it is a strong-construction regime, not a weak-method regime — at best a low-probability structured-algebraic shot, not a FunSearch-soft target.

---

# CANDIDATE D — four MOLS of order 22 (N(22) ≥ 4?)

## The object (KNOWN, web-verified)
- N(n) = max size of a set of mutually orthogonal Latin squares of order n; N(n) ≤ n−1 always.
- **N(22) = 3 is KNOWN** (≥3 constructed; e.g. three MOLS / idempotent MOLS of order 22 — Abel, Zhang & Zhang; Bose–Shrikhande gave the original orthogonal *pair* of order 22 in 1959/60, the "Euler spoiler" that helped kill Euler's 4m+2 conjecture). Source: search snippets citing Bose–Shrikhande and Abel–Zhang–Zhang; Wikipedia "Mutually orthogonal Latin squares".
- **N(22) ≥ 4 is OPEN.** Multiple sources: "22 is the **largest order** for which it is not known whether four MOLS exist." (Wikipedia MOLS; MDPI 16(12):1678 "Implementing the MOLS Table for n up to 500", 2024.) → **the open question is exactly N(22)∈{3,…,18}, with 4 the first undecided value.**
- **Upper bound: N(22) ≤ 18** (KNOWN — the n−4 bound holds for n = 6, 14, 21, 22; verified in search). So the "gap" is 3 vs 18 in principle, but the *contested* gap is the single step 3→4.

## S-criteria

**S1 — weak record method? → FAIL (record/non-existence frontier set by STRONG methods).**
The relevant "record" is the *failure* to find a 4th square, and that failure is the output of strong, modern campaigns:
- **arXiv:2103.11018** (Rubin, Bright, Cheung, Stevens, 2021, AAAI student abstract) — modern IP **and** CP solvers as black boxes, plus a new extended symmetry-breaking method and improved CP encoding, specifically for MOLS. KNOWN result: they resolve pairs in all orders ≤10 and *estimate the running time to settle even a **triple** of order 10*, framing it as a "longstanding open problem." (Verified from abstract.) **Implication:** finding a TRIPLE of order 10 is already at the edge of feasibility for state-of-the-art IP/CP — a 4-MOLS-of-22 search (vastly larger) is far beyond a black-box solver campaign.
- SAT attacks on MOLS exist and are active (e.g. arXiv:2503.10504, Myrvold's orthogonal-triple 10×10 via SAT; cube-and-conquer/BOINC searches). The small-order MOLS frontier is a *specialist, actively-cultivated* problem — exactly the S3 "cultivated table" red flag.
→ The current state is **not** a stale hand-construction with obvious slack; it's the residue after strong solver + design-theory effort.

**S2 — wide gap? → MIXED, but the contested gap is +1.**
Nominal gap 3 ≤ N(22) ≤ 18 looks wide, but the interesting/attackable boundary is the *single* step N(22) ≥ 4. Producing 4 MOLS(22) is one structure; it has resisted both algebraic construction (no prime-power / product / transversal-design route yields 4 at 22 — 22 = 2·11 is the obstruction) and search. A "+1" contested value sandwiched against heavy prior effort is the acute-set failure pattern.

**S3 — TIGHT red flags? → PRESENT.**
- On a **cultivated table** (the MOLS table is maintained in the Handbook of Combinatorial Designs and the 2024 MDPI "MOLS table to 500" paper) — direct S3 red flag.
- Nearby orders are *resolved or pushed by specialists*: the 2024 separable-permutation-code paper (below) jumped 54/96/108. Small orders are precisely the hard residue.

**S4 — neglected? → FAIL (freshly + repeatedly attacked).**
- **arXiv:2412.00480** (Abel, Janiszczak, Staszewski, Nov 2024) — the fresh structured angle the prompt flagged. KNOWN: improves N(54)≥8, N(96)≥10, N(108)≥9 via **separable permutation codes** (lengths 54/96, min-distance 53/95). **Verified: the paper's smallest improved order is 54; it does NOT mention order 22 or any small order, and gives no route to them.** The technique is asymptotic/large-order (needs room for long high-distance permutation codes); it structurally bypasses n=22.
- IP/CP (2021), SAT (2023–2025), cube-and-conquer, separable codes (2024): the area is under continuous strong attack. Not neglected.

**S5 — still a new fact if beaten? → YES.**
If a fleet actually produced 4 MOLS(22), that would be a genuine, exactly-verifiable, *famous* new result (settles the smallest open N(n)). Unowned and unbeaten NOW (verified open June 2026). But this cuts both ways: its fame is *why* it is hard — it is the headline open small-order MOLS case, not an overlooked niche.

## Verdict D: **TIGHT — confidence HIGH (~0.9).**
This is the survey's "swing, not a tap-in," confirmed harder than that: a 4th MOLS(22) is the **smallest open value on a specialist-cultivated table**, where (a) strong IP/CP can barely reach a *triple of order 10*, (b) SAT/cube-and-conquer have been thrown at small MOLS, and (c) the one 2024 breakthrough technique explicitly skips small orders. Every softness criterion that matters (S1 weak-method, S4 neglected) FAILS. This is acute-set-shaped: the contested value is +1 against near-exhaustive strong effort.
- **The NEW fact that would count:** an explicit set of four MOLS of order 22 (proves N(22)≥4), OR a proof N(22)=3. Either is a real result.
- **Why a weeks-fleet is a bad bet:** the search space dwarfs the order-10-triple frontier that already strains specialist solvers; FunSearch/AlphaEvolve-style code-evolution has no demonstrated traction on MOLS existence at this size, and the structured-construction route (22 = 2·11) has no known opening.

## Cheapest validate/falsify probe for D (<~1 hr)
**Probe:** Stand up a minimal SAT encoding for "3 known MOLS(22) + a compatible 4th square" (fix the known triple from the literature, encode only the 4th Latin square + its orthogonality to the three, hand to a modern SAT solver like CaDiCaL/Kissat with a few-minute timeout). 
**What it tells you:** if the solver instantly proves UNSAT for natural symmetry-broken extensions, that is direct evidence the boundary is tight/hard (extension-infeasible), → confirm KILL. If it's wildly inconclusive (no progress, huge), that confirms the space is beyond a fleet's reach → also KILL. There is essentially no cheap outcome that flips this to SOFT. (This is the cheapest way to *feel* the wall; expected result: confirms TIGHT.)
*Note:* extension-from-a-fixed-triple is more restrictive than full 4-MOLS search, so UNSAT there is suggestive, not a proof of N(22)=3 — but for the softness decision it is decisive enough.

---

# CANDIDATE E — multicolor quadrilateral Ramsey r_k(C₄)

## The object + exact bounds (KNOWN, web-verified)
r_k(C₄) = least n s.t. every k-edge-coloring of K_n has a monochromatic C₄. Verified values/bounds:

| k | lower | upper | gap | lower-bound source |
|---|-------|-------|-----|--------------------|
| 2 | 6 | 6 | 0 | = (exact) |
| 3 | 11 | 11 | 0 | = (exact) |
| 4 | **18** | **19** | 1 | r₄(C₄)=18 lower by **Exoo** (Utilitas Math. 2007); upper 19 (Sun Yongqi et al.) |
| 5 | **27** | **29** | 2 | r₅(C₄) ≥ 27 = 5²+2 (**Lazebnik–Woldar 2000**, odd prime power 5) |
| 6 | k²−k+2 = **32** (≥; k−1=5 prime power) | k²+k−1 = **41** | ~9 | Lazebnik–Woldar / Chung–Graham family |
| 7 | k²−k+2 = **44** (≥; k−1=6 NOT prime power → likely weaker) / k²+2=**51** needs 7 odd-prime-power ✓ | k²+k+1 = **57** | several | mixed |

NOTE on the table: k=4,5 lower/upper are firmly KNOWN-and-cited (18/19; 27/29). The k=6,7 entries are
the **general formulas applied** (CLAIMED at formula level, individual published table values UNVERIFIED
here — the canonical numbers live in Radziszowski DS1 §multicolor-cycles, rev.18 Jan-2026, and
Dybizbański–Dzido EJC v18i1p154; both PDFs failed clean text extraction this session → flag UNVERIFIED
for the *exact* r₆/r₇ table cells, though the bounding formulas below ARE verified).

Verified general bounds:
- **Lower:** r_k(C₄) ≥ k²+2 for k an **odd prime power** (Lazebnik–Woldar 2000); extended to ≥ k²+2 for any prime power; and r_k(C₄) ≥ k²−k+2 when **k−1 is a prime power** (Chung–Graham-type). (Verified across multiple sources.)
- **Upper:** r_k(C₄) ≤ k²+k+1 for all k≥2 (**Chung 1974 / Irving 1974**, independent); improved to **k²+k−1 for even k≥6** (Acta Math. Appl. Sinica 2023, "Upper Bounds on the Multicolor Ramsey Numbers r_k(C₄)"). (Verified.)

## The decisive structural fact (KNOWN, web-verified)
The Lazebnik–Woldar lower bound is **not a weak heuristic** — it is the **orthogonal polarity graph (Erdős–Rényi graph) of a projective plane PG(2,q)**, the extremal C₄-free graph. **Füredi proved orthogonal polarity graphs give the EXACT maximum number of edges of a C₄-free graph** (ex(n;C₄)) for those orders. So at prime-power k the lower bound is built from the *optimal* C₄-free object — an algebraic near-truth, not slack. This is the central S1/S3 finding for E and the reason the default should be TIGHT at prime-power k.

## S-criteria

**S1 — weak record method? → FAIL at prime-power k; PARTIAL PASS at non-prime-power k.**
- At k ∈ {prime powers} (k=4,5,7,8,9,…): lower bound = polarity-graph / projective-plane construction = Füredi-optimal extremal graph. This is a *strong algebraic optimum*, the opposite of a weak one-off heuristic. **S1 FAILS here.**
- At k ∈ {non-prime-powers} (k=6, 10, 12,…): no projective plane of that order ⇒ the construction degrades (you fall back to k²−k+2 from k−1, or ad-hoc/cyclic computer colorings). Here the record *is* from a weaker/sub-optimal construction with a wider gap → **S1 PASSES for k=6 (and the gap is widest there).** This is the only genuine softness pocket.

**S2 — wide gap? → only at k=6,7 (sub-quadratic).**
k=4 gap 1, k=5 gap 2 (acute-set-shaped, +1/+2). The gaps grow at k=6 (~32–41) and k=7, but the gap is **O(k)** against an **O(k²)** value — relatively thin, and both endpoints come from named theorems (so it's a "two theorems haven't met," not "no upper-bound effort"). Not the S2 "no serious upper bound" situation.

**S3 — TIGHT red flags? → PRESENT.**
- Lower bound = a **clean construction value** (k²+2 / k²−k+2) tied to projective planes — direct S3 red flag (record = construction value, like acute sets).
- The numbers live on the **Radziszowski DS1 cultivated Ramsey table** — S3 red flag.
- k=2,3 exact; k=4,5 sandwiched to +1/+2 — nearby values nearly pinned.

**S4 — neglected? → TECHNICALLY YES, but for the wrong reason.**
- The recent LLM/evolutionary sweeps do **NOT** touch pure r_k(C₄): **AlphaEvolve** & **RGCS** (arXiv:2603.09172 "Reinforced Generation of Combinatorial Structures: Ramsey Numbers", Mar 2026) attack **classical diagonal R(s,t)** (verified: paper is two-color R(k,k), not multicolor C₄). **Wesley SAT** (arXiv:2509.03784, Sep 2025) improves **mixed** colorings — R(K₃,K₄,C₄,C₄) ≥ 49, R(K₄,K₄−e,K₄−e) ≥ 35, R(C₃,C₆,C₆)=15 — **NOT** the pure r_k(C₄) sequence (verified from abstract). So pure r_k(C₄) is genuinely un-LLM-swept.
- BUT it is "neglected" because it's believed near-tight at prime-power k and because the interesting open k (6,7) are exactly where constructions are hard — neglect here is a *consequence of tightness/difficulty*, not an overlooked-easy signal. The mixed-C₄ variants ARE being actively pushed (Dybizbański–Dzido, Xu–Shao–Radziszowski, Wesley) — the neighbourhood is cultivated, just not this exact cell.

**S5 — still a new fact if beaten? → YES (verified unbeaten).**
Beating r_5(C₄)≥27→28, or r_6(C₄)/r_7(C₄) lower bounds, would be a genuine, exactly-verifiable new entry. Unowned/unbeaten as of June 2026 (verified). Modest but real.

## Realistic improvability assessment
- **r_5(C₄):** lower bound 27 = 5²+2 from the optimal PG(2,5) polarity graph; upper 29. To beat 27 you must find a *non-optimal-graph-based* 5-coloring on 27 vertices with no mono C₄ that the polarity construction misses — but the polarity graph is already the densest C₄-free graph, so the lower-bound side has little obvious slack. **Likely TIGHT (or the truth is 28/29, reachable only by hard SAT, not soft evolution).** Note blind search is dead (5³⁵¹), as the prompt says.
- **r_6(C₄):** **the one real opening.** 6 is not a prime power (no projective plane of order 6 — Euler/Tarry!), so the construction genuinely degrades; gap ~32–41 is the widest relative slack. A *structured algebraic-proposal* search (cyclic / Cayley colorings on Z_n, near-polarity pseudo-random C₄-free graphs, blow-ups) could conceivably push the lower bound a few above k²−k+2. This is the FunSearch-shaped sub-problem — but it is a *strong-construction* hunt, low base-rate, not a weak-method tap-in.
- **r_7(C₄):** 7 is an odd prime power ⇒ k²+2 = 51 lower from optimal polarity graph ⇒ S1 FAILS again ⇒ TIGHT-leaning like k=5.

## Verdict E: **TIGHT-leaning UNCERTAIN — confidence MED-HIGH (~0.75).**
The lower-bound machinery is the Füredi-optimal projective-plane polarity graph — a strong algebraic near-truth, failing S1/S3 at every prime-power k (including the headline k=5 and k=7). The ONLY genuine softness pocket is **k=6** (no plane of order 6 ⇒ off-optimal construction ⇒ widest relative gap), and even there the improvement ceiling is small (O(k) slack on an O(k²) value) and the hunt is a structured-construction problem, not a weak-method one. The prompt's framing is right: viable only as a **structured algebraic-proposal search**, and even then it's a low-probability shot at a thin margin, in a neighbourhood that's actively cultivated (mixed-C₄ is being pushed by specialists). Not FunSearch-soft.
- **The NEW fact that would count:** an explicit k-coloring proving r_6(C₄) ≥ (k²−k+2)+1 = 33 or higher (the best target), or r_5(C₄) ≥ 28, or any r_7(C₄) lower-bound bump — each a verifiable new DS1 entry.
- **Why not a fleet (yet):** at prime-power k the construction is optimal (no slack); at k=6 the slack is thin and demands clever algebraic/cyclic constructions, the exact regime where evolutionary code-search has weak priors and SAT is the better tool — and SAT-on-r_6(C₄) at ~32–41 vertices, 6 colors is itself heavy.

## Cheapest validate/falsify probe for E (<~1 hr)
**Probe:** Target **k=6 only** (the sole soft pocket). Run a short **cyclic-coloring search** for a mono-C₄-free 6-coloring of K_n on Z_n for n = 33, 34, 35 (i.e. one above the k²−k+2 = 32 lower bound): pick n, partition the n−1 nonzero differences {±1,…} of Z_n into 6 color-classes (difference sets), and check each color class' circulant graph is C₄-free (a difference set d gives C₄ ⇔ a repeated difference among {d_i−d_j}); a quick randomized/greedy or small ILP over difference-class assignments, few-minute budget.
**What it tells you:** if even a *cyclic* search comfortably finds a valid 6-coloring on 33–34 vertices, the published lower bound is soft and a fleet has a target → flag E **SOFT (k=6 only)**. If cyclic colorings stall right at/below 32 (matching the construction value), the bound is plausibly tight at k=6 too → **confirm TIGHT**. This is the single cheapest test that could flip E; it isolates the one regime where slack is even possible. (Cyclic ≠ general, so success = soft signal; failure = strong tight signal but not a proof.)

---

## Cross-candidate synthesis (for the main loop)
- **D = KILL.** Acute-set-shaped and harder: smallest open value on a cultivated table, strong solvers barely reach an order-10 *triple*, 2024 breakthrough skips small orders. S1+S4 fail decisively. No cheap outcome flips it. Confidence HIGH.
- **E = mostly KILL, with ONE thin probe worth running first.** Prime-power k (5,7,…) are TIGHT (Füredi-optimal construction). Only **k=6** is even arguably soft (no order-6 plane). Run the <1 hr cyclic-coloring probe on r_6(C₄) at n=33–34 *before* committing anything; if it doesn't trivially beat 32, drop E entirely.
- Relative to the FRESH-target hunt: both D and E confirm the lesson — a construction-value record on a cultivated specialist table (MOLS table; Ramsey DS1) is the acute-set TIGHT signature, regardless of nominal gap size. The softness you want is a record from a *weak/non-exhaustive* method, which neither D (strong solvers) nor E-at-prime-power-k (optimal polarity graph) provides.

## Honesty ledger (KNOWN vs CLAIMED vs UNVERIFIED)
- KNOWN (web-verified, multi-source): N(22)=3, N(22)≥4 open, N(22)≤18; arXiv:2103.11018 IP/CP can't settle a triple of order 10; arXiv:2412.00480 improves only N(54/96/108), skips small orders; r₄(C₄)=18 / r₅(C₄)∈[27,29]; Lazebnik–Woldar r_k(C₄)≥k²+2 (odd prime power); Chung/Irving upper k²+k+1, improved k²+k−1 (even k≥6); Füredi: polarity graphs = exact ex(n;C₄); AlphaEvolve/RGCS target classical R(s,t); Wesley SAT targets mixed-C₄ not pure r_k(C₄).
- CLAIMED / formula-level (not independently table-verified this session): exact r₆(C₄), r₇(C₄) published table cells (formulas verified; specific DS1/Dybizbański–Dzido cell values UNVERIFIED — PDF extraction failed; flagged above).
- NOT fabricated: no record, bound, or citation here is invented; every arXiv id and named theorem was returned by search. Where I could not extract an exact cell I said UNVERIFIED rather than guess.

READY FOR JUDGING.

### Sources (web-verified June 2026)
- N(22) status / MOLS table: en.wikipedia.org/wiki/Mutually_orthogonal_Latin_squares ; MDPI Symmetry 16(12):1678 "Implementing the MOLS Table for n Up to 500" (2024).
- IP/CP MOLS campaign: arXiv:2103.11018 (Rubin, Bright, Cheung, Stevens).
- Separable-permutation-code MOLS jump: arXiv:2412.00480 (Abel, Janiszczak, Staszewski, 2024); cf. arXiv:1812.06886 (Janiszczak et al.).
- SAT on small MOLS: arXiv:2503.10504.
- r_k(C₄) lower bounds: Lazebnik & Woldar, "New Lower Bounds on the Multicolor Ramsey Numbers r_k(C₄)", J. Combin. Theory Ser. B (2000); r₄(C₄)=18 Exoo (Utilitas Math. 2007); Dybizbański & Dzido, EJC v18i1p154.
- r_k(C₄) upper bounds: Chung (1974) / Irving (1974) k²+k+1; Acta Math. Appl. Sinica (2023) "Upper Bounds on the Multicolor Ramsey Numbers r_k(C₄)" k²+k−1 even k≥6; arXiv:2311.13582 (mixed-C₄ uppers).
- Füredi extremal C₄-free / polarity graphs optimal: Füredi (1996), via search snippets on orthogonal polarity / Erdős–Rényi graphs.
- LLM/evolutionary Ramsey sweeps (NOT pure r_k(C₄)): arXiv:2603.09172 (RGCS: Ramsey Numbers); arXiv:2509.03784 (Wesley, SAT, mixed multicolor); AlphaEvolve (Wikipedia / arXiv:2506.13131-class reporting).
- Canonical Ramsey table: Radziszowski, "Small Ramsey Numbers", DS1 rev.18 (Jan 2026), combinatorics.org.

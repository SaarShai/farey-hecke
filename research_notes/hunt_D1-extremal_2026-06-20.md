# Hunt D1 — Extremal / Ramsey / SAT-encodable combinatorics (2026-06-20)

Domain scout for an OPEN problem matching our fleet edge (parallel reasoning + adversarial
falsification + exact/interval-certified search + Lean/Aristotle verification + NT/dynamics
collaborator). Mode: literature + reasoning survey. Web-verified; UNVERIFIED flagged.

## Edge restatement (what we're matching to)
- Bottleneck must be SEARCH / CONSTRUCTION / VERIFICATION / pattern-finding — NOT deep analysis.
- We have modest compute, so NO raw-FLOPS brute force (no 17k-CPU-hour UNSAT runs).
- Our differentiator is a *structured / clever* search (group-constrained, symmetry-reduced)
  producing a WITNESS that is trivially independently checkable, plus optional formal proof.

The strongest-fit paradigm in this domain RIGHT NOW is **SAT modulo symmetries (SMS)** +
**block-Cayley / block-circulant constrained colorings** (Kirchweger–Peitl–Szeider; W. Wesley)
and **SAT+Lean formal verification of discrete-geometry numbers** (Heule–Scheucher; Subercaseaux
et al). These are lower-bound *witness constructions* and *certified UNSAT* — exactly our shape.

---

## CANDIDATES

### C1 (TOP PICK) — Lower bounds for small multicolor Ramsey numbers via structured (block-Cayley / circulant) colorings
- **Status: OPEN, ACTIVELY moving, NOT saturated.** W. J. Wesley, "New bounds for some small
  multicolor Ramsey numbers," arXiv:2509.03784 (Sep 2025) just improved:
  - R(K4, K4−e, K4−e): **35 ≤ · ≤ 47** (he raised LB 34→35 via a block-Cayley coloring on 34
    vertices; gap 12).
  - R(K3, K4, C4, C4): **49 ≤ · ≤ 75** (raised 43→49; gap 26).
- **Why it fits the filter:** the contribution is a coloring (an explicit edge-coloring of K_{n}
  with no monochromatic forbidden subgraph in the respective color) — a WITNESS that is checked
  in milliseconds independently. The search is made tractable precisely by *imposing group
  structure* (circulant / block-Cayley) so a SAT solver / structured enumeration handles it on
  modest compute. This is our exact mechanism (clever structured search + cheap verification),
  and a fleet can sweep many groups/orders in parallel and adversarially re-check.
- These improvements were made by a SINGLE researcher with SAT + a laptop-scale solver in 2025,
  i.e. the frontier is movable at our compute budget — the opposite of R(5,5).
- Author explicitly frames it as raisable ("Concluding remarks" invites more) — a near-frontier
  with room, not a closed table.

### C2 — Degree–Diameter problem (undirected, general + Cayley table) record graphs
- **Status: OPEN record table, records broken yearly.** Comellas/CombinatoricsWiki table; new
  record graphs found by Comellas in 2024 for (3,5),(6,8),(7,6),(7,7),(8,5),(9,4),(10,4),(10,5),
  (11,5),(12,5),(13,5),(14,5),(15,5); table edited as recently as Apr-2025 (UNVERIFIED exact
  dates per-cell). Cayley-graph sub-table (combinatoricswiki) also has movable cells.
- **Fit:** a record is a single explicit graph (adjacency list) — trivially checkable (compute
  its diameter). Best constructions are Cayley graphs of a chosen group + connection set, so the
  search = "pick group + generators, verify diameter" — structured search, cheap verify.
- **Caveat:** weaker "fame," and many cells are saturated; only a few small cells realistically
  movable. Good as a SECONDARY/warm-up or fallback that *guarantees* a checkable deliverable.

### C3 — Kochen–Specker minimum vector system (lower bound) via SMS + co-certificate learning
- **Status: OPEN, big gap. LB 24 (Kirchweger–Peitl–Szeider 2023, SMS+CCL), best known system
  31 vectors (Conway–Kochen).** Active.
- **Fit (partial):** the lower-bound proof is a certified non-existence (UNSAT-style) of a
  non-010-colorable graph below a size — verification-shaped and SMS-native. BUT pushing 24→25
  is a large symmetry-rich search that consumed serious compute; this is closer to a
  FLOPS-bound exhaustive search than C1. Better suited as a verification/methods collaboration
  than a solo construction we can crack in weeks. Listed for completeness.

### C4 — Erdős–Szekeres g(7)=33 (convex-7-gon) via SAT
- **Status: OPEN (g(7)=33 conjectured; lower bound 33 known via Szekeres–Peters config, upper
  bound NOT proven).** Dumitru, "Notes on the 33-point Erdős–Szekeres problem," arXiv:2512.24061
  (Dec 2025) gives a triple-orientation SAT encoding and UNSAT for several *anchored* sub-families
  only — the full instance is not yet in reach.
- **Fit (partial):** the empty-hexagon h(6)=30 precedent (Heule–Scheucher 2024; Subercaseaux et
  al. Lean verification ITP 2024) is the dream template (SAT result + Lean certificate). BUT the
  full g(7)=33 UNSAT is believed to be a very large computation (the bottleneck the Dumitru note
  hits) — likely beyond our compute for the *full* settle. A realistic fleet contribution is
  *partial anchored UNSAT families* / a better/smaller encoding — incremental, not the whole nut.

### C5 — Cycle/wheel/book multicolor Ramsey exact values from circulant colorings
- **Status: OPEN with small gaps.** Same Wesley line settled R(C3,C6,C6)=R(C5,C6,C6)=15 (2025);
  book-Ramsey R(B_{n−1},B_n)=4n−1 infinite family + scattered R(B_r,B_s) gaps (arXiv:2410.03625).
  Many small cycle/book triples remain with gap 1–3 between LB (circulant witness) and UB (SAT
  or SMS critical-graph enumeration).
- **Fit:** essentially the same engine as C1 on a different subgraph family; gaps are smaller so
  several could be CLOSED (exact value), not just nudged. Strong companion to C1.

---

## TOP PICK + precise statement
**C1: improve the lower bound (and ideally pin the exact value with the matching SAT upper
bound) of a small multicolor Ramsey number, starting with R(K4, K4−e, K4−e) [currently
35 ≤ R ≤ 47], by a structured block-Cayley / block-circulant coloring search across many
candidate groups of order 35–46, with each candidate coloring independently verified (no
monochromatic K4 in color 1, no monochromatic K4−e in colors 2,3) and the best witness optionally
Lean-checked.** Companion targets: R(K3,K4,C4,C4) [49 ≤ R ≤ 75] and the small cycle/book triples
in C5 where the gap is 1–3 (candidates to CLOSE).

### Contribution shape (concrete, verifiable)
A new explicit edge-coloring (adjacency data) of K_n raising a published multicolor-Ramsey lower
bound by ≥1, where the certificate is checked by a trivial independent subgraph-search script;
OR a SAT/SMS UNSAT closing a 1–3 gap to an EXACT value. Both are bulletproof-checkable and
Lean-formalizable on the empty-hexagon template.

### Why our edge gives a real shot
- The 2025 improvements (34→35, 43→49) were made by ONE person with a SAT solver — movable at
  our compute. Our fleet adds parallel group-sweeps + adversarial re-verification of each witness
  (kills false "improvements" instantly) + the option to ship a Lean certificate, which is a
  genuine differentiator vs the existing literature (most LBs are unverified-by-proof).
- Bottleneck is search+verification, not analysis — passes the hard filter cleanly.
- Explicitly OUTSIDE our forbidden corner (no Hecke/Maass/QUE/arithmeticity).

### Tractability (honest)
- Realistic in weeks for a *nudge* (LB +1) on R(K4,K4−e,K4−e) or for CLOSING a gap-1–3 cycle/book
  triple. The hard part: the right algebraic constraint (which group, which block structure) is
  not guaranteed to yield an improvement — Wesley may have already harvested the easy circulant
  structures, so we need a genuinely new structured family or a smarter symmetry-broken full SAT.
  Failure mode: every structured coloring we find is ≤ the known bound (no improvement), leaving
  only a "verified-existing-bound + Lean certificate" methods contribution (still publishable but
  not a record). For the big gaps (gap 12, gap 26) closing to exact is UNLIKELY for us.

### Novelty / ownership
- The multicolor-Ramsey + structured-coloring + SAT line is **partly owned/active** (W. J. Wesley,
  UC Davis, 2024–2026; SMS by Kirchweger–Peitl–Szeider, TU Wien). It is an *active collaborative
  frontier*, NOT a closed problem — record cells move and the authors invite improvement. Our
  *differentiated* slice = (a) parallel structured-group sweep + adversarial witness falsification,
  (b) Lean/Aristotle certificate for the witness (novel: existing LBs ship as raw colorings, not
  machine-checked proofs). The exact *numbers* are owned-until-beaten; the *verification layer* is
  open and ours to claim.

---

## Sources (web-verified 2026-06-20)
- W. J. Wesley, "New bounds for some small multicolor Ramsey numbers," arXiv:2509.03784 (Sep 2025)
  — R(K4,K4−e,K4−e)≥35, R(K3,K4,C4,C4)≥49, R(C3,C6,C6)=R(C5,C6,C6)=15; block-Cayley/circulant + Kissat.
- W. J. Wesley, "Lower Bounds for Book Ramsey Numbers," arXiv:2410.03625 (Sep 2025) — block-circulant,
  R(B_{n−1},B_n)=4n−1 family, SMS critical-graph enumeration.
- Kirchweger, Peitl, Szeider, "Co-Certificate Learning with SAT Modulo Symmetries," IJCAI 2023 /
  arXiv:2306.10427 — KS lower bound ≥24 via SMS+CCL.
- Stefan Szeider, "SAT Modulo Symmetries: A Survey," CEUR Vol-4116 (invited) — SMS scope.
- Subercaseaux, Nawrocki, Gallicchio, Codel, Carneiro, Heule, "Formal Verification of the Empty
  Hexagon Number," ITP 2024 / arXiv:2403.17370 — h(6)=30, SAT+Lean (the certificate template).
- B. Dumitru, "Notes on the 33-point Erdős–Szekeres problem," arXiv:2512.24061 (Dec 2025) — g(7)=33
  SAT encoding, partial anchored UNSAT only.
- Degree–Diameter table (web.mat.upc.edu/francesc.comellas; combinatoricswiki.org) — record cells,
  Comellas 2024 new records; table edited ~Apr-2025 (UNVERIFIED per-cell dates).
- L. Boza, "New Upper Bounds for the Classical Ramsey Numbers R(4,4,4),R(3,4,5),R(3,3,6)"
  arXiv:2603.10851 — R(4,4,4) ≤ 229 (context: only R(3,3,3)=17 known exactly among multicolor).

## Caveats
- "Famous-but-untouchable" rejected: R(5,5) [43..46], R(4,6), R(3,10) — UB side is deep-analytic /
  huge-search; do NOT chase the diagonal classical numbers.
- KS lower bound (C3) and full g(7)=33 (C4) are likely beyond our compute for the FULL result;
  treat as methods/verification collaborations, not solo conquests.
- Risk that Wesley/SMS groups have already exhausted the easy structured colorings; our genuine
  edge may reduce to the *verification layer* (Lean certificate) rather than a numeric record —
  acceptable but must be stated honestly up front.
- Per-cell dates on the degree–diameter table are UNVERIFIED at the cell level.

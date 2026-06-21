# Hunt D2 — Discrete & Combinatorial Geometry (2026-06-20)

Mode: literature + reasoning survey. Goal: find ONE open problem our fleet can
genuinely contribute to (witness/construction/verified-case), matching our edge
(parallel reasoning + adversarial falsification + exact/interval-certified
search + Lean/Aristotle verification + a number-theory/dynamics collaborator),
NOT raw FLOPS, NOT deep analysis.

## Domain scan summary

Surveyed: Hadwiger–Nelson / chromatic number of the plane (CNP), unit-distance
graphs (UDGs), distinct distances (Erdős / Erdős–Fishburn few-distance sets),
high-dimensional chromatic numbers, point configurations. The richest
ACTIVE-and-tractable seam is the **Polymath16 program**, which restarted in
**January 2026 (18th thread, Dustin Mixon's blog)** with a NEW unifying
conjecture and a concrete to-do list of graph constructions and
independence-number certifications — exactly search/construct/verify work.

---

## Candidate 1 (TOP) — Polymath16 simplex-free chromatic UDG conjecture: settle a small open {d,n} case

**Status: OPEN, ACTIVE (Polymath16, 18th thread, 2026-01-17).**

The new conjecture (Mixon/de Grey/Parts et al., Jan 2026): *for all d ≥ 2 and
3 ≤ n ≤ d+2, there is a (d+n−1)-chromatic unit-distance graph in R^d containing
no n-simplex.* Only finitely many {d,n} pairs are not already settled, so the
frontier is a FINITE, enumerable list of concrete construction targets.

Known/settled (web-verified, Jan-2026 thread): (2,3) [de Grey 5-chromatic],
(2,4) [4-chromatic triangle-free], (3,3),(3,4) [Asger Heine Jensen / de Grey],
(8,10) [Parts, χ(R^8)≥22], and all d ≥ 67 via Raigorodskii's exponential
sphere bound. Smallest OPEN cases flagged: **(3,5)** (a 7-chromatic UDG in R^3
— equivalently pushing χ(R^3) ≥ 7, currently 6), the dimension-**5** band
(little progress), and several (4,·),(6,·),(7,·) pairs.

**Why it fits our edge.** The deliverable is a *finite graph* — a UDG realized
at explicit algebraic coordinates with a certified chromatic number and a
certified forbidden-clique/simplex condition. Both certificates are exactly our
machinery: (i) χ ≥ k via a SAT/UNSAT proof that the graph is not (k−1)-colorable
(DRAT certificate, independently checkable — the de Grey/Heule lineage already
does this); (ii) simplex-free via clique enumeration; (iii) unit-distance
realizability via exact arithmetic on the coordinate field. A parallel fleet
proposes lattice/polytope subgraphs (E6/E7/E8 sublattices, 600-cell/120-cell
shells, Johnson graphs); an adversarial arm prunes false candidates; Lean/DRAT
makes the survivor bulletproof.

**Concrete sub-target with the cleanest verification shape:** improve a
**lower bound χ(R^d) ≥ m** for a small d (e.g. push R^5 above its current
published lower bound, or land (3,5) = χ(R^3) ≥ 7) by exhibiting an explicit
lattice/polytope subgraph G with vertex count N, certified independence number
α(G), giving χ ≥ ⌈N/α⌉. The HARD step the thread names is the
**independence-number computation** on 900–1700-vertex highly symmetric graphs
(mcqd takes weeks/months) — a symmetry-broken exact-search problem, which is our
"clever/structured search + certify" sweet spot, NOT raw FLOPS, and the answer
(an independent set + an LP/SDP or branch-and-bound upper-bound certificate) is
independently checkable.

**Honest risk:** the headline cases (3,5) and dim-5 may need a genuinely new
construction idea, not just search; the big-lattice independence numbers may be
out of modest-compute reach even with symmetry breaking; and the strongest
players (de Grey, Parts, Heule, Raigorodskii) are extremely good at exactly this
— we'd be entering an active competition, so we must pick a sub-case where our
certify/verify discipline is the differentiator (e.g. produce the *first
machine-checked DRAT/Lean certificate* for an existing or new bound, or settle a
mid-list {d,n} the principals haven't prioritized).

---

## Candidate 2 — Minimal triangle-free (and tetrahedron-free) 5-chromatic UDG in the plane

**Status: OPEN (minimization), very recent activity.**

de Grey, *"A 5-Chromatic, Triangle-Free Unit-Distance Graph in R^2 with 61
vertices,"* Geombinatorics 35 (2026) — current record 61 vertices (built from a
tetrahedron-free 31-vertex 3D embedding of a Grötzsch-like graph). The
minimization question ("smallest order of a triangle-free 5-chromatic UDG") is
explicitly open and is a named Polymath16 problem.

**Fit:** small graph (~61 vertices), fully verifiable: SAT-UNSAT for χ=5,
triangle enumeration for triangle-freeness, exact coordinates for unit-distance.
A fleet can do clausal minimization (Heule's method) to shave vertices, or
search new triangle-free seeds — a clean "improved explicit construction +
verified" deliverable. Lower in ceiling than Candidate 1 but very tractable.

**Risk:** record is fresh and held by de Grey himself; squeezing 61→lower may be
hard and incremental. Verification is trivial; the search is the work.

---

## Candidate 3 — Erdős–Fishburn few-distance sets: g(7)

**Status: OPEN for k ≥ 7 (web-verified; conflicting claims on g(5),g(6)).**

g(k) = max points in the plane spanning ≤ k distinct distances. Settled small:
Erdős–Fishburn (k≤4), Shinohara (k=5), Wei (g(6)=13). **g(7) is open.**
Conjecture: optimal sets lie in the triangular lattice for large k. Recent:
Wang, "On Few-Distance Sets in the Plane," arXiv:2510.09800 (2025) — improved
bounds, treats k=5,6,7 region; Tao's Sep-2024 post solved Erdős #135 (forbidden
4-point patterns) negatively and lists a tractable residual (super-linear lower
bound for sets avoiding all 8 four-point patterns).

**Fit:** determining g(7) is a finite extremal search + a non-existence
certificate — verifiable in principle. BUT: the search space (point sets up to
the conjectured ~14–16 points spanning 7 distances, over algebraic coordinates)
is combinatorially nasty, and "g(7) = X" needs an *exhaustive* impossibility
proof for X+1, which is the genuinely hard, possibly compute-heavy part. This is
more owned/harder-to-close than Candidates 1–2.

**Risk:** the non-existence (upper) side is the deep part and may exceed modest
compute; the lower side (a good explicit configuration) is doable but
incremental. Medium ownership.

---

## Cross-cutting verdict

- **CNP planar lower bound (χ(R²) ≥ 6)** and **minimal 5-chromatic UDG in the
  plane (record ~509 vertices, Parts 2021)** are too saturated / too
  incrementally contested to be our best shot, though the 509-vertex
  minimization is a clean verify target if we want a safe modest win.
- The **fresh, finite, construction-shaped** Polymath16 simplex-free list
  (Candidate 1) is the best edge-fit: collaborative frontier (NOT owned-closed),
  bottleneck = search + independence-number certification + DRAT/Lean
  verification (our strengths), deliverable independently checkable.

## Sources (web-verified 2026-06-20)
- Polymath16 18th thread (new conjecture, open {d,n} list, lattice/polytope
  candidates, independence-number obstacle): dustingmixon.wordpress.com,
  2026-01-17.
- de Grey 2018, "The chromatic number of the plane is at least 5," arXiv:1804.02385.
- Heule 2018, "Computing Small Unit-Distance Graphs with Chromatic Number 5,"
  arXiv:1805.12181 (553 verts, DRAT-certified χ).
- Parts 2021, 509-vertex 5-chromatic UDG (arXiv:2106.11824 / 2010.12665).
- de Grey 2026, Geombinatorics 35, 61-vertex triangle-free 5-chromatic UDG.
- Voronov–Neopryatnaya–Dergachev tetrahedron-free 5-chromatic sphere UDGs
  (372/972 verts) — MathWorld.
- Wang 2025, "On Few-Distance Sets in the Plane," arXiv:2510.09800.
- Tao 2024-09-03, "Planar point sets with forbidden four-point patterns..."
  (Erdős #135 solved; residual lower-bound question).
- Wei: g(6)=13; Shinohara: g(5); Erdős–Fishburn: k≤4 (background, web-confirmed).

## Caveats / UNVERIFIED flags
- Exact published lower bound for χ(R^5) and the precise current OPEN/closed
  status of each {d,n} pair beyond the smallest ones are summarized from the
  Jan-2026 blog thread (secondary source); a real attempt must re-confirm the
  exact record per dimension against primary papers before claiming an
  improvement.
- g(5),g(6): sources conflict on whether fully "settled"; treat g(7) as the
  firmly-open target.
- Whether the big-lattice independence numbers are within modest compute is
  UNVERIFIED — this is the make-or-break feasibility question for Candidate 1's
  lower-bound route.

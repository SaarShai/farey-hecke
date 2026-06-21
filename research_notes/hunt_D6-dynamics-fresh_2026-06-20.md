# Hunt D6 — Dynamics/ergodic-theory OUTSIDE Hecke/Maass: fresh certified-computation targets

Date: 2026-06-20. Agent: D6 (dynamics-fresh). Mode: literature+reasoning survey, no compute yet.
Domain assigned: dynamical systems / ergodic theory, AVOID Hecke/Rosen/arithmeticity/QUE/Maass.

OUR EDGE recap: parallel reasoning fleet + adversarial falsification; exact/interval-certified
arithmetic; Lean/Aristotle formal verification; NT/dynamics collaborator. NOT raw FLOPS; NOT the
deep-analytic frontier. Want: bottleneck = search/construction/verification/pattern-finding.

================================================================================
TOP PICK — Constructive periodic billiard orbits in obtuse triangles ("Great Periodic Path Hunt")
================================================================================

STATUS (web-verified):
- Existence of a periodic billiard orbit in EVERY polygon was a Katok "Five Most Resistant
  Problems in Dynamics" (Problem 3(ii)). NEW: Giovanni Forni, "Existence of a Periodic Orbit for
  Billiards in Polygons", arXiv:2606.10102, submitted 2026-06-08, proves EVERY finite polygon has
  a periodic orbit — but the proof is NON-CONSTRUCTIVE (proof by contradiction via
  Galperin–Krüger–Troubetzkoy dynamics + scaled-metric cut-locus topology). It does NOT produce
  explicit orbits and does NOT extend the constructive obtuse-triangle threshold.
- CONSTRUCTIVE state of the art for OBTUSE TRIANGLES:
  * Hooper–Schwartz (McBilliards) + Schwartz "100 Degree Theorem" (Exp. Math. 2008/2009):
    every obtuse triangle with big angle <= 100 deg has a STABLE periodic path (computer-assisted,
    exact arithmetic).
  * Garber–Marinov–Moore–Tokarsky, "One Hundred and Twelve Point Three Degree Theorem"
    (arXiv:1808.06667, 2018): threshold pushed to 112.3 deg (no stability claim).
  * Tokarsky's ongoing "Great Periodic Path Hunt" (gwtokarsky.github.io, active 2023–2025):
    covering the parameter triangle Δ = {acute angles (x,y)} with explicit "orbit tiles" O(W)
    (each W = a combinatorial word / orbit type whose unfolding corridor is non-empty, verified by
    EXACT integer arithmetic). Recent coverings: Aug-2023 region with vertices (6,39)-(10,35)-
    (10,57.6)-(6,61.6); Aug-2024 region (6,29)-(10,25)-(10,35)-(6,39) by Tokarsky + Huang, Huang,
    Lu, Mai, Mastel.

WHAT IS GENUINELY OPEN (the real gap, post-Forni):
1. The CONSTRUCTIVE/EXPLICIT problem: produce explicit orbit-types covering ALL obtuse triangles.
   Forni's abstract existence does NOT give you the orbit. The hunt's deliverable — an explicit,
   exact-arithmetic-certified periodic word W for each triangle — is a strictly stronger, still-open
   object. Concrete uncovered regions as of 2024–2025:
   (a) "one tiny flare around (15,30)" — a specific small hole with all angles > 11 deg still
       uncovered.
   (b) the strip of big-angle between ~112.3 deg and the right-angle/degenerate limits — no explicit
       coverage; the heuristic McBilliards belief is "works below 5π/8 = 112.5 deg, undecided above".
   (c) approach to the right-angle limit (big angle -> 90+, thin triangles) where corridor widths
       shrink and word length blows up — the hard computational régime.
2. STABILITY: GMMT's 112.3-deg orbits are not claimed stable; Schwartz's <=100 are. Upgrading
   coverage to STABLE orbit tiles (which then persist on open neighborhoods) is a separate, partly
   open refinement.

WHY THIS FITS OUR EDGE (tight match):
- Bottleneck IS search + construction + verification, not deep analysis. Finding a periodic word W
  for a target sub-region = depth-first search over combinatorial words + pruning (exactly
  McBilliards' loop). Our "clever/structured search + adversarial falsify" is the right tool.
- VERIFICATION is exact-integer / dyadic-rational arithmetic on the unfolded corridor — precisely
  our certified-arithmetic strength, and FORMALIZABLE: an orbit tile's non-emptiness is a finite
  system of rational linear inequalities (corridor = intersection of half-planes after unfolding).
  This is a clean Lean/Aristotle target — "this explicit word W gives a periodic orbit for every
  triangle in this rational box" is a decidable, machine-checkable statement. To our knowledge NO
  formally-verified (Lean) orbit-tile certificate exists — that alone is a fresh, citable artifact.
- Independently checkable: anyone can re-unfold W and check the inequalities.
- Modest compute: covering one new sub-region is laptop-scale (the hunt runs on laptops +
  occasional supercomputer verification), not FLOPS-bound.

CONTRIBUTION SHAPES (concrete, verifiable, weeks-scale):
- (Strongest, novel) FORMALLY VERIFY (Lean) a periodic-orbit-tile certificate: pick a region the
  hunt has covered numerically and turn its orbit word(s) into a sorry-free Lean proof that the
  corridor is non-empty over the stated rational box. First machine-verified billiard orbit tile.
- Cover (and exact-arithmetic certify) a NEW uncovered sub-region — e.g. attack the (15,30) flare
  with a structured word search + interval/exact corridor test; deliver explicit W + certificate.
- Push an explicit orbit tile into the 112.3–115 deg band (a concrete numeric advance on the
  constructive threshold, even a single new tile is publishable in the hunt's idiom).
- Sharp NEW conjecture: characterize the worst-case word-length growth as big-angle -> right-angle
  / as a function of distance to the (15,30) hole, backed by certified data — a quantitative
  "constructive complexity" statement the abstract Forni proof says nothing about.

NOVELTY / OWNERSHIP:
- Existence: now OWNED by Forni (2026, non-constructive) — do NOT attempt the abstract existence.
- Constructive coverage: PARTLY-OWNED, ACTIVE collaborative frontier (Tokarsky's hunt is explicitly
  open to contributors who are assigned uncovered regions). This is a Polymath-style live frontier,
  NOT saturated.
- Formal verification of orbit tiles: OPEN / un-owned as far as web search shows — our differentiator.

HARDEST PART / FAILURE MODES (honest):
- The (15,30) flare may be hard precisely because required words are long / corridors thin — search
  could blow up; mitigation = structured/heuristic word generation (McBilliards' pruning) + exact
  test, not blind enumeration.
- A formally-verified tile is "only" a verification contribution (the math is GMMT/Tokarsky's) —
  modest novelty, but a genuine first and squarely in our wheelhouse; pair with a NEW region for
  mathematical content.
- Right-angle limit is genuinely open and may resist a single-region push (don't overpromise full
  closure of the constructive problem).

================================================================================
RUNNER-UP A — Garsia entropy / dimension of Bernoulli convolutions at explicit algebraic params
================================================================================
STATUS (web-verified):
- For algebraic β∈(1,2): dim_H(ν_β) = min{1, H(β)/log β}, H = Garsia entropy (Hochman; Breuillard–
  Varjú). Hare–Kempton–Persson(–et al.), "Computing Garsia entropy for Bernoulli convolutions with
  algebraic parameters", Nonlinearity 34 (2021) 4744 — computer-assisted LOWER bounds proving
  dim = 1 on open regions of a parameter space of non-Pisot/non-Salem algebraic integers.
  (NOTE: the arXiv:1912.10987 version is WITHDRAWN "coauthor disagreement"; cite the Nonlinearity
  published version, not the arXiv preprint — UNVERIFIED whether content differs; flag this.)
- OPEN: the precise set of algebraic β∈(1/2,1) [equiv. β∈(1,2)] with dim ν_β < 1 is unknown; only
  Pisot reciprocals are known-singular (Erdős 1939) + a few explicit non-Pisot singular examples
  (Salem-number / non-Pisot constructions, e.g. arXiv:1708.05544 "Singular non-Pisot Bernoulli
  convolutions"). Whether any λ with λ^{-1} non-Pisot is singular is OPEN.
FIT: certified computation of Garsia entropy at a SPECIFIC algebraic β = exact-arithmetic / interval
job (count word-collisions, bound entropy) — our strength; verifiable; modest compute. Contribution:
certify dim ν_β = 1 (or a sharp lower bound) for a NAMED β not yet covered (e.g. a specific small
Salem number), or Lean-verify an existing Garsia-entropy lower-bound certificate.
RISK: this is closer to "the deep-analytic frontier" at the margins (the singular/abs-cont dichotomy
is hard); but the per-β LOWER-BOUND certification is genuinely combinatorial/finite and tractable.
Slightly more owned (Hare–Kempton–Persson, Pollicott) than the billiard hunt.

================================================================================
RUNNER-UP B — Computer-validated open spectral gaps, almost Mathieu at critical coupling
================================================================================
STATUS (web-verified): "Computer Validation of Open Gaps for the Almost Mathieu Operator with
Critical Coupling", arXiv:2410.18536 (Oct 2024) — a FRESH computer-assisted-proof line validating
that specified spectral gaps are open (Dry Ten Martini-flavored, critical coupling). This is an
exact/interval-certified verification problem.
FIT: certified-numerics + potential Lean target. RISK: closer to spectral theory (our "avoid"
deep-analytic edge); the hard cases are analysis-bound. Keep as a watch item, not a primary target.
Caveat: AMO sits near the quasiperiodic-Schrödinger world; verify it is far enough from our owned
Hecke/Maass corner before committing (it is — different object — but the "spectral" flavor is a
yellow flag against our stated edge).

================================================================================
DISCARDED / NOTED (do not re-chase)
================================================================================
- Lorenz attractor SRB / mixing: existence + computability already done (Tucker; Isabelle/HOL
  verified ODE solver), mixing proven (Luzzatto–Melbourne et al.). Saturated; remaining mixing-RATE
  questions are analysis-bound. SKIP.
- General triangle existence: SETTLED by Forni 2026 (non-constructive). Do NOT attempt existence.
- Furstenberg/random-matrix Lyapunov exponents: active (Pollicott algorithm, quantitative
  analyticity 2024–2026) but the headline conjectures are analysis-bound; per-value certified
  computation is possible but largely OWNED by Pollicott-style transfer-operator methods. Lower
  priority.

================================================================================
RECOMMENDATION
================================================================================
PRIMARY: join the constructive obtuse-triangle billiard frontier with TWO deliverables —
(1) a Lean/Aristotle-verified orbit-tile certificate (first of its kind), and (2) an exact-arithmetic
covering of a NEW uncovered sub-region (target the (15,30) flare or a 112.3–115 deg tile). Existence
is owned by Forni; the EXPLICIT/CERTIFIED coverage is open, collaborative, search-and-verify-bound,
and exactly our edge. Backup: per-β Garsia-entropy certification for a named algebraic parameter.

SOURCES (web-verified 2026-06-20):
- Forni, arXiv:2606.10102 (2026-06-08) — every polygon has a periodic orbit (non-constructive).
- Schwartz, "Obtuse Triangular Billiards II: 100 Degrees..." Exp. Math. 18 (2009).
- Garber–Marinov–Moore–Tokarsky, arXiv:1808.06667 (2018) — 112.3 deg theorem.
- Hooper–Schwartz, "Introduction to McBilliards" (math.brown.edu/reschwar/Papers/mcb.pdf).
- Tokarsky, "The Great Periodic Path Hunt", gwtokarsky.github.io (active 2023–2025).
- Quanta Magazine, "The Mysterious Math of Billiards Tables", 2024-02-15 (status overview).
- Hare–Kempton–Persson et al., "Computing Garsia entropy...", Nonlinearity 34 (2021) 4744
  (arXiv:1912.10987 WITHDRAWN — cite published version).
- "Singular non-Pisot Bernoulli convolutions", arXiv:1708.05544.
- "Computer Validation of Open Gaps for the Almost Mathieu Operator...", arXiv:2410.18536 (2024).

CAVEATS:
- arXiv:1912.10987 is WITHDRAWN; rely on the Nonlinearity 2021 published version (UNVERIFIED content
  match).
- Forni 2026 is a very recent (June 2026) preprint; abstract read directly, full-text constructive
  caveats inferred from abstract + the standing literature (GKT non-constructive lineage) — mark the
  "explicitly leaves constructive problem open" as STRONGLY-IMPLIED, not verbatim-quoted.
- The (15,30) flare and 112.3-deg threshold are reported via Tokarsky's hunt pages + Quanta + GMMT;
  exact current coverage map should be re-checked on gwtokarsky.github.io before committing compute.

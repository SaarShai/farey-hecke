# Hunt D5 — Experimental Mathematics: Identity / Closed-Form / Sequence Discovery

Date: 2026-06-20 (dated per assignment label). Web-verified June 2026.
Domain: Computer-discovered + certified identities (Ramanujan-Machine paradigm,
PSLQ/lattice-reduction, OEIS phenomena), then proved/verified.

## Bottom line

This domain matches our edge STRONGLY on the search/construction/verification
axes — but the "discover a brand-new fundamental-constant identity" headline is
now a CROWDED, well-funded frontier (Ramanujan Machine group: Nature 2021, PNAS
2024, NeurIPS 2024/2025, conservative-matrix-field machinery). We should NOT try
to out-discover them on raw conjecture generation.

The genuinely open + tractable + verifiable sub-niche that survives the hard
filter is the **Machin-like arctangent relation / Lehmer-measure search**: a
pure search+construction+exact-certification problem, NOT owned by a big group,
where the records literally moved in Aug 2025 and the authors explicitly list
open search directions they did NOT cover. This is our best pick. A close second
is **machine-checked (Lean) proof of specific still-open Ramanujan-Machine
continued-fraction conjectures** (verification edge, but proof-analytic, weaker
fit).

---

## Landscape (web-verified)

### A. Ramanujan Machine ecosystem — largely OWNED, fast-moving
- Original: Raayoni et al., *Nature* 590 (2021) 67 — "Generating conjectures on
  fundamental constants with the Ramanujan Machine."
- Proof progress: arXiv:2403.09729 (Mar 2024) proved 38 conjectures (differential
  equation / Petkovšek), generalized 31. So the easy ones are being cleared.
- arXiv:2403.09729 + Franel-number CF conjecture proof (Math. Intelligencer 2025,
  s00283-025-10497-9). π/4 non-canonical CF formal proof (Jan 2026).
- Structural engine: **Conservative Matrix Field** (David, arXiv:2303.09318;
  PNAS 2024 "intrinsic order among mathematical constants," 2321440121;
  arXiv:2507.08138 "Continuous Asymptotics and Arithmetic"). Unifies CF formulas,
  routes toward irrationality measures. This is the group's deep machinery.
- **Euler2AI** (arXiv:2502.17533, "From Euler to AI: Unifying Formulas for
  Mathematical Constants," NeurIPS 2025): LLM-harvest hundreds of π formulas from
  arXiv, UMAPS unification via coboundary equivalence; 94% of formulas connected,
  43% inside one Conservative Matrix Field. Ramanujan Library hypergraph
  (arXiv:2412.12361, Dec 2024).
- VERDICT: conjecture-GENERATION and the unification/irrationality-measure
  program are OWNED by a coordinated, resourced group. Avoid competing there.
  Their OPEN residue = many individual unproven CF conjectures (see candidate 2).

### B. Machin-like / Lehmer-measure search — OPEN + matches us (TOP PICK)
- Machin-like formula: π/4 = Σ c_k · arctan(1/n_k) (or arctan(a/b)); efficiency
  measured by **Lehmer's measure** λ = Σ 1/log10(arg^-1). Lower λ = fewer terms
  computed for given digits. Classic competitive niche (Wetherfield, Hwang
  Chien-Lih, Störmer; tracked historically on Wetherfield's MachinFormula pages).
- **arXiv:2508.08307** (Aug 2025), "Constrained PSLQ Search for Machin-like
  Identities Achieving Record-Low Lehmer Measures": couples PSLQ with
  Gaussian-integer (prime-group) number-theoretic filters. NEW RECORDS:
  - 5-term: λ = 1.4572 (beats Störmer 1896, λ = 1.7320)
  - 6-term: λ = 1.3291 (beats Hwang Chien-Lih 1997, λ = 1.5124)
  - Found 708,024 relations with λ < 1.86 across 2–15 terms.
- CRUCIALLY the authors state the search is **NOT exhaustive** and list explicit
  open directions:
  1. arctan relations with numerators ≠ 1 (arctan(a/b), a>1) under-explored.
  2. prime-group selection "didn't cover the whole space."
  3. OPEN THEORY QUESTION: is the number of arctan relations of a given length
     finite? (would give bounds on required primes).
- Why this fits US: it is *literally* constrained lattice-reduction search +
  exact (Gaussian-integer) arithmetic + a verification step (each candidate
  relation is an EXACT algebraic identity checkable by symbolic arctan addition /
  the Störmer–Todd Gaussian-integer factorization — bulletproof, independently
  re-checkable). Our fleet+falsify+exact-arith+Lean stack is a near-perfect tool
  match, and modest compute suffices (it's structured search, not raw FLOPS).

### C. OEIS unexplained phenomena — DIFFUSE, case-by-case
- OEIS has thousands of "conjectured formula / no proof" entries; Zeilberger-style
  "Prove or Disprove: 100 Conjectures from the OEIS" (math/0409509) is the genre.
- Fit: real but unfocused. Each is a one-off; no single concentrated target.
  Better as opportunistic side-quests than a campaign. NOT a top pick.

### D. Adjacent benchmarks (context, not targets)
- HorizonMath (arXiv:2603.15617), AI-for-math surveys (2606.08728). These measure
  AI discovery; not problems to solve.

---

## Candidates (ranked)

1. **Machin-like / Lehmer-measure record search** (TOP). Push 5–8+ term records
   below the Aug-2025 bar; systematically attack the arctan(a/b), a>1 family and
   the unexplored prime groups; OR settle the finiteness-per-length sub-question
   for small lengths with a certified (non-)existence argument. Status: ACTIVE,
   open, records moved Aug 2025, authors named the gaps. Verifiable: each
   identity is an exact algebraic check.

2. **Lean/Aristotle machine-proof of specific open Ramanujan-Machine CF
   conjectures.** Status: dozens still posted "open" on ramanujanmachine.com
   (e.g. 1/(1−ln2), 1/(2G) Catalan, various ζ-value CFs). Fit: our verification
   edge; but the bottleneck is finding the proof (often Petkovšek/D-finite/
   coboundary), which is analytic — weaker fit, and the easy ones are being
   cleared by the group. Good as a "certify a witness" play if we PSLQ-discover a
   companion identity first.

3. **OEIS closed-form / congruence hunt.** Pick high-interest unexplained
   sequences, PSLQ a closed form or g.f., then prove (creative telescoping). Fit
   ok but diffuse; opportunistic only.

4. **New Machin-like-style identities for OTHER constants** (ln2, Catalan G, ζ(3))
   via the same Gaussian/Eisenstein-integer constrained search — the 2508.08307
   method is π-specific; generalizing the constrained-PSLQ + algebraic-integer
   filter to other arctan/arccoth-expressible constants is a clean, owned-by-
   nobody construction target.

---

## Top pick — precise statement

**Beat the Aug-2025 Machin-like Lehmer-measure records and/or map the
under-explored regions the authors flagged, with every output an EXACTLY
certified arctangent identity.** Concretely, one or more of:
 (a) a 5-, 6-, 7-, or 8-term π/4 Machin-like relation with Lehmer measure strictly
     below the current best (5-term < 1.4572, 6-term < 1.3291; 7-term improve on
     Wetherfield 2003);
 (b) the first systematic certified sweep of arctan(a/b) (a>1) relations, which
     2508.08307 left under-explored;
 (c) a certified finiteness / non-existence statement for arctan relations of a
     fixed small length L below a Lehmer threshold (the open theory question),
     even just for L ≤ 6 over a bounded prime set.

Each deliverable is an exact identity verifiable by Gaussian-integer
factorization of (a+bi) — independently checkable to the last bit, ideal for a
Lean certificate.

## Why our edge fits
- Constrained PSLQ + algebraic-integer (Gaussian/Eisenstein) filters = exactly
  "structured/clever search," not brute FLOPS. We can run the fleet to partition
  the prime-group space the authors admit they didn't cover.
- Adversarial falsification kills spurious near-relations (PSLQ false positives)
  fast — a known failure mode this domain has, and our core strength.
- Exact/interval arithmetic + Lean turns each surviving candidate into a
  bulletproof, independently verifiable identity (a genuine differentiator vs the
  numerics-only literature).
- Modest-compute-friendly: the bottleneck is the cleverness of the prime-group
  constraint and the lattice reduction, not machine size.

## Tractability (honest)
- Realistic in weeks for (a) and (b): re-implement constrained PSLQ + Gaussian-
  integer filter (open-source: euler2ai repo + standard PSLQ), then sweep prime
  groups they skipped. A single improved record is a concrete, citable, verifiable
  contribution.
- Hard part: the 2508.08307 team already ran a large search; the low-hanging
  records may be gone, so we need a genuinely better constraint (their stated
  gaps — numerator>1, prime-group coverage — are the opening). Risk we fail = the
  remaining gains are tiny/diminishing and not worth a paper.
- (c) finiteness-per-length is more analytic (number-theoretic, ties to Størmer's
  theorem / S-unit equations) — higher reward, harder; treat as stretch.

## Novelty / ownership
- Records (a): OWNED only up to Aug-2025 by Störmer/Hwang/Wetherfield/2508.08307;
  any strict improvement is a clean, new, owned-by-us contribution.
- (b) arctan(a/b) sweep + (4) other-constant generalization: essentially
  UNCLAIMED — explicitly named as not-done by 2508.08307.
- (c): the finiteness question is OPEN and named by 2508.08307; partial certified
  results would be novel.
- NOT in the forbidden corner (no Maass/QUE/arithmeticity); orthogonal to our
  Hecke work.

## Caveats / honesty
- The Ramanujan-Machine *headline* (discover fundamental-constant CFs) is OWNED
  and resourced — do NOT compete on conjecture generation or the
  conservative-matrix-field / irrationality-measure program (deep-analytic, their
  turf).
- The Machin-like niche is real but MODEST in prestige (computational π-formula
  efficiency, niche audience of π-digit / arctan-identity enthusiasts). Honest
  reach ≈ our Hecke work: solid, verifiable, niche — not broad-impact.
- PSLQ "discoveries" are conjectural until the algebraic identity is closed; the
  value-add must be the EXACT certification, else it's just numerics others can
  redo.
- 2508.08307 is recent (Aug 2025) and may be unrefereed/preprint — verify its
  record claims against Wetherfield's tables before claiming to beat them.

## Sources (web-verified June 2026)
- arXiv:2508.08307 — Constrained PSLQ Search for Machin-like Identities (Aug 2025)
- arXiv:2403.09729 — Proof and generalization of Ramanujan Machine conjectures (Mar 2024)
- Nature 590 (2021) 67 — Ramanujan Machine (Raayoni et al.)
- arXiv:2502.17533 — From Euler to AI / Euler2AI (NeurIPS 2025); github RamanujanMachine/euler2ai
- arXiv:2303.09318 / PNAS 2321440121 (2024) — Conservative Matrix Field
- arXiv:2412.12361 — Ramanujan Library hypergraph (Dec 2024)
- arXiv:2507.08138 — Conservative Matrix Fields: Continuous Asymptotics & Arithmetic (Jul 2025)
- Wikipedia: Machin-like formula (Lehmer measure, Wetherfield/Hwang/Störmer records)
- ramanujanmachine.com/prove-our-conjectures — open conjecture submissions list
- arXiv:math/0409509 — Prove or Disprove: 100 Conjectures from the OEIS (genre ref)

LAUNCH PROMPT — Direction 4: Dirichlet Polynomial Avoidance Conjecture (DPAC) — evidence + obstruction characterization (NOT a proof attempt).

You are picking up a mathematics research project cold. Working root:
`/Users/za/Documents/Farey NOW/primes-equispaced`. First run `./te doctor`,
read `start.md`, and read memory (`/Users/za/.claude/projects/-Users-za-Documents-Farey-NOW/memory/`):
`MEMORY.md`, `project_farey_honest_map.md`, `project_farey_forward_verdict.md`,
**`project_koyama_risk.md` (in full)**. Token Economy is tooling only.

NON-NEGOTIABLE NORMS (project #1 failure mode = novelty/citation/RH-glamour
inflation):
- Adversarial honesty; derive-then-verify; label
  [PROVEN]/[NUMERICAL]/[CONJECTURAL]/[CITATION-UNVERIFIED]; primary-verify
  citations.
- KOYAMA GATING: counterparty UNVERIFIED (`correspondence/KOYAMA.md` RISK +
  `project_koyama_risk.md`). User's OWN work; no email/IP/compute toward
  Koyama; co-authorship unconfirmed; nothing sent/pushed without explicit
  user approval.
- HARD SCOPE CEILING: DPAC for general K is **LI-class** (comparable to the
  Linear Independence hypothesis for ζ-zeros — out of reach). DO NOT attempt
  a general-K proof or claim RH/LI progress. The only honest contributions
  are: (i) a clean, build-verified *formal statement*; (ii) extended
  *numerical avoidance evidence*; (iii) a precise *characterization of the
  obstruction*. Conjecture-with-evidence tier, nothing more.

STATEMENT: for fixed K ≥ 2, the truncated Möbius Dirichlet polynomial
`c_K(s) = Σ_{k=2}^{K} μ(k) k^{−s}` is nonzero at every nontrivial zero of
`riemannZeta`. `c_K` itself has infinitely many critical-strip zeros
(Langer 1931); the content is that none coincide with a ζ-zero.
Unconditional for K∈{2,3,4}; general K open, LI-class.

ARTIFACTS (in-repo): `formal-conjectures/DPAC_full.lean`,
`DPAC_closure_attempt.lean`, `DirichletPolynomialAvoidance.lean`. A cleaned,
build-verified version (`@[category research open, AMS 11]`, concrete
statement against Mathlib `riemannZeta`, `lake --wfail build` green on Lean
v4.27.0) is in **open draft PR #3716** to google-deepmind/formal-conjectures
(branch `farey-spectroscopy-conjectures`; see
`handoff-2026-05-16-D3-functionfield/FORMAL_CONJECTURES_PR_READINESS.md`,
`KR_CITATION_LOCK.md`, and `formal_conjectures_submission/`). Maintainer
`mo271` reviews; PR is DRAFT. `gh` is installed at `~/.local/bin/gh`;
GitHub auth is the user's (do not assume; verify `gh auth status`).

TASK (pick per user priority):
1. **Numerical evidence extension.** Rigorously (interval arithmetic,
   certified) verify `c_K(ρ) ≠ 0` for more K (beyond {10,20,50}) at more
   nontrivial ζ-zeros (beyond the first 100); produce a certified table +
   reproducible harness; quantify the empirical "avoidance margin"
   honestly (no over-interpretation of the 9×–52× ratios — re-derive,
   don't repeat prior framing).
2. **Obstruction characterization.** Precisely state what would close
   general-K (the FiniteLogRatioLI / Pólya-discreteness + avoidance
   certificate route in `DPAC_closure_attempt.lean`); make the LI-class
   reduction explicit and honest; do NOT attempt to discharge it.
3. **PR stewardship.** If `mo271` / maintainers comment on PR #3716,
   address feedback (conventions, `lake --wfail build` must stay green,
   no placeholder defs, de-inflated docstrings). Respond honestly;
   leave DRAFT unless maintainers move it; nothing pushed without explicit
   user approval.

GATES / done: certified numerics double-checked; the LI-class ceiling
stated plainly everywhere (no proof claim); deliverable = certified
evidence table + honest obstruction note + a clean PR state. Record durable
facts to wiki/memory; commit; no external send/push without explicit user
approval.

LAUNCH PROMPT — Direction 2: the "Dominance of −1" Chebyshev-bias hierarchy as standalone experimental number theory.

You are picking up a mathematics research project cold. Working root:
`/Users/za/Documents/Farey NOW/primes-equispaced`. First run `./te doctor`,
read `start.md`, and read these memory files (user auto-memory dir
`/Users/za/.claude/projects/-Users-za-Documents-Farey-NOW/memory/`):
`MEMORY.md`, `project_farey_honest_map.md`, `project_farey_forward_verdict.md`,
and **`project_koyama_risk.md` (read this in full before any Koyama-facing
action)**. Token Economy (`./te`, skills/, hooks/) is tooling only.

NON-NEGOTIABLE NORMS (this project's #1 documented failure mode is
novelty / citation / RH-glamour inflation):
- Adversarial honesty. Derive-then-verify. Label every claim
  [PROVEN] / [NUMERICAL] / [CONJECTURAL] / [CITATION-UNVERIFIED]. Verify
  citations against primary sources; never fabricate theorem numbers.
- KOYAMA GATING: this strand is adjacent to the Koyama "Dominance of −1"
  collaboration, whose counterparty is UNVERIFIED (see
  `correspondence/KOYAMA.md` RISK section + `project_koyama_risk.md`).
  Pursue this as the USER'S OWN independent experimental work. Do NOT email
  Koyama, send IP/PDF/code to him, spend money on compute "for the grant",
  or treat co-authorship as confirmed. Nothing is sent/pushed without
  explicit user approval.
- Honest scope ceiling: this is Experimental-Mathematics / specialist tier,
  NOT a breakthrough, NOT RH progress. Calibrate all framing accordingly.

BACKGROUND (real, published): Aoki–Koyama, "Chebyshev's bias against
splitting and principal primes in global fields," J. Number Theory 245
(2023); Rubinstein–Sarnak 1994. The phenomenon: a hierarchy of bias among
quadratic non-residue classes mod N, with −1 mod N conjectured dominant.
Existing in-repo machinery: `handoff-2026-05-09-followup/Koyama_*` (sieve +
residue-count code, EC/NDC sweeps), and the Phase-1 replication: two
independent implementations (C++/primesieve + hand-rolled C segmented sieve)
agreeing on every π(x;N,a) for N∈{7,8,11,19,23} to x=1.3·10¹³
(π(1.3·10¹³)=445,831,610,611), identity (3.1) = Dirichlet-character
orthogonality verified at 495 cells (worst residual 1.4·10⁻⁴).

TASK: produce a rigorous, reproducible, standalone experimental-NT study of
the −1-dominance hierarchy as a *dynamic curve in x* (not single endpoints),
extended toward the transient low-lying-zero scale (~e^{33.4} ≈ 3·10¹⁴),
documenting where/which moduli the predicted hierarchy becomes visible and
where low-lying zeros cause transient reversals. Keep the layers separate
(theoretical bias ordering vs raw π(x;q,a)−π(x;q,1) observable vs
finite-range evidence vs asymptotic interpretation). Cross-check everything
two independent ways + identity (3.1). Full provenance (code hash, machine,
runtime, restart logs); reproducible from a single artefact directory.

GATES / done: (a) decision gate before heavy compute — estimate wall-clock
and confirm 3·10¹⁴ is feasible vs settle for 10¹⁴; (b) every headline number
double-verified + (3.1)-consistent; (c) deliverable = a calibrated draft
note (Experimental Mathematics tier) citing Aoki–Koyama + Rubinstein–Sarnak,
honest about what is observed vs conjectured, framed as the user's
independent verification/extension — explicitly NOT a confirmed joint
deliverable. Record durable findings to the wiki/memory; commit; nothing
sent to Koyama or pushed without explicit user approval.

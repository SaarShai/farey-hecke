# GOAL 3 — Unconditional Farey–Mertens structure at the RH boundary

Preliminary map, 2026-08-14. Status: S0 EXECUTED same day — see EXECUTION_LOG
VERDICTS. D2 outcome (b): conjecture WRONG, corrected constant computed.
S = 0.02903 ± 0.00016 (two-sided); 2/π² and 3/π⁴ both excluded; likely first
receipts-grade numeric of the Ng/Gonek constant → new deliverable D2′ =
polish + more zeros + publish alongside the J_{-1} Gonek test (A3). C_W:
both prior growth claims wrong; persistent M-driven fluctuation ⇒ restate as
log-average. S1 (Kloosterman gate spec) is now the live front.
This is the sanctioned salvage lane (breakthrough-picks 2026-07-02), NOT a
re-pivot to per-step significance claims (see DO-NOT-RE-CHASE). Scope is
three bounded deliverables with hard gates.

## Aim

Extract unconditional theorems and exactly-determined constants from the
Farey/Mertens boundary where RH lives (Franel–Landau: RH ⟺
W(N) = O(N^{−1+ε})), without touching the RH-coupled statements themselves:

- D1: **DiscrepancyStep theorem** — prove unconditionally, via
  Kloosterman/Weil control of residue-permutation variance, that
  M(p) ≤ −3 ⇒ the exact integral observable inequality (N+B+C > A) holds.
- D2: **Settle the ζ′(ρ) zero-sum constant** — resolve the live conflict:
  log.md conjectures Σ_ρ 1/(|ρ|²|ζ′(ρ)|²) = 2/π² (from the Mikolás L²
  constant 2/3); the mimo E5 probe measured S(N=100)=0.0141 vs 0.2014
  expected. Either a new zeta-zero-sum identity (Ng-adjacent) or a clean
  refutation with the correct constant — both are new facts.
- D3: **Priority note** — the honest Exp.Math-tier note (Bridge identity
  Σ_{f∈F_{p−1}} e^{2πipf} = M(p)+2 Lean-proved + certified counterexample
  p=92,173 + exact-observable kill-test data), citing García 2025. Locks
  priority; already USER-sanctioned.

## Why this is RH-relevant

Franel–Landau makes Farey discrepancy an RH-equivalent object. Every
unconditional structural theorem about its increments narrows the corridor in
which RH-relevant oscillation can occur — the same "move a measurable
boundary" shape as the article's 41.6% → 67.2%. The zero-sum constant is a
concrete statement about ζ′ at the zeros (the family of quantities behind
M(x) = −Σ x^ρ/(ρζ′(ρ)) + …), where any exactly-determined new constant is
citable structure.

## What we already hold (verified)

- Bridge identity Lean-proved unconditional (FareyBridgeIdentity.lean).
- Exact prime-step machinery frozen + tested: E_p−E_{p−1} =
  ((p−1)/6p)(2−A(p−1)), A(x)=Σ M(⌊x/m⌋)/m, Σ a(n)/n^s = ζ(s+1)/ζ(s);
  first negative prime 8501 finite-certified; exact-fraction kernel + tests
  (projects/prime-step-breakthrough).
- Certified counterexamples: p=92,173 (sign conjecture), p=237,733 / 243,799
  (B-positivity, cross-term) — the honest-note core.
- Kill-test infra: integral_farey_kill_test.py, 4,617-prime exact scan,
  NO_SUPPORT_TO_LIMIT verdict machinery.
- The binding-piece analysis: notes state DiscrepancyStep needs "arithmetic
  info beyond PNT+Cauchy–Schwarz", NOT necessarily RH; Ustinov-style
  Kloosterman control is the identified route (Kloosterman prior art located:
  Nakamura 1401.2980, Matomäki 2009 in-repo citations).
- Mikolás L² constant 2/3 derivation + Q=500k numeric N·W = 0.6667; NW(Q)→C
  ≈ 0.679 ± 0.002 note; Σ M(n)²/n³ = 1.13616230745460 candidate constant.
- García 2025 prior-art boundary fully mapped (cite, never claim the
  Mertens↔discrepancy link as novel).
- IMPORTED 2026-08-14 (research_notes/imported_farey_now/, from the Farey NOW
  snapshot):
  - Smoothed_Dwf_explicit_formula_VERIFIED.md + T2_Lean_SmoothedDwf_REPORT.md
    — rigorous smoothed Möbius explicit formula Σ μ(n)W(n/N) = R₀ +
    2ℜ Σ_{γ>0} N^{½+iγ} M_W(½+iγ)/ζ′(½+iγ) + R_triv + E_A; R₀ = −2 exact;
    verified >10 digits (N=10⁵, 200 zeros); Lean residue chain proved, final
    assembly an explicit axiom, simple-zero hypothesis H3. The ready-made
    ζ′(ρ)-weighted zero-sum machine for D2.
  - Delta_machine_paper_theorem_registry.md — the constant family
    C_W^(k) = κ_k Σ_{γ>0} |M_W(ρ)|/|ζ′(ρ)|^k with status buckets.
  - SELBERG_INPUT_DISPROVED.md — Σ M(n)²/n² ~ (6/π²)log x is FALSE
    (ratio 0.28 at 5·10⁵, decreasing); AND records the known RH-conditional
    value (1/x)Σ M(n)² → Σ_ρ 1/(|ρ|²|ζ′(ρ)|²) ≈ 0.03.
  - FRANEL_LANDAU_LOWER_BOUND.md — unconditional Σ D² ≥ c·N³ (C_W(N) ≥ c₀);
    empirical C_W ≈ 0.16 + 0.24·log log N fit (audit before trusting).
  - EXPLICIT_FORMULA_RIGOROUS.md / EXPLICIT_FORMULA_ZEROS_DELTAW.md /
    MERTENS_AT_ZEROS.md — proved-vs-formal step separation; Ramanujan
    σ_a σ_b Dirichlet-series identity; partial Euler products at L-zeros.

## Headline NEW facts targeted

1. D1 theorem (JNT-tier if it lands): first unconditional sign-structure
   theorem for Farey discrepancy increments under a Mertens condition.
2. D2 constant: the true value (or refutation + corrected form) of the
   ζ′(ρ) zero sum — plus, if the 2/π² form survives, the bridge "Mikolás 2/3
   ⟺ zero-sum 2/π²" as a conditional equivalence with certified numerics at
   high zero count.
3. D3 note: priority-locking publication of the exact identities +
   counterexamples (modest tier, honest framing).

## Stage ladder with falsification gates

- **S0 (2–3 d).** D2 disambiguation FIRST (cheap, pure computation). Strong
  prior from the 2026-08-14 import: the literature-known RH-conditional value
  is Σ_ρ 1/(|ρ|²|ζ′(ρ)|²) ≈ 0.03 (Gonek/Ng circle; SELBERG_INPUT_DISPROVED
  records it), the E5 partial sum 0.0141 at 100 zeros is consistent with slow
  convergence toward ≈0.03, and the log.md 2/π² ≈ 0.2026 bridge therefore
  likely carries a normalization error. S0 = recompute with 10^4–10^5 zeros
  (mpmath/Arb ζ′(ρ)), locate the factor error in the Mikolás-2/3 → 2/π²
  derivation, and use the imported smoothed-Dwf formula (M_W/ζ′ weights) as
  the controlled setting. ALSO settle the newly surfaced second conflict:
  NW(Q) → 0.679 bounded (current note) vs C_W(N) ≈ 0.16 + 0.24·log log N
  slowly divergent (imported note) — same quantity, incompatible claims.
  GATE: identify (a) conjecture correct, (b) conjecture wrong with correct
  constant identified, or (c) divergent/ill-posed — all three recordable.
- **S1 (1–2 wk).** D1 probe per the 2026-07-02 spec: Kloosterman/Weil bound
  on the residue-permutation variance a ↦ pa mod b behind the N+B+C > A
  inequality for M(p) ≤ −3. GATE (pre-registered): if the variance bound
  falls short by a power of p (not just constants), record NO-GO and stop —
  this gate was designed to prevent the RH-coupled trap.
- **S2 (1 wk, parallel).** D3 note assembly from equispaced_honest_note.md +
  FACTS ledger; García citation; submit path per USER gate.
- **S3 (2–3 wk, only if S1 gate passes).** Full D1 theorem write-up +
  Aristotle/Lean of the finite lemmas + adversarial referee.
- **S4 (optional).** If D2 lands as a theorem-with-evidence: short note tying
  the Mikolás constant to the zero sum (conditional statement, honest tier).

## Kill criteria / risks

- S1 is genuinely open — treat the NO-GO gate as binding; do NOT continue
  into RH-coupled territory on failure (that exact trap is documented).
- D2 outcome (c) (slow/conditional convergence — the sum over zeros may need
  RH + simplicity to even be well-defined in the intended sense): then the
  deliverable is the corrected statement + numerics, not a theorem.
- Prior-art: zero sums Σ 1/(ρ ζ′(ρ)) variants have literature (Guo,
  Milinovich–Ng school). Focused scout before claiming D2 novelty.
- Scope discipline: no practical/QMC claims (dead), no "RH progress" claims
  (the honest-note language is already correct — keep it).
- NEVER build on Σ M(n)²/n² ~ (6/π²)log x — disproved (imported
  SELBERG_INPUT_DISPROVED.md); any mean-square Mertens input must be checked
  numerically before use (that note's lesson).
- The imported FRANEL_LANDAU_LOWER_BOUND "Theorem" label is UNAUDITED by us —
  independent proof audit required before citing it.

## First 3 actions

1. D2 recomputation script: exact target sum(s), 3 candidate forms, high-zero
   convergence table (scratch → research_notes/rh_goals_2026-08-14/).
2. Pull the DiscrepancyStep binding-piece note + write the S1 pre-registered
   gate spec (what bound suffices, what falls short).
3. Assemble D3 note skeleton from the FACTS ledger (no submission without
   USER gate).

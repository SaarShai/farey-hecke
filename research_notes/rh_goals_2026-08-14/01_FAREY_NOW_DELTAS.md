# Farey NOW snapshot deltas relevant to the RH goals — 2026-08-14

Source sweep: codex gpt-5.6-luna xhigh, diff-driven, read-only.
Snapshot: '/Users/za/Documents/Farey NOW' (non-git sibling). 23,769 files exist
only there; 109 differ. Items below are absent from farey-hecke (or older
divergent versions) and bear on the goal triad. IMPORTED 2026-08-14: all
items below (17 files incl. EXPLICIT_FORMULA_ZEROS_DELTAW.md) copied to
research_notes/imported_farey_now/ with sha256 provenance (PROVENANCE.md);
goal maps updated same day.

## Directly useful for GOAL 3 (Mertens / zero-sum lane)

1. `primes-equispaced/formal-conjectures/SmoothedDwfFormula_aristotle_result_extract/aristotle_dispatch_p3b_aristotle/Smoothed_Dwf_explicit_formula_VERIFIED.md`
   + `T2_Lean_SmoothedDwf_REPORT.md` — smoothed Möbius explicit formula
   Σ μ(n)W(n/N) = R₀ + 2ℜ Σ_{γ>0} N^{½+iγ} M_W(½+iγ)/ζ′(½+iγ) + R_triv + E_A,
   numerically verified >10 digits at N=10⁵ with 200 zeros; Lean 373 LOC,
   29 theorems, residue chain proved, final assembly AXIOM (boundary explicit;
   simple-zero hypothesis H3). This is exactly the ζ′(ρ)-weighted zero-sum
   machinery Goal 3 D2 needs. TOP IMPORT.
2. `primes-equispaced/paper/Delta_machine_paper_theorem_registry.md` — the
   constant family C_W^(k) = κ_k Σ_{γ>0} |M_W(ρ)|/|ζ′(ρ)|^k with
   theorem/proposition/conjecture confidence buckets — the D2 target family.
3. `primes-equispaced/experiments/EXPLICIT_FORMULA_RIGOROUS.md` — clean
   separation of proved Perron/Fourier steps vs the uncontrolled ΔW(p)
   extraction ("NOT a theorem"); prevents re-deriving known-formal steps.
4. `primes-equispaced/experiments/SELBERG_INPUT_DISPROVED.md` — NEGATIVE:
   Σ_{n≤x} M(n)²/n² = (6/π²)log x + O(1) is FALSE (measured ratio 0.28 at
   N=5·10⁵). Blocks a tempting mean-square input; also calibrates the
   Σ M(n)²/n³ = 1.13616... candidate constant (different exponent — still
   alive, but audit against this negative first).
5. `primes-equispaced/experiments/FRANEL_LANDAU_LOWER_BOUND.md` — snapshot
   claims an unconditional lower bound Σ D² ≥ N³/100 ("Theorem"-labeled,
   unaudited by us) + empirical C_W(N) ≈ 0.16 + 0.24 log log N; RH ⟺
   Σ D² = O(N^{3+ε}) normalization. Audit before use.
6. `primes-equispaced/experiments/MERTENS_AT_ZEROS.md` — partial Euler
   products at L-zeros ≈ L′(ρ,χ)/ζ(2) · 1/log K (ratios 0.86–0.98 at K=10⁶,
   computational). DRH/Koyama-adjacent; feeds boundary-Euler-Perron thread.

## Useful for GOAL 1 (detection / DPAC)

7. `primes-equispaced/formal-conjectures/DPAC_aristotle_result_extract/aristotle_dispatch_DPAC_aristotle/DPAC_context.md`
   + `ARISTOTLE_SUMMARY.md` — R_K avoidance ratios 4–16×, 300/300
   interval-certified nonvanishing, density-zero backbone proved,
   dpac_of_LI sorry. Cleanest DPAC evidence packet.
8. `primes-equispaced/experiments/SPECTROSCOPE_DETECTION_THRESHOLD.md` —
   detection statistic F_K(γ) with S/N>3 thresholds (K≥10, P≥1000); draft
   input for the S2 estimator analysis.
9. `primes-equispaced/experiments/LFUNC_BATCH_CROSSOVER_VERIFIED.md` — the
   actual batch-crossover benchmark (2.25×–20×) the spectroscope README
   cites; keeps the audited number, replaces the unaudited README claim.

## Scoped negatives worth preserving (all goals)

10. `primes-equispaced/experiments/MAYER_SPECTRAL_PROOF.md` — why the
    transfer-operator route does NOT prove prime-step monotonicity
    ("Mostly Speculative"); boundary marker between Goal 2 and Goal 3.
11. `primes-equispaced/experiments/DENSITY_ONE_UNCONDITIONAL_BROKEN.md` —
    the old "unconditional density-one" claim was RH-conditional (one
    off-line zero at Re=0.6 dominates); INVALID verdict.
12. `primes-equispaced/experiments/COUNTEREXAMPLE_DELTAWINV_VERIFY.md` —
    p=243,799 counterexample verification detail (B′/C′ decomposition).
13. `primes-equispaced/paper/REFEREE_REPORT_CODEX_FINAL.md` — referee audit
    of the old Δ-machine paper (telescoping-sum contradiction, false
    ΔW<0 ⟺ R>−½ equivalence); why that paper stayed unshipped.
14. `primes-equispaced/experiments/CHEBYSHEV_BIAS_FAREY.md` — δ_Farey(10⁷)
    = 0.732 definition + resultant R=0.77 data (matches the 0.73 density
    figure in current notes; keeps provenance).

## Non-actions

- farey-extremes external dir: single heatwave script, no zeta/RH content;
  only note = in-repo farey_extremes package sources missing (only
  __pycache__), restore from git history if App1 track resumes.
- Lean divergences (FareySignPattern.lean etc.): canonical is NEWER (has the
  p=13 withdrawal); snapshot versions are historical — do not import over.

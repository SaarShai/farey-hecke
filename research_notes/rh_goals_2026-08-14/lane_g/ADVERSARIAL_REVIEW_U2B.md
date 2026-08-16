# Adversarial review of LAW_U2B_CLOSURE.md — 2026-08-16

Cold frontier-verifier round. Full report preserved verbatim below the
summary; independent probes preserved at `law_probes/u2b_verifier/vk*.py`.

## OVERALL: SOUND-WITH-REPAIRS

Both headline theorems SURVIVE independent attack:
- **U2b-A (systole)**: normal form re-proved by an independent exact method
  (121-point integer-λ polynomial identity, a = 1..40); systole re-enumerated
  from raw SL2 matrices BEYOND the author's ranges (q=5 to m=9; new levels
  q=9,13,25); min|tr| = 2λ_q, argmin {(2),(q−2)}, 0 violations. Mixed-sign
  worry resolved (R^{−a} = −R^{q−a} folds signs; enumeration complete).
- **U2b-C (counting)**: interpolation/necklace step re-derived by hand — no
  union-bound error; constants reproduced; adversarial direct partial sums
  (up to 526,636 classes per q) sit ~300× BELOW the bound.
- q^{−6} inference: forced in kind (exponent = 2σ₀−1 at the reflection),
  see D5 for the honest range.

## Defects (all local, none needing new mathematics)

- **D1**: §1.2 printed decimal wrong: 2 arccosh(3/2) = **1.9248473**, not
  1.08707. Symbolic claim + probe value correct.
- **D2**: Lemma U2b-8 covering "iff" false as written — tube must sit in
  {σ₀ < Re s < σ₀ + 1/2} (one-line repair). AMENDMENT OWED TO T2:
  LAW_T2_DETERMINANT.md §3.2 requires Ω̃ ⊇ {Re s > 1}; shrinking Ω̃ must be
  enacted there, not just asserted harmless.
- **D3**: §2.2 receipt table silently truncated (m ≤ 4 cap): 14/21 tabulated
  pairs undercount the named quantity. Converged counts (verifier DFS with
  monotone-trace prune): N_θ(4,5,6) = 7, 25, 67; conclusion N_q ≥ N_θ holds
  at all 30 converged pairs q=5..50. Parent's N_q(4)=12 at q=10 is wrong
  (converged 10) — contradiction previously unremarked.
- **D4**: Ledger row U2b.10 label PROVED overstates: proved statement is
  N_q(L) ≥ #{faithful θ-classes ≤ L} (asymptotic to N_θ(L)); flat inequality
  for every q is MEASURED. Faithfulness threshold must read |a_i| < q/2
  (Lemma U1-1), not |a_i| ≤ q−1.
- **D5**: q^{−6} is a choice: floor is σ₀ ∈ (3.05, ∞), so forced exponent is
  2σ₀−1 > **5.1**; 6 corresponds to the σ₀ = 3.5 convenience point.
- **D6**: §5.1 displayed W_∞ formula wrong; correct
  W_∞ = 2(ζ(e_h)−1) + 2·2^{−e_l}ζ(e_l), verified to 6 digits. BONUS: W_q
  strictly antitone verified q = 5..2000, W_∞ = 0.867 < 1 — GAP U2b.15
  (the q > 3000 tail) is genuinely safe.
- **D7**: receipt-coverage gaps now FILLED by verifier probes: Lemma U2b-5
  checked directly (violB = 0, near-sharp: min ratio 1.0005 at q=100);
  Theorem U2b-B tested on 10,570 MIXED-SIGN words × 401 λ (0 violations);
  `light_u_eq_1` flag in u2b_normal_form.json is dead (initialised, never
  assigned).
- **D8**: cosmetic (mislabeled column; inconsistent N_θ(5) in one JSON;
  "nothing committed" header stale — work is committed as 6b51411).

Scope sweep clean: 14 files, 2212 insertions, 0 deletions; no drive-bys;
abstentions honored. Priority claim (Schmidt–Sheingorn 1995) remains
TODO-VERIFY (library access) — correctness unaffected.

## Status ruling (frontier, 2026-08-16)

LAW_U2B_CLOSURE.md: **SOUND-WITH-REPAIRS — CLOSED after repairs D1–D6 are
enacted in the note + T2 amendment ledgered.** D7's missing checks are
supplied by the preserved verifier probes. U2b-A may be labeled
THEOREM-GRADE once D1 is fixed; U2b-C once D2's one-line repair lands and
the T2 amendment is enacted.

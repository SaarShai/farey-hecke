# Aristotle task: uniform spectral-gap lower bound, Rosen/Hecke transfer operator (goal P1)

## Status

`RequestProject/Main.lean` already compiles **sorry-free** and **axiom-clean**
(`[propext, Classical.choice, Quot.sound]`) against Mathlib v4.28.0 in our local
environment (verified by direct `lake env lean` elaboration against a prebuilt
mathlib — no errors, no warnings, no `sorry`; the three `#print axioms` lines
report only the three standard axioms). It is submitted as an independent
re-elaboration / verification target, not because it contains an open `sorry`.

## What is certified outside Lean (the numeric input)

The Arb-certified spectral-gap data for the Rosen / Hecke `λ_q`-continued-fraction
transfer operator `L_s` at `s = 1` (leading eigenvalue `λ₁ = 1`, the Gauss–Kuzmin
invariant density). The engine `code/equidist_gap/cert_gap_rosen.py` +
`code/zeta_cert_rosen.py` builds the `κ_q·N`-truncated reduced operator as an Arb
ball matrix (exact-Hurwitz branch-tail closure, `acb_series` Taylor extraction)
and isolates the top two eigenvalue moduli with `acb_mat.eig(algorithm="rump")`
(Rump's verified ball eigensolver — each ball is PROVED to contain exactly one
eigenvalue). Headline (prec 300 bits, N-stable):

| q  | κ_q | `|λ₂|` certified upper enclosure | `gap_lo = 1 − l2_hi/l1_lo` |
|----|-----|---------------------------------|----------------------------|
| 5  | 3   | 0.2025127171                    | 0.7974872829               |
| 7  | 5   | 0.3406773836                    | 0.6593226164               |
| 9  | 7   | 0.4465190796                    | 0.5534809204               |
| 11 | 9   | 0.5172265902                    | 0.4827734098               |
| 13 | 11  | 0.5702300963                    | 0.4297699037               |

The `|λ₂(q)|` enclosures are encoded as rationals `subL2 q` (rounded UP from the
Arb `l2_hi`, so `|λ₂(q)| ≤ subL2 q` is implied by the certificate).

## What to prove (plain words)

With `gapLB q := 1 − subL2 q`:

1. `gap_lb_q5 … gap_lb_q13` — per-`q` gap lower bounds matching the table;
2. `subL2_le_uniform` — `subL2 q ≤ 57024/100000` for every `q ∈ {5,7,9,11,13}`;
3. **`uniform_gap_lower_bound`** — for every `q ∈ {5,7,9,11,13}`,
   `gapLB q ≥ 42976/100000` (= 0.42976), a UNIFORM positive lower bound on the
   certified finite-`N` truncation gap across the range, attained (to rounding) at
   `q = 13`.

## Honesty / scope (do NOT overstate)

- 1-D Rosen-CF map decay-of-correlations gap at `s = 1`; certified for the
  finite-`N` nuclear truncation. Does NOT prove 2-D horocycle effective
  equidistribution (BCZ section is parabolic / zero-entropy, no gap).
- **The certified gap is strictly DECREASING in `q`** (0.797 → 0.659 → 0.553 →
  0.483 → 0.430). The uniform constant `0.42976` is uniform only over `q ≤ 13`.
  Whether a positive lower bound persists as `q → ∞` is OPEN: over this short range
  the data fits both `gap ≈ 2.98/q + 0.214` (positive limit) and `gap ≈
  2.30·q^{-0.65}` (vanishing) and cannot distinguish them. No asymptotic claim is
  made.
- Scope: odd `q` (MMS eq.(34) certified engine; even `q` deferred).
- The file does NOT formalize the transfer operator; it certifies the arithmetic
  turning the Arb eigenvalue-modulus enclosures into the stated uniform gap bound.

## Proof method in the file

All proofs are `norm_num` / `fin_cases` / `linarith` over `ℚ` on the explicit
rational bounds — no analysis, no `sorry`. The mathematical content (the certified
`|λ₂|` enclosures) lives in the Arb certificate; Lean certifies the packaging.

## If Aristotle can extend

The genuinely open follow-on is the **asymptotic**: is `inf_q gap_q > 0`? That
requires a `q`-uniform lower bound on `1 − |λ₂(L_1^{(q)})|` for the Rosen Gauss-map
Perron operator as `λ_q → 2`, which is NOT a finite arithmetic fact and is out of
scope for this packaging file. Confirming/strengthening the local elaboration is
the primary ask.

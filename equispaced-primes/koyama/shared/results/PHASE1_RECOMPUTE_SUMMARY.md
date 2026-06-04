# Phase 1 Recompute Summary — Post-Bugfix (2026-04-20/21)

## Bugfix: μ_f(p²) Coefficient Correction

**Problem identified 2026-04-20.** The C₁ ensemble scripts used an incorrect μ_f(p²) coefficient.

| Form type | Incorrect formula | Corrected formula |
|-----------|------------------|------------------|
| Elliptic curve (EC) | used p^11 | must use p (arithmetic normalization) |
| Δ (weight-12 cusp form) | used p (correct) | p^11 (analytic normalization) |

The bug caused EC E[C₁²] values to be inflated by a factor of ~p^10. Δ results were
**unaffected** (it happened to use the right power for analytic normalization).

## Corrected E[C₁²] Table

| Form | E[C₁²] | ± | Zeros used | Notes |
|------|--------|---|-----------|-------|
| 37a1 (rank-1 EC) | 2.19 | 0.02 | 500 | corrected |
| 389a1 (rank-2 EC) | 3.11 | 0.03 | 500 | corrected |
| Δ (rank-0 cusp) | 0.9502 | 0.03 | 500 | unchanged, valid |
| 5077a1 (rank-3 EC) | 4.62 | 0.04 | 500 | corrected |

**Pattern:** E[C₁²] ≈ 1.47 + 0.90·rank (working conjecture W2 — not a theorem).

## What Is Invalidated

- Pre-bugfix EC ensemble outputs (experiments/ files dated before 2026-04-20 06:31)
- PATH_B_20FORMS.csv Δ row: Δ entry was computed with old normalization; all EC rows valid
- Any downstream computation that used the old 37a1/389a1 E[C₁²] ≈ 8.x values

## What Survives

- Δ = 0.9502 ±0.03 (Δ uses analytic normalization, unaffected)
- All Dirichlet character results (different normalization scheme, unaffected)
- The rank-linear pattern W2 (now confirmed with corrected values)
- GUE pair-correlation results (independent of C₁ computation)

## Shimura 8π³/N Identity Verification

For 37a1 (N=37) and 389a1 (N=389), the Shimura–Petersson norm relation
‖f‖² = (8π³/N)·L(Sym²f, 1)·ε(f) was verified numerically.
See `results/ONE_OVER_N_SIGNCHECK.md` for details.
Relative error < 0.3% in both cases — confirms correct normalization convention used.

## Koyama Sym²/⟨f,f⟩ Proportionality — Empirically Falsified

Koyama's 2002 conjecture that E[C₁²] ∝ L(Sym²f,1)/⟨f,f⟩ (specific constant)
**does not hold** across EC families with varying rank.
The Sym²/⟨f,f⟩ ratio is nearly constant across 37a1, 389a1, 5077a1 (≈2.0 ± 0.1),
while E[C₁²] varies linearly with rank (2.19 → 3.11 → 4.62).
Conclusion: the rank-linear term captures something beyond Sym²/⟨f,f⟩.
See `results/sym2_collapse_analysis.md` for full analysis.

## Working Conjecture W2 (Rank-Linear)

E[C₁²](f) ≈ 1.47 + 0.90 · rank(f)

Fit to 4 data points (ranks 0, 1, 2, 3). R² ≈ 0.998.
**Status: working conjecture, not proved.** Δ → 1 (rank-0 analytic target) is a
separate conjecture (supported by Δ = 0.9502 ≈ 1).
See `results/path_b_analysis.md` for 20-form regression details.

## Reproduction

```bash
python3 scripts/phase1_ec_recompute.py   # 37a1, 389a1 corrected values
python3 scripts/rank3_5077a1.py          # 5077a1 rank-3 anchor
python3 scripts/phase1_delta_500zeros.py # Δ 500-zero ensemble (Δ rows only valid)
python3 scripts/one_over_n_sign_check.py # Shimura identity verification
python3 scripts/path_b_20forms.py        # 20-form regression
python3 scripts/sym2_lvalues.py          # Sym² + Petersson values
```

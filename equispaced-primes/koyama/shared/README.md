# koyama-shared — Collaborative Materials (Primes-Equispaced)

**Project:** Numerical investigation of the C₁ ensemble statistic for GL(2) L-functions
**Primary researcher:** Saar Shai
**Collaboration:** Materials shared with Prof. Kohji Matsumoto and K. Koyama (ongoing correspondence, 2026)
**Scope:** Post-bugfix corrected scripts, data, and analysis for E[C₁²] across EC and cusp form families

---

## ⚠ Bugfix — Applied 2026-04-20

**What changed:** The μ_f(p²) coefficient was incorrect in pre-April-20 EC ensemble scripts.

| Form type | Old (wrong) | New (correct) |
|-----------|-------------|---------------|
| Elliptic curve | p^11 | p (arithmetic normalization) |
| Δ cusp form | p (correct) | p^11 (analytic normalization) |

**What is invalidated:**
- EC E[C₁²] values computed before 2026-04-20 06:31 (old values ~8.x were wrong)
- PATH_B_20FORMS.csv Δ row (EC rows valid)

**What survives:**
- Δ = 0.9502 ±0.03 (analytic normalization unaffected)
- All Dirichlet results
- GUE pair-correlation results
- Upward rank signal for W2 (still needs conductor/rank separation; see 2026-05-10 audit caveat below)

---

## Corrected Numerical Table

| Form | Rank | E[C₁²] | ± |
|------|------|--------|---|
| Δ (weight-12 cusp) | 0 | 0.9502 | 0.03 |
| 37a1 | 1 | 2.19 | 0.02 |
| 389a1 | 2 | 3.11 | 0.03 |
| 5077a1 | 3 | 4.62 | 0.04 |

Working conjecture W2: E[C₁²] increases with rank, but the coefficient is not
yet isolated from conductor effects.

---

## Status

- **W2 rank-linear conjecture:** working conjecture, not proved. Local audit downgrades the earlier tight-fit claim because rank and conductor are collinear in the available EC data.
- **Sym²/⟨f,f⟩ proportionality (Koyama 2002 specific constant):** empirically falsified across rank families. The Sym²/⟨f,f⟩ ratio is constant (~2.0) while E[C₁²] varies — rank carries additional information. See `results/sym2_collapse_analysis.md`.
- **Deligne door:** open. Rank dependence may reflect arithmetic conductor growth or RMT family change.
- **Δ → 1 target:** Δ = 0.9502 ≈ 1 consistent with rank-0 analytic conjecture. Not proved.
- **Shimura 8π³/N identity:** numerically verified for 37a1, 389a1. Confirms normalization convention.

### 2026-05-10 local audit caveat

`results/PATH_B_LOCAL_AUDIT_2026-05-10.md` recomputes the Path B regressions
from the local `data/PATH_B_20FORMS.csv`. The EC-only CSV supports an upward
rank signal, but does **not** support the stronger `R² ≈ 0.998` rank-only claim:
`log(conductor)` explains more variance than rank alone in the 19 EC rows, and
rank/conductor are collinear in the current design. Treat W2 as plausible but
not isolated from conductor until more rank-3/4 and rank-matched controls are
computed.

---

## Reproduction Recipe

```bash
# Corrected EC ensemble (37a1, 389a1) — USE THIS for post-bugfix EC values
python3 scripts/phase1_ec_recompute.py

# Rank-3 anchor
python3 scripts/rank3_5077a1.py

# Δ 500-zero ensemble (Δ rows only; EC rows in this file are invalid — use above)
python3 scripts/phase1_delta_500zeros.py

# Shimura 8π³/N identity check
python3 scripts/one_over_n_sign_check.py

# 20-form rank regression
python3 scripts/path_b_20forms.py

# Sym² L-values + Petersson norms
python3 scripts/sym2_lvalues.py

# Within-class rank-0 universality
python3 scripts/within_class_rank0.py

# Rank-4/5 extension (exploratory)
python3 scripts/rank4_5_extension.py
```

---

## File Index

### scripts/
| File | Description |
|------|-------------|
| `phase1_ec_recompute.py` | Corrected arithmetic-normalization EC ensemble (37a1, 389a1) |
| `phase1_delta_500zeros.py` | Δ 500-zero ensemble (Δ valid; EC portion had bug — see comment at top) |
| `path_b_20forms.py` | 20-form rank regression (W2 conjecture) |
| `rank3_5077a1.py` | 5077a1 rank-3 anchor computation |
| `sym2_lvalues.py` | Sym² L-values and Petersson norms |
| `one_over_n_sign_check.py` | Shimura 8π³/N identity numerical verification |
| `within_class_rank0.py` | Within-class rank-0 universality test |
| `rank4_5_extension.py` | Exploratory rank-4 and rank-5 extension |

### data/
| File | Description |
|------|-------------|
| `PHASE1_EC_RECOMPUTE.json` | Post-bugfix 37a1 and 389a1 values (2.19, 3.11) |
| `PHASE1_500ZEROS_CORRECTED.json` | Δ 500-zero ensemble (Δ=0.9502 valid; EC entries invalid) |
| `PATH_B_20FORMS.csv` | 20-form regression data (EC rows valid, Δ row invalid) |
| `RANK3_5077A1.json` | 5077a1 rank-3 anchor (4.62) |
| `SYM2_LVALUES.json` | Sym² L-values and Petersson norm data |
| `RANK0_CLUSTER.json` | Rank-0 cluster data for within-class universality |

### results/
| File | Description |
|------|-------------|
| `PHASE1_RECOMPUTE_SUMMARY.md` | Bugfix narrative, corrected E[C₁²] table, status |
| `ONE_OVER_N_SIGNCHECK.md` | Shimura 8π³/N identity verification for 37a1, 389a1 |
| `path_b_analysis.md` | 20-form rank regression analysis |
| `sym2_collapse_analysis.md` | Sym²/⟨f,f⟩ ratio analysis and Koyama conjecture falsification |
| `rank_monotone_analysis.md` | Rank-monotone E[C₁²] test |

---

## Latest Commit Reference

Updated `koyama-shared/` at commit c1b5642 (c1b56420641c9281f0b784aafe5b6a344f498166): https://github.com/SaarShai/Primes-Equispaced/tree/c1b56420641c9281f0b784aafe5b6a344f498166/koyama-shared

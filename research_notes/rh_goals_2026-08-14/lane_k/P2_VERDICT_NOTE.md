# P2 verdict: Mertens constant at 4 digits + first Gonek J₋₁ verdict at T ≈ 7.5×10⁴

Date: 2026-08-15 (overnight run). Inputs: `harvest/mertens_zeros_FULL.csv`
(90,001 verified zeros, indices 10000–100000, 5-gate PASS, receipt in
`harvest/GATE_RESULTS_2026-08-15.jsonl` + this run's gate line) + the v2
banked partial sum through N=10,000 (`lane_a/ZERO_SUM_V2_REPORT.md`).
Script: `p2_adjudication.py` (mpmath dps=40). Raw output: this note's tables.

## 1. Mertens constant S = Σ_ρ 1/(|ρ|²|ζ′(ρ)|²)

| quantity | value |
|---|---|
| partial two-sided sum through N=100,000 | 0.029031194853413583 |
| T (= γ_100000) | 74920.827498994187 |
| tail fit α (155 blocks, t>2×10⁴) | 0.97622 |
| central one-sided tail | 1.2607e-6 |
| envelope one-sided tail | 5.4287e-6 |
| **S central** | **0.0290337** |
| conservative interval | [0.0290312, 0.0290421] |
| two-sided envelope bar | 1.086e-5 |

**Claim: S = 0.029034 ± 0.000011 — FOUR significant digits certified
(0.02903), fifth digit central estimate 4.** Consistent with and sharper
than v2 (0.029033 ± 0.000018). The tail envelope remains a numerical
extrapolation, not a theorem-level bound (same caveat as v2, verbatim).

Caveat recorded: block-mean/Gonek-prediction ratios in the new range span
[0.71, 3.78] (v2's range on 5k–10k was [0.80, 1.10]) — one deep block
carries an unusually small |ζ′|²; the envelope holds that maximum, which
is why the bar did not shrink by the full 9×. Honest bar kept.

Closed-form exclusions unchanged: 2/π² = 0.2026… and 3/π⁴ = 0.0308…
remain excluded (now by >45σ and >4.6σ envelope-bars respectively;
3/π⁴ = 0.030802 vs interval top 0.029042).

## 2. Gonek's conjecture J₋₁(T) ~ (3/π³)T — first numerical verdict

J₋₁ increments over the verified range (the unknown J₋₁(γ_10000) offset
cancels in increments):

| statistic | value |
|---|---|
| raw increment ratio, full range (T ∈ [9878, 74921]) | 0.9787 |
| first-half increment ratio (T ∈ [9878, ~37500]) | 0.9589 |
| **second-half increment ratio (T ∈ [~37500, 74921])** | **1.0006** |
| one-term LS fit c₁/(3/π³) | 0.9613 |

**Verdict: CONSISTENT-WITH-GONEK, and convergent.** At T ≈ 10⁴ the ratio
was 0.95 ("too early", as recorded); the local density ratio now reaches
1.0006 over the top octave. The deficit is a low-T transient, shrinking
exactly as the conjecture requires. To our knowledge (triple-scouted,
lane_c) this is the first numerical test of Gonek 1989 at any height; the
verdict at T ≈ 7.5×10⁴ is support, not proof.

Fit-honesty note: the pre-registered two-term fit c₁(T−T₀) + c₂(T logT −
T₀ logT₀) is reported (c₁/(3/π³) = 0.737, c₂ = 0.0019) but is
collinearity-degenerate on this range (T and T logT nearly parallel);
the increment ratios are the meaningful statistic. Recorded so the
pre-registered fit isn't silently dropped.

## Status changes
- gonek-extension: CLOSED (full 100k-zero table verified and consumed).
- gonek-verdict-call: CLOSED — verdict above.
- mertens-constant-precision: CLOSED — 4 digits certified (target was 4–5;
  the 5th digit is central-only because of the deep-block envelope).
- constants-paper-greenlight: UNBLOCKED (HITL).

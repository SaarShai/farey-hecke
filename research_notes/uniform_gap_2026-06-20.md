# Uniform spectral-gap of the Rosen/Hecke transfer operator (goal P1) — 2026-06-20

## Goal

Turn the certified transfer-operator spectral gap `gap_q = 1 − |λ₂(L_s)|` into a
UNIFORM lower bound `gap_q ≥ c` over a range of `q`, Arb-certified, with a Lean
statement of the uniform inequality (Koyama's "uniform spectral constraint").

## Operator and parameter

Rosen / Hecke `λ_q`-continued-fraction transfer operator `L_s` at the conformal
parameter `s = 1`, where the leading eigenvalue is `λ₁ = 1` (the Gauss–Kuzmin
invariant density). `gap_q := 1 − |λ₂|/|λ₁|` is the exponential mixing rate of the
1-D Rosen Gauss map. Certified via `code/zeta_cert_rosen.py` (exact-Hurwitz
branch-tail, `acb_series`, Arb balls) + `acb_mat.eig(algorithm="rump")`
(Rump-verified: each ball PROVED to contain exactly one eigenvalue), so
`gap_lo = 1 − l2_hi/l1_lo` is RIGOROUS for the finite-`N` nuclear truncation.

Scope: **odd `q ≥ 5`** (the certified engine implements MMS eq.(34) odd-`q` block
structure; even `q` uses eq.(32) which `zeta_cert_rosen` does not generalize, and
is deferred to the Kaggle sweep / even-`q` engine).

## Certified results (this session, prec 300 bits, Rump-verified, N-stable)

`code/uniform_gap/cert_gap_sweep.py` → `out/cert_gap_sweep_q5to13.json`.
Headline `N` is the finest grid that produced a verified top-2 enclosure;
N-stability shown by the two-point `N`-grid drift (all ≲ 1.6e−8).

| q  | κ_q | `l1_lo` (→1)   | `|λ₂|` upper enclosure | `gap_lo` (certified) | `α_lo = −log(...)` |
|----|-----|----------------|------------------------|----------------------|--------------------|
| 5  | 3   | 0.99999999999… | 0.2025127171           | **0.7974872829**     | 1.596953           |
| 7  | 5   | 0.99999999999… | 0.3406773836           | **0.6593226164**     | 1.076819           |
| 9  | 7   | 0.99999999994… | 0.4465190796           | **0.5534809204**     | 0.806273           |
| 11 | 9   | 0.99999999994… | 0.5172265902           | **0.4827734098**     | 0.659274           |
| 13 | 11  | 0.99999999994… | 0.5702300963           | **0.4297699037**     | 0.561715           |

(`q = 5, 7` cross-checked against the prior `code/equidist_gap/out/cert_gap_rosen.json`
which used N up to 16/14 — identical to the digits shown.)

## Trend / verdict — THE GAP DECREASES IN q (honest, route-relevant)

**The certified spectral gap is strictly monotonically DECREASING in `q`:**
0.797 → 0.659 → 0.553 → 0.483 → 0.430 across `q = 5, 7, 9, 11, 13`.
Equivalently `|λ₂(q)|` rises monotonically toward 1 (0.203 → 0.570).

Fits over the 5 certified points:
- `gap ≈ 2.98/q + 0.214` (1/q + intercept) — extrapolates to a POSITIVE limit ≈ 0.214;
- `gap ≈ 2.30·q^{-0.65}` (power law) — extrapolates to 0.

**These two fits are indistinguishable over `q ≤ 13` and predict materially
different `q → ∞` behaviour** (e.g. at `q = 31`: 0.310 vs 0.246). So the data
ALONE cannot decide whether `inf_q gap_q > 0`. This is the honest open question and
the key caveat for the equidistribution route:

- IF `inf_q gap_q = c > 0`: the uniform spectral constraint holds and the
  effective-equidistribution route survives uniformly in `q`.
- IF `gap_q → 0`: the route degrades as `q → ∞` (the per-`q` mixing rate vanishes),
  and any "uniform" statement must be range-restricted or carry a `q`-dependent
  rate. This would NOT block a per-`q` or bounded-`q` result, but it blocks a single
  `q`-independent constant.

**Structural read (heuristic, not certified):** at `s = 1` the Rosen Gauss map is a
uniformly expanding Markov interval map for every `q`; its parabolicity is a 2-D
horocycle phenomenon, NOT a property of the 1-D CF map at `s = 1`. So a positive
limiting gap (`1/q + intercept` form) is structurally plausible — but unproven. The
honest deliverable is therefore a uniform bound **over the certified range**, not an
asymptotic theorem.

## What IS delivered (certified + machine-verified)

1. **Certified per-q gaps** `q = 5,7,9,11,13` (table above), Rump-verified, N-stable.
2. **Uniform-over-range lower bound**: `gap_q ≥ 0.42976` for every odd
   `q ∈ {5,7,9,11,13}`, with the floor attained (to rounding) at the largest `q =
   13`. This is the certified "uniform spectral constraint" over the range.
3. **Lean** (`projects/uniform_gap_lean/RequestProject/Main.lean`,
   sorry-free, axiom-clean `[propext, Classical.choice, Quot.sound]`, elaborated
   locally against Mathlib v4.28.0): the certified rational `|λ₂(q)|` upper bounds
   are packaged and the uniform gap floor `uniform_gap_lower_bound : ∀ q ∈ Qrange,
   gapLB q ≥ 42976/100000` is proved, plus per-q `gap_lb_q{5..13}` and the
   sub-radius ceiling `subL2_lt_one`. The file is FAITHFUL: it does not formalize
   the operator (which would risk a vacuous statement); it certifies the arithmetic
   that turns the Arb enclosures into the uniform bound, with the operator-level
   content explicitly attributed to the external Rump certificate.

## Honest scope / residuals

- 1-D Rosen-CF map decay-of-correlations gap at `s = 1`; `gap_lo` certified for the
  **finite-`N` nuclear truncation**. Eigenvalue dimension-tail propagation to the
  TRUE operator is a separate residual (`zeta_cert_rosen.dim_tail_from_matrix`
  exists but is not propagated to the eigenvalues here). N-stability is strong
  evidence the truncation has resolved `λ₁, λ₂`.
- Does **NOT** prove 2-D horocycle effective equidistribution (BCZ-Farey section is
  parabolic / zero-entropy, polynomial mixing, `1` in essential spectrum, no gap).
- Odd `q` only.
- **Asymptotic `inf_q gap_q > 0` is OPEN** (the two fits disagree) — this is the
  one fact that would upgrade "uniform over range" to "uniform in `q`".

## Artifacts

- `code/uniform_gap/cert_gap_sweep.py` — local sweep (reuses `cert_gap_rosen`).
- `code/uniform_gap/kaggle_gap_sweep.py` — heavy-range (`q = 5..31`) Kaggle kernel
  (prepared; bundle with `zeta_cert_rosen.py` + `zeta_cert_rosen_q5.py`, write to
  `/kaggle/working`). NOT yet run — q=15..31 each grow `κ=q−2`, rump cost grows
  (q=13/N=12 already ~53s locally); the heavy range is needed to extend the trend
  far enough to start to discriminate the two fits.
- `code/uniform_gap/out/cert_gap_sweep_q5to13.json` — certified table + N-stability.
- `projects/uniform_gap_lean/` — Lean RequestProject (Main.lean + PROMPT.md +
  lakefile/toolchain/manifest), sorry-free + axiom-clean.

## Next step to actually settle the route

Run `kaggle_gap_sweep.py` over `q = 15..31` (certified) to extend the trend; if
`gap_q` keeps tracking the power-law fit down past ~0.25 the route is `q`-degrading;
if it flattens toward ~0.21 the positive-limit reading is supported. Either way a
`q`-uniform PROOF of `inf gap_q > 0` needs an analytic lower bound on
`1 − |λ₂(L_1^{(q)})|` as `λ_q → 2` (not a finite computation).

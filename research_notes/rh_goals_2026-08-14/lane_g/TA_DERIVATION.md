# T-a — Disk geometry and contraction constants for the G_5 operator
Frontier working note, 2026-08-14. Feeds ticket flagship-tail-bound.

## Geometry (from the implementation, zeta_mayer_rosen.py)

- q=5: λ = 2cos(π/5) = φ ≈ 1.618, hq=1, κ=3 components.
- Markov partition Φ_1..Φ_3 of [−λ/2, 0] with boundary points from finite
  λ-CF values (partition_points(5)); disc D_i: center c_i = midpoint(Φ_i),
  radius rad_i = 2.5 · halfwidth(Φ_i).
- Branches (single-branch blocks): θ_n(z) = −1/(z + nλ), θ_{−n}(z) =
  +1/(z − nλ), n ≥ 1, with weight (θ′)^s; allowed transitions per the MMS
  Markov structure; the ∞-blocks sum n ≥ n₀ with analytic tail closure.

## Lemma ladder for the proven tail bound

- **L1 (branch-image nesting with margin).** For every allowed transition
  (j→i, branch ±n): sup_{|z−c_i| = rad_i} |θ_{±n}(z) − c_j| ≤ ρ⋆ · rad_j
  for an explicit ρ⋆ < 1. Finitely many head branches: per-branch certified
  sup via Arb interval evaluation on the contour (mechanical). Tail branches
  n ≥ n₀: |θ_{±n}(z)| ≤ 1/(nλ − λ/2 − rad_i) — monotone explicit bound ⇒
  a single inequality in n covers the whole tail. Candidate Aristotle
  targets: the tail inequality and the reduction "contour sup ≤ finite grid
  max + modulus-of-continuity term" (both finite real-arithmetic lemmas).
- **L2 (normalized-coefficient decay ⇒ singular-value bound).** In the
  normalized monomial bases, L1 + Cauchy estimates give |B[m,k]| ≤ W·ρ⋆^m
  (W = certified sup of |weight| on the contour, s in the certification
  box); hence singular values of the full block operator satisfy
  s_m ≤ C·ρ⋆^m with C = κ·W·(basis constants). Elementary; paper-proof +
  possible Aristotle for the summation algebra.
- **L3 (determinant truncation bound).** Standard trace-class bound
  (Simon, *Trace Ideals*, or the Gohberg–Krein inequality):
  |det(1−L) − det(1−L_N)| ≤ exp(1 + Σ_m s_m) · Σ_{m>N} s_m
  ≤ exp(1 + C/(1−ρ⋆)) · C ρ⋆^{N+1}/(1−ρ⋆) =: F(C, ρ⋆, N).
  Cited + paper-proved in our constants; NOT Lean (Mathlib gap); the
  citation-level dependence is disclosed in the theorem's preamble.
- **T-c radius.** Replace the ×4 heuristic inflation with F(C, ρ⋆, N) on
  every contour point; boxes re-certify (or N is raised until they do).

## Immediate recon (before proving anything)

Numerically measure the ACTUAL worst-case contraction margin ρ̂ over all
head branches and the tail bound at n₀ — if ρ̂ is close to 1 the proof
strategy needs different discs (smaller safety factor trade-off), and we
want to know that TODAY, not after the lemmas are written. Script:
lane_g/ta_recon.py; results below when run.

## Recon results (2026-08-14, ta_recon.py + ta_recon.json)

- Geometry: partition [−0.809017, −0.618034, −0.381966, 0], centers
  (−0.7135, −0.5, −0.1910), radii (0.2387, 0.2951, 0.4775) at safety 2.5.
- ρ̂ = 0.850599 worst over 357/360 head branch-contours landing strictly
  inside a disc; tail branches (n ≥ 8) bounded by 0.0858 — deep inside.
- Exceptions: the n=+1 branch from each disc (ratios 1.42–2.75). NEXT STEP:
  confirm these are outside the allowed Markov transition set by reading
  build_reduced_matrix's block pattern; restate L1 over allowed transitions.
- DESIGN DECISION RESOLVED (same day, tb_disc_sweep.py + tb_disc_opt.py):
  (1) Allowed-set verification from build_reduced_matrix (eq.34 code): the
  positive n=1 branch IS in the transition set — as block (3→1), and it is
  a FULL Markov branch (θ₁ maps Φ₃ ONTO Φ₁), so uniform inflation can never
  nest it (ratio exactly 1.0000 at safety 1, worse above). This was the
  recon's "exception" — real, and fatal for single-safety schemes.
  (2) FIX (Mayer-style): independent per-disc inflations. Optimum found:
  (a₁,a₂,a₃) = (3.140, 2.270, 1.700) ⇒ ρ⋆ = 0.6597, binding block now the
  balanced tail (2→3, n₀=2). Per-mode decay 0.66^N: N≈39 for 1e-7,
  N≈83 for 1e-15. Flagship boxes (contour bounds ~1e-6) need N≈45–50 ⇒
  ~2–4× current runtime. tb_disc_opt.json holds the constants.
  (3) Analyticity check at these radii: D₁ (radius .75 about −0.714) stays
  0.16 clear of the nearest pole (−λ); weight branch cuts avoided (z+nλ
  and nλ−z stay in the right half-plane on all used blocks) — to be
  re-verified with intervals in the certified pass.
- REMAINING T-b: (i) Arb-certify the 11 block contraction ratios at the
  optimized radii (agent, mechanical); (ii) write L1–L3 with these
  constants (frontier; v17 Aristotle shell lemmas pending); (iii) T-c:
  builder with optimized radii at N=48, rerun flagship boxes with the
  PROVEN radius F(C, 0.66, N).

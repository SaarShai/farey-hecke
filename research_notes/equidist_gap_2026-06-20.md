# Certified spectral gap & effective decay-of-correlations for the Rosen/Hecke transfer operator
**Goal G1 — 2026-06-20.** Agent: parallel-fleet G1 (certified effective equidistribution via transfer-operator spectral gap).

## Headline (what is and is not certified)

For the full Mayer–Mühlenbruch–Strömberg (MMS) transfer operator `L_s` of the
Rosen `λ_q`-continued-fraction (Gauss) map `f_q` of the Hecke triangle group
`G_q` (`λ_q = 2 cos(π/q)`), evaluated at the conformal parameter `s = 1` (where
the leading eigenvalue is `λ₁ = 1`, eigenfunction = Gauss–Kuzmin invariant
density), we obtain **Arb-CERTIFIED enclosures of the spectral gap**
`gap_q := 1 − |λ₂|/|λ₁|` of the finite-N nuclear truncation:

| q | `|λ₁|` (certified) | `|λ₂|` (certified) | **certified `gap_q ≥`** | `α_q = −log|λ₂/λ₁| ≥` | method |
|---|---|---|---|---|---|
| 5 | `1` (width <1e-13, N=16) | `0.20251271708` | **`0.797487282915`** | `1.5969525940` | arb-certified |
| 7 | `1` (width <2e-12, N=14) | `0.34067738362` | **`0.659322616376`** | `1.0768193386` | arb-certified |
| 8 | `0.99999999` | `0.38120803` | `0.6187919656` | `0.96441003` | **float-heuristic** |

- **q=5, q=7 are CERTIFIED** (`method = arb-certified`): python-flint Arb-ball
  arithmetic + Rump-verified ball eigensolver `acb_mat.eig(algorithm="rump")`,
  which returns balls each PROVED to contain exactly one eigenvalue. The
  reported `gap_lo = 1 − l2_hi/l1_lo` is therefore a rigorous lower bound on the
  gap of the N-truncated operator. Both N-converge tightly (l1 width → 0).
- **q=8 is FLOAT-HEURISTIC** (numpy `eigvals`, double precision): the certified
  engine `code/zeta_cert_rosen.py` only generalizes the ODD-q MMS eq.(34) block
  structure; even q uses eq.(32), not yet certified here. Deferred to the Kaggle
  sweep + a future even-q cert engine. The float value matches the certified
  q=5/q=7 values to ~9 digits (cross-validation of the cert path), so the q=8
  float gap is trustworthy as a heuristic but is NOT certified.

Cross-check: the float-heuristic full-operator gaps (`code/equidist_gap/out/float_gap_s1.json`)
q=5 `0.7974872793`, q=7 `0.6593226148` agree with the certified bounds to 9 digits.

## (b) Effective-rate statement (quasi-compactness / Lasota–Yorke ⇒ exponential mixing)

The MMS operator `L_s` is **nuclear of order 0** on the per-cell holomorphic
disc-algebras (MMS Thm 4.10; the Rosen branches `θ_n = ST^n` map the partition
discs strictly inside one another, Lemma 4.4). Nuclearity gives quasi-compactness
with a discrete spectrum accumulating only at 0; at `s = 1` the leading simple
eigenvalue is `λ₁ = 1`. Writing the spectral decomposition
`L_1 = P₁ + R`, where `P₁` is the rank-1 projection onto the invariant density
`h_q` and `‖R‖_spec = |λ₂| < 1`, one gets for observables `φ, ψ` in the
disc-algebra (Banach space `B` on which `L_1` acts) the exponential
**decay of correlations** of the Rosen Gauss map w.r.t. its a.c. invariant
measure `μ_q = h_q dx`:

> **Effective rate.** There is `C = C(q, φ, ψ) < ∞` such that for all `n ≥ 0`
> ```
> | ∫ (φ ∘ f_q^n) · ψ  dμ_q  −  (∫ φ dμ_q)(∫ ψ dμ_q) |  ≤  C · |λ₂|^n
>                                                       =  C · (1 − gap_q)^n .
> ```

With the certified gaps this is, explicitly,
- **q = 5:** rate `(1 − gap₅)^n ≤ 0.2025127171^n`, i.e. `exp(−1.5969525940 · n)`.
- **q = 7:** rate `(1 − gap₇)^n ≤ 0.3406773837^n`, i.e. `exp(−1.0768193386 · n)`.

Equivalently, for any `ρ ∈ (|λ₂|, 1)` the correlation function is `O(ρ^n)`; the
optimal base is the certified `|λ₂|`. (The Lasota–Yorke inequality that
underwrites quasi-compactness here is the analyticity/nuclearity estimate, not a
BV one; the constant `C` absorbs `‖ψ‖_B · ‖P_{≠1}φ‖_B` and the bound
`‖R^n‖ ≤ C' |λ₂|^n (1+o(1))` from the resolvent away from the leading
eigenvalue.) The `n`-step factor monotonicity `ρ^n ≤ (1−gap)^n` is the
Lean lemma `EquidistGap.decay_of_correlations`.

## (c) Lean artifact (prepared, verified sorry-free locally)

`projects/equidist_gap_lean/` (RequestProject, lakefile v4.28.0). Three lemmas,
namespace `EquidistGap`, **built sorry-free locally** against Mathlib v4.28.0,
axiom-clean `[propext, Classical.choice, Quot.sound]`:
- `gap_q5_ge`: from the certified enclosures (as hypotheses) `1 − |λ₂|/|λ₁| ≥ 0.79`.
- `gap_q7_ge`: `… ≥ 0.65`.
- `decay_of_correlations`: `0 ≤ ρ ≤ 1 − gap ⇒ ρ^n ≤ (1−gap)^n`.

These discharge the ARITHMETIC step (certified modulus bounds ⇒ gap bound ⇒
exponential factor) inside Lean. They do NOT re-derive the eigenvalue inside Lean
(that is the Arb verification, done externally). `PROMPT.md` states the task.

Local build: `lake env lean` against the built Mathlib in
`projects/aristotle_dispatch_v15/` (same toolchain) → EXIT 0, no `sorry`,
axioms clean.

## (d) Kaggle sweep (prepared, smoke-tested locally)

`kaggle_kernels/hecke_gap_sweep/` (`hecke_gap_sweep.py` + `kernel-metadata.json`).
Self-contained: freezes `zeta_cert_rosen_q5.py` + `zeta_cert_rosen.py`, pip-installs
python-flint, runs the certified gap sweep over odd `q ∈ {5,7,9,11,13,15,17}`,
`N ∈ {10..20}`, prec 400. Writes `result.json`. Smoke-tested locally on q=5 (N=10,12)
→ reproduces `gap_5 ≥ 0.7974872835`. NOT pushed (main loop pushes).

## Residual — what blocks a full effective-equidistribution THEOREM

1. **Eigenvalue dimension-tail propagation (the cert residual).** The certified
   `gap_lo` is rigorous for the *finite-N nuclear truncation*. To make it a
   theorem about the *true* operator one must propagate the certified determinant
   dimension-tail bound (already in `zeta_cert_rosen.dim_tail_from_matrix`) to the
   eigenvalues `λ₁, λ₂` (a perturbation/`det`-tail → eigenvalue enclosure step).
   N-stability is strong evidence but not yet a proof. **This is the cleanest next
   step and is local-engine-shaped.**
2. **Even-q certified engine.** q=8 (and all even q) needs the MMS eq.(32) block
   structure certified (`zeta_cert_rosen` only does odd q). Mechanical.
3. **Operator-norm constant `C`.** The effective rate's constant `C(q,φ,ψ)` is
   stated abstractly; making it explicit needs a quantitative resolvent /
   spectral-projection norm bound on the disc-algebra (the `‖R^n‖ ≤ C|λ₂|^n`
   step). This is the analytic content beyond the gap itself.
4. **STRUCTURAL CAVEAT (do not violate).** This is the **1-D Rosen-CF-map**
   decay-of-correlations gap. It does **NOT** prove **2-D horocycle effective
   equidistribution**: the BCZ-Farey horocycle section is parabolic /
   zero-entropy with polynomial mixing (`C(n) ~ n^−0.9`), NO spectral gap, 1 in
   the essential spectrum (`research_notes/bcz_mixing_rate_2026-06-14.md`). The
   1-D gap governs the Gauss-map renewal / cusp-excursion statistics, a different
   (though related) object from the horocycle flow.

## Files
- `code/equidist_gap/cert_gap_rosen.py` → `out/cert_gap_rosen.json` (certified q=5,7).
- `code/equidist_gap/out/float_gap_s1.json` (float cross-check q=5,7,8).
- `projects/equidist_gap_lean/` (Lean, sorry-free local, axiom-clean).
- `kaggle_kernels/hecke_gap_sweep/` (prepared sweep).

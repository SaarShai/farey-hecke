# θ = 1/2 for Farey/Hecke gap extremes: reduction to Marklof–Pollicott — DRAFT v1 (2026-07-03)

Status: proof PROGRAM with the probabilistic transfer fully cited, the deterministic
content machine-verified (q=3), and two named technical gaps (T1, T2) with assessed
difficulty. NOT a complete proof. Written against the verbatim M–P statements
(extraction 2026-07-03; arXiv:2408.01781 = Nonlinearity 38 (2025) 055003).

## Target theorem

**Theorem (goal).** Let λ be an admissible Borel probability measure on X = Γ\SL(2,ℝ),
Γ a finite-covolume Fuchsian group with cusp (Farey case Γ = SL(2,ℤ); Hecke G_q in
general). Let g_i be the gap-product observable P = ab along the BCZ/Taha section
orbit of the horocycle flow started at x₀ ~ λ. Choose thresholds u_n with
n·m(P < u_n) → 2τ. Then the exceedance point process of {P < u_n} on time scale n
converges to the compound Poisson process CP(τ; δ₂). Consequently:
- P(min over n steps ≥ u_n) → e^{−τ} — extremal index **θ = 1/2**;
- the k-th deepest excursion laws and interexceedance-time laws are those of CP(τ; δ₂).

## Step 1 — Transfer to stationarity [COMPLETE, citation]

M–P Thm 3 (their eq. 2.21) + the fdd statement (their p.7): for admissible λ, the
joint law of the first N rescaled hitting times + impact parameters
(e^{−R}ξ_j(x₀,R), w_j(x₀,R))_{j≤N} of the shrinking cusp section H_κ(R) converges,
as R→∞, to the law of (ξ_j(x,0), w_j(x,0))_{j≤N} under the invariant measure μ.
Input: geodesic-flow mixing + admissibility (their Remark 1.2, eq. 2.9) — no
horocycle/BCZ mixing rate anywhere. Deep exceedances of P in n BCZ steps ↔ hits of
H_κ(R_n) with e^{R_n} ≍ u_n^{−1/2}·(scale); the dictionary is the standard
BCZ-section ↔ cusp-excursion correspondence (their §6 recovers Hall's law from it —
same normalization we use).

## Step 2 — Poissonization at stationarity [GAP T1 — believed standard]

Claim: under μ, the times of excursions deeper than D (i.e. hits of H_κ(0) with
impact parameter in the depth-D set Σ_D, v(Σ_D) → 0) form, after time rescaling by
1/v(Σ_D), a Poisson process of intensity 1 in the limit D→∞.

Route (q=3): excursion times of the stationary horocycle frame = short-vector
epochs of the random lattice u_s x; counts in disjoint windows have factorial
moments expressible by Rogers/Siegel-type formulas for SL(2,ℤ)-random lattices;
moment convergence to Poisson is the classical Södergren/Strömbergsson–Södergren
mechanism. For fixed k the k-fold correlation reduces to counting k-tuples of
primitive vectors in disjoint shrinking hyperbolic regions — elementary per k.
Assessment: q=3 provable with known tools; write out factorial-moment bound.
[T1] General G_q: needs the Siegel–Veech-type second/higher-moment formulas for
Hecke lattices (Eisenstein-series route). Real work; not known to be written down.

## Step 3 — Deterministic cluster content = exactly 2 [q=3 core DONE/Lean]

(a) Upper bound: no 3 consecutive exceedances below Q²/8 — **machine-verified**
(`farey_no_triple_large_gap`, Aristotle 22e93551, sorry-free, axiom-clean).
(b) Lower bound: the two section-crossings of one excursion have products with
ratio → 1 (cusp-swap involution; numerics: max pair-ratio 1.0002 at s=3·10⁻⁴), so
for a.e. depth both sit on the same side of the threshold; the boundary window
where c_j = 1 has vanishing probability (empirically 18/27629 at s=0.01, ↓ with s).
Needs: the deterministic two-sided ratio bound |log(P_j/P_{j+1})| ≤ C·(depth)⁻¹ —
straightforward from the neighbor identities; formalize as the next Lean target.
[T2] General G_q: the pairing lemma must be re-proved on the Taha section (repo
numerics already support it: Pr(L=2) ≥ 0.994 at q=4,5,7 — theta_half_repp note).

## Step 4 — Assembly [routine]

Steps 1–3 give: exceedance count in the window = 2 × (Poisson(τ) count) + o_P(1)
⟹ CP(τ; δ₂). Leadbetter/O'Brien: θ = 1/E[cluster size] = 1/2. Order statistics
and interexceedance laws read off CP(τ; δ₂). (Also yields the M–P "not proven"
column: Poisson excursion counts, k-th deepest, interexcursion gaps.)

## Gap ledger

| gap | content | difficulty | plan |
|---|---|---|---|
| T1 | stationary Poissonization, q=3 via Rogers moments | standard, write-out | next session; lit-check Södergren SL(2) scope first |
| T1' | T1 for Hecke G_q (Siegel–Veech moments) | real research | later; possibly the Koyama-collaboration piece |
| T2 | pair-ratio deterministic bound + G_q pairing lemma | elementary + Lean | Aristotle next targets |

## Why this matters

Fills the explicitly-open column of a 2025 Nonlinearity paper (extremal index,
excursion Poisson counts, order statistics) for the canonical arithmetic case, with
the combinatorial mechanism machine-verified. The θ=1/2 value is q-independent —
one clustering constant for the whole Hecke family — in contrast to the hard-edge
θ_edge where q=3 is (preliminarily) the unique clustering case.

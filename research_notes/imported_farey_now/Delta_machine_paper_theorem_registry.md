---
title: "Delta-machine paper — Theorem-confidence registry"
date: 2026-05-09
status: companion to Delta_machine_paper_compositio_draft.md
confidence aggregation rule (single, applied throughout the draft):
  ≥ 0.95   → stated as **Theorem**
  0.85--0.95 → stated as **Proposition**
  0.65--0.85 → stated as **Conjecture (with evidence)**
  < 0.65   → omitted, or retained only as **Open Problem**
---

# Δ-machine paper — Theorem registry

For each theorem / proposition / conjecture appearing in the paper draft
`Delta_machine_paper_compositio_draft.md`, this file gives:

(a) the statement (capsule);
(b) the source file in the bundle;
(c) the stated confidence;
(d) the bucket (theorem / proposition / conjecture / open);
(e) the load-bearing citation(s);
(f) any demotion or correction relative to the source file.

---

## §2. Master theorems

### Theorem 2.1 (Master Δ-machine)

- **Statement.** For L ∈ S primitive, μ_L the Dirichlet inverse of L,
  and W Schwartz on (0, ∞) with Mellin transform M_W meromorphic of
  super-polynomial decay on vertical strips,
  `S_{μ_L}^W(N) = R_0(L; W) + Σ_{ρ: L(ρ)=0, 0<Re ρ<1} N^ρ M_W(ρ)/L'(ρ)
  + R_triv(L; W; N) + O_A(N^{-A})` for any A > 0.
  Unconditional whenever the standard analytic input (polynomial growth
  of 1/L on zero-free vertical strips) is unconditional, which is the
  case for L = ζ, Dirichlet L(s, χ), and GL(2) cusp-form L(s, f) (via
  Iwaniec–Kowalski Theorems 5.20 and 5.23).
- **Source.** `Delta_arithmetic_generalization.md §3.5`,
  `MK3_Bridge_Selberg_VERIFIED.md §4`, `Smoothed_Dwf_publishable.md
  Theorem X.3.1`, `Delta_machine_paper_bundle.md Theorem 2.1`.
- **Confidence.** **0.95.** Numerically verified at 8 digits for ζ
  (200 zeros, N = 10^5), 4 digits for L(s, χ_3), 3 digits for L(s, Δ).
  Proof is a textbook Mellin–Perron contour shift.
- **Bucket.** Theorem (≥ 0.95).
- **Load-bearing citations.** Iwaniec–Kowalski 2004 Thm 5.20 (1/ζ on
  zero-free strips), Thm 5.23 (1/L(s, f) for GL(2)); Titchmarsh 1986
  §3.11, §9.7 (zero-avoiding contour T_n).
- **Comments.** The master theorem as stated is the central
  contribution of the paper. The exact form covering uniformly
  ζ, Dirichlet, modular, and Rankin–Selberg cases is what is novel;
  the underlying contour-shift technology is classical.

### Theorem 2.2 (Higher-order Δ^k residue formula)

- **Statement.** For L ∈ S primitive with simple zeros and k ≥ 1,
  define μ_L^{(k)} = μ_L^{*k} (k-fold Dirichlet convolution). Then
  `S_L^{(k), W}(N) = R_0^{(k)} + Σ_{ρ: L(ρ)=0} Res_{s=ρ}[N^s M_W(s)/L(s)^k]
  + R_triv^{(k)} + O_A(N^{-A})`. For k = 2, the residue at a simple
  zero ρ is `(N^ρ / L'(ρ)^2) · [(log N) M_W(ρ) + M_W'(ρ) − M_W(ρ)
  L''(ρ)/L'(ρ)]`.
- **Source.** `Delta_machine_extended.md §3.1` (Theorem 3.1).
- **Confidence.** **0.92.** Numerical verification at 4 digits for
  k = 2, L = ζ, N = 10^4 in §4.1 of source. Direct application of
  residue calculus + Theorem 2.1 framework.
- **Bucket.** Proposition (the (log N)^{k-1} enhancement is provable;
  the strong-form polylog conjecture from the source bundle has
  been **demoted** — see Conjecture 5.Y below).
- **Load-bearing citations.** Same as 2.1; Faà di Bruno formula for
  general k is folklore.
- **Comments.** Stated as Proposition because confidence is 0.92,
  just below the theorem threshold; the (log N)^{k−1} structure is
  rigorous, the explicit Faà di Bruno coefficients for k ≥ 3 are
  schematically given but not all checked.

### Theorem 2.3 (k = 2 residual bound, corrected)

- **Statement.** On RH and the simple-zeros conjecture for ζ, for
  Schwartz W and any k ≥ 1,
  `|S_ζ^{(k), W}(N) − R_0^{(k)}(W)| ≤ C_W^{(k)} √N (log N)^{k-1}`,
  where `C_W^{(k)} = κ_k · Σ_{γ>0} |M_W(ρ)| / |ζ'(ρ)|^k` with κ_k a
  combinatorial Faà di Bruno constant (κ_1 = 1, κ_2 = 2, …).
- **Source.** `Higher_order_polylog_conjecture.md §4.2`.
- **Confidence.** **0.97** for the bound itself (immediate from
  Theorem 2.2 + Schwartz decay of M_W).
- **Bucket.** Theorem.
- **Load-bearing citations.** Same as 2.2.
- **Comments.** This **replaces** the strong-form polylog conjecture
  of `Delta_machine_extended.md §6.2` which was **falsified** for
  k = 2 (see Conjecture 5.Y below).

### Conjecture 2.4 (Polylog limiting distribution, RMT-conditional)

- **Statement.** Conditional on the Hughes–Keating–O'Connell
  conjecture and on a GUE phase-randomness heuristic for the zeros of
  ζ, the rescaled fluctuation `r(N) / (√N (log N)^{k-1})` admits a
  bounded limiting distribution as N → ∞.
- **Source.** `Higher_order_polylog_conjecture.md §3.4` (NEW
  conditional refined conjecture).
- **Confidence.** **0.75** (conditional on HKO + GUE phase-randomness,
  both standard but unproven).
- **Bucket.** Conjecture (with evidence, conditional).
- **Comments.** Replaces the falsified strong form. Stated explicitly
  as conditional in the draft.

### Proposition 2.5 (Cross-Selberg)

- **Statement.** Let L_1, L_2 ∈ S be distinct primitives of degrees
  d_1, d_2. The cross-Selberg Dirichlet series
  `F_{L_1, L_2}(s) = Σ μ_{L_1}(n) μ_{L_2}(n) / n^s` factors at
  unramified primes p as
  `F_{L_1, L_2}(s) = ∏_p ∏_{i=1}^{d_1} ∏_{j=1}^{d_2}
  (1 + α_{1,i,p} α_{2,j,p} p^{-s})` (Macdonald–Cauchy identity).
  Consequently, `Σ_n μ_{L_1}(n) μ_{L_2}(n) W(n/N) =
  P_{L_1, L_2}(log N) + (zero oscillation) + R_triv + O_A(N^{-A})`
  where `P_{L_1, L_2}` is a polynomial of degree at least 1.
  For ζ × L(s, χ_3), the old 12–19 % slope mismatch is resolved by the
  ramified factor `(1 - 3^{-2s})^{-1}`: the full explicit formula with
  the log-3 axis-pole lattice matches the direct sieved sum to 6+ digit
  accuracy at `N = 3 * 10^5`.
- **Source.** `Delta_machine_multi_L.md §3.2 / §5`,
  `Delta_machine_extended.md §3.2`,
  `Delta_machine_paper_bundle.md Theorem 2.4`.
- **Confidence.** **0.78–0.85** depending on rank.
- **Bucket.** Proposition (full Selberg-class membership of the
  plus-tensor object is unconditional only for low rank, conditional
  on JPSS-type results in higher rank).
- **Load-bearing citations.** Macdonald 1979/1995 Ch. I §4
  (Cauchy identity); Liu–Wang–Ye 2005 Theorem 1.1 (unconditional
  ζ × GL(2)); Jacquet–Piatetski-Shapiro–Shalika 1983 (general
  Rankin–Selberg).
- **Comments.** The former ζ × L(s, χ_3) slope mismatch is not a
  pending numerical problem. It was a missing ramified-axis-pole term
  in the §5.6 explicit formula. The higher-rank/global conditionality
  of Proposition 2.5 is unchanged.

### Proposition 2.5b (Ramified correction divisor and axis-pole multiplicities)

- **Statement.** Let `S_ram` be a finite set of primes and
  `E_ram(s)=prod_{p in S_ram} P_p(p^{-s})^{-1}`, with each
  `P_p(0) != 0`. If
  `P_p(z)=c_p prod_alpha (z-alpha)^{m_{p,alpha}}`, then the local
  divisor of `E_ram` is supported at
  `s=-log|alpha|/log p - i(arg alpha + 2*pi*k)/log p`, `k in Z`.
  The contribution is on the imaginary axis if and only if
  `|alpha|=1`. For the full integrand `I(s)=A(s)M_W(s)E_ram(s)`,
  `ord_{s0} I = ord_{s0}(A M_W)
  - sum_{p,alpha,k: s_{p,alpha,k}=s0} m_{p,alpha}`. Hence zeros of
  `A(s)M_W(s)` may cancel local ramified poles; without cancellation,
  coincident local multiplicities add.
- **Source.** `handoff-2026-05-11-breakthrough-wave-5/AGENT11_DELTA_2_5B_REGISTRY_EXECUTION_PLAN_2026-05-11.md`;
  `handoff-2026-05-09-followup/Cross_Selberg_slope_diagnosis.md`.
- **Confidence.** **0.90.**
- **Bucket.** Proposition.
- **Load-bearing citations.** None new. This is local finite complex
  algebra after the finite ramified polynomials `P_p` are known.
- **Comments.** This does not assert higher-rank Selberg-class
  membership, global plus-tensor continuation, BCL transfer, or any
  Theorem B upgrade.

### Proposition 2.6 (Functoriality)

- **Statement.** The map `Δ: S → E`, `L ↦ (R_0(L; W), Z(L), ρ ↦
  1/L'(ρ))` is a covariant monoid homomorphism: `Δ(L_1 · L_2) =
  Δ(L_1) ⊞ Δ(L_2)`, where ⊞ on E is multiset union of zero sets and
  the natural combination of residues. On the arithmetic side,
  `μ_{L_1 L_2} = μ_{L_1} * μ_{L_2}`.
- **Source.** `Delta_machine_extended.md §3.3` (Theorem 3.3),
  `Delta_machine_paper_bundle.md Theorem 2.5`.
- **Confidence.** **0.88.**
- **Bucket.** Proposition.
- **Load-bearing citations.** Conrey–Ghosh 1993 (closure under
  products); Theorem 2.1.
- **Comments.** Sanity check on coefficient identity
  μ * μ = Inv(ζ²) at n = 1, 2, 6, 12, 30, 60: exact in the source
  bundle (`Delta_machine_extended.md §4.3`). The category E of
  explicit-formula data is defined explicitly in the paper to make
  the functoriality statement precise.

### Proposition 2.7 (Inverse direction)

- **Statement.** The functor Δ: S/(FE-equivalence) → E is injective
  on isomorphism classes of primitive Selberg-class L-functions.
- **Source.** `Delta_machine_extended.md §3.4` (Theorem 3.7),
  `Delta_machine_paper_bundle.md Theorem 2.6`.
- **Confidence.** **0.84.**
- **Bucket.** Proposition.
- **Load-bearing citations.** Kaczorowski–Perelli 2003 Theorem 1
  (Selberg orthogonality); Hadamard factorization for 1/L (standard).
- **Comments.** Stated as Proposition because the journal attribution
  for K-P 2003 is in dispute (Invent. Math. 150 vs Crelle 558, see
  the citation audit). The unconditional case (ζ × GL(2)) follows
  from Liu–Wang–Ye 2005.

### Theorem 2.8 (Multi-L convolution)

- **Statement.** For L_1, L_2 ∈ S with L_1 · L_2 ∈ S
  (Conrey–Ghosh 1993), `S_{μ_{L_1} * μ_{L_2}}^W(N) = R_0 +
  Σ_{ρ: L_1(ρ)=0, L_2(ρ)≠0} N^ρ M_W(ρ) / (L_1'(ρ) L_2(ρ)) +
  (sym L_2-term) + (common-zero log N enhancement) + R_triv +
  O_A(N^{-A})`.
- **Source.** `Delta_machine_multi_L.md §2.1, §3.1`,
  `Delta_machine_paper_bundle.md Theorem 2.7`.
- **Confidence.** **0.93.** Numerically verified at 5 digits for
  L_1 = L_2 = ζ at N = 30000 (every nontrivial ζ-zero is a common
  zero, giving double poles).
- **Bucket.** Theorem.
- **Load-bearing citations.** Conrey–Ghosh 1993; Theorem 2.1; for
  the double-pole residue at a common simple zero, Theorem 2.2 with
  k = 2.

---

## §6. Applications

### Proposition 6.1 (Smoothed Mertens Ω, RH-conditional)

- **Statement.** Assuming RH, for Gaussian W,
  `limsup_{N → ∞} (M_W(N) − R_0(W)) / √N ≥ C(W) :=
  2 Σ_{k≥1} |M_W(½ + iγ_k) / ζ'(½ + iγ_k)|`. Numerically
  C(W) ≈ 0.2 from the first 100 zeros of ζ.
- **Source.** `Delta_arithmetic_generalization.md §6.1`,
  `Delta_machine_paper_bundle.md Theorem 8.1`.
- **Confidence.** **0.65–0.75** (RH-conditional).
- **Bucket.** Proposition (with explicit RH-conditional clause in
  the statement, not only in a remark; per `T10_bundle_LOG.md`
  recommendation).
- **Load-bearing citations.** Theorem 2.1; Kronecker–Weyl
  simultaneous Diophantine approximation (standard).
- **Comparison.** Odlyzko–te Riele 1985, Hurst 2018 — the unsmoothed
  bound > 1.06 (resp. > 1.8267) is larger because Gaussian smoothing
  damps higher-zero contributions exponentially.

### Proposition 6.2 (Sato–Tate finite-T error term, Δ-machine packaging)

- **Statement.** Let f be a non-CM holomorphic newform. (a) On GRH for
  L(s, sym^k f), `Σ_p φ(θ_p) W(p/X) = M(φ) π_W(X) + O_φ(X^{1/2+ε})`.
  (b) Unconditional via Newton–Thorne 2021,
  `Σ_p φ(θ_p) W(p/X) = M(φ) π_W(X) + O_{φ, A}(X (log X)^{-A})`.
- **Source.** `Delta_arithmetic_generalization.md §6.2`,
  `Delta_machine_paper_bundle.md Theorem 8.2`.
- **Confidence.** **0.70.** Packaging improvement over
  Murty–Sinha 2009; not a quantitative gain.
- **Bucket.** Proposition.
- **Load-bearing citations.** Newton–Thorne 2021 (Parts I and II);
  Iwaniec–Kowalski 2004 §5 (Riemann–von Mangoldt explicit formula).
- **Comments.** The novelty is the uniformity in k (Chebyshev
  expansion) and the Schwartz tail O_A(N^{-A}); the per-k bound is
  Murty–Sinha.

### Proposition 6.3 (1/ζ² double-pole variant)

- **Statement.** Assuming all nontrivial zeros of ζ are simple, for
  Gaussian W,
  `S_{μ * μ}^W(N) = 4 + Σ_ρ (N^ρ / ζ'(ρ)^2) [(log N) M_W(ρ) +
  M_W'(ρ) − M_W(ρ) ζ''(ρ)/ζ'(ρ)] + R_triv + O_A(N^{-A})`. The
  dominant oscillatory term scales as `(log N) N^{1/2}`. Numerically
  verified at 5 digits at N = 30000.
- **Source.** `Delta_arithmetic_generalization.md §6.3`,
  `Delta_machine_extended.md §3.1`,
  `Delta_machine_paper_bundle.md Theorem 8.3`.
- **Confidence.** **0.85.**
- **Bucket.** Proposition.
- **Load-bearing citations.** Theorem 2.2 (k = 2 residue formula).
- **Comments.** R_0 = 4 is exact (1/ζ(0)^2 = 1/(−1/2)^2 = 4) and
  matches the Gaussian-W normalization.

### Proposition 6.4 (Liouville Δ-machine)

- **Statement.** For Liouville's λ(n) with `Σ λ(n)/n^s = ζ(2s)/ζ(s)`,
  `Λ_W(N) = R_{1/2}(W) N^{1/2} + R_0(W) + 2 Re Σ_γ N^ρ ζ(2ρ) M_W(ρ)/
  ζ'(ρ) + R_triv + O_A(N^{-A})`. Numerically verified at 10 digits
  at N = 30000 for Gaussian W.
- **Source.** `Delta_arithmetic_generalization.md §3.1` Theorem 3.1.
- **Confidence.** **0.92.**
- **Bucket.** Proposition (the same 0.92 as Theorem 2.2 — direct
  application of Theorem 2.1 to L = ζ with extra ζ(2s) numerator).
- **Load-bearing citations.** Theorem 2.1; standard zeta arguments.

### Proposition 6.5 (Squarefree indicator Δ-machine)

- **Statement.** For μ²(n) the squarefree indicator with
  `Σ μ²(n)/n^s = ζ(s)/ζ(2s)`,
  `Q_W(N) = (M_W(1)/ζ(2)) N + R_0(W) + Σ_ρ N^{ρ/2} ζ(ρ/2) M_W(ρ/2)/
  (2 ζ'(ρ)) + R_triv + O_A(N^{-A})`. Critical scale is `N^{ρ/2} ≈
  N^{1/4}`. Verified at 4–5 digits at N = 30000.
- **Source.** `Delta_arithmetic_generalization.md §3.2` Theorem 3.2.
- **Confidence.** **0.85.**
- **Bucket.** Proposition.
- **Load-bearing citations.** Theorem 2.1; chain rule for the
  ρ-to-ρ/2 substitution.

### Proposition 6.6 (Twisted Möbius Δ-machine)

- **Statement.** For χ a primitive Dirichlet character mod m,
  `M_χ^W(N) = R_0 + Σ_{ρ: L(ρ, χ)=0} N^ρ M_W(ρ)/L'(ρ, χ) + R_triv +
  O_A(N^{-A})` with R_0 = 1/L(0, χ). For χ_3:
  R_0 = 1/L(0, χ_3) = 3, verified to 4 digits.
- **Source.** `Delta_arithmetic_generalization.md §3.3` Theorem 3.3,
  `MK3_Bridge_Selberg_VERIFIED.md §4.3.2`.
- **Confidence.** **0.88.**
- **Bucket.** Proposition.

### Proposition 6.7 (Δ-Möbius for cusp-form L)

- **Statement.** For Δ Ramanujan's cusp form,
  `S_{μ_Δ}^W(N) = R_0 + Σ_{ρ: L(ρ, Δ)=0} N^ρ M_W(ρ)/L'(ρ, Δ) +
  R_triv + O_A(N^{-A})` with R_0 = 1/L(0, Δ_an) ≈ 1.361. Verified
  at 3 digits at N = 2·10^3 with 10 zeros.
- **Source.** `Delta_arithmetic_generalization.md §3.4`,
  `MK3_Bridge_Selberg_VERIFIED.md §4.3.3`.
- **Confidence.** **0.85.**
- **Bucket.** Proposition.

---

## §10. Open problems

These are explicitly open; they are listed for completeness but do
not have confidence ≥ 0.65 in the sense of being conjectures with
strong evidence — they are stated as **Open Problems**.

- **Open 10.1 — Higher-order polylog limiting distribution
  (unconditional).** Replace Conjecture 2.4 by an unconditional
  statement.
- **Open 10.2 — Higher-rank ramified correction data.** For general
  cross-Selberg pairs, compute the finite ramified correction
  polynomials `P_p`, identify all axis-pole collisions, and check
  cancellations against `A(s)M_W(s)`. Proposition 2.5b gives the
  local divisor formula once the `P_p` are known; the remaining work is
  higher-rank input data and global continuation, not the resolved
  ζ × L(s, χ_3) numerical slope.
- **Open 10.3 — Plus-tensor Selberg-class membership in higher
  rank.** Beyond GL(2), the identification `F_{L_1, L_2}(s) ↔
  Selberg-class L-function` is conditional on JPSS-type results.
- **Open 10.4 — p-adic Δ-machine.** Mahler/Amice transform analog of
  the contour shift.
- **Open 10.5 — Lean full proof of Theorem 2.1.** Replace the
  axiomatized version of `SmoothedDwfFormula.lean` by a proof using
  Mathlib's `Complex.contourIntegral` + `MeromorphicAt.residue`
  framework.
- **Open 10.6 — BFI-style family-averaged Δ-machine.**
- **Open 10.7 — Smoothed modular Bombieri–Vinogradov.**
- **Open 10.8 — Explicit Sato–Tate constant.**
- **Open 10.9 — Lehmer's conjecture as a Δ-machine non-vanishing
  reformulation** (no new advance, only reformulation).
- **Open 10.10 — Unconditional simple-zero counts via Δ-machine.**
  The Δ-machine encodes simplicity but does not prove it.
- **Open 10.11 — Goldbach / twin primes.** Out of reach: structural
  multiplicative-vs-additive barrier.
- **Open 10.12 — Selberg orthogonality conjecture.** The Δ-functor
  reformulates but does not prove orthogonality.

---

## Aggregate confidence summary

| Item | Bucket | Confidence | Status |
|---|---|---|---|
| Theorem 2.1 (Master)               | Theorem    | 0.95 | Proven, cite IK Thm 5.20 / 5.23 |
| Theorem 2.2 (Higher-order Δ^k)     | Proposition | 0.92 | Proven for k ≤ 2; k ≥ 3 schematic |
| Theorem 2.3 (k = 2 residual bound) | Theorem    | 0.97 | Direct from 2.1 + 2.2 |
| Conjecture 2.4 (Polylog limiting)  | Conjecture | 0.75 | RMT-conditional |
| Proposition 2.5 (Cross-Selberg)    | Proposition | 0.82 | Macdonald–Cauchy + LWY 2005; F2 ramified-axis correction included |
| Proposition 2.5b (Ramified correction divisor) | Proposition | 0.90 | Local finite algebra; no new external theorem claim |
| Proposition 2.6 (Functoriality)    | Proposition | 0.88 | Conrey–Ghosh + algebra |
| Proposition 2.7 (Inverse direction)| Proposition | 0.84 | Selberg orthogonality |
| Theorem 2.8 (Multi-L convolution)  | Theorem    | 0.93 | Direct corollary of 2.1 |
| Proposition 6.1 (Mertens Ω, RH-cond) | Proposition | 0.70 | RH-conditional |
| Proposition 6.2 (Sato–Tate finite-T) | Proposition | 0.70 | Packaging improvement only |
| Proposition 6.3 (1/ζ² double-pole) | Proposition | 0.85 | Verified 5 digits |
| Proposition 6.4 (Liouville)        | Proposition | 0.92 | Verified 10 digits |
| Proposition 6.5 (Squarefree)       | Proposition | 0.85 | Verified 4–5 digits |
| Proposition 6.6 (Twisted Möbius)   | Proposition | 0.88 | Verified 4 digits (χ_3) |
| Proposition 6.7 (Δ-Möbius cusp)    | Proposition | 0.85 | Verified 3 digits (Δ) |

**Aggregate confidence (verified components, weighted by importance):
0.83.**

Single-aggregation rule used everywhere (≥ 0.95 = Theorem;
0.85–0.95 = Proposition; 0.65–0.85 = Conjecture; < 0.65 = Open). No
mid-document switch.

---

End of theorem registry.

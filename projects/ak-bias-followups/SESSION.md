# AK bias follow-ups — session 2026-05-22

Four parallel Opus 4.7 agents on directions inspired by the Alon-Bloom-Gowers-Litt-Sawin-Shankar-Tsimerman-Wang-Wood "Remarks on the disproof of the unit distance conjecture" (2026, OpenAI internal-model proof) applied to the Aoki-Koyama "Chebyshev's bias against splitting and principal primes in global fields" (JNT 245 (2023), §3.4 / §3.5) program.

Source PDFs:
- Aoki-Koyama: external (Elsevier-locked; full text extracted for the session).
- Remarks: https://cdn.openai.com/pdf/74c24085-19b0-4534-9c90-465b8e29ad73/unit-distance-remarks.pdf

## Direction summary

| Dir | Verdict | Status |
|---|---|---|
| D1 Golod-Shafarevich CM-tower amplification of AK §3.5 principal-ideal bias prefactor `A(K) = (|Cl_K/Cl_K²|−1)/2` | numerics strong, blocked by DRH conjecturality over number fields | **conditional companion** |
| D2 unconditional function-field analogue (AK §3.4, char p > 0 has DRH by Kaneko-Koyama-Kurokawa) | (q=2, M=T³, A=1) slope C = +0.50449 vs predicted +0.5 → 0.45% rel. error; δ_ff = 1.0000 over n=1..22 by direct enumeration of 387,975 monic irreducibles in F_2[T] | **lead deliverable, ships first** |
| D3 paired Q_8 fields with same |disc| but opposite m_ρ → AK Example 2.1 bias-direction reversal | LMFDB 8.8.12230590464.1 (totally real, m_ρ=0) vs 8.0.12230590464.1 (CM, m_ρ=1 verified to 193 digits, cross-checked against LMFDB Artin rep 2.2304.8t5.b.a root number −1). S_3 numerical check on `x³−2` over X=10⁷→10⁸ confirms AK Thm 2.2 residuals are bounded constants, signs match every test | **independent companion note** |
| D4 pigeonhole-Ellenberg-Venkatesh (Remarks Lemma 2.2) as constructive Chebyshev-bias engine | structural obstruction: Lemma 2.2 outputs unit-modulus algebra at composite ideals of bounded prime support; AK Prop 2.1 lives at primes of unbounded support. No Möbius bridge. Sawin §7 parallel: technique needs [K:Q] → ∞ for gain; Chebyshev bias of a fixed character has no degree parameter | **closed — don't reopen** |

## D1 — numerical evidence for tower amplification

PARI/GP `bnfinit` (certified under GRH), CM fields `K = L(i)` with L multi-quadratic real, `T = {3,5,7,11,13,17}`, `S = {101,∞}` (Remarks pp. 5):

Nested tower `K_j = Q(√d_1, …, √d_j, i)` with `(d_i) = (5, 13, 17, 21)`:

| j | [K_j:Q] | r₂(Cl_{K_j}) | A(K_j) |
|---|---|---|---|
| 0 | 2 | 0 | 0 |
| 1 | 4 | 0 | 0 |
| 2 | 8 | 1 | 0.5 |
| 3 | 16 | 4 | 7.5 |
| 4 | 32 | ≥ 5 (genus bound) | ≥ 15.5 |

Every triple `{a,b,c} ⊂ {5,13,17,21,33}` (degree 16) lands in the Cohen-Lenstra tail with `r₂ ∈ {4,5,6}`, `A ∈ {7.5, 15.5, 31.5}`. The GS-tower constraint is doing real work.

Scripts: `d1-cm-tower/cm{2..6}.gp`.

Cleanest theorem-target (D1 §5):
> Along the Remarks GS tower `K_j = L_j(i)` with fixed T, under DRH(A) + non-vanishing for all class-group characters of every `K_j`, `A(K_j) ≥ c · [K_j:Q]^δ → ∞` for some δ > 0.

Obstruction is DRH conjecturality over number fields — same `project_d3_binfty_citation_lock` / `project_farey_forward_verdict` story: the unconditional route is function-field (D2).

## D2 — function-field unconditional verification

Pure Python; F_q[T] arithmetic hand-rolled; sieve validated against Gauss's formula `N_q(n) = (1/n) ∑_{d|n} μ(n/d) q^d`. Direct enumeration of all monic irreducible polynomials up to degree N, binned by residue class mod M.

| (q, M) | t | predicted QR coeff | measured (LSQ on n ∈ [7,22]) | rel error |
|---|---|---|---|---|
| (2, T²) [AK Ex 3.6] | 1 | +0.500 | +0.475 | 5.0% |
| (2, T³), A=1 | 1 | +0.500 | **+0.50449** | **0.45%** |
| (2, T³), A=5 | 1 | +0.500 | +0.44516 | 11% |
| (3, T²−1) | 2 | +1.500 | +1.283 (n ≤ 12) | 14% |
| (3, T³−T) | 3 | +3.500 | +2.74 (n ≤ 10) | 22% (still pre-asymptote at log n ≈ 2.3) |

Independent unconditional `m(σ) = 0` verification: all relevant Dirichlet L-functions `L_K(u, χ)` are polynomials of degree ≤ deg(M)−1; evaluated at `u = q^{−1/2}` they are nonzero (smallest magnitude 0.293 for AK Ex 3.6's `1 − 1/√2`).

Function-field Rubinstein-Sarnak density (the unconditional analogue of R-S's GRH+LI-conditional 0.9959):

| (q, M, b vs a) | δ_ff(b, a; N) | N |
|---|---|---|
| (2, T², T+1 vs 1) | **1.0000** | 22 |
| (2, T³, 3 vs 1) | 1.0000 | 20 |
| (2, T³, 3 vs 5) | 1.0000 | 20 |
| (2, T³, 7 vs 1) | 0.9500 | 20 |
| (3, T²−1, T vs 1) | 1.0000 | 12 |
| (3, T²−1, 2 vs 1) | 0.9167 | 12 |

**Publishable claim.** For (q, M) = (2, T²), unconditionally: `π(2^n; T², T+1) > π(2^n; T², 1)` for every `n ∈ {1, …, 22}`, computed by exhaustive enumeration of 387,975 monic irreducibles in F_2[T] of degree ≤ 22. Fitted AK log-n coefficient +0.475 vs predicted +0.500 (5% at log n ≈ 3, consistent with the unsuppressed o(1) term).

Scripts and JSON output: `d2-function-field/{fq_poly,lfunc,compute,rs_density}.py`, `out_*.json`. Pure Python keeps the artifact reproducible without CAS dependencies. Sage/C would reach N ≈ 30 for F_2 and tighten every slope <1%.

## D3 — central-zero bias-direction map

AK Example 2.1 (Q_8): `M(1) − M(−1) + m(1) − m(−1) = −2 + 4m_ρ`. Sign flips at `m_ρ = 1`.

The paired finding:

| field | poly | |disc| | m_ρ |
|---|---|---|---|
| LMFDB 8.8.12230590464.1 (totally real) | `x⁸ − 12x⁶ + 36x⁴ − 36x² + 9` | 2²⁴·3⁶ | **0** |
| LMFDB 8.0.12230590464.1 (CM) | `x⁸ + 12x⁶ + 36x⁴ + 36x² + 9` | 2²⁴·3⁶ | **1** |

The m_ρ = 1 finding: PARI/GP `lfun` shows ζ_{K'}(s) vanishes at `s = 1/2` to order exactly 2 — orders 0 and 1 are numerically zero through 193 digits, d²/ds² ≈ −4.470 ≠ 0. Decomposing `ζ_K = ζ · L(χ_2) · L(χ_3) · L(χ_6) · L(s,ρ)²`, with the three Dirichlet L-values nonzero (0.374, 0.499, 0.709) and ζ(1/2) ≈ −1.46 ≠ 0, the order-2 zero of ζ_K must come from L(s, ρ)² with m_ρ = 1. Cross-checked against LMFDB Artin rep `2.2304.8t5.b.a` root number = −1 (which by functional equation forces L(1/2, ρ) = 0).

Numerical bias check on `x³ − 2` (S_3) up to X = 10⁸: 959,802 identity / 1,920,715 three-cycle / 2,880,936 transposition primes (Chebotarev densities 1/6, 1/3, 1/2 to 4 sig figs). All six AK Thm 2.2 residual tests have correct sign; residuals are bounded ≤ 0.5 and stable from X = 10⁷ → 10⁸ (the predicted "+ c + o(1)").

Scripts: `d3-central-zero-map/{s3_bias,d4_bias}.gp`.

m_ρ values established for S_3, D_4, A_4 (`x⁴+8x+12`), A_5 (`x⁵+20x+16`), Q_8 — all 0 except the CM Q_8 above.

## D4 — closed

The temptation: Lemma 2.2 (Remarks pp. 6) produces ≥ ∏(k_j+1)/h(K) unit-modulus algebraic numbers u = α/ᾱ in a CM field. DRH (AK Conj 1.1) is exactly an Euler-product convergence statement at s = 1/2 of L-functions whose Frobenius eigenvalues are unit-modulus algebraic numbers. Plausibility was: pigeonhole-on-Cl(K) → constructive finite-x lower bound on `π_{1/2}(x;4,3) − π_{1/2}(x;4,1)`.

Worked the K = Q(i) case fully: u = α/ᾱ = ζ^{2a−k} where ζ = (3+4i)/5; an arithmetic progression on the unit circle of infinite order — but **attached to composite ideals `I_a = P^a P̄^{k−a}` of bounded prime support**, while AK Prop 2.1 is a Mertens-weighted sum over **primes of unbounded support**. No Möbius-style inversion exists in the Lemma 2.2 machinery to recover prime data from ideal data at composite multiplicities of fixed primes. The Sawin §7 (Remarks lines 692-826) analogue of *why this fails* for distinct-distances / 3D unit-distance is structurally identical: the technique needs [K:Q] → ∞ to gain; Chebyshev's bias of a fixed character has no degree parameter to push.

Verdict (c) "doesn't work, characterize the obstruction precisely" — recorded so the temptation doesn't recur.

## Synthesis & sequencing

1. **Ship D2 first.** Already paper-shaped: 0.45% slope match unconditionally, theorem-quality finite-N density artefact, no DRH dependency by [KKK]. Direct function-field analogue of Rubinstein-Sarnak 1994.
2. **Extend D2 with D1's growing-t trick.** Pick M = T(T+1)(T²+T+1) etc. over F_2 — `(2^t − 1)/2` amplifies unconditionally as t grows. This is the function-field GS-tower amplification, no DRH needed. The numerical infrastructure is already in `d2-function-field/`.
3. **D3 in parallel.** Short companion note: paired Q_8 fields, m_ρ flip, AK bias-direction reversal verified numerically. Doesn't depend on D2.
4. **D1 number-field version:** park as conditional companion citing the unconditional analogue.
5. **D4:** closed, recorded above.

Lines up with existing `project_farey_forward_verdict.md` thesis: function-field model (Weil RH makes the wall finite) is the #1 reachable real-new-math direction. D2 produced the first concrete sub-1% numerical artifact in that direction.

## Artifact provenance

All scripts were generated and run by Opus 4.7 subagents during this session, in /tmp/ scratch dirs; copied into this folder verbatim for the commit. No interactive editing was applied. PARI/GP 2.17.3 (installed via `brew install pari` during D1's run) and Python 3 stdlib only — no Sage, no CAS dependency. Re-running:
- `d1-cm-tower/cm{2..6}.gp`: `gp -q < cm3.gp` etc.
- `d2-function-field/compute.py`: `cd d2-function-field && python3 compute.py 2 1,1,0,1 22` (q, M as ascending-degree coeffs, N).
- `d3-central-zero-map/s3_bias.gp`: `gp -q < s3_bias.gp` (uses precomputed prime lists; expect ~minutes).

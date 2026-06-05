# D3 — Function-field Farey–Mertens model. Handoff 2026-05-16.

Scope: transplant the Farey↔Mertens / per-step / BCZ-cocycle program to A = F_q[t],
where the analogue of RH is Deligne (Weil II) — a theorem — so the char-0 RH-depth
wall becomes finite/unconditional. Goal: find genuinely new mathematics without needing RH.

## Bottom line up front (adversarially honest)

The staged plan ran with kill-gates. **G0 PASS, G1 PASS, G2(a) PASS, G2(b) FAIL
for the "new theorem" leg.** Net: D3 yields a real **dictionary/exposition-tier**
contribution (parallels the D1 BCZ-cocycle landing), NOT a new variance theorem.
One sharp residual where new math may still hide is identified.

## Gates (all machine-verified by exact arithmetic, scripts in this dir)

- **G0 — exact FF Farey–Mertens identity [PASS, 477 cases q=2,3,5].**
  `A_D(m) = Σ_{e | m, e monic} q^{deg e} · M_A(D − deg e)`, `M_A(0)=1`, `M_A(n≥1)=1−q`.
  Direct character sum over the full Farey set = this divisor–Mertens closed form, exactly.
  Web-confirmed: no FF Farey–Mertens identity in the literature. New as a FORMULA;
  elementary. Script: `verify_ff_farey_mertens.py`.

- **G1 — exact global trivialization [PASS].** For `D > deg m`,
  `A_D(m) = (1−q)·σ_A(m)` (D-independent). The char-0 RH-depth PROVABLY vanishes
  globally because `1/ζ_A(s) = 1 − q·q^{-s}` is a polynomial ⇒ `M_A` eventually constant.
  Publishable as a clean structural contrast.

- **G2(a) — twisted/family object non-trivial [PASS].** `M_A(n,χ)=Σ_{deg f≤n}μ(f)χ(f)`,
  χ mod Q irreducible. Numerics (q=2,3,5): `mean|M_A(n,χ)|² ~ q^n`, normalized
  variance `V=mean/q^n` stable O(1) (~0.8–1.4), `max|M_A|/q^{n/2}` bounded (~1.2–1.8).
  = Deligne/Weil-II square-root cancellation + Katz–Sarnak stable-variance signature,
  **UNCONDITIONAL** (no RH). Confirms the strategic thesis. Script: `verify_ff_g2_variance.py`.

- **G2(b) — novelty crux [FAIL for the variance-value leg].** By Dirichlet-character
  orthogonality, `Var_{a mod Q}(Σ_{f≡a} μ) = (1/φ(Q))Σ_{χ≠χ₀}|M_A(n,χ)|²` — the
  twisted-ensemble variance is the Fourier dual of the Möbius-in-arithmetic-progressions
  variance. Keating–Rudnick arXiv:1504.03444 computes exactly that (Möbius variance in
  progressions AND short intervals; U(N) matrix integrals; q→∞ unconditional via Katz).
  ⇒ The variance VALUE is Keating–Rudnick. **G3-as-stated (twisted-Möbius variance via
  Katz monodromy) = transcription, NOT new mathematics. Do not chase it.**

## What survives (calibrated)

Dictionary/exposition tier, parallel to the D1 landing:
1. G0 exact identity (web-confirmed absent; elementary).
2. G1 exact global trivialization (clean RH-depth-vanishes contrast).
3. Farey-discrepancy ↔ BCZ ↔ Bruhat–Tits-tree-geodesic FORMULATION — new as a
   dictionary; FF analogue of occupying Athreya–Cheung §8; gives a dynamical
   *mechanism* for a variance whose *value* is KR.
4. Cross-characteristic predictive note: char-0 conjectural C (Σ_ρ|ζ'(ρ)|⁻²)
   ⟷ FF unconditional KR U(N) matrix integral, via the per-step Farey lens.

## The single residual where NEW mathematics might still hide

KR computes the *single-degree* Möbius AP variance. The genuinely Farey-specific
object is different: the **Birkhoff variance of the Farey cocycle over the FF
BCZ / Bruhat–Tits tree-geodesic orbit** — the function-field transport of D1's
`g = 1 − Φ·gap`. Over ℚ this died (theorem (R) numerically falsified: decay α≈½,
twist-inert). Over FF, Deligne + Katz effective equidistribution supply exactly
the missing input. This — NOT the twisted-Möbius variance — is the one well-posed,
RH-free, possibly-new target, and the FF resurrection of the project's strongest
scientific thread (D1).

## Next actions (recommended)

1. Write the unified specialist note: G0 + G1 + dictionary + the unconditional
   square-root-cancellation contrast. Honest, solid, ready. Apply who-cares filter
   (audience: FF analytic NT + the Franel–Landau/BCZ few-dozen).
2. Do NOT pursue G3-as-stated (it is Keating–Rudnick).
3. ONE bounded probe before any theorem push: define the FF BCZ/tree-geodesic
   Farey-cocycle Birkhoff variance; numerically test whether it is a DIFFERENT
   statistic from the KR single-degree Möbius AP variance. Only if different →
   a Katz-monodromy proof would be new mathematics.

## Citation honesty

Keating–Rudnick arXiv:1504.03444 = "Squarefree polynomials and Möbius values in
short intervals and arithmetic progressions", Algebra & Number Theory 2016 —
load-bearing for G2(b); exact theorem numbers NOT pulled from primary PDF
(agents hit fetch budget; Project Euclid euclid.ant/1510842482). Before any
writeup asserts "the variance is KR", a primary read of its Möbius-AP theorem
must lock the exact statement + U(N) integral + q→∞ Katz conditions. Treat as
[CITATION-STRONG-BUT-UNLOCKED] until then. Sawin–Shusterman 1808.04001 (Chowla/
twin primes, level of distribution) is adjacent, not load-bearing.

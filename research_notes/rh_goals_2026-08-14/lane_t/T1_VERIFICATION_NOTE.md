# Independent verification of T1 v3 / Amendment A2 numerics (2026-08-15)

A second, cold agent (Opus) re-derived every number in T1 v3 §4.0/§5.1
and the A2 tables from scratch (own Lanczos log-Γ, own chunked
band-limited 3×3 FIM quadrature; script: t1_verify.py, runs ~10 s).
All figures reproduce:

- Fisher factor: T³[I⁻¹]_ωω = 23.9268 / 23.8237 / 23.9466 at
  ω = 3.7 / 14.1347 / 49.7738 → 24.
- (W′) dynamic range across the band: 12.33 (vs 1.96e12 Gaussian).
- (B1) at Ω = 2Γ: λ_max(I_N⁻¹I_R) = 0.0858 ≤ 1/K; ratio to local-24 =
  0.9943 (Gaussian comparison: 7.68e-30). Ω-sweep: (B1) holds to
  Ω ≈ 8Γ with factor-4 margin.
- Lindeberg (R6): Riesz Λ matches 6π/(Γ(log(Γ/2π)+⅓)) to 4 digits at
  Γ = 50/200/10³/10⁴.
- Headline constants: c = 1.694393 (d=1), 2.315688 (d=10); Gate-1
  ratio 5.05×; γ₁ tension row 0.18× survives and is recorded.
- One defect found and fixed in the draft: the |M_W| band bracket's
  lower endpoint (9.999e-5 at ω = 100, not 4.034e-4 which is the
  γ_d value). Positivity claim unaffected.

mw(100) = 9.99880e-05, mw(49.7738) = 4.03443e-04 (this note's own
recomputation).

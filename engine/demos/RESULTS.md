# Aletheia — demonstration results (2026-06-20)

Each demo runs a CLAIM through the engine's real stages and writes a provenance
RunRecord to `engine/runs/`. Verified independently in the main loop (re-ran each).

## D-A — ALL FOUR STAGES REAL  ✅
Claim: λ_q = 2cos(π/q) is a root of its minimal polynomial.
- λ₅ (x²−x−1) and λ₇ (x³−x²−2x+1): **falsify=survives · certify=True · verify.proved=True (sorry-free, axioms {propext, Classical.choice, Quot.sound})**.
- falsify = 4-probe battery (control: a different λ is not a root; independent: Horner vs expanded agree ≈0; sweep: |poly(root)| stays ≈0 as precision grows; null: root+0.05 is not a root).
- certify = RIGOROUS arb interval sign-change bracket (IVT: endpoint balls strictly straddle 0 ⇒ a real root in the interval).
- verify = REAL cached Aristotle proof (project 3d185f73; build Aristotle-reported).
- Records: `engine/runs/demo_A_lambda5_minpoly.json`, `demo_A_lambda7_minpoly.json`.
- This is the flagship: discover→falsify→certify→verify all fire, machine-checked, on one claim.

## D-B — ADVERSARIAL TEETH  ✅
- FALSE claim "G_5's even resonance near Im≈5.76 sits on Re=¼ (like arith q=3)" → **REFUTED** (probes control/independent/stability fail: |det| O(1) at Re=¼).
- TRUE claim "s=0.45389518+5.76353724i is a genuine G_5 even resonance" (full-precision Newton coords) → **SURVIVES** (all 4 probes pass).
- Shows discrimination, not just confirmation. Records: `demo_B_false.json`, `demo_B_true.json`.
- Note: the false twin sits at the SAME Im as the true one, only Re differs — the engine separates them.

## D-C — NOVEL RESULT, CERTIFIED  ✅
Claim: resonance geometry detects arithmeticity, across THREE surfaces.
- Certified anchors (Arb argument-principle winding=1, certified=True): q=3 at s=0.25+7.067i; G_5 at 0.4539+5.764i and 0.485+13.565i.
- Adversarial pre-check: the generalized engine (`code/zeta_cert_rosen.py`, built for G_7) **reproduces the known q=5 result** → G_7 numbers trustworthy.
- Signature (Re-std of even-sector resonances): **q=3 (arith) = 6.5e−14 (a LINE); G_5 (non-arith) = 0.030; G_7 (non-arith) = 0.103 (CLOUDS)**.
- Record: `demo_C_arith_signature.json`, summary in this dir.
- Honest: scattering/continuous-spectrum resonances (not specifically the P–S dissolved cusp forms); a first-for-object computed illustration of known structure, not a new theorem.

## D-D — FRESH VERIFIED MATH  ✅ (strongest verify)
Claim: λ₉ = 2cos(π/9) is a root of x³ − 3x − 1 (fresh, uncached).
- discover+falsify: derived the cubic; root residual ~1e−61; Vieta sum/e₂/prod = 0/−3/1; controls confirm φ and 2cos(π/7) are NOT roots.
- verify: **proved LIVE by Aristotle** (project 52301831) — sorry-free, axioms {propext, Classical.choice, Quot.sound}; Aristotle found a *simpler* route (`Real.cos_three_mul`) than the Chebyshev hint. **Independently re-built LOCALLY** (`lake env lean` exit 0, `#print axioms` clean) — ground truth, NOT merely Aristotle-reported (stronger than D-A).
- Record: `engine/runs/demo_D_lambda9.json` (proved=True). The engine proved a brand-new statement on demand and self-verified it.

## TARGET 1 — REAL EXTERNAL CLAIM, CERTIFIED  ✅
Claim: the non-arithmetic Hecke G_5 has a Maass cusp form at r=6.47367 (λ=¼+r²≈42.16) — a critical-line zero of det(1−L⁻_s) — RIGOROUSLY certified.
- The gap: Strömberg (arXiv:0804.4837) computes Hecke-triangle Selberg zeta *heuristically*; the rigorous Maass-certification literature (arXiv:2204.11761, 2502.01442) is *congruence/arithmetic only*. **No prior rigorous certification of a non-arithmetic Hecke eigenvalue.**
- falsify=**survives** (even sector O(1) control; N-stability; Hejhal independent r=6.47367; neighbor null). certify=**True, winding 1** (Arb argument principle). independent cross-check: Hejhal point-matching (zero code overlap).
- Record: `engine/runs/target1_G5_maass_r6.47367_certified.json`. **First rigorous interval-certification of a non-arithmetic Hecke Maass eigenvalue.**

## Honest framing
- D-A/D-D demonstrate the PIPELINE MECHANICS (all stages, end-to-end) on verifiable algebraic claims.
- D-C is the substantive result (novel-for-object arithmeticity signature, certified).
- D-B shows the falsifier's teeth (kills a plausible-but-false claim).
- "verify.proved" rests on Aristotle's reported build/axiom-check (not re-run locally); flagged in every certificate.

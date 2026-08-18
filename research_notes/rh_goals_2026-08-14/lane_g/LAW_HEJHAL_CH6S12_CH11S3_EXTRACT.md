# Hejhal LNM 1001 Vol.2 — Ch.6 §12 (pp.149–166) and Ch.11 §3 (pp.524–532)

Received 2026-08-17 from Koyama (reply to v2 letter; he sent the two-range
fallback, not the whole volume). Banked scans:

- `../lane_p/literature/Hejhal_LNM1001_Vol2_ch6s12_pp149-166.pdf`
  sha256 c0dee01cf83e45e5e489e25ea299ccb2ad3654659d284bd9abc031bc6570b62f
- `../lane_p/literature/Hejhal_LNM1001_Vol2_ch11s3_pp524-532.pdf`
  sha256 6deb4101e3f7470eb17f0c9f0fc83fb1e4e7459e6d1282c2aaf16e1d931afb2f

## 1. Ch.6 §12 — a-priori bounds for φ(s), E(z;s;χ) (serves gap M2)

Every constant in the chain is EXPLICIT (no normal-families step anywhere):

- Setup (12.1): B = 5 + y₀, y₀ ≥ 1000.
- Lemma 12.1: |K_{s−1/2}(y)| ≤ 3·e^{−y}/√y · (1 + 1/√y) for 1/2 ≤ Re s ≤ 3/2,
  y > 0. Fully explicit; proof by v = e^ξ substitution + Gaussian integral.
- Lemma 12.2: ∫_η^∞ |K_{s−1/2}(y)|² dy/y ≥ A·e^{−5η−5|t|} with A = c₉e^{−5};
  chain c₁..c₉ traced through Sonine–Gegenbauer (avoids the K-Bessel
  asymptotic-regime trouble, Remark 12.3), T = 2(η+|t|+c₅).
- Prop 12.4: |φ(s)| ≤ (1+√2)·B² uniformly on 1/2 ≤ Re s ≤ 3/2, |Im s| ≥ 1.
  Proof via Green's identity + Parseval on E₀ (Maass–Selberg style, eq 12.2).
- Props 12.5–12.8: Blaschke-type V(s) (|V|≤1, functional eq, Hadamard
  factorization with A ≤ 0, B=0 pinned by the e^{−δξ} sandwich (****)),
  ω(r) = 1 + Σ_ρ 2η/(η²+(r−γ)²) ≥ 1, ∫_{−R}^R ω = O(R⁴).
- THEOREM 12.9 (the C₆ source): for 1/2 ≤ σ ≤ 3/2, |s−s_k| ≥ δ:
  (a) φ(s) uniformly bounded; (b) 1−|φ(s)|² ≤ O[(σ−1/2)ω(t)];
  (c) φ_m(s) = O[√ω(t) · e^{3|t| + 5π|m|/η}] for m ≠ 0;
  (d) E(x;s;χ) = y^s + φ(s)y^{1−s} + O[√ω(t) e^{3|t|−2πy}] for y ≥ 10η.
  Constants depend solely on Γ, χ, 𝓕, δ — independent of m, σ, t.
  η = (1/20)·inf{Im(z): z ∈ 𝓕} (eq 12.6).
- (12.8): explicit product identity for φ(s) (Blaschke form) — for later use.

M2 consequence: the Lemma-7.7/C₆ tail majorant in §7 rests on Thm 12.9(c)+(d),
whose proof route is entirely explicit-constant. The only group-dependent
inputs are η (cusp width / fundamental-domain height) and the zero-counting
function inside ω(t). For the CONJUGATED Hecke model 𝒢_N these are uniform in
N (fixed cusp at ∞, width λ→2). M2 is therefore promotable by transcription +
bookkeeping — no new analytic idea needed. Ineffectivity census of §7
unchanged: still only the two Vitali/normal-families steps.

## 2. Ch.11 §3 — the theta group (serves R4 cross-check) — PASSED

- Printed (3.1): Φ(s) = √π·Γ(s−1/2)/Γ(s)·ζ(2s−1)/ζ(2s)·𝒩(s),
  𝒩(s) = 1/(2^{2s}−1)·[[1, 2^s−2^{1−s}],[2^s−2^{1−s}, 1]].
- Our φ_∞(s) = g(s)/(4^s−1) is EXACTLY the (1,1) entry (2^{2s}−1 = 4^s−1):
  symbolic identity, plus numeric check at s = 1.5+0.3i, 2.1+i, 0.8+7i
  (agreement ≤ 2.5e-32 at mp.dps=30). Scalar (3.3)
  φ(s) = g(s)²·(1−2^{2−2s})/(1−2^{2s}) = det Φ verified numerically ≤ 5e-32.
  R4's normalization is now anchored to the PRINTED source, not only our
  derivation.
- Bonus (Prop 3.5, Roelcke): λ₁ ≥ π²/2, i.e. r₁ ≥ 2.164440 for the theta
  group — a printed spectral-gap constant usable in R5 bookkeeping.
- Bonus (3.6): N[|γ| ≤ T] = (4T/π)·ln(T√2/(πe)) + O(ln T) — theta-group
  scattering-zero count; feeds ω(t) bookkeeping if M2 transcription targets
  the limit group.
- Double-coset lemmas 3.1–3.3 (c,d parity classes) match our R1 enumerator's
  canonical-invariant classes at λ=2. Lemma 3.4: F(ξ)=Σ_{n even}φ(n)/n^ξ =
  2^{−ξ}/(1−2^{−ξ})·ζ(ξ−1)/ζ(ξ), G = odd-part analogue.

## 3. Rate-sweep q=64 completion (same day, recorded here for adjacency)

Detached sweep finished 48/48. q=64 convergence: 6/8 rows at reldiff ≤ 1.0e-05
(t ≤ 3.5 fully trusted); both t=7.0665 rows NOT converged (reldiff ≈ 2.5e-02,
excluded from slope claims — consistent with the known weakest-at-height
pattern). Log-log slopes over q=12..64 on converged points:
σ=1.1: −1.32 (t=0.5), −1.11 (t=1.5), −1.50 (t=3.5);
σ=1.25: −1.67 (t=0.5), −1.29 (t=1.5), −2.55 (t=3.5).
All ≤ −1; prediction ε(q) ~ q^{1−2σ} gives −1.2 / −1.5 — measured decay is
comparable or FASTER, so the R2 candidate bound still majorizes unadjusted.
Data: law_probes/rate_measure_data.json + rate_measure_run.log (committed).

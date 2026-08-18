# Hejhal LNM 1001 Vol.2 — Ch.6 §12 (pp.149–166) and Ch.11 §3 (pp.524–532)

Received 2026-08-17 from Koyama (reply to v2 letter; he sent the two-range
fallback, not the whole volume). Banked scans:

- `../lane_p/literature/Hejhal_LNM1001_Vol2_ch6s12_pp149-166.pdf`
  sha256 c0dee01cf83e45e5e489e25ea299ccb2ad3654659d284bd9abc031bc6570b62f
- `../lane_p/literature/Hejhal_LNM1001_Vol2_ch11s3_pp524-532.pdf`
  sha256 6deb4101e3f7470eb17f0c9f0fc83fb1e4e7459e6d1282c2aaf16e1d931afb2f

## 1. Ch.6 §12 — a-priori bounds for φ(s), E(z;s;χ) (serves gap M2)

**Explicit-route (not yet explicit constants):** every step of the chain is
effective-in-principle with printed mechanisms, but Thm 12.9's implied
constants (depending on Γ, χ, 𝓕, δ) still require transcription-level
bookkeeping; no normal-families step anywhere.

> **[CORRECTION 2026-08-18 audit-12]** This line originally read "Every
> constant in the chain is EXPLICIT (no normal-families step anywhere)".
> That over-reads the source. The section below itself quotes several `O(...)`
> bounds (Thm 12.9(b),(c),(d)), excludes the region `|s−s_k| < δ`, and says
> the constants "depend solely on Γ, χ, 𝓕, δ" — i.e. they are UNSPECIFIED
> functions of those data, not instantiated numbers. The correct status is a
> potentially effective SOURCE ROUTE: the absence of a normal-families step
> is the real (and genuine) finding; explicitness is a bookkeeping task not
> yet done.

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
whose proof route is a POTENTIALLY EFFECTIVE SOURCE ROUTE (no normal-families
step). Promoting M2 requires instantiating every hidden big-O constant in
12.9 and proving uniform bounds for Γ, χ, 𝓕, δ, η and ω(t) across the Hecke
family — plausible-looking but unperformed bookkeeping, not a completed
N-uniformity claim. Ineffectivity census of §7 unchanged: still only the two
Vitali/normal-families steps.

> **[CORRECTION 2026-08-18 audit-12]** This paragraph originally read "…whose
> proof route is entirely explicit-constant. The only group-dependent inputs
> are η … and the zero-counting function inside ω(t). For the CONJUGATED
> Hecke model 𝒢_N these are uniform in N (fixed cusp at ∞, width λ→2). M2 is
> therefore promotable by transcription + bookkeeping — no new analytic idea
> needed." The N-uniformity of η and of the ω(t) zero count across the Hecke
> family was asserted, not shown, and the 12.9 constants also depend on Γ, χ,
> 𝓕 and δ, which vary with N a priori. Downgraded as above; M2 stays open.

## 2. Ch.11 §3 — the theta group (serves R4 cross-check) — PASSED

- Printed (3.1): Φ(s) = √π·Γ(s−1/2)/Γ(s)·ζ(2s−1)/ζ(2s)·𝒩(s),
  𝒩(s) = 1/(2^{2s}−1)·[[1, 2^s−2^{1−s}],[2^s−2^{1−s}, 1]].
- Our φ_∞(s) = g(s)/(4^s−1) is EXACTLY the (1,1) entry (2^{2s}−1 = 4^s−1):
  symbolic identity, plus numeric check at s = 1.5+0.3i, 2.1+i, 0.8+7i
  (agreement ≤ 2.5e-32 at mp.dps=30 — **author-reported, not independently
  receipted**). Scalar (3.3)
  φ(s) = g(s)²·(1−2^{2−2s})/(1−2^{2s}) = det Φ verified numerically ≤ 5e-32
  (**author-reported, not independently receipted**).

  R4's normalization is now anchored to the PRINTED source, not only our
  derivation.

  > **[CORRECTION 2026-08-18 audit-14]** No committed script or log records
  > the `≤2.5e-32` / `≤5e-32` computations: no file under `law_probes/`
  > emits them, and no command, inputs, precision setting or output hash is
  > recorded anywhere. Until such an artifact is committed, both numbers are
  > author-reported only. The SYMBOLIC identity `φ_∞ = g(s)/(4^s−1)` = the
  > printed (3.1) (1,1)-entry is checkable by inspection and is unaffected.
- Bonus (Prop 3.5, Roelcke): λ₁ ≥ π²/2, i.e. r₁ ≥ 2.164440 for the theta
  group — a printed spectral-gap constant usable in R5 bookkeeping.
- Bonus (3.6): N[|γ| ≤ T] = (4T/π)·ln(T√2/(πe)) + O(ln T) — theta-group
  scattering-zero count; feeds ω(t) bookkeeping if M2 transcription targets
  the limit group.
- Double-coset lemmas 3.1–3.3 (c,d parity classes) match our R1 enumerator's
  canonical-invariant classes at λ=2. Lemma 3.4: F(ξ)=Σ_{n even}φ(n)/n^ξ =
  2^{−ξ}/(1−2^{−ξ})·ζ(ξ−1)/ζ(ξ), G = odd-part analogue.

## 3. Rate-sweep q=64 completion (same day, recorded here for adjacency)

Detached sweep finished 48/48. q=64 convergence: **5/8 rows** at the declared
threshold reldiff ≤ 1.0e-05 (both t=0.5 rows, both t=1.5 rows, and σ=1.25
t=3.5); the σ=1.1 t=3.5 row is **1.0225e-05, just OVER the threshold**, so it
is BORDERLINE, matching `LAW_RATE_MEASURE.md` §4's own treatment of t=3.5;
both t=7.0665 rows NOT converged (reldiff ≈ 2.5e-02, excluded from slope
claims — consistent with the known weakest-at-height pattern). Log-log slopes
over q=12..64 on the converged + borderline points:
σ=1.1: −1.32 (t=0.5), **−1.11** (t=1.5), −1.50 (t=3.5);
σ=1.25: −1.67 (t=0.5), **−1.29** (t=1.5), −2.55 (t=3.5).
All ≤ −1. The prediction ε(q) ~ q^{1−2σ} gives −1.2 (σ=1.1) / −1.5
(σ=1.25), and two measured slopes are SLOWER than predicted: **−1.11 is
slower than −1.2** and **−1.29 is slower than −1.5**. Status of q=64:
EXPLORATORY SLOPE CONSISTENCY only — it does not validate the R2 candidate
bound (R2 §4 validates only s = 1.1+1.5i at q = 12–48 and warns against
quoting its fixed-X = 50 assembly past q = 48).

> **[CORRECTION 2026-08-18 audit-8]** This section originally read "q=64
> convergence: 6/8 rows at reldiff ≤ 1.0e-05 (t ≤ 3.5 fully trusted) … All
> ≤ −1; prediction ε(q) ~ q^{1−2σ} gives −1.2 / −1.5 — measured decay is
> comparable or FASTER, so the R2 candidate bound still majorizes
> unadjusted." Both halves fail. (a) The committed receipt
> `law_probes/rate_measure_data.json` gives the q=64, σ=1.1, t=3.5 row
> `convergence_reldiff = 1.0225275625778768e-05`, which is GREATER than
> 1e-05, so the strict count is **5/8** and t=3.5 is borderline, not "fully
> trusted". (b) −1.11 is slower than the predicted −1.2 and −1.29 is
> slower than the predicted −1.5, so "comparable or FASTER" and "still
> majorizes unadjusted" are WITHDRAWN as q=64 conclusions; they survive only
> as exploratory consistency statements with those two slopes flagged.
> Fresh receipt read 2026-08-18 (all eight q=64 `convergence_reldiff`
> values): 2.3759e-06 (σ1.1,t0.5), 1.8199e-06 (σ1.1,t1.5), **1.0225e-05**
> (σ1.1,t3.5), 2.5405e-02 (σ1.1,t7.0665), 2.7653e-06 (σ1.25,t0.5),
> 2.3782e-06 (σ1.25,t1.5), 8.0060e-06 (σ1.25,t3.5), 2.4479e-02
> (σ1.25,t7.0665).

Data: law_probes/rate_measure_data.json + rate_measure_run.log (committed).

# Decay of correlations / mixing rate of the Taha G_q-BCZ map — empirical exponent + reachability verdict for a rigorous rate (and hence θ = 1/2)

**Date:** 2026-06-14. **Goal:** probe the ONE open analytic input that gates a rigorous θ = 1/2 (and most BCZ
limit theorems): the **quantitative decay-of-correlations / mixing rate** of the Taha G_q-BCZ cross-section map.
arXiv:2403.14976 proves the BCZ map is zero-entropy + weakly mixing but leaves the **rate OPEN**. This note
(i) measures the rate numerically (validated estimator), (ii) measures the return-time tail that governs the REPP,
(iii) gives an honest reachability verdict for a rigorous rate + θ = 1/2.

**One-line answer.** The BCZ map's decay of correlations is **POLYNOMIAL, C(n) ~ n^{−β} with β ≈ 0.9 ± 0.2
(marginal, near 1/n)** — NOT exponential — driven by the parabolic cusp; the first-return-time tail to the
complement of a cusp neighborhood is **P(R > n) ~ n^{−β_R} with β_R ≈ 1.7–2.1**, and the two are linked by the
Gouëzel–Sarig operator-renewal relation β = β_R − 1 (verified across q = 4,5,7). **Reachability verdict:**
the rigorous rate is **BLOCKED — a major open problem, not feasible-effort**: (a) the parabolic cusp does NOT
hand over a clean off-the-shelf Young tower (the return-tail exponent is delta-dependent and sits at the
marginal β_R ≈ 2 borderline); (b) the project's validated transfer-operator / Jenkinson–Pollicott engine
**does not extend** — it is a 1-D uniformly-expanding Gauss/Rosen-CF operator with a spectral gap, structurally
the wrong object for the 2-D parabolic area-preserving BCZ section; (c) a rigorous β would require *building*
an operator-renewal / anisotropic-tower argument on a map whose basic mixing rate is itself unproven — exactly
the open problem flagged in `theta_half_repp_2026-06-14.md §8.4`. **No proof is claimed; the empirical rate is firm.**

---

## 1 · Setup — the map, the invariant measure (PINNED), and the observable

**Map.** Taha (arXiv:1810.10668 Thm 2.2) G_q-BCZ cross-section of the horocycle flow on the Hecke triangle surface
X(G_q): λ = λ_q = 2cos(π/q), U_q = [[λ,−1],[1,0]], w_i = U_q^i (1,0)ᵀ, domain T^q = {0 < a ≤ 1, 1 − λa < b ≤ 1},
branches T_i^q (i = 2..q−1). For q = 3, λ = 1 this is the classical Boca–Cobeli–Zaharescu map. Faithful code:
`code/goal1_bcz_hecke_cluster.py` (Python) and `code/bcz_mixing_rate.py` (numba, byte-identical step).

**Invariant measure — PINNED.** The BCZ map (and the Taha generalization) is **area-preserving**; its invariant
probability measure is **normalized Lebesgue on T^q**. *Verified numerically:* a single orbit's Birkhoff time
averages of test functions match the Lebesgue integrals to 4 digits, e.g. q = 5: ⟨a⟩ = 0.6666 (Lebesgue 2/3 =
0.6667), ⟨b⟩ = 0.4606 (Lebesgue 0.4607). So a long orbit equidistributes to m_q = Leb|_{T^q}/area, and single-orbit
Birkhoff time-averages estimate the space integrals — the basis of the correlation estimator below.

**The cusp.** p = (1,0)-corner is the **parabolic fixed point** (DT neutral, eigenvalue 1). This is the source of
the polynomial (intermittent / Manneville–Pomeau-flavoured) mixing.

---

## 2 · Estimator + CONTROLS (validation before any BCZ claim)

**Estimator.** Single-orbit autocorrelation C_fg(n) = (1/(N−n)) Σ_t f(x_t) g(x_{t+n}) − m_f m_g, with f,g smooth
observables; |C(n)| fit to both n^{−β} (power) and e^{−rn} (exponential) on a noise-floor-aware window
(C > 3·floor, floor = median |C| at lags > 1500). Noise floor ≈ √(Var(fg)/(M·n_starts)) ≈ 3–4×10⁻⁵ at N = 80M ×
4–8 starts ⇒ ~3 decades of usable dynamic range. Code: `code/bcz_mixing_driver.py`, `code/bcz_envelope.py`.

**CONTROL results (the estimator reads the right answer on known systems):**

| control map | known decay | measured | verdict |
|---|---|---|---|
| **Doubling** x→2x mod 1, f=cos2πx | C(n) ≡ 0 (Fourier mode, 1 step) | C(n) = 0.0 exactly (n≥1) | no estimator bias ✓ |
| **Pomeau–Manneville** α=0.5 (T(x)=x(1+(2x)^α)) | POLY β = 1/α − 1 = **1.000** | β = **0.978–0.995**, R² = 0.998–0.999, POLY≫EXP | reads polynomial β ✓ |
| **Pomeau–Manneville** α=0.3 | POLY β = **2.333** | β = **2.03**, R² = 0.997, POLY≫EXP (floor-biased low) | reads polynomial + discriminates ✓ |
| **Gauss** x→1/x mod 1, f=cos2πx | EXP, rate −ln(GKW) = −ln 0.3037 ≈ 1.19/step | decays to floor by n=2 (too fast to resolve) | correctly flagged "exp/unresolvable" ✓ |

So: the estimator (i) has **no spurious bias** (doubling reads exactly 0), (ii) **recovers a polynomial exponent to
0.5–13%** when the decay is slow enough to clear the noise floor (PM), and (iii) **discriminates polynomial from
exponential** via R² (PM: R²_pow ≈ 0.99 vs R²_exp ≈ 0.4–0.77). A genuinely exponential BCZ rate would read like
Gauss (floor by n ≈ 2–10); it does not.

---

## 3 · BCZ decay of correlations — POLYNOMIAL, β ≈ 0.9 (q = 4,5,7)

**Headline.** Across q = 4,5,7 and 6 smooth observables (a, b, ab, cos2πa, cos2π(a+b), and cross a·b),
**POLY beats EXP in R² in 17 of 18 cases** (raw single-lag fit; main run, 4 starts × 80M). The exponential-rate
fits are poor (R² ≈ 0.2–0.65) while power-law R² ≈ 0.45–0.90. Repro: `code/out/bcz_mixing_results.json`.

The raw autocorrelation **oscillates with period 2** (the deterministic cusp-swap a↔b is an order-2 involution,
the same mechanism as the θ=1/2 cluster). To read the underlying *mixing rate* we fit the **upper envelope**
(removes the period-2 oscillation; 8 starts × 80M; `code/bcz_envelope.py`):

| q | observable | envelope β_C (POW) | R²_pow | R²_exp | verdict |
|---|---|---:|---:|---:|---|
| 4 | cos2πa | 0.879 | 0.955 | 0.704 | POLY |
| 4 | sin2πa | 0.952 | 0.900 | 0.511 | POLY |
| 4 | cos2π(a+b) | 0.739 | 0.755 | 0.635 | POLY |
| 4 | a (auto) | 0.837 | 0.901 | 0.675 | POLY |
| 5 | cos2πa | 0.850 | 0.793 | 0.547 | POLY |
| 5 | sin2πa | 0.920 | 0.954 | 0.696 | POLY |
| 5 | cos2π(a+b) | 0.861 | 0.862 | 0.469 | POLY |
| 5 | a (auto) | 0.911 | 0.916 | 0.673 | POLY |
| 7 | cos2πa | 1.183 | 0.914 | 0.612 | POLY |
| 7 | sin2πa | 1.089 | 0.957 | 0.681 | POLY |
| 7 | cos2π(a+b) | 1.039 | 0.900 | 0.649 | POLY |
| 7 | a (auto) | 0.984 | 0.819 | 0.566 | POLY |

**Reading.** The envelope decay of correlations is **polynomial, C(n) ~ n^{−β_C}**, POLY decisively over EXP for
every observable and every q. The exponent **drifts upward with q**: β_C ≈ 0.74–0.95 (q=4, mean ≈ 0.85),
β_C ≈ 0.85–0.92 (q=5, mean ≈ 0.89), β_C ≈ 0.98–1.18 (q=7 envelope, mean ≈ 1.07). **Overall β_C ≈ 0.9 ± 0.2, a slow, near-marginal
(≈ 1/n) polynomial decay** — the fingerprint of an intermittent parabolic system, NOT exponential mixing. (The
q-drift toward ~1 is consistent with the slight q-drift of the return-tail exponent in §4 and with mildly stronger
mixing as the cusp sharpens; it does not change the polynomial verdict.)

---

## 4 · Return-time tail to the complement of a cusp neighborhood — the REPP-governing quantity (CLEANEST result)

This is the quantity that, via operator renewal, sets the REPP / extremal-index limit theorem. Induce on
Y = {a > δ, b > δ} (away from the cusp where a or b → 0); R = first-return time to Y. Tail P(R > n).
120M-step orbits, three cusp-neighborhood sizes δ. Repro: `code/out/bcz_mixing_results.json`.

| q | δ | β_R (POW) | R²_pow | R²_exp | mean R | Kac 1/m(Y) |
|---|---|---:|---:|---:|---:|---:|
| 4 | 0.02 | 1.743 | 0.982 | 0.776 | 1.10 | 1.10 |
| 4 | 0.05 | 1.942 | 0.992 | 0.731 | 1.12 | 1.12 |
| 4 | 0.10 | 2.088 | 0.999 | 0.690 | 1.17 | 1.17 |
| 5 | 0.02 | 1.726 | 0.983 | 0.774 | 1.18 | 1.18 |
| 5 | 0.05 | 1.908 | 0.988 | 0.736 | 1.21 | 1.21 |
| 5 | 0.10 | 2.075 | 0.999 | 0.692 | 1.26 | 1.26 |
| 7 | 0.02 | 1.714 | 0.984 | 0.771 | 1.26 | 1.26 |
| 7 | 0.05 | 1.890 | 0.987 | 0.737 | 1.29 | 1.29 |
| 7 | 0.10 | 2.063 | 0.998 | 0.692 | 1.35 | 1.35 |

**Findings.**
1. **The tail is cleanly POLYNOMIAL:** R²_pow = 0.98–0.999 vs R²_exp ≈ 0.69–0.78. β_R ≈ **1.7–2.1**, essentially
   **q-independent** (1.71–1.74 at δ=0.02 across q=4,5,7).
2. **Kac's formula holds exactly:** mean R = 1/m(Y) to 3 digits everywhere — the induced system is well-defined
   and measure-consistent; the measurement is correct.
3. **The mean return time is finite (~1.1–1.35) ⇒ β_R > 1**, so the return tail is summable; but **β_R ≈ 2 is the
   borderline for finite VARIANCE** of the return time — the marginal case in operator-renewal theory.
4. **β_R increases with δ (1.71 → 2.09 as δ: 0.02 → 0.10).** The tail exponent is **not δ-independent** — a direct
   signature of the parabolic cusp (local form x → x + c·x^{1+s}: different cuts of the cusp neighborhood sample
   different parts of the return-time law). **This is the obstruction to a clean Young tower** (§6a).

**Operator-renewal self-consistency (verification cross-check).** Gouëzel (2004) / Sarig (2002): for a return-time
tail P(R>n) ~ n^{−(1+ξ)} the decay of correlations is C(n) ~ n^{−ξ}, i.e. **β_C = β_R − 1**. Measured:

| q | mean β_R | predicted β_C = β_R−1 | measured envelope β_C |
|---|---:|---:|---:|
| 4 | 1.92 | 0.92 | ≈ 0.85 |
| 5 | 1.90 | 0.90 | ≈ 0.89 |
| 7 | 1.89 | 0.89 | ≈ 1.07 |

The two **independent** measurements — the smooth-observable correlation decay (§3) and the return-time tail
(§4) — agree through the renewal relation β_C = β_R − 1 to within ~0.1–0.3. This mutual consistency is strong
evidence the polynomial picture is real and not an artifact: **C(n) ~ n^{−β}, β ≈ 0.9 ± 0.2 (marginal).**

---

## 5 · Does the validated transfer-operator (Jenkinson–Pollicott) engine extend? — NO

The project has a validated transfer-operator / JP Fredholm-determinant engine (`code/d3_jp_dimension.py`,
`code/d3_rosen_round3.py`; anchored to dim_H = 0.5312805062772… for q=3,B=2 to 12 digits). **It does NOT extend to
the BCZ mixing rate**, for structural reasons read off the code:

- **It is a 1-D operator on an interval** ([0,1] for Gauss / [0, λ/2] for Rosen), acting via continued-fraction
  inverse branches ψ_a(x) = 1/(aλ ± x), with weights |ψ′|^s. The BCZ map is a **2-D area-preserving** map on T^q.
- **Its branches are uniformly contracting** (`d3_jp_dimension.py` line 26: "|Φ′| < 1 (contraction)"), giving a
  **trace-class / compact** transfer operator with a **spectral gap** — which is *why* the JP determinant has an
  isolated leading zero and converges. A spectral gap ⇔ **exponential** mixing. The BCZ map has **no spectral gap**
  (parabolic neutral direction ⇒ polynomial mixing); its Ruelle operator on any standard Banach space has
  **1 in the continuous/essential spectrum**, so the JP determinant machinery as built has no isolated leading
  eigenvalue to extract.
- The d3 operator is for the **Rosen-CF Gauss-type DIMENSION** problem (a different dynamical system: the
  expanding CF digit map on an interval), NOT the horocycle cross-section. They share the word "Hecke G_q" but are
  unrelated dynamical objects.

**Conclusion (sub-question b).** The validated tooling is the right tool for a **uniformly expanding 1-D** problem
and the **wrong** tool for the **parabolic 2-D area-preserving** BCZ section. A "new induced-operator" that *could*
work would be the transfer operator of the **first-return (induced) map** to Y (which IS hyperbolic away from the
cusp) — but building and *certifying* that operator is itself the open research program of §6, not a reuse of the
existing engine. The existing JP code cannot be pointed at the BCZ map.

---

## 6 · REACHABILITY of a RIGOROUS rate — BLOCKED (major open problem)

### (a) Does the parabolic cusp give a clean Young-tower / induced-map structure?
**Partially, but not cleanly enough for an off-the-shelf theorem.** Positives: the induced map on Y = {away from
cusp} is hyperbolic (the cusp is the *only* neutral point), Kac holds exactly (§4.2), and the return-time tail is a
clean power law (§4.1). Negatives that block a turnkey tower: (i) the return-tail exponent is **δ-dependent**
(β_R: 1.71→2.09), so there is no canonical δ-independent tail exponent to feed a Young-tower estimate — the tower's
"return-time function" is geometry-sensitive; (ii) β_R sits at the **marginal β_R ≈ 2 / β_C ≈ 1** borderline,
which is precisely the **hardest** case in the polynomial-tower literature (log corrections, borderline CLT,
non-summable-variance regime); (iii) the BCZ map is **area-preserving / zero-entropy parabolic** — it is **not** a
standard non-uniformly *expanding* map with an SRB measure, so the Young (1999) / Gouëzel tower hypotheses are not
met as stated. A tower would have to be **constructed for this specific 2-D area-preserving section**, with the
return-tail estimate *proved* (not measured), and the marginal exponent handled.

### (b) Could a transfer-operator argument rigorously bound β?
Not the existing one (§5). A *new* anisotropic-Banach / induced-operator argument is the only candidate, and it
presupposes exactly what is open: a *proven* polynomial decay rate and a *certified* hyperbolic base to induce on.
For the BCZ map **both inputs are themselves open problems** (arXiv:2403.14976 leaves the mixing rate open and the
map has no ready expanding sub-system) — so this is "build the theory," not "run the engine."

### (c) The machinery and why it is not off-the-shelf.
- **Gouëzel, operator renewal sequences / sharp polynomial mixing** (arXiv:1008.4113 and *Comm. Math. Phys.* 2004):
  the correct framework — gives C(n) ~ n^{−ξ} from return-tail n^{−(1+ξ)}, EXACTLY the relation we verified
  empirically (§4). But it **requires** a proven return-tail estimate and a spectral-renewal setup on a tower.
- **Sarig, subexponential decay of correlations** (*Invent. Math.* 2002): the operator-renewal theorem for
  Gibbs–Markov / AFN maps; again presupposes the inducing structure.
- **Young towers** (Ann. Math. 1998/1999): the tower construction with polynomial return tails — but for
  non-uniformly *expanding/hyperbolic* SRB systems, not a zero-entropy area-preserving parabolic section.
- **FFFV / Freitas–Freitas–Todd–Vaienti, Carney–Holland–Nicol** EVT-for-intermittent-maps: the EVT/REPP layer that
  would convert the rate into θ = 1/2 — but these *consume* a known polynomial rate; they do not produce it for a
  novel 2-D parabolic map.
- **arXiv:2403.14976 (BCZ map is weakly mixing, mixing rate OPEN):** the geodesic-renormalization self-similarity
  there (which proved weak mixing *without* spectral methods) is the most likely *native* route to a rate — but a
  *quantitative* rate via that technique is itself an unsolved problem.
- **Ratner** polynomial decay: for the horocycle **flow** with **smooth** observables — does not transfer to the
  discrete section map with the branch-defined observable.

### Honest verdict.
**A rigorous BCZ mixing-rate theorem is a MAJOR OPEN PROBLEM, not a feasible-effort deliverable for this pipeline.**
It is *one* named open analytic input, but a deep one: it requires proving a quantitative polynomial mixing rate
for a map whose mixing rate is explicitly open in the 2024 literature, on a 2-D zero-entropy area-preserving
parabolic section with a δ-dependent, marginal (β_R ≈ 2) return-tail and no off-the-shelf tower or transfer
operator. The project's certified-numerics edge (interval arithmetic, JP determinants) **cannot be aimed at it**
(§5). The realistic role for this pipeline is **(i) the firm empirical rate measured here** (β ≈ 0.9, polynomial,
return-tail β_R ≈ 1.9, renewal-consistent) as evidence/guidance, and **(ii) a theory collaborator** to attempt the
renewal argument — consistent with the MEMORY pipeline-target verdict (pair the pipeline with a theory partner; do
not chase a broad-reach pure-math theorem solo).

---

## 7 · Consequence for θ = 1/2

`theta_half_repp_2026-06-14.md` grades θ = 1/2 as **(b) proved-modulo-a-named-limit-theorem**, with the named open
input being precisely the BCZ mixing rate (§8.4 there). **This note confirms and quantifies that bottleneck:**
- The deterministic content (period-2 cusp-swap ⇒ mean cluster size 2 ⇒ θ = 1/2) and the θ = 1/E[L] equality
  (rescued by the bounded δ₂ cluster law, outside the 1808.02970 failure mode) are unaffected — they remain
  unconditional / safe.
- The REPP convergence theorem needs the polynomial mixing rate. **Empirically that rate is C(n) ~ n^{−0.9}
  (polynomial, near-marginal), with the governing return-tail β_R ≈ 1.9.** A near-marginal β_C ≈ 0.9 < 1 is in the
  *slowly mixing / non-summable-correlations* regime — the technically hardest end for proving REPP limits (it may
  need the borderline-tower / log-correction machinery, or a normalization adapted to the slow rate).
- **Therefore θ = 1/2 stays (b): the deterministic skeleton is exact; the gap is the rigorous parabolic
  mixing-rate theorem, which this note shows is empirically polynomial-near-1/n and theoretically a major open
  problem — NOT reachable with the project's current (uniformly-expanding) tooling.**

---

## Files
- `code/bcz_mixing_rate.py` — numba BCZ map + correlation/return-time estimators + PM/Gauss/doubling controls.
- `code/bcz_mixing_driver.py` — control validation + BCZ C(n) (6 observables) + return-time tail (3 δ), q=4,5,7.
- `code/bcz_envelope.py` — period-2-oscillation-removed envelope decay-of-correlations fit.
- `code/out/bcz_mixing_results.json`, `code/out/bcz_envelope_results.json` — full numeric output.
- Cross-refs: `research_notes/theta_half_repp_2026-06-14.md` §8 (the θ=1/2 verdict this de-risks/quantifies);
  `research_notes/novelty_V1_theta_homdyn_2026-06-14.md` (prior-art landscape).
- Key external: arXiv:2403.14976 (BCZ weakly mixing, rate OPEN — the bottleneck), Gouëzel arXiv:1008.4113
  (operator renewal — the right but not off-the-shelf tool), Sarig Invent. 2002, Young Ann. Math. 1998/99.

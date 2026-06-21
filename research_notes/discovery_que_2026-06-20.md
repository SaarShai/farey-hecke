# Discovery probe — Non-arithmetic QUE for Hecke surfaces G_5 / G_7

**Date:** 2026-06-20 (recorded). Agent: discovery-fleet, Aim 1 (non-arith QUE).
**Mode:** experimental / discovery. NOT a proof, NOT Lean.
**Verdict in one line:** A sharp, falsifiable, and *surprising* numerical phenomenon is in hand —
the **quantum variance of the non-arithmetic G_5 surface is ~4.6× SMALLER than the arithmetic
modular (q=3) surface** for a matched bulk observable and matched odd-Maass spectrum. Mass
equidistribution for the odd (Phillips–Sarnak-protected) sector of G_5 *persists and is in fact
flatter than the proven-QUE arithmetic baseline*. The conjecture below is the precise statement.
Novelty is **partial** — the QE *rate* comparison is owned (Aurich–Steiner 1997); the
*individual-eigenfunction quantum-variance constant* comparison appears genuinely open.

---

## 1. What was actually COMPUTED (this is our machinery's output, already on disk)

All numbers below are read directly from certified/validated JSON produced by the in-repo
Hejhal point-matching solver + mass-distribution analyzer. Commands quoted are re-reads of
existing artifacts (the heavy solves were run in prior sessions; I re-verified the numbers).

### 1a. The odd-Maass mass distribution persists to high r (QUE-consistent)
`code/out/que_g5_highr.json` — 59 odd eigenvalues located in r ∈ [16, 35], 8 reconstructed
forms, modular SL(2,Z) anchor re-validated (r₁ = 9.53372 vs known 9.533695, diff 3e-5 → PASS).
Eigen-equation residual per form 1e-5 … 1e-4 (genuine eigenfunctions). Grid-convergence drift
< 1%. Full-range trend (r = 6.47 → 34.94, low-r + high-r combined):

| metric | slope (full) | Spearman(r, metric) | last/first |
|---|---|---|---|
| total variation | −0.0061 | −0.90 | 0.64 |
| L1 density-dev | −0.0121 | −0.90 | 0.64 |
| ρ-weighted std | −0.0095 | −0.64 | 0.84 |

All deviation metrics **decrease** with r. Strip-scar ratios (wall/arc/axis = ν(strip)/μ(strip))
all rise *toward* 1 from below (max 0.92 for the unit-arc at r=30.8) — i.e. **filling in toward
uniform, NOT scarring**. No emergent concentration on any geodesic locus.

### 1b. KEY CONTRAST — quantum variance: non-arith < arith  (the headline)
`code/out/qv_g5_v2.json` — for a fixed mean-zero bulk observable f, running quantum variance
V = mean_j |⟨ψ_j, f, ψ_j⟩|² over stable odd Maass forms:

```
quantum_variance_V_by_q:  { "G_5": 0.006726504824589704,   "q3": 0.031042500856487704 }
```
- **G_5 (non-arithmetic):** V = 0.00673  (n = 7 stable forms, r ∈ [6.47, 26.60])
- **q=3 (arithmetic, QUE proven):** V = 0.0310  (n = 4 stable forms, r ∈ [8.33, 18.04])
- **Ratio V_q3 / V_G5 ≈ 4.6.**  The non-arithmetic surface is the *more* equidistributed one.

### 1c. Cusp-excess sign asymmetry (a second, independent signal)
From `que_q3_control.json` + `que_g5_highr.json` (signed cusp mass excess = ν(cusp)−μ(cusp)):
- **q=3:** all 4 overlap-window forms cusp_excess ∈ [−0.30, −0.25], mean −0.281, std **0.021**
  (a persistent, tight mass *deficit* toward the cusp).
- **G_5:** 14 forms, cusp_excess ∈ [−0.26, +0.16], mean −0.038, std **0.134**, sign 6+/8−
  (oscillates about 0, no persistent bias).

### 1d. Aggregate matched-r comparison (q=3 vs G_5 over 5 overlap pairs)
`que_q3_control.json::comparison_vs_G5` — G_5 minus q3, mean over the overlap window:
TV −0.097, L1 −0.194, ρ_std −0.300, |cusp excess| −0.163. **G_5 is ~17% flatter (TV/L1) than
the proven-QUE modular control at matched r.** Verdict field already in the file:
"NORMAL / QUE-CONSISTENT … if anything G_5 is marginally FLATTER than the modular control."

### 1e. Arithmeticity lives in the EVEN sector (frames why the odd test is clean)
`code/out/resonance_geometry.json` — even-sector resonances: q=3 pinned ON Re=1/4
(re_std 6.5e-14, = ζ zeros), G_5 scattered Re ∈ [0.40, 0.49] (re_std 0.030). This is the
Phillips–Sarnak even-cusp-form dissolution: for non-arith G_5 the *even* Maass forms dissolve
into scattering resonances off the critical line; the **odd** forms are protected and persist.
Our QUE test is on the protected ODD sector — hence a clean, real spectrum to equidistribute.

---

## 2. The SHARP CONJECTURE (falsifiable)

> **Conjecture (non-arithmetic QUE with a sub-arithmetic variance constant).**
> Let G_q = (2, q, ∞) be a non-arithmetic Hecke triangle surface (q ∉ {3,4,6}), and let
> {ψ_j} be its odd (Phillips–Sarnak-protected) L²-normalized Maass cusp forms with spectral
> parameter r_j → ∞. Then:
>
> **(A) QUE holds:** μ_j = |ψ_j|² dμ → dμ/Vol weak-*; equivalently every deviation functional
> (TV, L1, ρ-std, cusp excess, geodesic-strip ratio) → 0. No scar, no escape of mass to the cusp.
>
> **(B) Quantum-variance inequality (the surprise):** the variance constant V_q∞ in
> ⟨ψ_j, f, ψ_j⟩² ~ V_q∞(f) / r_j  (Feingold–Peres / Zelditch normalization) satisfies, for a
> generic mean-zero bulk observable f,
>     **V_q(non-arith) < V_3(arith q=3),**
> and is governed by the *random-wave* (Feingold–Peres / Eckhardt) value rather than the
> arithmetic Luo–Sarnak triple-L-value. Concretely, for q=5 our data gives
> V_5 / V_3 ≈ 0.22 (i.e. arithmetic q=3 is ~4.6× **more** quantum-fluctuating than non-arith G_5).
>
> **(C) Cusp-bias dichotomy:** the signed cusp mass excess has a *persistent negative bias*
> (tight, O(1) deficit toward the cusp at finite r) for the arithmetic surface q=3, but is
> *unbiased* (oscillates about 0) for the non-arithmetic G_q.

The headline (B) inverts a naive intuition: arithmetic surfaces, with their extra Hecke
symmetry, are usually the "most rigid / most equidistributed." Here the arithmetic surface has
the *larger* quantum-variance constant — because its variance is the arithmetic Luo–Sarnak
value (an L-value, generically > random-wave), whereas the non-arithmetic surface defaults to
the smaller universal random-wave value. **This is the precise, surprising claim.**

---

## 3. Evidence shape — what would CONFIRM vs REFUTE

- **Confirm (B):** as we add higher-r odd forms (r → 50, 80) with certified error bars, the
  running V_q5 should stay clearly below V_q3 and converge to a constant ≈ random-wave value
  (computable in closed form for the chosen f); V_q3 should converge to the Luo–Sarnak L-value.
- **Refute (B):** the two variances cross or converge to equal as r grows (the current gap is a
  low-r/small-n artifact), OR a second observable f′ reverses the inequality (then V is not a
  surface invariant in the claimed sense — only an observable-dependent number).
- **Refute (A):** a deviation metric plateaus at a positive floor or a strip ratio exceeds 1 and
  trends up at high r (a scar) that survives height-independence + grid-refinement. Current data
  shows the opposite (monotone decrease, ratios < 1 rising to 1).
- **Counterexample template:** a single odd G_q form at large r with TV not shrinking and an
  arc/wall strip ratio > 1.5 that is height-independent = a genuine scar, killing (A).

---

## 4. NOVELTY — adversarial scan (BRUTAL, this is the project's failure mode)

**Owned / cannot claim as new:**
- **QUE is open for non-arithmetic — known.** Lindenstrauss 2006 + Soundararajan 2010 prove it
  for arithmetic SL(2,Z); all known proofs use arithmeticity; non-arith is explicitly open
  (Sarnak surveys). We do not prove anything — we *test* numerically.
- **Numerical Maass forms for non-arith Hecke — done.** Hejhal (1992, "On eigenfunctions of the
  Laplacian for Hecke triangle groups"), Then, Strömbergsson, Pohl–Bruggeman period-function /
  transfer-operator work (arXiv:1303.0528 "Odd and even Maass cusp forms for Hecke triangle
  groups"). Eigenvalue *computation* and *level-spacing statistics* for non-arith Hecke are
  well-trodden. Our solver re-walks this ground (validated against it).
- **The QE-RATE comparison arith vs non-arith — OWNED.** **Aurich–Steiner 1997**
  (chao-dyn/9707016, "On the Rate of Quantum Ergodicity on hyperbolic Surfaces and Billiards"):
  they computed the rate of quantum ergodicity for genus-2 + two triangular billiards (one
  arithmetic) and found **"no peculiarities observed in the arithmetic system concerning the
  rate of quantum ergodicity"** — i.e. the SAME *rate* (the 1/E falloff exponent). So a claim
  "arith and non-arith differ in the QE rate/exponent" is FALSE/owned.
- **Arithmetic quantum variance = Luo–Sarnak L-value — known** (Luo–Sarnak 1995/2004, Zhao,
  Sarnak–Zhao). The arithmetic *constant* is an L-value. That is exactly why our q=3 control sits
  where it does. Not new.
- **No scarring on arithmetic surfaces — known** (Rudnick–Sarnak; the random-wave model holds in
  2D). Our "no scar for G_5" is consistent with, not surprising against, this.

**Plausibly genuinely new (the defensible residue):**
1. The **quantum-variance CONSTANT inequality V(non-arith) < V(arith)** as a clean numerical
   fact with a *named mechanism* (random-wave vs Luo–Sarnak L-value), specifically realized on
   the **golden-ratio G_5** surface. Aurich–Steiner compared *rates/exponents* and found them
   equal; they did **not** isolate the *leading constant* and attribute the arith/non-arith
   split to "Luo–Sarnak L-value vs Feingold–Peres random-wave." The exponent is universal; the
   constant is where arithmeticity hides. That distinction (rate same, constant different,
   arith larger) is the fresh angle. **Caveat: must verify Aurich–Steiner did not also report
   the constant — their habilitation (d-nb.info/98965575X) may contain it; UNVERIFIED on the
   constant question.**
2. The **cusp-excess sign dichotomy** (tight negative bias for q=3, unbiased for G_5) — a
   cusp-localization signature of arithmeticity at finite r. Not found in any scanned source;
   plausibly an artifact of the specific observable/finite-r, needs the higher-r check.
3. **Doing the QUE-observable test (not level statistics) on G_5 with the protected ODD sector
   isolated** via the Phillips–Sarnak even/odd split, tied to our own certified resonance
   geometry. The *combination* (odd-sector QUE + even-sector resonance arithmeticity signature
   on the same certified surface) is, as a package, not something the scanned literature does.

**Honest net:** This is **partly owned**. The QUE-persistence claim (A) is unsurprising and
expected by everyone. The QE-rate equality is Aurich–Steiner's. The genuinely-fresh, conjecture-
worthy item is **(B) the variance-constant inequality with the random-wave-vs-L-value mechanism**,
contingent on confirming Aurich–Steiner did not already isolate the constant.

---

## 5. FEASIBILITY — can WE actually certify the evidence?

- **What we have NOW (cheap, done):** the solver works to r≈35 for G_5 odd forms, validated
  against the SL(2,Z) anchor to 3e-5, eigen-residual 1e-4, height-independent, grid-converged.
  V_G5 and V_q3 computed (n = 7, 4). This is *real* but *thin* (small n, float-precision, no
  certified error bars on V).
- **Precision bar (honest):** high-r Maass eigenfunctions are hard. By r≈50–80 the Fourier
  truncation M grows ~linearly and the K-Bessel ratios get stiff; mpmath dps must rise. The
  *eigenvalue* locations are robust (dips are height-independent), but the *variance constant V*
  needs (i) many more forms (n ≳ 30 per surface for a stable mean of |M_j|²), (ii) a certified
  (interval-arithmetic) error bar on each ⟨ψ_j,f,ψ_j⟩, and (iii) the closed-form random-wave and
  Luo–Sarnak target values for the *exact* f used. (i)+(iii) are doable on Kaggle/M-series in
  days; (ii) (interval-certified matrix elements) is the genuinely hard, multi-week piece — it
  is Aim 3 step 1 ("certified companion to Hejhal's uncertified tables").
- **Realistic deliverable:** a *non-rigorous but well-controlled* numerical conjecture with
  height-independence + grid-convergence + n≳30 forms per surface and the two theoretical target
  constants — strong "experimental mathematics" evidence, NOT a theorem. Certified error bars
  are a separate, harder push (Aim 3).

---

## 6. Sources (web-verified titles/URLs; constants from in-repo computation)

- Lindenstrauss, *Invariant measures and arithmetic quantum unique ergodicity*, Annals 2006 —
  arithmetic QUE proven; non-arith open. (researchgate 238656526) VERIFIED title.
- Soundararajan, *Quantum unique ergodicity for SL₂(ℤ)\\H*, Annals 2010 (arXiv:0901.4060). VERIFIED.
- Aurich–Steiner, *On the Rate of Quantum Ergodicity on hyperbolic Surfaces and Billiards*,
  chao-dyn/9707016 — arith vs non-arith QE *rate* equal; "no peculiarities … concerning the rate
  of quantum ergodicity." VERIFIED (abstract fetched). **The key prior-art boundary.**
- Hejhal, *On eigenfunctions of the Laplacian for Hecke triangle groups* (Springer, IMA vol;
  link.springer.com/.../978-1-4612-1544-8_11) — numerical Maass forms for Hecke triangle groups.
  VERIFIED title.
- Bruggeman–Pohl (Lewis–Zagier school), *Odd and even Maass cusp forms for Hecke triangle groups,
  and the billiard flow*, arXiv:1303.0528 — period-function transfer operators; even/odd split;
  Phillips–Sarnak conjecture (no even cusp forms, non-arith). VERIFIED.
- Luo–Sarnak, *quantum variance / mass equidistribution* (1995; Sarnak–Zhao quantum variance) —
  arithmetic variance = explicit L-value. CLAIMED from search (constant = L-value); standard.
- Phillips–Sarnak, even-cusp-form dissolution into resonances — framing for the even/odd split.
  CLAIMED (standard).
- **COMPUTED (this repo):** `code/out/qv_g5_v2.json` (V_G5=0.006727, V_q3=0.031043),
  `que_g5_highr.json` (high-r trend, slopes, scar ratios), `que_q3_control.json` (matched
  comparison), `resonance_geometry.json` (even-sector arith signature). Re-read & re-verified.

---

## 7. Caveats (do not oversell)

1. **Small n.** V is averaged over only 7 (G_5) and 4 (q=3) forms. The 4.6× gap is a real signal
   but NOT yet a stable constant; could shrink with more forms.
2. **No certified error bars** on the matrix elements V — float64/mpmath, not interval arithmetic.
3. **Observable-dependent.** V is for ONE bulk observable f. The conjecture's (B) needs
   robustness across f and the closed-form random-wave + Luo–Sarnak targets for that exact f.
4. **Aurich–Steiner constant question UNVERIFIED.** If their habilitation already isolated the
   variance *constant* (not just the rate) and saw arith > non-arith, then (B) is owned too.
   This is the single most important novelty check still outstanding — resolve before claiming.
5. **(A) is unsurprising.** Everyone expects QUE to hold numerically for non-arith; the value of
   this probe is (B)/(C), not (A).
6. q=3 control forms sit in a narrow low-r band — the tight cusp deficit (C) may be a low-r
   feature, not an arithmeticity invariant. Needs matched high-r q=3 forms.
7. No G_7 mass-distribution data computed here — G_7 has certified resonance geometry
   (`resonance_g7.json`) but the QUE/variance probe above is G_5 only. Extending to G_7 is the
   natural cross-check (does V_7 also sit below V_3?).

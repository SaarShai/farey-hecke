# Twin-index hyperuniformity — the spatial-rigidity face of the HL twin singular series (2026-06-14)

**One-line verdict.** The twin-index point set is **NOT hyperuniform**: in the
project's own structure-factor / number-variance vocabulary it is **Poisson-class**
(small-q exponent α ≈ 0, σ²(R) ~ R) at large scale, with only a *finite-range*
sub-Poisson granularity inherited from the punctured-residue (coprimality)
structure. It is therefore in a **different, weaker class than the prime-Farey
critical hyperuniformity** S(k)~k^1.8 (which is strongly suppressed, α≈1.8). This
note is the spatial-rigidity rendering of the Hardy–Littlewood twin singular
series in HU language — a **presentation/bridge, not a twin-primes advance**, and
the large-scale Poisson behaviour is itself essentially the well-known
Gallagher/Cramér statistics for prime constellations. Twin primes itself stays
unreachable (parity bottleneck of the circle method); do **not** attempt a proof.

Code: `code/twin_index_hyperuniform.py` (reuses the validated estimators in
`code/hyperuniform_farey.py`). Large-N run on M1 (`/tmp/twin_big.py`).

---

## 1. Setup and the punctured-circle reformulation

Every twin pair (p, p+2) with p>3 has p ≡ 5 (mod 6), p+2 ≡ 1 (mod 6), so the
**midpoint** mid = p+1 = 6k is a multiple of 6. Define the **twin index**

    K = { k = (p+1)/6 : (p, p+2) both prime, p > 3 } ⊂ ℤ_{>0}.

**Punctured circles.** On ℤ/rℤ for any prime r, both p = mid−1 and p+2 = mid+1
must be coprime to r, i.e.

    mid ≢ +1 (mod r)   and   mid ≢ −1 (mod r).

So **exactly two residue classes are forbidden** for the midpoint (and hence two
for the index k, at 6⁻¹·1 and 6⁻¹·(r−1) mod r). Survival = (r−2)/r. Verified
directly (`/tmp/punct.py`) at r = 5,7,11,101,1009: the forbidden classes are
exactly {6⁻¹, 6⁻¹(r−1)} mod r.

- **Asymptotic 2-puncture, with O(1) boundary correction.** For "generic" moduli
  (e.g. r=1009) *both* forbidden classes are empty → exactly 2 empty, survival
  1007/1009 = 0.99802 = (r−2)/r exactly. For small/special r one forbidden class
  still receives a **single** hit: the twin pair where the modulus *itself* is a
  member. Confirmed: at r=101 the count-1 outlier in class 17 is exactly the pair
  (101,103), since k ≡ 17 ⇒ mid ≡ 1 ⇒ 101 | (mid−1) = p ⇒ p = 101. This is an
  O(1) edge effect; the survival law (r−2)/r holds asymptotically.

- **Relative product → 2C₂.** The per-prime survival factors combine into the
  Hardy–Littlewood twin singular series:
  `2·∏_{p>2} p(p−2)/(p−1)² = 1.32032367` (p < 2·10⁶) vs `2C₂ = 1.32032363`,
  relative error **3.2·10⁻⁸** (`/tmp/check2c2.py`). This is the standard HL twin
  constant; it is the local-density depletion seen on each residue circle.

**Sub-Poisson within surviving classes (finite-range).** Per-circle occupancy is
*under*-dispersed vs a multinomial null, **after detrending** the trivial twin
density decay (twins thin out ⇒ raw across-class variance is drift-inflated).
Detrended dispersion E[z²] (1 = multinomial/Poisson; <1 = sub-Poisson):

| r     | empty classes | survival   | (r−2)/r    | detrended E[z²] |
|-------|---------------|------------|------------|-----------------|
| 101   | 1 (+1 single) | 0.9901     | 0.9802     | 0.93 (1e7) / boundary-noisy (2e8) |
| 1009  | 2             | 0.99802    | 0.99802    | **0.86 / 0.82** |
| 10007 | 1 (+1 single) | 0.99990    | 0.99980    | **0.88**        |

The robust signal (r = 1009, 10007) is genuine under-dispersion E[z²] ≈ 0.82–0.88.
**But this is a fixed-range residue effect, not large-scale hyperuniformity** — it
is exactly the discreteness floor that any coprimality-sieved integer set carries.

---

## 2. Estimator control validation (reused, re-verified this session)

The estimators are the *validated* ones from `code/hyperuniform_farey.py`
(number_variance, structure_factor, fit_powerlaw). Because the twin-index set is
**non-stationary** (density ~ 1/(ln x)², drops 2.47× across [0, 2·10⁸]), the
estimators are applied **block-wise**: split into contiguous blocks of ~constant
density, rescale each to unit density, average S(q) and σ²(R). The blockwise
pipeline was re-validated on controls (`run_controls`, this session):

| control            | σ²(R) slope | S(q) exponent α | expected            |
|--------------------|-------------|-----------------|---------------------|
| Poisson            | **0.99**    | **−0.11 (≈0)**  | slope 1, α≈0  ✓     |
| Lattice (perfect)  | **0.00**    | −1.6            | bounded σ², α<0 ✓   |
| Lattice+jitter0.3  | **0.00**    | −0.31           | bounded σ² (HU) ✓   |

(Single-realization S(q) is noisy at ±0.15 in α; this is why the Poisson α reads
−0.11 not exactly 0. Averaging 40 Poisson realizations gives α = −0.03 — the
estimator is unbiased; `/tmp/diag.py`.) σ²-slope is the sharper discriminant and
is exact: Poisson 0.99, lattices 0.00.

---

## 3. Hyperuniformity result for the twin-index set

Two sample sizes (local sieve; M1 for the large one):

| bound (p+2 ≤) | N twins | block | **α (S(q)→q^α)** | **σ²(R) slope** | σ²/R (small R) |
|---------------|---------|-------|------------------|-----------------|----------------|
| 10⁷           | 58,979  | 8000  | +0.08            | 1.09            | 1.6            |
| 2·10⁸         | 813,370 | 8000  | **+0.002**       | **0.97**        | 1.60           |
| 2·10⁸         | 813,370 | 16000 | **+0.015**       | **0.98**        | 1.62           |

**Reading.** α ≈ 0 and σ²(R) ~ R: the rescaled twin-index set is **Poisson-class**,
i.e. **NOT hyperuniform**. (Hyperuniform would require α > 0 with S(q)→0, and
σ²(R) growing *slower* than R. Neither holds.) The σ²/R ≈ 1.6 > 1 at the smallest
R is a mild *excess* (slight short-range clustering from the integer/sieve
granularity), not suppression. The naive global σ²(R) without block-detrending
gives a spurious slope 1.64 (>1, "super-Poisson") — that is purely the
**non-stationarity artifact** of the 1/(ln x)² density drift, NOT a real
anti-rigidity; flagged explicitly in the code's section (2).

**Singular-series prediction is consistent.** The HL constellation heuristic says
twins behave like an inhomogeneous Poisson process with intensity
2C₂/(ln x)² — i.e. Poisson statistics (α = 0) modulated by a smooth density. The
measured α ≈ 0, σ² ~ R is exactly that. There is **no** additional long-range
spectral suppression beyond the singular series.

---

## 4. Comparison to the prime-Farey S(k) ~ k^1.8

| object                         | small-q exponent α | class                         |
|--------------------------------|--------------------|-------------------------------|
| Rescaled Farey (prior result)  | **1.8–1.9**        | critically/strongly HU (class I-ish) |
| Twin-index set (this note)     | **≈ 0**            | Poisson-class, NOT HU         |

**Verdict: DIFFERENT class.** The prime-Farey set is strongly suppressed
(α≈1.8) because Stern–Brocot neighbour gaps are **anticorrelated** (consecutive
Farey gaps are negatively correlated via the mediant law) — a structural rigidity.
The twin-index set has **no analogous gap anticorrelation**: twin gaps are, to
leading order, those of an i.i.d. (renewal) point process with a 1/(ln x)²
intensity, so S(q) stays flat (α≈0). They are **not the same phenomenon** — the
twin set lacks the deterministic neighbour-recurrence that makes Farey rigid.

So of the three options posed: **(ii) a different exponent** (α≈0 vs 1.8), and
specifically a strictly weaker class — Poisson, not hyperuniform.

---

## 5. Honest novelty verdict vs Torquato et al.

- **Torquato, Zhang, Torquato (arXiv:1801.01541)**: the prime numbers themselves
  in a finite window have an *effective hyperuniform-like / quasi-periodic*
  structure factor with Bragg-like peaks governed by the prime constellations
  (the singular series shows up as the peak heights). They explicitly tie the
  diffraction pattern to the Hardy–Littlewood densities.
- **(arXiv:1804.06279, 1802.10498)**: Riemann ζ zeros and related arithmetic
  point processes — "effectively limit-periodic" / hyperuniform-of-class-analyses.

**What is genuinely NEW here: essentially nothing at the level of physics.** The
primes-on-a-circle / prime-constellation diffraction picture is **published**
(Torquato et al.), and the appearance of the HL singular series as the local
depletion factor is the *content* of that work. Our "punctured circle, survival
(r−2)/r, product = 2C₂" is a clean **re-derivation/reframing** of the twin
singular series — true and tidy, but classical (Hardy–Littlewood 1923; the local
factors are textbook).

**The one mildly fresh framing** (a presentation point, not a theorem):
expressing twins via the **index k = mid/6** makes the 2-puncture-per-circle and
survival (r−2)/r maximally transparent, and stating the *negative* HU result
crisply — "the twin-index set is **Poisson-class (α≈0), strictly weaker than the
prime-Farey critical class (α≈1.8)**; the only suppression is the finite-range
residue floor and the smooth singular-series density, with no long-range spectral
rigidity." That negative + the side-by-side with the project's own Farey result is
the deliverable. It is a **bridge note**, value identical to the wide-appeal
verdict's framing: mathematical/expository, modest, not a breakthrough.

---

## 6. Scope (ruthless)

- **Bridge, not breakthrough.** This renders the HL twin singular series in the
  project's HU vocabulary and benchmarks it against prime-Farey. No new theorem.
- **Twin primes itself: unreachable.** The circle-method major-arc side gives the
  singular series (what we measured spatially); the minor-arc / parity bottleneck
  blocks an asymptotic lower bound. Do **not** attempt a twin-primes proof here.
- **The sub-Poisson signal is finite-range**, from coprimality sieving, and does
  **not** lift to large-scale hyperuniformity (α≈0 confirmed at N=8·10⁵).
- Honest comparison to Torquato: the diffraction-of-primes / singular-series story
  is published; our contribution is the index reframing and the explicit
  negative-HU classification, both expository.

---

## Reproduce

```
python3 code/twin_index_hyperuniform.py 1e7          # local sieve, full report
# large N (M1):  scp /tmp/twin_big.py new@192.168.1.22:/tmp && ssh ... python3 /tmp/twin_big.py
```

Key numbers (verify-before-completion):
- Controls (blockwise): Poisson α=−0.11, σ²-slope=0.99; jitter-lattice σ²-slope=0.00.
  (40-rep Poisson α=−0.03.)
- Twin-index (N=813,370): **α = +0.002 … +0.015**, **σ²(R) slope = 0.97–0.98**.
- Survival product 2∏p(p−2)/(p−1)² = 1.32032367 vs 2C₂ = 1.32032363 (err 3·10⁻⁸).
- Detrended punctured-circle dispersion E[z²] = 0.82 (r=1009), 0.88 (r=10007) — sub-Poisson, finite-range.

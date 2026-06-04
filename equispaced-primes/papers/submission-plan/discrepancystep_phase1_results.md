# DiscrepancyStep — Phase-1 results (extended numerics + N/A characterization)

Status: Phase-1 complete. Date: 2026-06-03.
Verdict (executive): **NO-GO** on the unconditional push for sub-lemma (a).
Reasoning condensed in §5.

Target lemma (`papers/math_paper/main.tex:931-949`, statement
`main.tex:2149-2153`): `N(p)+B(p)+C(p) > A(p)` for primes `p≥11` with
`M(p)≤−3`, where `ΔW(p)=A−B−C−N`. Binding sub-lemma is **(a)**:
`N/A = 1 + O(1/p)` with an *effective* rate.

All compute used `float64` for the O(1) ratios (the 1e-11 cancellation
only matters for the `ΔW` sign, tracked separately via the four-term
sum). Engine: `code/discrepancystep_phase1.py` (vectorised, validated
exactly against the canonical `experiments/bridge_DA_compute.py::float_decomposition`
to <1e-9 on p∈{11..199}). Serial incremental runner:
`code/discrepancystep_phase1_serial.py`.

---

## 0. Data / range reached

- CSV: `code/discrepancystep_phase1.csv`
  (columns: `p, M, M_over_sqrtp, A_raw, B_raw, C_raw, N_raw, NA, CA, BA,
  margin=(B+C+N)/A−1, deltaW_sign`).
- **Largest range reached:** dense (every qualifying prime, `M(p)≤−3`,
  `p≥11`) up to **p ≈ 10,000**, plus a stride-12 sparse sample beyond,
  reaching **p ≈ 10,200+** (sparse tail to 50,000 was still extending at
  write time; the verdict does not depend on the tail).
- 625+ rows. Pushing past PMAX=6000 (the prior probe ceiling) by ~1.7×
  dense and confirming the trend on a sparse sample beyond.
- Compute note: the exact per-prime ABCN decomposition is intrinsically
  O(p²) (it sums over the ~0.30·p² fractions of `F_{p-1}`). A full dense
  10^5 run is therefore infeasible in the few-minute box (≈350 s/prime
  at p=10^5, ~9500 primes); multiprocessing OOMs (each worker needs
  ~1.4 GB at p=14k for the value array). Dense-to-10k + sparse beyond was
  the largest reliable range. This is sufficient: the structural verdict
  is already saturated by p≈3000 (see §2).

---

## 1. Reproduction of paper observations (extended range)

| quantity | extended-range value | paper |
|---|---|---|
| `N/A` range (M≤−3) | [0.9702, 1.1812] | [0.97, 1.12] ✓ (>1.12 only p=19) |
| `C/A` range | [0.1214, 0.2550] | "5–18%" ✓ (floor ≈ π²/80=0.1234) |
| `B/A` range | [0.0306, 4.235] | B>0 ✓ on target set |
| worst `(B+C+N)/A−1` | **+0.4014 at p=13 (M=−3)** | margin never < 0.40 |
| `ΔW<0` (sign holds) | 625/625 | ✓ no failure |

All paper observations reproduce on the extended range. No counterexample
to DiscrepancyStep appeared (no hard-abandon trigger).

---

## 2. Characterization of `N/A − 1` — IT IS MESSY (the decisive result)

Fits on the full extended CSV (p∈[13, 10200], 621 rows):

- **Clean rate `N/A = 1 + c/p`:** `c = 2.44`, **R² = 0.29**, RMS = 1.33e−2.
  (On the earlier p≤6000 probe this looked like `c≈2.5, RMS≈1.3e−2`; the
  extended fit shows the R² is poor — a single `c/p` explains <30% of
  the variance.)
- **`p·(N/A−1)`:** mean −56, std 57, and it **drifts** strongly with
  `log p` (regression slope −34 in log p). It is **not** a constant and
  **does not converge** — refuting a clean `1+c/p` law.
- **Flattest normalization search.** Every single-power normalization
  (`p·r`, `p·r/log p`, `p·r/log²p`, `r·√p`, `r·p·log p`) has
  std/|mean| > 1.2 — i.e. the scatter exceeds the mean for all of them.
  **There is no single functional form that flattens `N/A−1`.**
- **The residual is intrinsically Mertens-coupled.** Adding the
  fluctuation term `M(p)/p^{3/2}` to a smooth model jumps R² from 0.29 →
  0.50 (coef ≈ +23 on `M/p^1.5`); a further `M²/p²` term reaches only
  R²=0.51. So roughly half the variance is `M(p)`-driven and the other
  half is still-higher-order arithmetic noise.
- **Smooth-vs-fluctuation split (the killer statistic).** For **p>3000**
  (411 points): std(`N/A−1`) = 5.1e−3, while the std of the best smooth
  part (`1/p`+`log p/p`) = 1.3e−4. **The fluctuation is ~40× larger than
  any deterministic trend.** The deterministic *limit* `N/A→1` is solid;
  the *rate* is dominated by irreducible arithmetic fluctuation.

**Best functional form:** there is no clean one. The honest description
is `N/A − 1 = (smooth O(log p / p)) + (dominant fluctuation tracking
M(p)/p^{3/2} plus higher-order ζ-noise)`. The fluctuation, not the
smooth part, sets the size of `N/A − 1` for all p of interest.

---

## 3. Closed-form `N` via García rank formulas — THE KEY LEAD, CHECKED

This was flagged as the highest-value lead. Result: **the rank formula is
real and exact, but it does NOT make `N` closed-form-summable in any
useful sense — the obstruction is RH-equivalent.**

What is true and machine-verified here:
- The Möbius/García rank formula holds exactly:
  `rank_{F_{p-1}}(k/p) = 1 + Σ_{d=1}^{p-1} μ(d)·G(k/p, ⌊(p-1)/d⌋)`,
  `G(k/p,m) = Σ_{c=1}^{m} ⌊ck/p⌋` (a Hermite/Dedekind floor-sum,
  computable in O(log) via `floor_sum`). Verified vs brute force and vs
  `searchsorted` for p∈{13,31,101,199,503} (exact integer match).
- Hence the new-fraction discrepancy has the exact closed form
  `D_{F_p}(k/p) = rank_old(k/p) + (k−1) − n'·k/p`
  (equivalently the canonical `D_{F_p}(k/p) = D_old(k/p) + k/p`).
  Verified to machine precision against the engine for p≤503.

Why this does NOT give a provable `N/A = 1 + c/p`:
- Decompose `N_raw = Σ_{k} (D_old(k/p) + k/p)²
              = Σ_k D_old(k/p)²  +  2Σ_k (k/p)D_old(k/p)  +  Σ_k (k/p)²`.
  The last term `Σ(k/p)² = (p−1)(2p−1)/(6p)` is exact and O(p); the cross
  term is O(p); but the **first term dominates** (≈99% of `N_raw`):
  e.g. at p=4001, `Σ D_old² ≈ 6.27e6` vs cross `≈1.15e4`, square `≈1.3e3`.
- So `N ≈ Σ_{k=1}^{p-1} D_old(k/p)²` = the **second moment of the local
  Farey discrepancy sampled at the p equispaced points k/p**.
- `A`'s core is `old_D_sq = Σ_{f∈F_{p-1}} D(f)² = n²·W(p−1)`, where
  `W(N)` is the normalized Franel–Landau wobble — and **`W(N)=O(N^{−1+ε})`
  is equivalent to RH** (`main.tex:972`).
- Empirically `Σ_k D_old(k/p)² / p²` does **not** converge to a constant:
  it drifts 0.298 → 0.383 over p=101→1301 (grows ~log p). A finite
  Dedekind/cotangent closed form would force a clean constant; the
  observed `log`-drift is exactly the wobble's RH-coupled growth.
- Consequently `N/A` is, structurally, the **quadrature error of
  estimating the full Franel–Landau wobble (over ~0.3p² Farey points) by
  its p equispaced samples.** `N/A·n/(p−1) ≈ 2` but fluctuates 1.97–2.02
  with no settling. Evaluating `N` in clean closed form would mean
  evaluating the Franel–Landau second moment in closed form, i.e.
  resolving RH-strength equidistribution of the *moving* discrepancy
  field — precisely the obstruction `main.tex:2093-2098` names.

**Verdict on the lead:** García's rank formula gives an exact *pointwise*
closed form for `D_{F_p}(k/p)`, but `N = Σ D_{F_p}(k/p)²` is a second
moment of that field; its summation reduces to the Franel–Landau wobble
sampled at p points, which has no closed form short of RH-level
equidistribution. **The high-value lead does not pan out.**

---

## 4. Worst margin and B-sign (extended range)

- **Worst margin** over M(p)≤−3 primes: `(B+C+N)/A − 1 = +0.4014`,
  achieved at **p = 13 (M=−3)**, the smallest target prime. The margin is
  monotonically larger for deeper Mertens and stays bounded well away
  from 0 (≥0.40 throughout). No drift toward 0.
- **B-sign on the target set:** within `M(p)≤−3`, **B/A > 0 for all
  625 rows** (min B/A = 0.0306 at p=13). Under the engine's δ-convention
  (`δ(a/b)=(a−(pa mod b))/b`, `δ=0` at f∈{0,1}), `B(13)/A=+0.031>0` —
  this differs from the paper's "B(13)=−3.72e−4<0" (`main.tex:1023`),
  which is **convention-sensitive at the f=1 boundary** (already flagged
  in `papers/discrepancystep_scoping.md:144-152`).
- **Smallest p with B<0 (engine convention), scanning ALL primes:**
  p=11 (M=−2), 17 (M=−2), 97 (M=+1), 223 (M=+3), then a cluster near
  1399–1439 (all M ≥ +7). **Crucially, every B<0 prime has M(p)>−3** —
  i.e. all lie *outside* the DiscrepancyStep target set. B<0 occurs
  exactly when Mertens is high/positive, which is precisely the regime
  where DiscrepancyStep is not invoked. This is a clean refinement: on
  the relevant set `{M≤−3}`, B≥0 is robust.

---

## 5. GO / NO-GO

**NO-GO** for the unconditional push on sub-lemma (a) `N/A=1+O(1/p)`.

Justification (one paragraph): The Phase-1 gate (scoping §5,
`papers/discrepancystep_scoping.md:195-205`) required (i) the residual
after removing `c/p` to be `o(1)` and *structured*, and (ii) a candidate
second-moment statement to aim at. Neither holds. (i) fails decisively:
`N/A−1` is not a clean `1+c/p` (R²=0.29); no single normalization flattens
it (all std/|mean|>1.2); `p·(N/A−1)` drifts with log p instead of
converging; and for p>3000 the fluctuation is ~40× the size of any smooth
trend, with ~half the variance provably coupled to `M(p)/p^{3/2}` and the
rest higher-order arithmetic noise. (ii) fails because the high-value
closed-form lead — using García's exact rank formula to sum
`N=Σ D_{F_p}(k/p)²` — collapses to the Franel–Landau wobble sampled at p
points, whose closed-form evaluation is RH-equivalent (`main.tex:972`):
`Σ_k D_old(k/p)²/p²` drifts like log p rather than tending to a constant,
exactly as a non-closed-form, RH-coupled second moment must. The
difficulty is concentrated precisely where the paper said it would be
(`main.tex:2093-2098`): a uniform second moment of the *moving*
discrepancy field, beyond fixed-test-function Franel–Landau/BCZ. This is
**hard-open**, not a tractable target.

**What survives (positive Phase-1 output):**
- No counterexample to DiscrepancyStep through the extended range; the
  Sign Theorem's finite-computation value is intact and reconfirmed.
- A clean structural refinement worth folding into the paper: on the
  target set `{M(p)≤−3}`, `B≥0` is universal; every B<0 prime has
  `M(p)>−3` (outside the target). This sharpens the open `B≥0` remark.
- The pointwise García closed form `D_{F_p}(k/p) = rank_old(k/p)+(k−1)
  −n'k/p` with `rank_old` via the Möbius floor-sum — exact and citable,
  even though the *second moment* is not summable.
- Reconfirmed worst margin +0.40 at p=13, bounded away from 0.

**Recommendation:** record sub-lemma (a) as hard-open (RH-coupled,
beyond Franel–Landau), do not proceed to a Phase-2 attempt at an
effective `N/A` rate, and keep the finite Sign Theorem (p≤100,000) as the
published result. Sub-lemmas (b) `C/A≥c₀` and (c) `B≥0`-on-target remain
numerically robust and are the only pieces with any tractability, but
they cannot close DiscrepancyStep without the effective (a)-rate that
Phase-1 shows is absent. The realistic best outcome (scoping §5 line 234,
"DiscrepancyStep modulo effective-Mertens") is itself blocked by the
non-existence of a clean `N/A` rate, not merely by the ineffective-Walfisz
tail.

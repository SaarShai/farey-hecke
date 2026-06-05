# DPAC — certified numerical avoidance evidence (re-derived 2026-05-16)

Companion: `DPAC_OBSTRUCTION_NOTE.md` (why general-K is LI-class).
Harness: `dpac_certified_numerics.py` (reproducible, seeded).
Data: `dpac_certified_result.json`, `dpac_doublecheck_result.json`.
Tier: **conjecture-with-evidence**. No proof, no RH/LI claim.

---

## 1. What is certified vs not [scope, stated plainly]

`c_K(s) = Σ_{k=2}^{K} μ(k) k^{-s}`. DPAC(K): `c_K(ρ) ≠ 0` at every
nontrivial ζ-zero. Unconditional `K ≤ 4`; open & LI-class for `K ≥ 5`.

- **Rigorous part:** `c_K` is evaluated with mpmath **interval arithmetic**
  (outward-rounded `+,−,×,exp,log,sin,cos`) over the box
  `B_n = [½−δ, ½+δ] × [γ_n−ε, γ_n+ε]`. If the resulting complex interval
  excludes the origin, then `c_K(s) ≠ 0` for **every** `s ∈ B_n` — a
  rigorous statement. Certified lower bound `= max(dist(0,Re iv),
  dist(0,Im iv))` (since `|c_K| ≥ |Re|, |Im|`).
- **Not a formal certificate:** `γ_n` comes from `mpmath.zetazero(n)` at
  50–70 digit precision (standard high-precision computation). `ε` is set
  `10^{22}–10^{44}×` larger than its numerical error, and the box is
  RH-free in `Re` (covers a neighbourhood of ½). So the conclusion
  "`c_K ≠ 0` at the true n-th nontrivial ζ-zero" holds **conditional only
  on the standard correctness of `zetazero(n)`**. Sanity: residual
  `max|ζ(½+iγ_n)| = 5.2e-48` (main), `9.9e-69` (stressed) — ordinates are
  genuine ζ-zeros to that many digits.
- This is finite-height evidence only. It says **nothing** about general
  `K` (see obstruction note); it cannot and does not approach a proof.

## 2. Main certified run [NUMERICAL, rigorous in c_K]

`--zeros 500 --kset 2,3,5,6,7,10,20,50,100,200,500,1000 --prec 50
--ivdps 40 --eps-ord-exp 25 --delta-re-exp 9 --control-random 400
--seed 20260516`. 500 nontrivial ζ-zeros (γ₁≈14.13 … γ₅₀₀≈811.18),
extends well beyond the prior "first 100"; K up to 1000, beyond prior
{10,20,50}. **6000 (K, zero) interval certifications; 0 failures.**

| K | uncond | min certified \|c_K\| lower bound | min \|c_K(ρ)\| over 500 zeros | median |
|---|---|---|---|---|
| 2 | yes | 0.500599 | 0.707107 | 0.707107 |
| 3 | yes | 0.093644 | 0.129763 | 0.906317 |
| 5 | no (first open) | 0.0391155 | 0.0391776 | 0.893731 |
| 6 | no | 0.0441741 | 0.055691 | 1.03337 |
| 7 | no | 0.0236965 | 0.0238286 | 1.06141 |
| 10 | no | 0.085095 | 0.0943305 | 1.09071 |
| 20 | no | 0.0386258 | 0.0430779 | 1.22163 |
| 50 | no | 0.0387183 | 0.0454309 | 1.32499 |
| 100 | no | 0.0844553 | 0.101739 | 1.5071 |
| 200 | no | 0.0151686 | 0.0175352 | 1.61164 |
| 500 | no | 0.0435611 | 0.0599504 | 1.91979 |
| 1000 | no | 0.109168 | 0.133366 | 2.21015 |

- All certified lower bounds `> 0` and `≳ 0.015`, i.e. `~23` orders above
  the interval resolution — unambiguous, not borderline.
- **Closest approach in the whole grid:** `K=200`,
  `min|c_200(ρ)| ≈ 0.01754` (cert. lb `0.01517`). Some ζ-zeros bring `c_K`
  to `~10^{-2}`; none coincide; nothing closer than that over 500 zeros.
- `K=2`: `|c_2|=2^{-½}=0.70711` exactly (single term), constant — sanity ✓.

## 3. Double-check [independent corroboration]

Stressed re-run, `--zeros 150 --prec 70 --ivdps 60 --eps-ord-exp 24
--delta-re-exp 8 --seed 777` (boxes **10× wider** in both axes — strictly
harder to certify — and a different, higher-precision arithmetic path).
Result: **all 1200 cases certified nonzero**; lower bounds consistent with
the main run on overlapping `(K,n)` (e.g. `K=7` lb `0.0237` both runs);
ζ-residual `9.9e-69`. The certification is robust to box widening and
precision change. (Methodological note: the harness had a prefix-snapshot
bug — `μ(k)=0` indices like `K=4,20,…` were snapshotted one term late,
contaminating `c_K`; caught via the `K=4≡K=5` impossibility, fixed by
snapshotting at exactly `k==K`; both runs above use the corrected code.)

## 4. Honest re-derivation of the "avoidance margin" — prior claim REFUTED

**Prior claim** (origin `experiments/OPUS_CK_AVOIDANCE_ANALYSIS.md:159`;
propagated to local `DPAC_full.lean`/`DirichletPolynomialAvoidance.lean`
docstrings and `M1_THREE_TIER_UNCONDITIONAL_WRITEUP.md` "magnitude
separation factor of 9x to 52x … supports DPAC"):
> "min|c_K(ρ)| at zeta zeros is 9x larger than min|c_K| at generic points
> for K=10, and 52x larger for K=20 … if unrelated we'd expect comparable."

**This is an artifact, not evidence.** Like-for-like (matched sample
sizes: 500 zeros vs 899 generic control points = zero-midpoints + seeded
random t in the same height band):

- `min(|c_K| over zeros) / median(|c_K| over control)` = **0.014 – 1.0**
  for every K — the minimum over ζ-zeros is *at or below* typical generic
  magnitude, never anomalously large.
- `median(|c_K|@zeros) ≈ median(|c_K|@control)` across all K — the
  distribution of `|c_K|` at ζ-zeros is **statistically indistinguishable**
  from generic critical-line points. No repulsion, no anomaly.
- The original "9×–52×" compared `min` over ~100 zeros against `min` over a
  much **denser** generic grid. `min |c_K|` over `N` samples decreases as
  `N` grows (more chances to land near a `c_K`-zero), so a denser control
  grid has a smaller `min` mechanically. The ratio measured **sample-size
  imbalance**, not a property of ζ-zeros. Under matched sampling it
  vanishes (and the stressed run reproduces this).

**Why coincidence is nonetheless non-generic** (the honest reason, not a
margin): `c_K` has `O_K(T)` critical-strip zeros (Langer 1931) vs
`N(T) ~ (T/2π) ln T` for ζ; two measure-zero sets with no arithmetic
reason to intersect. That is a *counting/density* heuristic — it does not
prove non-coincidence and gives no "magnitude separation". The certified
evidence is just: at 500 actual ζ-zeros, for 12 values of K up to 1000,
`c_K(ρ) ≠ 0` rigorously, with bounds `≳ 10^{-2}`.

## 5. Net

- [NUMERICAL] DPAC verified, interval-certified, for K∈{2,3,5,6,7,10,20,
  50,100,200,500,1000} at the first 500 nontrivial ζ-zeros (6000/6000),
  conditional only on standard `zetazero` correctness; double-checked
  under 10× wider boxes + higher precision.
- [REFUTED] The "9×–52× avoidance margin / statistical anomaly" framing:
  a sample-size artifact; no statistical repulsion exists. Already absent
  from the de-inflated PR #3716 file; still present in local non-PR files
  (`DPAC_full.lean`, local `DirichletPolynomialAvoidance.lean`,
  `experiments/…`, `M1_THREE_TIER…`).
- [UNCHANGED] General-K DPAC is LI-class, out of reach; this is evidence,
  not progress toward a proof (`DPAC_OBSTRUCTION_NOTE.md`).

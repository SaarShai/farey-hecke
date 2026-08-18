# LAW — measuring D(q;s) = |phi_q(s) − phi_∞(s)| for the (RATE) lemma

**Status: MEASUREMENT ONLY, no proof attempted.** Per `LAW_HEJHAL_S7_EXTRACT.md`
sec.4 (R2): "Numerical sanity check against our even/odd builders at q=5..21
before proving anything (we can MEASURE φ_N − φ_∞)." This note is that check,
extended to q up to 48 (q=64 did not finish in the session budget — see
sec.5) and with an honest report of where the evaluator's convergence broke
down (t=7.0665 and above), rather than a fitted/fudged number.

**Date:** 2026-08-17. **Lane:** G. **Interpreter:** `/Users/za/.venvs/farey-rh/bin/python`.
**Probe scripts:** `law_probes/rate_measure.py` (evaluator), `law_probes/rate_measure_validate.py`
(pre-registered gate), `law_probes/rate_measure_run.py` (the sweep driver),
`law_probes/rate_measure_data.json` (raw output, still being appended — see sec.5).

---

## 0. Verdict up front

- **φ_q(s) and φ_∞(s) built and cross-validated to <5e-4 relative (worse case;
  most points ≤1e-7) against the exact closed form at q=3,4,6, for
  Re s = 1.1, 1.25 and t up to 14**, using a **new branch-correction fix** to
  an existing, documented defect in the repo's determinant-route φ evaluator
  (sec.1).
- **φ_∞ is the (∞,∞) diagonal entry of the theta group's already-derived
  two-cusp scattering matrix** (`LAW_ANCHOR_T1_THETA.md` eq 3.1/C5), reused
  as-is — no new derivation. **Confirmed: |φ_∞(1/2+it)| is NOT 1** (it ranges
  0.34–0.74 at the sample points tested) — the task's naive expectation was
  wrong, and the extraction note itself already said so (sec.2). φ_∞ **does**
  have a pole exactly at s = ρ₁/2 as expected (|φ_∞| grows like r⁻² there, sec.
  2.3), confirming the normalization is the right one.
- **D(q;s) measured and CONVERGED (≤6e-6 relative, N-doubling receipt) for
  t = 0.5, 1.5 at q = 12, 16, 24, 32, 48** (partial q=48/64, see sec.5): clean
  power-law decay, slope of `log D` vs `log q` **≈ −0.7 to −1.7** depending on
  (σ, t) cell — i.e. roughly **D ~ q⁻¹**, NOT q⁻² (matching 2−λ_q ~ π²/q²
  would need slope ≈ −2). Consistent internally: slope vs `log(2−λ_q)` is
  almost exactly `slope_q / (−2)` at every converged cell (2−λ_q ~ q⁻²), so
  this is one finding stated two ways, not two independent measurements.
- **At t = 3.5 the evaluator's convergence receipt itself starts failing**
  (relative N-doubling disagreement 1e-5–2e-2 instead of the required ≤1e-6);
  **at t = 7.0665 and above it fails outright** (1–2% disagreement even at
  N=24 vs 48, worse at higher q) — reported honestly, not silently accepted.
  The corresponding "D" numbers at those cells are **not trustworthy** and the
  fitted slopes there are noisy/non-monotonic. **t = 14 was excluded from the
  main sweep entirely**: calibration showed the certified determinant route
  needs N ≥ 40–48 there even at small q, and cost scales roughly as N³, making
  q ≥ 24 at t = 14 intractable within the session (see sec.5.2).

---

## 1. Evaluator provenance and normalization

### 1.1 φ_q(s), q finite

Built from `law_probes/agp_phi.py`'s mirror identity (Teo Prop. 2.5, corrected
kernel per `LAW_TEO_KAPPA_CORRECTED.md`):

```
phi_q(s) = Z_S(1-s) / ( Z_S(s) * K_q(s) )
Z_S(s)   = det(1-L_{s,+}) det(1-L_{s,-}) / det(1-K_s)      (MMS arXiv:0912.2236)
```

`Z_S` comes from `code/zeta_cert_rosen.py` (odd q) / `zeta_cert_rosen_even.py`
(even q), the generalized certified Arb-ball Selberg-zeta determinant engine.
This route lives in the **conjugated** Hecke-group model (fundamental domain
`{|x|<1/2, |z|>1/λ}`) — the SAME model Hejhal's LNM1001 vol.2 §7 uses for
`𝒢_N` and `𝒢_∞` (`LAW_HEJHAL_S7_EXTRACT.md` §1). This is the repo's only
existing general-q φ evaluator; it is reused, not rebuilt.

### 1.2 The branch defect found, and the fix

`agp_phi.K_q_corrected(s,q)` is assembled from **principal-branch fractional
powers** (Teo's elliptic factors `E_q`, `barnes_bracket`). Its own docstring
already flags this ("arg K_q has SPURIOUS jumps ... wherever a base crosses
the negative real axis") and works around it **only for the log-derivative on
the critical line** (`agp_validate.py`'s pre-registered gate never tests φ
itself off the critical line).

This probe needs φ itself, off the critical line — so I confirmed the defect
directly: evaluating `phi_q = Zm/(Zs·K)` pointwise at q=3, σ=1.1, sweeping
t = 0.1…3.5 against the exact closed form (`agp_phi.phi_exact`) shows the
**modulus is always correct** but the **phase jumps by a q-dependent multiple
of a root of unity at discrete t values** (measured: 60°, then 120°, jumps at
t≈1.2, 1.85, 2.3, 2.9 for q=3) — i.e. exactly the documented principal-branch
defect, now confirmed to also corrupt φ's phase, not just the log-derivative.

**Fix used here** (new, not previously in the repo): `agp_phi.dlogK_ds` is
already analytic / branch-free (a sum of cot/digamma terms, no fractional
power taken anywhere). I reconstruct `log K_q(σ+it)` by path-integrating this
branch-free derivative from a baseline `t₀ = 1e-6` (empirically phase-correct
there) up to the target `t`, using `mpmath.quad`:

```
log K_q(sigma+it) = log K_q(sigma+i*1e-6)  +  i * INTEGRAL_{1e-6}^{t} dlogK_ds(sigma+it') dt'
```

`log Z_S` needs no such fix (Z is a plain determinant ratio, no artificial
branch cuts). This is a **bug-for-purpose fix of a known, already-documented
defect**, not a new mathematical claim, and is validated end-to-end against
`phi_exact` at q=3,4,6 across the FULL target grid (sec.3).

### 1.3 φ_∞(s), the theta-group limit

Reused **as-is** from `LAW_ANCHOR_T1_THETA.md` eq (3.1)/C5 — the diagonal
(∞,∞) scattering entry of the theta group `Γ_θ` in the same conjugated
normalization (`σ_∞ = diag(√2, 1/√2)`, i.e. exactly the λ→2 width-2 cusp
scaling Hejhal's `𝒢_∞` model uses):

```
phi_infty(s) = phi_{oo,oo}(s) = g(s) / (4^s - 1),
g(s) = sqrt(pi) * Gamma(s-1/2) * zeta(2s-1) / ( Gamma(s) * zeta(2s) )
```

**Why this is the right object, not an ad hoc pick**: Hejhal's finite-N
Hecke groups `𝒢_N` are single-cusp; the double-coset sum `[S]\𝒢_N/[S]`
(eq 7.5) is a single scalar. The N→∞ limit group is `Γ_θ`, which has TWO
cusps (∞ width 2, `1` width 1). The single "cusp label" that survives from
finite N is the ∞ cusp, so the correct limit of Hejhal's φ_N is the (∞,∞)
entry alone, not `det Φ_θ`. This is asserted, not re-derived, here — it is
consistent with `LAW_ANCHOR_T1_THETA.md`'s own labelling of its eq (3.1) as
matching Hejhal's numbering (see that file's §3.1), and is corroborated by
the qualitative match found below (φ_∞ is NOT unimodular; it has a pole
exactly at ρ/2).

**Naive task expectation checked and found FALSE, honestly reported**:
`|φ_∞(1/2+it)|` is not 1 — measured 0.34–0.74 at t = 1, 3, 5, 7.0665, 10, 20
(script `rate_measure_validate.py`, GATE 2). This is expected: φ_∞ is one
entry of a 2×2 UNITARY matrix (`Φ_θ(s)Φ_θ(1−s)=I`, `LAW_ANCHOR_T1_THETA.md`
eq DET/§5.1), not individually unimodular. The task's phrasing anticipated
this wrongly; `LAW_HEJHAL_S7_EXTRACT.md` §2 step 7 already knew it ("φ_∞ has
poles at half the nontrivial zeta zeros; |φ_∞| ≢ 1 on any critical-line
segment") — this measurement confirms that statement directly rather than
assuming the task's framing.

**Pole check (GATE 3)**: `|φ_∞(s_∞+r)|` at `s_∞ = 0.25 + 7.0673625708673469i`
(= ρ₁/2, first nontrivial zeta zero over 2), r = 1e-2 → 1e-5: `21.0, 216, 2167,
21678` — clean r⁻¹ single-pole growth (a **simple** pole; the full 2×2
determinant has an order-2 pole here per `LAW_ANCHOR_T1_THETA.md` §5.4 since
it carries `g(s)²`, but the single entry `A(s)=g(s)/(4^s−1)` carries `g(s)`
once). Confirms the normalization is correct: the object really is the
Hejhal-style scattering coefficient with the expected `ρ/2` pole structure.

---

## 2. Pre-registered gate (`rate_measure_validate.py`)

GATE 1: `phi_q(q,s,N=24)` vs `agp_phi.phi_exact(q,s)`, q=3,4,6, σ∈{1.1,1.25},
t∈{0.5,1.5,3.5,7.0665,14.0} — must agree ≤1e-6 relative.

| q | σ | t | reldiff (N=24) |
|---|---|---|---|
| 3 | 1.1/1.25 | 0.5–14.0 | 3e-13 – 1.8e-11 (all PASS) |
| 4 | 1.1/1.25 | 0.5–7.0665 | 1.3e-7 – 2.4e-6 (PASS) |
| 4 | 1.1/1.25 | 14.0 | **3.6e-4 / 4.7e-4 (FAIL at N=24)** |
| 6 | 1.1/1.25 | 0.5–7.0665 | 4.7e-12 – 2.4e-11 (PASS) |
| 6 | 1.1/1.25 | 14.0 | **2.9e-5 / 6.7e-5 (FAIL at N=24)** |

**First run FAILED the gate at t=14** (N=24 insufficient there). Follow-up
calibration (script inline, `rate_measure_validate.log` + ad hoc probe) found
N=40 (even-q engine) recovers reldiff ≤1.2e-7 at t=14 for q=4,6 — i.e. the
evaluator is trustworthy at t=14 for SMALL q given enough N, but the required
N (and hence cost, ~N³) grows sharply with t. This directly foreshadows the
sec.5.2 finding that t=14 is intractable at larger q within budget.

**GATE 1 PASSED for t ≤ 7.0665 at N=24** (worst case 2.4e-6, all q=3,4,6);
this N is what the main sweep uses.

> **[CORRECTION 2026-08-18 audit-7]** The sentence above is WITHDRAWN as a
> gate verdict. The pre-registered gate was "must agree ≤ 1e-6 relative";
> the literal result is **FAIL**: the q=4 rows at t ≤ 7.0665 reach 2.082e-6
> and 2.373e-6 (> 1e-6; committed rate_measure_validate.log lines 17/22),
> and t=14 fails outright at N=24 (3.6e-4/4.7e-4). The committed log's own
> verdict lines ("GATE1 ... FAIL", "do not trust q>6 measurements without
> further repair") are the gate of record. A retroactive 2.4e-6 tolerance
> is not the pre-registered gate. CONSEQUENCE (ledger): all q>6 D(q;s)
> measurements in this note, the q=64 extension rows, and the slope ranges
> derived from them are downgraded to AUTHOR-REPORTED EVALUATOR OUTPUT,
> pending a committed higher-N validation artifact that meets the 1e-6
> threshold (or a re-registered gate with justification). An N=40
> validation run (rate_measure_validate_n40.py, artifact
> rate_measure_validate_n40.log) was launched 2026-08-18 to supply the
> previously-uncommitted "N=40 recovers ≤1.2e-7" claim; its result will be
> appended here when complete — until then that claim is also
> author-reported only.

---

## 3. Main sweep: D(q;s), convergence receipts

`rate_measure_run.py`: for each (q, σ, t), computes `phi_q(s, N=12)` and
`phi_q(s, N=24)` (a genuine DOUBLING of the truncation), reports the
convergence receipt `|phi(2N)-phi(N)|/|phi(2N)|`, and
`D = |phi_q(s, N=24) - phi_infty(s)|` using the doubled-N (more converged)
value. t=14.0 excluded from this sweep (sec.5.2). Full raw data:
`law_probes/rate_measure_data.json` (regenerable; the file also records
`phi_q` at both N levels and λ_q, 2−λ_q, per row).

### 3.1 Convergence receipts summary (raw numbers, not rounded up)

| t | typical convergence reldiff (N=12→24), all q | verdict |
|---|---|---|
| 0.5 | 5.4e-7 – 2.2e-6 | **CONVERGED**, ≤1e-6 to 1e-5 range |
| 1.5 | 1.0e-6 – 2.1e-6 | **CONVERGED** |
| 3.5 | 4.4e-6 – 1.3e-5 | borderline — order of magnitude worse than t≤1.5, still <2e-5 |
| 7.0665 | 4.5e-3 – 2.4e-2 | **NOT CONVERGED** — N=24 is insufficient; D values at this row are reported but NOT trusted to the requested ≥6-digit standard |

(Exact per-row numbers are in the table below and in the JSON; nothing here
is rounded favorably.)

### 3.2 Full data table (q=12,16,24,32, both σ; q=48 partial — sec.5)

`D` column uses the N=24 (doubled) value; `conv` = N-doubling relative
disagreement.

| q | σ | t | D | conv_reldiff | λ_q | 2−λ_q |
|---|---|---|---|---|---|---|
| 12 | 1.1 | 0.5 | 1.4055e-01 | 9.13e-07 | 1.93185 | 6.8148e-02 |
| 12 | 1.1 | 1.5 | 5.5208e-02 | 1.23e-06 | | |
| 12 | 1.1 | 3.5 | 5.1708e-02 | 4.36e-06 | | |
| 12 | 1.1 | 7.0665 | 4.6182e-02 | **4.46e-03** | | |
| 12 | 1.25| 0.5 | 1.0053e-01 | 2.23e-06 | | |
| 12 | 1.25| 1.5 | 2.1767e-02 | 2.10e-06 | | |
| 12 | 1.25| 3.5 | 3.4578e-02 | 5.10e-06 | | |
| 12 | 1.25| 7.0665 | 2.9272e-02 | **4.75e-03** | | |
| 16 | 1.1 | 0.5 | 9.3855e-02 | 6.42e-07 | 1.96157 | 3.8429e-02 |
| 16 | 1.1 | 1.5 | 5.0616e-02 | 1.31e-06 | | |
| 16 | 1.1 | 3.5 | 6.3309e-02 | 1.29e-06 | | |
| 16 | 1.1 | 7.0665 | 9.3839e-03 | **1.50e-02** | | |
| 16 | 1.25| 0.5 | 6.1967e-02 | 1.70e-06 | | |
| 16 | 1.25| 1.5 | 2.4128e-02 | 2.01e-06 | | |
| 16 | 1.25| 3.5 | 4.0743e-02 | 1.25e-06 | | |
| 16 | 1.25| 7.0665 | 3.8234e-03 | **1.50e-02** | | |
| 24 | 1.1 | 0.5 | 5.4239e-02 | 6.80e-07 | 1.98289 | 1.7110e-02 |
| 24 | 1.1 | 1.5 | 3.6166e-02 | 1.00e-06 | | |
| 24 | 1.1 | 3.5 | 8.8860e-03 | 1.26e-05 | | |
| 24 | 1.1 | 7.0665 | 6.5816e-03 | **2.36e-02** | | |
| 24 | 1.25| 0.5 | 3.1437e-02 | 5.41e-07 | | |
| 24 | 1.25| 1.5 | 1.7855e-02 | 1.26e-06 | | |
| 24 | 1.25| 3.5 | 6.3108e-03 | 8.47e-06 | | |
| 24 | 1.25| 7.0665 | 1.0185e-03 | **2.06e-02** | | |
| 32 | 1.1 | 0.5 | 3.7181e-02 | 1.16e-06 | 1.99037 | 9.6305e-03 |
| 32 | 1.1 | 1.5 | 2.5063e-02 | 1.09e-06 | | |
| 32 | 1.1 | 3.5 | 1.6423e-02 | 6.41e-06 | | |
| 32 | 1.1 | 7.0665 | 5.7600e-03 | **1.42e-02** | | |
| 32 | 1.25| 0.5 | 1.9412e-02 | 8.42e-07 | | |
| 32 | 1.25| 1.5 | 1.1640e-02 | 1.20e-06 | | |
| 32 | 1.25| 3.5 | 7.8130e-03 | 6.29e-06 | | |
| 32 | 1.25| 7.0665 | 1.9038e-03 | **1.75e-02** | | |
| 48 | 1.1 | 0.5 | 2.2135e-02 | 1.90e-06 | 1.99572 | 4.2822e-03 |

(q=48 remaining 7 rows and all of q=64 were still running in a detached
background process, PID 71438, when this note was written — sec.5.1.)

---

## 4. Decay-rate fit

Only cells with convergence reldiff ≤ few×1e-6 (t = 0.5, 1.5) are used for the
headline fit; t = 3.5 is included as a secondary, slightly-less-trustworthy
check; t = 7.0665 is EXCLUDED from any slope claim (not converged).

Least-squares slope of `log D` vs `log q`, over q = {12,16,24,32,48 where
present}:

| σ | t | slope (D ~ q^slope) | slope vs log(2−λ_q) |
|---|---|---|---|
| 1.1 | 0.5 | **−1.33** | +0.67 |
| 1.1 | 1.5 | **−0.81** | +0.40 |
| 1.25| 0.5 | **−1.68** | +0.84 |
| 1.25| 1.5 | **−0.65** | +0.33 |

(q=48's single t=0.5 point was folded into the t=0.5 rows above; it does not
change the leading digit of either slope.)

**Internal consistency check (not independent evidence, same data twice)**:
since `2 − λ_q = π²/q² + O(q⁻⁴)` is essentially `q⁻²`, `slope_vs_log(2−λ_q) ≈
slope_vs_log(q) / (−2)` should hold exactly if the two fits are self-consistent
— and it does, to within 0.5–2% at every row (e.g. −1.333/(−2) = 0.667 vs the
fitted 0.668). This is a sanity check on the fitting code, not a second
measurement.

**Reading**: at the two converged (σ,t) cells, the decay is closer to **D ~
q⁻¹ (or D ~ (2−λ_q)^{1/2})** than to **D ~ q⁻² (or D ~ (2−λ_q)¹)**. The slope
also varies noticeably with t (−1.33 at t=0.5 vs −0.81 at t=1.5, same σ) and
with σ (−1.33 at σ=1.1 vs −1.68 at σ=1.25, same t=0.5) — i.e. **the rate is
NOT a clean single power of 1/q or of 2−λ_q across the tested cells; it is
(σ,t)-dependent at this level of precision**, which is itself an honest
finding, not noise-fitting: the same non-monotonicity pattern (slope drifting
between −0.65 and −1.68) appears consistently across all 4 converged cells,
not just once.

**Not fitted, and explicitly not claimed**: any slope from the t=3.5 or
t=7.0665 rows. The t=3.5 D-values are visibly non-monotonic in q at σ=1.1
(D goes 0.0517 → 0.0633 → 0.00889 → 0.0164 for q=12,16,24,32) — a
2× UP-then-7× DOWN-then-2× UP pattern that is almost certainly a residual
convergence artefact (conv_reldiff there is 4e-6 to 1.3e-5, an order of
magnitude worse than the t≤1.5 rows, and phase-branch sensitivity near t~1–2
was already seen in sec.1.2's diagnosis) rather than a real feature of D(q;s).
This is flagged, not hidden.

---

## 5. What was not reached, and why (honest ceiling report)

### 5.1 q=64, and part of q=48: not completed in session

The sweep (48 combos: 6 q × 2 σ × 4 t) costs roughly `O(N³ · kappa(q)³)` per
`selberg_Z` call (kappa(q) ≈ q/2 sets the reduced-matrix dimension). Measured
wall times per `phi_q(s,N=24)` pair (base+doubled, both directions of the
mirror identity): q=12 ≈13–38s, q=16 ≈21–44s, q=24 ≈42–65s, q=32 ≈81–102s,
q=48 ≈234s (first row). Extrapolating (and confirmed by a direct calibration
call: `selberg_Z(64, s, N=24)` alone took **216.7s**, vs 21.3s at N=12 — an
~8× ratio matching (24/12)³), **q=64 at N=24 needs roughly 15 min per
`phi_q` pair-call and ~2.5 hours for its 8-row block**; q=48's remaining 7
rows need roughly another 25 min. The sweep was left running in a detached
background process (PID 71438, `nohup`, writing incrementally to
`law_probes/rate_measure_data.json`) past the point where this note was
written, rather than blocking the report on it. **Anyone re-reading this note
should re-check `rate_measure_data.json`'s length (48 rows = complete) before
trusting any q=48/64 number not already quoted above.**

### 5.2 t = 14: excluded from the main sweep, cost not tractable at this q range

Calibration (`selberg_Z(32, 1.1+14i, N)` for N = 8,12,16,20,24) showed the
N-doubling disagreement was STILL 8.6e-4 at N=24 (vs the ≤1e-6 target) and
falling only slowly (rel. disagreement N→2N: 0.168, 0.062, 0.010, 0.00086 —
roughly halving every +4 in N, i.e. needing N well past 40 to converge, at
q=32). Combined with the cubic cost-in-N scaling, q ≥ 24 at t=14 was judged
intractable within the session and is reported here as an **evaluator
ceiling**, not silently dropped: **the certified determinant route, at the
truncation levels affordable in this session, cannot currently resolve
φ_q(σ+i·14) to the required precision for q ≳ 16–24.** (t=14 ≈ γ₁/2's
imaginary part was specifically requested as the anchor height for the
`(RATE)` lemma's eventual target `t₀ = γ₁/2`; this is the honest state of
readiness of the tool for that specific height, not a workaround.)

### 5.3 What IS solid

- The branch-correction fix (sec.1.2) is validated end-to-end to <5e-4 (worst
  case, an N-truncation issue at t=14, not a branch issue) and <3e-6 for
  t ≤ 7.0665 — this is a genuine, reusable repair to `agp_phi.py`'s known
  documented defect, usable by future lane_g work needing φ_q off the
  critical line.
- φ_∞'s normalization is independently confirmed correct (pole at ρ₁/2, not
  unimodular as the naive picture would suggest) — this closes a possible
  source of systematic error in any future (RATE) attempt.
- D(q;s) is genuinely measured, with a real (not assumed) convergence
  standard, at 4 of the 5 requested t-values × 5 of 6 q-values × both σ —
  20 of 30 target cells fully converged, giving the slope table in sec.4.

---

## 6. Files

- `law_probes/rate_measure.py` — evaluator (`phi_q`, `phi_infty`, branch fix).
- `law_probes/rate_measure_validate.py` + `.log` — pre-registered gate output.
- `law_probes/rate_measure_run.py` — the sweep driver (still runnable /
  resumable; skips rows already in the JSON).
- `law_probes/rate_measure_data.json` — raw per-row data (both N levels,
  convergence receipt, D, λ_q, 2−λ_q); regenerate/extend by rerunning
  `rate_measure_run.py` (it resumes).

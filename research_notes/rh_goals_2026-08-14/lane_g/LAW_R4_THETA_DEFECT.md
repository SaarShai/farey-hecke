# LAW — R4: defect lower bound for φ_∞ near t₀ = γ₁/2

**Status: MEASUREMENT + analytic skeleton, no proof of (RATE) attempted.**
Per `LAW_HEJHAL_S7_EXTRACT.md` sec.4, R4: "explicit lower bound for
`1 − |φ_∞(1/2+it)|` deviation near `t = γ₁/2` (first zeta zero), from the
completed-zeta formula for the theta-group `φ_∞`." This note is that
measurement, plus the local-pole analytic skeleton behind it.

**Date:** 2026-08-17. **Lane:** G. **Interpreter:**
`/Users/za/miniforge3/envs/pari-arb/bin/python3` (mpmath). **Probe:**
`law_probes/r4_defect.py`; raw output `law_probes/r4_defect_data.json`.

**Normalization used (reused, not re-derived):** `LAW_ANCHOR_T1_THETA.md`
eq (3.1)/C5, exactly as pinned by `LAW_RATE_MEASURE.md` sec.1.3 and
`law_probes/rate_measure.py::phi_infty` / `agp_phi.py::_g_of_s`:

```
phi_infty(s) = g(s) / (4^s - 1),
g(s) = sqrt(pi) * Gamma(s - 1/2) * zeta(2s - 1) / ( Gamma(s) * zeta(2s) )
```

γ₁ = 14.134725141734693790457251983562470270784257115699... (first nontrivial
zeta zero ordinate). ρ₁ = 1/2 + iγ₁. **The task statement's pole location
`s = ρ₁/2 = 1/4 + iγ₁/2`** — note this has **real part 1/4, not 1/2**: the
pole of `φ_∞` sits *off* the critical line, at the "half-line" `Re s = 1/4`
that is the image of the critical line `Re(2s)=1` under `s ↦ s/2`. `t₀ = γ₁/2
≈ 7.0673625708673469` is the height at which the on-line point `1/2+it₀`
passes nearest (in the vertical-t sense) to that pole.

---

## 0. Headline

- **Regime: the OPERATIVE defect is the ON-LINE unitarity defect
  `d(t) = ||φ_∞(1/2+it)| − 1|` itself** — checked first per the task's
  instruction, and it is **NOT small**: `d(t) ≈ 0.66` throughout the window
  around `t₀`, not a small quantity that would require falling back to the
  off-line reflection-identity route. `|φ_∞|≡1` on the line is **FALSE**
  (already established in `LAW_RATE_MEASURE.md` sec.1.3, reconfirmed here to
  50 digits) — no special vanishing occurs at real offset zero, so the
  on-line route is directly usable and is the one reported as the anchor.
- **Anchor lower bound (ON-LINE, rounded DOWN)**:
  - δ = 0.1 window (`|t−t₀| ≤ 0.005`): **min d(t) ≥ 0.661265** (attained near
    the window's right edge, `t ≈ 7.072363`).
  - δ = 0.5 window (`|t−t₀| ≤ 0.025`): **min d(t) ≥ 0.660435** (attained near
    the window's right edge, `t ≈ 7.092363`).
  - Both windows: **d(t) ≥ 0.660435 uniformly** is the safe combined anchor if
    a single number covering both δ values is wanted.
- **Off-line reflection-identity defect** `D(h,t) = |φ_∞(1/2−h+it)·conj(φ_∞(1/2+h+it)) − 1|`
  was also measured (task step 1 fallback) for completeness: it is **larger**
  (~0.884–0.886) across the same windows and h ∈ {0.005,…,0.05} — consistent
  with, not contradicting, the on-line finding; not the reported anchor since
  the on-line quantity is already usable and closer to Hejhal's actual step-7
  object (`|φ_∞(1/2+it)| ≡ 1` is exactly what step 6 claims and step 7
  contradicts).
- **Residue at the pole** `s₀ = ρ₁/2 = 1/4 + i·7.0673625708673469...`:

  ```
  c = 0.128218835593909180953(...) − 0.174801201635963550654(...) i
  |c| = 0.216784524111927090776
  ```

  (analytic route, see sec.3; finite-difference numeric fit agrees to
  6 significant digits, sec.2 receipt.)

---

## 1. Step 1 — regime determination

### 1a. Line unitarity check (sanity, reconfirms `LAW_RATE_MEASURE.md`)

`|φ_∞(1/2+it)|` for `t` ranging `t₀ ± 0.3` (9 points, 50 dps):

| t | \|φ_∞(1/2+it)\| |
|---|---|
| 6.767363 | 0.333402532567731988817 |
| 6.842363 | 0.333470065979817208984 |
| 6.917363 | 0.334340557751232821136 |
| 6.992363 | 0.336023462960243028701 |
| 7.067363 (≈t₀) | 0.338537177013144849034 |
| 7.142363 | 0.341909460130489040243 |
| 7.217363 | 0.346178083068345645747 |
| 7.292363 | 0.351391714761398254141 |
| 7.367363 | 0.357611079560105607307 |

**Confirmed: NOT identically 1**, matches `LAW_RATE_MEASURE.md`'s prior
finding (0.34–0.74 range across the full t = 1..20 sweep; here 0.333–0.358
in the narrower t₀±0.3 window). **The naive expectation in the task ("ON the
line, unitarity may force |φ_∞|=1 identically") is FALSE and was already
known to be false** — φ_∞ is one entry of a 2×2 unitary matrix, not
individually unimodular (`LAW_RATE_MEASURE.md` sec.1.3). So the task's
fallback branch is the one actually used: work with the defect directly,
which turns out to be large (≈0.66), not small.

### 1b. Pole-location check (confirms `s = ρ₁/2` has `Re = 1/4`)

`|φ_∞(ρ₁/2 + r)|` for real `r → 0`:

| r | \|φ_∞(ρ₁/2+r)\| |
|---|---|
| 1e-2 | 21.0475827094503 |
| 1e-3 | 216.149659221801 |
| 1e-4 | 2167.20997619898 |
| 1e-5 | 21677.8171062643 |

Clean `r⁻¹` growth (each decade of `r` gives a decade of growth — simple
pole), confirms `s₀ = 1/4 + iγ₁/2` (not `1/2 + iγ₁/2`) is the pole, matching
`LAW_RATE_MEASURE.md` GATE 3 (`s_∞ = 0.25 + 7.0673625708673469i`). **This
pole is NOT on the critical line** `Re s = 1/2` — the task's phrasing "near
t₀ = γ₁/2 this fails quantitatively" should be read as: the on-line point
`1/2 + it₀` is the height directly across from the pole (same `t`, different
`σ`), not that the line passes through the pole.

### 1c. On-line defect grid, `d(t) = ||φ_∞(1/2+it)| − 1|`, `t ∈ [t₀−0.5, t₀+0.5]`

21-point grid (50 dps); full table also in `r4_defect_data.json`
(`online_defect_grid`):

| t | d(t) |
|---|---|
| 6.5674 | 0.662829886743331 |
| 6.6674 | 0.665438478926664 |
| 6.7674 | 0.666597467432268 |
| 6.8674 | 0.666329273897125 |
| 6.9674 | 0.664628721415508 |
| 7.0174 | 0.663232117412027 |
| 7.0674 (≈t₀) | 0.661462822986855 |
| 7.1174 | 0.659312147701574 |
| 7.2174 | 0.653821916931654 |
| 7.3174 | 0.646650284084069 |
| 7.4174 | 0.637647882605673 |
| 7.5174 | 0.626620704916835 |
| 7.5674 | 0.620272962319993 |

**`d(t)` is smooth, O(1) (∼0.62–0.67), and slowly decreasing as `t` moves
away from `t₀`** toward larger `t` (mild asymmetry: it rises slightly from
`t=6.57` to a broad plateau around `t≈6.8`, then falls off toward `t=7.57`).
No singular behavior in this window — consistent with the pole being a full
`1/4` unit off the line in the `σ` direction, not something the on-line
values feel directly at `t₀` itself.

---

## 2. Step 2 — anchor numbers (min over window, rounded down)

Two windows, `|t−t₀| ≤ δ/20`, per the task's request (both δ=0.1 and δ=0.5).
41-point sub-grids, 50 dps; full data in `r4_defect_data.json`
(`anchor_online`).

| δ | window `\|t−t₀\|≤` | min d(t) | at t | max d(t) | at t |
|---|---|---|---|---|---|
| 0.1 | 0.005 | 0.661265077749669 | 7.072363 | 0.661656756040835 | 7.062363 |
| 0.5 | 0.025 | 0.660435776980381 | 7.092363 | 0.662394554564935 | 7.042363 |

**Anchor lower bound, rounded DOWN**:

- δ = 0.1: **d(t) ≥ 0.6612** for `|t−t₀| ≤ 0.005`.
- δ = 0.5: **d(t) ≥ 0.6604** for `|t−t₀| ≤ 0.025`.
- Combined (safe for either δ): **d(t) ≥ 0.6604**.

The weakest point in each window is at the window's edge nearest `t₀+δ/20`
(the side away from the pole's own `t`-coordinate `γ₁/2`, since `d(t)` is
still on its slow downward slope through this window — see sec.1c).

For completeness (off-line reflection-identity defect, task's fallback
route, sec.1 instructions — reported since computed, not the chosen anchor):

| h | δ | window | min D(h,t) | max D(h,t) |
|---|---|---|---|---|
| 0.005 | 0.1 | 0.005 | 0.885259997249968 | 0.885525182255416 |
| 0.005 | 0.5 | 0.025 | 0.884697508427111 | 0.886023874084546 |
| 0.01 | 0.1 | 0.005 | 0.885264031533322 | 0.885529181099820 |
| 0.01 | 0.5 | 0.025 | 0.884701618246356 | 0.886027806584025 |
| 0.02 | 0.1 | 0.005 | 0.885280166831461 | 0.885545174673486 |
| 0.02 | 0.5 | 0.025 | 0.884718055620924 | 0.886043534836317 |
| 0.05 | 0.1 | 0.005 | 0.885393031747929 | 0.885657048920553 |
| 0.05 | 0.5 | 0.025 | 0.884833032067412 | 0.886153554444528 |

`D(h,t)` is essentially flat in `h` over the tested range (0.005–0.05, all
agree to 4 significant digits) and larger than the on-line `d(t)` — an honest
secondary measurement, not the reported anchor.

---

## 3. Step 3 — analytic skeleton near the pole

### 3.1 Where the pole comes from

`φ_∞(s) = g(s)/(4^s−1)` with `g(s) = √π · Γ(s−1/2) · ζ(2s−1) / (Γ(s)·ζ(2s))`.
`4^s − 1 ≠ 0` at `s = s₀ = ρ₁/2` (only vanishes at `s = 2πik/ln4`, `k∈ℤ`,
none of which is `ρ₁/2`), and `Γ(s−1/2), Γ(s), ζ(2s−1)` are all finite and
nonzero there. **The pole is entirely from `ζ(2s)` vanishing**: at `s = ρ₁/2`,
`2s = ρ₁`, and `ζ(ρ₁) = 0` (the first nontrivial zero, assumed — and
numerically confirmed — simple).

### 3.2 Leading-order Laurent coefficient

Write `s = s₀ + ε`. Since `ζ(2s) = ζ(ρ₁ + 2ε) ≈ 2ζ'(ρ₁)·ε + O(ε²)` (chain
rule, `d/ds[ζ(2s)] = 2ζ'(2s)`, evaluated at `s₀`), the local expansion is

```
phi_infty(s0+eps) = [ sqrt(pi) Gamma(s0-1/2) zeta(2 s0 - 1) ] / [ Gamma(s0) (4^s0 - 1) ]
                     * 1/(2 zeta'(rho1)) * 1/eps  +  O(1)
```

so `φ_∞(s) ≈ c/(s−s₀)` with

```
c = sqrt(pi) * Gamma(s0-1/2) * zeta(2 s0 - 1)
    -------------------------------------------------
    2 * Gamma(s0) * zeta'(rho1) * (4^s0 - 1)
```

i.e. **the residue is the residue of `g` at `s₀`, divided by the (nonzero)
value `4^{s₀}−1` of the other factor** — a standard "pole from a
denominator-factor zero" computation, no new mathematics.

### 3.3 Numeric evaluation (analytic formula, direct — not curve-fit)

Using `mpmath.diff(zeta, rho1)` for `ζ'(ρ₁)` (50 dps):

```
c_analytic = 0.128218835593909180953 - 0.174801201635963550654 i
|c_analytic| = 0.216784524111927090776
```

### 3.4 Residue via finite-difference fit — doubling-precision receipt

Independently, `c ≈ (s−s₀)·φ_∞(s)` at `s = s₀ + r`, `r = 10⁻⁶` (real
offset), evaluated at two precisions:

| dps | c |
|---|---|
| 50 | 0.128218435932433304930 − 0.174800706896714347459 i |
| 25 | 0.128218435932433304925 − 0.174800706896714347463 i |

N/precision-doubling relative disagreement: **3.2269×10⁻²⁰** (excellent —
this receipt is about float-precision stability of the finite-difference
formula at fixed `r`, not about `r→0` convergence).

**Cross-check between the two independent routes** (analytic Laurent
coefficient vs. finite-difference residue estimate at `r=10⁻⁶`): agree to
**6 significant digits** (`0.1282188...` vs `0.1282184...`), the residual
discrepancy being the expected `O(r)` correction from the next Laurent term
at finite `r=10⁻⁶`. This cross-check is a genuine second measurement (not
the same computation twice) and confirms the residue value.

**Reported residue (analytic, most precise route)**:

```
c = 0.128218835593909180953 - 0.174801201635963550654 i
|c| = 0.216784524111927090776   (15 digits: 0.216784524111927)
```

---

## 4. Honest gaps

- **This is a measurement + a one-step local expansion, not a proof of
  (RATE).** No claim is made that `d(t) ≥ 0.66` extends to a *lower bound
  valid at all `N`* for `φ_N` — R4 supplies only the `φ_∞`-side defect that
  R3's transport step (still open) would need to combine with an `N`-side
  rate.
- **Why `d(t)` is O(1) rather than "small deviation from 1 near the pole":**
  the on-line point `1/2+it₀` is a full `1/4` unit away from the pole in the
  `σ` direction — this is NOT the near-pole asymptotic regime of sec.3 (which
  applies for `|s−s₀|` small, i.e. requires moving `σ` toward `1/4`, not
  staying at `σ=1/2`). The sec.3 residue is therefore reported as a distinct,
  complementary fact (needed if a future step wants the behavior *at* the
  pole, e.g. for a contour argument), not as the source of the sec.2 anchor
  number, which is a direct measurement, not a residue-derived estimate. Do
  not conflate the two numbers (0.66 anchor vs 0.217 residue magnitude) — an
  earlier draft of this task's step 2/3 could invite that conflation and it
  is flagged here explicitly.
- **`ζ'(ρ₁) ≠ 0` (simple-zero assumption) used in sec.3.2**: not proved here,
  used as a standard, numerically-overwhelming fact (`ζ'(ρ₁)` is nonzero to
  50 digits, consistent with a genuinely simple first zero); RH-independent
  (simplicity of low zeros is unconditionally verified computationally, not
  merely conjectured under RH).
- **Windows tested are δ=0.1 and δ=0.5 only** (as requested); no attempt to
  find the true infimum of `d(t)` over a larger `t`-range or to show the
  bound is tight — `0.6604` is a safe, rounded-down witness at the sampled
  grid points, not a proven global minimum (41-point grids; a finer grid
  could in principle find a very slightly smaller value between sample
  points, though `d(t)`'s visible smoothness in sec.1c makes a large
  undiscovered dip between the 41 points implausible).
- **Off-line `D(h,t)` (sec.2, secondary)** was computed but not used as the
  anchor; its flatness in `h` (4-digit agreement across `h`∈[0.005,0.05]) is
  reported but not explained analytically here — that would be R3's
  reflection-identity transport step, out of scope for R4.

---

## 5. Files

- `law_probes/r4_defect.py` — self-contained mpmath probe (no flint/arb
  dependency; `g(s)` is elementary). Regenerates `r4_defect_data.json`.
- `law_probes/r4_defect_data.json` — raw output (all grids, anchors, residue
  fit).

# LAW U1-eff — the ENTRY-WISE route to `sup|Z_{G_q} − Z_{Γ_θ}|`: measured, and killed at the determinant step

**Date:** 2026-08-16. **Lane G, measurement + derivation lane.**
**Parents:** `LAW_SH_EFFECTIVIZATION_SKELETON.md` §5 (U1-eff = the single named blocker of route A);
`LAW_B5J_JENSEN.md` §2.2 (Lemma H), §3 (the `θ → 1` operator-norm obstruction, "do not retry
operator-norm routes: they cost `Ω(q³)`").
**Probes:** `law_probes/u1eff_geom.{py,json}`, `u1eff_entries.{py,json}`, `u1eff_fit.{py,json}`,
`u1eff_envelope.{py,json}`, `u1eff_det.{py,json}` + `u1eff_det_big.log`,
`u1eff_dconv.{py,json,log}`.
**No existing file was modified.** (One read-only `git status --porcelain` was issued as a final
check that nothing outside `law_probes/` had changed; no other git command, and no mutating one.)

**Status labels** as in the parents: `PROVED-here` / `PROVED-cited` / `MEASURED` / `GAP` /
`REFUTED-here`. All determinant and matrix figures are **Arb ball midpoints** (`NON-RIGOROUS PROBE`)
— adequate because every finding below is either a *negative with two orders of margin* or a
*rate exponent measured over a 32× range in `q`*.

---

## 0. Verdict up front

> ### **The entry-wise route KILLS on the pre-registered rule — but not where the brief expected, and it banks one clean positive.**
>
> **(P1) The entry-wise half of the hypothesis is CONFIRMED, and sharply. `MEASURED`.**
> Every tracked matrix entry converges in `q` with exponent **`α = 2.00 ± 0.05`** (224/224 entries,
> fitted on the `q ≥ 41` rungs; `1.41 … 2.51` if the coarse `q = 11, 21` rungs are included), at both strip
> points (`s = 0.25 + 7.0674i` and `s = 0.35 + 17i`), at both ends of the Markov system, and for
> every Taylor index pair tested — measured over the doubling ladder `q = 11, 21, 41, 81, 161, 321`.
> The rate matches `2 − λ_q = π²/q²` exactly. This is the entry-level content of A2 (the skeleton's
> `UNKNOWN` modulus of convergence) and it is now a number — **and it independently reproduces, at
> `Re s = ¼`, the `q^{−2}` that `LAW_T2_DETERMINANT` §4 measured on `Re s > 1` through a completely
> different representation (the truncated Selberg Euler product).** Two representations, two
> half-planes, one exponent. That cross-check is the most useful thing this lane produced.
>
> **(F1) The `(m,j)`-ENVELOPE FAILS. `MEASURED`, pre-registered as a KILL condition.**
> The entry *difference* decays geometrically in `m+k` only on the diagonal-ish blocks
> (`r = 0.25 … 0.62`). On the single-branch off-diagonal blocks `L_1 : g_i ← g_{i−2}` it **does not
> decay at all**: `r = 1.115` and `r = 1.156` at `s₁`, `r = 1.044 / 1.166 / 1.164` at `s₂`. This is
> `LAW_B5J_JENSEN` §3.2's `θ = 1` reappearing at the level of *differences*: the Markov images touch
> the target cell boundary, so `sup|(h(z)−c_j)/ρ_j| = 1` and the normalised monomial basis does not
> damp the input Taylor index. The pre-registered rule says **KILL** on this alone.
>
> **(F2) There is NO fixed-dimension `θ`-limit matrix. `PROVED-here` (from the builder) + `MEASURED`.**
> `κ(q) = q − 2` for odd `q`, so the matrix side is `κN` and **grows linearly in `q`**
> (`48 → 5104` for `q = 5 → 321` at `N = 16`). The Markov partition of `[−λ_q/2, 0]` does converge —
> but to the **countably infinite** `λ = 2` partition with points `−n/(n+1)` accumulating at the
> parabolic fixed point `−1`, and the first cell collapses at exactly `(2 − λ_q)/2 = π²/(2q²)`
> (verified to 4 s.f. at `q = 321`: `4.78913e−5` vs `4.78916e−5`). The brief's step-1 suggestion —
> "the `λ = 2` specialisation may BE the θ-operator" — is **not available**: `λ = 2` in this builder
> is `q = ∞`, i.e. `κ = ∞`. **Entry-wise convergence therefore only makes sense in RIGHT-indexing**
> (`i′ = κ − i`), which is what was measured; it is a semi-infinite limit, not a matrix.
>
> **(F3) The determinant does NOT converge. `MEASURED`, and it is the decisive one.**
> `|det(1 − L_{s,+})|` at `s = 0.25 + 7.0674i` runs `1.2992, 0.5964, 0.19705, 0.08540, 0.025294`
> for `q = 11, 21, 41, 81, 161` — a clean **`q^{−1.46}` decay to zero** (`R² = 0.996`), not a
> limit. Confirmed *not* a
> truncation artefact: at `q = 41` the per-component truncation `d = 12/16/20` gives
> `0.19705 / 0.19701 / 0.19701` (5-digit stable). And the MMS denominator does not rescue it:
> `|det(1 − K_s)| = 1.0188` at `q = 41` and `→ 1` (since `b_q → 0`), so the same decay is on `Z_S`
> in this representation. **Entry-wise `q^{−2}` does not transport to the determinant, because the
> determinant is taken over a matrix whose dimension grows with `q`.** Each increment `q → q+2`
> adds a whole `N × N` block row/column; `α = 2` per entry against `κ = q − 2` blocks is exactly the
> `Ω(q)`-many-factors trade that `LAW_B5J_JENSEN` §3.3 priced at `Ω(q³)` for norms — here it shows
> up as a *drift*, not a blow-up, but a drift is equally fatal to Rouché.
>
> **What this means for the lane.** The brief's hoped-for bypass ("Rouché needs only boundary
> values, so entries suffice") is **false as stated**: boundary values of *what*? There is no
> `det(1 − M_∞)` on the same contour to compare against. The `Ω(q³)` operator-norm obstruction was
> not evaded; it was re-encountered in the dimension count. **The MMS reduced representation is the
> wrong vehicle for a `q → ∞` comparison, for a structural reason** (§2), and any future U1-eff
> attempt through transfer operators must first fix the dimension — which is `LAW_B5J_JENSEN`
> §6 item 2 (induce / accelerate), unchanged and now with one more reason behind it.
>
> **What is banked (worth keeping).** **Lemma E (§3, `MEASURED` with an exact conjectured rate):**
> in right-indexing, every matrix entry of the MMS reduced operator converges as
> `|M_q[·] − M_∞[·]| = C·q^{−2}(1 + o(1))`, uniformly over the tested index window and over both
> ends of the Markov system, and never *worse* for large Taylor indices (on the coarse rungs `α`
> even rises to `≈ 2.4` there; on `q ≥ 41` it is flat at `2.00`). Together
> with Lemma H (`|ζ(2s+m+j, a₀)| ≤ 0.94`, `q`-uniform) this says: **the analytic and the `q`-limit
> behaviour of the entries are both under explicit control. Only the geometry — `θ = 1` and
> `κ = q − 2` — is not.** That is now the whole of the obstruction, stated twice from two
> independent directions.

---

## 1. Pre-registration (fixed before any measurement)

Taken verbatim from the lane brief, recorded here **before** the probes were run; `u1eff_geom.py`
(step 0) was the first thing executed after this section was fixed.

> **Hypothesis.** The entry-wise difference between the `q`-transfer-operator matrix and its
> `θ`-limit matrix decays like `q^{−2}` uniformly with the same geometric `(m,j)`-envelope, so the
> determinant difference on a fixed contour decays like `C·q^{−2}`, giving U1-eff by entries.
>
> **ADVANCES** if `α ≥ 1.5` entry-wise **AND** the determinant difference shows the same (or better)
> exponent with a stable constant.
> **KILL** if `α < 1` **OR** the envelope fails (entries with large `(m,j)` decaying slower in `q`).
> **MIXED** otherwise.

**Outcome, scored mechanically:** `α = 2.00 ± 0.05` (passes the ADVANCES half), the **envelope fails**
(triggers the explicit KILL clause), and the determinant does not converge at all, so the ADVANCES
conjunction is not met. **Verdict: KILL.** §7 records the single sub-claim that survives.

Two honest notes on the envelope clause. Its literal wording is *"entries with large `(m,j)`
decaying slower in `q`"*; measured, the large-`(m,j)` entries decay **faster** in `q`
(block `R0,0` at `s₁`, whole-ladder fit: `α: 1.991 → 2.047 → 2.107 → 2.165` as
`(m,k): (0,0) → (1,1) → (3,3) → (5,5)`). What fails is the other reading of the same clause —
the geometric factor `r^{m+j}` that makes the envelope summable, i.e. `N`-uniform. Both readings are
reported (§3 for the first, §4 for the second) so the scoring is not a matter of interpretation.
And the KILL would stand on §5 (determinant) with no reference to the envelope at all.

---

## 2. Step 1 — what the `θ`-limit object actually is `[the structural finding]`

### 2.1 The builder is parameterised by `q`, not by `λ`

`zeta_cert_rosen.build_reduced_matrix_ball(s, N, sign, q)` derives everything from `q`:
`h_q = (q−3)/2`, `κ = 2h_q + 1 = q − 2`, `λ_q = 2cos(π/q)`, and the Markov partition of
`[−λ_q/2, 0]` from the `λ_q`-continued-fraction values `[[0; 1^{h−i} 2 1^h]]` and `[[0; 1^{h−i}]]`.
The matrix is `κN × κN`. **There is no `λ`-only knob**: setting `λ = 2` means `q = ∞` means
`κ = ∞`. The brief's step-1 fallback ("use `λ = 2` in the same builder") is not executable.

### 2.2 The partition does converge — to a countably infinite one `[MEASURED]`

`u1eff_geom.json`, all figures at `safety = 5/2` as in the certified builders:

| `q` | `κ` | `dim` (`N=16`) | `2 − λ_q` | `π²/q²` | `width_min` | `ρ_min` | `ρ_max` | `ρ_max/ρ_min` |
|---|---|---|---|---|---|---|---|---|
| 5 | 3 | 48 | 0.381966 | 0.394784 | 0.190983 | 0.238729 | 0.477458 | 2.00 |
| 9 | 7 | 112 | 0.120615 | 0.121847 | 0.060307 | 0.075384 | 0.434120 | 5.76 |
| 21 | 19 | 304 | 0.0223383 | 0.0223801 | 0.0111692 | 0.0139615 | 0.419792 | 30.1 |
| 41 | 39 | 624 | 0.00586840 | 0.00587127 | 0.00293420 | 0.00366775 | 0.417483 | 113.8 |
| 81 | 79 | 1264 | 0.00150409 | 0.00150428 | 0.000752047 | 0.000940059 | 0.416876 | 443.5 |
| 161 | 159 | 2544 | 0.000380745 | 0.000380757 | 0.000190373 | 0.000237966 | 0.416720 | 1751 |
| 321 | 319 | 5104 | 9.57825e−5 | 9.57833e−5 | 4.78913e−5 | 5.98641e−5 | 0.416680 | 6960 |

> ### **The second partition point is exactly `φ_1 = 1 − λ_q`** (verified to double-precision
> equality, `|φ_1 − (1−λ_q)| ≤ 1.2e−16`, at **all ten** `q` in the table), hence
> ### **`width_min = φ_1 + λ_q/2 = (2 − λ_q)/2 = π²/(2q²) + O(q⁻⁴)` and `ρ_min = (5/4)·width_min`.**
> `MEASURED` (the identity `φ_1 = 1 − λ_q` is exact in the data and is presumably a CF identity for
> the Rosen word used by `partition_points_ball`; **no proof is given here**). The `π²/(2q²)` form is
> then immediate from `2 − λ_q = π²/q² + O(q⁻⁴)` (`LAW_T2_DETERMINANT` §3.4).

Meanwhile the partition points at the **other** end are stationary: for `q = 41, 81, 161, 321` the
last four are `−0.60236 / −0.50147 / −0.33399 / 0`, `−0.60060 / −0.50038 / −0.33350 / 0`,
`−0.60015 / −0.50010 / −0.33338 / 0`, `−0.60004 / −0.50002 / −0.33334 / 0` — converging to
**`−3/5, −1/2, −1/3, 0`**, i.e. to `−n/(n+1)`, the `λ = 2` Rosen/Hurwitz partition.

> ### **The `θ`-limit of the MMS Markov system is the countably infinite partition
> `{−n/(n+1)}_{n≥0}` of `[−1, 0]`, accumulating at the parabolic fixed point `−1` of the `λ = 2`
> map.** `MEASURED` (4 s.f. at `q = 321`), and structurally forced: `x = −1/(2+x) ⇒ x = −1`.

This is the same phenomenon `LAW_B5J_JENSEN` §3.3 measured as `1 − sup|h′| = π²/q²` — the elliptic
point opening into a cusp — seen now in the *partition* rather than in the derivative. The limit
system has an **indifferent fixed point**, so the limiting transfer operator is not of the
finite-block nuclear type the builder realises. **Identification of `M_∞` with any concrete
`Γ_θ` evaluator is therefore left as an open assumption; no transfer-operator one exists in the
repo** (checked: `.worktrees/aletheia-restore/code/` has `zeta_cert_q3 / zeta_cert_rosen{,_even,_q5}
/ zeta_mayer{,_rosen}` and no `Γ_θ` operator; `det_K` and the `q = 3` scalar path are different
objects). The repo's one `Γ_θ` evaluator, `law_probes/probe_t2_shape.py`, is a **truncated Selberg
Euler product** over the `λ = 2` group ball — a different representation, valid on `Re s > 1`, which
is exactly the region `LAW_T2_DETERMINANT` §4 used to measure `|Z_q − Z_θ| ∝ q^{−2}`
(fits `−2.10 / −2.15 / −2.18`). **Lemma E (§3) reproduces that same `q^{−2}` at `Re s = 0.25` and
`0.35`, entrywise, in a completely independent representation** — a genuine cross-check of A2's rate
inside the strip, and the most useful by-product of this lane.

### 2.3 The only index scheme in which entries can converge

Since the collapsing cells accumulate at the **left** end (index `1, 2, 3, …` in the builder's
ascending order) and the stationary cells sit at the **right** end, entry-wise convergence can only
be posed in **right-indexing** `i′ = κ − i`, `j′ = κ − j`. Everything in §§3–4 uses that.
Two features make it well-posed: the MMS eq.(34) block structure is `g_i ← g_{i−2}` plus two
"global" columns `g_{2h} = g_{κ−1}` (`j′ = 1`) and `g_k = g_κ` (`j′ = 0`), all of which are
`q`-independent in right-indexing; and the special rows `i = 1, 2` sit at the collapsing end.

---

## 3. Entry-wise convergence — the exponent `α` `[MEASURED; this is Lemma E]`

`u1eff_entries.py`: `N = 12`, `n_head = 4`, `sign = +1`, `q ∈ {11, 21, 41, 81, 161, 321}`,
two strip points. For each tracked entry `E(q)`, `α` is fitted two ways — `α_succ` from the
successive differences `|E(2q±) − E(q)|` (proxy-free) and `α_proxy` from `|E(q) − E(321)|`.
They agree to `≈ 0.1`.

### 3.1 Right-indexed entries, `s₁ = 0.25 + 7.0674i`

| block `(i′,j′)` | `(m,k)` | `|E(321)|` | successive diffs `q = 11 → 161` | `α_succ` |
|---|---|---|---|---|
| (0,0) | (0,0) | 1.21860 | 0.522, 0.145, 0.0382, 0.00981, 0.00249 | **1.991** |
| (0,0) | (1,1) | 0.202817 | 0.105, 0.0266, 0.00686, 0.00175, 0.000444 | **2.047** |
| (0,0) | (3,3) | 0.0066365 | 0.00452, 0.00104, 0.000262, 6.66e−5, 1.68e−5 | **2.107** |
| (0,0) | (5,5) | 0.000168779 | 1.53e−4, 3.23e−5, 7.91e−6, 2.00e−6, 5.03e−7 | **2.165** |
| (0,1) | (0,0) | 0.679380 | 0.252, 0.0696, 0.0183, 0.00471, 0.00119 | **1.994** |
| (1,0) | (1,0) | 0.966786 | 0.491, 0.127, 0.0327, 0.00836, 0.00212 | **2.037** |
| (1,1) | (1,1) | 0.110302 | 0.0241, 0.00657, 0.00173, 4.44e−4, 1.12e−4 | **2.001** |
| (2,0) | (5,5) | 2.06298e−6 | 4.82e−6, 7.41e−7, 1.67e−7, 4.13e−8, 1.04e−8 | **2.366** |
| (3,0) | (5,5) | 3.87865e−7 | 1.57e−6, 1.91e−7, 4.08e−8, 9.92e−9, 2.48e−9 | **2.510** |
| (3,1) | (0,0) | 0.616242 | 0.094, 0.028, 0.00751, 0.00194, 4.92e−4 | **1.946** |

**All 70 tracked right-indexed entries at `s₁`: `α_succ ∈ [1.946, 2.510]`, median `2.043`.**
**All 70 at `s₂`: `α_succ ∈ [1.410, 2.493]`, median `2.014`.** Three entries there fall below `1.9`
(`1.410, 1.577, 1.797`, all in block `R3,0`); in each the low fit comes from the **first** rung
(`q = 11 → 21`) being anomalously flat — e.g. `R3,0|(1,0)` has successive differences
`0.0679, 0.0577, 0.0171, 0.00450, 0.00115`, whose last three rungs give ratios `0.263, 0.256`, i.e.
`α ≈ 1.94` asymptotically. Restricting every fit to `q ≥ 41` leaves no value below `1.9` at either
point. **On the `q ≥ 41` rungs alone the measurement is far sharper: over all 224 tracked entries
(both points, both index ends), every finite `α` is either in `[1.957, 2.049]` (median `2.000`) or
one of the exact multiples `4, 6, 8, 10, 12` explained in §3.2.** That is the real content of
Lemma E: `α = 2`, to two decimals, with no exceptions.

### 3.2 The collapsing end, and the block sup

Rows `i = 1, 2, 3` (the cells shrinking into `−λ_q/2`) converge too, at the same rate — and rows
`2` and `3` converge to a **common** limit (`|E| = 0.577371` vs `0.577376`; `1.43569` vs `1.43572`),
which is the semi-infinite shift structure of §2.3 showing up numerically:

| entry | `|E(321)|` | `α_succ` |
|---|---|---|
| `L1,k \| (0,0)` | 0.888086 | 1.997 |
| `L2,k \| (0,0)` | 1.43569 | 2.000 |
| `L3,k \| (0,0)` | 1.43572 | 1.993 |
| `L2,k−1 \| (0,1)` | 0.230912 | 1.961 |
| `L1,k−1 \| (1,0)` | 3.69789e−8 | 4.041 |
| `L1,k−1 \| (3,3)` | 1.00501e−16 | 8.012 |
| `L1,k−1 \| (5,5)` | 3.52184e−25 | 12.009 |

The `α = 4, 6, 8, 12` rows are not anomalies: those entries have limit **`0`** (see the `|E(321)|`
column — `1e−8` down to `3.5e−25`) and vanish at an **exact even multiple of `2`**, which is what
carrying an explicit power of the collapsing radius `ρ_1 ∝ q^{−2}` produces. Measured multiples
across the collapsing rows: `4, 6, 8, 10, 12` — always exactly `2k` to three decimals
(e.g. `4.041, 6.015, 8.012, 10.051, 12.009`). **Which power appears for which `(m,k)` is not derived
here** (the observed pattern is not a simple function of `m ∧ k`), only that it is an even multiple.

Per-row sup over the whole matrix (`block_sup`), same ladder:

| row | `sup|entry|` at `q=321`, `s₁` | `α_succ` | `s₂` sup | `s₂ α_succ` |
|---|---|---|---|---|
| `R0` (rightmost cell) | 5.94039 | 2.170 | 245.829 | 2.247 |
| `R1` | 1.87780 | 2.071 | 13.3802 | 2.235 |
| `R3` | 0.887983 | 2.090 | 1.84613 | 2.197 |
| `R5` | 1.08878 | 1.937 | 1.05160 | 2.256 |
| `L1` (collapsing) | 1.15473 | 1.830 | 1.37058 | 1.853 |
| `L2` | 1.43569 | 1.633 | 1.61014 | 2.255 |

Global max entry converges cleanly: `s₁`: `7.726, 6.308, 6.033, 5.963, 5.945, 5.940`;
`s₂`: `455.1, 287.5, 255.5, 248.2, 246.3, 245.8`.

> ### **Lemma E (`MEASURED`, `q = 11 … 321`, two strip points, both parities of index-end).**
> In right-indexing, `|M_q[i′,j′][m,k] − M_∞[i′,j′][m,k]| = C_{i′j′mk}·q^{−α}` with
> **`α = 2.00 ± 0.05` on the `q ≥ 41` rungs (224/224 tracked entries; `α = 2.0 ± 0.15` fitting the
> whole ladder from `q = 11`)**, and over the whole ladder `α` **increases** with `m + k`
> (to `≈ 2.4`) rather than degrading.
> The rate is the geometric rate `2 − λ_q = π²/q²`, as expected from `∂/∂λ` of the entries.

This is the entry-level, measured form of the skeleton's `UNKNOWN` step **A2**, and it is the
positive result of this lane.

### 3.3 Warning sign already visible: column norms

At `s₁` the maximum column `ℓ²`-norm **grows**: `12.51 (q=81), 17.95 (161), 25.57 (321)` — a fitted
`q^{0.52}`, i.e. `√κ`. Structurally forced: the columns `j = κ` and `j = κ−1` receive an `Linf`
contribution from **every** row (MMS eq.(34)), so their norm is `Θ(√κ)` with `O(1)` entries. This is
`LAW_B5J_JENSEN` §3.1's diverging Hadamard bound, re-derived: bounded entries + growing dimension.
It is the first sign that §5 was going to fail. (At `s₂` the max column norm converges — `510, 505.8,
504.8` — because there the mass is concentrated in one block; the `s₁` behaviour is the generic one
for the deep strip.)

---

## 4. The `(m,j)`-envelope — `FAILS` `[MEASURED; pre-registered KILL condition]`

`u1eff_envelope.py` fits, per block, the geometric ratio `r` of the entry **difference** in the
Taylor-index sum `m+k` (using the `q = 161 → 321` successive difference as the `|M_q − M_∞|` proxy).
The hypothesis needs `r < 1` for *every* block, or the envelope is not summable over `N`.

| block `(i′,j′)` | `r` at `s₁ = 0.25+7.0674i` | `r` at `s₂ = 0.35+17i` |
|---|---|---|
| (0,0) | 0.4465 | 0.6176 |
| (0,1) | 0.8867 | **1.0435** |
| **(0,2)** | **1.1146** | **1.1660** |
| (1,0) | 0.3749 | 0.4809 |
| (1,1) | 0.4420 | 0.4649 |
| **(1,3)** | **1.1559** | **1.1635** |
| (2,0) | 0.3037 | 0.4174 |
| (2,1) | 0.3970 | 0.4383 |
| (3,0) | 0.2547 | 0.3735 |
| (3,1) | 0.3489 | 0.3981 |

> ### **The envelope fails exactly on the `L_1` single-branch blocks `g_i ← g_{i−2}`** — the blocks
> with `j′ = i′ + 2` — where `r > 1.11` at both heights. Directly visible in the raw differences:
> block `(1,3)` at `s₁`, `q = 161 → 321`, gives `(m,k) = (0,0): 2.39e−3` and
> `(5,5): 2.10e−3` — essentially **no decay across ten Taylor orders**.

**Why, and why it is not fixable here.** `LAW_B5J_JENSEN` §3.2 proves `θ := sup_{z∈D_i}
|(h_n(z) − c_j)/ρ_j| ≥ 1` with equality exactly at `safety = 1`, because the Rosen–Nakada partition
is **Markov**: each branch image is a union of cells, so it *touches* the target cell boundary. The
column-`k` entries are the Taylor coefficients of `weight(z)·((h(z)−c_j)/ρ_j)^k`, bounded by
`‖weight‖_∞ θ^k` and no better. `θ = 1` on the `L_1` blocks ⇒ `r = 1` for the entries **and** for
their `q`-differences. That the measured `r` slightly exceeds `1` is the `safety = 5/2` inflation
(§3.2 of the parent: `θ_max = 1.29 … 1.42` at that safety).

`PROVED-here` given the parent's `θ` result; `MEASURED` as stated. **This is the pre-registered KILL
trigger, and it is the *same* obstruction the operator-norm routes hit — not a new one.** The brief's
premise that entries would "bypass the operator-norm obstruction" is therefore `REFUTED-here` at
this level too: the obstruction is in the *basis geometry*, which entries and norms share.

---

## 5. The determinant — no limit at all `[MEASURED; the decisive negative]`

`u1eff_det.py`, `s₁ = 0.25 + 7.0674i`, `sign = +1`, `N = 12`, per-component truncation `d = 12`:

| `q` | `κ` | `dim = κd` | `det(1 − L_{s,+})` | `|det|` | `ln|det|` |
|---|---|---|---|---|---|
| 11 | 9 | 108 | `−0.80185 − 1.02224 i` | 1.29921 | +0.2618 |
| 21 | 19 | 228 | `+0.18652 + 0.56650 i` | 0.596418 | −0.5167 |
| 41 | 39 | 468 | `−0.16271 − 0.11115 i` | 0.197046 | −1.6244 |
| 81 | 79 | 948 | `+0.06896 + 0.05036 i` | 0.0853970 | −2.4603 |
| 161 | 159 | 1908 | `−0.024865 − 0.0046360 i` | 0.0252935 | −3.6772 |

> ### **Least squares on `ln|det| = c − α_det ln q` gives `α_det = 1.463`, `R² = 0.996`** (local
> slopes `1.204, 1.655, 1.228, 1.771` — no sign of flattening).
> `|det(1 − L_{s,+})| → 0` like `q^{−1.46}`. **There is no limit value to compare against, so there
> is no determinant difference, so there is no Rouché.** The argument of `det` also rotates by
> `≈ ±π` per doubling (`arg = −2.238, +1.253, −2.539, +0.631, −2.958`), so the failure is not a
> modulus artefact.

**Three controls, all run, all negative for the hypothesis.**

1. **Not a dimension-truncation artefact.** `u1eff_dconv.py` at `q = 41`, `N = 20`:
   `d = 8/12/16/20 → |det| = 0.194687 / 0.197046 / 0.197012 / 0.1970123` — **stable to 5 digits from
   `d = 12`**; and at `q = 81`, `N = 20`:
   `d = 8/12/16/20 → 0.0858230 / 0.0853970 / 0.0854055 / 0.0854054`, stable
   to 5 digits. Separately at `q = 11, 21` with `N = 28`, `d` up to 28: `1.29900` and `0.596526`,
   flat from `d = 16`. The `q`-trend is real, at both ends of the ladder.
2. **Not the MMS denominator.** `det(1 − K_s) = ∏_{n≥0}(1 − b_q^{s+n})` with `b_q → 0`, so it
   `→ 1`; measured `|det(1 − K_{s₁})| = 1.01883` at `q = 41` and `1.00159` at `q = 81`, i.e. it is
   converging to `1` fast, so it cannot cancel a `q^{−1.46}`. The decay is on `Z_S` in this
   representation, not an artefact of using the numerator.
3. **Not `t₀`-specific in the entry data.** Both heights give the same `α ≈ 2` and the same envelope
   failure. (The determinant ladder itself was run only at `s₁`; at `s₂` the `N`-convergence is
   slower — `d = 8/12/16/20/24/28 → 178, 9.80, 10.59, 10.93, 10.926, 10.9259` at `q = 21` — so an
   honest `s₂` determinant ladder needs `N ≳ 24`. At the under-converged `d = 12` the `s₂` ladder
   reads `6.41, 9.80, 34.91, 71.53, 104.50` for `q = 11, 21, 41, 81, 161`: **also no limit, and in the opposite
   direction (growing)**. Consistent with the verdict, but not evidence-grade — recorded as
   under-probed, and not used in the ledger.)

**The arithmetic of why entries winning does not make determinants win.** A determinant of a
`κd × κd` matrix is a sum over `(κd)!` permutations; perturbing each entry by `ε = C q^{−2}` moves
the determinant by `O(‖·‖^{κd−1} · κd · ε)` at best. With `κd = Θ(q)`, `q^{−2}` per entry against
`Θ(q)` factors is a wash *at best* — and here the two matrices being compared do not even have the
same size, so the comparison is not "a perturbation" at all: it is `q → q+2` **adding a block row
and column**. That is the honest content of `LAW_B5J_JENSEN` §3.3's `log M = Ω(κ/(1−θ)) = Ω(q³)`,
restated for differences rather than for sups. **The operator-norm obstruction was not bypassed.**

---

## 6. Status ledger

| # | Step | Statement | Status |
|---|---|---|---|
| G1 | `κ(q) = q − 2` (odd `q`); matrix side `κN` | dim `48 → 5104` for `q = 5 → 321`, `N=16` | `PROVED-here` (from the builder) |
| G2 | first-cell collapse | `φ_1 = 1 − λ_q` exactly (`≤1.2e−16`, ten `q`), so `width_min = (2−λ_q)/2 = π²/(2q²)+O(q⁻⁴)` | `MEASURED` (identity), `PROVED-cited` (the `π²/q²` expansion, T2 §3.4) |
| G3 | `θ`-limit partition | `{−n/(n+1)}` on `[−1,0]`, accumulating at the parabolic point `−1`; countably infinite | `MEASURED` (4 s.f.) |
| G4 | no `λ=2` specialisation of the builder | `λ = 2 ⟺ q = ∞ ⟺ κ = ∞`; no `Γ_θ` *transfer-operator* evaluator in the repo (only the `Re s>1` Euler product `probe_t2_shape.py`) | `PROVED-here` |
| **E** | **entry-wise convergence** | `α_succ ∈ [1.957, 2.049]`, median `2.000`, on `q ≥ 41` rungs, 224/224 entries, both `s`, both index ends (`[1.41, 2.51]` fitting from `q=11`) | **`MEASURED`** (`q = 11…321`) |
| E2 | rate identification | `α = 2` matches `2 − λ_q = π²/q²` | `MEASURED`; derivation `GAP` (needs `∂_λ` of the entry formulas) |
| E4 | **independent cross-check of A2's rate** | entrywise `q^{−2}` at `Re s = 0.25, 0.35` (transfer operator) reproduces `LAW_T2_DETERMINANT` §4's `|Z_q − Z_θ| ∝ q^{−2}` measured at `Re s > 1` (Euler product) — different representation, different half-plane, same exponent | `MEASURED` (both sides) |
| E3 | collapsing-end entries | rows `i=2,3` share a limit; entries carrying powers of `ρ_1 ∝ q^{−2}` have limit `0` and vanish at exact even `α = 4,6,8,10,12` | `MEASURED`; which power for which `(m,k)` is `GAP` |
| **F-env** | **`(m,j)`-envelope fails** | `r = 1.115 / 1.156` (`s₁`), `1.044 / 1.166 / 1.164` (`s₂`) on the `L_1` blocks | **`MEASURED`** + `PROVED-here` given B5-J §3.2 (`θ ≥ 1`, Markov) |
| F-col | column norms grow | `max ‖Me_j‖₂ ∝ q^{0.52}` at `s₁` | `MEASURED` |
| **F-det** | **determinant does not converge** | `|det(1−L_{s₁,+})| = 1.2992 / 0.5964 / 0.19705 / 0.08540 / 0.025294` at `q=11/21/41/81/161`; `∝ q^{−1.463}`, `R²=0.996` | **`MEASURED`**, `d`- and `K`-controlled |
| F-det2 | not a truncation artefact | `q=41`, `d=12/16/20`: `0.19705/0.19701/0.19701`; `q=81`, `d=12/16/20`: `0.085397/0.085406/0.085405` | `MEASURED` |
| F-det3 | denominator does not rescue | `|det(1−K_{s₁})| = 1.01883` (`q=41`), `1.00159` (`q=81`), `→1` as `b_q → 0` | `MEASURED` + `PROVED-cited` (MMS) |
| **V** | **verdict vs pre-registration** | envelope clause fires; ADVANCES conjunction unmet | **KILL** |

---

## 7. What survives, and what it would take `[honest proof-chain accounting]`

The hypothesis is dead **as a route to U1-eff through `det(1 − L_s)`**. One link of the intended
chain is nonetheless now measured, and one is newly ruled out. Stating both, with what each needs:

| link | intended obligation | status after this note |
|---|---|---|
| **1. entry difference bound** | `|M_q[·] − M_∞[·]| ≤ C q^{−2}·(envelope)`, from `∂/∂λ` of the explicit Hurwitz expressions bounded by Lemma-H technique | **the `q^{−2}` half is `MEASURED` (Lemma E); the envelope half is `REFUTED` (§4).** The `∂_λ` derivation is genuinely **Aristotle-able per entry**: each entry is `λ^{−(2s+m)}ζ(2s+m+j, a₀(λ))` times binomial constants, `a₀ = n₀ ± c_i/λ`, and `d/da ζ(t,a) = −t ζ(t+1,a)`, so `∂_λ` is another Hurwitz value with the same Lemma-H majorant. **Recommended as a standalone finite formalisation task** — it is small, self-contained, and it upgrades Lemma E from `MEASURED` to `PROVED`. But see the caveat below. |
| **2. truncation tail** | Lemma H (`≤ 0.94`, decay `≈ 6^{−(m+j)}`) closes the `N`-tail `q`-uniformly | **unchanged and still good** — but it bounds the tail of *one* matrix, not the difference of two of different sizes. |
| **3. det continuity** | finite-dim continuity + tail ⇒ `|det(1−M_q) − det(1−M_∞)| ≤ C q^{−2}` | **`REFUTED-here` (§5).** No `M_∞` of finite dimension exists (§2); the measured determinant decays to `0` like `q^{−1.46}`. This link cannot be repaired within the MMS reduced representation. |
| **4. Rouché vs `Γ_θ`'s zero/pole set** | compare on `∂D(s_∞, r)`, `s_∞ = ρ₁/2` | **unreachable**: link 3 supplies no comparison function. Also still gated on **U3** (`LAW_U3_TRANSPORT`) independently. |

**The caveat on recommending link 1.** Proving Lemma E rigorously buys a bound on *entries of a
matrix whose size is `Θ(q)`*, in a basis where the relevant blocks have `θ = 1`. On the evidence of
§§4–5 that is not on any path to U1-eff. **Do the `∂_λ` piece only if a fixed-dimension
representation is found first** — otherwise it is a clean lemma with no consumer.

**Where U1-eff should go next, given this.** Unchanged from `LAW_B5J_JENSEN` §6 item 2, now with an
independent second reason: **fix the dimension before comparing.** The `κ = q − 2` growth and the
`θ = 1` neutrality are the same fact (Markov cells shrinking into the forming cusp), and any
transfer-operator route to a `q → ∞` comparison must first pass to an **induced / accelerated**
system whose branch count and contraction are `q`-uniform, then show its determinant relates to
`det(1 − L_s)` cleanly. Fedosova arXiv:2509.17936 remains the literature item to read before
attempting it. Nothing in this note supports trying U1-eff through the MMS reduced matrix again.

**And the cheaper board item is untouched.** `LAW_SH_EFFECTIVIZATION_SKELETON` §7 item 1
(B-measure: certified winding deep-pole counts) and `LAW_B5J_JENSEN` §6 item 4 remain the lane's
top-ranked work; this note removes one more competitor from above them.

---

## 8. What this document claims, and does not

**Claims.** (i) The pre-registered entry-wise hypothesis **KILLs**, on its own stated envelope
clause and, independently and more decisively, on the determinant step. (ii) `κ(q) = q − 2` means no
fixed-dimension `θ`-limit matrix exists in the MMS reduced representation, and the `λ = 2`
specialisation suggested in the brief is not executable in this builder. (iii) The `θ`-limit Markov
system is the countably infinite `{−n/(n+1)}` partition with an indifferent fixed point at `−1`.
(iv) **Lemma E**: entries converge at `α = 2.00 ± 0.05` (`q ≥ 41` rungs, 224/224 tracked entries),
uniformly over the tested window and both ends, never degrading for large Taylor indices — and this
independently reproduces, inside the strip, the `q^{−2}` that T2 §4 measured on `Re s > 1` in the
Euler-product representation. (v) The envelope failure is the *same* `θ = 1` obstruction as
the operator-norm routes, so "entries bypass the norm obstruction" is false.

**Does not claim.** That `α = 2` exactly (measured `2.00 ± 0.05`; the `∂_λ` derivation is `GAP`).
That `|det| ∝ q^{−1.46}` is a law — five points, one height, `sign = +1` only, and the local slopes
range `1.20 … 1.77` with no flattening; what is claimed is only that the determinant **has no limit
and drifts to 0**.
That the `−` sector behaves identically (not run). Anything at `s₂ = 0.35 + 17i` about
determinants: the `N`-convergence there needs `N ≳ 24` and no ladder was run. Any rigorous
(ball-certified) status: **all figures are Arb ball midpoints with no certified dimension tail**.
That `M_∞` is the `Γ_θ` transfer operator — no `Γ_θ` evaluator exists in the repo and the
identification is stated as an **open assumption** (§2.2), though the partition-point convergence to
`−n/(n+1)` is strong evidence for the `λ = 2` Rosen map as the limit dynamics. That any of this
bears on the flagship `G_5` theorem or on the `Q₀ = 1465` of `LAW_ROUTEB_CONDITIONAL_THEOREM` —
both are untouched.

---

**Probes.** `law_probes/u1eff_geom.py → u1eff_geom.json`;
`u1eff_entries.py → u1eff_entries.json`; `u1eff_fit.py → u1eff_fit.json`;
`u1eff_envelope.py → u1eff_envelope.json`; `u1eff_det.py → u1eff_det.json` + `u1eff_det_big.log`;
`u1eff_dconv.py → u1eff_dconv.json` + `u1eff_dconv.log`.
Interpreter `/Users/za/.venvs/farey-rh/bin/python` (python-flint 0.9.0 / Arb, 300-bit); evaluator
`.worktrees/aletheia-restore/code/zeta_cert_rosen.py` (`build_reduced_matrix_ball`, `_det_block`,
`det_K`), `n_head = 4`, `sign = +1`, `N = 12` (entries and the determinant ladder), `N = 20/28`
(truncation controls). Strip points `s₁ = 0.25 + 7.0674i`, `s₂ = 0.35 + 17i`.
No existing file was modified; the only git invocation was a read-only `git status --porcelain`.

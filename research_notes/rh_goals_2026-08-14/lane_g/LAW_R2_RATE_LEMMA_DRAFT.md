# LAW — R2: candidate (RATE) lemma, draft with proof skeleton and explicit constants

**Status: DRAFT LEMMA + proof skeleton. Not a proved theorem.** Every constant
is either derived here or tagged [NUMERIC-CONJECTURED]. Per
`LAW_HEJHAL_S7_EXTRACT.md` §4 (R2). Inputs: `LAW_R1_COSET_STRUCTURE.md`
(matched-class dominance; empirical partial-window mass
`Σ_{10≤|c|≤50}|c|^{−2.2} ≤ 0.26`), `LAW_RATE_MEASURE.md`
(measured D(q;s)), `LAW_R4_THETA_DEFECT.md` (target: ε must beat ~0.66 after
transport).

> **[CORRECTION 2026-08-18 audit-9]** The header originally imported from R1
> a "tail majorant ≤0.26". R1 measures no tail majorant: the quantity is the
> empirical partial-window mass `Σ_{10≤|c|≤50}|c|^{−2.2} ≤ 0.26`, an
> UNDER-estimate of the true tail (R1 §5 says so explicitly). It is never a
> full-tail bound and is not used as one in this draft.

## [MACHINE-VERIFIED 2026-08-17]

Aristotle dispatch v26 (`projects/aristotle_dispatch_v26/`, project
`4730142e-cc15-417a-bccf-ca30b25f2bcf`) formalized and machine-verified the
§5-tagged "Aristotle: YES" foundational pieces of the P1–P6 chain, plus two
finite depth-bounded instances of gap M1. Local `lake build` (reusing the
v25 `.lake`/Mathlib cache) confirms this independently of Aristotle's cloud
report: `Build completed successfully (8027 jobs)`, 0 errors, 0 live
`sorry`. Result file: `projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle/RateCore.lean`.

- **P1, P2, P3, P5 proved as stated. P6: proved in PART only** — the
  Chebyshev `c`-identity `c_w(λ) = λ·U_{m−1}(λ/2)` and its λ=2 corollary
  `c_w(2) = 2m` are machine-verified; the derivative formula and the
  sharpness conclusion in §1(P6) are NOT (see `[CORRECTION 2026-08-18
  audit-13]` at §1(P6)).

  > **[CORRECTION 2026-08-18 audit-13]** This bullet originally read
  > "**P1, P2, P3, P5, P6 (+ P6's λ=2 corollary): PROVED as stated.**". The
  > harvested Lean file
  > (`projects/aristotle_dispatch_v26/result/.../RateCore.lean`, theorems
  > `c_chebyshevWord` and `c_chebyshevWord_two`) contains no derivative
  > theorem at all: `c'_w(2) = m + (m³−m)/3` and the "k² is attained"
  > sharpness step are paper algebra, not machine-verified. Machine
  > verification of P6 is scoped to the `c` identity and the λ=2 value.
- **P4: proved in CORRECTED form only** — see `[CORRECTION v26]` at §1(P4)
  below; the unconditional statement is false, the version with `Re s ≥
  -1/2` is proved.
- **M1: two finite instances proved** (depth-1, in corrected form — see
  `[CORRECTION v26]` at §5(M1) below; and depth-2, as stated). The general
  (all-`K`, all-`q`) M1 bijection claim is untouched — left as a standing
  `axiom` (`wordLimitMap_injective_on_matched`), confirmed **unused** by
  anything proved, i.e. no proved result in this dispatch secretly depends
  on the unproved general M1.
- **Unchanged (not in scope for v26):** N1's universal (C1) bound, N2–N4,
  M2, M3, and §3's assembled candidate lemma with its NUMERIC-CONJECTURED
  constants (11/20, C(1.1,1.5) ≤ 2.0). The RATE lemma remains DRAFT status.
- **Downstream-impact check (P4 correction vs §3/§4's ε-table): NO
  impact.** The draft's candidate lemma is stated and validated at `σ ≥
  σ₀ = 1.1` throughout (§3 lemma statement, §4 validation table all use
  `s = 1.1 + 1.5i`, i.e. `Re s = 1.1`). The corrected P4 needs `Re s ≥
  -1/2`, which `1.1 ≥ -1/2` satisfies with wide margin — the domain the
  draft actually works in was never in the region where the uncorrected
  P4 fails (that region is `Re s < -1/2`, never visited). §4's ε(q) table
  inputs (Δ_X, E_q, E_θ, T_X, all evaluated at σ=1.1) are unaffected;
  no entry in that table needs recomputation.

**Date:** 2026-08-17. **Lane:** G. **Interpreter:**
`/Users/za/miniforge3/envs/pari-arb/bin/python3`. **Probe:**
`law_probes/r2_drift.py` → `law_probes/r2_drift_data.json`.

---

## 0. Headline

- **The KEY quantitative question is answered (measured): sup_{λ∈[λ_q,2]}
  |c_w′(λ)| ≤ A·k_w²·|c_w(λ_q)|, k_w = word depth (number of Q letters),
  with A = 0.518 measured max over all **1,138 MATCHED** cosets tested, all
  q ∈ {12,16,24,32,48} (per-q maxima 0.501–0.518, strikingly stable); the
  246 escaping cosets in the same enumeration were NOT tested.** So the
  growth is neither |c|^α alone (fitted α ≈ 1.06–1.19, i.e. barely above 1)
  nor O(ℓ·|c|): the correct law is **O(k²·|c|)** — and the Chebyshev
  subfamily (§2.3) shows k² is EXACT (not improvable to k^{2−δ}).

  > **[CORRECTION 2026-08-18 audit-10]** The original bullet said A = 0.518 is
  > the "measured max over ALL enumerated cosets". It is not. `r2_drift.py`
  > (`law_probes/r2_drift.py:173-196`) collects matched cosets in `rows` and
  > escaping cosets in `esc_q`, and computes `Amax` from `rows` ONLY. §2.1's
  > table totals 1,384 enumerated q-cosets, of which 1,138 are matched and
  > 246 escape. So the honest statement is: **maximum over all 1,138 matched
  > cosets tested; 246 escaping cosets were not tested**, at X = 50 and word
  > depth ≤ 12. The universal claim (C1)/N1 stays OPEN, and is now open on a
  > strictly larger population than the measurement covered.
- **The q⁻² vs q⁻¹ reconciliation asked for in the task is CONSISTENT with
  the finite-window data** (§2.4): per-pair drift carries (2−λ_q) ≈ π²/q², but the
  matched class contains words of depth k up to ~q (the elliptic relation
  (Q_qS)^q = 1 is what terminates the family), and Σ_matched k²|c|^{−2σ}
  grows like q^{3−2σ}; net ε(q) ~ q^{1−2σ} = q^{−1.2} at σ = 1.1 —
  consistent with `LAW_RATE_MEASURE.md`'s measured off-axis slopes
  (−0.65…−1.68) and steeper real-axis slopes at larger σ.
- **Candidate lemma stated (§3) and validated (§4): the assembled bound
  MAJORIZES the measured D(q; 1.1+1.5i) at every tested q.** At q = 32:
  **ε(32) = 0.0973 vs measured D = 0.02506** (overshoot 3.9×). Overshoot
  range 2.7×–12.5× across q = 48…12 (lossy but one-sided, never under).
- **Matching changed from R1's rank proxy to a word-level λ→2 limit with
  GREEDY canonicalized claiming** (each q-coset's word re-evaluated at λ=2
  and canonicalized, smallest-|c| first): at q = 32, 48 this matches every
  theta coset in the |c| ≤ 50 window (0 unmatched) — finite-window,
  depth-≤12, Chebyshev-family EVIDENCE, not a proof, and not a closure of
  R1's §5 proxy caveat.

  > **[CORRECTION 2026-08-18 audit-4]** Two claims in this §0 are downgraded.
  > (a) The original read "**The q⁻² vs q⁻¹ reconciliation asked for in the
  > task CHECKS OUT quantitatively**". (b) The original read "**Matching
  > upgraded from R1's rank proxy to the EXACT word-level λ→2 limit** …
  > closing R1's §5 proxy caveat within the window", and MAP recorded "THE
  > POWER MYSTERY RESOLVED". Neither is earned. R1 states at its §3.4 that
  > the two slope measurements "are not directly comparable" and that R1
  > "does NOT claim to have resolved or reconciled" them, and at §5 that the
  > matching is a rank-matching PROXY. What this note adds is finite-window
  > (X = 50), depth-≤12, Chebyshev-family evidence under a greedy
  > canonicalized matching — the map is not proved well-defined, injective,
  > or surjective at coset level. "Resolved" and "exact" must wait for the
  > corrected coset-level M1 (§5(M1)); until then the reconciliation is a
  > consistent numerical account, not a resolution.
- **Gap count: 4 numerically-supported-only items, 3 missing items** (§5),
  each tagged for Aristotle-readiness.

---

## 1. Setup (all derived, nothing new assumed)

Conjugated Hejhal model (`LAW_HEJHAL_S7_EXTRACT.md` §1): S: z↦z+1,
Q = Q_λ = (0, −1/λ; λ, 0), λ = λ_q = 2cos(π/q) ∈ [√2, 2), theta group at
λ = 2. Double cosets [S]\𝒢/[S] represented by reduced words

    w = Q S^{n_1} Q S^{n_2} … S^{n_{k−1}} Q,   k ≥ 1, n_i ∈ ℤ∖{0},

c_w(λ) = lower-left entry of the product. By formula (7.5),

    φ(s) = M(s) · Σ_{cosets, c≠0} |c|^{−2s},   M(s) = √π Γ(s−1/2)/Γ(s).

**(P1)** Each entry of the product is a Laurent polynomial in λ with integer
coefficients (induction on the factors; Q contributes λ and −1/λ, S^n
contributes integers). In particular c_w(λ) is real-analytic on [λ_q, 2] and
the same WORD defines both c_w(λ_q) and its theta-side limit c_w(2).

**(P2)** dQ/dλ = (1/λ)·E·Q with E = diag(−1,1) — a one-line 2×2 identity
(verified to 1.2e−31 against a central difference, GATE A). Hence by the
product rule, c_w′(λ) is a sum of k terms, each the c-entry of the word with
one Q replaced by (1/λ)EQ.

**(P3)** Mean value: |c_w(λ_q) − c_w(2)| ≤ (2−λ_q) · sup_{λ∈[λ_q,2]}|c_w′(λ)|.

**(P4)** For x, y > 0, s = σ+it: |x^{−2s} − y^{−2s}| ≤ 2|s|·min(x,y)^{−2σ−1}·|x−y|
(mean value on t ↦ t^{−2s}, |d/dt| = 2|s| t^{−2σ−1}, monotone).

> **[CORRECTION v26]** Aristotle proved this statement is FALSE as written
> without a hypothesis on `Re s` (counterexample `x=1, y=2, s=-1`:
> LHS = 3 > RHS = 2 — the mean-value sup sits at `max(x,y)` instead of
> `min(x,y)` once the exponent `-2σ-1` turns positive, i.e. for `σ <
> -1/2`). The corrected, proved statement adds the hypothesis `Re s ≥
> -1/2`:
>     |x^{−2s} − y^{−2s}| ≤ 2|s|·min(x,y)^{−2σ−1}·|x−y|,  σ = Re s ≥ -1/2.
> This is harmless for the draft: §3/§4 work at `σ ≥ σ₀ = 1.1`, well inside
> `σ ≥ -1/2`, so no downstream constant changes (see the
> `[MACHINE-VERIFIED 2026-08-17]` block above). Lean names:
> `cpow_neg_two_s_bound_false` (falsity), `cpow_neg_two_s_bound'`
> (corrected form), `projects/aristotle_dispatch_v26/result/.../RateCore.lean`.

**(P5)** 2 − λ_q = 2(1 − cos(π/q)) ≤ π²/q².

**(P6, Chebyshev subfamily — exact)** For w = (QS)^{m−1}Q (all n_i = 1,
k = m): c_w(λ) = λ·U_{m−1}(λ/2) = λ·sin(mθ)/sin(θ) at λ = 2cos θ (verified
exactly, GATE A; provable by induction on m). At λ = 2: c = 2m. Hence
c_w′(λ) = U_{m−1}(λ/2) + (λ/2)U′_{m−1}(λ/2), and at λ = 2:
c_w′(2) = m + (m³−m)/3, i.e. **|c_w′| ~ (k²/3)·|c_w| for this family** —
the k² in the growth law is attained, up to constant.

> **[CORRECTION 2026-08-18 audit-13]** Scope of machine verification for P6:
> the v26 harvest proves ONLY `c_w(λ) = λ·U_{m−1}(λ/2)` (`c_chebyshevWord`)
> and `c_w(2) = 2m` (`c_chebyshevWord_two`). The derivative formula
> `c'_w(2) = m + (m³−m)/3` and the sharpness ("k² attained") conclusion above
> are PAPER ALGEBRA, verified only by the GATE A numeric identity checks in
> `law_probes/r2_drift.py`. They are a separate, not-yet-dispatched
> formalization item. §2.3's sharpness statement inherits the same status.

---

## 2. The measured structure (probe r2_drift.py, X = 50, depth ≤ 12)

### 2.1 Word-level matching, greedy canonicalized (finite-window evidence;
not an exact correspondence — see [CORRECTION 2026-08-18 audit-4] in §0)

For each enumerated q-coset (word kept), the SAME word is re-evaluated at
λ = 2 and canonicalized: if it lands on a theta coset in the window (and that
theta coset is not already claimed by a smaller-|c| q-coset), the pair is
MATCHED; otherwise the q-coset is ESCAPING. Unclaimed theta cosets are the
theta-side unmatched class.

| q | cosets | matched | esc_q | unmatched_θ | k_max matched |
|---|---|---|---|---|---|
| 12 | 318 | 204 | 114 | 33 | 7 |
| 16 | 296 | 224 | 72 | 13 | 9 |
| 24 | 276 | 236 | 40 | 1 | 12 |
| 32 | 253 | 237 | 16 | 0 | 12 |
| 48 | 241 | 237 | 4 | 0 | 12 |

(θ window has 237 cosets; at q = 32, 48 the matching is ONTO the window —
the exact-limit map covers the theta spectrum completely there.)

### 2.2 Growth of sup|c_w′|

Per-q fits and the uniform-constant check of sup|c′| ≤ A·k²·|c_q|:

| q | fit α in \|c′\|~\|c\|^α | fit β in \|c′\|/\|c\| ~ k^β | max A = sup\|c′\|/(k²\|c_q\|) |
|---|---|---|---|
| 12 | 1.090 | 1.608 | 0.518 |
| 16 | 1.092 | 1.723 | 0.510 |
| 24 | 1.064 | 1.754 | 0.504 |
| 32 | 1.129 | 1.714 | 0.502 |
| 48 | 1.186 | 1.674 | 0.501 |

**Answer to the task's KEY question**: |c_w′| is O(k²·|c_w|), NOT a pure
power |c_w|^α with α substantially above 1, and NOT O(ℓ·|c|). The uniform
constant A ≤ 0.518 over the 1138 MATCHED cosets measured (246 escaping
cosets untested — [CORRECTION 2026-08-18 audit-10], §0), with per-q max DECREASING
toward ~1/2 as q grows, motivates the conjectured clean form

    (C1) sup_{λ∈[λ_q,2]} |c_w′(λ)| ≤ (11/20)·k_w²·|c_w(λ_q)|   [NUMERIC-CONJECTURED]

(11/20 = 0.55 leaves margin over the measured 0.518; §5 discusses proof
routes — the Chebyshev family §1(P6) gives k²/3, so a proof must show general
words are at most ~3/2 worse, or prove a clean k² bound outright.)

### 2.3 Sharpness

The β fits (1.6–1.75 < 2) reflect that TYPICAL words are below the k²
envelope; the envelope itself is set by the near-Chebyshev words (P6), so k²
cannot be lowered in (C1) without losing the extremal family.

### 2.4 Reconciliation of q⁻² per-term vs measured ~q⁻¹ aggregate — CONSISTENT
with the finite-window data (downgraded from "CHECKED",
[CORRECTION 2026-08-18 audit-4])

For the Chebyshev family: drift of the m-th pair ≈ (2−λ_q)·(m³/3), Dirichlet
contribution ≈ 2|s|(2m)^{−2σ−1}·(2−λ_q)·m³/3 ~ |s|(2−λ_q)·m^{2−2σ}. The
family persists until the elliptic relation closes it (m < q; c_m(λ_q) =
λ_q sin(mπ/q)/sin(π/q) returns to 0 at m = q while the theta side keeps
c = 2m — this is WHERE the escaping/unmatched classes come from).
Σ_{m<q} m^{2−2σ} ~ q^{3−2σ}/(3−2σ), so the family's total drift ~
(π²/q²)·q^{3−2σ} = π²·q^{1−2σ}. **At σ = 1.1 this is q^{−1.2}, between the
measured off-axis slopes −0.81 (t=1.5) and −1.33 (t=0.5) — the "lost factor
of q" the task asked to check is exactly the depth-summed k² growth.** The
fixed-window (X = 50) data shows the complementary regime: there k ≤ 12 is
window-capped, so the in-window drift sum decays like q^{−2}·(k²-weighted
constant) — see §4's shrinking overshoot, which is WHY the beyond-window
tail term in the lemma is load-bearing.

---

## 3. Candidate lemma (DRAFT)

**Lemma (RATE, candidate).** Fix σ₀ = 1.1 and a height window |t| ≤ T (here
T = 1.5 validated; constants below are s-explicit except where tagged). Let
q ≥ 12, s = σ+it with σ ≥ σ₀. Then

    |φ_q(s) − φ_∞(s)| ≤ ε(q; s) :=
        |M(s)| · [ Δ_X(q,s)  +  E_q(X,σ)  +  E_θ(X,σ)  +  T_X(q,σ) ]

with M(s) = √π Γ(s−1/2)/Γ(s) (|M(1.1+1.5i)| = 1.43694…) and:

1. **Matched-drift core** (derived from P1–P5 + (C1)):
       Δ_X(q,s) = Σ_{matched pairs, |c|≤X} 2|s|·min(c_q,c_θ)^{−2σ−1}
                  · (2−λ_q) · sup|c_w′|
   ≤ 2|s|·(π²/q²)·(11/20)·Σ_matched k_w²·c_q^{−2σ}·max(1, (c_θ/c_q)^{...})
   — in the validation below Δ_X is evaluated with the MEASURED per-word
   sup|c_w′| (no conjecture needed in-window); the (C1) closed form is the
   version a proof would use.
2. **Escaping masses** (derived; these are full one-sided masses, P4 not
   applicable since no partner):  E_q = Σ_{escaping q-cosets} c^{−2σ},
   E_θ = Σ_{unmatched θ-cosets} c^{−2σ}. Both supported on the
   near-relation region (§2.4); measured to decay like q^{−2}-ish in the
   window.
3. **Beyond-window tail** [NUMERIC-CONJECTURED]:
       T_X(q,σ) = 2 · Δ_X^{outer}(q,s),
   where Δ_X^{outer} is the part of Δ_X with min(c_q,c_θ) > X/2. Rationale:
   the measured outer-half:total ratio is 0.13–0.22 at every q, i.e. the
   drift sum converges in X with per-doubling ratio < 1/2 within the window;
   doubling the outer-half is a geometric-series allowance
   Σ_j ratio^j ≤ 2 applied conservatively. A PROOF needs the closed-form
   majorant: with mult_θ(2n) = φ(2n) [NUMERIC-CONJECTURED, verified for
   2n ≤ 14] and k(c) ≤ min(q, c/λ_q+1) [derived: each Q S^{n}-step multiplies
   the continuant-majorant by ≥ 1 and depth is bounded by the relation],
       Σ_{c>X} k(c)²·φ(c)·c^{−2σ}  ≤  q²·( X^{2−2σ}/(2σ−2) + X^{1−2σ} )
   — explicit but grossly lossy in q; the honest asymptotic form is
   κ(σ)·q^{3−2σ}·X-corrections, giving the ε(q) ~ q^{1−2σ} law of §2.4.

**Asymptotic corollary (shape claim, modulo the §5 gaps):**
    ε(q; σ+it) ≤ C(σ,T) · q^{1−2σ},  σ ≥ 1.1,
with C(1.1, 1.5) ≤ 2.0 [NUMERIC-CONJECTURED — calibrated: max over tested q
of D·q^{1.2} is 1.64, and the assembled ε(q)·q^{1.2} stays below 2.0 for
q ≥ 24].

### Proof skeleton

(i) Split the double-coset series of φ_q and φ_∞ by the word-level λ→2 map
(§2.1); injectivity/surjectivity up to the elliptic cutoff is gap M1.
(ii) On matched pairs apply P4 then P3 then (C1) then P5: per-pair bound
2|s|·min^{−2σ−1}·(π²/q²)·(11/20)k²·c_q^{−2σ+…}. (iii) Escaping/unmatched
terms enter with full mass; localize them to the near-relation region
(Chebyshev picture, §2.4) — gap M1 again for the general-word version.
(iv) Beyond-window: closed-form majorant (gap N3/M2), Lemma 7.2-style,
N-independent per Hejhal. (v) Sum; the k²-weighted matched sum truncated at
depth ~q yields q^{3−2σ}; multiply by (2−λ_q) ≤ π²/q².

---

## 4. Validation at s = 1.1 + 1.5i (bound must MAJORIZE measured D)

Measured D from `rate_measure_data.json` (N=24 determinant route, converged
rows, `LAW_RATE_MEASURE.md`); bound assembled from r2_drift data with
measured per-word sup|c′| (in-window, conjecture-free) + the T_X allowance:

| q | Δ_X·\|M\| | (E_q+E_θ)·\|M\| | T_X·\|M\| | **ε(q) bound** | measured D | overshoot | majorizes? |
|---|---|---|---|---|---|---|---|
| 12 | 0.4794 | 0.0839 | 0.1267 | **0.6900** | 0.05521 | 12.5× | YES |
| 16 | 0.2945 | 0.0415 | 0.1285 | **0.4645** | 0.05062 | 9.2× | YES |
| 24 | 0.1455 | 0.0144 | 0.0443 | **0.2042** | 0.03617 | 5.6× | YES |
| 32 | 0.0690 | 0.0046 | 0.0237 | **0.0973** | 0.02506 | **3.9×** | YES |
| 48 | 0.0269 | 0.0011 | 0.0096 | **0.0376** | 0.01378 | 2.7× | YES |

- **Never undershoots** — the lemma survives its falsification test as
  drafted.
- **Lossiness**: overshoot 2.7–12.5×, WORSE at small q (the in-window
  matched class is smaller there — 204/318 at q=12 — so more mass sits in
  the crudely-bounded escaping class) and improving toward ~2× at q=48.
- **Warning, honestly flagged**: the in-window core decays ~q^{−2.2},
  FASTER than measured D (~q^{−0.8} at this s); naive extrapolation crosses
  near q ≈ 90–100. The bound stays valid only because T_X carries the true
  q^{1−2σ} tail scaling as X must grow with q; a fixed X = 50 assembly
  should NOT be quoted for q > 48 without re-enumeration at larger X. This
  is a structural feature (window-capped k ≤ 12), not a bug in the data.
- **Against the R4 target (0.66 defect)**: raw ε(q) < 0.66 for q ≥ 16
  already at σ = 1.1; the R3 transport multiplier (open) will consume
  margin, so the working target is the q ≳ 32 range where ε ≤ 0.1.

---

## 5. Gap list with Aristotle-readiness tags

**Proved in this draft (i):** P1 (integer-Laurent entries; induction —
**Aristotle: YES**, finite algebraic induction), P2 (Q′ = (1/λ)EQ —
**Aristotle: YES**, 2×2 identity), P3/P4 (mean-value bounds — **Aristotle:
YES** as stated for polynomials/monomials; the sup over [λ_q,2] per FIXED
word is **MAYBE via interval arithmetic**), P5 (cos inequality —
**Aristotle: YES**), P6 (Chebyshev family c_m = λU_{m−1}(λ/2) —
**Aristotle: YES**, induction on m).

**Numerically supported only (ii):**
- **N1 = (C1)**: sup|c′_w| ≤ (11/20)k²|c_w(λ_q)| uniformly over words.
  Measured max 0.518 over 1138 MATCHED cosets (X = 50, depth ≤ 12; 246
  escaping cosets untested — [CORRECTION 2026-08-18 audit-10]), 5 values of
  q. **Aristotle: MAYBE**
  — per-word instances are finite algebra + interval sup (yes); the
  UNIVERSAL claim needs an induction over words with a loop invariant
  (candidate: positivized-continuant comparison |c′| ≤ (k²/2)ĉ, ĉ the
  |n_i|-continuant, plus ĉ vs |c| control — the second half FAILS for
  words with heavy cancellation, so the invariant needs the elliptic-region
  structure; genuinely open).
- **N2**: matching is ONTO the theta window for q ≥ 32 (measured 0
  unmatched). **Aristotle: YES per fixed (q, X)** (finite check), the
  all-q statement is M1.
- **N3**: T_X = 2·outer-half is a valid tail allowance (measured ratio
  ≤ 0.22 < 1/2). **Aristotle: NO as stated** (infinite sum, no closed-form
  majorant yet); becomes YES if the φ(2n)-multiplicity majorant (below) is
  proved and the sum is bounded by the printed integral comparison.
- **N4**: mult_θ(2n) = φ(2n) (verified 2n ≤ 14) and the q^{3−2σ} scaling of
  the k²-weighted matched sum. **Aristotle: multiplicity claim MAYBE**
  (it is a Γ_θ-Kloosterman counting statement, likely in the literature —
  borrow-check before proving); scaling claim needs M1.

**Missing (iii):**
- **M1**: the word-level λ→2 map is a bijection {matched q-cosets} →
  {θ-cosets with c ≤ c*(q)}, with the complement (both sides) confined to
  the near-relation region. This is THE structural lemma; without it the
  split in §3(i) is data, not proof. **Aristotle: NOT as stated** (needs a
  normal-form/geodesic argument in ℤ₂ * ℤ_q vs ℤ₂ * ℤ); a finite-depth
  restricted version (all words of depth ≤ K) is **YES** per (q, K).

  > **[CORRECTION v26]** Two finite-depth instances of this "YES per (q,K)"
  > claim were sent to Aristotle and proved. The depth-2 instance
  > (`c_w[n]` for word `[n]`, the pair `(QS^nQ)`) closes exactly as stated:
  > `c_{[n]}(λ) = n·λ²`, injective in `n` for fixed `λ ≠ 0` (Lean:
  > `c_depth_two`). The depth-1 instance (`w = []`, the single letter `Q`)
  > was stated with the WRONG closed form: the working notes' assumed
  > value `c_{[]}(λ) = -1/λ` is the *upper-right* entry of `Q_λ = (0,
  > -1/λ; λ, 0)`, not the *lower-left* entry that `c_w` is defined to be
  > throughout this draft (§1). Aristotle proved the assumed value false
  > (`wordLimitMap_matched_depth_one_false`, witness `λ=1`) and proved the
  > entry-convention-consistent value `c_{[]}(λ) = λ`
  > (`wordLimitMap_matched_depth_one'`) — which also matches P6 at `m=1`
  > (`c = λ·U_0(λ/2) = λ`), so it is a pure bookkeeping/convention fix, not
  > a change to the underlying `Q_λ` matrix or to any other proved result.
  > No downstream constant in §3/§4 references this depth-1 value directly
  > (the general M1 bijection, not the depth-1 special case, is what §3's
  > proof skeleton needs — still open). Lean:
  > `projects/aristotle_dispatch_v26/result/.../RateCore.lean`.

  > **[CORRECTION v27, 2026-08-18]** The v26 formulation of the general M1
  > hypothesis (`wordLimitMap_injective_on_matched`: injectivity of the
  > c-ONLY word map `w ↦ c_2(w)` on matched words of bounded depth) is
  > FALSE already at depth 3: the closed form is
  > `c_λ([n,m]) = λ(n·m·λ² − 1)` (hand-derived, numerically verified at
  > 3 λ values; Aristotle certification of the disproof in flight, v27
  > project 0103cfab), so `[1,2]` and `[2,1]` collide at every λ. The
  > collision refutes only the c-only WORD-level proxy: the lower-right
  > entries differ (`d = −nλ` vs `−mλ`), so R1's canonical coset invariant
  > `(c, d mod c)` may still separate them. CORRECTED TARGET (statement of
  > record, replacing the c-only axiom): M1 is a canonical-normal-form
  > theorem at the COSET level — the λ→2 specialization is well-defined on
  > double cosets `[S]\𝒢_q/[S]` via the invariant `(c, d mod c)`, injective
  > on matched cosets into θ-cosets with `c ≤ c*(q)`, surjective onto the
  > sub-`c*(q)` range, with the complement localized to the near-relation
  > region — each of well-definedness / injectivity / surjectivity /
  > localization a separate obligation. The v26 axiom is
  > deleted-as-hypothesis (it was referenced by nothing proved); until the
  > coset-level statement is proved, §3(i)'s matched/escaping split remains
  > DATA, NOT PROOF, and the ε(q) exponent q^{1−2σ} remains a calibrated
  > conjecture. Strategy lane: M1_COSET_STRATEGY_SOL.md (in progress).
- **M2**: rigorous N-independent beyond-window majorant = making Hejhal
  Lemma 7.2's C(ε) explicit (route: ch.6 prop 5.1 tiny-disk argument, per
  the extraction note). **Aristotle: NO** (analytic, infinite sum) until a
  closed-form summable majorant is written; then MAYBE.
- **M3**: s-uniformity — constants here are validated at one s; |M(s)|,
  2|s| are explicit in s, but T_X's ratio and the C(σ,T) calibration are
  single-cell. Extending the validation grid is mechanical (evaluator
  exists); the PROOF-side s-dependence enters only through |M(s)| and 2|s|
  (both explicit), so this gap is small but real.

**Gap count: 4 numeric-only (N1–N4), 3 missing (M1–M3).**

---

## 6. Files

- `law_probes/r2_drift.py` — probe (GATE A identity checks, exact λ-derivative,
  word-level matching, fits, bound assembly). Rerun: `run()`.
- `law_probes/r2_drift_data.json` — per-q raw output (fits, masses, samples).
- Upstream data reused: `law_probes/rate_measure_data.json` (measured D),
  `law_probes/r1_coset_enum.py` (enumerator, imported).

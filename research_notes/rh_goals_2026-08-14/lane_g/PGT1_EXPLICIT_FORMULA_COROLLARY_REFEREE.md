# PGT-1 Cold Referee Report — installed verbatim

Installation note (orchestrator, 2026-08-23 07:10Z): read-only referee seat;
report installed verbatim from the referee's inline return. Verdict:
PROMOTABLE-WITH-CORRECTIONS. Corrections applied as the dated append-only §10
block in PGT1_EXPLICIT_FORMULA_COROLLARY_SOL.md.

---

## Referee report — `PGT1_EXPLICIT_FORMULA_COROLLARY_SOL.md`

### VERDICT: **PROMOTABLE-WITH-CORRECTIONS**

The three load-bearing claims (reflection into `Re s < 1/2`; `O_q(x^{1/2}(log x)²)`; the Prop 3.2 constant) all survive my independent re-derivation. The headline "PGT-error-neutral, no Ω-result" is correct. But §3.5 contains a factor-2 wrong constant **and** an unproven-as-stated density claim that is exactly the Phillips–Sarnak-open question, §5's quotable block violates the lane's mandated Hejhal 7.11/7.12 disclosure, and the note nowhere inherits the LAW's `[Sel90]`-unread standing that its own sibling note declares binding.

---

### Checks I reproduced

| # | Criterion | Evidence | Result |
|---|---|---|---|
| 1 | FJS sha256 receipts genuine | `shasum -a 256 /tmp/fjs.pdf` → `36c9d020…7228`; `/tmp/pgt_avd.pdf` → `457877ce…e72c`. Both match §9 and the banked `LAW_…SOURCE_SOL.md:380`. | PASS |
| 2 | FJS `Z`-divisor item 6 verbatim | My own `pdftotext`: `6. Zeros at each s = 1 − ρ, 1 − ρ where ρ is a zero of φ(s) with Re(ρ) > 21 and Im(ρ) > 0;` — identical, including the `21` mangling the note flags. | PASS |
| 3 | FJS `φ`-divisor item 5 verbatim | `5. Poles of the form 1 − ρ and 1 − ρ with Re(ρ) > 1/2 and Im(ρ) > 0;` reproduced. | PASS |
| 4 | Reflection bookkeeping (claim 1) | Full FJS `Z`-divisor list 1–7 extracted: items 1 (on-line, discrete spectrum), 2/5/7 (real), 3 (`s=1/2`), 4 (poles), 6 (reflected). Item 6 is indeed the **only** source of nonreal off-line `Z`-zeros, and they lie in `Re<1/2`. | PASS (see D6 — the note doesn't receipt this) |
| 5 | Avdispahić eq. (1) shape + declared gap | `nl -ba` lines 87–115 confirm `ψ1,Γ = α0x + β0x log x + α1 + β1 log x + F(1/x) + x²/2 + Σ x^{ρ+1}/(ρ(ρ+1)) + O(x²logx/T)`. Line 13: `strictly hyperbolic Fuchsian group`; line 42: `the complex zeros of ZΓ are of the form ρ = 1/2 ± iγ`. The note's GAP declaration is accurate. | PASS |
| 6 | (P2) exponent and log power | `|x^{1−ρ}| = x^{1−β} < x^{1/2}` since `β>1/2` ✓. Partial summation with `N(t)=Ct log t`: `Σ1/|γ| = N(T)/T + ∫₁ᵀ N(t)/t² dt = C log T + C(log T)²/2 ≍ (log T)²` ✓. Exponent `1/2` and power `2` both correct at `T=x`. | PASS (arithmetic) |
| 7 | Prop 3.2 constant | `N_q(T) ≤ (σ₀−1/2)·N^off(T)` ⇒ `N^off ≥ (1/(2π(σ₀−1/2)))T log T(1+o(1))` ✓. Monotonicity claim ("enlarging σ₀ only weakens") verified. | PASS |
| 8 | §3.4 `q=3` cross-check | mpmath: weighted sum `(1/4)·2N(2T)` vs `(1/2π)T log T` — ratio `0.690 (T=1e3) → 0.814 → 0.867 → 0.907 (T=1e10)`, converging to 1 as `1+(−logπ−1)/log T`. Leading coefficients agree **exactly**. Slack check: `1/π = 0.31831` vs truth `2/π = 0.63662`, factor **2.000000** — as the note states. | PASS |
| 9 | Lemma 3.1 | `LAW_…SOURCE_SOL.md` (N)/(NF) confirm `λ_{q,n}=(g_n/g_1)²>1`, `L*=1+Σa_nλ_n^{−s}`, gamma ratio zero-free in `Re s>1/2`. Tail `≤ λ₂^{−(σ−2)}Σa_nλ_n^{−2}→0`. Sketch is sound. | PASS |
| 10 | (U) sketch plausibility | (P) `L*=O_q(|t|^{1/2})` on `1/2≤σ≤3/2` and right-edge `1+O(e^{−cσ})` are both banked in the LAW note §3.3. Unit-disc Jensen ⇒ `O(log T)` zeros/disc ⇒ `O(T log T)`. Standard; correctly marked SKETCH. | PASS-as-marked |
| 11 | Kelmer-ledger contamination (§8.8) | `grep` for `A_q\|B_q\|C_q` numerics in the target: only symbolic `A_q·T` in the (C) restatement; no numeric leaked. | PASS |
| 12 | Weyl / density (§3.5) | **FAILED** — see D1, D2. |
| 13 | Mandated Hejhal 7.11/7.12 disclosure | **FAILED** — see D3. |
| 14 | Sel90 ledger inheritance | **FAILED** — see D4. |

---

### Defects

**D1 · HIGH · `|F_q|` is wrong by a factor 2.** §3.5 and the §6 ledger row print `|F_q| = π(1/2 − 1/q)`. Gauss–Bonnet for the `(2,q,∞)` von Dyck group gives `2π(1 − 1/2 − 1/q) = 2π(1/2 − 1/q)`. Sanity check at `q=3`: true area of `PSL(2,Z)\H` is `π/3 = 1.047198`; the note's formula yields `π/6 = 0.523599`. Verified for `q = 3,4,5,6,7,12` — ratio exactly `2.0` every time. The downstream eigenvalue constant `((1/2−1/q)/4)T²` should be `((1/2−1/q)/2)T²` (`q=5`: note `0.075`, correct `0.15`). The ledger row is labelled "order only", which mitigates but does not license a printed wrong constant. *Why missed:* the author almost certainly used the reflection-triangle area, and `T log T = o(T²)` is insensitive to the slip, so no downstream check caught it.

**D2 · HIGH · The density-zero claim is not proven for the target class — it is the Phillips–Sarnak open question.** §3.5 states flatly: *"`Z_q` has `≍_q T²` zeros on `Re s = 1/2`"* and *"The off-line zeros are a DENSITY-ZERO subset."* FJS `Z`-divisor item 1 (which I extracted) sources the on-line zeros from the **discrete** spectrum. For a general cofinite group the Selberg trace formula gives only `N_d(T) + M(T) ~ (|F|/4π)T²`, where `M(T)` is the scattering winding number. For **non-arithmetic** surfaces the Phillips–Sarnak expectation is precisely that `N_d(T) = o(T²)` and `M(T)` carries the `T²`. The repo's own bank agrees: `wiki`/memory records "G_5 even sector = Phillips–Sarnak cusp dissolution", and `LAW_DEFORMATION_PRIOR_ART.md` §1.2–1.4 catalogues the dissolution literature. The claim needs only `N_d(T)/(T log T) → ∞`, which is plausible but unproven; in an extreme PS scenario the density claim would be **false**. Ironically this defect undercuts the note's own modesty caveat, so the author had no incentive to attack it. Repair: restate as `N_d(T) + M(T) ≍ T²` and mark the density conclusion CONDITIONAL on a discrete Weyl law for `G_q`.

**D3 · HIGH · §5's quotable block omits the mandated Hejhal 7.11/7.12 disclosure.** `LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_SOL.md:461-465` mandates: *"PRINTED PARTIAL ANTECEDENT: Hejhal LNM 1001, Theorem 7.11 and Corollary 7.12 (pp. 577-579)… **Must be cited wherever novelty is framed.**"* §5 is explicitly labelled "**verbatim, for quotation**" and frames novelty ("now known to be false by an infinite, quantitatively counted margin rather than by a hypothetical one") with **no** Hejhal mention. The disclosure appears only in §8 item 5, a referee-attack list that will not travel with the quoted paragraph. The headline verdict block at lines 11–20 has the same problem. Mandate violated at the exact site it was written for.

**D4 · HIGH · The `[Sel90]`-unread inheritance is nowhere declared.** `LAW_SECOND_AUDIT_REFEREE.md` "Residual dependency I could not discharge": *"The complex-analytic engine is `[Sel90, Lemmas 1, 2]`… Neither the author, nor the first referee, nor I have read Selberg 1990."* The sibling `NOGO_METATHEOREM_SOL.md:12-19` treats this as binding under LEDGER RULE: *"Every occurrence of 'PROVED' below therefore means proved modulo that one unread citation."* The target note's §1 "Banked caveats consumed here" lists four caveats (no effective height, no `q`-uniform error, no `A_q` numerics, non-discriminating) and **omits this one**; §1 instead upgrades (C) to "CONFIRMED by two lineage-independent cold referees", and §2.1 concludes "immediate and **unconditional** given the LAW". Same omission for the Selberg-1990 attribution repair (`:451-459`). Add the inheritance line.

**D5 · MODERATE · §4 silently switches from the `ψ_{1,Γ}` formula it receipted to a `ψ_Γ` formula no cited source prints.** §2.2 receipts eq. (1) for `ψ_{1,Γ}`. Prop 4.1 then estimates `Σ x^{1−ρ}/(1−ρ)` as a block of **`ψ_Γ(x)`**. Avdispahić's own `ψ_Γ` statement (my extract, Theorem 2) has no such sum: `ψ_Γ(x) = x + Σ_{3/4−ε<ρ<1} x^ρ/ρ + O(x^{3/4}/(log x)^α)` — the full zero-sum is *absorbed into the error term*, which is exactly why the trivial PGT exponent is `3/4` rather than `1/2+ε`. So (EF)-for-`ψ_Γ` is not merely unverified; it is not the shape of any formula the note cites, and the `ψ_1 → ψ` differencing step is where the loss occurs. §8.1 flags (EF) generally but not this specific slide. *The verdict survives* by an easier argument (any reflected block sits at `Re < 1/2`, hence below `x^{1/2}`), but the derivation as written does not.

**D6 · LOW · "all of them in `Re s < 1/2`" is asserted, not receipted.** §5 and Cor. 3.3 need the *full* FJS `Z`-divisor list to exclude other nonreal off-line items; the note quotes only item 6 and asserts the rest parenthetically ("arise from no other divisor item except finitely many real ones"). I verified the assertion is **true** — items 1,2,5,7 are real or on-line, 3 is `s=1/2`, 4 are poles. Cheap fix: quote the list. Also, §5's "all of them" is grammatically ambiguous between "all of the counted ones" and "all off-line zeros of `Z_q`"; only the latter is the interesting claim and only the full list licenses it.

**D7 · LOW-MODERATE · Prior art incomplete: Garbin–Jorgenson missing.** The repo's own `LAW_DEFORMATION_PRIOR_ART.md:8` records that Garbin–Jorgenson (2018), pp. 161–163, *"reproduce those exact statements, identify the family as the Hecke triangle groups `G_N`, and **quantify the accumulation**."* Since the note's declared novelty is precisely "all finite `q`, **with a count**" (§8.5), a printed source that quantifies accumulation is the sharpest antecedent in the bank and is not cited anywhere in §8 or §9.

**D8 · LOW · Non-arithmetic framing conflicts with the banked non-discrimination warning.** §5's headline says the divisor description "is false for **every non-arithmetic** Hecke surface". The LAW's second audit (`:487-490`) warns: *"The 'nonarithmetic in particular' clause is NON-DISCRIMINATING: q=3 (arithmetic) has the same off-line property… This LAW must never be used as an arithmeticity signature."* §1 carries the caveat; §5 — the quotable block — drops it and restricts to non-arithmetic, implying specialness. State it for all finite `q ≥ 3`.

**D9 · LOW · Rounding-discipline mislabel.** §4 claims the log power is "rounded **UP** (`2`, not `1`)". Under (U) the partial summation gives genuinely `≍ (log T)²/2`; `2` is the true power, not a conservative margin. Harmless for an upper bound, but the ledger advertises safety slack that does not exist.

---

### What is *not* wrong

Claims (1), (2) and (3) of the brief are sound. The reflection direction is receipted verbatim and is the correct refutation of the naive Ω-argument (§8.6 is right to insist it be displayed). The `q=3` consistency check in §3.4 is a genuinely independent derivation and reproduces the (C) leading coefficient exactly, with the predicted factor-2 slack. The "no Ω-result" argument — that the LAW supplies zero information on the arguments `γ`, so no non-cancellation lower bound is reachable even in principle — is the strongest part of the note and I could not break it. The §7 downgrade request against `NOGO_AUDIENCE_SURVEY.md` is justified: a block at `O(x^{1/2}(log x)²)` cannot be a "usable input" to an analysis fighting `x^{3/4}` toward `x^{1/2+ε}`.

**Recommended gate:** correct D1, D2, D3, D4 before any quotation of §5 leaves the lane; D5–D9 before paper-level use.

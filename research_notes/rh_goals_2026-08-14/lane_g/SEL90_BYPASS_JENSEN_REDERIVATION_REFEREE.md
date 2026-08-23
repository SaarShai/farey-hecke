# COLD REFEREE — SEL90-BYPASS Jensen re-derivation

> Installation note (orchestrator, 2026-08-23): the referee seat was read-only
> and returned this report inline; installed verbatim, unedited except this
> note and HTML-entity unescaping. Referee scripts: scratchpad ref_check.py,
> ref2.py.

**Date:** 2026-08-22. **Referee:** independent seat, no shared context with the author.
**Under review:** `/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/SEL90_BYPASS_JENSEN_REDERIVATION_SOL.md` (519 lines, commit `b177d8e`).
**Method:** every claim re-derived by hand or re-run; no author artifact reused. Numerics written fresh at `mp.dps=30` (author used 25), at **seven** heights including four the author never tested.

## Per-claim verdicts

| # | Claim | My evidence | Verdict |
|---|---|---|---|
| 1 | §1.1 pinning: `(J)` quoted verbatim from LAW SOL **lines 208–224** | `awk 'NR>=204&&NR<=226'` on the LAW SOL — block matches the note character-for-character, `\tag{J}` at 223 | **CONFIRMED** |
| 2 | Chain consumes only `H3`, lower half | `LawSkeletonI.lean:154–164`: `law_right_zeros_infinite_target` takes exactly `hZfin, hFdef, hgrowth`; `hgrowth : ∃ C, ∀ T ≥ 1, (1/(4π))T²logT − CT² ≤ F T`. No `(C)`, no `(DIF)`, no D1–D4 in the signature | **CONFIRMED** |
| 3 | §1.2 Kelmer quotes; boundary case delegated to `[Sel90]` | Re-fetched arXiv 1402.4780 myself: `shasum -a 256` = `c15fb0c4…f8d5030` (matches). `k.txt:1129` Lemma 4.7 "For any α > (d−1)/2"; `k.txt:1065` Lemma 4.6 "α ≥ α₀"; `k.txt:1157–1163` (4.20) "for any α ≥ (d−1)/2 … [Sel90, Lemma 1,2]". Remark 0.2 (`k.txt:217`) fixes `α₀ = 3/4` at `d=2`, confirming the note's `α₀ = d−5/4`. So the **boundary α=(d−1)/2 is genuinely carried by Sel90 alone** | **CONFIRMED** |
| 4 | Lemma A orientation calibration | Re-derived independently: `∫_{−u}^{u}½log(t²+A²)dt = u log(u²+A²) −2u +2A arctan(u/A)` (verified by differentiation); brackets → `π(A−B)` and `π(A+B)`; total `(1/2π)(2πA)=A` ✔ | **CONFIRMED** |
| 5 | Lemma B / `(LW∞)` with the `1/π` | Reflection `arg L*(σ−iu) = −arg L*(σ+iu)` from (Rl) collapses `(1/2π)[∫−∫]` to `(1/π)∫`; zero/pole-free `ℜs ≥ σ₁` from (E) ✔ | **CONFIRMED** |
| 6 | **Lemma C** (the crux) — derivation | Re-derived from scratch. `P(s) = −∫_s^∞ log L*` along the horizontal ray is holomorphic off cuts with `P′ = log L*`; `d/du P(σ+iu) = i log L*` ⇒ `d/du ℜP = −arg L*`. Cut jump at a zero: `log L*` jumps `±2πi` on `(σ,β)`, `0` beyond ⇒ `P` jumps `∓2πi(β−σ)` — **purely imaginary independent of the sign convention**, so `ℜP(σ+i·)` is continuous. Independently, `ℜP(σ+iu) = −∫_σ^∞ log|L*(x+iu)|dx` is *manifestly branch-free*, which is a second, stronger reason the divisor drops out. FTC ⇒ `∫_0^T arg du = ℜP(σ)−ℜP(σ+iT)`; `∫_α^∞∫_σ^∞ = ∫_α^∞(x−α)` ✔. **No zero count is used anywhere ⇒ no circularity.** `u=0` endpoint: real poles (F) sit on `ℑs=0`, met only at the endpoint, and `|log|x−σ_j+iu|| ≤ |log|x−σ_j||+C` gives dominated convergence for `ℜP(σ+i0)` ✔ | **CONFIRMED** |
| 7 | Lemma C — numerics | My own script, `/Users/za/.venvs/farey-rh/bin/python`, mpmath, dps=30. First reproduced (G) `|ζ(2it)/ζ(1+2it)| = π^{−1/2}(t tanh πt)^{1/2}` to `rel ≈ 1e−31` at t=1,3.7,25,100. Then `|E_num − E_pred|`: T=25 → 9.5e−30; T=50 → 4.3e−29; T=100 → 1.7e−29 (author's `F`,`integral`,`E_num` values reproduced **digit-for-digit** on independent code). **New heights:** T=3.9 → 4.9e−32 and T=7.0 → 0.0 (*zero* divisor points, so `E` is pure Lemma-C content, not a cancellation artifact); T=60.5 → 9.4e−29; **T=200 → 3.2e−27; T=300 → 1.3e−26** | **CONFIRMED** |
| 8 | Lemma C across a zero ordinate | First divisor ordinate `γ = γ_ζ,1/2 = 7.06736257086735`. Tested `T = γ−1e−6` (n=0 zeros), `T = γ+1e−6` (n=1), `T = γ+1e−3`: agreement `4e−31 … 5e−31` throughout. The identity holds **on both sides of the jump**, exactly as the purely-imaginary-jump argument predicts | **CONFIRMED** |
| 9 | Cross-lineage: my `E_num(200) = −0.1469714` vs `LAW_SECOND_AUDIT_REFEREE.md:20` `T=200: diff=−0.147` | independent code, independent lineage, same number; also T=50 `−0.116`, T=100 `−0.047` | **CONFIRMED** |
| 10 | §3.5 bound `E(T) ≤ (σ₁−½)²/(4π)·log T + O_q(1)` | Re-derived: `(1/π)·((σ₁−α)²/2)·(½log T) = (σ₁−½)²/(4π)log T`. Tail `x≥σ₁`: `2A_q∫(x−α)e^{−c_qx} = O_q(1)`. `I₀` finite (log singularities at `x=½`, at `σ_j`, integrable). Rounding: every step rounds the bound **UP**, `|L*(s₀)| ≥ ½` rounds **DOWN**. Arithmetic exact | **CONFIRMED** |
| 11 | (F)/(NF)/(P)/(G) inputs are the banked ones | `LAW_..._SOL.md:160–175` (H7.7, `(P)` on `½≤σ≤3/2`, `σ≥3/2` bounded), `:185` Hejhal Lemma 7.7 receipt, `:261–265` FJS receipt for order ≤2 / `φφ(1−s)=1` / finite real poles. Match | **CONFIRMED** (see D-3) |
| 12 | Lemma D (§3.7) conformal sub-mean-value | Direction of sub-mean-value is right: subharmonic ⇒ `v(0) ≤ (1/π)∫∫_D v` ⇒ `∫∫ v ≥ −π log2` ✔. `∫∫v_- = ∫∫v_+ − ∫∫v ≤ π(M+log2)` ✔. Carathéodory extension justifies boundary max principle on the Jordan half-disc ✔. Pull-back `dA(w)=|ψ′|²dA(s)` ✔. `K = H̄∩{|s−c|≤R/2}` avoids both corners and the arc, and `K∩{ℜs=½} = [T−R/2, T+R/2]` is a **compact subset of the open diameter**, so Schwarz reflection gives `|ψ′| ≥ κ > 0` ✔. `R = 2σ₁+4` ⇒ `√((σ₁−½)²+1) ≤ σ₁+2 = R/2`, so `K ⊇ [½,σ₁]×[T−1,T+1]` ✔ | **CONFIRMED-with-corrections** (D-1, D-2) |
| 13 | Quantifier match: does the LAW need every `T` or a sequence? | `hgrowth` is `∀ T ≥ 1`. §3.8 delivers `∀ T ≥ T₀(q)` (monotonicity upgrades the single good `T*` to *every* `T`), and `1 ≤ T ≤ T₀` is absorbed by enlarging `C` since `F ≥ 0` and `(1/4π)T²logT − CT² ≤ 0` for `C ≥ (log T₀)/4π`. **No quantifier gap.** (The DISPATCH §7-A3 contradiction would in fact only need a sequence — the note over-delivers) | **CONFIRMED** |
| 14 | §3.8 `H3`, both halves, constant `1/4π` | Re-derived `∫_0^T(T−t)log t dt = ½T²log T − ¾T²`; with the `½` from (G) and `1/2π`: `(1/4π)T²log T − (3/8π)T²` ✔ (matches DISPATCH C1 float check). Slack: `T²logT − T*²logT* ≤ 2TlogT+T = O(T²)` ✔. `Σ(σ_j−½) ≥ 0` drop ✔; upper half uses §3.5 at every `T` plus `Σ(σ_j−½) = O_q(1)` ✔. Uniformity: `O_q(T²)` is **per-q**, matching DISPATCH decision 4 ("no `q`-uniformity is expressible here, and none is claimed") ✔ | **CONFIRMED** |
| 15 | GAP-1 honestly scoped | §3.7/§3.8 nowhere invoke GAP-1; traced every step. The structural block (no disc inside `{ℜs≥½}` covers a neighbourhood of `½+iT`; (F) converts left upper bounds into right *lower* bounds, false at zeros) is correct | **CONFIRMED** |
| 16 | GAP-2 honestly scoped | `(C)`/`(DIF)` enter only via D1–D4, which are **standalone abstract calculus targets** (`LawSkeletonI.lean:264–270`), not arguments of `law_right_zeros_infinite_target`. DISPATCH decision 2 states `(C)` is not used | **CONFIRMED** |
| 17 | Scope / side effects | `git show --stat b177d8e`: 3 files, **695 insertions, 0 deletions**, no modifications to existing files. The SOL note itself is a pure addition. No drive-by edits | **CONFIRMED** |

## Numbered defects (all cosmetic-to-rigor; none refutes a verdict)

**D-1 — §3.3 Fubini justification gives a *wrong reason*.**
The note writes: "the right-continued `arg L*` is bounded (by `π(2N+1)` with `N` the finite number of divisor points in that box)". This is **false as a general principle**: the winding accumulated by continuing `arg` leftward along a horizontal segment is controlled by the number of sign changes of `ℜL*` on that segment (Backlund / Titchmarsh Lemma 9.2 — exactly the machinery Kelmer cites in his Lemma 4.7), **not** by the count of divisor points in the box. The *conclusion* (local boundedness on `[α,σ₁]×[0,T]` for fixed `q,T`) is nonetheless true — `arg L* − Σ_k arg(s−ρ_k)` is continuous on the compact box, and only finiteness, not a uniform-in-`T` constant, is needed for Fubini (§3.3) and for the absolute continuity used in Lemma C step 3. **Correction required:** replace the parenthetical with "bounded on the compact box for each fixed `T` (no uniformity in `T` claimed or needed)". *Why the author missed it:* the bound is stated in a justification aside, and the correct statement gives the same conclusion, so the numerics could never catch it.

**D-2 — §3.7 quantifier arithmetic understated.**
The consequence display integrates over `[T−1, T+1]` (length 2) but the conclusion asserts `T* ∈ [T−1, T]`. This is fine (the integrand is `≥ 0`, so restricting to the length-1 subinterval preserves the bound and the average), but the note never says so. Also un-stated, and load-bearing: **`κ(R)` is independent of `T`** because `H` is a pure *translate* `H = H₀ + iT` of a fixed half-disc, so `ψ = ψ₀(· − iT)`. Without that remark the reader cannot see that `C_q(R)` is not secretly `C_q(R,T)`. **Correction required:** state both.

**D-3 — §2 `(P)` extension leaves a strip uncovered by its own two cited clauses.**
"(P) … for `½ ≤ σ ≤ 3/2` … With (E) this gives `≤ C_q′|t|^{1/2}` on the whole of `ℜs ≥ ½`" — but (E) only starts at `σ₁ ≥ 3/2`, so if `σ₁ > 3/2` the strip `3/2 < σ < σ₁` is covered by neither cited clause. The gap is closed by the banked `LAW_..._SOL.md:172` ("For `σ ≥ 3/2`, the absolutely convergent series supplies a bounded right half-plane"), which the note does not cite here. Load-bearing for the **arc** bound in Lemma D, where `ℜs` runs up to `R = 2σ₁+4`. **Correction:** cite line 172.

**D-4 — `σ₁` notation collision.** `σ₁` denotes the right-edge normalisation constant (`σ₁ ≥ 3/2`) in §2/§3, and the *pole location* (`σ₁ = 1`) in §4 line 415. Confusing in the one section where both appear; rename the §4 occurrence.

**D-5 — §1.1's DISPATCH line citation is off by one.** The quoted sentence "The LAW's analytic weight lives entirely in H3." spans DISPATCH lines 85–86, not 86. Trivial.

**D-6 — numeric claim is *under*-stated, not over-stated.** The note claims "14–16 significant digits". At `dps=30` with (G) in closed form I get agreement at `1e−26 … 1e−32` (≈ 26–31 digits). Their figure is limited by `dps=25` plus float readout. Flagging only so nobody later "corrects" the stronger number downward.

## What I could not break

- I attacked Lemma C step 2 hardest, per the author's own suggested attack order. It survives *twice over*: the jump argument is correct, and independently `ℜP` is defined by `−∫ log|L*|`, which never sees a branch at all. The `u = 0` endpoint (where real poles sit on the path) is handled correctly by (F) + dominated convergence.
- I attacked the numerics at heights the author avoided — including `T = 7.0` and `T = 3.9` where the divisor is **empty** (so no cancellation can mask an error), and at `T = γ ± 10⁻⁶` straddling the first zero ordinate. All confirm.
- No circularity: nothing in §3.1–§3.8 consumes any zero count. The one place a zero count *would* help (GAP-1) is explicitly quarantined and explicitly not used for `H3`.

## Gate

> **PROMOTABLE-with-corrections.**
>
> `(J)-avg`, **Lemma C**, **Lemma D** and `H3` (`F_q(½,T) = (1/4π)T²logT + O_q(T²)`, per-`q`, both halves) are **CONFIRMED** and independently reproduced. The `[Sel90, Lemmas 1,2]` citation is **replaceable for the banked LAW**: `S5`/`H3` in `projects/aristotle_dispatch_v33/DISPATCH.md` may be relabelled from "paper-level import, NOT proved here" to "PROVED (this lane, refereed)" **after** corrections D-1, D-2, D-3 are applied to the SOL note.
>
> `GAP-1` and `GAP-2` are **honestly scoped**: `(J)-sharp` and `(C)` still rest on Selberg 1990, and nothing in the LAW conclusion chain (`law_right_zeros_infinite_target`) touches them. That claim was verified against the Lean signature, not taken on the author's word.

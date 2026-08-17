# COLD REVIEW — Route B's fate: MIS-INSTANTIATED, and DEAD once corrected

**Date:** 2026-08-16. **Cold frontier verifier.** Independent of the authoring context; no
material under review was written by this reviewer.
**Under review:** `LAW_ROUTEB_CONDITIONAL_THEOREM.md` (incl. RB-A1/RB-A2), `LAW_AGAMMA_PROBE.md`,
`LAW_SELFBOUND_TRACE.md` §5.1.
**New probes (this review only):** `law_probes/crb_qm_identify.{py,json}`,
`law_probes/crb_smallr.{py,json}`. **No existing file was modified. No `git` was run.**
**Primary source OPENED (first time in this lane):** arXiv:1603.01494 **LaTeX e-print source**
(`arxiv.org/e-print/1603.01494` → `spec_ellip_degen_26_Feb_2016.tex`, 1951 lines), not ar5iv HTML.

---

## 0. RULING

> ### **MIS-INSTANTIATED — and the corrected instantiation is `O(1)`, so Route B via (B4★) is DEAD anyway.**
>
> **The identification error, located exactly.** `q_{M_q}` in HJL Lemma 5.3 is **not** the order of
> the degenerating elliptic point. It is the **smallest modulus** (smallest positive lower-left
> entry, cusp normalized to width 1) in the Dirichlet series of the scattering determinant — a
> **surface invariant of a fixed `M`**, which is why Hejhal's constant appears as
> `−φ'/φ(σ) → 2 log q_M` as `σ → +∞`. For the Hecke group `G_q`, normalizing the cusp width
> `λ_q = 2cos(π/q)` to 1 conjugates `S = [[0,−1],[1,0]]` to `[[0,−1/λ_q],[λ_q,0]]`, so
>
> ```
>        q_{M_q}  =  λ_q  =  2 cos(π/q)  ∈  [1, 2) ,        2 log q_{M_q}  ≤  2 log 2 = 1.3863 .
> ```
>
> **Verified numerically to full precision** (T2 below): `−φ'/φ(σ) − 1/(2σ) → 0 / log 2 / log 3`
> at `q = 3 / 4 / 6`, i.e. exactly `2 log λ_q = 0 / 0.69315 / 1.09861`, **not** `2 log q`.
> Corroborated by the lemma's own hypothesis `q_{M_q} > 1`: with `q_M = λ_q` that excludes exactly
> `q = 3` (`G_3 = PSL(2,ℤ)`, `λ = 1`) and nothing else — a fit that `q_M = q` cannot explain.
>
> **Consequence.** The budget is **bounded**, not `2 log q`. Pigeonhole (4.4) becomes
> `2 log λ_q − A_Γ ≤ 2C/δ₀ + (π²/6)C + (π²/3)δ₀(a + b log q)`: LHS bounded, RHS increasing in `q`.
> **No contradiction is ever reached, for any `C`, any `δ₀`.** `Q₀ = 1465` is withdrawn — not
> "conditional on B5", but **not implied at all** by (B4★).
>
> **Route B's positivity input is structurally vacuous, and the reason is now visible.**
> The exact Hadamard split is `−φ'/φ(½+ir) = 2 log q_M + [Γ-quotient, O(1/r)] + P_q(r) − E_q(r)`.
> The `2 log q_M` **IS** the archimedean constant of the Herglotz/Poisson representation. HJL
> Lemma 5.3 therefore says nothing more than `P_q(r) ≥ 0` — which the parent §1.2 already had for
> free. Route B was built on a tautology dressed as a budget.

---

## 1. Per-claim verdicts

| # | claim | evidence | verdict |
|---|---|---|---|
| C1 | HJL 5.3 transcription (`N-B4`) is faithful | arXiv **source** line 1108: `-\frac{\phi'}{\phi}(1/2 +ir) - \sum_{k=1}^{N} \frac{1-s_{k,q}}{(s_{k,q}-1/2)^2 + r^2} \ge 2 \log q_{M_{q}} > 0`, line 1110: `where $1/2 < s_{k,q}\le 1$ and $q_{M_{q}}>1.$` | **CONFIRMED** — the lane's transcription incl. `1−s_k` is verbatim. `N-B4` is hereby **discharged as to transcription** |
| C2 | `q_{M_q} = q` (parent §1.2(d), "`PROVED-here` from GJ Ex. 5.8") | `grep -c q_{M` on the source = **1 occurrence in the entire paper**; GJ never define `q_{M_q}`. The Hecke example (orders 2,3,N) is real but says nothing about `q_M`. HJL 97's title is *"…degenerating **hyperbolic** Riemann surfaces"* — there are **no elliptic orders** in HJL's setting, so `q_M` cannot be one | **REFUTED** — not a derivation; an inference from notational adjacency (`q_γ` vs `q_{M_q}`) |
| C3 | correct value of `q_M` for `G_q` | T2: `−φ'/φ(σ)` at `σ = 5,10,20,40,80` → `q=3`: `0.11868→0.006309`; `q=4`: `0.83160→0.699456`; `q=6`: `1.22619→1.104921`. Residual at `σ=80` is `0.00631 / 0.00631 / 0.00631` = `1/(2σ)` **identically** (the `Γ(s−½)/Γ(s)` tail), so limits are `0`, `log 2`, `log 3` = `2 log λ_q` | **`q_M = 2cos(π/q)`, PROVED-here** (closed form + the general width-1 normalization) |
| C4 | (B4★)-pointwise refuted at `q = 3,4,6`, `inf_r` LHS `< 0` | reproduced on an independent grid (`r ∈ [0.5,40.5)`, step 0.01, `mp.dps=40`, `mp.diff`): `inf = −1.907170 / −1.091564 / −0.492614` at `r = 0.5`; band means `1.32922 / 2.67618 / 3.60441` (note: `1.329/2.675/3.603`) | **CONFIRMED numerically, exactly** |
| C5 | the wrong step behind C4 | The subtracted numerator, not `q_M`, is what makes the LHS negative. With the **parent's own identity (1.4)** numerator `2(s_k−½)` and the single exceptional `s_1 = 1` (constant eigenfunction; pole of `φ` at `s=1`), the subtracted term is `1/(¼+r²)`. T3: `inf_r [−φ'/φ + 1/(¼+r²)] = 0.09283 / 0.90844 / 1.50739` vs `2 log λ_q = 0 / 0.69315 / 1.09861` → **holds with margin `+0.093 / +0.211 / +0.387`** (extended to `r ∈ (0,1]`, min at `r=0.002`: `0.09238 / 0.90446 / 1.48537`, same verdict) | **the correctly instantiated lemma is TRUE**; the printed `1−s_k` (with `s_k ∈ (½,1]`, giving `0` at `s_1 = 1`) is a **misprint / convention clash** in GJ, and parent §1.5's "non-load-bearing, both ≥ 0" is **REFUTED — it is exactly load-bearing** |
| C6 | `α = 2.000` for the order-`q` elliptic Γ-factor | independent recomputation of `Σ_{k=0}^{q−1} ((q−2k−1)/q)(π/q)cot(π(s+k)/q)` at `r = t₀`: `q = 100…4000` → `2.0529, 3.2295, 4.5079, 6.2747, 7.6389, 9.0141`, local slope in `log q` `1.6975 → 1.9840`. Analytically: weights `(q−2k−1)/q ≈ 1−2k/q`, `(π/q)cot(πk/q) ≈ 1/k` near `k=0` and `+1/(q−k)` near `k=q`, so the sum is `Σ_{k≲q/2}1/k + Σ ≈ **2 log q + O(1)**` | **CONFIRMED** (value and mechanism) |
| C7 | that `α = 2` is the `log q` coefficient of **`A_Γ`**, hence "`A_Γ` absorbs the budget" | The exact non-Blaschke part of `−φ'/φ` is `2 log q_M + [−ψ(ir)+ψ(½+ir)]`, i.e. **`A_Γ = O(1)`, `α = 0`**, and C3 measures its constant directly. `𝒜_q := Re(log K_q)'` is the **functional-equation** kernel of `κ_q = φ_q K_q`, which contains the elliptic `sin`-factors that are **not** in `φ_q` at all. So `𝒜_q ≠ A_Γ`; the `+2 log q` in `𝒜_q` is cancelled by `−2 log q` inside `𝒢_q` (branch 2 of the note's own §7.2 dichotomy) | **REFUTED as stated.** The note's §5.3(i) "resolution on branch 1" (slope(`𝒢`) `≈ −1.6…−0.4`, `R² ≤ 0.09`, 7 points) is **not evidence** — and its sign is the sign branch 2 predicts. `LAW_AGAMMA_PROBE.md` §0, AGP.3, G10/G11/G13 headline mechanism is wrong |
| C8 | "the split `−φ'/φ = 𝒢_q + 𝒜_q` is the right split relative to how the theorem consumed HJL 5.3" | see C7 | **NO.** The theorem consumed a **Blaschke/Hadamard** split; the probe measured a **functional-equation** split. The two differ by exactly the elliptic `sin`-factors, which carry the spurious `2 log q` |
| C9 | RB-A2's "T(0.2) = −0.023 ⇒ (B4★) degenerates to `P_q ≥ 0`" | The conclusion `P_q ≥ 0` (vacuous) is **CONFIRMED**, but by C3/C5, not by `α = 2`: with `A_Γ = O(1)` and budget `2 log λ_q ≤ 1.386`, (B4★) reads `P_q(r) ≥ 2 log λ_q − A_Γ(r) = O(1)` — no `log q` on either side | **right conclusion, wrong mechanism** |
| C10 | AGP §6: sliver is near-empty, no `q`-growth (1 at `q=15`, 2 at `q=21`) | not re-run (multi-hour Arb winding); receipts present and internally consistent | **NOT RE-VERIFIED** — and now **moot**: with the budget bounded there is no mass deficit to explain, so `LAW_SELFBOUND_TRACE.md` §5.1's whole "`4 log q` cannot be absorbed" audit dissolves |
| C11 | `LAW_SELFBOUND_TRACE.md` §5.1 reading 2 ("`A_Γ` contains a constant `−2 log c₀`, and `c₀` is what degenerates") | **structurally right, and it is the same object as `q_M`**: `c₀ = λ_q`. But it degenerates to `2`, not to `∞`: `α = 0`, not `α ≈ 0.078–0.7` | **half-CONFIRMED**: the term was correctly identified, its growth was wrongly guessed |

---

## 2. Consequences for the conditional theorem

1. **`Q₀ = 1465` is withdrawn.** Not "conditional on B5/(THRESH)" — **unsupported**. §5.1's
   hypothesis (B4★) is false in the form used (`2 log q`) and vacuous in the form that is true
   (`2 log λ_q − A_Γ`, bounded). Every downstream number (§5.2–5.4, `Q₀ = 1014/877`, the `C`
   sensitivity table) is void. **B7 `PROVED-here → REFUTED`.**
2. **§1.2(d) `B4.2` `PROVED-here → REFUTED`;** replace with `q_{M_q} = 2cos(π/q)`, `PROVED-here`.
3. **§1.5 claim (ii) is refuted, and B3 must be restored to the critical path.** "(B4★) supersedes
   B3 and removes three `UNKNOWN`s" is backwards: the **only** `log q` growth in Garbin–Jorgenson
   is the *averaged* counting asymptotic — `S(q_γ) = (1/π) log q_γ + O(1)`, `G_{M_q,0}(T) =
   (2C√(T−¼)/π) log Q + O(1)` with `0 < C < 1`, and `N_{M_q,0}(T) = c_0(T) log Q + O((log Q)^{3/4})`
   (source, Prop. 4.4(c), Thm 4.9 numbering of the e-print). That is **exactly B3**, with its
   unknown `C` and its `O((log Q)^{3/4})`. Route B cannot have the growth **and** avoid the
   unknown constants: the pointwise, constant-free input does not exist.
4. **§1.4 obligation `N-B4b` is discharged in the parent's favour, at a corrected value:**
   `A_Γ(r) = 2 log q_M + [−ψ(ir) + ψ(½+ir)]`, so `|A_Γ| ≤ 2 log 2 + 1/(2|r|) ≤ 1.64` for `r ≥ 2` —
   bounded and `q`-independent-up-to-`2 log λ_q`, as the parent expected. The parent's `0.25` was
   too small by the `2 log λ_q` constant it had omitted; **the `α log q` fear was unfounded.**
5. **`LAW_AGAMMA_PROBE.md`'s bankable positive survives intact:** AGP.1/G4 (first **phase**-level
   validation of the U4 + corrected-Teo mirror identity, `1.8e−11 / 3.2e−06 / 8.6e−11`) is
   independent of everything refuted here and is the lane's real yield. AGP.2/G8's *numbers* are
   confirmed; its *interpretation* is superseded by C5. AGP.3/G10's *number* is confirmed; its
   *identification* (G11/G13) is refuted.
6. **`LAW_SELFBOUND_TRACE.md`'s V1/V2 negatives stand** and are strengthened: V1 already said HJL
   5.3 is one-sided and gives no upper bound; it now also gives no useful lower bound. Its floor
   `c₂^prov ≥ 0.944` does not use (B4★) and is unaffected.
7. **What is NOT refuted:** that `φ_q` has deep poles accumulating as `q → ∞` (Hejhal Thm 7.11 /
   Selberg, and GJ Thm 4.9 quantifies the *rate* `c_0(T) log Q`). The **phenomenon** is real and
   proved-in-the-literature; only Route B's *effective* pathway to it via a pointwise budget is
   dead. Any revival must go through the **averaged** GJ statement (B3), accept its `0 < C < 1`
   and `O((log Q)^{3/4})`, and pay an averaging loss in the pigeonhole.

## 3. Ambiguity flagged, not smoothed

`q_{M_q}` is **never defined in GJ** (single occurrence, line 1108). C3 is therefore an
identification by (i) the exact `σ → ∞` asymptotics of the three arithmetic closed forms, (ii) the
standard Dirichlet-series/Herglotz structure of `φ`, and (iii) the `q_M > 1` hypothesis selecting
exactly `q ≥ 4`. It is **not** a reading of HJL 97 / Hejhal p. 160, which remain unopened
(HITL-blocked). Three independent lines agreeing at three points is strong, but the HITL item is
now the *only* way to close it — and it is cheap relative to what it decides. **If the source
should define `q_M` as anything growing in `q`, C3 falls and the ruling reverts to the RB-A2
question; nothing else in this review depends on C3** (C5's corrected inequality holds with
`q_M = λ_q` and would hold a fortiori for any smaller constant, and C7's `A_Γ = O(1)` follows from
the Γ-quotient alone once the constant is `r`-independent).

## 4. Recommended disposition

- Mark Route B **CLOSED** as an effective route through (B4★). Do not spend further compute on
  B5/B5b/(THRESH) *as a means of consuming a `2 log q` budget*; B5-J's Jensen counting retains
  independent value as a resonance-counting instrument, but it no longer has a theorem to feed.
- Amend the three notes at the identified steps (B4.2, §1.5(ii), AGP G10/G11/G13) rather than
  retracting them; the measurements are sound, the identifications are not.
- Open the single HITL item: Hejhal LNM 1001 vol. 2 p. 160 / HJL *JFA* **149** (1997) Lemma 5.3 —
  read the **definition of `q_M`**. One page decides §3.

**Probes:** `crb_qm_identify.py` (T1 grid, T2 `σ→∞`, T3 corrected inequality, T4 elliptic slope),
`crb_smallr.py` (T3 extended to `r ∈ (0,1]`). Interpreter
`/Users/za/miniforge3/envs/pari-arb/bin/python3`, `mp.dps = 40`.
**Source:** arXiv:1603.01494 e-print LaTeX, lines 1108–1110 (the lemma), 1050–1105 (Thm on
non-compact counting functions), 890–1000 (Prop. `S(q_γ) = (1/π)log q_γ + O(1)`), 1235–1256
(Hecke example), bibliography (`HJL 97` = *hyperbolic* degeneration).

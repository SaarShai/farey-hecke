# PGT-1 — What the LAW licenses for the Prime Geodesic Theorem on non-arithmetic Hecke surfaces

**Date:** 2026-08-23. **Lane:** G / PGT-1. **Author lane label:** SOL.

**STATUS: UNREFEREED. CONJECTURAL. NOT A BANKED RESULT.**
Every statement below is a lane-internal derivation pending a cold referee.
Two of the four ingredients are receipted primary source; two are
lane-internal sketches, marked as such at point of use. Nothing here is
promoted; nothing here is committed as a claim.

**Headline verdict, stated first so it cannot be skimmed past:**

> The LAW is **PGT-error-neutral**. It yields a **structural** correction to
> the divisor bookkeeping of the Selberg zeta on non-arithmetic Hecke
> surfaces, plus a quantitative **lower** bound on the number of off-line
> Selberg-zeta zeros. It does **NOT** yield an Ω-result, and it does **not**
> obstruct, improve, or complicate any known or conjectured prime-geodesic
> error exponent. The `NOGO_AUDIENCE_SURVEY.md` line calling the
> prime-geodesic row a **"usable input"** with **"high"** redirect value is
> **over-sold** by this lane's reading and should be downgraded (see §7).

---

## 1. The pinned objects

Fix a finite integer `q ≥ 3`, non-arithmetic (`q ∉ {3,4,6}`). Let
`Γ = G_q ⊂ PSL(2,R)` be the Hecke triangle group, `M_q = Γ\H` the cofinite
one-cusp orbifold, `φ_q(s)` the scalar trivial-character scattering
determinant, `Z_q(s)` the Selberg zeta function of `M_q`.

Prime-geodesic counting functions, standard:

```
ψ_Γ(x) = Σ_{N(P)^k ≤ x} log N(P),      ψ_{1,Γ}(x) = ∫_1^x ψ_Γ(t) dt
```

`P` over primitive hyperbolic conjugacy classes, `N(P) = exp(length P)`.

**The LAW, as banked** (`LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_SOL.md`,
promotion block 2026-08-19 + second-audit block 2026-08-20, CONFIRMED by two
lineage-independent cold referees):

- (C) weighted count, all finite `q ≥ 3`:
  `N_q(T) := Σ_{φ_q(ρ)=0, |γ|<T, β>1/2} (β − 1/2) = (1/2π)·T log T + A_q·T + O_q(log T)`
- Hence infinitely many nonreal zeros `ρ = β + iγ` of `φ_q` with `β > 1/2`,
  and multiplicity-matched poles at `1 − ρ` with `Re(1−ρ) < 1/2`.
- Banked caveats consumed here: **no** effective first height, **no**
  `q`-uniform error, **no** consumable numerics for `A_q`, and the LAW is
  **non-discriminating** for arithmeticity (`q = 3` has the same property).

---

## 2. WHERE φ_q enters the prime geodesic explicit formula — pinned

There are two equivalent entry points. This lane pins the **divisor** entry
point, because it is the one that is fully receipted.

### 2.1 Entry point A (receipted): φ_q's off-line zeros ARE Selberg-zeta zeros

Friedman–Jorgenson–Smajlović (arXiv:2011.12795), §2.5, print the divisor of
`Z(s)` for a **cofinite Fuchsian group with elliptic elements** (orbifold
case, exactly our setting), citing Venkov and Hejhal Vol. II p. 499. Item 6
of that divisor list is the load-bearing line:

> `6. Zeros at each s = 1 − ρ, 1 − ρ̄ where ρ is a zero of φ(s) with Re(ρ) > 1/2 and Im(ρ) > 0;`

and §2.4 item 5 of the **φ-divisor** list gives the matching poles:

> `5. Poles of the form 1 − ρ and 1 − ρ̄ with Re(ρ) > 1/2 and Im(ρ) > 0;`

Receipt (verbatim `grep -n` on `pdftotext` output; the PDF sha256 matches the
one already banked in `LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_SOL.md` §7):

```
$ shasum -a 256 /tmp/fjs.pdf
36c9d020fcc7d0118264c486330db9936f866670c45c0e77b185cdc2b9127228  /tmp/fjs.pdf
$ pdftotext /tmp/fjs.pdf /tmp/fjs.txt && grep -n "Zeros at each s = 1" /tmp/fjs.txt
486:6. Zeros at each s = 1 − ρ, 1 − ρ where ρ is a zero of φ(s) with Re(ρ) > 21 and Im(ρ) > 0;
$ grep -n "Poles of the form 1" /tmp/fjs.txt
380:5. Poles of the form 1 − ρ and 1 − ρ with Re(ρ) > 1/2 and Im(ρ) > 0;
$ sed -n '464,466p' /tmp/fjs.txt
the divisor of the Z(s) (see [24, p. 49] [12, p. 499]):
```

(`[12]` = Hejhal LNM 1001 Vol. II; `[24]` = Venkov.)
Note: "21" is `pdftotext` mangling of `1/2` (stacked fraction). Treat the two
displayed lines as **TRANSCRIPTIONS**, per the same relabelling discipline the
second audit imposed on the LAW note.

**Consequence, immediate and unconditional given the LAW:**

> `Z_q(s)` has **infinitely many nonreal zeros with `Re s < 1/2`**, located at
> `1 − ρ` and `1 − ρ̄` for the LAW's off-line `φ_q`-zeros `ρ`.

### 2.2 Entry point B (the ρ-sum): the explicit formula

Hejhal's explicit formula with error term for `ψ_{1,Γ}`, as transcribed by
Avdispahić (arXiv:1701.01642, eq. (1), citing Hejhal LNM 548 Vol. I,
Theorem 6.16, p. 110):

```
ψ_{1,Γ}(x) = α0 x + β0 x log x + α1 + β1 log x + F(1/x)
             + x²/2 + Σ_{ρ, |γ|<T} x^{ρ+1}/(ρ(ρ+1)) + O(x² log x / T)
```

Receipt:

```
$ shasum -a 256 /tmp/pgt_avd.pdf
457877cea428c7b2f20a20ed8e3b9d4b33511c3073f9d0de65975e0a42abe72c  /tmp/pgt_avd.pdf
$ nl -ba /tmp/pgt_avd.txt | sed -n '87,96p'
    87  Proof of Theorem 1. We shall take the same starting point as in [6], i.e. Hejhal's
    89  explicit formula with an error term for the function ψ1,Γ (x) = ψΓ (x) dx (cf. [5,
    92  Theorem 6.16. on p. 110]):
    94  (1)
    96  ψ1,Γ (x) = α0 x + β0 x log x + α1 + β1 log x
```

**GAP, declared:** Avdispahić's `Γ` is **strictly hyperbolic** (compact
surface), so his eq. (1) is *not* the cofinite statement, and his sentence
"the complex zeros of `Z_Γ` are of the form `ρ = 1/2 ± iγ`" is a
compact-case sentence that is **FALSE verbatim for cofinite `Γ`** by §2.1.
The correct cofinite reference is Hejhal LNM 1001 Vol. II (Ch. 10 / Ch. 6)
and Iwaniec, *Spectral Methods in Automorphic Forms* 2nd ed., Ch. 10 — **NOT
read in this lane; not receipted; a referee must pin the equation number.**
What this lane **assumes** (marked CONJECTURAL-IN-LANE, assumption **(EF)**):

> **(EF)** In the cofinite one-cusp explicit formula for `ψ_Γ` / `ψ_{1,Γ}`,
> the zeros of `Z_Γ` supplied by §2.1 item 6 enter the `ρ`-sum in the same
> shape as every other zero, i.e. as `x^ρ/ρ` (resp. `x^{ρ+1}/(ρ(ρ+1))`),
> with the standard truncation error `O(x² log x / T)`.

(EF) is the standard shape in every treatment this lane has seen, and is the
same shape by which the continuous-spectrum term
`−(1/4π)∫ (φ'/φ)(1/2+it) h(t) dt + (1/4)φ(1/2)h(0)` is converted to residues.
But it is **assumed here, not verified here.**

---

## 3. The quantitative content: how many off-line zeros, and how far off

This is the strongest *new* quantitative statement the LAW licenses. It is a
**lower** bound on an unweighted count, extracted from the LAW's weighted
asymptotic by an a-priori right-edge bound.

**Lemma 3.1 (right-edge zero-free half-plane).** There is a finite
`σ₀(q) > 1/2` such that `φ_q` has no zero with `Re s > σ₀(q)`.

*Proof sketch (lane-internal, elementary).* By (NF)/(N) of the LAW note,
in `Re s > 1/2` the zeros of `φ_q` are exactly the zeros of
`L*_q(s) = 1 + Σ_{n≥2} a_{q,n} λ_{q,n}^{−s}` with `λ_{q,n} > 1`. The series
converges absolutely for `Re s` large, so pick `σ₀(q)` with
`Σ_{n≥2} |a_{q,n}| λ_{q,n}^{−σ₀(q)} < 1`; then `|L*_q − 1| < 1` there. ∎
**Not effective in this lane** — `σ₀(q)` is not instantiated, and the LAW
note explicitly banks no effective height.

**Proposition 3.2 (off-line zero count, lower bound).** Write
`N^off_q(T) = #{ρ : φ_q(ρ) = 0, β > 1/2, |γ| < T}` with multiplicity. Then,
for every finite `q ≥ 3`,

```
N^off_q(T)  ≥  (1 / (2π (σ₀(q) − 1/2))) · T log T · (1 + o_q(1))       (P1)
```

*Proof.* Each summand of the LAW's `N_q(T)` obeys
`0 < β − 1/2 ≤ σ₀(q) − 1/2` by Lemma 3.1, so
`N_q(T) ≤ (σ₀(q) − 1/2) · N^off_q(T)`. Insert (C). ∎

Rounding discipline: `(P1)` is a **lower** bound and its constant is rounded
**DOWN** (any valid `σ₀` may be enlarged, which only weakens the constant —
so the bound is safe under any over-estimate of `σ₀`). Contrapositively it is
**not** claimed sharp.

**Corollary 3.3 (Selberg-zeta form).** For every finite `q ≥ 3`, the number
of zeros of `Z_q(s)` with `Re s < 1/2`, `Im s ≠ 0`, `|Im s| < T` is at least
`(1/(2π(σ₀(q)−1/2))) · T log T · (1+o_q(1))`. (§2.1 item 6, plus (P1).
The map `ρ ↦ 1 − ρ` is injective and off-line zeros of `Z_q` in `Re < 1/2`
arise from no other divisor item except finitely many real ones.)

### 3.4 Independent consistency check at q = 3 (the only place we can check)

`q = 3` is arithmetic and outside the target class, but it is the one case
with a closed form:
`φ_3(s) = √π · Γ(s−1/2)/Γ(s) · ξ(2s−1)/ξ(2s)`, so the `Re > 1/2` zeros are
`s = (1 + ρ_ζ)/2` over nontrivial zeta zeros `ρ_ζ`. Under RH, `β = 3/4`
exactly, so `β − 1/2 = 1/4`, and `|Im s| < T ⟺ |γ_ζ| < 2T`. Riemann–von
Mangoldt with both signs of `γ_ζ` gives `2 · (2T/2π) log(2T/2π) ~ (2/π) T log T`
such zeros, and the weighted sum is `(1/4)·(2/π) T log T = (1/2π) T log T`,
**exactly the leading coefficient of (C)**. This reproduces, by an
independent route, the numeric agreement the second cold audit reports at
`q = 3`. It also shows (P1)'s slack: with `σ₀ = 1` (safe, since
`ξ(2s−1)` zeros have `β < 1`), (P1) gives `≥ (1/π) T log T` against a truth
of `(2/π) T log T` — a factor-2 loss, as expected from a max-vs-average
argument.

### 3.5 What (P1) is NOT — density relative to the full zero set

The Weyl law for `M_q` (area `|F_q| = π(1/2 − 1/q)`) gives eigenvalue count
`~ (|F_q|/4π) T² = ((1/2 − 1/q)/4) T²`, so `Z_q` has `≍_q T²` zeros on
`Re s = 1/2` up to height `T`. Therefore:

> **The off-line zeros are a DENSITY-ZERO subset of the zeros of `Z_q`**
> (`T log T = o(T²)`). "Positive proportion" is true **only** relative to the
> scattering-zero count, never relative to the Selberg-zeta zero count. Any
> write-up must say which denominator it means.

---

## 4. The PGT consequence — derivation, and the honest verdict

**Proposition 4.1 (the resonance block is subordinate).** Assume (EF), and
assume the standard unweighted upper bound

> **(U)** `N^{tot}_q(T) := #{ρ : φ_q(ρ)=0, β>1/2, |γ|<T} = O_q(T log T)`,

which follows from a Jensen/Littlewood count using the LAW's vertical bound
(P) `L*_q(σ+it) = O_q(|t|^{1/2})` on `1/2 ≤ σ ≤ 3/2` together with
`L*_q(s) = 1 + O_q(e^{−c_q Re s})` on the right — **SKETCH ONLY, not carried
out here**. Then the total contribution to `ψ_Γ(x)` of the `Z_q`-zeros of
§2.1 item 6 is

```
Σ_{ρ off-line, |γ|<T}  x^{1−ρ}/(1−ρ)   ≪_q   x^{1/2} (log x)²          (P2)
```

with `T = x`.

*Proof.* `|x^{1−ρ}| = x^{1−β} < x^{1/2}` **strictly**, since `β > 1/2`.
Partial summation on (U) gives `Σ_{|γ|<T, |γ|≥1} 1/|γ| ≪_q (log T)²`; the
finitely many `|γ| < 1` terms are `O_q(1)`. ∎

Rounding discipline: (P2) is an **upper** bound and both the exponent
(`x^{1/2}`, not `x^{1/2−δ}`, even though every individual term is strictly
smaller) and the log power (`2`, not `1`) are rounded **UP**.

**Verdict, in the three candidate classes named in the brief:**

- **(a) Ω-result — NO.** An Ω-result would need the continuous/scattering
  block to *exceed* the exponent the discrete spectrum already forces. It
  does the opposite. The off-line zeros of `φ_q` sit at `Re > 1/2` but they
  enter the geodesic explicit formula **reflected**, at `1 − ρ` with
  `Re < 1/2`; their block is `≪ x^{1/2}(log x)²`, strictly below both the
  trivial bound `O(x^{3/4})` and the conjectured optimum `O(x^{1/2+ε})`.
  Additionally, an Ω-result would require a **non-cancellation** lower bound
  on an oscillating sum; the LAW supplies **no** information on the arguments
  `γ` (no height, no gaps, no linear-independence), so no such lower bound is
  reachable from banked material even in principle.
- **(b) Structural — YES, this is the licensed class.** See §5.
- **(c) Remark-only — YES for the PGT error term itself.** The LAW changes
  no exponent, no log power, and no known or conjectural PGT statement.

---

## 5. The strongest licensed statement (verbatim, for quotation)

> **Remark (structural; UNREFEREED, CONJECTURAL, conditional on (EF) and (U)).**
> Let `q ≥ 3` be finite and non-arithmetic, and let `M_q = G_q\H` be the
> corresponding one-cusp Hecke triangle orbifold. Then the Selberg zeta
> function `Z_q` has infinitely many nonreal zeros off the critical line —
> at least `c_q · T log T` of them with `|Im s| < T`, for some `c_q > 0` —
> all of them in the open half-plane `Re s < 1/2`, arising as the reflections
> `1 − ρ` of the off-line zeros `ρ` of the scattering determinant `φ_q`.
> Consequently the compact-surface description of the divisor of a Selberg
> zeta function ("all nontrivial zeros lie on `Re s = 1/2`, apart from
> finitely many real ones"), which is still sometimes carried over verbatim
> to the cofinite setting, is false for every non-arithmetic Hecke surface,
> and is now known to be false by an infinite, quantitatively counted margin
> rather than by a hypothetical one. It is false **harmlessly**: because the
> offending zeros lie strictly to the **left** of the critical line, their
> total contribution to the prime geodesic explicit formula is
> `O_q(x^{1/2} (log x)²)`, which is dominated by the critical-line block.
> The prime geodesic theorem on `M_q`, its trivial error exponent `3/4`, and
> the conjectured exponent `1/2 + ε` are therefore all **unaffected**. No
> Ω-result follows.

**Class: STRUCTURAL (divisor/bookkeeping correction with a quantitative
count), plus REMARK-ONLY on the error term. NOT an Ω-result.**

---

## 6. Estimate ledger (rounding discipline, one line each)

| Quantity | Value used | Direction rounded | Basis |
|---|---|---|---|
| `Σ (β−1/2)`, `|γ|<T` | `(1/2π) T log T + A_q T + O_q(log T)` | as banked | LAW (C), 2× CONFIRMED |
| `β` upper cutoff | `σ₀(q) < ∞`, not instantiated | UP (weakens P1) | Lemma 3.1, lane sketch |
| `N^off_q(T)` | `≥ (1/(2π(σ₀−1/2))) T log T (1+o(1))` | DOWN | (P1) |
| `N^tot_q(T)` | `O_q(T log T)` | UP | (U), **SKETCH ONLY** |
| `|x^{1−ρ}|` | `< x^{1/2}` | UP to `x^{1/2}` | `β > 1/2` strictly |
| `Σ 1/|γ|` | `≪_q (log x)²` | UP | partial summation on (U) |
| resonance block | `≪_q x^{1/2}(log x)²` | UP | (P2) |
| on-line block / trivial bound | `O(x^{3/4})` | as printed | Avdispahić Thm 1 (compact); cofinite analogue assumed |
| `Z_q` on-line zero count | `≍_q T²` | order only | Weyl, `|F_q| = π(1/2 − 1/q)` |

---

## 7. Ledger correction requested to a sibling note

`NOGO_AUDIENCE_SURVEY.md` (2026-08-22), §2 table, prime-geodesic row, reads:

> "**direct object overlap** … off-line resonances enter the PGT explicit
> formula … **high** — the LAW supplies the first proven off-line resonance
> family their error-term analyses must accommodate"

The first clause is **correct and now receipted** (§2.1). The redirect-value
clause is **over-sold**: an error-term analysis does not have to
"accommodate" a block that is `O(x^{1/2}(log x)²)` when the barrier it is
fighting is `x^{3/4}` and its target is `x^{1/2+ε}`. This lane's
recommendation: downgrade that row's redirect value from **high** to
**low–moderate**, and restate the value as *structural/bookkeeping* rather
than *usable input*. This note does not edit that file (append-only,
one-file-per-lane discipline); the correction is recorded here for the MAP
owner to action.

---

## 8. What a referee will attack

1. **(EF) is unverified.** The whole §4 estimate presumes the shape of the
   cofinite explicit formula. The referee should demand Hejhal LNM 1001
   Vol. II Ch. 10 (or Iwaniec Ch. 10, Thm 10.2) with an equation number, and
   should check whether the cofinite formula carries an extra explicit
   `φ'/φ` integral term *in addition to* the reflected-zero residues — if it
   does, §4 must estimate that integral directly rather than by residues, and
   the log power in (P2) may change. **Most likely point of failure.**
2. **(U) is a sketch.** The Jensen/Littlewood unweighted count from (P) is
   standard but is not carried out. Without (U) there is no `Σ 1/|γ|` bound
   and (P2) collapses. Note (C) alone does **not** give (U): (C) is weighted,
   and a weighted asymptotic bounds an unweighted count only from **below**
   (that is exactly Prop 3.2), never from above.
3. **`σ₀(q)` is not effective**, so `c_q` in §5 is not a number. A referee
   entitled to ask "how many, concretely, below height 100?" gets nothing.
   The LAW banks no effective first height; this note inherits that.
4. **Density-denominator equivocation.** §3.5 exists because the natural
   sloppy sentence ("a positive proportion of the zeros are off the line") is
   false against the Weyl `T²` denominator. Any referee will test this
   sentence first.
5. **Novelty.** For `q = 3` all of this is classical (`Z` has zeros at
   `ρ_ζ/2`), and the second cold audit already banked Hejhal Thm 7.11 /
   Cor. 7.12 (pp. 577–579) as a printed partial antecedent giving
   `φ_N`-zeros/poles in prescribed rectangles for all sufficiently large `N`.
   The genuinely new content is: **all** finite `q`, with a **count**. A
   referee may reasonably rate that as a remark, not a theorem.
6. **The `1 − ρ` reflection direction.** A hurried reader will assume
   `Re ρ > 1/2` gives `x^{β}` with `β > 1/2` and therefore an Ω-result. §2.1
   item 6 is the exact line that refutes this. Any write-up must display it.
7. **Multiplicity and the `ρ ↦ 1 − ρ` injectivity** in Cor. 3.3, and whether
   the `Re < 1/2` real-zero item (FJS `Z`-divisor item 5) can overlap the
   nonreal count. Claimed disjoint here (real vs. nonreal); trivially true
   but stated without proof.
8. **Kelmer-ledger contamination.** This note consumes only the leading
   coefficient of (C), never `A_q`, `B_q`, `C_q`, per the second audit's
   explicit warning. A referee should verify no numeric leaked in.

---

## 9. Source list

- Friedman–Jorgenson–Smajlović, *Super-zeta functions and regularized
  determinants associated to cofinite Fuchsian groups with finite-dimensional
  unitary representations*, [arXiv:2011.12795](https://arxiv.org/abs/2011.12795)
  — §2.4 (divisor of `φ`), §2.5 (divisor of `Z`, citing Venkov p. 49 and
  Hejhal Vol. II p. 499). sha256 `36c9d020…7228` (matches banked copy).
- Avdispahić, *On Koyama's refinement of the prime geodesic theorem*,
  [arXiv:1701.01642](https://arxiv.org/abs/1701.01642), eq. (1) transcribing
  Hejhal LNM 548 Vol. I, Thm 6.16, p. 110. sha256 `457877ce…e72c`.
  **Compact-`Γ` setting** — used only for the shape of the `ρ`-sum.
- Avdispahić, *Prime geodesic theorem of Gallagher type*,
  [arXiv:1701.02115](https://arxiv.org/abs/1701.02115) — same shape, compact.
- Hejhal, LNM 1001 Vol. II, Ch. 10 / Ch. 6 — the correct cofinite explicit
  formula. **NOT READ IN THIS LANE.**
- Iwaniec, *Spectral Methods in Automorphic Forms*, 2nd ed., Ch. 10 —
  the standard `PSL(2,Z)` cofinite statement. **NOT READ IN THIS LANE;**
  cited from general knowledge only, equation number deliberately omitted.
- In-repo: `LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_SOL.md` (LAW + both cold
  audit blocks), `LAW_HEJHAL_CH6S12_CH11S3_EXTRACT.md`,
  `NOGO_AUDIENCE_SURVEY.md`.

**Final lane label: UNREFEREED / CONJECTURAL. Class = STRUCTURAL +
REMARK-ONLY. Explicitly NOT an Ω-result. READY FOR COLD REFEREE.**

---

## §10 CORRECTION BLOCK (dated append-only, 2026-08-23, post cold referee)

Referee: PGT1_EXPLICIT_FORMULA_COROLLARY_REFEREE.md — verdict
PROMOTABLE-WITH-CORRECTIONS. All three load-bearing claims (reflection into
Re s < 1/2; O_q(x^{1/2}(log x)²); Prop 3.2 constant) independently
re-derived and CONFIRMED; the q=3 cross-check reproduced (factor-2 slack
exact). The corrections below SUPERSEDE §§1–6 wherever they conflict; body
text above untouched (append-only rule).

### C1 (D1 — HIGH): fundamental-domain area factor 2.
§3.5/§6 printed |F_q| = π(1/2 − 1/q). CORRECT (Gauss–Bonnet, (2,q,∞) von
Dyck): |F_q| = **2π(1/2 − 1/q)**; q=3 check: π/3 ✓ (the printed formula gave
π/6). Downstream Weyl constant corrected: ((1/2−1/q)/**2**)·T², not /4
(q=5: 0.15, not 0.075). The slip was the reflection-triangle area; the
density conclusion's ORDER (T² vs T log T) is unaffected.

### C2 (D2 — HIGH): density-zero claim made CONDITIONAL.
"Z_q has ≍_q T² zeros on Re s = 1/2" is NOT proven for non-arithmetic G_q —
the trace formula gives only N_d(T) + M(T) ~ (|F_q|/4π)T² (discrete
spectrum + scattering winding), and the Phillips–Sarnak expectation is
precisely N_d(T) = o(T²) with M(T) carrying the T². Corrected statement:
the COMBINED count N_d + M is ≍_q T², unconditionally; the claim "the
off-line zeros are a density-zero subset OF THE ON-LINE ZETA ZEROS" is
CONDITIONAL on a discrete Weyl law N_d(T) ≫ T log T for G_q, which is open
(and, in an extreme cusp-dissolution scenario, false). The off-line set IS
unconditionally density-zero against the combined T² count.

### C3 (D3 — HIGH): mandated Hejhal disclosure attached to the quotable block.
The §5 quotable paragraph and the §0 headline are amended to carry, wherever
they travel: "Printed partial antecedent: Hejhal LNM 1001, Theorem 7.11 and
Corollary 7.12 (pp. 577–579) prove zeros/poles of φ_N in prescribed
rectangles for all sufficiently large N; the present count covers ALL finite
q ≥ 3 with an explicit T log T lower bound." Mandate:
LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_SOL.md:461-465.

### C4 (D4 — HIGH): [Sel90] inheritance declared.
Add to §1's consumed-caveats list and read into every "unconditional given
the LAW" in this note: the LAW's (C) count rests on [Sel90, Lemmas 1, 2],
unread by author and both referees at time of writing; per the sibling NOGO
note's binding LEDGER-RULE clause, "PROVED"/"CONFIRMED" here means proved
modulo that one unread citation. (The SEL90 bypass discharges the
(J)-avg/H3 route for the LAW's conclusion chain, but the citation standing
declared by the second audit still binds this note's (C) usage as written.)

### C5 (D5–D9, acknowledged):
- (D5) §4's ψ_{1,Γ}→ψ_Γ slide: the cited Avdispahić ψ_Γ formula absorbs the
  zero-sum into the O(x^{3/4}) error; the derivation as written does not
  attach to a cited formula. The VERDICT stands by the easier argument: any
  reflected block sits at Re < 1/2, hence below x^{1/2}. Prop 4.1's proof is
  reread as that easier argument.
- (D6) "all of them in Re s < 1/2" now receipted: referee extracted the full
  FJS Z-divisor list 1–7; items 1/2/5/7 real-or-on-line, 3 at s=1/2, 4 are
  poles — item 6 is the ONLY source of nonreal off-line Z-zeros. The strong
  reading ("all off-line zeros of Z_q") is licensed.
- (D7) Prior art: Garbin–Jorgenson 2018 pp.161–163 (quantified accumulation
  for Hecke G_N) is the sharpest banked antecedent — cite wherever §8.5's
  novelty claim travels.
- (D8) §5's "every non-arithmetic Hecke surface" corrected to "every finite
  q ≥ 3, non-arithmetic in particular" — the property is NON-DISCRIMINATING
  (q=3 has it too); never an arithmeticity signature.
- (D9) "rounded UP (2, not 1)" withdrawn: 2 is the true log power under (U),
  not safety slack.

### Post-correction status
Remark-class, refereed PROMOTABLE-WITH-CORRECTIONS (applied above). Headline
unchanged and referee-confirmed: PGT-error-neutral, NO Ω-result; the no-Ω
argument was the part the referee "could not break". Gates before any §5
quotation leaves the lane: C1–C4 (done above); before paper-level use: C5.

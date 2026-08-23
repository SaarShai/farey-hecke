# SEL90-BYPASS — independent re-derivation of the Jensen/Littlewood rectangle input `(J)`

**Date:** 2026-08-22. **Lane:** G / SEL90-BYPASS. **Author lane:** sol.
**Status: UNREFEREED throughout.** Nothing in this note is promoted. It is
append-only, touches no other file, and no git command was run.

**Object.** Discharge the last unread citation in the LAW proof chain —
Selberg 1990, *Remarks on the distribution of poles of Eisenstein series*
(`[Sel90, Lemmas 1, 2]`), reached only through Kelmer arXiv:1402.4780 (4.20) —
by re-deriving its content from the standard complex-analytic toolkit and the
inputs already banked in this lane.

---

## 0. Verdict

> **(J) REDERIVED in the form the chain consumes; citation replaceable there.**
> **PARTIALLY for the sharp printed form.** One residual, `GAP-1`, blocks the
> printed `O(log T)` remainder at every height `T`; it does **not** block the
> statement the chain actually imports (`H3`).

Precisely:

| Form | What it says | Status after this note |
|---|---|---|
| `(J)-sharp` | rectangle identity with remainder `O_q(log T)` for **every** `T` | **PARTIALLY REDERIVED** — everything closed except a pointwise negative-part bound at height `T` (`GAP-1`) |
| `(J)-avg` | same identity, remainder `O_q(log T)` for **some** `T* ∈ [T−1, T]` | **REDERIVED** (§3.7, unconditional on the banked inputs) |
| `H3` = `F_q(1/2,T) = (1/4π)T² log T + O_q(T²)`, lower half | what `projects/aristotle_dispatch_v33/DISPATCH.md` imports | **REDERIVED** (§3.8, from `(J)-avg` + monotonicity of `F_q`) |

Since `DISPATCH.md` §2 imports only `H3` (lower half), and the 2026-08-19
promotion block of `LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_SOL.md` records that
the LAW existence conclusion needs only `F_q(1/2,T) = (1/4π)T²log T + O_q(T²)`,
**the `[Sel90]` citation is replaceable for the banked LAW**. It is *not* yet
replaceable for the sharp asymptotic `(C)`, which consumes `(J)-sharp` through
the finite-difference step `(DIF)`.

A by-product of the re-derivation, §3.5, is an exact closed form for the
remainder. It is verified numerically at `q = 3` to 14–16 significant digits
(§4) — this is a check of the *derivation*, not merely of the printed result.

---

## 1. The pinned statement `(J)`, exactly as consumed

### 1.1 In our banked chain

`research_notes/rh_goals_2026-08-14/lane_g/LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_SOL.md`,
§4.1, lines 208–224, verbatim:

~~~
208  Fix \(\alpha\ge1/2\), and let
210  F_q(\alpha,T)=
211  \sum_{\substack{L_q^*(\rho)=0,\;|\Im\rho|\le T\\
212  \Re\rho=\beta>\alpha}}
213  (T-|\Im\rho|)(\beta-\alpha).
215  Let \(\sigma_j>\alpha\) be the finitely many poles of \(L_q^*\), with
216  multiplicity. Jensen/Littlewood's rectangle, with the right side sent to
217  \(+\infty\) using \(L_q^*(s)=1+O_q(e^{-c_q\Re s})\), gives Kelmer's equation
218  (4.20) specialized to \(d=2\):
220  F_q(\alpha,T)=
221  \frac1{2\pi}\int_{-T}^{T}(T-|t|)\log|L_q^*(\alpha+it)|\,dt
222  +T\sum_{\sigma_j>\alpha}(\sigma_j-\alpha)+O_q(\log T).
223  \tag{J}
~~~

Downstream consumption, `projects/aristotle_dispatch_v33/DISPATCH.md`:

* line 35 — `| S5 | Jensen/Littlewood rectangle `(J)` = Kelmer (4.20) = `[Sel90, Lem 1,2]` | complex analysis | no |`
* line 73 — `| **H3** | `hgrowth` | `F_q(1/2,T) = (1/4π) T² log T + O_q(T²)`, lower half only | promotion block; `(J)` ∘ `(I)` | **paper-level import, NOT proved here** |`
* line 86 — `The LAW's analytic weight lives entirely in H3.`
* lines 158–160 — `(J)` … `the residual dependency the second audit could not discharge, since no one in the lineage has read Selberg 1990.`

Second audit, `LAW_SECOND_AUDIT_REFEREE.md` line 46:
`The complex-analytic engine is [Sel90, Lemmas 1, 2], reached only through Kelmer's transcription in (4.20). Neither the author, nor the first referee, nor I have read Selberg 1990.`

So the residual is exactly `(J)` at `α = 1/2`, `q ≥ 3`, for `L_q^*` as normalised
in `(N)`/`(NF)` of the SOL note.

### 1.2 In Kelmer arXiv:1402.4780

Fetched fresh for this note; the file is byte-identical to the one the earlier
lane notes used (sha256 receipt in §5). Verbatim from `pdftotext -layout`,
p. 19–20:

~~~
Lemma 4.7. For any α > (d−1)/2 we have
      ∫_α^∞ arg(L*(σ + iT))dσ = O(log(T)).
...
Proof of Theorem 3. The zeroes and poles of ϕ(s) in ℜ(s) > (d−1)/2 are the
same as the zeroes and poles of L*(s) in ℜ(s) > (d−1)/2. By Proposition
4.4, L*(s) satisfies all the assumptions needed for [Sel90, Lemma 1,2],
stating that for any α ≥ (d−1)/2,
(4.20)  Σ_{|γ|≤T, β>α} (T − |γ|)(β − α)
        = (1/2π) ∫_{−T}^{T} (T − |t|) log |L*(α + it)|dt
          + T Σ_{σ_j>α} (σ_j − α) + O(log(T)),
where the last sum is over the finitely many poles in ((d−1)/2, d].
~~~

and the attribution, p. 12 / Remark 0.2:

~~~
We conclude with the proof of Theorem 3, generalizing the results
of [Sel90] on the distribution of poles of Eisenstein series to hyperbolic
manifolds of higher dimensions. Our proof is very similar to Selberg's
original proof...
Remark 0.2. For hyperbolic surfaces this result is due to Selberg [Sel90]
~~~

**Pinned observation (load-bearing).** Kelmer's own Lemma 4.7 — the
argument-integral bound that would supply the remainder — is stated for
`α > (d−1)/2` **strictly**, and likewise Lemma 4.6 for `α ≥ α₀ = d − 5/4`.
The boundary case `α = (d−1)/2`, which is the *only* case the LAW uses, is
delegated **entirely** to `[Sel90, Lemma 1,2]`. So the unread citation is not
decorative: it carries the boundary case. This note therefore has to derive the
boundary case, not merely paraphrase Kelmer.

(Transcription note, per the second audit's repair 4: the `~~~` blocks above
are hand-cleaned `pdftotext -layout` output — mathematical content preserved,
LaTeX-ish glyph reflow applied. The raw file is receipted in §5.)

---

## 2. Standing inputs (all banked; none re-proved here)

Throughout `q ≥ 3` is fixed, `α = 1/2` unless stated, and `L* := L_q^*`.
Constants `C_q, c_q, …` depend on `q` only. Sources are the banked extracts
`LAW_HEJHAL_S7_EXTRACT.md`, `LAW_HEJHAL_CH6S12_CH11S3_EXTRACT.md` and
`LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_SOL.md` §3.

* **(D)/(NF)** `φ_q(s) = √π (Γ(s−½)/Γ(s)) d_q(1) g_{q,1}^{−2s} L*(s)`, with
  `L*(s) = 1 + Σ_{n≥2} a_{q,n} λ_{q,n}^{−s}`, `λ_{q,n} > 1`, absolutely
  convergent for `ℜs` large, coefficients real. Hejhal (7.5).
* **(E)** Right-edge normalisation: there are `σ₁ = σ₁(q) ≥ 3/2` and
  `A_q, c_q > 0` with `|L*(s) − 1| ≤ A_q e^{−c_q ℜ s} ≤ ½` for `ℜ s ≥ σ₁`.
  Immediate from (D). In particular `|L*| ≥ ½` and `|L*| ≤ 2` on `ℜ s ≥ σ₁`,
  and `L*` has **no zeros and no poles** in `ℜ s ≥ σ₁`.
* **(F)** `φ_q(s)φ_q(1−s) = 1`; `φ_q` meromorphic on ℂ, **of order at most 2**,
  holomorphic on `ℜ s > ½` except finitely many poles, all **real**, in `(½,1]`.
  FJS §2.4 / Venkov. (Cited in the SOL receipt at
  `/tmp/fjs_2011.12795.txt` lines 261–304.)
* **(U)/(G)** `|φ_q(½+it)| = 1` for `t ≠ 0`, hence
  `|L*(½+it)| = κ_q (|t| tanh(π|t|))^{1/2}` with `κ_q = g_{q,1}/(√π|d_q(1)|)`.
  **Consequence used repeatedly:** `L*` has **no zero on `ℜ s = ½` except the
  simple zero at `s = ½`**, and on the line `log|L*(½+it)| = ½ log|t| + O_q(1)`
  for `|t| ≥ 1` — it is *large*, not small.
* **(P)** Vertical polynomial bound: `|L*(σ+it)| ≤ C_q |t|^{1/2}` for
  `½ ≤ σ ≤ 3/2`, `|t| ≥ 1` (Hejhal Lemma 7.7 + Stirling). With (E) this gives
  `|L*(σ+it)| ≤ C_q' |t|^{1/2}` on the whole of `ℜ s ≥ ½`, `|t| ≥ 1`.
* **(Rl)** Reality: `L*(s̄) = conj(L*(s))`.

**Not available, and this matters (see `GAP-1`):** any upper bound for `|L*|` in
`ℜ s < ½`. By (F) such a bound is equivalent to a *lower* bound for `|L*|` in
`ℜ s > ½`, which fails at the zeros. This is precisely why the classical
Riemann–von-Mangoldt route to a local zero count is closed off here.

---

## 3. The re-derivation

### 3.1 Lemma A — Littlewood's lemma on a rectangle

> **Lemma A.** Let `f` be meromorphic on a neighbourhood of the closed rectangle
> `R = [a,b] × [−u,u]`, with no zeros and no poles on `∂R`. Let `arg f` be
> continued from the right edge. Then
> ```
>   Σ_{ρ∈R}(β−a) − Σ_{p∈R}(σ_p−a)
>     = (1/2π)[ ∫_{−u}^{u} log|f(a+it)|dt − ∫_{−u}^{u} log|f(b+it)|dt ]
>     + (1/2π)[ ∫_a^b arg f(σ+iu)dσ − ∫_a^b arg f(σ−iu)dσ ],
> ```
> zeros `ρ = β+iγ` and poles `p = σ_p+iτ` counted with multiplicity.

`PROVED-cited` (Littlewood; Titchmarsh, *Theory of the Riemann Zeta-Function*,
§9.9). It is the meromorphic form, obtained from the holomorphic one by
applying it to numerator and denominator of a local factorisation; poles enter
with the opposite sign, which is the **plus** sign in `(J)` once moved to the
other side (the sign the second audit refuted the alternative of, numerically).

**Sign calibration (done here, not cited).** Take `f(s) = s − β₀`, `a < β₀ < b`
real, `u → ∞`. LHS `= β₀ − a =: A`; put `B = b − β₀`.
`∫_{−u}^{u} log|it − A|dt = u log(u²+A²) − 2u + 2A arctan(u/A)`, so the first
bracket equals `u log((u²+A²)/(u²+B²)) + 2A arctan(u/A) − 2B arctan(u/B)
→ π(A−B)`. On the horizontals `arg f(σ±iu) → ±π/2`, so the second bracket
`→ π(b−a) = π(A+B)`. Total `= (1/2π)·π·2A = A`. ✔ The orientation above is the
one used below.

### 3.2 Lemma B — right edge to `+∞`

Send `b → ∞` in Lemma A with `f = L*`, `a = α ≥ ½`. By (E),
`|log|L*(b+it)|| ≤ 2A_q e^{−c_q b}`, so `∫_{−u}^{u}log|L*(b+it)|dt = O(u e^{−c_q b}) → 0`,
and `|arg L*(σ±iu)| ≤ 2A_q e^{−c_q σ}` makes the horizontal integrals converge.
By (E) there are no zeros or poles with `β ≥ σ₁`, so the zero/pole sums are
finite sums over the compact box `[α,σ₁]×[−u,u]`. Using (Rl) —
`arg L*(σ−iu) = −arg L*(σ+iu)` for the right-continued branch, by Schwarz
reflection — we get

> **(LW∞)** for every admissible height `u > 0`,
> ```
>   N(u) := Σ_{|γ|≤u, β>α} (β−α)
>         = Σ_{σ_j>α}(σ_j−α)
>           + (1/2π) ∫_{−u}^{u} log|L*(α+it)| dt
>           + (1/π)  ∫_α^{∞} arg L*(σ+iu) dσ .
> ```

**This is exactly the unweighted Littlewood formula Kelmer prints on p. 20 for
his (0.7)**, with the same `1/π`. That the two agree is an independent check of
the orientation fixed in §3.1.

*Admissibility.* `u` must avoid the (locally finite) set of ordinates of zeros
and poles; the left edge `ℜs = α = ½` is zero-free except at `s = ½` by (G), and
that single point is handled by the `α = ½+ε`, `ε ↓ 0` limiting device already
refereed in `LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_REFEREE.md` §5.2 (the
integrand there is `log|½+ε+it| → log|t|` in `L¹([−T,T])`, and the boundary zero
carries weight `β−α = 0`). Called **`R0`** below; refereed already, re-used, not
re-proved.

### 3.3 Integrate in `u`: the shape of `(J)`

`(T−|γ|)_+ = ∫_0^T 1_{|γ|≤u} du`, so `F_q(α,T) = ∫_0^T N(u)\,du`. Integrating
(LW∞):

* pole term → `T Σ_{σ_j>α}(σ_j−α)`;
* `∫_0^T ∫_{−u}^{u} g(t)\,dt\,du = ∫_{−T}^{T}(T−|t|)g(t)\,dt` (Fubini, `g` here
  is `log|L*(α+it)|`, integrable by (G): `= ½log|t| + O_q(1)`);
* argument term → `E(T) := (1/π)∫_0^T ∫_α^{∞} arg L*(σ+iu)\,dσ\,du`.

> **(J′)**  `F_q(α,T) = (1/2π)∫_{−T}^{T}(T−|t|)log|L*(α+it)|dt + T Σ_{σ_j>α}(σ_j−α) + E(T)`.

`(J)` is `(J′)` together with the claim `E(T) = O_q(log T)`. Note that the naive
route — `|∫_α^∞ arg L*(σ+iu)dσ| = O(log u)` (Kelmer Lemma 4.7) integrated in `u`
— gives only `E(T) = O(T log T)`, which is **useless**: it swamps the `C_qT`
term of `(I)` and would even swamp nothing worse than `O(T²)`, but it is a
factor `T/log T` off the printed remainder. So `(J)` genuinely requires
cancellation in `u`, and that cancellation is the content of `[Sel90, Lem 1,2]`.

*Fubini justification.* On `[α,σ₁]×[0,T]` the right-continued `arg L*` is
bounded (by `π(2N+1)` with `N` the finite number of divisor points in that box),
and on `[σ₁,∞)` it is `≤ 2A_q e^{−c_qσ}`. Measurable and absolutely integrable,
so the interchange in §3.4 is legitimate.

### 3.4 Lemma C — the closed form of the remainder (the new step)

> **Lemma C.** For every `T > 0` avoiding zero ordinates,
> ```
>   E(T) = (1/π) ∫_α^{∞} (x−α) [ log|L*(x+iT)| − log|L*(x)| ] dx .
> ```

**Proof.** Fix `σ ≥ α` such that no zero of `L*` has `β = σ` (all but countably
many `σ`). Define, using the right-continued branch at each height,
```
   P(s) := − ∫_{ℜs}^{∞} log L*(x + i·ℑs) dx      (absolutely convergent by (E)),
```
so that `P` is holomorphic off the horizontal cuts running left from each zero
and pole, `P′ = log L*`, and
```
   ℜ P(σ+iv) = − ∫_σ^{∞} log|L*(x+iv)| dx,   ℑ P(σ+iu) = − ∫_σ^{∞} arg L*(x+iu) dx .
```
1. `d/du · P(σ+iu) = i·log L*(σ+iu)`, hence
   `d/du · ℜP(σ+iu) = ℜ(i log L*) = − arg L*(σ+iu)`.
2. **The cut jumps are purely imaginary.** As `u` increases past the ordinate
   `γ` of a zero `ρ = β+iγ` with `β > σ`, the right-continued `log L*(x+iu)`
   jumps by `+2πi` for `x ∈ (σ,β)` and by `0` for `x > β`; hence `P(σ+iu)` jumps
   by `−2πi(β−σ)`. For a pole the jump is `+2πi(σ_p−σ)`. In every case the jump
   is purely imaginary, so **`ℜP(σ+i·)` is continuous on `[0,T]`** and piecewise
   `C¹` with derivative `−arg L*(σ+i·)`.
   (The poles of `L*` are real by (F); their cuts lie on `ℑ s = 0`, which the
   path meets only at the endpoint `u = 0`, so no crossing occurs for `u ∈ (0,T]`.)
3. Fundamental theorem of calculus on `[0,T]`:
   `∫_0^T arg L*(σ+iu)du = ℜP(σ) − ℜP(σ+iT)
      = ∫_σ^{∞} log|L*(x+iT)|dx − ∫_σ^{∞} log|L*(x)|dx.`
   (`ℜP(σ) := lim_{u↓0}`; the modulus makes it the ordinary real integral, with
   an integrable `+∞` at the real poles.)
4. Integrate over `σ ∈ [α,∞)` and swap (§3.3 Fubini):
   `∫_α^∞ ∫_σ^∞ h(x)dx dσ = ∫_α^∞ (x−α)h(x)dx`. Multiply by `1/π`. ∎

**Comment.** Step 2 is the whole trick: the entire zero/pole divisor drops out
of the *real part*, so no circularity. Lemma C is the exact analogue of
Littlewood's classical identity for `S₁(T) = ∫_0^T S(t)dt` for `ζ`. Its
numerical verification at `q = 3` to 14–16 digits (§4) is the strongest single
receipt in this note.

### 3.5 Upper bound: `E(T) ≤ O_q(log T)` — CLOSED

Write `E(T) = (1/π)[ I₁(T) − I₀ ]` with `I₁(T) = ∫_α^∞(x−α)log|L*(x+iT)|dx`,
`I₀ = ∫_α^∞(x−α)log|L*(x)|dx = O_q(1)` (a fixed finite number, the integrand
having only integrable logarithmic singularities at the real poles and at
`s = ½`, and decaying like `2A_q x e^{−c_q x}` at `+∞`).

* `α ≤ x ≤ σ₁`: by (P), `log|L*(x+iT)| ≤ ½ log T + log C_q'`. So this piece is
  `≤ ((σ₁−α)²/2)(½ log T + log C_q')`. **Upper bound rounded UP.**
* `x ≥ σ₁`: by (E), `|log|L*(x+iT)|| ≤ 2A_q e^{−c_q x}`, so this piece is
  `≤ 2A_q ∫_{σ₁}^{∞}(x−α)e^{−c_qx}dx = O_q(1)`.

Hence `E(T) ≤ (σ₁−½)²/(4π) · log T + O_q(1)`. ∎

### 3.6 Lower bound at a fixed height — the residual

`E(T) ≥ −O_q(log T)` is equivalent (given §3.5's second bullet and `I₀ = O_q(1)`) to

> **`GAP-1`.** For all `T ≥ T₀(q)`:
> `∫_{1/2}^{σ₁} (x − ½) · ( log|L*(x+iT)| )_− dx = O_q(log T)`,
> where `(·)_− = max(0, −·)`.

Two remarks fixing exactly what is missing.

1. **A local zero count would close it.** If
   `N_q(T) := #{ρ : β > ½, |γ − T| ≤ 1}` (with multiplicity) satisfied
   `N_q(T) = O_q(log T)`, then `GAP-1` follows: factor
   `L*(s) = ∏_{k≤N}(s−ρ_k)·h(s)` on a disc `D` containing the segment, note
   `∫_{1/2}^{σ₁}(x−½)|log|x+iT−ρ_k||dx ≤ (σ₁−½)·∫_{1/2}^{σ₁}|log|x−β_k||dx = O(1)`
   per zero, and bound `log|h| ≥ −O_q(log T)` by Borel–Carathéodory against the
   `(P)` majorant and the `(E)` anchor `|h| ≥ ½·(2σ₁)^{−N}`.
2. **Why the classical route to `N_q(T) = O_q(log T)` is unavailable here.** For
   `ζ`, that bound comes from Jensen on a disc `D(2+iT, 3)` which reaches into
   `ℜ s < 0`, where a growth bound is supplied by the functional equation. Here
   the functional equation (F) converts an upper bound left of `ℜ s = ½` into a
   **lower** bound for `|L*|` right of it, which fails at zeros. And *no* disc
   contained in `{ℜ s ≥ ½}` and centred at height `T` contains a neighbourhood
   of `½+iT`: such a disc meets the line in the single point `½+iT`. So the
   instrument is structurally blocked, not merely unattempted.
   Note also that the exact boundary modulus (G) does **not** force a zero-free
   strip: the half-plane Green's function vanishes on the boundary, so zeros may
   approach `ℜ s = ½` without contradicting `|L*(½+it)| ≍ |t|^{1/2}`.

`GAP-1` is therefore the precise residue of `[Sel90, Lemmas 1,2]` that this note
does not recover. **It is not needed for the LAW** (see §3.7–3.8).

### 3.7 What *does* close: the averaged remainder — CLOSED

> **Lemma D (local negative-part bound).** Fix `R ≥ 2σ₁ + 4`. Let
> `c = ½ + iT`, `T ≥ T₀(q)`, and `H = {|s−c| < R, ℜ s > ½}`. Then
> ```
>   ∫∫_{H ∩ {|s−c| < R/2}} ( log|L*| )_− dA  ≤  C_q(R) · log T .
> ```

**Proof.** `T₀(q)` is chosen so that `T − R > 1` and `T − R` exceeds the
ordinate of every (real) pole, so `L*` is holomorphic on `H̄` and `log|L*|` is
subharmonic there. Let `ψ : H → D` be a conformal bijection of the half-disc
onto the unit disc with `ψ(s₀) = 0`, `s₀ := ½ + R/2 + iT`; since `R/2 ≥ σ₁`,
(E) gives `|L*(s₀)| ≥ ½`. Put `v := log|L*∘ψ^{−1}|`, subharmonic on `D`.

*Upper bound on `∂D`.* `∂H` consists of the diameter — where by (G)
`log|L*| = ½log|t| + O_q(1) ≤ ½log(T+R) + O_q(1)` — and the arc, where (P)+(E)
give `log|L*| ≤ ½ log(T+R) + log C_q'`. So `v ≤ M := ½log(2T) + C_q''` on `∂D`,
hence on `D`. **UP.**

*Lower bound at the centre.* `v(0) = log|L*(s₀)| ≥ −log 2`. **DOWN.**

*Sub-mean-value.* `∫∫_D v\,dA ≥ π v(0) ≥ −π log 2`. With `v ≤ M`:
`∫∫_D v_+ ≤ πM`, hence `∫∫_D v_- = ∫∫_D v_+ − ∫∫_D v ≤ π(M + log 2)`.

*Pull back.* `∫∫_D v_- dA(z) = ∫∫_H (log|L*|)_-(s)·|(ψ^{-1})'|^{-2}… ` — concretely,
with `w = ψ(s)`, `dA(w) = |ψ'(s)|²dA(s)`, so
`∫∫_H (log|L*|)_- |ψ'|² dA = ∫∫_D v_- dA ≤ π(M+log 2)`.
`ψ` extends analytically across the open diameter and the open arc (Schwarz
reflection; both are analytic boundary arcs), and `ψ' ≠ 0` there; the only
degeneracies are the two corners `c ± iR`. The set `K := H̄ ∩ {|s−c| ≤ R/2}`
avoids both corners and the arc, so `|ψ'| ≥ κ(R) > 0` on `K`. Therefore
`∫∫_K (log|L*|)_- dA ≤ κ(R)^{-2} π (M + log 2) = C_q(R) log T`. ∎

**Consequence.** Choose `R = 2σ₁ + 4`, so that `K ⊇ [½,σ₁]×[T−1,T+1]`. Then
```
   ∫_{T−1}^{T+1} [ ∫_{1/2}^{σ₁} (x−½)( log|L*(x+iu)| )_- dx ] du
       ≤ (σ₁−½) · C_q(R) log T .
```
So **in every unit height interval there is an admissible `T* ∈ [T−1,T]` with**
```
   ∫_{1/2}^{σ₁}(x−½)( log|L*(x+iT*)| )_- dx ≤ (σ₁−½)C_q(R) log T ,
```
and hence, with §3.5,

> **`(J)-avg` [CLOSED].** For every `T ≥ T₀(q)` there is `T* ∈ [T−1,T]` with
> `|E(T*)| ≤ C_q log T`, i.e. `(J)` holds at `T*` with the printed `O_q(log T)`
> remainder.

### 3.8 From `(J)-avg` to `H3` — CLOSED

`F_q(½,·)` is non-decreasing and continuous: `F_q(½,T) = ∫_0^T N(u)du` with
`N ≥ 0`. Let `T ≥ T₀(q)` and pick `T* ∈ [T−1,T]` as in `(J)-avg`. Then, using
`(I)` (§4.2 of the SOL note, an elementary Stirling/`Γ`-quotient computation not
in dispute — its leading term is `2∫_0^T(T−t)\log t\,dt = T²\log T − (3/2)T²`
times the `½` from (G) and the `1/(2π)` outside, giving `(1/4π)T²\log T`), and
`Σ_{σ_j>½}(σ_j−½) ≥ 0`:

```
  F_q(½,T) ≥ F_q(½,T*)
           = (1/4π)T*² log T* + B_q T*² + C_q T* + T*Σ(σ_j−½) + O_q(log T)
           ≥ (1/4π)T² log T − [ (1/4π)(T² log T − T*² log T*) ] − |B_q|T² − |C_q|T − O_q(log T)
           ≥ (1/4π)T² log T − C_q' T² ,
```
because `0 ≤ T²logT − T*²logT* ≤ (T−T*)·(2T log T + T) ≤ 2T log T + T = O(T²)`.

> **`H3` [REDERIVED, lower half]:** `F_q(½,T) ≥ (1/4π)T² log T − C_q T²`.

The matching upper half follows the same way from §3.5's upper bound on `E`
(now valid at *every* `T`) plus `Σ(σ_j−½) ≤ (½)·#poles = O_q(1)`, giving
`F_q(½,T) ≤ (1/4π)T²logT + C_q T²`. The chain imports only the lower half.

### 3.9 What is *not* recovered

`(C)` — `N_q(T) = (1/2π)T log T + A_qT + O_q(log T)` — is obtained in the SOL
note from `(J)-sharp` through the finite-difference sandwich `(DIF)`. `(DIF)`
needs `(J)` at the three heights `T−1, T, T+1` **simultaneously**, with the
remainder `o(T)` at each. `(J)-avg` supplies only one good height per unit
interval, so `(C)` still rests on `[Sel90]`. Recorded as `GAP-2`.

---

## 4. Numerical verification at `q = 3` (independent receipt)

`q = 3` is `PSL(2,ℤ)`; `(NF)` has `g_{3,1} = d_3(1) = 1` and
`L*_3(s) = ζ(2s−1)/ζ(2s)`. Checked here, not assumed:
`|ζ(2it)/ζ(1+2it)| = |χ(2it)| = (1/√π)(|t| tanh(π|t|))^{1/2}`, which is exactly
(G) with `κ_3 = 1/√π`. In `ℜ s > ½` the divisor is: zeros `s = (1+ρ)/2` for each
nontrivial `ζ`-zero `ρ` (so `β = ¾`, `γ = γ_ζ/2` under RH, verified far beyond
the heights used), and a single pole `σ₁ = 1`.

Script `sel90_check.py` (scratchpad; interpreter `/Users/za/.venvs/farey-rh/bin/python`,
mpmath 1.4.1, `mp.dps = 25`). It computes independently
`E_num(T) = F_q(½,T) − (1/2π)∫_{−T}^{T}(T−|t|)log|L*(½+it)|dt − T·(σ₁−½)`
and `E_pred(T)` from **Lemma C**.

Verbatim output:

~~~
{"T": 25.0,  "F_lhs": 39.21537152875543,   "integral": 27.001656867719394,
 "poleterm": 12.5, "E_num": -0.2862853389639599,  "E_pred": -0.28628533896394964,
 "diff": -1.0261490770177418e-14, "logT": 3.2188758248682006}
{"T": 50.0,  "F_lhs": 273.88698581217795,  "integral": 249.0034359484204,
 "poleterm": 25.0, "E_num": -0.11645013624245523, "E_pred": -0.11645013624245514,
 "diff": -1.0220154639883466e-16, "logT": 3.912023005428146}
{"T": 100.0, "F_lhs": 1603.7807800292596,  "integral": 1553.8273025574463,
 "poleterm": 50.0, "E_num": -0.04652252818658234, "E_pred": -0.04652252818658194,
 "diff": -4.047447155406966e-16, "logT": 4.605170185988092}
~~~

Readings:

1. **Lemma C is confirmed to 14–16 significant digits** at three heights. This
   validates the orientation of Lemma A, the reality reduction, the `u`-integration,
   the purely-imaginary-jump step, and the Fubini swap — i.e. the whole chain
   §3.1–§3.4 — end to end, not just the final printed statement.
2. `F_lhs` at `T = 50` is `273.8870`, reproducing `LAW_SECOND_AUDIT_REFEREE.md`
   line 2b (`T=50: F=273.8870`) exactly. Independent lineage, same number.
3. `E_num` is `−0.286, −0.116, −0.047` — decreasing in magnitude, consistent
   with (and much smaller than) the `O(log T)` claim; the *plus* pole sign is
   again confirmed (the minus convention would leave residues `+T`).

`NON-RIGOROUS PROBE` for the `q = 3` instantiation (float readout of mpmath
quadrature, RH assumed for `β = ¾`); it corroborates the derivation, it does not
prove it.

---

## 5. GAP list

| # | Statement of what is missing | Blocks |
|---|---|---|
| **GAP-1** | `∫_{1/2}^{σ₁}(x−½)(log|L*(x+iT)|)_− dx = O_q(log T)` at **every** large `T` (equivalently: a local zero count `N_q(T) = #{ρ: β>½, |γ−T|≤1} = O_q(log T)`). Blocked because (i) no upper bound for `|L*|` in `ℜ s < ½` follows from (F)+(P) — it would be a lower bound for `|L*|` right of the line, false at zeros; (ii) no disc inside `{ℜ s ≥ ½}` centred at height `T` covers a neighbourhood of `½+iT`. | `(J)-sharp` at every height |
| **GAP-2** | `(DIF)`/`(C)`: the finite-difference sandwich needs `(J)-sharp` at `T−1, T, T+1` simultaneously; `(J)-avg` gives one good height per unit interval. | the sharp asymptotic `(C)` only |
| **R0** *(not new)* | The `α = ½+ε`, `ε↓0` indentation at the boundary zero `s = ½`. Already refereed in `LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_REFEREE.md` §5.2; re-used, not re-proved here. | nothing new |

Neither `GAP-1` nor `GAP-2` touches `H3`, which §3.8 derives outright.

---

## 6. Verdict line

> **(J) REDERIVED in the form the chain consumes — `H3` (`F_q(½,T) = (1/4π)T²logT + O_q(T²)`, both halves) is now proved here from the banked inputs (D),(E),(F),(U),(G),(P),(Rl) with no appeal to Selberg 1990 or to Kelmer (4.20). The `[Sel90, Lemmas 1,2]` citation is therefore REPLACEABLE for the banked LAW. PARTIALLY for the printed sharp form: `(J)` with remainder `O_q(log T)` at every height is derived down to the single residual `GAP-1` (pointwise negative-part bound / local zero density near the critical line at height `T`), and `(C)` additionally needs `GAP-2`. Selberg's text is still required for `(J)-sharp` and `(C)`, and for nothing else in the chain.**

---

## 7. Receipts

```
$ cd <scratchpad> && curl -sL -o kelmer.pdf https://arxiv.org/pdf/1402.4780
$ file kelmer.pdf
kelmer.pdf: PDF document, version 1.4, 26 pages
$ shasum -a 256 kelmer.pdf
c15fb0c4d1d72cc1e09ee6c70532e27d835afd8a8e01a23668cdb6049f8d5030  kelmer.pdf
```

The hash equals the one banked in `LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_SOL.md`
§7 for `/tmp/kelmer_1402.4780.pdf` — same object, fetched independently today.

```
$ pdftotext -layout kelmer.pdf kelmer.txt && grep -n "Sel90" kelmer.txt
128:  vious results of Selberg [Sel90] for hyperbolic surfaces...
217:  Remark 0.2. For hyperbolic surfaces this result is due to Selberg [Sel90]
597:  of [Sel90] on the distribution of poles of Eisenstein series to hyperbolic
617:  of Selberg's [Sel90, Lemma 3]
1149: Selberg's [Sel90] and we include it for the sake of completeness.
1157: 4.4, L* (s) satisfies all the assumptions needed for [Sel90, Lemma 1,2],
1517: [Sel90]  Atle Selberg. Remarks on the distribution of poles of Eisenstein series.
```

Numeric probe: `sel90_check.py` / `sel90_check.json`, kept in the session
scratchpad only; no PDF, script or JSON is a repository artifact. Interpreter
`/Users/za/.venvs/farey-rh/bin/python` (mpmath 1.4.1). Runtime 21 s.

**LEDGER RULE.**
* Selberg 1990 remains **UNREAD** by this author. Nothing above quotes,
  paraphrases or reconstructs its text; `[Sel90, Lemmas 1,2]` is quoted only as
  it appears inside Kelmer.
* This note claims **no** `q`-uniform constant, **no** effective first height,
  **no** machine formalization, and **no** value for `A_q`, `B_q`, `C_q`.
  Kelmer's printed `A_Γ`, `B_Γ` remain do-not-consume (second audit, finding C).
* The `q = 3` numerics are corroboration under RH, not proof, and carry no
  arithmeticity content (second audit, attack 5b).
* Everything here is **UNREFEREED**. `(J)-avg`, Lemma C, Lemma D and the `H3`
  derivation are `PROVED-here (UNREFEREED)`; they must not be promoted, cited as
  CONFIRMED, or used to relabel `S5` in `DISPATCH.md`, before a cold referee
  pass. Suggested referee attack order: (i) Lemma A orientation and the
  meromorphic sign; (ii) Lemma C step 2 (are all cut jumps purely imaginary,
  including at a pole met at the endpoint `u = 0`?); (iii) Lemma D's conformal
  pull-back constant `κ(R)` and the corner exclusion; (iv) the monotonicity
  upgrade in §3.8 and its `O(T²)` slack; (v) whether `GAP-1` is really needed,
  i.e. whether a half-plane Carleman argument bounds `Σ_{ρ∈H}(β−½)` sharply
  enough to give a pointwise bound.
* Append-only. No other file was read-modified; no `git` command was run.

---

## 8. Correction block (2026-08-23, from `SEL90_BYPASS_JENSEN_REDERIVATION_REFEREE.md`)

**APPEND-ONLY.** Nothing above is altered or deleted. This block records the
corrections required by the cold referee report
`research_notes/rh_goals_2026-08-14/lane_g/SEL90_BYPASS_JENSEN_REDERIVATION_REFEREE.md`
(gate: **PROMOTABLE-with-corrections**; blocking items D-1, D-2, D-3). Where a
correction contradicts text above, **this block governs**.

### D-1 — §3.3 Fubini justification gave a *wrong reason* (blocking; corrected)

§3.3 writes: "the right-continued `arg L*` is bounded (by `π(2N+1)` with `N` the
finite number of divisor points in that box)".

**Replace that parenthetical with:** "bounded on the compact box for each fixed
`T` (no uniformity in `T` claimed or needed)".

*Why the original reason is false as a general principle.* The winding
accumulated by continuing `arg` leftward along a horizontal segment is
controlled by the number of **sign changes of `ℜ L*`** on that segment
(Backlund / Titchmarsh, *Theory of the Riemann Zeta-Function*, Lemma 9.2 — the
same machinery Kelmer cites for his Lemma 4.7), **not** by the count of divisor
points in the box. So `π(2N+1)` with `N` = divisor count is not a valid bound in
general.

*The conclusion stands.* `arg L* − Σ_k arg(s−ρ_k)` is continuous on the compact
box `[α,σ₁]×[0,T]`, hence bounded there for each fixed `q, T`; and only
finiteness — not a uniform-in-`T` constant — is needed for the Fubini
interchange of §3.3 and for the absolute continuity used in Lemma C step 3.
Lemma C, `(J)-avg`, Lemma D and `H3` are unaffected.

### D-2 — §3.7 quantifier arithmetic understated (blocking; corrected)

Two facts are load-bearing in §3.7 and were left unstated. Both now recorded.

**(a) `[T−1,T+1] → [T−1,T]` restriction is valid.** The consequence display
integrates over `[T−1,T+1]` (length 2) while the conclusion asserts
`T* ∈ [T−1,T]`. This is legitimate **because the integrand is `≥ 0`**
(`(log|L*|)_−` and the weight `(x−½)` are both non-negative), so restricting to
the length-1 subinterval preserves both the bound and the averaging argument.

**(b) `κ(R)` is independent of `T`.** The half-disc `H` is a **pure translate**
of a fixed half-disc: `H = H₀ + iT` with `H₀ = {|s−½| < R, ℜ s > ½}`. Hence the
conformal map may be taken as `ψ = ψ₀(· − iT)`, so `|ψ′|` on `K = K₀ + iT`
equals `|ψ₀′|` on `K₀`, and `κ(R) = inf_{K₀}|ψ₀′| > 0` depends on `R` only.
Consequently `C_q(R) = κ(R)^{−2}·(…)` is **not secretly `C_q(R,T)`**; without
this remark the reader cannot see that Lemma D's constant is `T`-free, which is
what makes `(J)-avg` and §3.8 legitimate.

### D-3 — §2 `(P)` extension: strip `3/2 < σ < σ₁` (blocking; corrected)

§2 `(P)` reads: "for `½ ≤ σ ≤ 3/2` … With (E) this gives `≤ C_q′|t|^{1/2}` on
the whole of `ℜ s ≥ ½`". But `(E)` starts only at `σ₁ ≥ 3/2`, so when
`σ₁ > 3/2` the strip `3/2 < σ < σ₁` is covered by neither cited clause.

**Correction — add the missing citation.** The strip is covered by the banked
`LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_SOL.md:172`:

> "For `σ ≥ 3/2`, the absolutely convergent series supplies a bounded right
> half-plane."

With that clause the claimed bound holds on all of `ℜ s ≥ ½`, `|t| ≥ 1`. This is
load-bearing for the **arc** bound in Lemma D (§3.7), where `ℜ s` runs up to
`R = 2σ₁ + 4`.

### D-4 — `σ₁` notation collision (cosmetic; renamed)

`σ₁` denotes the right-edge normalisation constant (`σ₁ = σ₁(q) ≥ 3/2`) in §2
and §3, and separately the **pole location** (`σ₁ = 1`) in §4 (line 415).

**Rename:** the §4 occurrence is renamed **`σ_pole`** (`σ_pole = 1`, the single
pole of `L*_3` in `ℜ s > ½`). Read §4 line 415 as "a single pole `σ_pole = 1`",
and the pole term of §4's `E_num` definition as `T·(σ_pole − ½)`. Elsewhere in
the note `σ₁` keeps its §2 `(E)` meaning.

### D-5 — DISPATCH line citation off by one (cosmetic; corrected)

§1.1 cites "line 86" for the sentence "The LAW's analytic weight lives entirely
in H3." The sentence spans **`projects/aristotle_dispatch_v33/DISPATCH.md`
lines 85–86**. Read the §1.1 bullet as `lines 85–86`.

### D-6 — the numeric claim was *under*-stated (recorded, not weakened)

§0 and §4 claim "14–16 significant digits". The referee re-ran the check
independently at `mp.dps = 30` with `(G)` in closed form and obtained agreement
of **`1e−26 … 1e−32`, i.e. ≈ 26–31 digits**, at seven heights (including
`T = 3.9` and `T = 7.0`, where the divisor is empty, and `T = γ ± 10⁻⁶`
straddling the first zero ordinate `γ = 7.06736257086735`). The note's weaker
figure is an artefact of `dps = 25` plus float readout. **Recorded so that the
stronger number is not later "corrected" downward.**

### Post-correction status

> Post-correction status: PROMOTED per referee gate — (J)-avg, Lemma C, Lemma D,
> H3 CONFIRMED and independently reproduced; the [Sel90, Lemmas 1,2] citation is
> REPLACEABLE for the banked LAW (H3 consumed form). GAP-1/GAP-2 remain:
> (J)-sharp and (C) still rest on Selberg 1990; nothing in the LAW conclusion
> chain touches them.

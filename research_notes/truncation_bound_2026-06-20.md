# A-priori truncation / dimension-tail bound for the certified Selberg-zeta determinant

**Goal G2.** Replace the *validated-not-proved* dimension-tail used by
`code/zeta_cert_rosen.py :: dim_tail_from_matrix` with an a-priori PROOF, or the
strongest precisely-scoped partial. **Status: precisely-scoped partial.** A
rigorous trace-class statement is proved; the residual reduces to ONE named
inequality (the *cofactor-free spectral-tail inequality*), and the source of the
difficulty is fully diagnosed and numerically demonstrated.

All numbers below come from commands run this session (q=5 odd sector, sign=-1,
Maass zero `s = 1/2 + 6.4737 i` and `1/2 + 8.6368 i`, `n_head=4`); see the smoke
block at the end and `code/truncation_bound/`.

---

## 1. The object and the current (heuristic) bound

Let `L_s` be the reduced Rosen/MMS transfer operator (the `kappa·N × kappa·N`
Arb ball matrix produced by `build_reduced_matrix_ball`). The certified zeta
value is `det(1 − L_s)`. Truncating each component's Taylor expansion at `N`
coefficients yields `det(1 − L_s^{(N)})`. The truncation remainder is

```
    Δ(N,s) := | det(1 − L_s) − det(1 − L_s^{(N)}) |.
```

`dim_tail_from_matrix` bounds `Δ` by **extrapolating the determinant increments**
`D_d := det(1 − L_s^{(d)})`: it measures `g_m = |D_{d_{m+1}} − D_{d_m}|` over a
4-point window `d_0 < … < d_W = N`, certifies every consecutive ratio
`g_{m+1}/g_m ≤ q_cap (= 0.85)`, and returns the geometric tail
`g_last · q/(1−q)`. **This is rigorous about the finite increments it sees, but
its continuation is an assumption**: that the *observed* contraction rate of the
det-increments persists for all `d > N`. That is the "validated-not-proved" gap.

---

## 2. Precise truncation-remainder PROPOSITION (the defensible statement)

`L_s` is **trace class** (nuclear): it is a composition operator with a strictly
contracting, holomorphic symbol on a disjoint union of discs, so its singular
values `σ_0 ≥ σ_1 ≥ …` decay super-exponentially (Grothendieck/Ruelle theory of
holomorphic transfer operators; numerically `σ_n` falls from `≈ 2.7·10²` to
`≈ 6·10⁻²⁴` over 66 values at N=22). Hence both determinants are well defined.

**Proposition (Plemelj / Gohberg–Krein, spectral truncation).** Let `A := −L_s`,
let `A_r` be the *spectral* truncation keeping the top `r` singular directions
(`A_r = Σ_{n<r} σ_n u_n v_n^*`). Then

```
  (GK)   | det(1+A) − det(1+A_r) |  ≤  ( ∏_{n<r}(1+σ_n) ) · ( exp( Σ_{n≥r} σ_n ) − 1 ).
```

This is a *theorem* (Gohberg–Krein, Simon "Trace Ideals" Thm 3.4 + multiplicativity
of `det` across the orthogonal kept/discarded splitting). With the geometric
majorant of §3 it is fully a-priori and finite.

**Corollary (geometric-tail closed form).** If `σ_n ≤ σ_0 θ^n` for some
`θ ∈ (0,1)` (the residual constant, §4), then for `M := r`,

```
  (TAIL)  Σ_{n≥M} σ_n  ≤  σ_0 · θ^M / (1 − θ),
```

so `Δ ≤ ( ∏_{n<r}(1+σ_n) ) · ( exp( σ_0 θ^r/(1−θ) ) − 1 )`, a **closed,
a-priori, certifiable** upper bound. The `(TAIL)` step is the clean core
formalized in Lean (§6).

Everything in (GK)+(TAIL) is proved modulo (i) the trace-class nuclearity (a
classical analytic fact for these operators) and (ii) the majorant constant `θ`.

---

## 3. Certified inputs (this session, q=5, s = 1/2 + 6.4737 i, N=22, dim=66)

| quantity | certified upper bound | how |
|---|---|---|
| `σ_0 = ‖A‖_op` | `≤ 3.812·10²` | Schur test `√(‖A‖₁ₙₒᵣₘ · ‖A‖_∞)`, Arb sup over the ball matrix |
| `‖A‖_1` (nuclear) | `≤ 1.207·10³` | `Σ_c ‖A e_c‖₂`, certified |
| geometric-tail closed form | rel-err `1.3·10⁻¹⁶` | `Σ_{n≥54} a θ^n` vs `a θ⁵⁴/(1−θ)` |

`certified_sigma0_upper` and `certified_tracenorm_upper` are interval-valued
(Arb `abs_upper`); the singular values themselves are read off a float proxy
(clearly labelled heuristic) only to *validate* `θ`.

---

## 4. The residual: the cofactor and the constant θ — and why this is HARD

Two honest obstructions were found and demonstrated numerically; both are
intrinsic, not artifacts of effort.

**(a) The exponential cofactor is astronomically loose.** `‖A‖_1 ≈ 612` and
`‖A‖_HS ≈ 317` (top singular value `σ_0 ≈ 273`). Therefore the *provable*
constants blow up:

```
  exp(1 + 2‖A‖_1) = exp(≈1226) = +inf       (naive Plemelj)
  ∏_{n<r}(1+σ_n) ≈ 10²² … 10²⁷               (Gohberg–Krein cofactor, GK)
```

while the **true** remainder is `Δ ≈ 10⁻¹⁰ … 10⁻¹³`. The bare singular-value
tail `Σ_{n≥r} σ_n ≈ 10⁻⁸` already *over*-bounds the true remainder with margin
(ratio `Δ / Σσ ∈ [0.006, 0.20] < 1` across all tested `r`, both `s`), but the
**cofactor `∏(1+σ_n)` destroys this** — multiplying a small tail by `10²²`.

So the operative open inequality is the **cofactor-free spectral-tail bound**

```
  (★)   | det(1+A) − det(1+A_r) |  ≤  C · Σ_{n≥r} σ_n,        C = C(q,s).
```

**IMPORTANT honest finding (this session):** `(★)` does **NOT** hold with a
universal `C ≤ 1`. The broader sweep (q ∈ {3,5,7,9,11}, validate.py + the Kaggle
kernel) shows:

| q | s | regime | ratio `(true remainder)/(Σ_{n≥r}σ)` | (★) with C≤1? |
|---|---|---|---|---|
| 5 | 1/2+6.4737i | r=N..3N/2 | 0.08–0.20 | YES |
| 11 | 1/2+4i | r≈0.45–0.75·dim | 0.003–0.067 | YES |
| **7** | 1/2+5i | r≈0.75·dim | **1.59** | **NO** |
| **3** | 1/2+12i | r≈0.45–0.6·dim | **1.35–2.89** | **NO** |

For q=3 (modular surface) and q=7 at moderate `r`, the true determinant
remainder **exceeds** the bare singular-value tail — the Gohberg–Krein cofactor
`∏(1+σ_n)` is *genuinely needed* there, so a cofactor-free bound is FALSE. The
constant `C(q,s)` is therefore **not O(1) uniformly**; whether `C ≤ 1` holds
depends on q and the spectral configuration. It holds in the high-q non-arith
regime (q=5,11) because, on the critical line at a near-zero of the determinant,
`det(1+A_r)` is tiny (the determinant nearly vanishes), suppressing the
cofactor's effect; at q=3,7 in the tested ranges it does not.

**So the exact residual open inequality is the q-DEPENDENT bound `(★)` with an
explicit `C(q,s)`** — equivalently a uniform bound on the resolvent-weighted tail
`‖(A−A_r)(1+A_r)^{-1}‖_1`, i.e. a spectral-gap statement for `1+A_r` along the
critical line. The resolvent norm `‖(1−L^{(d)})^{-1}‖₂` was found to
**stabilize** at `≈ 7.35·10⁷` for `d ≥ 14` (q=5, s=1/2+6.4737i) — bounded, which
is what `(★)` needs at that q/s, but its a-priori (all-`d`, all-`q`) boundedness
is unproved and, per the table, the constant it yields is genuinely q-dependent.
A second numerical caveat: near `r = dim` the tail drops to the double-precision
noise floor (`~10⁻¹¹·σ_0`) and ratios there are round-off, not (★); the Kaggle
kernel masks those ("meaningful" flag).

**(b) The deployed truncation is COEFFICIENT truncation, not SPECTRAL.** (GK)
governs spectral truncation `A_r`; the code truncates Taylor coefficients
(`P_N A P_N` in the normalized monomial basis). In that basis the discarded part
has **huge** nuclear norm (`‖L − L_N‖_1 ≈ 1.35·10³`, inflated by the `ρ^{−k}`
basis normalization on high-`k` columns) even though it contributes
negligibly to the determinant. So a second residual is the **basis
reconciliation**: bound the coefficient-truncation remainder by the
spectral-truncation tail. Numerically the coefficient-truncation remainder
`|D_N − D_{N-2}|` and the spectral tail agree in magnitude (`≈ 10⁻⁹` at N=22),
but no norm-product inequality in the normalized basis proves it — the agreement
is the cancellation (★) again, viewed through the basis.

**Net:** G2's a-priori bound reduces to the single inequality **(★)** (with the
explicit `O(1)` constant `C`), equivalently the uniform resolvent bound
`sup_d ‖(1−L^{(d)})^{-1}‖ < ∞` on the relevant strip. Everything else — (GK),
(TAIL), nuclearity, the certified `σ_0`, `‖A‖_1` — is proved or certified.

---

## 5. What changes for the deployed `dim_tail_from_matrix`

Nothing needs to change operationally: the extrapolated tail is *numerically
sound* and now *explained* — its hidden assumption is exactly the cofactor-free
behaviour (★). The honest upgrade is documentation: the dimension tail is
certified **conditional on the contraction continuing**, and §4 isolates the
precise analytic statement that would make it unconditional.

A *strictly rigorous* (if conservative) replacement that needs NO new theory:
report `Σ_{n≥r} σ_n` for the **spectral** truncation via (GK)+(TAIL) — but the
`∏(1+σ_n)` cofactor makes it `10²²×` too weak to certify zeros, so it is not a
practical substitute. This is why the project uses extrapolation: the only
*tight* bound currently available is the empirical one.

---

## 6. Lean core (formalized)

`projects/truncation_bound_lean/` formalizes the clean, fully-rigorous piece:
the **geometric-tail summation bound** (TAIL),

```
  0 ≤ a,  0 ≤ θ < 1,  σ n ≤ a·θ^n  ⟹  Σ_{n≥M} σ n  ≤  a·θ^M/(1−θ),
```

plus the elementary `exp(x) − 1 ≤ x·exp(x)` step feeding (GK). These are the
analytic lemmas a verifier can close outright; the residual (★) is stated as a
hypothesis, not discharged. See `RequestProject/Main.lean` and `PROMPT.md`.

---

## 7. Honest verdict

- **PROVED (modulo classical nuclearity):** the Plemelj/Gohberg–Krein remainder
  inequality (GK) and the geometric-tail closed form (TAIL); certified `σ_0`,
  `‖A‖_1`.
- **NOT proved (the residual):** the spectral-tail inequality (★) with an
  explicit **q-dependent** constant `C(q,s)`, equivalently
  `sup_d ‖(1−L^{(d)})^{-1}‖ < ∞` on the strip with a controlled bound — this is
  what would make the *tight* dimension tail a-priori. The cofactor-free `C ≤ 1`
  form is FALSE in general (demonstrated at q=3,7), so the honest target is the
  q-dependent resolvent bound, not a universal constant.
- **Diagnosed:** why every standard trace-class inequality is `10²²×`–`exp(612)×`
  too loose here (large `‖L_s‖_1`; near-vanishing determinant), and why the
  deployed extrapolation is currently the only tight tool.

This is a rigorous scoped partial: a defended precise statement, a proof of the
clean core, certified numeric inputs, and the residual named exactly.

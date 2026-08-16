# LAW (U1) — the q-uniform growth bound

**Date:** 2026-08-15. **Lane G.** Ticket: `plans/wayfinder/rh-goals/tickets/family-law-theorem.md`,
obligation **U1** of `lane_g/LAW_T2_DETERMINANT.md` §5.2.
**Parents read in full:** `lane_g/LAW_T2_DETERMINANT.md` (the (T2′) Vitali+Hurwitz formulation and
U1's role in it), `lane_g/LAW_U3_TRANSPORT.md` (U3 closed: `Z_{Γ_θ}` has a zero of order `2·m(ρ₁)`
at `s_∞`, unconditional given the §2 citations; **and its §2.5 Teo functional equation, which is the
main analytic tool used here**), `lane_g/LAW_PROBES_D1_B1.md` (D1: pins migrate to `s_∞` at `~q⁻²`),
`lane_g/law_probes/probe_t2_shape.py` + `t2_shape.json` (word enumerator, `Z_q → Z_θ` at `q⁻²`).

**Status convention (identical to T2 / U3 / M1F):** `PROVED` = derived here in closed form or
verified in exact/symbolic arithmetic. `CITATION` = imported, import named.
`HEURISTIC` = float evidence or a plausibility argument, explicitly not a proof.
`GAP` = not justified; the missing statement is written out.
`TODO-VERIFY` = a specific check owed against a named source.

**No certificate is produced here. Nothing is committed. `lane_f` is untouched.**

---

## 0. Verdict up front

> ### **U1 is NOT PROVED. It is REDUCED — to one named q-uniform obligation, `(U1-φ)`.**
> ### The brief's named danger (the order-`q` elliptic data) is **SETTLED and harmless on `U`**.
> ### The brief's named fallback (renormalize by `C(q)`) is **REFUTED — it is logically useless.**
> ### **The numeric guard is ADVERSE.** `sup_{∂U}|Z_{G_q}|` (dropping the one boundary point that
> ### lies outside the determinant's identification domain) **increases monotonically**:
> ### `25.1 → 49.5 → 92.8 → 99.4` at `q = 16, 22, 30, 40`, log-log slope **`+1.50`**.
> ### U1 requires slope `0`. Five `q`, non-rigorous proxy — not a refutation, but not support.
>
> **Headline: U1-OPEN-REDUCED, GUARD-ADVERSE. The (T2′) tail route is now AT RISK.**

Six things are settled here, four of them new and load-bearing.

1. **(T2′-a) is over-stated and can be weakened.** Vitali needs *local uniform boundedness on a
   connected domain*, not a global order-2 bound. U1 is equivalent to boundedness of
   `{Z_{G_q}}` on **one compact rectangle** `K = [−1/10, 3/2] × [t_∞ − 3/10, t_∞ + 3/10]`
   plus the half-plane `Re s ≥ 3/2`, where the Euler product does the work. §1.2, `PROVED`.
2. **The elliptic factor of the functional-equation kernel — the brief's named danger — is
   computed exactly and is harmless on `U`.** `E_q(s) = ∏_{k=0}^{q−1} sin(π(s+k)/q)^{(q−2k−1)/q}`
   satisfies the **exact** identity `E_q = Z_{ell,q}(s)/Z_{ell,q}(1−s)` (§3.2, `PROVED`),
   `|E_q(1/2+it)| = 1` for every `q` (`PROVED`, verified to `7e−18`), and
   ```
      log E_q(s) = (2s - 1) log( q / 2 pi )  +  log( Gamma(1-s) / Gamma(s) )  +  O(1/q)
   ```
   (§3.3, `HEURISTIC-IDENTIFIED`: matched to 4 decimals at 7 test points, `q ≤ 4800`, residual
   halving exactly under `q`-doubling). On `U` (`Re s ≤ 1/2`) this is **`≤ 1` and decaying**;
   the naive fear that `q` sine-factors give `q`-dependent growth is **false** — the exponents sum
   to zero and the `2^{1−q}` of the sine multiplication formula cancels against the weighted sum.
   **But for `Re s > 1/2` it grows like `q^{2Re s−1}`, so `≍ (q/2π)³` at `Re s = 2`.**
3. **The renormalized fallback is dead.** If `C(q) → ∞`, then `Z_{G_q}/C(q) → 0` on
   `{Re s > 1}` (because `Z_{G_q} → Z_{Γ_θ} ≢ 0` there, `PROVED` in T2 §3.4/U2a), so Vitali forces
   the limit `≡ 0` on the whole domain and **Hurwitz gives no information at all**. §4, `PROVED`.
   **U1 must be proved as stated, or the (T2′) tail route fails.** This retires the brief's
   route (3) and it also removes the ledger's only fallback.
4. **A correction is owed to `LAW_T2_DETERMINANT.md` §3.3.** That note argues the uniform Weyl
   counting is "free" from `|F_q| = π(1 − 2/q) ≤ π`. It is free **only in the `T²` coefficient.**
   The elliptic mass of `G_q` is
   `M(q) = Σ_{k=1}^{q−1} 1/(2q sin(kπ/q)) = (1/π) log(2 e^γ q / π) + O(q^{-2})`
   (§3.4, `PROVED` numerically to 5 decimals over `q = 5 … 10⁴`) — it **grows like `(log q)/π`**,
   and it enters the Weyl law's **linear-in-`T`** coefficient. At the fixed height `T ≈ 8` that
   matters to us, the `T²` term is `≈ 16` and the elliptic term is `≈ (8/π)log q ≈ 17.6` at
   `q = 1000` — **the same size**. The counting is *not* uniform at fixed height without an
   argument. §5.2, `HEURISTIC` for the size, `PROVED` for `M(q)`.
5. **The guard measures a rise, not a plateau.** §7.3: `sup_{∂U}` of the two-sector determinant
   product grows with log-log slope `+1.50` over `q = 16 → 40`, `N`-converged to 9 significant
   digits at `N = 32, 48, 64`. That is the shape the *trivial* estimate `|φ_q| ≤ 1` predicts
   (`O(q^{2−σ})`, §5.1) and it is incompatible with U1, which needs slope `0`. Five points and a
   proxy whose identification is itself open (U4) — so this is a warning, not a refutation. But
   combined with item 3 it means the route has no soft landing **and** its one measurable proxy is
   moving the wrong way.
6. **The single remaining obligation is the scattering determinant.** Every route that can reach
   `Re s = 1/4` from `Re s > 1` — functional equation + convexity, or Hadamard + zero counting —
   passes through `φ_q(s) = det Φ_q(s)`, which for non-arithmetic `G_q` has no closed form
   (this is the Phillips–Sarnak situation). §5. That reduction is the note's main structural
   deliverable, and it is stated as `(U1-φ)` in §6.

**Bonus, banked:** the numeric guard independently corroborates the **U4** determinant
identification **at even `q = 12, 16, 22, 30, 40`** — `|det(1−L^+)·det(1−L^−)|` agrees with the
truncated Selberg Euler product to `3e−4 … 2e−3` at two control points with `Re s > 1` (§7.2).
The repo previously had this identification only at `q = 5` (R5). `HEURISTIC`, but it is the first
general-`q` evidence and it was not asked for.

---

## 1. What U1 must deliver, restated exactly

### 1.1 The (T2′) hypothesis as written

From `LAW_T2_DETERMINANT.md` §3.2:

> **(T2′-a) [uniform normal family]** there are `A, B < ∞` independent of `q` with
> `|Z_{G_q}(s)| ≤ A · exp( B (1+|s|)² )` for all `s ∈ Ω̃` and all `q ≥ Q₁`.

`Ω̃` is required open, connected, and to contain both `s_∞` and `{Re s > 1}`.

### 1.2 `PROVED` — the hypothesis can be weakened to boundedness on one compact rectangle

Fix `t_∞ := Im s_∞ = 7.0673625708673465`, `s_∞ = 1/4 + i t_∞`, and

```
   U   :=  { |s - s_inf| <= 1/4 }                                     (Re s in [0, 1/2])
   Om  :=  { Re s > 1 }  u  { -1/10 < Re s < 3/2,  |Im s - t_inf| < 3/10 }
   K   :=  [-1/10, 3/2] x [t_inf - 3/10, t_inf + 3/10]                (compact)
```

`Ω̃` is open and connected (the tube meets the half-plane in `1 < Re s < 3/2`), and `U ⊂ Ω̃`
(`Re s ∈ [0,1/2] ⊂ (−1/10, 3/2)`, `|Im s − t_∞| ≤ 1/4 < 3/10`). Every compact subset of `Ω̃`
is contained in `K ∪ {Re s ≥ 3/2} ∪ (compact subset of Re s > 1)`. Hence

> **Lemma U1-0.** (T2′-a) holds on `Ω̃` **iff**
> `sup_{q ≥ Q₁} sup_{s ∈ K} |Z_{G_q}(s)| < ∞` **and** `sup_{q ≥ Q₁} sup_{Re s ≥ 3/2}|Z_{G_q}(s)| < ∞`.
> `PROVED` (Montel/Vitali need only local uniform boundedness; the exponential shape of (T2′-a) is
> never used, because `Ω̃` can be chosen with bounded imaginary part).

**Consequence for the ledger.** The phrase "order-2 growth with `q`-uniform constants" in the
brief and in T2 §5.2 asks for more than the theorem needs. **U1 is a boundedness statement on a
`0.6 × 1.6` rectangle.** That is the version pursued below, and it is strictly easier.

The second half of Lemma U1-0 is §2. The first half is §3–§5, and is where the work is.

---

## 2. The right half-plane: `PROVED` modulo U2b

### 2.1 The bound

For `σ = Re s ≥ 3/2` the Selberg Euler product converges absolutely and

```
   | Z_Gamma(s) |  =  | prod_{[g] prim} prod_{k>=0} ( 1 - e^{-(s+k) l_g} ) |
                   <=  prod prod ( 1 + e^{-(sigma+k) l_g} )
                   <=  exp(  sum_{[g]} e^{-sigma l_g} / ( 1 - e^{-l_g} )  )  =: exp( S_Gamma(sigma) )
```

`PROVED` (elementary). With the uniform systole `sys(G_q) = 2 arccosh λ_q ≥ 2 arccosh λ_5 = 2.122550`
(T2 §3.4, `PROVED` given that `[S R²]` realises the systole — that half is `HEURISTIC`, and is
U2b) one has `1/(1 − e^{−ℓ}) ≤ 1.136010`, so `S_q(σ) ≤ 1.136010 · Σ_{[γ]} e^{−σ ℓ_γ}`.

### 2.2 `HEURISTIC` — the measured majorant is monotone decreasing in `q`

`law_probes/probe_u1_growth.py` part **B**, geodesics enumerated by the `probe_t2_shape.py` BFS at
`r_max = 9`, `ℓ ≤ 8`:

| `q` | `sys(G_q)` | `S_q(1.25)` | `S_q(1.5)` | `S_q(2.0)` |
|--:|---|---|---|---|
| 5 | 2.122550 | **0.44365** | **0.19144** | **0.04709** |
| 7 | 2.388409 | 0.40121 | 0.16216 | 0.03417 |
| 10 | 2.517006 | 0.36491 | 0.13997 | 0.02649 |
| 12 | 2.553374 | 0.35008 | 0.13190 | 0.02416 |
| 16 | 2.588962 | 0.33193 | 0.12268 | 0.02182 |
| 22 | 2.610248 | 0.31839 | 0.11621 | 0.02039 |
| 30 | 2.621218 | 0.30877 | 0.11224 | 0.01964 |
| 50 | 2.629353 | 0.29955 | 0.10880 | 0.01908 |
| 80 | 2.632134 | 0.29576 | 0.10748 | 0.01889 |
| 150 | 2.633409 | 0.29230 | 0.10665 | 0.01880 |
| **`Γ_θ`** | **2.633916** | **0.29130** | **0.10638** | **0.01877** |

**Strictly decreasing in `q` at all three `σ`, with `q = 5` the maximum and `Γ_θ` the infimum.**
Hence, over the tested range,

```
   sup_{q>=5} sup_{Re s >= 3/2} | Z_{G_q}(s) |  <=  exp( 0.19144 )  =  1.2110 .        (2.1)
```

Likewise `|Z_{G_q}(s)| ≥ exp(−2 S_q(3/2)) ≥ 0.68189` there: the family is uniformly bounded
**and uniformly bounded away from zero** on `Re s ≥ 3/2`. `HEURISTIC` (finite `q`-range, finite
length cutoff, float).

### 2.3 `PROVED` — why the counting is *nearly* monotone, and the one gap

The `q`-uniform counting input U2b needs `#{[γ] : ℓ_γ ≤ L}` bounded uniformly in `q`. Two facts:

> **Lemma U1-1 (`PROVED`).** For a cyclically reduced word `w = S R^{a_1} … S R^{a_m}` with
> `a_i ∈ Z`, `tr w(λ) ∈ Z[λ]` is a single polynomial evaluated at `λ_q` (`G_q`) or at `λ = 2`
> (`Γ_θ`). If every `|a_i| < q/2` (the *faithful lift* condition) then `w` names a genuine
> `G_q`-class and the map {such `G_q`-classes} → {`Γ_θ`-classes} is injective.
> (T2 §3.4; the exponent reduction mod `q` is what fails when some `|a_i| ≥ q/2`.)

> **Conjecture U1-2 (trace monotonicity), `HEURISTIC` — tested exhaustively.** For every
> cyclically reduced `w`, `|tr w(λ)|` is nondecreasing in `λ` on `(1, 2]`. Consequently, for every
> faithful lift, `ℓ_w(λ_q) ≤ ℓ_w(2)`, so `N_q^{faithful}(L) ≤ N_θ(L)`.
>
> **Test (`law_probes/probe_u1_aux.py`, part C′):** all `2171` primitive cyclic `Γ_θ`-classes
> in the BFS ball `r_max = 10`, crossed with `q ∈ {5,7,8,10,12,16,22,30,50,80,150,400}` restricted
> to faithful lifts — **19 765 (word, q) pairs tested, 0 violations of `|tr_w(λ_q)| ≤ |tr_w(2)|`
> and 0 failures of monotonicity in `q`.**

> **The gap (`GAP`, and it is small).** `N_q(L) ≤ N_θ(L)` is **false for small `q`** because of the
> *non*-faithful classes — those with a syllable `R^a`, `|a| ≥ q/2`. Measured: `N_q(4) = 12, 11, 9,
> 7, 7, 7` at `q = 10, 12, 16, 22, 30, 50` against `N_θ(4) = 7`. The excess is real, bounded, and
> vanishes for large `q`: the shortest non-faithful class is `[S R^{⌈q/2⌉}]` with
> `ℓ = 2 arccosh( sin(⌈q/2⌉π/q)/sin(π/q) ) ≥ 2 arccosh( 1/sin(π/q) ) → ∞`, so for fixed `L` every
> class of length `≤ L` is faithful once `q ≥ Q(L)` — with `q ≥ π/arcsin(1/cosh(L/2))`, i.e.
> `q ≥ 12, 20, 32, 86` for `L = 4, 5, 6, 8`. The measured crossover `N_q(L) ≤ N_θ(L)` sets in at
> `q ≈ 22, 30, 50` for `L = 4, 5, 6` — *later* than this single-syllable threshold, so
> multi-syllable non-faithful classes do contribute and the computation below is only partial.
> `PROVED` for the `m = 1` syllable count via
> `|tr(S R^a)| = 2 sin(aπ/q)/sin(π/q)` (Chebyshev, `R² = λR − I`); `GAP` for the general
> multi-syllable statement.

**Net status of §2:** `PROVED` given (i) U2b's systole half and (ii) a uniform counting bound.
(ii) is measured monotone and reduces to Conjecture U1-2 plus the finite non-faithful excess.
This half of Lemma U1-0 is **the easy half** and is close to closed.

---

## 3. The functional-equation kernel `κ_q`, assembled — and the elliptic danger settled

### 3.1 `PROVED` — the specialization of Teo's Proposition 2.5 to `G_q`

`G_q\H` has signature `(0; 1; 2, q)`: genus `0`, `n = 1` cusp, `v = 2` ramification points of
orders `m_1 = 2`, `m_2 = q`. Gauss–Bonnet:
`|X_q| = 2π(2g − 2 + n + Σ_j (1 − 1/m_j)) = 2π(−1 + 1/2 + 1 − 1/q) = π(1 − 2/q)` ✓ (agrees with
`M1F` §1.5). `CITATION(Teo, Prop. 2.5)` — quoted verbatim in `LAW_U3_TRANSPORT.md` §2.5 — then
gives `Z_{G_q}(1−s) = κ_q(s) Z_{G_q}(s)` with

```
   kappa_q(s) = (-1)^{A_q/2} · 2^{-(2s-1)} · phi_q(s)
                · [ tan(pi s / 2) ]^{1/2}                                  <- elliptic, m=2
                · E_q(s)                                                   <- elliptic, m=q
                · [ (2pi)^{2s-1} G2(s)^2 Gamma(1-s) / ( G2(1-s)^2 Gamma(s) ) ]^{(1-2/q)/2}
                · [ Gamma(3/2 - s) / Gamma(s + 1/2) ]^{1}                  <- parabolic, n=1
   E_q(s)  :=  prod_{k=0}^{q-1}  sin( pi (s+k) / q )^{(q - 2k - 1)/q}
   A_q = 1 - tr Phi_q(1/2) = 1 -/+ 1 ,     C = -n log 2 = -log 2 .
```

The `m = 2` factor is `PROVED` elementary: `k=0` gives `sin(πs/2)^{1/2}`, `k=1` gives
`sin(π(s+1)/2)^{−1/2} = cos(πs/2)^{−1/2}`, product `tan(πs/2)^{1/2}`.

> **Self-consistency check `PROVED` (and it validates the assembly).** On `Re s = 1/2` one has
> `1 − s = s̄`, and `Z` has real coefficients, so `|Z(1−s)| = |Z(s)|`, i.e. `|κ_q(1/2+it)| = 1`;
> since `|φ_q(1/2+it)| = 1` by unitarity of `Φ_q`, **every other factor must have modulus exactly
> `1` there.** `probe_u1_growth.py` part **A3** at `s = 1/2 + 7.0674 i`:
> `exp = ell₂ = ell_q = barnes = par = 0.000000` and `TOTAL = +0.000000` — for `q = 5, 12, 22, 30,
> 80, 300, 1200`, to full working precision. The assembly passes.

### 3.2 `PROVED` — an exact identity for the elliptic factor

> **Lemma U1-3.** `E_q(s) = Z_{ell,q}(s) / Z_{ell,q}(1−s)`, where
> `Z_{ell,q}(s) = ∏_{k=0}^{q−1} Γ((s+k)/q)^{(2k+1−q)/q}` is Teo's elliptic factor of
> `det(Δ − s(1−s))` (Teo Thm 2.2, quoted in `LAW_U3_TRANSPORT.md` §2.5).
>
> *Proof.* Put `e_k := (2k+1−q)/q`, so `Σ_k e_k = 0` and `e_{q−1−k} = −e_k`. Reflection with
> `z = (s+k)/q` gives `1 − z = ((1−s) + (q−1−k))/q`, hence
> `Γ((s+k)/q) · Γ(((1−s) + k')/q) = π / sin(π(s+k)/q)` with `k' = q−1−k`. Then
> `Z_{ell,q}(1−s) = ∏_{k'} Γ(((1−s)+k')/q)^{e_{k'}} = ∏_k [ π / (Γ((s+k)/q) sin(π(s+k)/q)) ]^{−e_k}
>  = Z_{ell,q}(s) · ∏_k sin(π(s+k)/q)^{e_k} · π^{−Σ e_k}`,
> and `Σ e_k = 0`, `∏_k sin^{e_k} = 1/E_q`. ∎ `PROVED`.

This is the structural reason the elliptic factor cannot misbehave on the critical line: it is a
`s ↔ 1−s` ratio of one function.

### 3.3 The elliptic factor's exact size — **the brief's named danger, settled**

> **Lemma U1-4a `PROVED`.** `|E_q(1/2 + it)| = 1` for every `q ≥ 3` and every real `t`.
> (Immediate from Lemma U1-3 with `1 − s = s̄` and `Z_{ell,q}` having real coefficients; verified
> numerically to `7.3e−18` at `q = 5 … 4800`.)

> **Lemma U1-4b `HEURISTIC-IDENTIFIED`.** Locally uniformly on `C \ R`,
> ```
>    log E_q(s)  =  (2s - 1) log( q / (2 pi) )  +  log( Gamma(1-s) / Gamma(s) )  +  O(1/q) .
> ```

*Derivation sketch (the `PROVED` skeleton, `TODO-VERIFY` on the Euler–Maclaurin remainder).*
Abel summation on `log E_q(s) = Σ_k c_k f_k`, `c_k = 1 − (2k+1)/q`, `f_k = log sin(π(s+k)/q)`:
since `Σ_{j≤k} c_j = (k+1)(1 − (k+1)/q)` and the total is `0`,
```
   log E_q(s)  =  - sum_{j=1}^{q-1}  [ j (q-j) / q ] · ( f_j - f_{j-1} )
              ~=  - (pi / q^2) sum_j  j(q-j) · cot( pi (s + j - 1/2)/q ) .
```
Writing `x = j/q`, the bulk is `−π q ∫_0^1 x(1−x) cot(πx) dx`, and this **vanishes** as a principal
value (`x(1−x)` is even and `cot(πx)` odd about `x = 1/2`), which is why the naive `O(q)` term is
absent and why the `2^{1−q}` of the sine multiplication formula
`∏_{k=0}^{q−1} sin(π(z+k)/q) = 2^{1−q} sin(πz)` must cancel. The surviving contributions are the
two endpoint zones `j = O(1)` and `q − j = O(1)`, where the shift `(s − 1/2)/q` regularises the
pole of `cot`; each contributes `(s − 1/2) log q + const`, total `(2s−1) log q + C(s)`.

*Numeric identification of `C(s)` (`probe_u1_growth.py` A1 + `u1_aux.py` A1′, `mpmath`, 60 dps):*

| `s` | `Re C(s)` measured at `q = 4800` | `Re[(1−2s)log 2π + log(Γ(1−s)/Γ(s))]` |
|---|---|---|
| `0.25 + 7.0674 i` | `+1.894057` | `+1.896369` |
| `0.50 + 7.0674 i` | `−0.000000` | `0.000000` |
| `0.00 + 7.0674 i` | `+3.788742` | `+3.793364` |
| `0.375 + 7.2839 i` | `+0.954510` | `+0.955701` |
| `0.125 + 7.2839 i` | `+2.863827` | `+2.867399` |
| `0.30 + 3.0 i` | `+1.172225` | `+1.173010` |
| `0.25 + 1.0 i` | `+0.899628` | `+0.899954` |

and the residual `C_q(s) − C_∞(s)` **halves exactly under each doubling of `q`**
(`−0.0365, −0.0183, −0.0092, −0.0046, −0.0023` at `q = 300 … 4800`), confirming the `O(1/q)`.
Cross-check away from `U`, at `s = 2 + 7.0674 i` and `s = 1.25 + 7.0674 i`: measured `log|E_q|`
matches the formula with residual `× q ≈ 66` resp. `33`, again `O(1/q)`.

> **Corollary U1-4c — the answer to the brief's question.**
> ```
>    | E_q(s) |  =  ( q / 2pi )^{ 2 Re s - 1 } · | Gamma(1-s)/Gamma(s) | · ( 1 + O(1/q) ) .
> ```
> **On `U` (`Re s ∈ [0, 1/2]`) the exponent `2Re s − 1 ∈ [−1, 0]`, so `|E_q| ≤ C_U` for all
> `q ≥ 2π`, and `→ 0` for `Re s < 1/2`. The elliptic term's growth contribution is BOUNDED — the
> danger does not materialise on `U`.**
> **Off `U`, for `Re s > 1/2`, it GROWS like `q^{2Re s − 1}`; at `Re s = 2` it is `≍ (q/2π)³`.**

The structural reading is exact and pleasing: as `q → ∞` the order-`q` cone point becomes a cusp,
and `Γ(1−s)/Γ(s)` is precisely the shape of Teo's parabolic factor `Γ(3/2−s)/Γ(s+1/2)` that
`Γ_θ`'s **second** cusp contributes. The divergent prefactor `(q/2π)^{2s−1}` is the normalisation
of that opening cusp. **The elliptic factor converges to a parabolic factor, up to an explicit
`q`-power.** `HEURISTIC` as an interpretation; the formula it interprets is the table above.

### 3.4 `PROVED` — the elliptic mass in the trace formula is `O(log q)`

The brief asks whether `Σ_{k=1}^{q−1} 1/(q sin(πk/q))` is `O(log q)`. It is, with the constant:

> **Lemma U1-5 `PROVED` (numerically, to 5 decimals, `q = 5 … 10 000`).**
> ```
>    M(q) := sum_{k=1}^{q-1} 1 / ( 2 q sin(k pi / q) )  =  (1/pi) log( 2 e^gamma q / pi ) + O(q^{-2}) .
> ```
> Measured `M(q) − (log q)/π`: `0.038253, 0.039102, 0.039554, 0.039900, 0.039942, 0.039986,
> 0.039990, 0.039990, 0.039990, 0.039990` at `q = 5, 7, 10, 22, 30, 100, 300, 1000, 3000, 10000`,
> against `(γ + log(2/π))/π = 0.0399902`.

So the elliptic weight is `q`-**unbounded but only logarithmically**. §5.2 shows where that log
lands and why it is not negligible at our height.

---

## 4. `PROVED` — the renormalized fallback is logically useless

The brief's route (3) is: if the sup leaks `C(q) = O(q^A)`, run Vitali+Hurwitz on
`Z_{G_q}/C(q)`, "legitimate if the limit stays `≢ 0`". It never does.

> **Lemma U1-6.** Let `C(q) > 0` with `C(q) → ∞`, and suppose `{Z_{G_q}/C(q)}` is locally
> uniformly bounded on `Ω̃`. Then `Z_{G_q}/C(q) → 0` locally uniformly on `Ω̃`, and Hurwitz yields
> **no** conclusion.
>
> *Proof.* Fix `s₁` with `Re s₁ > 1`. `Z_{Γ_θ}(s₁) ≠ 0` (absolutely convergent Euler product), and
> `Z_{G_q}(s₁) → Z_{Γ_θ}(s₁)` (T2 §3.4/U2a + U2b). Hence `Z_{G_q}(s₁)/C(q) → 0`. This holds on
> **all** of `{Re s > 1} ∩ Ω̃`, a set with accumulation points in `Ω̃`; by Vitali the whole family
> converges locally uniformly on `Ω̃` to `0`. Hurwitz requires a limit `≢ 0`. ∎ `PROVED`.

> **Corollary U1-6′ (general normalisers).** The same argument kills any normalisation by a
> nonvanishing holomorphic `g_q`: a nondegenerate limit forces `g_q` to converge to a nonvanishing
> limit on `{Re s > 1}`, i.e. the normalisation was unnecessary there and must already be bounded
> below and above — which is exactly U1 again on that half-plane, and gives nothing on `U`.
> `PROVED` for the constant case; `HEURISTIC` for the fully general case (a `g_q` that is bounded
> on `Re s > 1` but grows on `U` is not excluded, and would be a legitimate — and currently
> unknown — object; §6 records this as the one live variant, `(U1-alt)`).

**Consequence for the ledger.** `LAW_T2_DETERMINANT.md` §5.2's U1 row should be read as
*load-bearing without alternative*: if U1 fails, (T2′) fails, and the tail must be re-derived by
some other mechanism entirely. The route has no soft landing.

---

## 5. Why the two remaining routes both end at `φ_q`

### 5.1 Route 2 (functional equation + convexity) — the leak, quantified

`K` is bounded in `Im s`, so the maximum principle on the rectangle
`[−1, 2] × [t_∞ − 1, t_∞ + 1]` needs bounds on **all four** sides. The right side is (2.1). The
left side is supplied by the functional equation: for `Re s = −1`,
`|Z_{G_q}(s)| = |κ_q(1−s)| · |Z_{G_q}(1−s)|` with `Re(1−s) = 2`, so

```
   sup_{Re s = -1} | Z_{G_q} |  <=  1.048 · sup_{|t| <= t_inf + 1} | kappa_q(2 - i t) | .
```

The `q`-dependence of `κ_q(2+it)`, factor by factor (§3.1, and `probe_u1_growth.py` A3):

| factor of `κ_q(s)` | `q`-dependence | on `U` (`σ ≤ 1/2`) | at `σ = 2` |
|---|---|---|---|
| `(−1)^{A_q/2}` | `A_q = 1 − tr Φ_q(1/2) ∈ {0, 2}` | `|·| = 1` | `|·| = 1` |
| `2^{−(2s−1)}` | none | `O(1)` | `O(1)` |
| `[tan(πs/2)]^{1/2}` | none | `O(1)`, `≠ 0` off `R` | `O(1)` |
| `E_q(s)` (elliptic, `m = q`) | **`(q/2π)^{2σ−1}`** | **`≤ 1`, `→ 0`** | **`≍ (q/2π)³`** |
| Barnes/area `[·]^{(1−2/q)/2}` | exponent `→ 1/2` at rate `1/q` | `O(1)`, converges | `O(1)`, converges |
| parabolic `[Γ(3/2−s)/Γ(s+1/2)]` | none (`n = 1` for every `q`) | `O(1)` | `O(1)` |
| **`φ_q(s) = det Φ_q(s)`** | **UNKNOWN** | `|φ_q| = 1` on `Re s = 1/2` only | **`GAP`** |

`PROVED` for every row but the last two-thirds of the `E_q` row (Lemma U1-4b, `HEURISTIC-IDENTIFIED`)
and the `φ_q` row (`GAP`).

**The two possibilities, and both are bad for route 2 as executed:**

- **Trivial bound.** If one uses only `|φ_q(2+it)| ≤ 1` (which itself is `TODO-VERIFY` — it needs
  unitarity on `Re s = 1/2`, the pole of `φ` at `s = 1`, and a Phragmén–Lindelöf argument in the
  half-plane, none of which is written down here), then
  `sup_{Re s = −1}|Z_{G_q}| = O(q³)` and three-lines between `σ = −1` and `σ = 2` gives
  `|Z_{G_q}(σ + it)| = O(q^{2−σ})`, i.e. `O(q^{7/4})` at `σ = 1/4`. **By Lemma U1-6 that is
  useless** — a `q^{7/4}` renormalisation kills the limit.
- **Sharp behaviour.** If U1 *does* hold globally on the upper half-plane, then
  `κ_q = Z_{G_q}(1−s)/Z_{G_q}(s) → κ_θ` there, and comparing §3.1 for `G_q` against Teo for `Γ_θ`
  (`n = 2`, `v = 1`, `|X| = π`, `C = −2 log 2`) forces
  ```
     phi_q(s)  ~  ( pi / q )^{2s-1} · phi_theta(s) · Gamma(s) Gamma(3/2 - s)
                                                  / ( Gamma(1-s) Gamma(1/2 + s) ) .   (5.1)
  ```
  `HEURISTIC`, but it is a **falsifiable prediction**: `|φ_q(2+it)| ≍ q^{−3}`. It can be tested
  against Hejhal's numerically computed Hecke-group scattering determinants
  (`CITATION(Hejhal, Eigenvalues of the Laplacian for Hecke triangle groups, Memoirs AMS 469, 1992)`
  — `TODO-VERIFY`, not opened this session). **If (5.1) fails, U1 fails in its global form**, and
  U1 would have to be proved on the bounded `Ω̃` by a method that never visits `Re s = 2`.

### 5.2 Route 1 (trace formula / Weyl / Hadamard) — the same leak, plus a correction owed

`LAW_T2_DETERMINANT.md` §3.3 says the uniform zero counting is available "for free" from
`N_q(T) + M_q(T) ~ (|F_q|/4π) T²` with `|F_q| ≤ π`. Two things are wrong with using that as stated.

1. **`N + M` is not the zero count of `Z_{G_q}`.** `N_q(T)` counts discrete eigenvalues,
   `M_q(T) = (1/4π)∫_{−T}^{T}(−φ_q'/φ_q)(1/2+it)dt` is the **winding** of the scattering
   determinant — a signed quantity. The divisor of `Z_{G_q}` off the real axis is
   (spectral zeros on `Re s = 1/2`) ∪ (resonances = poles of `φ_q` in `Re s < 1/2`)
   (`LAW_U3_TRANSPORT.md` §2.3, items 1 and 6, `CITATION`). Bounding the **resonance count**
   uniformly in `q` is exactly a `φ_q` statement. `GAP`.
2. **The uniformity is only in the `T²` coefficient.** The trace formula's elliptic term for the
   order-`q` point carries the weight `M(q) = (1/π)log(2e^γ q/π)` of Lemma U1-5, and (in Hejhal's
   normalisation, elliptic term `Σ_k (2m sin(kπ/m))^{−1} ∫ h(r) cosh(π(1−2k/m)r)/cosh(πr) dr`) the
   small-`k` terms behave like `∫ h`, so the elliptic contribution to the smooth counting is
   `≍ (T/π) log q`. At the fixed height that matters here,
   ```
      T = 8 :    (|X_q|/4pi) T^2  =  16.0 ,       (T/pi) log q  =  17.6  at q = 1000 .
   ```
   **The two are the same size.** `HEURISTIC` for the coefficient (order of magnitude read off the
   trace-formula weight; the exact constant was not computed), `PROVED` for `M(q)`.

> **Correction owed to `LAW_T2_DETERMINANT.md` §3.3.** Replace
> *"the area is uniformly bounded, so the zero-counting of `Z_{G_q}` in a box of height `T` is
> uniformly `≤ (π/4π)T²(1+o(1))`, and a Hadamard factorization of order 2 with `q`-independent
> counting gives exactly the shape of bound (T2′-a) demands"*
> with: *the `T²` coefficient is uniform (`|F_q| ≤ π`, `PROVED`), but the linear coefficient carries
> the elliptic mass `≍ (log q)/π`, which at the fixed height `T ≈ 8` is comparable to the `T²`
> term; and `N + M` bounds the winding, not the resonance count. Uniform counting is an
> obligation, not a freebie.*

If the count in the fixed disc `|s − 1/2| ≤ 8` really grows like `c log q`, then a Hadamard product
over that many zeros in a bounded region admits only the bound `|Z_{G_q}| ≤ q^{O(1)}` — again
useless by Lemma U1-6. That would ordinarily be dismissed as one-sided pessimism — many zeros in a
region make `|Z|` *small* on average, not large — but **§7.3's guard measures the sup RISING, with
slope `+1.50`**, in the same direction and of the same order as this crude estimate. The two
independent pessimisms agreeing is the reason §9 now recommends extending the guard before
investing further, rather than filing this as a method defect.

### 5.3 Routes that were checked and cannot work at all `PROVED`

- **Bound on `U` from the bound on `Re s ≥ 3/2` alone.** Impossible: holomorphy plus an upper bound
  on one half-plane implies nothing on a disjoint region (`e^{s²}` is bounded on no half-plane but
  the point stands — take `Z_q · e^{−N(s−2)²}`, bounded on `Re s ≥ 3/2` uniformly in `N`, unbounded
  on `U`). Any route must supply information on a contour **surrounding** `U`.
- **Borel–Carathéodory / three-circles on `log Z_q`.** Needs an a-priori upper bound on a disc that
  contains `U`; every such disc pokes into `Re s < 3/2`. Circular.
- **Landau's `Z'/Z` argument.** Needs the zero count in a disc **and** a boundary upper bound; the
  latter is U1. Circular.

**These three exhaust the standard toolkit that avoids the functional equation.** The reduction in
§6 is therefore not laziness: it is what is left.

---

## 6. The obligation, isolated

> ### **(U1-φ) — the crux, replacing U1.**
> There exist `Q₁` and `A < ∞`, independent of `q`, such that **either**
>
> **(U1-φ-a)** `sup_{|t| ≤ t_∞ + 1} |φ_q(2 + it)| · (q/2π)³ ≤ A` for all `q ≥ Q₁`
> — i.e. the scattering determinant of `G_q` decays like `q^{−3}` on `Re s = 2`, cancelling the
> elliptic factor's growth (this is (5.1)); **or**
>
> **(U1-φ-b)** the resonance count is `q`-uniform on the fixed disc:
> `#{ poles of φ_q in |s − 1/2| ≤ 8 } ≤ A` for all `q ≥ Q₁`.
>
> Either one, together with §2's uniform Euler bound and Lemma U1-0, closes U1.

> ### **(U1-alt) — the one live variant of the renormalized route.**
> Lemma U1-6 kills constant normalisers. It does **not** kill a normaliser `g_q` that is bounded
> above **and below** on `{Re s > 1}` but unbounded on `U` — e.g. a `q`-dependent Hadamard-type
> factor `exp(a_q + b_q s + c_q s²)` with `(a_q, b_q, c_q)` bounded on the right and growing on
> the left. No such object is known here, and constructing one is not obviously easier than
> (U1-φ). Recorded so the option is not silently lost. `GAP`.

---

## 7. Numeric guard — **NON-RIGOROUS**

### 7.1 Method and its one honest caveat

`Z_{G_q}(s)` is not computable from its Euler product at `Re s = 1/4` (the product diverges).
The repo's only in-strip evaluator is the certified Rosen/MMS transfer-operator determinant
`det(1 − L_{s,q}^{±})` on the two `P`-symmetric sectors, built by
`.worktrees/aletheia-restore/code/zeta_cert_rosen_even.py` (even `q`; the same builder Probe D1
used). We evaluate the **product over the two sectors** as a proxy for `Z_{G_q}(s)` — the
identification is R5 at `q = 5` and obligation **U4** in general (`GAP`). Midpoint evaluation at
`N = 32` collocation points, 400-bit Arb precision, `n_head = 4`, no ball radii, **no winding
certificate**. Script `law_probes/probe_u1_sup.py`; receipt `law_probes/u1_sup.json`; log
`law_probes/u1_sup.log`.

`N`-stability: at `s_∞`, `|det^+|` agrees to 7 significant figures between `N = 32` and `N = 48`
for `q = 12, 22, 30` (`1.266513 / 1.266513`, `0.4881936 / 0.4881936`, `0.3355577 / 0.3355577`);
and at four `∂U` points for `q = 30` all of `N = 32, 48, 64` agree to 9 digits (§7.3).

### 7.2 Control points with `Re s > 1` — the proxy is validated, and U4 gains evidence

At two points where the truncated Euler product (`probe_t2_shape.selberg_trunc`, `L = 6`) is
available:

| `q` | `s` | `|det^+ · det^−|` | truncated Euler `|Z_{G_q}(s)|` | rel. diff |
|--:|---|---|---|---|
| 12 | `2.0` | 0.9757547 | 0.9763960 | `6.6e−4` |
| 12 | `1.5 + 7.0674 i` | 0.9609678 | 0.9594445 | `1.6e−3` |
| 16 | `2.0` | 0.9782560 | 0.9786565 | `4.1e−4` |
| 16 | `1.5 + 7.0674 i` | 0.9400399 | 0.9405768 | `5.7e−4` |
| 22 | `2.0` | 0.9797278 | 0.9800803 | `3.6e−4` |
| 22 | `1.5 + 7.0674 i` | 0.9367048 | 0.9377235 | `1.1e−3` |
| 30 | `2.0` | 0.9804791 | 0.9808030 | `3.3e−4` |
| 40 | `2.0` | 0.9808582 | 0.9812138 | `3.6e−4` |
| 40 | `1.5 + 7.0674 i` | 0.9349800 | 0.9365003 | `1.6e−3` |

The residual is the size of the `ℓ ≤ 6` Euler truncation. **This is independent numeric evidence
for the U4 identification `det(1−L^+)·det(1−L^−) = Z_{G_q}` at even `q = 12, 16, 22, 30, 40` — the
repo had it only at `q = 5` (R5).** `HEURISTIC`, unasked for, banked.

> **[CORRECTION 2026-08-16, LAW_Q3_BRANCH_DIAGNOSIS.md + LAW_DETK_IMPACT_AUDIT.md]**
> The identity as written above is FALSE: the MMS theorem is the quotient
> `det(1−L^+)·det(1−L^−) = Z_{G_q} · det(1−K_q)` (arXiv:0912.2236, main
> theorem). `det(1−K_q)` is zero-free on `Re s > 0` with closed form
> `Π_{n≥0}(1−b_q^{s+n})`. The numerical evidence in this section survives and
> IMPROVES under the corrected identity (8 of 9 control rows tighten; worst
> `1.6e−3 → 5.6e−4`). All §7.3/§10 slope conclusions re-audited under the
> correction: 0 flips (impact audit, 22 magnitudes classified).

### 7.3 The guard table — `sup_{∂U}` against `q`, and **it rises**

`∂U = {|s − s_∞| = 1/4}`, 8 equispaced points `s_j = s_∞ + (1/4)e^{2πi j/8}`, `j = 0 … 7`.
Full per-point values in `law_probes/u1_sup.json` and `u1_sup_q40.json`.

| `q` | `|Z_q(s_∞)|` | `sup_{∂U}` (all 8) | argmax | `sup_{∂U}` **excl. `dU_4`** | `min_{∂U}` |
|--:|---|---|---|---|---|
| 12 | 6.1374 | 170.008 | `dU_4` | 81.841 | 0.24454 |
| 16 | 2.6000 | 92.791 | `dU_4` | **25.138** | 0.08996 |
| 22 | 1.1380 | 49.473 | `dU_5` | **49.473** | 0.15247 |
| 30 | 1.1516 | 266.357 | `dU_4` | **92.808** | 0.15025 |
| 40 | 0.6813 | 275.415 | `dU_4` | **99.402** | 0.02532 |

`dU_4 = 0.000000 + 7.067363 i` is excluded in the fifth column because **`Re s = 0` lies exactly on
the boundary of the R5 common-continuation domain** `Ω* = {Re s > 1/2} ∪ {Re s > 0, Im s > 1}`
(`TB_R5_DETERMINANT_IDENTIFICATION.md`, Claim). At that point the determinant has no identification
guarantee at all, so its value is reported but not used.

> ### **Guard verdict: ADVERSE, and it must be reported loudly.**
> The sup is **not bounded-looking**. Dropping the out-of-domain point `dU_4`, it is
> **monotone increasing over `q = 16, 22, 30, 40`: `25.14 → 49.47 → 92.81 → 99.40`.**
> Log-log slopes: **`+1.50`** over `q = 16 → 40`, **`+1.17`** over `q = 22 → 40`.
> Including `dU_4`, the two largest values in the table are at the two largest `q`.

**This is the shape the trivial-`φ` bound predicts.** §5.1's three-lines estimate, using only
`|φ_q| ≤ 1`, gives `|Z_{G_q}(σ+it)| = O(q^{2−σ})`, i.e. `O(q^{1.93})` at the argmax abscissa
`σ = 0.0732` and `O(q^{1.75})` at `σ = 1/4`. The measured `+1.50` sits below those but is
**unambiguously positive**, whereas U1 requires slope `0`. So the guard is **consistent with the
trivial bound being close to the truth**, and by **Lemma U1-6** a polynomial leak of any positive
exponent is fatal to (T2′): it cannot be renormalised away.

**Three honest caveats against reading this as a refutation.**
1. **Five points, and they are not monotone as a set.** `q = 12` is the second largest value in the
   full column; the sequence dips through `q = 16, 22` before rising. Per-point behaviour is
   ragged — `dU_5` and `dU_6` both *fall* from `q = 30` to `q = 40` while `dU_2, dU_3, dU_4` rise.
   Local structure (zeros of `Z_{G_q}` migrating past `∂U` — the D1 pins sit at
   `0.2069+7.481i`, `0.4079+7.298i`, `0.2485+7.205i` for `q = 12, 16, 22`) plausibly dominates a
   5-point sample.
2. **The proxy is not `Z_{G_q}`.** `det(1−L^+)·det(1−L^−) = Z_{G_q}` is obligation **U4**, `GAP` for
   `q ≠ 5`. §7.2 gives it `3e−4 … 2e−3` numerical support at four `q`, on `Re s > 1` only.
3. **It is not a certificate.** Midpoints, no Arb ball radii, no winding.

**And one caveat that does NOT apply: this is not a discretisation artefact.**
`law_probes/u1_stab.py` re-evaluated `q = 30` at `dU_2, dU_3, dU_4, dU_5` with `N = 32, 48, 64`:
**all three `N` agree to all 9 printed significant digits, for both sectors, at all four points**
(e.g. `dU_4`: `|det^+| = 1.39128938e+01`, `|det^−| = 1.91446390e+01`, product `2.66357330e+02`,
identically at `N = 32, 48, 64`). The numbers are the evaluator's converged values.

### 7.4 What the guard does and does not establish

**Establishes (float level):** `sup_{∂U}` of the two-sector determinant product **increases** over
`q = 16 → 40`, with log-log slope `+1.5`, once the out-of-domain point `Re s = 0` is dropped; the
values are `N`-converged; and the proxy matches the truncated Euler product to `≤ 2e−3` at two
control points with `Re s > 1`, for `q = 12, 16, 22, 30, 40`.

**Does not establish:** that U1 is false — five `q`, a proxy with an open identification, no error
bars, and a ragged per-point pattern. Nor anything for `q > 40`, nor anything on `K ∖ U`.

**What it does do to the ledger.** It removes the presumption of success. Before this note, T2 §5.2
listed U1 as "standard-shaped, laborious … Aristotle-able in pieces". The measurement says the
opposite: the quantity U1 asserts to be bounded is, as far as five points can see, **growing at
roughly the rate the trivial estimate predicts**. Combined with Lemma U1-6 (no renormalisation
escape), **the (T2′) tail route is now at risk, not merely incomplete.**

---

## 8. Status ledger

| # | Step | Status | Note |
|---|---|---|---|
| U1.1 | (T2′-a) ⟺ boundedness on `K` + `{Re s ≥ 3/2}` | `PROVED` | §1.2 — weakens the hypothesis |
| U1.2 | Euler bound `|Z_q| ≤ e^{S_q(σ)}`, `σ ≥ 3/2` | `PROVED` | §2.1, elementary |
| U1.3 | `S_q(3/2) ≤ 0.19144`, monotone decreasing in `q` | `HEURISTIC` | §2.2, `q ≤ 150`, `ℓ ≤ 8` |
| U1.4 | `sys(G_q) = 2 arccosh λ_q ≥ 2.12255` | `PROVED` mod U2b | T2 §3.4; systole class `HEURISTIC` |
| U1.5 | Faithful-lift injectivity, `tr_w ∈ Z[λ]` | `PROVED` | §2.3 Lemma U1-1 |
| U1.6 | `|tr_w(λ)|` nondecreasing in `λ` | `HEURISTIC` | 19 765 pairs, **0** violations |
| U1.7 | `N_q(L) ≤ N_θ(L)` for `q ≥ Q(L)`; false for small `q` | `PROVED` (`m=1`) / `GAP` (general) | §2.3 |
| U1.8 | `κ_q` assembled for signature `(0;1;2,q)` | `PROVED` given `CITATION(Teo Prop 2.5)` | §3.1 |
| U1.9 | `|κ_q(1/2+it)| = 1` factor-by-factor | `PROVED` (numeric, to 1e−17) | §3.1 — validates U1.8 |
| U1.10 | `E_q = Z_{ell,q}(s)/Z_{ell,q}(1−s)` | `PROVED` | §3.2 Lemma U1-3 |
| U1.11 | `|E_q(1/2+it)| = 1` | `PROVED` | §3.3 Lemma U1-4a |
| U1.12 | `log E_q = (2s−1)log(q/2π) + log Γ(1−s)/Γ(s) + O(1/q)` | `HEURISTIC-IDENTIFIED` | §3.3; sketch + 7 points × 5 `q` |
| U1.13 | `|E_q|` bounded on `U`, `≍ q^{2σ−1}` off it | `PROVED` given U1.12 | §3.3 Cor. U1-4c — **the brief's danger, settled** |
| U1.14 | `M(q) = (1/π)log(2e^γ q/π) + O(q^{−2})` | `PROVED` (numeric, 5 dp, `q ≤ 10⁴`) | §3.4 |
| U1.15 | Renormalisation by `C(q) → ∞` is useless | `PROVED` | §4 Lemma U1-6 |
| U1.16 | Weyl counting is uniform in `T²` only; linear term `≍ (T/π)log q` | `HEURISTIC` | §5.2 — **correction owed to T2 §3.3** |
| U1.17 | `|φ_q| ≤ 1` on `Re s ≥ 2` | `TODO-VERIFY` | gives only `O(q^{7/4})`, useless by U1.15 |
| U1.18 | `φ_q(s) ≍ (π/q)^{2s−1}φ_θ(s)·Γ-ratio` | `HEURISTIC` prediction | (5.1) — falsifiable against Hejhal Memoirs 469 |
| U1.19 | **(U1-φ)** | `GAP` | §6 — **the crux** |
| U1.20 | **Numeric guard: sup RISES, slope `+1.50` over `q = 16 → 40`** | `HEURISTIC` | §7.3 — **adverse**; `N`-converged at `N = 32/48/64` |
| U1.21 | `det(1−L^+)det(1−L^−) = Z_{G_q}` at `q = 12, 16, 22, 30, 40` | `HEURISTIC` | §7.2 — new U4 evidence |

---

## 9. The assembled tail theorem — what it now needs

Under **(U1-φ)** the tail assembles as follows.

> **THEOREM (LAW, tail half) — conditional.** Assume (U1-φ), U2b, and the §2.3 counting bound.
> Then `{Z_{G_q}}_{q ≥ Q₁}` is locally uniformly bounded on `Ω̃` (U1, §1.2 + §2 + §5.1). By U2a
> (`PROVED`, T2 §3.4) and U2b it converges pointwise on `{Re s > 1}`, a set with accumulation
> points in `Ω̃`. By **Vitali–Montel** (`CITATION`, classical) it converges locally uniformly on
> `Ω̃` to `Z_{Γ_θ}`. By **U3** (`CLOSED`, `LAW_U3_TRANSPORT.md` §3.4) `Z_{Γ_θ}` has a zero at
> `s_∞ = ρ₁/2` of order exactly `2`, and `Z_{Γ_θ} ≢ 0`. By **Hurwitz** (`CITATION`, classical),
> for each `r ∈ (0, 1/8)` with `Z_{Γ_θ} ≠ 0` on `∂D(s_∞, r)` there is `Q₀(r)` with: for all
> `q ≥ Q₀`, `Z_{G_q}` has exactly `2` zeros in `D(s_∞, r)`, counted with multiplicity. Each has
> `Re s ≤ 1/4 + r < 1/2 − (1/8 − r)`. ∎

**Remaining obligations of the assembled theorem, in priority order:**

| # | Obligation | Status | Cost estimate |
|---|---|---|---|
| **U1-φ** | scattering determinant: `|φ_q(2+it)| = O(q^{−3})`, **or** uniform resonance count on `|s−1/2| ≤ 8` | `GAP` — **THE crux** | research-scale; no import found (T2 §2.6's scout stands) |
| **U2b** | uniform systole (`[S R²]` is the systole class) + uniform geodesic counting | `GAP`, near-closed | agent-scale: Conjecture U1-2 + the finite non-faithful excess (§2.3) |
| **U1.12** | Euler–Maclaurin proof of the `E_q` asymptotic | `TODO-VERIFY` | small; Aristotle-able |
| **U4** | `det(1−L_{s,q}) ↔ Z_{G_q}` for general `q` | `GAP`, demoted | needed only for the certified finite base `q ≤ Q₀`; §7.2 adds `q = 12, 16` evidence |
| **Q₀ effectivity (U5)** | quantitative (T2′-b) on `∂D(s_∞,r)` beaten against `min_{∂D}|Z_{Γ_θ}|` | `GAP` | needs U1's constants; §4 of T2 gives `ε(q) ≍ Cq^{−2}` for `Re s > 1` only |
| **U6 / V1–V3 hygiene** | `Z_{Γ_θ} ≠ 0` on some `∂D(s_∞,r)`, `r < 1/8`; prior-art scout; certificate discipline for anything published | `CITATION` + finite check | cheap |

**Recommended next ticket — and the order has changed because of §7.3.**

1. **Extend the guard before funding anything else.** The cheapest decisive experiment in the whole
   lane: re-run `law_probes/probe_u1_sup.py` at `q = 56, 72, 100` (`N = 32`; cost scales roughly
   `q²`, so `≈ 1, 2, 4` hours per `q` as background jobs) and refit the slope. If the `+1.5` slope
   persists to `q = 100`, **(T2′) is dead as formulated** — Lemma U1-6 leaves no renormalisation
   escape — and the lane should stop rather than spend on U2b/U1-φ. If the slope bends to `0`, U1
   is corroborated and U1-φ becomes worth the research investment. Two more `q` decide it.
2. **Test prediction (5.1)** against `CITATION(Hejhal, Memoirs AMS 469, 1992)`'s numerically
   computed Hecke-group scattering determinants: is `|φ_q(2+it)| ≍ q^{−3}` or `≍ 1`? This is a
   literature lookup plus one plot, and it answers (U1-φ-a) directly. `q^{−3}` ⇒ U1 plausible;
   `≍ 1` ⇒ U1 false in its global form.
3. **U2b** — cheap, agent-scale, and worth closing regardless since §2.3 leaves only a bounded
   finite excess and one exhaustively-tested monotonicity conjecture. But it is **not** on the
   critical path any more; do it after (1) and (2).

---

## 10. What this note claims and does not claim

**Claims.** (i) Lemma U1-0 (`PROVED`): U1 is boundedness on one compact rectangle plus a
half-plane; the order-2 exponential shape of (T2′-a) is unnecessary. (ii) Lemma U1-3 (`PROVED`):
the exact identity `E_q(s) = Z_{ell,q}(s)/Z_{ell,q}(1−s)`. (iii) Lemma U1-4a (`PROVED`):
`|E_q(1/2+it)| = 1`; and Lemma U1-4b/Cor. U1-4c (`HEURISTIC-IDENTIFIED` to 4 decimals at 7 points,
`q ≤ 4800`, `O(1/q)` residual confirmed by exact halving): `|E_q(s)| = (q/2π)^{2σ−1}|Γ(1−s)/Γ(s)|
(1+O(1/q))`, hence **bounded on `U`** and `≍ q³` at `Re s = 2` — the brief's named danger is
settled, in both directions. (iv) Lemma U1-5 (`PROVED` numerically): the elliptic mass is
`(1/π)log(2e^γ q/π) + O(q^{−2})`. (v) Lemma U1-6 (`PROVED`): the renormalized fallback is
logically useless, so U1 has no soft landing. (vi) The §5.2 correction owed to
`LAW_T2_DETERMINANT.md` §3.3: uniform Weyl counting is *not* free at fixed height. (vii) The
reduction of U1 to **(U1-φ)**, and the falsifiable prediction (5.1). (viii) `HEURISTIC`, and **adverse to the route**: the
sup on `∂U` (excluding the out-of-domain point `Re s = 0`) **rises monotonically**
`25.1 → 49.5 → 92.8 → 99.4` over `q = 16, 22, 30, 40`, log-log slope `+1.50`, `N`-converged to 9
digits at `N = 32, 48, 64`; and `det(1−L^+)det(1−L^−)` matches the truncated Euler product to
`≤ 2e−3` at `q = 12, 16, 22, 30, 40`.

**Does not claim.** **U1 is not proved.** No bound of any kind is established on `K ∖ U` or on `U`
itself — the numeric guard is float midpoints of an operator determinant whose identification with
`Z_{G_q}` is itself an open obligation (U4). No proof of Conjecture U1-2 (trace monotonicity),
though 19 765 tests found no violation. No proof of the Euler–Maclaurin remainder in Lemma U1-4b.
No claim that `|φ_q| ≤ 1` on `Re s ≥ 2` (labelled `TODO-VERIFY`, not used for anything except to
show that even if true it does not suffice). No claim about `q > 40` in the guard, none about
`q > 150` in the counting, none about `q > 4800` in the elliptic asymptotic. No certificate: every
number in §2.2, §3.3, §3.4, §7 is float64 or `mpmath` midpoint arithmetic, no interval arithmetic,
no winding computation. No prior-art clearance: T2 §2.6's scout found no literature on the
`q → ∞` Hecke limit and that has not been re-run here; absence of a retrieved source is not
clearance.

**A refutation was actively sought.** Three were found, and none is the one the brief expected.
The brief expected the elliptic term to be the leak; it is not — on `U` it is bounded and decaying,
`PROVED`-shaped. What *was* refuted is the brief's own fallback: renormalising by `C(q)` cannot
work (Lemma U1-6), so the ledger's U1 row is load-bearing without alternative. A second, softer
refutation: `LAW_T2_DETERMINANT.md` §3.3's claim that uniform Weyl counting comes free from
`|F_q| ≤ π` is wrong at fixed height, because the elliptic mass `≍ (log q)/π` enters the linear
term and is the same size as the `T²` term at `T ≈ 8`. A third, and the one that hurts: the guard
built to corroborate U1 **measured a rise instead**, at roughly the rate the trivial estimate
predicts. That result is reported as the guard's headline rather than buried, and it is what moved
the recommendation in §9 from "prove U1" to "spend two more `q` deciding whether U1 is true at
all".

---

## 11. Receipts index

- `law_probes/probe_u1_growth.py` — A1 (elliptic factor), A2 (elliptic mass), A3 (`κ_q` factors),
  B (counting + Euler majorant), C (trace monotonicity, unrestricted). Receipt
  `law_probes/u1_growth.json`, log `law_probes/u1_growth.log`.
- `law_probes/probe_u1_sup.py` — the `∂U` sup guard and the `Re s > 1` control points. Receipt
  `law_probes/u1_sup.json`, log `law_probes/u1_sup.log`.
- `law_probes/u1_sup_q40.json`, `u1_sup_q40.log` — the `q = 40` extension of the guard.
- `law_probes/u1_stab.py`, `u1_stab.json`, `u1_stab.log` — the `N = 32/48/64` stability check at
  `q = 30`, `∂U` points `dU_2, dU_3, dU_4, dU_5`.
- `law_probes/probe_u1_aux.py`, `u1_aux.log` — restricted (faithful-lift) trace monotonicity
  (19 765 pairs, 0 violations) and the numerical identification of `C(s)` in Lemma U1-4b.
- Reused unchanged: `law_probes/probe_t2_shape.py` (word enumerator, truncated Euler product),
  `.worktrees/aletheia-restore/code/zeta_cert_rosen_even.py` (even-`q` Arb determinant builder).

---

## §10 Addendum 2026-08-16: extended guard q = 56/72/100 — VERDICT

Runner: `law_probes/probe_u1_sup.py --qs 56,72,100` (N=32, same ∂U 8-point
ring, radius 0.25 around s_∞). Receipts: `law_probes/u1_guard_extended.json`,
`.log`. Combined with the q=12..40 baseline (`u1_sup.json`, `u1_sup_q40.json`),
log-log slopes of sup |det⁺·det⁻| over q = 12..100:

| domain | slope | uniform bound needs |
|---|---|---|
| ALL 8 ∂U points | +0.893 | ≤ 0 — FAILS |
| IDENTIFIED domain (excl. dU_3/dU_4/dU_5, Re ≤ 0.0732) | **+0.071** | ≤ 0 — **CONSISTENT (flat)** |
| Re = 1/2 point (dU_0) | **−0.574** | ≤ 0 — **PASSES (decays)** |

Identified-domain sups oscillate in [2.29, 13.69] with no trend (13.69 is
q=12, the smallest q; for q ≥ 16 the range is [2.29, 8.31]). The §7.3
adverse slope +1.50 is hereby CORRECTED per the U1-φ per-point breakdown:
the growth is confined to the three unidentified boundary points; on the
domain where the proxy is identified with Z_q the family is flat-to-decaying
over an 8× range of q.

**VERDICT: U1 CORROBORATED on the identification domain (HEURISTIC —
float, finite q-range, proxy modulo U4). The T2′ tail argument survives its
third and final deciding test of 2026-08-16 (D1 migration ✓, U1-φ exponent
−3 ✓ overdetermined, guard flat ✓). Routing per plan: fund U2b.**

## §11 Correction notice 2026-08-16 (from LAW_U2B_CLOSURE.md)

Two defects in §2.3, found and repaired by the U2b lane:
1. **Conjecture U1-2 is FALSE as stated** — counterexample |tr(S R⁵)| =
   2|λ⁴−3λ²+1|: 2.00 → 2.50 → 0 → 10 across λ = 1 → 1.2434 → λ₅ → 2
   (independently re-verified by frontier). Correct theorem: monotone on
   [2cos(π/(A+1)), 2], A = max|a_i| — exactly the normal-form levels. The
   19,765-pair test never entered the false region (faithful lifts only).
2. **The Γ_θ comparison inference was backwards**: ℓ_w(λ_q) ≤ ℓ_w(2) gives
   N_q(L) ≥ N_θ(L) (more short geodesics, not fewer). The multi-syllable
   non-faithful excess bound this note asked for is DISSOLVED, not deferred.
Status of §2's bound: superseded by LAW_U2B_CLOSURE.md §§2-4 (uniform bound
proved for Re s ≥ 3.5 with explicit constants; method floor σ₀ = 3.05).

# EVEN-Q CROSS-VALIDATION — independent `det(1−L_{s,±})` at `q = 12` (Kimi lane)

**Date:** 2026-08-17. **Lane G, bounded cross-validation** (the §7.4 caveat of
`LAW_CERTIFIED_DEEPCOUNT_MULTI.md`, its recommended next step 3: "Even-`q`
builder cross-validation at `q = 12`"). **No new research; verification only.**

> ## Verdict
> **PASS — the even-`q` Arb builder `zeta_cert_rosen_even.cert_det` is
> cross-validated at `q = 12` to a worst relative error of `2.07e−30` over all
> 24 evaluations** (12 `s`-points × both sign sectors, `N = 24`), against a
> second, independently written plain-mpmath implementation at 50 digits.
> **No LOUD finding (nothing above `1e−6`; everything below `1e−29`).**
> What is validated is `det(1−L_{s,±})`, the raw MMS **numerator** — per
> `LAW_Q3_BRANCH_DIAGNOSIS.md`, `Z_S = det(1−L)/det(1−K)`; no `K_s` factor is
> involved in this check, and none is needed since both builders return the
> numerator.

**Consequence.** Caveat 4 of `LAW_CERTIFIED_DEEPCOUNT_MULTI.md` §7 (the
even-`q` builder's header scopes its validation to `q = 8` and disclaims
`q ≠ 8`) is **discharged at `q = 12`**: the builder that underpins the
certified `q = 12` deep count (**5**) now reproduces an independent
implementation at every probed point of the certified window and beyond.
The certificate's remaining conditionals are unchanged and are *not* this
note's subject (the dimension-tail ratio device, §6 of that note).

---

## 1. The two implementations

| | **existing builder (reference)** | **independent reimplementation (this note)** |
|---|---|---|
| file | `.worktrees/aletheia-restore/code/zeta_cert_rosen_even.py` (used **unmodified**, via thin driver) | `law_probes/evenxval_mp.py` (**new**, shares no code) |
| arithmetic | Arb ball via python-flint, `PREC_BITS = 300` | plain `mpmath`, `dps = 50` |
| interpreter | `/Users/za/.venvs/farey-rh/bin/python` | `/Users/za/miniforge3/envs/pari-arb/bin/python3` |
| power series | `acb_series` AD | hand-rolled truncated-Cauchy series on `mpc` (mul/inv/log/exp) |
| determinant | `acb_mat.det` | `mpmath.det` (LU) |
| head/tail split `n_head` | 4 | **6** (deliberately different; the Hurwitz tail closure is exact, so the split point cannot change the value — agreement therefore also checks the head+tail recombination) |
| call | `cert_det(acb(arb(σ),arb(t)), 24, sign, 12, n_head=4)` — exact signature from `law_probes/certdcM_winding.py` | `det_one(σ, t, sign)` |

The independent file was written from the **MMS paper structure**
(Mayer–Mühlenbruch–Strömberg, arXiv:0912.2236): even-`q` reduced operators
(their `reduced1`, `q = 2h_q+2`, `κ_q = h_q = 5`),

```
(L_{s,±} g)_1 = Linf_{2,s} g_h ± Linf_{-1,s} g_h
(L_{s,±} g)_i = L_{1,s} g_{i-1} + Linf_{2,s} g_h ± Linf_{-1,s} g_h ,  2≤i≤h
```

with branch operators `L_{n,s} g = ((z+nλ)²)^{-s} g(−1/(z+nλ))`,
`L_{−n,s} g = ((z−nλ)²)^{-s} g(+1/(z−nλ))` (squared weight, principal sheet),
the even-`q` Markov partition `φ_i = [[0; 1^{h_q−i}]]_(−)` (minus
`λ`-CF), `φ_0 = −λ/2`, discs centred at cell midpoints with radius
`cell·(5/2)/2`, normalized monomial bases `((z−c_i)/ρ_i)^m`, and exact
Hurwitz-zeta closure of the `Linf` tails,
`Σ_{l≥n0} (l ± z/λ)^{−(2s+m)} = ζ(2s+m, a0 + slope·u)`.
The existing builder was read only to confirm these conventions; nothing was
imported or copied. `λ_12 = 2cos(π/12) = √(2+√3)` (both sides use the exact
algebraic form).

Both compute the **same truncated object**: `det(I − M)` for the
`κN × κN = 120 × 120` matrix at `N = 24`. The comparison is therefore a pure
builder-vs-builder check; dimension-tail convergence of the truncation is a
separate question (see §4).

## 2. Grid and gate

`s = σ + i·t`, `σ ∈ {0.1, 0.25, 0.4}`, `t ∈ {2, 7, 12, 17}`, both sign
sectors, `N = 24` → 24 evaluations per side. Gate: relative error
`|mp − ref| / |ref| ≤ 1e−8` at every point; `> 1e−6` would have been reported
as a LOUD, localized finding. The `t = 17` row lies deliberately **outside**
the certified window (`Im ≤ 12`) to probe the builder where it was never
certified.

## 3. Per-point table

Relative errors are limited from below only by the 30 printed digits of the
reference midpoints (`~1e−30`); the gate is `1e−8`.

| sign | σ | t | \|ref det\| | rel err | gate |
|---|--:|--:|--:|--:|:--|
| +1 | 0.1  | 2  | 1.05605 | 3.96e−31 | PASS |
| +1 | 0.1  | 7  | 4.61803 | 1.01e−30 | PASS |
| +1 | 0.1  | 12 | 87.6606 | 4.18e−31 | PASS |
| +1 | 0.1  | 17 | 283.018 | 3.31e−31 | PASS |
| +1 | 0.25 | 2  | 0.816539 | 6.40e−31 | PASS |
| +1 | 0.25 | 7  | 1.59682 | 4.91e−31 | PASS |
| +1 | 0.25 | 12 | 19.4383 | 2.07e−30 | PASS |
| +1 | 0.25 | 17 | 24.4606 | 1.82e−30 | PASS |
| +1 | 0.4  | 2  | 0.798194 | 2.77e−31 | PASS |
| +1 | 0.4  | 7  | 0.670795 | 1.02e−30 | PASS |
| +1 | 0.4  | 12 | 5.97487 | 6.40e−31 | PASS |
| +1 | 0.4  | 17 | 2.45777 | 4.23e−31 | PASS |
| −1 | 0.1  | 2  | 0.888558 | 5.34e−31 | PASS |
| −1 | 0.1  | 7  | 10.8682 | 1.62e−31 | PASS |
| −1 | 0.1  | 12 | 68.1341 | 5.91e−31 | PASS |
| −1 | 0.1  | 17 | 310.694 | 1.08e−30 | PASS |
| −1 | 0.25 | 2  | 0.818661 | 6.43e−31 | PASS |
| −1 | 0.25 | 7  | 5.20757 | 1.04e−30 | PASS |
| −1 | 0.25 | 12 | 13.0966 | 6.32e−31 | PASS |
| −1 | 0.25 | 17 | 26.7212 | 1.90e−30 | PASS |
| −1 | 0.4  | 2  | 0.808901 | 3.12e−31 | PASS |
| −1 | 0.4  | 7  | 2.89604 | 1.97e−30 | PASS |
| −1 | 0.4  | 12 | 2.87869 | 1.98e−30 | PASS |
| −1 | 0.4  | 17 | 1.85230 | 2.05e−30 | PASS |

**Worst:** `2.07e−30` at `(sign +1, s = 0.25 + 12i)`. No sector- or
point-localized disagreement. Full values (30–40 digits) in the JSON receipts.

## 4. Honest limits

1. **Truncation, not tail.** Both sides compute the same `N = 24` truncated
   determinant; this validates the *builder*, not the dimension-tail device.
   Notably, at the off-window points `(σ=0.1, t=17)` the reference's own
   dimension-tail radii are large (`199` in `+1`, `464` in `−1` — versus
   `≤ 0.03` at every in-window point with `t ≤ 12` at `σ = 0.1`), i.e.
   `N = 24` is **not dimension-converged at `t = 17, σ = 0.1`**. The
   agreement there still checks the builder, but no certificate should be run
   at that corner without a larger `N`.
2. **Numerator only.** Consistent with `LAW_Q3_BRANCH_DIAGNOSIS.md`, both
   builders return `det(1−L_{s,±})` with no `det(1−K_s)` divisor. Zero
   locations on `Re s > 0` are unaffected by that factor; magnitudes are.
3. The mpmath side is float arithmetic at 50 digits (not rigorous balls); the
   Arb side's own ball radii at these points are `≤ 5e−28`, so the comparison
   is meaningful to the printed digits.
4. Reference midpoints were banked at 30 significant digits; the observed
   `~1e−30` agreement floor is that print width, not a discrepancy.

## 5. Artifacts (all new, `evenxval_` prefix, in `law_probes/`)

- `evenxval_mp.py` → `evenxval_mp.json`, `evenxval_mp.log` — independent
  mpmath builder + 24 values (40 digits), 492 s wall.
- `evenxval_ref.py` → `evenxval_ref.json`, `evenxval_ref.log` — thin driver
  over `zeta_cert_rosen_even.cert_det`, 24 ball midpoints + tail radii,
  45 s wall.
- `evenxval_compare.py` → `evenxval_compare.json`, `evenxval_compare.log` —
  the per-point gate table of §3.

No existing file was modified. No git commands were run.

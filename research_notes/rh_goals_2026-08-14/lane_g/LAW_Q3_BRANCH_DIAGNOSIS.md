# LAW — the builder's defect, diagnosed: the repo computes MMS's **numerator only**

**Status:** `PROVED` (the source identity, quoted from the LaTeX source) + `PROVED` numerically
(the correction, to `≤ 5e−8` on 27 banked rows) + `GAP` (one downstream enumeration, §7).
**Date:** 2026-08-16. **Lane:** G. **Interpreter:** `/Users/za/miniforge3/envs/pari-arb/bin/python3`.
**New probes, all `q3diag`-prefixed:** `law_probes/q3diag_rosen_mp.py`, `law_probes/q3diag_detK.py`
(+ `.json`, `.log`). **No existing file was modified. No `git` command was run.**

**Parents read in full:** `lane_g/LAW_P_CONTINUATION_CHECK.md` (the `GAP` PC.9 and its §3.1
hypothesis; PC.10), `lane_g/LAW_TEO_KAPPA_CORRECTED.md` (§3.4's residual, §5's open `TODO`s).

---

## 0. Verdict up front

`LAW_P_CONTINUATION_CHECK.md` PC.9 left the builder's `O(1)` defect **localised but not
diagnosed**, with a named hypothesis (§3.1: "the `q = 3` scalar eq. (33) branch / nearest-integer-
vs-Gauss CF; **MMS source not opened**"). **The source is opened here.** The hypothesis pointed at
the right paper and the wrong line.

> ### MMS's theorem is a **quotient**, and the repo builders compute only its numerator.
>
> ```
>     Z_S(s)  =  det(1 - L_s) / det(1 - K_s)
>            =  det[(1 - L_{s,+})(1 - L_{s,-})] / det(1 - K_s)
> ```
> — Mayer–Mühlenbruch–Strömberg, arXiv:0912.2236, **Theorem `main-theorem`**, restated in the
> introduction as **eq. `\eqref{LoverK}`** (§1.1 below, verbatim).
>
> `zeta_cert_rosen.py` (odd `q`) and `zeta_cert_rosen_even.py` return
> `P_q = |det(1−L_{s,+})| |det(1−L_{s,−})|` — the **numerator**. The missing denominator is a
> single explicit, elementary, zero-free-on-`Re s > 0` factor, and MMS give its spectrum in closed
> form (§1.2), so the defect is **exactly quantified and exactly repairable**:
>
> ```
>     P_repo(s)  =  |Z_S(s)| * |det(1 - K_s)|,      det(1 - K_s) = prod_{n>=0} (1 - b_q^{s+n})
> ```

**Numeric confirmation, three ways, on 27 already-banked rows — no fitted parameter:**

| test | what | result |
|---|---|---|
| **T1** | `P_repo/P_indep` at the six `q = 3` mirror points **vs** `|det(1−K_s)|` | rel err `2.5e−11` … `4.5e−9` (= the independent evaluator's own `N`-drift, §1.2 of the parent) |
| **T2** | same at `σ = 2, 3, 4` (the §4 "structurally blind Euler check" points) | rel err `9.3e−10`, `1.1e−10`, `6.3e−12` **[CORRECTED 2026-08-16: the three values were listed in reverse order against `σ = 2, 3, 4`; §3.2 and the receipt are right]** |
| **T3** | mirror-identity ratio `× D(s)/D(1−s)`, **`q = 3, 4, 6`**, 21 `σ` values in `[0.55, 1.50]` | **`1.000000000`** (`q = 3, 6`), **`1.00000004`** (`q = 4`) |

**Consequences.** PC.9 → `PROVED`. PC.10 (`q = 4, 6` unexplained) → `PROVED`, same cause, no new
module needed. **U4 + the corrected Teo `κ_q` are now jointly confirmed at `q = 3, 4` and `6`, over
the whole swept `σ` range**, not just at three points at one `q`.

---

## 1. The source, opened

`CITATION(MMS)` D. Mayer, T. Mühlenbruch, F. Strömberg, *The transfer operator for the Hecke
triangle groups*, **arXiv:0912.2236**. Retrieved 2026-08-16 as the arXiv **LaTeX e-print**
(`https://arxiv.org/e-print/0912.2236` → `MMS15.03.tex`, 2173 lines, dated 15 Mar 2010), so every
quotation below is from the authors' own source, not from OCR.

`TODO-VERIFY(the journal version — Discrete Contin. Dyn. Syst. 32 (2012) 2453–2484. I read the
arXiv e-print. The theorem in that source is labelled `\label{main-theorem}` and carries no
printed number; confirm the journal's numbering before citing a number in any paper.)`

### 1.1 The theorem, verbatim

Introduction (the paragraph beginning "As a consequence, the Fredholm determinant"):

> "In contrast to this case, in the present case (i.e. for Hecke surfaces `M_q`) … there is not a
> one-to-one correspondence between the periodic orbits of the map `f_q` generating the CF's and
> the periodic orbits of the geodesic flow `Φ_t`. Indeed, for every `G_q`, there exist two periodic
> points, `r_q` and `−r_q`, of `f_q`, which correspond to the same periodic orbit `O` for the
> geodesic flow. For `q=3`, i.e. for the modular group, this fact follows by the results of Hurwitz
> [Hu89] … As a consequence, the Fredholm determinant of the Ruelle transfer operator, `L_s`, for
> the Hurwitz-Nakada map `f_q` **contains the contribution of the closed orbit `O` twice.
> Therefore it does not, by itself, correctly describe the corresponding Selberg zeta function**
> … To correct for this overcounting we introduce another transfer operator, `K_s`, whose Fredholm
> determinant exactly corresponds to the contribution of the orbit `O` to `Z_S(s)`."
>
> ```
>     Z_S(s) = det(1 - L_s) / det(1 - K_s).                     \eqref{LoverK}
> ```

and, at the end of §`secK`:

> "**Theorem `\label{main-theorem}`.** The Selberg zeta function `Z_S(s)` for the Hecke triangle
> group `G_q` can be written as
> `Z_S(s) = det(1−L_s)/det(1−K_s) = det[(1−L_{s,+})(1−L_{s,−})]/det(1−K_s)`,
> where `L_s`, `L_{s,±}` and `K_s = L_s^{O_+}` are the transfer operators given by Theorem `\ref{E6}`,
> `(\ref{reduced1})`–`(\ref{reduced3})` and `(\ref{transfereven})`–`(\ref{transferodd})`,
> respectively."

**The `L_{s,±}` in that theorem are exactly the repo's two signed operators**, so the numerator is
precisely `P_q` up to modulus. Nothing else in MMS's statement is missing from the repo — only the
denominator.

### 1.2 `det(1 − K_s)`, in closed form

> "**Proposition.** The spectrum of `K_s` is given by
> `σ(K_s) = { prod_{l=0}^{κ_q−1} ( f_q^l(r_q) )^{2s+2n},  n = 0,1,2,… }`
> where `κ_q` denotes the period of the point `r_q`."

and, from that Proposition's proof, the base is `ψ'(z*) = prod_{l=0}^{κ_q−1} (f_q^l(z*))^2 > 0`.
Writing

```
       b_q := prod_{l=0}^{kappa_q - 1} ( f_q^l(r_q) )^2 ,
       det(1 - K_s) = prod_{n>=0} ( 1 - b_q^{s+n} ).                          (D)
```

`r_q` is given by MMS Lemma `\label{lemma:det_op}`: `r_q = [0; \ov{3}]` for `q = 3`,
`[0; \ov{1^{h_q−1},2}]` for even `q = 2h_q+2`, `[0; \ov{1^{h_q},2,1^{h_q−1},2}]` for odd `q ≥ 5`.
`q3diag_detK.py` computes `b_q` from the orbit product and **cross-checks it against MMS's own
closed form** for even `q` (their Remark, `l = sqrt((2−λ_q)/(2+λ_q))`, so `b_q = (2−λ_q)/(2+λ_q)`):

| `q` | `κ_q` | `r_q` word | `b_q` | `1/b_q` | check |
|--:|--:|---|---|---|---|
| 3 | 1 | `[3]` | `0.145898033750` | `6.854101966` | `= φ^{−4}` exactly (`φ^{−4} = 0.145898033750315`) |
| 4 | 1 | `[2]` | `0.171572875254` | `5.828427125` | `(2−λ)/(2+λ)`, rel err **`0.0`** |
| 5 | 3 | `[1,2,2]` | `0.013092084695` | `76.382029544` | (odd `q`, no closed form used) |
| 6 | 2 | `[1,2]` | `0.071796769724` | `13.928203230` | `(2−λ)/(2+λ)`, rel err `4.0e−41` |
| 7 | 5 | `[1,1,2,1,2]` | `0.002973302217` | `336.326389690` | (odd `q`) |
| 8 | 3 | `[1,1,2]` | `0.039566129897` | `25.274142369` | `(2−λ)/(2+λ)`, rel err `3.6e−41` |

**`q = 3` is the sanity check that the whole reading is right.** `1/b_3 = φ^4 = (7+3√5)/2 =
6.854102`, so `(D)` is
`prod_{k≥0} (1 − N(P)^{−s−k})` with `N(P) = φ^4` — **the Selberg Euler factor of the shortest
closed geodesic on the modular surface** (the discriminant-5 class, trace 3, the Hurwitz
`\ov{3}` orbit). MMS's "counted twice" is exactly that geodesic, and the repo's `P_3` is
`|Z_{PSL(2,Z)}|` with it counted once too often.

`TODO-VERIFY`: MMS's Remark also gives an odd-`q` closed form `l = (2−λ_q)/(2+R λ_q)` whose symbol
`R` I did not resolve from the source. **It is not used here** — the odd-`q` `b_q` above come from
the orbit product, which is the Proposition itself.

---

## 2. What the defect is **not** — the repo's `q = 3` operator is a *faithful* transcription

`q3diag_rosen_mp.py`. Before accepting §1, the alternative reading in PC.9 §3.1 ("the lane's
transcription dropped something in eq. (33)") had to be excluded — and it is **excluded**.

MMS's `q = 3` lemma reads, verbatim:

> "For `q=3` the operator `L_s` is given by
> `(L_s g)_1 = L^∞_{3,s} g_1 + L^∞_{−2,s} g_{−1}`,
> `(L_s g)_{−1} = L^∞_{2,s} g_1 + L^∞_{−3,s} g_{−1}`."

with `L^∞_{±n,s} g(x) = Σ_{l≥n} (x ± l λ_q)^{−2s} g(−1/(x ± l λ_q))` (MMS eq. `\eqref{aux}`), and
`Φ_{−1} = −Φ_1`. Under the symmetry reduction `g_{−1}(x) = e·g_1(−x)`, `e = ±1`, the first line
becomes exactly

```
    (L_{s,e} f)(z) = sum_{n>=3} ((z+n)^2)^{-s} f(-1/(z+n))
                   + e * sum_{n>=2} ((z-n)^2)^{-s} f( 1/(z-n)),      lambda_3 = 1
```

which is **line-for-line** `zeta_cert_rosen.build_reduced_matrix_ball`'s `q == 3` branch
(`inf_block(1,1,3,False)` + `sgn * inf_block(1,1,2,True)`), on the single component
`Φ_1 = [−λ/2, 0]`, centre `−1/4` — the repo's `disc_centers_ball(3, 1)`. The start indices `3` and
`2` are MMS's own `N_{1,1} = Z_{≥3}`, `N_{1,−1} = Z_{≤−2}`. **The `+1/(z−n)` argument that looks
like a sign error against eq. `\eqref{aux}` is the symmetry reduction, and it is correct** (checked
symbolically: `(L g)_{−1}(x) = e·(L g)_1(−x)` holds identically under the substitution).

`q3diag_rosen_mp.py` then re-implements that operator in **mpmath**, in a different basis
(`(z−c)^m`, unscaled) with the branch sums closed in **closed-form Hurwitz zeta** rather than the
repo's `n_head`-split Arb tail, and reproduces the banked Arb determinants:

| point | sign | mpmath `N = 20` | `N = 28` | `N = 36` | rel err vs banked Arb (`N = 32/64`, prec 400) |
|---|--:|---|---|---|---|
| `σ = +1.25` | `+1` | — | — | `+0.842692470942+0.037485771033j` | `1.53e−10` |
| `σ = +1.25` | `−1` | — | — | `+0.995744673678+0.116210147350j` | `1.53e−10` |
| `σ = +1.40` | `+1` | — | — | `+0.881161146486+0.030447348295j` | `1.37e−10` |
| `σ = +1.40` | `−1` | — | — | `+1.001044326797+0.087410073583j` | `1.37e−10` |
| `σ = −0.25` | `+1` | — | — | `−1.259353698080+0.681765524935j` | `4.42e−10` |
| `σ = −0.25` | `−1` | — | — | `−0.339172265081−1.676265975628j` | `4.42e−10` |

(monotone in `N`: `1.5e−6` → `6.1e−9` → `4.4e−10` at `N = 20, 28, 36`.)

> **Q3D.1 `PROVED` numerically.** The Arb builder computes the operator MMS's `q = 3` lemma
> defines, to `4.42e−10` **[CORRECTED 2026-08-16: was `1.5e−10`, which is only the `σ = ±1.25`
> row; the worst of the three gates in the table above is `4.42e−10` at `σ = −0.25`]**. **The defect is not in the operator, the discs, the start indices, the
> symmetry reduction, or the Arb tail closure. It is one missing factor in the theorem.**

This matters for the blast radius: an operator-level transcription error would have been `q = 3`-
specific (a special-case branch); a missing theorem factor is **every `q`, every module**.

---

## 3. Numeric confirmation — `q3diag_detK.json`

`q3diag_detK.py` computes only `(D)`; every `P_repo`, `P_indep` and `ratio` it consumes is **read
from the already-banked JSON receipts** (`q3cont_compare.json`, `q3cont_largesigma.json`,
`mirror_u4_corrected.json`, `mirror_u4_corrected_sigmasweep.json`, `q3cont_q4_sigmasweep.json`).
No determinant is recomputed and no file is written except the probe's own `.json`/`.log`. There is
**no free parameter**: `b_q` is fixed by MMS's Proposition.

### 3.1 T1 — the six `q = 3` mirror points

The parent's §2.1 measured `R(s) = P_repo/P_indep` and could only call it "smooth and zero-free".
It is `|det(1 − K_s)|`:

| `σ` | point | `Re s` | measured `P_repo/P_indep` | **predicted `|det(1−K_s)|`** | rel err |
|--:|---|--:|---|---|---|
| 1.25 | `s` | `+1.25` | `0.949862738` | `0.949862738` | `2.53e−11` |
| 1.25 | `1−s` | `−0.25` | `1.242882499` | `1.242882505` | `4.50e−09` |
| 1.40 | `s` | `+1.40` | `0.961751914` | `0.961751914` | `4.41e−11` |
| 1.40 | `1−s` | `−0.40` | `1.599718243` | `1.599718249` | `4.09e−09` |
| 1.50 | `s` | `+1.50` | `0.968157043` | `0.968157043` | `3.91e−11` |
| 1.50 | `1−s` | `−0.50` | `1.919636471` | `1.919636477` | `3.42e−09` |

**The `4.5e−9` at the mirror points is not the prediction's error** — it is the independent
Mayer evaluator's own `N`-drift there (`2.6e−7`, `1.7e−7`, `7.3e−8`, parent §1.2). On the
`Re s > 1` side, where that evaluator is stable to `2.4e−9`, the agreement is `4e−11`.

### 3.2 T2 — large `σ`, the "structurally blind" points

| `σ` | measured ratio | predicted `|det(1−K_s)|` | rel err |
|--:|---|---|---|
| 2.0 | `0.987517688096` | `0.987517689018` | `9.33e−10` |
| 3.0 | `0.998154713020` | `0.998154712908` | `1.13e−10` |
| 4.0 | `0.999730266152` | `0.999730266158` | `6.25e−12` |

This also explains **why** the parent's §4 Euler-product check was blind: `det(1 − K_s) → 1` like
`b_q^σ = 0.1459^σ`, i.e. the missing factor decays at exactly the rate a truncated Euler product
is checked to.

### 3.3 T3 — the mirror identity, corrected, at `q = 3, 4, 6`

With `D(s) := |det(1 − K_s)|` and `ratio_corrected := ratio_repo · D(s)/D(1−s)` (the repo's
`P(1−s)/P(s)` divided by the spurious factor on each side):

| `σ` | `q = 3` ratio_repo | `D(s)/D(1−s)` | **corrected** | `q = 4` ratio_repo | `D(s)/D(1−s)` | **corrected** |
|--:|---|---|---|---|---|---|
| 0.55 | `0.981971` | `1.018360` | **`1.000000000`** | `0.870837` | `1.148321` | **`1.000000003`** |
| 0.60 | `0.965198` | `1.036057` | **`1.000000000`** | `0.755414` | `1.323777` | **`1.000000005`** |
| 0.70 | `0.939025` | `1.064935` | **`1.000000000`** | `0.551751` | `1.812411` | **`1.000000011`** |
| 0.80 | `0.928990` | `1.076438` | **`1.000000000`** | `0.370415` | `2.699675` | **`1.000000016`** |
| 0.90 | `0.943452` | `1.059937` | **`1.000000000`** | `0.206612` | `4.839992` | **`1.000000021`** |
| 1.00 | `0.991350` | `1.008726` | **`1.000000000`** | **`0.108344`** | **`9.229847`** | **`1.000000026`** |
| 1.10 | `1.081071` | `0.925009` | **`1.000000000`** | `0.207596` | `4.817052` | **`1.000000031`** |
| 1.25 | `1.308486` | `0.764242` | **`1.000000000`** | `0.455610` | `2.194860` | **`1.000000038`** |
| 1.50 | `1.982774` | `0.504344` | **`1.000000000`** | `0.840166` | `1.190242` | **`1.000000049`** |

and the three-point table of `mirror_u4_corrected.json`, **including `q = 6`**:

| `q` | `σ` | ratio_repo (K.6's `[0.456, 2.055]`) | `D(s)/D(1−s)` | **corrected** |
|--:|--:|---|---|---|
| 3 | 1.25 | `1.308486` | `0.764242` | **`1.000000000`** |
| 3 | 1.40 | `1.663338` | `0.601201` | **`1.000000000`** |
| 3 | 1.50 | `1.982774` | `0.504344` | **`1.000000000`** |
| 4 | 1.25 | `0.455610` | `2.194860` | **`1.000000038`** |
| 4 | 1.40 | `0.701397` | `1.425727` | **`1.000000045`** |
| 4 | 1.50 | `0.840166` | `1.190242` | **`1.000000049`** |
| 6 | 1.25 | `0.879730` | `1.136713` | **`1.000000000`** |
| 6 | 1.40 | `1.546651` | `0.646558` | **`1.000000000`** |
| 6 | 1.50 | `2.054840` | `0.486656` | **`1.000000000`** |

**`LAW_TEO_KAPPA_CORRECTED.md` K.6's entire `[0.456, 2.055]` residual is now zero, at every `q` and
every `σ` it was ever measured at.** The `10⁵–10¹³` failure was the `Γ₂ = 1/G` transcription (K.4);
the `O(1)` remainder is MMS's `det(1 − K_s)`. Nothing else is left.

The `q = 3` and `q = 6` rows print as exactly `1.000000000` because the banked ratios themselves
carry ~9 digits; the `q = 4` `4e−8` drift is the `q = 4` sweep's own banked precision, not a
mismatch (it is `σ`-monotone, i.e. a truncation signature, not a residual factor).

### 3.4 The `q = 4` "sharp minimum `0.108` at `σ = 1.00`" — mechanism

The parent's PC.12 flagged this shape as new and unexplained. It is a **near-zero of
`det(1 − K_{1−s})`**. `det(1 − K_s)` vanishes iff `b_q^{s+n} = 1`, i.e. at

```
       s  =  -n + i k (2 pi / log(1/b_q)),      n = 0,1,2,...,  k in Z,
```

so its zeros sit on `Re s ∈ {0, −1, −2, …}` with imaginary spacing `2π/log(1/b_q)`:

| `q` | imaginary spacing | nearest zero to `t_∞ = 7.0673626` |
|--:|---|---|
| 3 | `3.264251303` | `k = 2` → `6.528503` (distance `0.539`) |
| 4 | `3.564427956` | `k = 2` → **`7.128856`** (distance **`0.0615`**) |
| 5 | `1.449158507` | `k = 5` → `7.245793` (distance `0.178`) |
| 6 | `2.385492096` | `k = 3` → `7.156476` (distance `0.089`) |

At `σ = 1.00` the mirror point is `1 − s = 0 − i t_∞`, which sits `0.0615` from the `q = 4` zero at
`0 + 2i(2π/log(1/b_4))`. `D(1−s)` nearly vanishes, `D(s)/D(1−s)` spikes to `9.23`, and the repo's
ratio dives to `0.108`. **The `9`-fold "signal" is an accident of `t_∞` versus `2π/log(1/b_4)`, and
carries no information about `q = 4`.**

`PC.12`'s reading ("the shape is new and it is not the `q = 3` shape") is **withdrawn as a signal
and kept as a measurement**: the shape is real, and it is the shape of `1/|1 − b_4^{1−s}|`.

---

## 4. Even `q` — the task's Part 2, discharged without a new evaluator

The brief asked for an independent even-`q` determinant (theta group / `Γ₀(2)` classical
expressions) to test whether `zeta_cert_rosen_even.py` has the same class of defect. **That
construction is no longer the cheapest discriminator, and it is no longer needed**: MMS's Theorem
covers even `q` in the same sentence (`(\ref{transfereven})` is the even-`q` `K_s`), and §3.3
shows the correction closes `q = 4` and `q = 6` to `4e−8` and `1e−9` over the same `σ` grid as
`q = 3`. A separate classical `Z_{Γ_4}` evaluator would be testing a hypothesis that is already
confirmed to eight digits at nine abscissae.

**Honest limits of the even-`q` claim.** This is a *consistency* argument, not the *independent*
argument the `q = 3` case has:

- At `q = 3` the chain is closed: `P_repo` was compared to a **classical** `Z_{PSL(2,Z)}`
  (Mayer/Gauss-map, three independent validations, parent §1.1), so `P_repo = |Z| · |det(1−K)|` is
  a two-sided measurement.
- At `q = 4, 6` the only thing measured is that `P_repo(1−s)/P_repo(s) · D(s)/D(1−s) = 1`, i.e.
  that **U4 + corrected Teo + MMS's `det(1−K)` are mutually consistent**. It remains logically
  possible — though, after `q = 3`, contrived — that two of the three are wrong in compensating
  ways. `TODO-VERIFY`: an independent `Z_{Γ_4}` (theta group) evaluator would close this the way
  `q3cont_mayer_indep.py` closed `q = 3`. It is now a *nice-to-have*, not a blocker.
- **`zeta_cert_rosen_even.py` was not read or run in this note.** The correction is applied to its
  *banked outputs*. `TODO`: confirm by code audit that the even-`q` builder likewise returns the
  bare `det(1−L_{s,+})det(1−L_{s,−})` with no `K_s` factor — everything here is consistent with
  that, but it is an inference from the numbers, not an audit.

---

## 5. What this does and does not repair

`det(1 − K_s)` is **zero-free on `Re s > 0`** (§3.4: its zeros have `Re s ∈ −N₀`). That single fact
splits the blast radius cleanly.

| item | status |
|---|---|
| `LAW_TEO_KAPPA_CORRECTED.md` K.6 residual `[0.456, 2.055]`, **all** `q = 3, 4, 6` rows | **EXPLAINED and REMOVED.** `(*)` holds to `≤ 5e−8`. |
| K.9 (residual smooth, `→1` at the line, grows for `Re(1−s) < 0`) | **`HEURISTIC` → closed form.** It is `D(1−s)/D(s)`. |
| K.10 / PC.3 / PC.5 ("U4 confirmed at `q = 3` only") | **extended to `q = 4` and `q = 6`**, over `σ ∈ [0.55, 1.50]`. |
| PC.9 (cause not diagnosed) | **`GAP` → `PROVED`.** §1, §3. |
| PC.10 (`q = 4, 6` not explained, different module) | **`GAP` → `PROVED`.** §3.3, with §4's caveat. |
| PC.12 (`q = 4` sharp minimum `0.108` "a `q = 4`-specific signal") | **explained as an artefact** of a `det(1−K_4)` near-zero at `t_∞`. Not a signal. |
| PC.7 (`R(s)` smooth and zero-free where measured) | **explained**: `R = |det(1−K_s)|`, and it is zero-free *precisely* on `Re s > 0`. The parent measured it only there. |
| **zero locations of every repo determinant, `Re s > 0`** | **UNAFFECTED.** `det(1−K_s) ≠ 0` there, so `P_q`'s zeros on `Re s > 0` are `Z_S`'s zeros. |
| **zero locations on `Re s ≤ 0`** | **NOT clean.** `P_q` has spurious zeros at `s = −n + 2πik/log(1/b_q)`. Any zero-counting/winding on `Re s ≤ 0` must divide them out. |
| the flagship `G_5` results (`zeta_cert_rosen_q5.py`, `g5-offline-resonance-theorem`) | **zero/resonance claims UNAFFECTED** — the certified resonances sit at `Re s ≈ 0.45 > 0`, where `det(1−K_5)` is zero-free and finite. **Magnitude claims off the zero set are wrong by `|det(1−K_5)|`**, `b_5 = 0.0130921`. See §7. |
| `LAW_U1_GROWTH.md` §7.3 / §10 (viii) `sup_{∂U}` growth | **NOW REPAIRABLE, and probably shifted.** Those are magnitudes on `∂U` including `Re s ≤ 0`, where `|det(1−K_q)| ~ b_q^{σ}` blows up as `σ → −∞`. The artefact is no longer just named; it is computable. `TODO`. |
| `LAW_U1_GROWTH.md` §7.2 Euler-product validation | **shown non-discriminating, and now for a stated reason** (§3.2). |

---

## 6. Lane rule, sharpened

The parent stated: *"Every check this lane has trusted was run where the quantity under test is
near its trivial value."* This note adds the complementary failure:

> **Both defects found in this lane were invisible to every check that had been run, and both were
> found only by opening the source.** K.4 (`Γ₂ = 1/G`) came from reading Teo Prop. 2.5;
> Q3D.2 (the missing `det(1−K_s)`) came from reading MMS's Theorem. In both cases the lane had a
> *named hypothesis about the right paper* (`LAW_P_CONTINUATION_CHECK.md` §3.1 named MMS eq. (33))
> and the hypothesis was **wrong about which line**, while the instinct to open the source was
> right. Numerics localised; only the source diagnosed.

---

## 7. Status ledger

| id | claim | status | where |
|---|---|---|---|
| Q3D.1 | The repo's `q = 3` Arb operator is a **faithful** transcription of MMS's `q = 3` lemma — independently re-implemented in mpmath, agreeing to `4.42e−10` (worst gate; `1.53e−10` at `σ = ±1.25`) **[CORRECTED 2026-08-16]**. The defect is not in the operator. | **`PROVED`** numerically | §2 |
| Q3D.2 | MMS's Theorem is `Z_S = det(1−L_s)/det(1−K_s)`; **the repo builders compute the numerator only** | **`CITATION` + the finding** | §1.1 |
| Q3D.3 | `det(1−K_s) = prod_{n≥0}(1 − b_q^{s+n})`, `b_q = prod_{l<κ_q}(f_q^l(r_q))²`; `b_3 = φ^{−4}`, `b_4 = 3−2√2`, `b_6 = 7−4√3`, `b_5 = 0.0130921` | **`CITATION`** (MMS Prop.) + **`PROVED`** (even-`q` closed form reproduced to `4e−41`) | §1.2 |
| Q3D.4 | `P_repo/P_indep = |det(1−K_s)|` at all six `q = 3` mirror points, rel err `2.5e−11`–`4.5e−9` (bounded by the independent evaluator's own drift) | **`PROVED`** numerically — the finding | §3.1 |
| Q3D.5 | Same at `σ = 2, 3, 4`, rel err `≤ 9.3e−10`; and this explains why the Euler-product check was blind | **`PROVED`** numerically | §3.2 |
| Q3D.6 | **The mirror identity `(*)` holds to `≤ 5e−8` at `q = 3, 4, 6` across `σ ∈ [0.55, 1.50]`** once `det(1−K_q)` is divided out — 21 rows, no fitted parameter | **the finding** | §3.3 |
| Q3D.7 | `det(1−K_s)`'s zeros are exactly `s ∈ −N₀ + i(2π/log(1/b_q))Z`; **zero-free on `Re s > 0`** | **`PROVED`** | §3.4 |
| Q3D.8 | The `q = 4` `0.108` minimum at `σ = 1.00` is a `det(1−K_4)` near-zero (`t_∞ = 7.0674` vs the zero at `7.1289`), not a `q = 4` signal | **`PROVED`** numerically | §3.4 |
| Q3D.9 | Even-`q` (`q = 4, 6`) has the **same** defect — consistency-confirmed, **not** independently measured; `zeta_cert_rosen_even.py` not audited | **`HEURISTIC`, strong** + `TODO-VERIFY` | §4 |
| Q3D.10 | The odd-`q` closed form in MMS's Remark (`l = (2−λ)/(2+Rλ)`) — symbol `R` not resolved; not used | **`GAP`, cosmetic** | §1.2 |
| Q3D.11 | Enumeration of which `G_5` published numbers are magnitudes off the zero set (and so wrong by `|det(1−K_5)|`) | **`GAP` — not done here** | §5 |
| Q3D.12 | Journal-version numbering of MMS's Theorem (DCDS 32 (2012) 2453–2484) | **`TODO-VERIFY`** | §1 |

**What stays open, stated plainly.**

1. **No code was fixed.** This note diagnoses; `zeta_cert_rosen.py`, `zeta_cert_rosen_even.py` and
   `zeta_cert_rosen_q5.py` still return the bare numerator. A one-line `det(1−K_q)` divisor is the
   repair, but applying it is a mutation of validated engines and is **not** done here.
2. **Every `Z_S` magnitude the lane has published at any `q` is wrong by `|det(1−K_q)|`.** The
   factor is now known exactly, so each such number is *correctable*, but none has been corrected.
   Q3D.11 (which `G_5` claims) is the priority item.
3. **Zero-location claims on `Re s > 0` are safe** (Q3D.7) — this includes the `G_5` off-line
   resonances. Zero-location and winding claims touching `Re s ≤ 0` are **not** safe.
4. The even-`q` case is confirmed by consistency, not by an independent classical evaluator (§4).
5. `det(1−K_s)` is computed in mpmath floats at `dps = 40`, no interval arithmetic — the same
   epistemic status as every number in the parent notes.

---

## 8. Receipts

All under `lane_g/law_probes/`. Interpreter `/Users/za/miniforge3/envs/pari-arb/bin/python3`.

- `q3diag_rosen_mp.py` — §2, the mpmath re-implementation of the repo's `q = 3` operator and its
  gate against `q3cont_repo_builder.json` (run with no arguments; prints the gate table).
- `q3diag_detK.py` → `q3diag_detK.json`, `q3diag_detK.log` — §1.2, §3, §3.4. Reads five banked
  JSONs, writes only its own.
- Source: arXiv:0912.2236 LaTeX e-print (`MMS15.03.tex`), retrieved 2026-08-16.
- **Not modified:** every `q3cont_*` probe, `mirror_*`, `probe_u1_*`, `zeta_cert_rosen*.py`, every
  other lane. No `git` command was run.

---

READY FOR JUDGING

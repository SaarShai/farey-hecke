# LAW — the `O(1)` mirror residual **is** the determinant builder, and `q = 3` U4 + corrected Teo hold

**Status:** `measured, clean` (the localisation) + `PROVED` numerically (the two identities it
confirms) + `GAP` (the builder's defect is localised but not diagnosed).
**Date:** 2026-08-16. **Lane:** G. **Interpreter:** `/Users/za/miniforge3/envs/pari-arb/bin/python3`.
**New probes, all `q3cont`-prefixed:** `law_probes/q3cont_mayer_indep.py`, `q3cont_repo_builder.py`,
`q3cont_compare.py`, `q3cont_nhead.py`, `q3cont_largesigma.py`, `q3cont_q4_sigmasweep.py` (+ `.json`,
`.log`). **No existing probe file was modified. No `git` command was run.**

**Parents read in full:** `lane_g/LAW_TEO_KAPPA_CORRECTED.md` (the `TODO-VERIFY` in §3.4 and the
open `TODO`s (3) and (4) in §5), `lane_g/LAW_MIRROR_Q3_DISCRIMINATOR.md` (the setup).

---

## 0. Verdict up front

`LAW_TEO_KAPPA_CORRECTED.md` §3.4 logged a `HEURISTIC` hypothesis and its own decisive test:

> *"the residual is most plausibly in the **mirror** evaluation — the determinant builder's
> continuation to `Re s ≤ 0` … `TODO-VERIFY`: this is a hypothesis about the evaluator, not a
> measurement of it; the decisive test is a `P_3` vs. classical `Z_{PSL(2,Z)}` comparison at a point
> with `Re s < 0`, which is not run here."*

**That test is run here. The hypothesis is confirmed, and more sharply than it was stated.**

> ### With the repo determinant proxy replaced by an **independent** classical Mayer determinant — and **nothing else changed**, the same corrected Teo kernel — the mirror identity
>
> ```
>       P_3(1-s) / P_3(s)   ==   |phi_3(s)| * |K_3(s)|                    (*)
> ```
>
> **holds to a printed `4.5e−9` at all three test points** (defensible bound `3e−7`, §1.2).
> The `O(1)` residual `1.308 / 1.663 / 1.983` is
> **entirely** an artefact of `zeta_cert_rosen.py`'s `q = 3` determinant.

| `σ` | ratio, **repo** `P_3` | ratio, **independent** `P_3` |
|--:|---|---|
| 1.25 | `1.308486` | **`1.000000005`** |
| 1.40 | `1.663338` | **`1.000000004`** |
| 1.50 | `1.982774` | **`1.000000003`** |

Three consequences, in order of importance:

1. **U4 at `q = 3` is numerically confirmed, jointly with the corrected Teo `κ_3`**, to at least
   `3e−7` (§1.2 explains why the printed `4.5e−9` is not the honest bound) — against a residual of
   `0.31`–`0.98`, six orders larger. It was a theorem (Mayer); it is now also a measurement, and the
   measurement is a *joint* confirmation: a wrong kernel could not agree with a right determinant at
   three independent abscissae.
2. **`LAW_TEO_KAPPA_CORRECTED.md`'s `Γ₂ = 1/G` correction is confirmed by an independent route.**
   K.6's `[0.456, 2.055]` was the last unexplained thing in that note; at `q = 3` it is now
   explained and it is not in the kernel.
3. **`zeta_cert_rosen.py`'s `q = 3` branch does not compute `Z_{PSL(2,Z)}`.** It differs from it by a
   smooth, zero-free `O(1)` factor — `≈ 0.95` at `Re s = 1.25`, `≈ 1.92` at `Re s = −0.5` — that is
   `N`-stable to `1e−16` and **exactly `n_head`-flat**. This is a `GAP`, not a diagnosis, and §5
   bounds what it does and does not touch.

---

## 1. The independent evaluator, and exactly what "independent" means

`q3cont_mayer_indep.py`. At `q = 3`, `G_3 = PSL(2,Z)` and U4 is **Mayer's theorem**:

```
      Z_{PSL(2,Z)}(s) = det(1 - L_s) det(1 + L_s),
      (L_s f)(z) = sum_{n>=1} (z+n)^{-2s} f(1/(z+n))                    on |z-1| < 3/2.
```

So `P_3` has a classical target and **both sides of the comparison are the same analytic object** —
there is no normalisation constant to guess and no convention to fix.

**Derived in the probe, so the continuation is explicit.** Writing `f(z) = Σ_m a_m (z−1)^m`,

```
   (L_s f)(z) = Σ_m a_m Σ_{j=0}^{m} C(m,j)(-1)^j  zeta(2s+m-j, z+1),
   M_{k,m}(s) = Σ_{r=0}^{m} C(m,r) (-1)^{m-r+k} C(2s+r+k-1, k) [ zeta(2s+r+k) - 1 ].
```

Every entry is a **finite** sum of Riemann zeta values at `2s + (integer)` times a Pochhammer
symbol. Both are meromorphic on all of `C`. **The continuation to `Re s ≤ 0` is carried entirely by
the classical `ζ`** — it is the standard Mayer continuation, and it uses none of the Rosen/MMS
engine's machinery.

**Shared with `zeta_cert_rosen.py`: nothing but the mathematics.**

| | repo builder | this probe |
|---|---|---|
| library | `flint` / Arb balls | `mpmath`, `dps = 60` |
| dynamics | Rosen/`λ`-CF, MMS eq. (33), interval `[−λ/2, 0]` | Gauss map, full branch, `[0,1]` |
| basis | `acb_series` about the MMS disc centres | Taylor at `z = 1` |
| continuation | "exact-Hurwitz branch-tail closure" + `n_head` split heads | closed-form `ζ(2s+integer)`, no split |
| determinant | `acb_mat.det` block routine | `mpmath` LU |
| imports | — | imports **no** repo module, **no** `lane_g` probe |

### 1.1 Three classical validations, run before any comparison

All three are properties of `Z_{PSL(2,Z)}` known independently of this repo.

| id | test | result (`N = 12 → 28`) |
|---|---|---|
| **V1** | `Z(1) = 0` (constant eigenfunction; `L_1` = Gauss–Kuzmin, eigenvalue `1`) | `det(1−L_1)`: `3.05e−5 → 1.48e−6 → 7.55e−8 → 3.99e−9 → 2.16e−10`. **Converging to `0`.** `det(1+L_1) → 1.492576148` |
| **V2** | `Z(ρ/2) = 0` at the first Riemann zero (scattering zeros from `φ_3 = ξ(2s−1)/ξ(2s)`) — **at the mirror test's own height**, since `t_∞ = 7.0673625708673465 = γ₁/2` | `\|det(1−L)\|`: `1.45e−2 → 3.11e−4 → 5.08e−6 → 7.37e−8 → 1.02e−9`. **Converging to `0`.** |
| **V3** | first **odd** Maass form, `r = 9.533695261352` | `\|det(1+L)\|`: `6.91e−1 → 4.67e−2 → 1.81e−3 → 5.28e−5 → 1.30e−6`. **Converging to `0`**, and in the correct (odd) factor: `\|det(1−L)\| → 1.8109`. |

`V2` is the sharpest: the evaluator reproduces a zero of `Z` that is fixed by `ζ`'s first zero, at
exactly the height used throughout this lane.

### 1.2 `N`-stability of the independent evaluator at the mirror points

`rel drift(N = 24 → 28)`: `2.4e−9`, `4.7e−9`, `4.8e−9` at `Re s = 1.25, 1.40, 1.50`;
`2.6e−7`, `1.7e−7`, `7.3e−8` at `Re s = −0.25, −0.40, −0.50`. **The `4.5e−9` agreement in §0 is smaller than the mirror points' own `N`-drift (`2.6e−7`), so it
must not be read as `9`-digit accuracy of either `P` separately** — the truncation error is largely
common to `P(s)` and `P(1−s)` and cancels in the ratio. The defensible statement is: **the identity
holds to at least `3e−7`, and the residual under test is `0.31` to `0.98` — six orders larger.**
That is the whole claim; the extra digits are reported only because they are what the run printed.

---

## 2. The measurement — `q3cont_compare.json`

`q3cont_repo_builder.py` re-runs `zeta_cert_rosen.py` at the six points, `N = 32` **and** `N = 64`,
`ctx.prec = 400`; every value reproduces `mirror_q3.json` to the printed digit, and
`rel drift(32 → 64) ≤ 1.8e−16` everywhere. The kernel `|φ_3||K_3|` is imported **unchanged** from
`mirror_u4_corrected.py`. Only the determinant evaluator differs between the two ratio columns.

| `σ` | `RHS = \|φ_3\|\|K_3\|` | `P_repo(1−s)/P_repo(s)` | **ratio repo** | `P_May(1−s)/P_May(s)` | **ratio indep.** |
|--:|---|---|---|---|---|
| 1.25 | `2.2134094` | `2.8962162` | `1.308486` | `2.2134094` | **`1.000000005`** |
| 1.40 | `3.3669561` | `5.6003851` | `1.663338` | `3.3669561` | **`1.000000004`** |
| 1.50 | `4.3554517` | `8.6358757` | `1.982774` | `4.3554517` | **`1.000000003`** |

### 2.1 Where the residual comes from, split by side

The residual is the **quotient** of the two per-point discrepancies — reported here because it says
how much of it is the `Re s ≤ 0` mirror and how much is the `Re s > 1` side:

| `σ` | `P_repo/P_indep` at `s` (`Re s > 1`) | at `1−s` (`Re s < 0`) | quotient | measured residual |
|--:|---|---|---|---|
| 1.25 | `0.949863` | `1.242882` | `1.308486` | `1.308486` |
| 1.40 | `0.961752` | `1.599718` | `1.663338` | `1.663338` |
| 1.50 | `0.968157` | `1.919636` | `1.982774` | `1.982774` |

**The reconstruction is exact.** §3.4's reading — "it lives in the mirror evaluation" — is **right in
its dominant term and incomplete**: the mirror side carries `24 %` to `92 %` of error while the
`Re s > 1` side carries `3 %` to `5 %`, so the builder is wrong on **both** sides, by a factor that
grows as `Re s` decreases. The residual is the ratio of the two, which is why it tends to `1` at the
critical line and grows with `|σ − 1/2|`, exactly as K.9 recorded.

---

## 3. What the builder's defect is **not** — `q3cont_nhead.json`

`N`-truncation was already eliminated (K.8, `≤ 3.9e−16` to `N = 64`; re-confirmed here at `N = 64`).
The other truncation knob in `build_reduced_matrix_ball` is `n_head`, the number of Hurwitz heads
split off before the exact tail closure. Pre-registered before the run:

> *flat at both points ⇒ `n_head` is not the defect, the discrepancy is structural; small at
> `Re s > 1` and large at `Re s ≤ 0` ⇒ the head/tail split is the continuation defect.*

| point | `n_head = 2` | `4` | `6` | `8` | rel drift |
|---|---|---|---|---|---|
| `Re s = +1.25` | `0.84563714519754` | `0.84563714519754` | `0.84563714519754` | `0.84563714519754` | **`0.0`** |
| `Re s = −0.25` | `2.44914797385350` | `2.44914797385350` | `2.44914797385350` | `2.44914797385350` | **`0.0`** |

**Bit-identical.** By the pre-registered rule the defect is **structural, not a truncation**: the
builder converges — in `N` and in `n_head` — to a function that is not `Z_{PSL(2,Z)}`.

**So the word "continuation" in §3.4's hypothesis is the wrong word, while the hypothesis is
right.** The builder is not failing to *continue* correctly; the `q = 3` object it computes is a
different analytic function everywhere, differing from `Z` by a smooth zero-free factor `R(s)` that
happens to be near `1` where the lane first validated it and far from `1` at the mirror.

**It is not that the builder has no relation to `Z`:** at the scattering-zero point
`s = 1/4 + i t_∞` the repo builder returns `P_3 = 8.47e−16` (`drift(32→64) = 1.4e−12`), i.e. it has
the same zero. `R(s)` is zero-free where measured.

### 3.1 Leading structural hypothesis, **not** tested here

`q = 3` in `zeta_cert_rosen.py` is a **special-case branch** (`hq = 0`, `kappa = 1`, the "scalar
eq. (33)" two-line path), and `λ_3 = 1` makes the Rosen `λ`-continued fraction the **nearest-integer**
CF, not the Gauss CF that Mayer's theorem uses. The two transfer operators are known to be related
but are not the same operator. `TODO-VERIFY`: open MMS (Mayer–Mühlenbruch–Strömberg, *The transfer
operator approach to Selberg's zeta function …*) eq. (33) and check whether their `q = 3` statement
carries a correction factor relative to `Z` that the lane's transcription dropped. **The source was
not opened in this note** — this is a hypothesis about which line is wrong, exactly the kind of
claim `LAW_MIRROR_Q3_DISCRIMINATOR.md` §4 was right to refuse to assert without the source.

---

## 4. Why the earlier validations did not catch it — `q3cont_largesigma.json`

`LAW_U1_GROWTH.md` §7.2 validated `P_q` against the truncated Selberg Euler product at large
`Re s`, agreeing to `≤ 2e−3`. That is the obvious counter-argument to §0, and it fails:

| `σ` | `P_repo` | `P_indep` | ratio | `\|ratio − 1\|` |
|--:|---|---|---|---|
| 2.0 | `0.966590992839` | `0.978808789442` | `0.987517688` | `1.25e−2` |
| 3.0 | `0.995648409605` | `0.997489063185` | `0.998154713` | **`1.85e−3`** |
| 4.0 | `0.999410430176` | `0.999680077730` | `0.999730266` | `2.70e−4` |

`R(s) → 1` monotonically as `σ → ∞`, and **by `σ = 3` it is already inside §7.2's own `2e−3`
tolerance.** Both evaluators pass a large-`σ` Euler check; the check cannot separate them. This is
the **third** structurally blind validation this lane has found, after `|K_q(1/2+it)| = 1` (K.5) and
`N`-stability (§3). The pattern is now explicit and worth stating as a lane rule:

> **Every check this lane has trusted was run where the quantity under test is near its trivial
> value** — `|K| = 1` on the critical line, `P ≈ 1` at large `σ`, `drift ≈ 0` in `N`. A check has to
> be run where the object is *not* near-trivial, or it certifies nothing.

---

## 5. Blast radius — what this does and does not touch

**Measured at `q = 3` only, and `q = 3` is a special-case code branch.** The following is a
scoping statement, not a clean bill of health for anything.

| item | status |
|---|---|
| `LAW_TEO_KAPPA_CORRECTED.md` K.6 `[0.456, 2.055]` residual, `q = 3` rows | **EXPLAINED.** It is the builder. `(*)` holds at `q = 3`. |
| K.9 (residual smooth, `→1` at the line, grows for `Re(1−s) < 0`) | **`HEURISTIC` → mechanism named**: it is `R(1−s)/R(s)` for the builder's zero-free discrepancy factor `R`. |
| K.10 ("U4 not refuted, not confirmed") | **at `q = 3`, now CONFIRMED** (`≤ 3e−7`). At `q ≠ 3, 5` unchanged: still `GAP`. |
| `q = 4, 6` rows of K.6 (`0.456`–`2.055`) | **NOT explained.** They use `zeta_cert_rosen_even.py`, a different module, untested here. The `q = 3` finding makes "the builder" the leading candidate there too, but that is an inference, not a measurement. `TODO-VERIFY`. |
| the flagship `G_5` results (`zeta_cert_rosen_q5.py`, `research_notes` `g5-offline-resonance-theorem`) | **NOT touched by this note, and not cleared by it.** The `q = 5` path is a different branch with its own validations (`selfcheck_q5`, Maass zeros `r = 6.4737`, `8.6368`, cross-validation against Hejhal point-matching). Those validations are of the **zero locations**, which §3 shows survive a zero-free factor `R(s)`. **A zero-free `R` cannot move a zero.** So the `G_5` zero/resonance claims are structurally insulated; any `G_5` claim about a determinant's *magnitude* off the zero set is not. `TODO-VERIFY`: enumerate which. |
| `LAW_U1_GROWTH.md` §7.3 / §10 (viii) — the `sup_{∂U}` growth readings | **NOW IN DOUBT, in a new way.** They are magnitudes of `probe_u1_sup.py`'s determinant, on `∂U` including `Re s ≤ 0`, i.e. precisely where `R` departs from `1` fastest. §4.2 of the parent had already weakened the anti-artefact sub-claim; this note supplies the artefact. |
| `LAW_U1_GROWTH.md` §7.2's Euler-product validation | **shown non-discriminating** (§4). It does not defend the proxy. |

---

## 6. `q = 4` σ-sweep — the parent's `TODO-VERIFY` (5) discharged

`LAW_TEO_KAPPA_CORRECTED.md` §3.4: *"(`q = 4`, from the run log only, **not banked in the JSON** …
`TODO-VERIFY`: re-run and bank it.)"* Done: `q3cont_q4_sigmasweep.py` → `.json`, same corrected
kernel imported unchanged from `mirror_u4_corrected.py`, `N = 32`, `prec = 400`, `t = t_∞`, on the
same `σ` grid as the banked `q = 3` rows.

| `σ` | mirror `Re(1−s)` | **`q = 4` ratio** | `q = 3` ratio (banked, for contrast) |
|--:|--:|---|---|
| 0.55 | `+0.45` | `0.870837` | `0.98197` |
| 0.60 | `+0.40` | `0.755414` | `0.96520` |
| 0.70 | `+0.30` | `0.551751` | `0.93902` |
| 0.80 | `+0.20` | **`0.370415`** | `0.92899` |
| 0.90 | `+0.10` | **`0.206612`** | `0.94345` |
| 1.00 | `+0.00` | **`0.108344`** | `0.99135` |
| 1.10 | `−0.10` | `0.207596` | `1.08107` |
| 1.25 | `−0.25` | `0.455610` | `1.30849` |
| 1.50 | `−0.50` | `0.840166` | `1.98277` |

**Cross-checks:** the three `σ = 0.55, 0.60, 0.70` values reproduce the parent's run-log numbers
(`0.87084`, `0.75541`, `0.55175`) exactly, and `σ = 1.25, 1.50` reproduce
`mirror_u4_corrected.json`'s `0.455610`, `0.840166` exactly. The re-run is faithful.

**The shape is new and it is not the `q = 3` shape.** `q = 4` has a deep, sharp **minimum of
`0.108` at `σ = 1.00`** — a factor of `9` — and is symmetric-ish about it, rising back to `0.84` by
`σ = 1.5`. The `q = 3` sweep is a shallow well of depth `7 %` near `σ = 0.8` turning into monotone
growth. `TODO-VERIFY` (the parent's open item (4) remains open): the `q = 4` minimum sits at
`σ = 1`, where the mirror point is `Re(1−s) = 0` — the boundary of the region where §3's factor `R`
was measured to move. Whether that is the even-`q` builder's analogue of `R` or something else is
**not** determined here, and this note deliberately does not force a reading of it: the decisive
`q = 4` test would need an independent even-`q` determinant, which does not exist in this repo.

---

## 7. Status ledger

| id | claim | status | where |
|---|---|---|---|
| PC.1 | Independent Mayer/Gauss-map determinant built, sharing no code with the repo builder; matrix derived in-probe | **`PROVED`** (derivation) | §1 |
| PC.2 | It passes three classical validations: `Z(1) = 0`, `Z(1/4 + iγ₁/2) = 0`, first odd Maass `r = 9.5337` | **`PROVED`** numerically | §1.1 |
| PC.3 | **With it, `(*)` holds at `q = 3` at `σ = 1.25, 1.40, 1.50`** — printed deviation `≤ 4.5e−9`, defensible bound `≤ 3e−7` (§1.2) | **the finding** | §0, §2 |
| PC.4 | **The `O(1)` residual is the repo builder's `q = 3` determinant, entirely** — reconstructed exactly as the quotient of its per-point errors | **the finding** | §2.1 |
| PC.5 | **U4 at `q = 3` and the corrected Teo `κ_3` are jointly confirmed**, to `≤ 3e−7` against an `O(1)` residual | **`PROVED`** numerically | §0 |
| PC.6 | The builder's error is `N`-flat (`1.8e−16` to `N = 64`) **and** `n_head`-flat (bit-identical, `n_head = 2…8`) — structural, not a truncation | **`PROVED`** numerically | §3 |
| PC.7 | The discrepancy factor `R(s) = P_repo/P_indep` is smooth and zero-free where measured (`0.9499 → 0.9682` on `Re s > 1`; `1.2429 → 1.9196` on `Re s < 0`; `→ 1` as `σ → ∞`) | **measured** | §2.1, §4 |
| PC.8 | `LAW_U1_GROWTH.md` §7.2's Euler-product validation is **structurally blind**: `\|R − 1\| = 1.85e−3` at `σ = 3`, inside its own `2e−3` tolerance | **`PROVED`** numerically | §4 |
| PC.9 | Cause of the builder's defect: **not diagnosed.** Leading hypothesis = the `q = 3` scalar eq. (33) branch / nearest-integer-vs-Gauss CF; **MMS source not opened** | **`GAP` + `TODO-VERIFY`** | §3.1 |
| PC.10 | `q = 4, 6` residuals are **not** explained here (different module, `zeta_cert_rosen_even.py`) | **`GAP`** | §5 |
| PC.11 | A zero-free `R` cannot move a zero, so the `G_5` zero/resonance claims are structurally insulated; `G_5` magnitude claims off the zero set are not | **`HEURISTIC`** — needs an enumeration | §5 |
| PC.12 | `q = 4` σ-sweep banked; reproduces the parent's log and JSON values exactly; shape has a sharp minimum `0.108` at `σ = 1.00` | **measured, clean** | §6 |

**Open `TODO`s created here.** (1) Open MMS eq. (33) and settle PC.9. (2) Build an independent
even-`q` determinant, or find a `q` with a classical target, to settle PC.10. (3) Enumerate which
`G_5` claims are magnitude claims off the zero set (PC.11). (4) Re-read `LAW_U1_GROWTH.md` §7.3's
`∂U` growth table in the light of §5 — the artefact reading now has a measured mechanism.
The parent's `TODO`s (1), (2), (5) are **not** touched here.

---

## 8. Receipts

All under `lane_g/law_probes/`. Interpreter `/Users/za/miniforge3/envs/pari-arb/bin/python3`.

- `q3cont_mayer_indep.py` → `.json`, `.log` — the independent evaluator, V1–V3, the six points,
  `N = 12…28`, `mp.dps = 60`.
- `q3cont_repo_builder.py` → `.json`, `.log` — `zeta_cert_rosen.py` at the same six points plus the
  scattering zero, `N = 32` and `64`, `ctx.prec = 400`, per-sign determinants banked.
- `q3cont_compare.py` → `.json`, `.log` — §0 / §2 / §2.1, the verdict.
- `q3cont_nhead.py` → `.json`, `.log` — §3, the pre-registered `n_head` sweep.
- `q3cont_largesigma.py` → `.json`, `.log` — §4.
- `q3cont_q4_sigmasweep.py` → `.json`, `.log` — §6.
- **Not modified:** `mirror_u4.py`, `mirror_u4_corrected.py`, `mirror_q3.py`, `mirror_arith.py`,
  `probe_u1_*.py`, every other probe, `zeta_cert_rosen*.py`, `lane_f/`, every other lane.
  `q3cont_compare.py` and `q3cont_q4_sigmasweep.py` **import** from `mirror_u4_corrected.py`
  unchanged, so the kernel under test is byte-identical to the parent's.

**Rigour.** Float midpoints throughout, no interval arithmetic, no winding certificate — the same
status as every number in the parent notes. `PC.3`'s `4.5e−9` is quoted at the independent
evaluator's own `N`-resolution (`≤ 2.6e−7` at the mirror points, §1.2) and is **not** claimed tighter.

---

READY FOR JUDGING

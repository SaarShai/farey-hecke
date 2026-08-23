# SCAT-1 — a certified zero of the scattering determinant φ_q itself

**Date:** 2026-08-23. **Lane:** G / SCAT-1. **Status:**
**UNREFEREED / CONJECTURAL pending cold referee.** Append-only.
**Target:** NOGO-OPEN-1 (`NOGO_METATHEOREM_SOL.md` §5.1) — a theorem-valid
certified zero of `φ_q` in `1/2 < Re s < 1` for a non-arithmetic `q`, and, if
possible, two such zeros at distinct real parts.
**Interpreter:** `/Users/za/.venvs/farey-rh/bin/python` (mpmath).

---

## 0. Feasibility verdict, up front

Two verdicts, because the brief's two phases split cleanly.

> **V1 — the route the brief proposed (exact enumeration of the Hejhal (7.5)
> coefficients `d_q(n), g_{q,n}` with a proven tail bound) is INFEASIBLE,
> and not for want of effort or compute. It is blocked by a proof, not by a
> budget.** The generalized Dirichlet series `D_q(s) = Σ d_q(n) g_{q,n}^{−2s}`
> of (7.5) has abscissa of convergence **exactly `σ_c = 1`**. The whole target
> strip `1/2 < Re s < 1` lies outside it. No enumeration depth and no tail
> bound can evaluate `φ_q` at a point where the series diverges. §2 proves
> `σ_c = 1` two independent ways and measures it.

> **V2 — but the artifact NOGO-OPEN-1 calls absent is, in one clause,
> ALREADY IN THE BANK, and the NOGO note's own remark 2 is too pessimistic.**
> The certified off-line **Selberg-zeta** zero `s*` of `Z_{G_5}`
> (`THEOREM_G5_OFFLINE_ASSEMBLY.md`) is nonreal with `0 < Re s* < 1/2`.
> By the classical Selberg-zeta divisor theorem for cofinite Fuchsian groups,
> a nonreal zero of `Z_Γ` in `0 < Re s < 1/2` **is a pole of `φ`** — a fact
> the G_5 theorem *already consumes*, as its own link 7. The functional
> equation `φ(s)φ(1−s) = 1` then converts that pole into a **zero of `φ_5`**
> at `ρ = 1 − s*`, `Re ρ ≥ 0.5461038 > 1/2`. §3. The "wrong function"
> objection is repaired by reflection, not by a new certifier.

> **V3 — the countermodel NOGO-OPEN-1 actually asks for (TWO zeros at
> distinct real parts) is NOT delivered here, and its blocker is now sharp
> and purely computational:** one more certified `Z_{G_5}` off-line zero at a
> real part separated from `0.4538952`. That is a second winding box on
> machinery that already exists — not a new theory. §5.

**Nothing in this note is refereed. §3 in particular rests on one cited,
in-repo-unverified classical theorem (§3.3, `TODO-VERIFY`).**

---

## 1. What was read

`LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_SOL.md` (the `(D)`/`(N)`/`(NF)` normal
form and its 2026-08-19 / 2026-08-20 correction blocks),
`LAW_HEJHAL_S7_EXTRACT.md` (7.5 and the Thm 7.11 skeleton),
`LAW_R1_COSET_STRUCTURE.md` + its window-completeness corrections,
`SCAT_EVAL_Q_SOL.md` + `…_REFEREE.md`, `LAW_TEO_KAPPA_CORRECTED.md`,
`NOGO_METATHEOREM_SOL.md` §5, `THEOREM_G5_OFFLINE_ASSEMBLY.md`,
`NO_VERTICAL_LINE_COROLLARY.md`.

Wiki search `"scattering determinant coefficients"` returned `[]` — no wiki
page covers this. Recorded so the next agent does not repeat the query.

---

## 2. Phase 1 — why the enumeration route cannot reach the strip

### 2.1 The obstruction, stated

Write, per `(D)`,

```
    phi_q(s) = sqrt(pi) * Gamma(s-1/2)/Gamma(s) * D_q(s),
    D_q(s)   = Sum_{n>=1} d_q(n) g_{q,n}^{-2s}
             = Sum_{[S]\G_q/[S], c != 0} |c|^{-2s},        (Re s > 1)
```

with `d_q(n)` **positive integers** (multiplicity of the value `g_{q,n}` in the
double-coset `c`-spectrum; positivity is noted in the LAW note's 2026-08-20
correction 1). The question the brief asks — "can the coefficients be
enumerated exactly up to a truncation with a proven tail bound?" — has the
answer *yes for the enumeration, no for the tail*, and the "no" is fatal:

> **Proposition 2.1 (abscissa).** `D_q` has abscissa of convergence and of
> absolute convergence **exactly `σ_c = σ_a = 1`**, for every finite `q ≥ 3`.
> Consequently `D_q(s)` diverges at every `s` with `Re s ≤ 1`, and in
> particular at every point of the target strip `1/2 < Re s < 1`.

Two independent proofs.

**(a) Analytic (via the residual pole).** In the width-one cusp normalization
the Eisenstein series has the expansion `E_q(z,s) = y^s + φ_q(s) y^{1−s} + …`.
`E_q` has a simple pole at `s = 1` with residue the constant `1/vol(G_q\H)`
(the residual/constant eigenfunction; standard for any cofinite group with a
cusp). `y^s` is regular at `s = 1`, so the pole is carried by
`φ_q(s) y^{1−s}`; setting `y^{1−s} → 1`,

```
    Res_{s=1} phi_q(s) = 1 / vol(G_q\H),   vol(G_q\H) = pi (1 - 2/q).
```

`Γ(s−1/2)/Γ(s)` is holomorphic and nonzero at `s = 1`, so `D_q` has a simple
pole at `s = 1`. `D_q` is a generalized Dirichlet series with **nonnegative**
coefficients, so by Landau's theorem its abscissa of convergence is a
singularity of the sum. If `σ_c < 1` then `D_q` would be holomorphic on
`Re s > σ_c ∋ 1`, contradicting the pole. Hence `σ_c ≥ 1`; convergence for
`Re s > 1` (Hejhal (7.5)) gives `σ_c ≤ 1`. ∎

**(b) Geometric (via the counting function).** With
`N_q(X) := #{ [S]\G_q/[S] : 0 < |c| ≤ X }` (i.e. `Σ_{g_{q,n} ≤ X} d_q(n)`), the
classical one-cusp asymptotic is `N_q(X) ~ A_q X²` with `A_q = 1/(π·vol)`.
Then `D_q(σ) = ∫ x^{−2σ} dN_q(x)` diverges for `2σ ≤ 2`. ∎

The two proofs agree on the constant: matching `D_q(s) ≈ A_q/(s−1)` against
`Res_{s=1} φ_q = π·A_q = 1/vol` gives `A_q = 1/(π·vol) = 1/(π²(1−2/q))`.

### 2.2 Receipts

**Exact anchor at `q = 3`** (where `φ_3(s) = √π Γ(s−1/2)ζ(2s−1)/(Γ(s)ζ(2s))`
is known in closed form) — proof (a)'s residue formula is exact:

```
$ /Users/za/.venvs/farey-rh/bin/python scat1_residue.py
q=3 exact: Res_{s=1} phi_3 = sqrt(pi)Gamma(1/2)/Gamma(1)*(1/2)/zeta(2) = 0.954929658551
           1/vol(G_3) = 3/pi                                          = 0.954929658551
```

Agreement to all 12 printed digits. This is a *derivation check*, not a fit.

**Counting exponent and constant**, measured on the banked **saturated**
(completeness-repaired) `c`-spectra `X ≤ 50`
(`law_probes/r1_coset_enum_complete_X50.json`, `q = 5, 8, 12, θ`):

| q | N(X)=… at X=5,10,…,50 | log-log slope of N(X), X∈[20,50] |
|---|---|---|
| 5 | 3, 14, 36, 70, 106, 148, 204, 274, 346, 428 | **1.9909** |
| 8 | 6, 10, 34, 58, 88, 128, 164, 216, 278, 330 | **1.9080** |
| 12 | 3, 14, 26, 48, 76, 102, 156, 190, 256, 318 | **2.0650** |
| θ (λ=2) | 3, 13, 23, 45, 63, 95, 127, 173, 205, 263 | **1.9541** |

The predicted exponent is `2`, i.e. `σ_c = 1`. The **constant** matches too:

| q | vol = π(1−2/q) | A_pred = 1/(π·vol) | A_meas = N(50)/50² | rel. dev. |
|---|---|---|---|---|
| 5 | 1.884956 | 0.168869 | 0.171200 | **1.38 %** |
| 8 | 2.356194 | 0.135095 | 0.132000 | **2.29 %** |
| 12 | 2.617994 | 0.121585 | 0.127200 | **4.62 %** |
| θ | 3.141593 | 0.101321 | 0.105200 | **3.83 %** |

Deviations are at the level expected from a single finite window `X = 50`
(no error bars are claimed; this is corroboration of an asymptotic, not a
certified constant). The receipt is that the *exponent* and the *constant*
both land where proof (a) puts them, in the non-arithmetic cases too.

**Divergence, shown directly.** Partial sums `Σ_{|c| ≤ X} |c|^{−2σ}` on the
same saturated spectra. `σ = 1.5` (inside the half-plane of convergence)
saturates; `σ = 0.75` (the q=3 zero line, mid-strip) does not:

```
q=5   sigma=1.50  D_partial(X):   0.3475 0.3896 0.4031 0.4098 0.4130 0.4151 0.4167 0.4181 0.4190 0.4198
q=5   sigma=0.99  D_partial(X):   0.6831 0.9558 1.1198 1.2405 1.3164 1.3766 1.4337 1.4881 1.5305 1.5690
q=5   sigma=0.75  D_partial(X):   0.9580 1.6205 2.1550 2.6270 2.9645 3.2586 3.5620 3.8702 4.1275 4.3742
q=8   sigma=1.50  D_partial(X):   0.2402 0.2501 0.2633 0.2672 0.2699 0.2717 0.2727 0.2737 0.2745 0.2750
q=8   sigma=0.75  D_partial(X):   1.0217 1.2196 1.7730 2.0773 2.3609 2.6298 2.8183 3.0440 3.2664 3.4252
                                  (X = 5,10,15,20,25,30,35,40,45,50)
```

At `σ = 0.75` the `q = 5` partial sum has not flattened by `X = 50` and grows
consistently with the `X^{2−2σ} = X^{0.5}` law that Proposition 2.1 predicts;
at `σ = 1.5` it has converged to three digits by `X = 20`. Probe scripts:
`scat1_abscissa.py`, `scat1_residue.py` (scratchpad; nothing written into the
repo tree — this note is the only repo artifact).

### 2.3 Why there is no repair inside the series

Three natural repairs, all blocked, and it is worth saying why so the route is
not re-proposed:

1. **Bigger `X`, better tail bound.** Irrelevant. The obstruction is not the
   size of the tail; the tail is *infinite*. `Sum_{|c|>X} |c|^{−2σ} = ∞` for
   `σ ≤ 1`.
2. **Smoothing / approximate functional equation.** The classical device that
   continues `ζ` past its abscissa needs a functional equation of the form
   `f(s) = χ(s) f(1−s)` with a *Dirichlet series on both sides*. The
   scattering functional equation is **multiplicatively inverse**,
   `φ(s)φ(1−s) = 1`, and `1/φ` is not a Dirichlet series of the same shape.
   There is no Riemann–Siegel analogue here. This is precisely why `q = 3`
   works and general `q` does not: at `q = 3`, `φ_3` happens to be a **ratio**
   `ζ(2s−1)/ζ(2s)` of two separately continuable objects, and the strip
   values come from ζ's continuation — an arithmetic accident, unavailable
   for non-arithmetic `q`.
3. **A second, continuable presentation of `φ_q`.** This is the *only* live
   option, and there is exactly one known: the Teo/Selberg-zeta quotient
   `φ_q(s) = Z_{G_q}(1−s) / (Z_{G_q}(s) K*_q(s))` (`SCAT_EVAL_Q_SOL.md`
   (SCAT-EVAL)). So the Selberg-zeta route is not one option among many — it
   is structurally forced. §3 uses it, and its classical shadow.

**Consequence for the brief's Phase-1 question.** Coefficient enumeration is
feasible and already built (`law_probes/r1_coset_enum.py`, validated to 1–2 %
against the determinant-route evaluator, saturated at `X ≤ 50` for
`q = 5, 8, 12, θ`). Truncation-depth estimation for certified evaluation at
`Re s ∈ [0.55, 0.95]` is **not a well-posed question**: no finite depth
suffices, at any precision, in interval arithmetic or otherwise. No interval
evaluator was built, and building one would have been wasted work.

---

## 3. Phase 2 — the zero that is already certified, once reflected

### 3.1 The reduction

Let `Γ` be cofinite with one cusp, `Z_Γ` its Selberg zeta, `φ` its scalar
scattering determinant.

> **Lemma 3.1 (reflection).** Suppose `Z_Γ(s*) = 0` with `Im s* ≠ 0` and
> `0 < Re s* < 1/2`, of order `m ≥ 1`. Then `φ` has a zero of order `m` at
> `ρ := 1 − s*`, and `1/2 < Re ρ < 1`, `Im ρ ≠ 0`.

*Proof.* **(i)** By the Selberg-zeta divisor theorem for cofinite Fuchsian
groups (§3.3), the zeros of `Z_Γ` in `0 < Re s < 1/2` off the real axis are
exactly the poles of `φ`, with matching multiplicity: the spectral zeros lie
on `Re s = 1/2` or on the real segment `(1/2, 1]`, and every trivial zero or
pole contributed by the identity, elliptic, and parabolic terms sits on the
**real** axis. `Im s* ≠ 0` excludes all of those, so `s*` is a pole of `φ` of
order `m`. **(ii)** `φ(s)φ(1−s) ≡ 1`. Near `s = s*`, `φ(s) = C(s−s*)^{−m}(1+o(1))`
with `C ≠ 0`, hence `φ(1−s) = C^{−1}(s−s*)^{m}(1+o(1))`, i.e. `φ` has a zero of
order `m` at `1 − s*`. **(iii)** `Re ρ = 1 − Re s* ∈ (1/2, 1)` and
`Im ρ = −Im s* ≠ 0`. ∎

Step (ii) is the LAW note's own §5 argument, run in the opposite direction.
Step (i) is its link to the certified object.

### 3.2 Applied to G_5 — the box

`THEOREM_G5_OFFLINE_ASSEMBLY.md` (DECLARED, five adversarial rounds, V8
"THEOREM-GRADE YES") certifies a zero `s*` of `Z_{G_5}` with
`|Re s* − 0.4538951800749447| ≤ 10⁻⁶`, `|Im s* − 5.7635372417301305| ≤ 10⁻⁶`.
Reflecting the box (`scat1_box.py`, bounds UP, margins DOWN):

```
certified Z_{G_5} zero box:
  Re s* in [0.4538941800749447, 0.4538961800749447]
  Im s* in [5.7635362417301305, 5.7635382417301305]
reflected box rho = 1 - s*  (the phi_5 zero):
  Re rho in [0.5461038199250553, 0.5461058199250553]
  Im rho in [-5.7635382417301305, -5.7635362417301305]
  strict-right margin (Re rho - 1/2), rounded DOWN: 0.04610381993
  distance to the Re = 1 boundary,   rounded DOWN: 0.4538941801
```

> **CLAIM 3.2 (UNREFEREED / CONJECTURAL; conditional on §3.3).**
> The scalar trivial-character scattering determinant `φ_5` of the
> **non-arithmetic** Hecke triangle orbifold `G_5\H` has a zero `ρ` with
>
> ```
>   Re rho ∈ [0.5461038199250553, 0.5461058199250553]  ⊂ (1/2, 1)
>   Im rho ∈ [-5.7635382417301305, -5.7635362417301305]
> ```
>
> with strict-right margin `Re ρ − 1/2 ≥ 0.0461038` (rounded DOWN), and, by
> reality (`φ(s̄) = conj φ(s)`, axiom A3), a second zero at `conj ρ` — same
> real part.

Every numeral above is an interval endpoint inherited from the G_5 receipt;
no new numerical error is introduced by reflection (the map `s ↦ 1−s` is
exact on the box corners).

### 3.3 The one undischarged input — `TODO-VERIFY`

Lemma 3.1 step (i) is the **classical Selberg-zeta divisor theorem for
cofinite Fuchsian groups with elliptic fixed points and one cusp**, in the
precise form: *the nonreal zeros of `Z_Γ` in `0 < Re s < 1/2` are the poles of
`φ`, with multiplicity.*

- It is **not proved here** and **not verified against a page in this repo**.
- It is, however, **already consumed by the parent theorem**:
  `THEOREM_G5_OFFLINE_ASSEMBLY.md` link 7, "RESONANCE INTERPRETATION
  [STANDARD, CITED] … `Z_S` zeros in `0 < Re(s) < 1/2` off the real axis are
  resonances (scattering poles of the meromorphically continued
  resolvent/scattering matrix); discrete-spectrum zeros lie on `Re(s) = 1/2`
  or on the real segment", citing Hejhal LNM 1001, Iwaniec *Spectral Methods*
  ch. 10–11, Borthwick. **Claim 3.2 therefore adds no dependency the declared
  G_5 theorem does not already carry.** That is the honest strength of this
  route and also its ceiling.
- `TODO-VERIFY`: open Hejhal LNM 1001 Vol. 2, Theorem 5.3 (the divisor of
  `Z_Γ` for cofinite Γ, with the elliptic and parabolic trivial-divisor
  lists), and/or Venkov, and pin the exact statement — specifically that the
  *elliptic* trivial divisor of an orbifold contributes only on the real
  axis. Nothing in the bank contains that page. This is the single cheap
  literature item that would promote Claim 3.2 out of CONJECTURAL.

### 3.4 Route 2 — the same conclusion through Teo, as a cross-check

Independent of §3.3, Teo Prop. 2.5 (`LAW_TEO_KAPPA_CORRECTED.md`) gives
`Z(1−s) = κ_q(s) Z(s)` with `κ_q = K*_q · φ_q`. At `s = ρ = 1 − s*`:

```
    Z(s*) = K*_q(rho) · phi_q(rho) · Z(rho).
```

`Z(s*) = 0` (certified). So `φ_q(ρ) = 0` provided `K*_q(ρ) ∉ {0, ∞}` and
`Z(ρ) ≠ 0`. Both hold at this specific `ρ`:

- **`Z(ρ) ≠ 0`:** `Re ρ > 1/2` and `Im ρ ≠ 0`; in `Re s > 1/2` the only
  `Z`-zeros are the real small-eigenvalue parameters in `(1/2, 1]`.
- **`K*_q(ρ)` finite and nonzero**, computed at signature `(0; n=1; (2,q))`,
  `|X| = π(1−2/q)`, `Γ₂ = 1/G` (Lemma K-1) — `scat1_box.py`:

```
  K*_5 at rho (corner lo): |K*| = 1.31691271194
  K*_5 at rho (centre):    |K*| = 1.31692048194
  K*_5 at rho (corner hi): |K*| = 1.31692825199
    |sin(pi(rho+0)/2)| = 4273.5321      |sin(pi(rho+0)/5)| = 18.683421
    |sin(pi(rho+1)/2)| = 4273.5321      |sin(pi(rho+1)/5)| = 18.698632
                                        |sin(pi(rho+2)/5)| = 18.707116
                                        |sin(pi(rho+3)/5)| = 18.697159
                                        |sin(pi(rho+4)/5)| = 18.682511
```

Every elliptic `sin`-factor is `> 18`, so the fractional powers are far from
their branch points and `K*_5(ρ)` is bounded away from `0` and `∞`
(`Im ρ ≈ −5.76` is what buys this: the whole `K*_q` divisor sits on the real
axis). The `(−1)^{A/2}` prefactor is a unimodular constant and zero-free.

**Status of route 2: WEAKER than route 1, and reported only as a
cross-check.** The `SCAT_EVAL_Q_REFEREE` obligations stand in full — Teo must
still be specialized to signature `(0;1;(2,q))`, bound to Hejhal's width-one
cusp/scalar convention, and every branch in `K*_q` fixed. The numbers above
are float midpoints (mpmath, dps 40), **not interval enclosures**, and the
`|K*|` values are `NOT EVIDENCE` for a certificate — they are evidence that
*no divisor obstruction sits at this `ρ`*, which is the only thing route 2 is
asked to show here. Route 1 does not need any of it.

---

## 4. What this does and does not do to NOGO-OPEN-1

`NOGO_METATHEOREM_SOL.md` §5.1 asks for `M ∈ 𝔐(A)` with **two** nonreal zeros
`ρ₁, ρ₂`, `1/2 < Re ρ_i < 1`, `Re ρ₁ ≠ Re ρ₂`.

| §5.1 remark | status after this note |
|---|---|
| "The `G_5` off-line pin does not supply it … a *different function*, and on the *wrong side* of the line" | **Half-repaired.** The wrong-function/wrong-side objection dissolves: Lemma 3.1 maps the pin to `φ_5` and across the line in one step, adding no dependency the parent theorem lacks. The *two distinct real parts* objection survives untouched. |
| "We have no certified zero of any `φ_q` for non-arithmetic `q`" | **Superseded, conditionally** — Claim 3.2, conditional on §3.3, UNREFEREED. `SCAT-EVAL_q` as an *evaluator* remains OPEN; this route never builds one. |
| "A synthetic countermodel is a genuine construction problem" | Unchanged. Not attempted. |

**NOGO-OPEN-1 is NOT closed.** One zero is not two. And note the trap: `A3`
reality gives `conj ρ` for free, at the *same* real part — so conjugate pairs
never count as the second pin.

---

## 5. Blockers and the staged plan

### 5.1 Blocker, named precisely

> **The only thing standing between the bank and NOGO-OPEN-1 is a SECOND
> certified nonreal zero of `Z_{G_5}` in `0 < Re s < 1/2` whose real part is
> separated from `0.4538952` by more than the two boxes' widths.**

This is the same open item `NO_VERTICAL_LINE_COROLLARY.md` (scope limits,
item 4) already records — *"Excluding one line in general needs two certified
pins at distinct real parts; that remains open."* SCAT-1's contribution is to
show the two open items are **the same item**: closing the vertical-line
corollary closes NOGO-OPEN-1, via Lemma 3.1, with no further analysis.

The blocker is **computational, not conceptual**: the certifying machinery
(R3b winding + closed-contour exclusion, Arb/Acb subarc enclosure, the E1
enlarged-contraction transport, the MMS `K_s` divisor exclusion) is built,
adversarially reviewed, and replayable. What is missing is a *second box* and
the compute to certify it.

### 5.1b The second pin already has a named candidate — and known costs

`SECOND_PIN_PREP.md` (prep only; **nothing executed**) carries the intended
second G_5 pin at

```
    s_2 ~ 0.24302842340131198 + 10.560296779143401 i
```

(scan-level winding 1, winding ball `[0.99996722, 1.00003277]`, box half-width
**0.012** — not `1e-6` — `K_per_edge = 28`, `|det| ~ 3.56e-15`, heuristic tail
`1.05e-7`). Its real part is separated from the flagship's `0.4538952` by
`> 0.21`, which is **two orders of magnitude larger than either box** — so if
certified it would give distinct real parts with enormous margin, and via
Lemma 3.1 two `φ_5` zeros at `Re ~ 0.5461` and `Re ~ 0.7570`.

Three further empirical G_5 winding-1 coordinates from the same scan
(`Re = 0.4105437, 0.4470830, 0.4690553`) are also separated from the flagship
by `> 0.015`, i.e. `> 10⁴` box widths — several independent chances.

The costs are recorded, not hidden. `SECOND_PIN_PREP.md` §5 lists blockers
B1–B8; the two that bear on S2 planning:

- **B2 (hard).** Every box-local constant degrades at `s_2`: deep-tail
  parameter `p` falls `0.908 → 0.486` and `|t|` rises `5.76 → 10.56`, while
  the flagship closed with a margin of only `3.4378649e-8` at `N = 160`.
  `F_R` closure at `N = 160` is therefore **not** inferable; expect a larger
  `N`, and budget for the possibility that it does not close at all. Also the
  reported `N`-spread in `Re` is `4.5e-6`, exceeding the intended `1e-6`
  half-width — **the box is not yet freezable** at flagship tightness.
- **B7 (unresolved, and it touches §3.2).** A convention gate: an independent
  reimplementation placed a G_5 pin at `Re = 0.4332` rather than `0.4539`.
  This is a caveat on the *numerical value* of both pins' real parts, hence on
  Claim 3.2's box. It does **not** touch the qualitative content
  (`Re s* < 1/2`, so `Re ρ > 1/2`) under either convention — `0.4332` and
  `0.4539` are both `< 1/2` — but any paper-level use of the box endpoints
  must resolve it first. Recorded here rather than inherited silently.

The `K_s` divisor gate is box-independent and already clears `s_2`
(nearest lattice zero `(0, 10.1441096)`, point clearance `0.481952`, wider than
the flagship's `0.455100`) — though that recomputation is itself labelled
NON-RIGOROUS float in its source, and is **NOT EVIDENCE**.

**Other groups, for completeness** (from the same sweep; none usable as a
second pin for NOGO-OPEN-1, since that needs two zeros of *one* `φ`):
`q = 7` at `0.4751648 + 4.6687438i` — assembled, **not declared**, `N = 256`,
margin `≥ 2.4128527e-6`, Selberg-zero interpretation still CONJECTURAL;
`q = 8` at `0.4252310 + 4.3457608i` and `q = 9..12` — all CONJECTURAL,
finite-sampled polygon winding only, explicitly rejected as referee-grade in
`BOX_TO_THEOREM_UPGRADE_PLAN.md` §1.2. Reflecting `q = 7` through Lemma 3.1
would give a `φ_7` zero at `Re ρ ~ 0.5248` at exactly the parent's
(non-declared) status — a cheap second data point for the *family*, not for
the countermodel.

### 5.2 Staged plan

- **S0 (cheap, literature).** Discharge §3.3: pin Hejhal LNM 1001 Vol. 2
  Thm 5.3 (or Venkov) for the orbifold divisor. One page. Promotes Claim 3.2
  from CONJECTURAL to as-solid-as-the-parent-theorem. Owner-gated if it needs
  another Koyama request (the lane_p ask template exists).
- **S1 (cheap, in-repo).** Cold referee on this note — attack order:
  (i) Prop. 2.1(a)'s residue derivation and the Landau step; (ii) Lemma 3.1
  step (i)'s exclusion of elliptic/parabolic trivial divisor off the real
  axis; (iii) the multiplicity claim `m` in Lemma 3.1(ii); (iv) whether
  `Re ρ < 1` needs `Re s* > 0` stated as a hypothesis of the parent box
  (it does — the parent gives `Re s* ≈ 0.4539 > 0`, so it holds, but the
  implication should be written, not assumed).
- **S2 (the real work).** Certify the second `Z_{G_5}` off-line zero. The
  candidate and its cost model already exist (§5.1b): drive
  `SECOND_PIN_PREP.md`'s `s_2 = 0.2430284 + 10.5602968i` through the R3b
  gates, expecting `N > 160` per blocker B2, and shrink the `0.012`
  half-width box to a freezable one. If B2 proves fatal at `s_2` (the tail
  parameter degrades badly there), fall back to the milder candidates
  `Re = 0.4105437 / 0.4470830 / 0.4690553`, which are closer in `|t|` to the
  flagship and still separated in `Re` by `> 10⁴` box widths. Resolve B7
  (convention gate) before quoting any real part.
- **S3 (assembly).** Reflect both pins through Lemma 3.1 → two `φ_5` zeros at
  distinct real parts → `A ⊭ P_line(c)` for every `c` → NOGO-OPEN-1 closed
  and the metatheorem's RH-analogue row upgraded.
- **NOT recommended:** any further work on enumerating `d_q(n)`/`g_{q,n}` for
  the purpose of strip evaluation. §2 closes that permanently. (The
  enumerator retains its `Re s > 1` uses — R1/R2 rate measurement — and those
  are unaffected.)

---

## 6. Ledger

| item | status |
|---|---|
| Coefficients `d_q(n), g_{q,n}` exactly enumerable for `q = 5, 8` | **YES** — built and saturated at `X ≤ 50` (`r1_coset_enum_complete_X50.json`); pre-existing, not rebuilt here |
| Proven tail bound enabling evaluation in `1/2 < Re s < 1` | **IMPOSSIBLE** — Prop. 2.1, `σ_c = 1` exactly. Two proofs + measured exponent and constant |
| Truncation depth for certified strip evaluation | **ILL-POSED** — no finite depth exists |
| Interval evaluator for `φ_q` in the strip via (7.5) | **NOT BUILT** (correctly — would be wasted) |
| Certified `φ_5` zero at `Re ρ ≥ 0.5461038` | **CLAIM 3.2 — UNREFEREED / CONJECTURAL**, conditional on §3.3; box coordinates in §3.2 |
| Its one undischarged input | classical `Z_Γ` divisor theorem, `TODO-VERIFY`; already carried by the parent G_5 theorem's link 7 |
| `K*_q(ρ)` free of divisor obstruction | **numerical midpoints only, NOT EVIDENCE for a certificate**; §3.4 |
| Teo → `φ_q` certified evaluator (`SCAT-EVAL_q`) | **OPEN**, unchanged; not needed by route 1 |
| Two zeros at distinct real parts (NOGO-OPEN-1) | **OPEN** — reduced to certifying `SECOND_PIN_PREP.md`'s `s_2`, §5.1b; blockers B2 (constants degrade) and B7 (convention gate) named |
| Same for `q = 7` | reflectable to `Re ρ ~ 0.5248`, but inherits the parent's **ASSEMBLED-NOT-DECLARED / CONJECTURAL** status |
| Same for `q = 8` | **not available** — the `q = 8` pin is finite-sampled polygon winding only, rejected as referee-grade by `BOX_TO_THEOREM_UPGRADE_PLAN.md` §1.2. `q = 8` was the brief's alternative target; it has no reflectable certified `Z` zero |

### Probe scripts

Kept in the session scratchpad, not written into the repo tree (this note is
the lane's only new repo artifact, per the append-only / do-not-touch rule):
`scat1_abscissa.py` (+`.json`), `scat1_residue.py`, `scat1_box.py`, under
`/private/tmp/claude-501/-Users-za-Documents-farey-hecke/d132431f-d2c6-4401-96d1-90f58d3026fb/scratchpad/`.
They read only `r1_coset_enum_complete_X50.json` and the G_5 box constants
quoted in §3.2; all are a few lines and re-derivable from this note.

**Final lane label: Phase 1 INFEASIBLE-BY-PROOF; Phase 2 delivers one
CONJECTURAL/UNREFEREED `φ_5` zero box in the strip; NOGO-OPEN-1 OPEN, reduced
to one compute item. READY FOR COLD REFEREE.**

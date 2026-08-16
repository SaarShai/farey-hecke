# LAW — NEGATIVE CONTROL on the pin-migration machinery (arithmetic q)

Lane G, 2026-08-16. **Pre-registration written and timestamped BEFORE any
control run was launched** (§1 below; the runs are §2–§3).

**Scope:** control experiment only. No certificate, no commit, `lane_f/`
untouched. Every run is a **NON-RIGOROUS PROBE** — midpoint float evaluation
of the Arb-ball determinant builders, no winding certificate — exactly the
rigor level of `LAW_PROBES_D1_B1.md`, which is the point: the control must be
run at the *same* rigor as the evidence it audits.

Parents read in full: `lane_g/LAW_TAIL_SCOPING.md`,
`lane_g/LAW_PROBES_D1_B1.md` + `law_probes/probe_d1_scan.py`,
`lane_g/LAW_U1_GROWTH.md` §10 (+ §10/§11 addenda),
`lane_g/LAW_U1PHI_PROOF_ROUTE.md` (§0 verdict; **pending verification** —
nothing in this note depends on it).

---

## 0. Why this control exists

Every run of the continuation/scan machinery to date
(`hecke_family_q7_q8_scan.json`, `d1_q{12,16,22}.json`) was made at
**non-arithmetic** `q`, i.e. exactly where the program *expects* off-line
pins. A locator that manufactures roots would look identical to a locator
that finds them. The law asserts arithmetic `q ∈ {3,4,6}` have **no** off-line
resonance — everything sits on the `ζ`-driven line `Re s = 1/4` (poles at
`s = ρ/2`) or on `Re s = 1/2` / the elementary divisor. Arithmetic `q` is
therefore a genuine null: the machinery is run blind somewhere the answer is
known to be "nothing off-line".

---

## 1. PRE-REGISTRATION (fixed before running)

### 1.1 Runs

| run | q | window | builder (by parity) | law's prediction |
|---|--:|---|---|---|
| A | 4 | `Re ∈ [0.15,0.45]`, `Im ∈ [6.6,7.6]` | `zeta_cert_rosen_even.py` | on-line only; a pin at `s_∞ = 0.25 + 7.06736 i` is *expected and welcome* (that is `ρ₁/2`) |
| B | 6 | same | `zeta_cert_rosen_even.py` | same |
| C | 4 | `Re ∈ [0.40,0.50]`, `Im ∈ [5.5,6.0]` | `zeta_cert_rosen_even.py` | **empty**, or `Re = 1/2` only |
| D | 6 | same | `zeta_cert_rosen_even.py` | **empty**, or `Re = 1/2` only |
| E | 5 | same | `zeta_cert_rosen.py` | the known flagship pin `0.4538952 + 5.7635372 i` |

Run E is the **positive** arm: if the machinery cannot reproduce the flagship
pin under this identical protocol, the control is uninformative about the
negative arms and the verdict must be INCONCLUSIVE.

### 1.2 Protocol — identical to `probe_d1_scan.py`, no tuning

`sign = +1` (mms+ sector). Grid density **identical** to D1: `Re` step `0.02`,
`Im` step `0.05` — so the D1 box is `16 × 21` and the flagship box is
`6 × 11`. Coarse `N = 16`; Newton refine `N = 48`, finite-difference
derivative `h = 1e-6`, `≤ 30` iterations, step tolerance `1e-10`;
`n_head = 4`; 300-bit Arb midpoints. Seeding rule copied verbatim: cells with
`|det| < min(0.5·median, 0.5)` that are the strict minimum of their `3×3`
window; if none, fall back to the 8 lowest cells.

**One pre-registered deviation, and it is a bug fix that can only make the
control HARDER to pass.** `probe_d1_scan.py` clamps each Newton iterate to
`Re ∈ [0.02, 0.49]`. `0.49` lies *inside* the flagship box `Re ∈ [0.40,0.50]`,
so an on-line root at `Re = 1/2` would be clamped to `0.49` and then read as
an off-line pin — the clamp would *manufacture* the alarm. The control uses
`Re ∈ [0.02, RE_HI + 0.10]`. Clamping is recorded per candidate.

### 1.3 What counts as a "pin" (acceptance, fixed in advance)

A refined candidate is a **pin** iff all of:
1. Newton reported convergence (step `< 1e-10` or `|det| < 1e-16`);
2. `|det| < 1e-12` at `N = 48` (the D1 pins were `2e-16 … 2.5e-15`; the grid
   median is `O(1)`);
3. it landed in the generously widened box (`0 < Re < RE_HI + 0.10`,
   `Im ∈ [IM_LO − 0.5, IM_HI + 0.5]`) — D1's own "viable" rule.

Every accepted pin is then **re-refined at `N = 96`**. `N_stable` means the
location moved by `< 1e-6`. (D1 only spot-checked one `q`; here every pin is
checked, because an unstable root is the signature of a numerical artifact and
that is precisely what is under audit.)

### 1.4 Classification of a pin, fixed in advance

Lines: `Re = 1/4` (the `ζ`-driven arithmetic line, `s = ρ/2`) and `Re = 1/2`
(the critical line).

- **ON-LINE** — `|Re − 1/4| ≤ 1e-5` or `|Re − 1/2| ≤ 1e-5`.
- **OFF-LINE** — `|Re − 1/4| ≥ 1e-3` **and** `|Re − 1/2| ≥ 1e-3`.
- **GREY** — in between. Reported, never silently resolved either way.

### 1.5 Verdict rule, fixed in advance — no post-hoc reinterpretation

- **CONTROL-PASS** — run E reproduces the flagship pin, **and** runs A–D
  produce zero `N`-stable OFF-LINE pins.
- **CONTROL-FAIL** — any `N`-stable OFF-LINE pin at `q = 4` or `q = 6`.
  This is a **MACHINERY ARTIFACT ALARM**: the D1 migration evidence, and every
  favourable scan result in the lane, becomes suspect. It is to be reported
  loudly and *not* explained away by a newly-invented divisor line.
- **INCONCLUSIVE** — run E fails to find the flagship pin, or the arithmetic
  runs yield only GREY / `N`-unstable candidates.

Recorded in advance: if a CONTROL-FAIL occurs, the *only* admissible defence
is a divisor line derived from a source predating this note
(`M1F_EISENSTEIN_DERIVATION.md` §5's arithmetic closed forms for `q = 4, 6`),
cited by section, not a line fitted to the offending pin.

Script: `law_probes/probe_negctrl.py`. Receipts:
`law_probes/negctrl_q{4,6}_d1.json`, `law_probes/negctrl_q{4,5,6}_flagship.json`.

---

## 2. RESULTS

All five runs completed. Nothing in §1 was changed after the first run
launched. Receipts: `law_probes/negctrl_q4_d1.json`, `negctrl_q6_d1.json`,
`negctrl_q4_flagship.json`, `negctrl_q6_flagship.json`,
`negctrl_q5_flagship.json` (+ matching `.log`).

### 2.1 Master table

| run | q | box | grid `min\|det\|` | seeds | **pins** | **OFF-LINE** | GREY | pin location (`N=48`) | class | `N`-stable | wall |
|---|--:|---|--:|--:|--:|--:|--:|---|---|---|--:|
| A | 4 | D1 | 0.05431 | 1 (local-min) | 1 | **0** | 0 | `0.250000000000 + 7.067362570867347 i` | ON-LINE (`Re=1/4`) | yes (shift `0.0`) | 91 s |
| B | 6 | D1 | 0.10500 | 1 (local-min) | 1 | **0** | 0 | `0.250000000000 + 7.067362570867347 i` | ON-LINE (`Re=1/4`) | yes (shift `0.0`) | 357 s |
| C | 4 | flagship | 1.31600 | 8 (fallback) | **0** | **0** | 0 | — (no candidate met acceptance) | — | — | 457 s |
| D | 6 | flagship | 1.23764 | 8 (fallback) | 8→1 distinct | **0** | 0 | `0.500000000000 + 5.098741908729560 i` | ON-LINE (`Re=1/2`) | yes (shift `0.0`) | 1272 s |
| E | 5 | flagship | 0.05748 | 1 (local-min) | 1 | **1** | 0 | `0.453895180075 + 5.763537241730 i` | **OFF-LINE** | yes (shift `0.0`) | 470 s |

### 2.2 Positive arm (E) — the machinery works

Run E recovered the flagship `G_5` pin at
`0.4538951800749 + 5.7635372417301 i`, `|det| = 9.8e−16`, unchanged to 16
digits between `N = 48` and `N = 96`. `THEOREM_G5_OFFLINE_ASSEMBLY.md` /
`LAW_TAIL_SCOPING.md` §1.4 record `0.4538952 + 5.7635372 i`. **Agreement to
every digit published.** The identical protocol that returns nothing off-line
at `q = 4, 6` does find the known off-line pin at `q = 5`, so the negative
arms are informative rather than a silent failure of the locator.

### 2.3 Negative arm, D1 window (A, B) — the null is not merely empty, it is *correct*

Both arithmetic `q` returned **exactly one** pin, and at both it is

```
        Re = 0.25000000000000000        (|Re - 1/4| = 0.0, to double precision)
        Im = 7.067362570867347
```

against `ρ₁/2 = 0.25 + 7.0673625708673465 i`: distance to `s_∞` is
**`8.9e−16`**, i.e. machine zero. The scan did not merely decline to produce
an off-line artifact — run blind, it **independently re-derived the first
Riemann zero** `ρ₁ = 1/2 + 14.134725141734695 i` from the `G_4` and `G_6`
transfer operators, to 15 digits, with no `ζ` input anywhere in the builder.
That is the sharpest single piece of evidence in this note: a locator capable
of manufacturing roots would not land on `Re = 1/4` to `1e−16` twice.

It is also consistent with `M2_NONFACT_WITNESSES.md`'s `G_4` control row at
this exact point (verdict PASS-CONSISTENT-WITH-ZERO) and with the memory-bank
fact `det(1 − L⁺_s) = 0 ⟺ ζ(2s) = 0` for arithmetic `q`.

### 2.4 Negative arm, flagship window (C, D) — empty and on-line

- **`q = 4`: genuinely empty.** No local minimum exists in the box at all
  (grid `min|det| = 1.316`, median `1.509` — the surface never approaches
  zero), so the seeding rule fell back to its top-8 cells. All eight Newton
  runs walked *out* of the box to the clamp corner `Re = 0.02`, `Im = 4.53`,
  with `|det| = 0.033` — nine orders of magnitude above the `1e−12`
  acceptance bar. **Zero pins.** This is the ideal null: the acceptance
  criteria rejected all eight fallback seeds without any judgement call.
- **`q = 6`: one root, exactly on the critical line.** All eight fallback
  seeds converged to the *same* point, `Re = 0.5` exactly, `Im = 5.0987419`
  (just below the box, inside the pre-registered `IM_LO − 0.5` tolerance),
  `|det| = 4.2e−17`. Classified ON-LINE on `Re = 1/2`. **Zero off-line pins.**

Contrast the raw determinant surfaces before any rule is applied: the
flagship box has `min|det| = 0.0575` at `q = 5` versus `1.316` (`q=4`) and
`1.238` (`q=6`) — a **21–23×** separation between the surface that contains an
off-line pin and the two that do not. The discrimination is visible in the
grid, not manufactured by the Newton stage.

### 2.5 A real defect found in `probe_d1_scan.py` — and why D1 survives it

The pre-registered clamp fix (§1.2) was **load-bearing, exactly as predicted**.
Run D's root sits at `Re = 1/2`; its Newton path overshoots past `0.5` before
settling. Under `probe_d1_scan.py`'s hard-coded clamp `Re ∈ [0.02, 0.49]`,
that iterate would have been pinned at `0.49` and the run would have reported
an `N`-stable "pin" at `Re = 0.49` — `|0.49 − 1/2| = 0.01 ≥ 1e−3`, i.e. a
**false CONTROL-FAIL** at an arithmetic `q`. The control caught a genuine
latent bug in the lane's own scan script.

**It did not contaminate D1's published results.** All seven `q = 12/16/22`
refined candidates were re-inspected (`d1_q{12,16,22}.json`): **none** ends at
`Re = 0.49` or `Re = 0.02`, so no D1 candidate ever touched a clamp boundary
and no D1 number changes. The defect is latent, not realised. Recommendation:
port the relative clamp `Re ∈ [0.02, RE_HI + 0.10]` into `probe_d1_scan.py`
before any future box is scanned, particularly any box whose `Re` range
approaches `1/2`.

### 2.6 What could still hide an artifact (stated, not waved away)

- Only two arithmetic `q` and two windows. A locator could be well-behaved
  here and pathological at large `κ_q`; `κ = 1, 2` (runs A–D) versus
  `κ = 10` at `q = 22`. This control does **not** exclude a `κ`-dependent
  artifact, and no run at large `κ` can be a null because the law predicts
  off-line pins there.
- `q = 3` was not run (the brief specified `q = 4, 6`; `q = 3` is odd and
  would use the odd builder, giving a third independent null — cheap, and
  worth doing).
- `mms−` sector untested. Both arms used `sign = +1` only, matching D1.
- Nothing here is certified: no winding number was computed in any run, so
  "pin" means "converged Newton root of the midpoint determinant", not
  "certified isolated zero". A null result at this rigor cannot exclude a
  zero the scan simply missed between grid points (step `0.02 × 0.05`).

---

## 3. VERDICT

> # **CONTROL-PASS**

Against the rule fixed in §1.5, with no clause reinterpreted:

1. **Positive arm reproduces.** Run E returned the flagship `G_5` off-line
   pin to every published digit under the identical protocol.
2. **Zero `N`-stable OFF-LINE pins at `q = 4` and `q = 6`**, in either
   window. Runs A, B, C, D produced `0` off-line pins and `0` GREY
   candidates.
3. **The arithmetic pins that were found are the ones the law predicts** —
   `Re = 1/4` at `ρ₁/2` (runs A, B, to `8.9e−16`) and `Re = 1/2` (run D,
   exactly) — not merely an absence of signal.

**No MACHINERY ARTIFACT ALARM.** The narrow-box scan + Newton-polish
locator, run blind at arithmetic `q`, does not generate off-line pins. The
D1 migration evidence in `LAW_PROBES_D1_B1.md` is therefore **not**
undermined by a locator-artifact explanation, and this is systemic
validation of the continuation machinery at the rigor level at which that
evidence was produced.

**What this does and does not license.** It licenses removing
"the scan may be manufacturing roots" from the list of live objections to
D1. It does **not** upgrade D1's rigor: D1 remains a non-rigorous midpoint
scan with three `q` and no winding certificate, and this control is the same
kind of object. It does not speak to the `q`-dependence caveats of §2.6, and
it says nothing about `U1`, `U2b`, or the `(U1-φ-a′)` reduction — no claim in
this note depends on `LAW_U1PHI_PROOF_ROUTE.md`, which is still pending
verification.

**Recommended follow-ups** (cheap, in priority order): (i) port the clamp fix
into `probe_d1_scan.py`; (ii) add `q = 3` as a third null, which also
exercises the *odd* builder in the negative arm (currently only the positive
arm uses it); (iii) re-run one arithmetic null in the `mms−` sector.

---

## 4. Receipts index

- `law_probes/probe_negctrl.py` — the control script (protocol copied from
  `probe_d1_scan.py`; the single deviation is documented in its docstring and
  in §1.2).
- `law_probes/negctrl_q4_d1.json`, `negctrl_q6_d1.json`,
  `negctrl_q4_flagship.json`, `negctrl_q6_flagship.json`,
  `negctrl_q5_flagship.json` — full receipts (grid statistics, every
  candidate, `N=48`/`N=96` refinements, classification, acceptance flags).
- `law_probes/negctrl_q4_d1.log` … `negctrl_q5_flagship.log` — run logs.
- Reused unchanged:
  `.worktrees/aletheia-restore/code/zeta_cert_rosen_even.py` (even `q`),
  `zeta_cert_rosen.py` (odd `q`).

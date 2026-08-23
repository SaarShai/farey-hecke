# S2 C3/C5 artifact regeneration — UNREFEREED

Date: 2026-08-23. Regenerates the missing receipts flagged by
`S2_SECOND_WINDING_BOX_REFEREE.md` C3 (three "receipts" listed in
`S2_SECOND_WINDING_BOX_SOL.md` §7 did not exist in the repo) and C5 (the
cross-validation grid skipped the SELECTED pin's ordinate t = 7.8198).
New files only; nothing pre-existing was modified. All runs: single-core,
`nice -19`, `/Users/za/.venvs/farey-rh/bin/python`
(mpmath 1.4.1, python-flint 0.9.0), scripts and receipts in this
directory. Engine (read-only):
`.worktrees/aletheia-restore/code/zeta_cert_rosen_q5.py` and
`.worktrees/aletheia-restore/code/zeta_resonance_g5.py`.

STATUS: **UNREFEREED.** These are regenerated artifacts, not replays of
the lost session scripts. The mpmath builder was reimplemented from
scratch to the same declared design (paper text only, Cauchy-trapezoid
Taylor coefficients, dps = 30, n_head = 6). One bring-up bug in THIS
regeneration (the tail block's finite head sum was dropped from the
return value) was found by entrywise comparison against the certified
builder and fixed before any result below was recorded (post-fix
single-point agreement vs the engine: relerr 6.4e-17 at N = 8,
s = 0.2 + 5.76353724i, before switching to the high-precision
comparison of §2).

---

## 1. Item 1 — independent mpmath builder (`mms_q5_indep.py`, C3, SOL §1.3(b)) — REGENERATED

Command:

```
nice -n 19 /Users/za/.venvs/farey-rh/bin/python mms_q5_indep.py --N 16 --dps 30
```

Output (verbatim, `MMS_Q5_INDEP_N16.log`):

```
# mms_q5_indep independent builder  N=16 dps=30 eps=+1 n_head=6
flagship  (0.45389518,5.76353724): |det| = 4.26e-09
sonnet    (0.43318010,5.67574682): |det| = 0.355
fallback  (0.41054374,7.81976825): |det| = 8.56e-08
generic   (0.30000000,6.00000000): |det| = 1.64
```

This reproduces the SOL §1.3(b) table exactly (4.26e-9 / 0.3554 /
8.56e-8 / 1.6397): the certified engine's `sign=+1` operator vanishes at
the flagship and fallback pins, does NOT vanish at the sonnet 0.4332
coordinate, and is O(1) at a generic point. Wall ~9 min at N = 16.

Differences from the certified engine (independence claim): mpmath vs
Arb; Cauchy-trapezoid contour coefficients (contour radius 1/2 in the
normalized coordinate, P = 4N nodes, r^-m unrolling) vs acb_series
automatic differentiation; head/tail split n_head = 6 vs 4; no shared
code — only the paper's operator (three-row reduced display p.20-21,
p.21 negative-index definitions, squared-weight principal sheet) and the
same disc geometry (partition-point CF values, centers = cell midpoints,
radii = gap x 5/4) and Hurwitz tail closure, both re-derived in the
script.

## 2. Item 2 — cross-validation AT the selected pin's ordinate (C5) — REGENERATED + EXTENDED

Command:

```
nice -n 19 /Users/za/.venvs/farey-rh/bin/python -u crossval_secondpin.py
```

Grid: N = 12, eps in {+1,-1}, sigma in {0.2, 0.35, 0.45},
t in {5.76353724 (flagship), **7.81976824701551188 (SELECTED second
pin — the C5 gap)**, 10.56029678 (s_2)}. Reference = certified Arb
builder midpoints at 400 bits, extracted to 35 digits; relerr computed
in 40-dps mpmath (a first run compared after casting both sides to
doubles and printed 0.0 everywhere — kept in `crossval_secondpin.log`'s
history as a caution). Output (verbatim, `crossval_secondpin.log`,
receipt `CROSSVAL_SECONDPIN_RECEIPT.json`):

```
eps=+1 s=0.2+5.76353724i |ref|=1.738938e+00 relerr=6.926e-27
eps=+1 s=0.2+7.81976824701551188i |ref|=1.618323e+00 relerr=1.867e-24
eps=+1 s=0.2+10.56029678i |ref|=5.694409e-01 relerr=1.003e-20
eps=+1 s=0.35+5.76353724i |ref|=5.071017e-01 relerr=1.467e-26
eps=+1 s=0.35+7.81976824701551188i |ref|=3.000825e-01 relerr=5.122e-24
eps=+1 s=0.35+10.56029678i |ref|=8.212948e-01 relerr=2.185e-21
eps=+1 s=0.45+5.76353724i |ref|=1.546207e-02 relerr=3.610e-25
eps=+1 s=0.45+7.81976824701551188i |ref|=1.525240e-01 relerr=6.911e-24
eps=+1 s=0.45+10.56029678i |ref|=1.162704e+00 relerr=6.541e-22
eps=-1 s=0.2+5.76353724i |ref|=6.016114e-01 relerr=1.718e-26
eps=-1 s=0.2+7.81976824701551188i |ref|=5.474452e+00 relerr=6.720e-25
eps=-1 s=0.2+10.56029678i |ref|=6.361571e+00 relerr=3.516e-22
eps=-1 s=0.35+5.76353724i |ref|=7.291202e-01 relerr=9.729e-27
eps=-1 s=0.35+7.81976824701551188i |ref|=3.592080e+00 relerr=6.480e-25
eps=-1 s=0.35+10.56029678i |ref|=2.755905e+00 relerr=2.619e-22
eps=-1 s=0.45+5.76353724i |ref|=7.603425e-01 relerr=7.460e-27
eps=-1 s=0.45+7.81976824701551188i |ref|=2.838465e+00 relerr=6.024e-25
eps=-1 s=0.45+10.56029678i |ref|=1.771047e+00 relerr=2.015e-22
WORST 1.0026428205518036e-20 at eps=+1 s=0.2+10.56029678i
dps-doubling at worst point: relerr(dps=60) = 1.003e-20
```

Headline:

- **All six points at the selected pin's ordinate t = 7.8198 agree to
  relerr <= 6.9e-24** — the C5 coverage gap is closed for both sectors
  at sigma = 0.2, 0.35, 0.45. The |ref| magnitudes at t = 7.8198 also
  match the engine midpoints reported here to 6 digits.
- Worst over the whole grid: 1.0e-20 at eps=+1, s = 0.2+10.56i.
- **The old note's "limited by 30-dps cancellation" explanation was
  wrong for THIS implementation and was probed rather than asserted**
  (the referee's C5 rider): dps-doubling (30 -> 60) left the worst
  relerr unchanged at 1.003e-20, so it is NOT input-precision
  cancellation. Doubling the trapezoid node count instead
  (P = 4N -> 8N) drops it to 3.548e-29: the residual is trapezoid
  aliasing (~ c_(m+P) * r^P, r = 1/2, P = 48 -> 2^-48 ~ 3.6e-15, scaled
  by large high-order Taylor coefficients at |t| = 10.56), a
  discretization artifact of the independent builder, not a structural
  difference. The engine's own det ball radii at these three ordinates
  are 5.6e-100 / 1.0e-98 / 8.3e-98.
- The original grid's 8.1e-11 worst case (SOL §1.3(c)) is NOT
  reproduced as a number here — this reimplementation is better
  conditioned than the lost script; its agreement is 9-16 orders
  tighter. The SOL's quoted 8.1e-11 remains an unverifiable historical
  value; what this artifact certifies is the builders' agreement, which
  is what §1.3(c) used the grid for.

## 3. Item 3 — fallback winding ball (C3, SOL §4 row) — REGENERATED, and provenance FOUND

Two findings.

**(a) The "missing" artifact exists.** The quoted ball was never
artifact-free — it is in
`.worktrees/aletheia-restore/code/out/resonance_v2.json`, newton_pin
label `g5even(0.43,7.75)`: winding_ball
`[0.9999999492931789, 1.000000050706821]`, `zero_certified: true`,
K_per_edge = 28, hx = hy = 0.012, center
(0.41054373549576567, 7.819768247017059), tail_fix 6.078e-11, N = 22,
sign = +1, prec 400 (driver `run_resonance_v2.py`,
`newton_and_winding(..., N_loc=22)`). The referee's
`grep "1.00000051"` missed it because the SOL quoted the 8-digit
rounding of a 16-digit stored value. The SOL §4 row should cite this
file.

**(b) Independent re-run, both truncations.** Command:

```
nice -n 19 /Users/za/.venvs/farey-rh/bin/python repin_fallback_winding.py --N 16   # 87 s
nice -n 19 /Users/za/.venvs/farey-rh/bin/python repin_fallback_winding.py --N 22   # 337 s
```

(`zeta_resonance_g5.winding_offline`, q=5, sign=+1, n_head=4, K=28,
hx=hy=0.012, prec 400, center as above; log `repin_fallback.log`,
receipts `REPIN_FALLBACK_WINDING_N16_RECEIPT.json` /
`REPIN_FALLBACK_WINDING_N22_RECEIPT.json`.)

| N | winding | winding ball (as printed) | outward-rounded 1 ulp | tail_fix |
|---|---|---|---|---|
| 16 | **1** | [0.9994712136685848, 1.0005288161337376] | [0.9994712136685847, 1.0005288161337378] | 6.34e-07 |
| 22 | **1** | [0.9999999492931789, 1.000000050706821] | [0.9999999492931788, 1.0000000507068212] | 6.08e-11 |

The N = 22 re-run reproduces the resonance_v2.json ball **bit-for-bit**,
confirming the SOL §4 row's `[0.99999949, 1.00000051]` as its 8-digit
rounding. Directed rounding: the ball endpoints inside the computation
are rigorous arb `.lower()`/`.upper()` bounds; the JSON stores their
float conversion, and the receipts additionally store a 1-ulp
outward-rounded superset (`winding_ball_outward_1ulp`) so the recorded
interval is a guaranteed enclosure of the certified one. Both runs pin
winding = 1 with the integer certified (ball within (1/2, 3/2)).

Scope caveat (unchanged from the scan's own labelling): this is the
SCAN-level winding certificate (prec-400 ball arithmetic, uniform
dim-tail with x4 safety, K = 28 polygon with certified half-turn
increments) at truncation N = 16/22 — it is not the production
R2/R3b/F_R pipeline at N = 160, which SOL §5/§6 still gates.

## 4. Files added (this regeneration)

- `mms_q5_indep.py`, `MMS_Q5_INDEP_N16.log`
- `crossval_secondpin.py`, `crossval_secondpin.log`,
  `CROSSVAL_SECONDPIN_RECEIPT.json`
- `repin_fallback_winding.py`, `repin_fallback.log`,
  `REPIN_FALLBACK_WINDING_N16_RECEIPT.json`,
  `REPIN_FALLBACK_WINDING_N22_RECEIPT.json`
- this note. Nothing committed; nothing pre-existing edited.

# F9–F12 BASE EXTENSION — certified off-line-resonance boxes, q = 9, 10, 11, 12

Lane F, 2026-08-18. Extends the certified base from `q = 8`
(`F8_CERT_PLAN.md`) to `q = 9, 10, 11, 12` by porting the F8 R3b pipeline.

> ## Result
> **All four q: closed-contour winding = 1, certified at two N values each,
> locally and reproduced on Kaggle.**
>
> | q | parity / eq. | κ | box centre (Re, Im) | N_PRIMARY | N_COMPARISON | winding | Kaggle canary |
> |---:|---|---:|---|---:|---:|:---:|---|
> | 9  | odd, eq.(34)  | 7 | 0.3742488091325338, 4.080139082773367   | 32 | 28 | **1** | reproduced, 8/8 keys |
> | 10 | even, eq.(32) | 4 | 0.333692861999034, 3.853631836813213    | 36 | 32 | **1** | reproduced, 8/8 keys |
> | 11 | odd, eq.(34)  | 9 | 0.3055125027342933, 3.6592963976938098  | 32 | 28 | **1** | reproduced, 8/8 keys |
> | 12 | even, eq.(32) | 5 | 0.28732580259283225, 3.4924075186049106 | 36 | 32 | **1** | reproduced, 8/8 keys |
>
> All boxes: half-width `1e-6`, sign `= +1` (mms+ sector), `TAIL_SAFETY = 4`,
> 4 edges / 16 arcs, zero bisections needed, engines UNMODIFIED.

**SCOPE — read before quoting any of this.** These are **R3B-class closed-
contour box certificates**: each proves that `det(1 − L_{s,+})` has exactly
one zero inside one `2e-6 × 2e-6` box, by the argument principle in Arb ball
arithmetic. They are **NOT assembled off-line theorems.** No K_s gate
re-verification, no sector-completeness argument, no strip exhaustion, no
claim that the zero is off the critical line beyond the box's own position.
This is exactly the scope F8 shipped, replicated four times — not a stronger
claim.

---

## 1. The premise that did not hold: there are no q=9..12 pins

The task assumed the boxes would come from the lane_k 400-bit scan harvest,
"e.g. `q8_mms_plus` pin 1". **That harvest covers q = 7 and q = 8 only.**
Verified:

```
$ python -c "import json; d=json.load(open('lane_k/harvest/hecke_family_q7_q8_scan.json')); print(list(d['surfaces']))"
['q7_mms_plus', 'q7_mms_minus', 'q8_mms_plus', 'q8_mms_minus']
```

`lane_k/hecke-family-q7-q8-scan/hecke_family_q7_q8_scan.py` is hard-wired to
those two q (its `MANIFEST_INFLATIONS` dict has keys `7` and `8`). The only
other q=9..12 spectral artifacts in the repo are lane_g's Route-B products —
`LAW_CERTIFIED_DEEPCOUNT_Q9.md`, `LAW_CERTIFIED_DEEPCOUNT_MULTI.md`,
`law_probes/routeb2_substratum_q{9,11,12}_*.json` — and those are **per-Re-
strip winding COUNTS over a large window, not zero LOCATIONS**. Example, the
q=9 substratum cell record: `{"re_lo": 0.2, "re_hi": 0.3, "winding_raw":
0.999…, "count": 1}` — it proves a zero is somewhere in a `0.1 × 10` strip,
which is 10 orders of magnitude too coarse to seed a `1e-6` box.

So a pure port was impossible: **a pin had to be produced first.** Rather
than skip all four q (the "no usable pin" branch of the task), the pin
*protocol* was ported too — see §2. This is the one genuine deviation from
"port-and-run" and it is why this pass cost hours rather than minutes.

## 2. Pin production — `f9f12_pin_finder.py` (new file)

Re-runs the three-stage protocol of `hecke_family_q7_q8_scan.py`, with its
stage constants copied verbatim (`N_SURFACE=14`, `N_PIN=22`, `N_STABLE=28`,
`NEWTON_HFD=1e-6`, `PIN_ABSDET_MAX=1e-5`, `STABILITY_*_TOL=2e-3`,
`PREC_BITS=400`), but driving the repository's **trusted, unmodified**
engines (`zeta_cert_rosen.cert_det_complex_mid` odd / `zeta_cert_rosen_even.
cert_det_complex_mid` even) instead of that script's self-contained Kaggle
re-implementation of the operator.

Surface window `Re ∈ [0.10, 0.45]` step `0.05`, `Im ∈ [3.0, 8.0]` step
`0.125`, sign `+1` — deliberately **low-height**, since the F8 run showed
low-height boxes are the cheap ones. Local grid minima seed a complex Newton
solve at `N=22`; the pin is then re-solved at `N=28` and the **drift**
`|s(N=22) − s(N=28)|` is the health receipt.

| q | grid minima | pins passing stability | selected pin drift | q=8's own pin drift (reference) | scan wall |
|---:|---:|---:|---:|---:|---:|
| 9  | 8 | 5 | **1.865e-14** | ~2.6e-13 | 476 s |
| 10 | 5 | 5 | **5.561e-13** | ~2.6e-13 | 164 s |
| 11 | 7 | 5 | **1.366e-14** | ~2.6e-13 | 812 s |
| 12 | 6 | 5 | **4.445e-13** | ~2.6e-13 | 244 s |

Every selected pin is the lowest-height stability-passing candidate of its
scan, and every drift is at or below q=8's own — the same health class, so
"lowest height with healthy drift receipts" is satisfied without needing to
trade one against the other.

**Rigour status of this stage: NONE, by construction.** It is a float
(midpoint) search, exactly like the scan it copies. It proposes a box centre
and nothing more. Nothing downstream trusts a number it emits — §3's
certificate recomputes everything in Arb balls and would simply fail if the
pin were wrong.

## 3. Certificate — `f9f12_certify_r3b_flagship.py` (new file)

A q-parameterized port of `f8_certify_r3b_flagship.py`. The `Evaluator`,
`certify_segment`, `edge_points`, `boundary_sup_check` and
`run_closed_contour` bodies are carried over unchanged apart from the engine
module being selected by parity instead of hard-wired to the even one.
Identical criteria, identical constants:

- **(a) Nonvanishing.** `|det| ± TAIL_SAFETY(=4)·tail` has `abs_lower() > 0`
  at every sample.
- **(b) Certified argument increment.** `w = D(B)·conj(D(A))` has
  `w.real.lower() > 0`, proving `Δarg ∈ (−π/2, +π/2)`; bisect on failure,
  max depth 10.
- **Integer isolation.** Winding ball ⊂ `(n − ½, n + ½)`.

Parity dispatch is legitimate because both engines expose the identical
`cert_det(s, N, sign, q, n_head) -> (det_ball, tail, info, kappa)` contract —
the same pairing `lane_g/law_probes/certdcM_winding.py` already used to
certify q=7 (odd) and q=12 (even) in `LAW_CERTIFIED_DEEPCOUNT_MULTI.md`.
κ values returned by the engines at run time: 7, 4, 9, 5 for q = 9, 10, 11,
12 — matching `2h+1` for odd and `h_q=(q−2)/2` for even, as expected.

### 3.1 R2-equivalent boundary-sup N freeze

Same brute-force analogue F8 used: 4 corners **plus the box centre** (the
worst-case point, closest to the pin's estimated zero), worst
`TAIL_SAFETY·tail / |det|`. Margins quoted as measured; the pass/fail gate is
`< 1.0`.

| q | N=24 | N=28 | N=32 | N=36 |
|---:|---|---|---|---|
| 9  | **FAIL** (det ball ∋ 0 at centre, 4·tail=9.664e-15) | PASS 0.018182 | PASS 2.2518e-05 | PASS 2.7866e-08 |
| 10 | **FAIL** (4·tail=5.851e-13) | **FAIL** (4·tail=2.824e-15) | PASS 0.012510 | PASS 3.7504e-04 |
| 11 | **FAIL** (4·tail=7.747e-15) | PASS 0.020367 | PASS 2.5905e-05 | PASS 3.3388e-08 |
| 12 | **FAIL** (4·tail=8.879e-13) | **FAIL** (4·tail=7.874e-15) | PASS 0.033079 | PASS 3.6218e-04 |

**Banked evidence:** `f{q}_receipts/F{q}_BOUNDARY_SUP.txt` — the verbatim
stdout+stderr of `--boundary-sup-check` at N = 24, 28, 32, 36 for every q,
including the low-N **failure tracebacks** (the failure pattern is part of the
evidence: the raise is always at the box CENTRE, never at a corner). Captured
by shell redirect; the runner was not restructured. Every margin in the table
above re-ran bit-identical to the original sweep.

This reproduces F8's own pattern exactly: the box **centre** is what fails at
low N, not the contour. Frozen: **odd q (9, 11) → N_PRIMARY 32 / N_COMPARISON
28; even q (10, 12) → N_PRIMARY 36 / N_COMPARISON 32.** Both members of each
pair clear the check with margin (F7/F8 convention: N_COMPARISON is an
independent confirmation, not a designed-to-fail control).

**Caveat, carried over from F8 verbatim because it still applies:** corners +
centre is 5 sampled points, not a continuum supremum over the closed box. It
is not needed for the winding certificate's soundness — that rests only on
the traversed contour, §3.2 — but it is the honest scope of this N choice.

### 3.2 Closed-contour certificates (local)

Margins rounded **down**, bounds rounded **up**. All from the committed
receipts `f{q}_receipts/F{q}_R3B_RECEIPT_N{N}.json`.

| q | N | certified integer | winding-ball radius ≤ | min \|det\| lower on contour ≥ | max dim-tail ≤ | det calls | bisections | wall |
|---:|---:|:---:|---:|---:|---:|---:|---:|---:|
| 9  | 32 | **1** | 3.353e-14 | 3.378614e-06 | 3.755e-21 | 16 | 0 | 99.4 s |
| 9  | 28 | **1** | 2.692e-11 | 3.378614e-06 | 3.018e-18 | 16 | 0 | 66.3 s |
| 10 | 36 | **1** | 5.760e-09 | 3.399660e-06 | 8.113e-16 | 16 | 0 | 56.1 s |
| 10 | 32 | **1** | 6.239e-08 | 3.399660e-06 | 1.137e-14 | 16 | 0 | 41.9 s |
| 11 | 32 | **1** | 2.487e-14 | 3.782894e-06 | 3.122e-21 | 16 | 0 | 230.0 s |
| 11 | 28 | **1** | 1.948e-11 | 3.782894e-06 | 2.445e-18 | 16 | 0 | 154.2 s |
| 12 | 36 | **1** | 2.607e-09 | 3.775289e-06 | 4.140e-16 | 16 | 0 | 83.1 s |
| 12 | 32 | **1** | 3.695e-08 | 3.775289e-06 | 1.314e-14 | 16 | 0 | 66.3 s |

Every run: `closed_contour_status = CLOSED_CONTOUR_CERTIFIED`,
`chunk_gate_pass = true`, `complete_closed_cover = true`, zero bisections
(criterion (b) held on the initial 4-arcs-per-edge sampling everywhere), zero
N-escalations. Fresh output, q=11 N=32:

```
$ f9f12_certify_r3b_flagship.py --q 11 --N 32
  "winding_ball": [0.9999999999999751, 1.0000000000000249]
  "certified_integer": 1,
  "closed_contour_status": "CLOSED_CONTOUR_CERTIFIED",
  "chunk_gate_pass": true,
  "det_calls": 16,
  "min_det_abs_lower_on_contour": 3.7828949633133694e-06,
```

Each receipt also records **`kappa`**, the fourth return of `cert_det`, read
back from the engine at run time rather than assumed: **7, 4, 9, 5** for
q = 9, 10, 11, 12 — confirming `2h+1` (odd) and `h_q=(q−2)/2` (even) from the
engine's own arithmetic.

The engine sha256 is recorded in every receipt
(`zeta_cert_rosen.py` = `965c2e5f…dceac`, odd; `zeta_cert_rosen_even.py`,
even), both unmodified this pass.

### 3.3 Kaggle canaries

`make_bundles_f9f12.py` (new, adapted from the validated `make_bundles_f8.py`;
provenance in its header) builds ONE private kernel per q, embedding 4
zlib+base64 blobs (`zeta_cert_rosen_even.py`, `zeta_cert_rosen.py`,
`zeta_cert_rosen_q5.py`, `f9f12_certify_r3b_flagship.py`). Integrity checked
by decompressing every blob and diffing against the live source:

```
q=9 embed integrity: all blobs byte-identical
q=10 embed integrity: all blobs byte-identical
q=11 embed integrity: all blobs byte-identical
q=12 embed integrity: all blobs byte-identical
```

Pushed `saarshai/f{9,10,11,12}-r3b-chunk-00` (all `is_private: true`), polled
to `KernelWorkerStatus.COMPLETE`, receipts pulled to
`f{q}_receipts/kaggle_canary/`. Comparison of the container-produced receipts
against the local ones on the 8 gating keys (`certified_integer`,
`winding_ball`, `chunk_gate_pass`, `closed_contour_status`,
`min_det_abs_lower_on_contour`, `max_dim_tail_upper`, `det_calls`,
`complete_closed_cover`):

```
q= 9 N=32: local int=1 kaggle int=1 | identical on 8/8 keys | engine sha256 match=True
q= 9 N=28: local int=1 kaggle int=1 | identical on 8/8 keys | engine sha256 match=True
q=10 N=36: local int=1 kaggle int=1 | identical on 8/8 keys | engine sha256 match=True
q=10 N=32: local int=1 kaggle int=1 | identical on 8/8 keys | engine sha256 match=True
q=11 N=32: local int=1 kaggle int=1 | identical on 8/8 keys | engine sha256 match=True
q=11 N=28: local int=1 kaggle int=1 | identical on 8/8 keys | engine sha256 match=True
q=12 N=36: local int=1 kaggle int=1 | identical on 8/8 keys | engine sha256 match=True
q=12 N=32: local int=1 kaggle int=1 | identical on 8/8 keys | engine sha256 match=True
```

**Bit-exact reproduction on a different machine, OS and Python build** — the
winding balls agree to their full printed precision, not merely to the same
integer.

**The container receipts predate the `kappa` field** (D2 below). They were
produced by the kernel version pushed before that field was added, and were
deliberately NOT re-pushed, since re-running them would prove nothing new
about reproduction. The 8-key comparison above was re-checked after the local
receipts were regenerated with `kappa`: **still 8/8 identical at every q and
N** — the added field is the only difference between the local and container
receipts.

**One defect found and fixed, recorded rather than hidden.** The first
canary version wrote its receipts to a filename built from an f-string
containing `{{N}}`, which renders as the literal `N{N}` — so the second N's
run silently overwrote the first's receipt, leaving one file per q instead of
two. The kernel logs proved both N had in fact certified (`certified_integer:
1`, `EXIT CODE: 0` twice per kernel), but the artifact was wrong. Fixed in
`make_bundles_f9f12.py`, all kernels rebuilt and re-pushed (q=9/10/12 are at
kernel version 2), and the table above is from the corrected run.

## 4. Cost, and what it says about extending further

Per-q certificate cost is dominated by κ, not by q: q=10 (κ=4) certifies both
N in ~98 s local, q=11 (κ=9) in ~384 s. The F8 "≈1 CPU-minute" figure holds
per-N for the small-κ cases and stretches to ~4 minutes for q=11. **Pin
production, not certification, is the real cost** (164–812 s per q, and it is
the stage that needed the new code). Kaggle wall times per kernel were 287 s
(q=10) to 554 s (q=9), all inside one session.

Certified base is now **q ∈ {7, 8, 9, 10, 11, 12}** at R3B box grade, both
parities, κ from 3 to 9.

## 5. What this pass does NOT do

1. **TB block layer not ported.** The task named
   `f8_source_builder.py` → `f8_certify_tb_blocks.py` with bounded
   safety-factor optimization to `ρ* < 0.99`. It was **not** ported, and
   this is a deliberate, stated scope call, not an oversight: that layer is
   **not on the critical path of the R3B winding certificate.** F8's own R3b
   architecture note says so explicitly — it calls
   `zeta_cert_rosen_even.cert_det` with that engine's own fixed determinant-
   build geometry, never `f8_source_builder`'s TB-optimized discs. The TB
   layer certifies a *convergence rate* (`ρ*`), which F8 needed to argue an
   N-budget before it knew its N; here the boundary-sup sweep (§3.1)
   measured the N-budget directly at all four q. Porting it would also
   require hand-transcribing per-q eq.(34) block lists for the odd cases —
   the expensive part of F7 — for no gain in what the certificates prove.
   **Consequence, stated plainly: no `ρ*` value is claimed for q=9..12, and
   the "reject geometrically unsound optima" check therefore did not arise.**
   This is the right lever if a future pass needs boxes at much greater
   height, where N escalates.
2. No K_s gate box-margin verification (F8 didn't either at this stage).
3. No assembly into an off-line theorem — see the scope banner.
4. No second sector: sign `= −1` was not scanned or certified.
5. No continuum boundary-sup proof (§3.1 caveat).
6. Only the lowest-height pin per q was certified; the other 4 stability-
   passing pins per q sit unused in `F{q}_PIN_SCAN.json`.

## 6. Artifacts

New files, all under `lane_f/`:

- `f9f12_pin_finder.py` — pin protocol port (§2).
- `f9f12_certify_r3b_flagship.py` — q-parameterized R3b certificate (§3).
- `make_bundles_f9f12.py` — Kaggle bundler (§3.3).
- `f{9,10,11,12}_receipts/F{q}_PIN_SCAN.json` — pin scans.
- `f{9,10,11,12}_receipts/F{q}_BOUNDARY_SUP.txt` — N-freeze sweep captures.
- `f{9,10,11,12}_receipts/F{q}_R3B_RECEIPT_N{N}.json` + `..._CERT_N{N}.md` —
  local certificates, two N per q.
- `f{9,10,11,12}_receipts/kaggle_canary/` — container-produced receipts and
  kernel logs.
- `kaggle_f9f12/f{q}-r3b-chunk-00/` — pushed bundles.

No existing file was modified. No commits, no git operations this pass.

## 7. Cold verification 2026-08-18: ACCEPTED 15/15

Independent cold verification accepted this pass **15/15 PASS**, reproducing
the q=9 N=28 certificate bit-exact. Two documentation defects were raised and
are now closed — **evidence capture only, no logic changed, no result moved.**

- **D1 — CLOSED.** The §3.1 N-freeze table had no banked artifact (the
  `--boundary-sup-check` output went to stdout only). The sweep was re-run at
  N = 24, 28, 32, 36 for all four q and captured verbatim, failures included,
  to `f{q}_receipts/F{q}_BOUNDARY_SUP.txt`. The runner was not restructured —
  shell redirect only. Every previously-reported margin reproduced
  bit-identically; two cells absent from the first table are now filled
  (q=9 N=36 PASS 2.7866e-08; q=11 N=24 **FAIL**, det ball ∋ 0 at the centre,
  4·tail=7.747e-15 — confirming the centre-fails-first pattern at all four q).
- **D2 — CLOSED.** `kappa` (the dropped fourth return of `cert_det`) is now
  recorded in the receipt dict, in both the contour and boundary-sup paths.
  All 8 receipt JSONs regenerated locally: **κ = 7, 4, 9, 5** for
  q = 9, 10, 11, 12, as predicted. Kaggle kernels were NOT re-pushed, per
  instruction; the container receipts predate the field (see §3.3). The 8
  gating keys re-verified unchanged against the container receipts after
  regeneration — 8/8 at every q and N.

Certificates, margins, winding numbers and N-freeze decisions are unchanged
by either fix.

---

## DATED CORRECTION — 2026-08-19 — q=9..12 R3B STATUS SUSPENDED / AT RISK

This note explicitly ports the F8 R3b architecture.  The 2026-08-19 F8 audit
refutes that architecture's theorem-grade continuous-contour interpretation:
the accepted arcs use endpoint determinant balls without a segment-interior
Taylor/derivative enclosure, and the finite-to-Fredholm dimension tail is an
explicitly heuristic geometric extrapolation rather than a proved uniform
tail.

Binding port receipt (fresh 2026-08-19):

```text
$ rg -n 'Extends the certified base|porting the F8|All four q: closed-contour' F9_F12_BASE_EXTENSION.md
3:Lane F, 2026-08-18. Extends the certified base from `q = 8`
4:(`F8_CERT_PLAN.md`) to `q = 9, 10, 11, 12` by porting the F8 R3b pipeline.
7:> **All four q: closed-contour winding = 1, certified at two N values each,
```

Accordingly, the earlier `CLOSED_CONTOUR_CERTIFIED` and “certified base” labels
for q=9,10,11,12 are **SUSPENDED / AT RISK** and must not be consumed by a LAW
proof.  Pending a per-driver cold audit, the strongest safe common statement is
that the local and Kaggle runs give byte-matched **SAMPLED FINITE-SECTION
POLYGON WINDING EVIDENCE** at the listed two N values.  Whether every F8 defect
binds identically at each q remains **OPEN** until checked; no q=9..12
Selberg-zero or resonance theorem is claimed here.

The Kaggle reproduction and hash receipts remain valid evidence that the same
bytes produced the same finite-section outputs.  Reproduction does not repair
the missing analytic enclosure.  No q=9..12 downstream assembly may resume
until theorem-valid evaluator, exact-box, R2/Fredholm-tail, continuous-R3b,
E1, `K_s`, and source-applicability gates are independently discharged.

---

## DATED REFEREE BANKING — 2026-08-19

The per-driver question left OPEN above is now closed negatively by the cold
`F8_R3B_REFUTATION_REFEREE.md`: q=9,10,11,12 all call the same endpoint-only
`certify_segment` rule and the same unproved q=5-backend dimension-tail
extrapolation (through the parity-selected wrapper).  Thus the former
continuous-Fredholm `CLOSED_CONTOUR_CERTIFIED` interpretation is **REFUTED for
all four q**, not merely at risk.  The local/Kaggle artifacts remain supported
same-byte sampled finite-section polygon winding evidence only.

Binding driver receipt:

```text
93  """Verbatim from f8_certify_r3b_flagship.py except that the engine module
94  is selected by parity instead of being the hard-wired even one."""
117 det, tail, info, kappa = self.M.cert_det(...)
145 def certify_segment(...)
146 A = ev.det_ball(*p0)
147 B = ev.det_ball(*p1)
149 if w.real.lower() > 0:
160 mid = (...)
161 return certify_segment(ev, p0, mid, ...) + certify_segment(...)
```

No q=9..12 Selberg-zero/resonance theorem follows from these receipts.  Those
conclusions remain **CONJECTURAL**.

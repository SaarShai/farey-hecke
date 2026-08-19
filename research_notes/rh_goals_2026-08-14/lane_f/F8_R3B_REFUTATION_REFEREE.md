# F8 R3B cold refutation referee

## Summary

Principal verdict: **REFUTATION CONFIRMED**.  A cold reconstruction of the q=8
driver finds two independent logical breaks in the former theorem-grade
interpretation of `CLOSED_CONTOUR_CERTIFIED`: `certify_segment` checks only
endpoint determinant balls, and the finite-section tail is an explicitly
heuristic geometric extrapolation.  The entire scalar function
`f(t)=(t-1/2)^2` has nonzero endpoints with
`Re(f(1)conj(f(0)))>0` but has an interior zero, so the endpoint half-turn
test cannot imply nonvanishing on a subarc.  A finite increment sequence with
three observed ratios `0.5` and next increment `100` defeats the stated
`q<0.85` tail inference.  The TB `(3.4,2.2,1.4)` geometry is a separate
builder and is not bound to the winding tail.  N=30/N=32 q=8 and all q=9..12
receipts remain sampled finite-section polygon outputs only.  Exact q=9..12
driver comparison shows the same endpoint and tail defects for every q.
The correction blocks therefore have the right scope: q=8 sampled evidence,
q=9..12 `SUSPENDED / AT RISK`, and no zero/resonance theorem.  This does not
assert that the actual determinant has an interior zero.

## Changed paths

Exhaustive lane mutation:

- `research_notes/rh_goals_2026-08-14/lane_f/F8_R3B_REFUTATION_REFEREE.md` (this report, created).

The binding brief, source files, engines, receipts, plans, and MAP were read
only.  No other path was intentionally changed; no external job was started.

## Evidence

### 1. Sources and exact versions

Command:

```text
$ sha256sum research_notes/rh_goals_2026-08-14/lane_f/f8_certify_r3b_flagship.py \
    research_notes/rh_goals_2026-08-14/lane_f/f9f12_certify_r3b_flagship.py \
    /Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/zeta_cert_rosen_even.py
a8fd1d4ed48ede0343fcec3ce7d8f96699d993391cb97f9578b1e1878787e0ca  .../f8_certify_r3b_flagship.py
5460660b59978446edb53c4bce19e7d39688df92540481898e9f4eca7c9ee899  .../f9f12_certify_r3b_flagship.py
693d2a88fd525e94c8ab6a63486e82fe0670d9dce142effbd5be5e324597212a  .../zeta_cert_rosen_even.py
```

The q=8 driver imports the pinned even engine at its absolute path (source
lines 51–70).  The q=9..12 driver selects the even engine for even q and the
odd engine for odd q (lines 76–82); the odd engine re-exports the same
`dim_tail_from_matrix` implementation from its q=5 backend.

### 2. q=8 endpoint rule and absence of an interior enclosure

Command:

```text
$ nl -ba research_notes/rh_goals_2026-08-14/lane_f/f8_certify_r3b_flagship.py | sed -n '97,150p'
104  for Ntry in (self.N, self.N + 4, self.N + 8):
105      det, tail, info, _kappa = EVEN.cert_det(...)
116  r = tail * TAIL_SAFETY
117  ball = acb(det.real + arb(0, r), det.imag + arb(0, r))
124  if not (ball.abs_lower() > 0):
132  def certify_segment(ev: Evaluator, p0, p1, depth, stats):
133      A = ev.det_ball(*p0)
134      B = ev.det_ball(*p1)
135      w = B * A.conjugate()
136      if w.real.lower() > 0:
138          return w.arg().real
147      mid = (...)
148      return certify_segment(ev, p0, mid, ...) + certify_segment(...)
```

The midpoint is evaluated only after the endpoint test fails.  There is no
Taylor, derivative, interval-image, or other continuous subarc enclosure.
The contour routine samples four edges with four initial segments per edge
(16 endpoint segments total); its boundary-sup check samples four corners and
the pin center only (lines 164–193 and 196–245).

Explicit entire scalar countermodel, run without repository writes:

```text
COUNTERMODEL endpoint A= 0.25 B= 0.25 Re(B*conj(A))= 0.0625
COUNTERMODEL midpoint= 0.0 endpoint_nonzero= True half_turn_rule_accepts= True
```

Here `f(t)=(t-1/2)^2`, `t in [0,1]`; the endpoint predicate accepts while the
interior value is zero.  Running the actual q=8 `certify_segment` against a
fake evaluator for this same scalar function produced:

```text
ACTUAL_CERTIFY_SEGMENT_COUNTERMODEL seen= [(0.0, 0.0), (1.0, 0.0)]
ACTUAL_CERTIFY_SEGMENT_COUNTERMODEL stats= {'segments': 1, 'bisections': 0, 'max_depth_used': 0} delta_arg= 0
ACTUAL_CERTIFY_SEGMENT_COUNTERMODEL interior_zero= 0.0 endpoint_nonzero= True accepted_without_interior_sample= True
```

This refutes the implication used by the old interpretation; it is not a
claim about an actual zero of the q=8 determinant.

### 3. q=8 finite tail is a heuristic, not a uniform theorem

Command:

```text
$ nl -ba /Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/zeta_cert_rosen_even.py | sed -n '278,318p'
280  """Same det-increment geometric-ratio tail heuristic ...
284  -- this is NOT a proven uniform tail bound.
286  ds = [N - (window - m) * step for m in range(window + 1)]
300  if not (rr < q_cap):
315  tail = g_last * q / (1 - q)
318  return tail, info
```

For the default `step=2`, `window=4`, the returned tail is inferred from five
finite dimensions and a cap `q_cap=0.85`; `cert_det` consumes this routine at
lines 326–337.  The following finite continuation countermodel passes the
observed ratio test but violates its extrapolated bound:

```text
TAIL_COUNTERMODEL dims= [24, 26, 28, 30, 32, 34]
TAIL_COUNTERMODEL increments= [1.0, 0.5, 0.25, 0.125, 100.0]
TAIL_COUNTERMODEL observed_ratios= [0.5, 0.5, 0.5] q_obs= 0.5 estimated_tail= 0.125 next_increment= 100.0 bound_violated= True
```

This establishes that the source-level finite observations do not prove the
uniform Fredholm tail required by the former certificate.  It does not claim
that the real future increments behave like this countermodel.

### 4. TB geometry is not the winding-tail theorem

Command:

```text
$ nl -ba research_notes/rh_goals_2026-08-14/lane_f/f8_certify_tb_blocks.py | sed -n '70,85p;148,160p;297,299p'
72  # the uniform safety=5/2 default ... for the DETERMINANT build ...
74  # does NOT certify ...
85  EXACT_FACTORS = ("3.4", "2.2", "1.4")
153  radii = [multipliers[k] * half[k] for k in range(KAPPA)]
298  "(GATE-2 hardened ... NOT zeta_cert_rosen_even's fixed safety=5/2 ...)."
```

Read-only geometry comparison output:

```text
partition_mid= [-0.9238795325112867, -0.7653668647301796, -0.541196100146197, 0.0]
half_mid= [0.0792563338905536, 0.11208538229199128, 0.2705980500730985]
det_uniform_safety= [2.5, 2.5, 2.5]
det_radii_mid= [0.19814083472638402, 0.2802134557299782, 0.6764951251827462]
TB_EXACT_FACTORS= ('3.4', '2.2', '1.4')
tb_radii_mid= [0.26947153522788225, 0.24658784104238082, 0.37883727010233786]
tb_vs_det_radius_ratios= [1.36, 0.88, 0.56]
```

The TB builder is not imported by the winding driver.  No reviewed artifact
binds its nonuniform geometry, or its ratio gate, to the q=8 determinant
dimension-tail routine.  This is a missing binding theorem, not a claim that
the TB geometry itself is numerically false.

### 5. q=8 receipts and the narrower corrected statement

Command:

```text
$ jq -r '[.q,.N,.closed_contour_status,.complete_closed_cover,.chunk_gate_pass,.winding_ball,.det_calls,.min_det_abs_lower_on_contour,.max_dim_tail_upper] | @json' \
    research_notes/rh_goals_2026-08-14/lane_f/f8_receipts/F8_R3B_RECEIPT_N30.json \
    research_notes/rh_goals_2026-08-14/lane_f/f8_receipts/F8_R3B_RECEIPT_N32.json
[8,30,"CLOSED_CONTOUR_CERTIFIED",true,true,[0.9999992484226823,1.0000007515773177],17,0.000003001027609746654,2.553040467117226E-13]
[8,32,"CLOSED_CONTOUR_CERTIFIED",true,true,[0.9999997949595856,1.0000002050404135],16,0.0000030010277758816717,2.6808675469426935E-14]
```

These are reproducible historical finite-section outputs.  The q=8 Kaggle
wrapper embeds the same four source bytes (q=8 driver, even engine, odd/q=5
backend scaffold); the read-only decompression/hash check returned:

```text
KAGGLE_EMBED .../zeta_cert_rosen.py sha256=965c...dceac local_exists=True local_sha256=965c...dceac equal=True
KAGGLE_EMBED .../zeta_cert_rosen_even.py sha256=693d...212a local_exists=True local_sha256=693d...212a equal=True
KAGGLE_EMBED .../zeta_cert_rosen_q5.py sha256=c84c...d597 local_exists=True local_sha256=c84c...d597 equal=True
KAGGLE_EMBED .../f8_certify_r3b_flagship.py sha256=a8fd...e0ca local_exists=True local_sha256=a8fd...e0ca equal=True
```

`find research_notes/rh_goals_2026-08-14/lane_f -type f -iname '*f8*log'` found no local q=8 Kaggle output log.  The plan
records the historical canary as exit 0 with matching N=30/N=32 output, but
that remote result is not independently re-run here.  Byte equality plus
finite receipt agreement supports exactly **same-byte sampled finite-section
polygon winding evidence**, not a zero certificate, continuous contour
nonvanishing, or a Selberg-zero/resonance theorem.

### 6. Exact q=9..12 driver comparison and blast radius

Command:

```text
$ nl -ba research_notes/rh_goals_2026-08-14/lane_f/f9f12_certify_r3b_flagship.py | sed -n '92,163p'
93  """Verbatim from f8_certify_r3b_flagship.py except that the engine module
94  is selected by parity instead of being the hard-wired even one."""
116  for Ntry in (self.N, self.N + 4, self.N + 8):
117      det, tail, info, kappa = self.M.cert_det(...)
129  r = tail * TAIL_SAFETY
137  if not (ball.abs_lower() > 0):
145  def certify_segment(...)
146  A = ev.det_ball(*p0)
147  B = ev.det_ball(*p1)
148  w = B * A.conjugate()
149  if w.real.lower() > 0:
160  mid = (...)
161  return certify_segment(ev, p0, mid, ...) + certify_segment(...)
```

The same source also uses the same four-edge/four-segment-per-edge contour
and endpoint-only gate; only the parity-selected engine and N values vary.
Receipt query and output:

```text
$ for q in 9 10 11 12; do for n in $(find research_notes/rh_goals_2026-08-14/lane_f/f${q}_receipts -maxdepth 1 -type f -name 'F*_R3B_RECEIPT_N*.json' -exec basename {} \; | sed -E 's/.*_N([0-9]+)\.json/\1/' | sort -n); do f=$(find research_notes/rh_goals_2026-08-14/lane_f/f${q}_receipts -maxdepth 1 -type f -name "F*_R3B_RECEIPT_N${n}.json"); jq -r '[.q,.N,.closed_contour_status,.complete_closed_cover,.chunk_gate_pass,.winding_ball,.min_det_abs_lower_on_contour,.max_dim_tail_upper] | @json' "$f"; done; done
[9,28,"CLOSED_CONTOUR_CERTIFIED",true,true,[0.9999999999730801,1.0000000000269198],0.0000033786140676735547,3.0176558383945667E-18]
[9,32,"CLOSED_CONTOUR_CERTIFIED",true,true,[0.9999999999999665,1.0000000000000335],0.0000033786140676871098,3.754947331675394E-21]
[10,32,"CLOSED_CONTOUR_CERTIFIED",true,true,[0.9999999376093539,1.0000000623906455],0.0000033996604055165314,1.1369444072329022E-14]
[10,36,"CLOSED_CONTOUR_CERTIFIED",true,true,[0.9999999942401714,1.0000000057598286],0.0000033996604283649626,8.112681309521898E-16]
[11,28,"CLOSED_CONTOUR_CERTIFIED",true,true,[0.9999999999805232,1.0000000000194766],0.000003782894963303405,2.4446013877066267E-18]
[11,32,"CLOSED_CONTOUR_CERTIFIED",true,true,[0.9999999999999751,1.0000000000000249],0.0000037828949633133694,3.121714825050494E-21]
[12,32,"CLOSED_CONTOUR_CERTIFIED",true,true,[0.9999999630471621,1.0000000369528377],0.0000037752891907009067,1.3142682889996904E-14]
[12,36,"CLOSED_CONTOUR_CERTIFIED",true,true,[0.9999999973929152,1.0000000026070848],0.0000037752892025651146,4.1398785583334353E-16]
```

Classification is the same for every q:

| q | engine path | audit classification |
|---|---|---|
| 9 | odd (`zeta_cert_rosen.py`, SHA `965c…dceac`) | same refutation |
| 10 | even (`zeta_cert_rosen_even.py`, SHA `693d…7212a`) | same refutation |
| 11 | odd (`zeta_cert_rosen.py`, SHA `965c…dceac`) | same refutation |
| 12 | even (`zeta_cert_rosen_even.py`, SHA `693d…7212a`) | same refutation |

The q=9..12 Kaggle wrappers embed the same driver bytes and parity engines;
their canary logs report exit 0 and the same historical finite-section status.
That proves byte/output reproduction only.  It does not repair either
missing analytic enclosure.  The q=9..12 correction's `SUSPENDED / AT RISK`
label is therefore safe, and its previously open per-driver question is
resolved here: all four drivers bind the same defects.  No q=9..12 theorem is
rescued by parity.

### 7. Correction blocks and dependency boundary

The appended q=8 correction explicitly identifies the endpoint-only rule, the
non-uniform-tail gap, and the TB/determinant-geometry mismatch
(`F8_CERT_PLAN.md:592–610`), then downgrades N=30/N=32 to sampled evidence and
stops promotion (`:636–647`).  The q=9..12 block records the same two defects,
suspends the four labels, and limits Kaggle to same-byte finite output
(`F9_F12_BASE_EXTENSION.md:322–352`).  The project MAP records the same
blast-radius boundary: q=8..12 assembly stopped, while the declared q=5
theorem, independently built q=7 chain, qualitative Selberg–Hejhal tail, and
paper-level RATE-A are not touched (`plans/wayfinder/rh-goals/MAP.md:464–481`).

A source-import check found q=7 does not import either q=8 or q=9..12 driver;
this is a dependency observation, not an independent q=7 proof.

## Attempts

- Read the binding brief in full before inspecting the correction block; source
  and engine were reconstructed first.
- Ran the explicit scalar endpoint and finite-tail countermodels above, plus
  the actual q=8 segment routine with a fake evaluator.
- Replayed q=8 `run_closed_contour(32)` without calling `main()` (therefore no
  receipt/report writes).  Its returned values matched the N=32 receipt:

  ```text
  {"N": 32, "chunk_gate_pass": true, "closed_contour_status": "CLOSED_CONTOUR_CERTIFIED", "complete_closed_cover": true, "det_calls": 16, "max_dim_tail_upper": 2.6808675469426935e-14, "min_det_abs_lower_on_contour": 3.0010277758816717e-06, "winding_ball": [0.9999997949595856,1.0000002050404135]}
  NO_WRITE_REPLAY receipt/report writes avoided: main() not called
  ```

- One initial replay inspection requested a nonexistent result key
  `arcs_total` and raised `KeyError: 'arcs_total'`; it was abandoned and the
  corrected no-write replay above was run.  No expensive numerical job,
  Kaggle submission, or external service was started.

## Assumptions

- “Same-byte” means the embedded driver/engine bytes hash equal the local
  audited files; it does not elevate a finite run to a theorem.
- The two countermodels test the logical implications of the routines.  They
  do not assert any actual q=8..12 determinant zero or future increment.
- Historical JSON/log status strings are treated as program output, exactly as
  the correction blocks require, not as theorem status.

## Leftovers / concerns

- A local q=8 Kaggle output log is absent; only embedded-byte equality and the
  historical plan record are available for that canary.  q=9..12 have local
  canary receipts/log summaries.
- A genuine repair remains outside this referee: theorem-valid uniform
  Fredholm/dimension tails, continuous subarc interval/Taylor/derivative
  enclosures, exact-box binding, E1, `K_s`, and factorization applicability.
- No claim is made here about the independent q=5/q=7 mathematics or RATE-A
  beyond the dependency boundary checked above.

**Hash-ellipsis erratum — 2026-08-19.**  The q=10 and q=12 table rows above
abbreviate the even-engine hash as `693d…7212a`; the full verified SHA-256 is
`693d2a88fd525e94c8ab6a63486e82fe0670d9dce142effbd5be5e324597212a`, so the
ellipsis must end `…212a`.  This is a display-only correction; the evidence,
classification, and principal verdict do not change.

STATUS: COMPLETE_WITH_CONCERNS (local q=8 Kaggle output log absent; byte-equality replay and historical plan record available)
READY FOR JUDGING

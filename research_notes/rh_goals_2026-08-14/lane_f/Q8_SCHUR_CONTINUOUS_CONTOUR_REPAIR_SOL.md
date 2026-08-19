# q=8 Schur continuous-contour implementation repair

Date: 2026-08-19. Base/referee commit:
`2a00b3a3f7014f192d8ea104ad1f13834f70a1f3`.

## Verdict

**BOUNDED IMPLEMENTATION REPAIR; FAIL-CLOSED; CONJECTURAL PENDING A NEW COLD
REFEREE.** This is not a q=8 determinant, Fredholm, Selberg, resonance, or LAW
certificate. The N=104 contour was not run.

The finite complex-displacement enclosure and the F1024 geometry/provenance
binding are repaired. The full determinant homotopy is deliberately disabled:
the immutable q=8 artifacts contain input-column tails but no compatible
omitted-output-row/projection tail. The stale recorded tail upper bounds also
fail the corrected adverse comparison. Both conditions are explicit false
gates, so no finite/Fredholm status can be emitted.

## Repairs against the cold referee

1. `complex_modulus_enclosure(B)` now returns
   `acb(arb(0,B), arb(0,B))`. This rectangle contains the full closed disk
   `|z| <= B`; it does not mistake `acb(0,B)` for a two-dimensional enclosure.
2. Production midpoint and arc matrices now receive exact factor strings
   `("10", "4", "2")`. The loader requires the TB factor list to be exactly
   `['10','4','2']`, overlaps the engine lambda/centers/radii against all R2,
   TB, and W geometry balls, and verifies hard-coded hashes for R2, TB, W,
   `q8_r3b_engine.py`, `q8_contour_helpers.py`, `f8_source_builder.py`, and
   `f8_certify_tb_blocks.py`.
3. The input-column quantity is named `input_tail_only`. The required
   omitted-output/projection quantity is present as an unavailable component;
   consequently `full_tau=None`, `full_tail_certified=false`, and the homotopy
   gate is false. This is the only sound result from the currently pinned
   receipts: the W receipt itself says its Fredholm/dimension tail is OPEN.
4. A stored upper bound is now accepted only when
   `recomputed.upper() <= source.upper()`. The pinned N=256 and N=320 rows fail
   this corrected comparison, and `recorded_tail_checks_pass` is therefore
   false. The fresh input-only formula remains diagnostic; it is not promoted
   to a full tail.
5. Checkpoints use schema v2 and bind the repaired implementation, factors,
   receipt hashes, and source hashes. Loading rejects v1. Every completed
   initial arc must have unique binary leaves forming an exact dyadic partition;
   every saved PASS box must parse. Final ordered records are always reparsed,
   so saved and newly computed boxes cannot be conditionally omitted.
6. `test_q8_schur_contour_repair.py` reproduces the referee's literal N=2
   first-bottom-segment endpoint counterexample and adds geometry/hash,
   comparison-direction, missing-output-tail, and checkpoint regressions.

## Counterexample replay

Command:

```text
$ PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
... N=2 first bottom segment, entry (0,0) ...
PY
```

Output:

```text
endpoint_displacement [-1.768445340374934833575974614726695251410033088896e-6 +/- 8.21e-55] + [3.43215913162386120290084889232805301510904325078e-7 +/- 7.03e-55]j
B [1.80201611275187226545528152441180865232321713388370131098e-6 +/- 2.27e-63]
old_real_contains False
new_contains_complex_endpoint True
factor_strings ['10', '4', '2']
geometry_verified True
receipt_hashes_verified {'R2': True, 'TB': True, 'W': True}
source_hashes_verified {'q8_r3b_engine.py': True, 'q8_contour_helpers.py': True, 'f8_source_builder.py': True, 'f8_certify_tb_blocks.py': True}
recorded_256_source_covers False
full_tail_certified False
full_tau None
```

## Bounded N=2/4 behavior

Commands:

```text
$ PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python q8_schur_contour.py --N 2 --K 1 --max-depth 0 --arc-start 0 --arc-end 1 --out /tmp/q8_schur_repair_n2.json
$ PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python q8_schur_contour.py --N 4 --K 1 --max-depth 0 --arc-start 0 --arc-end 1 --out /tmp/q8_schur_repair_n4.json
```

Both exit 2 and report `OPEN`. In both receipts:

```text
factor_strings ['10', '4', '2']
geometry_verified True
tail_formula_checks_pass False
full_tail_certified False
full_tau None
```

The finite local gates were diagnostic only. At N=2,
`qF=2.1843890406771576e-5...` and `rH=9.3094277116900400e-6...`; at N=4,
`qF=0.0014676909332799674...` and `rH=4.7738356903267168e-5...`.
Neither result is a proof receipt because the two global tail/provenance gates
are false.

## Remaining OPEN gates

The first remaining mathematical gap is a certified omitted-output
row/projection coefficient tail, combined with the input-column tail in the
same explicitly bound Hardy/Hilbert norm. After that, the following remain
separately OPEN:

1. E1 on the required enlarged disc and branch/pole holomorphy region.
2. Exact q=8 MMS-to-Hardy/Hilbert operator, basis, and norm binding.
3. Nonvanishing and exact word/lattice identification of `K_s`.
4. Common meromorphic continuation and the Selberg determinant/zeta/scattering
   factorization.
5. A complete corrected four-edge winding and a new independent cold referee.

The projected N=104 behavior is therefore fail-closed `OPEN`; no N=104 runtime
or contour result is claimed.

---

## Dated checkpoint-provenance correction — 2026-08-19

This append-only correction answers the stacked cold-referee commit
`e0a9b30b893a13193e7567e61e6d3961a718f92a`. All claims remain
**CONJECTURAL PENDING A NEW COLD REFEREE**; the full output-projection tail is
still hard OPEN and N=104 was not run.

### Corrected checkpoint contract

Checkpoint schema v3 binds `params.checker_sha256` to the actual bytes of
`q8_schur_contour.py`, not merely an implementation label. The repaired
checker SHA-256 at this correction is:

```text
ef088d357da72ea44079bccfa643a4a76fc86fb87db3305566cff5e2b9233c76
```

The parameter object also retains the pinned precision, contour coordinates,
F1024 factors, dependency hashes, and receipt hashes. Any checker-byte change
therefore makes an old checkpoint parameter-incompatible.

After structural loading, every saved `PASS` leaf is treated as untrusted.
The checker reconstructs its segment solely from the trusted initial contour
arc and binary subdivision path, reruns `arc_certificate` at 384-bit precision
with the current verified receipts/bounds, and replaces the saved record and
box with that fresh result. If the fresh result is not `PASS`, resume raises
and fails closed before winding. Saved `OPEN_MAX_DEPTH` leaves remain
diagnostic, but their presence prevents winding as before.

### Adversarial receipts and blast radius

The added tests cover both load-bearing referee cases:

1. A v3 checkpoint carrying a different checker hash is rejected by exact
   parameter comparison.
2. Four forged nonzero overlapping PASS boxes have certified winding 1 when
   sent directly to the winding helper, but checkpoint resume reconstructs the
   real leaves and rejects them because the current full-tail gates cannot
   freshly produce PASS.

Blast radius is restricted to checkpoint creation/resume and its diagnostics:
old v1/v2 checkpoints are conservatively incompatible; v3 OPEN-only resumes
remain diagnostic; newly computed non-resume arcs use the same finite checker.
The F1024 geometry/hash gates, complex displacement enclosure, adverse tail
comparison, and hard-open `full_tau=None` behavior are unchanged. E1,
MMS/Hilbert binding, `K_s`, common continuation/Selberg factorization, and a
new independent referee remain OPEN.

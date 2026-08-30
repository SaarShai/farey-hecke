# S2 fine-granularity (n288r) campaign — harvest status, 2026-08-27

The 22-kernel `s2-contour-n288r-*` campaign (6 base arcs per chunk, arcs
60..192, N=288) was pushed 2026-08-24 and left unharvested. All 22 kernels
report `KernelWorkerStatus.COMPLETE`; all 22 receipts are now harvested into
`chunk_receipts/`.

**This campaign is a redundant confirmation, not the certificate of record.**
The certificate of record remains `chunk_receipts/S2_MERGED_CONTOUR_RECEIPT.json`
(16 chunks at 12 arcs each, full cover of arcs 0..192, `merged_winding = 1`,
`closed_contour_gate_pass = true`), which is two-seat refereed and archived in
`dissemination/zenodo_package/certificates/pin2_second/`. It was NOT overwritten.

## What landed

| Outcome | Chunks | Arc ranges |
|---|---|---|
| `status = complete`, `CHUNK_ARCS_CLEAR`, `chunk_gate_pass = true` | 14 | 78–108, 126–162, 174–192 |
| `status = partial` (11 h soft deadline, checkpointed) | 8 | 60–78, 108–126, 162–174 |

The 14 complete chunks form one homogeneous endpoint family: every one carries
the identical

    F_R(288) = [2.089448415544975208638923073866481...e-8 +/- 4.52e-128]

Their per-arc verdict agrees with the coarse campaign — every base arc they
cover is CLEAR there too.

## Why the fine F_R differs from the merged receipt

The merged (coarse) receipt carries

    F_R(288) = [2.089448415544807945468931703035184...e-8 +/- 4.18e-128]

The two enclosures are disjoint at the 13th significant digit. This is expected
and already refereed: `F_R` is a computed **upper bound**, not an enclosure of a
unique real, so two independent runs legitimately produce different admissible
bounds (see `../S2_ASSEMBLY_REFEREE_SOL.md`). `merge_s2_chunks.py` therefore
refuses to merge across families, which is why the fine chunks cannot be mixed
into the existing merged receipt — they would have to form their own complete
family.

## Residual (owner decision, not launched)

Completing an independent fine-granularity merged certificate needs the 8
partial chunks finished. A naive re-push does not do this: the kernel writes
`--checkpoint <receipt>.ckpt.json` to the kernel output only, and the checkpoint
is not staged back as a dataset input, so a resubmission restarts from scratch
and hits the same 39600 s deadline. Closing it requires wiring checkpoint
resume (upload the harvested `.ckpt.json` files into the input dataset and pass
them to `certify_r3b_flagship.py`) before re-pushing those 8.

Not done here because the coarse certificate already carries the result; this
lane buys extra confidence, not a new claim.

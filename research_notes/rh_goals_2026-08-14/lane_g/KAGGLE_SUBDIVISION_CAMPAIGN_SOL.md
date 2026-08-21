# q=8 Schur contour: depth-7 parallel subdivision campaign (Kaggle + local)

Date: 2026-08-20
Lane: lane_g (compute packaging only; `lane_f` is consumed UNMODIFIED)
Branch: `codex/prime-step-review-economic-validation`
No commit, no push of the repo. All Kaggle artifacts PRIVATE.

Files added (all under `lane_g/kaggle_q8_subdivision/`):

- `q8_leaf_shard.py` — leaf-sharded driver
- `merge_shards.py` — merge-time verifier, emits a lane_f v3 checkpoint
- `build_bundle.py` — dataset + kernel bundle builder
- `run_local_queue.sh` — local fallback queue for quota-rejected shards
- `bundle/` — generated dataset payload, kernel scripts, `PLAN.json`
- `shard_receipts/` — local receipts and logs

Files read but **not modified**: `lane_f/q8_schur_contour.py` and its whole
import closure.

## 0. Headline

`QF_TIGHTENING_SOL.md` §4 left the contour compute-bound, not stuck:
`qOp = 83.79 >= 1` at depth 0, halving per bisection, so depth 7 is needed —
512 leaves at ~1290 s each, ~1.8e2 CPU-hours.

This lane packaged that fan-out and started it. **5 of 8 shards are running on
private Kaggle CPU kernels; the remaining 3 were refused by a hard Kaggle quota
(`Maximum batch CPU session count of 5 reached`) and are running locally in a
nohup queue.** Nothing about the mathematics changed, and nothing here upgrades
any ledger item.

**Depth 7 is the minimum viable depth, and this was measured, not assumed.**
`qOp` is not constant along an arc: it peaks at the arc *midpoint*. Sampling the
worst (mid-arc) leaf at each depth, `N = 32`:

```text
depth 5:  worst mid-arc qOp = 2.6172   FAILS gate
depth 6:  worst mid-arc qOp = 1.3089   FAILS gate
depth 7:  worst mid-arc qOp = 0.6544   PASSES gate  (margin 1.53x)
depth 8:  worst mid-arc qOp = 0.3272   PASSES gate
```

The values halve exactly per level (2.6172 -> 1.3089 -> 0.6544 -> 0.3272),
confirming the halving law `QF_TIGHTENING_SOL.md` §4 predicted.

**A correction to an earlier draft of this note.** A first probe measured only
*leaf 0* — the arc endpoint — and read depth 6 as `0.880`, i.e. "clears, but
tight". That was a sampling error: leaf 0 is the arc *minimum*. At the arc
midpoint depth 6 is `1.3089` and **fails outright**. Depth 7 is therefore not
"the smallest depth with comfortable margin"; it is the smallest depth that
works at all. Equally, the depth-7 margin is `1.53x` (worst leaf), not the
`2.28x` that leaf 0 alone suggested. Never characterise an arc from its
endpoint.

Full depth-7 profile, all four arcs (`N = 32`; `qOp` is N-converged — the
`N = 262` production run reproduces the `N = 32` value to 7 significant
figures):

```text
leaf:    0      16     32     48     64     80     96     112    127
qOp:   0.4385 0.4979 0.5675 0.6298 0.6544 0.6217 0.5589 0.4931 0.4385
```

Symmetric about the midpoint, and identical across all four arcs to 3-4
decimals (the pin box is a square). Fine sweep around the peak (leaves 56-72,
step 2) tops out at `0.6544` at leaf 64. This is a **sample of 9+9 of 128
leaves, not a proof of the maximum** — which is precisely why the campaign
certifies every leaf rather than trusting the profile.

## 1. Why a driver, and what it is not allowed to do

The lane_f checker shards only by initial arc (`--arc-start/--arc-end`), and at
`K = 1` there are exactly four arcs — a granularity of ~45 CPU-hours per unit,
far past a 12-hour Kaggle session. The driver adds the missing axis and nothing
else:

- it reconstructs one leaf with the checker's own `segment_from_initial_path`;
- it certifies it with the checker's own `arc_certificate`;
- it relabels a non-PASS leaf at the target depth `OPEN_MAX_DEPTH`, exactly as
  the checker's own `certify_adaptive` does at `max_depth`;
- it writes records in the checker's own checkpoint-record shape.

Every gate, bound, hash check and Arb operation stays inside `lane_f`. The
driver contains no mathematics.

One deliberate difference from `certify_adaptive`: this campaign evaluates
**every** leaf at uniform depth 7 rather than stopping early at a passing
parent. That is strictly more work and strictly finer. It buys a static shard
map (a dead kernel is re-run, not re-planned) and a uniform-depth leaf family,
which is an exact partition of its arc — precisely what the checker's own
`validate_checkpoint_records` demands.

Leaf addressing: leaf `i` in `[0, 128)` is the big-endian bit path
`[b6,...,b0]`, i.e. the `i`-th sub-segment of the arc in `split_segment` order.

## 2. Receipt determinism

- The hashed payload carries no wall-clock value and no host detail. Timing
  lives in a sibling `timing` object that is **not** hashed.
- Every Arb/Acb quantity is a string, produced by the checker's own
  `arb_text`/`acb_text` (80 digits, `more=True`).
- `payload_sha256 = sha256(json.dumps(payload, sort_keys=True,
  separators=(",", ":")))` — recomputable by any verifier.
- `payload.params` **is** the checker's own `checkpoint_parameters(...)`, so a
  shard is bound to the exact checker bytes, source bytes and receipt bytes.
  Shards from two different checker builds cannot be merged.

Determinism was measured, not assumed. The same two leaves, run (a) in-repo
with 2 workers and (b) from the reconstructed Kaggle tree in a temp directory
with 1 worker, produced the identical payload hash:

```text
payload_sha256  e6b0325eea2a4af5efe27e17af378e1a1c096e47190147c7c708a176a852d0f1
                (both runs; worker count and install path are not in the payload)
```

## 3. Shard plan

Geometry: `K = 1`, 4 arcs, depth 7 → 128 leaves per arc, **512 leaves total**.
Shard unit: 64 leaves (half an arc). Kernel budget **as launched**: 4 workers ×
64 leaves ÷ 4 = 16 rounds × ~1290 s ≈ 5.7 h, against a 12 h Kaggle CPU session
and an in-kernel `--deadline-seconds 39600` (11 h) guard that writes a partial
receipt rather than losing the session's work.

**That sizing used the 1290 s reference and is now known to be optimistic.**
§8.1 measures the marginal leaf at ~1990 s, making a 64-leaf shard ~8.8 h on
hardware equal to this Mac — inside the guard by only 2.2 h, and over it on any
slower core. The launched kernels stay at 64 (re-pushing would restart them and
lose all progress); partial receipts are expected and are handled by §5 rule 1.
Size the next wave at 32.

| shard | kernel / process | arc | leaves | receipt | status (2026-08-20) |
|---|---|---|---|---|---|
| s00 | `saarshai/q8-schur-d7-s00` | 0 | 0–64 | `SHARD_a0_l0-64.json` | RUNNING (Kaggle) |
| s01 | `saarshai/q8-schur-d7-s01` | 0 | 64–128 | `SHARD_a0_l64-128.json` | RUNNING (Kaggle) |
| s02 | `saarshai/q8-schur-d7-s02` | 1 | 0–64 | `SHARD_a1_l0-64.json` | RUNNING (Kaggle) |
| s03 | `saarshai/q8-schur-d7-s03` | 1 | 64–128 | `SHARD_a1_l64-128.json` | RUNNING (Kaggle) |
| s04 | `saarshai/q8-schur-d7-s04` | 2 | 0–64 | `SHARD_a2_l0-64.json` | RUNNING (Kaggle) |
| s05 | local queue PID 34238 (slot 1) | 2 | 64–128 | `SHARD_a2_l64-128.json` | RUNNING (local, 12 workers) |
| s06 | local queue PID 34238 (slot 2) | 3 | 0–64 | `SHARD_a3_l0-64.json` | QUEUED (local) |
| s07 | local queue PID 34238 (slot 3) | 3 | 64–128 | `SHARD_a3_l64-128.json` | QUEUED (local) |
| — | local validation (PID 33707, exited) | 0 | 0–4 | `LOCAL_VALIDATION_a0_l0-4.json` | **COMPLETE — 4/4 PASS** (§8; cross-check of s00) |

Kernel status output, verbatim (all five, `grep -iv key` applied):

```text
q8-schur-d7-s00: saarshai/q8-schur-d7-s00 has status "KernelWorkerStatus.RUNNING"
q8-schur-d7-s01: saarshai/q8-schur-d7-s01 has status "KernelWorkerStatus.RUNNING"
q8-schur-d7-s02: saarshai/q8-schur-d7-s02 has status "KernelWorkerStatus.RUNNING"
q8-schur-d7-s03: saarshai/q8-schur-d7-s03 has status "KernelWorkerStatus.RUNNING"
q8-schur-d7-s04: saarshai/q8-schur-d7-s04 has status "KernelWorkerStatus.RUNNING"
```

### 3.1 The quota rejection, verbatim

```text
=== q8-schur-d7-s05 ===
Kernel push error: Maximum batch CPU session count of 5 reached.
=== q8-schur-d7-s06 ===
Kernel push error: Maximum batch CPU session count of 5 reached.
=== q8-schur-d7-s07 ===
Kernel push error: Maximum batch CPU session count of 5 reached.
```

This is a concurrency cap, not a rejection of the bundle: the kernel definitions
for s05–s07 exist under `bundle/kernels/` and push unchanged once a slot frees.
Two recovery routes, both live:

1. **Local queue (running now).** `run_local_queue.sh`, nohup PID **34238**,
   12 workers, 3 shards sequentially, ~2.2 h each ≈ 6.5 h total. Each shard has
   its own checkpoint, so a kill resumes rather than restarts.
2. **Kaggle re-push (next loop tick).** When any of s00–s04 completes, run
   `kaggle kernels push -p bundle/kernels/q8-schur-d7-s05` (then s06, s07). If
   the local queue has already produced a shard's receipt, skip that push — the
   shards are interchangeable by `(arc, leaf_range)`, not by host.

### 3.2 Two launch failures, both real, both fixed

Recorded because a future loop tick will hit them again.

**(a) Wrong dataset mount path.** The first push of s00–s04 all reached
`KernelWorkerStatus.ERROR`. `pip install python-flint==0.9.0` succeeded and
internet was live, so the bundle was fine; the kernel died on:

```text
FileNotFoundError: [Errno 2] No such file or directory:
  '/kaggle/input/q8-schur-subdivision-inputs/manifest.json'
```

Kaggle does **not** mount a dataset at `/kaggle/input/<id-slug>/`. Hardcoding
the id slug 404s silently until the kernel opens a file.

**(b) The mount is nested.** The obvious fix — glob
`/kaggle/input/*/manifest.json` — also failed, and printed why:

```text
mounted inputs: ['datasets']
expected exactly one mounted manifest.json, found []
```

The dataset sits under `/kaggle/input/datasets/...`, one level deeper. The
kernel now searches recursively (`/kaggle/input/**/manifest.json`,
`recursive=True`), requires exactly one hit, and prints both the mounted input
names and the resolved mount before doing anything else. Diagnose-on-failure was
what made the second fix a one-shot.

Both failures were in the *packaging*, never in lane_f, and neither could have
produced a wrong receipt — the kernel aborts before staging.

## 4. Dataset manifest

Private dataset `saarshai/q8-schur-subdivision-inputs`, status `ready`.
Files are stored flat (Kaggle's uploader does not preserve nested directories);
`manifest.json` maps each flat name to its path in the reconstructed lane tree.
**The kernel re-verifies every sha256 before staging the tree and aborts on any
mismatch**, so a corrupted or substituted dataset file cannot produce a receipt.

`manifest.json` sha256: `9e8d9f3dcc45271a5b71d20630eb929eab7afba3c7452a18a190c8e011c0a4e5`

| tree path | bytes | sha256 |
|---|---|---|
| `lane_f/q8_schur_contour.py` | 59070 | `6a9c1c3d7b28c2e0741a5e880d1b12d48066437ea03efcfd3cda90743f1fc3b0` |
| `lane_f/q8_contour_helpers.py` | 4967 | `54ff4dcf39b6f1521cdf25ad769e37a1b4858fc8e07dc711e015fb7cd13da2f0` |
| `lane_f/q8_r3b_engine.py` | 9466 | `8b63dfbfc6bad21b01a951cbbf9f25e5a218f0353f9dd1c3493674b311aca2fc` |
| `lane_f/f8_source_builder.py` | 6770 | `e7a27aaa23074eb5722c1d392a5a93f73f787c02ebc6f5faeb2af1d0802f747a` |
| `lane_f/f8_certify_tb_blocks.py` | 19376 | `30fd9b15a9425b1a356753f667909a8d58d826d4ac1e30f1a2e7667fcc73871c` |
| `lane_f/q8_tb_support.py` | 8930 | `b159154422d0047497548a58498429977e854bf67872fea32e627927ca2ec6d0` |
| `lane_g/law_probes/kaggle_boundary_rate/zeta_cert_rosen_q5.py` | 47890 | `c84c5c3f6d9f7a320bca7f1dbfd96a4859c3eea9b3de5420eb4eb223ad0d597b` |
| `lane_g/law_probes/kaggle_boundary_rate/zeta_cert_rosen_even.py` | 23770 | `693d2a88fd525e94c8ab6a63486e82fe0670d9dce142effbd5be5e324597212a` |
| `lane_g/law_probes/kaggle_boundary_rate/zeta_cert_rosen.py` | 19959 | `965c2e5f65ae88b458d79bc425375e31589dcbf50703173664ef0e30901dceac` |
| `lane_f/f8_receipts/Q8_R2_F1024_LOCAL_RECEIPT.json` | 88162 | `80daa5de82c4e47d43c3b4aaa84a5955be5281f2cb147e7730766a1bba946043` |
| `lane_f/f8_receipts/Q8_TB_BLOCK_CERTIFICATES_F1024_RECEIPT.json` | 48659 | `5f9cd3f9179c5b15539b3666bd3a2a3144995408648369dc1db6eda36f51d35c` |
| `lane_f/f8_receipts/Q8_W_ENVELOPE_F1024_RECEIPT.json` | 212014 | `7d7b33966e48c3fe5f45fcf9618943f17a65ca4ef91caa7e3b2067904d03011e` |
| `lane_g/l_out/Q8_R2OUT_F1024_REPIN_THETA1p230_RECEIPT.json` | 111970 | `15f1603af9319ccef1ae7deb942e5cd946835472ef507dbe0bd8b0d2372054d5` |
| `driver/q8_leaf_shard.py` | 14008 | `24f247af088f82727f0cd25f259e82e6d98f357ee707f93e6b47de676ddef4ea` |
| `driver/merge_shards.py` | 8503 | `886968a838afb056ff3d27275011099e175017827f86c39f5c6cb1f7a74d5191` |

Cross-check, not incidental: the four source hashes and the three receipt
hashes above are **the checker's own pins** — `PINNED_SOURCE_SHA256`,
`PINNED_RECEIPT_SHA256` and `PINNED_LOUT_SHA256` in `q8_schur_contour.py`. The
packaged bytes are the pinned bytes, and the checker re-verifies them itself
inside every kernel via `load_operator_bounds`.

The import closure was derived mechanically (walk `sys.modules` after importing
the checker, keep everything inside the repo), not guessed. The first packaging
attempt was one such walk short, and the local rehearsal caught it as a
`ModuleNotFoundError` before any Kaggle push.

One staleness note, stated rather than hidden: the dataset's
`driver/merge_shards.py` is the snapshot taken at upload time, before the
partial-shard rule of §5 (rule 1) was added. It is carried for provenance and is
**never executed in-kernel**; the repo copy is authoritative. It was not
re-uploaded because a dataset version bump would have disturbed the running
kernels for no gain.

`python-flint` is pinned to `0.9.0` in the manifest and in the kernel's
`pip install`, matching the local `farey-rh` venv. Arb results are only
bit-comparable across hosts at a fixed Arb build; treat cross-host hash
equality as evidence, not as a guarantee the pin can be relaxed.

## 5. Harvest procedure

For each finished kernel:

```bash
kaggle kernels status  saarshai/q8-schur-d7-sNN            2>&1 | grep -iv key
kaggle kernels output  saarshai/q8-schur-d7-sNN -p shard_receipts/ 2>&1 | grep -iv key
```

**Contingency, expected rather than hypothetical.** The 5.7 h per-shard estimate
uses this Mac's ~1290 s/leaf. A Kaggle CPU core is likely slower; if it is 2x
slower, a 64-leaf shard needs ~11.6 h and the 11 h deadline guard fires,
returning a partial receipt of roughly 56–60 leaves. That is a normal outcome,
not a failure: harvest the partial receipt, read `leaves_certified` from its
payload, and re-run only the missing leaves as a small shard. Do **not** re-push
the same kernel hoping to resume — `/kaggle/working` does not survive a version
bump, so the in-kernel checkpoint is lost and the shard restarts from leaf 0.

Local shards need no harvest step; `run_local_queue.sh` writes straight into
`shard_receipts/`.

Then merge:

```bash
python merge_shards.py shard_receipts/SHARD_a*.json \
    --out shard_receipts/MERGED_CHECKPOINT.json \
    --report shard_receipts/MERGE_REPORT.json
```

`merge_shards.py` refuses, fail-closed, unless all of the following hold:

1. **Every shard re-hashes.** `payload_sha256` must equal the recomputed
   canonical hash. A hand-edited receipt is refused. (Tested: flipping one
   record's `status` to `PASS` is caught — see §7.) A *partial* shard — a kernel
   that hit its 11 h deadline guard — is accepted with a `NOTE` on stderr rather
   than refused: its leaves are real leaves, and rule 3 is what actually decides
   whether the cover is complete. Refusing partial shards would have thrown away
   good leaves and made a deadline-truncated kernel worthless.
2. **Every shard agrees on the bound bytes.** `checker_sha256`, `source_sha256`,
   `receipt_sha256`, `implementation`, `N`, `K`, `max_depth`, `precision_bits`,
   `pin`, `sign`, `n_head`, `factor_strings`. The merging host must itself hold
   those bytes, or the merge aborts before writing anything.
3. **Coverage is exact.** The union of leaves must be exactly `{0..127}` for
   each of the 4 arcs — 512 leaves, each appearing exactly once. Missing,
   duplicated or out-of-range leaves are refused. (Tested: a 2-leaf input
   reports `coverage_exact false`, `missing_leaf_count 510`, and writes no
   checkpoint.)
4. **Per-leaf gate.** An arc certifies only if **every** one of its 128 leaves
   has `qOp_lt_1 == True` **and** `status == "PASS"`. One `OPEN_MAX_DEPTH` leaf
   opens the whole arc; one open arc opens the contour.
5. **The checker's own partition validator** then re-derives the exact-partition
   property from the recorded paths (`validate_checkpoint_records`), and the
   merged file is written by the checker's own `write_checkpoint`.

Cold audit (optional, expensive):

```bash
python lane_f/q8_schur_contour.py --N 262 --K 1 --max-depth 7 \
    --arc-start 0 --arc-end 4 \
    --resume shard_receipts/MERGED_CHECKPOINT.json \
    --out shard_receipts/Q8_SCHUR_D7_VERDICT.json
```

This re-derives the verdict including the certified winding number. Stated
honestly: the checker's `recompute_saved_pass_records` recomputes **every** PASS
leaf from scratch, so this audit costs the full campaign again, single-threaded.
It is the cold-referee path, not the harvest path. The harvest claim is the
merge report.

The `LOCAL_VALIDATION_a0_l0-4.json` receipt is deliberately **not** merged — its
leaves duplicate s00's, and the merge refuses duplicates. Its purpose is a
cross-host determinism check: leaves 0–3 of arc 0 computed on this Mac must
carry byte-identical record content to the same leaves inside s00's Kaggle
receipt. A mismatch there is a finding about the Arb build, and must be reported
before any merged number is quoted.

## 6. What a merged result will and will not mean

**Will mean**, if `all_arcs_certified` is true: every depth-7 leaf of all four
arcs satisfies `qOp < 1` and all strict gates, the finite-section arc cover is
complete, and the checker can compute a certified winding number for the finite
section. That is a real unblocking of the step `QF_TIGHTENING_SOL.md` §8 left
open, and it is the outcome the compute was spent on.

**Will not mean** a theorem. This is checker output. Specifically untouched and
still OPEN:

- E1;
- the q=8 MMS/Hilbert identification;
- `K_s`;
- analytic gates 5 and 6 of the 12-item ledger;
- continuation condition 8 of the 12-item ledger.

The `claim_status` the checker itself emits stays
`CONJECTURAL_PENDING_NEW_COLD_REFEREE`, and its `theorem_grade` field stays
`NO`. Nothing in this lane changes either. A merged `all_arcs_certified` is a
compute receipt that removes one blocker; it is not a promotion, and it must not
be quoted as one.

**Also will not mean** anything if coverage is short. A 511-of-512 result is not
"essentially certified" — the merge writes no checkpoint and reports
`coverage_exact false`. Partial shards are re-run, never rounded up.

## 7. Validation receipts

Driver end-to-end, from the reconstructed Kaggle tree (staged and hash-verified
exactly as the kernel does it):

```text
staged 15 files, all hashes verified
Q8_SHARD arc=0 leaves=[0,2) depth=7 N=32 workers=2 resumed=0 pending=2
Q8_SHARD leaf=1 status=OPEN_MAX_DEPTH qOp=[0.441855471676003678259 leaf_seconds=2.0
Q8_SHARD leaf=0 status=OPEN_MAX_DEPTH qOp=[0.438471653813449633916 leaf_seconds=2.1
{
  "arc": 0,
  "leaf_range": [0, 2],
  "leaves_complete": true,
  "status_counts": {"PASS": 0, "OPEN_MAX_DEPTH": 2},
  "qOp_lt_1_all": true,
  "payload_sha256": "e6b0325eea2a4af5efe27e17af378e1a1c096e47190147c7c708a176a852d0f1",
  "wall_seconds": 2.141448974609375
}
```

(`status` is `OPEN_MAX_DEPTH` here because at `N = 32` the output-projection
tail gate `full_tail_certified` is false — the certified target
`full_tau <= 1e-15` first holds at `N = 238`. The **arc gate** `qOp_lt_1` is
true at depth 7, which is what this probe was measuring. The campaign runs at
`N = 262`.)

Merge refusal, incomplete cover:

```text
"leaves_supplied": 2,
"coverage_exact": false,
"missing_leaf_count": 510,
"all_arcs_certified": false,
"merged_checkpoint": null,
```

Merge refusal, tampered receipt (one record's `status` flipped to `PASS`):

```text
tampered.json: payload hash mismatch
  recorded   e6b0325eea2a4af5efe27e17af378e1a1c096e47190147c7c708a176a852d0f1
  recomputed d8741028730cedfd0d6bf987e5620ae1715aeff751e972ca67b7c47d838ff24b
```

The `N = 262` local validation shard (arc 0, leaves 0–4, 4 workers) is still
running at the time of writing; its receipt lands at
`shard_receipts/LOCAL_VALIDATION_a0_l0-4.json` and is the first real
per-leaf-cost measurement on this hardware. Section 8 is filled on completion.

## 8. `N = 262` local validation shard — COMPLETE, all four leaves PASS

```text
Q8_SHARD arc=0 leaves=[0,4) depth=7 N=262 workers=4 resumed=0 pending=4
Q8_SHARD leaf=0 status=PASS qOp=[0.438471637709677022842 leaf_seconds=1985.4
Q8_SHARD leaf=1 status=PASS qOp=[0.441855455449863946139 leaf_seconds=1990.0
Q8_SHARD leaf=2 status=PASS qOp=[0.445239331808402014894 leaf_seconds=1990.1
Q8_SHARD leaf=3 status=PASS qOp=[0.448621147781441920416 leaf_seconds=1990.7
{
  "arc": 0,
  "leaf_range": [0, 4],
  "leaves_complete": true,
  "status_counts": {"PASS": 4, "OPEN_MAX_DEPTH": 0},
  "qOp_lt_1_all": true,
  "payload_sha256": "374f53bd7b2d9e1d9dc4bdb2502f1f89306b84a34a7001fdbcee40b5a09a7ac9",
  "wall_seconds": 1990.8501360416412
}
```

This is the campaign's first production-parameter result, and it is the one that
matters: at `N = 262`, depth 7, **all strict gates pass** — not just `qOp < 1`
but `recorded_tail_receipt_checks_pass` and `full_output_projection_tail_available`
too, which is why the status is `PASS` and not `FAIL_GATE`. Each leaf emitted a
`finite_taylor_box` (leaf 0: real part `-2.4985087762988397183673640389853448...`).

Two independent cross-checks fall out:

- **`qOp` really is N-converged.** Leaf 0 at `N = 32` gave
  `0.438471653813449633916`; at `N = 262` it gives `0.438471637709677022842` —
  agreement to 7 significant figures across an 8x change in truncation. This
  reproduces `QF_TIGHTENING_SOL.md` §3's finding independently.
- **The weighted Schur gate is doing real work but not much of it here.** Leaf 0:
  `qOp = 0.4384716377...` against `qF = 0.4384734604...`. A relative gain of
  `4.2e-6` — the same rank-one story §3 of that note tells, now confirmed at the
  production `N` and at depth 7.

### 8.1 Per-leaf cost: 1985-1991 s, not 1290 s

The measured marginal cost is **~1990 s per leaf**, 1.54x the 1290 s that
`QF_TIGHTENING_SOL.md` §4 quotes. All four leaves agree to within 0.3%, so this
is a stable figure, not noise. Two components should not be conflated:

A second correction to an earlier draft of this note. While the shard was still
running I saw workers pass 1610 s CPU with no leaf yet and attributed the
overshoot to `load_operator_bounds` amortising over a single leaf. **That was
wrong.** `leaf_seconds` is timed *inside* `_certify_leaf`, which runs after the
pool initializer has already built the bounds; it therefore excludes all setup.
The workers were simply still computing their way to 1990 s. So:

- **~1990 s is the clean marginal cost** of one `arc_certificate` call at
  `N = 262`, depth 7, 384-bit precision, on this hardware;
- worker setup (`load_operator_bounds`: receipt parsing, hash verification,
  F1024 geometry, bound assembly) is paid once per worker **on top** of that,
  and is not in the 1990 s.

**Budget consequence.** At 1990 s marginal, a 64-leaf shard at 4 workers costs
16 x 1990 s = **8.8 h** on hardware equal to this Mac, before setup. That is
already inside the 11 h deadline guard by only 2.2 h, so a Kaggle core even
25% slower overruns it. Expect partial receipts from s00-s04, and size the
*next* wave at 32 leaves per kernel (§9, step 0). The deadline guard and the
partial-shard merge rule (§5, rule 1) are what make an overrun survivable
rather than wasted; see the contingency in §5.

Cross-host determinism check, when both are in hand: leaves 0–3 of arc 0 appear
in **both** this receipt and s00's. Their record content must match byte for
byte. A mismatch is a finding about the Arb build across hosts and must be
reported before any merged number is quoted.

## 9. Honest status

- Packaging, sharding, determinism and merge-refusal behaviour are **measured**,
  not asserted; the receipts are in §7.
- 5 of 8 shards are on private Kaggle CPU kernels and confirmed RUNNING; 3 were
  quota-refused and are draining through a local nohup queue.
- **No shard has produced a certified arc yet.** No `qOp < 1` claim is made at
  `N = 262` beyond the depth probe at `N = 32`.
- **4 of 512 leaves are certified PASS at production parameters** (`N = 262`,
  depth 7, arc 0 leaves 0-3), with all strict gates passing and determinant
  boxes emitted. That is the first evidence the depth-7 campaign will clear the
  arc gate — but it is 4 leaves out of 512, on the arc's *easiest* stretch
  (`qOp ~ 0.44` against a mid-arc peak of `~0.65`). It certifies nothing yet.
- Depth 7 is the **minimum viable** depth: depth 6 fails outright at the arc
  midpoint (`qOp = 1.3089`). An earlier draft of this note got that wrong by
  sampling only the arc endpoint; §0 records the correction.
- Marginal per-leaf cost is **~1990 s**, 1.54x the 1290 s reference. A second
  earlier claim — that the overshoot was worker-setup amortisation — was also
  wrong, and §8.1 records why.
- The contour verdict remains `status OPEN`. This lane spent compute; it did not
  move a ledger item.

### Next loop tick

0. **Size the next wave at 32 leaves per kernel, not 64.** §8.1 measures the
   marginal leaf at ~1990 s, so a 64-leaf shard is ~8.8 h at 4 workers on
   hardware equal to this Mac and overruns the 11 h guard on any core more than
   ~25% slower. s00-s04 are already launched at 64; expect partial receipts from
   them and do not re-push them at 64.
1. Poll `kaggle kernels status saarshai/q8-schur-d7-s0{0..4}`; harvest each with
   `kaggle kernels output` as it completes.
2. Harvest partial receipts too, and re-shard only their missing leaves (§5
   contingency).
3. Let the local queue (PID 34238) drain s05–s07, or push them to Kaggle as
   slots free — whichever lands first; do not run both, the merge refuses
   duplicate leaves.
4. Run the cross-host determinism check of §8 before quoting any merged number.
5. Merge with `merge_shards.py` and read the report's `all_arcs_certified`.
   Whatever it says, it is checker output — §6 governs what may be claimed.

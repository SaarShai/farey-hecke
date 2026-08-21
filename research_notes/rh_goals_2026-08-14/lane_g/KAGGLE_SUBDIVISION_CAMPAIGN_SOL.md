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

---

# 10. Depth-8 wave (append-only, 2026-08-21)

Date: 2026-08-21 · lane_g · unrefereed · repo NOT committed, NOT pushed
Repo state at launch: branch `codex/prime-step-review-economic-validation`,
HEAD `4be6d0e348ef21cf60d5bf8e9351d14187bcded8`, `lane_f/` clean.

`DEPTH8_PREFLIGHT_SOL.md` returned 6/6 PASS at `N = 262` and the orchestrator
declared **FULL GO**. This section records the launch of the uniform depth-8
wave. Sections 0-9 above describe the depth-7 wave and are left untouched;
nothing in them is retracted, but **no depth-7 leaf receipt can enter a
depth-8 certificate** — see §10.1.

## 10.1 Why depth-7 work cannot be stitched in

`q8_leaf_shard.py` binds every shard to
`checker.checkpoint_parameters(N, K, args.depth, arc, arc+1)`, and `max_depth`
is one of `merge_shards.py`'s `BOUND_KEYS`. A depth-7 and a depth-8 receipt
therefore disagree on a bound parameter and the merge refuses them as a pair —
by construction, not by convention. The wave is a fresh, uniform
`--depth 8 --N 262 --K 1` campaign: **256 leaves per arc, 4 arcs, 1024 leaves.**

The 6 `PREFLIGHT_d8_*` leaves ARE at depth 8 and would merge. They are
nevertheless **re-run inside their shards anyway**: uniform coverage from a
static shard map beats receipt-stitching, and the pre-flight receipts are then
free to serve as independent cross-checks (§10.5). This costs 6 leaves of
1024 (0.6%) and buys a cover that needs no exception list.

## 10.2 Depth-7 Kaggle kernels: NOT stopped — deviation, recorded

The instruction was to stop `q8-schur-d7-s00..s04`. **They are still RUNNING,
and this is a deliberate, reasoned deviation.** Receipts, at 2026-08-21
04:50 UTC:

```text
saarshai/q8-schur-d7-s00 has status "KernelWorkerStatus.RUNNING"
saarshai/q8-schur-d7-s01 has status "KernelWorkerStatus.RUNNING"
saarshai/q8-schur-d7-s02 has status "KernelWorkerStatus.RUNNING"
saarshai/q8-schur-d7-s03 has status "KernelWorkerStatus.RUNNING"
saarshai/q8-schur-d7-s04 has status "KernelWorkerStatus.RUNNING"
```

Why they were not stopped:

1. **The Kaggle CLI has no cancel/stop verb.** `kaggle kernels --help` lists
   exactly `list, files, get, init, push, pull, output, status, logs, update,
   delete`. A grep of the installed `kaggle` package for a cancel/stop API
   method returns nothing.
2. **Superseding by push is refused by the very quota it would free.** Pushing
   a no-op "STOPPED" version to `q8-schur-d7-s00` returned:
   `Kernel push error: Maximum batch CPU session count of 5 reached.`
3. **`delete` is destructive** and is the only remaining CLI route. It would
   discard the kernels and their in-flight outputs irreversibly.
4. **Stopping is not on the critical path.** The kernels carry a 39600 s
   (11 h) deadline guard and started ~00:00 UTC, so they release their slots
   at ~11:00 UTC on their own. The local queue (§10.4) runs ~23 h. Kaggle
   shards claiming slots at ~11:00 UTC and finishing ~6.3 h later still land
   comfortably inside the local window.

**Consequence:** the 5 depth-8 Kaggle shards are **queued, not yet running.**
`push_d8_kaggle.sh` polls every 300 s and pushes them the moment a slot frees;
it is idempotent (a per-slug marker file) and logs every attempt. If the owner
wants the slots sooner, the Kaggle web UI has a per-session Stop button —
pressing it for s00-s04 makes the pusher claim the slots on its next pass. No
kernel was deleted.

## 10.3 Dataset rebuild at the current lane_f commit

Rebuilt with `build_bundle.py --depth 8 --N 262 --K 1 --shard-size 64
--prefix q8-schur-d8 --workers 4 --deadline 39600 --created 2026-08-21`.
The previous depth-7 `bundle/` was moved aside, not overwritten.

**Checker identity verified against git, not asserted:**

```text
git show HEAD:...lane_f/q8_schur_contour.py | shasum -a 256
  6a9c1c3d7b28c2e0741a5e880d1b12d48066437ea03efcfd3cda90743f1fc3b0
shasum -a 256 ...lane_f/q8_schur_contour.py
  6a9c1c3d7b28c2e0741a5e880d1b12d48066437ea03efcfd3cda90743f1fc3b0
git status --porcelain ...lane_f/   ->  (empty)
```

Identical, and the manifest records the same digest. All 15 payload files
re-hashed from the built dataset directory: **15 verified, 0 mismatches.**

| tree path | sha256 | bytes |
|---|---|---|
| `lane_f/q8_schur_contour.py` | `6a9c1c3d7b28c2e0741a5e880d1b12d48066437ea03efcfd3cda90743f1fc3b0` | 59070 |
| `lane_f/q8_contour_helpers.py` | `54ff4dcf39b6f1521cdf25ad769e37a1b4858fc8e07dc711e015fb7cd13da2f0` | 4967 |
| `lane_f/q8_r3b_engine.py` | `8b63dfbfc6bad21b01a951cbbf9f25e5a218f0353f9dd1c3493674b311aca2fc` | 9466 |
| `lane_f/f8_source_builder.py` | `e7a27aaa23074eb5722c1d392a5a93f73f787c02ebc6f5faeb2af1d0802f747a` | 6770 |
| `lane_f/f8_certify_tb_blocks.py` | `30fd9b15a9425b1a356753f667909a8d58d826d4ac1e30f1a2e7667fcc73871c` | 19376 |
| `lane_f/q8_tb_support.py` | `b159154422d0047497548a58498429977e854bf67872fea32e627927ca2ec6d0` | 8930 |
| `lane_g/law_probes/kaggle_boundary_rate/zeta_cert_rosen_q5.py` | `c84c5c3f6d9f7a320bca7f1dbfd96a4859c3eea9b3de5420eb4eb223ad0d597b` | 47890 |
| `lane_g/law_probes/kaggle_boundary_rate/zeta_cert_rosen_even.py` | `693d2a88fd525e94c8ab6a63486e82fe0670d9dce142effbd5be5e324597212a` | 23770 |
| `lane_g/law_probes/kaggle_boundary_rate/zeta_cert_rosen.py` | `965c2e5f65ae88b458d79bc425375e31589dcbf50703173664ef0e30901dceac` | 19959 |
| `lane_f/f8_receipts/Q8_R2_F1024_LOCAL_RECEIPT.json` | `80daa5de82c4e47d43c3b4aaa84a5955be5281f2cb147e7730766a1bba946043` | 88162 |
| `lane_f/f8_receipts/Q8_TB_BLOCK_CERTIFICATES_F1024_RECEIPT.json` | `5f9cd3f9179c5b15539b3666bd3a2a3144995408648369dc1db6eda36f51d35c` | 48659 |
| `lane_f/f8_receipts/Q8_W_ENVELOPE_F1024_RECEIPT.json` | `7d7b33966e48c3fe5f45fcf9618943f17a65ca4ef91caa7e3b2067904d03011e` | 212014 |
| `lane_g/l_out/Q8_R2OUT_F1024_REPIN_THETA1p230_RECEIPT.json` | `15f1603af9319ccef1ae7deb942e5cd946835472ef507dbe0bd8b0d2372054d5` | 111970 |
| `driver/q8_leaf_shard.py` | `24f247af088f82727f0cd25f259e82e6d98f357ee707f93e6b47de676ddef4ea` | 14008 |
| `driver/merge_shards.py` | `fe9e19d6d732ba2c8c707d0b068a11a70d3da288e7c0db3d2529f54bd7bb7260` | 9198 |

`manifest.json` itself: `6b5d06418073d695d93f2bc3b3710984acc7913c4312e2ddad296db298d5bf3b`
(geometry `{K_per_edge: 1, arcs: 4, depth: 8, leaves_per_arc: 256,
leaves_total: 1024}`).

**One source change was needed and is recorded here.** `build_dataset()`
hardcoded `depth: 7, leaves_total: 512` and a depth-7 `purpose` string, so a
depth-8 build would have shipped a manifest that lied about its own geometry.
`build_bundle.py` now threads `depth` into both fields. This touches
packaging metadata only; **no payload byte and no mathematics changed**, as
the identical checker digest above shows.

Dataset `saarshai/q8-schur-subdivision-inputs` bumped 04:56 UTC (private);
`kaggle datasets status` returns `ready` and the uploaded file sizes match the
manifest `bytes` column exactly.

## 10.4 Shard table (16 shards x 64 leaves)

Plan is `build_bundle.py`'s own `plan(depth=8, shard_size=64)`: arc-major,
64 leaves per shard, 4 shards per arc, 1024 leaves total.

| id | arc | leaves | runner | status at 04:57 UTC | note |
|---|---|---|---|---|---|
| s00 | 0 | [0, 64) | Kaggle `q8-schur-d8-s00` | QUEUED (slot busy) | |
| s01 | 0 | [64, 128) | Kaggle `q8-schur-d8-s01` | QUEUED (slot busy) | |
| s02 | 0 | [128, 192) | Kaggle `q8-schur-d8-s02` | QUEUED (slot busy) | holds PREFLIGHT leaf 128 |
| s03 | 0 | [192, 256) | Kaggle `q8-schur-d8-s03` | QUEUED (slot busy) | |
| s04 | 1 | [0, 64) | Kaggle `q8-schur-d8-s04` | QUEUED (slot busy) | |
| s05 | 1 | [64, 128) | local queue | **RUNNING** (PID 78866) | holds PREFLIGHT leaf 127 |
| s06 | 1 | [128, 192) | local queue | queued | |
| s07 | 1 | [192, 256) | local queue | queued | |
| s08 | 2 | [0, 64) | local queue | queued | |
| s09 | 2 | [64, 128) | local queue | queued | |
| s10 | 2 | [128, 192) | local queue | queued | holds PREFLIGHT leaves 142, 143 |
| s11 | 2 | [192, 256) | local queue | queued | |
| s12 | 3 | [0, 64) | local queue | queued | |
| s13 | 3 | [64, 128) | local queue | queued | holds PREFLIGHT leaves 84, 85 |
| s14 | 3 | [128, 192) | local queue | queued | |
| s15 | 3 | [192, 256) | local queue | queued | |

Runners:

* **Kaggle** — `push_d8_kaggle.sh`, 4 workers per kernel, 39600 s deadline
  guard. 64 leaves at the pre-flight's measured 1429 s/leaf is
  `16 x 1429 s = 6.35 h`, inside the guard with 4.6 h of headroom. (The
  depth-7 wave's §8.1 overrun warning does not carry over: that was 1990 s per
  leaf at depth 7, against 1429 s measured at depth 8 in the pre-flight.)
* **local queue** — `run_local_queue_d8.sh`, launched under `nohup`, 12
  workers, shards run **sequentially**. `64 x 1429 / 12 = 2.12 h` per shard,
  so 11 shards ≈ **23.3 h**.

Receipts land in `shard_receipts/d8/` — a **separate directory** from the
depth-7 receipts. This is load-bearing: `SHARD_a2_l64-128.json` and
`SHARD_a3_l0-64.ckpt.json` already exist there from the depth-7 wave, and
`load_checkpoint()` raises `SystemExit` on a foreign-parameter checkpoint. The
collision would kill the shard (fail-closed, not silently wrong); separate
directories avoid the abort entirely.

Launch receipts:

```text
=== QUEUE START s05 a1_l64-128 2026-08-21T04:52:12Z ===
Q8_SHARD arc=1 leaves=[64,128) depth=8 N=262 workers=12 resumed=0 pending=64
```

queue PID 78862, driver PID 78866, and 12 compute workers (PIDs 78868-78879)
confirmed at 94.5-99.3 %CPU each, aggregate 1158 %CPU.

## 10.5 Harvest and merge at depth 8

0. **Poll.** `kaggle kernels status saarshai/q8-schur-d8-s0{0..4}`; watch
   `shard_receipts/d8/LOCAL_QUEUE_D8.log` and `KAGGLE_PUSHER_D8.log`. Note
   that a shard prints nothing for its first ~1429 s — the driver logs only on
   leaf completion, so an apparently frozen log inside the first ~24 min is
   expected, not a hang. Check worker %CPU instead.
1. **Harvest.** `kaggle kernels output saarshai/q8-schur-d8-sNN -p
   shard_receipts/d8/`. Harvest **partial** receipts too: a deadline-hit
   kernel exits 3 with a real partial receipt, and its leaves are real leaves.
2. **Coverage.** The merge requires the union of leaves to be exactly
   `{0..255}` for **each of the 4 arcs** — 1024 leaves, each appearing
   **exactly once**. Missing, duplicated or out-of-range leaves are refused.
   Duplication is the live hazard here: never run the same shard locally and
   on Kaggle at once.
3. **Partial-merge rule (carried over from §5).** A partial shard is accepted
   into the merge; what is never relaxed is rule 2. Re-shard only the missing
   leaves of a partial shard, then merge the completion alongside it.
4. **Per-leaf gate.** An arc certifies only if EVERY one of its 256 leaves has
   `qOp_lt_1 == True` **AND** `status == "PASS"`. A single `OPEN_MAX_DEPTH`
   leaf opens the whole arc, and one open arc opens the contour. At depth 8
   the pre-flight predicts `qOp ~ 0.30-0.33` and `rH ~ 0.14-0.20` against the
   square-box predictor `1/(1+sqrt 2) = 0.41421`, so a leaf near either
   threshold is a finding and must be reported, not averaged away.
5. **Cross-host determinism check — run this BEFORE quoting any merged
   number.** Kaggle shard s02 recomputes arc 0 leaf 128, which the local
   `PREFLIGHT_d8_a0_l128-129.json` already holds
   (`rH = 0.1892125248420895230`, `qOp = 0.3271992747911403256`, payload hash
   `8412cd87f75a4fca...`). The two records must match **byte for byte**. A
   mismatch is a finding about the Arb build across hosts and blocks the
   harvest claim. The three local-vs-local pairs (s05/leaf 127, s10/leaves
   142-143, s13/leaves 84-85) are same-host reproducibility checks and are
   weaker evidence; s02 is the only genuine cross-host pair.
6. **Merge.** `merge_shards.py` with all 16 receipt paths, then read
   `all_arcs_certified` in the report. On complete coverage it hands the
   record set to the checker's OWN `validate_checkpoint_records` and writes a
   `q8-schur-contour-checkpoint/v3` file. The cold-audit path (feeding that
   checkpoint back to `q8_schur_contour.py --max-depth 8`) recomputes every
   PASS leaf single-threaded and costs the full campaign again; it is not the
   harvest path.

## 10.6 Standing caveat

Unchanged from §6 and restated because the depth-8 numbers will look stronger
than the depth-7 ones:

**A merged receipt is CHECKER OUTPUT, not a theorem.** Even
`all_arcs_certified == true` over all 1024 leaves establishes only that the
finite-section arc cover closes at `N = 262`, depth 8. E1, the q=8 MMS/Hilbert
identification, `K_s`, analytic gates 5-6 and continuation condition 8 of the
12-item ledger are untouched and remain OPEN. The analytic gates stand
independently of any amount of leaf compute.

Two further limits, stated plainly:

* The referee's condition-4 screen (`depth-7 rH > 1.66` predicts failure at
  depth 8) remains **measured on samples**. Arcs 0 and 1 were never fully
  certified at depth 7, so a depth-7 `rH` above 1.66 hiding there would
  invalidate the prediction for those arcs. The depth-8 wave tests this
  directly — that is part of what it is for.
* Nothing in this wave proves a uniform bound on `H_true`. It certifies 1024
  specific leaves, or it does not.

**This section records a launch, not a result. No leaf has been certified at
depth 8 by this wave yet; the only depth-8 leaves in hand are the 6 pre-flight
ones.**

## 10.7 Runner PIDs and one pusher correction (append-only)

Live processes at launch:

| process | PID | role |
|---|---|---|
| `run_local_queue_d8.sh` | 78862 | local queue, 11 shards sequential |
| `q8_leaf_shard.py` (s05) | 78866 | shard driver, arc 1 leaves [64,128) |
| pool workers | 78868-78879 | 12 workers, 94.5-99.3 %CPU each |
| `push_d8_kaggle.sh` | **79519** | Kaggle pusher (see correction below) |

**Correction to the first pusher launch.** The pusher first ran as PID 78986
and decided push success by grepping the CLI's message for
`successfully pushed`. That is unsafe: if Kaggle's wording drifts, a push that
actually SUCCEEDED would be read as a failure and retried on every 300 s pass,
spawning duplicate kernel versions and duplicate leaf work — and duplicated
leaves are exactly what the merge coverage rule refuses. PID 78986 was stopped
before it pushed anything (its only log lines are the two quota refusals) and
relaunched as **PID 79519** with the authority moved to the kernel's own
`kaggle kernels status`: a slug is marked pushed only when its status reads
`RUNNING|QUEUED|COMPLETE|ERROR|CANCEL`, i.e. only when a run demonstrably
exists. The superseded log is kept at `KAGGLE_PUSHER_D8.log.attempt1`.

**Shard-map coverage was verified mechanically, not by eye**: the 5 Kaggle
shards plus the 11 local shards cover **1024 leaves, 0 duplicates, 0
missing**, and the 6 pre-flight leaves land in s02 (arc 0 leaf 128, the
cross-host pair) and in local shards s05, s10, s13.

## 10.8 HEAD moved mid-launch; the pin still holds (append-only)

While this wave was being launched the orchestrator committed `332c2a9`
("Promote effective theorem: CONFIRMED-conditional, eight gates"), so HEAD is
no longer the `4be6d0e` recorded in §10 above. **The dataset pin is
unaffected, and this was checked rather than assumed:**

```text
git diff --stat 4be6d0e HEAD -- .../lane_f/     ->  (empty)
git show HEAD:.../lane_f/q8_schur_contour.py | shasum -a 256
  6a9c1c3d7b28c2e0741a5e880d1b12d48066437ea03efcfd3cda90743f1fc3b0
```

`lane_f/` is byte-identical across `4be6d0e..332c2a9`, and the checker digest
still equals the one in the §10.3 manifest table. Every in-flight shard is
therefore bound to the same checker bytes as the uploaded dataset, and shards
from the local queue and the Kaggle kernels remain mergeable with each other.
The §10 line "HEAD `4be6d0e`" stands as a statement about launch time, not a
claim about the current tip.

This lane made **no commit and no push**. Working-tree changes it owns:
`KAGGLE_SUBDIVISION_CAMPAIGN_SOL.md` (this append), `build_bundle.py` (the
§10.3 depth-threading fix), and the new untracked
`run_local_queue_d8.sh`, `push_d8_kaggle.sh`, `bundle/`,
`bundle_d7_archived_20260821T045111Z/`, `shard_receipts/d8/`.

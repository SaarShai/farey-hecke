# D8 Kaggle Harvest Receipt — UNREFEREED

Date: 2026-08-23. Harvester: Claude agent (d8 harvest + merge lane).

## HEADLINE: coverage is INCOMPLETE — 923/1024 depth-8 leaves covered (all PASS), 101 leaves MISSING. No merge run.

All five d8 wave-2 Kaggle kernels were cut off by the runtime deadline before
finishing their 64-leaf spans. No leaf anywhere is OPEN_MAX_DEPTH and no leaf
FAILED — every computed leaf is PASS — but the a0 arm and a1 l33-63 have gaps.

## 1. Kernel statuses (verbatim `kaggle kernels status`, 2026-08-23)

| slug | status string | receipt |
|---|---|---|
| saarshai/q8-schur-d8-s00 | `KernelWorkerStatus.CANCEL_ACKNOWLEDGED` | SHARD_a0_l0-64 (partial) |
| saarshai/q8-schur-d8-s01 | `KernelWorkerStatus.COMPLETE` | SHARD_a0_l64-128 (partial) |
| saarshai/q8-schur-d8-s02 | `KernelWorkerStatus.COMPLETE` | SHARD_a0_l128-192 (partial) |
| saarshai/q8-schur-d8-s03 | `KernelWorkerStatus.CANCEL_ACKNOWLEDGED` | SHARD_a0_l192-256 (partial) |
| saarshai/q8-schur-d8-s04 | `KernelWorkerStatus.COMPLETE` | SHARD_a1_l0-64 (partial) |

Note: the tasking assumed all five were COMPLETE; two are in fact
CANCEL_ACKNOWLEDGED (s00, s03 — presumably evicted when the S2 campaign
claimed slots). Even the three literal-COMPLETE kernels wrote PARTIAL shards:
`leaves_complete: false` in every payload — they hit the in-kernel deadline
guard, not the end of the span. This receipt records what the payloads say,
not the tasking's assumption.

Harvested to `kaggle_q8_subdivision/shard_receipts/d8_kaggle_harvest/s00..s04/`
(same layout as the d7 harvest). For each shard the `.ckpt.json` is FRESHER
than the final `.json` (e.g. s00: ckpt 41 records vs json 21) — the checkpoint
is the authority used below, matching each kernel log's last `done=` line.

## 2. Per-shard leaf counts and status_counts (checkpoint payloads)

| shard | span | records | status_counts | leaves_complete |
|---|---|---|---|---|
| Kaggle s00 | a0 l0-64 | 41/64 | {PASS: 41, OPEN_MAX_DEPTH: 0} | false |
| Kaggle s01 | a0 l64-128 | 50/64 | {PASS: 50, OPEN_MAX_DEPTH: 0} | false |
| Kaggle s02 | a0 l128-192 | 57/64 | {PASS: 57, OPEN_MAX_DEPTH: 0} | false |
| Kaggle s03 | a0 l192-256 | 37/64 | {PASS: 37, OPEN_MAX_DEPTH: 0} | false |
| Kaggle s04 | a1 l0-64 | 34/64 | {PASS: 34, OPEN_MAX_DEPTH: 0} | false |
| local ×11 (`shard_receipts/d8/`) | a1 l64-256, a2 l0-256, a3 l0-256 | 64/64 each | {PASS: 64, OPEN_MAX_DEPTH: 0} each | true ×11 |

Local queue: 11 shards, 704/704 PASS, log line `QUEUE DRAINED 2026-08-23T11:19:36Z`.
Kaggle partials: 219 PASS leaves. Leaf identity re-derived from each record's
binary `path` (all in-span, zero duplicates, zero overlap with local spans).

## 3. Coverage verdict

**NOT an exact tiling: 923/1024 leaves covered, 101 missing, aggregate PASS 923, OPEN_MAX_DEPTH 0, FAIL 0.**

Missing leaf ranges (inclusive):

- arc 0: l41-63 (23), l114-127 (14), l184 (1), l186-191 (6), l229-255 (27) — 71 leaves
- arc 1: l33 (1), l35-63 (29) — 30 leaves
- arc 2, arc 3: none

## 4. Merge

NOT RUN. `merge_shards.py` is fail-closed on `coverage_exact` per
KAGGLE_SUBDIVISION_CAMPAIGN_SOL.md §5/§10; running it on 923/1024 would write
nothing. A 923-of-1024 result is not "essentially certified" — partial spans
are re-run, never rounded up.

## 5. Next steps (gap = 101 leaves, ~all in a0 + a1 head)

1. Re-run the 5 partial spans seeded from the harvested `.ckpt.json` files
   (the shard driver resumes from a seed checkpoint — the Kaggle kernels
   already use `seed__SHARD_*.ckpt.json`; refresh the input dataset with these
   fresher checkpoints so only the 101 missing leaves are computed, ~101
   leaf-solves total).
2. Route: local queue (S2 campaign holds the Kaggle slots; do not touch
   s2-contour-*). At the observed ~2.1-2.4 h/leaf on Kaggle CPU vs local
   throughput that drained 704 leaves in ~1 day, a seeded 5-shard local wave
   is the shortest path.
3. Merge only after all 16 spans report `leaves_complete: true` and the
   payload_sha256 build-identity gate passes.

## 6. Gap-fill relaunch — 2026-08-23 (local, seeded)

Launched 2026-08-23T11:25:25Z by the d8 gap-fill compute lane.

### Commands

```
# Seed: copy fresher harvested checkpoints into the local receipts dir
# (no collisions — d8/ previously held only a1 l64-256, a2, a3)
cp shard_receipts/d8_kaggle_harvest/s00/SHARD_a0_l0-64.ckpt.json    shard_receipts/d8/
cp shard_receipts/d8_kaggle_harvest/s01/SHARD_a0_l64-128.ckpt.json  shard_receipts/d8/
cp shard_receipts/d8_kaggle_harvest/s02/SHARD_a0_l128-192.ckpt.json shard_receipts/d8/
cp shard_receipts/d8_kaggle_harvest/s03/SHARD_a0_l192-256.ckpt.json shard_receipts/d8/
cp shard_receipts/d8_kaggle_harvest/s04/SHARD_a1_l0-64.ckpt.json    shard_receipts/d8/

# Queue: run_gap_fill_d8.sh = run_local_queue_d8.sh with spans s00-s04
# (same driver q8_leaf_shard.py, same flags --depth 8 --N 262 --K 1
#  --workers 12, same receipt schema/paths)
cd kaggle_q8_subdivision && nohup nice -n 10 ./run_gap_fill_d8.sh \
  > shard_receipts/d8/GAP_FILL.log 2>&1 &   # queue pid 12652
```

### Seeding evidence

Driver resume lines must show `resumed=` equal to the harvested checkpoint
record counts (41/50/57/37/34). First shard, from GAP_FILL.log:

```
Q8_SHARD arc=0 leaves=[0,64) depth=8 N=262 workers=12 resumed=41 pending=23
```

resumed=41 matches the s00 checkpoint's 41 records; only the 23 missing
leaves are computed. Expected for the rest of the queue: s01 resumed=50
pending=14, s02 resumed=57 pending=7, s03 resumed=37 pending=27, s04
resumed=34 pending=30. Total pending 23+14+7+27+30 = 101 = the missing set.
Verified running: 12 spawn-pool workers at nice 15, ~100% CPU each.

### Expected wall time

Prior local wave: 64 leaves/shard in ~3-10.7 h at 12 workers. For 101
leaves across 5 sequential shards (with parallel-tail inefficiency on the
small pendings): estimate **~6-18 h wall**, done in the ballpark of
2026-08-23 late evening to 2026-08-24 morning UTC.

### Harvest / monitor

- Progress: `tail shard_receipts/d8/GAP_FILL.log` — `done=N/64` lines;
  `=== GAPFILL DRAINED ===` marks completion.
- On completion each span's final receipt overwrites
  `shard_receipts/d8/SHARD_a{0,1}_l*.json` with `leaves_complete: true`
  (checkpoints updated per-leaf, so a kill resumes).
- Then all 16 spans live in `shard_receipts/d8/` (the 5 gap-filled + the
  11 prior local receipts) — run `merge_shards.py` per §4/§5 gates.

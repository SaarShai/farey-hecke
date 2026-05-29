# Does cluster=2 universality buy us an algorithmic speedup?

**Date:** 2026-05-27
**Code:** `projects/mimo-mini-project/code/cluster2_pruning_demo.py`
**Raw output:** `projects/mimo-mini-project/code/cluster2_bench_output.txt`

**Verdict.** A **small real speedup (~13–17%) in the materialised pure-Python
implementation** at q within ~3% of q*_BCZ; **shrinks to ~1% at q = 0.99**;
**zero (or even slightly negative) in the streaming variant**; and **trivially
zero against vectorised NumPy** (which is already 50–80× faster than the
Python loops and has no per-element branch to elide).

This is a clean *small* free lunch in a narrow regime. It is **not**
algorithmically transformative.

---

## 1. The chosen problem

**Extreme-gap Farey run enumeration.** Given a Farey order N and a quantile
q > q*_BCZ = (11 − 8·ln 3/2)/9 ≈ 0.86181, enumerate every *maximal run* of
consecutive Farey gaps g_i = a_{i+1}/b_{i+1} − a_i/b_i exceeding the
sample threshold τ_q. Output: list of (start_index, run_length).

This is the right problem to test cluster=2 against because the structural
constraint maps directly: **above q\*\_BCZ, no maximal run can have length ≥ 3**.
A correct algorithm only needs to recognise size-1 and size-2 runs.

## 2. Algorithms

Five algorithms across two execution modes:

**Materialised mode** (whole gap array in RAM):

1. **`enumerate_runs_baseline`** — plain Python while-loop with an inner
   while-loop that extends a run as long as `gaps[j] > τ`.
2. **`enumerate_runs_pruned`** — same outer loop, but the moment we see two
   consecutive extreme gaps we record a size-2 run and **advance the index
   by 3**, skipping the threshold comparison on the third gap. cluster=2
   guarantees this third gap is non-extreme, so the answer is identical.
3. **`enumerate_runs_vectorised`** — the realistic NumPy baseline: build a
   boolean mask, diff it, find run starts/ends. cluster=2 cannot help here.

**Streaming mode** (no gap array; Stern–Brocot recurrence on the fly):

4. **`enumerate_runs_streaming_baseline`** — single pass, compute each
   `g = 1/(b_{i−1} · b_i)`, test against τ, run-length encode.
5. **`enumerate_runs_streaming_pruned`** — same, but after a size-2 cluster
   the next iteration sets `skip_next_compare=True`, hitting a fast `continue`
   that skips both the float division and the threshold compare.

Timing methodology:
- Median over 5 (materialised) / 3 (streaming) repeats.
- **Interleaved** runs (base, prune, vec, base, prune, vec, …) so that cache
  warm-up / CPU thermal effects do not systematically bias one algorithm.
- One warm-up call discarded before timing.
- A first attempt without interleaving showed a misleading 5.5× speedup that
  evaporated when the order of runs was randomised — proper methodology
  matters here.

## 3. Benchmark results (materialised, MacBook, Python 3.9, NumPy)

|       N |    q | \|gaps\|   | #runs    | base (ms) | prune (ms) | vec (ms) | prune/base | same? |
|--------:|-----:|-----------:|---------:|----------:|-----------:|---------:|-----------:|------:|
|   1 000 | 0.99 |    304 192 |    1 567 |     25.18 |      24.93 |     0.39 |  **0.990** |   OK  |
|   3 000 | 0.99 |  2 736 188 |   14 017 |    226.27 |     224.09 |     3.13 |  **0.990** |   OK  |
|  10 000 | 0.99 | 30 397 486 |  155 819 |   2498.71 |    2484.71 |    38.61 |  **0.994** |   OK  |
|   1 000 | 0.90 |    304 192 |   16 739 |     29.25 |      25.46 |     1.73 |  **0.870** |   OK  |
|   3 000 | 0.90 |  2 736 188 |  150 575 |    264.14 |     227.56 |    14.55 |  **0.862** |   OK  |
|   5 000 | 0.90 |  7 600 458 |  418 253 |    729.89 |     635.87 |    40.24 |  **0.871** |   OK  |
|   1 000 | 0.87 |    304 192 |   22 197 |     30.34 |      25.33 |     2.12 |  **0.835** |   OK  |
|   3 000 | 0.87 |  2 736 188 |  199 611 |    277.01 |     230.71 |    18.34 |  **0.833** |   OK  |
|   5 000 | 0.87 |  7 600 458 |  554 365 |    777.26 |     649.45 |    54.71 |  **0.836** |   OK  |

**Negative control** at q = 0.50 (below q*_BCZ; cluster=2 does not hold):

|       N |    q | \|gaps\|   | #runs    | base (ms) | prune (ms) | #sz≥3 | prune/base | same? |
|--------:|-----:|-----------:|---------:|----------:|-----------:|------:|-----------:|------:|
|   3 000 | 0.50 |  2 736 188 |  595 101 |    387.14 |     250.54 | 109 558 |    0.647 |  FAIL |

The pruned algorithm misses 109 558 size-≥3 clusters → **wrong output**,
exactly as the theorem predicts. Empirically confirms that q*_BCZ is the
correct safety boundary.

## 4. Benchmark results (streaming mode)

|       N |    q |    #runs |   #sz=2 | base (s) | prune (s) | prune/base | same? |
|--------:|-----:|---------:|--------:|---------:|----------:|-----------:|------:|
|   3 000 | 0.90 |  151 203 | 123 495 |     0.61 |      0.62 |  **1.017** |   OK  |
|   5 000 | 0.90 |  415 247 | 339 663 |     1.69 |      1.72 |  **1.016** |   OK  |
|   3 000 | 0.87 |  199 293 | 155 893 |     0.62 |      0.62 |  **1.009** |   OK  |
|   5 000 | 0.87 |  547 171 | 429 055 |     1.72 |      1.74 |  **1.010** |   OK  |

In streaming mode the prune is **~1–2 % slower**, because the
`if skip_next_compare:` check at the top of every loop iteration costs slightly
more than the work it eliminates on the ~5% of iterations that fire.

## 5. What the speedup actually is, in the materialised regime

Two factors drive the size of the speedup:

- **Density of size-2 clusters.** As q ↓ q\*\_BCZ, more gaps are extreme,
  so a larger fraction of clusters are size-2 (rather than size-1), and the
  prune fires more often.
    - q = 0.99 → ~94 % of clusters are size-1, prune almost never fires →
      ~1 % speedup, within timing noise.
    - q = 0.87 → ~78 % of clusters are size-2, prune fires hundreds of
      thousands of times → ~17 % speedup.

- **Per-iteration cost.** In the *materialised* baseline each pass through
  the inner extension loop costs an `np.ndarray.__getitem__`, a Python float
  compare, and a `+=`. That is ~150 ns of interpreter overhead per gap. The
  prune saves one full iteration per size-2 cluster.

In the streaming baseline the inner-loop body is *already* doing useful
arithmetic (the gap division `1.0/(prev*b)`), so the relative saving from
skipping one iteration is dwarfed by the cost of the extra branch added at
the top of the loop. Net: a wash, or 1 % regression.

The honest one-line summary:

> cluster=2 lets you skip *exactly one branch per size-2 cluster*. That is
> negligible against any vectorised implementation (NumPy is 50–80× faster
> than the Python loops to begin with), modestly positive (~13–17 %) in
> indexed-Python loops near q\*\_BCZ, and a slight net loss in
> single-pass streaming loops where the prune-check costs more than it saves.

## 6. Where this matters / does not matter

**Matters (modest):**
- Indexed-Python prototypes operating on a pre-computed gap array.
- Implementations where the inner-loop body is expensive in absolute terms
  (e.g. logging, allocating per-run records, yielding to a downstream
  consumer), so that saving one full iteration pays back the prune-check.
- Quantiles near q\*\_BCZ where size-2 clusters dominate.

**Does not matter:**
- Vectorised NumPy / C / Rust / GPU implementations. Run-length encoding
  via boolean mask + diff has no per-element branch to elide.
- Single-pass streaming loops where the per-iteration body is already
  cheap. The prune-check adds more cost than it saves.
- Quantiles far above q\*\_BCZ (q ≥ 0.97), where size-2 clusters are rare.
- Any setting where threshold computation (full sort or partition of |F_N|
  floats) dominates total wall time.

## 7. Verdict

**SMALL BUT REAL SPEEDUP** in the materialised pure-Python regime,
~13–17 % at q ∈ [0.87, 0.90]; **NEGLIGIBLE** (within noise) at q ≥ 0.99;
**ZERO-or-negative** in streaming pure-Python; **ZERO** against vectorised
NumPy. Correctness verified by exact-output comparison at 9 (N, q) points
above q\*\_BCZ; falsified (as expected) at q = 0.50 below q\*\_BCZ.

This is **not** a transformative algorithmic improvement. It is a clean
empirical confirmation that:

1. The cluster=2 theorem is correct at the scales tested (|F_N| up to
   ~3 × 10^7 gaps).
2. The predicted q\*_BCZ = (11 − 8 ln(3/2))/9 is the right boundary —
   the prune is exact above it, broken below it.
3. *Constant-factor* algorithmic exploitation of the universality is
   modest at best. The structural constraint is sharp (no size-3 cluster
   above q\*) but the work saved per fire is tiny (one comparison) and
   only pays back when the inner-loop body is expensive enough.

## 8. Honest caveats

- Asymptotic complexity is unchanged. The Stern–Brocot recurrence is the
  dominant cost in streaming mode and cluster=2 cannot let us skip
  recurrence steps (we still need b_{i+3} for the *next* gap).
- The 5.5× speedup observed in a first naive single-shot streaming
  measurement was pure cache/order noise. After interleaving and warm-up,
  the streaming prune is *worse* than baseline. Methodology matters.
- I did not test |F_N| below ~3 × 10^5 — at those sizes the entire
  benchmark is sub-millisecond and noise dominates.
- Repeats: 5 (materialised), 3 (streaming), median reported. Variance
  within repeats was < 5 %.
- No cache-miss / `perf` analysis — the program is too small and
  Python-interpreter-dominated for those numbers to be informative.
- A C / Rust reimplementation might shrink the materialised speedup to
  the streaming-mode 1 % regression — the relative payoff is an artefact
  of Python's high per-iteration overhead.

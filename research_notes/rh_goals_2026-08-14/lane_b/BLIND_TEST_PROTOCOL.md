# BLIND-TEST PROTOCOL — arithmeticity from resonance geometry

**Status: PREREGISTERED DESIGN ONLY — NOT YET RUN.** No q has been sampled,
no protocol engine run has been launched, and no result has been scored under
this document.

## 1. Question and fixed hypotheses

The test asks whether an evaluator can classify arithmetic versus
non-arithmetic Hecke surfaces from resonance-geometry statistics alone.

- Arithmetic class: `q ∈ {3, 4, 6}`.
- Non-arithmetic class: `q ∈ {5, 7, 8}`.
- Primary prediction: arithmetic samples have `re_std <= 1e-6`; non-arithmetic
  samples have `re_std > 1e-6` when at least four independent eligible
  MMS-even resonance coordinates are available.
- The classification target is the surface class, not a claim that a finite
  sample proves the full resonance set or a completeness theorem.

The sector is fixed before sampling: MMS-even (`mms+`, with the q-dependent
operator convention frozen in the engine manifest). Odd-sector Maass points
and on-line `Re(s)=1/2` points are not eligible observations for this test.

## 2. Declared q pool and sample size

The declared pool is exactly:

```text
arithmetic      A = {3, 4, 6}
non-arithmetic  N = {5, 7, 8}
```

The sample has exactly 24 blinded draws:

1. Put two copies of each q in the draw list. This creates 12 mandatory draws,
   with every q represented twice.
2. Draw six additional arithmetic q values independently and uniformly from
   `{3,4,6}`, with replacement.
3. Draw six additional non-arithmetic q values independently and uniformly
   from `{5,7,8}`, with replacement.
4. Shuffle the resulting 24 labels with a cryptographically secure random
   permutation. Repeated q values are retained; no deduplication is allowed.

This fixes 12 arithmetic and 12 non-arithmetic draws while guaranteeing at
least two observations of every q. Agent A records the random seed, the
unshuffled label list, and the final permutation in a sealed ground-truth
receipt. The seed is generated after this document is frozen and is not shown
to Agent B before scoring.

## 3. Engine and locked output

Agent A uses the existing transfer-operator engine and its already-defined
q-specific entry point, without changing the operator, sector, scan domain,
precision, candidate filters, or stability thresholds after seeing a result.
The engine manifest must be sealed before sampling and must identify the exact
source commit/file for q=3, q=4, q=5, q=6, q=7, and q=8.

For each draw, A emits only a run ID and the following statistic record:

```json
{
  "run_id": "opaque-id",
  "n": 0,
  "re_mean": 0.0,
  "re_std": 0.0,
  "re_min": 0.0,
  "re_max": 0.0
}
```

The record contains no q, lambda, filename, source path, sector label, scan
plot, resonance coordinates, method-specific wording, or timing that could
identify q. A separate sealed A receipt retains the full coordinates,
provenance, engine version, and true q for later audit. A must not send that
receipt to B until B submits all 24 classifications.

The statistic definition is fixed to the population standard deviation of the
listed Re coordinates. Coordinates must be independent resonance locations:
finite-N repeats and independent-method confirmations of the same location are
collapsed before `n` and the statistics are emitted.

## 4. Roles and information barrier

### Agent A — sampler and executor

Agent A knows the q labels, performs the sealed random draw, runs the locked
engine, collapses duplicate confirmations according to the predeclared
independence rule, and sends B only the opaque statistic records in a randomly
permuted run-ID order. A must not provide B with any surface-specific metadata.

### Agent B — blind classifier

Agent B receives only the 24 opaque records and this protocol. B applies the
decision rule in Section 5 independently to each record and returns exactly
one label per run ID before seeing any q label, coordinate, source file,
engine log, or A receipt. B may not tune the threshold, discard an inconvenient
run, request a q-specific rerun, or infer q from side-channel metadata.

After B submits, A reveals the sealed q map and the full receipt. The scorer
then joins by run ID and evaluates the fixed success criterion.

## 5. Pre-declared decision rule

For each record with valid numeric fields:

```text
if n < 4:                         UNCLASSIFIABLE
elif re_std <= 1e-6:              ARITHMETIC
else:                             NON-ARITHMETIC
```

The equality boundary belongs to `ARITHMETIC`. `re_mean`, `re_min`, and
`re_max` are displayed to B for audit context but do not alter the decision.
The threshold `1e-6` is fixed before sampling and cannot be replaced by a
threshold estimated from the observed batch.

For scoring, `UNCLASSIFIABLE` is not correct for either class. B must not
replace it with a guessed class.

## 6. Validity, failure handling, and stopping rules

An individual draw is invalid if the engine crashes, times out, emits NaN or
missing statistics, has fewer than four independent eligible coordinates,
contains a sector mismatch, or cannot provide a receipt tying the statistic to
the sealed q. Invalidity is recorded as `UNCLASSIFIABLE` and counts as a failed
classification. There is no replacement draw, no q substitution, and no
post-hoc scan-window expansion.

The protocol stops after the fixed 24 draws. If the engine cannot supply a
locked entry point for a declared q before sampling, the protocol is aborted
before any draw; the pool is not silently narrowed. Any exploratory retry after
the 24-draw test is a separate experiment requiring a new preregistration.

## 7. Success criterion

The test succeeds only if all conditions hold:

1. all 24 draws are valid and classified as either ARITHMETIC or
   NON-ARITHMETIC;
2. at least 22 of 24 classifications are correct against the sealed q map;
3. at least 11 of 12 arithmetic draws and at least 11 of 12 non-arithmetic
   draws are correct.

Otherwise the result is `FAILURE` for this preregistered test. A failure does
not justify changing the threshold or removing difficult q values; it is
reported with the per-draw reason, the locked engine receipt, and the exact
number of invalid and incorrect classifications.

## 8. Reproducibility and cost note

The sealed receipt must preserve the random seed, final run order, engine
manifest, raw coordinate lists, independence-group decisions, emitted
statistics, B's pre-unblinding labels, and the post-unblinding score. The
existing G5 geometry artifact records a wall time of 1585.366377353668
seconds. As a planning-only baseline, 24 sequential G5-scale draws would be
38048.793056488032 seconds (about 10.57 hours). No runtime budget is part of the
success criterion, and this blind test is not being run in this task. Any
future execution must report measured wall time from the sealed receipt.

# Operational optimizer independent reviews

Date: 2026-07-16

## Sol Ultra adversarial audit

The read-only advisor ran as `gpt-5.6-sol` with `xhigh` reasoning against the
live compact constrained implementation, paper, interfaces, tests, and frozen
million-item evidence.  Its final verdict was **ACCEPT WITH REQUIRED REPAIRS**.

The proof audit accepted the contracted-frontier/Kahn argument, the fixed-queue
comparison set, every implemented lower-bound term, the independent tiny
oracle, and the primary-`B`-only interpretation of closed bounds.  It confirmed
that the scalable block-entry term is a valid linear-time relaxation rather
than the exact minimax stated as a possible bound in Theorem 8.

It required two final engineering repairs:

1. give the benchmark subprocess a hard timeout and a memory-sensitive ceiling;
2. make the frozen million-item block exercise repeated, consecutive
   occurrences from one category, with negative gap and reversal tests.

Both were implemented.  The worker now has a hard 30-second timeout and a
128-MiB RSS ceiling.  The frozen block contains `alpha#1001, alpha#1002` in
order; `BLOCK_CATEGORY_GAP` and `BLOCK_OCCURRENCE_ORDER_CONFLICT` have explicit
regression fixtures.  The regenerated frozen evidence has constraint digest
`85b5161d9c938f437a3d24315d271abf5cdf8bc14eba1e972a410e006dd1ae1a`
and order digest
`3194a7661d0d90f6115bba41cfed1c506fd8f9442c0f54c0a8069ff90662c675`.

## Earlier cold-review rejection and resolution

The first independent cold review rejected release because the code hid cubic
block-entry work, rescanned block participants, trusted forged result metadata,
did not freeze the exact constraint fixture, called primary-objective closure
an unqualified exact optimum, and admitted unbounded `N*C` interface work.

The repaired release:

- uses linear participant work for scalable block-entry certification and
  constant-time block-alignment readiness;
- states total certificate time as
  `O(NC + (N+K) log(C+K))`, while reserving the smaller bound for scheduling;
- recomputes exact feasibility and explanation metadata and requires packed
  `array('I')` storage;
- freezes constraints, both order digests, and exact `U`, `L`, `Q`, gap, and
  ratio, with adversarial mutation tests;
- exposes `primary_optimum_proved` and `proved_objective=primary_B_only`; and
- applies shared pre-solve caps of `C=256`, `N*C=8,000,000`, 10,000 constraint
  references, and block width 1,024, plus a loopback-only research server.

## Verification after repairs

`PYTHONDONTWRITEBYTECODE=1 python3 verify_operational.py` passed the static,
browser-JavaScript, operational unit/oracle, unconstrained million-item,
constrained million-item, original regression, source-mutation, and
cache-mutation gates.  The constrained frozen run emitted 1,000,000 positions
in 4.135954 seconds at 46,546,944 bytes RSS with the regenerated order digest.

The live browser run separately exercised keyboard entry, selection, clicks,
all four compact constraint classes, malformed JSON, recovery, the
primary-`B`-only label, and visual layout.  See
`BROWSER_VERIFICATION_OPERATIONAL.md`.

## Final cold re-review

After every repair, the independent cold reviewer returned **ACCEPT — no
remaining blockers**.  It rechecked the complexity labels, 5,000-participant
canary, forged metadata and storage rejection, both frozen-artifact validators,
the primary-`B`/secondary-`Q` counterexample, admission caps, loopback guard,
hard timeout, 128-MiB ceiling, repeated-category block, and gap/reversal
witnesses.  Its fresh million run passed in 4.080396 seconds at 46,989,312
bytes RSS, and its focused suite passed 31 tests in 5.964 seconds.

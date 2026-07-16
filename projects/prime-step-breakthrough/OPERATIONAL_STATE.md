# Operational Optimizer State

Date: 2026-07-16

## Goal

Deliver a proof-qualified, explainable, constrained multidimensional prefix
optimizer that processes one million categorical items, exposes measurable
guarantees against the true stated optimum, and works through Python, CLI,
JSON HTTP, and browser interfaces without regressing the original package.

## Current phase

The mathematical implementation and original operational gates are complete.
Fable 5's repair-authorized review found interface and evidence gaps; its
acceptance pass is being resolved before economic validation or marketing use.

## Mathematical and algorithmic result

For categorical inventories, occurrence `(c,j)` is the `j`-th member of a fixed
within-category queue.  The constrained comparison set is every interleaving
of those queues satisfying declared ordered blocks, exact prefix/suffix pins,
and occurrence-precedence edges.

The packed frontier/Kahn scheduler uses block-adjusted EDF pressure only as a
priority.  Its scheduling core costs `O((N+K) log(C+K))` time and `O(C+K)`
auxiliary memory plus the packed `O(N)` result.  The released certificate
recomputes exact achieved maximum discrepancy `U` and accumulated discrepancy
`Q` in `Theta(NC)`, so complete time is
`O(NC + (N+K) log(C+K))`.

The result reports a mathematically valid lower bound `L` for the same
comparison set, hence `L <= OPT_B <= U`, plus `U-L` and `U/L` when `L>0`.
`primary_optimum_proved` is true only when `L=U`; it proves the primary `B`
objective, not that the achieved `Q` is best among `B`-optimal orders.  No
unconstrained factor-three label is inherited under constraints.

## Operational boundaries

The shared CLI/API path rejects work before construction above:

- 256 categories;
- 8,000,000 exact metric cells `N*C`;
- 10,000 occurrence references, counting two per precedence edge; or
- fixed-block width 1,024.

The local HTTP service accepts only `127.0.0.1`, `localhost`, or `::1`.  It is
research software, not a hardened public multi-user deployment. It validates a
nonblank loopback `Host`, rejects non-loopback browser `Origin` headers, requires JSON for
API POSTs, caps all exact-arithmetic compute routes by endpoint-specific and
combined bit-work budgets (including supplied rational/common-denominator,
exact-output-size, and prefactored-kernel complexity), applies a 15-second socket timeout, and bounds concurrent
handlers at 64. The timeout is not total request cancellation; a same-host client
can occupy a slot until a read times out. Direct Python/CLI callers receive the
exact complexity contract but are not generally subject to HTTP admission caps.

## Frozen million-item evidence

The 1,000,000-item fixture activates all four constraint classes and contains
the repeated-category block prefix `alpha#1001, alpha#1002`, proving that the
consecutive within-category block rule is exercised.  The benchmark worker has
a hard 30-second timeout and a 128-MiB RSS ceiling.

Frozen values:

- constraint digest:
  `85b5161d9c938f437a3d24315d271abf5cdf8bc14eba1e972a410e006dd1ae1a`;
- order digest:
  `3194a7661d0d90f6115bba41cfed1c506fd8f9442c0f54c0a8069ff90662c675`;
- `U=360167777/200000`;
- `L=1799839/1000`;
- `Q=455298078991/62500`;
- additive gap `199977/200000`;
- ratio `360167777/359967800`.

The stable full verifier measured 4.135954 seconds and 46,546,944 bytes RSS;
the final cold reviewer independently measured 4.080396 seconds and 46,989,312
bytes RSS.  Both reproduced the frozen digest and exact metrics.

## Verification and review

`PYTHONDONTWRITEBYTECODE=1 python3 verify_operational.py` passed:

- static and browser-JavaScript gates;
- operational unit and independent-oracle gates;
- unconstrained and constrained million-item subprocess gates;
- the original `verify_all.py` regression suite; and
- source- and cache-mutation gates.

Adversarial tests reject forged feasibility/explanation fields, altered exact
metrics, altered constraint payloads with self-consistent digests, tuple or
wrong-width order storage, non-loopback serving, over-cap work, block reversal,
and within-category block gaps.  A 5,000-participant block preparation and
lower-bound canary runs in about 0.05 seconds under a 2-second gate.

The live browser run used keyboard input, native selection, and clicks for all
four compact constraint classes; checked the primary-`B` label, exact bounds,
ranked preview, digest, malformed JSON, recovery, and final visual layout.

The impact scanner ran in degraded lexical mode and reported HIGH/UNKNOWN due
generic symbols in a new isolated subtree; the complete project verifier covers
the actual package, CLI, server, and browser blast radius.  The security scanner
reported lexical REVIEW hits only on mathematical words such as `verify` and
`token`.  Manual review found no credentials, authentication, dynamic
evaluation, unsafe deserialization, user-controlled process execution, or new
runtime dependencies; subprocess calls are fixed benchmark/verifier commands.

## Honest remaining boundary

- The million-scale theorem is categorical/joint-stratum, not arbitrary-vector
  optimization or continuous star discrepancy.
- Constraints receive an input-specific interval, not a universal constant
  approximation factor.
- Rendering, finance, and laboratory presets remain demonstrations; no
  downstream time, money, accuracy, causal, clinical, or regulatory benefit has
  been measured.
- The UCI audit replay demonstrates one statistical prefix-estimation effect,
  not production-safe stopping, reviewer-time savings, workflow-cost savings, or
  realized monetary value.
- External novelty and publication claims still require specialist review.

## Next action

Accept and commit the Fable 5 repair baseline while preserving unrelated user
work. Only then begin production-relevant economic and safe-stopping validation.
Any message to Rogelio remains a separate user-approved action.

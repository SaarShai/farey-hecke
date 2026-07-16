# Final release gates

Date: 2026-07-16

## End-to-end verification

```text
PYTHONDONTWRITEBYTECODE=1 python3 projects/prime-step-breakthrough/verify_all.py
exit 0
60 unit tests passed
7 live HTTP tests passed
13/13 benchmark gates passed
artifact, cache, and mutation-boundary gates passed
```

Rendered keyboard/click/browser evidence is recorded separately in
`BROWSER_VERIFICATION.md`.

The multidimensional operational release separately passed:

```text
PYTHONDONTWRITEBYTECODE=1 python3 projects/prime-step-breakthrough/verify_operational.py
exit 0
static gate: PASS
browser JavaScript syntax gate: PASS
operational unit/oracle gate: PASS
million-item subprocess gate: PASS
million-item sparse-constraint gate: PASS
original verify_all regression gate: PASS
source-mutation gate: PASS
cache-mutation gate: PASS
OPERATIONAL VERIFICATION PASS
```

The constrained frozen order digest is
`3194a7661d0d90f6115bba41cfed1c506fd8f9442c0f54c0a8069ff90662c675`.
The stable full run took 4.135954 seconds at 46,546,944 bytes RSS under a hard
30-second subprocess timeout and 128-MiB ceiling.  The exact constraint payload
contains a repeated-category block and all four constraint classes.  The final
Sol-Ultra audit's required repairs were implemented, and the final independent
cold review returned **ACCEPT — no remaining blockers**.  See
`OPERATIONAL_REVIEWS.md` and `BROWSER_VERIFICATION_OPERATIONAL.md`.

## Specification-derived evaluation

`eval-gate` evaluated the full preprint against
`research/FINAL_EVAL_CRITERIA.json`, whose provenance is the frozen research
specification.  The installed `gemma4:31b-mlx` judge returned PASS with a
normalized score of 1.0 and passed all seven required criteria.  The requested
three-member verifier panel degraded to the single judge because none of its
configured panel members were reachable; it is not counted as panel evidence.
Independent Sol/xhigh and cold-verifier reviews are recorded in
`research/INDEPENDENT_REVIEWS.md`.

## Impact review

The final lexical impact tool reported HIGH/UNKNOWN because this is an all-new
Python subtree, no code graph includes it yet, and names such as `main` and
`error` collide textually across the repository.  A direct check found no
tracked pre-existing import or reference to `coprimebatch` or the new project.
The actual blast radius is therefore the new package, CLI, local HTTP service,
browser client, benchmark, and tests.  It is classified MEDIUM until external
users exercise the public API; all those paths are covered by the fresh suite
and live-browser run.

## Security review

The final scoped lexical scanner reported REVIEW only: words such as `verify`
and occurrence `token` were misclassified as authorization logic.  Manual
review found:

- no runtime dependencies, credentials, authentication, payment, dynamic
  evaluation, shell execution, or unsafe deserialization;
- the sole build requirement is the standard `setuptools>=68` backend;
- the HTTP server rejects every non-loopback bind, caps bodies at 1,000,000
  bytes, rejects unsupported methods, resolves static paths beneath its fixed
  web root, and applies pre-solve `C`, `N*C`, constraint-reference, block-width,
  and full-order caps; and
- malformed-input and path behavior is covered by the HTTP suite and live UI
  recovery checks.

No obvious introduced security defect remains.  This is a local research
service, not a hardened public multi-user deployment.

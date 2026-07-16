# Builder acceptance of the Fable 5 review

Date: 2026-07-16

This is the controlling disposition of `FABLE5_REVIEW.md` and
`BUILDER_HANDOFF_PACKET.md`. The original review was valuable but its security
closure and evidence reproducibility were incomplete. Acceptance therefore used
the review as an attack brief, not as a self-certifying verdict.

## Decisions

| Finding | Decision | Resolution |
|---|---|---|
| Theorem bridge, quota `<3`, binary mechanical exactness, constrained `L<=OPT_B<=U`, primary-B-only closure, determinism | Accept | Preserve mathematics and independent oracles; no algorithm change |
| Original positive-control bundle: bind/body/balance admission/traversal/method/JSON/digest/factorization integrity | Accept and preserve | Keep every control and regression; post-repair harness still exercises the interface subset |
| `PIN_SPLITS_BLOCK` versus expanded feasibility | Accept as declared restriction | Keep structural admission rule; document that it is not general infeasibility |
| Endpoint magnitude/count denial of service | Accept | Retain Fable count/span/factorization/exponent caps |
| Supplied exact-gap and prefactored-certificate bit complexity | Accept, found by final refutation | Add per-rational/per-denominator bit caps and aggregate exact bit-work proxies; reject before certificate/kernel entry |
| Optimize endpoint closure | Accept, original repair incomplete | Add a pre-solve trial-division budget over denominator magnitude and repeated samples; add a combined matrix/evaluation budget including `comb(C,L)*L^2` for automatic brute force; reduce returned random samples to 2,000 |
| DNS rebinding / browser compute drive | Accept, original repair incomplete | Retain strict loopback Host; reject malformed authorities, non-loopback Origin, and non-JSON POSTs |
| Slowloris/thread exhaustion | Accept | Retain 15-second socket timeout and 64-handler semaphore; clean disconnect tests and warnings |
| Oversized-body VULN label | Reject as a server defect; accept as harness defect | Correct the probe to declare an oversized body without transmitting it; live server returns 400 before read |
| Task 3/4 recorded results | Accept conclusion, reject old reproducibility | Make both runners self-contained; regenerate result JSON; include both known exact-solver traps |
| Operational documentation | Accept | Document Host/Origin/content-type, endpoint work caps, timeout/concurrency, direct-call boundary, and split-block scope |
| Browser `p=8501` default | Accept | Retain `p=257`, maximum 512 |
| Hard wall-clock cancellation/process isolation | Defer for local research release | Required before hosted or untrusted-network deployment; current release label remains loopback research software |
| Quota/binary category and `N*C` cap asymmetry | Accept and defer while 1 MB body cap remains | The measured 48,000-category request completed in about 0.21 seconds; reassess and add symmetric caps before raising the body cap or hosting |
| Lower the 64-connection cap | Reject without workload evidence | The existing finite bound is adequate for local research; hosted service requires a different architecture, not an arbitrary smaller number |
| Cap every direct Python/CLI call | Reject for the research core | Wrappers must impose their own budgets; preserve direct exact research access |
| Application/economic benefit and novelty claims | Accept as unresolved | Statistical UCI replay is not production-safe stopping or monetary evidence; external novelty review remains required |

## New admission model

The HTTP optimizer now rejects before any optimizer call when either conservative
work proxy exceeds its cap:

```text
trial_division_units = 5*sum(isqrt(candidate))
                     + samples*layers*max(isqrt(candidate))

kernel_cells = 2*C^2
             + (samples + 4 + exact_subset_count)*layers^2
```

`exact_subset_count = comb(C,layers)` only when the HTTP path would invoke its
automatic small-pool exact branch. Current caps are 5,000,000 trial-division
units and 1,000,000 matrix/evaluation cells. They are admission proxies, not
runtime guarantees; the server still lacks cancellable process isolation.

Supplied exact gaps and prefactored certificates are additionally bounded
before solver entry:

```text
gap_bit_work = N * (sum(bitlen(unique reduced denominators))
                    + max(bitlen(reduced numerator)))
gap_common_denominator_bits = bitlen(lcm(reduced denominators))

certificate_output_bits = sum(bitlen(denominator))
certificate_kernel_bit_cells = C*(C+1)/2 * certificate_output_bits
```

The current caps are 8,000,000 exact-gap bit-cells, 5,000 common-denominator
bits for supplied gaps, 4,096 bits per certificate denominator, 12,000
aggregate certificate exact-output bits, and 10,000,000 certificate kernel
bit-cells. The aggregate caps keep admitted exact numerator/denominator output
below Python's decimal integer-to-string safety limit. Each
factorization's exponent/prime bit proxy is also checked before its product is
materialized.

Measured accepted near-bound cases on this machine:

- explicit five-candidate, one-layer, 2,000-sample request: 0.021 seconds;
- benchmark candidates 2 through 514, ten layers: 1.273 seconds.

## Reproduced mathematical evidence

Fresh self-contained runners reported:

- quota constructor: 1,000 instances; zero violations; maximum observed ratio 2;
- binary mechanical path: 91 pairs; zero findings;
- constrained path: 500 accepted feasible instances, 1,830 infeasible
  agreements, 89 declared `PIN_SPLITS_BLOCK` restrictions, zero certificate or
  returned-constraint failures;
- general exact solver: 547 unique problems across scalar, rational, 2-D,
  variable-mass, and two known-trap families; zero errors/findings;
- determinism: 11 cases; zero findings.

## Live interface evidence

`review_fable5/iface/attack.py` now writes `results_post_repair.json` rather than
overwriting the historical pre-repair evidence. Fresh live result:

```text
HARDENED: 34
INFO: 2
VULN: 0
```

Formerly expensive shift/gap/optimizer requests fail with HTTP 400 in under one
millisecond. Huge optimizer magnitude, combined-work, and automatic-bruteforce
probes also fail before solve. The two final-refutation cases—100 distinct large
exact rational gaps and 18 valid prefactored large denominators—now fail in under
one millisecond before solver entry. Hostile Origin returns 403; the isolated
`loopback_origin_textplain_post` probe and
`test_post_rejects_hostile_origin_and_non_json_content_type` return 415; and a
declared 1,000,083-byte body returns 400 before body transmission.
The certificate probe just below its factorization budget completed in about
0.7 seconds and was classified bounded, not rejected.

## Completed acceptance gates

- focused arithmetic/HTTP hardening: 37 tests and 6,621 subtests passed with
  `ResourceWarning` promoted to error;
- full unit/oracle suite: 151 tests and 7,824 subtests passed;
- full operational verifier passed, including the frozen million-item
  constrained digest `3194a7661d0d90f6115bba41cfed1c506fd8f9442c0f54c0a8069ff90662c675`;
- independent security refuter: ACCEPT for the scoped loopback research release;
- independent evidence/claim reviewer: implementation and evidence accepted
  after the two stale test-count strings were corrected;
- cached Git scope contains only `projects/prime-step-breakthrough/`; unrelated
  projects, `.DS_Store`, caches, and ephemeral `iface/server.log` are excluded.

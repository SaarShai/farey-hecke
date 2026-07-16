# Fable 5 adversarial review — CoprimeBatch / prefix-balance optimizer

> Builder acceptance addendum: this review correctly found the original Host,
> endpoint-cap, exponent, and concurrency defects, but its closure was incomplete.
> The subsequent acceptance pass found optimize magnitude/combined-work,
> exact-rational/prefactored-kernel bit-work, and ordinary cross-origin compute
> gaps plus evidence-reproducibility defects. See
> `ACCEPTANCE_AND_REPAIRS.md` for the controlling final disposition.

Date: 2026-07-16
Repository: `/Users/za/Documents/farey-hecke`
Project: `projects/prime-step-breakthrough`
Mode: independent, refute-if-possible, repair-authorized (per
`artifacts/FABLE5_ADVERSARIAL_REVIEW_PACKET.md`)

This pass builds on two earlier in-tree adversarial workstreams
(`review_fable5/fuzz/REPORT.md` — math/solver correctness;
`review_fable5/iface/FINDINGS.md` — interface/security) and carries the
security findings through an end-to-end patch → regression-test →
independent-review → live-verification loop. Out-of-scope items from the packet
(external correspondence, publication, unrelated projects) were deliberately not
touched.

## 1. Claim verdicts

| Claim | Verdict | Evidence | Severity | Repair |
|---|---|---|---|---|
| Theorem 1 bridge `u_i = W·a_i − w_i·A`, `B/Q` normalization | holds | `tests/test_prefix_balance.py`, `solve_exact` matches brute force on 547 self-contained instances (`fuzz/REPORT.md §4`) | — | none |
| `quota_order` quota-valid + strict `<3` factor vs unconstrained OPT_B (≥2 positive cats) | holds | 1000 exhaustive instances, max ratio observed = 2 at counts `(2,1)` (`fuzz/REPORT.md §1`) | — | none |
| `quota_mechanical_order` prefixwise-exact `B` and `Q` (binary) | holds | 91 pairs `a+b≤12` match exhaustive lex optimum; lower word not minimax for `(1,4)` confirmed (`fuzz/REPORT.md §2`) | — | none |
| `solve_constrained_quota` certificate `L ≤ OPT_B ≤ U`, `U` = recomputed `B` | holds on accepted comparison set | 500 solver-accepted feasible instances, 0 interval/constraint/U failures (`fuzz/REPORT.md §3`) | — | none |
| `primary_optimum_proved` proves only primary `B`, not `Q` | holds | Certificate label `primary_B_only`; verified in interface tests | — | none |
| Pins partially covering a fixed block | uncertain → documented sharp edge | `PIN_SPLITS_BLOCK` rejects 89 instances the expanded oracle calls feasible; packet §5 lists this as unsupported (`fuzz/REPORT.md §3`) | low (contract clarity) | none needed; behavior matches declared scope |
| Determinism under dict-insertion / UTF-8 category order | holds | 11 instances identical codes/digest (`fuzz/REPORT.md §5`) | — | none |
| Loopback bind guard, 1 MB body cap, balance admission caps, static-traversal, method allow-list, JSON strictness, digest, factorization integrity | holds | `iface/FINDINGS.md` (20 HARDENED controls); `tests/test_http_api.py`, `tests/test_prefix_balance_interfaces.py` | — | none |
| Compute endpoints (`/api/gaps`,`/api/shift`,`/api/optimize`,`/api/certificate`) are safe under the "localhost research software" disclaimer | refuted | Uncapped magnitude → single-request CPU/RAM DoS; `iface/FINDINGS.md` VULN‑1; `iface/scaling.txt` | high (availability) | **fixed** — per-endpoint admission caps |
| Server safe against DNS-rebinding / cross-origin drive | refuted | No `Host`/`Origin` check; `iface/FINDINGS.md` VULN‑2 | medium | **fixed** — `Host` loopback allow-list |
| Server safe against slowloris / thread exhaustion | refuted | No socket timeout, unbounded threads; `iface/FINDINGS.md` VULN‑3, `iface/slowloris.py` | medium | **fixed** — socket timeout + bounded concurrency |
| `/api/certificate` trial-division budget bounds all factorization work | refuted (residual, found during repair) | Large factor **exponent** forces `prime**exponent` before product check → hang | medium | **fixed** — exponent ≤ `denominator.bit_length()` cap |
| Shipped browser shift default (`p=8501`, exact) is usable | refuted | Does not finish within 25 s exact; latent hang | low (UX/DoS) | **fixed** — default lowered to `p=257`, input `max=512` |

## 2. Repair → verification ledger

| Finding | Files changed | Regression test | Independent review | Live verification | Residual risk |
|---|---|---|---|---|---|
| VULN‑1 uncapped compute endpoints | `src/coprimebatch/web.py` (`_enforce_certificate_limits`, `_certificate`, `_optimize`, `_shift`, `_gaps`, caps) | `tests/test_http_api.py::test_compute_endpoints_reject_uncapped_work_before_solving` | security-review subagent (`a7dc8aeb`) | 4 DoS payloads (`shift p=4001`, `gaps 4000`, `optimize 2M`, `bench stop=6000`, `cert 1e18`) all fast-fail 400 in <12 ms against a live server | Direct Python/CLI callers are intentionally uncapped (packet §8); a client may still hold ≤64 trickled sockets within the 15 s per-read timeout |
| VULN‑2 DNS-rebinding / no Host check | `src/coprimebatch/web.py` (`_host_is_loopback`, `_reject_non_loopback_host`, `do_GET`/`do_POST`) | `tests/test_http_api.py::test_host_header_must_be_loopback`, `HostHeaderUnitTests` | final acceptance refuter found and closed a documentation mismatch | Live: `Host: attacker.example.com` → 403; loopback Host → 200 | Absent, blank, malformed, and non-loopback Host rejected |
| VULN‑3 slowloris / unbounded threads | `src/coprimebatch/web.py` (`Handler.timeout`, `_BoundedThreadingHTTPServer`, `serve`) | `tests/test_http_api.py::SlowConnectionHardeningTests` | security-review subagent (`a7dc8aeb`) | Bounded server drops connections beyond cap; semaphore released in `finally` | Up to 64 concurrent slow connections tolerated (bounded, was unbounded) |
| Certificate exponent DoS (residual) | `src/coprimebatch/web.py` (`_enforce_certificate_limits`) | `tests/test_http_api.py::test_compute_endpoints_reject_uncapped_work_before_solving` (999/3^60000000 case + valid 8=2^3 case) | security-review subagent (`8566a0fe`) — **CLOSED** | `999 → {3:60_000_000}` blocked in <1 ms; valid `8→{2:3}` still 200 | None for `/api/certificate`; direct kernel callers unaffected by interface cap |
| Supplied exact-gap / valid prefactored-kernel bit complexity (final residuals) | `src/coprimebatch/web.py` (`_bounded_gap_values`, `_enforce_certificate_limits`) | `test_exact_gap_bit_work_rejects_before_certificate_entry`, `test_certificate_bit_work_rejects_before_kernel_entry` | final security refuter reproduced 7.1 s and 2.3 s live requests; builder repaired and reran | Both new live probes → 400 in <1 ms; patched solver entry points assert not called | Direct Python/CLI remain outside HTTP caps by declared research contract |
| Browser shift default hang | `web/index.html` | Covered by `verify_operational.py` browser JS/static gate | — | Operational verifier browser gate PASS | None |

## 3. Verification output (fresh)

Full test suite:

```
python3 -m pytest tests/ -q
151 passed, 7824 subtests passed
```

Operational verifier (chains original `verify_all.py` regression + browser gate):

```
PYTHONDONTWRITEBYTECODE=1 python3 verify_operational.py
static gate: PASS
browser JavaScript syntax gate: PASS
operational unit/oracle gate: PASS
million-item subprocess gate: PASS
  positions=1000000 wall=1.53s digest=c92afcfc… (unconstrained)
million-item sparse-constraint gate: PASS
  positions=1000000 wall=4.25s digest=3194a766…1c506fd8f9442c0f54c0a8069ff90662c675 (matches frozen)
original verify_all regression gate: PASS
source-mutation gate: PASS
cache-mutation gate: PASS
OPERATIONAL VERIFICATION PASS
```

The frozen constrained order digest `3194a766…` is reproduced unchanged, so the
security hardening did not perturb the mathematical result.

## 4. Summary judgments (packet §14)

- **Strongest surviving mathematical result:** the categorical / fixed-queue
  constrained optimizer with an input-specific certificate `L ≤ OPT_B ≤ U` where
  `U` is the exact achieved primary discrepancy, `primary_optimum_proved` iff
  `L=U`, proving primary `B` only. This survived 2,330 constrained instances
  (500 feasible + 1,830 infeasible-agreements) and the exact `solve_exact` path
  survived 547 brute-force comparisons with zero counterexamples.
- **Strongest surviving operational result:** a deterministic, dependency-free
  million-item constrained scheduler with a self-recomputing certificate,
  reproducible digest, and — after this pass — a loopback HTTP surface whose
  every compute endpoint has an admission cap, a Host allow-list, and bounded
  concurrency.
- **Most dangerous untested assumption:** that category-prefix balance implies a
  downstream benefit. The application presets remain demonstrations; no time,
  money, accuracy, or clinical benefit has been measured. Balance of a category
  is not balance of the loss/error signal inside it.
- **Claims that must be removed/qualified before deployment or publication:** do
  not describe the HTTP service as safe for any untrusted network; it is
  loopback research software with residual same-host DoS surface (≤64 slow
  connections; uncapped direct Python callers). Do not let "constrained"
  optimality language imply a universal approximation constant — none exists for
  the constrained set. Novelty/priority claims still need specialist review.
- **Minimum next experiment:** one real integration with a preregistered
  interruption-prefix metric, comparing stable-order vs seeded-random vs this
  optimizer on identical jobs/workers — to test whether prefix balance produces
  a measurable downstream gain at all.
- **Release recommendation:**
  - Mathematics: **publishable at its stated (narrow) scope** — categorical /
    fixed-queue prefix optimization with exact certificates, pending specialist
    novelty review.
  - Software: **research software, now hardened** for local single-user use.
  - Product / domain: **not ready** — no validated downstream application.

## 5. Blocked / out-of-scope items

- External correspondence (e.g. any message to Rogelio) and publication remain
  user-owned actions — not performed.
- A hard per-request wall-clock budget and a total-thread ceiling below 64 would
  further reduce same-host DoS but require a work-queue redesign; left as a noted
  residual rather than an in-scope repair.
- Direct-Python / CLI callers are intentionally exempt from the interface caps
  per packet §8; not changed.

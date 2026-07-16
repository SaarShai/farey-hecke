# Builder handoff packet — Fable 5 adversarial review

> Superseded as a final closure decision by `ACCEPTANCE_AND_REPAIRS.md`. This
> packet remains the original reviewer handoff and evidence map.

Date: 2026-07-16  
Project: `projects/prime-step-breakthrough`  
Audience: the agent (or human) that built CoprimeBatch / the constrained
prefix-balance optimizer  
Authorization basis: `artifacts/FABLE5_ADVERSARIAL_REVIEW_PACKET.md`
(independent, refute-if-possible, repair-authorized)

Give this file to the builder first. It is the map. The detailed evidence lives
in the linked artifacts under `review_fable5/`.

---

## 0. One-paragraph verdict

The mathematical certificates and million-item constrained path survived
adversarial fuzzing with **no correctness counterexample** in budget. The
loopback HTTP research surface had three real availability / local-exposure
defects (uncapped compute endpoints, missing Host allow-list, unbounded
slowloris). Those were **repaired in-tree** with regression tests and
re-verified. Frozen constrained digest `3194a766…` still matches. Software is
research-grade and now hardened for local single-user use; domain claims remain
unvalidated. Release stance: **publishable math at stated scope** (pending
specialist novelty review); **research software hardened**; **not pilot-ready**.

---

## 1. What the builder should do with this packet

1. Read §2–§4 (findings + repairs already applied).
2. Diff / accept the three production files listed in §5.
3. Run the verify commands in §6; expect green.
4. Optionally absorb the documentation / residual items in §7–§8.
5. Do **not** weaken proofs or tests to make anything pass. Do **not** silently
   change the declared constrained comparison set.
6. External correspondence / publication remain user-owned — not authorized here.

---

## 2. Mathematics — what held (no code change required)

Full write-up: [`fuzz/REPORT.md`](fuzz/REPORT.md)  
Reproducer for the only sharp edge: [`fuzz/repro_findings.py`](fuzz/repro_findings.py)

| Claim | Verdict | Budget / witness |
|---|---|---|
| `quota_order` quota-valid + B-ratio &lt; 3 (scope: ≥2 positive cats) | **HOLDS** | 1000 instances; max ratio **2** at counts `(2,1)` |
| `quota_mechanical_order` prefix-optimal B and Q (binary) | **HOLDS** | 91 pairs `a+b≤12`; lower word on `(1,4)` confirmed **not** minimax |
| `solve_constrained_quota` `L ≤ OPT_B ≤ U` on **accepted** set | **HOLDS** | 500 feasible accepted; 1830 solver/oracle agree infeasible; 0 interval failures |
| `solve_exact` lex (B, Q) vs brute force | **HOLDS** | 547 unique instances |
| Determinism under dict insertion / UTF-8 names | **HOLDS** | 11 instances |
| `primary_optimum_proved` proves only primary B, not Q | **HOLDS** | Label `primary_B_only` consistent with code/UI |

**Documented sharp edge (not a silent math bug):**

- `PIN_SPLITS_BLOCK`: pins that only partially cover a fixed block are rejected
  while an expanded-order oracle may still call the instance feasible (89 random
  hits). This matches packet §5 (“arbitrary interior pins that split a block”
  unsupported). Builder action if desired: make docs/UI error text even sharper
  that this is a structural admission rule, not a feasibility oracle failure.

Independent oracles (`tests/prefix_balance_oracles.py`,
`tests/constrained_quota_oracles.py`) import **no** production code — treat as
trusted judges for small instances.

---

## 3. Interface / security — what was refuted and fixed

Pre-repair attack report: [`iface/FINDINGS.md`](iface/FINDINGS.md)  
Harnesses: `iface/attack.py`, `iface/scaling.py`, `iface/slowloris.py`,
`iface/verify_transport.py`

### 3.1 Pre-existing controls that held (do not regress)

Loopback bind guard; 1 MB body cap; constrained-quota admission caps; static
path traversal defense; method allow-list; duplicate-key JSON rejection;
SHA-256 order digest honesty; forged / non-prime factorization rejection.

### 3.2 Defects found and repaired

| ID | Severity | Defect | Root cause | Fix applied |
|---|---|---|---|---|
| VULN-1 | High (availability) | `/api/gaps`, `/api/shift`, `/api/optimize`, `/api/certificate` accept unbounded magnitudes → single-request CPU/RAM DoS; abandoned client leaves handler running | Caps existed only on `/api/balance` | Per-endpoint admission caps before solve (see §5 constants) |
| VULN-2 | Medium | No `Host` check → DNS-rebinding / cross-origin drive of compute | Bind guard ≠ Host allow-list | Reject non-loopback `Host`; 403 |
| VULN-3 | Medium | No socket timeout; unbounded `ThreadingHTTPServer` threads → slowloris | Default stdlib server | `Handler.timeout = 15s` + `_BoundedThreadingHTTPServer` (64 concurrent) |
| Residual | Medium → **closed** | Certificate budget counted factor **bases** but not **exponents**; `{"999":{"3":60000000}}` forced huge `prime**exponent` before product mismatch | Validation materializes `prime**exponent` | Reject `exponent > max(denominator.bit_length(), 1)` before kernel |
| UX | Low | Browser default shift `p=8501` exact never finishes (~25s+ hang) | Uncapped UI default above new `SHIFT_PRIME_CAP` | Default `257`, input `max=512` |

Live post-fix: DoS payloads that previously ran 20–35s (or hung) now return
**400 in &lt;12 ms**. Spoofed Host → **403**. Frozen million-item constrained
digest unchanged.

Independent security re-review after the exponent fix: residual **CLOSED**.

---

## 4. Claim table (packet §14 format)

| claim | holds/refuted/uncertain | evidence | severity | repair |
|---|---|---|---|---|
| Theorem 1 / B,Q normalization | holds | unit + exact fuzz | — | none |
| quota_order &lt;3 factor | holds | fuzz 1000; max ratio 2 | — | none |
| mechanical binary exact | holds | fuzz 91 | — | none |
| constrained L≤OPT_B≤U (accepted set) | holds | fuzz 500 | — | none |
| PIN_SPLITS_BLOCK vs expanded feasible | uncertain→documented | fuzz 89; repro script | low | docs only if desired |
| compute endpoints capped | was refuted → holds after fix | iface + live + tests | was high | applied |
| Host loopback allow-list | was refuted → holds after fix | iface + tests | was medium | applied |
| slowloris bound | was refuted → holds after fix | iface + tests | was medium | applied |
| certificate exponent budget | was refuted → holds after fix | security re-review | was medium | applied |
| application / domain benefit | uncertain / unvalidated | `APPLICATION_VALIDATION.md` | high for product claims | do not claim |

---

## 5. Files the builder must treat as part of the repair

### Production / UI (already patched in working tree)

| File | What changed |
|---|---|
| `src/coprimebatch/web.py` | Caps; `_enforce_certificate_limits` (incl. exponent); `_host_is_loopback` / reject; `Handler.timeout`; `_BoundedThreadingHTTPServer`; `serve` uses bounded server |
| `web/index.html` | Shift default `p=257`, `max=512`; farey-order `max=512` |
| `tests/test_http_api.py` | Regression: over-cap endpoints, Host spoof, socket timeout, concurrency drop, exponent DoS + valid factorization |

### New review artifacts (evidence; keep in tree)

| Path | Role |
|---|---|
| `review_fable5/BUILDER_HANDOFF_PACKET.md` | **This file** — start here |
| `review_fable5/FABLE5_REVIEW.md` | Full Fable 5 claim + repair ledger |
| `review_fable5/fuzz/*` | Solver-vs-oracle adversarial suite + `REPORT.md` |
| `review_fable5/iface/*` | Pre-repair interface attack suite + `FINDINGS.md` |

### Cap constants (HTTP layer only; direct Python uncapped by design)

```text
GAP_FAREY_ORDER_CAP = 512
GAP_SUPPLIED_COUNT_CAP = 20_000
GAP_SUPPLIED_EXACT_WORK_BIT_CAP = 8_000_000
GAP_SUPPLIED_COMMON_DENOMINATOR_BIT_CAP = 5_000
SHIFT_PRIME_CAP = 512
SHIFT_MAX_ORDER_CAP = 12
OPTIMIZE_CANDIDATE_CAP = 64
OPTIMIZE_SAMPLE_CAP = 2_000
OPTIMIZE_TRIAL_DIVISION_BUDGET = 5_000_000
OPTIMIZE_KERNEL_WORK_CELL_CAP = 1_000_000
OPTIMIZE_BENCHMARK_SPAN_CAP = 512
CERTIFICATE_DENOMINATOR_COUNT_CAP = 256
CERTIFICATE_DENOMINATOR_BIT_CAP = 4_096
CERTIFICATE_OUTPUT_INTEGER_BIT_CAP = 12_000
CERTIFICATE_KERNEL_BIT_CELL_CAP = 10_000_000
CERTIFICATE_TRIAL_DIVISION_BUDGET = 50_000_000   # sum of isqrt(bases)
SOCKET_TIMEOUT_SECONDS = 15.0
MAX_CONCURRENT_CONNECTIONS = 64
```

Factorization rules: for each supplied factor of denominator `d`, require
`exponent ≤ max(d.bit_length(), 1)` and total
`sum(exponent*bit_length(base)) ≤ 2*bit_length(d)` before calling
`portfolio_certificate`.

---

## 6. How to re-verify (builder acceptance gate)

From `projects/prime-step-breakthrough`:

```bash
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH=src:tests

# Focused hardening regressions
python3 -m pytest tests/test_http_api.py -q

# Full unit/oracle suite (expect 151 passed)
python3 -m pytest tests/ -q

# Operational chain (static, browser JS, million-item, verify_all, mutation)
python3 verify_operational.py
```

Expected operational signal includes:

```text
OPERATIONAL VERIFICATION PASS
...
digest=3194a7661d0d90f6115bba41cfed1c506fd8f9442c0f54c0a8069ff90662c675
```

Optional math fuzz re-run:

```bash
export PYTHONPATH=src:tests:review_fable5/fuzz
python3 review_fable5/fuzz/task1_quota_order.py
python3 review_fable5/fuzz/task2_mechanical.py
python3 review_fable5/fuzz/task3_constrained.py
python3 review_fable5/fuzz/task4_solve_exact.py
python3 review_fable5/fuzz/task5_determinism.py
python3 review_fable5/fuzz/repro_findings.py
```

Optional live DoS smoke (server on 127.0.0.1): payloads with `farey_order=4000`,
`p=4001`, `samples=2000000`, `stop=6000`, huge certificate denominators must
**400 immediately**, not compute.

---

## 7. Residual risk the builder should own going forward

1. **Same-host DoS residual:** up to 64 trickled connections can still park
   workers within the 15 s per-read timeout. A hard wall-clock work queue was
   **not** added (would be a larger redesign). Acceptable for loopback research
   software; do not call this production-hardened.
2. **Direct Python / CLI uncapped:** interface caps apply to HTTP (and balance
   CLI path for constrained-quota resource limits). Raw `kernel` /
   `farey_shift_moments` / `farey_gaps` callers can still burn the machine —
   intentional per original contract.
3. **`PIN_SPLITS_BLOCK` documentation:** behavior is correct per V1 contract;
   expand user-facing error copy if operators confuse it with infeasibility.
4. **Application claims:** presets are demonstrations only. Category-prefix
   balance ≠ downstream accuracy / money / clinical benefit. Do not ship
   monetary or domain-validation language without a preregistered experiment.
5. **Novelty / publication:** external specialist review still required;
   this pass does not certify priority over classical ingredients.

---

## 8. Recommended next actions for the builder (priority order)

1. **Accept / commit** the three patched files + review artifacts when the user
   asks for a commit (not done by the reviewer).
2. **Update docs** that still say only balance has admission caps:
   `OPERATIONAL_STATE.md`, `OPERATIONAL_ARCHITECTURE.md`, README security notes
   — state that research compute endpoints are now capped similarly, Host-checked,
   and concurrency-bounded.
3. **Optional hardening** (not blocking research release): per-request wall-clock
   cancel; Origin/custom-header for POST; lower `MAX_CONCURRENT_CONNECTIONS` if
   desired.
4. **Minimum domain experiment** before any pilot language: same jobs, same
   workers, preregistered interruption-prefix metric, baselines =
   stable-order vs seeded-random vs optimizer.

---

## 9. Summary judgments (for the builder’s state docs)

| Layer | Recommendation |
|---|---|
| Mathematics | Credible at stated scope: categorical / fixed-queue optimizer with input-specific `L≤OPT_B≤U`, primary-B-only closure |
| Implementation / certificates | Credible; fuzz + frozen digest + mutation gates green after hardening |
| Interfaces | Loopback research software; previously overstated relative to uncapped endpoints — **now repaired** |
| Applications | Not ready; no measured downstream benefit |
| Release label | **Research software (hardened) + publishable math sketch at narrow scope** — not pilot-ready product |

---

## 10. Artifact index (give the builder the whole folder)

```text
review_fable5/
  BUILDER_HANDOFF_PACKET.md   ← you are here
  FABLE5_REVIEW.md            ← full claim/repair ledger
  fuzz/
    REPORT.md                 ← math adversarial results
    task*.py, results_*.json, repro_findings.py, common.py
  iface/
    FINDINGS.md               ← pre-repair interface/security results
    attack.py, results.json, results_post_repair.json, scaling.py, scaling.txt
    slowloris.py, verify_transport.py, transport.txt
```

Upstream context the builder already knows:

- `artifacts/FABLE5_ADVERSARIAL_REVIEW_PACKET.md` — original mission
- `OPERATIONAL_STATE.md`, `IMPLEMENTATION_CONTRACT.md`, `OPERATIONAL_ARCHITECTURE.md`
- `paper/MULTIDIMENSIONAL_PREFIX_BALANCE.md`
- `artifacts/APPLICATION_VALIDATION.md`

---

## 11. What was intentionally not done

- No commit / push / PR (user must request).
- No message to external contacts; no publication.
- No weakening of proof obligations or comparison-set definitions.
- No change to unconstrained / constrained mathematical algorithms beyond HTTP
  admission and UI defaults.
- No production multi-user deployment stack (auth, TLS, rate limits, process
  isolation) — still out of scope for this research tool.

End of builder handoff packet.

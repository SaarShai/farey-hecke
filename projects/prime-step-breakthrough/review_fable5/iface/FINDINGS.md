# Adversarial interface/security review — CoprimeBatch loopback HTTP API

> Historical pre-repair report. The builder acceptance pass found and repaired
> additional optimize combined-work and cross-origin gaps. Current live results
> are in `results_post_repair.json`: **34 HARDENED, 2 INFO, 0 VULN**. The old
> `results.json` labeled `body_over_cap` VULN because the client hit BrokenPipe
> while the server rejected before reading; the corrected probe declares the
> oversized length without sending a body and receives HTTP 400 in under 1 ms.
> Final refutation added compact exact-gap and valid-prefactored-certificate
> bit-complexity probes; both now receive HTTP 400 before solver entry in under
> 1 ms on the recorded run.

Target: `src/coprimebatch/web.py` (dependency-free `ThreadingHTTPServer`) and the
`balance` interface shared with `cli.py`. All probes are read-only against the
shipped package; nothing under `src/`, `tests/`, `web/`, or the verify scripts
was modified. Reproduction scripts and raw output live in this folder.

Server under test: `python3 -m coprimebatch.web --host 127.0.0.1 --port 8765`
(Python 3.14.6, macOS).

## TL;DR

The advertised posture holds where it is defined: the loopback bind guard, the
1 MB body cap, the five `/api/balance` admission caps, static-path traversal
defense, method allow-listing, JSON strictness (duplicate-key rejection), the
SHA-256 order digest, and user-supplied-factorization validation all behave as
claimed.

The real gap is **scope**: the admission caps only protect `/api/balance`. The
other four compute endpoints — `/api/certificate`, `/api/optimize`,
`/api/shift`, `/api/gaps` — accept **unbounded** numeric inputs and do
super-linear exact-arithmetic work, so a single tiny request is a reliable
CPU/RAM denial of service. On top of that, the server does DNS-rebinding /
cross-origin requests with no `Host`/`Origin` validation, and has no socket
timeout or worker-thread bound (slowloris). These are consistent with, but not
fully captured by, the "no auth/TLS, localhost research software" disclaimer.

Historical verdict tally from `results.json`: 20 HARDENED, 7 VULN, 3 INFO
(+ slowloris VULN, + scaling evidence). One of those seven, `body_over_cap`, was
a harness-classification defect rather than a server bypass, as noted above.

---

## VULN-1 (High for availability): uncapped compute endpoints → trivial DoS

The documented caps (`<=256` categories, `<=8,000,000` `N*C` cells, `<=10,000`
occurrence refs, `<=1024` per block, plus the 1 MB body cap) are enforced only
inside `balance_response`. The four other endpoints validate types and lower
bounds but set **no upper bound** on the magnitude or count of their inputs:

| Endpoint | Unbounded input | Backing cost | Where |
|---|---|---|---|
| `/api/gaps` | `farey_order` | `farey_gaps` materialises ~`0.30 * order^2` `Fraction`s | `gap_permutation.py:300` |
| `/api/shift` | `p` (and `max_order`) | `farey_shift_moments` is `O(p^2)` exact-`Fraction` moment loop | `shear.py:42` |
| `/api/optimize` | `samples` | `random_portfolio_baselines` runs `samples` evaluations, no cap | `web.py:212`, `optimizer.py:199` |
| `/api/optimize` (`benchmark`) | `start`/`stop` | `_kernel_matrix` is `O((stop-start)^2)` | `optimizer.py:66` |
| `/api/certificate` | denominator magnitude | `factorint` is `O(sqrt n)` trial division | `arithmetic.py:23` |

Measured wall-clock (see `scaling.txt`), from the live server:

```
gaps  farey_order 200->1600 : 0.14s -> 0.64s -> 3.69s -> 22.19s   (~n^2.6 observed)
shift p          251->2003  : 0.18s -> 0.87s -> 4.95s -> 34.52s
optimize samples 10k->160k  : 0.34s -> 1.40s -> 5.66s
certificate      1e10->1e14 : 0.01s -> 0.02s -> 0.23s prime (sqrt growth; 1e18 ~ minutes)
```

The four "30s+" probes in the main harness (`shift p=4001`, `gaps
farey_order=4000`, `optimize samples=2,000,000`, `optimize benchmark stop=6000`)
each hit the client's 30 s timeout. Critically, **the work continues after the
client disconnects** — Python does not cancel the handler thread. Immediately
after the DoS burst the server process was measured at:

```
PID    %CPU    RSS
16308  99.8    1492688 KB  (~1.49 GB)
```

i.e. one abandoned request left the server pinned at 100% CPU and ~1.5 GB RAM.
Under the GIL, CPU-bound handler threads also degrade every concurrent request.
A handful of these requests exhausts the host.

Secondary observation: for `exact=True` (the default) `/api/shift` with `p`
around 2000 aborts with `"Exceeds the limit (4300 digits) for integer string
conversion"` — the exact moment sums overflow CPython's int→str guard during
JSON serialization. It returns HTTP 400, but only *after* paying the full
`O(p^2)` cost, so it is still a DoS and additionally surfaces an internal
CPython limit to the client.

Fix direction: apply per-endpoint admission caps (max `farey_order`, max `p`,
max `max_order`, max `samples`, max `stop-start`, max denominator bit-length /
require supplied factorizations above a threshold) mirroring what
`_enforce_constrained_quota_resource_limits` already does for balance; and/or run
solves in a worker with a wall-clock budget.

Repro: `python3 review_fable5/iface/scaling.py`; `attack.py` cases in category
`dos-uncapped`.

## VULN-2 (Medium): no `Host` / `Origin` validation → DNS-rebinding & CSRF surface

`do_GET` / `do_POST` never inspect the `Host` or `Origin` request headers.

- `GET /api/health` with `Host: attacker.example.com` returns 200
  (`host_header_spoof`). The loopback *bind* stops direct remote TCP, but it does
  not stop a **DNS-rebinding** attack: a malicious page whose domain re-resolves
  to `127.0.0.1` will pass the browser's same-origin check against its own
  origin and reach this API. A `Host`-allowlist (`127.0.0.1`/`localhost` only)
  is the standard mitigation for local-only servers and is absent.
- `POST /api/balance` sent as a cross-origin `text/plain` "simple request" with
  `Origin: http://attacker.example.com` is processed and returns 200
  (`cross_origin_textplain_post`) — the body is parsed regardless of
  `Content-Type`. No CORS headers are emitted (`cors_header_probe`), so a
  browser cannot *read* the response cross-origin, which bounds this to a
  compute/DoS trigger rather than data theft — but combined with VULN-1 it means
  any web page the user visits can drive the expensive endpoints.

Fix direction: reject requests whose `Host` is not in the loopback allow-list;
optionally require a same-origin/absent `Origin` and a custom header for POSTs.

## VULN-3 (Medium): no socket timeout / no worker-thread bound → slowloris

`Handler` sets no `timeout`, and `serve()` uses a plain `ThreadingHTTPServer`
with no cap on concurrent threads. `_body()` calls
`request.rfile.read(Content-Length)`, which blocks until the declared bytes
arrive. A client can declare a body just under the 1 MB cap and then trickle it,
parking a dedicated server thread (and its buffer) indefinitely.

`slowloris.py` opened 8 connections each declaring 900,000 bytes while sending
~30, and the server held **8/8 for the full 8 s window with no timeout**:

```
t=1s..8s: 8/8 slow connections still accepted by server
held 8/8 connections for 8.0s with no server-side timeout -> VULN
```

There is no bound on how many such threads accumulate; enough of them exhaust
memory / thread limits. Fix direction: set `Handler.timeout` (and a body read
deadline), and cap concurrent connections.

## Non-bypass PROBE (Low): quota/binary mode has no category or `N*C` cap

Unlike `constrained-quota`, `quota`/`binary` mode only enforces the 5 M total-
item cap in `_counts`; there is no category-count or `N*C` limit. 48,000
single-item categories build in ~0.20 s (`quota_many_categories_48k`). This is
*incidentally* bounded by the 1 MB body cap (≈48–60 k categories max), so it is
not a strong standalone DoS, but the asymmetry with the constrained path is worth
noting if the body cap is ever raised.

---

## Confirmed HARDENED (positive controls)

- **Bind guard** — `--host 0.0.0.0` / `10.0.0.5` refused; only `127.0.0.1`,
  `localhost`, `::1` accepted (`_loopback_host`). See shell transcript.
- **Body cap** — a >1,000,000-byte declared body is rejected before read
  (`body_over_cap`); negative and non-integer `Content-Length` → 400.
- **Balance admission caps** — all four enforced: 300 categories → 400;
  `N*C=12M` → 400; block width 10,999 → 400; quota 5,000,001 items → 400.
- **Static traversal** — `/../../../../etc/passwd`, `//etc/passwd`, `/../web.py`,
  `/%2e%2e/...`, `/../src/coprimebatch/web.py` all → 404, nothing leaked
  (`_serve_static` `.resolve()` + `ROOT in parents` check).
- **Method handling** — `PUT`/`DELETE` → 405; non-`/api/` POST → 404.
- **JSON strictness** — duplicate top-level key → 400 (`_unique_json_object`);
  array body → 400; invalid UTF-8 → 400.
- **Transport honesty** — a full 10-item quota order's advertised `sha256`
  exactly matches an independent `uint32-big-endian` recomputation
  (`transport.txt`); `full_order=true` above 10,000 items → 400; large orders
  return `included:false` + preview + digest.
- **Factorization integrity** — a forged factorization (`15 = 7^1`) → 400
  ("product does not match"); a non-prime factor base (`12 = 4·3`) → 400
  ("factor bases must be prime"). `_validate_factorizations` cannot be tricked
  into certifying a wrong kernel.

---

## Files

- `attack.py` — main probe harness (writes `results_post_repair.json`).
- `results_post_repair.json` — current machine-readable post-repair results.
- `results.json` — historical pre-repair machine-readable results.
- `slowloris.py` — connection-holding / no-timeout probe.
- `scaling.py` / `scaling.txt` — super-linear cost measurements for VULN-1.
- `verify_transport.py` / `transport.txt` — digest + factorization positive controls.
- `server.log` — ephemeral local server stdout; intentionally not committed.

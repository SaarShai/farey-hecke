#!/usr/bin/env python3
"""Adversarial interface probes against the CoprimeBatch loopback HTTP server.

Read-only w.r.t. the shipped package: this only sends HTTP requests and inspects
the responses. Post-repair findings are written to results_post_repair.json so
the historical results.json remains intact. Every request uses a client-side
timeout so a successful denial-of-service on the server does not hang this
harness.
"""

from __future__ import annotations

import http.client
import json
import socket
import time
from math import log2
from pathlib import Path
from typing import Any

HOST = "127.0.0.1"
PORT = 8765
BASE = f"http://{HOST}:{PORT}"
OUT = Path(__file__).with_name("results_post_repair.json")

RESULTS: list[dict[str, Any]] = []


def raw_request(
    method: str,
    path: str,
    body: bytes | None = None,
    headers: dict[str, str] | None = None,
    timeout: float = 10.0,
) -> dict[str, Any]:
    """Send one request with a hard client timeout; report status/time/snippet."""
    conn = http.client.HTTPConnection(HOST, PORT, timeout=timeout)
    started = time.perf_counter()
    try:
        conn.request(method, path, body=body, headers=headers or {})
        resp = conn.getresponse()
        data = resp.read(4_000_000)
        elapsed = time.perf_counter() - started
        text = data.decode("utf-8", "replace")
        return {
            "status": resp.status,
            "elapsed_s": round(elapsed, 4),
            "body": text[:800],
            "full_body": text,
            "timed_out": False,
            "client_error": None,
        }
    except socket.timeout:
        return {
            "status": None,
            "elapsed_s": round(time.perf_counter() - started, 4),
            "body": "",
            "full_body": "",
            "timed_out": True,
            "client_error": "timeout",
        }
    except Exception as exc:  # noqa: BLE001 - report any client-visible failure
        return {
            "status": None,
            "elapsed_s": round(time.perf_counter() - started, 4),
            "body": f"{type(exc).__name__}: {exc}",
            "full_body": "",
            "timed_out": False,
            "client_error": f"{type(exc).__name__}: {exc}",
        }
    finally:
        conn.close()


def post_json(path: str, payload: Any, timeout: float = 10.0) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    return raw_request(
        "POST",
        path,
        body=body,
        headers={"Content-Type": "application/json"},
        timeout=timeout,
    )


def declared_oversize_request(length: int) -> dict[str, Any]:
    """Declare an oversized body without transmitting it; expect immediate 400."""

    started = time.perf_counter()
    with socket.create_connection((HOST, PORT), timeout=5) as connection:
        connection.settimeout(5)
        connection.sendall(
            (
                "POST /api/balance HTTP/1.1\r\n"
                f"Host: {HOST}:{PORT}\r\n"
                "Content-Type: application/json\r\n"
                f"Content-Length: {length}\r\n"
                "Connection: close\r\n\r\n"
            ).encode("ascii")
        )
        response = bytearray()
        while True:
            chunk = connection.recv(4096)
            if not chunk:
                break
            response.extend(chunk)
    status_line = bytes(response).split(b"\r\n", 1)[0].decode("ascii", "replace")
    parts = status_line.split()
    status = int(parts[1]) if len(parts) >= 2 and parts[1].isdigit() else None
    return {
        "status": status,
        "elapsed_s": round(time.perf_counter() - started, 4),
        "body": bytes(response[-800:]).decode("utf-8", "replace"),
        "full_body": bytes(response).decode("utf-8", "replace"),
        "timed_out": False,
        "client_error": None,
    }


def record(name: str, category: str, detail: str, result: dict[str, Any], verdict: str) -> None:
    RESULTS.append(
        {
            "name": name,
            "category": category,
            "detail": detail,
            "verdict": verdict,
            "result": result,
        }
    )
    flag = {"VULN": "!!", "HARDENED": "ok", "INFO": "..", "WEAK": "?!"}.get(verdict, "  ")
    t = result.get("elapsed_s")
    print(f"[{flag}] {name:<38} status={result.get('status')} t={t}s to={result.get('timed_out')}")


# --------------------------------------------------------------------------
# 1. Health / baseline
# --------------------------------------------------------------------------
def test_baseline() -> None:
    r = raw_request("GET", "/api/health")
    record("health_baseline", "baseline", "GET /api/health", r,
           "HARDENED" if r["status"] == 200 else "INFO")


# --------------------------------------------------------------------------
# 2. Host / Origin header handling (DNS-rebinding & CSRF surface)
# --------------------------------------------------------------------------
def test_host_origin() -> None:
    # Spoofed Host header: a DNS-rebinding attacker's page resolves evil.com to
    # 127.0.0.1 and the browser sends Host: evil.com. Server must reject or the
    # rebind reaches the API.
    r = raw_request("GET", "/api/health", headers={"Host": "attacker.example.com"})
    record("host_header_spoof", "dns-rebind",
           "GET /api/health with Host: attacker.example.com",
           r, "VULN" if r["status"] == 200 else "HARDENED")

    # Cross-origin POST (text/plain simple request; no CORS preflight). The
    # server parses the body regardless of Content-Type and returns a result.
    body = json.dumps({"mode": "quota", "counts": {"A": 1, "B": 1}}).encode()
    r = raw_request("POST", "/api/balance", body=body,
                    headers={"Content-Type": "text/plain",
                             "Origin": "http://attacker.example.com"})
    record("cross_origin_textplain_post", "csrf",
           "POST /api/balance as text/plain with hostile Origin",
           r, "VULN" if r["status"] == 200 else "HARDENED")

    # Isolate the content-type control from Origin ordering: a loopback Origin
    # with text/plain must receive 415 rather than execute.
    r = raw_request(
        "POST",
        "/api/balance",
        body=body,
        headers={"Content-Type": "text/plain", "Origin": BASE},
    )
    record(
        "loopback_origin_textplain_post",
        "csrf",
        "POST /api/balance as text/plain with loopback Origin",
        r,
        "HARDENED" if r["status"] == 415 else "VULN",
    )

    # Does the server emit any CORS headers? (informational)
    r = raw_request("GET", "/api/health", headers={"Origin": "http://attacker.example.com"})
    record("cors_header_probe", "csrf",
           "check for Access-Control-* on health", r, "INFO")


# --------------------------------------------------------------------------
# 3. Content-Length / body-cap handling
# --------------------------------------------------------------------------
def test_body_cap() -> None:
    # Oversized body (declared > 1,000,000): must be rejected pre-read.
    declared_length = 1_000_083
    r = declared_oversize_request(declared_length)
    record("body_over_cap", "body-cap",
           f"declared POST body {declared_length} bytes (> 1,000,000), no body sent",
           r, "HARDENED" if r["status"] == 400 else "VULN")

    # Body just under the cap of harmless whitespace -> should parse.
    ok = b'{"mode":"quota","counts":{"A":1,"B":1}}'
    ok = ok[:-1] + b"," + b'"C":1}'  # noqa (still valid JSON)
    r = raw_request("POST", "/api/balance",
                    body=b'{"mode":"quota","counts":{"A":1,"B":1}}',
                    headers={"Content-Type": "application/json"})
    record("body_under_cap", "body-cap", "normal small body", r,
           "HARDENED" if r["status"] == 200 else "INFO")

    # Negative Content-Length (manually crafted; overrides auto length).
    r = raw_request("POST", "/api/balance", body=b"{}",
                    headers={"Content-Type": "application/json",
                             "Content-Length": "-1"})
    record("content_length_negative", "body-cap",
           "Content-Length: -1", r,
           "HARDENED" if r["status"] in (400, 200) and not r["timed_out"] else "INFO")

    # Non-integer Content-Length.
    r = raw_request("POST", "/api/balance", body=b"{}",
                    headers={"Content-Type": "application/json",
                             "Content-Length": "abc"})
    record("content_length_nonint", "body-cap",
           "Content-Length: abc", r,
           "HARDENED" if not r["timed_out"] else "INFO")


# --------------------------------------------------------------------------
# 4. Balance admission caps + bypass attempts
# --------------------------------------------------------------------------
def test_balance_caps() -> None:
    # 4a. constrained-quota category cap (> 256).
    counts = {f"c{i}": 1 for i in range(300)}
    payload = {"mode": "constrained-quota", "counts": counts, "constraints": {}}
    r = post_json("/api/balance", payload)
    record("cq_category_cap_300", "balance-cap",
           "constrained-quota 300 categories (cap 256)", r,
           "HARDENED" if r["status"] == 400 else "VULN")

    # 4b. constrained-quota N*C cell cap (> 8,000,000). 200 cats * 60k = 12M.
    counts = {f"c{i}": 60000 for i in range(200)}
    payload = {"mode": "constrained-quota", "counts": counts, "constraints": {}}
    r = post_json("/api/balance", payload)
    record("cq_cell_cap_12M", "balance-cap",
           "constrained-quota N*C=12,000,000 (cap 8M)", r,
           "HARDENED" if r["status"] == 400 else "VULN")

    # 4c. occurrence-reference cap (> 10,000) via one huge fixed block.
    counts = {"a": 200000}
    occ = [{"category": "a", "occurrence": i} for i in range(1, 11000)]
    payload = {"mode": "constrained-quota", "counts": counts,
               "constraints": {"fixed_blocks": [{"block_id": "b", "occurrences": occ}]}}
    r = post_json("/api/balance", payload)
    record("cq_block_width_11000", "balance-cap",
           "constrained-quota fixed block width 10,999 (cap 1024)", r,
           "HARDENED" if r["status"] == 400 else "VULN")

    # 4d. quota-mode total-item cap (> 5,000,000).
    payload = {"mode": "quota", "counts": {"A": 5_000_001}}
    r = post_json("/api/balance", payload)
    record("quota_item_cap_5M", "balance-cap",
           "quota total 5,000,001 items (cap 5M)", r,
           "HARDENED" if r["status"] == 400 else "VULN")

    # 4e. PROBE: quota/binary mode has NO category-count cap and NO N*C cap
    # (only the 5M item total and the 1MB body cap apply). ~48k single-item
    # categories fit under the body cap and force an O(N log C) build.
    counts = {f"k{i:06d}": 1 for i in range(48000)}
    payload = {"mode": "quota", "counts": counts}
    r = post_json("/api/balance", payload, timeout=20.0)
    record("quota_many_categories_48k", "balance-cap-bypass",
           "quota 48,000 distinct categories (no category cap in quota mode)",
           r, "WEAK" if (r["status"] == 200 and r["elapsed_s"] > 0.5) else "INFO")


# --------------------------------------------------------------------------
# 5. Regression probes for formerly uncapped compute endpoints
# --------------------------------------------------------------------------
def test_dos_endpoints() -> None:
    # 5a. /api/certificate: factorint is O(sqrt n) trial division; a large prime
    # denominator with no supplied factorization forces a long factor scan.
    # 10**15+37 is prime; sqrt ~ 3.16e7 iterations.
    r = post_json("/api/certificate", {"denominators": [10**15 + 37]}, timeout=30.0)
    record("cert_large_prime_1e15", "dos-uncapped",
           "certificate denominators=[10**15+37] (trial-division factor)", r,
           "HARDENED" if not r["timed_out"] and r["elapsed_s"] < 2.0 else "VULN")

    # 5b. /api/shift: farey_shift_moments is O(p^2) exact-Fraction work.
    r = post_json("/api/shift", {"p": 4001, "max_order": 6}, timeout=30.0)
    record("shift_p_4001", "dos-uncapped",
           "shift p=4001 (O(p^2) Fraction moment loop)", r,
           "HARDENED" if r["status"] == 400 and r["elapsed_s"] < 2.0 else "VULN")

    # 5c. /api/gaps: farey_gaps(order) materialises ~0.30*order^2 fractions.
    r = post_json("/api/gaps", {"farey_order": 4000}, timeout=30.0)
    record("gaps_farey_order_4000", "dos-uncapped",
           "gaps farey_order=4000 (~4.8M fractions materialised)", r,
           "HARDENED" if r["status"] == 400 and r["elapsed_s"] < 2.0 else "VULN")

    # 5d. /api/optimize: excessive samples must be rejected before evaluation.
    r = post_json("/api/optimize",
                  {"candidates": [2, 3, 5, 7, 11], "layers": 3, "samples": 2_000_000},
                  timeout=30.0)
    record("optimize_samples_2M", "dos-uncapped",
           "optimize samples=2,000,000 (uncapped baseline loop)", r,
           "HARDENED" if r["status"] == 400 and r["elapsed_s"] < 2.0 else "VULN")

    # 5e. /api/optimize benchmark: start/stop uncapped -> O((stop-start)^2) kernel.
    r = post_json("/api/optimize",
                  {"benchmark": True, "start": 2, "stop": 6000, "layers": 10},
                  timeout=30.0)
    record("optimize_benchmark_stop_6000", "dos-uncapped",
           "optimize benchmark stop=6000 (O(range^2) kernel matrix)", r,
           "HARDENED" if r["status"] == 400 and r["elapsed_s"] < 2.0 else "VULN")

    # 5f. A tiny candidate list with a huge denominator must not bypass the
    # count/span caps and reach trial division.
    r = post_json(
        "/api/optimize",
        {"candidates": [(1 << 61) - 1], "layers": 1, "samples": 1},
    )
    record(
        "optimize_huge_candidate",
        "dos-combined-work",
        "optimize one huge candidate (trial-division magnitude)",
        r,
        "HARDENED" if r["status"] == 400 and r["elapsed_s"] < 2.0 else "VULN",
    )

    # 5g. Individually legal parameters can combine into excessive work.
    r = post_json(
        "/api/optimize",
        {"candidates": list(range(2, 66)), "layers": 32, "samples": 2_000},
    )
    record(
        "optimize_combined_work",
        "dos-combined-work",
        "optimize 64 candidates x 32 layers x 2,000 samples",
        r,
        "HARDENED" if r["status"] == 400 and r["elapsed_s"] < 2.0 else "VULN",
    )

    # 5h. The automatic exact branch must account for combination count.
    r = post_json(
        "/api/optimize",
        {"candidates": list(range(2, 20)), "layers": 9, "samples": 1},
    )
    record(
        "optimize_bruteforce_work",
        "dos-combined-work",
        "optimize automatic comb(18,9) exact branch",
        r,
        "HARDENED" if r["status"] == 400 and r["elapsed_s"] < 2.0 else "VULN",
    )

    # 5i. A compact body of distinct large rational denominators used to grow
    # a huge common denominator before discovering that the gaps do not sum to
    # one. The aggregate exact-bit proxy must reject before certificate work.
    gaps = [f"1/{(1 << (1_000 + index)) - 1}" for index in range(100)]
    r = post_json("/api/gaps", {"gaps": gaps, "exact": True})
    record(
        "gaps_distinct_rational_bit_work",
        "dos-combined-work",
        "100 exact gaps with distinct approximately 1,000-bit denominators",
        r,
        "HARDENED" if r["status"] == 400 and r["elapsed_s"] < 2.0 else "VULN",
    )

    # 5j. Valid supplied small-base factorizations used to bypass trial-work
    # admission while creating large denominators and pairwise kernel fractions.
    primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61)
    exponents = [int(4_000 / log2(prime)) for prime in primes]
    denominators = [prime**exponent for prime, exponent in zip(primes, exponents)]
    factorizations = {
        str(value): {str(prime): exponent}
        for prime, exponent, value in zip(primes, exponents, denominators)
    }
    r = post_json(
        "/api/certificate",
        {"denominators": denominators, "factorizations": factorizations},
    )
    record(
        "certificate_prefactored_bit_work",
        "dos-combined-work",
        "18 valid prefactored denominators near the HTTP bit-work boundary",
        r,
        "HARDENED" if r["status"] == 400 and r["elapsed_s"] < 2.0 else "VULN",
    )


# --------------------------------------------------------------------------
# 6. Static-file serving: traversal + method handling
# --------------------------------------------------------------------------
def test_static() -> None:
    for path in ("/../../../../etc/passwd", "//etc/passwd", "/../web.py",
                 "/%2e%2e/%2e%2e/etc/passwd", "/../src/coprimebatch/web.py"):
        r = raw_request("GET", path)
        leaked = ("root:" in r["body"]) or ("def serve" in r["body"])
        record(f"traversal {path}", "static-traversal",
               f"GET {path}", r, "VULN" if leaked else "HARDENED")

    for method in ("PUT", "DELETE"):
        r = raw_request(method, "/api/health")
        record(f"method_{method}", "static-method", f"{method} /api/health", r,
               "HARDENED" if r["status"] in (404, 405) else "INFO")


# --------------------------------------------------------------------------
# 7. Large-order transport (count + preview + digest)
# --------------------------------------------------------------------------
def test_transport() -> None:
    # full_order requested above cap -> rejected.
    r = post_json("/api/balance",
                  {"mode": "quota", "counts": {"A": 20000, "B": 20000}, "full_order": True})
    record("full_order_over_cap", "transport",
           "full_order=true with 40,000 items (cap 10,000)", r,
           "HARDENED" if r["status"] == 400 else "VULN")

    # digest-only path returns preview + sha256, no full order.
    r = post_json("/api/balance",
                  {"mode": "quota", "counts": {"A": 20000, "B": 20000}})
    try:
        body = json.loads(r["full_body"]) if r["status"] == 200 else {}
    except Exception:  # noqa: BLE001
        body = {}
    has_digest = bool(body.get("order", {}).get("sha256"))
    included = body.get("order", {}).get("included")
    record("large_order_digest", "transport",
           "40,000-item order returns preview+digest (included=false)", r,
           "HARDENED" if (has_digest and included is False) else "INFO")


# --------------------------------------------------------------------------
# 8. JSON parser strictness
# --------------------------------------------------------------------------
def test_json_parser() -> None:
    r = raw_request("POST", "/api/balance",
                    body=b'{"mode":"quota","mode":"binary","counts":{"A":1}}',
                    headers={"Content-Type": "application/json"})
    record("duplicate_json_keys", "json",
           "duplicate top-level key rejected", r,
           "HARDENED" if r["status"] == 400 else "VULN")

    r = raw_request("POST", "/api/balance", body=b"[1,2,3]",
                    headers={"Content-Type": "application/json"})
    record("non_object_body", "json", "array body rejected", r,
           "HARDENED" if r["status"] == 400 else "VULN")

    r = raw_request("POST", "/api/balance", body=b"\xff\xfe not utf8",
                    headers={"Content-Type": "application/json"})
    record("invalid_utf8_body", "json", "invalid UTF-8 body rejected", r,
           "HARDENED" if r["status"] == 400 else "VULN")


def main() -> None:
    print(f"=== adversarial probes against {BASE} ===")
    test_baseline()
    test_host_origin()
    test_body_cap()
    test_balance_caps()
    test_static()
    test_transport()
    test_json_parser()
    # DoS last: these may leave a CPU-bound worker thread behind; the harness
    # itself always returns thanks to the client timeout.
    test_dos_endpoints()

    for row in RESULTS:
        row["result"].pop("full_body", None)
    with OUT.open("w") as fh:
        json.dump(RESULTS, fh, indent=2)
    counts: dict[str, int] = {}
    for row in RESULTS:
        counts[row["verdict"]] = counts.get(row["verdict"], 0) + 1
    print("\n=== verdict tally ===")
    for verdict, n in sorted(counts.items()):
        print(f"  {verdict}: {n}")
    print(f"{OUT} written")


if __name__ == "__main__":
    main()

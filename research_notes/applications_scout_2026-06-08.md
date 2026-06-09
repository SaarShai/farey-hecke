# Applications scout — 2 viable industry paths from the Farey/BCZ work (2026-06-08)

Goal: 2 viable + highly-likely + ≥moderately-valuable industry paths (no pedagogy / no
Lean-Mathlib-community tooling). Workflow wf_f01d33d0-de3: 6 industry-angle generators → 45
ideas → adversarial viability scout → sieve. Full result: tasks/wbmhat40v.output.

## Meta-finding
Our one genuine industrial EDGE is the **D2 gap-structure diagnostic applied to entropy /
randomness quality**. Every other angle was dominated by incumbents (see kill-list) — so the 2
surviving paths are both in the **RNG / crypto-security** vertical, two distinct go-to-markets of
the same de-risked core.

## PATH 1 — HIGHLY LIKELY, strong. Embedded TRNG health-monitor (HSM/TPM silicon)
- **What:** online rolling-window D2 cluster-size test on ring-oscillator entropy sources;
  flags **partial harmonic/locking** degradation that NIST SP 800-90B (RCT/APT) and AIS-31 are
  structurally blind to (they preserve ~50% bit balance, pass the mandated tests).
- **Discovery:** D2 bounded-cluster diagnostic (`code/d2_diagnostic_suite.py`); periodic/harmonic
  signal collapses `f(size≥3)` at `q*`. ~1000× class separation, Lean-verified threshold.
- **Why highly likely:** the blind spot is real and the test is the *mandated* one; de-risk is a
  single **$100 FPGA, 2–3 day** go/no-go (inject partial locking that passes RCT+APT, measure D2
  separation). Killer risk = raw-timing access + does locking preserve the timing comb — *empirically
  testable*, not a category error.
- **Value:** HSM market $1.4B→$5B (15% CAGR); **FIPS 140-3 ESV mandatory since Jan 2025** = pull.
  Buyers: TRNG silicon vendors (Infineon, STMicro, Microchip), FIPS eval labs (atsec, SafeLogic).
- **Edge vs incumbent:** RCT/APT/AIS-31 = frequency/proportion tests, no gap-cluster test; Quantum
  Dice DISC requires replacing the source with a photonic QRNG. Ours is a drop-in on existing RO-TRNGs.
- **First step:** the FPGA experiment above; if separation >10×, CHES/TCHES note + approach eval labs.

## PATH 2 — HIGHLY LIKELY, same core / different market. Offline entropy-test-suite tool
- **What:** D2 cluster statistic packaged as an **offline test** added to 800-90B / AIS-31 batteries
  — a software tool/plugin for TRNG designers and FIPS evaluation labs (not embedded silicon).
- **Discovery + de-risk:** identical D2 core; the SAME FPGA/data experiment validates it. Different
  product (software), different buyers (eval labs, crypto-library / IP vendors), no silicon
  integration risk → independently viable.
- **Value:** security-testing market $14.7B; PQC rollout raising demand. Lower per-seat $ than
  embedded IP but far lower barrier to ship.
- **Edge:** structural (gap-distribution) classification of entropy quality vs presence-only batteries.

## Higher-upside / NOT-highly-likely (flagged, offered as a stretch, not one of the 2)
- **Timing side-channel structural classifier** (D2 on cache-timing spacings): real market + prior-art
  gap, **but the scout itself flagged a physics-level killer risk** — OS/RDTSC jitter ~10,000× the
  ~4 ns L1 signal; arithmetic address structure may not survive into timing. 1–2 day kill-test;
  do NOT count as highly-likely.

## Rejected (adversarial kills — useful)
- **5G Farey pilot grid:** wrong metric (star-discrepancy ≠ mutual coherence; cyclic difference sets hit the Welch bound, Farey doesn't).
- **CBRS spectrum sensor:** wrong market (ESC mandate = Navy-radar incumbents; LTE subframe periodicity → false positives).
- **LCG/PRNG pre-screener:** dominated by the spectral test (detects LCG lattice from algebra, fewer samples, upstream).
- **QMC / low-discrepancy sampling (finance/graphics):** dominated by Sobol/Halton/lattice rules — Farey/prime-denom does not beat them.

## Bottom line
1 strong highly-likely path (TRNG/entropy validation), realized as **2 distinct products** (embedded
monitor + offline test-suite tool), both de-risked by ONE cheap FPGA experiment. The side-channel
idea is the only other thing with a real market but is physics-gated. Everything else lost to incumbents.

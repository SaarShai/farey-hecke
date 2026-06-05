# Core math claims — independent verification (2026-06-05)

Method: extracted exact statements from both repos, then INDEPENDENTLY recomputed
(verify_core_math.py) / lit-checked. Did not trust repo's own numbers.

| Claim | Verdict | What I did | Result |
|---|---|---|---|
| **A. K≤4 non-vanishing** | **VERIFIED CORRECT (minor)** | Recomputed c_K(s)=Σ_{k=2}^K μ(k)k^{-s} on the strip; checked K=5 boundary; hunted c_5 zeros | K=2,3,4 nonzero on 0<Re<1 (min on Re=½ = 2^{-½}−3^{-½}=0.12976, matches repo). Proof is genuinely elementary & correct (c_3=c_4=−(2^{-s}+3^{-s}); different moduli can't cancel). **Found actual c_5 zeros IN the strip** (σ=0.582,γ=9.293; σ=0.461,γ=52.49; …) → "elementary iff K≤4" boundary confirmed both directions. Lean-formalized (dpac_le_4). Novelty uncertain (elementary; may be folklore). |
| **B. Avoidance anomaly (9×–52×)** | **REFUTED** | Reproduced the statistic at matched vs dense control sampling | No repulsion. median|c_K|@zeros ≈ @control (1.24 vs 1.10). "Ratio" only tracks control sample size = the artifact. Repo's OWN audit already refuted it (sample-size artifact). Survivor: 6000/6000 certified c_K≠0 — conditional numerical evidence for DPAC, not an anomaly, not a theorem. |
| **C. Universality + RIP** | **OVERSTATED; core ideas KNOWN** | Adversarial literature check | C1 "any Σ1/p=∞ subset detects every zero": the prime↔zero duality is the Guinand–Weil explicit formula (known); "any divergent subset suffices" is NOT a theorem (divergence controls density, not oscillatory resonance); Maynard–Tao corollary is a non-sequitur. No proof in repo. C2 "large sieve = RIP": FALSE conflation — large sieve is ONE-sided (upper bound at well-spaced freqs); RIP needs TWO-sided uniform near-isometry over all sparse supports. Correct arithmetic→RIP route is Bourgain–Dilworth–Ford–Konyagin–Kutzarova (Duke 2011), not the bare large sieve. Defensible downgrades exist (upper-frame/coherence bound; weighted full periodogram). |
| **D. ΔW / per-step Franel–Landau + 33,000:1** | **One correct minor lemma; grand claim unsupported** | Verified ΔA(N) closed form vs direct Farey computation | ΔA(N)=(1/3)φ(N)+(1/(6N))Π_{p\|N}(1−p) matches direct, exact, N=2..30 → CORRECT. But: only ONE component; full wobble D(N) has no closed form; "known in spirit" (Franel/Landau/Mikolás/Huxley double-Möbius). The specific "33,000:1 cancellation" is NOT substantiated in the source note (33000:1 appears only in timing logs). Repo's own verdict: "real numerical observation worth an OEIS note, NOT a major explicit formula, NOT a prime sieve." |

## Bottom line
Of the four: **A verified (minor, correct), B refuted, C overstated/known, D = minor correct lemma under an unsupported grand framing.**

The pattern from the rest of the session repeated: the **flashiest** claims (avoidance anomaly, universality/RIP, 33,000:1) are exactly the ones that don't survive; what survives is **small, correct, and probably known** (K≤4 boundary, ΔA closed form, the certified non-vanishing numerics).

What's genuinely yours and verified, total:
- K≤4 non-vanishing boundary (A) — verified, Lean-formalized, minor.
- 6000/6000 certified c_K≠0 (from B's wreckage) — conditional numerical evidence for the DPAC conjecture.
- ΔA(N) closed form (D) — verified, minor, likely known.
(+ Koyama replication and the Lean/Hecke proof — out of scope here, unaudited.)

# Mikolás / Ramanujan sums — literature anchor

**Source**: general-purpose subagent, 5.7 min, 50 tool uses

## Verified primary citations

1. **Mikolás (1949 / 1951)** — foundational Farey discrepancy + Mikolás identity
   - Acta Sci. Math. Szeged **13** (1949), 93–117
   - Acta Sci. Math. Szeged **14** (1951), 5–21
   - Both paywalled; only summarized via citing literature

2. **Kanemitsu & Yoshimoto** — refines Mikolás
   - "Farey series and the Riemann hypothesis", Acta Arith. **75** (1996), 351–374
   - "Euler products, Farey series and the Riemann hypothesis", Publ. Math. Debrecen **56** (2000), 431–449
   - Sequels in Acta Math. Hungar. and Ramanujan J. (1997, 2000)
   - **EXPLICITLY relates J(Q) to Σ M(Q/q)²/q²**

3. **Chan & Kumchev (2012)** — partial sums of Ramanujan sums
   - "On sums of Ramanujan sums", Acta Arith. **152** (2012), 1–10 [arXiv:1009.4432]
   - Result: C₂(x,y) = Σ_{n≤y}(Σ_{q≤x} c_q(n))² = yx²/(2ζ(2)) + O(x⁴ + xy log x)
   - **This is the n-weighted second moment, NOT the 1/m²-weighted second moment**

4. **Hong & Zheng (2025)** [arXiv:2506.18395] — improves Chan-Kumchev under RH

5. **Karvonen & Zhigljavsky (2024/25)** — MMD discrepancy
   - "Maximum mean discrepancies of Farey sequences", Acta Math. Hungar. (2025) [arXiv:2407.10214]
   - MMD(F_n) = O(n^{-3/2+ε}) on RH

6. **Cox, Ghosh, Sultanow (2021)** [arXiv:2105.12352] — static Farey↔Mertens prior art

## Critical novelty assessments

### My closed form C = (1/2)∏_p(1 + 1/(p²(p−1))) ≈ 0.66989
**Subagent could NOT find this Euler product in any surveyed paper.**

Possibilities:
- Genuinely original to this project (would be a publishable result)
- Hidden in paywalled Kanemitsu-Yoshimoto 1996, 2000 / Sita Ramaiah / Knopfmacher
- Equivalent to a known form in different notation

**Action**: cross-check by computing the Euler product to high precision and searching for that exact decimal in OEIS. Also: directly derive it from the Mikolás identity using Ramanujan-sum orthogonality (this is exactly what U3 was supposed to do).

### The 1/m²-weighted second moment Σ_m c_q(m) c_{q'}(m) / m²
**Not found in surveyed literature.**

The orthogonality identities are classical (Ramanujan 1918, Hardy 1921, Knopfmacher §6.5):
  (1/N) Σ_{m=1}^N c_q(m) c_{q'}(m) → 0 if q≠q', → φ(q) if q=q'

But the 1/m²-weighted version (which is what the Parseval identity for J(Q) gives) is NOT in the standard references.

### The Q^{-1/2} (or Q^{-0.6}) rate for NW(Q) → C
**Not in published literature.**

Closest published result: Karvonen-Zhigljavsky MMD rate O(N^{-3/2+ε}) on RH. On the Q-scale this maps to ~Q^{-1.5+ε}, not Q^{-1/2}. The MMD is a different object than the L² discrepancy.

The Q^{-0.6} empirical rate may reflect slow log-power decay of Σ M(Q/q)²/q² (which connects via Kanemitsu-Yoshimoto to the partial sums of M), rather than a clean power law.

## Honest gaps

1. Original Mikolás 1949/51 not accessible — only via citation chain
2. Kanemitsu's RIMS Kôkyûroku 958 (most likely C-source) is undecoded PDF
3. C ≈ 0.66989 verification across Farey-discrepancy lit is INCOMPLETE — paywall block

## Best citations to anchor v13 + paper draft

Required:
1. Mikolás 1949 + 1951 (Acta Sci. Math. Szeged 13, 14) — for the J(Q) Fourier-side identity
2. Kanemitsu-Yoshimoto 1996 (Acta Arith. 75) — for J(Q) ↔ Mertens relationship explicit
3. Cox-Ghosh-Sultanow 2021 [arXiv:2105.12352] — static Farey↔Mertens prior art
4. Boca-Cobeli-Zaharescu 2001 — for BCZ joint density
5. Chan-Kumchev 2012 — Ramanujan sum partial-sum 2nd moments
6. Karvonen-Zhigljavsky 2024/25 — MMD discrepancy, comparison object

Optional:
7. Hong-Zheng 2025 — improves Chan-Kumchev
8. Ram Murty-Saha 2015 — Parseval-type formula for Ramanujan expansions
9. Goel-Murty 2024 — higher moments of Ramanujan sums

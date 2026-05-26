---
model: mimo-v2.5-pro
max_tokens: 12000
---

# L8 — Lit check: Is the asymptote of NW(Q) actually known?

## Setup

For Farey F_Q with E_Q(x) = #{α ≤ x} − Φ(Q)·x, define J(Q) = ∫₀¹ E_Q² dx, NW(Q) = Q·J(Q)/Φ(Q).

Empirically (exact streaming, verified against rational arithmetic at small Q):
- NW(Q=50k) = 0.6642
- NW(Q=200k) = 0.6691
- NW(Q=400k) = 0.6711
- NW(Q=300k area) ≈ 0.698 (SPIKES — anomalous)

Candidate closed form: C = (1/2)·Π_p (1 + 1/(p²(p−1))) = 0.66989.

## Questions

1. Is the asymptote lim_{Q→∞} NW(Q) known to be a specific constant in the literature?

2. Specifically, examine:
   - **Mikolás 1949** (Acta Math. Acad. Sci. Hungar.) — proved a formula for J(Q)
   - **Codecá-Perelli 1988** (Acta Arith. or similar) — proved asymptotic with explicit constant
   - **Hall 1970s** — on Farey discrepancy moments
   - **Boca-Cobeli-Zaharescu 2000s** — BCZ joint density work, related but different statistic
   - **Franel 1924** — equivalence with RH
   - **Kanemitsu et al.** — possible analytic computations

3. Is the constant (1/2)·Π_p(1 + 1/(p²(p−1))) = 0.66989 documented anywhere?

4. The slightly larger value 0.671 from empirical normal-trend — does that match any known constant?

5. If the asymptote is conjectural (not proved), what's the best-known unconditional bound?

Be precise about which paper/year/page if you cite. If you can't verify, say "I'd need to check" — that's more useful than confabulating.

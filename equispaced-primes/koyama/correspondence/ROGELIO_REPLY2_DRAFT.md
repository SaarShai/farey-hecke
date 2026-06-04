# Reply to Rogelio — Draft
Date: 2026-04-15
Re: structure of term A

---

Dear Rogelio,

You're right on both counts.

**On A being redundant:**

Yes — since n ≈ |F_{p-1}| and n' ≈ |F_p|, the exact formula is

    A = (n'²/n² − 1) · W(p−1)

which is W(p-1) scaled by a known factor (n'²−n²)/n². For large p, n'/n ≈ p/(p-1), so n'²/n² − 1 ≈ 2/p, giving A ≈ 2W(p-1)/p. So A is indeed determined by W(p-1) alone — no new object. One could write the decomposition directly without naming A.

The reason I introduced A as a named term: the central result of the theorem is |N/A − 1| = O(1/p²), i.e., N ≈ A. Naming A gives the comparison point. But you're right that this is the same as saying N ≈ 2W(p-1)/p, which one could state directly.

**On W(p-1) persisting:**

Yes, it does, and you've identified the real structure. The decomposition n'²·ΔW = A − B − C − N is effectively

    n'²·ΔW = W(p-1)·(n'²−n²)/n² − B − C − N

Since N ≈ A, the two W(p-1)-dependent terms nearly cancel, and

    n'²·ΔW ≈ −(B + C)

This is the actual payoff: the per-step change in discrepancy is approximately −(B+C)/n'², independent of W(p-1). The decomposition reduces the sign question to whether B + C > 0, which is a sum over existing fractions' shifts — no longer involving the global state W.

So: you're correct that A could be eliminated by substituting its definition; the useful content is the near-cancellation N ≈ A and the residual −(B+C). I'll clarify this in the paper.

Best,
Saar

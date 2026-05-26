---
model: mimo-v2.5-pro
max_tokens: 12000
---

# Z7 — Draft the Mertens-NW paper (~30-page main paper, or short note)

## Material to draft from

**Main empirical finding**: Pearson(NW(Q), |M(Q)|) = 0.892 across 18 Q values in [50k, 10⁶].

**Mechanism**: m=1 Mikolás Fourier-side term M(Q)²/(2π²) contributes (after Q · /Φ(Q) normalization) approximately M(Q)²/(6Q) to NW(Q).

**Predicted value at Q = 926265** (M(Q) = -368): NW ≈ 0.694. v2 stream_J test running.

**Predicted value at Q = 300k** (M(Q) = +220): NW ≈ 0.6699 + 0.027 = 0.697 vs observed 0.6987. (7% match)

**Predicted value at Q = 10⁶** (M(Q) = +212): NW ≈ 0.677 vs observed 0.6793. (25% match)

**Connection to RH**: M(x) = O(x^{1/2+ε}) under RH. Mertens conjecture |M(x)| < √x was disproved by Odlyzko-te Riele 1985 (so |M(x)| can exceed √x infinitely often). Implication: NW(Q) − C can exceed M(Q)²/(6Q) ≈ 1/6 for very anomalous Q.

## Draft outline

**Title** (proposed): "Mertens Function Fluctuations and the L²-Discrepancy of the Farey Sequence"

**Sections**:
1. **Introduction** (1-2 pages):
   - Farey sequence L²-discrepancy is a well-studied object (Franel-Landau, RH)
   - Recent empirical observation: NW(Q) = Q · J(Q) / Φ(Q) has sporadic large deviations from its conjectured asymptote C
   - We show these deviations correlate with |M(Q)| via the explicit Mikolás formula

2. **Background** (3-4 pages):
   - Farey discrepancy and Franel-Landau theorem
   - Mikolás's Fourier-side formula: J(Q) = (1/2π²) Σ_m |S_Q(m)|²/m² where S_Q(m) involves M(Q/d)
   - The constant C = (1/2)·Π_p(1 + 1/(p²(p−1))) ≈ 0.66989 (verified internally consistent)

3. **Main result** (5-6 pages):
   - Theorem (heuristic): NW(Q) − C ≈ (1/(6Q)) · (M(Q)² + cross-terms)
   - Justification via dominant m=1 Mikolás term
   - Predicted scaling: |NW(Q) − C| ~ |M(Q)|²/Q

4. **Numerical evidence** (4-5 pages):
   - Pearson correlation 0.892 over 18 Q values
   - Table of (Q, NW(Q), M(Q), prediction, residual)
   - Spike Q values 300k, 350k, 600k, 700k, 900k, 10⁶ all have |M(Q)| ≈ 200+
   - Normal Q values all have |M(Q)| < 81

5. **Adversarial verification** (2-3 pages):
   - Initial "5^5 factorization rule" was overfit and refuted
   - The genuine correlate is |M(Q)|, not factorization structure
   - Direct stream_J_v2 verification at Mertens-predicted Q (Q=926265)

6. **Open questions** (1-2 pages):
   - Rigorous proof of the Mertens-NW formula
   - Connection to Mertens conjecture failure (Odlyzko-te Riele)
   - Implication for the Franel-Landau equivalence under RH

7. **Conclusion** (1 page)

## What I want

Draft a clean abstract (200 words) + the introduction (2 pages of polished prose) for this paper, assuming submission target = J. Number Theory.

Then list 5-10 SPECIFIC technical claims that would need verification before submission.

Honest framing only. The 7-25% prediction errors are real and must be acknowledged in the abstract.

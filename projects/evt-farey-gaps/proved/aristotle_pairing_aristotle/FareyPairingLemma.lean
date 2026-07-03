/-
Combinatorial core of the θ = 1/2 extremal-index law for Farey gap MAXIMA
(large gaps = small denominator products).

Context: q0 q1 q2 q3 are four consecutive denominators of the Farey sequence
F_Q. Classical facts supplied as hypotheses:
  * adjacent denominators sum to more than Q            (h01, h12, h23)
  * the neighbor recursion q_{i+2} = k·q_{i+1} − q_i (k ≥ 1) gives
    q_{i+2} ≥ q_{i+1} − q_i, in ℕ-safe form q1 ≤ q2 + q0  (hrecF)
    and, by the x ↦ 1−x reversal symmetry of F_Q,        q2 ≤ q1 + q3 (hrecB).

Claim: three CONSECUTIVE gap-exceedances q_i·q_{i+1} < Q²/8 are impossible.
Hence exceedance clusters have size ≤ 2, which (with Hall's gap law) yields
extremal index θ = 1/2 for the large-gap extremes of the Farey sequence.

Proof sketch: from h12, max(q1,q2) > Q/2; if 2q1 > Q then hP0, hP1 force
4q0 < Q and 4q2 < Q, so hrecF gives q1 ≤ q0 + q2 < Q/2, contradiction;
the case 2q2 > Q is the mirror image via hP1, hP2, hrecB.
-/

import Mathlib

theorem farey_no_triple_large_gap
    (Q q0 q1 q2 q3 : ℕ)
    (h01 : Q < q0 + q1) (h12 : Q < q1 + q2) (h23 : Q < q2 + q3)
    (hrecF : q1 ≤ q2 + q0) (hrecB : q2 ≤ q1 + q3)
    (hP0 : 8 * (q0 * q1) < Q * Q)
    (hP1 : 8 * (q1 * q2) < Q * Q)
    (hP2 : 8 * (q2 * q3) < Q * Q) : False := by
  nlinarith only [ h01, h12, h23, hP0, hP1, hP2, hrecF, hrecB ]
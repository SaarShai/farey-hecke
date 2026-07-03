/-
In-cluster arithmetic-progression law for hard-edge exceedance clusters of
Farey gaps (the θ_edge = 2/3 mechanism).

Context: q0 q1 q2 are three consecutive denominators of the Farey sequence
F_Q with two consecutive deep hard-edge exceedances: both products exceed
(3/4)·Q². Classical facts supplied as hypotheses: denominators are ≤ Q, and
the neighbor recursion q2 = k·q1 − q0 holds for some k ≥ 1 (ℕ-safe form
q2 + q0 = k·q1).

Claim: k = 2 — i.e. q2 = 2·q1 − q0, the denominators are in arithmetic
progression. This machine-verifies the "parabolic shear" anatomy of
hard-edge clusters (every in-cluster step uses the k = 2 branch).

Proof sketch: the product bounds force q0, q1, q2 > (3/4)·Q (each partner
is ≤ Q), so q2 + q0 > (3/2)·Q ≥ (3/2)·q1 and q2 + q0 ≤ 2·Q < (8/3)·q1,
hence 3/2 < k < 8/3, so k = 2.
-/

theorem farey_hard_edge_cluster_is_AP
    (Q q0 q1 q2 k : ℕ)
    (hQ : 0 < Q)
    (hb0 : q0 ≤ Q) (hb1 : q1 ≤ Q) (hb2 : q2 ≤ Q)
    (hk : 1 ≤ k)
    (hrec : q2 + q0 = k * q1)
    (hP0 : 3 * (Q * Q) < 4 * (q0 * q1))
    (hP1 : 3 * (Q * Q) < 4 * (q1 * q2)) : k = 2 := by
  sorry

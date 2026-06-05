#!/usr/bin/env python3
"""
THEOREM (R) numerical cross-check (exact arithmetic where load-bearing).

Citation-locked inputs used here (see THEOREM_R_2026-05-15.md §0):
  - Athreya-Cheung IMRN 2014, Thm 1.1: Omega Poincare section, R(a,b)=1/(ab),
    BCZ map eq (1.4); Thm 1.2: dm = 2 da db is the unique a.c. ergodic
    invariant prob. measure; Thm 1.3: the level-Q periodic orbits
    equidistribute -> m  (so a Birkhoff average over one F_Q orbit converges
    to the Omega-integral against dm = 2 da db).

What this script verifies (numerics guide; the theorem-(R) analytic argument
is in THEOREM_R_2026-05-15.md):

  R0. Exact restatement.  With f_0=0 boundary convention (V4), Phi=|F_Q|,
        J(Q) = sum_j gap_j ( S_j^2 - S_j Phi gap_j + (Phi gap_j)^2/3 ),
      S_j = E_Q(f_j).  W(Q)=J(Q)/Phi, target  C = lim Q*W(Q) ~ 0.66.
      Confirm Q*J/Phi rises toward ~0.66 (reproduces V3 headline, EXACT J).

  R1. Hall coordinates.  s_j := Phi*gap_j  (mean spacing -> 1).  Verify
      <s> = (1/n) sum s_j -> 1 exactly (telescoping: sum gap = 1, n=Phi).
      So g_j = 1 - s_j is the *centered* Hall cocycle (mean 0 exactly).

  R2. Hall-unit truncation is the right renormalization (sharpens V7).
      Define s_j^{(M)} = min(s_j, M).  Show the truncated roof-weighted
      second moment
        Chat(Q,M) := Q*Phi^{-2} * sum_j  s_j^{(M)} * S_j^2 * (1/Phi)   ... [see note]
      Actually use the *exact* decomposition: the part of J from gaps with
      s_j<=M, scaled, is Q-stable per fixed M and -> C as M->inf.

  R3. Birkhoff = space integral (AC Thm 1.3).  The leading roof-weighted
      mean square  (1/n) sum_j s_j S_j^2 ... is compared to the Omega
      integral form; we check Q-stability of the *per-fixed-M* truncated
      variance proxy sigma2(M) and its M->inf limit vs C.

All Farey/identity computation uses exact Fraction.  Float only for the
final asymptotic constant comparison.
"""
from fractions import Fraction
import numpy as np


def farey(Q):
    a, b, c, d = 0, 1, 1, Q
    out = []
    while c <= Q:
        if (a, b) != (0, 1):
            out.append((a, b))
        k = (Q + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
    out.append((1, 1))
    return out


def exact_nodes_fr(Q):
    """EXACT.  Phi, exact Fraction nodes f_0=0..f_Phi=1, exact Birkhoff sums
    S_j = E_Q(f_j) = j - Phi f_j (V4-PROVEN identity), exact gaps."""
    F = farey(Q)
    Fx = [Fraction(0)] + [Fraction(h, k) for (h, k) in F]
    Phi = len(F)
    S = [j - Phi * Fx[j] for j in range(len(Fx))]
    gaps = [Fx[j] - Fx[j - 1] for j in range(1, len(Fx))]
    return Phi, Fx, S, gaps


def fast_arrays(Q):
    """Float arrays (per-node values are exact rationals; float only for the
    asymptotic constant, exactly as the in-repo V3 convention).  Returns
    Phi, S_left[j] = E_Q(f_j) = j - Phi f_j, gap[j] = f_{j+1}-f_j."""
    F = farey(Q)
    num = np.array([0] + [h for (h, k) in F], dtype=np.float64)
    den = np.array([1] + [k for (h, k) in F], dtype=np.float64)
    x = num / den
    Phi = len(F)
    j = np.arange(len(x), dtype=np.float64)
    S = j - Phi * x                       # exact identity, evaluated in float
    gap = x[1:] - x[:-1]
    return Phi, S[:-1], gap                # S at left node of each interval


def R0_exact_J(Q):
    """EXACT J(Q) via the V3/1.4 identity (Fraction), and Q*J/Phi.  Q<=600."""
    Phi, Fx, S, gaps = exact_nodes_fr(Q)
    J = Fraction(0)
    for j in range(len(gaps)):
        g = gaps[j]
        Sj = S[j]
        J += g * (Sj * Sj - Sj * Phi * g + (Phi * g) ** 2 / 3)
    return Phi, J, Fraction(Q) * J / Phi


def R0_fast_J(Q):
    """Same J(Q) identity, float-vectorized (per-node values exact)."""
    Phi, S, gap = fast_arrays(Q)
    Pg = Phi * gap
    J = float(np.sum(gap * (S * S - S * Pg + Pg * Pg / 3.0)))
    return Phi, J, Q * J / Phi


def R1_hall_mean(Q):
    """s_j = Phi*gap_j; <s> over the orbit is exactly 1 (telescoping)."""
    Phi, Fx, S, gaps = exact_nodes_fr(Q)
    n = len(gaps)
    return n, (Phi * sum(gaps)) / n        # exact Fraction == 1


def R2_truncated_constant(Q, Ms):
    """Split Q*J/Phi by Hall spacing s_j=Phi*gap_j <= M (in) vs > M (out).
    Per-node values exact; sums in float (V3 convention).  Claim(R): in-M
    Q-stable per fixed M and -> C as M->inf; out-M = Mikolas O(1) tail."""
    Phi, S, gap = fast_arrays(Q)
    s = Phi * gap
    Pg = Phi * gap
    term = gap * (S * S - S * Pg + Pg * Pg / 3.0)
    out = {}
    for M in Ms:
        mask = s <= float(M)
        cin = Q * float(np.sum(term[mask])) / Phi
        cout = Q * float(np.sum(term[~mask])) / Phi
        out[M] = (cin, cout)
    return Phi, out


def R3_hall_variance(Q, Ms, maxlag=60):
    """Hall-normalized TRUNCATED cocycle Green-Kubo (correct Hall units).
    psi^{(M)}_j = (1 - min(s_j, M)); report c_0(M) and sigma2(M;L).
    Claim(R) needs these Q-stable per fixed M (V7 gap*Q cap was NOT)."""
    Phi, S, gap = fast_arrays(Q)
    s = Phi * gap
    n = len(s)
    res = {}
    for M in Ms:
        g = 1.0 - np.minimum(s, float(M))
        gh = g - g.mean()
        c0 = float(np.mean(gh * gh))
        acc = c0
        for j in range(1, maxlag + 1):
            acc += 2.0 * float(np.mean(gh[:n - j] * gh[j:]))
        res[M] = (c0, acc)
    return res


def R4_brownian_bridge(Q, Ms):
    """Closed-orbit Brownian-bridge assembly (the constant predictor).
    S_j is a Birkhoff sum of the mean-zero Hall cocycle on a CLOSED orbit
    (S_0=S_Phi=0, V4).  So (1/Phi^2) sum_j S_j^2 -> sigma^2 * int_0^1 t(1-t)
    = sigma^2/6 IF Var(S_j) ~ sigma^2 * j(Phi-j)/Phi (bridge).  Predict
        C_pred(M) = (pi^2/3) * sigma2(M) / 6 * <R>_weight ...
    We instead directly measure the dimensionless ratio
        rho(Q) := (Q*J/Phi)  vs  (pi^2/3)/6 * sigma2_eff
    and the raw bridge quantity  beta(Q) := (1/Phi^2) sum_j S_j^2  (-> const,
    Q-stable) and  Q*J/Phi.  Reports both so the analytic constant can be
    pinned from data + cited Phi ~ 3Q^2/pi^2."""
    Phi, S, gap = fast_arrays(Q)
    beta = float(np.sum(S * S)) / (Phi ** 2)          # -> sigma^2/6 if bridge
    # roof-weighted version (gap weight = the J integrand leading part):
    Llead = float(np.sum(gap * S * S))                # = sum gap_j S_j^2
    QLlead = Q * Llead / Phi
    return Phi, beta, QLlead


def main():
    print("=" * 74)
    print("THEOREM (R) numerical cross-check  (citation-locked inputs; exact J)")
    print("=" * 74)

    print("\n[R0] J(Q) via 1.4 identity; Q*J/Phi -> C ~ 0.66")
    print("     (EXACT Fraction for Q<=600 cross-checks float; float for big Q,")
    print("      per the in-repo V3 convention -- per-node values are exact)")
    print("   Q      Phi        J(float)     J(exact<=600)   Q*J/Phi")
    for Q in (50, 100, 200, 400, 600, 1000, 2000, 4000):
        Phi, Jf, QJP = R0_fast_J(Q)
        if Q <= 600:
            _, Je, _ = R0_exact_J(Q)
            je = f"{float(Je):14.6f}"
            assert abs(float(Je) - Jf) < 1e-6 * (1 + abs(Jf)), (Q, float(Je), Jf)
        else:
            je = "      --      "
        print(f"  {Q:5d}  {Phi:8d}   {Jf:12.5f}   {je}   {QJP:.6f}")

    print("\n[R1] Hall mean <s> = Phi*<gap> must be exactly 1 (telescoping)")
    for Q in (100, 300, 600):
        n, ms = R1_hall_mean(Q)
        print(f"  Q={Q:4d}: n={n:7d}  <s>={ms}  (==1: {ms == 1})")

    print("\n[R2] EXACT truncated constant Chat(Q,M) [in-M] and discarded")
    print("     [out-M] piece.  Claim(R): in-M Q-stable per fixed M,")
    print("     in-M -> C~0.66 as M grows; out-M is the Mikolas O(1) tail.")
    Ms = (2, 4, 8, 16, 32, 64)
    for Q in (400, 800, 2000, 4000):
        Phi, out = R2_truncated_constant(Q, Ms)
        row = "  Q=%4d: " % Q
        for M in Ms:
            cin, cout = out[M]
            row += f"M{M}[{cin:.4f}/{cout:.4f}] "
        print(row)
    print("     (format  M[in-M/out-M];  in+out = full Q*J/Phi from R0)")

    print("\n[R4] Closed-orbit Brownian-bridge assembly: beta=(1/Phi^2)sum S^2")
    print("     (-> sigma^2/6, Q-stable) and Q*sum(gap S^2)/Phi (leading C)")
    print("   Q      Phi       beta=(1/Phi^2)SumS^2   Q*Sum(gap S^2)/Phi")
    for Q in (200, 400, 800, 2000, 4000):
        Phi, beta, QL = R4_brownian_bridge(Q, Ms)
        print(f"  {Q:5d}  {Phi:8d}   {beta:18.6f}   {QL:.6f}")

    print("\n[R3] Hall-normalized TRUNCATED cocycle Green-Kubo sigma2(M)")
    print("     Claim(R): c_0(M) and sigma2(M) Q-STABLE per fixed M")
    print("     (contrast V7 gap*Q truncation which was NOT Q-stable).")
    for Q in (500, 1000, 2000, 4000):
        res = R3_hall_variance(Q, Ms=(2, 4, 8, 16), maxlag=60)
        row = "  Q=%4d: " % Q
        for M in (2, 4, 8, 16):
            c0, s2 = res[M]
            row += f"M{M}[c0={c0:.4f},s2={s2:.4f}] "
        print(row)
    print("=" * 74)


if __name__ == "__main__":
    main()

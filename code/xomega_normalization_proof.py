"""
xomega_normalization_proof.py  —  FALSIFICATION RECORD (formerly a false "proof")
=================================================================================
STATUS 2026-06-14: this script previously CLAIMED to "prove" a lambda^3
diagonal-conjugacy "normalization bridge" between the Hecke/Taha gap-product edge
(1/lambda^3) and the Athreya-Chaika-Lelievre (ACL) golden-L slope-gap edge (1).
Two independent verifiers flagged it (bug #14) as INTERNALLY INCONSISTENT, and the
3-track scout (research_notes/Xomega_generalize_2026-06-14.md,
research_notes/novelty_U2_cusp_edge_2026-06-14.md) FALSIFIED the underlying
Veech-bridge normalization. This file is now an honest NEGATIVE record. It does
NOT prove the bridge; it documents WHY the bridge is false and computes the
self-contradiction explicitly.

WHAT THE OLD SCRIPT ASSERTED (both at once, and that is the bug):
  (i)  A diagonal conjugation D = diag(t, 1/t) with t^2 = 1/lambda sends the Hecke
       parabolic [[1,lambda],[0,1]] to the ACL parabolic [[1,1],[0,1]], rescaling
       slopes by t^2 = 1/lambda and slope-GAPS by t^4 = 1/lambda^2.
  (ii) The two "support edges" of the SAME surface (golden L = Hecke H_5 =
       Delta(2,5,inf)) differ by exactly lambda^3 (Hecke 1/lambda^3 vs ACL 1).

INCONSISTENCY #1 (a single diagonal conjugation cannot do both).
  Under D, the script's OWN stated rescaling of the relevant quantity is 1/lambda^2.
  But the asserted edge ratio is 1/lambda^3. These differ by a bare factor of
  lambda (1/lambda^3 = (1/lambda^2) * (1/lambda)) that NO diagonal conjugation in
  this normalization produces. So the "QED artifact" line was unsupported: the
  lambda^3 ratio is NOT the conjugation-scaling the script computed.

INCONSISTENCY #2 (the two numbers are not even the same observable).
  The Hecke/Taha edge 1/lambda^3 is the value of the gap-PRODUCT  P = a*b  at the
  cusp tip. The ACL golden-L edge 1 is the smallest value of the slope-gap /
  return-time  R  of the horocycle section. Per the 3-track scout, on the cusp
  branch these observables are RECIPROCAL,  R = 1/P,  NOT related by any diagonal
  conjugation. If a genuine "same surface, matched units" identity held it would
  read R_edge = 1/P_edge; but 1/(1/lambda^3) = lambda^3 != 1. So the two edges are
  two DIFFERENT observables under two DIFFERENT normalizations whose numerical
  values happen to sit a power of lambda apart -- a coincidence of conventions,
  NOT a conjugation/diagonal-bridge identity.

CONCLUSION (corrected). The X_Omega = 1/lambda^3 value is NOT the Veech slope-gap
support edge transported by a diagonal conjugation. The Veech-bridge normalization
is FALSIFIED. What survives the audit is ONLY:
  - the qualitative MECHANISM "support edge is attained at the cusp / parabolic-
    fixed point of the section" (Athreya-Chaika no-small-gaps; ports as a mechanism), and
  - the fact that the scalar X_Omega is normalization-dependent (it is the
    gap-PRODUCT value 1/lambda^3 in the project's Taha normalization, and the
    RECIPROCAL return-time edge 1 in the ACL normalization) and therefore is NOT a
    new lattice invariant.
The "1/lambda^3 = lambda^3 * (ACL edge)" line is retained ONLY to display the
contradiction, flagged as FALSIFIED -- it is not a derivation.
"""
import math, json, os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

phi = (1 + math.sqrt(5)) / 2   # lambda_5
lam = phi

print("=" * 72)
print("FALSIFICATION RECORD: the lambda^3 'Veech-bridge normalization' is FALSE")
print("=" * 72)
print(f"  lambda_5 = phi = {lam:.8f}")
print(f"  Hecke/Taha edge  = gap-PRODUCT value  P = a*b at cusp tip = 1/lambda^3 = {1/lam**3:.8f}")
print(f"  ACL golden-L edge = smallest slope-gap / return time  R           = 1.0")
print(f"  These are DIFFERENT observables (product vs return-time), in DIFFERENT")
print(f"  normalizations. Per the 3-track scout, on the cusp branch they are")
print(f"  RECIPROCAL: R = 1/P -- NOT related by any diagonal conjugation.")

print("\n" + "-" * 72)
print("INCONSISTENCY #1 : a single diagonal conjugation cannot give both factors")
print("-" * 72)
t2 = 1.0 / lam          # t^2, the script's own conjugation parameter
gap_scaling = t2 ** 2   # t^4 = 1/lambda^2, the OLD script's stated slope-gap scaling
edge_ratio  = 1 / lam**3
print(f"  OLD claim (i):  D=diag(sqrt(1/lambda),sqrt(lambda)) sends Hecke parabolic")
print(f"                  [[1,lambda],[0,1]] -> [[1,1],[0,1]];  t^2 = 1/lambda = {t2:.6f}.")
print(f"                  Stated slope-GAP scaling under D = t^4 = 1/lambda^2 = {gap_scaling:.6f}.")
print(f"  OLD claim (ii): the two edges differ by lambda^3  (1/lambda^3 = {edge_ratio:.6f} vs 1).")
print(f"  CONTRADICTION:  1/lambda^2 ({gap_scaling:.6f}) != 1/lambda^3 ({edge_ratio:.6f}).")
print(f"                  Extra unexplained factor = lambda^3 / lambda^2 = lambda = {lam:.6f}.")
print(f"                  A single diagonal conjugation produces 1/lambda^2, NOT 1/lambda^3.")
print(f"                  => the 'QED artifact' was UNSUPPORTED; the bridge is not a conjugation.")

print("\n" + "-" * 72)
print("INCONSISTENCY #2 : the reciprocal test (the correct relation) fails matching")
print("-" * 72)
P_edge = 1 / lam**3
R_edge_ACL = 1.0
recip_of_P = 1 / P_edge
print(f"  Correct cusp-branch relation (3-track scout): R = 1/P.")
print(f"  Hecke gap-product edge  P_edge        = 1/lambda^3 = {P_edge:.8f}")
print(f"  Its reciprocal          1/P_edge      = lambda^3   = {recip_of_P:.8f}")
print(f"  ACL return-time edge    R_edge        = {R_edge_ACL:.8f}")
print(f"  A genuine same-surface/matched-units identity would need 1/P_edge = R_edge,")
print(f"  i.e. {recip_of_P:.6f} = {R_edge_ACL:.6f}  -- which is FALSE (off by lambda^3).")
print(f"  => the two edges are NOT one observable in two coordinate systems; they are")
print(f"     two different observables under two different normalizations.")

print("\n" + "=" * 72)
print("WHAT SURVIVES THE AUDIT (the honest residual)")
print("=" * 72)
print("  [SURVIVES] Mechanism: the support edge is attained at the cusp / parabolic-")
print("             fixed point of the horocycle section. Qualitative (Athreya-Chaika,")
print("             Smillie-Weiss no-small-gaps); ports across the triangle-group family.")
print("  [SURVIVES] X_Omega is normalization-dependent: gap-PRODUCT value 1/lambda^3 in")
print("             the Taha normalization vs RECIPROCAL return-time edge 1 in ACL coords.")
print("             Hence X_Omega is NOT a new lattice invariant and NOT a commensurability")
print("             detector (it lies in the classical trace field Q(cos pi/q)).")
print("  [FALSIFIED] The lambda^3 diagonal-conjugacy 'normalization bridge' that identifies")
print("              1/lambda^3 with the Veech slope-gap edge. P and R are reciprocal on the")
print("              cusp branch (R = 1/P), not diagonally conjugate. DO NOT re-assert it.")

res = {
    "status": "FALSIFICATION_RECORD",
    "bug_id": 14,
    "lambda_5": lam,
    "hecke_gap_product_edge_P_1_over_lam3": 1 / lam**3,
    "acl_return_time_edge_R": 1.0,
    "correct_cusp_branch_relation": "R = 1/P (reciprocal), NOT diagonal conjugation",
    "inconsistency_1": {
        "stated_diagonal_gap_scaling": gap_scaling,      # 1/lambda^2
        "asserted_edge_ratio": edge_ratio,               # 1/lambda^3
        "unexplained_extra_factor": lam,                 # the missing lambda
        "verdict": "1/lambda^2 != 1/lambda^3; single diagonal conjugation cannot give both",
    },
    "inconsistency_2_reciprocal_test": {
        "1_over_P_edge": recip_of_P,                     # lambda^3
        "acl_R_edge": R_edge_ACL,                        # 1
        "match": False,
        "verdict": "R != 1/P in matched units -> different observables, different normalizations",
    },
    "survives": [
        "mechanism: edge attained at cusp/parabolic-fixed point (qualitative, ports)",
        "X_Omega is normalization-dependent -> NOT a new invariant, NOT a commensurability detector",
    ],
    "falsified": "lambda^3 diagonal-conjugacy Veech-bridge normalization (P,R reciprocal not conjugate)",
}
with open(os.path.join(OUT, "xomega_normalization_proof.json"), "w") as f:
    json.dump(res, f, indent=2)
print(f"\nSaved (as falsification record) {os.path.join(OUT, 'xomega_normalization_proof.json')}")

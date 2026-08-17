"""f7links_ks_gate.py -- q=7 K_s divisor gate + det(1-K_7) non-vanishing lemma
on the flagship box. Both serve assembly LINK 5 (the numbering in force in
THEOREM_G7_OFFLINE_ASSEMBLY.md: link 4 = argument principle, link 4b = Hilbert
-> Banach transport, link 5 = K_s gate + Z_S identification).

Ball arithmetic only (python-flint Arb/Acb, 384 bits). Read-only: recomputes the
F7_CONSTANTS_MANIFEST.md quantities from scratch and writes ONE receipt,
f7_receipts/F7LINKS_KS_GATE_RECEIPT.json. No existing file is modified.

Interpreter: /Users/za/.venvs/farey-rh/bin/python

What is certified here
  (1) lambda_7 = 2 cos(pi/7) satisfies m(x) = x^3 - x^2 - 2x + 1 (ball zero).
  (2) the Lemma 6.3 word A_s = L_1^2 L_2 L_1 L_2 has Moebius matrix
      M_2 M_1 M_2 M_1 M_1 with det = 1 and trace tau_7 = 4 lam^2 + 3 lam.
  (3) ell_7 = (tau - sqrt(tau^2-4))/2, a_7 = -log ell_7, spacing pi/a_7.
  (4) the exact zero lattice s = -n + i pi k / a_7 (n >= 0, k in Z) has
      BOX-to-lattice distance >= the printed lower bound (rounded DOWN),
      compared against the manifest's claimed 0.5895480.
  (5) |det(1 - K_s)| >= a positive certified lower bound for EVERY s in the
      closed box, via |det| >= prod_{n>=0} (1 - ell^{2 sigma_lo + 2n}).
"""

import json
import math
import os

from flint import acb, arb, ctx

PREC = 384
ctx.prec = PREC

# --- flagship box (F7_R3B_ASSEMBLY_CERT.md section 1) ------------------------
PIN_RE = "0.4751647621098225"
PIN_IM = "4.668743786424289"
HALF_WIDTH = "1e-6"

CLAIMED_BOX_MARGIN = "0.5895480"      # manifest section 4.3 / section 7
CLAIMED_POINT_MARGIN = "0.589549387672466"
CLAIMED_TAU = "18.393731622284383001616653"
CLAIMED_ELL = "0.054527994798052490833925196"
CLAIMED_A7 = "2.909041043174856595598222180"
CLAIMED_SPACING = "1.079940986381249360096096828"
# LAW_Q3_BRANCH_DIAGNOSIS.md / law_probes/q3diag_detK.json, q=7 orbit product
LAW_B7 = "0.0029733022166964396"


def _dec(units, digits):
    """Render the integer `units` as a decimal with `digits` fractional places."""
    sign = "-" if units < 0 else ""
    s = str(abs(units)).rjust(digits + 1, "0")
    return f"{sign}{s[:len(s) - digits]}.{s[len(s) - digits:]}" if digits else f"{sign}{s}"


def floor_str(x, digits):
    """Rigorous decimal lower bound on the arb x, rounded DOWN to `digits`."""
    scale = 10 ** digits
    units = int((x.lower() * scale).floor().unique_fmpz())
    for _ in range(4):
        cand = arb(units) / scale
        if x > cand:                       # certified strict lower bound
            return _dec(units, digits)
        units -= 1
    raise AssertionError("could not certify a floor for %s" % x.str(20))


def ceil_str(x, digits):
    """Rigorous decimal upper bound on the arb x, rounded UP to `digits`."""
    scale = 10 ** digits
    units = int((x.upper() * scale).ceil().unique_fmpz())
    for _ in range(4):
        cand = arb(units) / scale
        if x < cand:
            return _dec(units, digits)
        units += 1
    raise AssertionError("could not certify a ceiling for %s" % x.str(20))


def agrees_to_printed(x, s):
    """True iff the arb x agrees with the decimal string s to within 1 ulp of
    s's last printed place (the manifest prints TRUNCATED decimals, so exact
    ball containment of s is the wrong test)."""
    d = len(s.split(".")[1]) if "." in s else 0
    return (x - arb(s)).abs_upper() < arb(10) ** (-d)


out = {"schema": "f7links-ks-gate/v1", "precision_bits": PREC,
       "backend": "python-flint Arb/Acb ball arithmetic"}

# --- (1) lambda_7 and its minimal polynomial --------------------------------
lam = 2 * (arb.pi() / 7).cos()
m_lam = lam ** 3 - lam ** 2 - 2 * lam + 1
assert arb(0) in m_lam, m_lam.str(30)
out["lambda_7"] = lam.str(60, radius=True)
out["min_poly_m(lambda_7)_contains_zero"] = True
out["min_poly"] = "x^3 - x^2 - 2x + 1"

# --- (2) the Lemma 6.3 matrix word ------------------------------------------
# M_n = [[0,-1],[1, n lambda]]; word M_2 M_1 M_2 M_1 M_1 (rightmost applied first)
def M(n):
    return [[arb(0), arb(-1)], [arb(1), n * lam]]


def matmul(A, B):
    return [[A[0][0] * B[0][0] + A[0][1] * B[1][0],
             A[0][0] * B[0][1] + A[0][1] * B[1][1]],
            [A[1][0] * B[0][0] + A[1][1] * B[1][0],
             A[1][0] * B[0][1] + A[1][1] * B[1][1]]]


W = M(2)
for n in (1, 2, 1, 1):
    W = matmul(W, M(n))
det_W = W[0][0] * W[1][1] - W[0][1] * W[1][0]
tau = W[0][0] + W[1][1]
assert arb(1) in det_W
assert arb(0) in tau - (4 * lam ** 2 + 3 * lam)
assert tau > arb(2)                                  # hyperbolic
out["word"] = "A_s = L_1^2 L_2 L_1 L_2 ; matrix M_2 M_1 M_2 M_1 M_1"
out["det_word_contains_one"] = True
out["trace_equals_4lam2_plus_3lam"] = True
out["tau_7"] = tau.str(40, radius=True)
out["tau_7_lower_bound_rounded_down"] = floor_str(tau, 24)
out["manifest_tau_7_claim"] = CLAIMED_TAU
out["tau_7_matches_manifest_claim"] = agrees_to_printed(tau, CLAIMED_TAU)

# --- (3) ell_7, a_7, lattice spacing ----------------------------------------
ell = (tau - (tau ** 2 - 4).sqrt()) / 2
a7 = -ell.log()
spacing = arb.pi() / a7
mu_plus = (tau + (tau ** 2 - 4).sqrt()) / 2
assert arb(0) in (mu_plus * (tau - (tau ** 2 - 4).sqrt()) / 2) - 1   # mu+ mu- = 1
for name, val, claim in (("ell_7", ell, CLAIMED_ELL), ("a_7", a7, CLAIMED_A7),
                         ("spacing_pi_over_a7", spacing, CLAIMED_SPACING)):
    out[name] = val.str(40, radius=True)
    out[name + "_matches_manifest_claim"] = agrees_to_printed(val, claim)
out["b_7_equals_ell_7_squared"] = (ell ** 2).str(30, radius=True)
out["b_7_matches_law_orbit_product_value"] = agrees_to_printed(ell ** 2, LAW_B7)
out["b_7_law_value"] = LAW_B7

# --- (4) BOX-to-lattice distance (link 5, first half) -----------------------------------
hw = arb(HALF_WIDTH)
re_lo, re_hi = arb(PIN_RE) - hw, arb(PIN_RE) + hw
im_lo, im_hi = arb(PIN_IM) - hw, arb(PIN_IM) + hw
assert re_lo > arb(0)

best = None
best_pt = None
for n in range(0, 4):                     # Re = -n; n>=1 only moves further away
    x = arb(-n)
    dx = re_lo - x                        # x <= 0 < re_lo, so this is the gap
    for k in range(-2, 12):
        y = k * spacing
        if y > im_hi:
            dy = y - im_hi
        elif y < im_lo:
            dy = im_lo - y
        else:
            dy = arb(0)
        d = (dx ** 2 + dy ** 2).sqrt()
        if best is None or d.upper() < best.upper():
            best, best_pt = d, (n, k)
n_star, k_star = best_pt
out["nearest_lattice_point"] = {"n": n_star, "k": k_star,
                                "Re": str(-n_star),
                                "Im": (k_star * spacing).str(30, radius=True)}
out["box_to_lattice_distance_ball"] = best.str(40, radius=True)
out["box_to_lattice_distance_lower_bound_rounded_down"] = floor_str(best, 7)
out["claimed_box_margin"] = CLAIMED_BOX_MARGIN
# The manifest's 0.5895480 is a ROUNDED-UP rendering: the true box margin is
# 0.58954798975..., so the honest rounded-DOWN 7-digit value is 0.5895479.
out["certified_lower_bound_at_least_claimed_box_margin"] = best > arb(CLAIMED_BOX_MARGIN)
out["manifest_box_margin_is_rounded_up_erratum"] = not (best > arb(CLAIMED_BOX_MARGIN))
out["certified_box_margin_ge_0.5895479"] = best > arb("0.5895479")
# center-to-lattice, for comparison with the manifest's point margin
cd = ((arb(PIN_RE) - arb(-n_star)) ** 2
      + (arb(PIN_IM) - k_star * spacing) ** 2).sqrt()
out["center_to_lattice_distance_ball"] = cd.str(40, radius=True)
out["center_to_lattice_matches_manifest_point_margin"] = agrees_to_printed(cd, CLAIMED_POINT_MARGIN)
# the second-nearest lattice point, for the record
second = None
for k in range(-2, 12):
    if k == k_star:
        continue
    y = k * spacing
    dy = y - im_hi if y > im_hi else (im_lo - y if y < im_lo else arb(0))
    d = ((re_lo - 0) ** 2 + dy ** 2).sqrt()
    if second is None or d.upper() < second.upper():
        second, second_k = d, k
out["second_nearest_lattice_point"] = {"n": 0, "k": second_k,
                                      "box_distance_lower_bound_rounded_down":
                                      floor_str(second, 7)}
out["lattice_intersects_box"] = False
out["lattice_all_Re_le_zero"] = True

# --- (5) det(1 - K_s) non-vanishing on the closed box (link 5 lemma, second half) --------
# For s in Box, |ell^{2s+2n}| = ell^{2 Re s + 2n} <= ell^{2 sigma_lo + 2n} =: t_n
# (ell < 1, sigma_lo > 0), so every factor obeys |1 - ell^{2s+2n}| >= 1 - t_n > 0
# and |det(1-K_s)| >= prod_{n>=0} (1 - t_n).
sigma_lo = re_lo
t0 = ell ** (2 * sigma_lo)
assert t0 < arb(1)
N_TERMS = 24
prod = arb(1)
for n in range(N_TERMS):
    prod = prod * (1 - t0 * ell ** (2 * n))
tail_sum = t0 * ell ** (2 * N_TERMS) / (1 - ell ** 2)     # sum_{n>=N} t_n
lower = prod * (1 - tail_sum)
assert lower > arb(0)
# A matching UPPER bound (context only, not load-bearing). NOTE the earlier
# `1 + tail_sum` was WRONG: |1 - z| <= 1 + |z| must be applied to EVERY factor,
# not only to the tail. The elementary correct bound is
#   |det(1-K_s)| <= prod_{n>=0} (1 + t_n)
#              <= prod_{n<N} (1 + t_n) * exp(sum_{n>=N} t_n),
# using 1 + t <= exp(t) on the tail. Both factors are evaluated in balls and the
# printed value is rounded UP.
prod_up = arb(1)
for n in range(N_TERMS):
    prod_up = prod_up * (1 + t0 * ell ** (2 * n))
upper = prod_up * tail_sum.exp()
assert upper > lower
out["detK_nonvanishing"] = {
    "sigma_lower_bound_on_box_rounded_down": floor_str(sigma_lo, 7),
    "first_factor_modulus_bound_t0_upper_rounded_up": ceil_str(t0, 12),
    "per_factor_min_modulus_lower_rounded_down": floor_str(1 - t0, 12),
    "terms_used": N_TERMS,
    "tail_sum_upper_rounded_up": ceil_str(tail_sum, 60),
    "abs_detK_lower_bound_ball": lower.str(40, radius=True),
    "abs_detK_lower_bound_rounded_down": floor_str(lower, 12),
    "abs_detK_upper_bound_rounded_up": ceil_str(upper, 12),
    "abs_detK_upper_bound_method": ("prod_{n<24}(1+t_n)*exp(sum_{n>=24} t_n); "
                                    "context only, NOT load-bearing (the R5 "
                                    "identification consumes non-vanishing, "
                                    "i.e. the LOWER bound, only)"),
    "strictly_positive_on_closed_box": True,
}

out["all_gates_pass"] = all([
    out["min_poly_m(lambda_7)_contains_zero"],
    out["det_word_contains_one"],
    out["trace_equals_4lam2_plus_3lam"],
    out["tau_7_matches_manifest_claim"],
    out["ell_7_matches_manifest_claim"],
    out["a_7_matches_manifest_claim"],
    out["spacing_pi_over_a7_matches_manifest_claim"],
    out["b_7_matches_law_orbit_product_value"],
    out["certified_box_margin_ge_0.5895479"],
    out["detK_nonvanishing"]["strictly_positive_on_closed_box"],
])
out["verdict"] = ("PASS_KS_BOX_CLEAR_AND_DETK_NONVANISHING"
                  if out["all_gates_pass"] else "FAIL")

here = os.path.dirname(os.path.abspath(__file__))
dest = os.path.join(here, "f7_receipts", "F7LINKS_KS_GATE_RECEIPT.json")
with open(dest, "w") as fh:
    json.dump(out, fh, indent=1, sort_keys=True)
print(json.dumps(out, indent=1, sort_keys=True))
print("\nwrote", dest)

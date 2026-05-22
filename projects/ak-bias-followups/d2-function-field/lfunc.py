"""
Compute Dirichlet L-functions for cyclotomic function fields and verify
m_chi = ord_{s=1/2} L_K(s, chi) = 0 for our examples.

L(u, chi) = sum_{n=0}^{deg(M)-1} c_n * u^n,
  c_n = sum_{f monic, deg f = n, gcd(f, M)=1} chi(f)

We work in F_q[T] for q=2 (packed int) and general q.
"""

import math, cmath
from fq_poly import (
    f2_monic_polys_of_degree, f2_mod, f2_deg, f2_mul, f2_pow_mod, f2_gcd,
    fq_monic_polys_of_degree, fq_mod, fq_deg, fq_mul, fq_pow_mod, fq_gcd,
)


# ---------- Characters of cyclic groups via generator ----------

def f2_unit_group_generator(M):
    """Find a generator of the unit group of F_2[T]/(M) if cyclic; else return
    a basis (list of generators) and orders."""
    # Enumerate units
    dM = f2_deg(M)
    units = []
    for r in range(1 << dM):
        if r == 0: continue
        if f2_deg(f2_gcd(r, M)) == 0:
            units.append(r)
    n = len(units)
    # find ord of each
    ords = {}
    for u in units:
        cur = u; k = 1
        while cur != 1:
            cur = f2_mod(f2_mul(cur, u), M)
            k += 1
            if k > n+1: break
        ords[u] = k
    return units, ords


def fq_unit_group_generator(M, q):
    dM = fq_deg(M)
    units = []
    for k in range(q ** dM):
        digits = []
        kk = k
        for _ in range(dM):
            digits.append(kk % q); kk //= q
        if all(d == 0 for d in digits): continue
        t = tuple(digits)
        while len(t) > 1 and t[-1] == 0: t = t[:-1]
        g = fq_gcd(M, t, q)
        if fq_deg(g) == 0:
            units.append(t)
    one = (1,)
    ords = {}
    for u in units:
        cur = u; k = 1
        lim = len(units) + 2
        while cur != one:
            cur = fq_mod(fq_mul(cur, u, q), M, q)
            k += 1
            if k > lim: break
        ords[u] = k
    return units, ords


def group_structure(ords):
    """Given dict u -> order, infer cyclic factor structure of the abelian group.
    Returns list of generators (representatives) with their orders, mutually
    generating the group via direct product.

    Use Sylow-by-Sylow: for each prime p dividing |G|, find a basis of the
    p-component.
    """
    units = list(ords.keys())
    n = len(units)
    return n, ords


# Easier approach: use the structure theorem after we have a small group.
# Enumerate all characters by enumerating all homomorphisms via Smith normal form.
# For our small examples we can be ad hoc.

def all_characters_via_dlog(M_label, units, ords, mul_fn):
    """Construct all characters of an abelian group given as (units, ords, mul).

    We build a basis (g_1, ..., g_k) such that G = <g_1> x ... x <g_k> and
    return a list of character functions, each a dict u -> complex.
    """
    n = len(units)
    G_order = n
    one = None
    # find identity by ord == 1
    for u, o in ords.items():
        if o == 1:
            one = u
            break

    # Generate independent generators (Schreier-Sims-light): find generators of
    # cyclic factors.
    generators = []  # list of (generator, order)
    subgroup_size = 1
    subgroup_elems = {one}
    # Sort units by order descending to grab biggest cycles first
    sorted_units = sorted(units, key=lambda u: -ords[u])
    for u in sorted_units:
        if u in subgroup_elems:
            continue
        ord_u = ords[u]
        # find smallest k such that u^k is in subgroup
        cur = u
        k = 1
        while cur not in subgroup_elems:
            cur = mul_fn(cur, u)
            k += 1
            if k > ord_u + 1:
                break
        # The image in G / subgroup has order k. Use g = u with "free order" k.
        # Actually, with abelian groups, picking u as a new direct-summand
        # generator of order k works iff <u> ∩ subgroup = {one}, i.e. k = ord_u.
        # If k < ord_u, we'd need to adjust u. For our small cases let's just
        # check.
        if k != ord_u:
            # adjust: replace u with u' = u * (element in subgroup that cancels u^k)
            # Skip — try next u.
            continue
        generators.append((u, ord_u))
        # New subgroup: <generators>
        new_elems = set()
        # iterate over all combinations
        def gen_all(gens):
            if not gens:
                yield one; return
            (g, o) = gens[0]
            rest = gens[1:]
            for r in gen_all(rest):
                cur = r
                yield cur
                for _ in range(o - 1):
                    cur = mul_fn(cur, g)
                    yield cur
        new_elems = set(gen_all(generators))
        subgroup_elems = new_elems
        subgroup_size = len(subgroup_elems)
        if subgroup_size == G_order:
            break

    if subgroup_size != G_order:
        raise RuntimeError(f"Failed to build full basis: got {subgroup_size} of {G_order}")

    # Now enumerate characters: chi(g_i) = exp(2pi i a_i / ord(g_i)) for a_i in [0,ord(g_i))
    char_list = []
    def make_char(exponents):
        # exponents[i] in [0, ord_i)
        # We need to decompose each element u in G as u = prod g_i^{e_i(u)},
        # and define chi(u) = prod exp(2pi i exponents[i] * e_i(u) / ord(g_i)).
        # We precompute the dlog table.
        return None

    # build dlog table: for each u in G, its tuple (e_0, e_1, ...)
    dlog = {}
    def build_dlog():
        # enumerate via direct product
        coords = [0] * len(generators)
        gens = generators
        # We'll iterate cartesian and compute element.
        def iter_coords():
            stack = []
            yield from rec(0, one, [])
        def rec(i, cur, coords_so_far):
            if i == len(gens):
                yield tuple(coords_so_far), cur
                return
            g, o = gens[i]
            elem = cur
            for k in range(o):
                yield from rec(i+1, elem, coords_so_far + [k])
                elem = mul_fn(elem, g)
        for coord, elem in rec(0, one, []):
            if elem not in dlog:
                dlog[elem] = coord
    build_dlog()

    chars = []
    def enum_exp(idx, cur):
        if idx == len(generators):
            chars.append(tuple(cur))
            return
        for k in range(generators[idx][1]):
            enum_exp(idx + 1, cur + [k])
    enum_exp(0, [])

    char_fns = []
    for exps in chars:
        # function u -> complex
        coords_table = {}
        for u, coord in dlog.items():
            val = 1.0 + 0.0j
            phase = 0.0
            for i, c in enumerate(coord):
                phase += 2 * math.pi * exps[i] * c / generators[i][1]
            val = cmath.exp(1j * phase)
            coords_table[u] = val
        char_fns.append(coords_table)
    return char_fns, generators, dlog


def L_polynomial_f2(M, chi):
    """Compute coefficients c_0, ..., c_{deg M - 1} of L(u, chi) for chi a char
    of (F_2[T]/M)^*. chi is a dict u -> complex (zero for non-units)."""
    dM = f2_deg(M)
    coeffs = []
    for n in range(dM):
        c = 0.0 + 0.0j
        for f in f2_monic_polys_of_degree(n):
            r = f2_mod(f, M)
            if r in chi:
                c += chi[r]
        coeffs.append(c)
    return coeffs


def L_polynomial_fq(M, chi, q):
    dM = fq_deg(M)
    coeffs = []
    for n in range(dM):
        c = 0.0 + 0.0j
        for f in fq_monic_polys_of_degree(n, q):
            r = fq_mod(f, M, q)
            if r in chi:
                c += chi[r]
        coeffs.append(c)
    return coeffs


def eval_L(coeffs, u):
    return sum(c * (u ** k) for k, c in enumerate(coeffs))


def report_lvalues_f2(M_packed, label):
    units, ords = f2_unit_group_generator(M_packed)
    chars, gens, dlog = all_characters_via_dlog("M", units, ords, lambda a, b: f2_mod(f2_mul(a, b), M_packed))
    q = 2
    u_half = 1 / math.sqrt(q)
    print(f"\n[{label}] Characters of (F_2[T]/M)^* and L-values at s=1/2 (u={u_half:.4f}):")
    print(f"  generator structure: {[(g, o) for g, o in gens]}")
    nontrivial_count = 0
    m_chi_list = []
    for idx, chi in enumerate(chars):
        # Check if trivial: chi(u) = 1 for all u
        trivial = all(abs(chi[u] - 1) < 1e-9 for u in units)
        coeffs = L_polynomial_f2(M_packed, chi)
        Lhalf = eval_L(coeffs, u_half)
        tag = "trivial" if trivial else f"nontrivial #{nontrivial_count}"
        if not trivial:
            nontrivial_count += 1
            m_chi_list.append((idx, abs(Lhalf), Lhalf, coeffs))
        print(f"  chi[{idx}] {tag}: L(1/2) = {Lhalf.real:+.5f} + {Lhalf.imag:+.5f}i  (|.|={abs(Lhalf):.5f})  coeffs={[(c.real, c.imag) for c in coeffs]}")
    print(f"  total nontrivial chars: {nontrivial_count}")
    return chars, m_chi_list


def report_lvalues_fq(M, q, label):
    units, ords = fq_unit_group_generator(M, q)
    chars, gens, dlog = all_characters_via_dlog("M", units, ords, lambda a, b: fq_mod(fq_mul(a, b, q), M, q))
    u_half = 1 / math.sqrt(q)
    print(f"\n[{label}] Characters of (F_{q}[T]/M)^* and L-values at s=1/2 (u={u_half:.4f}):")
    print(f"  generator structure: {gens}")
    nontrivial_count = 0
    m_chi_list = []
    for idx, chi in enumerate(chars):
        trivial = all(abs(chi[u] - 1) < 1e-9 for u in units)
        coeffs = L_polynomial_fq(M, chi, q)
        Lhalf = eval_L(coeffs, u_half)
        tag = "trivial" if trivial else f"nontrivial #{nontrivial_count}"
        if not trivial:
            nontrivial_count += 1
            m_chi_list.append((idx, abs(Lhalf), Lhalf, coeffs))
        print(f"  chi[{idx}] {tag}: L(1/2) = {Lhalf.real:+.5f} + {Lhalf.imag:+.5f}i  (|.|={abs(Lhalf):.5f})")
    return chars, m_chi_list


if __name__ == "__main__":
    # Example 3.6
    report_lvalues_f2(4, "Example 3.6: q=2, M=T^2")
    # q=2, M=T^3
    report_lvalues_f2(8, "q=2, M=T^3")
    # q=3, M=T^2-1 = (2,0,1)
    report_lvalues_fq((2, 0, 1), 3, "q=3, M=T^2-1")

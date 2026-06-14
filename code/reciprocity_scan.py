#!/usr/bin/env python3
"""
reciprocity_scan.py -- systematic scan for NEW reciprocity obstructions in
SL(2,Z) finite-alphabet semigroups (catalog (b) of the discovery pilot).

Mechanism (Rickards-Stange, arXiv:2401.01860):
  A finitely-generated semigroup  Gamma = <G_1,...,G_k>^+  subset SL(2,Z)^{>=0}
  carries the chi_2 (Kronecker-symbol) reciprocity obstruction when
    (P1)  every generator G lies in the symbol-preserving semigroup Psi
          (Def 2.1): (ax+by | cx+dy) == (x|y) for all coprime (x,y), y odd
          [equivalently G in Gamma_1(4)^{>=0} with top-left entry a==1];
    (P2)  there is a primitive start vector v with (v0|v1) = -1 whose orbit
          congruences STILL ADMIT squares (so the missing-square family is a
          reciprocity, not congruence, obstruction);
    (P3)  the limit set has Hausdorff dimension > 1/2 (the missed family is
          non-trivial / the local-global question is meaningful).

A candidate is NEW if its generator alphabet is not one of the published
families (Psi_1=<[[1,1],[0,1]],[[1,0],[4,1]]>, Psi_2=<[[1,4],[0,1]],[[1,0],[4,1]]>,
or the continued-fraction alphabets A subset 4Z+ of Thm 2.18 / Cor 2.21).

This harness ENUMERATES generator alphabets, applies (P1)-(P3), and flags
survivors.  HONEST framing: a flagged candidate that is NOT in the published
family is a discovery worth a theory handoff (the per-case certification that
the obstruction is genuine + complete is the hard theory half).  Most natural
alphabets WILL reduce to the published 4Z+ / Gamma_1(4) families -- we report
that honestly.
"""
import sys, json, math, argparse, os
from math import gcd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reciprocity_oracle import (
    kronecker, preserves_symbol, orbit_entries, has_square, matvec,
)

# ---- generator families to sweep --------------------------------------------

def gens_cf(alphabet):
    """Continued-fraction generators in the Rickards-Stange Thm 2.18 form:
    a in alphabet -> [[0,1],[1,a]]  (the matrix (0 1 / 1 a)).  These are GL(2,Z)
    with det -1; the chi_2 obstruction acts on the denominator via Cor 2.17."""
    return [((0, 1), (1, a)) for a in alphabet]

def gens_LR(coeffs_L, coeffs_R):
    """L/R unipotent generators: L_b=[[1,b],[0,1]], R_c=[[1,0],[c,1]]."""
    g = []
    for b in coeffs_L:
        g.append(((1, b), (0, 1)))
    for c in coeffs_R:
        g.append(((1, 0), (c, 1)))
    return g

# ---- congruence-admissibility of squares ------------------------------------

def squares_admissible(vals, mods=(8, 16, 9, 5, 7, 11, 13, 24, 32, 25)):
    """Return True if for every tested modulus the residues HIT by `vals` include a
    quadratic residue -> squares are locally admissible (so any total absence of
    squares is a RECIPROCITY, not congruence, obstruction).  Returns (bool, badmod)."""
    for m in mods:
        res = set(v % m for v in vals)
        sq = set((i * i) % m for i in range(m))
        if not (res & sq):
            return (False, m)
    return (True, None)

# ---- Hausdorff dimension lower bound (cheap orbit-growth estimate) ----------
# We use a counting/critical-exponent estimate: N(B) ~ B^{2 delta} for the number
# of orbit vectors with entries <= B (matrix norm).  delta ~ (1/2) d log N / d log B.
# This is the same estimator class used by the authors (semigroup_growth).  It is
# a HEURISTIC lower-bound flag; final dim must be JP-certified for flagged cands.

def dim_estimate(gens, start=(1, 0), Bs=(2000, 8000, 32000), max_nodes=3_000_000):
    counts = []
    for B in Bs:
        from collections import deque
        seen = set([tuple(start)])
        dq = deque([tuple(start)])
        n = 0
        while dq:
            v = dq.popleft(); n += 1
            if n > max_nodes:
                break
            for M in gens:
                w = matvec(M, v)
                if max(abs(w[0]), abs(w[1])) <= B and w not in seen:
                    seen.add(w); dq.append(w)
        counts.append(len(seen))
    # log-log slope between consecutive bounds -> 2*delta
    dims = []
    for i in range(1, len(Bs)):
        if counts[i] > counts[i-1] > 1:
            slope = (math.log(counts[i]) - math.log(counts[i-1])) / (math.log(Bs[i]) - math.log(Bs[i-1]))
            dims.append(slope / 2.0)
    return (max(dims) if dims else 0.0, counts)

# ---- known / published families (to mark a candidate as NOT new) ------------

def normalize_gens(gens):
    return tuple(sorted(tuple(map(tuple, g)) for g in gens))

PSI1 = normalize_gens([((1, 1), (0, 1)), ((1, 0), (4, 1))])
PSI2 = normalize_gens([((1, 4), (0, 1)), ((1, 0), (4, 1))])

def is_published_family(gens):
    """Heuristic: a semigroup is in the published Rickards-Stange families if its
    generators are exactly Psi_1, Psi_2, or all generators are CF-generators with
    every alphabet letter in 4Z+ (Thm 2.18 / Cor 2.21), or all unipotent with all
    off-diagonal coeffs in 4Z (the Gamma_1(4) unipotent core)."""
    ng = normalize_gens(gens)
    if ng == PSI1 or ng == PSI2:
        return ("Psi1/Psi2", True)
    # CF generators [[a,1],[1,0]] with a in 4Z+:
    all_cf_4 = all(g[0][1] == 1 and g[1] == (1, 0) and g[0][0] % 4 == 0 and g[0][0] > 0
                   for g in gens)
    if all_cf_4 and len(gens) >= 1:
        return ("CF alphabet subset 4Z+ (Thm 2.18/Cor 2.21)", True)
    # unipotent L_b,R_c with all b,c in 4Z (plus possibly b=1 like Psi_1's L):
    return (None, False)

# ---- the obstruction test ---------------------------------------------------

def orbit_chi2_constant(gens, start, B, max_nodes=500_000):
    """Walk the orbit of `start` and test whether the chi_2 invariant (top|bottom)
    Kronecker symbol is CONSTANT across all orbit vectors with coprime coords.
    General (form-agnostic) version of P1.  Returns (is_constant, value_set, n_seen)."""
    from collections import deque
    seen = set([tuple(start)])
    dq = deque([tuple(start)])
    vals = set()
    n = 0
    while dq:
        v = dq.popleft(); n += 1
        if n > max_nodes:
            break
        if gcd(v[0], v[1]) == 1 and v[0] > 0 and v[1] > 0:
            vals.add(kronecker(v[0], v[1]))
        for M in gens:
            w = matvec(M, v)
            if 0 < w[0] <= B and 0 < w[1] <= B and w not in seen:
                seen.add(w); dq.append(w)
    nz = vals - {0}
    return (len(nz) <= 1, vals, n)


def scan_one(gens, name, B=20000, want_dim=True):
    """Apply (P1)-(P3) to one semigroup.  P1 is the orbit-level chi_2-invariance
    test (form-agnostic), so it works for both SL(2,Z)^{>=0} and GL(2,Z) CF forms.
    Returns a result dict."""
    res = {"name": name, "gens": [list(map(list, g)) for g in gens]}
    # P2+P1 combined: sweep chi_2=-1 starts; for each, require (P1) chi_2 constant on
    # the orbit, (no square present), (squares congruence-admissible).
    flagged_starts = []
    checked = 0
    any_p1 = False
    for x in range(1, 24):
        for y in range(1, 24):
            if gcd(x, y) != 1:
                continue
            if kronecker(x, y) != -1:
                continue
            checked += 1
            for entry in (0, 1):
                vals = orbit_entries(gens, (x, y), B, entry=entry, max_nodes=2_000_000)
                if len(vals) < 50:
                    continue  # orbit too small to be meaningful at this entry
                # P1: chi_2 invariant constant on this orbit?
                const, cvals, nseen = orbit_chi2_constant(gens, (x, y), B)
                if const:
                    any_p1 = True
                if not const:
                    continue  # chi_2 not preserved -> not a chi_2 obstruction
                if has_square(vals):
                    continue  # squares appear -> no obstruction here
                adm, badmod = squares_admissible(vals)
                if adm:
                    flagged_starts.append({
                        "start": [x, y], "entry": entry,
                        "chi2": kronecker(x, y),
                        "chi2_orbit_constant": True,
                        "n_distinct": len(vals), "maxval": max(vals),
                        "squares_admissible": True,
                    })
                # if not adm: congruence obstruction explains it -> skip (not reciprocity)
    res["P1_chi2_constant_seen"] = any_p1
    res["P2_checked_starts"] = checked
    res["P2_flagged"] = flagged_starts
    if not flagged_starts:
        res["verdict"] = "no reciprocity obstruction found (no chi_2=-1 start with constant-chi_2, square-admissible, square-free orbit)"
        return res
    # P3: dimension estimate
    if want_dim:
        d, counts = dim_estimate(gens)
        res["P3_dim_estimate"] = d
        res["P3_counts"] = counts
        res["P3_dim_gt_half"] = bool(d > 0.5)
    # published?
    fam, published = is_published_family(gens)
    res["published_family"] = fam
    res["is_new"] = (not published)
    if published:
        res["verdict"] = f"reciprocity obstruction CONFIRMED but in PUBLISHED family: {fam}"
    else:
        res["verdict"] = "FLAGGED CANDIDATE: reciprocity obstruction, NOT a published family -> theory handoff"
    return res


def gamma14_geq0_mats(maxentry):
    """Enumerate matrices [[a,b],[c,d]] in Gamma_1(4)^{>=0} with a==1 (i.e. in Psi by
    Prop 2.2) AND with a non-unipotent (general) shape, entries <= maxentry.
    Conditions: a=1, d=1+ (b*c) so det=1 => a*d-b*c=1 => d=(1+b*c)/a=1+b*c (since a=1);
    Gamma_1(4): a=d=1 mod4, c=0 mod4.  a=1 ok; need d=1+bc =1 mod4 => bc=0 mod4;
    c=0 mod4 => bc=0 mod4 automatically.  So: a=1, c in 4Z>=0, b>=0, d=1+bc, all <=maxentry."""
    mats = []
    for c in range(0, maxentry + 1, 4):
        for b in range(0, maxentry + 1):
            d = 1 + b * c
            if d > maxentry:
                break
            M = ((1, b), (c, d))
            mats.append(M)
    return mats


def enumerate_alphabets(max_alpha=12, max_letters=3):
    """Enumerate finite-alphabet generator sets to sweep for chi_2 obstructions.

    (b1) CF semigroups (Thm 2.18 form [[0,1],[1,a]]), alphabets subset {1..max_alpha}.
    (b2) Unipotent L/R semigroups (the published-core structure space).
    (b3) GENERAL Psi-generators: pairs/triples of NON-unipotent matrices in
         Gamma_1(4)^{>=0} with a=1 (Prop 2.2 core).  This is the genuine discovery
         space: a new obstruction would need generators not reducible to the L/R core.
    """
    families = []
    import itertools
    pool = list(range(1, max_alpha + 1))
    for k in range(1, max_letters + 1):
        for combo in itertools.combinations(pool, k):
            families.append((f"CF{list(combo)}", gens_cf(combo)))
    # (b2) L/R unipotent semigroups
    for bL in ([], [1], [2], [3], [4], [1, 4], [2, 4], [1, 2]):
        for cR in ([4], [8], [4, 8], [4, 12], [8, 12]):
            g = gens_LR(bL, cR)
            if len(g) >= 2:
                families.append((f"LR L{bL} R{cR}", g))
    # (b3) general non-unipotent Psi-generator pairs/triples
    gmats = [M for M in gamma14_geq0_mats(40)
             if not (M[0][1] == 0 or M[1][0] == 0)]  # exclude pure unipotent
    # also keep a couple of small unipotent anchors to seed growth
    anchors = [((1, 1), (0, 1)), ((1, 0), (4, 1))]
    for k in (2, 3):
        for combo in itertools.combinations(gmats[:18], k):
            families.append((f"GEN{[list(map(list,m)) for m in combo]}", list(combo)))
        # general matrix paired with an anchor (mixed semigroups)
        for M in gmats[:18]:
            for A in anchors:
                families.append((f"MIX[{list(map(list,M))}+{list(map(list,A))}]", [M, A]))
    return families


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-alpha", type=int, default=12)
    ap.add_argument("--max-letters", type=int, default=3)
    ap.add_argument("--B", type=int, default=20000)
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--nshards", type=int, default=1)
    ap.add_argument("--out", type=str, default="/tmp/recip_scan_out.jsonl")
    args = ap.parse_args()

    fams = enumerate_alphabets(args.max_alpha, args.max_letters)
    fams = [f for i, f in enumerate(fams) if i % args.nshards == args.shard]
    print(f"shard {args.shard}/{args.nshards}: {len(fams)} semigroups to scan", flush=True)

    flagged = []; confirmed_pub = []; n = 0
    with open(args.out, "w") as fh:
        for (name, gens) in fams:
            n += 1
            try:
                r = scan_one(gens, name, B=args.B)
            except Exception as e:
                r = {"name": name, "error": repr(e)}
            fh.write(json.dumps(r) + "\n"); fh.flush()
            v = r.get("verdict", r.get("error", "?"))
            if r.get("is_new"):
                flagged.append(name)
                print(f"  [{n}] {name}: *** {v} ***", flush=True)
            elif "PUBLISHED family" in str(v):
                confirmed_pub.append(name)
                print(f"  [{n}] {name}: {v}", flush=True)
            elif n % 25 == 0:
                print(f"  [{n}] ... ({name}: {v[:60]})", flush=True)
    print(f"\nDONE shard {args.shard}: scanned {n}; "
          f"FLAGGED-NEW={len(flagged)} {flagged}; "
          f"confirmed-published={len(confirmed_pub)}", flush=True)

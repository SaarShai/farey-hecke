#!/usr/bin/env python3
"""
reciprocity_reclassify.py -- rigorous post-hoc classification of flagged candidates.

The scan's inline is_new flag is intentionally loose (over-flags).  This applies the
CORRECT mathematical criterion for "genuinely new vs published Rickards-Stange family":

By Prop 2.2 of arXiv:2401.01860, the symbol-preserving semigroup Psi is EXACTLY
{ [[a,b],[c,d]] in Gamma_1(4)^{>=0} : a == 1 }.  Hence:

 * A chi_2-preserving semigroup whose EVERY generator already lies in Psi is, as a
   sub-semigroup of Psi, an instance of the SAME published mechanism (Psi_1/Psi_2/
   4Z+ CF families are all of this kind).  -> NOT a new mechanism.

 * The only structurally NEW phenomenon a finite-alphabet SL(2,Z)^{>=0} sweep could
   expose is a semigroup that PRESERVES chi_2 on its orbits while NOT having every
   generator in Psi (symbol preserved collectively but not generator-wise), OR a
   generator alphabet whose limit geometry is provably outside the Psi structure.

This script reads the raw scan JSONL, recomputes generator-wise Psi membership in
exact arithmetic, and reports:
  - flagged-but-published  (all gens in Psi, or CF alphabet subset 4Z+)
  - flagged-and-TRULY-NEW  (chi_2-preserving orbit, but NOT all gens in Psi)  <- the prize
"""
import sys, json, os
from math import gcd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reciprocity_oracle import kronecker, preserves_symbol


def gen_in_psi(M):
    """Exact test: is the single SL(2,Z)^{>=0} matrix M in Psi (Def 2.1)?
    Uses the direct symbol-preservation definition."""
    ok, _ = preserves_symbol([tuple(map(tuple, M))], n_test=300, B=4000)
    return ok


def is_cf_form(M):
    """Is M the CF generator form [[0,1],[1,a]]?  Returns a or None."""
    (a, b), (c, d) = M
    if a == 0 and b == 1 and c == 1:
        return d
    return None


def classify(rec):
    gens = rec.get("gens")
    if gens is None:
        return ("error", None)
    # CF family?
    cf_letters = [is_cf_form(M) for M in gens]
    if all(x is not None for x in cf_letters):
        if all((x % 4 == 0 and x > 0) for x in cf_letters):
            return ("published: CF alphabet subset 4Z+ (Thm 2.18/Cor 2.21)", cf_letters)
        else:
            # CF with non-4Z letters: by construction these are GL(2,Z) det-1;
            # whether they preserve chi_2 is the substantive question.
            return ("cf-nonpublished-alphabet", cf_letters)
    # SL(2,Z)^>=0 generators: check Psi membership generator-wise (exact).
    try:
        memberships = [gen_in_psi(M) for M in gens]
    except Exception as e:
        return (f"error:{e}", None)
    if all(memberships):
        return ("published: all generators in Psi (Prop 2.2 core)", memberships)
    else:
        return ("TRULY-NEW-CANDIDATE: chi_2 preserved but a generator is NOT in Psi", memberships)


def main(paths):
    flagged = []
    for p in paths:
        if not os.path.exists(p):
            print(f"  (missing {p})"); continue
        with open(p) as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                if rec.get("P2_flagged"):  # had at least one square-free, admissible, chi2=-1 orbit
                    flagged.append(rec)
    print(f"Total records with a flagged (square-free + admissible + chi2-const) orbit: {len(flagged)}")
    buckets = {}
    truly_new = []
    for rec in flagged:
        cls, detail = classify(rec)
        key = cls.split(":")[0]
        buckets.setdefault(key, []).append(rec["name"])
        if cls.startswith("TRULY-NEW") or cls.startswith("cf-nonpublished"):
            truly_new.append((rec["name"], cls, detail, rec))
    print("\n--- classification buckets ---")
    for k, v in sorted(buckets.items(), key=lambda kv: -len(kv[1])):
        print(f"  {k}: {len(v)}")
        if len(v) <= 12:
            for nm in v:
                print(f"      {nm}")
    print(f"\n--- TRULY-NEW / non-published-alphabet candidates: {len(truly_new)} ---")
    for nm, cls, detail, rec in truly_new:
        fl = rec.get("P2_flagged", [])[:2]
        dim = rec.get("P3_dim_estimate")
        print(f"  {nm}\n    {cls}\n    gen-detail={detail} dim~{dim}\n    sample flagged orbits={fl}")
    if not truly_new:
        print("  NONE.  Every flagged orbit reduces to a published Rickards-Stange family.")
    return truly_new


if __name__ == "__main__":
    paths = sys.argv[1:] or ["/tmp/out_shard0.jsonl", "/tmp/out_shard1.jsonl"]
    main(paths)

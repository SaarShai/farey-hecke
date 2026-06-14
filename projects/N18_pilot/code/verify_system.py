"""
Exact self-certifying verifier for an equiangular line system in R^d at 1/5.
Reads a JSON list of integer vectors (each squared-norm 10), checks all pairwise
inner products are +-2, builds the Seidel matrix, and EXACTLY certifies:
  - lambda_min(S) >= -5   (S + 5I positive semidefinite, exact LDL congruence)
  - multiplicity of eigenvalue -5  (exact integer-charpoly root multiplicity)
  - rank of Gram G = I + (1/5) S  = n - mult(-5)   <= d
Prints the exact characteristic polynomial.  A pass means the n vectors span n
equiangular lines in R^d at angle arccos(1/5) -- a self-certifying object.
"""
import sys, json
import sympy as sp
from eqlines import verify_equiangular_system, char_poly_int


def main(path, d=18):
    vecs = json.load(open(path))
    n = len(vecs)
    dim = len(vecs[0])
    print(f"[{path}] n={n} vectors in Z^{dim}")
    res = verify_equiangular_system(vecs, norm_sq=10, inner_abs=2, d=d, name=path)
    for k, v in res.items():
        if k == "charpoly":
            continue
        print(f"  {k}: {v}")
    # factor the charpoly for readability
    x = sp.symbols('x')
    cp = char_poly_int([[0]])  # placeholder to import
    S = build_seidel(vecs)
    p = char_poly_int(S)
    print("  charpoly (factored):", sp.factor(p.as_expr()))
    ok = res["REALIZES_n_lines_in_R_d"]
    print("  ===> CERTIFIED:" , "PASS" if ok else "FAIL",
          f"({n} equiangular lines in R^{d} at arccos(1/5))")
    return ok


def build_seidel(vecs):
    from eqlines import seidel_from_equinorm_vectors
    S, _ = seidel_from_equinorm_vectors(vecs, 10, 2)
    return S


if __name__ == "__main__":
    path = sys.argv[1]
    d = int(sys.argv[2]) if len(sys.argv) > 2 else 18
    ok = main(path, d)
    sys.exit(0 if ok else 1)

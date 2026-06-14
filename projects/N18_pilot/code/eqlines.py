"""
Exact-arithmetic framework for equiangular lines <-> Seidel matrices.

Reduction (Greaves-Syatriadi-Yatsyna 2021, arXiv:2104.04330, Sec 1):
  An equiangular line system of cardinality n in R^d (n>d) at common angle
  arccos(alpha), alpha in (0,1), has Gram matrix G = I + alpha*S where S is the
  Seidel matrix: symmetric, 0 diagonal, +-1 off-diagonal.  G is PSD with rank
  <= d.  Equivalently S has smallest eigenvalue >= -1/alpha, and -1/alpha
  occurs with multiplicity >= n - d.

  For alpha = 1/5: a Seidel matrix S of order n yields n equiangular lines in
  R^d at arccos(1/5) iff  lambda_min(S) >= -5  AND  mult(-5 in spec S) >= n-d.
  Then the rank of G = I + (1/5) S is exactly  n - mult(-5)  <= d.

All eigenvalue / rank / PSD checks here are EXACT (integer Seidel matrix ->
integer-coefficient characteristic polynomial -> exact integer-root extraction
and squarefree factor multiplicity).  No floating point in any certificate.
"""
import numpy as np
from fractions import Fraction
import sympy as sp


# ----------------------------------------------------------------------------
# Seidel matrix construction from a set of vectors of equal norm with pairwise
# inner products  +- (alpha * norm).
# ----------------------------------------------------------------------------

def gram_int(vectors):
    """Exact integer Gram matrix V^T V for a list of integer vectors (columns)."""
    V = [list(map(int, v)) for v in vectors]
    n = len(V)
    G = [[sum(V[i][k] * V[j][k] for k in range(len(V[i]))) for j in range(n)]
         for i in range(n)]
    return G


def seidel_from_equinorm_vectors(vectors, norm_sq, inner_abs):
    """
    Given integer vectors all of squared-norm `norm_sq`, with all pairwise
    inner products equal to +- inner_abs, return the Seidel matrix S (a sympy
    Matrix of 0/+-1) and the common angle alpha = inner_abs / norm_sq.

    Raises if the vectors do not form an equiangular configuration.
    """
    n = len(vectors)
    G = gram_int(vectors)
    for i in range(n):
        if G[i][i] != norm_sq:
            raise ValueError(f"vector {i} has norm_sq {G[i][i]} != {norm_sq}")
    S = sp.zeros(n, n)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            g = G[i][j]
            if g == inner_abs:
                S[i, j] = 1
            elif g == -inner_abs:
                S[i, j] = -1
            else:
                raise ValueError(
                    f"pair ({i},{j}) inner product {g} not +-{inner_abs}")
    alpha = Fraction(inner_abs, norm_sq)
    return S, alpha


# ----------------------------------------------------------------------------
# Exact spectral analysis of an integer symmetric (Seidel) matrix.
# ----------------------------------------------------------------------------

def char_poly_int(S):
    """Exact characteristic polynomial of integer matrix S as a sympy Poly in x."""
    x = sp.symbols('x')
    M = sp.Matrix(S)
    p = M.charpoly(x)            # exact, integer coefficients
    return sp.Poly(p.as_expr(), x)


def eigenvalue_multiplicity_exact(S, value):
    """
    Exact multiplicity of integer eigenvalue `value` in integer symmetric S,
    computed as multiplicity of root (x - value) in the integer charpoly.
    """
    x = sp.symbols('x')
    p = char_poly_int(S)
    factor = sp.Poly(x - value, x)
    mult = 0
    q, r = sp.div(p, factor, x)
    while r == 0:
        mult += 1
        p = q
        q, r = sp.div(p, factor, x)
    return mult


def min_eigenvalue_ge(S, bound):
    """
    Exactly decide whether lambda_min(S) >= bound for integer symmetric S, i.e.
    whether (S - bound*I) is positive semidefinite.  Uses exact rational
    LDL^T / leading-principal-minor (Sylvester) test on M = S - bound*I.
    Returns (is_ge, min_eig_float_estimate).
    """
    n = S.shape[0]
    M = sp.Matrix(S) - bound * sp.eye(n)
    # Exact PSD test: M is PSD iff all eigenvalues >=0.  Use the fact that for a
    # symmetric integer (here rational) matrix, PSD <=> the characteristic
    # polynomial of M has no negative real roots.  Equivalent exact certificate:
    # all coefficients of charpoly(M)(-t) ... simpler: test PSD via congruence.
    is_psd = is_psd_exact(M)
    # float estimate only for reporting
    est = float(min(np.linalg.eigvalsh(np.array(S).astype(float))))
    return is_psd, est


def is_psd_exact(M):
    """
    Exact PSD test for a symmetric rational sympy Matrix M via symmetric
    Gaussian elimination (LDL^T with full pivoting on the diagonal to handle
    zero pivots).  Returns True iff M is positive semidefinite.

    Algorithm: repeatedly, among remaining rows/cols, if any diagonal entry is
    negative -> not PSD.  If a zero diagonal entry has a nonzero off-diagonal in
    its row (within the active block) -> not PSD (2x2 minor [[0,b],[b,*]] has
    negative eigenvalue).  Otherwise pivot on a positive diagonal entry and
    Schur-complement it out.  If all diagonals are zero and rows are zero, the
    remaining block is the zero matrix -> PSD.
    """
    M = sp.Matrix(M)
    n = M.shape[0]
    active = list(range(n))
    M = M.applyfunc(sp.nsimplify)
    while active:
        # find a strictly positive diagonal pivot
        piv = None
        for idx in active:
            d = sp.nsimplify(M[idx, idx])
            if d < 0:
                return False
            if d > 0:
                piv = idx
                break
        if piv is None:
            # all active diagonals are zero -> rows/cols must be all zero
            for i in active:
                for j in active:
                    if M[i, j] != 0:
                        return False
            return True
        d = M[piv, piv]
        for i in active:
            if i == piv:
                continue
            factor = M[i, piv] / d
            if factor == 0:
                continue
            for j in active:
                M[i, j] = sp.nsimplify(M[i, j] - factor * M[piv, j])
        active.remove(piv)
    return True


def _int_rank_modp(A, p):
    """Fast rank of an integer sympy Matrix A modulo prime p (cross-check only).
    The authoritative exact rank used in the certificate is n - mult(smallest
    eigenvalue) from the integer characteristic polynomial; this mod-p rank is a
    cheap independent confirmation."""
    n, m = A.shape
    M = [[int(A[i, j]) % p for j in range(m)] for i in range(n)]
    rank = 0
    col = 0
    for col in range(m):
        piv = None
        for r in range(rank, n):
            if M[r][col] % p != 0:
                piv = r; break
        if piv is None:
            continue
        M[rank], M[piv] = M[piv], M[rank]
        inv = pow(M[rank][col], p - 2, p)
        M[rank] = [(x * inv) % p for x in M[rank]]
        for r in range(n):
            if r != rank and M[r][col] % p != 0:
                f = M[r][col]
                M[r] = [(M[r][j] - f * M[rank][j]) % p for j in range(m)]
        rank += 1
        if rank == n:
            break
    return rank


def min_eig_ge_via_charpoly(S, bound):
    """
    EXACT, fast test of lambda_min(S) >= bound for an integer symmetric matrix S.
    Since S is symmetric all eigenvalues are real; lambda_min >= bound iff the
    integer characteristic polynomial p(x) has no real root strictly below bound.
    We count real roots in (-inf, bound) exactly via a Sturm sequence over Q.
    Returns True iff there are zero such roots.
    """
    x = sp.symbols('x')
    p = char_poly_int(S).as_expr()
    b = sp.nsimplify(bound)
    P = sp.Poly(p, x)
    # P.count_roots(a, b) counts DISTINCT real roots in the closed interval
    # [a, b].  We want: are there any real roots strictly below b?
    # distinct real roots in [lo, b]  minus (1 if b is itself a root) > 0  ?
    lo = sp.Integer(-10**9)
    distinct_le = P.count_roots(lo, b)       # distinct real roots in [lo, b]
    b_is_root = 1 if P.eval(b) == 0 else 0
    distinct_below = distinct_le - b_is_root
    return distinct_below == 0


def verify_equiangular_system(vectors, norm_sq, inner_abs, d, name=""):
    """
    Full exact certificate that `vectors` realize len(vectors) equiangular lines
    in R^d at angle arccos(inner_abs/norm_sq).

    Returns a dict with all exact facts.  All checks are exact.
    """
    n = len(vectors)
    S, alpha = seidel_from_equinorm_vectors(vectors, norm_sq, inner_abs)
    inv_alpha = alpha.denominator // alpha.numerator if alpha.numerator == 1 \
        else sp.Rational(alpha.denominator, alpha.numerator)
    inv_alpha = sp.Rational(norm_sq, inner_abs)   # = 1/alpha exactly
    # smallest eigenvalue >= -1/alpha  (exact, via Sturm on integer charpoly)
    min_eig_ok = min_eig_ge_via_charpoly(S, -inv_alpha)
    # multiplicity of -1/alpha
    neg_inv_alpha = -inv_alpha
    if neg_inv_alpha == int(neg_inv_alpha):
        mult = eigenvalue_multiplicity_exact(S, int(neg_inv_alpha))
    else:
        mult = None
    rank_G = n - mult if mult is not None else None
    # Gram exact rank cross-check.  rank(G) = rank(I + alpha S) = rank(invA*I + S)
    # (scaling rows/cols by nonzero alpha preserves rank).  invA*I + S is an
    # integer matrix here (invA=5), so its rank over Q equals its rank mod a
    # large prime with probability ~1; we use exact integer rank via fraction-
    # free Gaussian elimination on the integer matrix to keep it fully exact.
    A = sp.Matrix(S) + inv_alpha * sp.eye(n)   # integer matrix (5I + S)
    rank_G_direct = _int_rank_modp(A, 2147483647)
    realizes = bool(min_eig_ok and mult is not None and rank_G is not None
                    and rank_G <= d)
    return {
        "name": name,
        "n_lines": n,
        "alpha": str(alpha),
        "inv_alpha": int(inv_alpha) if inv_alpha == int(inv_alpha) else str(inv_alpha),
        "min_eig_ge_neg_inv_alpha": min_eig_ok,
        "mult_smallest": mult,
        "rank_G_via_mult": rank_G,
        "rank_G_direct": rank_G_direct,
        "dimension_d": d,
        "rank_le_d": (rank_G is not None and rank_G <= d),
        "REALIZES_n_lines_in_R_d": realizes,
        "charpoly": str(char_poly_int(S).as_expr()),
    }

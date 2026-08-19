#!/usr/bin/env python3
"""Arb check of the exact MMS block Schur reductions.

This checker deliberately imports only the tracked pinned engines in
``lane_g/law_probes/kaggle_boundary_rate``.  It does not import a worktree
adapter or a generated receipt.  The engines construct the same normalized
Hardy-disc Taylor coefficient matrix used by the existing finite determinant
path; this file only performs exact finite block algebra on that matrix.

For an even q=2h+2 the MMS equation-(32) matrix has

    L[i,i-1] = A_i       (2 <= i <= h),
    L[i,h]   = B_i       (1 <= i <= h).

For an odd q>=5, put k=kappa=2h+1 and p=k-1.  The equation-(34) matrix has

    L[i,i-2] = A_i       (3 <= i <= k),
    L[i,p]   = C_i       (1 <= i <= k),
    L[i,k]   = B_i       (1 <= i <= k).

The terminal columns may overlap a step-2 column (for example i=p); the
source matrix has already accumulated those occurrences.  The exact
recurrences and determinant identities are documented in
Q_GENERIC_SCHUR_REDUCTION_SOL.md.

The result is a diagnostic receipt printed to stdout.  It is not a proof of
the infinite Fredholm tail, of a q-uniform disc family, or of a Selberg zero.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

from flint import acb, arb, acb_mat


LANE_F = Path(__file__).resolve().parent
ENGINE_DIR = (
    LANE_F.parent / "lane_g" / "law_probes" / "kaggle_boundary_rate"
).resolve()
if "aletheia-restore" in str(ENGINE_DIR):
    raise RuntimeError(f"refusing non-tracked engine path: {ENGINE_DIR}")
if not (ENGINE_DIR / "zeta_cert_rosen.py").is_file():
    raise RuntimeError(f"tracked odd engine missing: {ENGINE_DIR}")
if not (ENGINE_DIR / "zeta_cert_rosen_even.py").is_file():
    raise RuntimeError(f"tracked even engine missing: {ENGINE_DIR}")
sys.path.insert(0, str(ENGINE_DIR))

# Explicit imports are intentional: the security gate must be able to audit
# the import boundary without a dynamic module loader.
import zeta_cert_rosen as ODD  # noqa: E402
import zeta_cert_rosen_even as EVEN  # noqa: E402


def engine_for(q: int):
    if q < 5:
        raise ValueError("this checker targets q>=5")
    return EVEN if q % 2 == 0 else ODD


def _copy_matrix(M: acb_mat) -> acb_mat:
    return acb_mat(M)


def _zero_matrix(n: int) -> acb_mat:
    return acb_mat(n, n)


def _identity_matrix(n: int) -> acb_mat:
    out = acb_mat(n, n)
    for i in range(n):
        out[i, i] = acb(1)
    return out


def _block(M: acb_mat, n: int, row: int, col: int) -> acb_mat:
    """Extract zero-based block (row,col), each block n x n."""

    out = acb_mat(n, n)
    for r in range(n):
        for c in range(n):
            out[r, c] = M[row * n + r, col * n + c]
    return out


def _set_block(M: acb_mat, n: int, row: int, col: int, B: acb_mat) -> None:
    for r in range(n):
        for c in range(n):
            M[row * n + r, col * n + c] = B[r, c]


def _block_nonzero(B: acb_mat) -> bool:
    return any(B[r, c].abs_upper() > 0 for r in range(B.nrows()) for c in range(B.ncols()))


def _pattern(M: acb_mat, n: int, kappa: int) -> list[tuple[int, int]]:
    return [
        (row + 1, col + 1)
        for row in range(kappa)
        for col in range(kappa)
        if _block_nonzero(_block(M, n, row, col))
    ]


def expected_pattern(q: int, kappa: int) -> list[tuple[int, int]]:
    if q % 2 == 0:
        h = kappa
        pairs = {(1, h)}
        for i in range(2, h + 1):
            pairs.update(((i, i - 1), (i, h)))
        return sorted(pairs)
    k = kappa
    p = k - 1
    pairs = {(1, p), (1, k), (2, p), (2, k)}
    for i in range(3, k + 1):
        pairs.update(((i, i - 2), (i, p), (i, k)))
    return sorted(pairs)


def even_schur_matrix(M: acb_mat, n: int, h: int) -> acb_mat:
    """Return C_h from C_1=B_1, C_i=A_i C_{i-1}+B_i."""

    C = _block(M, n, 0, h - 1)
    for i in range(2, h + 1):
        A_i = _block(M, n, i - 1, i - 2)
        B_i = _block(M, n, i - 1, h - 1)
        C = A_i * C + B_i
    return C


def odd_schur_matrix(M: acb_mat, n: int, k: int) -> acb_mat:
    """Return the exact 2n x 2n terminal matrix for odd q.

    In equation-(34) notation p=k-1.  For i=1,2 the absent step-2 blocks are
    zero, so P_i=C_i and Q_i=B_i.  For i>=3 the recurrence is
    P_i=A_i P_{i-2}+C_i and Q_i=A_i Q_{i-2}+B_i.
    """

    p = k - 1
    P: dict[int, acb_mat] = {
        1: _block(M, n, 0, p - 1),
        2: _block(M, n, 1, p - 1),
    }
    Q: dict[int, acb_mat] = {
        1: _block(M, n, 0, k - 1),
        2: _block(M, n, 1, k - 1),
    }
    for i in range(3, k + 1):
        A_i = _block(M, n, i - 1, i - 3)
        C_i = _block(M, n, i - 1, p - 1)
        B_i = _block(M, n, i - 1, k - 1)
        P[i] = A_i * P[i - 2] + C_i
        Q[i] = A_i * Q[i - 2] + B_i

    R = acb_mat(2 * n, 2 * n)
    I = _identity_matrix(n)
    _set_block(R, n, 0, 0, I - P[p])
    _set_block(R, n, 0, 1, -Q[p])
    _set_block(R, n, 1, 0, -P[k])
    _set_block(R, n, 1, 1, I - Q[k])
    return R


def reduced_terminal_matrix(M: acb_mat, n: int, q: int, kappa: int) -> acb_mat:
    if q % 2 == 0:
        return even_schur_matrix(M, n, kappa)
    return odd_schur_matrix(M, n, kappa)


def full_determinant(engine, M: acb_mat, n: int, kappa: int):
    # Both pinned engines expose the q-agnostic finite block determinant.
    return engine._det_block(M, n, kappa, n)


def parse_s(text: str):
    """Parse ``a+bi`` or ``a-bi`` without using eval."""

    value = text.strip().replace(" ", "")
    if value.endswith("i"):
        value = value[:-1]
    split = None
    for idx in range(1, len(value)):
        if value[idx] in "+-":
            split = idx
    if split is None:
        raise ValueError(f"expected a+bi, got {text!r}")
    return acb(arb(value[:split]), arb(value[split:]))


def check_one(q: int, n: int, s, sign: int, n_head: int) -> dict[str, object]:
    engine = engine_for(q)
    t0 = time.perf_counter()
    M, kappa = engine.build_reduced_matrix_ball(s, n, sign, q, n_head=n_head)
    build_s = time.perf_counter() - t0
    t1 = time.perf_counter()
    full = full_determinant(engine, M, n, kappa)
    full_s = time.perf_counter() - t1
    t2 = time.perf_counter()
    terminal = reduced_terminal_matrix(M, n, q, kappa)
    # Even recurrence returns C_h, so its terminal factor is I-C_h.  The odd
    # recurrence returns the already assembled 2x2 terminal matrix R.
    reduced = (
        (_identity_matrix(n) - terminal).det()
        if q % 2 == 0
        else terminal.det()
    )
    reduce_s = time.perf_counter() - t2
    delta = full - reduced
    pattern = _pattern(M, n, kappa)
    expected = expected_pattern(q, kappa)
    return {
        "q": q,
        "N": n,
        "sign": sign,
        "s": str(s),
        "kappa": kappa,
        "full_dim": kappa * n,
        "reduced_dim": n if q % 2 == 0 else 2 * n,
        "pattern_ok": pattern == expected,
        "pattern": pattern,
        "expected_pattern": expected,
        "full_vs_reduced_contains_zero": bool(delta.contains(acb(0))),
        "difference_abs_upper": str(delta.abs_upper()),
        "build_seconds": build_s,
        "full_det_seconds": full_s,
        "reduced_det_seconds": reduce_s,
    }


def run(args: argparse.Namespace) -> int:
    print(f"ENGINE_DIR={ENGINE_DIR}")
    print(f"ODD_ENGINE={ODD.__file__}")
    print(f"EVEN_ENGINE={EVEN.__file__}")
    print("IMPORT_PATH_GUARD=PASS")
    failures = 0
    for q in args.q:
        sign = args.sign_even if q % 2 == 0 else args.sign_odd
        for n in args.N:
            for s_text in args.s:
                row = check_one(q, n, parse_s(s_text), sign, args.n_head)
                ok = row["pattern_ok"] and row["full_vs_reduced_contains_zero"]
                status = "PASS" if ok else "FAIL"
                failures += int(not ok)
                print(
                    f"SCHUR q={q} parity={'even' if q % 2 == 0 else 'odd'} "
                    f"N={n} s={s_text} full_dim={row['full_dim']} "
                    f"reduced_dim={row['reduced_dim']} pattern_ok={row['pattern_ok']} "
                    f"difference_abs_upper={row['difference_abs_upper']} "
                    f"contains_zero={row['full_vs_reduced_contains_zero']} "
                    f"build_s={row['build_seconds']:.6f} "
                    f"full_det_s={row['full_det_seconds']:.6f} "
                    f"reduced_det_s={row['reduced_det_seconds']:.6f} "
                    f"status={status}"
                )

    if args.q8_speed:
        t0 = time.perf_counter()
        row = check_one(8, 16, parse_s(args.speed_s), 1, args.n_head)
        elapsed = time.perf_counter() - t0
        ok = row["pattern_ok"] and row["full_vs_reduced_contains_zero"]
        failures += int(not ok)
        print(
            f"Q8_SPEED N=16 s={args.speed_s} full_dim={row['full_dim']} "
            f"reduced_dim={row['reduced_dim']} wall_s={elapsed:.6f} "
            f"contains_zero={row['full_vs_reduced_contains_zero']} status={'PASS' if ok else 'FAIL'}"
        )
    print(f"OVERALL_STATUS={'PASS' if failures == 0 else 'FAIL'} failures={failures}")
    return int(failures != 0)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--q", nargs="+", type=int, default=[7, 8, 9, 10])
    parser.add_argument("--N", nargs="+", type=int, default=[4, 8])
    parser.add_argument("--s", nargs="+", default=["0.55+2.1i", "0.63+4.3i"])
    parser.add_argument("--n-head", type=int, default=4)
    parser.add_argument("--sign-odd", type=int, choices=(-1, 1), default=1)
    parser.add_argument("--sign-even", type=int, choices=(-1, 1), default=1)
    parser.add_argument("--q8-speed", action="store_true")
    parser.add_argument("--speed-s", default="0.4252310423737965+4.345760788321986i")
    args = parser.parse_args()
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())

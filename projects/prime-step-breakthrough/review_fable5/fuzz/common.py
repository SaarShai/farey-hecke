"""Shared helpers for adversarial prefix-balance fuzz (throwaway)."""

from __future__ import annotations

import itertools
import sys
from fractions import Fraction
from pathlib import Path
from typing import Iterable, Sequence

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "tests")]


def compositions(n: int, parts: int) -> Iterable[tuple[int, ...]]:
    """Nonnegative integer compositions of n into exactly `parts` parts."""
    if parts == 1:
        yield (n,)
        return
    for first in range(n + 1):
        for rest in compositions(n - first, parts - 1):
            yield (first, *rest)


def count_vectors(*, max_n: int, max_categories: int) -> list[tuple[int, ...]]:
    """All count vectors with sum <= max_n, length 1..max_categories (incl. zeros)."""
    out: list[tuple[int, ...]] = []
    for c in range(1, max_categories + 1):
        for n in range(0, max_n + 1):
            for vec in compositions(n, c):
                out.append(vec)
    # Deduplicate by content while keeping distinct lengths (trailing zeros matter for API)
    return out


def positive_count_vectors(*, max_n: int, max_categories: int) -> list[tuple[int, ...]]:
    """Count vectors with sum in 1..max_n, up to max_categories, at least one positive."""
    seen: set[tuple[int, ...]] = set()
    out: list[tuple[int, ...]] = []
    for c in range(1, max_categories + 1):
        for n in range(1, max_n + 1):
            for vec in compositions(n, c):
                if sum(1 for x in vec if x > 0) == 0:
                    continue
                # Drop trailing-only length variants that are identical after stripping
                # leading structure: keep all lengths as API accepts them.
                if vec in seen:
                    continue
                seen.add(vec)
                out.append(vec)
    return out


def ratio_or_none(num: Fraction, den: Fraction) -> Fraction | None:
    if den == 0:
        return None if num == 0 else Fraction(10**9)
    return Fraction(num, den)


def fmt_ratio(r: Fraction | None) -> str:
    if r is None:
        return "n/a"
    return f"{r} ({float(r):.6f})"

#!/usr/bin/env python3
"""Extreme-value statistics for Farey denominator-product gaps.

The hot loops stream the Farey denominator recursion and are JIT compiled with
numba.  Products are never stored globally.
"""

from __future__ import annotations

import argparse
import contextlib
import json
import math
import time
from io import StringIO
from pathlib import Path
from typing import Any, Dict, List

import numpy as np

try:
    from numba import njit
except Exception as exc:  # pragma: no cover
    raise SystemExit("numba is required for the compiled-speed run") from exc


S_VALUES = np.array([1e-2, 3e-3, 1e-3, 3e-4], dtype=np.float64)
S_NUM = np.array([100, 30, 10, 3], dtype=np.int64)
S_DEN = 10000

DELTA_VALUES = np.array([0.05, 0.02, 0.01, 0.005, 0.002], dtype=np.float64)
DELTA_NUM = np.array([50, 20, 10, 5, 2], dtype=np.int64)
DELTA_DEN = 1000

SKIP_EDGE_GAPS = 10
MAX_TRACKED_BAD_K = 64


@njit(cache=True)
def count_farey_gaps(q_limit: int) -> int:
    q_prev = 1
    q_cur = q_limit
    n_gaps = 0
    while True:
        n_gaps += 1
        if q_cur == 1:
            break
        k = (q_limit + q_prev) // q_cur
        q_next = k * q_cur - q_prev
        q_prev = q_cur
        q_cur = q_next
    return n_gaps


@njit(cache=True)
def finalize_ferro_segers(
    exceedances: int,
    sum_t: float,
    sum_t2: float,
    sum_tm1: float,
    sum_tm1_tm2: float,
    max_t: int,
) -> tuple:
    intervals = exceedances - 1
    if intervals <= 0:
        return math.nan, 0
    if max_t <= 2:
        denom = intervals * sum_t2
        if denom == 0.0:
            return math.nan, 1
        return 2.0 * sum_t * sum_t / denom, 1
    denom = intervals * sum_tm1_tm2
    if denom == 0.0:
        return math.nan, 2
    return 2.0 * sum_tm1 * sum_tm1 / denom, 2


@njit(cache=True)
def record_k_value(
    values: np.ndarray,
    counts: np.ndarray,
    uniques: np.ndarray,
    overflow: np.ndarray,
    row: int,
    k_value: int,
    amount: int,
) -> None:
    for u in range(uniques[row]):
        if values[row, u] == k_value:
            counts[row, u] += amount
            return
    if uniques[row] < values.shape[1]:
        u = uniques[row]
        values[row, u] = k_value
        counts[row, u] = amount
        uniques[row] += 1
    else:
        overflow[row] += amount


@njit(cache=True)
def merge_current_bad_ks(
    global_values: np.ndarray,
    global_counts: np.ndarray,
    global_uniques: np.ndarray,
    global_overflow: np.ndarray,
    current_values: np.ndarray,
    current_counts: np.ndarray,
    current_uniques: np.ndarray,
    current_overflow: np.ndarray,
    row: int,
) -> None:
    for u in range(current_uniques[row]):
        record_k_value(
            global_values,
            global_counts,
            global_uniques,
            global_overflow,
            row,
            current_values[row, u],
            current_counts[row, u],
        )
    global_overflow[row] += current_overflow[row]


@njit(cache=True)
def reset_current_bad_ks(
    current_values: np.ndarray,
    current_counts: np.ndarray,
    current_uniques: np.ndarray,
    current_overflow: np.ndarray,
    row: int,
) -> None:
    current_uniques[row] = 0
    current_overflow[row] = 0


@njit(cache=True)
def close_large_cluster(
    row: int,
    size: int,
    first_p: int,
    second_p: int,
    hist: np.ndarray,
    size2_count: np.ndarray,
    size2_min: np.ndarray,
    size2_max: np.ndarray,
) -> None:
    if size == 1:
        hist[row, 0] += 1
    elif size == 2:
        hist[row, 1] += 1
        ratio = float(second_p) / float(first_p)
        size2_count[row] += 1
        if ratio < size2_min[row]:
            size2_min[row] = ratio
        if ratio > size2_max[row]:
            size2_max[row] = ratio
    elif size == 3:
        hist[row, 2] += 1
    else:
        hist[row, 3] += 1


@njit(cache=True)
def close_small_cluster(
    row: int,
    size: int,
    ap_ok: bool,
    hist: np.ndarray,
    ge_counts: np.ndarray,
    ap_total_ge3: np.ndarray,
    ap_good_ge3: np.ndarray,
    ap_bad_ge3: np.ndarray,
    global_bad_k_values: np.ndarray,
    global_bad_k_counts: np.ndarray,
    global_bad_k_uniques: np.ndarray,
    global_bad_k_overflow: np.ndarray,
    current_bad_k_values: np.ndarray,
    current_bad_k_counts: np.ndarray,
    current_bad_k_uniques: np.ndarray,
    current_bad_k_overflow: np.ndarray,
) -> None:
    if size <= 10:
        hist[row, size - 1] += 1
    for n in range(1, 51):
        if size >= n:
            ge_counts[row, n] += 1
    if size >= 3:
        ap_total_ge3[row] += 1
        if ap_ok:
            ap_good_ge3[row] += 1
        else:
            ap_bad_ge3[row] += 1
            merge_current_bad_ks(
                global_bad_k_values,
                global_bad_k_counts,
                global_bad_k_uniques,
                global_bad_k_overflow,
                current_bad_k_values,
                current_bad_k_counts,
                current_bad_k_uniques,
                current_bad_k_overflow,
                row,
            )


@njit(cache=True)
def farey_stats_pass(
    q_limit: int,
    s_num: np.ndarray,
    s_den: int,
    delta_num: np.ndarray,
    delta_den: int,
    n_total_gaps: int,
    skip_edges: int,
):
    n_s = s_num.size
    n_d = delta_num.size
    q2 = q_limit * q_limit

    large_ex = np.zeros(n_s, np.int64)
    large_clusters = np.zeros(n_s, np.int64)
    large_hist = np.zeros((n_s, 4), np.int64)
    large_current = np.zeros(n_s, np.int64)
    large_in = np.zeros(n_s, np.bool_)
    large_first_p = np.zeros(n_s, np.int64)
    large_second_p = np.zeros(n_s, np.int64)
    large_size2_count = np.zeros(n_s, np.int64)
    large_size2_min = np.empty(n_s, np.float64)
    large_size2_max = np.empty(n_s, np.float64)
    for i in range(n_s):
        large_size2_min[i] = math.inf
        large_size2_max[i] = -math.inf

    small_ex = np.zeros(n_d, np.int64)
    small_clusters = np.zeros(n_d, np.int64)
    small_hist = np.zeros((n_d, 10), np.int64)
    small_ge_counts = np.zeros((n_d, 51), np.int64)
    small_current = np.zeros(n_d, np.int64)
    small_in = np.zeros(n_d, np.bool_)
    small_first_diff = np.zeros(n_d, np.int64)
    small_ap_ok = np.ones(n_d, np.bool_)
    small_ap_total_ge3 = np.zeros(n_d, np.int64)
    small_ap_good_ge3 = np.zeros(n_d, np.int64)
    small_ap_bad_ge3 = np.zeros(n_d, np.int64)

    current_bad_k_values = np.zeros((n_d, MAX_TRACKED_BAD_K), np.int64)
    current_bad_k_counts = np.zeros((n_d, MAX_TRACKED_BAD_K), np.int64)
    current_bad_k_uniques = np.zeros(n_d, np.int64)
    current_bad_k_overflow = np.zeros(n_d, np.int64)
    global_bad_k_values = np.zeros((n_d, MAX_TRACKED_BAD_K), np.int64)
    global_bad_k_counts = np.zeros((n_d, MAX_TRACKED_BAD_K), np.int64)
    global_bad_k_uniques = np.zeros(n_d, np.int64)
    global_bad_k_overflow = np.zeros(n_d, np.int64)

    large_sum_t = np.zeros(n_s, np.float64)
    large_sum_t2 = np.zeros(n_s, np.float64)
    large_sum_tm1 = np.zeros(n_s, np.float64)
    large_sum_tm1_tm2 = np.zeros(n_s, np.float64)
    large_max_t = np.zeros(n_s, np.int64)
    large_last_ex_idx = np.full(n_s, -1, np.int64)

    small_sum_t = np.zeros(n_d, np.float64)
    small_sum_t2 = np.zeros(n_d, np.float64)
    small_sum_tm1 = np.zeros(n_d, np.float64)
    small_sum_tm1_tm2 = np.zeros(n_d, np.float64)
    small_max_t = np.zeros(n_d, np.int64)
    small_last_ex_idx = np.full(n_d, -1, np.int64)

    analyzed_gaps = 0
    q_prev = 1
    q_cur = q_limit
    gap_idx = 0
    last_k = 0

    while True:
        p = q_prev * q_cur
        include = gap_idx >= skip_edges and gap_idx < n_total_gaps - skip_edges

        if include:
            analyzed_gaps += 1
            scaled_large_p = p * s_den
            scaled_small_p = p * delta_den

            for i in range(n_s):
                is_ex = scaled_large_p < s_num[i] * q2
                if is_ex:
                    large_ex[i] += 1
                    if large_last_ex_idx[i] >= 0:
                        t = gap_idx - large_last_ex_idx[i]
                        large_sum_t[i] += t
                        large_sum_t2[i] += t * t
                        tm1 = t - 1
                        large_sum_tm1[i] += tm1
                        large_sum_tm1_tm2[i] += tm1 * (t - 2)
                        if t > large_max_t[i]:
                            large_max_t[i] = t
                    large_last_ex_idx[i] = gap_idx

                    if large_in[i]:
                        large_current[i] += 1
                        if large_current[i] == 2:
                            large_second_p[i] = p
                    else:
                        large_in[i] = True
                        large_clusters[i] += 1
                        large_current[i] = 1
                        large_first_p[i] = p
                        large_second_p[i] = 0
                else:
                    if large_in[i]:
                        close_large_cluster(
                            i,
                            large_current[i],
                            large_first_p[i],
                            large_second_p[i],
                            large_hist,
                            large_size2_count,
                            large_size2_min,
                            large_size2_max,
                        )
                        large_in[i] = False
                        large_current[i] = 0

            for i in range(n_d):
                is_ex = scaled_small_p > (delta_den - delta_num[i]) * q2
                if is_ex:
                    small_ex[i] += 1
                    if small_last_ex_idx[i] >= 0:
                        t = gap_idx - small_last_ex_idx[i]
                        small_sum_t[i] += t
                        small_sum_t2[i] += t * t
                        tm1 = t - 1
                        small_sum_tm1[i] += tm1
                        small_sum_tm1_tm2[i] += tm1 * (t - 2)
                        if t > small_max_t[i]:
                            small_max_t[i] = t
                    small_last_ex_idx[i] = gap_idx

                    diff = q_cur - q_prev
                    if small_in[i]:
                        small_current[i] += 1
                        if diff != small_first_diff[i]:
                            small_ap_ok[i] = False
                            record_k_value(
                                current_bad_k_values,
                                current_bad_k_counts,
                                current_bad_k_uniques,
                                current_bad_k_overflow,
                                i,
                                last_k,
                                1,
                            )
                    else:
                        small_in[i] = True
                        small_clusters[i] += 1
                        small_current[i] = 1
                        small_first_diff[i] = diff
                        small_ap_ok[i] = True
                        reset_current_bad_ks(
                            current_bad_k_values,
                            current_bad_k_counts,
                            current_bad_k_uniques,
                            current_bad_k_overflow,
                            i,
                        )
                else:
                    if small_in[i]:
                        close_small_cluster(
                            i,
                            small_current[i],
                            small_ap_ok[i],
                            small_hist,
                            small_ge_counts,
                            small_ap_total_ge3,
                            small_ap_good_ge3,
                            small_ap_bad_ge3,
                            global_bad_k_values,
                            global_bad_k_counts,
                            global_bad_k_uniques,
                            global_bad_k_overflow,
                            current_bad_k_values,
                            current_bad_k_counts,
                            current_bad_k_uniques,
                            current_bad_k_overflow,
                        )
                        small_in[i] = False
                        small_current[i] = 0

        if q_cur == 1:
            break

        k = (q_limit + q_prev) // q_cur
        q_next = k * q_cur - q_prev
        q_prev = q_cur
        q_cur = q_next
        gap_idx += 1
        last_k = k

    for i in range(n_s):
        if large_in[i]:
            close_large_cluster(
                i,
                large_current[i],
                large_first_p[i],
                large_second_p[i],
                large_hist,
                large_size2_count,
                large_size2_min,
                large_size2_max,
            )

    for i in range(n_d):
        if small_in[i]:
            close_small_cluster(
                i,
                small_current[i],
                small_ap_ok[i],
                small_hist,
                small_ge_counts,
                small_ap_total_ge3,
                small_ap_good_ge3,
                small_ap_bad_ge3,
                global_bad_k_values,
                global_bad_k_counts,
                global_bad_k_uniques,
                global_bad_k_overflow,
                current_bad_k_values,
                current_bad_k_counts,
                current_bad_k_uniques,
                current_bad_k_overflow,
            )

    large_theta_fs = np.empty(n_s, np.float64)
    large_fs_branch = np.zeros(n_s, np.int64)
    for i in range(n_s):
        theta, branch = finalize_ferro_segers(
            large_ex[i],
            large_sum_t[i],
            large_sum_t2[i],
            large_sum_tm1[i],
            large_sum_tm1_tm2[i],
            large_max_t[i],
        )
        large_theta_fs[i] = theta
        large_fs_branch[i] = branch
        if large_size2_count[i] == 0:
            large_size2_min[i] = math.nan
            large_size2_max[i] = math.nan

    small_theta_fs = np.empty(n_d, np.float64)
    small_fs_branch = np.zeros(n_d, np.int64)
    for i in range(n_d):
        theta, branch = finalize_ferro_segers(
            small_ex[i],
            small_sum_t[i],
            small_sum_t2[i],
            small_sum_tm1[i],
            small_sum_tm1_tm2[i],
            small_max_t[i],
        )
        small_theta_fs[i] = theta
        small_fs_branch[i] = branch

    return (
        analyzed_gaps,
        large_ex,
        large_clusters,
        large_hist,
        large_theta_fs,
        large_fs_branch,
        large_max_t,
        large_size2_count,
        large_size2_min,
        large_size2_max,
        small_ex,
        small_clusters,
        small_hist,
        small_ge_counts,
        small_theta_fs,
        small_fs_branch,
        small_max_t,
        small_ap_total_ge3,
        small_ap_good_ge3,
        small_ap_bad_ge3,
        global_bad_k_values,
        global_bad_k_counts,
        global_bad_k_uniques,
        global_bad_k_overflow,
    )


@njit(cache=True)
def fill_large_size2_ratios(
    q_limit: int,
    s_num: np.ndarray,
    s_den: int,
    n_total_gaps: int,
    skip_edges: int,
    offsets: np.ndarray,
    ratio_values: np.ndarray,
) -> np.ndarray:
    n_s = s_num.size
    q2 = q_limit * q_limit
    fill_counts = np.zeros(n_s, np.int64)
    current = np.zeros(n_s, np.int64)
    in_cluster = np.zeros(n_s, np.bool_)
    first_p = np.zeros(n_s, np.int64)
    second_p = np.zeros(n_s, np.int64)

    q_prev = 1
    q_cur = q_limit
    gap_idx = 0

    while True:
        p = q_prev * q_cur
        include = gap_idx >= skip_edges and gap_idx < n_total_gaps - skip_edges
        if include:
            scaled_p = p * s_den
            for i in range(n_s):
                is_ex = scaled_p < s_num[i] * q2
                if is_ex:
                    if in_cluster[i]:
                        current[i] += 1
                        if current[i] == 2:
                            second_p[i] = p
                    else:
                        in_cluster[i] = True
                        current[i] = 1
                        first_p[i] = p
                        second_p[i] = 0
                else:
                    if in_cluster[i]:
                        if current[i] == 2:
                            out_idx = offsets[i] + fill_counts[i]
                            ratio_values[out_idx] = float(second_p[i]) / float(first_p[i])
                            fill_counts[i] += 1
                        in_cluster[i] = False
                        current[i] = 0

        if q_cur == 1:
            break

        k = (q_limit + q_prev) // q_cur
        q_next = k * q_cur - q_prev
        q_prev = q_cur
        q_cur = q_next
        gap_idx += 1

    for i in range(n_s):
        if in_cluster[i] and current[i] == 2:
            out_idx = offsets[i] + fill_counts[i]
            ratio_values[out_idx] = float(second_p[i]) / float(first_p[i])
            fill_counts[i] += 1

    return fill_counts


def linreg_with_intercept(x: np.ndarray, y: np.ndarray) -> Dict[str, float]:
    mask = np.isfinite(x) & np.isfinite(y)
    x = x[mask]
    y = y[mask]
    if x.size < 2:
        return {"slope": math.nan, "intercept": math.nan, "r2": math.nan, "n": int(x.size)}
    xm = float(x.mean())
    ym = float(y.mean())
    ssx = float(np.sum((x - xm) ** 2))
    if ssx == 0.0:
        return {"slope": math.nan, "intercept": math.nan, "r2": math.nan, "n": int(x.size)}
    slope = float(np.sum((x - xm) * (y - ym)) / ssx)
    intercept = ym - slope * xm
    yhat = intercept + slope * x
    sst = float(np.sum((y - ym) ** 2))
    sse = float(np.sum((y - yhat) ** 2))
    r2 = math.nan if sst == 0.0 else 1.0 - sse / sst
    return {"slope": slope, "intercept": intercept, "r2": r2, "n": int(x.size)}


def linreg_through_origin(x: np.ndarray, y: np.ndarray) -> Dict[str, float]:
    mask = np.isfinite(x) & np.isfinite(y)
    x = x[mask]
    y = y[mask]
    if x.size < 1:
        return {"c": math.nan, "r2": math.nan, "n": 0}
    denom = float(np.sum(x * x))
    if denom == 0.0:
        return {"c": math.nan, "r2": math.nan, "n": int(x.size)}
    c = float(np.sum(x * y) / denom)
    yhat = c * x
    ym = float(y.mean())
    sst = float(np.sum((y - ym) ** 2))
    sse = float(np.sum((y - yhat) ** 2))
    r2 = math.nan if sst == 0.0 else 1.0 - sse / sst
    return {"c": c, "r2": r2, "n": int(x.size)}


def fs_branch_name(branch: int) -> str:
    if branch == 1:
        return "max_T_le_2"
    if branch == 2:
        return "alternative"
    return "insufficient_intervals"


def analyze_q(q_limit: int) -> Dict[str, Any]:
    t0 = time.perf_counter()
    n_total = int(count_farey_gaps(q_limit))
    t_count = time.perf_counter()

    stats = farey_stats_pass(
        q_limit,
        S_NUM,
        S_DEN,
        DELTA_NUM,
        DELTA_DEN,
        n_total,
        SKIP_EDGE_GAPS,
    )
    t_stats = time.perf_counter()

    (
        analyzed_gaps,
        large_ex,
        large_clusters,
        large_hist,
        large_theta_fs,
        large_fs_branch,
        large_max_t,
        large_size2_count,
        large_size2_min,
        large_size2_max,
        small_ex,
        small_clusters,
        small_hist,
        small_ge_counts,
        small_theta_fs,
        small_fs_branch,
        small_max_t,
        small_ap_total_ge3,
        small_ap_good_ge3,
        small_ap_bad_ge3,
        global_bad_k_values,
        global_bad_k_counts,
        global_bad_k_uniques,
        global_bad_k_overflow,
    ) = stats

    counts = np.asarray(large_size2_count, dtype=np.int64)
    offsets = np.zeros(counts.size + 1, dtype=np.int64)
    offsets[1:] = np.cumsum(counts)
    ratio_values = np.empty(int(offsets[-1]), dtype=np.float64)
    filled = fill_large_size2_ratios(
        q_limit,
        S_NUM,
        S_DEN,
        n_total,
        SKIP_EDGE_GAPS,
        offsets,
        ratio_values,
    )
    if not np.array_equal(filled, counts):
        raise RuntimeError(f"size-2 ratio fill mismatch for Q={q_limit}: {filled} vs {counts}")
    t_ratios = time.perf_counter()

    ratio_medians = np.empty(counts.size, dtype=np.float64)
    for i, count in enumerate(counts):
        if count == 0:
            ratio_medians[i] = math.nan
        else:
            vals = ratio_values[offsets[i] : offsets[i + 1]]
            vals.sort()
            ratio_medians[i] = float(np.median(vals))
    t_sort = time.perf_counter()

    task1: List[Dict[str, Any]] = []
    for i, s in enumerate(S_VALUES):
        ex = int(large_ex[i])
        cl = int(large_clusters[i])
        task1.append(
            {
                "s": float(s),
                "exceedances": ex,
                "clusters": cl,
                "theta_runs": float(cl / ex) if ex else math.nan,
                "theta_FS": float(large_theta_fs[i]),
                "ferro_segers_branch": fs_branch_name(int(large_fs_branch[i])),
                "max_interexceedance_T": int(large_max_t[i]),
                "cluster_size_hist": {
                    "1": int(large_hist[i, 0]),
                    "2": int(large_hist[i, 1]),
                    "3": int(large_hist[i, 2]),
                    ">=4": int(large_hist[i, 3]),
                },
                "size2_ratio": {
                    "count": int(large_size2_count[i]),
                    "min": float(large_size2_min[i]),
                    "median": float(ratio_medians[i]),
                    "max": float(large_size2_max[i]),
                },
            }
        )

    task2: List[Dict[str, Any]] = []
    theta_x = []
    theta_y = []
    for i, delta in enumerate(DELTA_VALUES):
        ex = int(small_ex[i])
        cl = int(small_clusters[i])
        theta_runs = float(cl / ex) if ex else math.nan
        ge = small_ge_counts[i]
        ns = np.arange(2, 51, dtype=np.float64)
        tail_counts = ge[2:51].astype(np.float64)
        valid = tail_counts > 0
        tail_fit = linreg_with_intercept(np.log(ns[valid]), np.log(tail_counts[valid]))
        ap_total = int(small_ap_total_ge3[i])
        ap_good = int(small_ap_good_ge3[i])
        violators = []
        for u in range(int(global_bad_k_uniques[i])):
            violators.append(
                {
                    "k": int(global_bad_k_values[i, u]),
                    "transition_occurrences": int(global_bad_k_counts[i, u]),
                }
            )
        theta_x.append(1.0 / math.log(1.0 / float(delta)))
        theta_y.append(theta_runs)
        task2.append(
            {
                "delta": float(delta),
                "exceedances": ex,
                "clusters": cl,
                "theta_runs": theta_runs,
                "theta_FS": float(small_theta_fs[i]),
                "ferro_segers_branch": fs_branch_name(int(small_fs_branch[i])),
                "max_interexceedance_T": int(small_max_t[i]),
                "cluster_size_counts_1_to_10": {
                    str(n): int(small_hist[i, n - 1]) for n in range(1, 11)
                },
                "tail_slope_fit_log_ge_n_vs_log_n_n_2_50": tail_fit,
                "ap_signature_size_ge3": {
                    "clusters_size_ge3": ap_total,
                    "constant_second_difference": ap_good,
                    "fraction": float(ap_good / ap_total) if ap_total else math.nan,
                    "violator_clusters": int(small_ap_bad_ge3[i]),
                    "violator_k_values": violators,
                    "violator_k_overflow_transition_occurrences": int(global_bad_k_overflow[i]),
                },
            }
        )

    theta_fit = linreg_through_origin(np.asarray(theta_x), np.asarray(theta_y))
    theta_fit["model"] = "theta_runs = c / log(1/delta), intercept fixed at 0"

    invariants = check_invariants(q_limit, n_total, int(analyzed_gaps), task1, task2)
    return {
        "Q": q_limit,
        "total_gaps_including_edges": n_total,
        "analyzed_gaps_after_skip": int(analyzed_gaps),
        "N_asymptotic_3Q2_over_pi2": float(3.0 * q_limit * q_limit / (math.pi * math.pi)),
        "runtime_seconds": {
            "count_total_gaps": t_count - t0,
            "stats_pass": t_stats - t_count,
            "ratio_fill_pass": t_ratios - t_stats,
            "ratio_sort": t_sort - t_ratios,
            "total": t_sort - t0,
        },
        "task1_large_gap_extremes": task1,
        "task2_small_gap_extremes": task2,
        "task2_theta_runs_vs_delta_fit": theta_fit,
        "invariants": invariants,
    }


def check_invariants(
    q_limit: int,
    n_total: int,
    analyzed_gaps: int,
    task1: List[Dict[str, Any]],
    task2: List[Dict[str, Any]],
) -> Dict[str, Any]:
    checks: Dict[str, Any] = {}
    checks["analyzed_gaps_equals_total_minus_20"] = analyzed_gaps == n_total - 2 * SKIP_EDGE_GAPS
    checks["N_relative_error_vs_3Q2_pi2"] = abs(n_total - 3.0 * q_limit * q_limit / (math.pi * math.pi)) / n_total

    large_ok = True
    for row in task1:
        hist = row["cluster_size_hist"]
        if hist["1"] + hist["2"] + hist["3"] + hist[">=4"] != row["clusters"]:
            large_ok = False
        weighted_lower_bound = hist["1"] + 2 * hist["2"] + 3 * hist["3"] + 4 * hist[">=4"]
        if weighted_lower_bound > row["exceedances"]:
            large_ok = False
        if row["size2_ratio"]["count"] != hist["2"]:
            large_ok = False
        if not (math.isnan(row["theta_runs"]) or (0.0 < row["theta_runs"] <= 1.0)):
            large_ok = False
        if not (math.isnan(row["theta_FS"]) or row["theta_FS"] > 0.0):
            large_ok = False
    checks["task1_cluster_histograms_reconcile"] = large_ok

    small_ok = True
    for row in task2:
        counts = row["cluster_size_counts_1_to_10"]
        if sum(counts[str(n)] for n in range(1, 11)) > row["clusters"]:
            small_ok = False
        ap = row["ap_signature_size_ge3"]
        if ap["constant_second_difference"] + ap["violator_clusters"] != ap["clusters_size_ge3"]:
            small_ok = False
        if not (math.isnan(row["theta_runs"]) or (0.0 < row["theta_runs"] <= 1.0)):
            small_ok = False
        if not (math.isnan(row["theta_FS"]) or row["theta_FS"] > 0.0):
            small_ok = False
    checks["task2_cluster_counts_reconcile"] = small_ok
    checks["all_passed"] = bool(all(v for v in checks.values() if isinstance(v, bool)))
    return checks


def format_float(x: float, ndigits: int = 12) -> str:
    if x is None or math.isnan(x):
        return "nan"
    return f"{x:.{ndigits}g}"


def print_summary(results: Dict[str, Any]) -> None:
    print("# EVT Farey gaps summary")
    print(json.dumps(results["metadata"], indent=2, sort_keys=True))
    for qres in results["runs"]:
        q = qres["Q"]
        print(f"\n## Q={q}")
        print(
            "gaps_total="
            f"{qres['total_gaps_including_edges']} analyzed={qres['analyzed_gaps_after_skip']} "
            f"asymptotic={format_float(qres['N_asymptotic_3Q2_over_pi2'])} "
            f"runtime_total_s={format_float(qres['runtime_seconds']['total'])}"
        )

        print("Task 1 theta")
        print("s\texceedances\tclusters\ttheta_runs\ttheta_FS\tFS_branch")
        for row in qres["task1_large_gap_extremes"]:
            print(
                f"{row['s']:g}\t{row['exceedances']}\t{row['clusters']}\t"
                f"{format_float(row['theta_runs'])}\t{format_float(row['theta_FS'])}\t"
                f"{row['ferro_segers_branch']}"
            )

        print("Task 1 cluster hist and size-2 ratios")
        print("s\thist_1\thist_2\thist_3\thist_ge4\tratio_min\tratio_median\tratio_max")
        for row in qres["task1_large_gap_extremes"]:
            hist = row["cluster_size_hist"]
            ratio = row["size2_ratio"]
            print(
                f"{row['s']:g}\t{hist['1']}\t{hist['2']}\t{hist['3']}\t{hist['>=4']}\t"
                f"{format_float(ratio['min'])}\t{format_float(ratio['median'])}\t{format_float(ratio['max'])}"
            )

        print("Task 2 theta")
        print("delta\texceedances\tclusters\ttheta_runs\ttheta_FS\tFS_branch\ttail_slope\tAP_fraction")
        for row in qres["task2_small_gap_extremes"]:
            ap = row["ap_signature_size_ge3"]
            print(
                f"{row['delta']:g}\t{row['exceedances']}\t{row['clusters']}\t"
                f"{format_float(row['theta_runs'])}\t{format_float(row['theta_FS'])}\t"
                f"{row['ferro_segers_branch']}\t"
                f"{format_float(row['tail_slope_fit_log_ge_n_vs_log_n_n_2_50']['slope'])}\t"
                f"{format_float(ap['fraction'])}"
            )

        print("Task 2 cluster counts 1..10")
        print("delta\t" + "\t".join(str(n) for n in range(1, 11)))
        for row in qres["task2_small_gap_extremes"]:
            counts = row["cluster_size_counts_1_to_10"]
            print(f"{row['delta']:g}\t" + "\t".join(str(counts[str(n)]) for n in range(1, 11)))

        fit = qres["task2_theta_runs_vs_delta_fit"]
        print(
            "Task 2 theta_runs_vs_delta_fit: "
            f"c={format_float(fit['c'])} R2={format_float(fit['r2'])} n={fit['n']}"
        )
        print("Invariants:", json.dumps(qres["invariants"], sort_keys=True))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", nargs="*", type=int, default=[10000, 30000])
    parser.add_argument("--out", type=Path, default=Path("results.json"))
    parser.add_argument("--log", type=Path, default=Path("summary.log"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    metadata = {
        "method": "streaming Farey denominator recursion; numba JIT compiled hot loops",
        "s_thresholds": [float(x) for x in S_VALUES],
        "deltas": [float(x) for x in DELTA_VALUES],
        "large_threshold_integer_rule": "P * 10000 < s_num * Q^2 for s_num=[100,30,10,3]",
        "small_threshold_integer_rule": "P * 1000 > (1000-delta_num) * Q^2 for delta_num=[50,20,10,5,2]",
        "skip_first_and_last_gaps": SKIP_EDGE_GAPS,
        "ferro_segers_formula": {
            "branch_rule": "if max(T_j) <= 2 use 2*(sum T_j)^2 / ((N-1)*sum T_j^2), else use 2*(sum(T_j-1))^2 / ((N-1)*sum((T_j-1)*(T_j-2)))",
            "N": "number of exceedances; there are N-1 interexceedance intervals",
            "T_j": "interexceedance times in Farey gap-index units after dropping first and last 10 gaps",
        },
    }
    results = {"metadata": metadata, "runs": []}

    # Pay compilation cost before timing the requested Q values.
    warm_n = count_farey_gaps(8)
    warm_stats = farey_stats_pass(8, S_NUM, S_DEN, DELTA_NUM, DELTA_DEN, warm_n, 0)
    warm_counts = np.asarray(warm_stats[7], dtype=np.int64)
    warm_offsets = np.zeros(warm_counts.size + 1, dtype=np.int64)
    warm_offsets[1:] = np.cumsum(warm_counts)
    warm_ratios = np.empty(int(warm_offsets[-1]), dtype=np.float64)
    fill_large_size2_ratios(8, S_NUM, S_DEN, warm_n, 0, warm_offsets, warm_ratios)

    for q in args.q:
        print(f"Running Q={q}", flush=True)
        results["runs"].append(analyze_q(q))
        args.out.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")

    args.out.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
    buf = StringIO()
    with contextlib.redirect_stdout(buf):
        print_summary(results)
    summary = buf.getvalue()
    args.log.write_text(summary)
    print(summary, end="")


if __name__ == "__main__":
    main()

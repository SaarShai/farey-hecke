#!/usr/bin/env python3
"""Reproducibly compute the Path-B B1/B2 elliptic-curve C1 control matrix.

The fixed Path-B observable is deliberately kept identical to
``path_b_20forms.py``: rho=1+i*gamma, K=10000, mu(p)=-a_p, mu(p^2)=p,
and 200 positive zero ordinates.  This program owns only the new B1/B2
artifacts; it never edits the historical 20-form CSV.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import mpmath as mp


SHARED = Path(__file__).resolve().parents[1]
DEFAULT_DATA = SHARED / "data"
DEFAULT_MANIFEST = DEFAULT_DATA / "PATH_B_B1_B2_MANIFEST.csv"
DEFAULT_CSV = DEFAULT_DATA / "PATH_B_B1_B2_CONTROLS.csv"
EULER_GAMMA = mp.mpf("0.5772156649015328606065120900824024310421593359399235")
BANDS = {
    "B1": {"lo": 350, "hi": 650, "targets": (("389a1", 2), ("433a1", 2), ("446d1", 2), ("571b1", 2)), "needs": {0: 3, 1: 3}},
    "B2": {"lo": 4500, "hi": 5600, "targets": (("5077a1", 3),), "needs": {0: 2, 1: 2, 2: 2}},
}
MANIFEST_FIELDS = ("label", "band", "role", "rank", "weight", "conductor", "nearest_target_distance")
OUTPUT_FIELDS = ("label", "band", "rank", "weight", "conductor", "K", "precision", "N_zeros", "Tmax", "E_C1", "E_C1_sq", "error", "provenance_hash")


def gp_eval(script: str, timeout: int = 7200) -> str:
    if not shutil.which("gp"):
        raise RuntimeError("gp is not on PATH")
    proc = subprocess.run(["gp", "-q", "--default", "parisizemax=4G"], input=script,
                          capture_output=True, text=True, timeout=timeout)
    if proc.returncode:
        raise RuntimeError(proc.stderr.strip() or f"gp exited {proc.returncode}")
    return proc.stdout


def require_int(text: str, what: str) -> int:
    try:
        return int(text)
    except ValueError as exc:
        raise ValueError(f"invalid {what}: {text!r}") from exc


def parse_manifest(path: Path) -> list[dict[str, Any]]:
    with path.open(newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None or not set(MANIFEST_FIELDS[:-1]).issubset(reader.fieldnames):
            raise ValueError(f"malformed curves manifest {path}: expected {', '.join(MANIFEST_FIELDS[:-1])}")
        rows: list[dict[str, Any]] = []
        for line, raw in enumerate(reader, 2):
            label = (raw.get("label") or "").strip()
            band = (raw.get("band") or "").strip()
            role = (raw.get("role") or "").strip()
            if not label or band not in BANDS or role not in {"target", "control"}:
                raise ValueError(f"malformed curves manifest {path}:{line}")
            rows.append({"label": label, "band": band, "role": role,
                         "rank": require_int(raw.get("rank", ""), "rank"),
                         "weight": require_int(raw.get("weight", ""), "weight"),
                         "conductor": require_int(raw.get("conductor", ""), "conductor"),
                         "nearest_target_distance": require_int(raw.get("nearest_target_distance", "0"), "nearest_target_distance")})
    labels = [row["label"] for row in rows]
    if len(labels) != len(set(labels)):
        raise ValueError(f"malformed curves manifest {path}: duplicate label")
    return rows


def discover_controls(precision: int) -> list[dict[str, Any]]:
    """Discover only the specified bands, then use the predeclared tie break."""
    lines = [f"default(realprecision,{precision});"]
    for band, spec in BANDS.items():
        lines.extend([
            f'print("BAND,{band}");',
            f'for(N={spec["lo"]},{spec["hi"]},C=ellsearch(N);for(i=1,#C,lab=C[i][1];E=ellinit(lab);r=ellanalyticrank(E)[1];if(r<={max(spec["needs"])},print(lab,",",r,",",ellglobalred(E)[1]))))',
        ])
    output = gp_eval("\n".join(lines))
    found: dict[str, list[tuple[str, int, int]]] = {band: [] for band in BANDS}
    band = ""
    for line in output.splitlines():
        text = line.strip()
        if text.startswith("BAND,"):
            band = text.split(",", 1)[1]
            continue
        parts = [part.strip() for part in text.split(",")]
        if band in found and len(parts) == 3:
            try:
                found[band].append((parts[0], int(parts[1]), int(parts[2])))
            except ValueError:
                pass
    rows: list[dict[str, Any]] = []
    for band, spec in BANDS.items():
        targets: list[int] = []
        for label, rank in spec["targets"]:
            # Resolve conductor through elldata rather than trust an old table.
            conductor = next((n for lab, _, n in found[band] if lab == label), None)
            if conductor is None:
                conductor = int(gp_eval(f'E=ellinit("{label}"); print(ellglobalred(E)[1]);').strip())
            rows.append({"label": label, "band": band, "role": "target", "rank": rank,
                         "weight": 2, "conductor": conductor, "nearest_target_distance": 0})
            targets.append(conductor)
        for rank, count in spec["needs"].items():
            choices = [item for item in found[band] if item[1] == rank]
            choices.sort(key=lambda item: (min(abs(item[2] - target) for target in targets), item[2], item[0]))
            selected: list[tuple[str, int, int]] = []
            seen_classes: set[str] = set()
            for choice in choices:
                curve_class = isogeny_class(choice[0])
                if curve_class in seen_classes:
                    continue
                selected.append(choice)
                seen_classes.add(curve_class)
                if len(selected) == count:
                    break
            if len(selected) < count:
                raise RuntimeError(f"{band}: found only {len(selected)}/{count} distinct-isogeny rank-{rank} controls")
            for label, selected_rank, conductor in selected:
                rows.append({"label": label, "band": band, "role": "control", "rank": selected_rank,
                             "weight": 2, "conductor": conductor,
                             "nearest_target_distance": min(abs(conductor - target) for target in targets)})
    return sorted(rows, key=lambda r: (r["band"], r["role"] != "target", r["rank"], r["conductor"], r["label"]))


def isogeny_class(label: str) -> str:
    """Cremona class, e.g. 446c1 and 446c2 both map to 446c."""
    match = re.fullmatch(r"(\d+[a-z]+)\d+", label)
    if not match:
        raise ValueError(f"malformed Cremona label {label!r}")
    return match.group(1)


def write_manifest(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=MANIFEST_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def sieve_primes(nmax: int) -> list[int]:
    sieve = bytearray(b"\x01") * (nmax + 1)
    sieve[:2] = b"\x00\x00"
    for i in range(2, math.isqrt(nmax) + 1):
        if sieve[i]:
            sieve[i * i::i] = b"\x00" * len(range(i * i, nmax + 1, i))
    return [i for i in range(2, nmax + 1) if sieve[i]]


def build_mu_ec(ap: dict[int, int], nmax: int) -> list[mp.mpf]:
    """Euler reciprocal coefficients: mu(p)=-a_p, mu(p^2)=p, higher=0."""
    mu = [mp.mpf(0)] * (nmax + 1)
    mu[1] = mp.mpf(1)
    for p in sieve_primes(nmax):
        if p not in ap:
            raise ValueError(f"missing a_p for prime {p}")
        for pk, value in ((p, -ap[p]), (p * p, p)):
            if pk > nmax or not value:
                continue
            for m in range(1, nmax // pk + 1):
                if m % p and mu[m]:
                    mu[m * pk] = mu[m] * value
    return mu


def gp_curve_payload(label: str, k: int, zeros: int, tmax: int, precision: int) -> dict[str, Any]:
    script = f'''default(realprecision,{precision});
E=ellinit("{label}");
print("META,",ellanalyticrank(E)[1],",",ellglobalred(E)[1]);
Z=lfunzeros(E,[1e-6,{tmax}]); n=min(#Z,{zeros});
for(i=1,n,print("ZERO,",i,",",Z[i]));
forprime(p=2,{k},print("AP,",p,",",ellap(E,p)));
for(i=1,n,v=lfun(E,1+I*Z[i],1);print("LPRIME,",i,",",real(v),",",imag(v)));'''
    meta: tuple[int, int] | None = None
    z: list[str] = []
    ap: dict[int, int] = {}
    lp: list[tuple[str, str]] = []
    for line in gp_eval(script).splitlines():
        parts = [part.strip() for part in line.split(",")]
        if not parts:
            continue
        if parts[0] == "META" and len(parts) == 3:
            meta = (int(parts[1]), int(parts[2]))
        elif parts[0] == "ZERO" and len(parts) == 3:
            z.append(parts[2])
        elif parts[0] == "AP" and len(parts) == 3:
            ap[int(parts[1])] = int(parts[2])
        elif parts[0] == "LPRIME" and len(parts) == 4:
            lp.append((parts[2], parts[3]))
    if meta is None:
        raise RuntimeError(f"{label}: PARI emitted no metadata")
    if len(z) != zeros or len(lp) != zeros:
        raise RuntimeError(f"{label}: need exactly {zeros} zeros, got zeros={len(z)} lprimes={len(lp)} at Tmax={tmax}")
    return {"rank": meta[0], "conductor": meta[1], "zeros": z, "ap": ap, "lprimes": lp}


def canonical_hash(value: Any) -> str:
    # JSON has string object keys.  Canonicalize *after* that conversion so a
    # fresh Python dict (integer a_p keys) hashes identically after raw JSON
    # is written and reloaded (where those keys are strings).
    json_value = json.loads(json.dumps(value, separators=(",", ":"), ensure_ascii=True))
    text = json.dumps(json_value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(text.encode()).hexdigest()


def compute_row(spec: dict[str, Any], k: int, zeros: int, tmax: int, precision: int, output_dir: Path) -> dict[str, Any]:
    payload = gp_curve_payload(spec["label"], k, zeros, tmax, precision)
    if payload["rank"] != spec["rank"] or payload["conductor"] != spec["conductor"]:
        raise RuntimeError(f"{spec['label']}: manifest metadata disagrees with PARI (rank={payload['rank']}, N={payload['conductor']})")
    mu = build_mu_ec(payload["ap"], k)
    terms = [(n, mu[n], mp.log(n), mp.exp(-mp.mpf(n) / k)) for n in range(1, k + 1) if mu[n]]
    denom = mp.log(k) + EULER_GAMMA
    c1: list[str] = []
    cks: list[tuple[str, str]] = []
    for gamma_text, (real_text, imag_text) in zip(payload["zeros"], payload["lprimes"]):
        gamma = mp.mpf(gamma_text)
        ck = sum(coeff * weight * mp.exp((-1 - mp.j * gamma) * log_n) for n, coeff, log_n, weight in terms)
        value = abs(ck) * abs(mp.mpc(mp.mpf(real_text), mp.mpf(imag_text))) / denom
        cks.append((mp.nstr(mp.re(ck), precision), mp.nstr(mp.im(ck), precision)))
        c1.append(mp.nstr(value, precision))
    values = [mp.mpf(value) for value in c1]
    provenance = {"manifest": spec, "K": k, "precision": precision, "N_zeros": zeros, "Tmax": tmax,
                  "pari": payload, "normalization": "rho=1+i*gamma; mu(p)=-a_p; mu(p^2)=p"}
    provenance_hash = canonical_hash(provenance)
    raw = {"provenance_hash": provenance_hash, "provenance": provenance,
           "zeros": payload["zeros"], "Lprime": payload["lprimes"], "cK": cks, "C1": c1,
           "E_C1": mp.nstr(sum(values) / len(values), precision),
           "E_C1_sq": mp.nstr(sum(value * value for value in values) / len(values), precision)}
    raw_path = output_dir / f"{spec['label']}.json"
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    raw_path.write_text(json.dumps(raw, indent=2, sort_keys=True) + "\n")
    return {"label": spec["label"], "band": spec["band"], "rank": spec["rank"], "weight": spec["weight"],
            "conductor": spec["conductor"], "K": k, "precision": precision, "N_zeros": zeros, "Tmax": tmax,
            "E_C1": raw["E_C1"], "E_C1_sq": raw["E_C1_sq"], "error": "", "provenance_hash": provenance_hash}


def existing_valid(raw_path: Path, spec: dict[str, Any], k: int, zeros: int, tmax: int, precision: int) -> dict[str, Any] | None:
    try:
        raw = json.loads(raw_path.read_text())
        provenance = raw["provenance"]
        if (provenance["manifest"] == spec and provenance["K"] == k and provenance["N_zeros"] == zeros
                and provenance["Tmax"] == tmax and provenance["precision"] == precision
                and len(raw["zeros"]) == zeros and len(raw["Lprime"]) == zeros
                and len(raw["cK"]) == zeros and len(raw["C1"]) == zeros
                and canonical_hash(provenance) == raw["provenance_hash"]):
            return {"label": spec["label"], "band": spec["band"], "rank": spec["rank"], "weight": spec["weight"],
                    "conductor": spec["conductor"], "K": k, "precision": precision, "N_zeros": zeros, "Tmax": tmax,
                    "E_C1": raw["E_C1"], "E_C1_sq": raw["E_C1_sq"], "error": "", "provenance_hash": raw["provenance_hash"]}
    except (OSError, ValueError, KeyError, TypeError):
        return None
    return None


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def verify_raw_label_set(output_dir: Path, specs: list[dict[str, Any]]) -> None:
    expected = {spec["label"] for spec in specs}
    actual = {path.stem for path in output_dir.glob("*.json")}
    if actual != expected:
        raise RuntimeError(f"raw artifact labels differ from manifest: missing={sorted(expected - actual)}, extra={sorted(actual - expected)}")


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--curves-manifest", type=Path, default=DEFAULT_MANIFEST)
    p.add_argument("--output-dir", type=Path, default=DEFAULT_DATA / "path_b_b1_b2_raw")
    p.add_argument("--output-csv", type=Path, default=DEFAULT_CSV)
    p.add_argument("--k", type=int, default=10000)
    p.add_argument("--zeros", type=int, default=200)
    p.add_argument("--precision", type=int, default=50)
    # 150 gives 246 zeros for the sparsest selected target (389a1); every
    # selected B1/B2 curve has conductor at least 389, so it uniformly clears
    # the requested 200 without evaluating the unnecessary 1000-height tail.
    p.add_argument("--tmax", type=int, default=150)
    p.add_argument("--resume", action="store_true")
    p.add_argument("--regenerate-manifest", action="store_true", help="rerun discovery and overwrite the selected-control manifest")
    p.add_argument("--manifest-only", action="store_true", help="discover and write the deterministic manifest without C1 computation")
    p.add_argument("--verify-artifacts", action="store_true", help="verify raw JSON labels exactly match the manifest")
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if min(args.k, args.zeros, args.precision, args.tmax) <= 0:
        raise ValueError("K, zeros, precision, and Tmax must be positive")
    mp.mp.dps = args.precision
    if args.curves_manifest.exists() and not args.regenerate_manifest:
        specs = parse_manifest(args.curves_manifest)
    else:
        specs = discover_controls(args.precision)
        write_manifest(args.curves_manifest, specs)
    if args.manifest_only:
        print(f"wrote {args.curves_manifest} ({len(specs)} rows)")
        return 0
    if args.verify_artifacts:
        verify_raw_label_set(args.output_dir, specs)
        print(f"raw labels match {args.curves_manifest} ({len(specs)} rows)")
        return 0
    rows: list[dict[str, Any]] = []
    for spec in specs:
        raw_path = args.output_dir / f"{spec['label']}.json"
        if args.resume:
            prior = existing_valid(raw_path, spec, args.k, args.zeros, args.tmax, args.precision)
            if prior:
                print(f"resume {spec['label']}", flush=True)
                rows.append(prior)
                continue
        print(f"compute {spec['label']} ({spec['band']} rank={spec['rank']} N={spec['conductor']})", flush=True)
        try:
            rows.append(compute_row(spec, args.k, args.zeros, args.tmax, args.precision, args.output_dir))
        except Exception as exc:
            rows.append({"label": spec["label"], "band": spec["band"], "rank": spec["rank"], "weight": spec["weight"],
                         "conductor": spec["conductor"], "K": args.k, "precision": args.precision, "N_zeros": 0,
                         "Tmax": args.tmax, "E_C1": "", "E_C1_sq": "", "error": str(exc), "provenance_hash": ""})
            write_csv(args.output_csv, rows)
            raise
        write_csv(args.output_csv, rows)
    print(f"wrote {args.curves_manifest}, {args.output_csv}, and {args.output_dir}")
    verify_raw_label_set(args.output_dir, specs)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

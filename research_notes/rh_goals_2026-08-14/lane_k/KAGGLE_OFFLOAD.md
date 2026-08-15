# Kaggle offload — 2026-08-14

Status at time of writing: bundle construction and static validation complete; all six Kaggle pushes and all six status checks were blocked before upload by the local sandbox's inability to resolve `api.kaggle.com`. No kernel is claimed as pushed or running.

## Precedent and setup

Requested pull:

```text
kaggle kernels pull saarshai/hecke-spectrum-extend-certify -p /tmp/kg_precedent -m
```

The pull was attempted first. The local restore copy of the same precedent metadata was inspected because the network pull produced no files. Its pattern is mirrored exactly:

```json
{
  "language": "python",
  "kernel_type": "script",
  "is_private": true,
  "enable_gpu": false,
  "enable_tpu": false,
  "enable_internet": true
}
```

The q7/q8 script installs the precedent dependency with:

```python
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "python-flint"], check=True)
```

The zero scripts use `mpmath.mp.dps = 25`; their residual gate is `abs(zeta(1/2+i*gamma)) < 1e-15`. The q7/q8 script inlines the exact-Hurwitz/Arb-series primitives and q7 odd-q/q8 even-q block placement, and uses the family receipt's asymmetric manifest inflations:

```text
q7: 2.79, 2.39, 1.90, 1.56, 1.35
q8: 3.00, 1.90, 1.35
```

## Intended private kernel refs

| Kernel | Intended ref | Bundle | Intended work |
|---|---|---|---|
| Mertens part 1 | `saarshai/mertens-zeros-n100k-part1` | `mertens-zeros-n100k-part1` | indices 10,000–27,999; 18,000 rows |
| Mertens part 2 | `saarshai/mertens-zeros-n100k-part2` | `mertens-zeros-n100k-part2` | indices 28,000–45,999; 18,000 rows |
| Mertens part 3 | `saarshai/mertens-zeros-n100k-part3` | `mertens-zeros-n100k-part3` | indices 46,000–63,999; 18,000 rows |
| Mertens part 4 | `saarshai/mertens-zeros-n100k-part4` | `mertens-zeros-n100k-part4` | indices 64,000–81,999; 18,000 rows |
| Mertens part 5 | `saarshai/mertens-zeros-n100k-part5` | `mertens-zeros-n100k-part5` | indices 82,000–100,000; 18,001 rows to cover the inclusive endpoint |
| Hecke family | `saarshai/hecke-family-q7-q8-scan` | `hecke-family-q7-q8-scan` | q7/q8, both signs, surface + Newton pinning |

Each Mertens bundle contains `zeros1.txt` (100,000 lines; SHA-256 is computed in-kernel). Each CSV is checkpoint-appended every 500 rows with columns:

```text
index,gamma_refined,abs_zeta_prime_sq,residual
```

The Hecke output paths are:

```text
/kaggle/working/hecke_family_q7_q8_scan.json
/kaggle/working/hecke_family_q7_q8_stats.json
```

The scan protocol is `N_surface=14`, `N_pin=22`, `N_stable=28`, `n_head=4`, Re grid `0.10..0.50` with 17 points, and Im grid `3.0..17.0` with 0.1 spacing. It runs q7/q8 for `sign=+1` (`mms+`) and `sign=-1` (`mms-`).

## Push/status results

All six `kaggle kernels push -p <bundle>` commands exited `1`. All six `kaggle kernels status <ref>` commands also exited `1`. No successful push response or Kaggle runtime status was observed.

Canonical exact CLI error (identical for the pull, pushes, and status checks):

```text
urllib3.exceptions.NameResolutionError: HTTPSConnection(host='api.kaggle.com', port=443): Failed to resolve 'api.kaggle.com' ([Errno 8] nodename nor servname provided, or not known)
urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='api.kaggle.com', port=443): Max retries exceeded with url: /v1/security.OAuthService/IntrospectToken (Caused by NameResolutionError("HTTPSConnection(host='api.kaggle.com', port=443): Failed to resolve 'api.kaggle.com' ([Errno 8] nodename nor servname provided, or not known)"))
requests.exceptions.ConnectionError: HTTPSConnectionPool(host='api.kaggle.com', port=443): Max retries exceeded with url: /v1/security.OAuthService/IntrospectToken (Caused by NameResolutionError("HTTPSConnection(host='api.kaggle.com', port=443): Failed to resolve 'api.kaggle.com' ([Errno 8] nodename nor servname provided, or not known)"))
```

The token was not printed, copied, or inspected.

## Expected runtime

These are estimates only; no Kaggle execution began.

- Each Mertens part: tens of minutes to a few CPU-hours, depending on mpmath zeta throughput at ordinates up to about 75,000. The five parts are independent.
- Hecke family scan: roughly several to 18 CPU-hours for 9,588 surface cells plus Newton candidates; q7 is the dominant cost. It may approach or exceed a single Kaggle kernel runtime cap.

## Harvest commands after a successful push

```bash
mkdir -p /tmp/kg_harvest/mertens-zeros-n100k-part1
kaggle kernels output saarshai/mertens-zeros-n100k-part1 -p /tmp/kg_harvest/mertens-zeros-n100k-part1

mkdir -p /tmp/kg_harvest/mertens-zeros-n100k-part2
kaggle kernels output saarshai/mertens-zeros-n100k-part2 -p /tmp/kg_harvest/mertens-zeros-n100k-part2

mkdir -p /tmp/kg_harvest/mertens-zeros-n100k-part3
kaggle kernels output saarshai/mertens-zeros-n100k-part3 -p /tmp/kg_harvest/mertens-zeros-n100k-part3

mkdir -p /tmp/kg_harvest/mertens-zeros-n100k-part4
kaggle kernels output saarshai/mertens-zeros-n100k-part4 -p /tmp/kg_harvest/mertens-zeros-n100k-part4

mkdir -p /tmp/kg_harvest/mertens-zeros-n100k-part5
kaggle kernels output saarshai/mertens-zeros-n100k-part5 -p /tmp/kg_harvest/mertens-zeros-n100k-part5

mkdir -p /tmp/kg_harvest/hecke-family-q7-q8-scan
kaggle kernels output saarshai/hecke-family-q7-q8-scan -p /tmp/kg_harvest/hecke-family-q7-q8-scan
```

## Local verification evidence

```text
python_syntax_ok=6
metadata_private_cpu_internet_ok
security_scan: 0 finding(s) — risk = NONE
```

The local environment did not have `mpmath` or `python-flint`, so dependency execution was not locally runnable. The static checks did not execute the Kaggle kernels.

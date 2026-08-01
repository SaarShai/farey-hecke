# Prospective UCI blind audit

Pilot: `uci-optdigits-2026-08-01-label-blind-v2`
Frozen: `2026-08-01T19:24:02Z`
Items: **1797**
Outcome state: **ABSENT_BY_DESIGN**

## Commitments

- freeze.json SHA-256: `43af5bdcc36bc1d53fbdd6aca5781ad65e00ddcbf39c222d9eed1679cc25c7f8`
- manifest core SHA-256: `c9ad9346e5d56f074ca16d7e8c83279bba9be329d6a3443ac890471edcf1ed28`
- production order: `5050723c9ce258113b28c726d752a1f93b4b2c0c81e4cc75ce8ff42705c6c07d`
- seeded_random order: `94da556235d6a85312281011f4e2027c1d4bb4408d1ae767a76898ab26e80b5e`
- quota_balanced order: `9b8b85f3fe4da6623e8328933bec69d862997881c5e73ed86baf13ecc853d4e0`

The freeze contains predicted labels and confidence strata only. Test labels are not written to the manifest.
The result must be generated in a later reveal step and remains bound to this freeze digest.

## Commands

```bash
PYTHONPATH=src python3 prospective_uci_blind.py verify --dataset /path/to/optdigits.zip --pilot-dir pilots/uci-optdigits-2026-08-01
PYTHONPATH=src python3 prospective_uci_blind.py reveal --dataset /path/to/optdigits.zip --pilot-dir pilots/uci-optdigits-2026-08-01
```

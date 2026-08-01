# Prospective UCI blind audit

Pilot: `uci-optdigits-2026-08-01`
Frozen: `2026-08-01T19:16:13Z`
Items: **1797**
Outcome state: **ABSENT_BY_DESIGN**

## Commitments

- freeze.json SHA-256: `370604e81bc0099ce2bd64ab177cc59fc25b9bf94afdc3e7da8f8852aed02156`
- manifest core SHA-256: `2297588dc2289ad7ec27dc4404548d472ed7fd8c64fa972445da76109015d651`
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

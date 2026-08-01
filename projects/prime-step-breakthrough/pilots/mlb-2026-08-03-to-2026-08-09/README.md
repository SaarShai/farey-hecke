# Prospective blind audit pilot

Pilot: `mlb-2026-08-03-to-2026-08-09`
Frozen before outcomes: `2026-08-01T16:48:26.309411Z`
Fixed future games: **94**
Outcome state: **ABSENT_BY_DESIGN**

## Commitments

- freeze.json SHA-256: `d39fc9c16899c5a063c32b301537d114aac5ad4440d836329985fe646a4d2b73`
- manifest core SHA-256: `aadc3c2b6c86336daeaaa9cba55f3ccd74192c94e884bd444104dc66dde959f2`
- production order: `ea5aaffce8140f5fdbac5a457ce6a8d0407f40dca316a578f3aa794d62dea7d3`
- seeded-random order: `8c4e769fd3d4ccf0c8f36840c422e2c8e7f902f93679881c81b8f228bc8ea9d6`
- quota-balanced order: `91c4e409898efd2eb1534669c2fa12bfc9acd93d8f7862abd3f58ce723f3458e`

The three full game-ID sequences, source snapshots, prediction rule, strata, randomization seed, and analysis rule are frozen in `freeze.json`.
`reveal` fails closed until every fixed game ID is final. The production order receives only the distribution-free stopping certificate; exact hypergeometric stopping requires the committed randomization used by the other two orders.

## Commands

```bash
PYTHONPATH=src python3 prospective_blind_audit.py verify --pilot-dir pilots/mlb-2026-08-03-to-2026-08-09
PYTHONPATH=src python3 prospective_blind_audit.py status --pilot-dir pilots/mlb-2026-08-03-to-2026-08-09
PYTHONPATH=src python3 prospective_blind_audit.py reveal --pilot-dir pilots/mlb-2026-08-03-to-2026-08-09
```

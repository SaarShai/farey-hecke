# Fleet & tooling — live as of 2026-06-08 (non-secret)

Secrets live in `.secrets/credentials.env` (gitignored) — `source` it to load keys. NEVER commit keys.

## Aristotle (Lean-4 automated prover) — WORKING
- CLI installed: `~/.local/bin/aristotle` (v2.0.0, `uv tool install aristotlelib`). Key in `.secrets/` (`ARISTOTLE_API_KEY`).
- Pattern: build a self-contained Lean project dir (toolchain `leanprover/lean4:v4.28.0`, lakefile requiring mathlib `v4.28.0`; copy from `projects/aristotle_dispatch_v10/`), then:
  - `export PATH="$HOME/.local/bin:$PATH"; source .secrets/credentials.env`
  - `aristotle submit "<proof instructions>" --project-dir <dir>` (ASYNC → returns project id; do NOT use --wait)
  - poll `aristotle show <id>`; fetch `aristotle download <id> --destination <path>` (a `.tgz`)
- Proven end-to-end this session: `bczOnsetEqualsQStar` (X(3)=q* onset), 0 sorries — `projects/aristotle_dispatch_v10/solved/`.

## Kaggle — WORKING
- CLI `~/.local/bin/kaggle`, authenticated (token `~/.kaggle/access_token`, user `saarshai`). Unused this session (local sufficed); use for >~10 min jobs.

## Compute nodes M1 / M2 — UP (key-authorized)
- M1: `ssh -i ~/.ssh/id_ed25519 new@192.168.1.22` (10c, mpmath 1.3, numpy 2.0)
- M2: `ssh -i ~/.ssh/id_ed25519 alicia@192.168.1.92` (12c, mpmath 1.4, numpy 2.0)
- IPs DRIFT (DHCP); re-discover per `MACHINE_ACCESS.md` if a connect fails. Farey repo absent on nodes → `scp` the script first; wrap long jobs in `caffeinate -s`.
- Used this session: M2 ran the D3-r4 JP large-q sweep.

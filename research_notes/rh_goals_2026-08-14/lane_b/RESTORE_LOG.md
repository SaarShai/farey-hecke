# Lane B — Aletheia stack restore log — 2026-08-14

## G2-S0 GATE: PASSED

- Worktree: `.worktrees/aletheia-restore`, first at b973d56, then advanced to
  4c42ca0 (Wave 2 — fullest state: resonance engine + G_7 + collocation
  cross-checks + MMS convention pin).
- Environment rebuilt fresh: uv venv `/Users/za/.venvs/farey-rh` with
  mpmath 1.4.1, python-flint 0.9.0, numpy 2.5.2.
- Smoke-run: `code/zeta_cert_q3.py` (at b973d56; diff vs 4c42ca0 empty for
  this script) — runtime 978.6 s. Output verbatim verdict:
  "6/6 enclosures contain published; 6/6 proven Re sign-change; 6/6
  dimension-certified; 6/6 strict-interior; max width 1.22e-05".
  Matches the recorded 2026-06-20 anchor (6/6 @ width 1.2e-5).
  Receipt: `.worktrees/aletheia-restore/code/out/zeta_cert_q3.json`.
- zeta_cert_q3.py is byte-identical between b973d56 and 4c42ca0 (empty
  diff), so the anchor pass carries to the advanced worktree.

## Present in worktree (4c42ca0)

zeta_cert_q3.py, zeta_cert_rosen_q5.py, zeta_mayer.py, zeta_mayer_rosen.py,
run_zeta_rosen_staged.py, hejhal_g5_maass.py, hejhal_g8_maass.py,
run_resonance_g7.py, run_resonance_geometry.py, run_resonance_p3.py,
certify_g7_resonances.py (+ goal1_Bq_* rotation-arc suite).

## Geometry signature reproduction (same day): PASSED

run_resonance_geometry.py, 1585 s, fresh env. q=3: n=8, re_mean
0.24999999999998, re_std 6.475e-14 (recorded 6.5e-14 — match). G_5: n=8
N-stable, Re ∈ [0.39982, 0.48527], re_std 0.029986 (recorded ~0.03 — match);
pinned coordinates identical to the 2026-06-20 list. Receipt:
`.worktrees/aletheia-restore/code/out/resonance_geometry.json`.
G2-S0 CLOSED in full.

## Next (G2-S1)

- q=4 / q=6 arithmetic controls dispatched to codex lane (prediction: rigid
  vertical line(s); failure kills the signature claim → fallback = atlas).
- Decide merge strategy: this stack should come back to a live branch
  (currently only in worktree/history).

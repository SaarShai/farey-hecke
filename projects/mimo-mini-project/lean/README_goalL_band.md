# Goal-L Hecke scalar window-lemma band (q = 7..16)

Machine-checked lower-bound engine for the Hecke ergodic-optimization theorem
**`X_Ω(q) = 1/λ³`, `λ = λ_q = 2cos(π/q)`** (the user's own paper; keep separate from Koyama work).
Each file proves: along a genuine-domain scalar `BCZ_q` orbit, no window of `W(q)` consecutive
gap-products `P_n = c_n c_{n+1}` is all `< 1/λ³`. Its orbit form `g{q}_no_window_below_genuine` is
exactly the `hWin` input of the verified `essSup` window engine, giving `X_Ω(q) = 1/λ³` (with the
all-q cusp upper bound, already verified elsewhere).

## Files
| file | q | window W | field deg `d_q` | `9/5<λ` source | maxHeartbeats |
|---|---|---|---|---|---|
| `HeckeLamBounds_VERIFIED.lean` | — | — | — | `hecke_lam_lo : ∀q≥10, 9/5<2cos(π/q)` | default |
| `BCZHeckeG7_window_VERIFIED.lean`  | 7  | 4 | 3 | `g7_lam_lo` from `hps` (unique root) | 1 600 000 |
| `BCZHeckeG8_window_VERIFIED.lean`  | 8  | 4 | 4 | `g8_lam_lo` from `hps` | 1 600 000 |
| `BCZHeckeG9_window_VERIFIED.lean`  | 9  | 4 | 3 | `g9_lam_lo` from `hps` | 1 600 000 |
| `BCZHeckeG10_window_VERIFIED.lean` | 10 | 4 | 4 | hypothesis `hlo` (← `hecke_lam_lo`) | 1 600 000 |
| `BCZHeckeG11_window_VERIFIED.lean` | 11 | 4 | 5 | hypothesis `hlo` | 1 600 000 |
| `BCZHeckeG12_window_VERIFIED.lean` | 12 | **5** | 4 | `g12_lam_lo` from `hps` | 20 000 000 |
| `BCZHeckeG13_window_VERIFIED.lean` | 13 | 5 | 6 | hypothesis `hlo` | 20 000 000 |
| `BCZHeckeG14_window_VERIFIED.lean` | 14 | 5 | 6 | hypothesis `hlo` | 20 000 000 |
| `BCZHeckeG15_window_VERIFIED.lean` | 15 | 5 | 4 | `g15_lam_lo` from `hps` | 20 000 000 |
| `BCZHeckeG16_window_VERIFIED.lean` | 16 | 5 | 8 | hypothesis `hlo` | 20 000 000 |

- **q=12** uses `W=5` (its `W=4` `(1,1,1)`-case had no Positivstellensatz certificate at product-degree
  ≤ 3; the weaker `W=5` window has a degree-2 certificate and gives the same conclusion).
- The multi-root `hlo : 9/5 < λ` hypothesis is **not vacuous** — `HeckeLamBounds_VERIFIED.lean` proves
  `9/5 < 2cos(π/q)` for all `q ≥ 10`, so for `λ = 2cos(π/q)` only the algebraic relation `hps` is a
  genuine input.

## Verify
```bash
# needs a built full-Mathlib v4.28.0 Lake project (default /tmp/lean-minus1, 8018 oleans)
./verify_goalL_band.sh [ENV_DIR]
```
Asserts `EXIT=0` and `#print axioms = [propext, Classical.choice, Quot.sound]` (no `sorryAx`) for every
file. Single command per file: `( cd ENV_DIR && ~/.elan/bin/lake env lean FILE.lean )`.
Total ~20–30 min single-threaded (q=16's degree-8 / 84-product certificate is ~8 min).

## How each proof works (for future edits)
1. **Floor reduction:** inside a full `W`-window every *interior* floor `K_n` is forced to `1`
   (`g{q}_floor_helper`): the `K≥2` bound `λ⁴ m² < 1` + a neighbour bound + a Taha edge contradict the
   **field-independent** fact `(λ²−λ)² ≥ 2`, which holds from `9/5 < λ < 2` alone.
2. **Single case:** with all floors `=1` the recurrence is the linear Chebyshev/rotation map, so the
   window core is ONE Positivstellensatz infeasibility certificate (`case_q{q}`) — a nonnegative
   combination of products of the domain generators that reduces (mod the minimal polynomial `hps`) to a
   negative rational, closed by `linarith`. Certificates are produced by `code/Lgoal_buildcore.py`.
3. **Glue:** `g{q}_core` proves each `K_n=1` then dispatches `case_q{q}`; `g{q}_no_window_below_genuine`
   lifts it to orbits.

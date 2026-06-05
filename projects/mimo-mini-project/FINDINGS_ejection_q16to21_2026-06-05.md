# Deep-mid EJECTION lemma — PROVEN in Lean, uniform box q=16..21 (GATE-2 piece 3)

**Date:** 2026-06-05. Self-recompiled in `/tmp/lean-minus1`: **EXIT=0**, `#print axioms
HeckeEjection.ejection_kick = [propext, Classical.choice, Quot.sound]`, no `sorryAx` (Hard Rule 1).
File: `lean/BCZHeckeEjection_q16to21_VERIFIED.lean`.

## What it is
The §5-B deep-mid ejection lemma (handoff GATE-2 (3)): a non-F-corridor branch step with `P_i < thr`
ejects in one step (`dwell ≤ 1`). It GENERALIZES the existing
`BCZHeckeTwoStepKick_q1617_VERIFIED.two_step_kick` from the q=16,17 box to a single box covering
**q = 16,17,18,19,20,21**. Same statement/modeling; only the rational parameter box widened.

## Modeling (verified sound vs the validated genuine map, not just asserted)
On a non-F branch `i` write `u=L_{i−1}, v=L_i, r=x_{i−2}/x_{i−1}`.
- **Observable is exact:** `P_i = a·L_i/x_{i−1} = uv − rv²` — proven by hand via the Casorati identity
  `x_{i−1}² − x_i x_{i−2}=1`, and confirmed numerically (0 mismatch).
- **Successor on scalar branch q−1** (verified q=16..21, 12625 cells, 0 exceptions): `a'=v`,
  `b'=(λv−u)+kλv`, `k=⌊(1−L_{i+1})/(λL_i)⌋ ≥ 0`. Genuine successor observable
  `P' = v·((λv−u)+kλv) = (λv²−uv) + kλv² ≥ λv²−uv`. So **`thr ≤ λv²−uv ⟹ thr ≤ P'` for ANY k** —
  the lemma's conclusion is a valid lower bound on the genuine successor, independent of the floor.
  (The q16,17 file's "k=0" prose was loose; the bound holds for all k≥0 because `kλv² ≥ 0`.)
- **Domain hyps hold genuine** (verified, 0 violations q=16..21): `u>1` (branch enter), `v≤1`
  (branch), `λv−u≤1` (from `b'≤1` and `kλv≥0`), `1<2λv−u`.

## The box (verified: contains all genuine cells AND keeps margin>0)
`l∈[49/25,99/50]=[1.96,1.98]`, `r∈[47/50,61/50]=[0.94,1.22]`, `thr∈[129/1000,663/5000]=[0.129,0.1326]`.
- **Containment:** all 12625 genuine non-F sub-threshold cells at q=16..21 lie inside box+hyps
  (`/tmp/box_final.py`, 0 outside). Genuine ranges: `l=1.9616…1.9777`, `r=0.955…1.207`,
  `thr=1/λ³=0.1293…0.1325`.
- **Margin:** `min(λv²−uv−thr) = 0.0527 > 0` over the FULL relaxed box (12M-sample search, all >0).
  Comfortably above rational-bound error ⇒ a single `nlinarith` (proof mirrors `two_step_kick`,
  widened `(61/50−r)` hint). `hr`/`htop` end up unused (only the upper-r and lower-successor
  bounds bind) — kept for faithfulness to the genuine domain.

## Honest status / what this does NOT yet close
- **PROVEN (Lean, my-verified):** ejection lemma, q=16..21. This is GATE-2 piece (3).
- GATE-2 closure for q=17..21 ALSO needs (per `FINDINGS_GATE2_multibranch_2026-06-05.md`):
  (2) (L2) F-family switches — PROVEN; (4) torsion-quantization — NUMERICAL only, not a stated Lean
  lemma; and the **genuine per-q assembly** wiring (`essSup_ge_of_window` chaining) — NOT a single
  proven theorem yet (the q16,17 file flags it as "to be wired").
- ✅ **F-window gap at q=17 CLOSED (2026-06-05, later same day).** Emitted via
  `code/Lgoal_buildcore_q17tmp.py 17` (W=6, degree-8 field `lam^8 = lam^7+7lam^6-6lam^5-15lam^4
  +10lam^3+10lam^2-4lam-1` = genuine minpoly of 2cos(π/17)), compiled in `/tmp/lean-minus1`
  (maxHeartbeats 400M + maxRecDepth 10000), **EXIT=0, axiom-clean** `[propext, Classical.choice,
  Quot.sound]` on all 4 decls (`g17_floor_helper`, `case_q17`, `g17_core`,
  `g17_no_window_below_genuine`) — NO Aristotle needed, closed locally. Installed as
  `lean/BCZHeckeG17_window_VERIFIED.lean`. Non-vacuity checked: `9/5<lam` (≈1.96595) isolates this
  root (next conjugate 2cos(3π/17)≈1.70 < 1.8). **Window series is now CONTIGUOUS q=7..21.** So
  q=17's closure is NO LONGER blocked on its F-window. (q=18..21 windows exist as `*_VERIFIED` files
  but were NOT re-recompiled by me this session — status is as-claimed, not my-verified.)

## Artifacts (scratch, /tmp only — no repo pollution)
`/tmp/eject_probe.py`, `/tmp/eject_all.py`, `/tmp/verify_twostepkick.py`, `/tmp/box_final.py`.

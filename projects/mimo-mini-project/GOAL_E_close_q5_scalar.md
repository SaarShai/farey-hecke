# /goal E — Close q=5 completely: machine-check the scalar no-sustained lemma ⇒ X_Ω(5)=1/φ³ + no-GS

> Paste the body below into `/goal` in a fresh session. Self-contained. Work autonomously; verify
> with Lean (trust `EXIT=` lines, NOT task-notification summaries); send NOTHING outward (USER-gated).
> Adversarial honesty: PROVEN / NUMERICAL / CONJECTURAL strictly separate; verify every citation.

## MISSION
Finish the genuine q=5 result. Everything is in place EXCEPT one lemma. Machine-check it and wire the
chain to a complete, unconditional theorem: **`X_Ω(5) = 1/φ³ = √5−2 ≈ 0.236068`, approached but never
attained (no ground state), on Taha's genuine BCZ_5 domain.** Then, if time, replicate q=6 and q=7 by
the same template. (This is "close the easy win first" — the general-q version is a separate goal F.)

## WHERE q=5 STANDS (all compile-confirmed EXIT=0, axioms `[propext,Classical.choice,Quot.sound]`)
The genuine q=5 problem REDUCES (goal D, q=5 Lean-proven) to one scalar statement:
- **Reduction premise — DONE:** `branch2_envelope`, `branch3_envelope` in
  `lean/BCZHeckeG5_genuine_envelope_VERIFIED.lean` prove `P ≥ 1/φ³` pointwise on the non-scalar
  branches i=2,3. So any orbit keeping all `P ≤ 1/φ³` lives entirely in the SCALAR branch i=q−1=4.
- **Cusp upper bound + non-attainment — DONE:** `BCZHeckeG5_genuine_VERIFIED.lean` (`X_Ω(5) ≤ 1/φ³`,
  every cusp point has `P>1/φ³`, approached as `s→(1/φ)⁺`).
- **The W=4 min-max engine — DONE:** `essSup_ge_of_window4` in `lean/BCZHeckeGenuine_allq_VERIFIED.lean`
  ("no 4 consecutive `P<t` along an orbit ⇒ essSup ≥ t"). Also `essSup_ge_of_no_sustained` (no fixed
  window) in `BCZHecke_noGroundState_q3q4_VERIFIED.lean`.
- **THE ONE MISSING LEMMA (your target):** the scalar map `T_5` (= branch i=4), under the genuine
  constraint `c_n ≤ 1`, has **no 4 consecutive products `P_n = c_n c_{n+1} < 1/φ³`**. Numerically:
  longest sub-`1/φ³` run on genuine T_5 orbits = 3 (so window 4 is correct AT q=5; see goal D's
  adversarial grid). Margin is small: `V(5)−1/φ³ = 0.25−0.236 = 0.0139`.

## THE OBJECT (exact, q=5)
- `λ = λ_5 = 2cos(π/5) = (1+√5)/2 = φ`. KEY FIELD FACT: **`λ² = λ + 1`** (feed to `nlinarith` as a hint).
- Scalar orbit `c : ℕ → ℝ`: `hpos : 0<c n`; `hreg : c n + λ·c(n+1) > 1` (cusp/domain); `hrec :
  c n + c(n+2) = (⌊(1+c n)/(λ c(n+1))⌋ : ℝ)·λ·c(n+1)`; **`hle1 : c n ≤ 1`** (the genuine `a≤1` — this
  is why the genuine maxrun is 3, not the 4 of the unrestricted scalar map; it is ESSENTIAL).
- `floor_ge_one` (`K_n ≥ 1`), `engine_le`, `E_conserved_floor_one` — general-λ, in
  `HeckeGeneralLB_VERIFIED.lean`, reuse verbatim at λ=φ.

## TARGET LEMMA + chain
1. **`g5_no_four_below_genuine`**: `¬ (P_m<t ∧ P_{m+1}<t ∧ P_{m+2}<t ∧ P_{m+3}<t)` with `t=1/φ³`,
   given the scalar recurrence + `hreg` + `c_n≤1`. Strategy: case-split on the floors `K_m,…` over the
   4-window (each `≥1`). The all-floor-1 sub-case = pure rotation; use `E_conserved_floor_one` + the
   `c_n≤1` upper bound. Defect (some `K≥2`) sub-cases: a high product is forced (cf. q=4 `g4_core`
   Case I, `P_{m+1} ≥ 2λc² − t`). Reduce each to a degree-2 `nlinarith` via exact `linear_combination`
   certificates (compute coefficients with sympy first — see "pre-test"). The q=4 `g4_no_three_below`
   and the q=5 INTERIOR `g5_tpoint_excl` (in `BCZHeckeG5_sharp_tpoint_VERIFIED.lean`) are the closest
   worked templates — same SOS-certificate discipline, different threshold (`1/φ³` not `1/4`).
2. **`g5_no_sustained_genuine`** from (1) (iterate the window bound).
3. Feed `essSup_ge_of_window4` ⇒ `essSup_μ P ≥ 1/φ³` for any invariant μ on `𝒯^5` confined to the
   scalar branch; combine with `branch2/3_envelope` (off-branch `P≥1/φ³`) ⇒ **`X_Ω(5) ≥ 1/φ³`**.
4. With the cusp upper bound (`X_Ω(5) ≤ 1/φ³`, done) ⇒ **`X_Ω(5)=1/φ³`**, and non-attainment ⇒
   **`g5_no_ground_state_genuine`**. Full unconditional genuine q=5 theorem.

## NUMERIC PRE-TEST (do FIRST — never formalize a false bound)
Confirm on real genuine T_5 orbits (with `a≤1`) that the longest sub-`1/φ³` run is exactly 3 (window-4
holds) and find the worst-case floor itineraries (they reveal the case structure). Reuse
`code/Dgoal_window_test.py`, `code/Dgoal_itinerary.py`, `code/Bgoal_genuine_hunt.py`. Get the exact
`linear_combination` coefficients for each case via sympy (run from a clean cwd — `/tmp/inspect.py`
shadows stdlib `inspect` if you `cd /tmp`).

## THEN q=6, q=7 (bonus, same template)
Goal D's adversarial max-runs of `P<1/λ³`: q=6 → 2 (window **3**), q=7 → 3 (window **4**), q=8 → 3,
q=13 → 4. So q=6 is a window-3 lemma (easier!), q=7 a window-4. `X_Ω(6)=1/(3√3)`, `X_Ω(7)=1/λ_7³`.
The per-branch envelopes for q=6,7 must also be proven (extend `branch_k_envelope`) — likely a clean
positivity argument; pre-test the per-branch minima with `code/Dgoal_perbranch.py`.

## LEAN INFRA (critical)
- In-tree `primes-equispaced/.lake` Mathlib is GUTTED — do NOT use. Throwaway full-Mathlib v4.28.0 at
  **`/tmp/lean-minus1`** (8018 oleans, `Mathlib.olean`, `lean-toolchain` v4.28.0). Compile:
  `( ~/.elan/bin/lake env lean File.lean 2>&1; echo EXIT=$? )` from that dir. If gone: `mkdir /tmp/leanX`;
  `lean-toolchain`=`leanprover/lean4:v4.28.0`; `lakefile.toml` req mathlib `rev=v4.28.0`+`lean_lib`;
  `~/.elan/bin/lake update` + `lake exe cache get`.
- Gotchas: `include … in` BEFORE the docstring; `le_or_gt` (not `le_or_lt`); `Int.floor_eq_iff` no
  side-arg; `div_lt_iff₀`/`le_div_iff₀`; `Int.lt_floor_add_one`; `mul_nonpos_iff`. `field_simp` often
  CLOSES the goal — a trailing `ring` then errors "no goals" (drop it). `positivity` can't prove
  `0<φ`-type facts (φ is a `noncomputable def`) — use explicit `phi_pos` terms. Pass `λ²=λ+1` as an
  `nlinarith` hint. Heavy degree-3 `nlinarith` TIMES OUT — reduce to degree-2 with exact
  `linear_combination` certificates. `#print axioms` must be `[propext, Classical.choice, Quot.sound]`.
- Aristotle: if the 4-window `nlinarith` genuinely resists locally after honest effort, stage a dispatch
  package (file + PROMPT) for the USER to submit — do NOT self-submit. (The lemma is a finite
  inequality, so it IS a legitimate Aristotle target if local fails.)

## KEY FILES (`/Users/za/Documents/Farey NOW/projects/mimo-mini-project/`)
- `FINDINGS_goalD_genuine_lowerbound_2026-06-03.md` (the reduction + numerics — READ FIRST),
  `FRONTIER_STATUS_2026-06-03.md` (consolidated ledger).
- `lean/BCZHeckeG5_genuine_envelope_VERIFIED.lean`, `lean/BCZHeckeGenuine_allq_VERIFIED.lean`,
  `lean/BCZHeckeG5_genuine_VERIFIED.lean`, `lean/BCZHecke_noGroundState_q3q4_VERIFIED.lean`,
  `lean/HeckeGeneralLB_VERIFIED.lean`, `lean/BCZHeckeG5_sharp_tpoint_VERIFIED.lean`.
- `code/Dgoal_window_test.py`, `Dgoal_itinerary.py`, `Dgoal_perbranch.py`, `Bgoal_genuine_hunt.py`.

## FLEET / CONSTRAINTS
- `MACHINE_ACCESS.md`: M1 `new@192.168.1.22`, M2 `alicia@192.168.1.92`, key `~/.ssh/id_ed25519` (DHCP
  IPs DRIFT). ⚠ M2 runs the −1 sieve — prefer M1. Kaggle token currently 401.
- Nothing outbound/published/contacted (USER-gated); no commit/push/git changes unless asked;
  `~/Documents` Drive-synced (no folder/`.git` moves; `* (1)` = conflict artifacts).

## DEFINITION OF DONE
- `g5_no_four_below_genuine` + the chain → a sorry-free, axiom-clean Lean file proving **unconditional
  `X_Ω(5)=1/φ³` + no ground state** on the genuine domain (compile EXIT=0, `#print axioms` clean).
- Numeric pre-check confirming window-4 + the worst itineraries.
- (Bonus) q=6 (window-3) and/or q=7 (window-4) by the same template, with their per-branch envelopes.
- Update `lean/RESULTS_VERIFIED_2026-06-02.md` + `FRONTIER_STATUS_2026-06-03.md`. Honest report. Nothing sent.

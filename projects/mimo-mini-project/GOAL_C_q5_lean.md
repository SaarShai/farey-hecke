# /goal C — Machine-check q=5: sharp X(5)=1/4 + no-ground-state (first connected-regime case)

> 🛑 **PREMISE FALSE (2026-06-03) — DO NOT run as written.** Two independent results killed it:
> (1) goal C's OWN run found the 4-window bound `g5_no_four_below` is **FALSE** (explicit entry-edge
> witness; max below-run = 4, so cluster C(5)=4, not 3 — see `project_g5_window_refutation` memory);
> only the NON-sharp `X(5) ≥ (√5−2)/2` was machine-checked on the naive map. (2) goal B
> (`FINDINGS_goalB_genuine_domain_2026-06-03.md`, re-verified) showed the genuine value is
> `X_Ω(5)=1/φ³=√5−2≈0.2361` (cusp word `[(q−2,0)]` on Taha's BCZ_q), NOT `1/4`. `1/4=V(5)` is only the
> single-branch INTERIOR optimum. If reviving a q=5 Lean target, use the genuine cusp value `1/λ³` or
> the corrected window, not `X(5)=1/4`/4-window. λ=φ, λ²=λ+1 still apply.

> Paste the body below into `/goal` in a fresh session. Self-contained. Work autonomously; verify
> with Lean (trust `EXIT=` lines, NOT task-notification summaries); send NOTHING outward (USER-gated).
> Adversarial honesty: PROVEN / NUMERICAL / CONJECTURAL strictly separate; verify citations.

## MISSION
Extend the machine-checked set beyond q=3,4 by formalizing **q=5** in Lean (Mathlib v4.28.0):
1. the sharp lower bound `X(5) = 1/4` (no `T_5`-orbit keeps all products `P_n = c_n c_{n+1} < 1/4`),
2. hence no ground state (the infimum `1/4` is approached but unattained).
This is the FIRST connected-regime case (`V(5)=1/4 > 1/(4λ)=(√5−1)/8≈0.1545`), so it is genuinely
harder than q=4 (tangent) — but it is concrete, bounded, and `g4`-style. Goal: a sorry-free,
axiom-clean file `lean/BCZHeckeG5_noGroundState.lean`, `#print axioms` = `[propext, Classical.choice,
Quot.sound]`. (If you also get q=6,7 by the same template, bonus; q=5 is the DoD.)

## THE OBJECT (exact, q=5)
- `λ = λ_5 = 2cos(π/5) = (1+√5)/2 = φ` (golden ratio). KEY ALGEBRAIC RELATION: **`λ² = λ + 1`**
  (use this everywhere `nlinarith`/`linear_combination` need the field fact, exactly as the q=4 proof
  uses `s²=2`).
- Map `T_5(x,y) = (y, ⌊(1+x)/(λy)⌋·λy − x)` on `D = {x>0, y>0, x+λy>1}`; observable `P=xy`.
- Scalar orbit form (the proof works on `c : ℕ → ℝ` with): `hpos : 0<c n`; `hreg : c n+λ·c(n+1)>1`;
  `hrec : c n + c(n+2) = (⌊(1+c n)/(λ c(n+1))⌋ : ℝ)·λ·c(n+1)`. Floor `K_n ≥ 1` always (`floor_ge_one`,
  already proven in `HeckeGeneralLB_VERIFIED.lean`).
- Target: `V(5)=1/4`. The optimizer word is `(1,1,2)` (period N=q−2=3), orbit `c_n=R·sin((n+1)π/5)`
  = `R·(sin36°, sin72°, sin72°)`. The cluster bound is `C(5)=3` (#7, genuine cusps), so the WINDOW
  bound to prove is a **4-window**: no 4 consecutive products `< 1/4` (max of any 4 consecutive `≥ 1/4`).

## WHAT TO PROVE (the chain, mirroring q=4)
1. **`g5_no_four_below`** (the window bound): for all n, `max(P_n,P_{n+1},P_{n+2},P_{n+3}) ≥ 1/4`
   — equivalently NOT all four `< 1/4`. This is the crux. Strategy: case-split on the floors
   `K_n,…` over the window (each `≥1`); the all-floor-1 (pure rotation) sub-case uses the conserved
   `E = c_n²+c_{n+1}²−λ c_n c_{n+1}` (lemma `E_conserved_floor_one`, PROVEN) which on a rotation run
   pins the swept product max `≥ V`; the defect sub-cases (some `K≥2`) are handled as in q=4's
   "Middle"/floor-jump cases. Expect `nlinarith` with `λ²=λ+1` + the `E`-identity + `sq_nonneg`
   witnesses. PRE-TEST numerically (q=5 orbits, 4-window min-max → 1/4⁺) before grinding Lean.
2. **`g5_no_sustained`**: no orbit has all products `< 1/4` (iterate the window bound).
3. **`g5_exists_product_gt` / measure form**: plug into the abstract engine **`essSup_ge_of_window`**
   (already machine-checked, in `BCZHecke_noGroundState_q3q4_VERIFIED.lean`) with `t=1/4`,
   window=4 ⇒ `essSup_μ P ≥ 1/4` for any invariant μ on D. With the family giving `essSup→1/4`,
   conclude `X(5)=1/4` unattained = **`g5_no_ground_state`**.

## TEMPLATE TO PARAMETRIZE (read these — q=4 is the blueprint)
- `projects/mimo-mini-project/lean/BCZHecke_noGroundState_q3q4_VERIFIED.lean` — has the abstract engine
  `essSup_ge_of_window` AND the full q=4 chain: `g4_core`, `g4_no_three_below` (3-window),
  `g4_not_t_at` (t-point exclusion, 4 cases incl. floor-=3 Middle), `g4_no_sustained`,
  `g4_exists_product_gt`, `g4_no_ground_state`. **Copy this structure; change `s²=2`→`λ²=λ+1`,
  3-window→4-window, `√2`→`φ`.**
- `projects/mimo-mini-project/lean/BCZHeckeG4_noGroundState_WIP.lean` + `code/BCZHeckeG4_core.lean` —
  the standalone q=4 scalar core (cleanest starting point to clone for q=5).
- `projects/mimo-mini-project/lean/HeckeGeneralLB_VERIFIED.lean` — `floor_ge_one`, `engine_le`,
  `E_conserved_floor_one` (reuse directly; they are general-λ, so they apply at λ=φ verbatim).
- `projects/mimo-mini-project/research_notes/TrackA_no_ground_state.md` — the q=3,4 PAPER proofs.
- `projects/mimo-mini-project/research_notes/TrackA_general_lower_bound_strategy.md` — the q=5 route sketch + the connected-regime explanation.
- `projects/mimo-mini-project/FINDINGS_corrected_2026-06-02.md` — corrected scope (q=5 IS feasible; read first).

## NUMERIC PRE-CHECK (do before Lean)
Confirm on real `T_5` orbits that the 4-window min-max → `1/4⁺` and there IS no 5th-consecutive
(cluster exactly 3). Re-use / adapt `code/Xq_cluster_crosscheck.py` and `code/ergodic_hecke_hunt.py`
(`orbit_direction`, `svalid_range` — note q=5 word `(1,1,2)` is feasible, `s_lo<s_hi`). This nails the
exact constant the window bound must hit and prevents formalizing a false bound.

## LEAN INFRA (critical — costs a session if missed)
- In-tree `primes-equispaced/.lake` Mathlib is GUTTED — do NOT use. Throwaway full-Mathlib v4.28.0
  already at **`/tmp/lean-minus1`** (8018 oleans, `Mathlib.olean`, `lean-toolchain` v4.28.0).
  Compile from there: `( ~/.elan/bin/lake env lean File.lean 2>&1; echo EXIT=$? )`. If gone, rebuild:
  `lean-toolchain`=`leanprover/lean4:v4.28.0`, `lakefile.toml` req mathlib `rev=v4.28.0`,
  `~/.elan/bin/lake update` + `lake exe cache get`.
- Gotchas seen: `include … in` BEFORE the docstring; `le_or_gt` (not `le_or_lt`); `Int.floor_eq_iff`
  no side-arg; `div_lt_iff₀`/`le_div_iff₀`; `Int.lt_floor_add_one`; `mul_nonpos_iff`. For the field
  fact pass `λ²=λ+1` (`hλsq`) as an nlinarith hint, not a rewrite. `#print axioms` must show only
  `[propext, Classical.choice, Quot.sound]` (no `sorryAx`). Trust the `EXIT=` line.
- Aristotle option: if the 4-window `nlinarith` resists locally, stage a dispatch package (the file +
  a PROMPT) for the USER to submit to Aristotle — do NOT self-submit.

## FLEET / CONSTRAINTS
- `MACHINE_ACCESS.md`: M1 `new@192.168.1.22`, M2 `alicia@192.168.1.92`, key `~/.ssh/id_ed25519`
  (DHCP IPs drift). ⚠ M2 busy with the −1 sieve — prefer M1 for any heavy numeric search.
- Hard rules: nothing outbound/published/contacted (USER-gated); no commit/push/git changes unless
  asked; `~/Documents` Drive-synced (no folder/`.git` moves; `* (1)` = conflict artifacts);
  PROVEN/NUMERICAL/CONJECTURAL strictly separate; verify citations vs primary.

## CITATIONS (if cited, verify vs primary)
- Boca–Cobeli–Zaharescu, Crelle 535 (2001). Athreya–Cheung, IMRN 2014 (arXiv:1206.6597).
- O. Jenkinson, ETDS 39 (2019). G. Contreras, Invent. Math. 205 (2016) (compact+generic — no
  contradiction with our non-compact specific-P setting). Taha, arXiv:1810.10668.

## DEFINITION OF DONE
- `lean/BCZHeckeG5_noGroundState.lean` compiling EXIT=0, `g5_no_four_below` + `g5_no_ground_state`
  sorry-free, `#print axioms` = `[propext, Classical.choice, Quot.sound]`.
- A numeric pre-check confirming the 4-window 1/4 bound + cluster=3 on real T_5 orbits.
- Update `lean/RESULTS_VERIFIED_2026-06-02.md` (q=5 now machine-checked). Honest report. Nothing sent.

# HANDOFF — session 2026-06-02 (−1 dominance + Hecke ergodic-optimization discovery)

> Self-contained handoff for a fresh session. Everything is committed to the local repo (and on
> disk, Drive-synced) so any session can read it. Work autonomously; verify with results (trust
> `EXIT=`/`run.log` lines, NOT task-notification summaries); send NOTHING outward (Koyama/IP/publish
> are USER-gated); adversarial honesty (separate PROVEN / NUMERICAL / CONJECTURAL; verify every
> citation — fabrication is this project's #1 failure mode).

## 0. TWO threads ran this session
**(A) "−1 dominance" prime-race investigation** — finished + synthesized. **(B) A NEW discovery
that spun out of it: ergodic optimization of Hecke BCZ return maps** (the live, valuable thread).

## 1. GIT / SAVE STATE (everything is committed)
- Repo root `/Users/za/Documents/Farey NOW` is a **local-only git repo (NO remote)** on `main`.
  HEAD = `4c20700`. All session work committed here (102+ files): `projects/minus1-dominance/**`,
  `projects/mimo-mini-project/**` (DISCOVERY, ESCAPE, CLOSED_FORM, GOAL_*, lean/, code/),
  `MACHINE_ACCESS.md`. **Parent has no remote by design → never pushed.**
- Submodule `primes-equispaced` (remote = **PUBLIC** github.com/SaarShai/Primes-Equispaced):
  - `formal-conjectures/Minus1Core.lean` — **PUSHED** (commit `ad1a164`, public, safe math).
  - `correspondence/KOYAMA.md` — committed **LOCAL ONLY** (`bd75801`, 1 ahead of origin) — sensitive
    (verbatim Koyama email + advance-fee/impersonation analyst note). **DO NOT PUSH** the submodule
    without per-action user confirmation (it would publish KOYAMA.md).
- Google-Drive `* (1)` conflict artifacts and `.git (1)/` are NOT tracked — never `git add -A`;
  add explicit paths and `git reset -- '*(1)*'`.
- Memory updated: `project_farey_forward_verdict`, `project_farey_lean_infra` (see those for infra).

## 2. Thread (A): −1 dominance — VERDICT + status
**Verdict (conditional GRH+LI; adversarially verified):** "−1 dominates among non-residues" is
FALSE/backwards — `a=−1` is the **LEAST**-biased non-residue (RS sign-density δ MINIMUM) because its
limiting variance `V(N;−1,1)` is the MAXIMUM. = **Fiorilli–Martin, Crelle 676 (2013), Thm 1.10**
(primary-verified). NR-vs-NR δ=1/2 (vacuous). Nothing unconditional over ℚ. Function-field escape
hatch CLOSED (Cha 2008: GSH provably violated; no unconditional analogue — see
`projects/minus1-dominance/FF_EXPLORATION.md`).
- DONE: `REPORT.md`, option-3 variance sweep (`compute_delta.py`/`sweep_variance.py` on M1: 4808
  primes q≡3 mod4 < 10⁵, **0 exceptions**, `sweep_results.tsv`+`sweep_plot.png`), `Minus1Core.lean`
  Lean-certified (EXIT=0, axioms `[propext, Quot.sound]`).
- **ONLY PENDING ITEM (the committed −1 /goal DoD):** finalize `projects/minus1-dominance/LEDGER.md`
  **§4** — needs the M2 sieve to finish. See §4 below.

## 3. Thread (B): THE DISCOVERY — Hecke BCZ ergodic optimization
Map `T_q(x,y)=(y,⌊(1+x)/(λy)⌋λy−x)`, `λ=2cos(π/q)`, on `{x>0,y>0,x+λy>1}`, observable `P=xy`.
`X(q)=inf_μ ess-sup_μ P` (ergodic-optimization "ground value"). q=3 = classical SL(2,ℤ)/Farey BCZ.
Three findings (write-up: `mimo-mini-project/DISCOVERY_Hecke_ergodic_optimization.md`,
`ESCAPE_FAMILY_hunt.md`, `CLOSED_FORM_Xq.md`; code `code/ergodic_hecke_hunt.py`):
1. **Optimizer = parabolic word `(1^{q−3},2)`** (q≥4; q=3 is `(1,4)`) = rotation-by-π/q + one defect.
2. **NO GROUND STATE — universal** across the Hecke family (inf approached at an OPEN cusp/floor
   boundary, never attained). **PROVEN in Lean for q=3,4** (`lean/BCZHecke_noGroundState_q3q4_VERIFIED.lean`,
   EXIT=0, axioms clean — `no_ground_state`, `g4_no_ground_state`, incl. the hard floor-=3 Middle
   case). Numerical+structural for q≥5. (Does NOT contradict Contreras 2016: his is compact/generic;
   this is non-compact escape-of-mass.)
3. **CLOSED FORM (proven, /goal #2 done, verified to <1e-30 vs independent boundary scan):**
   eigenvector `v_n=sin((n+1)π/q)`; cusp always binds → `s_lo=1/(2sin(2π/q))`; so
   `X(q)=maxprod/(4sin²(2π/q))`, with branches **q even:** `1/(8 sin(π/q) sin(2π/q))`, **q odd:**
   `cos²(π/2q)/(4 sin²(2π/q))`, q=3 special `2/9`. **X minimized at q=4 = √2/8**; strictly
   increasing, →∞. The even/odd split = why no single elementary formula.
HONEST scope: X(q) is a rigorous UPPER bound ∀q (explicit family); EXACT+no-GS PROVEN only q=3,4;
optimal word search-verified q=4..10; exact/no-GS q≥5 CONJECTURAL.

## 4. LIVE COMPUTE (still running — check first)
- **M2 sieve** `alicia@192.168.1.92:~/farey-sieve/` → `curve_3e14.tsv` (`mr1_par`, caffeinated).
  At handoff ~170/224 chunks; late chunks slow (~5.6e3 s); writes output only AT COMPLETION. Check:
  `pgrep -fl mr1_par; grep -c "chunk.*done" run.log; ls -la curve_3e14.tsv`.
- **M1 replication** `new@192.168.1.22:~/farey-sieve-m1/` → `curve_m1_3e14.tsv` (independent, T=9,
  ~91/224) — for a frontier integer cross-check vs M2.
- **WHEN M2's curve lands** (the −1 DoD): `scp` it to `projects/minus1-dominance/`, run
  `python3 minus1_curve_analysis.py curve_3e14.tsv` (Part A: integer cross-check vs `out2.tsv` at the
  9 shared checkpoints 1e9–1.3e13, must match EXACTLY; Part B: RS-normalized `V(N;a,1)` over the grid
  — does `a=−1` become variance-MAX for **N=19,23** at the 3e14 onset?). Then
  `python3 compare_curves.py curve_m1_3e14.tsv curve_3e14.tsv` (M1-vs-M2 integer match). Finalize
  `LEDGER.md §4`. (Free-check baseline already done: at ≤1.3e13, −1 NOT variance-max for any N —
  onset not reached. `minus1_curve_analysis.py`/`compare_curves.py` parser-validated, ready.)

## 5. THREE spun-off /goal directions (separate sessions) — status
- **#2 closed form — DONE** (`CLOSED_FORM_Xq.md`, verified; see §3.3). Prompt: `GOAL_2_closed_form.md`.
- **#1 general-q theorem** (no-GS + X(q)=inf ∀q; paper proof → Lean). Prompt: `GOAL_1_general_theorem.md`.
  In progress in a parallel session (search files `code/hunt_*.py`, `code/inf_direct.py`).
- **#7 arithmetic meaning** (X(q) = sharp Diophantine gap-product constant for `G_q`-Farey; q=3 = the
  proven 2/9 cap). Prompt: `GOAL_7_arithmetic_meaning.md`. In progress (`code/G4_hecke_farey_*.py`,
  `code/Gq_hecke_farey_general.py`). Each GOAL_*.md is a self-contained `/goal` body.

## 6. WHAT A NEW SESSION SHOULD DO (pick one)
- **(default) Finish the committed −1 /goal:** poll the M2 sieve; when `curve_3e14.tsv` exists, run
  the §4 analysis above + finalize `LEDGER.md §4` + report. This is the only open item from the
  original goal.
- **OR advance the discovery:** continue #1 (general theorem — highest value, converts discovery→
  theorem; q=4 Lean template in `BCZHecke_noGroundState_q3q4_VERIFIED.lean`) or #7 (arithmetic
  meaning), reading the corresponding `GOAL_*.md`. Don't duplicate a session already running.
- **OR write-up:** internal paper draft combining #1+#2+#7 (external sharing = USER-gated).

## 7. INFRA / CONSTRAINTS (read before acting)
- **Lean:** in-tree `primes-equispaced/.lake` Mathlib is **GUTTED** (source deleted) — do NOT compile
  there. Use a throwaway full-Mathlib v4.28.0 in `/tmp`: lakefile requiring mathlib `rev=v4.28.0` +
  `lean-toolchain` v4.28.0; `~/.elan/bin/lake update` + `lake exe cache get` (→ ~7655 oleans);
  `( ~/.elan/bin/lake env lean F.lean 2>&1; echo EXIT=$? )`. (`/tmp/lean-minus1` may still have it.)
  Gotchas: `include … in` BEFORE the docstring; `le_or_gt` (not `le_or_lt`); `Int.floor_eq_iff` no
  side-arg. `#print axioms` must be `[propext, Classical.choice, Quot.sound]` (no `sorryAx`).
- **Fleet:** `MACHINE_ACCESS.md` — M1 `new@192.168.1.22`, M2 `alicia@192.168.1.92`, key
  `~/.ssh/id_ed25519`; Wi-Fi DHCP IPs DRIFT (re-discover per that file). Long jobs
  `caffeinate -i nohup CMD > log 2>&1 &`. Kaggle wired if more CPU. Compute offload = INTERNAL.
- **Hard rules:** never send outbound / publish / contact Koyama (USER-driven); never push the
  PUBLIC submodule without per-action confirmation (KOYAMA.md is local-only there); never
  commit/push/change git/hooks unless the user explicitly asks; `~/Documents` is Drive-synced — no
  folder/`.git` move/rename/delete without confirmation, treat `* (1)` as conflict artifacts.

## 8. KEY FILES (quick map)
- −1: `projects/minus1-dominance/{REPORT,LEDGER,FF_EXPLORATION}.md`, `minus1_curve_analysis.py`,
  `compare_curves.py`, `sweep_variance.py`/`sweep_results.tsv`/`sweep_plot.png`, `Minus1Core.lean`,
  `compute_delta.py`, primary texts (`FM_text.txt` Thm 1.10 @L324, `AK_text.txt`, `PNR_text.txt`).
- Discovery: `projects/mimo-mini-project/{DISCOVERY_Hecke_ergodic_optimization,ESCAPE_FAMILY_hunt,
  CLOSED_FORM_Xq}.md`, `code/ergodic_hecke_hunt.py`, `code/Xq_closedform_verify.py`,
  `lean/BCZHecke_noGroundState_q3q4_VERIFIED.lean`, `lean/RESULTS_VERIFIED_2026-06-02.md`.
- Goal prompts: `projects/mimo-mini-project/GOAL_{1,2,7}_*.md`.
- This handoff: `projects/mimo-mini-project/HANDOFF_2026-06-02_session.md`.

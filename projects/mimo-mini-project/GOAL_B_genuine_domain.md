# /goal B — The genuine natural-extension domain: is the Hecke ergodic optimization well-posed for ALL q?

> Paste the body below into `/goal` in a fresh session. Self-contained. Work autonomously; verify
> with results/Lean (trust `EXIT=` lines, NOT task-notification summaries); send NOTHING outward
> (USER-gated). Adversarial honesty: separate PROVEN / NUMERICAL / CONJECTURAL; verify every citation
> against the primary text (fabrication is this project's #1 failure mode).

## MISSION
Resolve the question the q≥12 retraction exposed: **is the Hecke BCZ ergodic optimization a real
all-q phenomenon, or genuinely q=3-special?** The naive triangle `D = {x>0,y>0,x+λy>1}` is invariant
under `T_q` ONLY for q=3 — for every q≥4 ~100% of generic seeds ESCAPE D (a known Rosen/Hecke
continued-fraction natural-extension fact). So `X(q)=inf esssup P` on the naive D is ill-posed for
large q (no feasible parabolic orbit exists past q=11). Rebuild the optimization on the **TRUE
natural-extension domain** Ω_q of the genuine Hecke BCZ map (Taha / Rosen λ-CF), and determine:
1. For each q, what is the correct return-map domain Ω_q and the correct observable?
2. Does a well-defined `X(q) = inf_μ esssup_μ P` exist on Ω_q for ALL q (rescuing the "all q" story),
   and is it still approached-but-not-attained (no ground state)?
3. If yes, what is X(q) on Ω_q (does it match the q≤11 closed form, or differ)? If no, prove the
   phenomenon is q=3-special (or q∈{3,4,6}-special, the arithmetic Hecke groups).

This is the deepest open question; it determines whether goals A/#2/#7 generalize. Hardest of the
three. A clean NEGATIVE (q=3-special, proven) is as valuable as a positive.

## BACKGROUND — what is established (read the corrected docs first)
- The naive map `T_q(x,y)=(y,⌊(1+x)/(λy)⌋λy−x)`, `λ=2cos(π/q)`, `P=xy`. On naive D the parabolic
  word `(1^{q−3},2)` (orbit `c_n=R sin((n+1)π/q)`) is the optimizer but is FEASIBLE only q≤11
  (q=12 degenerate `s_lo=s_hi`, q≥13 empty scale window — `svalid_range` returns None).
- **Measured:** naive D invariant only for q=3; ≈100% seed-escape for all q≥4 (vs 0% q=3). This is
  the Rosen/Hecke subtlety: for non-arithmetic q the natural-extension domain is a PROPER subset with
  a non-triangular ("staircase"/fractal-boundary) shape.
- **Genuine map (prior art, in repo):** Taha, "The BCZ map analogue for the Hecke triangle groups
  `G_q`" (arXiv:1810.10668) — defines `BCZ_q` as the return map of the horocycle flow to a Poincaré
  section, with next-term `c_{n+1} = a_n·λ·c_n − c_{n−1}` (Rosen λ-CF convergent recurrence; the `·λ`
  coefficient, confirmed 3 ways in `prior_art_taha_cobeli.md`). The genuine domain is Taha's section
  Ω_q, NOT the naive triangle.
- **#7's genuine cusps:** `code/Gq_hecke_farey_general.py` generates GENUINE `G_q`-Farey cusps via
  exact ℤ[λ] arithmetic + Galois-height bound — the static/arithmetic shadow of Ω_q. On these,
  cluster bound `C(q)=2,2,3,5` (q=3..6), dets ∈{1,λ}(q=4,5)/{1,√3,2}(q=6), and the X(q) values
  `√2/8,1/4,√3/6` DO appear as sharp floors. So the arithmetic object is real for q≥4 even though the
  naive DYNAMICS escape — the genuine domain is where they reconcile.

## THE CORE TASK
1. **Construct Ω_q explicitly** for q=4,5,6,7 (at least): the true natural-extension domain of the
   Rosen λ-CF / Taha `BCZ_q`. Use Rosen's λ-continued-fraction natural extension (Burton–Kraaikamp–
   Schmidt; Nakada-style natural extensions for Hecke groups). Verify INVARIANCE numerically: seeds in
   Ω_q stay in Ω_q under `BCZ_q` (the test naive D fails for q≥4).
2. **Define the observable + optimization on Ω_q.** Translate `P=xy` (= `1/(Q²·gap)` in Farey terms)
   to the genuine coordinates. Compute `X_Ω(q) = inf_μ esssup_μ P` over `BCZ_q`-invariant measures
   numerically (recurrent-orbit / periodic-word search IN Ω_q).
3. **Compare** `X_Ω(q)` to the naive closed form V(q): equal for q≤11? Defined and finite for q≥12?
   Is the no-ground-state (escape-to-cusp) structure preserved on Ω_q?
4. **Verdict:** all-q phenomenon on the genuine domain (state X_Ω(q), no-GS) OR q=3-special /
   {3,4,6}-special (prove the obstruction). Either way, give the precise reason.

## METHOD NOTES / PITFALLS (learned this project)
- Random-seed iteration of the NAIVE map is useless for q≥4 (escapes). Use either (a) the genuine
  Ω_q with verified invariance, or (b) periodic-word / parabolic-family search (all periodic orbits
  in any invariant domain are trace-2 scale-free families = closed horocycles).
- `svalid_range` (in `ergodic_hecke_hunt.py`) is the trustworthy feasibility check (computes the
  floor UPPER bound s_hi); `Xq_exact_for_word` is NOT (s_lo only — this is what produced the bogus
  q≥12 values). Always feasibility-check.
- The genuine domain for non-arithmetic q has a fractal/“staircase” boundary (Rosen–Schmidt); don't
  assume a polygon. For the ARITHMETIC q∈{3,4,6} (Takeuchi) the structure is cleanest — start there.

## KEY FILES (`/Users/za/Documents/Farey NOW/`)
- `projects/mimo-mini-project/FINDINGS_corrected_2026-06-02.md` — the retraction + escape measurement (read FIRST).
- `projects/minus1-dominance/.. ` n/a. `prior_art_taha_cobeli.md` (repo root or memory) — Taha `BCZ_q` def + Rosen λ-CF recurrence.
- `projects/mimo-mini-project/code/Gq_hecke_farey_general.py` — genuine ℤ[λ] cusp generator (#7); the arithmetic shadow of Ω_q.
- `projects/mimo-mini-project/research_notes/ARITHMETIC_MEANING_Xq.md` — #7: X(q) as gap-product constant on genuine cusps; cluster law C(q).
- `projects/mimo-mini-project/DISCOVERY_Hecke_ergodic_optimization.md` (retraction banner) + `CLOSED_FORM_Xq.md` — the naive-D results to compare against.
- `projects/mimo-mini-project/code/ergodic_hecke_hunt.py` — `orbit_direction`, `svalid_range`, `monodromy`, `lam`.

## CITATIONS (verify vs primary before citing)
- M. D. Taha, arXiv:1810.10668 — `G_q` BCZ map / Poincaré section. (Already in `prior_art_taha_cobeli.md`.)
- D. Rosen, "A class of continued fractions associated with certain properly discontinuous groups",
  Duke Math. J. 21 (1954) — Rosen λ-CF.
- R. M. Burton, C. Kraaikamp, T. A. Schmidt, "Natural extensions for the Rosen fractions",
  Trans. AMS 364 (2012) — the natural extension domains Ω_q (THE key reference; verify exact form).
- H. Nakada, natural extensions (Tokyo J. Math 1981) — method. K. Takeuchi, J. Math. Soc. Japan 29
  (1977) — Hecke arithmetic ⟺ q∈{3,4,6,∞}. Athreya–Cheung, IMRN 2014 (arXiv:1206.6597).

## LEAN / FLEET / CONSTRAINTS
- Lean (if any formal claim): throwaway full-Mathlib v4.28.0 at `/tmp/lean-minus1` (8018 oleans);
  `( ~/.elan/bin/lake env lean F.lean 2>&1; echo EXIT=$? )`; `#print axioms` must be
  `[propext, Classical.choice, Quot.sound]`. This goal is mostly PAPER+NUMERICAL; Lean optional.
- Fleet: `MACHINE_ACCESS.md` (M1 `new@192.168.1.22`, M2 `alicia@192.168.1.92` — ⚠ M2 busy with the
  −1 sieve, prefer M1). Kaggle token currently 401 (needs refresh).
- Hard rules: nothing outbound/published/contacted (USER-gated); no commit/push/git changes unless
  asked; `~/Documents` Drive-synced (no folder/`.git` moves; `* (1)` = conflict artifacts);
  PROVEN/NUMERICAL/CONJECTURAL strictly separate.

## DEFINITION OF DONE
- Explicit Ω_q for q=4,5,6,7 with NUMERICALLY VERIFIED invariance under `BCZ_q` (the test naive D fails).
- `X_Ω(q) = inf esssup P` on Ω_q computed for those q; comparison to the naive V(q); whether it is
  defined/finite for q≥12; whether no-ground-state (escape-to-cusp) survives on Ω_q.
- A clear VERDICT with proof or precise evidence: all-q phenomenon (give X_Ω(q) + no-GS) OR
  q=3- / {3,4,6}-special (give the obstruction). Honest scope. Nothing sent outward.

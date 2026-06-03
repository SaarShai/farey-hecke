# /goal #2 — A closed form / geometric formula for X(q) (Chebyshev / cusp-width)

> Paste the body below into `/goal` in a fresh session. Self-contained. Work autonomously, verify
> with results (high-precision mpmath + PSLQ; cross-check vs the X(q) table), send NOTHING outward.
> Adversarial honesty: a *clean uniform formula* must match ALL computed q to many digits, or be
> proven from the orbit structure — otherwise report the honest negative + best characterization.

## MISSION
Find and PROVE a uniform closed-form (or clean geometric) expression for the Hecke
ergodic-optimization infimum `X(q)`, exploiting that the optimizer is **rotation-by-π/q with one
defect** (Chebyshev structure). Determine definitively whether `X(q)` has a uniform formula in
`λ_q=2cos(π/q)` / the cusp width; if no uniform *elementary* form exists (current evidence), give
the cleanest uniform expression (e.g. a Chebyshev-U ratio, a cusp-width formula, or an implicit
characterization) and prove it.

## THE OBJECT + WHAT IS KNOWN (this session, 2026-06-02)
- `λ=2cos(π/q)`; map `T_q(x,y)=(y,⌊(1+x)/(λy)⌋λy−x)` on `{x>0,y>0,x+λy>1}`; `P=xy`;
  `X(q)=inf_μ ess-sup_μ P`.
- **Optimizer = parabolic word** `(1^{q−3},2)` (period q−2), q≥4; q=3 is `(1,4)`. Monodromy
  `M(k)=[[0,1],[-1,kλ]]`; the word's monodromy has trace 2 (eigenvalue 1) ⇒ scale-free family
  `a_n(s)=s·v_n`, `v` = the eigenvector. The all-1 recurrence `a_{n+2}=λa_{n+1}−a_n` is **rotation
  by θ=π/q**: its solutions are `a_n = A·sin(nθ)+B·cos(nθ)` (Chebyshev `U_n(cosθ)=sin((n+1)θ)/sinθ`).
  The single `2` is the defect that closes the period-(q−2) orbit.
- `X(s) = s²·max_n(v_n v_{n+1})`; the valid s-range `(s_lo, s_hi]` comes from floor-consistency
  `⌊(1+s v_n)/(λ s v_{n+1})⌋=k_n` + triangle `s(v_n+λ v_{n+1})>1`; `X(q)=s_lo²·max_n(v_n v_{n+1})`
  (inf at the OPEN lower boundary `s_lo`). The binding at `s_lo` is either the cusp edge
  `x+λy=1` (triangle) or a floor-jump. See `code/ergodic_hecke_hunt.py` (`Xq_exact_for_word`,
  `svalid_range`) for the exact logic.
- **Computed values (exact, mpmath):** X(3)=2/9, X(4)=√2/8 (GLOBAL MIN), X(5)=1/4, X(6)=√3/6,
  X(7)=0.388739533…, X(8)=½cos(π/8), X(9)=0.586824…, X(10)=½cot(π/5), X(11)=0.837985…,
  X(12)=cos(π/12); strictly increasing for q≥4, →∞ (X(200)≈253). Full table to q=30 reproducible
  via `code/ergodic_hecke_hunt.py`.
- **Current PSLQ status:** the integer relations among {X(q),1,cos(π/q),cos²,cos³} DIFFER per q
  (e.g. X(4)=cos³(π/4)/2; X(8)=½cos(π/8); X(10)=½cot(π/5); X(12)=cos(π/12)) ⇒ **no single uniform
  elementary formula in cos(π/q) found** — but the rotation structure strongly suggests a uniform
  expression via Chebyshev-U ratios or the cusp width. THAT is what to derive.

## APPROACH
1. **Derive the eigenvector v(q) and the orbit in closed form** from the rotation recurrence: with
   `θ=π/q`, the all-1 segments give `a_n ∝ sin((n+φ)θ)`; impose the single-`2` defect + periodicity
   (period q−2) to solve for the phase φ and the closure. Express `v_n = sin((n+φ)θ)/sinθ` (or
   Chebyshev `U`-values). The eigenvector of the parabolic monodromy is explicit.
2. **Compute `s_lo` and `max_n(v_n v_{n+1})` in closed form.** Determine which constraint binds (the
   cusp edge `x+λy=1` vs the floor-jump) as a function of q — likely a clean q-pattern (the data
   alternates). Then `X(q) = s_lo²·max(v_n v_{n+1})` becomes an explicit trig/Chebyshev expression.
   Candidate forms to test to 40+ digits against ALL q (and prove): Chebyshev-U ratios
   `U_a(λ/2)/U_b(λ/2)` with `U_n(cos θ)=sin((n+1)θ)/sinθ`; tan/cot of rational multiples of π/q
   (note `X(10)=½cot(π/5)`, `X(6)=½cot(π/3)` fit `½cot(2π/q)` but q=8 does not — investigate why,
   likely the binding type changes); a cusp-width expression in `λ_q`.
3. **Settle the uniform-formula question.** Either (a) a single uniform closed form matching all q
   (PROVE it from step 1–2), or (b) a uniform expression *conditioned on binding type* (two
   sub-formulas, triangle vs floor-jump, each proven), or (c) a rigorous statement that `X(q)` is an
   explicit algebraic number of growing degree with NO uniform elementary form, plus the cleanest
   uniform implicit characterization (e.g. `X(q)=` the product `xy` at the unique cusp-edge point of
   the rotation-defect orbit — a uniform GEOMETRIC formula even if not elementary).
4. **Cross-check** every candidate to ≥40 digits via `mpmath` against `Xq_exact_for_word`, and use
   `mp.pslq`/`mp.identify` carefully (enough digits to avoid spurious relations — the #1 risk).
   Re-derive q=3 (special word `(1,4)`) separately.

## KEY FILES (in `/Users/za/Documents/Farey NOW/`)
- `projects/mimo-mini-project/code/ergodic_hecke_hunt.py` — `Xq_exact_for_word(q,word)` (high-prec
  X for a word), `hunt(q)`, `svalid_range` (the binding logic), `monodromy`, `orbit_direction`.
- `projects/mimo-mini-project/DISCOVERY_Hecke_ergodic_optimization.md` — X(q) table + scope + the
  per-q PSLQ findings (the clean values and the non-uniformity).
- `projects/mimo-mini-project/ESCAPE_FAMILY_hunt.md` — the criterion + binding-type notes.
- `projects/mimo-mini-project/lean/BCZHecke_noGroundState_q3q4_VERIFIED.lean` — proven X(3)=2/9,
  X(4)=√2/8 (the closed form must reproduce these and the no-ground-state boundary structure).

## TOOLS
- `mpmath` (set `mp.mp.dps=60+`), `mp.pslq`, `mp.identify`. Chebyshev: `U_n(cosθ)=sin((n+1)θ)/sinθ`.
- Fleet (`MACHINE_ACCESS.md`: M1 `new@192.168.1.22`, M2 `alicia@192.168.1.92`, key
  `~/.ssh/id_ed25519`, IPs DRIFT) for high-precision sweeps over many q / large-degree PSLQ.
- If a Lean-checkable identity emerges: throwaway full-Mathlib v4.28.0 in `/tmp` (the in-tree
  primes-equispaced Mathlib is GUTTED — do not use it); `lake update` + `lake exe cache get`; trust
  `EXIT=`.

## REFERENCES (verify before citing)
- Hecke groups + λ=2cos(π/q): E. Hecke (1936); D. Rosen, λ-continued fractions (1954).
- Chebyshev polynomials of the second kind `U_n` — standard.
- BCZ map: Boca–Cobeli–Zaharescu, J. reine angew. Math. 535 (2001); Athreya–Cheung, IMRN 2014
  (cusp width / horocycle return — relevant if X(q) ties to the cusp geometry).
- Takeuchi, "Arithmetic triangle groups", J. Math. Soc. Japan 29 (1977) — arithmeticity q∈{3,4,6,∞}
  (note: clean values at q=4,6,12 may correlate with arithmetic/cyclotomic structure — investigate).

## CONSTRAINTS (hard)
- Never send outbound / publish — USER-driven. Never commit/push/change git/hooks unless asked.
- `~/Documents` Google-Drive-synced: no folder/`.git` move/rename/delete without per-action
  confirmation; `* (1)` files are conflict artifacts.
- Adversarial honesty: a claimed closed form MUST match all computed q to many digits AND be
  derived/proven; use enough PSLQ precision to avoid spurious relations; if no uniform elementary
  form, SAY SO and give the proven geometric/implicit characterization instead. Do not overclaim.

## DEFINITION OF DONE
- Either: a PROVEN uniform closed form for X(q) (matching all q to ≥40 digits, derived from the
  rotation/parabolic structure), possibly split by binding type; OR a proven uniform GEOMETRIC /
  Chebyshev-ratio / cusp-width characterization; OR a rigorous demonstration that no uniform
  elementary form exists + the best uniform implicit form. In all cases: the closed-form derivation
  of the explicit values X(3)=2/9, X(4)=√2/8, X(5)=1/4, X(6)=√3/6 from the general expression.
- Results doc + honest report to the user. Nothing sent outward.

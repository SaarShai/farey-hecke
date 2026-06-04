# Farey / Stern–Brocot library → Mathlib PR — HANDOFF

Fresh session, **no prior context**. Everything you need is here. Work under `/goal`: finish the
library and stage a Mathlib PR — **but do NOT submit/push/open-PR (user-driven).**

## MISSION
Complete the Farey / Stern–Brocot Lean 4 library and prepare a Mathlib PR. The genuinely
**novel-to-Lean** contribution is the **Farey sequence as an object** + its neighbour theorem +
`|Fₙ| = 1 + Σ_{k=1}^n φ(k)`. Verified ABSENT from Mathlib (Mathlib has continued-fraction
*convergents* and the convergent determinant identity + Legendre's theorem — but those are about the
convergents of *one real*, a DIFFERENT object from the Farey sequence of order n; do NOT re-prove
them).

Honest scope (state it, don't overclaim): foundational **formal-math infrastructure** for the
Lean/Mathlib number-theory community; modest audience; **not** new mathematics. The value is filling
a missing classical object.

## CURRENT STATE (done, sorry-free, checks against Mathlib v4.28.0)
Two standalone files (compiled via `lake env lean`, NOT yet a lake package):
- `/Users/za/Documents/Farey NOW/projects/farey-lean/Farey/Mediant.lean` — the mediant / unimodular
  core: `det`, `Unimodular` (`b*c-a*d=1`), `det_mediant_left/right`, `Unimodular.mediant_left/right`,
  `Unimodular.isCoprime_mediant`, `mediant_strictAnti_left`/`mediant_strictMono_right`,
  `Unimodular.ad_lt_cb`; the chain layer `Frac`/`medFrac`/`Adj`/`IsFareyChain`/`isFareyChain_base`/
  **`isFareyChain_insert_mediant`** (mediant insertion preserves unimodular adjacency); the
  denominator bound **`Unimodular.den_ge_of_strictBetween`** + `not_strictBetween_of_den_le`; and the
  **gap formula `Unimodular.rat_sub`** (`c/d - a/b = 1/(b*d)`).
- `/Users/za/Documents/Farey NOW/projects/farey-lean/Farey/Neighbour.lean` —
  **`neighbour_unimodular`** = the Farey neighbour theorem (Hardy–Wright Thm 28): consecutive Farey
  fractions are unimodular. Currently stated on abstract integer pairs `(a,b,c,d)` with a
  "no fraction `x/y`, `0<y≤n`, strictly between" hypothesis.
- `README.md`, `lean-toolchain`.

## WORK TO DO (in order)
1. **`|Fₙ| = 1 + Σ_{k=1}^n φ(k)`** (headline missing-from-Mathlib result). Define `Fₙ` as a
   `Finset ℚ` = reduced rationals in `[0,1]` with `den ≤ n`; prove its cardinality via `Nat.totient`.
   Sanity: `|F₁|=2, |F₂|=3, |F₃|=5`. This is likely the hardest new lemma — the `ℚ`↔coprime-pair
   bijection + the totient count. DE-RISK on paper first; use Aristotle for the counting bijection if
   it resists. Mathlib hooks: `Nat.totient`, `Nat.totient_eq_card_coprime`/`Nat.totient_eq_card_lt_and_coprime`,
   `Rat.num`/`Rat.den`/`Rat.reduced`, `Finset.card_biUnion`/`card_image_of_injective`.
2. **(Recommended) restate the neighbour theorem on the actual `Fₙ` object** (consecutive elements of
   the sorted `Fₙ` Finset are unimodular), so it's the "real" Farey neighbour theorem, not the
   abstract-pair version. Reuse `den_ge_of_strictBetween` + the mediant lying strictly between.
3. **Polish to Mathlib standards** (see conventions).

## MATHLIB CONVENTIONS (follow exactly — this is for an upstream PR)
- **Minimal imports** — NOT `import Mathlib`; import only the needed modules.
- **Naming:** defs `lowerCamelCase`, types `UpperCamelCase`, theorems descriptive; match neighbouring
  NT files (`Mathlib/NumberTheory/DiophantineApproximation/`, `Mathlib/Algebra/ContinuedFractions/`).
- **Docstring on every public declaration**; a module docstring with `## Main results` + `## References`.
- **Apache-2.0 copyright header** (copy the exact format from any Mathlib file; authors = the user).
- Likely path: `Mathlib/NumberTheory/Farey/Basic.lean` (+ `Neighbour.lean`). Unify the two files into a
  coherent module with proper imports.
- Sorry-free; `#print axioms` = `[propext, Classical.choice, Quot.sound]`; **0 warnings**; avoid
  banned/heavy tactics where reasonable.

## BUILD & VERIFY (discipline)
- Develop against Mathlib v4.28.0:
  `cd "/Users/za/Documents/Farey NOW/primes-equispaced" && ( ~/.elan/bin/lake env lean "<file>" 2>&1; echo "EXIT=$?" ) > /tmp/farey.out 2>&1`
  then **Read `/tmp/farey.out` and trust the `EXIT=` line, NOT the task-notification summary** (it has
  falsely reported "exit 0"). `import Mathlib` ≈ 80–90 s; one lemma per compile.
- For the actual PR the files must build against **current Mathlib master** (rebase + `lake exe cache get`);
  do that LAST, after development against v4.28.0.

## ORCHESTRATION
- Subagents (Agent tool): Mathlib API search, the `|Fₙ|` paper-proof, adversarial verification.
  CONSTRAINTS: local only, **no external sends, no git commit/push, no person names, NEW files only.**
- Aristotle = the project's automated Lean prover via a **user-submitted web workflow**. For the
  `|Fₙ|` counting bijection if it resists, prepare a clean sorry-quarantined dispatch package (mirror
  `projects/aristotle_dispatch_v*/`) and **ask the user to submit** (you cannot submit).
- M1/M2 = the user's machines for compute (creds template: `m1-m2-handoff.md`); run scripts foreground.

## HARD CONSTRAINTS
- **Never commit / push / open a PR / post to Zulip autonomously** — all outward steps are
  USER-DRIVEN. You prepare PR-ready files + a PR description; the user submits.
- **Before any PR, re-check current Mathlib master for a Farey sequence** (it could have landed) + a
  Zulip "Is-there-code-for-X?" check. If upstream already has it, STOP and report.
- Never change git config; never skip hooks.

## PRIOR ART / HONESTY (project's #1 failure mode = overclaiming + fabricated citations)
- Mathlib already has: convergent determinant identity (`ContinuedFractions/Determinant.lean`) and
  Legendre's theorem (`DiophantineApproximation/Basic.lean`) — do NOT re-prove. Our Farey-sequence
  object + neighbour theorem + `|Fₙ|` are genuinely new to Lean.
- Cite Hardy–Wright (neighbour theorem = Thm 28), the Stern–Brocot tree, standard Farey references.
  Verify every citation against a primary source; mark anything unverified.

## DEFINITION OF DONE
Complete library — mediant/unimodular core + neighbour theorem (ideally on the `Fₙ` object) + gap
formula + `|Fₙ| = 1 + Σφ(k)` — unified into a clean Mathlib-style module, minimal imports, sorry-free,
`#print axioms` clean, 0 warnings, docstrings + license headers, duplication-checked vs current
master, plus a drafted PR description. **Staged, NOT submitted.** Report honestly: what's proved, the
honest scope, the citations.

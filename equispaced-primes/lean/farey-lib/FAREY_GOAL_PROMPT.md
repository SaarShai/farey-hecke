GOAL: Finish the Farey / Stern-Brocot Lean 4 library and STAGE (do NOT submit) a Mathlib PR. Work autonomously until it is complete, sorry-free, `#print axioms` shows only [propext, Classical.choice, Quot.sound], 0 warnings, and Mathlib-style.

FIRST ACTION - read these in full; they contain ALL instructions, current state, conventions, the lemma plan, orchestration, and constraints:
- /Users/za/Documents/Farey NOW/projects/farey-lean/FAREY_PR_HANDOFF.md   (the full handoff)
- /Users/za/Documents/Farey NOW/projects/farey-lean/Farey/Mediant.lean    (done: mediant/Unimodular core, chain, den-bound, gap formula)
- /Users/za/Documents/Farey NOW/projects/farey-lean/Farey/Neighbour.lean  (done: neighbour theorem, Hardy-Wright Thm 28)

HEADLINE TASK: add |F_n| = 1 + sum_{k=1}^n phi(k) (define F_n as a Finset of reduced rationals in [0,1] with denominator <= n; count via Nat.totient; sanity |F_1|=2,|F_2|=3,|F_3|=5) - the genuinely missing-from-Mathlib result and the hardest new lemma. Then restate the neighbour theorem on the actual F_n object. Then polish to Mathlib standards (minimal imports - NOT `import Mathlib`; docstrings on every public decl; module docstring with Main results + References; Apache-2.0 headers; unify into one clean module). The Farey SEQUENCE object is verified absent from Mathlib; do NOT re-prove Mathlib's existing continued-fraction determinant or Legendre's theorem (different object).

COMPILE: cd "/Users/za/Documents/Farey NOW/primes-equispaced" && ( ~/.elan/bin/lake env lean "<file>" 2>&1; echo "EXIT=$?" ) > /tmp/farey.out 2>&1 -- then READ /tmp/farey.out and trust the EXIT= line, NOT the task-notification summary (it has falsely said "exit 0"). ~80-90s per compile; one lemma at a time.

NON-NEGOTIABLE: never commit / push / open-PR / post to Zulip autonomously - ALL outward steps are user-driven (you prepare PR-ready files + a PR description; the user submits). Never change git config; never skip hooks. Before any PR, check current Mathlib master + Zulip for an existing Farey sequence; if it exists upstream, STOP and report. Honest framing only: foundational formal-math infrastructure for the Lean/Mathlib number-theory community, modest audience, NOT new mathematics; verify every citation (this project has a fabrication history); cite Hardy-Wright + Stern-Brocot.

ORCHESTRATE: subagents (local only; NO external sends, NO commits/push, NO person names, NEW files only) for Mathlib API search, the |F_n| paper proof, and adversarial verification; the user-submitted Aristotle web workflow for the |F_n| counting bijection if it resists (prepare a clean sorry-quarantined package and ASK the user to submit); M1/M2 = the user's machines (creds: m1-m2-handoff.md), run scripts foreground. All details, conventions, and the definition of done are in FAREY_PR_HANDOFF.md.

DONE = complete library (mediant core + neighbour theorem on F_n + gap formula + |F_n| count), unified Mathlib-style module, minimal imports, sorry-free, #print axioms clean, 0 warnings, docstrings + license headers, duplication-checked vs current master, PR description drafted - STAGED, not submitted. Report honestly: what's proved, the scope, the citations.

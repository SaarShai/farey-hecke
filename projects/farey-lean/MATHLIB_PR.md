# Mathlib PR package — the three-gap (Steinhaus) theorem

Everything needed to submit `Farey/ThreeGap.lean` to Mathlib. Status below distinguishes what is
**done**, what **only you can do**, and the **exact commands** for the rest.

---

## ✅ Done (in `Farey/ThreeGap.lean`)
- Full `three_gap` theorem, `sorry`-free, `#print axioms` = `propext, Classical.choice, Quot.sound`.
- 0 warnings; every line ≤ 100 columns (Mathlib's hard limit).
- Docstrings on all public declarations.
- Faithfulness + duplication audited (three-gap absent from current Mathlib master).

## 🔒 Only you can do (legal / identity)
1. **Confirm the author name** for the Apache header (best guess: `Saar Shai`).
2. **Sign the Mathlib CLA** — when the PR opens, the `CLA-bot` comments a link; you click to agree.
   This is a legal act under your name; I will not do it for you. (Note: this is the *leanprover-community*
   CLA, separate from the Google CLA you signed for `formal-conjectures`.)
3. **Approve opening the public PR** under `SaarShai`.

## ⚙️ Mechanical, can be scripted (commands below)
Fork → clone (outside `~/Documents`) → cache → place file → header/namespace/imports → build → lint
→ commit → push → open PR.

---

## Header to prepend (replace the current module docstring block)

```lean
/-
Copyright (c) 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Saar Shai
-/
import Mathlib   -- TODO: minimize (see step 6)

/-!
# The three-gap (Steinhaus / three-distance) theorem

For irrational `α` and any `N`, the points `{0·α}, …, {(N-1)·α}` on the circle `ℝ ⧸ ℤ` split it
into arcs taking at most **three** distinct lengths (`three_gap`).

## Main results
* `ThreeGap.three_gap` : `(Finset.univ.image (gap hα)).card ≤ 3`.

## Implementation notes
We use the concrete representatives `x α k = Int.fract (k·α) ∈ [0,1)` (a `LinearOrder`, so the
sorted point set and its gaps are available via `Finset.orderEmbOfFin`), and Liang's rigid-gap
argument re-cast through the *oriented forward distance* `fwdDist a c = Int.fract ((c-a)·α)`.

## References
* J. H. Liang, *A short proof of the 3d distance theorem*, Discrete Math. 28 (1979) 325–326.
* Prior formalization (Coq): M. Mayero, *The Three Gap Theorem (Steinhaus Conjecture)*, TYPES'99
  (2000); arXiv:cs/0609124.
-/
```
Also: change `namespace Farey.ThreeGap` → `namespace ThreeGap`, and **delete** the
`#print axioms three_gap` line (Mathlib forbids `#`-debug commands in library files).

Proposed path: `Mathlib/NumberTheory/ThreeGapTheorem.lean` (maintainers may prefer
`Mathlib/Dynamics/`; easy to move).

---

## Runbook (gh is already authenticated as `SaarShai`)

```bash
# 1. Fork (one-time)
gh repo fork leanprover-community/mathlib4 --clone=false

# 2. Clone OUTSIDE Google Drive (never build Mathlib inside ~/Documents)
mkdir -p ~/code && cd ~/code
git clone https://github.com/SaarShai/mathlib4.git
cd mathlib4
git remote add upstream https://github.com/leanprover-community/mathlib4.git
git fetch upstream
git checkout -b three-gap-theorem upstream/master   # branch off the LATEST master

# 3. Prebuilt cache (so you don't compile Mathlib from source)
lake exe cache get

# 4. Place the file + apply the header edits above
cp "/Users/za/Documents/Farey NOW/projects/farey-lean/Farey/ThreeGap.lean" \
   Mathlib/NumberTheory/ThreeGapTheorem.lean
#   then edit: Apache header, namespace ThreeGap, delete `#print axioms`

# 5. Register it in the import index (insert in sorted position)
#    add a line `import Mathlib.NumberTheory.ThreeGapTheorem` to Mathlib.lean

# 6. Minimize imports (Mathlib CI forbids `import Mathlib`)
#    put `#min_imports in` above the first decl to get the minimal set, OR build and let the
#    `shake`/import linter tell you. Replace `import Mathlib` with the reported modules.

# 7. Build + lint the file
lake build Mathlib.NumberTheory.ThreeGapTheorem
lake exe runLinter Mathlib.NumberTheory.ThreeGapTheorem

# 8. Commit — author email MUST match the CLA signature (saar.shai@gmail.com)
git add Mathlib/NumberTheory/ThreeGapTheorem.lean Mathlib.lean
git -c user.name="Saar Shai" -c user.email="saar.shai@gmail.com" \
    commit -m "feat(NumberTheory): the three-gap (Steinhaus) theorem"

# 9. Push to your fork
git push -u origin three-gap-theorem

# 10. (Recommended etiquette for a NEW theorem) post on Lean Zulip #mathlib4 / #new-members
#     "Is there code for X?" — get a maintainer's nod before/at PR time.

# 11. Open the PR (start as DRAFT so nothing merges before CLA + review)
gh pr create --repo leanprover-community/mathlib4 \
  --base master --head SaarShai:three-gap-theorem --draft \
  --title "feat(NumberTheory): the three-gap (Steinhaus) theorem" \
  --body-file "/Users/za/Documents/Farey NOW/projects/farey-lean/MATHLIB_PR_BODY.md"

# 12. Sign the CLA when the bot comments (YOU), then mark the PR "Ready for review".
```

### Gotchas
- **Author email**: the commit author email must equal the CLA email (`saar.shai@gmail.com`), or the
  `cla/...` check fails (this bit a previous PR). The `git -c user.email=...` in step 8 handles it.
- **Never build Mathlib in `~/Documents`** (Google Drive sync + ~5 GB). Use `~/code`.
- **Minimal imports + linters** are the only substantive remaining work; expect the maintainers to
  request style tweaks (naming, `namespace`, file location) regardless — that's normal.
- Re-run a 1-minute duplication glance at `Mathlib.lean` on master right before opening (it can
  change any day).

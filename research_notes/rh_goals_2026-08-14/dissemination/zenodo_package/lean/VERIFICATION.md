# Lean 4 machine-verification artifacts

All three files below elaborate with **zero `sorry`** and axiom set
`[propext, Classical.choice, Quot.sound]` (the standard Mathlib/classical
axiom set; no extra axioms are introduced). Comments inside the files that
mention the word "sorry" are status-report prose, not `sorry` tactic
invocations — this was checked with `grep -n sorry <file>` and manual
inspection of each hit before packaging.

Toolchain: `leanprover/lean4:v4.28.0`, Mathlib pinned at `rev = v4.28.0`
(from the source projects' `lean-toolchain` / `lakefile.toml` /
`lake-manifest.json`; `.lake` build caches are NOT included in this
package — re-elaboration downloads them fresh via `lake exe cache get`).

## Re-elaboration recipe (per file)

1. Recreate a Lean project with `lean-toolchain` containing
   `leanprover/lean4:v4.28.0` and a `lakefile.toml` requiring
   `mathlib` at `rev = "v4.28.0"`.
2. Drop the `.lean` file into the project and add it to the library target.
3. `lake exe cache get` (fetch prebuilt Mathlib `.olean`s), then
   `lake build <ModuleName>`.
4. Confirm "Build completed successfully" with no error diagnostics and no
   `sorry` warnings.
5. Axiom check: open the file in the Lean server and run
   `#print axioms <theorem_name>` on each named theorem, or use Mathlib's
   `AxiomCheck`/`#print axioms` pattern. Expected output for every theorem
   in these three files:
   ```
   'theorem_name' depends on axioms: [propext, Classical.choice, Quot.sound]
   ```

## Per-file summary

### `v34_TwoPinNoLine/TwoPinNoLine.lean`
Source: `projects/aristotle_dispatch_v34/project_aristotle/TwoPinNoLine.lean`
(the returned Aristotle artifact — NOT the root `aristotle_dispatch_v34/`
dispatch stub). Cited in main.tex §6 ("Machine verification") and
§4.4 (Metatheorem III proof) as the file machine-verifying the pure
logical core of Corollary "no common line": four theorems —
`no_common_line`, the exact interval gap `4334944458020843/10^17`,
disjointness, and distinct real parts — sorry-free, axioms exactly
`[propext, Classical.choice, Quot.sound]`. Statements are byte-identical
to the dispatch summary quoted in the paper. Scope caveat carried from the
paper: `\varphi_5` has no Lean definition here; FJS/MMS analytic content
is cited, not formalized.

### `v33_LawSkeletonI/LawSkeletonI.lean`
Source: `projects/aristotle_dispatch_v33/aristotle_dispatch_v33_aristotle/LawSkeletonI.lean`
(the returned artifact — NOT `projects/aristotle_dispatch_v33/LawSkeletonI.lean`,
which the paper explicitly flags as carrying 16 `sorry` occurrences and
stating "This file machine-verifies nothing"). Cited in main.tex §6 as
machine-verifying, conditional on named hypotheses H1-H5, that growth of
the weighted Jensen count together with finiteness of the real zeros
implies infinitely many strictly off-line zeros and their reflections.
Per the paper's dispatch-summary correction, rows S5 and H3 are
relabelled PROVED (in the consumed (J)-avg form only); H4 and H5 keep
their "NOT proved here" labels — no scattering-theoretic content
(`\varphi_q`, meromorphic continuation, the Jensen/Littlewood rectangle)
is formalized; those enter only as named hypotheses. Also contains the
constant-identity targets of the Kelmer erratum (§5 of the paper),
machine-verified sorry-free and axiom-clean in the same file.

### `v33_Scat1Lemma31Reflection/Scat1Lemma31Reflection.lean`
Source: `projects/aristotle_dispatch_v33/aristotle_dispatch_v33_aristotle/aristotle_dispatch_v33_aristotle/Scat1Lemma31Reflection.lean`
(the nested artifact the paper directs readers to cite — the root
`aristotle_dispatch_v33/Scat1Lemma31Reflection.lean` dispatch stub still
carries a `sorry`). Cited in main.tex §4.4.1 as the file formalizing
*only* the order-preserving pole-to-zero implication under
`\varphi(s)\varphi(1-s)=1`, used to transport the two certified
Selberg-zeta pins (`certificates/`) to the two zeros of `\varphi_5` with
distinct real parts. Does not formalize FJS, MMS, or `\varphi_5` itself.

# V28 dispatch note — Shimizu/Ford reduction + M1 key algebra

**Status:** DRAFT FOR ARISTOTLE. Every theorem in `RateCoreIII.lean` has a
live `sorry`; none is claimed machine-proved by this dispatch. The (RATE)
lemma, the full Ford horoball injection, and coset-level M1 remain OPEN at the
Lean level.

## Sources and inherited conventions

- `research_notes/rh_goals_2026-08-14/lane_g/M2_FORD_PACKING_REFEREE.md`
  records the Ford replacement as **CONFIRMED at paper level; Lean
  formalization open**. Its authoritative input is Series, Theorem 2.21 and
  Lemma 2.22; its finite packing reduction is at lines 74–116.
- `research_notes/rh_goals_2026-08-14/lane_g/M2_G1G2_CLOSURE_SOL.md` §6
  lists Shimizu and the finite cylinder-packing inequality as Lean dispatch
  candidates.
- `research_notes/rh_goals_2026-08-14/lane_g/M1_COSET_STRATEGY_SOL.md` §6
  marks translation action and arithmetic key normalization a
  **CONJECTURAL target; Lean-formalizable**. That exact caveat is retained.
- `Qmat`, `Spow`, `wordMatrix`, `depth`, and `c` are copied verbatim from the
  v26/v27 dispatch inputs. No v26 c-only injectivity axiom is revived; v27
  machine-refuted that proxy at depth three.

## Mathlib reality check

The reachable cache is the harvested v26 project cache under
`projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle/.lake`.
It contains generic special/projective-special-linear matrix infrastructure
and an upper-half-plane Möbius action, but the cached Mathlib source contains
no named Shimizu, Jørgensen, or Fuchsian theorem.

Toolchain receipt:

```text
$ sed -n '1p' projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle/lean-toolchain
leanprover/lean4:v4.28.0
```

Command receipt (run 2026-08-18 from the repository root):

```text
$ rg -n -i 'shimizu|jørgensen|jorgensen|fuchsian|kleinian' projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle/.lake/packages/mathlib/Mathlib --glob '*.lean'
(no output; exit 1)
```

Positive surface receipt:

```text
$ rg -l 'ProjectiveSpecialLinearGroup|SpecialLinearGroup' projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle/.lake/packages/mathlib/Mathlib --glob '*.lean' | sort | head -5
projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle/.lake/packages/mathlib/Mathlib/Analysis/Complex/UpperHalfPlane/MoebiusAction.lean
projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle/.lake/packages/mathlib/Mathlib/Analysis/Normed/Algebra/MatrixExponential.lean
projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle/.lake/packages/mathlib/Mathlib/Data/Fintype/Parity.lean
projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle/.lake/packages/mathlib/Mathlib/LinearAlgebra/Matrix/FixedDetMatrices.lean
projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle/.lake/packages/mathlib/Mathlib/LinearAlgebra/Matrix/GeneralLinearGroup/Defs.lean
```

Consequently v28 does **not** assert a fake imported Fuchsian-group theorem.
It packages the exact Jørgensen trace inequality as
`WidthOneJorgensenAssumption` and asks Aristotle to prove the determinant-one
matrix identity and its algebraic Shimizu consequence. Connecting that
assumption to a non-elementary discrete subgroup remains OPEN.

## Obligations

| Lean name | Scope | Source status carried into v28 |
|---|---|---|
| `trace_unitTranslationCommutator` | `tr([S,B]) = 2+c²` for a determinant-one real matrix | PAPER-LEVEL RECEIPTED; Lean target OPEN |
| `shimizu_lower_left_of_explicit_jorgensen` | `|c|≥1` from the explicit Jørgensen inequality input | honest weaker Mathlib-facing form; full discrete/Fuchsian bridge OPEN |
| `ford_count_le_floor_sq_of_circle_arcs` | finite length-sum proof of `A(X)≤⌊X²⌋` after disjoint unit-circle arcs are supplied | group result PAPER-LEVEL CONFIRMED; only finite arithmetic dispatched |
| `doubleTranslation_bottomRow` | exact action of `S^u M S^v` on `(c,d)` | M1 §6 CONJECTURAL TARGET; Lean-formalizable |
| `red_mem_Ico` | `d-c floor(d/c)∈[0,c)` for `c>0` | M1 §6 CONJECTURAL TARGET; Lean-formalizable |
| `red_add_int_mul` | invariance under `d↦d+nc` | M1 §6 CONJECTURAL TARGET; Lean-formalizable |
| `bottomRowKey_doubleTranslation` | invariance of normalized `(c,d mod c)` under both parabolic translations | exact algebraic sub-obligation of M1-W only; M1-W itself remains CONJECTURAL |

## Deliberate exclusions

- No assertion that Mathlib's generic `IsDiscrete` topology proves
  Jørgensen or Shimizu.
- No PSL quotient action, non-elementarity predicate, Fuchsian subgroup API,
  or Hecke-family discreteness theorem is invented locally.
- No horoball-to-double-coset injection is asserted. The Ford target begins
  only after disjoint arcs and the unit-circumference length inequality have
  been supplied.
- No finite rewrite-system confluence target is sent yet: §6 calls it
  Lean-formalizable for each fixed `q`, but v28 lacks the centered alphabet,
  endpoint tie, and critical-pair definitions needed for an honest statement.
- No M1-W/I/S/L theorem is sent. They depend on the CONJECTURAL NF–Rosen
  bridge and must remain four separate gates.
- No old c-only word-map injectivity axiom: v27 certified it FALSE at depth
  three.

## FALSE-statement escape hatch

Follow the harvested v26 pattern and the explicit v27 rule. If a target is
FALSE as stated:

1. retain the original only in a `FALSE AS STATED` comment;
2. prove `<target>_false` as its negation with an exact witness;
3. state and prove the weakest corrected `<target>'` theorem;
4. report the downstream status change rather than forcing the original.

## Local syntax receipt

Run against the reachable v26 harvested cache without copying or committing
`.lake`:

```text
$ ( cd projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle && ~/.elan/bin/lake env lean ../../../aristotle_dispatch_v28/RateCoreIII.lean )
../../../aristotle_dispatch_v28/RateCoreIII.lean:96:8: warning: declaration uses `sorry`
../../../aristotle_dispatch_v28/RateCoreIII.lean:109:8: warning: declaration uses `sorry`
../../../aristotle_dispatch_v28/RateCoreIII.lean:129:8: warning: declaration uses `sorry`
../../../aristotle_dispatch_v28/RateCoreIII.lean:161:8: warning: declaration uses `sorry`
../../../aristotle_dispatch_v28/RateCoreIII.lean:172:8: warning: declaration uses `sorry`
../../../aristotle_dispatch_v28/RateCoreIII.lean:180:8: warning: declaration uses `sorry`
../../../aristotle_dispatch_v28/RateCoreIII.lean:191:8: warning: declaration uses `sorry`
[exit 0]
```

Verdict: syntax/type-check PASSED. The seven warnings are exactly the seven
dispatch obligations; they are expected and remain live proof holes for
Aristotle. No `.lake` directory was created under v28.

```text
$ find projects/aristotle_dispatch_v28 -type d -name .lake -print
(no output; exit 0)
```

## DISPATCHED 2026-08-18

Project `aa66c34e-c545-424e-a0aa-8251b8349c2b`. Orchestrator independently
re-ran the syntax pre-check before submission (`lake env lean` against the
v26 cache: exit 0, sorry-only warnings). Submitted without .lake (CLI warning
noted; v26/v27 also ran mathlib-side without our cache). FALSE-statement
escape hatch + WidthOneJorgensenAssumption-as-given instruction included in
the prompt. Harvest on completion.

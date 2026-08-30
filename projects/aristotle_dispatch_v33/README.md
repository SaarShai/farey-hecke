# aristotle_dispatch_v33 — what the nested directories are

Two Aristotle runs returned into this dispatch, and each return was unpacked
inside the previous one, so the layout self-nests. It is confusing but the
contents are not redundant — read this before moving anything.

| Path | Role |
|---|---|
| `.` (this directory) | **Dispatch input.** `LawSkeletonI.lean` here carries the 16 `sorry` bodies as sent; `Scat1Lemma31Reflection.lean` carries its one `sorry`. `DISPATCH.md` is the request. |
| `aristotle_dispatch_v33_aristotle/` | **Result of run `1f7dca67-f547-4632-9440-25cbac8dc060`.** Its `LawSkeletonI.lean` has no `sorry` bodies left (the three matches are prose in comments); the run reports all 14 targets A1–A3, B1–B5, C1, … proved, `lake build` clean, `#print axioms` showing only `propext`, `Classical.choice`, `Quot.sound`. |
| `aristotle_dispatch_v33_aristotle/aristotle_dispatch_v33_aristotle/` | **Result of run `87925d91-8e83-452a-a4b5-785493464ca2`.** The one file that matters here is `Scat1Lemma31Reflection.lean`, whose `sorry` in `scat1_lemma31_reflection` is replaced by a full proof. Its `LawSkeletonI.lean` is just a copy of the dispatch input. |

A fourth nesting level existed and was deleted: it duplicated the run
`1f7dca67` result byte for byte.

The `.lake` build cache (12 GB of Lean 4.28.0 + Mathlib oleans, manifest-pinned)
was deleted as regenerable. **Nothing here has been rebuilt locally since**, so
the "no `sorry`, no `axiom`" statements above are the runs' own reports, not a
claim re-verified in this repo. Re-checking means `lake exe cache get` followed
by `lake build` in the relevant directory.

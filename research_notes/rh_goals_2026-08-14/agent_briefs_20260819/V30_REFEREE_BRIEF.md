GOAL: Cold-adversarially referee committed v30 harvest candidate 41e1af6 and write only projects/aristotle_dispatch_v30/V30_REFEREE.md.
IN-SCOPE: projects/aristotle_dispatch_v30/DISPATCH.md, draft projects/aristotle_dispatch_v30/RateCoreV.lean, returned projects/aristotle_dispatch_v30/result/aristotle_dispatch_v30_aristotle/RateCoreV.lean and returned metadata; write only projects/aristotle_dispatch_v30/V30_REFEREE.md.
OUT-OF-SCOPE: Do not edit any existing source, result, MAP, task file, theorem ledger, or git state; do not claim analytic FW, AM, RATE-A, or source-table coverage beyond the exact returned Lean statements.

PHASE 0 — before any edit: reply with your plan and EVERY disagreement with this
brief, citing real files as evidence — or state what you checked before concluding
it is sound. Verify named APIs/paths/versions against the live repo before
planning. Silent compliance is a lane defect; silent scope additions are a lane
defect.

GATE (re-run, do not self-certify): your final output is judged by a SEPARATE
verifier on a machine check — not your done-claim. Return raw findings/data, not
"done". State attempts tried + abandoned and every assumption. If you produce a
file/artifact, say exactly what you changed; do NOT touch anything outside the
named scope. END with "READY FOR JUDGING", never "complete".

ACTIVE RULES:
- team-lead: Team-lead: leader plans+reviews only; builders do keystrokes; every claim cold-verified; one worker one lane; briefs self-contained (hooks don't fire in subagents).

DONE MEANS:
- Hash the exact returned RateCoreV.lean and independently rebuild it with /Users/za/.elan/bin/lake against /Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle; quote the command, all output, and exit.
- Prove from the actual source that there are zero sorry terms and zero declared axioms, then independently stream #print axioms for every named target and distinguish standard Lean axiom dependencies from declarations.
- Compare every requested target statement in the draft and returned source; detect weakening, reordered dependencies, added assumptions, false-as-stated changes, or a name whose prose overstates its formal scope.
- Attack decoder totality/injectivity, list length parsers, tags, signed integers, malformed-input guards, and whether the returned theorem covers only the explicit MarkedCode serialization rather than the paper source-table encoder.
- Write projects/aristotle_dispatch_v30/V30_REFEREE.md with source hashes, statement/scope ledger, exact receipts, adversarial findings, and a final CONFIRMED, GAPS, or REFUTED verdict for each finite Lean target and for any broader claimed scope.

VERIFY: run the v26-cache Lean rebuild, exact forbidden-declaration search, streamed axiom audit, focused statement diff, git diff --check, forbidden artifact/secret scan, and git status proving no changed path except V30_REFEREE.md plus this untracked brief.

Critical status boundary:
- A successful finite serializer proof may be machine-verified while the full analytic FW estimate, Ford counting, canonical normal form, source-table coverage, AM atom moment, and RATE-A machine certificate remain CONJECTURAL at Lean level.
- The theorem called marked_code_source_injective_target is acceptable only at the exact scope its types encode. Explicitly say whether it proves a decoder for the full paper marked-source map or only for the locally defined wire format.
- Standard dependencies propext, Classical.choice, and Quot.sound are not zero dependencies; quote them exactly and reject any nonstandard declaration.

LANE REPORT (hard shape — the orchestrator reads only this): summary <=200 words;
changed_paths (every file, exhaustive); evidence (exact commands + output lines
for each done-means criterion); attempts; assumptions; leftovers/concerns. End
with exactly one status line: STATUS: COMPLETE | COMPLETE_WITH_CONCERNS (list) |
BLOCKED (exact blocker + what you tried) — then the line READY FOR JUDGING. Raw
results only — no verdicts about your own work, no 'done'.

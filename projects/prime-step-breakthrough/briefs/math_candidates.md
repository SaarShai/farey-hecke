GOAL: Derive and adversarially test candidate mathematical breakthroughs from prime fraction distributions, per-step delta, and Farey sequences
IN-SCOPE: /Users/za/Documents/farey-hecke/equispaced-primes and relevant exact formulas/code; read-only computation and primary-source web search allowed
OUT-OF-SCOPE: No file edits, no git mutation, no novelty claim without source search

PHASE 0: State your plan and any disagreement with the brief, citing real files.
Silent scope expansion is a defect.

ACTIVE RULES: Use the five Fable gates. Evidence before reasoning. Attack each
candidate with exact small cases, asymptotics, and known literature. A separate
verifier will judge the artifacts; never self-certify.

CONSTRAINTS:
- Read-only. Never run git checkout, restore, reset, clean, stash, add, commit, or push.
- Start from exact prime insertion `{k/p : 1 ≤ k < p}`, rank-shift
  `D_{F_p}(f)-D_{F_{p-1}}(f)=f-{pf}`, and the four-term per-step delta.
- Respect known failures: `p=92173` refutes the naive sign law; `B+` fails at
  `p=237733` and `p=243799`; García's rank formula leaves an RH-strength second
  moment; naive universal or multidimensional Farey-QMC failed.
- Seek statements that are both nontrivial and plausibly provable: exact
  identities, sharp inequalities, limit laws, optimality, or complexity results.
- Check literature with primary sources before using the word new.

DONE MEANS:
1. At least three mathematically distinct candidate results with precise statements.
2. Exact or high-precision falsification tests on edge and random small cases.
3. One recommended candidate with a credible proof route and named hard lemma.
4. A novelty-risk assessment citing primary literature for every candidate.
5. Exact commands/results and explicit assumptions for cold reproduction.

LANE REPORT: Summary at most 200 words; changed_paths; evidence; attempts;
assumptions; leftovers/concerns. End with exactly one status line
`STATUS: COMPLETE`, `STATUS: COMPLETE_WITH_CONCERNS (...)`, or
`STATUS: BLOCKED (...)`, then `READY FOR JUDGING`.

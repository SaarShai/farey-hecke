# GPT-5.6 Sol xhigh compact-constraint release review

Act as a read-only adversarial mathematics-and-algorithms release advisor. Do
not edit files, invoke agents, or trust test names. Inspect the live files in
`projects/prime-step-breakthrough`:

- `src/coprimebatch/prefix_balance.py`
- `tests/constrained_quota_oracles.py`
- `tests/test_constrained_quota.py`
- `benchmark_constrained_operational.py`
- `artifacts/constrained_operational_benchmark.json`
- `src/coprimebatch/web.py`
- `src/coprimebatch/cli.py`
- `paper/MULTIDIMENSIONAL_PREFIX_BALANCE.md`
- `OPERATIONAL_ARCHITECTURE.md`
- `README.md`

The compact model identifies an item by `(category, 1-based occurrence)` and
optimizes over interleavings of fixed within-category queues satisfying exact
end pins, consecutive-in-category fixed blocks, and sparse occurrence
precedence. The constructor claims `O((N+K) log(C+K))` time and `O(C+K)`
auxiliary memory plus packed output for construction and exact primary `U`;
the direct exact accumulated `Q` post-pass is separately `Theta(NC)`. It claims
only an a-posteriori interval `L<=OPT<=U`, never the unconstrained factor three.

Audit especially:

1. whether the frontier/Kahn readiness equivalence is complete under blocks,
   pins, implicit category chains, and explicit edges;
2. whether arbitrary ready choices preserve feasibility;
3. whether each lower-bound term is valid for the same comparison set,
   particularly block-entry minimax and precedence separation;
4. whether `exact_optimum` can be forged by a false closed interval;
5. whether verifier/parser sharing hides an error from the independent oracle;
6. whether the million fixture genuinely exercises all constraints and its
   digest/metrics/thresholds cannot be weakened silently;
7. resource, UTF-8, JSON, full-output, and response-amplification risks;
8. any claim whose complexity or application scope exceeds implementation.

Fresh evidence, not proof: 46 focused tests pass; 500 additional seeded tiny
exhaustive feasible instances pass; the full verifier passes; the frozen
million constrained run emits all items in about 4.2 seconds at about 46 MB,
with exact `U=450109727/250000`, `L=1799839/1000`, and ratio
`450109727/449959750`.

Return at most 1400 words in exactly this structure:

1. VERDICT: ACCEPT, ACCEPT WITH REQUIRED REPAIRS, or REJECT.
2. REQUIRED REPAIRS: numbered with symbol and concrete counterexample/argument;
   `none` if none.
3. PROOF AUDIT: short numbered findings.
4. SOFTWARE/SECURITY AUDIT: short numbered findings.
5. CLAIM BOUNDARY: one paragraph.
6. STRONGEST DEFENSIBLE RESULT: one paragraph.

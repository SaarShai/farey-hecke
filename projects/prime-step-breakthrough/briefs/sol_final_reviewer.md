# GPT-5.6 Sol Ultra advisory review

Act as a read-only senior mathematics-and-algorithms reviewer.  Do not edit any
file and do not invoke other agents or skills.  Inspect these live files:

- `src/coprimebatch/prefix_balance.py`
- `tests/prefix_balance_oracles.py`
- `tests/test_prefix_balance.py`
- `paper/MULTIDIMENSIONAL_PREFIX_BALANCE.md`
- `research/MULTIDIMENSIONAL_PRIOR_ART.md`
- `OPERATIONAL_ARCHITECTURE.md`

The release claims only: exact rational centering; an `O(N log C)` quota EDF
constructor for unconstrained equal-mass one-hot categorical inventories with
`B<1` and strict approximation ratio below 3; an exact nearest binary word; a
two-pass exact small-instance oracle; and constrained V1 feasible schedules
with an a-posteriori `L<=OPT<=U` certificate.  It explicitly does not claim a
general-vector million-scale factor or downstream application accuracy.

Audit the actual code against the theorem, looking especially for a false
lower bound, a false exact label, a DP state/reconstruction error, a constraint
contraction error, a verifier that shares the production mistake, or a scaling
claim not realized by the code.  The independent suite currently passes 23/23,
128 additional random exhaustive cases pass, and the one-million categorical
benchmark is about 1.52 seconds / 37 MB; treat those as evidence, not proof.

Return no more than 1200 words in this exact structure:

1. VERDICT: ACCEPT, ACCEPT WITH REQUIRED REPAIRS, or REJECT.
2. REQUIRED REPAIRS: numbered, with file/line or symbol and a concrete failing
   example or argument; say `none` if none.
3. CLAIM-SCOPE RISKS: numbered.
4. STRONGEST CONTRIBUTION: one paragraph.
5. NEXT RESEARCH MOVE: one paragraph.

Do not praise style.  Prefer a falsifiable objection to a general suggestion.

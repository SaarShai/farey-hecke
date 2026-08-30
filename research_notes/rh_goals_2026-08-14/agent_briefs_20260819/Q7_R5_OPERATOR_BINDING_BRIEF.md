# Writer brief — q7 Clause-1 operator binding/common continuation

Work only in this isolated worktree. Other agents are active elsewhere; do not
revert or modify their files. Your sole owned deliverable is:

- `research_notes/rh_goals_2026-08-14/lane_f/Q7_R5_OPERATOR_BINDING_SOL.md`

Do not edit the brief, MAP, assembly, manifests, receipts, or code. Do not
commit, push, submit Aristotle, or launch Kaggle.

## Objective and exact status

Write the smallest rigorous paper proof that closes Link 4b identified by
`THEOREM_G7_OFFLINE_REFEREE2.md`: bind the q7 certified five-disc/19-occurrence
engine to the MMS reduced `+` operator in equation (34), bind its normalized
matrix to the finite compression, and instantiate the already-banked
Hilbert/Banach common-continuation argument. Mark this as a `PROOF CLAIM —
AWAITING COLD REFEREE`; do not upgrade q7, the LAW, or MAP.

If any implication cannot actually be proved from the supplied bytes and
receipts, state it as `GAP / CONJECTURAL` instead of forcing it. The paper's
abstract operator statements do not by themselves identify the Python engine.

## Required theorem statement

Set `lambda_7=2 cos(pi/7)`, `h_7=2`, `kappa_7=5`. Define exact partition
points as in `f7_certify_tb_blocks.py`, centers as midpoints, and radii
`R_j=a_j*(phi_j-phi_{j-1})/2` with exact rational decimal factors
`(3.522,2.622,2.372,1.79,1.6)`. Define the branch maps and squared-denominator
weights with the exact engine/MMS sign convention. State and prove:

1. the q7 discs are admissible for the MMS reduced operator;
2. specializing MMS (34) at `2h=4`, `kappa=5`, sign `+1` gives exactly the
   engine's ordered 19 occurrences (9 heads, 10 tails);
3. on normalized monomials, `_single_block_allcols` and
   `_tail_block_allcols` give the coefficients of the exact branches/tails;
4. `M_N(s)` is the matrix of `P_N L^H_{s,+} P_N`, with the correct finite
   determinant identity (do not equate the finite determinant to the infinite
   one);
5. on
   `Omega* = {Re s > 1/2} union {Re s > 0 and Im s > 1}`,
   `det_H(1-L^H_{s,+}) = det_B(1-L^{MMS}_{s,+})`, using q7 E1 for smoothing,
   equality of nonzero Jordan spectra on the absolute-convergence region,
   spectral determinant products, trace/nuclear holomorphy, and the identity
   theorem;
6. the only downstream corollary claimed inside this note is closure of Link
   4b conditional on cold confirmation. Any Selberg-zero or LAW promotion
   stays withheld for the assembly-level referee/ledger turn.

## Primary source (freshly inspected)

Use only MMS arXiv:0912.2236v2, 15 Mar 2010, DCDS 32 (2012), 2453–2484.
Versioned PDF URL: `https://arxiv.org/pdf/0912.2236v2`; current PDF SHA-256:
`a10020bd084534dc60fc3e887958f1583f2fc115d567961b461df1a59b32e072`.

Relevant exact source locations:

- p. 15, equations (26)–(27): atomic and infinite branch operators;
- p. 20, Theorem 4.10: nuclear order zero for `Re s>1/2`, meromorphic
  nuclear continuation, poles only at `(1-k)/2`;
- p. 21, Lemma 5.1 and equation (34): `P` symmetry, reduced sectors, and the
  printed `q=2h_q+3>5` formula; q7 qualifies literally;
- p. 28, Theorem 6.4: Selberg quotient and factorization through the reduced
  sectors and `K_s`;
- p. 29, Remark 4: MMS does not prove the general q>3 transfer-eigenfunction
  to automorphic-function correspondence. Do not claim scattering or geometric
  parity from MMS.

Important convention: after reduction, MMS p. 21 writes negative branches with
composition argument `1/(z-n lambda_q)`, matching the engine. Explain rather
than conflating this with the unreduced p. 15 notation.

## Exact implementation and machine receipts

Read:

- `f7_source_builder.py`, especially lines 37–110;
- `f7_r3b_engine.py`, especially lines 61–170;
- `lane_g/law_probes/kaggle_boundary_rate/zeta_cert_rosen_q5.py`, especially
  branch/tail definitions around lines 199–260 and all-column implementations;
- `F7_TB_BLOCK_CERTIFICATES_RECEIPT.json`;
- `f7_receipts/F7_E1_ENLARGED_CONTRACTION_V2_RECEIPT.json`;
- `lane_g/TB_R5_DETERMINANT_IDENTIFICATION.md`;
- `THEOREM_G7_OFFLINE_REFEREE2.md`.

Fresh root receipts to quote exactly:

```text
q=7 h=2 kappa=5 twoh=4
expected_atomic_calls= 19
source_atomic_calls= 19
receipt_atomic_calls= 19
source_equals_eq34_instantiation= True
receipt_equals_eq34_instantiation= True
source_equals_receipt= True
heads= 9 tails= 10
```

All 16 embedded Kaggle q7 chunk scripts agree with the live sources:

```text
chunk_count= 16
f7_source_builder.py embedded_hash_count=1
  038bcb49d3df00cfd4e1fb4aafca46a4e11e34f6b18300c07d4666be51bf45c6
f7_r3b_engine.py embedded_hash_count=1
  661a4d2b132d1821d18499a302f58805bf7565e560d8f1520379dde156bc7d1a
zeta_cert_rosen_q5.py embedded_hash_count=1
  c84c5c3f6d9f7a320bca7f1dbfd96a4859c3eea9b3de5420eb4eb223ad0d597b
f7_certify_tb_blocks.py embedded_hash_count=1
  9c17cd7ce42c7d41e6d811eb2b8ecf3ced88b8d89e6b411b4cd19aaf7b5c80b1
f7_certify_r3b_flagship.py embedded_hash_count=1
  df9873d9f1e47c47f2e846d38d906f8f77619a17871e6d7c6da8c225bb63f687
embedded_matches_live=True for every listed file
```

The generic `zeta_cert_rosen.py` live path drifted from the certified hash, but
the value builder uses the q5 primitives above and its own explicit 19-call
assembly. State this drift and why it is not used to infer the binding. Do not
silently claim the live generic engine was certified.

TB receipt facts: q=7, h=2, kappa=5; exact factors above; 384-bit Arb/Acb;
`rho_star=[0.763212029206899202166157 +/- 1.41e-25]`, conservatively upper
rounded to `0.763213`; all head/deep-tail, pole-clearance, and branch-cut gates
pass. E1: 19 blocks; `rho_hat` upper rounded UP to
`0.9152411837446922`; remaining pole/cut clearance lower rounded DOWN to
`0.9915`; verdict `PASS_RHO_HAT_LT_1`.

## Required 19-row table

Give one row per atomic occurrence with output, input, branch/tail start,
sign, MMS term, and code call line. Preserve occurrence multiplicity even when
two calls share a matrix `(row,column)` block.

## Proof hygiene

- Receipts before every numeric/status claim.
- Margins round down; upper bounds round up.
- Treat all source claims no stronger than MMS wording.
- State that the MMS PDF contains no scattering/common-continuation theorem;
  the common continuation here is the paper argument instantiated from R5.
- Explain why the Hurwitz head+tail split is exactly the full tail and why it
  is valid first on `Re s>1/2` before analytic continuation.
- End with an obligations/blast-radius ledger and `READY FOR COLD REFEREE`.
- Run and quote `git diff --check` and scoped `git status --short --branch`.

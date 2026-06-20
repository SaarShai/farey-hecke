# GOAL — drive the top-4 surviving directions to complete closure

Date: 2026-06-20. Owner: main loop (Aletheia/farey-hecke). Metric: closeness × significance × appeal.
Closure = drive each to its **reachable endpoint** with machine-verification (Lean/Aristotle) +
certified numerics (Arb) + heavy compute (Kaggle) where it helps, and **honestly document the
residual** where a piece is genuinely open. "Closure" never means overclaiming a still-open analytic gap.

Tools mandated this run: **Aristotle** (Lean formal verify) and **Kaggle** (heavy numeric offload).

## Sub-goals (each a dedicated /goal for one agent)

### G1 — Certified effective equidistribution via transfer-operator spectral gap  [top reach]
Establish a rigorously **certified spectral gap** (2nd-eigenvalue-modulus enclosure, Arb) for the
Rosen/Hecke transfer operator, and derive the **effective equidistribution / mixing rate** it implies.
Assets: code/d3_rosen_spectral_gap.py, code/d3_rosen_nuclear_gap.py, code/zeta_mayer_rosen.py.
Done: certified gap γ_q with interval bounds for a set of q (Kaggle sweep), the effective-rate formula
(quasi-compactness / Lasota–Yorke), a Lean statement of the certified gap inequality submitted to Aristotle.

### G2 — A-priori truncation / dimension-tail bound  [highest significance]
Replace the "validated-not-proved" dim-tail bound with an **a-priori proof** (or the strongest scoped
partial). This legitimizes every certified spectrum/resonance result.
Assets: code/zeta_cert_rosen.py (`_tail_block_allcols`, `dim_tail_from_matrix`), zeta_cert_rosen_even.py.
Done: a precise statement of the truncation-remainder bound; a rigorous proof or a precisely-scoped
partial naming the exact open inequality; Lean core submitted to Aristotle; numeric validation of constants.

### G3 — B(q) full machine-verified theorem  [bankable]
Close the residuals of B(q) = rotation-arc-count. SCOUT existing proofs first:
projects/aristotle_dispatch_v15/uniform_q5to18/BCZHeckeRotationArc{,R1,R2,R2hi,R2hi2,R3Parity}.lean
and per-q BCZHeckeG{5..21}_window_VERIFIED.lean (many q may already be done).
Done: enumerate exactly what's proved vs open; close additional per-q realizations (R2) and/or the
R3 lattice-gap/parity lemma via Aristotle; honest residual on uniform-all-q.

### G4 — Certified Maass spectrum extension + packaging  [referee/DB value]
Extend the certified spectrum table (more q / more eigenvalues; G_8 done) and finalize the
Strömberg/Pohl/LMFDB package. Assets: code/zeta_cert_rosen.py, run_cert_g8.py, code/out/*.json,
research_notes/{certified_hecke_spectrum_table,aletheia_hecke_evidence_package}.md, Kaggle hecke_highr_sweep.
Done: additional certified eigenvalues (winding=1) via Kaggle high-r sweep + Hejhal cross-check; updated package.

## Honesty + closure rules (apply to every agent)
- Report **READY FOR JUDGING**, never "done"; list attempts + assumptions; quote smoke output.
- Write ONLY your assigned disjoint paths; do NOT git; do NOT echo/commit API keys (HOME-only).
- Certified = Arb interval enclosure. Aristotle-verified = sorry-free + axioms {propext,Classical.choice,Quot.sound}.
- Distinguish proved / certified-numeric / heuristic explicitly. Surface honest partials; do not manufacture closure.

## Async handling (main loop, after fleet returns)
Poll Aristotle project IDs + fetch Kaggle kernels to completion; locally re-verify each proof
(grep 0 sorry; axiom check); land + commit; synthesize; update goals; iterate sub-fleets per direction as needed.

# Wiki Log

## [2026-06-20] verify | Hejhal confirms G_5 odd Maass eigenvalues (transfer-operator eq.34)

Created `L2_facts/hejhal-confirms-g5-maass-eigenvalues.md` (verified fact). Independent automorphy point-matching (no transfer-operator code reused) confirms first two odd eigenvalues r₁=6.47367, r₂=8.63677 to 5 sig figs vs TO claim 6.4737, 8.6368. Modular-group validation SL(2,Z) r₁=9.53370 ✓. Critical bug diagnosed & fixed: sqrt(y) Whittaker prefactor omission caused Y₀-dependent offset; after fix, dips height-independent (genuine eigenfunction). Closes TO credibility for low spectrum; r₅,r₆ unverified.

## [2026-06-14] update | Track-C extremal index theta_q for BCZ extreme-gap process

Created `concepts/track-c-extremal-index-theta-q-for-bcz-extreme-gap-process.md` from `page` template.


- [2026-06-14] Track-C extremal index theta_q: VERDICT falsified lambda_q-family. Limiting theta=1/2 all q>=4 (deterministic cusp swap-pair, no lambda_q); finite onset-threshold theta_q(X(q)) q-dependent but no elementary closed form. q3=0.5641,q4=0.5923,q5=0.5924. See concepts/track-c-extremal-index-theta-q-for-bcz-extreme-gap-process.md
## [2026-06-14] update | X_Omega(q) equality upper bound — verdict and cusp-Dirac inadmissibility

Created `concepts/x-omega-q-equality-upper-bound-verdict-and-cusp-dirac-inadmissibility.md` from `page` template.


## 2026-06-14 — X_Omega(q) equality upper bound verdict
Created concepts/x-omega-q-equality-upper-bound-verdict-and-cusp-dirac-inadmissibility.md (trust: verified).
GOAL G-F: X_Ω(q)=1/λ³ NOT machine-verified; cusp-tip Dirac inadmissible in lower-bound class (3 machine-checked obstructions, EqualityUpperBound.lean, axiom-clean). Verified footprint stays X_Ω(q)≥1/λ³ for q∈{5,7,…,21}.
## [2026-06-14] update | B(q) cluster ceiling: 2+floor((q-1)/6) is FALSE; true slope 2arccos(2sqrt2/3)/pi

Created `concepts/b-q-cluster-ceiling-2-floor-q-1-6-is-false-true-slope-2arccos-2sqrt2-3-pi.md` from `page` template.

2026-06-14 FALSIFIED B(q)=2+floor((q-1)/6); true slope 2arccos(2sqrt2/3)/pi=0.2163; exact witnesses q=5,23,24,30,40 exceed formula. concepts/b-q-cluster-ceiling-...

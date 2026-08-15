# D3 Open Items

This list is the human gate before any submission decision. The six requested source paths existed, so no source-path substitution was made. [EXACT]

1. **Venue.** Choose the target venue and confirm that its Experimental-Mathematics tier accepts a short note whose central formal identity is classical in the literature and whose new finite content is negative/counterexample evidence. [EXACT]

2. **Author list.** Supply and approve the complete author list, affiliations, and order; the source packet does not determine them. [EXACT]

3. **Fresh Lean re-verification.** A fresh re-verification is pending. Decide whether to run a fresh Lean build and record the theorem receipt for `FareyBridgeIdentity.farey_bridge_identity_unconditional` before submission. The FACTS ledger explicitly makes no claim about a freshly checked formalization, and it does not record a `#print axioms` footprint. The exact axiom status must therefore be obtained and inserted before any stronger formal-verification wording is used. [LEAN]

4. **Numerical-certification threshold.** Decide whether the compensated-`long double` records for \(p=92{,}173\), \(237{,}733\), and \(243{,}799\) are sufficient for the venue, or whether an independent interval/exact rerun is required; the source records stable signs but not interval proofs. [NUMERICAL]

5. **Submission wording.** Preserve the explicit boundaries: no RH progress, no density-one theorem, and finite computations only. Preserve the sole novelty claim as per-step/bridge packaging plus the certified counterexamples, with no novelty claim for the static identity. [EXACT]

6. **Bibliography check.** Confirm the final Garcia 2025 and Cox--Ghosh--Sultanow 2021 entries against the venue’s citation style and retain both as prior art before submission. [EXACT]

**Assembly assumption.** This skeleton treats the current Lean source’s `farey_bridge_identity_unconditional` statement as the reported `[LEAN]` result while keeping fresh-build and axiom-footprint verification open, because the named FACTS ledger does not provide that receipt. [LEAN]

## Outlook-section material from the Kloosterman gate (closed NO-GO 2026-08-14)

Precise open problem for the outlook: the per-step Farey fluctuation is
exactly V_residue(p) = Σ_c M(⌊(p−1)/c⌋)·s(p,c) (Mertens-weighted
Dedekind-sum convolution; exact extraction + zero-error rational receipts
in lane_i/V_EXTRACTION.md). Weil/Kloosterman methods cannot reach it — the
frozen paper's own completion analysis rules the direct Kloosterman form
invalid, and any sufficient bound embeds Mertens cancellation (RH-strength).
State as: "sign-structure at the Franel–Landau boundary requires
power-saving in a Mertens-weighted Dedekind convolution — beyond
square-root cancellation."

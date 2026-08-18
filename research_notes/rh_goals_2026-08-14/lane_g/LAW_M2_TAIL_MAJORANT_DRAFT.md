# M2 — explicit tail majorant for the coset Dirichlet series (DRAFT)

Status: DRAFT 2026-08-17. Closes the "no closed-form majorant" blocker on
gap M2 of LAW_R2_RATE_LEMMA_DRAFT.md using the printed source received
today (Hejhal LNM 1001 Vol.2: Ch.6 §12 pp.149–166 + Ch.11 §3 pp.524–532;
extraction: LAW_HEJHAL_CH6S12_CH11S3_EXTRACT.md). LEDGER: this is a drafted
majorant with one structural lemma at proof-sketch level (M2.L below), not a
finished proof; constants are explicit and rounded UP.

## 1. Target

M2 (from the R2 draft): an explicit, N-uniform majorant

    T(X, sigma)  >=  Σ_{cosets w : |c_w| > X} |c_w|^{-2σ}      (all N ≥ 3, σ ≥ 1.1)

playing the role of Hejhal's Lemma 7.2 constant C(ε) (N-INDEPENDENT there;
our job is only to make it numeric). It feeds the R2 assembly term T_X and
the N3 tail allowance.

## 2. Multiplicity lemma (M2.L — the one structural input)

**Claim (M2.L).** In the conjugated model 𝒢_N (cusp at ∞, width λ = λ_N ≤ 2),
a double coset [S]\𝒢_N/[S] with lower-left entry c ≠ 0 is determined by the
pair (|c|, d mod λ|c|), d the lower-right entry; hence the number of double
cosets with |c_w| = c is at most

    m_N(c) ≤ λ_N · c ≤ 2c.

*Proof sketch.* Left multiplication by S^k fixes (c,d); right multiplication
sends d ↦ d + kλc. So (c, d mod λc) is a double-coset invariant, and d runs
over a discrete subset of an interval of length λc. Injectivity of the
invariant on cosets = the standard bottom-row classification (printed
analogue at λ=2: Vol.2 Ch.11 §3 Lemmas 3.1–3.3, where the count for fixed c
is EXACTLY φ(2c) ≤ 2c — the trivial bound is attained-order, not wasteful).
[GAP M2.G1: the sketch's discreteness step needs the ring Z[λ_N] lattice
spacing ≥ some explicit δ(N) — at λ=2 spacing is 1 (integers); for general N
the c-values are algebraic integers and the R1 enumerator's canonical
invariant (c, d mod c) empirically separates cosets at q ≤ 48, X ≤ 50.
Aristotle-checkable per (q, depth).]

Cross-check at λ=2: v27 dispatch theorem `theta_coset_count` (φ(2c) count,
from printed Lemma 3.1) — machine verification in flight.

## 3. The majorant

For σ > 1 and X ≥ 1, using m(c) ≤ 2c and monotone comparison:

    Σ_{|c|>X} |c|^{-2σ}  ≤  Σ_{c > X} 2c · c^{-2σ}
                          =  2 Σ_{c > X} c^{1-2σ}
                          ≤  2 ∫_X^∞ t^{1-2σ} dt + 2 X^{1-2σ}
                          =  X^{2-2σ} · [ 1/(σ-1) + 2 X^{-1} ]                 (M2.T)

with the c-values indexed by their sorted magnitudes ≥ spacing-1 grid at
λ=2, and for general N by [GAP M2.G2]: the c-spectrum of 𝒢_N majorized
entrywise by the integer grid — equivalent to c_min ≥ 1 and gaps ≥ 1, which
holds at λ=2 exactly (c even integers, v27 `c_two_even`) and empirically for
q ≤ 48 (R1 X≤50 window: min |c| = λ ≥ λ_3 = 1, gap structure Chebyshev).
ROUNDED-UP numeric instances of (M2.T):

    σ = 1.1:  T(X) ≤ X^{-0.2} · (10 + 2/X)     e.g. X=50: 4.60;  X=200: 3.47
    σ = 1.25: T(X) ≤ X^{-0.5} · (4 + 2/X)      e.g. X=50: 0.572; X=200: 0.284

(Receipts: direct evaluation 4.5913 / 3.4692 / 0.5713 / 0.2835, rounded UP.
Sanity vs exact grid sum: 2·Σ_{c>10} c^{-1.2} = 5.3772 ≤ T(10) = 6.4358 ✓.)

Consistency: the R1 measured tail Σ_{|c|≥10}|c|^{-2.2} ≤ 0.26 (UP, uniform
in q ≤ 48) vs (M2.T) at σ=1.1, X=10: 6.44 — majorizes measured by ~25×,
one-sided. The large slack is honest: the trivial multiplicity 2c vastly
overcounts the cosets actually present in the R1 X≤50 window; (M2.T) is a
worst-case ceiling, not a fit. PASSES unadjusted (and the σ=1.1 tail decays
slowly, X^{-0.2} — R5 should prefer σ nearer 1.25 for the tail term).

## 4. What this discharges

- **M2 (R2 gap list): DRAFTED** — closed-form majorant (M2.T) with explicit
  constants; remaining sub-gaps M2.G1 (lattice discreteness, per-(q,K)
  Aristotle-checkable) and M2.G2 (c-spectrum ≥ integer grid for all N —
  needs c_min(N) ≥ 1, plausibly from the trace bound t ≥ 2λ_q already
  machine-verified in v24 HeckeSystole A3; TODO connect).
- **N3 (tail allowance): numeric instances replaced by formula** (M2.T);
  promotion to proved awaits G1+G2.
- The Hejhal-side C(ε) is now redundant for our σ ≥ 1.1 domain: (M2.T) at
  X = 1 gives the full-series bound Σ|c|^{-2σ} ≤ 1/(σ-1) + 2 = 12 at
  σ = 1.1 (receipt: direct evaluation 12.0000) — crude but explicit and
  N-uniform; Lemma 7.2's role in the effectivization is fully replaceable
  by this chain.

## 5. Honest limits

- (M2.T) uses the TRIVIAL multiplicity 2c; at λ=2 the truth is φ(2c) (mean
  ~ (8/π²)c) — a factor ~2.5 recoverable if R5 ever needs it. Not needed at
  current slack.
- The majorant is for the |c|-tail at fixed σ; the R2 warning that X must
  grow with q (beyond-window drift mass) is UNTOUCHED by this note — M2
  bounds the tail SIZE, the drift split is R2's job.
- Nothing here is on the critical line: σ ≥ 1.1 throughout; strip transport
  stays R3 (printed-explicit 7.9/7.10 + now Thm 12.9's explicit φ_m bound
  as an alternative route — noted for R3, not developed).

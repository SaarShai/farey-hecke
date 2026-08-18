# M2 — explicit tail majorant for the coset Dirichlet series (DRAFT)

Status: DRAFT 2026-08-17; corrected 2026-08-18 (audit findings 3/5/6 — see
dated blocks below). Supplies a CANDIDATE closed-form majorant for gap M2 of
LAW_R2_RATE_LEMMA_DRAFT.md, conditional on M2.L (corrected form) + G1 + G2,
using the printed source received 2026-08-17 (Hejhal LNM 1001 Vol.2: Ch.6
§12 pp.149–166 + Ch.11 §3 pp.524–532; extraction:
LAW_HEJHAL_CH6S12_CH11S3_EXTRACT.md). LEDGER: M2 and N3 remain OPEN; this
note's formula (M2.T) is their candidate closed form, not their closure;
constants are explicit and rounded UP.

## 1. Target

M2 (from the R2 draft): an explicit, N-uniform majorant

    T(X, sigma)  >=  Σ_{cosets w : |c_w| > X} |c_w|^{-2σ}      (all N ≥ 3, σ ≥ 1.1)

playing the role of Hejhal's Lemma 7.2 constant C(ε) (N-INDEPENDENT there;
our job is only to make it numeric). It feeds the R2 assembly term T_X and
the N3 tail allowance.

## 2. Multiplicity lemma (M2.L — the one structural input)

> **[CORRECTION 2026-08-18 audit-3]** The original M2.L below mixed two
> normalizations (width-λ translations `d ↦ d + kλc` against the width-1
> conjugated model that R1 and the v26/v27 Lean files actually use, where
> `S : z ↦ z+1` and the invariant is `(c, d mod c)`). Statement of record
> is now in the WIDTH-1 CONJUGATED MODEL throughout; the original text is
> preserved struck-through in spirit by this block. The printed λ=2
> Lemma 3.1 count (d mod 2c, φ(2c)) lives in the UNCONJUGATED width-2 theta
> model; the conjugation dictionary between the two models is one more
> bookkeeping obligation, folded into gap M2.G1.

**Claim (M2.L, corrected — width-1 conjugated model).** In 𝒢_N (cusp at ∞,
width 1, S : z ↦ z+1), a double coset [S]\𝒢_N/[S] with lower-left entry
c ≠ 0 is determined by the pair (|c|, d mod |c|), d the lower-right entry;
under the discreteness hypothesis G1 (admissible d-residues spaced ≥ 1 in
the relevant algebraic grading) the number of double cosets with |c_w| = c
is at most

    m_N(c) ≤ c ≤ 2c        (the 2c ceiling is kept as the working constant
                            so (M2.T) below is unchanged as an UP-rounded
                            ceiling under either normalization).

*Proof sketch.* Left multiplication by S^k fixes (c,d); right multiplication
sends d ↦ d + kc (width 1). So (c, d mod c) is a double-coset invariant —
exactly R1's canonical invariant — and d runs over a discrete subset of an
interval of length c. Injectivity of the invariant on cosets = the standard
bottom-row classification. Printed λ=2 cross-check (after the conjugation
dictionary): Vol.2 Ch.11 §3 Lemmas 3.1–3.3 count φ(2c) ≤ c for fixed c in
the width-2 model — consistent with, and sharper than, the ceiling.
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
- [CORRECTION 2026-08-18 audit-5/6] Previous text here said Lemma 7.2's
  C(ε) is "fully replaceable" and called the X = 1 instance a "full-series
  bound ... 12". Both overstated. (a) (M2.T) at X = 1 bounds only the
  STRICT tail |c| > 1; the |c| = 1 mass (attainable: c = λ_3 = 1 at q = 3)
  adds ≤ m(1) ≤ 2, so the full-series ceiling is ≤ 14 at σ = 1.1, not 12.
  (b) The whole chain is CONDITIONAL on M2.L (corrected form) + G1 + G2;
  until those close, (M2.T) is a candidate formula and Lemma 7.2's C(ε)
  is "replaceable-if"; N3 stays OPEN with (M2.T) as its candidate closed
  form, not its replacement. (c) The stated target covers finite N ≥ 3;
  the N = ∞ theta side needs the same count separately — at λ=2 that IS
  the printed φ(2c) lemma (v27 `theta_coset_count`, certification in
  flight), so the θ-side is the better-grounded half.

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

> **[STATUS CHANGE 2026-08-18 — G1/G2 RETIRED, FORD REPLACEMENT CONFIRMED]**
> M2.G1 and M2.G2 as stated are REFUTED (exact witnesses at N=5 and N=8;
> `M2_G1G2_CLOSURE_SOL.md`, witnesses independently re-verified numerically).
> The tail formula no longer routes through them: an adversarial referee pass
> (`M2_FORD_PACKING_REFEREE.md`) CONFIRMED at paper level the Ford-horoball
> packing bound A_Γ(X) ≤ ⌊X²⌋ (constant 1, PSL double-coset count, uniform in
> N after width-one conjugation; hypotheses = discrete + non-elementary +
> exact ⟨S⟩ cusp stabilizer, sourced to Series Thm 2.21/Lemma 2.22 and Pohl
> arXiv:1503.00525 §2.2), giving via Stieltjes summation
>   Σ_{|c|>X} |c|^{−2σ} ≤ (σ/(σ−1))·X^{2−2σ}   (σ>1, X≥1),
> full-series ceilings 12 (σ=1.1) and 6 (σ=1.25) — coefficient arithmetic and
> the q=5/q=8 enumerator consistency packet re-run fresh this session.
> (M2.T)'s m(c) ≤ 2c multiplicity route is superseded; this bound needs no
> multiplicity ceiling at all. REMAINING for full M2 closure: this covers the
> TAIL SUM shape; Lean formalization of Shimizu + the packing injection is
> OPEN; the Hejhal-7.7/C₆ per-term majorant transcription (Ch.6 §12 constants)
> is a separate, still-open bookkeeping task.

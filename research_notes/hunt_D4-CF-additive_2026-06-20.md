# Hunt D4 — Additive combinatorics / continued fractions / Diophantine approximation
Date: 2026-06-20 (web-verified 2026-06-21)
Agent path: /goal D4-CF-additive

## TL;DR
The single best-fit open problem for our edge is the **reciprocity-obstruction /
continued-fraction-alphabet program of Rickards–Stange** (Duke Math. J. 2025,
arXiv:2401.01860). They DISPROVED the Bourgain–Kontorovich "local-global for
continued-fraction alphabets" conjecture by exhibiting a finite alphabet whose
limit set has Hausdorff dimension δ>1/2 yet which provably NEVER produces a
square denominator — a reciprocity (not congruence) obstruction. The follow-on
questions are explicitly computational, public PARI/GP code exists, and the
central sub-problem (which finite alphabets carry such obstructions, and the
MINIMAL alphabet with δ>1/2) is a search + interval-certified-dimension problem
— exactly our fleet + Arb/transfer-operator strength. This is NOT the
analysis-bound full Zaremba conjecture, and it is NOT the owned Hecke corner.

---

## Domain map (what is owned vs reachable)

### Zaremba's conjecture (1971) — the famous version is OWNED/analysis-bound
- Statement: every q∈ℕ is the denominator of some p/q with all partial quotients
  ≤ A (conjecturally A=5). Equivalently D_5(N)=N for all N, where D_A(N)=#{q≤N
  occurring as a denominator with digits in {1..A}}.
- State (web-verified):
  - Bourgain–Kontorovich (Annals 2014, arXiv:1107.3776): density-one set of q
    satisfies it with A=50, later pushed to A=5 (and alphabet {1,2,3,4,10}, etc.).
  - Positive-proportion / density-one is the frontier; the FULL conjecture is a
    minor-arc / spectral-gap / sum-product analytic problem ⇒ NOT our edge.
  - Computational fact (Niederreiter / Kontorovich expositions): exhaustively,
    [1,10^6] ⊂ D_5, and [1,10^6] \ D_4 = {54, 150}. So D_4 already covers all
    q ≤ 10^6 except two integers; D_5 covers all ≤ 10^6.
- VERDICT: the full conjecture is unreachable for us. The computational residue
  (extending exact D_4/D_5 census, the exceptional set {54,150}) is doable but
  LOW-significance and largely already done — do NOT lead with it.

### Reciprocity obstructions to square denominators — RICKARDS–STANGE — REACHABLE, FRESH
- Papers: Rickards–Stange "Reciprocity obstructions in semigroup orbits in
  SL(2,ℤ)", arXiv:2401.01860 (v1 Jan 2024), ACCEPTED Duke Math. J. 4 Mar 2025.
  Companion: "The local-global conjecture for Apollonian circle packings is
  false", arXiv:2307.02749, accepted Annals of Math. 17 Jun 2024.
- Mechanism: a thin sub-semigroup Ψ ⊆ Γ_1(4) preserves Kronecker symbols;
  quadratic/quartic reciprocity forces certain orbits to avoid squares — a
  Brauer–Manin-flavoured obstruction NOT seen by any single congruence.
- Headline counterexample: continued fractions [0; a_1,…,a_n, 1,1,2] with each
  a_i ∈ {4,8,12,…,128} never have a SQUARE denominator, even though squares are
  congruence-admissible and the average multiplicity → ∞. The limit set of the
  alphabet 𝒜={4,8,…,128} has δ = 0.500890640842 ± 10^-12 (>1/2) — this is what
  refutes Bourgain–Kontorovich, which predicted all large admissible integers
  appear once δ>1/2.
- Explicit OPEN conjectures stated in the paper (computational thresholds!):
  - **Conj 2.13**: Table 1 fully classifies which integers appear as
    numerators/denominators in all seven orbit types of Ψ_1 (only partial now).
  - **Conj 2.14**: every non-square integer n > 10,569 appears as a numerator in
    the orbit Ψ_1(2/3).  ← a finite-search verification / threshold-sharpening.
  - **Conj 2.21**: every non-square v ≥ 10^13 is the denominator of some
    [0; 4a_1,…,4a_n, a_{n+1}, 1, 2] with positive coefficients.
  - Implicit: find the MINIMAL finite alphabet 𝒜 ⊆ 4ℤ^+ (containing 4 and 8)
    with δ>1/2 — they exhibit {4,…,128}; minimality is open and is an
    interval-certified-dimension search.
- Public code: github.com/JamesRickards-Canada/Semigroup-Reciprocity (PARI/GP).
  ⇒ independent re-verification + extension is realistic.

### Adjacent reachable tooling (our certified-dimension edge)
- Jenkinson–Pollicott (arXiv:1611.09276): rigorous Hausdorff dimension of
  restricted-digit CF Cantor sets to 100+ digits (E_2), transfer operator +
  Hardy space + certified approximation numbers. Falk–Nussbaum + INTLAB interval
  arithmetic is the standard certified pipeline (arXiv:2408.06330, 2504.20878).
  ⇒ We can CERTIFY δ for candidate alphabets to find the δ>1/2 threshold case,
  exactly the object Rickards–Stange need.

### Markov / Lagrange spectra — partially owned, one reachable corner
- Jeffreys–Matheus–Moreira "New gaps on the Lagrange and Markov spectra"
  (JTNB 2024; arXiv:2209.12876 + 2405.20581): new portion of M\L near 3.938,
  dim(M\L) ≥ 0.593, new maximal gaps via renormalization + thickness.
  The METHOD is owned by Matheus–Moreira–Delecroix (renormalization + computer
  pictures). Finding a NEW explicit gap or a new element of M\L is a
  pattern-search task, but the gap-certification machinery is their specialty;
  our marginal edge is thin. SECONDARY.

### Markoff uniqueness conjecture — NOT a good fit (number-theory analytic)
- Frobenius 1913: each Markoff number is the max of a unique triple. Still open.
  Bourgain–Gamburd–Sarnak (strong approximation, almost-all composite) is the
  analytic frontier. Computational verification of uniqueness is already pushed
  far (no counterexample known); marginal new contribution. DROP as primary.

### Function-field analogue (McMullen/Zaremba over F_q[X]) — niche but clean
- Malagoli arXiv:1704.02640: polynomial Zaremba holds over infinite fields;
  over F_q it would imply polynomial McMullen. Concrete finite-field census /
  small-q construction questions are exact-arithmetic-friendly but low-reach.
  TERTIARY.

---

## HARD-FILTER scorecard (top pick = Rickards–Stange reciprocity-obstruction)
1. Bottleneck = search/construction/certification (find alphabets, certify δ,
   verify thresholds) — NOT deep analysis. ✅
2. Not owned/saturated: paper is months old (Duke 2025), conjectures EXPLICITLY
   left open with numeric thresholds, classification (Table 1 / Conj 2.13)
   admittedly partial. ✅ active frontier, small community.
3. Tractable in weeks: re-run/extend public PARI code to (a) certify the minimal
   δ>1/2 alphabet, (b) test Conj 2.14 threshold 10,569 by exhaustive orbit
   enumeration, (c) hunt new obstruction-bearing alphabet families. ✅
4. Verifiable: a witness alphabet + certified δ + an exhaustive no-square census
   is independently checkable; Lean/Aristotle can formalize the reciprocity
   parity lemma for a fixed alphabet. ✅
5. Avoids Hecke/Maass/QUE/arithmeticity. ✅ (different corner entirely.)

## Honest tractability / failure modes
- The DEEP theory (general classification of reciprocity obstructions across all
  thin SL(2,ℤ) semigroups) is hard and is the authors' own program — we will not
  out-theory them. Our realistic contribution is the COMPUTATIONAL layer:
  certified minimal-δ witness, threshold verification, new explicit families, and
  a formal-verified parity/Kronecker lemma for specific alphabets.
- Risk: the authors (with public code) may already be extending exactly these.
  Mitigation: pick the formal-verification + interval-certified-minimality angle,
  which is OUR differentiated edge, not theirs.
- Risk: certifying δ near 1/2 to enough digits to decide δ>1/2 for a candidate
  small alphabet needs careful interval arithmetic — but this is precisely the
  Jenkinson–Pollicott/Falk–Nussbaum regime, well within reach.

## Concrete first deliverables (if chosen)
- D1 (witness/construction): exhaustively search alphabets 𝒜 ⊆ {4,8,…,4k}
  containing {4,8}; for each, certify δ(𝒜) by transfer-operator + interval
  arithmetic; output the MINIMAL 𝒜 with δ>1/2 and a certified δ — sharpening or
  confirming the {4,…,128} example. Independently verifiable.
- D2 (verification): exhaustive orbit enumeration of Ψ_1(2/3) to test Conj 2.14
  (every non-square n>10,569 appears) up to a large bound; report true threshold
  or first gap.
- D3 (formal): Lean/Aristotle proof of the Kronecker-symbol invariance + "no
  square denominator" parity lemma for a FIXED small obstruction alphabet — a
  bulletproof, citable micro-result.
- D4 (new conjecture): a sharp conjecture for the minimal δ over the obstruction
  family, or a new obstruction-bearing alphabet outside 4ℤ^+ (e.g. via other
  reciprocity moduli) found by fleet search + certification.

## Sources (web-verified 2026-06-21)
- Rickards, Stange, "Reciprocity obstructions in semigroup orbits in SL(2,ℤ)",
  arXiv:2401.01860; accepted Duke Math. J. 2025-03-04. (HTML read; Conj 2.13/
  2.14/2.21, δ=0.500890640842, alphabet {4,8,…,128} confirmed.)
- Rickards, Stange, "The local-global conjecture for Apollonian circle packings
  is false", arXiv:2307.02749; Annals of Math. (accepted 2024-06-17).
- Code: github.com/JamesRickards-Canada/Semigroup-Reciprocity (PARI/GP); Rickards
  homepage jamesrickards-canada.github.io; Stange publications math.katestange.net.
- Bourgain, Kontorovich, "On Zaremba's conjecture", Annals 2014, arXiv:1107.3776;
  computational fact [1,10^6]\D_4={54,150}, [1,10^6]⊂D_5.
- Jenkinson, Pollicott, arXiv:1611.09276 (certified δ for CF Cantor sets, 100+
  digits); rigorous-dimension pipeline arXiv:2408.06330, 2504.20878.
- Jeffreys, Matheus, Moreira, "New gaps on the Lagrange and Markov spectra",
  JTNB 2024, arXiv:2209.12876; local-dimension update arXiv:2405.20581 (dim
  M\L ≥ 0.593, new gaps near 3.938).
- Malagoli, "Continued fractions in function fields…", arXiv:1704.02640
  (polynomial McMullen/Zaremba analogues).
- Frobenius 1913 / Markoff uniqueness; Bourgain–Gamburd–Sarnak strong
  approximation (almost-all Markoff numbers composite) — noted, DROPPED.

## CAVEATS
- "[1,10^6]\D_4={54,150}" and "[1,10^6]⊂D_5" are quoted from secondary
  expositions of the Bourgain–Kontorovich/Niederreiter line; re-verify the exact
  bound (10^6 vs higher) against the primary source before citing in a paper.
- δ=0.500890640842 for {4,…,128} is the authors' certified value; our D1 would
  RE-certify independently, not assume it.
- Whether Rickards/Stange already have minimality/threshold results in
  preparation is unknown — check arXiv listings again before committing.

# COROLLARY — the zero set of Z_{G_5} is not contained in the critical line

Scope-honest corollary note, 2026-08-15. Lane G.
Parent: `THEOREM_G5_OFFLINE_ASSEMBLY.md` (v2, DECLARED, five adversarial
rounds).
Ruling in force: `plans/wayfinder/rh-goals/tickets/flagship-statement-ruling.md`
(V1) — the "arithmeticity law" framing is REFUTED as stated; only the
localized-resonance statement is defensible. This note claims nothing
beyond one pin.

## Setting and notation

G_5 = Hecke triangle group, λ_5 = 2cos(π/5) = golden ratio; X_5 = G_5\H
the non-arithmetic finite-area hyperbolic orbifold; Z_S = Z_{G_5} its
Selberg zeta function, meromorphically continued to C.

Write

  Λ := { s ∈ C : Z_S(s) = 0 },
  Λ° := Λ ∩ { 0 < Re(s) < 1, Im(s) ≠ 0 }   (the non-real strip zeros),
  L  := { s ∈ C : Re(s) = 1/2 }            (the critical line).

Λ° is the bookkeeping-clean object: it excludes the real-axis zeros
(trivial zeros at the non-positive integers/half-integers coming from the
identity contribution, and the small-eigenvalue parameters s ∈ (1/2, 1]),
which are present for *every* finite-area surface and carry no
information. See "Bookkeeping" below.

## Corollary (certified)

**COROLLARY 1.** There exists s* ∈ Λ° with

  |Re(s*) − 0.4538951800749447| ≤ 10⁻⁶,
  |Im(s*) − 5.7635372417301305| ≤ 10⁻⁶.

In particular

  Re(s*) ≤ 0.4538962 < 1/2,   δ := 1/2 − Re(s*) ≥ 0.0461038,

so s* ∉ L. Hence

  **Λ° ⊄ L :** the non-real strip zeros of the Selberg zeta function of
  the non-arithmetic orbifold X_5 are *not* all on the critical line,
  and the deviation is quantitative — at least 0.0461038 in real part.

Equivalently, in scattering language (assembly link 7): X_5 has a
scattering resonance at s*, with essential gap δ ≥ 0.0461038.

**COROLLARY 2 (the vertical-line reading, exactly as far as it goes).**
No single vertical line V_c = { Re(s) = c } with c = 1/2 contains Λ°.
Therefore the "all non-real strip zeros on one distinguished vertical
line" picture — which *does* hold, at the level of the arithmetic
controls' data, for the arithmetic members q = 3, 4, 6 where the strip
zeros are pinned to the ζ(2s) line — fails for q = 5.

This is a refutation of the c = 1/2 line only. It is **not** a refutation
of "some other single vertical line", and not of "finitely many vertical
lines": one certified pin cannot exclude the hypothesis Λ° ⊂ V_{0.45390}.
Excluding one line in general needs two certified pins at distinct real
parts; that remains open (see Scope limits, item 4).

## Proof

Immediate from the parent theorem. The assembly's THEOREM states that
Z_S has a zero s* with |Re(s*) − 0.4538951800749447| ≤ 10⁻⁶ and
|Im(s*) − 5.7635372417301305| ≤ 10⁻⁶, obtained as follows: the certified
finite winding + closed-contour exclusion (link 1, R3b receipt: 284 Acb
subarcs, min margin ≥ 3.43786e-8, winding 1) together with the finite-section
identity (link 2), the Gohberg–Krein/Simon determinant comparison with
machine constants (link 3), and the argument-principle homotopy (link 4)
place exactly one zero of det(1 − L_{s,+}) in Box; link 4b transports that
zero to the MMS Banach determinant on Ω* ⊃ Box; link 5 shows the K_s
divisor cannot cancel it on Box; and MMS Theorem 6.4 (link 6),
Z_S = det(1−L_{s,+})·det(1−L_{s,−})/det(1−K_s), with det(1−L_{s,−})
analytic near Box, converts the determinant zero into a zero of Z_S of
multiplicity at least that of the + factor. Since Im(s*) ≈ 5.7635 ≠ 0 and
0 < Re(s*) < 1, s* ∈ Λ°. The interval bound Re(s*) ≤ 0.4538951800749447 +
10⁻⁶ = 0.4538962 < 1/2 gives δ ≥ 1/2 − 0.4538962 = 0.0461038, so s* ∉ L
and Λ° ⊄ L. ∎

## Bookkeeping: zeros and poles that must not be miscounted

1. **Real-axis zeros.** Z_S of any finite-area surface has zeros on the
   real axis: the trivial zeros from the identity/elliptic contribution
   and the parameters of the discrete spectrum below 1/4 (s ∈ (1/2, 1]).
   These lie off L but are known and uninformative, which is exactly why
   the corollary is stated for Λ° (Im ≠ 0), not for Λ. Stating "Λ ⊄ L"
   would be true but vacuous.

2. **The K_s divisor.** Per assembly link 5 (KS_GATE_REPORT.md; Lean v17
   `KsZeroLattice`; 90-digit crosscheck KS_CROSSCHECK.md), the zero set of
   det(1 − K_s) is the exact lattice s = −n + iπk/a_q, all with Re(s) ≤ 0.
   In the factorization these are *poles* of the quotient, not zeros of
   Z_S, and they lie at Re ≤ 0, hence outside the strip 0 < Re(s) < 1 and
   outside Box (Re ≈ 0.454 > 0). They therefore (a) cannot cancel the
   certified determinant zero and (b) contribute nothing to Λ°. No other
   divisor bookkeeping is required in Box.

3. **Multiplicity.** The certified winding is 1 for the + factor in Box;
   link 6 gives multiplicity of Z_S at s* at least that of the + factor.
   The corollary asserts existence only and is insensitive to the exact
   multiplicity.

4. **Sector label.** L_{s,+} is the MMS P-symmetric (CF-reflection)
   sector, which is *not* the geometric even/odd Maass sector. No parity
   label is attached to s* here, per the assembly's convention-honesty
   section.

## Scope limits — what is NOT claimed

1. **Nothing about all zeros.** No claim that Λ° is disjoint from L, that
   "most" zeros are off the line, or that any *other* specific zero is
   off the line. Exactly one zero is localized.

2. **No density, counting, or distribution claim.** No resonance-counting
   asymptotic, no essential-spectral-gap theorem for X_5, no statement
   that δ ≥ 0.0461038 is the maximal gap or that it is attained by the
   first resonance. δ is a lower bound at one certified pin.

3. **No family claim.** Nothing is asserted for G_q, q ≠ 5. The family
   statement ("every non-arithmetic Hecke group has an off-line
   resonance") is an open ticket (`family-offline-theorem.md`), not a
   consequence of this corollary.

4. **No "finitely many lines" refutation, and no single-line refutation
   in general.** Corollary 2 excludes c = 1/2 only. The G_5 scatter
   statistics and the additional B3 pins are, at this date,
   winding-certified only in part (see
   `tickets/winding-certificates-q4q6.md`: 5/5 certified-modulo-heuristic,
   with the tail heuristic shown non-monotone at one box corner). Until a
   second G_5 pin at a *distinct* real part is certified to the same
   standard as s*, "the G_5 zeros lie on no single vertical line" stays
   EMPIRICAL.

5. **No "arithmetic ⟺ critical line" law.** V1 REFUTED that framing:
   the arithmetic Hecke triangle groups {3,4,6} form one commensurability
   class (one data point), and the arithmetic-side and non-arithmetic-side
   protocols are not comparable. The contrast noted in Corollary 2 is
   descriptive of the data, not a proved equivalence, and must not be
   written as a law, a criterion, or a conjecture with evidential weight
   in the flagship paper.

6. **No claim of unconditionality beyond the dependency ledger.** The
   result is computer-assisted. It rests on machine-certified Arb/Acb
   interval receipts (links 1, 3-constants, 5), Lean-proved abstract
   joints (Aristotle v17/v18/v19, axiom-clean), cited published theorems
   (Simon, "Notes on infinite determinants," Adv. Math. 24 (1977)
   Thm 4.2 with Lidskii Cor. 4.3; Grothendieck, Résumé Thm 8; MMS Thm
   6.4; standard
   Selberg/scattering theory), and short self-contained paper-proofs. The
   resonance *interpretation* (link 7) is citation-level standard theory,
   not re-proved here; the determinant *localization* (Corollary 1's
   displayed inequalities) does not depend on it.

## Receipts pointers

- Parent theorem and 8-link chain:
  `research_notes/rh_goals_2026-08-14/lane_g/THEOREM_G5_OFFLINE_ASSEMBLY.md`
- Winding / contour certificate: `R3B_FLAGSHIP_CERT_RECEIPT.json`
  (384-bit Arb/Acb; `all_theorem_gates_pass = True`; 284 subarcs; min
  margin ≥ 3.437864e-8 (rounded down); winding 1, ball width 7.81e-114)
- Tail bound receipt (R2): T_tail(160) = 6.26786e-22; F_R(160) = 1.77974e-6;
  ‖L‖₁ ≤ 17.2911968
- Hilbert→Banach transport: `TB_R5_DETERMINANT_IDENTIFICATION.md` v3.1 and
  `E1_ENLARGED_CONTRACTION_RECEIPT.json`
  (sha256 cd1dc6f409ebca7852bc12a9607b4d2a2f6a10b10be3590055e50ee62ad37187;
  ρ̂ ≤ 0.9484; min clearance ≥ 1.0023)
- K_s divisor gate: `KS_GATE_REPORT.md`, `KS_CROSSCHECK.md`, Lean v17
  `KsZeroLattice`
- Adversarial review chain: `ADVERSARIAL_REVIEW_V{4,5,6,7,8}*`
- Statement ruling (what may not be claimed):
  `plans/wayfinder/rh-goals/tickets/flagship-statement-ruling.md`
- Ticket: `plans/wayfinder/rh-goals/tickets/no-vertical-line-corollary.md`

## Obstruction noted while drafting

The assembly supports Corollary 1 fully. It does **not** support the
ticket's stronger headline ("the G_5 data are inconsistent with any
single-vertical-line structure"): the assembly certifies exactly one
zero, at one real part. A single pin refutes the line Re = 1/2 and
nothing more. The B3 pins that would supply a second distinct certified
real part are, per the q=4/q=6 winding ticket, certified only
modulo a tail heuristic that was shown non-monotone at one box corner.
Corollary 2 is therefore stated in the weak form the certificates carry,
and the general single-line refutation is listed as open.

## UPGRADE 2026-08-26 — Scope-limit item 4 DISCHARGED: no single vertical line

The condition item 4 demanded — "a second G_5 pin at a *distinct* real
part … certified to the same standard as s*" — is now met:
`THEOREM_G5_SECONDPIN_ASSEMBLY.md` (STATUS: REFEREED — PROMOTED
2026-08-26; two cold seats, both PASS-WITH-CORRECTIONS, corrections
applied) certifies s₂ with
  Re(s₂) ∈ [0.41054273549473627, 0.41054473549473627],
  Im(s₂) ∈ [7.81976724701551188, 7.81976924701551188],
winding 1 (simple), same contour standard as s*.

**COROLLARY 3 (two-pin; ends the EMPIRICAL status of item 4).**
Λ° contains two zeros with certified real-part intervals
  Re(s*) ⊂ [0.45389418007494470, 0.45389618007494470],
  Re(s₂) ⊂ [0.41054273549473627, 0.41054473549473627],
disjoint with closed-interval separation ≥ 0.04334944458020843 > 0.
Hence **no single vertical line V_c contains Λ°, for ANY c ∈ ℝ**: for
each fixed c at least one of the two certified real parts differs from
c. The hypothesis Λ° ⊂ V_{0.45390} left open by Corollary 2 is refuted.
Machine-verified logical core: no_common_line + pin gap lemmas in
projects/aristotle_dispatch_v34/project_aristotle/TwoPinNoLine.lean
(sorry-free; axioms propext, Classical.choice, Quot.sound). The φ_5
scattering-side consequence and the NOGO discharge live in
NOGO_METATHEOREM_III_DRAFT.md (REFEREED — PROMOTED; NOGO-OPEN-1
CLOSED at its stated standing). Items 1–3 and 5 above are unchanged.

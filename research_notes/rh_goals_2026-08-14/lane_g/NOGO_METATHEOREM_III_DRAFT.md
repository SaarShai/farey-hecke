# Metatheorem III: A ⊭ P_line(c) for every c — NOGO-OPEN-1 discharged via the two certified pins

STATUS: **REFEREED — PROMOTED 2026-08-26.** Gate (i): the S2 assembly
THEOREM_G5_SECONDPIN_ASSEMBLY.md passed its full referee cycle (seats
fable + sol, both PASS-WITH-CORRECTIONS, all corrections applied;
STATUS: REFEREED — PROMOTED). Gate (ii): this note passed its own cold
adversarial referee (NOGO_METATHEOREM_III_REFEREE.md,
PASS-WITH-CORRECTIONS; all 5 exact required corrections applied
2026-08-26, this revision). Per the referee's closing ruling,
**NOGO-OPEN-1 is CLOSED** at the explicitly stated citation /
computer-assisted standing below.

## What was upgraded

NOGO_METATHEOREM_SOL.md §5.1 (NOGO-OPEN-1, verbatim): exhibit
M = (φ, 𝒟) ∈ 𝔐(A) and two nonreal zeros ρ₁, ρ₂ of φ with
1/2 < Re ρᵢ < 1 and Re ρ₁ ≠ Re ρ₂. "Any such M gives A ⊭ P_line(c)
**for every c simultaneously**, and upgrades the slogan 'generic
machinery cannot prove on-line rigidity' from a claim about P_naive to a
claim about the genuine RH-analogue."

## The exhibition

Witness data (referee correction 1): let 𝒟₅ = (d₅(n), g₅,ₙ)ₙ≥₁ be the
Hejhal/FJS Dirichlet data used in the q = 5 A4 receipt of
NOGO_METATHEOREM_SOL.md §2, and set **M₅ = (φ₅, 𝒟₅)** — the scalar
scattering determinant of the Hecke triangle group G_5 with its
Dirichlet-series data. 𝔐(A) contains pairs, not bare functions.

1. **Membership.** M₅ ∈ 𝔐(A) by NOGO_METATHEOREM_SOL.md §3.2 (breadth
   lemma: every finite q ≥ 3, proved row by row in §2), at the caveat
   level of §5.3 as superseded by §8 (see Standing below).
2. **Two zeros, distinct real parts.** From the two certified
   Selberg-zeta pins via the cited FJS divisor step, followed by the
   Lean-verified order-preserving pole-to-zero implication under
   φ(s)φ(1−s) = 1 (referee correction 3; the verified artifact is the
   nested returned file
   projects/aristotle_dispatch_v33/…/Scat1Lemma31Reflection.lean —
   Lean formalizes ONLY that implication, not FJS, MMS, or φ₅ itself):
     ρ₁ = 1 − s₁: Re ∈ [0.54610381992505530, 0.54610581992505530],
                  Im ∈ [−5.7635382417301305, −5.7635362417301305];
     ρ₂ = 1 − s₂: Re ∈ [0.58945526450526373, 0.58945726450526373],
                  Im ∈ [−7.81976924701551188, −7.81976724701551188].
   No conjugation enters: ρᵢ = 1 − sᵢ (referee correction 2). Both
   nonreal (imaginary intervals strictly negative), both real-part
   intervals strictly inside (1/2, 1), closed-interval separation
   exactly 0.04334944458020843 > 0, hence Re ρ₁ ≠ Re ρ₂ certified.
   Sources: THEOREM_G5_SECONDPIN_ASSEMBLY.md (REFEREED — PROMOTED) +
   THEOREM_G5_OFFLINE_ASSEMBLY.md (first pin, DECLARED).

## METATHEOREM III (promoted; fixed-witness quantifiers explicit)

> **There exists one M₅ = (φ₅, 𝒟₅) ∈ 𝔐(A)** — the witness above —
> **such that for every c ∈ (1/2, 1), M₅ does not satisfy P_line(c).
> Hence for every c ∈ (1/2, 1), A ⊭ P_line(c).**
> One common countermodel serves all c (referee correction 4): for any
> fixed c, at least one of Re ρ₁ ≠ Re ρ₂ differs from c, so a certified
> zero of φ₅ violates P_line(c). Consequently no derivation from A
> alone can establish **any member of the family P_line(c)** — the
> genuine RH-analogue family, not merely P_naive. Any argument that
> appears to derive some P_line(c) from the shared axioms contains an
> error, and the error can be exhibited: apply it to M₅.
>
> **Standing (referee correction 5, part of the theorem block):** this
> result holds at the caveat level of NOGO_METATHEOREM_SOL.md §§3.2/5.3
> as superseded by §8, and at the computer-assisted / citation standing
> of the two pin assemblies' dependency ledgers. The scope is exactly
> the family P_line(c), c ∈ ℝ — not every statement informally
> describable as "on-line rigidity."

The Lean file projects/aristotle_dispatch_v34/project_aristotle/
TwoPinNoLine.lean additionally machine-verifies the pure logical core
(no_common_line: two distinct-real-part zeros refute every vertical
line simultaneously; exact gap 4334944458020843/10^17; disjointness;
distinct-Re) sorry-free, axioms [propext, Classical.choice, Quot.sound].

## Why this route is free of the Sel90 debt

Metatheorem I consumes the LAW, which carries the undischarged
[Sel90, Lemmas 1, 2] citation. The exhibition above does NOT consume the
LAW: the pin chain is contour certificates (machine) + R5 + MMS
Theorem 6.4 + whole-box K_s + FJS divisor + Lean reflection core; the
membership proof is §3.2's row-by-row Hejhal/FJS/MMS receipt table.
Referee-confirmed: independence means the named [Sel90, Lemmas 1, 2]
engine is absent — the route still cites other published
Selberg/scattering results and is NOT citation-free.

## Dependency ledger (carried caveats)

- §5.3 caveats (as superseded by §8): A5 flag superseded; A4
  discreteness source-established by FJS Thm 2.1 (enumeration =
  corroboration); A1/A6 Hejhal/FJS transcriptions cold re-extracted,
  not machine-checked quotations; width-one normalization changes φ by
  the zero-free factor c^(1−2s) (functional equation and divisor
  preserved; disclosed).
- MMS q = 5 heading inconsistency (eq. (34) heading prints q > 5;
  general formulas + Thm 6.4 use odd q ≥ 5) — carried from the S2
  assembly.
- **FJS p. 4 notation inconsistency (found by THIS referee, new):**
  immediately after defining k = Σⱼ dim Vⱼ (degree of singularity,
  = 1 here), FJS prints "k = 0" in a sentence evidently colliding with
  automorphic-weight notation; Theorem 2.1 and the divisor formulas
  retain the degree-of-singularity parameter. Does not alter the
  set-level divisor classification; must be disclosed wherever FJS is
  cited as the scalar-specialization source.
- Both pin assemblies are computer-assisted; dependency ledgers in the
  two assembly documents. The FJS bypass is an INDIRECT,
  citation-backed φ₅ zero certificate (no direct SCAT-EVAL_5
  evaluator exists); the referee ruled §5.1 requires zeros of φ, not a
  specified certification technology, so this meets the standard.

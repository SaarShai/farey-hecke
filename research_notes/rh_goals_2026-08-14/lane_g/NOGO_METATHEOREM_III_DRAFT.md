# Metatheorem III (DRAFT): A ⊭ P_line(c) for every c — NOGO-OPEN-1 discharge via the two certified pins

STATUS: **DRAFT / UNREFEREED / GATED.** This note may not be promoted, and
NOGO-OPEN-1 may not be marked closed, until (i) — SATISFIED 2026-08-26:
THEOREM_G5_SECONDPIN_ASSEMBLY.md passed its full referee cycle (seat 1
fable PASS-WITH-CORRECTIONS, seat 2 sol PASS-WITH-CORRECTIONS; all
corrections applied; STATUS promoted to REFEREED) — and (ii) this note
itself passes a cold adversarial referee (IN FLIGHT). Written
2026-08-26.

## What is being upgraded

NOGO_METATHEOREM_SOL.md §5.1 (NOGO-OPEN-1, verbatim): exhibit
M = (φ, 𝒟) ∈ 𝔐(A) and two nonreal zeros ρ₁, ρ₂ of φ with
1/2 < Re ρᵢ < 1 and Re ρ₁ ≠ Re ρ₂. "Any such M gives A ⊭ P_line(c)
**for every c simultaneously**, and upgrades the slogan 'generic
machinery cannot prove on-line rigidity' from a claim about P_naive to a
claim about the genuine RH-analogue."

## The exhibition

M = (φ_5, 𝒟): the scalar scattering determinant of the Hecke triangle
group G_5.

1. **Membership.** φ_5 ∈ 𝔐(A) by NOGO_METATHEOREM_SOL.md §3.2 (breadth
   lemma: φ_q ∈ 𝔐(A) for every finite q ≥ 3, proved row by row at the
   caveat level of §5.3).
2. **Two zeros, distinct real parts.** From the two certified Selberg-zeta
   pins via the FJS divisor step + Lean reflection core (assembly link 7):
     ρ₁: Re ∈ [0.54610381992505530, 0.54610581992505530]
     ρ₂: Re ∈ [0.58945526450526373, 0.58945726450526373]
   Both nonreal (Im ≈ −5.7635, −7.8198), both real-part intervals
   strictly inside (1/2, 1), rigorous interval separation
   ≥ 0.04334944458020843 > 0, hence Re ρ₁ ≠ Re ρ₂ certified.
   Source: THEOREM_G5_SECONDPIN_ASSEMBLY.md (two-pin consequence) +
   THEOREM_G5_OFFLINE_ASSEMBLY.md (first pin).

## The claim (once gates clear)

> **METATHEOREM III.** A ⊭ P_line(c) for every c ∈ (1/2, 1)
> simultaneously; witness M = (φ_5, 𝒟) with the two certified zeros
> above. Consequently no derivation from A alone can establish ANY
> on-line rigidity statement for the right-strip zeros — the genuine
> RH-analogue, not merely P_naive. Any argument that appears to derive
> P_line(c) for any c from the shared axioms contains an error, and the
> error can be exhibited: apply it to φ_5.

This makes the informal slogan ("any RH proof using only the properties
zeta shares with these systems cannot work") ACTUALLY licensed at the
P_line strength, not merely broader-sounding.

## Why this route is cleaner than Metatheorem I's

Metatheorem I consumes the LAW, which carries the undischarged
[Sel90, Lemmas 1, 2] citation (declared in §5). The exhibition above does
NOT consume the LAW: the pin chain is contour certificates (machine) +
R5 + MMS Theorem 6.4 + whole-box K_s + FJS divisor + Lean reflection
core. Sel90 never enters. Metatheorem III is therefore free of the one
declared citation debt in the NOGO package — subject to referee
confirmation of this dependency claim.

## Honest blockers inherited (must be carried by the referee)

- D11's blocker ("no certified zero of any φ_q for non-arithmetic q";
  SCAT-EVAL_q OPEN) is discharged here ONLY through the Selberg-zeta
  bypass: the FJS completed-zeta divisor identification (banked PDF,
  lane_p/literature/FJS_completed_zeta_divisor.pdf, sha 36c9d020…7228)
  + the one-cusp scalar specialization (MMS) + the Lean reflection core
  (order-preserving pole↔zero under φ(s)φ(1−s)=1). No direct φ_5
  zero-minus-pole certifier exists; the referee must rule whether the
  bypass meets NOGO-OPEN-1's standard for "zeros of φ".
- §3.2 membership carries §5.3's four flagged rows (none a failure).
- Both pin assemblies are computer-assisted; dependency ledgers in the
  two assembly documents.

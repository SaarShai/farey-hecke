# `lg_unconditional` — assembling the all-q onset lower bound with the analytic residuals discharged

## Goal

Verify the assembled onset lower bound

> `Xomega_ge_final : 1/l³ ≤ Xomega l (Tgen l) Sclosed`   (for `q = m+2 ≥ 5`, `l = 2cos(π/q)`)

with the two analytic residuals `hEfloor` and `hAgreePrefix` now PROVED inside the file, and the
keystone instantiated on the CONCRETE genuine scalar map `Tgen l p = (b, −a + (kfloor l p)·λb)`.

This is the faithful no-confinement onset keystone
(`LgConfinement.Xomega_ge_no_confinement`, reproduced verbatim here as
`Xomega_ge_no_confinement`) with:

  * **§A** the uniform E-floor `hEfloor_keystone` (q ≥ 5) discharged (byte-matching `lg_efloor_lean`);
  * **§B** the bounded-prefix `k=1` agreement `hAgreePrefix_genuine` PROVED by induction over the
    `k=1` prefix from the single-step law `genuine_step_eq_Mmap_of_bracket` (= `Tgen_eq_Mmap_of_isK1`);
  * **§C/§D** the genuine one-step ejection carried as the single named genuine-corridor input and
    the keystone assembled.

## Faithfulness anchors (VERBATIM, do not rewrite)

`lamq`, `Pgen`, `Mmap`, `Eform`, `Dcorr`, `alphaC`, `rhoC`, `EfloorQ`, `kfloor`, `XomegaSet`,
`Xomega` are reproduced byte-for-byte from the sealed onset objects
(`UniformOnset.Pgen`, `BCZHeckeRotationArc.Mmap`/`kfloor`, the `lg_confinement` keystone).  The
conclusion is the GENUINE `1/l³ ≤ Xomega l (Tgen l) Sclosed`.

## Hypothesis classification of `Xomega_ge_final`

DEFINITIONAL: `hm : 3 ≤ m`, `hl : l = lamq (m+2)`, `hne` (class inhabited), `hpcorr` (section ⊆
corridor), `hK1` (`isK1 ⟺ kfloor=1` floor bracket).

PROVED here (not carried): `hEfloor`, `hAgreePrefix`.

NON-DEFINITIONAL residual carried: `hEject` (orbit-wide one-step ejection; reduces to the
SOS-proved `genuine_hEject_deepmid` + the genuine deep-mid corridor data, TRUE on every realized
section, not derivable from the `Boundary` cusp data alone).

## q = 3, 4

`hEfloor` is FALSE at q = 3, 4; the uniform E-floor is q ≥ 5 (`hm : 3 ≤ m`).  The arithmetic cases
q = 3, 4 are covered by the separate `OnsetEqualityLowQ` route (cited, not re-proved here).

## Axiom audit

Every theorem is sorry-free.  Expect `[propext, Classical.choice, Quot.sound]` only — NO `sorryAx`.
The residual is carried in the HYPOTHESES of `Xomega_ge_final`, not as an axiom or `sorry`.

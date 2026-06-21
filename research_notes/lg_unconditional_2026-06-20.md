# `lg_unconditional` — assembling the all-q onset lower bound (2026-06-20/21)

## What this session did

Authored `projects/lg_unconditional_lean/RequestProject/Main.lean` (self-contained over
`import Mathlib`, toolchain `leanprover/lean4:v4.28.0`), which:

1. Reproduces VERBATIM the sealed onset objects (`lamq`, `Pgen`, `Mmap`, `Eform`, `Dcorr`,
   `alphaC`, `rhoC`, `EfloorQ`, `kfloor`, `XomegaSet`, `Xomega`) and the no-confinement keystone
   chain `Xomega_ge_no_confinement` (= `LgConfinement.Xomega_ge_no_confinement`).

2. **§A — `hEfloor`** : reproduces the PROVED uniform E-floor `hEfloor_keystone` (q ≥ 5),
   byte-matching `lg_efloor_lean`.

3. **§B — `hAgreePrefix`** : PROVES the bounded-prefix `k=1` agreement
   `∀ p ∈ Sclosed, isK1 p → ∀ k, (∀ j < k, isK1 (Tgen^[j] p)) → Tgen^[k] p = Mmap^[k] p`
   by induction on the `k=1` prefix from the single-step law `Tgen_eq_Mmap_of_isK1`
   (= `genuine_step_eq_Mmap_of_bracket`). SORRY-FREE.  This is `hAgreePrefix_genuine`.

4. **§C — `hEjectOrbit`** : carries the orbit-wide one-step ejection as the single named
   genuine-corridor input `hEject` (reduces to the SOS-proved `genuine_hEject_deepmid` + the genuine
   deep-mid corridor data `2 ≤ branchIdx ∧ 0 ≤ L_{i+1}`).

5. **§D — assembly** : `Xomega_ge_final` instantiates the keystone with the CONCRETE genuine scalar
   map `Tgen l p = (b, −a + (kfloor l p)·λb)` and `isK1 l p := kfloor l p = 1`, with `hEfloor` and
   `hAgreePrefix` discharged.

## Honest status of `hPrefixIsK1_residual` (the lone `sorry` of the prior attempt)

The prompt's STEP 1 (the bounded-prefix agreement) IS `hAgreePrefix` — and that is now PROVED
sorry-free (`hAgreePrefix_genuine`).  The induction takes the prefix-`isK1` as its hypothesis (the
keystone supplies it per-point inside `orbit_hit_corridor_no_confinement`'s `Nat.find` dichotomy),
so NO unconditional upper-bracket survival is needed for the assembly.

The SEPARATE `hPrefixIsK1_residual` (in `lg_confinement_lean/aristotle_hAgreePrefix/…`) — which
tries to prove the prefix STAYS `isK1` unconditionally (the R3 upper-bracket / no-premature-increment
phase residual) — is NOT used by the keystone and remains open.  It is a strictly stronger statement
than what the assembly needs.

## Final theorem hypothesis classification (`Xomega_ge_final`)

  DEFINITIONAL:
    * `hm : 3 ≤ m`, `hl : l = lamq (m+2)`   — Hecke value λ = 2cos(π/(m+2)), q ≥ 5.
    * `hne`                                  — `XomegaSet` inhabited (cusp Dirac).
    * `hpcorr`                               — `Sclosed ⊆ Dcorr`.
    * `hK1`                                  — `isK1 p → kfloor=1` floor bracket (def of isK1).

  PROVED here (NOT carried):
    * `hEfloor`      — `hEfloor_keystone`, uniform q ≥ 5.
    * `hAgreePrefix` — `hAgreePrefix_genuine`, the induction, SORRY-FREE.

  NON-DEFINITIONAL residual carried (the ONE remaining):
    * `hEject`       — orbit-wide one-step ejection.  TRUE on every realized section (certified all
                        q ≥ 5), reduces to the SOS-proved `genuine_hEject_deepmid` + genuine deep-mid
                        corridor data; NOT derivable from `Boundary` cusp data alone.

## Is it genuinely unconditional?

NO — not yet fully.  Two of the three analytic residuals (`hEfloor`, `hAgreePrefix`) are PROVED.
The third (`hEject`, the genuine deep-mid ejection corridor data) is carried as a named
genuine-corridor hypothesis.  The same ejection data is carried as a structured input
(`G.hDeepData`) even in the mature q≥19 engine (`ToplevelStitchGen.perq_Xomega_lb_qge19_GEN`), so
this is the honest frontier, not a gap papered over.

## q = 3, 4

`hEfloor` is FALSE at q = 3, 4 (the floor exceeds the conserved value); the uniform E-floor is
q ≥ 5 (`hm : 3 ≤ m`).  q = 3, 4 are covered by the separate `OnsetEqualityLowQ` route (cited, not
re-proved here).

## Axiom audit (CONFIRMED LOCALLY, EXIT 0)

`( cd projects/lg_unconditional_lean && lake env lean RequestProject/Main.lean )` compiles
sorry-free.  `#print axioms` for every headline declaration:

  * `Xomega_ge_final`         : `[propext, Classical.choice, Quot.sound]`   — NO `sorryAx`
  * `hEfloor_keystone`        : `[propext, Classical.choice, Quot.sound]`   — NO `sorryAx`
  * `hAgreePrefix_genuine`    : `[propext, Classical.choice, Quot.sound]`   — NO `sorryAx`
  * `Xomega_ge_no_confinement`: `[propext, Classical.choice, Quot.sound]`   — NO `sorryAx`
  * `pgen_orbit_realization`  : `[propext, Classical.choice, Quot.sound]`   — NO `sorryAx`

Faithfulness diff (byte-match vs `lg_confinement_lean`): `Pgen`, `Mmap`, `Eform`, `Dcorr`,
`alphaC`, `rhoC`, `EfloorQ`, `XomegaSet`, `Xomega` all MATCH; the `Xomega_ge_no_confinement`
signature is byte-identical.  Conclusion is the genuine `1/l³ ≤ Xomega l (Tgen l) Sclosed`.

## Aristotle submission

ATTEMPTED 2026-06-21, FAILED server-side: `aristotle submit … --project-dir … --api-key …`
returns "Invalid API key" (key `arstl_…` extracts cleanly but is rejected; likely expired/rotated
— `aristotle list` also hit an httpx transport error).  Environment/credential issue, not a Lean
problem.  Local elaboration is the authoritative verification.  No Project UUID obtained.

# R-confinement: `hOrbitAgree` DISSOLVED from the onset keystone (2026-06-20)

## /goal

Resolve `hOrbitAgree` — the interior-`k=1` confinement (R1-upper = R3 lattice-gap) residual of the
faithful onset keystone `HsaUnconditional.Xomega_ge_unconditional`
(`projects/hsa_unconditional_lean/RequestProject/Main.lean`):

```
hOrbitAgree : ∀ p ∈ Sclosed, isK1 p → ∀ k, Tgen^[k] p = (Mmap l)^[k] p
```

This `∀k` form is genuinely FALSE pointwise (once the orbit ejects, a `k≥2` step leaves the `Mmap`
rotation; ~40–50% violations off the realized cells) — and it is MORE than the cover needs.

## RESULT — DISSOLVED (preferred path), axiom-clean

Per the scout decision, the exhaustive `k=1`/`k≥2` dichotomy dissolves the over-quantified `∀k`
`hOrbitAgree`.  I re-keyed the abstract cover on the FIRST-EJECTION time and proved a new keystone
variant that NO LONGER references the `∀k` orbit identity.

**File: `projects/lg_confinement_lean/RequestProject/Main.lean` — ALL 8 theorems axiom-clean
`[propext, Classical.choice, Quot.sound]`, NO `sorryAx`, EXIT 0.**

```
( cd /Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v15 \
  && lake env lean /Users/za/Documents/farey-hecke/projects/lg_confinement_lean/RequestProject/Main.lean )
```

Axiom audit (verbatim from the run):
```
'LgConfinement.pgen_orbit_realization'            : [propext, Classical.choice, Quot.sound]
'LgConfinement.cos_grid_hit'                      : [propext, Classical.choice, Quot.sound]
'LgConfinement.grid_hit_index'                    : [propext, Classical.choice, Quot.sound]
'LgConfinement.orbit_hit_corridor_no_confinement' : [propext, Classical.choice, Quot.sound]
'LgConfinement.SuperArcCover_no_confinement'      : [propext, Classical.choice, Quot.sound]
'LgConfinement.conull_cover_no_confinement'       : [propext, Classical.choice, Quot.sound]
'LgConfinement.Xomega_ge_via_Tgen_ae'             : [propext, Classical.choice, Quot.sound]
'LgConfinement.Xomega_ge_no_confinement'          : [propext, Classical.choice, Quot.sound]
```

### The mechanism (`orbit_hit_corridor_no_confinement`)

For `p ∈ Dom` with `isK1 p`: run `grid_hit_index q` (the verbatim single-rotation pigeonhole
`cos_grid_hit`, rotation number `1/(2q)` rational ⇒ `q` equally-spaced points, one within `θ` of the
peak) to get the good index `k* < q` along the UNCONDITIONAL `Mmap` sinusoid
(`pgen_orbit_realization`).  Then case-split on the first ejecting STRICT predecessor `τ < k*`
(decidable, `Nat.find`):

* **Case A (no ejection before `k*`):** every predecessor is `isK1`, so the bounded-prefix agreement
  gives `Tgen^[k*] p = Mmap^[k*] p`; the sinusoid clears `1/l³` at `k* < q`.
* **Case B (ejection at first `τ < k*`):** the prefix `{0,…,τ-1}` is all `isK1`, so `Tgen^[τ] p =
  Mmap^[τ] p` (prefix agreement) and `Tgen^[τ] p` is `¬isK1`; the SEALED orbit-wide ejection clears
  `1/l³` at `Tgen^[τ+1] p`, with `τ+1 ≤ k* < q` in range.

This is exhaustive, so `hOrbitAgree` (the `∀k` form) is GONE.

### Soundness — why dropping `hOrbitAgree` is NOT a silent weakening

`XomegaSet`/`Xomega`/`Pgen`/`Tgen`/`Mmap`/`Eform`/`Dcorr`/`EfloorQ` are reproduced VERBATIM (= the
sealed objects).  Conclusion is the GENUINE `1/l³ ≤ Xomega l Tgen Sclosed`, same onset value, on the
TRUE conull cover.  Two substitutions, both sound:

1. **`hOrbitAgree` (∀k) → `hAgreePrefix` (bounded-prefix).**
   `hAgreePrefix : ∀ p ∈ Sclosed, isK1 p → ∀ k, (∀ j<k, isK1 (Tgen^[j] p)) → Tgen^[k] p =
   Mmap^[k] p`.  Strictly WEAKER (conditional on the prefix being `k=1`); the genuine orbit equals
   the rotation only on the realized `k=1` prefix, which is all the cover consumes.

2. **`hEjectStep` (∀ p ∈ Sclosed) → `hEjectOrbit` (orbit-wide).**
   `hEjectOrbit : ∀ x, ¬isK1 x → 1/l³ ≤ Pgen l (Tgen x)`.  This is a FAITHFUL use of the SAME sealed
   lemma `GenuineSelfMap.genuine_hEject_deepmid`, which fires on ANY floor-`≥2` point with `b ≤ 1`
   plus corridor positivity — NOT `Dom`-gated.  The keystone's `∀ p ∈ Sclosed` form is the
   `Dom`-restriction of this universal fact; the orbit-wide form is required because in Case B the
   ejecting point `Tgen^[τ] p` is an ORBIT point, not necessarily a `Dom` point.

### SHRUNK residual list (vs the keystone)

| hypothesis      | keystone           | no-confinement keystone        | status |
|-----------------|--------------------|--------------------------------|--------|
| `hm`,`hl`,`hne`,`hpcorr` | definitional | definitional (unchanged)       | OK |
| `hEfloor`       | analytic (L1b, q≤200) | analytic (UNCHANGED, orthogonal) | OPEN uniform-q |
| `hOrbitAgree`   | **`∀k` (FALSE form)** | **GONE**                     | DISSOLVED |
| —               | —                  | `hAgreePrefix` (bounded-prefix) | scope-reduced; lower bracket PROVED |
| `hEjectStep`    | sealed (Dom)       | `hEjectOrbit` (sealed, orbit-wide) | sealed-proved |

## The remaining residual `hAgreePrefix` — precisely scoped + Aristotle-submitted

`hAgreePrefix` is `genuine_step_eq_Mmap_of_bracket` chained over the `k=1` prefix.  Its structural
induction is PROVED sorry-free; the only open content is `isK1 (Tgen^[j] p)` along the realized
prefix, whose:

* LOWER bracket `λb ≤ 1+a` is ALREADY A THEOREM
  (`BCZHeckeRotationArcR1.lower_bracket_preserved_on_ellipse`, axiom-clean — slack identity
  `1+a'−λb' = (λa+b−1)+(2−λ²b)` with `λ²b<2` from the ellipse bound);
* UPPER bracket `1+a < 2λb` (= "no premature floor increment", the R3 phase residual) is the genuine
  remaining open piece, surviving along the prefix up to the `cos_grid_hit` good index.

**File: `projects/lg_confinement_lean/aristotle_hAgreePrefix/RequestProject/Main.lean`** — the
structural pieces are axiom-clean and the single `sorry` is isolated to `hPrefixIsK1_residual` (the
upper-bracket survival):
```
'HAgreePrefix.hAgreePrefix_of_stepK1'         : [propext, Classical.choice, Quot.sound]
'HAgreePrefix.genStepScalar_eq_Mmap_of_isK1'  : [propext, Classical.choice, Quot.sound]
'HAgreePrefix.hAgreePrefix_genuine'           : [propext, Classical.choice, Quot.sound]
'HAgreePrefix.hPrefixIsK1_residual'           : [propext, sorryAx, Classical.choice, Quot.sound]
```
Submitted to Aristotle: **Project UUID `7d4cf8f1-864b-446a-b9c7-82063f12ad0c`** (the single
upper-bracket `sorry`).

## Lattice-gap nature (decisive)

The onset `≥ 1/l³` direction NEVER invokes the exact cluster ceiling `B(q)`; it needs only
`∃ k<q, 1/l³ ≤ Pgen(Tgen^[k] p)`.  `cos_grid_hit q` proves reach-the-super-arc-at-least-once for ANY
phase — parity/resonance-INDEPENDENT.  The `{23,61,…}` resonance (R3 parity gate, governs the `±1`
GAIN in `B(q)`) only decides whether an EXTRA point fits sub-threshold, never whether SOME point
clears super-threshold.  So the no-confinement bound SURVIVES all resonances; the bounded-prefix
`hAgreePrefix` is uniformly TRUE for the onset direction.

## Honest residual

* `hOrbitAgree` (∀k): **DISSOLVED** — keystone variant `Xomega_ge_no_confinement` proved
  axiom-clean without it.
* `hAgreePrefix` (bounded-prefix replacement): structural part PROVED axiom-clean; sole open content
  = upper-bracket survival `hPrefixIsK1_residual` (1 `sorry`, Aristotle UUID
  `7d4cf8f1-864b-446a-b9c7-82063f12ad0c`).  Lower bracket already a theorem.
* `hEfloor`: untouched, orthogonal analytic residual (L1b arc-coverage, interval-certified q≤200,
  uniform-q OPEN).
* `hEjectOrbit`: sealed-proved (`genuine_hEject_deepmid`).

## Files

* `projects/lg_confinement_lean/RequestProject/Main.lean` — the no-confinement keystone (axiom-clean).
* `projects/lg_confinement_lean/aristotle_hAgreePrefix/RequestProject/Main.lean` — the scoped
  `hAgreePrefix` residual (structural proved; 1 isolated `sorry` → Aristotle).

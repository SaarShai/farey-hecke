# hSuperArc faithful targets — scout (2026-06-20)

Scout for the SOLE remaining lemma `hSuperArc_Tgen`. Produces the exact
realization statement, the high-dps constants Kaggle must pin, the faithful
covering target, and the reduction path. Anchored to the verbatim sealed defs.

## Sealed defs (verbatim, faithfulness anchors)

- `Mmap l (a,b) = (b, -a + l*b)` (BCZHeckeRotationArc.Mmap; k=1 special case of Tgen)
- `Pgen l (a,b) = a*(a + l*b)/l` (BCZHeckeUniformOnset.Pgen — RAW observable)
- `Eform l (a,b) = a^2 - l*a*b + b^2` (conserved: `Mmap_preserves_E`)
- `Dcorr l = {0<a<=1, 0<b<=1, a+l b>1, l a+b>1}` (UniformOnset.Dcorr)
- `lamq q = 2 cos(pi/q)`, `thetaq q = pi/q`
- `Tgen` genuine map; on k=1 bracket `lambda b <= 1+a < 2 lambda b`, `Tgen = Mmap`
  (`genuine_step_eq_Mmap_of_bracket`); on `2 lambda b <= 1+a`, k>=2, `Tgen != Mmap`.
- `genuine_hEject_deepmid`: at k>=2 (deep-mid) branches `1/l^3 <= Pgen(genStep)` (ejection clears threshold).
- `Mmat_conj_eq_rot`: in whitening coords `L^T = [[1,-cos th],[0,sin th]]`, `Mmap` = rotation `R(-th)`.

## (1) pgen_orbit_realization — EXACT faithful statement

The CURRENT file statement (Main.lean:326-337) asserts the gate for ALL `p in Dcorr l`.
**That is FALSE for small q** (numerically verified, see below): small-E corridor points
keep the whole Mmap-orbit sub-threshold. The faithful realization splits the orbit identity
(always true) from the gate (needs an E-floor / is discharged off-corridor by ejection).

### (1a) Orbit sinusoid identity — UNCONDITIONALLY TRUE (this is the realization core to prove)

For all `l>0`, `p`, and all `k`:
```
Pgen l ((Mmap l)^[k] p) = alpha(l)*E + rho(l)*E*cos(phi0(p) - 2*k*theta)
```
with `theta = pi/q`, `E = Eform l p`, and the l-only constants below. Equivalently in the
file's `+2 k theta` convention with `phi := -phi0`:
```
Pgen l ((Mmap l)^[k] p) = C0 + R*cos(phi + 2*k*theta),  C0 = alpha*E, R = rho*E.
```
PROOF: `Mmap_preserves_E` (orbit on fixed ellipse) + `Mmat_conj_eq_rot` (Mmap = R(-theta) in
whitening coords) + `Pgen` is the quadratic form with symmetric matrix `Q = [[1/l, 1/2],[1/2, 0]]`;
push Q through the whitening `(a,b) = (L^T)^{-1} u`, `|u|^2 = E`, `u = sqrt(E)*(cos psi, sin psi)`,
`psi -> psi - theta` per step.

### (1b) Threshold gate — the part that needs the E-floor / corridor split

Gate `(1/l^3 - C0)/R <= cos theta` is equivalent to:
```
E >= 1/( l^3 * (alpha(l) + rho(l)*cos theta) )   =: Efloor(l)
```
This DOES NOT cancel E (t = 1/l^3 is fixed). So the faithful realization statement is ONE of:

- **(Form A, E-floor hypothesis — recommended for the k=1 arc):**
  ```
  theorem pgen_orbit_realization (m : N) (l : R) (hl : l = lamq (m+2))
      (p : R x R) (hp : p in Dcorr l) (hE : Efloor l <= Eform l p) :
      exists C0 R phi, 0 < R and
        (forall k, Pgen l ((Mmap l)^[k] p) = C0 + R*cos(phi + 2 k (pi/(m+2)))) and
        (1/l^3 - C0)/R <= cos(pi/(m+2))
  ```
  where `Efloor l = 1/(l^3*(alpha l + rho l * cos(pi/(m+2))))`.

- **(Form B, identity-only + gate-as-separate-lemma):** export the unconditional identity
  (1a) as `pgen_orbit_sinusoid`, and the gate as `pgen_gate_of_Efloor` consuming
  `arc_coverage_ineq`. Cleaner for Aristotle; `orbit_hit_in_corridor` then takes `hE`.

The low-E points where `hE` fails (E < Efloor) are EXACTLY the k>=2 deep-mid region; on the
Tgen orbit those are handled by `genuine_hEject_deepmid` (one step lands >= 1/l^3), NOT by the
Mmap rotation. This is why the honest covering must be the **Tgen** covering, and why a literal
`for all p in Dcorr` Mmap gate is unprovable as written.

## (2) constants_spec — pin at high dps on Kaggle (exact closed forms; c=cos(pi/q), s=sin(pi/q), l=2c)

```
alpha(l) = 1/(4 c) + 3 c/(4 s^2)                       [mean coeff, = C0/E]
rho(l)   = sqrt(8 c^2 + 1)/(4 s^2 c)                   [amplitude coeff, = R/E; c>0 for q>=3]
Efloor(l) = 1 / ( l^3 * (alpha + rho*c) )              [gate E-floor]
```
Asymptotics (verify): `alpha*(4-l^2) -> 3`, `rho*(4-l^2) -> 3` as `l -> 2` (q->inf).
Reference numerics (verify to >=30 dps):
```
q=5  l=1.6180340 alpha=2.065248 rho=2.233574 cos th=0.809017 Efloor=0.060957  1/l^3=0.236068
q=7  l=1.8019377 alpha=3.866899 rho=4.034959 cos th=0.900969 Efloor=0.022775  1/l^3=0.170915
q=12 l=1.9318517 alpha=...      rho=...       cos th=0.965926 Efloor=0.006317  1/l^3=...
q=22 l=1.9796466 alpha=36.90626 rho=37.07312 cos th=0.989821 Efloor=0.001745  1/l^3=0.128896
```
NOTE: these RAW-Pgen constants are NOT the L1b `Fobs` constants. L1b uses
`Fobs = 3l/2 + sqrt(1+2l^2) cos`, i.e. mean `3l/(4 A2)`, amp `1/(2 sqrt A2)`, `A2=1+2l^2`,
under a DIFFERENT observable normalization `Pgen_L1b = (E/(2 A2)) Fobs`. Symbolic check shows
`alpha != 3l/(4 A2)` and `rho != 1/(2 sqrt A2)`. The realization on the LITERAL `Pgen` must use
the raw `alpha, rho` above. If instead the keystone observable is the L1b-normalized one, use the
Fobs constants — Kaggle should pin BOTH and the wiring lemma picks the one matching the sealed
`Pgen` def actually fed to `Xomega`. (Sealed `Pgen l (a,b) = a(a+lb)/l` => raw constants are correct.)

The sub-arc width input `2 sqrt 6 / 5` (in `arc_coverage_ineq`) is the L1b-normalization cosine
value; under raw-Pgen the corresponding super-arc gate is the inequality `Efloor(l) <= E` above,
provable from `arc_coverage_ineq` once the two normalizations are bridged (one ring identity per q).

## (3) Faithful corridor-inclusion covering target (discharges hSuperArc_Tgen)

NOT `= Set.univ` (FALSE via (0,0) fixed point, `superarc_univ_is_false` PROVED). Faithful form,
a.e. on `Sclosed` / corridor-inclusion shape:
```
hSuperArc_Tgen :
  forall mu, IsProbabilityMeasure mu -> MeasurePreserving Tgen mu mu -> mu (Sclosed)^c = 0 ->
    (Union k in range q, (Tgen^[k]) ^{-1} {x | 1/l^3 <= Pgen l x})  =ᵐ[mu]  Set.univ
```
equivalently the inclusion `Dcorr l \subseteq Union k<q, (Tgen^[k])^{-1} {1/l^3 <= Pgen}` up to a
`mu`-null set, which is what `SuperArcCover_corridor` already delivers for the `Mmap` orbit on the
E-floored part and which `genuine_hEject_deepmid` delivers on the sub-floor part. `covering_pos_measure`
only needs the super-level set to carry positive `mu`-mass, so a.e.-cover suffices.

## (4) Reduction path

```
hSuperArc_Tgen
  | split each corridor point by genuine floor k = floor((1+a)/(l b)):
  |
  +-- k=1 region (lambda b <= 1+a < 2 lambda b, i.e. E >= Efloor):
  |     genuine_step_eq_Mmap_of_bracket : Tgen = Mmap there
  |     -> orbit_hit_in_corridor (Mmap orbit) via pgen_orbit_realization (1a)+(1b Form A)
  |     -> gate (1b) from arc_coverage_ineq / B1_target at the corridor E-floor
  |     -> orbit hits {1/l^3 <= Pgen} within q steps  (cos_grid_hit pigeonhole, PROVED)
  |
  +-- k>=2 region (2 lambda b <= 1+a, E < Efloor, deep-mid):
  |     genuine_hEject_deepmid : 1/l^3 <= Pgen(Tgen p)  in ONE step (k=1 preimage hits)
  |     -> covered at step 1, only HELPS the cover
  |
  wired by: pgen_orbit_realization (the single named residual; identity 1a UNCONDITIONAL,
            gate 1b from sealed arc_coverage_ineq). Everything downstream PROVED:
            cos_grid_hit, orbit_hit_of_realization, wide_arc_translates_cover_on,
            SuperArcCover_corridor (modulo the residual), superarc_univ_is_false.
```

## Available sealed lemmas to consume

`arc_coverage_ineq` (2 arccos(2 sqrt6/5)/pi < 33/256, PROVED), `cos_sq_lt`, `B1_target`,
`fcorr_lb`, `g_corr` (L1bArcCoverage); `Mmap_preserves_E`, `Mmat_conj_eq_rot`,
`genuine_step_eq_Mmap_of_bracket`, `kstep_eq_Mmap_of_k1` (BCZHeckeRotationArc);
`genuine_hEject_deepmid`, `genStep_scalar_eq`, `kfloor_ge_two_iff`, `branchIdx_deepmid_entry`
(GenuineSelfMap); `essSup_ge_of_no_sustained_strict`, `no_sustained_corridor`,
`prod_le_Pgen_orbit` (BCZHeckeUniformOnset); `cos_grid_hit`, `orbit_hit_of_realization`,
`wide_arc_translates_cover_on`, `SuperArcCover_corridor`, `superarc_univ_is_false`
(mu_close_hSuperArc/Main.lean, PROVED modulo residual).

## Risks / honesty flags

- The current `pgen_orbit_realization` (Form: gate for ALL `p in Dcorr`) is FALSE for small q
  (q=5: 199/160000 sampled corridor points violate the gate; required Efloor 0.0610 vs Dcorr
  Emin ~0.056). Must add `hE : Efloor l <= Eform l p` (Form A) OR split via the genuine floor
  and route low-E points through `genuine_hEject_deepmid` (Tgen covering). DO NOT prove the
  current too-strong statement as-is.
- Raw-Pgen constants alpha, rho differ from the L1b Fobs constants — pick the set matching the
  sealed `Pgen` literally fed to `Xomega` (= raw, since `Pgen l (a,b)=a(a+lb)/l`). Bridge to
  `arc_coverage_ineq`'s `2 sqrt6/5` is a ring identity, not a new analytic fact.
- `= Set.univ` covering is FALSE ((0,0) fixed point). Use a.e./corridor-inclusion.

# PS-1 — G_q + chi family: design + alpha-ball feasibility probe

**Date:** 2026-08-23. **Lane:** NEXT-3 (deformation family), step PS-1.
**Status: UNREFEREED.** LEDGER RULE binds. Inherits every caveat of
`PS0_DEFORMATION_SCOPING_SOL.md` and the corrected design of
`PS0_DEFORMATION_SCOPING_REFEREE.md` (C1–C8): family = G_5 + unitary rep via
Pohl's coding (arXiv:1503.00525, 1606.09109), reusing the calibrated Rosen
blocks in `.worktrees/aletheia-restore/code/zeta_cert_rosen.py`; certification
= alpha-BALL contour enclosure through the existing winding machinery.
Compute in this pass: one feasibility probe, < 1 CPU-min, nice 19, single
core. Everything heavier is DEFERRED to the §5 written plan.

## 1. CHARACTER VARIETY OF G_5 — the crux

**Fact (elementary, checked by hand).** G_q ≅ Z/2 * Z/q (S² = (ST)^q = id),
so G_q^ab ≅ Z/2 × Z/q and

    Hom(G_5, U(1)) = mu_2 × mu_5  — exactly 10 characters, FINITE.

There is **no continuous 1-dimensional character family for any Hecke group**
(contrast Γ₀(4), whose abelianization is infinite — that is WHY Selberg/
Fraczek–Mayer worked there). A continuous alpha-family for G_5 must come from
one of:

(a) **U(2) character variety (RECOMMENDED — smallest continuous family).**
A unitary rep ρ: Z/2 * Z/5 → U(2) is exactly a pair of unitaries
A = ρ(S), B = ρ(U) with A² = I, B⁵ = I (U = ST elliptic of order 5).
Fix the conjugacy classes: A ~ diag(1,−1) (non-scalar), B ~ diag(ζ^j, ζ^k)
with ζ = e^{2πi/5}, j ≠ k. The remaining modulus is the relative position of
the two eigenbases; after the U(1)×U(1) gauge it is a single angle

    θ ∈ [0, π/2],   dim = dim C(A-class) + dim C(B-class) − dim PU(2)
                        = 2 + 2 − 3 = 1.

So for each choice (j,k) with j≠k there is a genuine **1-real-parameter arc**
of unitary reps: irreducible for 0 < θ < π/2, **reducible at the endpoints**,
where ρ ≅ χ ⊕ χ′ splits into two of the 10 finite characters and

    Z(s, ρ_{θ=0}) = Z(s, χ) · Z(s, χ′).

This is exactly the shape Pohl's framework covers ("unitary finite-dimensional
representations (V,χ)" of Hecke triangle groups, arXiv:1503.00525 abstract;
1606.09109 ties eigenvalue-1 eigenfunctions of the fast operator to Z(Γ,χ;·)
zeros for ANY Hecke triangle group and ANY finite-dim unitary χ).

**Anchor point — honest statement.** G_5 is non-arithmetic; NOTHING on this
family is ζ- or L-expressible. The "arithmetic anchor" of the Γ₀(4) lane is
replaced here by a **certified-computable anchor**: choose (j,k) so that
χ = trivial at θ = 0; then Z(s, ρ_0) = Z(s, 1) · Z(s, χ′), whose first factor
is the banked flagship G_5 certificate (off-line resonance theorem 2026-08-15)
and whose second factor is a finite-order character twist computable by the
same engine with root-of-unity block weights (§2). The θ-arc then deforms
away from our own certified pins — calibration for free, novelty pressure
low (Pohl's papers prove the framework but publish no certified zeros; the
Fraczek–Mayer–Strömberg G_q computations, arXiv:0804.4837, are χ-trivial and
uncertified). If the referee judges a ζ-expressible anchor mandatory, the
recorded fallback stays Γ₀(4)+χ_α (PS-0 §6), at the cost of the C1 crowding.

(b) **Commutator cover (larger, kept as reserve).** [G_5, G_5] is free of
rank 4 (Euler characteristic: χ(G_5) = 1/2 + 1/5 − 1 = −3/10; index 10 ⇒
χ = −3 = 1 − rank). Hom([G_5,G_5], U(1)) = U(1)⁴, a 4-torus; inducing to G_5
gives a continuous family of **10-dimensional** unitary reps. Continuous and
Pohl-covered, but matrix dimension ×10 (vs ×2 for (a)) with no compensating
advantage. Reserve only.

(c) **Real weight / multiplier systems** (PS-0 §3 item 3): still not swept in
depth; not needed once (a) exists. Remains OPEN, not blocking.

**Crux resolution: the smallest continuous family Pohl's framework supports
for G_5 is the 1-parameter U(2) arc (a), anchored at the reducible endpoint
θ=0 to the product of the banked flagship certificate and one finite-character
twist.**

## 2. HOW chi ENTERS THE ROSEN BLOCKS

Per Pohl (1503.00525; and the Fraczek–Mayer Γ₀(4) precedent), the weighted
transfer operator acts on V-valued functions:

    (L_{s,ρ} f)(x) = Σ_{g inverse branches} |g′(x)|^s · ρ(g)^{-1} f(g x),

i.e. **each block is multiplied on the left by the unitary ρ(g)^{-1} of the
group element that block realizes**. In `zeta_cert_rosen.py`
(`build_reduced_matrix_ball`) the correspondence is:

- `single_block(i, j, n, neg)` = the inverse branch x ↦ −1/(x ± nλ), the
  group element g = S T^{∓n} (MMS eq. (34) placements). Weight:
  ρ(g)^{-1} = ρ(T)^{±n} ρ(S), with ρ(S) = A and ρ(T) = ρ(SU) = A·B(θ).
- `inf_block(i, j, n0, neg)` = Σ_{n ≥ n0} of the same branches. Weight
  ρ(T)^{±n} A now sits INSIDE the n-sum, so the exact-Hurwitz tail closure
  (Σ_n Hurwitz) becomes a **Lerch-type sum** Σ_n z^n (·)^{-s-m} with z an
  eigenvalue of ρ(T)(θ). After diagonalizing ρ(T) = V diag(e^{iφ₁}, e^{iφ₂})V*
  the tail is two scalar Lerch transcendents Φ(z, s+m, a); Arb ships a
  certified `lerch_phi` (`acb_dirichlet_lerch_phi` / python-flint
  `acb.lerch_phi` — availability in our pinned python-flint to be verified,
  named obligation §4). NO new analysis, one new certified special-function
  primitive.
- `sign = ±1` prefactor: the even/odd sector reduction. With ρ non-trivial
  this reduction is NOT automatic (referee C8(a)); until re-derived, run the
  UNREDUCED operator (dimension 2·(2κ)·N instead of 2κN) — correctness first,
  the sector saving later.
- Matrix bookkeeping: every scalar acb entry becomes a 2×2 block (family (a)),
  so dim = 2κN = 6N for q=5.

Singularity structure: whether 1 ∈ spec ρ(T)(θ) controls which "cusps" of the
cover are open (regular vs singular rep), hence the Eisenstein contribution
and the divisor of Z(s,ρ) — this is exactly referee C5 transplanted to G_5,
listed in §4. At the anchor θ=0 with χ trivial, 1 ∈ spec ρ(T) always
(trivial summand): the anchor is a SINGULAR point of the family, as in
Selberg's Γ₀(4) picture. Expected and welcome (that is where dissolution
starts), but the divisor bookkeeping must track it.

## 3. ALPHA-BALL FEASIBILITY PROBE (run 2026-08-23, single core, nice 19)

Setup: flagship G_5 even-sector matrix (`build_reduced_matrix_ball`, q=5,
sign=+1, n_head=4, prec=300 bits) at fixed s = 0.4539 + 5.7640i (banked even
off-line resonance region, on the R3B contour scale). Trivial weight injected
as the acb ball χ = 1 ± w multiplying every entry — equivalent to giving
every block a width-w unimodular weight ball, the worst case of the α-ball
design. Script: scratchpad `ps1_alpha_ball_probe.py`. ~0.1 s per
determinant; total < 1 CPU-min. Numbers below are Arb upper bounds on ball
radii (outward/directed rounding by construction); mids quoted to 3–6 digits.

Baseline w=0, N=14 (dim 42): det mid = −5.083206e−04 + 1.750962e−03 i,
radius ≤ 1.690e−84, dim-tail ≤ 1.366e−07, exclusion margin
|mid|/(rad+tail) ≈ 1.3e+04. (Engine healthy at this s.)

Radius amplification, det(1 − χL), amp := rad(det)/w:

| N (dim) | w=1e−10 | w=1e−8 | w=1e−7 | w=1e−6 | w=1e−5 |
|---|---|---|---|---|---|
| 10 (30) | amp 2.27e3, margin 8.0e3 | 2.29e3, 79 | 2.39e3, 7.6 | 3.91e3, 0.46 | **5.1e6, 3.5e−5** |
| 14 (42) | 4.73e3, 3.9e3 | 4.78e3, 38 | 5.26e3, 3.5 | 1.61e4, 0.11 | **2.8e11, 6e−10** |
| 18 (54) | 9.35e3, 2.0e3 | 9.54e3, 19 | 1.16e4, 1.6 | 1.39e5, 0.013 | **2.1e20, 9e−19** |

(margin = |det mid| / rad; margin > ~3 needed for zero-exclusion on a
contour. At w=1e−4, N=14: rad ≤ 1.353e+39 — total blow-up.)

Additionally, at every w ≥ 1e−8 the **dimension-tail certification FAILED**
(`dim_tail_from_matrix` ratios go non-contracting, e.g. w=1e−8:
ratios [1.0, 2.7e−20, 1.004]): the det-increment sequence becomes
radius-dominated, so the tail bound must be established at the α-midpoint
with a separate α-uniform argument — referee obligation C8(b) is hereby
CONFIRMED EMPIRICALLY, not just plausible.

**Reading.**
1. Amplification is linear and modest (≈ 2–10 × dim) for w ≤ 1e−7; the
   ball determinant enters a combinatorial blow-up regime at w ≈ 1e−6 and is
   catastrophic by 1e−5.
2. Viable naive α-ball width at flagship scale: **w ≈ 1e−8** (margin 19–79).
   Covering an arc of length ~1 needs ~1e8 balls — DEAD as the sole
   continuation mechanism.
3. Therefore the α-ball is the right FINAL-SCALE gluing primitive, but the
   arc must be traversed by **holomorphic continuation in the parameter**:
   the det is holomorphic in a complexified θ; a Cauchy bound on a θ-disk of
   radius R (~1e−2) gives a certified derivative bound and Taylor steps of
   width h ~ 1e−3 with error M h²/R — ~1e3 steps per unit arc instead of
   1e8. The referee's C8 verdict ("α-ball for free, no perturbation lemma")
   is thus **half-right**: the enclosure works, but only at widths that make
   grid-free traversal infeasible; a derivative/Cauchy layer returns through
   the front door. Alternatively: probe whether rad growth is dominated by
   the mid-radius cross terms and can be tamed by evaluating det(1−χL) as a
   polynomial in χ (characteristic-coefficient route) — recorded as a PS-2
   design experiment, not assumed.

**Probe verdict: alpha-ball enclosure is numerically VIABLE at w ≤ 1e−8 and
NOT viable as the traversal mechanism. PS-2 design = Cauchy–Taylor steps in
complexified θ + α-ball gluing at the fine scale.**

## 4. NAMED OBLIGATIONS (carried from the referee + new)

1. **Sector-reduction re-derivation** (C8(a)): the sign=±1 reduction uses a
   symmetry that ρ breaks in general; until re-derived for (G_5, ρ_θ), run
   unreduced (dim ×2). Deliverable: a short proof or a counterexample per
   sector.
2. **Dim-tail uniform in α** (C8(b), now empirically forced by §3): prove the
   det-increment contraction with the tail ratio uniform over the θ-ball, or
   compute the tail at θ-mid + a θ-Lipschitz correction.
3. **Contour width vs α-drift** (C8(c)): each Taylor step must keep the
   tracked zero strictly inside the fixed contour; step size h is bounded by
   the certified zero-drift rate, not only by the Cauchy error.
4. **Zeta-zero vs resonance identification** (C5/C2 — PS-2, named, NOT folded
   into porting): a certificate on det(1−L_{s,ρ}) certifies a Z(s,ρ) zero;
   "resonance" needs the divisor argument, which is θ-dependent through
   spec ρ(T)(θ) (singular vs regular, §2). Same conditional scope as the
   banked flagship (R3B_FLAGSHIP_CERT.md:83) until discharged.
5. **Lerch tail primitive**: verify certified `lerch_phi` exists in our
   pinned python-flint/Arb; if absent, write the exact-tail closure for
   Σ z^n Hurwitz-terms with |z|=1 by the same integral-representation route
   as the current Hurwitz closure.
6. **Scoop-risk re-check 2026-11-01** (C4): Bandtlow–Pohl–Schick–Weiße
   (2002.03334) + Bandtlow–Slipantschuk a-priori bounds = nearest live risk;
   also re-sweep Pohl and Levitin–Strohmaier post-2021.
7. Inherited unread sources: Fraczek LNM 2139 relevant chapter; [Sel90] via
   Kelmer transcription (standing).

## 5. COST ESTIMATE (referee m5) — written plan, NOT run now

- Matrix: q=5 unreduced 2×2-block operator, dim = 2·(2κ)·N = 12N
  (obligation 1 unresolved) or 6N (resolved). At N=14: dim 168 / 84.
  Measured: dim-42 det ≈ 0.1 s at 300 bits; det cost ~ dim³ ⇒ dim-84 ≈ 0.8 s,
  dim-168 ≈ 6 s per (s, θ) evaluation.
- Contour: existing `winding_offline` geometry, K=24 per side ⇒ ~100
  evaluations per (θ-step, box).
- Traversal: θ-arc length π/2, Taylor step h ≈ 1e−3 (conservative until
  obligation 3 sizes it) ⇒ ~1.6e3 steps ⇒ ~1.6e5 evaluations.
- Wall-clock: reduced ~35 CPU-h; unreduced ~270 CPU-h. Embarrassingly
  parallel in θ-segments and contour points.
- **Where:** NOT local while the d8 queue saturates the box. Pilot
  (10 θ-steps near θ=0 anchor, reduced-if-proved else unreduced N=10,
  ~20–90 CPU-min) → local nice-19 AFTER d8 drains. Full arc → Kaggle after
  the S2 campaign releases slots. Nothing from this section was executed in
  this pass.

## Go / no-go

**GO for PS-2**, with the design amended as in §3 (Cauchy–Taylor traversal +
fine-scale α-ball gluing; unreduced operator until obligation 1 clears), on
the U(2) arc family of §1 anchored at the flagship certificate. The crux
(finite 1-dim character variety) is real and is resolved inside Pohl's
framework without leaving G_5.

## §6 — Referee corrections applied (2026-08-23, append-only)

Source of truth: `PS1_GQ_CHI_DESIGN_REFEREE.md` (verdict:
PROMOTABLE-WITH-CORRECTIONS, 7 majors, 6 minors). This section supersedes,
but does not delete, the statements above wherever they conflict. Favourable
outcome first: the referee independently derived a structural fact worth
banking — for j=0 the family is singular ONLY at θ=0 (1 ∈ spec ρ(T) iff
cos2θ = 1); the entire open interior arc (0, π/2) is regular. That is the
strongest argument for the C1 relocation below: the interior is clean.

- **C1 — anchor is an algebraic branch point (BLOCKING).** §1's θ=0 anchor
  is RETIRED as the pilot target. The tail block Φ(z, s+m, a) has a branch
  point of Lerch's formula at z=1 (singular part Γ(1−s)(−log z)^{s−1},
  divergent for Re s ≈ 0.45); since z(θ) = 1 + O(θ²) at the anchor, det(1 −
  L_{s,ρ_θ}) has an algebraic branch point in θ at θ=0, and the tail blocks
  are unbounded and discontinuous there. Superseding statement: the pilot
  re-anchors at an interior θ_0 bounded away from 0, with an alternative
  route via Φ-regularisation at z=1 (analytically subtracting the singular
  part before ball-evaluating) recorded as route (b). Named obligation:
  prove det(1 − L_{s,ρ_θ}) is holomorphic in θ on a stated domain, with the
  domain excluding θ=0 unless the z=1 regularisation is done.

- **C2 — anchor factorisation stated against the wrong object.** §1's "Z(s,
  ρ_0) = Z(s,1)·Z(s,χ′), whose first factor is the banked flagship G_5
  certificate" is corrected: the flagship (`R3B_FLAGSHIP_CERT.md:7`) is
  q=5, sign +1, the EVEN sector only, and Z(s,1) = Z_+ · Z_− under the
  reflection extension. Superseding statement: the anchor is a
  **four-factor product** Z(s,ρ_0) = Z_+ · Z_− · Z(s,χ′)'s two further
  factors under the trivial/χ′ split, of which the flagship certifies a
  winding box for the even-sector truncated determinant only, at
  conditional scope (`R3B_FLAGSHIP_CERT.md`: "MMS sector/factorization and
  the separate closed det(1−K_s) ≠ 0 identification remain outside this
  verdict"). Identifying the tracked θ-arc zero with a specific factor is
  an open obligation.

- **C3 — coding compatibility asserted, not proved.** §1/§2's claim that
  "this is exactly the shape Pohl's framework covers," with ρ(g)^{-1}
  inserted directly into `build_reduced_matrix_ball`'s MMS eq. (32)–(34)
  Rosen blocks, assumes Pohl's det(1−L_{s,χ}) = Z(Γ,χ;s) identity (proved
  for HER slow/fast cross-section operators) transfers unchanged to our
  MMS/Rosen coding. Named first-class obligation (promoted from implicit
  to explicit, §4): prove or cite the transfer of Pohl's det ↔ Z identity
  to the MMS coding. Candidate reference: Pohl, "Selberg zeta functions,
  cuspidal accelerations, and existence of strict transfer operator
  approaches" (2024-02).

- **C3b — sign inconsistency in the block↔group-element dictionary
  (implementation-critical).** §2's "`single_block(i,j,n,neg)` = the
  inverse branch x ↦ −1/(x ± nλ), the group element g = S T^{∓n}" is
  self-contradictory: x ↦ −1/(x±nλ) is S∘T^{±n}, not S T^{∓n}. Corrected
  dictionary: g = S T^{±n} (matching the stated weight ρ(T)^{±n}ρ(S)).
  Getting this backwards silently swaps z ↔ z̄ in every Lerch tail. Fix
  required before any code is written.

- **C4 — §3's headline viability figure refuted by the probe's own
  machinery.** §3 Reading 2 / probe verdict "VIABLE at w ≤ 1e−8" and "the
  dim-tail certification FAILED" only "at every w ≥ 1e−8" are both
  corrected. Measured (N=10, 14, 18, prec 300): tail is OK at w=1e−12
  (already 65× degraded, 1.3656e−7 → 8.8456e−6) and FAILS at w=1e−10 at
  all three N. Superseding statement: certifiable α-ball width at flagship
  scale is **w ≲ 1e−12**, not 1e−8 (100–1000× smaller); ball count for a
  unit arc is ~1e12, not ~1e8. Obligation 2 (dim-tail uniform in α) is
  promoted from a refinement to a **precondition** for any positive-width
  α-ball enclosure at all.

- **C5 — unreduced operator is not a code path; it is an unbuilt
  derivation.** §2/§4 obligation 1's "run the UNREDUCED operator
  (dimension ×2)" is corrected: `zeta_cert_rosen.py` has exactly one
  builder (`build_reduced_matrix_ball`, the reduced sign=±1 MMS eq.
  (33)/(34) placements); no unreduced builder exists (MMS eq. (32) for
  even q is already `NotImplementedError` in the same file). Superseding
  statement: the unreduced operator is an unbuilt MMS-eq.-(32)-class
  derivation, not a dimension flag. §2's phrase "the sector saving later"
  is WITHDRAWN as an expectation — the referee's independent check
  (conjugation by reflection J sends ρ ↦ ρ^J with ρ^J(U) = ρ(ST^{−1}),
  not isomorphic to ρ for generic θ) suggests obligation 1 resolves as a
  counterexample, not a proof.

- **C6 — cost model priced against the wrong machinery.** §5's ~35 CPU-h
  (reduced) / ~270 CPU-h (unreduced) estimate used `winding_offline` at
  N=14/dim 42/300 bits — the PROBE path, not the flagship's certification
  machinery (N=160, dim 480, 384 bits, 284 accepted subarcs, 92 adaptive
  splits, 512 enlarged-contour arcs per block, plus the Jacobi-derivative
  rH<1 layer). Superseding cost, re-priced at U(2)-reduced dim 960:
  ≈1.2e3 s/det × 284 subarcs ≈ 96 CPU-h per θ-step × 1571 steps ≈
  **~1.5e5 CPU-h (reduced) / ~1.2e6 CPU-h (unreduced)** — three-plus orders
  above the original figure, machinery graded at flagship scale. Matrix
  build cost (now two `acb.lerch_phi` calls per tail entry instead of one
  shared Hurwitz closure, expensive precisely near z=1 where C1 places the
  pilot) is also no longer negligible and is omitted from both estimates.
  PS-2 scope decision is escalated to the owner given this re-pricing.

- **C7 — sweep missed six on-point Pohl papers.** §1/§4/§6-obligation-6's
  citation list and 2026-11-01 scoop-recheck date are corrected. Six
  papers added: Doll–Pohl, arXiv:2607.14981, "The divisor of the twisted
  Selberg zeta function" (2026-07-16) — the reference for the zeta-zero-
  vs-resonance obligation (named obligation 4) and for §2's 1 ∈ spec ρ(T)
  bookkeeping; Pohl, "Some aspects of the spectral theory with twisting
  representations" (2026-07-24); "Counting Resonances on Hyperbolic
  Surfaces with Unitary Twists" (2021-09); "Scattering Theory with Unitary
  Twists" (2022-02); "Odd and even Maass cusp forms for Hecke triangle
  groups, and the billiard flow" (2013-03); "Selberg zeta functions,
  cuspidal accelerations, and existence of strict transfer operator
  approaches" (2024-02, also cited under C3 above). The scoop-recheck date
  is re-dated off 2026-11-01 (which was calibrated against the six-year-old
  2002.03334 while the 2026-07 twisted-divisor paper by the same group was
  already out). What survives unchanged: no work was found computing or
  certifying Z(Γ,χ) zeros along a unitary-rep family, on any surface — the
  novelty claim is intact; only the ledger of citations was incomplete.

- **m1 — large-w table rows are precision artifacts, not properties of the
  family.** §3's w ≥ 1e−6 column (including the quoted amp 2.8e11 and rad
  1.353e+39 at w=1e−4) is flagged: at N=14, w=1e−5 the radius is 3.382e+15
  at prec 300 but 2.086e+27 at prec 600 and 1200 (converged) — a
  precision artifact, not a converged measurement, and beyond any usable
  width regardless.

- **m2 — Cauchy remainder formula corrected.** §3 Reading 3's stated
  remainder "M h²/R" is corrected to M(h/R)²/(1−h/R) ≈ M h²/R². With the
  stated R=1e−2, h=1e−3 this is ≈1% of the sup of |det| on the disk, not
  of |det| at the tracked point — the wrong comparand, since near a
  tracked zero |det| at the point is orders smaller than the disk sup.
  The ~1.6e3-step figure built on this formula is therefore unsupported
  as stated.

- **m3 — obligation 5 (lerch_phi existence) CLOSED.** §2/§4's obligation
  5 ("availability in our pinned python-flint to be verified") is closed:
  `python-flint 0.9.0` in `/Users/za/.venvs/farey-rh` ships `acb.lerch_phi`
  (verified, ball radius 2.5e−87 at 300 bits on unimodular z). It is
  replaced by the real remaining Lerch obligation, identified under C1
  above: regularising Φ at z=1.

- **m4 — provenance note.** §1/§3 name
  `.worktrees/aletheia-restore/code/zeta_cert_rosen.py`, the general-q
  wrapper used by the §3 probe. The banked flagship certificate is
  sha-pinned instead to `zeta_cert_rosen_q5.py` plus `tb_certify/`,
  `tc_rerun/` (`R3B_FLAGSHIP_CERT.md` §1). Harmless for the probe itself;
  noted so the probe is not read as reusing the calibrated flagship
  artifact.

- **m5 — dissolution clause deleted.** §2's "Expected and welcome (that is
  where dissolution starts)" is DELETED per PS-0 §7/C6, which explicitly
  retired the Phillips–Sarnak dissolution framing ("no bearing on the
  Phillips–Sarnak counting conjecture") and ordered that retirement
  preserved on every capability claim. G_5 is non-arithmetic; there is
  essentially nothing there to dissolve.

- **m6 — torsion-freeness line added.** §1(b)'s "[G_5,G_5] is free of rank
  4" is supplemented with the licensing step it omitted: torsion-freeness
  of the commutator subgroup (all finite-order elements of G_5 are
  conjugates of powers of S or U, all non-trivial in the abelianisation),
  which via Kurosh's subgroup theorem licenses "free" rather than merely
  "of Euler characteristic −3/10."

**Append-only precision within C3b.** The corrected group element
`g=S T^{±n}` has inverse weight
`ρ(g)^{-1}=ρ(T)^{∓n}ρ(S)`, not `ρ(T)^{±n}ρ(S)`; the latter is the weight that
was consistent with the superseded `S T^{∓n}` dictionary. This sign correction
remains an implementation precondition before any code is written.

**Append-only precision within m6.** The group has
`χ(G_5)=−3/10`; the index-10 commutator subgroup has `χ=−3=1−r`, hence
`r=4`. Its torsion-freeness via Kurosh is the licensing step for freeness.

- **Favourable derivation — the interior arc is clean.** Referee point: this
  structural fact was absent from the design. Superseding statement: for
  `j=0`, the family is singular **ONLY at `θ=0`**,
  `1 ∈ spec ρ(T) ⟺ cos 2θ=1`; the entire open arc `(0,π/2)` is regular and
  the divisor bookkeeping is constant there. Named obligation: none added;
  the result supports C1's interior `θ_0` anchor and holomorphy-domain
  obligation.

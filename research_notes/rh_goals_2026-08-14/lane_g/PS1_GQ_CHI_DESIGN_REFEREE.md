# COLD ADVERSARIAL REFEREE — PS-1 `PS1_GQ_CHI_DESIGN_SOL.md`

> Installation note (orchestrator, 2026-08-23): report received verbatim from
> the read-only referee seat and installed unchanged.

**Date** 2026-08-23. **Seat**: read-only, independent (no repo files written; all scratch under the session scratchpad).
**Subject**: `/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/PS1_GQ_CHI_DESIGN_SOL.md` (221 lines, UNREFEREED).
**Evidence produced by this seat**: independent re-derivation of the `Z/2 * Z/5` character variety and of the `tr(AB)` moduli invariant; independent reproduction of the §3 α-ball probe against `/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/zeta_cert_rosen.py` at N=10/14/18 and w∈[1e−20,1e−5] with a precision sweep; direct `acb.lerch_phi` tests in `/Users/za/.venvs/farey-rh` (python-flint 0.9.0); a numerical determination of the tail-block behaviour as z→1; arXiv API sweeps of Pohl (60 entries), Bandtlow, `"Selberg zeta" AND "unitary representation"`, `"Hecke triangle" AND resonances`; reads of `PS0_DEFORMATION_SCOPING_SOL.md` (incl. §7), `PS0_DEFORMATION_SCOPING_REFEREE.md`, `R3B_FLAGSHIP_CERT.md`.

## VERDICT: PROMOTABLE-WITH-CORRECTIONS (7 majors, 6 minors)

The §1 crux — the deliverable that matters — is **correct and I re-derived it independently**. That is a real result and it does resolve the blocker PS-0/C1 left open. But the *anchor* on which the entire "calibration for free" pitch rests is mathematically the single worst point on the arc (an algebraic branch point of the tail blocks, verified numerically), the §3 headline "viable at w ≤ 1e−8" is **refuted by the doc's own machinery** (the tail certification actually fails from w ≈ 1e−11 upward, not 1e−8), the coding-compatibility premise is asserted rather than proved, the cost model is priced against machinery that has never produced a theorem-grade certificate, and the sweep misses six on-point Pohl papers — two of them from the last six weeks — repeating the exact failure mode PS-0/C1 was raised for.

---

## Criterion-by-criterion

| # | Claim under review | Evidence I produced | Grade |
|---|---|---|---|
| 1a | `G_q ≅ Z/2 * Z/q`, `G_q^ab ≅ Z/2 × Z/q`, `Hom(G_5,U(1)) = μ_2 × μ_5` = 10, finite for **every** q | Hand re-derivation: (2,q,∞) triangle group is the free product; abelianisation of a free product is the direct sum; `Z/2 × Z/5 ≅ Z/10`. Finiteness holds for all q≥3, so "no continuous 1-dim family for any Hecke group" is right, and the Γ₀(4) contrast is right | **PASS** |
| 1b | U(2) arc dim `= 2+2−3 = 1`, `θ ∈ [0,π/2]` | Re-derived two ways. (i) `V ∈ U(2)` (4) minus right torus (2) minus left torus (2) plus common centre (1) = **1**. (ii) Complete invariant computed explicitly: with `A=diag(1,−1)`, `B=V diag(ζ^j,ζ^k)V*`, `tr(AB) = cos2θ·(ζ^j − ζ^k)` — a single real modulus `cos2θ ∈ [−1,1]`. Stabiliser of an irreducible pair in PU(2) is trivial, so the count is not spoiled | **PASS** |
| 1c | Endpoints reducible, interior irreducible | `cos2θ = ±1 ⟺ V` diagonal or antidiagonal ⟺ `A,B` simultaneously diagonalisable. For `0<θ<π/2` no common eigenvector. Reps pairwise non-isomorphic since `tr ρ(T)` varies ⟹ genuine family, not a gauge orbit | **PASS** |
| 1d | `θ=0` reduces to **trivial** χ ⊕ χ′ | Achievable: `j=0` gives `χ(S)=1, χ(U)=1` = trivial; `χ′(S)=−1, χ′(U)=ζ^k`, `k≠0`. `Z(s,ρ) = ∏_γ∏_m det(1−ρ(γ)N(γ)^{−s−m})` is multiplicative on ⊕, so `Z(s,ρ_0)=Z(s,1)Z(s,χ′)` | **PASS on the algebra** |
| 1e | "…whose first factor **is** the banked flagship G_5 certificate" | `R3B_FLAGSHIP_CERT.md:1,7` — the flagship is `q=5, sign +1`, the **even sector only**, i.e. a factor `Z_+` of `Z(s,1)=Z_+Z_−`; and `R3B_FLAGSHIP_CERT.md` scope line: *"MMS sector/factorization and the separate closed det(1−K_s) ≠ 0 identification remain outside this verdict"* | **FAIL — C2** |
| 1f | Reserve family (b): `[G_5,G_5]` free of rank 4, index 10, induced dim 10 | Re-derived: `χ_orb = −3/10`; torsion-free (all finite-order elements are conjugates of powers of S or U, all non-trivial in the abelianisation) ⟹ free by Kurosh; `χ=−3=1−r ⟹ r=4`; `Hom(F_4,U(1))=U(1)^4`; `Ind` dim `= 1×10` | **PASS** (clean) |
| 2 | Pohl's framework covers Hecke triangle groups + arbitrary finite-dim unitary reps | arXiv 1503.00525 abstract verbatim: *"Hecke triangle surfaces … Selberg zeta functions with unitary finite-dimensional representations (V,χ)"*. arXiv 1606.09109: *"any Hecke triangle surface … and any finite-dimensional unitary representation χ"*, eigenvalue-1 eigenfunctions of the fast operator ↔ zeros of `Z(Γ,χ)` | **PASS on framework existence** |
| 2b | …with **the same Rosen/MMS coding our engine uses** | Nothing in either abstract, or in the design, establishes this. Pohl's identity is proved for *her* slow/fast cross-section operators; our engine implements the MMS eq. (32)–(34) Rosen-CF blocks (`build_reduced_matrix_ball`, lines 174–240). No transfer of Pohl's `det ↔ Z(Γ,χ)` identity to the MMS coding is given or cited | **FAIL — C3** |
| 3a | `ρ(T)^n` inside `inf_block` ⟹ Lerch transcendents | Algebra re-derived: `Σ_{n≥n0} z^n (nλ+a)^{−s−m} = λ^{−s−m} z^{n0} Φ(z, s+m, n0+a/λ)`. `T = SU` ⟹ `ρ(T)=AB`, infinite order, eigenvalues generically not roots of unity ⟹ Lerch genuinely needed; eigenbasis split is *how you get there*, not an alternative to it. Consistency check passes: at the anchor (`j=0,θ=0`) `ρ(T)=diag(1,−ζ^k)` so `z=1` and `Φ→ζ(s,a)`, recovering the existing Hurwitz closure | **PASS on the algebra** |
| 3b | Obligation 5 ("verify certified `lerch_phi` exists in our pinned python-flint") | Discharged in <1 min: `python-flint 0.9.0`, `acb.lerch_phi` **present**; at 300 bits, `z=e^{0.4i}`, `s=2.45+5.76i` → ball radius `2.5e−87`. Obligation 5 should not be carried as an open item | **PASS** (obligation stale) |
| 4a | Entrywise `1±w` faithfully models unimodular χ-phases | **Not a defect — tested.** In ball arithmetic a width-`w` phase arc and a radius-`w` disc are the same object to first order. Measured at N=14, w=1e−8: phase-only ball `1+i[−w,w]` → rad `4.782e−05`; full ball → `9.656e−05`. **Factor 2**, no change in any verdict. The doc's quoted `amp 4.78e3` is *exactly* my phase-only figure ⟹ the probe is reproducible and the model is the tighter of the two | **PASS** |
| 4b | "at every w ≥ 1e−8 the dim-tail certification FAILED" | **Refuted — it fails far earlier.** My run, N=14, prec 300: `w=1e−12 → tail OK (8.85e−06)`; `w=1e−10 → tail = None, FAILED`. Same at N=10 and N=18 (`w=1e−10` fails at all three). Threshold is ≈1e−11, **100–1000× smaller** than stated | **FAIL — C4** |
| 4c | "α-ball enclosure is numerically VIABLE at w ≤ 1e−8" | Follows from 4b: at `w=1e−8` there is **no certified tail at any tested N**, so no certificate exists at the doc's own "viable" width. Certifiable width (det margin **and** tail) is `w ≲ 1e−12`, and at `w=1e−12` the tail is already 65× degraded (1.37e−7 → 8.85e−6). Ball count is ~1e12, not 1e8 | **FAIL — C4** |
| 4d | Blow-up figures at `w ≥ 1e−6` | Precision-dependent, hence not properties of the family: N=14, `w=1e−5` → rad `3.382e+15` at prec 300, `2.086e+27` at prec 600 **and** prec 1200 (converged). The doc's `2.8e11`/`1.353e+39` are prec-300 truncations, understating by ~12 orders | **FAIL (minor) — m1** |
| 5a | Cost arithmetic, internal | All checks: `(84/42)³=8→0.8s`; `(168/42)³=64→6.4s≈6s`; `4×24=96≈100`; `(π/2)/1e−3=1571≈1.6e3`; `1.6e3×100=1.6e5`; `1.6e5×0.8s=35.6 CPU-h`; `1.6e5×6s=267 CPU-h`. `κ=3` for q=5 confirmed at `hecke_params` (`hq=(5−3)/2=1, κ=2hq+1=3`), so `2κN=6N`, `2(2κ)N=12N` are consistent, and dim `3×14=42` matches the measured baseline | **PASS (arithmetic)** |
| 5b | Cost is priced against the right machinery | It is not. The probe/cost use `winding_offline` + `dim_tail_from_matrix` at N=14, dim 42, 300 bits. The *theorem-grade* flagship (`R3B_FLAGSHIP_CERT.md:5,7`) required **N=160** (scalar dim 480), **384 bits**, 284 accepted subarcs, 92 adaptive splits, 512 enlarged-contour arcs per block, plus the Jacobi-derivative `rH<1` layer. Re-priced: U(2)-reduced dim 960 ⟹ `(960/42)³×0.1s ≈ 1.2e3 s`/det; ×284 subarcs = 96 CPU-h **per θ-step**; ×1571 steps ≈ **1.5e5 CPU-h** (reduced) / **1.2e6** (unreduced). ~4000× the quoted figure. Matrix *build* cost (now 2 Lerch evaluations per tail entry, not one shared Hurwitz) is also omitted entirely | **FAIL — C6** |
| 5c | Cauchy–Taylor step formula `error M h²/R` | Wrong. `M Σ_{n≥2}(h/R)^n = M(h/R)²/(1−h/R) ≈ M h²/R²`. With the stated `R=1e−2, h=1e−3` the remainder is `≈0.011·M` — 1% of the **sup on the disk**, not of `|det|` at the point, which on a zero-tracking contour is orders smaller | **FAIL (minor) — m2** |
| 6 | Scoop / prior art | No paper found computing or certifying `Z(Γ,χ)` zeros along a unitary-rep family. `all:"Selberg zeta" AND all:"unitary representation"` (40 hits), `au:Pohl_Anke` (25), `au:Bandtlow_O`, `"Hecke triangle" AND resonances` — nothing certified-along-a-family. **Gap survives.** But six directly on-point Pohl papers are uncited, two from the last six weeks | **PASS on the gap, FAIL on the sweep — C7** |

---

## MAJORS

### C1 — the anchor is an algebraic branch point of the tail blocks. The crux resolution is anchored at the worst point on the arc. (BLOCKING before any compute)

§1 makes `θ=0` the load-bearing anchor and §5 makes the pilot "10 θ-steps near θ=0". §2 notices `1 ∈ spec ρ(T)` there and calls it *"Expected and welcome"*. It is neither.

I computed the eigenvalue motion: with `j=0`, `tr(AB)=cos2θ(1−ζ^k)`, `det(AB)=−ζ^k`, so `1 ∈ spec ρ(T) ⟺ cos2θ=1 ⟺ θ=0` — the family is **singular exactly at the anchor and regular on the whole open arc**, and the eigenvalue leaves 1 **quadratically**, `z(θ)=1+O(θ²)`.

The tail block is `Φ(z, s+m, a)`. By Lerch's formula the singular part at `z→1` is `Γ(1−s)(−log z)^{s−1}`, which for `Re s ≈ 0.45` **diverges**. Measured at `s = 0.4539+5.7640i`, `a=1.3`, prec 400:

```
theta=0.5     |Phi|=4.42e+00
theta=1e-4    |Phi|=4.157e+02
theta=1e-6    |Phi|=5.138e+03
theta=1e-8    |Phi|=6.352e+04     <- growth exponent log(12.36)/log(100)=0.546 = 1-Re s
theta=0       |Phi|=5.903e-01     <- = |zeta(s,a)|, DISCONTINUOUS
```

So, at the anchor: (i) the tail blocks are **unbounded** as `θ→0⁺` (like `|z−1|^{Re s−1} ~ θ^{−1.1}` in θ), (ii) they are **discontinuous** at `θ=0`, (iii) `det(1−L_{s,ρ_θ})` has an **algebraic branch point in θ** at `θ=0` (`(z−1)^{s−1}` with `z−1 ~ θ²` gives `θ^{2s−2}`, non-integer exponent), and (iv) the divisor of `Z(s,ρ_θ)` jumps singular→regular there.

Consequences, all fatal as written:
- §3 conclusion 3 — *"the det is holomorphic in a complexified θ; a Cauchy bound on a θ-disk of radius R (~1e−2)"* — **fails at the anchor**. There is no such disk. The branch cut of `Φ(·,s,a)` on `z ∈ [1,∞)` passes through the anchor's parameter value.
- §5's pilot ("10 θ-steps near θ=0") aims the first production run directly into the singularity.
- "calibration for free" is inverted: the neighbourhood of the calibration point is where ball arithmetic degrades fastest, because the divergence is entrywise and ball arithmetic cannot recover the cancellation that keeps the Fredholm determinant finite.

**Required correction.** Either (a) anchor the traversal at `θ_0` bounded away from 0 and treat `θ=0` only as a one-sided limit with a separately proved uniform statement, or (b) re-derive the tail closure in a form regular at `z=1` (subtract the `Γ(1−s)(−log z)^{s−1}` singular part analytically before ball-evaluating). Add a named obligation: *prove `det(1−L_{s,ρ_θ})` is holomorphic in θ on a stated domain, with the domain excluding the anchor unless (b) is done.* Note (b) is required regardless for `θ` small, since the divergence is real, not numerical.

### C2 — the anchor factorisation is stated against the wrong object; the flagship is an even-sector factor, and its own verdict excludes the link

§1: *"then `Z(s, ρ_0) = Z(s, 1) · Z(s, χ′)`, whose first factor is the banked flagship G_5 certificate."*

`R3B_FLAGSHIP_CERT.md:7` — the flagship operator is `q=5, sign +1`, the even sector. `Z(s,1) = Z_+(s)·Z_−(s)` under the reflection extension `G_5 ⋊ ⟨J⟩`, so the flagship covers `Z_+`, i.e. **one of four** factors of `Z(s,ρ_0) = Z_+ · Z_− · Z(s,χ′)`. Worse, `R3B_FLAGSHIP_CERT.md` scope: *"MMS sector/factorization and the separate closed det(1−K_s) ≠ 0 identification remain outside this verdict."* So the very identification needed to call the flagship "the first factor" is explicitly outside the certified scope — this is PS-0/C2, which §7 of PS-0 ordered preserved on **every** capability claim, recurring here unmarked.

Restate as: *the anchor is a product of four factors; the flagship certifies a winding box for the even-sector truncated determinant only, at conditional scope; identifying the tracked θ-arc zero with a specific factor is an open obligation.*

### C3 — coding compatibility (Pohl's theorem ↔ our MMS/Rosen blocks) is asserted, never proved

§1: *"This is exactly the shape Pohl's framework covers"*; §2 then inserts `ρ(g)^{-1}` into `build_reduced_matrix_ball`'s blocks as if the identity transfers.

Pohl's `det(1−L_{s,χ}) = Z(Γ,χ;s)` is proved for **her** slow/fast cross-section operators (and 1606.09109's abstract is careful: it *"characterizes **some** of the zeros"*). Our engine implements the MMS eq. (32)–(34) Rosen-CF branch list. Inserting `ρ(g)^{-1}` into a *different* coding's branches yields *a* twisted operator; that its Fredholm determinant equals `Z(G_5,ρ)` needs proof or an explicit citation transferring Pohl's identity to the MMS coding. This is a first-class obligation, currently absent from §4. It compounds C2: at the trivial rep the MMS→`Z` link is *already* outside the flagship verdict.

Also flag the strongest candidate for that transfer, uncited: Pohl, *"Selberg zeta functions, cuspidal accelerations, and existence of strict transfer operator approaches"* (2024-02).

### C3b — sign inconsistency in the block↔group-element dictionary (implementation-critical)

§2, one sentence, contradicts itself: *"`single_block(i,j,n,neg)` = the inverse branch `x ↦ −1/(x ± nλ)`, the group element `g = S T^{∓n}`."* The map `x ↦ −1/(x±nλ)` is `S∘T^{±n}`, not `S T^{∓n}`. The stated weight `ρ(T)^{±n}ρ(S)` is consistent with the (wrong) second half. Getting this backwards swaps `z ↔ z̄` in every Lerch tail — silently, and with a plausible-looking answer. Fix before any code is written.

### C4 — §3's headline viability figure is refuted by the probe's own machinery

Reproduced faithfully (baselines identical: N=14 mid `−5.083206e−04+1.750962e−03j`, tail `1.3655e−7`; N=10 and N=18 also match; phase-only `amp 4.78e3` at N=14/w=1e−8 matches the doc digit-for-digit). Then extended below the doc's floor, N=14, prec 300:

```
w=1e-20  rad=9.455e-17  amp=9.46e3  tail OK  (1.3656e-07)
w=1e-16  rad=9.455e-13  amp=9.46e3  tail OK  (1.3739e-07)
w=1e-14  rad=9.455e-11  amp=9.46e3  tail OK  (2.2240e-07)
w=1e-12  rad=9.455e-09  amp=9.46e3  tail OK  (8.8456e-06)   <- already 65x degraded
w=1e-10  rad=9.457e-07  amp=9.46e3  tail FAILED
```

The doc says the tail fails "at every `w ≥ 1e−8`". It fails at `w = 1e−10` too — at N=10, N=14 **and** N=18. So the doc's §3 Reading 2, *"Viable naive α-ball width at flagship scale: w ≈ 1e−8 (margin 19–79)"*, and the probe verdict *"VIABLE at w ≤ 1e−8"*, describe a width at which **no certificate exists at any tested N**. The genuinely certifiable width is `w ≲ 1e−12`; ball count for a unit arc is ~**1e12**, not 1e8.

This does not reverse the design's direction (naive α-ball traversal is dead either way — indeed *more* dead), but it means: the §3 verdict sentence is false as written, obligation 2 is not a refinement but a **precondition for any positive-width α-ball at all**, and the "half-right" adjudication of PS-0/C8 is generous to itself — at certifiable widths the referee's α-ball-for-free is not merely infeasible as traversal, it is unavailable as an enclosure without obligation 2 first.

### C5 — "run the UNREDUCED operator (dimension ×2)" is not a code path; it is an unbuilt derivation presented as a parameter change

§2 and §4 obligation 1 treat dropping the sector reduction as a dimension bump. `zeta_cert_rosen.py` has exactly one builder, `build_reduced_matrix_ball` (line 174) — the `sign=±1` **reduced** MMS eq. (33)/(34) placements. `grep` for any unreduced builder returns nothing. The unreduced Hecke transfer operator has a different branch structure (MMS eq. (32) for even q is already flagged `NotImplementedError` in the same file), so §5's "unreduced ~270 CPU-h" prices a matrix nobody has written down.

Separately, my read is that obligation 1 will resolve as the **counterexample**, not the proof: conjugation by the reflection `J` sends `S↦S`, `T↦T^{−1}`, so it acts on the family by `ρ ↦ ρ^J` with `ρ^J(U)=ρ(ST^{−1})`, which is not isomorphic to `ρ` for generic θ. The design's *"the sector saving later"* should be withdrawn as an expectation.

### C6 — the cost model is priced against machinery that has never produced a theorem-grade certificate

See criterion 5b. `winding_offline` at N=14/dim 42/300 bits is the **probe** path. The banked flagship needed N=160, 384 bits, 284 accepted subarcs with 92 adaptive splits, 512 enlarged-contour arcs per block, and the `rH<1` Jacobi-derivative layer (`R3B_FLAGSHIP_CERT.md` §1–§2). Re-priced at U(2)-reduced dim 960: ≈1.2e3 s/det, ×284 subarcs ≈ 96 CPU-h per θ-step, ×1571 steps ≈ **1.5e5 CPU-h**; unreduced ≈1.2e6. Three-plus orders above §5's 35/270. Matrix *build* cost is also omitted, and it is no longer negligible: every tail entry now needs two `acb.lerch_phi` calls instead of one shared Hurwitz closure, and `lerch_phi` near `z=1` is expensive precisely where C1 puts the pilot. PS-0/m5 required a falsifiable cost claim; this one is falsifiable and false.

### C7 — the sweep misses six on-point Pohl papers, two from the last six weeks; PS-0/C1's failure mode recurs

`au:"Pohl Anke"` (arXiv API, 25 most recent), all uncited here, all directly on this design's obligations:

- **`arXiv:2607.14981`, Doll–Pohl, "The divisor of the twisted Selberg zeta function" (2026-07-16, 56 pp.)** — factorisation of `Z(Γ,χ)` in terms of resonances, Barnes G, and **"the singularity degrees of the representation"**. That is obligation 4 (zeta-zero vs resonance) and §2's `1 ∈ spec ρ(T)` bookkeeping, in the literature, five weeks before this design. Infinite-area, so not a scoop of the cofinite case — but it is *the* reference for obligation 4 and it shows Pohl's group is actively working this exact problem.
- **Pohl, "Some aspects of the spectral theory with twisting representations" (2026-07-24)** — four weeks before this design.
- **"Counting Resonances on Hyperbolic Surfaces with Unitary Twists" (2021-09)**
- **"Scattering Theory with Unitary Twists" (2022-02)** — the Eisenstein/singular-cusp machinery §2 needs.
- **"Odd and even Maass cusp forms for Hecke triangle groups, and the billiard flow" (2013-03)** — the sector-reduction literature for obligation 1, for our exact groups.
- **"Selberg zeta functions, cuspidal accelerations, and existence of strict transfer operator approaches" (2024-02)** — the coding-existence question of C3.

PS-0/C1 was raised because a sweep omitted the field's principal author. This design cites two Pohl papers and misses six, including her two most recent. The 2026-11-01 re-check date in obligation 6 is calibrated against a six-year-old paper (2002.03334) while a 2026-07 twisted-divisor paper by the same group was already out. **Re-date the scoop check and add all six.**

*What survives*: I found no work computing or certifying `Z(Γ,χ)` zeros along a unitary-rep family, on any surface. The §2-gap of PS-0 holds. The novelty claim is intact — the ledger is not.

---

## MINORS

- **m1** — §3's `w ≥ 1e−6` table entries and the `w=1e−4 → 1.353e+39` figure are precision artifacts, not properties of the family: N=14, `w=1e−5` gives rad `3.382e+15` at prec 300 but `2.086e+27` at prec 600 **and** 1200 (converged). Quoting `amp 2.8e11` as a measured amplification is not reproducible. Either re-run the large-`w` column at converged precision or delete it (it is beyond any usable width anyway).
- **m2** — §3 Reading 3's Cauchy remainder `M h²/R` should be `M(h/R)²/(1−h/R) ≈ M h²/R²`. With the stated `R=1e−2, h=1e−3` the remainder is ~1% of the **sup of |det| on the disk**, which is the wrong comparand: near a tracked zero `|det|` at the point is orders smaller. `h ~ 1e−3` is therefore not justified even before C1; the `~1.6e3 steps` figure is unsupported.
- **m3** — §4 obligation 5 is already dischargeable and should be closed: `python-flint 0.9.0` in `/Users/za/.venvs/farey-rh` ships `acb.lerch_phi` (verified, ball radius `2.5e−87` at 300 bits on unimodular `z`). Carrying it as open work overstates remaining risk. The *real* remaining Lerch obligation is the one C1 identifies: regularising `Φ` at `z=1`.
- **m4** — provenance mismatch: §1/§3 name `.worktrees/aletheia-restore/code/zeta_cert_rosen.py`, but the flagship certificate is sha-pinned to `zeta_cert_rosen_q5.py` plus `tb_certify/`, `tc_rerun/` (`R3B_FLAGSHIP_CERT.md` §1). The probe used the general-q wrapper. Harmless for the probe, misleading as a claim of reusing "the calibrated Rosen blocks" of the banked result.
- **m5** — §2's *"At the anchor … the anchor is a SINGULAR point of the family … Expected and welcome (that is where dissolution starts)"* reintroduces the dissolution framing that PS-0 §7/C6 explicitly retired (*"no bearing on the Phillips–Sarnak counting conjecture"*). `G_5` is non-arithmetic; if PS is right there is essentially nothing there to dissolve. Delete the clause — this is a correction regression, and PS-0 §7 said §7 supersedes.
- **m6** — §1(b): the reserve-family arithmetic is clean (I checked `χ_orb=−3/10`, torsion-freeness via Kurosh, rank 4, induced dim 10) but the doc omits the torsion-freeness step that licenses "free of rank 4". One line.

---

## What passed cleanly (and is worth banking)

- **The §1 crux is right and is the doc's real contribution.** `Hom(G_q,U(1))` finite for all q; `dim = 2+2−3 = 1` confirmed by two independent routes; the complete invariant is `tr(AB)=cos2θ(ζ^j−ζ^k)`, a single real modulus, with `θ∈[0,π/2]` a genuine fundamental interval and reducible endpoints; interior points irreducible and pairwise non-isomorphic. This resolves PS-0/C1's open family question without leaving `G_5`.
- **A structural fact the doc should add** (I derived it; it is favourable and non-obvious): for `j=0` the family is **singular only at `θ=0`** and regular on the entire open arc — `1 ∈ spec ρ(T) ⟺ cos2θ=1`. The divisor bookkeeping §2 worries about is therefore constant on `(0,π/2)`. This is the strongest available argument for the C1 fix (anchor away from 0): the *interior* is clean.
- **§3 is honestly reported and reproducible in the linear regime.** Baselines and amplifications match my independent run digit-for-digit at `w ≤ 1e−7`. Confirming C8(b) empirically rather than assuming it is good practice; the fault is that the confirmation is stronger than the doc realised.
- **The phase-vs-magnitude concern is not a defect** — measured factor 2, verdict unchanged.
- **The Lerch algebra is correct**, including the self-consistency check that the anchor degenerates to the existing Hurwitz closure.
- **Internal cost arithmetic is exact** (every one of the seven figures re-derived) — the error is in the choice of comparand, not the sums.
- **The scoop gate holds** on four independent arXiv queries.

---

## Required before PS-2 compute

1. **C1** — relocate the anchor off `θ=0`, or regularise `Φ` at `z=1`; add an explicit holomorphy-domain-in-θ obligation. Redesign the §5 pilot, which currently targets the singularity.
2. **C2** — restate the anchor as a four-factor product; preserve the flagship's even-sector + conditional-scope caveat verbatim.
3. **C3 / C3b** — add a named obligation to transfer Pohl's `det ↔ Z(Γ,χ)` identity to the MMS/Rosen coding; fix the `S T^{±n}` sign before implementation.
4. **C4** — correct the §3 verdict sentence to the measured `w ≲ 1e−12` threshold; promote obligation 2 to a precondition.
5. **C5** — state that the unreduced operator must be derived and implemented (MMS eq. (32)-class work), not obtained by a dimension flag; withdraw "sector saving later".
6. **C6** — re-price against the flagship's actual certification machinery, including build cost and Lerch evaluation.
7. **C7** — add the six Pohl papers; re-date the scoop check off 2026-11-01.

*Scratch artifacts (not repo files): `/private/tmp/claude-501/-Users-za-Documents-farey-hecke/d132431f-d2c6-4401-96d1-90f58d3026fb/scratchpad/rep.py`, `rep2.py`.*

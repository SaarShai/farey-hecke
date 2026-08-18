# (RATE) note-graph referee audit (sol xhigh, read-only, 2026-08-18)

17 findings: 4 CRITICAL, 12 MAJOR, 1 MINOR-cluster. Persisted verbatim from
the auditor session log. Repair wave tracked in MAP; corrections land as
dated [CORRECTION 2026-08-18 audit] blocks, never silent rewrites.

1. **CRITICAL — v27 is not machine-certified.**

   - `projects/aristotle_dispatch_v27/DISPATCH.md:5-7`: “6 sorry'd theorems… 6 declaration-uses-sorry warnings”.
   - Contradiction: `DISPATCH.md:13-17`: “machine-certified REFUTATION”.
   - `projects/aristotle_dispatch_v27/RateCoreII.lean:69-71,84-87,91-93,98-105,114-118`: every one of the six theorem bodies is still `sorry`.
   - `plans/wayfinder/rh-goals/MAP.md:155` repeats “machine-certified REFUTATION” while simultaneously saying “pending Aristotle confirmation”.

   **Demanded correction:** Replace every current “machine-certified” claim with: “hand-derived and numerically checked; syntax-checked dispatch with six live `sorry`s; harvest and independent sorry-free build pending.” Do not promote the product invariant, evenness, or N4 count either.

2. **CRITICAL — the v26 general M1 axiom is false, and R2 still leans on it.**

   - `projects/aristotle_dispatch_v26/result/.../RateCore.lean:364-373` assumes injectivity of `w ↦ c 2 w`.
   - `projects/aristotle_dispatch_v27/RateCoreII.lean:67-87` gives
     `c_λ([n,m]) = λ(nmλ²−1)` and the `[1,2]`/`[2,1]` collision. At `λ=2`, both have `c=14`.
   - `LAW_R2_RATE_LEMMA_DRAFT.md:242-250`: the proof skeleton splits the series using that word-level map.
   - `LAW_R2_RATE_LEMMA_DRAFT.md:317-320`: “This is THE structural lemma; without it the split … is data, not proof.”
   - Its existing correction at `:324-341` covers only depths 1 and 2, not the depth-3 refutation.

   The collision is only for the **c-only word proxy**: R1 correctly says the coset invariant is `(c,d mod c)` at `LAW_R1_COSET_STRUCTURE.md:66-83`; `[1,2]` and `[2,1]` can still have different `d`.

   **Demanded correction:** Add a prominent `[CORRECTION v27]` block to R2. Delete/quarantine the false c-only general axiom and restate M1 as a canonical-coset normal-form theorem using `(c,d mod c)`, including well-definedness, injectivity, surjectivity, and localization of the complement. The numerics need not be discarded solely because of this collision, but the theorem assembly remains data.

3. **CRITICAL — M2 uses the wrong cusp-width normalization.**

   - `LAW_R1_COSET_STRUCTURE.md:59-71`: in the conjugated model, `S:z↦z+1`; right multiplication gives `d↦d+bC`, so the invariant is `d mod c`.
   - `projects/aristotle_dispatch_v27/RateCoreII.lean:49-51`: `Spow n = [[1,n],[0,1]]`.
   - Contradiction: `LAW_M2_TAIL_MAJORANT_DRAFT.md:22-34` calls the conjugated cusp width `λ`, uses `d mod λc`, and asserts `d↦d+kλc`.

   **Demanded correction:** Choose one normalization. Either remain in the conjugated width-one model and rederive M2.L using `d mod c`, or transform every group, matrix, invariant, and counting formula consistently to a width-`λ` model. Until then, `m_N(c)≤λc≤2c` and M2.T are unproved.

4. **MAJOR — R2 upgrades R1’s proxy into an “exact” resolution.**

   - `LAW_R1_COSET_STRUCTURE.md:230-243`: the two slope measurements “are not directly comparable” and R1 “does NOT claim to have resolved or reconciled” them.
   - `LAW_R1_COSET_STRUCTURE.md:294-303`: matching is a “RANK-MATCHING proxy,” not an exact word/coset correspondence.
   - Contradiction: `LAW_R2_RATE_LEMMA_DRAFT.md:58-64`: reconciliation “CHECKS OUT quantitatively”.
   - `LAW_R2_RATE_LEMMA_DRAFT.md:69-72`: “EXACT word-level λ→2 limit… closing R1’s §5 proxy caveat”.
   - `MAP.md:150`: “THE POWER MYSTERY RESOLVED”.

   **Demanded correction:** Describe this as finite-window, depth-≤12, Chebyshev-family evidence with greedy canonicalized matching. “Resolved” and “exact” must wait for the corrected coset-level M1.

5. **MAJOR — M2’s explicit formula is promoted beyond its open hypotheses.**

   - `LAW_M2_TAIL_MAJORANT_DRAFT.md:3-8`: “DRAFT… one structural lemma at proof-sketch level”.
   - `:35-39`: G1 discreteness is open.
   - `:53-57`: G2 integer-grid domination is open.
   - `:75-81`: promotion to proved “awaits G1+G2”.
   - Contradiction: `:82-86`: Hejhal’s constant is “fully replaceable”.
   - `MAP.md:156`: calls it a “closed-form N-uniform majorant” and says “N3 numeric instances replaced by formula”.

   **Demanded correction:** Call M2.T a candidate formula conditional on corrected M2.L, G1, and G2. Retain M2 and N3 as open. Separately cover the `N=∞` theta side, because the stated target at `M2:12-18` only says finite `N≥3`.

6. **MAJOR — the advertised full-series bound at `X=1` omits the boundary.**

   - `LAW_M2_TAIL_MAJORANT_DRAFT.md:14,46-51`: M2.T bounds the strict tail `|c|>X`.
   - Contradiction: `:82-85`: setting `X=1` is called a “full-series bound” of `12`.
   - For `q=3`, the shortest `c` can equal `λ_3=1`; strict `|c|>1` does not include it.

   **Demanded correction:** Either call `12` only the `|c|>1` tail, or add the `|c|=1` mass. Under the note’s own `m(1)≤2` ceiling, the corresponding full-series bound is at most `14`, not `12`.

7. **CRITICAL — the pre-registered numerical gate failed but the note calls it passed.**

   - `LAW_RATE_MEASURE.md:146-147`: required agreement is `≤1e-6`.
   - Contradiction: `LAW_RATE_MEASURE.md:152,164-165`: q=4 errors through `2.4e-6` are labelled “PASS”; “GATE 1 PASSED”.
   - `law_probes/rate_measure_validate.log:17,22`: actual errors are `2.082e-06` and `2.373e-06`.
   - `rate_measure_validate.log:34,50`: “GATE1 … FAIL” and “do not trust q>6 measurements without further repair.”
   - The claimed N=40 recovery at `LAW_RATE_MEASURE.md:157-162` has no committed N=40 row in that validation log.

   **Demanded correction:** Record the literal gate result as FAIL. Commit a reproducible post-repair/N=40 validation artifact and rerun the original threshold before calling q>6 RATE measurements validated. A retroactive `2.4e-6` tolerance is not the pre-registered gate.

8. **MAJOR — q=64 convergence count and asymptotic inference are wrong.**

   - `LAW_HEJHAL_CH6S12_CH11S3_EXTRACT.md:63-70` and `MAP.md:157`: “6/8” rows are `≤1e-5`, `t≤3.5 fully trusted`, and all slopes are “comparable or FASTER” than `−1.2/−1.5`.
   - Contradiction: `law_probes/rate_measure_data.json:2` has the q=64, `σ=1.1,t=3.5` receipt `0.000010225275625778768`, which is greater than `1e-5`. The strict count is **5/8**.
   - The reported `−1.11` is slower than `−1.2`, and `−1.29` is slower than `−1.5`.
   - `LAW_RATE_MEASURE.md:273-279` explicitly treats `t=3.5` as borderline and excludes it from the original slope claim.
   - `LAW_R2_RATE_LEMMA_DRAFT.md:254-278` validates only `s=1.1+1.5i`, q=12–48, and warns not to quote fixed-X results past q=48.

   **Demanded correction:** State 5/8 at the declared threshold; classify `t=3.5` as borderline; remove “all comparable-or-faster” and “still majorizes” as q64 conclusions. q64 supplies exploratory slope consistency, not validation of the R2 bound.

9. **MAJOR — the `0.26` partial-window mass is repeatedly called a tail majorant.**

   - `LAW_R1_COSET_STRUCTURE.md:249-251`: the sum is only `X'≤|c|≤50`.
   - `:304-310`: `0.26` is an “UNDER-estimate” and “should not be read as a bound” on the full spectrum.
   - Contradiction: `LAW_R2_RATE_LEMMA_DRAFT.md:3-7` imports “tail majorant ≤0.26”.
   - `LAW_M2_TAIL_MAJORANT_DRAFT.md:66-70` calls it a “measured tail”.
   - `MAP.md:149` calls it a “Tail majorant,” although it retains the `X≤50` caveat.

   **Demanded correction:** Everywhere write
   `Σ_{10≤|c|≤50}|c|^{-2.2}≤0.26`, described as empirical partial-window mass. Never use it as a full-tail bound or majorant.

10. **MAJOR — the `A≤0.518` population is misstated.**

   - `LAW_R2_RATE_LEMMA_DRAFT.md:51-54`: “over ALL enumerated cosets”.
   - Its table at `:139-145` contains 1,384 total q-cosets but only 1,138 matched cosets.
   - `law_probes/r2_drift.py:173-196` places matched cosets in `rows`, escaping cosets in `esc_q`, and computes `Amax` from `rows` only.

   **Demanded correction:** Say “maximum over all 1,138 matched cosets tested; 246 escaping cosets were not tested.” Retain universal C1 as open and add `X=50`, depth `≤12`, and matched-only to MAP’s summary.

11. **MAJOR — sampled grid minima are stated as interval lower bounds.**

   - `LAW_R4_THETA_DEFECT.md:146-159`: 41-point grids are followed by `d(t)≥0.6612/0.6604` over the whole windows.
   - Contradiction/caveat: `:280-286`: `0.6604` is only “a safe, rounded-down witness at the sampled grid points, not a proven global minimum”; a finer grid could be smaller.
   - `MAP.md:145` still headlines “Anchor lower bound… d(t)≥0.6604”.

   **Demanded correction:** Use “sampled-grid minimum/witness” throughout. A continuous interval lower bound requires interval arithmetic or a derivative/Lipschitz enclosure between grid points.

12. **MAJOR — the Ch.6 extraction upgrades big-O statements into explicit, N-uniform constants without doing the bookkeeping.**

   - `LAW_HEJHAL_CH6S12_CH11S3_EXTRACT.md:13`: “Every constant in the chain is EXPLICIT”.
   - Yet `:26-31` quotes several `O(...)` bounds, excludes `|s-s_k|<δ`, and says constants depend on `Γ,χ,𝓕,δ`.
   - `:34-40` then says only `η` and the zero count matter, are N-uniform, and M2 is promotable with “no new analytic idea”.
   - `MAP.md:153` upgrades this to “ENTIRELY EXPLICIT-CONSTANT” and N-uniform.

   **Demanded correction:** Downgrade to “potentially effective source route”. Instantiate every hidden big-O constant and prove uniform bounds for `Γ,χ,𝓕,δ,η`, and `ω(t)` across the Hecke family before claiming explicit N-uniformity.

13. **MAJOR — R2 overstates what v26 machine-verified in P6.**

   - `LAW_R2_RATE_LEMMA_DRAFT.md:20`: “P6 … PROVED as stated.”
   - P6 at `:120-125` includes the derivative formula
     `c'_w(2)=m+(m³−m)/3` and the sharp `k²` conclusion.
   - The harvested Lean result at `projects/aristotle_dispatch_v26/result/.../RateCore.lean:332-351` proves only the Chebyshev `c` identity and `c(2)=2m`; it contains no derivative theorem.

   **Demanded correction:** Scope machine verification to the `c` identity and λ=2 value. Formalize the derivative/sharpness step separately or label it paper algebra, not machine-verified P6.

14. **MAJOR — several numerical claims lack committed receipts.**

   - `LAW_RATE_MEASURE.md:157-162`: N=40 gives `≤1.2e-7`; no N=40 output appears in the committed validation log.
   - `LAW_R1_COSET_STRUCTURE.md:217-228`: fit slopes `−1.72/−1.85`; the committed script does not emit those fits.
   - `LAW_HEJHAL_CH6S12_CH11S3_EXTRACT.md:47-49`: `≤2.5e-32` and `≤5e-32`; no named script/log records the computation.
   - `BRANCH_DEFECT_BLAST_AUDIT.md:3-7`: explicitly says independent spot-verification was “none beyond reading”, while `:72-79` reports an 850-file scan and a fresh `3.91e-10` comparison.

   **Demanded correction:** Commit the exact executable command, inputs, precision, outputs, and hashes for each claim, or relabel them “author/auditor-reported, not independently receipted.” The branch audit’s scoped conclusion may stand, but its numerical census is not presently reproducible from the report alone.

15. **MAJOR — R1’s own quantitative prose contradicts its table and arithmetic.**

   - `LAW_R1_COSET_STRUCTURE.md:43-46`: X′=40 range is `0.019–0.027`.
   - Table `:255-261`: q=12 gives `0.02951`.
   - `:263-266`: q=8 is allegedly largest at every X′; q=12 is larger at X′=30 and 40.
   - `:222-225`: `n_q` falling `330→237` allegedly means “MORE matched terms”, and slopes `−1.72/−1.85` are “slightly steeper than q^-2”.
   - Falling counts mean fewer total q-cosets, while `−1.72` and `−1.85` are shallower than `−2`.
   - Least squares directly on the displayed totals gives approximately `−1.759` and `−1.969`, not `−1.72` and `−1.85`.

   **Demanded correction:** Regenerate all prose and fits from the committed table, state the precise fit convention, change the X′=40 range to approximately `0.019–0.030`, and remove the erroneous “more/steeper” explanation.

16. **MAJOR — the scalar pole order contradicts itself.**

   - `LAW_RATE_MEASURE.md:24-30`: `|φ_∞|` grows like `r^-2`.
   - Contradiction: `:134-139`: the scalar entry has clean `r^-1` simple-pole growth; only the 2×2 determinant has order two.
   - `LAW_R4_THETA_DEFECT.md:97-108` agrees with the simple scalar pole.

   **Demanded correction:** Change the headline to `r^-1`; reserve `r^-2` for `det Φ`.

17. **MINOR — stale and small consistency errors remain unmarked.**

   - `LAW_RATE_MEASURE.md:6-13,232-233,286-301`: q64 unfinished and JSON still appending; contradicted by `LAW_HEJHAL_CH6S12_CH11S3_EXTRACT.md:61-71` and `MAP.md:157`, where 48/48 is complete.
   - `LAW_HEJHAL_S7_EXTRACT.md:141-142`: R1–R5 “not started”; current `MAP.md:149-156` records R1/R2/R4/M2 work.
   - `MAP.md:144`: branch audit “queued”; `MAP.md:155` says it is discharged.
   - `LAW_RATE_MEASURE.md:293-295`: `216.7/21.3` is `10.17×`, not `~8×`.
   - `projects/aristotle_dispatch_v27/RateCoreII.lean:78` says the collision words are nonzero for every `λ>0`; the formula vanishes at `λ=1/√2`. The intended Hecke range is safe, but the comment is false as written.
   - `projects/aristotle_dispatch_v26/DISPATCH.md:75-86` says “8 statements”; the eight obligation rows contain nine named theorem declarations.

   **Demanded correction:** Add dated supersession blocks rather than silently rewriting historical notes; fix the arithmetic/comment/counting statements. Label the v26 root Lean file as superseded dispatch input, distinct from the corrected harvested result.

**Weakest link:** the corrected **coset-level M1**. R2 itself concedes at `LAW_R2_RATE_LEMMA_DRAFT.md:317-320` that without M1 the matched/escaping split is data, not proof. The only formal general proxy is c-only and false at depth three. Until a normal-form theorem controls full coset invariants and localizes the complement, neither the `q^{3-2σ}` summation nor the RATE exponent follows. M2 normalization/G1/G2 and the nonconverged target height `t≈7.0665` are the next blockers; R3 transport and M3 uniformity remain open afterward.

**Explicitly clean categories:**

- No numeric contradiction was found in the R4 residue, `γ₁/2` location, or the distinction between the `0.6604` sampled anchor and `0.2167845…` residue magnitude.
- M2’s displayed arithmetic `4.5913, 3.4692, 0.5713, 0.2835`, and `T(10)=6.4358` is correct conditional on M2.L/G1/G2.
- The q64 slope calculations themselves match the committed JSON; the defect is the convergence count and inference.
- The exponent formula `q^{1-2σ}` correctly gives `−1.2` and `−1.5`; the claim that every measured slope is at least that fast is false.
- The Hejhal scan hashes and printed theta-entry normalization are consistent.
- The v26 harvested result contains no live `sorry` and genuinely proves corrected P4, the Chebyshev c-identities, and depth-1/depth-2 statements. It does not prove general M1 or the P6 derivative.
- The branch-defect audit preserves its branch-specific scope and keeps t=7/t=14 truncation separate; its future-use warning about raw `K_q_corrected` is appropriate.
- `MAP.md:154` is ledger-clean in scope: it explicitly labels pins self-generated, pin rigor `NONE`, makes no `ρ*` claim, and calls the results box certificates rather than assembled theorems.
- No hunt category is globally clean: numeric consistency, ledger-rule propagation, receipts, and stale-status handling all have defects above.


tokens used
290,581
Verdict: **FAIL**. At current HEAD `bc75458`, the RATE graph is not internally consistent or ready for theorem-level reliance. I found 4 critical, 12 major, and 1 minor defect. No files were written.

All unqualified note paths below are under `research_notes/rh_goals_2026-08-14/lane_g/`.

1. **CRITICAL — v27 is not machine-certified.**

   - `projects/aristotle_dispatch_v27/DISPATCH.md:5-7`: “6 sorry'd theorems… 6 declaration-uses-sorry warnings”.
   - Contradiction: `DISPATCH.md:13-17`: “machine-certified REFUTATION”.
   - `projects/aristotle_dispatch_v27/RateCoreII.lean:69-71,84-87,91-93,98-105,114-118`: every one of the six theorem bodies is still `sorry`.
   - `plans/wayfinder/rh-goals/MAP.md:155` repeats “machine-certified REFUTATION” while simultaneously saying “pending Aristotle confirmation”.

   **Demanded correction:** Replace every current “machine-certified” claim with: “hand-derived and numerically checked; syntax-checked dispatch with six live `sorry`s; harvest and independent sorry-free build pending.” Do not promote the product invariant, evenness, or N4 count either.

2. **CRITICAL — the v26 general M1 axiom is false, and R2 still leans on it.**

   - `projects/aristotle_dispatch_v26/result/.../RateCore.lean:364-373` assumes injectivity of `w ↦ c 2 w`.
   - `projects/aristotle_dispatch_v27/RateCoreII.lean:67-87` gives
     `c_λ([n,m]) = λ(nmλ²−1)` and the `[1,2]`/`[2,1]` collision. At `λ=2`, both have `c=14`.
   - `LAW_R2_RATE_LEMMA_DRAFT.md:242-250`: the proof skeleton splits the series using that word-level map.
   - `LAW_R2_RATE_LEMMA_DRAFT.md:317-320`: “This is THE structural lemma; without it the split … is data, not proof.”
   - Its existing correction at `:324-341` covers only depths 1 and 2, not the depth-3 refutation.

   The collision is only for the **c-only word proxy**: R1 correctly says the coset invariant is `(c,d mod c)` at `LAW_R1_COSET_STRUCTURE.md:66-83`; `[1,2]` and `[2,1]` can still have different `d`.

   **Demanded correction:** Add a prominent `[CORRECTION v27]` block to R2. Delete/quarantine the false c-only general axiom and restate M1 as a canonical-coset normal-form theorem using `(c,d mod c)`, including well-definedness, injectivity, surjectivity, and localization of the complement. The numerics need not be discarded solely because of this collision, but the theorem assembly remains data.

3. **CRITICAL — M2 uses the wrong cusp-width normalization.**

   - `LAW_R1_COSET_STRUCTURE.md:59-71`: in the conjugated model, `S:z↦z+1`; right multiplication gives `d↦d+bC`, so the invariant is `d mod c`.
   - `projects/aristotle_dispatch_v27/RateCoreII.lean:49-51`: `Spow n = [[1,n],[0,1]]`.
   - Contradiction: `LAW_M2_TAIL_MAJORANT_DRAFT.md:22-34` calls the conjugated cusp width `λ`, uses `d mod λc`, and asserts `d↦d+kλc`.

   **Demanded correction:** Choose one normalization. Either remain in the conjugated width-one model and rederive M2.L using `d mod c`, or transform every group, matrix, invariant, and counting formula consistently to a width-`λ` model. Until then, `m_N(c)≤λc≤2c` and M2.T are unproved.

4. **MAJOR — R2 upgrades R1’s proxy into an “exact” resolution.**

   - `LAW_R1_COSET_STRUCTURE.md:230-243`: the two slope measurements “are not directly comparable” and R1 “does NOT claim to have resolved or reconciled” them.
   - `LAW_R1_COSET_STRUCTURE.md:294-303`: matching is a “RANK-MATCHING proxy,” not an exact word/coset correspondence.
   - Contradiction: `LAW_R2_RATE_LEMMA_DRAFT.md:58-64`: reconciliation “CHECKS OUT quantitatively”.
   - `LAW_R2_RATE_LEMMA_DRAFT.md:69-72`: “EXACT word-level λ→2 limit… closing R1’s §5 proxy caveat”.
   - `MAP.md:150`: “THE POWER MYSTERY RESOLVED”.

   **Demanded correction:** Describe this as finite-window, depth-≤12, Chebyshev-family evidence with greedy canonicalized matching. “Resolved” and “exact” must wait for the corrected coset-level M1.

5. **MAJOR — M2’s explicit formula is promoted beyond its open hypotheses.**

   - `LAW_M2_TAIL_MAJORANT_DRAFT.md:3-8`: “DRAFT… one structural lemma at proof-sketch level”.
   - `:35-39`: G1 discreteness is open.
   - `:53-57`: G2 integer-grid domination is open.
   - `:75-81`: promotion to proved “awaits G1+G2”.
   - Contradiction: `:82-86`: Hejhal’s constant is “fully replaceable”.
   - `MAP.md:156`: calls it a “closed-form N-uniform majorant” and says “N3 numeric instances replaced by formula”.

   **Demanded correction:** Call M2.T a candidate formula conditional on corrected M2.L, G1, and G2. Retain M2 and N3 as open. Separately cover the `N=∞` theta side, because the stated target at `M2:12-18` only says finite `N≥3`.

6. **MAJOR — the advertised full-series bound at `X=1` omits the boundary.**

   - `LAW_M2_TAIL_MAJORANT_DRAFT.md:14,46-51`: M2.T bounds the strict tail `|c|>X`.
   - Contradiction: `:82-85`: setting `X=1` is called a “full-series bound” of `12`.
   - For `q=3`, the shortest `c` can equal `λ_3=1`; strict `|c|>1` does not include it.

   **Demanded correction:** Either call `12` only the `|c|>1` tail, or add the `|c|=1` mass. Under the note’s own `m(1)≤2` ceiling, the corresponding full-series bound is at most `14`, not `12`.

7. **CRITICAL — the pre-registered numerical gate failed but the note calls it passed.**

   - `LAW_RATE_MEASURE.md:146-147`: required agreement is `≤1e-6`.
   - Contradiction: `LAW_RATE_MEASURE.md:152,164-165`: q=4 errors through `2.4e-6` are labelled “PASS”; “GATE 1 PASSED”.
   - `law_probes/rate_measure_validate.log:17,22`: actual errors are `2.082e-06` and `2.373e-06`.
   - `rate_measure_validate.log:34,50`: “GATE1 … FAIL” and “do not trust q>6 measurements without further repair.”
   - The claimed N=40 recovery at `LAW_RATE_MEASURE.md:157-162` has no committed N=40 row in that validation log.

   **Demanded correction:** Record the literal gate result as FAIL. Commit a reproducible post-repair/N=40 validation artifact and rerun the original threshold before calling q>6 RATE measurements validated. A retroactive `2.4e-6` tolerance is not the pre-registered gate.

8. **MAJOR — q=64 convergence count and asymptotic inference are wrong.**

   - `LAW_HEJHAL_CH6S12_CH11S3_EXTRACT.md:63-70` and `MAP.md:157`: “6/8” rows are `≤1e-5`, `t≤3.5 fully trusted`, and all slopes are “comparable or FASTER” than `−1.2/−1.5`.
   - Contradiction: `law_probes/rate_measure_data.json:2` has the q=64, `σ=1.1,t=3.5` receipt `0.000010225275625778768`, which is greater than `1e-5`. The strict count is **5/8**.
   - The reported `−1.11` is slower than `−1.2`, and `−1.29` is slower than `−1.5`.
   - `LAW_RATE_MEASURE.md:273-279` explicitly treats `t=3.5` as borderline and excludes it from the original slope claim.
   - `LAW_R2_RATE_LEMMA_DRAFT.md:254-278` validates only `s=1.1+1.5i`, q=12–48, and warns not to quote fixed-X results past q=48.

   **Demanded correction:** State 5/8 at the declared threshold; classify `t=3.5` as borderline; remove “all comparable-or-faster” and “still majorizes” as q64 conclusions. q64 supplies exploratory slope consistency, not validation of the R2 bound.

9. **MAJOR — the `0.26` partial-window mass is repeatedly called a tail majorant.**

   - `LAW_R1_COSET_STRUCTURE.md:249-251`: the sum is only `X'≤|c|≤50`.
   - `:304-310`: `0.26` is an “UNDER-estimate” and “should not be read as a bound” on the full spectrum.
   - Contradiction: `LAW_R2_RATE_LEMMA_DRAFT.md:3-7` imports “tail majorant ≤0.26”.
   - `LAW_M2_TAIL_MAJORANT_DRAFT.md:66-70` calls it a “measured tail”.
   - `MAP.md:149` calls it a “Tail majorant,” although it retains the `X≤50` caveat.

   **Demanded correction:** Everywhere write
   `Σ_{10≤|c|≤50}|c|^{-2.2}≤0.26`, described as empirical partial-window mass. Never use it as a full-tail bound or majorant.

10. **MAJOR — the `A≤0.518` population is misstated.**

   - `LAW_R2_RATE_LEMMA_DRAFT.md:51-54`: “over ALL enumerated cosets”.
   - Its table at `:139-145` contains 1,384 total q-cosets but only 1,138 matched cosets.
   - `law_probes/r2_drift.py:173-196` places matched cosets in `rows`, escaping cosets in `esc_q`, and computes `Amax` from `rows` only.

   **Demanded correction:** Say “maximum over all 1,138 matched cosets tested; 246 escaping cosets were not tested.” Retain universal C1 as open and add `X=50`, depth `≤12`, and matched-only to MAP’s summary.

11. **MAJOR — sampled grid minima are stated as interval lower bounds.**

   - `LAW_R4_THETA_DEFECT.md:146-159`: 41-point grids are followed by `d(t)≥0.6612/0.6604` over the whole windows.
   - Contradiction/caveat: `:280-286`: `0.6604` is only “a safe, rounded-down witness at the sampled grid points, not a proven global minimum”; a finer grid could be smaller.
   - `MAP.md:145` still headlines “Anchor lower bound… d(t)≥0.6604”.

   **Demanded correction:** Use “sampled-grid minimum/witness” throughout. A continuous interval lower bound requires interval arithmetic or a derivative/Lipschitz enclosure between grid points.

12. **MAJOR — the Ch.6 extraction upgrades big-O statements into explicit, N-uniform constants without doing the bookkeeping.**

   - `LAW_HEJHAL_CH6S12_CH11S3_EXTRACT.md:13`: “Every constant in the chain is EXPLICIT”.
   - Yet `:26-31` quotes several `O(...)` bounds, excludes `|s-s_k|<δ`, and says constants depend on `Γ,χ,𝓕,δ`.
   - `:34-40` then says only `η` and the zero count matter, are N-uniform, and M2 is promotable with “no new analytic idea”.
   - `MAP.md:153` upgrades this to “ENTIRELY EXPLICIT-CONSTANT” and N-uniform.

   **Demanded correction:** Downgrade to “potentially effective source route”. Instantiate every hidden big-O constant and prove uniform bounds for `Γ,χ,𝓕,δ,η`, and `ω(t)` across the Hecke family before claiming explicit N-uniformity.

13. **MAJOR — R2 overstates what v26 machine-verified in P6.**

   - `LAW_R2_RATE_LEMMA_DRAFT.md:20`: “P6 … PROVED as stated.”
   - P6 at `:120-125` includes the derivative formula
     `c'_w(2)=m+(m³−m)/3` and the sharp `k²` conclusion.
   - The harvested Lean result at `projects/aristotle_dispatch_v26/result/.../RateCore.lean:332-351` proves only the Chebyshev `c` identity and `c(2)=2m`; it contains no derivative theorem.

   **Demanded correction:** Scope machine verification to the `c` identity and λ=2 value. Formalize the derivative/sharpness step separately or label it paper algebra, not machine-verified P6.

14. **MAJOR — several numerical claims lack committed receipts.**

   - `LAW_RATE_MEASURE.md:157-162`: N=40 gives `≤1.2e-7`; no N=40 output appears in the committed validation log.
   - `LAW_R1_COSET_STRUCTURE.md:217-228`: fit slopes `−1.72/−1.85`; the committed script does not emit those fits.
   - `LAW_HEJHAL_CH6S12_CH11S3_EXTRACT.md:47-49`: `≤2.5e-32` and `≤5e-32`; no named script/log records the computation.
   - `BRANCH_DEFECT_BLAST_AUDIT.md:3-7`: explicitly says independent spot-verification was “none beyond reading”, while `:72-79` reports an 850-file scan and a fresh `3.91e-10` comparison.

   **Demanded correction:** Commit the exact executable command, inputs, precision, outputs, and hashes for each claim, or relabel them “author/auditor-reported, not independently receipted.” The branch audit’s scoped conclusion may stand, but its numerical census is not presently reproducible from the report alone.

15. **MAJOR — R1’s own quantitative prose contradicts its table and arithmetic.**

   - `LAW_R1_COSET_STRUCTURE.md:43-46`: X′=40 range is `0.019–0.027`.
   - Table `:255-261`: q=12 gives `0.02951`.
   - `:263-266`: q=8 is allegedly largest at every X′; q=12 is larger at X′=30 and 40.
   - `:222-225`: `n_q` falling `330→237` allegedly means “MORE matched terms”, and slopes `−1.72/−1.85` are “slightly steeper than q^-2”.
   - Falling counts mean fewer total q-cosets, while `−1.72` and `−1.85` are shallower than `−2`.
   - Least squares directly on the displayed totals gives approximately `−1.759` and `−1.969`, not `−1.72` and `−1.85`.

   **Demanded correction:** Regenerate all prose and fits from the committed table, state the precise fit convention, change the X′=40 range to approximately `0.019–0.030`, and remove the erroneous “more/steeper” explanation.

16. **MAJOR — the scalar pole order contradicts itself.**

   - `LAW_RATE_MEASURE.md:24-30`: `|φ_∞|` grows like `r^-2`.
   - Contradiction: `:134-139`: the scalar entry has clean `r^-1` simple-pole growth; only the 2×2 determinant has order two.
   - `LAW_R4_THETA_DEFECT.md:97-108` agrees with the simple scalar pole.

   **Demanded correction:** Change the headline to `r^-1`; reserve `r^-2` for `det Φ`.

17. **MINOR — stale and small consistency errors remain unmarked.**

   - `LAW_RATE_MEASURE.md:6-13,232-233,286-301`: q64 unfinished and JSON still appending; contradicted by `LAW_HEJHAL_CH6S12_CH11S3_EXTRACT.md:61-71` and `MAP.md:157`, where 48/48 is complete.
   - `LAW_HEJHAL_S7_EXTRACT.md:141-142`: R1–R5 “not started”; current `MAP.md:149-156` records R1/R2/R4/M2 work.
   - `MAP.md:144`: branch audit “queued”; `MAP.md:155` says it is discharged.
   - `LAW_RATE_MEASURE.md:293-295`: `216.7/21.3` is `10.17×`, not `~8×`.
   - `projects/aristotle_dispatch_v27/RateCoreII.lean:78` says the collision words are nonzero for every `λ>0`; the formula vanishes at `λ=1/√2`. The intended Hecke range is safe, but the comment is false as written.
   - `projects/aristotle_dispatch_v26/DISPATCH.md:75-86` says “8 statements”; the eight obligation rows contain nine named theorem declarations.

   **Demanded correction:** Add dated supersession blocks rather than silently rewriting historical notes; fix the arithmetic/comment/counting statements. Label the v26 root Lean file as superseded dispatch input, distinct from the corrected harvested result.

**Weakest link:** the corrected **coset-level M1**. R2 itself concedes at `LAW_R2_RATE_LEMMA_DRAFT.md:317-320` that without M1 the matched/escaping split is data, not proof. The only formal general proxy is c-only and false at depth three. Until a normal-form theorem controls full coset invariants and localizes the complement, neither the `q^{3-2σ}` summation nor the RATE exponent follows. M2 normalization/G1/G2 and the nonconverged target height `t≈7.0665` are the next blockers; R3 transport and M3 uniformity remain open afterward.

**Explicitly clean categories:**

- No numeric contradiction was found in the R4 residue, `γ₁/2` location, or the distinction between the `0.6604` sampled anchor and `0.2167845…` residue magnitude.
- M2’s displayed arithmetic `4.5913, 3.4692, 0.5713, 0.2835`, and `T(10)=6.4358` is correct conditional on M2.L/G1/G2.
- The q64 slope calculations themselves match the committed JSON; the defect is the convergence count and inference.
- The exponent formula `q^{1-2σ}` correctly gives `−1.2` and `−1.5`; the claim that every measured slope is at least that fast is false.
- The Hejhal scan hashes and printed theta-entry normalization are consistent.
- The v26 harvested result contains no live `sorry` and genuinely proves corrected P4, the Chebyshev c-identities, and depth-1/depth-2 statements. It does not prove general M1 or the P6 derivative.
- The branch-defect audit preserves its branch-specific scope and keeps t=7/t=14 truncation separate; its future-use warning about raw `K_q_corrected` is appropriate.
- `MAP.md:154` is ledger-clean in scope: it explicitly labels pins self-generated, pin rigor `NONE`, makes no `ρ*` claim, and calls the results box certificates rather than assembled theorems.
- No hunt category is globally clean: numeric consistency, ledger-rule propagation, receipts, and stale-status handling all have defects above.



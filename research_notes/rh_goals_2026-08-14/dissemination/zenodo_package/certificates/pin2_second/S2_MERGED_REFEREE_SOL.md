# S2 merged-contour cold adversarial referee report

- Date: 2026-08-26
- Status: UNREFEREED
- Author: gpt-5.6-sol via codex

This review treats the merged receipt, its hash-resolved chunk inputs, the bound code archived in the campaign bundle, the live theorem-assembly notes, and the banked primary-source PDFs as separate layers. I did not run the certification program. Receipt parsing, SHA-256 checks, exact dyadic arithmetic, endpoint/ordering checks, and decimal interval arithmetic were the only numerical work.

## 1. Winding and the finite-to-Fredholm passage — CONFIRMED

The winding calculation is not merely a point-sample winding. Each accepted leaf contains the image of an entire closed parameter arc under the finite determinant

\[
D_N(s)=\det(I-P_NL_sP_N).
\]

`_jacobi_taylor_arc` encloses that image in `finite_Taylor_det_box`. `certified_winding_via_overlap_polygon` selects one point in every cyclic adjacent-box intersection and replaces each actual image arc by the segment joining the two selected points. Both curves and the straight interpolation between them remain inside the same convex rectangle, and every such rectangle excludes zero. The construction therefore preserves winding. The stored winding ball is

`[0.999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999996472261 +/- 1.22e-113]`,

which pins the integer to `1`.

The passage is also licensed for the analytic Hilbert-space Fredholm determinant, not only for the finite matrix. `TB_R1_HILBERT_RESTATEMENT.md` gives the required finite-section identity

\[
\det_{P_NH}(I-P_NL_sP_N)=\det_H(I-L_sP_N)
\]

by the finite-range determinant identity and Sylvester identity. The endpoint trace-bound phase then supplies

\[
|\det_H(I-L_s)-D_N(s)|\leq F_R
\]

uniformly on the whole coordinate box, with

`F_R_upper_bound = [2.08944841554480794546893170303518402484279326150214266103429255553903168777160838104954000553255960867179384564034473972e-8 +/- 4.18e-128]`.

The determinant perturbation formula used in the code is `T_tail(N) * exp(1 + 2*B_same(N))`. The minimum certified boundary clearance after subtracting this error is

`[3.06455432937695175525195262005655994346423176440780165413600568643794900752254193539243802403115848655197110360098571341e-8 +/- 3.07e-126]`,

strictly positive. Hence the straight-line homotopy

\[
H_t(s)=(1-t)D_N(s)+t\det_H(I-L_s)
\]

cannot meet zero on the boundary. The Fredholm determinant has the same winding, namely `1`. Once its analyticity on this box is supplied by the R5 common-continuation result discussed in item 4, the argument principle gives one interior Fredholm zero counted with multiplicity.

Adversarial conclusion: the merge function itself reparses only the finite boxes and trusts the per-chunk inflated-box gates. That would be too weak against a fabricated receipt. I therefore checked the selected records as artifacts: all `452` have both finite and inflated exclusions true, and the displayed global minimum is the minimum of their certified finite-lower-minus-`F_R` margins. The finite-to-Fredholm step is sound, but its proof is distributed across R1, the endpoint-bound phase, and the chunk records rather than self-contained in the merged JSON.

## 2. Closed contour, tiling, seams, and orientation — CONFIRMED

The `16` half-open ranges are

`[0,12), [12,24), [24,36), [36,48), [48,60), [60,72), [72,84), [84,96), [96,108), [108,120), [120,132), [132,144), [144,156), [156,168), [168,180), [180,192)`.

They tile `[0,192)` exactly once. The canonical contour has `48` base arcs on each edge and is counter-clockwise: bottom left-to-right, right bottom-to-top, top right-to-left, and left top-to-bottom.

I independently replayed the receipt-level geometry without importing the certifier:

- The selected chunks contain `452` accepted leaves and `260` subdivisions.
- For every base arc, the `L`/`R` lineage suffixes tile `[0,1)` exactly in rational dyadic arithmetic; no base arc is absent or repeated.
- Every recorded `edge`, `edge_name`, and `edge_index` agrees with its base-arc index and the canonical four-edge ordering.
- Every `s_start` and `s_end` agrees with the corresponding canonical rectangle edge and dyadic parameter interval; all `452` adjacent endpoint pairs overlap, including the last-to-first wrap seam.
- The `452` finite determinant boxes overlap cyclically in the same order. The selected endpoint of one argument-increment record is exactly the selected start of the next, including the closing record.
- Re-summing the serialized argument increments reproduces the stored winding ball.

Thus the chunks compose into one closed cycle. There is no gap, overlap, doubled base arc, reversed edge, or missing wrap seam in the selected artifacts.

The implementation has a defense-in-depth omission: `merge_chunks_and_verify_closure` validates range and lineage tiling but does not regenerate the canonical geometric endpoints from the box definition. This review performed that missing check; it passed. A future merge should perform it in code rather than trust record metadata.

## 3. Legitimacy and provenance of the 16 chunks — CONFIRMED

All `16` SHA-256 values in the merged receipt resolve byte-for-byte to files under `kaggle_s2_contour/local_receipts/`. Across those selected files I confirmed:

- `N = 288`, matrix dimension `864`, precision `384` bits, sign `+1`, and one identical S2 coordinate box;
- one identical exact-geometry record and endpoint-trace-bound record;
- one identical nine-entry `source_bindings` map;
- one identical endpoint `F_R` family and matching merged `F_R_upper_bound`;
- `status = complete`, `CHUNK_ARCS_CLEAR`, `chunk_gate_pass = true`, complete local cover, and both finite and inflated exclusion gates true.

The local replacement of `a036-048` is genuine. `LOCAL_FILL.log` records the 2026-08-26 `F_R`-uniformity rerun, and the resulting file has SHA-256

`7247dcecf63e3cf1716fc0b68ba2f6e73fb9407d0e97e10bb7245d802350a07c`,

exactly the hash selected by the merged receipt. The older same-named harvested file has SHA-256

`35dd66051cd3dda44533a08a18062904d9694956698a77493bb71593a0bf2d21`

and was not selected. Both versions carry the same mathematical source bindings and geometry, but their platform-dependent upper bounds differ. The merge explicitly skips names ending in `.ckpt.json`; the selected SHA-256 proves that no checkpoint contaminated the aggregate.

There is nevertheless a material reproducibility defect. The merged receipt records only chunk basenames, not `local_receipts/...` paths. With the merge script's current default directory order, the stale complete harvested `a036-048` wins over the local rerun. The remaining ranges come from the local directory, producing two different `F_R` strings, so the current default merge aborts rather than recreating the stored receipt. The aggregate is hash-resolvable and internally coherent, but not reproducible by the default command.

The chunks bind the run-time orchestrator SHA-256

`4ac59a18767bbf36ff39b0fb90a910685ea92b07391c352cff87ee75c8203840`.

The current file at the recorded source path has SHA-256

`7468cbd19a5866b1df2870a93de1330ea4f35252afd665d4948b949a606a010e`,

but the campaign bundle contains the exact bound `4ac59a18767bbf36ff39b0fb90a910685ea92b07391c352cff87ee75c8203840` source. A direct diff shows that the current change only adds platform/version fields to newly produced receipts; it does not alter the computation. The actual merge script has SHA-256

`1fb975c2a201b58186dc74b17e9cf7cf92a49efaf1ced798e7ec3436fdefa0b9`,

but that hash is not recorded in the merged JSON. These are provenance defects requiring correction, not numerical refutations of the stored aggregate.

## 4. Fredholm zero to Selberg zero and scattering zero — CONFIRMED

The merged receipt does not itself certify this bridge, but the bridge is supported by the separate artifacts and primary sources.

First, `TB_R5_DETERMINANT_IDENTIFICATION.md` identifies the certified Hardy/Hilbert operator with the MMS Banach-space reduced `+` sector on

\[
\Omega^*=\{\operatorname{Re}s>1/2\}\cup\{\operatorname{Re}s>0,\operatorname{Im}s>1\}.
\]

The entire S2 box lies in the second component because its lower coordinate bounds are `0.41054273549473627` and `7.81976724701551188`. R5 proves equality of the two determinants first on an absolute-convergence region and then on `Omega*` by analyticity and the identity theorem. Its exact block list, signs, branch maps, squared-weight convention, and tail starts match the bound `tc_rerun.py` calls for `q = 5`, `h_q = 1`, `kappa_q = 3`, sign `+1`.

Second, the banked MMS PDF `MMS_arxiv_0912.2236.pdf`, SHA-256

`a10020bd084534dc60fc3e887958f1583f2fc115d567961b461df1a59b32e072`,

states in Theorem 6.4

\[
Z_{G_q}(s)=\frac{\det(1-L_{s,+})\det(1-L_{s,-})}{\det(1-K_s)}.
\]

For `q = 5`, the exact `K_s` product used in `KS_GATE_REPORT.md` has zeros only at real part `-n`, `n >= 0`. The S2 box has strictly positive real part, so the denominator is zero-free on the whole box; no point-distance approximation is needed. The plus-sector Fredholm zero therefore forces a Selberg-zeta zero in the box.

There is a source-citation defect that must be carried honestly. In the MMS PDF, equation (34) is the odd-`q` reduced-operator display, while Theorem 6.4 is the later determinant factorization. The heading over equation (34) prints `q = 2h_q + 3 > 5`, even though the paper's general odd-`q` incidence formulas, Lemma 6.3, Theorem 6.4, and its explicit `q = 5` functional equation use odd `q >= 5`. The `h_q = 1` specialization also reproduces the exact three-row code. The bridge survives, but an assembly must disclose this internal heading inconsistency and must not misidentify equation (34) as the factorization.

Third, the Selberg-to-scattering step is not proved by Aristotle's Lean result alone. `SCAT1_LEMMA31_ARISTOTLE.md` machine-verifies only the reflection core: a pole of the scalar scattering function at `s` becomes a zero of the same order at `1-s` under `phi(s) phi(1-s) = 1`. The load-bearing assertion that a nonreal off-line Selberg zero supplies the relevant scattering divisor is separate.

I opened the banked Friedman-Jorgenson-Smajlovic source directly (`/tmp/fjs.pdf`, SHA-256 `36c9d020fcc7d0118264c486330db9936f866670c45c0e77b185cdc2b9127228`). Its completed-zeta definition is

\[
Z_+(s)=\frac{Z(s)}{G_1(s)\Gamma(s-1/2)^k},\qquad Z_-(s)=Z_+(s)\phi(s),
\]

and its enumerated nontrivial zero set identifies the nonreal left-half-strip zeros with reflections of scattering-determinant zeros, with the functional symmetry stated explicitly. The gamma and `G_1` trivial divisors are on real loci and do not meet either pin box. MMS also states that every Hecke triangle group has one cusp, so for trivial representation the scattering matrix is `1 x 1` and its determinant is the scalar `phi_5`. This supplies the divisor step needed here. `M1F_EISENSTEIN_DERIVATION.md` does not supply this bridge and must not be cited as if it did; its own resonance-transport and sector-assignment items remain gaps.

Accordingly, the assembled Fredholm-to-`Z_{G_5}`-to-`phi_5` implication is supported. The correction is attribution and assembly scope: Lean verifies the reflection core only, while R5, MMS Theorem 6.4, exact `K_s` exclusion, and the scalar divisor source carry the other steps.

## 5. Distinct reflected real parts — CONFIRMED

The artifacts give boxes, not exact zero coordinates.

For the flagship Selberg zero, the real interval is

`[0.4538941800749447, 0.4538961800749447]`.

After reflection, the corresponding `phi_5` zero has

`Re rho_1 in [0.5461038199250553, 0.5461058199250553]`

and

`Im rho_1 in [-5.7635382417301305, -5.7635362417301305]`.

For the S2 Selberg zero, the real interval is

`[0.41054273549473627, 0.41054473549473627]`.

After reflection, the corresponding `phi_5` zero has

`Re rho_2 in [0.58945526450526373, 0.58945726450526373]`

and

`Im rho_2 in [-7.81976924701551188, -7.81976724701551188]`.

The reflected centers differ by `0.04335144458020843`, and the rigorous gap between the two closed real intervals is `0.04334944458020843`. The intervals are therefore disjoint by a large margin and both lie strictly in `1/2 < Re s < 1`. They satisfy the distinct-real-part condition in NOGO-OPEN-1 and the two-pin premise of `NO_VERTICAL_LINE_COROLLARY`.

The corrected S2 reflected center is

`1 - 0.41054373549473627 = 0.58945626450526373`,

which rounds to `0.5894562645052637` at `16` digits after the decimal point. The earlier `0.5894543` is false; it differs from the correct center by `0.00000196450526373`.

The wording `Re rho_2 = 0.5894562645052637` is also false as a theorem claim: that number is the box center, not the certified zero's exact real coordinate. Only the interval statement above is licensed. The same qualification applies to `Re rho_1 approximately 0.5461`.

## 6. Missing controls and assembly — CONFIRMED

The receipt explicitly leaves an `N = 128` control arm and an S2 assembly document outstanding.

The missing `N = 128` arm is not a logical premise of the `N = 288` argument-principle certificate. The `N = 288` trace-norm error bound and its positive boundary margin stand on their own. Its absence nevertheless removes a planned negative/regression control, weakens comparison with the flagship campaign's acceptance package, and makes it harder to detect a shared implementation or artifact-selection error. It should be completed or explicitly waived as non-load-bearing before promotion; it must not be silently described as passed.

The missing assembly document matters more to scope. The merged JSON certifies only its finite/Fredholm contour conclusion and says so. It contains neither R5, MMS Theorem 6.4, the exact `K_s` exclusion, the scalar scattering-divisor source, nor the distinct-box arithmetic. Those links can be assembled from existing artifacts, as item 4 does, but until an S2-specific assembly records them, the receipt alone cannot close either ledger item.

## 7. Literal overclaiming audit — REFUTED

The literal statement “the merged receipt certifies a second `Z_{G_5}` zero, gives an exact `phi_5` real part, and closes both ledger items” is false. The gaps between the receipt and that sentence are:

1. The receipt's own status is `UNREFEREED`.
2. It literally claims only a finite/Fredholm determinant zero and explicitly calls the control arm and assembly separate steps.
3. Its chunk basenames omit the actual `local_receipts/...` provenance, and the current default merge does not recreate it.
4. It does not bind the merge script or point to the archived run-time orchestrator after the live path changed.
5. It does not contain the R5 Hilbert-to-MMS determinant identity, the MMS quotient, or the `K_s` divisor exclusion.
6. It does not contain the Selberg-to-scalar-scattering divisor theorem. Aristotle's Lean proof covers only the subsequent reflection core.
7. A winding of `1` locates a zero somewhere inside the box; it does not place the zero at the box center.
8. `0.5894562645052637` is a rounded reflected center, not an equality for the zero's real part. `0.5894543` is numerically wrong.
9. The planned `N = 128` control has not been run.
10. The existing ledger documents remain textually open; no receipt field or automatic consequence edits them.
11. `M1F_EISENSTEIN_DERIVATION.md` retains its own transport gaps and cannot be substituted for the q=5 R5/MMS/FJS chain.
12. The MMS equation-(34) heading inconsistency at `q = 5` and the distinction between equation (34) and Theorem 6.4 must be disclosed.

The stronger mathematical conclusion is nevertheless supported after assembling the separate links: the hash-resolved S2 contour artifacts give a plus-sector Fredholm zero in a box disjoint from the flagship box; R5 and MMS with zero-free `K_s` give a second Selberg zero; the scalar divisor theorem and reflection give a second `phi_5` zero in the reflected interval; and the two reflected real intervals are disjoint.

**VERDICT: PROMOTABLE-WITH-CORRECTIONS** — promotion is conditional on making every correction below exactly:

1. Replace “the merged receipt certifies a second zero of `Z_{G_5}`” with “the merged receipt certifies winding `1` for the q=5 plus-sector Hilbert Fredholm determinant; the separate R5 + MMS Theorem 6.4 + zero-free `K_s` assembly promotes it to a `Z_{G_5}` zero.”
2. Replace “`Re rho_2 = 0.5894562645052637`” with “`Re rho_2 in [0.58945526450526373, 0.58945726450526373]`, whose interval center is `0.58945626450526373`.” Replace the first pin by its interval `Re rho_1 in [0.5461038199250553, 0.5461058199250553]` as well.
3. Attribute only the pole-to-reflected-zero step to the Aristotle/Lean reflection core. Cite the Friedman-Jorgenson-Smajlovic completed-zeta divisor statement and the one-cusp scalar specialization for the Selberg-to-`phi_5` step.
4. Reissue or amend the merged provenance so every chunk records its `local_receipts/...` path, the actual merge script SHA-256 `1fb975c2a201b58186dc74b17e9cf7cf92a49efaf1ced798e7ec3436fdefa0b9`, the archived producer path and SHA-256 `4ac59a18767bbf36ff39b0fb90a910685ea92b07391c352cff87ee75c8203840`, and an explicit local-only merge command that recreates the stored hashes and common `F_R`.
5. Correct the MMS citation: equation (34) is the odd-`q` reduced operator; Theorem 6.4 is the determinant quotient. Carry the printed `q > 5` heading inconsistency and the independently checked `h_q = 1` specialization for `q = 5`.
6. Complete the planned `N = 128` control, or label it explicitly as an unrun, non-load-bearing negative control in the promoted package.
7. Add an S2-specific assembly document containing the R5 domain check, MMS sector identification, exact whole-box `K_s` exclusion, scalar scattering-divisor source, reflected intervals, and rigorous interval separation before changing NOGO-OPEN-1 or `NO_VERTICAL_LINE_COROLLARY` from open to closed.

## What a second referee must check

- Resolve all `16` merged SHA-256 values independently to the intended `local_receipts/...` files and reproduce the merge with an explicit directory choice; verify that the stale harvested `a036-048` and every `.ckpt.json` are excluded.
- Recompute the exact `452`-leaf dyadic tiling, canonical rectangle endpoints, counter-clockwise ordering, all chunk seams, and the cyclic wrap seam from the box geometry rather than trusting JSON flags.
- Recompute the winding from the serialized finite determinant boxes and independently audit the convex-box homotopy, including the last-to-first overlap.
- Audit the R2 input-tail and output-tail bounds entering `B_same`, the determinant perturbation inequality, the finite-section/Sylvester identity, and the minimum finite-lower-minus-`F_R` calculation.
- Compare the archived SHA-bound producer to the current producer and verify that the only changes are receipt-environment provenance fields.
- Derive the `q = 5`, sign-`+1` three-row operator directly from the full odd-`q` MMS matrix and symmetry restriction, explicitly confronting the printed equation-(34) heading.
- Check R5 determinant equality on the entire S2 box, not merely at its center, and verify `det(1-K_s)` is zero-free on the whole closed box from the exact lattice.
- Open the Friedman-Jorgenson-Smajlovic source and independently verify the nonreal Selberg/scattering divisor statement, the absence of trivial divisors in both pin boxes, the one-cusp scalar specialization, and the precise scope of the Lean reflection theorem.
- Verify the two reflected real and imaginary intervals, their positive separation `0.04334944458020843`, and the exact logical hypotheses of both ledger items.
- Review the `N = 128` control result and the completed S2 assembly before authorizing any ledger-status change.

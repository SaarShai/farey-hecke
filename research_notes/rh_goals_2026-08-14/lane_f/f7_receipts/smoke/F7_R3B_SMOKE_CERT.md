# VERDICT: THEOREM-GRADE closed-contour NO — partial at N=256

Run status: `partial`.

## 1. Constants and provenance

- Execution error: `SignalTermination: signal 15`
- Arithmetic: python-flint Arb/Acb at `384` bits.
- Flagship s-box: center `0.4751647621098225 + 4.668743786424289 i`, coordinate half-width `1e-6`.
- Operator: q=7, sign `+1`, engine head split `4`; exact radius strings `3.522`, `2.622`, `2.372`, `1.79`, `1.6`.
- Closed cover: `4*48=192` base arcs; primary `N=256`, arithmetic/failure comparison `N=224`.
- Immutable R2 receipt required sha256 `4e5f0105e80f6f4fc0e173750abc628534bbc944928f759b1cf3e12bb9202efc`; consumed unchanged: `True`.
- Immutable TB V2 receipt required sha256 `93baddf565b2dca6e94da441a9d7e906ab81576c4acf3506ab334bcf1251f4f6`; consumed unchanged: `True`.
- R2_receipt: `/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_f/f7_receipts/F7_R2_FLAGSHIP_ENVELOPE_RECEIPT.json` — sha256 `4e5f0105e80f6f4fc0e173750abc628534bbc944928f759b1cf3e12bb9202efc`.
- TB_V2_receipt: `/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_f/f7_receipts/F7_TB_BLOCK_CERTIFICATES_RECEIPT.json` — sha256 `93baddf565b2dca6e94da441a9d7e906ab81576c4acf3506ab334bcf1251f4f6`.
- attempt1_report: `/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_f/F7_PILOT2_REPORT.md` — sha256 `2bbebd689de07814ed888aab0998c24d70539b12712dcfd50615c4f1dda24e30`.
- R1_restatement: `/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_f/F7_TB_R2_RECEIPTS.md` — sha256 `02230ad94f4480659d2b5b0ffbdaaa99a01a7b6c0557a907c752c59c51e20ba7`.
- engine: `/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/zeta_cert_rosen.py` — sha256 `b6ee87fd8f35f0b704323a1f4c0f7d1c510b5ac6c79a0d6dbf58c95d70e28a0f`.
- R2_code: `/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_f/f7_certify_r2_flagship.py` — sha256 `56d30d4771a832998c790096fba8026b7ecbd6257d443d29733c1db12fbb296f`.
- R3b_orchestrator: `/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_f/f7_certify_r3b_flagship.py` — sha256 `df9873d9f1e47c47f2e846d38d906f8f77619a17871e6d7c6da8c225bb63f687`.
- R3b_derivative: `/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_f/f7_r3b_engine.py` — sha256 `661a4d2b132d1821d18499a302f58805bf7565e560d8f1520379dde156bc7d1a`.
- R3b_endpoint: `/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_f/f7_r3b_endpoint.py` — sha256 `3ad7918899c70bda3efb50cabd3a9814e7fb9c7fd6c1214e398d3996ac78478c`.
- R2 B_total (comparison only): `[119.06285559909506923733105505540038073444204661321639737225436126041286995631480026545596 +/- 4.39e-87]` from `/B_total_full_operator_column_sum_upper_bound`.
- R2 T_tail(224): `[1.4792058281325539748603802619554165552377648576548274999569040540025817664661217849158409e-23 +/- 7.80e-113]`; T_tail(256): `[2.4114870765008821786740995136173071286026016793840098027676886638887413159663541053986189e-27 +/- 8.08e-117]` from immutable `/tail_bounds`.
- Enlarged-contour cover: `512` closed Acb arcs per block.
- Per-block enlarged radius: original R plus one quarter of the certified minimum pole/cut clearance; `eta=R/R_enlarged<1`.
- Enlarged-contour U bounds: direct single-branch sup, or Hurwitz-closed Phi0 plus the R2 center-split `A q^k + C k rho^(k-1)`.
- M' central-difference sanity at arc 0, N=6: matrix agreement `15` digits; Jacobi determinant derivative agreement `15` digits (step `1e-8`).

## 2. Closed-arc exclusions and winding

Closed-contour run is partial: N=`256`, evaluations=`0`, accepted subarcs=`0`, pending=`unknown`. No winding claim is made.

## 3. Theorem-valid endpoint trace norm

### N=256

- Computed-row column 2-norm sum: `[20.1696369233844020573936104029716156288641170873265410730893361242905387384343107542821575120833917614727126075517631667 +/- 2.07e-119]`.
- Sum of enlarged-disc output-tail corrections: `[70749595.63308117425554916010481337892139745760005468682033721327756433148282090778307369556964996437 +/- 5.8e-95]`.
- Retained full-column sum B_ret: `[70749615.8027180976399512174984237818930130864641717741468782863669004557733596462173844498518074764592690648551948451153 +/- 2.40e-113]`.
- Immutable input tail T_tail: `[2.41148707650088217867409951361730712860260167938400980276768866388874131596635410539861890808000003354449905512392399933e-27 +/- 3.48e-147]`.
- Same valid bound for both endpoints `||L||_1, ||LP_N||_1`: `[70749615.8027180976399512174984237843045001629650539528209777999842075843759613256013942526194961403480103808215489532487 +/- 5.00e-113]`.
- `F_R=T_tail*exp(1+2*B_same)`: `[1.97865724449533330128944608643403565074649821781351705522695503693180660762347018863658028317124480313843933649502163880e+61452309 +/- 4.01e+61452189]`.
### N=224

- Computed-row column 2-norm sum: `[20.1696367902021966529810981155512125120173547828291547019948737243184256175648670494537043851666776384626234899332489337 +/- 1.22e-119]`.
- Sum of enlarged-disc output-tail corrections: `[11795452.17476872102710322306885374038995248251344048586163646271097099902233012561747691025835700477 +/- 1.12e-93]`.
- Retained full-column sum B_ret: `[11795472.3444055112292998760499518559411649945307952686907911647058447233407557431823439597120613899358297587672205835337 +/- 4.10e-113]`.
- Immutable input tail T_tail: `[1.47920582813255397486038026195541655523776485765482749995690405400258176646612178491584090780000001972005630934915596117e-23 +/- 4.33e-143]`.
- Same valid bound for both endpoints `||L||_1, ||LP_N||_1`: `[11795472.3444055112292998760499666479994463200705438724934107188713971009893322914573435287526014157534944199850697422215 +/- 4.91e-113]`.
- `F_R=T_tail*exp(1+2*B_same)`: `[5.07643166716469098029519103678566866915775625278155690329615306591545609302876075774056185886008352265289576496567921521e+10245394 +/- 4.40e+10245274]`.

## 4. Failed inequalities and numeric margins

The run is partial; unevaluated inequalities are explicitly not claimed to pass.

## Mathematical validity and scope

For a closed straight subarc A with midpoint s0 and radius r, Acb inversion of `A(s)=I-M(s)` over the whole subarc certifies `H >= sup |tr(A(s)^(-1) M'(s))|`. Jacobi gives `|d'(s)| <= H |d(s)|`. If `D=sup_A |d'|`, the segment mean-value integral gives `sup_A |d| <= |d(s0)|+rD`, hence `D <= H(|d(s0)|+rD)`. The certified inequality `rH<1` therefore yields `D <= G := H|d(s0)|/(1-rH)`, and `d(s0)+ball(0,rG)` contains `det(I-M(s))` for every s in the closed subarc.

For each retained column, Cauchy's coefficient estimate on the certified enlarged output disc gives `|a_m| <= U eta^m`; summing `m>=N` gives `U eta^N/(1-eta)`, which dominates the omitted-output H2 norm. Adding this to the computed-row 2-norm gives a full retained-column bound. Adding immutable R2 `T_tail(N)` bounds `||L||_1`; the same sum also bounds `||LP_N||_1`.

The finite Taylor cover supplies the certified argument increments. Because every F-inflated tube excludes 0, the straight-line perturbation from the finite determinant to the Fredholm determinant stays nonzero on the boundary, so winding is preserved.

Scope: this is the R2/R3 closed-contour computation. MMS sector/factorization and the separate closed `det(1-K_s) != 0` identification remain outside this verdict, as in the mandatory attempt-1 report.


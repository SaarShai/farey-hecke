# VERDICT: THEOREM-GRADE closed-contour NO at N=256

Run status: `complete`.

## 1. Constants and provenance

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
- R3b_endpoint: `/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_f/f7_r3b_endpoint.py` — sha256 `3d397de0091229668cd73be2f353e19b67cd4e710bc2e552685123f111cb8c9d`.
- R2 B_total (comparison only): `[119.06285559909506923733105505540038073444204661321639737225436126041286995631480026545596 +/- 4.39e-87]` from `/B_total_full_operator_column_sum_upper_bound`.
- R2 T_tail(224): `[1.4792058281325539748603802619554165552377648576548274999569040540025817664661217849158409e-23 +/- 7.80e-113]`; T_tail(256): `[2.4114870765008821786740995136173071286026016793840098027676886638887413159663541053986189e-27 +/- 8.08e-117]` from immutable `/tail_bounds`.
- Enlarged-contour cover: `512` closed Acb arcs per block.
- Per-block enlarged radius: original R plus one quarter of the certified minimum pole/cut clearance; `eta=R/R_enlarged<1`.
- Enlarged-contour U bounds: direct single-branch sup, or Hurwitz-closed Phi0 plus the R2 center-split `A q^k + C k rho^(k-1)`.
- M' central-difference sanity at arc 0, N=6: matrix agreement `15` digits; Jacobi determinant derivative agreement `15` digits (step `1e-8`).

## 2. Closed-arc exclusions and winding

### N=256

- Complete closed cover: `True`; accepted subarcs `12`; adaptive splits `0`.
- Every finite Taylor enclosure excludes 0: `True`.
- Every F-inflated closed-arc enclosure excludes 0: `True`.
- Certified finite-cover argument winding: `None`; winding ball `unavailable`.
- Full determinant winding by the nonvanishing straight-line homotopy inside the F-inflated tubes: `None`.
- Minimum finite Taylor |det| lower bound: `[2.41502002976608377729898035410150963732778061893731668185173078569906867697395720063218115245365025068513187817866021996e-6 +/- 9.54e-125]`.
- Minimum certified `finite lower - F` margin: `[2.41285380530118956012129676683210495601606866410337633466195199007117256627396036352247008992945747582134627729365453219e-6 +/- 1.01e-124]`.
- Maximum Taylor radius `rG`: `[8.88494738000128345959580732564724936578008719347659715020153362606025167769962779535013356742527326182345264442883782127e-7 +/- 4.81e-125]`; maximum self-consistency factor `rH`: `[0.211063924743695573064727361150339119414874896563201578568383981013938997959206747411356504809408970530257821563536386734 +/- 1.30e-119]`.
### N=224

- Complete closed cover: `False`; accepted subarcs `0`; adaptive splits `0`.
- Every finite Taylor enclosure excludes 0: `False`.
- Every F-inflated closed-arc enclosure excludes 0: `False`.
- Certified finite-cover argument winding: `None`; winding ball `unavailable`.
- Full determinant winding by the nonvanishing straight-line homotopy inside the F-inflated tubes: `None`.
- Minimum finite Taylor |det| lower bound: `None`.
- Minimum certified `finite lower - F` margin: `None`.
- Maximum Taylor radius `rG`: `None`; maximum self-consistency factor `rH`: `None`.

## 3. Theorem-valid endpoint trace norm

### N=256

- Computed-row column 2-norm sum: `[20.1696369233844355095351318663678808976454087505001476309706301840016652295612162340827558268021086857807780463560229727 +/- 3.07e-119]`.
- Sum of enlarged-disc output-tail corrections: `[7.706042496573776902616531098546786270709958158012581816423107648942442481065931398377819786560871581e-13 +/- 4.05e-113]`.
- Retained full-column sum B_ret: `[20.1696369233852061137847892440581425507552634291272186267864314421833075403261104783308624199419464677594341335142295184 +/- 4.10e-119]`.
- Immutable input tail T_tail: `[2.41148707650088217867409951361730712860260167938400980276768866388874131596635410539861890808000003354449905512392399933e-27 +/- 3.48e-147]`.
- Same valid bound for both endpoints `||L||_1, ||LP_N||_1`: `[20.1696369233852061137847892464696296272561456078013181404037385707859092197101202810985510838306877837257882389128489895 +/- 3.44e-119]`.
- `F_R=T_tail*exp(1+2*B_same)`: `[2.16622446489421717768358726940468131171195483394034718977879562789611069999683710971106252419277486378560088500548535025e-9 +/- 3.52e-129]`.
### N=224

- Computed-row column 2-norm sum: `[20.1696367902022301031923814395936146632242676028810886060642258622242080538441813371265240438976788053261105221318711543 +/- 3.18e-119]`.
- Sum of enlarged-disc output-tail corrections: `[6.747801381654432463403155345030222665600680570213259087440726332420557240756137680240209362036953164e-11 +/- 9.18e-112]`.
- Retained full-column sum B_ret: `[20.1696367902697081170089257642276462166745698295370954117663584530986153171683869095340854207000808989464800537766289032 +/- 1.79e-119]`.
- Immutable input tail T_tail: `[1.47920582813255397486038026195541655523776485765482749995690405400258176646612178491584090780000001972005630934915596117e-23 +/- 4.33e-143]`.
- Same valid bound for both endpoints `||L||_1, ||LP_N||_1`: `[20.1696367902697081170089405562859275422143184333397149659319108307471918654433864785746254465177455601643292121857076666 +/- 5.15e-120]`.
- `F_R=T_tail*exp(1+2*B_same)`: `[1.32876142346267259961242752273340372801761717627698322593775315739325224350653852550499270163395284578968575905847299212e-5 +/- 1.40e-125]`.

## 4. Failed inequalities and numeric margins

- N=224, arc `0`: F-inflated Taylor enclosure contains zero; finite lower - F = `[-9.44306558608178031101452325736845754625867430555853709397368416670850097410179090033018575452990544050989028851980609739e-6 +/- 3.03e-126]`, finite Taylor lower = `[3.84454864854494568510975196996557973391749745721129516540384740722402146096359435471974126180962301738696730206492440468e-6 +/- 1.81e-126]`, F = `[1.32876142346267259961242752273340372801761717627698322593775315739325224350653852550499270163395284578968575905847303084e-5 +/- 4.53e-125]`, rH = `[0.107888119301220750826196699192242344433423394694622621593859259623696428819898030596621497937041547845781741968483190216 +/- 2.58e-121]`.

## Mathematical validity and scope

For a closed straight subarc A with midpoint s0 and radius r, Acb inversion of `A(s)=I-M(s)` over the whole subarc certifies `H >= sup |tr(A(s)^(-1) M'(s))|`. Jacobi gives `|d'(s)| <= H |d(s)|`. If `D=sup_A |d'|`, the segment mean-value integral gives `sup_A |d| <= |d(s0)|+rD`, hence `D <= H(|d(s0)|+rD)`. The certified inequality `rH<1` therefore yields `D <= G := H|d(s0)|/(1-rH)`, and `d(s0)+ball(0,rG)` contains `det(I-M(s))` for every s in the closed subarc.

For each retained column, Cauchy's coefficient estimate on the certified enlarged output disc gives `|a_m| <= U eta^m`; summing `m>=N` gives `U eta^N/(1-eta)`, which dominates the omitted-output H2 norm. Adding this to the computed-row 2-norm gives a full retained-column bound. Adding immutable R2 `T_tail(N)` bounds `||L||_1`; the same sum also bounds `||LP_N||_1`.

The finite Taylor cover supplies the certified argument increments. Because every F-inflated tube excludes 0, the straight-line perturbation from the finite determinant to the Fredholm determinant stays nonzero on the boundary, so winding is preserved.

Scope: this is the R2/R3 closed-contour computation. MMS sector/factorization and the separate closed `det(1-K_s) != 0` identification remain outside this verdict, as in the mandatory attempt-1 report.


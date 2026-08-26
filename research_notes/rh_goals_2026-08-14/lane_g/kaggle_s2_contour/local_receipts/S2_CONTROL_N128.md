# VERDICT: THEOREM-GRADE closed-contour NO at N=288

Run status: `complete`.

## 1. Constants and provenance

- Arithmetic: python-flint Arb/Acb at `384` bits.
- Second-pin (S2) s-box: center `0.41054373549473627 + 7.81976824701551188 i`, coordinate half-width `1e-6`.
- Operator: q=5, sign `+1`, engine head split `4`; exact radius strings `3.14`, `2.27`, `1.70`.
- Closed cover: `4*48=192` base arcs; primary `N=288`, arithmetic/failure comparison `N=128`.
- Immutable R2 receipt required sha256 `6410dff31e503176dbf03a1b181568c99f5bc386287b109ced371f08d7eee83d`; consumed unchanged: `True`.
- Immutable TB V2 receipt required sha256 `73b506f8ee26b1ba9e22eac2e5badc80395bafee15ec687e620201ec6156d63d`; consumed unchanged: `True`.
- R2_receipt: `/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/second_pin/R2_SECONDPIN_ENVELOPE_RECEIPT.json` — sha256 `6410dff31e503176dbf03a1b181568c99f5bc386287b109ced371f08d7eee83d`.
- TB_V2_receipt: `/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_BLOCK_CERTIFICATES_V2_RECEIPT.json` — sha256 `73b506f8ee26b1ba9e22eac2e5badc80395bafee15ec687e620201ec6156d63d`.
- attempt1_report: `/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/second_pin/R2R3_SECONDPIN_CERT.md` — sha256 `82f82b7923601b4e29921f1ae6190b6bee24f9f00f13adae19a026262d0f8386`.
- R1_restatement: `/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_R1_HILBERT_RESTATEMENT.md` — sha256 `6c319b78605efbf7acc2916db80656a95e12daffa313c4a46f26400c64b4861f`.
- engine: `/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/zeta_cert_rosen_q5.py` — sha256 `c84c5c3f6d9f7a320bca7f1dbfd96a4859c3eea9b3de5420eb4eb223ad0d597b`.
- R2_code: `/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/second_pin/certify_r2_flagship.py` — sha256 `16edea6c9212516f2ccd6ec14425480101e80bfea968c85e2d3e667108695347`.
- R3b_orchestrator: `/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/second_pin/certify_r3b_flagship.py` — sha256 `7468cbd19a5866b1df2870a93de1330ea4f35252afd665d4948b949a606a010e`.
- R3b_derivative: `/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/tc_rerun/r3b_engine.py` — sha256 `579ede0d7a9b59ed92305a845263008e89d1559136a07fe3a366326c079cb8eb`.
- R3b_endpoint: `/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/second_pin/r3b_endpoint.py` — sha256 `9927240167b96e19b365bb7bd49d6ec3fe07268d875f17834c342e305c007311`.
- R2 B_total (comparison only): `[203.10387353826911551997336348475650258753894966494577596888858128720391288387593500268874 +/- 1.49e-88]` from `/B_total_full_operator_column_sum_upper_bound`.
- R2 T_tail(128): `[8.0133595081418321531084482717288642913293642580876401174964800594134765013354233768443062e-17 +/- 3.40e-106]`; T_tail(160): `[9.5185738240321838118789421842962792923369841977382874147901563715661482266608204903075018e-22 +/- 1.58e-111]` from immutable `/tail_bounds`.
- Enlarged-contour cover: `512` closed Acb arcs per block.
- Per-block enlarged radius: original R plus one quarter of the certified minimum pole/cut clearance; `eta=R/R_enlarged<1`.
- Enlarged-contour U bounds: direct single-branch sup, or Hurwitz-closed Phi0 plus the R2 center-split `A q^k + C k rho^(k-1)`.
- M' central-difference sanity at arc 0, N=6: matrix agreement `15` digits; Jacobi determinant derivative agreement `15` digits (step `1e-8`).

## 2. Closed-arc exclusions and winding

### N=288

- Complete closed cover: `True`; accepted subarcs `2`; adaptive splits `1`.
- Every finite Taylor enclosure excludes 0: `True`.
- Every F-inflated closed-arc enclosure excludes 0: `True`.
- Certified finite-cover argument winding: `None`; winding ball `unavailable`.
- Full determinant winding by the nonvanishing straight-line homotopy inside the F-inflated tubes: `None`.
- Minimum finite Taylor |det| lower bound: `[3.74480966199806849125075735093942913900237226667752067206395421271308409958597386942554128339671536257122171422861523409e-6 +/- 9.80e-125]`.
- Minimum certified `finite lower - F` margin: `[3.72391517784262041179606803390907729875394433406249924545361128715769378270825778561504588334138976648450377577221157340e-6 +/- 1.03e-124]`.
- Maximum Taylor radius `rG`: `[1.55186932296300594140053415529044699649437747116800090834581130867229576370985636514746100915074668775206742224906587427e-6 +/- 4.91e-125]`; maximum self-consistency factor `rH`: `[0.207833164478418010342165629274747001844612641346556135419862258744871500925699038254420000853135251201446449850073052923 +/- 6.58e-120]`.
### N=128

- Complete closed cover: `False`; accepted subarcs `0`; adaptive splits `0`.
- Every finite Taylor enclosure excludes 0: `False`.
- Every F-inflated closed-arc enclosure excludes 0: `False`.
- Certified finite-cover argument winding: `None`; winding ball `unavailable`.
- Full determinant winding by the nonvanishing straight-line homotopy inside the F-inflated tubes: `None`.
- Minimum finite Taylor |det| lower bound: `None`.
- Minimum certified `finite lower - F` margin: `None`.
- Maximum Taylor radius `rG`: `None`; maximum self-consistency factor `rH`: `None`.

## 3. Theorem-valid endpoint trace norm

### N=288

- Computed-row column 2-norm sum: `[37.6839778232248239423371313856483904751034021134617142395284978987079309195336080217791661022400191767588761990269620021 +/- 4.26e-119]`.
- Sum of enlarged-disc output-tail corrections: `[4.262887907090295998929381124336257795744899115229393064078858567042204543703342922369032171352036982e-11 +/- 2.38e-111]`.
- Retained full-column sum B_ret: `[37.6839778232674528214080343456376842863467646914191632306807918293487195052040300672161995314637094984723965688543724663 +/- 3.20e-119]`.
- Immutable input tail T_tail: `[1.42511503589480827742832184532169468567888262861178458817355998109515684607236336075866556447964840305832553684278841145e-41 +/- 1.92e-161]`.
- Same valid bound for both endpoints `||L||_1, ||LP_N||_1`: `[37.6839778232674528214080343456376842863467789425695221787635661125671727221508868560424856493095912340722075204228332756 +/- 2.50e-119]`.
- `F_R=T_tail*exp(1+2*B_same)`: `[2.08944841554480794546893170303518402484279326150214266103429255553903168777160838104954000553255960867179384564034473972e-8 +/- 4.18e-128]`.
### N=128

- Computed-row column 2-norm sum: `[37.6839778209131869611327968999117201141153284170335085109963703692360355433161562495632152327973669891582717545446785811 +/- 4.11e-119]`.
- Sum of enlarged-disc output-tail corrections: `[0.001989164164700984940029555953221002383161545954215185426816019170761528642598134119949777978829522182 +/- 1.47e-103]`.
- Retained full-column sum B_ret: `[37.6859669850778879460728264558649411164984899629877236964231863884067970719587543836831650107761965113402368140088957899 +/- 3.74e-119]`.
- Immutable input tail T_tail: `[8.01335950814183215310844827172886429132936425808764011749648005941347650133542337684430623400000009447711084120259393656e-17 +/- 2.46e-137]`.
- Same valid bound for both endpoints `||L||_1, ||LP_N||_1`: `[37.6859669850778880262064215372832626475829726802763666097168289692831982469235549778179300241304302797832991540088967448 +/- 2.92e-119]`.
- `F_R=T_tail*exp(1+2*B_same)`: `[117957109755879322.723667500168209221341748650879776742396368896678044031062858520491808428552041794237142901609217336200 +/- 4.52e-103]`.

## 4. Failed inequalities and numeric margins

- N=128, arc `0`: Jacobi arc evaluation failed: ArithmeticError: Jacobi self-consistency rH is not below one: [1.216520408071738556634537104247536255194316310344245802845259828417602173517760757959969379391551474221261854529698 +/- 2.33e-115]; finite lower - F = `unavailable`, finite Taylor lower = `unavailable`, F = `unavailable`, rH = `unavailable`.

## Mathematical validity and scope

For a closed straight subarc A with midpoint s0 and radius r, Acb inversion of `A(s)=I-M(s)` over the whole subarc certifies `H >= sup |tr(A(s)^(-1) M'(s))|`. Jacobi gives `|d'(s)| <= H |d(s)|`. If `D=sup_A |d'|`, the segment mean-value integral gives `sup_A |d| <= |d(s0)|+rD`, hence `D <= H(|d(s0)|+rD)`. The certified inequality `rH<1` therefore yields `D <= G := H|d(s0)|/(1-rH)`, and `d(s0)+ball(0,rG)` contains `det(I-M(s))` for every s in the closed subarc.

For each retained column, Cauchy's coefficient estimate on the certified enlarged output disc gives `|a_m| <= U eta^m`; summing `m>=N` gives `U eta^N/(1-eta)`, which dominates the omitted-output H2 norm. Adding this to the computed-row 2-norm gives a full retained-column bound. Adding immutable R2 `T_tail(N)` bounds `||L||_1`; the same sum also bounds `||LP_N||_1`.

The finite Taylor cover supplies the certified argument increments. Because every F-inflated tube excludes 0, the straight-line perturbation from the finite determinant to the Fredholm determinant stays nonzero on the boundary, so winding is preserved.

Scope: this is the R2/R3 closed-contour computation. MMS sector/factorization and the separate closed `det(1-K_s) != 0` identification remain outside this verdict, as in the mandatory attempt-1 report.


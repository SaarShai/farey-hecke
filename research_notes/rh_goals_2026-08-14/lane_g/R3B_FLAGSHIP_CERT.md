# VERDICT: THEOREM-GRADE closed-contour YES at N=160

Run status: `complete`.

## 1. Constants and provenance

- Arithmetic: python-flint Arb/Acb at `384` bits.
- Flagship s-box: center `0.4538951800749447 + 5.7635372417301305 i`, coordinate half-width `1e-6`.
- Operator: q=5, sign `+1`, engine head split `4`; exact radius strings `3.14`, `2.27`, `1.70`.
- Closed cover: `4*48=192` base arcs; primary `N=160`, arithmetic/failure comparison `N=128`.
- Immutable R2 receipt required sha256 `7eed214ec19da696e9a7d1c81ce255f2775e5662ddb8a0de3864b75aa1464f19`; consumed unchanged: `True`.
- Immutable TB V2 receipt required sha256 `73b506f8ee26b1ba9e22eac2e5badc80395bafee15ec687e620201ec6156d63d`; consumed unchanged: `True`.
- R2_receipt: `/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/R2_FLAGSHIP_ENVELOPE_RECEIPT.json` — sha256 `7eed214ec19da696e9a7d1c81ce255f2775e5662ddb8a0de3864b75aa1464f19`.
- TB_V2_receipt: `/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_BLOCK_CERTIFICATES_V2_RECEIPT.json` — sha256 `73b506f8ee26b1ba9e22eac2e5badc80395bafee15ec687e620201ec6156d63d`.
- attempt1_report: `/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/R2R3_FLAGSHIP_CERT.md` — sha256 `0e2025208eaa90290624fe1d63684c2a98b875bb5dbe195412705e1855792734`.
- R1_restatement: `/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_R1_HILBERT_RESTATEMENT.md` — sha256 `06e5d85a8e34ef6317848179ee2007f62c9c65a57d6cd44750fb33e545a910fb`.
- engine: `/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/zeta_cert_rosen_q5.py` — sha256 `c84c5c3f6d9f7a320bca7f1dbfd96a4859c3eea9b3de5420eb4eb223ad0d597b`.
- R2_code: `/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/tb_certify/certify_r2_flagship.py` — sha256 `942e9f27208bcb6e1d189958f04776d874e6b3d7371432129e778bbe4b95e3c2`.
- R3b_orchestrator: `/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/tc_rerun/certify_r3b_flagship.py` — sha256 `5b1bb0851fbb143651471fcf7737738a84a45e126b9971a94905c74357831945`.
- R3b_derivative: `/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/tc_rerun/r3b_engine.py` — sha256 `579ede0d7a9b59ed92305a845263008e89d1559136a07fe3a366326c079cb8eb`.
- R3b_endpoint: `/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/tb_certify/r3b_endpoint.py` — sha256 `6f070195b236c9509e2649a05334d5bd89c05a7e4a86e3ef751119538c797acd`.
- R2 B_total (comparison only): `[97.766647533940862488034539727239144622929442098407973478756854067071818779107064143190288 +/- 2.21e-88]` from `/B_total_full_operator_column_sum_upper_bound`.
- R2 T_tail(128): `[5.2715959382383759312384105894015797403897402970069566684001761767759085257458135387374085e-17 +/- 2.29e-106]`; T_tail(160): `[6.2678578810114395914973253606275271917615058801880325124593283869336444761682872844214265e-22 +/- 5.16e-112]` from immutable `/tail_bounds`.
- Enlarged-contour cover: `512` closed Acb arcs per block.
- Per-block enlarged radius: original R plus one quarter of the certified minimum pole/cut clearance; `eta=R/R_enlarged<1`.
- Enlarged-contour U bounds: direct single-branch sup, or Hurwitz-closed Phi0 plus the R2 center-split `A q^k + C k rho^(k-1)`.
- M' central-difference sanity at arc 0, N=6: matrix agreement `15` digits; Jacobi determinant derivative agreement `15` digits (step `1e-8`).

## 2. Closed-arc exclusions and winding

### N=160

- Complete closed cover: `True`; accepted subarcs `284`; adaptive splits `92`.
- Every finite Taylor enclosure excludes 0: `True`.
- Every F-inflated closed-arc enclosure excludes 0: `True`.
- Certified finite-cover argument winding: `1`; winding ball `[0.999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999997639714 +/- 7.81e-114]`.
- Full determinant winding by the nonvanishing straight-line homotopy inside the F-inflated tubes: `1`.
- Minimum finite Taylor |det| lower bound: `[1.81411771093769618591878911450347789310882331426232723057386098116703242371151805755028478608260290371355601398838911631e-6 +/- 1.03e-124]`.
- Minimum certified `finite lower - F` margin: `[3.43786497928918500410424272442873672667672716818717159714497929272533329959250132138262975715142405488627774949297323299e-8 +/- 2.99e-126]`.
- Maximum Taylor radius `rG`: `[2.31264467211389842236278617603337669254421662598028729059401876980667435357081184272506285690041641859958857733519753257e-6 +/- 1.91e-124]`; maximum self-consistency factor `rH`: `[0.359130125701344396310203295957410141466820794259179330694964712875195263480699772825984206877484749400904419202031712689 +/- 2.54e-119]`.
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

### N=160

- Computed-row column 2-norm sum: `[17.2911875616472160516359524117351864306884228759682933601969499127189829662276625368888095617603581209346500946555632087 +/- 2.32e-119]`.
- Sum of enlarged-disc output-tail corrections: `[9.236403414770353720638991585252596946231109530521855429913652514614326688470644687251854532759333920e-6 +/- 2.15e-106]`.
- Retained full-column sum B_ret: `[17.2911967980506308219896730507267716832853691070778238820523798263714975805543510075334968136148908802685716946355545390 +/- 3.31e-119]`.
- Immutable input tail T_tail: `[6.26785788101143959149732536062752719176150588018803251245932838693364447616828728442142650516000001900340942749146966478e-22 +/- 4.99e-142]`.
- Same valid bound for both endpoints `||L||_1, ||LP_N||_1`: `[17.2911967980506308219902998365148728272445188396138866347715559769595163838055969403721901780625077089970138372860710669 +/- 4.15e-119]`.
- `F_R=T_tail*exp(1+2*B_same)`: `[1.77973906114480433587774668725919052584205604258045551460241118823977909071559304433645848851108866316469323649345933406e-6 +/- 3.88e-126]`.
### N=128

- Computed-row column 2-norm sum: `[17.2911875598726118334559822388780288399006239123755235303401871612729417947367106329277001120496281575720328742524200999 +/- 3.13e-120]`.
- Sum of enlarged-disc output-tail corrections: `[0.0003157157412641198568596129969352809056099282924032349748618699659414849666729958960212142442586606743 +/- 2.16e-104]`.
- Retained full-column sum B_ret: `[17.2915032756138759533128418518749641208062338406679267653150490312388832797033836288237213262938868182464310563378744270 +/- 1.62e-119]`.
- Immutable input tail T_tail: `[5.27159593823837593123841058940157974038974029700695666840017617677590852574581353873740852290000009396898238084174250846e-17 +/- 1.40e-137]`.
- Same valid bound for both endpoints `||L||_1, ||LP_N||_1`: `[17.2915032756138760060288012342587234331903397346837241692124520013084499637051453965828065837520222056205162853378758539 +/- 4.11e-119]`.
- `F_R=T_tail*exp(1+2*B_same)`: `[0.149777131707267557357831600851950909909810980857721575429099342486583464139792768943375252968823401385029725246888668194 +/- 3.97e-122]`.

## 4. Failed inequalities and numeric margins

- N=128, arc `0`: F-inflated Taylor enclosure contains zero; finite lower - F = `[-0.149773363532907647413562239245610795410732810677252644077355356355544274899713254774769274738253149057343067452781120601 +/- 1.11e-121]`, finite Taylor lower = `[3.76817435990994426936160634011449907817018046893135174398613103918924007951416860597823057025232768665779410755937649700e-6 +/- 4.99e-126]`, F = `[0.149777131707267557357831600851950909909810980857721575429099342486583464139792768943375252968823401385029725246888674539 +/- 1.86e-121]`, rH = `[0.193700183051675387243316455084266139708035823040797180587955085547384486908874537560749304394584759128284523221106763680 +/- 3.93e-121]`.

## Mathematical validity and scope

For a closed straight subarc A with midpoint s0 and radius r, Acb inversion of `A(s)=I-M(s)` over the whole subarc certifies `H >= sup |tr(A(s)^(-1) M'(s))|`. Jacobi gives `|d'(s)| <= H |d(s)|`. If `D=sup_A |d'|`, the segment mean-value integral gives `sup_A |d| <= |d(s0)|+rD`, hence `D <= H(|d(s0)|+rD)`. The certified inequality `rH<1` therefore yields `D <= G := H|d(s0)|/(1-rH)`, and `d(s0)+ball(0,rG)` contains `det(I-M(s))` for every s in the closed subarc.

For each retained column, Cauchy's coefficient estimate on the certified enlarged output disc gives `|a_m| <= U eta^m`; summing `m>=N` gives `U eta^N/(1-eta)`, which dominates the omitted-output H2 norm. Adding this to the computed-row 2-norm gives a full retained-column bound. Adding immutable R2 `T_tail(N)` bounds `||L||_1`; the same sum also bounds `||LP_N||_1`.

The finite Taylor cover supplies the certified argument increments. Because every F-inflated tube excludes 0, the straight-line perturbation from the finite determinant to the Fredholm determinant stays nonzero on the boundary, so winding is preserved.

Scope: this is the R2/R3 closed-contour computation. MMS sector/factorization and the separate closed `det(1-K_s) != 0` identification remain outside this verdict, as in the mandatory attempt-1 report.


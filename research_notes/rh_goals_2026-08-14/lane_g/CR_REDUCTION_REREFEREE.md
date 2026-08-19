# Cold re-referee report: repaired RATE-A constant reduction

Date: 2026-08-19
Candidate: repaired CR_REDUCTION_SOL.md at df192e517ae0f7f6a92716c1bed8aaec1ef4ffa7
Combined candidate: 33fe3d652cb957c08e0c07cfe77c2c997a4a526d
Prior referee: CR_REDUCTION_REFEREE.md at the combined candidate
Scope: candidate, prior referee, and cited immutable local sources only.
Interpreter: /Users/za/.venvs/farey-rh/bin/python, Python 3.13.13, python-flint 0.9.0.
Write scope: this file only.

## Summary

Section 8 closes the prior referee's exact ranked-autopsy gap. Its verbatim Arb
replay matches every displayed ratio, logarithmic/e-fold reduction,
counterfactual F and S diagnostic, and wrap fraction. An independent 120-digit
assembly confirms that the only banked reduction is C4: 2^100 -> 2^62+1; the
pair term dominates, while the retained wrap is 1.0401603...e-21 of the
assembled primary bound. The appended section does not alter earlier claims:
the repaired-solution diff is 83 insertions at the end of the prior note. The
reduced primary and fallback constants are confirmed as paper-level conditional
arithmetic/component results. A0 remains a selected conditional transport
cutoff. Machine formalization, a certified full-operator enclosure, finite
base block, standalone N1-RATE, and full all-gates q0 remain open or
conjectural.

## changed_paths

- research_notes/rh_goals_2026-08-14/lane_g/CR_REDUCTION_REREFEREE.md — this report only.
- REFEREE_BRIEF.md — pre-existing untracked lane contract; read only and untouched.

No source note, map, task file, prior note, or git state was edited.

## Phase 0 and live environment

The complete 36-line REFEREE_BRIEF.md was read before any task action. I found
no disagreement with its scope, evidence gate, proof/status boundary, or report
shape. The named files are under
research_notes/rh_goals_2026-08-14/lane_g/, as required by the brief. Initial
status was only ?? REFEREE_BRIEF.md. start.md, ./te doctor,
token-economy.yaml, and worktree instructions were checked. ./te doctor passed
(ok: true, runtime_syntax_ok: true).

Command:

~~~bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
import sys, flint
print('python=',sys.version.split()[0])
print('flint_version=',getattr(flint,'__version__','<no __version__>'))
print('flint_path=',flint.__file__)
from flint import arb, acb, ctx
ctx.dps=80
print('arb_api=',arb(1))
print('acb_zeta_zero_api=',acb.zeta_zero(1))
PY
~~~

Output:

~~~text
python= 3.13.13
flint_version= 0.9.0
flint_path= /Users/za/.venvs/farey-rh/lib/python3.13/site-packages/flint/__init__.py
arb_api= 1.0000000000000000000000000000000000000000000000000000000000000000000000000000000
acb_zeta_zero_api= 0.50000000000000000000000000000000000000000000000000000000000000000000000000000000 + [14.134725141734693790457251983562470270784257115699243175685567460149963429809257 +/- 2.59e-79]j
~~~

## Commit and immutable-source receipt

Commands:

~~~bash
git rev-parse 33fe3d6^{commit}
git show -s --format='commit=%H%nparent=%P%nsubject=%s' 33fe3d6
git rev-parse df192e5^{commit}
git show -s --format='commit=%H%nparent=%P%nsubject=%s' df192e5
shasum -a 256 \
  research_notes/rh_goals_2026-08-14/lane_g/CR_REDUCTION_SOL.md \
  research_notes/rh_goals_2026-08-14/lane_g/CR_REDUCTION_REFEREE.md \
  research_notes/rh_goals_2026-08-14/lane_g/BOUNDARY_ALPHA_THEOREM_SOL.md \
  research_notes/rh_goals_2026-08-14/lane_g/ATOM_MOMENT_BRIDGE_SOL.md \
  research_notes/rh_goals_2026-08-14/lane_g/AM_REFEREE.md \
  research_notes/rh_goals_2026-08-14/lane_g/RATE_A_REFEREE.md \
  research_notes/rh_goals_2026-08-14/lane_g/FW_RENEWAL_COUNT_SOL.md \
  research_notes/rh_goals_2026-08-14/lane_g/KF_WALL_ATTACK_SOL.md \
  research_notes/rh_goals_2026-08-14/lane_g/KF_WALL_REFEREE.md
~~~

Output:

~~~text
33fe3d652cb957c08c0e07cfe77c2c997a4a526d
commit=33fe3d652cb957c08c0e07cfe77c2c997a4a526d
parent=df192e517ae0f7f6a92716c1bed8aaec1ef4ffa7
subject=(RATE-A) referee confirms reduced constant arithmetic with autopsy gap
df192e517ae0f7f6a92716c1bed8aaec1ef4ffa7
commit=df192e517ae0f7f6a92716c1bed8aaec1ef4ffa7
parent=d8b7a44bcdcd69e2d5761d454132d5d84a7803e7
subject=(RATE-A) add ranked reduced-constant loss autopsy
89fc61e9bc33db55c95856f5412e87c45da72d3623616435575fb494321b3417  research_notes/rh_goals_2026-08-14/lane_g/CR_REDUCTION_SOL.md
f0f71f09c1c4547805c44f4c649c12a26568fa0f2e8843a90d574ea856dcfa5a  research_notes/rh_goals_2026-08-14/lane_g/CR_REDUCTION_REFEREE.md
58441b334a5f279aae6298e3b5383ef5677b3e6ec6e7d5bc6a908a4936111e6e  research_notes/rh_goals_2026-08-14/lane_g/BOUNDARY_ALPHA_THEOREM_SOL.md
59ce32f7c6fa86580055d9049e609a2189ecc1645528dd4136758fcf547fbbbb  research_notes/rh_goals_2026-08-14/lane_g/ATOM_MOMENT_BRIDGE_SOL.md
3d655f2c05395688be73e8786cd9a954182cc4842005ff9e7662d05cccf503b4  research_notes/rh_goals_2026-08-14/lane_g/AM_REFEREE.md
b835804104f502f54cc757336ba8fe54a82a05eaa18261a4d78f697aba358590  research_notes/rh_goals_2026-08-14/lane_g/RATE_A_REFEREE.md
70cf0a9d12cdc6938c431bd1246b0ca18d929c151fb98399a8e94a75d7f6fd3c  research_notes/rh_goals_2026-08-14/lane_g/FW_RENEWAL_COUNT_SOL.md
efa518c9908e3c68005c3b7349bdee6c4af63dc7146ef85b13882560c2644aad  research_notes/rh_goals_2026-08-14/lane_g/KF_WALL_ATTACK_SOL.md
73c6eb59b25038f9e23ae38fa8c409af65d50fd0219b45417022663486361710  research_notes/rh_goals_2026-08-14/lane_g/KF_WALL_REFEREE.md
~~~

The prior referee's exact open item is at CR_REDUCTION_REFEREE.md:111: the
candidate had not ranked the orders-of-magnitude loss by separating the C4
drop, retained wrap, and A0 exponentiation. The candidate repair is
append-only:

~~~bash
git diff --stat d8b7a44bcdcd69e2d5761d454132d5d84a7803e7 \
  df192e517ae0f7f6a92716c1bed8aaec1ef4ffa7 -- \
  research_notes/rh_goals_2026-08-14/lane_g/CR_REDUCTION_SOL.md
git diff --numstat d8b7a44bcdcd69e2d5761d454132d5d84a7803e7 \
  df192e517ae0f7f6a92716c1bed8aaec1ef4ffa7 -- \
  research_notes/rh_goals_2026-08-14/lane_g/CR_REDUCTION_SOL.md
~~~

Output:

~~~text
.../CR_REDUCTION_SOL.md | 83 ++++++++++++++++++++++
1 file changed, 83 insertions(+)
83  0  research_notes/rh_goals_2026-08-14/lane_g/CR_REDUCTION_SOL.md
~~~

The diff starts at the former final line and adds only Section 8. No earlier
constant, hierarchy, theorem scope, or status claim was silently rewritten.

## Exact Section 8 replay

Command replayed verbatim from CR_REDUCTION_SOL.md:515-540:

~~~bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import arb, acb, ctx
ctx.dps=80
alpha=arb(6)/5
pub=arb(10489412368759562746433608215977724802)
primary=arb(38160259896392973127946053)
qpub=arb(332093267419812025416641789732742045430624465595)
qprimary=arb(97418971860452658435229799565334786148)
ratio=pub/primary
print('C4_ratio_2^100_over_2^62_plus_1=',arb(2)**100/(arb(2)**62+1))
print('CR_ratio_pub_over_primary=',ratio)
print('CR_log_gain=',ratio.log())
print('CR_decimal_orders_gain=',ratio.log()/arb(10).log())
print('predicted_A0_log_q_gain_5_over_6=',ratio.log()/alpha)
print('actual_transport_integer_ratio=',qpub/qprimary)
F12=arb(7940); Finf=arb(1225)/4
print('retained_F12_over_F_infinity=',F12/Finf)
print('counterfactual_F_log_q_headroom=',(F12/Finf).log()/alpha)
S=arb('7.648'); t0=(acb.zeta_zero(1)/2).imag
Strue=(arb('1.1')**2+(t0+arb('.5'))**2).sqrt()
print('retained_Splus1_over_exact_first_zero_Splus1=',(S+1)/(Strue+1))
p=arb(11)/5; pair_pref=2*arb.pi()**2*(S+1)*p
wrap=p*128*(1+arb(2).log())*30
inside=pair_pref*(arb(2)**62+1)*F12+wrap
print('retained_wrap_fraction_primary_raw=',wrap/inside)
PY
~~~

Output (all lines match the candidate's Section 8 receipt):

~~~text
C4_ratio_2^100_over_2^62_plus_1= [274877906943.99999994039535522460937501292469707114105741706316388494353544572607 +/- 1.41e-69]
CR_ratio_pub_over_primary= [274877906943.99999994010943445842741471236781422942372676070069066732083830942528 +/- 2.41e-69]
CR_log_gain= [26.339592861277921757636940007225731303574249568797996488951897847403771279336238 +/- 4.46e-79]
CR_decimal_orders_gain= [11.439139835231285418027453653682274464098627516442177144935850736695230219344481 +/- 2.31e-79]
predicted_A0_log_q_gain_5_over_6= [21.949660717731601464697450006021442752978541307331663740793248206169809399446865 +/- 4.44e-79]
actual_transport_integer_ratio= [3408917801.9197065874125291505009477738856775886079565124869054118074214408356601 +/- 1.63e-71]
retained_F12_over_F_infinity= [25.926530612244897959183673469387755102040816326530612244897959183673469387755102 +/- 7.23e-80]
counterfactual_F_log_q_headroom= [2.7127223269852038882840797465808487141537645626118542167461593807005333006743130 +/- 5.75e-80]
retained_Splus1_over_exact_first_zero_Splus1= [1.0001279946880542040326816790184759533388408736293087248331550148855713052518603 +/- 8.51e-81]
retained_wrap_fraction_primary_raw= [1.0401603157596627398211006085231419011537089926537046290030360458673782087083230e-21 +/- 6.97e-101]
~~~

## Independent arithmetic and interpretation checks

A separate 120-digit scalar check, not importing candidate receipt code,
recomputed the primary pair, wrap, full M0 assembly, C4/CR ratio difference,
the exponential of the A0 log gain, the integer transport ratio, F(12)/F∞,
and exact elementary coefficient values.

Command:

~~~bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import arb, ctx
ctx.dps=120
alpha=arb(6)/5
pub=arb(10489412368759562746433608215977724802)
primary=arb(38160259896392973127946053)
qpub=arb(332093267419812025416641789732742045430624465595)
qprimary=arb(97418971860452658435229799565334786148)
F12=arb(7940); Finf=arb(1225)/4
S=arb('7.648'); p=arb(11)/5; M0=arb('2.775')
pair_pref=2*arb.pi()**2*(S+1)*p
wrap=p*128*(1+arb(2).log())*30
pair=pair_pref*(arb(2)**62+1)*F12
inside=pair+wrap; raw=M0*inside
ratio=pub/primary; pred=ratio.log()/alpha
print('pair_upper=',pair.upper())
print('wrap_upper=',wrap.upper())
print('pair_plus_wrap_upper=',inside.upper())
print('M0_raw_upper=',raw.upper())
print('wrap_fraction_of_pair_plus_wrap=',(wrap/inside).upper())
print('wrap_fraction_of_M0_raw=',(M0*wrap/raw).upper())
print('pair_fraction_of_inside=',(pair/inside).upper())
print('CR_ratio_minus_C4_ratio=',(pub/primary-(arb(2)**100/(arb(2)**62+1))).upper())
print('exp_predicted_log_gain=',pred.exp())
print('actual_integer_transport_ratio=',(qpub/qprimary).upper())
print('actual_over_predicted=',(qpub/qprimary/pred.exp()).upper())
print('F12=',F12,'Finf=',Finf,'exact_F_ratio=',F12/Finf)
print('F12_identity=',arb(1225)/4+arb(91605)/12)
print('C4_primary=',arb(2)**62+1,'C4_fallback=',arb(2)**63)
PY
~~~

Output lines:

~~~text
pair_upper= [13751445007709179505551841.3339578611169088508026670806267626131492814778535196867948216088756856777143323628194345882136 +/- 2.19e-95]
wrap_upper= [14303.7073813704179739567769620786756471018251350754363868115047202001893183999809574383333864657450723548285116617811531 +/- 1.60e-116]
pair_plus_wrap_upper= [13751445007709179505566145.0413392315348828075796291593024097149744165532899064982995418090650040776952898011528210539587 +/- 4.77e-95]
M0_raw_upper= [38160259896392973127946052.4897163675092997910334709170641869590540059353794905327812285201553863156044291981990784247353 +/- 3.76e-95]
wrap_fraction_of_pair_plus_wrap= [1.04016031575966273982110060852314190115370899265370462900303604586737820870832304398368357414738935185773046259950976129e-21 +/- 2.31e-141]
wrap_fraction_of_M0_raw= [1.04016031575966273982110060852314190115370899265370462900303604586737820870832304398368357414738935185773046259950976129e-21 +/- 1.98e-141]
pair_fraction_of_inside= [0.999999999999999999998959839684240337260178899391476858098846291007346295370996963954132621791291676956016316425852610650 +/- 4.18e-121]
CR_ratio_minus_C4_ratio= [-2.85920766181960300556882841717330656362473217622697136300788997462525959798982381646828536688913913865905381634936825553e-10 +/- 2.97e-130]
exp_predicted_log_gain= [3408917801.9197065874125291505009477739006295333460774972593738825454483729241620790217432700401445877642551601949268496 +/- 6.52e-110]
actual_integer_transport_ratio= [3408917801.91970658741252915050094777388567758860795651248690541180742144083566011588997064093645074303875345661870636663 +/- 4.69e-111]
actual_over_predicted= [0.999999999999999999999999999999999999995613873490965106633005505182376899847042633940757127214316659586475793617207064746 +/- 9.77e-122]
F12= 7940.00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 Finf= 306.250000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 exact_F_ratio= [25.9265306122448979591836734693877551020408163265306122448979591836734693877551020408163265306122448979591836734693877551 +/- 4.27e-120]
F12_identity= 7940.00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
C4_primary= 4611686018427387905.00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 C4_fallback= 9223372036854775808.00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
~~~

The wrap_fraction_of_M0_raw line confirms the denominator interpretation:
external positive M0 multiplies both pair and wrap, so the factor cancels. A
different prior-reporter wrap/raw diagnostic divided the unmultiplied wrap by
an M0-multiplied denominator and is not the fraction of the assembled wrap
contribution.

## Gap-closure and ranked-ordering ledger

| Criterion | Result | Evidence and scope |
|---|---|---|
| Exact prior gap identified | PASS | Prior report :111 names the missing ranked log-ratio/autopsy for C4, wrap, and A0 exponentiation. |
| C4 is the only banked reduction | PASS | Candidate :423-435 retains S=7.648, M0=2.775, F(12)=7940 and says “only replace” C4; :431 says no domain/exponent/activation/wrap/contour/transport hypothesis changes. |
| Dominant C4 loss | PASS | Replay: C4 ratio 274877906943.999...; CR ratio 274877906943.999...; decimal gain 11.439139835...; independent CR_ratio_minus_C4_ratio is only -2.8592e-10. |
| A0 log/e-fold interpretation | PASS | Replay: CR_log_gain 26.339592861..., predicted A0 log gain 21.949660717..., integer transport ratio 3408917801.919...; independent exp and actual_over_predicted=0.999.... |
| F diagnostic/counterfactual only | PASS | Replay: F12/F∞ 25.926530612..., counterfactual F log headroom 2.712722326...; candidate :565-570 labels it diagnostic and rejects a banked q-dependent replacement. |
| S diagnostic/counterfactual only | PASS | Replay: retained S+1 ratio 1.000127994...; candidate :450-456 says no tighter rational contour ceiling is combined. |
| Wrap negligible at stated scale | PASS | Replay and independent check: wrap fraction 1.040160315...e-21; pair fraction 0.999999999999999999998959.... |
| No speculative M0 gain | PASS | Candidate :458-465 says M0, C1, and wrap refinements are not claimed; Section 8 item 5 (:577-579) leaves M0 unranked for lack of a proved alternative. |
| Primary/fallback arithmetic unchanged and strict | PASS | Candidate Section 4 and independent prior receipt retain CR'=38160259896392973127946053 and CR^63=76320519792785946239303038; direct bridge source gives 2^62+1 at ATOM_MOMENT_BRIDGE_SOL.md:483-489; F(12)=7940 is exact at BOUNDARY_ALPHA_THEOREM_SOL.md:529-540. |
| Earlier claims not silently changed | PASS | Candidate repair diff is exactly 83 appended lines; no pre-Section-8 lines changed. |

## Source-grounded status limits

The paper-level reduction is a conditional component result only. The source
boundary assembly is positive and linear in C4
(BOUNDARY_ALPHA_THEOREM_SOL.md:510-525), and the wrap source gives the
independent C4-free term (FW_RENEWAL_COUNT_SOL.md:475-498). Those facts support
the substitution but do not upgrade its premises.

Binding caveats:

- N1-RATE remains CONJECTURAL and bypassed, not a standalone theorem
  (BOUNDARY_ALPHA_THEOREM_SOL.md:279-283,681); no N1 claim entered the
  reduction.
- The A0 integer is a conditional transport cutoff under the selected strict
  envelope; it assumes the full-side RATE and holomorphy/no-pole hypotheses
  (KF_WALL_ATTACK_SOL.md:160-201,178-201).
- Machine RATE-A certification and a certified full-operator enclosure remain
  open; the RATE referee records omitted dimension tails and midpoint
  extraction (RATE_A_REFEREE.md:18-25,266-306).
- The final all-gates onset remains a maximum over RATE, transport, divisor,
  geometry, monotonicity, and other gates, not q_transport alone
  (BOUNDARY_ALPHA_THEOREM_SOL.md:663-671,686-687).
- The direct atom bridge and Ford/two-mark inputs remain paper-level premises;
  no finite base block, full-program q0, or theorem-ledger promotion is
  inferred here.

## Attempts

- Read the complete brief and verified named paths, interpreter, arb, and
  acb.zeta_zero APIs before planning; no disagreement found.
- Replayed the exact Section 8 command at 80-digit Arb precision; every
  embedded output line matched.
- Wrote and ran an independent 120-digit Arb assembly; all pair, wrap,
  ratio, log/e-fold, F, coefficient, and cancellation checks passed.
- Rehashed the repaired solution, prior referee, and cited immutable sources;
  all paths were present and stable during this lane.
- Checked the repaired-solution commit diff; it is append-only at Section 8.
- Searched focused status lines for N1-RATE, machine/full-operator limits, A0
  conditionality, full-program onset, and the candidate's banked versus
  diagnostic labels; all required caveats remain visible.
- A full finite determinant/operator rerun was considered and not executed:
  it would be out of scope and, per RATE_A_REFEREE.md:266-306, would not certify
  the omitted dimension tail.

## Assumptions

- The cited Route-B/Ford/two-mark, wrap, beta-integral, and A0 premises are
  accepted exactly at the hashed local revisions; no stronger status is
  inferred.
- 7.648, 2.775, .1552, and .0439 are safe declared endpoints, not midpoint
  estimates.
- Arb upper endpoints control displayed ratios and assembly ceilings; exact
  integer quotients are used only where explicitly stated.
- The Section 8 S comparison is diagnostic geometry only; it is not a new
  contour theorem or banked constant.
- The transport integer ratio is an e-fold consequence of the selected A0
  envelope and is not a full-program onset ratio.

## Leftovers / concerns

1. The repaired ranked-autopsy documentation is closed, but the result remains
   paper-level conditional arithmetic, not machine/full-operator certification.
2. q_RATE=12 is the analytic tail onset after fixed F(12) absorption; the A0
   integer is a conditional transport cutoff, not a final q0.
3. The wrap fraction is negligible only for the retained primary assembly; no
   new wrap proof or smaller M0 is claimed.
4. Standalone N1-RATE, finite base-block certification, divisor/holomorphy,
   geometry/monotonicity, and full-program activation remain open or
   conjectural as stated above.

## Final mechanical checks

Commands:

~~~bash
git diff --check
awk '/[[:blank:]]$/{print NR ": trailing whitespace"; bad=1} END{if (bad) exit 1}' \
  research_notes/rh_goals_2026-08-14/lane_g/CR_REDUCTION_REREFEREE.md
git status --short
~~~

Output:

~~~text
?? REFEREE_BRIEF.md
?? research_notes/rh_goals_2026-08-14/lane_g/CR_REDUCTION_REREFEREE.md
~~~

git diff --check and the trailing-whitespace check emitted no diagnostics and
exited zero. The status whitelist contains exactly the pre-existing brief and
this assigned report.

## Final verdict

CONFIRMED for the repaired candidate's exact prior gap: Section 8 closes the
missing ranked-autopsy/documentation item. C4'=2^62+1 and
CR'=38160259896392973127946053 are confirmed as paper-level conditional
arithmetic/component results; C4=2^63 and
CR^63=76320519792785946239303038 remain a weaker confirmed fallback. The
published C4=2^100 and published CR are unchanged. The theorem-level status is
still GAPS outside that arithmetic/component scope for the machine/full-
operator, finite-base, conditional A0, standalone N1-RATE, and
full-program/all-gates claims listed above. No numeric refutation was found.

STATUS: COMPLETE_WITH_CONCERNS (paper-level conditional; machine/full-operator, finite-base, standalone N1-RATE, and full/all-gates closure remain open)
READY FOR JUDGING

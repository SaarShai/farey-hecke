# LAW symmetric Route-B tail: the scalar reflection obstruction

Date: 2026-08-19

Lane: Route B, symmetric-tail attack

Status: CANDIDATE REFUTATION — AWAITING COLD REFEREE; no LAW closure.

## 0. Executive verdict

The proposed strengthening

    use the global negation of the LAW and
    phi_q(s) overline(phi_q(1-s-bar)) = 1 to put an O(E_R(q)) bound on
    F_q = phi_q - phi_infty on both vertical sides of a symmetric rectangle

fails for the scalar target phi_infty used by the existing RATE notes. The
reason is structural, not a missing Harnack constant: the displayed
phi_infty is the (infinity,infinity) entry of the two-cusp theta scattering
matrix, not a scalar unitary scattering determinant. Its reflected entry is
not the reciprocal of its right entry.

Grant the strongest contradiction hypothesis (global absence of every
off-line zero/pole needed to make the finite scattering coefficient
holomorphic and nonzero), the candidate right-boundary endpoint estimate, and
the right-side lower bound. At

    s_R = 3/2 + i t_0,       s_L = 1 - overline(s_R) = -1/2 + i t_0,

the exact theta formula gives

    D_theta := |1/overline(phi_infty(s_R)) - phi_infty(s_L)|
        > 15.4230148900416.

The finite functional equation gives the reflected finite value
phi_q(s_L) = 1/overline(phi_q(s_R)). Therefore, if
E_R(q) >= |F_q(s_R)| and |phi_q(s_R)| is bounded below,

    |F_q(s_L)| >= D_theta
        - E_R(q)/( |phi_infty(s_R)| |phi_q(s_R)| ).

The right endpoint candidate has E_R(q) tending to zero, so this lower bound
tends to the nonzero constant D_theta. No q-uniform constant C can satisfy
sup_{Gamma_L}|F_q| <= C E_R(q) on that tail. The claimed symmetric transport
is therefore false as a statement about this F_q, even under its strongest
global contradiction assumptions.

This note does not refute the LAW. It refutes only the proposed scalar
two-sided F_q-transport. Every prospective Harnack, horizontal-side, or
matrix-channel repair below is CONJECTURAL unless explicitly stated as an
algebraic identity or an outward Arb enclosure. A separate cold referee file
is required before any proof-status upgrade.

## 1. Inputs and status ledger

The existing Route-B source note records the target function and its status:

    $ sed -n '64,76p' research_notes/rh_goals_2026-08-14/lane_g/R3_ROUTE_B_TRANSPORT_SOL.md
    The theta entry is the printed Ch. 11, (3.1), ((infinity,infinity))-entry

    phi_infty(s) =
      sqrt(pi) Gamma(s-1/2) zeta(2s-1) /
      (Gamma(s) zeta(2s) (4^s-1)).

    It is one entry of a two-cusp scattering matrix. It is not a scalar unitary
    scattering determinant.

The theta-channel derivation in LAW_ANCHOR_T1_THETA.md writes the same matrix
as

    A(s) = phi_infty(s) = g(s)/(4^s-1),
    B(s) = g(s)(2^s-2^(1-s))/(4^s-1).

It records the full matrix equation Phi_theta(s) Phi_theta(1-s) = I, not a
scalar equation for A:

    $ sed -n '205,235p' research_notes/rh_goals_2026-08-14/lane_g/LAW_ANCHOR_T1_THETA.md
    Hence, by M1F's Euler-product restriction lemma with p = 2,
       phi_{oo,oo}(s) = g(s) / (4^s - 1). (3.1)
    ...
       phi_{oo,1}(s) = g(s) (2^s - 2^(1-s))/(4^s - 1). (3.3)
    ...
    By (1.3) Phi_theta is the Gamma_0(2) scattering matrix with the two
    cusps relabelled.

The right endpoint source is explicitly conditional and not a LAW theorem:

    $ sed -n '1,36p' research_notes/rh_goals_2026-08-14/lane_g/LAW_EFFECTIVE_TAIL_COVER_SOL.md
    # LAW Route-B effective tail / covering: endpoint p=3 candidate
    Status: CONDITIONAL CANDIDATE — AWAITING COLD REFEREE; not an
    unconditional proof of the LAW.
    ...
    q_endpoint = 31951437654668744792.

Accordingly, the right-boundary estimate used below is CONJECTURAL upstream
input until its endpoint cold referee and all stated atom/Ford/transport
interfaces are banked. The obstruction itself is an exact functional-equation
calculation conditional only on those inputs.

For the contradiction branch, write H_global(q) for the strong hypothesis
that the global negation of the LAW has removed every off-line scattering
zero/pole relevant to the symmetric domain and its reflection, so that phi_q
is holomorphic and nonzero there. This is stronger than the local H_0 used in
the existing transport note. Granting H_global(q) can only help the proposed
route; the obstruction below survives it.

## 2. Exact theta-channel mismatch

Set r(s) = 2^s - 2^(1-s). The theta matrix has the symmetric form

    Phi_theta(s) = [[A(s), B(s)], [B(s), A(s)]],     B(s) = r(s) A(s).

Its printed matrix functional equation implies

    A(s) A(1-s) + B(s) B(1-s) = 1.

Since r(1-s) = -r(s), this simplifies to the exact identity

    A(s) A(1-s) = 1/(1-r(s)^2).                         (2.1)

The coefficients are real under conjugation. For s_L = 1-overline(s_R),

    phi_infty(s_R) overline(phi_infty(s_L))
        = 1/(1-r(s_R)^2).                               (2.2)

The right-hand side is not 1 at the target point. The scalar finite-group
identity and the theta-entry identity are therefore different identities:

    phi_q(s_R) overline(phi_q(s_L)) = 1,
    phi_infty(s_R) overline(phi_infty(s_L))
        = 1/(1-r(s_R)^2) != 1.

This is the exact reason the informal substitution

    F_q(s_L) ?= 1/overline(phi_q(s_R))
                 - 1/overline(phi_infty(s_R))

is invalid: the second term is not phi_infty(s_L).

## 3. Reflection lemma and the no-go consequence

Let b = phi_infty(s_R), ell = phi_infty(s_L), and a_q = phi_q(s_R).
Suppose E_R(q) >= |a_q-b| and E_R(q) < |b|. Under the finite scattering
functional equation,

    F_q(s_L) = 1/overline(a_q) - ell,
    D_q = 1/overline(a_q) - 1/overline(b),
    D_theta = 1/overline(b) - ell.

The reverse triangle inequality and |a_q| >= |b|-E_R(q) give

    |D_q| <= E_R(q)/( |a_q| |b| )
          <= E_R(q)/( |b| (|b|-E_R(q)) ),

and hence

    |F_q(s_L)| >= |D_theta|
       - E_R(q)/( |b| (|b|-E_R(q)) ).                    (3.1)

This bound uses the requested right-side lower bound and is stronger than a
mere failure to find one. If a candidate RATE has E_R(q) tending to zero,

    liminf_{q -> infinity} |F_q(s_L)| >= |D_theta| > 0,

whereas C E_R(q) tends to zero for every fixed C. Thus the proposed
two-sided O(E_R) estimate is algebraically impossible for
F_q = phi_q - phi_infty.

The global no-off-line-zero/pole contradiction does not change (3.1). It
justifies the finite reflection identity in the contradiction branch; it
does not turn the two-cusp entry A into a scalar unitary coefficient.

## 4. Independent outward-Arb receipt

The receipt is
research_notes/rh_goals_2026-08-14/lane_g/law_probes/symmetric_tail_obstruction.py.
It evaluates the exact formula above, the endpoint candidate at the fixed
right point, and a geometry-only symmetric harmonic measure. Run:

    $ PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python \
        research_notes/rh_goals_2026-08-14/lane_g/law_probes/symmetric_tail_obstruction.py
    t0= [7.06736257086734689522862599178123513539212855784962158784278373007498171490462838247450519658578050638960148577439871838 +/- 3.71e-120]
    phiR_abs_lower= [0.0600417546692132792080716592748026370544647185874444987221628954713324731822435481928427637856004764889395266148431493300 +/- 1.96e-122]
    phiR_abs_upper= [0.0600417546692132792080716592748026370544647185874444987221628954713324731822435481928427637856004764889395266148431494636 +/- 3.94e-122]
    theta_product_minus_1_abs_lower= [0.926024876287502534352463729814300606876059001261877898688550796426737468229028447710251160571877367553558801948537493143 +/- 3.40e-121]
    theta_product_minus_exact_abs_upper= [6.93574108465083523028029001730614181336052514086486781330759016505377827355149961624990325915542732860657684569961393055e-118 +/- 4.78e-238]
    D_theta_reflection_abs_lower= [15.4230148900416227765896480276160756324393005292756731019115240557483539271777067847767337930437122223387996262189909103 +/- 1.41e-119]
    S_vertical_upper= [9.56570225051069034617237597906392145926152602134742614580424666309555128836661007191372820220954656406610153030062701095 +/- 3.43e-120]
    q_endpoint= 31951437654668744792.000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
    E_endpoint_upper= [2.82132013514546723977834029344037679461436119352362364819548377683222245040313289922180129809846665304420829487236358278e-16 +/- 4.08e-136]
    phi_q_right_floor_lower= [0.0600417546692129970760581447280786592204353745497650372860435431089676536338658649705977234723105543088097167681778449091 +/- 4.03e-122]
    reciprocal_correction_upper= [7.826104039102542904402053155762714771581894466320972898688550410...e-14 +/- 4.24e-134]
    F_left_floor_lower= [15.4230148900415445155492570021870316119077429021279572829668608460193678942344241572740816345216134885215911487306257410 +/- 1.40e-119]
    F_left_over_E_lower= [54665951225865880.0238592854873438448426397531282863677969050731855256752416347376941878115200741410328860932660642859621 +/- 1.05e-104]
    symmetric_union_harmonic_measure_lower= [0.944067026571504309702707553893741360009407915927620458330381969033463398059186294474334565320054994756160409 +/- 1.71e-121]
    symmetric_union_harmonic_measure_upper= [0.944067026571504309702707553893741360009407915927620458330381969033463398059186294474334590410285933842392304888966060452 +/- 4.07e-122]
    symmetric_harmonic_tail_upper_right= [1.25451154695431157332274246499903290700054512773077556689756003615350062245615012265039557533901504174565205302393115537 +/- 4.92e-209]
    symmetric_harmonic_tail_upper_left= [1.70865400785922096134273720626753165948377855753970099044790373310873850410605214955188803467319637232265844067614093401 +/- 2.67e-267]

All lower claims use interval lower endpoints and all upper claims use interval
upper endpoints. The identity check is decisive: the theta product differs
from 1 by more than 0.9260, while its difference from 1/(1-r(s_R)^2) is below
7 times 10^(-118). This is not a precision or branch artifact.

At the candidate endpoint, (3.1) gives

    |F_q(s_L)| > 15.4230148900415,
    |F_q(s_L)|/E_R(q) > 5.4665951225865 times 10^16,

with the inequalities rounded in the adverse directions. The ratio is not
the asymptotic no-go by itself—the candidate constants could be enlarged—but
the nonzero D_theta and E_R(q) tending to zero are decisive.

## 5. Geometry-only symmetric harmonic measure

For comparison, take the proposed symmetric rectangle

    Omega_sym = { -1/2 < Re(s) < 3/2,
                  |Im(s)-t_0| < 2.38 }.

The seed zero has real coordinate 3/4, hence normalized horizontal coordinate
x=5/4 from the left edge; the reflected horizontal coordinate is 3/4. The
rectangle has L=2 and H=4.76. Summing the odd separated-variables series and
adding an absolute geometric tail gives

    0.9440670265715043097027075538937413
      < omega_left + omega_right
      < 0.9440670265715043097027075538937414.              (5.1)

This is a geometry-only enclosure at the seed centre. It is not a transport
result: the left boundary datum for F_q is bounded below by the nonzero
mismatch (0.1), not by E_R(q). The apparent harmonic-measure gain therefore
cannot be spent on the desired q^(-2) log(q) endpoint error.

## 6. The requested horizontal/Harnack attack

The bottom of the delta=2.38 strip remains well above t=0:

    $ PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
    from flint import acb, arb, ctx
    ctx.dps=100
    t0=(acb.zeta_zero(1)/2).imag
    d=arb('2.38')
    print('t_bottom_lower=',(t0-d).lower())
    print('t_top_upper=',(t0+d).upper())
    eps=arb('4.68')
    C6=arb(100)*(1/eps+(1+1/eps**2).sqrt())
    print('C6_eps_4.68_upper=',C6.upper())
    PY
    t_bottom_lower= [4.687362570867346895228625991781235135392128557539... +/- 2.41e-100]
    t_top_upper= [9.447362570867346895228625991781235135392128557539... +/- 4.70e-100]
    C6_eps_4.68_upper= [123.6248974799147571158881087298810863558621869397994659653859804025224940626592480636568992672347346 +/- 2.88e-98]

The printed Lemma 7.7 transcription gives

    |phi_q(s)| <= C6(epsilon),
    C6(epsilon)=100(epsilon^(-1)+sqrt(1+epsilon^(-2))),

for the finite coefficient on 1/2 <= Re(s) <= 3/2, |t| > epsilon.
Thus the right half of this rectangle has the conditional q-uniform upper
ceiling C6(4.68) < 123.625.

One could CONJECTURALLY add an outer right-half rectangle, still with
Im(s)>0, on which the global contradiction hypothesis guarantees that phi_q
is zero-free. Then

    u_q(s) = log(C6(4.68)/|phi_q(s)|)

would be positive harmonic, and a fully explicit Harnack/Poisson-chain
calculation from the anchor lower bound could give a q-uniform lower bound on
interior horizontal points. The existing ledger does not provide the needed
outer zero-free rectangle or its chain constant; promoting such a bound is
CONJECTURAL. More importantly, even a successful Harnack construction would
only establish the m_q used in (3.1). It cannot set D_theta to zero. If the
outer zero-free assumption is not granted, the Harnack step is invalid because
log|phi_q| need not be harmonic across its zeros/poles; the proposed
horizontal-side bound is then also CONJECTURAL.

This separates the two issues cleanly:

1. a possible Harnack lower-bound gate for the finite coefficient; and
2. the exact scalar theta-channel mismatch, which kills the desired
   F_q-transport even after gate 1 is granted.

### 6.1 Normalizing by zeta(2s) does not produce a holomorphic full wall

The natural attempted repair is

    G_q(s) = zeta(2s) F_q(s)
           = zeta(2s) phi_q(s) - H(s),

where

    H(s) = sqrt(pi) Gamma(s-1/2) zeta(2s-1)
           /(Gamma(s)(4^s-1)).

The zeta factor does cancel the theta-entry denominator poles at zeros of
zeta(2s), including the reflected theta pole near
s=1/4+i t_0, provided the finite coefficient is holomorphic there. It does
not cancel the independent rational divisor 4^s-1=0. In the proposed
rectangle, the point

    s_p = 2 pi i/log(2),
    Im(s_p) = 9.0647202836543876192553658914...,

lies strictly between t_0-2.38 and t_0+2.38. At this point H has residue

    sqrt(pi) Gamma(s_p-1/2) zeta(2s_p-1)
      /(Gamma(s_p) log(4)),

whose Arb absolute lower bound is greater than 2.81082314196179. The same
receipt gives positive lower bounds greater than 3.12123858834773 for
|zeta(2s_p)| and greater than 6.62904417198114 for
|zeta(2s_p-1)|. Hence the pole is not canceled by either zeta factor. Under
H_global, zeta(2s) phi_q(s) is holomorphic at s_p, so G_q itself has an
uncancelled simple pole there.

The local seed-circle normalization is legal by a separate elementary check:
the circle has center 3/4+i t_0 and radius 1/40, so
Re(2s) >= 2(3/4-1/40) = 29/20 > 1. The Euler product therefore makes
zeta(2s) holomorphic and nonzero on that circle. This local fact supports a
Rouche normalization near the seed only; it cannot remove the interior
rational pole on the full symmetric wall.

The divisor audit is therefore:

* the k=1 rational pole has height 4.53236014182719, below the strip;
* the k=2 rational pole s_p is inside the strip;
* the k=3 rational pole has height 13.59708042548158, above the strip;
* Gamma(s-1/2) and Gamma(s) have no off-real-axis poles in this height
  window;
* the zeta(2s) multiplier cancels its own denominator divisor only, not the
  rational divisor.

The added receipt output is:

    rational_pole_t_lower= [9.06472028365438761925536589143333362034372293544759116837203309588120190744261020451816775920803217930613292541555805615 +/- 2.01e-120]
    rational_pole_t_upper= [9.06472028365438761925536589143333362034372293544759116837203309588120190744261020451816775920803217930613292541555805616 +/- 2.72e-120]
    rational_pole_residue_abs_lower= [2.81082314196179094940212748157336081991834801642433121075233847113056461675758567846041276037773073573815829472590342451 +/- 4.40e-120]
    zeta_2s_at_rational_pole_abs_lower= [3.12123858834773532707119107210756979807192458201951063683293821438981965005650529115925870875508289595105123534690969752 +/- 3.85e-120]
    zeta_2sminus1_at_rational_pole_abs_lower= [6.62904417198114476945143637103056273098063058179260833997828789979366788356444873200322133375054179709336679552143601540 +/- 4.97e-120]

Thus the normalized G route is blocked twice: away from the rational pole it
still carries the nonzero reflected scalar defect D_theta, while on the full
four-side symmetric domain it is not holomorphic. A complete zeta-growth
bound on all four sides cannot turn this meromorphic G into the desired
maximum-principle object.

## 7. Corrected strongest statement

The reflection argument does yield an O(E_R) statement for a different left
target. Define

    tilde_phi_infty(s_L;s_R) = 1/overline(phi_infty(s_R)).

If m_q <= |phi_q(s_R)| and m_infty <= |phi_infty(s_R)| are positive, then

    |phi_q(s_L)-tilde_phi_infty(s_L;s_R)|
      <= E_R(q)/(m_q m_infty).                            (7.1)

This is the corrected strongest scalar reflection statement. It is not a
bound for F_q(s_L)=phi_q(s_L)-phi_infty(s_L), because

    |tilde_phi_infty(s_L;s_R)-phi_infty(s_L)| = D_theta

has the nonzero magnitude in (0.1). Multiplying by zeta(2s) to cancel the
reflected theta-entry pole does not remove this defect: it multiplies both
terms by the same nonzero factor at any point away from the zeta divisor.
At a zero of zeta(2s), a separate local leading-term calculation is needed;
there is no scalar functional-equation identity that makes the defect vanish.

A possible future repair would compare a full theta scattering matrix or one
of its eigenchannels A+B or A-B, each of which has a scalar functional
equation after diagonalization. Identifying a finite one-cusp coefficient with
such a channel, and transferring the theta zero with that identification, is a
new CONJECTURAL theorem; it is not supplied by the current scalar RATE ledger.

## 8. Final lane verdict and handoff

The symmetric two-vertical-side O(E_R) transport for the existing scalar
phi_infty target is REFUTED AS STATED, pending a cold referee pass on the
algebra/source conventions. The exact first remaining gap is not a
harmonic-measure optimization: it is the missing scalar theta functional
equation. No amount of global zero-freeness, Lemma 7.7, anchor propagation, or
a q-uniform horizontal-side ceiling can repair that mismatch.

The parent lane must therefore either:

* bank this refutation after its independent *_REFEREE.md pass and retain the
  existing one-sided Route-B transport; or
* open a separate matrix/eigenchannel identification theorem, marked
  CONJECTURAL until proved and refereed.

No MAP entry, plan edit, or status promotion was made in this isolated lane.

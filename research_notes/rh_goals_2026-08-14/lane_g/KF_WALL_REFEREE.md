# Adversarial referee report: `KF_WALL_ATTACK_SOL.md`

**Date:** 2026-08-18

**Mode:** read-only audit apart from this report

**Required interpreter:** `/Users/za/.venvs/farey-rh/bin/python` with `python-flint`/Arb

**Target:** `KF_WALL_ATTACK_SOL.md`

## Verdict

**Overall: GAPS, not REFUTED.**

The two mathematical cores survive adversarial checking:

1. **Claim 1 -- conditional local bound:** **CONFIRMED after one necessary
   hypothesis clarification.**  Under nonvanishing and holomorphy on the full
   Hejhal rectangle
   \([1/2,1/2+\delta]\times[t_c-\delta,t_c+\delta]\), the Poisson argument
   correctly gives
   \[
   \sup_{D_0}|\phi_q-\phi_\infty|<109,
   \qquad \log 109=4.6913478822\ldots<4.692.
   \]
   It does not misuse positivity of the complex-valued difference.
2. **Claim 2 -- A0 side bound:** **CONFIRMED.**  The new bound controls the
   same \(K_+\) that A0 consumes:
   \[
   \sup_{\partial\Omega\setminus\Gamma_R}|\phi_q-\phi_\infty|
   <116.9436264459\ldots<117.
   \]

The report is nevertheless not clean enough for an unqualified `CONFIRMED`:

- `KF_WALL_ATTACK_SOL.md:270-286` does not define which inherited \(H_0\) is
  meant.  The proof needs the **full** width \(1/2\le\sigma\le1/2+\delta
  =1.4999\), whereas the old Route-B note literally defines a narrower
  \(H_0\) at `R3_ROUTE_B_TRANSPORT_SOL.md:91-120`.  The assembly plan and
  Hejhal's theorem do use the full \(R_\delta\)
  (`R3_R5_ASSEMBLY_PLAN_SOL.md:60-69`;
  `LAW_HEJHAL_S7_EXTRACT.md:43-47,67-76`), so this is a repairable statement
  gap, not a failure of the rebuilt argument.  Importing the old narrow
  \(H_0\) literally would invalidate the harmonicity step.
- The note alternates between a raw strict bound and a chosen ledger constant:
  `KF_WALL_ATTACK_SOL.md:440-442` writes both \(\sup|F_q|<109\) and
  \(109=:K_F\), while the headline says \(K_F<109\).  The correct formulation
  is either "the raw supremum is \(<109\)" or "take the safe constant
  \(K_F=109\)."
- The displayed three-decimal thresholds are safe when derived from the
  full-precision receipts, but they do not chain consistently to every
  subsequently printed rounded number.  In particular, the listed A0 integer
  does **not** satisfy the boxed condition \(\log q>38.386\); it satisfies the
  unrounded condition \(\log q>38.38555358\ldots\).  The Route-B threshold
  \(5599.981\) likewise uses the unrounded base, not the displayed
  \(4.687278\).  Receipts are below.

The advertised roughly \(10^5\)-fold collapse is also not like-for-like.  The
old \(4.711\times10^6\) threshold is Route B at the sixth-zero geometry; the
new \(38.386\) threshold is A0 at the first-zero contour.  Like-for-like:

- A0 improves \(86.640\to38.386\), a factor about \(2.26\) in \(\log q\);
- rebuilt Route B improves \(4{,}711{,}753.120\to5599.981\), a factor about
  \(841\).

This cross-route headline is rhetorically misleading, but it does not falsify
either conditional implication.

## 1. Section 3, line by line

### 1.1 Domain and regularity -- GAPS in wording; sufficient after repair

The affine map at `KF_WALL_ATTACK_SOL.md:270-281` sends
\(A=(0,1)\times(-1,1)\) to

\[
1/2<\sigma<1/2+\delta=1.4999,
\qquad |t-t_c|<\delta.
\]

This is within Lemma 7.7's strip \(1/2\le\sigma\le3/2\), and the lowest height
is

\[
t_c-\delta=17.7431840794\ldots>17.
\]

The source domain and finite-\(N\) nature of Lemma 7.7 are checked at
`M2_PERTERM_REFEREE.md:96-135`; the sixth-zero geometry is fixed at
`C0_TRANSPORT_CAMPAIGN_SOL.md:680-685`.

For the next line to be valid, \(H_0\) must mean

\[
\phi_q(s)\ne0
\quad\text{on the full closed right rectangle},
\]

and \(\phi_q\) must be holomorphic on an open neighborhood of that closure.
Then there are neither zeros nor poles there, \(\log|\phi_q|\) is harmonic,
and its boundary traces are continuous.  The target's words "closed-rectangle
holomorphy, and no poles" point in the right direction but do not cure the
ambiguous inherited \(H_0\).

### 1.2 The harmonic majorant -- CONFIRMED

At `KF_WALL_ATTACK_SOL.md:284-300`, Lemma 7.7 plus the repaired \(H_0\) gives

\[
0<|\phi_q|<107,
\qquad
u=\log\frac{107}{|\phi_q|}\ge0.
\]

Because \(\phi_q\) is holomorphic and nonzero, \(u\) is harmonic; this is not
merely a subharmonic-modulus assertion.  On the critical-line side,
unitarity/reflection gives \(|\phi_q|=1\), hence \(u=c=\log107\)
(`LAW_HEJHAL_S7_EXTRACT.md:67-70`).  If \(\omega_L\) is the harmonic measure of
that side, then

\[
v=u-c\omega_L
\]

is harmonic.  Its boundary data are zero on the left and \(u\ge0\) on the
other three sides, so the maximum principle gives \(v\ge0\).  Corner values
are harmless (zero harmonic-measure mass), provided the preceding
neighborhood/continuity hypothesis is stated.

There is **no tacit positivity assumption on**
\(F_q=\phi_q-\phi_\infty\).  The positive harmonic function is built from
\(\phi_q\) alone.  The complex-valued \(F_q\) enters only at the final triangle
inequality (`KF_WALL_ATTACK_SOL.md:436-441`).

### 1.3 Poisson-kernel ratio -- CONFIRMED

The kernels used at `KF_WALL_ATTACK_SOL.md:301-318` have the correct domains:

- right-side kernel on \((0,1)\times(-1,1)\): vertical sine modes with
  \(\sinh(n\pi x/2)/\sinh(n\pi/2)\);
- top/bottom kernels: horizontal sine modes with
  \(\sinh(n\pi(1\pm y))/\sinh(2n\pi)\).

At the boundary-coordinate endpoints both numerator and denominator vanish.
Factoring
\(\sin(n\alpha)=\sin\alpha\,U_{n-1}(\cos\alpha)\) is legitimate, and
\(|U_{n-1}|\le n\) gives the printed geometric tails.  The Arb boxes cover the
entire boundary parameter interval and the semicircle.  For fixed boundary
point, \(P_j(z,\xi)/P_j(a,\xi)\) is harmonic in \(z\); it vanishes on the
diameter \(x=0\).  Therefore the maximum principle extends the semicircle
bound to all of \(T_\kappa\), exactly as claimed at
`KF_WALL_ATTACK_SOL.md:406-409`.  Reflection \(y\mapsto-y\) covers the bottom
kernel.

Independent execution of the target's full Arb script
`KF_WALL_ATTACK_SOL.md:321-383` returned:

```text
right target_tail_upper=1.81245336103090916749e-25...
right anchor_tail_upper=3.88521088217974638393e-13...
right anchor_factored_den_lower=0.16384417909602939212118...
right factored_num_upper=0.05831631225945842481649... where=(128,128)
right CERT_GLOBAL_RATIO_UPPER=0.35592544441434883535848...
top target_tail_upper=1.39580343436914596983e-39...
top anchor_tail_upper=7.32665706469001107334e-43...
top anchor_factored_den_lower=0.04289202215633439903963...
top factored_num_upper=0.01244129607428639779288... where=(150,0)
top CERT_GLOBAL_RATIO_UPPER=0.29006084229230112602729...
CERT_H_lt_0.356=True
```

Thus

\[
v(z)\le0.356v(a)\le0.356u(a)
\]

is valid.  This is a standard positive-boundary-data Poisson comparison, not a
boundary-Harnack theorem requiring additional smooth-domain hypotheses.  The
rectangle is Lipschitz in any event, and the proof explicitly supplies the
kernel comparison it consumes.

### 1.4 Reflection and the constant 109 -- CONFIRMED conditionally

Anchor activation gives
\(|\phi_q(a)|>0.07843/2\), hence

\[
u(a)<\log(2\cdot107/0.07843)=7.9115247867\ldots.
\]

Since \(u-c=-\log|\phi_q|\), reflection gives on the left half of \(D_0\)

\[
\log|\phi_q|<0.356(7.9115247867\ldots)
=2.8165028240\ldots,
\]

so \(|\phi_q|<16.718282\).  On the right half, Lemma 7.7 gives
\(|\phi_q|<107\).  The sixth-zero theta square cover gives
\(\sup_{D_0}|\phi_\infty|<1.867346<2\)
(`C0_TRANSPORT_CAMPAIGN_SOL.md:722-750`).  Therefore

\[
\sup_{D_0}|F_q|<\max(107+2,16.719+2)=109.
\]

The argument is conditional on the full zero-free hypothesis, anchor
activation, and the holomorphy/divisor gate.  It does not prove those gates.

## 2. Route 1 / A0 promotion

### 2.1 Same quantity -- CONFIRMED

The original A0 note defines

\[
F_q=\phi_q-\phi_\infty,
\qquad
K_+\ge\sup_{\partial\Omega\setminus\Gamma_R}|F_q|
\]

at `R3_TRANSPORT_EXECUTION_SOL.md:68-83,167-185`.  The target uses the identical
\(\Omega\) and \(t_0\) (`KF_WALL_ATTACK_SOL.md:94-110`).  On every non-RATE
side,

\[
|t|\ge t_0-1/2
=6.567362570867\ldots>13/2.
\]

Lemma 7.7 may therefore be used with \(\varepsilon=13/2\).  The independent
full boundary cover gives \(|\phi_\infty|<0.3825\) on the same rectangle
(`R3_ROUTE_B_TRANSPORT_SOL.md:293-301,654-696`).  Hence the triangle inequality
proves the exact A0 side norm, not an adjacent diagnostic:

\[
K_+^{\rm raw}
<C_6(13/2)+0.3825
<116.9436264459<117.
\]

The old \(4{,}876{,}833\) value occupied the same formal slot but depended on
the conjectural common \(y_0=1000\) use of Proposition 12.4
(`R3_TRANSPORT_EXECUTION_SOL.md:254-279`;
`C0_TRANSPORT_CAMPAIGN_SOL.md:890-946`).  The new proof bypasses that assumption.

Minor repairs:

- say "take the safe envelope \(K_+=117\)" after proving the raw supremum is
  \(<117\);
- restore the original \(0<E_R\le K_+\) hypothesis, or treat \(E_R=0\)
  separately;
- remove the stray comma in `117^{,1-0.1552}` at
  `KF_WALL_ATTACK_SOL.md:157-159`.

### 2.2 C6 source category -- CONFIRMED with a wording restriction

The banked p. 574 scan identifies Lemma 7.7 as a bound on the **whole finite-\(N\)
scattering coefficient** \(\phi_N\), not on a Fourier coefficient
(`M2_PERTERM_TRANSCRIPTION_SOL.md:186-207,609-622`).  Solving the p. 155
quadratic permits the explicit choice

\[
C_6(\varepsilon)
=100\{\varepsilon^{-1}+\sqrt{1+\varepsilon^{-2}}\}
\]

(`M2_PERTERM_TRANSCRIPTION_SOL.md:351-370`;
`M2_PERTERM_REFEREE.md:96-135`).  It is an admissible explicit choice, not a
source-printed canonical or optimal constant.

Theorem 12.9(c),(d) instead controls per-mode \(\phi_m\) and the Eisenstein
tail with hidden constants depending on \((\Gamma,\chi,\mathcal F,\delta)\)
(`M2_PERTERM_TRANSCRIPTION_SOL.md:506-529`).  Its covering number, low-height
argument, divisor clearance, and family uniformity remain open
(`M2_PERTERM_TRANSCRIPTION_SOL.md:549-607,683-719`).

Thus the two premise corrections in `KF_WALL_ATTACK_SOL.md:23-35` are
**CONFIRMED for finite q**.  "Per-mode constants are avoidable" must be scoped
to the conditional A0/Route-B non-RATE transport bound; it does not prove the
still-missing full-side RATE.

## 3. Independent Arb arithmetic

### 3.1 Reproduced constants

Independent consolidated execution with
`/Users/za/.venvs/farey-rh/bin/python`, `ctx.dps=100`, returned:

```text
A0_C6_upper=116.56112644589158030740374763945456...
A0_Kraw_upper=116.94362644589158030740374763945456...
A0_Kraw_lt_117=True
A0_logq_CR1_upper=38.38555358149782944200035562679008...
A0_E_required_lower=9.89097430637911054877177614823e-21...
A0_finite_contour_upper=77.75306553638937642333399749787051...
A0_finite_margin_ratio_upper=1771.14044502025914403949880405172...
B_tc_minus_delta_lower=17.74318407941283562860888174035267...
B_C6_eps17_upper=106.05521391721412450666659896398425...
B_C6_lt_107=True
B_La_upper=7.91152478677941342201372747758559...
B_HLa_upper=2.81650282409347117823688698202047...
B_reflected_phi_upper=16.71828154714109585793366183422372...
log109_upper=4.69134788222914370037731645220920...
B_c0=0.0008677256...
B_base_upper=4.68727707957322768732242032506432...
B_logq_CR1_upper=5599.98072458948676591556126523593...
B_anchor_logq_CR1_upper=4.37170867223036160838089659974...
B_ideal_base0_logq_upper=1098.48366955539564375050093869153...
B_finite_logE3_upper=4.68910588160682817081150041471...
log(0.3186)=-1.14381888150618890185294761279...
```

The older "insert \(C_6=117\) into the old chain" diagnostic at
`KF_WALL_ATTACK_SOL.md:193-201` also reproduces:

```text
routeB_C6_117_Lanchor_upper=8.00086988711526336755330657597268...
routeB_C6_117_A_upper=47.05477215808903827973075647600198...
routeB_C6_117_logKH_upper=4792.95973441456765653202050328087...
```

All central full-precision constants are therefore numerically correct.

### 3.2 End-to-end rounding defects

#### A0 integer

The exact threshold is

\[
T_A=38.3855535814978294420\ldots,
\]

so
\(\lfloor e^{T_A}\rfloor+1=46{,}841{,}857{,}142{,}466{,}894\) is valid for the
**exact** threshold.  But `KF_WALL_ATTACK_SOL.md:170-181,579-584` boxes the
stronger rounded condition \(\log q>38.386\).  Independent Arb output is:

```text
ln_listed_A0_integer=
  38.38555358149782946215712664344555...
listed_satisfies_boxed_38p386=False
exp_38p386_upper=46862772882410611.87017827030246...
strict_integer_for_boxed_38p386=46862772882410612
```

Therefore the displayed integer is refuted **as the integer corresponding to
the boxed three-decimal condition**.  It remains correct for the unrounded Arb
condition.  The note must choose one precision convention and keep it.

#### Route-B displayed base

The exact base
\(4.6872770795732276\ldots\) gives
\(T_B=5599.9807245894\ldots\), so the boxed \(5599.981\) is safe.  However
`KF_WALL_ATTACK_SOL.md:461-472` first displays the rounded-up base
\(4.687278\).  Chaining only displayed numbers gives:

```text
T_from_displayed_base_4p687278=
  5599.98160853518372422202327248000...
3dp_safe_for_displayed_base=5599.982
largest_base_compatible_with_5599p981=
  4.68727736635013109814705238721...
displayed_base_4p687278_compatible=False
```

Thus \(5599.981\) is confirmed from the full-precision receipt, but
\(5599.982\) is required if the rounded displayed base is the sole premise.

## 4. Anchor and window consistency

**CONFIRMED; no hidden mixing inside either chain.**

- A0 uses the first-zero contour \(t_0=\gamma_1/2\), the Rouché margin
  \(m_z>0.0439\), and harmonic-measure floor \(\nu_z>0.1552\)
  (`R3_TRANSPORT_EXECUTION_SOL.md:38-97`).  It consumes neither
  \(d_*>0.6603\) nor \(d_*>0.3186\).
- The rebuilt Route B uses the sixth-zero shift
  \(t_c=t_6-0.050005\), \(\delta=0.9999\), target segment
  \([t_6-0.1,t_6-0.00001]\), and \(d_*>0.3186\)
  (`C0_TRANSPORT_CAMPAIGN_SOL.md:461-485,680-685,819-825`).
- The old \(d_*>0.6603\) belongs to the first-zero Route-B window
  (`R3_ROUTE_B_TRANSPORT_SOL.md:526-549`) and is not used in the new
  \(5599.981\) calculation.

The only mixing is in the headline comparison between the old Route-B
threshold and the new A0 threshold, already flagged as not like-for-like.

## 5. Proved-only regime and final ledger

The proved boundary campaign supplies only q-independent Ford envelopes and
therefore only \(\alpha=0\); a positive RATE remains open
(`R3_BOUNDARY_RATE_CAMPAIGN_SOL.md:5-25,396-408`).  Its determinant lineage also
lacks a proved Fredholm dimension tail (`R3_BOUNDARY_RATE_CAMPAIGN_SOL.md:27-38`).
Consequently the target's

\[
q_0=\texttt{UNDEFINED},
\qquad \log q_0=\texttt{UNDEFINED}
\]

is **CONFIRMED** (`R3_BOUNDARY_RATE_CAMPAIGN_SOL.md:554-570`).  Writing
\(+\infty\) would indeed overstate a missing theorem.

| audited claim | verdict |
|---|---|
| finite-\(q\) Lemma 7.7 is whole-scattering, not Theorem 12.9 per-mode | **CONFIRMED** |
| per-mode 12.9 constants/family uniformity remain open | **CONFIRMED** |
| A0 raw non-RATE-side supremum is \(<117\) | **CONFIRMED**; same \(K_+\) quantity |
| Poisson ratio \(H<0.356\) | **CONFIRMED** by independent full Arb rerun |
| direct \(\sup_{D_0}|F_q|<109\) | **CONFIRMED CONDITIONALLY** after defining full-width \(H_0\) |
| notation \(K_F<109\) together with \(K_F:=109\) | **GAP / inconsistent notation** |
| exact A0 threshold \(38.38555358\ldots\) | **CONFIRMED CONDITIONALLY** |
| listed A0 integer as satisfying boxed \(\log q>38.386\) | **REFUTED**; correct boxed-threshold integer is 46,862,772,882,410,612 |
| exact rebuilt Route-B threshold \(5599.98072458\ldots\) | **CONFIRMED CONDITIONALLY** |
| \(5599.981\) chained from displayed base \(4.687278\) alone | **REFUTED**; use full precision or round threshold to 5599.982 |
| sixth-zero chain uses \(d_*>0.3186\), not old \(0.6603\) | **CONFIRMED** |
| unconditional effective \(q_0\) | **`UNDEFINED`**, honestly stated |

**Final referee disposition:** retain the two conditional mechanisms, but do
not promote the note unchanged.  Define the full-width \(H_0\), normalize the
meaning of \(K_F,K_+\), scope the C6 wording to an admissible finite-\(q\)
choice, and repair the rounded threshold/integer chain.

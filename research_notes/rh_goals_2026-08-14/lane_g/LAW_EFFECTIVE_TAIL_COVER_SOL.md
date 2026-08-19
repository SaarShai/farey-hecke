# LAW Route-B effective tail / covering: endpoint \(p=3\) candidate

**Date:** 2026-08-19
**Lane:** Route B, effective-tail/covering
**Status:** `CONDITIONAL CANDIDATE — AWAITING COLD REFEREE`; not an
unconditional proof of the LAW.

## 0. Executive verdict

The useful structural improvement is an exact endpoint calculation at
\(p=3\), rather than taking the singular-looking \(p<3\) estimate to a
limit. Under the paper-level atom-moment bridge, the referee-confirmed `(FW)`
count, the printed whole-coefficient Hejhal bound, and the matched boundary
decomposition, the endpoint tail has the form

\[
 E(q,s)\le q^{-2}\{a(\log q+5+65/q)+b\}.
\]

The enlarged rectangle

\[
 \frac12<\Re s<\frac32,
 \qquad |\Im s-t_0|<2.38,
\]

with seed circle centre \(3/4+it_0\), radius (1/40), has an outward-Arb
cover that passes the pointwise Rouché/harmonic-measure inequality at the
strict integer

\[
 \boxed{q_{\mathrm{endpoint}}=31951437654668744792}.
\]

This is an effective-tail candidate, not a certified full LAW theorem. The
number is useful because it is a finite, reproducible target; it is still
conditional on upstream theorem scope and a separate cold referee. The
receipt does **not** prove that this integer is the least possible one; the
predecessor fails only the displayed conservative interval certificate.

The first exact gap is the endpoint promotion itself: the existing
`BOUNDARY_ALPHA_THEOREM_SOL.md` proof is written for \(2<p<3\). The direct
endpoint layer-cake calculation below is mathematically straightforward, but
the MVT/pairing normalization, the \(M(3/2)\) endpoint, and the closed-strip
scope of Lemma 7.7 must be checked by an adversarial referee before any status
upgrade.

## 1. Ledger and primary-source audit

The primary Hejhal source used here is the scan

`research_notes/rh_goals_2026-08-14/lane_p/literature/Hejhal_LNM1001_Vol2_s7_pp568-600.pdf`,

pp. 568--600, especially Lemma 7.7 (p. 574), Proposition 7.8, and the
Theorem 7.11 proof (pp. 577--578). The repository extraction records the
source hash and the distinction between the printed qualitative theorem and
the quantitative whole-coefficient estimate:

```text
$ sed -n '1,85p' research_notes/rh_goals_2026-08-14/lane_g/LAW_HEJHAL_S7_EXTRACT.md
# Hejhal LNM 1001 Vol. 2, §7 — full extraction (source received from Koyama, 2026-08-17)
Source: scan pp. 568–600, banked at ../lane_p/literature/Hejhal_LNM1001_Vol2_s7_pp568-600.pdf
...
- Prop 7.6: E_N ⇒ E_∞ and φ_N ⇒ φ_∞ on compacta of H × {Re s > 1}
- Lemma 7.7: |φ_N(s)| ≤ C₆(ε) for 1/2 ≤ σ ≤ 3/2, |t| ≥ ε (uniform in N).
- Prop 7.8: φ_N ⇒ φ_∞ on compacta of ℛ₁ ... (Vitali ...).
- Theorem 7.11 (p. 577): ... whenever N is sufficiently large.
...
3. [I] Prop 7.8 + Hurwitz ... ineffective: no rate, no explicit inf.
6. [I] Vitali ... φ_N ⇒ φ_∞ ...
```

The p. 574 estimate is a bound for the whole scattering coefficient, not a
per-mode estimate. Its explicit safe form and strip are recorded by:

```text
$ rg -n -F -e 'C6(epsilon)' -e 'B=10' -e '1/2 <= Re(s) <= 3/2' \
    research_notes/rh_goals_2026-08-14/lane_g/M2_PERTERM_TRANSCRIPTION_SOL.md
12:    C6(epsilon)=100[epsilon^(-1)+sqrt(1+epsilon^(-2))].
192:    LEMMA 7.7. For each epsilon > 0, there exists a positive constant C6(epsilon) ...
199:image confirms `|phi_N(s)|<=C6(epsilon)`, `B=10`, and that this is the whole
203:    C6(epsilon) = 100 [ epsilon^{-1} + sqrt(1+epsilon^{-2}) ].
222:For 1/2 <= Re(s) <= 3/2 and y>0,
```

The atom-moment input is not silently strengthened here. The direct bridge and
its referee ledger give (C_4=2^{62}+1) at paper level; machine
formalization remains open. `(FW)` is likewise used only with its
referee-confirmed paper-level scope. Both inputs are therefore hypotheses of
the candidate until the required cold referee pass is banked.

## 2. Two false targets corrected before the endpoint calculation

### 2.1 The earlier (p\simeq2.98), \(\sigma_R=1.1\) scan was invalid

The renewal estimate is parameterized by (p=2\sigma), not by an independent
free (p). Thus (p\simeq2.98) requires a right boundary near
\(\sigma_R\simeq1.49\). Using (p\simeq2.98) on the old
\(\sigma_R=1.1\) rectangle was a false target and is not used below. The
endpoint (p=3) is paired with the legal closed-strip endpoint
\(\sigma_R=3/2\).

### 2.2 The old HJL (q_M=q) Route-B budget is refuted

The independent cold review says the corrected invariant is the normalized
cusp width (q_M=\lambda_q=2\cos(\pi/q)), not (q); the proposed unbounded
positivity budget is therefore dead. This endpoint route does not consume that
budget. The correction is recorded rather than rewritten into the old note:

```text
$ rg -n -i -e 'q_M' -e 'lambda_q' -e 'REFUT' -e 'DEAD' \
    research_notes/rh_goals_2026-08-14/lane_g/COLD_REVIEW_ROUTEB_FATE.md | head -20
1:# COLD REVIEW — Route B's fate: MIS-INSTANTIATED, and DEAD once corrected
16:... corrected instantiation is `O(1)`, so Route B via (B4★) is DEAD anyway.
22:... normalizing the cusp width `λ_q = 2cos(π/q)` ...
52:... `q_{M_q} = q` ... **REFUTED** ...
53:... `q_M = 2cos(π/q)`, **PROVED-here** ...
```

## 3. Direct endpoint tail calculation

Use the exact atom-moment weight from the bridge,

\[
 A_X=\sum_{|a_j|\ge2}|a_j|+\ell(W_X),
 \qquad w_X=1+A_X^2,
 \qquad x_X\ge1,
\]

not (k_X^2). The source convention is recorded by:

```text
$ rg -n -F -e 'w_X:=1+A_X^2' -e 'w(W)=1+A(W)^2' \\
    research_notes/rh_goals_2026-08-14/lane_g/ATOM_MOMENT_BRIDGE_SOL.md \\
    research_notes/rh_goals_2026-08-14/lane_g/BOUNDARY_ALPHA_THEOREM_SOL.md
research_notes/rh_goals_2026-08-14/lane_g/ATOM_MOMENT_BRIDGE_SOL.md:114: w_X:=1+A_X^2,}                                      \tag{1.2}
research_notes/rh_goals_2026-08-14/lane_g/BOUNDARY_ALPHA_THEOREM_SOL.md:328: w(W)=1+A(W)^2,                                      \tag{3.3}
```

Let

\[
 W_q(Y)=\sum_{x_X\le Y}w_X.
\]

The two-mark/atom bridge supplies the positive majorant

\[
 W_q(Y)\le C_4Y^2
 \begin{cases}
 Y,&1\le Y\le q,\\
 qR^2+R^4,&Y\ge q,
 \end{cases}
 \qquad R=1+\log_+(Y/q).
 \tag{3.1}
\]

with (C_4=2^{62}+1) as a paper-level input. For (p=3), Tonelli gives

\[
 S_w(3,q)=\sum_Xw_Xx_X^{-3}
 =3\int_1^\infty W_q(Y)Y^{-4}\,dY.
\]

Split the integral at (Y=q), without passing through (p<3):

\[
\begin{aligned}
3\int_1^q C_4Y^{-1}\,dY&=3C_4\log q,\\
3\int_q^\infty C_4Y^2(qR^2+R^4)Y^{-4}\,dY
 &=3C_4\left[
   \int_1^\infty u^{-2}(1+\log u)^2du
  +q^{-1}\int_1^\infty u^{-2}(1+\log u)^4du
 \right].
\end{aligned}
\]

For (j\ge0),

\[
 \int_1^\infty u^{-2}(\log u)^jdu=j!,
\]

so the two endpoint integrals are (1+2+2=5) and
(1+4+12+24+24=65). Consequently the direct endpoint statement is

\[
 \boxed{S_w(3,q)\le3C_4\left(\log q+5+\frac{65}{q}\right).}
 \tag{3.2}
\]

This exact endpoint passage avoids the artificial (1/(3-p)) divergence in
the (p<3) display. It is a proposed theorem step, not yet a status upgrade:
`AWAITING COLD REFEREE`.

### 3.1 Pair and wrap terms

For the matched pair, use the already printed positive comparison
\(x_X\le y_X\), the endpoint version of the shallow/deep split, and
\(2-\lambda_q\le\pi^2/q^2\). Directly at (p=3), the same two cases give

\[
 E_{\mathrm{pair}}(q,s)
 \le \frac{6\pi^2(|s|+1)C_4}{q^2}
       \left(\log q+5+\frac{65}{q}\right).
 \tag{3.3}
\]

The `(FW)` count is stated for every (p=2\sigma>2), including (p=3),
and its direct layer-cake integral is

\[
 E_{\mathrm{wrap}}(q,s)
 \le pC_1q^{1-p}
   \left(\frac1{p-2}+\frac1{(p-2)^2}\right),
 \qquad C_1=128(1+\log2).
\]

At (p=3), this is

\[
 E_{\mathrm{wrap}}(q,s)\le 6C_1q^{-2}.
 \tag{3.4}
\]

The endpoint uses (M(3/2)=B(1,1/2)=2) from the beta-integral majorant.
On the right boundary \(\sigma_R=3/2\), set

\[
 S_R=\sup_{s\in\Gamma_R}|s|,
 \quad a=2\cdot6\pi^2(S_R+1)C_4,
 \quad b=2\cdot6C_1.
\]

The resulting endpoint error envelope is

\[
 E_R(q)\le E_3(q):=
 q^{-2}\left[a\left(\log q+5+\frac{65}{q}\right)+b\right].
 \tag{3.5}
\]

Equivalently, with (C_1=128(1+\log2)),

\[
 \boxed{
 E_3(q)\le
 12q^{-2}\left[\pi^2(S_R+1)C_4
 \left(\log q+5+\frac{65}{q}\right)+C_1\right].}
 \tag{3.6}
\]

The factor 12 is (M(3/2)\times 6): the (6) is the endpoint factor in
the pair and wrap bounds after (3.2), while the atom weight itself is exactly
(w(W)=1+A(W)^2) as quoted above. No hidden replacement by (k(W)^2) or a
second atom-weight factor is made.

The three preceding displays are the structural Route-B improvement. Their
formal status is `AWAITING COLD REFEREE`; no claim here upgrades the source
ledger's `(RATE-A)` status.

## 4. Enlarged geometry and pointwise covering

Use the rectangle

\[
 \Omega=\{s:\tfrac12<\Re s<\tfrac32,
                 |\Im s-t_0|<\delta\},
 \qquad \delta=2.38,
\]

and the seed circle \(|s-(3/4+it_0)|=r\), (r=0.025). In normalized
coordinates (x=\Re s-1/2), (y=\Im s-(t_0-\delta)), one has

\[
 L=1,\qquad H=2\delta=4.76,
\]

and the harmonic measure of the right side is represented by

\[
 \omega(x,y)=\sum_{n\ \text{odd}}
 \frac4{n\pi}
 \frac{\sinh(n\pi x/H)}{\sinh(n\pi L/H)}
 \sin(n\pi y/H).
 \tag{4.1}
\]

For the seed circle, the (n>101) tail is bounded by the geometric envelope

\[
 \frac4{\pi n_0(1-e^{-2\pi L/H})}
 \frac{e^{-n_0a}}{1-e^{-a}},
 \quad n_0=103,
 \quad a=\frac{\pi(L-(1/4+r))}{H}.
 \tag{4.2}
\]

The continuous seed-circle enclosure uses 8192 interval boxes. The endpoint
activation is evaluated pointwise: for each box (i), use its own lower
bounds (m_i\le\min|\phi_\infty|) and \(\nu_i\le\omega), rather than
combining the global minima from different boxes. Since (E_3(q)<K),

\[
 K^{1-\nu_i}E_3(q)^{\nu_i}
 \le K^{1-\underline\nu_i}E_3(q)^{\underline\nu_i},
\]

and the latter is compared with \(\underline m_i\). This is the relevant
pointwise Rouché/harmonic-measure pincer. The global floors are retained only
as diagnostics; they are not multiplied together.

### 4.1 Full Arb receipt

The complete replay is in
`research_notes/rh_goals_2026-08-14/lane_g/law_probes/routeb_endpoint_p3_cover.py`.
Run it with the declared Arb/flint interpreter:

```bash
$ PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python \
    research_notes/rh_goals_2026-08-14/lane_g/law_probes/routeb_endpoint_p3_cover.py
```

The command printed the following (the output is quoted before the claims
that consume it):

```text
sigma_R= 1.500000000000000000000000000000000000000000000000000000000000000000000 p=3 alpha=2
delta= [2.380000000000000000000000000000000000000000000000000000000000000000000 +/- 5.84e-72] radius= [0.02500000000000000000000000000000000000000000000000000000000000000000000 +/- 1.14e-73] L= 1.000000000000000000000000000000000000000000000000000000000000000000000 H= [4.760000000000000000000000000000000000000000000000000000000000000000000 +/- 1.17e-71]
t0= [7.067362570867346895228625991781235135392128557849621587842783730074982 +/- 4.17e-70]
circle_boxes= 8192 harmonic_boxes= 8192 series_nmax= 101
harmonic_tail_upper= [1.748104603018052326184818127852444898645746998909357406784699706716472e-23 +/- 3.37e-93]
min_phi_lower= 0.01168887213862035423517227172851562500000000000000000000000000000000000
min_nu_lower= [0.2245322055999083002460647051958323866789050537738555497887256757038436 +/- 4.42e-71]
S_vertical_upper= [9.565702250510690346172375979063921459261526021347426145804246663095551 +/- 3.47e-70]
theta_boundary_sup_upper= 1.114396933466196060180664062500000000000000000000000000000000000000000 edge= left cell= 3716
C4= 4611686018427387905
M_endpoint= 2.000000000000000000000000000000000000000000000000000000000000000000000
a_upper= [5770840757117238329716.761706657768159026050115058822218160162626309995 +/- 1.65e-49]
b_upper= [2600.674069340075995264868538559759208563968206377352070329364494581853 +/- 3.60e-67]
C6_epsilon_4.68= [123.6248974799147571158881087298810863558621869397994659653859804025225 +/- 1.58e-68]
Kraw_upper= [124.7392944133809531760687727923810863558621869397994659653859804025225 +/- 1.58e-68]
CERT_Kraw_lt_125= True
q= 31951437654668744792
E_endpoint_upper= [2.821320135145467239778340293440376794614361193523623648195483776832223e-16 +/- 3.14e-86]
max_ratio_q_upper= [0.9999999999999999999883692775839494652069751039144774898937695919613894 +/- 2.88e-71] cell= 4136
max_ratio_q_cell_m_lower= 0.01363041861623059958219528198242187500000000000000000000000000000000000
max_ratio_q_cell_nu_lower= [0.2245436958930480714945581707626372200348608173081028924425863498894329 +/- 6.24e-72]
PASS_all_cells_q= True
q_minus_1= 31951437654668744791
max_ratio_prev_upper= [1.000000000000000000002283784093023924202037770193596600349355895732696 +/- 1.41e-70] cell= 4136
PREV_CERTIFICATE_FAILS= True
endpoint_derivative_bracket_lower= [570283126614840517431175.2860094782328107386534955348970232304237454 +/- 2.35e-47]
MONOTONE_FOR_q_ge_12= True
```

The interval cover therefore gives (K_+<125) for this enlarged geometry,
and the active worst box has (m_i>0.0136304) and
\(\nu_i>0.2245436\). The global circle floor is only (0.0116888\ldots);
the receipt uses the paired box values, not an invalid global-minimum pairing.

## 5. Monotonic activation and exact first gap

Write

\[
 H(q)=a\left(\log q+5+\frac{65}{q}\right)+b,
 \qquad E_3(q)=q^{-2}H(q).
\]

The derivative is exact:

\[
 E_3'(q)=q^{-3}\left[a\left(1-\frac{65}{q}\right)-2H(q)\right]
 =-q^{-3}\left[a\left(2\log q+9+\frac{195}{q}\right)+2b\right]<0
 \quad(q\ge12).
 \tag{5.1}
\]

The final two receipt lines give a positive lower enclosure for the bracket,
so the endpoint envelope is decreasing on the full tail (q\ge12). Thus the
all-cell inequality at the displayed integer propagates to every larger
integer, subject to the theorem inputs listed below.

The predecessor line is deliberately reported as
`PREV_CERTIFICATE_FAILS=True`, not as a proof that the true LAW fails at
\(q-1\). It means only that the same conservative interval pincer does not
certify \(q-1\).

## 6. What remains open (and what this route does not prove)

1. **Endpoint cold referee.** The direct (p=3) layer cake, the endpoint
   shallow/deep complex-power MVT, the use of (M(3/2)=2), and the
   closed-strip use of Lemma 7.7 require a separate adversarial review in an
   own `*_REFEREE.md`. Until that pass, every claim in Sections 3--5 is
   `AWAITING COLD REFEREE`.

2. **Atom bridge scope.** The (C_4=2^{62}+1) bridge is paper-level and
   referee-confirmed only under the accepted marked-coding/Ford inputs; its
   independent Lean/machine certificate is still open. The receipt therefore
   cannot upgrade the full LAW to unconditional.

3. **Finite-(q) analytic gates.** The cover supplies a continuous
   theta-boundary enclosure, but the transport argument still consumes the
   full-rectangle holomorphy/nonvanishing contradiction case split and the
   already-identified R5 activation gates. The endpoint calculation does not
   create a machine proof of those analytic hypotheses.

4. **Hejhal's qualitative theorem is not an effective tail.** The printed
   Theorem 7.11 proof uses Hurwitz/Vitali and says “sufficiently large”; it
   does not itself supply the integer above. The integer here comes from the
   separate matched-tail majorant and interval cover, conditional on their
   ledgers.

5. **Machine formalization.** No Aristotle/Lean dispatch was claimed for this
   endpoint in this lane. A formal endpoint layer-cake lemma and a decoder for
   the marked coding remain background work, not evidence for this note.

The exact first blocker for an unconditional LAW statement is therefore: a
cold referee must accept the endpoint theorem and its upstream AM/FW/transport
interfaces, after which the parent lane must update the dated MAP ledger and
run the independent machine/formalization gates. The effective-tail route has
made a finite candidate explicit; it has not removed those logical gates.

## 7. Reproducibility and handoff

Primary receipt artifact:

`research_notes/rh_goals_2026-08-14/lane_g/law_probes/routeb_endpoint_p3_cover.py`

The script is read-only with respect to the repository and uses
`/Users/za/.venvs/farey-rh/bin/python` only. It does not access credentials,
Kaggle, or Aristotle. The candidate should be cold-refereed before any
promotion block is appended to `MAP.md` or to a theorem note.

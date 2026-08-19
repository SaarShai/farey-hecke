# Cold referee: LAW symmetric scalar-tail obstruction

**Date:** 2026-08-19

**Candidate reviewed:** `322b7dba91d9e74b00769a7849f5ca8553f641b6`

**Solution:** `LAW_SYMMETRIC_TAIL_SOL.md`

**Referee verdict:** **REFUTATION CONFIRMED**, with the narrow scope stated
below.  The fresh Arb run also exposes a non-load-bearing transcription error
in the solution's geometry-only receipt; that receipt needs a dated correction
block before it is reused.

## 0. Exact scope of the verdict

The following proposed scalar conclusion is false for the existing target

\[
 F_q(s)=\phi_q(s)-\phi_\infty(s),
 \qquad \phi_\infty=A=\phi_{\infty,\infty}^{\theta}:
 \qquad
 \sup_{s\in\Gamma_L}|F_q(s)|=O(E_R(q)),\quad E_R(q)\to0,
\]

when the left and right points are paired by
\(s_L=1-\overline{s_R}\) and finite \(\phi_q\) is reflected using its
one-cusp scalar functional equation.  At the fixed pair used by the solution,
the left error instead tends to a nonzero channel mismatch.  This is a genuine
refutation of the proposed scalar two-wall transport, not merely failure to
prove it.

This verdict does **not** refute the LAW, does **not** promote the endpoint
RATE candidate, and does **not** prove a full-matrix or eigenchannel repair.
Every such repair remains **CONJECTURAL**.

Isolation receipt:

```text
$ git status --short --branch && git rev-parse HEAD
## codex/law-symmetric-tail-referee-20260819
322b7dba91d9e74b00769a7849f5ca8553f641b6
```

## 1. Source convention: the target really is the diagonal matrix entry

The convention attack passes.  The theta source note orders the rows and
columns by the two cusps and identifies the target as the diagonal
\((\infty,\infty)\) entry, while the pre-existing Route-B note independently
uses that same entry as `phi_infty`:

```text
$ nl -ba research_notes/rh_goals_2026-08-14/lane_g/LAW_ANCHOR_T1_THETA.md \
    | sed -n '18,30p;162,187p'
22   Phi_theta(s) = [[ A(s), B(s) ],
23                   [ B(s), A(s) ]] rows/cols ordered (cusp oo, cusp 1)
25   A(s) = phi_{oo,oo} = phi_{1,1} = g(s) / (4^s - 1)
164  sigma_infty = diag(sqrt(2), 1/sqrt(2)) ...
166  Allowed moduli ... all even positive integers.
186  phi_{oo,oo}(s) = g(s) / (4^s - 1). (3.1)

$ nl -ba research_notes/rh_goals_2026-08-14/lane_g/R3_ROUTE_B_TRANSPORT_SOL.md \
    | sed -n '62,76p'
62  The theta entry is the printed Ch. 11, (3.1), ((infinity,infinity))-entry
65  phi_infty(s)=
66   sqrt(pi) Gamma(s-1/2) zeta(2s-1) /
67    (Gamma(s) zeta(2s) (4^s-1)).
70  It is one entry of a two-cusp scattering matrix.  It is not a scalar unitary
71  scattering determinant.
```

I also visually read printed p. 527, equation (3.1), in the banked Hejhal scan.
It prints a two-by-two matrix whose common scalar factor is
\(g(s)\), whose diagonal entries are \((4^s-1)^{-1}\), and whose
off-diagonal numerator is \(2^s-2^{1-s}\).  The source identities used here
therefore are

\[
 \Phi_\theta(s)=
 \begin{pmatrix}A(s)&B(s)\\B(s)&A(s)\end{pmatrix},\qquad
 A(s)=\frac{g(s)}{4^s-1},\qquad
 B(s)=\bigl(2^s-2^{1-s}\bigr)A(s).
\]

Source/hash receipt:

```text
$ pdfinfo research_notes/rh_goals_2026-08-14/lane_p/literature/Hejhal_LNM1001_Vol2_ch11s3_pp524-532.pdf | rg 'Pages'
Pages:           9
$ shasum -a 256 research_notes/rh_goals_2026-08-14/lane_p/literature/Hejhal_LNM1001_Vol2_ch11s3_pp524-532.pdf
6deb4101e3f7470eb17f0c9f0fc83fb1e4e7459e6d1282c2aaf16e1d931afb2f  research_notes/rh_goals_2026-08-14/lane_p/literature/Hejhal_LNM1001_Vol2_ch11s3_pp524-532.pdf
```

`LAW_ANCHOR_T1_THETA.md:140-151` retains an inherited citation-hygiene
obligation: the external theorem number for the general constant-term formula
was not pinned in that session.  That does not create a convention gap here,
because the printed special-case matrix itself was inspected and the same
entry was independently bound in the Route-B note.

## 2. Exact matrix algebra and conjugations

Put \(r(s)=2^s-2^{1-s}\).  The diagonal entry of
\(\Phi_\theta(s)\Phi_\theta(1-s)=I\) is

\[
 A(s)A(1-s)+B(s)B(1-s)=1.
\]

Here \(r(1-s)=-r(s)\), hence

\[
 A(s)A(1-s)\bigl(1-r(s)^2\bigr)=1,
 \qquad
 A(s)A(1-s)=\frac1{1-r(s)^2}.                 \tag{R1}
\]

This does not require trusting a numerical matrix-functional-equation check.
Writing \(g(s)=\Lambda(2s-1)/\Lambda(2s)\), the classical meromorphic identity
\(\Lambda(w)=\Lambda(1-w)\) gives \(g(s)g(1-s)=1\).  With
\(x=2^s\), direct exact algebra gives

\[
 1-r(s)^2=(x^2-1)(4/x^2-1),
\]

which is exactly the product of the two rational denominators; the off-diagonal
matrix numerator is \(r(s)+r(1-s)=0\).  Independent exact receipt:

```text
$ gp -q <<'GP'
x='x; r=x-2/x; rr=2/x-x; D=(x^2-1)*(4/x^2-1);
print("r_ref_plus_r=", simplify(rr+r));
print("one_minus_r2_minus_D=", simplify(1-r^2-D));
print("matrix_offdiag=", simplify(r+rr));
print("matrix_diag_minus_D=", simplify(1+r*rr-D));
GP
r_ref_plus_r=0
one_minus_r2_minus_D=0
matrix_offdiag=0
matrix_diag_minus_D=0
```

All factors use the standard real branches on positive bases, and Gamma and
zeta commute with conjugation as meromorphic functions.  For
\(s_L=1-\overline{s_R}\), therefore

\[
 \overline{A(s_L)}=A(1-s_R),\qquad
 A(s_R)\overline{A(s_L)}=\frac1{1-r(s_R)^2}.  \tag{R2}
\]

This is not one in general.  The finite one-cusp convention, by contrast, is
explicitly recorded as

```text
$ nl -ba research_notes/rh_goals_2026-08-14/lane_g/R3_TRANSPORT_EXECUTION_SOL.md \
    | sed -n '220,231p'
220 Hejhal (7.22) ... is
223 phi_q(1/2-h+it) *
225 overline(phi_q(1/2+h+i*bar(t)))=1.
228 It follows that phi_q has a pole of the same order at
231 1-overline(s_q).
```

At real \(t=t_0\), away from a zero or pole, this says exactly

\[
 \phi_q(s_L)=\frac1{\overline{\phi_q(s_R)}}.    \tag{R3}
\]

## 3. Reflection inequality and genuine asymptotic refutation

Let \(a=\phi_q(s_R)\), \(b=A(s_R)\), and \(\ell=A(s_L)\).  Equations (R2)--(R3)
give

\[
 F_q(s_L)=
 \left(\frac1{\bar a}-\frac1{\bar b}\right)
 +\left(\frac1{\bar b}-\ell\right).
\]

If \(|a-b|\le E_R<|b|\), then \(|a|\ge |b|-E_R\), so

\[
 \left|\frac1{\bar a}-\frac1{\bar b}\right|
 =\frac{|a-b|}{|a||b|}
 \le \frac{E_R}{|b|(|b|-E_R)}.
\]

Consequently the solution's load-bearing inequality is correct:

\[
 |F_q(s_L)|\ge
 \left|\frac1{\bar b}-\ell\right|
 -\frac{E_R}{|b|(|b|-E_R)}.                    \tag{R4}
\]

The falsity is not conditional on the unrefereed explicit endpoint constant.
Hejhal Proposition 7.6 already supplies qualitative convergence on the compact
right wall:

```text
$ nl -ba research_notes/rh_goals_2026-08-14/lane_g/LAW_HEJHAL_S7_EXTRACT.md \
    | sed -n '19,38p'
19 Hecke group G_N ... N >= 3, N = infinity allowed and G_infinity = theta group
23 scattering coefficient phi_N(s) ... Re s > 1.
34 Prop 7.6: E_N => E_infinity and phi_N => phi_infinity on compacta of
35 H x {Re s > 1}.
```

Thus at the fixed \(s_R=3/2+it_0\), \(a\to b\).  Since the fresh Arb receipt
below proves \(|b|>0.0600417546692132\), (R3) is legal for all sufficiently
large finite \(q\), and

\[
 F_q(s_L)\longrightarrow \frac1{\bar b}-\ell.
\]

The latter has modulus strictly larger than \(15.4230148900416\).  Hence the
left error does not even tend to zero, whereas the actual right-wall compact
error tends to zero by Proposition 7.6.  No fixed constant can give the
proposed scalar two-wall \(O(E_R)\) estimate.  **REFUTATION CONFIRMED.**

## 4. Fresh outward-Arb receipts

The committed checker was read line by line and rerun without bytecode writes.
Its environment and hash are:

```text
$ PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
import flint
print('python-flint=', flint.__version__)
print('flint=', flint.__FLINT_VERSION__)
PY
python-flint= 0.9.0
flint= 3.6.0
$ shasum -a 256 research_notes/rh_goals_2026-08-14/lane_g/law_probes/symmetric_tail_obstruction.py
00940a76c15a516cd468fca298926fc8215f22df7b69bdb583e9d789799784a0  research_notes/rh_goals_2026-08-14/lane_g/law_probes/symmetric_tail_obstruction.py
```

Load-bearing rerun output (lower bounds are interval lower endpoints, upper
bounds are interval upper endpoints):

```text
$ PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python \
  research_notes/rh_goals_2026-08-14/lane_g/law_probes/symmetric_tail_obstruction.py
phiR_abs_lower= [0.06004175466921327920807165927480263705... +/- 1.96e-122]
theta_product_minus_1_abs_lower= [0.92602487628750253435246372981430060687... +/- 3.40e-121]
theta_product_minus_exact_abs_upper= [6.93574108465083523028029001730614181336e-118 +/- 4.78e-238]
D_theta_reflection_abs_lower= [15.42301489004162277658964802761607563243... +/- 1.41e-119]
E_endpoint_upper= [2.82132013514546723977834029344037679461e-16 +/- 4.08e-136]
reciprocal_correction_upper= [7.82610403910254290440205315576271477158e-14 +/- 4.24e-134]
F_left_floor_lower= [15.42301489004154451554925700218703161190... +/- 1.40e-119]
F_left_over_E_lower= [54665951225865880.02385928548734384484... +/- 1.05e-104]
rational_pole_t_lower= [9.06472028365438761925536589143333362034... +/- 2.01e-120]
rational_pole_t_upper= [9.06472028365438761925536589143333362034... +/- 2.72e-120]
rational_pole_residue_abs_lower= [2.81082314196179094940212748157336081991... +/- 4.40e-120]
zeta_2s_at_rational_pole_abs_lower= [3.12123858834773532707119107210756979807... +/- 3.85e-120]
zeta_2sminus1_at_rational_pole_abs_lower= [6.62904417198114476945143637103056273098... +/- 4.97e-120]
symmetric_harmonic_tail_upper_right= [1.25451154695431157332274246499903290700e-89 +/- 4.92e-209]
symmetric_harmonic_tail_upper_left= [1.70865400785922096134273720626753165948e-147 +/- 2.67e-267]
```

An independent 160-decimal Arb evaluation, written without importing the
candidate checker, returned:

```text
$ PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import acb, arb, ctx
ctx.dps=160
one=acb(1); half=acb('0.5')
t0=(acb.zeta_zero(1)/2).imag
sR=acb(arb('1.5'),t0); sL=one-sR.conjugate()
def A(s):
    return acb.pi().sqrt()*(s-half).gamma()*(2*s-one).zeta() / \
        (s.gamma()*(2*s).zeta()*(acb(4)**s-one))
r=acb(2)**sR-acb(2)**(one-sR)
product=A(sR)*A(sL).conjugate()
D=1/A(sR).conjugate()-A(sL)
sp=acb(0,(2*acb.pi()/acb(2).log()).real)
res=acb.pi().sqrt()*(sp-half).gamma()*(2*sp-one).zeta() / \
    (sp.gamma()*acb(4).log())
print('ind_product_minus_1_lower=',abs(product-one).lower())
print('ind_product_identity_error_upper=',abs(product-1/(1-r*r)).upper())
print('ind_D_lower=',abs(D).lower())
print('ind_sp_im_lower=',sp.imag.lower())
print('ind_sp_im_upper=',sp.imag.upper())
print('ind_residue_lower=',abs(res).lower())
print('ind_zeta2sp_minus1_lower=',abs((2*sp-one).zeta()).lower())
PY
ind_product_minus_1_lower= [0.92602487628750253435246372981430060687... +/- 2.59e-161]
ind_product_identity_error_upper= [7.02865056163200233102360182300949679026e-158 +/- 4.51e-318]
ind_D_lower= [15.42301489004162277658964802761607563243... +/- 3.41e-159]
ind_sp_im_lower= [9.06472028365438761925536589143333362034... +/- 4.47e-160]
ind_sp_im_upper= [9.06472028365438761925536589143333362034... +/- 1.60e-161]
ind_residue_lower= [2.81082314196179094940212748157336081991... +/- 1.57e-160]
ind_zeta2sp_minus1_lower= [6.62904417198114476945143637103056273098... +/- 4.66e-160]
```

The explicit endpoint numbers remain conditional on the upstream endpoint
candidate exactly as `LAW_SYMMETRIC_TAIL_SOL.md:86-98` says.  They illustrate
(R4); the qualitative refutation in Section 3 does not promote them.

### Receipt correction required

The displayed transcript in `LAW_SYMMETRIC_TAIL_SOL.md:192,195,197-198` is not
a byte-faithful copy of the checker output:

```text
$ sed -n '192p;195p;197,198p' \
  research_notes/rh_goals_2026-08-14/lane_g/LAW_SYMMETRIC_TAIL_SOL.md
reciprocal_correction_upper= [7.826104039102542904402053155762714771581894466320972898688550410...e-14 +/- 4.24e-134]
symmetric_union_harmonic_measure_lower= [0.944067026571504309702707553893741360009407915927620458330381969033463398059186294474334565320054994756160409 +/- 1.71e-121]
symmetric_harmonic_tail_upper_right= [1.25451154695431157332274246499903290700054512773077556689756003615350062245615012265039557533901504174565205302393115537 +/- 4.92e-209]
symmetric_harmonic_tail_upper_left= [1.70865400785922096134273720626753165948377855753970099044790373310873850410605214955188803467319637232265844067614093401 +/- 2.67e-267]
```

Most importantly, line 197 omits the central-value exponent `e-89`, and line
198 omits `e-147`; the printed `e-209` and `e-267` are the radii, not the
central values.  Line 192 also has an elided/corrupted middle digit string.
The fresh output above is the safe receipt.  This affects only the geometry
diagnostic: none of the matrix identity, \(D_\theta\), reflection inequality,
or pole claims consumes either harmonic-tail value.  A dated correction block
should be appended to the solution before those transcript lines are quoted
again.

## 5. Rational pole and noncancellation attack

For

\[
 H(s)=\frac{\sqrt\pi\,\Gamma(s-1/2)\zeta(2s-1)}
 {\Gamma(s)(4^s-1)},
\]

the roots of \(4^s-1\) are \(s=\pi i k/\log2\).  The solution uses the
\(k=2\) root \(s_p=2\pi i/\log2\).  It is simple because the derivative of
\(4^s-1\) there is \(\log4\), so

\[
 \operatorname*{Res}_{s=s_p}H(s)=
 \frac{\sqrt\pi\,\Gamma(s_p-1/2)\zeta(2s_p-1)}
 {\Gamma(s_p)\log4}.                           \tag{R5}
\]

The fresh lower bound in Section 4 proves this residue is nonzero.  Gamma is
finite and nowhere zero at the nonreal point, and the separate positive Arb
lower bounds prove that neither relevant zeta value vanishes.  The pole lies
strictly inside the stated height window; the adjacent rational poles lie
strictly outside:

```text
$ PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import acb, arb, ctx
ctx.dps=120
t0=(acb.zeta_zero(1)/2).imag
delta=arb('2.38')
tp=(2*acb.pi()/acb(2).log()).real
print('bottom_to_pole_lower=',(tp-(t0-delta)).lower())
print('top_minus_pole_lower=',((t0+delta)-tp).lower())
print('k1_below_bottom_lower=',((t0-delta)-tp/2).lower())
print('k3_above_top_lower=',(3*tp/2-(t0+delta)).lower())
PY
bottom_to_pole_lower= [4.37735771278704072402673989965209848495... +/- 4.72e-120]
top_minus_pole_lower= [0.38264228721295927597326010034790151504... +/- 2.73e-121]
k1_below_bottom_lower= [0.15500242904015308560094304606456832522... +/- 1.84e-121]
k3_above_top_lower= [4.14971785461423453365442284536876529512... +/- 6.03e-121]
```

Therefore, under the solution's explicitly stronger `H_global` hypothesis,
\(\zeta(2s)\phi_q(s)\) is holomorphic at \(s_p\), while \(H\) has the nonzero
simple pole (R5).  The proposed normalized full-rectangle function
\(G_q=\zeta(2s)(\phi_q-\phi_\infty)\) is not holomorphic there.  This is a
correct conditional secondary obstruction; it is not needed for the scalar
refutation.

## 6. Corrected moving target

The solution's repaired point-paired target is exact.  Define

\[
 \widetilde\phi_\infty(s_L;s_R)=\frac1{\overline{A(s_R)}}.
\]

If \(|a|\ge m_q>0\), \(|b|\ge m_\infty>0\), and \(|a-b|\le E_R\), then

\[
 \left|\phi_q(s_L)-\widetilde\phi_\infty(s_L;s_R)\right|
 =\frac{|a-b|}{|a||b|}
 \le\frac{E_R}{m_qm_\infty}.                    \tag{R6}
\]

This is not a bound for \(F_q(s_L)\), because its target differs from
\(A(s_L)\) by the nonzero \(D_\theta\).  For an entire paired wall it can be
written as the fixed reflected target
\(s_L\mapsto1/\overline{A(1-\overline{s_L})}\); it still is not the theta
diagonal entry at \(s_L\).

Diagonalizing the theta matrix gives formal scalar eigenchannels \(A+B\) and
\(A-B\), but identifying the finite one-cusp coefficient with either channel
and transporting the desired zero through that identification is a new
**CONJECTURAL** theorem.  Nothing in this referee upgrades it.

## 7. Blast radius

The candidate commit added only the solution and its checker, and no other
tracked Markdown file consumes the new result:

```text
$ git diff --name-status 322b7db^ 322b7db
A research_notes/rh_goals_2026-08-14/lane_g/LAW_SYMMETRIC_TAIL_SOL.md
A research_notes/rh_goals_2026-08-14/lane_g/law_probes/symmetric_tail_obstruction.py
$ rg -l "LAW_SYMMETRIC_TAIL_SOL|symmetric two-vertical-side O\\(E_R\\)|D_theta_reflection" --glob '*.md' . | sort
./research_notes/rh_goals_2026-08-14/lane_g/LAW_SYMMETRIC_TAIL_SOL.md
```

Accordingly:

1. **Refuted:** only the proposed scalar symmetric two-vertical
   \(O(E_R)\) transport for \(F_q=\phi_q-A\).
2. **Retained with its source caveats:** the one-sided right-wall Route-B
   transport and `LAW_EFFECTIVE_TAIL_COVER_SOL.md`, whose own header remains
   `CONDITIONAL CANDIDATE — AWAITING COLD REFEREE`.
3. **Unaffected:** the existing RATE theorem, finite-q work, and the statement
   of the LAW.
4. **Still open/CONJECTURAL:** full-matrix/eigenchannel identification,
   horizontal/Harnack closure, and unconditional LAW closure.

The mathematical blast radius is therefore narrow even though it decisively
stops this proposed scalar symmetric-tail continuation.

## 8. Pre-commit quality and security receipts

The referee adds documentation only.  The repo has no current graph index, so
the impact tool ran in its explicitly labelled degraded lexical mode; the
targeted dependency search in Section 7 is the substantive blast-radius check.

```text
$ if test -f graphify-out/graph.json; then echo GRAPH_INDEX=present; else echo GRAPH_INDEX=absent; fi
GRAPH_INDEX=absent
$ git status --short
?? research_notes/rh_goals_2026-08-14/lane_g/LAW_SYMMETRIC_TAIL_REFEREE.md
$ git diff --cached --check
[no output]
$ python3 .codex/skills/impact-of-change/tools/impact.py --repo . --diff working
# Impact of change (DEGRADED-MODE)
0 symbol(s) changed, 0 affected caller(s), risk = LOW
$ python3 .codex/skills/security-oversight/tools/security_scan.py --repo . --diff working
# Security oversight (lexical-triage)
456 added line(s) across 1 file(s); 0 finding(s) — risk = NONE
```

Security conclusion: no secret, dangerous sink, dependency, or authorization
surface was introduced by this Markdown-only referee.  This is lexical triage,
not a proof of security; the scanner's stated soundness limit remains in force.

**READY FOR JUDGING**

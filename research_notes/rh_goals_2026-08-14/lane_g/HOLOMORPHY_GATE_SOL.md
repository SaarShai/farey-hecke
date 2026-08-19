# Holomorphy/nonvanishing gate audit

**Date:** 2026-08-19  
**Lane:** G / holomorphy gate  

All computations below use
`/Users/za/.venvs/farey-rh/bin/python`. Bounds are reported with lower margins
rounded down and upper bounds rounded up. A computation explicitly labelled
`NOT EVIDENCE` is not used as a theorem premise.

## 0. Receipts before claims

### 0.1 Printed-source identity and page inventory

The three local primary-source extracts were hashed before use.

```text
$ shasum -a 256 \
    research_notes/rh_goals_2026-08-14/lane_p/literature/Hejhal_LNM1001_Vol2_{ch6s12_pp149-166,ch11s3_pp524-532,s7_pp568-600}.pdf
c0dee01cf83e45e5e489e25ea299ccb2ad3654659d284bd9abc031bc6570b62f  .../Hejhal_LNM1001_Vol2_ch6s12_pp149-166.pdf
6deb4101e3f7470eb17f0c9f0fc83fb1e4e7459e6d1282c2aaf16e1d931afb2f  .../Hejhal_LNM1001_Vol2_ch11s3_pp524-532.pdf
b0f9a7001b10f5e0eae5e5aca85124c0a233256aa0e08b5c0f04720185a2b1e9  .../Hejhal_LNM1001_Vol2_s7_pp568-600.pdf

$ pdfinfo .../Hejhal_LNM1001_Vol2_ch6s12_pp149-166.pdf | rg '^(Pages|Page size)'
Pages:           18
Page size:       461 x 684 pts
$ pdfinfo .../Hejhal_LNM1001_Vol2_ch11s3_pp524-532.pdf | rg '^(Pages|Page size)'
Pages:           9
Page size:       461 x 684 pts
$ pdfinfo .../Hejhal_LNM1001_Vol2_s7_pp568-600.pdf | rg '^(Pages|Page size)'
Pages:           33
Page size:       461 x 684 pts
```

Visual inspection of the rendered pages gave the following primary-source
statements.

| printed location | checked statement |
|---|---|
| Ch. 6, Proposition 12.5, pp. 156--157 | For \(\Re s\ge1/2\), \(V(s)=q_c^{2s-1}\phi(s)\prod_{k=0}^{M_\epsilon}(s-s_k)/(1-s-s_k)\), with \(\lvert V(s)\rvert\le1\). |
| Ch. 6, Theorem 12.9, p. 164 | Its strip estimates assume \(1/2\le\sigma\le3/2\) and \(\lvert s-s_k\rvert\ge\delta_p\); the theorem bounds away from exceptional points, rather than proving their absence. |
| Ch. 11, Section 3, p. 528, (3.6) | \(N_\theta(\lvert\gamma\rvert\le T)=(4T/\pi)\log(T\sqrt2/(\pi e))+O(\log T)\). |
| Ch. 11 notes, p. 599, note 86 | \(\lambda_1>1/4\) for the Hecke groups; the note points to the triangle-group argument of note 8. |
| Ch. 11, Section 7, p. 577, Theorem 7.11 | For every real \(t_0\) and \(0<\delta<1\), \([1/2,1/2+\delta]\times[t_0-\delta,t_0+\delta]\) contains zeros of \(\phi_N\) for all sufficiently large finite \(N\). |

The repo transcriptions independently locate the same facts at
`M2_PERTERM_TRANSCRIPTION_SOL.md:372-384,506-529,531-539,652-675` and
`LAW_HEJHAL_S7_EXTRACT.md:17-56,76-104,117-120`.

### 0.2 Exact full-\(H_0\) geometry

The kf-referee fixes \(t_c=t_6-0.050005\) and \(\delta=0.9999\)
(`KF_WALL_REFEREE.md:72-90,376-384`).

```text
$ PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python -B - <<'PY'
from flint import acb, arb, ctx
ctx.prec=256
d=arb('0.9999')
t6=(acb.zeta_zero(6)/2).imag
tc=t6-arb('0.050005')
print('backend=python-flint Arb prec_bits=',ctx.prec)
print('t6_ball=',t6)
print('tc_ball=',tc)
print('H0_re=[0.5,1.4999]')
print('H0_im_lo=',tc-d)
print('H0_im_hi=',tc+d)
PY
backend=python-flint Arb prec_bits= 256
t6_ball= [18.79308907941283562860888174035266641070279867541539660916650055681107454481 +/- 1.10e-75]
tc_ball= [18.74308407941283562860888174035266641070279867541539660916650055681107454481 +/- 1.40e-75]
H0_re=[0.5,1.4999]
H0_im_lo= [17.74318407941283562860888174035266641070279867541539660916650055681107454481 +/- 1.71e-75]
H0_im_hi= [19.74298407941283562860888174035266641070279867541539660916650055681107454481 +/- 1.92e-75]
```

Thus the full rectangle is

\[
 H_0=[1/2,1.4999]\times[t_c-0.9999,t_c+0.9999],
 \qquad \Im H_0>17.7431840794.
\]

### 0.3 Current certificate-engine identity

```text
$ git ls-tree -r HEAD -- engine/certify
[no output]
$ git -C .worktrees/aletheia-restore rev-parse HEAD
9687720a4ecac683afefbd302e132b3fd7a7f837
```

The root commit contains no tracked `engine/certify` implementation. The only
inspected implementation is in the dirty auxiliary worktree. Its own source
says that the artifact is a simple zero of
\(\det(1-L_s^{\mathrm{sign}})\), not a zero or pole of \(\phi_q\)
(`.worktrees/aletheia-restore/engine/certify/certify.py:17-35,128-145,250-296`).
It also says that the Fredholm dimension tail is *validated, not proved*
(`.worktrees/aletheia-restore/engine/certify/certify.py:37-45`). A no-write q=12
auxiliary-evaluator probe returned:

```text
stock_engine_q12_status=REJECTED
stock_engine_exception=NotImplementedError: even q transfer operator not generalized; reference plugin supports q=3 and odd q>=5
stock_engine_wall_s=0.000013
```

That exception is exactly the branch at
`.worktrees/aletheia-restore/engine/certify/certify.py:174-180`. The quoted
13-microsecond value is warm in-process branch latency after import, not
standalone CLI wall time.

### 0.4 Reuse of the boundary-RATE Arb/Ford evaluator

The existing evaluator was rerun without its writing CLI. Although tagged as
the q=12 test, the function is deliberately q-independent.

```text
$ PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python -B - <<'PY'
import importlib.util, time
from pathlib import Path
from flint import ctx
ctx.prec=300
p=Path('research_notes/rh_goals_2026-08-14/lane_g/law_probes/kaggle_boundary_rate/boundary_rate_kernel.py')
spec=importlib.util.spec_from_file_location('brk',p)
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
t0=time.perf_counter()
a=m.rigorous_segment_envelope('0.5',16384)
b=m.rigorous_segment_envelope('0.25',16384)
dt=time.perf_counter()-t0
print('test_label=q12_reuse_of_q_independent_Ford_envelope')
print('status='+a['status'])
print('prec_bits='+str(ctx.prec))
print('cells_per_segment='+str(a['cells']))
print('route_A_E_upper='+repr(a['E_interval'][1]))
print('route_B_E_upper='+repr(b['E_interval'][1]))
print('wall_s='+format(dt,'.6f'))
print('scope='+a['proof_scope'])
PY
test_label=q12_reuse_of_q_independent_Ford_envelope
status=RIGOROUS_ARB_FORD_ENCLOSURE
prec_bits=300
cells_per_segment=16384
route_A_E_upper=8.408224199432881
route_B_E_upper=8.228313336614521
wall_s=9.209192
scope=All finite one-cusp Hecke groups in width-one normalization; Arb covers the continuous t-segment, and Ford packing bounds the uncomputed double-coset series absolutely.
```

This is genuine continuous-segment evidence, but only on the absolutely
convergent right side \(\Re s=1.1\). Its implementation is the bound
\(12|M(s)|+|\phi_\infty(s)|\), not a narrow enclosure of the true \(\phi_q\)
(`law_probes/kaggle_boundary_rate/boundary_rate_kernel.py:6-31,70-148`). It
contains no phase information and cannot be continued across the full \(H_0\)
contour. Its cost therefore does not estimate a full-\(H_0\) winding.

### 0.5 q=12 full-\(H_0\) surrogate stress test

For a direct scale test, the q=12 even-sector builder used by the older
`certdcH_winding.py` was pointed at the actual full rectangle, with \(N=32\),
300-bit Arb, and eight initial segments (nine endpoint samples) per edge. The
binary64 endpoints are nominal approximations to the Arb geometry in §0.2. No
receipt file was written; `run_sector` was called directly.

```text
$ PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python -B - <<'PY'
import importlib.util, json, time
from pathlib import Path
from flint import ctx
ctx.prec=300
p=Path('research_notes/rh_goals_2026-08-14/lane_g/law_probes/certdcH_winding.py')
spec=importlib.util.spec_from_file_location('certdch',p)
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
m.Q=12; m.BUILDER=m.ZE; m.BUILDER_NAME='zeta_cert_rosen_even.cert_det'
m.RE_LO=.5; m.RE_HI=1.4999
m.IM_LO=17.743184079412835; m.IM_HI=19.742984079412835
m.N=32; m.INIT_V=8; m.INIT_H=8
print('TEST_LABEL=NOT_EVIDENCE_ENDPOINT_POLYGON_WRONG_FUNCTION')
print('q=12 N=32 prec_bits=300 init_v=8 init_h=8')
print('rectangle_re=[0.5,1.4999] rectangle_im=[17.743184079412835,19.742984079412835]')
out={'label':'NOT_EVIDENCE_ENDPOINT_POLYGON_WRONG_FUNCTION',
     'q':12,'N':32,
     'rectangle':{'re':[m.RE_LO,m.RE_HI],'im':[m.IM_LO,m.IM_HI]},
     'sectors':{}}
t0=time.time()
for sign in (1,-1):
    ts=time.time()
    try:
        out['sectors'][str(sign)]={'status':'SCOUT_ONLY','result':m.run_sector(sign)}
    except Exception as e:
        out['sectors'][str(sign)]={'status':'SCOUT_FAILED_NOT_CERTIFICATE',
                                  'wall_s':time.time()-ts,
                                  'exception':type(e).__name__+': '+str(e)}
out['total_wall_s']=time.time()-t0
print(json.dumps(out,indent=2))
PY
```

Its terminal tail was (the per-edge progress lines are omitted):

```text
TEST_LABEL=NOT_EVIDENCE_ENDPOINT_POLYGON_WRONG_FUNCTION
q=12 N=32 prec_bits=300 init_v=8 init_h=8
rectangle_re=[0.5,1.4999] rectangle_im=[17.743184079412835,19.742984079412835]

{
  "label": "NOT_EVIDENCE_ENDPOINT_POLYGON_WRONG_FUNCTION",
  "q": 12,
  "N": 32,
  "rectangle": {
    "re": [0.5, 1.4999],
    "im": [17.743184079412835, 19.742984079412835]
  },
  "sectors": {
    "1": {
      "status": "SCOUT_FAILED_NOT_CERTIFICATE",
      "wall_s": 151.50317391700082,
      "exception": "RuntimeError: det ball contains 0 at (0.5,18.680590329412837); tail*4=2.207e-02"
    },
    "-1": {
      "status": "SCOUT_FAILED_NOT_CERTIFICATE",
      "wall_s": 177.95572033299686,
      "exception": "RuntimeError: det ball contains 0 at (0.5,17.985347360662836); tail*4=7.515e-03"
    }
  },
  "total_wall_s": 329.45899654100504
}
```

This is **NOT EVIDENCE** for a zero or pole of \(\phi_{12}\): it evaluates the
wrong determinant, uses the unproved dimension-tail model, and its endpoint
only half-turn chain does not enclose segment interiors. The failures on
\(\Re s=1/2\) are also unsurprising because transfer determinants see
cusp-spectrum zeros which are absent from the scalar scattering divisor. What
the run does establish is an engineering fact: the current \(N=32\) surrogate
already consumes 5.49 minutes and fails before closing either contour.

For scale comparison, the theorem-grade q=7 R3B receipt records 192 accepted
closed arcs and

```text
gates.margins.total_chunk_wall_seconds=387908.974999943
gates.margins.total_chunk_runtime_seconds=441267.10927032103
```

(`lane_f/F7_R3B_ASSEMBLY_RECEIPT.json`; about 107.75 h of contour wall time and
122.57 h aggregate per-chunk runtime), on a tiny box rather than the nominal
\(0.9999\times1.9998\) full rectangle. These are aggregate chunk costs, not the
elapsed time of a parallel job. The receipt is historical and pins engine bytes
that have since drifted; it concerns a transfer determinant, not \(\phi_q\).
There is no honest extrapolation from either run to a true-\(\phi_q\),
full-\(H_0\) completion time.

## 1. Verdict

The finite-Hecke **pole/holomorphy gate is provable from the printed theory and
closes with `q_pole = q_divisor = 3`** for the trivial scalar scattering
coefficient on the full right \(H_0\) and the A0/Route-B right domains; the
reflected \(D_0\) piece follows under \(H_0(q)\). The asserted family-wide
nonvanishing gate is **FALSE**: Hejhal Theorem 7.11 says that the full rectangle
eventually contains a zero. The corrected proof is a dichotomy: a zero closes
the target immediately; otherwise nonvanishing is the contradiction hypothesis
under which the \(K_F\) harmonic argument runs. The remaining effective
obstruction is RATE/activation/monotonicity, not a finite-\(q\) pole divisor.

## 2. Exact gate inventory

Here “holomorphic on a closed set” is read, as the referee requires, as
holomorphic on an open neighborhood of that set.

The four execution notes predate this audit and correctly record the divisor
gate as open in their own ledgers. The `PROVED` upgrade below is a **new,
superseding deduction from the separately checked printed Hejhal sources in
§0.1 and §3**; it is not attributed to those execution notes.

| ID | exact assertion consumed | primary file:line | audit status |
|---|---|---|---|
| A0-HOL | A0 assumes both \(\phi_q\) and \(\phi_\infty\) holomorphic on \(\overline\Omega\), hence \(F_q=\phi_q-\phi_\infty\) holomorphic there; the two-constants step also assumes \(E_R(q)\le K_+\). | `R3_TRANSPORT_EXECUTION_SOL.md:1-12,75-97,167-185,383-405` | The implication is correct. The former `q_divisor` gap is `R3_TRANSPORT_EXECUTION_SOL.md:239-252`. It closes analytically in §3 below for all finite \(q\ge3\). |
| A0-SIDE/RATE | One family-uniform \(K_+\) bounds the three non-RATE sides and \(E_R(q)\le C_Rq^{-\alpha}\) on all of \(\Gamma_R\), with \(\alpha>0\). | `R3_TRANSPORT_EXECUTION_SOL.md:383-409`; strengthened constant in `KF_WALL_ATTACK_SOL.md:160-201` | \(K_+<117\) is proved in the later note. Positive RATE and its activation remain open. |
| old-RB-\(H_0\) | The old Route B assumes \(\phi_q\ne0\) on \(R^+=[1/2,3/4]\times[t_0-1/4,t_0+1/4]\). A boundary zero is already success. | `R3_ROUTE_B_TRANSPORT_SOL.md:91-126` | Correct for that old route, but **too narrow** for the rebuilt \(K_F\) wall. |
| KF-full-\(H_0\) | On \(H_0=[1/2,1.4999]\times[t_c-.9999,t_c+.9999]\), \(\phi_q\) is nonzero and holomorphic on a neighborhood; then \(\log\lvert\phi_q\rvert\) is harmonic and continuous. | `KF_WALL_ATTACK_SOL.md:298-314`; referee formulation `KF_WALL_REFEREE.md:92-103` | Holomorphy/no-poles is proved in §3. Nonvanishing is the contradiction hypothesis, not a family theorem. |
| KF-anchor | The first-stage anchor is active: \(\lvert\phi_q(a)\rvert>m_a/2\), \(m_a=.07843\). | `KF_WALL_ATTACK_SOL.md:443-452` | Separate RATE/activation gate; not a divisor issue. |
| KF-bound | Under full \(H_0\), the anchor, holomorphy, and reflection, the raw supremum satisfies \(\sup_{D_0}\lvert F_q\rvert<109\). | `KF_WALL_ATTACK_SOL.md:443-480`; referee confirmation `KF_WALL_REFEREE.md:183-209,392-426` | **PROVED CONDITIONAL IMPLICATION.** Correct notation: take the safe ledger constant \(K_F=109\), not \(K_F<109\). |
| finite-divisor | An activation \(q_{\rm divisor}\) makes the finite scattering coefficient pole-free on every transport domain. | `R3_TRANSPORT_EXECUTION_SOL.md:239-252`; `KF_WALL_ATTACK_SOL.md:614-680`; `R5_ASSEMBLY_EXECUTION_SOL.md:466-476` | The notes called this open. Printed theory closes the right-domain part with \(q_{\rm divisor}=3\); under \(H_0(q)\), (7.22) closes the finite-\(q\) mirrored \(D_0\) part, while `C0_TRANSPORT_CAMPAIGN_SOL.md:680-755` independently clears the theta denominator there. |
| R5-RATE | \(E_R(N)=\sup_{\Gamma_R}\lvert F_N\rvert\le C_RN^{-\alpha}\) must hold on the whole exact boundary with \(C_R>0,\alpha>0\), an activation, and boundary monotonicity. | `R5_ASSEMBLY_EXECUTION_SOL.md:28-64` | **CONJECTURAL / OPEN.** The current full-boundary rigorous envelope has \(\alpha=0\); this does not negate DH2's partial, conditional \(q^{-1.2}\) pieces, which do not assemble a full RATE theorem. |
| R5-\(H_0/K_F\) | Under zero-freeness on the full \(R_\delta^+\), the symbolic Hejhal constants give \(\sup_{D_0}\lvert\phi_N\rvert\le K_H\), hence \(\sup_{D_0}\lvert F_N\rvert\le K_F\). | `R5_ASSEMBLY_EXECUTION_SOL.md:105-133`; sixth-zero wall `KF_WALL_ATTACK_SOL.md:298-314,443-480` | This R5 instantiation is symbolic. The later sixth-zero kf-referee geometry has its own proved conditional \(K_F=109\) wall after anchor activation; that does not instantiate every older R5 constant. |
| mixing | Before substituting harmonic-measure lower bounds, \(E_R(N)\le K_+\) and \(K_+^{1-\nu_{\rm seed}}E_R(N)^{\nu_{\rm seed}}\le K_F\). | `R5_ASSEMBLY_EXECUTION_SOL.md:135-176` | The monotonic direction is proved there. The activation `N_monotone` remains undefined until positive RATE and all constants exist. |
| tail-monotone | A single strict crossing must be promoted to the whole integer tail, with all activations and the tail supremum proved. | `R5_ASSEMBLY_EXECUTION_SOL.md:466-487`; `DH2_RENEWAL_PROOF_SOL.md:696-732` | **CONJECTURAL / OPEN.** DH2's strict test is \(E_3(q)<0.6603\), but DH2, RATE, and the remaining R5 gates are unproved. |
| finite base | The older notes ask for artifact-level zero/pole certificates for every finite \(q\) below an analytic onset. | `KF_WALL_ATTACK_SOL.md:562-595`; `R3_ROUTE_B_TRANSPORT_SOL.md:747-794`; `R5_ASSEMBLY_EXECUTION_SOL.md:475-476` | After §3 proves \(P_q=0\), the remaining per-q task is a scalar-\(\phi_q\) zero count with boundary clearance. Current determinant boxes do not provide it. |

The old onset ledgers

\[
q_0=\max(12,q_{\rm RATE},q_A,q_C,q_{\rm divisor},q_{\rm monotone})
\]

and

\[
q_0=\max(12,q_{\rm RATE},q_{\rm divisor},q_{\rm transport},q_{\rm monotone})
\]

occur at `R3_ROUTE_B_TRANSPORT_SOL.md:583-592` and
`KF_WALL_ATTACK_SOL.md:652-661`. This audit removes only the divisor term; it
does not manufacture any of the other thresholds.

## 3. Printed-theory closure of the pole/holomorphy gate

### 3.1 Finite Hecke groups

For the width-one, one-cusp finite Hecke group with trivial character, the
scattering matrix is \(1\times1\), hence its determinant is the scalar
\(\phi_q\). In \(\Re s>1\), Hejhal's (7.5) gives the absolutely convergent
Dirichlet series

\[
 \phi_q(s)=\sqrt\pi\,\frac{\Gamma(s-1/2)}{\Gamma(s)}
 \sum_{[S]\backslash\mathcal G_q/[S],\ c\ne0}|c|^{-2s}.
\]

The series is holomorphic in \(\Re s>1\); its meromorphic continuation has the
standard constant-mode pole at the boundary point \(s=1\). More precisely in
the right half-plane, Proposition 12.5 factors

\[
 V_q(s)=q_c^{2s-1}\phi_q(s)
 \prod_{k=0}^{M_\epsilon}\frac{s-s_{k,q}}{1-s-s_{k,q}},
 \qquad |V_q(s)|\le1,                                      \tag{3.1}
\]

The printed proposition defines \(V_q\) analytic in \(\Re s\ge1/2\). Solving
the finite factorization for the scattering coefficient gives

\[
 \phi_q(s)=q_c^{1-2s}V_q(s)
 \prod_{k=0}^{M_\epsilon}\frac{1-s-s_{k,q}}{s-s_{k,q}}.       \tag{3.2}
\]

The \(s_k\) convention is the source's Claim 9.6 convention, invoked on printed
p. 156: these are all residual/small-\(L^2\)-eigenvalue parameters, real
\(s_{k,q}\in(1/2,1]\), with \(s_{0,q}=1\) for the trivial character. The local
source bridge is recorded at
`LAW_ROUTEB_CONDITIONAL_THEOREM.md:139-168`. Therefore (3.2), rather than
meromorphic continuation alone, proves that poles of \(\phi_q\) in
\(1/2<\Re s\le1\) can only occur at those real \(s_{k,q}\). Embedded cusp-form
eigenvalues do **not** enter this scalar scattering divisor.

Hejhal note 86 says \(\lambda_1>1/4\) for every finite Hecke group. Therefore
there are no positive small-eigenvalue parameters \(s_{k,q}\in(1/2,1)\); the
only right-half-plane scattering pole is the constant pole \(s=1\).

Critical-line regularity does not have to be assumed. Proposition 12.5 gives
\(V_q\) holomorphic there and \(\lvert V_q(1/2+it)\rvert=1\). Every \(s_{k,q}\)
is real and \(>1/2\), so both numerator and denominator of every finite factor
in (3.2) are nonzero on the high critical line, and their moduli agree.
Also \(\lvert q_c^{1-2s}\rvert=1\). Hence \(\phi_q\) is finite and nonzero there
and

\[
 \lvert\phi_q(1/2+it)\rvert=1.                              \tag{3.3}
\]

The full \(H_0\) has \(\Im s>17.7431840794\) by §0.2. The A0 sides have
\(\lvert t\rvert>6.567\) (`KF_WALL_ATTACK_SOL.md:108-124`), while the old
Route-B domains are centered at \(t_0\approx7.067\)
(`R3_ROUTE_B_TRANSPORT_SOL.md:84-100`). These right domains, including \(D_z\),
all lie in \(1/2\le\Re s\le3/2\), so \(s=1\) is outside each of them. Each
\(\phi_q\) is meromorphic, so its poles are locally discrete; compactness of a
pole-free closed right domain then supplies a q-dependent open pole-free
neighborhood, even though left-half-plane resonances certainly exist elsewhere.
Consequently:

> **Finite-Hecke holomorphy theorem.** For every finite Hecke index \(q\ge3\),
> \(\phi_q\) is holomorphic on an open neighborhood of the full \(H_0\), of the
> A0 domain \(\overline\Omega\), of \(D_z\), and of the old Route-B right
> domains. Thus one may take
>
> \[
> q_{\rm pole}=q_{\rm divisor}=3.
> \]

This uses the trivial scalar coefficient specified by the program. It is not
a statement about arbitrary characters or arbitrary entries of a multicusp
scattering matrix. Nor does it assert that the left half-plane is pole-free.
For the rebuilt disc \(D_0\), its right half lies inside full \(H_0\); under
\(H_0(q)\), the meromorphic scattering identity (7.22) maps any left-half pole
to a right-half zero, so nonvanishing transfers to pole-freeness on the
reflected left half. Hence no extra \(q_{\rm divisor}\) activation is needed in
that contradiction branch. This is conditional on the full \(H_0(q)\); it is
not an unconditional assertion about the left half-plane.

Theorem 12.9 is consistent with, but does not itself prove, this conclusion.
After note 86 its only exceptional point is \(s_0=1\); throughout full \(H_0\),
\(|s-1|>17.7431840794\). Hence its disc-exclusion hypothesis is automatically
satisfied, for example with the distinct theorem parameter
\(\delta_p=1\). The symbol \(\delta_p\) must not be confused with the rectangle
half-width \(0.9999\). The hidden constants in Theorem 12.9(b)--(d) remain a
family-uniform bound problem, but **divisor clearance does not**.

### 3.2 Theta endpoint

The endpoint used by the program is the \((\infty,\infty)\) entry

\[
 \phi_\infty(s)=
 \frac{\sqrt\pi\,\Gamma(s-1/2)\zeta(2s-1)}
      {\Gamma(s)\zeta(2s)(4^s-1)}.                            \tag{3.4}
\]

On the high full \(H_0\), the gamma factors are regular and \(4^s-1\ne0\).
The denominator \(\zeta(2s)\) could vanish only at
\(s=\rho/2\), where a nontrivial zeta zero satisfies
\(0<\Re\rho<1\), so

\[
 0<\Re(\rho/2)<1/2.                                         \tag{3.5}
\]

At the boundary \(\Re s=1/2\), \(\zeta(1+2it)\ne0\). Compactness then gives an
open pole-free neighborhood of the closed high rectangle. Therefore
\(\phi_\infty\) is holomorphic on the same full \(H_0\).

Two corrections are binding:

1. **FALSE:** “\(\rho/2\)-type scattering poles are exceptions in
   \(\Re s>1/2\).” **Corrected:** they lie strictly to the left of the critical
   line. Their reflected divisor points \((1+\rho)/2\) are zeros in the right
   half-plane. The sixth such theta zero is the intended anchor inside this
   \(H_0\).
2. Equation (3.6) is a global theta zero-count asymptotic with an unspecified
   \(O(\log T)\) constant. It supplies neither local full-\(H_0\) clearance nor
   a finite-\(q\), family-uniform divisor bound. The local pole conclusion here
   comes from the explicit formula (3.4), not from (3.6).

It follows immediately that

\[
 F_q=\phi_q-\phi_\infty
\]

is holomorphic on an open neighborhood of every audited right transport domain
for every finite \(q\ge3\). Under \(H_0(q)\), the same is true on the reflected
\(D_0\) used by the \(K_F\) wall. The theta entry is independently regular
there: `C0_TRANSPORT_CAMPAIGN_SOL.md:680-755` gives the square-cover
denominator-clearance pass and
\(K_{\infty,D_0}<1.867346<2\), summarized at
`KF_WALL_ATTACK_SOL.md:464-466`. Zeros of either summand do not obstruct
holomorphy of the difference; poles would, and have been excluded as just
specified.

## 4. Nonvanishing is a contradiction branch, not a family gate

The proposed assertion

\[
 \phi_q(s)\ne0\quad\text{on full }H_0
 \quad\text{for every sufficiently large }q                 \tag{4.1}
\]

is **FALSE**. Hejhal Theorem 7.11 proves its negation: for the fixed
\(t_c\) and \(0<0.9999<1\), full \(H_0\) contains a zero of \(\phi_q\) for every
sufficiently large finite \(q\) (with an ineffective onset in the printed
proof).

The correct logic is:

\[
\begin{array}{c}
\phi_q\text{ has a zero in full }H_0
\end{array}
\quad\Longrightarrow\quad
\text{target obtained},                                    \tag{4.2a}
\]

while

\[
 H_0(q):\ \phi_q\ne0\text{ on full }H_0                    \tag{4.2b}
\]

is assumed only in the complementary contradiction branch. By §3, there are
already no poles. Hence under (3.2b), \(\log|\phi_q|\) is harmonic and
continuous on a neighborhood of the full closure, exactly as the kf-referee
requires. If the \(K_F\)+RATE inequalities then contradict (3.2b), a zero is
forced. No proof of eventual nonvanishing is needed or possible.

This also separates the functions correctly:

- \(\phi_q\) must be nonzero only to define the harmonic logarithm;
- \(F_q=\phi_q-\phi_\infty\) must be holomorphic for two-constants and maximum
  principles, but it is not required to be nonzero;
- \(\phi_\infty\) deliberately has the right-half-plane theta zero used by the
  Rouché/defect argument.

## 5. Correct per-\(q\) certified computation

Analytic pole-freeness reduces the finite computation to a **zero-count
dichotomy**, not an undifferentiated “no-zeros-no-poles” test. For a fixed
finite \(q\), a referee-grade certificate should do the following.

1. **Exact geometry.** Encode \(q\),
   \(\lambda_q=2\cos(\pi/q)\), \(t_c=t_6-0.050005\), and the four sides of
   \(H_0\) in Arb. A boundary zero is success, not a failed control.
2. **Evaluate the correct object.** Supply a certified meromorphic-continuation
   evaluator for the scalar \(\phi_q\): either a Fourier/scattering linear solve
   with explicit truncation and conditioning bounds, or a proved Selberg-zeta
   ratio including all elementary factors, branch continuation, denominator
   clearances, and a theorem-level Fredholm dimension tail. A raw
   transfer-operator determinant is not a substitute.
3. **Closed-segment enclosure.** Adaptively subdivide each oriented side. On
   every entire segment, use an Acb Taylor/derivative enclosure to prove
   \(0\notin\phi_q(S_j)\). Endpoint samples alone are insufficient. Any
   missing denominator, residual, branch, or tail clearance is
   **`UNVERIFIABLE`**, never evidence.
4. **Argument principle.** Enclose each argument increment and isolate the
   integer

   \[
     W_q=\frac1{2\pi i}\int_{\partial H_0}\frac{\phi_q'(s)}{\phi_q(s)}\,ds
        =Z_q-P_q.                                             \tag{5.1}
   \]

   The boundary must be certified nonzero. Section 3 supplies \(P_q=0\), so
   \(W_q=Z_q\ge0\). Thus \(W_q=0\) certifies the contradiction hypothesis for
   this q; \(W_q>0\) certifies the desired zero directly. A winding of zero
   **without** the independent pole theorem would prove only \(Z_q=P_q\), not
   \(Z_q=P_q=0\).
5. **Controls and receipt.** Repeat at larger truncation and precision; record
   code hash, precision, every segment ball, minimum boundary modulus lower
   bound, maximum tail upper bound, winding interval, isolated integer, and
   wall/CPU time. Deliberately weakened \(N\) or precision must fail cleanly.

### 5.1 Current computability verdict

The boundary-RATE evaluator is fast and rigorous for its actual task (9.21 s
for two 16,384-cell segments), but it proves only a q-independent absolute
envelope on \(\Re s=1.1\). The Dirichlet series is not absolutely convergent on
the portions of \(\partial H_0\) with \(\Re s\le1\), and the kernel supplies
neither phase nor a whole-contour continuation evaluator. It therefore cannot
be reused as a winding oracle.

The repo's R3B machinery contains the right *shape* of local tools--Acb
determinants, adaptive contour subdivision, and argument increments--but the
available implementations certify a different function and retain an unproved
dimension-tail premise. The inspected stock `engine/certify` wrapper rejects
even q=12; the separate older `zeta_cert_rosen_even` builder accepts q=12 but
has the wrong target and no proved dimension tail. That older surrogate failed
the nominal \(H_0\) stress test after 329.46 s at \(N=32\), before completing
one sector; the historical q=7 receipt reports over 107 aggregate chunk-hours
for a theorem-grade small-box determinant contour. Therefore:

> **Current honest cost assessment.** A true-\(\phi_{12}\), full-\(H_0\) winding
> is mathematically finite and certifiable in principle, but it is **not
> presently computable by a theorem-valid repo evaluator at any defensible
> quoted budget**. A new evaluator/identification and proved continuation tail
> are prerequisites. Extrapolating the present small-box determinant timings
> to \(H_0\) would be numerology.

Per-\(q\) certification remains useful only for a finite block whose upper end
is supplied independently. It cannot replace the analytic RATE proof for an
infinite tail or discover its onset by exhaustive search.

## 6. Gate-closure ledger

| item | verdict | consequence / remaining cost |
|---|---|---|
| Meromorphic continuation of finite \(\phi_q\) | **PROVED FROM PRINTED THEORY** | Standard scattering continuation; (7.5) supplies the initial half-plane. |
| No finite-\(q\) poles on full \(H_0\) or the A0/Route-B right domains | **PROVED FROM PRINTED THEORY** | Proposition 12.5/Claim 9.6 + note 86 leave only \(s=1\) on the closed right half-plane at these heights. Take \(q_{\rm pole}=q_{\rm divisor}=3\). |
| \(\phi_\infty\) pole-free on full \(H_0\) | **PROVED FROM PRINTED THEORY** | Explicit formula; \(\rho/2\) poles lie left of \(\Re s=1/2\), and the remaining elementary poles are outside the high rectangle. |
| \(F_q=\phi_q-\phi_\infty\) holomorphic on audited right domains | **PROVED** | Difference of the preceding holomorphic functions. Reflected \(D_0\) is conditional on full \(H_0(q)\) via (7.22), plus the independent C0 theta-cover clearance. The separate A0/R5 divisor activation is removed in that branch. |
| “\(\rho/2\) is a possible right-half-plane pole” | **FALSE** | Negation proved by \(0<\Re\rho<1\Rightarrow\Re(\rho/2)<1/2\). The reflected point is a zero. |
| \(\phi_q\ne0\) on full \(H_0\) for every large q | **FALSE** | Hejhal Theorem 7.11 proves eventual zeros. Correct use: contradiction hypothesis / case split. |
| Harmonic \(K_F\) wall | **PROVED CONDITIONAL IMPLICATION** | Under the nonzero branch and anchor activation, raw \(\sup\lvert F_q\rvert<109\); take safe \(K_F=109\). The full width, not old Route B's strip, is mandatory. |
| Theorem 12.9 exceptional-disc gate | **PROVED / AUTOMATIC HERE** | Only \(s_0=1\); full \(H_0\) is more than 17.743 away. This does not instantiate the hidden family constants in 12.9(b)--(d). |
| Direct per-q full-\(H_0\) zero count | **PROVABLE BY COMPUTATION AFTER A NAMED BUILD** | Needs a true scalar-\(\phi_q\) evaluator, theorem-level tail, and segment-interior Acb bounds. Current completion cost is unknown; q=12 surrogate failure cost was 329.46 s and is `NOT EVIDENCE`. |
| Existing `hecke_transfer_operator_zero` / R3B boxes close the gate | **FALSE** | Wrong function; root wrapper absent, q=12 unsupported by the inspected stock wrapper, dimension tail unproved there, and historical boxes are tiny/off-target. The older even-q builder runs q=12 but does not cure those mathematical gaps. |
| Mixing-direction lemma | **PROVED** | Given the two inequalities in R5 (1.11), lower harmonic-measure substitutions are valid. |
| Activation of the two mixing inequalities (R5 (1.11)) | **PROVABLE BY FINITE ARITHMETIC ONCE RATE EXISTS; CURRENTLY UNDEFINED** | With explicit \(C_R,\alpha,q_{\rm RATE},K_+,K_F,\nu_{\rm seed}\), solve and round strict thresholds upward. This closes only the local mixing-direction activation, not boundary monotonicity or the whole-tail supremum. |
| Positive full-boundary RATE and whole-tail monotonicity | **GENUINELY OPEN** | Current rigorous campaign proves only \(\alpha=0\); R5/DH2 cannot activate. |
| Effective analytic \(q_0\) and finite-base coverage | **GENUINELY OPEN** | Removing \(q_{\rm divisor}\) does not define \(q_{\rm RATE}\), \(q_{\rm monotone}\), the anchor onset, or a certified finite block. |

**Bottom line.** The holomorphy/no-pole gate was a removable bookkeeping gap,
and printed theory removes it uniformly for all finite \(q\ge3\). Universal
nonvanishing was never a legitimate gate: it is contradicted by the theorem the
program is effectivizing. The remaining pincer is still open because positive
RATE, its activations, whole-tail monotonicity, and a true finite-\(q\)
scattering evaluator are absent.

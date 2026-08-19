# Q7 R5 — Clause-1 operator binding and common continuation

**Status: PROOF CLAIM — AWAITING COLD REFEREE**

This note closes only the q=7 operator-binding/common-continuation implication
identified as Link 4b.  It does not promote q=7 to the LAW, does not promote a
Selberg zero, and does not replace the assembly-level ledger.

## Source and receipt boundary

The primary source for the abstract transfer operator is Mayer–Mühlenbruch–
Strömberg (MMS), arXiv:0912.2236v2, 15 March 2010, DCDS 32 (2012),
2453–2484: <https://arxiv.org/pdf/0912.2236v2>.  The supplied SHA-256 of that
version is
`a10020bd084534dc60fc3e887958f1583f2fc115d567961b461df1a59b32e072`.
The relevant source locations are MMS pp. 15, 20–21, 28–29: (26)–(27),
Theorem 4.10, Lemma 5.1, (34), Theorem 6.4, and Remark 4.  MMS is used here
for the operator formulas, the P-reduction, nuclear continuation, and the
factorization statement only.  MMS does **not** identify a Python engine with
its operator, does **not** state the Hilbert/Banach common-continuation lemma
proved below, and Remark 4 expressly withholds a general q>3 transfer-
eigenfunction/automorphic-function correspondence.  No scattering, parity,
or automorphic-function claim is made here.

The machine inputs are the supplied q=7 files
`f7_certify_tb_blocks.py`, `f7_source_builder.py`, `f7_r3b_engine.py`,
`zeta_cert_rosen_q5.py`,
`f7_receipts/F7_TB_BLOCK_CERTIFICATES_RECEIPT.json`, and
`f7_receipts/F7_E1_ENLARGED_CONTRACTION_V2_RECEIPT.json`.  The TB receipt
binds its 19-block source to
`f7_tb_disc_sweep.py` with SHA-256
`b8e693376369e44085d88925fc635ce32004173efed46ffed95e04c1c897241f`.
The source bytes read for this note have SHA-256 values

| file | SHA-256 |
|---|---|
| `f7_source_builder.py` | `038bcb49d3df00cfd4e1fb4aafca46a4e11e34f6b18300c07d4666be51bf45c6` |
| `f7_r3b_engine.py` | `661a4d2b132d1821d18499a302f58805bf7565e560d8f1520379dde156bc7d1a` |
| `zeta_cert_rosen_q5.py` | `c84c5c3f6d9f7a320bca7f1dbfd96a4859c3eea9b3de5420eb4eb223ad0d597b` |
| `f7_certify_tb_blocks.py` | `9c17cd7ce42c7d41e6d811eb2b8ecf3ced88b8d89e6b411b4cd19aaf7b5c80b1` |
| `f7_certify_r3b_flagship.py` | `df9873d9f1e47c47f2e846d38d906f8f77619a17871e6d7c6da8c225bb63f687` |

The supplied 16-chunk q=7 audit reports `chunk_count=16`, one embedded hash
for each of the five files above, and `embedded_matches_live=True` for every
listed file.  That audit is provenance evidence, not a fresh Kaggle run in
this note.  The live generic `zeta_cert_rosen.py` path has SHA-256
`965c2e5f65ae88b458d79bc425375e31589dcbf50703173664ef0e30901dceac`, which
differs from the certified generic-engine bytes.  It is not used to infer the
binding: the value builder uses the q5 primitives in the hashed
`zeta_cert_rosen_q5.py` and its own explicit q7 19-call assembly.

The root occurrence audit supplied with this lane is quoted exactly:

```text
q=7 h=2 kappa=5 twoh=4
expected_atomic_calls= 19
source_atomic_calls= 19
receipt_atomic_calls= 19
source_equals_eq34_instantiation= True
receipt_equals_eq34_instantiation= True
source_equals_receipt= True
heads= 9 tails= 10
```

The receipt fields, rather than decimal re-computation, control all certified
numeric/status assertions below.  Upper bounds are rounded up; lower bounds
and margins are rounded down.

## The q=7 discs and branch convention

Set

\[
 \lambda_7=2\cos(\pi/7),\qquad h_7=2,\qquad
 \kappa_7=2h_7+1=5.
\]

These values are MMS's odd-q relation (q=2h_q+3), specialized to q=7, and
are also the `Q`, `HQ`, and `KAPPA` constants in
`f7_certify_tb_blocks.py:47-55`.

For a finite digit string define the exact finite λ-CF value

\[
 [a_1,\ldots,a_r]_{\lambda}:=x_0,
 \quad x_r=0,\quad x_{t-1}=-\frac1{a_t\lambda+x_t}.
\]

Thus the exact partition points used by
`f7_certify_tb_blocks.py:79-97` are

\[
\begin{aligned}
 \phi_0&=-\lambda_7/2, &
 \phi_1&=[1,1]_{\lambda_7}, &
 \phi_2&=[1,2,1,1]_{\lambda_7},\\
 \phi_3&=[1]_{\lambda_7}, &
 \phi_4&=[2,1,1]_{\lambda_7}, &
 \phi_5&=0.
\end{aligned}
\]

Equivalently, this is the source's formula
\(\phi_{2i}=[1]^{h_7-i}[2][1]^{h_7}\) and
\(\phi_{2i+1}=[1]^{h_7-i}\), with empty digit string equal to zero.  Put

\[
 c_j=\frac{\phi_{j-1}+\phi_j}{2},\qquad
 h_j=\frac{\phi_j-\phi_{j-1}}2,
 \qquad R_j=a_jh_j,
\]

where the **exact rational decimal strings** in
`F7_TB_BLOCK_CERTIFICATES_RECEIPT.json` are

\[
 (a_1,a_2,a_3,a_4,a_5)=(3.522,2.622,2.372,1.79,1.6).
\]

Here \(D_j=D(c_j,R_j)\) and \(D_{-j}=-D_j\) in the unreduced MMS space.
The certified TB receipt records the corresponding Arb balls (384-bit,
M=512):

```text
lambda = [1.80193773580483825247220 +/- 4.64e-24]
source_radii =
  [0.174393823623839918698224 +/- 1.85e-25],
  [0.144100222333087263908995 +/- 4.83e-26],
  [0.162557120697671468351865 +/- 3.51e-25],
  [0.177265726454669764037377 +/- 1.52e-25],
  [0.285516694313767555115520 +/- 3.93e-25]
```

The receipt's older preparation factors in the manifest are not used; the
five exact strings above are the sole radius binding for this note.

For \(n\ge1\), define the two branch maps and weights

\[
\begin{array}{ll}
 \theta_{+n}(z)=-1/(z+n\lambda_7),
 &w_{+n,s}(z)=((z+n\lambda_7)^2)^{-s},\\[2mm]
 \theta_{-n}(z)=1/(z-n\lambda_7),
 &w_{-n,s}(z)=((z-n\lambda_7)^2)^{-s}.
\end{array}
\]

The power is the principal power of the squared denominator.  This is MMS's
convention in the proof of Lemma 5.1: on a positive branch use
\(\Re(z+n\lambda_7)>0\), and on a negative branch use
\(\Re(n\lambda_7-z)>0\).  Since
\((z-n\lambda_7)^2=(n\lambda_7-z)^2\), the latter fixes the same principal
sheet without replacing the composition (1/(z-n\lambda_7)) by its negative.
This distinction is essential: the unreduced p. 15 notation and the reduced
p. 21 notation must not be conflated.

## 1. Admissibility of the five discs

The TB receipt records q=7, \(\kappa=5\), the five exact factors, 19 source
occurrences, and `all_head_and_deep_tail_terms_pass=true`,
`all_pole_clearances_pass=true`, and `all_branch_cut_clearances_pass=true`.
It records

```text
rho_star = [0.763212029206899202166157 +/- 1.41e-25]
certification_verdict = PASS_RHO_LT_0.80
```

The TB receipt's certified upper endpoint is conservatively rounded up to
0.763213, still below its receipt threshold 0.80.

The tail part of that receipt is not a heuristic infinite scan.  For each
tail family it individually certifies the finite head and uses the centered
deep-tail bound

\[
 \frac1{n\lambda_7-|c_i|-R_i}+|c_j|,
\]

whose supremum is at the first omitted index.  Therefore every branch in the
19-row list below is holomorphic on its source disc, maps its source disc
strictly inside the stated target disc, and has a pole/cut-free principal
weight.  This is exactly the disc admissibility required in MMS Lemma 4.4,
not an appeal to q-independence.

For smoothing, the E1 receipt records 19/19 blocks, the rule
`e_B=min(clearance_B/4,0.15*R_i)`, all enlarged-contour ratios strictly below
one, and

```text
eta_max_upper_bound = 0.8695652173913044   (rounded UP)
rho_hat_upper_bound = 0.9152411837446922  (rounded UP)
rho_hat_worst_block = 5→3, +1, head
verdict = PASS_RHO_HAT_LT_1
```

Its smallest remaining pole/cut clearance lower endpoint is
`0.9915072451437825...`, hence the conservative lower-rounded value used here
is `0.9915`.  Thus each branch extends holomorphically to an enlarged source
disc and its image remains in a compact subset of the target disc.  The
receipts establish the numerical premise; the operator consequences are the
elementary composition-operator argument used in §5 below.

## 2. MMS (34) at q=7, plus sector, and the 19 occurrences

MMS (34) for \(q=2h_q+3>5\) gives, after setting \(h_q=2\) and
\(\kappa_q=5\),

\[
\begin{aligned}
 (L_{s,+}g)_1&=L_{+2,s}g_4+L^\infty_{+3,s}g_5
                 +L_{-1,s}g_4+L^\infty_{-2,s}g_5,\\
 (L_{s,+}g)_2&=L^\infty_{+2,s}g_5
                 +L_{-1,s}g_4+L^\infty_{-2,s}g_5,\\
 (L_{s,+}g)_i&=L_{+1,s}g_{i-2}+L^\infty_{+2,s}g_5
                 +L_{-1,s}g_4+L^\infty_{-2,s}g_5,
                 \qquad 3\le i\le5.
\end{aligned}
\]

Here \(L_{+n,s}\) is one branch at \(+n\), \(L_{-n,s}\) is one branch at
\(-n\), and \(L^\infty_{+n,s}\) (respectively \(L^\infty_{-n,s}\)) is the
sum over \(\ell\ge n\) with the corresponding branch convention above.  The
coefficient on every negative-index term is \(+1\), because this is the MMS
`+` sector.  The source uses `sgn=CERT.acb(sign)` and the certified call is
`sign=1`.

The following table is the binding.  “Tail start” means the full tail begins
at that integer; it is not merely the first Hurwitz term.  Repeated
output/input pairs are retained as separate occurrences.

| # | output (i) | input (j) | branch / tail start | sector coefficient | MMS term | source-builder call |
|---:|---:|---:|---|---:|---|---:|
| 1 | 1 | 4 | (+2), head | (+1) | (L_{+2,s}g_4) | `f7_source_builder.py:77` |
| 2 | 1 | 5 | (+\ell, \ell\ge3), tail (n_0=3) | (+1) | (L^\infty_{+3,s}g_5) | `:78` |
| 3 | 1 | 4 | (-1), head | (+1) | (L_{-1,s}g_4) | `:79` |
| 4 | 1 | 5 | (-\ell, \ell\ge2), tail (n_0=2) | (+1) | (L^\infty_{-2,s}g_5) | `:80` |
| 5 | 2 | 5 | (+\ell, \ell\ge2), tail (n_0=2) | (+1) | (L^\infty_{+2,s}g_5) | `:82` |
| 6 | 2 | 4 | (-1), head | (+1) | (L_{-1,s}g_4) | `:83` |
| 7 | 2 | 5 | (-\ell, \ell\ge2), tail (n_0=2) | (+1) | (L^\infty_{-2,s}g_5) | `:84` |
| 8 | 3 | 1 | (+1), head | (+1) | (L_{+1,s}g_1) | `:86` |
| 9 | 3 | 5 | (+\ell, \ell\ge2), tail (n_0=2) | (+1) | (L^\infty_{+2,s}g_5) | `:87` |
| 10 | 3 | 4 | (-1), head | (+1) | (L_{-1,s}g_4) | `:88` |
| 11 | 3 | 5 | (-\ell, \ell\ge2), tail (n_0=2) | (+1) | (L^\infty_{-2,s}g_5) | `:89` |
| 12 | 4 | 2 | (+1), head | (+1) | (L_{+1,s}g_2) | `:91` |
| 13 | 4 | 5 | (+\ell, \ell\ge2), tail (n_0=2) | (+1) | (L^\infty_{+2,s}g_5) | `:92` |
| 14 | 4 | 4 | (-1), head | (+1) | (L_{-1,s}g_4) | `:93` |
| 15 | 4 | 5 | (-\ell, \ell\ge2), tail (n_0=2) | (+1) | (L^\infty_{-2,s}g_5) | `:94` |
| 16 | 5 | 3 | (+1), head | (+1) | (L_{+1,s}g_3) | `:96` |
| 17 | 5 | 5 | (+\ell, \ell\ge2), tail (n_0=2) | (+1) | (L^\infty_{+2,s}g_5) | `:97` |
| 18 | 5 | 4 | (-1), head | (+1) | (L_{-1,s}g_4) | `:98` |
| 19 | 5 | 5 | (-\ell, \ell\ge2), tail (n_0=2) | (+1) | (L^\infty_{-2,s}g_5) | `:99` |

The nine head rows and ten tail rows are exactly the receipt/source audit
quoted above.  This proves item (2) of the claim by a literal specialization
of MMS (34), not by the q=5 layout or by a generic-loop label.

## 3. Exact action on normalized monomials

Let

\[
 e_{j,k}(w)=\left(\frac{w-c_j}{R_j}\right)^k,
 \qquad u=\frac{z-c_i}{R_i},\qquad z=c_i+R_i u.
\]

For one occurrence \(i\leftarrow j\) and branch \(\varepsilon n\), direct
substitution gives

\[
 (T_{\varepsilon n,s}^{i\leftarrow j}e_{j,k})(c_i+R_i u)
 =w_{\varepsilon n,s}(c_i+R_i u)
 \left(\frac{\theta_{\varepsilon n}(c_i+R_i u)-c_j}{R_j}\right)^k.
\]

`zeta_cert_rosen_q5.py:270-288` constructs the right side as an `acb_series`
in \(u\), starting at \(k=0\) and multiplying by the normalized input base.
Therefore the list returned by `_single_block_allcols(...,N)` has column (k)
equal to the normalized Taylor series of \(T e_{j,k}\), and its coefficient of
\(u^m\) is the coefficient of \(e_{i,m}\).  The q=7 wrapper passes the exact
q=7 centers, radii, λ, branch, and n at
`f7_source_builder.py:61-64`.

For a tail beginning at \(n_0\), the normalized input monomial has the finite
binomial identity

\[
 \left(\frac{\theta_{\varepsilon\ell}(z)-c_j}{R_j}\right)^k
 =R_j^{-k}\sum_{m=0}^{k}{k\choose m}(-c_j)^{k-m}
       \theta_{\varepsilon\ell}(z)^m.
\]

For both signs, after factoring the squared weight,

\[
 w_{\varepsilon\ell,s}(z)\theta_{\varepsilon\ell}(z)^m
 =(\lambda_7^2)^{-s}\left(-\frac1{\lambda_7}\right)^m
 \begin{cases}
 (\ell+z/\lambda_7)^{-(2s+m)},&\varepsilon=+,\\
 (\ell-z/\lambda_7)^{-(2s+m)},&\varepsilon=-.
 \end{cases}
\]

Consequently, on the initial absolute-convergence domain

\[
 \Omega_0=\{s:\Re s>1/2\},
\]

the full tail is exactly

\[
 (\lambda_7^2)^{-s}R_j^{-k}
 \sum_{m=0}^k {k\choose m}(-c_j)^{k-m}
 \left(-\frac1{\lambda_7}\right)^m
 \zeta(2s+m,a_\varepsilon(u)),
\]

where

\[
 a_+(u)=n_0+\frac{c_i+R_i u}{\lambda_7},\qquad
 a_-(u)=n_0-\frac{c_i+R_i u}{\lambda_7}.
\]

The series is absolutely and locally uniformly convergent there because
\(2\Re s+m>1\) for every \(m\ge0\).  This is the full tail, not only its
center term.  `zeta_cert_rosen_q5.py:291-318` computes the same formula:
`Z[m]` contains the Hurwitz series for (m=0,ldots,N-1), and column (k)
contains every (m=0,ldots,k).  The q=7 wrapper's
`inf_block` (`f7_source_builder.py:66-73`) first adds the head terms
(\ell=n_0,ldots,n_0+n_{\rm head}-1), then adds the Hurwitz tail beginning
at (n_0+n_{\rm head}).  Their union is exactly all \(\ell\ge n_0\), with
no omission or duplicate.  The identity is proved first on \(\Omega_0\);
the Hurwitz expression then supplies the meromorphic continuation.

## 4. The finite matrix identity

Let \(P_N\) retain normalized Taylor modes \(0\le k<N\) on each of the five
discs.  Order rows by \((i,m)\) and columns by \((j,k)\), with index
((i-1)N+m) and ((j-1)N+k).  `f7_source_builder.py:101-110` writes

\[
 M_N(s)_{(i,m),(j,k)}=[u^m]\bigl((L^H_{s,+}e_{j,k})_i(c_i+R_i u)\bigr),
\]

after accumulating the 19 occurrences in the table.  Hence, as an exact
finite-dimensional identity,

\[
 M_N(s)=\left.P_NL^H_{s,+}P_N\right|_{\operatorname{ran}P_N},
 \qquad
 \det_{5N}(I_{5N}-M_N(s))
 =\det_{\operatorname{ran}P_N}
   \left(I-P_NL^H_{s,+}P_N\right).
\]

This is the only finite determinant identity asserted here.  In particular,
\(\det_{5N}(I-M_N(s))\) is **not** identified with
\(\det_H(I-L^H_{s,+})\) at finite (N).  Any finite-to-infinite zero argument
belongs to the separately receipted q=7 contour/homotopy chain and is not
silently substituted for the operator identity proved in §5.

## 5. Common continuation of the Hilbert and MMS realizations

Let

\[
 B=\bigoplus_{j=1}^{5}B(D_j),\qquad
 H=\bigoplus_{j=1}^{5}H^2(D_j),
\]

where \(B(D_j)\) is holomorphic in \(D_j\), continuous on its closure, with
the sup norm, and \(H^2(D_j)\) is the Hardy space in the normalized variable.
The inclusion \(B\subset H\) is continuous.  Let \(L^{MMS}_{s,+}\) denote
the operator defined by MMS (34) on \(B\), and let \(L^H_{s,+}\) denote the
same 19 branch/tail formulas on \(H\), with tails represented by the exact
Hurwitz expressions of §3.

### 5.1 Equality on the absolute-convergence region

On \(\Omega_0\), §3 proves that every Hurwitz tail equals its absolutely
convergent branch sum.  The TB and E1 receipts prove the common five-disc
domain, pole/cut exclusion, and strict image contraction.  Thus the two
operators have literally the same action on \(B\), and \(L^H_{s,+}\) maps
\(H\) into \(B\): on an enlarged source disc the composition argument lies in
a target subdisc with ratio at most the E1 upper-rounded
\(\widehat\rho=0.9152411837446922<1\), while the weight is holomorphic and
bounded.  The Hardy reproducing-kernel estimate gives, for
\(f\in H^2(D_j)\),

\[
 |f(c_j+R_jv)|\le (1-|v|^2)^{-1/2}\|f\|_{H^2(D_j)},
 \qquad |v|\le\widehat\rho.
\]

The finite heads are immediate.  For tails, the exact head-plus-Hurwitz split
and the binomial formula in §3 give a locally uniform column estimate on every
compact \(K\Subset\Omega^*\):

\[
 b_k(s)\le A_K\widehat\rho^{k}
       +C_K k\widehat\rho^{k-1},
 \qquad s\in K,
\]

where \(b_k\) is the sum of the H-column norms over the five output discs,
\(A_K\) bounds the finitely many Hurwitz-closed center columns, and \(C_K\)
comes from the first-moment remainder.  The latter is finite because, on
\(K\),
\(\sum_{\ell\ge n_0}\ell^{-(2\inf_K\Re s+1)}\) converges; the (m=0)
Hurwitz term is kept as one closed tail and is not incorrectly replaced by
that sum.  Since \(\widehat\rho<1\),

\[
 \sup_{s\in K}\sum_{k\ge0}b_k(s)<\infty.
\]

The normalized monomials are an orthonormal Hardy basis, so this column-sum
bound makes \(s\mapsto L^H_{s,+}\) a locally uniformly trace-class (hence
holomorphic trace-class) family on \(\Omega^*\).  On \(\Omega_0\), the MMS
Theorem 4.10 statement gives that \(L^{MMS}_{s,+}\) is nuclear of order zero.

If \(L^H_{s,+}v_0=\lambda v_0\) with \(\lambda\ne0\), then
\(v_0=\lambda^{-1}L^H_{s,+}v_0\in B\).  For a Jordan chain,
\((L-\lambda)v_r=v_{r-1}\) gives
\(v_r=\lambda^{-1}(Lv_r-v_{r-1})\), so induction puts the full chain in
\(B\).  Conversely \(B\subset H\).  Therefore the two realizations have the
same nonzero eigenvalues with algebraic multiplicity on \(\Omega_0\).

The trace-class Fredholm determinant on \(H\) and the order-zero nuclear
determinant on \(B\) are their genus-zero spectral products.  The preceding
Jordan-chain equality makes those products identical on \(\Omega_0\):

\[
 \det_H(1-L^H_{s,+})=\det_B(1-L^{MMS}_{s,+}),
 \qquad s\in\Omega_0.
\]

No finite determinant is used in this equality.

### 5.2 Analytic continuation to \(\Omega^*\)

Set

\[
 \Omega^*=\{\Re s>1/2\}\ \cup\ \{\Re s>0,\ \Im s>1\}.
\]

The E1 bounds keep the branch weights holomorphic on the fixed enlarged discs.
The Hurwitz expressions are meromorphic only at the real points
\(s=(1-k)/2\), (k=0,1,2,\ldots), as in MMS Theorem 4.10.  None of these
points belongs to \(\Omega^*\).  The local column estimate above therefore
gives analyticity of \(s\mapsto\det_H(1-L^H_{s,+})\) on \(\Omega^*\), while
MMS Theorem 4.10 gives analyticity of
\(\det_B(1-L^{MMS}_{s,+})\) there after removal of its real pole lattice.
The two open sets in the definition of \(\Omega^*\) overlap, so \(\Omega^*\)
is open and connected.  The identity theorem extends the equality from the
nonempty open set \(\Omega_0\) to all of \(\Omega^*\):

\[
 \boxed{\det_H(1-L^H_{s,+})=\det_B(1-L^{MMS}_{s,+})\quad(s\in\Omega^*).}
\]

This is the claimed common continuation.  It is a paper proof instantiated
at q=7; it is not a claim that MMS itself supplied the Hilbert realization or
the Python correspondence.

## Obligations and blast-radius ledger

| item | status in this note | boundary |
|---|---|---|
| Five-disc q=7 admissibility | **PROOF CLAIM**, receipt-backed | TB/E1 receipts remain the numerical authority; no rerun was launched. |
| MMS (34) `+` sector to 19 occurrences | **PROVED by literal specialization** | The 19-row table and source call lines are binding; occurrence multiplicity is preserved. |
| Normalized monomial action and Hurwitz tails | **PROVED** | Equality to the actual infinite tail is first on \(\Re s>1/2\); continuation uses the Hurwitz formula. |
| Finite matrix | **PROVED** | Only \(M_N=P_NL^HP_N\) and its finite determinant are asserted; no finite/infinite determinant conflation. |
| Hilbert/Banach determinant equality on \(\Omega^*\) | **PROOF CLAIM** | Awaits cold referee review of the column-sum estimate, standard spectral-product facts, and source conventions. |
| R2 receipt `analytic_linkage=UNPROVEN` | **UNCHANGED** | This note does not edit or relabel the receipt; the paper claim is the proposed repair. |
| Generic `zeta_cert_rosen.py` drift | **DISCLOSED** | Its live bytes are not used to bind q=7. |
| MMS PDF banking | **CAVEAT** | URL and supplied SHA are recorded; no PDF bytes are added by this deliverable. |
| Selberg-zero, scattering, automorphic, LAW, or parity promotion | **WITHHELD** | Those claims remain assembly/ledger work and are outside this note's sole downstream corollary. |

The only downstream corollary asserted here is: **Link 4b is closed
conditional on cold confirmation of this proof claim and the cited receipts.**

**READY FOR COLD REFEREE**

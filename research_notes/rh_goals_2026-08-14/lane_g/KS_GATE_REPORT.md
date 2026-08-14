| pin id | q | s value | K_s-zero distance | verdict |
|---|---:|---|---:|---|
| g5_pin_1 | 5 | 0.453895180075 + 5.763537241730i | 0.455100243722 | CLEAR |
| g5_pin_2 | 5 | 0.410543735496 + 7.819768247017i | 0.705687094273 | CLEAR |
| g5_pin_3 | 5 | 0.399820892950 + 11.664755512714i | 0.406161547373 | CLEAR |
| g5_pin_4 | 5 | 0.447082980719 + 12.079716368844i | 0.660692931995 | CLEAR |
| g5_pin_5 | 5 | 0.469055256719 + 12.785854147381i | 0.534642160416 | CLEAR |
| g5_pin_6 | 5 | 0.485274314326 + 13.565375308892i | 0.713418914915 | CLEAR |
| g5_pin_7 | 5 | 0.400438577366 + 15.147872264096i | 0.768806823233 | CLEAR |
| g5_pin_8 | 5 | 0.444480984099 + 16.487520683785i | 0.70464781709 | CLEAR |
| q4_pin_1 | 4 | 0.250000000000 + 7.067362570867i | 0.257450593538 (box) | CLEAR |
| q4_pin_2 | 4 | 0.250000000000 + 10.511019819387i | 0.30929736861 (box) | CLEAR |
| q4_pin_3 | 4 | 0.250000000000 + 12.505428789965i | 1.7700259411 (box) | CLEAR |
| q6_pin_1 | 6 | 0.250000000000 + 7.067362570867i | 0.265407074794 (box) | CLEAR |
| q6_pin_2 | 6 | 0.250000000000 + 10.511019819425i | 1.00077882077 (box) | CLEAR |

# K_s definition and source

The local extraction is sufficient for the over-counting context and the factorization, but it does not contain Section 6.2. I therefore used the primary MMS arXiv PDF, §6.2, equations (42)-(43), Lemma 6.3, Proposition 2, and Remark 4. The local extraction records the same context at `/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/research_notes/MMS_0912.2236_EXTRACTION.txt:26-35`.

MMS identify the duplicated orbit as the two points `r_q` and `-r_q`, subtract the `O_+` contribution, and define `K_s = L_s^{O_+}`. In the paper's notation the inverse branches are `theta_n(z) = -1/(z+n lambda_q)` and `(L_{n,s}g)(z) = (theta_n'(z))^s g(theta_n(z))`. The source locations are §6.2 eqs. (42)-(43), PDF text lines 2861-2894; the determinant reduction is Lemma 6.3, lines 3313-3326; the spectrum is Proposition 2, lines 3415-3425. See [MMS arXiv PDF](https://arxiv.org/pdf/0912.2236).

Writing `h=h_q`, the complete component definition from equations (42)-(43) is as follows. For even `q=2h+2`, on `B_h`,

`(K_s g)_i=L_{1,s}g_{i+1}` for `1<=i<=h-1`, and ` (K_s g)_h=L_{2,s}g_1`.

For odd `q=2h+3` with `q>=5`, on `B_{2h+1}`,

`(K_s g)_i=L_{1,s}g_{i+1}` for `1<=i<=h`; `(K_s g)_{h+1}=L_{2,s}g_{h+2}`;

`(K_s g)_{h+i}=L_{1,s}g_{h+i+1}` for `2<=i<=h`; and `(K_s g)_{2h+1}=L_{2,s}g_1`.

For q=5, `h_q=1`, so equation (43) is the explicit three-cycle

`(K_s g)_1 = L_{1,s}g_2`, ` (K_s g)_2 = L_{2,s}g_3`, ` (K_s g)_3 = L_{2,s}g_1`.

Lemma 6.3 gives, for odd q, `det(1-K_s) = det(1-L_{1,s}^{h_q} L_{2,s} L_{1,s}^{h_q-1} L_{2,s})`; therefore q=5 reduces to `A_s=L_{1,s}L_{2,s}L_{2,s}`.

# Derived determinant and zero lattice

Let `M_n = [[0,-1],[1,n lambda_q]]`, the Möbius matrix of `theta_n`. For q=5 the argument map of `A_s` is `psi = theta_2 o theta_2 o theta_1`, with matrix `M_2 M_2 M_1`. Using `lambda_5^2=lambda_5+1`, the matrix is

`M_2 M_2 M_1 = [[-2 lambda_5, 1-2 lambda_5^2], [4 lambda_5^2-1, 4 lambda_5^3-3 lambda_5]]`.

Its determinant is 1 and its trace is

`tau_5 = 4 + 3 lambda_5`, `lambda_5 = 2 cos(pi/5) = (1+sqrt(5))/2`.

`ell_5 = (tau_5 - sqrt(tau_5^2-4))/2 = 0.11442064802926044`,

the attracting multiplier's positive square root. The scalar composition operator therefore has eigenvalues `ell_5^(2s+2n)`, n=0,1,..., exactly the Proposition 2 spectrum after the Lemma 6.3 reduction. Thus

`det(1-K_s) = product_{n>=0} (1 - ell_5^(2s+2n))`.

Writing `a_5=-log(ell_5)=2.167873726556495`, a zero satisfies `exp(-2 a_5 (s+n))=1`, hence the exact lattice is

`s = -n + i*pi*k/a_5`, for `n=0,1,2,...` and `k in Z`.

The vertical spacing is `1.44915850729921`. The exact intersection with the requested rectangle `Re in [0.35, 0.52], Im in [3.0, 17.5]` is `[]`: no K_s zeros.

For the q=4 and q=6 controls, the same reduction gives `ell_4=sqrt(2)-1` and `ell_6=2-sqrt(3)`, respectively. Their zero lattices have the same horizontal rows `Re(s)=-n`; only the vertical spacings differ.

# Per-pin justification

Distances for G5 are point-to-lattice Euclidean distances. For q=4/q=6, the reported distance is the distance from the entire closed winding box to the nearest lattice zero, so it is a box-level nonvanishing margin. The contamination tolerance is `1.0e-10`.

## g5_pin_1 (q=5)

- center: `0.453895180075 + 5.763537241730i`
- nearest center lattice zero: `(0.000000000000, 5.796634029197)` (n=0, k=4); center distance=`0.455100243722066`
- gated clearance (point): `0.455100243722066` to `(0.000000000000, 5.796634029197)`
- numerical product check: `|det(1-K_s)|=0.860347115852439` using 18 terms
- verdict: **CLEAR**

## g5_pin_2 (q=5)

- center: `0.410543735496 + 7.819768247017i`
- nearest center lattice zero: `(0.000000000000, 7.245792536496)` (n=0, k=5); center distance=`0.705687094272593`
- gated clearance (point): `0.705687094272593` to `(0.000000000000, 7.245792536496)`
- numerical product check: `|det(1-K_s)|=1.14058694123124` using 18 terms
- verdict: **CLEAR**

## g5_pin_3 (q=5)

- center: `0.399820892950 + 11.664755512714i`
- nearest center lattice zero: `(0.000000000000, 11.593268058394)` (n=0, k=8); center distance=`0.406161547373054`
- gated clearance (point): `0.406161547373054` to `(0.000000000000, 11.593268058394)`
- numerical product check: `|det(1-K_s)|=0.831640701900586` using 18 terms
- verdict: **CLEAR**

## g5_pin_4 (q=5)

- center: `0.447082980719 + 12.079716368844i`
- nearest center lattice zero: `(0.000000000000, 11.593268058394)` (n=0, k=8); center distance=`0.660692931994847`
- gated clearance (point): `0.660692931994847` to `(0.000000000000, 11.593268058394)`
- numerical product check: `|det(1-K_s)|=1.08193792875555` using 18 terms
- verdict: **CLEAR**

## g5_pin_5 (q=5)

- center: `0.469055256719 + 12.785854147381i`
- nearest center lattice zero: `(0.000000000000, 13.042426565693)` (n=0, k=9); center distance=`0.534642160416305`
- gated clearance (point): `0.534642160416305` to `(0.000000000000, 13.042426565693)`
- numerical product check: `|det(1-K_s)|=0.948653118478701` using 18 terms
- verdict: **CLEAR**

## g5_pin_6 (q=5)

- center: `0.485274314326 + 13.565375308892i`
- nearest center lattice zero: `(0.000000000000, 13.042426565693)` (n=0, k=9); center distance=`0.713418914914677`
- gated clearance (point): `0.713418914914677` to `(0.000000000000, 13.042426565693)`
- numerical product check: `|det(1-K_s)|=1.08342694350818` using 18 terms
- verdict: **CLEAR**

## g5_pin_7 (q=5)

- center: `0.400438577366 + 15.147872264096i`
- nearest center lattice zero: `(0.000000000000, 14.491585072992)` (n=0, k=10); center distance=`0.768806823233028`
- gated clearance (point): `0.768806823233028` to `(0.000000000000, 14.491585072992)`
- numerical product check: `|det(1-K_s)|=1.17226681391726` using 18 terms
- verdict: **CLEAR**

## g5_pin_8 (q=5)

- center: `0.444480984099 + 16.487520683785i`
- nearest center lattice zero: `(0.000000000000, 15.940743580291)` (n=0, k=11); center distance=`0.704647817090296`
- gated clearance (point): `0.704647817090296` to `(0.000000000000, 15.940743580291)`
- numerical product check: `|det(1-K_s)|=1.11059289832086` using 18 terms
- verdict: **CLEAR**

## q4_pin_1 (q=4)

- center: `0.250000000000 + 7.067362570867i`
- nearest center lattice zero: `(0.000000000000, 7.128855912765)` (n=0, k=2); center distance=`0.257451803446393`
- gated clearance (closed_winding_box): `0.257450593538093` to `(0.000000000000, 7.128855912765)`
- numerical product check: `|det(1-K_s)|=0.319209398183444` using 43 terms
- verdict: **CLEAR**

## q4_pin_2 (q=4)

- center: `0.250000000000 + 10.511019819387i`
- nearest center lattice zero: `(0.000000000000, 10.693283869148)` (n=0, k=3); center distance=`0.3093867867824`
- gated clearance (closed_winding_box): `0.309297368610159` to `(0.000000000000, 10.693283869148)`
- numerical product check: `|det(1-K_s)|=0.384971601255027` using 43 terms
- verdict: **CLEAR**

## q4_pin_3 (q=4)

- center: `0.250000000000 + 12.505428789965i`
- nearest center lattice zero: `(0.000000000000, 14.257711825531)` (n=0, k=4); center distance=`1.77002707231646`
- gated clearance (closed_winding_box): `1.77002594110062` to `(0.000000000000, 14.257711825531)`
- numerical product check: `|det(1-K_s)|=1.86605473677625` using 43 terms
- verdict: **CLEAR**

## q6_pin_1 (q=6)

- center: `0.250000000000 + 7.067362570867i`
- nearest center lattice zero: `(0.000000000000, 7.156476287341)` (n=0, k=3); center distance=`0.265407713647898`
- gated clearance (closed_winding_box): `0.265407074793774` to `(0.000000000000, 7.156476287341)`
- numerical product check: `|det(1-K_s)|=0.491115538129502` using 29 terms
- verdict: **CLEAR**

## q6_pin_2 (q=6)

- center: `0.250000000000 + 10.511019819425i`
- nearest center lattice zero: `(0.000000000000, 9.541968383122)` (n=0, k=4); center distance=`1.00078003887072`
- gated clearance (closed_winding_box): `1.00077882076971` to `(0.000000000000, 9.541968383122)`
- numerical product check: `|det(1-K_s)|=1.50797524695409` using 29 terms
- verdict: **CLEAR**

# MISSING / BLOCKED

No K_s definition or zero-set item remains unresolved. The local extraction does omit Section 6.2, so the exact definition was sourced from the fetched arXiv PDF as documented above. A shell `curl` attempt could not resolve `arxiv.org`; the browser fetch of the primary PDF succeeded. The receipt records this external-fetch dependency and the exact paper locations.

The numerical determinant values are supporting evaluations. The CLEAR verdicts come from the exact analytic zero lattice and the stated geometric margins, not from the finite product alone.

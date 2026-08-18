# M2 per-term transcription audit — Hejhal LNM 1001 Vol. 2, Ch. 6 §12

**Scope.** Primary-source audit of pp. 149–166 (the banked scan
research_notes/rh_goals_2026-08-14/lane_p/literature/Hejhal_LNM1001_Vol2_ch6s12_pp149-166.pdf),
covering Lemma 12.1, Lemma 12.2 (the displayed c1,...,c9 chain), Proposition
12.4, Propositions 12.5–12.8, and Theorem 12.9(a)–(d). Cross-checks are
LAW_HEJHAL_CH6S12_CH11S3_EXTRACT.md (including its audit-12 downgrade),
M2_FORD_PACKING_REFEREE.md, and theta-group equation (3.6).

**Status (2026-08-18).** The literal finite-`N` Lemma 7.7 constant is closed:

    C6(epsilon)=100[epsilon^(-1)+sqrt(1+epsilon^(-2))].

Lemma 12.2 is also closed here by an independent admissible instantiation of
`c1,...,c9`. The stronger statement “all Theorem 12.9 constants are explicit
and N-uniform” is **FALSE**: the scan leaves several O(.) constants, a finite
covering number, a low-height estimate, and the geometric/zero data
`(Gamma,chi,F,delta,omega)` unspecified. The corrected statement is:

> **SOURCE ROUTE / POTENTIALLY EFFECTIVE, FAMILY-UNIFORMITY OPEN.** The
> dependence on t,m,eta,omega(t) displayed below is explicit. The high-height
> prefactor can be reduced to one uninstantiated covering number; the
> low-height proof cites material outside the banked scan. Proving either
> prefactor uniform for the conjugated family G_N is an additional theorem,
> not present in §12. No normal-families argument occurs in §12; this does not
> make the hidden constants numeric or N-uniform.

All exact formula transcriptions below are from the rendered page images (the
scan OCR is visibly lossy); command receipts are retained before claims. No
tail sum is re-derived here.

## 1. Receipts

### R0 — source identity and page geometry

Command run:

    $ shasum -a 256 research_notes/rh_goals_2026-08-14/lane_p/literature/Hejhal_LNM1001_Vol2_ch6s12_pp149-166.pdf
    c0dee01cf83e45e5e489e25ea299ccb2ad3654659d284bd9abc031bc6570b62f  research_notes/rh_goals_2026-08-14/lane_p/literature/Hejhal_LNM1001_Vol2_ch6s12_pp149-166.pdf
    $ pdfinfo research_notes/rh_goals_2026-08-14/lane_p/literature/Hejhal_LNM1001_Vol2_ch6s12_pp149-166.pdf | rg 'Pages|Page size|Encrypted'
    Pages:           18
    Encrypted:       no
    Page size:       461 x 684 pts

The PDF pages map consecutively to printed pp. 149–166.

### R1 — raw OCR locators (not used to guess missing symbols)

Command run:

    $ src=research_notes/rh_goals_2026-08-14/lane_p/literature/Hejhal_LNM1001_Vol2_ch6s12_pp149-166.pdf
    $ for p in 1 2 5 8 13 14 16 18; do
    >   echo "---pdf-page-$p---"; pdftotext -raw -f "$p" -l "$p" "$src" - | sed -n '1,120p'
    > done
    ---pdf-page-1---
    149
    ...
    (12.1) )
    LEMMA 12.1. For ...
    ---pdf-page-2---
    150
    ...
    LEMMA 12.2. ... where A is some [positive] constant.
    ---pdf-page-5---
    153
    Consequently: ... Thus A = cge -5 ... PROPOSITION 12.4. ...
    ---pdf-page-8---
    156
    In other words: ... (1 + ... )B 2 ... PROPOSITION 12.5.
    ---pdf-page-13---
    161
    PROPOSITION 12.7. ... (iii) ... O(R 4) ...
    ---pdf-page-14---
    162
    PROPOSITION 12.8. ... O[(sigma-1/2)omega(t)] ...
    ---pdf-page-16---
    164
    THEOREM 12.9. ...
    ---pdf-page-18---
    166
    ... Assertion (c) follows immediately. Assertion (d) ...

Because this OCR drops inequality signs, Greek letters, and exponents, the
mathematical symbols below are transcribed from the rendered images, not
reconstructed from OCR.

### R2 — rendered-page audit

Exact in-memory rendering command and stdout receipt (no image file written):

    $ python3 -c 'import fitz,hashlib; p="research_notes/rh_goals_2026-08-14/lane_p/literature/Hejhal_LNM1001_Vol2_ch6s12_pp149-166.pdf"; d=fitz.open(p); [(lambda b,n: print(f"printed_page={n} png_bytes={len(b)} sha256={hashlib.sha256(b).hexdigest()}"))(d[i].get_pixmap(matrix=fitz.Matrix(2.2,2.2),colorspace=fitz.csGRAY,alpha=False).tobytes("png"),149+i) for i in (0,2,3,4,7,8,11,12,13,14,15,16,17)]'
    printed_page=149 png_bytes=68761 sha256=81ffaa71dfd6c5019fff3d8c825fe5ad65df5c48da168b91462d0c4792e7ffe7
    printed_page=151 png_bytes=63714 sha256=e6e9f796a5e0dcfd01f2fd5f7288f4e3a959fef2e431724217e940dfa1e3cace
    printed_page=152 png_bytes=62093 sha256=7363cb67b33251d6dff1289f4a4b8e3a677f5dfb7746ba5b443af6d93070b444
    printed_page=153 png_bytes=75792 sha256=061759f526b52138a2ea425b9230d559b54f182cc853c1d77c0e1935f8869488
    printed_page=156 png_bytes=58632 sha256=ab10066fb44a4833447d872518c1bfd5349ebeda5ffabc6f5b891f4d9b4aee89
    printed_page=157 png_bytes=100595 sha256=3afe6c128df77af675554399de634e867008db5e17abe5d74007b42d8b793665
    printed_page=160 png_bytes=73913 sha256=f2bc9f26fca45b241b5238652f34fe4f2770b6554599c89b57617ec135937b22
    printed_page=161 png_bytes=62378 sha256=5bbbae99f9db18402968840c1ecb32ab9186b2745956d0c0038532e2f1768eab
    printed_page=162 png_bytes=58934 sha256=034951556b6f5a8ae02ee4df5c54f374556f681d97c28ec7fbc104c4dce70fae
    printed_page=163 png_bytes=68609 sha256=3aa3651e05086bd7101ecab440943e0c033a99e385e13fd96a0340a9bc35e3ad
    printed_page=164 png_bytes=71928 sha256=db72c17529412a6ef90f11faefc6b2eef7471c6c000f1075d51db3adc68fc4fa
    printed_page=165 png_bytes=51172 sha256=78dde90e181f0f542ea0c06a2dc5cb0cc4217f3e9bdd48d0822a994226e3cabb
    printed_page=166 png_bytes=71628 sha256=05babbcb483623dc54333a35534913368588900773216bc335c830e603a94d10

These exact renders were visually inspected. In particular, p. 149 visibly
has `B>=5+y0` (not equality), and p. 164 has the two
`exp(3|t|+...)` and `exp(3|t|-2 pi y)` factors quoted below.

### R3 — extract and audit-12 correction

Command run:

    $ rg -n -C 2 "audit-12|Lemma 12\.1|Lemma 12\.2|Prop 12\.4|Props 12\.5|THEOREM 12\.9|Bonus \(3\.6\)|M2 consequence" research_notes/rh_goals_2026-08-14/lane_g/LAW_HEJHAL_CH6S12_CH11S3_EXTRACT.md
    18:> [CORRECTION 2026-08-18 audit-12] This line originally read "Every
    19-> constant in the chain is EXPLICIT (no normal-families step anywhere)".
    28:- Setup (12.1): B = 5 + y0, y0 >= 1000.
    29:- Lemma 12.1: |K_{s-1/2}(y)| <= 3 e^{-y}/sqrt(y) (1+1/sqrt(y)) ...
    31:- Lemma 12.2: ... >= A e^{-5 eta-5|t|} with A = c9 e^{-5};
    34:- Prop 12.4: |phi(s)| <= (1+sqrt(2)) B^2 ...
    38:- omega(r) = 1 + sum rho 2 eta/(eta^2+(r-gamma)^2) >= 1, integral omega = O(R^4).
    39:- THEOREM 12.9 ...
    47:M2 consequence: the Lemma-7.7/C6 tail majorant ... potentially effective ...
    55:> [CORRECTION 2026-08-18 audit-12] ... explicitness is a bookkeeping task not yet done.
    86:- Bonus (3.6): N[|gamma| <= T] = (4T/pi) ln(T sqrt(2)/(pi e)) + O(ln T) ...

The extract line 28 is corrected here to the source's B >= 5+y0 as verified
in R2; the extract's audit-12 downgrade itself is accepted.

### R4 — Ford referee cross-check (tail sum only; no re-summation here)

Command run:

    $ rg -n -C 2 "A_Gamma\(X\)|uniformity in N|sigma>1|full-series ceilings|Paper-proof|CONFIRMED" research_notes/rh_goals_2026-08-14/lane_g/M2_FORD_PACKING_REFEREE.md | head -120
    4:**Verdict:** **CONFIRMED — paper-level; Lean formalization open.** ...
    147:with A_Gamma(1)<=1, gives full-series ceilings 12 at sigma=1.1
    148:and 6 at sigma=1.25.
    232:**Bottom line:** retire G1/G2 ... Ford replacement is **CONFIRMED ... at paper level**;

The referee note's displayed paper-level estimate is
sum_{|c|>X}|c|^{-2 sigma} <= [sigma/(sigma-1)] X^{2-2 sigma} for sigma>1,
X>=1, with unit-cylinder/PSL constant independent of N after width-one
conjugation. This cumulative tail statement does not instantiate a §12
per-term prefactor.

### R5 — theta endpoint, equation (3.6)

Commands run:

    $ theta=research_notes/rh_goals_2026-08-14/lane_p/literature/Hejhal_LNM1001_Vol2_ch11s3_pp524-532.pdf
    $ shasum -a 256 "$theta"
    6deb4101e3f7470eb17f0c9f0fc83fb1e4e7459e6d1282c2aaf16e1d931afb2f  research_notes/rh_goals_2026-08-14/lane_p/literature/Hejhal_LNM1001_Vol2_ch11s3_pp524-532.pdf
    $ pdfinfo "$theta" | rg 'Pages|Encrypted|Page size'
    Pages: 9
    Encrypted: no
    Page size: 461 x 684 pts
    $ rg -n -C 2 "Bonus \(3\.6\)" research_notes/rh_goals_2026-08-14/lane_g/LAW_HEJHAL_CH6S12_CH11S3_EXTRACT.md
    86:- Bonus (3.6): N[|gamma| <= T] = (4T/pi) ln(T sqrt(2)/(pi e)) + O(ln T) — theta-group
    87-  scattering-zero count; feeds omega(t) bookkeeping if M2 transcription targets
    88-  the limit group.
    $ python3 -c 'import fitz,hashlib; p="research_notes/rh_goals_2026-08-14/lane_p/literature/Hejhal_LNM1001_Vol2_ch11s3_pp524-532.pdf"; d=fitz.open(p); b=d[4].get_pixmap(matrix=fitz.Matrix(2.2,2.2),colorspace=fitz.csGRAY,alpha=False).tobytes("png"); print(f"printed_page=528 png_bytes={len(b)} sha256={hashlib.sha256(b).hexdigest()}")'
    printed_page=528 png_bytes=68391 sha256=66c31aaf8bc00c5508210a48c4e996a4a6043c51dc088f930d11f98d389c34b0

The rendered printed p. 528 image shows

    N_theta(T) = N[|gamma| <= T]
                 = (4T/pi) log(T sqrt(2)/(pi e)) + O(log T).       (3.6)

The O(log T) coefficient is not printed. This is an endpoint asymptotic, not
an explicit pointwise upper bound for omega(t) and not a finite-N uniformity
theorem.

### R6 — family source locator

Command run:

    $ rg -n -C 2 "Hecke group G_N|N >= 3|N = infinity|conjugated model|G_N|lambda = 2" research_notes/rh_goals_2026-08-14/lane_g/LAW_HEJHAL_S7_EXTRACT.md | head -100
    19:- ... G_N = <E,S^lambda>, lambda = 2cos(pi/N), N >= 3, N = infinity allowed and G_infinity = theta group ...
    21-  Conjugated model G_N = a(1/sqrt(lambda)) G_N a(sqrt(lambda)), generators Q_N,S; ...
    24-  phi_N(s)=...sum_{W infinity in [S]\G_N/[S]} |c|^{-2s}, Re s > 1.

The family under audit is the width-one conjugated family G_N, including the
N=infinity theta endpoint. Lemma 7.2's C(epsilon) is N-independent, but this
does not uniformize §12's Gamma,F,delta,eta or hidden O constants.

### R7 — Lemma 7.7 is a different (whole-scattering) C6

Command run:

    $ pdftotext -layout -f 7 -l 7 research_notes/rh_goals_2026-08-14/lane_p/literature/Hejhal_LNM1001_Vol2_s7_pp568-600.pdf - | sed -n '1,220p'
    574
    LEMMA 7.7. For each epsilon > 0, there exists a positive constant C6(epsilon) ...
    (7.15)
    1 <     < 3
    Z=cr=Z             and          ItI > £
    Proof. Repeat the derivation of 155(12.2) with B 10 when N<00 ...

The OCR loses the displayed formula and equality sign. The rendered p. 574
image confirms `|phi_N(s)|<=C6(epsilon)`, `B=10`, and that this is the whole
coefficient `phi_N(s)`, not a Fourier/per-term `phi_m`. Solving the displayed
quadratic envelope in the proof gives the independently checkable route

    C6(epsilon) = 100 [ epsilon^{-1} + sqrt(1+epsilon^{-2}) ].

At epsilon=1 this is 100(1+sqrt(2)) = 241.4213562373095..., so the safe
rounded-UP integer ceiling is 242. This is a valid explicit whole-scattering
bound for Lemma 7.7; it is not the per-m C6-per-term bound in Theorem 12.9(c).

## 2. Primary-source transcription, pp. 149–153

### Setup (12.1), p. 149

The source fixes chi(S)=1 and defines

    B >= 5 + y0,       y0 >= 1000.                              (12.1)

The inequality B >= 5+y0 is visually unambiguous in R2. Neither a finite
upper bound for B nor a family choice of y0 is supplied.

### Lemma 12.1, p. 149

For 1/2 <= Re(s) <= 3/2 and y>0,

    |K_{s-1/2}(y)| <= [3 e^{-y}/sqrt(y)] [1+1/sqrt(y)].

The coefficient 3, strip endpoints 1/2 and 3/2, and y>0 are source-printed
numeric data (R0–R2). This Bessel estimate has no Gamma, chi, F, or N input
and is immediately N-uniform.

### Lemma 12.2, pp. 150–153

For s=1/2+h+it, 0<=h<=1, t real, eta>0,

    integral_eta^infinity |K_{s-1/2}(y)|^2 dy/y >= A exp(-5 eta-5|t|).  (12.2-L)

The source says only “A is some [positive] constant.” Its proof gives
A=c9 exp(-5), but no c9 value.

The c-chain is:

1. On p. 151 (eta>1 branch), the Sonine–Gegenbauer formula is used with
   nu=h+it, mu=it, x=eta. The source records
   K0(eta) >= c1 exp(-eta)/eta and
   |Gamma(1+it)| >= c2 exp(-pi|t|/2),
   “with absolute constants cj>0.” No values are printed.

2. Absorbing these constants, p. 152 introduces c3>0:
   c3 exp(-pi|t|/2) eta^(-h) exp(-eta)
   <= integral_eta^infinity |K_{s-1/2}(y)| y^(1-h) dy.

3. For T>=1+eta, Lemma 12.1 gives a c4>0 with
   c3 exp(-pi|t|/2) eta^(-h) exp(-eta) - c4 T^(1/2) exp(-T)
   <= integral_eta^T |K_{s-1/2}(y)| y^(1-h) dy.
   The intermediate coefficient 6 comes from 3(1+y^{-1/2})<=6 on this
   range; c4 itself is not evaluated in the source.

4. The next lower bound has the shape
   c3 exp[-pi(eta+|t|)/2]/(eta+|t|)^h - c4 T^(1/2) exp(-T).
   The source says “take T=2(eta+|t|+c5) with c5 approximately infinity,”
   and remembers 0<=h<=1. Thus c5 means sufficiently large, not a number.

5. The source then introduces c6>0:
   c6 exp[-2(eta+|t|+c5)]
   <= integral_eta^T |K_{s-1/2}(y)| y^(1-h) dy.

6. Cauchy–Schwarz on p. 153 gives
   integral_eta^T |K|^2 dy/y
   >= [c6 exp(-2(eta+|t|+c5))]^2/T^4
   >= c7 exp[-4(eta+|t|+c5)]/T^4,
   with c7>0 unnamed.

7. Enlarging the absolute choice of c5 absorbs T^-4 into one more
   exponential, introducing c8,c9>0:
   integral_eta^infinity |K|^2 dy/y
   >= c8 exp[-5(eta+|t|+c5)]
   = c9 exp(-5 eta-5|t|).
   For 0<eta<=1 the source shifts the lower limit to 1+eta. It concludes
   A=c9 exp(-5).

**Independent explicit instantiation (not printed by Hejhal).** A separate
Arb bookkeeping certificate instantiates

    c1=exp(-1), c2=1, c3=exp(-1), c4=9, c5=20,
    c6=1, c7=4, c8=1, c9=exp(-100), A=exp(-105).

The role-by-role choices are: c1=exp(-1) in the elementary K0 lower
bound, c2=1 in `|Gamma(1+it)|>=exp(-pi|t|/2)`, and c3=c1*c2=exp(-1).
For completeness, for `eta>=1`,

    K0(eta)=integral_0^infinity exp(-eta cosh u)du
      >= integral_0^(1/eta) exp[-eta(1+u^2)]du
      >= exp(-1)exp(-eta)/eta,

using `cosh u<=1+u^2` on `[0,1]`. Also

    |Gamma(1+it)|^2
      =2 pi |t| exp(-pi|t|)/(1-exp(-2 pi |t|))
      >= exp(-pi|t|),

with the value at `t=0` understood by continuity. These prove the stated
`c1,c2,c3`, rather than numerically sampling them.
For T>=1+eta, Lemma 12.1 gives
`6 integral_T^infinity exp(-y)y^(1/2)dy <= 9 sqrt(T) exp(-T)`, so c4=9.
Set `U=eta+|t|+20` and `T=2U` (thus U>=21 on the eta>1 branch). The
normalized tail/main ratio is the expression evaluated below and decreases
for U>=21; the `main` margin then permits c6=1. Cauchy–Schwarz with
`integral_eta^T y^(3-2h)dy <= T^4/4` gives c7=4. The `poly` margin allows
c8=1 after replacing `exp(-4U)/(4U^4)` by `exp(-5U)`. Finally,
`5c5=100` gives c9=exp(-100), and the source's eta<=1 lower-limit shift
gives A=c9 exp(-5)=exp(-105).

These values are a separate elementary/Arb bookkeeping certificate, not a
claim that the scan printed them. Exact command and output (Arb 160-bit
intervals) are:

    $ /Users/za/.venvs/farey-rh/bin/python -c 'from flint import arb, ctx; ctx.prec=160; pi=arb.pi(); alpha=arb(2)-pi/2; U=arb(21); c3=(-arb(1)).exp(); c4=arb(9); tail=(2*c4*arb(2).sqrt()/c3)*U.sqrt()*U*(-alpha*U).exp(); main=(c3/2)*(alpha*U).exp()/U; poly=U.exp()/(4*U**4); C61=100*(1+arb(2).sqrt()); A=(-arb(105)).exp(); print("alpha =",alpha); print("tail_ratio_U21 =",tail); print("main_over_expminus2U_U21 =",main); print("expU_over_4U4_U21 =",poly); print("C6_epsilon1 =",C61); print("A = exp(-105) =",A); [print(f"eta_{n} =", ((pi/n).tan()/40)) for n in (3,4,6,10,100)]'
    alpha = [0.42920367320510338076867830836024855790141530031 +/- 2.51e-48]
    tail_ratio_U21 = [0.8109506053764602677306223982496785788301119286 +/- 6.99e-47]
    main_over_expminus2U_U21 = [71.92382112914791045775875385987666380836670608 +/- 5.97e-45]
    expU_over_4U4_U21 = [1695.3015133653347849018655855138841134756665656 +/- 5.87e-45]
    C6_epsilon1 = [241.42135623730950488016887242096980785696718754 +/- 2.75e-45]
    A = exp(-105) = [2.5065674758999531731031572443379307585175264602e-46 +/- 2.54e-93]
    eta_3 = [0.043301270189221932338186158537646809173570131345 +/- 3.90e-49]
    eta_4 = [0.025000000000000000000000000000000000000000000000 +/- 9.32e-50]
    eta_6 = [0.014433756729740644112728719512548936391190043782 +/- 2.87e-49]
    eta_10 = [0.0081229924058226581538967853053783616238725867880 +/- 5.67e-50]
    eta_100 = [0.00078565665108377869547026581321540061389274795748 +/- 5.65e-51]

Here alpha=2-pi/2. The tail expression is the normalized tail/main
comparison after T=2U:
`(2 c4 sqrt(2)/c3) U^(3/2) exp(-(2-pi/2)U)`. It is decreasing for U>=21,
so the displayed interval is below 0.811<1 and gives tail < main. The `main`
interval is above 71.923>1 and gives
`(c3/2) exp(alpha U)/U > 1`, hence the remainder is at least exp(-2U). The
`poly` interval is above 1695.30>1 and gives `exp(U)/(4U^4)>1`; with the Cauchy denominator
`integral_eta^T y^(3-2h)dy <= T^4/4` this yields c7=4 and c8=1.
Together with T=2U and the eta<=1 lower-limit shift, c9=exp(-100) and
A=exp(-105). For the whole-scattering Lemma 7.7 value, the Arb interval
`C6_epsilon1` is below 241.422, so the safe integer bound is the upward
ceiling 242 (never a downward rounding). The source-level status remains
that c1,...,c9 are unnamed; these are an admissible replacement chain, not
recovered printed values.

The two further exact prefactors used below were also evaluated with the
approved Arb interpreter:

    $ /Users/za/.venvs/farey-rh/bin/python -c 'from flint import arb,ctx; ctx.prec=160; Cb=arb(2)+4*arb(2).log(); Ca0=arb(13).sqrt()/2; print("C_b = 2+4log(2) =",Cb); print("sqrt(13)/2 =",Ca0)'
    C_b = 2+4log(2) = [4.7725887222397812376689284858327062723020005374 +/- 4.29e-47]
    sqrt(13)/2 = [1.8027756377319946465596106337352479731256482869 +/- 2.36e-47]

## 3. Proposition 12.4 and the Blaschke chain, pp. 153–163

### Proposition 12.4, pp. 153–156

For 1/2<=Re(s)<=3/2 and |Im(s)|>=1, Green's identity and Parseval applied
to E0 yield

    |phi(s)| <= (1+sqrt(2)) B^2.                                (12.4)

More precisely, with `h=sigma-1/2`, the last displayed inequality on p. 155 is

    |phi(s)|^2 B^(-2h) <= B^(2h)+2h|phi(s)/t|.

Thus, for `|t|>=epsilon>0`, `0<=h<=1`, and `B>=1`, the positive root gives

    |phi(s)| <= B^2[epsilon^(-1)+sqrt(1+epsilon^(-2))].       (12.4-eps)

At `epsilon=1` this is `(1+sqrt(2))B^2`. The displayed coefficient is
absolute. A general upper choice of `B` is not printed, but the width-one
Hecke family admits the explicit choice in (12.7-Hecke) below.

### Proposition 12.5, pp. 156–157

For Re(s)>=1/2,

    V(s)=q_c^(2s-1) phi(s) product_{k=0}^{M_epsilon} (s-s_k)/(1-s-s_k),

where `q_c=min{|c|:c!=0}` (the subscript distinguishes this cusp parameter
from the Hecke index `N`).

The source proves |V(1/2+iu)|=1, |V(s)|<=1, V(conj(s))=conj(V(s)), and
sum_rho eta/(1+|gamma|^2)<infinity for rho=1/2+eta+i gamma, eta>=0.
The prefactor `q_c`, finite `M_epsilon`, and the zero set are not numeric in
§12. The exact bound `|V|<=1` is numeric and needs no zero-count constant.

### Proposition 12.6, pp. 157–160

The Hadamard/Blaschke factorization is

    V(s)=phi(1/2) exp[A(s-1/2)]
      product_j (s-rho_j)/(1-s-rho_j)
      product_{gamma>0}
      [(1-(s-1/2)/(eta+i gamma))(1-(s-1/2)/(eta-i gamma))]
      /[(1+(s-1/2)/(eta+i gamma))(1+(s-1/2)/(eta-i gamma))].

The source states absolute convergence away from the displayed zero/pole
locations and `A<=0`. The proof uses Hadamard degree `p=4` and then identifies

    A=2 log(q_c/q_1),       B_cubic=0.                          (12.6-AB)

For the trivial character, the first nonzero coefficient cannot cancel, so
`q_1=q_c` and hence `A=0`. No zero-count constant or finite-factor bound is
supplied. The
e^{-delta xi} sandwich is qualitative: for each fixed delta>0 it holds for
sufficiently large xi and forces B=0; it does not print a numeric delta.

### Equations (12.3)–(12.5), p. 160

    q_1=inf{x>0: sum_{|c|=x} chi(w0^{-1}) != 0,
                 w0 in Gamma_infinity\Gamma/Gamma_infinity}.   (12.3)

No numeric `q_1` or family-uniform lower bound is printed for a general
character. For the trivial-character Hecke family, `q_1=q_c`. The source sets

    V1(s)=q_1^(2s-1) phi(s) product_{k=0}^{M_epsilon}(s-s_k)/(1-s-s_k)
         =(q_1/q_c)^(2s-1)V(s),                                (12.4)

and obtains its zero product (12.5). The disjointness of the finite
divisor sets is qualitative.

### Proposition 12.7, pp. 161–162

For real r,

    omega(r)=1-V1'(1/2+ir)/V1(1/2+ir).

The source proves

    omega(r)>=1,  omega is even,
    integral_{-R}^R omega(r) dr = O(R^4) for R>=1,
    omega(r)=1+sum_rho 2 eta/[eta^2+(r-gamma)^2].          (12.7-P)

The numbers 1 and 4 and numerator 2 eta are explicit. The O(R^4)
coefficient is not supplied and depends on the zero set.

The proof also displays the following finite ledger before invoking the
zero-count estimate (notation `gamma` and `eta` is that of the zero set):

    integral_{-R}^R omega(r) dr
      <= 2R + 2 pi sum_{|gamma|<=2R} 1
         + 16R sum_{|gamma|>2R} eta/|gamma|^2.                   (12.7-ledger)

Thus the numerical coefficients 2, 2 pi, and 16 are source-visible, but the
finite zero count and the tail's weighted sum are still uninstantiated. This
is an explicit decomposition, not a tail-sum replacement for the requested
per-term bound.

### Proposition 12.8, pp. 162–163

For s=sigma+it, 1/2<=sigma<=3/2, |t|>=1,

    1-|phi(s)|^2 = O[(sigma-1/2) omega(t)].                  (12.8-P)

The source says the implied constant depends solely on Gamma and chi. In the
trivial-character width-one Hecke family it can in fact be instantiated.
Write `h=sigma-1/2`. The product on p. 163 gives exactly

    1-|V1(s)|^2 <= 2h omega(t).

Shimizu gives `1<=q_c`, while the generator `Q_N` gives `q_c<=lambda_N<=2`;
triviality gives `q_1=q_c`. Every exceptional factor dropped in the source is
at least one in modulus on the right half-strip. Therefore

    1-|phi(s)|^2
      <= 2h omega(t) + [1-q_c^(-4h)]
      <= (2+4 log 2) h omega(t),                               (12.8-Hecke)

using `1-exp(-x)<=x` and `omega(t)>=1`. This is an explicit N-independent
prefactor for the trivial-character family. For a nontrivial character,
`q_1` can cancel and the source supplies no uniform replacement.

### Equations (12.6)–(12.7), p. 163

    eta=(1/20) inf{Im(z): z in F}.                            (12.6)
    Im T(z) <= eta/2 for T in Gamma-[S] and y>=y0.             (12.7)

The factor 1/20, eta/2, and the y0 threshold are source-printed, but the
infimum over F and required y0 are not. For a width-one group, Shimizu's
`|c|>=1` gives, for every nonparabolic `T`,

    Im T(x+iy)=y/|c(x+iy)+d|^2 <= 1/(c^2 y) <= 1/y.

Consequently an explicit admissible choice is

    y0(eta)=max(1000,2/eta),    B(eta)=5+y0(eta).              (12.7-Hecke)

A “tiny” divisor-clearance `delta>0` is chosen for disjoint disks; no numeric
family choice is printed.

For the standard conjugated Hecke fundamental domain used in the family
cross-check, `lambda_N=2cos(pi/N)` and its lower corners give

    inf_F Im z=sqrt(lambda_N^(-2)-1/4)=(1/2)tan(pi/N),

hence

    eta_N = tan(pi/N)/40.

The Arb receipt in §2 evaluates eta_3, eta_4, eta_6, eta_10, eta_100; in
particular eta_N tends to 0 as N tends to infinity. Therefore the printed
factor `exp(5 pi |m|/eta_N)` and threshold `y>=10 eta_N` cannot be promoted to
a single finite N-uniform numerical majorant without an additional argument.
This geometric observation is a family obstruction, not a claim that §12
itself proves a uniform theorem.

## 4. Theorem 12.9 and the requested per-term majorant, p. 164

Take 1/2<=sigma<=3/2, retain |s-s_k|>=delta for 0<=k<=M_epsilon, and use
the s0 convention. The source states:

* (a) phi(s) is uniformly bounded.
* (b) 1-|phi(s)|^2 = O[(sigma-1/2)omega(t)].
* (c), for m != 0,

      |phi_m(s)| <= C12.9,c(Gamma,chi,F,delta)
                    sqrt(omega(t)) exp(3|t|+5 pi |m|/eta).     (C6-per-term)

* (d), for y>=10 eta,

      |E(z;s;chi)-y^s-phi(s)y^(1-s)|
        <= C12.9,d(Gamma,chi,F,delta)
           sqrt(omega(t)) exp(3|t|-2 pi y).                   (C6-E-tail)

The source says the implied constants depend solely on Gamma, chi, F, delta,
and are independent of m, sigma, t. It does not say the two implied
constants are equal. Their maximum may be named C6_src, but no numeric
value is printed. The explicit dependence on m,t,y,eta,omega(t) in these two
boxes is the strongest justified C6-type per-term statement. No tail sum is
performed.

For the trivial-character finite Hecke groups, the banked §7 note 86
(`lambda_1>1/4`) removes the exceptional `s_k` other than the constant mode
`s_0=1`. Then the definition of `V`, `q_c>=1`, and `|V|<=1` give

    |phi(s)| <= |s|/|s-1|.

On `|t|<=1`, `sigma<=3/2`, and `|s-1|>=delta`, this is at most
`sqrt(13)/(2delta)`. Combining it with Proposition 12.4 and (12.7-Hecke)
instantiates 12.9(a), under precisely that trivial-character/note-86 input,
as

    C12.9,a(eta,delta)
      = max{(1+sqrt(2))B(eta)^2, sqrt(13)/(2delta)}.            (Ca-Hecke)

Equation (12.8-Hecke) similarly instantiates 12.9(b) with the N-independent
prefactor `C12.9,b=2+4 log 2`; pointwise family control still requires a bound
for the varying function `omega_N(t)` itself.

### High-height reduction to one missing geometric constant

The independent `A=exp(-105)` above lets one carry the printed proof farther
than its O-notation. Define `k_N(eta)` to be the least cardinality in the
finite covering used verbatim on p. 164,

    [0,1] x [eta,y0] subset union_{j=1}^{k_N(eta)} T_j(F_B).

For the trivial-character finite Hecke group put

    B=B(eta)=5+max(1000,2/eta),
    C_phi,hi=(1+sqrt(2))B^2,
    C_b=2+4 log 2,
    D_N(eta)=(k_N(eta)+1)
       [2B^2 log B + C_b/2 + C_phi,hi].                       (E-ledger)

Indeed, p. 165 and (12.2) give the three bracketed contributions. Uniformly
for `0<=h<=1`,

    (B^(2h)-B^(-2h))/(2h) <= 2B^2 log B,
    (1-|phi|^2)B^(-2h)/(2h) <= (C_b/2)omega(t),
    |phi(s)|/|t| <= C_phi,hi                         (|t|>=1).

Since `omega>=1`, their sum is at most `D_N(eta)omega(t)`. Lemma 12.2 and
Parseval then give the explicit **conditional** high-height coefficient bound

    |phi_m(s)|
      <= exp(105/2)sqrt(D_N(eta)omega(t))
         exp[(5/2)|t|+5 pi |m| eta],              |t|>=1.     (C-high)

This is the sharper exponent actually visible in the last display on p. 166.
For finite Hecke `eta<=1`, weakening `(5/2)|t|` to `3|t|` and `eta` to
`1/eta` recovers the printed shape in 12.9(c), with conditional prefactor

    C12.9,c,high = exp(105/2)sqrt(D_N(eta)).                    (Cc-high)

This is not yet the requested function of `(eta,delta,omega)` alone:
`k_N(eta)` is asserted finite but never estimated in §12. Treating it as
uniform, or as a printed function of eta, is **CONJECTURAL**.

The same sharper bound and Lemma 12.1 give, for `y>=10eta`, the conditional
tail prefactor

    C12.9,d,high(eta)
      = [6 C12.9,c,high/sqrt(2 pi)]
        [1+1/sqrt(20 pi eta)]
        [exp(5 pi eta)+exp(-10 pi eta)/(1-exp(-15 pi eta))],  (Cd-high)

so the nonconstant Fourier sum is at most
`C12.9,d,high(eta)sqrt(omega(t))exp(3|t|-2 pi y)` for `|t|>=1`.
The two signs of `m` account for the factor 6. This is a summation of the
Fourier modes in 12.9(d), not a re-derivation of the already-closed Ford
double-coset tail.

The full 12.9(c),(d) constants still do not close: for `|t|<=1` p. 164 says
only “use the analog of (9.19),” which is not in the banked §12 scan, and the
dependence on the divisor clearance `delta` is not evaluated. Thus
`Cc-high`/`Cd-high` are proved conditional high-height ledgers, not full
Theorem 12.9 constants.

**Category warning.** Lemma 7.7 (p. 574) is a different statement:
|phi_N(s)|<=C6(epsilon) bounds the whole scattering coefficient, not each
Fourier coefficient phi_m. Its source proof explicitly repeats 155(12.2)
with B=10. The quadratic envelope gives

    C6(epsilon)=100 [epsilon^(-1)+sqrt(1+epsilon^(-2))].

At epsilon=1 this is 100(1+sqrt(2))=241.4213562373095..., so 242 is a
safe rounded-UP integer. This whole-coefficient bound is explicit for every
finite `N`, exactly the case for which p. 574 says to repeat (12.2) with
`B=10`. The theta endpoint is sent instead to pp. 527 and 508; p. 508 is not
banked here, so the same numeric endpoint bound is not independently
transcribed in this note. In either case, Lemma 7.7 does not instantiate
C12.9,c or C12.9,d.

### Equation (12.8), p. 166

The source's later product identity is

    phi(s)=q_1^(1-2s) phi(1/2)
      product_{k=0}^{M_epsilon}(1-s-s_k)/(s-s_k)
      product_j(s-rho_j)/(1-s-rho_j)
      product_{gamma>0}(s-rho)(s-conj(rho))
                         /[(s+conj(rho)-1)(s+rho-1)].          (12.8)

It adds no numeric constant; `q_1`, finite zeros, and the infinite zero product
remain group/character dependent.

## 5. Constant ledger and N-uniformity classification

The family is the width-one conjugated G_N of R6, including the N=infinity
theta endpoint. This table records what §12 proves.

| item | exact displayed data | status across G_N |
|---|---|---|
| (12.1),(12.7) | `B(eta)=5+max(1000,2/eta)` is admissible by Shimizu | explicit function of eta; not a single N-uniform number |
| Lemma 12.1 | coefficient 3, strip [1/2,3/2], y>0 | **UNIFORM** Bessel estimate |
| Lemma 12.2 | `c1=e^-1,c2=1,c3=e^-1,c4=9,c5=20,c6=1,c7=4,c8=1,c9=e^-100,A=e^-105` | **UNIFORM** admissible replacement chain; values are not source-printed |
| Prop. 12.4 | (12.4-eps) | coefficient uniform; substitute `B(eta)` |
| Props. 12.5–12.6 | `|V|<=1`, `p=4`, `A=2log(q_c/q_1)`, cubic `B=0` | trivial chi: `q_1=q_c`, so `A=0`; zero divisor varies |
| Prop. 12.7 | omega>=1 and (12.7-ledger) | **CONDITIONAL ON ZERO INPUT**: count and weighted tail vary |
| Prop. 12.8 / 12.9(b) | `C_b=2+4log2` for trivial chi | prefactor **UNIFORM**; `omega_N(t)` itself is not controlled |
| (12.6) | `eta_N=tan(pi/N)/40` for finite N | **GENUINELY VARIES** and tends to zero |
| 12.9(a) | (Ca-Hecke) | explicit in `(eta,delta)` under trivial chi + note 86 |
| 12.9(c), high | (Cc-high) | explicit except for `k_N(eta)`; pointwise factor also needs `omega_N(t)` |
| 12.9(d), high | (Cd-high) | inherits `k_N(eta)` and `omega_N(t)` |
| 12.9(c),(d), low | analog of (9.19) | **FAILED TRANSCRIPTION**: cited estimate is outside banked scan |
| theta (3.6) | (4T/pi)log(T sqrt(2)/(pi e))+O(log T) | endpoint asymptotic; O coefficient unspecified |

The Ford referee's A_Gamma(X)<=X^2 and
sum_{|c|>X}|c|^{-2sigma} <= [sigma/(sigma-1)]X^(2-2sigma) are paper-level
N-uniform cumulative tail controls after width-one conjugation (R4). They
do not bound C12.9,c/d, give a uniform eta_N, or give a uniform
omega_N zero count.

The classification requested in the task is therefore:

* **Automatic from width one / the fixed cusp:** the unit x-period,
  Shimizu `|c|>=1`, `q_c<=2`, (12.7-Hecke), Lemma 12.1, the replacement
  Lemma 12.2 chain, the quadratic coefficient in Proposition 12.4, and the
  trivial-character prefactor `2+4log2` in Proposition 12.8.
* **Conditional on the omega/zero input:** Proposition 12.7's `O(R^4)`, any
  pointwise family majorant for `omega_N(t)`, and hence the family use of
  12.9(b)–(d). Theta (3.6), with its hidden O coefficient, supplies neither a
  finite-N uniform zero count nor the weighted tail in (12.7-ledger).
* **Genuinely varying or missing:** `F_N`, `eta_N`, `B(eta_N)`, the cover
  `k_N(eta_N)`, the scattering divisor, and a general divisor clearance.
  At the theta endpoint the standard domain has a second cusp and
  `inf_F Im z=0`, so (12.6) gives `eta_infinity=0`; the scalar §12 formula
  cannot simply be substituted there. Scalar-entry/matrix/determinant
  compatibility is an additional endpoint obligation.

## 6. Corrected M2 conclusion

The transcription failed, or necessarily changed status, at exactly these
steps:

1. The printed `c1,...,c9` are unnamed. This note repairs that gap with an
   independently proved admissible chain and `A=exp(-105)`; it does not
   pretend to recover Hejhal's hidden choices.
2. Proposition 12.5 uses an unquantified large-half-plane bound,
   Phragmen--Lindelof, and Poisson--Jensen. The final `|V|<=1` is exact, but no
   numerical total for its zero sum is produced.
3. Proposition 12.7 invokes the order-four zero count with hidden coefficient
   and an uninstantiated weighted zero tail. Equation theta (3.6) has its own
   hidden O coefficient and covers only the endpoint asymptotic.
4. Proposition 12.8 is numerically repaired only for the trivial-character
   Hecke family (`2+4log2`). Cancellation in `q_1` leaves the general-character
   version open.
5. The proof of 12.9(c) asserts a finite cover of
   `[0,1]x[eta,y0]` but gives no cardinality. This is the precise unresolved
   `k_N(eta)` in (E-ledger); omitting it would be an invalid constant drop.
6. For `|t|<=1`, 12.9(c),(d) cite only an analog of (9.19), outside the banked
   scan. Consequently their `delta`-dependent low-height prefactors were not
   instantiated.
7. The standard finite-Hecke geometry has `eta_N=tan(pi/N)/40 -> 0`; at the
   two-cusp theta endpoint the same standard-domain infimum is zero. Therefore
   the requested full N-uniform 12.9 bound is **FALSE in this direct
   parametrization**. A corrected endpoint theorem needs a different cusp
   decomposition and the scattering-matrix/scalar-entry identification.
8. Lemma 7.7's `C6` is categorically the whole scattering coefficient, not a
   Fourier-mode majorant. Its finite-N constant is the explicit formula above;
   the endpoint proof cites an unbanked page.

Thus the literal finite-N Lemma 7.7 gate is **CLOSED**, the absolute
Lemma 12.2 gate is **CLOSED by replacement**, and the high-height per-mode
route is reduced to (Cc-high)/(Cd-high) with the named cover constant.
The full Theorem 12.9 per-mode certificate and its N-uniformity remain
**OPEN**, not merely “bookkeeping completed.” The Ford result separately
closes the cumulative geometric tail at paper level; no part of that tail
sum was redone here.

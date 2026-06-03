# THEORY_SCHEMA — Canonical recipe for "-1 among the non-residues"

Reconciliation of 4 independent derivations into ONE correct recipe.
All numbers RUN (python3 + mpmath/sympy); primary sources text-extracted in this dir.
Tags: [PROVEN] [NUMERICAL] [CONDITIONAL: GRH/LI or DRH] [CONJECTURAL].

Verification scripts (this dir): `canonical_verify.py` (claims 1-5, reproduces RS
0.99590/0.99906 to 5 dp), `canonical_ordering.py` (V(-1) largest, delta smallest,
q=7,11,19,23). Existing siblings: `why_minus1.py`, `cchi_parity.py`,
`compute_density_fm.py`, `anchor_fixed.py`, `sign_audit.py`.

================================================================================
## HEADLINE (adversarial honesty)
================================================================================
The claim "a=-1 DOMINATES / leads the non-residue hierarchy" is, for the standard
Rubinstein-Sarnak logarithmic sign-density delta, **FALSE — it is exactly backwards.**
The established theorem is the OPPOSITE:

  Fiorilli-Martin, Crelle 676 (2013), **Theorem 1.10** (VERBATIM, GRH+LI, FM_text.txt:325):
  "For any integer a != -1, delta(q;-1,1) < delta(q;a,1) for all but finitely many
   integers q with (q,a)=1 such that both -1 and a are nonsquares (mod q)."

=> a=-1 is the unique **LEAST-biased** non-residue vs the principal class. What -1
DOES maximize is the **VARIANCE** of the RS limiting distribution; larger variance
pulls delta toward 1/2, which is precisely why -1 LOSES the sign-density race.

The only true reading under which "-1 leads" is the AMPLITUDE / |D| reading
(largest typical excursion = largest variance), which is the same fact that makes
it lose the sign-density race.

================================================================================
## 1. CRUX: leading means tie across all non-residues [PROVEN classical / NUMERICAL]
================================================================================
RS limiting mean of the normalized error E(x;q,a) = -1 + #{b mod q: b^2=a, (b,q)=1}.
For EVERY non-residue this is -1 (no square roots). Verified q=3..24 (canonical_verify.py
Claim 1: all NR tie at -1). So the leading mean CANNOT discriminate among NR.
Equivalently, the head-to-head density delta(q;-1,a) for two distinct non-residues
is EXACTLY 1/2 (RS pairwise symmetry). The whole question lives at finer order.

================================================================================
## 2. THE FINER DISCRIMINANT = the RS COVARIANCE/VARIANCE (NOT skew, NOT DRH) [PROVEN]
================================================================================
RS covariance of the limiting vector (FM Def 1.3):
   Cov(X_a, X_b) = sum_{chi != chi0} c_chi * conj(chi(a)) * chi(b),
   c_chi = sum_{gamma: L(1/2+i gamma, chi)=0} 1/(1/4 + gamma^2)   [= FM b(chi)].
Race a-vs-1 variable D_a = X_a - X_1:
   Var(D_a) = V(q;a,1) = sum_{chi != chi0} c_chi |chi(a) - 1|^2.

EXACT combinatorial identity (canonical_verify.py Claim 2, RUN):
   sum_{chi != chi0} |chi(a) - 1|^2 = 2 phi(q)  for EVERY a != 1.
=> if c_chi were constant, ALL classes would tie in variance too. The discriminant
is therefore the **chi-dependence of c_chi**, and specifically its **PARITY split**.

WHY NOT SKEW: D_a = m + sum_k A_k cos(theta_k) with theta_k iid Uniform (LI) is
SYMMETRIC, so its skewness is identically 0 (skew_kurtosis.py). The "non-Gaussian
skew" hypothesis in the task brief is a DEAD END. The only non-Gaussian feature is
the (symmetric) kurtosis, a small same-sign secondary nudge; the dominant lever is
the variance.

WHY NOT AK/DRH MAGNITUDE: Aoki-Koyama (JNT 245, 2023) measure size-of-discrepancy
~ C loglog x on the p^{-1/2}-weighted scale. Their per-class tie-breaker is
m(a)=sum_{chi!=chi0} chi(a) * ord_{s=1/2} L(s,chi). Under expected Chowla
nonvanishing L(1/2,chi)!=0, every m_chi=0, so m(a)=0 for all a and the AK leading
hierarchy among non-residues is IDENTICALLY DEGENERATE (AK Cor 3.3 / Ex 3.5 prove
NRs are mutually unbiased to leading order; difference = bounded constant). AK do
NOT single out -1; -1-dominance is NOT a DRH-magnitude effect. (Numerically
verified L(1/2,chi)!=0 for q=3,5,7,11,13,23; q=5 quadratic L(1/2)=0.231751 smallest.)
AK and RS are logically independent notions (AK state this explicitly).

================================================================================
## 3. WHY a=-1 IS SPECIAL — the parity / log2 mechanism [PROVEN + NUMERICAL]
================================================================================
chi(-1) = +1 (even chi) or -1 (odd chi). So chi(-1)-1 = 0 (even) or -2 (odd):
**a=-1 places ALL of its |chi(-1)-1|^2 = 4 weight on ODD characters, zero on even.**
Any other NR spreads |chi(a)-1|^2 across both parities. (canonical_verify.py Claim 3:
even-weight = 0.000 ONLY for a=-1, for q=7,11,19,23.)

Two equivalent quantitative statements of "odd weighs more":
  (a) Archimedean: c_chi = log(q/pi) + psi((1+a_chi)/2) + 2 Re L'/L(1,chi),
      a_chi=parity (0 even, 1 odd). psi(1) = -gamma = -0.57722 (odd) vs
      psi(1/2) = -gamma-2ln2 = -1.96351 (even): odd c_chi larger by 2 ln2 = 1.38629
      from the Gamma-factor alone (canonical_verify.py Claim 4, RUN).
  (b) FM closed form (Thm 1.4, FM_text.txt:182): the parity term collapses to the
      indicator iq(-a*b^{-1}) log2; for b=1 it is iq(-a) log2 = log2 iff a == -1.
      Combinatorial check: -sum_chi |chi(a)-1|^2 chi(-1) = 2 phi(q) [a==-1]
      (canonical_verify.py Claim 3, equals 2phi only at a=-1, else 0).

NET: V(q;-1,1) carries an EXTRA +2 phi(q) log2 that NO other non-residue gets, so
V(q;-1,1) is the LARGEST among non-residues. RUN with realistic analytic c_chi
(canonical_ordering.py): -1 is rank 1/by-variance and rank-last-by-delta for
q=7 (V=3.727), 11 (11.55), 19 (55.27), 23 (54.62) — EVERY case.

VARIANCE -> DENSITY sign (sign_audit.py / FM Thm 1.1): delta = 1/2 + rho(q)/
sqrt(2 pi V) + O(V^{-3/2}), rho(q)=#real chars (SAME for all NR vs 1). Larger V =>
delta closer to 1/2 => SMALLER. Hence max variance <=> least-biased. QED for FM 1.10.

================================================================================
## 4. CLOSED-FORM VARIANCE [PROVEN formula, CONDITIONAL: GRH]
================================================================================
FM Thm 1.4 (arithmetic closed form, GRH):
   V(q;a,b) = 2 phi(q) [ Lambda(q) + Kq(a-b) + iq(-a b^{-1}) log2 ] + 2 M*(q;a,b),
   Lambda(q) = log( q / (2 pi e^{gamma0}) ) for prime q  [FM Def 1.5],
   Kq(n) = Lambda(q/(q,n))/phi(q/(q,n)) - Lambda(q)/phi(q),  0 <= Kq <= log2,
   iq(n) = 1 iff n == 1 (mod q),
   M*(q;a,b) = sum_{chi != chi0} |chi(a)-chi(b)|^2 Re L'/L(1, chi*)  (chi* = primitive inducer).
Asymptotically V(q;a,b) ~ 2 phi(q) log q.  The per-NR difference vs b=1 is carried by
Kq(a-1), the unique iq(-a)log2 (=log2 only for a=-1), and M*.

================================================================================
## 5. DENSITY RECIPE for delta(N;-1,a) — the computable object [VALIDATED]
================================================================================
Read "delta(N;-1,a)" precisely. TWO regimes:
 (A) NR-vs-NR (a,b both nonsquares): delta(N;-1,a) = 1/2 EXACTLY (RS symmetry).
     => no non-residue sign-dominates another. (the literal task phrasing is empty here.)
 (B) Each NR vs the principal class b=1: delta(N;a,1) > 1/2 and these DIFFER. The only
     coherent "hierarchy among NR" is the ordering of delta(N;a,1); a=-1 is its MINIMUM.

COMPUTABLE delta(q;a,1) (two interchangeable routes, both RUN & validated):

ROUTE I — exact characteristic function + Gil-Pelaez (validated to 5 dp):
   D_a = m + sum_{chi != chi0} sum_{gamma_chi > 0} A_{chi,gamma} cos(theta),  theta iid U(0,2pi),
   m = #sqrt(1) - #sqrt(a) = rho(q) for a NR vs 1,
   A_{chi,gamma} = |chi(a) - 1| * 2 / sqrt(1/4 + gamma^2),
   phi_D(xi) = e^{i xi m} * prod_{chi,gamma>0} J0( A_{chi,gamma} xi ) * e^{-xi^2 sigma_tail^2 / 2},
   sigma_tail^2 = sum_chi |chi(a)-1|^2 * 2 * int_T^inf (1/(2pi)) log(q t / 2pi) / (1/4+t^2) dt,
   delta(q;a,1) = 1/2 + (1/pi) int_0^inf Im phi_D(xi) / xi  d xi.
   VALIDATION (canonical_verify.py, single real odd char, 150 zeros, T~last zero):
     delta(4;3,1) = 0.99593  (RS published 0.99590)   <-- 3e-5 agreement
     delta(3;2,1) = 0.99907  (RS published 0.99906)   <-- 1e-5 agreement

ROUTE II — FM 2-term asymptotic (fast, ordering-exact, needs q>=43 for value):
   delta(q;a,1) = 1/2 + rho(q)/sqrt(2 pi V(q;a,1)) + O(rho^3/V^{3/2}),  V from Sec 4.
   Rank NR by V ascending; a=-1=q-1 has the largest V hence the smallest delta.
   (For q<43 use the variance ORDERING, not the truncated value — it can give delta>1.)

c_chi (=b(chi)) exact recipe: c_chi = log(q/pi) + psi((1+a_chi)/2) + 2 Re L'/L(1,chi);
zeros of real primitive chi via Hardy Z(t)=Re[(q/pi)^{(s+a)/2} Gamma((s+a)/2) L(s,chi)],
L(s,chi)=q^{-s} sum_{r=1}^q chi(r) zeta(s, r/q) (Hurwitz). Validated 1st zeros
6.020948 (chi_4), 8.039737 (chi_3).

================================================================================
## 6. SANITY VALUES (validate any implementation against these) [PRIMARY-SOURCED]
================================================================================
- delta(4;3,1) = 0.99590  (RS 1994; my recipe -> 0.99593)
- delta(3;2,1) = 0.99906  (RS 1994; my recipe -> 0.99907)
- two distinct non-residues: delta(q;a,b) = 1/2 EXACTLY (RS pairwise symmetry)
- 1st zero ordinates: gamma(chi_4)=6.020948, gamma(chi_3)=8.039737
- c_chi: c(chi_4) ~ 0.1556, c(chi_3) ~ 0.1132 (low-zero sum + tail)
- rho(q) = 2 for prime q;  V(q;a,b) ~ 2 phi(q) log q
- q=163 (FM Table 3): a=162 == -1 is the GLOBAL MIN of delta(163;a,1) among NR
  (delta ~ 0.524032; low-lying zero gamma~0.2029, small h(-163), inflates V ~56%)
- WARNING anti-sanity: it is NOT true that 7 == -1 (mod 8) tops delta mod 8.
  delta(8;3,1) > delta(8;7,1) > delta(8;5,1) — -1 is not first (FM-style).
- AK gives NO density value; its only "sanity" is the degenerate NR flat-tie
  (Ex 3.5: pi_{1/2}(x;8,j)-pi_{1/2}(x;8,k) = c + o(1) for any j,k in {3,5,7}).

================================================================================
## 7. RECONCILING THE 4 DERIVATIONS (where they disagree, who is right)
================================================================================
AGREEMENT (all 4, and confirmed by my runs): (i) leading means tie at -1 for all NR;
(ii) the discriminant is the VARIANCE/covariance, not skew; (iii) -1 is singled out
by the iq(-a)log2 / odd-parity mechanism; (iv) FM Thm 1.10 makes -1 the LEAST-biased
NR; (v) AK DRH-magnitude does not separate NR (m_chi=0 generically).

DISAGREEMENTS resolved:
- Deriv 1 ("FM Thm 10"): conclusion (rank by discriminant, -1 largest => smallest
  density) is CORRECT, but its covariance line "2 phi q (L+K+indicator log2)" states
  only the AGGREGATE variance and omits that the true per-character object is
  c_chi |chi(a)-1|^2 with c_chi parity-dependent. Use Deriv 2/4's c_chi form. Its
  "variance not skewness" call is RIGHT.
- Deriv 2 (RS-distribution): CORRECT and most complete on covariance + Gil-Pelaez +
  symmetry-kills-skew. Adopted as the spine of Sec 2,5. Its "delta=1/2 for two NR" and
  anchors are right.
- Deriv 3 (AK/DRH): CORRECT as a NEGATIVE result — AK cannot be the mechanism. Adopted
  in Sec 2 as the reason DRH-magnitude is ruled out. Do NOT use AK to claim -1 leads.
- Deriv 4 (FM density): CORRECT and primary-source-exact (Thm 1.10 verbatim, Thm 1.4
  closed form, q=163 table). Adopted for Sec 3,4 and the prior-art verdict.

CANONICAL MECHANISM (single sentence): among non-residues all leading RS means tie at
-1, and the finer order is set by the RS variance V(q;a,1)=sum_chi c_chi|chi(a)-1|^2;
a=-1 alone dumps all its character weight onto the heavier ODD characters (extra
+2 phi(q) log2), giving it the MAXIMAL variance and therefore the MINIMAL sign-density
— so "-1 dominates the non-residues" is true only in amplitude/variance and is the
exact REVERSE of the truth for the standard sign-density delta (FM Thm 1.10).

================================================================================
## 8. PRIOR ART [VERIFIED PRIMARY SOURCES — PDFs + text extracts in this dir]
================================================================================
- Rubinstein-Sarnak, Experiment. Math. 3 (1994) 173-197 — limiting distribution,
  GRH+LI, pairwise symmetry, delta(4;3,1)=0.9959, delta(3;2,1)=0.99906. [RS PDF
  download was blocked; statements cross-checked via GM & FM, FLAGGED second-hand.]
- Granville-Martin, Amer. Math. Monthly 113 (2006) 1-33 — VERIFIED first-hand
  (PNR_text.txt): two non-squares => exactly 1/2; square-root-count mean.
- Fiorilli-Martin, Crelle 676 (2013) = arXiv:0912.4908 — VERIFIED first-hand
  (FM_text.txt): Def 1.3 (rho, V), Thm 1.4 closed variance with iq(-ab^{-1})log2
  (line 182), Thm 1.10 (line 325, VERBATIM above). THE source for -1-among-NR.
- Aoki-Koyama, J. Number Theory 245 (2023) = arXiv:2203.12266 — VERIFIED first-hand
  (AK_text.txt): DRH bias-magnitude C loglog x + c; no NR hierarchy; does not
  single out -1.
VERDICT: "-1 dominates among non-residues" is UNATTESTED as a positive claim and is
CONTRADICTED (for sign-density delta) by FM Thm 1.10. The variance/amplitude reading
("-1 maximizes V, biggest |D|") is TRUE and is exactly Fiorilli-Martin — NOT novel.

================================================================================
## 9. CONDITIONALITY / CAVEATS
================================================================================
- ALL density/ordering statements assume **GRH + LI**. FM Thm 1.4 (variance) needs
  only GRH. NONE is unconditional. Do NOT upgrade.
- AK is CONDITIONAL on **DRH** (strictly stronger than GRH; unconditional only for
  function fields char(K)>0, NOT for Dirichlet races over Q). Do NOT upgrade.
- Applies only when -1 is a NON-residue: q ≡ 3 (mod 4) primes (7,11,19,23), and the
  relevant even moduli. For q ≡ 1 (mod 4) (e.g. 13), -1 is a QR and the NR question
  is vacuous.
- Route-II value needs q >= 43 (Lambda(q)>0); for small q use the variance ORDERING
  (monotone, valid) or Route-I exact integral.
- Skew is RULED OUT (symmetric law). m_chi=0 inferred from numeric nonvanishing, not
  rigorous zero-counting (smallest |L(1/2,chi)| seen 0.2318, comfortably nonzero).
- RS-specific equation numbers are second-hand (RS PDF was not read directly).

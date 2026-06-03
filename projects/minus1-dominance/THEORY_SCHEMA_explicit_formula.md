# THEORY_SCHEMA — "-1 among non-residues" via the explicit formula

Angle: EXPLICIT FORMULA for pi(x;q,a) via Dirichlet characters.
All numbers below were RUN (python3/mpmath/sympy) and primary-source-checked
against Fiorilli–Martin, Crelle 676 (2013) = arXiv:0912.4908 (PDF in this dir).
Status tags: [PROVEN], [NUMERICAL], [CONJECTURAL], [CONDITIONAL: GRH/LI].

## 0. Explicit-formula starting point [PROVEN, classical]
psi(x;q,a) - x/phi(q) = -(1/phi(q)) sum_{chi!=chi0} conj(chi)(a) sum_{rho_chi} x^{rho}/rho + ...
Subtracting two classes and passing to pi:
  D(x;q,a)-D(x;q,b) = (1/phi(q)) sum_{chi!=chi0} (conj chi(a) - conj chi(b)) sum_{p<=x} chi(p) + (lower order).
Normalized E(x;q,a) = (phi(q) log x / sqrt x)(pi(x;q,a)-pi(x;q,1)); under GRH+LI
E converges in log-density to a random variable X_a (Rubinstein–Sarnak 1994).

## 1. CRUX RESOLVED — equal leading means among NR [PROVEN/NUMERICAL]
Mean of X_a (race a vs 1): mu(a) = -(#sqrt of a) (square classes carry the
prime-square deficit). For ANY non-residue a, #sqrt(a)=0 => mu(a)=0. Verified
for q=5,7,8,11,12,19,23: every NR ties at the same leading mean. Hence:
  HEAD-TO-HEAD delta(q;-1,a)=dens{D(-1)>D(a)} = 1/2 EXACTLY for two NR
  [Rubinstein–Sarnak: delta=1/2 when a,b both nonsquares]. MC q=8: 0.500.
=> "-1 dominance" is NOT a leading-mean nor a head-to-head sign-density effect.

## 2. The REAL discriminant = the race AGAINST 1, via the variance term ι_q(-ab^-1)log2
Feuerverger–Martin: delta(q;a,b)=delta(q;ab^-1,1) for square b, so study delta(q;a,1).
Fiorilli–Martin Cor 1.9 (q>=43, a NR, b=1):
  delta(q;a,1) = 1/2 + rho(q)/(2 sqrt(pi phi(q) L(q))) * (1 - Delta(q;a,1)/(2L(q)) + O(1/log^2 q))
  Delta(q;a,1) = K_q(a-1) + ι_q(-a) log2 + Λ(r1)/r1 + Λ(r2)/r2 + H,   r1=a, r2=a^-1.
LARGER Delta => SMALLER delta (paper, verbatim).
Variance: V(q;a,1)=2phi(q)(L(q)+K_q(a-1)+ι_q(-a)log2)+2M*  (Thm 1.4).

## 3. WHY a=-1 IS SPECIAL [PROVEN, exact mechanism]
ι_q(-ab^-1) for b=1 is ι_q(-a)=[a ≡ -1 (mod q)]. Among ALL non-residues a,
ONLY a=-1 makes -a ≡ 1, so ONLY a=-1 picks up the extra + log2 ≈ 0.6931.
Origin (FM eq 3.7): -log2 * sum_chi |chi(a)-chi(b)|^2 chi(-1) = (2log2)phi(q)ι_q(-ab^-1);
this is the contribution of the prime p=2 / the chi(-1) gamma-factor sign in the
completed L-functions. Verified ι_q(-a)=1 iff a=q-1 for q=7,8,11,12,19,23,24,163.
Consequence of the SAME +log2 term, in two metrics:
  (i) delta(q;-1,1): +log2 is the LARGEST Delta among NR => -1 has the SMALLEST
      delta(q;-1,1). -1 is the LEAST-favored NR vs the principal class.
  (ii) V(q;-1,1): +log2 is added to the variance => -1 has the LARGEST variance
      => biggest typical |D(-1)|. -1 "leads in amplitude."

## 4. PRIOR ART — the established theorem (direction = OPPOSITE of "dominance")
Fiorilli–Martin Theorem 1.10 (GRH+LI), verbatim:
  "For any integer a != -1, delta(q;-1,1) < delta(q;a,1) for all but finitely many
   q with (q,a)=1 such that both -1 and a are nonsquares (mod q)."
So -1 is provably (cond. GRH+LI) the LEAST favored non-residue in the race
against 1 — it is NOT the largest/leading class in sign-density. Any "-1 dominates
among NR" claim is FALSE for sign-density delta and TRUE only for the variance/
amplitude V. The phenomenon is fully explained by ONE term: ι_q(-a) log2.

## 5. NUMERICAL VALIDATION (all RUN)
- Reproduced FM Table 3 (q=163, prime): my closed-form vs published
    a=162(=-1): 0.523578 vs 0.524032 (diff 4.5e-4 = O(1/log^2 q), max where Delta max)
    a=3:0.525013/0.525168 a=2:0.525330/0.525370 a=5:0.525455/0.525428 a=7:0.525676/0.525664
  -1=162 confirmed GLOBAL MIN of delta(163;a,1) among all NR.
- Delta-ranking puts a=-1 LAST among NR for q=19,23,43,47,163 (and small q by Delta).
- MC sanity: delta(4;3,1)=0.998, delta(3;2,1)=1.000 (right direction, NR favored;
  magnitudes slightly high — only ~37 truncated zeros => b(chi) undercounted;
  true b(chi_-4)≈0.143 gives RS 0.9959). Head-to-head NR-vs-NR MC = 0.500.
- Dirichlet L first zeros (mpmath, |L|<1e-12): chi_-4 6.0209, chi_-3 8.0397,
  chi_8(even) 6.0209-line / odd mod8 3.5762 — match LMFDB.

## 6. CONDITIONALITY / CAVEATS
- Theorem 1.10 and Cor 1.9 are [CONDITIONAL: GRH + LI]. Do NOT upgrade.
- Cor 1.9 asymptotic needs q>=43 (L(q)>0); for small q (7,8,11,12,24) use the
  Delta-ordering (monotone, valid) not the closed-form delta value.
- For q ≡ 1 (mod 4), -1 is a QUADRATIC RESIDUE, so the "NR" question is vacuous;
  applies only when -1 is a nonsquare (q≡3 mod4, q≡0 mod 4 in part, etc.).
- AK/DRH (Aoki–Koyama) is a SEPARATE magnitude refinement for number/function
  fields; the q-aware ordering here is the Fiorilli–Martin (GRH+LI) mechanism,
  not DRH. Function-field unconditional analogue lives in ../ak-bias-followups.

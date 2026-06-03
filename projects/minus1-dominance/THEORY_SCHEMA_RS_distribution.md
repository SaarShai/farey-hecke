# THEORY_SCHEMA — "-1 among non-residues" via the RUBINSTEIN–SARNAK LIMITING DISTRIBUTION

Angle: the RS 1994 limiting logarithmic distribution of the normalized error
vector, its mean / covariance / shape. Companion to
`THEORY_SCHEMA_explicit_formula.md` (same conclusion, explicit-formula route).
All numbers RUN (python3 + mpmath/sympy), primary-source-checked vs
Fiorilli–Martin, Crelle 676 (2013) = arXiv:0912.4908 (PDF in this dir).
Tags: [PROVEN] [NUMERICAL] [CONDITIONAL: GRH/LI] [CONJECTURAL].

CRITICAL HEADLINE (adversarial honesty): the task's conjecture "-1 dominates /
leads among non-residues" is FALSE for sign-density δ. The established theorem
(FM Thm 1.10, GRH+LI) is the OPPOSITE: among non-residues raced vs 1, a=-1 has
the SMALLEST δ(q;a,1). What -1 DOES maximize is the VARIANCE of the RS limiting
distribution. Larger variance ⇒ δ closer to ½ ⇒ -1 is the LEAST-biased NR.

--------------------------------------------------------------------------------
## 1. The RS limiting distribution [CONDITIONAL: GRH+LI; RS 1994]
Normalized error E(x;q,a) = (φ(q) log x / √x)(π(x;q,a) − π(x)/φ(q)). Under GRH+LI
its log-density limit is the law of the random vector
   X_a = mean(a) + Σ_{χ≠χ0} χ(a) Z_χ,
   Z_χ = Σ_{γ_χ>0} (2/√(¼+γ²)) · Re(e^{iθ_γ}),  θ_γ iid Uniform(0,2π)  (LI).
Each cosine term A·cos(θ) is symmetric ⇒ X_a − mean is SYMMETRIC.

## 2. MEAN — the leading tie [NUMERICAL, PROVEN classical]
mean of E_a = −1 + #{b mod q : b²=a}.  For EVERY non-residue a this is −1
(zero square roots). Verified q=3,4,5,7,8,11,12,13,15,19,23,24 (verify_mean.py):
all NR tie at −1. ⇒ the mean cannot separate -1 from other NR.
[CRUX confirmed: not a leading-mean effect.]

## 3. COVARIANCE — the actual discriminant [PROVEN formula; NUMERICAL c_χ]
   Cov(X_a,X_b) = Σ_{χ≠χ0} c_χ · conj(χ(a)) χ(b),  c_χ = Σ_{γ_χ} 1/(¼+γ²).
   (= FM Def 1.3 b(χ); = task's B(N;a,b).)
Race a-vs-1 variable D_a = X_a − X_1 (χ(1)=1):
   Var(D_a) = Σ_χ c_χ |χ(a)−1|².
EXACT combinatorial identity (RUN, why_minus1.py): Σ_{all χ≠χ0} |χ(a)−1|² = 2φ(q)
for EVERY a≠1 — so with c_χ≡1 ALL classes a≠1 (residue or not) tie in variance.
⇒ the discriminant is the χ-DEPENDENCE of c_χ, specifically its PARITY split.

## 4. WHY a=-1 IS SPECIAL — the parity mechanism [PROVEN + NUMERICAL]
χ(−1) = +1 (χ even) or −1 (χ odd). So χ(−1)−1 = 0 (even) or −2 (odd):
   a=-1 places ALL its |χ(−1)−1|²=4 weight on ODD characters, NONE on even.
Any other NR spreads |χ(a)−1|² across both parities.
Odd characters carry MORE c_χ weight than even ones. Mechanism (two-term):
  (a) Archimedean: c_χ = log(q/π) + ψ((1+a_χ)/2) + 2 Re L'/L(1,χ),  a_χ=parity.
      ψ(1) = −γ ≈ −0.5772 (odd) vs ψ(1/2) = −γ−2ln2 ≈ −1.9635 (even):
      odd c_χ larger by ≈ 2 ln2 ≈ 1.386 from the Γ-factor alone.
  (b) FM eq 3.7 (the clean closed identity): the parity asymmetry contributes
      −log2·Σ_χ |χ(a)−1|² χ(−1) = (2 log2) φ(q) · ι_q(−a),  ι_q(−a)=[a≡−1].
      ⇒ a=-1 gets an EXTRA +2φ(q)·log2 of variance; no other NR does.
NUMERICAL (cchi_parity.py, analytic c_χ, all χ): mean c_χ(odd) > mean c_χ(even)
in every case, and V(D_{-1}) is STRICTLY LARGEST among NR:
   q=7:  c̄_odd 0.311 > c̄_even 0.218; V(-1)=3.731 > next 3.004;  -1 rank 1/3
   q=11: c̄_odd 0.577 > c̄_even 0.332; V(-1)=11.55 > 10.04;       -1 rank 1/5
   q=19: c̄_odd 1.539 > c̄_even 0.534; V(-1)=55.40 > 48.92;       -1 rank 1/9
   q=23: c̄_odd 1.240 > c̄_even 0.625; V(-1)=54.56 > 44.16;       -1 rank 1/11

## 5. SHAPE / SKEW — what "non-Gaussian" really means here [PROVEN]
The CRUX-statement's "non-Gaussian SKEW" hypothesis is FALSE as a discriminant:
D_a = mean + Σ A_k cos(θ_k) is SYMMETRIC ⇒ skewness ≡ 0 EXACTLY (skew_kurtosis.py).
The non-Gaussianity is in the (symmetric) KURTOSIS / tail shape (4th+ cumulants),
strongest when few odd zeros dominate c_χ. At FIXED variance, kurtosis moves δ only
slightly (e.g. one-cosine vs 200-cosine at V=12: δ 0.366 vs 0.282). The DOMINANT
lever is the VARIANCE. So: discriminant = covariance/variance (Item 4), with a
secondary leptokurtic nudge (same sign), NOT skew.

## 6. VARIANCE → DENSITY direction [PROVEN; the sign that reverses naive intuition]
NR leads ⇒ δ(q;NR,1) > ½. With mean m>0 (NR ahead) and variance V:
   δ = P(D>0) = Φ-type(m/√V) + (sym. corrections);  |δ−½| DECREASES as V↑.
RUN (sign_audit.py, Gil–Pelaez exact inversion, m=2):
   V=4→δ0.841, V=8→0.760, V=12→0.718, V=20→0.672, V=40→0.624, V=80→0.588.
⇒ larger V ⇒ δ CLOSER to ½ ⇒ a=-1 (max V) is the LEAST-biased NR. Matches FM
Thm 1.1: δ = ½ + ρ(q)/√(2π V) + O(V^{-3/2}), ρ(q)=#real chars (same for all a vs 1).
(My first pass density_implication.py read this direction backwards; CORRECTED.)

## 7. DENSITY RECIPE δ(q;a,1) [computable; VALIDATED]
Gil–Pelaez on the EXACT (non-Gaussian) characteristic function:
   φ_D(ξ) = e^{iξ m} · Π_{χ≠χ0} Π_{γ_χ>0} J0( |χ(a)−1| · (2/√(¼+γ²)) · ξ ),
            m = (#√1) − (#√a)   [= +ρ(q) for a NR vs 1],   J0 = Bessel.
   δ(q;a,1) = ½ + (1/π)∫_0^∞ Im φ_D(ξ)/ξ dξ.
High zeros: replace tail by Gaussian factor exp(−ξ²σ_tail²/2),
   σ_tail² = Σ_χ |χ(a)−1|² · 2·∫_{T}^∞ (1/π)log(qt/2π)/(¼+t²) dt.
VALIDATION (anchor_fixed.py, single odd quadratic χ, 114–121 zeros, T=200):
   δ(4;3,1) = 0.99151  (RS published 0.99590)
   δ(3;2,1) = 0.99684  (RS published 0.99906)
Right direction (NR leads, δ→1) and magnitude; residual is zero-truncation +
crude Gaussian tail (gap shrinks monotonically as T grows; sibling's closed-form
reproduces FM Table-3 q=163 to 4.5e-4).

## 8. c_χ — exact recipe [VALIDATED]
Definition (unambiguous): c_χ = Σ_{γ:L(½+iγ,χ)=0} 1/(¼+γ²).
Analytic closed form (RUN + VALIDATED vs zero-sum):
   c_χ = log(q/π) + ψ((1+a_χ)/2) + 2 Re L'/L(1,χ),  a_χ = (1−χ(−1))/2.
Zeros via Hardy Z(t)=Re[(q/π)^{(s+a)/2}Γ((s+a)/2)L(s,χ)], s=½+it, for real primitive
χ (root number +1). Validated against known β(s)=L(s,χ_4) zeros 6.020948, 10.243770,
12.988098 and L(s,χ_3) zeros 8.039737, 11.249193, 15.704619 (zfun_clean.py).
Convergence to analytic value (cchi_converge.py, χ_4): zero-sum→0.155568 as T:60→400
(gap 0.024→0.014→0.0079→0.0051, the slow tail). c_χ4≈0.1556, c_χ3≈0.1132.

## 9. PRIOR ART [VERIFIED primary source]
- Fiorilli–Martin, Crelle 676 (2013), Thm 1.10 bullet 1 (VERBATIM, GRH+LI):
  "For any integer a≠−1, δ(q;−1,1) < δ(q;a,1) for all but finitely many integers q
   with (q,a)=1 such that both −1 and a are nonsquares (mod q)."
  ⇒ -1 is the unique LEAST-favored NR vs 1. Table 3 (q=163): smallest δ is a=162≡−1.
- The variance/covariance form (Item 3), the closed variance (Thm 1.4) and the
  log2 / ι_q(−ab⁻¹) mechanism are ALL Fiorilli–Martin (descendant of RS 1994).
- Rubinstein–Sarnak, Exp. Math. 3 (1994) 173–197: original limiting distribution,
  δ(q;a,b)=½ for two distinct NR, δ(4;3,1)=0.9959, δ(3;2,1)=0.99906.
- Aoki–Koyama (JNT 245, 2023): SEPARATE DRH magnitude (single class, C log log x),
  m_ρ=0 generically ⇒ no NR hierarchy from AK; does NOT single out -1.
VERDICT: "-1 dominance among NR" is NOT established; the OPPOSITE is (δ-sense). -1
is special as the unique VARIANCE-maximizing / least-biased NR. NOVEL? No — the
mechanism is exactly Fiorilli–Martin. Only an AMPLITUDE re-reading ("-1 leads in
|D|/variance") is a true statement consistent with -1 LOSING the sign-density race.

## 10. CONDITIONALITY / CAVEATS
- All ordering statements (FM Thm 1.10, Cor 1.9, Thm 1.1) are [CONDITIONAL: GRH+LI].
  Do NOT upgrade to unconditional.
- Applies only when -1 is a NON-residue: q≡3 mod 4 primes (7,11,19,23), q≡0 mod 4
  in part. For q≡1 mod 4 (e.g. 13), -1 is a QR and the NR question is vacuous.
- δ-closed-form (Cor 1.9) needs q≥43 (L(q)>0); for small q use the Δ/variance
  ORDERING (monotone, valid), not the asymptotic δ value.
- The "skew" discriminant is RULED OUT (Item 5): distribution is symmetric.
- My density-direction sign was corrected mid-analysis (Item 6); final statement
  agrees with FM. The earlier file density_implication.py is kept but its prose
  direction is superseded by sign_audit.py.

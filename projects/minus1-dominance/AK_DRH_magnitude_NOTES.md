# -1-Dominance via the Aoki-Koyama DRH magnitude — NOTES (angle: AK DRH magnitude)

LOCAL ONLY. No external sends. Adversarial honesty: PROVEN / NUMERICAL / CONJECTURAL flagged.

## Citation (VERIFIED against primary sources)
- Title: "Chebyshev's Bias against Splitting and Principal Primes in Global Fields"
- Authors: Miho Aoki, Shin-ya Koyama
- Journal: J. Number Theory 245 (2023) 233-262.  arXiv:2203.12266.
- Verified: ScienceDirect S0022314X22002335 (vol/pages 245/233-262, 2023); arXiv abstract;
  publisher PDF on researchmap (full text extracted to /tmp/ak_norm.txt, 1843 lines).
- The framework rests on DRH (= conditional). NOT upgraded to unconditional except char(K)>0
  (function fields), where AK cite DRH proved [their ref 19].

## The AK magnitude framework (PROVEN-under-DRH, their Thm 3.1 / eq (3.3),(3.4))
Weighted counting function pi_{1/2}(x;q,a) = sum_{p<x, p=a mod q} p^{-1/2}.
For L=Q(zeta_q)/Q, G=(Z/qZ)^*, with m_chi := ord_{s=1/2} L(s,chi) (analytic rank) and
m(a) := sum_{chi != 1} chi(a) m_chi:

  pi_{1/2,Q}(x) - phi(q) pi_{1/2}(x;q,a)
     = ( (2^t - 1)/2 + ... )    -- residue case
  Eq (3.3):  pi_{1/2,Q}(x) - phi(q)*pi_{1/2}(x;q,a) ~
     [ (2^t-1)/2 + m(a) ] loglog x + c + o(1)   if a is QR
     [   -1/2     + m(a) ] loglog x + c + o(1)   if a is NR
  where t is the (corrected) number of distinct prime divisors of q, |G/G^2| = 2^t.

Eq (3.4) (assuming m(a)=0 for all a, i.e. all central values L(1/2,chi) != 0):
  pi_{1/2}(x;q,b_NR) - pi_{1/2}(x;q,a_QR) = ((2^t - 1)/phi(q)) loglog x + c + o(1).

Cor 3.3 (the CRUX): if m(a)=0 for all a, then
  pi_{1/2}(x;q,b) - pi_{1/2}(x;q,b') = c + o(1)   for ANY two NRs b,b'  (and any two QRs).
=> NO leading (loglog x) difference between non-residues. AK Example 3.5 (q=8) states this
   explicitly: for any j,k in {3,5,7}, pi_{1/2}(x;8,j)-pi_{1/2}(x;8,k) = c + o(1).

## DECISIVE VERDICT for "-1 dominance"
In the AK DRH-magnitude scale (the e^{-gamma}-type / conditional-convergence normalization that
weights primes by p^{-1/2} and measures size on the loglog x scale):

  * Every non-residue class has the SAME leading coefficient (2^t-1)/phi(q) vs the residues.
    => This confirms the task's CRUX SUBTLETY from the AK side: all NR tie at leading order.
  * The tie among non-residues is broken ONLY by m(a) = sum_{chi!=1} chi(a) m_chi, i.e. by the
    ANALYTIC RANKS m_chi = ord_{s=1/2} L(s,chi) of the Dirichlet L-functions.
  * GENERIC CASE (all L(1/2,chi) != 0, m_chi=0 for all chi):  m(a)=0 for every a, so AK predict
    -1 does NOT lead -- it ties every other non-residue at leading order AND at the loglog x
    coefficient, with only a BOUNDED constant c_b distinguishing them. AK do NOT compute c_b.
    => Under the AK magnitude framework, "-1 dominance among non-residues" is INVISIBLE / not a
       DRH-magnitude effect. It must come from the O(1) constant term, which is exactly the part
       AK discard. (This is the honest negative result for this angle.)

## When could AK's magnitude term make -1 special? (CONJECTURAL mechanism)
m(a) is nonzero only if some L(1/2,chi)=0 (m_chi>0). a=-1 is the unique element of order 2 that
is complex conjugation; chi(-1)=+1 for EVEN chi, -1 for ODD chi. So
  m(-1) = sum_{chi even, !=1} m_chi  -  sum_{chi odd} m_chi.
The class -1 maximally weights ODD vs EVEN central-zero deficits. For -1 to TOP the NR hierarchy
in AK's scale you would need m(-1) > m(b) for every NR b != -1, i.e. an asymmetry in the
distribution of central zeros L(1/2,chi)=0 across parity classes weighted by chi(-1). This is
exotic: it is widely expected (Chowla) that L(1/2,chi) != 0 for ALL Dirichlet chi, in which case
m(a)=0 for all a and the AK term gives NO hierarchy at all.

CONCLUSION FOR THE ANGLE: the AK 2023 DRH magnitude does NOT explain -1 dominance among
non-residues in the generic (Chowla) regime. It tells us the discriminator is NOT in the
loglog x magnitude but in the bounded constant c_b — which is where the RS-covariance /
skewness / c_chi angles must look. The AK framework's positive content here is the EXACT
statement that NR's tie to all orders in loglog x (its Cor 3.3 / Ex 3.5), sharpening the
task's leading-mean observation to the full weighted-magnitude scale.

## Numerical verification (RUN, real numbers; scripts in this dir)
ak_central_values.py — L(1/2,chi) for q=3,5,7,11,13,23 (Hurwitz-zeta). ALL non-zero:
  e.g. q=7 Legendre L(1/2)=1.14659; q=11 Legendre L(1/2)=0.991577; q=23 Legendre L(1/2)=2.45536.
  q=5 chi_2 (quadratic) L(1/2)=0.231751 (smallest seen) still != 0. => m_chi=0 for all tested.
  => m(a)=0 for all classes a at these moduli => AK leading hierarchy is degenerate (Cor 3.3).
ak_hierarchy.py — leading NR-vs-QR coeff (2^t-1)/phi(q):
  q=4:0.5  q=7:0.16667  q=8:0.75  q=11:0.1  q=19:0.05556  q=23:0.04545 ; identical for every NR.
minus1_role.py — confirms -1 is a NON-residue for q=7,8,11,19,23 (q=3 mod 4 => (-1|q)=-1).

## Status tags
- PROVEN (conditional on DRH): AK Thm 3.1, eq (3.3),(3.4), Cor 3.3, Ex 3.5  (their theorems).
- PROVEN unconditional: only char(K)>0 (function fields). NOT applicable to Z/qZ over Q.
- NUMERICAL (this session): m_chi=0 for q in {3,5,7,11,13,23} via L(1/2,chi)!=0 (mpmath dps=25-30).
- CONJECTURAL: any -1-topping-hierarchy claim from AK requires parity-weighted central-zero
  asymmetry, contradicted by the expected Chowla nonvanishing => AK predicts NO NR hierarchy
  generically. -1 dominance, if real, is an O(1)-constant / RS-density phenomenon, not AK-magnitude.

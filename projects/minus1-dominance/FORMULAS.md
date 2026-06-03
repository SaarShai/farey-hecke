# minus-1 among non-residues: exact formulas & prior-art (local research notes)

## Verified primary sources (PDFs in this dir)
- Granville-Martin, "Prime Number Races", Amer. Math. Monthly 113 (2006) 1-33.  `PNR_granville_martin.pdf` / `PNR_text.txt`
- Fiorilli-Martin, "Inequities in the Shanks-Renyi prime number race: an asymptotic formula for the densities", J. reine angew. Math. (Crelle) 676 (2013) 121-212. arXiv:0912.4908.  `FiorilliMartin_ISRPNRAFD.pdf` / `FM_text.txt`
- Aoki-Koyama, "Chebyshev's Bias against Splitting and Principal Primes in Global Fields", J. Number Theory 245 (2023). arXiv:2203.12266.  `AokiKoyama_2203.12266.pdf` / `AK_text.txt`
- Rubinstein-Sarnak, "Chebyshev's bias", Experiment. Math. 3 (1994) 173-197.  (download blocked; results cross-checked via FM/GM which restate them)

## The leading-mean tie (user's crux, CONFIRMED)
RS limiting mean of normalized error E(x;q,a) = -1 + #{b mod q: b^2=a}. For every NON-residue a this is -1. All non-residues tie at leading order. (rs_means.py, verify_mean.py.)

## The real discriminant: the RS VARIANCE (FM Def 1.2/1.3, Thm 1.4)
- delta(q;a,b) = 1/2 + rho(q)/sqrt(2 pi V(q;a,b)) + O(rho^3/V^{3/2})   [FM eq 1.2]
- rho(q) = #{x: x^2=1 mod q} = number of real chars; SAME for all (nonsquare a vs square b).  => the ONLY thing varying between two non-residues a,a' (both raced vs b=1) is V.
- V(q;a,b) = sum_{chi mod q} |chi(b)-chi(a)|^2 b(chi),  b(chi)=sum_{gamma:L(1/2+ig,chi)=0} 1/(1/4+gamma^2).  [FM Def 1.3]
- Arithmetic closed form [FM Thm 1.4, GRH]:
  V(q;a,b) = 2 phi(q)[ Lambda(q) + Kq(a-b) + iq(-a b^{-1}) log2 ] + 2 M*(q;a,b),
  iq(n)=1 iff n==1 mod q;  Kq>=0 bounded;  M*(q;a,b)=sum_{chi!=chi0}|chi(a)-chi(b)|^2 Re L'/L(1,chi*).

## Why a=-1 is SPECIAL (and LOSES, not dominates)
For b=1: the term iq(-a*1^{-1}) log2 = iq(-a) log2 = log2 EXACTLY when a == -1 (mod q), else 0.
So a=-1 (alone among non-residues vs 1) carries an EXTRA +2 phi(q) log2 in V.
Larger V => delta closer to 1/2 => SMALLER density.
=> a=-1 is the LEAST-leading non-residue. This is FM **Theorem 1.10, bullet 1**:
   "For any integer a != -1, delta(q;-1,1) < delta(q;a,1) for all but finitely many q
    with (q,a)=1 and both -1,a nonsquares."
(Mechanism: under b->-b duality, racing a vs -a is the most balanced; a=-1 vs 1 is the a=-(b) case, maximal cancellation in the bias / maximal variance.)

## Numerics (compute_density_fm.py, this dir)
delta(q;a,1) for all nonsquares a, q in {7,11,19,23,43,47,67,163}: a=-1=q-1 is rank LAST
(smallest delta, largest V) in EVERY case. q=163 (small h(-163), low-lying zero) extreme.
Variance-gap check: V(q;-1,1) > V(q;a,1) for all a, gap sign robust.

## Sanity (sanity_rs.py)
b(chi4)~0.156, b(chi3)~0.116 from low zeros; Gaussian delta(4;3,1)~0.9943, delta(3;2,1)~0.9983
vs literature 0.99590 / 0.99906 (gap = known non-Gaussian skew). Scale confirmed.

## Aoki-Koyama relation
AK give a DRH bias-magnitude for a SINGLE class sigma: C log log x + c + o(1), C via central-zero
order m_rho (Conj 1.1). For Dirichlet chars mod q, m_rho=0 generically => no hierarchy among
non-residues from AK either. AK do NOT single out a=-1; not a source of "-1 dominance".

## PRIOR-ART VERDICT
"-1 dominates among non-residues" is NOT established anywhere; the established result is the
OPPOSITE (FM Thm 1.10): -1 is the unique LEAST-biased non-residue vs the principal class.

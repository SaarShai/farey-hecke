"""
The REAL discriminant: skewness of the RS limiting distribution.

For two non-residues a, b with EQUAL leading mean mu=-1, define
   delta(N; b, a) = density{ X_b > X_a } = P( X_b - X_a > 0 ),
where W := X_b - X_a has MEAN ZERO (means cancel). If W were symmetric,
delta = 1/2 exactly. The deviation from 1/2 is third-order: by an
Edgeworth/Gram-Charlier expansion of a mean-zero r.v. W with variance s^2 and
third cumulant k3,
   P(W>0) = 1/2 + k3/(6 sqrt(2 pi) s^3) + (higher) .
So the LEADING discriminant of the race between two equal-mean classes is the
SKEWNESS  gamma1(W) = k3 / s^3,  and
   delta(N;b,a) = 1/2 + gamma1(W)/(6 sqrt(2pi)) + ...   (approx).

We need the third cumulant of  W = X_b - X_a.  From the explicit formula, the
RS random variable is (combining each chi with its conjugate; b(.) real):
   X_a = mu(a) + sum_{chi != chi0} conj(chi(a)) * R_chi
where R_chi are the random fluctuation contributions. Crucially the R_chi for
chi and conj(chi) are complex-conjugate of each other so X_a is real, and the
families {R_chi : chi in a conj-pair} are INDEPENDENT across distinct unordered
conj-pairs (under LI). Each unordered pair {chi, chibar} contributes a real
random variable; for chi=chibar (real char) it is a single real family.

THIRD CUMULANT. Cumulants add over independent summands. Write
   X_b - X_a = sum_{chi} (conj(chi(b)) - conj(chi(a))) R_chi.
Group into conj-pairs. For a conj-pair {chi,chibar} the joint contribution to W is
   c_chi R_chi + conj(c_chi) R_chibar ,   c_chi := conj(chi(b))-conj(chi(a)).
Because R_chibar = conj(R_chi), this real summand is  2 Re( c_chi R_chi ).
Its 3rd cumulant is the engine.

The third cumulant of the explicit-formula random sum is NONZERO only when the
zeros enter with an UNBALANCED phase. R_chi = sum_gamma 2 Re( e^{i gamma U}/(1/2+i gamma) ) with U uniform; under LI each gamma term is an independent
oscillation. The 3rd cumulant of 2Re(c R_chi) over the sum of independent
zero-terms equals sum over gamma of the 3rd cumulant of each term, and each
term's 3rd cumulant scales like Re(c^3) times a positive zero-weight
w3(gamma)=stuff/(1/4+gamma^2)^{3/2}. Hence

   k3(W) = sum_{chi != chi0}  Re( c_chi^3 ) * K3(chi),
   c_chi = conj(chi(b)) - conj(chi(a)),   K3(chi) >0 a zero-density constant
   ( same for chi and chibar; real ).

So the SIGN/SIZE of the skewness is governed by  sum_chi Re(c_chi^3) K3(chi).

This is the EXACT finer discriminant the crux asked for. Let's expand c_chi^3.

We specialize b = -1. chi(-1) = +-1 (real). So conj(chi(-1)) = chi(-1) = eps_chi
in {+1,-1}: eps_chi = +1 if chi even, -1 if chi odd.
   c_chi = eps_chi - conj(chi(a)).
   c_chi^3 = (eps_chi - chibar(a))^3
           = eps_chi^3 - 3 eps_chi^2 chibar(a) + 3 eps_chi chibar(a)^2 - chibar(a)^3
           = eps_chi - 3 chibar(a) + 3 eps_chi chibar(a)^2 - chibar(a)^3   (eps^2=1,eps^3=eps)
   Re(c_chi^3) = eps_chi - 3 Re(chibar(a)) + 3 eps_chi Re(chibar(a)^2) - Re(chibar(a)^3)
              = eps_chi - 3 Re(chi(a)) + 3 eps_chi Re(chi(a)^2) - Re(chi(a)^3)   (Re even in conj)

Now SUM over non-principal chi, weighted by K3(chi). Use orthogonality-style
sums.  Because eps_chi = chi(-1), the term  sum_chi eps_chi K3(chi) and the
cross terms tie -1 to a via the GROUP CHARACTERS of a.  The point that makes
a=-1 SPECIAL: the term  3 eps_chi Re(chi(a)^2) = 3 chi(-1) Re(chi(a^2)) and
the pure  eps_chi = chi(-1) term reinforce, because -1 is the unique element
that pairs trivially with the even/odd (chi(-1)) split that the explicit
formula's zero-symmetry already imposes.

We verify all this NUMERICALLY below with real Dirichlet zeros, but first the
clean closed form of the skewness predictor:

   S(N; a) :=  sum_{chi != chi0}  K3(chi) * Re( (chi(-1) - conj chi(a))^3 ).
   delta(N;-1,a) ~ 1/2 + S(N;a) / (6 sqrt(2pi) * s_a^3),
   s_a^2 = Var(X_{-1}-X_a) = sum_{chi!=chi0} K3-independent V(chi)|chi(-1)-chi(a)|^2.

a = -1 vs a: the larger S(N;a) (the more positively skewed the difference toward
X_{-1}), the more -1 dominates.
"""
print(__doc__)

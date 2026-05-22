default(parisize, "4000M");
default(realprecision, 40);

\\ S_3 example: L = splitting field of x^3-2
\\ Classify rational primes p (unramified, p ≠ 2,3) by Frobenius in S_3:
\\   p ≡ 2 mod 3                : Frob = transposition class (size 3)
\\   p ≡ 1 mod 3, 2^((p-1)/3) ≡ 1: Frob = identity (size 1)  [split completely]
\\   p ≡ 1 mod 3, 2^((p-1)/3) ≠ 1: Frob = 3-cycle (size 2)   [inert in Q(2^{1/3})]

X = 10^8;
print("Computing primes up to X = ", X);

s_id = 0.0;
s_3c = 0.0;
s_tr = 0.0;
n_id = 0; n_3c = 0; n_tr = 0;

forprime(p = 5, X, {
  if(p % 3 == 2,
    s_tr = s_tr + 1.0/sqrt(p);
    n_tr = n_tr + 1
  ,
    e = (p-1)/3;
    r = lift(Mod(2, p)^e);
    if(r == 1,
      s_id = s_id + 1.0/sqrt(p);
      n_id = n_id + 1
    ,
      s_3c = s_3c + 1.0/sqrt(p);
      n_3c = n_3c + 1
    )
  )
});

print();
print("== Prime counts (X = ", X, ") ==");
print("Identity (split):       n = ", n_id);
print("3-cycle (inert in K):   n = ", n_3c);
print("Transposition (mixed):  n = ", n_tr);
total = n_id + n_3c + n_tr;
print("Total                : ", total);
print("Density id   : ", 1.0*n_id/total, "  (Chebotarev 1/6 = ", 1./6, ")");
print("Density 3c   : ", 1.0*n_3c/total, "  (Chebotarev 1/3 = ", 1./3, ")");
print("Density tr   : ", 1.0*n_tr/total, "  (Chebotarev 1/2 = ", 1./2, ")");

print();
print("== Weighted sums Σ 1/√p ==");
print("S_id = ", s_id);
print("S_3c = ", s_3c);
print("S_tr = ", s_tr);

loglogX = log(log(1.0*X));
print();
print("log log X = ", loglogX);

print();
print("== AK Theorem 2.2 (iii) tests ==");

\\ M values: M(1)=3/2, M((12))=-1/2, M((123))=0.  Assume m_χ=m_psi=0.
\\ (iii): π_{1/2}(x;τ)/|c_τ| - π_{1/2}(x;σ)/|c_σ|
\\        = (1/[L:K])(M(σ)+m(σ) - M(τ)-m(τ)) loglogx + c + o(1)
\\ Use K=Q so [L:K]=6.

print();
print("Test A: S_tr/3 - S_id  vs (1/6)(M(1)-M(trans)) loglogX = (1/6)(3/2+1/2) loglogX = (1/3) loglogX");
diffA = s_tr/3 - s_id;
predA = (1.0/3) * loglogX;
print("  measured  : ", diffA);
print("  predicted : ", predA);
print("  residual  : ", diffA - predA);

print();
print("Test B: S_tr/3 - S_3c/2  vs (1/6)(M(3c)-M(trans)) loglogX = (1/6)(0+1/2) loglogX = (1/12) loglogX");
diffB = s_tr/3 - s_3c/2;
predB = (1.0/12) * loglogX;
print("  measured  : ", diffB);
print("  predicted : ", predB);
print("  residual  : ", diffB - predB);

print();
print("Test C: S_id - S_3c/2  vs (1/6)(M(3c)-M(1)) loglogX = (1/6)(0-3/2) loglogX = (-1/4) loglogX");
diffC = s_id - s_3c/2;
predC = -0.25 * loglogX;
print("  measured  : ", diffC);
print("  predicted : ", predC);
print("  residual  : ", diffC - predC);

print();
print("== AK Theorem 2.2 (ii) tests ==");
\\ π_{1/2,K}(x) - [L:K]/|c_σ| · π_{1/2}(x;σ)  =  (M(σ)+m(σ)) loglogx + c + o(1)
\\ With K=Q, π_{1/2,K} ≈ S_id + S_3c + S_tr (skipping ramified primes 2,3 - their contribution is O(1))
s_all = s_id + s_3c + s_tr;
print();
print("S_all (sum over unramified rationals 5..X) = ", s_all);
print();
print("Test (ii)-a: S_all - 6*S_id  vs M(1) loglogX = (3/2) loglogX");
print("  measured  : ", s_all - 6*s_id);
print("  predicted : ", 1.5*loglogX);
print("  residual  : ", s_all - 6*s_id - 1.5*loglogX);

print();
print("Test (ii)-b: S_all - 2*S_tr  vs M((12)) loglogX = (-1/2) loglogX");
print("  measured  : ", s_all - 2*s_tr);
print("  predicted : ", -0.5*loglogX);
print("  residual  : ", s_all - 2*s_tr - (-0.5*loglogX));

print();
print("Test (ii)-c: S_all - 3*S_3c  vs M((123)) loglogX = 0");
print("  measured  : ", s_all - 3*s_3c);
print("  predicted : 0 (just a constant)");

quit;

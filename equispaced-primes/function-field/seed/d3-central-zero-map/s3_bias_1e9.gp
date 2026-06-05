default(parisize, "4000M");
default(realprecision, 40);

\\ S_3 example: L = splitting field of x^3-2
\\ Extended sweep to X = 10^9 with decade checkpoints.
\\ Frobenius classification (p != 2, 3, unramified):
\\   p ≡ 2 mod 3                : Frob = transposition class (size 3)
\\   p ≡ 1 mod 3, 2^((p-1)/3) ≡ 1: Frob = identity (size 1)  [split completely]
\\   p ≡ 1 mod 3, 2^((p-1)/3) ≠ 1: Frob = 3-cycle (size 2)   [inert in Q(2^{1/3})]

X = 10^9;
print("Computing primes up to X = ", X);
gettime();

s_id = 0.0; s_3c = 0.0; s_tr = 0.0;
n_id = 0; n_3c = 0; n_tr = 0;

\\ Decade checkpoints
checkpoints = [10^6, 10^7, 10^8, 10^9];
nextcp = 1;

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
  );
  \\ Decade checkpoint
  if(nextcp <= 4 && p > checkpoints[nextcp],
    loglogXc = log(log(1.0*checkpoints[nextcp]));
    s_allc = s_id + s_3c + s_tr;
    print();
    print("=== CHECKPOINT X = ", checkpoints[nextcp], " (wallclock so far: ", gettime()/1000.0, "s) ===");
    print("counts: id=", n_id, " 3c=", n_3c, " tr=", n_tr);
    print("S_id=", s_id, " S_3c=", s_3c, " S_tr=", s_tr);
    print("log log X = ", loglogXc);
    print("(ii)-a S_all - 6 S_id  vs (3/2) loglogX = ", 1.5*loglogXc);
    print("  measured  ", s_allc - 6*s_id);
    print("  residual  ", s_allc - 6*s_id - 1.5*loglogXc);
    print("(ii)-b S_all - 2 S_tr  vs (-1/2) loglogX = ", -0.5*loglogXc);
    print("  measured  ", s_allc - 2*s_tr);
    print("  residual  ", s_allc - 2*s_tr + 0.5*loglogXc);
    print("(ii)-c S_all - 3 S_3c  vs 0");
    print("  measured  ", s_allc - 3*s_3c);
    print("(iii)-A  S_tr/3 - S_id  vs (1/3) loglogX = ", (1.0/3)*loglogXc);
    print("  measured  ", s_tr/3 - s_id);
    print("  residual  ", s_tr/3 - s_id - (1.0/3)*loglogXc);
    print("(iii)-B  S_tr/3 - S_3c/2  vs (1/12) loglogX = ", (1.0/12)*loglogXc);
    print("  measured  ", s_tr/3 - s_3c/2);
    print("  residual  ", s_tr/3 - s_3c/2 - (1.0/12)*loglogXc);
    print("(iii)-C  S_id - S_3c/2  vs (-1/4) loglogX = ", -0.25*loglogXc);
    print("  measured  ", s_id - s_3c/2);
    print("  residual  ", s_id - s_3c/2 + 0.25*loglogXc);
    nextcp = nextcp + 1;
  )
});

print();
print("=== FINAL (X = ", X, ", total wallclock: ", gettime()/1000.0, "s) ===");

quit;

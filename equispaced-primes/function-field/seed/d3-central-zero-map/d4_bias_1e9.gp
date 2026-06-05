default(parisize, "4000M");
default(realprecision, 40);

\\ D_4 example: L = Q(2^{1/4}, i), Galois group D_4. Extended sweep to X = 10^9.

X = 10^9;
print("D_4 bias check, X = ", X);
gettime();

s1 = 0.0; sr2 = 0.0; sr = 0.0; ss = 0.0; srs = 0.0;
n1=0; nr2=0; nr=0; ns=0; nrs=0;

checkpoints = [10^6, 10^7, 10^8, 10^9];
nextcp = 1;

forprime(p = 3, X, {
  if(p == 2, ,
    m = p % 8;
    if(m == 5,
      sr = sr + 1.0/sqrt(p); nr = nr + 1
    ,
    if(m == 7,
      k_n2 = kronecker(-2, p);
      if(k_n2 == -1,
        ss = ss + 1.0/sqrt(p); ns = ns + 1
      ,
        srs = srs + 1.0/sqrt(p); nrs = nrs + 1
      )
    ,
    if(m == 3,
      srs = srs + 1.0/sqrt(p); nrs = nrs + 1
    ,
    if(m == 1,
      e = (p-1)/4;
      r4 = lift(Mod(2, p)^e);
      if(r4 == 1,
        s1 = s1 + 1.0/sqrt(p); n1 = n1 + 1
      ,
        sr2 = sr2 + 1.0/sqrt(p); nr2 = nr2 + 1
      )
    )))));
  if(nextcp <= 4 && p >= checkpoints[nextcp],
    loglogXc = log(log(1.0*checkpoints[nextcp]));
    s_all_c = s1 + sr2 + sr + ss + srs;
    print();
    print("=== CHECKPOINT X = ", checkpoints[nextcp], " (wallclock: ", gettime()/1000.0, "s) ===");
    print("counts: 1=", n1, " r2=", nr2, " r=", nr, " s=", ns, " rs=", nrs);
    print("S_all = ", s_all_c, "  log log X = ", loglogXc);
    print("(ii) sigma=1:  S_all-8*S_1 vs (5/2) loglogX = ", 2.5*loglogXc);
    print("  measured ", s_all_c - 8*s1, "  resid ", s_all_c - 8*s1 - 2.5*loglogXc);
    print("(ii) sigma=r^2: S_all-8*S_r2 vs (1/2) loglogX = ", 0.5*loglogXc);
    print("  measured ", s_all_c - 8*sr2, "  resid ", s_all_c - 8*sr2 - 0.5*loglogXc);
    print("(ii) sigma=r:  S_all-4*S_r vs (-1/2) loglogX = ", -0.5*loglogXc);
    print("  measured ", s_all_c - 4*sr, "  resid ", s_all_c - 4*sr + 0.5*loglogXc);
    print("(ii) sigma=s:  S_all-4*S_s vs (-1/2) loglogX = ", -0.5*loglogXc);
    print("  measured ", s_all_c - 4*ss, "  resid ", s_all_c - 4*ss + 0.5*loglogXc);
    print("(ii) sigma=rs: S_all-4*S_rs vs (-1/2) loglogX = ", -0.5*loglogXc);
    print("  measured ", s_all_c - 4*srs, "  resid ", s_all_c - 4*srs + 0.5*loglogXc);
    nextcp = nextcp + 1;
  )
});

print("=== FINAL X = ", X, " wallclock=", gettime()/1000.0, "s ===");
quit;

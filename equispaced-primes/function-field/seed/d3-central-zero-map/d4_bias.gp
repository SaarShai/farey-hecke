default(parisize, "4000M");
default(realprecision, 40);

\\ D_4 example: L = Q(2^{1/4}, i), Galois group D_4
\\ Generators: r = (rotation, sends 2^{1/4} → i·2^{1/4}), s = complex conjugation (fixes 2^{1/4})
\\ Quadratic subfields: Q(√2)=L^{<r²,s>}, Q(i)=L^{<r>}, Q(√-2)=L^{<r²·s>} ... etc.
\\
\\ Three quadratic chars of D_4 (going through D_4/[D_4,D_4]=V_4):
\\   χ_1 ↔ Q(√2) :: kills <s, r²>; i.e., χ_1(p) = (2/p) Kronecker
\\   χ_2 ↔ Q(i)  :: kills <r>; i.e., χ_2(p) = (-1/p)
\\   χ_3 ↔ Q(√-2):: kills <rs, r²>; χ_3(p) = (-2/p)
\\
\\ The 2-dim irrep ρ has character χ_ρ:
\\   χ_ρ(1) = 2, χ_ρ(r²) = -2, χ_ρ(r) = 0, χ_ρ(s) = 0, χ_ρ(rs) = 0
\\
\\ For an unramified rational prime p, its Frobenius (up to conjugacy) is determined by
\\ its splitting in L. The 5 conjugacy classes correspond to splitting patterns in L/Q.
\\ Equivalent reformulation: Frobenius (mod conjugacy) determined by:
\\   (chi_1(p), chi_2(p), chi_3(p))  for the 1-dim chars, and
\\   the cycle structure of Frob_p acting on the 8 roots
\\
\\ For our specific L = Q(2^{1/4}, i):
\\   p splits completely in L  ⇔  p ≡ 1 mod 8  AND  2 is a 4th power mod p
\\   p has Frob = r²            ⇔  p ≡ 1 mod 8  AND  2 is NOT 4th power mod p (but is a square)
\\   p has Frob = r (order 4)   ⇔  p ≡ 5 mod 8  (then 2 is a non-square mod p — Q(√2) inert)
\\   p has Frob = s             ⇔  p ≡ 7 mod 8  (then (-1/p)=-1, (2/p)=+1 → 2 is square)
\\   p has Frob = rs            ⇔  p ≡ 3 mod 8
\\
\\ Class sizes: {1}, {r²}, {r,r³}, {s,r²s}, {rs,r³s} → sizes 1,1,2,2,2 (total 8)
\\ Densities:  1/8,1/8, 1/4, 1/4, 1/4

X = 10^7;
print("D_4 bias check, X = ", X);

\\ Initialize sums
s1   = 0.0;  \\ Frob = 1 (split)
sr2  = 0.0;  \\ Frob = r² (8 prime factors in 4 pairs)
sr   = 0.0;  \\ Frob = r (rotation, 2 primes of degree 4 ?)
ss   = 0.0;  \\ Frob = s (reflection)
srs  = 0.0;  \\ Frob = rs
n1=0; nr2=0; nr=0; ns=0; nrs=0;

forprime(p = 3, X, {
  if(p == 2,
    \\ ramified — skip
  ,
    \\ p mod 8
    m = p % 8;
    if(m == 5,
      \\ Q(√2) inert: -2 isn't a 4th-residue, in fact (2/p)=-1, so Q(√2) is inert, Frob=r (order 4)
      sr = sr + 1.0/sqrt(p); nr = nr + 1
    ,
    if(m == 7,
      \\ (-1/p)=-1, (2/p)=+1, so Q(i) inert, Q(√2) split. Frob is order-2 reflection.
      \\ Disting between s and rs by (-2/p) = (-1/p)·(2/p) = -1; so Q(√-2) inert → Frob fixes Q(√-2) iff s²s? Actually Frob "is" one of the reflections.
      \\ Convention: take "s" class if (-2/p)=-1, "rs" class if (-2/p)=+1.
      \\ (-2/p) when p≡7 mod 8: -2 ≡ 5 mod 8 → (5/p) = (p/5) = (2/5) = -1 (p=7 mod 8 ⇒ p mod 5 varies)
      \\ Actually just: -2 ≡ 5 mod 8 → (-2/p) depends on p mod 5
      \\ Let me redo: for p ≡ 7 (mod 8), (-2/p) by quadratic reciprocity... simpler: compute it via kronecker
      k_n2 = kronecker(-2, p);
      if(k_n2 == -1,
        ss = ss + 1.0/sqrt(p); ns = ns + 1
      ,
        srs = srs + 1.0/sqrt(p); nrs = nrs + 1
      )
    ,
    if(m == 3,
      \\ (-1/p)=-1, (2/p)=-1, (-2/p)=+1 → Q(√-2) split, Q(i) inert, Q(√2) inert
      \\ Frob is a reflection in the other coset → "rs"
      \\ Always p≡3 mod 8 gives one reflection class
      \\ Symmetry: for p≡3 mod 8, (-2/p) = +1, classify as rs
      srs = srs + 1.0/sqrt(p); nrs = nrs + 1
    ,
    if(m == 1,
      \\ All three quadratic subfields split. p ≡ 1 mod 8.
      \\ Now check if 2 is a 4th power mod p, i.e., 2^((p-1)/4) ≡ 1 (mod p)
      e = (p-1)/4;
      r4 = lift(Mod(2, p)^e);
      if(r4 == 1,
        s1 = s1 + 1.0/sqrt(p); n1 = n1 + 1
      ,
        sr2 = sr2 + 1.0/sqrt(p); nr2 = nr2 + 1
      )
    )))))
});

print();
print("== D_4 prime counts ==");
print("Frob 1 (split):           n = ", n1);
print("Frob r² (center):         n = ", nr2);
print("Frob r (rotation order 4): n = ", nr);
print("Frob s (refl class A):    n = ", ns);
print("Frob rs (refl class B):   n = ", nrs);
tot = n1 + nr2 + nr + ns + nrs;
print("Total: ", tot);

print();
print("Densities (Chebotarev expected: 1/8, 1/8, 1/4, 1/4, 1/4):");
print("  d_1 :  ", 1.0*n1/tot);
print("  d_r²:  ", 1.0*nr2/tot);
print("  d_r :  ", 1.0*nr/tot);
print("  d_s :  ", 1.0*ns/tot);
print("  d_rs:  ", 1.0*nrs/tot);

print();
print("== Weighted sums ==");
print("S_1   = ", s1);
print("S_r²  = ", sr2);
print("S_r   = ", sr);
print("S_s   = ", ss);
print("S_rs  = ", srs);

s_all = s1 + sr2 + sr + ss + srs;
loglogX = log(log(1.0*X));
print();
print("S_all = ", s_all);
print("log log X = ", loglogX);

\\ AK predictions (assuming m_ρ = m_χi = 0):
\\ M(1) = 5/2, M(r²) = 1/2, M(r) = M(s) = M(rs) = -1/2
\\ [L:K]=8
\\ Test (ii): S_all - [L:K]/|c_σ| * S_σ ~ M(σ) loglogX
\\   σ=1:    S_all - 8 S_1   ~ (5/2) loglogX
\\   σ=r²:   S_all - 8 S_r²  ~ (1/2) loglogX
\\   σ=r:    S_all - 4 S_r   ~ (-1/2) loglogX  (since |c_r|=2)
\\   σ=s:    S_all - 4 S_s   ~ (-1/2) loglogX
\\   σ=rs:   S_all - 4 S_rs  ~ (-1/2) loglogX
print();
print("== AK Theorem 2.2 (ii) tests (predicted asymptotic coefficient · log log X) ==");
print();
print("σ=1:    S_all - 8*S_1   vs (5/2)*loglogX = ", 2.5*loglogX);
print("  measured  ", s_all - 8*s1);
print("  resid     ", s_all - 8*s1 - 2.5*loglogX);
print();
print("σ=r²:   S_all - 8*S_r²  vs (1/2)*loglogX = ", 0.5*loglogX);
print("  measured  ", s_all - 8*sr2);
print("  resid     ", s_all - 8*sr2 - 0.5*loglogX);
print();
print("σ=r:    S_all - 4*S_r   vs (-1/2)*loglogX = ", -0.5*loglogX);
print("  measured  ", s_all - 4*sr);
print("  resid     ", s_all - 4*sr + 0.5*loglogX);
print();
print("σ=s:    S_all - 4*S_s   vs (-1/2)*loglogX = ", -0.5*loglogX);
print("  measured  ", s_all - 4*ss);
print("  resid     ", s_all - 4*ss + 0.5*loglogX);
print();
print("σ=rs:   S_all - 4*S_rs  vs (-1/2)*loglogX = ", -0.5*loglogX);
print("  measured  ", s_all - 4*srs);
print("  resid     ", s_all - 4*srs + 0.5*loglogX);

quit;

\\p 38

/*
  PARI/GP low-zero certificate for the 300-trillion prime-race curves.

  For every nonprincipal Dirichlet character modulo q in Q, compute the
  critical-line zeros in (0, HEIGHT] twice, using two different lfunzeros
  subdivision parameters.  A CHECK row records whether the two lists agree.

  Output is tab-separated and is consumed by spectral_reconstruction.py.
*/

Q = [7, 8, 11, 19, 23];
HEIGHT = 80;
DIVZ_A = 64;
DIVZ_B = 96;
TOL = 1e-28;

print("# generator=PARI/GP lfunzeros height=", HEIGHT, " divz_a=", DIVZ_A, " divz_b=", DIVZ_B, " precision_digits=38");
print("# PHASE\tq\tconrey_m\tconductor\tcharacter_order\ta\tchi_phase_turns");
print("# CHECK\tq\tconrey_m\tcount_a\tcount_b\tmax_abs_difference\tmax_abs_lfun_at_zero\tstatus");
print("# ZERO\tq\tconrey_m\tindex\tgamma");

emit_character(q, m) = {
  my(D, G, chi, conductor, character_order, L, ZA, ZB, same, maxdiff, maxresidual);
  D = znchar(Mod(m, q));
  G = D[1];
  chi = D[2];
  conductor = zncharconductor(G, chi);
  character_order = charorder(G, chi);
  for (a = 1, q - 1, if (gcd(a, q) == 1, print("PHASE\t", q, "\t", m, "\t", conductor, "\t", character_order, "\t", a, "\t", chareval(G, chi, a))));
  L = lfuncreate(D);
  ZA = lfunzeros(L, HEIGHT, DIVZ_A);
  ZB = lfunzeros(L, HEIGHT, DIVZ_B);
  same = (#ZA == #ZB);
  maxdiff = 0;
  if (same, for (i = 1, #ZA, maxdiff = max(maxdiff, abs(ZA[i] - ZB[i]))); same = (maxdiff < TOL));
  maxresidual = 0;
  for (i = 1, #ZB, maxresidual = max(maxresidual, abs(lfun(L, 1/2 + I*ZB[i]))));
  print("CHECK\t", q, "\t", m, "\t", #ZA, "\t", #ZB, "\t", Strprintf("%.30g", maxdiff), "\t", Strprintf("%.30g", maxresidual), "\t", if(same && maxresidual < 1e-28, "PASS", "FAIL"));
  for (i = 1, #ZB, print("ZERO\t", q, "\t", m, "\t", i, "\t", ZB[i]));
};

for (qi = 1, #Q, q = Q[qi]; for (m = 2, q - 1, if (gcd(m, q) == 1, emit_character(q, m))));

\\p 38

/*
  Deep q=19 PARI/GP zero list for K=25/50/100 stability testing.

  The independent low-zero existence certificate is certify_n19.py and uses
  FLINT/Arb, not this file.  This generator extends the original PARI spectral
  reconstruction to at least 100 positive zeros per nonprincipal character.
*/

Q = 19;
M_TEXT = getenv("N19_CONREY_M");
if(#M_TEXT == 0, error("set N19_CONREY_M to one Conrey index in 2..18"));
M = 0;
for(candidate = 2, 18, if(M_TEXT == Str(candidate), M = candidate));
if(M == 0 || gcd(M, Q) != 1, error("invalid N19_CONREY_M"));
HEIGHT = 160;
DIVZ_A = 128;
DIVZ_B = 192;
TOL = 1e-28;
MIN_COUNT = 100;

print("# generator=PARI/GP q=19 conrey_m=", M, " height=", HEIGHT, " divz_a=", DIVZ_A, " divz_b=", DIVZ_B, " precision_digits=38 min_count=", MIN_COUNT);
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
  print("CHECK\t", q, "\t", m, "\t", #ZA, "\t", #ZB, "\t", Strprintf("%.30g", maxdiff), "\t", Strprintf("%.30g", maxresidual), "\t", if(same && maxresidual < TOL && #ZB >= MIN_COUNT, "PASS", "FAIL"));
  for (i = 1, #ZB, print("ZERO\t", q, "\t", m, "\t", i, "\t", ZB[i]));
};

emit_character(Q, M);

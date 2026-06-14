# Scout: "certified constant closes a named open problem" — VERDICT (2026-06-14)

Question: where does a FINITE rigorous computation + interval/Lean CERTIFICATE
resolve/advance a NAMED open problem, given our edge (interval arith + Lean/Aristotle
+ Ruelle/JP transfer-operator dimension to ~1e-15)?

## VERDICT: MAYBE (not TOP-TIER). edge_real ~6, reachability ~5, reach ~5.

The certified-dimension niche FITS our tooling exactly — but it is ALREADY HEAVILY
MINED by the inventors of the method. Honest blockers below.

### The fit cluster (transfer-operator + interval certificate)
- Pollicott-Vytnova arXiv:2012.07083 (Lagrange/Markov spectra, Zaremba, Fuchsian):
  rigorous Hausdorff dim to 100-200 DIGITS via dynamical zeta + bisection. This IS
  our method, done first and to absurd precision.
- Chousionis-Leykekhman-Urbanski-Wendt arXiv:2408.06330 (rev Apr 2025): FEM/Perron-
  Frobenius rigorous dim for conformal GDMS in R^n, n>=2. Active competitor.
- Apollonian gasket dim = 1.3056867280... rigorously certified (June 2024). Done.
- Matheus-Moreira-Vytnova arXiv:2212.11371: 12 plateaux of dimension function d(t)
  of M/L spectra, rigorously. t_1 (Markov dim-1 transition) already certified.

### Why each named target is NOT a clean "pin-a-constant" win:
- ZAREMBA: does NOT reduce to a dimension threshold. dim(F_A) already exceeds any
  needed bound; obstruction is sum-product/circle-method DENSITY argument (Bourgain-
  Kontorovich), arithmetic not dynamical. Hensley "dim>1/2" conj is FALSE
  ({2,4,6,8,10} counterexample). Our edge here = WISHFUL.
- LEHMER / Mahler measure 1.17628: search space exhausted far below; lower bound is
  "no small Salem number" — genuinely hard, NOT certificate-shaped. No transfer op.
- CHOWLA COSINE: just got POLYNOMIAL bounds Sept 2025 by COMBINATORIAL methods
  (Bedert arXiv:2509.05260 n^{1/12}; Jin-Milojevic-Tomon-Zhang arXiv:2509.03490
  n^{1/10}). Not a certified-constant problem; not our tooling.
- BARKER sequences: 2-adic/algebraic obstruction (Eliahou et al rule out N<5000 except
  6); not interval-shaped.
- dim(M\L) (Markov-minus-Lagrange diff set, heuristic ~0.593): genuinely open EXACT
  value, our method applies — but the exact value is NOT a famous inequality-flip;
  reach is niche (Diophantine-approximation community only).

### Closest REAL opening for us (the MAYBE):
A SPECIFIC certified dimension/spectral constant that FLIPS an inequality inside
someone's THEOREM (the "feeds a named conjecture" pattern, a la how Bourgain-
Kontorovich needed dim(F_50) close to 1). Candidates that are still live AND where a
tighter certified constant is load-bearing:
  - thin-group SPECTRAL GAP / base-eigenvalue bounds feeding local-global (Apollonian,
    Sarnak's spectral-gap question arXiv:2210.13969) — but higher-rank/representation-
    theoretic, beyond our 2D transfer operator (matches prior HIGHER-RANK = DROP memo).
  - Selberg/Hecke-Schottky explicit spectral gap (arXiv:2305.02228) — closest to our
    Hecke machinery; a certified bottom-eigenvalue could feed an effective count, but
    needs the rep-theory side too.

### Honest scores
- edge_real = 6: method fits PERFECTLY but the named targets either don't reduce to a
  constant (Zaremba/Lehmer/Chowla/Barker) or are already certified (PV/Apollonian).
  The only un-mined certified-constant targets (dim(M\L) exact, a specific gap-flip)
  are reachable but the EDGE over PV/CLUW is marginal — they own the engine.
- reachability = 5: we could plausibly nail dim(M\L) or reproduce/extend a PV constant;
  flipping a named inequality is lower-odds.
- reach = 5: solutions land in Diophantine-approx / thin-groups community. NOT broad
  (not crypto/coding/physics). Apollonian/local-global is the broadest but unreachable.

### Bottom line
Do NOT pivot the whole pipeline here as a flagship. The certified-constant lane is
where our tooling is most NATIVE, but the high-reach named problems in it are either
already won by the method's inventors or not constant-shaped. Best use: a TARGETED
strike on dim(M\L) exact value or a single gap-flip lemma INSIDE an existing theorem,
as a satellite result — not a TOP-TIER flagship. Keeps value MATHEMATICAL, modest reach.

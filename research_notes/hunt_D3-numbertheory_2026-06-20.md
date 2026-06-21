# Hunt D3 — Computational Number Theory & Diophantine (structured-search-bound)

Date: 2026-06-20. Agent path: /goal D3. Mode: literature + reasoning survey.

## Verdict (one line)
TOP PICK = **Ideal Prouhet–Tarry–Escott (PTE) at size n = 11 over ℤ** — the smallest open
ideal-PTE size, a pure structured-search / exact-arithmetic problem with instantly
machine-checkable witnesses, in a NEGLECTED corner (no DeepMind/AlphaEvolve pipeline aimed
at it). Realistic concrete contributions in weeks: (a) extend the certified search above
height 3500 and either FIND the missing solution or push a clean "no solution below H"
certificate; (b) a sharp existence/non-existence conjecture backed by the local-obstruction
+ near-miss structure.

## Lanes surveyed and why most were rejected

- **Erdős–Straus 4/n = 1/x+1/y+1/z** (arXiv:2509.00128 Sep-2025 verification to ~1e18;
  arXiv:2602.20036, arXiv:2404.01508 parametric/congruence). REJECT for us: remaining gap
  is the n≡1 (mod 4) exceptional set, which is DENSITY-ZERO and the open core is analytic
  (no finite covering system possible — Mordell's quadratic-residue obstruction). A witness
  search only re-confirms "no counterexample below H" (already 1e18). Weak contribution shape.

- **Zaremba's conjecture** (bounded partial quotients; AMM Apr-2024 folding-lemma; arXiv:2512.11357).
  REJECT: full-density already done (Bourgain–Kontorovich); residual is analytic/thin-groups.

- **Aliquot 276 / Lehmer five / Catalan–Dickson.** REJECT: bottleneck = factoring 200-digit
  cofactors = raw FLOPS, explicitly outside our edge.

- **Coprime (vertex) Ramsey R_cop(k).** Looked promising from the metafunctor blog (R_cop(4)=59,
  R_cop(5)>138 via SAT). But arXiv:2605.26815v2 (Du–Xi–Deng–Ma, 25-May-2026) gives a CLOSED-FORM
  R_cop(k₁..k_c)=p_{Σ(kᵢ-1)} (the M-th prime) with prime certificates — the (vertex) problem is
  SOLVED. The blog's R_cop(4)=59/R_cop(5)>138 is a DIFFERENT normalization (edge/threshold
  variant), but the headline vertex-coprime lane is closed. REJECT as a clean open target.
  (Caveat: the exact relation of the blog's variant to the Du et al. closed form is unverified —
  a possible minor side-check, not a research target.)

- **Cap sets in AG(n,3), n=7,8,9.** GENUINELY open (n=7: best lower bound 236, upper <289;
  n=8 pushed 496→512). Good verifiability + modest compute. REJECT as TOP only because it is a
  CROWDED arena: FunSearch (DeepMind, Dec-2023, C≥2.2202) and X-evolve (arXiv:2508.07932,
  Aug-2025, C≥2.2203) are heavily optimized LLM+EA pipelines already matching SOTA for n≤8.
  Our modest compute competes poorly there. Keep as a SECONDARY candidate.

- **Erdős minimum-overlap.** REJECT: now an AlphaEvolve / TTT-Discover (arXiv:2601.16175)
  battleground; bound 0.380924; convex-optimization-bound, not our edge.

- **Elliptic-curve rank records** (Elkies–Klagsbrun rank ≥29, 2024). REJECT: needs K3/Mordell–Weil
  sieve machinery at Elkies scale; not our construction edge.

- **No-three-in-line.** Open in general but the frontier is asymptotic density (3n/2 vs 2n);
  small-grid records are well-trodden and the gap is not cleanly witness-shaped for us. SECONDARY.

## TOP PICK detail — Ideal PTE at n = 11 over ℤ

Problem: find disjoint integer multisets A,B of size n with Σa^k = Σb^k for k=1..n−1 (degree
n−1 = "ideal"). Status (Wikipedia; Caley–Jones–Rouse-type work arXiv:2304.11254 = Math. Comp.
93 (2024), no. 349; survey arXiv:2506.11429 Jun-2025): ideal solutions are KNOWN for n=3..10
and n=12, but **NO ideal solution is known for n=11, nor for any n≥13.** n=11 is the smallest
open case and was still open as of the Jun-2025 survey and our Jun-2026 search.

Why it fits our edge (exact, structured-search, verifiable, neglected):
- A witness is a finite integer multiset; verification = check 10 power-sum equalities exactly
  (trivially Lean/Aristotle-formalizable — a clean "machine-checked witness" deliverable).
- The search is heavily STRUCTURED, not brute force: known required prime divisors of the
  PTE constant C₁₁ (17 | C₁₁, and Caley: 19 | C₁₁), and local obstructions force any solution
  to reduce, mod 29, to a unique local solution; symmetric solutions (B = −A) have A = −A even
  part forced. The 2023 work used (p₁,p₂)=(31,29) as required divisors to slash the space.
- Modest compute suffices: prior symmetric search reached only **height 3500** (Caley et al.),
  up from height 2000 (Borwein et al.). For scale: the smallest known n=12 symmetric ideal
  solution has height 1511 (A=±{107,622,700,1075,1138,1511}); next 14770. So an n=11 solution,
  if it exists, may well sit just past height ~3500–15000 — within reach of a smarter sieve.
- NEAR-MISSES already found: at n=11 there exist solutions with 9 integers + 2 real-quadratic
  irrationals, e.g. A={−95,−68−α,−52,−48,−13,−9,30,34,61,65,95+α}, α=root of x²+163x−8. This is
  strong evidence the integer locus is "almost" populated — a guided search around these
  algebraic near-misses (rationalizing the quadratic part) is exactly a clever-construction play.

Honest tractability: this is a needle-in-haystack with NO guarantee the n=11 solution exists at
all (it may genuinely not exist, like n=11 being a true gap). The realistic contribution is
EITHER (i) the witness (big win, low probability in weeks) OR (ii) a substantially extended
CERTIFIED non-existence-below-H bound + a defensible existence/non-existence conjecture from the
divisor/local + near-miss data (modest, high probability). Both are verifiable and publishable.
Hard part = an efficient exact sieve exploiting the forced divisors (31,29,19,17,13,11) to push
H from 3500 to ≥ 5e4–1e6 with a minimality certificate (the erdos396/jdehorty "every candidate
below H ruled out" model is the template).

## Secondary candidates (kept on the bench)
1. Cap set AG(7,3): improve/confirm the 236 lower bound or tighten toward the <289 upper bound,
   verifiable, but crowded (FunSearch/X-evolve). 
2. No-three-in-line specific small/medium grids with certified maxima.
3. Side-check: reconcile the metafunctor R_cop(5)>138 "edge/threshold" variant against the
   Du et al. closed-form vertex result (clarification, not research).

## Sources
- arXiv:2304.11254 "Ideal solutions in the Prouhet–Tarry–Escott problem" (= Math. Comp. 93
  (2024) 349) — n=11 searched to height 3500, no solution; near-misses; divisor constraints.
  (PDF text extracted and read directly.)
- arXiv:2506.11429 survey of PTE (Jun-2025) — confirms n=11, n≥13 open.
- en.wikipedia.org/wiki/Prouhet–Tarry–Escott_problem — ideal solutions known n=3..10,12; n=11 smallest open.
- arXiv:2605.26815v2 (Du–Xi–Deng–Ma, May-2026) — vertex-coprime Ramsey closed-form (kills that lane).
- arXiv:2508.07932 X-evolve (Aug-2025) cap-set C≥2.2203; FunSearch (Dec-2023) C≥2.2202.
- arXiv:2509.00128 Erdős–Straus verification (Sep-2025); arXiv:2602.20036 parametric.
- arXiv:2601.16175 TTT-Discover / AlphaEvolve min-overlap 0.380924.
- terrytao.wordpress.com 31-Aug-2025 Erdős-problems↔OEIS crowdsourcing; github jdehorty/erdos396 (witness-certificate template).
```

# -1 Dominance — Verdict & Synthesis

STATUS: The automated workflow (run wf_9ffc1616-c18) completed Theory, Compute, and Prove (incl.
adversarial verification) but ABORTED at its Lean step (local `lake env lean` against
`primes-equispaced` hung on a 0-olean `.lake` cache), so its auto-Synthesize never ran. This file is
the synthesis, hand-assembled from the completed phases + workspace artifacts (THEORY_SCHEMA.md,
RECONCILE_COMPUTE.md, canonical_verify.py, empirical_rank.py) + a free empirical variance check on the
existing verified curve. Everything below is sourced; nothing new is asserted.

## VERDICT (conditional GRH+LI; adversarially verified — REFUTED)
"-1 dominates the non-residue hierarchy" is FALSE and, for the standard Rubinstein-Sarnak sign-density,
exactly backwards: **a = -1 (mod N) is the LEAST-biased non-residue** — the unique MINIMUM of
delta(N;a,1) for N = 7, 11, 19, 23. NR-vs-NR is vacuous: delta(N;-1,a) = 1/2 exactly for distinct
non-residues (RS symmetry). For primes q == 3 (mod 4) this is **Fiorilli-Martin, Crelle 676 (2013),
Thm 1.10** (primary-verified verbatim, FM_text.txt).

Mechanism (three identities, independently re-derived + verified): (1) leading RS mean = -1 + #{sqrt a}
= -1 for every non-residue (all tie at leading order); (2) sum_{chi!=chi0} |chi(a)-1|^2 = 2*phi(N)
(total weight identical across classes); (3) even-character weight = 0 **iff** a = -1, so all of -1's
weight sits on ODD characters (larger c_chi, the 2*ln2 = psi(1)-psi(1/2) gap) => **a=-1 has MAXIMAL RS
variance V => MINIMAL delta**. Skew = 0 (symmetric law); Aoki-Koyama DRH magnitude ruled out as a
discriminant (m(a)=0 generically). NOTHING is unconditional over Q.

Sanity: reproduced RS densities delta(4;3,1)=0.99593 (RS 0.99590), delta(3;2,1)=0.99907 (RS 0.99906);
exhaustive zero-violation scan q < 2000.

## Per-N (from RECONCILE_COMPUTE.md)
| N | -1 | delta(N;-1,1) | delta-rank (1=min=least biased) | theory V-rank (1=max amplitude) | emp D-rank @1.3e13 |
|---|----|---------------|---------------------------------|---------------------------------|--------------------|
| 7 | 6  | 0.83364 | 1/3 MIN          | 1/3 MAX          | 2/3 |
| 8 | 7  | 0.99894 | 2/3 (a=5 is min) | 2/3 (a=5 is max) | 1/6 strict* |
| 11| 10 | 0.70044 | 1/5 MIN          | 1/5 MAX          | 3/5 |
| 19| 18 | 0.60368 | 1/9 MIN          | 1/9 MAX          | 3/9 |
| 23| 22 | 0.59368 | 1/11 MIN         | 1/11 MAX         | 7/11 |

*N=8 is NOT prime == 3 mod 4; theory does not single out -1 there. Its empirical "lead" is amplitude +
finite-x noise (the large negative columns a=2,4,6 are non-units = parsing artifact, irrelevant to the
unit race {1,3,5,7}).

## Amplitude reading + the open empirical test (what the M2 sieve is for)
The ONLY sense in which -1 "leads" is amplitude: V(N;-1,1) = MAX (largest typical |D| excursions) — in
THEORY for N = 7,11,19,23. A free empirical variance check on the existing verified curve (<= 1.3e13)
corroborates this for **N = 7, 11** (asymptotic regime reached) but NOT for N = 8, 19, 23, whose onset
is ~ e^33.4 ~ 3e14, beyond our data. **The M2 sieve to 3e14 tests exactly this**: does empirical V
become maximal for N = 19, 23 at the onset scale, as the conditional theory predicts? (Empirically at
1.3e13, -1 is mid-pack for 7/11/19/23 and onset is not yet reached for any N.)

## PROVEN / NUMERICAL / FORMALIZED (honest separation)
- **PROVEN (conditional GRH+LI):** delta decreasing in V; the variance parity identities; -1 = delta-min
  for primes q==3 mod 4 (= FM Thm 1.10). The variance closed form needs GRH only.
- **NUMERICAL:** c_chi (validated vs low-zero sums); the per-N delta values; the empirical curve (two
  independent sieves agree to the integer at <= 1.3e13).
- **FORMALIZED:** not yet. `Minus1Core.lean` (combinatorial core: c(N,a)=#{sqrt a}, = 0 on non-residues
  => equal leading means) is TODO — the workflow's Lean step hung; see GOAL_HANDOFF.md step 1.

## Citations (primary-source verified, texts in this dir)
- Fiorilli-Martin, Crelle (J. reine angew. Math.) 676 (2013), Thm 1.10 — FM_text.txt.
- Rubinstein-Sarnak, Experimental Mathematics 3 (1994), 173-197.
- Granville-Martin, Amer. Math. Monthly (2006) — PNR_text.txt.
- Aoki-Koyama, J. Number Theory 245 (2023), arXiv:2203.12266 — AK_text.txt.

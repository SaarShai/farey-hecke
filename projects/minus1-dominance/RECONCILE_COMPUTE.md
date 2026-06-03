# -1 Dominance: Theory vs Empirical reconciliation (COMPUTE merge)

LOCAL-ONLY. Adversarial honesty. PROVEN / NUMERICAL / CONDITIONAL separated.

## Verdict (one line)
"-1 dominates among non-residues" is FALSE for the asymptotic Rubinstein-Sarnak
sign-density and is, if anything, EXACTLY BACKWARDS: a=-1 is the UNIQUE MINIMUM
(least-biased) non-residue in delta(N;a,1) for N=7,11,19,23 (Fiorilli-Martin
Crelle 676 Thm 1.10, GRH+LI). NR-vs-NR, delta(N;-1,a)=1/2 EXACTLY (RS symmetry,
Granville-Martin), so no non-residue sign-dominates another. The ONLY true reading
is the amplitude/variance one (a=-1 has MAXIMAL RS variance V, the largest typical
|D|), and that is the SAME parity fact that makes -1 LOSE the sign race. Even that
amplitude reading FAILS at N=8 (a=5 has larger V; -1=7 is rank 2).

Empirically at the largest verified x = 1.3e13, the asymptotic sign-density bias is
NOT yet visible (onset ~ e^33.4 ~ 3e14): -1 is mid-pack for N=7,11,19,23 and the
ranks track neither the asymptotic delta nor cleanly the amplitude V. N=8 is the
single case where -1 leads empirically (rank 1/6, strict) -- but that is the
amplitude reading, and theory does NOT single out -1 at N=8.

## Three crux identities (INDEPENDENTLY re-derived from scratch, all 5 N)
1. Leading RS mean = -1 + #{sqrt(a)} = -1 for EVERY non-residue  -> all NR tie at
   leading order; -1 dominance is NOT a leading-mean effect. [VERIFIED]
2. sum_{chi!=chi0} |chi(a)-1|^2 = 2 phi(N) for every a!=1 -> total weight identical
   across classes; discriminant must be finer than the raw sum. [VERIFIED]
3. Even-character weight of |chi(a)-1|^2 = 0 IFF a=-1; for a=-1 all weight sits on
   ODD characters (larger c_chi, the 2 ln2 = psi(1)-psi(1/2) gap), giving a=-1
   MAXIMAL variance V hence MINIMAL delta. [VERIFIED]
   The finer discriminant is the RS VARIANCE parity-weighting, NOT skewness
   (law symmetric, skew=0) and NOT Aoki-Koyama DRH magnitude (m(a)=0 generically).

## Citations (primary-source verified)
- FM_text.txt (Fiorilli-Martin, Crelle 676, 2013), Thm 1.10, verbatim:
  "For any integer a != -1, we have d(q;-1,1) < d(q;a,1) for all but finitely many
   integers q ... such that both -1 and a are nonsquares (mod q)." [GRH + LI]
- PNR_text.txt (Granville-Martin, Monthly 2006), p.1107-1149: a,b both nonsquares
  => RS limiting distribution symmetric, #{qn+a > qn+b} exactly half the time. [GRH+LI]

## Per-N table
N | -1 | delta_I(N;-1,1) | delta-rank(1=min) | V-rank(1=max ampl) | emp D-rank@1.3e13
7 |  6 | 0.833640        | 1/3 (MIN)         | 1/3 (MAX V)        | 2/3
8 |  7 | 0.998938        | 2/3 (NOT min;a=5) | 2/3 (NOT max;a=5)  | 1/6 (STRICT, units {3,5,7})
11| 10 | 0.700439        | 1/5 (MIN)         | 1/5 (MAX V)        | 3/5
19| 18 | 0.603681        | 1/9 (MIN)         | 1/9 (MAX V)        | 3/9
23| 22 | 0.593680        | 1/11 (MIN)        | 1/11 (MAX V)       | 7/11

delta(N;-1,a)=1/2 EXACTLY for every other NR a, all N (RS symmetry).

## AGREE column logic
- Asymptotic density vs empirical: theory predicts -1 is LEAST-biased (would rank
  near LAST among NR as x->inf in the sign sense). Empirically (finite x) we measure
  signed D which is amplitude-dominated until onset; so empirical rank should match
  neither yet. At x=1.3e13 onset not reached for any N. CONTRADICTION with a naive
  "-1 dominates" premise is clearest where empirical -1 is mid-or-low (N=7,11,19,23).
- N=8 is the lone empirical "-1 leads" case, but theory does NOT predict -1 special
  at N=8 (rank 2 in both delta and V). So N=8 empirical lead is NOT theory-endorsed
  -1 dominance; it is consistent with -1 having large (rank-2) amplitude plus finite-x
  noise, and the dramatic negative columns (a=2,4,6) are NON-UNITS (parsing artifact),
  irrelevant to the AP race among true units {1,3,5,7}.

## Caveats
- ALL theory CONDITIONAL on GRH + LI. Variance closed form needs only GRH. None unconditional.
- c_chi NUMERICAL (validated vs low-zero sums), not a proof.
- Empirical NUMERICAL, single x=1.3e13, two independent sieves agree to the integer.
- Onset figure e^33.4~3e14 carried from brief, not re-derived here.

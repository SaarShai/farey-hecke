# Finite-object / falsification scout — verdict (2026-06-14, wf_00951f06)

Reframe: pipeline's true edge = VERIFIED FINITE OBJECT (counterexample/witness/certificate/exact
value), self-certifying, no collaborator. 7 probes + adversarial vet (11 agents).

## SURVIVOR (vet keep=TRUE, only one): N(18) equiangular lines
- Max # equiangular lines in R^18. SMALLEST open dimension of Haantjes(1948)/Lemmens-Seidel(1973).
- OPEN (vet-verified primary sources, June 2026): 57 <= N(18) <= 59. LB 57 = arXiv:2104.04330 (2023).
- Resolution = self-certifying finite object: WITNESS (explicit Seidel/Gram matrix realizing 58/59
  lines at angle 1/5, checkable by exact PSD+rank) OR LP/Farkas infeasibility certificate (<=58/<=57).
- Findability NOT astronomical (switching-class/polynomial enumeration collapses 2^C(58,2)).
- Significance: classical, well-known (combinatorics / frame theory / coding). sig 7, obj 9, find 7
  (scout) -> vet revised 18/30, keep=TRUE.
- HONEST caveat (vet): not pure push-button. enumerate + LP kills most, leaves a BOUNDED number of
  genuinely-hard residual cases (may need SDP / structural arg, not plain LP).
- Crack plan: (1) oracle = reproduce a settled N(d); (2) build Seidel-matrix + LP-upper-bound +
  Gram-PSD machinery; (3) enumerate switching classes / LP-certify; (4) attack the residual; verify
  any certificate in Lean. PILOT LAUNCHED.

## Secondary (demoted, "pipeline + theory collaborator"): reciprocity-obstruction discovery
- Apollonian local-global DISPROVED 2023 (Haag-Kertzer-Rickards-Stange, Annals; arXiv:2307.02749).
- Cheap chi_2 (Kronecker-symbol) scan over Kontorovich-Nakamura taxonomy + SL2 semigroups FINDS
  candidate obstructed families (embarrassingly parallel, our exact arithmetic + JP dim>1/2 cert).
- VET KILL: certifying each candidate is a genuine obstruction needs a per-case quadratic-form +
  analytic reciprocity proof -> NOT self-certifying push-button. = pipeline-discovers + theory-certifies.
- Two Apollonian types (6,1,1,1),(8,11,1) still OPEN (quartic/octic obstruction unexplored).
- sig 8, obj 9, find 7 (scout) -> vet revised 11, keep=FALSE (certification not push-button).

## Failed the FINDABILITY filter (honest, corrects priors)
- Hadwiger-Nelson chromatic-number-of-plane + ALL SAT targets (Schur6/vdW/Ramsey/ES(7)): find=2,
  astronomical search. (My de-Grey-2018 prior was WRONG on current findability.)
- Fermat-Catalan 11th solution: maximally self-certifying (single tuple) but in-budget region
  (~1e21) likely already searched; significance/findability anti-correlated. keep=FALSE.
- Square-energy EFGW spectral conjecture: attackable families disjoint from the open region. DROP.
- Certified-dimension-decides + spectral-Ramanujan: not finite-object / findability 3. DROP.

## Bottom line
At least ONE genuine target exists: N(18) equiangular lines — significant, classical, genuinely open,
self-certifying resolution, findability in reach (bounded hard residual). This directly answers the
user's challenge. Full data: tasks/wiok2jr18.output.

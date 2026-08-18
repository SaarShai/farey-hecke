# (RATE) promotion plan: M3 and N1–N4

**Date:** 2026-08-18

**Role:** research strategy

**Scope:** promotion plan only; no claim below upgrades the DRAFT (RATE) lemma.

## 0. Status discipline and evidence precedence

- **THEOREM** means a complete proof artifact is present. **CERTIFIED-FINITE**
  means an exhaustive, replayable certificate for a stated finite domain.
  **CONJECTURAL** means the mathematical statement remains unproved, even when
  numerically supported.
- The parent note is still “DRAFT LEMMA + proof skeleton. Not a proved theorem”
  (`LAW_R2_RATE_LEMMA_DRAFT.md:1-8`), and the measurement note is explicitly
  measurement-only (`LAW_RATE_MEASURE.md:1-9`).
- The referee audit's pre-harvest warning not to promote the v27 count
  (`RATE_NOTEGRAPH_REFEREE_AUDIT.md:7-14`) is superseded **only for the N4
  multiplicity subclaim** by the harvested, sorry-free `RateCoreII.lean` proof
  described below. It does not promote M1, N1–N3, the N4 scaling claim, or the
  assembled (RATE) lemma.
- The committed N=40 receipt is real but narrow: the pre-registered `1e-6` gate
  passes on the exact-comparator grid `q in {3,4,6}` with worst relative error
  `1.154e-07` (`LAW_RATE_MEASURE.md:205-210`, `:393-400`). The main `q>6`
  sweep was still computed at N=24, so those rows retain their per-row
  N-doubling status; the N=40 small-q gate is not a certificate for them
  (`LAW_RATE_MEASURE.md:210-217`).
- In particular, `t=7.0665` has N-doubling residuals
  `4.5e-3`–`2.4e-2` and is **NOT CONVERGED** at N=24
  (`LAW_RATE_MEASURE.md:231-241`). The listed q=12–32 rows show the same failure
  (`LAW_RATE_MEASURE.md:248-281`), both q=64 rows are also unconverged
  (`LAW_RATE_MEASURE.md:17-25`), and no `t=7.0665` value may be used in a rate
  fit (`LAW_RATE_MEASURE.md:289-293`). This is a numerical-validation blocker,
  not a counterexample to an analytic (RATE) theorem.

## 1. Promotion ledger

| Item | Status now | Proof-grade endpoint | Primary route | Effort after dependencies |
|---|---|---|---|---|
| M3 | OPEN; single-cell calibration | uniform bound on a frozen `s`-domain | analytic argument + interval certificate | 4–7 researcher-days |
| N1 | CONJECTURAL; matched finite sample | cancellation-stable all-q derivative bound | analytic argument; interval falsification/certification; then Lean | 2–4 weeks |
| N2 | CONJECTURAL globally; finite observation at q=32,48 | CERTIFIED-FINITE result at observed q; global claim absorbed into M1 | exact enumeration + Lean for finite scope; analytic M1 globally | 2–4 days finite; M1-sized globally |
| N3 | CONJECTURAL/OPEN | proved absolute tail majorant; factor-2 shell rule only if separately proved | analytic argument; then Lean | 1–3 weeks |
| N4 | multiplicity **THEOREM**; scaling CONJECTURAL | explicit weighted-sum upper bound | Lean already closes count; analytic argument for scaling | 1–2 weeks after M1 |

Effort estimates are planning estimates, not mathematical claims. “After
dependencies” is essential: the corrected coset-level M1 is still the weakest
link, and without it the matched/escaping split is data rather than proof
(`LAW_R2_RATE_LEMMA_DRAFT.md:405-425`; `RATE_NOTEGRAPH_REFEREE_AUDIT.md:170-180`).

## 2. M3 — `s`-uniformity

### Current status

**OPEN.** The assembled bound is validated only at `s=1.1+1.5i`
(`LAW_R2_RATE_LEMMA_DRAFT.md:314-326`). The draft itself says that `|M(s)|`
and `2|s|` are explicit, but the `T_X` ratio and `C(sigma,T)` calibration are
single-cell (`LAW_R2_RATE_LEMMA_DRAFT.md:430-434`). The advertised
`C(1.1,1.5) <= 2.0` is explicitly numeric-conjectured
(`LAW_R2_RATE_LEMMA_DRAFT.md:294-298`).

### Exact statement to prove

First freeze the domain actually needed downstream. The current numerical band
is `1.1 <= sigma <= 1.25` (`LAW_RATE_MEASURE.md:168-169`); the target-height
tests require a window reaching at least `|t|=7.0665`, whose current large-q
rows are not converged (`LAW_RATE_MEASURE.md:231-241`). Define

```text
K* = {s = sigma + i t : 1.1 <= sigma <= 1.25, |t| <= T*},  T* >= 7.0665.
```

The minimal program statement is:

> **M3(K*) — CONJECTURAL.** There is a fully explicit finite constant `C_K*`,
> independent of `q`, such that for every `q >= 12` and every `s in K*`,
> `|phi_q(s)-phi_infty(s)| <= C_K* q^(1-2 Re(s))`.

The stronger statement of record in the R2 draft is:

> **M3(sigma,T) — CONJECTURAL.** For every `sigma >= 1.1`, finite `T`,
> `q >= 12`, and `|t| <= T`,
> `|phi_q(s)-phi_infty(s)| <= C(sigma,T) q^(1-2 sigma)`, with an explicit
> `C(sigma,T)` independent of `q`.

The first statement should be promoted first. The second must not be claimed
until the summation regime in N4 is proved for the full `sigma` range; the
printed heuristic `sum_{m<q} m^(2-2 sigma) ~ q^(3-2 sigma)`
(`LAW_R2_RATE_LEMMA_DRAFT.md:241-247`) changes at `sigma=3/2`.

### Promotion route

1. **Analytic argument (primary).** Replace every sampled constant by an
   explicit bound on `K*`: bound
   `sqrt(pi) Gamma(s-1/2)/Gamma(s)`, `2|s|`, the matched core, both escaping
   masses, and the proved N3 tail majorant. Preserve the exact candidate split
   at `LAW_R2_RATE_LEMMA_DRAFT.md:257-286`; do not calibrate `C_K*` from D-data.
2. **Interval-arithmetic certificate (supporting).** Certify the supremum of
   the explicit special-function factors over the whole compact rectangle,
   with subdivision and outward rounding. This may also provide a regression
   grid for the analytic constants. Point samples, including a higher-N
   `t=7.0665` rerun, are falsification evidence only.
3. **Lean dispatch (last).** Dispatch the compact-set inequalities and the
   final algebraic assembly only after M1/N1/N3/N4 supply explicit lemmas. Lean
   is not the discovery route for the infinite-sum estimates.

### Dependencies and effort

- Theorem dependencies: corrected coset-level M1; the N1 derivative bound on
  the matched domain; an N3 absolute tail majorant; the re-scoped N4 weighted
  sum; explicit escaping-mass bounds.
- Certificate dependency: a higher-N or different certified evaluator at
  `t=7.0665` for a meaningful numerical falsification pass. The N=40 small-q
  receipt does not certify the large-q rows.
- R3 transport is downstream of the raw RATE estimate, not part of M3 itself;
  its open multiplier merely determines how small `C_K* q^(1-2sigma)` must be
  (`LAW_R2_RATE_LEMMA_DRAFT.md:339-341`).
- **Estimate:** 4–7 researcher-days once M1/N1/N3/N4 are proved; add roughly
  1–2 weeks for proof-assistant formalization. End-to-end calendar time is
  dominated by those upstream gaps.

## 3. N1 — universal derivative envelope (C1)

### Current status

**CONJECTURAL.** The statement is

```text
sup_{lambda in [lambda_q,2]} |c'_w(lambda)|
  <= (11/20) k_w^2 |c_w(lambda_q)|.
```

It is supported by a measured maximum `0.518` over 1,138 **matched** cosets at
`q in {12,16,24,32,48}`, `X=50`, depth at most 12; 246 escaping cosets were not
tested (`LAW_R2_RATE_LEMMA_DRAFT.md:71-88`, `:211-229`, `:355-365`). The
candidate positivized-continuant comparison loses control under heavy
cancellation, so the stated universal induction is not presently available
(`LAW_R2_RATE_LEMMA_DRAFT.md:361-365`).

### Exact statement to prove

Use a falsification-first two-tier target:

> **N1-strong — CONJECTURAL.** For every `q >= 12` and every reduced word `w`
> with `c_w(lambda_q) != 0`, C1 holds with the constant `11/20`.

> **N1-RATE — CONJECTURAL.** If N1-strong is false, then for every `q >= 12`
> and every canonical representative of an M1-matched double coset, C1 holds
> with one explicit constant `A < infinity`, preferably `A=11/20`.

N1-RATE is the minimum theorem used by the matched-drift core
(`LAW_R2_RATE_LEMMA_DRAFT.md:268-274`). Do not silently call it “uniform over
words”; its domain must be the proved coset-normal-form domain.

### Promotion route

1. **Interval arithmetic (falsification gate).** Exhaust all current words and
   extend deliberately into escaping/heavy-cancellation families and greater
   depth. Certify each polynomial/rational derivative supremum on
   `[lambda_q,2]` with outward-rounded intervals. A single counterexample
   retires N1-strong or the `11/20` constant.
2. **Analytic argument (primary proof).** Find a cancellation-stable invariant
   tied to the corrected coset normal form, not only the positivized
   continuant. Prove a matrix/continuant induction controlling both `c'_w` and
   the lower bound for `|c_w(lambda_q)|` in the matched elliptic region.
3. **Lean dispatch.** Formalize the invariant and induction once written.
   Fixed-word interval certificates and bounded-depth instances are useful
   regression theorems but do not promote the all-q statement.

### Dependencies and effort

- Mathematical dependency for N1-strong: none on M1, but it needs a precise
  reduced-word domain and a cancellation-resistant invariant.
- RATE-use dependency: M1 must identify canonical matched cosets and localize
  the complement; otherwise the restriction in N1-RATE is not theorem-defined.
- **Estimate:** 2–4 days for an expanded certified falsification sweep;
  2–4 weeks for the universal analytic invariant and proof; 3–5 additional
  days for Lean after the lemma is stable. Risk is high because the current
  candidate invariant already fails on cancellation.

## 4. N2 — onto matching in the theta window

### Current status

**FINITE NUMERICAL OBSERVATION; GLOBAL CLAIM CONJECTURAL.** Matching is a
greedy canonicalized word-specialization procedure, not yet a proved coset map
(`LAW_R2_RATE_LEMMA_DRAFT.md:187-194`). At `X=50`, depth at most 12, the theta
window has 237 cosets; the measured unmatched counts are 33, 13, 1, 0, 0 for
`q=12,16,24,32,48` respectively (`LAW_R2_RATE_LEMMA_DRAFT.md:196-205`). Thus
the data prove neither “all `q>=32`” nor any unbounded-window statement.

### Exact statement to prove

Split the promotion rather than overstate the sample:

> **N2-finite — CONJECTURAL until certified.** For each
> `q in {32,48}`, every theta double coset in the exactly specified `X=50`
> window has a preimage among the exactly enumerated q-cosets of depth at most
> 12, under the canonical `(c,d mod c)` map.

> **N2-global — CONJECTURAL and not an independent gap.** For every `q>=32`,
> the corrected coset-level specialization is surjective onto all theta cosets
> below the proved cutoff `c*(q)`, and the complement is confined to the
> near-relation region.

N2-global is precisely the surjectivity/localization part of corrected M1
(`LAW_R2_RATE_LEMMA_DRAFT.md:405-425`). After N2-finite is certified, remove N2
from the global gap ledger and track N2-global under M1; a finite window cannot
promote an all-q theorem.

### Promotion route

1. **Exact enumeration / interval certificate.** Freeze the group
   normalization, canonical coset invariant, cutoff convention, depth bound,
   algebraic comparison precision, and enumerator version. Emit a bijection
   receipt with complete source and target lists, not only “unmatched=0”.
2. **Lean dispatch.** Import the finite lists or a compact checked certificate
   and prove coverage for q=32 and q=48. The draft already classifies fixed
   `(q,X)` checks as formalizable (`LAW_R2_RATE_LEMMA_DRAFT.md:366-368`).
3. **Analytic argument for global scope.** Prove M1's well-definedness,
   injectivity, surjectivity, and complement localization. No denser numerical
   grid can replace this step.

### Dependencies and effort

- N2-finite: exact canonicalization; completeness of both enumerations; the
  width-one/width-two conjugation dictionary; a fixed cutoff/depth contract.
  The proved N4 theta count supplies an independent target-cardinality check.
- N2-global: corrected M1 in full.
- **Estimate:** 2–4 days for the two finite certificates plus Lean checking.
  Global effort is M1-sized—multiple weeks—and should not be charged to a
  separate numeric N2 lane.

## 5. N3 — beyond-window tail

### Current status

**OPEN / CONJECTURAL.** The literal rule

```text
T_X(q,sigma) = 2 Delta_X^outer(q,s)
```

comes from measured outer-half/total ratios `0.13`–`0.22`, followed by a
geometric-series extrapolation (`LAW_R2_RATE_LEMMA_DRAFT.md:280-292`). That is
not a proof of dyadic contraction. The M2 note supplies the candidate raw-tail
formula

```text
sum_{|c_w|>X} |c_w|^(-2 sigma)
  <= X^(2-2 sigma) [1/(sigma-1) + 2/X],
```

but explicitly keeps M2 and N3 open pending corrected M2.L, G1, and G2
(`LAW_M2_TAIL_MAJORANT_DRAFT.md:1-10`, `:61-74`, `:90-110`). Its arithmetic is
correct only conditional on those hypotheses
(`RATE_NOTEGRAPH_REFEREE_AUDIT.md:172-180`).

### Exact statement to prove

There are two distinct statements; do not conflate them:

> **N3-shell — CONJECTURAL.** For the precisely defined nonnegative matched
> drift summand `delta_w(s)`, every `q>=12`, every `s` in the M3 domain, and an
> explicit admissible `X`,
> `sum_{min(c_q,c_theta)>X} delta_w(s)
>  <= 2 sum_{X/2<min(c_q,c_theta)<=X} delta_w(s)`.

> **N3-absolute — CONJECTURAL; preferred endpoint.** Prove explicit,
> q-uniform finite- and theta-side raw-tail majorants, then combine them with
> M1, N1, and N4-scale to obtain a closed-form `B(q,sigma,X)` satisfying
> `Delta_{>X}(q,s) <= B(q,sigma,X)` and permitting an explicit choice `X(q)`
> in the final RATE assembly.

N3-absolute is sufficient for RATE and is safer than trying to preserve the
empirical factor 2. Retain `T_X=2 Delta_X^outer` only if N3-shell itself is
proved; otherwise replace it by `B`.

### Promotion route

1. **Analytic argument (primary).** Close corrected M2.L in the width-one
   model, G1 lattice discreteness, and G2 integer-grid domination; prove the
   raw-tail inequality on both finite-q and theta sides. The strict-tail
   boundary matters: at `X=1`, the displayed formula omits `|c|=1`; under the
   note's ceiling the full-series value is at most 14, not 12
   (`LAW_M2_TAIL_MAJORANT_DRAFT.md:99-110`).
2. Lift raw mass to drift mass using the proved N1 derivative envelope and
   M1's matched/escaping localization. Use the N4 multiplicity theorem on the
   theta side; its constant is no longer an open N3 dependency.
3. **Interval arithmetic (audit only).** Certify finite shell ratios over a
   broad grid to falsify a proposed analytic contraction constant. No finite
   ratio table proves the infinite tail.
4. **Lean dispatch.** Formalize the integral comparison and algebra after G1,
   G2, and the drift majorant are written as explicit lemmas.

### Dependencies and effort

- Corrected M2.L; M2.G1; M2.G2; normalization dictionary.
- Corrected M1; N1-RATE; N4-scale. The N4 multiplicity count is discharged.
- **Estimate:** 1–3 weeks for the analytic chain after the structural inputs
  are available; 3–5 additional days for certificate generation and Lean
  assembly. Risk is high because M2.T controls raw mass, while N3 needs the
  weighted drift tail.

## 6. N4 — re-scoped after `theta_coset_count`

### Current status

N4 originally bundled two claims: theta multiplicity and the
`q^(3-2 sigma)` scaling of the `k^2`-weighted matched sum
(`LAW_R2_RATE_LEMMA_DRAFT.md:373-376`). They now have different statuses.

**N4-count: THEOREM; discharged.** The harvested theorem states

```text
#{d < 2c : gcd(c,d)=1 and c+d is odd} = phi(2c).
```

The statement is at
`projects/aristotle_dispatch_v27/result/aristotle_dispatch_v27_aristotle/RateCoreII.lean:159-176`;
the proof splits on the parity of `c`, identifies the even-c case with residues
coprime to `2c`, and gives the odd-c bijection `d <-> d/2`
(`projects/aristotle_dispatch_v27/result/aristotle_dispatch_v27_aristotle/RateCoreII.lean:177-214`).
The harvested summary records all six sorries
removed and a clean build
(`projects/aristotle_dispatch_v27/result/aristotle_dispatch_v27_aristotle/ARISTOTLE_SUMMARY.md:1-2`),
and describes this proof specifically
(`projects/aristotle_dispatch_v27/result/aristotle_dispatch_v27_aristotle/ARISTOTLE_SUMMARY.md:14-16`).
This planning pass source-checked the complete proof body; the clean-build line
is the harvested receipt, not a fresh independent rebuild. Therefore
the multiplicity constant must not remain on the open N4 ledger. Applying the
count across conjugated group models is normalization bookkeeping under M2/M1,
not a reopening of the combinatorial theorem.

**N4-scale: CONJECTURAL; this is the re-scoped N4.** The printed draft says
the scaling still needs M1 (`LAW_R2_RATE_LEMMA_DRAFT.md:373-376`), and the
referee audit likewise says the exponent does not follow without the corrected
coset normal form (`RATE_NOTEGRAPH_REFEREE_AUDIT.md:170-180`).

### Exact statement to prove

On the current RATE band `1.1 <= sigma <= 1.25`, let `M_q` be the matched
coset set furnished by corrected M1 and let `k(x)` be the depth of its canonical
representative. Prove:

> **N4-scale — CONJECTURAL.** There is an explicit `K(sigma)`, independent of
> `q`, such that for all `q>=12`,
> `W_q(sigma) := sum_{x in M_q} k(x)^2 |c_q(x)|^(-2 sigma)
>  <= K(sigma) q^(3-2 sigma)`.

If the matched-core comparison uses
`(c_q/min(c_q,c_theta))^(2 sigma+1)`, prove the same bound with that factor
included; it may not be hidden in an ellipsis. This is the upper bound RATE
needs. A two-sided asymptotic or sharp constant is unnecessary.

For any extension beyond the current band, prove the elementary summation
regimes rather than repeating one exponent for all `sigma`:

```text
sum_{m<q} m^(2-2 sigma) =
  O(q^(3-2 sigma))  for 1 < sigma < 3/2,
  O(log q)          for sigma = 3/2,
  O(1)              for sigma > 3/2.
```

Until formalized in the actual coset sum, these RATE applications are
**CONJECTURAL**. They show why the draft's half-plane-wide shape claim should
not be promoted from the `sigma=1.1,1.25` evidence alone.

### Promotion route

1. **Lean dispatch: complete for N4-count.** No new multiplicity dispatch is
   needed unless the statement itself changes.
2. **Analytic argument (primary for N4-scale).** Use M1 to parameterize matched
   cosets by canonical normal forms, prove the depth cutoff/localization, group
   by theta denominator, insert the proved `phi(2c)` count, and apply explicit
   partial-summation/integral bounds in the correct `sigma` regime.
3. **Interval arithmetic (supporting).** Compare the proved upper bound with
   finite q windows and search for missing comparison factors. This is a
   falsification check, not the promotion artifact.
4. **Lean dispatch (final).** Formalize the finite sum/integral comparison once
   M1 supplies the combinatorial indexing theorem.

### Dependencies and effort

- The multiplicity theorem has no remaining proof dependency.
- N4-scale depends critically on corrected M1's well-definedness,
  injectivity/surjectivity, cutoff, and complement localization. It also needs
  a canonical depth function and an explicit comparison between `c_q` and its
  theta specialization.
- **Estimate:** 1–2 weeks after M1 is available; 3–5 additional days for Lean
  formalization. Before M1, only finite diagnostic work is meaningful.

## 7. Recommended execution order and promotion gates

1. **Freeze definitions:** `K*`, the exact matched-domain invariant, cutoff
   `c*(q)`, depth convention, and finite enumerator contract.
2. **Run falsification lanes:** expanded interval N1 sweep; exact N2-finite
   certificates; higher-N `t=7.0665` evaluator calibration. None changes a
   theorem status by itself.
3. **Close structural inputs:** corrected M1 and M2.G1/G2. These are the gates
   that turn N1/N3/N4 analytic formulas into statements about the actual coset
   series.
4. **Promote N1-RATE and N4-scale:** explicit constants, correct `sigma`
   regime, no hidden comparison factor.
5. **Promote N3-absolute:** replace the factor-2 empirical tail unless the
   dyadic shell contraction is separately proved.
6. **Promote M3 last:** assemble the proved pieces uniformly on `K*`, certify
   special-function suprema by interval arithmetic, and only then dispatch the
   final algebra to Lean.

The proof-status exit criterion is literal: M3, N1, N2-global, N3, and
N4-scale remain **CONJECTURAL** until their stated universal quantifiers are
proved. N2-finite may become **CERTIFIED-FINITE** without changing M1. N4-count
is already **THEOREM** and is removed from the open-gap count.

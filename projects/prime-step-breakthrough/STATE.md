# Prime-Step Breakthrough State

Date: 2026-07-15

## Goal

Develop and validate a new mathematical result from prime-denominator Farey
insertions and per-step discrepancy, then build and live-verify a practical
application whose advantage depends on that result.

## Current gate

The original one-dimensional implementation remains green.  The
multidimensional operational extension now passes its proof, exact-verifier,
million-scale, interface, security, blast-radius, cold-review, Sol-Ultra, and
live-browser gates and is ready for the scoped commit.  External mathematical
priority remains subject to professional literature review.

## Promoted mathematical results

1. **Farey shear.**  For the old interior fractions before a prime step,

   \[
   \frac1{p-1}\le D^*\{(x,\{px\})\}
   =O_\varepsilon(p^{-1+\varepsilon}).
   \]

2. **Triangular prime-step law.**  The shift
   \(\delta_p(x)=x-\{px\}\) converges to density \(1-|t|\); odd moments vanish
   exactly and the former shift-squared conjecture has leading term
   \(p^2/(2\pi^2)\).

3. **Primitive-layer kernel.**  Complete reduced-residue denominator layers
   have an exact Gram kernel and sharp one-dimensional \(H^1\) worst-case
   integration certificate.  The pair-multiplicative object is \(12K\), not
   \(K\).

4. **Prime energy driver.**  The exact marginal layer energy is controlled by
   \((p-1)(2-A(p-1))/(6p)\); the first exact negative prime is 8501.

5. **García conjecture.**  Classical finite-population moments reduce to the
   sharp universal fourth-moment bound

   \[
   \mathbb E S_i^4\le\frac13\left(\sum_j\Delta_j^2\right)^2.
   \]
   Interpolation and the prefix variance prove both qualitative halves of
   García's Conjecture 1:

   \[
   \frac9{160}\sigma_gN^{3/2}
   \le\overline r_g
   \le\frac1{\sqrt6}\sigma_gN^{3/2}.
   \]
   The constants are rigorous but do not reach García's provisional values.

## Application

`GapPermutation Certificate` computes, in \(O(N)\) arithmetic operations:

- supplied-order absolute, quadratic, and continuous \(L^2\) discrepancy;
- exact permutation-average quadratic and continuous-\(L^2\) quantities;
- rigorous two-sided mean-\(L^1\) bounds; and
- exact/logarithmic distinct-order counts without materializing permutations.

The Python API, CLI, JSON HTTP API, and browser UI all implement the same
contract.  A million-gap case completes without permutation enumeration.
`CoprimeBatch Designer` remains a deliberately narrower secondary tool; its
losses to unrestricted midpoint and admissible broader grids remain visible.

## Multidimensional operational extension

The frozen centered-vector contract contains rational one-dimensional gaps and
one-hot category counts as exact special cases.  Its implemented paths are:

- release-aware EDF for unconstrained categorical inventories, with
  `O(N log C)` time, `O(C)` working memory, and strict factor below three;
- an exact nearest-integer mechanical word for binary inventories;
- a two-pass exact small rational-vector oracle; and
- a packed deterministic constrained categorical scheduler for fixed blocks,
  exact end pins, and sparse precedence, carrying an input-specific
  `L <= OPT_B <= U` certificate against fixed within-category queue
  interleavings.

The constrained scheduling core is `O((N+K) log(C+K))`; exact released metrics
make the complete certificate `O(NC + (N+K) log(C+K))`.  A closed interval
proves primary `B` only, never secondary `Q`.  Shared interfaces cap `C`, `N*C`,
constraint references, and block width before construction and expose only a
loopback research server.

Three compact synthetic presets are registered: a 4,096-item rendering
joint-cell benchmark-ready demonstration, a 65,536-scenario finance
demonstration, and a 512-job pre-randomized laboratory inventory
demonstration.  None is a domain integration.  The laboratory path never
assigns treatments.

## Review and falsification history

- Historical sign routes were excluded after counterexamples at 92173, 237733,
  and 243799.
- The operational Sol-Ultra route was `gpt-5.6-sol` with xhigh reasoning; the
  literal `gpt-5.6-sol-ultra` identifier was unavailable.
- Sol caught the false multiplicativity wording for \(K\), forced stronger
  application baselines, and derived the improved \(9/160\) constant.
- A cold independent verifier re-derived the endpoint quadratics, checked
  126,399 rational cases, all permutations through \(N=8\), and the sharp
  equality witness at \(N=4\).
- Prior-art review demoted the variance, fourth-moment, and continuous-
  \(L^2\) ingredients to classical machinery.  Novelty is claimed only for the
  García-specific deduction and synthesis.
- Live browser use exposed JavaScript rounding of huge exact numerators.  The
  API now adds a canonical `fraction` string while retaining legacy fields;
  high-bit regression tests cover the fix.
- Visual review exposed unbounded result panes; the final UI uses scrollable
  32-rem results with long-fraction wrapping.

## Fresh verification

```text
PYTHONDONTWRITEBYTECODE=1 python3 projects/prime-step-breakthrough/verify_all.py
exit 0
60 unit tests passed
7 live HTTP tests passed
13/13 benchmark gates passed
artifact, cache, and mutation-boundary gates passed
```

The in-app browser gate separately passed keyboard input, clicks, supplied and
Farey gap modes, all four panels, exact high-bit rendering, malformed-input
display/recovery, and CLI/API/browser parity.  See
`artifacts/BROWSER_VERIFICATION.md`.

The operational extension separately passed:

```text
PYTHONDONTWRITEBYTECODE=1 python3 projects/prime-step-breakthrough/verify_operational.py
exit 0
static and browser-JavaScript gates passed
operational unit/oracle gate passed
unconstrained 1,000,000-item gate passed
constrained 1,000,000-item gate passed
original verify_all regression passed
source- and cache-mutation gates passed
```

The final constrained fixture includes a repeated-category block, all four
constraint classes, a hard 30-second worker timeout, and a 128-MiB ceiling.  It
reproduced digest
`3194a7661d0d90f6115bba41cfed1c506fd8f9442c0f54c0a8069ff90662c675`
in 4.135954 seconds at 46,546,944 bytes RSS.  The final independent cold review
returned **ACCEPT — no remaining blockers**.  Updated click/keyboard/error-
recovery evidence is in `artifacts/BROWSER_VERIFICATION_OPERATIONAL.md`.

## Remaining boundary

- A bounded search is not an exhaustive novelty proof; MathSciNet/zbMATH and
  specialist citation-graph review remain before publication.
- T1--T4 are proof-qualified project results and should receive specialist
  analytic-number-theory review before external priority claims.
- No email, preprint, push, or publication has been sent by this workflow.
- The operational extension has no million-scale arbitrary-vector constructor,
  no general-vector constant factor, no production domain integration, and no
  observed time, money, effort, error, accuracy, adoption, causal, clinical, or
  final-all-items benefit.

## Next action

Commit the scoped operational release.  Send the concise follow-up draft to
Rogelio only after user approval.

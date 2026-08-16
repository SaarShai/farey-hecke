# V23 dispatch — skipped obligations

Source: `research_notes/rh_goals_2026-08-14/lane_g/LAW_ANCHOR_T1_THETA.md` §7.2.
Task named T-1..T-9 as the Aristotle-able candidate set, with T-4 flagged
highest value. **T-1, T-2, T-3, T-4, T-6, T-7, T-9 are dispatched** in
`ThetaGroupAnchor.lean`. Two are skipped, per the task's own instruction to
skip rather than weaken:

## T-5 — skipped (checked for a prior dispatch; none found)

T-5 (§3.1) is "the Euler-product restriction lemma, verbatim M1F A-4 at `p=2`":
`Σ_{2|c} φ_E(c) c^{-2s} = (ζ(2s−1)/ζ(2s))/(4^s−1)` and the odd-modulus analogue.
The task instruction was: reuse M1F A-4 if it has already been dispatched via a
v-series project; otherwise note either way.

Checked: `grep -rl "phi_E\|EulerProduct\|Euler.*product\|A_4\|zeta_2s"
projects/aristotle_dispatch_v*/*.lean` — **no match** across the full v6..v22
dispatch tree. `research_notes/rh_goals_2026-08-14/EXECUTION_LOG.md` mentions
M1F's "7 Aristotle-able items extracted (A-1..A-7; highest-value is A-4, the
Euler-product restriction lemma)" as a *scoping* note (M1F Eisenstein
derivation, 2026-08-15) but records no evidence a v-series project was ever
submitted for the M1F obligations themselves — only for M1D (v22, the
intertwiner obligations) and now this T1 note.

**Verdict: A-4 was never dispatched. It is skipped here anyway** (not
retroactively picked up), because it is a genuine formal Dirichlet-series /
Euler-product identity over `Re s > 1` — an infinite sum, not a finite
statement — and dispatching it correctly is a distinct, non-trivial unit of
work outside this task's named T-1..T-9 list. `T-4` in this dispatch already
carries the finite core of the *same* content (the per-modulus counting
bijection that the Dirichlet series sums over), per the task's own fallback
instruction ("state the per-modulus counting bijection as the finite core and
record the reduction in a comment") — see the doc-comment above `T-4` in
`ThetaGroupAnchor.lean`. A future v-series project can dispatch T-5/M1F-A-4
directly as a Dirichlet-series identity if that is wanted.

## T-8 — skipped (not finitely stateable in this Mathlib version)

T-8 (§4.2) is "the order of `det Φ_θ` at `s = ρ/2` is `−2m(ρ)`, given `T-7` and
the divisor of `Λ`". This is bookkeeping over the divisor of `Λ(2s) =
π^{-s}Γ(s)ζ(2s)` — i.e. it needs, as an *input*, the full zero set of the
nontrivial zeros of `ζ` **with multiplicities** (`m(ρ)`), plus meromorphic-
order arithmetic (sum/difference of orders of zeros and poles of a product of
meromorphic functions) at those points.

This is not a finite statement: it quantifies over the infinite (and, absent
RH, not finitely describable) set of nontrivial zeta zeros, each carrying an
a-priori-unknown multiplicity `m(ρ)`. Mathlib (as of the `v4.28.0` toolchain
pinned in `lean-toolchain`) has `Complex.RiemannZeta` machinery but no
developed API for the zero-multiplicity function `m(ρ)` or for order-of-pole
arithmetic on `Λ` at those unnamed points, so there is no way to state the
claim as a closed finite proposition without either (a) taking `m` as an
uninterpreted hypothesis-function (which drains the statement of the content
the note actually wants — that no cancellation occurs, which is precisely a
claim *about* how `m` and the divisors of `E`, `Λ(2s−1)`, `Γ(s−1/2)/Γ(s)`
interact) or (b) importing meromorphic-function divisor calculus that is not
in scope for a finite-algebra dispatch.

`T-7` (the divisor of `E`, an elementary complex-exponential fact) **is**
dispatched, since it is exactly the finite half of T-8's argument. The
non-cancellation conclusion itself (§4.2 channels 1-4 of the source note)
remains a `GAP`/frontier item, consistent with the source note's own labelling
of `C14`/`C17` as non-Aristotle-able and its statement that "Not
Aristotle-able: ... anything in §6.2 (numerics)" — T-8 is adjacent to the same
boundary between finite algebra and genuine analytic-number-theory content.

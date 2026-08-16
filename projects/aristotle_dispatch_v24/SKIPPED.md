# V24 dispatch — skipped obligations

Source: `research_notes/rh_goals_2026-08-14/lane_g/LAW_U2B_CLOSURE.md` §6.
The numbered Aristotle-able candidate set is A1..A6, with A1 flagged
highest-value ("the single highest-value target: everything else in this note
is downstream of it"). **A1, A2, A3, A6 are dispatched** in
`HeckeSystole.lean`. Two are skipped, per the note's own scoping ("§6" flags
A5 explicitly as "not purely algebraic"):

## A5 — skipped (analytic, not finite algebra)

A5 (§6) is "the monotonicity lemma (Theorem U2b-B's engine)":

```lean
theorem tcot_strictAntiOn : StrictAntiOn (fun t => t * Real.cot t) (Set.Ioo 0 Real.pi)
theorem u_monotone (j : ℕ) (hj : 1 ≤ j) :
    MonotoneOn (fun lam => u lam j) (Set.Icc (2 * Real.cos (Real.pi / j)) 2)
```

The note itself flags this: "**Not purely algebraic** — `tcot_strictAntiOn`
needs `sin 2t < 2t`." The proof (`LAW_U2B_CLOSURE.md` §3.1, Lemma U2b-2) is a
derivative computation, `g'(t) = (sin t cos t - t)/sin² t = (½ sin 2t -
t)/sin² t < 0` for `t ∈ (0,π)`, i.e. a real-analysis argument over an
uncountable domain, not a finite/decidable statement. Out of scope for this
finite-algebra dispatch per the brief's own instruction to skip A4/A5.

## A4 — skipped (depends on A5)

A4 (§6) is "`W_q` is decreasing in `q` (closes `GAP` U2b.15)":

```lean
theorem W_antitone (e_h e_l : ℝ) (he : 2 < e_h) (hl : 2 < e_l) :
    ∀ q ≥ 5, W (q+1) e_h e_l ≤ W q e_h e_l
```

This is explicitly "low, given A5" in the source note — its proof leans on
`u_a(lam_{q+1}) ≥ u_a(lam_q)`, i.e. exactly the A5 monotonicity fact, applied
inside a sum over an infinite family of levels `q`. Since A5 is itself
analytic (see above) and not dispatched here, A4 inherits the same gap and is
skipped alongside it, consistent with the brief's instruction "A5/A4 are
analytic — SKIP them."

Both A4 and A5 remain live `GAP` items in `LAW_U2B_CLOSURE.md` (§5.1
"cheap to close" for the U2b.15 consequence of A4/A5 together) and are
candidates for a future dispatch that targets real-analysis lemmas
specifically (derivative sign arguments, `StrictAntiOn` over `Set.Ioo`), which
is a different unit of work than this finite-algebra pass.

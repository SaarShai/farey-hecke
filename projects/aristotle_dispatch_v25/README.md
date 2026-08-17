# V25 — U3 transport: the divisor-bookkeeping core

**Target.** Obligation **U3** of
`research_notes/rh_goals_2026-08-14/lane_g/LAW_T2_DETERMINANT.md` §5.2
(= C14 of `LAW_ANCHOR_T1_THETA.md` = G6/N2 of `M1F_EISENSTEIN_DERIVATION.md`),
analysed in `lane_g/LAW_U3_TRANSPORT.md` and named recommended-lane #2 in
`lane_g/LAW_SH_EFFECTIVIZATION_SKELETON.md` §7 ("textbook-shaped").

**Ask.** Prove the 13 `sorry`s in `U3Transport.lean`. Every statement is
hypothesis-complete: the analytic inputs (Selberg functional equation, `Z_Γ`
zero-free off the critical line in `Re s > 1/2`, `κ`'s non-`φ` factors being
units off `ℝ`, `Λ`'s divisor, `E`'s divisor) are hypotheses, not obligations.
What is asked is exactly the **order arithmetic**:

```
ord_{s0} Z(1 - .)  =  ord_{s0} kappa  +  ord_{s0} Z
ord_{s0} Z(1 - .)  =  ord_{1-s0} Z    =  0        (hypothesis)
ord_{s0} kappa     =  ord_{s0} phi    =  -m       (unit factor + hypothesis)
==>                   ord_{s0} Z      =  +m
```

plus the `Γ_θ` divisor computation `det Φ_θ = g² E`, `g = Λ(2s-1)/Λ(2s)`, at the
anchor `s₀ = ρ/2` (order `-2m` pole) and at the conjugate point `(1+ρ)/2`
(order `+2m` zero), and the arithmetic identity `1 - conj(ρ/2) = (1+ρ)/2` when
`Re ρ = 1/2`.

**Mathlib vocabulary this is written against** (`v4.28.0`,
`Mathlib/Analysis/Meromorphic/Order.lean`):
`meromorphicOrderAt`, `meromorphicOrderAt_mul`, `meromorphicOrderAt_pow`,
`meromorphicOrderAt_inv`, `meromorphicOrderAt_congr`,
`meromorphicOrderAt_mul_of_ne_zero`, `meromorphicOrderAt_comp_of_deriv_ne_zero`,
`AnalyticAt.meromorphicOrderAt_eq`, `meromorphicOrderAt_eq_top_iff`.
Orders live in `WithTop ℤ`; the finiteness hypotheses (`≠ ⊤`) are present
wherever cancellation is needed.

**Contents.**

| file | what |
|---|---|
| `U3Transport.lean` | 13 theorem statements, all `sorry`-free in the statement, `sorry` in the proof |
| `SKIPPED.md` | S1–S7: everything deliberately left analytic / citation-level |
| `DISPATCH_NOTE.md` | what was sent, what remains analytic, ledger line |
| `PROJECT_ID.txt`, `TASK_ID.txt` | Aristotle identifiers |

**Local check before dispatch.** `U3Transport.lean` elaborates against Mathlib
`v4.28.0` with exactly 13 `declaration uses 'sorry'` warnings and no errors
(run in `projects/aristotle_dispatch_v22`, same toolchain and pinned Mathlib rev).

**Novelty.** None claimed. The transport theorem is 1980s classical
(Hejhal / Venkov); see `LAW_U3_TRANSPORT.md` §6 V4. This dispatch is a
machine-checked skeleton of the bookkeeping, not a new theorem.

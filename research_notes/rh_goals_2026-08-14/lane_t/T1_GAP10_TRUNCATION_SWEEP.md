# GAP-10 — sensitivity of T1 to the (M3) amplitude-truncation quantile q

2026-08-26. Answers `plans/wayfinder` ticket item GAP-10 (T1_CRAMER_RAO_DRAFT.md
ledger, §1.4 clause (M3), §7.2). Script: `lane_t/t1_gap10_sweep.py` (imports,
does not rederive, `lane_t/t1_verify.py`). Receipt:
`lane_t/T1_GAP10_SWEEP_RECEIPT.json`. Not committed.

## 0. What (M3) says, and what the reused machinery actually computes

(M3): "a_γ = |M_W(½+iγ)| · r_γ with r_γ = 1/|ζ′(½+iγ)| drawn from the
empirical lane_a law, **truncated at a quantile q**" (§1.4). §7.2 argues this
truncation is moot for T1's leading constant because the leading constant
only ever uses S_ε(γ_j)^{1/2}/a_{γ_j} = (log(γ_j/2π))^{1/2} — the *density*,
not the amplitude law — after Prop. 4.4's cancellation.

Inspecting `t1_verify.py` (the machinery this task is told to reuse) shows
the mootness argument is realised even more directly than §7.2 states it:
every place the script computes S_ε, the factor-24 FIM, or the Lindeberg
ratio, it sets **r_γ ≡ 1** (its docstring: "the convention that reproduces
the v2 number S_ε(γ_d) = 7.23e−35"). There is no stochastic amplitude *law*
in the reused machinery at all, hence nothing for a quantile q to truncate.
This is the "inapplicable as stated" case the task brief anticipates for
items (a) and (b), and it is reported here rather than silently patched
around: **(a) and (b) are exactly q-invariant by construction**, not merely
empirically insensitive.

(c) is different: the max-bounded-summand constant is a statement about a
single *realised* interferer's amplitude, which is exactly what r_γ's tail
controls, and it is not folded into the mean-field S_ε machinery. No
committed empirical quantile function for r_γ exists in this repo (lane_a
has only the first-moment J_{−1} report). The **nearest well-defined
analogue**, labelled as an analogue throughout: model r_γ as
Pareto(α=2, x_m=1). α=2 is not a free choice — it is the boundary value
implied directly by the draft's own stated fact (§1.3, §7.2) that
E[r] = J_{−1} is finite while E[r²] = J_{−2} diverges (Gonek–Hejhal): any
α ≤ 2 gives divergent second moment, any α > 1 gives finite first moment, and
α = 2 is the unique value on both boundaries at once. Quantile function
r_q = (1−q)^{−1/2}.

## 1. Sweep table

Window (W′) Riesz k=1, Γ=50, Ω=2Γ=100, T=log(3·10⁷)=17.2167, tone γ_d=49.7738.

| q | (a) [I⁻¹]_ωω ÷ local-24 | (a) λ_max(I_N⁻¹I_R) | (b) Λ(50) | (c) r_q | (c) max 2a_γ | (c) max 2a_γ / σ |
|---|---|---|---|---|---|---|
| 0.90  | 0.99432 | 0.08575 | 0.15652 | 3.162  | 2.529e−3 | 1.769 |
| 0.95  | 0.99432 | 0.08575 | 0.15652 | 4.472  | 3.576e−3 | 2.502 |
| 0.99  | 0.99432 | 0.08575 | 0.15652 | 10.00  | 7.996e−3 | 5.595 |
| 0.995 | 0.99432 | 0.08575 | 0.15652 | 14.14  | 1.131e−2 | 7.913 |
| 0.999 | 0.99432 | 0.08575 | 0.15652 | 31.62  | 2.529e−2 | 17.69 |
| 1.0 (no truncation) | 0.99432 | 0.08575 | 0.15652 | ∞ | ∞ | ∞ |

Columns (a) and (b) are literally the same six digits at every q — not
"stable to <1%" but bit-identical, because q never enters those two
formulas in the reused machinery. Column (c)'s ratio grows without bound as
q → 1 (Pareto has no finite mean-of-max at the untruncated limit for a
single worst-case draw, consistent with the divergent-second-moment
diagnosis the draft itself makes).

σ used in (c) is the mean-field Lindeberg scale
σ = √(2a_Γ²/Λ(50)) = 1.429e−3, the same σ that (b)'s Λ(50) is built from —
i.e. (c) mixes a *realised worst-case amplitude* (which does depend on
truncation) against a *mean-field* normalising scale (which does not). That
mismatch is exactly the content of GAP-17's open Berry–Esseen obligation:
Λ(Γ) → 0 controls the mean-field Lindeberg condition, but the finite-Γ CLT
rate needs the actual tail of individual summands, i.e. needs a q.

## 2. Reading — is the §7.2 mootness claim borne out?

**Yes, and it is stronger than claimed.** §7.2's assertion is that the
leading CR constant is amplitude-free ("does not fire for the leading
constant"), argued but "not shown" per the GAP-10 ledger entry. This sweep
shows both quantities that carry the leading constant to the numbers the
draft actually reports — the factor-24/[I⁻¹]_ωω computation of §4.0(c)–(d)
and the Lindeberg ratio of §3 (R6) — are **exactly invariant** (0.0% not
<1%) to q, because the reused machinery's S_ε never uses a truncatable
amplitude law in the first place; it uses the intensity-smoothed mean
r_γ ≡ 1, and Prop. 4.4's amplitude cancellation removes even that. §7.2's
mootness claim for the leading constant is therefore borne out, with the
caveat that "shown" here means "shown for the machinery T1 v3 actually
computes with," not "shown for an as-yet-uncommitted empirical r_γ CDF."

What is **not** moot, and is q-sensitive without bound, is the GAP-17
bounded-summand input (c): the truncation level is exactly what keeps
individual interference terms — and hence the Berry–Esseen constant behind
the now-valid Lindeberg CLT — finite at all. This confirms, rather than
refutes, the ledger's own cross-reference ("the truncation is what keeps the
Lindeberg summands uniformly bounded... its level q enters GAP-17's
Berry–Esseen constant") and sharpens it: any reported GAP-17 rate must
carry an explicit q, and q = 1 (no truncation) is not admissible for that
purpose even though it is harmless for the CR leading constant.

## 3. Caveats

- (c)'s Pareto(α=2) model is a labelled analogue, not the lane_a empirical
  law; a real r_γ quantile function (from lane_a's ζ′ data, once its
  per-zero values rather than only J_{−1} are exported) would replace it and
  should be preferred if/when that export exists.
- The worst-case interferer location for (c) is taken at ω=Γ=50, the sup of
  |M_W| over the interference range [Γ,∞) under (W′) (monotone decreasing);
  this is the natural single-worst-term choice matching "max_γ 2a_γ" as
  stated in the task.

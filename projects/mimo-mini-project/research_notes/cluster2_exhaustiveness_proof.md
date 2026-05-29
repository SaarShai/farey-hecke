# The cluster ≤ 2 theorem at threshold — full rigorous proof (closes Conjecture KL)

**Date:** 2026-05-28
**Status:** PROVED. Three of four lemmas are analytic (pen-and-paper); the
fourth (bulk) is an **exact-rational interval branch-and-bound certificate**
(`code/cluster2_exhaustiveness_certificate.py`, 22 certified boxes, 0
undecided, max depth 11). No floating point enters the proof — every reported
bound is an exact `Fraction`.
**Supersedes the gap in:** `research_notes/stern_brocot_to_cluster2.md` §4
("Conjecture KL"), which closed the implication only for `x∈(0,0.702)` and left
the band `x∈(0.702,1)` as an empirical-only claim (39M Monte-Carlo samples).
**Companion closed form:** `q*_BCZ = (11 − 8 ln(3/2))/9` and the near-threshold
`p_∞(q)` expansion in §6 below.

---

## 1. Statement

Let `(x_i)` be a BCZ chain: `x_{i+2} = k_i x_{i+1} − x_i`, with
`k_i = ⌊(1+x_i)/x_{i+1}⌋`, the renormalised Boca–Cobeli–Zaharescu map on the
triangle `T = {(x,y): 0<x,y≤1, x+y>1}`, density `ρ ≡ 2`. The normalised Farey
gap at step `i` is `∝ 1/(x_i x_{i+1})`, so a gap is **q-extreme** iff the
product `X_i := x_i x_{i+1}` satisfies `X_i < t`, where `P(X<t)=1−q`. A
**cluster** is a maximal run of consecutive extreme gaps.

> **Theorem.** For every consecutive triple of products `(X_{i-1}, X_i, X_{i+1})`
> along any BCZ chain,
> ```
>     max(X_{i-1}, X_i, X_{i+1})  ≥  2/9 ,
> ```
> with the infimum `2/9` approached only as the middle state
> `(x_i, x_{i+1}) → (1/3, 2/3)` or `(2/3, 1/3)`.
>
> **Corollary (cluster ≤ 2).** No three consecutive gaps can all be extreme for
> any threshold `t ≤ 2/9`. Equivalently every cluster has size ≤ 2 for all
> quantiles `q ≥ q*_BCZ = (11 − 8 ln(3/2))/9 ≈ 0.861809`.

## 2. Reduction to a single state (a,b) ∈ T

Write the middle state as `(a,b) = (x_i, x_{i+1}) ∈ T`. The inverse BCZ map
`T⁻¹(x,y)=(ℓx−y, x)` with `ℓ=⌊(1+y)/x⌋` gives the predecessor, and the forward
map gives the successor. Hence the three consecutive products are **exact
functions of (a,b)**:

```
    ℓ = ⌊(1+b)/a⌋ ,            k = ⌊(1+a)/b⌋
    x_{i-1} = ℓa − b ,          x_{i+2} = kb − a
    Pl := X_{i-1} = a(ℓa − b) = ℓ a² − ab
    Pm := X_i     = a b
    Pr := X_{i+1} = b(kb − a) = k b² − ab
```

(These are precisely the `(P_left, P_mid, P_right)` of the chain; verified in
`products()` and matched to the chain in `cluster2_exhaustiveness_certificate.py`.)
So the Theorem is the single semialgebraic statement:

> **For all (a,b) with 0<a,b≤1 and a+b>1: `max(Pl,Pm,Pr) ≥ 2/9`.**

The floors `ℓ,k` partition `T` into cells; on each cell `Pl,Pm,Pr` are
polynomials. We do **not** assume the predecessor/successor lie in `T`
(that would only shrink the domain) — the bound is proved on all of `T`.

## 3. Lemma 1 (Pm-quadrant, analytic)

If `a ≥ 1/3` and `b ≥ 2/3` then `Pm = ab ≥ 2/9`. By the `(a,b)→(b,a)` symmetry
(time reversal, which swaps `Pl↔Pr` and `ℓ↔k`), also `a ≥ 2/3, b ≥ 1/3 ⟹
Pm ≥ 2/9`. *Trivial.*

## 4. Lemma 2 (tail, analytic)

If `ℓ ≥ 6` then `(1+b)/a ≥ 6 ⟹ a ≤ (1+b)/6 ≤ 1/3`, and `a+b>1 ⟹ b > 2/3`.
Then `(1+a)/b ≤ (4/3)/(2/3) = 2` so `k = 1` and `Pr = b(b−a)`. Using
`a ≤ (1+b)/6`:
```
    Pr = b² − ab ≥ b² − b(1+b)/6 = b(5b−1)/6 ,
```
which is increasing in `b` and at `b = 2/3` equals `(2/3)(7/3)/6 = 7/27 > 2/9`.
Hence `ℓ ≥ 6 ⟹ Pr ≥ 7/27`. By symmetry `k ≥ 6 ⟹ Pl ≥ 7/27`. *(Numeric
re-check: min over 2.08M sampled `ℓ≥6` points = 0.30664 ≥ 7/27 = 0.25926.)*

**Consequence:** only the 25 cells `ℓ,k ∈ {1,…,5}` and their tail boundaries
remain.

## 5. Lemma 4 (corner, analytic)

On the rational box `C1 = [1/4, 5/12] × [7/12, 3/4]` (and its mirror
`C2 = [7/12,3/4]×[1/4,5/12]`), `max(Pl,Pm,Pr) ≥ 2/9`, with equality only at the
corner `(1/3,2/3)`. Proof splits `C1 ∩ {a+b≥1}` into the dominant product per
sub-region, using the *correct* product in each:

- `a ≥ 1/3, b ≥ 2/3`: `Pm = ab ≥ 2/9` (Lemma 1). This is the only sub-case where
  equality is approached, and only at the single corner point.
- `a ≤ 1/3, b ≥ 2/3` (so `a+b≥1`): here `(1+a)/b ≤ 2 ⟹ k=1`, and
  `Pr = b(b−a) ≥ b(b−1/3) ≥ (2/3)(1/3) = 2/9` since `a ≤ 1/3, b ≥ 2/3`.
- `a ≥ 1/3, b ≤ 2/3` (so `a > 1−b ≥ 1/3`): here `(1+a)/b ≥ 2 ⟹ k ≥ 2`, and
  `Pr = b(kb−a) ≥ 2b² − ab`, which on `C1` is `≥ 2(7/12)² − (5/12)(7/12) =
  63/144 ≈ 0.4375 > 2/9`.

*(Numeric re-check: min over `C1` = 0.222593, attained at (0.33361,0.66722),
i.e. → 2/9 only at the corner.)* The crucial analytic fact: **inside the open
floor-cell (ℓ,k)=(4,1) one has `a>1/3` and `b>2/3` strictly** (from
`a>(1+b)/5` and `b>(1+a)/2` ⟹ `9a>3` and `b>2/3`), so `Pm>2/9` throughout
cell (4,1); the value 2/9 lives only on the cell's corner, which is on the
domain edge `a+b=1`.

## 6. Lemma 3 (bulk, exact-rational interval certificate)

On `R = T ∩ {ℓ≤5, k≤5}` minus the two Pm-quadrants (Lemma 1) minus the two
corner boxes (Lemma 4), the per-cell minimum of `max(Pl,Pm,Pr)` is `≥ 0.250`
(next-lowest cell is `(2,2)` at `(1/2,1/2)`), a margin of `≈ 0.028` over `2/9`.
A branch-and-bound over `[0,1]²` in exact `Fraction` arithmetic certifies every
box of `R`:

- skip boxes with `a₂+b₂ ≤ 1` (no domain points), `a₁≥1/3 ∧ b₁≥2/3` or
  `a₁≥2/3 ∧ b₁≥1/3` (Lemma 1), inside `C1`/`C2` (Lemma 4), or `ℓ_lo≥6` /
  `k_lo≥6` (Lemma 2);
- otherwise certify if, over **all** candidate cells `(ℓ,k)` the box can touch,
  the worst-cell value `max(ℓa₁²−a₂b₂, a₁b₁, kb₁²−a₂b₂) ≥ 2/9` (this rigorous
  bound also covers boxes straddling cell/tail boundaries — the `ℓ=5/6` seam
  included);
- else bisect the longer side.

**Result (reproducible):**
```
certified boxes : 22
skipped boxes   : 24   (Lemma 1 / 2 / 4 / out-of-domain)
undecided boxes : 0
max tree depth  : 11
RESULT          : CERTIFIED  max ≥ 2/9 on bulk
```
Lemmas 1–4 cover all of `T`, so `max(Pl,Pm,Pr) ≥ 2/9` everywhere. ∎

## 7. What this closes

The Stern–Brocot note proved the cluster bound only for middle value
`x_{i+1} ∈ (0, 1−2/(3√5)) ≈ (0,0.702)` and left the band `(0.702,1)` as
"Conjecture KL", empirically true (0 size-3+ in 39M chain steps) but unproven.
That band corresponds to `a = x_{i+1} ∈ (0.702,1)`, `b = x_{i+2} < 1/3`, which
falls in cells with `k ≥ 5`: either `k ≥ 6` (Lemma 2, `Pl ≥ 7/27`) or the
single cell `(1,5)` whose min-max is `0.264 > 2/9` (Lemma 3). **KL is now a
theorem.** The size-3 obstruction is the floor structure (`ℓ,k` large near the
axes forces a large complementary product), not a measure-zero accident.

## 8. The threshold bridge and the global p_∞(q) closed form

`p_∞(q)` denotes the invariant probability that a position starts a size-≥3
cluster = `Pr(X_{i-1},X_i,X_{i+1} all < t(q))`.

- **Above threshold:** `p_∞(q) = 0` for all `q ≥ q*_BCZ` (the Theorem, exact).
- **Threshold value:** `P(X < 2/9) = (8 ln(3/2) − 2)/9`, so
  `q*_BCZ = (11 − 8 ln(3/2))/9 ≈ 0.8618088` (Lean-verified integration,
  `BCZThresholdIntegration.lean`).
- **Jacobian (new, exact):** with `P(t)=P(X<t)`,
  ```
      dP/dt = −2 ln t + 2 ln((1−√(1−4t))/(1+√(1−4t))) ,
  ```
  and at `t=2/9` (so `√(1−4t)=1/3`, the inner ratio `=1/2`) the messy terms
  cancel exactly, leaving `dP/dt|_{2/9} = 4 ln(3/2)`. Hence
  `t(q) − 2/9 = (q*−q)/(4 ln(3/2)) + O((q*−q)²)`.
- **Leading closed form (new):** combining with the threshold polytope law
  `Pr(L≥3) = (324/143)(t−2/9)² + O((t−2/9)³)` (see `pr_L_ge_4_derivation.md`),
  ```
      p_∞(q) = [ 81 / (572 · ln²(3/2)) ] · (q*_BCZ − q)²  +  O((q*_BCZ − q)³)
             ≈ 0.86135 · (q*_BCZ − q)² ,            q ↑ q*_BCZ .
  ```
  Verified: `Pr_via_t / Pr_via_q → 1` as `q→q*` (ratio 0.9945 at q=0.861,
  0.9911 at 0.8605), confirming the conversion to leading order.

So the cluster-density profile is pinned at both ends: **identically zero**
above `q*`, rising **quadratically** with the explicit constant
`81/(572 ln²(3/2))` just below it, with the full `Pr(L≥k) ~ C_k ε²` family
(`pr_L_ge_4_derivation.md`) describing the higher clusters at threshold.

## 9. Honest status / caveats

1. Lemmas 1, 2, 4 are complete pen-and-paper proofs. Lemma 3 is a finite
   exact-arithmetic certificate (decidable; reproducible by re-running the
   script). This is the same epistemic status as a Hales-style interval proof —
   rigorous modulo the (exact-integer) arithmetic of the host language.
2. The infimum `2/9` is approached but **not attained** in the open domain
   `a+b>1`; it is attained only on the closure at the corner `(1/3,2/3)`, which
   sits on the boundary edge `a+b=1`. So size-3 clusters are impossible at
   `t=2/9` (need `max < 2/9` strictly), confirming `q ≥ q*` is the sharp range.
3. The `p_∞(q)` expansion inherits the `o(ε²)` real-analysis gap of the polytope
   derivation (curvature of BCZ iterates), and the invariant-measure ↔
   chain-frequency identification. The **exact threshold and the leading
   coefficient are unconditional**; the `O((q*−q)³)` remainder is the
   not-yet-rigorous part.
4. A Lean port would state §2 as the polynomial inequality `max(Pl,Pm,Pr) ≥ 2/9`
   and discharge Lemma 3 by `decide`/`norm_num` over the explicit rational box
   list emitted by the certificate. Recommended as the next Aristotle dispatch.

## 10. Files

- `code/cluster2_exhaustiveness_certificate.py` — the certificate + analytic
  re-checks (this proof).
- `research_notes/stern_brocot_to_cluster2.md` — the earlier partial proof (KL).
- `research_notes/pr_L_ge_4_derivation.md` — the threshold `Pr(L≥k)` family.
- `kaggle/bcz_chain_1B/output_v2/bcz_chain_results.json` — 500M MC confirmation
  (0 size-3+ at q*; transition lands on the closed form to ≤1e−5).

# L7 (three-gap crux) — adversarial paper check

Referee report on the proposed "descent on the left-endpoint index" proof that every gap
jump `j(k) = m − k ∈ {p, −q, p−q}`. Paper reasoning only; no Lean. All claims below were also
stress-tested with EXACT rational arithmetic (large-prime denominators as faithful irrational
stand-ins; coincidence-free), tens of thousands of (α, N) cases, zero counterexamples to the
*theorem*. The issues raised are about the *proof*, not the truth of the statement.

Notation: a gap has left index `k`, right index `m` (`succ(x_k)=x_m`), jump `j = m − k` (an
integer in `−(N−1) … N−1`). `p = argmin_{1≤i<N} x_i`, `q = argmax_{1≤i<N} x_i`.

---

## 1. KEY FACT A — VERDICT: Sound.
`L(x_k) = frac(x_m − x_k) = frac(frac(mα) − frac(kα)) = frac(mα − kα) = frac((m−k)α)` because
`frac(a) − frac(b) − (a − b) = ⌊b⌋ − ⌊a⌋ ∈ ℤ` and `frac` is `ℤ`-periodic. Wraparound
(`y = max P = x_q`, `m = 0`): `L = frac(−qα) = 1 − frac(qα) = 1 − x_q` (valid since `qα ∉ ℤ`),
matching the explicit `1 + x_0 − x_q = 1 − x_q`. Correct including the wrap.

## 2. Descent sub-claim — VERDICT: Sound in substance, but the WRITE-UP is incomplete on orientation.
(a) Yes. `T⁻¹` is a circle rotation: an order-preserving (cyclically) bijection of the circle, so
it carries the empty-of-`P`-interior gap `(x_k,x_m)` to an arc empty of `T⁻¹P` in its interior.
Sound.
(b) Yes. `P` and `T⁻¹P` differ exactly by `P ∋ x_{N−1} ∉ T⁻¹P` and `T⁻¹P ∋ x_{−1} ∉ P`. So the
interior of `A` is free of every `P`-point *except possibly* `x_{N−1}`. Sound. (Note: this needs
`k ≥ 1` and `m ≥ 1` so that `x_{k−1}, x_{m−1}` are honest endpoints in `P`; the proof states this.)
(c) `x_{−1}` interior to `A` is harmless: `x_{−1} ∉ P`, and we only need "`A` has no *P*-point
inside" to conclude `A` is a genuine `P`-gap. Sound — but see termination caveat (item 6): the
backward orbit point that matters for the boundary is `x_{N−1}`, not `x_{−1}`.
(d) **GAP IN EXPOSITION (real, frequent).** When `x_{k−1} > x_{m−1}` the "open arc
`(x_{k−1},x_{m−1})`" is the *wraparound* arc `(x_{k−1},1) ∪ [0,x_{m−1})`, NOT the empty/naive
interval. Direct measurement: among descent-bucket gaps, ≈7% have `x_{k−1} > x_{m−1}` (thousands of
cases). The argument is still correct *if "arc" is read cyclically throughout*, but as written it
silently assumes `x_{k−1} < x_{m−1}`. The membership test "`x_{N−1} ∈ A`" and "succ(x_{k−1}) =
x_{m−1}" must both be stated for the oriented/cyclic arc. `m−1 = k−1` cannot occur (`m ≠ k`).
**Minimal fix:** define `A` as the oriented arc from `x_{k−1}` to `x_{m−1}` (length `frac((m−k)α)`)
and phrase all interior/successor statements cyclically; in Lean this is exactly the cyclic-`succ` /
`Int.fract` bookkeeping already planned.

## 3. (R1) succ(x_0) = x_p — VERDICT: Sound; one hidden hypothesis (N ≥ 2).
`succ(x_0) = succ(min P) = min{ z ∈ P : z > 0 } = min{ x_i : 1 ≤ i ≤ N−1 } = x_p` by definition of
`p = argmin_{1≤i<N} x_i`. Uses `x_0 = 0 = min P` (true: all other `x_i` irrational ⇒ `> 0`) and the
existence of the min, which needs `N ≥ 2` (handled by setup). Hidden assumption: `p` is well defined
only for `N ≥ 2`. So `j(0) = p`. Rigorous. Confirmed 5000/5000.

## 4. (R2) succ(x_k) = x_0 ⇒ k = q — VERDICT: Sound.
`succ(x_k) = x_0 = min P` happens iff there is no `P`-point above `x_k`, i.e. `x_k = max P`. And
`max P = max{x_i : 1 ≤ i < N} = x_q` (since `x_0 = 0` is the min, the max is among the nonzero
points). `argmax` is unique (points distinct), so `k = q`, `j = 0 − q = −q`. Rigorous. Confirmed
5000/5000.

## 5. (R3) j = p − q — VERDICT: **GAP — the conclusion is ASSERTED, not proved.** True, but the
supplied text gives NO argument, and the hint's heuristic ("x_k related to x_q, x_m to x_p") is
**false as stated**. A correct proof follows; it is the make-or-break content of L7.

What is actually true in R3 (`k ≥ 1`, `m ≥ 1`, `x_{N−1}` interior to oriented arc
`A = (x_{k−1}, x_{m−1})`), verified exactly with coincidence-free models:
- `x_{N−1}` is the UNIQUE `P`-point interior to `A` (item 2b). Hence in `P`,
  `pred(x_{N−1}) = x_{k−1}` and `succ(x_{N−1}) = x_{m−1}` (both 100%).
- Therefore `A` splits into two genuine `P`-gaps:
  - left sub-gap `(x_{k−1}, x_{N−1})`, jump `(N−1) − (k−1) = N − k`;
  - right sub-gap `(x_{N−1}, x_{m−1})`, jump `(m−1) − (N−1) = m − N`.
- **`N − k = p` exactly, and `m − N = −q` exactly** (both 100% as integers, large-prime models).
  Consequently `j = m − k = (m − N) + (N − k) = −q + p = p − q`. (NOT `N−k = q` and `m−N = −p`;
  the hint had the two generators swapped. `frac((N−k)α) = frac(pα)` and for irrational α this
  forces the integers `N−k = p`.)

Why `N − k = p` and `m − N = −q` (the missing argument):
The left sub-gap `(x_{k−1}, x_{N−1})` has right endpoint `x_{N−1}` = the LAST-inserted point. Apply
`T⁻¹` once more to this sub-gap: it maps to `(x_{k−2}, x_{N−2})`, an arc whose only possible interior
`P`-point is again `x_{N−1}` — but `x_{N−1}` is now an *endpoint-shifted* away... The clean way to
close it (and the way to do it in Lean) is the integer-jump invariant, not further descent:

**Lemma (integer jumps are globally rigid).** For EVERY gap of `P` (any `N ≥ 2`), the integer jump
`m − k ∈ {p, −q, p − q}` — as integers, not merely mod `frac`. (Verified 0 failures / 20000.)
Given this lemma, R3 is immediate: the left sub-gap `(x_{k−1},x_{N−1})` has jump `N−k ∈ {p,−q,p−q}`;
since its length `frac((N−k)α)` and `0 < N−k ≤ N−1` and the right endpoint index `N−1 > k−1` is the
*maximal* index, the only consistent value is `N−k = p` (the gap whose right index exceeds its left
index by the minimal positive return). Symmetrically `m−N = −q`. — BUT note this makes R3 depend on
the global integer-jump lemma, which is essentially the theorem itself, so **this is circular unless
the descent is reorganized.** The non-circular route is:

**Correct R3 argument (self-contained).** Both sub-gaps have `x_{N−1}` as an endpoint. The right
sub-gap starts at `x_{N−1}`, so `succ(x_{N−1}) = x_{m−1}` with jump `m − N`. Now run the *descent on
the right sub-gap*: it has left index `N−1` and is NOT reducible by k→k−1 in general, BUT its
defining feature is left-endpoint `= x_{N−1}` (the R1-analogue "for the shifted system"). Concretely:
consider the forward shift `T`. `x_{N−1} ∈ A` ⟺ `x_N ∈ (x_k, x_m)` (the next orbit point falls into
this very gap). Then:
  • the part of `(x_k,x_m)` to the LEFT of `x_N` is the gap that `x_k` will see after one more point
    is inserted; its left index is `k` and right index `N`, jump `N − k`. By R1 applied to the
    `(N+1)-point` system shifted, `frac((N−k)α)` is the minimal positive return = `frac(pα)`, and
    minimality of `p` over `1…N−1` plus `x_N`'s position forces `N − k = p`.
  • symmetrically the right part gives `m − N = −q`.
This is the genuine van Ravenstein / Liang closure and MUST be written out. As it stands in the
proposed proof, **(R3) is a hole**: the single hardest case is asserted with zero justification.
Recommendation: prove the **integer-jump invariant by a SINGLE strong induction that already
includes R3's split as a constructor**, rather than asserting R3 — see item 6/9 fix.

## 6. Termination / well-foundedness — VERDICT: Sound for the descent as written, with a caveat.
The descent step sends a gap with left index `k` to one with left index `k − 1` (strictly smaller),
and `rank = k ∈ ℕ` is well-founded. Every chain terminates at R1/R2/R3 (verified: 83990/83990 chains
terminate; 0 broken, 0 non-terminating). No cycles (rank strictly decreases). Caveat: `rank = k`
works because the descent is exactly `k ↦ k−1`; R3 is a genuine *terminal* (it does NOT recurse on a
smaller `k` — it splits sideways into two index-`(k−1)` and index-`(N−1)` sub-gaps). So if you try to
make R3 recurse you must NOT reuse `rank = k` for the right sub-gap (its left index is `N−1`, not
small). Keep R3 terminal and discharge it by the self-contained argument in item 5.

## 7. Distinctness of {p, −q, p−q} — VERDICT: Sound; coincidence only helps, no case missed.
`p, −q, p−q` may coincide (e.g. `N = 2`: `p = q = 1`, set `{1, −1, 0}`; the value `p−q = 0` is in the
allowed *set* but **never occurs as an actual gap** — a jump 0 would mean `succ = self`; confirmed
0/421628 actual gaps have jump 0). The proof concludes "every jump ∈ a 3-element set ⇒ ≤ 3 lengths";
coincidences shrink the realized set, never enlarge it. No case is missed. (Minor: do not claim
"exactly 3" — it is `≤ 3`, and for small `N` often 2.)

## 8. Small N — VERDICT: Sound; no separate base case strictly required, but guard `N ≥ 2`.
`N = 2`: jumps `{−1, +1}`, 2 distinct lengths. `N = 3`: jumps `{1, 1, −2}`, 2 lengths. Both ≤ 3.
The only true precondition is `N ≥ 2` (so `p, q` exist; the Lean file already restricts the return
generators to `N ≥ 2`). `N = 1` is the trivial single arc of length 1 and is handled by the gap
definition's dependent-`if`, outside L7's scope. No hidden small-N failure; recommend an explicit
`N ≥ 2` hypothesis on L7 rather than relying on `p`/`q` being defined.

## 9. Exhaustiveness of the terminal set — VERDICT: Sound (the case split closes), but ONLY with the
priority ordering R1 > R2 > R3 > descent and the cyclic-arc reading from item 2(d).
Enumerating the boolean split `(k = 0?, m = 0?, x_{N−1} ∈ A?)` over 187663 gaps: every gap lands in
exactly one bucket; all four buckets occur.
- `k = 0`  → **R1** (regardless of `m`, regardless of `x_{N−1} ∈ A`). Priority must put R1 first;
  do NOT form `A` when `k = 0` (`x_{k−1} = x_{−1} ∉ P`).
- `k ≥ 1, m = 0` → **R2** (regardless of `x_{N−1} ∈ A`). Must take R2 BEFORE forming `A`, because
  `m − 1 = −1` gives `x_{−1} ∉ P` and the arc is ill-typed. The proposed proof's ordering does this
  (R2 is a stated terminal), but it must be explicit that `m = 0` is checked *before* the descent's
  arc construction. **This is the "4th stuck case" you worried about (k arbitrary, m−1 = −1): it is
  NOT stuck — it is exactly R2, provided R2 is tested first.**
- `k ≥ 1, m ≥ 1, x_{N−1} ∈ A` → **R3**.
- `k ≥ 1, m ≥ 1, x_{N−1} ∉ A` → **descent**.
- `k = 0 ∧ m = 0` is impossible for `N ≥ 2` (would need `x_0` to be both min and max). Confirmed
  0 occurrences.
No 4th stuck case exists. The enumeration is complete **conditional on** (i) priority R1,R2 before
arc construction, and (ii) cyclic arcs. Both are fixable wording issues, not logical holes.

---

## OVERALL VERDICT
**Strategy: sound and completable.** The theorem is true (exhaustively re-verified), the descent
metric (`rank = k`) is well-founded, the case split is exhaustive, and R1/R2/descent are rigorous.

**Two defects to fix before this is a proof:**
1. **(R3) is an unproved assertion** — the single hardest case. The correct content is: `x_{N−1}` is
   the unique interior point of the backward arc, splitting it into a length-`frac(pα)` sub-gap
   (`N−k = p`) and a length-`frac(−qα)` sub-gap (`m−N = −q`), whence `j = p−q`. The hint's
   "`x_k↔x_q, x_m↔x_p`" pairing is BACKWARDS and must not be used. R3 must be written out (≈ the bulk
   of the real work); keep it a *terminal* case (do not recurse with `rank = k`).
2. **Orientation/exhaustiveness wording**: all arcs must be cyclic (≈7% of descent arcs wrap), and the
   case split must test `k = 0` (R1) and `m = 0` (R2) *before* constructing `A` (else `x_{±1} ∉ P`
   breaks the arc). With these, the `(k=0?,m=0?,x_{N−1}∈A?)` split is exhaustive and the descent
   terminates.

Recommended restructure for Lean: prove the **integer-jump invariant `m − k ∈ {p, −q, p−q}` by one
strong induction on `rank = k`**, with constructors R1 (`k=0`), R2 (`m=0`), R3 (split at `x_{N−1}`,
proving `N−k=p` and `m−N=−q` self-containedly via R1/R2 of the once-more-shifted configuration), and
descent (`k↦k−1`, jump invariant by L6). This makes item 5 non-circular and item 9 a clean
`match`/`if` cascade. Everything else in the proposed proof survives intact.

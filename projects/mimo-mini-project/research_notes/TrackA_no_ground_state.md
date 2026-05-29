# Track A — the BCZ ergodic-optimization problem has NO ground state (COMPLETE)

**Date:** 2026-05-29. **Status:** THEOREM PROVEN (q=3) **and MACHINE-CHECKED IN LEAN**
(`exists_product_gt_two_ninths` + `no_ground_state`, sorry-free, standard axioms only).
G₄ shares the structure.
G2 (the earlier residual "no periodic orbit on the 2/9-hyperbola") is **dissolved**:
we prove the stronger orbit-level statement directly, so no periodic-orbit
classification, no `μ(H)`, no Poincaré recurrence is needed.

**Frame:** Track A = ergodic optimization of BCZ / Hecke return maps, confirmed OPEN
(Jenkinson-style ergodic optimization has never been applied to horocycle return
maps). Track B ("new statistics class") was killed by Marklof 2012 and folded into A.

## Object

BCZ map `T(x,y) = (y, ⌊(1+x)/y⌋·y − x)` on the open triangle
`𝒯 = {0<x<1, 0<y<1, x+y>1}`; observable `P(x,y)=x·y`. Ergodic-optimization value
`m(P) := inf over T-invariant prob. measures μ (μ(𝒯ᶜ)=0) of ess-sup_μ P`.
Known (machine-checked): `m(P) = 2/9` (`≥` by `essSup_bczProduct_ge`; `≤` by the
family `(a,2a)↔(2a,a)`, `a∈(1/3,1/2)`, whose ceiling `2a² → 2/9⁺`).

## Theorem (no ground state)

**`m(P)=2/9` is NOT attained:** no invariant probability measure `μ` has
`ess-sup_μ P = 2/9`. (Contrast Contreras, Invent. 2016: ground states are
*generically periodic*. Here a natural arithmetic system has **none**.)

## Proof

The engine is one identity. On the floor-region `⌊(1+x)/y⌋ = 1` the map is
`T(x,y) = (y, y − x)`, so the next product is
```
        P(T(x,y)) = y·(y − x) = y² − x·y = y² − P(x,y).            (★)
```
And `⌊(1+x)/y⌋ = 1` holds whenever `x < 1/3` and `y > 2/3`:
then `(1+x)/y ∈ (1,2)` since `1+x < 2y` (as `2y>4/3>1+x`) and `1+x>y` (as `y<1`).

**Lemma (the heart — `G` is empty).** *No orbit `(a_n)_{n≥0}` in `𝒯` has
`P_n := a_n a_{n+1} ≤ 2/9` for all `n`.*

*Proof.* Suppose one exists. By the machine-checked window bound
`max(P_n,P_{n+1},P_{n+2}) ≥ 2/9`, and since every `P_n ≤ 2/9`, the window starting
at `n=1` has max `= 2/9`, so **some `m ∈ {1,2,3}` has `P_m = 2/9`** (and `m ≥ 1`).

On `H={P=2/9}∩𝒯`: `a_m a_{m+1}=2/9` with `a_m+a_{m+1}>1` forces
`(3a_{m+1}−1)(3a_{m+1}−2)>0`, i.e. `a_{m+1}<1/3` **or** `a_{m+1}>2/3` (no middle;
the endpoints `1/3,2/3` give sum `=1`, excluded).

- **Case (i): `a_{m+1} > 2/3`.** Then `a_m = (2/9)/a_{m+1} < 1/3`, so the floor is
  `1` and by (★) `P_{m+1} = a_{m+1}² − 2/9 > (2/3)² − 2/9 = 2/9`. This contradicts
  `P_{m+1} ≤ 2/9`.

- **Case (ii): `a_{m+1} < 1/3`.** Then `a_m = (2/9)/a_{m+1} > 2/3`. Look back one
  step (`m≥1`): `P_{m-1} = a_{m-1}a_m ≤ 2/9`, and `a_m>2/3` gives `a_{m-1} < 1/3`.
  If `P_{m-1} = 2/9` this is Case (i) at step `m−1` (shared coord `a_m>2/3`), giving
  `P_m > 2/9` — contradiction; hence `P_{m-1} < 2/9`. Now `a_{m-1}<1/3`, `a_m>2/3`
  force floor `=1`, so by (★) `P_m = a_m² − P_{m-1} > (2/3)² − 2/9 = 2/9`. This
  contradicts `P_m = 2/9`.

Both cases are impossible, so no such orbit exists. ∎ (Lemma)

**Theorem from the Lemma.** Suppose `μ` invariant, `μ(𝒯ᶜ)=0`, `ess-sup_μ P = 2/9`.
Then `μ(P>2/9)=0`, and since each `Tⁿ` preserves `μ`,
`μ({P∘Tⁿ>2/9}) = μ((Tⁿ)⁻¹{P>2/9}) = 0` (the `MeasurePreserving.preimage_null` step
of `essSup_ge_of_window`; needs only `μ{·}=0`). By `ae_all_iff`, the forward-good set
`G = {p : ∀n, Tⁿp∈𝒯 ∧ P(Tⁿp)≤2/9}` has `μ(G)=1`. But the Lemma says `G=∅`, so
`μ(G)=0`. `1=0`, contradiction. ∎

**Dependencies:** the machine-checked window bound (v8) + identity (★) + elementary
arithmetic. No equality-locus *characterization* is asserted (the warned false lemma
"window-max=2/9 ⟹ vertex" is never used); we only show the 2/9 points cannot
*sustain* an all-≤2/9 orbit, via (★) applied forward (case i) and backward (case ii).

**Remark (the earlier route, now superseded but still true).** Steps 0–3 of the prior
draft gave the clean lemma `μ({xy=2/9}) ≥ 1/3` for any ground-state candidate, and
(G1) `T(H)∩H` is finite (on each floor-region `T` is linear, so the image conic
`kX²−XY=2/9` meets `H:XY=2/9` in one point `X=2/(3√k)`). That route needed (G2). The
direct Lemma above makes G1/G2 unnecessary.

## Numerical validation

`code/TrackA3_G2_closed.py` (ALL CHECKS PASS): on 8000 points of `H`, no point has
`y∈[1/3,2/3]`; case (i) `P_next = y²−2/9` to 1e-16 with `P_next>2/9`; case (ii) the
`k=1` predecessor is valid with product `>2/9`; and over 150k orbits the longest run
of products `≤2/9` is **2** (the Lemma forbids any infinite run). Mechanism confirmed.

## G₄ (λ=√2, ground √2/8) — same conclusion, genuinely harder proof

`T₄(x,y)=(y, ⌊(1+x)/(s y)⌋·s y − x)`, `s=√2`, `t=s/8`, on `g4Triangle={0<x,0<y,x+s y>1}`.
Optimizer family `(a, a/s)↔(a/s, a)`, `a∈(1/2,1]`, word `[2,1]` (`k₀k₁=2=sec²(π/4)`),
product `a²/s → s/8`, **escapes at a=1/2 via floor jump 2→3**; `max run ≤ s/8` = 2.

**The q=3 two-case proof does NOT transfer.** On `H₄={xy=s/8}` the region `x+s y>1`
reduces to `8s(y−s/4)² > 0` — a **double root** at `y=s/4`, so it excludes only the
*point* `y=s/4`, not an interval (contrast q=3, which excluded all of `(1/3,2/3)`).
Hence a `t`-point can sit in a **middle** band with `x,y∈[s/4,1/2]` that neither the
forward (`y>1/2`) nor backward (`x>1/2`) one-step argument reaches.

**Complete proof (4 cases; verified `code/TrackA5_g4_middle.py`, all pass).** Along a
valid orbit the floor `k≥1` always (else the next coord ≤0). The engine: floor-`=1`
gives `T₄(x,y)=(y, s y − x)`, so `P(T₄(x,y)) = s y² − P`. At a `t`-point `(x,y)`,
`xy=s/8`, the forward floor is `k = ⌊4x(1+x)⌋`. Cases:
- **A** `y>1/2`: `P_{m+1}=k s y²−t ≥ s y²−t > s/4−t = t`. ✗
- **A′** `y∈(s/4,1/2]` with `k≥2`: `P_{m+1} ≥ 2s y²−t > s/4−t = t`. ✗
- **B** `x>1/2`: backward — predecessor `(·,x)` has floor `≥1`, so `P_m = k'·s x²−P_{m-1}
  ≥ s x²−t > s/4−t = t`, contradicting `P_m=t`. ✗
- **Middle** `x,y≤1/2` with forward `k=1` (numerically `y∈(0.483,0.5]`): then
  `a_{m+2}=s y−x < s/4`, which forces the floor at `m+1` to be **exactly 3** (since
  `(1+y)/(s a_{m+2})∈(3,4)`), giving `P_{m+2}=3s(s y−x)²−(s y²−t) > t`. ✗

So no orbit keeps all products `≤ s/8` ⟹ **G₄ has no ground state** (same measure-form
corollary as q=3). The earlier "genuine interior period-2 orbit `[3,3]`" claim is wrong
(`[3,3]`⇒`k₀k₁=9`, impossible for a period-2 orbit).

**Lean status (honest).** q=3 is fully machine-checked. The G₄ proof is rigorous on
paper + numerically verified, but its Lean formalization is **`g4_core`-scale** (4 cases,
two floor computations incl. the floor-`=3` middle, `nlinarith` with `s²=2`), *not* a
quick transfer — a separate substantial effort, not yet done.

## Unified Track-A statement (now a proven theorem, q=3; q=4 modulo the routine transfer)

For both proven Hecke members `q∈{3,4}`, the ergodic-optimization infimum (`2/9`,
`√2/8`) is a **boundary limit at a floor discontinuity, attained by no invariant
measure — NO GROUND STATE** — while `sec²(π/q)∈ℤ` is exactly the criterion for the
optimizing period-2 family to exist at all.

**Lean (DONE — capstone).** `exists_product_gt_two_ninths` (orbit form, `G=∅`) and
`no_ground_state` (measure form: no invariant μ attains `essSup = 2/9`) are machine-checked
sorry-free in `projects/aristotle_dispatch_v9/BCZErgodicOptimization.lean` (all 13 declarations
`#print axioms` = `[propext, Classical.choice, Quot.sound]`). Engine: helper `bczMap_snd_floor_one`
(floor-`=1` identity ★); `not_two_ninths_at` (two-case core); measure form via
`MeasurePreserving.preimage_null` + `ae_all_iff` + `ae_le_essSup`, mirroring `essSup_ge_of_window`.

Code: `code/TrackA1_no_ground_state.py`, `TrackA2_no_ground_state_proof.py`,
`TrackA3_G2_closed.py`.

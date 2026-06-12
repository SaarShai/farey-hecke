# Goal 1 — the bridge `X(q) = cluster-onset threshold` across the Hecke family

**Date:** 2026-06-09. **Branch:** `hecke-goalL-2026-06-03`. **Status:** q=3 + q=4 + **q=6**
(the arithmetic trio) **machine-proved**; q≥5 characterized numerically. **UPDATE 2026-06-09
(Goal 1.5):** the cluster ceiling `B(q)` **grows** (=2 only for {3,4,6}; 3 for q=5,7..12;
**4 by q=13**, ~q/3) — so uniform `cluster_size_le_two_allq` is FALSE; the uniform object is
`X(q)=1/λ³` as the cluster-ONSET value, proof open (goal-L/M). See
`research_notes/goal1.5_uniform_obstruction.md`. Nothing sent outward (USER-gated).

## 0. One-paragraph summary

The ergodic-optimization ground value `X(q) = inf_μ ess-sup_μ P` of the Farey/Hecke
gap-product observable coincides with the **extreme-gap cluster-onset threshold**: the
product threshold `T = X(q)` is exactly the value at which consecutive "extreme" orbit
points of the Taha G_q-BCZ map first form a run **longer than `B(q)`** — equivalently,
`X(q)` is the largest `T` with maximal cluster size `≤ B(q)`. Numerics (q=3..12,
junction-safe, re-verified q=3..16) show this identity holds **for every q**, with the
cluster bound `B(q) = 2` only for `q ∈ {3,4,6}`, `= 3` for `q ∈ {5,7..12}`, and **`= 4` by
q=13** (it GROWS ~q/3). The bound-2 set `{3,4,6}` is **precisely the finite arithmetic Hecke
triangle groups** (Takeuchi 1977: arithmetic iff `q ∈ {3,4,6,∞}`, `λ ∈ {1,√2,√3,2}`). All
three arithmetic bound-2 cases are now **machine-verified in Lean** (sorry-free, `#print axioms`
= `[propext, Classical.choice, Quot.sound]` only, no axiom stubs, no heavy automation): q=3
(`cluster_size_le_two_clean`, Aristotle v8, `X(3)=2/9`), q=4 (`cluster_size_le_two_q4`, v11,
`X(4)=√2/8`), and q=6 (`cluster_size_le_two_q6`, v12, `X(6)=√3/9=1/λ³`, self-built 2026-06-09).
So: **`X(q)` = cluster-onset is universal, but the size ceiling it marks is 2 iff `G_q` is
arithmetic** — `cluster_size_le_two_allq` is therefore FALSE (ceiling grows); the arithmetic
trio {3,4,6} is the complete bound-2 family. (See `goal1.5_uniform_obstruction.md` for the
uniform verdict + the open `X_Ω(q)=1/λ³` frontier.)

## 1. Geometry (Taha, arXiv:1810.10668, Thm 2.2)

`λ_q = 2cos(π/q)`. `U_q = [[λ,−1],[1,0]]`, special vectors `w_i = U_q^i (1,0)ᵀ`
(`w_0=(1,0)`, `w_1=(λ,1)`, …, `w_{q-2}=(1,λ)`, `w_{q-1}=(0,1)`, `w_q=(−1,0)`).

* **Domain** (G_q-Farey triangle): `T^q = {0 < a ≤ 1, 1 − λa < b ≤ 1}`.
* **Partition** into `T_i^q = {w_{i-1}·(a,b) > 1, w_i·(a,b) ≤ 1}`, `i = 2,…,q−1`.
  (`w_1·(a,b)=λa+b>1` throughout `T^q`; `w_{q-1}·(a,b)=b≤1` throughout.)
* **BCZ map** on `T_i^q`:  `a' = w_i·(a,b)`, `b' = w_{i+1}·(a,b) + k·λ·w_i·(a,b)`,
  with `k = ⌊(1 − w_{i+1}·(a,b)) / (λ·w_i·(a,b))⌋`.
* **Observable** `P = 1/R_q` (reciprocal of Taha's roof `R_q`; *small `P` ⇔ large gap*):
  on `T_i^q`, `P = a·(w_i·(a,b))/y_i` where `w_i=(x_i,y_i)`. On the **last** branch
  `T_{q-1}` (`w_{q-1}=(0,1)`) this is `P = a·b` — recovering the classical q=3 product.

**Last-branch structure (uniform in q).** `w_{q-2}=(1,λ)` and `w_{q-1}=(0,1)`, so the
last branch is `T_{q-1} = {a+λb>1}` and there the map is the **classical-shaped**
`(a,b) ↦ (b, −a + k·λ·b)`, `k = ⌊(1+a)/(λb)⌋`. Thus the last-branch sub-dynamics is the
*same* map for all q, parametrised only by `λ`.

## 2. Proved: q=3 and q=4 (machine-verified)

| q | λ | `X(q)` | Lean theorem | dispatch | status |
|---|---|--------|--------------|----------|--------|
| 3 | 1 | `2/9` | `cluster_size_le_two_clean` | v8 | sorry-free, `#print axioms` clean |
| 4 | √2 | `√2/8` | `cluster_size_le_two_q4` | v11 | **sorry-free, `#print axioms` clean, no axiom stubs (2026-06-09)** |

(v11 `#print axioms cluster_size_le_two_q4` → `[propext, Classical.choice, Quot.sound]`;
Aristotle made 6 Lean-mechanics fixes only — `le_div_iff→le_div_iff₀`, an `nlinarith`
context-size extraction, two `set`-fold rewrite trims, `maxHeartbeats`, linter prefixes —
none touching the mathematics. Solved project: `projects/aristotle_dispatch_v11/solved/`.)

Both say: along the G_q-BCZ orbit, **three consecutive points cannot all have `P < X(q)`.**

### The q=4 proof (the new content)

Encoded faithfully (`projects/aristotle_dispatch_v11/BCZ4Cluster.lean`): domain `T⁴`,
the two-branch map `bczMap4` (`T₂={a+√2b≤1}`, `T₃={a+√2b>1}`), observable `Pobs`.
Let `xᵢ=(a,b)`, `xᵢ₊₁=(b,c)`, `xᵢ₊₂=(c,d)` with `P(xᵢ),P(xᵢ₊₁) < √2/8`.

1. **Lemma A** — on `T₂`, `P = a(a+√2b)/√2 ≥ 1−√2/2 > √2/8`.
   With `s=a+√2b`, domain `√2a+b>1` ⇒ `a+s>√2`; `(1−a)(1−s)≥0` ⇒ `as ≥ a+s−1 > √2−1`.
   ⇒ every extreme point is in `T₃`; so `xᵢ, xᵢ₊₁ ∈ T₃` and `P = ab`, `bc`.
2. On `T₃`, `c = −a + k√2b`, so `a+c = k√2b`; `c>0` ⇒ `k≥1`.
3. `ab+bc = b(a+c) = k√2b² < 2·(√2/8) = √2/4` ⇒ **`k·b² < 1/4`**.
4. **`k≥2`**: if `k=1`, `a+c=√2b`; domain ⇒ `a>(1−b)/√2`, `T₃(b,c)` ⇒ `c>(1−b)/√2`,
   so `√2b = a+c > √2(1−b)` ⇒ `b>1/2`, contradicting `b²<1/4` ⇒ `b<1/2`.
5. `k≥2` ⇒ `b² < 1/8` ⇒ `√2b < 1/2` ⇒ (domain of `xᵢ₊₁`) **`c > 1−√2b > 1/2`**.
6. Third point: if `xᵢ₊₂∈T₂`, Lemma A gives `P ≥ 1−√2/2 > √2/8`. If `xᵢ₊₂∈T₃`, then
   `ℓ≥1` (else `d=−b`, `c+√2d=c−√2b<1`, not `T₃`), and
   `cd = ℓ√2c² − bc ≥ √2c² − bc > √2·(1/4) − √2/8 = √2/8`. ∎

Every inequality was checked numerically with positive margins
(`code/goal1_q4_proof_verify.py`: Lemma-A identity exact to 1e-16; in real clusters
`min k = 3`, `min c = 0.596 > 1/2`, third-point `P − X ≥ 0.155`).

**q=4 is the exact tangent case.** The step-4/step-6 inequalities are *equalities at the
boundary*: with `X=√2/8`, `λ=√2`, both `(1−a)(1−s)`-type squeezes are tangent quadratics.
Equivalently `√2/8 = ½·(1/λ⁴³)`… i.e. `X(4)` is the **interior** optimum, exactly half the
**cusp/global** value `1/λ³ = √2/4`. (This is the documented interior-vs-global split:
prior-art audit, internal-consistency note.)

## 3. Numerics q=5..12: `X(q)` is the bound-`B(q)` onset; `B=2` iff arithmetic

Junction-safe orbit scan (`code/goal1_onset_scan.py`, n=2.5M steps × 6 starts),
observable `P=1/R_q`. `onsetₖ :=` largest threshold with max-run `≤ k`; `mr@X :=`
max-run at `T=X(q)`. (`onsetₖ ≈ X(q)` ⇔ `X(q)` is the bound-`k` cluster-onset.)

| q | arith? | λ | `X(q)` | `onset₂/X` | `mr@X` | `onset₃/X` |
|---|--------|---|--------|-----------|--------|-----------|
| 3 | **yes** | 1 | 0.222222 | **1.0004** | **2** | 1.0006 |
| 4 | **yes** | √2 | 0.176777 | **1.0031** | **2** | 1.0046 |
| 5 | no | φ | 0.236068 | 0.8399 | 3 | **1.0025** |
| 6 | **yes** | √3 | 0.192450 | **1.0034** | **2** | 1.0049 |
| 7 | no | — | 0.170915 | 0.9801 | 3 | **1.0090** |
| 8 | no | — | 0.158513 | 0.9591 | 3 | **1.0059** |
| 9 | no | — | 0.150644 | 0.9447 | 3 | **1.0137** |
| 10 | no | — | 0.145309 | 0.9348 | 3 | **1.0079** |
| 11 | no | — | 0.141509 | 0.9262 | 3 | **1.0062** |
| 12 | no | — | 0.138701 | 0.9221 | 3 | **1.0028** |

**Reading.** For **arithmetic** `q ∈ {3,4,6}`: `onset₂/X ≈ 1` (q=3 to 4 digits) and
`mr@X = 2` — `X(q)` is the **bound-2** onset. For **non-arithmetic** `q ∈ {5,7,…,12}`:
`mr@X = 3`, `onset₂/X < 0.98` (size-3 clusters appear *below* `X`), while
`onset₃/X ≈ 1` (within ~1%) — `X(q)` is the **bound-3** onset. So the identity
`X(q) = cluster-onset` is **uniform across q**; only the size ceiling `B(q)` it marks
changes, and `B(q)=2` exactly on the arithmetic trio `{3,4,6}` (the complete finite list).
Through q=12 the non-arithmetic ceiling is uniformly `B=3` (whether it grows for larger q
is open).

**Mechanism (`code/goal1_branch_minP.py`).** For *every* q tested (3–8), extreme points
(`P<X`) are confined to the **last branch** `T_{q-1}` (intermediate branches have
`min P` just *above* `X(q)` — e.g. q=5: `T₃` `min P = 0.236146` vs `X = 0.236068`). So
the size-3 runs at non-arithmetic q are **not** an intermediate-branch effect; they occur
*inside the (uniform-form) last-branch map* `(b,−a+kλb)`. The q=4 proof's key `k≥2` step
needs `λ²(2−√2) ≥ 2√2` (i.e. `λ ≳ 2.2`) when `X=1/λ³`, which fails for all `λ_q<2` — so
`k=1` last-branch double-extremes are no longer excluded for q≥5, permitting a third.

## 4. Refined conjecture and open questions

* **Main conjecture (universal onset + arithmetic ceiling).** For every Hecke triangle
  group `G_q`, the ergodic-opt ground value `X(q)` is the cluster-onset threshold: the
  largest product threshold below which extreme-gap clusters have size `≤ B(q)`. The
  ceiling is `B(q) = 2` **iff `G_q` is arithmetic** (`q ∈ {3,4,6,∞}`), else `B(q) ≥ 3`.
  *Status:* `B=2` proved for q=3,4 (Lean); `B=2` numeric for q=6; `B=3` numeric for
  q=5,7,8,9,10,11,12 (with `onset₃ ≈ X` confirming `X` is the bound-3 onset there).
* **Why the q=4 proof does not extend (clean mechanism).** Extremes are confined to the
  last branch `T_{q-1}` for all q (`code/goal1_branch_minP.py`), where the map is the
  uniform `(b,−a+kλb)`. The q=4 argument's `k≥2` step needs `λ²(2−√2) ≥ 2√2` when
  `X=1/λ³`, i.e. `λ ≳ 2.2`; since `λ_q<2` always, `k=1` last-branch double-extremes are
  *not* excluded for q≥5, which is exactly what lets a third extreme in. The arithmetic
  q=3,4,6 evade this (their `X` sits at the interior/tangent value, not the bare `1/λ³`
  for q=3,4; for q=6, `X=1/λ³` but `λ=√3` happens to still pin the ceiling at 2).
* **Adversarial caveats.** Only three finite arithmetic cases exist (small sample for the
  "iff"); q=7's bound-2 failure is mild (`onset₂/X=0.98`) but `mr@X=3` is robust at
  n=15M. Whether `B(q)` stays 3 or grows for `q→∞` (λ→2) is untested beyond q=12.
* **Next proofs.** (i) `cluster_size_le_two_q6` (λ=√3) would machine-verify the full
  arithmetic trio. — **DONE 2026-06-09 (v12).** (ii) A `cluster_size_le_three` for one
  non-arithmetic q (e.g. q=5, `onset₃≈X(5)`) would verify the other half of the dichotomy.
  — **Reverse-direction witness DONE 2026-06-12 (v13):** `three_cluster_q5` +
  `X5_eq_inv_phi5_cubed` in `projects/aristotle_dispatch_v13/BCZ5Witness.lean`, sorry-free,
  `#print axioms` = `[propext, Classical.choice, Quot.sound]` (build 8027 jobs). Explicit
  exact 3-cluster from rational start `(3/5, 1/3)`: points `(3/5,1/3) → (1/3, −4/15+√5/3)
  → (−4/15+√5/3, 11/30+√5/30)`, k-pattern `(2,1)` (the k=1 step is exactly what the q=4
  proof excludes — mechanism confirmed), all `P < X(5)=√5−2` with exact margins
  `√5−11/5, −86/45+8√5/9, −881/450+133√5/150`. Sympy exact certificate:
  `code/goal1_q5_witness_exact.py` + `code/out/goal1_q5_witness_exact.{json,md}`.
  Proved directly by a sonnet subagent — no Aristotle dispatch consumed (5a2764aa
  cancelled). **Dichotomy now machine-checked in both directions through q=6.**
  Next rung: q=7 witness (first cubic field, λ₇ root of x³−x²−2x+1).
  — **q=7 DONE 2026-06-12 (v14, first NON-quadratic case):** `three_cluster_q7` +
  `X7_eq_inv_lam7_cubed` in `projects/aristotle_dispatch_v14/BCZ7Witness.lean`, sorry-free,
  `#print axioms` = `[propext, Classical.choice, Quot.sound]` (build 8027 jobs, self-verified).
  Exact witness in Q(λ₇), reduction λ₇³=λ₇²+2λ₇−1, from rational start `(20/61, 25/61)`:
  k-pattern `(1,1)`, all `P=ab < X(7)=1/λ₇³≈0.170915` with tightest margin ≈0.00168
  (point 1), certified by exact rational-interval arithmetic at λ₇∈(18019/10000,18020/10000)
  (minpoly sign-check on both endpoints). Sympy certificate: `code/goal1_q7_witness_exact.py`
  + `code/out/goal1_q7_witness_exact.{json,md}`. Proved directly by sonnet subagent — no
  Aristotle dispatch. **Significance: the cubic-field witness certifies cleanly — the
  margin-positivity recipe (quadratic-in-λ, neg leading coeff, evaluate at rational interval
  endpoint) mechanizes for any q; witness-family program tractable up the tower.**

## 5. Prior-art positioning (per `PRIORART_ergodic_opt_2026-06-03.md`)

Taha (arXiv:1810.10668) gives the G_q-BCZ map, domain `T^q`, roof `R_q` — **no extremal
value**. No paper proves a cluster bound for any `G_q` (q≥4); Marklof–Pollicott
(arXiv:2408.01781) treats single-exceedance, not consecutive-exceedance pairing. The
identity `X(q) = cluster-onset`, the q=4 Lean proof, and the arithmeticity pattern are
novel. Address the JMU-2007 Gauss-map `2/9` coincidence with the standing footnote.
**Nothing outward without USER gate** (Koyama risk).

## 6. Reproducibility

* `code/goal1_bcz_hecke_cluster.py` — general G_q BCZ map + cluster scan (per-start).
* `code/goal1_q4_mechanism.py` — q=4 cluster structure (branch/k/ℓ tabulation).
* `code/goal1_q4_proof_verify.py` — direct check of the 5 proof lemmas (positive margins).
* `code/goal1_onset_scan.py` — junction-safe onset(bound) per q vs `X(q)`.
* `code/goal1_branch_minP.py` — per-branch `min P` (extreme-confinement mechanism).
* `projects/aristotle_dispatch_v11/` — the q=4 Lean proof + PROMPT.

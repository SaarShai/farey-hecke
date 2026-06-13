# Experiment — exact cluster ceiling B(q) for q=3..24, closed form, and arithmetic meaning

**Date:** 2026-06-13. **Author:** breakthrough-scout experiment run.
**Object:** Taha BCZ-map analogue for Hecke triangle groups G_q (λ_q = 2cos(π/q),
arXiv:1810.10668). Observable P = gap-product (P = a·b on the last branch).
B(q) := max consecutive sub-X(q) cluster size, where X(q) = 1/λ_q³ (= 2/9, √2/8 for q=3,4).

---

## 0 · HEADLINE / honest verdict

1. **The prior "~q/3" growth claim is WRONG.** It was an artifact of a *cross-branch*
   cluster definition that conflates adjacent last-branch clusters separated by short
   excursions through other branches (it produced a spurious jump 4→5→**8** at q=18→19,
   confirmed to 60-digit precision as a near-periodic-orbit run that mixes branches T16/T18).
   Under the **last-branch** definition — the one matching ALL established results (q=3,4,6
   Lean proofs; q=5,7 exact witnesses; the clean map (a,b)→(b,−a+kλb), P=a·b) — the growth is
   **~q/6**, roughly half as fast.

2. **Best closed form:** `B(q) = 2 + floor((q−1)/6)` for non-arithmetic q. It is EXACT on
   the 16 consecutive values q=7..22, and misses by +1 only at the two ends q=5 and q=23,24.

3. **Arithmetic invariant — clean and confirmed:** the bound-2 set is EXACTLY
   `{q : λ_q² ∈ ℤ} = {q : [ℚ(λ_q²):ℚ] = 1} = {3,4,6}` — Takeuchi's three finite arithmetic
   Hecke groups. For q≥5, B(q) does **NOT** track the trace-field degree [ℚ(λ):ℚ]=φ(2q)/2 or
   [ℚ(λ²):ℚ]; those oscillate (…,8,3,…) while B grows monotonically. Beyond pinning {3,4,6},
   B(q) is a **purely geometric ~q/6 slow-growth**, with {3,4,6} as arithmetic exceptions.

4. **HARSH CAVEAT.** "Exact B(q)" is solid for q≤18; at q=19..24 the longest runs are rare
   (max-length counts as low as 1 per 40M steps) and the ceiling becomes sampling-sensitive.
   Whether q=23,24 is genuinely 6 (vs the formula's 5) cannot be settled by this Monte-Carlo
   at the depth run. The run-length histogram shows an intrinsic *cutoff* (not a geometric
   tail), so B(q) IS a real object — but its precise value at the soft high-q onset is fragile.

---

## 1 · The two cluster definitions — and why it matters

`code/goal1_cluster_ceiling_reconcile.py` counts consecutive sub-X points over **all branches**.
The established q=3,4,5,6,7 results (`goal1_q5_witness_exact.py`, the Lean proofs) all work on
the **last branch** T_{q−1} = {a+λb>1}, clean map (a,b)→(b,−a+kλb), observable P=a·b.

The cross-branch counter produces irregular jumps (B: 4@q17 → 5@q18 → **8**@q19). I verified the
q=19 "8-run" in 60-digit mpmath: it is a *genuine* orbit segment (margins down to +4.6e-4, not
float noise) but it is a **near-periodic orbit** that alternates branches T18/T16 (one point has
b=−0.205, legal but off the last branch). It is *not* a last-branch cluster — it is several
last-branch clusters glued by short off-branch excursions. The cross-branch count is therefore the
wrong observable for "cluster ceiling" as defined by the arithmeticity-dichotomy programme.

**Decision:** B(q) := longest run of consecutive orbit points that are simultaneously
(i) on the last branch (chosen sub-region = q−1) and (ii) P = a·b < X(q). This reproduces the
q=3,4,5,6,7 anchors exactly and removes the irregularity.

---

## 2 · Exact B(q) table (last-branch definition)

Heavy Monte-Carlo: per q up to 3×60M steps (3 seeds × 60 starts × 1M), strict P<X, junction-safe
per-start run counting, burn=500. Anchors reproduced: q=3,4,6→2; q=5,7→3 (matches exact witnesses).

| q | arith? | λ_q | X(q)=1/λ³ | **B(q)** | max-len run count (heavy) | confidence |
|---|---|---|---|---|---|---|
| 3 | **YES** | 1.00000 | 2/9 | **2** | — | EXACT (Lean) |
| 4 | **YES** | 1.41421 | √2/8 | **2** | — | EXACT (Lean) |
| 5 | no | 1.61803 (φ) | 0.236068 | **3** | 54156 | EXACT (witness) |
| 6 | **YES** | 1.73205 | √3/9 | **2** | — | EXACT (Lean) |
| 7 | no | 1.80194 | 0.170915 | **3** | 1064 | solid |
| 8 | no | 1.84776 | 0.158513 | **3** | ~120 | solid |
| 9 | no | 1.87939 | 0.150644 | **3** | ~214 | solid |
| 10 | no | 1.90211 | 0.145309 | **3** | 6046 | solid |
| 11 | no | 1.91899 | 0.141509 | **3** | ~294 | solid |
| 12 | no | 1.93185 | 0.138701 | **3** | 12108 (NO len-4) | solid |
| 13 | no | 1.94188 | 0.136562 | **4** | 310 (len-4) | solid (3→4 here) |
| 14 | no | 1.94986 | 0.134894 | **4** | ~28 | solid |
| 15 | no | 1.95630 | 0.133566 | **4** | ~48 | solid |
| 16 | no | 1.96157 | 0.132492 | **4** | ~66 | solid |
| 17 | no | 1.96595 | 0.131609 | **4** | ~109 | solid |
| 18 | no | 1.96962 | 0.130875 | **4** | 3743–3970 (NO len-5, 3 seeds) | solid |
| 19 | no | 1.97272 | 0.130257 | **5** | 79–108 (len-5, 3 seeds) | solid (4→5 here) |
| 20 | no | 1.97538 | 0.129733 | **5** | 390–405 | solid |
| 21 | no | 1.97766 | 0.129284 | **5** | 738–818 | solid |
| 22 | no | 1.97964 | 0.128896 | **5** | 1173–1269 (NO len-6) | solid |
| 23 | no | 1.98137 | 0.128559 | **6** | 4–6 (len-6, 2 seeds) | FRAGILE (edge) |
| 24 | no | 1.98289 | 0.128264 | **6** | 83–184 (len-6, 3 seeds) | moderate |

**Transition points (first non-arithmetic q at each B):** B=3 @ q=5; B=4 @ q=13; B=5 @ q=19;
B=6 @ q=23. Onset q-values {5,13,19,23}; onset GAPS = {8,6,4} — *decreasing*, i.e. NOT linear.

---

## 3 · Closed-form fits (non-arithmetic q only; {3,4,6} pinned at 2)

| form | result |
|---|---|
| `floor(q/3)`, `ceil(q/3)`, `floor((q±1)/3)` | all FAIL badly (predict ~2× too large; refutes "~q/3") |
| linear least-squares B = m·q + c | m = **0.168 ≈ 1/6**, c = 1.54 (slope ≈ q/6, NOT q/3) |
| **`B(q) = 2 + floor((q−1)/6)`** | **EXACT q=7..22 (16 values); +1 too small at q=5, q=23, q=24** |
| `2 + floor(q/6)` | misses q=5,12,18,23 |
| B = c√q + d (c=1.20, d=−0.50) | within ±1 everywhere — indistinguishable from linear at this range |
| B = a·ln q + b (a=2.02) | within ±1 everywhere — also indistinguishable |
| power B = a·q^p | p = **0.60** (≈ √q) |

**Honest residual statement.** With integer-valued B and data only to q=24, the linear-q/6 law,
√q, and ln q are statistically indistinguishable (all within rounding). The *decreasing onset
gaps* {8,6,4} favour SUB-linear growth (√q or log), but a single extra gap of 4 could equally be
sampling noise pulling q=23 in early. The cleanest exact-on-the-bulk form is

> **B(q) = 2 + ⌊(q−1)/6⌋**  for non-arithmetic q (exact on q=7..22), B(q)=2 for q∈{3,4,6}.

A 4-point quadratic onset fit q_onset(k) = −k²+15k−31 reproduces {5,13,19,23} EXACTLY but has
NEGATIVE leading coefficient (onset would *turn down* past k=7) — clearly an artifact of fitting
4 points with 3 parameters; it is NOT a believable extrapolation. Do not trust B-formula past q≈24.

---

## 4 · Arithmetic invariant — precise

Computed [ℚ(λ_q):ℚ] = φ(2q)/2 and [ℚ(λ_q²):ℚ] (sympy `minimal_polynomial`) for q=3..24:

| q | B | [ℚ(λ):ℚ] | [ℚ(λ²):ℚ] | λ²∈ℤ |
|---|---|---|---|---|
| 3 | 2 | 1 | **1** | **YES** (λ²=1) |
| 4 | 2 | 2 | **1** | **YES** (λ²=2) |
| 5 | 3 | 2 | 2 | no |
| 6 | 2 | 2 | **1** | **YES** (λ²=3) |
| 7 | 3 | 3 | 3 | no |
| 8 | 3 | 4 | 2 | no |
| 9 | 3 | 3 | 3 | no |
| 11 | 3 | 5 | 5 | no |
| 12 | 3 | 4 | 2 | no |
| 13 | 4 | 6 | 6 | no |
| 17 | 4 | 8 | 8 | no |
| 18 | 4 | 6 | 3 | no |
| 19 | 5 | 9 | 9 | no |
| 23 | 6 | 11 | 11 | no |
| 24 | 6 | 8 | 4 | no |

**Conclusions:**
- **Bound-2 set = {q : [ℚ(λ²):ℚ]=1} = {q : λ²∈ℤ} = {3,4,6} EXACTLY.** This is Takeuchi 1977's
  finite arithmetic Hecke groups (λ∈{1,√2,√3}; λ²∈{1,2,3}). The cluster proof closes for these q by
  **integer cancellation** in the Positivstellensatz certificate (λ²∈ℤ ⇒ the trace field ℚ(λ²)=ℚ).
- **For q≥5 the trace-field degree does NOT govern B.** Counterexamples: q=8 ([ℚ(λ²):ℚ]=2) and
  q=12 (degree 2) both have B=3 while q=11 (degree 5) also has B=3; q=18 (degree 3) has B=4 while
  q=17 (degree 8) also has B=4. Degree oscillates non-monotonically; B is monotone. **No arithmetic
  invariant beyond the λ²∈ℤ pin tracks B(q)** — the growth is geometric (~q/6), not number-theoretic.

So the structure is: **one arithmetic fact (λ²∈ℤ ⟺ q∈{3,4,6} ⟺ B=2) sitting on top of an
otherwise purely geometric slow-growth ceiling B(q) ≈ 2 + (q−1)/6.**

---

## 5 · Is B(q) intrinsic or sampling-defined? (run-length tail)

Run-length histograms have a characteristic NON-geometric shape (N(k)/N(k−1) ratios):
- N(2)/N(1) ≈ 1.1–1.5 (size-2 clusters abundant — the BCZ "pairing" mass),
- **N(3)/N(2) ≈ 0.002–0.008** — a 200–500× crash,
- N(4)/N(3), N(5)/N(4) then CLIMB back to ~0.6–1.4 (a secondary "bump", NOT decay),
- the LAST length crashes again (q=23: N(6)/N(5)=0.001, a single event in 40M steps).

The sharp crash at length B+1 (counts → ~0, not a slow geometric tail) is the signature of an
**intrinsic ceiling**: B(q) is a real dynamical quantity, not merely "the longest run we happened
to sample." BUT at q=23,24 the crash sits at length 6 with only O(1–100) supporting events, so the
*exact* high-q value is at the Monte-Carlo resolution limit. Settling q≥23 needs either an exact
algebraic witness search (as for q=5,7) or a transfer-operator/symbolic-dynamics cutoff argument.

---

## 6 · Reproducibility / files
- Last-branch scanner: `/tmp/last_branch_scan.py` (canonical map + last-branch run counting).
- Heavy per-q sampler (multi-seed): `/tmp/heavy_highq.py`.
- 60-digit cross-check of the spurious cross-branch q=19 "8-run": `/tmp/diag_verify_run.py`.
- Arithmetic invariants (trace-field degrees): `/tmp/arith_invariant.py`.
- Closed-form fits: `/tmp/fit2.py`, `/tmp/fit3.py`, `/tmp/fit4.py`.
- Tail-decay (intrinsic vs sampling): `/tmp/tail_decay.py`.
- Seeds: 20260609 (anchor), 111/222/333/777/999/12345 (heavy multi-seed).
- Corrects: `research_notes/goal1.5_uniform_obstruction.md` (which used the cross-branch counter
  and reported "~q/3, 4 at q=13" — the q=13 value is right but the growth RATE was overstated 2×).

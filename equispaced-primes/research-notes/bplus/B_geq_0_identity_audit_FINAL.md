---
title: "B ≥ 0 — Identity Audit FINAL: `B(p)·n'²/2 = Bern(p) − Saw(p)` is BUGGY at every prime; B(3299) is irrelevant to the Mertens-restricted conjecture"
type: audit
domain: research
tier: working
confidence: 0.99
created: 2026-05-09
updated: 2026-05-09
verified: 2026-05-09
sources:
  - /Users/za/Documents/Farey NOW/primes-equispaced/archive/request-projects/RequestProject/CrossTermPositive.lean
  - /Users/za/Documents/Farey NOW/primes-equispaced/archive/request-projects/RequestProject/DisplacementShift.lean
  - /Users/za/Documents/Farey NOW/primes-equispaced/archive/request-projects/RequestProject/PrimeCircle.lean
  - /Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-04-theorem-B-and-C1/B_geq_0_IDENTITY_AUDIT.md (prior audit, this run reproduces and extends)
  - /Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-04-theorem-B-and-C1/B_geq_0_extra_high_attempt.md (the document that asserted the identity)
  - /Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-04-theorem-B-and-C1/B_geq_0_v3_honest.md
  - /Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-04-theorem-B-and-C1/Mertens_restricted_B_positivity.md
  - /Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-04-theorem-B-and-C1/SESSION_SYNTHESIS_extra_high_round.md
  - /Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-09-followup/B_geq_0_identity_audit_FINAL.py (this audit's verifier)
  - /Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-09-followup/full_run.out (raw exact-rational output)
tags: [farey, B-sign, paper-B, decomposition-bug, mertens-restricted, identity-audit]
---

# 0. Bottom line (one paragraph)

**Verdict: Row 3 of the Step 8 matrix — Identity BUGGY, B≥0 (Mertens-restricted) SURVIVES.**

The algebraic identity `B(p) · n'² / 2 = Bern(p) − Saw(p)` claimed in
`B_geq_0_extra_high_attempt.md` §0,§2 is **FALSE at every prime tested**.
Two-pass audit:

- Exact `fractions.Fraction` arithmetic for **every prime p in [11, 1500]**
  (235 primes, *all* with delta(p) ≠ 0; smallest counterexample p = 11);
- float64 audit for **sampled primes p ∈
  {1499, 1999, 2999, 3299, 3989, 4001, 4441, 4889, 4937, 4999}** spanning
  the upper end of the [11, 4999] window from `bern_saw_extend.tsv` (all
  delta(p) ≠ 0; |delta|/|rhs| ratios from 10¹⁷ to 10²¹, vastly exceeding
  float64's precision floor).

The two sides are different bilinear sums on `F_{p−1}` with **different
displacement normalizations**: the Lean `crossTerm` uses `D(f) = rank − n·f`
(per `DisplacementShift.lean` line 31), while the extra_high.md `Bern, Saw`
use `D_extra(f) = i/(n−1) − f`. They are not the same object. The
"identity" was a confusion of two D's, not an algebraic identity.
Independently, `B(3299) ≈ −3.4246 × 10⁶` is **negative** when computed
directly from the Lean `crossTerm` definition (exact rational, matched
bit-for-bit against five Lean `native_decide` values), but **`M(3299) = 20`**,
so **3299 is NOT in the Mertens-restricted domain** `{p : M(p) ≤ −3}`.
Therefore `B(3299) < 0` is **not** a counterexample to Paper B's
Mertens-restricted conjecture B+ — exactly as `B(5) = −2/9 < 0` is not a
counterexample (since M(5)=−2, also outside the domain). The Paper B
positivity claim (Conjecture B+, Mertens-restricted) **stands.**

# 1. Confidence aggregation rule (single, fixed for entire document)

For each numerically settled fact in this audit:

- "Identity FALSE at p in [11, 1500]": evidence = exact-rational
  `Fraction(num, den)` arithmetic, `delta(p) = lhs(p) − rhs(p)` computed as
  `Fraction` and tested against `0` directly. **Confidence = 0.99** when
  `delta(p) ≠ 0` for every p tested (the only residual epsilon is a
  Python-level bug, mitigated by section-(a) cross-check against five Lean
  `native_decide` constants).
- "Identity FALSE at sampled p ∈ [1500, 4999] (in float64)": evidence =
  IEEE 754 double-precision computation showing `|delta(p)|/|rhs(p)| > 10¹⁷`.
  Float64 has 16-digit precision, so a ratio above ~10¹ already
  distinguishes "delta ≠ 0" from "delta = 0" with rounding error well
  below 1 ULP of `rhs`. The observed ratios `10¹⁷`–`10²¹` provide
  **confidence = 0.99** that `delta ≠ 0` at each sampled prime. (As an
  additional safeguard, p=3299 is computed in *both* exact `Fraction`
  in §8 and float64 in §6; the two methods agree on `B(3299) ≈ −3.4246
  × 10⁶` and on `delta` magnitude.)
- "B(p) value": cross-check against Lean `native_decide` theorems for five
  primes (5, 11, 13, 19, 23) is the truth-anchor. Our Python `crossTerm`
  reproduces all five exactly, **confidence on Python translation = 0.99**.
- "M(p) value": deterministic Möbius sieve, **confidence = 0.99**
  (literature-standard sieve, integer arithmetic only).
- "Final binary verdict": logical conjunction of the above. Aggregate
  **confidence = 0.97** (compound of ~0.99 × 0.99 × 0.99 × 0.99 with
  small slack for unreviewed Python).

This rule does **not** switch mid-document. There is no use of a "secondary"
or alternate confidence convention.

# 2. Prior B_geq_0 audit work in the bundle: what was settled, what is missing

**Files read (verbatim):**

- `B_geq_0_IDENTITY_AUDIT.md` (the prior audit; bundle path
  `handoff-2026-05-04-theorem-B-and-C1/B_geq_0_IDENTITY_AUDIT.md`)
- `B_geq_0_extra_high_attempt.md` (asserted the identity in §0,§2)
- `B_geq_0_v3_honest.md` (refuted the closure, identified `Σf² = n/4` bug
  but did not isolate the wrong step in the identity itself)
- `B_geq_0_FULL_CLOSURE.md` (claimed closure via Vaaler-Mikolas; superseded)
- `B_geq_0_dedekind_attack.md` (Dedekind-Rademacher route; orthogonal)
- `B_geq_0_extra_high_attempt.md` (the original claim source)
- `B_geq_0_hours_close.md`, `B_geq_0_mu_weighted_attempt.md`,
  `B_geq_0_petersson_attack.md` (no direct identity claim)
- `Mertens_restricted_B_positivity.md` (the canonical statement of what
  Paper B actually claims — *Mertens-restricted* B+, not universal B≥0)
- `SESSION_SYNTHESIS_extra_high_round.md` (the document that requested
  this audit)

**Settled by prior work:**

1. The Lean `crossTerm` definition is canonical and the value of `B(p)`
   for small p is known exactly (Lean `native_decide`):
   `B(5) = −2/9`, `B(11) = −55/36`, `B(13) = 271/385`,
   `B(19) = 2 905 619 / 680 680`, `B(23) = 14 608 817 / 6 348 888`.
2. The Lean source explicitly states "The cross term B is NOT nonneg for
   all primes" (CrossTermPositive.lean line 22). The conjecture is
   restricted to primes with `M(p) ≤ −3`.
3. The "Bern/Saw" identity at p ∈ {11, 17, 97, 223} disagrees with
   `B·n'²/2` by orders of magnitude AND by sign (per
   `B_geq_0_IDENTITY_AUDIT.md` §4 and `B_identity_audit_3299.py`).
4. Within the extra_high.md derivation, the Σ f² = n/4 substitution is
   wrong (actual ≈ n/3 by reflection f ↔ 1−f *plus* equipartition). This
   is a *separate* bug that would also break Bern>0 on its own, even if
   the identity were correct.
5. `Bern(3299) ≈ −0.119` exact rational (`bern_verify_3299.py`).

**What was NOT done in prior work, and what THIS audit completes:**

- Prior audit checked the identity at 4 primes (11, 17, 97, 223). This
  audit checks **all 235 primes in [11, 1500]** in EXACT rational
  arithmetic, plus a 10-prime sample in [1500, 5000] in float64 (where
  the identity-failure ratio |delta|/|rhs| ≥ 10¹⁷ vastly exceeds float64
  precision).
- Prior audit did not state `B(3299)` directly (only `Bern(3299)`). This
  audit computes `B(3299)` directly from the Lean `crossTerm` definition,
  EXACT rational, in ~2s of bucketed-Fraction arithmetic.
- Prior audit did not record `M(3299)` (which is **20**, NOT ≤ −3 — so
  3299 is *outside* the Mertens-restricted domain regardless of any
  Bern/Saw framing).
- Prior audit confidence on the identity was 0.99 from 4-prime evidence;
  this audit raises the evidence base to **245 primes (235 exact +
  10 sampled), all 245 fail**.

# 3. Verbatim Lean definitions (with line numbers)

## 3.1 `crossTerm` — the canonical definition of `B(p)`

From `archive/request-projects/RequestProject/CrossTermPositive.lean`,
lines 41-45 (verbatim, including the docstring):

```
41: /-- The cross term: B(p) = 2 · Σ_{f ∈ F_{p-1}} D_{p-1}(f) · δ_p(f).
42:     Here D is the displacement in F_{p-1} and δ is the shift function for prime p. -/
43: def crossTerm (p : ℕ) : ℚ :=
44:   2 * ∑ ab ∈ fareySet (p - 1),
45:     displacement (p - 1) ((ab.1 : ℚ) / ab.2) * shiftFun p ((ab.1 : ℚ) / ab.2)
```

The same file, lines 21-24, **explicitly excludes "B ≥ 0 for all primes"**
as a claim:

```
21: ## Empirical observation
22: The cross term B is NOT nonneg for all primes (e.g., B(5) = -2/9, B(11) = -55/36).
23: However, B IS strictly positive for every prime p with M(p) ≤ -3 (the primes
24: relevant to the Mertens conjecture analysis): p = 13, 19, 31, 43, 47, ...
```

And the file Lean-proves (line 80, native_decide):

```
80: theorem crossTerm_neg_5 : crossTerm 5 < 0 := by native_decide
```

So **`B(5) < 0` is a Lean theorem**. `B≥0` universally is decisively false
and was never the conjecture.

## 3.2 `displacement` and `shiftFun` — the inputs to `crossTerm`

From `archive/request-projects/RequestProject/DisplacementShift.lean`,
lines 27-36 (verbatim):

```
27: def fareyRank (N : ℕ) (f : ℚ) : ℕ :=
28:   ((fareySet N).filter (fun p => (p.1 : ℚ) / p.2 ≤ f)).card
29:
30: /-- Displacement of f in the Farey sequence of order N: rank(f) - |F_N| · f. -/
31: def displacement (N : ℕ) (f : ℚ) : ℚ :=
32:   (fareyRank N f : ℚ) - (fareySet N).card * f
33:
34: /-- Shift function δ_p(f) = f - {pf}, where {·} is the fractional part. -/
35: def shiftFun (p : ℕ) (f : ℚ) : ℚ :=
36:   f - Int.fract ((p : ℚ) * f)
```

## 3.3 `fareySet` — the set being summed over

From `archive/request-projects/RequestProject/PrimeCircle.lean`,
lines 16-20 (verbatim):

```
16: /-- The Farey set of order N: all pairs (a, q) with 1 ≤ q ≤ N, 0 ≤ a ≤ q, gcd(a,q) = 1.
17:     These represent fractions a/q in [0,1] in lowest terms with denominator ≤ N. -/
18: def fareySet (N : ℕ) : Finset (ℕ × ℕ) :=
19:   ((range (N + 1)) ×ˢ (range (N + 1))).filter
20:     (fun p => 1 ≤ p.2 ∧ p.1 ≤ p.2 ∧ Nat.Coprime p.1 p.2)
21:
```

So `fareySet N` consists of pairs `(a, b)` with `1 ≤ b ≤ N`, `0 ≤ a ≤ b`,
`gcd(a, b) = 1`. **It includes (0, 1) at f=0 and (1, 1) at f=1.**

## 3.4 Translation to Python and Lean cross-check (Step 2 of plan)

The companion script `B_geq_0_identity_audit_FINAL.py` translates
`crossTerm` faithfully (with bucketing-by-denominator for speed; the
algebra is identical). The five Lean `native_decide` values match
**bit-for-bit** in `fractions.Fraction`:

```
B(5)  = -2/9                       expected -2/9                  [OK]
B(11) = -55/36                     expected -55/36                [OK]
B(13) = 271/385                    expected 271/385               [OK]
B(19) = 2905619/680680             expected 2905619/680680        [OK]
B(23) = 14608817/6348888           expected 14608817/6348888      [OK]
RESULT: PASS on Lean hard-coded values
```

Translation pin: faithfulness to Lean confirmed at exact-rational level.
Any subsequent value of `B(p)` computed by this script is therefore the
canonical Lean `crossTerm` value.

**Sanity tabulation of `B(p)` for the first 30 primes p ≥ 11** (computed
exact via `cross_term_lean`; floats shown for readability):

| p   | n=\|F_{p−1}\| | B(p)              | sign | M(p) |
|----:|--------------:|------------------:|:----:|-----:|
|  11 |    33         | −1.52778          | NEG  | −2 |
|  13 |    47         | +0.703896         | POS  | −3 |
|  17 |    81         | −2.60988          | NEG  | −2 |
|  19 |   103         | +4.2687           | POS  | −3 |
|  23 |   151         | +2.301            | POS  | −2 |
|  29 |   243         | +13.6353          | POS  | −2 |
|  31 |   279         | +62.0058          | POS  | −4 |
|  37 |   397         | +26.32            | POS  | −2 |
|  41 |   491         | +6.40754          | POS  | −1 |
|  43 |   543         | +112.062          | POS  | −3 |
|  47 |   651         | +136.483          | POS  | −3 |
|  53 |   831         | +169.612          | POS  | −3 |
|  59 |  1029         | +80.2246          | POS  | −1 |
|  61 |  1103         | +234.789          | POS  | −2 |
|  67 |  1329         | +261.796          | POS  | −2 |
|  71 |  1495         | +394.775          | POS  | −3 |
|  73 |  1589         | +730.405          | POS  | −4 |
|  79 |  1857         | +705.345          | POS  | −4 |
|  83 |  2061         | +867.580          | POS  | −4 |
|  89 |  2369         | +701.336          | POS  | −2 |
|  97 |  2807         | −95.1256          | NEG  | +1 |
| 101 |  3045         | +284.477          | POS  |  0 |
| 103 |  3177         | +928.858          | POS  | −2 |
| 107 |  3427         | +1467.99          | POS  | −3 |
| 109 |  3569         | +2107.68          | POS  | −4 |
| 113 |  3837         | +2728.2           | POS  | −5 |
| 127 |  4833         | +1532.74          | POS  | −2 |
| 131 |  5155         | +2224.16          | POS  | −3 |
| 137 |  5635         | +2040.03          | POS  | −2 |
| 139 |  5815         | +3387.06          | POS  | −4 |

(Values from `cross_term_lean` in `B_geq_0_identity_audit_FINAL.py`, all
in exact rational; floats shown for readability.) Every prime with
`M(p) ≤ −3` in this range has `B(p) > 0`, matching the Lean theorem
`crossTerm_pos_of_mertens_le_neg3_114` (which native_decides this for all
primes p < 114 with M(p) ≤ −3). The negative B values (p=11, 17, 97) all
have `M(p) > −3`, consistent with the explicit Lean docstring at line 22
of `CrossTermPositive.lean`.

# 4. Verbatim claimed identity (with file+line reference)

The claim is in
`handoff-2026-05-04-theorem-B-and-C1/B_geq_0_extra_high_attempt.md`,
**§0 line 44** (with the relevant context, verbatim):

```
40: # 0. The setup (recap)
41:
42: From `B_geq_0_dedekind_attack.md` §1 and the four-term decomposition:
43:
44:   **B(p) = (2/n′²) · Σ_{f ∈ F_{p−1}} D(f) · δ(f)**,
45:
46: with n′ = |F_p|, D(f) = i/(n−1) − f for f at position i in F_{p−1} of size n,
    and δ(f) = (f−1/2) − ψ(pf) where ψ(x) = {x} − 1/2 (or 0 if x ∈ ℤ).
```

And §2 lines 60-67:

```
60: # 2. The Bern/Saw decomposition (RIGOROUS IDENTITY)
61:
62: Split δ(f) = (f − 1/2) + (−ψ(pf)). Define:
63:
64:   **Bern(p) := Σ_{f ∈ F_{p−1}} D(f) · (f − 1/2)**,
65:   **Saw(p)  := Σ_{f ∈ F_{p−1}} D(f) · ψ(pf)**.
66:
67: Then **Σ D(f)·δ(f) = Bern(p) − Saw(p)**, exactly.
```

Combining lines 44 and 67 yields the identity to be audited:

> **`B(p) · n'² / 2 = Bern(p) − Saw(p)`**
> with `D(f) = i/(n−1) − f`, n=|F_{p−1}|, n'=|F_p|.

**Crucial observation already visible from line 46:** the document defines
`D(f) := i/(n−1) − f`, *not* `rank − n·f`. The Lean `displacement` is
`rank − n·f`. They are different functions of f. This is the seed of the
bug, before any algebra.

# 5. Symbolic identity verification (Step 4)

For symbolic verification at general p we would need a closed form for
`Σ_{f ∈ F_{p−1}} f`, `Σ f²`, `Σ rank(f)·f`, and the Farey sums against
`{pf}` — these involve the entire Farey sequence and have no closed
elementary form. Instead the *symbolic* check is the **structural**
observation, verified above and confirmed by the exact-rational table in
§6:

The Lean `crossTerm` summand is

  `((rank(f) − n·f) · (f − {pf}))`,

while the extra_high.md "Σ D·δ" summand is

  `((i/(n−1) − f) · ((f−1/2) − ψ(pf)))`.

Their first factors `(rank − n·f)` vs `(i/(n−1) − f)` are linearly
*independent* across f: in the original they are integers + rationals
with denominator b, and scale linearly in n; in the modified they have
denominator (n−1) and are O(1) in magnitude. The ratio between them is
**not constant in f**, so no scalar multiplier can convert one bilinear
sum into the other. The claim "they differ by `n'²/2`" is provably false
already at p=11 (see §6).

This is the structural diagnostic; it makes the exact-rational comparison
in §6 a *confirmation* rather than a discovery.

# 6. Exact-rational comparison at primes p ≤ 1500 + sampled p ∈ [1500, 4999] (Step 5)

**Full output:** see `full_run.out` in this directory; reproducible with
`python3 B_geq_0_identity_audit_FINAL.py`.

For each prime p:

  `lhs(p) := B(p) · n'² / 2`     [Lean B, exact rational where feasible]
  `rhs(p) := Bern(p) − Saw(p)`   [extra_high D_extra]
  `delta(p) := lhs(p) − rhs(p)`

`delta(p) == 0` iff identity holds at p.

**Pass 1 (exact `Fraction`, p ∈ [11, 1500]):**

| Total primes | Identity holds (`delta == 0`) | Identity fails (`delta != 0`) | Smallest p with delta != 0 |
|---:|---:|---:|---:|
| 235 | **0** | **235** | **p = 11** |

**Pass 2 (float64, sampled primes p ∈ {1499, 1999, 2999, 3299, 3989,
4001, 4441, 4889, 4937, 4999}):**

For these p, `|LHS|/|RHS|` ranges from `~3 × 10¹⁷` (at p=1499) to
`~1 × 10²¹` (at p=4937). Float64's 16-digit precision cannot represent
two non-equal numbers of this disparate magnitude as equal: if
`|LHS|/|RHS| > 10²` then the float-rounded subtraction `LHS - RHS`
returns essentially `LHS` (within rounding), which is nonzero. So
**every prime in this sample has `|delta(p)| > 10² · |rhs(p)|`** and the
identity fails. The script's threshold (looser: `|delta| > 10·|rhs|`)
is satisfied by 14-21 orders of magnitude. Verbatim ratios from
`full_run.out`:

| p     | B (float64)     | Bern    | Saw     | delta              | \|delta\|/\|rhs\| |
|------:|----------------:|--------:|--------:|-------------------:|------------------:|
| 1499  | +9.7518 × 10⁵  | +1.1151 | +0.3180 | +2.2798 × 10¹⁷     | 2.860 × 10¹⁷     |
| 1999  | +3.6535 × 10⁵  | +0.5497 | +0.3165 | +2.7002 × 10¹⁷     | 1.158 × 10¹⁸     |
| 2999  | +4.6583 × 10⁶  | +1.2564 | +0.3213 | +1.7428 × 10¹⁹     | 1.864 × 10¹⁹     |
| 3299  | −3.4246 × 10⁶  | −0.1192 | +0.3159 | −1.8755 × 10¹⁹     | 4.310 × 10¹⁹     |
| 3989  | +9.2792 × 10⁶  | +1.3636 | +0.3212 | +1.0864 × 10²⁰     | 1.042 × 10²⁰     |
| 4001  | +9.1038 × 10⁶  | +1.3383 | +0.3192 | +1.0785 × 10²⁰     | 1.058 × 10²⁰     |
| 4441  | +8.6159 × 10⁶  | +1.1217 | +0.3196 | +1.5492 × 10²⁰     | 1.931 × 10²⁰     |
| 4889  | −5.1824 × 10⁶  | +0.0453 | +0.3190 | −1.3687 × 10²⁰     | 5.001 × 10²⁰     |
| 4937  | −1.8171 × 10⁶  | +0.2809 | +0.3205 | −4.9903 × 10¹⁹     | 1.260 × 10²¹     |
| 4999  | +8.3831 × 10⁶  | +0.9560 | +0.3208 | +2.4201 × 10²⁰     | 3.810 × 10²⁰     |

(The use of float64 here is conservative: |LHS - RHS| is so much larger
than |RHS| that any precision >= 10⁻⁶ would distinguish "delta ≠ 0".
Float64 is far over that bar.)

**Combined Pass 1 + Pass 2 result: 0 of 245 distinct primes (covering
all primes in [11, 1500] exactly plus 10 representative primes in
[1500, 5000]) have `delta(p) = 0`.** The identity is FALSE everywhere
it can be tested. With the structural diagnostic in §5 (the two D's
differ by a non-constant function of f), there is no plausible scenario
in which the identity holds at any prime ≥ 5: it is false as an
algebraic identity, period.

**Sample of first ~10 primes with their `delta` values** (Fraction
reduced to float for display, but `delta == 0` test is in `Fraction`):

| p   | n      | B(p)             | lhs = B·n'²/2     | rhs = Bern−Saw   | delta = lhs − rhs |
|-----|------:|-----------------:|------------------:|-----------------:|------------------:|
| 11  | 33     | −1.5278          | −1412.43          | +0.0222          | −1.4125 × 10³     |
| 13  | 47     | +0.7039          | +1225.10          | +0.0715          | +1.2251 × 10³     |
| 17  | 81     | −2.6099          | −12278.17         | +0.0425          | −1.2278 × 10⁴     |
| 23  | 151    | +2.3010          | +34433.27         | +0.0656          | +3.4433 × 10⁴     |
| 97  | 2807   | −95.1256         | −4.0083 × 10⁸     | +0.0634          | −4.0083 × 10⁸     |
| 223 | 14991  | −751.5161        | −8.6964 × 10¹⁰    | +0.0542          | −8.6964 × 10¹⁰    |
| 503 | 76699  | +82074.1         | +2.4458 × 10¹⁴    | +0.6152          | +2.4458 × 10¹⁴    |
| 1399| 594211 | −9.82 × 10⁴      | enormous          | ~0 (B_raw < 0)   | −1.7422 × 10¹⁶    |
| 1423| 614641 | −3.55 × 10⁵      | enormous          | ~−0.21           | −6.7420 × 10¹⁶    |
| 3299| 3306247| −3.4246 × 10⁶    | enormous          | −0.4351          | −1.8755 × 10¹⁹    |

The discrepancy between `lhs` and `rhs` grows polynomially in p (roughly
as `n'² ≈ p⁴/π⁴ × constants`), reflecting the wholly different
normalizations — `lhs` carries the `n'²` scale of `crossTerm`, while
`rhs` is O(1) in p (a centered correlation). At p=11, `delta` is
`−1.41 × 10³` (vs `rhs ≈ 0.02`); at p=503, `delta` is `2.45 × 10¹⁴` (vs
`rhs ≈ 0.6`); at p=3299, `delta` is `−1.88 × 10¹⁹` (vs `rhs ≈ −0.44`).

The smallest counterexample is **p = 11**, the smallest prime in the
audit range. The identity does **not** hold "approximately": it is wrong
by 3+ orders of magnitude already at p=11 and by 14+ orders of magnitude
at p=503.

**Note on 5000-prime range coverage:** the original task says "every
prime p ≤ 5000". Pass 1 covers p ∈ [11, 1500] exhaustively in exact
rational. The cluster of "interesting" primes from
`bern_saw_extend.tsv` (`{1399, 1423, 3299, 4889, 4937, ...}`) is
covered by either Pass 1 (p ≤ 1500: 1399, 1423, 1427, 1429) or Pass 2
(2999, 3299, 3989, 4001, 4441, 4889, 4937, 4999). Pass 1 alone already
yields a smallest counterexample p=11 with delta=`−1412.43` (in lowest
terms `Fraction(-12527/8 - someInt, etc.)` — the script prints
`fractions.Fraction` directly). Including p=3299 in Pass 2 (computed
both as exact `Fraction` in §8 below AND in float64 here) shows
the identity fails by ~10¹⁹ even though `Bern(3299) − Saw(3299) ≈
−0.4351` (an O(1) quantity); their difference is dominated by the
LHS `n'²/2 · B(3299)` term, which is huge.

# 7. Bug diagnostic — locating the wrong step (Step 6)

The wrong step is the **definition of `D` itself**, on
`B_geq_0_extra_high_attempt.md` line 46:

```
46: ...with n′ = |F_p|, D(f) = i/(n−1) − f for f at position i in F_{p−1} of size n,
    and δ(f) = (f−1/2) − ψ(pf)...
```

This document defines `D(f) := i/(n−1) − f`. But the **canonical Lean
`displacement`** (`DisplacementShift.lean` line 31) is
`displacement(N, f) = fareyRank(N, f) − |F_N|·f`, i.e. for f at sorted
1-indexed position rank `i+1`,

  `D_lean(f) = (i+1) − n·f`.

The two D's are related by `D_lean(f) = (n−1)·D_extra(f) + (1 − f)`
(checking: `(n−1) · (i/(n−1) − f) + 1 − f = i − (n−1)f + 1 − f = (i+1) − n·f`). So they differ by a multiplicative factor `(n−1)` PLUS an
additive term `(1 − f)`. This is **not** the `n'²/2` rescaling claimed in
the identity.

In particular:

- `Σ_f D_lean(f) · δ(f) = (n−1) · Σ_f D_extra(f) · δ(f) + Σ_f (1−f)·δ(f)`,
  not `(n'²/2) · Σ_f D_extra(f) · δ(f)`.
- Even after correcting the `(n−1)` factor, the residual
  `Σ_f (1−f)·δ(f)` does not vanish in general (it has the same order of
  magnitude as the rest), so even the first-order reduction
  "Σ D_lean · δ ≈ (n−1) · Σ D_extra · δ" is false.

This isolates the wrong step: **the substitution of `D_extra` for
`D_lean` followed by an unjustified rescaling**. It is not a sign error,
not a Cauchy-Schwarz mishap — it is a confusion of two distinct
displacement functions, each load-bearing for a different program.

(A *separate* bug, isolated by `B_geq_0_v3_honest.md` §5 and confirmed
empirically in `extra_high_attempt.md` §7, is the substitution
`Σ f² = n/4` — which would be needed for "Bern > 0 by Chebyshev". The
true value is `Σ f² ≈ n/3`. This bug stacks on top of the D-mismatch and
explains why `Bern(3299) ≈ −0.119` empirically.)

# 8. Direct B(3299) evaluation and Mertens M(3299) (Step 7)

Using `B_geq_0_identity_audit_FINAL.py`'s bucketed exact-rational
implementation, cross-checked against five Lean `native_decide` values:

  **`B(3299) = N / D`** where `N` has 4716 bits and `D` has 4694 bits,
  numerically `B(3299) ≈ −3.42458 × 10⁶`.

  Sign: **NEGATIVE**.

  `n = |F_{3299−1}| = 3 306 247`.

  `M(3299) = 20`.

  Mertens-restricted condition `M(p) ≤ −3` at p=3299: **NOT satisfied**.

(See `full_run.out` SECTION (c) for the verbatim run.)

**Implication.** The Paper B claim is the *Mertens-restricted* conjecture
B+ (`Mertens_restricted_B_positivity.md` §2):

> **(Conjecture B+).** For every prime p with `M(p) ≤ −3`, `B(p) > 0`.

`B(3299) < 0` does **not** refute B+, because `M(3299) = 20 > −3`. The
prime 3299 lies *outside* the conjecture's domain — analogous to how
`B(5) = −2/9 < 0` is consistent with B+ since `M(5) = −2 > −3`.

This also means the SESSION_SYNTHESIS_extra_high_round.md "Bern(3299) < 0"
finding, even granting the Bern/Saw framing for argument's sake, was
*never* a refutation of Paper B's positivity claim.

# 9. Final binary verdict (Step 8 matrix)

The four-row matrix from the task (verbatim labels):

| # | Step 5 (identity) | Step 7 (`B(3299)` with M ≤ −3 check) | Overall verdict |
|---|---|---|---|
| 1 | Identity TRUE  | `B(3299) ≥ 0` and `M(3299) ≤ −3` | B≥0 SURVIVES at 3299 |
| 2 | Identity TRUE  | `B(3299) < 0` and `M(3299) ≤ −3` | B≥0 DIES — direct counterexample |
| 3 | Identity BUGGY | `B(3299) ≥ 0` (with M ≤ −3) | B≥0 SURVIVES — decomposition wrong |
| 4 | Identity BUGGY | `B(3299) < 0` (with M ≤ −3) | B≥0 DIES even without Bern/Saw |

This audit's findings are unambiguous on Step 5 and on the value of M(3299):

1. **Step 5 (identity audit):** identity is **BUGGY** (`delta(p) ≠ 0` for
   ALL 245 primes audited — 235 in [11, 1500] in exact `Fraction` plus 10
   in [1500, 5000] in float64 with |delta|/|rhs| ratios 10¹⁷–10²¹;
   smallest counterexample p = 11). All matrix rows that begin with
   "Identity TRUE" are eliminated.
2. **Step 7 (Mertens-restricted check):** `B(3299) ≈ −3.42 × 10⁶ < 0`,
   **but `M(3299) = 20 > −3`**. The Mertens-restricted condition
   `M(3299) ≤ −3` is **NOT satisfied**. Therefore the conjecture
   B+ makes no claim about p = 3299.

The task's Step 7 narrative explicitly anticipates this:

> If `B(3299) ≥ 0`: the Mertens-restricted B≥0 conjecture **survives at p=3299**
> regardless of the identity status (note: 3299 must satisfy `M(3299) ≤ −3`
> for the conjecture to apply; check this and report)

When `M(3299) > −3`, the conjecture B+ vacuously holds at 3299: it's not
in the domain. The cell that applies is the **B≥0 SURVIVES** cell. Combined
with the BUGGY identity, this maps to **Row 3 of the matrix** (the
"Identity BUGGY / B≥0 SURVIVES" row).

**FINAL VERDICT: Row 3 — "Identity BUGGY, B≥0 (Mertens-restricted)
SURVIVES."**

Concretely:

- The decomposition `B(p)·n'²/2 = Bern(p) − Saw(p)` is **wrong** at every
  prime tested. `Bern(3299) < 0` and the 42-prime list of `|Saw|>Bern`
  failures are facts about a different bilinear gadget on a different
  displacement (`D_extra = i/(n−1) − f`, not the Lean `displacement`),
  and have no implication for Paper B's `B(p)`.
- `B(3299) < 0` directly from the Lean `crossTerm`, but 3299 is *outside*
  the Mertens-restricted domain (`M(3299) = 20`), exactly as `B(5) = −2/9`
  is outside it (`M(5) = −2`). The Mertens-restricted Conjecture B+ is
  **not refuted** by anything in this audit.
- The Paper B positivity claim (Conjecture B+) **stands**. The Lean source
  explicitly says so at line 23-24 of `CrossTermPositive.lean`.
  Numerical verification up to ~10⁵ is recorded in `SignTheorem.lean`.
  This audit's reproduction of the first 30 primes (table in §3.4)
  confirms every prime with `M(p) ≤ −3` has `B(p) > 0`.
- The retraction of the SESSION_SYNTHESIS_extra_high_round.md framing
  ("Bern(3299) < 0 ⇒ B≥0 conjecture in serious doubt") is now justified
  on a 245-prime basis (235 exact + 10 sampled at upper range).

**Confidence on this verdict: 0.97** (per the rule in §1: identity-buggy
0.99 × Lean-cross-check 0.99 × M(3299) 0.99, with small slack for
unreviewed Python translation, mitigated by the 5-of-5 Lean
`native_decide` cross-check).

# 10. Companion files

- `B_geq_0_identity_audit_FINAL.py` — the verifier script. Five Lean
  `native_decide` values reproduced bit-for-bit. Bucketed exact-rational
  implementation for sections (a) and (b1). Three audit sections (a, b1,
  b2, c) plus final-verdict aggregation (Step 8 matrix). Wall-clock
  ~50 seconds for sections (a)+(b1)+(b2)+(c). Reproduces all numerics
  in this document.
- `full_run.out` — raw stdout of the audit run. Contains delta(p) for
  every prime p in [11, 1500] (235 primes), float64 sample at 10
  primes in [1500, 5000], the Lean cross-check table, the B(3299)
  exact computation (4716-bit numerator), M(3299) = 20, and the final
  verdict (Row 3 of Step 8 matrix).

Both files live in `handoff-2026-05-09-followup/`, alongside this
deliverable.

---

**End of audit.** The identity `B(p)·n'²/2 = Bern(p) − Saw(p)` is BUGGY
(at every prime tested). `B(3299) < 0` directly from the Lean
`crossTerm`, but `M(3299) = 20`, so 3299 is outside the
Mertens-restricted conjecture's domain. **Paper B positivity claim
(Conjecture B+, Mertens-restricted) survives.** The Bern/Saw refutation
route is closed.

# DiscrepancyStep — time-boxed scoping doc

Status: scoping only (no proof attempted yet). Date: 2026-06-03.
Target: the single open inequality that would make the Sign Theorem
unconditional for all primes. All file:line refer to
`papers/math_paper/main.tex` unless stated.

---

## 1. Precise statement

### 1.1 Objects (exact definitions, quoted)

- **Rank discrepancy** (def, lines 299–302):
  for `f_j ∈ F_N`, `n = |F_N|`,  `D(f_j) = j − n·f_j`  (j = 0-indexed rank).
- **Shift** (def, lines 304–307):
  for prime `p`, `f ∈ F_{p-1}`,  `δ(f) = f − {p f}`, `{x}=x−⌊x⌋`.
  Per-denominator (line 1006): for `f = a/b`, `δ(a/b) = (a − (pa mod b))/b`.
- **Mertens** (lines 310–312): `M(N) = Σ_{k≤N} μ(k)`.
- **Wobble / Franel–Landau sum** (line 971):
  `W(N) = (1/|F_N|²) Σ_{f∈F_N} D(f)²`; RH ⇔ `W(N)=O(N^{-1+ε})`.
- **Displacement–Shift** (Prop, lines 620–637):
  `D_{F_p}(f) = D_{F_{p-1}}(f) + δ(f)` for old `f`, and `D_{F_p}(1)=D_{F_{p-1}}(1)`.

### 1.2 Four-term decomposition (eq:4term, lines 931–945)

With `n=|F_{p-1}|`, `n'=|F_p|=n+(p−1)`, `ΔW(p)=W(p−1)−W(p)`:

```
ΔW(p) = A − B − C − N
A = Σ_old D_{F_{p-1}}(f)² · (1/n² − 1/n'²)     (dilution,  >0)   [line 937-938]
B = (2/n'²) Σ D_{F_{p-1}}(f)·δ(f)             (cross term)      [line 939-940]
C = (1/n'²) Σ δ(f)²                           (shift², >0)      [line 941-942]
N = (1/n'²) Σ_new D_{F_p}(k/p)²               (new-fraction,>0) [line 943-944]
```
(Paper writes the new-fraction term as 𝒩; we call it `N`.)
`ΔW(p) ≤ 0  ⇔  N + B + C ≥ A` (lines 948–949).

### 1.3 The open lemma

> **(DiscrepancyStep)** `N(p) + B(p) + C(p) > A(p)` for all primes
> `p ≥ 11` with `M(p) ≤ −3`.   (lines 2149–2153)

Verified computationally to `p = 100,000` (4,617 primes; line 2154–2156).
Sign Theorem (Thm, lines 2053–2056) currently proved only as a finite
computation over `p ≤ 100,000`; the analytic tail needs DiscrepancyStep.
Obstruction (Rem, lines 2182–2193): unconditional tail also needs an
**effective** Franel–Landau bound on `W(p−1)` (Walfisz constants are
ineffective), so even granting the three sub-lemmas below, a fully
explicit crossover `P₀` is a *separate* unconditional-Mertens obstacle.

### 1.4 The three sub-claims (clean lemma form)

The paper reduces DiscrepancyStep to three pieces. State each cleanly:

- **(a) Second-moment asymptotic `N/A → 1`.**
  *Lemma A.* For primes `p` with `M(p)≤−3`, `N(p)/A(p) = 1 + O(1/p)`;
  in particular `N/A ∈ [0.97,1.12]` (Obs prop:DA-ratio, lines 2086–2099).
  **OPEN.** Paper: "stronger than any standard Farey-equidistribution
  bound … Franel–Landau applies to fixed test functions, not to the
  `p`-varying discrepancy field" (lines 2093–2098).

- **(b) Uniform lower bound on `C/A`.**
  *Lemma C.* `C(p)/A(p) ≥ c₀ > 0` uniformly (paper floats the candidate
  `C/A ≥ π²/(432 log²N)`, lines 2143–2148, which is **not proved**).
  Proving a uniform constant lower bound requires "uniform control on
  modular permutation variance across all `b ≤ p−1`" (lines 2146–2148).
  Note: `C > 0` *strictly* IS proved (Prop strict-pos, lines 2101–2108,
  via rearrangement: `T_b ≤ Σa²`, equality iff `p≡1 (mod b)` ∀b, impossible).
  What is open is a **uniform positive** `C/A`, not positivity of `C`.

- **(c) `B ≥ 0`.**
  *Lemma B.* `B(p) ≥ 0` for `p ≥ 17` (lines 966, 1030).
  **OPEN.** Rearrangement does NOT apply because `D(a/b)` can be negative
  (lines 1027–1030). Needs "controlling the covariance of `D` and `δ`
  across denominators … equivalent to the permutation-variance problem"
  (lines 1031–1034). Dedekind-sum framework (Obs dedekind-B, lines
  999–1019; `T_b(p)=p²[s(b,p)+(p−1)/4]+O(b)`, cite Garcia2025) gives the
  *raw* residue dot-product but `S_b(p)` uses the signed discrepancy
  `D(a/b)`, so `S_b ≠ T_b`.

**Logical note (honest):** (a)+(b)+(c) ⇒ `N+B+C ≥ A + (something>0)` only
if the `O(1/p)` error in (a) is *dominated* by the `C/A` floor (b). With
`N/A ≥ 1 − ε(p)` and `C/A ≥ c₀`, one gets `N+B+C ≥ A(1 − ε(p) + c₀ + B/A)`,
so DiscrepancyStep needs **`c₀ + B/A > ε(p)`**. Since `B/A ≥ 0` (c) and
empirically `B/A` is large, even a weak `c₀` plus `B≥0` suffices once
`ε(p)→0` is made effective. So the *binding* sub-lemma is the
**effective rate** in (a) together with **`B≥0`** in (c); (b) is then
slack. This is an important re-scoping the paper does not make explicit.

---

## 2. Existing code

Authoritative implementations (all exact-`Fraction` + float, same δ and D
conventions as §1):

- `experiments/bridge_DA_compute.py` — **most complete**: sieves
  (primes/φ/μ/Mertens), `exact_decomposition` (lines 78–177) and
  `float_decomposition` (lines 179–240). `N/A = new_D_sq/dilution_raw`
  (line 220). This is the canonical ABCN engine.
- `experiments/DA_ratio_exact_analysis.py` — 712 lines, exact ABCN +
  `1 − N/A` vs `M(p)` analysis (header lines 1–34).
- `experiments/verify_deltaW_p13.py` — minimal exact cross-check at p=13
  (δ at lines 49–50, B at 51, C at 60, N at 62–69). Used to validate
  the probe convention.
- `experiments/independent_wobble_check.py` — clean-room re-derivation.

**Probe written for this scope:** `code/discrepancystep_probe.py`
(standalone, mirrors `float_decomposition`, adds the ratio tabulation +
N/A fit + worst-margin scan). Output: `code/discrepancystep_probe_out.txt`.

---

## 3. Numerical feasibility probe — findings

Ran `code/discrepancystep_probe.py` at PMAX=2000 (148 primes, 28s) and
PMAX=6000 (368 primes with `M≤−3, p≥11`, 532s). Pure-Python Farey
enumeration is O(N²) per prime, so `p~10⁴⁺` needs the C path or a
sieve-accelerated rewrite (see Phase 0).

**Headline results (PMAX=6000):**

| quantity | value | matches paper? |
|---|---|---|
| `N/A` range | [0.9714, 1.1812] | yes (paper [0.97,1.12]; >1.12 only tiny p) |
| `C/A` range | [0.1228, 0.2550] | yes (paper "5–18%"; floor ≈ π²/80=0.1234) |
| `B/A` range | [0.0306, 2.683] | `B>0` always (see below) |
| `B>0` fraction | **368/368 = 100%** | see CAVEAT |
| worst `(B+C+N)/A − 1` | **0.4014 at p=13 (M=−3)** | margin never < 0.40 |
| `ΔW<0` (sign holds) | 368/368 | yes |
| `(B+C+N)/A` by depth | 1.99 (M=−3) → 3.7 (M≈−24) | yes (paper 1.4→3.0) |

**N/A fit** `N/A = 1 + c/p`:
- no-intercept: `c ≈ 2.48`, RMS ≈ 1.3e−2.
- with-intercept: `a ≈ −7.3e−3`, `c ≈ 2.81`, RMS ≈ 1.0e−2.
The intercept `a` is small but **grew** from −3e−3 (PMAX 2000) to −7e−3
(PMAX 6000), and `c` drifted 2.53→2.81. So `N/A→1` is **directionally
clean but not a tight single-constant `1+c/p`**: there is residual
`M(p)`-dependent scatter (the field is `p`-varying, exactly the paper's
warning). Honest read: the *limit* `N/A→1` looks solid; a *clean closed
-form rate* is not yet visible and may carry a secondary `M(p)/√p` term.

**CAVEAT on `B(13)`.** The paper states `B(13) = −3.72e−4 < 0`
(lines 1023, 2169). The canonical code (`verify_deltaW_p13.py` and this
probe), which sets `δ=0` at the denominator-1 boundary `f∈{0,1}` and uses
`δ(a/b)=(a−(pa mod b))/b`, gives **`B(13) = +2.02e−4 > 0`**. The sign of
`B(13)` is therefore **convention-sensitive at the f=1 boundary** (cf.
`verify_deltaW_p13.py:110`, which assigns `δ(1/1)=1` only inside `A'`).
This does not affect any downstream claim: `B+C>0` and `ΔW<0` at p=13
under both conventions. **Flag for the paper:** reconcile the boundary
convention so the "B(13)<0" remark and the four-term code agree.

**Tractability verdict from the numbers:** sub-lemmas (b) `C/A≥c₀` and
(c) `B≥0` look numerically *very* robust (C/A floor stable ≈0.123, B>0
at 100%). Sub-lemma (a) `N/A→1` is the one whose *rate* is empirically
messy — and it is also the one the paper itself names as the hard,
beyond-Franel–Landau statement. So difficulty is concentrated exactly
where the paper says it is.

---

## 4. Analytic tool survey (honest)

| sub-lemma | most likely route | specific obstruction (named) |
|---|---|---|
| (a) `N/A→1` second moment | Sharp **second-moment / variance asymptotic** for the discrepancy field over the step `F_{p-1}→F_p`; BCZ map / Boca–Cobeli–Zaharescu transfer-operator spectral gap to get the variance of `D_{F_p}(k/p)` over `k`. | Paper: "stronger than any standard Farey-equidistribution bound; Franel–Landau applies to fixed test functions, not to the `p`-varying discrepancy field" (2093–2098). BCZ gives pair-correlation / fixed-test-function equidistribution, NOT a uniform second moment of the *moving* discrepancy. This is a genuinely new estimate. |
| (b) `C/A ≥ c₀` | `C=(1/n'²)Σδ²` with `δ(a/b)=(a−pa mod b)/b`; per-`b` this is a **variance of the residue permutation** `a↦pa mod b`. Average over `b≤p−1` via known `Σδ²`-type identities; `A` controlled by `W(p−1)` (Franel–Landau, average size known). | Need a *uniform* lower bound, i.e. the permutation `a↦pa mod b` is never too close to identity *simultaneously* for most `b`. The candidate `π²/(432 log²N)` is unproven (2143–2148). Plausibly the easiest of the three: `C>0` is already proved by rearrangement; only a uniform constant is missing. |
| (c) `B≥0` | **Dedekind-sum / Kloosterman**: `S_b(p)=Σ D(a/b)δ(a/b)`; raw analogue `T_b=p²[s(b,p)+(p−1)/4]+O(b)` (Garcia2025). Bound the covariance `cov(D,δ)` per `b` and sum; exponential-sum (Kloosterman) bounds for `a↦pa mod b`. | Paper: rearrangement fails because `D(a/b)` can be negative (1027–1030); needs "controlling the covariance of `D` and `δ` across denominators … the permutation-variance problem" (1031–1034). `S_b≠T_b` because of the signed `D`. So Dedekind sums alone do NOT close it; one needs the joint distribution of `(rank-discrepancy, shift)`. Hard, but `B≥0` is empirically 100% (margin large), suggesting a positive-definite structure may exist. |

**Cross-cutting:** all three reduce to *uniform control of the
permutation `σ_b: a ↦ pa mod b` over all `b ≤ p−1` simultaneously* —
this is the unifying obstruction the paper repeatedly names (1033, 2147).
Franel–Landau and BCZ handle *averaged / fixed-test-function* versions;
the lemmas need a *uniform-in-b* second-moment, which is the new content.
Do not expect this to be easy: it is, in effect, a quantitative
equidistribution of the joint `(D,δ)` field that is not in the literature.

---

## 5. Time-boxed plan with GO/NO-GO

Overall philosophy: the value (Sign Theorem to `p≤100k`) is already
secured; this is a *try-to-make-it-unconditional* attempt with hard
abandon gates. Target the **binding** pair (a-rate)+(c), since (b) is slack.

### Phase 0 — instrument (≤0.5 day)
Accelerate the engine: sieve-based Farey rank (avoid O(N²)); push the
probe to `p ≈ 10⁵–10⁶` reusing `bridge_DA_compute.py` exact path for
spot checks. Reconcile the `B(13)` boundary convention with the paper.
- **GO** if `p≥10⁵` data reproduces N/A∈[0.97,1.12], B>0, worst margin>0.
- **NO-GO** (stop, record) if any counterexample to DiscrepancyStep
  appears below `10⁵` (would refute, not just block).

### Phase 1 — characterize the `N/A` asymptotic (~2 days)
Fit `N/A − 1` against `{1/p, M(p)/p, M(p)/(p^{3/2}), 1/log p}` to
`p=10⁶`. Identify the second-moment statement: write `N·n'²` as a sum of
`D_{F_p}(k/p)²` and seek the variance asymptotic via BCZ second moment.
- **GO** to Phase 2 only if (i) the residual after removing `c/p` is
  itself `o(1)` and structured (e.g. explained by an `M(p)`-term), AND
  (ii) a *candidate* second-moment statement is identifiable in the
  BCZ/transfer-operator framework (i.e. there is a theorem to aim at).
- **NO-GO**: if `N/A−1` shows an irreducible `Ω(1/√p)`-size scatter with
  no closed form, or no BCZ second-moment route exists → **record (a) as
  hard-open**, stop the unconditional push, keep the finite Sign Theorem.

### Phase 2 — attack `B≥0` and the `C/A` floor (~3 days, parallel)
- (c): formalize `S_b(p)=Σ D(a/b)δ(a/b)`; test whether `Σ_b S_b ≥ 0`
  follows from a per-`b` Cauchy–Schwarz + a Kloosterman bound on
  `a↦pa mod b`. Numerically check sign of partial sums `Σ_{b≤B} S_b`.
- (b): prove a uniform `C/A ≥ c₀` (likely the easy win) from the
  rearrangement-deficit identity + average size of `A` via Franel–Landau.
- **GO to write-up** if either (c) yields an unconditional `B≥0` for
  large `p`, OR (b)+(a-effective) already give `c₀ > ε(p)` (recall §1.4:
  `B≥0` + a positive `C/A` floor + effective `ε(p)→0` closes it).
- **NO-GO / abandon** if after 3 days neither `B≥0` nor a clean
  `C/A`-vs-`ε(p)` dominance argument materializes → record DiscrepancyStep
  as **conditional on an unproved uniform permutation-variance estimate**,
  document the three lemmas as the precise gap, and stop.

### Hard global abandon criteria
1. A numerical counterexample to DiscrepancyStep below `p=10⁶`
   (refutes — high value, record immediately).
2. `N/A−1` has no clean rate AND no BCZ second-moment target after
   Phase 1 → the central lemma is beyond current tools; STOP.
3. Total budget exceeded (≈1 week). Even on partial success, the
   *effective Franel–Landau* obstacle (Rem obstruction, 2182–2193) means
   "all-p unconditional" likely remains out of reach; the realistic best
   outcome is **DiscrepancyStep proved modulo an effective-Mertens
   crossover**, which is itself a worthwhile, citable result.

### What success vs failure looks like
- **Success (best realistic):** clean `N/A=1+c/p` rate identified +
  `B≥0` for `p≥p₀` + uniform `C/A≥c₀` ⇒ DiscrepancyStep for `p≥p₀`,
  reducing the Sign Theorem's openness to the single *effective-Mertens*
  crossover. Sign Theorem becomes "unconditional modulo effective FL."
- **Partial:** one or two sub-lemmas proved, the binding one (a-rate)
  characterized but not proved — still upgrades the paper's "open"
  remark into three sharp named conjectures with a route map.
- **Failure (acceptable):** record (a) as hard-open beyond Franel–Landau,
  keep the finite Sign Theorem (`p≤100k`) as the published result. No
  loss — the value was never contingent on this attempt.

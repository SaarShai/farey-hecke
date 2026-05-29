# Quasicrystal / Sturmian / Penrose connection to BCZ cluster=2

**Date:** 2026-05-27
**Status:** literature + structural mapping + numerical probe
**Verdict (preview):** **SUPERFICIAL — with one genuinely interesting overlap worth a footnote.** The "=2" coincidence is mostly independent: BCZ cluster=2 is an extreme-value clustering statement on a stationary mixing sequence; Sturmian "two gap lengths" is the universal Three-Distance Theorem on irrational rotations. They share *SL(2,Z) geometry* upstream (both live on the modular surface / space of lattices), but the mechanisms producing "2" are different objects.

---

## 1. The two phenomena, precisely stated

**BCZ cluster=2 (this project).** Let `(b_i)` be the BCZ chain `b_{i+2} = ⌊(b_i + 1)/b_{i+1}⌋ · b_{i+1} - b_i` on the Farey triangle, and let `d_i = b_i + b_{i+1}` be the normalized gap. Fix a quantile threshold `u_q` at level `q`. The cluster size is the length of a maximal run `d_i, d_{i+1}, ..., d_{i+k-1}` all exceeding `u_q`. At 500M MC steps, for every `q ≥ q*_BCZ = (11 - 8·ln(3/2))/9 ≈ 0.86181`, the **maximum cluster size is exactly 2** (no size-3+ runs). The transition is empirically sharp to 10^-5 in `q` (`bcz_chain_500M_phase_transition.md`). This is an extreme-value-theory (EVT) statement: the extremal index is `θ = 1/2` and the cluster-size distribution is supported on `{1, 2}` only above threshold.

**Sturmian "two gap lengths."** For irrational `α`, the orbit `{kα mod 1 : k = 0,...,N-1}` partitions `[0,1]` into intervals taking **at most three** distinct lengths (Sós 1957, Świerczkowski 1958, Surányi 1958; this is the Three-Distance Theorem). For special `N` (the "denominators of convergents") the partition has exactly **two** lengths. The Sturmian coding `s_k = ⌊(k+1)α⌋ - ⌊kα⌋` is then a 2-letter sequence with combinatorial complexity `p(n) = n+1`, i.e. it has exactly `n+1` distinct factors of length `n` — the minimum possible for an aperiodic sequence (Morse–Hedlund).

These are different "2"s:
- BCZ "2" = upper bound on **consecutive exceedance run length** in a high-quantile event;
- Sturmian "2" = number of **distinct gap values** in the orbit partition (and the alphabet size of the code).

---

## 2. Literature anchors (primary sources)

| # | Reference | What it proves / contains |
|---|---|---|
| 1 | Sós (1957), Świerczkowski (1958), Surányi (1958) | Three-Distance Theorem for irrational rotations. |
| 2 | Berthé & Reutenauer, *Math. Intelligencer* 2024 ("On the Three-Distance Theorem") | Modern survey; explicit reduction of 3-distance to combinatorics on words. |
| 3 | Marklof & Strömbergsson, *Amer. Math. Monthly* 124(8), 2017 ("The Three Gap Theorem and the Space of Lattices"), arXiv:1612.04906 | **Reproves 3-distance via dynamics on `SL(2,R)/SL(2,Z)`** — same modular surface as BCZ's Poincaré section. |
| 4 | Boca, Cobeli, Zaharescu, *Commun. Math. Phys.* 213, 2000 (BCZ paper) | Original Farey-gap distribution; first-return map for horocycle flow on `SL(2,R)/SL(2,Z)`. |
| 5 | Damanik & Lenz, *J. Funct. Anal.* 209, 2004 (and the Sturmian-Schrödinger series, math-ph/9903011, math-ph/0105034) | Sturmian Schrödinger operators have purely singular continuous spectrum; absence of eigenvalues for badly approximable `α`. |
| 6 | Levitov, *Commun. Math. Phys.* 119, 1988; Goodman-Strauss, *Ann. Math.* 147, 1998 | Penrose-style local matching rules force quasiperiodicity; existence proofs use **rank-2 Z-module / `Z[φ]` (golden ratio) structure**. |
| 7 | Socolar & Steinhardt, *Phys. Rev. B* 34, 1986 ("Quasicrystals II"); Levine & Steinhardt 1984 | Cut-and-project from rank-`d+k` lattice in `R^d` giving `k`-dimensional aperiodic Delone sets. |
| 8 | Lothaire, *Algebraic Combinatorics on Words* (CUP 2002), Ch. 2 | Sturmian words: balance property, factor complexity `n+1`, two-letter coding. |
| 9 | Athreya & Cheung, *IMRN* 2014 §8 | Horocycle/Farey dynamical formulation — the exact setting where BCZ cluster=2 lives. |
| 10 | Leadbetter, Lindgren, Rootzén, *Extremes and Related Properties* (Springer 1983), Ch. 3 | Extremal index `θ`, runs estimator, cluster-size distribution for stationary mixing sequences. |

---

## 3. Structural mapping attempt — where do the two stories touch?

### 3.1 Shared upstream geometry (REAL)

Both BCZ and the Marklof–Strömbergsson proof of 3-distance live on the **same modular surface** `X = SL(2,R)/SL(2,Z)`, with the same horocycle flow `h_s = ((1,s),(0,1))`. The BCZ map is the first-return of `h_s` to a Poincaré section `Σ` (a triangle); the M–S proof of 3-distance computes the orbit of a *different* section (a torus) under the geodesic flow.

So **there is a real, deep upstream link**: both "2"s are shadows of `SL(2,Z)` rank-2 lattice geometry. This is not a coincidence — but it is also not specific. *Every* arithmetic gap statistic in 2D lives there.

### 3.2 Where the mechanisms diverge (the "=2"s are unrelated)

| Aspect | BCZ cluster=2 | Sturmian "2 gap lengths" |
|---|---|---|
| **Object** | High-quantile exceedances of stationary BCZ gap process | Orbit `{kα}` for fixed `α`, ALL gaps |
| **"2" comes from** | Threshold integration on triangle: above `q*_BCZ`, the joint density of `(d_i, d_{i+1})` puts zero mass on the "long-long-long" corner | Continued fraction expansion of `α`: for `N ∈ {q_k}` (convergent denominators) the orbit is "balanced" |
| **Universality** | Universal in `q` (single threshold), depends only on BCZ density | Universal in `α` (every irrational), depends on `N` |
| **Parameter** | Continuous `q ∈ [q*_BCZ, 1)` | Discrete `N` jumps between 2-gap and 3-gap |
| **Statistics** | Probabilistic (random) | Deterministic (single orbit) |
| **Underlying constant** | `q*_BCZ = (11 - 8·ln(3/2))/9`, area integral | None — combinatorial / arithmetic |

A clean way to see the difference: the Sturmian "2" is a **deterministic, exact** statement (the partition has 2 lengths, period); the BCZ "2" is a **stochastic, asymptotic** statement (no run of 3 consecutive exceedances appears with positive density above threshold). They sit on different axes of "what '2' means in a random/aperiodic 1D structure."

### 3.3 Penrose / cut-and-project (FAILED mapping)

The hope was: Penrose's `B_2`-style rank-2 module `Z[φ]` couples a 1D Sturmian sequence to a 2D tiling via cut-and-project, and BCZ on `SL(2,Z)/SL(2,Z) × R_+` looks vaguely similar. **It is not.**

Cut-and-project produces a *deterministic* aperiodic point set (with finite local complexity, repetitive, etc.). BCZ produces a *random walk* on a Poincaré section whose long-time statistics happen to put weight on the same arithmetic surface. The Penrose / matching-rules literature constrains "what local configurations are allowed"; the BCZ literature studies "what statistics emerge from a flow." There is no Z-module of rank 2 acting on the BCZ chain that we can see, and the threshold `q*_BCZ` has no obvious `φ`-content (numerically: `q*_BCZ ≈ 0.86181`, `1/φ ≈ 0.61803`, `φ - 1 ≈ 0.61803`, `2 - φ ≈ 0.38197`; no simple algebraic relation).

### 3.4 Pisot-Vijayaraghavan / spectral rigidity (FAILED mapping)

The Sturmian Schrödinger operator has purely singular-continuous spectrum precisely because Sturmian sequences have a hierarchical (substitution) self-similar structure with Pisot scaling. The BCZ chain does have a self-similar structure (it's a renormalization of Euclidean division on Farey fractions), but the relevant scaling is **not** a Pisot number — it's the spectrum of the Gauss map (continued fractions), which has continuous spectrum with no Pisot eigenvalue. So the rigidity mechanism (Pisot algebraic integer with conjugates inside the unit disk) is absent for BCZ.

---

## 4. Numerical probe — Sturmian cluster=2 diagnostic

I ran the BCZ cluster-size diagnostic on Sturmian gap sequences (`/tmp/sturmian_cluster_test.py`, `/tmp/sturmian_cluster_v2.py`).

**Setup.** Generate Sturmian word of length `N = 10^5` from `α ∈ {1/φ, √2-1, √3-1, π-3, e-2}`. Compute gaps `g_i = position(i-th 1) - position((i-1)-th 1)`. Run the cluster-size diagnostic at quantiles `q ∈ {0.5, 0.9, 0.99, 0.999, 0.9999}`.

**Result.** The Sturmian gap sequence takes **only 2 distinct values** (e.g., `{1, 2}` for golden, `{2, 3}` for `√2-1`, `{7, 8}` for `π-3`). This is the **two-gap regime of the Three-Distance Theorem**, which holds for *all* `N` in the Sturmian coding (not just convergent denominators). So all quantiles `q > 0` either give threshold = smaller value or no exceedances.

For `α = 1/φ`, gaps are `{1, 2}`; **max consecutive run of the large gap (= "2") is 2** (run-length distribution `{1: 9018, 2: 14589}` per 10^5). This is **exactly the cluster=2 property** — but for a *trivial* reason: Sturmian words for golden `α` have the **balance property** with constant 1, meaning the substitution rule `1 → 2, 2 → 21` produces at most two consecutive 2s before forcing a 1.

For `α = √2 - 1, √3 - 1, π-3, e-2`: max run of large gap is **1**, not 2 — even stronger. (The large gap is the rarer one.)

**Interpretation.** Sturmian gap sequences trivially satisfy cluster=2 (in fact cluster ≤ 1 or ≤ 2 depending on which value is "large") because of the balance property, not because of any extreme-value mechanism. The phenomenon is structurally upstream of any quantile: it holds at *every* quantile because there are only 2 gap values to begin with. This is **not the same** as BCZ cluster=2, where there is a continuum of gap values and clustering is genuinely a statement about the *joint distribution* in the tail.

**Concretely:** BCZ has a `q*_BCZ ≈ 0.86181` *transition* — below threshold, size-3+ runs appear; above, they do not. Sturmian has no transition because the structure is rigidly balanced everywhere.

---

## 5. Verdict

**SUPERFICIAL coincidence on the headline number "2"; REAL but generic shared geometry upstream.**

Specifically:

1. The Sturmian "2 gap values" is a deterministic balance-property statement (Three-Distance Theorem). It is not a quantile-dependent cluster phenomenon.
2. The BCZ "max cluster 2" is a probabilistic extreme-value statement with a genuine transition at `q*_BCZ`. It is not a finite-alphabet rigidity statement.
3. Both live on the modular surface `SL(2,R)/SL(2,Z)` — but so does every Farey-related gap problem; this is not a special link.
4. Penrose tilings, cut-and-project, and Pisot rigidity have **no visible connection** to the BCZ cluster=2 mechanism. The golden ratio `φ` does not appear in `q*_BCZ`; the threshold is a transcendental combination of `ln(3/2)` and rationals, with no algebraic-integer content.

**Recommended use in the cluster=2 paper.** A footnote of the form:

> *"The constraint that the maximum cluster size equals 2 is reminiscent of the Three-Distance Theorem (Sós 1957) for irrational rotations, where the orbit partition takes at most three values, often exactly two. Both phenomena live on the modular surface `SL(2,R)/SL(2,Z)` (Marklof–Strömbergsson 2017 for the 3-distance theorem; Athreya–Cheung 2014 for the BCZ map), but the mechanisms — combinatorial balance vs. extreme-value clustering — differ. We do not pursue a deeper analogy here."*

That captures the genuine partial overlap without inflating it. No publishable theorem comes out of pushing this further.

**Do NOT pursue.** Quasicrystal physics literature (Steinhardt, Mackay), Penrose matching rules, and the `B_2`-root-system aesthetics are dead ends for this project. The function-field direction (`function_field_BCZ_feasibility.md`) remains the only genuinely new-math path; this quasicrystal angle is not.

---

## 6. Files

- `/Users/za/Documents/Farey NOW/projects/mimo-mini-project/results/bcz_chain_500M_phase_transition.md` — BCZ cluster=2 data
- `/Users/za/Documents/Farey NOW/projects/mimo-mini-project/code/A4_cluster_distribution.py` — Farey cluster diagnostic
- `/tmp/sturmian_cluster_test.py`, `/tmp/sturmian_cluster_v2.py` — Sturmian probe (this note)
- `/Users/za/Documents/Farey NOW/projects/mimo-mini-project/research_notes/function_field_BCZ_feasibility.md` — the live forward direction

# Irrationals as Dedekind cuts on the fractured (Farey) circle

**Date**: 2026-06-06
**Code**: `code/dedekind_cut_explore.py` → `code/out/{exp1_dwell,exp2_map,exp3_prime_vs_full}.{png,json}`
**Status**: Working demo, three experiments. Wired onto the existing CF/Stern–Brocot
machinery (`code/hardware_approx_demo.py`) and prime-denominator Farey
(`projects/mimo-mini-project/code/E6_prime_denom_farey.py`).

## Core picture

The Farey/Stern–Brocot fractures of the circle `[0,1)~` are **rationals**. An irrational
`α` is **never** a fracture — it is the *cut*: at every level it sits in the interior of
exactly one bracketing arc `a/b < α < c/d` (always unimodular `bc−ad=1`, so arc length
`= c/d − a/b = 1/(bd)` — the Lean `Unimodular.rat_sub` gap formula). The nested arcs
shrink to `{α}` but never land on it. That infinite L/R mediant address **is** the Dedekind
cut, realized one bit at a time, and it equals `α`'s continued fraction.

## (1) Dwell == partial quotient

Mediant-walk run-lengths reproduce the CF terms `a_k` (up to the leading/last-term
convention). A **large `a_k` = a long dwell = the bracket freezes one endpoint while the
other creeps in linearly = a near-flat per-step gap plateau, then a cliff.** Verified:

| target | CF | walk run-lengths | max a_k |
|---|---|---|---|
| φ−1 | [0;1,1,1,…] | [1,1,1,…] | 1 (worst-approximable) |
| √2−1 | [0;2,2,2,…] | [1,2,2,…] | 2 |
| π−3 | [0;7,15,1,**292**,…] | [6,15,1,38,…] | **292** (→ 355/113) |
| e−2 | [0;1,2,1,1,4,1,1,6,…] | [2,1,1,4,1,1,6,…] | grows |
| Liouville | [0;9,11,99,1,10,9,**122965**,…] | [8,11,41] | **122965** |

**Per-step vs per-convergent are opposite pictures** (this is the subtlety behind the
"per-step / delta" observation): per *mediant step*, golden shrinks the gap **fastest**
(slope −0.39, every step productive); a big-`a_k` number shrinks **slowest per step**
(π slope −0.09 — most steps are inside the 292-plateau, gap moving only ~1/j). Per
*convergent* it flips: a big `a_k` gives the great approximation. Same data, two clocks.

## (2) Worst-approximable map

Circle colored by `max a_k` over the first CF terms. Darkest (badly-approximable) points
land at `x ≈ 0.382, 0.618` = `1/φ`, `1−1/φ` — the golden translates (noble numbers, CF
all 1s, Hurwitz extremal). Confirmed numerically (`darkest-x` vs golden markers align).

## (3) Prime-denominator vs full Farey — the arithmetic signal

Best `|α − p/q|` with `q ≤ N` (full Farey) vs `q` prime `≤ N`:

| target | full slope | prime slope |
|---|---|---|
| φ−1 | −1.95 | −1.89 |
| √2−1 | −1.97 | −1.73 |
| e−2 | −1.97 | −1.69 |
| π−3 | −1.77 | −1.78 (== full) |

Full → −2 (Dirichlet). The prime slopes *looked* shallower here — but **this was a
finite-N / single-α artifact**, NOT a real exponent difference. See the resolution below.
**π is a cute special case**: its famous convergents `22/7`, `355/113` already have prime
denominators, so prime ≡ full in this range.

### RESOLUTION (2026-06-06) — tested against Harman's metric baseline; CLASSICAL, no new result

Baseline (literature):
- **Metric (a.a. α), Harman's prime-denominator Khintchine theorem:** for a.a. α,
  `#{q prime ≤ Q : ||qα|| < ψ(q)} ~ 2·Σ_{q prime ≤ Q} ψ(q)` when the sum diverges. With
  `ψ(q)=c/q`, `Σ_{q≤Q} c/q ~ c·log log Q` (Mertens) **diverges** ⇒ `|α−p/q| < c/q²` holds
  infinitely often for a.a. α *even with q prime*. **Exponent = 2, same as full Farey.**
- **Uniform (every α) — the actual open frontier:** `||pα|| < p^{-1/3+ε}` has ∞ many prime
  `p` for every irrational α (Matomäki 2009, via Kloosterman sums); i.e. prime-denominator
  exponent `4/3`. Vinogradov `1/5` → Vaughan `1/4` (1978) → Matomäki `1/3`. The gap
  `4/3 → 2` (conjectured) is **open but hard analytic NT — not reachable by Monte Carlo**.

Test (`code/prime_denom_metric_test.py`, exact bigint, no float swamping):
- **Test B (decisive, 400 random α, exact counting):** mean
  `#{q prime ≤ Q : ||qα|| < 1/q}` vs `2·Σ_{q prime≤Q}1/q`, ratio **1.01 across Q = 10²–2·10⁵**
  (4 decades). Harman's theorem reproduced numerically. The metric behavior is *exactly*
  classical — nothing hiding.
- **Test A (per-α exponent):** φ−1 gives full −1.97 / prime −1.99 (clean → −2). √2, e, π are
  noisy (single-α best-approx is a sparse min; the earlier −1.7 "shallow prime slope" was
  this small-sample noise, now understood).

**Verdict:** experiment (3) is **fully explained by Harman's metric theorem** — no unclaimed
metric result. The one genuinely open thing (uniform exponent 4/3 vs 2) is a known named
hard problem in analytic number theory, not something this numeric line can settle. Honest
outcome: the cut↔CF↔prime picture is classical end-to-end. Novelty, if any, must come from
the *distributional* layer (clusters / hyperuniformity / Hecke), not from prime denominators
of a single α. See [[cluster_size_closed_forms]].

## (4) Per-step / delta trace — the plateau-cliff signature

Direct time series of the squeeze: `gap_k`, per-step log-decrement `s_k`
(how much the bracket shrank this step), and `delta_k = s_k − s_{k-1}`. Run-ends
(where a convergent completes, labeled `a_k`) marked. Confirms the per-step/delta
reading:

- **π−3**: a short cliff then a long flat plateau of near-zero `s_k` (the 292/58
  dwell) — the bracket parked on `355/113` — ending in one drop. Big `a_k` =
  long flat stretch + single cliff.
- **e−2**: periodic cliff+decay blocks of growing length, mirroring CF
  `[1,2,1,1,4,1,1,6,…]`.
- **φ−1**: a perfectly even staircase — constant `s_k`, no plateaus, no spikes.
  The worst-approximable number has *no* delta events. This is the visual
  baseline the spikes are measured against.

## (5) The dark band is a measured fractal — dim_H(E_≤B)

`code/badly_approx_dimension.py` → `code/out/badly_approx_dimension.png`. The exp(2)
dark band is the bounded-type Cantor set `E_≤B = {x : a_k ≤ B ∀k}`. Hausdorff
dimension, two independent ways:

- **Transfer operator** (Ruelle, `(L_s f)(x)=Σ_{a≤B}(a+x)^{-2s}f(1/(a+x))`, `dim = s` with
  leading eigenvalue 1; Chebyshev collocation). **Validation: `dim E_{1,2} = 0.5312805062772`,
  matching the known Jenkinson–Pollicott value to `8e-16`.**
- **Box-counting** (cylinder unions, dyadic boxes) confirms independently: `B=5` gives
  `0.836` vs transfer `0.837`; `B=3` `0.716` vs `0.706`; `B=2` `0.505` vs `0.531` (naive
  box-count undershoots via log corrections — expected).

| B | dim_H(E_≤B) |
|---|---|
| 2 | 0.5312805 |
| 3 | 0.7056609 |
| 5 | 0.8368294 |
| 10 | 0.9257376 |
| →∞ | → 1 (Jarník: badly-approximable set has full dimension) |

So the worst-approximable band has a *measured* fractal dimension at every darkness
threshold B. **Method bridge:** this is the same transfer-operator / thermodynamic-formalism
engine as the Hecke-BCZ ergodic-optimization frontier — dimension is `pressure P(s)=0`;
the ergodic-optimization `X=inf_μ ess-sup_μ P` is the zero-temperature (β→∞, L∞) end of the
*same* Ruelle-operator family. The fractal here and the [[cluster_size_closed_forms]] /
goal-O cusp-escape work are run by one machine.

## Relation to the three-gap theorem

`ThreeGap.lean` (Steinhaus, Liang rigid-gap): the orbit `{0·α},…,{(N−1)·α}` on the circle
cuts it into arcs of **≤3 distinct lengths**, and which lengths occur is governed by the CF
of `α`. It is the *same* cut machinery seen dynamically: feeding the circle one cut-step
at a time, the gap structure stays rigid (≤3 values) precisely because the CF controls the
return times. Three-gap = the gap-length spectrum of the cut's orbit; experiment (1) = the
gap-shrink history of the cut itself.

## Reproduce
```
python3 code/dedekind_cut_explore.py
```

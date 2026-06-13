# Packet for Shin-ya Koyama — BCZ/Hecke results

**Saar Shai · 2026-06-12**

Two deliverables, as requested:

1. **`lean/`** — the Lean proof files: the trace identities behind the Hecke
   extremal-constant family, plus the no-escape / no-ground-state and value
   structure.
2. **`cluster_size/`** — the short write-up of the cluster-size computation at
   the threshold, with the Monte-Carlo cross-check and the code.

---

## 1 · Lean files (`lean/`)

All files were compiled against a clean **Mathlib v4.28.0** (off-drive `/tmp`
build), `lake env lean`, EXIT = 0. Every headline theorem reports
`#print axioms` = `[propext, Classical.choice, Quot.sound]` — **no `sorryAx`**.
Each file is standalone (`import Mathlib`); to check one, drop it into any
Mathlib v4.28.0 project and run `lake env lean <file>.lean`.

### The trace identities (the structural reason for $1/\lambda^3$)

- **`BCZHeckeL2_traceIdentity_allq_VERIFIED.lean`** — the conceptual backbone,
  parametric in $l = \lambda = 2\cos(\pi/q)$, all $q$:
  - `tr_mul_add_tr_mul_adj` — general $\mathrm{SL}_2$ trace identity
    $\operatorname{tr}(XY) + \operatorname{tr}(X\,\mathrm{adj}\,Y) = \operatorname{tr}X\cdot\operatorname{tr}Y$.
  - `adjF_switch_parabolic` — the corridor switch element is **parabolic**
    ($\operatorname{tr} = 2$) for all $k_1,k_2,l$: the reason chains crossing the
    threshold close up.
  - `lam_is_max_elliptic_trace` — $|2\cos\theta| \le \lambda$ on
    $[\pi/q,\pi-\pi/q]$: $\lambda$ is the largest elliptic trace = the slowest
    rotation (the extremal configuration is the $\lambda$-rotation).
  - `rotation_trace_spectrum` — $\operatorname{tr}(R^n) = 2\cos(n\pi/q)$
    (Chebyshev): $\langle R\rangle$ realises exactly the trace spectrum.
- **`HeckeLamBounds_VERIFIED.lean`** — the isolating bound $9/5 < \lambda_q$ for
  all $q\ge 10$ (used to discharge the floor estimates uniformly).

### No escape / no ground state (the "never attained" effect)

- **`BCZHeckeNoInfiniteRotation_allq_VERIFIED.lean`** — `no_infinite_rotation`:
  for $0<l<2$ (every finite Hecke $q$) no positive sequence sustains the
  floor-1 (pure-rotation) recurrence forever. The rigorous $q$-uniform core of
  "a rotation corridor is finite"; the optimum drifts into the cusp and is never
  attained. Includes the conserved quantity
  $E = c_n^2 + c_{n+1}^2 - l\,c_n c_{n+1}$ and `infinitely_many_high_floor`.
- **`BCZHecke_noGroundState_q3q4_VERIFIED.lean`** — the full $q=3$ and $q=4$
  no-ground-state: $\operatorname{ess\,sup}P \ne 2/9$ (resp. $\sqrt2/8$) for
  every invariant probability measure. The infimum is a boundary limit at a
  floor discontinuity, attained by no measure.

### Value structure

- **`BCZHecke_unified_verified.lean`** — the unified "one engine, both Hecke
  constants" theorem: the shared abstract ergodic-optimization principle
  `essSup_ge_of_window` driving both $2/9$ ($q=3$) and $\sqrt2/8$ ($q=4$).
- **`HeckeGeneralLB_VERIFIED.lean`** — `hecke_ground_value_pos`: a uniform
  positive lower bound $X(q) \ge l/(2(1+l)^2) > 0$ for **all** $q$ at once
  (never collapses to 0).
- **`BCZHeckeG5_genuine_VERIFIED.lean`** — the genuine ($q=5$) cusp upper bound:
  the genuine map fixes every cusp point, observable $P = s^2/\varphi$ there with
  $P > 1/\varphi^3 = \sqrt5 - 2$ (strict) and $P \to 1/\varphi^3$ as
  $s\to(1/\varphi)^+$ — value approached but never attained.
- **`BCZHeckeTwoStepKick_q1617_VERIFIED.lean`** — `two_step_kick`: a single
  `nlinarith` over the parameter box covering the non-scalar branches at
  $q=16,17$ (a non-scalar sub-threshold step has an above-threshold successor).

### Scope / honesty notes

- The constant is **$1/\lambda^3 = 1/(2\cos(\pi/q))^3$** for the Hecke family
  ($2/9$ at $q=3$). It is distinct from the Haas–Series Hurwitz constant (which
  stays in $[0.447,0.5]$); these are genuinely new extremal constants.
- The **fully Lean-proven sharp band is $q = 3,4$** (no-ground-state, both
  directions). For $q = 5$ the cusp **upper** bound is machine-checked; the
  matching sharp lower bound is structural/numerical. The trace-identity
  backbone, $\lambda$-extremality, and no-infinite-rotation hold for **all $q$**.
- **Value safety to $q \le 200$** (adversarial min-ess-sup $\ge 1/\lambda^3$,
  ratio $\le 1.00008$, minimiser = cusp word) is a **numerical** certificate, not
  a Lean theorem. I have not included that script here (it was run interactively,
  not committed); happy to send it if useful.

## 2 · Cluster-size write-up (`cluster_size/`)

- `cluster_size_writeup.md` — the note: two exact identities, the Stern–Brocot
  strip decomposition, the $2/45$ tail collapse, the $J_8$ closed form, the
  numerics ($\Pr(L=1) = 0.2273516778\ldots$), and the Monte-Carlo cross-check.
- `cluster_size_distribution_at_threshold.py` — streaming `numba` MC at
  $t = 2/9$ exactly. Run: `python cluster_size_distribution_at_threshold.py`.
- `*_results.json`, `*_results_5e9.json` — the $10^9$ and $5\times10^9$ runs.

Headline: at $t^\*=2/9$, $\Pr(L=1)=0.2273516778\ldots$, $\Pr(L=2)=0.7726\ldots$;
the deep Stern–Brocot tail collapses to the clean rational $2/45$; MC agrees to
$1.4\times10^{-6}$ ($<0.1\sigma$); zero size-$\ge3$ clusters, matching the Lean
size-$\le2$ bound.

# V32 dispatch — the full `(FW)` constant chain over `ℝ`

**Date:** 2026-08-20
**Slot:** `projects/aristotle_dispatch_v32/`
**Status at authoring:** `DRAFT FOR ARISTOTLE — NOT SUBMITTED`. Local syntax
passed against the v26 cache. Every target carries a `sorry` body and is
therefore **CONJECTURAL at the Lean level**. This dispatch machine-verifies
nothing.

This slot does not touch `projects/aristotle_dispatch_v31/`, which is a
refutation slot marked `DO NOT SUBMIT`.

## 1. What this dispatch adds over v30

`projects/aristotle_dispatch_v30/` machine-verified the *finite* ordered-ring
core of `(FW)` (`fw_product_gain`, `fw_product_mono`) plus the typed `(AM)`
decoder. Its "Deliberate exclusions" section names, among others:

* the full `(FW)` estimate
  `A_wrap,q(Y) ≤ 128(1+log 2) · (Y²/q) · (1 + log₊(Y/q))`;
* the `(AM)` atom-moment estimate with constant `2^63`/`2^100`.

V32 states the first of those as an explicit ladder of Lean targets over `ℝ`
with `Real.log`, and states the *stateable part* of the second. It does not
attempt the canonical normal form or Ford counting, which remain excluded
(§5).

## 2. Source ledger and the LEDGER RULE

| Item | Source | Carried status |
|---|---|---|
| `(FW)` boxed bound, `C₁ = 128(1+log 2)`, domain `q ≥ 3`, `Y ≥ q` | `FW_RENEWAL_COUNT_SOL.md:195-473` | **PROVED at paper level** |
| Adversarial confirmation of the above | `FW_REFEREE.md:392-401` | **CONFIRMED — paper-level, not machine-formalized** |
| (1.17) divisor convolution | `FW_RENEWAL_COUNT_SOL.md:424-436`; referee §1(d) | CONFIRMED |
| (1.18) per-block summation | `FW_RENEWAL_COUNT_SOL.md:438-445`; referee §1(d) | CONFIRMED |
| (1.19)–(1.20) `log₊` chain and constant arithmetic | `FW_RENEWAL_COUNT_SOL.md:447-462`; referee §1(d) | CONFIRMED |
| (2.1)–(2.2) weighted consequence | `FW_RENEWAL_COUNT_SOL.md:475-498`; referee §1(e) | CONFIRMED for fixed `σ > 1` |
| `4r` prefix/suffix multiplicity | `FW_RENEWAL_COUNT_SOL.md:322-361` | **CONFIRMED, paper-level dependency** (cusp stabilizer) |
| Ford packing `A(Y) ≤ Y²`, used for `3 ≤ q ≤ 7` | `M2_FORD_PACKING_REFEREE.md:81-118` | **CONFIRMED, paper-level dependency** |
| `(AM)` bound `W_q(Y) < 2^63 Y² Φ_q(Y)` and the `2^100` relaxation | `ATOM_MOMENT_BRIDGE_SOL.md:126-146`; `AM_REFEREE.md:1-22` | **PROVED at paper level; machine formalization open** |

**LEDGER RULE applied.** The Lean file states exactly the confirmed bound and
never a stronger one:

* The conclusion is the displayed **upper** bound. No lower bound is stated.
* No optimality of the logarithm is claimed. `FW_REFEREE.md` §3.3 records
  that log optimality is **open**; the file's docstring repeats this.
* The domain hypothesis is `Y ≥ q`, exactly as in the source; the referee
  §1(d) notes the proof does not extend below it, and neither does the Lean
  statement.
* `(DH)` and full `(RATE)` are not mentioned as provable anywhere. They remain
  **CONJECTURAL / OPEN** (`FW_RENEWAL_COUNT_SOL.md:524-537`,
  `FW_REFEREE.md` §3.5).
* The weighted consequence is stated for a **fixed** `p = 2σ > 2` only. The
  referee §1(e) records that the coefficient diverges as `σ ↓ 1`, so no
  uniform-at-the-endpoint statement is made.
* The two counting inputs the referee flags as *paper-level dependencies*
  (the `4r` multiplicity and the Ford bound) are carried as **explicit Lean
  hypotheses** (`hconv`, `hford`), never asserted. Aristotle is asked to prove
  the analytic chain, not to invent the geometry.

## 3. The ladder — 15 targets in `RateCoreVI.lean`

Locally proved scaffolding (no `(FW)` content, no `sorry`):
`logPlus_nonneg`, `logPlus_eq_log`, `log_two_nonneg`.

| # | Target | Source equation | Difficulty |
|---|---|---|---|
| 1 | `fw_log_halfshift_target` | (1.19) second half | small |
| 2 | `fw_log_absorb_target` | (1.20) | small |
| 3 | `fw_threshold_lower_target` | (1.19) first half, `h-1 ≥ q/4` | small |
| 4 | `fw_triangular_le_sq_target` | (1.17), `1+⋯+m ≤ m²` | small |
| 5 | `fw_harmonic_target` | (1.17), `∑ 1/r ≤ 1 + log N` | medium |
| 6 | `fw_divisor_convolution_target` | (1.17) assembled | medium |
| 7 | `fw_inv_sq_tail_target` | (1.18), `∑_{n≥h} n⁻² ≤ 1/(h-1)` | medium |
| 8 | `fw_renewal_block_sum_target` | (1.18) assembled | medium |
| 9 | `fw_bound_large_q_target` | (1.16)–(1.20), `q ≥ 8` | large |
| 10 | `fw_bound_small_q_target` | Ford patch, `3 ≤ q ≤ 7` | small |
| 11 | `fw_constant_chain_target` | **the boxed `(FW)`** | assembly |
| 12 | `fw_weighted_integral_target` | (2.2) substitution integral | medium |
| 13 | `fw_weighted_consequence_target` | (2.2) | small |
| 14 | `am_regime_one_le_target` | `(AM)` regime factor `Φ_q ≥ 1` | small |
| 15 | `am_constant_relaxation_target` | `2^63 → 2^100` | small |

Rungs 1–8 are self-contained real-analysis facts and are the pieces Aristotle
can most plausibly win outright. Rungs 9–11 are the assembly; 12–13 the
weighted tail; 14–15 the stateable `(AM)` fragment.

### Statement-selection decisions

1. **`A_wrap,q` is a bare real, not a defined counting function.** Defining it
   in Lean would require the theta double-coset type, the canonical normal
   form, and the image characterization — none of which exist in this
   dispatch. Instead `Awrap` is a real number constrained by the two counting
   hypotheses. This is weaker than a definitional statement and therefore
   ledger-safe: proving the target proves the analytic chain and nothing about
   the geometry.
2. **`hconv` encodes (1.15)+(1.16) through summation ranges.** The relaxed
   triple count `2·(4r)·(4s) = 32rs` appears as the literal factor `32`, and
   the product constraint `n r s ≤ Y` appears as the ranges `n ≤ ⌊Y⌋`,
   `r ≤ ⌊Y/n⌋`, `s ≤ ⌊Y/(n r)⌋`. This is a faithful transcription of the
   displayed (1.16), not a reformulation.
3. **`h = ⌈q/2⌉` is spelled `hOf q = (q+1)/2` on `ℕ`.** Natural-number
   division makes this exactly the ceiling for every `q ≥ 0`, avoiding a
   `Nat.ceil` coercion in every statement.
4. **`log₊` is defined as `max (Real.log x) 0`.** Under the hypothesis
   `Y ≥ q` it equals `Real.log (Y/q)`; `logPlus_eq_log` is proved locally so
   Aristotle can move between the two forms without a `sorry`.
5. **The `q ≥ 8` / `q ≤ 7` split is preserved.** The source uses `q ≥ 8` only
   to get `n - 2 ≥ n/2` and `h - 1 ≥ q/4`; the referee §1(c) confirms the
   Ford patch covers `3 ≤ q ≤ 7` for **all** real `Y ≥ q`, not merely a
   finite box. `fw_constant_chain_target` therefore takes both branch inputs
   as guarded hypotheses and covers every `q ≥ 3`.
6. **`(AM)` is only partially stated — see §5.**
7. **The decimal `C₁ = 216.722839111673…`** from `FW_REFEREE.md` §1(d) is
   recorded in a comment as a diagnostic and is used as a hypothesis nowhere.
   `C₁` is defined symbolically as `128 * (1 + Real.log 2)`.

## 4. FALSE-statement escape hatch

If Aristotle finds a requested target false, it must not force an inconsistent
proof. Retain the original only inside a `FALSE AS STATED` comment, prove a
named `<target>_false` negation with an exact witness, then state and prove the
weakest corrected theorem and report the downstream status change. The same
convention as v30.

## 5. Deliberate exclusions

This dispatch does not encode or claim:

* the canonical `R^{a_0} Q ⋯ Q R^{a_k}` normal-form theorem, its endpoint
  conditions, or the strict prefix recurrence `|U_j| > |U_{j-1}|`;
* the exact image characterization `im L_q = {words with all exponents in
  𝒜_q}`, hence the identification of the overflow class;
* the `4r` prefix/suffix multiplicity bound and its cusp-stabilizer input —
  carried as the hypothesis `hconv`, never proved;
* Ford packing `A(Y) ≤ Y²` — carried as the hypothesis `hford`, never proved;
* the rank-one marked-letter factorization `c(P R^a V) = c(PV) + aAB` and the
  product gain `|a||A||B| ≤ Y` at the matrix level (v30 proved only its finite
  ordered-ring shadow, `fw_product_gain`);
* **the `(AM)` summation itself.** `ATOM_MOMENT_BRIDGE_SOL.md` bounds
  `W_q(Y) = ∑_{X ∈ 𝓒_q : x_X ≤ Y} (1 + A_X²)`. The population `𝓒_q`, the
  atom-cost `A_X`, the source-table encoder, and the Ford summation of
  `TWOMARK_RENEWAL_SOL.md` §§3–5 have **no Lean type in this dispatch**.
  V30's `MarkedCode` is a local wire format, not that population; using it
  would misrepresent the claim. Only the regime factor `Φ_q` and the
  `2^63 → 2^100` constant relaxation are stated (targets 14–15). The
  atom-moment estimate itself is **recorded here as an explicit exclusion**
  and remains **CONJECTURAL at the Lean level**;
* `(DH)`, full `(RATE)`, the effective R5 threshold, and any analytic operator
  tail.

All such statements remain paper-level or **CONJECTURAL at the Lean level**
until a returned source is independently rebuilt and audited for `sorry`s and
nonstandard axioms.

## 6. Exact local syntax receipt

The pre-check was run against the v26 cache, not a fresh dependency
environment. No `.lake` directory is created inside `v32`.

Command:

```bash
( cd /Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle && \
  ~/.elan/bin/lake env lean \
  /Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v32/RateCoreVI.lean ); echo "exit=$?"
```

Verbatim output:

```text
/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v32/RateCoreVI.lean:82:8: warning: declaration uses `sorry`
/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v32/RateCoreVI.lean:89:8: warning: declaration uses `sorry`
/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v32/RateCoreVI.lean:95:8: warning: declaration uses `sorry`
/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v32/RateCoreVI.lean:110:8: warning: declaration uses `sorry`
/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v32/RateCoreVI.lean:115:8: warning: declaration uses `sorry`
/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v32/RateCoreVI.lean:121:8: warning: declaration uses `sorry`
/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v32/RateCoreVI.lean:134:8: warning: declaration uses `sorry`
/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v32/RateCoreVI.lean:139:8: warning: declaration uses `sorry`
/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v32/RateCoreVI.lean:161:8: warning: declaration uses `sorry`
/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v32/RateCoreVI.lean:172:8: warning: declaration uses `sorry`
/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v32/RateCoreVI.lean:182:8: warning: declaration uses `sorry`
/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v32/RateCoreVI.lean:200:8: warning: declaration uses `sorry`
/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v32/RateCoreVI.lean:208:8: warning: declaration uses `sorry`
/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v32/RateCoreVI.lean:242:8: warning: declaration uses `sorry`
/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v32/RateCoreVI.lean:249:8: warning: declaration uses `sorry`
exit=0
```

There are no errors and no lint warnings. The fifteen `sorry` warnings are
exactly the fifteen dispatch targets of §3; they are not machine-verified
claims.

## 7. Independent statement audit before submission

Each target was checked by hand against the source equation before the
pre-check was accepted. Spot checks that a reviewer should repeat:

* `fw_bound_small_q_target` is true because `q ≤ 7` gives `C₁/q ≥ C₁/7 > 1`
  and `1 + log₊(Y/q) ≥ 1`, so `Y² ≤ C₁ Y²/q (1 + log₊(Y/q))`. This reproduces
  `FW_RENEWAL_COUNT_SOL.md:464-472`, where the source uses the weaker constant
  `7 < C₁`.
* `fw_threshold_lower_target` is true because `hOf q ≥ q/2`, so
  `hOf q - 1 ≥ q/2 - 1 ≥ q/4` exactly when `q ≥ 4`; the hypothesis `q ≥ 8` is
  strictly stronger, matching (1.19).
* `fw_divisor_convolution_target` is tight at `T = 1` (both sides equal `1`),
  so the statement is not accidentally vacuous or accidentally false at the
  boundary of its domain.
* `fw_weighted_integral_target`: `∫_q^∞ t^{1-p}(1+log(t/q)) dt`, substituting
  `t = qu`, equals `q^{2-p} ∫_1^∞ u^{1-p}(1+log u) du =
  q^{2-p}(1/(p-2) + 1/(p-2)²)`. Composing with `hlayer` gives the
  `p C₁ q^{1-p}` coefficient of (2.2) exactly.
* `am_constant_relaxation_target` is sound because `am_regime_one_le_target`
  gives `Φ_q ≥ 1 > 0`, so `2^63 · Y²Φ ≤ 2^100 · Y²Φ`.

## 8. Dispatch command — NOT RUN

This slot is a draft. Nothing was submitted to Aristotle and nothing was
committed. If a future orchestrator submits, the v30 convention applies:
credentials are sourced from `~/.farey_api_keys` without printing, and every
CLI stream is sanitized through `grep -iv key`.

```bash
# NOT RUN in this session.
set -a; source ~/.farey_api_keys; set +a
aristotle submit \
  --project-dir /Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v32 \
  'Prove the targets in RateCoreVI.lean. Work up the ladder: the log-plus helpers (fw_log_halfshift_target, fw_log_absorb_target, fw_threshold_lower_target), then the divisor convolution (fw_triangular_le_sq_target, fw_harmonic_target, fw_divisor_convolution_target), then the per-renewal-block sum (fw_inv_sq_tail_target, fw_renewal_block_sum_target), then the assembly (fw_bound_large_q_target, fw_bound_small_q_target, fw_constant_chain_target), then the weighted tail and the AM fragment. Partial credit is wanted: prove as many rungs as possible rather than only attempting the top. Do not weaken or strengthen any statement. Do not prove the counting hypotheses hconv/hford - they are deliberate paper-level imports. If a target is false, use the FALSE AS STATED escape hatch: give a counterexample and the weakest corrected theorem. Return Lean source suitable for an independent v26-cache rebuild; introduce no axioms and leave no sorrys in results you claim proved.' \
  2>&1 | grep -iv key
```

## 9. Harvest and independent rebuild (for whoever submits)

Harvest only Lean source and non-cache metadata under `result/`; exclude
`.lake`, caches, worktrees, and archives. The orchestrator must independently
run the returned source against the v26 cache, quote the exact exit output,
search the returned source for actual `sorry` and `axiom` declarations, stream
`#print axioms` for every target, and record each target as `PROVED`,
`REFUTED`, or still `OPEN`. Statement preservation must be diffed
target-by-target against this file: a returned theorem with a weakened
hypothesis or a strengthened conclusion is a defect, not a win. No returned
file is promoted until this rebuild succeeds **and** a separate cold
adversarial `V32_REFEREE.md` has reviewed any proof-status upgrade.

## 10. Verification checklist

```text
( cd /Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle && \
  ~/.elan/bin/lake env lean \
  /Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v32/RateCoreVI.lean )
rg -n "sorry|axiom|CONJECTURAL|paper-level|escape" projects/aristotle_dispatch_v32
find projects/aristotle_dispatch_v32 -name '.lake' -o -name '*.olean'
git diff --check -- projects/aristotle_dispatch_v32
rg -n -i "api[_-]?key|authorization|bearer|token" projects/aristotle_dispatch_v32
```

The secret scan must print only names and locations, never values. Any
key-like value in output or in a written file is a hard failure.

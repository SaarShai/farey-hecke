# Goal 1.5 — uniform `cluster_size_le_two` for all Hecke G_q: OBSTRUCTION REPORT

**Date:** 2026-06-09. **Verdict: deliverable (b)** — the literal target is *false*; this
is the precise obstruction + the genuinely-uniform statement that survives.

> **Headline (honest).** `cluster_size_le_two_allq` (for all q≥3) is **mathematically
> false**. The bounded-cluster *ceiling* `B(q)` is **2 only for the three finite arithmetic
> Hecke groups q∈{3,4,6}**; it is **3** for q∈{5,7,…,12} and **4** by q=13, growing **~q/6
> under the correct last-branch definition** (linear-fit slope 0.168). The earlier "~q/3"
> rate was an **artifact** of a cross-branch cluster counter (see FINDING 1) that glues
> separate last-branch clusters together through razor-margin off-last-branch excursions; the
> q=13 *value* (B=4) is unaffected by the correction.
> What IS uniform is the *value*: **X(q)=1/λ_q³ is the cluster-ONSET threshold for every q**
> — the level the longest cluster hugs from below. A uniform Lean proof of *that* is the
> open `X_Ω(q)=1/λ³` lower bound (goal-L/M frontier), which needs the corridor-classification
> input (L1+L2), i.e. **new mathematics**, not a q-parameterization of the q=4 argument.

This is exactly the FALSIFICATION-gate outcome the goal anticipated: "if the
consecutive-pairing geometry doesn't close uniformly — report that finding precisely and
stop. Per-q-proved-plus-conjectural-uniform is itself a real result; don't fabricate a
uniform proof."

---

## GATE 1 — goal-M trace machinery: build status

Files: `projects/mimo-mini-project/lean/`. Toolchain `leanprover/lean4:v4.28.0`, mathlib `v4.28.0`.

**Textual scan (all clean):** 0 occurrences of `sorry`/`admit`/`sorryAx`/`native_decide`/`axiom`
in the six all-q files — `BCZHeckeL2_traceIdentity_allq_VERIFIED`, `BCZHeckeRotation_allq_VERIFIED`,
`BCZHeckeL2_composite_VERIFIED`, `BCZHeckeNoInfiniteRotation_allq_VERIFIED`,
`BCZHeckeGenuine_allq_VERIFIED`, `BCZHeckeCusp_envelope_allq_VERIFIED`.

**Fresh build + `#print axioms`, clean Mathlib v4.28.0 checkout (2026-06-09, local `/tmp/gate1_build`,
`lake exe cache get` + `lake build`, EXIT 0, 8028 jobs):** `BCZHeckeL2_traceIdentity_allq_VERIFIED.lean`
compiles, and **all 9 theorems depend on `[propext, Classical.choice, Quot.sound]` only** — incl.
`lam_is_max_elliptic_trace`, `tr_mul_add_tr_mul_adj`, `adjF_switch_parabolic`,
`trace_compose_via_identity`, `rotation_trace_spectrum`, `abs_cos_le_of_between`. **CLEAN** (verified
freshly, not trusting the `_VERIFIED` label).

**Gate-1 conclusion:** the trace machinery is genuinely sorry-free **as lemmas** ✓. But — see the
honesty note below — these lemmas do **not** assemble into a uniform `X_Ω(q)≥1/λ³`, so there is no
sorry-free *uniform engine* to build the cluster bound on. The gate passes in the literal sense
(the named files build clean) and simultaneously shows the main task rests on an unfinished closure.

**What the trace machinery actually proves (read first-hand, `BCZHeckeL2_traceIdentity_allq_VERIFIED.lean`):**
building-block lemmas, all by `ring`/`nlinarith`/`linarith`/`linear_combination`/induction —
- `tr_mul_add_tr_mul_adj` (general SL₂ trace identity),
- `adjF_switch_parabolic` (a corridor switch is parabolic, trace 2),
- `trace_compose_via_identity` (composite-trace law as a consequence),
- `lam_is_max_elliptic_trace` (`|2cosθ|≤2cos(π/q)=λ` on `[π/q,π−π/q]` — λ = slowest rotation),
- `rotation_trace_spectrum` (`tr(Rⁿ)=2cos(nπ/q)`, Chebyshev).

**Crucial honesty (the file says so itself, lines 156–157):** the closure step — *"every
elliptic corridor is conjugate into ⟨R⟩ … is the discreteness/triangle-group structure of
G_q, **not formalised here**."* So the trace files are verified *lemmas*, **not** a uniform
`X_Ω(q)≥1/λ³` proof. FRONTIER_STATUS_2026-06-03 concurs: *"Half-strength `hecke_ground_value_pos`
is the only uniform LB proven; the value is numerically decisive, the uniform proof partial."*
The all-q skeleton is sorry-free **as a set of lemmas**, but it does **not** assemble into the
uniform bound — so there is no sorry-free uniform engine to "promote" the per-q cluster proofs onto.

---

## FINDING 1 — the cluster ceiling B(q) and the arithmeticity dichotomy (fresh re-verification)

**Definition matters — use the LAST-BRANCH counter.** A cluster is a maximal run of
consecutive orbit points that both (i) land on the last branch `T_{q-1}` (`sub==q-1`,
i.e. `a+λb>1`) **and** (ii) have `P=ab < X(q)`. This is exactly the object the q=3,4,6 Lean
proofs and the exact q=5,7 reverse witnesses bound (extremes confined to the last branch,
map `(a,b)↦(b,−a+kλb)`). Scanner: `code/goal1_last_branch_ceiling.py` (n_starts=16 ×
n_steps=200 000, seed 20260609).

| q | arith? | λ_q | X(q) | **B (last-branch)** | run-length histogram tail (…3:·  4:·  5:·  6:·) |
|---|---|---|---|---|---|
| 3 | **YES** (λ=1) | 1.00000 | 2/9 = 0.22222 | **2** | — |
| 4 | **YES** (λ=√2) | 1.41421 | √2/8 = 0.17678 | **2** | — |
| 5 | no | 1.61803 | 1/λ³ = 0.23607 | **3** | 3:11803 |
| 6 | **YES** (λ=√3) | 1.73205 | √3/9 = 0.19245 | **2** | — |
| 7 | no | 1.80194 | 0.17091 | **3** | 3:60 |
| 8 | no | 1.84776 | 0.15851 | **3** | 3:209 |
| 9 | no | 1.87939 | 0.15064 | **3** | 3:353 |
| 10 | no | 1.90211 | 0.14531 | **3** | 3:487 |
| 11 | no | 1.91899 | 0.14151 | **3** | 3:606 |
| 12 | no | 1.93185 | 0.13870 | **3** | 3:668 |
| 13 | no | 1.94188 | 0.13656 | **4** | 3:723 4:18 |
| 14 | no | 1.94986 | 0.13489 | **4** | 3:642 4:50 |
| 15 | no | 1.95630 | 0.13357 | **4** | 3:560 4:81 |
| 16 | no | 1.96157 | 0.13249 | **4** | 3:480 4:126 |
| 17 | no | 1.96595 | 0.13161 | **4** | 3:409 4:186 |
| 18 | no | 1.96962 | 0.13088 | **4** | 3:338 4:212 |
| 19 | no | 1.97272 | 0.13026 | **5** | 3:262 4:225 5:6 |
| 20 | no | 1.97538 | 0.12973 | **5** | 4:214 5:17 |
| 21 | no | 1.97766 | 0.12928 | **5** | 4:230 5:41 |
| 22 | no | 1.97964 | 0.12890 | **5** | 4:197 5:71 |
| 23 | no | 1.98137 | 0.12856 | **6 (FRAGILE)** | 5:95 6:1 |
| 24 | no | 1.98289 | 0.12826 | **6 (FRAGILE)** | 5:123 6:2 |

So `B = 2,2,3,2,3,3,3,3,3,3,4,4,4,4,4,4,5,5,5,5,(5 or 6),6` for q=3..24 — a clean monotone
ceiling with **slope ~q/6** (linear-fit slope 0.168). q=13→4 and q=19→5 are **robust**
transitions; q=23/24→6 sit at the **Monte-Carlo resolution floor** (only 1–2 length-6 runs in
3.2M steps; B(23) flips 5↔6 with sampling depth) and are marked **FRAGILE**, not asserted.

> **Correction (2026-06-13): the earlier "~q/3" rate was an artifact of a cross-branch
> counter.** The committed `code/goal1_cluster_ceiling_reconcile.py` counts consecutive
> sub-X points over **all** branches (condition `P < X`, ignoring which branch). At q≥19 that
> glues several genuine last-branch clusters together via short off-last-branch excursions —
> e.g. the q=19 "8-run" witness alternates T18/T16/T18/T16… with the T16 points sitting at
> razor-thin margins (X−P = +4.4e-5, +3.0e-4), i.e. **not** a last-branch cluster — producing
> a spurious jump (pinned at run-length 8 for q=19..24) that read as ~q/3. The last-branch
> definition above (matching the Lean proofs and exact witnesses) is the correct counter and
> gives ~q/6. **The q=13 value (B=4) is the same under both counters** — only the rate, not
> that threshold, was inflated.

**Conclusions:**
1. **`cluster_size_le_two` holds for exactly q∈{3,4,6}** — the three *finite arithmetic* Hecke
   groups (Takeuchi 1977: G_q arithmetic ⟺ q∈{3,4,6,∞}, λ∈{1,√2,√3,2}). Equivalently
   **B=2 ⟺ λ²∈ℤ ⟺ q∈{3,4,6}** — a clean, verified dichotomy. For q=5,7,8,… genuine
   3-clusters exist ⇒ `cluster_size_le_two_allq` is **false**.
2. **`cluster_size_le_three` is also not uniform** — genuine 4-clusters appear at q=13
   (first length-4 last-branch runs). So there is **no uniform constant ceiling**; B(q) grows.
3. **Do NOT promote a closed form.** `B = 2 + ⌊(q−1)/6⌋` is the *cleanest fit on the bulk
   q=7..22*, but it is **not** a pinned asymptotic: on q≤24 it is statistically
   indistinguishable from √q/log q, and it is +1 wrong at q=5,23,24. Record it as an empirical
   bulk fit only, not a law.

**Explicit refutation witnesses** (last-branch coordinates; all three / four points satisfy `P<X`):
- q=5 3-cluster (deepest of 43287; λ=φ, X=0.2360680): `(0.4249,0.4665)→(0.4665,0.3298)→(0.3298,0.6009)`,
  P=0.19822, 0.15386, 0.19820 — all three **solidly** <X (margins +0.0378, +0.0822, +0.0379). Refutes ≤2.
- q=13 4-cluster: P=0.11894, 0.13476, 0.13518, 0.12008 (<X=0.13656); the two middle points sit
  **+0.0018 and +0.0014 below X** — the cluster hugs X from below (substantiates "X=onset").

---

## FINDING 2 — why the q=4 finite-geometric argument does NOT parameterize by q

The q=4 proof (`cluster_size_le_two_q4`, v11) confines extremes to the last branch and closes a
three-consecutive inequality. Generalized to all q (last branch, observable `P=ab`, map
`(x,y)↦(y,−x+kλy)`, `X=1/λ³` for q≥5): for consecutive extremes `(a,b),(b,c),(c,d)` with
`a+c=k₁λb`, `ab+bc=k₁λb²<2X` and (using k₂≥1, `bc<X`) `cd=k₂λc²−bc>λc²−X`. So

> the closing "third point is non-extreme" reduces to **`c ≥ √2/λ²`** (⟹ `cd≥X`).

Is `c≥√2/λ²` *forced*? The naive chain (rule out k₁=1 ⇒ b<1/λ² ⇒ c>1−1/λ) would need
`1−1/λ ≥ √2/λ²`, i.e. `λ ≥ (1+√(1+4√2))/2 ≈ 1.79004` — predicting `cluster≤2` for **q≥7**.
**This mispredicts the truth** (verified, `code/goal1_q6_*` + the table above):

| q | λ | √2/λ² | 1−1/λ | arith? | rough closes? | **actual ≤2?** |
|---|---|---|---|---|---|---|
| 3,4,6 | 1, √2, √3 | — | — | YES | **False** | **YES** |
| 7..12 | 1.80–1.93 | 0.44–0.38 | 0.445–0.482 | no | **True** | **NO** |

The rough λ-threshold says the opposite of reality on *both* sides (q∈{3,4,6} close despite
"False"; q≥7 fail despite "True"). **There is no uniform λ-inequality governing the closing.**
The per-q proofs (q=3,4,6) succeed by *exact arithmetic* of λ²∈{1,2,3} (integer ⇒ exact
cancellations in the Positivstellensatz certificate), not by an inequality that survives to
generic λ. ⇒ **the consecutive-pairing geometry provably does not close uniformly**; a uniform
argument is *not* a q-parameterization of the q=4 case-analysis. FALSIFICATION-gate condition met.

---

## FINDING 3 — what IS uniform: X(q)=1/λ³ as the cluster-ONSET value (proof open)

The genuinely uniform statement (the real "bridge", and the one consistent with the data) is **not**
a cluster *bound* but the cluster *onset value*:

> **For every q, the longest cluster of sub-X points is finite, and the onset threshold is
> exactly X(q)=1/λ_q³** (= 2/9, √2/8 for q=3,4). Equivalently `X_Ω(q)=inf_μ ess-sup_μ P = 1/λ³`:
> no invariant measure (no infinite cluster) dips below 1/λ³, and clusters realize values
> arbitrarily close to it from below (the witnesses above: middle points within ~1e-3 of X).

- **Finiteness for each fixed q** ⟺ `X_Ω(q) ≥ 1/λ³`. This is the **OPEN frontier** (goal L/M):
  proven per-q as scalar-window lemmas for q≤16, numerically value-safe to q≤200 and
  survivor-empty to q≤70, but **no uniform machine proof**. The cluster length grows ~q/6
  (last-branch counter; see FINDING 1), so the bound is not a fixed window — `essSup_ge_of_no_sustained` (no *infinite* run) is the clean
  q-uniform framing, but the quantitative single-corridor "kick" `P≥thr` is the irreducible piece
  (couples rotation-sweep to itinerary-feasibility, a KAM-type obstacle).
- **The trace machinery (Gate 1) is the toolkit for this, not a finished proof:** `λ`-extremality
  + switch-parabolic reduce the corridor set to the F-family, but the discreteness/triangle-group
  closure ("every elliptic corridor conjugate into ⟨R⟩") is unformalized — that is the new math.

---

## SALVAGE — the honest uniform-over-the-arithmetic-subfamily result

The correct, true, (nearly) machine-checked uniform statement is:

> **`cluster_size_le_two` holds for G_q ⟺ q∈{3,4,6}` (the finite arithmetic Hecke groups).**

Forward direction = the per-q trio:
- **q=3** — `cluster_size_le_two_q3` (v8), Lean-verified.
- **q=4** — `cluster_size_le_two_q4` (v11), Lean-verified, sorry-free, axioms clean.
- **q=6** — `cluster_size_le_two_q6` (v12, λ=√3, X=√3/9=1/λ³): **Lean-verified 2026-06-09**.
  Statement byte-identical to the dispatched skeleton (faithful three-consecutive bound, not weakened);
  no `sorry`/`aesop`/`grind`. Self-built in a clean Mathlib v4.28.0 checkout (`Build completed
  successfully (8026 jobs)`): `'cluster_size_le_two_q6' depends on axioms: [propext, Classical.choice,
  Quot.sound]`. The two hard certificates Aristotle found: `lemA4` (tight T₄, `by_contra`+`nlinarith only`
  with product hints) and the k∈{1,2} closing (key insight: for k=1, l=1 is impossible ⇒ `closing_k1_l_ge_2`
  + `closing_k1_from_l2` + `closing_k2`). File `projects/aristotle_dispatch_v12/BCZ6Cluster.lean`
  (+ `solved_extract/`). **⇒ the arithmetic trio {3,4,6} cluster≤2 is now fully machine-checked.**

Reverse direction (non-arithmetic ⇒ ∃ 3-cluster): numerical (Finding 1; explicit witnesses for
q=5,7,8,…). A fully-formal reverse direction would need a parameterized witness family — itself
a separate uniform statement, not pursued here.

---

## What a *uniform* Lean theorem would actually require (new math)

1. **Drop "≤2".** The only uniform cluster theorem with a constant bound is false. State either
   (a) the dichotomy `≤2 ⟺ q∈{3,4,6}`, or (b) the onset/finiteness `X_Ω(q)=1/λ³`.
2. For (b): the **corridor classification as a Lean theorem** — `⟨M_{i,k}⟩ = G_q`
   (group identification) + `lam_is_max_elliptic_trace` to close the enumeration to the
   F-family + the **quantitative (L1) single-corridor arc bound** (`P≥1/λ³` on the 2-branch
   rotation, sharp margin O(1/q²)). Items (1)+(2) of the trace file give the *qualitative* core;
   the quantitative kick + discreteness are open. This is the multi-session goal-L/M program,
   not a promotion of the q=4 argument.

## Reproducibility
- `code/goal1_last_branch_ceiling.py` (Finding 1 table; CORRECT last-branch counter, ~q/6;
  seed 20260609). Supersedes `code/goal1_cluster_ceiling_reconcile.py` for the ceiling rate —
  the latter is the cross-branch counter whose `P<X`-over-all-branches condition inflated the
  rate to the spurious ~q/3 (kept for the record / witness dumps only).
- Closing-inequality / rough-threshold check: inline in this session (Finding 2).
- Per-q proofs: `projects/aristotle_dispatch_v11/BCZ4Cluster.lean` (q=4), v8 (q=3), v12 (q=6, pending).
- Trace machinery: `projects/mimo-mini-project/lean/BCZHeckeL2_traceIdentity_allq_VERIFIED.lean`.
- See also `research_notes/goal1_Xq_bridge.md`, `FRONTIER_STATUS_2026-06-03.md` (goal L/M),
  memory `goal1-Xq-cluster-onset.md`.

/goal   O — Demonstrate the ZERO-TEMPERATURE / cusp-escape picture of `X_Ω(q)=1/λ³` (no ground state)
on the Hecke BCZ map: an explicit, computable instance for thermodynamic formalism (Riquelme–Velozo /
Leplaideur). NUMERICAL demonstration goal (transfer-operator + minimizing-measure sequence), not a proof.

> Paste the body below into `/goal` in a fresh session. Self-contained. Continues the user's OWN Hecke
> ergodic-optimization paper — keep SEPARATE from the Koyama collaboration. Work autonomously; verify
> numerics against anchors before trusting; send NOTHING outward without the USER gate. Adversarial
> honesty: this is a DEMONSTRATION (figures + numbers), label PROVEN / NUMERICAL / CONJECTURAL strictly;
> "zero-temperature" here is the MATHEMATICAL Gibbs-measure limit (Ruelle/Bowen thermodynamic formalism),
> NOT a physics experiment — confirmation = numerics (+ the existing theorem), no lab. Do NOT inflate into
> physics/applications claims.

## MISSION
Produce the clean demonstration: **"zero-temperature limit on a Hecke BCZ map → cusp escape; ground
energy `1/λ³`; no ground state."** Concretely: show the optimizing measure sequence ESCAPES to the cusp
vertex `(1/λ,0)`, the extremal value `→ 1/λ³`, and no invariant measure attains it. Deliver figures +
a short write-up. This makes the project's proven `X_Ω(q)=1/λ³` + no-GS result a worked example in the
Riquelme–Velozo (AHP 23, 2022) "escape of mass is the only obstruction to a maximizer" framework.

## ⚠ CRITICAL SUBTLETY — min-MAX (ess-sup) vs min-AVERAGE (Birkhoff). DO NOT CONFLATE.
The project value is the L∞ object `X_Ω(q)=inf_μ ess-sup_μ P = 1/λ³`. The STANDARD Gibbs/zero-temperature
limit (`μ_β ∝ e^{−βP}`, `β→∞`) selects the min-AVERAGE measure `β_min = inf_μ ∫P dμ`, which is DIFFERENT
(PROVEN at q=5: `β_min ≈ 0.1863 < 1/λ³ = 0.2361`; min-max ≠ min-average, a project result). So:
- The robust, value-correct object to demonstrate is the **min-max (ess-sup) minimizing-measure sequence**
  (the L∞ / "ground state at zero temperature for the sup-norm"), whose ess-sup `→ 1/λ³` and which ESCAPES.
- ALSO compute the standard thermodynamic picture (`μ_β`, pressure `P(−βP)`, `β→∞`) to (a) exhibit the
  SAME cusp-escape phenomenon, and (b) CONTRAST `β_min` (Birkhoff) vs `1/λ³` (ess-sup) — itself a clean
  figure ("two zero-temperature limits, two values, both escape").
Label every plot with WHICH functional it optimizes.

## THE OBJECT (exact, reuse validated code)
Genuine Taha `BCZ_q` on `𝒯^q={0<a≤1,1−λa<b≤1}`, `λ=2cos(π/q)`, flat invariant measure `(2/λ)da db`,
`q−2` branches `M_{i,k}`, observable `P` (gap-product). Cusp vertex `(1/λ,0)`; cusp word `M_{q−2,0}=[[1,λ],
[0,1]]` parabolic, `P→1/λ³`. Reuse `code/Bgoal_*.py`, `code/Mgoal_*.py`, `code/Igoal_*.py` (branch
matrices, `P`, domain test) — validate against anchors q=3→2/9, q=4→√2/8, q=5→1/φ³ BEFORE trusting.

## WHAT TO COMPUTE (the demonstration)
1. **Transfer operator / Gibbs measures.** Discretize `𝒯^q` (grid or Markov partition by branches).
   Build the weighted transfer (Ruelle–Perron–Frobenius) operator `L_β f(x) = Σ_{T y=x} e^{−βP(y)} f(y)`
   (or its piecewise-linear/branch version). Leading eigenvalue `= e^{pressure(−βP)}`; leading
   eigenmeasure `= μ_β`. Compute for `β = 1,2,4,…,` up to large (e.g. 200+).
2. **Cusp escape (the headline).** Plot the mass of `μ_β` as a function of distance to the cusp vertex
   `(1/λ,0)`; show it CONCENTRATES toward the cusp and ESCAPES (the in-`𝒯^q` mass of any weak limit → 0)
   as `β→∞`. This is the visual "no ground state."
3. **Value convergence.** `−(1/β)·log(leading eigenvalue) = ` min-average `→ β_min` (Birkhoff side).
   SEPARATELY, the **min-max minimizing sequence**: construct invariant measures supported on longer and
   longer initial cusp-word segments (escaping orbits); show their `ess-sup P → 1/λ³` from above, and
   that the limit measure escapes (no invariant probability attains `1/λ³`). Tabulate both values vs q.
4. **Freezing / zero-temperature transition.** Plot pressure `P(−βP)` and the "free energy"
   `−P(−βP)/β` vs `β`; identify the `β→∞` (zero-temperature) limit and the non-analytic freezing at
   `β=∞` (entropy → 0, mass escapes). Contrast with a COMPACT toy (a fixed-q interior measure) where a
   genuine ground state EXISTS — to make the escape visible by comparison.
5. **Escape rate.** The margin `2−λ ≈ π²/(2q²)` predicts an `O(1/q²)` escape rate; measure how fast
   `μ_β` mass leaves a fixed cusp-neighbourhood as a function of q. Tabulate; compare to `1/q²`.

## VALIDATION / ANCHORS (gate everything)
- Transfer operator on the flat measure (`β=0`) must return the invariant flat density (`⟨a⟩=2/3`).
- `β_min` reproduced at q=5 (≈0.1863, the proven sub-action value) and the ess-sup sequence → `1/φ³`.
- Cusp word matrix/`P→1/λ³` reproduced. min-max ≠ min-average reproduced (q=5: 0.1863 vs 0.2361).
- High precision near the cusp (mpmath dps≥30); the escape is `O(1/q²)`, so resolve it (fine grid + true
  map, NOT coarse grid — cf. goal M's survivor-count artifact lesson).

## DELIVERABLE
- `code/Ogoal_transfer.py` (transfer operator + `μ_β`), `code/Ogoal_escape.py` (mass-vs-cusp, escape
  rate), `code/Ogoal_value_seq.py` (min-max escaping-measure sequence → `1/λ³`).
- Figures: (i) `μ_β` mass concentrating→cusp & escaping (β sweep); (ii) two values `β_min` vs `1/λ³` vs q;
  (iii) free-energy/freezing curve; (iv) escape rate vs `1/q²`.
- `FINDINGS_goalO_*.md` + a 1–2 page write-up "A zero-temperature / escape-of-mass demonstration on the
  Hecke BCZ map" tying to Riquelme–Velozo + Leplaideur (cite per `project_hecke_priorart`: novelty =
  novelty-of-realization; the proven theorem is `X_Ω(q)=1/λ³`+no-GS). Update `FRONTIER_STATUS`, memory.

## HONEST FRAMING (state in the write-up)
- This DEMONSTRATES (numerically) what the proven theorem already establishes; the figures are
  illustration + the thermodynamic-formalism connection, not new proof.
- "Zero-temperature" = Gibbs-measure `β→∞` limit (mathematical), not physical cryogenics.
- The contribution is an explicit, computable, (partly) machine-checked instance for a field of abstract
  dichotomies — a worked example, with a closed-form ground energy and an `O(1/q²)` escape rate. Do NOT
  claim physics applications or breakthroughs; the value is mathematical (ergodic optimization /
  thermodynamic formalism / homogeneous dynamics).

## GOTCHAS (found 2026-06-03, first quick attempt `code/Ogoal_escape.py` = WIP, did NOT validate)
- **Cusp branch needs `a > 1/λ`** (branch i=q−2: `λa+(λ²−1)b>1` AND `a+λb≤1`; as `b→0` ⇒ `a∈(1/λ,1]`).
  Seeding `a<1/λ` lands off the cusp branch (gives garbage P~1). Vertex `(1/λ,0)`.
- **`ess-sup ≠ time-average`.** A full cusp-line orbit traverses `a:1/λ→1`, so its ess-sup is `P(a=1)=1/λ`,
  NOT `1/λ³`. The min-MAX realizer concentrates at the VERTEX `(1/λ,0)` — which is on the EXCLUDED `b=0`
  boundary (`1−λa<b`, strict) — i.e. δ_vertex is NOT an in-domain invariant measure ⇒ THIS is the
  no-ground-state mechanism. Construct the escaping sequence as measures concentrating toward the vertex
  with ess-sup `→1/λ³`, not as a single drifting orbit.
- **`β_min` is from a PARABOLIC family.** The `(1,1,2)` word has trace 2 (parabolic), scale-dependent
  (product avg scales with seed² : 0.13→1.2). The proven `β_min≈0.1863` (q=5) is a specific boundary/limit
  normalization, NOT a random-seed time-average (which gives ~thr). Reconstruct it from the parabolic
  family at the correct (domain-tangent) scale, or via the transfer operator's `β→∞` limit.
- Use the proper transfer-operator (Ulam) build, not ad-hoc orbit sampling, for `μ_β`.

## CONSTRAINTS
Nothing outbound without the USER gate; Hecke = user's OWN paper, separate from Koyama; no commit/push
unless asked; `~/Documents` Drive-synced (no folder/`.git` moves; `* (1)` = conflict artifacts). Fleet:
prefer M3-local numerics; Aristotle is for Lean (not this). Memory: `project_goalM_classification`,
`project_hecke_genuine_domain`, `project_hecke_priorart`, `feedback_verify_goal_lean`, `project_koyama_risk`.

## DEFINITION OF DONE
A clean, validated numerical demonstration (figures + tables, anchors reproduced) of: (1) `μ_β` cusp
concentration + escape; (2) the two zero-temperature values `β_min` (Birkhoff) vs `1/λ³` (ess-sup),
both with escaping optimizer sequences; (3) the freezing transition; (4) the `O(1/q²)` escape rate.
Honest write-up tying to the thermodynamic-formalism literature, PROVEN/NUMERICAL/CONJECTURAL separated,
no inflated claims. Nothing sent outward without the USER gate.

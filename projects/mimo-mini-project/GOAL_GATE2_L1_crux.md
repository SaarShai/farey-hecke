# GOAL — GATE 2 crux (L1): uniform corridor-escape with the O(1/q²) margin

**This is the single open step between the current state and genuine `X_Ω(q)=1/λ³` for q≥18.**
Everything around it is done or numerically certain. Read `FINDINGS_GATE2_probes_2026-06-03.md`
and memory `project_goalI_L2_refutation_survived.md` first. HARD RULE: re-compile any Lean.
Nothing outward (Hecke = user's OWN paper). PROVEN / NUMERICAL / OPEN kept separate.

## State (what is settled)
- **Value certain:** no sub-threshold invariant set; re-verified q=60,70 by TRUE-MAP escape
  (17848 seeds, max dwell ≤15, 0 trapped). Cheap tests (eps-closure, grid survivor) FALSE-POSITIVE
  at large q — use true-map escape only.
- **Mechanism (confirmed):** sustained sub-threshold motion = the elliptic corridor word
  `W_q=(q−1,3)(q−1,0)(q−3,0)`, monodromy **trace = λ exactly ∀q** ⇒ rotation by **π/q**,
  near-period **2q**, through the **2-branch corridor {q−1, q−3}**. Finite dwell ~q/4..q/5, escapes.
- **Area-preserving:** det DT = X(i)²−X(i−1)X(i+1) = 1 (Casorati). KAM-wall source; no soft argument.
- **(L2) PROVEN all q (F-family), Lean `BCZHeckeL2_composite_VERIFIED`:** any branch/floor SWITCH
  ⇒ |trace|≥2 (parabolic/hyperbolic) ⇒ expansion. So sustained sub-thr ⇒ stay in ONE corridor.
- **Bedrock (Aristotle d5e000f9, pending):** casorati det=1 + two-generator trace classification.

## (L1) — the open crux, stated sharply
Staying in one corridor = iterating the elliptic rotation `R=W_q` (angle θ=π/q). The sub-threshold
∩ in-domain region is a bounded **angular arc** of the rotation. (L1) =
> **the sub-threshold arc width `Δ(q)` satisfies `Δ(q) < (escape angle)` with a margin, uniformly
> in q**, i.e. no full rotation-period stays sub-threshold ⇒ dwell `≈ Δ(q)/θ` is finite and the
> max product over the arc reaches `1/λ³`.

Equivalent closed-form target (scalar analog already done in goal-N): with the rotation
`c_n=r·cos(nθ−ψ)`, product `p_n=(r²/2)[λ/2+cos((2n+1)θ−2ψ)]`, domain
`c_n+λc_{n+1}=r√(1+2λ²)cos(nθ−ψ+δ)`, prove the genuine **corridor** version of
`g_closed(L,q)≥1/λ³` at `L=⌈arc⌉` — an explicit trig inequality, uniform in q, with the binding
**margin shrinking like O(1/q²)** (goal-O; this vanishing margin is exactly what makes it hard and
what fools the cheap numeric tests).

## Why it is hard (honest)
θ=π/q→0 as q→∞: the rotation slows, the arc and the escape angle both →0, and their **difference is
O(1/q²)** — so the inequality is true but by a vanishing margin. A crude bound (mean-value, or
`|Σcos|≤|sin Lθ/sinθ|`) gives a margin of the wrong order and FAILS. Needs the sharp `max cos` form
+ careful uniform control of the arc endpoints. This is analysis, **not** an ATP search target
(route-4 Aristotle 9.5h did not crack the q≥18 statement). ATP CAN do the per-q instances.

## Attack plan (two sub-targets)
**(L1a) per-q corridor-escape certs, q=18..30 — ATP/emitter-tractable (extends proven band).**
For each q: the genuine corridor word has a fixed itinerary; "no sub-threshold full arc" is a finite
2-variable semialgebraic emptiness in (a,b) over ℚ(λ) — the goal-L window shape but on the genuine
2-branch corridor (not the scalar reduction, which fails q≥16). Emit per-q Positivstellensatz certs
(adapt `code/Lgoal_buildcore.py` to the corridor itinerary; reuse the verified W=6 machinery). Each
verified q extends the genuine band past 17 concretely. STAGE for Aristotle.

**(L1b) uniform trig inequality — human-analytic (the actual theorem).**
1. Derive the genuine corridor closed forms (the W_q-rotation analog of goal-N's scalar c_n,p_n,
   domain sinusoid) — `code/Egate2_*.py` + goal-N `code/Ngoal_*` are the materials.
2. Compute the sub-threshold arc width Δ(q) and the escape angle in closed form; confirm the
   `O(1/q²)` margin numerically (q=18..500, validated interval).
3. Prove `Δ(q) < escape − c/q²` uniformly (the sharp `max cos` form; split small-q certs + q→∞
   parabolic-limit tail — renormalize the cusp neighborhood, θ→0).

## Next experiments (the ones not yet run)
- **E5 drift = rotation phase:** confirm the corridor phase advances monotonically by θ per W_q and
  the sub-thr arc is a single interval (⇒ dwell bound). `Egate2_stability.py` extended to phase.
- **E6 renormalization:** rescale a,b near the cusp by q; seek the θ→0 limiting (parabolic) map that
  controls the O(1/q²) tail uniformly. Fit Δ(q), escape-margin vs q for the closed form.
- **arc-width closed form:** the key missing analytic object; once known, (L1b) is explicit calculus.

## Resource notes
- Aristotle (cloud, runs offline): q19 cert `43e0fbfa-b495-42fb-b334-02f2cf19d127`; GATE-2 bedrock
  `d5e000f9-6745-4f74-a684-b7421d7c24be`. Check `aristotle show <id> --api-key $(cat ~/.config/aristotle/api_key)`.
- M1/M2: BLOCKED (no creds/ssh). Not usable.
- Local jobs die at device-off; only Aristotle progresses offline.

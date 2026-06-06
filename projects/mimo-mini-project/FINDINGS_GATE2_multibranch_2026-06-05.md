# GATE-2 multi-branch crux — RE-LOCALIZED (deep-middle corridors provably dominated)

**Date:** 2026-06-05. Source: workflow `gate2-multibranch` (wf_188a2838-bc3, 6 agents, adversarial
refuter) + my own independent spot-check. **Good progress; GATE-2 NOT closed but the multi-branch
"zoo" collapses to 2 concrete lemmas.** Value X_Ω(q)=1/λ³ not in question (no-island q≤420).

## Headline
The deep-middle multi-branch corridors that `FINDINGS_GATE2_L1b_REFUTED` flagged as the real
obstruction are **provably dominated** — they cannot sustain a sub-threshold run:
- **Only TWO sustained corridors exist at every q**, both F-family (j=1, trace λ): C1={q−1} (scalar
  = goal-N window) and C2={q−1,q−3} (W_q rotation). NO other branch-set sustains a run ≥3 at any q
  tested (18,25,40,50,60,75,90; exhaustive full-domain grid 11 q incl. primes/large q to 200).
- **Deep-middle branches dip below thr but EJECT in one step.** They reach minP=X(i−1)/(1+X(i−2))²
  (e.g. q=40 offset-11 minP=0.076 ≪ thr=0.126) BUT next-step P≥thr always. **dwell = 1**, can't chain.
  MY INDEPENDENT SPOT-CHECK (/tmp/check_deepmid.py, q=40,60,90): of 11199/12141/12543 non-F
  sub-threshold cells, **0** have next-P<thr; min next-P = 0.1954/0.1917/0.1906 ≫ thr≈0.125
  (margin ~0.065, q-uniform). Confirmed.
- **F-family is extremal**: trace spectrum 2cos(jπ/q) strictly decreasing in j (HP residual ~1e-48);
  j=1 (λ) is the slowest rotation = longest dwell. Deeper corridors rotate j× faster ⇒ shorter.
- **All switches escape**: every distinct-center corridor switch ⇒ |trace|≥2 (non-elliptic);
  ~10^6 switches/q tested, 0 elliptic-staying. Since only F-family sustains, all relevant switches
  are F-to-F = already covered by the PROVEN (L2) `switch_forces_nonelliptic`.

## Genuine observable on middle branches (E2, derived)
P_i = a·L_i/X(i−1); min over the branch cell = X(i−1)/(1+X(i−2))² (matches goal-F). A corridor of
index j has sinusoid product p_n=(r²/2)[cos J + cos((2n+1)J−2ψ)], J=jπ/q, cos J=tr_j/2 — goal-N's
j=1 form with θ→J. Deeper j (j≥2) rotate faster ⇒ shorter dwell; this generic-j family is exactly
the DEEP-MID corridors, and it is why they are dominated/eliminated.
**Both sustained F-family corridors are j=1 (J=π/q), NOT just C1.** ⚠ CORRECTION (2026-06-05, exact
symbolic, /tmp/verify_wq_trace.py): the C2 word W_q=(q−1,3)(q−1,0)(q−3,0) has monodromy
M=M_{q−3,0}·M_{q−1,0}·M_{q−1,3}=[[−λ, 2λ²+1],[−1, 2λ]], det 1, **trace = λ EXACTLY** (T(λ)−λ≡0 as a
polynomial in λ; verified mod the distinct minpolys of 2cos(π/q) for q=7,8,11,13,17,18,19,23). So C2
rotates by θ=π/q — the SAME slowest rotation as the scalar C1 — and is **j=1, NOT j=2** (its trace is
λ, NOT λ²−2=2cos(2π/q)). C2 reaches ~8 GENUINE steps only because the word packs 3 genuine steps
(q−1,q−1,q−3) per single π/q rotation; in ROTATION UNITS it is dominated by C1 and reduces to the
IDENTICAL scalar F-window inequality (the word-start product P0=a·b is exactly a scalar c_m·c_{m+1} of
the rotation-by-θ sequence a_{m+2}=λa_{m+1}−a_m). Confirmed on genuine orbits q=17..25 (rotation-units
≤ L*(q)−1 in every case).

## Re-localized GATE-2 (q≥17) — the remaining program
GATE-2 (no sustained sub-threshold orbit) = conjunction of:
1. **F-corridor window** — = goal-N scalar floor-1 window. PROVEN per-q (Lean q≤21) + computer-assisted
   uniform (q=18..500). Uniform all-q Lean = the standing GATE-1 formalization (the (L1) O(1/q²) item).
2. **Deep-mid ejection lemma** [NEW, tractable, OPEN-Lean] — "branch i∉{q−1,q−3}, P<thr ⟹ next-P≥thr"
   (dwell≤1). Margin ~0.065 NON-vanishing ⇒ Positivstellensatz-tractable (kick_pure-style, per-branch
   over ℚ(λ)). NUMERICAL-verified (exhaustive + my spot-check); not yet Lean. Closes the multi-branch piece.
3. **(L2) F-family switches** — PROVEN (`BCZHeckeL2_composite_VERIFIED`, my-verified).
4. **Torsion quantization** — "every realizable corridor monodromy trace ∈ {2cos(jπ/q)}" — NUMERICAL
   only (HP residual ~1e-48); needed so steps 1–2 cover ALL corridors. Likely elementary (Hecke G_q torsion).

## Honest status tags
- **PROVEN (Lean, my-verified):** bedrock det=1 + generator classification; (L2) F-family; F-window per-q q=7..21.
- **NUMERICAL (verified, exhaustive + my spot-check):** F-extremality, deep-mid dwell≤1 / ejection, all-switch-escape.
- **OPEN:** (a) ejection lemma in Lean [tractable]; (b) uniform F-window in Lean [the standing hard (L1)];
  (c) torsion-quantization as a stated lemma.

## Achievable near-term milestone
For q=17..21 the F-window is ALREADY Lean-proven. So: **ejection lemma + (L2) + torsion-quantization +
genuine assembly ⇒ GATE-2 CLOSES per-q for q=17..21** — the FIRST genuine X_Ω(q)=1/λ³ proofs past q≤15.
Path to finish: (i) prove ejection lemma (Aristotle/local), (ii) assemble per-q closure q≤21, (iii) the
uniform all-q remains = the standing (L1) F-window formalization.

## Artifacts
Workflow scratch in /tmp (r1_vec.py exhaustive census, midbranch.py, r1_deepmid.py). My check:
/tmp/check_deepmid.py. No repo pollution from agents (scratch /tmp only).

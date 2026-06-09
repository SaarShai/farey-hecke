# Two pursuable math breakthroughs (2026-06-08)

Workflow wf_624b91ff-b80 (generate → adversarial vet on achievability × researcher-value × prior-art → sieve). Both rest on our Lean-verified assets + the working Aristotle pipeline. Through-line: the novel structural identity **X(q) (ergodic-opt ground value) = cluster-onset threshold q\***, absent from all prior art.

NOTE: claims about existing Lean files being sorry-free are per the agents' repo reading; **step 1 of each plan confirms via a fresh `lake build` + `#print axioms`** (not yet independently re-verified here).

## Breakthrough 1 — Fully-formal X(3)=2/9, stubs removed: *first machine-verified result in ergodic optimization*
- **Aim:** one auditable Lean library where `#print axioms` on `essSup_bczProduct_ge` + `no_ground_state` reports only `propext/Classical.choice/Quot.sound` — wiring `BCZThresholdIntegration` (v5) as an import (not an axiom stub), plus one short theorem for the approximant sequence `(a,2a), a→1/3⁺` reaching ess-sup 2/9. Delivers X(3)=2/9 + non-attainment + cluster≤2, machine-verified.
- **Achievability: HIGH.** All hard math already proved sorry-free across v5/v8/v9 + Aristotle v10 (`bczOnsetEqualsQStar`, 0 sorries). Remaining = Lean plumbing + 1 lemma, 1–2 Aristotle dispatches. No new mathematics.
- **Value: MODERATE.** Ergodic optimization (Jenkinson/Bochi/Bousch, ~dozens) — L∞ objective is new to them; horocycle dynamics (Athreya/Cheung/Boca, ~dozens) — BCZ/cusp-escape realization new; Lean/formal-math (hundreds) — *first machine-verified result in a new subfield*.
- **First step:** `lake build BCZThresholdIntegration.lean` (v5) in a clean Mathlib v4.28.0 checkout → confirm sorry-free; replace `axiom bczProb_eq_value` with the import; re-run `#print axioms`.

## Breakthrough 2 — cluster≤2 for Hecke G_q (Rosen-BCZ), starting with a Lean proof for q=4; headline = X(q) = cluster-onset threshold
- **Aim:** prove `cluster_size_le_two` for q=4 in Lean on Taha's explicit domain `T⁴ = {0<a≤1, 1−√2·a < b ≤ 1}` (three consecutive orbit points can't all have `ab < √2/8 = X(4)`); publish q=3 (Lean, done) + q=4 (new) + numeric q=5–8, headline: the ergodic-optimization **ground value X(q) coincides with the cluster-onset threshold** — a new bridge between the ergodic-opt and extreme-gap literatures.
- **Achievability: MODERATE-HIGH.** q=3 fully Lean-proved (v8); q=4 = well-posed finite geometric case-analysis on Taha's closed-form domain (arXiv:1810.10668); D2 numerics already confirm cluster≤2 for q=4–8. Partial q=3+q=4 + conjectural q≥5 is independently publishable.
- **Value: HIGH.** Homogeneous dynamics / horocycle (Marklof, Strömbergsson, Athreya–Cheung, ~100–200); Hecke/Rosen-CF; ergodic optimization; Katz–Sarnak gap-statistics (universality-class separator).
- **Prior-art delta:** no paper proves a cluster bound for any G_q (q≥4); Taha states no extremal value; Marklof–Pollicott (arXiv:2408.01781) does single-exceedance, not consecutive-exceedance pairing. The `t_q* = X(q) = cluster-onset` identity is novel.
- **First step:** read Taha §3 (T⁴ domain + return map); write the three-consecutive-orbit inequality system for q=4; dispatch to Aristotle (same nlinarith/case-split style as v8).

## Rejected (moderate achievability — need NEW math, not just assembly)
General `X(q)=1/λ³` lower bound over all invariant measures; GUE Fredholm-determinant RMT comparison; JP-determinant `C_q(λ_q)` proof (vs the numeric law D3 r4 is computing).

## Goal 1.5 (next escalation, after q=4 lands) — the UNIFORM all-q theorem
Promote `cluster≤2` (hence `X(q)=q*`) from case-by-case (q=3 proved, q=4 in progress) to **one
theorem for ALL Hecke G_q, q≥3**, in Lean — the complete bridge across the whole family.
- **Why high-achievability:** the all-q skeleton is reportedly already Lean-verified (FRONTIER_STATUS
  goal M: `BCZHeckeL2_traceIdentity_allq_VERIFIED`, `lam_is_max_elliptic_trace`, value-safe to q≤200).
  Remaining = connect that λ-extremal trace structure to the cluster bound uniformly (q=4's finite
  argument, parameterized by q). **CAVEAT: confirm the goal-M files build (`lake build` + `#print
  axioms`) FIRST**; if a single uniform argument needs new math (not per-q case-analysis), drops to moderate.
- **Why high-value:** a *universal* theorem (all Hecke q) + the novel ergodic-opt↔gap-statistics
  bridge for the entire family — homogeneous dynamics, ergodic optimization, Hecke/Rosen, Katz–Sarnak.
- **First step:** verify goal-M Lean files; then the uniform cluster bound via λ-extremality.
- **After 1.5 (not yet):** extend the bridge beyond Hecke to general lattices/Fuchsian groups
  (Athreya–Cheung §8.1) — higher reach, lower achievability.

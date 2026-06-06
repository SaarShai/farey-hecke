> ⛔ **SUPERSEDED (2026-06-05, later same day) by `FINDINGS_bridge_robustness_2026-06-05.md`.** This
> round used a DIFFERENT, partly hand-tuned observable per group. A robustness gate (ONE frozen canonical
> observable `ψ=1/R = P`) REFUTED the strong claims below: the (2,4,6) "decisive positive" and the
> (2,3,7) prediction are TUNING ARTIFACTS — both select the hyperbolic systole, not the slowest elliptic,
> under the canonical observable. The "~1.7× slowest-torsion rejection law" does NOT survive. What
> survives is only the **cusp / torsion-free dichotomy** (Γ(2)/octagon anchors). Read the robustness file;
> treat the "decisive positive" / "slowest torsion generalizes" language below as RETRACTED pending the
> Bowen-Series-coding discriminator. Kept for the record / methodology only.

# Bridge generalization — does min-ess-sup select slowest-torsion/cusp (not hyperbolic Lagrange) beyond Hecke?

**Date:** 2026-06-05. Source: workflow `bridge-generalization` (wf_f7f1c05a-4a1, 5 agents, M1/M2
exact word-enumeration). Γ(2) backbone independently re-verified by me (`/tmp/verify_gamma2.py`);
(2,4,6) and octagon are subagent numerics (float64, cross-checked 2 ways by the agents, **NOT** re-run
by me). Tags below are honest. **Bottom line: the law generalizes in a CONDITIONAL form, with one
decisive negative and a known observable-tuning caveat.**

## Three test groups (all genuinely non-Hecke-triangle)
| Group | signature | non-hyp available | min-ess-sup extremizer | attained? | hyperbolic "Lagrange" |
|---|---|---|---|---|---|
| **Γ(2)** (level-2 congruence; Romik/Stern-Brocot) | (0; −; 3 cusps), torsion-free | parabolic (cusps) only | **parabolic cusp**; n=1 → 2/9 (= Hecke q=3) | **no** (inf→0, drifts to cusp) | rejected, unbounded margin (silver LR, tr 6) |
| **(2,4,6) von Dyck** (cocompact Coxeter) | (0; 2,4,6; 0 cusps), has elliptic torsion | elliptic (cone pts) | **slowest elliptic** order-6, tr √3=2cos(π/6) | **YES** (real periodic orbit) | rejected **1.6775×** (systole tr √6) |
| **genus-2 octagon** surface group (Bowen-Series) | (2; −; 0 cusps), torsion-free | **none** (all non-id hyperbolic) | **hyperbolic** (forced; period-2, tr 2+2√2) | yes (inf attained) | n/a — extremizer *is* hyperbolic |

## What it decides
- **The essential ingredient is EXISTENCE of torsion-or-cusp, NOT "escape to a cusp".** The cocompact
  **(2,4,6)** case is decisive: no cusp at all, yet min-ess-sup still selects the *slowest elliptic*
  (largest cone order ⇒ rotation closest to identity ⇒ trace 2cos(π/6)=√3, the top of the elliptic
  trace spectrum) and the extremizer is **attained** at a genuine periodic orbit. This disambiguates
  what Hecke q=3 (parabolic/cusp) could not: the phenomenon is *slowest-torsion per se*.
- **Conditional, not universal.** The cocompact **torsion-free** genus-2 octagon — the sharpest
  discriminator — has neither cusp nor torsion, so the extremizer is forced hyperbolic and the inf is
  *attained* (longer words approach from above; no escape, no non-attainment). When no torsion/cusp
  exists there is simply nothing for the law to select.
- **Recurring ~1.7× rejection ratio:** Hecke G_3 1.72×, (2,4,6) 1.6775× — suggestive, possibly a
  coincidence of the specific trace ratios; needs more cocompact-with-torsion groups to test.

## Honest status tags
- **PROVEN-structural (group theory, certain):** Γ(2) torsion-free ⇒ non-hyperbolic = parabolic-cusp
  only. (2,4,6) cocompact, max cone order 6 ⇒ largest elliptic trace = 2cos(π/6)=√3 < 2 < √6 = systole
  (a genuine spectral gap). Genus-2 octagon cocompact torsion-free ⇒ every non-identity element
  hyperbolic. These fix *what each group makes available* — they do NOT establish the selection law.
- **NUMERICAL (my-verified):** Γ(2) — pure-L parabolic (tr 2 ∀ powers), LR hyperbolic (tr 6, fixed pts
  √2−1, −(1+√2)), cusp gap-product P_n=(n+1)/(n+2)² with n=1=2/9 reproduced exactly
  (`/tmp/verify_gamma2.py`).
- **NUMERICAL (subagent, NOT re-run by me):** (2,4,6) — exhaustive 4,234,149 corner words to length 9
  on M1, float64 trace residual ~1e-14, min ρ=||tr|−2|=2−√3=0.2679 at order-6 elliptic, systole √6
  rejected 1.6775×. Octagon — 5.76M Bowen-Series SFT words to L=8 on M2, period-pt close-err ≤1e-16,
  min-ess-sup 4.6116 = larger eigenvalue of tr-(2+2√2) period-2 orbit, attained, systole rejected
  2.07×, two observables agree.
- **OPEN / SPECULATIVE (the real caveat):** Each group used a DIFFERENT, partly hand-tuned observable
  (Γ(2): ab/(a+b)²; (2,4,6): ρ=||tr|−2| *after the agent rejected the literal spec 1/|tr−√3| as
  degenerate*; octagon: 1/|F′| dwell). The selection law's **robustness to a single canonical
  observable is UNVERIFIED** — this is the load-bearing gap. The "uniform principle across all Fuchsian
  groups" is stated, never derived. No theorem here.

## Novelty boundary
Firmly DISTINCT from classical Lagrange–Markov (which extremizes over *hyperbolic* badly-approximable
geodesics; bottom of the Markov spectrum = golden/√5 hyperbolic class). The min-ess-sup is an
L∞/min-MAX over invariant measures (not a liminf) and explicitly REJECTS that hyperbolic element in all
three groups. Coding machinery (Series, Adler–Flatto, Bowen, Romik) is classical; "systole = badly-
approximable analog" is standard. NON-standard = the min-MAX objective whose extremizer is
torsion-or-cusp-driven and (in cusped/parabolic cases) ground-state-free. **Realistic ceiling: novelty
of formulation/realization, not a famous-problem result.** The cocompact-torsion-free negative is itself
the most informative output — it BOUNDS the phenomenon to groups possessing torsion or cusps.

## Required next step (gate before any claim of "generalizes")
1. **Observable-robustness:** re-run all three groups under ONE fixed geometric observable (period-
   normalized translation-length / Lyapunov roof) — rule out per-group tuning. THIS IS THE GATE.
2. Then **(2,3,7)** (minimal-area cocompact triangle group, competing elliptic orders 2,3,7): test
   whether min-ess-sup picks order-7 (slowest) over 2,3 and whether systole is again rejected ~1.7×.
   Cheap on M1, validated pipeline.

## Artifacts (scratch /tmp only; no repo pollution from agents)
Per-group scripts ran on M1/M2 (results in workflow task output `wzbkpiib8`). My check:
`/tmp/verify_gamma2.py`. Full per-group structured results retained in the workflow output file.

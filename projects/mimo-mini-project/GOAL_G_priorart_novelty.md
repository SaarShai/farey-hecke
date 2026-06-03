# /goal G — Prior-art & novelty audit: is the Hecke-BCZ ergodic-optimization layer actually new?

> Paste the body below into `/goal` in a fresh session. Self-contained. Work autonomously; verify every
> citation against the PRIMARY source (abstract/PDF, not a summary). Send NOTHING outward (this is an
> internal audit; USER-gated for any external use). Adversarial honesty is the whole point here:
> **assume the result is NOT novel until the literature shows otherwise** — fabricated/over-claimed
> novelty is this project's #1 failure mode, and a clean "already known" verdict is as valuable as "new."

## MISSION
Settle, with primary-source citations, whether the central results of this project's Hecke-BCZ
ergodic-optimization work are genuinely new, already in the literature, or "novel-as-formulation"
(known pieces, new assembly). This GATES any write-up or external claim. Produce a prior-art map: for
each result, the closest known work and a precise verdict.

## THE CLAIMS TO AUDIT (what we'd want to call "ours")
1. **Ergodic optimization of the BCZ / Hecke-BCZ return map.** Object: the BCZ map (q=3) and Taha's
   Hecke `BCZ_q` (q≥4); observable `P` = the Farey/horocycle gap-product (`P=xy`, `=1/(Q²·gap)`); the
   quantity `X(q) = inf_μ ess-sup_μ P` (ergodic-optimization "ground value"). **Has anyone studied
   ergodic optimization (min-max of a Birkhoff-type/observable) on the BCZ map or Hecke BCZ map?**
2. **The constants.** q=3 value `2/9`; the general genuine value `X_Ω(q) = 1/λ³ = 1/(2cos(π/q))³`
   (q≥5), `√2/8` (q=4). Are these extremal Farey/Hecke-gap constants known anywhere (e.g. as
   sharp bounds on consecutive Farey gaps, Hall-type results, Diophantine approximation by Hecke
   groups, Rosen continued fractions)?
3. **No ground state via cusp escape.** The infimum is approached but never attained because the
   optimizing configurations escape to a cusp (escape of mass on a non-compact system). Is this
   mechanism / this kind of non-attainment example known in ergodic optimization?
4. **The "two different answers" phenomenon.** `inf_μ ess-sup_μ P = 1/λ³` while `inf_μ ∫P dμ = β_min <
   1/λ³` (min-max ≠ minimal-average) — a concrete system where the two ergodic-optimization problems
   genuinely differ. Known examples?

## CLOSEST-PRIOR CANDIDATES (check each against primary source; find the REAL nearest neighbor)
- **Ergodic optimization framework:** O. Jenkinson, "Ergodic optimization in dynamical systems", ETDS
  39 (2019) [survey — read for: which systems/observables are standard; is any horocycle/BCZ example
  there]. E. Garibaldi, "Ergodic Optimization in the Expanding Case" (Springer 2017). G. Contreras,
  "Ground states are generically a periodic orbit", Invent. Math. 205 (2016) [compact + generic;
  ours is non-compact + specific observable — confirm the non-overlap precisely]. Bochi's surveys.
- **BCZ map & Farey/horocycle:** Boca–Cobeli–Zaharescu, Crelle 535 (2001); Athreya–Cheung, IMRN 2014
  (arXiv:1206.6597) [the §8 open-questions list — check if any min-max/extremal-gap question is posed];
  Athreya "Gap distributions and homogeneous dynamics" (survey).
- **Hecke / Rosen CF:** M. D. Taha, arXiv:1810.10668 (the genuine `BCZ_q`; already in
  `prior_art_taha_cobeli.md` — check whether Taha or follow-ups study any extremal/optimization
  quantity, not just the gap DISTRIBUTION); Burton–Kraaikamp–Schmidt (Rosen natural extensions, TAMS
  352 (2000)); Nakada; R. Schmidt / Hecke-group Diophantine approximation constants (Hurwitz constants
  for Hecke groups — `√2/8`, `1/λ³` may coincide with a known Hurwitz/Markov-type Hecke constant —
  CHECK THIS carefully; it is the most likely "already known" hit).
- **Farey-gap extremes:** Hall's conjecture on Farey fractions; Kesseböhmer–Stratmann (Farey/Stern–
  Brocot multifractal); any "largest/smallest product of consecutive Farey denominators" result.
- **Escape of mass:** Einsiedler–Kadyrov–Pohl; Eskin–Margulis — for the non-attainment mechanism.

## METHOD (adversarial, primary-source)
- Use web search + arXiv + fetch actual abstracts/PDFs. Consider the bundled `deep-research` skill for
  the fan-out. For each candidate: read the primary source, state exactly what it proves, and whether
  it subsumes / overlaps / is distinct from each claim above. **Verify every citation's
  author/venue/year/volume against the source** (the project has a history of fabricated vol/pages —
  e.g. a prior "Annals 170" that didn't exist; BKS was mis-cited as 364(2012) vs the correct 352(2000)).
- Special attention to the **Hurwitz constant for Hecke groups**: if `1/λ³` or `√2/8` is a known
  Diophantine-approximation constant for `G_q`, the "new constant" claim collapses to a new
  DERIVATION of a known constant — say so plainly.
- Distinguish three verdicts per claim: **KNOWN** (cite it), **NOVEL-AS-FORMULATION** (pieces known,
  this assembly/quantity not stated), **APPARENTLY NOVEL** (no prior found — and note search limits).

## KEY CONTEXT (`/Users/za/Documents/Farey NOW/`)
- `projects/mimo-mini-project/FRONTIER_STATUS_2026-06-03.md` (what we claim, ledger),
  `FINDINGS_goalB_genuine_domain_2026-06-03.md`, `FINDINGS_goalD_genuine_lowerbound_2026-06-03.md`.
- `primes-equispaced/.../prior_art_taha_cobeli.md` (existing Taha/Cobeli prior-art notes).
- Memory: `project_farey_prior_art` (the existing novelty boundary: static Farey↔Mertens = Cox–Ghosh–
  Sultanow arXiv:2105.12352; dynamical/per-step BCZ-cocycle occupies Athreya–Cheung IMRN2014 §8 open Q),
  `project_hecke_genuine_domain`, `project_koyama_risk` (no external sharing/collab without user gate).

## CONSTRAINTS (hard)
- Internal audit only. Nothing outbound / published / sent to any collaborator (Koyama etc.) — USER-gated.
- No commit/push/git changes unless the user explicitly asks. `~/Documents` Drive-synced: no folder/
  `.git` moves; `* (1)` = conflict artifacts.
- Do not inflate. If a constant/result is already known, say so prominently — that protects the project.

## DEFINITION OF DONE
- A prior-art audit doc `research_notes/PRIORART_ergodic_opt_2026-06-xx.md`: for each of claims 1–4, the
  closest primary-verified prior work + verdict (KNOWN / NOVEL-AS-FORMULATION / APPARENTLY NOVEL), with
  every citation's author/venue/year/volume confirmed against the source.
- A one-paragraph bottom line: **is there a defensible novel contribution, and if so stated how**, plus
  the single biggest risk (most likely the Hecke Hurwitz-constant overlap). This is the go/no-go input
  for a write-up.
- Update memory (`project_farey_prior_art` or a new `project_hecke_priorart`). Nothing sent outward.

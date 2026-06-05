# External opportunities for the project's novel achievements (2026-05-16)

Honest map. Pairs with `NOVEL_ACHIEVEMENTS.md`. Adversarial-honesty norm
applied — including correcting two citation errors a research agent
introduced (the project's #1 documented failure mode is citation/novelty
inflation; caught here, not propagated).

## Blunt bottom line

**There are no monetary bounties for this work.** Millennium Prize = RH-class
(we explicitly make no RH claim). Erdős prizes (~$15K total, erdosproblems.com)
are combinatorics/graph-focused — **Farey discrepancy / Mertens is not
listed** (checked). Lean/DeepMind funds infrastructure, not per-theorem
prizes. The real value stream is **publication + collaboration + formal
record**, exactly as the project's honest map already says. Anyone claiming
otherwise is inflating.

## A. Journals (realistic fit, by result)

| Venue | Fits | Note |
|---|---|---|
| **Experimental Mathematics** (tandfonline uexm20) | A1 (N·W→C), A2 (Sign Thm), A3 (BCZ dict.) | **Primary target.** Aistleitner explicitly suggested it. Welcomes verified empirical corrections + computer/Lean-checked results. |
| **Research in Number Theory** (Springer 40993) | A1–A4 | Open access; BCZ-dictionary + function-field are in scope. |
| **Integers** (integers-ejcnt.org) | A1–A3 | Fast, no fees; good for the Sign Theorem note. |
| **Journal of Number Theory** | A2, A4 | Tier-1; needs the cleanest framing. |
| **Acta Arithmetica / Functiones et Approximatio** | A1–A4 | Archival Farey/discrepancy homes; high bar. |

Realistic packaging: **(i)** an Exp. Math. note = A1 + A2 + A3 (the per-step
lens: empirical correction + Sign Theorem + BCZ-cocycle dictionary); **(ii)**
the function-field results (A4) as a short separate note or an appendix;
**(iii)** the Koyama joint paper (C1) — already in motion, its own track.

## B. Academic callout — Athreya–Cheung §8 (CORRECTED)

- Correct citation (verified primary read, project prior-art lock):
  **Athreya & Cheung, "A Poincaré section for horocycle flow on the space of
  lattices", IMRN 2014, no. 10, 2643–2690 = arXiv:1206.6597.**
  (A research agent mis-cited this as arXiv:1403.7502 — WRONG; do not use.)
- What §8 actually asks (verified, NOT "is the BCZ map ergodic/weak-mixing" —
  that is a different, since-resolved question, Cheung–Quas arXiv:2403.14976):
  §8 poses whether an **optimal bound on the BCZ/Theorem-1.3 error term is
  equivalent to the Riemann Hypothesis**, citing Franel–Landau.
- Honest callout we may make in a writeup: *"We give the explicit cocycle
  `g=1−Φ·gap` whose Birkhoff sum is the Farey discrepancy `E_Q`, making
  precise the object implicit in the open question of Athreya–Cheung
  (IMRN 2014, §8); we do NOT resolve it — we further show the natural
  variance route is numerically obstructed (raw cocycle not uniformly L²,
  decay α≈½, twist-inert)."* Formulation-novelty + honest non-resolution.
  Adds credibility to an Exp. Math. submission; it is **not** a prize.

## C. Formalization venue (concrete, real)

- **Google DeepMind `formal-conjectures`** (github.com/google-deepmind/
  formal-conjectures): accepts formalized conjectures/statements; path =
  open an issue then PR. The Lean-4 Sign Theorem (A2) is a direct fit.
  No bounty; permanent formal/benchmark record + visibility.
- mathlib: only if the lemmas generalize cleanly; otherwise keep as a
  project-local Lean artifact + `formal-conjectures` entry.

## D. OEIS / permanent record

- Candidate sequences: prime-step increment `ΔA(m)=−1+p·𝟙[p|m]`; the
  function-field Mikolás constant `C_FF(q)=(q+1)²` → {9,16,36,64,…} (this is
  just (q+1)² but the *derivation context* is the citable part); the verified
  `N·W(N)` table. **Verify any existing OEIS A-number before citing** — an
  agent suggested "A084237" UNVERIFIED; do not cite it without checking.
  No payment; permanent reference + discoverability.

## E. Not available (stated so no one re-checks)

- Monetary bounties / competitions for this analytic-NT tier: **none**
  (Millennium = RH-class; Erdős = combinatorics; Lean = infra-funded).
- 2026 Farey/discrepancy conference with open CFP: none found this cycle.
- Active Polymath in this domain: none.

## Recommended action order (nothing sent without user approval)

1. **Koyama joint paper** — the real center of gravity; continue on the
   agreed Technical/Computational scope. (C1)
2. **Exp. Math. note** — A1+A2+A3, with the corrected Athreya–Cheung §8
   callout. Aistleitner is the natural referee/contact.
3. **`formal-conjectures` PR** — the Lean Sign Theorem (A2); low effort,
   real formal record.
4. Function-field note (A4) — short, or fold into (2) as a section.
5. OEIS + arXiv deposit once (2)/(4) drafted.

All of the above require the user's go: no submission, email, PR, or push is
made autonomously (project rule; sensitive items like the Koyama drafts stay
user-controlled).

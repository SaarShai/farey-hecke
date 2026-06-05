# equispaced-primes (curated)

Curated import of the **valid** material from the `Primes-Equispaced` research repo.
The full, unpruned archive remains at `github.com/SaarShai/Primes-Equispaced` and in
the relocated source git history; **nothing was deleted** — "curated" means only the
material judged still-valid (per the project's honest-map) was copied here. The dead
H1/halo/Theorem-B wave saga (~500M of `experiments/`, `archive/`, and ~40
`handoff-2026-05-1x-*` dirs) was intentionally **not** carried over.

> The **live** Hecke ergodic-optimization work is NOT here — it lives at the repo
> root in [`projects/mimo-mini-project/`](../projects/mimo-mini-project) and on the
> `hecke-goalL-2026-06-03` branch. This subtree holds the equispaced-primes lineage
> (Lean, Koyama, papers, function-field, BCZ-cocycle, DPAC) that the Hecke work grew out of.

## Layout

| Path | Contents | Status |
|---|---|---|
| `lean/formal-conjectures/` | Sign Theorem, Ramanujan-sum bridge, Mertens spectroscope, DPAC, corrected B∞, −1-core | compile-clean, axiom-audited |
| `lean/farey-lib/` | Farey/Stern-Brocot library (`|F_n|=1+Σφ(k)`), three-gap; staged for a Mathlib PR | certified |
| `koyama/{shared,correspondence,joint-paper}/` | Koyama collaboration: corrected C₁-ensemble scripts/data, email threads, joint-paper bundle | see ⚠ below |
| `papers/nw-mertens-note/` | The shippable **N·W(N)→C≈0.66** per-step Farey↔Mertens honest note | VALID headline |
| `papers/sign-theorem/` | "The Geometric Signature of Primes in Farey Sequences" (`main.tex`/`main.pdf`) | VALID |
| `papers/{amr,math-paper,spectroscope,submission-plan}/` | companion drafts + arXiv plan | drafts |
| `function-field/` | D3 function-field model + DPAC certified numerics (6000/6000) + PR #3716 artifacts | REAL, see ⚠ |
| `bcz-cocycle/` | D1 dynamical/per-step BCZ-cocycle (occupies Athreya–Cheung IMRN 2014 §8) | NOVEL-as-formulation |
| `hecke-ergodic/cluster-universality/` | cluster=2 universality diagnostics (LMFDB Δ-zeros) | supports Hecke work |
| `code/`, `research-notes/` | verified numerics, publish tooling, fact ledgers | provenance |
| `docs/log.md` | append-only timeline (honest D-track verdicts + citation corrections) | history |

## ⚠ Curation note — dead claims, corrected citations, honest framing

**Do NOT re-import or restate these as live results:**

- **Annals "2/(3π)"** (Theorem-B-exact unconditional) is BLOCKED on the multi-decade
  GDC support-4 wall. Only the **GRH-conditional 0.85** and the unconditional cage
  `(17±√145)/(12π)` survive.
- **Unconditional H1** and the entire halo / Door-A-B-C-D / Gonek–Hejhal / BFMT
  "research-track-split" + "breakthrough-wave-*" saga reduces to **thin-strip
  critical-line density (TSDB)** — a known open problem. Not progress; not carried over.
- **B≥0 / B_∞ unconditional positivity**: Conjecture B+ (Mertens-restricted) is
  **directly false** (e.g. `B(p)<0` at p=237733). The B∞ identity is correct but
  **conditional (DRH)**; the 2026-05-16 pass was citation hygiene, not new math.
- **DPAC "9×–52× avoidance margin"** is **REFUTED** as a sample-size artifact. Keep only
  the **6000/6000 certified c_K≠0** result and the **K≤4 unconditional / K=5 first-open /
  LI-class** boundary.

**Propagate the corrected citations, never the originals:**

- Soundararajan = **Crelle 631 (2009) 141–152**, NOT the fabricated "Annals of Math. 170".
- Akatsuka = **2017, Kodai Math. J. 40, 79–101** (NOT 2013); eq.(2.5) unconditional, Thm 1 RH/DRH-conditional.
- Aoki–Koyama JNT 245 (2023) e^{−γ} result is **DRH-conditional**; Inoue JTNB 33(2) 2021 is unconditional.
- **P(3/2) = 0.8495626836…**, NOT 0.45224 (a drafts arithmetic error that equalled P(2)).
- arXiv:**2407.10214** = Karvonen–Zhigljavsky *MMD of Farey sequences* (was misattributed).
  Static Farey↔Mertens prior art = **Cox–Ghosh–Sultanow arXiv:2105.12352 (2021) only**.
- Keating–Rudnick (D3 §6 duality) = arXiv:1504.03444 / Algebra & Number Theory 10(2) 375–420 (2016).

**Honest framing of the kept headlines:**

- The **dynamical/per-step BCZ-cocycle** is NOVEL-as-formulation (AC IMRN 2014 §8 open Q);
  the underlying static Farey↔Mertens link is prior art (CGS 2021).
- The **function-field (D3) model** is REAL, exact, machine-verified, but **dictionary-tier,
  not new mathematics** — its only non-elementary object is the existing Keating–Rudnick
  variance. Ship as supporting exposition, not a headline.
- **N·W(N)→C≈0.66** (BCZ second-moment renormalization) is verified; the earlier log-N
  growth belief was wrong.
- The **Koyama collaboration is unverified** (project memory): gate any outbound use / IP /
  name-use on independent identity verification + written terms. The research has standalone
  value regardless.

**Rescued artifacts (post-audit):**
- `research-notes/bplus/` — the **reproducible B+ counterexample** bundle (`B_plus_direct_verify.c`
  + certified `.out` for p=237733, 243799 + writeup). B+ Mertens-restricted positivity is FALSE;
  this is the artifact behind that prose claim.
- `koyama/followup-proofs/` — Koyama B∞ + C₁-subleading proof notes (companions to the joint-paper appendices).
- `papers/sign-theorem/figures/*.png` — the 12 figures the paper `\includegraphics` (were absent;
  `\graphicspath` patched to `{figures/}{../figures/}` so it builds self-contained).
- `function-field/seed/{d1-cm-tower,d3-central-zero-map,mimo-sprint}/` — small D2/D3 seed siblings.

**Lean trust base:** kept `formal-conjectures` headline theorems use only
`{propext, Classical.choice, Quot.sound}` (plus `Lean.ofReduceBool, Lean.trustCompiler`
for `dpac_le_4`). No `axiom` declarations. Re-run `lake build _AxiomCheck` after any change.
Two DPAC-headline `sorry`s remain — the honest open LI-class boundary.

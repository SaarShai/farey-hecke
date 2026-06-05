# Bundle contents

This folder contains the draft Technical/Computational section of
the joint paper and its supporting material.

## Primary deliverable (sent to Koyama 2026-05-12)

| File | Purpose |
|---|---|
| `COVER_NOTE_TO_KOYAMA_2026-05-12.md` | Cover letter (body of the email). Two scope-confirmation questions and the list of Phase-1 table cells pending reconciliation. Both scope questions have been confirmed by Koyama's 2026-05-12 reply. |
| `SECTION_DRAFT_2026-05-12.md` | §X. Methodology, formalization, and numerical evidence. |
| `APPENDIX_A_BINFTY_PROOF.md` | Full pen-and-paper proof of Theorem X.4.1 (corrected $B_\infty$ identity). |
| `APPENDIX_B_CK_SUBLEADING_PROOF.md` | Full pen-and-paper proof of Theorem X.4.2 ($c_K$ leading + subleading), with the Laurent-algebra for the local Perron double-pole residue in §B.2. |
| `LEAN_SORRY_STATUS.md` | Per-`sorry` inventory of the 10-file Lean lake project. Two sorries remain (DPAC headline at general $K$, LI-class); eight files are fully proved (the RamanujanSum addition of 2026-05-14 brought the count from 7-of-9 to 8-of-10). Includes a cumulative `#print axioms` audit. |
| `HALO_GL1_SKETCH_2026-05-12.md` | Supplementary technical sketch: GL(1) halo-route reduction toward (SP-L). Negative finding. |

## Compiled LaTeX bundle

| Folder | Purpose |
|---|---|
| `latex/` | `paper.tex` driver, the three converted subfiles (`section_X.tex`, `appendix_A.tex`, `appendix_B.tex`), `references.bib` (18 entries), the `clean.py` regeneration pipeline, and `paper.pdf` (≈18 pages). Builds reproducibly via `python3 clean.py && tectonic paper.tex`. **NOTE (2026-05-15):** `paper.pdf` was rebuilt 2026-05-15 09:41 with tectonic 0.15.0 after the perfection pass, citation corrections, and the cross-session reconciliation (see `log.md`): it now carries the **Mikolás (1949) prior-art attribution** for the static Farey–Mertens identity (§X.6 provenance note + bib entry, 12 references) and a **§X.7 Structural remark** making the shared (SP-L)/DPAC/LI obstruction precise (Ng 2004). It is **current, not stale**, 20 pp, 0 undefined refs/cites, bibliography rendered. `clean.py` now carries an idempotent Unicode safety map and hardened citation conversion. Remaining build warnings are cosmetic only (overfull/underfull boxes in the dense §X.5/§X.6 tables; a benign hyperref duplicate-destination on the (AK)/(NDC)/(SP-L) display equations). |

## Forward-looking discussion documents (drafted while Koyama is reviewing Phase-1 cells)

| File | Purpose |
|---|---|
| `INTRO_AND_ABSTRACT_OUTLINE_2026-05-13.md` | Bullet-form skeleton for the joint paper's Abstract + Introduction. |
| `ABSTRACT_DRAFT_2026-05-13.md` | One recommended Abstract (~165 words, tight version) plus two alternatives (long form ≈235 words; arXiv-announcement ≈115 words). Updated 2026-05-14 with the corrected 8-of-10 Lean count. |
| `INTRODUCTION_DRAFT_2026-05-13.md` | First-pass Introduction prose (~900 words, 5 subsections). Uses real `references.bib` keys throughout; two explicit `KOYAMA-INSERT-*` cues mark the spots where the Dominance-of-$-1$ framing material should drop in. |
| `SP_L_SUFFICIENT_PACKAGES_2026-05-13.md` | Focused technical note on three sufficient packages (Routes I–III) that would close (SP-L). |
| `MIDWEEK_UPDATE_TO_KOYAMA_DRAFT.md` | Pre-drafted brief status update for whenever Koyama's reconciliation arrives (week of May 20). Includes send-decision criteria and §X.5.1 variants depending on his cell-flip resolution. **Contingent** — sent only if his reply triggers it. |
| `REPLY_TO_KOYAMA_DRAFT_2026-05-14.md` | **Proactive** reply, drafted 2026-05-14, summarising the post-2026-05-12 polish work (K=10^8 extension, 10-file Lean state with axiom audit, notation/citation/Soundararajan adversarial sweep, Abstract+Intro forward drafts) and surfacing four specific questions where Koyama's input would help before LaTeX integration. Send-decision notes at the end of the file. |

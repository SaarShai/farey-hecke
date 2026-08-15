# DRAFT STATUS — FLAGSHIP_PAPER_DRAFT.tex

Date: 2026-08-15. Lane P. Ticket: `plans/wayfinder/rh-goals/tickets/flagship-paper-draft.md`.

**Status: DRAFTING COMPLETE. NOT for circulation.** Dissemination
(submission, Koyama letter, any distribution) remains owner-gated per
the HITL tickets. Nothing has been submitted or emailed.

## Files

- `FLAGSHIP_PAPER_DRAFT.tex` — submission-shaped LaTeX draft: title,
  abstract, intro with literature positioning, main theorem (exact
  assembly-v2 statement, constants verbatim, margins rounded down),
  8-link proof-chain section with in-repo receipt citations,
  computational-certificates section with constants table and
  provenance hashes, weak-form no-vertical-line corollary (with scope
  limits per `NO_VERTICAL_LINE_COROLLARY.md`), Lean/machine-verification
  subsection (v18 `det_one_sub_proj_mul_proj` + joints; v17
  `KsZeroLattice`; 0 sorry; axioms propext / Classical.choice /
  Quot.sound), reproducibility appendix (in-repo receipts only, no
  external-availability claim), review/audit appendix, bibliography.

## Compile status

- **pdflatex is NOT installed on this machine** (`which pdflatex`
  returned nothing, 2026-08-15). The TeX therefore has NOT been
  compiled here. The preamble uses only `amsmath, amssymb, amsthm,
  geometry, hyperref` and standard environments; no exotic packages.
  First action before any circulation: compile with
  `pdflatex -interaction=nonstopmode FLAGSHIP_PAPER_DRAFT.tex` (twice,
  for hyperref/refs) on a machine with a TeX distribution and fix any
  issues.

## Open TODOs (must be resolved before any circulation)

1. **Bibliography TODO-VERIFY items** (marked `% TODO-VERIFY` in the
   .tex, never invented):
   - Phillips–Sarnak 1985 ×2: page ranges.
   - Simon 1977: page of Thm 4.2 (reported as p. 258 in R5 report).
   - Simon, Trace Ideals: exact theorem number for the perturbation
     bound (reported as "Thm 3.4 form").
   - Grothendieck 1952: page range (Thm 8 reported pp. 108–109).
   - Bandtlow–Jenkinson 2008: page range.
   - MMS: full author first names, exact title/venue/page range;
     confirm Thms 4.10, 6.4 and eq. (34) numbering against the primary
     PDF.
   - Bruggeman–Pohl 2009/2023: final venues, volumes, pages.
   - Pohl–Wabnitz 2026 (Memoirs AMS 318 no. 1616): author given names;
     only abstract/metadata was accessible to the novelty scout.
   - Borthwick–Weich 2021 (Stoch. Dyn. 21(3)): article number/pages.
   - Borthwick book: confirm edition/volume for the resonance framing.
   - **Frączek–Mayer entry is a placeholder** (`[Numerical resonances /
     Selberg zeta computations for Hecke triangle groups]`) — the exact
     title/venue/year must be found; the draft must not circulate with
     this stub.
   - arXiv 2509.17936 and 2507.09021: author lists.
2. **Author block** is a placeholder (`[Authors withheld in draft]`).
3. **Framing re-check against the V1 ruling** by a human reader: the
   draft claims only "first rigorous localization ... Re ≤ 1/2 − δ_gap"
   with the novelty-scout citation on every "first"; verify no stray
   "law"/family/density language crept in.
4. **Constants spot-check** against
   `lane_g/THEOREM_G5_OFFLINE_ASSEMBLY.md` and
   `R3B_FLAGSHIP_CERT_RECEIPT.json` (rounding direction: all margins
   rounded DOWN; min margin 3.43786e-8, not 3.43787e-8).
5. **MMS q>5 heading footnote** (Remark 2.1 in the draft) — mandatory
   per Kimi audit 1-E7; confirm wording against the primary PDF.
6. **Serialization caveat** (Remark after Link 1): the tighter winding
   ball (7.81e-114) requires re-running the pinned code; decide whether
   the paper quotes only the ~1e-99 reconstruction level.
7. **Lean receipt paths** (`projects/aristotle_dispatch_v1*/project_
   aristotle/`) — verify the exact filenames before citation.
8. **Known latent code notes** reproduced in Appendix A — confirm they
   stay in sync with `R3B_FLAGSHIP_CERT.md` if that report is amended.
9. **No external availability claim**: Appendix A states receipts are
   in-repo only. If a public deposit is later approved, update the
   appendix and artifact bibliography entries.

## What a human must verify before any circulation (summary)

- Compile the TeX (not done here; no pdflatex on this machine).
- Complete/verify every TODO-VERIFY bibitem against primary sources;
  replace the Frączek–Mayer placeholder.
- Re-read the theorem statement against the assembly note v2 verbatim;
  confirm round-down discipline and the exact constants
  (s* = 0.4538951800749447 + 5.7635372417301305i; box 1e-6/coordinate;
  δ ≥ 0.0461038; min margin ≥ 3.43786e-8; ‖L‖₁ ≤ 17.2911968;
  F_R = 1.77974e-6; T_tail(160) = 6.26786e-22; winding 1; 284 subarcs).
- Confirm the framing matches the V1 ruling (no "law", no family claim,
  no density claim; "first" only with the novelty-scout citation and
  its stated limitations).
- Confirm every "in-repo artifact" citation path actually exists.
- Owner sign-off: dissemination is owner-gated; this draft existing in
  the repo is NOT approval to submit, post, or email.

## Notes

- pdflatex command attempted per ticket:
  `( cd research_notes/rh_goals_2026-08-14/lane_p && pdflatex ... )` —
  pdflatex absent; compile deferred (see TODO 1/compile status above).
- No git commit made. No other lanes' files touched.

# 2026-08-26 — T1 completion + preprint assembly

## T1 final wave
- [x] GAP-4: Lemma-1 restatement — closed at ceiling standing, OWED-1 disclosed
- [x] GAP-7: van Trees closed — constant 2.395 vs √6, verified
- [x] GAP-17 propagation: closed-at-class-restricted (Gaussian-score class); Stam direction correction banked
- [x] GAP-9: landed (luna) — Cameron–Martin obstruction named, OWED items disclosed
- [x] GAP-13: landed (luna) — C_RMSE(d)=√(6·log(γ_d/2π)), draft claim corrected
- [ ] GAP-11 interpretation: estimator run on y(t) itself (local python, builder lane)
- [x] GAP-12: live-web prior-art re-check (research-lite) — NONE/SETUP-ONLY, closed
- [x] Frontier cold-verify of all lanes done
- [x] T1 cold referee: NOT-PROMOTABLE (19 defects, 8 blocking) — v4 rewrite required

## Preprint
- [x] Preprint main.tex assembled, compiles (15pp), intervals verbatim, 0 discrepancies
- [x] FIG-1 rendered from d8 shard receipts (range 0.2188–0.3273, matches spec) — referee pending
- [x] Zenodo package assembled (28 files, 7.5M) — pin-cert match verified; licence + upload = owner
- [ ] §11 pre-submission checklist
- [x] Preprint referee: PROMOTABLE-WITH-CORRECTIONS — all 13 corrections applied (764984f)
- [ ] Owner read before arXiv post

## Review / results
(append as lanes land)
- [x] T1 v4→v7 loop converged: round-5 PROMOTABLE-WITH-CORRECTIONS, corrections applied; T1 stands as conditional partially-certified result


## Koyama finalization — 2026-08-26 (Exp.Math retarget + Zenodo + final TeX)
[RESTORED 2026-08-26 by session d132431f: this section, added by session
"Koyama paper revision coordination" (32f5fbb1) at 05:35 local, was lost when
this session rewrote todo.md at ~11:00; reconstructed from that session's
transcript + its 13:14/20:14Z status reports. The pre-existing Aug-15/16
"Expansion run" todo content is safe in git at f4722a5:tasks/todo.md.]

Context: Koyama approved all 4 decisions from the 2026-08-16 packet, proposed
Stage-1 submission to Experimental Mathematics / Math. of Computation (Stage-2
analytic paper is his, next year); asked for (a) a Zenodo DOI for the
computational package and (b) the final TeX for his quick review.

- [ ] T1 (owner) Reply to Koyama agreeing to Experimental Mathematics as
      Stage-1 target; draft ready for review before sending.
- [x] T2 Kaggle token works (stale 401 note); no new token needed.
- [ ] T3 Independent frontier replication: 12h monolithic kernel
      farey-frontier-indep CANCELLED at the ~12h wall; TAKEN OVER by d132431f
      — split kernels part1/part2 pushed 2026-08-26 ~15:45, part3 queued
      behind the 5-CPU-session cap (poller pushes it when a slot frees).
      On landing: merge_parts.py, compare_curves.py vs curve_3e14.tsv, exact
      72/72 grid-point agreement required, REPLICATION receipt, drop the
      "one run" caveat from §Data-and-code.
- [x] T4 Zenodo package staged: output/koyama_final_2026-08-26/zenodo/
      prime-races-computational-package (checksums verified, 567/567 baseline
      PASS, .zenodo.json CC-BY-4.0). Upload/DOI = owner; then swap placeholder.
- [x] T5/T5b TeX pass done: arXiv:2607.28931 cited, Zenodo DOI placeholder in
      §Data-and-code, Exp.Math reframe; 8pp compile clean.
- [ ] T6 Send Koyama final TeX + PDF + changelog; both-authors-approve gate
      before any arXiv/journal action. Reply states the finite-x mollified
      plot stays excluded (agreed omission, not silent).
- [ ] T7 Exp.Math submission: format OK (amsart accepted), cover letter
      drafted (cover_letter_draft.md); submission behind T6 gate; agree who
      submits.

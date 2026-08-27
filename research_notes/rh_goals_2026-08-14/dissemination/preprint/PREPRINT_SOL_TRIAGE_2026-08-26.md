# Triage of the sol adversarial report (42 defects) — 2026-08-26

Frontier triage of PREPRINT_SOL_ADVERSARIAL_2026-08-26.md. Owner directive:
"run the triage and start the rewrite."

## Governing decision (resolves defect 1's fork)

**The rewrite is the q=5 certified-computation paper** (sol's option B).
Rationale: it matches what is actually proved — two interval-certified
transfer-operator zeros for G_5, an upgrade of Strömberg 2008's explicitly
non-rigorous numerics — and it answers the preprint requests honestly.
The fixed-q analytic LAW is NOT claimed as a theorem; it appears only as a
motivational remark, explicitly conditional, with the Selberg/Hejhal/Kelmer
question stated openly. The model-theoretic apparatus (axioms A, models,
Metatheorems I–III, decision table, "Sel90-independence") is deleted
entirely, not repaired.

Fact-checks performed before triage (frontier, this session):
- main.tex:215 does say "winding $=1$ so each zero is simple" — defect 7 REAL.
- main.tex:992 caption ends "Not yet rendered." while \includegraphics
  renders fig1_qop_hist.pdf — defect 34 REAL.
- main.tex:27 DRAFT date line; :1107 drafting-checklist section — defect 42 REAL.
- zenodo_package/certificates/pin2_second/W_ENVELOPE_CERT_S2_RECEIPT.json has
  N_evaluation=48; the merged N=288 receipt
  (lane_g/kaggle_s2_contour/chunk_receipts/S2_MERGED_CONTOUR_RECEIPT.json,
  merged_winding=1, two-seat refereed: S2_MERGED_REFEREE_FABLE.md /
  S2_MERGED_REFEREE_SOL.md, unanimous PROMOTABLE-WITH-CORRECTIONS) is NOT in
  the archive — defect 9 REAL; repairable (artifact exists).

## Dispositions

Legend: ACCEPT-PIVOT = resolved by deleting the framing in the rewrite;
ACCEPT-FIX = concrete repair in the rewrite; ACCEPT-DISCLOSE = repaired by
honest scoping language; DEFER-OWNER = needs an owner decision.

### BLOCKING
1. ACCEPT-PIVOT — decision/independence language withdrawn everywhere;
   paper retitled around the certified computation.
2. ACCEPT-PIVOT — LAW demoted from theorem to a conditional remark (open
   question stated: is the fixed-q LAW an immediate corollary of
   Selberg/Hejhal/Kelmer in orbifold generality?).
3. ACCEPT-PIVOT — axiom system deleted.
4. ACCEPT-PIVOT — A4/H3 transfer no longer claimed (moot after pivot); the
   broken-joint finding is banked for any future analytic note.
5. ACCEPT-PIVOT — breadth lemma deleted.
6. ACCEPT-FIX — theorem-delta literature table added (Selberg 1990, Hejhal,
   Kelmer 2015, Phillips–Sarnak, Garbin–Jorgenson, Strömberg 2008, MMS,
   Möller–Pohl, Adam–Pohl, FJS 2021, Jorgenson–Smajlović); novelty claim
   narrowed to: first *certified* (interval-arithmetic, argument-principle)
   localization of G_5 transfer-operator zeros, vs Strömberg's heuristic
   numerics.
7. ACCEPT-FIX — simplicity stated only for det(1−L_{s,+}); Z_{G_5}
   multiplicity stated as ≥ that of the + factor. (Same fix as first
   referee's D-1; the sentence at :215 had survived — regression.)
8. ACCEPT-FIX — the 13-joint chain becomes an explicit dependency
   proposition: each joint labeled CERTIFIED (Arb receipt), CITED (exact
   published theorem, hypotheses checked in-line), or OPEN. The
   scattering/no-line consequence is stated as conditional on the CITED+OPEN
   joints, clearly severed from the unconditional two-pin theorem.
9. ACCEPT-FIX — archive to include S2_MERGED_CONTOUR_RECEIPT.json (N=288),
   the 16 chunk receipts, and both merged-referee reports; data-availability
   statement rewritten to describe exactly what is included. DOI minting =
   DEFER-OWNER (upload is owner-gated).
10. ACCEPT-PIVOT — BBM/Berry–Keating audit deleted.

### MAJOR (11–33)
11–17. ACCEPT-PIVOT — metatheorems, decision table, P_naive, arithmeticity
   corollary, "Sel90-independence" terminology, A6, axiom scope notes: all
   deleted with the framing.
18. ACCEPT-FIX — Lean paragraph rewritten to actual strength: "the Lean
   artifacts formalize elementary conditional implications between stated
   hypotheses; no analytic or spectral content is formalized."
19. ACCEPT-DISCLOSE — multiplicity convention of the Lean statement
   disclosed next to the theorem it accompanies.
20–21. ACCEPT-FIX — new title/abstract; abstract delivers the certified
   theorem in the first two sentences.
22. ACCEPT-PIVOT — process ledgers, standing sentences, internal chronology
   removed; lab-notebook register dropped.
23. ACCEPT-PIVOT — Appendix A deleted (LAW no longer a theorem).
24. ACCEPT-PIVOT — Kelmer erratum claim deleted.
25. ACCEPT-PIVOT — q=8 section deleted (open computation; may return in a
   future paper when certified).
26. ACCEPT-PIVOT — prime-geodesic remark deleted.
27. ACCEPT-FIX — related-work section built around the table of defect 6.
28. ACCEPT-FIX — self-containment: transfer operator, Selberg zeta, and the
   certification pipeline defined in the paper; a reader can verify the
   two-pin theorem from the paper + archive alone.
29. ACCEPT-PIVOT — unread-source declarations deleted; every remaining
   citation is load-bearing and checked.
30. ACCEPT-FIX — data-availability statement made true (see 9).
31. ACCEPT-FIX — bibliography completed (journal refs where published,
   arXiv ids elsewhere; no bare internal paths).
32. ACCEPT-PIVOT — Selberg-class paragraph deleted.
33. ACCEPT-FIX — target ~8–10 pages: method + theorem + dependency
   proposition + literature table carry the weight.

### MINOR (34–42)
34. ACCEPT-FIX — caption regression fixed ("Not yet rendered." removed).
35. ACCEPT-FIX — \shorttitle/running head set.
36. ACCEPT-FIX — hidelinks.
37. ACCEPT-FIX — "Hecke triangle group G_q with q < ∞" phrasing; "finite
    Hecke group" dropped.
38–39. ACCEPT-FIX — resonance defined at first use; notation table ordered
    before use; collisions renamed.
40. ACCEPT-PIVOT — decision table deleted.
41. ACCEPT-FIX — artifact paths moved to the data-availability section as
    archive-relative paths.
42. ACCEPT-FIX — front/back matter reduced to submission material;
    checklist removed from the tex (kept in repo notes).

### Refutations
None. Every fact-checkable claim sol made was verified true. (Its round-5
counterpart on T1 contained numerical errors; this report contains none we
found.)

## Rewrite plan
- New file main_v2.tex alongside main.tex (main.tex frozen as the refereed
  draft-of-record). Drafter: grok xhigh; frontier verification pass +
  compile before presenting. Cold referee on v2 after owner read.
- External-expert binary question (repair item 12) = DEFER-OWNER: requires
  sending the manuscript out; owner decides recipient.

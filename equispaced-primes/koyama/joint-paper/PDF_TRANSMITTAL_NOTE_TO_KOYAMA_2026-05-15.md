> ⚠️ **SUPERSEDED — DO NOT SEND.** Stale: cites "≈18 pp / 181.90 KiB"
> and an "unconditional in our computational range … the one we make
> in §X.5.4" framing that was **corrected** 2026-05-15 (that exact
> overclaim was removed from §X.4.2/§X.5.4/App. B; PDF is now 20 pp).
> Use `REPLY_TO_KOYAMA_2026-05-15_PDF.md`. Kept for history only.

# Transmittal note — updated paper.pdf (draft, 2026-05-15) [SUPERSEDED]

Short note to accompany the `paper.pdf` attachment Koyama requested
(reply of 2026-05-15) for use in his current grant application.
Purpose: ensure any wording he lifts for grant reviewers inherits
the correct conditionality / proof-state labelling. Send only after
review.

**Attachment:** `paper.pdf` (≈ 18 pp, 181.90 KiB) — the post-review
build, reproducible via `python3 clean.py && tectonic paper.tex`
from the markdown sources in `handoff-2026-05-12-paper-prep/recent/`.

---

**Subject:** Updated §X bundle PDF — attached

Dear Shin-ya,

Thank you — and congratulations on the grant application. The
updated 18-page PDF is attached. Please use any of it freely;
two precise phrasings, in case they help when quoting to reviewers:

- **Lean 4 status.** The accurate headline is *"10-file Lean 4
  project; 8 files fully proved and machine-checked; 2 remaining
  `sorry`s, both the Dirichlet Polynomial Avoidance Conjecture at
  general $K$ (diagnostically LI-class); no `axiom`s, verified by a
  cumulative `#print axioms` audit."* Unconditional DPAC for
  $K \in \{2,3,4\}$ (`dpac_le_4`) is fully proved.

- **The $10^{8}$ verification.** The corrected $B_\infty$ identity
  is numerically verified across three $K$-scales spanning two
  decades, up to $K = 10^{8}$. The associated $K^{-1/2}$ decay rate
  is RH-conditional in general (character analogue of
  Soundararajan 2009); it is *unconditional in our computational
  range* because RH for $L(s,\chi)$ is numerically verified well
  beyond our $K$-heights for the four characters. Both framings are
  defensible to reviewers — the second is the stronger claim and is
  the one we make in §X.5.4.

Everything else in the PDF is as we discussed. No rush on the
Phase-1 reconciliation or the §1.1A / Conjecture 2 material — after
May 20 is perfectly fine.

Best,
Saar

---

## Notes

- The two bullets exactly match §X (post nine-finding adversarial
  sweep, 2026-05-14) and `LEAN_SORRY_STATUS.md`. They are stated so
  that a reviewer-facing paraphrase cannot accidentally overclaim
  unconditionality or the Lean proof state.
- No technical claim changed since the 2026-05-14 reply he already
  acknowledged; this note is purely a labelling safeguard for the
  external (grant-reviewer) audience.
- If Saar prefers a barer cover ("PDF attached, use freely"), the
  two bullets can be dropped — but they cost three sentences and
  remove the only third-party-exposure risk in the bundle.

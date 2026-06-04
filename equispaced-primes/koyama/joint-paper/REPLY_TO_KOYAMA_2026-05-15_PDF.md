# Reply to Shin-ya — updated PDF attached (draft, 2026-05-15)

Very brief cover reply for the `paper.pdf` Koyama requested for his
grant application. **Supersedes** the now-stale
`PDF_TRANSMITTAL_NOTE_TO_KOYAMA_2026-05-15.md` (that note quotes
"≈18 pp" and an "unconditional in our computational range"
phrasing that has since been corrected — do not send it).

**Attach:** `handoff-2026-05-12-paper-prep/recent/latex/paper.pdf`
(20 pp, ~202 KiB, built 2026-05-15). Single attachment recommended.

---

**Subject:** Updated §X draft — attached

Dear Shin-ya,

Congratulations again on the grant application — the updated draft
is attached. It is the self-contained **§X technical/computational
section plus the two proof appendices** (20 pp); the joint Abstract
and Introduction remain ours to finalise after the 20th, so they
are deliberately not in this file.

Two phrasings, in case they help when quoting to reviewers:

- **Lean 4.** *"A 10-module Lean 4 / Mathlib (v4.28.0)
  formalisation; 8 of the 10 fully machine-checked with no
  `sorry` and no `axiom` (cumulative `#print axioms` audit); the
  2 remaining `sorry`s are both the Dirichlet Polynomial
  Avoidance Conjecture at general K. Unconditional, fully proved
  DPAC for K ∈ {2,3,4}."*

- **The 10⁸ verification.** *"The corrected B∞ identity is
  numerically verified across three K-scales to K = 10⁸, in two
  independent software stacks."* The associated K^(−1/2) decay
  rate is RH-conditional (character analogue of Soundararajan,
  Crelle 2009); in our K-range it is the operative rate because
  the relevant zeros are numerically verified on the critical
  line. I've phrased it in §X.5.4 as exactly that — not as an
  unconditional theorem — so anything lifted verbatim stays
  referee-safe.

One note for the novelty wording in a panel context: the static
Farey–Mertens "bridge" identity is classical (Mikolás 1949); what
is genuinely ours is the *differential, per-step* refinement and
the formalisation. §X.6 now states this provenance explicitly, so
the draft is self-consistent on that point — worth preserving the
same distinction in the Introduction when we get to it.

Your m-convention and the §2/§3 titles are noted for the
post-20th integration. No rush.

Best,
Saar

---

## Attachment recommendation

- **Send only `paper.pdf`.** It is self-contained; §X.6 already
  carries the Lean headline + axiom audit, so no separate Lean
  file is needed for a grant context.
- **Offer, don't attach:** `LEAN_SORRY_STATUS.md` (per-`sorry`
  detail) — mention it is available if a reviewer wants
  module-level granularity, rather than attaching it by default.
- **Do not include:** the stale transmittal note, the source
  bundle, run logs, or the README — all are noise for a
  grant-stage email.

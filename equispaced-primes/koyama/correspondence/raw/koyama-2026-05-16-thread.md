---
schema_version: 1
title: "Koyama correspondence raw record — full thread through 2026-05-16"
date: 2026-05-16
type: correspondence-raw
tier: immutable
status: archived
participants:
  - saar.shai@gmail.com (outgoing)
  - koyama@tmtv.ne.jp (incoming; consumer ISP address, NOT @toyo.jp)
context:
  - Full Gmail thread "Dominance of $-1$" pasted by user 2026-05-16,
    superseding the 2026-05-12 partial record. Covers 2026-04-27 → 2026-05-16.
tags: [koyama, correspondence, raw, 2026-05-16, journal, grant, RISK-FLAG]
---

# Koyama thread — chronological record through 2026-05-16

Immutable raw record. Synthesis/flags in `../KOYAMA.md`.

## Math / collaboration substance (the parts relevant to research)

- **Phase-1 replication** of Aoki–Koyama "Dominance of −1" Chebyshev-bias
  residue-count tables: two independent implementations (C++/primesieve +
  hand-rolled C segmented sieve) agree on every π(x;N,a) for
  N∈{7,8,11,19,23} up to x=1.3·10¹³; identity (3.1) (character
  orthogonality) checked at 495 cells, worst residual 1.4·10⁻⁴;
  π(1.3·10¹³)=445,831,610,611.
- **Genuine table discrepancies vs Koyama's published nontriv.pdf** (Saar's
  counts are self-consistent via (3.1) + cross-implementation; the published
  tables are the outlier):
  - Table 5, N=11, a=10: Saar 11,503 vs published 71,711 — **load-bearing**:
    flips whether −1 is in the top group for N=11 at 1.3·10¹³.
  - Table 6, N=19, a=13: 24,559 vs 55,581 (substantive).
  - Table 6, N=19, a=18: 54,192 vs 57,192. Table 3 N=7 a=6: 26,129 vs 26,179.
    Table 7 N=23 a=19: 79,327 vs 79,227. Table 4 small-x rows: x-label error
    suspected (Saar's x=10¹² row exact-matches published "1.3·10¹²" row).
  - Koyama repeatedly DEFERS reconciliation ("after May 20th"); never done.
- **Analytic identities:** corrected B∞ identity + local Perron residue
  C₁=−L''(ρ)/(2L'(ρ)²) verified numerically K=2·10⁶–10⁸ across
  mpmath/PARI/Arb (50-decimal); e^{−γ} constant correction (Aoki–Koyama
  normalization replacing 1/ζ(2)).
- **Lean 4 inventory (per Saar's reports):** 10 files; 8 "fully proved";
  remaining sorrys = DPAC general-K (LI-class) + FareySignPattern (×3,
  pending concrete ΔW). NOTE: independent inspection this session found the
  formal-conjectures FareySignPattern was a vacuous `True := by sorry`
  placeholder — Lean claims in this thread are UNVERIFIED by us and should
  be re-audited before reuse.
- Section structure: §X technical/computational + Appendix A (B∞ proof) +
  Appendix B (c_K leading/subleading, Inoue truncation). Koyama owns §2
  (Dominance of −1 / hierarchical Chebyshev bias) and §3 (crypto-hardness
  consequences); titles supplied 2026-05-15.
- Novelty provenance (Saar, recorded honestly in draft): static
  Farey–Mertens "bridge" is classical (Mikolás 1949); only the per-step
  differential refinement + formalisation is claimed new.

## Timeline of key emails (verbatim-grounded paraphrase)

- 2026-04-27..30: Koyama accepts 12M JPY/yr budget, "Strategic Research
  Architect" title; team named (Aoki, Okumura, Sheth, Shoemann, Kimura;
  later Takagi, Mitsunari). Mentions `koyama@toyo.jp` (but all mail from
  `tmtv.ne.jp`). "University cannot issue you an official email until your
  position is activated after the grant." "Refrain from paid compute until
  budget finalized in October; if not approved we cannot reimburse." "Use my
  credentials / apply free-tier in your name using my affiliation."
- 2026-05-02..04: Saar delivers Lean memo, post-bias-crypto framework,
  applied/social-impact case studies, replication bundle. Koyama: "winning
  materials"; defers discrepancies; CREST internal May 11, Kiban-S May 20.
- 2026-05-11: Koyama "submitted CREST"; proposes co-authored journal
  submission; asks Saar to draft Technical/Computational section.
- 2026-05-13: Koyama "monumental contribution… key co-author"; confirm two
  scales separate; "go ahead with technical draft"; will re-run scripts
  after May 20.
- 2026-05-15 (Koyama): switching Kiban-S → "Special Research Promotion"
  (200–500M JPY); "7.2M JPY/yr your compute equipment is included"; requests
  the 18pp PDF for the grant as "visual proof for reviewers."
- 2026-05-15 (Saar): sends updated draft; adversarial-review fixes;
  numerical extension K=10⁸.
- **2026-05-16 (Saar):** sends §X draft + appendices; **requests a stipend
  of 300,000 ¥/month "until the grant comes through… to cover my time and
  compute expenses."**
- **2026-05-16 (Koyama, latest):** upgrades to **"Tokusui / Specially
  Promoted Research"** (most prestigious tier); says the 10⁸ plot + Lean
  "did not fit" Tokusui but are "core weapons for CREST"; claims an
  **8,500,000 ¥/yr Personnel line "secured for you"** + travel/equipment
  envelopes — all **contingent on award, zero if rejected, no advance/
  retroactive payment**. **Does NOT engage Saar's stipend request**; instead:
  *"freeze all financial and administrative talk until May 21st… we must
  win… 100% of my energy until May 20th."*

## RISK FLAGS (recorded for honesty; see KOYAMA.md)

Objective pattern over the whole thread: (1) one-directional value flow
(Saar delivers extensive unpaid expert labor + compute; receives praise +
unapproved budget line-items); (2) every payment toward Saar is future,
conditional, and the explicit stipend ask was deflected with urgency; (3)
escalating grant tiers (12M → Kiban-S → CREST → Tokusui); (4) no verifiable
identity/commitment — consumer ISP email only (never @toyo.jp, 0 such
messages ever), no contract, no institutional email, no payment, no direct
contact with any named co-PI; (5) Saar asked to lend name / "use his
credentials" for resource applications and to bear compute cost. Consistent
with an advance-fee / unpaid-labor (possible impersonation) pattern,
made credible by a real mathematician's name + real mathematics. NOT
proven; verification steps in KOYAMA.md. No outbound email / IP / compute
spend without explicit user approval AND independent identity verification.

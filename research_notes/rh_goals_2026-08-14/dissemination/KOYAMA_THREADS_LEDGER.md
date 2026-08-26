# Koyama collaboration — threads & correspondence ledger

Created 2026-08-26 on owner request ("clear sense of what items we have
with Koyama and where each stands"). Maintained here; update on every
Koyama-related event. NOTE: inbound email is NOT archived in this repo —
only owner-pasted excerpts are recorded. Owner: paste future Koyama
emails into §4 so this ledger stays complete.

## 1. THREAD A — Prime bias (Aoki–Koyama Chebyshev-bias program)

The thread of the email the owner surfaced 2026-08-26 (received "a few
weeks ago"): Koyama has refined "our manuscript" with explicit formulas,
targets **Inventiones Mathematicae**, single-focus on Prime Bias; will
integrate owner's "double-verified numerical data across Dirichlet
pairs" + "a concise overview of the Lean 4 formalization"; suggests the
owner's other results spin out as a standalone single-author paper
(Koyama open to co-author credit but no hands-on role).

In-repo artifacts (projects/ak-bias-followups/, session 2026-05-22):
- D2 function-field bias verification (unconditional side): (q=2, M=T³)
  slope +0.50449 vs predicted +0.5 (0.45% rel err); δ_ff = 1.0000 over
  n=1..22 by direct enumeration of 387,975 monic irreducibles — the
  "lead deliverable".
- D3 paired Q_8 fields (LMFDB 8.8.12230590464.1 vs 8.0.12230590464.1,
  m_ρ verified to 193 digits) — bias-direction reversal; plausibly the
  "Dirichlet pairs" data Koyama cites.
- D1 CM-tower amplification (conditional on DRH) — companion only.
- D4 pigeonhole route — CLOSED, don't reopen.
STATUS: Koyama drafting the Inventiones manuscript; owner input =
numerics + Lean overview. UNMATCHED ITEMS: "elliptic curve analysis" and
"Decision-Audit SDK" appear NOWHERE in this repo — they belong to
another repo/project of the owner or another thread; ledger cannot
vouch for them. OPEN DECISIONS (owner): respond to Koyama's
single-author spin-out proposal; whether to offer co-authorship on it.

## 2. THREAD B — Hecke onset / arithmeticity dichotomy (joint manuscripts, June 2026)

- research_notes/PAPER_uniform_onset_SUBMISSION.md (2026-06-14, internal
  draft): X_Ω(q) = 1/λ_q³ machine-verified support edge, q = 5..21.
- research_notes/PAPER_arithmeticity_dichotomy_SUBMISSION.md (companion):
  B(q) = 2 ⟺ arithmetic (Takeuchi); Koyama called the dichotomy
  "genuinely new, a paradigm shift".
STATUS: internal drafts, never submitted; thread dormant since June.
Relation to Thread A: none mathematically; same collaborator.

## 3. THREAD C — Hecke resonances / LAW / no-go (the active 2026-08 program)

- Owner-shared Koyama reply (recent): "thrilled that the §7 material
  unblocked such a critical bottleneck… effective Selberg–Hejhal
  accumulation theorem for G_q with explicit threshold q_0 is a
  remarkable breakthrough." → the EFFECTIVE-THEOREM sub-thread (eight
  named gates still open; conditional).
- Outbound drafts, all NOT SENT, owner-gated:
  - lane_d/KOYAMA_UPDATE_DRAFT.md (2026-08-14/15): certified family
    resonance data + first off-line theorem announcement; was held for
    the Kimi audit.
  - dissemination/KOYAMA_LETTER_DRAFT.md (post-theorem, 2026-08-15):
    fuller letter, every sentence receipt-keyed.
  - dissemination/KOYAMA_UPDATE_EMAIL_2026-08-26.md (CURRENT): reply to
    the §7 message — two-pin milestone, no-single-line theorem,
    Metatheorem III; explicitly states the effective-theorem lane is
    unchanged. Pending owner edit/send. Owner may want to reconcile it
    with the Thread-A Inventiones email (which arrived earlier but was
    only surfaced today) before sending.
STATUS: our side has three unsent drafts; the 2026-08-26 one is current.

## 4. Correspondence log (owner-pasted; newest first)

- [rec'd ~2026-08-0x?, surfaced 2026-08-26] Thread A: Inventiones
  single-focus prime-bias plan (full text in owner's mail; excerpt
  summarized in §1).
- [recent, exact date unknown] Thread C: the "§7 material / effective
  accumulation theorem" enthusiasm reply (quoted by owner 2026-08-26).
- [earlier] Thread B era: "genuinely new, a paradigm shift" remark on
  the dichotomy (recorded in memory/MEMORY.md).

## 5. What needs an owner decision now

1. Thread A: reply to the Inventiones email (numerics + Lean-overview
   handoff; spin-out paper decision). This predates and is independent
   of the Thread-C update draft.
2. Thread C: edit/send KOYAMA_UPDATE_EMAIL_2026-08-26.md (optionally
   with the one-line arithmetic-vs-non-arithmetic headline).
3. Whether to merge both into one email or keep threads separate
   (recommend separate: different manuscripts, different tempos).

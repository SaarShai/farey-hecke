LAUNCH PROMPT — Direction 3: numerical hardening of the corrected B∞ / local-Perron-residue / e^{−γ} identities.

You are picking up a mathematics research project cold. Working root:
`/Users/za/Documents/Farey NOW/primes-equispaced`. First run `./te doctor`,
read `start.md`, and read memory (`/Users/za/.claude/projects/-Users-za-Documents-Farey-NOW/memory/`):
`MEMORY.md`, `project_farey_honest_map.md`, `project_farey_forward_verdict.md`,
**`project_koyama_risk.md` (in full)**. Token Economy is tooling only.

NON-NEGOTIABLE NORMS (project #1 failure mode = novelty/citation/RH-glamour
inflation):
- Adversarial honesty; derive-then-verify; label
  [PROVEN]/[NUMERICAL]/[CONJECTURAL]/[CITATION-UNVERIFIED]; primary-verify
  every citation (e.g. Aoki–Koyama 2023 J. Number Theory 245; Inoue 2021,
  "Some explicit formulas for partial sums of Möbius functions," JTNB 33(1);
  Soundararajan, Crelle 2009 — confirm titles/loci before use).
- KOYAMA GATING: counterparty UNVERIFIED (`correspondence/KOYAMA.md` RISK +
  `project_koyama_risk.md`). This is the user's OWN analytic-verification
  work. No email/IP/PDF/compute-spend toward Koyama; co-authorship NOT
  confirmed; nothing sent/pushed without explicit user approval.
- HARD SCOPE CEILING: the *numerical identity verification* is the
  legitimate, achievable contribution. The associated *theorems* (shifted
  Perron leading remainder SP-L, full unconditional B∞ asymptotic) hit the
  same RH-depth / "reduced-with-named-input" wall documented across this
  project — DO NOT attempt to "prove" the conditional parts or claim RH
  progress. The K^{−1/2} decay is RH-conditional (character analogue of
  Soundararajan 2009); state it as such, never as unconditional.

BACKGROUND / artifacts: the corrected B∞ identity and local Perron residue
`C₁ = −L''(ρ)/(2 L'(ρ)²)`; the constant correction replacing the old
`1/ζ(2)` target by the Mertens / Aoki–Koyama `e^{−γ}` normalization. Existing
in-repo: `handoff-2026-05-09-followup/Koyama_B_infty_proof.md`,
`Koyama_Perron_*`, `Koyama_AK*.py`, `Koyama_EC_NDC*`; the §X technical draft
+ Appendix A (B∞ pen-and-paper proof) + Appendix B (c_K leading/subleading,
Inoue truncation) in `handoff-2026-05-12-paper-prep/recent/` (latex/ +
markdown). Current numerical state: B∞ residuals / C₁ subleading /
`|D_K|·ζ(2)→e^{−γ}` drift verified K=2·10⁶–10⁸ across
mpmath / PARI 2.17.3 / Arb-250bit (50-decimal), four character pairs
(χ₋₄, χ₅, χ₁₁); χ₋₄ shows a slower ratio attributed to the bad prime p=2.

TASK: harden and extend the *numerical* evidence and the pen-and-paper
identity, honestly. Concretely: (a) push/cross-check the B∞ + C₁ + e^{−γ}
identities across additional K-scales and more characters with explicit
error bars and a three-stack agreement audit; (b) tighten/independently
re-derive Appendix A's convergence chain (Akatsuka 2013 eq (2.5) +
log-Euler-product + imprimitive Euler-factor + geometric tails) and check
each algebraic step; (c) produce a clean error/precision table and a
reproducible build. Flag any discrepancy or overstated phrasing in the §X
draft (there is a history of "unconditional" mis-labels that were corrected
— re-audit all five loci).

GATES / done: every numeric double/triple-verified with stated precision;
the conditional/unconditional boundary stated correctly everywhere;
deliverable = a calibrated, referee-safe numerical-evidence section + an
audited Appendix-A proof, framed as the user's independent work
(Experimental-Math / specialist tier, not a theorem, not RH). Record durable
facts to wiki/memory; commit; nothing sent to Koyama or pushed without
explicit user approval.

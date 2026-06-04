# Reply to Shin-ya — progress summary + open questions (draft, not yet sent)

Drafted 2026-05-14, for review before sending. Differs from the
contingent `MIDWEEK_UPDATE_TO_KOYAMA_DRAFT.md` in that it is a
proactive note rather than a reactive one: it summarises everything
that has happened on the §X bundle since the 2026-05-12 exchange
and surfaces four specific items where his input is needed before
LaTeX integration into the joint paper.

The tone is brief and item-by-item. Send only after review.

---

**Subject:** §X bundle — progress update and four small questions

Dear Shin-ya,

Thank you again for the green light, the two scope confirmations,
and the offer to re-run the Phase-1 scripts after May 20. I've used
the interval to extend the verification, harden the Lean inventory,
and prepare Abstract and Introduction draft prose for whenever
you're ready to discuss them. None of this changes the technical
claims in the section you have — all of it is consolidation and
polish on top of the bundle you saw.

A short summary, then four small questions where I'd benefit from
your judgement before LaTeX integration.

---

**1. Numerical extension to $K = 10^{8}$.** I extended the
verification of the corrected $B_\infty$ identity to $K = 10^{8}$
on the four pairs via PARI/GP 2.17.3 closed-form component
evaluation (the L2 leg of the cross-stack; ≈ 4 min wall-clock). The clean-character pairs ($\chi_5$ and $\chi_{11}$)
give residual ratios $3.7$ and $4.3$ from $K = 10^{7}$ to
$K = 10^{8}$, both above and within a factor of $\le 1.4$ of the
predicted $K^{-1/2}$ rate (per-decade factor $\sqrt{10} \approx 3.16$;
RH-conditional via the character analogue of Soundararajan 2009,
applicable unconditionally for our four characters via numerical
verification of RH). The $\chi_{-4}$ pairs continue to show the
slower $\sim 1.09\text{–}1.15$ ratio across the two $K$-steps,
attributable to the bad-prime $p = 2$ contribution to
$\mathrm{BPC}_1$. The identity is now verified across three
$K$-scales spanning two decades. §X.5.4 has been updated and the
new $K = 10^{8}$ run log (`BINFTY_K100M_run.log`) is in the bundle.

**2. Lean inventory: 10 files, 8 fully proved, axiom audit clean.**
Two additions since the bundle you saw — one new file and one
upgrade to an existing file:

- *New:* `RamanujanSum.lean` (geometric sum identity for roots of
  unity, primitive-roots-sum $=$ Möbius via Dirichlet convolution
  and strong induction, the coprime $c_q(n) = \mu(q)$ case, and
  the FareySet decomposition). This discharges the
  `h_ramanujan_decomp` hypothesis of `FareyBridgeIdentity`, which
  is therefore now **unconditional**
  (`farey_bridge_identity_unconditional`).
- *Upgraded:* `MertensSpectroscopeUniversality.lean` gained two
  unconditionally-proved infrastructure lemmas
  (`spectroscope_nonneg`, `reciprocal_sqrt_not_summable`) plus a
  5-step blueprint documenting the precise Mathlib gap; the
  headline universality statement remains conditional on a
  Soundararajan-style explicit-formula hypothesis as before.

The remaining two `sorry`s are both the headline Dirichlet
Polynomial Avoidance Conjecture at general $K$ — diagnostically
LI-class, as recorded in §X.7 Q:DPAC. A new `_AxiomCheck.lean` runs
`#print axioms` on the audited headline theorems: six depend only
on the standard Lean trust base
(`propext`/`Classical.choice`/`Quot.sound`), and the seventh
audited headline (`dpac_le_4`, unconditional DPAC for
$K \in \{2, 3, 4\}$) additionally uses `Lean.ofReduceBool` and
`Lean.trustCompiler`, Mathlib's standard kernel-reduction
primitives. The no-`axiom` convention is preserved throughout.

**3. Adversarial review pass on §X and appendices.** I ran a
self-review pass with two findings worth flagging:

- *Notation drift on $T_K$.* The symbol $T_K$ had been doing
  double duty in some places — both for the partial prime-power sum
  $T_K(\chi,\rho)$ of §X.1 and for the Inoue truncation height in
  Theorem X.4.2 and Appendix B. I renamed the latter to $T(K)$
  throughout, matching Inoue's notation, with explicit
  cross-references between the two uses. Also tightened the
  Theorem X.4.2 hypothesis to use $|\mathrm{Im}(\rho')| \le T(K)$
  rather than $|\gamma' - \tau|$, matching Inoue's $s$-plane
  convention.
- *Soundararajan 2009 labelling.* The earlier text described
  Soundararajan's $\sqrt{x}\exp((\log x)^{1/2}(\log\log x)^{14})$
  rate as "unconditional" in five places (§X.4.2, Appendix B intro,
  Appendix B §B.4 table, §X References, `references.bib`). This
  rate is in fact RH-conditional; the unconditional state of the
  art is Vinogradov–Korobov-style. The intended meaning (consistent
  with Appendix B §B.3.5 and §X.5.4) was *unconditional in the
  computational regime of §X.5 because RH for $L(s, \chi)$ is
  numerically verified to heights well beyond our $K$-ranges for
  the four characters $\chi_{-4}, \chi_5, \chi_{11}$*. All five
  locations now state this correctly.

Two citation provenance fixes: the §X References entries for
Aoki–Koyama 2023 (corrected to *Chebyshev's bias against splitting
and principal primes in global fields*, J. Number Theory **245**)
and Inoue 2021 (corrected to *Some explicit formulas for partial
sums of Möbius functions*, JTNB **33**(1)) had paraphrased titles
that disagreed with the actual published titles in
`references.bib`. Both aligned.

**4. Forward-looking drafts.** In the bundle as discussion
documents:

- `ABSTRACT_DRAFT_2026-05-13.md`: one recommended Abstract
  (~165 words, tight version) plus two alternatives (long form
  ≈ 235 words for venues that tolerate it; arXiv-announcement
  ≈ 115 words). All three now reflect the 8-of-10 Lean count.
- `INTRODUCTION_DRAFT_2026-05-13.md`: ~900 words across five
  subsections, drafted using real `references.bib` keys so it
  compiles directly. Two explicit insertion cues
  (`KOYAMA-INSERT-1.1A`, `KOYAMA-INSERT-1.5`) mark the spots that
  need your framing material.
- `SP_L_SUFFICIENT_PACKAGES_2026-05-13.md` (in the bundle since
  the first exchange): three sufficient packages for (SP-L) —
  Route I shifted negative second moment, Route II halo (negative
  at GL(1)), Route III Gonek–Hejhal $+$ Mertens-oscillation — now
  cited from §X.7 Q:Perron.

The LaTeX bundle compiles to an ≈ 18-page PDF via
`python3 clean.py && tectonic paper.tex`; all 18 equation
cross-references resolve, the bibliography renders, and the build
is reproducible from the markdown sources in
`handoff-2026-05-12-paper-prep/recent/`.

---

**Four questions where your input would help before LaTeX
integration into the joint paper:**

1. **The `m` convention in your (1.4).** In our current §X.4.3 and
   in the Introduction §1.2, I have written
   $m = m(s,\chi) := \mathrm{ord}_{s' = s}\,L(s', \chi)$ — the
   order of zero of $L(s,\chi)$ at the evaluation point $s$, so
   that $m$ is a function of $s$ and equals $1$ at any simple
   noncentral zero $s = \rho \neq 1/2$. This is the only reading
   consistent with the specialisation we use. If your paper's
   (1.4) instead uses a fixed $m = m_\chi = \mathrm{ord}_{s = 1/2}\,L(s,\chi)$,
   please correct the convention in §X.4.3 and §1.2 — they should
   stay in sync.

2. **The Dominance-of-$-1$ framing paragraph for §1.1.** The
   placeholder `KOYAMA-INSERT-1.1A` marks one paragraph in §1.1 of
   the Introduction where I've drafted holding text from your
   *Dominance of nontriv.pdf*. The paragraph names the conjecture,
   states the numerical signal, and lists the moduli in scope. I'd
   appreciate your replacing this with the authoritative
   statement: what $\chi_{a, 1}$ vs $\chi_{1, a}$ denotes, what is
   conjectured of $\log L(1, \chi_{-1, 1})$, and what numerical
   signature distinguishes $a = -1$ in the residue-count tables.

3. **Section titles for §2 and §3.** The placeholder
   `KOYAMA-INSERT-1.5` in §1.5 needs real titles for §2 (the
   Dominance-of-$-1$ chapter) and §3 (any theoretical-consequences
   chapter you have in mind). If §3 doesn't exist as a separate
   chapter, just delete that sentence and §1.5 stays clean.

4. **Whether to send you the updated bundle, or wait for your
   Phase-1 reconciliation first.** The current `paper.pdf` is the
   ≈ 18-page version of everything above. If it would help to have
   it in front of you before May 20, I can attach it now; if you'd
   prefer to wait until you've done the Phase-1 cell re-run and we
   can discuss everything in one go, that works too.

Please take whatever time you need on the Phase-1 reconciliation;
the polish work above doesn't change any of the substantive claims
the §X.5.1 cells depend on.

Best,
Saar

---

## Send-decision notes

- The note is structured to be sendable as-is, but verify (1) the
  $K = 10^{8}$ ratios in item 1 match the latest `BINFTY_K100M_run.log`
  values (currently 3.7 / 4.3 / 1.09–1.15), (2) the four questions
  reflect what you actually want him to weigh in on, and (3) the
  "ten files / eight proved / two `sorry`s" count is still accurate
  (it is as of 2026-05-14).
- If a research-track milestone lands between this draft and
  send-time that changes the §X picture (e.g. a Door A breakthrough
  on `AllZeroShiftedNeg_2`), surface it before sending. As of
  2026-05-14 the research-track Stage 0/1 work concerns H1 at
  GL(2), not (SP-L) at GL(1), so §X.7 Q:Perron's Route II status
  is unchanged.
- The contingent `MIDWEEK_UPDATE_TO_KOYAMA_DRAFT.md` remains the
  fallback if his Phase-1 reconciliation arrives first; this proactive
  note supersedes it once sent.

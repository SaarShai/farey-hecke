# Research-track milestone summary for Shin-ya (draft block, not yet sent)

Drafted 2026-05-14. Intended as an added item in the pending
`REPLY_TO_KOYAMA_DRAFT_2026-05-14.md` (it is the "research-track
milestone" the send-decision notes say to surface if the §X picture
changes — it does, for §X.7 Q:Perron and Q:DPAC framing). Register
matches that draft: brief, item-by-item, honest about limits.

---

**5. Research-track milestone — the H1/(SP-L)/DPAC inputs collapse to
one hypothesis.**

A consolidation result on the conditional structure of the section,
not a new unconditional theorem. In brief:

- **No unconditional H1.** I pushed hard on an unconditional offcentral
  H1 bound for fixed $E/\mathbb{Q}$ along ten routes. All reduce to
  thin-strip critical-line density for $L_E^\*$; three apparent
  unconditional bounds turned out to hide GRH and have been retracted in
  our internal record. The honest §X position is unchanged: the
  proved deliverable is the **conditional** halo bound
  $R_\Phi(T) \ll T^{7/4+\varepsilon}$ under GRH for $L_E^\*$. We should
  *not* claim an unconditional H1; a referee would find the hidden GRH.

- **One spine.** The (SP-L) sufficient package of §X.7 Q:Perron (the
  Gonek–Hejhal–type negative second moment, Route I of
  `SP_L_SUFFICIENT_PACKAGES`) and the H1 input are the **same
  functional** $\mathrm{GH}(\Lambda;T)=\sum_{0<\gamma\le T}
  |\Lambda'(\rho)|^{-2}$, at GL(1)/Dirichlet and GL(2)/$L_E^\*$
  respectively (sharp form for (SP-L); soft sub-cubic form for H1).
  §X.7 can therefore cite **one named classical conjecture**
  (Gonek–Hejhal) instead of two bespoke packages.

- **One root, shared with DPAC.** Tracing the soft H1 input through the
  Hadamard gap–derivative dictionary, it is equivalent to a *pointwise*
  no-near-collision statement on the ordinates of $L_E^\*$ — a
  **quantitative-LI / non-resonance** statement. This is the *same
  class* as Q:DPAC at general $K$ (the two remaining Lean `sorry`s,
  already labelled LI-class in §X.7). So a single hypothesis — LI for
  the relevant $L$-spectrum — simultaneously (i) gives unconditional H1,
  (ii) closes the last two Lean `sorry`s, and (iii) feeds the
  $c_K\to e^{-\gamma}$ chain via the spine above.

- **The natural shortcuts are provably closed.** Two scoped barrier
  results: (a) unconditional band-limited pair correlation
  (Rudnick–Sarnak window) is Paley–Wiener-blind to the small-gap tail,
  so it cannot supply the bound; (b) Baker / effective-Diophantine
  methods have no admissible input (the ordinates carry no known
  algebraic/period structure). These are method-obstruction remarks,
  worth at most a footnote — their value is that they stop us, and a
  referee, from expecting an easy unconditional route.

**Net effect on the paper.** No change to any proved claim or numerical
cell. It *strengthens* the framing: §X.7 Q:Perron and Q:DPAC become two
faces of one recognised conjecture rather than separate open ends, and
the two Lean `sorry`s are honestly presentable as *the same root*, not
two unrelated gaps. Full internal derivation chain and confidence
tags are in `handoff-2026-05-14-research-track-split/` (six notes,
2026-05-14).

---

## Honest framing guidance (for Saar, not for the email)

- Lead with the conditional theorem as the deliverable; present the
  unification as a *clarifying companion*, not a breakthrough.
- Do not oversell "another LI-equivalent" — it is incremental in the
  field's eyes; its value here is internal coherence and referee-safety.
- Be explicit that several routes were retracted: Shin-ya will trust the
  record more, not less, for seeing the failed routes named.

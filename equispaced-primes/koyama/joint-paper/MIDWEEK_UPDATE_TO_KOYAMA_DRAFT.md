# Mid-week update to Shin-ya (draft, not sent)

A short follow-up note prepared in advance for when the Phase-1
discrepancy reconciliation arrives (week of May 20). Designed to be
sent within 24h of his reply, summarising what has been done in the
interim and surfacing any decisions that need his input before
LaTeX integration.

The note is intentionally short. Three substantive items plus a
forward look.

---

**Subject:** Status update — week before integration

Dear Shin-ya,

Thanks again for your green light. A brief note on what I've done
in the meantime, all building on the technical/computational
section you've seen, none of it altering its claims.

**1. B_∞ identity verified at one more decade.** I extended the
PARI/GP cross-stack verification of the corrected $B_\infty$
identity to $K = 10^{8}$ on the four pairs (≈ 4 min wall-clock).
The clean-character pairs ($\chi_5$ and $\chi_{11}$) now give
residual ratios $3.7$ and $4.3$ from $K = 10^7$ to $K = 10^8$,
both above and within a factor of $\le 1.4$ of the predicted
$K^{-1/2}$ rate (per-decade factor $\sqrt{10} \approx 3.16$;
RH-conditional via the character analogue of Soundararajan 2009,
applicable unconditionally for our four characters via numerical
verification of RH); the $\chi_{-4}$ pairs continue to show the
slower $\sim 1.09$–$1.15$ ratio across both $K$-steps,
attributable to the bad-prime $p = 2$ contribution to
$\mathrm{BPC}_1$. The empirical decay envelope is now verified at
three $K$-scales across two decades. §X.5.4 in the section draft
has been updated.

**2. Lean inventory tightened.** Ten Lean files in
`formal-conjectures/` now compile under Lean 4.28.0 with **two
`sorry`s** remaining (down from five at the time of my first email);
the two remaining are both the headline Dirichlet Polynomial
Avoidance Conjecture itself, diagnostically LI-class. **Eight of
ten** files are now fully proved. Two additions since the bundle
you have:

- **`RamanujanSum.lean`** — geometric sum identity for roots of
  unity, primitive-roots-sum = Möbius via Dirichlet convolution +
  strong induction, the coprime $c_q(n) = \mu(q)$ case, and the
  FareySet decomposition. This discharges the
  `h_ramanujan_decomp` hypothesis of `FareyBridgeIdentity`, which
  is therefore now **unconditional** (`farey_bridge_identity_unconditional`).
- **`MertensSpectroscopeUniversality.lean`** gained two new
  unconditionally-proved infrastructure lemmas
  (`spectroscope_nonneg`, `reciprocal_sqrt_not_summable`) plus a
  5-step blueprint documenting the precise Mathlib gap (Perron
  inversion, explicit formula for $M(x)$, oscillatory-integral
  partial summation, zero simplicity). The headline universality
  statement remains conditional on a Soundararajan-2009-style
  explicit-formula input as before.

A cumulative `_AxiomCheck.lean` running `#print axioms` on each
audited headline theorem confirms six audited headlines depend only
on the standard `propext`, `Classical.choice`, `Quot.sound` triple;
the remaining audited headline `dpac_le_4` additionally pulls in
`Lean.ofReduceBool` and `Lean.trustCompiler` (Mathlib's standard
kernel-reduction primitives, expected for a theorem that computes
Möbius values at small primes in the kernel). The eighth
fully-proved file, `SmoothedDwfFormula_full`, is a 17-lemma chain
whose component lemmas use only the standard trust base. The
no-`axiom` convention is preserved throughout;
`FareySignPattern.lean`'s pointwise falsifications at
$p = 237{,}733$ and $p = 243{,}799$ are closed under explicit
named hypotheses naming the numerical witnesses.

**3. Supplementary drafts ready for your review.** A sketch
Introduction (≈ 900 words, 5 subsections) and three Abstract
variants are now in the bundle as discussion documents. Both are
framed as starting points to react to, not committed prose. The
Introduction has placeholder cues for your authoritative framing of
the Dominance-of-$-1$ programme; the Abstract drafts can be tuned to
whichever venue you prefer.

**Forward look.** I'm ready to begin LaTeX conversion of the
integrated full paper as soon as you signal which discrepancies
resolved. The whole §X bundle (cover note + section + appendices +
Lean inventory + supporting notes) is in
`handoff-2026-05-12-paper-prep/recent/`; the typeset PDF (≈ 18 pages)
builds reproducibly via `tectonic paper.tex` from the source.

Best,
Saar

---

## Send-decision criteria

Default: do NOT send this proactively. Send only if Koyama's
discrepancy report arrives ON or BEFORE May 20 with material that
materially changes §X.5.1. If he comes back asking "should we keep
going?", reply with this draft as the substantive answer.

If his reply on May 20 instead just confirms a couple of cells and
declines to flag a major change, the note above over-communicates;
strip items 1–3 to the headline bullets and skip the LaTeX-status
paragraph.

## Variants if he reports a substantive cell flip

If Koyama's reply changes the Table-5 $N=11, a=10$ cell from
$71{,}711$ to $11{,}503$ (i.e., agrees with our value), §X.5.1
should be updated to:

> The qualitative dominance signal at $x = 1.3 \cdot 10^{13}$ is
> reproduced for $N = 8$ (strictly) and for $N = 19$ (top group);
> for $N = 11$, the corrected value $a = 10$ shifts $-1$'s rank
> from 2nd to 3rd of 5 non-residues, *out of the strict top group
> at this checkpoint* — consistent with the Aoki–Koyama framework
> if one allows for a transient low-zero deflection like the one
> Koyama identifies for $N = 19$.

If he instead reaffirms his $71{,}711$, §X.5.1 stays as-is and we
note "joint reconciliation pending" as the entry for that cell.

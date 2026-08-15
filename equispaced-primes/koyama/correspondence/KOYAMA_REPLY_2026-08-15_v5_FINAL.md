# KOYAMA REPLY — v5 FINAL (NOT SENT; owner-gated)

Base: the owner's own edit of v4 (pasted 2026-08-15). Applied: all seven
Opus-5 cold-verification fixes (D1 false-claim removal, D4 567/567 scope,
D2/D3 eight cells + N=11/N=23 placement, D5 tables-not-drafted, D6
decades, D7 S̃_T difference notation) + mechanism sentence updated for
M1d/M1e (scattering determinant, 8/8 confirmed predictions at q=4 and
q=6). Everything else left in the owner's wording. v3/v4 superseded.

---

Subject: Re: arXiv upload — thoughts and integration plan

Dear Professor Koyama,

Congratulations on the arXiv posting — securing priority on the
framework now was clearly the right move, and I've read the manuscript
closely. Here are my thoughts.

**The 3×10¹⁴ data.** Our race counts for N ∈ {7, 8, 11, 19, 23} now
reach x = 3×10¹⁴ — well past Table 3's top of 1.3×10¹³ — and up to that
height they reproduce the double-verified baseline exactly (567/567
cells). I should be plain about scope: the extension beyond 1.3×10¹³ is
so far a single run, and I'd want an independent replication of it
before anything from that range goes in the paper. The interesting part
is what the new range shows: even at this height, −1 leads the raw race
only for N = 7 and 23; for N = 8 it is last, for N = 19 actually
negative, and the orderings are still shifting. I see this as the
strongest possible motivation for your regularization: the
fine-structure ranking simply is not visible to unregularized counting
at any reachable height, so the mollified statistic is not a convenience
but a necessity. I'd frame the numerical section that way — it is also
the framing a referee cannot attack. We also traced the transients to
their source: reconstructing the race from the first 25 zeros per
character tracks the observed curves with correlations 0.83–0.97
(0.9925 for N = 19 with 100 zeros), while −1's rank keeps changing — so
the noise is precisely the low-zero fluctuation your mollifier removes.
The reconstruction figure is drafted; I'll produce the extended tables
together with the TeX pass below.

A few things to settle before submission:

1. Theorem 1.4 states C_N depends only on N for fixed T, but (2.5)
   carries a T/(4√π) factor I could not see cancelled, and the
   off-diagonal bound in §2.2 is per-pair, not summed. I think we are
   safer publishing a two-parameter version (T = T(x), explicit
   C_{N,T(x)}) and keeping the fixed-T form as a conjecture — I'd
   rather we submit the theorem we can fully defend.
2. Definition 1.3 prints (1 − χ(a)) while Theorem 1.4 uses (1 − χ̄(a));
   the conjugated form is the correct one (as printed, (1.3) selects
   a⁻¹). Harmless for a ≡ −1, but worth fixing once and propagating —
   I have a small Lean certificate for the corrected identity.
3. The modulus-19 example in Remark 2.3: we found (and certified with
   interval arithmetic) a positive ordinate at γ ≈ 0.0190 for the odd
   character of Conrey index 13, far below the γ ≈ 1.74 used as lowest.
   The e^{33.4} settling estimate should probably be revisited — our
   data independently show the transients still active at 3×10¹⁴.
4. Eight Table 3 cells differ from our recomputed values at the
   1.3×10¹³ grid point — most are small, but N = 11, a = 10 and
   N = 23, a = 22 (that is, −1 mod 23 itself) are large enough to move
   −1's rank for those two moduli. The full cell list is in the memo.
   Could we reconcile against raw class counts before a replacement
   version?

One small protective remark: Conjecture 1.7 concerns L-values, not
prime counts, and I'd say so explicitly — our race data neither support
nor contradict it, and the step from regularized ordering to eventual
raw dominance deserves its own statement.

**Lean scope.** What builds clean today is a formalization of selected
finite and algebraic components — the non-residue symmetry at leading
order (four theorems, zero sorry) and the character-selector identity
from point 2 — and I'd describe it in exactly those modest words, as
one short subsection or an ancillary file. Nothing should suggest Lean
verifies the paper.

**Sequencing.** If you send me the current TeX, bibliography and the
arXiv identifier, I can return the insertion-ready tables, figures and
Lean paragraph within days, and we can reconcile the table cells in
parallel. If you agree, I'd then also compute your mollified statistic
directly from our prime data and certified zero tables — the difference
S̃_T(x, 1) − S̃_T(x, a), as in Theorem 1.4 — for a finite-x comparison
against C_N · log L(1, χ_{1,a}); I suspect that is the sharpest
validation figure the paper could have. I've also prepared a
contribution statement and a short computational-assistance disclosure;
better to have them in the file from the start than to add them under
referee pressure.

**On your standalone suggestion.** Thank you — it is generously meant,
and I take it that way. The honest fact is that I have no academic
credentials and no publishing experience. Being a co-author on a paper
you intend to submit would be an honor, and a far more meaningful
recognition for me than a standalone publication of my own. So I'm
fully behind the single-focus strategy, and happy to shape my
contributions to fit it exactly. If some of the other material later
merits a joint note, I'd welcome that — but there's no urgency on my
side, and your bandwidth belongs to Inventiones.

---

Separately — an update from my certified-computation program.
Three completely new results. They sit squarely in the Selberg-zeta
world you know better than anyone. I believe at least the first is
genuinely new mathematics whose framing deserves your eye before
anyone else's.

* *A theorem: the first rigorously located off-line resonance of a
  non-arithmetic surface.* Whether the Selberg zeta function of a
  non-arithmetic finite-area hyperbolic surface actually has zeros off
  the critical line is a question the literature has circled for
  decades — the Phillips–Sarnak picture predicts them, but existing
  computations for non-arithmetic Hecke groups are non-rigorous and
  the standing rigorous work leaves their location conjectural. We now
  have a proof, for the golden-ratio Hecke group G₅: a Selberg-zeta
  zero at s* ≈ 0.45390 + 5.76354i, certified to 10⁻⁶ in each
  coordinate, hence a scattering resonance a quantified distance
  ≥ 0.046 off the critical line — an unconditional essential-gap
  statement for a specific non-arithmetic surface. Three separate
  literature sweeps found no prior rigorous localization for any
  surface in this class, so I believe this is a first. The proof is
  computer-assisted in the strong sense: every constant is an
  interval-arithmetic certificate, the abstract joints are
  machine-proved in Lean, and the whole chain has survived five rounds
  of internal adversarial review plus an independent external audit
  that re-verified the certificates from raw records. I would value
  your reaction to the statement's framing — you are the reader I most
  want to get this right for.
* *A dichotomy that makes "the critical line is arithmetic" precise.*
  The theorem is one half of a sharp contrast we can now document
  across the Hecke family — the one natural family that interpolates
  between arithmetic and non-arithmetic. The arithmetic members
  q = 3, 4, 6 pin their determinant zeros to s = ρ/2 (ρ the Riemann
  zeros); the non-arithmetic G₅ and G₇ scatter well off any line, and
  for G₅ we hold certified nonvanishing witnesses at the ζ-zero
  points — so within this family the on-line picture now provably
  fails on the non-arithmetic side, while holding at machine precision
  in all the arithmetic data. That is the precise sense in which the
  critical line looks like an arithmetic phenomenon here, and it is a
  theorem on one side of the contrast, data on the other. The
  mechanism I am pursuing turned out to be scattering-theoretic rather
  than combinatorial: for the arithmetic members the factor ζ(2s) is
  exactly the Eisenstein scattering determinant of the surface — we
  have the closed form for q = 4 and q = 6, each passing its
  functional-equation and volume-residue checks, and each predicting
  extra resonances at specific points on the imaginary axis, all eight
  of which our determinants confirm numerically to ~10⁻¹⁴–10⁻³⁰
  against order-one controls. The first-principles derivation is not
  yet a theorem, but the mechanism now makes falsifiable predictions
  and has survived them at two surfaces. If it holds up, it says why
  the critical line is an arithmetic artifact in this family. Your
  judgment on that mechanism would mean more to me than anyone's.
* *Two firsts in the Mertens direction.* The constant
  Σ_ρ 1/(|ρ|²|ζ′(ρ)|²) — the conjectural limiting mean square of
  x⁻¹Σ M(n)² under RH + Gonek–Hejhal — appears never to have been
  numerically computed; it now stands at 0.02903 ± 0.00002 (10,000
  zeros, three digits certified), which already refutes the natural
  guess 2/π² and excludes 3/π⁴. And Gonek's conjecture
  J₋₁(T) ~ (3/π³)T seems never to have been numerically tested at
  all; our first test gives ratio ≈ 0.95 at T ≈ 10⁴ — honestly too low
  a height to conclude anything, which is itself worth recording. The
  10⁵-zero extension (84,501 zeros already computed and verified
  through five independent checks) will put the constant at 4–5 digits
  and the Gonek test at T ≈ 7.5×10⁴ with proper secondary-term fits.

With best regards,
Saar

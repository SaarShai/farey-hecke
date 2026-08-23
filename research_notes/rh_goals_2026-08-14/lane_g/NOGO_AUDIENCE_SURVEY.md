# No-Go Audience Survey — who is exposed to an axiom-list no-go for on-line rigidity

**Date:** 2026-08-22
**Status:** SURVEY — NOT A RESEARCH CLAIM.
This file makes no mathematical claim. It classifies *other people's* active
programs by their exposure to our lane-G no-go metatheorem, from public
sources. Every classification carries a URL. Researcher-count figures are
order-of-magnitude estimates from arXiv/workshop activity, not census data.

---

## 1. What the no-go says (scope statement, for honest classification)

Our lane-G result (see the G_5 off-line resonance theorem, memory
`g5-offline-resonance-theorem.md`) proves: every non-arithmetic finite-index
Hecke group has infinitely many off-line scattering resonances, although the
full analytic apparatus — meromorphic continuation, functional equation,
spectral/scattering structure — is present. The metatheorem being built on top
of it: **no proof schema that uses only the shared axiom list A (continuation,
functional equation, generic spectral/scattering structure) can establish
on-line rigidity.** Arithmetic input is essential.

**Two honesty constraints applied throughout.**

1. The no-go binds only schemas that use **nothing beyond A**. Most programs
   that *look* purely analytic in fact import ζ-specific arithmetic somewhere
   (Euler product, explicit formula over primes, Hecke eigenvalue relations,
   adelic/trace-formula structure). Where that import exists, the program is
   **not** refuted — it is at most *disciplined* (it now knows which of its
   steps is load-bearing). We do not inflate the body count.
2. The **moral is not ours**. It is standard folklore, and has been for ~90
   years, since Davenport–Heilbronn (1936): a Dirichlet series with a
   functional equation but no Euler product has zeros off the critical line.
   Epstein zeta functions of class number > 1 give the same negative control.
   Our contribution is narrower and should be stated narrowly: **making the
   folklore a theorem in the spectral/scattering setting**, where until now the
   only counterexamples were Dirichlet-series ones and the spectral programs
   could (and did) claim their setting was different.

### Prior art for the moral itself — cite these, do not compete with them

- **Davenport–Heilbronn / Epstein**: the canonical negative control. Standard
  statement: the Davenport–Heilbronn function "has almost all the same
  properties of ζ … except that it has no Euler product," has infinitely many
  on-line zeros, and also zeros off the line.
  <https://arxiv.org/pdf/1707.01770> (Pérez-Marco, *Notes on the Riemann
  Hypothesis*, survey treatment) ·
  <https://arxiv.org/abs/2503.24275> (2025 activity on the same object) ·
  <https://arxiv.org/pdf/2411.18492> (Epstein zeta, positive proportion on the
  line — the same object, positive side)
- **Sarnak, Clay "Problems of the Millennium: RH" (2004)** — three statements
  directly relevant, all quotable:
  - On Hilbert–Pólya self-adjointness: "While the evidence for the spectral
    nature of the zeros … has grown dramatically in recent years, I don't
    believe that the self-adjointness idea is very likely. It is not the source
    of the proof of the Weil Conjectures."
  - On de Branges: "the positivity condition that he would like to verify in
    his recent attempts, is false since it implies statements about the zeros
    of the zeta function which are demonstrably false [Conrey–Li]."
  - On arithmetic vs. transcendental: "some may feel that GRH is true for the
    Λ(s,π)'s for which π is arithmetic in nature … but that for the more
    transcendental π's such as general Maass forms, that it may fail."
  <http://home.olemiss.edu/~mbmilino/Sarnak_RH.pdf>
- **Bombieri, Clay "Problems of the Millennium: RH" (2000)** — does *not* state
  a no-go, but frames the Euler product as the defining extra structure of the
  global L-function class and concludes that RH's "solution may require
  attacking much more general problems, by means of entirely new ideas."
  <https://www.claymath.org/wp-content/uploads/2022/05/riemann.pdf>
- **Conrey–Li (2000), "A note on some positivity conditions related to zeta-
  and L-functions"** — the exact precedent for our logic: a *negative control
  killing a proof schema*. They show de Branges' positivity conditions fail for
  the relevant reproducing-kernel functions. This is the paper our metatheorem
  is methodologically modelled on, and it should be cited as such, not as
  something we are extending unawares.
  <https://arxiv.org/pdf/math/9812166> ·
  <https://academic.oup.com/imrn/article/2000/18/929/726555>

---

## 2. Classification table

Exposure key:
**(a)** consumes arithmetic input essentially → **not** exposed; no-go is a
discipline, not a refutation.
**(b)** operates only on the shared axiom list A → **structurally unable to
succeed as formulated**, if the no-go holds.
**(c)** mixed / unclear — the arithmetic import exists but is not isolated, so
the program cannot presently say which of its steps is load-bearing.

| # | Program | Exposure | Active scale (order of mag.) | Redirect value | Key URLs |
|---|---|---|---|---|---|
| 1 | **Hilbert–Pólya spectral realization, generic form** (build a self-adjoint operator whose spectrum = zeros, using only continuation + functional equation + spectral structure) | **(b)** | ~10^2 authors; a long, steady, mostly low-citation arXiv stream (math.NT / math-ph) | **HIGHEST** — this is the population the spectral-setting sharpening speaks to directly, and the one that has *not* internalized the Davenport–Heilbronn moral because it believed the spectral setting escaped it | <https://arxiv.org/pdf/2406.01828> · <https://arxiv.org/pdf/2408.15135> · <https://arxiv.org/pdf/2511.18309> |
| 2 | **Berry–Keating xp / quantum-chaos Hamiltonians**, incl. the Bender–Brody–Müller 2017 line and successors | **(b)**, with a **(c)** tail | ~50–150 authors across math-ph / quant-ph; the BBM PRL alone seeded a large successor literature | **HIGH** — BBM-type constructions *derive* their operator from ξ but the self-adjointness argument they need is generic; a spectral negative control is exactly the missing discipline. The (c) tail: constructions that smuggle in the Euler product via a prime-indexed potential | <https://link.aps.org/doi/10.1103/PhysRevLett.118.130201> · <https://arxiv.org/abs/1608.03679> · <https://arxiv.org/pdf/1610.06472> · <https://arxiv.org/pdf/2307.01254> |
| 3 | **Connes adelic / trace-formula program; Connes–Consani** (adele class space, Scaling Site, ζ-cycles, prolate wave operator, Riemann–Roch over F_1) | **(a)** — arithmetic is the whole content: adeles, primes as places, Weil explicit formula as a trace | ~10–30 core; a well-defined school | **LOW as refutation; MODERATE as confirmation** — this program is the clearest *positive* instance of "arithmetic input is essential", and can cite our theorem as evidence that its adelic input is not decorative | <https://alainconnes.org/wp-content/uploads/scalingH.pdf> · <https://arxiv.org/pdf/2401.08401> · <https://arxiv.org/pdf/2207.10419> · <https://arxiv.org/pdf/1910.14368> |
| 4 | **de Branges Hilbert-space positivity** | **(b)** — and *already refuted by the same logic* | ~1–5 active; effectively dormant post-2000 | **LOW (as audience) / HIGHEST (as precedent)** — cite Conrey–Li as the template, do not re-kill this program | <https://arxiv.org/pdf/math/9812166> · Sarnak p.6, above |
| 5 | **Nyman–Beurling / Báez-Duarte criterion** | **(c)**, leaning (a) | ~20–50 authors, steady low-volume | **MODERATE** — the criterion itself is an equivalence, not a schema, so the no-go does not bite it; but *attempts to verify* the approximation condition by generic Hilbert-space means are exposed. The Möbius/Dirichlet-coefficient input is arithmetic, so the program is defensible | <https://arxiv.org/abs/1805.06733> · <https://arxiv.org/pdf/math/0202141> · <https://arxiv.org/html/2607.12084> · <https://arxiv.org/pdf/2409.16489> |
| 6 | **De Bruijn–Newman constant / heat flow** (Rodgers–Tao Λ≥0; Polymath15 Λ≤0.22) | **(a)** — Λ≥0 is proved *from* the known zero statistics of ζ; Polymath15's bound uses explicit ζ numerics and mollifiers | ~20–60 (Polymath-style, bursty) | **LOW–MODERATE** — the program is arithmetic-fed and the Λ≥0 result is itself a "RH is barely true if true" statement, i.e. independently anti-generic. Worth citing as convergent evidence | <https://arxiv.org/abs/1801.05914> · <https://arxiv.org/abs/1904.12438> · <https://michaelnielsen.org/polymath/index.php?title=De_Bruijn-Newman_constant> · <https://arxiv.org/abs/1901.06596> |
| 7 | **Li's criterion / Keiper–Li coefficients** | **(c)** — Bombieri–Lagarias give λ_n an *arithmetic* interpretation (prime-sum/explicit-formula), so the criterion is arithmetic-fed; but positivity-proof attempts are generic | ~20–50, steady low-volume, plus a persistent amateur tail | **MODERATE** — the useful message is precisely which side of the criterion is arithmetic | <https://arxiv.org/pdf/2006.13103> · <https://arxiv.org/pdf/1404.7276> · <https://www.numdam.org/item/10.5802/aif.2311.pdf> · <https://en.wikipedia.org/wiki/Li%27s_criterion> |
| 8 | **Random-matrix / GUE statistics** (Montgomery → Keating–Snaith → CFKRS moments, low-lying zeros, symmetry types) | **(a)** — the whole enterprise is a *statistical* theory of arithmetic families; symmetry type is read off arithmetic, and function-field analogues supply the arithmetic model | ~10^2–10^3; the largest population here by far | **LOW as refutation; HIGH as framing** — RMT was never a proof schema for on-line rigidity, and its practitioners know it. But RMT *is* where the "universality vs. arithmetic" boundary is argued, so the sharpening is intelligible to this audience | Sarnak, above (Montgomery–Odlyzko law, Keating–Snaith) · <https://arxiv.org/pdf/1707.01770> |
| 9 | **Physics-inspired: statistical mechanics, PT-symmetry, scattering-with-impurities models** | **(b)** predominantly | ~50–150, high arXiv churn, low mathematical citation weight | **HIGH by volume, LOW by influence** — the largest genuinely-exposed population, but poorly positioned to act on the result | <https://arxiv.org/pdf/2307.01254> · <https://arxiv.org/pdf/2109.03068> · <https://arxiv.org/html/2606.24405> |
| 10 | **Machine-learning-assisted zero / L-function studies** (murmurations; ML of vanishing order) | **(a)** — the discovered signal (murmurations) is arithmetic: a_p vs. conductor. Not a proof schema at all | ~30–80 and growing fast | **LOW** — not exposed; but a natural venue for *stating* the arithmetic-is-essential moral to a new audience | <https://arxiv.org/html/2603.09680> · <https://arxiv.org/pdf/2502.10360> |
| 11 | **Selberg-class / axiomatic-Dirichlet-series programs** (added: this is where the Dirichlet-series analogue of our axiom list A already lives) | **(a)** by construction — the Selberg class *includes* an Euler product axiom precisely because Davenport–Heilbronn showed you must | ~30–80 | **MODERATE** — this community already codified the moral into an axiom. Our theorem is the spectral-side mirror of that codification, and this is the community best able to referee that claim | <https://arxiv.org/pdf/2008.02570> · <https://arxiv.org/pdf/1602.06328> |
| 12 | **Eisenstein-series / Maass–Selberg non-vanishing (Sarnak's "most powerful method towards GRH")** (added) | **(a)** — arithmetic quotients, automorphic input essential | ~30–100 | **LOW as refutation; HIGH as contrast case** — this is the standing counter-example to "spectral means generic": a spectral method that works *because* it is arithmetic. Our non-arithmetic Hecke groups are the control group for exactly this method | Sarnak p.6, above |

---

## 3. Where the community already internalized the moral (do not claim discovery)

- The **Selberg class** builds the Euler product in as an axiom (row 11).
- **Sarnak (2004)** rejects generic self-adjointness explicitly, and separates
  "arithmetic π" from "transcendental π" for GRH (row 1, 4, 12).
- **Conrey–Li (2000)** already ran the negative-control argument against a
  named positivity schema (row 4).
- **Davenport–Heilbronn** is folklore taught in every RH survey.

The defensible statement of our contribution is therefore:

> The moral — functional equation without arithmetic does not force on-line
> zeros — has been Dirichlet-series folklore since 1936 and is codified in the
> Selberg-class axioms. It had **no theorem-strength analogue on the
> spectral/scattering side**, which is precisely why spectral programs (rows
> 1, 2, 9) continued as though their setting were exempt. We supply that
> analogue: a family of scattering problems with the full analytic apparatus
> and provably infinitely many off-line resonances, with arithmeticity as the
> exact discriminant.

Anything stronger than that is over-claiming.

---

## 4. Top three by redirect value

1. **Hilbert–Pólya generic spectral realizations (row 1).** Largest genuinely
   exposed mathematically-serious population, and the one whose working
   assumption — "the spectral setting is different from the Dirichlet-series
   setting, so Davenport–Heilbronn does not apply to me" — is exactly what the
   theorem removes. Redirect: any candidate operator construction must name the
   step at which arithmetic enters, or it is provably insufficient.

2. **Berry–Keating xp / Bender–Brody–Müller line (row 2).** Highest-visibility
   exposed program (PRL-level attention, large successor literature), and its
   open gap is precisely a *generic* self-adjointness claim on a
   scattering-type operator. Our non-arithmetic Hecke groups are the sharpest
   available test case: same operator-theoretic shape, off-line spectrum
   provable. Redirect: the missing ingredient is not analytic rigour, it is
   arithmetic input.

3. **Connes / Connes–Consani adelic program (row 3) — as a beneficiary, not a
   target.** The single strongest confirmation audience. This program's
   distinguishing bet is that adelic arithmetic is indispensable; a theorem
   showing the non-arithmetic case *fails* converts that bet into supported
   methodology. It is also the audience with the standing and the venue to make
   the sharpening visible. Pair with row 12 (Eisenstein/Maass–Selberg) as the
   working example of a spectral method that succeeds *because* it is
   arithmetic.

---

## 5. Caveats

- Researcher counts are inferred from arXiv listing density and citation
  clusters observed in this survey, not from a systematic bibliometric pull.
  Treat as order-of-magnitude only.
- Rows 1, 2, 9 contain a substantial low-quality tail (the perennial-RH-claim
  literature). Redirect value there is real but should not be measured by
  headcount.
- Row 5 and 7 classifications as (c) are judgement calls: both criteria are
  *equivalences* fed by arithmetic, so only the verification attempts are
  exposed. Do not report them as (b).
- No claim here has been checked against the actual lane-G proof text; this
  survey takes the theorem statement as given by the task brief.

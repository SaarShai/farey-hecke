# Outreach drafts — Mertens computing / explicit-formula / arithmetic moments

**Status**: DRAFT (not sent). Review before use.
**Date**: 2026-05-27
**Common attachments**: Σ M(n)²/n^s table (s ∈ {2.1,...,6.0}, N=10⁸) + Jordan-totient convolution identity

---

## 1. Nathan Ng — `nathan.ng@uleth.ca`
**Subject**: Σ M(n)²/n³ = 1.13616 to 13 digits — possible explicit-formula expansion?

Dear Professor Ng,

In computing Farey L²-discrepancy via the structural identity (Franel 1924 form), I encountered a convergent series Σ_{n≥1} M(n)²/n³ = 1.1361623076908(2) computed to 13 stable digits at N = 10⁸. The constant does not appear in OEIS or in any reference I have checked. Its companions Σ M(n)²/n^s for s ∈ {2.1, 2.25, ..., 6.0} have also been tabulated to high precision; the s = 2.5 case sits at 1.0775... and converges noticeably faster.

Given your 2004 PhD thesis and PLMS paper on the explicit formula for M(x), I wondered whether Σ M(n)²/n³ admits an expansion in terms of Σ_ρ over Riemann zeros under RH (analogous to your derivation for the unweighted Mertens sums), and whether the s-dependence has a clean Dirichlet-series interpretation. I have the raw data, a Kaggle notebook, and a 1-page reduction sketch ready to share. Any pointer would be welcome.

— Saar Shai

---

## 2. Tim Trudgian — `t.trudgian@adfa.edu.au`
**Subject**: New convergent constant Σ M(n)²/n³ — connection to your Mertens bounds?

Dear Professor Trudgian,

In recent computational work on Farey L²-discrepancy I encountered a convergent series

  Σ_{n ≥ 1} M(n)²/n³ = 1.1361623076908... (13 digits stable at N = 10⁸)

which is, as far as I can determine, not catalogued. The series controls part of the structural identity 12·J(Q) = Σ_e (J_2(e)/e²)·T(Q/e)² + 2T(Q) + 1 (Jordan-totient convolution form of Franel 1924), and a Tauberian closure for J(Q) reduces it (under RH) to a weighted reciprocal-zeta moment that aligns with Gonek 1989.

Given your work on explicit Mertens-function bounds, I wondered whether you'd find Σ M(n)²/n^s for s ∈ (2, ∞) a useful test case for your inequalities, and whether the constant 1.13616 lands inside any of your published estimate windows. Happy to share the tabulated data and the reduction note.

— Saar Shai

---

## 3. Greg Martin — `gerg@math.ubc.ca`
**Subject**: Jordan-totient convolution form of Σ_{d,d'} gcd² M(Q/d)M(Q/d')/(dd')

Dear Professor Martin,

I derived (via a J_2 identity) the following reduction of the Franel 1924 double-sum:

  Σ_{d,d' ≤ Q} gcd(d,d')² · M(⌊Q/d⌋) · M(⌊Q/d'⌋) / (d·d') = Σ_e (J_2(e)/e²) · T(⌊Q/e⌋)² 

where J_2 is the Jordan totient and T(x) = Σ_{n≤x} μ(n) M(⌊x/n⌋). The 3D-to-1D collapse saves roughly a factor of Q in compute and turns a quadratic-in-Q problem into linear-in-Q. The associated convergent constant Σ M(n)²/n³ = 1.1361623076908 at N = 10⁸.

Given your work on arithmetic-function moments and the totient family, I wondered (a) whether you've seen this convolution form elsewhere, and (b) whether it would generalize cleanly to Σ_{d,d'} gcd^k · f(Q/d) · g(Q/d')/(d·d')^s for arbitrary multiplicative f,g. The technique would be a small but real productivity gain for anyone working with this kind of nested sum. Note draft available.

— Saar Shai

---

## 4. Kannan Soundararajan — `ksound@math.stanford.edu`
**Subject**: New Mertens-square moment Σ M(n)²/n³ = 1.13616 — RH interpretation?

Dear Professor Soundararajan,

Pursuing the Tauberian closure of a Franel-type identity for Farey L²-discrepancy, I encountered the convergent series Σ_{n≥1} M(n)²/n³ = 1.1361623076908 to 13 stable digits (N = 10⁸ direct computation, cross-checked via Mellin/Perron framework). The reduction passes through Σ_e (J_2(e)/e²) · T(Q/e)² + 2T(Q) + 1 (where T(Q) = Σ μ(n) H(Q/n)) and reaches a weighted reciprocal-zeta second-moment integral

  ∫_{(1/2)} dw / [w²(2−w)² · ζ(w) · ζ(2−w)] = 36·C·ζ(3)/π²

under RH (with C = OEIS A065483/2). This integral aligns with the conjectural framework of Gonek 1989. The Σ M²/n³ constant does not appear in OEIS.

Given your work on Mertens-square moments and zeta moments more broadly, I would welcome (1) confirmation or refutation that the Σ M²/n³ constant is genuinely new, and (2) any reading on whether the weighted-reciprocal-zeta integral is tractable in the AFE / sharp-cutoff style. A short note is ready to share.

— Saar Shai

---

---

## 5. Steve Gonek — `steven.gonek@rochester.edu`
**Subject**: Tauberian closure reducing to your 1989 weighted reciprocal-zeta moment

Dear Professor Gonek,

In a Tauberian closure of the Franel 1924 identity for Farey L²-discrepancy J(Q), I arrive — under RH and a sharp-cutoff Mellin/Perron step — at the weighted reciprocal-zeta integral

  ∫_{(1/2)} dw / [w²·(2−w)²·ζ(w)·ζ(2−w)] = 36·C·ζ(3)/π²

where C = OEIS A065483/2 (totient summatory). This integral aligns with the framework you proposed in your 1989 paper on weighted moments of reciprocal zeta. The reduction passes through the Mellin transform 𝒯(s) = 1/(s²·ζ(s)) of T(Q) = Σ_{n≤Q} μ(n)·H(⌊Q/n⌋), and the structural identity collapses to 12·J(Q) = Σ_e (J_2(e)/e²)·T(⌊Q/e⌋)² + 2T(Q) + 1.

A side product: Σ M(n)²/n³ = 1.1361623076908 to 13 stable digits at N = 10⁸, a constant I cannot find in OEIS or in references I've consulted. I would value your reading on whether the integral above is now tractable in the AFE / sharp-cutoff style you've developed since 1989, and whether the 1.13616 constant has been computed elsewhere. A short note + raw data are ready to share.

— Saar Shai

---

## Not contacted (unconfirmed email via public sources)
- Harald Helfgott — only personal Gmail found; pass for now
- Dave Platt — Bristol page 404; co-author chain via Booker
- Andrew Booker — Bristol staff page 404; LMFDB chair, try later via LMFDB list
- John Cremona — listed in algorithmic_nt drafts
- Cox / Ghosh / Sultanow (prior-art on static Farey↔Mertens) — different community, hold

## Notes for sending
- Group B audience considers Σ M²/n³ + Jordan-totient reduction as headline.
- The Tauberian closure remains conditional — be explicit about that.
- Cite Franel 1924, Mikolás 1949/51, Kanemitsu-Yoshimoto 1996 explicitly; the structural identity is *not* novel and must be presented as a derivation/repackaging.

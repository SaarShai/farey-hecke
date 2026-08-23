# DRAFT — arXiv paper skeleton (math.NT / math.SP). NOT SUBMITTED. NOT REVIEWED BY THE OWNER.

**Status: DRAFT SKELETON ONLY.** No sentence below is promoted by this file.
Every claim carries the status of its most-caveated banked source (LEDGER
RULE). Section headers marked `[PLACEHOLDER]` contain no result yet.
Nothing here has been sent, posted, or submitted anywhere.

**Sources of record used to build this skeleton** (all repo-relative):

- `research_notes/rh_goals_2026-08-14/lane_g/LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_SOL.md`
  (2026-08-19 promotion block; 2026-08-20 second-audit correction block)
- `research_notes/rh_goals_2026-08-14/lane_g/LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_REFEREE.md`
  and `LAW_SECOND_AUDIT_REFEREE.md`
- `research_notes/rh_goals_2026-08-14/lane_g/NOGO_METATHEOREM_SOL.md` §§1–5,
  **with §8 corrections D1–D13 and the §9 addendum governing**
- `research_notes/rh_goals_2026-08-14/lane_g/NOGO_AUDIENCE_SURVEY.md` §3
- `research_notes/rh_goals_2026-08-14/lane_g/SEL90_BYPASS_JENSEN_REDERIVATION_SOL.md`
  and `..._REFEREE.md`
- `projects/aristotle_dispatch_v33/aristotle_dispatch_v33_aristotle/LawSkeletonI.lean`
  and `projects/aristotle_dispatch_v33/DISPATCH.md` §11
- `research_notes/rh_goals_2026-08-14/lane_g/EFFECTIVE_THEOREM_ASSEMBLY_SOL.md`
- `plans/wayfinder/rh-goals/MAP.md` (q8 compute ticks)

---

## Working title

**Off-line scattering resonances for the Hecke triangle orbifolds, and what
the generic scattering axioms cannot decide**

Alternative: *A spectral-side negative control for on-line rigidity.*

## Author block

**TODO (owner).** Authorship, ordering, affiliations, and whether
Prof. S. Koyama is invited as coauthor are owner decisions. Do not fill in.

---

## 1. Abstract [DRAFT]

> For every finite integer \(q \ge 3\) we prove that the scalar
> trivial-character scattering determinant \(\varphi_q\) of the one-cusp
> Hecke triangle orbifold \(G_q \backslash \mathbb{H}\) has infinitely many
> nonreal zeros \(\rho\) with \(\Re\rho > 1/2\), and therefore infinitely
> many multiplicity-matched scattering poles \(1-\rho\) with
> \(\Re(1-\rho) < 1/2\). In particular every nonarithmetic finite Hecke
> group \(G_q\), \(q \notin \{3,4,6\}\), has a scattering resonance strictly
> off \(\Re s = 1/2\).
>
> We then isolate the hypotheses the proof actually consumes as an explicit
> axiom list \(A\) (meromorphic continuation of order at most two, the
> functional equation \(\varphi(s)\varphi(1-s)=1\), reality, a generalized
> Dirichlet series with the Hejhal archimedean factor at \(\kappa=1\),
> finiteness and reality of the right divisor with strip confinement, a
> polynomial vertical bound, and the exact critical-line modulus), and prove
> a metatheorem: \(A\) *entails the negation* of the naive on-line rigidity
> statement. No proof schema quantifying over all models of \(A\) can place
> all right-half-plane zeros on \(\Re s = 1/2\); a schema that appears to do
> so is refuted already by the modular case \(\varphi_3\). We also show that
> \(A\) fails to decide the genuine RH-analogue \(P_{\mathrm{line}}(3/4)\) in
> at least one direction, unconditionally.
>
> The moral is not new: since Davenport–Heilbronn (1936) it has been
> Dirichlet-series folklore that a functional equation without an Euler
> product does not force on-line zeros, and the Selberg class encodes that
> folklore as an axiom. What was missing was a theorem-strength analogue on
> the spectral/scattering side. This paper supplies one.

**Ledger notes on the abstract.**
- The first paragraph is the promoted LAW, quoted verbatim from the
  2026-08-19 promotion block. Do not strengthen.
- The "in particular, nonarithmetic" clause is **non-discriminating**:
  \(q = 3\) (arithmetic) has the same off-line property. The abstract must
  never present it as an arithmeticity signature
  (`LAW_..._SOL.md:486–489`).
- Metatheorem I is stated in its §9-upgraded, unconditional form
  \(A \models \neg P_{\mathrm{naive}}\) — see §4 below for the exact
  residuals that upgrade permits and does not permit.

---

## 2. Introduction — the honest framing

### 2.1 What is claimed, in one paragraph

Follow `NOGO_AUDIENCE_SURVEY.md` §3 verbatim as the *defensible framing*:

> The moral — functional equation without arithmetic does not force on-line
> zeros — has been Dirichlet-series folklore since 1936 and is codified in
> the Selberg-class axioms. It had **no theorem-strength analogue on the
> spectral/scattering side**, which is precisely why spectral programs
> continued as though their setting were exempt. We supply that analogue: a
> family of scattering problems with the full analytic apparatus and
> provably infinitely many off-line resonances.

**Correction applied here, mandatory.** The survey's sentence ends "with
arithmeticity as the exact discriminant". That clause is **refuted by our
own bank** and must be deleted: the second cold audit records that the
non-arithmeticity clause "is NON-DISCRIMINATING: q=3 (arithmetic) has the
same off-line property" and "must never be used as an arithmeticity
signature" (`LAW_..._SOL.md:486–489`), and Corollary 3.5 of
`NOGO_METATHEOREM_SOL.md` makes the blindness formal. The introduction must
state the blindness explicitly rather than let a reader infer a dichotomy.

### 2.2 Prior art, cited as prior art

- **Davenport–Heilbronn (1936); Epstein zeta functions of class number > 1.**
  The canonical negative control on the Dirichlet-series side: a function
  with almost all the properties of \(\zeta\) except an Euler product, with
  zeros off the line. Cite as the origin of the moral, not as something we
  extend.
- **The Selberg class.** The Euler product is an axiom there *precisely
  because* of Davenport–Heilbronn. Our axiom list \(A\) is the
  spectral-side mirror of that codification.
- **Conrey–Li (2000),** *A note on some positivity conditions related to
  zeta- and L-functions*. The methodological precedent: a negative control
  that kills a named proof schema (de Branges positivity). Our metatheorem
  is modelled on this argument shape and should say so.
- **Sarnak, Clay "Problems of the Millennium: RH" (2004).** Three quotable
  positions: scepticism that generic self-adjointness is the source of a
  proof; the Conrey–Li refutation of de Branges' positivity; the separation
  of "arithmetic \(\pi\)" from "transcendental \(\pi\)" for GRH.
- **Hejhal, LNM 1001, Theorem 7.11 / Corollary 7.12 (pp. 577–579).** The
  *printed partial antecedent*: for all sufficiently large \(N\), zeros and
  poles of \(\varphi_N\) in any prescribed rectangle touching the critical
  line. Weaker in \(q\)-range, stronger in localization. **Must be cited
  wherever novelty is framed** (`NOGO_METATHEOREM_SOL.md` §5.2,
  §5.4).
- **Selberg (1990),** *Remarks on the distribution of poles of Eisenstein
  series*, Israel Math. Conf. Proc. 3. The source of the \(d=2\) counting
  theorem consumed as (C), per Kelmer Remark 0.2. **State that it was not
  read** by the authors; see §7 below.
- **Kelmer, arXiv:1402.4780**, §4 — the complex-analytic proof template
  (torsion-free global setup; only the template is reused).
- **Friedman–Jorgenson–Smajlović, arXiv:2011.12795**, §§2.1, 2.4 —
  continuation, functional equation, divisor list in orbifold generality.
- **Venkov,** *Trudy Mat. Inst. Steklov* **153 (1981)**, Thm 3.5 p. 59 —
  **not** the 1979 Uspekhi survey; reached only through FJS
  (`NOGO_METATHEOREM_SOL.md` §5.4, D12).
- **Mayer–Mühlenbruch–Stromberg**, transfer operator for the Hecke triangle
  groups — presentation and the one-cusp statement.

**Do not over-cite Bombieri.** The Clay problem description does not state
a no-go; at most it may be cited once, for framing the Euler product as the
defining extra structure of the global L-function class
(`NOGO_AUDIENCE_SURVEY.md` §1).

### 2.3 What is *not* claimed

Reproduce the SCOPE box of `NOGO_METATHEOREM_SOL.md` §5 essentially
verbatim in the introduction, not only in a late section. In particular:

- We do **not** claim there is no proof of RH without an Euler product.
- We do **not** claim the RH-analogue in this family is unprovable,
  undecidable, or independent of anything.
- We do **not** claim any arithmeticity criterion. Corollary 3.5 is a
  *blindness* statement.
- \(P_{\mathrm{naive}}\) failing is a statement about a naive formulation,
  not about RH.

---

## 3. The LAW (main theorem)

**Statement — quoted verbatim from the promotion block of
`LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_SOL.md` (lines 406–413), which is the
most-caveated banked phrasing:**

> **THEOREM (paper-level, unconditional).** For every finite integer
> \(q\ge3\), the scalar trivial-character scattering determinant of the
> one-cusp Hecke triangle orbifold has infinitely many nonreal zeros
> \(\rho\) with \(\Re\rho>1/2\), and therefore infinitely many
> multiplicity-matched scattering poles \(1-\rho\) with
> \(\Re(1-\rho)<1/2\). In particular, every nonarithmetic finite Hecke
> group \(G_q\), \(q\notin\{3,4,6\}\), has a scattering resonance strictly
> off \(\Re s=1/2\).

Supporting count, in the form the existence conclusion needs:
\[
F_q(\tfrac12,T)=\frac{1}{4\pi}T^2\log T+O_q(T^2),
\]
finitely many total right zeros forcing the defining sum to be only
\(O_q(T)\).

**Certified-as-absent, and to be stated as absent in the paper**
(`LAW_..._SOL.md:435–439`): no effective first height; no \(q\)-uniform
error; no machine formalization of the analytic content; no
project-specific Selberg-zeta normalization. These remain OPEN and are not
needed for the stated LAW.

**Three wording repairs carried from the promotion block** (§3 of the paper
must incorporate all three): \(\varphi_q\) has no central divisor and the
normalization \(L_q^*\) has the exactly simple zero at \(s=1/2\); the
horizontal \(O_q(\log T)\) term uses the right-edge normalization and the
Selberg–Titchmarsh argument as reproduced by Kelmer, not the modulus bound
alone; no explicit formula for the group-dependent linear coefficient
\(A_q\) is consumed, only its existence.

**Consume-side warning to be honoured in the paper:** do **not** consume
\(A_q\), \(B_q\), or \(C_q\) numerics from Kelmer — his printed \(B_\Gamma\)
carries a spurious \(\log\pi\) and his \(A_\Gamma\) assembly formula is
wrong (`LAW_..._SOL.md:480–485`).

---

## 4. The axiom list \(A\) and the metatheorem

*(This section is written fresh. The §6 "candidate paper section" of
`NOGO_METATHEOREM_SOL.md` is **deprecated** per D9/D10/D11 and is not
reused.)*

### 4.1 The structures

A *Hecke-type scattering pair* is \(M=(\varphi,\mathcal D)\) with
\(\varphi\) meromorphic on \(\mathbb C\) and
\(\mathcal D=(d(n),g_n)_{n\ge1}\) its Dirichlet data. Write
\(\mathfrak M(A)\) for the class of pairs satisfying A0–A7. Nothing in the
language of \(A\) mentions \(q\), a group, a surface, arithmeticity, or
\(\zeta\).

### 4.2 The axioms

- **A0 (scalar, one channel, \(\kappa=1\)).** \(\varphi\) is a \(1\times1\)
  determinant; degree of singularity 1; the archimedean factor carries
  \(\kappa=1\).
- **A1 (meromorphy and right-half-plane regularity).** \(\varphi\)
  meromorphic on \(\mathbb C\) of order at most 2, holomorphic in
  \(\Re s>1/2\) apart from finitely many poles.
- **A2 (functional equation).** \(\varphi(s)\varphi(1-s)=1\).
- **A3 (reality).** \(\varphi(\bar s)=\overline{\varphi(s)}\); equivalently
  \(d(n)\in\mathbb R\).
- **A4 (generalized Dirichlet series, Hejhal archimedean factor).** For
  \(\Re s>1\),
  \(\varphi(s)=\sqrt\pi\,\Gamma(s-\tfrac12)/\Gamma(s)\cdot\sum_{n\ge1}d(n)g_n^{-2s}\),
  with \(0<g_1<g_2<\dots\to\infty\) discrete, \(d(1)\neq0\), the series
  absolutely convergent. **A4⁺** (used only where flagged): \(d(n)>0\).
- **A5 (right divisor: finiteness, reality of poles, strip confinement) —
  in the D2-corrected form.** In \(\Re s>1/2\): finitely many real zeros
  \(\rho_i>1/2\) with multiplicity; **every pole of \(\varphi\) in
  \(\Re s>1/2\) is real and lies in \((1/2,1]\), and there are finitely
  many**; and every zero lies in a vertical strip. *(The reality-of-poles
  clause is used essentially — see §9 of `NOGO_METATHEOREM_SOL.md`.)*
- **A6 (vertical polynomial bound).** For every \(\varepsilon>0\) there is
  \(C(\varepsilon)<\infty\) with \(|\varphi(\sigma+it)|\le C(\varepsilon)\)
  for \(1/2\le\sigma\le3/2\), \(|t|\ge\varepsilon\).
- **A7 (critical-line modulus).** \(|\varphi(1/2+it)|=1\) for real \(t\), in
  the exact-modulus form (G), not merely unitarity.

**Not in \(A\), deliberately:** any Euler product, multiplicativity, or
Ramanujan bound; any group, surface, or spectral input beyond A0; any
\(q\)-uniformity; any effective first height; any arithmeticity.

**Note on strip confinement (D6b).** Strip confinement is not an
independent assumption: it is an immediate corollary of A4 via the (NF)
right-edge estimate \(|L^*-1|<1\) for large \(\Re s\).

### 4.3 Breadth lemma

\(\varphi_q\in\mathfrak M(A)\) for every finite integer \(q\ge3\),
arithmetic and non-arithmetic alike. Receipts are per-axiom, both sides, in
the table of `NOGO_METATHEOREM_SOL.md` §2. **In five of the nine rows the
two columns are the same citation** (A0, A4, A4⁺, A6, A7) — the corrected
count per D4; A1, A2, A3, A5 carry distinct arithmetic-side derivations from
\(\Lambda\). \(A\) was not assembled by intersecting two separately verified
lists.

For \(q=3\) the Dirichlet data is explicitly \(d(n)=\phi_{\rm Euler}(n)\),
\(g_n=n\), \(d(1)=1\), giving
\(\sum d(n)g_n^{-2s}=\zeta(2s-1)/\zeta(2s)=L^*_3(s)\) (D5). Note that
Hejhal's Lemma 7.3, used in the A4⁺ row, is printed for \(N\ge4\) and does
**not** cover \(q=3\); \(q=3\) is covered by the direct positive-integer
count (D3).

### 4.4 The two candidate rigidity statements

\[
P_{\mathrm{naive}}: \ \varphi \text{ has no zero } \rho \text{ with }
\Re\rho>1/2 \text{ and } \Im\rho\neq0,
\]
\[
P_{\mathrm{line}}(c): \ \text{every zero } \rho \text{ with }
1/2<\Re\rho<1,\ \Im\rho\neq0, \text{ has } \Re\rho=c.
\]

This is the canonical definition of \(P_{\mathrm{naive}}\) (D10) and must be
used everywhere; A5 explicitly permits finitely many *real* right zeros, so
the "no zeros at all" reading is non-derivable for a second and trivial
reason.

### 4.5 Metatheorem I

> **METATHEOREM I.** \(A \models \neg P_{\mathrm{naive}}\). Every
> \(M\in\mathfrak M(A)\) has infinitely many zeros \(\rho\) with
> \(\Re\rho>1/2\), \(\Im\rho\neq0\), and hence by A2 infinitely many
> multiplicity-matched poles \(1-\rho\) with \(\Re(1-\rho)<1/2\).
>
> **Consequence (the no-go).** There is no valid derivation of
> \(P_{\mathrm{naive}}\) from \(A\) — not because \(A\) is too weak, but
> because \(A\) proves its negation. Any argument that appears to derive
> on-line rigidity in the sense of \(P_{\mathrm{naive}}\) from meromorphic
> continuation, the functional equation, critical-line unitarity, a
> generalized Dirichlet series, and polynomial vertical growth **contains an
> error**, and the error can be exhibited: **apply the argument to
> \(\varphi_3\)**, where the failure is classical fact (D11).

*Proof sketch for the paper.* This is the LAW read as a statement about
\(\mathfrak M(A)\) rather than about Hecke orbifolds. Every input is an
axiom: (NF) and the right-edge estimate from A4; the Jensen/Littlewood
rectangle from A1, A5 (finitely many real right poles), A6 (horizontal
edges), A4 (right edge to \(+\infty\)); the critical-line integral with
leading coefficient \(1/4\pi\) from A7's exact modulus plus
\(|\Gamma(\tfrac12+it)/\Gamma(it)|^2=|t|\tanh(\pi|t|)\); the divergence step
from A5 against \(F(\tfrac12,T)=(1/4\pi)T^2\log T+O(T^2)\), with **strip
confinement (A5) consumed at the divergence step** to convert an unbounded
weighted sum into infinitely many zeros (D6a); strictness from the
vanishing Jensen weight at \(\Re\rho=1/2\), independently from
A2+A3+A7 forcing no divisor on the line at all; nonreality from A5; and
reflection from A2. No step consumes a group, a surface, arithmeticity, an
Euler product, or \(q\).

**Status and the exact residual (this must be stated in the paper).**
The unconditional form \(A\models\neg P_{\mathrm{naive}}\) is licensed by
the §9 genericity/transfer addendum of `NOGO_METATHEOREM_SOL.md`: the
Sel90-bypass derivation cites only the interface facts (D)/(NF), (E), (F),
(G)/(U), (P), (Rl) plus classical ambient analysis, and each of those is a
consequence of the corrected axiom list, so the derivation transfers
verbatim to an arbitrary \(M\in\mathfrak M(A)\). Prior to that addendum the
honest form was the D1 form \(A\wedge H_{\rm Sel90}\models\neg
P_{\mathrm{naive}}\). Residuals that remain, none of them a hypothesis on
\(\varphi\): the rectangle identity is consumed only in the (J)-avg / H3
form; GAP-1 ((J)-sharp, remainder \(O_q(\log T)\) at *every* height) and
GAP-2 ((C) and (DIF)) still rest on Selberg 1990 and are absent from the
conclusion chain's signature.

### 4.6 Metatheorem II

> **METATHEOREM II (conditional on RH).** Assume RH. Then
> \(A\nvDash\neg P_{\mathrm{line}}(3/4)\): the pair
> \(\varphi_3\in\mathfrak M(A)\) satisfies \(P_{\mathrm{line}}(3/4)\).
> Hence there is no valid derivation from \(A\) of the failure of on-line
> rigidity in its RH-analogue form.

The conditionality is **unavoidable for this witness** (D7); we give no
argument that no other \(M\in\mathfrak M(A)\) has unconditionally collinear
right-strip zeros.

### 4.7 The RH calibration

> **PROPOSITION.** \(P_{\mathrm{line}}(3/4)\) holds for \(\varphi_3\) if and
> only if RH. Moreover \(P_{\mathrm{naive}}\) fails for \(\varphi_3\)
> unconditionally.

Proof from \(\varphi_3(s)=\Lambda(2s-1)/\Lambda(2s)\): the zeros of
\(\varphi_3\) in \(\Re s>1/2\) are exactly \(s=(1+\rho)/2\) for \(\rho\) a
nontrivial zero of \(\zeta\), a multiplicity-preserving bijection, all
nonreal, all with \(1/2<\Re s<1\); and \(\Re((1+\rho)/2)=3/4\iff\beta=1/2\).
Confirmed unconditionally by the cold referee and re-verified numerically to
20+ digits. The closed form for \(\varphi_3\) is a **NOT-READ standard
citation** (Iwaniec, *Spectral Methods of Automorphic Forms*, 2nd ed. §3.4),
corroborated twice inside our own bank.

**Why this matters, and it is the point of the paper's title:** the
functional equation reflects about \(\Re s=1/2\), so \(1/2\) is the
*symmetry* line; the zeros of the underlying \(\zeta\) are pushed to
\(\Re s=3/4\) by \(w=2s-1\), so \(3/4\) is the *rigidity* line. Writing
"on-line rigidity" without saying which line is the mistake this paper
exists to catch.

By A2, \(P_{\mathrm{line}}(3/4)\) for zeros is equivalent to all nonreal
scattering poles of the modular orbifold lying on \(\Re s=1/4\) — the
Faddeev–Pavlov / Lax–Phillips reading (both **NOT-READ citations** here; the
equivalence above does not depend on them).

### 4.8 The decision table (governs; supersedes any earlier trichotomy)

| statement | relation to \(A\) | status |
|---|---|---|
| \(P_{\mathrm{naive}}\) (§4.4 definition) | \(A\models\neg P_{\mathrm{naive}}\) | **PROVED**, unconditional in the §9-upgraded form; residuals GAP-1/GAP-2 outside the conclusion chain |
| \(\neg P_{\mathrm{line}}(3/4)\) | \(A\nvDash\neg P_{\mathrm{line}}(3/4)\) | **PROVED, conditional on RH**; witness \(\varphi_3\); conditionality unavoidable *for this witness* |
| \(P_{\mathrm{line}}(3/4)\) | \(A\models P_{\mathrm{line}}(3/4)\)? | **OPEN and RH-HARD** — a positive answer proves RH via \(\varphi_3\) and the Proposition, in one line |
| decidability of \(P_{\mathrm{line}}(3/4)\) by \(A\) | \(A\) fails to decide it in at least one direction | **PROVED UNCONDITIONALLY** — RH \(\Rightarrow A\nvDash\neg P_{\mathrm{line}}(3/4)\); \(\neg\)RH \(\Rightarrow A\nvDash P_{\mathrm{line}}(3/4)\) |

The fourth row is the sharpest honest statement in the paper and should be
displayed as such.

### 4.9 Corollary — arithmeticity-blindness, correctly glossed

> **COROLLARY.** If \(A\models S\) then \(S\) holds for \(\varphi_q\) for
> every finite \(q\ge3\). Consequently **no consequence of \(A\)** separates
> arithmetic \(q\in\{3,4,6\}\) from non-arithmetic \(q\), and no \(A\)-only
> argument can serve as an arithmeticity criterion.

**Mandatory accompanying sentence (D9).** The Dirichlet *data* is **not**
arithmeticity-blind: the structures are pairs \((\varphi,\mathcal D)\) with
the \(g_n\) equal to the \(|c|\)-values, which lie in \(\mathbb Z[\lambda_q]\)
and therefore encode \(q\). An argument that inspects the Dirichlet data —
still "generic analytic machinery" by any ordinary reading — is **not**
covered by this corollary. Any gloss of the form "\(A\) cannot separate the
arithmetic members from the non-arithmetic ones" is refuted as written.

### 4.10 The open problem

> **OPEN.** Exhibit \(M=(\varphi,\mathcal D)\in\mathfrak M(A)\) and two
> nonreal zeros \(\rho_1,\rho_2\) with \(1/2<\Re\rho_i<1\) and
> \(\Re\rho_1\neq\Re\rho_2\). Any such \(M\) gives
> \(A\nvDash P_{\mathrm{line}}(c)\) for every \(c\) simultaneously.

Three reasons it is not available today, all to be stated: the \(G_5\)
off-line pin is a zero of the *Selberg zeta*, a different function, and on
the wrong side of the line; we have **no certified zero of any
\(\varphi_q\) for non-arithmetic \(q\)**; and a synthetic
Davenport–Heilbronn-type countermodel would still have to satisfy A4's
archimedean factor at \(\kappa=1\), A5, A6, and the exact modulus A7, none
of which has been checked. **Nothing in this paper asserts that such an
\(M\) exists.**

---

## 5. Appendix A (summary) — the Jensen/Littlewood rectangle, re-derived

Purpose: self-containedness. The rectangle identity (J) that the counting
argument consumes is normally imported from Selberg 1990, Lemmas 1 and 2,
reached only through Kelmer's (4.20). Appendix A re-derives it from the
standard complex-analytic toolkit and the interface facts already used.

Source: `SEL90_BYPASS_JENSEN_REDERIVATION_SOL.md` (corrections D-1..D-3
applied), cold-refereed in `SEL90_BYPASS_JENSEN_REDERIVATION_REFEREE.md`
(gate: PROMOTABLE-with-corrections).

| form | statement | status |
|---|---|---|
| (J)-sharp | rectangle identity with remainder \(O_q(\log T)\) at **every** \(T\) | **PARTIALLY re-derived** — one residual, GAP-1, a pointwise negative-part bound at height \(T\) |
| (J)-avg | same identity, remainder \(O_q(\log T)\) for **some** \(T^*\in[T-1,T]\) | **RE-DERIVED**, unconditional on the banked inputs |
| H3 | \(F_q(1/2,T)=(1/4\pi)T^2\log T+O_q(T^2)\), per-\(q\), both halves | **RE-DERIVED** from (J)-avg plus monotonicity of \(F_q\) |

Since the LAW's existence conclusion needs only H3, **the [Sel90] citation
is replaceable for the theorem of §3**. It is *not* replaceable for the
sharp asymptotic (C), which consumes (J)-sharp through the
finite-difference step; (C) does not appear in this paper's conclusion
chain.

Appendix contents in outline: Lemma A (orientation calibration of the
\(\Gamma\)-integral), Lemma B / (LW∞) with the \(1/\pi\), **Lemma C** (the
crux — the potential \(P(s)=-\int_s^\infty\log L^*\) has purely imaginary
jumps across the cuts, so \(\Re P\) is continuous and branch-free; no zero
count is used anywhere, hence no circularity), and Lemma D (conformal
sub-mean-value on a translated half-disc, with \(\kappa(R)\) independent of
\(T\) because \(H=H_0+iT\) is a pure translate). The referee reproduced
Lemma C's numerics on independent code at \(\mathrm{dps}=30\), agreeing to
\(10^{-26}\)–\(10^{-32}\) at seven heights including two where the divisor
is empty and two straddling the first zero ordinate
\(\gamma=7.06736257086735\).

**Honesty items for the appendix.** GAP-1 blocks only (J)-sharp; the Fubini
justification is by compactness on the box for each fixed \(T\), with no
uniformity in \(T\) claimed or needed; the \(3/2<\sigma<\sigma_1\) strip is
covered by the absolutely convergent series bound.

---

## 6. Machine verification

Statement to be used, exactly:

> The combinatorial / real-analytic **finish** of the theorem of §3 is
> machine-verified in Lean 4 (Mathlib), conditional on named hypotheses
> H1–H5, in
> `projects/aristotle_dispatch_v33/aristotle_dispatch_v33_aristotle/LawSkeletonI.lean`
> (the returned, `sorry`-free artifact; status line "No `sorry` bodies
> remain", with an independent local re-compile recorded). The verified
> statement is: growth of the weighted Jensen count together with
> finiteness of the real zeros implies infinitely many strictly off-line
> zeros and their reflections. **No scattering-theoretic content is
> machine-verified**: \(\varphi_q\) has no Lean definition, and no spectral
> theory, meromorphic continuation, Jensen/Littlewood rectangle, or property
> of \(\varphi_q\) is formalized. Those enter only as named hypotheses.

Two pointer corrections that the paper must respect:

1. The **dispatch** file `projects/aristotle_dispatch_v33/LawSkeletonI.lean`
   is *not* the artifact: it carries 16 `sorry` occurrences and states "This
   file machine-verifies nothing." Cite the
   `aristotle_dispatch_v33_aristotle/` path (D13).
2. Per `projects/aristotle_dispatch_v33/DISPATCH.md` §11, rows S5 (the
   rectangle (J)) and H3 (`hgrowth`) are **relabelled to PROVED** (this
   lane, refereed 2026-08-23, corrections D-1..D-3 applied), in the
   consumed (J)-avg form only. Scope limits unchanged: no \(q\)-uniform
   constant, no effective first height, no machine formalization of the
   analytic content. **H4 and H5 keep their "NOT proved here" labels** and
   the paper must say so.

---

## 7. Declarations of unread and transcribed sources

A single displayed paragraph, mandatory (D12 plus the second-audit
repairs):

- **Selberg 1990, Lemmas 1 and 2** — the complex-analytic engine citation,
  reached only through Kelmer's transcription of (4.20). **Not read** by any
  author or referee of the underlying notes. Its content is re-derived in
  Appendix A in the consumed form; GAP-1 and GAP-2 still rest on it and are
  outside the conclusion chain.
- **Selberg 1990** is also the correct attribution for the \(d=2\) counting
  theorem consumed as (C) (per Kelmer Remark 0.2); Kelmer's own contribution
  is the \(d\ge3\) generalization.
- **Iwaniec, §3.4** — the classical closed form of \(\varphi_3\); declared
  not read, corroborated twice inside our bank.
- **Venkov, Trudy Mat. Inst. Steklov 153 (1981), Thm 3.5 p. 59** — reached
  only through FJS, never at source. The 1979 Uspekhi survey is the wrong
  item.
- **Hejhal §7 and FJS** — consumed through `pdftotext` **transcriptions**,
  not verbatim quotations; the A1 (order \(\le2\)) and A6 chains rest on
  these.
- **Faddeev–Pavlov, Lax–Phillips** — not read; cited for context only.
- **Hejhal (7.2)–(7.5)** are stated for the conjugated group with cusp width
  1 and \(\varkappa\equiv1\); the normalization changes \(\varphi\) only by
  the zero-free factor \(c^{1-2s}\), which preserves the divisor and the
  functional equation. \(A\) is stated for the conjugated normalization.

---

## 8. [PLACEHOLDER] Certified localization at \(q=8\) — computation in progress

**No result is claimed in this section yet.** Intended content: an
interval-arithmetic certified localization of a resonance for \(q=8\),
produced by the Schur-complement contour machinery with adaptive
subdivision, as a concrete instance sitting alongside the non-effective
theorem of §3.

Status at the time of drafting, from `plans/wayfinder/rh-goals/MAP.md`:

- Target box provenance (certified scan, lane-K harvest `q8_mms_plus`,
  pin 1): \(s_0 = 0.4252310423737965 + 4.345760788321986\,i\), drift
  \(2.57\times10^{-13}\)/\(4.67\times10^{-13}\) across \(N\!=\!22\to28\),
  \(K_s\) box margin \(0.6227577\), \(\delta\ 0.0747680\), sign \(+1\);
  backup pin 3 at \((0.437608560356531, 7.278671743987394)\).
- Depth-8 subdivision wave: at the 2026-08-22 18:35Z tick, **400 of 1024
  leaves certified, PASS on every one, zero OPEN_MAX_DEPTH, \(q_{\rm Op}<1\)
  everywhere**; depth 8 confirmed sufficient across all sampled arcs.
  Remaining leaves in compute.
- The merged certificate additionally requires the merge procedure with the
  cross-host determinism check, and then the analytic-assembly referee
  campaign. Until both complete, **nothing from this lane may be stated as
  a theorem.**

**Related but distinct, and to be kept distinct:** the lane also holds a
*conditional effective* theorem
(`EFFECTIVE_THEOREM_ASSEMBLY_SOL.md`, promoted CONFIRMED-conditional on
eight named gates), which places an off-line zero of \(\varphi_q\) in an
explicit disc for every integer \(q\ge Q_0\) with
\(Q_0=11761546420922598622910053339543258496\) (\(\log_{10}Q_0\approx37.07\)).
That statement is conditional on its gates and its threshold is astronomical;
if it appears in the paper at all it belongs in a clearly-labelled remark,
never in the abstract.

---

## 9. Remark / outlook — prime geodesics (NOT a theorem)

**Label this a REMARK, not a result.** Off-line resonances enter the
explicit formula behind the prime geodesic theorem for the underlying
surface, so a proven family of off-line resonances on non-arithmetic Hecke
surfaces is a constraint that error-term analyses in that literature must
accommodate. Per `NOGO_AUDIENCE_SURVEY.md` (addendum), the prime-geodesic
community has **direct object overlap** with this theorem's subject, and —
unlike the class-(b) redirect targets — gains a *usable input* rather than
only a no-go.

**What must not be said here.** We derive no prime geodesic error term, no
effective first resonance height, and no \(q\)-uniform statement; the LAW
gives no effective first height at all. The remark is an outlook paragraph
naming a consumer, not a claim about the PGT.

---

## 10. Acknowledgments and authorship

**TODO (owner).** Acknowledgments, funding, collaborator credit, and the
authorship decision are left blank deliberately. See the companion draft
`KOYAMA_LETTER_DRAFT.md`.

---

## 11. Drafting checklist before any submission

- [ ] Owner decides authorship and whether to invite a coauthor.
- [ ] Every "NOT READ" declaration of §7 survives into the submitted text.
- [ ] Hejhal Thm 7.11 / Cor. 7.12 cited wherever novelty is framed.
- [ ] The non-arithmeticity clause never presented as a discriminant.
- [ ] §8 either carries a completed, refereed certificate or is deleted.
- [ ] Bombieri cited at most once, and not as a no-go.
- [ ] A cold referee reads the assembled manuscript before submission.

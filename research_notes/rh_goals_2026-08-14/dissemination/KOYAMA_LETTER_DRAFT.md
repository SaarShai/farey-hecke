# DRAFT — NOT SENT — OWNER REVIEW REQUIRED

**This is a drafting artifact only.** It has not been sent, will not be sent
without the owner's explicit instruction, and the owner should edit tone,
salutation, and every claim before any use. Each substantive sentence is
keyed to a banked source in the notes that follow the letter; the LEDGER
RULE applies — no sentence is stronger than its most-caveated source.

---

Dear Professor Koyama,

I hope this finds you well. I am writing with a substantial update on the
Hecke-group work we have discussed, because the picture has changed shape
since our last correspondence and I would value your judgement on how to
frame it.

**What is new.** Three things have landed.

First, a paper-level theorem, now double-audited by two independent cold
referees: for every finite integer \(q \ge 3\), the scalar trivial-character
scattering determinant of the one-cusp Hecke triangle orbifold has
infinitely many nonreal zeros with \(\Re\rho > 1/2\), and therefore
infinitely many multiplicity-matched scattering poles with
\(\Re(1-\rho) < 1/2\). In particular every nonarithmetic \(G_q\),
\(q \notin \{3,4,6\}\), has a scattering resonance strictly off the critical
line. I should say immediately what the audit forced me to see: this
statement is **not** an arithmeticity signature. The modular case \(q=3\)
has the same off-line property, and I have had to strike every gloss that
suggested otherwise.

Second — and this is the part I most want your reading on — I isolated the
hypotheses that proof actually consumes into an explicit axiom list
(continuation of order at most two, the functional equation
\(\varphi(s)\varphi(1-s)=1\), reality, a generalized Dirichlet series with
the Hejhal archimedean factor at \(\kappa=1\), finiteness and reality of the
right divisor with strip confinement, a polynomial vertical bound, the exact
critical-line modulus), and proved a metatheorem over the class of all
structures satisfying it. The axiom list *entails the negation* of the naive
on-line rigidity statement. So no proof schema quantifying over that class
can place all right-half-plane zeros on \(\Re s = 1/2\); a schema that
appears to do so is already refuted by \(\varphi_3\). A second, sharper and
unconditional line: the axiom list fails to decide the genuine RH-analogue
\(P_{\rm line}(3/4)\) in at least one direction, whichever way RH goes. And
the converse direction — whether the axioms *prove* the RH-analogue — is
open and RH-hard, since a positive answer would prove RH in one line through
\(\varphi_3\).

Third, two pieces of hygiene that make the paper self-contained. The one
citation the chain still leaned on — Selberg's 1990 lemmas, reached only
through Kelmer's (4.20), and read by nobody in the project — has been
re-derived independently in the form the argument consumes, and that
re-derivation has itself been cold-refereed and its corrections applied.
Separately, the combinatorial finish is now machine-verified in Lean,
conditional on named hypotheses; no scattering-theoretic content is
formalized, and I am careful to say so. A certified interval-arithmetic
localization at \(q=8\) is still in compute — roughly 400 of 1024 leaves
certified, every one passing — and is not part of any claim yet.

**Why I think it matters.** The moral is old: since Davenport–Heilbronn in
1936 it has been folklore that a functional equation without an Euler
product does not force zeros onto the line, and the Selberg class encodes
that folklore as an axiom. What was missing was a theorem-strength analogue
on the spectral/scattering side, which is exactly why spectral programs have
continued as though their setting were exempt. Conrey and Li's 2000 note is
the methodological precedent I am modelling on — a negative control that
kills a named schema. So the contribution is narrow and I intend to state it
narrowly. But it does mean the dichotomy you called a paradigm shift now has
a resonance-side theorem next to it, and a no-go that says precisely which
part of the analytic apparatus can never do the work.

**What I would ask of you.** Two things, whichever you have time for. First,
your read on the metatheorem's framing — in particular whether the axiom
list is the right one to put in front of this audience, and whether the
"decidability fails in at least one direction" statement is the right
headline or whether it will read as a curiosity. You know the community's
tolerances far better than I do. Second, whether you would have any interest
in joining this as a coauthor, or in advising on where it should go. I would
be glad either way, and glad simply to hear your objections.

I can send the full draft, the two referee reports, and the re-derivation
appendix at once if that is useful.

With warm regards and thanks,

**[TODO — owner: signature, affiliation, contact]**

---

## Source notes (not part of the letter)

- **Theorem statement**: quoted from the 2026-08-19 promotion block of
  `research_notes/rh_goals_2026-08-14/lane_g/LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_SOL.md`;
  double-audited CONFIRMED by `LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_REFEREE.md`
  and, cold and independently, by `LAW_SECOND_AUDIT_REFEREE.md`.
- **Non-discrimination caveat**: `LAW_..._SOL.md:486–489` — the
  "nonarithmetic in particular" clause carries zero arithmeticity
  information and must never be used as an arithmeticity signature.
- **Axiom list, Metatheorem I (unconditional form \(A \models \neg
  P_{\rm naive}\)), Metatheorem II, D8a OPEN-and-RH-HARD, D8b unconditional**:
  `NOGO_METATHEOREM_SOL.md` §§1–5 with the §8 corrections and the §9
  addendum governing.
- **Sel90 bypass**: `SEL90_BYPASS_JENSEN_REDERIVATION_SOL.md` +
  `..._REFEREE.md` (gate PROMOTABLE-with-corrections; D-1..D-3 applied);
  relabelling licence recorded in
  `projects/aristotle_dispatch_v33/DISPATCH.md` §11. GAP-1 and GAP-2 remain
  and are outside the conclusion chain — the letter does not claim otherwise.
- **Machine verification**: the returned, `sorry`-free artifact at
  `projects/aristotle_dispatch_v33/aristotle_dispatch_v33_aristotle/LawSkeletonI.lean`,
  conditional on H1–H5; H4 and H5 remain "NOT proved here".
- **q8 compute figures**: `plans/wayfinder/rh-goals/MAP.md`, tick
  2026-08-22 18:35Z (400/1024 leaves, all PASS, zero OPEN_MAX_DEPTH).
- **Framing, Davenport–Heilbronn, Conrey–Li**:
  `NOGO_AUDIENCE_SURVEY.md` §§1, 3. Bombieri deliberately not cited.
- **"paradigm shift"**: Koyama's own characterization of the arithmeticity
  dichotomy, as recorded in the project memory; the letter attributes it to
  him rather than asserting it.
- **Not said in the letter, deliberately**: no effective first height, no
  \(q\)-uniform error, no arithmeticity criterion, no prime-geodesic
  consequence, and no claim that the \(q=8\) certificate exists.

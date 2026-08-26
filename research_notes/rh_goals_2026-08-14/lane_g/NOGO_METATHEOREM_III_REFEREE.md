# COLD ADVERSARIAL REFEREE — Metatheorem III / NOGO-OPEN-1

Date: 2026-08-26. Object: `NOGO_METATHEOREM_III_DRAFT.md`. Posture:
read-only except this report; attempted refutation against the mandated repo
sources and the directly load-bearing FJS/MMS/Lean artifacts.

## Executive ruling

The load-bearing mathematical claim survives. The promoted two-pin assembly,
the FJS Selberg/scattering divisor classification, the one-cusp scalar
specialization, and the functional-equation reflection together exhibit one
fixed pair whose scalar scattering function has two nonreal right-strip zeros
with distinct real parts. That is enough for the NOGO-OPEN-1 standard in
`NOGO_METATHEOREM_SOL.md:468-474`. Section 5.1 does not require a direct
`phi_5` evaluator or an end-to-end Lean formalization, so D11's former direct-
certifier blocker does not defeat this indirect, citation-backed exhibition.

I did not refute the pin values, their separation, the claimed independence
from `[Sel90, Lemmas 1,2]`, or the fixed-witness quantifier argument. I do,
however, require corrections to the theorem's formal witness notation,
quantifier display, inherited caveat/status language, exact imaginary
intervals, and description of the Lean result. I also found one FJS source-
notation caveat not recorded by either S2 referee.

## Sources and integrity checks

1. The FJS PDF at
   `lane_p/literature/FJS_completed_zeta_divisor.pdf` has SHA-256
   `36c9d020fcc7d0118264c486330db9936f866670c45c0e77b185cdc2b9127228`,
   exactly the mandated hash. I inspected the rendered and extracted complete
   relevant pages 4-6 and 11, not merely the assembly's transcription.
2. `THEOREM_G5_SECONDPIN_ASSEMBLY.md:5-22` is `REFEREED — PROMOTED
   2026-08-26`; it records both PASS-WITH-CORRECTIONS seats and says their four
   exact correction sets were applied. It establishes the two-pin premise,
   not by itself the membership premise or closure of NOGO-OPEN-1.
3. `THEOREM_G5_OFFLINE_ASSEMBLY.md:4-15` is `DECLARED` after five
   adversarial rounds and a theorem-grade V8 ruling. It is not labelled
   `REFEREED — PROMOTED`; nothing in the draft requires that stronger label.
4. The Fable and SOL assembly reports both end PASS-WITH-CORRECTIONS and
   report no refutation of the certified boxes, winding, R5 domain, whole-box
   `K_s` exclusion, FJS/MMS source content, or real-part separation. Their
   required corrections are represented in the current promoted assembly.

## 1. Does the FJS bypass meet the section 5.1 standard for zeros of phi?

Yes, at ordinary theorem-level mathematical standards. It is an indirect
certificate of actual zeros of the scalar `phi_5`; it is not merely a
statement about zeros of a different function.

The source-level implication is as follows.

- FJS p. 5, section 2.4 defines `phi(s)=det Phi(s)`, gives
  `phi(s)phi(1-s)=1`, and exhaustively lists the nonreal scattering divisor:
  right-strip zeros `rho, conjugate(rho)` and reflected left-strip poles
  `1-rho, 1-conjugate(rho)`.
- FJS p. 6, section 2.5 exhaustively lists the Selberg-zeta divisor. Every
  other listed zero is real, on `Re s=1/2`, or a real trivial divisor. Thus a
  nonreal Selberg-zeta zero with `0<Re s<1/2` can only be one of
  `1-rho, 1-conjugate(rho)` arising from a right-strip scattering zero.
- Both certified pin boxes have positive imaginary part and lie strictly in
  `0<Re s<1/2`. Consequently, for each pin zero `s_i`, `1-s_i` is the
  corresponding negative-imaginary zero of the scattering determinant. FJS
  p. 11, Definition 3.8 (`Z_+=Z/(G_1 Gamma^k)`, `Z_-=Z_+ phi`) and the
  same-multiplicity symmetry `N(Z_-)=1-N(Z_+)` also give the matching-order
  version; `SCAT1_DIVISOR_GATE_CHECK.md:78-100` records that derivation.
- MMS states that every finite Hecke triangle group has one cusp. For the
  trivial one-dimensional representation, FJS's own definition
  `k=sum_j dim V_j` gives `k=1`; hence the scattering matrix is `1x1` and its
  determinant is the scalar `phi_5` used in `A0`.
- The sorry-free returned Lean theorem at
  `projects/aristotle_dispatch_v33/aristotle_dispatch_v33_aristotle/aristotle_dispatch_v33_aristotle/Scat1Lemma31Reflection.lean:38-75`
  verifies the generic order-preserving implication pole at `s` to zero at
  `1-s`, assuming meromorphy and the functional equation. The root dispatch
  file still contains `sorry`; the nested returned file is the verified one.

Therefore the absence of a direct `SCAT-EVAL_5` zero-minus-pole evaluator is
not a logical gap under NOGO-OPEN-1's printed standard. Section 5.1 asks for
two zeros of `phi`, not for a specified certification technology. D11 was
correct when written, before the two-pin FJS bridge was assembled; the
promoted S2 assembly supersedes its factual premise for these two pins only.

Two qualifications are mandatory.

First, this is an indirect, citation-backed `phi_5` certificate. Lean proves
only the abstract pole-to-zero reflection; it does not define `phi_5`, prove
the FJS divisor theorem, or formalize the MMS specialization. The draft must
not call the whole bridge Lean-verified or a direct certifier.

Second, FJS p. 4 contains an internal notation inconsistency not flagged in
either S2 referee: immediately after defining `k` as the degree of singularity
`sum_j dim V_j`, it says that "k = 0" because higher-weight forms are not
considered. For the one-cusp trivial representation the stated definition
gives `k=1`; the sentence evidently uses or collides with automorphic-weight
notation, while the subsequent Theorem 2.1 and divisor formulas retain the
degree-of-singularity parameter. This does not alter the set-level divisor
classification used here, but it must be disclosed alongside the already
recorded MMS `q=5` heading inconsistency. It may not be silently quoted as an
uncaveated scalar-specialization source.

## 2. Is M_5=(phi_5,D_5) in M(A), and what caveats attach?

Yes. `NOGO_METATHEOREM_SOL.md:247-252` states the breadth lemma for every
finite integer `q>=3`, explicitly including arithmetic and non-arithmetic
members. Therefore it includes `q=5`. Its proof is the row-by-row receipt
table in section 2, where every axiom is PASS for the non-arithmetic family.
The later re-referee also correctly distinguishes the Hejhal/FJS receipts as
membership evidence rather than hypotheses imported from Sel90.

The draft's notation is not yet formal enough. `M(A)` contains pairs, not bare
functions (`NOGO_METATHEOREM_SOL.md:80-87`). The witness must be written

`M_5=(phi_5,D_5)`, where `D_5=(d_5(n),g_{5,n})_{n>=1}` is the Hejhal/FJS
Dirichlet data used in the `q=5` A4 receipt.

Writing an unindexed, undefined `D` and then saying "phi_5 is in M(A)" is
acceptable shorthand in the source lemma but insufficient in the final
exhibition.

Membership is licensed only at the standing explicitly attached to section
3.2: "at the caveat level of section 5.3." Those caveats are not additional
axioms and none is a known failure, but they are provenance/status limits and
must travel with Metatheorem III. In current, correction-aware form they are:

1. the old A5 strip-confinement flag is superseded by section 8/D6, which
   derives confinement immediately from A4's right-edge normalization;
2. A4 discreteness is source-established by FJS Theorem 2.1; enumeration is
   corroboration, not the theorem;
3. the A1/order and A6 source chain rests on Hejhal/FJS transcriptions that
   were cold re-extracted and image-checked but are not machine-checked
   quotations; and
4. the width-one/conjugated Hecke normalization changes `phi` by the
   zero-free factor `c^(1-2s)`, so it preserves the functional equation and
   divisor, but the normalization repair must remain disclosed.

The Metatheorem III theorem block must explicitly inherit section 3.2/5.3
(as superseded by section 8) and the two assemblies' computer-assisted and
citation ledgers. A cross-reference inside the block is sufficient; omitting
the standing from the quotable statement is not.

## 3. Sel90 independence

The claimed independence is correct, including the membership step, provided
it is stated as independence from the specific `[Sel90, Lemmas 1,2]` LAW
engine rather than from all classical Selberg/scattering literature.

The two pin links and the promoted S2 dependency ledger consume contour
receipts, finite-section and determinant comparison, R5, the exact `K_s`
divisor, MMS Theorems 6.4/4.10, the FJS divisor classification, and the Lean
reflection core. Neither pin assembly contains a LAW or Sel90 input. The
`q=5` membership proof is section 3.2's section-2 row-by-row Hejhal/FJS/MMS
receipt proof. It does not invoke Metatheorem I's Jensen/counting proof.

The fact that the explicit axiom list `A` was historically extracted while
auditing the LAW does not make the LAW, or Sel90, a premise of the semantic
statement `A not-models P_line(c)`. The explicit axioms and the proof that
`M_5` satisfies them are independently stated. The Sel90 residuals belong to
the old Metatheorem I counting route, not to this countermodel exhibition.

Accordingly, draft lines 54-60 are sound if "Sel90 never enters" means that
the named Sel90 engine is absent. The route still relies on other published
Selberg/scattering results and must not be advertised as citation-free.

## 4. Pin data

The draft matches the promoted S2 assembly exactly:

| quantity | promoted assembly and draft |
|---|---|
| `Re rho_1` | `[0.54610381992505530, 0.54610581992505530]` |
| `Re rho_2` | `[0.58945526450526373, 0.58945726450526373]` |
| closed-interval separation | `0.04334944458020843` |

The separation is exact endpoint arithmetic:

`0.58945526450526373 - 0.54610581992505530 = 0.04334944458020843`.

The promoted assembly also gives the exact nonreal intervals:

- `Im rho_1` in `[-5.7635382417301305, -5.7635362417301305]`;
- `Im rho_2` in `[-7.81976924701551188, -7.81976724701551188]`.

The draft's `Im approximately ...` shorthand is weaker than, and repeats a
phrasing defect already removed from the promoted assembly by the SOL seat.
The theorem note must quote the intervals or explicitly cite them, not use a
box centre as if it were the certified zero.

## 5. Quantifier structure

The implication is valid, but the fixed-witness quantifiers should be printed
instead of left to the word "simultaneously."

Let `r_i=Re rho_i`, with `r_1 != r_2`. For any fixed `c`, at least one of
`r_1,r_2` differs from `c`, so at least one certified zero violates
`P_line(c)`. The same fixed `M_5` works for every `c`. The strongest clean
form delivered by the exhibition is

`there exists M_5 in M(A) such that for every c in (1/2,1),
M_5 does not satisfy P_line(c)`.

It follows that

`for every c in (1/2,1), A does not model P_line(c)`.

Thus this is stronger than a bare `for every c there exists some M_c`
argument: there is one common countermodel. Equivalently, when `c` is made an
object-language real parameter, `A` does not entail `there exists c in
(1/2,1) such that P_line(c)`.

The draft's conclusion about derivations follows by the semantic definition
in `NOGO_METATHEOREM_SOL.md:225-238`, but "ANY on-line rigidity statement" is
too broad. The proof excludes exactly the family `P_line(c)` (indeed for any
real `c`), not every conceivable statement one might describe informally as
on-line rigidity.

## Exact required corrections

1. Define the actual witness data before the membership claim:
   `D_5=(d_5(n),g_{5,n})_{n>=1}` from the `q=5` Hejhal/FJS A4 receipt, and
   `M_5=(phi_5,D_5)`. Replace the shorthand `phi_5 in M(A)` by
   `M_5 in M(A)` in the exhibition and theorem block.
2. Replace the draft's point-like imaginary shorthand by the two exact closed
   intervals quoted in section 4 of this report. Preserve the no-conjugation
   formula `rho_i=1-s_i`.
3. Replace "Lean reflection core (order-preserving pole<->zero)" by
   "the cited FJS divisor step, followed by the Lean-verified
   order-preserving pole-to-zero implication under
   `phi(s)phi(1-s)=1`." Identify the nested returned Lean file as the verified
   artifact; do not imply that the FJS/MMS bridge or `phi_5` is formalized.
4. Put the fixed-witness quantifiers in the METATHEOREM III block:
   `there exists one M_5 in M(A) such that for every c in (1/2,1), M_5 does
   not satisfy P_line(c); hence for every such c, A does not model
   P_line(c)`. Replace "ANY on-line rigidity statement" by "any member of
   the family P_line(c)."
5. Add inside the theorem block an explicit standing sentence: the result is
   at the caveat level of `NOGO_METATHEOREM_SOL.md` sections 3.2/5.3 as
   superseded by section 8, and at the computer-assisted/citation standing of
   the two pin assemblies. Retain the MMS `q=5` heading caveat and add the FJS
   p. 4 `k=0` versus degree-of-singularity `k=1` notation inconsistency to the
   dependency ledger.

After these corrections, the draft may be promoted and NOGO-OPEN-1 may be
marked closed at the explicitly stated citation/computer-assisted standing.

VERDICT: PASS-WITH-CORRECTIONS

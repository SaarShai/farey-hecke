# Maximally adversarial referee report — 2026-08-26

## Scope

Reviewed the current `main.tex` and compiled 15-page `main.pdf`, the machine-verification artifacts named by the manuscript, and the advertised data-availability package. I used `PREPRINT_REFEREE_2026-08-26.md` only to avoid repeating its source-fidelity audit. I did not recheck its decimal transcriptions or its full internal-source comparison.

Two defects from that report nevertheless reappear in the current source and PDF. They are reported below because they are live theorem/presentation defects, not because I reran the old fidelity pass.

## Executive summary

**Combined verdict: NO.** The current manuscript might clear arXiv's minimal subject-matter moderation, because it contains recognizable mathematics in math.NT/math.SP. It is not safe to upload in this form: the PDF visibly says `DRAFT`, contains a submission checklist and an empty authorship section, repeats a false simplicity claim, advertises a rendered figure as “Not yet rendered,” and makes a priority claim that the cited literature does not support. It would not survive a serious journal referee. My recommendation as a simulated Referee 2 is **reject in present form; invite a wholly rewritten paper only if the authors first isolate a genuinely new theorem and supply its proof and reproducibility package**.

The potentially publishable mathematical core is much narrower than the manuscript says:

1. a fixed-`q` consequence of the classical Selberg/Hejhal weighted scattering-divisor machinery, if the authors can prove that the precise orbifold hypotheses and normalization cover every finite Hecke triangle group and if this consequence is not already explicit in the literature; and
2. two rigorously interval-certified `q=5` transfer-operator zeros, hence two Selberg-zeta zeros and, after a published divisor theorem plus the scattering functional equation, two scattering zeros with distinct real parts.

The first item is presently asserted rather than proved. Its engine is recognizably classical. The second may be a real computational upgrade over heuristic numerics, but the paper does not expose the certificate chain sufficiently and the advertised archive does not contain the final promoted second-pin assembly/merged contour receipt. The “metatheorems” add almost no mathematical content: once a class has a universal off-line theorem or one counterexample, the displayed semantic non-entailments are immediate.

The central title claim — “what the generic scattering axioms cannot decide” — is not proved. Unconditionally, Metatheorem III establishes only `A \nvDash P_line(c)`. It does **not** establish `A \nvDash \neg P_line(3/4)`; that direction is conditional on RH. Failure of one entailment is not undecidability.

## Numbered defects

### BLOCKING

#### 1. The title and abstract claim non-decision; the paper proves only one unconditional non-entailment

**Location:** title, `main.tex` lines 16–17; abstract lines 47–52; Metatheorem II lines 391–402; decision table lines 432–450.

**Problem:** To say that `A` “cannot decide” `P_line(3/4)` has the standard meaning

\[
A\nvDash P_{\mathrm{line}}(3/4)
\quad\text{and}\quad
A\nvDash\neg P_{\mathrm{line}}(3/4).
\]

Metatheorem III proves the first statement unconditionally. Metatheorem II proves the second only under RH, using `\varphi_3`, and lines 400–402 expressly concede that there is no unconditional collinear witness. Calling this “fails to decide it in at least one direction” is a semantic dodge: any theory that entails `\neg P` also fails to entail `P`, yet it decides `P`. The decision-table row “decidability ... PROVED UNCONDITIONALLY” is therefore false or, at best, deliberately nonstandard terminology. The title overclaims the strongest result in the paper.

**Repair:** Either produce an unconditional model of `A` satisfying `P_line(3/4)` and then state genuine semantic independence, or delete every occurrence of “decide,” “undecidable,” and “cannot decide.” A truthful title would say that the axioms **do not imply vertical-line rigidity**.

#### 2. The LAW and Metatheorem I have no paper-level proof

**Location:** Theorem 2.1 and the undefined supporting count, lines 175–203; proof sketch, lines 365–389; “Appendix A (summary),” lines 749–795; machine-verification scope, lines 860–900.

**Problem:** The main theorem is followed by a displayed asymptotic for `F_q(1/2,T)`, but `F_q` is never defined anywhere in `main.tex`. The reader is not told the divisor being summed, whether multiplicities and poles enter with signs, whether both half-planes are counted, or why the extra triangular weight produces `T^2 log T` rather than the standard `T log T` weighted divisor count. The alleged proof is a paragraph naming Jensen/Littlewood, a gamma identity, and internal labels `(J)-avg`, `H3`, `GAP-1`, `(C)`, and `(DIF)`. Appendix A does not state or prove Lemmas A–D; it gives a status table and an outline. `LawSkeletonI.lean` assumes the crucial growth hypothesis `hgrowth`/H3 and formalizes only the elementary implication “growth + finitely many real zeros => infinitely many nonreal zeros.”

This is not a proof of Theorem 2.1 and not a proof that every `M in M(A)` satisfies the growth law. The transfer sentence at lines 380–389 (“transfers verbatim”) is the very theorem that needs proof.

**Repair:** Define `F_q` exactly; state a generic analytic theorem with all hypotheses; prove the admissible-height selection, Littlewood identity, boundary bounds, critical-line integral, pole terms, monotonic interpolation, and multiplicity conventions in the paper; then specialize it to `\varphi_q` row by row. Alternatively, state the LAW and Metatheorem I explicitly conditional on H3 and stop saying they are proved from A.

#### 3. The displayed “axiom system” is not a well-defined mathematical class

**Location:** structures and A0–A7, lines 252–301.

**Problem:** `M=(\varphi,\mathcal D)` contains only a meromorphic function and sequences `(d(n),g_n)`, but A0 predicates it with undefined external notions (“one channel,” “degree of singularity 1,” “archimedean factor carries `\kappa=1`”). “Meromorphic of order at most 2” is not defined — Nevanlinna order, a quotient of entire functions of order at most two, or something else? A5 does not say whether “every zero lies in a vertical strip” means every zero in `C`, every right-half-plane zero, or a strip whose constants are part of the model. No satisfaction relation or formal language is supplied, even though the manuscript repeatedly invokes models, semantic entailment, derivability, proof schemas, and decidability.

The authors can use `\models` informally, but only after defining an ordinary class of analytic objects precisely. As displayed, membership is not checkable.

**Repair:** Delete the model-theory costume and define a class `C_A` by explicit analytic conditions, including all constants, domains, divisor conventions, and normalizations. Then state ordinary universal/counterexample propositions. If actual model theory is intended, specify the language, structures, and satisfaction relation.

#### 4. A4 does not imply the right-edge estimate used in the proof

**Location:** A4, lines 273–280; “strip confinement” note, lines 299–301; Metatheorem I proof sketch, lines 365–369.

**Problem:** A4 assumes only `d(1) != 0` and `0 < g_1 < g_2 < ...`; it does not assume `d(1)=g_1=1`. Therefore the asserted consequence `|L^*-1|<1` for large `Re s` does not follow. The leading term is `d(1)g_1^{-2s}`, not `1`. If `g_1<1` it grows, if `g_1>1` it decays, and if `g_1=1` it tends to `d(1)`. A normalized series may tend to one, but that normalization is absent.

This is a genuine broken joint in the advertised A-to-H3 transfer. A zero-free leading exponential can probably repair the argument, but it changes the boundary calculation and must be carried explicitly.

**Repair:** Require `d(1)=g_1=1`, or define

\[
\widetilde L(s)=\frac{L^*(s)}{d(1)g_1^{-2s}}
\]

and prove `|\widetilde L-1|<1`, tracking the removed factor in every contour integral and asymptotic.

#### 5. The “breadth lemma” is an assertion, not a lemma

**Location:** lines 315–328; reused at lines 481–506 and 519–526.

**Problem:** The statement `\varphi_q in M(A)` for every finite `q` is load-bearing twice: it is the specialization of the LAW and the membership premise for the `q=5` countermodel. The paper supplies no theorem environment, no receipt table, and no proofs of A0–A7. It gives one elementary `q=3` Dirichlet-series computation and says the remaining “receipts are per-axiom.” That is an internal-project claim, not a journal proof. It is particularly inadequate for A1, A5, and A6, whose precise strength may not match the cited sources.

**Repair:** Include a proposition with a two-column source table (`q=3`, general finite `q`), exact theorem numbers and normalizations, followed by proofs of every nontrivial implication. Read and verify the load-bearing sources; do not cite an internal “receipt.”

#### 6. The novelty claim is contradicted by direct prior literature

**Location:** abstract lines 54–58; introduction lines 67–74 and 85–100; prior-art list lines 102–150.

**Problem:** “No theorem-strength analogue on the spectral/scattering side” and “first single-family version” are not credible.

- Selberg's 1990 scattering-pole distribution and Hejhal's treatment are the source of the exact Jensen/Littlewood engine being repackaged. Kelmer's [Theorem 3 and Section 4](https://arxiv.org/abs/1402.4780) give the modern higher-dimensional formulation and explicitly attribute the surface case to Selberg; DOI [10.1093/imrn/rnv051](https://doi.org/10.1093/imrn/rnv051).
- Hejhal, *The Selberg Trace Formula*, Vol. 2, Theorem 7.11/Corollary 7.12 already gives right-zero/left-pole accumulation in the Hecke family. Garbin–Jorgenson, [*Spectral asymptotics on sequences of elliptically degenerating Riemann surfaces*](https://ems.press/journals/lem/articles/16236), quantifies that Hecke-family result; DOI [10.4171/LEM/64-1/2-7](https://doi.org/10.4171/LEM/64-1/2-7).
- Phillips–Sarnak gave theorem-strength deformation and resonance-dissolution results in [Invent. Math. 80 (1985)](https://doi.org/10.1007/BF01388610) and [JAMS 5 (1992)](https://doi.org/10.1090/S0894-0347-1992-1127079-X). Their [*On the spectrum of the Hecke groups*](https://doi.org/10.1215/S0012-7094-85-05212-3) is direct Hecke-family spectral precedent.
- The transfer/zeta apparatus is classical or established for Hecke groups: Fried [1986](https://doi.org/10.24033/asens.1515), Mayer–Mühlenbruch–Strömberg [2012](https://doi.org/10.3934/dcds.2012.32.2453), Möller–Pohl [2013](https://doi.org/10.1017/S0143385711000794), Pohl [2016](https://doi.org/10.1017/etds.2014.64), and Adam–Pohl [2020](https://doi.org/10.1017/etds.2018.51).

Not all of these papers prove the exact fixed-`q` infinitude claimed here. That distinction is the only possible novelty opening. The manuscript never performs the required theorem-by-theorem comparison. A priority claim is not established by declaring selected sources “not read.”

**Repair:** Replace the priority rhetoric with a precise delta table: prior theorem, its hypotheses, why it does not already imply the fixed-`q` orbifold statement, and the exact new lemma supplied here. If the result is only a clean specialization/corollary of Selberg–Hejhal–Kelmer, say so.

#### 7. The current theorem again makes the false simplicity inference the prior referee said was fixed

**Location:** lines 210–215; contradicted by lines 1065–1078; visible on PDF page 3.

**Problem:** “winding = 1 so each zero is simple” applies to the certified zero of `det(1-L_{s,+})`, not automatically to the zero of the full Selberg zeta function. In the MMS factorization the `-` determinant may also vanish at the point. The later corollary correctly proves only that the `Z_{G_5}` multiplicity is **at least** that of the `+` factor. The current source therefore reintroduces defect D-1 from the earlier report and is internally inconsistent.

**Repair:** Say: “each box contains exactly one simple zero of the `+` Fredholm factor and hence a zero of `Z_{G_5}` of multiplicity at least one.” Claim simplicity of the Selberg-zeta zero only after separately certifying the `-` factor nonzero in both boxes.

#### 8. The two-pin-to-scattering chain is compressed across numerous unproved joints

**Location:** lines 234–247, 499–567, and 1065–1100.

**Problem:** The elementary last step is valid: two actual `\varphi_5` zeros in the strip with distinct real parts refute every `P_line(c)`. But the paper does not prove that its two numerical boxes contain such zeros. The full chain is:

1. define the exact `q=5`, `+` transfer operator and its determinant normalization;
2. prove the interval evaluation encloses the determinant on the whole contour and excludes zero there;
3. prove the computed winding is one;
4. pass from the finite section to the infinite Hilbert-space determinant using an explicit determinant-norm inequality and numerical constants;
5. justify the argument-principle homotopy;
6. prove the Hilbert-to-Banach transport R5 and equality of determinants on `Omega*`;
7. exclude every zero/pole of the `K_s` denominator on each full box;
8. establish that MMS Theorem 6.4 applies at `q=5` despite the printed `q>5` heading;
9. conclude a zero of raw `Z_{G_5}` with the correct multiplicity lower bound;
10. state the exact FJS divisor theorem showing that a nonreal left-strip `Z` zero here is a scattering pole of `\varphi_5`, with no completed/trivial/gamma divisor or cancellation at the boxes;
11. use `\varphi(s)\varphi(1-s)=1` to reflect that pole to a multiplicity-matched zero at `1-s_i`;
12. transport the certified rectangles and prove their real parts distinct; and
13. prove `(\varphi_5,\mathcal D_5) in M(A)`.

Lean checks only items 11–12 abstractly and the trivial two-points/no-line implication. MMS/FJS can legitimately discharge parts of 8–10, but the manuscript must state their exact theorems and verify their hypotheses. Items 1–7 and 13 are neither in the paper nor in a stable cited supplement.

**Repair:** Add a computer-assisted-theorem section containing formal definitions, a certificate theorem, all error bounds, exact artifact identifiers, and a dependency table with “proved here / machine checked / published theorem.” Do not replace those statements with labels such as R5, “machine constants,” “whole-box exclusion,” or “cold referee ruled sufficient.”

#### 9. The advertised archive does not substantiate the second pin

**Location:** data availability, lines 903–921; `dissemination/zenodo_package/README.md` lines 20–68; packaged `certificates/pin2_second/W_ENVELOPE_CERT_S2.md` lines 3–11; final assembly pointer in `lane_g/THEOREM_G5_SECONDPIN_ASSEMBLY.md` line 79.

**Problem:** The package labels `W_ENVELOPE_CERT_S2` “REFEREED / PROMOTED,” but that file's table says `VERDICT NOT` at `N=48` and “minimal certifying N 1287.” It is a tail-envelope component, not the final winding certificate. The final promoted assembly and `S2_MERGED_CONTOUR_RECEIPT.json` are not in the package; the README itself admits that cited artifacts and merge checkpoints were omitted. Thus the statement that “all material supporting this paper is archived” is false, and an external referee cannot reproduce Theorem 2.2 or Metatheorem III from the advertised package.

This does not prove the pin is false. It proves that the paper has not delivered the evidence needed to accept it.

**Repair:** Deposit the exact final source, local chunks, merged contour receipt, assembly theorem, dependency versions, scripts, and verification command in an immutable archive. Make the manifest map every theorem joint to one artifact. Remove the failed N=48 component as the apparent theorem certificate or label its limited role accurately.

#### 10. The BBM/Berry–Keating “worked audit” is mathematically inapplicable

**Location:** lines 597–747, especially 645–703.

**Problem:** The section admits that the authors have not checked the paper beyond its abstract and that items 1–6 are their reconstruction. More seriously, it conflates two different lines. Self-adjointness for a zeta Hamiltonian is intended to place zeta zeros on `Re w=1/2`, which under `w=2s-1` becomes `Re s=3/4` for zeros of `\varphi_3`. It is not `P_naive`, which forbids all nonreal `\varphi` zeros in `Re s>1/2` and is false for `\varphi_3` even under RH. The paper itself explains this calibration at lines 420–424 and then ignores it in the audit.

There is also no functor from an arbitrary scattering pair `(\varphi,\mathcal D)` to the BBM operator or boundary condition. Saying “if the open step used only our reconstructed list, then it could not work” is a tautological conditional, not an audit of BBM.

**Repair:** Delete the entire worked audit. It is irrelevant, based on unread work, and its identification of the desired conclusion is wrong. A separate expository essay could discuss proof-schema diagnostics after reading the primary literature and formulating a genuine transfer theorem.

### MAJOR

#### 11. The “metatheorems” are semantic repackaging, not new mathematics

**Location:** all of Section 3, especially lines 346–363, 452–469, and 471–516.

**Problem:** `A models not P_naive` is just the generic analytic theorem, if proved. `A not-models P_line(c)` follows immediately from one counterexample. The “blindness” corollary says that a sentence true in all models is true in each listed model — a tautology. The model-theoretic vocabulary creates the appearance of foundational depth without a formal theory, definability result, compactness argument, independence construction, or nontrivial transfer principle.

**Repair:** Replace the entire metatheorem section with one short “scope of hypotheses” proposition and one counterexample corollary. Spend the saved space proving the analytic theorem.

#### 12. Metatheorem II is only an RH restatement, not an independence theorem

**Location:** lines 391–430.

**Problem:** The proposition correctly observes `P_line(3/4)` for `\varphi_3` iff RH. Therefore “assuming RH, `\varphi_3` witnesses `A not-models not P_line(3/4)`” is merely RH rewritten in the manuscript's notation. It supplies no unconditional information about A and no model construction.

**Repair:** Keep the calibration as a two-sentence remark. Do not number it as a metatheorem or use it to advertise decision/independence.

#### 13. `P_naive` is not “on-line rigidity” in the ordinary sense

**Location:** lines 330–344 and 348–363.

**Problem:** `P_naive` says there are no nonreal zeros in the open right half-plane. It does not say that zeros lie on a line; it ignores line zeros and permits finitely many real right zeros under A5. Moreover A2+A3 already force no divisor on the scattering symmetry line, so `Re s=1/2` is not a plausible RH line for these scattering zeros. Calling the negation a no-go for “on-line rigidity” encourages exactly the confusion the later `3/4` calibration corrects.

**Repair:** Rename it `P_no-right-nonreal` and present its failure as a scattering-divisor existence theorem, not an RH analogue.

#### 14. The arithmeticity-blindness corollary is tautological and its gloss is self-contradictory

**Location:** lines 452–469 and 741–747.

**Problem:** If A has every `q` member as a model, an unconditional sentence entailed by A holds for every `q`; that says nothing about whether analytic arguments can distinguish subfamilies. Since the structure includes `\mathcal D`, and the paper immediately concedes that `g_n` encodes `q`, an A-language conditional or an argument inspecting D can distinguish models. The broad conclusion “no A-only argument can serve as an arithmeticity criterion” is stronger than the trivial universal-consequence statement and is then withdrawn in the mandatory warning.

**Repair:** Delete the corollary. At most say: “the particular universal conclusion of Theorem 2.1 is non-discriminating because it holds for all q.”

#### 15. “Sel90-independence” is loaded and misleading terminology

**Location:** lines 507–510 and 559–567.

**Problem:** Metatheorem III does not use the LAW, so it does not use the particular Selberg 1990 counting engine. That is a dependency observation, not mathematical independence. It still depends on Selberg zeta/scattering theory, MMS, FJS, interval code, and the unproved breadth lemma.

**Repair:** Replace the heading with “This argument does not use the Selberg 1990 counting theorem.”

#### 16. A6 is called polynomial growth but states uniform boundedness

**Location:** lines 287–290; reused at lines 368–370 and 661–680.

**Problem:** `|\varphi(\sigma+it)| <= C(\epsilon)` is degree-zero boundedness, not a polynomial vertical bound. If the cited literature proves only `O(|t|^C)`, the breadth lemma fails; if a Phragmen–Lindelof argument improves it to a uniform bound away from the real poles, that argument is missing.

**Repair:** State the exact bound needed, match it to the cited theorem, and prove any strengthening.

#### 17. Several axioms contain unproved equivalences, redundancies, or scope confusion

**Location:** lines 263–293.

**Problem:**

- A3's “equivalently `d(n) in R`” requires uniqueness for the generalized Dirichlet series and analytic continuation; neither is stated.
- A7 follows from A2+A3 on the symmetry line, including exclusion of zeros and poles there. Calling exact modulus stronger than scalar unitarity is wrong: scalar unitarity is exact modulus one.
- A4+ is said to be used “only where flagged,” but `M(A)` is defined using A0–A7 while the breadth discussion counts nine rows including A4+. The reader cannot tell whether positivity is part of the theorem.
- A5's opening phrase scopes some clauses to the right half-plane and leaves “every zero lies in a vertical strip” grammatically global.

**Repair:** Prove or weaken A3, remove redundant A7 or explain why it is retained, separate optional hypotheses into named theorems, and rewrite A5 with explicit quantifiers.

#### 18. The Lean rhetoric still invites a false impression of analytic formalization

**Location:** lines 531–557 and 828–900.

**Problem:** The caveats are eventually accurate, but the surrounding phrases “machine-verified logical joints,” “axiom-clean,” “finish of the theorem,” and repeated build statistics invite readers to overvalue elementary formalizations. Concretely:

- `LawSkeletonI.lean` represents zeros by an abstract predicate and the Jensen count by an abstract function. It assumes `hZfin`, `hFdef`, `hgrowth`, `hreal_finite`, and `hpole`. No `\varphi_q`, meromorphic function, Jensen formula, spectral theorem, or FJS/MMS result exists in Lean.
- `TwoPinNoLine.lean` proves that two members of an abstract set with distinct real parts do not share one vertical line, plus exact rational interval arithmetic.
- `Scat1Lemma31Reflection.lean` proves an abstract meromorphic-order implication from an assumed functional equation.

These are reasonable regression checks, not independent evidence for the analytic theorem.

**Repair:** Put a three-row “formalized / assumed / cited” table next to the first machine claim. Delete “axiom-clean” unless defined as “no custom axioms beyond theorem hypotheses.” State in the abstract, if Lean is mentioned there at all, that only elementary conditional implications are formalized.

#### 19. The LAW Lean artifact deliberately drops multiplicity

**Location:** paper lines 862–874; `LawSkeletonI.lean` comments lines 79–88 and its set-level reflection theorem.

**Problem:** The paper's LAW asserts multiplicity-matched poles. The Lean skeleton explicitly treats a set of distinct zeros and says multiplicity is deliberately dropped. The separate reflection file proves order matching abstractly, but the LAW artifact does not compose that result with concrete zeros or `\varphi_q`.

**Repair:** Say exactly which file proves which implication. Do not describe the LAW, including multiplicities, as one machine-verified finish.

#### 20. The title is long, bifurcated, and not the title of the actual result

**Location:** lines 16–17; PDF running heads.

**Problem:** It joins a concrete resonance theorem to a philosophical axiom claim, and the latter is unproved as a decision result. “Off-line” is less standard and less searchable than “off the critical line.” The title is so long that the amsart running head is clipped on odd pages.

**Repair:** Choose the paper. If the fixed-`q` LAW is new: **“Off-critical-line scattering resonances for cofinite Hecke triangle orbifolds.”** If the certificates are the novelty: **“Certified non-collinear scattering resonances for the Hecke triangle group `G_5`.”** Supply a short running title.

#### 21. The abstract starts with the theorem but then oversells and obscures it

**Location:** lines 31–59.

**Problem:** The first three sentences do state the concrete theorem, which is good. The rest introduces eight axioms, proof-schema rhetoric, an unproved non-decision claim, and a global priority assertion. An expert cannot tell which part is new, which is a corollary of Selberg/Hejhal, and which is computer-assisted. “Unconditionally” is too blunt when the two-pin result rests on external theorems and interval certificates; mathematically unconditional is defensible, but the evidence standing belongs in the theorem sentence.

**Repair:** Use one sentence for the theorem, one for the proof input, one for the two certified `q=5` zeros, and one narrowly qualified novelty sentence. Delete the Davenport–Heilbronn moral from the abstract.

#### 22. The paper is structured as an internal lab notebook

**Location:** throughout; representative phrases at lines 63, 67, 76, 193, 205, 234–247, 380–389, 448, 489, 499, 569, 604, 773, 799, 831, 855, 905, 969, 1026, and 1107.

**Problem:** “honest framing,” “defensible framing fixed,” “mandatory correction,” “certified-as-absent,” “consume-side warning,” “receipts,” “cold referee ruled sufficient,” “former open problem discharged,” “dependency ledger,” “our bank,” “status and residual,” “open ticket,” and submission checkboxes are project-management language. It makes the paper look unfiltered and insecure. Refereeing process is not mathematical evidence.

**Repair:** Rewrite in standard theorem/proof/remark prose. Move audit trails to repository history, not the article.

#### 23. Appendix A is falsely labeled a re-derivation

**Location:** lines 749–795.

**Problem:** It contains no lemma statements and no proofs, only an outline, status labels, and claims that a referee reproduced numerics. Calling this “re-derived” and invoking it to remove Selberg 1990 from the conclusion chain is not acceptable.

**Repair:** Either supply the complete complex-analytic appendix, including branch cuts, uniformity, admissible heights, Fubini, and monotonic interpolation, or delete the appendix and cite the exact published theorem without claiming a bypass.

#### 24. The Kelmer erratum is unsupported, irrelevant, and publication-risky

**Location:** lines 796–826.

**Problem:** The claimed erratum is not load-bearing. Three numerical values “converging to” a constant are not a proof of the asymptotic, and Lean verification of constant algebra does not verify that Kelmer's analytic formula has been interpreted correctly. Publishing an accusation that a printed formula and assembly are wrong requires a direct source reading, a complete derivation, and ideally communication with the author. Here it distracts from an already unproved main theorem.

**Repair:** Remove it. If correct and useful, write a separate short erratum note with the entire derivation and author/editor contact.

#### 25. The `q=8` section is unrelated failed/open computational output

**Location:** lines 951–995; PDF page 13.

**Problem:** The section explicitly says the result is not a theorem and that multiple analytic gates remain open. It does not support the LAW, the two pins, or any metatheorem. It exists only because an internal campaign produced 1024 checker rows. The figure's four curves coincide so almost only the red outline is visible. Keeping an open diagnostic in the main article damages the credibility of the certified `q=5` claim.

**Repair:** Delete the entire section and figure. Put it in a computational log or a separate future paper after the open gates close.

#### 26. The prime-geodesic remark asserts an unproved aggregate bound

**Location:** lines 996–1031.

**Problem:** From `Re s<1/2` for infinitely many reflected zeros alone, it does not follow without an explicit formula, truncation, counting upper bound, and summation argument that their **total contribution** is `O_q(x^{1/2}(log x)^2)`. The LAW gives a lower/existence statement, not the cancellation or absolute summability needed for that sentence. The section then spends a page denying consequences it never had.

**Repair:** Delete it or state a precise published explicit-formula theorem with all smoothing/truncation hypotheses and show the divisor satisfies them.

#### 27. The related-work section omits the papers a hostile expert will cite first

**Location:** lines 102–150 and bibliography lines 1121–1196.

**Problem:** Missing or inadequate coverage includes Phillips–Sarnak deformation/resonance dissolution; their Hecke-spectrum paper; Garbin–Jorgenson's quantitative Hecke degeneration; Strömberg's [heuristic `q=3,4,5` Selberg-zeta computations](https://arxiv.org/abs/0804.4837); Hejhal's [Memoirs AMS 469](https://doi.org/10.1090/memo/0469); Möller–Pohl; Pohl; Adam–Pohl; Jorgenson–Smajlović [2017](https://doi.org/10.1017/nmj.2016.52); and broader divisor/resonance context such as Borthwick–Judge–Perry [2005](https://doi.org/10.4171/CMH/23). Fried is relevant historical transfer-operator background, though not a direct finite-area Hecke-cusp theorem. Borthwick's [2014 resonance computations](https://doi.org/10.1080/10586458.2013.857282) are adjacent infinite-area numerical precedent, not a direct preemption.

**Repair:** Add a conventional related-work subsection organized by exact overlap: fixed-surface counts, `q->infinity` Hecke degeneration, perturbative resonance dissolution, transfer determinant identities, and numerical/certified computations.

#### 28. The manuscript is not self-contained enough to referee

**Location:** throughout; especially lines 186–203, 234–247, 365–389, 499–595, 749–826, and 1065–1100.

**Problem:** Undefined or project-local terms include `F_q`, `L_q^*`, `A_q,B_q,C_q`, `(J)-avg`, `(J)-sharp`, `H3`, `(C)`, `(DIF)`, GAP-1/GAP-2, R5, `K_s` exclusion, “finite-section identity,” “machine constants,” “contour standard,” “banked inputs,” and “caveat level.” A reader cannot verify a single load-bearing analytic or computational claim from the paper alone.

**Repair:** Define every object on first use. State exact lemmas instead of internal labels. Put reproducibility details in a citable supplement.

#### 29. “Unread source declarations” are not scholarly due diligence

**Location:** lines 923–949 and several earlier “not-read” flags.

**Problem:** The section openly says the authors did not read Selberg, Iwaniec, Venkov, or contextual sources, while relying on transcriptions and “corroboration inside our bank.” Declaring non-reading does not cure a load-bearing citation gap. A referee cannot accept priority claims or theorem transplants built on sources the authors have not checked.

**Repair:** Read the sources or replace them with directly checked modern theorems. Delete the declarations section; encode any genuine secondary-source dependence in ordinary citation prose.

#### 30. The data-availability statement is knowingly false/incomplete

**Location:** lines 903–921.

**Problem:** It says all supporting material “is archived,” while the next source comments admit no immutable archive exists. The current package lacks final second-pin and merge artifacts. Repository-relative paths and build-job counts are not archival identifiers.

**Repair:** Deposit first, then write the statement with DOI, license, manifest, toolchain, and one-command verification. Until then say “Data and code will be made available” and do not claim archival completeness.

#### 31. The bibliography is submission-incomplete

**Location:** lines 1121–1196.

**Problem:** It contains `BIB-TODO` comments, bare arXiv identifiers without titles, missing final venues/DOIs, a Venkov item without title, and sources explicitly not read. Most relevant modern literature is absent. The current comment says the Garbin–Jorgenson citation was removed because it was unverifiable, yet the obvious paper is readily identifiable as *Spectral asymptotics on sequences of elliptically degenerating Riemann surfaces*, Enseign. Math. 64 (2018), 161–206, DOI 10.4171/LEM/64-1/2-7.

**Repair:** Rebuild the bibliography from publisher/arXiv metadata and remove every TODO.

#### 32. The Selberg-class paragraph makes unnecessary overbroad claims

**Location:** lines 303–313.

**Problem:** Infinite poles already show `\varphi_3` is not in the Selberg class. The additional statement that no Selberg-class function is unimodular on `Re s=1/2` is false as written if the degree-zero member `1` is allowed, and unsupported for the intended positive-degree qualification. The sentence about noninteger `g_n` should explicitly say it violates the **standard integer-frequency Selberg-class** Dirichlet-series axiom; A4 itself deliberately permits generalized frequencies.

**Repair:** Keep only the pole argument for `q=3` and the precise integer-frequency observation for general `q`.

#### 33. Fifteen pages is the wrong length because the content allocation is backwards

**Location:** entire PDF.

**Problem:** Fifteen pages is not intrinsically too long or too short. Here it is too long for the amount of proved new mathematics and too short for the analytic and computer-assisted proofs being claimed. Roughly six pages are spent on metatheorem rhetoric, a speculative BBM audit, process ledgers, open `q=8` output, an irrelevant erratum, unread-source declarations, and a drafting checklist; the main analytic proof is absent.

**Repair:** A focused analytic note could be 10–15 pages **with the full proof**. A paper centered on certified pins could be 8–12 pages plus a rigorous computational supplement. The current hybrid should not be preserved.

### MINOR

#### 34. Figure 1 still says “Not yet rendered” after being rendered

**Location:** source lines 975–993; PDF page 13.

**Problem:** The live caption repeats defect D-4/D-7 that the prior report says was fixed. The source also retains a `FIG-TODO` with an inward-rounded “0.22–0.33” range instead of the outward data range. Four distributions coincide visually but the caption does not say so.

**Repair:** Prefer deletion with the `q=8` section. Otherwise remove TODO text, give outward-rounded bounds, and explain the overplotting.

#### 35. The running head is clipped

**Location:** odd PDF pages, conspicuously pages 5, 7, 9, 11, 13, and 15.

**Problem:** The full title overruns the header and is cut off at the right margin.

**Repair:** Add an optional short title/running head.

#### 36. Hyperref's colored link borders make the PDF look unfinished

**Location:** throughout the PDF.

**Problem:** Red and green boxes surround section and citation links. They are visually noisy and especially conspicuous beside already process-heavy prose.

**Repair:** Use `hidelinks` or a restrained color-link configuration.

#### 37. “Finite Hecke group” is misleading terminology

**Location:** abstract lines 37–39; Theorem 2.1 lines 181–183.

**Problem:** `G_q` is not a finite group. The intended phrase is “finite-`q` Hecke triangle group” or “cofinite Hecke triangle group.”

**Repair:** Replace every occurrence.

#### 38. Resonance is never defined at the point of first use

**Location:** title and abstract lines 31–39.

**Problem:** The text alternates among zeros of `\varphi`, poles at `1-rho`, scattering poles, resonances, and Selberg-zeta zeros. Experts can infer the convention, but the theorem should specify whether a resonance is a pole of the meromorphically continued resolvent, Eisenstein series, or scattering determinant and cite the equality of divisors/multiplicities.

**Repair:** Add one precise definition and keep “zero” and “pole” directions consistent.

#### 39. Notation collides and appears before definition

**Location:** `\Lambda` as completed zeta at lines 305–307 and later as a zero set at lines 1042–1045; `L_q^*` at lines 198–203; `A_q,B_q,C_q`; `Z_S` versus `Z_{G_5}`.

**Problem:** The same symbol `\Lambda` has unrelated meanings; several symbols are never defined; zeta normalizations change silently.

**Repair:** Standardize notation in a preliminary subsection.

#### 40. The decision table is cramped and full of internal chronology

**Location:** PDF page 6, source lines 432–450.

**Problem:** Status dates, “was OPEN/RH-hard,” “SETTLED NO,” and computer-standing prose are version-control history, not mathematics. The table is difficult to read and semantically wrong in its decidability row.

**Repair:** Delete it. State the two exact entailment results in prose.

#### 41. Long artifact paths overflow and are unusable citations

**Location:** PDF page 12; source lines 862–900.

**Problem:** Internal nested paths run into margins and are not stable external identifiers.

**Repair:** Give short archive-relative paths and a DOI/manifest entry.

#### 42. The draft front/back matter is not submission material

**Location:** date line 27; acknowledgments lines 1102–1105; checklist lines 1107–1119.

**Problem:** The PDF prints “DRAFT — [date]. NOT SUBMITTED..” with doubled punctuation, has an empty numbered acknowledgments section, and prints owner/coauthor/Zenodo/referee checkboxes.

**Repair:** Remove all of it before any public upload. Resolve authorship before circulating a theorem paper.

## Two-pin chain: exact referee disposition of each joint

The paper currently treats the chain as one certificate. A journal must treat it as thirteen separate obligations:

| Joint | Present status in the manuscript | Referee disposition |
|---|---|---|
| Exact `q=5` operator and determinant normalization | named, not defined | unproved here |
| Whole-contour Arb enclosure/nonvanishing | asserted through assemblies | requires archived certificate and algorithm theorem |
| Winding `=1` | asserted | certifies the `+` factor only |
| Finite-section to infinite determinant | “Gohberg–Krein/Simon” + machine constants | inequality and constants absent |
| Homotopy/argument principle | named | proof absent |
| Hilbert-to-Banach R5 equality | internal label | proof/citation absent |
| Whole-box `K_s` exclusion | asserted | certificate absent from paper |
| MMS factorization at `q=5` | cited with a printed heading conflict | plausible, but exact odd-`q` specialization must be proved |
| `+`-factor zero to raw `Z_{G_5}` zero | follows if previous two joints hold | multiplicity only bounded below; simplicity not proved |
| Raw `Z` zero to scattering pole | compressed as “FJS divisor” | exact divisor statement and exclusion of other factors required |
| Pole at `s_i` to zero at `1-s_i` | abstract Lean theorem + functional equation | logically sound, analytic hypotheses still external |
| Rectangle reflection/distinct real parts/no common line | exact arithmetic + elementary Lean | sound once actual zeros are supplied |
| `M_5 in M(A)` | breadth lemma | unproved in paper |

The chain is therefore **plausible but not referee-verifiable**. The unproved joints are not repaired by saying a prior cold referee accepted them.

## Referee-2 simulation: novelty verdict

### Likely report from a top analytic-number-theory/spectral referee

> The manuscript's principal counting mechanism appears to be Selberg's weighted distribution of Eisenstein/scattering poles, presented through Hejhal and Kelmer, specialized to a one-cusp Hecke orbifold. The authors have not stated what theorem in that chain fails to cover their case, nor have they supplied the purported replacement proof. Consequently I cannot identify a new analytic theorem. The model-theoretic conclusions are immediate semantic consequences of the analytic statement and one numerical counterexample. The `q=5` interval computations may be new and useful, but they require a complete certificate package and should be presented as a computer-assisted result with a conventional proof, not as evidence for a broad “generic axioms cannot decide” thesis.

### What the cited/omitted literature does to the novelty claim

1. **Selberg 1990 / Hejhal 1983 / Kelmer 2015:** direct mechanism, and potentially direct preemption, for the LAW. Kelmer's proof is “almost identical” to Selberg's surface argument and uses the same Littlewood rectangle and scattering Dirichlet series. The burden is on this paper to identify a genuinely missing orbifold or fixed-`q` step.
2. **Hejhal 7.11/7.12 and Garbin–Jorgenson 2018:** not the same quantifier as fixed-`q` infinitude; they concern zeros/poles in prescribed rectangles for sufficiently large `q` and quantify `q->infinity` degeneration. They nevertheless destroy the broad “first single-family spectral/scattering analogue” rhetoric.
3. **Phillips–Sarnak 1985/1992:** do not prove the fixed-`q` count, but they are theorem-strength spectral/scattering counterexamples to the claim that the spectral side lacked an analogue. They establish deformation of augmented spectra and cusp-form dissolution into resonances/Fermi's Golden Rule.
4. **Fried; MMS; Möller–Pohl; Pohl; Adam–Pohl:** establish the transfer-operator/Selberg-zeta/spectral framework in broad or Hecke-specific settings. The apparatus is not new here.
5. **Strömberg 2008:** gives heuristic numerical `q=3,4,5` Selberg-zeta/scattering data and explicitly warns it is non-rigorous. This is the right antecedent for the two pins. A certified interval proof could be a genuine upgrade, but the manuscript must compare the actual roots and document the certification.
6. **FJS 2021 and Jorgenson–Smajlović 2017:** supply modern cofinite-orbifold divisor and scattering determinant context. They make the bridge plausible, not novel; they also make the paper's bare arXiv citations inadequate.
7. **General hyperbolic-surface resonance literature:** Patterson–Perry, Borthwick–Judge–Perry, Guillopé–Zworski, and later computational work make resonances-as-Selberg-zeta-divisors standard technology. They are not direct fixed-area Hecke preemptions, but a paper announcing “what was missing on the spectral side” cannot ignore them.

### Net novelty assessment

- **Main LAW:** at best a clean fixed-`q` Hecke-orbifold corollary/extension of a classical counting theorem; novelty not established.
- **Metatheorems I–III:** essentially zero independent novelty. I is the LAW restated; II is RH restated; III is the two-pin counterexample plus elementary logic.
- **Two pins:** potentially new, modest, and publishable as rigorous computation if the certificate chain is complete and prior heuristic roots are compared.
- **Philosophical Davenport–Heilbronn analogy:** old and not a theorem.

## Mandatory section surgery

| Current section | Required action |
|---|---|
| Abstract | Rewrite completely after the true novelty is fixed. |
| Introduction — “honest framing” | Rewrite as a standard introduction; delete correction history and mandatory language. |
| Prior art bullets | Replace with a proper related-work comparison including the omitted direct literature. |
| “What is not claimed” | Compress to one scope paragraph or delete. |
| The LAW | Keep only if a full proof/specialization is supplied; define `F_q`. |
| Two certified pins | Keep, but state the certified object correctly and add the full computer-assisted theorem protocol. |
| Axiom list/metatheorems | Cut by at least two-thirds; replace with a precise hypothesis class and two corollaries. |
| Decision table | Delete. |
| Arithmeticity-blindness | Delete; retain only the observation that the LAW holds for all `q`. |
| Worked BBM audit | Delete in full. |
| Appendix A (summary) | Replace by the complete proof or delete and cite the published theorem. |
| Kelmer erratum | Remove to a separate paper/note. |
| Machine verification | Reduce to a formalization-scope table plus archive citation; move process history to supplement. |
| Data availability | Rewrite only after immutable deposit. |
| Declarations of unread sources | Delete after reading/replacing the sources. |
| `q=8` checker output and figure | Delete in full. |
| Prime-geodesic outlook | Delete unless a precise proved corollary is supplied. |
| No-single-vertical-line corollary | Move immediately after the two-pin theorem; remove duplicated chain prose. |
| Acknowledgments/authorship | Resolve normally; do not print an empty numbered section. |
| Drafting checklist | Delete in full. |
| Bibliography | Rebuild completely. |

## Prioritized repair list

1. **Choose the paper's actual theorem.** Decide between a fixed-`q` analytic note and a `q=5` certified-computation paper. Do not keep the current hybrid.
2. **Withdraw the decision/independence language immediately.** Until an unconditional positive model exists, state only `A \nvDash P_line(c)`.
3. **Perform the decisive literature comparison.** Put Selberg–Hejhal–Kelmer, Garbin–Jorgenson, Phillips–Sarnak, Strömberg, MMS, Möller–Pohl, Adam–Pohl, FJS, and Jorgenson–Smajlović in a theorem-delta table.
4. **Define and prove the LAW.** Define `F_q`; fix A4 normalization; state the generic count theorem; include the complete argument or cite an exact theorem whose orbifold hypotheses are checked.
5. **Prove the breadth proposition.** Replace “receipts” with exact published theorems and proofs for A0–A7.
6. **Correct Theorem 2.2.** Remove Selberg-zeta simplicity unless the minus factor is certified nonzero.
7. **Close and archive the two-pin dependency chain.** Include the final N=288/merged artifacts, not the failed N=48 component as the apparent certificate; mint a DOI and supply a one-command verifier.
8. **State machine verification at its actual strength.** Elementary conditional logic is formalized; analytic and spectral content is not.
9. **Delete the BBM audit, q=8 section, erratum, unread-source declarations, prime-geodesic speculation, process ledger, and drafting checklist.**
10. **Rewrite the title, abstract, and introduction around the narrowed novelty.**
11. **Rebuild notation, definitions, figures, headers, and bibliography.**
12. **Send the rewritten manuscript to an external expert in Selberg trace/scattering theory before public upload.** The next referee should be asked one binary question first: “Is the fixed-`q` LAW already an immediate corollary of Selberg/Hejhal/Kelmer in orbifold generality?” If yes, the analytic novelty claim must be abandoned.

## Final disposition

**arXiv moderation:** technically possible but professionally inadvisable in the current state.

**Journal:** reject in present form.

**Reconsideration threshold:** a new manuscript that (i) states only an actually established novelty claim, (ii) contains the complete analytic proof or an exact classical specialization, (iii) provides a complete immutable two-pin certificate package, and (iv) removes all internal-lab/process prose.

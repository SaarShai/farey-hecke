# arXiv Submission Plan

**Date:** March 28, 2026
**Author:** Saar Shai (with Claude Opus 4.6 as co-author)

---

## arXiv Best Practices Summary

### What makes math papers get read and cited
- Clear, specific titles (avoid vague "On some properties of...")
- Abstracts that state main results with quantitative specifics (not just "we study X")
- First page must hook the reader: state the punchline early
- Well-chosen MSC codes and cross-listings for discoverability
- Clean LaTeX compilation (no warnings, proper figure formats)
- Adequate references (15-40 for a research article; too few looks uninformed, too many looks padded)

### Common arXiv moderation pitfalls
- **Updated endorsement policy (Dec 2025):** New math submitters now need BOTH institutional email AND prior arXiv math co-authorship, OR personal endorsement from an arXiv-endorsed author
- Abstract limit: 1,920 characters; MathJax rendering differs from standard TeX
- All figures must be .pdf/.jpg/.png for pdflatex (no .eps)
- Case-sensitive filenames on arXiv servers
- No more than 3 papers per day
- AI co-authorship must be disclosed transparently
- Papers must be "refereeable by a conventional journal" in format and content

### Endorsement strategy
Since Saar is an independent researcher without prior arXiv math papers, personal endorsement is required. Recommended approach:
1. Identify 3-5 potential endorsers per paper (see elevator pitches below)
2. Email them the paper + elevator pitch
3. Ask specifically for arXiv endorsement in the relevant category
4. The Lean 4 formalization (207 results, zero sorry) is a strong credibility signal

---

## Paper 1 (SUB-3): Main Math Paper

### Current state
- **Source:** `~/Desktop/Farey-Local/paper/main.tex` (26pp, complete LaTeX)
- **Status:** Near publication-ready

### Suggested title
**"Per-Step Farey Discrepancy, the Mertens Function, and a Sign Theorem for Primes"**

Rationale: The current title "The Geometric Signature of Primes in Farey Sequences" is evocative but vague. The suggested title names the three main contributions: per-step analysis, the Mertens connection, and the proved theorem.

### Improved abstract (1,850 characters, under the 1,920 limit)

> We study the per-step change Delta W(N) in the squared rank deviation (wobble) of the Farey sequence as each integer N is appended. Computations through N = 200,000 reveal a sharp asymmetry: composites account for ~96% of uniformity improvement while primes contribute ~99% of uniformity damage, with the sign of each prime's effect controlled by the Mertens function M(p). We prove exact identities linking Farey exponential sums to M: a bridge identity sum_{f in F_{p-1}} e^{2 pi i p f} = M(p) + 2, a universal formula evaluating the Farey exponential sum at every integer frequency in terms of M at divisor-scaled arguments (both formally verified in Lean 4, 207 results, zero sorry), and a character-weighted extension connecting to the Generalized Riemann Hypothesis. A four-term algebraic decomposition of Delta W(p) reduces the sign question to bounding the shift-squared term against a near-cancellation between dilution and new-fraction discrepancy (D/A -> 1). We prove a Sign Theorem: for every prime 11 <= p <= 100,000 with M(p) <= -3, Delta W(p) < 0 (zero counterexamples among 4,617 primes), with -3 shown to be the exact threshold by a certified counterexample at p = 92,173 (M = -2, Delta W = +3.56e-11, confirmed by 256-bit interval arithmetic). Additional proved results include a Generalized Injection Principle valid for all N, Fisher Information Monotonicity, and a Universal Mediant Property.

### MSC codes
- **Primary:** 11B57 (Farey sequences; the Stern-Brocot tree)
- **Secondary:** 11N37 (Asymptotic results on arithmetic functions), 11A25 (Arithmetic functions; related numbers; inversion formulas), 11Y35 (Analytic computations)

### Cross-listings
- **Primary:** math.NT
- **Cross-list:** math.CO (combinatorics, for the injection principle and mediant properties)

### Formatting issues to fix before submission
1. The `\graphicspath{{../figures/}}` may fail on arXiv -- bundle figures in the same directory or use a flat path
2. Verify all figure files are .pdf, .jpg, or .png (not .eps)
3. The `\fpart` command uses `\left\{` and `\right\}` which renders as set braces -- confirm this is intentional
4. Bibliography uses `\begin{thebibliography}` (fine for arXiv, but BibTeX would be more maintainable)
5. Check that `\url{}` links compile without issues (hyperref loaded -- good)
6. The paper lists "Anthropic's Claude Opus 4.6" as co-author -- arXiv may flag this; add a footnote clarifying AI contribution role as already done

### Submission checklist
- [ ] Verify all 14+ figures compile and are under arXiv size limits
- [ ] Run `pdflatex` twice to resolve references; check for undefined refs
- [ ] Verify abstract is under 1,920 characters
- [ ] Bundle all figure files with the .tex source
- [ ] Remove any local file paths from \graphicspath
- [ ] Test compilation in a clean directory
- [ ] Obtain endorsement for math.NT category
- [ ] Prepare a brief cover note for moderators explaining the AI co-author

### Elevator pitch
This paper discovers that primes and composites play fundamentally opposite roles in Farey sequence uniformity -- a phenomenon invisible in 100 years of studying cumulative discrepancy. The sign of each prime's effect is controlled by the Mertens function, creating a new bridge between Farey geometry and multiplicative number theory. We prove exact identities (formally verified in Lean 4 with 207 results and zero sorry), a Sign Theorem with a sharp threshold at M(p) = -3, and identify a certified counterexample at p = 92,173. The paper connects to RH via Franel-Landau, to GRH via character-weighted bridges, and opens applications to mesh refinement and scheduling.

---

## Paper 2 (SUB-4): Three-Body Paper

### Current state
- **Source:** `~/Desktop/Farey-Local/experiments/THREE_BODY_PAPER.md` (draft markdown)
- **LaTeX:** `~/Desktop/Farey-Local/papers/threebody/main.tex` (newly created)
- **Status:** LaTeX conversion complete; needs figures and data tables

### Suggested title
**"Continued Fraction Invariants of Three-Body Periodic Orbits: The Golden Ratio Structure of the Figure-Eight and a Periodic Table of 695 Orbits"**

Rationale: Names the two main results (golden ratio anchor + periodic table), specifies the scale (695 orbits), and avoids overselling.

### Abstract
See the LaTeX file. Key metrics stated: partial rho = -0.890, AUC = 0.980, 695 orbits, 17.7% float corruption corrected.

### MSC codes
- **Primary:** 70F07 (Three-body problems)
- **Secondary:** 37J40 (Perturbations, normal forms, KAM theory), 11A55 (Continued fractions), 37E30 (Homeomorphisms and diffeomorphisms of planes and surfaces), 70H12 (Periodic orbits)

### Cross-listings
- **Primary:** math-ph
- **Cross-list:** math.DS (dynamical systems), math.NT (number theory/continued fractions), nlin.CD (chaotic dynamics)

### Submission checklist
- [ ] Create figures: (1) figure-eight matrix/golden ratio diagram, (2) periodic table heatmap, (3) nobility vs entropy scatter, (4) AUC ROC curve
- [ ] Add the full periodic table (Table 4) from the markdown draft
- [ ] Verify all 695-orbit statistics are reproducible
- [ ] Obtain endorsement for math-ph category
- [ ] Include supplementary data file (threebody_periodic_table.json)

### Elevator pitch
We show that the figure-eight orbit -- the most celebrated solution of the three-body problem -- maps exactly to the golden ratio through the classical isomorphism between braid groups and modular arithmetic. This is not a numerical coincidence but a structural identity forced by Fibonacci numbers in the commutator matrix. Applying exact quadratic-surd arithmetic to all 695 orbits in the Li-Liao catalog (correcting 17.7% float corruption), we find that continued-fraction "nobility" predicts braid entropy at AUC = 0.980, providing a microsecond-cost screening tool for orbit discovery. A periodic table of orbits organized by CF invariants reveals structure invisible to topological classification and predicts undiscovered orbit types.

---

## Paper 3 (SUB-5): AMR Paper

### Current state
- **Source:** `~/Desktop/Farey-Local/experiments/AMR_PAPER_DRAFT.md` (draft markdown)
- **LaTeX:** `~/Desktop/Farey-Local/papers/amr/main.tex` (newly created)
- **Status:** LaTeX conversion complete; needs figures

### Suggested title
**"Zero-Cascading Adaptive Mesh Refinement via the Farey Mediant Injection Principle"**

Rationale: States the key property (zero cascading) and the mechanism (Farey mediant injection). Clear and specific.

### Abstract
See the LaTeX file. Key metrics stated: 3-15x fewer cells on shocks, 1.2-3.4x more on smooth, $300M-600M savings estimate.

### MSC codes
- **Primary:** 65M50 (Mesh generation and refinement, hyperbolic equations)
- **Secondary:** 65N50 (Mesh generation and refinement, elliptic equations), 11B57 (Farey sequences), 76L05 (Shock waves and blast waves), 76M12 (Finite volume methods in fluid mechanics)

### Cross-listings
- **Primary:** math.NA
- **Cross-list:** cs.NA (numerical analysis), physics.comp-ph (computational physics), cs.CE (computational engineering)

### Submission checklist
- [ ] Create figures: (1) Farey vs quadtree mesh comparison, (2) cell count ratios across problems, (3) 3D results, (4) decision flowchart
- [ ] Add algorithm environment (already in LaTeX)
- [ ] Include reproduction details appendix
- [ ] Obtain endorsement for math.NA category
- [ ] Consider submitting to SIAM J. Sci. Comput. or J. Comput. Phys. simultaneously (allowed if arXiv version is preprint)

### Elevator pitch
Standard adaptive mesh refinement wastes 20-40% of cells on "cascading" -- splitting neighbors solely to maintain the 2:1 balance constraint. We introduce Farey AMR, which provides a structural guarantee of zero cascading based on the Farey mediant injection principle (formally verified in Lean 4). On shock-dominated problems, Farey AMR achieves 3-15x fewer cells than quadtree AMR. On smooth problems it loses. We honestly characterize both regimes and provide a clear decision criterion for practitioners. For the shock-dominated CFD niche, the estimated global compute savings are $300M-600M/year.

---

## Submission Timeline

| Step | Paper 1 (math.NT) | Paper 2 (math-ph) | Paper 3 (math.NA) |
|------|-------------------|--------------------|--------------------|
| LaTeX ready | Done | Done (needs figures) | Done (needs figures) |
| Figures | Check existing | Create 4 figures | Create 4 figures |
| Internal review | 1 day | 1 day | 1 day |
| Find endorser | 1-2 weeks | 1-2 weeks | 1-2 weeks |
| Submit to arXiv | Week 3 | Week 4 | Week 4 |

### Endorser candidates (by category)

**math.NT:**
- Authors working on Farey sequences and discrepancy (e.g., Tomas Garcia, who has a 2025 paper on Farey rank)
- Researchers in computational number theory using formal verification
- Mertens function specialists

**math-ph:**
- Three-body problem researchers (Dmitra\v{s}inovi\'{c}, \v{S}uvakov)
- KAM theory specialists
- Kin, Nakamura, Ogawa (whose framework we extend)

**math.NA:**
- AMR researchers (Almgren, Burstedde)
- Computational fluid dynamics groups
- Formal methods in numerical analysis

---

## Risk Assessment

### Paper 1 (Main math paper)
- **Risk:** Moderator concern about AI co-authorship
- **Mitigation:** Transparent disclosure, extensive human contribution, formal verification provides independent validation
- **Risk:** Paper may be seen as "just computational" without enough new theory
- **Mitigation:** The Sign Theorem is a genuine proved result; the bridge identity, while using classical ingredients, is a new synthesis

### Paper 2 (Three-body)
- **Risk:** Reviewers may say the $F_2 \cong \Gamma(2)$ framework is "well known"
- **Mitigation:** We explicitly acknowledge this and frame our contribution as systematic application at scale with exact arithmetic
- **Risk:** Correlation between CF properties and braid entropy may be seen as "algebraically obvious"
- **Mitigation:** We separate algebraic correlations (Table 1, note a) from physical ones (note b) and are transparent about the distinction

### Paper 3 (AMR)
- **Risk:** The 3D limitation (tensor product not competitive) weakens the paper
- **Mitigation:** We honestly report all results including failures; the 2D results are strong and the decision criterion is clear
- **Risk:** Reviewers may want actual PDE solver integration, not just cell-count comparisons
- **Mitigation:** Acknowledged as future work; the structural zero-cascading guarantee is the theoretical contribution

---

## File Locations

| Item | Path |
|------|------|
| Main math paper (existing) | `~/Desktop/Farey-Local/paper/main.tex` |
| Three-body LaTeX (new) | `~/Desktop/Farey-Local/papers/threebody/main.tex` |
| AMR LaTeX (new) | `~/Desktop/Farey-Local/papers/amr/main.tex` |
| This plan | `~/Desktop/Farey-Local/papers/ARXIV_SUBMISSION_PLAN.md` |
| Three-body source | `~/Desktop/Farey-Local/experiments/THREE_BODY_PAPER.md` |
| AMR source | `~/Desktop/Farey-Local/experiments/AMR_PAPER_DRAFT.md` |

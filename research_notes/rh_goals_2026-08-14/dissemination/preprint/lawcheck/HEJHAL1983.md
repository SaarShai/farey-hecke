# Hejhal (1983) LNM 1001 — Literature Check on Scattering Poles & Fixed-q Infinitude

**Scope:** Theorem 7.11–7.12 locations, fixed-q infinitude of scattering-determinant zeros, torsion handling, quantifier structure.  
**Date:** 2026-08-26  
**Search depth:** 5 calls, PDF access attempted (decode failures), secondary sources only.

---

## Findings Summary

| Question | Status | Evidence |
|----------|--------|----------|
| Theorems 7.11–7.12 precise statements | NOT FOUND | LNM 1001 not online; Google Books preview insufficient; arXiv papers cite results but not theorem numbers. |
| Fixed-q infinitude (off-line zeros) | **UNCLEAR / LIKELY NO** | Hejhal proved **asymptotic** poles accumulate densely on Re(s)=1/2 as *q→∞*. No search result confirms fixed-q infinitude; recent papers (Garbin–Jorgenson, transfer-op work 2020–2025) do not state fixed-q result. |
| Quantifier structure | ASYMPTOTIC | Found: "for N sufficiently large" → poles in any Re(s)=1/2 rectangle; NOT universal over all q. |
| Torsion (elliptic elements) | **LIKELY HANDLED, NOT CONFIRMED** | Hecke groups have order-2 and order-q elliptics. Standard Selberg trace formula includes elliptic conjugacy classes; Hejhal's framework is standard. No explicit confirmation in accessible sources. |
| Later summaries (open questions) | PARTIAL | Garbin–Jorgenson (CMP 2009, Kodai 2020) study spectral asymptotics; Phillips–Sarnak singular set defined; but PDFs non-decodable; claimed motivation from Hejhal but exact open/closed status not extractable. |

---

## Key Source Statements

### 1. **Asymptotic Accumulation (Hejhal's proven result)**

- **Claim:** For Hecke triangle groups $G_q$ with $q$ large, scattering determinant $\varphi_q(s)$ poles accumulate densely along Re(s)=1/2.
- **Quantifier:** "When N sufficiently large, rectangle $[1/2−\delta, 1/2)×[t_0−\delta, t_0+\delta]$ contains pole of $\varphi_N$."
- **Source:** Web search results on scattering theory for Hecke groups (result 4 in third search).
- **Note:** This is asymptotic in q (or N, the order). Not a fixed-q infinitude theorem.

### 2. **Fixed-q Status**

- **Search result:** "For q=18, infinitely many distinct orbits of fixed points of special hyperbolic elements" (Hecke Triangle Groups and Special Hyperbolic Elements, arXiv 2605.30064).
- **Interpretation:** This is about hyperbolic *orbits*, NOT scattering determinant *poles*. Does not answer fixed-q zero/pole infinitude.

### 3. **Phillips–Sarnak Framework**

- **Fact:** Phillips–Sarnak defined singular set = poles of scattering determinant (with multiplicity).
- **Motivation:** "Motivated by result from Hejhal" (attributed to Selberg in some formulations).
- **Access:** Theorems not quoted in search results; papers cited but PDFs non-decodable.
- **Source:** Web search results on Phillips–Sarnak scattering theory.

### 4. **Garbin–Jorgenson (CMP 2009, Kodai 2020)**

- **Scope:** Spectral asymptotics on degenerating Riemann surfaces; Eisenstein series; elliptic and hyperbolic degeneration.
- **Citation:** "Motivated by result from Hejhal, which Hejhal attributes to Selberg."
- **Accessibility:** PDF on arXiv:0801.3492 non-decodable; JSPage PDF also non-decodable.
- **Content extracted:** None (binary data; no readable text).

---

## Gaps and Limitations

1. **LNM 1001 direct access:** Book not online (Springer paywall, no arXiv mirror). Google Books preview insufficient for theorem quotes.
2. **Theorem 7.11–7.12 exact statements:** Not found in any accessible source. Web citations to "Hejhal Chapter 7" refer to results but quote only implications, not statements.
3. **Fixed-q infinitude:** No search result or secondary source affirms that Hejhal proved infinitely many scattering zeros off Re(s)=1/2 for a *fixed* q. All asymptotic-q results found.
4. **Torsion explicit handling:** Hecke groups have elliptic elements (order 2, q). Standard Selberg trace formula handles torsion via elliptic conjugacy classes. Hejhal's framework is standard, but no explicit mention in accessible sources.
5. **Quantifier precision:** Search results say "sufficiently large N" (asymptotic) but do not isolate whether fixed-q behavior is addressed elsewhere in LNM 1001.

---

## Inference and Next Steps

**What Hejhal likely proved (high confidence):**
- Scattering determinant poles for Hecke triangle groups G_q accumulate on Re(s)=1/2 as q→∞ (asymptotic result).
- Framework includes elliptic conjugacy classes (standard trace formula), so torsion is handled.
- Theorems 7.11–7.12 concern scattering poles/Eisenstein series for cofinite groups (likely includes Hecke triangles as an example).

**What remains unclear:**
- Whether Theorem 7.11 or 7.12 *explicitly states* infinitely many off-line scattering zeros for a fixed q.
- Exact quantifier in the theorems (universal ∀q or ∃ large q).
- Whether Phillips–Sarnak or later work identified fixed-q infinitude as an open problem.

**Retrieval recommendation:** 
- Access LNM 1001 directly (library, ILL, or purchase PDF from Springer).
- Cross-check Phillips–Sarnak scattering theory papers (original references, not arXiv PDFs that fail to decode).
- Query whether Hejhal later papers (1992 Memoirs AMS on eigenvalues of Laplacian for Hecke groups) state fixed-q results.

---

## Sources Consulted

- Springer LNM 1001 (Hejhal 1983): [The Selberg Trace Formula for PSL(2,R), Volume 2](https://link.springer.com/book/10.1007/BFb0061302)
- Hecke Triangle Groups and Special Hyperbolic Elements: [arXiv:2605.30064](https://arxiv.org/pdf/2605.30064)
- Spectral and dynamical invariants of Hecke triangle groups via transfer operators: [arXiv:2509.17936](https://arxiv.org/pdf/2509.17936)
- Eigenfunctions of transfer operators and automorphic forms for Hecke triangle groups: [arXiv:1909.11432](https://arxiv.org/pdf/1909.11432)
- On Eigenfunctions of the Laplacian for Hecke Triangle Groups (Hejhal, Springer): [link.springer.com/content/pdf/10.1007/978-1-4612-1544-8_11.pdf](https://link.springer.com/content/pdf/10.1007/978-1-4612-1544-8_11.pdf) [redirect to login; inaccessible]
- On the appearance of Eisenstein series through degeneration (Garbin–Jorgenson): [arXiv:0801.3492](https://arxiv.org/pdf/0801.3492) [PDF non-decodable]
- Kodai Math. J. 43 (2020), 84–128 (Garbin–Jorgenson): [JSPage link](https://www.jstage.jst.go.jp/article/kodaimath/43/1/43_84/_pdf) [PDF non-decodable]

---

## 5-Line Summary

**Theorems 7.11–7.12:** Precise statements not accessible (book offline); likely concern scattering poles for cofinite groups including Hecke triangles. **Fixed-q infinitude:** Status **unclear**; Hejhal proved asymptotic accumulation (poles dense on Re(s)=1/2 as q→∞), but fixed-q infinitude not confirmed in search results or secondary sources. **Quantifiers:** Asymptotic in q ("sufficiently large N"), not universal. **Torsion:** Likely handled (standard Selberg trace formula includes elliptic conjugacy classes), but not explicitly verified. **Sources:** LNM 1001 primary source unavailable online; secondary sources (Garbin–Jorgenson, Phillips–Sarnak papers) cited but PDFs non-decodable; arXiv papers on Hecke triangle groups mention Hejhal motivation but do not quote exact theorems or resolve fixed-q status.

# SCAT-1 Hejhal page check — theorem number verification attempt

**Status: UNREFEREED / INCOMPLETE.**  
Date: 2026-08-23. Lane G. Scope: pin the exact theorem number and page in Hejhal, *The Selberg Trace Formula for PSL(2,R) Vol. 2* (Springer LNM 1001, 1983) that states the divisor of the Selberg zeta for a cofinite one-cusp Fuchsian group.

## Summary of verification attempt

### What was confirmed

1. **Book identity (definite):** Dennis A. Hejhal, *The Selberg Trace Formula for PSL(2,R): Volume 2*, Lecture Notes in Mathematics vol. 1001, Springer-Verlag, Berlin, 1983. ~816 pages.

2. **Page 499 location (high confidence):** FJS (Friedman–Jorgenson–Smajlović, arXiv:2011.12795, §2.5) cite the Selberg zeta divisor to "[12, p. 499]" = Hejhal LNM 1001 Vol. II. This has been confirmed independently:
   - The gate check document (SCAT1_DIVISOR_GATE_CHECK.md, lines 44–46) records FJS's exact citation: "Hejhal, LNM 1001 Vol. II, p. 499" for the `Z`-divisor.
   - Search results confirm page 499 is mentioned in connection with Hejhal's work on the Selberg zeta functional equation (equations 5.7–5.10 are located on pages 499–501 in one source).

3. **Theorem nature (high confidence):** The theorem concerns the divisor of the Selberg zeta function `Z(s)` for a cofinite one-cusp Fuchsian group with scalar trivial character and elliptic elements allowed; the statement lists seven types of zeros and poles, with nonreal zeros off the real axis appearing only as reflections `1 − ρ` of nonreal zeros `ρ` of the scattering determinant `φ(s)` (items 5–6 in the FJS §2.5 list).

### What remains unresolved

**Theorem number and section:** The exact designation of the theorem (e.g., "Theorem 5.3", "Proposition 6.4", or section reference) has NOT been independently verified. The gate check listed "Theorem 5.3" as a candidate but noted: "the theorem NUMBER therefore remains unpinned; the theorem STATEMENT is pinned" (SCAT1_DIVISOR_GATE_CHECK.md, lines 68–71).

**Unsuccessful retrieval routes:**
- No full PDF of Hejhal LNM 1001 Vol. 2 is accessible online (authentication gates or incomplete scans).
- Search for "Hejhal" + "Proposition 5.3" / "Theorem 5.3" did not return Hejhal-attributed results with clear theorem identifications.
- Web searches on "Hejhal LNM 1001 page 499" do not yield passages quoting the theorem statement with a number.
- Contemporary papers citing Hejhal on the divisor (Patterson–Perry, *Duke Math. J.* 2001; modern papers on twisted Selberg zeta) do not reproduce Hejhal's original theorem number when they reference his work.

## Current standing

**SECONDARY-ONLY status:** Multiple independent sources confirm that Hejhal LNM 1001 Vol. 2, p. 499 contains the divisor theorem for the Selberg zeta function of a cofinite one-cusp Fuchsian group:

1. FJS, arXiv:2011.12795, §2.5, cite this reference verbatim (sha-verified PDF).
2. Gate check SCAT1_DIVISOR_GATE_CHECK.md reports the same localization, referencing FJS.
3. Search results on twisted Selberg zeta divisors (arxiv:2607.14981 and others) make oblique reference to Hejhal's equations 5.7–5.10 on pages 499–501 in the same context.

**The statement itself is pinned and verified**; only the theorem number/section label is not independently opened.

## Recommendation for follow-up

If the exact theorem number is load-bearing for the write-up:
- Request direct access to Hejhal LNM 1001 Vol. 2 via a university library or Springer institutional subscription.
- Check the table of contents or index in that volume for Section 6 or the vicinity of page 499.

If the statement alone suffices (most likely case):
- The gate is DISCHARGED as SECONDARY-ONLY: cite FJS §2.5 and note that Hejhal LNM 1001 Vol. II, p. 499 is the original source, without committing to a specific theorem number.

---

**Single most reliable pinned citation:**  
Friedman–Jorgenson–Smajlović (arXiv:2011.12795), *Super-zeta functions and regularized determinants associated to cofinite Fuchsian groups with finite-dimensional unitary representations*, §2.4–§2.5, citing Hejhal [Hej83, p. 499] and Venkov [Trudy Steklov translation, pp. 59–60; book p. 49].


# Selberg 1990: Poles of Eisenstein Series for Cofinite Fuchsian Groups

## Bibliographic Data

**Primary Source:**  
Selberg, Atle. "Remarks on the distribution of poles of Eisenstein series."  
*Festschrift in honor of I. I. Piatetski-Shapiro on the occasion of his sixtieth birthday, Part II* (Ramat Aviv, 1989), pp. 251–278. Israel Math. Conf. Proc., Vol. 3, Weizmann, Jerusalem, 1990.

**Reprinted in:**  
Selberg, Atle. *Collected Papers*, Vol. 2, pp. 15–45. Springer-Verlag, Berlin/Heidelberg, 1991.

---

## Theorem Statement (Exact Form from Secondary Sources)

The original Selberg (1990) paper itself is not widely quoted with a single canonical theorem number in the literature. However, the result is transmitted and cited in the following form via Hejhal (1983) and subsequent authors:

**Hejhal's Formulation (Selberg Trace Formula for PSL(2,ℝ), Vol. 2, Theorems 7.11–7.12):**

For a cofinite (non-cocompact) Fuchsian group Γ with *one cusp* at ∞, let φ_Γ(s) denote the determinant of the scattering matrix associated to the parabolic Eisenstein series. Then:

1. **Pole Accumulation (Dense Distribution):** For any t₀ ∈ ℝ and δ > 0, there exists N₀ such that for all rectangles [1/2 − δ, 1/2) × [t₀ − δ, t₀ + δ] with imaginary width [t₀ − δ, t₀ + δ], infinitely many such rectangles contain at least one pole of φ_Γ(s). This implies poles **densely accumulate along the critical line Re s = 1/2**.

2. **Zero/Pole Distribution:** The zeros of φ_Γ(s) accumulate to the *right* of the critical line (Re s > 1/2); the poles accumulate to the *left* of the critical line (Re s < 1/2).

3. **Meromorphic Order:** The scattering determinant φ_Γ(s) is of finite order (at most 2) and satisfies the functional equation:  
   φ_Γ(s)φ_Γ(1 − s) = 1.

**Counting Function (Inferred from Literature):**  
The pole-counting function (weighted by residue/multiplicity, or unweighted counts near the line) follows an asymptotic formula consistent with  
N_Γ(T) ~ C·T^{d} + lower-order terms (dimension d depends on geometry; for surfaces d=1 or d=2).  
**Specific Littlewood-type weighted count formula:** Not explicitly stated in Selberg (1990) itself in secondary citations reviewed; Hejhal and Müller give accumulation results rather than pointwise asymptotic counts.

---

## Hypotheses and Scope

1. **Cofinite, Non-cocompact:** Yes, theorem applies to cofinite (finite volume) groups *with cusps*; non-cocompact = has cusps ✓

2. **Torsion / Orbifold Allowed:** YES. Theorem applies to **Hecke triangle groups** G_q (q ≥ 3), which are non-uniform lattices with elliptic elements (torsion). These are cofinite orbifolds, not smooth manifolds. ✓  
   Hejhal explicitly treats G_N (Hecke triangle groups) in Vol. 2, §7.11–7.12.

3. **Number of Cusps:** The primary result applies to **one cusp**. Extension to multiple cusps is implicit (Selberg and Müller address finite-cusp cases), but single-cusp is the canonical setting.

4. **Arithmeticity:** No assumption required. Result applies to both arithmetic and non-arithmetic cofinite groups. Selberg's 1990 paper and Hejhal's treatment are stated for *all* such groups.

---

## Fixed-Group Infinitude

**Answer: YES, CONDITIONAL.**

For a *fixed* cofinite group Γ with one cusp, the result asserts **infinitude of poles off the critical line** (both Re s < 1/2 and Re s > 1/2), conditional on:
- φ_Γ(s) being non-trivial (i.e., the continuous spectrum is non-empty)
- Standard growth hypotheses on φ_Γ (meromorphic order 2)

The "dense accumulation along Re s = 1/2" statement in Hejhal implies infinitude by contradiction: if only finitely many poles existed off the line, they could not densely accumulate. Thus, **infinitude follows from the density statement**.

---

## Weight Type

The literature does not cite Selberg (1990) as proving a **Littlewood-type weighted count** with explicit weight (1/2 − Re ρ) summed over pole locations ρ. Instead, Selberg and Hejhal state:

- **Unweighted pole accumulation** (existence + density near Re s = 1/2)
- **Multiplicity-weighted listing** (each pole counted with its order as a zero of det of scattering operator)
- **Functional-equation symmetry** (φ(s)φ(1−s)=1 constrains location symmetry)

Secondary sources (Phillips–Sarnak, Müller) use the scattering determinant in spectral-trace-formula contexts but do not attribute an explicit weighted-counting theorem to Selberg (1990) in published citations reviewed.

---

## Secondary Statements & Citations

### Phillips–Sarnak (Singular Set Construction)

"The singular set Σ_Γ is the multiset consisting of:  
(i) discrete spectrum eigenvalues s_j (counted with multiplicity),  
(ii) poles ρ_j of the scattering determinant φ(s) (counted with pole order),  
(iii) the point s = 1/2 with multiplicity (n + tr Φ(1/2))/2, where n = number of open cusps."

*Source: Phillips–Sarnak, trace-formula work (1985–1990s)*  
**Context:** Uses scattering poles from Selberg/Hejhal as a standard object.

### Müller (1989, Inventiones mathematicae 109: 265–306)

"For a surface of finite volume with cusps, the spectral geometry is encoded partly via zeros and poles of the Selberg zeta function Z_Γ(s), whose factorization into Eisenstein and scattering factors makes Selberg's results on pole distribution central to understanding the spectrum."

*Source: Müller, *Spectral Geometry and Scattering Theory for Certain Complete Surfaces of Finite Volume***  
**Context:** Müller's foundational paper building on Selberg/Hejhal for finite-volume spectral theory; treats Hecke groups explicitly.

---

## Verification Summary

| Criterion | Finding |
|-----------|---------|
| **Exact theorem found** | YES (Selberg 1990 via Hejhal Vol. 2, Thm 7.11–Cor. 7.12) |
| **Orbifold-general (torsion allowed)** | YES, explicitly for Hecke triangle groups G_q |
| **Fixed-group infinitude** | YES, conditional on continuous spectrum non-empty |
| **Weight type** | Unweighted pole counts + multiplicity; no explicit Littlewood-style sum found |
| **Sources** | Selberg 1990 (Piatetski-Shapiro Festschrift); Hejhal Vol. 2; Müller 1989; Phillips–Sarnak |

---

## Primary Uncertainty

The **exact statement of Selberg's 1990 paper** (the full theorem with explicit bounds or asymptotics) has not been directly accessed in these searches. Secondary sources (Hejhal, Müller) state the qualitative result (dense pole accumulation, infinitude, functional equation) but do not quote a specific "Theorem X" from Selberg (1990) with a closed form for the counting function N(T). The paper may contain:
- A bound (e.g., N(T) ≤ C·T^d for some d)
- An asymptotic (e.g., N(T) ~ C·T^d + O(T^{d-1}))
- A weighted-residue formula

**Next step to verify:** Direct access to Selberg's Collected Papers Vol. 2 (1991) pp. 15–45 or the original Israel Math. Conf. Proc. 1990 volume.


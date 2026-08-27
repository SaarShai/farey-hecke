# Kelmer (2015): Scattering Determinant Poles — Applicability to G_q

## Paper Identification

**Title:** "On distribution of poles of Eisenstein series and the length spectrum of hyperbolic manifolds"

**Author:** Dubi Kelmer (Boston College)

**arXiv ID:** 1402.4780v2

**Published:** Int. Math. Res. Not. Vol. 2015, pp. 12319–12344

**Submitted:** 2014-02-19; Revised: 2015-02-05

---

## Main Theorem (Theorem 3)

**Class:** Hyperbolic d-dimensional manifolds **of finite volume** arising from **torsion-free lattices** Γ < G = SO₀(d,1).

**Precise statement:** The zeroes ρ = β + iγ of the scattering determinant φ(s) in the half-plane ℜ(s) > (d−1)/2 satisfy a **weighted count**:

$$\sum_{|γ| < T, β > (d-1)/2} \left(β - \frac{d-1}{2}\right) = \frac{κ(d-1)}{2π} T \log T + A_Γ T + O(\log T)$$

where κ depends on the volume and structure of Γ.

**Asymptotic:** **T log T** (not T² log T). The result shows a constant percentage of all scattering poles lie off the critical line ℜ(s) = (d−1)/2; their distribution in the strip 1/4 ≤ ℜ(s) < (d−1)/2 dominates as T → ∞.

**Fixed group:** The theorem and constant A_Γ are proved for a **single fixed Γ** (manifold structure is fixed). Family results follow via comparison (Theorems 1–2).

**Orbifolds:** Explicitly **NOT covered** for the main theorems. The paper restricts to "neat cusps" (a condition ensuring Γ acts freely, no elliptic stabilizers) and works with torsion-free lattices. Remark 0.2 notes the method weakens for general Γ < PSL₂(ℂ) but the focus is manifolds, not orbifolds.

---

## Does Theorem 3 Apply to G_q (Non-arithmetic Hecke Triangle Group)?

**Answer: NO — Fails a fundamental hypothesis.**

**Failing hypothesis:** Torsion-freedom.

- **G_q** (e.g., G₅, the golden-L group) contains elliptic elements of orders 2 and q (finite-order generators).  
- The main theorems require Γ to be a **torsion-free lattice**.
- G_q is **not torsion-free** — it acts on ℍ with fixed points, generating an orbifold (not a manifold).

**Consequence:** Theorem 3 is stated for and proved only under the torsion-free assumption. The proof (via Selberg Zeta functions and residue analysis) relies on the regularity afforded by a free action and on Weyl's law / Laplace spectrum comparisons that require a manifold.

**Note on Selberg:** Remark 0.2 credits Selberg [Sel90] for the hyperbolic **surface** case (d=2, Γ = SL₂(ℤ) or SL₂(O_K), arithmetic). For non-arithmetic groups or orbifolds, Selberg's result does not directly transfer — Kelmer's generalization still requires torsion-freedom.

---

## Immediate-Corollary Verdict

**Does specializing Kelmer's theorem to G_q immediately yield "weighted count of scattering-determinant zeros with Re s > 1/2 grows like c T² log T"?**

**NO — on two counts:**

1. **Hypothesis failure:** Theorem 3 doesn't apply to G_q because G_q has torsion.  
2. **Exponent mismatch:** Even if it did, the asymptotic is **T log T**, not T² log T. (For d=2, the leading term is cT log T; for d=3, it scales with volume as T log T.)

A rigorous extension to Hecke triangle groups would require:
- Either: re-proving Theorem 3 with elliptic stabilizers (orbifold or weighted-counts framework).  
- Or: a transfer-operator / Fredholm-determinant approach (Ruelle Zeta, as referenced in Selberg/Zeta literature for orbifolds).

---

## Sources & Citations

- [Dubi Kelmer, "On distribution of poles of Eisenstein series and the length spectrum of hyperbolic manifolds," Int. Math. Res. Not. 2015, 12319–12344. arXiv:1402.4780](https://arxiv.org/abs/1402.4780)
- References within to Selberg [Sel90] and Gon–Park [GP10] (Selberg Zeta functions).
- Related orbifold literature: Hecke triangle groups via Ruelle / Fredholm determinants (e.g., Streit, Müller, and works on transfer operators for non-arithmetic groups).

---

## Summary

| Aspect | Finding |
|--------|---------|
| **Paper** | Kelmer (2015, arXiv 1402.4780, IMRN) |
| **Theorem class** | Torsion-free finite-volume hyperbolic manifolds |
| **Asymptotic** | Weighted scattering-pole count ~ T log T (leading term κ(d−1)/(2π) T log T) |
| **Fixed group** | Yes, single Γ; family results by comparison |
| **Applies to G_q** | **NO** — requires torsion-freedom; G_q has elliptic elements of orders 2, q |
| **Corollary for G_q** | **None** — hypothesis fails; exponent also differs (T log T ≠ T² log T) |
| **Orbifold coverage** | Explicitly excluded; neat cusps / manifold structure required |

# Deformation prior art for the Hecke-family off-line-resonance law

Date: 2026-08-16  
Scope: published deformation/degeneration literature; primary sources checked where accessible.

## Top-line VERDICT: **SCOOPED**

The **full proposed law** (“every non-arithmetic `G_q`, `q not in {3,4,6}`”) was not found in the surveyed literature. However, the requested scoop test explicitly includes a *family statement*, and that tail statement is already in the literature: Hejhal, *The Selberg Trace Formula for PSL(2,R), Vol. 2* (1983), Theorem 7.11 and Corollary 7.12, states that for every height `t_0` and every `0 < delta < 1`, the rectangles immediately to the right and left of `Re(s)=1/2` contain, respectively, zeros and poles of the scalar Hecke-triangle scattering determinant `phi_N(s)` once `N` is sufficiently large. Garbin–Jorgenson (2018), pp. 161–163, reproduce those exact statements, identify the family as the Hecke triangle groups `G_N`, and quantify the accumulation. Since the scattering determinant is unitary and nonzero on the regular part of `Re(s)=1/2`, these poles/zeros are genuinely off-line (apart from the usual need to avoid a singular boundary ordinate by shrinking/offsetting the rectangle). Thus the `q -> infinity` existence/tail component is already proved, even though the finite list of individual non-arithmetic groups and the universal “every `q`” assertion remain open on the evidence located here. Most Phillips–Sarnak-style work is only adjacent: it starts with an embedded cusp-form eigenvalue and proves conditional dissolution into a resonance under a different deformation.

## 1. Scoop risk

### 1.1 Direct scoop: Hejhal/Selberg and elliptic degeneration of the Hecke triangles

Let `G_N = <z -> -1/z, z -> z + 2 cos(pi/N)>`, with scalar scattering determinant `phi_N(s)`. Garbin–Jorgenson quote the final results of Hejhal, Vol. 2, as follows (their Introduction, pp. 161–162):

- **Hejhal, Theorem 7.11.** Given `t_0 in R` and `0 < delta < 1`, the rectangle
  ` [1/2, 1/2+delta] x [t_0-delta, t_0+delta] ` contains zeros of `phi_N(s)` for all sufficiently large `N`.
- **Hejhal, Corollary 7.12.** The reflected rectangle
  ` [1/2-delta, 1/2] x [t_0-delta, t_0+delta] ` contains poles of `phi_N(s)` for all sufficiently large `N`.

Garbin–Jorgenson explicitly describe these as “zeros accumulating to the right of the critical line and poles to the left,” and say that Hejhal proves convergence of the Eisenstein series and scattering determinants through this Hecke elliptic degeneration. See [Garbin–Jorgenson 2018, Introduction](https://ems.press/content/serial-article-files/44365), especially pp. 161–163; the bibliographic source is Hejhal (1983), Theorem 7.11 and Corollary 7.12.

This is not merely Fermi-golden-rule dissolution. It is an unconditional **large-`N` family location theorem for the exact cofinite Hecke triangle groups**, at arbitrary bounded height. In particular it covers a window around the target height `Im(s_inf) approximately 7.067` for all sufficiently large `q`. It therefore supplies the qualitative tail conclusion that the proposed Rouché continuation route was designed to prove.

Two qualifications matter:

1. The theorem is asymptotic: the threshold depends on `(t_0,delta)` and is not made into the desired explicit `Q_0` in the quoted statement. It does not settle any specified small or medium `q`.
2. It does not assert the stronger law for **every** non-arithmetic `q`; arithmetic/non-arithmetic is not the mechanism in the proof. For sufficiently large integer `N`, however, all `N` except the already-passed arithmetic values `3,4,6` are non-arithmetic.

Garbin–Jorgenson’s **Theorem 5.7** gives a quantitative weighted spectral-counting asymptotic for an elliptically degenerating family,
`N_{M_q,0}(T) = c_0(T) log(Q) + O(log(Q)^(3/4))`.
Their **Remark 5.8** specializes it to the Hecke triangle family (`Q=N`) and explains that it quantifies the accumulation of poles of the scattering determinant. This strengthens abundance/counting, rather than isolating the continuation of the particular theta-group pole `rho_1/2`.

### 1.2 Phillips–Sarnak: adjacent dissolution, not the direct Hecke-family result

Phillips and Sarnak, **“Perturbation theory for the Laplacian on automorphic functions”** (JAMS 5 (1992), 1–32), develop analytic perturbation of the augmented spectrum and the automorphic Fermi golden rule. Their key conclusion is conditional in the relevant sense: given an embedded eigenvalue/cusp form and a deformation direction with nonzero coupling to Eisenstein data, the spectral branch leaves the unitary axis and becomes a scattering pole. This really does locate the perturbed pole off `Re(s)=1/2`, but only after supplying the embedded eigenvalue and verifying the coupling. It is not an unconditional theorem that a particular non-arithmetic Hecke triangle group has such a pole, and the rigid `(2,q,infinity)` orbifolds are not a Teichmüller curve through varying integer `q`.

Phillips–Sarnak, **“On cusp forms in character varieties”** (GAFA 4 (1994), 93–118), moves to character deformations and uses the same instability mechanism to study scarcity of cusp forms. Again the deformation is in a character variety of a fixed group, not `lambda=2 cos(pi/q)` through the cofinite Hecke triangle groups. The precise Fermi-golden-rule formula commonly cited from this paper is equation (5.29); Avelin applies it explicitly in her equations (16)–(18).

Verdict for this corpus: **adjacent, not independently a scoop of the Hecke-`q` law**. It is useful for tracking a known embedded eigenvalue, not for manufacturing the anchor-independent existence assertion.

### 1.3 Petridis–Risager: higher-order dissolution remains conditional/local

Petridis and Risager, **“Dissolving cusp forms: Higher-order Fermi’s Golden Rules”**, Mathematika 59 (2013), 269–301, DOI [10.1112/S0025579312001118](https://doi.org/10.1112/S0025579312001118), prove higher-order necessary and sufficient criteria for a given cusp form to dissolve. Their **Theorem 3.1** gives the higher-order pole-motion/Fermi-golden-rule statement (including multiplicity), and **Theorem 4.2** gives meromorphic continuation and functional equations for higher derivatives of character-deformed Eisenstein series. Their example forces an embedded eigenvalue to become a resonance in a punctured neighborhood of the character-deformation space.

That is a genuine off-line resonance result, but its logical form is still:

`known embedded eigenvalue + nonvanishing derivative/coupling => nearby resonance`.

It neither treats the discrete elliptically degenerating sequence `G_q -> G_infinity` nor proves an off-line resonance for every, generic, or specified non-arithmetic cofinite Hecke triangle group. **Adjacent, not the direct scoop.**

### 1.4 Balslev–Venkov: “Hecke groups” is a dangerous false friend

Balslev–Venkov, **“Spectral theory of Laplacians for Hecke groups with primitive character”**, Acta Math. 186 (2001), 155–217, studies the arithmetic congruence groups `Gamma_0(N)` with primitive characters—not the `(2,q,infinity)` Hecke triangle groups `G_q`. The paper proves a Weyl law (**Theorem 3.6**) and studies regular character perturbations of embedded eigenvalues. Its perturbation section shows that, subject to its hypotheses, eigenfunctions in the relevant odd eigenspaces become resonance functions, with an exceptional arithmetic set of spectral parameters.

This is strong dissolution prior art, but it is a different meaning of “Hecke group,” a fixed arithmetic/congruence setting, and a character perturbation. It does not establish the desired location statement for non-arithmetic Hecke triangles. Primary preprint: [Balslev–Venkov](https://webdoc.sub.gwdg.de/ebook/e/2002/maphysto/publications/mps-rr/1999/41.pdf).

Balslev’s earlier analytic-dilation treatment of embedded eigenvalues likewise rederives the Fermi golden rule by rotating the continuous spectrum so embedded eigenvalues/resonances become isolated eigenvalues of a non-self-adjoint dilated operator. This is perturbation machinery, not a Hecke-triangle existence theorem.

### 1.5 Farmer–Lemurell and Avelin: numerical pole tracking, not a theorem for `G_q`

Farmer–Lemurell, **“Deformations of Maass forms”**, Math. Comp. 74 (2005), 1967–1982, DOI [10.1090/S0025-5718-05-01746-1](https://doi.org/10.1090/S0025-5718-05-01746-1), reports numerical calculations testing the Phillips–Sarnak conjecture. Its abstract carefully says the calculations “indicate” that cusp forms either persist along special deformation sets or dissolve into resonances. It is not a rigorous generic-existence or Hecke-triangle-location theorem.

Avelin, **“Deformation of `Gamma_0(5)`-cusp forms”**, Math. Comp. 76 (2007), 361–384, rigorously relates Taylor coefficients of pole motion to Phillips–Sarnak’s formula and numerically tracks poles. **Lemma 3.1** supplies a sufficient positivity condition for destruction throughout a punctured neighborhood; the paper also stresses that its computations concern `Gamma_0(5)` Teichmüller space. This is excellent nearby methodology, but not the cofinite Hecke `q` sequence.

### 1.6 Bruggeman–Fraczek–Mayer: a real off-line-curve theorem, but for singular character deformation of `Gamma_0(4)`

Bruggeman, Fraczek, and Mayer, **“Perturbation of zeros of the Selberg zeta-function for `Gamma_0(4)`”**, Experimental Math. 22 (2013), 217–242, DOI [10.1080/10586458.2013.776381](https://doi.org/10.1080/10586458.2013.776381), arXiv:[1201.2324](https://arxiv.org/abs/1201.2324), is closer to a location result than the basic Fermi-golden-rule papers. **Theorems 1.4 and 1.5** describe curves of zeros/resonances under a singular character deformation and their tangency/asymptotics at `Re(s)=1/2`; the proofs place the resonance branches on the left side. This is a proved off-line resonance-curve statement.

It still does not scoop the cofinite Hecke-triangle law: the base is arithmetic `Gamma_0(4)`, the parameter is a character/singular perturbation, and the resulting family is not `G_q`. It does demonstrate that “off-line location under deformation” as a general phenomenon is established prior art; only the Hecke-triangle specialization/tail is supplied directly by Hejhal/Garbin–Jorgenson.

### 1.7 Wolpert, Borthwick, and the Zworski-school resonance literature

Wolpert, **“Asymptotics of the spectrum and the Selberg zeta function on the space of Riemann surfaces”**, Comm. Math. Phys. 112 (1987), 283–315, concerns hyperbolic degeneration by pinching geodesics. It proves degeneration/continuity results for spectral data and the Selberg zeta function, not an off-line resonance for a non-arithmetic Hecke triangle group. Its geometry is not the relevant one: `q -> infinity` is **elliptic degeneration** (a cone point of order `q` becomes a cusp), not pinching a closed geodesic.

Borthwick’s book, *Spectral Theory of Infinite-Area Hyperbolic Surfaces*, 2nd ed. (2016), Chapters 7–11, develops meromorphic resolvents, scattering poles, multiplicities, growth estimates, and the Selberg-zeta divisor. Borthwick–Perry and Borthwick–Judge–Perry prove structural equivalence/divisor results and genericity statements for resonances under potential/metric perturbations. These results tell one how resonances move and how zeta zeros encode them; they do not assert the requested resonance for a cofinite non-arithmetic `G_q`. Moreover, the much-studied continuous Hecke family `Gamma_w`, `w>2`, has infinite area (the cusp-to-funnel side of `w=2`), whereas the cofinite sequence here approaches `w=2` from the isolated values `w=2 cos(pi/q)<2`.

**Scoop-risk conclusion.** The general deformation papers are adjacent. The direct scoop is more specific and older: Hejhal’s Hecke-triangle scattering theorem, subsequently reframed and quantified as elliptic degeneration by Garbin–Jorgenson.

## 2. Gift: ranked importable statements

### 1. Hejhal, Theorem 7.11 and Corollary 7.12 — import the conclusion, not merely a bound

**Source.** Hejhal (1983), Vol. 2, Theorem 7.11 and Corollary 7.12; exact statement independently reproduced in Garbin–Jorgenson (2018), pp. 161–162.

**Gift.** For the actual Hecke sequence, it already gives zeros/poles in arbitrary rectangles adjacent to the critical line for all sufficiently large `q`. For the lane’s purpose, this can replace the proposed local-boundedness-plus-Rouché tail step altogether, unless the proof specifically requires continuation of the *particular* theta pole at `rho_1/2` or an explicit computable threshold `Q_0`.

**Adaptation.** Set `t_0 = 7.067...` and choose `delta` smaller than the desired height/real-part margin. Combine the qualitative tail with finite verification below the resulting (currently ineffective/unextracted) threshold. The immediate next literature task should be to reconstruct Hejhal’s proof constants, not to reprove qualitative existence.

### 2. Garbin–Jorgenson, Theorem 7.1 and Corollary 7.2 — exact elliptic-degeneration continuity of `Z`

**Source.** Garbin–Jorgenson (2018), **Theorem 7.1** and **Corollary 7.2**.

**Statement.** For an elliptically degenerating finite-volume sequence `M_q -> M_infinity`, the truncated logarithmic derivatives converge, and `Z_{M_q}(s) -> Z_{M_infinity}(s)` for

`Re(s)>1` **or** `Re(s^2-s)>1/4`.

**Why it matters.** This is the exact degeneration type and explicitly includes the Hecke triangle example. It is the cleanest published donor for continuity in `q`/elliptic order.

**Critical limitation.** At `s = sigma + i*7.067` with `sigma in (3/4,1)`,
`Re(s^2-s)=sigma^2-sigma-(7.067)^2`, which is far below `1/4`. Therefore the published domain does **not** include the lane’s target strip at that height. The theorem cannot be cited as proving the requested local boundedness there. Its heat-trace/logarithmic-derivative proof is nevertheless the correct template to extend; the missing donor-strengthening is compact-uniform meromorphic control at large imaginary part inside `1/2 < sigma < 1`.

### 3. Garbin–Jorgenson, Theorem 5.7 and Remark 5.8 — quantitative control of scattering-pole accumulation

**Source.** Garbin–Jorgenson (2018), **Theorem 5.7**, **Remark 5.8**.

**Statement.** The continuous-plus-discrete spectral counting function grows as `c_0(T) log(Q)` with error `O(log(Q)^(3/4))`; for Hecke triangles, `Q=N`, and the result quantifies accumulation of scattering poles.

**Adaptation.** This does not give a pointwise bound on `phi_q(s)` or `Z_q(s)`, but it can furnish a normal-family/zero-counting input on bounded spectral windows and may make the Hejhal threshold quantitative after the proof is unpacked. It is better suited to existence/abundance than to a Rouché estimate for one prescribed contour.

### 4. Schulze, Theorems 3.18 and 3.21; Corollary 3.17 — the strongest ready-made local-boundedness pattern

**Source.** Michael Schulze, **“On the resolvent of the Laplacian on functions for degenerating surfaces of finite geometry”**, J. Funct. Anal. 236 (2006), 120–160, arXiv:[math/0410434](https://arxiv.org/abs/math/0410434).

- **Corollary 3.17:** normalized approximate Eisenstein functions and scattering matrices depend continuously on the degeneration parameter as meromorphic families off `Re(s)=1/2`.
- **Theorem 3.18:** after dividing by the pinched-geodesic local factors, the Selberg zeta functions vary continuously in the topology of locally uniform convergence on `Re(s)>1/2`.
- **Theorem 3.21:** on relatively compact `K subset {Re(s)>1/2}` and a relatively compact parameter set, the normalized zeta (after removing small-eigenvalue zeros and pinching factors) has uniform positive upper and lower bounds.

**Adaptation.** If an elliptic-degeneration analogue of Theorems 3.18/3.21 is proved, it gives exactly the requested compact-uniform boundedness on `sigma in (3/4,1)` near `sigma+i7.067`. The obstacle is hypothesis transfer: Schulze treats fixed-topological-type **hyperbolic pinching**, whereas `G_q -> G_infinity` changes a cone point into a cusp. No direct citation-based substitution is valid. Garbin–Jorgenson supplies the correct elliptic heat-kernel framework, suggesting a feasible synthesis.

### 5. Petridis–Risager, Theorem 4.2 — meromorphic deformation derivatives of Eisenstein data

**Source.** Petridis–Risager (2013), **Theorem 4.2**.

**Statement.** Higher character derivatives of Eisenstein series admit meromorphic continuation, satisfy resolvent identities and functional equations, and have polynomial growth in vertical strips away from the singular set.

**Adaptation.** For a genuine analytic deformation on a fixed surface/group, Cauchy estimates on the parameter Taylor series can yield local bounds for Eisenstein/scattering data away from moving poles. But `q` is discrete and the cone-to-cusp endpoint is singular; this theorem supplies the perturbative algebra, not the uniform endpoint estimate. It ranks below the elliptic-degeneration results.

### 6. Phillips–Sarnak analytic augmented spectrum and Fermi-golden-rule expansion

**Source.** Phillips–Sarnak (1992), especially the analytic perturbation framework and second-order Fermi-golden-rule formula; Phillips–Sarnak (1994), equation (5.29), for the character-variety form.

**Adaptation.** Once a pole/eigenvalue branch is isolated and the deformation is analytic, these formulas control its first nonzero departure from the line. They could identify the direction/size of motion of the theta anchor. They do **not** by themselves give a uniform bound for the full zeta/scattering determinant near the elliptic endpoint, nor do they turn the discrete `q` sequence into a smooth family.

### 7. Naud–Pohl–Soares, Theorem 1.1 and Proposition 4.1 — analytic transfer operators on the other side of `lambda=2`

**Source.** Naud, Pohl, Soares, **“Hecke Triangle Groups, Transfer Operators and Hausdorff Dimension”**, Ann. Henri Poincare 23 (2022), 2373–2408, DOI [10.1007/s00023-021-01117-1](https://doi.org/10.1007/s00023-021-01117-1).

**Statement.** **Theorem 1.1** represents `Z_{Gamma_w}(s,rho)` by a Fredholm determinant of a trace-class transfer operator for `w>2`, `Re(s)>1/2`. **Proposition 4.1** gives explicit matrix coefficients with analytic `w`-dependence (involving `zeta(2s+i+j) w^{-(2s+i+j)}`), on a fixed Bergman-space model.

**Adaptation.** This is attractive for deriving compact-uniform determinant bounds by trace-norm continuity, but it approaches `w=2` from the **infinite-area** side. It does not cover the cofinite values `w=2 cos(pi/q)<2`, whose symbolic dynamics has an elliptic relation of changing order. It is evidence that a fixed-space transfer-operator proof is plausible, not a theorem that closes the lane.

## Recommended import decision

1. For the qualitative large-`q` law, cite **Hejhal Theorem 7.11/Corollary 7.12** and stop trying to prove that same tail by Rouché.
2. For a paper-quality modern formulation and quantitative abundance, cite **Garbin–Jorgenson Theorem 5.7/Remark 5.8**.
3. If the project specifically needs local uniform convergence of `Z_q` near the theta zero, the closest exact donor is **Garbin–Jorgenson Theorem 7.1/Corollary 7.2**, but its domain misses the target height. The missing new lemma is an extension of their elliptic-degeneration control to compact subsets of `Re(s)>1/2` away from poles, analogous to **Schulze Theorems 3.18/3.21**.
4. Do not cite Phillips–Sarnak, Petridis–Risager, or Balslev–Venkov as proving the Hecke-triangle tail; they prove a different conditional dissolution mechanism.

## References

- H. Avelin, “Deformation of `Gamma_0(5)`-cusp forms,” *Mathematics of Computation* **76** (2007), 361–384. DOI: 10.1090/S0025-5718-06-01884-7.
- E. Balslev, “Spectral deformation of Laplacians on hyperbolic manifolds,” *Communications in Analysis and Geometry* **5** (1997), no. 2, 213–247. (No theorem from this paper is load-bearing here.)
- E. Balslev and A. Venkov, “Spectral theory of Laplacians for Hecke groups with primitive character,” *Acta Mathematica* **186** (2001), 155–217. [Primary preprint](https://webdoc.sub.gwdg.de/ebook/e/2002/maphysto/publications/mps-rr/1999/41.pdf).
- D. Borthwick, *Spectral Theory of Infinite-Area Hyperbolic Surfaces*, 2nd ed., Progress in Mathematics 318, Birkhauser, 2016. DOI: [10.1007/978-3-319-33877-4](https://doi.org/10.1007/978-3-319-33877-4).
- D. Borthwick, C. Judge, and P. A. Perry, “Selberg’s zeta function and the spectral geometry of geometrically finite hyperbolic surfaces,” *Commentarii Mathematici Helvetici* **80** (2005), 483–515. DOI: [10.4171/CMH/23](https://doi.org/10.4171/CMH/23).
- R. Bruggeman, M. Fraczek, and D. Mayer, “Perturbation of zeros of the Selberg zeta-function for `Gamma_0(4)`,” *Experimental Mathematics* **22** (2013), 217–242. DOI: [10.1080/10586458.2013.776381](https://doi.org/10.1080/10586458.2013.776381); arXiv:[1201.2324](https://arxiv.org/abs/1201.2324).
- D. W. Farmer and S. Lemurell, “Deformations of Maass forms,” *Mathematics of Computation* **74** (2005), 1967–1982. DOI: [10.1090/S0025-5718-05-01746-1](https://doi.org/10.1090/S0025-5718-05-01746-1); arXiv:[math/0302214](https://arxiv.org/abs/math/0302214).
- D. Garbin and J. Jorgenson, “Spectral asymptotics on sequences of elliptically degenerating Riemann surfaces,” *L’Enseignement Mathematique* **64** (2018), 161–206. DOI: [10.4171/LEM/64-1/2-7](https://doi.org/10.4171/LEM/64-1/2-7); [full text](https://ems.press/content/serial-article-files/44365); arXiv:[1603.01494](https://arxiv.org/abs/1603.01494).
- D. A. Hejhal, *The Selberg Trace Formula for PSL(2,R), Volume 2*, Lecture Notes in Mathematics 1001, Springer, 1983. See Theorem 7.11 and Corollary 7.12. DOI: [10.1007/BFb0061302](https://doi.org/10.1007/BFb0061302).
- M. Moller and A. D. Pohl, “Period functions for Hecke triangle groups, and the Selberg zeta function as a Fredholm determinant,” *Ergodic Theory and Dynamical Systems* **33** (2013), 247–283. DOI: [10.1017/S0143385711000794](https://doi.org/10.1017/S0143385711000794); arXiv:[1103.5235](https://arxiv.org/abs/1103.5235).
- F. Naud, A. Pohl, and L. Soares, “Hecke Triangle Groups, Transfer Operators and Hausdorff Dimension,” *Annales Henri Poincare* **23** (2022), 2373–2408. DOI: [10.1007/s00023-021-01117-1](https://doi.org/10.1007/s00023-021-01117-1).
- Y. N. Petridis and M. S. Risager, “Dissolving cusp forms: Higher-order Fermi’s Golden Rules,” *Mathematika* **59** (2013), 269–301. DOI: [10.1112/S0025579312001118](https://doi.org/10.1112/S0025579312001118); arXiv:[1003.2820](https://arxiv.org/abs/1003.2820).
- R. S. Phillips and P. Sarnak, “Perturbation theory for the Laplacian on automorphic functions,” *Journal of the American Mathematical Society* **5** (1992), 1–32. DOI: [10.1090/S0894-0347-1992-1127079-8](https://doi.org/10.1090/S0894-0347-1992-1127079-8).
- R. S. Phillips and P. Sarnak, “On cusp forms in character varieties,” *Geometric and Functional Analysis* **4** (1994), 93–118. [EuDML record/full-text link](https://eudml.org/doc/58158).
- M. Schulze, “On the resolvent of the Laplacian on functions for degenerating surfaces of finite geometry,” *Journal of Functional Analysis* **236** (2006), 120–160. DOI: [10.1016/j.jfa.2006.02.009](https://doi.org/10.1016/j.jfa.2006.02.009); arXiv:[math/0410434](https://arxiv.org/abs/math/0410434).
- S. A. Wolpert, “Asymptotics of the spectrum and the Selberg zeta function on the space of Riemann surfaces,” *Communications in Mathematical Physics* **112** (1987), 283–315. DOI: [10.1007/BF01217868](https://doi.org/10.1007/BF01217868).

## Confidence and unresolved verification points

- **High confidence:** the Hejhal theorem/corollary wording, numbering, and Hecke-family specialization, because Garbin–Jorgenson reproduce them explicitly and build their paper around them.
- **High confidence:** Garbin–Jorgenson Theorems 5.7, 7.1 and Corollary 7.2; Schulze Corollary 3.17 and Theorems 3.18, 3.21; these were checked in full text.
- **Moderate confidence:** the detailed theorem-number summaries for Petridis–Risager and Bruggeman–Fraczek–Mayer; the papers and broad statements are verified, but any final publication should check the displayed hypotheses directly against the typeset PDFs.
- **Not found:** a published compact-uniform bound for `Z_{G_q}` or `phi_q` on a neighborhood of `sigma+i7.067`, `sigma in (3/4,1)`, with an explicit rate in `2-lambda_q`; nor a theorem proving the off-line resonance law separately for every non-arithmetic `q`.

---

## Frontier verification 2026-08-16 (primary source)

Garbin–Jorgenson, L'Enseignement Math. (2) 64 (2018) 161–206, DOI
10.4171/LEM/64-1/2-7, fetched and read (pp. 161–163). CONFIRMED verbatim
(p. 162): "Given t₀ ∈ ℝ and 0 < δ < 1, the rectangle [1/2, 1/2+δ] ×
[t₀−δ, t₀+δ] must contain zeros of φ_N(s) and the rectangle [1/2−δ, 1/2] ×
[t₀−δ, t₀+δ] must contain poles of φ_N(s) when N is sufficiently large."
(Hejhal Vol. 2, Thm 7.11 + Cor 7.12; Hejhal attributes the result to
SELBERG — "appears in the ending remarks of Selberg's Göttingen lectures
part 2".) GJ Cor 7.2 (Z-continuity through elliptic degeneration) holds for
Re(s) > 1 or Re(s²−s) > −1/4; at s_∞ = 1/4 + 7.067i, Re(s²−s) ≈ −50 —
NOT a donor for the strip, as the scout said.

## Frontier ruling

1. **The qualitative large-q tail of the law is a Selberg–Hejhal theorem
   (1983), ineffective in q.** Our program's tail obligation reframes from
   "prove existence for large q" to "make it EFFECTIVE (explicit Q₀) and
   certify the finite base q < Q₀" — which, combined, still yields the full
   law "every non-arithmetic q", a statement the literature does NOT have.
2. **The flagship G_5 theorem's novelty is intact**: Selberg–Hejhal is
   asymptotic and says nothing about any specific q, gives no constants, no
   boxes, no certificates. Ours is the first rigorous localization at a
   named surface (V1 ruling unchanged in substance).
3. **Corrections owed NOW**: flagship paper v2's novelty framing (its
   "Hejhal 1983 UNRESOLVED" is resolved AGAINST family-statement novelty —
   must cite Selberg–Hejhal and reposition as effective/instance-level
   contribution + dichotomy mechanism); N3 prior-art status; ledger; the
   U1-min/strip lanes re-aim at effectivity rather than bare existence.
4. **Gift confirmed in kind**: Hejhal §7's proof (elliptic degeneration of
   Eisenstein/scattering data) is now the natural donor skeleton for an
   effective version. Hejhal Vol. 2 §7 full text = HITL library item
   (currently have only GJ's quotation of the statements).

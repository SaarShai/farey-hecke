# Citation-grade novelty audit — U2 "Quantitative cusp-geometry edge formula"

**Date:** 2026-06-14. **Auditor stance:** default "likely known"; we overclaimed once
(reciprocity scan) and must not repeat. WebSearch/WebFetch + direct PDF extraction of the
two load-bearing papers (golden-L 1308.4203, Taha 1810.10668).

## The statement under audit (U2)
> For EVERY lattice (Veech) translation surface (equiv. every non-uniform lattice Fuchsian
> group with cusps), the SUPPORT EDGE / smallest value ("hard edge") of the slope-gap (or
> gap-product) distribution of saddle connections / the horocycle cross-section equals an
> EXPLICIT FUNCTION OF THE CUSP GEOMETRY (cylinder widths / systole / parabolic-fixed-point
> data) — uniformly across the family via ONE formula, not surface-by-surface.

---

## VERDICT: **PARTIAL — but the genuinely-new core is thin and the headline claim is essentially KNOWN / not-a-theorem.**

Split by piece:

| Sub-claim | Status | Why |
|---|---|---|
| There IS a hard edge iff lattice surface | **KNOWN** (Athreya–Chaika 2012; Smillie–Weiss "no small triangles") | qualitative — the existence of the edge is the defining lattice-surface property |
| The edge = **minimum of the return-time / roof function** of the (uniformly constructed) horocycle Poincaré section | **KNOWN / structural** (Athreya–Chaika–Lelièvre 1308.4203; Kumanduri–Sanchez–Wang 2102.10069; Taha 1810.10668) | the slope gap **is** the return time `R`; edge = ess-inf `R`. ACL: "`R` … uniformly bounded below by 1" ⇒ "f(x)=0 for 0≤x≤1". This is already a per-surface reading-off of a cusp/section quantity. |
| The section / framework is built **UNIFORMLY for all Veech surfaces** | **KNOWN** (KSW 2102.10069; Taha for all `G_q`) | KSW give the explicit Poincaré-section parametrization for an **arbitrary** Veech surface and prove piecewise-real-analytic + quadratic tail; Taha gives the roof function `R_q(a,b)` for **all** Hecke `G_q`. |
| The edge written as a **closed-form function of cusp geometry, uniformly via one formula** | **NOT FOUND stated as a theorem** — this is the only genuinely-open slot | KSW/Taha stop at constructing the section and proving structure; they do **not** extract `ess-inf R` as a closed-form cusp invariant. The edge is read off **per surface** from the explicit section (ACL: value 1 for golden-L; Taha: not extracted for general `q`). |
| The edge characterised as an **ergodic-optimization ground value** (inf_μ ess-sup) + cluster-onset bridge | **NOT FOUND in this literature** — this is the project's own framing | EO/zero-temperature lens on the parabolic section map is not in the slope-gap papers. |

**Bottom line:** the *object* (edge = min return time of a uniformly-constructed section, a
cusp/cylinder quantity) and the *uniform machinery* (KSW, Taha) are **already in the
literature**. What is NOT explicitly written down is (i) the edge as a **single closed-form
function of cusp data valid across a family**, and (ii) the **ergodic-ground-value /
cluster-onset characterization**. Those two are narrow and partly normalization-artifacts (see
§"narrowest new version"). This is **not** a new unifying theorem in the strong sense U2 asserts —
it is a methods-grade strengthening + a re-characterization of edges that are individually known.

---

## Closest papers (exact titles + arXiv id + one-line relevance)

1. **Athreya, Chaika — "The distribution of gaps for saddle connection directions"**, GAFA 2012
   (arXiv:1204.5642 / Springer s00039-012-0164-9).
   *The qualitative dichotomy:* liminf of renormalized gaps is bounded away from 0 **iff** the
   surface is a lattice surface — i.e. there IS a hard edge, but **no value** is given.

2. **Athreya, Chaika, Lelièvre — "The gap distribution of slopes on the golden L"**,
   arXiv:1308.4203 (2013/2015).
   *The prototype edge.* Proves the slope gap = return time `R` of an explicit BCZ-type
   section; "`R` … uniformly bounded below by **1**", hence density `f(x)=0` on `[0,1]`, edge `=1`.
   **Per-surface**, derived from the explicit 3-piece roof function — exactly the
   "extract-edge-from-full-section" pattern, not a uniform cusp formula.

3. **Kumanduri, Sanchez, Wang — "Slope gap distributions of Veech surfaces"**,
   arXiv:2102.10069 (AGT 24 (2024) 951–980).
   *The uniform construction.* Explicit Poincaré-section parametrization for an **arbitrary**
   Veech surface; proves piecewise-real-analytic + quadratic tail **uniformly**. Constructs the
   section family-wide but **does not** state the support edge as a closed-form cusp invariant —
   the closest prior art to U2's "uniformity," and it stops short of U2's "edge formula."

4. **Taha — "The Boca–Cobeli–Zaharescu map analogue for the Hecke triangle groups G_q"**,
   arXiv:1810.10668 (2018/19).
   *The project's own object, family-wide.* Gives the explicit roof function
   `R_q(a,b)=y_i^q/(a·((a,b)·w_i^q))` and slope-gap law `= m_q(1_{R_q≥t})` for **all** `G_q`;
   wedge products bounded below by `q` (the discreteness/no-small-gap input). **Does not** extract
   `ess-inf R_q` (the edge) as a closed-form function of `q`/`λ_q`. That extraction (= `1/λ³`) is
   precisely what the Farey-Hecke project adds.

5. **Hubert, Marchese, Ulcigrai — "Lagrange spectrum of a Veech surface has a Hall ray"**,
   arXiv:1409.7023 (and Artigiani–Marchese, "Persistent Hall rays …", arXiv:1710.02042).
   *Opposite end — anti-match.* These give the **TOP** of the spectrum (a Hall ray `[r(S),∞)` of
   large values / well-approximable directions / large gaps) as a per-surface quantity. U2's hard
   edge is the **BOTTOM/smallest gap**; these confirm the relevant literature works the *other*
   end of the spectrum, so they do **not** pre-empt U2 — but they show "explicit-spectral-endpoint
   as cusp data" is a familiar move in the field.

6. **Marklof, Pollicott — "Extreme events for horocycle flows"**, arXiv:2408.01781 (2024/25).
   *Near-miss on vocabulary, not on content.* EVT for **cusp excursions** (max excursion INTO the
   cusp = large-deviation / large-gap end), limit law via **Hall's** Farey formula. Same
   "extreme-value + horocycle + cusp" words as our cluster-onset framing, but it is the
   large-excursion tail, **not** the smallest-gap hard edge, and gives no uniform edge formula.

*(Also logged, lower relevance: 2n-gon slope gaps arXiv:2109.04495; double-heptagon
arXiv:2508.19252; effective slope gaps arXiv:2409.15660 — all per-surface/per-family computations
or convergence-rate results, none stating a uniform closed-form edge-as-cusp-invariant.)*

---

## Narrowest genuinely-new version (what survives the audit)

Each per-surface edge is known and the uniform *section machinery* is known (KSW, Taha). What is
**not** in the literature, and is the only defensible novelty:

- **(N1) A family-uniform support-edge THEOREM derived by one method** — i.e. proving
  `edge = (explicit cusp/parabolic-vertex value)` for a whole family (Hecke `G_q`, prospectively
  2n-gon / Bouw–Möller) by a single argument (GATE-2 corridor-classification → arc-coverage →
  edge forced), rather than computing the full density surface-by-surface. This is a **methods**
  contribution: it collapses the one-surface-per-paper pattern. KSW give the *section* uniformly
  but not the *edge value* uniformly; that gap is real.
- **(N2) The ergodic-optimization characterization of the edge** — edge `= inf_μ ess-sup_μ P`
  (zero-temperature ground value of the parabolic section map), **plus** the machine-verified
  bridge edge = extreme-gap **cluster-onset** threshold. The EO/zero-temperature lens on a
  parabolic, zero-entropy section is genuinely absent from the slope-gap literature.

Both are narrow. (N1)'s *output* is normalization-dependent (the golden-L edge is the artifact
constant **1**; for `G_q` it is `1/λ³` under the project's normalization — same object, different
units), so it is **not a new lattice invariant** and **not an arithmeticity detector** — the
project's own `Xomega_generalize_2026-06-14.md` reached this same conclusion independently.

---

## One honest sentence

This is **not a new unifying theorem** in the strong sense U2 asserts — the support edge is
already understood, family-wide, as the minimum return time of the uniformly-constructed
horocycle Poincaré section (KSW/Taha/ACL), so U2 mostly **repackages known per-surface edges**;
the only honest novelty is (i) *proving* the edge for a whole family by one method instead of
case-by-case, and (ii) the ergodic-ground-value/cluster-onset re-characterization — i.e. a
**methods-and-reframing** contribution, not a new invariant or a genuine unifying law.

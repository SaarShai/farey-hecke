# Phillips–Sarnak dissolution geometry of even cusp forms in Hecke triangle groups
## Discovery note — AIM 2, 2026-06-20

**Status: READY FOR JUDGING.** Conjecture posed from certified data on TWO non-arithmetic
surfaces (G_5, G_7) + one arithmetic anchor (q=3). Not a theorem; not formalized.

---

## 0. Setup and parameterization (read first — this is load-bearing)

- Surfaces: cofinite (finite-area, one cusp) Hecke triangle groups G_q = (2, q, ∞),
  λ_q = 2cos(π/q). Arithmetic only for q = 3, 4, 6, ∞ (Takeuchi 1977). q = 5, 7 non-arithmetic.
- The Selberg zeta / Mayer transfer-operator determinant det(1 − L_s^±) is computed in the
  **s-plane**, where the spectral edge (bottom of continuous spectrum / cusp threshold) is
  **Re(s) = 1/2**, and an even (+)/odd (−) Maass cusp form of eigenvalue s(1−s) gives a
  1-eigenfunction on Re(s) = 1/2 (Pohl; Bruggeman–Pohl; Mayer–Mühlenbruch–Strömberg).
- Engine: `code/zeta_cert_rosen.py` (Arb-ball certified), validated on q=5 against the
  hard-coded `zeta_cert_rosen_q5.py` (max midpoint diff 0). Newton search is confined to the
  strip `0 < Re(s) < 1/2` and stopped at `Re(s) ≥ 1/2` (engine line 198).
- **Arithmetic anchor (q=3):** the even-sector "resonances" are pinned at **Re(s) = 1/4**,
  Im = γ_n/2 — i.e. ρ = 1/4 + iγ_n/2 are the nontrivial zeta zeros (det(1−L^+_s)=0 ⟺ ζ(2s)=0).
  Certified at Re=1/4 to std 6.5e−14 (`resonance_geometry.json`). This is the *undissolved* line.

So the dissolution picture in these coordinates is: the even-sector spectrum, which for the
arithmetic q=3 sits on the **line Re = 1/4**, **drifts UP toward the spectral edge Re = 1/2**
as the surface is deformed to a non-arithmetic G_q, where the even cusp forms cannot exist
(Phillips–Sarnak conjecture) and instead appear as scattering resonances Re(s) < 1/2.

---

## 1. Certified data (COMPUTED — quoted from repo JSON; one resonance independently re-run)

From `code/out/resonance_geometry.json` (q=3, G_5; prec 400 bits) and
`code/out/resonance_g7.json` (G_7; prec 400 bits, engine self-checked vs q=5).

| surface | arith? | λ_q | n | even-resonance Re: mean | std | min | max |
|---------|--------|-----|---|--------|-----|-----|-----|
| q = 3   | YES    | 1.000 | 8 | 0.250000 | 6.5e−14 | 0.25 | 0.25 |
| G_5     | no     | 1.618 | 8 | 0.4388 | 0.0300 | 0.3998 | 0.4853 |
| G_7     | no     | 1.802 | 12 | 0.3932 | 0.1029 | 0.1535 | 0.4842 |

Sorted Re-values:
- **G_5:** 0.3998, 0.4004, 0.4105, 0.4445, 0.4471, 0.4539, 0.4691, 0.4853 — one tight band.
- **G_7:** 0.1535, 0.2303, 0.3165 | 0.3928, 0.3969, 0.4031, 0.4453, 0.4696, 0.4732, 0.4752, 0.4780, 0.4842
  — a **low tail of 3** + a **high cluster of 9**. The Re-gaps after sorting (0.077, 0.086, 0.076,
  then 0.004, 0.006, ...) show a clean break at Re ≈ 0.35.

**Independent reproducibility check (COMPUTED this session):**
`cd code && python3 -c "import zeta_cert_rosen as Z; ..."` at the published G_5 even resonance
s = 0.4538952 + 5.7635372i, sign=+1, q=5, N=12 →
`|det| = 1.72e−06` (deep dip; publication uses larger N → 7.5e−16), while off-resonance control
Re=0.40 → `|det| = 0.2368`. Resonance is genuine and reproducible.

---

## 2. The two phenomena (COMPUTED)

### (A) Universal dissolved-bulk attractor — the dissolved even spectrum piles up at a
### q-INDEPENDENT real part Re* ≈ 0.44, NOT at a q-dependent location.

Dissolved bulk = {all 8 G_5} ∪ {the 9 high G_7, Re > 0.35}:
- G_5 bulk: Re = 0.4388 ± 0.0106 (SEM)
- G_7 bulk: Re = 0.4465 ± 0.0120 (SEM)
- **Welch two-sample t-test of the two bulk centers: t = −0.45, p = 0.66** → statistically
  **indistinguishable**, despite λ_5 = 1.618 vs λ_7 = 1.802 (a 11% change in deformation).
- Combined bulk (n=17): **Re* = 0.4429 ± 0.034 (std), SEM 0.008**; i.e. **0.057 ± 0.034 below
  the spectral edge Re = 1/2**.

This is the surprise. The naive Fermi-golden-rule reading ("more deformation ⇒ resonance pushed
further off the line") would put the G_7 bulk at a *different* Re than G_5. Instead both bulks lock
onto the **same** sub-edge band. The deformation does not set *where* the dissolved bulk lands; it
sets *how much* of the spectrum has reached the attractor.

No clean closed form for 0.443 found (checked 1/2−1/2π = 0.341, golden 1/2−(√5−2)/2 = 0.382,
δ/2 of the badly-approximable set = 0.266 — none match). Reported as an empirical band, not overfit.

### (B) Partial vs. full dissolution — a non-arithmeticity "completeness" signature.

G_5 (further from any arithmetic q): **fully dissolved** — all 8 even resonances are in the
attractor band, none left near the old Re=1/4 line.
G_7 (adjacent to arithmetic q=6, λ_6=1.732, |λ_7−λ_6|=0.070): **partially dissolved** — 3 of 12
resonances (Re = 0.15, 0.23, 0.32) are strung BACK toward the Re=1/4 line, a residual "memory" of
the undissolved arithmetic spectrum. The Re-range (max−min) is the right ordering:
**G_5 range 0.085 (compact) vs G_7 range 0.331 (a tail).** This inverts the std-only reading
(G_7 std 0.103 > G_5 std 0.030) by attributing G_7's larger spread to the *tail*, not the *bulk*.

---

## 3. THE CONJECTURE (sharp, falsifiable)

Let G_q = (2,q,∞), q non-arithmetic (q ∉ {3,4,6}), and let
R^+(q) = {even-sector scattering resonances s, 0 < Re s < 1/2} (zeros of det(1−L^+_s)).

> **Conjecture (Dissolution attractor).** There is a universal band
> Re* ∈ [0.42, 0.47] (numerically Re* ≈ 0.443, i.e. ≈ 0.057 ± 0.034 below the spectral edge 1/2),
> **independent of q**, such that the *bulk* of R^+(q) — all but a finite (q-dependent) number of
> low-lying resonances — accumulates with Re(s) → Re* as the surface is held fixed and Im(s) grows.
> The *fraction* of R^+(q) that has reached the band increases monotonically with the
> "arithmetic distance" dist(λ_q, {λ_3,λ_4,λ_6,2}); the complementary residual resonances form a
> **dissolution tail** trailing from the band back toward the line Re = 1/4 (the arithmetic q=3
> even locus). For surfaces maximally far from arithmetic, the tail is empty (full dissolution).

Two independent sub-claims, each separately falsifiable:
- **(A) q-independence of the bulk band** — strong form: lim sup over q of the bulk-center spread
  is O(10^−2), NOT growing with λ_q.
- **(B) tail ↔ arithmetic-proximity** — the number of off-band (Re ≲ 0.35) resonances is a
  monotone function of proximity to the nearest arithmetic Hecke point.

---

## 4. Evidence shape — what would CONFIRM vs REFUTE (and how WE can run it)

CONFIRM (A): compute even resonances for **G_9, G_11, G_12** (q=12 is the *next* arithmetic point;
its non-arith neighbours q=11,13 should show tails like G_7; q=9 is "interior" non-arith like G_5
and should be near-fully dissolved). If their bulk centers all sit in [0.42, 0.47] within ~0.03,
(A) is corroborated on 5 surfaces. **Feasible NOW**: `code/zeta_cert_rosen.py` is q-general
(`hecke_params(q)`); `run_resonance_g7.py` is a ready template (it took ~2800 s wall for G_7 at 400
bits, 12 resonances). A 3-surface sweep is an overnight job.

REFUTE (A): any non-arith G_q whose bulk center lands clearly outside [0.40, 0.49] (e.g. tracks
1/2 − c·(λ_q−λ_3) for some c>0), i.e. the bulk *does* move with deformation. A single clean
counterexample kills the universality.

CONFIRM (B): G_11, G_13 (arith-adjacent) show non-empty low tails of size comparable to G_7's 3;
G_9 (interior) shows an empty/tiny tail like G_5. REFUTE (B): G_9 has a big tail or G_11 none.

A counterexample to the whole thing: the q=3 even locus is itself the trivial-zeros line Re=1/4;
if a deformation analysis (continuously deform λ from 1 upward, tracking the first few resonances)
showed them moving DOWN/staying near 1/4 rather than up toward 1/2, the "drift toward the edge"
frame is wrong.

---

## 5. NOVELTY — brutal scan

**What is OWNED (do not claim):**
- *That* even cusp forms dissolve into resonances off Re=1/2 for non-arith Hecke groups:
  Phillips–Sarnak 1985 conjecture; reformulated via transfer operators by
  Möller/Pohl and **Bruggeman–Pohl** ("Odd and even Maass cusp forms for Hecke triangle groups",
  arXiv:1303.0528; Memoirs AMS 287/1423, 2023). The even-sector L^+_s framing we use is theirs.
- *The rate* an embedded eigenvalue leaves the line under deformation: Phillips–Sarnak Fermi
  Golden Rule; higher orders by **Petridis–Risager** ("Dissolving cusp forms: higher order Fermi's
  golden rules", arXiv:1003.2820, Mathematika 2013). This is the **infinitesimal** law.
- Resonance-free regions / fractal-Weyl real-part bounds in terms of limit-set dimension δ:
  these are for **convex cocompact (infinite-area, no cusp)** surfaces (e.g. arXiv:2301.03023,
  2101.05757) and **infinite-covolume** Hecke groups (Bruggeman–Pohl arXiv:1909.11432; fractal
  Weyl arXiv:1810.04489) — a DIFFERENT geometric class from our cofinite/cusped G_q.
- GOE spectral statistics of non-arith Hecke triangles (Bogomolny–Schmit, Hejhal–Then) — about
  *eigenvalue* statistics, not *resonance* real-part geometry.

**What appears GENUINELY NEW (my web scan returned no source with these):**
1. A **certified numerical map** of the even-sector resonance real parts for the *cofinite*
   G_5 and G_7 at 400-bit Arb precision (resonances pinned to |det| ≈ 1e−15). Repeated searches
   ("numerical Re value computed", "real part 0.44", Pohl/Bruggeman/Strohmaier + numerical) return
   theory only; no public table of these Re-values. (Caveat: niche; could exist in a thesis.)
2. The **q-independent attractor band Re* ≈ 0.44** for the dissolved *bulk* (sub-claim A). This is
   a statement the Fermi-golden-rule literature does **not** make: FGR is about the infinitesimal
   *departure rate*, not the *finite-deformation accumulation locus*, and gives no reason for two
   different λ_q to share a bulk band. I found no source asserting q-independence of the dissolved
   real-part bulk for Hecke (or any cofinite) family.
3. The **partial-vs-full dissolution / tail ↔ arithmetic-proximity** signature (sub-claim B) tying
   the *count* of near-line resonances to distance from the nearest arithmetic Hecke point.

**Honest verdict on novelty:** the *frame* (even forms dissolve off Re=1/2) is fully owned. The
*specific quantitative geometry* — a universal sub-edge attractor band + an arithmetic-proximity
tail, on certified data — is, to the depth of this scan, **not in the literature**. It is a
conjecture about a phenomenon, strongest as sub-claim (A). It needs the 3-surface sweep (§4) before
it is more than a 2-point pattern.

---

## 6. CAVEATS (do not skip)

1. **n = 2 non-arith surfaces.** The whole universality claim rests on G_5 and G_7 only. The
   t-test (p=0.66) shows they are *consistent* with a shared band; it does NOT establish
   universality. q=9,11,12,13 are required and are the decisive experiment.
2. **Small samples per surface** (8 and 12 resonances, low Im). "Bulk accumulation as Im→∞" is an
   extrapolation; only the low spectrum is computed. A high-Im run could reveal the band drifts.
3. **The attractor 0.443 has no closed form** and is reported with a wide ±0.034 std. The band
   [0.42,0.47] is an honest empirical bracket, not a derived constant. Do not dress it as exact.
4. **q=3 anchor is the trivial-zeros line (Re=1/4), not a generic even cusp spectrum.** The "drift
   from 1/4 to ~0.44" narrative uses q=3's special arithmetic structure (ζ(2s) factorization) as
   the undissolved reference; a non-arithmetic-limit reference would need a different anchor.
5. **Even/odd bookkeeping is engine-dependent** (sign=+1 even for odd q=5,7; the populated sector
   flips for even q=8 — see `certified_g8.json`, which is odd-sector only). The conjecture is
   stated for odd q only; even q (8,10,12) needs the even-q builder `zeta_cert_rosen_even.py` and
   its sector convention re-checked before including q=12 as a sweep point.
6. Engine validated against an independent method (Hejhal point-matching) only for the **odd**
   on-line Maass zeros (`hejhal_g5_maass.json`); the **even off-line resonances** are
   self-consistent (Arb winding number + Newton) but lack a second independent solver. A genuine
   independent check (e.g. complex-scaling FEM on the surface) would harden the data.

---

## 7. Sources (web-verified this session)

- Bruggeman–Pohl, "Odd and even Maass cusp forms for Hecke triangle groups, and the billiard flow,"
  arXiv:1303.0528 (Ergodic Theory Dynam. Systems). [even/odd L^±_s framing; PS reformulation]
- Petridis–Risager, "Dissolving cusp forms: higher order Fermi's golden rules,"
  arXiv:1003.2820 (Mathematika 2013). [infinitesimal dissolution rate / FGR]
- Bruggeman–Pohl, "Eigenfunctions of transfer operators and automorphic forms for Hecke triangle
  groups of infinite covolume," arXiv:1909.11432 (Memoirs AMS 287/1423, 2023). [infinite-covolume —
  DIFFERENT class]
- "Fractal Weyl bounds and Hecke triangle groups," arXiv:1810.04489. [infinite-covolume fractal Weyl]
- "Improved fractal Weyl bounds ... convex cocompact hyperbolic surfaces," arXiv:2301.03023;
  "Uniform resonance free regions ...," arXiv:2101.05757. [convex cocompact, no cusp — DIFFERENT class]
- Phillips–Sarnak, "On cusp forms for cofinite subgroups of PSL(2,R)," Invent. Math. 80 (1985).
  [original dissolution] (UNVERIFIED this session — cited from memory of the standard reference.)
- Takeuchi, "A characterization of arithmetic Fuchsian groups," J. Math. Soc. Japan 27 (1975/77).
  [q∈{3,4,6,∞} arithmetic] (UNVERIFIED this session — standard.)

Data: `code/out/resonance_geometry.json`, `code/out/resonance_g7.json`,
`code/out/hejhal_g5_maass.json`, `code/out/certified_g8.json`.
Engine: `code/zeta_cert_rosen.py`, `code/run_resonance_g7.py`, `code/run_resonance_geometry.py`.

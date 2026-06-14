# Track B — Local-statistic arithmeticity criterion BEYOND Hecke triangle groups

**Date:** 2026-06-14. **Question (pipeline follow-on Path 3):** does a cluster-ceiling /
extreme-gap LOCAL statistic of a horocycle cross-section detect arithmeticity for a
NON-triangle cofinite Fuchsian group? Our Hecke dichotomy `B(q)=2 iff arithmetic` lives only
for triangle groups, where arithmeticity = `λ²∈ℤ` and the mechanism is integer cancellation in
the floor. Does that mechanism generalize?

## VERDICT: **NEGATIVE (well-supported), with one genuine structural insight.**

The cross-section cluster-ceiling statistic does **NOT** give a new arithmeticity detector beyond
triangle groups. The honest decomposition:

1. **The integer-cancellation mechanism is the SPECIAL (degree-2, totally-real) case of a known
   GENERAL arithmeticity criterion — the Luo–Sarnak Bounded Clustering Property (BCP) of the
   length/trace spectrum.** Our `λ²∈ℤ` is exactly "traces are algebraic integers whose Galois
   conjugates stay in [−2,2]" specialized to the trace field `ℚ(cos π/q)`. So the mechanism
   *does* generalize — but as an instance of an existing criterion (Luo–Sarnak 1994; Sarnak &
   Schmutz conjectures; Geninska–Leuzinger math/0609477), **not a new local detector**.

2. **That general criterion lives on the GEODESIC/HYPERBOLIC spectrum (closed-geodesic lengths =
   traces of hyperbolic elements), a DIFFERENT object from the BCZ/horocycle gap-product
   cross-section** (which sees the CUSP/parabolic structure). The cluster-ceiling of the horocycle
   section is NOT the bounded-clustering-of-traces statistic. So our cross-section statistic is the
   *wrong observable* to detect arithmeticity in general; it coincided with arithmeticity for
   Hecke only because both are controlled by the single scalar `λ`.

3. **The cleanest NON-triangle testable pair — congruence vs non-congruence finite-index
   subgroups of PSL(2,ℤ) — has NO arithmetic dichotomy to detect: ALL finite-index subgroups of
   PSL(2,ℤ) are arithmetic** (commensurable with PSL(2,ℤ), trace field ℚ; BCP holds for every one
   of them). The only available dichotomy at that commensurability class is congruence-vs-not, and
   that is invisible to BOTH detectors:
   - **Trace side:** the modular group has an *infinite family* of finite-index subgroups
     (including congruence ones) with the **identical trace set** (Schmutz-Schaller-type;
     arXiv:1312.7771). Identical trace set ⇒ identical BCP ⇒ the trace/length statistic cannot
     separate them, let alone separate congruence from non-congruence.
   - **Horocycle side:** Heersink (arXiv:1403.7502) shows the lifted BCZ gap distribution on the
     cover SL(2,ℝ)/H depends only on the **cusp widths** (the coset/permutation combinatorics),
     which are not the congruence property. Confirmed numerically below.

## Numerical confirmation (`code/track_b_congruence_detector.py`)

Matched index-7 pair (smallest index where non-congruence subgroups of PSL(2,ℤ) exist):

| subgroup | cusp widths | level N | monodromy | congruence? | min support edge | **cluster ceiling B** |
|---|---|---|---|---|---|---|
| profile (7,) | (7) | 7 | L₂(7), \|G\|=168 | **CONGRUENCE** (168 = \|PSL₂(ℤ/7)\|) | 0.00126 | **2** |
| profile (1,6) | (1,6) | 6 | \|G\|=42 | **NON-CONG** (42 ∤ 72 = \|PSL₂(ℤ/6)\|) | 0.00126 | **2** |

The lifted-BCZ cross-section (BCZ orbit `T(a,b)=(b,−a+⌊(1+a)/b⌋b)`, observable `P=ab`, coset
label transported by the index-7 coset permutation rep) gives **identical** cluster ceiling
(B=2) and identical support edge for the congruence and the certified-non-congruence subgroup.
**The statistic does not separate congruence from non-congruence.** (Independent non-congruence
certificate: monodromy order does not divide |PSL₂(ℤ/N)|, Wohlfahrt level N.)

> Note the B=2 here is NOT the Hecke ceiling — different observable normalization on the
> uplifted section. The load-bearing fact is *equality* across the congruence/non-congruence
> split, not the value.

## Why the integer-cancellation mechanism is genuinely special to λ²∈ℤ (the honest core)

- The Hecke dichotomy works because the trace field of `G_q` is `ℚ(λ_q)` of degree φ(2q)/2, and
  arithmeticity ⇔ that field is `ℚ` (λ²∈ℤ ⇔ q∈{3,4,6}, crystallographic restriction, Takeuchi
  1977). The "floor cancellation" is the degree-1 manifestation of the BCP norm-separation bound
  `1 ≤ |N_{K|ℚ}(t−s)|`. For higher-degree non-arithmetic groups the same bound is what makes
  traces *fail* to cluster (dense trace set) — the GENERAL detector — but it is a property of the
  hyperbolic length spectrum, NOT recoverable from a parabolic horocycle cross-section.
- Sarnak's Conjecture 1.1 ("BCP of trace set ⇒ arithmetic") is PROVEN for non-uniform lattices
  (Geninska–Leuzinger) and OPEN for cocompact; Schmutz's "linear trace growth ⇒ arithmetic" is
  open. So a *global* effective arithmeticity criterion already exists (trace-set growth /
  clustering, with a sharp 1/log/linear trichotomy, arXiv:2410.05223 Cor 1.5). Our Hecke result
  is a fully-worked, machine-verified *instance*, not a new criterion or a new *local* refinement.

## What WOULD be needed for a genuine positive (and why it is out of reach for this pipeline)

A true new result would be a **horocycle/parabolic LOCAL statistic that reconstructs the
hyperbolic-spectrum BCP** — i.e. detects arithmeticity from cusp-excursion data alone, for a
family where arithmeticity actually varies. The only cofinite families where arithmeticity varies
are: (a) triangle groups (DONE — ours), (b) Veech/Teichmüller eigenform loci (Track-3 verdict:
slope-gap complexity is monotone, does NOT jump at the arithmetic locus), (c) genuinely
non-arithmetic cocompact deformations (Riley/quasi-Fuchsian) — but those have no cusp, hence no
BCZ horocycle section at all. The horocycle-section route structurally **cannot** see the
hyperbolic-trace clustering that defines arithmeticity off the triangle-group line.

## Files
- `code/track_b_congruence_detector.py` (+ `.out`) — index-7 coset-diagram enumeration by
  cusp-width profile, monodromy/Wohlfahrt non-congruence certificate, lifted-BCZ cross-section
  cluster-ceiling comparison (congruence vs non-congruence).

## Do-not-rechase
- Cluster-ceiling / horocycle-section statistic as a NON-triangle arithmeticity detector: **DROP**
  (wrong observable — sees cusps/parabolics, not the hyperbolic trace clustering that = arithmeticity;
  congruence/non-congruence invisible to it AND to the trace set itself).
- "B=2 iff arithmetic" beyond triangle groups: **DROP** as a new local criterion — it is the
  degree-1 case of the existing Luo–Sarnak/Geninska–Leuzinger trace-set BCP criterion.
- Genuine residual (theory-partner only, niche): the Hecke result as the first *machine-verified*
  worked instance of the BCP-arithmeticity dichotomy — a Koyama-style collaboration framing, not a
  solo broad-reach target (consistent with pipeline_target_verdict_2026-06-14).

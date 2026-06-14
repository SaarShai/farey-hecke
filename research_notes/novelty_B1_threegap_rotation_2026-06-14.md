# Novelty probe B1 — Hecke G_q-BCZ corridor as elliptic rotation → three-gap / circle-rotation bridge

Date: 2026-06-14. WebSearch/WebFetch-hard novelty audit. Default prior: "likely known."

## Candidate bridge (B1)

Using the project-verified fact that the Hecke G_q-BCZ **last-branch corridor** block
monodromy `M_W` is an **elliptic rotation by θ=π/q** (rotation number 1/(2q), rational for
all q, finite order 2q; conserves the binary quadratic form `E = a² − λ·a·b + b²`,
λ=2cos(π/q)) — is there a NEW bridge from the Hecke gap dynamics to **circle-rotation gap
statistics** (three-gap / Steinhaus–Sós, Ostrowski, Sturmian, bounded-remainder sets) in the
Rosen/Hecke-CF setting for q>3, beyond the known q=3 Farey case and known Rosen-CF theory?

---

## VERDICT: PARTIAL-NOVEL, narrow scope (one genuinely-new observation; NOT a delivered bridge)

Split into the three key questions:

- **(Q1) Is the "corridor = rotation by π/q on a conserved binary quadratic form" structure for
  the G_q-BCZ map in the literature?** → **NO, appears new to this project (NOVEL, narrow).**
  None of the directly-governing papers carry it:
  - **Taha (1810.10668)**, the actual G_q-BCZ source, derives a *next-term / Stern–Brocot
    algorithm* and slope statistics for Λ_q = G_q(1,0)ᵀ. Its abstract and framing mention **no**
    elliptic element, **no** rotation, **no** conserved quadratic form, **no** three-gap /
    continued-fraction language. The corridor-block-monodromy-is-elliptic decomposition is not
    its object.
  - The classical/global BCZ map and its slope-gap cousins are described everywhere as
    **piecewise-Möbius / piecewise-affine** maps **renormalized by the geodesic flow**
    (hyperbolic character; return time R = 1/(ab)). The global map is **weakly mixing**
    (2403.14976) — i.e. the *opposite* of an elliptic/finite-order system. Nothing in this
    literature isolates an elliptic finite-order rotation on a sub-corridor.
  - "On binary quadratic forms and the Hecke groups" (math/9905157) builds a **reduction
    theory** of forms over ℤ[λ] (static arithmetic / Diophantine), not a dynamical
    rotation-of-a-conserved-form for a gap map.
  - The finite-order / trace∈algebraic-integers fact itself is the **classical crystallographic
    restriction** (older and more elementary than any of this); generic, not a bridge.

  So the *specific* packaging — last-branch corridor word W_q ↦ elliptic M_W (det 1, trace λ),
  rotating the state through a proper in-domain arc of width →0.1282π by π/q per block — is, on
  this search, **not previously written down**. (Consistent with the prior energy-route audit:
  it was flagged as the genuinely-new mechanism, with the trace-λ elliptic invariant itself
  classical but its *corridor incarnation* new.)

- **(Q2) Does it yield a NEW three-gap-type bridge specific to Hecke q>3, beyond q=3 Farey and
  known Rosen-CF theory?** → **NOT YET — this is the residue, currently UNCLAIMED in the
  literature AND not delivered here.** Repeated targeted searches found **no** "three-gap /
  three-distance theorem for Rosen / Hecke-λ continued fractions" for q>3. The classical
  three-gap↔CF↔BCZ↔space-of-lattices chain (Sós; Marklof–Strömbergsson 1612.04906) is **entirely
  the q=3 / SL(2,ℤ) story**. Rosen-CF theory exists richly (transcendence, CLT 2009.02047,
  Tong's spectrum, geodesic Rosen CF 1310.1585, Nakada α-CF cross-sections 1207.7299) but the
  *three-gap/Steinhaus statement itself* for q>3 is **absent**. So there is a real open slot —
  but B1 as stated does **not** fill it: an elliptic-rotation structure on ONE corridor is not
  the same as a three-distance theorem for the Rosen-λ orbit/rotation, and no derivation linking
  the two has been done. The bridge is *plausible and unclaimed*, not *established*.

- **(Q3) Is it subsumed (rotation-renormalization generic for triangle-group sections)?**
  → **PARTLY.** The *renormalization-by-flow* picture IS generic and well understood — but it is
  **geodesic** (hyperbolic) renormalization, not elliptic. The lateral sibling (Veech slope-gap
  for 2n-gon / Hecke-Veech surfaces: golden-L 1308.4203, 2n-gon 2109.04495, double-heptagon
  2508.19252, effective 2409.15660) has explicit piecewise-rational return maps with
  linearly-growing non-differentiability counts — but **none** frames a branch as elliptic /
  conserved-quadratic-form, and **none** invokes the three-gap theorem. So the elliptic-corridor
  observation is **not** subsumed by the generic picture; it is orthogonal to it.

---

## 4–6 closest papers

1. **Taha, "The BCZ Map Analogue for the Hecke Triangle Groups G_q"** — arXiv:1810.10668.
   THE governing object (the G_q-BCZ map this project uses). Next-term algorithm + Λ_q slope
   statistics; contains NO rotation/conserved-form/three-gap framing → the closest near-miss and
   the strongest evidence the elliptic packaging is new.
2. **Marklof–Strömbergsson, "The three gap theorem and the space of lattices"** —
   arXiv:1612.04906. The canonical three-gap↔lattice/horocycle↔BCZ renormalization explanation —
   but strictly the q=3 circle-rotation case. Defines the bar B1 would have to clear for q>3.
3. **(author varies), "Slope Gap Distribution of Saddle Connections on the 2n-gon"** —
   arXiv:2109.04495 (also golden-L 1308.4203; double-heptagon 2508.19252). Lateral sibling:
   Hecke-Veech slope-gap sections; piecewise-rational, NOT elliptic, no three-gap invocation —
   the place a rotation-of-conserved-form renorm would live if it existed, and doesn't.
4. **"BCZ map is weakly mixing"** — arXiv:2403.14976. Global BCZ map is weakly mixing ⇒ globally
   NOT elliptic/finite-order; leaves room only for a *sub-corridor* to be finite-order. Bounds
   any "the map is a rotation" overclaim — the elliptic structure must be corridor-local.
5. **(author varies), "On binary quadratic forms and the Hecke groups"** — arXiv:math/9905157.
   Reduction theory of binary quadratic forms over ℤ[λ_q]. Same algebraic object class
   (Hecke binary quadratic forms) but static/arithmetic, not the dynamical rotated-conserved-form
   of a gap map → shows the form algebra is known, the *dynamical rotation use* is not.
6. **Bugeaud–Hubert–Schmidt, "Transcendence with Rosen continued fractions"** (EMS) +
   "A Central Limit Theorem for Rosen Continued Fractions" arXiv:2009.02047 + "Geodesic Rosen
   continued fractions" arXiv:1310.1585. State-of-the-art Rosen/Hecke-λ-CF theory — rich, but
   demonstrably contains NO three-gap/Steinhaus statement for q>3.

---

## Narrowest genuinely-new residue

The only defensible new object is **(R)**: *the last-branch G_q corridor word W_q has an
elliptic finite-order (order-2q) block monodromy M_W that rotates the state by π/q on the
conserved binary quadratic form E, and the in-domain corridor is a proper arc of that rotation
(width → 0.1282π).* This corridor-local elliptic-rotation-of-a-conserved-form framing of the
G_q-BCZ map is not in Taha, the slope-gap literature, or the Hecke-form-reduction literature.

It is, however, **a structural observation, not yet a theorem about gaps**. To become a real
bridge it would need a derivation showing the corridor rotation *produces a three-gap-type / few-
distance partition of the Rosen-λ orbit for q>3* — exactly the slot the literature leaves open
(Q2). That derivation has not been done here or anywhere found. The numerics/Lean to date use
(R) to drive the **uniform onset lower bound** (arc-width dwell ∝ q), which is a *support-edge /
extremal* statement, NOT a gap-counting (three-distance) statement — a category gap that must be
crossed before claiming a three-gap result.

## One honest sentence

It is mostly the known BCZ-renormalization picture reframed — with **one genuinely new,
narrow twist**: a corridor-local *elliptic* (rotation-by-π/q, conserved-quadratic-form) reading
of the G_q-BCZ map that the literature does not carry; but the advertised three-gap/circle-
rotation *bridge* itself is, as stated, an unclaimed-and-undelivered conjecture (real open slot
for q>3, not yet bridged), not an established new theorem.

# V25 dispatch note — U3 transport

**Date:** 2026-08-16. **Lane G.** **Project ID:** `07777c9a-bdad-4302-88ec-d446941c1821`.
**Task ID:** `ba4afdec-9c23-4909-824f-19602ea2fdfb` (QUEUED at submit).
Toolchain `leanprover/lean4:v4.28.0`, Mathlib pinned `v4.28.0` — same as v24.

**Obligation.** U3 (`LAW_T2_DETERMINANT.md` §5.2 = C14 = G6/N2): a scattering
pole of `det Φ_θ` at `s_∞ = ρ₁/2` transports to a Selberg-zeta zero of order 2
for `Γ_θ`. Named "textbook-shaped" and recommended lane #2 in
`LAW_SH_EFFECTIVIZATION_SKELETON.md` §7.

## What was sent (13 statements, `U3Transport.lean`)

Order arithmetic:

1. `meromorphicOrderAt_reflect` — `ord_{s₀} Z(1-·) = ord_{1-s₀} Z`.
2. `meromorphicOrderAt_affine` — the same for any `s ↦ a s + b`, `a ≠ 0`
   (used for `Λ(2s-1)`, `Λ(2s)`).
3. `meromorphicOrderAt_eq_of_unit_factor` — Lemma U3-B, algebraic half: an
   analytic non-vanishing factor does not move the order.
4. `meromorphicOrderAt_div` — `ord(F/G) = ord F - ord G`, both finite.
5. `zero_of_meromorphicOrderAt_pos` — positive order at an analytic point is a
   zero.

The transport chain:

6. `transport_order` — **THEOREM U3, algebraic core.** From
   `Z(1-s) = κ(s)Z(s)` near `s₀`, `κ = c·φ` with `c` a unit, `ord_{s₀} φ = -m`
   (`m ≥ 1`), and `ord_{1-s₀} Z = 0`: conclude `ord_{s₀} Z = m`.
7. `transport_order_ge_two` — the `m ≥ 2` corollary in the form the Hurwitz step
   of `(T2′)` §3.2 consumes.

`Γ_θ` divisor bookkeeping (`det Φ_θ = g² E`, `g = Λ(2s-1)/Λ(2s)`):

8. `order_detPhi` — `ord(g²E) = 2(ord Λ(2s₀-1) - ord Λ(2s₀))` for `E` a unit.
9. `order_detPhi_at_pole` — at `s₀ = ρ/2` (denominator vanishes to order `m`):
   pole of order exactly `2m`. This is (T1).
10. `order_detPhi_at_conjugate` — at `w = (1+ρ)/2` (numerator vanishes to order
    `m`): zero of order exactly `2m`. This is §3.3, the form in which the
    literature states the transport.
11. `conj_reflect_of_re_half` — `Re ρ = 1/2 ⇒ 1 - conj(ρ/2) = (1+ρ)/2`, i.e.
    identity (3.1), the step that avoids importing "`φ` is real on `ℝ`".

Assembled:

12. `anchor_order` — (U3-θ): `ord_{s₀} Z = 2m`.
13. `anchor_zero` — `Z s₀ = 0` and `ord ≥ 2`.

**Pre-dispatch check.** The file elaborates against the pinned Mathlib with
exactly 13 `declaration uses 'sorry'` warnings and **no errors** (checked in the
already-built `projects/aristotle_dispatch_v22` tree, identical toolchain/rev).
No `sorry` appears inside any statement.

## What remains analytic (not sent) — see `SKIPPED.md`

* **S1** the Selberg functional equation `Z(1-s) = κ(s)Z(s)` in Teo's closed form
  (Barnes `Γ₂`, `sin`-power elliptic factor, parabolic `Γ`-ratio). `CITATION`.
* **S2** Lemma U3-B's concrete content: those factors have **real** divisors,
  hence are units at non-real `s₀`. `PROVED` on paper, factor by factor.
* **S3** Lemma U3-A: `Z_Γ` holomorphic and zero-free on `Re s > 1/2`, `Im s ≠ 0`
  (7-item divisor list, FJS 2021). `CITATION`.
* **S4** the identity `det Φ_θ = g²E` and the divisor of `E`. `PROVED` (T1).
* **S5** the analytic properties of `Λ`/`ζ` (zero orders, pole locations,
  simplicity of `ρ₁`, `Re ρ < 1`). `CITATION`.
* **S6** the Hurwitz/Vitali step and everything `q`-uniform (U1, U2b, U5).
* **S7** library errands V1–V3 (Hejhal p. 498, Venkov p. 49, Teo journal
  numbering). Non-blocking.

## Status effect

If the task returns clean, U3's **bookkeeping** is machine-checked and the
remaining U3 content is exactly the citation set S1–S5 — i.e. U3 stays
`CLOSED-BY-CITATION` in the lane notes, with the algebraic step now
`MACHINE-VERIFIED` rather than hand-checked. **No change to U1**, which remains
the crux. **No novelty claim** — the transport is 1980s classical
(`LAW_U3_TRANSPORT.md` §6 V4).

Ledger line for `plans/wayfinder/rh-goals/MAP.md` (to be appended by the owner,
not by this lane): *"2026-08-16 — U3 algebraic core dispatched to Aristotle
(project `07777c9a-bdad-4302-88ec-d446941c1821`, 13 order-arithmetic statements);
analytic remainder S1–S7 recorded in `projects/aristotle_dispatch_v25/SKIPPED.md`."*

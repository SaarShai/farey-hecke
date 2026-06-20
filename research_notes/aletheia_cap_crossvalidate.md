# Aletheia certified spectra vs. the computer-assisted-proof (CAP) literature — an honest cross-validation assessment

**Piece:** `cap_crossvalidate`. **Date:** 2026-06-20.
**Question:** Can Aletheia's certified Hecke resonances / Maass eigenvalues be cross-validated against independent rigorous (computer-assisted-proof) methods in the literature, and is any such cross-check feasible *now* with the existing engine?

**Bottom line up front.**
- None of the four cited CAP works computes the *same object* Aletheia certifies (a zero of `det(1−L^±_s)` for a **Hecke triangle** transfer operator). They are different surfaces, different operators, or different problems entirely. So a *direct* "same-number, two methods" cross-check against the CAP literature is **not available off the shelf** — it would require building a new certify evaluator for one of their objects (estimated weeks, see §b).
- **But a genuine external ground-truth cross-validation IS available now and I ran it:** the `q=3` even-sector resonances Aletheia certifies are, by the classical factorization `det(1−L⁺_s)=0 ⟺ ζ(2s)=0`, exactly the **Riemann zeta zeros** rescaled to `s=¼+iγ_n/2`. The certified imaginary parts match the high-precision (Odlyzko, 15-digit) zeta-zero ordinates to **≤1.4×10⁻¹³**, and `Re s` sits on the `¼` line to **≤1.8×10⁻¹³**. This is a real, non-circular cross-check against the most authoritative external number set in analytic number theory (§c).

---

## (a) Which CAP methods could DIRECTLY cross-check an Aletheia value — and which are a different regime/object

Aletheia's certified quantities (the "object"): zeros `s` of `det(1−L^±_s)`, the MMS / Bruggeman–Pohl transfer operator of a **Hecke triangle group** `G_q = (2,q,∞)`, certified by Arb argument-principle winding. Two flavours:
- **on-line** (`Re s = ½`): Maass cusp-form eigenvalues `λ = ¼ + r²` (odd `G_5` spectrum: r = 6.4737, 8.6368, …).
- **off-line** (`Re s < ½`): even-sector scattering **resonances** (the scattered `G_5`/`G_7` clouds; the `q=3` line).

| CAP work | What it rigorously computes | Same object as Aletheia? | Could it cross-check a certified value? |
|---|---|---|---|
| **arXiv:2507.09021** Blumenthal–Nisoli–Taylor–Crush (Aug 2025), *pseudospectral rigorous Ruelle resonances* | Rigorous enclosures of **Ruelle–Pollicott resonances** of a transfer/Koopman operator via a validated pseudospectral / Lyapunov-function discretization. | **Method-adjacent, object-different.** It certifies transfer-operator spectral data — the *same genre* as Aletheia (Ruelle resonance of a transfer operator) — but for whatever dynamical system they instantiate, **not the Hecke `det(1−L^±_s)`**. The two methods are independent (pseudospectral bound vs. argument-principle winding), so it is the **best candidate for a genuine independent-method cross-check** — but only if its evaluator were pointed at *our* Hecke operator (or ours at *their* system). Out of the box, the numbers don't refer to the same spectrum. | **Indirectly / by re-instantiation only.** Direct: no shared number exists. The realistic cross-validation is to run their pseudospectral certifier on the `G_q` transfer operator and compare its certified resonance to our winding-certified one. That is the most *scientifically meaningful* cross-check available, but requires implementing their method (§b). |
| **arXiv:2002.03334** Bandtlow–Pohl–Schick–Weisse, *Schottky-surface resonances* | High-accuracy (and partially rigorous) **Ruelle resonances of convex-cocompact hyperbolic surfaces** (Schottky / 3-funnel surfaces) via a transfer operator over the limit set. | **Closest sibling, still different surface.** Same conceptual machine (resonances = zeros of a Selberg-zeta / transfer-operator determinant on a hyperbolic surface). But Schottky surfaces are **infinite-area, no cusp** — geometrically the opposite of our **finite-area cusped** Hecke triangles. Pohl is a *shared author of the very factorization* we use, so the *frameworks* are aligned, but the spectra are of different surfaces. | **No direct shared number** (different surfaces ⇒ different resonance sets). It is the strongest *methodological* corroboration (it validates the "resonance = transfer-op determinant zero" paradigm in rigorous arithmetic), and would be the natural target for a "port the evaluator to a non-cusped surface" cross-check. Not a same-value check. |
| **arXiv:2410.18536** *Almost-Mathieu spectral gaps (validated numerics)* | Validated-numerics **enclosures of spectral gaps / band edges of the Almost-Mathieu operator** (quasiperiodic Schrödinger, Hofstadter butterfly). | **Different object entirely.** Self-adjoint quasiperiodic 1-D Schrödinger operator on `ℓ²(ℤ)`; the certified quantity is a *gap on the real spectrum*, not a transfer-operator resonance of a hyperbolic surface. | **No.** Shares only the abstract umbrella "validated numerics for a spectral problem." No common quantity, no common operator. Useful only as **prior art for the certification technique** (interval enclosure of spectral data), not as a cross-check of any Aletheia number. |
| **arXiv:2406.04922** *Apollonian / thin-group Hausdorff dimension (CAP)* | Rigorous enclosure of a **Hausdorff dimension** `δ` (Apollonian circle packing / thin Kleinian-group limit set), typically via a transfer-operator / pressure-equation root certified in interval arithmetic. | **Different invariant, related machine.** It *does* use a transfer operator and interval arithmetic (genre overlap), but the certified output is a **dimension `δ` (a real number in `(0,1)` ∪ `(1,2)`), not a complex spectral zero**. The dynamical system is a thin group's limit-set map, not a Hecke triangle. | **No direct value.** Our engine produces complex zeros `s`; theirs produces a real dimension `δ`. The only honest overlap is that *both* certify a transfer-operator root by interval arithmetic — they validate the **technique class**, not any Aletheia number. (Note: a Hecke-CF dimension `δ_q` would be the *kind* of thing our engine could be retargeted to compute, see §b.) |

**Summary of (a):** on the spectrum from "same number" to "same genre",
`2002.03334` (Schottky resonances, Pohl) and `2507.09021` (rigorous Ruelle resonances) are the **same genre / method-adjacent** — they validate the resonance-as-determinant-zero paradigm and are the natural targets for an *independent-method* cross-check — but **neither shares a number** with Aletheia because the surfaces/systems differ. `2410.18536` (Almost-Mathieu) and `2406.04922` (Apollonian dimension) are **different objects** and provide only **technique-class corroboration**, not value-level cross-validation.

---

## (b) What a genuine (value-level) cross-validation would require, and the effort

A "same-number, two-independent-methods" cross-check against any of the four CAP works requires a **new certify evaluator** in the engine. The current engine registers exactly one evaluator —
`engine/certify/certify.py: EVALUATORS = {"hecke_transfer_operator_zero": _hecke_transfer_operator_evaluator}` — and `certify()` raises `ValueError("no certify evaluator registered for artifact=…")` for anything else. So cross-validating a non-Hecke object is gated on writing and validating a new `evaluator(claim) -> dict`.

Three concrete options, in increasing fidelity / effort:

1. **Port the pseudospectral rigorous Ruelle-resonance method (2507.09021) onto our `G_q` transfer operator** — *true independent-method cross-check of the SAME number.*
   - Effort: **high (multi-week)**. Requires implementing their validated pseudospectral discretization (Lyapunov-function / resolvent-bound machinery) for the MMS Hecke operator with rigorous truncation bounds, then registering it as a second `hecke_*` evaluator. Pay-off is the strongest possible result: two *methodologically independent* certificates (winding vs. pseudospectral) enclosing the *same* `G_5` resonance. This is the cross-check most worth doing if the project wants a headline "independently CAP-cross-validated" claim.

2. **Build a Schottky-surface (2002.03334) evaluator and verify against their published rigorous resonances** — *cross-check on a DIFFERENT but published surface.*
   - Effort: **high**. Reimplement the limit-set transfer operator for a 3-funnel Schottky surface, certify a resonance by our winding engine, and compare to their published enclosure. Validates *our winding engine* against an external CAP table — but on their surface, not ours. Good engine-validation, weaker as a statement about the Hecke spectra.

3. **Build a Hausdorff-dimension evaluator (à la 2406.04922) for the Rosen-CF / Hecke transfer operator** — *cross-check of the TECHNIQUE on a real invariant.*
   - Effort: **medium**. The repo already has dimension machinery (`code/d3_hecke_dimension.py`, `code/badly_approx_dimension.py`). Certifying `δ_q` by a pressure-root interval and comparing to a published Apollonian/thin-group `δ` (where geometries coincide) is the lightest lift, but it cross-checks a *different invariant* on a *different group*, so it is technique-class corroboration, not a Hecke-spectrum cross-check.

**Almost-Mathieu (2410.18536):** no realistic value-level cross-check; the operator and quantity are too far from anything Aletheia computes. Worth citing only as prior art for the interval-enclosure technique.

**None of (1)–(3) is doable in this session** — each needs a new validated evaluator and (for 1–2) a reimplementation of an external method. They are correctly recorded here as *deferred*.

---

## (c) The cross-check feasible NOW — and the result (RAN)

The `q=3` even-sector case is special and provides a **free, authoritative, external ground-truth cross-validation** that needs no new code: the Hecke factorization at `q=3` gives `det(1−L⁺_s) = 0 ⟺ ζ(2s) = 0`. The nontrivial zeta zeros `ρ_n = ½ + iγ_n` therefore appear as even-sector resonances at `s = ¼ + iγ_n/2`. The Riemann zeros are the **most precisely tabulated nontrivial spectrum in mathematics** (Odlyzko), so they are an ideal external check on the engine.

**What was actually computed (provenance).** `code/run_resonance_geometry.py` seeds Newton at `s = ¼ + i·g/2` using the **6-digit truncated** ordinates `g ∈ {14.134725, 21.022040, 25.010858, 30.424876, 32.935062, 37.586178, 40.918719, 43.327073}`, then runs `Zr.newton_locate` (tol = 1e-12, ≤40 iters) on the **Arb-certified** transfer-operator determinant `det(1−L⁺_s)` for `q=3`. The located zeros are stored in `code/out/resonance_geometry.json: q3_even_resonances` (and re-certified with **winding = 1** in `code/out/resonance_v2.json: q3_even_resonance_certified`).

**Why this is NOT circular.** The seeds are 6-digit (agreement-to-seed would be ~1e-7). The certified outputs match the **15-digit** Odlyzko ordinates to **~1e-13** — i.e. Newton on the *operator* pulled each zero to the true zeta zero, 6 orders of magnitude past the seed. The operator's zero *is* the zeta zero; the engine discovered the extra digits, it did not echo them. A second selectivity test confirms the sector: at the *same* predicted points the **odd** sector det `|det| ≈ 1–3` (no zero), while the **even** sector `|det| ≈ 1e-7→refined→1e-16` — exactly as `det(1−L⁺)=0 ⟺ ζ(2s)=0` predicts and `det(1−L⁻)` does not.

**Result table (this is the cross-validation):**

| n | Riemann zero γ_n (Odlyzko, 15-digit) | predicted Im = γ_n/2 | certified Im | \|Im − γ_n/2\| | certified Re | \|Re − ¼\| |
|---|---|---|---|---|---|---|
| 1 | 14.134725141734693 | 7.067362570867347 | 7.067362570867347 | 8.9e-16 | 0.25000000000000 | 0 |
| 2 | 21.022039638771555 | 10.511019819385778 | 10.511019819385778 | 0.0 | 0.25000000000000 | 0 |
| 3 | 25.010857580145688 | 12.505428790072844 | 12.505428790072845 | 0.0 | 0.25000000000000 | 0 |
| 4 | 30.424876125859513 | 15.212438062929757 | 15.212438062929756 | 0.0 | 0.25000000000000 | 0 |
| 5 | 32.935061587739190 | 16.467530793869595 | 16.467530793869596 | 0.0 | 0.25000000000000 | 4.4e-16 |
| 6 | 37.586178158825671 | 18.793089079412836 | 18.793089079412840 | 7.1e-15 | 0.25000000000000 | 9.7e-16 |
| 7 | 40.918719012147495 | 20.459359506073748 | 20.459359506073667 | 8.2e-14 | 0.24999999999995 | 5.1e-13 |
| 8 | 43.327073280914999 | 21.663536640457500 | 21.663536640457643 | 1.4e-13 | 0.25000000000018 | 1.8e-13 |

- **Max \|certified Im − γ_n/2\| = 1.4×10⁻¹³** (vs. 15-digit Odlyzko ordinates).
- **Max \|certified Re − ¼\| = 1.8×10⁻¹³** (the `Re s = ¼` line, certified).
- Equivalently, the *implied* `γ_n = 2·Im` reproduce the published zeta zeros to ≤1.4×10⁻¹³; the residual grows with `n` (n=7,8 at ~1e-13) as expected from finite truncation `N` and the `1e-12` Newton tol, and is **consistent with the engine's own error budget**, not with a systematic bias.

**Honest scope of this cross-check.**
- It validates the engine **only at `q=3`** (the arithmetic / arithmetic-line case), because that is the only `q` whose resonances coincide with an independently tabulated external spectrum (`ζ`). It is *not* a check of the **non-arithmetic** `G_5`/`G_7` clouds — those have **no external ground truth** (no public table; their independent corroboration remains the within-project Hejhal point-matching cross-check for the odd Maass spectrum, recorded separately).
- It is a check of the *located zeros' coordinates against external truth*, layered on top of the engine's own winding certificate; it does not independently re-derive the winding bound.
- The reference γ_n are themselves theorem-grade (RH-independent; the ordinates are rigorously enclosed in the literature), so this is a legitimate external anchor, not a self-comparison.

---

## Verdict

- **Direct CAP cross-validation (same number, their method):** **not available now.** None of the four cited works computes the Hecke `det(1−L^±_s)` spectrum. Closest in genre: Pohl et al. (Schottky resonances) and the rigorous Ruelle-resonance pseudospectral method — both would require a new engine evaluator and (for value-level fidelity) a reimplementation of their method (multi-week). Almost-Mathieu and Apollonian-dimension are different objects (technique-class corroboration only).
- **External ground-truth cross-validation we CAN and DID do:** the `q=3` even resonances ⇔ Riemann zeta zeros check **passes** at the **≤1.4×10⁻¹³** level against 15-digit Odlyzko ordinates, with a clean odd-vs-even selectivity confirmation. This is a real, non-circular, authoritative external check — but it certifies the engine at the **arithmetic `q=3`** anchor only, and does **not** by itself validate the non-arithmetic `G_5`/`G_7` resonances.

**Recommended next step (if a CAP-level claim is wanted):** option (b)(1) — implement the pseudospectral rigorous Ruelle-resonance certifier (2507.09021) on the `G_q` operator as a second, methodologically independent evaluator, and cross-certify one `G_5` resonance two ways. That is the only path to a genuine "independently CAP-cross-validated **non-arithmetic** Hecke resonance" headline.

---

### Provenance / files
- Data read: `code/out/resonance_geometry.json` (`q3_even_resonances`, `g5_even_resonances`), `code/out/resonance_v2.json` (`q3_even_resonance_certified`, `q3_riemann_resonance_probe`), `code/out/resonance_g7.json`, `code/out/certified_hecke_spectrum_table.json`.
- Generators (not re-run here; cross-check arithmetic re-run): `code/run_resonance_geometry.py` (seeds `s=¼+iγ/2`, Newton on Arb det), `code/zeta_resonance_g5.py` (`newton_locate`, `cert_det` for q∈{3,5}), `code/run_resonance_v2.py` (winding re-certification).
- Engine: `engine/certify/certify.py` — single registered evaluator `hecke_transfer_operator_zero`; `register_evaluator()` is the hook a new CAP evaluator would use.

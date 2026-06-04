# Q5 — Adversarial self-review of D3_NOTE_DRAFT.md

Hostile-referee pass. Posture: assume overclaim until proven otherwise.
Verdict per claim: PASS / DOWNGRADE / CORRECT.

## Finding 1 — G0 novelty framing  [PASS, with sharpened honesty]
"New as a formula, web-confirmed absent, elementary." Defensible, but make the
triviality explicit: the FF Farey–Mertens identity is a **2-line corollary** of
Carlitz's evaluation of the function-field Ramanujan sum
`c_g(m)=Σ_{e|gcd(g,m)}q^{deg e}μ(g/e)` summed over `deg g≤D`. Its absence from
the literature reflects that it is **too elementary to publish alone**, not
that it is deep. Note already says "elementary"; add the Carlitz one-liner so no
reader mistakes absence-from-literature for depth. Applied.

## Finding 2 — §6 CONFLATION  [CORRECT — a real overclaim by me]
The draft wrote: *"By the duality, `C_FF` and the G2(a) twisted variance are —
up to normalization — that same [Keating–Rudnick] object."* **This is wrong and
is exactly the novelty/citation-inflation failure mode the project warns about,
committed by me.** Two *different* quantities were conflated:

- **C_FF (§5)** = the **untwisted** Mikolás/Parseval second moment
  `lim q^D Φ_D^{-1}(q−1)Σ_{m monic}A_D(m)²q^{-2deg m}`. By G0,
  `A_D(m)=(1−q)σ_A(m)` for `deg m<D`, so this is, in the limit, an **explicit
  convergent `σ_A²` Euler-product constant** — rational in `q`, **elementary,
  no characters, no fluctuation, NOT Keating–Rudnick-deep**. It is the FF
  analogue of the classical Mikolás `W(N)` bilinear form, which here collapses
  to a zeta value because `M_A` is constant. This is *less* than dictionary-
  tier: it has no arithmetic depth at all.
- **The G2(a) twisted variance** `Φ_A(Q)^{-1}Σ_{χ≠χ_0}|M_A(n,χ)|²` = the
  Möbius-in-arithmetic-progressions variance — *this* is the Keating–Rudnick /
  `U(N)` / Katz object (via the §6 orthogonality duality, which is itself
  correct — re-derived below).

These are **distinct objects** with distinct reasons for being "not new":
C_FF is *elementary*; the twisted variance is *KR*. The duality connects the
twisted variance to KR; it does **NOT** make C_FF a KR object. CORRECTED in the
note: §5/§6 rewritten to separate them; the headline verdict
(dictionary-tier, no new mathematics) is **unchanged and in fact strengthened**
(the untwisted second moment is shallower than I claimed).

### Re-derivation check of the §6 orthogonality duality  [PASS — proof correct]
`Σ_{χ mod Q} χ(f)χ̄(g) = Φ_A(Q)·1_{f≡g (Q),(f,Q)=1}` ⇒
`Σ_χ|Σ_{(f,Q)=1}α(f)χ(f)|² = Φ_A(Q)Σ_{a∈(A/Q)^*}|Σ_{f≡a}α(f)|²`.
Dropping `χ_0` ↔ centering by the mean ⇒ residue-variance =
`Φ_A(Q)^{-1}Σ_{χ≠χ_0}|M_A(n,χ)|²`. Correct, elementary, citation-free. PASS.

## Finding 3 — §5 label inflation  [DOWNGRADE]
Draft tagged "[PROVEN-exact, decisive] R_D converges to C_FF(q)". The
*numbers* (≈9.4/17/37) are a **[NUMERICAL] geometric extrapolation** (dR ratio
≈0.70 for q=2 ⇒ tail ≈+1.3 ⇒ limit ≈9.3). Existence + rationality of the limit
is *plausible* (M_A piecewise-constant ⇒ the q^D-normalized bilinear sum should
satisfy a fixed rational recurrence) but **not yet proven** — that is exactly
Q6. DOWNGRADE to: "[NUMERICAL] R_D converges (dR geometric); rigorous existence
+ exact closed form of C_FF(q) PENDING Q6 (σ_A² Euler product / bilinear-
Mikolás)." Applied.

## Net
Headline verdict UNCHANGED and strengthened: D3 = exact unconditional
dictionary/model, **no new mathematics**; the untwisted constant is *elementary*
(not even KR-deep), the twisted variance *is* KR. One genuine self-inflicted
overclaim caught and corrected (Finding 2) — the adversarial pass did its job.
Remaining rigor gap: Q6 (closed form / convergence proof of C_FF(q)).
Citation honesty intact: KR still [CITATION-UNVERIFIED at theorem granularity];
the verdict does not depend on it (duality is self-proved).

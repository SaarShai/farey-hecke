# DRAFT email to Koyama — uniform bound q ≥ 22 (the open frontier)

Status: DRAFT for review. Tone matches the existing thread (research_notes/koyama_correspondence_log.md).
Honest: reports a machine-verified REDUCTION + a precisely-characterized open residual, NOT a closed theorem.

---

Dear Koyama,

A substantial update on the uniform lower bound `X_Ω(q) ≥ 1/λ_q³` — the open frontier you flagged —
and where it now genuinely stands.

**Your energy route was the right instinct, and it paid off twice.** Coupling the conserved energy
`E = c_n² + c_{n+1}² − λ c_n c_{n+1}` with the escape-of-mass into the cusp is now a *machine-verified
reduction* of the q ≥ 22 confinement, not just a heuristic. Two things came out of it:

1. A clean **demystification**: the onset `≥` bound does **not** inherit the resonance/parity
   obstruction that governs the exact cluster ceiling B(q). It needs only that the corridor rotation
   reaches the super-threshold arc *once* within q steps — a resonance-independent fact. So the
   onset bound survives the resonances {23, 61, …} even though B(q)'s exact value does not. (One
   refinement to your phrasing: the operative mechanism is a *no-dwell / measure* argument, not a
   uniform spectral gap — we checked, and the transfer-operator gap actually *shrinks* with q. The
   energy/escape-of-mass picture is the correct one; the gap reading is not.)

2. A concrete proof architecture, all formalized in Lean 4 and machine-checked sorry-free.

**The technical state, precisely.** The historical q ≤ 21 cap was purely a *fixed window length*
in the no-sustained argument. We generalized it to a q-dependent window `L_blk(q) = ⌈33q/256⌉ + 2`
(staying entirely on the genuine multi-branch map, so the deep-mid ejection and the invariant
measure are unaffected). The hard analytic ingredient — the uniform arc-coverage margin
`δ_∞ = 5.77·10⁻⁵ > 0`, interval-certified through q = 10000 — is fully proved and axiom-clean, as
is the corridor product/observable realization `a·b = C0 + R cos(φ + 2kθ)` on the conserved
`E`-ellipse (the exact analog of the energy-route identity).

**What remains is now a single, sharply-identified residual** — and we *proved* what it is not.
The whole q ≥ 22 bound reduces to one in-domain "radius forcing" datum on the corridor orbit,
`r²·B_λ²·cos²(|μc| + H) ≥ 1`. We then proved a small but decisive *negative*: this datum is **false
unconditionally** as currently interfaced, because the realization bridge threads only positivity
and *drops the in-domain residency* `D_{N+j} > 1` — which is exactly the information needed (and is
available in the corridor hypotheses). So the remaining task is not a missing estimate but an
*interface re-architecture*: thread the in-domain residency through the realization so the per-orbit
radius bound becomes uniform in q. This is precisely the kind of place your thermodynamic-formalism
/ transfer-operator viewpoint might cut cleaner than our hands-on corridor bookkeeping — I would
value your eye on it.

**Net.** The q = 5..21 equality stands exactly as before (the paper's cornerstone is untouched).
For q ≥ 22 we now have a machine-verified *reduction* down to that single residency-threading step,
with a proof that the naive route cannot close it. I think this is a genuine step toward the all-q
statement, and it isolates the one piece that needs a real idea rather than more bookkeeping.

I'll keep this corridor section firming up at a comfortable pace over the summer; no rush on your
side, and I know the `−1`-dominance repair under the `p^{-1/2}` weighting is your focus. Happy to
send the Lean files for the L_blk window and the realization identities whenever useful.

With warm regards,
[name]

---

## Notes for us (not for the email)
- Everything above is `lake build`-verified axiom-clean; cite research_notes/UNCONDITIONAL_REDUCTION_2026-06-20.md.
- The one claim to keep honest: q≥22 is a REDUCTION, not a theorem. Do not let the prose imply closure.
- If he asks for files: LblkWindow.lean, CorridorProductRealization.lean, WindowRealizeClose.lean,
  CorridorCollapse.lean, HpinClose.lean (all in projects/aristotle_dispatch_v15/uniform_q5to18/),
  + L1bArcCoverage.lean (B1_target/fcorr_lb).
- The residual to pose to him: thread `D_{N+j}>1` (in-domain residency) through
  `windowProductRealizes_corridor` so `hpin`'s radius forcing holds uniformly — the
  `hpin_not_unconditional` negative shows why the current interface fails.

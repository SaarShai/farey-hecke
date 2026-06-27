# DRAFT email to Koyama — uniform bound q ≥ 22 (the open frontier)

Status: DRAFT for review. Tone matches the existing thread (research_notes/koyama_correspondence_log.md).
Honest: reports a machine-verified REDUCTION + a precisely-characterized open residual, NOT a closed theorem.
Tightened 2026-06-27 (architecture-level, less Lean notation; added the dichotomy link).

---

Dear Koyama,

A substantial update on the uniform lower bound `X_Ω(q) ≥ 1/λ_q³` — the open frontier you flagged.

**Your energy route was the right instinct.** Coupling the conserved energy
`E = c_n² + c_{n+1}² − λ c_n c_{n+1}` with the escape-of-mass into the cusp is now a *machine-verified
reduction* of the q ≥ 22 confinement, not just a heuristic — formalized in Lean 4, sorry-free. It also
clarified the mechanism: the onset `≥` bound does **not** inherit the resonance/parity obstruction that
governs the exact cluster ceiling B(q). It needs only that the corridor rotation reaches the
super-threshold arc *once* within q steps — a resonance-independent fact, so the bound survives the
resonances {23, 61, …} even though B(q)'s exact value does not. (One refinement to your phrasing: the
operative mechanism is a no-dwell / measure argument, not a uniform spectral gap — the transfer-operator
gap in fact *shrinks* with q. The energy / escape-of-mass picture is the right one.)

**Where it stands.** The old q ≤ 21 cap was purely a fixed window length; generalizing it to a
q-dependent window (still on the genuine multi-branch map, so the invariant measure is untouched)
reduces the whole q ≥ 22 bound to a **single, sharply-identified residual** — one in-domain
radius-forcing datum on the corridor orbit. And we proved a small but decisive *negative*: the naive
form of that datum is false, because the realization bridge currently threads only positivity and drops
the in-domain residency that is exactly the missing information. So the remaining task is not a missing
estimate but an interface re-architecture — and it is precisely where your thermodynamic-formalism /
transfer-operator viewpoint may cut cleaner than our hands-on bookkeeping. I would value your eye on it.

**Net.** The q = 5..21 equality stands exactly as before (the paper's cornerstone is untouched); for
q ≥ 22 we now have a machine-verified *reduction* to that one residency-threading step, with a proof
that the naive route cannot close it. A genuine step toward the all-q statement, isolating the one piece
that needs a real idea rather than more bookkeeping.

**A tool that may be useful to you and your group — "Aletheia."** Alongside the bound I have been
building a small engine that rigorously certifies spectral data for Hecke triangle groups: using
interval (Arb) arithmetic it encloses zeros of the Bruggeman–Pohl transfer-operator determinant
`Z(s) = det(1−L⁺_s)·det(1−L⁻_s)` by a verified winding number — a rigorous proof that exactly one simple
zero lies in a given box. So far: (i) what appears to be the first interval-certified spectrum table for
the *non-arithmetic* `G_5` and `G_7` (Maass eigenvalues and even-sector resonances); (ii) a ground-truth
check at `q = 3`, where it recovers `det(1−L⁺_s) = 0 ⟺ ζ(2s) = 0` and reproduces the first Riemann zeros
to `≤ 1.4×10⁻¹³`; and (iii) — the part I think will interest you — a **spectral face of your arithmeticity
dichotomy**: the even resonances lie on the rigid line `Re s = ¼` for arithmetic `q = 3` but scatter off
it for non-arithmetic `q`. Your cluster-ceiling detector and this resonance geometry look like two faces
of one phenomenon.

I raise it because it is a *tool*, not only a result — a small, registerable evaluator — and I would
gladly put it in the hands of your colleagues and students: rigorously enclosed eigenvalues or
resonances for any Hecke `G_q` (or a related surface, with a modest new evaluator), engine and data
shared and wired up. Honest scope: the external ground truth is so far only the arithmetic `q = 3`
anchor; the non-arithmetic tables are corroborated within the project (independent Hejhal
point-matching), with a literature cross-check the natural next step rather than something already done.

I'll keep firming up the corridor section at a comfortable pace over the summer — no rush on your side
while you focus on the `−1`-dominance repair. Happy to send the Lean files for the window and
realization identities whenever useful.

With warm regards,
[name]

---

## Notes for us (not for the email)
- Everything above is `lake build`-verified axiom-clean; cite research_notes/UNCONDITIONAL_REDUCTION_2026-06-20.md.
- The one claim to keep honest: q≥22 is a REDUCTION, not a theorem. Do not let the prose imply closure.
- Tightened 2026-06-27 per Saar: cut internal Lean notation (raw radius formula `r²·B_λ²·cos²(|μc|+H)≥1`,
  exact window `L_blk(q)=⌈33q/256⌉+2`, `δ_∞=5.77e-5`, the `a·b=C0+Rcos` identity) → plain language;
  tightened the Aletheia offer; ADDED the link (iii) resonance-geometry = spectral face of the
  cluster-ceiling arithmeticity dichotomy he called a "paradigm shift".
- Optional data to add back if he engages on the gap: certified transfer-op gaps gap_q5=0.797, gap_q7=0.659
  (substantiate "the gap shrinks with q").
- If he asks for files: LblkWindow.lean, CorridorProductRealization.lean, WindowRealizeClose.lean,
  CorridorCollapse.lean, HpinClose.lean (all in projects/aristotle_dispatch_v15/uniform_q5to18/),
  + L1bArcCoverage.lean (B1_target/fcorr_lb).
- The residual to pose to him: thread `D_{N+j}>1` (in-domain residency) through
  `windowProductRealizes_corridor` so `hpin`'s radius forcing holds uniformly — the
  `hpin_not_unconditional` negative shows why the current interface fails.
- Aletheia scope caveat (keep honest): external ground-truth = q=3 only; non-arith = within-project Hejhal
  corroboration; CAP literature cross-check is DEFERRED (multi-week). Do NOT imply non-arith tables are
  externally CAP-validated.
- If he wants Aletheia: engine/certify/certify.py (single evaluator `hecke_transfer_operator_zero`;
  `register_evaluator()` is the extension hook), certified data code/out/certified_hecke_spectrum_table.json
  + resonance_geometry.json + resonance_v2.json, and the full write-up research_notes/aletheia_hecke_evidence_package.md
  (+ aletheia_cap_crossvalidate.md for the q=3 ζ check and the deferred CAP options).

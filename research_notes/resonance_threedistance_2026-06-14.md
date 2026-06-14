# Cluster-ceiling resonance B(q): a parity-gated rotation-arc covering condition — NOT a clean inhomogeneous-Diophantine bridge

**Date:** 2026-06-14. **Probe:** is the cluster-ceiling resonance (where the discrete B(q)
exceeds the continuous rotation-arc count) an inhomogeneous-Diophantine / three-distance
phenomenon — a bridge from B(q) to circle-rotation gap theory?

**One-line verdict.** The resonance IS a rotation-orbit-vs-small-arc *covering* phenomenon, and
the controlling rule is exact and arithmetic — but the arithmetic that decides it is **parity of
the rotation-arc count**, NOT a Diophantine approximation/three-distance condition. The "bridge to
inhomogeneous Diophantine approximation" as hypothesized is **REFUTED**; the honest finding is a
cleaner one: a *parity gatekeeper* + a transcendental near-integer window. New for this object, but
it does NOT fill the B1 open slot (no three-gap theorem for Rosen/Hecke CF, q>3).

---

## 0 · What was asked vs what is true

The probe hypothesised: "resonant q (where B(q) > continuous arc-width count) are characterized by
an inhomogeneous-Diophantine / three-distance condition on how the rotation orbit {n/(2q)} avoids
the notch." The prompt also asserted a resonant SET {23,24,29,30,33–36,38,39,40} from a now-deleted
earlier-formula table (`/tmp/bq_final_table.py`, frac=0.9999).

**Correction (reproduced, exact).** Under the *corrected* continuous formula already in the note's
CORRECTED SECTION — `B₀(q)=⌊W(q)·q/π⌋+1` with W(q) the sub-threshold last-branch arc width on the
governing ellipse with peak ab → t⁻ (frac→1⁻) — the discrete B(q) exceeds B₀(q) at **q=23 ALONE in
7..50** (and the next one is **q=61**; see §3). The stated set {23,24,29,…} is the failure set of
the *earlier buggy* `⌊w·q/π⌋+1` proxy (frac=0.9999, an under-measured w), whose failures are exactly
the "first few q of each B-plateau"; that proxy was already demoted in the note. So the genuine
resonance is **rare and isolated**, not a dense set. (`code/goal1_Bq_arc_width_asymptotic.py` already
shows only q=23 fails its `floor+1` in 7..60; this note reproduces and explains it.)

Everywhere except the resonant q, the optimal discrete count is realized at **frac<1** (peak strictly
*below* threshold, NO notch), and equals B₀(q) exactly. The notch regime (frac>1) only ever matters
at the resonant q. (Verified exact, `code/goal1_Bq_resonance_notch_gain.py`: notch-gain = +1 only at
q=23 in 7..39; at every other q the optimum is at frac<1.)

---

## 1 · Pinned geometry (exact, dps=50)

Last-branch k=1 map `M=[[0,1],[−1,λ]]`, λ=2cos(π/q), conserves `E=a²−λab+b²`; whitened, M = rotation
by −θ, θ=π/q. On a level set E=E₀ the state is y=√E₀(cos φ, sin φ) and the observable is

>   **P(φ) = a·b = E₀·( c₀ + amp·cos 2(φ−φ\*) )**,  peak μ_max = c₀+amp = 1/(2−λ) at φ=φ\* (a=b),
>   trough μ_min = c₀−amp = −1/(2+λ).

(Verified dps=50: c₀,amp,φ\* extracted exactly as `Q=(L⁻¹)ᵀ S L⁻¹`, S=[[0,½],[½,0]];
mu_max/mu_min match 1/(2−λ), −1/(2+λ) to 40 digits — `/tmp/notch_geometry.py`.)

Threshold t=1/λ³. Parametrise the governing ellipse by **frac = peak_ab/t = E₀·μ_max/t**.
- **frac ≤ 1:** peak below t, the whole sub-threshold last-branch arc is one connected arc; no notch.
- **frac > 1:** the peak pokes a **super-threshold NOTCH** of half-width δ centered at φ\*, where

>   **cos(2δ) = (t/E₀ − c₀)/amp = (μ_max/frac − c₀)/amp**,   so   2δ = arccos((μ_max/frac − c₀)/amp).

The notch opens like 2δ ≈ √(2(μ_max/amp)(frac−1)) for frac→1⁺ (fast, √-rate).

A **cluster** = a maximal run of consecutive rotation-lattice points φ_n = φ₀ − nθ that are
simultaneously in the last-branch domain AND sub-threshold (P<t). B(q) is the max run length over E₀
and offset φ₀.

---

## 2 · The exact resonance condition — PARITY of the arc count, not Diophantine

### 2.1 Decomposition: B(q) = B₀(q) + [resonance gain ∈ {0,1}]

Let **B₀(q)** = max run with peak ≤ t (no notch) = the connected-arc count = `⌊W(q)·q/π⌋+1`
(continuous arc width / θ, floor, +1). The resonance is the extra +1 you can sometimes get by
growing the ellipse past frac=1, opening a narrow notch, and letting the rotation lattice **hop** it.

### 2.2 The mechanism (exact, dps=50 — `code/goal1_Bq_resonance_parity_proof_dps50.py`)

To gain B₀+1 points you must place B₀+1 consecutive lattice points (spacing θ) all in-domain and
sub-threshold on an ellipse with frac>1. The longest run is symmetric about φ\* (the arc is
symmetric-unimodal about the peak). Then there are exactly two cases by the **parity of the target
count B₀+1**:

- **B₀+1 EVEN (i.e. B₀ ODD):** the symmetric placement straddles φ\* — the *center gap*
  (φ\*−½θ, φ\*+½θ) lands ON the notch, with the two flanking points at φ\*±½θ. If 2δ<θ (notch
  narrower than a gap) the notch sits inside that empty center gap and **every** lattice point is
  sub-threshold → **HOP succeeds, gain +1.**
  *(q=23, target 6: flanking points at φ\*±½θ have P=0.12816593 < t=0.128559, t−P=+3.9·10⁻⁴ each;
  notch P>t falls in the empty center gap → all 6 valid. Confirmed dps=50.)*

- **B₀+1 ODD (i.e. B₀ EVEN):** the symmetric placement puts **one point exactly at φ\*** — on the
  peak, i.e. *inside* the notch (P>t) → that point is super-threshold → placement INVALID, no gain.
  *(q=47, target 11: the rel=0 point has P=0.1259041 > t=0.1259041−6.3·10⁻⁵, IN the notch → blocked,
  even though every other point passes and the arc is only 0.003θ short. B(47)=10, not 11. dps=50.)*

So the **gatekeeper is parity of B₀(q)**: a notch-hop can gain a point **only when B₀(q) is ODD**
(so the +1 target is even and the lattice straddles the peak). When B₀(q) is even, no amount of
ellipse-tuning helps — a symmetric run of odd length always impales the peak. (An *asymmetric* run
cannot do better: the arc is symmetric-unimodal, so the longest run is symmetric; an asymmetric
shift loses a point at one end before gaining at the other. Confirmed by the full grid `Bdisc`.)

### 2.3 The secondary (necessary) window — and it is TRANSCENDENTAL, not Diophantine

Parity is necessary but not sufficient. Within the odd-B₀ bands, the gain also needs the arc to be
**just short of fitting the extra point at frac=1** so that a *small* frac>1 push (which keeps
2δ<θ) suffices to widen it. Precisely: gain ⟺ B₀(q) odd AND s(q):=W(q)·q/π is close enough to
B₀ (= ⌊s⌋+1) from below that the integer-crossing frac* (where W·q/π hits B₀) still has 2δ(frac*)<θ.

This second condition is governed by **s(q) = W(q)·q/π** and the notch-rate, both **transcendental
functions of λ=2cos(π/q)** — NOT arithmetic. There is no clean "frac(q·something) ∈ interval" form:
W(q) is a 1-D root-find on the ellipse with no closed arithmetic expression. So the *position* of
the resonance is set by analysis, not number theory; only the *gate* (parity) is arithmetic.

### 2.4 Prediction vs actual — 100% (q=7..40), plus the predicted q=61

Model **predB = B₀+1 if (B₀ odd AND symmetric (B₀+1)-straddle fits for some frac>1) else B₀**:

| band | q range | B₀ | parity | s(q) just-below-odd-int reached? | resonance |
|------|---------|----|--------|----------------------------------|-----------|
| B₀=3 | 7–12 | 3 | ODD | no (s 2.08–2.85, far) | none |
| B₀=4 | 13–18 | 4 | EVEN | — (even, parity blocks) | none |
| B₀=5 | 19–23 | 5 | ODD | **q=23: s=4.969→5⁻, close** | **q=23 ✓** |
| B₀=6 | 24–28 | 6 | EVEN | — (parity blocks; q=28 s=5.994 ignored) | none |
| B₀=7 | 29–32 | 7 | ODD | no (s 6.20–6.83, not close to 7⁻) | none |
| B₀=8 | 33–37 | 8 | EVEN | — | none |
| B₀=9 | 38–42 | 9 | ODD | no (s 8.09–8.93) | none |
| B₀=10| 43–47 | 10| EVEN | — (q=47 s=9.997→10⁻ EXTREMELY close, IGNORED by parity) | none |
| B₀=11| 48–51 | 11| ODD | no (s 10.21–10.85) | none |
| B₀=12| 52–56 | 12| EVEN | — | none |
| B₀=13| 57–61 | 13| ODD | **q=61: s=12.989→13⁻, close** | **q=61 ✓** |

**34/34 exact match q=7..40** (`code/goal1_Bq_resonance_parity.py`, 0 mismatches vs genuine-map ground truth
table C3). **The model PREDICTED the next resonance at q=61** (`code/goal1_Bq_resonance_find_next.py` on M1): s=12.989
just below odd 13, B₀=13 odd, symmetric 14-straddle fits at frac=1.0002 → B(61)=14. **Confirmed
exact (dps=50, `code/goal1_Bq_resonance_q61_exact.py`):** 13 fits at frac=0.983 (B₀, peak below t), 14 fits via the
notch-hop at frac=1.0002 (even straddle, 2δ=0.547·θ < θ), and 15 does NOT fit (odd → impales the
peak). Since the cluster is an exact arc of the M-rotation, a valid dps=50 placement satisfying all
last-branch + sub-threshold conditions IS a genuine-map run — so **B(61)=14**, the second member of
the resonance family, predicted and verified.

**The cleanest natural experiment is q=47.** Its arc is only ~0.003·θ short of fitting an 11th
point (s=9.99721, frac(s)=0.9972 — the closest-to-integer in the whole range, FAR closer than
q=23's 0.969). A naive "just-below-integer / inhomogeneous-Diophantine" criterion would scream
resonance at q=47. **It does not resonate** (B(47)=10), because B₀=10 is even: the 11th point would
land on the peak. q=23 (less close to its integer) resonates because B₀=5 is odd. **Parity beats
proximity** — this is the decisive evidence that the resonance is parity-gated, not
Diophantine-gated.

---

## 3 · Is it a three-distance / inhomogeneous-Diophantine bridge? — REFUTED (with a cleaner truth)

**The covering picture is real but trivially-arithmetic.** "Does the equally-spaced rotation lattice
{φ₀−nθ}, θ=π/q (orbit {n/(2q)} on the circle), place a point inside the small super-threshold notch
arc?" IS a covering / inhomogeneous-approximation *question*. But because the rotation number is the
**rational** 1/(2q), the orbit is the *exact* equally-spaced lattice of spacing 1/(2q) — there is NO
Diophantine subtlety (no continued-fraction structure, no Ostrowski expansion, no three-distance
trichotomy: an equally-spaced rational lattice has only ONE gap, not three). The only freedom is the
phase offset φ₀, and the only question is whether a single lattice gap (width θ) can be centered on
the notch (width 2δ<θ) — which is possible **iff the requisite run length is EVEN** (so the center
of the run is a gap, not a point). Hence the controlling arithmetic collapses to **parity**, the
most degenerate possible "Diophantine" condition.

So the hypothesized bridge — "resonance characterized by an inhomogeneous-Diophantine / three-
distance condition" — is **REFUTED in substance**: there is no three-distance theorem in play (the
orbit is a single-gap rational lattice), and the deciding arithmetic is parity, not approximation
quality. What *is* true and new is a sharper, humbler statement: **a parity-gated rotation-arc
covering rule** with a transcendental near-integer window.

**Does it touch the B1 open slot (no three-gap theorem for Rosen/Hecke CF, q>3)?** **NO.** The B1
slot asks for a genuine three-*distance* partition of the Rosen-λ orbit for q>3 (a number-theoretic
gap trichotomy). This finding is the opposite: precisely *because* the corridor rotation is rational
(1/(2q)), it produces a single-gap lattice and a parity rule — it does not exhibit, and cannot
supply, a three-distance theorem. It confirms (does not fill) the slot: the natural rotation here is
too degenerate (rational, finite-order) to host three-gap structure. (Consistent with B1's verdict
that the elliptic-rotation structure is "orthogonal to," not an instance of, three-gap theory.)

---

## 4 · Novelty verdict

**Searches** (WebSearch 2026-06-14): three-gap theorem & space of lattices (Marklof–Strömbergsson
1612.04906; Wikipedia; "Symmetries of the Three Gap Theorem" 2208.01680); three-distance theorem
(Berthé–Reutenauer; "Specified Three Distance Theorem" AMM 2020); Rosen/Hecke CF (Schmidt;
transcendence; geodesic Rosen CF 1310.1585); "rotation orbit even/odd points straddle vs impale a
symmetry line" (symbolic-codes-for-rotational-orbits nlin/0408015).

- The **three-gap / three-distance** literature is about *irrational* rotations (CF/Ostrowski
  structure). Our object is a **rational** rotation 1/(2q) → degenerate single-gap → NOT a
  three-gap instance; the literature does not phrase a "parity decides whether the orbit can
  straddle a shrinking symmetric arc" rule for a *run-length / cluster-ceiling* observable.
- The closest abstract analogue is the symbolic-dynamics fact (nlin/0408015) that symmetric orbits
  "hop across a symmetry line iff index odd, cross iff even" — the SAME parity flavor, but for
  periodic-orbit symmetry classes, **not** for a sub-threshold run length / extremal cluster ceiling
  of a gap map, and with no notch/threshold mechanism.
- No BCZ/Hecke/Veech-slope-gap or EVT-cluster-size source gives a parity-gated arc-covering
  derivation of a cluster ceiling (consistent with the parent note's §5 and the B1 audit).

**Verdict: the *parity-gated rotation-arc covering* account of when the cluster ceiling B(q) jumps
above its continuous arc count is NOVEL for this object** (BCZ/Hecke last-branch cluster size), but
**modest**: the controlling arithmetic is parity (elementary), and the resonance *location* is
transcendental (W(q) near an odd integer), not arithmetic. It is **not** an inhomogeneous-Diophantine
/ three-distance bridge, and it does **not** fill the B1 q>3 three-gap open slot — it explains why
that slot stays open (the natural rotation is rational/single-gap).

---

## 5 · Honest caveats / residual

1. **W(q) is transcendental, computed by root-find.** The "near an odd integer" window has no closed
   arithmetic form; the resonance set is `{q : B₀(q) odd AND s(q) close enough to ⌊s⌋+1 from below}`,
   with "close enough" set by the √-rate notch opening vs dW/dfrac. Confirmed resonances: q=23, q=61
   (period ≈ 38 in q, ≈ the q-gap for s to advance by 2 at slope ≈0.2127). Predicting them needs the
   numeric s(q), not a formula.
2. **Parity rule proven structurally + exact (dps=50), not yet a Lean theorem.** The symmetric-run-
   is-longest claim (so the gain hinges on whether the run center is a gap or a point) rests on the
   arc being symmetric-unimodal about φ\* (true: P(φ)=E₀(c₀+amp cos2(φ−φ\*)) is a single cosine). A
   rigorous statement needs: (a) longest run is symmetric (calculus on the unimodal P over the
   symmetric domain), (b) the even/odd straddle/impale dichotomy (elementary once (a) holds).
3. **Ground-truth B(61) verification — DONE.** B(60)=13 confirmed by genuine full-Taha-map deep MC
   (M1, `code/goal1_Bq_ground_truth.py`). B(61)=14 confirmed EXACT at dps=50 (`code/goal1_Bq_resonance_q61_exact.py`):
   the 14-point even straddle is a valid genuine-map arc; the 15-point odd run impales the peak and
   fails. (For such rare long runs the exact-arc placement is more reliable than MC, which needed a
   120-start heavy batch even to confirm the single q=23 length-6 run — the dps=50 arc is definitive.)
4. **The corrected resonance set is {23, 61, …} (rare/isolated), NOT the dense {23,24,29,…}** the
   probe quoted from the deleted earlier table. The dense set was the earlier buggy proxy's
   plateau-onset failures, already superseded in the parent note.

---

## 6 · Files / repro
- `code/goal1_Bq_rotation_arc_corrected.py` — discrete B(q) counter (ground truth integer).
- `code/goal1_Bq_arc_width_asymptotic.py` — W(q) / s(q)=W·q/π (continuous B₀, the `floor+1`).
- `code/goal1_Bq_ground_truth.py` — genuine full Taha-map B(q) (deep MC); B(60)=13 confirmed.
- `code/goal1_Bq_resonance_notch_gain.py` — notch vs no-notch discrete count: gain=+1 only at q=23 (7..39).
- `code/goal1_Bq_resonance_parity.py` — parity model, 34/34 match q=7..40 vs ground truth.
- `code/goal1_Bq_resonance_parity_proof_dps50.py` — dps=50 proof: q=23 even-straddle VALID, q=47 odd-impale INVALID.
- `code/goal1_Bq_resonance_find_next.py` — predicts & checks next resonance band q=55..68 (finds q=61).
- `code/goal1_Bq_resonance_q61_exact.py` — dps=50 exact: B(61)=14 (14 even-straddle fits, 15 odd impales).
- Parent: `research_notes/Bq_rotation_arc_2026-06-14.md` (mechanism + CORRECTED SECTION).
- Prior novelty: `research_notes/novelty_B1_threegap_rotation_2026-06-14.md` (the B1 open slot).
</content>
</invoke>

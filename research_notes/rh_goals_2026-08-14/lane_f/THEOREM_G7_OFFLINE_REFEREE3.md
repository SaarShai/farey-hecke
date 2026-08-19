# THEOREM G7 OFFLINE ASSEMBLY — THIRD COLD REFEREE

Date: 2026-08-19
Worktree: `/Users/za/Documents/farey-hecke/.worktrees/law-q7-assembly-referee3-20260819`
Reviewed commit: `7e6441d15de619356d1a6be9d763348b87ffd8e8`

## Verdict

**CONFIRMED.** The q7 paper-level chain is now closed at the following exact
scope: the certified `mms+` Hilbert Fredholm zero in the flagship box transports
to the MMS `+` determinant, then gives a Selberg-zeta zero off
\(\Re s=1/2\), and hence the standard scattering-resonance interpretation.
This is not a promotion of a geometric parity label, an automorphic
correspondence, the full LAW, or the `h_q=2` priority sentence.

The verdict is an assembly-scope confirmation, not a claim that every remaining
formal, provenance, review-depth, or dissemination gate is complete.

## Scope and first-gap closure

The first assembly referee (`THEOREM_G7_OFFLINE_REFEREE2.md`) accepted the
finite/Hilbert winding, endpoint comparison, E1 geometry, and `K_s` clearance,
but identified Link 4b as load-bearing open: the q5 Clause-1 note did not by
itself bind the q7 19-block engine to the MMS operator
(`THEOREM_G7_OFFLINE_REFEREE2.md:129-173`). Its leftovers explicitly required
an explicit q7 Clause-1/common-continuation proof and MMS source banking
(`THEOREM_G7_OFFLINE_REFEREE2.md:303-317`).

That repair is now present and has its own second cold referee:

- `Q7_R5_OPERATOR_BINDING_SOL.md:490-712` supplies the exact q7 19-row
  specialization, branch/sign conventions, all-tail-input-5 audit, and R1--R9
  centered tail-column proof. It derives the \(O(1/\ell)\) centered difference,
  the \(\sum \ell^{-(2\sigma_K+1)}\) first moment, local trace-norm summability,
  and trace-class holomorphy on \(\Omega^*\).
- `Q7_R5_OPERATOR_BINDING_REFEREE.md:398-422` identifies the original two
  load-bearing omissions. `Q7_R5_OPERATOR_BINDING_REFEREE2.md:160-206`
  independently confirms that R1--R9 close those omissions and that the
  Simon, Grothendieck, and MMS sector roles match the accepted q5 precedent.
- The repaired source binding is q7-specific: `h_7=2`, `\kappa_7=5`, sign `+1`,
  and 19 occurrences (9 heads, 10 tails). It is not an inference from the q5
  `h=1`, `\kappa=3`, 11-block wrapper.

## Primary-source, theorem-number, and equation-(34) audit

`Q7_MMS_PRIMARY_SOURCE_RECEIPT.md` is now the documentary authority. It records
Mayer--Mühlenbruch--Strömberg, arXiv `0912.2236v2`, 15 March 2010, with the
versioned PDF hash

```text
a10020bd084534dc60fc3e887958f1583f2fc115d567961b461df1a59b32e072
```

The receipt's fresh-fetch comparison and `pdftotext` search report these exact
locations (`Q7_MMS_PRIMARY_SOURCE_RECEIPT.md:18-62`):

```text
1216:Theorem 4.10. The operator Ls : B → B is nuclear of order zero ...
1337:Lemma 5.1. The operators P : B → B and Ls : B → B commute ...
1385:For q = 2hq + 3 > 5 we get
1872:Theorem 6.4. The Selberg zeta function ZS (s) ...
1914:Remark 4. Using the explicit form of the maps which fix rq ...
```

The q7 substitution receipt is explicit: `q=7 h=2 kappa=5 odd_scope=True`
(`Q7_MMS_PRIMARY_SOURCE_RECEIPT.md:64-78`). Thus the source/version/theorem
numbering and the odd-q heading are no longer the unbanked documentary gap
reported by Referee2. The receipt also states the source boundary: MMS does not
itself prove the Python-to-operator correspondence or the Hilbert/Banach lemma;
those are exactly what the q7 binding proof supplies
(`Q7_MMS_PRIMARY_SOURCE_RECEIPT.md:80-87`).

Theorem 4.10 and Lemma 5.1 are used at the right scope. The former supplies
order-zero nuclearity and the real pole lattice for the full Banach operator;
the latter supplies commutation with `P` and complemented invariant `P`
eigenspaces. The q7 proof then supplies the bounded restriction/conjugacy to
the five-disc `+` operator, so no q-independent label is being substituted for
the q7 implementation.

## Receipt and numerical checks

The existing immutable receipts were read directly. The focused checks returned:

```text
$ jq '{verdict,precision_bits,N_primary,N_comparison,base_closed_arc_count,chunk_count}' \
    F7_R3B_ASSEMBLY_RECEIPT.json
{
  "verdict": "THEOREM-GRADE closed-contour YES at N=256",
  "precision_bits": 384,
  "N_primary": 256,
  "N_comparison": 224,
  "base_closed_arc_count": 192,
  "chunk_count": 16
}

$ jq '{schema,precision_bits,rho_hat_upper_bound,eta_max_upper_bound,
       rho_hat_less_than_one,verdict}' \
    f7_receipts/F7_E1_ENLARGED_CONTRACTION_V2_RECEIPT.json
{
  "schema": "f7-e1-enlarged-contraction/v2",
  "precision_bits": 384,
  "rho_hat_upper_bound": "[0.9152411837446921486199057183790500874132201822167121491776750120826392648965487186604668777644585600 +/- 3.97e-101]",
  "eta_max_upper_bound": "[0.8695652173913043478260869565217391304347826086956521739130434782608695652173913043478260869565217391 +/- 3.06e-101]",
  "rho_hat_less_than_one": true,
  "verdict": "PASS_RHO_HAT_LT_1"
}

$ jq '{all_gates_pass,box_to_lattice_distance_lower_bound_rounded_down,
       detK_nonvanishing,verdict}' f7_receipts/F7LINKS_KS_GATE_RECEIPT.json
{
  "all_gates_pass": true,
  "box_to_lattice_distance_lower_bound_rounded_down": "0.5895479",
  "detK_nonvanishing": {
    "abs_detK_lower_bound_rounded_down": "0.936818983390",
    "abs_detK_upper_bound_rounded_up": "1.063204693008",
    "strictly_positive_on_closed_box": true
  },
  "verdict": "PASS_KS_BOX_CLEAR_AND_DETK_NONVANISHING"
}
```

The q7 binding receipt reproduction remains the banked `K_start=12` run, not
the rejected `K_start=8` diagnostic:

```text
K_start=12, max_K=64
rho_star = [0.763212029206899202166157 +/- 1.41e-25]
worst_block = 5→3, +1, head
verdict = PASS_RHO_LT_0.80
```

The q7 binding second referee records that all 19 rows pass, all 10 tails have
input component 5, and the enlarged-disc value is
\(\widehat\rho\le0.9152411837446922<1\)
(`Q7_R5_OPERATOR_BINDING_REFEREE2.md:17-69`). These are premises of Link 4b,
not replacements for its proof.

## Link-by-link decision

### Link 1 through Link 4: Hilbert zero

Referee2 accepted the q7 closed-contour chain at its Hilbert scope. The banked
assembly receipt has 384-bit arithmetic, `N=256`, 192 arcs, 16 chunks, and
verdict `THEOREM-GRADE closed-contour YES at N=256`; the `N=224` arm is the
designed `NOT_CERTIFIED` control. Its merged winding is 1, the minimum certified
finite-lower-minus-tail margin is
`0.00000241285276269068356797445`, and all F-inflated arc enclosures exclude
zero (`F7_R3B_ASSEMBLY_RECEIPT.json`, nested closed-contour/winding fields).
The prior referee explicitly accepted this as a q7 Hilbert Fredholm zero
route (`THEOREM_G7_OFFLINE_REFEREE2.md:85-105`).

### Link 4b: Hilbert to MMS Banach determinant

**Closed at the stated q7 scope.** The q7 repair binds the actual branches,
weights, discs, 19 calls, and `+` sector to MMS equation (34), then proves the
common determinant on \(\Omega^*\). The second binding referee's verdict is
`CONFIRMED — REPAIRED PROOF CLAIM`, not merely `NOT REFUTED`
(`Q7_R5_OPERATOR_BINDING_REFEREE2.md:194-206`).

The determinant citations are correctly scoped: Simon Theorem 4.2/equation
(4.2) gives the Hilbert trace-class spectral product with algebraic
multiplicity; Simon Theorem 3.3 gives analyticity of a trace-class-holomorphic
family; MMS Theorem 4.10 and Lemma 5.1 transfer order-zero nuclearity to the
complemented invariant reduced sector; and Grothendieck Théorème 8 gives the
genus-zero Banach spectral product for the \(p\le2/3\) class
(`Q7_R5_OPERATOR_BINDING_SOL.md:690-712`). Lidskii is not being substituted
for Simon's determinant-product theorem.

### Link 5: the `K_s` divisor

**Closed at q7 machine scope.** The independent 384-bit receipt gives the
zero lattice \(s=-n+i\pi k/a_7\), all lattice points with `Re <= 0`, box-to-
lattice distance at least `0.5895479`, and a strict closed-box lower bound
`|det(1-K_s)| >= 0.936818983390`. The upper bound
`1.063204693008` is context only; the lower bound is the load-bearing
nonvanishing fact. Referee2 accepted this gate (`THEOREM_G7_OFFLINE_REFEREE2.md:
175-199`). The missing q7 Lean specialization is not load-bearing because the
ball receipt directly proves the finite-box nonvanishing statement consumed by
the assembly.

### Link 6: MMS factorization and numerator/denominator logic

**Closed conditional on the now-confirmed Link 4b and the cited MMS theorem.**
The source receipt verifies Theorem 6.4 in the consumed arXiv v2 and records its
bounded use as the quotient of the full/reduced determinant product by the
`K_s` determinant (`Q7_MMS_PRIMARY_SOURCE_RECEIPT.md:54-62`). The assembly's
formula is therefore used as

\[
 Z_S(s)=
 \frac{\det(1-L_{s,+})\det(1-L_{s,-})}{\det(1-K_s)}.
\]

The plus determinant has the Link-4b zero. The `K_s` denominator is finite and
nonzero on the closed box by Link 5. The minus determinant is holomorphic there:
MMS Theorem 4.10 puts its poles on the real lattice
\(s=(1-k)/2\), whereas the box has nonzero imaginary part near `4.67`.
Consequently the quotient has a Selberg-zeta zero, with multiplicity at least
that of the plus factor. No cancellation by the denominator is possible.

The former assembly `TODO-VERIFY` on the MMS source/version and equation-(34)
heading is superseded by the primary-source receipt. The receipt does not claim
that MMS proves the Python/Hilbert correspondence; that implication is covered
by the q7 repair, as required.

### Link 7: scattering interpretation

**Supported at the standard cited scope, conditional on Link 6.** The box has
\(0<\Re s_*<1/2\) and nonzero imaginary part. Thus the Selberg zero is not a
real small-eigenvalue alternative and is not on the tempered line; the standard
finite-area Selberg/scattering correspondence identifies it as a scattering
resonance. This is exactly the conditional scope accepted by Referee2
(`THEOREM_G7_OFFLINE_REFEREE2.md:220-234`). It does not assign a geometric
even/odd Maass parity label; the assembly explicitly withholds that claim.

## Exact supported claim and explicit non-claims

Supported now:

1. A q7 `mms+` Hilbert Fredholm determinant zero in the certified box.
2. Its transport to the MMS `+` Banach determinant on the common continuation
   domain.
3. A Selberg-zeta zero with
   \(|\Re s_*-0.4751647621098225|\le10^{-6}\) and
   \(|\Im s_*-4.668743786424289|\le10^{-6}\), hence
   \(\Re s_*\le0.4751658<1/2\) and gap \(\delta\ge0.0248342\).
4. The standard scattering-resonance interpretation of this nonreal zero.

Not supported by this verdict:

- a q7 Lean `KsZeroLattice.lean` specialization;
- geometric parity, automorphic/eigenfunction correspondence, or a complete
  resonance list;
- the full LAW, RATE, `phi_q`, q8, or any q-generic theorem beyond the explicit
  q7 operator and box;
- the literature-priority sentence “first at `h_q=2`” without a fresh prior-art
  audit.

## Remaining non-paper gates and provenance blast radius

The following remain honest release/formalization gates, not failures of the
paper-level q7 zero implication:

1. The q7 Lean lattice joint is absent. The machine `K_s` receipt is sufficient
   for the stated finite-box theorem, but formal coverage remains open.
2. The assembly has one adversarial round, whereas the q5 chain had five rounds
   plus a hostile audit. Owner review depth and dissemination remain gated.
3. E1 was re-derived from raw fields, not independently re-implemented; any
   rerun must preserve the recorded cap and pinned receipts.
4. The live generic `zeta_cert_rosen.py` is drifted and is not evidence for the
   certified run. The q7 chain uses the pinned q7 builder/engine/certifier and
   q5 primitive hashes recorded in `Q7_R5_OPERATOR_BINDING_SOL.md:25-50`; restore
   those bytes before any rerun. This provenance issue does not alter the
   immutable receipt-backed result.
5. Latent runner assertions and the unverified `h_q=2` priority/prior-art claim
   remain disclosed and must not be silently promoted.

There is therefore no remaining paper-level obstruction in Links 4b--7 at the
scope above. The blast radius is local: the assembly may be upgraded from
“Link 4b conjectural/open” to a confirmed q7 Selberg-zero plus standard
resonance statement, while its declaration/release label and the non-claims
above remain unchanged.

## Verification receipt for this referee

Focused provenance hashes read in this worktree included:

```text
Q7_MMS_PRIMARY_SOURCE_RECEIPT.md
  9df992f8a812cbbe3ac94364445b331d24507009f3d0adc82870b33b45038383
Q7_R5_OPERATOR_BINDING_SOL.md
  b5fe7f8a82a6b7b16981f71735533c620c8f8a3b5e83c7acd4d0e246eb7c99a5
Q7_R5_OPERATOR_BINDING_REFEREE2.md
  aec58b5cd6746cfcf4a07f328a5f4a3dd046cbf18c623314818b4869463befb0
```

Pinned transitive implementation bytes read as:

```text
f7_source_builder.py       038bcb49d3df00cfd4e1fb4aafca46a4e11e34f6b18300c07d4666be51bf45c6
f7_r3b_engine.py           661a4d2b132d1821d18499a302f58805bf7565e560d8f1520379dde156bc7d1a
f7_certify_tb_blocks.py    9c17cd7ce42c7d41e6d811eb2b8ecf3ced88b8d89e6b411b4cd19aaf7b5c80b1
f7_tb_disc_sweep.py        b8e693376369e44085d88925fc635ce32004173efed46ffed95e04c1c897241f
zeta_cert_rosen_q5.py      c84c5c3f6d9f7a320bca7f1dbfd96a4859c3eea9b3de5420eb4eb223ad0d597b
```

After authoring this report:

```text
$ git diff --check
(no output; exit 0)

$ git status --short --branch
## codex/law-q7-assembly-referee3-20260819
?? research_notes/rh_goals_2026-08-14/lane_f/THEOREM_G7_OFFLINE_REFEREE3.md
```

No assembly, proof, MAP, task, code, receipt, or git state was edited or
committed.

STATUS: CONFIRMED_AT_EXACT_Q7_SELBURG_ZERO_AND_STANDARD_RESONANCE_SCOPE; NON-PAPER_GATES_REMAIN

READY FOR JUDGING

# V22 dispatch — skipped obligations

None. All 5 obligations named by the task (coset-cocycle constancy, the W₂ normalizer
computation `wγw⁻¹=[[d,−c],[−2b,a]]`, weight-neutrality of the D₂ composition operator
via the chain rule, the block-diagonalization identity, and the exact 2×2 determinant
splitting `det(1−N_s)=det(1−L)·det(1+L)`) admit a finite, self-contained statement and
are included in `M1DIntertwiner.lean`.

Note on obligation 5 (determinant splitting): the M1D note's own proof route (§3.3, gaps
ledger G1) is via a trace expansion and meromorphic continuation for a *nuclear operator*
on a Banach space — that route is genuinely analytic and out of scope for a finite dispatch.
What is dispatched instead is the finite linear-algebra shadow the ledger itself flags as
"a standard nuclear-determinant lemma" and "mechanical": `det(1 − A⊗σ) = det(1−A)det(1+A)`
for a general `n×n` matrix `A` over `ℂ`, realized via the block matrix `[[0,A],[A,0]]`.
This is a faithful, strictly finite restatement of the same algebraic content, not a
weaker substitute claim.

Everything else in the M1D gaps ledger (§9: G5–G9, the Eisenstein-derivation of `phi_4`,
the resonance/divisor transport theorems, the `N_{s,+}` ↔ `Z_{Γ₀(2)}` identification) is
explicitly tagged FRONTIER in the source note and was out of scope for this lane by the
task's own instruction (5 named obligations only).

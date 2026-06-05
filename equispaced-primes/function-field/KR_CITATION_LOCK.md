# Keating–Rudnick citation — LOCKED from primary source (2026-05-16)

Was [CITATION-UNVERIFIED] (PDF/Project Euclid blocked for earlier agents).
Now locked via **ar5iv full-text render** (ar5iv.labs.arxiv.org/html/1504.03444)
+ **arXiv abstract** (arxiv.org/abs/1504.03444), read this session.

## Reference
J. P. Keating and Z. Rudnick, *Squarefree polynomials and Möbius values in
short intervals and arithmetic progressions*, **arXiv:1504.03444**; published
**Algebra & Number Theory 10 (2016), no. 2, 375–420**.

## Abstract (verbatim)
> "We calculate the mean and variance of sums of the Möbius function and the
> indicator function of the squarefrees, in both short intervals and
> arithmetic progressions, in the context of the ring of polynomials over a
> finite field of q elements, in the limit q→∞. We do this by relating the
> sums in question to certain matrix integrals over the unitary group, using
> recent equidistribution results due to N. Katz, and then by evaluating
> these integrals. In many cases our results mirror what is either known or
> conjectured for the corresponding problems involving sums over the integers
> … The ranges over which our results hold is significantly greater than
> those established for the corresponding problems in the number field
> setting."

## Locked facts (primary-confirmed)
- **Möbius, short intervals — Theorem 1.2:** `Var(N_μ(·;h)) ~ H` with
  `H=q^{h+1}`, `~ H·∫_{U(n−h−2)} |tr Sym^n U|² dU = H`; monodromy
  **U(n−h−2)**; regime `0 ≤ h ≤ n−5`, `q→∞`, q odd.
- **Möbius, arithmetic progressions mod Q (§8):**
  `Var_Q(S_μ) = (1/Φ(Q)) Σ_{gcd(A,Q)=1} |S_{μ,n,Q}(A)|²`,
  `S_{μ,n,Q}(A)=Σ_{f∈M_n, f≡A (Q)} μ(f)`; matrix model **U(n−deg Q−2)**,
  unitary; limit `q→∞`, `deg Q < n`.
- **§1.3 (verbatim sense):** "Restricting to short intervals or arithmetic
  progressions leads to sums over **Dirichlet characters** involving the
  associated **L-functions** … written in terms of unitary matrices …
  [which] become equidistributed in the unitary group" (Katz). **This is
  exactly the character-orthogonality framework our D3 §6 duality uses.**
- μ² short intervals = **Theorem 1.4** (parity-dependent); μ² arithmetic
  progressions = **Theorem 1.5**.

## Honest residual (do NOT inflate)
The exact theorem **number** for the *Möbius-in-arithmetic-progressions*
case (as distinct from short-interval Thm 1.2 and μ²-AP Thm 1.5) was **not
rendered verbatim** by ar5iv — it lives in §8 as the AP analogue (likely
"Theorem 1.3", NOT verbatim-confirmed). For any external writeup citing the
AP-Möbius result: cite as **"Keating–Rudnick (Algebra & Number Theory 10
(2016), Thm 1.2 and §8; arXiv:1504.03444)"** and confirm the precise AP
theorem number against the published PDF before final submission. The
load-bearing fact (KR compute the Möbius-AP variance = unitary matrix
integral via the Dirichlet-character/L-function reduction, q→∞) is
**primary-confirmed**.

## Consequence for the D3 verdict (unchanged, now on solid citation)
Our D3 §6 character-orthogonality duality (self-proved, citation-free) showed
the twisted/Farey Möbius variance = `Φ_A(Q)^{-1}Σ_{χ≠χ0}|M_A(n,χ)|²` = the
Möbius-in-progressions variance. KR §8 + §1.3 confirm this is *exactly* their
object and method (Dirichlet characters → L-functions → unitary Katz
equidistribution). ⇒ the D3 "dictionary-tier, not new mathematics, it is
Keating–Rudnick" verdict is now backed by a **locked primary citation**, not
just the self-proof. No change to the verdict; the BLOCKED-FOR-USER item #1
(lock KR) is **RESOLVED** (modulo the one soft theorem-number above).

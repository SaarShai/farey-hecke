---
model: mimo-v2.5-pro
max_tokens: 12000
---

# D4 — Defend killer-app PIPELINE value vs Z4's "Sym^k is textbook"

## Z4's claim

"Sym^k Chebyshev recurrence is Fulton-Harris §15.2 textbook. Verifying it to 10 digits is like verifying 2+2=4 to 10 decimal places. Not a discovery."

## Counter

Z4 is correct about the math being textbook. But misses what's actually claimed.

### The actual claim chain

The KILLER-APP is:
1. **Concept**: prime-bias signal ψ_L(x) − x is a sum of complex exponentials with frequencies γ_k of L-zeros (Riemann explicit formula, 1859).
2. **Algorithm**: apply MUSIC (or Prony, ESPRIT) to recover γ_k.
3. **Pipeline**: For each L-function family, compute the appropriate λ_p and form the bias signal.
4. **Validation**: works across 6-8 distinct L-function families (or 10 if we count Sym⁴/⁵).

For Sym^k Δ:
- The Hecke eigenvalue formula λ_p(Sym^k) = U_k(τ(p)/(2·p^{11/2})) is from SU(2) rep theory (textbook).
- IMPLEMENTING this for computational MUSIC on Sym⁴, Sym⁵ — has this been done before?

### The real novelty questions

Z4 says "verification of 2+2=4". The defense:

**Sym^k recurrence ALONE is not a discovery.** Agreed.

**The application — computing Sym^k λ_p via the recurrence and using it as MUSIC input for L-zero extraction — has this been done?**

I genuinely don't know. AV1 searched for "MUSIC + L-zeros" and found nothing. The Sym^k specifically isn't searched yet.

### What would make the "pipeline" novel

If we can show:
1. Sym^k L-zero recovery hadn't been done before via spectral estimation
2. The pipeline produces useful zeros (not just verification of known ones)
3. There's a quantitative claim (precision bound, runtime advantage)

Then it's a contribution as APPLIED math, even if the math ingredients are textbook.

### Concrete pipeline value claim

For Sym^4 Δ (degree 5):
- Classical methods (Dokchitser's computeL, etc.) require analytic setup specific to each L-function
- MUSIC pipeline: compute τ(p) once via E_4³ - E_6², then recurrence gives λ_p(Sym^k) for ALL k
- For "rapid first-pass zero estimation", MUSIC is fast and uniform
- For PRECISION zero computation, classical methods are still better

So the pipeline value is: cheap, uniform, sub-optimal precision. A "screening" tool.

## What I want

1. Honest defense of the killer-app PIPELINE value (vs the textbook ingredients).
2. State explicitly: what makes the pipeline more than "Sym^k is textbook + MUSIC is textbook = 0 contribution"?
3. The claim to make in the paper: "concept demo + theoretical CR bound + 6-10 settings" — is this publishable?

Don't overclaim. Z4 was right about ingredients being textbook. The defense is about COMPOSITION value.

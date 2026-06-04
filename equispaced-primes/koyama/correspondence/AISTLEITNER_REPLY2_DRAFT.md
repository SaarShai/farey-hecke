# Reply to Aistleitner — Second Draft
Date: 2026-04-16
Re: Mikolas 1949, W(N) second moment, prior art

---

Dear Prof. Aistleitner,

Thank you for the Mikolas paper. I have now read it carefully.

The key formula is equation (16): W(N) is expressed as a double sum
W(N) = (1/12|F_N|) · Σ_{a,b=1}^N M(N/a) M(N/b) · gcd(a,b)² / (ab) + lower-order terms,
where M(x) = Σ_{n≤x} μ(n) is the Mertens function. The diagonal terms (a = b) give
(1/12|F_N|) · Σ_{a=1}^N M(N/a)² / a²,
which matches your description. The Plancherel step is Lemma 5: a Parseval identity for the
Bernoulli-type functions p_λ(at), giving
∫₀¹ p_λ(at) p_λ(bt) dt = ζ(2λ) · gcd(a,b)^{2λ} / (ab)^λ,
making the cross-terms tractable in closed form.

For the asymptotic: Mikolas Eq. (13) gives W(N) = O(1) unconditionally, and Theorem 3 (via
Lemma 8) gives W(N) = O(N^{-1+ε}) conditionally under RH. So yes — the conditional second-
moment bound does exist in Mikolas, and we will cite it as prior art.

Our contribution is the prime-step increment ΔW(p) = W(p) − W(p−1), which is absent from
Mikolas. Differencing the double-sum formula (16) at a prime step is non-trivial: |F_p| − |F_{p−1}|
adds exactly p−1 new fractions {k/p : 1 ≤ k < p, gcd(k,p)=1}, and the cross-terms between old
and new Mertens values do not factor cleanly. Our four-term identity
ΔW(p) = (A − B' − C' − D) / n'²
gives ΔW(p) directly from M(p) and explicit Farey sums, without going through the Mikolas
double sum. The spectroscopic layer — where ΔW(p) is governed by the phase γ₁·log(p) mod 2π
via the explicit formula — is entirely outside Mikolas.

So the framing is: Mikolas establishes W(N) via Mertens double sum and gives the RH-conditional
decay rate. Our contribution is the prime-step decomposition, its exact four-term form, and the
spectroscopic behaviour at the single-prime level.

Best regards,
Saar Shai

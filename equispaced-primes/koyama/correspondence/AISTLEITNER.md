# Correspondence: Christoph Aistleitner

**Affiliation**: TU Graz (Austria)  
**Expertise**: Discrepancy theory, Farey sequences, metric number theory, low-discrepancy sequences  
**Context**: Sent paper for feedback; received direct critical assessment

---

## Timeline

| Date | Direction | Key content |
|------|-----------|-------------|
| Apr 2026 | → | Paper draft — Farey discrepancy, ΔW, Bridge Identity, spectroscope |
| Apr 2026 | ← | Critical assessment: experimental nature fair; cannot speak to W(N) asymptotics |
| Apr 2026 | → | Response: NW(N) grows slowly (0.28→0.56); Bridge Identity is concrete proved object; ask about ΔW prior art |
| Apr 15 | ← | **[Latest]** Confirms separation good idea; no heuristic for W(N) asymptotics; NW(N) is natural; references Steinerberger 1902.03269 |

---

## First Critical Reply (full text)

*"I've read your manuscript today. To be honest, in my opinion this does not match the standards of academic research-level mathematical writing - it's more a mixture of experiments and heuristics, and doesn't contain many theorems that hold in generality (beyond finite many values of primes, say). So honestly speaking it isn't to my taste - but never mind my taste, you could try to send it to a journal such as 'Experimental Mathematics' and see what happens.*

*On a mathematical level, I wonder if studying increase/decrease of W(N) is the right question. Since W(N) -> 0, there is a 'built-in' tendency of W to decrease. Maybe N W(N) might be the more interesting quantity to study - this factor might remove the 'built-in' decay and allow one to really see a 'signal' (if there is any).*

*On an abstract level, I confess I am not sure about your approach - if your Farey spectroscope really can 'see' something that the primes themselves cannot see (in the sense: we know the primes say something about the zeta zeros. Does your approach just mean: the Farey wobble has to do with primality, and primes say something about zeta zeros).*

*By the way, if you have a technical question on Dedekind sums (Conjecture 6.6), ask my young colleague Paolo Minelli: minelli@tugraz.at (but don't mention my name, to be sure you get an independent response from him)."*

---

## Apr 15 Reply (full text)

*"Yes, I guess that would be a good idea, to make a clearer separation between the 'theoretical' and the 'experimental' parts of the paper. Concerning your questions, I cannot really say... I don't know if there is any good heuristic for the 'true' asymptotic order of W(N), so I really cannot say. To me, N W(N) seems to be the most natural quantity to consider, but I don't really know.*

*As for the other question ('philosophical concern'), I understand that what you do goes beyond primes and incorporates all fractions. I don't know an answer here either, I just tried to say that this is something to think about.*

*Concerning the last question, no, I haven't seen this question before. It reminds me a very little bit of a paper of Steinerberger: the topic is the construction of low-discrepancy sequences, and it is done in a 'greedy' step-by-step way. Maybe you find this interesting - it's also somewhere between 'classical' and experimental mathematics. https://arxiv.org/abs/1902.03269."*

---

## Our Email (Apr 15, sending context)

Key points raised:

1. **On experimental/theoretical split**: Agreed to revise with Experimental Mathematics framing in mind.

2. **On N·W(N)**: Computed immediately; p·W(p) grows from ≈0.28 (p=2) to ≈0.56 (p=113). Decay slightly slower than 1/N — perhaps W(N) ~ C·log(N)/N, making N·W(N) ~ C·log(N). Asked whether N·W(N)/log(N) is the right object.

3. **On philosophical concern** (Farey wobble → primality → ζ zeros chain): Argued Bridge Identity Σ_{f∈F_{p-1}} e^{2πipf} = M(p)+2 is the concrete new element — proved identity (Lean-verified), connects full Farey set (not primes) to Mertens at p.

4. **On ΔW prior art**: Asked whether any discrepancy-theory literature tracks ΔW(p) = W(p)−W(p−1) at prime steps specifically.

---

## Key Takeaways from Aistleitner Exchange

### What he confirmed
1. **Theory/experiment split**: Correct diagnosis. We should do it. Target: Experimental Mathematics journal framing.
2. **N·W(N) natural**: His preferred quantity. He has no formula for it either — no known heuristic for W(N) asymptotics.
3. **ΔW prior art**: He has NOT seen this question before. Incremental ΔW at prime steps appears to be novel framing.

### What he didn't resolve
- True asymptotic of W(N): genuine open problem even to experts
- Philosophical novelty question: he acknowledged Bridge Identity "goes beyond primes" but left the deeper question open
- No formula or known heuristic offered for W(N) ~ ? 

### Steinerberger Connection (NEW LEAD)
- Paper: https://arxiv.org/abs/1902.03269
- Topic: greedy step-by-step construction of low-discrepancy sequences
- Aistleitner: "somewhere between classical and experimental mathematics"
- Relevance: our ΔW(p) computation is also step-by-step, greedy-like, prime-indexed
- **ACTION**: Read Steinerberger 1902.03269; check if ΔW framework connects to greedy discrepancy minimization

---

## What Aistleitner Could Help With
- Discrepancy theory framing and literature context
- Possible referee for Experimental Mathematics submission
- Connection to classical Farey discrepancy results (Hall, Franel-Landau)
- NOT: endorsement for novelty claims (appropriately cautious)

## Open Questions (from this exchange)
1. Is W(N) ~ C·log(N)/N the right ansatz? Does N·W(N)/log(N) converge?
2. Is Steinerberger's greedy construction formally related to our ΔW(p) object?
3. Can we prove ΔW novel in discrepancy literature? Aistleitner hasn't seen it — use as evidence.

## WAITING FOR
- Aistleitner response to Apr 15 draft (sent after review)
- Steinerberger 1902.03269 — read and assess formal connection to ΔW

## Apr 15 — Our Reply (sent)

*"Dear Prof. Aistleitner,*

*Thank you for the Steinerberger reference. The structural parallel is clear: Steinerberger builds sequences greedily to minimize discrepancy step by step; we are studying how discrepancy changes at each prime step of the Farey construction. Whether there is a formal connection — whether ΔW(p) > 0 can be interpreted as a "greediness failure" of the Farey sequence, or whether the minimization principle in Steinerberger's setting has a Farey analogue — is now a question we want to pursue.*

*On W(N): the empirical picture is that p·W(p) grows from ≈0.28 (p=2) to ≈0.56 (p=113) without flattening, consistent with W(N) ~ C·log(N)/N. One question we could not resolve: is there a conditional result under RH that directly bounds W(N) = Σ_{f∈F_N} D(f)²? The Franel-Landau theorem handles Σ|f_r − r/N| but we have not found a bound on this second moment in the literature. If you know of one — or are confident there isn't one — that would help us frame what is genuinely open.*

*On the philosophical concern: we now have an exact proved identity ΔW(p) = (A − B − C − N)/n'², where A, B, C, N are explicit sums over existing Farey fractions' shifts, with no reference to primality in the terms themselves. The connection to ζ zeros enters only when we evaluate the new-fraction term N at the specific set {k/p : 1 ≤ k < p}. This gives a cleaner two-layer picture: the four-term identity is Farey-intrinsic; the spectroscopic behaviour is a consequence of which fractions N inserts. We will make this separation explicit in the revision.*

*Best regards, Saar Shai"*

## WAITING FOR
- Aistleitner response to Apr 15 reply
- Steinerberger 1902.03269 — read and assess formal connection to ΔW

---

## Apr 16 — Aistleitner Reply (received)

*"Yes, there is also a bound for this second moment, probably first established by Mikolas (see the attached paper). The second moment should actually be easier than the first absolute moment, since it allows to apply Plancherel's equality. Mikolas essentially shows that W is a weighted sum of Mertens values, something like W(N) = 1/|F_N| Σ_{k=1}^N M(k)²/k² (the exact formula is in the paper)."*

### Mikolas Paper: "Farey series and their connection with the prime number problem. I." (1949)

Key results extracted:

- **Eq. (16)** — exact formula for W(N) = Σ(ρ_ν − ν/Φ)²:
  W(N) = (1/12|F_N|) Σ_{a,b=1}^N M(N/a)M(N/b)·gcd(a,b)²/(ab) + lower order
  Diagonal (a=b): (1/12|F_N|) Σ M(N/a)²/a² — matches correspondent's description

- **Eq. (13)**: W(N) = O(1) unconditionally (trivial bound via Landau)

- **Eq. (21) + Theorem 3**: Under RH, W(N) = O(N^{-1 + c·logloglog N/log log N}) — essentially O(N^{-1+ε})

- **Lemma 5** (Plancherel/Parseval): ∫₀¹ p_λ(at)p_λ(bt)dt = ζ(2λ)·gcd(a,b)^{2λ}/(ab)^λ where p_λ are Bernoulli-type Fourier series. This is why second moment is tractable.

- **Lemma 8**: RH ↔ Σ_{n≤x} (1/n^λ)M(x/n) = O(x^{1/2+ε}) for all λ ≥ 1/2

- **ΔW(p) = W(p) − W(p−1)**: NOT in Mikolas. Differencing (16) at prime step non-trivial (change in |F_N|, new fractions k/p, cross-terms).

### Implications for Our Work

1. W(N) second-moment formula: KNOWN (Mikolas 1949). Cite as prior art.
2. RH conditional bound on W(N): KNOWN. Frame what's open as ΔW(p), not W(N).
3. Our four-term identity for ΔW(p) gives prime-step increment DIRECTLY from M(p) — not in Mikolas.
4. Spectroscopic behavior of ΔW: entirely absent from Mikolas.
5. Empirical N·W(N) ~ 0.28→0.56 consistent with W(N) = O(N^{-1+ε}) under RH.


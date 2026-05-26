---
model: mimo-v2.5-pro
max_tokens: 12000
---

# V8 — Adversarial review of v4 findings (devil's advocate)

## The picture as of v4

After adversarial verification of v3:

1. NW(Q) data from exact-streaming v2 long-double C code:
   - Q=50k: 0.6642
   - Q=200k: 0.6691
   - Q=300k area: 0.698 (SPIKE PLATEAU, 4 consecutive Q)
   - Q=350k: 0.6915 (spike)
   - Q=400k: 0.6711

2. Killer-app: 8 settings verified — function field, Riemann ζ (10 zeros to 0.5%), Dirichlet L, modular form Δ, EC 11a1, Selberg/Maass, Sym² Δ, Sym³ Δ.

3. Cluster=2 (Discovery #7): >99% mass at q=0.9999, N=10⁴.

4. NW(Q) spikes are a NEW phenomenon, not in v3 doc.

## Adversarial review wanted

Pretend you're an Annals of Math referee. Reject this work. Give your 5 strongest criticisms.

Then: respond to each criticism. Which are valid? Which are addressed?

Specifically attack:

1. **The Sym² Δ and Sym³ Δ MUSIC results**: are they actually catching the right γ values, or just any peaks above noise?

2. **The cluster=2 result**: N=10⁴, 10⁵ might not be enough; cluster size could be 3 or larger asymptotically. Where's the proof?

3. **The +1/2 lag-1 correlation**: BCZ density implies this trivially. Where's the new contribution?

4. **NW(Q) spike phenomenon**: could be a coincidence of small Q values; needs Q = 10⁶, 10⁷ to confirm.

5. **D*(F^prime_N) = D*(F_N)/2**: only verified at N=5000. Asymptotic claim weak.

6. **Discovery #4 (Δ(A))**: 5 cases verified is suspicious — could have over-fit a heuristic.

## Goal

If we publish these results, what NEEDS to be addressed first? What's the weakest claim, the strongest claim, and the most overhyped claim?

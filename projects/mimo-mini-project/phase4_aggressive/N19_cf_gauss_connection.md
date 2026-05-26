---
model: mimo-v2.5-pro
max_tokens: 12000
---

# N19 — Farey, continued fractions, and Gauss map

The Farey sequence and the continued fraction algorithm are tightly linked via the Stern-Brocot tree. The Gauss map T(x) = {1/x} is the symbolic dynamics of CF.

Our findings:
- Farey gap lag-1 corr = +1/2 (level ATTRACTION)
- Cluster-size = 2 in extremes
- NW(Q) has spikes at specific Q

Continued fraction statistics:
- Lévy's constant: e^{π²/(12 ln 2)} = limit of (a_n)^{1/n} for typical x (a_n = nth CF partial quotient)
- Kuzmin's theorem: distribution of CF tails
- Gauss-Kuzmin-Lévy statistics

## Question

Is there a Gauss-map / CF analog of:

1. **Lag-1 correlation = 1/2** for the sequence of CF partial quotients (a_1, a_2, ...)?

2. **Cluster-size = 2** for extreme partial quotients?

3. **Specific x where CF statistics spike** (analog of NW(Q) spikes at specific Q)?

If Farey ↔ CF correspondence preserves these structures, we get new Gauss-map invariants.

## Possible connection to "Markov spectrum"

The Markov spectrum is the set of values lim sup (a_i a_{i+1} ... a_{i+k}) for various windows. It has known structure: discrete values below Freiman's constant 4.5278..., continuous above.

Question: Do our "spike" Q values correspond to x ∈ [0,1] with specific Markov spectrum properties?

## Concrete asks

1. Reference for the bridge between Farey gap statistics and CF partial quotient statistics (Marklof-Strömbergsson? Sinai-Ulcigrai?).

2. Is the lag-1 = 1/2 a known property of either Farey or CF?

3. If we apply our MUSIC algorithm to CF partial quotients (treating them as sources of a discrete spectrum), what L-zeros (if any) emerge?

4. Specific reference: Doeblin-Lenstra constant, Khintchine-Lévy theorem, Aaronson-Denker.

Honest answers only — if you don't know, say so.

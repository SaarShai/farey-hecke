---
model: mimo-v2.5-pro
max_tokens: 14000
---

# L2 — Literature review: lag-1 correlation of consecutive Farey gaps = 1/2

## The empirical fact

For Farey sequence F_N gaps d_i, I find lim_{N→∞} Corr(d_i, d_{i+1}) = **1/2** (empirically 0.382 at N=50k, extrapolation to 1/2 via 1/log(N) decay).

## Your task

Search the literature for explicit statements:

1. **Boca-Cobeli-Zaharescu** (multiple papers 2001-2005): they explicitly derived the joint density of consecutive Farey gaps. Did they compute the lag-1 Pearson correlation?

2. **Athreya-Cheung IMRN 2014**: their BCZ-flow renewal framework. They discuss limiting distributions of gaps. Did they compute the correlation?

3. **Hall, R. R.** ("On the Mertens function" and Farey papers): any correlation-type statements?

4. **Hardy-Littlewood / Schoenberg**: classical Farey gap distribution work — any correlation results?

5. **Random matrix theory analogy**: lag-1 correlation = 1/2 is reminiscent of certain log-correlated processes. Is there an RMT result showing the same constant?

6. **Diophantine approximation literature**: anyone explicitly note 1/2 for consecutive Farey gap correlation?

State for each:
- Is the result published with value 1/2?
- Is something nearby published (e.g., autocorrelation function, joint moments)?
- If not, this is a clean numerical observation worth documenting.

Honesty note: if your search is limited (no access to specific papers), say so explicitly.

# D10 — Is 1/lambda^3 a length-spectrum / systole invariant of (2,q,inf) Hecke orbifold?

**Date:** 2026-06-14. **Verdict: NEGATIVE (well-supported). One EXACT but ALGEBRAIC restatement
via the systole; NO length-spectrum equality and NO log-scale bridge.**

## Concrete computed facts (mpmath dps=40, q=3..21)
- Shortest hyperbolic primitive of G_q = <S,T> is **ST^2** (=S T T) for q>=4, found by BFS over
  reduced words len<=6. Its trace is **EXACTLY 2*lambda = 4 cos(pi/q)** (ST^n has trace n*lambda;
  n=2 is the first hyperbolic since lambda*1<2<=2*lambda for q>=4). q=3: ST^2 is PARABOLIC (tr 2),
  systole comes from STST^{-1}, tr 3, L=2 arccosh(3/2)=1.9248.
- Systole **L_sys = 2 arccosh(2 cos(pi/q))**, so **lambda = cosh(L_sys/2)** EXACTLY (trace-length
  dictionary |tr|=2cosh(L/2)). This is a standard triangle-group fact (Schmidt-Sheingorn,
  Length spectra of the Hecke triangle groups, Math. Z. 220 (1995); triangle-group geodesics
  have the form 2 arccosh(.) in cos(pi/q)) -- NOT novel.

## The candidate identity and why it is only algebraic
- From lambda=cosh(L_sys/2): **1/lambda^3 = sech(L_sys/2)^3 = 8/(systole trace)^3.** EXACT.
- But this is a function of the systole TRACE, not equal to any length-spectrum LENGTH. It is a
  cube of the trace-length dictionary, not a geometric invariant in the rigidity sense.
- **Log-scale bridge FAILS:** exp(-L)=1/lambda^3 would need L=3 log(lambda); a geodesic of that
  length needs trace = lambda^{3/2}+lambda^{-3/2} (non-integer power of lambda) which is NOT a
  trace of any group element. So there is NO closed geodesic of length 3 log(lambda).

## Other geometric quantities ruled out
- Hyperbolic AREA(G_q)=pi(1-2/q) -> pi as q->inf; 1/lambda^3 -> 0.118. No match.
- Cusp width / max-horoball horocycle length are all O(lambda) or O(1/lambda) (linear), never a
  CUBE. 1/lambda^3=(1/lambda)^3 cannot be a single geodesic or horocycle length.

## Where the cube actually comes from (consistent with exp_energy_cusp note)
- 1/lambda^3 = (1/lambda)^2 * (1/lambda): the cusp-periodic orbit grazes (s,0), s->1/lambda;
  P=s^2/lambda. Two cusp-coordinate factors + one branch-jacobian factor. Origin is the BCZ
  cross-section gap-PRODUCT (an AREA in the (a,b) section coords), NOT a hyperbolic length.
  This is why a length-spectrum identity was never going to land: 1/lambda^3 is an
  area/cross-section object, the length spectrum is a length object.

## Bottom line
The honest, novelty-aware result: **lambda=cosh(L_sys/2)** ties 1/lambda^3 to the systole TRACE
algebraically (and that trace fact is already in the Hecke literature), but **1/lambda^3 is not
itself a length, area, cusp-width, or horocycle-length invariant**, and the log bridge to a
geodesic length is provably empty. NOT a length-spectrum-rigidity bridge. Do not re-propose.

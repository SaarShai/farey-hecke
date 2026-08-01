# Local numerical evidence — 2026-07-18

## Build and run

```sh
cc -O3 -std=c11 -Wall -Wextra -o /tmp/nw_mertens_reproduce reproduce_numerics.c -lm
/tmp/nw_mertens_reproduce delta 92173
/tmp/nw_mertens_reproduce cross 237733 243799
```

`reproduce_numerics.c` is self-contained.  It computes `M(p)` with a linear
Möbius sieve and enumerates the relevant Farey sequence with the standard
successor recurrence.  Squares and cross-term summands use compensated
`long double` accumulation.

## Definitions

For `delta`, the program uses the zero-indexed Farey order
\(\mathcal F_N=\{f_j\}_{j=0}^{|\mathcal F_N|-1}\) and

\[
 W(N)=\sum_j\left(j/|\mathcal F_N|-f_j\right)^2,
 \qquad \Delta W(p)=W(p-1)-W(p).
\]

For `cross`, it uses the separate R1 convention

\[
 B_{\rm R1}(p)=2\sum_{f=a/b\in\mathcal F_{p-1}}
 \left(\operatorname{rank}_{\rm R1}(f)-|\mathcal F_{p-1}|f\right)
 \frac{a-(pa\bmod b)}b,
\]

where \(\operatorname{rank}_{\rm R1}(0/1)=1\).  `B_R1` is not `ΔW`.

## Recorded outputs

```text
$ /tmp/nw_mertens_reproduce delta 92173
definition=deltaW W(N)=sum_{j=0}^{|F_N|-1}(j/|F_N|-f_j)^2
p=92173 M(p)=-2 |F_(p-1)|=2582383991 |F_p|=2582476163
W(p-1)=7.250559484613499687207828e-06
W(p)=7.250523870205767020240967e-06
deltaW=3.561440773266696686177868e-11 sign=positive

$ /tmp/nw_mertens_reproduce cross 237733
definition=B_R1=2sum D_R1(f)delta_p(f), rank_R1(0/1)=1
p=237733 M(p)=-20 |F_(p-1)|=17178971883
B_R1=-3.018492026640170288085938e+10 sign=negative

$ /tmp/nw_mertens_reproduce cross 243799
definition=B_R1=2sum D_R1(f)delta_p(f), rank_R1(0/1)=1
p=243799 M(p)=-3 |F_(p-1)|=18066862385
B_R1=-9.190201299936826705932617e+09 sign=negative
```

## Consequences with no overreach

- `92173` falsifies \(M(p)<0\Rightarrow\Delta W(p)\leq0\).
- `237733` and `243799` falsify restricted R1 cross-term positivity on
  \(M(p)\leq-3\).
- These finite computations say nothing about a density, a limiting
  probability, a universal ΔW law, or RH.

## Precision boundary

The signs are stable in the recorded `long double` calculations, but this is
not an interval proof.  No claim here relies on an unrecorded MPFR run.

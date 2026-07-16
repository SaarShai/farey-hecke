# Draft follow-up to Rogelio Tomás García

Subject: Re: Farey rank discrepancy, Mertens structure, and a question on novelty

Hi Rogelio,

A substantial update to the \(L^2\) companion I sent earlier: after matching
the notation to Conjecture 1, we found a fourth-moment argument that appears to
prove the missing lower half as well.  In other words, it appears to prove the
full qualitative conjecture, although not your sharper provisional constants.

With \(\Delta_j=g_j-1/N\),
\(\sigma_g^2=N^{-1}\sum_j\Delta_j^2\), and
\(S_i^\pi=\sum_{j\le i}\Delta_{\pi(j)}\), sampling without replacement gives
\[
 \mathbb E(S_i^\pi)^2
 =\sigma_g^2\frac{i(N-i)}{N-1}.
\]
An exact fourth-moment expansion also gives the sharp universal bound
\[
 \mathbb E(S_i^\pi)^4
 \le \frac13\left(\sum_j\Delta_j^2\right)^2.
\]
Applying \(L^1\)--\(L^2\)--\(L^4\) interpolation to the central prefix indices
and summing yields
\[
 \frac9{160}\,\sigma_gN^{3/2}
 \le \mathbb E_\pi\sum_{i=1}^{N-1}|S_i^\pi|.
\]
Cauchy--Schwarz gives the other side,
\[
 \mathbb E_\pi\sum_{i=1}^{N-1}|S_i^\pi|
 \le \frac{\sigma_g}{\sqrt{N-1}}
      \sum_{i=1}^{N-1}\sqrt{i(N-i)}
 \le \frac1{\sqrt6}\sigma_gN^{3/2}.
\]
Therefore Conjecture 1 holds with the explicit conservative constants
\(c_1=9/160\) and \(c_2=1/\sqrt6\), provided I have matched your averaging
convention correctly.  Repeated gaps cause no change: every distinct ordering
has the same number of labelled preimages.

The ingredients need careful attribution.  The prefix-variance identity
appears in equivalent normalization in Pozdnyakov--Steele (2013), and the
sampling-without-replacement fourth moments go back at least to Isserlis
(1931).  The finite-population moment machinery is classical.  What may be new
in this context is its application to deduce your qualitative two-sided bound.
I have not found that consequence in a focused search, but I would value your
view on whether it is known in another notation.

There is also the exact continuous \(L^2\) companion
\[
 \mathbb E_\pi D_2(\pi)^2
 =\frac1{3N^2}+\frac{\sigma_g^2(N+1)}6.
\]
The underlying one-dimensional \(L^2\)-discrepancy identity is classical
(Koksma--Warnock; see also Kirk--Pausinger); the new point here is again its
specialization to your fixed-gap permutation model.
Together, these formulas give an \(O(N)\) certificate in place of averaging
over up to \(N!\) permutations.  We checked it against exhaustive rational
enumeration through \(N=8\), repeated-gap cases, and a million-gap scaling
case without materializing a permutation.

One separate result also answers your earlier question about the shift
\(\delta_p(f)=f-\{pf\}\): for the old interior fractions of \(F_{p-1}\), its
distribution converges to the triangular density \(1-|t|\), every odd moment
vanishes exactly, and
\[
 \sum_f\delta_p(f)^2
 =\frac{p^2}{2\pi^2}+O_\varepsilon(p^{1+\varepsilon}).
\]
This settles the shift-squared leading constant without reviving the failed
global sign conjecture.

We obtained this through the falsify/verify stages of our Aletheia workflow and
now have a compact proof-and-test bundle.  If useful, I would be glad to send
it and discuss whether the gap-permutation theorem belongs in a short follow-up
or joint note.  Your check of the interpretation and prior-art boundary would
be especially valuable.

Best regards,

Saar

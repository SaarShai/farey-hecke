# B(q) rotation-arc breakthrough: closed continuous width + scalar resonance gate

Date: 2026-06-18  
Target branch: `hecke-goalL-2026-06-03`  
Scope: follow-up to `research_notes/Bq_rotation_arc_2026-06-14.md`.

## /goal

Turn the corrected rotation-arc mechanism into a sharper theorem target:

1. replace the grid-computed continuous width `W(q)` by a closed formula;
2. extract the exact asymptotic constant and first correction terms;
3. reduce the `+1` resonance to a scalar interval inequality;
4. identify new high-value resonance targets beyond q=23 and q=61.

## Result 1: closed form for the continuous governing width

Let

\[
\theta=\pi/q,\qquad \lambda=2\cos\theta,\qquad r=\tan(\theta/2).
\]

On the governing ellipse

\[
E(a,b)=a^2-\lambda ab+b^2=E_*:=\frac{2-\lambda}{\lambda^3},
\]

write

\[
s=\frac{a+b}{2},\qquad d=\frac{a-b}{2}.
\]

Then

\[
E=(2-\lambda)s^2+(2+\lambda)d^2,
\]

and a convenient angular parametrization is

\[
s=\lambda^{-3/2}\cos\psi,
\qquad
 d=\lambda^{-3/2}r\sin\psi,
\qquad r=\sqrt{\frac{2-\lambda}{2+\lambda}}=\tan(\theta/2).
\]

The last-branch lower edges reduce to

\[
a+\lambda b>1,
\qquad
\lambda a+b>1.
\]

Equivalently, for a symmetric arc about the peak `a=b`, the binding inequality is

\[
(1+\lambda)\cos\psi-(\lambda-1)r|\sin\psi|>\lambda^{3/2}.
\]

Therefore the continuous half-width \(\alpha_q\) is the unique positive solution of

\[
(1+\lambda)\cos\alpha_q-(\lambda-1)r\sin\alpha_q=\lambda^{3/2}.
\]

So the continuous width is not a grid/root-finding object. It is explicit:

\[
\boxed{
W(q)=2\alpha_q
=2\left[
\arccos\left(
\frac{\lambda^{3/2}}
{\sqrt{(1+\lambda)^2+((\lambda-1)r)^2}}
\right)
-
\arctan\left(\frac{(\lambda-1)r}{1+\lambda}\right)
\right].
}
\]

This agrees with the repo's grid values from `goal1_Bq_arc_width_asymptotic.py`:

| q | closed W(q) | W(q)q/π | floor+1 |
|---:|---:|---:|---:|
| 7 | 0.9349194947 | 2.083158826 | 3 |
| 13 | 0.7321013976 | 3.029456463 | 4 |
| 19 | 0.6891414738 | 4.167850338 | 5 |
| 23 | 0.6786995407 | 4.968845792 | 5 |
| 24 | 0.6770397706 | 5.172202856 | 6 |
| 30 | 0.6712109007 | 6.409591962 | 7 |
| 40 | 0.6684550588 | 8.511034147 | 9 |
| 61 | 0.6689641279 | 12.989211621 | 13 |

## Result 2: exact limiting slope

As \(q\to\infty\), \(\lambda\to2\) and \(r\to0\). The boundary equation becomes

\[
3\cos\alpha_\infty=2\sqrt2.
\]

Since \(\sin\alpha_\infty=1/3\),

\[
\boxed{W_\infty=2\alpha_\infty=2\arcsin(1/3)=2\arccos(2\sqrt2/3).}
\]

Numerically,

\[
W_\infty=0.679673818908243\ldots,
\qquad
\frac{W_\infty}{\pi}=0.216346895938785\ldots.
\]

This replaces the empirical “≈0.216” slope by an exact geometric constant.

More sharply, expanding the boundary equation at \(\theta=0\) gives

\[
\boxed{
W(q)=2\arcsin(1/3)-\frac{\pi}{3q}
+\frac{31\sqrt2\,\pi^2}{18q^2}
+O(q^{-3}).
}
\]

Consequently the continuous/no-notch count satisfies

\[
B_0(q)=\left\lfloor \frac{2\arcsin(1/3)}{\pi}q-\frac13
+\frac{31\sqrt2\,\pi}{18q}+O(q^{-2})\right\rfloor+1.
\]

## Result 3: scalar resonance gate

The corrected note says q=23 beats the continuous proxy because the rotation lattice hops over a narrow super-threshold notch. The same mechanism has a closed scalar test.

Let

\[
B_0(q)=\lfloor W(q)q/\pi\rfloor+1,
\qquad N=B_0(q)+1.
\]

A `+1` resonance can only occur when \(N\) is even. If \(N\) is odd, the symmetric lattice has a point on the peak `a=b`, so any `frac>1` notch regime impales the peak and fails.

For even \(N\), define

\[
\psi_{\rm ext}=\frac{N-1}{2}\theta,
\]

\[
D_N(q)=(1+\lambda)\cos\psi_{\rm ext}
-(\lambda-1)r\sin\psi_{\rm ext},
\]

and

\[
G(q)=\cos^2(\theta/2)-r^2\sin^2(\theta/2).
\]

The extreme points enter the last-branch domain when

\[
\rho>\rho_{\min}:=\left(\frac{\lambda^{3/2}}{D_N(q)}\right)^2,
\]

where \(\rho\) is `peak_ab / threshold`. The nearest-to-peak points remain sub-threshold while

\[
\rho<\rho_{\max}:=\frac{1}{G(q)}.
\]

So the scalar resonance criterion is

\[
\boxed{
R(q)=1
\iff
N=B_0(q)+1\text{ is even and }1<\rho_{\min}<\rho_{\max}.
}
\]

Then the corrected rotation-arc model predicts

\[
\boxed{B(q)=B_0(q)+R(q).}
\]

This isolates the hard residual to a one-line interval inequality in \(q\).

## Verified resonance targets

Using the scalar gate:

| q | B0 | predicted B | W(q)q/π | rho_min | rho_max | status |
|---:|---:|---:|---:|---:|---:|---|
| 23 | 5 | 6 | 4.968845792 | 1.001617274 | 1.004700811 | repo-known resonance |
| 61 | 13 | 14 | 12.989211621 | 1.000198559 | 1.000663835 | repo-known resonance |
| 126 | 27 | 28 | 26.987159704 | 1.000113498 | 1.000155457 | new predicted resonance |
| 570 | 123 | 124 | 122.997826554 | 1.000004236 | 1.000007594 | new predicted resonance |

High-precision symmetric-run checks confirm the lower-bound witnesses for q=126 and q=570:

| q | N | k-pattern | min domain margin | min threshold gap |
|---:|---:|---|---:|---:|
| 126 | 28 | `[1 × 27, 2]` | 1.048856648e-5 | 2.624491823e-6 |
| 570 | 124 | `[1 × 123, 2]` | 8.396561857e-7 | 2.099229947e-7 |

These are not just continuous-width predictions: the actual symmetric lattice points are in the last branch, are sub-threshold, and have the expected terminal `k=2` ejection pattern. The upper-bound side still relies on formalizing the symmetric-longest-run / parity gate interface that the repo is already building.

A double-precision scan of the scalar gate gives predicted resonances up to q=10,000:

\[
q=23,61,126,570,1476,1892,6884.
\]

The first four are numerically comfortable. The larger three should be rechecked with interval arithmetic before being treated as certified.

## Proof tasks now smaller than before

The old proof target was: “derive B(q).”  
The new target decomposes into four clean lemmas:

1. **Branch-vector simplification.**  Prove from Chebyshev/sine identities that
   \[
   w_{q-1}=(0,1),\qquad w_{q-2}=(1,\lambda),\qquad w_q=(-1,0).
   \]

2. **Continuous width lemma.**  Formalize the `(s,d)` parametrization and prove the closed formula for `W(q)` above.

3. **Asymptotic lemma.**  Prove
   \[
   W(q)=2\arcsin(1/3)-\pi/(3q)+O(q^{-2})
   \]
   first, then optionally the sharper \(31\sqrt2\pi^2/(18q^2)\) term.

4. **Resonance interval lemma.**  Prove the scalar gate
   \[
   R(q)=1 \iff N\text{ even and }1<\rho_{\min}<\rho_{\max}.
   \]

This is a better formalization route than trying to make Lean reason over a grid/root-find. The theorem has become trigonometry, not fog.

## Caveats

This note sharpens the corrected rotation-arc model. It does not by itself close the global genuine-map theorem for every q. The remaining repo-level bridge is still the same bridge flagged in `Bq_rotation_arc_2026-06-14.md`: cluster confinement/realization/maximality must connect the scalar arc theorem to the genuine Taha BCZ map for all q.

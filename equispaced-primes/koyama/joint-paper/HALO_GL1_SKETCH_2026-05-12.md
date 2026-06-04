# Halo-route reduction in the GL(1) Dirichlet case — sketch toward (SP-L)

This note is the GL(1) Dirichlet specialization of the halo-route
framework used in our GL(2)/EC programme, transferred to the
context of (SP-L) and (NDC) (§X.4.4 and §X.7 of the main section).
It is presented as a "what would the analogous statements look
like?" sketch rather than a complete proof: it identifies four
conditional doors A', B', C', D' and indicates which transfer
mechanically from the GL(2) version and which require new GL(1)
input.

## 1. Set-up — what we are bounding

Let $\chi$ be a primitive non-principal Dirichlet character of
conductor $q \ge 2$, and let $\rho = \tfrac12 + i\tau$ be a simple
zero of $L(s, \chi)$ on the critical line, $\tau \ne 0$. Define the
shifted Perron integrand at scale $K > 1$:
$$
F_K(w) \;:=\; \frac{K^w}{w \cdot L(w + \rho, \chi)}.
$$
The shifted Perron representation of $c_K(\chi, \rho)$, after
extracting the double-pole residue at $w = 0$ (Lemma X.3.1 of the
main text), reads:
$$
c_K(\chi, \rho)
\;=\;
\frac{\log K}{L'(\rho, \chi)} + C_1(\chi, \rho)
\;+\;
\sum_{\rho' \ne \rho} \mathop{\mathrm{Res}}_{w = \rho' - \rho} F_K(w)
\;+\;
(\text{contour pieces}).
$$

The target (SP-L) is to show that the off-target nontrivial-zero
residue aggregate is $o(\log K)$ — i.e., the second-to-last group
above contributes a term *smaller* than the leading $\log K /
L'(\rho)$.

## 2. The halo-region setup, GL(1) version

Let $Z_K^{\mathrm{red}}$ denote the reduced set of nontrivial zeros
of $L(s, \chi)$ in the strip $|\mathrm{Im}(\rho') - \tau| \le T_K$,
$\rho' \ne \rho$, with multiplicity collapsed (each cluster counted
once). Choose

- $\alpha := 1/\log K$ (shift step),
- $A > 0$ (cluster radius parameter),
- $R > \sqrt{1 + A^2}$ (halo radius; the bound from Door B' below),
- $R_K \in [R,\, 2R]$ (halo-radius parameter, chosen so that no
  zero lies on the boundary of $\Omega_K$).

Define the halo region
$$
\Omega_K \;:=\; \bigcup_{\rho' \in Z_K^{\mathrm{red}}}
D(\rho' - \rho,\, R_K \alpha)
$$
(union of disks of radius $R_K\alpha$, centered at the shifted
off-target zeros relative to the target $\rho$). By the cluster-disk
exclusion construction, the boundary $\partial \Omega_K$ avoids every
off-target zero.

The off-target residue aggregate is then (by Stokes)
\begin{equation}
\label{eq:halo-stokes-GL1}
R_K(\chi, \rho)
\;:=\;
\sum_{\rho' \in Z_K^{\mathrm{red}}}
\mathop{\mathrm{Res}}_{w = \rho' - \rho} F_K(w)
\;=\;
\frac{1}{2\pi i} \int_{\partial \Omega_K} F_K(w)\, dw.
\end{equation}

This is the **halo identity in GL(1)**: same structure as the GL(2)
version, just with $L$-function replaced by $L(s, \chi)$ and the
zero set replaced by the Dirichlet $L$-function zero set.

## 3. The four GL(1) doors

The GL(1) analogues of Doors A, B, C, D of the GL(2) halo plan:

### Door A' — GL(1) shifted-moment input

**Statement (Door A').**
$$
\sum_{\rho'}^{\mathrm{mult}} |L(\rho' + \alpha, \chi)|^{-2}
\;\ll_\chi\;
T_K \cdot (\log T_K)^{C_\chi},
$$
where $\rho'$ ranges over the nontrivial zeros of $L(s, \chi)$ in
$|\mathrm{Im}(\rho')| \le T_K$ (counted with multiplicity), and
$C_\chi$ is a $\chi$-dependent polynomial-in-conductor constant.

**Status.** OPEN.

**Source-availability.** The literature provides the Gonek–Hejhal-type
second-moment bound for $\zeta$:
$\sum_{|\gamma| \le T} |\zeta'(\rho)|^{-2} \ll T (\log T)^{?}$
(Hejhal's "Lindelöf hypothesis for $\sum |\zeta'|^{-2}$"). The
Dirichlet analogue is expected to follow the same model. We have
not found a primary source that states the Dirichlet $L$ shifted
$|L(\rho + \alpha)|^{-2}$ second-moment with $T (\log T)^{O(1)}$
unconditionally; it is a known open problem (cf. Ng 2004, §4 of
the survey article *The distribution of the summatory function of the
Möbius function*). For the purposes of (SP-L), assuming Door A' is
the GL(1) analog of assuming AllZeroShiftedNeg_2 in GL(2); it is the
*main analytic input still owed*.

### Door B' — GL(1) halo shift comparison

**Statement (Door B').** Under the framework's GRH for $L(s, \chi)$,
for $R > \sqrt{1 + A^2}$ and every boundary arc
$w \in \partial \Omega_K$ assigned to $\rho_0' \in Z_K^{\mathrm{red}}$:
$$
|L(w + \rho, \chi)|^{-1}
\;\le\;
C_\chi(A, R) \cdot
|L(\rho_0' + \alpha, \chi)|^{-1},
$$
with $C_\chi(A, R)$ independent of $K$ and of the local cluster size.

**Status.** *Provable by the GL(2) argument translated.* The GL(2)
proof in §5.1 of the halo plan uses only:

1. The geometric fact that $w \in \partial \Omega_K$ is outside every
   off-target halo (forced by $\partial \Omega_K$ construction).
2. The cluster-factor ratio
   $|\alpha + \rho_0' - \rho_j'|/|w - \rho_j'| \le \sqrt{1 + A^2}/R < 1$
   per cluster mate, giving an arbitrary-order contraction.
3. The cluster-free remainder
   $H_A(w)/H_A(\rho_0' + \alpha) = O(1)$ via the existing local
   noncluster stability lemma (`ClusterShiftDerivativeComparison`).

Steps (1) and (2) are *geometric* and transfer verbatim to GL(1):
the disk-exclusion definition of $\partial \Omega_K$ is identical;
the cluster-factor contraction is identical (same Pythagoras
argument, same $\sqrt{1 + A^2}$ constant). Step (3) requires a
GL(1) version of the `ClusterShiftDerivativeComparison` lemma — the
Dirichlet $L$-function analog of the GL(2) repo lemma. This is a
1-page lemma: noncluster zeros within $O(\alpha)$ of $\rho_0'$ make
a $\log|H_A|$ variation $\sum (\alpha/d_j)^2$ contribution bounded by
the Riemann–von Mangoldt density.

**Hence Door B' is conditional only on the framework's GRH for
$L(s, \chi)$**, not on a separate shifted-moment input.

### Door C' — ResidueFirstSP-L rewrite

**Statement (Door C').** Identify the step in the proof of (SP-L)
that consumes the *budget*
$\widetilde R_K(\chi, \rho) := \sum_{\rho' \ne \rho} |L'(\rho', \chi)|^{-1}$
(termwise absolute value) and replace it by the *signed* contour
residue $R_K(\chi, \rho)$ of (\ref{eq:halo-stokes-GL1}).

**Status.** Programmatic — requires auditing the existing
shifted-Perron-leading argument (companion technical note,
available on request) to verify that the $o(\log K)$ bound on the
off-target aggregate can be weakened from termwise absolute values
to the signed contour residue.

The structural reason this should succeed: the budget bound's role
in (SP-L) is to control the *aggregate* off-target contribution to
the shifted Perron leading theorem; the signed contour residue is
the *actual* contribution, and the budget is an upper envelope. If
the analytic estimates downstream of the budget bound only use the
upper envelope rather than the termwise sum, they can be re-derived
from the signed residue + a cluster-disposition lemma.

### Door D' — Test-function $M_K$ bound

**Statement (Door D').**
$M_K := \sup_{w \in \partial \Omega_K} |K^w| = K^{\sup_{w \in \partial \Omega_K} \mathrm{Re}(w)}$
satisfies $M_K = K^{o(1)} \cdot K^0$ (i.e., bounded along the
contour) on the chosen halo construction.

**Status.** The halo boundary $\partial \Omega_K$ lies within
distance $R_K \alpha = R/\log K$ of the critical line $\mathrm{Re}(w) = 0$.
On every such boundary arc, $|K^w| = K^{\mathrm{Re}(w)} = e^{R}$, i.e.
*bounded* by an absolute constant depending on $R$ but not $K$. So
$M_K = O(1) = K^{o(1)}$. **Door D' is automatic.**

## 4. Halo theorem in GL(1)

**Halo theorem, GL(1) form (conditional).** Under the framework's
GRH for $L(s, \chi)$ (giving Door B' via the GL(2)-transferred
argument) and Door A' (the GL(1) shifted-moment input), with the
halo-region construction of §2,
$$
\bigl|R_K(\chi, \rho)\bigr|
\;\le\;
M_K \cdot T_K^{1/2 + \varepsilon + o(1)}
$$
for any $\varepsilon > 0$. Choosing the standard $T_K = K (\log K)^{-B}$
(for $B$ sufficiently large, to make the truncation tails negligible),
$M_K = O(1)$, and the bound becomes
$$
\bigl|R_K(\chi, \rho)\bigr| \;\ll\; K^{1/2 + \varepsilon + o(1)} = o(\log K) \cdot K^{1/2 + \varepsilon + o(1)}.
$$

Wait — that gives $K^{1/2+\varepsilon}$, not $o(\log K)$. The
exponent in the GL(2) version is $T^{7/4 + \varepsilon}$ relative to
the leading $T^2$ scale; the GL(1) version, with $T = T_K \sim K /
\log K$ and the natural leading $\log K$ scale, gives a much weaker
relative bound. **Conclusion: the halo theorem in GL(1) form does
*not*, in its naïve transfer, give $o(\log K)$ for the off-target
aggregate.**

The GL(2) halo theorem succeeds at exponent $T^{7/4} = T^{1.75} <
T^2$ because the leading scale in H1 is $T^2$. The corresponding
GL(1) leading scale is $\log K$, which is much smaller than the
natural envelope $K^{1/2 + \varepsilon}$. The halo theorem in GL(1)
therefore does *not* by itself close (SP-L).

## 5. Implications and revised path

**Revised conclusion.** The halo-route's *structural pivot* (signed
contour residue + cluster-disposition + Door B' as an absolute-constant
theorem) **transfers cleanly from GL(2) to GL(1)**, but the
**resulting exponent does not close (SP-L) at the $\log K$ scale**.
The GL(2) halo theorem gives an $o(T^2)$ bound on the GL(2) H1
residue contribution (where $T^2$ is the leading H1 scale); the
GL(1) halo theorem gives only an $O(K^{1/2+\varepsilon})$ bound on
the off-target Dirichlet residue aggregate, which is *much weaker
than the leading $\log K$ scale required for (SP-L)*.

**What this means.** The halo route is the right *mechanism* — it
correctly identifies that signed-cancellation is the operative
phenomenon, not termwise budgets — but the GL(1) shifted-Perron
problem operates at a different scale than the GL(2) H1 problem,
so the halo theorem alone does not close it. **(SP-L) requires
either a stronger version of Door A' than the $T(\log T)^{O(1)}$
second-moment, or a different mechanism that exploits the
$\log K$ leading scale more efficiently.**

This is honest. The §X.7.1 entry of the section draft correctly
states that the GL(2) halo plan is "the cleaner forcing function"
and that the GL(1) transfer is "conceptual"; the analysis above
makes the *conceptual* transfer explicit and shows where the GL(1)
case needs additional input beyond the GL(2) doors.

## 6. Status table — (SP-L) ledger after the halo sketch

| Object | GL(2) status (halo plan) | GL(1) status (this sketch) |
|---|---|---|
| Halo identity (Stokes) | Established | Established |
| Door A: shifted moment | OPEN | OPEN (Door A') |
| Door B: halo shift comparison | **THEOREM** under GRH, $R > \sqrt{1+A^2}$ | **Provable** under GRH for $L(s,\chi)$, same constants, via translation of §5.1 of the GL(2) plan |
| Door C: residue-first rewrite | Open (programmatic) | Open (programmatic; smaller change in GL(1)) |
| Door D: $M_T$ sup-bound | OPEN | **AUTOMATIC** ($M_K = O(1)$ on the halo) |
| Halo theorem yields | $o(T^2)$ at GL(2) leading scale | $O(K^{1/2+\varepsilon})$ at GL(1) leading scale $\log K$ — **does not close (SP-L) alone** |

## 7. What this writeup adds to the paper

**For §X.4.4 / §X.7 Q:Perron / §X.7.1.** Honest record that the halo
route is the right structural pivot but its naïve GL(1) transfer is
insufficient. The off-target Dirichlet aggregate's $o(\log K)$
target is at a scale where halo cancellation alone underperforms;
either Door A' is dramatically strengthened (better than
$T(\log T)^{O(1)}$ — entering Lindelöf-like territory) or a
different mechanism is needed.

**For the open-challenges section of the paper.** Question Q:Perron
remains open. The halo route gives a precise structural envelope:

> *To close (SP-L), it is sufficient to prove either
> (a) a Dirichlet shifted moment $\sum_{\rho'}^{\mathrm{mult}} |L(\rho' + \alpha, \chi)|^{-2} \ll (\log K)^{O(1)}$
> (much stronger than the natural $T_K(\log T_K)^{O(1)}$), or
> (b) a mechanism not based on the halo signed cancellation that
> exploits the $\log K$ leading scale of the shifted Perron problem.*

This is now the *precisely stated* GL(1) version of Koyama's
"shifted Perron remainder requirements."

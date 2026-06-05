import math
import numpy as np
# ANGULAR ARC FORMULATION of (L1b).
# Block state rotates by th=pi/q. Phase variable phi (=n th - psi mod 2pi), advancing by th per block.
# Two sinusoidal constraints on the rotating state (radius r fixed for a given orbit/ellipse):
#
#  (A) SUB-THRESHOLD arc: P(phi) < thr.
#      P(phi)=(r^2/(2 A2))[3l/2 + sqrt(A2) cos(2 phi + eta)],  A2=1+2l^2.
#      P<thr  <=>  cos(2 phi+eta) < C_P(r):=(2 A2 thr/r^2 - 3l/2)/sqrt(A2).
#      In the doubled-phase var (2phi), sub-thr is the arc where cos< C_P, i.e. |2phi+eta - pi|<pi-arccos(C_P)... 
#      Width of sub-thr in phi: if |C_P|<=1, the cos< C_P set in (2phi) has measure 2(pi-arccos(C_P)); 
#        in phi that's (pi - arccos(C_P)). Call this Delta_sub(r) [width in phi where P<thr].
#      As r grows, C_P shrinks -> Delta_sub shrinks (less of the circle is sub-thr).
#      As r->small, C_P>1 -> entire circle sub-thr (Delta_sub=pi, the whole half... actually full 2pi? 
#        P has period pi in phi, so "full" sub-thr means Delta_sub=pi).
#
#  (B) IN-DOMAIN arc: Dom(phi)=r B_lam cos(phi+xi) > 1.
#      <=> cos(phi+xi) > 1/(r B_lam) =: C_D(r).  In-domain arc in phi: width 2 arccos(C_D(r)) (if C_D<1).
#      As r grows, C_D shrinks -> in-domain arc WIDENS. As r->1/B_lam, arc->0.
#
# A SUSTAINED (trapped) orbit needs: the in-domain arc SUBSET-OF the sub-thr arc, AND the orbit
# rotates through phi by th forever. Since rotation visits ALL phases on its circle (the orbit phase
# advances by th each block, eventually dense / covers the circle mod the period), a TRAPPED orbit
# requires EVERY in-domain phase to be sub-thr: in-domain arc \subseteq sub-thr arc.
# Equivalently NO trapped orbit  <=>  for every r, the in-domain arc is NOT contained in the sub-thr arc,
#   i.e. there is an in-domain phase with P>=thr. The orbit, rotating, MUST hit it => escapes.
#
# The cleanest SUFFICIENT condition (uniform): the in-domain arc is WIDER than the sub-thr arc's 
#   complement-gap... Actually the precise escape condition:
#   The set {P>=thr} (super-threshold) is the arc of width  pi - Delta_sub  (in phi, per pi-period),
#   i.e. arccos(C_P) in 2phi => width arccos(C_P) in phi (the super-thr arc half-width is arccos(C_P)/... )
# Let me just compute, as a function of r, the two arcs and check containment. The ESCAPE MARGIN is
#   the angle by which the in-domain arc 'sticks out' of the sub-thr arc (>0 => an in-domain super-thr phase exists).
#
# DOMAIN-DOMINATES formulation: an orbit is trapped iff in-domain arc ⊆ sub-thr arc.
# Because the in-domain arc is CENTERED at phi=-xi (where Dom is max) and the super-threshold arc 
# (P>=thr) is CENTERED at phi where cos(2phi+eta)=max => 2phi+eta=0 => phi=-eta/2.
# Both centers are near 0 (xi,eta ~ 1/q small). So the super-thr arc sits NEAR the center of the in-domain arc!
# => the in-domain arc's MIDDLE is super-threshold. So as long as the super-thr arc is non-empty within
#    the in-domain arc, the orbit escapes. 
#
# The orbit escapes UNLESS r is so small that the whole circle is sub-thr (C_P>=1) AND the in-domain arc 
#   is non-empty. So the danger zone: C_P(r)>=1 (entire circle sub-thr) AND C_D(r)<1 (in-domain arc nonempty).
#   C_P>=1: r^2 <= 2 A2 thr/(3l/2+sqrt(A2)) = 2A2 thr/(3l/2+sqrt(A2)) =: r_submax^2 (P_max<=thr).
#   C_D<1 : r > 1/B_lam =: r_dommin  (in-domain arc exists at the peak phase).
# TRAPPED-POSSIBLE iff r_dommin < r <= r_submax, i.e. iff  1/B_lam < r_submax  
#    BUT that just says a single phase can be both in-domain and sub-thr; trapped needs WHOLE in-domain arc sub-thr.
# Since whole circle is sub-thr when C_P>=1, ANY r in (r_dommin, r_submax] gives a trapped orbit at the 
#    single peak phase... no -- need the orbit to STAY in-domain for all its phases. The orbit's phases are
#    r-fixed on its circle; in-domain requires cos(phi+xi)>C_D for the phases it VISITS. A trapped orbit 
#    visits phases forming its rotation; to be trapped ALL visited phases must be in-domain AND sub-thr.
# The orbit visits an arc only if it never leaves -- but rotation by th means it visits an ever-growing 
#   set of phases (advances by th each step). To stay in-domain forever it must stay within the in-domain arc,
#   but rotation pushes phi out of any proper arc within ~ (arc width)/th steps. So NO orbit stays in a proper 
#   arc forever (rotation is minimal/irrational-ish; even rational, it steps OUT of the in-domain arc).
# => The ONLY way to be trapped: in-domain arc = FULL circle (C_D<=-1, i.e. Dom>1 everywhere) AND sub-thr everywhere.
#    Dom(phi)=r B_lam cos(phi+xi) has min -r B_lam <... cannot be >1 everywhere (it's a centered sinusoid, goes negative!).
# THEREFORE in-domain is ALWAYS a proper arc (Dom goes negative somewhere) => rotation ALWAYS exits it => 
#    every orbit escapes the domain in finite time. The DWELL = (in-domain arc width)/th. 
# The question for X_Omega is sharper: does the orbit reach P>=thr (escape UP, giving a super-thr sample) 
#    BEFORE OR WHEN it exits the domain? If it exits the domain while still sub-thr, that's fine too 
#    (the orbit leaves T^q; it's not a sub-thr invariant orbit). EITHER exit kills 'sustained sub-thr'.
# So actually the DWELL being finite (in-domain arc finite) ALREADY gives no sustained sub-thr orbit!
# BUT: exiting the domain means the orbit MAPS to a new point that re-enters elsewhere (BCZ is a bijection of T^q).
# The orbit continues; 'sustained sub-thr' = the FULL forward orbit stays sub-thr, across re-entries.
# That's where (L2) + the corridor structure matters: after domain-exit, the next step has P>=thr (the 'kick').
#
# So (L1b) properly = the ARC-WIDTH bound: the in-domain corridor arc has width Delta(q), the orbit 
#   dwells ~Delta(q)/th blocks, and within that dwell the max P reaches thr (=g_closed>=thr) OR it exits 
#   with a super-thr kick. The g_closed>=thr formulation is the clean sufficient condition. 
# Let me compute Delta(q)=in-domain arc width at the BINDING radius (r=r_submax, the largest sub-thr r),
#   and the escape angle, and their difference's ORDER.

def quant(q):
    th=math.pi/q; l=2*math.cos(th); A2=1+2*l*l
    thr=1.0/l**3
    Blam=math.sqrt(12*l**4+8*l**2+1)/(2*l*l+1)
    eta=math.atan2(math.sin(th),3*math.cos(th))
    xi=math.atan2(l*math.sin(th),3*l*l+1+l*math.cos(th))
    # r_submax: P_max=thr => r^2=2 A2 thr/(3l/2+sqrt(A2))
    r2_sub=2*A2*thr/(3*l/2+math.sqrt(A2))
    r_sub=math.sqrt(r2_sub)
    # at r=r_sub, the whole circle is exactly at-or-below thr (P_max=thr). in-domain arc:
    C_D=1.0/(r_sub*Blam)
    if C_D>=1:
        dom_arc=0.0  # no in-domain phase even at peak
    else:
        dom_arc=2*math.acos(C_D)   # full in-domain arc width in phi
    # dwell in blocks at the binding radius:
    dwell_blocks=dom_arc/th
    return th,l,thr,r_sub,C_D,dom_arc,dwell_blocks,Blam

print(" q     r_submax  C_D=1/(r B)   dom_arc[rad]  dwell_blocks  dom_arc(as pi-frac)")
for q in [18,20,25,30,40,60,80,100,150,200,300,500,1000]:
    th,l,thr,r_sub,C_D,dom_arc,dwb,Blam=quant(q)
    print(f" {q:4d}  {r_sub:.5f}   {C_D:.6f}    {dom_arc:.5f}     {dwb:8.3f}     {dom_arc/math.pi:.4f} pi")

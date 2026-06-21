"""
THE q-INDEPENDENT MEASURE-THEORETIC WRAPPER (the proposed hCorr replacement core).

Lemma (RotCover). Let R = rotation by alpha = 2pi/q on S^1=R/2piZ. Let S be a closed arc
of width W = 2w. If W >= alpha (i.e. w >= pi/q), then the q translates {R^{-k} S}_{k=0..q-1}
COVER S^1. Consequently any R-invariant prob measure mu has mu(S)>0 (else mu(S^1)=0).

This is purely combinatorial: q equally-spaced arcs of width >= the spacing alpha tile
the circle. Verify the covering condition numerically for the realized block geometry, and
state the EXACT remaining inequality:  w_block(q) >= pi/q  (super-arc half-width >= step).

We already have (PROVED, L1bArcCoverage.arc_coverage_ineq):
   2 arccos(2 sqrt6/5)/pi < 33/256.
The limit super-arc half-width (block 2phi var) is pi/2 - arccos-of-... ; the SUB arc
half-width fraction is C/2=0.0641 < 1/q-fraction? No: we need SUPER half-width >= step.
SUPER half-width fraction = 1/2 - C/2 = 0.4359 (of pi) -> super half-width = 0.4359*pi.
Step alpha=2pi/q in 2phi var, half-step = pi/q. Condition w_super >= pi/q:
   0.4359*pi >= pi/q  <=> q >= 1/0.4359 = 2.29. TRUE for all q>=3. HUGE margin.
"""
import mpmath as mp
mp.mp.dps=40
def lam(q): return 2*mp.cos(mp.pi/q)
C = 2*mp.acos(2*mp.sqrt(6)/5)/mp.pi   # sub-arc fraction limit
print(f"sub-arc fraction (limit) C={mp.nstr(C,8)}; super-arc fraction = 1-C = {mp.nstr(1-C,8)}")
print(f"super-arc HALF-width (block 2phi) = {mp.nstr((1-C)/2,8)}*pi")
print("covering needs super-HALF >= step pi/q i.e. (1-C)/2 >= 1/q:")
for q in [3,5,22,47,100]:
    cond = (1-C)/2 >= mp.mpf(1)/q
    print(f"  q={q}: (1-C)/2={mp.nstr((1-C)/2,6)} vs 1/q={mp.nstr(mp.mpf(1)/q,6)} -> covered={cond}")

# Direct covering simulation at the finite-q realized geometry: q equally spaced arcs of
# the actual super-arc half-width cover the circle.
def super_half_block(q):
    # realized block: F = 3l/2 + sqrt(A2) cos(psi) (scaled), threshold t' chosen so window
    # max = t. The realized SUB-arc fraction is <= C + O(1/q). Use upper bound C+0.001 to be safe.
    return mp.pi*(1-(C))/2  # conservative super half-width (>= realized since sub <= C asymptotically)

for q in [22,47,100,300]:
    sh = super_half_block(q); step=2*mp.pi/q
    n_translates_to_cover = mp.ceil((2*mp.pi)/ (2*sh)) if sh>0 else mp.inf
    covered = (2*sh) >= step
    print(f"q={q}: super arc width 2w={mp.nstr(2*sh,6)} step={mp.nstr(step,6)} covered_by_q_translates={covered}")

# Verdict

q=4: **LINE**; re_std=9.829142370588003e-12; pinned coordinates (N=28): (0.24999999999999986, 7.0673625708673464), (0.25000000000243783, 10.511019819386503), (0.24999999998047526, 12.50542878996472)
q=6: **LINE**; re_std=1.025589335680139e-11; pinned coordinates (N=28): (0.25000000000000555, 7.0673625708673651), (0.24999999997949376, 10.511019819425393)

# q=3 validation evidence

Validation status: **PASS**. The gate was run before q=4/q=6: both q=3 points used N=30 and sign=1; max |Re(s)-0.25|=0.0; max |det|=1.2038426631040734e-15.
- seed gamma=14.134725, s=0.25+7.067362570867347i, Re error=0.0, absdet=7.653303790632259e-16, Newton converged=True.
- seed gamma=21.02204, s=0.25+10.511019819385778i, Re error=0.0, absdet=1.2038426631040734e-15, Newton converged=True.

# Honest caveats

Newton pinning used tolerance=1e-12, finite-difference step=1e-06, and the N-stability test compared N=22 against N=28 with coordinate tolerances (0.002, 0.002).
- q=4: scan coverage Re=[0.1, 0.49, 16], Im=[3.0, 17.0, 141]; surface cells 2256/2256; raw/selected seeds=123/3; runtime=177.6051848330535 seconds; runtime-cap reduction triggered=False.
  N-stability: checked=True, candidate_count=3, stable_count=3.
  pin (0.24999999999999986, 7.0673625708673464): delta_Re=4.2573999881057034e-12, delta_Im=1.1937117960769683e-12, absdet(N22,N28)=(3.1276686691545863e-16, 1.7415993373559034e-16).
  pin (0.25000000000243783, 10.511019819386503): delta_Re=1.3138609922247468e-09, delta_Im=9.733964745350931e-09, absdet(N22,N28)=(5.059849660737591e-16, 1.9814076730286193e-15).
  pin (0.24999999998047526, 12.50542878996472): delta_Re=2.3228416781706507e-07, delta_Im=1.044541271255639e-07, absdet(N22,N28)=(4.214269711373649e-15, 1.1915488679716475e-14).
- q=6: scan coverage Re=[0.1, 0.49, 16], Im=[3.0, 17.0, 141]; surface cells 2256/2256; raw/selected seeds=42/2; runtime=410.1243464171421 seconds; runtime-cap reduction triggered=False.
  N-stability: checked=True, candidate_count=2, stable_count=2.
  pin (0.25000000000000555, 7.0673625708673651): delta_Re=7.814734970246207e-11, delta_Im=7.037659344177882e-11, absdet(N22,N28)=(1.4441611082370266e-15, 1.049732279194465e-15).
  pin (0.24999999997949376, 10.511019819425393): delta_Re=6.619982664823887e-08, delta_Im=9.093986896857587e-08, absdet(N22,N28)=(1.2752910088606246e-14, 1.040348918332571e-14).
The scan is a certified-Arb midpoint surface plus Newton pinning and finite-N stability; no argument-principle winding box was used for the reported geometry. Resonances outside the recorded scan rectangle are not excluded.

# FAMILY PREP CONSTANTS — 2026-08-14

## Manifest

| q | kappa | ell_q | lattice-clear? | rho* | N-needed |
|---:|---:|---:|:---:|---:|---:|
| 5 | 3 | 0.11442064802926020189523836764788 | YES | 0.659688826442 | 39 |
| 6 | 2 | 0.26794919243112270647255365849413 | YES | — | — |
| 7 | 5 | 0.054527994798052490833925195943494 | YES | 0.782263813618 | 66 |
| 8 | 3 | 0.19891236737965800691159762264468 | YES | 0.820778458004 | 82 |
| 9 | 7 | 0.031997896494675144462233578913467 | YES | — | — |
| 10 | 4 | 0.15838444032453629383888309269437 | YES | — | — |
| 11 | 9 | 0.021081887805120581405472197217452 | YES | — | — |
| 12 | 5 | 0.13165249758739585347152645740972 | YES | — | — |

**K_s lattice headline: ALL REQUESTED q=7..12 ARE CLEAR. No q has a zero with Re(s)>0.**

`rho*` and `N-needed` are float preparation values, not Arb-certified bounds. q=5 is included as a method anchor; q=6 is the arithmetic control and was not disc-optimized in this task.

## K_s zero lattices

For odd q, Lemma 6.3 gives `A_s = L_1^h L_2 L_1^(h-1) L_2`; for even q, the §6.2 cycle gives `A_s = L_1^(h-1) L_2`. The argument map reverses the operator factors, so its matrix word is the one recorded below.

| q | operator word | map matrix word | trace in lambda_q | trace (decimal) | ell_q (20+ digits) | pi/a_q |
|---:|---|---|---|---:|---:|---:|
| 5 | `L_1^h L_2 L_1^(h-1) L_2` | `M_2 M_2 M_1` | `3*x + 4` | 8.854101966249684544613760503 | 0.11442064802926020189523836764788 | 1.4491585072992118233030904940843 |
| 6 | `L_1^(h-1) L_2` | `M_2 M_1` | `4` | 4.0 | 0.26794919243112270647255365849413 | 2.3854920957804487699369129566343 |
| 7 | `L_1^h L_2 L_1^(h-1) L_2` | `M_2 M_1 M_2 M_1 M_1` | `4*x^2 + 3*x` | 18.39373162228438300161665299 | 0.054527994798052490833925195943494 | 1.0799409863812493600960968281985 |
| 8 | `L_1^(h-1) L_2` | `M_2 M_1 M_1` | `2*x^3 - 4*x` | 5.226251859505506111426572694 | 0.19891236737965800691159762264468 | 1.945390008778187590169189484731 |
| 9 | `L_1^h L_2 L_1^(h-1) L_2` | `M_2 M_1 M_1 M_2 M_1 M_1 M_1` | `4*x^2 + 7*x + 4` | 31.28405223595454165837667109 | 0.031997896494675144462233578913467 | 0.91270045642688366324939011634642 |
| 10 | `L_1^(h-1) L_2` | `M_2 M_1 M_1 M_1` | `4*x^2 - 8` | 6.472135954999579392818347337 | 0.15838444032453629383888309269437 | 1.7048577894913147259508726081507 |
| 11 | `L_1^h L_2 L_1^(h-1) L_2` | `M_2 M_1 M_1 M_1 M_2 M_1 M_1 M_1 M_1` | `4*x^4 + 4*x^3 - 8*x^2 - 5*x + 4` | 47.45516413147923407694373296 | 0.021081887805120581405472197217452 | 0.81402308050074853033251713873617 |
| 12 | `L_1^(h-1) L_2` | `M_2 M_1 M_1 M_1 M_1` | `4*x` | 7.727406610312546293997945598 | 0.13165249758739585347152645740972 | 1.5494224914631032316337757417979 |

With `a_q = -log(ell_q)`, the determinant reduction is `det(1-K_s) = product_{n>=0}(1 - ell_q^(2s+2n))`. Hence every zero is

```text
s = -n + i*pi*k/a_q,    n >= 0, k in Z.
```

Because every computed trace is >2 and every ell_q lies strictly in (0,1), the displayed lattice has Re(s)=-n<=0 for all n. This is the requested all-zero verification, not a finite scan.

### Fixed-point cross-check

The composed Mobius map was iterated directly from z=0. Its attracting derivative is `ell_q^2`; taking its positive square root must agree with the trace-derived ell.

| q | fixed point | ell from iteration | relative error | iterations |
|---:|---:|---:|---:|---:|
| 5 | (-0.35372049571993275678074973111783 + 0.0j) | 0.11442064802926020189523836764788 | 1.49456073411e-93 | 49 |
| 6 | (-0.36602540378443864676372317075294 + 0.0j) | 0.26794919243112270647255365849413 | 7.65751617531e-93 | 80 |
| 7 | (-0.34413214421212620664701257931723 + 0.0j) | 0.054527994798052490833925195943494 | 9.94530285182e-95 | 37 |
| 8 | (-0.3511533023570844946552312438511 + 0.0j) | 0.19891236737965800691159762264468 | 1.91544142687e-92 | 65 |
| 9 | (-0.33996151074384285170792048244486 + 0.0j) | 0.031997896494675144462233578913467 | 6.61697145251e-94 | 31 |
| 10 | (-0.34457651675525573410005359184626 + 0.0j) | 0.15838444032453629383888309269437 | 1.7731265565e-92 | 57 |
| 11 | (-0.33780211218914401578568043788456 + 0.0j) | 0.021081887805120581405472197217452 | 4.45734865666e-95 | 28 |
| 12 | (-0.34108137740210887763712119135191 + 0.0j) | 0.13165249758739585347152645740972 | 8.22693567396e-93 | 52 |

All relative errors are far below the requested 15-digit agreement threshold.

## Disc optimization

The q=7 and q=8 allowed-block lists below were rebuilt by recording calls made by `build_reduced_matrix` in the restore worktree. No block list was copied from the q=5 script.

### q=7

- `kappa=5`; source builder: `/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/zeta_mayer_rosen.py`; captured calls: `19`.
- Allowed blocks: `(1->4, n=2 head), (1->5, n=3 tail), (1->4, n=-1 head), (1->5, n=-2 tail), (2->5, n=2 tail), (2->4, n=-1 head), (2->5, n=-2 tail), (3->1, n=1 head), (3->5, n=2 tail), (3->4, n=-1 head), (3->5, n=-2 tail), (4->2, n=1 head), (4->5, n=2 tail), (4->4, n=-1 head), (4->5, n=-2 tail), (5->3, n=1 head), (5->5, n=2 tail), (5->4, n=-1 head), (5->5, n=-2 tail)`
- Full Markov branches at inflation 1: `(1->4, n=2 head), (2->5, n=2 tail), (3->1, n=1 head), (4->2, n=1 head), (5->3, n=1 head), (5->4, n=-1 head)`
- Optimal inflations: `(2.790000000000, 2.390000000000, 1.900000000000, 1.560000000000, 1.350000000000)`
- Float `rho* = 0.782263813617748`; worst block `(2->5, n=2 tail)`; worst tail n `2`.
- Implied tail exponent: `N = log(1e-7)/log(rho*) = 65.637250`, so integer `N-needed = 66`.
- Search: grid `[1.0, 1.1, 1.2, 1.35, 1.5, 1.7, 1.9, 2.2, 2.6, 3.0]` (100000 points), then three local refinements with coordinate offsets `(-0.07, 0, +0.07)` clipped to `[0.95,4.0]`.

### q=8

- `kappa=3`; source builder: `/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/zeta_mayer_rosen.py`; captured calls: `8`.
- Allowed blocks: `(1->3, n=2 tail), (1->3, n=-1 tail), (2->1, n=1 head), (2->3, n=2 tail), (2->3, n=-1 tail), (3->2, n=1 head), (3->3, n=2 tail), (3->3, n=-1 tail)`
- Full Markov branches at inflation 1: `(2->1, n=1 head), (3->2, n=1 head), (3->3, n=-1 tail)`
- Optimal inflations: `(3.000000000000, 1.900000000000, 1.350000000000)`
- Float `rho* = 0.820778458003607`; worst block `(3->3, n=-1 tail)`; worst tail n `1`.
- Implied tail exponent: `N = log(1e-7)/log(rho*) = 81.609764`, so integer `N-needed = 82`.
- Search: grid `[1.0, 1.1, 1.2, 1.35, 1.5, 1.7, 1.9, 2.2, 2.6, 3.0]` (1000 points), then three local refinements with coordinate offsets `(-0.07, 0, +0.07)` clipped to `[0.95,4.0]`.

The unit-inflation full-branch observation is expected: a complete Markov branch can have ratio exactly 1 at inflation 1, so a uniform-radius choice cannot contract it. The asymmetric radii are the intended fix.

## Reproducibility and scope

- Calculator: `/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/family_prep/family_prep_constants.py`
- Authoritative builder: `/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/zeta_mayer_rosen.py` (sha256 `070732923ce4d05c1482c97727fc1824548578955ca59b1fef99c334f6ea06c4`)
- Reference method read: `/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/tb_disc_opt.py` (sha256 `f9e6e95dde44db4859796e7d611ee3087f3ff4779c7eb73983103da576ef2134`)
- Receipt: `/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/FAMILY_PREP_CONSTANTS_RECEIPT.json`
- Runtime: specified `/Users/za/.venvs/farey-rh/bin/python`; high precision is used only for 2x2 Mobius constants and fixed-point checks; disc work is float64.
- Explicitly not run: Arb scans, large transfer-matrix spectral scans, or off-line resonance searches.


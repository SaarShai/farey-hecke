# /goal J — Bulletproof the value: massive search for any orbit below 1/λ³ (refutation hunt at scale)

> Paste the body below into `/goal` in a fresh session. Self-contained. Work autonomously; verify with
> results (trust `EXIT=` lines, NOT task summaries); send NOTHING outward (USER-gated). Adversarial
> honesty: this is a REFUTATION HUNT — you are trying to BREAK `X_Ω(q)=1/λ³`, not confirm it. A clean
> "nothing below threshold across a huge search" is the deliverable; a single orbit below it is a major
> (publishable) refutation. Verify any candidate at high precision before believing it.

## MISSION
Drive the empirical certainty of **`X_Ω(q)=1/λ³`** (genuine Taha BCZ_q, q≥17) as high as compute allows,
and hunt for any refutation. The existing evidence is THIN: goal H's exhaustive search was only
**top branches {q−4..q−1}, period ≤ 6, digit ≤ 4** at q=16/20/30. The danger (per goal F/H) is a
sub-threshold INVARIANT SET (a KAM-style island, or a long sub-threshold cycle) at LARGE q — which a
short search cannot see. Push hard: longer periods, more q, the full relevant branch set.

> **Concretely: is there ANY `BCZ_q`-orbit with `ess-sup P < 1/λ³`?** If yes → `X_Ω(q) < 1/λ³`,
> refuting the headline for that q. If no (across a massive search) → the conjecture is empirically
> bulletproof, and the search itself maps the corridor structure for the (L2) proof (goal I).

## WHAT TO SEARCH (cover the gaps in prior searches)
1. **Periodic-word search at LONG period.** Genuine map, word = list of `(branch i, digit k)`; a word is
   a candidate sub-threshold orbit iff its monodromy is parabolic/elliptic (trace |·|≤2) AND its
   scale-family `ess-sup P = s_lo²·max_n P̂_n` is `< 1/λ³`. Push **period to 15–30** (goal H stopped at
   6 — a sub-threshold CYCLE chaining corridors could be long), **digit to ~6**, branches across the
   FULL range (not just top-4 — include the middle band `[≈q/2, q−3]` where (B) fails, and confirm via
   itinerary whether middle branches ever appear in long candidates). Use necklace/canonical-word dedup
   to cut the factorial blowup; prune hyperbolic words early (they escape).
2. **Direct orbit search.** Long forward orbits from many seeds on the genuine map; track running
   `ess-sup P` and the longest sub-threshold run vs q (goal H: max-run ~0.4q). Adversarially minimize
   `ess-sup P` over seeds (hill-climb / basin-hopping) at q=17,20,30,50,80,120. Does the min ever dip
   below `1/λ³`? (goal H got ≈1.12×thr at q=20,30,50 — push more seeds, more q, longer orbits.)
3. **Corridor-cycle search (feeds goal I).** Enumerate the elliptic corridors (family `(q−1,k)(q−1,0)
   (q−3,0)`, k∈{1,2,3}, trace `λ(k−2)`, + any others), build the transition graph, and search for any
   cycle that keeps all `P<1/λ³`. This is the sharp form of the refutation hunt.
4. **High-precision verify** any candidate that looks sub-threshold (mpmath, dps≥50): is it a real
   periodic orbit in `𝒯^q` with `ess-sup P < 1/λ³`, or a numerical artifact / boundary escape?

## SCALE IT (this is the compute front — use real horsepower)
- **Fleet:** M1 `new@192.168.1.22`, M2 `alicia@192.168.1.92`, key `~/.ssh/id_ed25519`. ⚠ Both are
  currently running the −1 prime sieve — **check `pgrep -fl mr1_par` on each first**; launch heavy
  searches there only once a node is free (the sieves finish within hours). Until then run a moderate
  pass locally on M3. Long jobs: `caffeinate -i nohup CMD > log 2>&1 &`. `MACHINE_ACCESS.md` for
  re-discovery (DHCP IPs drift).
- **Kaggle:** wired but token is currently **401** (expired) — if you want Kaggle CPU, the USER must
  drop a fresh `~/.kaggle/kaggle.json` first (ask; do not block on it).
- Port the hot inner loop to C or vectorized numpy (the genuine map is 2×2 matrix products — fast).
  Pure-Python at period≤6 already strained; period≥15 needs C/numpy + necklace pruning + parallelism.

## REUSE (validated genuine-map code — do NOT reinvent the map)
- `code/Hgoal_wordtest.py` (genuine matrices `M_{i,k}`, monodromy, scale-family `ess-sup`; EXTEND its
  branch set + period), `code/Hgoal_{driver,itin,dichotomy}.py`, `code/Fgoal_*.py` (large-q infimum /
  max-run), `code/Bgoal_genuine_hunt.py` (the map + observable `P=1/R_q`). Validate against anchors
  (q=3→2/9, q=4→√2/8, q=5→1/φ³, W_q trace=λ) before trusting any extended run.

## OBJECT (exact)
`λ_q=2cos(π/q)`, genuine `BCZ_q` on `𝒯^q={0<a≤1,1−λa<b≤1}`, `q−2` branches `M_{i,k}=[[x_i,y_i],
[x_{i+1}+kλx_i,y_{i+1}+kλy_i]]`, `x_i=sin((i+1)π/q)/sinπ/q`, `y_i=x_{i−1}`, det 1; observable
`P=1/R_q`. Threshold `1/λ³` = the cusp value (exact). `X_Ω(q)=1/λ³` conjectured ∀q (proven q≤5,
reduction route q≤16).

## CONSTRAINTS (hard)
- Nothing outbound/published/contacted (USER-gated); no commit/push/git changes unless asked;
  `~/Documents` Drive-synced (no folder/`.git` moves; `* (1)` = conflict artifacts).
- PROVEN/NUMERICAL/CONJECTURAL strictly separate. A search result is NUMERICAL evidence, never proof.

## DEFINITION OF DONE
- A reproducible report: max period / digit / q searched, total words/orbits, and the **min `ess-sup P`
  found vs `1/λ³`** per q. Plus the corridor list + transition graph + any sub-threshold cycle found.
- A clear verdict: either a high-precision REFUTATION (orbit with `ess-sup P<1/λ³` — overturns the value
  for that q) OR strong bulletproofing ("nothing below `1/λ³` across period≤P, q=17..N"). Hand the
  corridor map to goal I. Honest ledger update (`FRONTIER_STATUS`, `FINDINGS_*`). Nothing sent outward.

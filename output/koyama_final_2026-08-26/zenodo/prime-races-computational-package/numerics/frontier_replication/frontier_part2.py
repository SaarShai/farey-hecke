#!/usr/bin/env python3
# Kaggle script kernel — INDEPENDENT frontier cross-check of the project's mr1_par sieve.
#
# WHY: at x<=1.3e13 the prime-counting curve is already corroborated by TWO independent
# methods (primesieve replicate.cpp == hand-rolled independent_sieve.c, Koyama bundle).
# But the frontier 1.3e13 -> 3e14 (the RS variance ONSET region, ~e^33.4) is computed ONLY
# by mr1_par on M1+M2 — same code on both, so a large-x logic bug (64-bit overflow, segment
# offset) would pass both. This kernel recomputes pi(x;N,a) with primesieve (a different,
# battle-tested implementation) at mr1_par's EXACT frontier grid points, for an independent
# cross-check via compare_curves.py.
#
# Output: /kaggle/working/curve_kaggle_indep.tsv  in mr1_par schema:  N<TAB>x<TAB>a<TAB>count
#         plus TOTAL<TAB>N<TAB>x<TAB>pi_x.  Convention: ALL primes (from 2), residue p%N,
#         a = 0..N-1  (identical to mr1_par.c, so compare_curves.py diffs cell-for-cell).
import subprocess, sys, os, textwrap, time

# mr1_par grid points >= 1.3e13 (the frontier; copied verbatim from M2 grid_full.txt)
CK = [13000000000000,13109403780009,13727016344541,14373725982157,15050903519343,
15759984365207,16502471554108,17279938931625,18094034490631,18946483864533,
19839093985085,20773756912534,21752453846202,22777259324031,23850345619961,
24973987348488,26150566286152,27382576420175,28672629234945,30023459247572,
31437929804219,32919039149526,34469926781966,36093880108624,37794341413493,
39574915154062,41439375601662,43391674841769,45435951151211,47576537770051,
49817972086731,52165005255944,54622612269628,57196002502427,59890630753972,
62712208811383,65666717556514,68760419643587,71999872774107,75391943597177,
78943822264697,82663037672284,86557473418223,90635384514286,94905414883828,
99376615684263,100000000000000,104058464492742,108960885395717,114094270024970,
119469499584686,125097967916282,130991605649859,137162905493486,143624948713920,
150391432864885,157476700821694,164895771183756,172664370109409,180798964650562,
189316797657804,198235924329971,200000000000000,207575250485640,217354572637679,
227594619955796,238317098206027,249544735760329,261301331773756,273611806631400,
286502254771965,300000000000000]
LIMIT = max(CK)  # 3e14
RLO = 100000000000000
RHI = 200000000000000

def sh(cmd):
    print("+", cmd, flush=True)
    return subprocess.run(cmd, shell=True, check=False)

# ---- install primesieve dev headers + lib (need internet enabled in kernel metadata) ----
ok = sh("apt-get -qq update && apt-get -qq install -y libprimesieve-dev").returncode == 0
if not (ok and os.path.exists("/usr/include/primesieve.hpp")):
    print("apt path failed; building primesieve from source", flush=True)
    sh("git clone --depth 1 https://github.com/kimwalisch/primesieve /tmp/ps")
    sh("cmake -S /tmp/ps -B /tmp/ps/build -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=ON >/tmp/cm.log 2>&1")
    sh("cmake --build /tmp/ps/build -j4 >/tmp/mk.log 2>&1 && cmake --install /tmp/ps/build >/dev/null 2>&1")
    sh("ldconfig")

# ---- C++: primesieve iterator, parallel by range, snapshot at CK ----
cks = ",".join(str(c) + "ULL" for c in CK)
cpp = textwrap.dedent(f"""
#include <primesieve.hpp>
#include <cstdint>
#include <cstdio>
#include <vector>
#include <omp.h>
using u64 = uint64_t;
static const int NS[5] = {{7,8,11,19,23}};
static const int OFF[5] = {{0,7,15,26,45}};   // prefix offsets; total residues = 68
static const int TOTR = 68;
static const u64 CKv[] = {{ {cks} }};
static const int NCK = sizeof(CKv)/sizeof(CKv[0]);  // 72

int main() {{
    const u64 LIM = {LIMIT}ULL;
    const u64 RLO = {RLO}ULL, RHI = {RHI}ULL;  // this part owns primes in [RLO, RHI)
    const int NCH = 256;                          // chunks for load balance
    std::vector<std::vector<long long>> snap(NCH, std::vector<long long>((size_t)NCK*TOTR, 0));
    #pragma omp parallel for schedule(dynamic,1)
    for (int c = 0; c < NCH; ++c) {{
        // half-open ownership [lo,hi): boundary primes belong to exactly one chunk.
        u64 lo = RLO + (u64)((__int128)(RHI - RLO) * c / NCH);
        u64 hi = (c == NCH-1) ? RHI : (RLO + (u64)((__int128)(RHI - RLO) * (c+1) / NCH));
        long long cnt[TOTR]; for (int i=0;i<TOTR;i++) cnt[i]=0;
        auto *S = snap[c].data();
        int j = 0;
        // start slightly before lo so the first prime >= lo is reachable regardless of
        // primesieve's >/>= start convention; the explicit p<lo guard makes it exact.
        primesieve::iterator it(lo == 0 ? 0 : lo - 1, hi);
        for (u64 p = it.next_prime(); p < hi; p = it.next_prime()) {{
            if (p < lo) continue;                 // exact lower bound -> own primes in [lo,hi)
            // snapshot all checkpoints ck < p with the counts accumulated so far
            while (j < NCK && CKv[j] < p) {{
                for (int i=0;i<TOTR;i++) S[(size_t)j*TOTR+i] = cnt[i];
                ++j;
            }}
            for (int m=0;m<5;m++) cnt[OFF[m] + (int)(p % NS[m])]++;
        }}
        // remaining checkpoints (ck >= last prime in range) get the full range count
        while (j < NCK) {{ for (int i=0;i<TOTR;i++) S[(size_t)j*TOTR+i] = cnt[i]; ++j; }}
    }}
    // combine
    std::vector<long long> tot((size_t)NCK*TOTR, 0);
    for (int c=0;c<NCH;c++) for (size_t k=0;k<(size_t)NCK*TOTR;k++) tot[k]+=snap[c][k];
    FILE* f = fopen("/kaggle/working/curve_kaggle_indep.tsv","w");
    fprintf(f, "# primesieve INDEPENDENT frontier cross-check of mr1_par; LIMIT=%llu\\n", (unsigned long long)LIM);
    fprintf(f, "# schema: N<TAB>x<TAB>a<TAB>count  and  TOTAL<TAB>N<TAB>x<TAB>pi_x\\n");
    for (int jc=0;jc<NCK;jc++) {{
        for (int m=0;m<5;m++) {{
            long long pix=0;
            for (int a=0;a<NS[m];a++) {{
                long long v = tot[(size_t)jc*TOTR + OFF[m] + a];
                fprintf(f, "%d\\t%llu\\t%d\\t%lld\\n", NS[m], (unsigned long long)CKv[jc], a, v);
                pix += v;
            }}
            fprintf(f, "TOTAL\\t%d\\t%llu\\t%lld\\n", NS[m], (unsigned long long)CKv[jc], pix);
        }}
    }}
    fclose(f);
    // sanity to stdout: pi(x) at a few CK via N=7 totals
    for (int jc : {{0, NCK/2, NCK-1}}) {{
        long long pix=0; for (int a=0;a<7;a++) pix += tot[(size_t)jc*TOTR + OFF[0] + a];
        printf("pi(%llu) = %lld\\n", (unsigned long long)CKv[jc], pix);
    }}
    return 0;
}}
""")
open("frontier.cpp","w").write(cpp)

# ---- compile + run ----
if sh("g++ -O3 -fopenmp -std=c++17 frontier.cpp -o frontier -lprimesieve").returncode != 0:
    print("COMPILE FAILED", flush=True); sys.exit(1)
t0 = time.time()
r = sh("OMP_NUM_THREADS=4 ./frontier")
print(f"frontier run: rc={r.returncode}  wall={time.time()-t0:.0f}s", flush=True)
sh("head -30 /kaggle/working/curve_kaggle_indep.tsv")
sh("wc -l /kaggle/working/curve_kaggle_indep.tsv")
# known-pi sanity: pi(1e14)=3204941750802 ; pi(3e14)=? printed above. pi(1.3e13)=409514304484? check N totals sum.
print("DONE", flush=True)

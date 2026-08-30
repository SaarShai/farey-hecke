
#include <primesieve.hpp>
#include <cstdint>
#include <cstdio>
#include <vector>
#include <omp.h>
using u64 = uint64_t;
static const int NS[5] = {7,8,11,19,23};
static const int OFF[5] = {0,7,15,26,45};   // prefix offsets; total residues = 68
static const int TOTR = 68;
static const u64 CKv[] = { 13000000000000ULL,13109403780009ULL,13727016344541ULL,14373725982157ULL,15050903519343ULL,15759984365207ULL,16502471554108ULL,17279938931625ULL,18094034490631ULL,18946483864533ULL,19839093985085ULL,20773756912534ULL,21752453846202ULL,22777259324031ULL,23850345619961ULL,24973987348488ULL,26150566286152ULL,27382576420175ULL,28672629234945ULL,30023459247572ULL,31437929804219ULL,32919039149526ULL,34469926781966ULL,36093880108624ULL,37794341413493ULL,39574915154062ULL,41439375601662ULL,43391674841769ULL,45435951151211ULL,47576537770051ULL,49817972086731ULL,52165005255944ULL,54622612269628ULL,57196002502427ULL,59890630753972ULL,62712208811383ULL,65666717556514ULL,68760419643587ULL,71999872774107ULL,75391943597177ULL,78943822264697ULL,82663037672284ULL,86557473418223ULL,90635384514286ULL,94905414883828ULL,99376615684263ULL,100000000000000ULL,104058464492742ULL,108960885395717ULL,114094270024970ULL,119469499584686ULL,125097967916282ULL,130991605649859ULL,137162905493486ULL,143624948713920ULL,150391432864885ULL,157476700821694ULL,164895771183756ULL,172664370109409ULL,180798964650562ULL,189316797657804ULL,198235924329971ULL,200000000000000ULL,207575250485640ULL,217354572637679ULL,227594619955796ULL,238317098206027ULL,249544735760329ULL,261301331773756ULL,273611806631400ULL,286502254771965ULL,300000000000000ULL };
static const int NCK = sizeof(CKv)/sizeof(CKv[0]);  // 72

int main() {
    const u64 LIM = 300000000000000ULL;
    const u64 RLO = 0ULL, RHI = 100000000000000ULL;  // this part owns primes in [RLO, RHI)
    const int NCH = 256;                          // chunks for load balance
    std::vector<std::vector<long long>> snap(NCH, std::vector<long long>((size_t)NCK*TOTR, 0));
    #pragma omp parallel for schedule(dynamic,1)
    for (int c = 0; c < NCH; ++c) {
        // half-open ownership [lo,hi): boundary primes belong to exactly one chunk.
        u64 lo = RLO + (u64)((__int128)(RHI - RLO) * c / NCH);
        u64 hi = (c == NCH-1) ? RHI : (RLO + (u64)((__int128)(RHI - RLO) * (c+1) / NCH));
        long long cnt[TOTR]; for (int i=0;i<TOTR;i++) cnt[i]=0;
        auto *S = snap[c].data();
        int j = 0;
        // start slightly before lo so the first prime >= lo is reachable regardless of
        // primesieve's >/>= start convention; the explicit p<lo guard makes it exact.
        primesieve::iterator it(lo == 0 ? 0 : lo - 1, hi);
        for (u64 p = it.next_prime(); p < hi; p = it.next_prime()) {
            if (p < lo) continue;                 // exact lower bound -> own primes in [lo,hi)
            // snapshot all checkpoints ck < p with the counts accumulated so far
            while (j < NCK && CKv[j] < p) {
                for (int i=0;i<TOTR;i++) S[(size_t)j*TOTR+i] = cnt[i];
                ++j;
            }
            for (int m=0;m<5;m++) cnt[OFF[m] + (int)(p % NS[m])]++;
        }
        // remaining checkpoints (ck >= last prime in range) get the full range count
        while (j < NCK) { for (int i=0;i<TOTR;i++) S[(size_t)j*TOTR+i] = cnt[i]; ++j; }
    }
    // combine
    std::vector<long long> tot((size_t)NCK*TOTR, 0);
    for (int c=0;c<NCH;c++) for (size_t k=0;k<(size_t)NCK*TOTR;k++) tot[k]+=snap[c][k];
    FILE* f = fopen("/kaggle/working/curve_kaggle_indep.tsv","w");
    fprintf(f, "# primesieve INDEPENDENT frontier cross-check of mr1_par; LIMIT=%llu\n", (unsigned long long)LIM);
    fprintf(f, "# schema: N<TAB>x<TAB>a<TAB>count  and  TOTAL<TAB>N<TAB>x<TAB>pi_x\n");
    for (int jc=0;jc<NCK;jc++) {
        for (int m=0;m<5;m++) {
            long long pix=0;
            for (int a=0;a<NS[m];a++) {
                long long v = tot[(size_t)jc*TOTR + OFF[m] + a];
                fprintf(f, "%d\t%llu\t%d\t%lld\n", NS[m], (unsigned long long)CKv[jc], a, v);
                pix += v;
            }
            fprintf(f, "TOTAL\t%d\t%llu\t%lld\n", NS[m], (unsigned long long)CKv[jc], pix);
        }
    }
    fclose(f);
    // sanity to stdout: pi(x) at a few CK via N=7 totals
    for (int jc : {0, NCK/2, NCK-1}) {
        long long pix=0; for (int a=0;a<7;a++) pix += tot[(size_t)jc*TOTR + OFF[0] + a];
        printf("pi(%llu) = %lld\n", (unsigned long long)CKv[jc], pix);
    }
    return 0;
}

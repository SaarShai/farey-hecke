/* Library-independent segmented Eratosthenes sieve.
 * Hand-rolled in plain C99, no external dependencies.
 * Counts residues p mod N for N in {7,8,11,19,23}, snapshots at checkpoints.
 * Purpose: cross-validate primesieve-based replicate.cpp.
 *
 * Build:  cc -O3 -std=c99 -Wall independent_sieve.c -o independent_sieve
 * Run:    ./independent_sieve <upto>
 *
 * Output schema matches replicate.cpp's out.tsv (same per-N tables).
 * Algorithm: classical segmented sieve, segment size 2^21 bytes.
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <time.h>

#define SEG_BYTES (1<<21)   /* segment size in bytes (covers 2*SEG_BYTES integers if odd-only) */

static int Ns[5] = {7, 8, 11, 19, 23};
#define NN 5
#define MAXMOD 23

static uint64_t cur[NN][MAXMOD];   /* running residue counts */

static int n_checkpoints;
static uint64_t *checkpoints;
static uint64_t (*snap)[NN][MAXMOD];   /* snap[c][n][a] */

static uint64_t total = 0;
static int cp_idx = 0;

static double now_s(void) {
    struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec + t.tv_nsec * 1e-9;
}

static void dump_checkpoint_incremental(int j) {
    /* Append partial-dump line so killing mid-run keeps results.
       Format: "PARTIAL N x a count" — easy to grep/parse. */
    FILE *f = fopen("indep_partial.tsv", "a");
    if (!f) return;
    for (int i = 0; i < NN; ++i)
        for (int a = 0; a < Ns[i]; ++a)
            fprintf(f, "PARTIAL\t%d\t%llu\t%d\t%llu\n",
                    Ns[i], (unsigned long long)checkpoints[j], a,
                    (unsigned long long)snap[j][i][a]);
    fflush(f);
    fclose(f);
}

static void record_prime(uint64_t p) {
    while (cp_idx < n_checkpoints && p > checkpoints[cp_idx]) {
        for (int i = 0; i < NN; ++i)
            for (int a = 0; a < Ns[i]; ++a)
                snap[cp_idx][i][a] = cur[i][a];
        dump_checkpoint_incremental(cp_idx);
        fprintf(stderr, "[indep] CHECKPOINT x=%llu reached, partial dump written\n",
                (unsigned long long)checkpoints[cp_idx]);
        ++cp_idx;
    }
    for (int i = 0; i < NN; ++i)
        cur[i][(uint64_t)p % (uint64_t)Ns[i]] += 1;
    ++total;
    if ((total % 1000000000ULL) == 0) {
        fprintf(stderr, "[indep] primes=%llu p=%llu\n",
                (unsigned long long)total, (unsigned long long)p);
    }
}

/* simple sieve for base primes up to sqrt(N) */
static uint64_t *base_primes;
static size_t n_base;

static void sieve_base(uint64_t lim) {
    uint8_t *sv = calloc(lim + 1, 1);
    for (uint64_t i = 2; i * i <= lim; ++i)
        if (!sv[i]) for (uint64_t j = i*i; j <= lim; j += i) sv[j] = 1;
    n_base = 0;
    base_primes = malloc(sizeof(uint64_t) * (lim / 4 + 100));
    for (uint64_t i = 2; i <= lim; ++i) if (!sv[i]) base_primes[n_base++] = i;
    free(sv);
}

int main(int argc, char **argv) {
    uint64_t MAXX = (argc > 1) ? strtoull(argv[1], NULL, 10) : 100000000000ULL; /* default 1e11 */

    /* checkpoints: 1e9, 1e10, 1.3e10, 1e11, 1.3e11, 1e12, 1.3e12, 1e13, 1.3e13 — keep those <= MAXX */
    static uint64_t all_cp[] = {
        1000000000ULL, 10000000000ULL, 13000000000ULL,
        100000000000ULL, 130000000000ULL,
        1000000000000ULL, 1300000000000ULL,
        10000000000000ULL, 13000000000000ULL
    };
    int total_cp = sizeof(all_cp)/sizeof(all_cp[0]);
    n_checkpoints = 0;
    for (int i = 0; i < total_cp; ++i) if (all_cp[i] <= MAXX) ++n_checkpoints;
    checkpoints = malloc(sizeof(uint64_t) * n_checkpoints);
    for (int i = 0; i < n_checkpoints; ++i) checkpoints[i] = all_cp[i];
    snap = calloc(n_checkpoints, sizeof(*snap));

    fprintf(stderr, "[indep] MAXX=%llu  checkpoints=%d  segment=%d bytes\n",
            (unsigned long long)MAXX, n_checkpoints, SEG_BYTES);

    uint64_t sqrtN = (uint64_t)floor(sqrt((double)MAXX)) + 2;
    sieve_base(sqrtN);
    fprintf(stderr, "[indep] base primes (<=%llu): %zu\n", (unsigned long long)sqrtN, n_base);

    /* segmented sieve over odd numbers only.
     * segment covers integers [low, low + 2*SEG_BYTES) where bit i represents low + 2*i + 1.
     * (Index 0 = low (odd), index 1 = low+2, etc.)  — odd-only sieve.
     * Handle p=2 separately.
     */
    record_prime(2);
    uint8_t *seg = malloc(SEG_BYTES);

    uint64_t low = 3;
    while (low <= MAXX) {
        uint64_t high = low + 2ULL * SEG_BYTES - 2ULL;
        if (high > MAXX) high = MAXX;
        if ((high & 1ULL) == 0) high -= 1;

        size_t span = (size_t)((high - low) / 2 + 1);  /* number of odd entries */
        memset(seg, 0, span);

        for (size_t k = 1; k < n_base; ++k) {  /* skip base prime 2 */
            uint64_t p = base_primes[k];
            if (p * p > high) break;
            uint64_t start = p * p;
            if (start < low) {
                /* first odd multiple of p that is >= low */
                uint64_t r = low % p;
                start = (r == 0) ? low : low + (p - r);
                if ((start & 1ULL) == 0) start += p;   /* make it odd */
            }
            for (uint64_t m = start; m <= high; m += 2*p) {
                seg[(m - low) / 2] = 1;
            }
        }

        for (size_t i = 0; i < span; ++i) {
            if (!seg[i]) {
                uint64_t p = low + 2ULL * (uint64_t)i;
                record_prime(p);
            }
        }
        low = high + 2;
    }
    /* flush snapshots */
    while (cp_idx < n_checkpoints) {
        for (int i = 0; i < NN; ++i)
            for (int a = 0; a < Ns[i]; ++a)
                snap[cp_idx][i][a] = cur[i][a];
        ++cp_idx;
    }

    free(seg);

    /* Output identical schema to replicate.cpp out.tsv */
    printf("# Library-independent sieve replication (segmented Eratosthenes wheel-30 omitted; pure odd-only)\n");
    for (int i = 0; i < NN; ++i) {
        int N = Ns[i];
        printf("\n## N = %d\n", N);
        printf("x");
        for (int a = 1; a < N; ++a) printf("\tcount_a=%d", a);
        printf("\n");
        for (int j = 0; j < n_checkpoints; ++j) {
            printf("%llu", (unsigned long long)checkpoints[j]);
            for (int a = 1; a < N; ++a) printf("\t%llu", (unsigned long long)snap[j][i][a]);
            printf("\n");
        }
        printf("# diffs pi(x;%d,a)-pi(x;%d,1)\n", N, N);
        printf("x");
        for (int a = 2; a < N; ++a) printf("\tdiff_a=%d", a);
        printf("\n");
        for (int j = 0; j < n_checkpoints; ++j) {
            printf("%llu", (unsigned long long)checkpoints[j]);
            int64_t c1 = (int64_t)snap[j][i][1];
            for (int a = 2; a < N; ++a) {
                int64_t ca = (int64_t)snap[j][i][a];
                printf("\t%lld", (long long)(ca - c1));
            }
            printf("\n");
        }
    }
    return 0;
}

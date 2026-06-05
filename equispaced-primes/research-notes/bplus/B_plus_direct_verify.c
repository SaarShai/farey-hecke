/*
 * B_plus_direct_verify.c
 *
 * Direct streaming verifier for the Lean-canonical cross term
 *
 *   B(p) = 2 * sum_{f in F_{p-1}} D_{p-1}(f) * delta_p(f)
 *
 * where D_N(f) = fareyRank_N(f) - |F_N| * f and
 * delta_p(a/b) = a/b - frac(p*a/b) = (a - (p*a mod b))/b.
 *
 * This file exists because older bprime_* experiments predate the May 9
 * R1/SP-2 reduction and are easy to misclassify. The implementation below:
 *
 *   - uses the Lean rank convention explicitly (rank(0/1)=1),
 *   - cross-checks the five Lean native_decide anchors in double precision,
 *   - verifies M(p) with a Mobius sieve,
 *   - reports the Mobius-harmonic T(p-1) value that triggered the SP-2 alarm.
 *
 * Compile:
 *   cc -O3 -march=native -o B_plus_direct_verify B_plus_direct_verify.c -lm
 *
 * Example:
 *   ./B_plus_direct_verify 237733 243703 243799
 */

#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

static int *phi_arr = NULL;
static signed char *mu_arr = NULL;
static int *mertens_arr = NULL;

static void die_alloc(const char *name) {
    fprintf(stderr, "allocation failed: %s\n", name);
    exit(2);
}

static void compute_phi(int n) {
    phi_arr = (int *)malloc((size_t)(n + 1) * sizeof(int));
    if (!phi_arr) die_alloc("phi_arr");
    for (int i = 0; i <= n; i++) phi_arr[i] = i;
    for (int i = 2; i <= n; i++) {
        if (phi_arr[i] == i) {
            for (int j = i; j <= n; j += i) {
                phi_arr[j] -= phi_arr[j] / i;
            }
        }
    }
}

static void compute_mobius_mertens(int n) {
    int *primes = (int *)malloc((size_t)(n + 1) * sizeof(int));
    bool *is_comp = (bool *)calloc((size_t)(n + 1), sizeof(bool));
    mu_arr = (signed char *)calloc((size_t)(n + 1), sizeof(signed char));
    mertens_arr = (int *)calloc((size_t)(n + 1), sizeof(int));
    if (!primes) die_alloc("primes");
    if (!is_comp) die_alloc("is_comp");
    if (!mu_arr) die_alloc("mu_arr");
    if (!mertens_arr) die_alloc("mertens_arr");

    int pc = 0;
    mu_arr[1] = 1;
    for (int i = 2; i <= n; i++) {
        if (!is_comp[i]) {
            primes[pc++] = i;
            mu_arr[i] = -1;
        }
        for (int j = 0; j < pc; j++) {
            long long v = (long long)i * primes[j];
            if (v > n) break;
            is_comp[v] = true;
            if (i % primes[j] == 0) {
                mu_arr[v] = 0;
                break;
            }
            mu_arr[v] = (signed char)(-mu_arr[i]);
        }
    }
    for (int i = 1; i <= n; i++) {
        mertens_arr[i] = mertens_arr[i - 1] + (int)mu_arr[i];
    }

    free(primes);
    free(is_comp);
}

static bool is_prime_ll(long long n) {
    if (n < 2) return false;
    if (n % 2 == 0) return n == 2;
    for (long long d = 3; d * d <= n; d += 2) {
        if (n % d == 0) return false;
    }
    return true;
}

static long long farey_size_from_phi(int N) {
    long long n = 1; /* 0/1 */
    for (int k = 1; k <= N; k++) n += phi_arr[k];
    return n;
}

static double harmonic_T(int N) {
    double T = 1.0;
    double c = 0.0;
    for (int k = 1; k <= N; k++) {
        double term = (double)mertens_arr[N / k] / (double)k;
        double y = term - c;
        double t = T + y;
        c = (t - T) - y;
        T = t;
    }
    return T;
}

static void verify_one(long long p, bool progress) {
    if (p < 5 || p - 1 > 2147483640LL) {
        fprintf(stderr, "unsupported p=%lld\n", p);
        exit(2);
    }
    if (!is_prime_ll(p)) {
        fprintf(stderr, "warning: p=%lld is not prime; continuing anyway\n", p);
    }

    int N = (int)(p - 1);
    long long n = farey_size_from_phi(N);
    double n_d = (double)n;
    int Mp = mertens_arr[(int)p];
    double Tp1 = harmonic_T(N);

    printf("\n=== p=%lld N=%d ===\n", p, N);
    printf("M(p)=%d  T(p-1)=%.12f  |F_N|=%lld\n", Mp, Tp1, n);
    fflush(stdout);

    time_t t0 = time(NULL);

    double B = 0.0, C = 0.0, sum_delta = 0.0, sum_D = 0.0;
    double kB = 0.0, kC = 0.0, kDelta = 0.0, kD = 0.0;

    int a = 0, b = 1, c = 1, d = N;
    long long rank = 1;      /* Lean rank of 0/1 */
    long long processed = 0; /* interior plus final 1/1 if encountered */
    long long progress_step = n / 10;
    if (progress_step < 1) progress_step = 1;

    while (!(a == 1 && b == 1)) {
        long long kk = ((long long)N + b) / d;
        int na = (int)(kk * c - a);
        int nb = (int)(kk * d - b);
        a = c;
        b = d;
        c = na;
        d = nb;
        rank++;

        double f = (double)a / (double)b;
        double D = (double)rank - n_d * f;

        long long r = (b > 1) ? ((p * (long long)a) % (long long)b) : 0LL;
        double delta = (double)((long long)a - r) / (double)b;

        double yB = 2.0 * D * delta - kB;
        double tB = B + yB;
        kB = (tB - B) - yB;
        B = tB;

        double yC = delta * delta - kC;
        double tC = C + yC;
        kC = (tC - C) - yC;
        C = tC;

        double yd = delta - kDelta;
        double td = sum_delta + yd;
        kDelta = (td - sum_delta) - yd;
        sum_delta = td;

        double yD = D - kD;
        double tD = sum_D + yD;
        kD = (tD - sum_D) - yD;
        sum_D = tD;

        processed++;
        if (progress && rank % progress_step == 0) {
            time_t now = time(NULL);
            printf("  %5.1f%% rank=%lld/%lld elapsed=%lds B=%.6e C=%.6e\n",
                   100.0 * (double)rank / (double)n, rank, n,
                   (long)(now - t0), B, C);
            fflush(stdout);
        }
    }

    time_t t1 = time(NULL);
    printf("B(p)=%.15e\n", B);
    printf("C(p)=%.15e\n", C);
    printf("B/C=%.15f\n", C == 0.0 ? NAN : B / C);
    printf("sum_delta=%.15e  sum_D=%.15e  processed=%lld  elapsed=%lds\n",
           sum_delta, sum_D, processed, (long)(t1 - t0));
    printf("VERDICT: %s\n", B > 0 ? "B+ HOLDS at this p" : (B < 0 ? "B+ FAILS at this p" : "B+ ZERO"));
    fflush(stdout);
}

static void small_anchor_checks(void) {
    const long long ps[] = {5, 11, 13, 19, 23};
    const double expected[] = {
        -2.0 / 9.0,
        -55.0 / 36.0,
        271.0 / 385.0,
        2905619.0 / 680680.0,
        14608817.0 / 6348888.0,
    };

    printf("=== Lean native_decide anchor checks (double) ===\n");
    for (int idx = 0; idx < 5; idx++) {
        long long p = ps[idx];
        int N = (int)(p - 1);
        long long n = farey_size_from_phi(N);
        double n_d = (double)n;

        int a = 0, b = 1, c = 1, d = N;
        long long rank = 1;
        double B = 0.0;
        while (!(a == 1 && b == 1)) {
            long long kk = ((long long)N + b) / d;
            int na = (int)(kk * c - a);
            int nb = (int)(kk * d - b);
            a = c;
            b = d;
            c = na;
            d = nb;
            rank++;
            double f = (double)a / (double)b;
            double D = (double)rank - n_d * f;
            long long r = (b > 1) ? ((p * (long long)a) % (long long)b) : 0LL;
            double delta = (double)((long long)a - r) / (double)b;
            B += 2.0 * D * delta;
        }
        printf("p=%lld B=%.12f expected=%.12f diff=%.3e %s\n",
               p, B, expected[idx], B - expected[idx],
               fabs(B - expected[idx]) < 1e-9 ? "OK" : "FAIL");
    }
    fflush(stdout);
}

int main(int argc, char **argv) {
    if (argc < 2) {
        fprintf(stderr, "usage: %s p [p...]\n", argv[0]);
        return 2;
    }

    long long max_p = 0;
    for (int i = 1; i < argc; i++) {
        long long p = atoll(argv[i]);
        if (p > max_p) max_p = p;
    }

    time_t t0 = time(NULL);
    printf("Preparing phi/mobius tables to %lld...\n", max_p);
    compute_phi((int)max_p);
    compute_mobius_mertens((int)max_p);
    printf("Tables ready in %lds\n", (long)(time(NULL) - t0));

    small_anchor_checks();

    for (int i = 1; i < argc; i++) {
        verify_one(atoll(argv[i]), true);
    }

    free(phi_arr);
    free(mu_arr);
    free(mertens_arr);
    return 0;
}

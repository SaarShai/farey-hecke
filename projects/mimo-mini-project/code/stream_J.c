/*
 * Streaming J(Q) = ∫_0^1 E_Q(x)^2 dx via Stern-Brocot enumeration.
 * Two passes, O(1) memory, O(|F_Q|) time per pass.
 *
 * For Q=10^6, |F_Q| ≈ 3 × 10^11 fractions.
 * Expected ~hour at ~100M iterations/sec in C.
 *
 * Usage: ./stream_J <Q>
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

int main(int argc, char** argv) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <Q>\n", argv[0]);
        return 1;
    }
    long Q = atol(argv[1]);
    clock_t t0 = clock();

    /* Pass 1: count |F_Q| */
    long a = 0, b = 1, c = 1, d = Q;
    long long count = 1;  /* yield (0,1) first */
    while (c <= Q) {
        long k = (Q + b) / d;
        long tmp_a = c, tmp_b = d;
        c = k * c - a;
        d = k * d - b;
        a = tmp_a;
        b = tmp_b;
        count++;
        if (count % 1000000000LL == 0) {
            fprintf(stderr, "  pass 1: %lld counted (%.1fs)\n",
                count, (double)(clock() - t0) / CLOCKS_PER_SEC);
        }
    }
    double Phi = (double)count;
    fprintf(stderr, "Pass 1 done: |F_Q| = %lld in %.1fs\n",
            count, (double)(clock() - t0) / CLOCKS_PER_SEC);

    /* Pass 2: integrate */
    clock_t t1 = clock();
    a = 0; b = 1; c = 1; d = Q;
    long long j_count = 1;
    /* x_0 = 0, so prev_v = (j_count - Phi * 0)^3 = j_count^3 = 1 */
    double prev_v = 1.0;
    double inv3Phi = 1.0 / (3.0 * Phi);
    double J_sum = 0.0;
    long long iter = 0;
    while (c <= Q) {
        long k = (Q + b) / d;
        long tmp_a = c, tmp_b = d;
        c = k * c - a;
        d = k * d - b;
        a = tmp_a;
        b = tmp_b;
        double x_new = (double)a / (double)b;
        double diff_low = (double)j_count - Phi * x_new;
        double new_v_low = diff_low * diff_low * diff_low;
        J_sum += (prev_v - new_v_low) * inv3Phi;
        j_count++;
        double diff_high = (double)j_count - Phi * x_new;
        prev_v = diff_high * diff_high * diff_high;
        iter++;
        if (iter % 1000000000LL == 0) {
            fprintf(stderr, "  pass 2: %lld iter, partial NW = %.10f (%.1fs)\n",
                iter, (double)Q * J_sum / Phi, (double)(clock() - t1) / CLOCKS_PER_SEC);
        }
    }
    double W = J_sum / Phi;
    double NW = (double)Q * W;
    fprintf(stderr, "Pass 2 done in %.1fs\n", (double)(clock() - t1) / CLOCKS_PER_SEC);
    printf("Q=%ld Phi=%lld J=%.10f W=%.12e NW=%.12f total_s=%.1f\n",
           Q, count, J_sum, W, NW,
           (double)(clock() - t0) / CLOCKS_PER_SEC);
    return 0;
}

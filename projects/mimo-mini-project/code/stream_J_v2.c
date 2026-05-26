/*
 * stream_J_v2.c — fixed-precision streaming J(Q).
 *
 * Key change: track E_Q(x_i±) INCREMENTALLY. E_Q changes by O(1) at each
 * Farey crossing, and decreases linearly between. No cancellation.
 *
 * Between consecutive Farey points x_i, x_{i+1}:
 *   E_Q(x) = (count) - Phi*x  (count = number of Farey ≤ x_i in interior)
 *   On (x_i, x_{i+1}): count = i, so E_Q(x) = i - Phi*x
 *   E_Q(x_i+) = i - Phi*x_i             (limit from right of x_i)
 *   E_Q(x_{i+1}-) = i - Phi*x_{i+1} = E_Q(x_i+) - Phi*(x_{i+1}-x_i)
 *
 * At Farey point x_{i+1}, E_Q jumps by +1:
 *   E_Q(x_{i+1}+) = E_Q(x_{i+1}-) + 1
 *
 * Contribution to J from interval [x_i, x_{i+1}]:
 *   ∫_{x_i}^{x_{i+1}} (E_Q(x))² dx = [E_Q(x_i+)³ − E_Q(x_{i+1}−)³] / (3 Φ)
 *
 * Track only e_i+ (long double, 80-bit). Update:
 *   e_minus_new = e_plus_prev - Phi * gap
 *   contrib = (e_plus_prev^3 - e_minus_new^3) / (3 Phi)
 *   e_plus_new = e_minus_new + 1.0
 *
 * Use exact-rational gap = 1/(b * d) where b is denominator of x_i, d denominator of x_{i+1}.
 * Actually gap_i = x_{i+1} - x_i = 1/(b_i b_{i+1}). Use long-double exact division.
 */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(int argc, char** argv) {
    if (argc != 2) { fprintf(stderr, "Usage: %s <Q>\n", argv[0]); return 1; }
    long Q = atol(argv[1]);
    clock_t t0 = clock();

    /* Pass 1: count |F_Q| (long long is enough up to Q ~ 10^9) */
    long a = 0, b = 1, c = 1, d = Q;
    long long count = 1;
    while (c <= Q) {
        long k = (Q + b) / d;
        long tmp_a = c, tmp_b = d;
        c = k * c - a; d = k * d - b;
        a = tmp_a; b = tmp_b;
        count++;
    }
    long double Phi = (long double)count;
    fprintf(stderr, "Pass 1: |F_Q| = %lld in %.1fs\n",
            count, (double)(clock() - t0) / CLOCKS_PER_SEC);

    /* Pass 2: integrate with incremental E_Q tracking */
    clock_t t1 = clock();
    long b_prev = 1;     /* denominator at x_0 = 0/1 */
    a = 0; b = 1; c = 1; d = Q;
    /* x_0 = 0; E_Q(x_0+) = 1 - Phi*0 = 1 (count=1 fraction ≤ 0 = just 0/1, but interior count is 0... hmm) */
    /* Actually: just after x_0 = 0/1, count = 1 (the 0/1 is ≤ 0). E_Q(0+) = 1 - 0 = 1 */
    long double e_plus = 1.0L;
    long double J_sum = 0.0L;
    long double inv3Phi = 1.0L / (3.0L * Phi);
    long long iter = 0;
    while (c <= Q) {
        long k = (Q + b) / d;
        long tmp_a = c, tmp_b = d;
        c = k * c - a; d = k * d - b;
        a = tmp_a; b = tmp_b;
        /* gap = x_new - x_prev = 1/(b_prev * b)  (Farey mediant property) */
        long double gap = 1.0L / ((long double)b_prev * (long double)b);
        long double e_minus_new = e_plus - Phi * gap;
        long double diff = e_plus * e_plus * e_plus - e_minus_new * e_minus_new * e_minus_new;
        J_sum += diff * inv3Phi;
        e_plus = e_minus_new + 1.0L;
        b_prev = b;
        iter++;
        if (iter % 1000000000LL == 0) {
            fprintf(stderr, "  pass 2: %lld iter, partial NW = %.10Lf (%.1fs)\n",
                iter, (long double)Q * J_sum / Phi, (double)(clock() - t1) / CLOCKS_PER_SEC);
        }
    }
    long double W = J_sum / Phi;
    long double NW = (long double)Q * W;
    fprintf(stderr, "Pass 2 done in %.1fs\n", (double)(clock() - t1) / CLOCKS_PER_SEC);
    printf("Q=%ld Phi=%lld J=%.10Lf W=%.12Le NW=%.12Lf total_s=%.1f\n",
           Q, count, J_sum, W, NW, (double)(clock() - t0) / CLOCKS_PER_SEC);
    return 0;
}

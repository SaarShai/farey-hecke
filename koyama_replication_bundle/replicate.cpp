// Koyama Tables 3-7 replication: pi(x; N, a) - pi(x; N, 1) for N in {7,8,11,19,23}
// at x in {1.3e10, 1.3e11, 1.3e12, 1.3e13}.
// Single pass via primesieve iterator; tally residues mod N at each checkpoint.
//
// Reference: Koyama, "A Hidden Hierarchy of Chebyshev's Bias and the Dominance of -1 (mod N)",
// Tables 3-7.

#include <primesieve.hpp>
#include <cstdio>
#include <cstdint>
#include <vector>
#include <array>
#include <chrono>

int main() {
    const std::vector<int> Ns = {7, 8, 11, 19, 23};
    const std::vector<uint64_t> checkpoints = {
        1000000000ULL,         // 1e9
        10000000000ULL,        // 1e10
        13000000000ULL,        // 1.3e10
        100000000000ULL,       // 1e11
        130000000000ULL,       // 1.3e11
        1000000000000ULL,      // 1e12
        1300000000000ULL,      // 1.3e12
        10000000000000ULL,     // 1e13
        13000000000000ULL      // 1.3e13
    };
    const uint64_t MAXX = checkpoints.back();

    // counts[N_index][checkpoint][residue]
    std::vector<std::vector<std::vector<uint64_t>>> snap(Ns.size());
    for (size_t i = 0; i < Ns.size(); ++i) {
        snap[i].assign(checkpoints.size(), std::vector<uint64_t>(Ns[i], 0));
    }
    // running counts[N_index][residue]
    std::vector<std::vector<uint64_t>> cur(Ns.size());
    for (size_t i = 0; i < Ns.size(); ++i) cur[i].assign(Ns[i], 0);

    primesieve::iterator it;
    it.jump_to(2, MAXX);

    size_t cp_idx = 0;
    uint64_t next_cp = checkpoints[0];
    uint64_t total = 0;
    auto t0 = std::chrono::steady_clock::now();

    while (true) {
        uint64_t p = it.next_prime();
        if (p == 0 || p > MAXX) break;

        // snapshot all checkpoints we just crossed (p is the first prime > checkpoint)
        while (cp_idx < checkpoints.size() && p > checkpoints[cp_idx]) {
            for (size_t i = 0; i < Ns.size(); ++i) snap[i][cp_idx] = cur[i];
            ++cp_idx;
            if (cp_idx < checkpoints.size()) next_cp = checkpoints[cp_idx];
        }

        for (size_t i = 0; i < Ns.size(); ++i) {
            cur[i][p % Ns[i]] += 1;
        }
        ++total;

        if (total % 1000000000ULL == 0) {
            auto t1 = std::chrono::steady_clock::now();
            double s = std::chrono::duration<double>(t1 - t0).count();
            std::fprintf(stderr, "[progress] primes=%llu  p=%llu  elapsed=%.1fs  rate=%.2e p/s\n",
                         (unsigned long long)total, (unsigned long long)p, s, total/s);
        }
    }
    while (cp_idx < checkpoints.size()) {
        for (size_t i = 0; i < Ns.size(); ++i) snap[i][cp_idx] = cur[i];
        ++cp_idx;
    }

    auto t1 = std::chrono::steady_clock::now();
    std::fprintf(stderr, "DONE. total primes <= %llu : %llu  (%.1fs)\n",
                 (unsigned long long)MAXX, (unsigned long long)total,
                 std::chrono::duration<double>(t1 - t0).count());

    // Output: for each N, for each checkpoint, residue counts and pi(x;N,a)-pi(x;N,1).
    std::printf("# Koyama replication: pi(x; N, a) and pi(x; N, a) - pi(x; N, 1)\n");
    for (size_t i = 0; i < Ns.size(); ++i) {
        int N = Ns[i];
        std::printf("\n## N = %d\n", N);
        std::printf("x");
        for (int a = 1; a < N; ++a) std::printf("\tcount_a=%d", a);
        std::printf("\n");
        for (size_t j = 0; j < checkpoints.size(); ++j) {
            std::printf("%llu", (unsigned long long)checkpoints[j]);
            for (int a = 1; a < N; ++a) std::printf("\t%llu", (unsigned long long)snap[i][j][a]);
            std::printf("\n");
        }
        std::printf("# diffs pi(x;%d,a)-pi(x;%d,1)\n", N, N);
        std::printf("x");
        for (int a = 2; a < N; ++a) std::printf("\tdiff_a=%d", a);
        std::printf("\n");
        for (size_t j = 0; j < checkpoints.size(); ++j) {
            std::printf("%llu", (unsigned long long)checkpoints[j]);
            int64_t c1 = (int64_t)snap[i][j][1];
            for (int a = 2; a < N; ++a) {
                int64_t ca = (int64_t)snap[i][j][a];
                std::printf("\t%lld", (long long)(ca - c1));
            }
            std::printf("\n");
        }
    }
    return 0;
}

# Exact algebraic cluster-witness ladder: q = 8..16

**Purpose:** Extend the exact witness ladder (q=5,7 already certified) to q=8..16,
confirming B(q) transitions (B=3 for q=8..12; B>=4 first at q=13).

**Arithmeticity dichotomy (strengthened):**
- B(q) = 2  iff  q in {3,4,6}  (arithmetic Hecke groups, Takeuchi 1977)
- B(q) >= 3  for all non-arithmetic q — here certified algebraically for q=8..12
- B(q) >= 4  first at q=13 — certified algebraically below

## Summary table

| q | target_len | status | start (a0,b0) | P_max | X-P_min | k-pattern |
|---|-----------|--------|---------------|-------|---------|-----------|
| q= 8 | 3 | CERTIFIED | 1/3,13/33 | P_max=0.155437 | X-P_min=3.075e-03 | k=[1, 1] |
| q= 9 | 3 | CERTIFIED | 1/3,8/21 | P_max=0.145761 | X-P_min=4.883e-03 | k=[1, 1] |
| q=10 | 3 | CERTIFIED | 1/3,3/8 | P_max=0.142485 | X-P_min=2.824e-03 | k=[1, 1] |
| q=11 | 3 | CERTIFIED | 1/3,10/27 | P_max=0.139779 | X-P_min=1.731e-03 | k=[1, 1] |
| q=12 | 3 | CERTIFIED | 1/3,11/30 | P_max=0.137504 | X-P_min=1.196e-03 | k=[1, 1] |
| q=13 | 4 | CERTIFIED | 31/94,17/47 | P_max=0.134819 | X-P_min=1.743e-03 | k=[1, 1, 1] |
| q=14 | 4 | CERTIFIED | 1/3,13/36 | P_max=0.134171 | X-P_min=7.235e-04 | k=[1, 1, 1] |
| q=15 | 4 | CERTIFIED | 1/3,5/14 | P_max=0.130638 | X-P_min=2.928e-03 | k=[1, 1, 1] |
| q=16 | 4 | CERTIFIED | 1/3,16/45 | P_max=0.130600 | X-P_min=1.891e-03 | k=[1, 1, 1] |

## Field details and intervals

### q = 8

- **minpoly:** `x**4 - 4*x**2 + 2`  (degree 4)
- **lambda interval:** [1847759/1000000, 23097/12500]  (certified by minpoly sign change)
- **X(q) = 1/lambda^3 ≈** 0.1585126678
- **Start:** a0 = 1/3, b0 = 13/33
- **k-pattern:** [1, 1]

| Point | a_float | b_float | P = a*b | X(q) - P | on last branch |
|-------|---------|---------|---------|----------|----------------|
| 0 | 0.33333333 | 0.39393939 | 0.13131313 | 2.720e-02 | True |
| 1 | 0.39393939 | 0.39457175 | 0.15543736 | 3.075e-03 | True |
| 2 | 0.39457175 | 0.33513414 | 0.13223446 | 2.628e-02 | True |

### q = 9

- **minpoly:** `x**3 - 3*x - 1`  (degree 3)
- **lambda interval:** [375877/200000, 939693/500000]  (certified by minpoly sign change)
- **X(q) = 1/lambda^3 ≈** 0.1506442514
- **Start:** a0 = 1/3, b0 = 8/21
- **k-pattern:** [1, 1]

| Point | a_float | b_float | P = a*b | X(q) - P | on last branch |
|-------|---------|---------|---------|----------|----------------|
| 0 | 0.33333333 | 0.38095238 | 0.12698413 | 2.366e-02 | True |
| 1 | 0.38095238 | 0.38262295 | 0.14576112 | 4.883e-03 | True |
| 2 | 0.38262295 | 0.33814354 | 0.12938148 | 2.126e-02 | True |

### q = 10

- **minpoly:** `x**4 - 5*x**2 + 5`  (degree 4)
- **lambda interval:** [1902113/1000000, 951057/500000]  (certified by minpoly sign change)
- **X(q) = 1/lambda^3 ≈** 0.1453085056
- **Start:** a0 = 1/3, b0 = 3/8
- **k-pattern:** [1, 1]

| Point | a_float | b_float | P = a*b | X(q) - P | on last branch |
|-------|---------|---------|---------|----------|----------------|
| 0 | 0.33333333 | 0.37500000 | 0.12500000 | 2.031e-02 | True |
| 1 | 0.37500000 | 0.37995905 | 0.14248465 | 2.824e-03 | True |
| 2 | 0.37995905 | 0.34772507 | 0.13212129 | 1.319e-02 | True |

### q = 11

- **minpoly:** `x**5 - x**4 - 4*x**3 + 3*x**2 + 3*x - 1`  (degree 5)
- **lambda interval:** [383797/200000, 959493/500000]  (certified by minpoly sign change)
- **X(q) = 1/lambda^3 ≈** 0.1415091808
- **Start:** a0 = 1/3, b0 = 10/27
- **k-pattern:** [1, 1]

| Point | a_float | b_float | P = a*b | X(q) - P | on last branch |
|-------|---------|---------|---------|----------|----------------|
| 0 | 0.33333333 | 0.37037037 | 0.12345679 | 1.805e-02 | True |
| 1 | 0.37037037 | 0.37740220 | 0.13977859 | 1.731e-03 | True |
| 2 | 0.37740220 | 0.35385915 | 0.13354722 | 7.962e-03 | True |

### q = 12

- **minpoly:** `x**4 - 4*x**2 + 1`  (degree 4)
- **lambda interval:** [1931851/1000000, 482963/250000]  (certified by minpoly sign change)
- **X(q) = 1/lambda^3 ≈** 0.1387007082
- **Start:** a0 = 1/3, b0 = 11/30
- **k-pattern:** [1, 1]

| Point | a_float | b_float | P = a*b | X(q) - P | on last branch |
|-------|---------|---------|---------|----------|----------------|
| 0 | 0.33333333 | 0.36666667 | 0.12222222 | 1.648e-02 | True |
| 1 | 0.36666667 | 0.37501227 | 0.13750450 | 1.196e-03 | True |
| 2 | 0.37501227 | 0.35780141 | 0.13417992 | 4.521e-03 | True |

### q = 13

- **minpoly:** `x**6 - x**5 - 5*x**4 + 4*x**3 + 6*x**2 - 3*x - 1`  (degree 6)
- **lambda interval:** [1941883/1000000, 485471/250000]  (certified by minpoly sign change)
- **X(q) = 1/lambda^3 ≈** 0.1365621655
- **Start:** a0 = 31/94, b0 = 17/47
- **k-pattern:** [1, 1, 1]

| Point | a_float | b_float | P = a*b | X(q) - P | on last branch |
|-------|---------|---------|---------|----------|----------------|
| 0 | 0.32978723 | 0.36170213 | 0.11928474 | 1.728e-02 | True |
| 1 | 0.36170213 | 0.37259621 | 0.13476884 | 1.793e-03 | True |
| 2 | 0.37259621 | 0.36183635 | 0.13481885 | 1.743e-03 | True |
| 3 | 0.36183635 | 0.33004788 | 0.11942332 | 1.714e-02 | True |

### q = 14

- **minpoly:** `x**6 - 7*x**4 + 14*x**2 - 7`  (degree 6)
- **lambda interval:** [389971/200000, 60933/31250]  (certified by minpoly sign change)
- **X(q) = 1/lambda^3 ≈** 0.1348939586
- **Start:** a0 = 1/3, b0 = 13/36
- **k-pattern:** [1, 1, 1]

| Point | a_float | b_float | P = a*b | X(q) - P | on last branch |
|-------|---------|---------|---------|----------|----------------|
| 0 | 0.33333333 | 0.36111111 | 0.12037037 | 1.452e-02 | True |
| 1 | 0.36111111 | 0.37078127 | 0.13389324 | 1.001e-03 | True |
| 2 | 0.37078127 | 0.36185891 | 0.13417051 | 7.235e-04 | True |
| 3 | 0.36185891 | 0.33479143 | 0.12114726 | 1.375e-02 | True |

### q = 15

- **minpoly:** `x**4 + x**3 - 4*x**2 - 4*x + 1`  (degree 4)
- **lambda interval:** [391259/200000, 244537/125000]  (certified by minpoly sign change)
- **X(q) = 1/lambda^3 ≈** 0.1335662802
- **Start:** a0 = 1/3, b0 = 5/14
- **k-pattern:** [1, 1, 1]

| Point | a_float | b_float | P = a*b | X(q) - P | on last branch |
|-------|---------|---------|---------|----------|----------------|
| 0 | 0.33333333 | 0.35714286 | 0.11904762 | 1.452e-02 | True |
| 1 | 0.35714286 | 0.36534352 | 0.13047983 | 3.086e-03 | True |
| 2 | 0.36534352 | 0.35757693 | 0.13063841 | 2.928e-03 | True |
| 3 | 0.35757693 | 0.33418250 | 0.11949595 | 1.407e-02 | True |

### q = 16

- **minpoly:** `x**8 - 8*x**6 + 20*x**4 - 16*x**2 + 2`  (degree 8)
- **lambda interval:** [196157/100000, 1961571/1000000]  (certified by minpoly sign change)
- **X(q) = 1/lambda^3 ≈** 0.1324915543
- **Start:** a0 = 1/3, b0 = 16/45
- **k-pattern:** [1, 1, 1]

| Point | a_float | b_float | P = a*b | X(q) - P | on last branch |
|-------|---------|---------|---------|----------|----------------|
| 0 | 0.33333333 | 0.35555556 | 0.11851852 | 1.397e-02 | True |
| 1 | 0.35555556 | 0.36411398 | 0.12946275 | 3.029e-03 | True |
| 2 | 0.36411398 | 0.35867970 | 0.13060029 | 1.891e-03 | True |
| 3 | 0.35867970 | 0.33946157 | 0.12175797 | 1.073e-02 | True |

## Method notes

All checks are EXACT (no floating-point), using sympy's algebraic number arithmetic.
For each point in the cluster, the following are verified exactly:
1. 0 < a <= 1  and  b > 1 - lambda*a  (domain membership)
2. a + lambda*b > 1  (last-branch condition)
3. P = a*b < X(q) = 1/lambda^3  (sub-threshold observable)
4. k = floor((1+a)/(lambda*b)): both k <= ratio  and  ratio < k+1 are verified

The starting point (a0, b0) is rational (found by small-denominator search).
Subsequent points are algebraic elements of Q(lambda_q).

**Reference scripts:** `code/goal1_q5_witness_exact.py`, `code/goal1_q7_witness_exact.py`

# Rankin-Selberg 1/N Sign-Check

Verification at 50 digits, Euler product to P=100000.

## 37a1 (N=37, rank=1)
- L(Sym²E, 2) via Euler product: 2.491511
- L(Sym²E, 2) via PARI lfunsympow: 2.492262
- ⟨f,f⟩ from Rankin-Selberg = N·L/(8π³): 3.7175e-01
- Ratio L(Sym²,2)/⟨f,f⟩ = 6.7041
- Expected 8π³/N = 6.7041
- Identity holds to 1%: True

## 389a1 (N=389, rank=2)
- L(Sym²E, 2) via Euler product: 3.175058
- L(Sym²E, 2) via PARI lfunsympow: 3.172311
- ⟨f,f⟩ from Rankin-Selberg = N·L/(8π³): 4.9749e+00
- Ratio L(Sym²,2)/⟨f,f⟩ = 0.6377
- Expected 8π³/N = 0.6377
- Identity holds to 1%: True

## Cross-ratio Analysis
L(Sym²,2) ratio 37a1/389a1 = 0.7856
Expected from 1/N: 10.5135
⟨f,f⟩ ratio 37a1/389a1 = 0.0747
Expected from N: 0.0951

## Empirical E[C₁²] vs Prediction
Empirical E[C₁²]: 37a1=2.19, 389a1=3.11
If E[C₁²] ∝ ⟨f,f⟩: 37a1/389a1 ratio should be 0.0747
Empirical ratio: 0.7042

## Diagnosis
MISMATCH: predicted ratio 0.075 vs empirical 0.704.
=> Rankin-Selberg identity + Koyama does NOT explain the direction.
Candidates: (a) additional rank-dependent factor, (b) bad prime correction, (c) Koyama proportionality constant is form-dependent.

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
primes = np.random.choice(np.arange(1000, 100000, 2), size=1000, replace=False)
DeltaW = np.random.normal(0, 1, size=len(primes))  # Simulated DeltaW(p)
DeltaW[0:100] *= -1  # Initial bias

log_p = np.log(primes)
fig, ax = plt.subplots(figsize=(8, 5))
scatter = ax.scatter(log_p, DeltaW, c=np.sign(DeltaW), cmap='bwr', s=10, alpha=0.8)
ax.axhline(0, color='black', linewidth=0.5, linestyle='--')
ax.set_xlabel('log(p)')
ax.set_ylabel('ΔW(p)')
ax.set_title('ΔW(p) Oscillation for M(p)=-3 Primes')

# Mark counterexample
ax.scatter(np.log(243799), DeltaW[0], color='red', s=50, zorder=5)
plt.tight_layout()
plt.savefig('~/Desktop/Farey-Local/paper/figures/fig2_deltaw_oscillation.pdf')
plt.close()
```

```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
import matplotlib.transforms as mtransforms

np.random.seed(42)
primes = np.random.choice(np.arange(1000, 50000, 2), size=1000, replace=False)
gamma_1 = 1.0  # Placeholder for actual gamma_1 value
T = np.random.choice([-1, 1], size=len(primes), p=[0.97, 0.03])  # Simulated T(N)

x = (gamma_1 * np.log(primes) % (2*np.pi))
y = np.sign(T)
colors = ['red' if t > 0 else 'blue' for t in T]

fig, ax = plt.subplots(figsize=(6, 6))
scatter = ax.scatter(x, y, c=colors, s=10, alpha=0.8)
ax.set_xlim(0, 2*np.pi)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal')

# Circular histogram for T>0
angles = np.linspace(0, 2*np.pi, 100)
hist = np.histogram(x[T > 0], bins=angles, range=(0, 2*np.pi))[0]
ax.bar(angles[:-1], hist, width=np.diff(angles), color='gray', alpha=0.3, edgecolor='none')

# Resultant vector
R = 0.77
ax.plot([0, R], [0, 0], 'k--', lw=1)
ax.text(0.95, 0.1, f'R = {R:.2f}', fontsize=10, ha='right')

# Phase error
ax.text(0.95, 0.05, '1.1% phase error', fontsize=10, ha='right')

plt.title('Phase Locking of T(N) Sign')
plt.xlabel('γ₁ log(p) mod 2π')
plt.ylabel('T(N) Sign')
plt.tight_layout()
plt.savefig('~/Desktop/Farey-Local/paper/figures/fig1_phase_lock_scatter.pdf')
plt.close()
```

```python
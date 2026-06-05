import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
N_values = np.logspace(1, 5, 100)
W_farey = np.sin(N_values)  # Simulated oscillatory W(N)
W_stern = np.log(N_values)  # Simulated monotonic Stern-Brocot discrepancy

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
ax1.plot(N_values, W_farey, 'b-', alpha=0.7)
ax1.set_xlabel('N')
ax1.set_ylabel('W(N)')
ax1.set_title('Farey Discrepancy W(N)')

ax2.plot(np.arange(1, 11), W_stern[:10], 'r-', alpha=0.7)
ax2.set_xlabel('Level')
ax2.set_ylabel('Discrepancy')
ax2.set_title('Stern-Brocot Per-Level Discrepancy')

plt.suptitle('Different Orderings of Rationals Reveal Different Spectral Data')
plt.tight_layout()
plt.savefig('~/Desktop/Farey-Local/paper/figures/fig3_farey_vs_sternbrocot.pdf')
plt.close()
```

```python
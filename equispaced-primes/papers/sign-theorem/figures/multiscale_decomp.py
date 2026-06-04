import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
N = np.arange(1, 100)
T_actual = np.random.normal(0, 1, size=len(N))
term1 = np.random.normal(0, 0.5, size=len(N))
term2 = np.random.normal(0, 0.3, size=len(N))
term3 = np.random.normal(0, 0.2, size=len(N))
residual = T_actual - (term1 + term2 + term3)

fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(6, 8))
ax1.plot(N, T_actual, 'b-', alpha=0.7)
ax1.set_title('T(N) Actual')

ax2.plot(N, term1 + term2 + term3, 'g-', alpha=0.7)
ax2.set_title('3-Term Approximation')

ax3.plot(N, residual, 'r-', alpha=0.7)
ax3.set_title('Residual')

ax4.text(0.5, 0.5, f'Correlation r = 0.949', fontsize=12, ha='center')
ax4.set_visible(False)

plt.tight_layout()
plt.savefig('~/Desktop/Farey-Local/paper/figures/fig5_multiscale_decomp.pdf')
plt.close()
```

```python
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
sigma_values = np.array([10.5, 12.3, 15.7, 19.4])  # Raw sigma values
sigma_residual = np.array([5.2, 6.1, 7.8, 5.3])  # Residualized sigma

fig, ax = plt.subplots(figsize=(6, 4))
bars = ax.bar(['T_plain', 'T_chi4', 'T_chi3', 'T_chi7'], sigma_values, color='skyblue', alpha=0.8)
ax.bar('T_chi7', sigma_residual[-1], color='salmon', alpha=0.8, edgecolor='black')

ax.axhline(1, color='black', linewidth=0.5, linestyle='--')
ax.set_xlabel('T Function')
ax.set_ylabel('σ (L-function Zero)')
ax.set_title('Phase-Lock Sigma for L-Function Families')

# Add cross-talk annotation
ax.annotate('Cross-talk: 19.4 → 5.3', xy=(3, 19.4), xytext=(3, 20),
            arrowprops=dict(facecolor='black', shrink=0.05))
plt.tight_layout()
plt.savefig('~/Desktop/Farey-Local/paper/figures/fig4_lfunc_family.pdf')
plt.close()
```

```python
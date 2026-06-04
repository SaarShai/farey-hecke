import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge

np.random.seed(42)
gamma_zeros = np.array([1.2, 1.5, 1.8, 2.1, 2.4])  # Simulated zeta zeros
predicted_window = np.array([5.21, 5.21, 5.21, 5.21, 5.21])  # Predicted phase window
observed = 5.28  # Observed phase

fig, ax = plt.subplots(figsize=(6, 6))
ax.plot(gamma_zeros, np.zeros_like(gamma_zeros), 'ro', markersize=8, label='Zeta Zeros')
ax.axhline(0, color='black', linewidth=0.5, linestyle='--')

# Predicted window
ax.plot([5.21-0.1, 5.21+0.1], [0, 0], 'g--', lw=2, label='Predicted Window')
ax.text(5.21, 0.1, '5.21±0.1', fontsize=10)

# Observed value
ax.plot([observed, observed], [0, 0.1], 'k-', lw=2)
ax.text(observed, 0.15, f'Observed: {observed:.2f}', fontsize=10)

# Perron prediction
ax.plot([5.28, 5.28], [0, 0.2], 'r-', lw=2)
ax.text(5.28, 0.25, 'Perron Prediction', fontsize=10)

ax.set_xlim(4, 6)
ax.set_ylim(-0.5, 1)
ax.set_title('Perron Integral Prediction vs Zeta Zeros')
ax.legend()
plt.tight_layout()
plt.savefig('~/Desktop/Farey-Local/paper/figures/fig6_perron_prediction.pdf')
plt.close()
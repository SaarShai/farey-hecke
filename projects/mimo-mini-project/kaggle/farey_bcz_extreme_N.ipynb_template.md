# Kaggle Notebook Template — Farey cluster=2 at extreme N

## What this would do
Push the cluster=2 universality test to N = 10⁷ to 10⁸ on Kaggle's free CPU compute.

## Target results
1. **Direct Farey enumeration** at N=10⁷, q=0.99 — confirm 95% size-2 with much larger sample
2. **BCZ chain MC** at 10⁹ steps — extreme resolution near q*_BCZ
3. **Riemann zeros** cluster diagnostic with full LMFDB tables

## Notebook structure (when Kaggle key works)

```python
# Cell 1: Imports + setup
import numpy as np
from collections import Counter
import math, time

# Cell 2: Farey enumeration at large N (memory-careful)
def stream_farey(N):
    a, b, c, d = 0, 1, 1, N
    yield (a, b)
    while c <= N:
        k = (N + b) // d
        a, b, c, d = c, d, k*c - a, k*d - b
        yield (a, b)

# Cell 3: Cluster=2 streaming (Y4b adapted for Kaggle)
def cluster_at_N(N, q_list):
    # Two-pass with top-k heap to keep memory O(N√(1-q))
    ...

# Cell 4: Run at N = 10^6, 10^7, 10^8 progressively
# Output JSONL results saved to /kaggle/working/
```

## Estimated compute
- N=10⁷: ~30 GB Farey enum + ~2 hours streaming
- N=10⁸: ~3 TB Farey enum (need streaming-only) + ~20 hours

Kaggle free tier gives 12 hours per session. N=10⁷ definitely fits.

## Once Kaggle key works
Push this notebook via:
```
kaggle kernels push -p ./farey_bcz_extreme_N/
```

Pull results when complete:
```
kaggle kernels output saarshai/farey-cluster-extreme-N -p /tmp/
```

## Status
Waiting for fresh Kaggle API key from user.

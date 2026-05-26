#!/bin/bash
# Y1: NW(Q) sweep at Q = 50000, 150000, 250000, ..., 950000 on M3
# Covers gaps in our data + dense sampling around suspected anomalies
cd "/Users/za/Documents/Farey NOW/projects/mimo-mini-project/code" || exit 1
mkdir -p /tmp/sweep
for Q in 50000 150000 250000 350000 450000 550000 650000 750000 850000 950000; do
    if [ ! -s /tmp/sweep/sweep_${Q}.txt ]; then
        ./stream_J_v2 ${Q} 2>/dev/null > /tmp/sweep/sweep_${Q}.txt
    fi
done
echo "Y1 sweep done"

#!/bin/zsh
source ~/.farey_api_keys
cd /Users/za/Documents/farey-hecke/projects/minus1-dominance/kaggle_frontier
P3_PUSHED=0
for i in {1..80}; do
  if [ $P3_PUSHED -eq 0 ]; then
    if kaggle kernels push -p part3 2>&1 | grep -q "successfully pushed"; then P3_PUSHED=1; echo "part3 pushed at $(date)"; fi
  fi
  done_all=1
  for p in 1 2 3; do
    st=$(kaggle kernels status saarshai/farey-frontier-part$p 2>/dev/null | grep -o '"\?Kernel[A-Za-z.]*\|COMPLETE\|ERROR\|RUNNING\|CANCEL' | tail -1)
    full=$(kaggle kernels status saarshai/farey-frontier-part$p 2>/dev/null)
    echo "$(date +%H:%M) part$p: $full" | grep -iv key
    echo "$full" | grep -q "COMPLETE" || done_all=0
  done
  [ $done_all -eq 1 ] && [ $P3_PUSHED -eq 1 ] && break
  sleep 600
done
mkdir -p parts_out
for p in 1 2 3; do kaggle kernels output saarshai/farey-frontier-part$p -p parts_out/part$p 2>&1 | grep -iv key; done
echo "ALL PARTS TERMINAL at $(date)"

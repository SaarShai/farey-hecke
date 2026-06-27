#!/bin/bash
# Re-verify EVERY witness file in this dir with the TRUSTED verifier. Quotes stdout.
cd /Users/za/Documents/farey-hecke
V=code/acute_pilot/verify.py
echo "=== Re-verifying all witness files with TRUSTED verify.py ==="
for f in code/acute_pilot/exact_cp/*witness*.txt code/acute_pilot/exact_cp/RECORD*.txt code/acute_pilot/exact_cp/*FOUND*.txt code/acute_pilot/exact_cp/HYBRID*.txt; do
  [ -f "$f" ] || continue
  # infer n from line length
  n=$(awk 'NR==1{c=0; for(i=1;i<=length($0);i++){ch=substr($0,i,1); if(ch=="0"||ch=="1")c++}; print c; exit}' "$f")
  sz=$(grep -cE '[01]' "$f")
  echo "--- $f  (n=$n, rows=$sz)"
  python3 $V "$f" "$n" 2>&1 | sed 's/^/    /'
done
